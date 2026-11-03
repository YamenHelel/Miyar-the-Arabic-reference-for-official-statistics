# ADR-0003: Practitioner directory, with an opt-in form and private storage

- **Date:** 2026-11-03 · **Status:** accepted

## Decision
Practitioners register through a public opt-in form (Tally or Google Forms) that has explicit consent per field. Responses are stored privately, owned by the project lead and **never committed to this repository**. Only the fields a person marks as public are later exported to the website.

## Why
The data is personal and spans jurisdictions with data-protection laws (Tunisia, Morocco, KSA PDPL, UAE PDPL, Jordan PDPL, UK GDPR, EU GDPR). Committing it to a Git repo would make it permanent and public.

## Consequences
See `directory/` for the schema, consent texts and form specification. Export to the site happens through a manual or scripted step that filters on the consent flags.
