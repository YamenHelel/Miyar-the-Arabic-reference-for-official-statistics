# ADR-0007: One shared quotes store

- **Date:** 2026-11-04 · **Status:** accepted

## Context
Quote slots lived inside each indicator file. New indicators and glossary concepts reuse the same official paragraphs (ILO §16, §27, §47), so the text would have been duplicated, and the copies could drift apart.

## Decision
All official wording lives in `content/quotes.yml` (schema `content/schema-quote.yaml`). Indicators and concepts reference slots by id. The file is machine-maintained (`tools/apply_quotes.py`). The validator checks that:
- every reference resolves
- text only comes from verified sources
- no slot is orphaned

## Consequences
One paste updates every page that uses the paragraph. The refactor was checked by rebuilding the unemployment page before and after: identical HTML.
