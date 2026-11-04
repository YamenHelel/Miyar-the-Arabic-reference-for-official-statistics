# STATUS (read this first)

**Project:** مِعيار · Miʿyar, the Arabic reference for official statistics · **Licence:** CC BY 4.0
**Updated:** 2026-11-04 · **Phase:** 0a, Foundation · **Next phase:** 0b, Pilot content (10 indicators)

## Done
- Repo published on GitHub; structure, agent rules, PRD (15 files), ADRs 0001–0006
- Name (Miʿyar) and content licence (CC BY 4.0) decided
- Source registry v0: **112 records** (101 collected, 11 to-locate, 0 verified)
- Microdata access catalogue for the 10 countries; practitioner directory design
- Tools: `validate.py` (passing), `check_links.py`, `archive.py`; CI workflow

## Next 3 tasks
1. **Lead:** on GitHub, open Actions → "checks" → *Run workflow* to get the first link report (it is attached to the run as `link-report`).
2. **Lead:** verify P1 sources, about 10 per day, starting with `sources/international/ilo.yaml`.
3. **Agent:** apply the link-report results (`collected` → `link-ok`/`broken`), locate the 11 `to-locate` items, and draft the indicator schema + the first pilot indicator (unemployment rate).

## Blockers / open questions
- The cloud sandbox network blocks statistical sites, so collection relies on web search and links are checked in CI.
- Contact email for the directory form and corrections; code licence (MIT?); domain name and LinkedIn page.
- Morocco is moving from the ENE to a redesigned survey in 2026. Confirm the new survey's official name and series start.
