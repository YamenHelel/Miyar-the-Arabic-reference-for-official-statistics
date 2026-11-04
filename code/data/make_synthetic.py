#!/usr/bin/env python3
"""Make Miʿyar's SYNTHETIC labour force survey file (code/data/synthetic_lfs.csv).

The data are INVENTED, for testing and teaching only — they describe no real country.
Design: 8 strata x 20 PSUs (clusters) x 12 households, 1–6 persons per household, design weights varying by stratum.
Seeded, so every run produces the same file.

Variables (one row per person):
  hh_id, person_id, stratum, psu, weight          survey design
  age, sex (1 male, 2 female), nationality (1 national, 2 non-national)
  in_education, in_training                        0/1 (for NEET)
  worked_1h                                        worked at least 1 hour for pay or profit in the reference week (0/1)
  temp_absent                                      has a job but temporarily absent (0/1)
  searched_days                                    days since the last active job-search step (empty = no search)
  available_days                                   could start work within N days after the reference week (0 = in the week; empty = not available)
  future_starter                                   has found a job that starts later (0/1)
  wants_work                                       would like to work (0/1)
  hours_usual                                      usual weekly hours in all jobs (employed only)
  wants_more_hours, available_more_hours           0/1 (employed only)
"""
import csv
import random
from pathlib import Path

SEED = 20261105
OUT = Path(__file__).resolve().parent / "synthetic_lfs.csv"


def main():
    rnd = random.Random(SEED)
    rows = []
    pid = 0
    for stratum in range(1, 9):
        urban = stratum <= 4
        base_w = rnd.choice([120, 150, 180, 220, 260])
        for p in range(1, 21):
            psu = stratum * 100 + p
            psu_effect = rnd.gauss(0, 0.06)          # clustering: neighbours resemble each other
            for h in range(1, 13):
                hh = psu * 100 + h
                size = rnd.choice([1, 2, 3, 3, 4, 4, 5, 6])
                w = round(base_w * rnd.uniform(0.85, 1.15), 2)
                nonnat_hh = rnd.random() < (0.25 if urban else 0.08)
                for k in range(size):
                    pid += 1
                    age = rnd.randint(25, 60) if k == 0 else rnd.randint(0, 75)
                    sex = 1 if (k == 0 and rnd.random() < 0.8) else rnd.choice([1, 2])
                    nat = 2 if nonnat_hh else 1
                    in_edu = int(6 <= age <= 24 and rnd.random() < (0.85 if age < 18 else 0.35))
                    in_trn = int(15 <= age <= 29 and not in_edu and rnd.random() < 0.05)
                    r = dict(hh_id=hh, person_id=pid, stratum=stratum, psu=psu, weight=w, age=age, sex=sex, nationality=nat,
                             in_education=in_edu, in_training=in_trn, worked_1h=0, temp_absent=0, searched_days="",
                             available_days="", future_starter=0, wants_work=0, hours_usual="", wants_more_hours=0,
                             available_more_hours=0)
                    if age >= 15:
                        p_part = (0.80 if sex == 1 else 0.22) + (0.12 if nat == 2 else 0) - (0.35 if in_edu else 0) \
                                 - (0.45 if age >= 63 else 0) + psu_effect
                        if rnd.random() < max(0.02, min(0.97, p_part)):
                            p_unemp = (0.33 if age < 25 else 0.12) + (0.10 if sex == 2 else 0) - (0.08 if nat == 2 else 0) + psu_effect
                            if rnd.random() > max(0.02, p_unemp):        # employed
                                if rnd.random() < 0.04:
                                    r["temp_absent"] = 1
                                else:
                                    r["worked_1h"] = 1
                                hrs = max(1, round(rnd.gauss(44 if sex == 1 else 36, 10)))
                                r["hours_usual"] = hrs
                                if hrs < 35 and rnd.random() < 0.45:
                                    r["wants_more_hours"] = 1
                                    r["available_more_hours"] = int(rnd.random() < 0.8)
                            else:                                       # job seeker of some kind
                                r["wants_work"] = 1
                                r["searched_days"] = rnd.choice([3, 7, 10, 14, 21, 25, 28, 28, 40, 60])
                                r["available_days"] = rnd.choice([0, 0, 0, 7, 10, 14, 15, 21, 28, ""])
                                r["future_starter"] = int(rnd.random() < 0.05)
                        elif rnd.random() < 0.12:                       # outside LF but close to it
                            r["wants_work"] = 1
                            r["available_days"] = rnd.choice([0, 7, 14, ""])
                    rows.append(r)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        f.write("# SYNTHETIC DATA - invented for testing Miʿyar code; not real statistics of any country\n")
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader()
        wr.writerows(rows)
    print(f"{len(rows)} synthetic persons -> {OUT}")


if __name__ == "__main__":
    main()
