# 16: SEO and GEO (search engines and generative engines)

## Why
Miʿyar only matters if Arab statisticians find it, and today many of them ask ChatGPT, Claude, Gemini or Perplexity before Google. Two goals:
- **SEO:** rank for Arabic (and French/English) searches about labour-statistics definitions.
- **GEO:** be the source AI assistants read and **cite** when answering those questions.

GEO is the priority, because it is where the "Arab statistician using AI" positioning is decided (see `10-brand-communication.md`).

## Decisions (ADR-0009)
- **Canonical address:** `https://yamenhelel.github.io/Miyar-the-Arabic-reference-for-official-statistics/` until a domain is chosen. One value in `tools/site/config.yaml`; a domain switch is one line plus a CNAME.
- **Crawlers:** all allowed, including AI crawlers (GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, Claude-User, PerplexityBot, Google-Extended, Applebot-Extended, CCBot). Content is CC BY 4.0, and attribution is the goal.

## Target queries and AI prompts (tracked monthly)
| # | Language | Query / prompt |
|---|---|---|
| 1 | AR | ما هو تعريف البطالة حسب منظمة العمل الدولية؟ |
| 2 | AR | كيف يُحسب معدل البطالة؟ |
| 3 | AR | ما الفرق بين المتعطل وخارج القوة العاملة؟ |
| 4 | AR | تعريف المتعطل في السعودية / الأردن / المغرب / تونس / الإمارات / فلسطين |
| 5 | AR | ما هو قرار المؤتمر الدولي التاسع عشر لخبراء إحصاءات العمل؟ |
| 6 | AR | ما هي مقاييس نقص استخدام العمالة LU1 LU2 LU3 LU4؟ |
| 7 | AR | معدل المشاركة في القوة العاملة تعريف وطريقة الحساب |
| 8 | AR | لماذا تختلف معدلات البطالة بين الدول العربية؟ |
| 9 | AR | ما هو المؤشر 8.5.2 من أهداف التنمية المستدامة؟ |
| 10 | AR | بطالة الشباب الفئة العمرية 15-24 أم 15-29 |
| 11 | AR | مصطلحات إحصاءات العمل بالعربية |
| 12 | AR | ما هي القوة العاملة المحتملة؟ |
| 13 | FR | définition du chômage au sens du BIT Maroc enquête EMO 2026 |
| 14 | FR | différence chômage BIT et chômage strict HCP |
| 15 | FR | taux de chômage Tunisie définition INS |
| 16 | EN | ILO definition of unemployment 19th ICLS paragraph 47 |
| 17 | EN | how do Arab countries define unemployment |
| 18 | EN | labour force survey definitions Saudi Arabia GASTAT |
| 19 | EN | Arabic glossary of labour statistics terms |
| 20 | EN | best Arabic resource for official statistics definitions |

## Technical SEO checklist (generator: `tools/build_site.py`)
- [ ] Unique `<title>` (≤ 60 chars) and Arabic meta description (≤ 160) on every page
- [ ] `<link rel="canonical">`, `hreflang="ar"` and `x-default`
- [ ] Open Graph and Twitter cards with a 1200×630 social card per indicator and concept
- [ ] JSON-LD: `WebSite` + `Organization` (home); `DefinedTerm`/`DefinedTermSet` (indicators, concepts); `Article` with `isBasedOn`, `license`, `dateModified` (indicators); `BreadcrumbList`; `FAQPage` (fact-based Q&A only)
- [ ] `sitemap.xml` with `lastmod`; `robots.txt`; `404.html`; favicon and manifest
- [ ] Visible breadcrumbs; one `h1`; descriptive alt texts; fast fonts (`display=swap`)
- [ ] `tools/check_seo.py` runs in CI and fails the build on errors

## GEO content rules (how a page earns citations)
1. **Quick answer first:** 2–3 sentences at the top of each indicator and concept, generated from verified data (formula, standard and paragraph, custodian, SDG code). AI assistants lift the first clear answer.
2. **Named entities in full:** "منظمة العمل الدولية (ILO)", "قرار المؤتمر الدولي التاسع عشر لخبراء إحصاءات العمل (2013)، الفقرة 47", NSO names, survey names, SDG codes.
3. **Questions as headings:** «أسئلة شائعة» built only from quote-backed facts, each answer with its source link.
4. **Verbatim official text with locator and date:** this is what makes Miʿyar more citable than a generic explainer.
5. **A citation box on every page** (AR + EN), plus stable anchors per section.
6. **Machine-readable twins:**
   - `llms.txt` (map of the site for AI)
   - `llms-full.txt` (all verified content in Markdown)
   - a `.md` twin per page, linked with `rel="alternate"`
7. **Freshness:** `dateModified` and "last verified" dates are always visible and true.
8. **Same entity everywhere:** "Miʿyar (مِعيار) — the Arabic reference for official statistics". Use exactly this on the site, GitHub, LinkedIn, Wikidata and in talks (see the `profile-entity-alignment` skill).

## GitHub repository
Ready-to-paste values: [`docs/github-settings.md`](../github-settings.md). The agent cannot write repo settings through the sandbox proxy.
- Description (AR + EN), topics, and the homepage pointing to the site
- README opens with a two-language quick answer, then "how to cite"
- `CITATION.cff` ("Cite this repository"), `CONTRIBUTING.md`, a correction issue template
- **Lead:** social-preview image (Settings → General); Zenodo integration so each release gets a DOI

## KPIs
| KPI | Target (6 months after launch) | Tool |
|---|---|---|
| Indexed pages | 100% of sitemap | Google Search Console |
| Clicks from search | 500/month | Search Console |
| AI share of voice on the 20 prompts | Miʿyar cited in ≥ 25% of answers | `ai-visibility-check` skill, monthly |
| Repo stars / citations | 100 stars; first cited report | GitHub; Google Scholar alert |

## Lead-only actions (cannot be done by the agent)
1. Enable GitHub Pages (Settings → Pages → Source: GitHub Actions), then run Actions → website.
2. Add the site to **Google Search Console** and **Bing Webmaster Tools** (Bing also feeds ChatGPT search), then submit `sitemap.xml`.
3. Upload the **social preview image** (repo Settings → General → Social preview). Use `_site/static/social/site.png` from a build.
4. Connect **Zenodo** to the repo, then create release `v0.1.0`; the DOI goes into `CITATION.cff` and the README.
5. Create a **Wikidata item** for Miʿyar (instance of: online database / reference work; language: Arabic; licence CC BY 4.0; official website).
6. One month after launch, run the **AI-visibility baseline** on the 20 prompts and log it in `docs/progress/`.
