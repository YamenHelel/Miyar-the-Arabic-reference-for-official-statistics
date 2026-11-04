#!/usr/bin/env python3
"""Compare the R results (CI) with code/expected/results_python.json.

Usage: python tools/compare_code_results.py results_r.json
Point estimates must agree to 0.001 percentage points (values are rounded to 4 decimals); standard errors within 1% relative.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    py = json.loads((ROOT / "code" / "expected" / "results_python.json").read_text(encoding="utf-8"))
    r = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    bad, n = [], 0
    pairs = [("ilo_default", py["ilo_default"], r["ilo_default"])]
    pairs += [(f"jor/{g}", py["jor"][g], r["jor"][g]) for g in py["jor"]]
    for label, a, b in pairs:
        for k, va in a.items():
            vb = b[k]
            n += 1
            if abs(va["estimate"] - vb["estimate"]) > 1e-3:
                bad.append(f"{label}/{k}: estimate python {va['estimate']} vs R {vb['estimate']}")
            if va["se"] and abs(va["se"] - vb["se"]) / va["se"] > 0.01:
                bad.append(f"{label}/{k}: SE python {va['se']} vs R {vb['se']}")
    for b_ in bad:
        print("  MISMATCH", b_)
    print(f"Compared {n} indicator results: {'OK — R and Python agree' if not bad else str(len(bad)) + ' mismatches'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
