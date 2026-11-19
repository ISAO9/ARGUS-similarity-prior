#!/usr/bin/env python3
# =============================================================================
# Script : 26_05_set_size_control.py  (v1)
# Project: ARGUS (SRL resubmission) — set-size control for C3 (descriptive, NOT registered)
#
# Question
#   C3 builds its prior from the 10 most similar past events, while the reference
#   M6r builds it from all past events with the same first-P station (at least 5,
#   often many more). Is the gain of C3 due to the similarity, or only to a smaller,
#   more concentrated set of 10 events?
#
# What this script does (runs on the Mac in ~/SWIFT; reads only frozen files)
#   1. Loads the FROZEN similarity script of one sequence (21_04, 21_20 or 25_05) as
#      text, checks its SHA-256 against the frozen judgment JSON, and executes only
#      its input, coordinate, velocity, grid, prior, similarity and method sections
#      (up to section "9. 評価"). The one-shot "opened" record block is NOT executed,
#      so no registered record, judgment or CSV is written or changed.
#   2. For every evaluated test event and tau in {0.5, 2} s it recomputes
#        M6r (prior from the same-first-P-station past events, set m3), and
#        C3  (prior from the 10 most similar past events),
#      and STOPs unless both equal the frozen per-event CSV errors (|diff| <= 1e-4 km).
#   3. It then computes two controls with the SAME physics and the SAME prior rule,
#      changing only the set of past events, chosen WITHOUT similarity from m3:
#        R10    : 10 events drawn at random from m3 (20 draws, seeds 0..19; when m3
#                 holds 10 events or fewer, all of m3 is used, i.e. the control = M6r)
#        Late10 : the 10 most recent events of m3
#   4. Writes per-event errors and a summary (median error per method and tau; for R10
#      the median over draws of the per-draw median; paired comparison C3 vs R10 by the
#      fraction of events where C3 is better than the draw-median R10 error).
# Outputs: data/26_05_set_size_control_<seq>.csv, data/26_05_set_size_control_<seq>.json
# Usage  : cd ~/SWIFT && uv run python src/26_05_set_size_control.py --seq ct2016
#          (then --seq osaka and --seq shimane; --draws 20 by default)
# =============================================================================
import argparse, hashlib, json, sys, time
from pathlib import Path
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--seq", required=True, choices=["ct2016", "osaka", "shimane"])
ap.add_argument("--draws", type=int, default=20)
ap.add_argument("--base", default=".", help="~/SWIFT (holds src/, models/, data/)")
ap.add_argument("--dev", action="store_true", help="check mode on the frozen dev outputs (*_dev files); no test event is touched")
A = ap.parse_args()
BASE = Path(A.base).resolve()
CFG = {"ct2016": ("src/21_04_ct2016_similarity_confirmation.py", "models/21_04_judgment.json", "data/21_04_per_event.csv", []),
       "osaka": ("src/21_20_osaka2018_similarity_confirmation.py", "models/21_20_judgment.json", "data/21_20_per_event.csv", []),
       "shimane": ("src/25_05_shimane2018_similarity_confirmation.py", "models/25_05_judgment.json", "data/25_05_per_event.csv",
                   ["--no-causal"])}
SP, JP, CP, EXTRA = CFG[A.seq]
if A.dev:
    JP, CP, EXTRA = JP.replace(".json", "_dev.json"), CP.replace(".csv", "_dev.csv"), EXTRA + ["--dev"]
SP, JP, CP = BASE / SP, BASE / JP, BASE / CP
for p in (SP, JP, CP):
    if not p.exists(): sys.exit(f"[26_05] STOP: missing {p}")
J = json.load(open(JP))
src = SP.read_text(encoding="utf-8")
if hashlib.sha256(SP.read_bytes()).hexdigest() != J["script_sha256"]:
    sys.exit(f"[26_05] STOP: {SP.name} is not the frozen script (SHA-256 differs from {JP.name})")
M_OPEN = "# ---------------------------------------------------------------- 1 回だけの記録"
M_PICKS = "def picks_of(ie, tau=np.inf):"
M_EVAL = "# ---------------------------------------------------------------- 9. 評価"
for m in (M_OPEN, M_PICKS, M_EVAL):
    if src.count(m) != 1: sys.exit(f"[26_05] STOP: marker not found exactly once in {SP.name}: {m[:40]}")
i0, i1, i2 = src.index(M_OPEN), src.index(M_PICKS), src.index(M_EVAL)
if not (i0 < i1 < i2): sys.exit("[26_05] STOP: unexpected section order in the frozen script")
# the opened-record block is replaced by a stop() that only raises (no file is written)
code = src[:i0] + "\nSUF = '_26_05'\nIN_H5 = False\ndef stop(msg):\n    raise SystemExit(msg)\n\n" + src[i1:i2]
sys.argv = [str(SP), "--cache", J["cache"]] + EXTRA
NS = {"__file__": str(SP), "__name__": "frozen_core"}
t0 = time.time()
print(f"[26_05] {A.seq}: executing the frozen sections 1–7 of {SP.name} (SHA-256 {J['script_sha256'][:12]}…; no record is written)")
exec(compile(code, str(SP), "exec"), NS)
g = NS
EVAL, FIRST, POOL_OK = g["EVAL"], g["FIRST"], g["POOL_OK"]
library, prior_members, locate_map, picks_of = g["library"], g["prior_members"], g["locate_map"], g["picks_of"]
similarity, c_from, to_ll, km_between, SRC, BAND, TOPK = g["similarity"], g["c_from"], g["to_ll"], g["km_between"], g["SRC"], g["BAND"], g["TOPK"]
OTNS = g["OTNS"]
if len(EVAL) != J["n_evaluated"]: sys.exit(f"[26_05] STOP: {len(EVAL)} evaluated events != frozen {J['n_evaluated']}")

import csv
rows_csv = list(csv.DictReader(open(CP)))
if len(rows_csv) != len(EVAL): sys.exit("[26_05] STOP: per-event CSV rows != evaluated events")


def err(ie, xy):
    la, lo = to_ll(xy[0], xy[1]); return km_between(la, lo, SRC[ie, 0], SRC[ie, 1])


TAUS = ["0.5", "2"]
out_rows, maxdiff = [], 0.0
for ii, ie in enumerate(EVAL):
    lib = library(ie); p0 = FIRST[ie]; m3 = prior_members(lib, p0[0], (p0[1], p0[2]))
    rec = dict(origin_time=rows_csv[ii]["origin_time"], n_m3=int(len(m3)))
    for t in TAUS:
        tau = float(t); pk = picks_of(ie, tau)
        m6r = locate_map(pk, m3); e6 = err(ie, m6r)
        S, ni = similarity(ie, tau, lib, BAND); o = c_from(S, lib, pk, m3, m6r, TOPK, ie=ie, with_c4=False)
        e3 = err(ie, o["C3"])
        for name, v in (("M6r", e6), ("C3", e3)):
            fz = float(rows_csv[ii][f"{name}_err_t{t}"]); d = abs(round(v, 4) - fz); maxdiff = max(maxdiff, d)
            if d > 1e-4: sys.exit(f"[26_05] STOP: recomputed {name} at tau {t} for {rec['origin_time']} = {v:.4f} km, frozen {fz:.4f} km")
        late = m3[np.argsort(OTNS[m3], kind="stable")[-10:]] if len(m3) > 10 else m3
        eL = err(ie, locate_map(pk, late))
        eR = []
        for sd in range(A.draws):
            sub = np.random.default_rng(sd).choice(m3, 10, replace=False) if len(m3) > 10 else m3
            eR.append(err(ie, locate_map(pk, np.sort(sub))))
        rec.update({f"M6r_t{t}": round(e6, 4), f"C3_t{t}": round(e3, 4), f"Late10_t{t}": round(eL, 4),
                    f"R10_drawmedian_t{t}": round(float(np.median(eR)), 4)})
        rec.update({f"R10_d{sd}_t{t}": round(v, 4) for sd, v in enumerate(eR)})
    out_rows.append(rec)
    if (ii + 1) % 10 == 0: print(f"  … {ii + 1}/{len(EVAL)}  ({time.time() - t0:.0f} s)")

summ = {}
for t in TAUS:
    c3 = np.array([r[f"C3_t{t}"] for r in out_rows]); m6 = np.array([r[f"M6r_t{t}"] for r in out_rows])
    lt = np.array([r[f"Late10_t{t}"] for r in out_rows]); rm = np.array([r[f"R10_drawmedian_t{t}"] for r in out_rows])
    per_draw = [float(np.median([r[f"R10_d{sd}_t{t}"] for r in out_rows])) for sd in range(A.draws)]
    summ[t] = dict(median_km=dict(C3=float(np.median(c3)), M6r=float(np.median(m6)), Late10=float(np.median(lt)),
                                  R10_median_of_draw_medians=float(np.median(per_draw)), R10_min_draw_median=float(np.min(per_draw)),
                                  R10_max_draw_median=float(np.max(per_draw))),
                   C3_vs_R10=dict(frac_better=float(np.mean(c3 < rm)), frac_tied=float(np.mean(c3 == rm)), frac_worse=float(np.mean(c3 > rm))),
                   C3_vs_Late10=dict(frac_better=float(np.mean(c3 < lt)), frac_tied=float(np.mean(c3 == lt)), frac_worse=float(np.mean(c3 > lt))),
                   events_with_m3_le_10=int(sum(r["n_m3"] <= 10 for r in out_rows)))
res = dict(script="26_05_set_size_control.py", version="v1", sequence=A.seq, frozen_script=SP.name, frozen_script_sha256=J["script_sha256"],
           cache=J["cache"], n_events=len(EVAL), draws=A.draws, max_abs_diff_vs_frozen_km=maxdiff, median_n_m3=float(np.median([r["n_m3"] for r in out_rows])),
           summary=summ, note="descriptive control, not registered; same physics and prior rule as M6r and C3, only the set of past events differs")
OUT = BASE / "data"; OUT.mkdir(exist_ok=True)
TAG = A.seq + ("_dev" if A.dev else "")
json.dump(res, open(OUT / f"26_05_set_size_control_{TAG}.json", "w"), indent=1)
with open(OUT / f"26_05_set_size_control_{TAG}.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys())); w.writeheader(); w.writerows(out_rows)
print(f"[26_05] {A.seq}: M6r and C3 reproduced the frozen errors (max |diff| {maxdiff:.1e} km) for {len(EVAL)} events")
for t in TAUS:
    s = summ[t]["median_km"]
    print(f"[26_05] tau {t} s  median km: C3 {s['C3']:.3f}  R10 {s['R10_median_of_draw_medians']:.3f} "
          f"(draws {s['R10_min_draw_median']:.3f}-{s['R10_max_draw_median']:.3f})  Late10 {s['Late10']:.3f}  M6r {s['M6r']:.3f}  "
          f"| C3 better than R10 {summ[t]['C3_vs_R10']['frac_better']:.2f}, tied {summ[t]['C3_vs_R10']['frac_tied']:.2f}")
print(f"[26_05] wrote data/26_05_set_size_control_{TAG}.json and .csv  ({time.time() - t0:.0f} s)")
