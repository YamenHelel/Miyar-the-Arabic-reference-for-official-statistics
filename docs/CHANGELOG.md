# CHANGELOG (current month, newest first)

Format: `## YYYY-MM-DD: title` → Done / Files / Decisions / Open questions. Older months are in `progress/`.

## 2026-11-04: Verification applied, repairs, first pilot indicator (session 4)
**Done**
- Applied the lead's 55 P1 verdicts: **51 verified, 4 broken**. Cleared the desk's verdicts. Phase 0a exit criterion met.
- Repairs (search, 2026-11-04):
  - ILO "aligning LFS" page → English URL; ILO Survey Catalog retired (410), so national metadata now comes from the ILOSTAT national sources catalogue.
  - Tunisia: Q1 2026 INS release page found. The INS NADA legacy URL also returned 404, so it is still broken.
  - Morocco: the new survey is the **Enquête sur la Main-d'Œuvre (EMO2026)**, from January 2026; the profile was updated.
  - PCBS: Q3 2025 release and 2025 microdata metadata added; the 2024 annual report is available via catalogue 740.
  - HCP and GCC-Stat pages return 404 to the robot but are indexed by search, so they are queued for a hand check (`--keep`).
  - Also added: ABS Detailed release, RAK LFS 2025, UN Statistical Commission 2013 Arabic employment statistics document.
- Second CI link check applied (`apply_link_report.py --keep`).
- **Phase 0b started:**
  - `content/schema-indicator.yaml`; validator extended to indicators.
  - `content/indicators/ind-unemployment-rate.yml`: 10 countries, 4 comparability notes, AI explanation, 14 quote slots `to-paste`.
- WebFetch could not reach any statistical host (DNS blocked), so no quotation was written by the agent.
- Desk v2 has a ✍️ quotes tab (collection `quotes`). New `tools/apply_quotes.py`, `tools/build_indicator_page.py` + `tools/indicator/template.html`. Indicator preview published: https://claude.ai/artifact/LXjvP5D5bhewcrVLFGCx6y

**Open questions:** network hosts for agents (I-044); domain/LinkedIn; feedback on the indicator page format before more indicators are built.

## 2026-11-04: Verification Desk (session 3)
**Done**
- Published the **Verification Desk**, a private artifact page: https://claude.ai/artifact/Vz1iDkkfzc7RZTa6fZdBiE. It holds a queue of 93 sources to check (55 P1). Each card has an "open source" button and ✅/⚠️/❌/⏭ verdicts plus a note. Verdicts are saved in the artifact's database (collection `verdicts`, only the owner/editors can write).
- New tools: `tools/build_verification_page.py` (page from YAML, template in `tools/verification/`) and `tools/apply_verification.py` (verdicts → YAML: verified/broken/review_note). Tested end to end with one test row (written, exported, applied, then reverted and deleted).
- Schema: added `review_note`.

**Open questions:** the Miʿyar domain name and LinkedIn page (to record).

## 2026-11-04: Name, licence, first push (session 2)
**Done**
- Lead's decisions applied: project name **مِعيار · Miʿyar, the Arabic reference for official statistics** (ADR-0006) and content licence **CC BY 4.0** (ADR-0005 accepted for content; the code licence is still open).
- Added `LICENSE` and a citation format to the README.
- Repository published at github.com/YamenHelel/Miyar-the-Arabic-reference-for-official-statistics (first push of the foundation from session 1).

**Files:** README.md, CLAUDE.md, LICENSE, docs/00-index.md, docs/decisions/ADR-0005, ADR-0006, docs/prd/01, 10, 15, docs/STATUS.md

- Later the same day: contact email set to yamen.hlel@gmail.com (README, consent texts, form spec, legal); **MIT** confirmed for code (`LICENSE-CODE`); first manual link-check run triggered in GitHub Actions.

- **First link check** (Actions run 41775682762): 120 URLs, 77 OK and 43 failing. Applied with the new `tools/apply_link_report.py`: **61 → link-ok, 8 → broken, 32 unchanged**.
  - Unchanged = the site blocks automated checkers (403: ILOSTAT, BLS, ESCWA, OECD, ISI, FCSC), SSL errors (PCBS) or temporary errors (ILO 502). These need a manual check in a browser.
  - Broken (404 / unreachable): HCP May 2026 ENE→new-survey note, GASTAT 2020 methodology PDF (already superseded), nada.ins.tn, archive.unescwa.org node, and 4 GCC-Stat pages (the site seems restructured).
- Added the `link_check` field to the schema. The workflow now prints the report into the run log and job summary (the artifact can't be downloaded from the sandbox). Actions bumped off Node 20.

**Open questions:** domain name and LinkedIn page for Miʿyar (lead says checks are done; record what was chosen).

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
