# ADR-0004: Source status lifecycle, and no binaries in git

- **Date:** 2026-11-03 · **Status:** accepted

## Lifecycle
| Status | Meaning | Who sets it |
|---|---|---|
| `to-locate` | The source is known or likely to exist, but no URL has been found yet | agent or human |
| `collected` | URL found (e.g. through search results) but not yet fetched or checked | agent |
| `link-ok` | Automated HTTP check returned 2xx/3xx on the last run | `tools/check_links.py` |
| `broken` | Last automated check failed (4xx/5xx/timeout) | `tools/check_links.py` |
| `verified` | A human opened the source and confirmed title, publisher, date and relevance | **human lead only** |
| `superseded` | Replaced by a newer edition (keep it for history; point `superseded_by`) | human |

## No binaries
PDFs and other files are not committed (copyright, repo size). Each record keeps `url` and `archived_url` (Internet Archive), and optionally `sha256` of the downloaded file to detect silent changes.

## Context note (2026-11-03)
The first collection session ran in a cloud sandbox whose network policy blocked direct access to statistical sites. All URLs were therefore collected from web search results (`status: collected`). The link check runs in GitHub Actions instead (`.github/workflows/checks.yml`).
