# 07: Data model

The source schema is implemented in `sources/schema.yaml`. The others are specified here and implemented in Phase 0b.

## Source (implemented)
`id, title_en, title_ar, title_orig, publisher, scope (international|country), country, type, domain, languages[], url, archived_url, date_published, date_accessed, version, licence_terms, icls_standard, sdg_indicators[], priority (P1–P3), status, verified_by, verified_date, superseded_by, notes`

## Indicator
```yaml
id: ind-unemployment-rate
name_ar: معدل البطالة
names: { en: Unemployment rate, fr: Taux de chômage }
term_variants: [ { term: نسبة البطالة, used_in: [jor] } ]
domain: labour
international:
  standard: src-ilo-icls19-res1          # source id
  paragraph: "47"
  definition_quote: "…"                 # exact, original language
  definition_ar: "…"
  translation: official|unofficial
  custodian: ILO
formula: "UR = U / LF × 100"
components: [con-unemployed, con-labour-force]
sdg: ["8.5.2"]
countries:
  tun: { definition_quote: "…", source: src-tun-…, icls_standard: "19th", age: "15+",
         reference_period: "week", frequency: quarterly, non_nationals: included, notes: "…" }
comparability_notes_ar: "…"
explanation_ai_ar: "…"                  # labelled AI-assisted
related: [ind-lu3, ind-youth-unemployment-rate]
status: draft|reviewed|verified
reviewers: [ … ]
last_verified: 2026-12-01
```

## Concept
`id, name_ar, names{en,fr}, term_variants[], category (statistical|labour|survey|classification), definition_ar, definition_quote, source, formula, example_ar, related[], status`

## Term (terminology concordance)
`id, concept_id, ar_variants[{term, countries[], region (maghreb|mashreq|gulf), source}], en, fr, preferred_ar, notes`

## Practitioner (private store only; see `directory/schema.yaml`)

## Identifiers
`ind-*` indicators · `con-*` concepts · `term-*` terms · `src-*` sources. Lowercase, hyphenated and stable (never reused).
