#!/usr/bin/env python3
"""Miʿyar code library — labour indicators from LFS microdata (ICLS-19), with survey weights and standard errors.

Usage (command line):
  python code/python/miyar_lfs.py DATA.csv [--country jor] [--by sex] [--json out.json]

Usage (Python):
  from miyar_lfs import Params, derive, indicators
  df = derive(df, Params.for_country("jor"))
  table = indicators(df)

Input variables (map your national file to these names first — see code/README.md):
  stratum, psu, weight, age, sex, nationality, in_education, in_training, worked_1h, temp_absent,
  searched_days, available_days, future_starter, wants_work, hours_usual, wants_more_hours, available_more_hours

Standards: ILO 19th ICLS resolution (2013, amended by the 21st ICLS in 2023), §27 (employment), §47 (unemployment),
§73 (headline indicators LU1–LU4). Country rules come from code/presets/countries.json, which Miʿyar builds only
from verified official texts.

Standard errors: Taylor linearisation of the ratio R = Σw·y / Σw·x for a stratified multi-stage design, treating
PSUs as sampled with replacement (the usual approximation, same as R `survey` with ids=~psu, strata=~stratum).
It ignores finite-population corrections and the variance gained or lost through calibration of the weights.

Licence: MIT. Source: https://github.com/YamenHelel/Miyar-the-Arabic-reference-for-official-statistics
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, field, asdict
from pathlib import Path

import numpy as np
import pandas as pd

PRESETS = Path(__file__).resolve().parents[1] / "presets" / "countries.json"
Z95 = 1.959963984540054


@dataclass
class Params:
    age_min: int = 15
    age_max: int | None = None
    search_days: int = 28           # job search in the last N days (§47(b): four weeks or one month)
    availability_days: int = 14     # available within N days after the reference week (§47(d)(i): ≤ two weeks in total)
    future_starters: bool = True    # count future starters who are available as unemployed
    hours_threshold: float = 35     # time-related underemployment: usual hours below this (national choice)
    youth: tuple = (15, 24)
    country: str = "ilo-default"
    sources: dict = field(default_factory=dict)

    @classmethod
    def for_country(cls, iso: str | None) -> "Params":
        """Parameters from Miʿyar's quote-backed presets; any value not stated in the official text uses the ILO default."""
        presets = json.loads(PRESETS.read_text(encoding="utf-8"))
        d = presets["_default_ilo"]
        p = cls(age_min=d["age_min"], search_days=d["search_days"], availability_days=d["availability_days"],
                future_starters=d["future_starters"], hours_threshold=d["hours_threshold"], country=iso or "ilo-default")
        src = {k: "ILO default" for k in ("age_min", "search_days", "availability_days", "future_starters", "hours_threshold")}
        if iso:
            c = presets.get(iso)
            if c is None:
                raise SystemExit(f"No Miʿyar preset for '{iso}'. Available: " + ", ".join(k for k in presets if not k.startswith("_")))
            for k in ("age_min", "search_days", "availability_days"):
                if c.get(k) is not None:
                    setattr(p, k, c[k])
                    src[k] = f"{c['quote']} ({c['status']})"
        p.sources = src
        return p


# ---------------------------------------------------------------- derivation
def _flag(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce").fillna(0).astype(int).eq(1)


def derive(df: pd.DataFrame, p: Params) -> pd.DataFrame:
    """Add ICLS-19 labour force status columns (0/1): wap, employed, unemployed, lf, plf, tru, outside, youth, neet."""
    d = df.copy()
    age = pd.to_numeric(d["age"], errors="coerce")
    wap = age >= p.age_min
    if p.age_max is not None:
        wap &= age <= p.age_max
    employed = wap & (_flag(d["worked_1h"]) | _flag(d["temp_absent"]))
    searched = pd.to_numeric(d["searched_days"], errors="coerce").le(p.search_days)          # NaN (no search) -> False
    available = pd.to_numeric(d["available_days"], errors="coerce").le(p.availability_days)  # NaN (not available) -> False
    future = _flag(d["future_starter"]) if p.future_starters else pd.Series(False, index=d.index)
    unemployed = wap & ~employed & available & (searched | future)
    # potential labour force: unavailable jobseekers + available potential jobseekers (ICLS-19)
    plf = wap & ~employed & ~unemployed & ((searched & ~available) | (~searched & available & _flag(d["wants_work"])))
    hours = pd.to_numeric(d["hours_usual"], errors="coerce")
    tru = employed & hours.lt(p.hours_threshold) & _flag(d["wants_more_hours"]) & _flag(d["available_more_hours"])
    youth = age.between(p.youth[0], p.youth[1])
    neet = youth & ~employed & ~_flag(d["in_education"]) & ~_flag(d["in_training"])
    for name, s in dict(wap=wap, employed=employed, unemployed=unemployed, lf=employed | unemployed, plf=plf, tru=tru,
                        outside=wap & ~(employed | unemployed), youth=youth & wap, neet=neet,
                        youth_lf=youth & (employed | unemployed), youth_unemployed=youth & unemployed,
                        tru_or_u=tru | unemployed, u_or_plf=unemployed | plf, elf=employed | unemployed | plf,
                        tru_u_plf=tru | unemployed | plf).items():
        d[name] = s.astype(int)
    return d


# ---------------------------------------------------------------- estimation
INDICATORS = {   # key: (numerator, denominator, Arabic name, English name)
    "lfpr": ("lf", "wap", "معدل المشاركة في القوة العاملة", "Labour force participation rate"),
    "epr": ("employed", "wap", "نسبة العمالة إلى السكان", "Employment-to-population ratio"),
    "lu1": ("unemployed", "lf", "معدل البطالة (LU1)", "Unemployment rate (LU1)"),
    "lu2": ("tru_or_u", "lf", "LU2: نقص التشغيل المرتبط بالوقت والبطالة", "LU2: time-related underemployment + unemployment"),
    "lu3": ("u_or_plf", "elf", "LU3: البطالة والقوة العاملة المحتملة", "LU3: unemployment + potential labour force"),
    "lu4": ("tru_u_plf", "elf", "LU4: المقياس المركب لنقص استخدام العمالة", "LU4: composite measure of labour underutilization"),
    "yur": ("youth_unemployed", "youth_lf", "معدل البطالة بين الشباب", "Youth unemployment rate"),
    "neet": ("neet", "youth", "نسبة الشباب خارج التعليم والعمل والتدريب", "Youth NEET rate"),
}


def ratio(d: pd.DataFrame, y: str, x: str, domain: pd.Series | None = None) -> dict:
    """Weighted ratio Σw·y/Σw·x with linearised SE for a stratified cluster design (PSUs with replacement)."""
    w = d["weight"].astype(float).to_numpy()
    dom = np.ones(len(d), bool) if domain is None else domain.to_numpy(bool)
    yv = d[y].to_numpy(float) * dom
    xv = d[x].to_numpy(float) * dom
    Y, X = float((w * yv).sum()), float((w * xv).sum())
    if X <= 0:
        return {"estimate": math.nan, "se": math.nan, "cv": math.nan, "ci95": [math.nan, math.nan], "deff": math.nan, "n": 0}
    R = Y / X
    z = w * (yv - R * xv) / X
    tot = pd.DataFrame({"h": d["stratum"].to_numpy(), "psu": d["psu"].to_numpy(), "z": z}).groupby(["h", "psu"])["z"].sum()
    var = 0.0
    for _, zh in tot.groupby(level=0):
        nh = len(zh)
        if nh > 1:
            var += nh / (nh - 1) * float(((zh - zh.mean()) ** 2).sum())
    se = math.sqrt(var)
    n = int(xv.sum())
    srs = R * (1 - R) / n if n > 1 and 0 < R < 1 else math.nan    # simple-random-sampling variance of a proportion
    return {"estimate": round(100 * R, 4), "se": round(100 * se, 4),
            "cv": round(100 * se / R, 2) if R > 0 else math.nan,
            "ci95": [round(100 * (R - Z95 * se), 4), round(100 * (R + Z95 * se), 4)],
            "deff": round(var / srs, 3) if srs and srs == srs else math.nan, "n": n}


def indicators(d: pd.DataFrame, by: str | None = None) -> dict:
    """All headline indicators, overall and optionally by a grouping variable (e.g. sex, nationality)."""
    out = {"total": {k: ratio(d, num, den) for k, (num, den, *_) in INDICATORS.items()}}
    if by:
        for g in sorted(d[by].dropna().unique()):
            out[f"{by}={g}"] = {k: ratio(d, num, den, d[by].eq(g)) for k, (num, den, *_) in INDICATORS.items()}
    return out


def read_lfs(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path, comment="#")


def main():
    ap = argparse.ArgumentParser(description="Miʿyar: ICLS-19 labour indicators with standard errors")
    ap.add_argument("data")
    ap.add_argument("--country", help="Miʿyar preset (e.g. jor, sau, mar, are, aus, usa, ilo)")
    ap.add_argument("--by", help="disaggregate by this variable (e.g. sex)")
    ap.add_argument("--json", help="write results to this JSON file")
    a = ap.parse_args()
    p = Params.for_country(a.country)
    d = derive(read_lfs(a.data), p)
    res = indicators(d, a.by)
    print(f"Miʿyar · parameters for '{p.country}':")
    for k in ("age_min", "search_days", "availability_days", "future_starters", "hours_threshold"):
        print(f"  {k:18} = {getattr(p, k)!s:6}  ({p.sources.get(k, '')})")
    for grp, table in res.items():
        print(f"\n[{grp}]  {'indicator':48} {'%':>8} {'SE':>7} {'CV%':>6} {'95% CI':>17} {'deff':>6}")
        for k, r in table.items():
            name = INDICATORS[k][3]
            print(f"  {name:56} {r['estimate']:8.2f} {r['se']:7.2f} {r['cv']:6.1f} "
                  f"[{r['ci95'][0]:6.2f},{r['ci95'][1]:6.2f}] {r['deff']:6.2f}")
    if a.json:
        Path(a.json).write_text(json.dumps({"params": {k: v for k, v in asdict(p).items() if k != "sources"},
                                            "sources": p.sources, "results": res}, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
