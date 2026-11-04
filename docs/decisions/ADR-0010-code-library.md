# ADR-0010: Code library for computing the indicators

- **Date:** 2026-11-05 · **Status:** accepted

## Decision
- Miʿyar ships code (MIT) that computes the ICLS-19 indicators from LFS microdata: Python (reference, tested), R (`survey` package, run in CI and compared with Python), and Stata (written to match, not executed).
- Standard errors use Taylor linearisation for ratios in a stratified cluster design, with PSUs sampled with replacement. Domain estimates zero out units outside the domain, the same as `survey::subset`.
- Country rules (age floor, search window, availability window) come from `code/presets/countries.json`. It is generated from quote-backed `measures` only. A rule not stated in a verified or pasted text falls back to the ILO default, and the program prints which values came from where.
- Tests run on an invented, seeded synthetic file (`code/data/synthetic_lfs.csv`, committed as an explicit exception to the `*.csv` ignore rule). No real microdata is ever committed.

## Consequences
- Pasting more national texts directly improves the code (presets fill in).
- Known limits: no calibration-aware or replicate-weight variance yet (backlog I-056); the hours threshold for underemployment is a placeholder (35) until national texts give it.
