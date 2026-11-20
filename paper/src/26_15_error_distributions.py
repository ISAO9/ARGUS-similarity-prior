#!/usr/bin/env python3
# =============================================================================
# Script : 26_15_error_distributions.py  (v1.3, 2026-11-20: v1.3 figure layout; v1.2 relative input paths)
# Project: ARGUS (SRL new submission) — full error distributions and tail statistics
#
# What this script does
#   Reads ONLY the frozen outputs of the registered runs (judgment JSON and
#   per-event CSV files; nothing is recomputed from waveforms) and reports the
#   whole distribution of the epicentral errors, not only the medians:
#     1. Figure S2: empirical cumulative distribution of the epicentral error of
#        BEST, M6r, C3, and C4 at tau = 0.5 s (top row) and tau = 2 s (bottom
#        row), one column per test sequence (Central Tottori 2016, Northern Osaka
#        2018, Western Shimane 2018). Log-scaled error axis; the 0.5-km floor is
#        marked. BEST(tau) is chosen by the registered rule (smallest median among
#        the nine similarity-free reference methods that give an estimate for
#        every evaluated event) and must equal the frozen judgment (STOP if not).
#     2. Table S9 values: for each sequence, tau, and method, the number of events,
#        the median, the 90th percentile, and the fractions of events with errors
#        above 1, 5, and 10 km; and, for C3 against BEST, the number of events
#        where C3 is worse by more than 1 km and by more than 5 km.
#     3. The share of evaluated events with only one station with a P pick at
#        tau = 0.5 s (column n_sta_t0.5), quoted in the Discussion: for these
#        events equation (2) has no misfit and the estimate rests on the prior.
#   This analysis is descriptive and was not registered.
#
# Rules followed (SRL / author): no title inside the figure, white background,
#   English labels, legend outside the axes, panel labels outside the upper left,
#   Okabe-Ito colors with distinct line styles (readable in gray), sans-serif
#   font 7-9 pt, the same colors and styles as Figs. 5-9 (26_02).
#
# Inputs : {21_04,21_20,25_05}_judgment.json and {21_04,21_20,25_05}_per_event.csv,
#          searched first in data/inputs/models and data/inputs/data (public copy),
#          then in models/ and data/ of the project folder (~/SWIFT, where the
#          registered runs wrote them). The SHA-256 of each file used is reported.
# Outputs: PDF/26_15_FigS2_error_cdf.pdf (+ .png at 300 dpi for checking)
#          data/26_15_tail_stats.json, data/26_15_tail_stats.csv,
#          data/26_15_table_S9.md (markdown table for the supplement)
# Usage  : cd ~/SWIFT && uv run python src/26_15_error_distributions.py
#          (run from the project folder that holds data/inputs, as for 26_02)
# =============================================================================
import json, sys, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
INP = ROOT / "data" / "inputs"
PDFD = ROOT / "PDF"; PDFD.mkdir(exist_ok=True)
OUTD = ROOT / "data"

SEQUENCES = [
    dict(key="ct2016", label="Central Tottori 2016", judg="models/21_04_judgment.json", pev="data/21_04_per_event.csv"),
    dict(key="osaka", label="Northern Osaka 2018", judg="models/21_20_judgment.json", pev="data/21_20_per_event.csv"),
    dict(key="shimane", label="Western Shimane 2018", judg="models/25_05_judgment.json", pev="data/25_05_per_event.csv"),
]
BASE = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]   # similarity-free reference methods
TAUS = ["0.5", "2"]
METHODS = ["BEST", "M6r", "C3", "C4"]
FLOOR_KM = 0.5
THR = (1.0, 5.0, 10.0)
STY = {"BEST": dict(c="#000000", ls="-"), "M6r": dict(c="#999999", ls=":"),
       "C3": dict(c="#0072B2", ls="-"), "C4": dict(c="#009E73", ls="--")}
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "Liberation Sans", "DejaVu Sans"],
                     "font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
                     "axes.linewidth": 0.6, "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
                     "pdf.fonttype": 42, "ps.fonttype": 42})


def stop(msg):
    print(f"[26_15] STOP: {msg}"); sys.exit(1)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def best_of(summary, t):
    """BEST(tau) by the registered rule: smallest median among the 9 reference methods with available == 1"""
    full = [m for m in BASE if m in summary and summary[m][t]["available"] == 1.0 and summary[m][t]["median_km"] is not None]
    return min(full, key=lambda m: summary[m][t]["median_km"])


# ------------------------------------------------------------------ load and check against the frozen judgments
LOADED, INPUT_SHA = [], {}
for s in SEQUENCES:
    pj = next((p for p in (INP / s["judg"], ROOT / s["judg"]) if p.exists()), None)
    pe = next((p for p in (INP / s["pev"], ROOT / s["pev"]) if p.exists()), None)
    if pj is None or pe is None:
        stop(f"missing input for {s['label']}: {s['judg']} or {s['pev']} under {INP} or {ROOT}")
    print(f"[26_15] inputs: {pj.relative_to(ROOT)}  {pe.relative_to(ROOT)}")
    J = json.load(open(pj)); E = pd.read_csv(pe)
    INPUT_SHA[str(pj.relative_to(ROOT))], INPUT_SHA[str(pe.relative_to(ROOT))] = sha(pj), sha(pe)
    H = J.get("hypotheses", {})
    best = {}
    for t in TAUS:
        b = best_of(J["summary"], t); best[t] = b
        hk = {"2": "H1", "0.5": "H3"}[t]
        if hk in H and H[hk].get("best") and H[hk]["best"] != b:
            stop(f"{s['label']}: BEST at tau {t} {b} != frozen {H[hk]['best']}")
        med = float(np.nanmedian(E[f"{b}_err_t{t}"].to_numpy(float)))
        if hk in H and H[hk].get("best_median_km") is not None and abs(med - H[hk]["best_median_km"]) > 6e-5:
            stop(f"{s['label']}: median of {b} at tau {t} = {med} != frozen {H[hk]['best_median_km']}")
        for m in ("C3", "C4", "M6r"):
            if f"{m}_err_t{t}" not in E.columns: stop(f"{s['label']}: column {m}_err_t{t} missing")
    LOADED.append(dict(s, J=J, E=E, best=best))
    print(f"[26_15] {s['label']}: {len(E)} evaluated events, BEST = {best}")


def errs(s, m, t):
    col = s["best"][t] if m == "BEST" else m
    x = s["E"][f"{col}_err_t{t}"].to_numpy(float)
    if np.isnan(x).any(): stop(f"{s['label']}: {col} at tau {t} has {int(np.isnan(x).sum())} missing errors")
    return x


# ------------------------------------------------------------------ statistics
rows = []
for s in LOADED:
    for t in TAUS:
        for m in METHODS:
            x = errs(s, m, t)
            r = dict(sequence=s["label"], tau_s=float(t), method=m, method_used=(s["best"][t] if m == "BEST" else m),
                     n=int(len(x)), median_km=round(float(np.median(x)), 4), p90_km=round(float(np.percentile(x, 90)), 4))
            for th in THR: r[f"frac_gt_{th:g}km"] = round(float(np.mean(x > th)), 4)
            rows.append(r)
        d = errs(s, "C3", t) - errs(s, "BEST", t)
        rows.append(dict(sequence=s["label"], tau_s=float(t), method="C3-BEST", method_used=f"C3-{s['best'][t]}", n=int(len(d)),
                         worse_by_gt_1km=int(np.sum(d > 1.0)), worse_by_gt_5km=int(np.sum(d > 5.0)),
                         better_by_gt_1km=int(np.sum(d < -1.0)), better_by_gt_5km=int(np.sum(d < -5.0))))
ONE = {s["label"]: dict(n=int(len(s["E"])), n_one_station=int((s["E"]["n_sta_t0.5"] == 1).sum()),
                        share_one_station_pct=round(100.0 * float((s["E"]["n_sta_t0.5"] == 1).mean()), 1),
                        median_n_sta=float(s["E"]["n_sta_t0.5"].median())) for s in LOADED}
T = pd.DataFrame(rows)
T.to_csv(OUTD / "26_15_tail_stats.csv", index=False)
json.dump(dict(script="26_15_error_distributions.py v1.3", descriptive=True, input_sha256=INPUT_SHA, rows=rows,
               one_station_at_tau_0p5=ONE),
          open(OUTD / "26_15_tail_stats.json", "w"), indent=1, ensure_ascii=False)

# markdown table for the supplement (Table S9)
md = ["| Sequence | τ (s) | Method | n | Median (km) | P90 (km) | > 1 km (%) | > 5 km (%) | > 10 km (%) |",
      "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    if r["method"] == "C3-BEST": continue
    name = f"BEST ({r['method_used']})" if r["method"] == "BEST" else r["method"]
    md.append(f"| {r['sequence']} | {r['tau_s']:g} | {name} | {r['n']} | {r['median_km']:.2f} | {r['p90_km']:.2f} | "
              f"{100 * r['frac_gt_1km']:.0f} | {100 * r['frac_gt_5km']:.0f} | {100 * r['frac_gt_10km']:.0f} |")
md.append("")
md.append("| Sequence | τ (s) | Comparison | n | C3 worse by > 1 km | C3 worse by > 5 km | C3 better by > 1 km | C3 better by > 5 km |")
md.append("|---|---|---|---|---|---|---|---|")
for r in rows:
    if r["method"] != "C3-BEST": continue
    md.append(f"| {r['sequence']} | {r['tau_s']:g} | {r['method_used']} | {r['n']} | {r['worse_by_gt_1km']} | {r['worse_by_gt_5km']} | "
              f"{r['better_by_gt_1km']} | {r['better_by_gt_5km']} |")
(OUTD / "26_15_table_S9.md").write_text("\n".join(md) + "\n")

# ------------------------------------------------------------------ Figure S2
# layout: sequence name above each column, n and BEST inside the empty lower-right corner,
# the 0.5-km floor as a long-dashed line (distinct from the dotted M6r), plain tick labels,
# one shared legend in the bottom margin, outside every panel
from matplotlib.ticker import FixedLocator, FixedFormatter, NullFormatter
TICKS = [0.01, 0.1, 1, 10, 100]
fig, axs = plt.subplots(2, 3, figsize=(7.0, 5.0), sharex=True, sharey=True)
for j, s in enumerate(LOADED):
    for i, t in enumerate(TAUS):
        ax = axs[i, j]
        ax.axvline(FLOOR_KM, color="0.55", lw=0.7, ls=(0, (6, 3)), zorder=1)
        for m in METHODS:
            x = np.sort(np.clip(errs(s, m, t), 0.01, None))
            y = np.arange(1, len(x) + 1) / len(x)
            ax.step(x, y, where="post", color=STY[m]["c"], ls=STY[m]["ls"], lw=1.1, label=m, zorder=2)
        ax.set_xscale("log"); ax.set_xlim(0.01, 100); ax.set_ylim(0, 1.0)
        ax.xaxis.set_major_locator(FixedLocator(TICKS))
        ax.xaxis.set_major_formatter(FixedFormatter(["0.01", "0.1", "1", "10", "100"]))
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.grid(True, which="major", lw=0.3, color="0.85")
        if i == 0: ax.set_title(s["label"], fontsize=8, pad=4)
        if i == 1: ax.set_xlabel("Epicentral error (km)")
        if j == 0: ax.set_ylabel(f"Fraction of events\n(τ = {t} s)")
        ax.text(0.97, 0.04, f"n = {len(s['E'])}\nBEST = {s['best'][t]}", transform=ax.transAxes,
                ha="right", va="bottom", fontsize=7)
        ax.text(-0.16 if j == 0 else -0.08, 1.02, f"({'abcdef'[i * 3 + j]})", transform=ax.transAxes,
                ha="left", va="bottom", fontsize=9, fontweight="bold")
h, l = axs[0, 0].get_legend_handles_labels()
h.append(plt.Line2D([], [], color="0.55", lw=0.7, ls=(0, (6, 3)))); l.append("0.5-km floor")
fig.legend(h, l, loc="lower center", ncol=5, frameon=False, fontsize=7, handlelength=2.6, bbox_to_anchor=(0.55, 0.0))
fig.subplots_adjust(left=0.11, right=0.98, top=0.93, bottom=0.16, wspace=0.16, hspace=0.22)
for ext in ("pdf", "png"):
    fig.savefig(PDFD / f"26_15_FigS2_error_cdf.{ext}", dpi=300)
plt.close(fig)

# ------------------------------------------------------------------ report
print("\n" + "\n".join(md))
print("\n[26_15] events with one station picked at tau = 0.5 s:")
for k, v in ONE.items(): print(f"  {k}: {v['n_one_station']}/{v['n']} = {v['share_one_station_pct']}% (median stations {v['median_n_sta']:g})")
print(f"\n[26_15] wrote PDF/26_15_FigS2_error_cdf.pdf, data/26_15_tail_stats.json/.csv, data/26_15_table_S9.md")
