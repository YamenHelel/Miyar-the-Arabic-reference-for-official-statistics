#!/usr/bin/env python3
"""Write docs/VALIDATION.md: everything in Miʿyar that still needs the lead's (or a reviewer's) check.

Usage:
  python tools/build_validation_queue.py           # rewrite docs/VALIDATION.md
  python tools/build_validation_queue.py --check   # exit 1 if the file is out of date (used in CI)

Generated from the data, so it is always current: run it after any content or source change (end-of-session routine).
Manual items (decisions, settings) come from docs/lead-actions.yml.
"""
import sys
from collections import defaultdict

from common import (ROOT, concept_files, datasource_files, indicator_files, iter_sources, load_quotes,
                    load_yaml, source_files)

OUT = ROOT / "docs" / "VALIDATION.md"
COUNTRIES = {"tun": "Tunisia", "sau": "Saudi Arabia", "mar": "Morocco", "jor": "Jordan", "are": "UAE", "pse": "Palestine",
             "usa": "USA", "gbr": "UK", "aus": "Australia", "fra": "France"}


def users_of_slots():
    """slot id -> list of content ids that use it."""
    use = defaultdict(list)
    for p in indicator_files():
        i = load_yaml(p)
        intl = i.get("international", {})
        for s in [intl.get("definition_quote"), intl.get("formula_quote")] + [c.get("quote") for c in intl.get("components", [])]:
            if s:
                use[s].append(i["id"])
        for iso, c in (i.get("countries") or {}).items():
            if c.get("definition_quote"):
                use[c["definition_quote"]].append(f"{i['id']}:{iso}")
    for p in concept_files():
        c = load_yaml(p)
        use[c["definition_quote"]].append(c["id"])
    for p in datasource_files():
        d = load_yaml(p)
        for oq in d.get("official_quotes", []):
            use[oq["slot"]].append(d["id"])
    return use


def build():
    reg = {r["id"]: r for _, r in iter_sources()}
    quotes = load_quotes()
    use = users_of_slots()
    md = ["# Validation queue (generated, do not edit)", "",
          "Everything in Miʿyar that still needs a human check, in the order the lead should work through it.",
          "Regenerate with `python tools/build_validation_queue.py` (part of the end-of-session routine).",
          "Where to act: the **Verification Desk** (link in `docs/STATUS.md`): ✍️ tab for quotes, sources tab for links.", ""]

    # ---- summary ----
    qs_by = defaultdict(list)
    for q in quotes:
        qs_by[q["status"]].append(q)
    src_by = defaultdict(list)
    for r in reg.values():
        src_by[r["status"]].append(r)
    drafts = []
    for kind, files in (("indicator", indicator_files()), ("concept", concept_files()), ("data source", datasource_files())):
        for p in files:
            d = load_yaml(p)
            if d.get("status") == "draft":
                drafts.append((kind, d["id"], d.get("name_ar", "")))
    snippets = []
    for p in indicator_files():
        i = load_yaml(p)
        for iso, c in (i.get("countries") or {}).items():
            fb = str(c.get("facts_basis", ""))
            if fb and not fb.startswith("quote"):
                snippets.append((i["id"], iso, fb))
    to_verify = []
    for p in source_files():
        if p.parent.name == "countries":
            prof = (load_yaml(p).get("profile") or {})
            for f in prof.get("to_verify", []) or []:
                to_verify.append((p.stem, f))
    manual = load_yaml(ROOT / "docs" / "lead-actions.yml").get("actions", []) if (ROOT / "docs" / "lead-actions.yml").exists() else []
    open_manual = [a for a in manual if a.get("status") != "done"]

    md += ["## Summary", "", "| Queue | Items | Where |", "|---|---|---|",
           f"| 1. Official texts to paste | {len(qs_by['to-paste'])} | Desk ✍️ tab, then say \"apply my quotes\" |",
           f"| 2. Pasted texts to confirm | {len(qs_by['pasted'])} | Desk ✍️ tab (or tell Claude \"confirmed\") |",
           f"| 3. Sources to open and check | {len(src_by['collected']) + len(src_by['link-ok'])} | Desk sources tab, then \"apply my verifications\" |",
           f"| 4. Sources still missing or broken | {len(src_by['to-locate']) + len(src_by['broken'])} | Find a URL or confirm it does not exist |",
           f"| 5. Country facts from search snippets | {len(snippets)} | Confirmed automatically once the country's text is pasted |",
           f"| 6. Country-profile fields to confirm | {len(to_verify)} | Reply in chat or edit the YAML |",
           f"| 7. AI-drafted pages awaiting review | {len(drafts)} | Read the page; say \"reviewed <id>\" or send corrections |",
           f"| 7b. Unofficial translations to review | {sum(1 for q in quotes if q.get('translation_status') == 'unofficial')} | Read each against its original on the indicator page (language switcher) |",
           f"| 8. Code not yet executed | 1 | Stata script (needs someone with Stata) |",
           f"| 9. Lead decisions and settings | {len(open_manual)} | See the list at the end |", ""]

    # ---- 1. quotes to paste, grouped by source ----
    md += ["## 1. Official texts to paste", "",
           "Grouped by document, so one opened document serves several texts. Paste verbatim, in the original language.", ""]
    by_src = defaultdict(list)
    for q in qs_by["to-paste"]:
        by_src[q["source"]].append(q)
    order = sorted(by_src, key=lambda s: (-len(by_src[s]), s))
    for sid in order:
        r = reg.get(sid, {})
        flag = "" if r.get("status") == "verified" else f" ⚠️ source is `{r.get('status')}`: verify the document first"
        md += [f"### {r.get('title_en', sid)} ({len(by_src[sid])}){flag}", f"`{sid}` · {r.get('url', '')}", ""]
        for q in by_src[sid]:
            md.append(f"- `{q['slot']}` → used by {', '.join(use.get(q['slot'], ['(unused)']))}. **Copy:** {q.get('locator', '')}")
        md.append("")

    # ---- 2. pasted ----
    md += ["## 2. Pasted texts awaiting confirmation", ""]
    md += [f"- `{q['slot']}` ({', '.join(use.get(q['slot'], []))}): {q.get('document_note', '')}" for q in qs_by["pasted"]] or ["- none"]
    md.append("")

    # ---- 3/4. sources ----
    md += ["## 3. Sources to open and check", "", "| id | title | status | last robot check |", "|---|---|---|---|"]
    for st in ("collected", "link-ok"):
        for r in sorted(src_by[st], key=lambda r: (r.get("priority", "P3"), r["id"])):
            md.append(f"| `{r['id']}` | {r.get('title_en', '')[:90]} | {st} ({r.get('priority', '')}) | {r.get('link_check', '—')} |")
    md += ["", "## 4. Sources missing or broken", ""]
    for st in ("to-locate", "broken"):
        for r in sorted(src_by[st], key=lambda r: r["id"]):
            md.append(f"- `{r['id']}` ({st}): {r.get('title_en', '')}. {(r.get('notes') or '').strip()[:160]}")
    md.append("")

    # ---- 5/6 ----
    md += ["## 5. Country facts taken from search snippets (shown with «؟» on the site)", ""]
    md += [f"- {COUNTRIES.get(iso, iso)} · `{ind}`: basis `{fb}`" for ind, iso, fb in snippets] or ["- none"]
    md += ["", "## 6. Country-profile fields to confirm", ""]
    md += [f"- {COUNTRIES.get(iso, iso)}: `{f}`" for iso, f in to_verify] or ["- none"]

    # ---- 7. drafts ----
    md += ["", "## 7. AI-drafted pages awaiting review", "",
           "AI text is always labelled on the site; review means a statistician has read it and found nothing wrong.", ""]
    for kind in ("data source", "indicator", "concept"):
        ids = [f"`{i}`" for k, i, _ in drafts if k == kind]
        if ids:
            md.append(f"- **{kind}s ({len(ids)}):** {', '.join(ids)}")
    md += ["", "## 7b. Unofficial translations to review", "",
           "Shown on indicator pages through the عربي / English switcher, always labelled unofficial, with the original one click away.", ""]
    md += [f"- `{q['slot']}` ({q['lang']} → {', '.join(x for x, k in (('ar', 'translation_ar'), ('en', 'translation_en')) if q.get(k))}): "
           f"{q.get('translation_by', '')}" for q in quotes if q.get("translation_status") == "unofficial"] or ["- none"]
    md += ["", "## 8. Code not yet executed", "",
           "- `code/stata/miyar_lfs.do`: written to match Python and R, never run. Someone with Stata runs it on "
           "`code/data/synthetic_lfs.csv` and compares with `code/expected/results_python.json`.",
           "- Hours threshold for time-related underemployment: 35 is a placeholder in every preset until a national text gives it.", ""]

    # ---- 9. manual ----
    md += ["## 9. Lead decisions and settings", "", "From `docs/lead-actions.yml` (edit that file; mark `status: done`).", ""]
    md += [f"- [ ] **{a['title']}**: {a.get('detail', '')}" for a in open_manual] or ["- none"]
    done = [a for a in manual if a.get("status") == "done"]
    if done:
        md += ["", "Done: " + "; ".join(a["title"] for a in done)]
    md.append("")
    return "\n".join(md)


def main():
    text = build()
    if "--check" in sys.argv:
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if cur != text:
            print("docs/VALIDATION.md is out of date: run python tools/build_validation_queue.py")
            sys.exit(1)
        print("docs/VALIDATION.md is current.")
        return
    OUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
