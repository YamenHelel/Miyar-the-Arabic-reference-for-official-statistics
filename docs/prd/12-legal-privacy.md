# 12: Legal and privacy

> Not legal advice. Have a lawyer review this before collecting directory data at scale.

## Copyright and quoting
- Quote short extracts of official definitions with full attribution and a link. This is generally accepted for definitions and standards, but check each publisher's terms (record them in `licence_terms`).
- ILO, UN and OECD materials: attribution required; check specific reuse terms, especially for translations. Arabic translations of ILO texts are marked unofficial unless the ILO published them.
- Do not republish full PDFs. Link to them and archive them on the Wayback Machine.
- Microdata: never redistribute. Link only to the official access route.

## Personal data (practitioner directory)
| Jurisdiction | Law | Note |
|---|---|---|
| Tunisia | Organic Law 2004-63 on personal data protection (INPDP authority) | Check whether notification to INPDP is needed |
| Morocco | Law 09-08 (CNDP authority) | Consent and declaration rules |
| Saudi Arabia | Personal Data Protection Law (PDPL), SDAIA | Cross-border transfer rules |
| UAE | Federal Decree-Law 45/2021 (PDPL) | |
| Jordan | Personal Data Protection Law No. 24 of 2023 | |
| Palestine | No comprehensive law confirmed as of this writing (to check) | Apply the strictest standard |
| UK / France | UK GDPR / EU GDPR | Applies if residents of these countries register |

*(Law names and numbers were written from general knowledge and must be verified before publication; tracked as `to-verify`.)*

## Applied rules
- Explicit, per-field opt-in consent; separate consent for "public listing" and "contact for project".
- Data minimisation: only the fields in `directory/schema.yaml`.
- Right to access, correct and delete: by email to yamen.hlel@gmail.com, within 30 days.
- Retention: deleted 24 months after the last confirmation unless renewed.
- Storage: the form provider's private store, with 2FA on the account. Not in Git.
