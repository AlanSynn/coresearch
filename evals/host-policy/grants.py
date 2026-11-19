#!/usr/bin/env python3
"""Top-tier models in the evaluation: only the user can allow them, a limited number of times.

Fable and Astra cost the most and their usage limits are tight, so an evaluation that would run an agent or a judge on
either refuses unless the user has granted that family a number of runs. Only the user grants: the grant command reads
its confirmation from the controlling terminal, so an agent's shell cannot answer it. An agent that needs a grant asks
the user to run the command; it never creates, edits or works around a grant.

    python3 evals/host-policy/grants.py grant fable --runs 40 [--hours 12]   # in the user's own terminal
    python3 evals/host-policy/grants.py list
    python3 evals/host-policy/grants.py revoke fable

The same file is the hook that stops a subagent inside a run from switching to a family the run has no grant for:
`grants.py guard --block fable astra` reads a PreToolUse event (Claude Code or Codex) and denies a subagent whose
requested model names a blocked family.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import json
import os
import re
import shlex
import sys
import tempfile
from pathlib import Path

FAMILIES = ("fable", "astra")
# Aliases that resolve to an account or profile default could select a top-tier model without naming it.
INDIRECT = {"", "default", "best"}
GRANTS = ".config/coresearch/eval-grants.json"
SELF = Path(__file__).resolve()
GUARD_LOG = "subagent-models.jsonl"
# Codex config lines that would choose a model or effort behind --codex-model and --codex-effort.
CODEX_MODEL_SETTING = re.compile(r"^\s*(?:model|profile|review_model|model_provider|model_reasoning_effort)\s*="
                                 r"|^\s*\[\s*(?:profiles|agents|model_providers)\b", re.M)
# Environment variables through which Claude Code would pick a model other than the one named on its command line.
CLAUDE_MODEL_ENV = re.compile(r"^(?:ANTHROPIC|CLAUDE_CODE)_\w*MODEL\w*$")


def family(model: str) -> str | None:
    """The top-tier family a model id belongs to, or None; a model named only indirectly is refused."""
    name = model.strip().lower()
    if name in INDIRECT:
        raise ValueError(f"name the model explicitly instead of {model!r}: an alias for the default could pick a top-tier model")
    return next((item for item in FAMILIES if item in name), None)


def grants_path(home: Path | None = None) -> Path:
    return (home or Path.home()) / GRANTS


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def _save(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, prefix=path.name + ".")
    with os.fdopen(handle, "w") as stream:
        json.dump(data, stream, indent=2)
        stream.write("\n")
    os.replace(temporary, path)


class _Lock:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.stream = path.with_name(path.name + ".lock").open("a")

    def __enter__(self):
        fcntl.flock(self.stream, fcntl.LOCK_EX)
        return self

    def __exit__(self, *_):
        fcntl.flock(self.stream, fcntl.LOCK_UN)
        self.stream.close()


def _usable(entry: dict | None, now: dt.datetime) -> int:
    if not entry or dt.datetime.fromisoformat(entry["expires"]) <= now:
        return 0
    return int(entry["runs"])


def reserve(counts: dict[str, int], purpose: str, home: Path | None = None, now: dt.datetime | None = None) -> None:
    """Take counts[family] runs from the user's grants before anything starts, or raise PermissionError and take none."""
    counts = {name: number for name, number in counts.items() if number > 0}
    if not counts:
        return
    path, now = grants_path(home), now or _now()
    with _Lock(path):
        data = _load(path)
        short = {name: number for name, number in counts.items() if _usable(data.get(name), now) < number}
        if short:
            lines = [f"{purpose} needs top-tier models the user has not allowed:"]
            for name, number in short.items():
                lines.append(f"  {name}: {number} runs needed, {_usable(data.get(name), now)} granted")
            lines.append("Choose another model, or ask the user to run, in their own terminal:")
            lines += [f"  python3 {SELF} grant {name} --runs {number}" for name, number in short.items()]
            lines.append("An agent never creates, edits or works around a grant.")
            raise PermissionError("\n".join(lines))
        for name, number in counts.items():
            data[name]["runs"] -= number
            data[name].setdefault("used", []).append({"at": now.isoformat(timespec="seconds"), "runs": number, "for": purpose})
        _save(path, data)


def _confirm(prompt: str, answer: str) -> bool:
    """True when the person at the controlling terminal types the answer; False when there is no terminal."""
    try:
        terminal = open("/dev/tty", "r+")
    except OSError:
        return False
    with terminal:
        terminal.write(prompt)
        terminal.flush()
        return terminal.readline().strip() == answer


def grant(name: str, runs: int, hours: float, home: Path | None = None, now: dt.datetime | None = None) -> dict:
    path, now = grants_path(home), now or _now()
    entry = {"runs": runs, "granted": now.isoformat(timespec="seconds"),
             "expires": (now + dt.timedelta(hours=hours)).isoformat(timespec="seconds")}
    with _Lock(path):
        data = _load(path)
        data[name] = entry
        _save(path, data)
    return entry


def model_free_env() -> dict[str, str]:
    """This process's environment without the variables that would choose Claude Code's models behind the harness."""
    return {key: value for key, value in os.environ.items() if not CLAUDE_MODEL_ENV.match(key)}


def guard_command(blocked: list[str], workspace: Path) -> str:
    """The hook command that denies subagents on the blocked families and logs model requests in the workspace."""
    return " ".join(shlex.quote(part) for part in
                    [sys.executable, str(SELF), "guard", "--log", str(workspace / GUARD_LOG), "--block", *blocked])


def write_codex_hooks(home: Path, blocked: list[str], workspace: Path) -> None:
    """Install the guard in a temporary CODEX_HOME; it sees every tool call, since Codex names the subagent tool
    collaborationspawn_agent or spawn_agent depending on the version."""
    hooks = {"hooks": {"PreToolUse": [{"hooks": [{"type": "command", "command": guard_command(blocked, workspace)}]}]}}
    (home / "hooks.json").write_text(json.dumps(hooks, indent=2) + "\n")


def guard_log(workspace: Path) -> list[dict]:
    """The subagent model requests the guard saw in a run, each with whether it was denied."""
    path = workspace / GUARD_LOG
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def guard(blocked: list[str], event: dict) -> dict | None:
    """The PreToolUse decision for a subagent request that names a blocked family; None lets the call through."""
    tool_input = event.get("tool_input") or {}
    requested = str(tool_input.get("model") or "")
    hit = next((name for name in blocked if name in requested.lower()), None)
    if not hit:
        return None
    return {"hookSpecificOutput": {
        "hookEventName": "PreToolUse", "permissionDecision": "deny",
        "permissionDecisionReason": f"{requested} is a top-tier model ({hit}) that this evaluation run has no grant "
                                    "for; leave the model unset so the subagent inherits the run's model."}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    give = commands.add_parser("grant", help="allow a top-tier family for a number of runs (the user, at a terminal)")
    give.add_argument("family", choices=FAMILIES)
    give.add_argument("--runs", type=int, required=True, help="agent runs and judgments together")
    give.add_argument("--hours", type=float, default=12.0, help="the grant lapses after this many hours")
    commands.add_parser("list", help="show the grants")
    take = commands.add_parser("revoke", help="remove a family's grant")
    take.add_argument("family", choices=FAMILIES)
    hook = commands.add_parser("guard", help="PreToolUse hook: deny subagents on blocked families")
    hook.add_argument("--block", nargs="*", default=[])
    hook.add_argument("--log", type=Path, help="append each tool call that requests a model to this file")
    args = parser.parse_args()

    if args.command == "grant":
        if args.runs < 1 or args.hours <= 0:
            parser.error("--runs and --hours must be positive")
        until = (_now() + dt.timedelta(hours=args.hours)).astimezone()
        prompt = (f"Allow {args.runs} evaluation runs or judgments on {args.family} until {until:%Y-%m-%d %H:%M %Z}?\n"
                  f"Type {args.family} to confirm: ")
        if not _confirm(prompt, args.family):
            print("not granted: the grant needs the user's confirmation at a terminal", file=sys.stderr)
            return 1
        entry = grant(args.family, args.runs, args.hours)
        print(f"granted {args.family}: {entry['runs']} runs until {entry['expires']}")
        return 0
    if args.command == "list":
        data, now = _load(grants_path()), _now()
        for name in FAMILIES:
            entry = data.get(name)
            state = f"{_usable(entry, now)} runs left until {entry['expires']}" if _usable(entry, now) else "not granted"
            print(f"{name}: {state}")
        return 0
    if args.command == "revoke":
        with _Lock(grants_path()):
            data = _load(grants_path())
            data.pop(args.family, None)
            _save(grants_path(), data)
        print(f"revoked {args.family}")
        return 0
    event = json.loads(sys.stdin.read() or "{}")
    decision = guard(args.block, event)
    if args.log and "model" in (event.get("tool_input") or {}):
        with args.log.open("a") as stream:
            stream.write(json.dumps({"tool": event.get("tool_name"), "model": (event.get("tool_input") or {}).get("model"),
                                     "denied": bool(decision)}) + "\n")
    if decision:
        print(json.dumps(decision))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
