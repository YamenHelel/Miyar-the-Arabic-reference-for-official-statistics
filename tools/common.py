"""Shared helpers: load all source records from sources/**/*.yaml."""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SOURCES_DIR = ROOT / "sources"


def source_files():
    return sorted(p for p in SOURCES_DIR.rglob("*.yaml") if p.name != "schema.yaml")


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def iter_sources():
    """Yield (path, record) for every source record."""
    for path in source_files():
        data = load_yaml(path)
        for rec in data.get("sources", []) or []:
            yield path, rec


def iter_catalog_urls():
    """Yield (path, label, url) for microdata catalogue routes."""
    for path in source_files():
        data = load_yaml(path)
        for entry in data.get("catalog", []) or []:
            for route in entry.get("routes", []) or []:
                yield path, f"{entry.get('country')}:{route.get('provider')}", route.get("url")


CONTENT_DIR = ROOT / "content"


def indicator_files():
    return sorted((CONTENT_DIR / "indicators").glob("*.yml"))


QUOTES_FILE = CONTENT_DIR / "quotes.yml"
QUOTES_HEADER = """# Miʿyar shared quotes store — official wording, copied verbatim by a human from a verified source.
# Machine-maintained: edit through tools/apply_quotes.py (or by hand with care; keep text verbatim).
# Indicators and concepts reference these slots by id. Schema: content/schema-quote.yaml.
"""


class _Literal(str):
    pass


def _literal_representer(dumper, data):
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")


yaml.SafeDumper.add_representer(_Literal, _literal_representer)


def load_quotes():
    """Return the list of quote slots (dicts) from content/quotes.yml."""
    if not QUOTES_FILE.exists():
        return []
    return load_yaml(QUOTES_FILE).get("quotes", []) or []


def save_quotes(quotes):
    out = []
    for q in quotes:
        q = dict(q)
        if isinstance(q.get("text"), str) and "\n" in q["text"]:
            q["text"] = _Literal(q["text"])
        out.append(q)
    body = yaml.safe_dump({"quotes": out}, allow_unicode=True, sort_keys=False, width=1000)
    QUOTES_FILE.write_text(QUOTES_HEADER + body, encoding="utf-8")


def quotes_by_slot():
    return {q["slot"]: q for q in load_quotes()}


def concept_files():
    return sorted((CONTENT_DIR / "concepts").glob("*.yml"))


def datasource_files():
    return sorted((CONTENT_DIR / "data-sources").glob("*.yml"))
