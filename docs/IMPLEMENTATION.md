# Implementation progress

Updated every session, together with `STATUS.md`. **Built** means the agent has done the work; **validated** means the lead
(or a reviewer) has checked it. The live list of what awaits validation is [VALIDATION.md](VALIDATION.md), generated from the data.

Legend: ✅ done · 🟡 built, awaiting validation · 🔨 in progress · ⬜ planned

## Modules

| # | Module (PRD) | Built | Validated | Notes |
|---|---|---|---|---|
| M1 | Repo, PRD, progress system, ADRs (03) | ✅ | ✅ | ADR-0001…0012 |
| M2 | Source registry (F-05) | ✅ 133 records | 🟡 56 verified | 60 to check, 14 missing or broken |
| M3 | Shared quotes store (ADR-0007) | ✅ 85 slots | 🟡 13 verified, 1 pasted | 71 to paste |
| M4 | Indicator pages (F-01) | ✅ 4 pilots | 🟡 drafts | Phase 0b target: 10 indicators |
| M5 | Glossary (F-02) | ✅ 40 concepts | 🟡 drafts | Phase 0b target: 50 |
| M6 | **Data sources (F-11, ADR-0011)** | ✅ 4 types + 6-part LFS guide | 🟡 drafts, 15 texts to paste | Country inventory: LFS only; census and registers in Phase 1 |
| M7 | Country profiles (F-04) | ✅ 10 countries | 🟡 20 fields to confirm | |
| M8 | Microdata catalogue (F-06) | ✅ | 🟡 | `sources/microdata/puf-catalog.yaml` |
| M9 | Website generator + design (ADR-0008) | ✅ 73 pages | 🟡 lead review pending | Private preview; not public yet |
| M10 | SEO/GEO (PRD 16, ADR-0009) | ✅ | ⬜ go-live tasks (lead) | `check_seo.py` in CI |
| M11 | Claude skill (F-09) | ✅ v0, 56 references | ⬜ external test | `skills/miyar-labour-stats/` |
| M12 | Code library (ADR-0010) | ✅ Python, R | 🟡 Stata not run | R = Python on 32 results in CI |
| M13 | Verification Desk | ✅ | ✅ in use | Artifact with `verdicts` and `quotes` collections |
| M18 | عربي / English switcher on national definitions and country cards (ADR-0012) | ✅ | 🟡 10 translations + 10 country cards to review | ILO sheets still original-only (I-063) |
| M14 | Validation queue | ✅ | n/a | `tools/build_validation_queue.py` → `VALIDATION.md`, checked in CI |
| M15 | Practitioner directory (ADR-0003) | ✅ design | ⬜ form not opened | Phase 1 |
| M16 | SDG hub (F-07) | ⬜ | ⬜ | SDG metadata sources collected |
| M17 | Standards library (F-03) | ⬜ | ⬜ | Sources collected; pages not built |

## Phase checklist (from PRD 03)

**Phase 0a: Foundation**: ✅ complete (exit criterion met on 2026-11-04).

**Phase 0b: Pilot content**: 🔨
- ✅ site generator, skill v0, code library, data sources section
- 🔨 10 pilot indicators (4 built)
- 🔨 50 concepts (40 built)
- ⬜ official texts pasted for the pilots (13 + 1 of 85)
- ⬜ exit: 5 external statisticians test it

**Phase 1: Public launch (Jan–Mar 2027)**: ⬜, with SEO/GEO base already built.

## Next build steps (agent)
1. Apply the lead's quotes and verifications as they arrive; refresh site, skill, desk and previews.
2. Indicators 5–10: NEET, LU2/LU3/LU4, informal employment rate, time-related underemployment.
3. Data sources, Phase 1: census and administrative registers for each of the 10 countries (needs about 30 new source records).
