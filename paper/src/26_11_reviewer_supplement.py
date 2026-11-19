#!/usr/bin/env python3
# =============================================================================
# Script : 26_11_reviewer_supplement.py  (v1; run on the author's Mac in ~/SWIFT)
# Project: ARGUS (SRL resubmission) — three descriptive checks for the supplement.
#          None of them is a registered test; the registered verdicts are unchanged.
#
# Part 1  Independent reference (Central Tottori 2016, November 2016 only)
#   Reads the frozen per-event outputs of 23_02 (memory = JMA) and 23_03 (memory moved
#   to the DPRI frame: "jma_shift" and "dpri"). For tau in {0.5, 2} s and each memory
#   frame, it compares C3 and C4 with M6r event by event, scored against the JMA
#   catalog and against the DPRI catalog: n, median paired difference, fractions
#   better / tied / worse, and the one-sided Wilcoxon signed-rank p value
#   (zero_method="wilcox", the same test as the registered hypotheses; nominal,
#   descriptive). Gate: the memory = JMA rows of 23_02 and 23_03 must be identical.
#   Note carried into the output: 23_03 estimated the JMA-to-DPRI offset from all
#   matched events, including the scored test events (optimistic).
#
# Part 2  Effect on the predicted JMA intensity, with C3 (extends 21_10)
#   21_10 used BEST and C4 of Central Tottori 2016 only. This part applies the same
#   formulas (copied unchanged from 21_10 v2: Si & Midorikawa 1999 PGV, equivalent
#   hypocentral distance as the main model, the fault-distance form at Mw 6 and 7 as
#   sensitivity, I = 2.54 + 1.82 log10 PGV, 72 azimuths, sites at 3-80 km) to BEST,
#   C3 and C4 of all three test sequences at tau = 0.5 and 2 s. BEST is chosen by
#   the rule of 26_04 (lowest median among the nine similarity-free methods).
#   Gate: for Central Tottori 2016 the BEST and C4 rows must reproduce
#   models/21_10_gmpe_location_error.json (|diff| <= 1e-9), else STOP.
#
# Part 3  Figure for the memory-truncation check (26_10)
#   Reads data/26_10_memory_truncation_{ct2016,osaka,shimane}.json and draws, for
#   variant B (memory and calibration cut to mainshock + T h), the median error of
#   C3_T and M6r_T against T, with variant A as thin dashed lines and the full-memory
#   values as markers at the right; a bottom row shows the fraction of events where
#   C3_T is better minus the fraction where it is worse.
#
# Inputs (read only)
#   data/23_02_per_event.csv, data/23_03_per_event.csv
#   data/{21_04,21_20,25_05}_per_event.csv, models/{21_04,21_20,25_05}_judgment.json
#   models/21_10_gmpe_location_error.json
#   data/26_10_memory_truncation_{ct2016,osaka,shimane}.json
# Outputs (new files only)
#   data/26_11_reviewer_supplement.json
#   PDF/26_11_FigS_memory_truncation.pdf (and .png)
# Usage
#   cd ~/SWIFT && uv run python src/26_11_reviewer_supplement.py
# =============================================================================
import argparse, csv, hashlib, json, sys, time
from pathlib import Path
import numpy as np
from scipy.stats import wilcoxon

ap = argparse.ArgumentParser()
ap.add_argument("--base", default=".", help="~/SWIFT (holds data/, models/, PDF/)")
A = ap.parse_args()
R = Path(A.base).resolve()
for d in ("data", "PDF"): (R / d).mkdir(exist_ok=True)
TAUS = ["0.5", "2"]


def stop(m):
    print(f"\n[26_11] STOP: {m}"); sys.exit(1)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def need(p):
    p = R / p
    if not p.exists(): stop(f"missing {p}")
    return p


OUT = dict(script="26_11_reviewer_supplement.py", version="v1", script_sha256=sha(__file__),
           utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), inputs={})


def paired(a, b):
    """a - b per event; negative = a better. Nominal one-sided Wilcoxon (a < b)."""
    ok = np.isfinite(a) & np.isfinite(b); d = a[ok] - b[ok]
    rec = dict(n=int(ok.sum()))
    if rec["n"] == 0: return rec
    rec.update(median_a_km=float(np.median(a[ok])), median_b_km=float(np.median(b[ok])), median_diff_km=float(np.median(d)),
               frac_better=float(np.mean(d < 0)), frac_tied=float(np.mean(d == 0)), frac_worse=float(np.mean(d > 0)),
               n_nonzero=int(np.sum(d != 0)))
    rec["p_one_sided"] = (float(wilcoxon(d, zero_method="wilcox", alternative="less").pvalue) if rec["n_nonzero"] >= 1 else None)
    return rec


# ================================================================ Part 1
print("\n" + "#" * 78 + "\n# PART 1  independent DPRI reference, Central Tottori 2016 (descriptive)\n" + "#" * 78)
P2, P3 = need("data/23_02_per_event.csv"), need("data/23_03_per_event.csv")
OUT["inputs"].update({P2.name: sha(P2), P3.name: sha(P3)})


def load_long(p):
    rows = list(csv.DictReader(open(p)))
    for k in ("origin_time", "memory", "tau", "method", "err_vs_jma_km", "err_vs_dpri_km"):
        if rows and k not in rows[0]: stop(f"column {k} missing in {p.name}")
    T = {}
    for r in rows:
        f = lambda v: float(v) if v not in ("", None) else np.nan
        T[(r["memory"], f"{float(r['tau']):g}", r["method"], r["origin_time"])] = (f(r["err_vs_jma_km"]), f(r["err_vs_dpri_km"]))
    return T


L2, L3 = load_long(P2), load_long(P3)
mem2 = sorted({k[0] for k in L2}); mem3 = sorted({k[0] for k in L3})
print(f"[26_11] memory frames: 23_02 {mem2}, 23_03 {mem3}")
k2 = {k: v for k, v in L2.items() if k[0] == "jma"}; k3 = {k: v for k, v in L3.items() if k[0] == "jma"}
if set(k2) != set(k3): stop("memory = jma rows differ in their keys between 23_02 and 23_03")
dmax = max(np.nanmax(np.abs(np.array(k2[k]) - np.array(k3[k]))) if np.isfinite(np.array(k2[k])).any() else 0.0 for k in k2)
if dmax > 1e-9: stop(f"memory = jma errors differ between 23_02 and 23_03 by {dmax:.2e} km")
print(f"[26_11] gate PASS: memory = jma rows of 23_02 and 23_03 are identical ({len(k2)} rows)")
P1 = {}
frames = [("jma", L2), ("jma_shift", L3), ("dpri", L3)]
print(f"{'memory':>9s} {'tau':>4s} {'pair':>9s} {'truth':>5s} {'n':>4s} {'med a':>6s} {'med b':>6s} {'med d':>7s} {'better':>6s} {'tied':>5s} {'worse':>6s} {'p(one-sided)':>12s}")
for mem, L in frames:
    if mem not in {k[0] for k in L}: print(f"[26_11] note: memory frame {mem} not present; skipped"); continue
    for t in TAUS:
        evs = sorted({k[3] for k in L if k[0] == mem and k[1] == t})
        for a, b in (("C3", "M6r"), ("C4", "M6r")):
            for ti, truth in enumerate(("jma", "dpri")):
                va = np.array([L.get((mem, t, a, e), (np.nan, np.nan))[ti] for e in evs], float)
                vb = np.array([L.get((mem, t, b, e), (np.nan, np.nan))[ti] for e in evs], float)
                rec = paired(va, vb); P1[f"{mem}|{t}|{a}-{b}|vs_{truth}"] = rec
                if rec["n"] == 0: continue
                ps = f"{rec['p_one_sided']:.2g}" if rec["p_one_sided"] is not None else "—"
                print(f"{mem:>9s} {t:>4s} {a + '-' + b:>9s} {truth:>5s} {rec['n']:4d} {rec['median_a_km']:6.2f} {rec['median_b_km']:6.2f} "
                      f"{rec['median_diff_km']:+7.2f} {rec['frac_better']:6.2f} {rec['frac_tied']:5.2f} {rec['frac_worse']:6.2f} {ps:>12s}")
OUT["part1_dpri"] = dict(results=P1, notes=[
    "descriptive, not registered; Central Tottori 2016 test events matched to the DPRI catalogue (November 2016 only)",
    "memory = jma: as in the registered test; memory = jma_shift / dpri come from 23_03, whose JMA-to-DPRI offset was estimated "
    "from all matched events including the scored test events (optimistic)",
    "velocity, static station terms, KDE bandwidth and grid were fitted at JMA locations in every frame",
    "p values are nominal: events share past events and paths"])

# ================================================================ Part 2
print("\n" + "#" * 78 + "\n# PART 2  effect on the predicted JMA intensity with C3 (formulas of 21_10 v2)\n" + "#" * 78)
# ---- copied unchanged from 21_10_gmpe_location_error.py v2 ----
DIST = [3.0, 5.0, 10.0, 20.0, 40.0, 80.0]; AZ = np.radians(np.arange(0, 360, 5))
SLOPE, CLASS_W, SIGMA_LOG = 1.82, 0.5, 0.23
MODELS = {"EHD (main)": None, "fault-distance form, Mw 6": 6.0, "fault-distance form, Mw 7": 7.0}


def gdist(Rr, mw):
    return (-np.log10(Rr) - 0.002 * Rr) if mw is None else (-np.log10(Rr + 0.0028 * 10 ** (0.5 * mw)) - 0.002 * Rr)


def dI(err, h, delta, mw):
    e = err[:, None]; dp = np.sqrt(np.maximum(delta ** 2 + e ** 2 - 2 * delta * e * np.cos(AZ)[None, :], 0.0))
    Rr = np.sqrt(delta ** 2 + h[:, None] ** 2); Rp = np.sqrt(dp ** 2 + h[:, None] ** 2)
    return SLOPE * (gdist(Rp, mw) - gdist(Rr, mw))
# ---- end of the copied block ----


def rows_for(e, h):
    out = []
    for mname, mw in MODELS.items():
        for dl in DIST:
            X = np.abs(dI(e, h, dl, mw)); amax = X.max(1)
            out.append(dict(model=mname, site_epi_km=dl, median_azmean_absdI=float(np.median(X.mean(1))),
                            median_azmax_absdI=float(np.median(amax)), max_azmax_absdI=float(amax.max()),
                            class_change_prob_upper=float(np.mean(np.minimum(X / CLASS_W, 1.0)))))
    return out


BASE9 = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]   # same list as 26_04


def best_of(S, t):  # identical to 26_04
    full = [m for m in BASE9 if S[m][t]["available"] == 1.0 and S[m][t]["median_km"] is not None]
    return min(full, key=lambda m: S[m][t]["median_km"])


SEQ = [("Central Tottori 2016", "21_04"), ("Northern Osaka 2018", "21_20"), ("Western Shimane 2018", "25_05")]
P2R = {}
for lab, k in SEQ:
    pc, pj = need(f"data/{k}_per_event.csv"), need(f"models/{k}_judgment.json")
    OUT["inputs"].update({pc.name: sha(pc), pj.name: sha(pj)})
    J = json.load(open(pj)); rows = list(csv.DictReader(open(pc)))
    col = lambda c: np.array([float(r[c]) if r[c] not in ("", None) else np.nan for r in rows])
    P2R[lab] = {}
    for t in TAUS:
        b = best_of(J["summary"], t)
        eb, e3, e4, h = col(f"{b}_err_t{t}"), col(f"C3_err_t{t}"), col(f"C4_err_t{t}"), col("depth_km")
        m = np.isfinite(eb) & np.isfinite(e3) & np.isfinite(e4) & np.isfinite(h)
        for meth, e in (("BEST", eb), ("C3", e3), ("C4", e4)):
            P2R[lab][f"tau{t}_{meth}"] = dict(method=(b if meth == "BEST" else meth), n_events=int(m.sum()),
                                              error_median_km=float(np.median(e[m])), rows=rows_for(e[m], h[m]))
# gate: reproduce 21_10 for Central Tottori 2016 (BEST and C4)
pg = need("models/21_10_gmpe_location_error.json"); OUT["inputs"][pg.name] = sha(pg)
G = json.load(open(pg))["results"]["dense (full Hi-net, 21_04)"]
gmax = 0.0
for t in TAUS:
    for meth in ("BEST", "C4"):
        old, new = G[f"tau{t}_{meth}"], P2R["Central Tottori 2016"][f"tau{t}_{meth}"]
        if old["method"] != new["method"]: stop(f"21_10 used {old['method']} as {meth} at tau {t}; this script uses {new['method']}")
        if old["n_rows"] != new["n_events"]: stop(f"21_10 used {old['n_rows']} events at tau {t} {meth}; this script {new['n_events']}")
        for ro, rn in zip(old["rows"], new["rows"]):
            for kk in ("median_azmean_absdI", "median_azmax_absdI", "max_azmax_absdI", "class_change_prob_upper"):
                gmax = max(gmax, abs(ro[kk] - rn[kk]))
if gmax > 1e-9: stop(f"Central Tottori 2016 BEST/C4 do not reproduce 21_10 (max |diff| {gmax:.2e})")
print(f"[26_11] gate PASS: Central Tottori 2016 BEST and C4 reproduce 21_10 (max |diff| {gmax:.1e})")
print("main model (equivalent hypocentral distance), site at 10 km: median over events of the azimuth-mean |dI| / "
      "upper bound of the class-change probability")
for lab in P2R:
    for t in TAUS:
        line = []
        for meth in ("BEST", "C3", "C4"):
            o = P2R[lab][f"tau{t}_{meth}"]; r10 = [r for r in o["rows"] if r["model"] == "EHD (main)" and r["site_epi_km"] == 10.0][0]
            line.append(f"{meth}({o['method']}) err {o['error_median_km']:.2f} km: {r10['median_azmean_absdI']:.3f} / {r10['class_change_prob_upper']:.3f}")
        print(f"  {lab:21s} tau {t:>3s} s  n={P2R[lab][f'tau{t}_BEST']['n_events']:3d} | " + " | ".join(line))
OUT["part2_intensity"] = dict(results=P2R, site_epi_km=DIST, slope=SLOPE, class_width=CLASS_W, gmpe_sigma_log10=SIGMA_LOG,
                              conversion="I = 2.54 + 1.82 log10 PGV", source="formulas copied unchanged from 21_10_gmpe_location_error.py v2",
                              limits=["point source; finite-fault distances not included", "depth and magnitude errors not included",
                                      "errors of 1.5 <= Mj < 2.0 events", "one PGV-to-intensity conversion; no site terms",
                                      "class-change probability is an upper bound with the narrowest class width 0.5"])

# ================================================================ Part 3
print("\n" + "#" * 78 + "\n# PART 3  figure of the memory-truncation check (26_10)\n" + "#" * 78)
S10 = {}
for lab, s in (("Central Tottori 2016", "ct2016"), ("Northern Osaka 2018", "osaka"), ("Western Shimane 2018", "shimane")):
    p = need(f"data/26_10_memory_truncation_{s}.json"); OUT["inputs"][p.name] = sha(p); S10[lab] = json.load(open(p))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
plt.rcParams.update({"font.size": 10, "axes.facecolor": "white", "figure.facecolor": "white", "savefig.facecolor": "white"})
C_C3, C_M6 = "#0072B2", "#E69F00"     # Okabe-Ito
fig, axs = plt.subplots(3, 3, figsize=(12, 10), sharex=True)
for j, (lab, Jt) in enumerate(S10.items()):
    H = Jt["hours"]; SM = Jt["summary"]
    def ser(tag, t, key):
        return [SM[f"{tag}{h:g}h"][t][key] if f"{tag}{h:g}h" in SM else np.nan for h in H]
    for i, t in enumerate(TAUS):
        ax = axs[i, j]
        for tag, ls, lw, al in (("B", "-", 1.8, 1.0), ("A", "--", 1.0, 0.7)):
            ax.plot(H, ser(tag, t, "median_C3_km"), ls, color=C_C3, lw=lw, alpha=al, marker="o" if tag == "B" else None, ms=4)
            ax.plot(H, ser(tag, t, "median_M6r_km"), ls, color=C_M6, lw=lw, alpha=al, marker="s" if tag == "B" else None, ms=4)
        xa = H[-1] * 1.6
        ax.plot([xa], [SM["all"][t]["median_C3_km"]], marker="*", color=C_C3, ms=10, ls="none", clip_on=False)
        ax.plot([xa], [SM["all"][t]["median_M6r_km"]], marker="*", color=C_M6, ms=10, ls="none", clip_on=False)
        ax.set_xscale("log"); ax.grid(alpha=0.3); ax.set_ylim(bottom=0)
        if j == 0: ax.set_ylabel(f"Median epicentral error (km)\nτ = {t} s")
        if i == 0: ax.set_title(f"{lab}\n(n = {Jt['n_events']} test events)", fontsize=10)
    ax = axs[2, j]
    for t, ls, cc in (("0.5", "-", "0.15"), ("2", ":", "0.55")):
        net = [SM[f"B{h:g}h"][t]["frac_better"] - SM[f"B{h:g}h"][t]["frac_worse"] if f"B{h:g}h" in SM else np.nan for h in H]
        ax.plot(H, net, ls, color=cc, marker="o", ms=4, lw=1.6)
    ax.axhline(0, color="0.5", lw=0.8); ax.set_xscale("log"); ax.grid(alpha=0.3); ax.set_ylim(-1, 1)
    ax.set_xticks(H); ax.set_xticklabels([f"{h:g}" for h in H])
    ax.set_xlabel("Memory and calibration up to mainshock + T (hr)")
    if j == 0: ax.set_ylabel("Fraction C3 better\nminus fraction worse (B)")
hs = [Line2D([], [], color=C_C3, marker="o", lw=1.8, label="C3, variant B (memory and calibration cut at T)"),
      Line2D([], [], color=C_M6, marker="s", lw=1.8, label="M6r, variant B"),
      Line2D([], [], color="0.4", ls="--", lw=1.0, label="Variant A (memory cut at T, calibration on the 72-hr pool)"),
      Line2D([], [], color="0.4", marker="*", ls="none", ms=10, label="Full memory, as in the registered test"),
      Line2D([], [], color="0.15", ls="-", marker="o", label="τ = 0.5 s (bottom row)"),
      Line2D([], [], color="0.55", ls=":", marker="o", label="τ = 2 s (bottom row)")]
from matplotlib.ticker import NullLocator
for a_ in axs.ravel(): a_.xaxis.set_minor_locator(NullLocator())
fig.legend(handles=hs, loc="lower center", ncol=2, frameon=False, fontsize=9, bbox_to_anchor=(0.5, 0.0))
fig.suptitle("Memory truncation: the same late test events located with knowledge of the first T hours only (descriptive)", fontsize=11)
fig.tight_layout(rect=(0, 0.1, 1, 0.97))
fig.savefig(R / "PDF/26_11_FigS_memory_truncation.pdf"); fig.savefig(R / "PDF/26_11_FigS_memory_truncation.png", dpi=200); plt.close(fig)
OUT["part3_figure"] = dict(pdf="PDF/26_11_FigS_memory_truncation.pdf", source="26_10 summaries, variant B solid, variant A dashed")
json.dump(OUT, open(R / "data/26_11_reviewer_supplement.json", "w"), indent=1)
print("[26_11] wrote PDF/26_11_FigS_memory_truncation.pdf (.png) and data/26_11_reviewer_supplement.json\nDONE")
