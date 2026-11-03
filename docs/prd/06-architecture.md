# 06: Architecture

```
                  ┌───────────────────────────────────────────┐
                  │  GitHub repo: single source of truth      │
                  │  sources/*.yaml   content/indicators/*.yml │
                  │  content/concepts/*.yml   docs/            │
                  └───────────────┬───────────────────────────┘
                  validate.py · check_links.py · archive.py (CI)
          ┌───────────────────────┼─────────────────────────┬──────────────────┐
          ▼                       ▼                         ▼                  ▼
  Quarto website (RTL AR)   Claude skill (SKILL.md     MCP server (P2)    Exports (P2)
  GitHub Pages + domain     + generated reference      search / get       JSON, CSV, SDMX-like
  main channel              files) — Codex/others      indicator/concept  for partners
```

## Components
| Component | Tech | Phase | Notes |
|---|---|---|---|
| Content store | YAML + Markdown in Git | 0 | Human-readable, diffable and cheap for AI to read |
| Validation | Python (`pyyaml`, `jsonschema`) | 0 | Run locally and in CI |
| Link check and archive | Python (`requests`) + Wayback "Save Page Now" | 0 | Weekly CI job opens an issue listing broken links |
| Website | **Quarto** (RTL, Arabic fonts such as Noto Naskh Arabic / IBM Plex Sans Arabic) | 0b–1 | Pages generated from YAML through templates; static, free hosting |
| Search | Client-side (Quarto search or Pagefind) with Arabic normalisation | 1 | No server needed |
| Claude skill | `SKILL.md` + reference files generated from YAML | 0b–1 | The skill reads the indexes first, then single entries |
| MCP server | Python or TypeScript, read-only over the YAML/JSON export | 2 | Tools: `search`, `get_indicator`, `get_concept`, `compare_countries`, `list_sources` |
| Analytics | Privacy-friendly (Plausible / GoatCounter) | 1 | KPIs in `13-metrics-kpis.md` |
| Forms | Tally / Google Forms | 1 | Directory and corrections |

## Folder plan (future)
```
content/indicators/<id>.yml     # one indicator per file
content/concepts/<id>.yml
content/terms/<id>.yml          # term variants
site/                           # Quarto project, templates
skills/claude/                  # generated skill package
mcp/                            # MCP server
```

## Design choices
- **Static first:** no database and no server in phases 0–1. Cost ≈ domain name only.
- **Generated, never hand-copied:** the site and skills are build outputs of the YAML.
- **Token efficiency:** each entity is one small file; index files list IDs and titles, so agents read the index and then fetch one file.
