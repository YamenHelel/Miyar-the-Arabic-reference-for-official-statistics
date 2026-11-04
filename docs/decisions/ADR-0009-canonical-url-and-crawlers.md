# ADR-0009: Canonical address and crawler policy

- **Date:** 2026-11-04 · **Status:** accepted (lead)

## Decision
- Canonical base URL: `https://yamenhelel.github.io/Miyar-the-Arabic-reference-for-official-statistics/` until a domain is chosen. It is set only in `tools/site/config.yaml`; switching domain means changing that value, adding a `CNAME` file and keeping the Pages URL as a redirect.
- All crawlers are allowed, AI crawlers explicitly included. The content is CC BY 4.0, and being read and cited by AI assistants is a project goal (PRD 16, GEO).

## Consequences
Every page carries a canonical link and appears in `sitemap.xml`. `robots.txt` lists the AI user agents by name (explicit allow), and `llms.txt` / `llms-full.txt` are published at the root.
