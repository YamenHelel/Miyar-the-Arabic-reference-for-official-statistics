# Index of project documents

Read [STATUS.md](STATUS.md) first. Each document below has a one-line description so you can open only what you need.

## Progress
- [STATUS.md](STATUS.md): 1-page snapshot of the current phase, what is done, the next 3 tasks and blockers.
- [CHANGELOG.md](CHANGELOG.md): daily log for the current month, newest first.
- [progress/](progress/): archived monthly logs (`YYYY-MM.md`).

## Product Requirements Document (PRD)
| File | Content |
|------|---------|
| [prd/01-vision-goals.md](prd/01-vision-goals.md) | Vision, problem, positioning, long-term goals, definition of success |
| [prd/02-users-personas.md](prd/02-users-personas.md) | Target users, personas, jobs-to-be-done, typical questions |
| [prd/03-scope-phases-roadmap.md](prd/03-scope-phases-roadmap.md) | Phases 0–4, exit criteria, country/domain expansion order, 1h/day plan |
| [prd/04-features-current.md](prd/04-features-current.md) | Features in scope now (MVP): indicator pages, glossary, comparisons, registry |
| [prd/05-ideas-backlog.md](prd/05-ideas-backlog.md) | **All future ideas**, with ID, priority and target phase |
| [prd/06-architecture.md](prd/06-architecture.md) | Single source of truth → website + AI skills + MCP; hosting; CI |
| [prd/07-data-model.md](prd/07-data-model.md) | Schemas: indicator, concept, country implementation, source, term, practitioner |
| [prd/08-quality-governance.md](prd/08-quality-governance.md) | Verification workflow, statuses, editorial board, citation and AI labelling |
| [prd/09-business-model.md](prd/09-business-model.md) | Free core and paid services (training, consulting), pricing ideas |
| [prd/10-brand-communication.md](prd/10-brand-communication.md) | Positioning, LinkedIn plan, launch events, visibility in AI search |
| [prd/11-partnerships.md](prd/11-partnerships.md) | ILO, ESCWA, AITRS, GCC-Stat, ALO, ERF, NSOs: what to offer and ask |
| [prd/12-legal-privacy.md](prd/12-legal-privacy.md) | Copyright and attribution, data-protection laws, consent |
| [prd/13-metrics-kpis.md](prd/13-metrics-kpis.md) | KPIs and how they are measured |
| [prd/14-risks.md](prd/14-risks.md) | Risk register with mitigations |
| [prd/15-naming.md](prd/15-naming.md) | Name decision (Miʿyar), options considered, remaining checks |

## Decisions (ADR)
- [ADR-0001](decisions/ADR-0001-repo-and-single-source-of-truth.md): GitHub repo as the single source of truth
- [ADR-0002](decisions/ADR-0002-languages.md): English internal docs, Arabic user content
- [ADR-0003](decisions/ADR-0003-practitioner-directory-privacy.md): directory uses an opt-in form and private storage
- [ADR-0004](decisions/ADR-0004-source-status-lifecycle.md): source status lifecycle and no binaries in git
- [ADR-0005](decisions/ADR-0005-licensing.md): licences: CC BY 4.0 for content, MIT for code (accepted)
- [ADR-0006](decisions/ADR-0006-name-miyar.md): project name Miʿyar (مِعيار)
- [ADR-0007](decisions/ADR-0007-shared-quotes-store.md): one shared quotes store (`content/quotes.yml`)
- [ADR-0008](decisions/ADR-0008-site-generator-and-design.md): website generator (jinja2) and the Miʿyar design system

## Data
- [../content/quotes.yml](../content/quotes.yml): all official wording (shared store); schemas `content/schema-*.yaml`
- [../content/indicators/](../content/indicators/) and [../content/concepts/](../content/concepts/): indicators and glossary
- [../tools/site/](../tools/site/): website templates and design system · [../skills/miyar-labour-stats/](../skills/miyar-labour-stats/): generated Claude skill
- [../sources/README.md](../sources/README.md): source registry guide and counts
- [../directory/README.md](../directory/README.md): practitioner directory design
