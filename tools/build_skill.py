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

from common import ROOT, concept_files, datasource_files, indicator_files, iter_sources, load_yaml, quotes_by_slot
from markdown_render import concept_md, datasource_md, indicator_md, verifier_name

OUT = ROOT / "skills" / "miyar-labour-stats"
def main():
    reg = {r["id"]: r for _, r in iter_sources()}
    quotes = quotes_by_slot()
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "references").mkdir(parents=True)
    index = []

    for p in indicator_files():
        i = load_yaml(p)
        (OUT / "references" / f"{i['id']}.md").write_text(indicator_md(i, quotes, reg), encoding="utf-8")
        index.append(f"- `references/{i['id']}.md` — indicator: {i['name_ar']} ({i['names']['en']})")

    for p in concept_files():
        c = load_yaml(p)
        (OUT / "references" / f"{c['id']}.md").write_text(concept_md(c, quotes, reg), encoding="utf-8")
        index.append(f"- `references/{c['id']}.md` — concept: {c['name_ar']} ({c['names']['en']})")

    for p in datasource_files():
        d = load_yaml(p)
        (OUT / "references" / f"{d['id']}.md").write_text(datasource_md(d, quotes, reg), encoding="utf-8")
        kind = "LFS guide" if d["kind"] == "guide" else "data source"
        index.append(f"- `references/{d['id']}.md` — {kind}: {d['name_ar']} ({d['names']['en']})")

    code_readme = (ROOT / "code" / "README.md").read_text(encoding="utf-8")
    presets = (ROOT / "code" / "presets" / "countries.json").read_text(encoding="utf-8")
    (OUT / "references" / "code.md").write_text(
        "# Miʿyar code library (compute the indicators from LFS microdata)\n\n"
        "When a user asks how to compute an indicator from microdata, point to these files and adapt the snippets. "
        "Python is tested; R is checked in CI against Python; Stata has not been executed — say so.\n\n"
        + code_readme + "\n\n## Country presets (from verified quotes only)\n\n```json\n" + presets + "\n```\n", encoding="utf-8")
    index.append("- `references/code.md` — code library (Python/R/Stata) to compute the indicators with SEs; country presets")
    src = ["# Miʿyar source registry (snapshot)", "", "| id | title | publisher | country | status | verified |", "|---|---|---|---|---|---|"]
    for _, r in iter_sources():
        src.append(f"| {r['id']} | {r.get('title_en', '')} | {r.get('publisher', '')} | {r.get('country', '')} | {r['status']} | "
                   f"{verifier_name(r.get('verified_by', ''))} {r.get('verified_date', '') or ''} |")
    (OUT / "references" / "sources.md").write_text("\n".join(src) + "\n", encoding="utf-8")
    index.append("- `references/sources.md` — every source with its verification status")

    skill = f"""---
name: miyar-labour-stats
description: >-
  Miʿyar (مِعيار), the Arabic reference for official statistics. Use when someone asks about labour-statistics definitions,
  indicators or concepts (unemployment rate, labour force participation, employment-to-population ratio, youth unemployment,
  employed/unemployed, labour force, potential labour force, time-related underemployment, standard error), data sources
  (labour force survey design, questionnaire, sampling, weighting; census; administrative records; establishment surveys), ILO/ICLS
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
