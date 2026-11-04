#!/usr/bin/env python3
"""Render one indicator (content/indicators/<id>.yml) as a standalone Arabic HTML page.

Usage:
  python tools/build_indicator_page.py ind-unemployment-rate OUT.html

This is the first version of the website's indicator template (Phase 0b preview).
Rules it enforces on screen:
  - official wording only from quotes[] with status pasted/verified; otherwise a visible "awaiting official text" box
  - facts with basis search-snippet carry a "to confirm" marker
  - explanation_ai_ar is always shown under an AI label
"""
import datetime as dt
import html
import sys
from pathlib import Path

from common import CONTENT_DIR, iter_sources, load_yaml

COUNTRIES = {
    "tun": "تونس", "sau": "السعودية", "mar": "المغرب", "jor": "الأردن", "are": "الإمارات", "pse": "فلسطين",
    "usa": "الولايات المتحدة", "gbr": "المملكة المتحدة", "aus": "أستراليا", "fra": "فرنسا",
}
ORDER = ["tun", "sau", "mar", "jor", "are", "pse", "usa", "gbr", "aus", "fra"]
STATUS_AR = {"verified": "مُتحقَّق منه", "link-ok": "الرابط يعمل", "collected": "قيد التحقق", "broken": "معطّل",
             "to-locate": "غير موجود بعد", "superseded": "مُستبدَل"}
e = html.escape


def quote_block(q, src):
    if not q:
        return ""
    cite = f'<a href="{e(src.get("url", ""))}" target="_blank" rel="noopener">{e(src.get("title_en", q["source"]))}</a>'
    if q.get("status") in ("pasted", "verified") and q.get("text"):
        d = "rtl" if q.get("lang") == "ar" else "ltr"
        badge = "نص رسمي — مُتحقَّق منه" if q["status"] == "verified" else "نص رسمي — منسوخ، بانتظار المراجعة"
        return (f'<figure class="quote"><span class="qbadge">{badge}</span>'
                f'<blockquote dir="{d}" lang="{e(q.get("lang", "en"))}">{e(q["text"])}</blockquote>'
                f'<figcaption>{cite} · {e(q.get("locator", ""))}</figcaption></figure>')
    return (f'<figure class="quote pending"><span class="qbadge">بانتظار النص الرسمي</span>'
            f'<p>سيُنسخ هنا النص الحرفي من <a href="{e(src.get("url", ""))}" target="_blank" rel="noopener">المصدر ↗</a></p>'
            f'<figcaption dir="auto">{e(q.get("locator", ""))}</figcaption></figure>')


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    ind = load_yaml(CONTENT_DIR / "indicators" / f"{sys.argv[1]}.yml")
    reg = {r["id"]: r for _, r in iter_sources()}
    quotes = {q["slot"]: q for q in ind.get("quotes", [])}
    intl = ind["international"]

    def src_of(slot):
        q = quotes.get(slot) or {}
        return reg.get(q.get("source"), {})

    used = set()
    comps = "".join(
        f'<li><b>{e(c["name_ar"])}</b>{quote_block(quotes.get(c.get("quote")), src_of(c.get("quote")))}</li>'
        for c in intl.get("components", []) if c.get("quote") != intl.get("definition_quote"))

    rows = []
    for iso in ORDER:
        c = ind["countries"].get(iso)
        if not c:
            continue
        used.add(c["source"])
        flag = ' <span class="tc" title="من مقتطف بحث — بانتظار التأكيد من النص">؟</span>' if c.get("facts_basis") == "search-snippet" else ""
        q = quotes.get(c.get("definition_quote"), {})
        qstate = "✓ منسوخ" if q.get("status") in ("pasted", "verified") else "بانتظار النص"
        rows.append(
            f'<tr><th scope="row">{COUNTRIES[iso]}</th><td dir="auto">{e(c.get("survey", ""))}</td>'
            f'<td>{e(c.get("age", "—"))}{flag}</td><td dir="auto">{e(c.get("job_search_period", "—"))}</td>'
            f'<td dir="auto">{e(c.get("frequency", "—"))}</td><td dir="auto">{e(c.get("population_note", ""))}</td>'
            f'<td><span class="qs">{qstate}</span></td></tr>')

    notes = "".join(f'<li>{e(n["text"])}</li>' for n in ind.get("comparability_notes_ar", []))
    for n in ind.get("comparability_notes_ar", []):
        used.update(n.get("sources", []))
    used.update(q["source"] for q in quotes.values())
    used.add(intl["standard_source"])
    srcs = "".join(
        f'<li><a href="{e(reg[s]["url"])}" target="_blank" rel="noopener" dir="auto">{e(reg[s]["title_en"])}</a>'
        f' <span class="st st-{e(reg[s]["status"])}">{STATUS_AR.get(reg[s]["status"], reg[s]["status"])}</span></li>'
        for s in sorted(used) if s in reg and str(reg[s].get("url", "")).startswith("http"))
    pasted = sum(q.get("status") in ("pasted", "verified") for q in quotes.values())

    tpl = (Path(__file__).resolve().parent / "indicator" / "template.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{NAME_AR}}", e(ind["name_ar"]))
              .replace("{{NAME_EN}}", e(ind["names"]["en"]))
              .replace("{{NAME_FR}}", e(ind["names"]["fr"]))
              .replace("{{SDG}}", " · ".join(f"هدف التنمية المستدامة {e(s)}" for s in ind.get("sdg", [])))
              .replace("{{CUSTODIAN}}", e(intl.get("custodian", "")))
              .replace("{{STANDARD}}", e(reg.get(intl["standard_source"], {}).get("title_en", "")))
              .replace("{{DEF_QUOTE}}", quote_block(quotes.get(intl["definition_quote"]), src_of(intl["definition_quote"])))
              .replace("{{FORMULA_AR}}", e(intl.get("formula_ar", "")))
              .replace("{{FORMULA}}", e(intl.get("formula", "")))
              .replace("{{FORMULA_QUOTE}}", quote_block(quotes.get(intl.get("formula_quote")), src_of(intl.get("formula_quote"))))
              .replace("{{COMPONENTS}}", comps)
              .replace("{{INTL_NOTES}}", e(" ".join(str(intl.get("notes_ar", "")).split())))
              .replace("{{ROWS}}", "".join(rows))
              .replace("{{NOTES}}", notes)
              .replace("{{AI}}", e(" ".join(str(ind.get("explanation_ai_ar", "")).split())))
              .replace("{{SOURCES}}", srcs)
              .replace("{{STATUS}}", {"draft": "مسودة", "reviewed": "مُراجَع", "verified": "مُتحقَّق منه"}[ind["status"]])
              .replace("{{PROGRESS}}", f"{pasted}/{len(quotes)}")
              .replace("{{UPDATED}}", str(ind.get("last_updated", dt.date.today()))))
    Path(sys.argv[2]).write_text(out, encoding="utf-8")
    print(f"Wrote {sys.argv[2]} ({pasted}/{len(quotes)} official texts in place)")


if __name__ == "__main__":
    main()
