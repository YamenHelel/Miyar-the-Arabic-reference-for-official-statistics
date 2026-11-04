# 04: Features in current scope (MVP: Phases 0–1)

## F-01 Indicator pages (صفحة المؤشر)
One page per indicator. Sections:
1. Arabic name, with the **term variants** used in each country
2. English and French names
3. Short Arabic explanation (labelled AI-assisted and reviewed)
4. **International standard**: quoted definition, source (ICLS resolution, paragraph number), custodian agency
5. Formula and its components (linked to concept pages)
6. SDG link (if any) and metadata summary
7. **Country implementations table**: for each of the 10 countries, the national definition (quoted), standard applied (ICLS-13/19), age range, reference period, source survey, frequency, coverage of non-nationals, link
8. **Comparability notes**: what makes the figures differ across countries
9. Where to get the data: ILOSTAT, national portal, microdata
10. Related indicators and concepts
11. Sources and "last verified" date

## F-02 Concept glossary (مسرد المفاهيم)
Statistical concepts (mean, median, variance, standard error, CV, confidence interval, design effect, weighting, calibration, non-response, imputation, seasonal adjustment…) and labour concepts (reference week, job search, availability, potential labour force, own-use production work, ICSE-18 statuses…). Each entry has an Arabic definition, the original-language source definition, a formula when relevant, an example, and term variants.

## F-03 Standards library (مكتبة المعايير)
ICLS resolutions (13th, 19th, 20th, 21st), ILO manuals, classifications (ISCO-08, ISIC Rev.4/5, ICSE-18), UN SDG metadata, Eurostat/OECD guidance. Each has a short Arabic summary and a link, plus the Arabic version where one exists.

## F-04 Country profiles (بطاقة البلد)
For each country: NSO, LFS design (sample, mode, frequency), standard applied, key publications, release calendar, data portal, microdata access, contact page. Built from `sources/countries/*.yaml`.

## F-05 Source registry (سجل المصادر)
A browsable and filterable list of every source, with status and archive link. This builds transparency and trust.

## F-06 Microdata catalogue (دليل البيانات الجزئية)
For each country and survey: whether a PUF or licensed file exists, where to get it, conditions, years, and harmonised versions (ERF, IPUMS).

## F-07 SDG labour indicators hub
The labour-related SDG indicators, each with custodian, Arabic metadata summary, link to the UN metadata, and links to country reporting.

## F-08 Search (Arabic-aware)
Client-side search that handles Arabic normalisation (alef forms, taa marbuta, diacritics) and finds an entry through any of its term variants.

## F-09 Claude skill v1
A skill that answers labour-statistics questions **only from the knowledge base**, always cites the source and verification date, and says "not in the base yet" instead of guessing. Arabic by default.

## F-10 Practitioner directory (سجل الممارسين)
Opt-in registration form, consent-filtered public list, and search by country and speciality. See `directory/`.

## F-11 Feedback and corrections
A "suggest a correction" link on every page (form or GitHub issue) that feeds the review queue.

## Out of scope for the MVP
Interactive calculators, questionnaire reviewer, MCP server, other domains, user accounts, paid features. All are in the backlog.

## F-11 Data sources (مصادر البيانات)
Added 2026-11-04 (ADR-0011). A section on where labour statistics come from, with the ILO as the first source of truth.
- **Four source types:** labour force survey, population census, administrative records and registers, establishment surveys. Each page has:
  - the official ILO/UN wording (quote slots)
  - how the source works, its strengths and limits (AI-assisted, labelled)
  - what it can measure for labour statistics
  - its instance in each of the 10 countries (LFS now; census and registers in Phase 1)
- **LFS guide in six parts:** conceptual framework (19th ICLS), questionnaire and the ILO model, sample design and rotation, weighting and estimation, periodicity, quality and comparability. Linked to the glossary and the code library.
- **Index page:** a "which source for which question" matrix.
- Not yet covered (backlog I-061): household income/expenditure surveys, informal-sector/mixed surveys, time-use surveys.

