# STATUS (read this first)

**Updated:** 2026-11-03 · **Phase:** 0a, Foundation · **Next phase:** 0b, Pilot content (10 indicators)

## Done
- Repo structure, agent rules (`CLAUDE.md`), PRD (15 files), 5 ADRs
- Source registry v0: **112 records** (101 collected, 11 to-locate, 0 verified), covering the ILO, Arab regional bodies, global bodies, labour SDGs and 10 countries
- Microdata access catalogue for the 10 countries
- Practitioner directory design (schema, AR/EN consent, form spec)
- Tools: `validate.py` (passing), `check_links.py`, `archive.py`; CI workflow

## Next 3 tasks
1. **Lead:** create the GitHub repo and share owner/name → agent pushes; the CI link check runs.
2. **Lead:** verify P1 sources, about 10 per day (start with `international/ilo.yaml`, then the Arab countries). Decide the licence (ADR-0005) and a name (`prd/15-naming.md`).
3. **Agent:** apply the link-report results; archive URLs; locate the 11 `to-locate` items; draft the indicator schema and the first pilot indicator (unemployment rate).

## Blockers / open questions
- The cloud sandbox network blocks statistical sites. Collection uses web search, and link checks run in CI. Option: allow the hosts in the environment's network settings.
- Morocco is moving from the ENE to a redesigned survey in 2026. Confirm the new survey's official name and series start.
- Is the lead's own email or a project email used for the directory form and corrections?
