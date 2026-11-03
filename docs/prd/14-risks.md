# 14: Risk register

| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Wrong definition published (AI error or misreading) | M | **High** | Quote-only official text; status lifecycle; human verification; correction channel |
| R2 | Maintenance load exceeds 1h/day | **High** | High | Narrow scope; AI does drafting and collection; editorial board; automate link checks |
| R3 | Link rot (NSO sites change often) | **High** | M | Wayback archiving, weekly link check, `superseded_by` |
| R4 | Sources outdated after a methodology change (e.g. Morocco ENE → new survey 2026) | M | M | `date_accessed`; yearly re-check; monitoring (I-037) |
| R5 | Perceived as a vendor promotion (Claude) | M | M | Vendor-neutral content and licence; Claude framed as the tool, not the identity |
| R6 | NSO objects to how its practice is described | L | M | Neutral wording; quote their own documents; invite their focal point to review |
| R7 | Personal data breach (directory) | L | High | Private store, minimal fields, 2FA, no Git |
| R8 | Copyright complaint over quoted text | L | M | Short quotes, attribution, takedown process |
| R9 | Low adoption (users don't know it exists) | M | High | LinkedIn series, partnerships, AI-search optimisation, webinars |
| R10 | Someone copies the project | M | L | CC BY requires attribution; being first and the most up to date is the advantage |
| R11 | Sandboxed AI sessions cannot reach some sites | **High** | L | Search-based collection + CI link checks; lead checks blocked sites manually |
