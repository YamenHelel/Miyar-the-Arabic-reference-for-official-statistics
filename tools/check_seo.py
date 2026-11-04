#!/usr/bin/env python3
"""SEO/GEO gate for the built site (PRD 16). Fails (exit 1) on errors; prints warnings.

Usage:
  python tools/check_seo.py [_site] [--skip-images]     (--skip-images: social cards not rendered, e.g. push-time CI)

Checks every HTML page: title (unique, ≤ 65 chars), meta description (unique, 50–160 chars), canonical under base_url,
Open Graph image present on disk, JSON-LD parses, exactly one <h1>, images have alt, internal links resolve.
Checks the site: sitemap URLs exist, robots.txt allows AI crawlers and points to the sitemap, llms.txt links resolve.
"""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse

from common import ROOT, load_yaml

SITE_CFG = load_yaml(Path(__file__).resolve().parent / "site" / "config.yaml")
BASE = SITE_CFG["base_url"]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.in_title, self.meta, self.links, self.h1, self.imgs, self.ld, self._ld = "", False, {}, [], 0, [], [], None
        self.canonical = None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            k = a.get("name") or a.get("property")
            if k:
                self.meta[k] = a.get("content", "")
        elif tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "h1":
            self.h1 += 1
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._ld = ""

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "script" and self._ld is not None:
            self.ld.append(self._ld)
            self._ld = None

    def handle_data(self, d):
        if self.in_title:
            self.title += d
        if self._ld is not None:
            self._ld += d


def local(site, page_path, href):
    """Map an href to a file in the built site, or None if external/anchor."""
    if href.startswith(("mailto:", "tel:", "#", "javascript:")):
        return None
    if href.startswith(BASE):
        rel = href[len(BASE):]
    elif href.startswith(("http://", "https://")):
        return None
    else:
        rel = urlparse(urljoin("https://x/" + page_path.relative_to(site).as_posix(), href)).path.lstrip("/")
    rel = rel.split("#")[0]
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    return site / rel


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    skip_images = "--skip-images" in sys.argv
    site = Path(args[0]) if args else ROOT / "_site"
    errors, warns = [], []
    titles, descs = {}, {}
    pages = sorted(p for p in site.rglob("*.html"))
    for p in pages:
        rel = p.relative_to(site).as_posix()
        pg = Page()
        pg.feed(p.read_text(encoding="utf-8"))
        t, d = pg.title.strip(), pg.meta.get("description", "").strip()
        if not t:
            errors.append(f"{rel}: missing <title>")
        elif len(t) > 65:
            warns.append(f"{rel}: title {len(t)} chars (> 65)")
        if not d:
            errors.append(f"{rel}: missing meta description")
        elif not 50 <= len(d) <= 160:
            warns.append(f"{rel}: description {len(d)} chars (aim 50–160)")
        if rel != "404.html":
            titles.setdefault(t, []).append(rel)
            descs.setdefault(d, []).append(rel)
            if not pg.canonical or not pg.canonical.startswith(BASE):
                errors.append(f"{rel}: canonical missing or not under base_url")
            og = pg.meta.get("og:image", "")
            if not og.startswith(BASE) or (not skip_images and not (site / og[len(BASE):]).exists()):
                errors.append(f"{rel}: og:image missing or file not built ({og})")
            if pg.h1 != 1:
                errors.append(f"{rel}: {pg.h1} <h1> elements (need exactly 1)")
        for block in pg.ld:
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                errors.append(f"{rel}: JSON-LD does not parse ({e})")
        for img in pg.imgs:
            if not img.get("alt"):
                errors.append(f"{rel}: <img src={img.get('src')}> has no alt text")
        for href in pg.links:
            f = local(site, p, href)
            if f is not None and not f.exists():
                errors.append(f"{rel}: broken internal link {href}")
    for t, ps in titles.items():
        if len(ps) > 1:
            errors.append(f"duplicate title '{t}' on {ps}")
    for d, ps in descs.items():
        if len(ps) > 1:
            warns.append(f"duplicate description on {ps}")

    sm = (site / "sitemap.xml").read_text(encoding="utf-8") if (site / "sitemap.xml").exists() else ""
    if not sm:
        errors.append("sitemap.xml missing")
    for loc in re.findall(r"<loc>(.*?)</loc>", sm):
        f = local(site, site / "index.html", loc)
        if f is None or not f.exists():
            errors.append(f"sitemap URL has no page: {loc}")
    rb = (site / "robots.txt").read_text(encoding="utf-8") if (site / "robots.txt").exists() else ""
    for bot in ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended"):
        if f"User-agent: {bot}" not in rb:
            errors.append(f"robots.txt does not name {bot}")
    if f"Sitemap: {BASE}sitemap.xml" not in rb:
        errors.append("robots.txt has no Sitemap line")
    llms = (site / "llms.txt").read_text(encoding="utf-8") if (site / "llms.txt").exists() else ""
    if not llms:
        errors.append("llms.txt missing")
    for u in re.findall(r"\]\((https?://[^)]+)\)", llms):
        f = local(site, site / "index.html", u)
        if f is not None and not f.exists():
            errors.append(f"llms.txt link has no file: {u}")

    print(f"Checked {len(pages)} pages, {len(re.findall('<loc>', sm))} sitemap URLs.")
    for w in warns:
        print("  WARN ", w)
    for e in errors:
        print("  ERROR", e)
    if errors:
        sys.exit(1)
    print("OK: SEO/GEO checks pass.")


if __name__ == "__main__":
    main()
