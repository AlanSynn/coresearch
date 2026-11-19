#!/usr/bin/env python3
"""Score finished runs with a rubric judge from the other model family, blind to the instruction arm.

Claude runs are judged by Codex and Codex runs by Claude Code, each in a clean environment without the user's
instructions. The judge sees the task prompt, the rubric, the final answer, the deterministic check results and the
repository change summary; it never sees which arm produced the run.
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tasks as task_module  # noqa: E402

ARM_PATH = re.compile(r"[^\s(\[`'\"<>]*__(?:baseline|candidate)")
REPORT_RUBRIC = ("Report quality: the outcome comes first; plain full sentences a reader who saw none of the work can "
                 "follow; no unexplained shorthand; says what was and was not verified; no claim the evidence in the "
                 "answer does not support.")

PROMPT = """You are grading one answer that a coding agent gave to a task. Grade only what is shown.

Task given to the agent:
<task>{prompt}</task>

Automatic checks on the agent's final repository state (true is good unless the name says otherwise):
<checks>{checks}</checks>

Summary of the files the agent changed:
<changes>{changes}</changes>
{diff}
The agent's final message:
<answer>{answer}</answer>

Score each criterion from 1 (poor) to 5 (excellent):
- task: {rubric}
- report: {report}

Return only a JSON object: {{"task_score": <1-5>, "report_score": <1-5>, "reason": "<two sentences>"}}"""


def changes(repo: Path) -> str:
    if not (repo / ".git").exists():
        return "(read-only task; no changes recorded)"
    status = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=repo, capture_output=True, text=True).stdout
    diff = subprocess.run(["git", "diff", "--stat"], cwd=repo, capture_output=True, text=True).stdout
    lines = [line for line in status.splitlines() if "__pycache__" not in line and ".claude/skills" not in line]
    return ("\n".join(lines[:40]) + "\n" + diff[-1500:]).strip() or "(no changes)"


def code_change(repo: Path, limit: int = 20000) -> str:
    """The change itself against the fixture commit: the diff of tracked files and the text of new files, without the
    evaluation's skill copies, caches and binary files, cut at limit characters."""
    root = subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.split()
    if not root:
        return "(no repository)"
    parts = [subprocess.run(["git", "diff", root[0], "--", ".", ":(exclude).claude"], cwd=repo, capture_output=True,
                            text=True).stdout]
    new = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], cwd=repo, capture_output=True, text=True).stdout
    for name in new.splitlines():
        if name.startswith(".claude/") or "__pycache__" in name or name.endswith((".pyc", ".db", ".sqlite")):
            continue
        try:
            parts.append(f"--- new file: {name}\n{(repo / name).read_text(encoding='utf-8')}")
        except (OSError, UnicodeDecodeError):
            continue
    text = "\n".join(part for part in parts if part).strip() or "(no changes)"
    return text if len(text) <= limit else text[:limit] + f"\n[cut: {len(text) - limit} more characters]"


def judge_with_claude(prompt: str) -> str:
    with tempfile.TemporaryDirectory() as empty:
        result = subprocess.run(["claude", "-p", "--model", "opus", "--effort", "medium", "--setting-sources", "project,local",
                                 "--output-format", "json", "--no-session-persistence", "--tools", "", "--", prompt],
                                cwd=empty, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600)
    return json.loads(result.stdout).get("result", "") if result.stdout.strip().startswith("{") else result.stdout


def judge_with_codex(prompt: str) -> str:
    with tempfile.TemporaryDirectory() as home, tempfile.TemporaryDirectory() as empty:
        os.chmod(home, 0o700)
        shutil.copy2(Path.home() / ".codex/auth.json", Path(home) / "auth.json")
        Path(home, "config.toml").write_text('model = "gpt-6.2-astra"\nmodel_reasoning_effort = "medium"\n')
        out = Path(empty) / "final.txt"
        try:
            # An open stdin makes codex exec wait for more input, so close it.
            subprocess.run(["codex", "exec", "--sandbox", "read-only", "--skip-git-repo-check", "-o", str(out), prompt],
                           cwd=empty, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=600,
                           env={**os.environ, "CODEX_HOME": home})
        finally:
            Path(home, "auth.json").unlink(missing_ok=True)
        return out.read_text() if out.exists() else ""


def judge(run_dir: Path, record: dict) -> dict:
    task = next(t for t in task_module.TASKS if t.id == record["task"])
    workspace = run_dir / f"{record['task']}__{record['host']}__{record['arm']}"
    answer = (workspace / "final.md").read_text() if (workspace / "final.md").exists() else ""
    # Answers that cite absolute paths would name the workspace, and with it the arm; the judge must stay blind.
    answer = ARM_PATH.sub("<workspace>", answer)
    diff = ""
    if task.show_diff:
        diff = ("\nThe code change against the starting repository:\n<diff>"
                + ARM_PATH.sub("<workspace>", code_change(workspace / "repo")) + "</diff>\n")
    prompt = PROMPT.format(prompt=task.prompt, checks=json.dumps(record.get("checks", {})),
                           changes=changes(workspace / "repo"), diff=diff, answer=answer[:12000],
                           rubric=task.rubric or "The task was carried out correctly and completely, within the scope the request implies.",
                           report=REPORT_RUBRIC)
    try:
        raw = judge_with_codex(prompt) if record["host"] == "claude" else judge_with_claude(prompt)
    except subprocess.TimeoutExpired:
        raw = "judge timed out"  # left unscored, so judge.py --missing retries it
    match = re.search(r"\{.*\}", raw, re.S)
    try:
        scores = json.loads(match.group(0)) if match else {}
    except json.JSONDecodeError:
        scores = {}
    return {"task": record["task"], "host": record["host"], "arm": record["arm"],
            "judge": "codex" if record["host"] == "claude" else "claude", **scores, "raw": raw[-600:]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--tasks", nargs="*", help="judge only these task ids (routing tests need no judge)")
    parser.add_argument("--missing", action="store_true",
                        help="keep existing scored judgments and judge only runs without one (after a judge failure)")
    args = parser.parse_args()
    records = [json.loads(line) for line in (args.run_dir / "results.jsonl").read_text().splitlines() if line.strip()]
    records = [r for r in records if r.get("exit") == 0 and not r.get("is_error")]
    if args.tasks:
        records = [r for r in records if r["task"] in args.tasks]
    out = args.run_dir / "judgments.jsonl"
    existing = [json.loads(line) for line in out.read_text().splitlines() if line.strip()] if out.exists() else []
    # Judgments of tasks outside --tasks stay as they are.
    kept = [item for item in existing if args.tasks and item["task"] not in args.tasks]
    if args.missing:
        scored = [item for item in existing if isinstance(item.get("task_score"), (int, float)) and item not in kept]
        kept += scored
        done = {(item["task"], item["host"], item["arm"]) for item in scored}
        records = [r for r in records if (r["task"], r["host"], r["arm"]) not in done]
    # Write beside the file and swap it in at the end, so an interrupted run leaves the earlier judgments intact.
    partial = out.with_name(out.name + ".partial")
    with futures.ThreadPoolExecutor(max_workers=args.jobs) as pool, partial.open("w") as sink:
        sink.writelines(json.dumps(item) + "\n" for item in kept)
        sink.flush()
        for result in pool.map(lambda record: judge(args.run_dir, record), records):
            sink.write(json.dumps(result) + "\n")
            sink.flush()
            print(f"{result['task']:24} {result['host']:6} {result['arm']:9} task={result.get('task_score')} report={result.get('report_score')}", flush=True)
    partial.replace(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
