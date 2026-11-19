#!/usr/bin/env python3
"""Save vendor prompting guides as Markdown for local reading. Python 3.10+, stdlib.

Reads docs/guides.json, writes <output>/<id>.md and <output>/receipt.json with the URL,
retrieval time, byte count and SHA-256 of each saved file. Markdown endpoints are
saved verbatim; HTML pages are reduced to their <article> or <main> element and
converted with pandoc when it is installed. The saved text is reference material
only: it is never executed and stays out of version control (.sources/ is ignored).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USER_AGENT = "coresearch-guides/1 (reference crawl)"


def fetch(url: str, timeout: float) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read(), response.headers.get("Content-Type", "")


def html_to_markdown(html: str) -> str:
    match = re.search(r"<article\b.*?</article>", html, re.S) or re.search(r"<main\b.*?</main>", html, re.S)
    body = match.group(0) if match else html
    if shutil.which("pandoc") is None:
        raise RuntimeError("HTML source needs pandoc for conversion")
    result = subprocess.run(
        ["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none"],
        input=body.encode("utf-8"), capture_output=True, check=True, timeout=60,
    )
    text = result.stdout.decode("utf-8")
    return re.sub(r"!\[[^\]]*\]\(data:[^)]*\)\s*", "", text)  # drop inline icon images


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--manifest", type=Path, default=ROOT / "docs" / "guides.json")
    parser.add_argument("--output", type=Path, default=ROOT / ".sources" / "guides" / dt.date.today().isoformat())
    parser.add_argument("--only", nargs="*", help="ids to fetch")
    parser.add_argument("--timeout", type=float, default=40)
    args = parser.parse_args(argv)
    entries = json.loads(args.manifest.read_text(encoding="utf-8"))
    if args.only:
        entries = [entry for entry in entries if entry["id"] in set(args.only)]
    args.output.mkdir(parents=True, exist_ok=True)
    receipt_path = args.output / "receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.exists() else {}
    failures = 0
    for entry in entries:
        record = {"url": entry["url"], "retrieved": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")}
        try:
            raw, content_type = fetch(entry["url"], args.timeout)
            text = raw.decode("utf-8", errors="replace")
            if "html" in content_type:
                text = html_to_markdown(text)
                record["converted_from_html"] = True
            data = text.encode("utf-8")
            (args.output / f"{entry['id']}.md").write_bytes(data)
            record.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(), status="ok")
        except Exception as error:  # record the failure and continue with the next guide
            failures += 1
            record.update(status="failed", error=f"{type(error).__name__}: {error}")
        receipt[entry["id"]] = record
        print(f"{record['status']:6} {entry['id']}", file=sys.stderr)
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"saved to {args.output} ({len(entries) - failures} ok, {failures} failed)")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
