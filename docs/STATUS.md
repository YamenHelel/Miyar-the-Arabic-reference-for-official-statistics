# STATUS (read this first)

**Project:** مِعيار · Miʿyar, the Arabic reference for official statistics · **Licence:** CC BY 4.0 (content), MIT (code) · **Contact:** yamen.hlel@gmail.com
**Updated:** 2026-11-04 · **Phase:** 0a, Foundation · **Next phase:** 0b, Pilot content (10 indicators)

## Done
- Repo published on GitHub; structure, agent rules, PRD (15 files), ADRs 0001–0006
- Name (Miʿyar), licences (CC BY 4.0 content, MIT code) and contact email decided
- Source registry v0: **112 records**: 61 link-ok, 32 collected (bot-blocked: check by hand), 8 broken, 11 to-locate, 0 verified
- Microdata access catalogue for the 10 countries; practitioner directory design
- Tools: `validate.py` (passing), `check_links.py`, `archive.py`; CI workflow

**Verification Desk (lead's daily tool):** https://claude.ai/artifact/Vz1iDkkfzc7RZTa6fZdBiE

## Next 3 tasks
1. **Agent:** find replacement URLs for the 8 `broken` sources (P1 first: HCP 2026 note, nada.ins.tn, GCC-Stat labour publications) and the 11 `to-locate` items.
2. **Lead:** about 10 sources a day on the Verification Desk (55 P1 → ~6 days), then say "apply my verifications".
3. **Agent:** apply the link-report results (`collected` → `link-ok`/`broken`), locate the 11 `to-locate` items, and draft the indicator schema + the first pilot indicator (unemployment rate).

## Blockers / open questions
- The cloud sandbox network blocks statistical sites, so collection relies on web search and links are checked in CI.
- Record the chosen domain name and LinkedIn page for Miʿyar.
- Morocco is moving from the ENE to a redesigned survey in 2026. Confirm the new survey's official name and series start.
