# Validation queue (generated, do not edit)

Everything in Miʿyar that still needs a human check, in the order the lead should work through it.
Regenerate with `python tools/build_validation_queue.py` (part of the end-of-session routine).
Where to act: the **Verification Desk** (link in `docs/STATUS.md`): ✍️ tab for quotes, sources tab for links.

## Summary

| Queue | Items | Where |
|---|---|---|
| 1. Official texts to paste | 71 | Desk ✍️ tab, then say "apply my quotes" |
| 2. Pasted texts to confirm | 1 | Desk ✍️ tab (or tell Claude "confirmed") |
| 3. Sources to open and check | 60 | Desk sources tab, then "apply my verifications" |
| 4. Sources still missing or broken | 14 | Find a URL or confirm it does not exist |
| 5. Country facts from search snippets | 15 | Confirmed automatically once the country's text is pasted |
| 6. Country-profile fields to confirm | 20 | Reply in chat or edit the YAML |
| 7. AI-drafted pages awaiting review | 54 | Read the page; say "reviewed <id>" or send corrections |
| 7b. Unofficial translations to review | 10 definitions + 10 country cards | Read each against its original (عربي / English switcher on indicator and country pages) |
| 8. Code not yet executed | 1 | Stata script (needs someone with Stata) |
| 9. Lead decisions and settings | 7 | See the list at the end |

## 1. Official texts to paste

Grouped by document, so one opened document serves several texts. Paste verbatim, in the original language.

### ISI Multilingual Glossary of Statistical Terms (33)
`src-isi-glossary` · https://www.isi-web.org/glossary

- `q-isi-standard-error` → used by con-standard-error. **Copy:** ISI glossary — entry 'standard error' (English, and the Arabic term if listed)
- `q-isi-mean` → used by con-mean. **Copy:** ISI Multilingual Glossary — entry 'Arithmetic mean' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-weighted-mean` → used by con-weighted-mean. **Copy:** ISI Multilingual Glossary — entry 'Weighted mean' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-median` → used by con-median. **Copy:** ISI Multilingual Glossary — entry 'Median' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-mode` → used by con-mode. **Copy:** ISI Multilingual Glossary — entry 'Mode' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-range` → used by con-range. **Copy:** ISI Multilingual Glossary — entry 'Range' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-variance` → used by con-variance. **Copy:** ISI Multilingual Glossary — entry 'Variance' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-standard-deviation` → used by con-standard-deviation. **Copy:** ISI Multilingual Glossary — entry 'Standard deviation' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-coefficient-of-variation` → used by con-coefficient-of-variation. **Copy:** ISI Multilingual Glossary — entry 'Coefficient of variation' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-percentile` → used by con-percentile. **Copy:** ISI Multilingual Glossary — entry 'Percentile and quartiles' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-interquartile-range` → used by con-interquartile-range. **Copy:** ISI Multilingual Glossary — entry 'Interquartile range' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-outlier` → used by con-outlier. **Copy:** ISI Multilingual Glossary — entry 'Outlier' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-population` → used by con-population. **Copy:** ISI Multilingual Glossary — entry 'Population (statistical)' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-sample` → used by con-sample. **Copy:** ISI Multilingual Glossary — entry 'Sample' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-sampling-frame` → used by con-sampling-frame. **Copy:** ISI Multilingual Glossary — entry 'Sampling frame' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-simple-random-sampling` → used by con-simple-random-sampling. **Copy:** ISI Multilingual Glossary — entry 'Simple random sampling' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-stratified-sampling` → used by con-stratified-sampling. **Copy:** ISI Multilingual Glossary — entry 'Stratified sampling' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-cluster-sampling` → used by con-cluster-sampling. **Copy:** ISI Multilingual Glossary — entry 'Cluster sampling' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-sampling-weight` → used by con-sampling-weight. **Copy:** ISI Multilingual Glossary — entry 'Sampling weight' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-non-response` → used by con-non-response. **Copy:** ISI Multilingual Glossary — entry 'Non-response' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-response-rate` → used by con-response-rate. **Copy:** ISI Multilingual Glossary — entry 'Response rate' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-estimate` → used by con-estimate. **Copy:** ISI Multilingual Glossary — entry 'Estimate' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-sampling-error` → used by con-sampling-error. **Copy:** ISI Multilingual Glossary — entry 'Sampling error' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-non-sampling-error` → used by con-non-sampling-error. **Copy:** ISI Multilingual Glossary — entry 'Non-sampling error' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-confidence-interval` → used by con-confidence-interval. **Copy:** ISI Multilingual Glossary — entry 'Confidence interval' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-margin-of-error` → used by con-margin-of-error. **Copy:** ISI Multilingual Glossary — entry 'Margin of error' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-design-effect` → used by con-design-effect. **Copy:** ISI Multilingual Glossary — entry 'Design effect' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-bias` → used by con-bias. **Copy:** ISI Multilingual Glossary — entry 'Bias' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-rate` → used by con-rate. **Copy:** ISI Multilingual Glossary — entry 'Rate' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-ratio` → used by con-ratio. **Copy:** ISI Multilingual Glossary — entry 'Ratio and proportion' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-percentage-point` → used by con-percentage-point. **Copy:** ISI Multilingual Glossary — entry 'Percentage point' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-index-number` → used by con-index-number. **Copy:** ISI Multilingual Glossary — entry 'Index number' (if missing: OECD Glossary of Statistical Terms)
- `q-isi-seasonal-adjustment` → used by con-seasonal-adjustment. **Copy:** ISI Multilingual Glossary — entry 'Seasonal adjustment' (if missing: OECD Glossary of Statistical Terms)

### Resolution concerning statistics of work, employment and labour underutilization (19th ICLS, 2013) — PDF, as amended by the 21st ICLS (2023) (7)
`src-ilo-icls19-res1-pdf` · https://www.ilo.org/sites/default/files/wcmsp5/groups/public/@dgreports/@stat/documents/normativeinstrument/wcms_230304.pdf

- `q-ilo-working-age` → used by ind-employment-to-population-ratio, ind-labour-force-participation-rate, con-working-age-population. **Copy:** 19th ICLS resolution — paragraph setting the working-age population and its lower age limit (section on population coverage)
- `q-ilo-potential-lf` → used by con-potential-labour-force. **Copy:** 19th ICLS resolution — paragraph defining the 'potential labour force' (§51 approx.)
- `q-ilo-time-related-underemployment` → used by con-time-related-underemployment. **Copy:** 19th ICLS resolution — paragraph defining 'persons in time-related underemployment' (§43 approx.)
- `q-ilo-headline-73ab` → used by ind-employment-to-population-ratio, ind-labour-force-participation-rate. **Copy:** 19th ICLS resolution — paragraph 73 items (a) and (b) (labour force participation rate; employment-to-population ratio)
- `q-ilo-icls19-data-sources` → used by ds-labour-force-survey. **Copy:** 19th ICLS resolution I — the paragraph(s) on data sources in the part on the national programme of work statistics (search the PDF for "administrative records" or "establishment surveys"): the text naming household surveys, population censuses, establishment surveys and administrative records
- `q-ilo-icls19-lfs-frequency` → used by ds-lfs-periodicity. **Copy:** 19th ICLS resolution I — the paragraph recommending how often labour force statistics should be collected and published (search the PDF for "frequency", "sub-annual" or "monthly or quarterly")
- `q-ilo-icls19-reference-period` → used by ds-lfs-framework. **Copy:** 19th ICLS resolution I — the paragraph defining the short reference period (one week or seven days) for measuring employment and labour underutilization (search the PDF for "short reference period")

### Quick guide on sources and uses of labour statistics (ILO, 2017) (4) ⚠️ source is `collected`: verify the document first
`src-ilo-quick-guide-sources-uses` · https://researchrepository.ilo.org/esploro/outputs/encyclopediaEntry/Quick-guide-on-sources-and-uses/995219003402676

- `q-ilo-qg-lfs` → used by ds-labour-force-survey. **Copy:** Quick guide on sources and uses of labour statistics — section on household-based surveys / labour force surveys: the description and the listed advantages and disadvantages
- `q-ilo-qg-census` → used by ds-population-census. **Copy:** Quick guide on sources and uses of labour statistics — section on population censuses: description, advantages and disadvantages
- `q-ilo-qg-admin` → used by ds-administrative-records. **Copy:** Quick guide on sources and uses of labour statistics — section on administrative records: description, advantages and disadvantages
- `q-ilo-qg-establishment` → used by ds-establishment-survey. **Copy:** Quick guide on sources and uses of labour statistics — section on establishment surveys: description, advantages and disadvantages

### FCSC — labour force data file with Arabic definitions (xlsx, 2025) (3)
`src-are-lfs-methodology` · https://fcsc.gov.ae/wp-content/uploads/2025/06/%D8%A7%D9%84%D8%B9%D9%84%D8%A7%D9%82%D8%A9-%D8%A8%D9%82%D9%88%D8%A9-%D8%A7%D9%84%D8%B9%D9%85%D9%84-ar.xlsx

- `q-are-lfpr` → used by ind-labour-force-participation-rate:are. **Copy:** FCSC labour force data file — definitions sheet — definition of the labour force participation rate
- `q-are-epr` → used by ind-employment-to-population-ratio:are. **Copy:** FCSC labour force data file — definitions sheet — definition of the employment-to-population ratio
- `q-are-yur` → used by ind-youth-unemployment-rate:are. **Copy:** FCSC labour force data file — definitions sheet — definition of the youth unemployment rate (and the youth age band used)

### DoS — Employment and unemployment: labour force concepts page (3)
`src-jor-dos-methodology` · https://dosweb.dos.gov.jo/labourforce/employment-and-unemployment/

- `q-jor-lfpr` → used by ind-labour-force-participation-rate:jor. **Copy:** DoS employment and unemployment concepts page — definition of the labour force participation rate
- `q-jor-epr` → used by ind-employment-to-population-ratio:jor. **Copy:** DoS employment and unemployment concepts page — definition of the employment-to-population ratio
- `q-jor-yur` → used by ind-youth-unemployment-rate:jor. **Copy:** DoS employment and unemployment concepts page — definition of the youth unemployment rate (and the youth age band used)

### HCP — Note d'information sur la situation du marché du travail au Maroc au troisième trimestre 2026 selon l'Enquête sur la Main-d'Œuvre (EMO) (3)
`src-mar-hcp-chomage-strict` · https://www.hcp.ma/attachment/2927551/

- `q-mar-lfpr` → used by ind-labour-force-participation-rate:mar. **Copy:** HCP note d'information EMO T3 2026 — encadré définitions — definition of the labour force participation rate
- `q-mar-epr` → used by ind-employment-to-population-ratio:mar. **Copy:** HCP note d'information EMO T3 2026 — encadré définitions — definition of the employment-to-population ratio
- `q-mar-yur` → used by ind-youth-unemployment-rate:mar. **Copy:** HCP note d'information EMO T3 2026 — encadré définitions — definition of the youth unemployment rate (and the youth age band used)

### PCBS — Guide to the statistical indicators provided by PCBS, 2025 (book2740) (3)
`src-pse-pcbs-book2740` · https://www.pcbs.gov.ps/media/qznfsoov/book2740.pdf

- `q-pse-lfpr` → used by ind-labour-force-participation-rate:pse. **Copy:** PCBS indicators guide 2025 (book2740) — indicators table — definition of the labour force participation rate
- `q-pse-epr` → used by ind-employment-to-population-ratio:pse. **Copy:** PCBS indicators guide 2025 (book2740) — indicators table — definition of the employment-to-population ratio
- `q-pse-yur` → used by ind-youth-unemployment-rate:pse. **Copy:** PCBS indicators guide 2025 (book2740) — indicators table — definition of the youth unemployment rate (and the youth age band used)

### Methodology of Labor Market Statistics — Q1 2025 (EN) (3)
`src-sau-gastat-lms-methodology-2025q1` · https://www.stats.gov.sa/documents/d/guest/methodology-of-labor-market-statistics-q1-2025-en

- `q-sau-lfpr` → used by ind-labour-force-participation-rate:sau. **Copy:** GASTAT Methodology of Labor Market Statistics Q1 2025 — definitions section 2.3.1 — definition of the labour force participation rate
- `q-sau-epr` → used by ind-employment-to-population-ratio:sau. **Copy:** GASTAT Methodology of Labor Market Statistics Q1 2025 — definitions section 2.3.1 — definition of the employment-to-population ratio
- `q-sau-yur` → used by ind-youth-unemployment-rate:sau. **Copy:** GASTAT Methodology of Labor Market Statistics Q1 2025 — definitions section 2.3.1 — definition of the youth unemployment rate (and the youth age band used)

### Methodological note — Employment survey Tunisia (3)
`src-tun-ins-enpe-methodo` · https://ins.tn/sites/default/files-ftp3/files/publication/pdf/Note%20M%C3%A9thodologique%20Enquete%20emploi%20Tunisie.pdf

- `q-tun-lfpr` → used by ind-labour-force-participation-rate:tun. **Copy:** Note méthodologique INS — definition of the labour force participation rate
- `q-tun-epr` → used by ind-employment-to-population-ratio:tun. **Copy:** Note méthodologique INS — definition of the employment-to-population ratio
- `q-tun-yur` → used by ind-youth-unemployment-rate:tun. **Copy:** Note méthodologique INS — definition of the youth unemployment rate (and the youth age band used)

### ILO guidelines and tools for aligning national LFS with latest ICLS standards and best practices (English page) (1) ⚠️ source is `collected`: verify the document first
`src-ilo-aligning-lfs-icls-en` · https://ilostat.ilo.org/resources/ilo-guidelines-and-tools-for-aligning-national-labour-force-surveys-with-latest-icls-standards-and-best-practices/

- `q-ilo-aligning-sample` → used by ds-lfs-sample-design. **Copy:** ILO guidelines and tools for aligning national LFS — the section or item on sample design (survey phase: design). If the hub has no text on sampling, set status source-missing

### ILO LFS toolkit — model questionnaires (CAPI 2024 edition), adaptation guides, derivation syntax (1)
`src-ilo-lfs-toolkit` · https://ilostat.ilo.org/resources/lfs-toolkit/

- `q-ilo-lfs-toolkit-model` → used by ds-lfs-questionnaire. **Copy:** ILO LFS toolkit page — the introductory description of the model LFS questionnaire (CAPI edition): what it covers and how countries should adapt it

### ILOSTAT Microdata Processing Quick Guide — principles and methods for processing anonymized household survey microdata (1) ⚠️ source is `link-ok`: verify the document first
`src-ilo-microdata-quick-guide` · https://www.ilo.org/publications/ilostat-microdata-processing-quick-guide-principles-and-methods-underlying

- `q-ilo-microdata-weights` → used by ds-lfs-weighting-estimation. **Copy:** ILOSTAT Microdata Processing Quick Guide — the paragraph on survey weights (how ILO uses the national weights when deriving indicators)

### Sources and Methods: Labour Statistics, Volume 2 — Employment, wages, hours of work and labour cost (establishment surveys) (1) ⚠️ source is `collected`: verify the document first
`src-ilo-ssm2-establishment-surveys` · https://webapps.ilo.org/ilostat-files/SSM/SSM2_NEW/E/main.html

- `q-ilo-ssm2-establishment-intro` → used by ds-establishment-survey. **Copy:** ILO Sources and Methods vol. 2 — Introduction: the paragraph describing establishment surveys and what they measure (employment, earnings, hours, labour cost)

### Sources and Methods: Labour Statistics, Volume 4 — Employment, unemployment, wages and hours of work (administrative records and related sources) (1) ⚠️ source is `collected`: verify the document first
`src-ilo-ssm4-admin-records` · https://webapps.ilo.org/ilostat-files/SSM/SSM4A/E/INTRO.html

- `q-ilo-ssm4-admin-intro` → used by ds-administrative-records. **Copy:** ILO Sources and Methods vol. 4 — Introduction: the paragraph describing administrative records as a source of labour statistics and their limits for international comparison

### ILOSTAT — WORK database description (19th ICLS) (1)
`src-ilo-work-db-description` · https://ilostat.ilo.org/databases/work/description/

- `q-ilo-work-db-comparability` → used by ds-lfs-quality. **Copy:** ILOSTAT WORK database description — the paragraph explaining why statistics based on the 19th ICLS are not comparable with those based on the 13th ICLS (LFS database)

### UN SDG metadata — Goal 8 (decent work and economic growth) (1)
`src-sdg-goal8-metadata` · https://unstats.un.org/sdgs/metadata/?Goal=8

- `q-sdg-852-youth` → used by ind-youth-unemployment-rate. **Copy:** SDG metadata 8.5.2 — 'Definition' and 'Disaggregation' sections (age groups, youth 15–24)

### Principles and Recommendations for Population and Housing Censuses, Revision 3 (UN, 2017) (1) ⚠️ source is `collected`: verify the document first
`src-un-census-pr-rev3` · https://unstats.un.org/unsd/publication/seriesM/Series_M67Rev3en.pdf

- `q-un-census-definition` → used by ds-population-census. **Copy:** UN Principles and Recommendations for Population and Housing Censuses, Rev.3 — Part one, the paragraph that begins "A population census is …" (definition) and, if separate, the paragraph listing its essential features

### Measuring the Economically Active in Population Censuses: A Handbook (UN and ILO, 2010) (1) ⚠️ source is `collected`: verify the document first
`src-un-ilo-census-economically-active-handbook` · https://unstats.un.org/unsd/publication/seriesf/Seriesf_102e.pdf

- `q-un-ilo-census-vs-lfs` → used by ds-population-census. **Copy:** UN/ILO handbook (2010) — the paragraph comparing the population census with labour force surveys as sources on the economically active population (introduction or first chapter)

## 2. Pasted texts awaiting confirmation

- `q-pse-unemployed` (ind-unemployment-rate:pse): Transcribed by Claude from the lead's screenshot of the table cell (line breaks were cell wrapping); spelling kept as printed, including «خلال ل 4» and «الاسناد/الأسناد». Lead to confirm on the desk.

## 3. Sources to open and check

| id | title | status | last robot check |
|---|---|---|---|
| `src-gccstat-labour-publications` | Labour statistics in the GCC countries (publication series) | collected (P1) | 2026-11-04 404 |
| `src-ilo-admin-data-sources` | ILOSTAT — Administrative data sources for labour statistics (resources page) | collected (P1) | — |
| `src-ilo-aligning-lfs-icls-en` | ILO guidelines and tools for aligning national LFS with latest ICLS standards and best pra | collected (P1) | 2026-11-04 403 |
| `src-ilo-establishment-surveys-resources` | ILOSTAT — Establishment surveys for labour statistics (resources page) | collected (P1) | — |
| `src-ilo-quick-guide-sources-uses` | Quick guide on sources and uses of labour statistics (ILO, 2017) | collected (P1) | — |
| `src-mar-hcp-ene-to-emo-2026-note` | Technical note (May 2026) — transition from ENE to the redesigned employment survey | collected (P1) | 2026-11-04 404 |
| `src-pse-pcbs-lfs-q3-2025-release` | Results of the Labour Force Survey, West Bank, Q3 (July–September) 2025 — PCBS release pag | collected (P1) | 2026-11-04 SSLError |
| `src-un-census-pr-rev3` | Principles and Recommendations for Population and Housing Censuses, Revision 3 (UN, 2017) | collected (P1) | — |
| `src-un-ilo-census-economically-active-handbook` | Measuring the Economically Active in Population Censuses: A Handbook (UN and ILO, 2010) | collected (P1) | — |
| `src-escwa-lm-data-structures` | Labour market data structures and challenges in the ESCWA region | collected (P2) | 2026-11-04 403 |
| `src-escwa-statistical-abstract` | Statistical Abstract of the Arab Region (Arabic version, UN iLibrary) | collected (P2) | 2026-11-04 403 |
| `src-gccstat-labour-survey-page` | GCC-Stat — Labour statistics survey page | collected (P2) | 2026-11-04 404 |
| `src-ilo-arab-states-stats` | ILOSTAT — Statistics in Arab States (tag page) | collected (P2) | 2026-11-04 403 |
| `src-ilo-capi-adaptation-guide` | ILO CAPI LFS National Adaptation Guide | collected (P2) | 2026-11-04 502 |
| `src-ilo-forms-of-work` | ILOSTAT — Forms of work (concepts) | collected (P2) | 2026-11-04 403 |
| `src-ilo-icls20-classification-status` | Classification of status at work — ILOSTAT concepts page | collected (P2) | 2026-11-04 403 |
| `src-ilo-lfs-questionnaire-viewer` | ILO LFS questionnaire viewer | collected (P2) | 2026-11-04 403 |
| `src-ilo-sdg-topic` | ILOSTAT — SDG labour market indicators topic page | collected (P2) | 2026-11-04 403 |
| `src-ilo-ssm2-establishment-surveys` | Sources and Methods: Labour Statistics, Volume 2 — Employment, wages, hours of work and la | collected (P2) | — |
| `src-ilo-ssm3-household-surveys` | Sources and Methods: Labour Statistics, Volume 3 — Economically active population, employm | collected (P2) | — |
| `src-ilo-ssm4-admin-records` | Sources and Methods: Labour Statistics, Volume 4 — Employment, unemployment, wages and hou | collected (P2) | — |
| `src-oecd-glossary` | OECD Glossary of Statistical Terms | collected (P2) | — |
| `src-oecd-unemployment-indicator` | OECD — Unemployment rate indicator (definition) | collected (P2) | 2026-11-04 403 |
| `src-usa-bls-cps-documentation` | CPS technical documentation (incl. "How the Government Measures Unemployment") | collected (P2) | 2026-11-04 403 |
| `src-escwa-skills-monitor` | ESCWA Skills Monitor | collected (P3) | 2026-11-04 403 |
| `src-gccstat-ilo-lfs-workshop` | Regional workshop on labour force statistics organised by GCC-Stat & ILO | collected (P3) | 2026-11-04 404 |
| `src-ilo-surveylib` | ILO Survey Library (catalogue of national labour force survey microdata/metadata) | link-ok (P1) | 2026-11-04 200 |
| `src-tun-ins-quarterly-release` | Employment and unemployment indicators — Q1 2026 (INS publication page) | link-ok (P1) | 2026-11-04 200 |
| `src-alo-home` | Arab Labour Organization — official website | link-ok (P2) | 2026-11-04 200 |
| `src-are-ilo-country-profile` | ILO profile of UAE labour statistics system | link-ok (P2) | 2026-11-04 200 |
| `src-aus-abs-lfs-detailed` | Labour Force, Australia, Detailed — August 2025 release | link-ok (P2) | 2026-11-04 200 |
| `src-eurostat-glossary-unemployed` | Eurostat glossary — Unemployed | link-ok (P2) | 2026-11-04 200 |
| `src-fra-insee-eec-puf-2025` | Activité, emploi et chômage en 2025 — EEC detail file | link-ok (P2) | 2026-11-04 200 |
| `src-fra-insee-eec-research-access` | Enquête Emploi — micro-data access for researchers (via Quetelet-Progedo / ADISP) | link-ok (P2) | 2026-11-04 200 |
| `src-fra-insee-eec-source-doc` | Enquête Emploi en continu — methodological documentation (source page) | link-ok (P2) | 2026-11-04 200 |
| `src-gbr-ons-lm-methodology-list` | ONS — People in work: topic-specific methodology (list) | link-ok (P2) | 2026-11-04 200 |
| `src-gccstat-marsa-labour` | GCC-Stat Marsa data portal — Labour dataset (beta) | link-ok (P2) | 2026-11-04 200 |
| `src-ihsn-catalog` | IHSN Survey Catalog (metadata of national surveys incl. LFS) | link-ok (P2) | 2026-11-04 200 |
| `src-ilo-microdata-quick-guide` | ILOSTAT Microdata Processing Quick Guide — principles and methods for processing anonymize | link-ok (P2) | 2026-11-04 200 |
| `src-ilo-understanding-labour-stats-fr` | Understanding labour statistics (French version) | link-ok (P2) | 2026-11-04 200 |
| `src-jor-ihsn-eus` | Jordan EUS — IHSN catalogue metadata (sampling design, coverage) | link-ok (P2) | 2026-11-04 200 |
| `src-mar-hcp-refonte-announcement` | HCP launches the redesign of the national employment survey (announcement) | link-ok (P2) | 2026-11-04 200 |
| `src-pse-erf-lfs` | Palestine LFS on ERF data portal (e.g. LFS 2021) | link-ok (P2) | 2026-11-04 200 |
| `src-pse-pcbs-lfs-2025-metadata` | Labour Force Survey 2025 (yearly file) — PCBS microdata catalogue entry and data dictionar | link-ok (P2) | 2026-11-04 200 |
| `src-sdg-goal9-metadata` | UN SDG metadata — Goal 9 (9.2.2 manufacturing employment share) | link-ok (P2) | 2026-11-04 200 |
| `src-sdg-metadata-8-5-2-docx` | SDG metadata file 8.5.2 (unemployment rate) — docx | link-ok (P2) | 2026-11-04 200 |
| `src-tun-ins-serie-methodes` | INS statistical methods series | link-ok (P2) | 2026-11-04 200 |
| `src-unsc-2013-employment-stats-ar` | UN Statistical Commission 44th session (2013) — Employment statistics, ILO report (Arabic  | link-ok (P2) | 2026-11-04 200 |
| `src-wb-microdata-library` | World Bank Microdata Library | link-ok (P2) | 2026-11-04 200 |
| `src-aitrs-un-profile` | AITRS institutional profile (UN Global Institutions for Statistical Training) | link-ok (P3) | 2026-11-04 200 |
| `src-alo-employment-report-1-summary` | First ALO report on employment and unemployment in Arab States — English summary | link-ok (P3) | 2026-11-04 200 |
| `src-alo-employment-report-2-summary` | Second ALO report on employment and unemployment in Arab States — English summary | link-ok (P3) | 2026-11-04 200 |
| `src-are-glmm-lfs-notes` | GLMM — UAE LFS tables with methodological notes | link-ok (P3) | 2026-11-04 200 |
| `src-are-raksc-lfs-2025` | Ras Al Khaimah Labour Force Survey Report 2025 (part of the national survey coordinated wi | link-ok (P3) | 2026-11-04 200 |
| `src-eurostat-lfs-public-microdata` | Eurostat — EU-LFS public microdata | link-ok (P3) | 2026-11-04 200 |
| `src-ilo-icls21-news` | Statisticians adopt new standards for measuring informal employment (ILO news, 21st ICLS) | link-ok (P3) | 2026-11-04 200 |
| `src-ilo-lfs-dos-donts` | Dos and Don'ts working with the ILO model LFS CAPI questionnaire | link-ok (P3) | 2026-11-04 200 |
| `src-ipums-international` | IPUMS International (harmonised census and survey microdata) | link-ok (P3) | 2026-11-04 200 |
| `src-mar-ihsn-ene` | ENE quarterly rounds — IHSN catalogue metadata | link-ok (P3) | 2026-11-04 200 |
| `src-sau-glmm-lfs-tables` | Gulf Labour Markets, Migration and Population (GLMM) — Saudi LFS tables and notes | link-ok (P3) | 2026-11-04 200 |

## 4. Sources missing or broken

- `src-aitrs-glossary` (to-locate): AITRS Arabic statistical glossary / dictionary (if published). Ask AITRS directly; very relevant to the terminology concordance (I-002).
- `src-alo-statistical-yearbook` (to-locate): ALO Arab labour statistical yearbook (latest edition). A 2010 edition is cited by researchers; latest edition not found.
- `src-amf-arab-statistics` (to-locate): Arab Monetary Fund — Arab statistics database / Joint Arab Economic Report (labour chapter). Not searched in session 1. Secondary relevance (macro data, labour chapter of the Joint Arab Economic Report).
- `src-aus-abs-lfs-methodology` (to-locate): ABS Labour Force, Australia — methodology (latest release). The ABS "Labour Force Survey Methodology" page is referenced from the Detailed releases but its URL was not returned by search (2026-11-04). See src-aus-abs-lfs
- `src-ilo-admin-records-guidelines-1997` (to-locate): Labour statistics based on administrative records: guidelines on compilation and presentation (ILO, Bangkok, 1997). Found only as library catalogue records; no ILO URL yet.
- `src-ilo-census-resources` (to-locate): ILOSTAT — Population census resources (aligning censuses with the latest labour standards). An ILO guide lists this resource category on ILOSTAT; the page URL was not found in search results.
- `src-ilo-icls-arabic-translations` (to-locate): Arabic versions of ICLS resolutions and ILO statistical manuals. Still not found (searches 2026-11-03 and 2026-11-04, EN and AR). Ask ILO ROAS (Beirut) directly. Arabic UN Statistical Commission documents on employment statis
- `src-jor-dos-quarterly-report` (to-locate): DoS quarterly employment and unemployment report (latest). Not found on dosweb by search (2026-11-04). DoS releases the quarterly labour market report (Q1 2026 released 2026-05-31 per Petra: overall 16.1%, Jordanians 21
- `src-tun-ins-questionnaire` (to-locate): ENPE questionnaire (latest). Check ILO Survey Library related materials for ENPE 2022 and the INS NADA catalogue.
- `src-escwa-icls19-preparatory-meeting` (broken): Preparatory regional meeting of labour statisticians in support of the 19th ICLS (ESCWA archive). Useful for official Arabic terminology (e.g. المؤتمر الدولي لخبراء الإحصاءات العمالية).
- `src-gccstat-icse18-workshop-ar` (broken): GCC regional workshop on ICSE-18 and informal sector (2021) — presentation. Useful source for Arabic terminology on ICSE-18 used in the Gulf.
- `src-pse-pcbs-lfs-annual-2024` (broken): Labour Force Survey annual report 2024 (concepts and definitions, methodology, quality). Direct PDF link broken (lead, 2026-11-04). The 2024 annual report is still listed under "related materials" in the PCBS metadata catalogue (src-pse-pcbs-microda
- `src-sau-gastat-lms-methodology-2020q4` (broken): Methodology of Labor Market Statistics — Q4 2020 (EN). 
- `src-tun-ins-nada-catalog` (broken): INS NADA microdata catalogue (ENPE and other surveys). Address taken from IHSN catalogue links (2026-11-04). Replaces nada.ins.tn, which did not resolve. Contact for access questions is ins@ins.tn (per IHSN record).

## 5. Country facts taken from search snippets (shown with «؟» on the site)

- Tunisia · `ind-employment-to-population-ratio`: basis `search-snippet`
- USA · `ind-employment-to-population-ratio`: basis `search-snippet`
- UK · `ind-employment-to-population-ratio`: basis `search-snippet`
- France · `ind-employment-to-population-ratio`: basis `search-snippet`
- Tunisia · `ind-labour-force-participation-rate`: basis `search-snippet`
- USA · `ind-labour-force-participation-rate`: basis `search-snippet`
- UK · `ind-labour-force-participation-rate`: basis `search-snippet`
- France · `ind-labour-force-participation-rate`: basis `search-snippet`
- UK · `ind-unemployment-rate`: basis `search-snippet`
- France · `ind-unemployment-rate`: basis `search-snippet`
- Tunisia · `ind-unemployment-rate`: basis `search-snippet`
- Tunisia · `ind-youth-unemployment-rate`: basis `search-snippet`
- USA · `ind-youth-unemployment-rate`: basis `search-snippet`
- UK · `ind-youth-unemployment-rate`: basis `search-snippet`
- France · `ind-youth-unemployment-rate`: basis `search-snippet`

## 6. Country-profile fields to confirm

- UAE: `nso.name (FCSC vs FCSA)`
- UAE: `lfs.icls_standard`
- UAE: `latest LFS year`
- UK: `lfs.age`
- UK: `TLFS transition date`
- Jordan: `lfs.icls_standard`
- Jordan: `lfs.sample`
- Jordan: `dosweb URL`
- Morocco: `emo2026.first_results`
- Morocco: `lfs.icls_standard`
- Morocco: `back-casting of the series to 2017 (press`
- Morocco: `ledesk.ma)`
- Palestine: `lfs.icls_standard`
- Palestine: `coverage of Gaza 2023–2026 rounds`
- Saudi Arabia: `lfs.icls_standard`
- Saudi Arabia: `lfs.sample`
- Tunisia: `lfs.frequency`
- Tunisia: `lfs.icls_standard`
- Tunisia: `lfs.sample_size`
- Tunisia: `lfs.mode`

## 7. AI-drafted pages awaiting review

AI text is always labelled on the site; review means a statistician has read it and found nothing wrong.

- **data sources (10):** `ds-administrative-records`, `ds-establishment-survey`, `ds-labour-force-survey`, `ds-lfs-framework`, `ds-lfs-periodicity`, `ds-lfs-quality`, `ds-lfs-questionnaire`, `ds-lfs-sample-design`, `ds-lfs-weighting-estimation`, `ds-population-census`
- **indicators (4):** `ind-employment-to-population-ratio`, `ind-labour-force-participation-rate`, `ind-unemployment-rate`, `ind-youth-unemployment-rate`
- **concepts (40):** `con-bias`, `con-cluster-sampling`, `con-coefficient-of-variation`, `con-confidence-interval`, `con-design-effect`, `con-employed`, `con-estimate`, `con-index-number`, `con-interquartile-range`, `con-labour-force`, `con-margin-of-error`, `con-mean`, `con-median`, `con-mode`, `con-non-response`, `con-non-sampling-error`, `con-outlier`, `con-outside-labour-force`, `con-percentage-point`, `con-percentile`, `con-population`, `con-potential-labour-force`, `con-range`, `con-rate`, `con-ratio`, `con-response-rate`, `con-sample`, `con-sampling-error`, `con-sampling-frame`, `con-sampling-weight`, `con-seasonal-adjustment`, `con-simple-random-sampling`, `con-standard-deviation`, `con-standard-error`, `con-stratified-sampling`, `con-time-related-underemployment`, `con-unemployed`, `con-variance`, `con-weighted-mean`, `con-working-age-population`

## 7b. Unofficial translations to review

Shown on indicator pages through the عربي / English switcher, always labelled unofficial, with the original one click away.

- `q-usa-unemployed` (en → ar): AI-assisted (Claude), 2026-11-05, not yet reviewed
- `q-gbr-unemployed` (en → ar): AI-assisted (Claude), 2026-11-05, not yet reviewed
- `q-fra-unemployed` (fr → ar, en): AI-assisted (Claude), 2026-11-05, not yet reviewed
- `q-aus-unemployed` (en → ar): AI-assisted (Claude), 2026-11-05, not yet reviewed
- `q-sau-unemployed` (en → ar): AI-assisted (Claude), 2026-11-05, not yet reviewed
- `q-tun-unemployed` (fr → ar, en): AI-assisted (Claude), 2026-11-05, not yet reviewed
- `q-mar-unemployed` (fr → ar, en): AI-assisted (Claude), 2026-11-05, not yet reviewed
- `q-jor-unemployed` (en → ar): AI-assisted (Claude), 2026-11-05, not yet reviewed
- `q-are-unemployed` (ar → en): AI-assisted (Claude), 2026-11-05, not yet reviewed
- `q-pse-unemployed` (ar → en): AI-assisted (Claude), 2026-11-05, not yet reviewed

Country cards (Arabic/English renderings of Miʿyar's profile notes in `sources/countries/*.yaml`, keys `lfs_ar`, `lfs_en`, `notes_ar`, `nso_ar`, `nso_en`):

- UAE: AI-assisted (Claude), 2026-11-05, not yet reviewed
- Australia: AI-assisted (Claude), 2026-11-05, not yet reviewed
- France: AI-assisted (Claude), 2026-11-05, not yet reviewed
- UK: AI-assisted (Claude), 2026-11-05, not yet reviewed
- Jordan: AI-assisted (Claude), 2026-11-05, not yet reviewed
- Morocco: AI-assisted (Claude), 2026-11-05, not yet reviewed
- Palestine: AI-assisted (Claude), 2026-11-05, not yet reviewed
- Saudi Arabia: AI-assisted (Claude), 2026-11-05, not yet reviewed
- Tunisia: AI-assisted (Claude), 2026-11-05, not yet reviewed
- USA: AI-assisted (Claude), 2026-11-05, not yet reviewed

## 8. Code not yet executed

- `code/stata/miyar_lfs.do`: written to match Python and R, never run. Someone with Stata runs it on `code/data/synthetic_lfs.csv` and compares with `code/expected/results_python.json`.
- Hours threshold for time-related underemployment: 35 is a placeholder in every preset until a national text gives it.

## 9. Lead decisions and settings

From `docs/lead-actions.yml` (edit that file; mark `status: done`).

- [ ] **Review the website preview**: Feedback on design and wording (private preview link in docs/STATUS.md), including the new «مصادر البيانات» section.
- [ ] **Confirm the Arabic spelling of your name**: Used in the founder's letter on the methodology page (draft in your voice; edit freely).
- [ ] **Paste the repository About box, topics and social preview**: Values ready in docs/github-settings.md (about 10 minutes).
- [ ] **Turn on GitHub Pages and publish**: Settings → Pages → Source "GitHub Actions", then Actions → website → Run workflow.
- [ ] **After go-live, register the site**: Google Search Console and Bing Webmaster Tools, then Zenodo DOI and Wikidata item (docs/github-settings.md).
- [ ] **Decide the domain name and LinkedIn page**: Custom domain (I-051) and a LinkedIn page for Miʿyar; record them in docs/prd/15-naming.md.
- [ ] **Optional — allow statistical sites in the cloud environment's network policy**: Lets the agent open ILO/NSO documents and draft quotes for you to confirm (I-044). Without it, quotes stay paste-only.
