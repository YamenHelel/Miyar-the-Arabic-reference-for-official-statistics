#!/usr/bin/env python3
"""Apply the lead's verdicts from the Verification Desk to the source YAML files.

Usage:
  python tools/apply_verification.py <verdicts.json | export_dir/verdicts> [--by YH] [--dry-run]

Input: a JSON list of {id, verdict, note, date}, or the folder written by
ArtifactData `list` with `out_dir` (one JSON file per verdict). Rules:
  ok      -> status: verified, verified_by, verified_date (+ review_note if a note was given)
  broken  -> status: broken (+ review_note)
  fix     -> status unchanged, review_note added: the agent must act on it
  skip    -> ignored
Records already verified/superseded are not touched. Edits are line-based.
Prints the ids handled per verdict so the agent can clean up the artifact
(delete `fix` verdicts once fixed, so the item returns to the queue).
"""
import argparse
import json
import re
from pathlib import Path

from common import source_files


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("verdicts")
    ap.add_argument("--by", default="YH")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = Path(args.verdicts)
    if src.is_dir():
        rows = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(src.glob("*.json"))]
    else:
        rows = json.loads(src.read_text(encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("documents") or rows.get("docs") or list(rows.values())
    verdicts = {}
    for r in rows:
        body = r.get("data", r) if isinstance(r, dict) else {}
        if body.get("id") and body.get("verdict") in ("ok", "broken", "fix"):
            verdicts[body["id"]] = body

    done = {"ok": [], "broken": [], "fix": [], "protected": []}
    seen = set()
    for path in source_files():
        lines = path.read_text(encoding="utf-8").splitlines()
        out, cur, changed = [], None, False
        for line in lines:
            mid = re.match(r"^\s*- id: (src-[a-z0-9-]+)\s*$", line)
            if mid:
                cur = mid.group(1)
            v = verdicts.get(cur)
            if v and re.match(r"^\s+(verified_by|verified_date|review_note):", line):
                continue  # rewritten below
            ms = re.match(r"^(\s+)status: (\S+)\s*$", line)
            if ms and v:
                indent, status = ms.groups()
                seen.add(cur)
                if status in ("verified", "superseded") and v["verdict"] != "fix":
                    done["protected"].append(cur)
                    out.append(line)
                    continue
                kind = v["verdict"]
                if kind == "ok":
                    out.append(f"{indent}status: verified")
                    out.append(f"{indent}verified_by: {args.by}")
                    out.append(f"{indent}verified_date: {v.get('date')}")
                elif kind == "broken":
                    out.append(f"{indent}status: broken")
                else:
                    out.append(line)
                note = (v.get("note") or "").strip()
                if note:
                    out.append(f"{indent}review_note: {q(note + ' (' + str(v.get('date')) + ')')}")
                done[kind].append(cur)
                changed = True
                continue
            out.append(line)
        if changed and not args.dry_run:
            path.write_text("\n".join(out) + "\n", encoding="utf-8")

    missing = sorted(set(verdicts) - seen)
    for k, ids in done.items():
        print(f"{k}: {len(ids)}" + (f"  {', '.join(ids)}" if ids and k != "ok" else ""))
    if missing:
        print("unknown ids (not in registry):", ", ".join(missing))


if __name__ == "__main__":
    main()
