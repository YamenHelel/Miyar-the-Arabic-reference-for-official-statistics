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
