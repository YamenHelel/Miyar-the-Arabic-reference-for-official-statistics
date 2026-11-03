#!/usr/bin/env python3
"""Submit registry URLs without an archived_url to the Internet Archive (Save Page Now).

Usage:
  python tools/archive.py [--limit 20] [--dry-run]

Prints `id -> snapshot URL` lines; paste them into the YAML `archived_url` field
(or let an agent apply them). Be polite: the script waits between requests.
"""
import argparse
import time

import requests

from common import iter_sources

SAVE = "https://web.archive.org/save/"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    todo = [r for _, r in iter_sources()
            if str(r.get("url", "")).startswith("http") and not r.get("archived_url")]
    print(f"{len(todo)} records without archived_url; processing {min(args.limit, len(todo))}.")
    for rec in todo[: args.limit]:
        if args.dry_run:
            print(f"[dry-run] {rec['id']} -> {rec['url']}")
            continue
        try:
            r = requests.get(SAVE + rec["url"], timeout=120,
                             headers={"User-Agent": "arab-labour-stats-wiki archiver"})
            loc = r.headers.get("Content-Location") or r.url
            snap = loc if loc.startswith("http") else "https://web.archive.org" + loc
            print(f"{rec['id']} -> {snap} (HTTP {r.status_code})")
        except requests.RequestException as e:
            print(f"{rec['id']} -> FAILED ({type(e).__name__})")
        time.sleep(10)


if __name__ == "__main__":
    main()
