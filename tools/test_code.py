#!/usr/bin/env python3
"""Tests for the Miʿyar code library (code/python/miyar_lfs.py). Exit 1 on failure.

Writes code/expected/results_python.json (reference numbers the R job in CI must reproduce).
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code" / "python"))
from miyar_lfs import INDICATORS, Params, derive, indicators, ratio, read_lfs  # noqa: E402

DATA = ROOT / "code" / "data" / "synthetic_lfs.csv"
fails = []


def check(cond, msg):
    print(("  ok    " if cond else "  FAIL  ") + msg)
    if not cond:
        fails.append(msg)


def main():
    raw = read_lfs(DATA)
    p = Params.for_country(None)
    d = derive(raw, p)
    res = indicators(d)["total"]

    print("Identities")
    check(((d["employed"] + d["unemployed"]) == d["lf"]).all(), "LF = employed + unemployed for every person")
    check(not (d["employed"] & d["unemployed"]).any(), "nobody is both employed and unemployed")
    check(not (d["plf"] & d["lf"]).any(), "potential labour force is outside the labour force")
    check(all(0 <= r["estimate"] <= 100 for r in res.values()), "all rates between 0 and 100")
    check(res["lu1"]["estimate"] <= res["lu2"]["estimate"] + 1e-9, "LU1 <= LU2")
    check(res["lu3"]["estimate"] <= res["lu4"]["estimate"] + 1e-9, "LU3 <= LU4")
    check(res["lu1"]["estimate"] <= res["lu3"]["estimate"] + 1e-9, "LU1 <= LU3")
    check(all(r["ci95"][0] <= r["estimate"] <= r["ci95"][1] for r in res.values()), "every estimate inside its 95% CI")

    print("Standard error against the simple-random-sampling formula")
    rnd = np.random.default_rng(1)
    n = 4000
    s = pd.DataFrame({"stratum": 1, "psu": np.arange(n), "weight": 1.0, "y": (rnd.random(n) < 0.3).astype(int), "x": 1})
    r = ratio(s, "y", "x")
    pp = s["y"].mean()
    srs = math.sqrt(pp * (1 - pp) / (n - 1)) * 100
    check(abs(r["se"] - srs) / srs < 0.01, f"SE {r['se']:.4f} ≈ √(p(1−p)/n) {srs:.4f} (equal weights, one person per PSU)")
    check(abs(r["deff"] - 1) < 0.02, f"design effect ≈ 1 for simple random sampling ({r['deff']})")

    print("Country rules move the numbers in the right direction")
    u = {}
    for days in (0, 14, 28):
        q = Params.for_country(None)
        q.availability_days = days
        u[days] = int(derive(raw, q)["unemployed"].sum())
    check(u[0] <= u[14] <= u[28], f"wider availability window never lowers unemployment ({u})")
    q = Params.for_country(None)
    q.future_starters = False
    check(int(derive(raw, q)["unemployed"].sum()) <= int(d["unemployed"].sum()), "excluding future starters never raises unemployment")

    print("Presets trace to quotations")
    presets = json.loads((ROOT / "code" / "presets" / "countries.json").read_text(encoding="utf-8"))
    quotes = {q["slot"]: q for q in __import__("yaml").safe_load((ROOT / "content" / "quotes.yml").read_text(encoding="utf-8"))["quotes"]}
    for iso, c in presets.items():
        if iso.startswith("_"):
            continue
        qd = quotes.get(c.get("quote"), {})
        check(qd.get("status") in ("verified", "pasted"), f"preset '{iso}' comes from quote {c.get('quote')} ({qd.get('status')})")

    out = {"note": "Reference results on the SYNTHETIC file (ILO-default parameters and the 'jor' preset). The R job must reproduce them.",
           "ilo_default": res, "jor": indicators(derive(raw, Params.for_country("jor")), "sex")}
    path = ROOT / "code" / "expected" / "results_python.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nWrote {path.relative_to(ROOT)}")
    if fails:
        print(f"{len(fails)} failure(s)")
        sys.exit(1)
    print("OK: code library tests pass.")


if __name__ == "__main__":
    main()
