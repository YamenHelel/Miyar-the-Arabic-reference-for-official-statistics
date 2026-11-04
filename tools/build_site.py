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

import seo
from markdown_render import concept_md, datasource_md, indicator_md
from common import (CONTENT_DIR, ROOT, SOURCES_DIR, concept_files, datasource_files, indicator_files, iter_sources,
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
LFS_LABELS_EN = {"name_en": "Name", "name_fr": "Name", "frequency": "Frequency", "mode": "Collection mode", "coverage": "Coverage",
                 "sample": "Sample", "icls_standard": "Standard applied", "age": "Age", "history": "History", "universe": "Universe",
                 "framework": "Framework", "status_note": "Note", "standards_note": "Standards", "employed_definition_note": "Employed (definition)",
                 "classifications": "Classifications", "unemployed": "Unemployed (definition)", "unemployed_fr": "Unemployed (definition)",
                 "scope": "Scope", "coverage_note": "Coverage note"}
LFS_LABELS = {"name_en": "الاسم", "name_fr": "الاسم", "name_ar": "الاسم بالعربية", "frequency": "الدورية", "mode": "طريقة الجمع",
              "coverage": "التغطية", "sample": "العينة", "icls_standard": "المعيار المطبَّق", "age": "السن", "history": "التاريخ",
              "universe": "المجتمع", "framework": "الإطار", "status_note": "ملاحظة", "standards_note": "المعايير",
              "employed_definition_note": "تعريف المشتغل", "classifications": "التصنيفات", "unemployed": "تعريف المتعطل",
              "unemployed_fr": "تعريف المتعطل", "scope": "النطاق", "coverage_note": "ملاحظة التغطية"}


LIST_START = re.compile(r"^\s*(\([أ-ي]\)|\(\d+\)|\[|[a-d]\.\s|\(?[a-z]\)|\(?[ivx]+\)|\([a-z]\)|LU\d|\d+(\.\d+)*\.?\s|\d+\.\S|[•\-–]|[أ-ي]\.|\d+\s*\.|[a-zA-Z][a-zA-Z ]{0,24}$)")


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
    cfg = load_yaml(SITE / "config.yaml")
    base = cfg["base_url"]
    pages = []      # (path, lastmod) for sitemap.xml
    social = []     # social cards to render: {file, kind, title, sub}
    vq = sum(1 for q in quotes.values() if q.get("status") == "verified")
    stats = {"sources": len(reg), "verified_sources": sum(1 for r in reg.values() if r.get("status") == "verified"), "verified_quotes": vq}
    counts_line = " · ".join(f"{STATUS_AR[k]} {v}" for k, v in sorted(
        {s: sum(1 for r in reg.values() if r.get("status") == s) for s in STATUS_AR}.items(), key=lambda kv: -kv[1]) if v)

    env = Environment(loader=FileSystemLoader(SITE / "templates"), autoescape=select_autoescape(["html"]),
                      trim_blocks=True, lstrip_blocks=True)
    env.filters["tojson_ar"] = lambda v: json.dumps(v, ensure_ascii=False)
    env.filters["reflow"] = reflow

    def url_of(path):
        return base if path == "index.html" else base + (path[: -len("index.html")] if path.endswith("/index.html") else path)

    def render(tpl, path, lastmod=None, card=None, **ctx):
        depth = len(Path(path).parts) - 1
        root = base if path == "404.html" else "../" * depth   # 404 is served at any depth: absolute links
        f = out / path
        f.parent.mkdir(parents=True, exist_ok=True)
        ctx.setdefault("description", cfg["description_ar"])
        ctx["description"] = seo.clip(ctx["description"], 158)
        ctx.setdefault("jsonld", None)
        ctx.setdefault("crumbs", None)
        ctx.setdefault("md_alt", None)
        canonical = url_of(path)
        og = "static/social/site.png"
        if card:
            og = f"static/social/{card['file']}"
            social.append(card)
        title_plain = ctx.get("title", cfg["name_ar"]).split(" · ")[0]
        ctx.setdefault("cite", seo.citation(cfg, title_plain, ctx.get("title_en", cfg["name_en"]), canonical, built))
        ctx.update(cfg=cfg, canonical=canonical, og_image=base + og)
        pages.append((path if path.endswith(".html") else path, lastmod or built))
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

    # ---------------- code library (snippets per indicator) ----------------
    CODE_MAP = {"ind-unemployment-rate": ("lu1", "unemployed", "lf"), "ind-labour-force-participation-rate": ("lfpr", "lf", "wap"),
                "ind-employment-to-population-ratio": ("epr", "employed", "wap"), "ind-youth-unemployment-rate": ("yur", "youth_unemployed", "youth_lf")}

    def code_for(ind_id):
        if ind_id not in CODE_MAP:
            return None
        key, num, den = CODE_MAP[ind_id]
        py = (f"import sys; sys.path.insert(0, \"code/python\")\nfrom miyar_lfs import Params, derive, ratio, read_lfs\n\n"
              f"p = Params.for_country(\"jor\")          # قواعد الأردن من النص الرسمي\n"
              f"d = derive(read_lfs(\"lfs.csv\"), p)\nprint(ratio(d, \"{num}\", \"{den}\"))   # estimate, se, cv, ci95, deff")
        r = (f"source(\"code/r/miyar_lfs.R\")\nd <- derive(read.csv(\"lfs.csv\", comment.char = \"#\"), params_for(\"jor\"))\n"
             f"des <- svydesign(ids = ~psu, strata = ~stratum, weights = ~weight, data = d)\nsvyratio(~{num}, ~{den}, des)")
        st = (f"* بعد تشغيل code/stata/miyar_lfs.do لاشتقاق الحالة\nsvyset psu [pweight = weight], strata(stratum)\n"
              f"svy: ratio ({key}: {num}/{den})")
        return {"snippets": [
            {"key": "py", "name": "Python", "code": py, "file": "code/python/miyar_lfs.py", "status": "مُختبَرة"},
            {"key": "r", "name": "R", "code": r, "file": "code/r/miyar_lfs.R", "status": "تُشغَّل في CI وتطابق Python"},
            {"key": "st", "name": "Stata", "code": st, "file": "code/stata/miyar_lfs.do", "status": "لم تُشغَّل بعد"}]}

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
                             "tr_ar": reflow((q or {}).get("translation_ar")), "tr_en": reflow((q or {}).get("translation_en")),
                             "tr_official": (q or {}).get("translation_status") == "official",
                             "tr_note": (q or {}).get("translation_note_ar", ""),
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
        quick = seo.indicator_quick(i, quotes, reg)
        faq = seo.indicator_faq(i, quotes, reg)
        path = f"indicators/{i['id']}.html"
        term = {"@type": "DefinedTerm", "@id": base + path + "#term", "name": i["name_ar"],
                "alternateName": [i["names"]["en"], i["names"]["fr"]], "description": quick,
                "inDefinedTermSet": base + "indicators/", "url": base + path}
        art = {"@type": "Article", "headline": i["name_ar"], "inLanguage": "ar", "description": quick, "url": base + path,
               "dateModified": str(i.get("last_updated", built)), "license": cfg["license_url"], "publisher": seo.org(cfg),
               "about": {"@id": base + path + "#term"}, "isAccessibleForFree": True,
               "isBasedOn": [{"@type": "CreativeWork", "name": s["title"], "url": s["url"], "publisher": s["publisher"]} for s in sources]}
        ld = seo.graph(term, art, seo.breadcrumbs(cfg, [("مِعيار", ""), ("المؤشرات", "indicators/"), (i["name_ar"], None)]), seo.faq_ld(faq))
        render("indicator.html", path, title=f"{i['name_ar']} · مِعيار", title_en=i["names"]["en"], section="indicators", ind=i,
               done=done, total=total, rows=rows, national=national, notes=notes, sources=sources, components=components,
               variants=variants, others=[o for o in inds if o["id"] != i["id"]], quick=quick, faq=faq, jsonld=ld, code=code_for(i["id"]),
               crumbs=[("المؤشرات", "indicators/index.html"), (i["name_ar"], None)], md_alt=f"{i['id']}.md",
               lastmod=str(i.get("last_updated", built)),
               card={"file": f"{i['id']}.png", "kind": "مؤشر · إحصاءات العمل", "title": i["name_ar"], "sub": i["names"]["en"]},
               description=quick)
        (out / "indicators" / f"{i['id']}.md").write_text(indicator_md(i, quotes, reg, url=base + path), encoding="utf-8")
    tset = {"@type": "DefinedTermSet", "@id": base + "indicators/", "name": "مؤشرات إحصاءات العمل في مِعيار", "inLanguage": "ar",
            "hasDefinedTerm": [{"@id": base + f"indicators/{i['id']}.html#term", "name": i["name_ar"]} for i in inds]}
    render("index_list.html", "indicators/index.html", title="المؤشرات · مِعيار", section="indicators", heading="المؤشرات",
           title_en="Indicators", jsonld=seo.graph(tset, seo.breadcrumbs(cfg, [("مِعيار", ""), ("المؤشرات", None)])),
           crumbs=[("المؤشرات", None)], description="مؤشرات إحصاءات العمل في مِعيار: معدل البطالة، معدل المشاركة، نسبة العمالة إلى السكان، بطالة الشباب، بتعاريفها الرسمية في عشر دول.",
           intro="أربعة مؤشرات تجريبية في إحصاءات العمل. كل بطاقة تجمع النص الدولي والتعاريف الوطنية وملاحظات المقارنة.",
           groups=[{"title": "", "rows": [{"href": f"indicators/{i['id']}.html", "name": i["name_ar"],
                     "meta": "النصوص الرسمية {} من {}".format(*qref_count(i)), "sub": i["names"]["en"]} for i in inds]}])

    # ---------------- concepts ----------------
    cat_ar = {"labour": "مفاهيم العمل", "statistical": "مفاهيم إحصائية", "survey": "المسوح", "classification": "التصنيفات",
              "descriptive": "الإحصاء الوصفي", "sampling": "المعاينة والمسوح", "estimation": "التقدير والجودة",
              "rates": "المعدلات والنسب والأرقام القياسية"}
    SECTIONS = ["labour", "descriptive", "sampling", "estimation", "rates"]
    STAT_ORDER = ["con-mean", "con-weighted-mean", "con-median", "con-mode", "con-range", "con-variance", "con-standard-deviation",
                  "con-coefficient-of-variation", "con-percentile", "con-interquartile-range", "con-outlier",
                  "con-population", "con-sample", "con-sampling-frame", "con-simple-random-sampling", "con-stratified-sampling",
                  "con-cluster-sampling", "con-sampling-weight", "con-non-response", "con-response-rate",
                  "con-estimate", "con-sampling-error", "con-non-sampling-error", "con-standard-error", "con-confidence-interval",
                  "con-margin-of-error", "con-design-effect", "con-bias",
                  "con-rate", "con-ratio", "con-percentage-point", "con-index-number", "con-seasonal-adjustment"]

    def section_of(c):
        return "labour" if c["category"] == "labour" else c.get("group", "estimation")
    cons.sort(key=lambda c: (SECTIONS.index(section_of(c)), STAT_ORDER.index(c["id"]) if c["id"] in STAT_ORDER else 0, c["id"]))
    for c in cons:
        related = []
        for r in c.get("related", []):
            if r in con_by:
                related.append({"href": f"concepts/{r}.html", "name": con_by[r]["name_ar"]})
            elif r in ind_by:
                related.append({"href": f"indicators/{r}.html", "name": ind_by[r]["name_ar"]})
        vl = [{"term": v["term"], "where": "، ".join(COUNTRIES.get(x, x) for x in v.get("used_in", [])) or "الاستعمال قيد التحقق",
               "basis": v.get("basis", "")} for v in c.get("term_variants", [])]
        cq = seo.concept_quick(c, quotes, reg)
        cpath = f"concepts/{c['id']}.html"
        cterm = {"@type": "DefinedTerm", "@id": base + cpath + "#term", "name": c["name_ar"], "alternateName": [c["names"]["en"], c["names"]["fr"]],
                 "description": cq, "inDefinedTermSet": base + "concepts/", "url": base + cpath}
        render("concept.html", cpath, title=f"{c['name_ar']} · مِعيار", title_en=c["names"]["en"], section="concepts", con=c,
               quick=cq, description=cq, jsonld=seo.graph(cterm, seo.breadcrumbs(cfg, [("مِعيار", ""), ("المفاهيم", "concepts/"), (c["name_ar"], None)])),
               crumbs=[("المفاهيم", "concepts/index.html"), (c["name_ar"], None)], md_alt=f"{c['id']}.md", lastmod=str(c.get("last_updated", built)),
               card={"file": f"{c['id']}.png", "kind": "مفهوم · مسرد مِعيار", "title": c["name_ar"], "sub": c["names"]["en"]},
               cat=cat_ar.get(section_of(c), c["category"]), related=related, variants_list=vl,
               variants="، ".join(v["term"] for v in c.get("term_variants", [])))
        (out / "concepts" / f"{c['id']}.md").write_text(concept_md(c, quotes, reg, url=base + cpath), encoding="utf-8")
    groups = []
    for cat in SECTIONS:
        rows = [{"href": f"concepts/{c['id']}.html", "name": c["name_ar"], "meta": c["names"]["en"],
                 "sub": status_state(quotes.get(c["definition_quote"]))} for c in cons if section_of(c) == cat]
        if rows:
            groups.append({"title": cat_ar[cat], "rows": rows})
    cset = {"@type": "DefinedTermSet", "@id": base + "concepts/", "name": "مسرد مِعيار لمفاهيم إحصاءات العمل والإحصاء", "inLanguage": "ar",
            "hasDefinedTerm": [{"@id": base + f"concepts/{c['id']}.html#term", "name": c["name_ar"]} for c in cons]}
    render("index_list.html", "concepts/index.html", title="المفاهيم · مِعيار", section="concepts", heading="المفاهيم", title_en="Glossary",
           jsonld=seo.graph(cset, seo.breadcrumbs(cfg, [("مِعيار", ""), ("المفاهيم", None)])), crumbs=[("المفاهيم", None)],
           description="مسرد مِعيار: مفاهيم إحصاءات العمل والمفاهيم الإحصائية بالعربية، مع مقابلها الدولي وتعريفها الرسمي ومتغيرات المصطلح بين الدول.",
           intro="المسرد: المصطلح العربي ومتغيراته بين الدول، ومقابله في المعيار الدولي، وتعريفه الرسمي.", groups=groups)

    # ---------------- countries ----------------
    unemp = ind_by.get("ind-unemployment-rate", {"countries": {}})
    cards = {}
    for iso in ARAB + REFC:
        prof = profiles.get(iso, {})
        p = prof.get("profile", {})
        nso = p.get("nso", {})
        recs = [r for r in prof.get("sources", [])]
        def rows(view):
            labels = LFS_LABELS if view == "ar" else LFS_LABELS_EN
            alt = (p.get("lfs_ar") if view == "ar" else p.get("lfs_en")) or {}
            sep = "، " if view == "ar" else ", "
            out_rows = []
            for k, v in (p.get("lfs") or {}).items():
                if k not in labels or (view == "en" and k == "name_ar"):
                    continue
                v = alt.get(k, v)
                if isinstance(v, list):
                    v = sep.join(map(str, v))
                if isinstance(v, (str, int)) and str(v) not in {str(r[1]) for r in out_rows}:
                    out_rows.append((labels[k], v))
            return out_rows
        lfs = rows("ar")
        lfs_en = rows("en")
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
                "lfs_en": lfs_en, "notes_ar": " ".join(str(p.get("notes_ar", "") or "").split()),
                "nso_ar": nso.get("name_ar") or p.get("nso_ar", ""), "nso_en": nso.get("name_en") or p.get("nso_en", ""),
                "rendered": bool(p.get("translation_by")),
                "sources": [{"url": str(r.get("url", "")), "title": r.get("title_ar") or r.get("title_en", ""),
                             "type": TYPE_AR.get(r.get("type"), r.get("type")), "status": r["status"], "status_ar": STATUS_AR[r["status"]]} for r in recs]}
        cards[iso] = card
    for iso, card in cards.items():
        nso_ld = {"@type": "GovernmentOrganization", "name": card["nso"], **({"url": card["nso_url"]} if card["nso_url"] else {})}
        page_ld = {"@type": "WebPage", "name": f"{card['name']}: إحصاءات العمل", "inLanguage": "ar", "url": base + f"countries/{iso}.html", "about": nso_ld}
        render("country.html", f"countries/{iso}.html", title=f"{card['name']} · مِعيار", title_en=iso.upper(), section="countries", c=card,
               others=[cards[o] for o in ARAB + REFC if o != iso],
               description=f"{card['name']}: {card['nso']}، مسح القوى العاملة، تعاريف البطالة والعمالة كما يعتمدها، والمصادر الرسمية والبيانات الجزئية.",
               jsonld=seo.graph(page_ld, seo.breadcrumbs(cfg, [("مِعيار", ""), ("الدول", "countries/"), (card["name"], None)])),
               crumbs=[("الدول", "countries/index.html"), (card["name"], None)])
    render("index_list.html", "countries/index.html", title="الدول · مِعيار", section="countries", heading="الدول", title_en="Countries",
           crumbs=[("الدول", None)], description="الدول في مِعيار: تونس والسعودية والمغرب والأردن والإمارات وفلسطين، مع الولايات المتحدة والمملكة المتحدة وأستراليا وفرنسا للمقارنة.",
           intro="ست دول عربية في المرحلة الأولى، وأربع دول مرجعية للمقارنة. تُضاف الدول تباعاً.",
           groups=[{"title": "الدول العربية", "rows": [{"href": f"countries/{i}.html", "name": cards[i]["name"], "meta": f"{cards[i]['verified']} مصدراً مُتحقَّقاً منه", "sub": cards[i]["nso"]} for i in ARAB]},
                   {"title": "دول مرجعية", "rows": [{"href": f"countries/{i}.html", "name": cards[i]["name"], "meta": f"{cards[i]['verified']} مصدراً مُتحقَّقاً منه", "sub": cards[i]["nso"]} for i in REFC]}])

    # ---------------- data sources (types + LFS guide) ----------------
    TOPICS = {"unemployment": "البطالة بالمفهوم الدولي", "participation": "المشاركة ونسبة العمالة إلى السكان",
              "structure": "التشغيل حسب النشاط والمهنة والحالة", "informality": "العمالة غير المنظمة",
              "hours": "ساعات العمل ونقص التشغيل", "earnings": "الأجور وتكلفة العمل",
              "small_area": "المناطق الصغيرة", "timeliness": "الدورية وسرعة النشر"}
    LEVEL_AR = {"main": "رئيسي", "partial": "جزئي", "none": "لا"}
    dss = [load_yaml(p) for p in datasource_files()]
    ds_by = {d["id"]: d for d in dss}
    ds_types = sorted((d for d in dss if d["kind"] == "type"), key=lambda d: d["order"])
    ds_guide = sorted((d for d in dss if d["kind"] == "guide"), key=lambda d: d["order"])

    def ds_count(d):
        slots = [oq["slot"] for oq in d.get("official_quotes", [])]
        return sum(1 for s_ in slots if (quotes.get(s_) or {}).get("status") in ("verified", "pasted")), len(slots)

    def ds_state(d):
        dn, tt = ds_count(d)
        return f"النصوص الرسمية {dn} من {tt}"

    def rel_link(r):
        if r in con_by:
            return {"href": f"concepts/{r}.html", "name": con_by[r]["name_ar"]}
        if r in ind_by:
            return {"href": f"indicators/{r}.html", "name": ind_by[r]["name_ar"]}
        if r in ds_by:
            return {"href": f"data-sources/{r}.html", "name": ds_by[r]["name_ar"]}
        return None

    def reading_of(d):
        outl = []
        for sid in d.get("further_reading", []) or []:
            r = reg.get(sid)
            if r:
                outl.append({"url": r["url"] if str(r.get("url", "")).startswith("http") else "", "title": r.get("title_ar") or r["title_en"],
                             "status": r["status"], "status_ar": STATUS_AR[r["status"]], "publisher": r.get("publisher", "")})
        return outl

    lfs_rows = []
    for iso in ARAB + REFC:
        lf = ((profiles.get(iso, {}).get("profile") or {}).get("lfs") or {})
        lfs_rows.append({"iso": iso, "name": COUNTRIES[iso], "survey": lf.get("name_ar") or lf.get("name_fr") or lf.get("name_en") or "—",
                         "frequency": FREQ_AR.get(str(lf.get("frequency", "")), lf.get("frequency") or "—"),
                         "standard": {"19th": "المؤتمر 19", "13th": "المؤتمر 13", "mixed": "مختلط", "unknown": "غير مؤكَّد"}.get(
                             str(lf.get("icls_standard", "")), "انظر صفحة البلد")})
    for d in dss:
        dn, tt = ds_count(d)
        dpath = f"data-sources/{d['id']}.html"
        parent = ds_by.get(d.get("parent")) if d["kind"] == "guide" else None
        produces = [{"topic": TOPICS[p_["topic"]], "level": p_["level"], "level_ar": LEVEL_AR[p_["level"]], "note": p_["note_ai_ar"]}
                    for p_ in d.get("produces", []) or []]
        guide_rows = [{"id": g["id"], "order": g["order"], "name_ar": g["name_ar"], "en": g["names"]["en"], "state": ds_state(g)}
                      for g in ds_guide] if d["id"] == "ds-labour-force-survey" else []
        dq = seo.clip(" ".join(str(d["summary_ai_ar"]).split()), 300)
        crumbs = [("مصادر البيانات", "data-sources/index.html")]
        if parent:
            crumbs.append((parent["name_ar"], f"data-sources/{parent['id']}.html"))
        crumbs.append((d["name_ar"], None))
        bc = [("مِعيار", ""), ("مصادر البيانات", "data-sources/")] + ([(parent["name_ar"], f"data-sources/{parent['id']}.html")] if parent else []) + [(d["name_ar"], None)]
        art = {"@type": "Article", "headline": d["name_ar"], "alternativeHeadline": d["names"]["en"], "inLanguage": "ar", "url": base + dpath,
               "description": dq, "dateModified": str(d.get("last_updated", built)), "license": cfg["license_url"], "publisher": seo.org(cfg),
               "isAccessibleForFree": True, "isBasedOn": [{"@type": "CreativeWork", "name": r["title"], "url": r["url"], "publisher": r["publisher"]}
                                                          for r in reading_of(d) if r["url"]]}
        render("datasource.html", dpath, title=f"{d['name_ar']} · مِعيار", title_en=d["names"]["en"], section="data-sources", ds=d,
               done=dn, total=tt, produces=produces, guide=guide_rows, guide_total=len(ds_guide),
               lfs_rows=lfs_rows if d.get("country_table") else [], reading=reading_of(d), parent=parent,
               siblings=[{"id": g["id"], "order": g["order"], "name_ar": g["name_ar"]} for g in ds_guide] if parent else [],
               related=[x for x in (rel_link(r) for r in d.get("related", []) or []) if x and not (parent and x["href"].startswith("data-sources/ds-lfs-"))],
               description=dq, jsonld=seo.graph(art, seo.breadcrumbs(cfg, bc)), crumbs=crumbs, md_alt=f"{d['id']}.md",
               lastmod=str(d.get("last_updated", built)),
               card={"file": f"{d['id']}.png", "kind": "مصادر البيانات" + (" · دليل مسح القوى العاملة" if parent else ""), "title": d["name_ar"], "sub": d["names"]["en"]})
        (out / "data-sources" / f"{d['id']}.md").write_text(datasource_md(d, quotes, reg, url=base + dpath), encoding="utf-8")
    matrix = [{"topic": TOPICS[k], "cells": [next(({"level": p_["level"], "level_ar": LEVEL_AR[p_["level"]], "note": p_["note_ai_ar"]}
                                                    for p_ in t.get("produces", []) if p_["topic"] == k), {"level": "none", "level_ar": "—", "note": ""})
                                              for t in ds_types]} for k in TOPICS]
    ds_quick = ("لإحصاءات العمل أربعة مصادر رئيسية: مسح القوى العاملة، والتعداد العام للسكان، والسجلات الإدارية، ومسوح المؤسسات. "
                "مسح القوى العاملة هو المصدر الرئيسي للبطالة والمشاركة وفق معايير منظمة العمل الدولية، والمصادر الأخرى تكمّله: "
                "التعداد للمناطق الصغيرة وإطار المعاينة، والسجلات للبيانات الشهرية عن العمل المسجَّل، ومسوح المؤسسات للأجور والوظائف.")
    dset = {"@type": "CollectionPage", "name": "مصادر بيانات إحصاءات العمل", "inLanguage": "ar", "url": base + "data-sources/", "description": ds_quick,
            "hasPart": [{"@type": "Article", "name": d["name_ar"], "url": base + f"data-sources/{d['id']}.html"} for d in ds_types + ds_guide]}
    render("datasources_index.html", "data-sources/index.html", title="مصادر البيانات · مِعيار", title_en="Data sources", section="data-sources",
           quick=ds_quick, description=ds_quick, crumbs=[("مصادر البيانات", None)],
           jsonld=seo.graph(dset, seo.breadcrumbs(cfg, [("مِعيار", ""), ("مصادر البيانات", None)])),
           types=[{"id": t["id"], "name_ar": t["name_ar"], "en": t["names"]["en"], "state": ds_state(t)} for t in ds_types],
           guide=[{"id": g["id"], "order": g["order"], "name_ar": g["name_ar"], "en": g["names"]["en"], "state": ds_state(g)} for g in ds_guide],
           matrix=matrix, card={"file": "data-sources.png", "kind": "مِعيار", "title": "مصادر البيانات", "sub": "LFS · census · registers · establishments"})

    # ---------------- sources registry ----------------
    rows = []
    for _, r in iter_sources():
        rows.append({"url": str(r.get("url", "")), "title": r.get("title_ar") or r.get("title_en", ""), "publisher": r.get("publisher", ""),
                     "country": COUNTRIES.get(r.get("country", "int"), r.get("country", "")), "type": TYPE_AR.get(r.get("type"), r.get("type")),
                     "status": r["status"], "status_ar": STATUS_AR[r["status"]], "vdate": str(r.get("verified_date", "") or ""),
                     "scope": "int" if r.get("country") in (None, "int") else "country"})
    rows.sort(key=lambda x: (["verified", "link-ok", "collected", "to-locate", "broken", "superseded"].index(x["status"]), x["title"]))
    ds = {"@type": "Dataset", "name": "سجل مراجع مِعيار", "alternateName": "Miʿyar source registry", "inLanguage": "ar",
          "description": "قائمة الوثائق الرسمية التي يستند إليها مِعيار (معايير منظمة العمل الدولية، منهجيات الأجهزة الإحصائية) مع حالة التحقق من كل منها.",
          "license": cfg["license_url"], "creator": seo.org(cfg), "url": base + "sources/", "isAccessibleForFree": True,
          "distribution": {"@type": "DataDownload", "encodingFormat": "application/x-yaml", "contentUrl": cfg["github"] + "/tree/main/sources"}}
    render("sources.html", "sources/index.html", title="سجل المراجع · مِعيار", section="sources", rows=rows, counts=counts_line, title_en="Source registry",
           jsonld=seo.graph(ds, seo.breadcrumbs(cfg, [("مِعيار", ""), ("المراجع", None)])), crumbs=[("المراجع", None)],
           description="سجل مراجع مِعيار: كل وثيقة رسمية يستند إليها المرجع، بحالة التحقق منها وتاريخه، من منظمة العمل الدولية والأجهزة الإحصائية في عشر دول.",
           filters=[(k, v) for k, v in STATUS_AR.items()] + [("int", "دولية"), ("country", "وطنية")])

    presets = json.loads((ROOT / "code" / "presets" / "countries.json").read_text(encoding="utf-8"))
    prow = []
    for iso, c in presets.items():
        if iso.startswith("_"):
            continue
        prow.append({"name": "المعيار الدولي (ILO)" if iso == "ilo" else COUNTRIES.get(iso, iso), "age_min": c.get("age_min"),
                     "search_days": c.get("search_days"), "availability_days": c.get("availability_days"),
                     "state": status_state(quotes.get(c.get("quote"))) or "",
                     "href": "indicators/ind-unemployment-rate.html" + ("#intl" if iso == "ilo" else f"#nat-{iso}")})
    variables = [("stratum, psu, weight", "تصميم العينة: الطبقة، الوحدة الأولية، الوزن النهائي"), ("age, sex, nationality", "العمر والجنس والجنسية"),
                 ("in_education, in_training", "1 إذا كان في التعليم النظامي / التدريب"), ("worked_1h", "1 إذا عمل ساعة على الأقل مقابل أجر أو ربح في أسبوع الإسناد"),
                 ("temp_absent", "1 إذا كان له عمل وغاب عنه مؤقتاً"), ("searched_days", "عدد الأيام منذ آخر خطوة بحث فعلي عن عمل (فارغ إن لم يبحث)"),
                 ("available_days", "يستطيع بدء العمل خلال N يوماً بعد أسبوع الإسناد (0 = خلاله؛ فارغ إن لم يكن متاحاً)"),
                 ("future_starter", "1 إذا وجد عملاً يبدأ لاحقاً"), ("wants_work", "1 إذا كان يرغب في العمل"),
                 ("hours_usual, wants_more_hours, available_more_hours", "للحساب نقص التشغيل المرتبط بالوقت")]
    code_quick = ("مكتبة شيفرة مفتوحة (MIT) تحسب مؤشرات سوق العمل من البيانات الجزئية لمسح القوى العاملة وفق قرار المؤتمر الدولي التاسع عشر "
                  "لخبراء إحصاءات العمل، مع الأوزان والخطأ المعياري ومجال الثقة، بلغات Python وR وStata، وبقواعد كل بلد مأخوذة من نصوصه الرسمية.")
    soft = {"@type": "SoftwareSourceCode", "name": "Miʿyar code library", "description": code_quick, "codeRepository": cfg["github"] + "/tree/main/code",
            "programmingLanguage": ["Python", "R", "Stata"], "license": "https://opensource.org/licenses/MIT", "inLanguage": "ar"}
    render("code.html", "code/index.html", title="مكتبة الشيفرة · مِعيار", title_en="Code library", section="code", quick=code_quick,
           description=code_quick, presets=prow, variables=variables,
           ind_names=["معدل المشاركة في القوة العاملة", "نسبة العمالة إلى السكان", "معدل البطالة (LU1)", "LU2: نقص التشغيل المرتبط بالوقت والبطالة",
                      "LU3: البطالة والقوة العاملة المحتملة", "LU4: المقياس المركب لنقص استخدام العمالة", "معدل البطالة بين الشباب",
                      "نسبة الشباب خارج التعليم والعمل والتدريب (NEET)"],
           files=[{"lang": "Python", "path": "code/python/miyar_lfs.py", "status": "مُختبَرة (tools/test_code.py)"},
                  {"lang": "R", "path": "code/r/miyar_lfs.R", "status": "تُشغَّل في CI وتطابق Python في 32 نتيجة"},
                  {"lang": "Stata", "path": "code/stata/miyar_lfs.do", "status": "لم تُشغَّل بعد؛ كُتبت لتطابق النسختين"},
                  {"lang": "بيانات", "path": "code/data/synthetic_lfs.csv", "status": "بيانات مصطنعة للاختبار"}],
           jsonld=seo.graph(soft, seo.breadcrumbs(cfg, [("مِعيار", ""), ("الشيفرة", None)])), crumbs=[("الشيفرة", None)])
    render("about.html", "about/index.html", title="المنهجية · مِعيار", section="about", counts=counts_line, title_en="Methodology",
           crumbs=[("المنهجية", None)], jsonld=seo.graph(seo.breadcrumbs(cfg, [("مِعيار", ""), ("المنهجية", None)])),
           description="كيف يعمل مِعيار: النص الرسمي منسوخ حرفياً مع مصدره، والتعليق منفصل، وشرح الذكاء الاصطناعي موسوم؛ مراحل التحقق من المصادر وطريقة الاستشهاد.")

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
        {"title": "وُجد المصدر", "gap": 24, "text": "يُسجَّل كل رابط يُعثر عليه في سجل المراجع بحالة «قيد التحقق»، ولا يُبنى عليه شيء بعد.",
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
    for cat in SECTIONS:
        items = []
        for c in cons:
            if section_of(c) != cat:
                continue
            q = quotes.get(c["definition_quote"], {})
            prev = " ".join((q.get("text") or c["explanation_ai_ar"]).split())[:240] + "…"
            items.append({"id": c["id"], "name_ar": c["name_ar"], "en": c["names"]["en"], "preview": prev,
                          "variants": "، ".join(v["term"] for v in c.get("term_variants", []))})
        if items:
            glossary.append({"title": cat_ar[cat], "terms": items[:6], "more": max(0, len(items) - 6)})
    ind_rows = []
    for i in inds:
        d, t = qref_count(i)
        ind_rows.append({"id": i["id"], "name_ar": i["name_ar"], "formula": i["international"].get("formula", ""), "done": d, "total": t,
                         "custodian": i["international"].get("custodian", ""), "sdg": "، ".join(i.get("sdg", []))})
    site_ld = {"@type": "WebSite", "@id": base + "#website", "name": cfg["name_en"], "alternateName": [cfg["name_ar"], cfg["tagline_ar"]],
               "url": base, "inLanguage": "ar", "description": cfg["description_ar"], "license": cfg["license_url"], "publisher": seo.org(cfg)}
    render("home.html", "index.html", title="مِعيار · المرجع العربي للإحصاء الرسمي", section="home", first_indicator=first,
           title_en=cfg["name_en"], jsonld=seo.graph(site_ld, seo.org(cfg)), description=cfg["description_ar"],
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
    for d in dss:
        idx.append({"t": d["name_ar"], "c": "مصدر بيانات" if d["kind"] == "type" else "دليل مسح القوى العاملة", "u": f"data-sources/{d['id']}.html",
                    "k": " ".join([d["names"]["en"], d["names"]["fr"], "LFS census register survey مصدر بيانات"])})
    idx.append({"t": "مكتبة الشيفرة: Python وR وStata", "c": "أداة", "u": "code/index.html",
                "k": "code python r stata survey standard error microdata شيفرة برمجة بيانات جزئية"})
    for iso, card in cards.items():
        idx.append({"t": card["name"], "c": "بلد · " + card["nso"], "u": f"countries/{iso}.html", "k": iso})
    (out / "search.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    # ---------------- 404, root files, social cards list ----------------
    render("404.html", "404.html", title="الصفحة غير موجودة · مِعيار", section="", description="الصفحة غير موجودة في مِعيار، المرجع العربي للإحصاء الرسمي. ابحث عن مؤشر أو مفهوم أو ابدأ من الصفحة الرئيسية.")
    pages[:] = [(pth, d) for pth, d in pages if pth != "404.html"]
    (out / "robots.txt").write_text(seo.robots_txt(cfg), encoding="utf-8")
    (out / "sitemap.xml").write_text(seo.sitemap_xml(cfg, pages), encoding="utf-8")
    llms = seo.llms_txt(cfg, inds, cons, [(i, COUNTRIES[i]) for i in ARAB + REFC], dss)
    (out / "llms.txt").write_text(llms, encoding="utf-8")
    full = [llms, "\n---\n"]
    full += [indicator_md(i, quotes, reg, url=base + f"indicators/{i['id']}.html") + "\n---\n" for i in inds]
    full += [concept_md(c, quotes, reg, url=base + f"concepts/{c['id']}.html") + "\n---\n" for c in cons]
    full += [datasource_md(d, quotes, reg, url=base + f"data-sources/{d['id']}.html") + "\n---\n" for d in ds_types + ds_guide]
    (out / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")
    manifest = {"name": f"{cfg['name_ar']} · {cfg['tagline_ar']}", "short_name": cfg["name_ar"], "lang": "ar", "dir": "rtl",
                "start_url": "./", "display": "browser", "background_color": cfg["theme_color"], "theme_color": cfg["theme_color"],
                "icons": [{"src": "static/favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}
    (out / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    (out / "static" / "social").mkdir(parents=True, exist_ok=True)
    social.insert(0, {"file": "site.png", "kind": cfg["tagline_ar"], "title": cfg["name_ar"], "sub": cfg["tagline_en"]})
    (out / "static" / "social" / "cards.json").write_text(json.dumps(social, ensure_ascii=False), encoding="utf-8")
    n = len(list(out.rglob("*.html")))
    print(f"Built {n} pages into {out}")


if __name__ == "__main__":
    main()
