#!/usr/bin/env python3
# =============================================================================
# Script : 26_09_reviewer_checks.py  (v1; run on the author's Mac)
# Project: ARGUS (SRL resubmission) — answers to expected reviewer questions,
#          read from FROZEN outputs only. Descriptive, not registered.
#
# What this script does
#   Part A  (read only) Prints the stored results of analyses already run:
#           23_01 (how much C3/C4 lean on the JMA "memory"), 23_02 (scoring with
#           the independent DPRI catalog for Central Tottori 2016), 23_03 (DPRI
#           scoring after aligning the memory frame), and 21_10 (effect of the
#           epicentral error on the predicted JMA intensity). Nothing is recomputed.
#   Part B  (new, descriptive) "Does the gain hold early in the sequence, when
#           fewer past events exist?" For each opened test sequence and
#           tau in {0.5, 2} s, the test events are split into three equal-count
#           groups by origin time (early / middle / late). For each group the
#           script reports n, the median error of C3 and of BEST (the frozen
#           best similarity-free method, chosen exactly as in 26_04), the median
#           paired difference C3 - BEST, and the fractions better / tied / worse.
#           A Spearman rank correlation between origin-time rank and the paired
#           difference is added. No test statistic is used for a claim.
#
# Inputs (read only)
#   ~/SWIFT/models/{23_01,23_02,23_03}_summary.json
#   ~/SWIFT/models/21_10_gmpe_location_error.json
#   ~/SWIFT/models/{21_04,21_20,25_05}_judgment.json
#   ~/SWIFT/data/{21_04,21_20,25_05}_per_event.csv
# Output
#   ~/SWIFT/models/26_09_reviewer_checks.json   (new file; nothing else written)
# Usage
#   cd ~/SWIFT && python3 ~/Downloads/26_09_reviewer_checks.py
#   (options: --root ~/SWIFT  --maxchars 6000)
# =============================================================================
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

SEQ = [("Central Tottori 2016", "21_04"), ("Northern Osaka 2018", "21_20"),
       ("Western Shimane 2018", "25_05")]
BASE = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]  # same list as 26_04
# BEST names written by 26_04 (frozen); the script recomputes them and stops on a mismatch.
EXPECTED_BEST = {("21_04", "0.5"): "M6r", ("21_04", "2"): "M6r",
                 ("21_20", "0.5"): "M6p", ("21_20", "2"): "M5f",
                 ("25_05", "0.5"): "M6p", ("25_05", "2"): "M6r"}
TAUS = ("0.5", "2")


def stop(msg):
    print("\nSTOP:", msg)
    sys.exit(1)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def best_of(S, t):  # identical to 26_04_paper_effect_sizes.py
    full = [m for m in BASE if S[m][t]["available"] == 1.0 and S[m][t]["median_km"] is not None]
    return min(full, key=lambda m: S[m][t]["median_km"])


def dump(obj, maxchars):
    s = json.dumps(obj, indent=1, ensure_ascii=False, default=str)
    return s if len(s) <= maxchars else s[:maxchars] + f"\n... [truncated, {len(s)} chars total]"


def spearman(x, y):
    rx = pd.Series(x).rank().to_numpy(); ry = pd.Series(y).rank().to_numpy()
    if np.std(rx) == 0 or np.std(ry) == 0:
        return float("nan")
    return float(np.corrcoef(rx, ry)[0, 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="~/SWIFT")
    ap.add_argument("--maxchars", type=int, default=6000)
    a = ap.parse_args()
    R = Path(os.path.expanduser(a.root))
    M, D = R / "models", R / "data"
    print("26_09 reviewer checks | python", sys.version.split()[0], "| numpy", np.__version__,
          "| pandas", pd.__version__, "|", time.strftime("%Y-%m-%d %H:%M:%S"))
    out = {"script": "26_09_reviewer_checks.py v1", "script_sha256_16": sha(__file__),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "inputs": {},
           "partA_note": "printed only, not copied", "partB": []}

    # ---------------- Part A: stored results, printed as they are ----------------
    print("\n" + "#" * 78 + "\n# PART A  stored results (read only)\n" + "#" * 78)
    for name in ("23_01_summary.json", "23_02_summary.json", "23_03_summary.json",
                 "21_10_gmpe_location_error.json"):
        p = M / name
        print("\n" + "=" * 78 + f"\n{p}")
        if not p.exists():
            print("  NOT FOUND"); continue
        out["inputs"][name] = sha(p)
        J = json.load(open(p))
        keys = [k for k in ("summary", "gates", "limits", "results", "conversion", "models")
                if k in J]
        for k in keys:
            print(f"--- {k} ---")
            print(dump(J[k], a.maxchars))

    # ---------------- Part B: gain by position in the test period ----------------
    print("\n" + "#" * 78 + "\n# PART B  gain by position in the test period (descriptive)\n" + "#" * 78)
    for lab, k in SEQ:
        pj, pe = M / f"{k}_judgment.json", D / f"{k}_per_event.csv"
        for p in (pj, pe):
            if not p.exists():
                stop(f"missing {p}")
            out["inputs"][p.name] = sha(p)
        J = json.load(open(pj)); E = pd.read_csv(pe)
        t_utc = pd.to_datetime(E["origin_time"], utc=True, format="mixed")
        order = np.argsort(t_utc.to_numpy(), kind="stable")
        n = len(E)
        group = np.empty(n, dtype=object)
        for gi, part in enumerate(np.array_split(order, 3)):
            group[part] = ("early", "middle", "late")[gi]
        rank = np.empty(n); rank[order] = np.arange(n)
        print(f"\n{lab} ({k}): n={n}, test period {t_utc.min()} -> {t_utc.max()} (UTC)")
        for t in TAUS:
            b = best_of(J["summary"], t)
            if b != EXPECTED_BEST[(k, t)]:
                stop(f"BEST mismatch for {k} tau={t}: {b} vs 26_04 {EXPECTED_BEST[(k, t)]}")
            c3 = E[f"C3_err_t{t}"].to_numpy(float); bb = E[f"{b}_err_t{t}"].to_numpy(float)
            d = c3 - bb; ok = np.isfinite(d)
            rho = spearman(rank[ok], d[ok])
            print(f"  tau={t} s  BEST={b}  Spearman(rank, C3-BEST)={rho:+.3f}  (negative d = C3 better)")
            print(f"    {'group':7s} {'n':>4s} {'first UTC':>20s} {'med C3':>7s} {'med BEST':>8s} "
                  f"{'med d':>7s} {'better':>6s} {'tied':>5s} {'worse':>6s}")
            for g in ("early", "middle", "late"):
                m = ok & (group == g)
                rec = dict(sequence=lab, key=k, tau=t, best=b, group=g, n=int(m.sum()),
                           first_utc=str(t_utc[m].min()), last_utc=str(t_utc[m].max()),
                           median_C3_km=round(float(np.median(c3[m])), 3),
                           median_BEST_km=round(float(np.median(bb[m])), 3),
                           median_diff_km=round(float(np.median(d[m])), 3),
                           frac_better=round(float(np.mean(d[m] < 0)), 3),
                           frac_tied=round(float(np.mean(d[m] == 0)), 3),
                           frac_worse=round(float(np.mean(d[m] > 0)), 3),
                           spearman_rank_vs_diff=round(rho, 3))
                out["partB"].append(rec)
                print(f"    {g:7s} {rec['n']:4d} {rec['first_utc'][:19]:>20s} {rec['median_C3_km']:7.2f} "
                      f"{rec['median_BEST_km']:8.2f} {rec['median_diff_km']:+7.2f} {rec['frac_better']:6.2f} "
                      f"{rec['frac_tied']:5.2f} {rec['frac_worse']:6.2f}")
            # sanity: overall medians must equal the frozen judgment
            fz3 = J["summary"]["C3"][t]["median_km"] if "C3" in J["summary"] else None
            fzb = J["summary"][b][t]["median_km"]
            print(f"    check overall medians: C3 {np.median(c3[ok]):.4f} (frozen {fz3}), "
                  f"BEST {np.median(bb[ok]):.4f} (frozen {fzb})")

    op = M / "26_09_reviewer_checks.json"
    json.dump(out, open(op, "w"), indent=1)
    print(f"\nwrote {op}\nDONE")


if __name__ == "__main__":
    main()
