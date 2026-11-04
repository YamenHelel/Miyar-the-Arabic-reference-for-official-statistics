# STATUS (read this first)

**Project:** مِعيار · Miʿyar, the Arabic reference for official statistics · **Licence:** CC BY 4.0 (content), MIT (code) · **Contact:** yamen.hlel@gmail.com
**Updated:** 2026-11-05 · **Phase:** 0b, Pilot content (site and skill foundations of Phase 1 already built)

**Lead's tools:**
- Verification Desk https://claude.ai/artifact/Vz1iDkkfzc7RZTa6fZdBiE (sources + ✍️ 56 texts to paste: 24 labour + 32 ISI statistical definitions)
- Website preview (private) https://claude.ai/artifact/HN6DnYMFTDKFiSaHke6jqg
- Old single-indicator preview https://claude.ai/artifact/LXjvP5D5bhewcrVLFGCx6y (superseded by the site)

## Done
- **Content:**
  - 4 pilot indicators: unemployment rate (13 verified + 1 pasted official texts), participation rate, employment-to-population ratio, youth unemployment.
  - 40 concepts: 7 labour + 33 statistical (descriptive, sampling, estimation, rates), with a calculator on descriptive pages.
  - One shared quotes store, 38 slots: 13 verified, 1 pasted, 24 to paste.
- **Registry:** 123 sources: 56 verified, 34 link-ok, 17 collected, 5 broken, 3 superseded, 8 to-locate.
- **Website:** generator + design system (ADR-0008), 28 Arabic pages, search, live ruler; passes the design gate on the home page. Deploy workflow is ready but manual.
- **Code library (ADR-0010):** Python (tested), R (matches Python in CI), Stata (not executed); country presets from verified quotes; code page and tabs on indicator pages.
- **Claude skill v0:** `skills/miyar-labour-stats/`, generated from the base.
- **SEO/GEO (PRD 16):**
  - structured data, sitemap, robots (AI allowed), social cards
  - quick answers, fact-based FAQ, citation box, llms.txt and Markdown twins
  - `check_seo.py` in CI
  - README, CITATION.cff and CONTRIBUTING rewritten for search and AI

## Next 3 tasks
1. **Lead:**
   - On the desk's ✍️ tab, paste the 56 texts (the 32 statistical ones come from the ISI glossary, about 1 minute each), including the 24 texts (ILO §73(a)(b), working age, potential LF, underemployment, SDG 8.5.2 youth, ISI standard error, and the 6 Arab countries × 3 indicators). Then say "apply my quotes".
   - Confirm the Palestine transcription on the unemployment page.
2. **Lead:**
   - Review the website preview and give feedback on the design and wording.
   - Confirm the Arabic spelling of your name for the founder's letter; the letter is a draft in your voice, so edit it freely.
   - To go live: Settings → Pages → Source "GitHub Actions", then Actions → website → Run workflow.
3. **Lead (SEO/GEO, ~10 min):** paste the repo About box, topics and social preview from `docs/github-settings.md`. After go-live: Search Console + Bing, Zenodo DOI, Wikidata.
4. **Agent:** apply the quotes; confirm facts and add `measures` for the new indicators; add national definitions for USA, UK, Australia and France (Phase 1); refresh the site, skill and previews.

## Blockers / open questions
- The sandbox and WebFetch cannot reach statistical sites or open image collections, so quotes come from the lead, and the site's pictures are limited to the project's own artefacts (I-048).
- Domain name and LinkedIn page for Miʿyar (to record).
