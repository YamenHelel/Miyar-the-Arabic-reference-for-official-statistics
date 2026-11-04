#!/usr/bin/env python3
"""Apply a link report (from check_links.py) to the source YAML files.

Usage:
  python tools/apply_link_report.py reports/link-report.md [--date 2026-11-04] [--dry-run]

Rules (never touches records with status verified / superseded / to-locate):
  - HTTP < 400                              -> status: link-ok
  - HTTP 404 / 410, ConnectionError         -> status: broken
  - 403 / 401 / 429 / 5xx / SSL / timeouts  -> status unchanged (site blocks bots or is flaky;
                                               check by hand in a browser)
In every case a `link_check: "<date> <code>"` line is written or updated in the record.
Edits are line-based so comments and formatting are preserved.
"""
import argparse
import datetime as dt
import re
from pathlib import Path

from common import source_files

ROW = re.compile(r"^\| (src-[a-z0-9-]+) \| [^|]* \| ([^|]+) \|")
PROTECTED = {"verified", "superseded", "to-locate"}


def decide(code):
    code = code.strip()
    if code.isdigit():
        n = int(code)
        if n < 400:
            return "link-ok"
        if n in (404, 410):
            return "broken"
        return None
    if code in ("ConnectionError",):
        return "broken"
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--date", default=str(dt.date.today()))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    results = {}
    for line in Path(args.report).read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            results[m.group(1)] = m.group(2).strip()

    counts = {"link-ok": 0, "broken": 0, "unchanged": 0}
    for path in source_files():
        lines = path.read_text(encoding="utf-8").splitlines()
        out, cur, changed = [], None, False
        for line in lines:
            mid = re.match(r"^\s*- id: (src-[a-z0-9-]+)\s*$", line)
            if mid:
                cur = mid.group(1)
            if re.match(r"^\s+link_check:", line) and cur in results:
                continue  # drop old value; rewritten after status
            ms = re.match(r"^(\s+)status: (\S+)\s*$", line)
            if ms and cur in results:
                indent, status = ms.groups()
                code = results[cur]
                new = decide(code)
                if status not in PROTECTED and new and new != status:
                    line = f"{indent}status: {new}"
                    counts[new] += 1
                else:
                    counts["unchanged"] += 1
                out.append(line)
                out.append(f'{indent}link_check: "{args.date} {code}"')
                changed = True
                continue
            out.append(line)
        if changed and not args.dry_run:
            path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(counts)


if __name__ == "__main__":
    main()
