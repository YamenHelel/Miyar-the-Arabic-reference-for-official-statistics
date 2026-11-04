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

from common import CONTENT_DIR, SOURCES_DIR, concept_files, indicator_files, iter_sources, load_quotes, load_yaml, source_files


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

    # ---- shared quotes store ----
    reg = {r.get("id"): r for _, r in iter_sources()}
    quotes = load_quotes()
    slots = {}
    for qd in quotes:
        s = qd.get("slot", "<no slot>")
        where = f"content/quotes.yml::{s}"
        if not str(s).startswith("q-"):
            errors.append(f"{where}: slot id must start with q-")
        if s in slots:
            errors.append(f"{where}: duplicate slot")
        slots[s] = qd
        src = reg.get(qd.get("source"))
        if not src:
            errors.append(f"{where}: unknown source {qd.get('source')}")
        st = qd.get("status")
        if st not in ("to-paste", "pasted", "verified", "source-missing"):
            errors.append(f"{where}: invalid status {st}")
        if (qd.get("text") or "").strip():
            if st == "to-paste":
                errors.append(f"{where}: has text but status to-paste")
            if src and src.get("status") != "verified":
                errors.append(f"{where}: text comes from a source that is not verified ({src.get('id')})")
        elif st in ("pasted", "verified"):
            errors.append(f"{where}: is {st} but has no text")
    used = set()

    def check_ref(where, ref):
        if ref:
            used.add(ref)
            if ref not in slots:
                errors.append(f"{where}: reference to undefined quote slot {ref}")

    def check_src(where, sid):
        if sid and sid not in reg:
            errors.append(f"{where}: unknown source {sid}")

    ind_ids = {p.stem for p in indicator_files()}
    con_ids = {p.stem for p in concept_files()}
    # ---- indicators ----
    ischema = load_yaml(CONTENT_DIR / "schema-indicator.yaml")
    for path in indicator_files():
        ind = load_yaml(path)
        where = f"content/indicators/{path.name}"
        for key in ischema.get("required", []):
            if key not in ind:
                errors.append(f"{where}: missing '{key}'")
        if path.stem != ind.get("id") or not path.stem.startswith("ind-"):
            errors.append(f"{where}: id must start with ind- and match the file name")
        if "quotes" in ind:
            errors.append(f"{where}: quotes belong in content/quotes.yml, not in the indicator")
        intl = ind.get("international", {}) or {}
        check_src(where, intl.get("standard_source"))
        for ref in (intl.get("definition_quote"), intl.get("formula_quote")):
            check_ref(where, ref)
        for c in intl.get("components", []) or []:
            check_ref(where, c.get("quote"))
            if c.get("id") and c["id"].startswith("con-") and c["id"] not in con_ids:
                errors.append(f"{where}: component {c['id']} has no concept file")
        for iso, c in (ind.get("countries") or {}).items():
            check_src(f"{where}:{iso}", c.get("source"))
            check_ref(f"{where}:{iso}", c.get("definition_quote"))
        for n in ind.get("comparability_notes_ar", []) or []:
            for sid in n.get("sources", []):
                check_src(where, sid)
    # ---- concepts ----
    cschema = load_yaml(CONTENT_DIR / "schema-concept.yaml") if (CONTENT_DIR / "schema-concept.yaml").exists() else {}
    for path in concept_files():
        con = load_yaml(path)
        where = f"content/concepts/{path.name}"
        for key in cschema.get("required", []):
            if key not in con:
                errors.append(f"{where}: missing '{key}'")
        if path.stem != con.get("id") or not path.stem.startswith("con-"):
            errors.append(f"{where}: id must start with con- and match the file name")
        check_ref(where, con.get("definition_quote"))
        check_src(where, con.get("source"))
        for r in con.get("related", []) or []:
            if r not in con_ids | ind_ids:
                errors.append(f"{where}: related id {r} not found")
    for s in set(slots) - used:
        errors.append(f"content/quotes.yml::{s}: slot not referenced by any indicator or concept")

    if "--stats" in sys.argv:
        recs = [r for _, r in iter_sources()]
        by_file = Counter(p.relative_to(SOURCES_DIR).as_posix() for p, _ in iter_sources())
        print(f"Total source records: {len(recs)}")
        print("By status:  ", dict(Counter(r.get("status") for r in recs)))
        print("By priority:", dict(Counter(r.get("priority") for r in recs)))
        print("By type:    ", dict(Counter(r.get("type") for r in recs)))
        qs = load_quotes()
        print(f"Indicators: {len(indicator_files())} · concepts: {len(concept_files())} · quote slots: {len(qs)} ·",
              dict(Counter(q.get("status") for q in qs)))
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
