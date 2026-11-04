#!/usr/bin/env python3
"""Build the Miʿyar website (static, Arabic, RTL) from the repository's data.

Usage:
  python tools/build_site.py [OUT_DIR]        # default: _site/

Reads sources/, content/ (indicators, concepts, quotes.yml) and renders tools/site/templates/*.html
with jinja2. Design system: tools/site/static/miyar.css (see ADR-0008). Every page is plain HTML that
works without JavaScript; miyar.js adds search, the ruler and motion.
"""
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from common import (CONTENT_DIR, ROOT, SOURCES_DIR, concept_files, indicator_files, iter_sources,
                    load_yaml, quotes_by_slot, source_files)

SITE = Path(__file__).resolve().parent / "site"
COUNTRIES = {"tun": "تونس", "sau": "السعودية", "mar": "المغرب", "jor": "الأردن", "are": "الإمارات", "pse": "فلسطين",
             "usa": "الولايات المتحدة", "gbr": "المملكة المتحدة", "aus": "أستراليا", "fra": "فرنسا", "int": "دولي"}
ARAB = ["tun", "sau", "mar", "jor", "are", "pse"]
REFC = ["usa", "gbr", "aus", "fra"]
FREQ_AR = {"monthly": "شهري", "quarterly": "ربع سنوي", "annual": "سنوي", "quarterly + annual": "ربع سنوي وسنوي",
           "quarterly (rolling)": "ربع سنوي (متحرك)", "continuous, quarterly results": "مستمر، بنتائج ربع سنوية"}
STATUS_AR = {"verified": "مُتحقَّق منه", "link-ok": "الرابط يعمل", "collected": "قيد التحقق", "broken": "معطّل",
             "to-locate": "غير موجود بعد", "superseded": "مُستبدَل"}
TYPE_AR = {"standard": "معيار", "manual": "دليل", "methodology": "منهجية", "questionnaire": "استمارة", "metadata": "بيانات وصفية",
           "sdg-metadata": "بيانات وصفية لأهداف التنمية", "database": "قاعدة بيانات", "publication": "منشور", "glossary": "مسرد",
           "microdata": "بيانات جزئية", "portal": "بوابة", "classification": "تصنيف", "organisation": "جهة", "news": "خبر"}
ACCESS_AR = {"public": "تنزيل حر", "registration": "تسجيل مجاني", "licensed": "بترخيص وطلب", "secure": "بيئة آمنة فقط",
             "none-found": "لم يُعثر على مسار", "unknown": "شروط الوصول غير معروفة بعد"}
LFS_LABELS = {"name_en": "الاسم", "name_fr": "الاسم", "name_ar": "الاسم بالعربية", "frequency": "الدورية", "mode": "طريقة الجمع",
              "coverage": "التغطية", "sample": "العينة", "icls_standard": "المعيار المطبَّق", "age": "السن", "history": "التاريخ",
              "universe": "المجتمع", "framework": "الإطار", "status_note": "ملاحظة", "standards_note": "المعايير",
              "employed_definition_note": "تعريف المشتغل", "classifications": "التصنيفات", "unemployed": "تعريف المتعطل",
              "unemployed_fr": "تعريف المتعطل", "scope": "النطاق", "coverage_note": "ملاحظة التغطية"}


LIST_START = re.compile(r"^\s*(\(?[a-z]\)|\(?[ivx]+\)|\([a-z]\)|LU\d|\d+(\.\d+)*\.?\s|\d+\.\S|[•\-–]|[أ-ي]\.|\d+\s*\.|[a-zA-Z][a-zA-Z ]{0,24}$)")


def reflow(text):
    """Display only: join PDF hard-wrapped lines, keep a break before list items, numbered paragraphs and short headings.
    The stored quotation stays verbatim."""
    if not text:
        return text
    lines = [l.rstrip() for l in str(text).replace("\r\n", "\n").split("\n")]
    out = []
    for l in lines:
        if not l.strip():
            out.append("")
            continue
        if out and out[-1] != "" and not LIST_START.match(l) and not re.match(r"^[A-Z][a-z]+$", out[-1].strip()):
            out[-1] = out[-1] + " " + l.strip()
        else:
            out.append(l.strip())
    return "\n".join(x for x in out)


def status_state(q):
    if not q:
        return None
    return {"verified": "منسوخ ومُتحقَّق منه", "pasted": "منسوخ، بانتظار التأكيد"}.get(q.get("status"), "بانتظار النص")


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site"
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SITE / "static", out / "static")

    reg = {r["id"]: r for _, r in iter_sources()}
    quotes = quotes_by_slot()
    inds = [load_yaml(p) for p in indicator_files()]
    order = ["ind-unemployment-rate", "ind-labour-force-participation-rate", "ind-employment-to-population-ratio", "ind-youth-unemployment-rate"]
    inds.sort(key=lambda i: order.index(i["id"]) if i["id"] in order else 99)
    cons = [load_yaml(p) for p in concept_files()]
    con_by = {c["id"]: c for c in cons}
    ind_by = {i["id"]: i for i in inds}
    profiles = {}
    for p in source_files():
        if p.parent.name == "countries":
            profiles[p.stem] = load_yaml(p)
    catalog = load_yaml(SOURCES_DIR / "microdata" / "puf-catalog.yaml").get("catalog", [])

    built = dt.date.today().isoformat()
    vq = sum(1 for q in quotes.values() if q.get("status") == "verified")
    stats = {"sources": len(reg), "verified_sources": sum(1 for r in reg.values() if r.get("status") == "verified"), "verified_quotes": vq}
    counts_line = " · ".join(f"{STATUS_AR[k]} {v}" for k, v in sorted(
        {s: sum(1 for r in reg.values() if r.get("status") == s) for s in STATUS_AR}.items(), key=lambda kv: -kv[1]) if v)

    env = Environment(loader=FileSystemLoader(SITE / "templates"), autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    env.filters["tojson_ar"] = lambda v: json.dumps(v, ensure_ascii=False)
    env.filters["reflow"] = reflow

    def render(tpl, path, **ctx):
        depth = len(Path(path).parts) - 1
        root = "../" * depth
        f = out / path
        f.parent.mkdir(parents=True, exist_ok=True)
        ctx.setdefault("description", None)
        html = env.get_template(tpl).render(root=root, built=built, stats=stats, q=lambda s: quotes.get(s),
                                            srcq=lambda s: reg.get((quotes.get(s) or {}).get("source"), {}), **ctx)
        f.write_text(html, encoding="utf-8")

    def qref_count(i):
        refs = [i["international"].get("definition_quote"), i["international"].get("formula_quote")]
        refs += [c.get("quote") for c in i["international"].get("components", [])]
        refs += [c.get("definition_quote") for c in i["countries"].values()]
        refs = [r for r in dict.fromkeys(filter(None, refs))]
        done = sum(1 for r in refs if (quotes.get(r) or {}).get("status") in ("verified", "pasted"))
        return done, len(refs)

    # ---------------- indicators ----------------
    for i in inds:
        done, total = qref_count(i)
        rows, national = [], []
        for iso in ARAB + REFC:
            c = i["countries"].get(iso)
            if not c:
                continue
            q = quotes.get(c.get("definition_quote"))
            m = c.get("measures") or {}
            rows.append({"iso": iso, "name": COUNTRIES[iso], "survey": c.get("survey", ""),
                         "age": c.get("age", "—"), "unconfirmed": not str(c.get("facts_basis", "")).startswith("quote"),
                         "search": c.get("job_search_period", "—"), "availability": c.get("availability", "—"),
                         "frequency": FREQ_AR.get(c.get("frequency", ""), c.get("frequency", "—")), "qstate": status_state(q) if q else None})
            src = reg.get((q or {}).get("source") or c.get("source"), {})
            national.append({"iso": iso, "name": COUNTRIES[iso], "pending": not (q and q.get("text")),
                             "state": status_state(q) if q else "يُضاف لاحقاً",
                             "text": reflow((q or {}).get("text")), "lang": (q or {}).get("lang", "ar"),
                             "url": (q or {}).get("quoted_from_url") or src.get("url", ""),
                             "src_title": src.get("title_ar") or src.get("title_en", ""),
                             "note": (q or {}).get("document_note") or c.get("definition_note") or (q or {}).get("locator", "")})
        notes = [{"text": n["text"], "cites": "، ".join(reg[s].get("publisher", s) for s in n.get("sources", []) if s in reg)}
                 for n in i.get("comparability_notes_ar", [])]
        used = {i["international"].get("standard_source")}
        for qid in [i["international"].get("definition_quote"), i["international"].get("formula_quote")] + \
                   [c.get("definition_quote") for c in i["countries"].values()]:
            if qid and qid in quotes:
                used.add(quotes[qid]["source"])
        for n in i.get("comparability_notes_ar", []):
            used.update(n.get("sources", []))
        sources = sorted(({"url": reg[s]["url"], "title": reg[s].get("title_ar") or reg[s]["title_en"], "status": reg[s]["status"],
                           "status_ar": STATUS_AR[reg[s]["status"]], "publisher": reg[s].get("publisher", "")}
                          for s in used if s in reg and str(reg[s].get("url", "")).startswith("http")), key=lambda x: x["title"])
        components = []
        for c in i["international"].get("components", []):
            components.append({"id": c["id"], "name_ar": c["name_ar"], "state": status_state(quotes.get(c.get("quote"))) if c.get("quote") else ""})
        variants = "، ".join(v["term"] for v in i.get("term_variants", []) if v.get("used_in") and v["term"] != i["name_ar"])
        render("indicator.html", f"indicators/{i['id']}.html", title=f"{i['name_ar']} · مِعيار", section="indicators", ind=i,
               done=done, total=total, rows=rows, national=national, notes=notes, sources=sources, components=components,
               variants=variants, others=[o for o in inds if o["id"] != i["id"]],
               description=f"{i['name_ar']}: التعريف الدولي والتعاريف الوطنية في عشر دول، منسوخة من مصادرها.")
    render("index_list.html", "indicators/index.html", title="المؤشرات · مِعيار", section="indicators", heading="المؤشرات",
           intro="أربعة مؤشرات تجريبية في إحصاءات العمل. كل بطاقة تجمع النص الدولي والتعاريف الوطنية وملاحظات المقارنة.",
           groups=[{"title": "", "rows": [{"href": f"indicators/{i['id']}.html", "name": i["name_ar"],
                     "meta": "النصوص الرسمية {} من {}".format(*qref_count(i)), "sub": i["names"]["en"]} for i in inds]}])

    # ---------------- concepts ----------------
    cat_ar = {"labour": "مفاهيم العمل", "statistical": "مفاهيم إحصائية", "survey": "المسوح", "classification": "التصنيفات"}
    for c in cons:
        related = []
        for r in c.get("related", []):
            if r in con_by:
                related.append({"href": f"concepts/{r}.html", "name": con_by[r]["name_ar"]})
            elif r in ind_by:
                related.append({"href": f"indicators/{r}.html", "name": ind_by[r]["name_ar"]})
        vl = [{"term": v["term"], "where": "، ".join(COUNTRIES.get(x, x) for x in v.get("used_in", [])) or "الاستعمال قيد التحقق",
               "basis": v.get("basis", "")} for v in c.get("term_variants", [])]
        render("concept.html", f"concepts/{c['id']}.html", title=f"{c['name_ar']} · مِعيار", section="concepts", con=c,
               cat=cat_ar.get(c["category"], c["category"]), related=related, variants_list=vl,
               variants="، ".join(v["term"] for v in c.get("term_variants", [])))
    groups = []
    for cat in ["labour", "statistical"]:
        rows = [{"href": f"concepts/{c['id']}.html", "name": c["name_ar"], "meta": c["names"]["en"],
                 "sub": status_state(quotes.get(c["definition_quote"]))} for c in cons if c["category"] == cat]
        if rows:
            groups.append({"title": cat_ar[cat], "rows": rows})
    render("index_list.html", "concepts/index.html", title="المفاهيم · مِعيار", section="concepts", heading="المفاهيم",
           intro="المسرد: المصطلح العربي ومتغيراته بين الدول، ومقابله في المعيار الدولي، وتعريفه الرسمي.", groups=groups)

    # ---------------- countries ----------------
    unemp = ind_by.get("ind-unemployment-rate", {"countries": {}})
    cards = {}
    for iso in ARAB + REFC:
        prof = profiles.get(iso, {})
        p = prof.get("profile", {})
        nso = p.get("nso", {})
        recs = [r for r in prof.get("sources", [])]
        lfs = []
        for k, v in (p.get("lfs") or {}).items():
            if isinstance(v, (str, int)) and k in LFS_LABELS:
                lfs.append((LFS_LABELS[k], v))
            elif isinstance(v, list) and k in LFS_LABELS:
                lfs.append((LFS_LABELS[k], "، ".join(map(str, v))))
        defs = []
        for i in inds:
            c = i["countries"].get(iso)
            if c and c.get("definition_quote"):
                defs.append({"ind": i["id"], "name": i["name_ar"], "state": status_state(quotes.get(c["definition_quote"]))})
        micro = []
        for e in catalog:
            if e.get("country") == iso:
                for r in e.get("routes", []):
                    url = r.get("url") if str(r.get("url", "")).startswith("http") else ""
                    micro.append({"provider": r.get("provider"), "url": url, "access": ACCESS_AR.get(r.get("access_level"), r.get("access_level")),
                                  "years": r.get("years", "")})
        name_local = nso.get("name_ar") or nso.get("name_en") or nso.get("name_fr") or ""
        card = {"iso": iso, "name": COUNTRIES[iso], "arab": iso in ARAB, "nso": name_local, "nso_url": nso.get("url", ""),
                "verified": sum(1 for r in recs if r.get("status") == "verified"), "total": len(recs), "lfs": lfs,
                "notes": " ".join(str(p.get("notes", "") or "").split()), "definitions": defs, "micro": micro,
                "sources": [{"url": str(r.get("url", "")), "title": r.get("title_ar") or r.get("title_en", ""),
                             "type": TYPE_AR.get(r.get("type"), r.get("type")), "status": r["status"], "status_ar": STATUS_AR[r["status"]]} for r in recs]}
        cards[iso] = card
    for iso, card in cards.items():
        render("country.html", f"countries/{iso}.html", title=f"{card['name']} · مِعيار", section="countries", c=card,
               others=[cards[o] for o in ARAB + REFC if o != iso])
    render("index_list.html", "countries/index.html", title="الدول · مِعيار", section="countries", heading="الدول",
           intro="ست دول عربية في المرحلة الأولى، وأربع دول مرجعية للمقارنة. تُضاف الدول تباعاً.",
           groups=[{"title": "الدول العربية", "rows": [{"href": f"countries/{i}.html", "name": cards[i]["name"], "meta": f"{cards[i]['verified']} مصدراً مُتحقَّقاً منه", "sub": cards[i]["nso"]} for i in ARAB]},
                   {"title": "دول مرجعية", "rows": [{"href": f"countries/{i}.html", "name": cards[i]["name"], "meta": f"{cards[i]['verified']} مصدراً مُتحقَّقاً منه", "sub": cards[i]["nso"]} for i in REFC]}])

    # ---------------- sources registry ----------------
    rows = []
    for _, r in iter_sources():
        rows.append({"url": str(r.get("url", "")), "title": r.get("title_ar") or r.get("title_en", ""), "publisher": r.get("publisher", ""),
                     "country": COUNTRIES.get(r.get("country", "int"), r.get("country", "")), "type": TYPE_AR.get(r.get("type"), r.get("type")),
                     "status": r["status"], "status_ar": STATUS_AR[r["status"]], "vdate": str(r.get("verified_date", "") or ""),
                     "scope": "int" if r.get("country") in (None, "int") else "country"})
    rows.sort(key=lambda x: (["verified", "link-ok", "collected", "to-locate", "broken", "superseded"].index(x["status"]), x["title"]))
    render("sources.html", "sources/index.html", title="سجل المصادر · مِعيار", section="sources", rows=rows, counts=counts_line,
           filters=[(k, v) for k, v in STATUS_AR.items()] + [("int", "دولية"), ("country", "وطنية")])

    render("about.html", "about/index.html", title="المنهجية · مِعيار", section="about", counts=counts_line)

    # ---------------- home ----------------
    first = "ind-unemployment-rate"
    slips = []
    heights = [36, 28, 44, 30, 40, 26]
    for k, iso in enumerate(["sau", "jor", "are", "mar", "aus", "usa"]):
        c = unemp["countries"].get(iso, {})
        q = quotes.get(c.get("definition_quote"))
        if q and q.get("status") == "verified":
            slips.append({"iso": iso, "country": COUNTRIES[iso], "text": " ".join(q["text"].split()), "lang": q.get("lang", "ar"),
                          "h": heights[k % 6], "lines": 6 + heights[k % 6] // 6})
    rc = []
    intl = unemp["international"].get("measures", {})
    rc.append({"name": "المعيار الدولي", "availability": intl.get("availability_days_after_reference_max"), "search": intl.get("search_days"), "age": None})
    for iso in ARAB + REFC:
        m = (unemp["countries"].get(iso) or {}).get("measures") or {}
        rc.append({"name": COUNTRIES[iso], "availability": m.get("availability_days_after_reference"), "search": m.get("search_days"), "age": m.get("age_min")})
    ruler = {"countries": rc, "criteria": {
        "availability": {"min": 0, "max": 28, "step": 1, "major": 7, "unit": "يوماً",
                         "note": "عدد الأيام التي يُقبل فيها أن يبدأ الشخص العمل بعد فترة الإسناد. قرار المؤتمر 19 يسمح بأسبوعين على الأكثر."},
        "search": {"min": 0, "max": 35, "step": 1, "major": 7, "unit": "يوماً",
                   "note": "الفترة التي يجب أن يكون الشخص قد بحث فيها عن عمل. هنا تتفق الدول: أربعة أسابيع."},
        "age": {"min": 14, "max": 17, "step": 1, "major": 1, "unit": "سنة",
                "note": "الحد الأدنى لسن السكان في سن العمل كما ورد في نص تعريف المتعطل."}}}
    ilo47 = quotes.get("q-ilo-unemployed", {})
    tun = reg.get("src-tun-ins-enpe-methodo", {})
    moments = [
        {"title": "وُجد المصدر", "gap": 24, "text": "يُسجَّل كل رابط يُعثر عليه في سجل المصادر بحالة «قيد التحقق»، ولا يُبنى عليه شيء بعد.",
         "art": "<pre>id: src-tun-ins-enpe-methodo\ntitle_orig: Note méthodologique\npublisher: Institut National\n  de la Statistique\ntype: methodology\nstatus: collected</pre>"},
        {"title": "فُحص الرابط آلياً", "gap": 96, "text": "كل أسبوع يفتح روبوت كل الروابط ويسجّل النتيجة. بعض المواقع ترفض الروبوت، فيبقى القرار للإنسان.",
         "art": "<pre>link_check: \"2026-11-04 200\"\nstatus: link-ok\n\nlink_check: \"2026-11-04 403\"\n# الموقع يحجب الروبوت\nstatus: collected</pre>"},
        {"title": "فتحه إنسان", "gap": 48, "text": "يفتح المراجع الوثيقة ويتأكد من عنوانها وناشرها وإصدارها، ثم يوقّع باسمه والتاريخ.",
         "art": '<img src="static/img/desk-card.jpg" alt="بطاقة مصدر في مكتب التحقق: عنوان الوثيقة ورابطها وأزرار صحيح ويحتاج تعديل ومعطّل" width="712" height="385" loading="lazy">'},
        {"title": "نُسخ النص حرفياً", "gap": 128, "text": "يُنسخ التعريف كما ورد. حين يتشوّه النص العربي عند النسخ من ملف PDF، يُنقل من صورة الصفحة نفسها.",
         "art": '<img src="static/img/pcbs-definition.png" alt="صورة جدول من دليل المؤشرات الإحصائية للجهاز المركزي للإحصاء الفلسطيني يعرّف مؤشر البطالة" width="150" height="388" loading="lazy">'},
        {"title": "قُورن بين الدول", "gap": 16, "text": "تُوضع التعاريف الوطنية جنباً إلى جنب: السن، ومدة البحث، والإتاحة، والدورية، مع إشارة إلى ما لم يؤكده نص رسمي بعد.",
         "art": '<img src="static/img/table-unemployment.jpg" alt="جدول مقارنة تعريف البطالة في عشر دول: المسح والسن ومدة البحث والإتاحة والدورية" width="1044" height="760" loading="lazy">'},
        {"title": "نُشر بختمه", "gap": 64, "text": "يظهر النص على الورقة الذهبية مع رابط مصدره وفقرته واسم من تحقق منه.",
         "art": '<img src="static/img/sheet-ilo-47.jpg" alt="النص الرسمي للفقرة 47 من قرار المؤتمر التاسع عشر كما يظهر على الورقة الذهبية مع ختم التحقق" width="861" height="1157" loading="lazy">'},
    ]
    countries_home = []
    for iso in ARAB:
        card = cards[iso]
        c = unemp["countries"].get(iso, {})
        p = (profiles.get(iso, {}).get("profile") or {})
        survey = c.get("survey") or (p.get("lfs") or {}).get("name_ar", "")
        blurb_bits = [f"{card['nso']}."]
        if c.get("population_note"):
            blurb_bits.append(str(c["population_note"]))
        q = quotes.get(c.get("definition_quote")) or {}
        qsrc = reg.get(q.get("source"), {})
        excerpt = " ".join((q.get("text") or "").split())
        countries_home.append({"iso": iso, "name": card["name"], "nso": card["nso"], "verified": card["verified"], "survey": survey,
                               "frequency": FREQ_AR.get(c.get("frequency", ""), c.get("frequency", "")),
                               "age": c.get("age", ""), "def_state": status_state(q) or "—",
                               "excerpt": excerpt[:420] + ("…" if len(excerpt) > 420 else ""), "lang": q.get("lang", "ar"),
                               "src_title": qsrc.get("title_ar") or qsrc.get("title_en", ""), "src_url": q.get("quoted_from_url") or qsrc.get("url", "")})

    glossary = []
    for cat in ["labour", "statistical"]:
        items = []
        for c in cons:
            if c["category"] != cat:
                continue
            q = quotes.get(c["definition_quote"], {})
            prev = " ".join((q.get("text") or c["explanation_ai_ar"]).split())[:240] + "…"
            items.append({"id": c["id"], "name_ar": c["name_ar"], "en": c["names"]["en"], "preview": prev,
                          "variants": "، ".join(v["term"] for v in c.get("term_variants", []))})
        if items:
            glossary.append({"title": cat_ar[cat], "terms": items})
    ind_rows = []
    for i in inds:
        d, t = qref_count(i)
        ind_rows.append({"id": i["id"], "name_ar": i["name_ar"], "formula": i["international"].get("formula", ""), "done": d, "total": t,
                         "custodian": i["international"].get("custodian", ""), "sdg": "، ".join(i.get("sdg", []))})
    render("home.html", "index.html", title="مِعيار · المرجع العربي للإحصاء الرسمي", section="home", first_indicator=first,
           slips=slips, ruler_json=json.dumps(ruler, ensure_ascii=False), moments=moments, countries=countries_home,
           glossary=glossary, glossary_count=len(cons), indicators=ind_rows)

    # ---------------- search index ----------------
    idx = []
    for i in inds:
        idx.append({"t": i["name_ar"], "c": "مؤشر", "u": f"indicators/{i['id']}.html",
                    "k": " ".join([i["names"]["en"], i["names"]["fr"]] + [v["term"] for v in i.get("term_variants", [])] + i.get("sdg", []))})
    for c in cons:
        idx.append({"t": c["name_ar"], "c": "مفهوم", "u": f"concepts/{c['id']}.html",
                    "k": " ".join([c["names"]["en"], c["names"]["fr"]] + [v["term"] for v in c.get("term_variants", [])])})
    for iso, card in cards.items():
        idx.append({"t": card["name"], "c": "بلد · " + card["nso"], "u": f"countries/{iso}.html", "k": iso})
    (out / "search.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    n = len(list(out.rglob("*.html")))
    print(f"Built {n} pages into {out}")


if __name__ == "__main__":
    main()
