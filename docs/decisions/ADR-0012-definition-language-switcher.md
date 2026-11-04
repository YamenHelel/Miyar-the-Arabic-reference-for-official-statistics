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

## Extended to country cards (2026-11-05, lead's request)
- The «مسح القوى العاملة» card on each country page has the same switch. The choice is shared with the definitions cards and carries across pages.
- The card's values are Miʿyar's own notes (not official text), so their renderings live in the country profile. They use `lfs_ar`, `lfs_en` (for French values only), `notes_ar`, `nso_ar` and `nso_en`, with `translation_by`. Each view carries a label saying so.
- The validator checks that the rendering keys match `lfs` and that `translation_by` is present. Queue 7b lists the 10 cards to review.
- When a profile value is corrected, its rendering must be corrected in the same edit.

## Extended to official text sheets (2026-11-05, lead's request)
- The `sheet()` macro (gold "official text" sheet) shows the switch whenever its quote has a translation in the other language. This covers ILO texts on indicator, concept and data-source pages, and any future slot (ISI and others) once translated.
- The hallmark now reads «النص الأصلي: نص رسمي مُتحقَّق منه…», so the verification stamp certifies the original, not the translation.
- The 4 ILO texts present now have unofficial Arabic translations: §47, §27, §16, §73(c). Each has a note that an official ILO Arabic text, once pasted, replaces the translation.
- Arabic list markers ((أ), (1), [ ) now keep their line breaks on display.
