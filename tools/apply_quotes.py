#!/usr/bin/env python3
"""Write quotes pasted on the Verification Desk into the shared store content/quotes.yml.

Usage:
  python tools/apply_quotes.py <export_dir/quotes | quotes.json> [--status pasted|verified] [--by YH] [--dry-run]

Input: the folder written by ArtifactData `list` (collection `quotes`, with out_dir), or a
JSON list of {slot, text, date, [source], [lang], [quoted_from_url], [document_note]}.
Clean pasted link/header lines into those fields first; never edit the verbatim body.

For each slot still `to-paste`, the verbatim text is stored and the slot moves to --status:
  pasted    default: text recorded, awaiting a human check
  verified  when the lead pasted the text themselves (their paste is the human check)
Slots already pasted/verified are left alone and reported.
"""
import argparse
import json
from pathlib import Path

from common import load_quotes, save_quotes


def load_rows(src):
    src = Path(src)
    if src.is_dir():
        return [json.loads(f.read_text(encoding="utf-8")) for f in sorted(src.glob("*.json"))]
    return json.loads(src.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("quotes")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", default="pasted", choices=["pasted", "verified"])
    ap.add_argument("--by", default="YH")
    args = ap.parse_args()

    rows = {r["slot"]: r for r in load_rows(args.quotes) if r.get("slot") and (r.get("text") or "").strip()}
    quotes = load_quotes()
    applied, skipped = [], []
    for q in quotes:
        row = rows.get(q["slot"])
        if not row:
            continue
        if q.get("status") != "to-paste":
            skipped.append(q["slot"])
            continue
        q["text"] = row["text"].strip().replace("\r\n", "\n")
        q["status"] = args.status
        for k in ("source", "lang", "quoted_from_url", "document_note"):
            if row.get(k):
                q[k] = row[k]
        q["pasted_on"] = row.get("date", "")
        if args.status == "verified":
            q["verified_by"] = args.by
        applied.append(q["slot"])
    if not args.dry_run:
        save_quotes(quotes)
    print(f"applied: {len(applied)} {applied}")
    if skipped:
        print(f"already filled (not changed): {skipped}")
    missing = sorted(set(rows) - set(applied) - set(skipped))
    if missing:
        print(f"unknown slots: {missing}")


if __name__ == "__main__":
    main()
