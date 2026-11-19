#!/usr/bin/env python3
# =============================================================================
# Script : 26_10_memory_truncation.py  (v1)
# Project: ARGUS (SRL resubmission) — "how early does the memory help?"
#          Descriptive check, NOT registered. Runs on the Mac in ~/SWIFT.
#
# Question
#   Every registered test scored events later than mainshock + 72 h. The first 72 h
#   (the pool) fitted the physics and seeded the memory. A reviewer will ask how the
#   method behaves earlier in a sequence, when the memory is short. Scoring the pool
#   events themselves would be in-sample for every method, so this script keeps the
#   FROZEN test events and shortens only what the methods are allowed to know.
#
# What this script does (reads only frozen files; writes two new files)
#   1. Loads the FROZEN similarity script of one sequence (21_04, 21_20 or 25_05),
#      checks its SHA-256 against the frozen judgment JSON, and executes only its
#      sections 1-7 (input ... methods), exactly as 26_05 does. The one-shot
#      "opened" record block is NOT executed, so no registered file is touched.
#   2. Reproduction gate: for every evaluated test event and tau in {0.5, 2} s,
#      M6r and C3 with the full memory must equal the frozen per-event CSV
#      (|diff| <= 1e-4 km), else STOP.
#   3. Memory truncation. For T in {1, 3, 6, 12, 24, 48, 72} h, the past-event list
#      of each target is cut to events with origin time <= mainshock + T h
#      (the 1-h buffer before the target is kept, as in the frozen rule).
#      M6r_T (prior from the same-first-P-station events of the cut list) and
#      C3_T (prior from the 10 most similar events of the cut list; the frozen
#      fallback C3 = M6r applies when fewer than 5 events have S > 0) are computed
#      with the frozen rules. The similarity S of each past event depends only on
#      the two waveforms, so S is computed once on the full list and subset.
#      Two variants:
#        A "fixed"  : velocity, station terms, residual scale, KDE bandwidth, grid
#                     and fixed depth stay as fitted on the 72-h pool (frozen).
#        B "refit"  : the same quantities are refitted on the pool events up to
#                     mainshock + T h only (the frozen code is executed again with
#                     only the calibration list CAL restricted; the test events,
#                     picks and all rules are unchanged). Skipped for a T with
#                     fewer than --min-cal calibration events.
#      Consistency gates: S recomputed in each refit namespace equals the reused S
#      for the first 3 events; B at T = 72 h equals A at T = 72 h (|diff| <= 1e-4 km).
#   4. Summary per variant, T and tau: number of scored events, median error of C3_T
#      and M6r_T, median paired difference C3_T - M6r_T, fractions better/tied/worse,
#      median length of the cut list, fraction of C3 fallbacks; the frozen
#      full-memory C3 and M6r medians are given as the reference row "all".
#
# Limits (also written into the JSON)
#   - Descriptive only; the registered verdicts are not changed.
#   - The test events are the same late events (> 72 h); only the knowledge is cut.
#     Waveform overlap and catalog incompleteness of the first hours are therefore
#     not reproduced.
#   - Variant A uses physics fitted on 72 h of data that an early system would not have.
#
# Inputs : src/{21_04,21_20,25_05}_*_similarity_confirmation.py (frozen),
#          models/<key>_judgment.json, data/<key>_per_event.csv, the frozen cache
# Outputs: data/26_10_memory_truncation_<seq>.csv, data/26_10_memory_truncation_<seq>.json
# Usage  : cd ~/SWIFT && caffeinate -i uv run python src/26_10_memory_truncation.py --seq ct2016
#          (then --seq osaka and --seq shimane)
# =============================================================================
import argparse, csv, hashlib, json, sys, time
from pathlib import Path
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--seq", required=True, choices=["ct2016", "osaka", "shimane"])
ap.add_argument("--base", default=".", help="~/SWIFT (holds src/, models/, data/)")
ap.add_argument("--hours", default="1,3,6,12,24,48,72", help="memory cut-offs T after the mainshock (h)")
ap.add_argument("--min-cal", type=int, default=10, help="minimum calibration events for variant B")
ap.add_argument("--no-refit", action="store_true", help="run variant A only")
ap.add_argument("--dev", action="store_true", help="plumbing check on the frozen dev outputs (*_dev files)")
A = ap.parse_args()
BASE = Path(A.base).resolve()
HOURS = [float(h) for h in A.hours.split(",")]
if 72.0 not in HOURS: sys.exit("[26_10] STOP: --hours must contain 72 (used by the consistency gate)")
CFG = {"ct2016": ("src/21_04_ct2016_similarity_confirmation.py", "models/21_04_judgment.json", "data/21_04_per_event.csv", []),
       "osaka": ("src/21_20_osaka2018_similarity_confirmation.py", "models/21_20_judgment.json", "data/21_20_per_event.csv", []),
       "shimane": ("src/25_05_shimane2018_similarity_confirmation.py", "models/25_05_judgment.json", "data/25_05_per_event.csv",
                   ["--no-causal"])}
SP, JP, CP, EXTRA = CFG[A.seq]
if A.dev:
    JP, CP, EXTRA = JP.replace(".json", "_dev.json"), CP.replace(".csv", "_dev.csv"), EXTRA + ["--dev"]
SP, JP, CP = BASE / SP, BASE / JP, BASE / CP
for p in (SP, JP, CP):
    if not p.exists(): sys.exit(f"[26_10] STOP: missing {p}")
J = json.load(open(JP))
src = SP.read_text(encoding="utf-8")
if hashlib.sha256(SP.read_bytes()).hexdigest() != J["script_sha256"]:
    sys.exit(f"[26_10] STOP: {SP.name} is not the frozen script (SHA-256 differs from {JP.name})")
M_OPEN = "# ---------------------------------------------------------------- 1 回だけの記録"
M_PICKS = "def picks_of(ie, tau=np.inf):"
M_EVAL = "# ---------------------------------------------------------------- 9. 評価"
M_CAL = "\nCAL = [ie for ie in pool_idx if HASP[ie]]\n"
for m in (M_OPEN, M_PICKS, M_EVAL, M_CAL):
    if src.count(m) != 1: sys.exit(f"[26_10] STOP: marker not found exactly once in {SP.name}: {m.strip()[:40]}")
i0, i1, i2 = src.index(M_OPEN), src.index(M_PICKS), src.index(M_EVAL)
if not (src.index(M_CAL) < i0 < i1 < i2): sys.exit("[26_10] STOP: unexpected section order in the frozen script")
# the opened-record block is replaced by a stop() that only raises (no file is written); same as 26_05
CORE = src[:i0] + "\nSUF = '_26_10'\nIN_H5 = False\ndef stop(msg):\n    raise SystemExit(msg)\n\n" + src[i1:i2]
ARGV = [str(SP), "--cache", J["cache"]] + EXTRA


def run_frozen(cal_hours=None):
    """Execute frozen sections 1-7. cal_hours=None: frozen calibration; else CAL cut to mainshock + cal_hours."""
    code = CORE
    if cal_hours is not None:
        new = (f"\nCAL = [ie for ie in pool_idx if HASP[ie] and OTNS[ie] <= OTNS[im] + int({cal_hours!r} * 3600e9)]\n")
        code = code.replace(M_CAL, new)
        if code.count(new) != 1: sys.exit("[26_10] STOP: could not restrict CAL")
    sys.argv = list(ARGV)
    ns = {"__file__": str(SP), "__name__": "frozen_core"}
    exec(compile(code, str(SP), "exec"), ns)
    return ns


t0 = time.time()
print(f"[26_10] {A.seq}: executing the frozen sections 1-7 of {SP.name} (SHA-256 {J['script_sha256'][:12]}…; no record is written)")
g0 = run_frozen()
EVAL, OTNS, IM = g0["EVAL"], g0["OTNS"], int(g0["im"])
MAIN_NS = int(OTNS[IM])
if len(EVAL) != J["n_evaluated"]: sys.exit(f"[26_10] STOP: {len(EVAL)} evaluated events != frozen {J['n_evaluated']}")
rows_csv = list(csv.DictReader(open(CP)))
if len(rows_csv) != len(EVAL): sys.exit("[26_10] STOP: per-event CSV rows != evaluated events")
CAL0 = np.array(g0["CAL"], int)
n_cal = {h: int(np.sum(OTNS[CAL0] <= MAIN_NS + int(h * 3600e9))) for h in HOURS}
print(f"[26_10] mainshock {g0['OT'][IM][:19]} UTC; calibration events with a P pick within T h: "
      + ", ".join(f"{h:g} h: {n_cal[h]}" for h in HOURS))
TAUS = ["0.5", "2"]


def err(g, ie, xy):
    la, lo = g["to_ll"](xy[0], xy[1]); return g["km_between"](la, lo, g["SRC"][ie, 0], g["SRC"][ie, 1])


# ---- step 2: reproduction with the full memory, and the similarity cache --------------------------
SC = {}           # (ii, tau) -> (lib, S)
out = [dict(origin_time=r["origin_time"]) for r in rows_csv]
maxdiff = 0.0
for ii, ie in enumerate(EVAL):
    lib = g0["library"](ie); p0 = g0["FIRST"][ie]; m3 = g0["prior_members"](lib, p0[0], (p0[1], p0[2]))
    out[ii]["n_lib_all"] = int(len(lib))
    for t in TAUS:
        pk = g0["picks_of"](ie, float(t))
        m6r = g0["locate_map"](pk, m3)
        S, _ = g0["similarity"](ie, float(t), lib, g0["BAND"])
        o = g0["c_from"](S, lib, pk, m3, m6r, g0["TOPK"], ie=ie, with_c4=False)
        e6, e3 = err(g0, ie, m6r), err(g0, ie, o["C3"])
        for name, v in (("M6r", e6), ("C3", e3)):
            fz = float(rows_csv[ii][f"{name}_err_t{t}"]); d = abs(round(v, 4) - fz); maxdiff = max(maxdiff, d)
            if d > 1e-4: sys.exit(f"[26_10] STOP: recomputed {name} at tau {t} for {rows_csv[ii]['origin_time']} = {v:.4f} km, frozen {fz:.4f} km")
        out[ii][f"all_M6r_t{t}"] = round(e6, 4); out[ii][f"all_C3_t{t}"] = round(e3, 4)
        SC[(ii, t)] = (lib, S)
    if (ii + 1) % 20 == 0: print(f"  reproduction … {ii + 1}/{len(EVAL)}  ({time.time() - t0:.0f} s)")
print(f"[26_10] reproduction gate PASS: M6r and C3 equal the frozen errors (max |diff| {maxdiff:.1e} km) for {len(EVAL)} events")


def truncated(g, tag, h, check_S=False):
    cut = MAIN_NS + int(h * 3600e9); nS = 0
    for ii, ie in enumerate(EVAL):
        p0 = g["FIRST"][ie]
        for t in TAUS:
            lib, S = SC[(ii, t)]
            if check_S and ii < 3:
                S2, _ = g["similarity"](ie, float(t), lib, g["BAND"])
                if not np.allclose(S2, S, rtol=0, atol=1e-12): sys.exit(f"[26_10] STOP: similarity differs in variant {tag} T={h:g} h")
                nS += 1
            keep = OTNS[lib] <= cut; libT, ST = lib[keep], S[keep]
            k = f"{tag}{h:g}h"
            out[ii][f"{k}_nlib"] = int(len(libT))
            if len(libT) == 0:
                out[ii][f"{k}_M6r_t{t}"] = out[ii][f"{k}_C3_t{t}"] = np.nan; out[ii][f"{k}_fb_t{t}"] = np.nan; continue
            m3 = g["prior_members"](libT, p0[0], (p0[1], p0[2]))
            pk = g["picks_of"](ie, float(t))
            m6r = g["locate_map"](pk, m3)
            o = g["c_from"](ST, libT, pk, m3, m6r, g["TOPK"], ie=ie, with_c4=False)
            out[ii][f"{k}_M6r_t{t}"] = round(err(g, ie, m6r), 4)
            out[ii][f"{k}_C3_t{t}"] = round(err(g, ie, o["C3"]), 4)
            out[ii][f"{k}_fb_t{t}"] = int(bool(o["fb"]))
    print(f"[26_10] variant {tag} T = {h:g} h done ({time.time() - t0:.0f} s)" + (f"; similarity check on {nS} cases PASS" if check_S else ""))


# ---- step 3A: fixed calibration ------------------------------------------------------------------
for h in HOURS:
    truncated(g0, "A", h)

# ---- step 3B: refitted calibration ---------------------------------------------------------------
skipped = {}
if not A.no_refit:
    for h in HOURS:
        if n_cal[h] < A.min_cal:
            skipped[f"{h:g}"] = f"only {n_cal[h]} calibration events (< {A.min_cal})"
            print(f"[26_10] variant B T = {h:g} h skipped: {skipped[f'{h:g}']}"); continue
        print(f"[26_10] variant B T = {h:g} h: re-executing the frozen sections with CAL cut to mainshock + {h:g} h")
        gT = run_frozen(cal_hours=h)
        if len(gT["CAL"]) != n_cal[h]: sys.exit("[26_10] STOP: refitted CAL size differs from the expected count")
        if not np.array_equal(gT["EVAL"], EVAL): sys.exit("[26_10] STOP: the test events changed in the refit run")
        truncated(gT, "B", h, check_S=True)
    if "72" not in skipped:
        dmax = max(abs(r[f"A72h_{m}_t{t}"] - r[f"B72h_{m}_t{t}"]) for r in out for m in ("M6r", "C3") for t in TAUS
                   if np.isfinite(r[f"A72h_{m}_t{t}"]))
        if dmax > 1e-4: sys.exit(f"[26_10] STOP: B at 72 h differs from A at 72 h by {dmax:.2e} km")
        print(f"[26_10] consistency gate PASS: B(72 h) = A(72 h) (max |diff| {dmax:.1e} km)")

# ---- step 4: summary -----------------------------------------------------------------------------
def summ(prefix, t):
    c3 = np.array([r.get(f"{prefix}_C3_t{t}", np.nan) for r in out], float)
    m6 = np.array([r.get(f"{prefix}_M6r_t{t}", np.nan) for r in out], float)
    ok = np.isfinite(c3) & np.isfinite(m6); d = c3[ok] - m6[ok]
    rec = dict(n_scored=int(ok.sum()), median_C3_km=float(np.median(c3[ok])) if ok.any() else None,
               median_M6r_km=float(np.median(m6[ok])) if ok.any() else None,
               median_diff_C3_minus_M6r_km=float(np.median(d)) if ok.any() else None,
               frac_better=float(np.mean(d < 0)) if ok.any() else None, frac_tied=float(np.mean(d == 0)) if ok.any() else None,
               frac_worse=float(np.mean(d > 0)) if ok.any() else None)
    if prefix != "all":
        nl = np.array([r[f"{prefix}_nlib"] for r in out], float); fb = np.array([r.get(f"{prefix}_fb_t{t}", np.nan) for r in out], float)
        rec.update(median_n_past_events=float(np.median(nl)), frac_C3_fallback=float(np.nanmean(fb)) if np.isfinite(fb).any() else None)
    else:
        rec.update(median_n_past_events=float(np.median([r["n_lib_all"] for r in out])))
    return rec


SUMMARY = {"all": {t: summ("all", t) for t in TAUS}}
for tag in (["A"] if A.no_refit else ["A", "B"]):
    for h in HOURS:
        if tag == "B" and f"{h:g}" in skipped: continue
        SUMMARY[f"{tag}{h:g}h"] = {t: summ(f"{tag}{h:g}h", t) for t in TAUS}
SUMMARY["all"]["n_calibration_events"] = int(len(CAL0))
for h in HOURS:
    for tag in ("A", "B"):
        if f"{tag}{h:g}h" in SUMMARY: SUMMARY[f"{tag}{h:g}h"]["n_calibration_events"] = (len(CAL0) if tag == "A" else n_cal[h])

res = dict(script="26_10_memory_truncation.py", version="v1", sequence=A.seq, frozen_script=SP.name,
           frozen_script_sha256=J["script_sha256"], cache=J["cache"], n_events=len(EVAL), hours=HOURS, min_cal=A.min_cal,
           mainshock_utc=g0["OT"][IM], max_abs_diff_vs_frozen_km=maxdiff, skipped_refit=skipped, summary=SUMMARY,
           limits=["descriptive, not registered; the registered verdicts are unchanged",
                   "the scored events are the frozen late test events (> mainshock + 72 h); only the memory (and, in B, the calibration) is cut",
                   "waveform overlap and catalog incompleteness of the first hours after the mainshock are not reproduced",
                   "variant A keeps the physics fitted on the 72-h pool, which an early system would not have",
                   "the 1-h buffer before each target is kept; M6r_T and C3_T use the same cut list, so their comparison is paired"])
OUT = BASE / "data"; OUT.mkdir(exist_ok=True)
TAG = A.seq + ("_dev" if A.dev else "")
json.dump(res, open(OUT / f"26_10_memory_truncation_{TAG}.json", "w"), indent=1, default=float)
keys = []
for r in out:
    for k in r:
        if k not in keys: keys.append(k)
with open(OUT / f"26_10_memory_truncation_{TAG}.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(out)

print(f"\n[26_10] {A.seq}: {len(EVAL)} events, calibration events {len(CAL0)} (72-h pool)")
print(f"{'set':>8s} {'tau':>4s} {'n':>4s} {'n_past':>7s} {'n_cal':>6s} {'C3':>6s} {'M6r':>6s} {'med d':>7s} {'better':>6s} {'tied':>5s} {'worse':>6s} {'fb':>5s}")
for key, v in SUMMARY.items():
    for t in TAUS:
        s = v[t]
        if s["n_scored"] == 0: print(f"{key:>8s} {t:>4s}    0  (no event scored)"); continue
        fb = s.get("frac_C3_fallback"); fbs = f"{fb:5.2f}" if fb is not None else "    —"
        print(f"{key:>8s} {t:>4s} {s['n_scored']:4d} {s['median_n_past_events']:7.0f} {v['n_calibration_events']:6d} "
              f"{s['median_C3_km']:6.2f} {s['median_M6r_km']:6.2f} {s['median_diff_C3_minus_M6r_km']:+7.2f} "
              f"{s['frac_better']:6.2f} {s['frac_tied']:5.2f} {s['frac_worse']:6.2f} {fbs}")
print(f"[26_10] wrote data/26_10_memory_truncation_{TAG}.json and .csv  ({time.time() - t0:.0f} s)")
