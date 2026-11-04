# ADR-0012: Arabic/English switcher on national definitions, with unofficial translations

- **Date:** 2026-11-05 · **Status:** accepted (lead's request)

## Context
National definitions on indicator pages are quoted verbatim in each publisher's language (Arabic, English or French). Readers
wanted to read every card in one language.

## Decision
- Each national-definition card has a عربي / English switcher at its top. One choice applies to all cards and is remembered in
  the browser. Arabic is the default. Without JavaScript, the Arabic view shows.
- If the original is in the chosen language, the official text shows as it is.
- Otherwise a translation shows, stored in `content/quotes.yml` as `translation_ar` / `translation_en`, with these fields:
  - `translation_status`: `official` only when the publisher issued it, otherwise `unofficial`
  - `translation_by`
  - an optional `translation_note_ar`
- Unofficial translations are always labelled on the page. The original sits one click away (`details`), and stays the reference.
- When a publisher's own Arabic text is pasted (e.g. GASTAT, DoS Jordan), it replaces the unofficial Arabic translation.
- The validator requires `translation_status` and an original text. The validation queue lists unofficial translations (queue 7b). The Markdown twins and the skill carry them labelled UNOFFICIAL.

## Consequences
- 10 national definitions now read fully in Arabic and in English (AI-assisted translations, pending the lead's review).
- Official wording is unchanged; the quote store is still the only place for official text (ADR-0007).
