#!/usr/bin/env python3
"""Summarize host-policy runs: check pass rates, judge scores and resource use per host and arm."""
from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

BAD_WHEN_TRUE = {"ended_with_question", "unqualified_b_wins", "w900_called_failure"}
# build_removed was informational in the first summaries; it is scored because cleaning up is what t04 asks for.
INFORMATIONAL = {"changed", "found", "added_tests"}


def load(run_dirs: list[Path]) -> tuple[list[dict], dict]:
    records, judgments = [], {}
    for run_dir in run_dirs:
        for line in (run_dir / "results.jsonl").read_text().splitlines():
            if line.strip():
                record = json.loads(line)
                if record.get("exit") == "rate-limited":
                    continue
                record["rep"] = run_dir.name
                records.append(record)
        path = run_dir / "judgments.jsonl"
        if path.exists():
            for line in path.read_text().splitlines():
                if line.strip():
                    item = json.loads(line)
                    judgments[(run_dir.name, item["task"], item["host"], item["arm"])] = item
    return records, judgments


def passed(record: dict) -> tuple[int, int, list[str]]:
    good = total = 0
    failures = []
    for name, value in record.get("checks", {}).items():
        if name in INFORMATIONAL or not isinstance(value, bool):
            continue
        ok = (not value) if name in BAD_WHEN_TRUE else value
        good += ok
        total += 1
        if not ok:
            failures.append(name)
    if record.get("exit") not in (0, None):
        failures.append(f"exit={record.get('exit')}")
        total += 1  # a run that failed outright counts as one failed check, so it cannot vanish from the rate
    return good, total, failures


def main(argv: list[str]) -> int:
    records, judgments = load([Path(arg) for arg in argv])
    groups = defaultdict(list)
    for record in records:
        groups[(record["host"], record["arm"])].append(record)
    print("| Host | Arm | Runs | Checks passed | Task score | Report score | Input tokens (median) | Output tokens (median) | Turns (median) | Seconds (median) | Cost USD (sum, Claude) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for (host, arm), items in sorted(groups.items()):
        good = sum(passed(r)[0] for r in items)
        total = sum(passed(r)[1] for r in items)
        scores = [judgments.get((r["rep"], r["task"], host, arm), {}) for r in items]
        task_scores = [s["task_score"] for s in scores if isinstance(s.get("task_score"), (int, float))]
        report_scores = [s["report_score"] for s in scores if isinstance(s.get("report_score"), (int, float))]
        def median(key):
            values = [r[key] for r in items if isinstance(r.get(key), (int, float))]
            return f"{statistics.median(values):,.0f}" if values else "n/a"
        cost = sum(r.get("cost_usd") or 0 for r in items)
        print(f"| {host} | {arm} | {len(items)} | {good}/{total} | "
              f"{statistics.mean(task_scores):.2f} (n={len(task_scores)}) | " if task_scores else f"| {host} | {arm} | {len(items)} | {good}/{total} | n/a | ", end="")
        print(f"{statistics.mean(report_scores):.2f} | " if report_scores else "n/a | ", end="")
        print(f"{median('input_tokens')} | {median('output_tokens')} | {median('turns')} | {median('seconds')} | "
              f"{cost:.2f} |" if host == "claude" else f"{median('input_tokens')} | {median('output_tokens')} | {median('turns')} | {median('seconds')} | n/a |")
    print("\nFailed checks and judge scores by task:\n")
    print("| Task | Host | Arm | Rep | Failed checks | Task | Report | Tokens in/out | Seconds |")
    print("|---|---|---|---|---|---|---|---|---|")
    for record in sorted(records, key=lambda r: (r["task"], r["host"], r["arm"], r["rep"])):
        score = judgments.get((record["rep"], record["task"], record["host"], record["arm"]), {})
        print(f"| {record['task']} | {record['host']} | {record['arm']} | {record['rep']} | "
              f"{', '.join(passed(record)[2]) or '-'} | {score.get('task_score', '')} | {score.get('report_score', '')} | "
              f"{record.get('input_tokens', '')}/{record.get('output_tokens', '')} | {record.get('seconds', '')} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
