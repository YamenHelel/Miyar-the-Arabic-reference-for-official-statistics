#!/usr/bin/env python3
"""Generate the Claude skill skills/miyar-labour-stats/ from the Miʿyar knowledge base.

Usage:
  python tools/build_skill.py

Output (committed, so the skill can be installed from the repo):
  skills/miyar-labour-stats/SKILL.md            instructions + index of what the base contains
  skills/miyar-labour-stats/references/*.md     one file per indicator and concept, plus sources and countries
Rules carried into the skill: answer only from the references; official wording only from verified/pasted quotes,
always with its source and verification date; AI explanations labelled; say "not in Miʿyar yet" otherwise.
"""
import datetime as dt
import shutil

from common import ROOT, concept_files, indicator_files, iter_sources, load_yaml, quotes_by_slot

OUT = ROOT / "skills" / "miyar-labour-stats"
COUNTRIES = {"tun": "تونس", "sau": "السعودية", "mar": "المغرب", "jor": "الأردن", "are": "الإمارات", "pse": "فلسطين",
             "usa": "الولايات المتحدة", "gbr": "المملكة المتحدة", "aus": "أستراليا", "fra": "فرنسا"}
STATE = {"verified": "VERIFIED official text", "pasted": "official text, PASTED — awaiting reviewer confirmation"}


def quote_md(q, reg):
    if not q:
        return "_No official text linked._\n"
    src = reg.get(q.get("source"), {})
    head = f"**Source:** {src.get('title_en', q.get('source'))} — {src.get('publisher', '')}  \n"
    head += f"**URL:** {q.get('quoted_from_url') or src.get('url', '')}  \n**Locator:** {q.get('locator', '')}  \n"
    if q.get("status") in STATE and q.get("text"):
        head += f"**Status:** {STATE[q['status']]}" + (f" (by {q.get('verified_by')}, {q.get('pasted_on')})" if q.get("verified_by") else "") + "  \n"
        if q.get("document_note"):
            head += f"**Note:** {q['document_note']}  \n"
        body = "\n".join("> " + l if l.strip() else ">" for l in q["text"].split("\n"))
        return head + f"**Language:** {q.get('lang')}\n\n{body}\n"
    return head + "**Status:** NOT YET AVAILABLE — do not quote; say the official text is pending in Miʿyar.\n"


def main():
    reg = {r["id"]: r for _, r in iter_sources()}
    quotes = quotes_by_slot()
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "references").mkdir(parents=True)
    index = []

    for p in indicator_files():
        i = load_yaml(p)
        intl = i["international"]
        md = [f"# {i['name_ar']} — {i['names']['en']} / {i['names']['fr']}", "",
              f"Miʿyar id: `{i['id']}` · status: {i['status']} · last updated {i['last_updated']}" +
              (f" · SDG {', '.join(i['sdg'])}" if i.get("sdg") else ""), "",
              "## International definition", "", quote_md(quotes.get(intl.get("definition_quote")), reg)]
        md += ["## Formula", "", f"- {intl.get('formula_ar', '')}", f"- `{intl.get('formula', '')}`", ""]
        if intl.get("formula_quote"):
            md += ["### Official text for the formula", "", quote_md(quotes.get(intl["formula_quote"]), reg)]
        if intl.get("notes_ar"):
            md += [f"Notes (Miʿyar commentary): {' '.join(str(intl['notes_ar']).split())}", ""]
        md += ["## Country practice", "",
               "| Country | Survey | Age | Job-search period | Availability | Frequency | Facts basis |",
               "|---|---|---|---|---|---|---|"]
        for iso, c in i["countries"].items():
            md.append(f"| {COUNTRIES.get(iso, iso)} | {c.get('survey', '')} | {c.get('age', '')} | {c.get('job_search_period', '—')} | "
                      f"{c.get('availability', '—')} | {c.get('frequency', '')} | {c.get('facts_basis', '')} |")
        md += ["", "Facts whose basis is `search-snippet` are preliminary: present them as unconfirmed.", "",
               "## National definitions (verbatim)", ""]
        for iso, c in i["countries"].items():
            md += [f"### {COUNTRIES.get(iso, iso)}", ""]
            md += [quote_md(quotes.get(c.get("definition_quote")), reg) if c.get("definition_quote")
                   else f"_{c.get('definition_note', 'Not in Miʿyar yet.')}_\n"]
        md += ["## Comparability notes (Miʿyar commentary, sourced)", ""]
        for n in i.get("comparability_notes_ar", []):
            md.append(f"- {n['text']} (sources: {', '.join(n.get('sources', []))})")
        md += ["", "## Plain explanation — AI-ASSISTED, label it as such when you use it", "",
               " ".join(str(i.get("explanation_ai_ar", "")).split()), ""]
        (OUT / "references" / f"{i['id']}.md").write_text("\n".join(md), encoding="utf-8")
        index.append(f"- `references/{i['id']}.md` — indicator: {i['name_ar']} ({i['names']['en']})")

    for p in concept_files():
        c = load_yaml(p)
        md = [f"# {c['name_ar']} — {c['names']['en']} / {c['names']['fr']}", "", f"Miʿyar id: `{c['id']}` · category: {c['category']}", "",
              "## Official definition", "", quote_md(quotes.get(c.get("definition_quote")), reg)]
        if c.get("formula"):
            md += ["## Formula", "", f"`{c['formula']}`", ""]
        if c.get("term_variants"):
            md += ["## Arabic term variants", ""] + [f"- {v['term']} — used in: {', '.join(COUNTRIES.get(x, x) for x in v.get('used_in', [])) or 'to confirm'} ({v.get('basis', '')})"
                                                     for v in c["term_variants"]] + [""]
        md += ["## Plain explanation — AI-ASSISTED", "", " ".join(str(c.get("explanation_ai_ar", "")).split()), ""]
        if c.get("example_ai_ar"):
            md += ["## Worked example — AI-ASSISTED, illustrative numbers", "", " ".join(str(c["example_ai_ar"]).split()), ""]
        (OUT / "references" / f"{c['id']}.md").write_text("\n".join(md), encoding="utf-8")
        index.append(f"- `references/{c['id']}.md` — concept: {c['name_ar']} ({c['names']['en']})")

    src = ["# Miʿyar source registry (snapshot)", "", "| id | title | publisher | country | status | verified |", "|---|---|---|---|---|---|"]
    for _, r in iter_sources():
        src.append(f"| {r['id']} | {r.get('title_en', '')} | {r.get('publisher', '')} | {r.get('country', '')} | {r['status']} | "
                   f"{r.get('verified_by', '')} {r.get('verified_date', '') or ''} |")
    (OUT / "references" / "sources.md").write_text("\n".join(src) + "\n", encoding="utf-8")
    index.append("- `references/sources.md` — every source with its verification status")

    skill = f"""---
name: miyar-labour-stats
description: >-
  Miʿyar (مِعيار), the Arabic reference for official statistics. Use when someone asks about labour-statistics definitions,
  indicators or concepts (unemployment rate, labour force participation, employment-to-population ratio, youth unemployment,
  employed/unemployed, labour force, potential labour force, time-related underemployment, standard error), ILO/ICLS
  standards, SDG 8.5.2, or how Tunisia, Saudi Arabia, Morocco, Jordan, UAE, Palestine, USA, UK, Australia or France define them —
  in Arabic, French or English. Answers come only from Miʿyar's verified references, with sources.
---

# Miʿyar — labour statistics (snapshot {dt.date.today().isoformat()})

You answer as Miʿyar's assistant for official statisticians. Default language: Arabic (Modern Standard), unless the user writes
in another language.

## Rules (strict)
1. Answer ONLY from the files in `references/`. Read the index below, open the one or two relevant files, then answer.
2. Official wording: quote it **exactly as written in the reference, in its original language**, only when its status is
   VERIFIED or PASTED. Always give the source title, the locator (paragraph/section) and the URL. For PASTED, say it awaits
   reviewer confirmation.
3. If a reference says NOT YET AVAILABLE, or the question is not covered, say: «هذا غير متوفر في مِعيار بعد» and suggest the
   official source to consult. Never fill the gap from memory.
4. Translations you make are unofficial: label them «ترجمة غير رسمية».
5. Text marked AI-ASSISTED may be used for explanation, labelled «شرح مُعدّ بمساعدة الذكاء الاصطناعي».
6. Facts with basis `search-snippet` are preliminary: say they are not yet confirmed by an official text.
7. When comparing countries, mention the reference population (nationals vs total) and the differences in age, search period
   and availability — they change the published rate.
8. End answers that use official text with: «المصدر: مِعيار — [title], [URL]، تاريخ التحقق [date]».

## What Miʿyar contains
{chr(10).join(index)}

Website: built from the same data (repository: github.com/YamenHelel/Miyar-the-Arabic-reference-for-official-statistics).
Corrections and contributions: yamen.hlel@gmail.com. Content licence CC BY 4.0.
"""
    (OUT / "SKILL.md").write_text(skill, encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Miʿyar Claude skill\n\nGenerated by `python tools/build_skill.py` — do not edit by hand.\n\n"
        "Install: copy the folder `miyar-labour-stats/` into your Claude skills (Claude Code: `~/.claude/skills/`; "
        "claude.ai: Settings → Capabilities → Skills → upload a zip of the folder).\n\n"
        "The skill answers only from `references/`, quotes official text verbatim with its source, and says when "
        "something is not in Miʿyar yet.\n", encoding="utf-8")
    print(f"Skill written: {len(index)} reference files")


if __name__ == "__main__":
    main()
