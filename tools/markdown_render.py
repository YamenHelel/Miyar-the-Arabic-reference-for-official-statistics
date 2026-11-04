"""Markdown rendering of Miʿyar indicators and concepts (shared by the Claude skill, llms-full.txt and .md page twins)."""

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


def indicator_md(i, quotes, reg, url=None):
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
    if url:
        md += [f"Page: {url}", ""]
    return "\n".join(md)


def concept_md(c, quotes, reg, url=None):
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
    if url:
        md += [f"Page: {url}", ""]
    return "\n".join(md)
