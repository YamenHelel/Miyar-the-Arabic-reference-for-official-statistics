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
6. Run `python tools/validate.py` and `python tools/build_validation_queue.py` (rewrites `docs/VALIDATION.md`; CI fails if it is stale) before committing.
   Update `docs/IMPLEMENTATION.md` (built vs validated per module).
7. When the lead says "apply my verifications" (or at session start if verdicts exist): export the Verification Desk verdicts
   (`ArtifactData` list, collection `verdicts`, url https://claude.ai/artifact/Vz1iDkkfzc7RZTa6fZdBiE, out_dir in scratchpad), run
   `python tools/apply_verification.py <out_dir>/verdicts`, then delete the applied `ok`/`broken` verdict docs and act on `fix` notes
   (delete each `fix` verdict once handled so the item returns to the queue). Rebuild the page with
   `python tools/build_verification_page.py <scratchpad>/verification-desk.html` and republish it to the same URL.
8. When the lead says "apply my quotes": export the desk's `quotes` collection (ArtifactData list, out_dir), run
   `python tools/apply_quotes.py <out_dir>/quotes`, delete the applied quote docs, validate, rebuild both the desk and the
   indicator preview (`python tools/build_indicator_page.py <ind-id> <scratchpad>/<ind-id>.html`, republish to its URL in STATUS.md).
9. After a CI link check, apply it with `python tools/apply_link_report.py` (read the report from the run log with `gh run view <id> --log`); pass `--keep <ids>` for sources
   queued for a hand check so a robot 404 does not mark them broken again.

## Content (content/)
- Official wording ONLY in `content/quotes.yml` (ADR-0007), pasted verbatim by a human from a verified source; indicators
  (`content/indicators/`), concepts (`content/concepts/`) and data sources (`content/data-sources/`, ADR-0011; ILO first) reference slots by id. Schemas: `content/schema-*.yaml`.
- Numbers used by the site's ruler (`measures:`) must be read from verified/pasted quotes only.
- After any content change: `python tools/build_site.py` (website), `python tools/build_skill.py` (Claude skill, commit the output),
  and refresh the private previews (`tools/prepare_site_preview.py`, URLs in STATUS.md).
- Design changes: follow ADR-0008 and re-run the tasteskill gate (`lint.mjs`, `inspect.mjs`) on `_site/`.
- SEO/GEO (PRD 16, ADR-0009):
  - The base URL lives only in `tools/site/config.yaml`.
  - Builders: `tools/seo.py` (JSON-LD, quick answers, quote-backed FAQ, robots, sitemap, llms.txt); `tools/build_social_cards.mjs` (OG images).
  - After building, run `python tools/check_seo.py` (add `--skip-images` without social cards).
  - Quick answers and FAQ must stay deterministic and quote-backed: never add free AI prose there.
- The sandbox cannot reach statistical sites (WebFetch too), so never fill a quote yourself: create a `to-paste` slot with a precise `locator` and `what_ar`.
- A screenshot from the lead is a valid source: transcribe exactly, set `status: pasted` and a `document_note`, and let the lead confirm.

## Code library (code/, ADR-0010)
- Python is the reference: run `python tools/test_code.py` after any change. `.github/workflows/code.yml` checks that R matches.
- Presets are generated: `python tools/build_code_presets.py`. Never hand-edit `code/presets/countries.json`.
- Never commit real microdata. Only the synthetic file is allowed.

## Conventions
- Country codes: ISO 3166-1 alpha-3 lowercase (`tun`, `sau`, `mar`, `jor`, `are`, `pse`, `usa`, `gbr`, `aus`, `fra`).
- IDs: `src-<scope>-<short-slug>`, e.g. `src-ilo-icls19-res1`, `src-tun-ins-enpe-methodo`.
- Dates: ISO `YYYY-MM-DD`.
