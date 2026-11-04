# ADR-0011: Data sources section and the LFS guide

- **Date:** 2026-11-04 · **Status:** accepted (lead chose the scope in chat)

## Context
Users need to know where labour statistics come from and which source fits which question. The lead asked for a part on data
sources (LFS, census, registers…), with the ILO as the first source of truth for the LFS.

## Decision
- New content type `content/data-sources/` (schema `content/schema-datasource.yaml`), with `kind: type | guide`.
- **First wave (lead's choice):**
  - the core four types: LFS, population census, administrative records, establishment surveys
  - a full six-part LFS guide
  - country instances for the LFS only. Census and registers per country move to Phase 1 (I-059).
- **Official wording:**
  - quote slots in `content/quotes.yml` (ADR-0007), as usual
  - the ILO comes first: ICLS-19 resolution, the ILO quick guide on sources and uses, the LFS toolkit, the microdata guide, Sources and Methods
  - UN texts are used for the census (P&R Rev.3, UN/ILO handbook 2010)
- Everything else is AI-assisted and labelled. This covers the summaries, strengths and limits, the "what it measures" grid, and the guide sections; field names end in `_ai_*`.
- The `produces` grid uses `main | partial | none` (not `no`, which YAML reads as false).
- The site gets a "مصادر البيانات" section. The document registry is renamed «المراجع / سجل المراجع» so the two are not confused. The home page's folder tab now opens the data sources section; the registry stays in the nav and footer.

## Consequences
- 15 new quote slots and 10 new source records (8 collected, 2 to-locate) join the lead's queue.
- `tools/validate.py` checks data-source files; the skill and `llms.txt` include them.
