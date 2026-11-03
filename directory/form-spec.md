# Form specification

## Tool
**Tally** (recommended: free tier, good RTL support, conditional logic, GDPR-oriented, CSV export) or Google Forms as a fallback. The account is owned by the lead and has 2FA.

## Layout (Arabic, RTL)
1. Intro: purpose, 3 lines, plus a link to the full consent text
2. Identity: name (AR/Latin), position, organisation, organisation type, country
3. Expertise: specialisations, years of experience, languages, LinkedIn
4. Contact: email
5. Participation: review / contribute / training interest
6. "What do you need most?" (free text; this is the demand survey)
7. Visibility: one public/private toggle per field (defaults from `schema.yaml`)
8. Consents: 3 checkboxes (processing is required)

## Validation
- Email format; LinkedIn URL must start with `https://www.linkedin.com/`.
- Country from the ISO list (Arab countries first, then others).
- No file uploads (minimisation).

## Export procedure (monthly)
1. Export CSV from the form tool to a local, private folder (never into the repo).
2. Run a filter script (to be written in Phase 1: `tools/directory_export.py`) that keeps only the rows with `consent_public_listing = true` and only the fields set to public. It writes `site/data/practitioners_public.json`.
3. Review the output by hand before publishing.
4. Log the export in the CHANGELOG (counts only, no names).

## Deletion requests
Delete the row in the form tool, re-run the export, republish the site, and confirm by email.
