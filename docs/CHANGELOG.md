# CHANGELOG (current month, newest first)

Format: `## YYYY-MM-DD: title` → Done / Files / Decisions / Open questions. Older months are in `progress/`.

## 2026-11-05: Data sources section, validation queue, implementation tracker (session 10)
**Done**
- **Data sources (ADR-0011):** `content/data-sources/` with schema `content/schema-datasource.yaml`. Scope chosen by the lead: the core 4 types, a full LFS guide, and LFS-only country inventory.
  - **Types:** labour force survey, population census, administrative records, establishment surveys. Each has:
    - official-text slots
    - how the source works, its strengths and limits, and a "what it measures" grid (all AI-labelled)
    - further reading from the registry
  - **LFS guide:** framework (ICLS-19), questionnaire (ILO model), sample design and rotation, weighting and estimation, periodicity, quality and comparability. Linked to the glossary and the code library.
  - **15 new to-paste quote slots.** ILO first: ICLS-19 (3), ILO quick guide on sources and uses (4), LFS toolkit, microdata guide, aligning-LFS hub, WORK database description, Sources and Methods vol. 2 and 4. UN for the census: P&R Rev.3, UN/ILO 2010 handbook.
  - **10 new source records** (8 collected, 2 to-locate), all from search results and not opened: ILO quick guide, ILOSTAT admin-data and establishment-survey pages, Sources and Methods vols 2, 3 and 4, UN census P&R Rev.3, UN/ILO census handbook. To-locate: the ILO 1997 admin-records guidelines and the ILOSTAT census resources page.
- **Site:**
  - new «مصادر البيانات» section: index with the source × topic matrix, 10 pages with Markdown twins, JSON-LD, social cards, search entries and llms.txt
  - the registry is renamed «المراجع / سجل المراجع»
  - the home folder tab now opens data sources
  - 73 pages; SEO check passes
  - no horizontal scroll at 390 px
- **Skill:** gains 10 data-source references (56 total).
- **Validation queue:** `tools/build_validation_queue.py` writes `docs/VALIDATION.md` from the data, with 9 queues and counts. Manual decisions are in `docs/lead-actions.yml`. CI checks it is current (`--check`).
- **Implementation tracker:** `docs/IMPLEMENTATION.md` shows built vs validated per module and the phase checklist.
- **Docs:** PRD 04 F-11, roadmap 0b, backlog I-059…I-062, index, and the CLAUDE.md routine (step 6).

**Files:** content/data-sources/*, content/schema-datasource.yaml, content/quotes.yml, sources/international/{ilo,global-other}.yaml, tools/{build_site,validate,common,markdown_render,seo,build_skill,build_validation_queue}.py, tools/site/templates/{datasource,datasources_index,base,home,sources}.html, tools/site/static/miyar.css, .github/workflows/checks.yml, docs/*.

**Open questions:** none. Census and registers per country are deferred to Phase 1 by the lead's choice.

## 2026-11-05: Code library (session 9)
**Done**
- `code/`: computes the ICLS-19 indicators (LFPR, EPR, LU1–LU4, youth UR, NEET) from LFS microdata, with weights, linearised SE, CV, 95% CI and approximate design effect; disaggregation by any variable.
  - Python `code/python/miyar_lfs.py`: tested, `tools/test_code.py` with 22 checks
  - R `code/r/miyar_lfs.R` (survey package): run in CI, **agrees with Python on all 32 results**
  - Stata `code/stata/miyar_lfs.do`: not executed, labelled as such
- Country presets `code/presets/countries.json`, generated from quote-backed measures only (`tools/build_code_presets.py`): ILO, USA, AUS, SAU, MAR, JOR, ARE, PSE.
- Synthetic, seeded test file (6,824 invented persons). The first CI run failed because `*.csv` was gitignored; fixed with an explicit exception.
- **Site:**
  - new code page (`code/index.html`, SoftwareSourceCode JSON-LD) and a "الشيفرة" nav link
  - «احسبه من بياناتك» tabs (Python/R/Stata) on 4 indicator pages
  - the website's Python snippet was executed and works
- Skill gains `references/code.md`. ADR-0010; backlog I-018 done, I-056…I-058.

**Open questions:** none.

## 2026-11-05: Statistical concepts glossary, core set (session 8)
**Done**
- **32 new statistical concepts** in 4 groups:
  - descriptive (11): mean, weighted mean, median, mode, range, variance, SD, CV, percentiles, IQR, outlier
  - sampling (9): population, sample, frame, SRS, stratified, cluster, weights, non-response, response rate
  - estimation (8, with standard error): estimate, sampling/non-sampling error, CI, margin of error, design effect, bias
  - rates (5): rate, ratio/proportion, percentage point, index number, seasonal adjustment

  The glossary now has 40 concepts.
- Each concept has:
  - Arabic name and EN/FR names
  - Arabic term variants (Mashreq/Maghreb, marked «للتحقق»)
  - a formula in standard notation (labelled «صيغة رياضية قياسية، وليست نصاً رسمياً منقولاً»)
  - an AI explanation, a worked example and a "use in labour statistics" note, all labelled
  - a quote slot for the official ISI wording (32 new to-paste slots; the OECD Glossary is the fallback)
- `src-oecd-glossary` URL found (publication page, `collected`); Arabic titles added for the ISI and OECD glossaries.
- Schema: `group`, `formula_basis`, `in_labour_stats_ai_ar`; the validator requires `group` for statistical concepts.
- **«احسب بنفسك» calculator** on descriptive concept pages: deterministic, shows the formula of each measure, accepts Arabic digits. Checked against known values (mean 5, median 4.5, mode 4, SD 2 / 2.138; weighted mean 620).
- **Site:**
  - concepts index and home glossary sheet grouped into 5 sections
  - "concept · group" label moved under the title (it read as an eyebrow); the pending-sheet contrast fixed
  - quick answer rewritten so the Latin names come last (it scrambled on phones)
  - 61 pages; `check_seo.py` passes; the design gate shows only the defended picture floor on reading pages
- Skill regenerated (45 reference files); desk (56 texts to paste) and private preview refreshed. Backlog I-054, I-055.

**Open questions:** none; the lead pastes the ISI definitions from the desk.

## 2026-11-04: SEO and GEO for the website and the repository (session 7)
**Done**
- Plan: PRD 16 (20 target queries/AI prompts AR/FR/EN, checklist, citability rules, KPIs, lead actions); ADR-0009 (Pages URL as canonical; all crawlers incl. AI allowed); roadmap Phase 1/2 items; backlog I-050…I-053.
- **Technical SEO:**
  - `tools/site/config.yaml`; canonical, hreflang, OG/Twitter, robots meta, favicon, manifest, 404
  - JSON-LD: WebSite/Organization, DefinedTerm(Set), Article with `isBasedOn`, BreadcrumbList, FAQPage, Dataset
  - `sitemap.xml`; `robots.txt` naming 17 AI user agents; social cards for 13 pages + site (`tools/build_social_cards.mjs`)
- **GEO:**
  - deterministic quick answers and quote-backed FAQ (US age from a snippet is excluded); citation box with copy on every page
  - `llms.txt`, `llms-full.txt` (67 KB), and a `.md` twin per indicator/concept
  - shared `tools/markdown_render.py` (skill output byte-identical after the refactor)
- **Gate:** `tools/check_seo.py` passes (29 pages, 28 sitemap URLs); added to both workflows. The design gate shows no new failures.
- **GitHub:**
  - README opening rewritten (bilingual quick answer, badges, what's inside, how to cite)
  - `CITATION.cff` (valid against the CFF 1.2.0 schema), `CONTRIBUTING.md`, correction issue form + label
  - Repo description/topics/homepage are blocked by the sandbox proxy, so ready-to-paste values are in `docs/github-settings.md`
- Private site preview refreshed (with the SEO files and social cards).

**Open questions:** none new; the lead's actions are listed in `docs/github-settings.md`.

## 2026-11-04: Programming day: quotes store, concepts, indicators 2–4, website, Claude skill (session 6)
**Done**
- **Lead's inputs:**
  - Palestine definition transcribed from the lead's screenshot (`pasted`, to confirm).
  - PCBS book2740 title («دليل المؤشرات الإحصائية…، 2025», PDF letter-order artefacts corrected) and HCP EMO Q3 2026 note title recorded.
  - «chômage strict» confirmed as the EMO2026 definition.
- **ADR-0007:** shared `content/quotes.yml`. All tools rewired; the unemployment page is byte-identical before and after.
- **Concepts (8):** working-age population, labour force, employed, unemployed, outside LF, potential LF, time-related underemployment, standard error.
- **Indicators 2–4:**
  - participation rate, employment-to-population ratio, youth unemployment rate
  - 24 new to-paste slots with precise locators
  - comparability notes: age floor, nationals vs total, 13th vs 19th ICLS, youth age bands
- **ADR-0008 website:**
  - `tools/build_site.py` + `tools/site/` (templates, `miyar.css`, `miyar.js`), 28 pages, Arabic-normalised search
  - live ruler (availability, search period, age) using quote-backed `measures` only
  - display-only reflow of PDF line breaks; comparison facts in Arabic
  - design by the tasteskill process: direction "page is the object", gold sheet + hallmark for official text, Amiri
  - Gate: home 0 FAIL / 3 defended WARN; indicator page 1 FAIL (picture floor, defended for reading pages)
- **Pictures:** the lead's PCBS screenshot plus photographs of the project's own tools (desk card, official sheet, comparison table). Open collections were unreachable.
- **Deploy and preview:** `.github/workflows/pages.yml` (manual only); `tools/prepare_site_preview.py`; private preview published.
- **Claude skill v0:** `tools/build_skill.py` → `skills/miyar-labour-stats/` (SKILL.md + 13 references). A check confirms no pending text is presented as official.
- Desk and old preview refreshed. Backlog I-046…I-049.

**Open questions:** Arabic spelling of the lead's name (letter signed "مؤسس مِعيار" for now); domain/LinkedIn.

## 2026-11-04: Lead's quotes applied, unemployment rate 13/14 official texts (session 5)
**Done**
- Applied 13 of the lead's 14 pasted texts to `ind-unemployment-rate` as `verified` (the lead's own verbatim paste is the human check).
  - Pasted link and document-header lines were moved into `quoted_from_url` / `document_note`.
  - A script confirmed every stored text is an unchanged excerpt of the paste.
- **Palestine:** the pasted text came out garbled (PDF extraction broke the Arabic), so the slot is back to `to-paste` with new instructions.
- Registry:
  - New records, verified via the lead's paste: `src-ilo-icls19-res1-pdf` (resolution text amended by the 21st ICLS 2023), `src-mar-hcp-chomage-strict`, `src-pse-pcbs-book2740`.
  - Filled `src-jor-dos-methodology` (dosweb concepts page) and `src-are-lfs-methodology` (FCSC xlsx).
- Country facts now based on the quotes for AUS, SAU, MAR, JOR, ARE (age, search period, availability) and partly for USA.
- New comparability notes:
  - **Availability windows differ:** reference week (AUS, USA); +2 weeks (SAU, MAR); 15 days (JOR); 4 weeks after the interview (ARE), which is wider than the 19th ICLS maximum of two weeks (§47-d).
  - **UK and France:** the quoted texts are the 1982 (13th ICLS) wording that ONS and Insee reproduce.
- `apply_quotes.py`: `--status verified`, source/lang overrides, `quoted_from_url`, `document_note`. Preview adds an availability column and document notes.
- Desk quotes cleared; the desk now shows 1 quote card (Palestine) and 51 sources.

**Open questions:** exact titles of the HCP attachment 2927551 and PCBS book2740; whether the HCP «chômage strict» definition is EMO2026.

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
