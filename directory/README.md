# Practitioner directory (سجل ممارسي إحصاءات العمل العرب)

A voluntary, opt-in directory of Arab labour statisticians, currently in the **design** stage. It is not open yet; the target is Phase 1.

## Purpose
- Help Arab statisticians find peers (by country, institution and speciality).
- Recruit reviewers and contributors for the knowledge base.
- Build the community behind the project (and the demand for training).

## How it works
1. A person fills in the public form ([form-spec.md](form-spec.md)) in Arabic, with English and French labels.
2. For **each field** they choose: public / visible only to the project / not provided.
3. Responses are stored **privately** in the form tool. They are **never** stored in this Git repository ([ADR-0003](../docs/decisions/ADR-0003-practitioner-directory-privacy.md)).
4. Monthly, the lead exports only consented public fields to the website listing.
5. Each person can ask to correct or delete their data at any time.

## Files
- [schema.yaml](schema.yaml): fields, types and the default visibility of each
- [consent-ar.md](consent-ar.md): Arabic consent text (authoritative)
- [consent-en.md](consent-en.md): English consent text
- [form-spec.md](form-spec.md): form layout, validation and the export procedure

## Value for members
A public profile (optional), early access to new tools, invitations to webinars, credit as reviewer, and a certificate for contributors (I-035).
