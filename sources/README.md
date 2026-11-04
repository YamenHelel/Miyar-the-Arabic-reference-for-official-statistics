# Source registry (سجل المصادر)

The registry of every official source the knowledge base relies on. Schema: [schema.yaml](schema.yaml). Lifecycle: [ADR-0004](../docs/decisions/ADR-0004-source-status-lifecycle.md).

## Layout
| Folder / file | Content | Records |
|---|---|---|
| [international/ilo.yaml](international/ilo.yaml) | ICLS resolutions (13th, 19th, 20th, 21st), ILOSTAT methods, LFS toolkit, SDG descriptions | 25 |
| [international/arab-regional.yaml](international/arab-regional.yaml) | ESCWA, AITRS, GCC-Stat, Arab Labour Organization, ERF, Arab Monetary Fund | 20 |
| [international/global-other.yaml](international/global-other.yaml) | UN SDG metadata, OECD, Eurostat, IPUMS, World Bank, IHSN, ISI glossary | 12 |
| [sdg/labour-sdg-indicators.yaml](sdg/labour-sdg-indicators.yaml) | Labour SDG metadata entry points + a reference table of 16 indicators | 6 |
| [countries/](countries/) | One file per country, with `profile` (survey facts) + `sources` | 49 |
| [microdata/puf-catalog.yaml](microdata/puf-catalog.yaml) | Access routes to LFS microdata per country | 11 entries |

Totals on 2026-11-04 after the first link check: **112 source records**: 61 `link-ok`, 32 `collected` (site blocks automated checks, so check by hand), 8 `broken`, 11 `to-locate`, 0 `verified`. 66 are priority P1.

## How to add a source
1. Pick the right file (country or organisation). Copy an existing record.
2. Give it a stable ID: `src-<scope>-<slug>`.
3. Set `status: collected` (or `to-locate` with `url: TO-LOCATE`).
4. Run `python tools/validate.py`.
5. Run `python tools/archive.py` to get a Wayback snapshot, and fill in `archived_url`.

## Link checks
GitHub Actions → **checks** → *Run workflow* (it also runs every Monday). The report is shown in the run's summary. To apply it:
`python tools/apply_link_report.py <report.md> --date YYYY-MM-DD`. A 403 usually means the site blocks bots, not that the page is gone.

## How to verify a source (lead's daily task)
Use the **Verification Desk** page: https://claude.ai/artifact/Vz1iDkkfzc7RZTa6fZdBiE (private, owner-only saves). It lists every source still to check (P1 first). For each one, open it, check it, and click ✅ / ⚠️ / ❌ / ⏭. Then tell Claude "apply my verifications". The manual method below is the fallback.

Open the URL, then check the title, publisher, date and edition, and that it is the latest one. Then set:
```yaml
status: verified
verified_by: <initials>
verified_date: 2026-11-04
```
If a newer edition exists, add it and set `superseded_by` on the old record.

## Known gaps (to-locate)
- ILO: Arabic versions of the ICLS resolutions; exact URL of the 19th ICLS resolution PDF.
- AITRS Arabic statistical glossary; ALO latest statistical yearbook; Arab Monetary Fund labour data; OECD glossary's current location.
- Tunisia: latest ENPE questionnaire and the quarterly release page.
- Jordan: DoS methodology document and the quarterly release page.
- UAE: LFS methodology/metadata.
- Australia: current LFS methodology page.

## Caveat on this first collection
Built on 2026-11-03 from web search results, because the cloud sandbox could not open statistical sites directly. Some URLs were **inferred** (noted in `notes`: e.g. `nada.ins.tn`, `uaestat.fcsc.gov.ae`, the ILO Survey Library base, the ONS user-guidance URL). The CI link check and the human verification will confirm or correct them.
