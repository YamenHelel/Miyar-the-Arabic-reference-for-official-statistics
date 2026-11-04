#!/usr/bin/env python3
"""Prepare the built site (_site/) for publishing as a private claude.ai artifact preview.

Usage:
  python tools/build_site.py && python tools/prepare_site_preview.py OUT_PAGE.html OUT_FILES.json

The artifact wraps its main page in its own document skeleton, so index.html is reduced to its <title>, head links
and body. Every other file is listed in OUT_FILES.json as {published_path: source_path} for the Artifact `files` map.
Preview URL (lead only): see docs/STATUS.md.
"""
import json
import re
import sys
from pathlib import Path

from common import ROOT


def main():
    site = ROOT / "_site"
    html = (site / "index.html").read_text(encoding="utf-8")
    head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
    body = re.search(r"<body>(.*)</body>", html, re.S).group(1)
    head = re.sub(r'<meta charset="utf-8">\s*<meta name="viewport"[^>]*>', "", head)
    title = re.search(r"<title>.*?</title>", head).group(0)
    head = head.replace(title, "", 1)
    page = (title + '\n<meta name="claude:viewport-fit-sides" content="cover">\n' + head.strip() +
            '\n<script>document.documentElement.lang="ar";document.documentElement.dir="rtl";'
            'document.documentElement.setAttribute("data-root","./");</script>\n' + body)
    Path(sys.argv[1]).write_text(page, encoding="utf-8")
    files = {str(p.relative_to(site)): str(p.relative_to(ROOT)) for p in sorted(site.rglob("*"))
             if p.is_file() and p.relative_to(site).as_posix() != "index.html"}
    Path(sys.argv[2]).write_text(json.dumps(files, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"page -> {sys.argv[1]}; {len(files)} files -> {sys.argv[2]}")


if __name__ == "__main__":
    main()
