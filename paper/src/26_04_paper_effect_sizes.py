#!/usr/bin/env python3
# =============================================================================
# Script : 26_04_paper_effect_sizes.py  (v1.1: --swift runs in ~/SWIFT with models/ and data/; numbers unchanged)
# Project: ARGUS (SRL resubmission) — descriptive effect sizes (not registered)
#
# What this script does
#   For each opened test sequence and tau in {0.5, 2} s, reads the frozen per-event
#   CSV and judgment JSON and computes, for C3 - BEST, C4 - BEST and C3 - M6r:
#     * the Hodges-Lehmann paired shift (median of Walsh averages of the paired
#       differences, zeros kept) with a 95% interval from a day-block bootstrap
#       (events grouped by JST calendar day of origin; 2,000 resamples, seed 0),
#     * the fraction better / tied / worse.
#   Day blocks keep events that share past events and days together, so the interval
#   reflects the dependence between events within a sequence. Descriptive only.
# Inputs : data/inputs/models/{21_04,21_20,25_05}_judgment.json, data/inputs/data/*_per_event.csv
# Outputs: data/26_04_effect_sizes.json, data/26_04_effect_sizes.csv
# Usage  : uv run python src/26_04_paper_effect_sizes.py            (paper repository layout, data/inputs/)
#          cd ~/SWIFT && uv run python src/26_04_paper_effect_sizes.py --swift   (inputs models/, data/; outputs data/)
# =============================================================================
import json
from pathlib import Path
import numpy as np, pandas as pd
import sys
ROOT = Path(__file__).resolve().parents[1]
INP = ROOT if "--swift" in sys.argv else ROOT / "data" / "inputs"   # ~/SWIFT keeps models/ and data/ at the top
SEQ = [("Central Tottori 2016", "21_04"), ("Northern Osaka 2018", "21_20"), ("Western Shimane 2018", "25_05")]
BASE = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]
NB, SEED = 2000, 0


def best_of(S, t):
    full = [m for m in BASE if S[m][t]["available"] == 1.0 and S[m][t]["median_km"] is not None]
    return min(full, key=lambda m: S[m][t]["median_km"])


def hl(d):
    d = np.sort(d); i, j = np.triu_indices(len(d))
    return float(np.median((d[i] + d[j]) / 2.0))


rows, out = [], {}
rng = np.random.default_rng(SEED)
for lab, k in SEQ:
    J = json.load(open(INP / f"models/{k}_judgment.json")); E = pd.read_csv(INP / f"data/{k}_per_event.csv")
    day = pd.to_datetime(E["origin_time"], utc=True, format="mixed").dt.tz_convert("Asia/Tokyo").dt.date.astype(str).to_numpy()
    days = np.unique(day); idx = [np.where(day == dd)[0] for dd in days]
    for t in ("0.5", "2"):
        b = best_of(J["summary"], t)
        for a, r, name in (("C3", b, "BEST"), ("C4", b, "BEST"), ("C3", "M6r", "M6r")):
            d = E[f"{a}_err_t{t}"].to_numpy(float) - E[f"{r}_err_t{t}"].to_numpy(float); ok = np.isfinite(d)
            est = hl(d[ok]); bs = []
            for _ in range(NB):
                pick = np.concatenate([idx[i] for i in rng.integers(0, len(idx), len(idx))])
                dd = d[pick]; dd = dd[np.isfinite(dd)]
                if len(dd) > 1: bs.append(hl(dd) if len(dd) <= 400 else float(np.median(dd)))
            lo, hi = np.percentile(bs, [2.5, 97.5])
            rec = dict(sequence=lab, tau=t, comparison=f"{a}-{name}",
                       ref=r, n=int(ok.sum()), n_days=len(days), hl_shift_km=round(est, 3), ci_lo=round(float(lo), 3), ci_hi=round(float(hi), 3),
                       frac_better=round(float(np.mean(d[ok] < 0)), 3), frac_tied=round(float(np.mean(d[ok] == 0)), 3),
                       frac_worse=round(float(np.mean(d[ok] > 0)), 3))
            rows.append(rec); print(rec)
pd.DataFrame(rows).to_csv(ROOT / "data/26_04_effect_sizes.csv", index=False)
json.dump(rows, open(ROOT / "data/26_04_effect_sizes.json", "w"), indent=1)
