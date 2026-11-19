#!/usr/bin/env python3
"""A stand-in for the PACE-Phoenix cluster in the pace tasks, installed as pace, ssh, scp, rsync and the Slurm commands.

Every call is appended to cluster.log in the run's workspace, so a check can see what the agent ran, and nothing
reaches the real cluster. Remote paths ("~/..." or "$HOME/...") map to the workspace's remote/ directory. The canned
answers come from the workspace's cluster.json: "pace" maps a subcommand to its output, and "ssh" is a list of rules
({"match": [regex, ...], "out": text}) tried before the file-backed commands (ls, cat, head, tail, du, find).
Help, version, cost and list-defaults run the real pace, whose own ssh calls come back here.
"""
from __future__ import annotations

import fnmatch
import json
import os
import re
import shlex
import shutil
import sys
from pathlib import Path

WORKSPACE = Path(os.environ["FAKE_CLUSTER_DIR"])
SCENARIO = json.loads((WORKSPACE / "cluster.json").read_text(encoding="utf-8"))
REMOTE = WORKSPACE / "remote"
REAL_PACE = Path.home() / ".local/bin/pace"
SUBMIT = {"run", "gpu-run", "gpu-shell", "start", "start-cpu"}


def log(tool: str, argv: list[str]) -> None:
    with (WORKSPACE / "cluster.log").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"tool": tool, "argv": argv, "cwd": os.getcwd()}) + "\n")


def remote_path(text: str) -> Path:
    text = text.strip().strip("'\"")
    for prefix in ("~/", "$HOME/", "${HOME}/"):
        if text.startswith(prefix):
            return REMOTE / text[len(prefix):]
    if text in ("~", "$HOME"):
        return REMOTE
    return REMOTE / text.lstrip("/")


def show(path: Path) -> str:
    if path.is_dir():
        return "\n".join(sorted(child.name + ("/" if child.is_dir() else "") for child in path.iterdir())) + "\n"
    return path.read_text(encoding="utf-8", errors="replace")


def file_command(command: str) -> str | None:
    """Answer a simple remote shell command from the mirrored cluster files, or None when it is not one."""
    out = []
    for part in re.split(r"\s*(?:&&|;|\|\|)\s*", command):
        words = shlex.split(part) if part.strip() else []
        if not words:
            continue
        name, args = words[0], [word for word in words[1:] if not word.startswith("-")]
        if name in {"ls", "cat", "head", "tail", "less", "du", "find", "wc", "stat"}:
            for arg in args or ["~"]:
                if arg.isdigit():
                    continue
                path = remote_path(arg)
                matches = sorted(path.parent.glob(path.name)) if any(c in path.name for c in "*?[") else [path]
                for match in matches:
                    if not match.exists():
                        out.append(f"{name}: {arg}: No such file or directory\n")
                    elif name == "du":
                        size = sum(f.stat().st_size for f in match.rglob("*") if f.is_file()) if match.is_dir() else match.stat().st_size
                        out.append(f"{max(size // 1024, 1)}K\t{arg}\n")
                    elif name == "find":
                        out.append("".join(f"{arg.rstrip('/')}/{f.relative_to(match)}\n" for f in sorted(match.rglob("*"))))
                    elif name in {"tail", "head"} and match.is_file():
                        lines = match.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
                        out.append("".join(lines[-40:] if name == "tail" else lines[:40]))
                    else:
                        out.append(show(match))
        elif name in {"echo", "cd", "true", "hostname", "whoami", "printf"}:
            out.append(" ".join(words[1:]) + "\n" if name == "echo" else "")
        else:
            return None
    return "".join(out)


def ssh(argv: list[str]) -> int:
    words, index = argv[:], 0
    while index < len(words) and words[index].startswith("-"):
        index += 2 if words[index] in {"-o", "-i", "-p", "-l", "-F", "-J"} else 1
    command = " ".join(words[index + 1:])  # words[index] is the host
    for rule in SCENARIO.get("ssh", []):
        if all(re.search(pattern, command) for pattern in rule["match"]):
            sys.stdout.write(rule["out"])
            return rule.get("code", 0)
    if re.search(r"\b(sbatch|salloc|srun|scancel)\b", command):
        sys.stdout.write("Submitted batch job 9199999\n" if "sbatch" in command else "")
        return 0
    answer = file_command(command)
    sys.stdout.write(answer or "")
    return 0


def copy(source: Path, destination: Path, contents: bool, excludes: list[str]) -> None:
    def ignored(directory, names):
        return [name for name in names if any(fnmatch.fnmatch(name, pattern.strip("/")) for pattern in excludes)]
    if source.is_dir():
        target = destination if contents else destination / source.name
        shutil.copytree(source, target, dirs_exist_ok=True, ignore=ignored)
    elif source.exists():
        target = destination / source.name if destination.is_dir() else destination
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    else:
        sys.stderr.write(f'rsync: link_stat "{source}" failed: No such file or directory (2)\n')


def transfer(tool: str, argv: list[str]) -> int:
    excludes, paths, dry = [], [], False
    takes_value = {"-e", "--rsh", "-i", "-o", "-F", "-J"} | ({"-P"} if tool == "scp" else set())
    words = iter(argv)
    for word in words:
        if word.startswith("--exclude="):
            excludes.append(word.split("=", 1)[1])
        elif word == "--exclude":
            excludes.append(next(words, ""))
        elif word in takes_value:
            next(words, None)
        elif tool == "rsync" and (word == "--dry-run" or (word.startswith("-") and not word.startswith("--") and "n" in word[1:])):
            dry = True
        elif not word.startswith("-"):
            paths.append(word)
    if len(paths) < 2:
        return 0
    *sources, destination = paths
    remote = re.compile(r"^[\w.@-]+:")
    for source in sources:
        contents = source.endswith("/")
        if remote.match(source):
            src, dst = remote_path(remote.sub("", source)), Path(destination)
        else:
            src, dst = Path(source), remote_path(remote.sub("", destination))
        if dry:
            sys.stdout.write(f"(dry run) {source} -> {destination}\n")
            continue
        if not dst.suffix or dst.is_dir() or destination.endswith("/"):
            dst.mkdir(parents=True, exist_ok=True)
        copy(src, dst, contents, excludes)
    return 0


def pace(argv: list[str]) -> int:
    command = argv[0] if argv else ""
    if command in {"", "help", "--help", "-h", "version", "cost", "list-defaults"} or "--help" in argv or "-h" in argv:
        os.execv(str(REAL_PACE), [str(REAL_PACE), *argv])
    canned = SCENARIO.get("pace", {})
    for key in (" ".join(argv[:2]), command):
        if key in canned:
            sys.stdout.write(canned[key])
            return 0
    if command in {"run", "gpu-run"}:
        sys.stdout.write("[pace] Syncing project files...\n[pace] Submitted batch job 9199999\n")
        return 0
    if command == "sync" and len(argv) > 1:
        job = argv[1]
        run = SCENARIO.get("sync_runs", {}).get(job)
        if not run:
            sys.stderr.write(f"[pace] Error: no run directory found for job {job}\n")
            return 1
        destination = Path(argv[argv.index("--dest") + 1]) if "--dest" in argv else Path(".")
        copy(remote_path(run), destination, True, [])
        receipt = Path("runs/fetched") / f"{Path(run).name}.json"
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(json.dumps({"run": Path(run).name, "job": job}) + "\n")
        sys.stdout.write(f"[pace] Synced {run} -> {destination}\n[pace] Wrote receipt {receipt}; commit it before the next run.\n")
        return 0
    sys.stdout.write("")
    return 0


def main() -> int:
    tool, argv = Path(sys.argv[0]).name, sys.argv[1:]
    log(tool, argv)
    if tool == "pace":
        return pace(argv)
    if tool == "ssh":
        return ssh(argv)
    if tool in {"rsync", "scp"}:
        return transfer(tool, argv)
    if tool in {"sbatch", "salloc", "squeue", "sacct", "sinfo", "scontrol", "sshare"}:
        sys.stderr.write(f"{tool}: command not found on this machine; Slurm runs on the cluster\n")
        return 127
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
