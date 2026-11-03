#!/usr/bin/env python3
"""Validate source records against sources/schema.yaml.

Usage:
  python tools/validate.py          # validate, exit 1 on errors
  python tools/validate.py --stats  # also print counts by file/status/priority
"""
import datetime as dt
import re
import sys
from collections import Counter

from common import SOURCES_DIR, iter_sources, load_yaml, source_files


def check_type(value, spec):
    t = spec.get("type")
    if t == "str":
        return isinstance(value, str)
    if t == "list":
        return isinstance(value, list)
    if t == "datelike":
        return isinstance(value, (dt.date, int)) or (isinstance(value, str) and bool(re.fullmatch(r"\d{4}(-\d{2}){0,2}", value)))
    if t == "date":
        if isinstance(value, dt.date):
            return True
        return isinstance(value, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))
    return True


def main():
    schema = load_yaml(SOURCES_DIR / "schema.yaml")
    fields, required = schema["fields"], schema["required"]
    errors, seen = [], {}

    for path in source_files():
        data = load_yaml(path)
        if "file_meta" not in data:
            errors.append(f"{path.name}: missing file_meta")

    for path, rec in iter_sources():
        rid = rec.get("id", "<no id>")
        where = f"{path.relative_to(SOURCES_DIR)}::{rid}"
        for key in required:
            if key not in rec or rec[key] in (None, ""):
                errors.append(f"{where}: missing required field '{key}'")
        for key, value in rec.items():
            spec = fields.get(key)
            if spec is None:
                errors.append(f"{where}: unknown field '{key}'")
                continue
            if value is None:
                continue
            if not check_type(value, spec):
                errors.append(f"{where}: field '{key}' should be {spec['type']}")
            if "enum" in spec and isinstance(value, str) and value not in spec["enum"]:
                errors.append(f"{where}: '{key}'='{value}' not in {spec['enum']}")
            if "pattern" in spec and isinstance(value, str) and not re.search(spec["pattern"], value):
                errors.append(f"{where}: '{key}' does not match {spec['pattern']}")
        if rid in seen:
            errors.append(f"{where}: duplicate id (also in {seen[rid]})")
        seen[rid] = path.name
        if rec.get("status") == "verified" and not (rec.get("verified_by") and rec.get("verified_date")):
            errors.append(f"{where}: status verified requires verified_by and verified_date")
        if rec.get("url") == "TO-LOCATE" and rec.get("status") != "to-locate":
            errors.append(f"{where}: url TO-LOCATE requires status to-locate")
        sup = rec.get("superseded_by")
        if sup and sup not in [r.get("id") for _, r in iter_sources()]:
            errors.append(f"{where}: superseded_by '{sup}' not found")

    if "--stats" in sys.argv:
        recs = [r for _, r in iter_sources()]
        by_file = Counter(p.relative_to(SOURCES_DIR).as_posix() for p, _ in iter_sources())
        print(f"Total source records: {len(recs)}")
        print("By status:  ", dict(Counter(r.get("status") for r in recs)))
        print("By priority:", dict(Counter(r.get("priority") for r in recs)))
        print("By type:    ", dict(Counter(r.get("type") for r in recs)))
        print("By file:")
        for f, n in sorted(by_file.items()):
            print(f"  {f}: {n}")

    if errors:
        print(f"\n{len(errors)} error(s):")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("OK: all source records valid.")


if __name__ == "__main__":
    main()
