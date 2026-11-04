# مِعيار · Miʿyar: the Arabic reference for official statistics

[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-1d5c4a)](LICENSE) [![Code: MIT](https://img.shields.io/badge/code-MIT-1d5c4a)](LICENSE-CODE) [![Checks](https://github.com/YamenHelel/Miyar-the-Arabic-reference-for-official-statistics/actions/workflows/checks.yml/badge.svg)](https://github.com/YamenHelel/Miyar-the-Arabic-reference-for-official-statistics/actions/workflows/checks.yml)

**مِعيار** مرجع عربي مفتوح لتعاريف **إحصاءات العمل** الرسمية. يجمع التعريف الدولي لكل مؤشر، منسوخاً حرفياً من قرارات **المؤتمر الدولي لخبراء إحصاءات العمل (ICLS)** لدى **منظمة العمل الدولية**، ويضع بجانبه التعريف الذي يطبّقه كل جهاز إحصائي وطني في **تونس والسعودية والمغرب والأردن والإمارات وفلسطين**، مع **الولايات المتحدة والمملكة المتحدة وأستراليا وفرنسا** للمقارنة. كل نص رسمي يحمل مصدره وفقرته وتاريخ التحقق منه، وكل شرح كتبه الذكاء الاصطناعي موسوم بذلك.

**Miʿyar** is an open Arabic reference of official **labour-statistics definitions**. For each indicator (unemployment rate, labour force participation rate, employment-to-population ratio, youth unemployment, SDG 8.5.2), it quotes the **ILO / 19th ICLS** standard verbatim. It sets that next to the definition applied by national statistical offices in six Arab countries and four reference countries, and explains what makes the published figures comparable or not. Every official text carries its source, paragraph and verification date; AI-assisted explanations are always labelled.

- **Website:** https://yamenhelel.github.io/Miyar-the-Arabic-reference-for-official-statistics/ (beta)
- **For AI assistants:** [`llms.txt`](https://yamenhelel.github.io/Miyar-the-Arabic-reference-for-official-statistics/llms.txt) · a [Claude skill](skills/miyar-labour-stats/) generated from the same verified data
- **Status:** pilot, with 4 indicators, 8 glossary concepts and 123 registered sources (56 verified by a human). See [docs/STATUS.md](docs/STATUS.md).
- **Maintainer:** an independent Arab statistician working on AI for official statistics, with Claude as the main tool · contact yamen.hlel@gmail.com

### What you will find
| | |
|---|---|
| **Indicators** | معدل البطالة · معدل المشاركة في القوة العاملة · نسبة العمالة إلى السكان · معدل البطالة بين الشباب |
| **Official texts** | ILO 19th ICLS resolution (2013, amended 2023) §16, §27, §47, §73; national definitions from INS, GASTAT, HCP, DoS, FCSC, PCBS, BLS, ONS, ABS, Insee |
| **Glossary** | القوة العاملة، المشتغلون، المتعطلون، خارج القوة العاملة، القوة العاملة المحتملة، نقص التشغيل المرتبط بالوقت، الخطأ المعياري… with Arabic term variants by country |
| **Registry** | Every source document with its verification status ([sources/](sources/)) |

### How to cite
> مِعيار، «عنوان الصفحة»، الرابط، تاريخ الاطلاع. ترخيص CC BY 4.0.
> Miʿyar, "page title", URL, accessed date. CC BY 4.0.

To cite the repository, use GitHub's **"Cite this repository"** button ([CITATION.cff](CITATION.cff)).

---

## Summary

| # | Area | Where | What's inside |
|---|------|-------|---------------|
| 1 | **Start here** | [docs/STATUS.md](docs/STATUS.md) | Current phase, what is done, the next 3 tasks, blockers (1 page) |
| 2 | Index of project docs | [docs/00-index.md](docs/00-index.md) | One-line description of every document |
| 3 | Product Requirements (PRD) | [docs/prd/](docs/prd/) | Vision, users, scope, features, ideas backlog, architecture, data model, governance, business model, brand, partnerships, legal, KPIs, risks, naming |
| 4 | Daily progress log | [docs/CHANGELOG.md](docs/CHANGELOG.md) | Newest first; older months are in [docs/progress/](docs/progress/) |
| 5 | Decisions | [docs/decisions/](docs/decisions/) | Architecture Decision Records (ADR) |
| 6 | **Source registry** | [sources/README.md](sources/README.md) | Archived official sources: international bodies, 10 countries, SDGs, microdata |
| 7 | Practitioner directory | [directory/README.md](directory/README.md) | Opt-in directory of Arab labour statisticians (design and consent) |
| 8 | Content | [content/](content/) | Indicators, concepts and the shared store of official texts (`quotes.yml`) |
| 9 | Website | [tools/site/](tools/site/) | Generator, templates and design system (`python tools/build_site.py`) |
| 10 | Claude skill | [skills/miyar-labour-stats/](skills/miyar-labour-stats/) | Generated from the base; answers only from verified references |
| 11 | Tools | [tools/](tools/) | Validation, link checks, archiving, verification desk, quotes, site and skill builders |

## Licence and how to cite

Miʿyar's original content is licensed under **[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)**, and its code under the **[MIT License](LICENSE-CODE)**. You may share and adapt it, including commercially, as long as you give credit.

**Citation format:** «مِعيار — <عنوان الصفحة>، <الرابط>، تاريخ الاطلاع <التاريخ>»
*Miʿyar — <page title>, <URL>, accessed <date>.*

Quoted official texts (ILO, UN, national statistical offices…) remain under their publishers' own terms.

## Contact and corrections
Found an error, or want to contribute or review? Write to **yamen.hlel@gmail.com** or open a GitHub issue.

## Countries in phase 1

Arab: 🇹🇳 Tunisia · 🇸🇦 Saudi Arabia · 🇲🇦 Morocco · 🇯🇴 Jordan · 🇦🇪 UAE · 🇵🇸 Palestine
Reference (developed): 🇺🇸 USA · 🇬🇧 UK · 🇦🇺 Australia · 🇫🇷 France

## Principles (non-negotiable)

1. **Every fact has a source.** Official text is quoted, linked, archived and dated.
2. **Official text ≠ AI explanation.** AI-written explanations are always labelled as such.
3. **Human verification.** Nothing is marked `verified` unless a human reviewer has checked it against the source.
4. **Public metadata only.** No confidential microdata, ever.
5. **Arabic first** for users; English for internal project docs.
