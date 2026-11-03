#!/usr/bin/env python3
"""Check HTTP status of every URL in the registry and write a Markdown report.

Usage:
  python tools/check_links.py [--report reports/link-report.md] [--timeout 20]

Does NOT edit YAML files: the report lists suggested status changes
(collected -> link-ok / broken) for a human or agent to apply.
"""
import argparse
import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

from common import ROOT, iter_catalog_urls, iter_sources

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; arab-labour-stats-wiki link checker)"}


def check(url, timeout):
    try:
        r = requests.head(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if r.status_code in (403, 405, 501) or r.status_code >= 400:
            r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True, stream=True)
        return r.status_code, r.url
    except requests.RequestException as e:
        return None, type(e).__name__


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", default="reports/link-report.md")
    ap.add_argument("--timeout", type=int, default=20)
    args = ap.parse_args()

    items = []
    for path, rec in iter_sources():
        url = rec.get("url")
        if url and url.startswith("http"):
            items.append((rec["id"], rec.get("status"), url))
    for path, label, url in iter_catalog_urls():
        if url and str(url).startswith("http"):
            items.append((f"catalog:{label}", "-", url))

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda it: (*it, *check(it[2], args.timeout)), items))

    ok = [r for r in results if r[3] and r[3] < 400]
    bad = [r for r in results if not r[3] or r[3] >= 400]
    out = Path(ROOT / args.report)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# Link report — {dt.date.today()}", "",
             f"Checked {len(results)} URLs: {len(ok)} OK, {len(bad)} failing.", "",
             "## Failing (suggest status: broken, or fix URL)", "",
             "| id | current status | code/error | url |", "|---|---|---|---|"]
    lines += [f"| {i} | {s} | {c or e} | {u} |" for i, s, u, c, e in bad]
    lines += ["", "## OK (suggest status: link-ok if currently collected)", "",
              "| id | current status | code | final url |", "|---|---|---|---|"]
    lines += [f"| {i} | {s} | {c} | {e} |" for i, s, u, c, e in ok]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{len(ok)} OK, {len(bad)} failing. Report: {out}")


if __name__ == "__main__":
    main()
