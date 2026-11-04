# Instructions for AI agents (Claude, Codex, others)

Project: **Miʿyar (مِعيار) — the Arabic reference for official statistics**. Content licence: CC BY 4.0 · Code licence: MIT · Contact: yamen.hlel@gmail.com.

## Read order (to save tokens)
1. `docs/STATUS.md`: always read this first. It is short.
2. Read only the specific files the task needs. Use `docs/00-index.md` to find them.
3. Do NOT read the whole `sources/` tree or the full `docs/prd/` set unless the task requires it.

## Hard rules
- **Never invent a source, URL, definition, date or number.** If something is not found, write `status: to-locate` and say so.
- A URL taken from a search engine result without opening the page gets `status: collected`. It becomes `link-ok` only after an automated HTTP check passes, and `verified` only when the human lead has checked the content.
- Only the human lead sets `status: verified` (with `verified_by` and `verified_date`).
- Quote official definitions exactly, in their original language. An Arabic translation is marked `translation: unofficial` unless the publisher issued it.
- AI-written explanations go in fields named `explanation_ai_*` and are always shown labelled.
- No personal data in this repository. Practitioner directory entries live in the private store (see `directory/README.md`).
- No PDFs or other binaries in git. Store the URL plus an `archived_url` (Wayback Machine).
- Internal docs are in English. User-facing content (definitions, site) is in Arabic, with original-language quotes.

## End-of-session routine (every working session)
1. Add an entry at the top of `docs/CHANGELOG.md`: date, what was done, files touched, open questions.
2. Rewrite `docs/STATUS.md` (keep it to 1 page): phase, done, next 3 tasks, blockers.
3. Add any new idea to `docs/prd/05-ideas-backlog.md`, giving it the next free ID.
4. If a decision was made, add `docs/decisions/ADR-NNNN-*.md` and link it from `docs/00-index.md`.
5. On the first session of a new month, move the previous month's CHANGELOG entries to `docs/progress/YYYY-MM.md`.
6. Run `python tools/validate.py` before committing.

## Conventions
- Country codes: ISO 3166-1 alpha-3 lowercase (`tun`, `sau`, `mar`, `jor`, `are`, `pse`, `usa`, `gbr`, `aus`, `fra`).
- IDs: `src-<scope>-<short-slug>`, e.g. `src-ilo-icls19-res1`, `src-tun-ins-enpe-methodo`.
- Dates: ISO `YYYY-MM-DD`.
