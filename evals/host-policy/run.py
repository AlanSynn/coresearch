#!/usr/bin/env python3
"""Run the host-policy evaluation: each task under each instruction arm on each host, in isolated workspaces.

Arms differ only in the global instructions and the skills they ship. Claude Code runs with
`--setting-sources project,local`, so the user's own CLAUDE.md, settings and skills stay out; the arm's global
instructions sit in a CLAUDE.md above the task repository and its skills in the repository's `.claude/skills`.
Codex runs with a temporary CODEX_HOME holding the arm's AGENTS.md, a minimal config and the arm's skills; a copy of
the user's auth.json is placed there for the run and deleted right after it.

Every model is named on the command line. Fable and Astra run only within a grant the user made (grants.py), and a
hook in every run stops a subagent from switching to a top-tier family the run has no grant for.
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import datetime as dt
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import grants  # noqa: E402
import tasks as task_module  # noqa: E402

spec = importlib.util.spec_from_file_location("coresearch_cli", ROOT / "scripts/coresearch.py")
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)

CLAUDE_SETTINGS = json.dumps({"pluginConfigs": {"cc-plugin-agents-md@builtin": {"options": {"instructionFiles": "claude-md-and-agents-md"}}}})


CANDIDATE_SKILLS: dict[str, Path] = {}  # skills kept outside this checkout, added to the candidate arm (--candidate-skill)
CLUSTER_TOOLS = ("pace", "ssh", "scp", "rsync", "sshfs", "sbatch", "salloc", "squeue", "sacct", "sinfo", "scontrol", "sshare")
# Absolute paths would bypass the stand-in cluster tools on PATH, so Claude Code may not call them directly.
CLUSTER_DENY = [f"Bash({path}:*)" for path in ("/usr/bin/ssh", "/usr/bin/scp", "/usr/bin/rsync", "/opt/homebrew/bin/rsync")]


def arm_material(arm: str, host: str, baseline: Path) -> tuple[str, dict[str, Path]]:
    """Global instructions text and {skill name: source dir} for an arm on a host."""
    if arm == "candidate":
        text = cli.render(host)
        skills = {name: ROOT / "skills" / name for name in cli.skills()} | CANDIDATE_SKILLS
    else:
        text = (baseline / f"{host}_global.md").read_text(encoding="utf-8")
        skills = {path.name: path for path in sorted((baseline / "skills").iterdir())
                  if path.name != "frontend-skill" and (path / "SKILL.md").is_file()}
    if host == "codex":
        skills["frontend-skill"] = baseline / "skills/frontend-skill"
    return text, skills


SKILL_FILE = re.compile(r"skills/([a-z0-9-]+)/((?:references/)?[\w.-]+\.md)")
# A call of the glm-delegate script with an option, a redirect or a quoted brief; reading its SKILL.md or
# "command -v glm-delegate" is not one.
GLM_CALL = re.compile(r"glm-delegate(?=\s+[-<\"'])")


def tool_calls(transcript: str, host: str) -> list[str]:
    """The agent's tool-call inputs as text (not tool output, which can merely list or echo things): Claude Code's
    tool_use inputs, with Skill calls as 'Skill <name>', and Codex's executed commands."""
    calls = []
    for line in transcript.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if host == "claude" and event.get("type") == "assistant":
            for item in event.get("message", {}).get("content", []):
                if isinstance(item, dict) and item.get("type") == "tool_use":
                    arguments = item.get("input", {})
                    if item.get("name") == "Skill" and isinstance(arguments, dict):
                        calls.append(f"Skill {arguments.get('skill') or arguments.get('command')}")
                    calls.append(json.dumps(arguments))
        elif host == "codex" and event.get("type") == "item.completed":
            item = event.get("item", {})
            if item.get("type") == "command_execution":
                calls.append(str(item.get("command", "")))
    return calls


def skill_files(calls: list[str]) -> list[str]:
    """Skill files the agent opened, such as 'engineering/references/design.md'."""
    found: set[str] = set()
    for text in calls:
        if text.startswith("Skill "):
            found.add(f"{text.split(' ', 1)[1]}/SKILL.md")
        found.update(f"{match.group(1)}/{match.group(2)}" for match in SKILL_FILE.finditer(text))
    return sorted(found)


def trace_fields(task, calls: list[str]) -> dict:
    """Per-run fields read from the tool calls: skill files, glm-delegate calls, and the task's own trace signals."""
    fields = {"skill_files": skill_files(calls), "glm_calls": sum(bool(GLM_CALL.search(text)) for text in calls)}
    if task.trace_check:
        fields["trace"] = task.trace_check(calls)
    return fields


def copy_skills(skills: dict[str, Path], destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name, source in skills.items():
        shutil.copytree(source.resolve(), destination / name, symlinks=False,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def stand_in_cluster(task, workspace: Path) -> dict[str, str]:
    """Build the stand-in PACE cluster for a pace task and return the environment that puts its tools first on PATH."""
    (workspace / "cluster.json").write_text(json.dumps(task.cluster(workspace), indent=2), encoding="utf-8")
    tools = workspace / "bin"
    tools.mkdir()
    for name in CLUSTER_TOOLS:
        shutil.copy2(HERE / "fakecluster.py", tools / name)
        os.chmod(tools / name, 0o755)
    path = f"{tools}:{os.environ['PATH']}"
    # Claude Code's shell snapshot re-applies the user's shell profile, which puts ~/.local/bin (the real pace) first;
    # its environment file runs after the snapshot, before each command.
    (workspace / "cluster-env.sh").write_text(f'export PATH="{tools}:$PATH"\nexport FAKE_CLUSTER_DIR="{workspace}"\n')
    return {"PATH": path, "FAKE_CLUSTER_DIR": str(workspace), "CLAUDE_ENV_FILE": str(workspace / "cluster-env.sh")}


def run_one(task, host: str, arm: str, out: Path, baseline: Path, models: dict, timeout: int) -> dict:
    workspace = out / f"{task.id}__{host}__{arm}"
    repo = workspace / "repo"
    workspace.mkdir(parents=True)
    task.build(repo)
    cluster_env = stand_in_cluster(task, workspace) if task.cluster else {}
    text, skills = arm_material(arm, host, baseline)
    started = time.time()
    record = {"task": task.id, "host": host, "arm": arm, "model": models[host]}
    try:
        if host == "claude":
            (workspace / "CLAUDE.md").write_text(text, encoding="utf-8")
            copy_skills(skills, repo / ".claude/skills")
            exclude = repo / ".git/info/exclude" if (repo / ".git").is_dir() else None
            if exclude:
                exclude.parent.mkdir(parents=True, exist_ok=True)
                with exclude.open("a") as stream:
                    stream.write("\n.claude/skills/\n")
            settings = json.loads(CLAUDE_SETTINGS)
            settings["hooks"] = {"PreToolUse": [{"matcher": "Agent|Task", "hooks": [
                {"type": "command", "command": grants.guard_command(models["blocked"]["claude"], workspace)}]}]}
            if task.cluster:
                settings["permissions"] = {"deny": CLUSTER_DENY}
            command = ["claude", "-p", "--model", models["claude"], "--effort", models["claude_effort"],
                       "--setting-sources", "project,local", "--settings", json.dumps(settings),
                       "--permission-mode", "bypassPermissions", "--output-format", "stream-json", "--verbose",
                       "--no-session-persistence", task.prompt]
            result = subprocess.run(command, cwd=repo, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                    timeout=timeout, env={**grants.model_free_env(), **cluster_env})
            (workspace / "transcript.jsonl").write_text(result.stdout)
            (workspace / "stderr.txt").write_text(result.stderr)
            data = {}
            for line in result.stdout.splitlines():  # the last event, of type result, carries the answer and usage
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(event, dict) and event.get("type") == "result":
                    data = event
            record.update(trace_fields(task, tool_calls(result.stdout, "claude")))
            final = data.get("result", "")
            usage = data.get("usage", {})
            if "hit your" in final and "limit" in final:
                record.update(exit="rate-limited")
                (workspace / "record.json").write_text(json.dumps(record, indent=2))
                return record
            record.update(exit=result.returncode, turns=data.get("num_turns"), cost_usd=data.get("total_cost_usd"),
                          input_tokens=usage.get("input_tokens", 0) + usage.get("cache_creation_input_tokens", 0)
                          + usage.get("cache_read_input_tokens", 0),
                          output_tokens=usage.get("output_tokens"), is_error=data.get("is_error"))
        else:
            home = workspace / "codex-home"
            home.mkdir(mode=0o700)
            shutil.copy2(Path.home() / ".codex/auth.json", home / "auth.json")
            os.chmod(home / "auth.json", 0o600)
            (home / "AGENTS.md").write_text(text, encoding="utf-8")
            extra = [models["codex_config"], models["candidate_codex_config"] if arm == "candidate" else "",
                     # Non-login shells keep the stand-in cluster tools first on PATH; the sandbox keeps the network off.
                     "allow_login_shell = false" if task.cluster else ""]
            (home / "config.toml").write_text(f'model = "{models["codex"]}"\nmodel_reasoning_effort = "{models["codex_effort"]}"\n'
                                              + "".join(line + "\n" for line in extra if line))
            copy_skills(skills, home / "skills")
            grants.write_codex_hooks(home, models["blocked"]["codex"], workspace)
            # The only hooks in this temporary home are the evaluation's own, so they run without a trust review.
            command = ["codex", "exec", "--dangerously-bypass-hook-trust", "--json", "-o", str(workspace / "final.txt"),
                       "--sandbox", "workspace-write", "--skip-git-repo-check", task.prompt]
            try:
                # An open stdin makes codex exec wait for more input, so close it.
                result = subprocess.run(command, cwd=repo, stdin=subprocess.DEVNULL, capture_output=True, text=True,
                                        timeout=timeout, env={**grants.model_free_env(), **cluster_env, "CODEX_HOME": str(home)})
            finally:
                (home / "auth.json").unlink(missing_ok=True)
            (workspace / "events.jsonl").write_text(result.stdout)
            (workspace / "stderr.txt").write_text(result.stderr[-20000:])
            record.update(trace_fields(task, tool_calls(result.stdout, "codex")))
            final = (workspace / "final.txt").read_text() if (workspace / "final.txt").exists() else ""
            usage = {"input_tokens": 0, "output_tokens": 0, "turns": 0}
            for line in result.stdout.splitlines():
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("type") == "turn.completed":
                    usage["turns"] += 1
                    usage["input_tokens"] += event.get("usage", {}).get("input_tokens", 0)
                    usage["output_tokens"] += event.get("usage", {}).get("output_tokens", 0) + event.get("usage", {}).get("reasoning_output_tokens", 0)
            record.update(exit=result.returncode, turns=usage["turns"], input_tokens=usage["input_tokens"],
                          output_tokens=usage["output_tokens"])
        (workspace / "final.md").write_text(final)
        record["checks"] = task.check(repo, final)
        record["final_chars"] = len(final)
    except subprocess.TimeoutExpired:
        record.update(exit="timeout", checks=task.check(repo, ""))
    except Exception as error:  # keep the batch running and record the failure
        record.update(exit="harness-error", error=f"{type(error).__name__}: {error}")
    finally:
        record["seconds"] = round(time.time() - started, 1)
        record["subagent_models"] = grants.guard_log(workspace)
        if task.flatpack:
            record.setdefault("checks", {})
            subprocess.run(["git", "-C", str(task_module.FLATPACK), "worktree", "remove", "--force", str(repo)],
                           capture_output=True)
    (workspace / "record.json").write_text(json.dumps(record, indent=2))
    return record


def recheck(run_dir: Path) -> int:
    """Recompute deterministic checks from saved workspaces after a check is corrected; flatpack worktrees are gone,
    so their repository checks keep the recorded values and only text checks are recomputed."""
    records = [json.loads(line) for line in (run_dir / "results.jsonl").read_text().splitlines() if line.strip()]
    for record in records:
        task = next(t for t in task_module.TASKS if t.id == record["task"])
        workspace = run_dir / f"{record['task']}__{record['host']}__{record['arm']}"
        final = (workspace / "final.md").read_text() if (workspace / "final.md").exists() else ""
        for name in ("transcript.jsonl", "events.jsonl"):
            if (workspace / name).exists():
                record.update(trace_fields(task, tool_calls((workspace / name).read_text(), record["host"])))
        if (workspace / "repo").exists():
            record["checks"] = task.check(workspace / "repo", final)
        elif task.flatpack and task.id == "t10-flatpack-question":
            record["checks"].update({k: v for k, v in task_module.check_flatpack_question(workspace, final).items() if k != "no_edits"})
    (run_dir / "results.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records))
    print(f"rechecked {len(records)} runs in {run_dir}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--hosts", nargs="+", default=["claude", "codex"], choices=["claude", "codex"])
    parser.add_argument("--arms", nargs="+", default=["baseline", "candidate"])
    parser.add_argument("--tasks", nargs="*", help="task ids; default: all")
    parser.add_argument("--baseline", type=Path, help="directory with <host>_global.md and skills/ (required for runs)")
    parser.add_argument("--out", type=Path, default=Path("/tmp/host-policy-eval") / dt.datetime.now().strftime("%Y%m%d-%H%M%S"))
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--claude-model", help="required with the claude host; Fable needs the user's grant (grants.py)")
    parser.add_argument("--claude-effort", default="high")
    parser.add_argument("--codex-model", help="required with the codex host; Astra needs the user's grant (grants.py)")
    parser.add_argument("--codex-effort", default="high")
    parser.add_argument("--codex-config", default="",
                        help="TOML lines added to both arms' Codex config, such as the sandbox settings glm-delegate needs")
    parser.add_argument("--candidate-codex-config", default="",
                        help="TOML lines added to the candidate arm's Codex config, to compare one setting")
    parser.add_argument("--candidate-skill", action="append", default=[], metavar="NAME=DIR",
                        help="add or replace a skill in the candidate arm, such as one kept in another repository")
    parser.add_argument("--recheck", type=Path, help="recompute checks for a finished run directory and exit")
    args = parser.parse_args()
    for item in args.candidate_skill:
        name, _, directory = item.partition("=")
        if not (Path(directory) / "SKILL.md").is_file():
            parser.error(f"--candidate-skill {item}: no SKILL.md in {directory}")
        CANDIDATE_SKILLS[name] = Path(directory).resolve()
    if args.recheck:
        return recheck(args.recheck)
    if args.baseline is None:
        parser.error("--baseline is required for runs")
    chosen = {host: getattr(args, f"{host}_model") for host in args.hosts}
    for host, model in chosen.items():
        if not model:
            parser.error(f"--{host}-model is required: name the model for every host that runs")
    for lines in (args.codex_config, args.candidate_codex_config):
        if grants.CODEX_MODEL_SETTING.search(lines):
            parser.error("choose the Codex model and effort with --codex-model and --codex-effort, not through config lines")
    try:
        families = {host: grants.family(model) for host, model in chosen.items()}
    except ValueError as error:
        parser.error(str(error))
    selected = [task for task in task_module.TASKS if not args.tasks or task.id in args.tasks]
    jobs = [(task, host, arm) for task in selected for host in args.hosts for arm in args.arms]
    counts: dict[str, int] = {}
    for _, host, _ in jobs:
        if families[host]:
            counts[families[host]] = counts.get(families[host], 0) + 1
    try:
        grants.reserve(counts, f"run.py ({len(jobs)} runs)")
    except PermissionError as error:
        print(error, file=sys.stderr)
        return 2
    models = {"claude": args.claude_model, "claude_effort": args.claude_effort,
              "codex": args.codex_model, "codex_effort": args.codex_effort,
              "codex_config": args.codex_config, "candidate_codex_config": args.candidate_codex_config,
              "blocked": {host: [name for name in grants.FAMILIES if name != families.get(host)] for host in ("claude", "codex")}}
    args.out.mkdir(parents=True, exist_ok=True)
    print(f"{len(jobs)} runs -> {args.out}", flush=True)
    with futures.ThreadPoolExecutor(max_workers=args.jobs) as pool, (args.out / "results.jsonl").open("a") as sink:
        pending = {pool.submit(run_one, task, host, arm, args.out, args.baseline, models, args.timeout): (task.id, host, arm)
                   for task, host, arm in jobs}
        for done in futures.as_completed(pending):
            record = done.result()
            sink.write(json.dumps(record) + "\n")
            sink.flush()
            print(f"{record['task']:24} {record['host']:6} {record['arm']:9} exit={record.get('exit')} "
                  f"{record.get('seconds')}s checks={record.get('checks')}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
