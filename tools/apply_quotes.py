#!/usr/bin/env python3
"""Write quotes pasted on the Verification Desk into the indicator files.

Usage:
  python tools/apply_quotes.py <export_dir/quotes | quotes.json> [--dry-run]

Input: the folder written by ArtifactData `list` (collection `quotes`, with out_dir),
or a JSON list of {slot, text, date, [source], [lang], [quoted_from_url], [document_note]}
(clean pasted link/header lines into those fields first; never edit the verbatim body). For each slot still `to-paste`, the
verbatim text is stored and the slot moves to `status: pasted`. A later human
check (or the lead's own paste, which is already a human act) can promote it to
`verified`. Slots already pasted/verified are left alone and reported.
Edits are line-based on the slot's flow mapping, so comments and layout survive.
"""
import argparse
import json
import re
from pathlib import Path

from common import indicator_files


def load_rows(src):
    src = Path(src)
    if src.is_dir():
        return [json.loads(f.read_text(encoding="utf-8")) for f in sorted(src.glob("*.json"))]
    return json.loads(src.read_text(encoding="utf-8"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("quotes")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", default="pasted", choices=["pasted", "verified"],
                    help="verified when the lead pasted the text themselves (their paste is the human check)")
    ap.add_argument("--by", default="YH")
    args = ap.parse_args()

    rows = {r["slot"]: r for r in load_rows(args.quotes) if r.get("slot") and (r.get("text") or "").strip()}
    applied, skipped = [], []
    for path in indicator_files():
        text = path.read_text(encoding="utf-8")
        for slot, row in rows.items():
            m = re.search(r"(\n\s*- \{slot: " + re.escape(slot) + r",.*?\})", text, flags=re.S)
            if not m:
                continue
            block = m.group(1)
            if "status: to-paste" not in block:
                skipped.append(slot)
                continue
            verbatim = row["text"].strip().replace("\r\n", "\n")
            new = block.replace("status: to-paste", f"status: {args.status}", 1)
            new = new.replace('text: ""', "text: " + json.dumps(verbatim, ensure_ascii=False), 1)
            if row.get("source"):
                new = re.sub(r"source: [a-z0-9-]+", "source: " + row["source"], new, count=1)
            if row.get("lang"):
                new = re.sub(r"lang: [a-z]{2}", "lang: " + row["lang"], new, count=1)
            extra = f", pasted_on: {row.get('date', '')}"
            if args.status == "verified":
                extra += f", verified_by: {args.by}"
            for k in ("quoted_from_url", "document_note"):
                if row.get(k):
                    extra += f", {k}: " + json.dumps(row[k], ensure_ascii=False)
            new = new.rstrip("}") + extra + "}"
            text = text.replace(block, new, 1)
            applied.append(slot)
        if not args.dry_run:
            path.write_text(text, encoding="utf-8")
    print(f"applied: {len(applied)} {applied}")
    if skipped:
        print(f"already filled (not changed): {skipped}")
    missing = sorted(set(rows) - set(applied) - set(skipped))
    if missing:
        print(f"unknown slots: {missing}")


if __name__ == "__main__":
    main()
