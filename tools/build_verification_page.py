#!/usr/bin/env python3
"""Build the Verification Desk page (an HTML artifact) from the source registry.

Usage:
  python tools/build_verification_page.py OUT.html

Also lists every indicator quote slot still `to-paste` (the "quotes" tab).
The queue = every source whose status is `collected` or `link-ok` (it still
needs a human check), ordered by priority then by group. Records that are
verified, superseded, broken or to-locate are left out: broken and to-locate
items are the agent's job, not the lead's.
The output is a build artifact; it is published with the Artifact tool and
not committed.
"""
import datetime as dt
import json
import sys
from pathlib import Path

from common import SOURCES_DIR, indicator_files, iter_sources, load_yaml

TEMPLATE = Path(__file__).resolve().parent / "verification" / "template.html"

# group key -> (sort order, label shown in the filter chips)
GROUPS = {
    "ilo": (0, "ILO"),
    "arab-regional": (1, "هيئات عربية"),
    "tun": (2, "تونس"), "sau": (3, "السعودية"), "mar": (4, "المغرب"),
    "jor": (5, "الأردن"), "are": (6, "الإمارات"), "pse": (7, "فلسطين"),
    "sdg": (8, "SDG"),
    "global-other": (9, "هيئات دولية أخرى"),
    "usa": (10, "USA"), "gbr": (11, "UK"), "aus": (12, "Australia"), "fra": (13, "France"),
}
TODO = {"collected", "link-ok"}


def group_of(path):
    rel = path.relative_to(SOURCES_DIR)
    if rel.parts[0] == "sdg":
        return "sdg"
    return rel.stem


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    queue = []
    for path, rec in iter_sources():
        if rec.get("status") not in TODO:
            continue
        g = group_of(path)
        queue.append({
            "id": rec["id"],
            "file": path.relative_to(SOURCES_DIR).as_posix(),
            "group": g,
            "priority": rec.get("priority", "P3"),
            "status": rec.get("status"),
            "type": rec.get("type"),
            "title_en": rec.get("title_en", ""),
            "title_ar": rec.get("title_ar", ""),
            "publisher": rec.get("publisher", ""),
            "date_published": str(rec.get("date_published", "") or ""),
            "url": rec.get("url"),
            "hint": " ".join(str(rec.get("notes", "") or "").split())[:280],
        })
    queue.sort(key=lambda q: (q["priority"], GROUPS.get(q["group"], (99, ""))[0], q["id"]))
    groups = {k: v[1] for k, v in sorted(GROUPS.items(), key=lambda kv: kv[1][0])
              if any(q["group"] == k for q in queue)}

    reg = {r["id"]: r for _, r in iter_sources()}
    quotes = []
    for ipath in indicator_files():
        ind = load_yaml(ipath)
        for qd in ind.get("quotes", []) or []:
            if qd.get("status") != "to-paste":
                continue
            src = reg.get(qd.get("source"), {})
            quotes.append({"slot": qd["slot"], "indicator": ind["id"], "indicator_name_ar": ind.get("name_ar", ""),
                           "source": qd.get("source"), "source_title": src.get("title_en", ""), "url": src.get("url", ""),
                           "locator": qd.get("locator", ""), "what_ar": qd.get("what_ar", ""), "lang": qd.get("lang", "en")})

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("/*__QUOTES__*/[]", json.dumps(quotes, ensure_ascii=False).replace("</", "<\\/"))
    data = json.dumps(queue, ensure_ascii=False).replace("</", "<\\/")
    html = html.replace("/*__QUEUE__*/[]", data)
    html = html.replace("/*__GROUPS__*/{}", json.dumps(groups, ensure_ascii=False))
    html = html.replace("/*__BUILT__*/", str(dt.date.today()))
    Path(sys.argv[1]).write_text(html, encoding="utf-8")
    p1 = sum(q["priority"] == "P1" for q in queue)
    print(f"Queue: {len(queue)} sources ({p1} P1), {len(quotes)} quote slots. Wrote {sys.argv[1]}")


if __name__ == "__main__":
    main()
