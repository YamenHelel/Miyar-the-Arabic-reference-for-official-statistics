# 03: Scope, phases and roadmap

Capacity: **about 1 hour per day, 7 days a week** for the lead (~30 h/month). AI agents do the drafting and collection; the lead reviews, verifies and decides.

## Phase 0a: Foundation (Nov 2026) ← *current*
- [x] Repo structure, PRD, progress system, ADRs
- [x] Source registry v0: international bodies, 10 countries, SDGs, microdata (status `collected`)
- [x] Practitioner directory design
- [x] Repo pushed to GitHub; link checker runs in CI
- [x] Lead verifies the top-priority sources (all 55 P1 done 2026-11-04)

**Exit:** all P1 sources are `link-ok` and at least 50% of them `verified`.

## Phase 0b: Pilot content (Dec 2026)
- Indicator schema finalised. **10 pilot indicators** fully documented: labour force participation rate, employment-to-population ratio, unemployment rate, youth unemployment rate, NEET rate, LU2/LU3/LU4, informal employment rate, time-related underemployment.
- **50 concepts** in the glossary (statistical and labour).
- A Quarto RTL site running locally.
- Claude skill v0 that answers only from the base.

**Exit:** 5 external statisticians test it and give feedback.

## Phase 1: Public launch, labour domain (Jan–Mar 2027)
- ~60 indicators, ~150 concepts, 10 countries, labour SDGs.
- Public website (GitHub Pages and a custom domain); Claude skill v1 published.
- Practitioner directory form opened.
- Launch campaign: a LinkedIn series, a webinar, and Arab Statistics Day if the timing fits.

**Exit:** 500 monthly visitors, 10 reviewers registered, first training booked.

## Phase 2: Grow (Apr–Dec 2027)
- More Arab countries, one at a time (suggested order: Egypt, Oman, Qatar, Bahrain, Kuwait, Algeria, Lebanon, Iraq, Sudan, Mauritania, Libya, Yemen, Syria, Somalia, Djibouti, Comoros); see the per-country checklist below.
- Second domain chosen by demand (candidates: prices/CPI, population and demography, national accounts).
- MCP server; Codex and other agent skills; English/French UI.
- Editorial board formalised.

## Phase 3: Toolbox (2028)
Interactive tools: questionnaire reviewer, metadata drafter, indicator calculator, code library and more. See `05-ideas-backlog.md`.

## Phase 4: Statistics AI wiki (2028+)
All domains and roles; institutional partnerships; optional hosted versions for NSOs.

## Checklist for adding a country
1. Create `sources/countries/<iso3>.yaml` from an existing file.
2. Fill in: NSO, LFS (name, frequency, mode, sample, ICLS standard), methodology documents, questionnaire, publications, data portal, microdata access, other surveys with labour indicators.
3. Add microdata entries to `sources/microdata/puf-catalog.yaml`.
4. Run the validator and the link checker.
5. Lead verifies the P1 entries.
6. Add the country's implementation to every existing indicator page.
7. Announce it (LinkedIn post: "X now added").

## Typical daily hour for the lead
| Minutes | Task |
|---|---|
| 5 | Read `STATUS.md` |
| 35 | Verify sources or review AI-drafted content (≈ 8–10 items) |
| 15 | Brief the AI agent on the next batch / approve PR |
| 5 | AI updates the CHANGELOG and STATUS |
