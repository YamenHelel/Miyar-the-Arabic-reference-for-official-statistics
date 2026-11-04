# STATUS (read this first)

**Project:** مِعيار · Miʿyar, the Arabic reference for official statistics · **Licence:** CC BY 4.0 (content), MIT (code) · **Contact:** yamen.hlel@gmail.com
**Updated:** 2026-11-04 · **Phase:** 0b, Pilot content (Phase 0a exit criterion met: all P1 sources checked)

**Lead's tools:** Verification Desk https://claude.ai/artifact/Vz1iDkkfzc7RZTa6fZdBiE (sources + ✍️ quotes tab) · Indicator preview https://claude.ai/artifact/LXjvP5D5bhewcrVLFGCx6y

## Done
- Registry: **120 sources**: 51 verified, 34 link-ok, 17 collected, 5 broken, 3 superseded, 10 to-locate.
- All 55 P1 sources checked by the lead (51 ok, 4 broken → replacements found or documented).
- Indicator schema (`content/schema-indicator.yaml`) and the first pilot indicator **ind-unemployment-rate**: structure, 10-country table, comparability notes and AI explanation are done. **14 official quotes still to paste.**
- Tools: `apply_quotes.py`, `build_indicator_page.py`; the validator checks indicators (sources exist, quotes only from verified sources).

## Next 3 tasks
1. **Lead:** on the desk's ✍️ tab, paste the 14 official texts (open the document, copy the paragraph verbatim, Save). Then say "apply my quotes".
2. **Lead (lighter):** the remaining 51 sources on the desk (6 P1 first).
3. **Agent:** after the quotes, mark country facts confirmed or corrected from the pasted text; build pilot indicators 2–4 (participation rate, employment-to-population ratio, youth unemployment) the same way.

## Blockers / open questions
- **The sandbox and WebFetch cannot reach statistical sites**, so every quotation needs the lead. Allowing hosts in the environment's network settings (ilo.org, ilostat.ilo.org, bls.gov, insee.fr, ons.gov.uk, abs.gov.au, stats.gov.sa, ins.tn, hcp.ma, pcbs.gov.ps, dos.gov.jo, fcsc.gov.ae) would let the agent draft quotes for the lead to check instead (I-044).
- Still to locate: Jordan DoS methodology and quarterly report page, UAE LFS methodology, ABS LFS methodology page, the ILO Arabic ICLS texts, the AITRS glossary.
- Domain name and LinkedIn page for Miʿyar (to record).
