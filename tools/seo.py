"""SEO and GEO builders for the Miʿyar site (PRD 16, ADR-0009).

Everything here is generated from verified data: quick answers and FAQ items use only facts whose basis is a quotation,
and every answer carries its source. No free-form AI text is produced here.
"""
import json
import re

AI_BOTS = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "anthropic-ai",
           "PerplexityBot", "Perplexity-User", "Google-Extended", "Applebot-Extended", "CCBot", "Meta-ExternalAgent",
           "Bytespider", "DuckAssistBot", "cohere-ai", "MistralAI-User"]
COUNTRIES = {"tun": "تونس", "sau": "السعودية", "mar": "المغرب", "jor": "الأردن", "are": "الإمارات", "pse": "فلسطين",
             "usa": "الولايات المتحدة", "gbr": "المملكة المتحدة", "aus": "أستراليا", "fra": "فرنسا"}


def para_of(locator):
    """'… paragraph 47 …' or '§47' -> '47' (for writing the standard's paragraph in full)."""
    m = re.search(r"(?:paragraph|§)\s*(\d+)", locator or "")
    return m.group(1) if m else None


def clip(s, n):
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def org(cfg):
    return {"@type": "Organization", "name": cfg["name_en"], "alternateName": cfg["name_ar"], "url": cfg["base_url"],
            "email": cfg["email"], "sameAs": [cfg["github"]], "logo": cfg["base_url"] + "static/favicon.svg"}


def breadcrumbs(cfg, items):
    """items: [(name, path or None)] — path relative to base_url."""
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": n, **({"item": cfg["base_url"] + p} if p is not None else {})}
        for k, (n, p) in enumerate(items)]}


def graph(*nodes):
    return json.dumps({"@context": "https://schema.org", "@graph": [n for n in nodes if n]}, ensure_ascii=False, indent=1)


# ---------------- quick answers (deterministic, from verified data) ----------------
def indicator_quick(i, quotes, reg):
    intl = i["international"]
    q = quotes.get(intl.get("definition_quote")) or {}
    src = reg.get(q.get("source") or intl.get("standard_source"), {})
    p = para_of(q.get("locator"))
    std = src.get("title_ar") or src.get("title_en", "")
    parts = [f"{i['name_ar']} ({i['names']['en']}) مؤشر في إحصاءات العمل يُحسب كما يلي: {intl.get('formula_ar', '')}."]
    ref = f"يستند تعريفه الدولي إلى {std}" + (f"، الفقرة {p}" if p else "")
    ref += f"، والجهة الراعية له {'منظمة العمل الدولية (ILO)' if intl.get('custodian') == 'ILO' else intl.get('custodian', '')}"
    if i.get("sdg"):
        ref += f"، وهو مؤشر هدف التنمية المستدامة {'، '.join(i['sdg'])}"
    parts.append(ref + ".")
    nat = sum(1 for c in i["countries"].values() if (quotes.get(c.get("definition_quote")) or {}).get("status") in ("verified", "pasted"))
    parts.append(f"يعرض مِعيار التعريف الدولي حرفياً، ويقارن تطبيقه في عشر دول، منها {nat} بنصوصها الرسمية المنسوخة.")
    return " ".join(parts)


def concept_quick(c, quotes, reg):
    q = quotes.get(c.get("definition_quote")) or {}
    src = reg.get(q.get("source") or c.get("source"), {})
    p = para_of(q.get("locator"))
    std = src.get("title_ar") or src.get("title_en", "")
    s = f"{c['name_ar']} ({c['names']['en']}، {c['names']['fr']}) مفهوم يعرّفه {std}" + (f" في الفقرة {p}" if p else "") + "."
    if q.get("status") in ("verified", "pasted"):
        s += " النص الرسمي منسوخ أدناه حرفياً بلغته الأصلية مع مصدره."
    else:
        s += " النص الرسمي بانتظار النسخ من مصدره."
    return s


# ---------------- FAQ (only quote-backed facts) ----------------
def indicator_faq(i, quotes, reg):
    items = []
    intl = i["international"]
    std = reg.get(intl.get("standard_source"), {})
    items.append((f"كيف يُحسب {i['name_ar']}؟",
                  f"{intl.get('formula_ar', '')} ({intl.get('formula', '')}). المرجع: {std.get('title_ar') or std.get('title_en', '')}."))
    for iso, c in i["countries"].items():
        if not str(c.get("facts_basis", "")).startswith("quote"):
            continue
        q = quotes.get(c.get("definition_quote")) or {}
        if q.get("status") not in ("verified", "pasted"):
            continue
        src = reg.get(q.get("source"), {})
        bits = []
        m = c.get("measures") or {}
        if m.get("age_min"):                      # quote-backed number only (snippet ages are excluded)
            bits.append(f"السن {m['age_min']} سنة فأكثر")
        if c.get("job_search_period"):
            bits.append(f"البحث عن عمل: {c['job_search_period']}")
        if c.get("availability"):
            bits.append(f"الإتاحة للعمل: {c['availability']}")
        if not bits:
            continue
        name = COUNTRIES.get(iso, iso)
        items.append((f"كيف تعرّف {name} المتعطل في مسح القوى العاملة؟",
                      "، ".join(bits) + f". المصدر: {src.get('title_ar') or src.get('title_en', '')}."))
    return items


def faq_ld(items):
    if not items:
        return None
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": qn, "acceptedAnswer": {"@type": "Answer", "text": a}}
                                               for qn, a in items]}


# ---------------- citations ----------------
def citation(cfg, title_ar, title_en, url, date):
    return {"ar": f"مِعيار، «{title_ar}»، {url}، تاريخ الاطلاع: {date}. ترخيص CC BY 4.0.",
            "en": f"Miʿyar, \"{title_en}\", {url}, accessed {date}. CC BY 4.0."}


# ---------------- root files ----------------
def robots_txt(cfg):
    lines = ["# Miʿyar — all crawlers welcome, AI crawlers included (ADR-0009). Content: CC BY 4.0, please cite.", "",
             "User-agent: *", "Allow: /", ""]
    for b in AI_BOTS:
        lines += [f"User-agent: {b}", "Allow: /", ""]
    lines += [f"Sitemap: {cfg['base_url']}sitemap.xml", ""]
    return "\n".join(lines)


def sitemap_xml(cfg, pages):
    """pages: [(path, lastmod)]"""
    rows = "".join(f"  <url><loc>{cfg['base_url']}{'' if p == 'index.html' else p}</loc><lastmod>{d}</lastmod></url>\n" for p, d in pages)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + rows + "</urlset>\n")


def llms_txt(cfg, inds, cons, countries):
    out = [f"# {cfg['name_en']} ({cfg['name_ar']}) — {cfg['tagline_en']}", "",
           f"> {cfg['description_en']}", "",
           "Miʿyar quotes official definitions verbatim in their original language (Arabic, French or English), always with the source "
           "document, paragraph and verification date. AI-assisted explanations are labelled. Content licence CC BY 4.0: cite as "
           f"\"Miʿyar, <page title>, <URL>, accessed <date>\". Contact: {cfg['email']}.", "",
           "## Indicators (labour statistics)"]
    out += [f"- [{i['names']['en']} — {i['name_ar']}]({cfg['base_url']}indicators/{i['id']}.md): international definition, formula, "
            f"definitions in 10 countries" for i in inds]
    out += ["", "## Concepts (glossary)"]
    out += [f"- [{c['names']['en']} — {c['name_ar']}]({cfg['base_url']}concepts/{c['id']}.md)" for c in cons]
    out += ["", "## Countries"]
    out += [f"- [{name}]({cfg['base_url']}countries/{iso}.html)" for iso, name in countries]
    out += ["", "## Optional", f"- [All verified content in one file]({cfg['base_url']}llms-full.txt)",
            f"- [Source registry]({cfg['base_url']}sources/index.html)", f"- [Methodology]({cfg['base_url']}about/index.html)",
            f"- [Source code and data]({cfg['github']})", ""]
    return "\n".join(out)
