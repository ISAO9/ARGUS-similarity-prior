#!/usr/bin/env python3
# =============================================================================
# Script : 26_12_causal_mean_check.py  (v1)
# Project: ARGUS (SRL resubmission) — effect of the non-causal mean removal of the
#          stored traces. Descriptive check, NOT registered. Runs on the Mac in ~/SWIFT.
#
# Question
#   Each stored trace (20.48 s, P pick at sample IP = 300, i.e. 3 s after the window
#   start) was differentiated and had its mean over the whole window removed when the
#   cache was built. That mean uses samples after the time of the estimate. A reviewer
#   may ask whether this non-causal constant changes the similarity and the results.
#
# What this script does (reads only frozen files; writes two new files)
#   1. Executes sections 1-7 of the FROZEN similarity script of one sequence (21_04,
#      21_20 or 25_05) after checking its SHA-256, exactly as 26_05 and 26_10 do. The
#      one-shot "opened" record block is not executed; no registered file is touched.
#   2. Gate: recomputes M6r, C3 and C4 for every evaluated test event at tau = 0.5 and
#      2 s with the cached traces and STOPs unless all equal the frozen per-event CSV
#      (|diff| <= 1e-4 km).
#   3. Causal mean: for every cached event and station, subtracts from the stored trace
#      the mean of its own pre-P samples [0, IP - 10) (the 2.9 s that end 0.1 s before
#      the P pick), per component. Because the stored trace equals x - mean(x), this
#      gives x - mean_pre(x): the mean is then taken only from data recorded before the
#      P arrival, and therefore before any estimate time tau >= 0. The waveform filter
#      cache is cleared, and C3 and C4 are recomputed with the same rules. M6r does not
#      use waveforms and must stay identical (checked).
#   4. Summary per tau: medians of C3 and C4 before and after, number of events whose
#      error changed, the largest change, and the registered win rule (median below
#      BEST, one-sided Wilcoxon p below alpha, >= 10 non-zero pairs, BEST >= 0.5-km
#      floor) applied to H1 (C3, 2 s, alpha 0.01), H2 (C4, 2 s, 0.005) and H3 (C3,
#      0.5 s, 0.005) with the cached and with the causal traces. BEST is chosen by the
#      rule of 26_04 from the frozen judgment and does not use waveforms.
#
# Inputs : src/{21_04,21_20,25_05}_*_similarity_confirmation.py (frozen),
#          models/<key>_judgment.json, data/<key>_per_event.csv, the frozen cache
# Outputs: data/26_12_causal_mean_<seq>.csv, data/26_12_causal_mean_<seq>.json
# Usage  : cd ~/SWIFT && caffeinate -i uv run python src/26_12_causal_mean_check.py --seq ct2016
#          (then --seq osaka and --seq shimane)
# =============================================================================
import argparse, csv, hashlib, json, sys, time
from pathlib import Path
import numpy as np
from scipy.stats import wilcoxon

ap = argparse.ArgumentParser()
ap.add_argument("--seq", required=True, choices=["ct2016", "osaka", "shimane"])
ap.add_argument("--base", default=".", help="~/SWIFT (holds src/, models/, data/)")
ap.add_argument("--gap", type=int, default=10, help="samples left out before the P pick (default 10 = 0.1 s)")
ap.add_argument("--dev", action="store_true", help="plumbing check on the frozen dev outputs (*_dev files)")
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
    if not p.exists(): sys.exit(f"[26_12] STOP: missing {p}")
J = json.load(open(JP))
src = SP.read_text(encoding="utf-8")
if hashlib.sha256(SP.read_bytes()).hexdigest() != J["script_sha256"]:
    sys.exit(f"[26_12] STOP: {SP.name} is not the frozen script (SHA-256 differs from {JP.name})")
M_OPEN = "# ---------------------------------------------------------------- 1 回だけの記録"
M_PICKS = "def picks_of(ie, tau=np.inf):"
M_EVAL = "# ---------------------------------------------------------------- 9. 評価"
for m in (M_OPEN, M_PICKS, M_EVAL):
    if src.count(m) != 1: sys.exit(f"[26_12] STOP: marker not found exactly once in {SP.name}: {m.strip()[:40]}")
i0, i1, i2 = src.index(M_OPEN), src.index(M_PICKS), src.index(M_EVAL)
if not (i0 < i1 < i2): sys.exit("[26_12] STOP: unexpected section order in the frozen script")
CORE = src[:i0] + "\nSUF = '_26_12'\nIN_H5 = False\ndef stop(msg):\n    raise SystemExit(msg)\n\n" + src[i1:i2]
sys.argv = [str(SP), "--cache", J["cache"]] + EXTRA
g = {"__file__": str(SP), "__name__": "frozen_core"}
t0 = time.time()
print(f"[26_12] {A.seq}: executing the frozen sections 1-7 of {SP.name} (SHA-256 {J['script_sha256'][:12]}…; no record is written)")
exec(compile(CORE, str(SP), "exec"), g)
EVAL, EVS, IP = g["EVAL"], g["EVS"], int(g["IP"])
if len(EVAL) != J["n_evaluated"]: sys.exit(f"[26_12] STOP: {len(EVAL)} evaluated events != frozen {J['n_evaluated']}")
rows = list(csv.DictReader(open(CP)))
if len(rows) != len(EVAL): sys.exit("[26_12] STOP: per-event CSV rows != evaluated events")
TAUS = ["0.5", "2"]
BASE9 = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]   # same list as 26_04


def best_of(S, t):  # identical to 26_04
    full = [m for m in BASE9 if S[m][t]["available"] == 1.0 and S[m][t]["median_km"] is not None]
    return min(full, key=lambda m: S[m][t]["median_km"])


def err(ie, xy):
    la, lo = g["to_ll"](xy[0], xy[1]); return g["km_between"](la, lo, g["SRC"][ie, 0], g["SRC"][ie, 1])


def run_all():
    """M6r, C3, C4 errors for every evaluated event and tau, with the current traces."""
    out = {}
    for ii, ie in enumerate(EVAL):
        lib = g["library"](ie); p0 = g["FIRST"][ie]; m3 = g["prior_members"](lib, p0[0], (p0[1], p0[2]))
        for t in TAUS:
            pk = g["picks_of"](ie, float(t)); m6r = g["locate_map"](pk, m3)
            S, _ = g["similarity"](ie, float(t), lib, g["BAND"])
            o = g["c_from"](S, lib, pk, m3, m6r, g["TOPK"], ie=ie, with_c4=True)
            out[(ii, t)] = dict(M6r=err(ie, m6r), C3=err(ie, o["C3"]), C4=err(ie, o["C4"]), Smax=float(S.max()) if len(S) else 0.0)
        if (ii + 1) % 20 == 0: print(f"  … {ii + 1}/{len(EVAL)}  ({time.time() - t0:.0f} s)")
    return out


# ---- step 2: gate with the cached traces --------------------------------------------------------
R0 = run_all(); maxdiff = 0.0
for (ii, t), v in R0.items():
    for m in ("M6r", "C3", "C4"):
        fz = float(rows[ii][f"{m}_err_t{t}"]); d = abs(round(v[m], 4) - fz); maxdiff = max(maxdiff, d)
        if d > 1e-4: sys.exit(f"[26_12] STOP: recomputed {m} at tau {t} for {rows[ii]['origin_time']} = {v[m]:.4f}, frozen {fz:.4f}")
print(f"[26_12] gate PASS: M6r, C3 and C4 equal the frozen errors (max |diff| {maxdiff:.1e} km) for {len(EVAL)} events")

# ---- step 3: causal mean --------------------------------------------------------------------------
n_tr, pre_end = 0, IP - A.gap
if pre_end < 50: sys.exit("[26_12] STOP: too few pre-P samples")
shift_abs = []
for e in EVS:
    W = np.array(np.asarray(e["waveforms"]), dtype=np.float64, copy=True)
    n = int(e["n_real_stations"])
    if W.ndim != 3 or W.shape[0] < n or W.shape[2] <= IP: sys.exit(f"[26_12] STOP: unexpected trace shape {W.shape}")
    for k in range(n):
        mu = W[k, :, :pre_end].mean(axis=1, keepdims=True)
        shift_abs.append(float(np.max(np.abs(mu)) / (np.std(W[k]) + 1e-30)))
        W[k] -= mu; n_tr += 1
    e["waveforms"] = W.astype(np.float32)
g["FILT"].clear()
print(f"[26_12] causal mean applied to {n_tr} stored traces (pre-P samples 0-{pre_end - 1}); "
      f"median |pre-P mean| / trace std = {np.median(shift_abs):.3g}, 99th percentile {np.percentile(shift_abs, 99):.3g}")
R1 = run_all()
for k in R0:
    if abs(R0[k]["M6r"] - R1[k]["M6r"]) > 1e-9: sys.exit("[26_12] STOP: M6r changed, but it does not use waveforms")
dS = np.array([R1[k]["Smax"] - R0[k]["Smax"] for k in R0])
print(f"[26_12] change of the maximum similarity per event: median |dS| = {np.median(np.abs(dS)):.2e}, largest {np.max(np.abs(dS)):.2e}")

# ---- step 4: summary ------------------------------------------------------------------------------
HYP = [("H1", "C3", "2", 0.01), ("H2", "C4", "2", 0.005), ("H3", "C3", "0.5", 0.005)]
SUMM = {"per_tau": {}, "hypotheses": {}}
for t in TAUS:
    b = best_of(J["summary"], t)
    rec = dict(best=b)
    for m in ("C3", "C4"):
        a0 = np.array([R0[(ii, t)][m] for ii in range(len(EVAL))]); a1 = np.array([R1[(ii, t)][m] for ii in range(len(EVAL))])
        dd = a1 - a0
        rec[m] = dict(median_cached_km=float(np.median(a0)), median_causal_km=float(np.median(a1)),
                      n_changed=int(np.sum(np.abs(dd) > 1e-4)), max_abs_change_km=float(np.max(np.abs(dd))),
                      median_change_km=float(np.median(dd)))
    SUMM["per_tau"][t] = rec


def win(meth_err, best_err, alpha):
    d = meth_err - best_err; nz = int(np.sum(d != 0))
    p = float(wilcoxon(d, zero_method="wilcox", alternative="less").pvalue) if nz > 0 else None
    mb, mm = float(np.median(best_err)), float(np.median(meth_err))
    floor = mb < 0.5
    w = (not floor) and mm < mb and p is not None and p < alpha and nz >= 10
    return dict(median_km=mm, best_median_km=mb, p=p, n_nonzero=nz, frac_better=float(np.mean(d < 0)), frac_tied=float(np.mean(d == 0)),
                outcome="PHYSICS-AT-FLOOR" if floor else ("win" if w else "no win"))


for h, m, t, alpha in HYP:
    b = SUMM["per_tau"][t]["best"]
    be = np.array([float(r[f"{b}_err_t{t}"]) for r in rows])
    a0 = np.array([R0[(ii, t)][m] for ii in range(len(EVAL))]); a1 = np.array([R1[(ii, t)][m] for ii in range(len(EVAL))])
    SUMM["hypotheses"][h] = dict(method=m, tau=t, alpha=alpha, best=b, cached=win(a0, be, alpha), causal=win(a1, be, alpha))

res = dict(script="26_12_causal_mean_check.py", version="v1", sequence=A.seq, frozen_script=SP.name, frozen_script_sha256=J["script_sha256"],
           cache=J["cache"], n_events=len(EVAL), pre_p_samples=[0, pre_end], n_traces=n_tr, max_abs_change_Smax=float(np.max(np.abs(dS))), gate_max_abs_diff_km=maxdiff, summary=SUMM,
           note="descriptive, not registered; the stored traces are re-centred on their pre-P mean; M6r and BEST do not use waveforms")
OUT = BASE / "data"; OUT.mkdir(exist_ok=True)
TAG = A.seq + ("_dev" if A.dev else "")
json.dump(res, open(OUT / f"26_12_causal_mean_{TAG}.json", "w"), indent=1)
with open(OUT / f"26_12_causal_mean_{TAG}.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["origin_time", "tau", "C3_cached", "C3_causal", "C4_cached", "C4_causal", "M6r"])
    for ii in range(len(EVAL)):
        for t in TAUS:
            w.writerow([rows[ii]["origin_time"], t] + [round(R0[(ii, t)]["C3"], 4), round(R1[(ii, t)]["C3"], 4),
                                                     round(R0[(ii, t)]["C4"], 4), round(R1[(ii, t)]["C4"], 4), round(R0[(ii, t)]["M6r"], 4)])
print(f"\n[26_12] {A.seq}: {len(EVAL)} events")
for t in TAUS:
    r = SUMM["per_tau"][t]
    for m in ("C3", "C4"):
        x = r[m]
        print(f"  tau {t:>3s} s {m}: median {x['median_cached_km']:.3f} -> {x['median_causal_km']:.3f} km; "
              f"changed {x['n_changed']}/{len(EVAL)} events; largest change {x['max_abs_change_km']:.3f} km")
for h, v in SUMM["hypotheses"].items():
    c0, c1 = v["cached"], v["causal"]
    f = lambda p: "—" if p is None else f"{p:.2g}"
    print(f"  {h} ({v['method']} vs {v['best']}, tau {v['tau']} s, alpha {v['alpha']}): cached {c0['median_km']:.2f} vs {c0['best_median_km']:.2f}, "
          f"p {f(c0['p'])}, {c0['outcome']} | causal {c1['median_km']:.2f}, p {f(c1['p'])}, {c1['outcome']}")
print(f"[26_12] wrote data/26_12_causal_mean_{TAG}.json and .csv  ({time.time() - t0:.0f} s)")
