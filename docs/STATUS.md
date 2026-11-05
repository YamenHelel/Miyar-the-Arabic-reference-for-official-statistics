# STATUS (read this first)

**Project:** مِعيار · Miʿyar, the Arabic reference for official statistics · **Licence:** CC BY 4.0 (content), MIT (code) · **Contact:** yamen.hlel@gmail.com
**Updated:** 2026-11-05 · **Phase:** 0b, Pilot content (site and skill foundations of Phase 1 already built)

**Lead's tools:**
- Verification Desk https://claude.ai/artifact/Vz1iDkkfzc7RZTa6fZdBiE (sources + ✍️ 71 texts to paste)
- Website preview (private) https://claude.ai/artifact/HN6DnYMFTDKFiSaHke6jqg
- **What to validate:** [VALIDATION.md](VALIDATION.md) (generated) · **Progress per module:** [IMPLEMENTATION.md](IMPLEMENTATION.md)

## Done
- **Content:**
  - 4 pilot indicators and 40 concepts (7 labour, 33 statistical)
  - **New: data sources section (ADR-0011).** It covers the LFS, census, administrative records and establishment surveys, plus a 6-part LFS guide with the ILO as first source. There is a "which source for which question" matrix and an LFS table for the 10 countries.
  - Quotes store: 85 slots, of which 13 verified, 1 pasted, 71 to paste.
- **Registry:** 133 sources: 56 verified, 34 link-ok, 26 collected, 9 to-locate, 5 broken, 3 superseded.
- **Website:** 73 Arabic pages, private preview only. The nav now has «مصادر البيانات», and the document registry is renamed «المراجع».
- **Code library:** Python tested, R = Python in CI, Stata not executed.
- **Skill:** 56 references.
- **SEO/GEO:** checks pass on all pages.
- **Language switcher (ADR-0012):** عربي / English on national definitions, country cards and the ILO text sheets. Translations are labelled unofficial and the original stays the reference (24 items to review, queue 7b).
- **Validation queue:** `tools/build_validation_queue.py` writes `docs/VALIDATION.md` from the data, and CI fails if it is stale. Manual decisions live in `docs/lead-actions.yml`.

## Next 3 tasks
1. **Lead:** work through [VALIDATION.md](VALIDATION.md) top-down, starting with queue 1.
   - Paste the texts on the desk ✍️ tab and say "apply my quotes".
   - The new data-source texts mostly come from one ILO document (quick guide on sources and uses, 4 texts) and the ICLS-19 PDF (3 texts).
2. **Lead:**
   - Review the preview, including the new data sources pages.
   - Confirm the Palestine transcription.
   - Go-live steps (Pages, GitHub About, then Search Console, Zenodo, Wikidata) are listed in section 9 of VALIDATION.md.
3. **Agent:**
   - Apply quotes and verifications as they arrive.
   - Build indicators 5–10 (NEET, LU2–LU4, informality, underemployment).
   - Then census and registers per country (I-059).

## Blockers / open questions
- The sandbox cannot reach statistical sites, so quotes come from the lead (I-044 would lift this).
- Domain name and LinkedIn page are still to be decided.
