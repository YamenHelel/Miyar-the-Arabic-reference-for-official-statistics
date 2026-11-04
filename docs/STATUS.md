# STATUS (read this first)

**Project:** مِعيار · Miʿyar, the Arabic reference for official statistics · **Licence:** CC BY 4.0 (content), MIT (code) · **Contact:** yamen.hlel@gmail.com
**Updated:** 2026-11-04 · **Phase:** 0b, Pilot content (Phase 0a exit criterion met: all P1 sources checked)

**Lead's tools:** Verification Desk https://claude.ai/artifact/Vz1iDkkfzc7RZTa6fZdBiE (sources + ✍️ quotes tab) · Indicator preview https://claude.ai/artifact/LXjvP5D5bhewcrVLFGCx6y

## Done
- Registry: **123 sources**: 56 verified, 34 link-ok, 17 collected, 5 broken, 3 superseded, 8 to-locate.
- All 55 P1 sources checked by the lead (51 ok, 4 broken → replacements found or documented).
- Indicator schema (`content/schema-indicator.yaml`) and the first pilot indicator **ind-unemployment-rate**: **13/14 official texts verified** (ILO §16, §27, §47, §73 and 9 countries); facts confirmed from the quotes for 5 countries; 6 comparability notes. Palestine still to paste.
- Tools: `apply_quotes.py`, `build_indicator_page.py`; the validator checks indicators (sources exist, quotes only from verified sources).

## Next 3 tasks
1. **Lead:** re-paste Palestine's definition (the PDF copy was garbled; type it or copy from another format). Review the indicator preview.
2. **Lead (lighter):** the remaining 51 sources on the desk (6 P1 first).
3. **Agent:** build pilot indicators 2–4 (participation rate, employment-to-population ratio, youth unemployment), reusing the verified ILO PDF and country documents, so many quotes may already be on pages the lead has opened.

## Blockers / open questions
- **The sandbox and WebFetch cannot reach statistical sites**, so every quotation needs the lead. Allowing hosts in the environment's network settings (ilo.org, ilostat.ilo.org, bls.gov, insee.fr, ons.gov.uk, abs.gov.au, stats.gov.sa, ins.tn, hcp.ma, pcbs.gov.ps, dos.gov.jo, fcsc.gov.ae) would let the agent draft quotes for the lead to check instead (I-044).
- Still to locate: Jordan DoS methodology and quarterly report page, UAE LFS methodology, ABS LFS methodology page, the ILO Arabic ICLS texts, the AITRS glossary.
- Domain name and LinkedIn page for Miʿyar (to record).
