# CHANGELOG (current month, newest first)

Format: `## YYYY-MM-DD: title` → Done / Files / Decisions / Open questions. Older months are in `progress/`.

## 2026-11-03: Project foundation (session 1)
**Done**
- Created the repo structure and the agent rules (`CLAUDE.md`) with an end-of-session routine.
- Wrote the full PRD (01–15): vision, personas, roadmap, current features, ideas backlog (I-001…I-043), architecture, data model, governance, business model, brand, partnerships, legal and privacy, KPIs, risks, naming.
- Source registry v0: 112 records across the ILO (25), Arab regional bodies (20), global bodies (12), SDG (6) and 10 countries (49). Labour SDG reference table with 16 indicators.
- Microdata catalogue: access routes per country (ERF OAMDI, national NADA catalogues, Insee detail files, CPS/IPUMS, UK Data Service, ABS TableBuilder).
- Practitioner directory design: schema, consent text (AR authoritative, EN), form spec, export procedure.
- Tools: `validate.py` (all records valid), `check_links.py`, `archive.py`; GitHub Actions workflow (validate on push, weekly link check).

**Decisions:** ADR-0001 to ADR-0004 accepted; ADR-0005 (licensing) proposed.

**Notable findings (to verify)**
- Morocco: HCP redesigned the ENE; a May 2026 technical note describes the move to a new survey (sample 90k → 135k households, aligned with the ICLS).
- ILOSTAT: the LFS database is based on the 13th ICLS, the WORK database on the 19th. This is a key comparability point for the site.
- Jordan: DoS publishes both overall and Jordanian-only unemployment rates (Q2 2026 per press: 16.1% overall, 21.0% Jordanians).
- UAE: LFS tables have not been split by nationality since 2020 (per GLMM); methodology metadata is scarce.
- France: Insee publishes free annual EEC detail files (CSV/Parquet), which are good for training labs.
- 21st ICLS (2023) informality resolution replaces the 1993 and 2003 texts, which affects SDG 8.3.1.

**Open questions:** GitHub repo name; licence choice; project name; contact email for the directory.

**Environment note:** the sandbox network policy blocked direct access to statistical sites (403 at the proxy). All URLs come from search results, so their status is `collected`.
