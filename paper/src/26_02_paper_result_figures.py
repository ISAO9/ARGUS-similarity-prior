#!/usr/bin/env python3
# =============================================================================
# Script : 26_02_paper_result_figures.py  (v1)
# Project: ARGUS (SRL resubmission) — paper figures 5–9 from frozen outputs only
#
# What this script does
#   Reads ONLY the frozen outputs of the registered runs (judgment JSON and
#   per-event CSV files; nothing is recomputed from waveforms) and draws the
#   result figures of the manuscript:
#     Fig. 5  Median epicentral error vs elapsed time tau (BEST, M6r, C1, C3, C4)
#             with the frozen bootstrap 95% intervals, one panel per sequence.
#     Fig. 6  Forest plot at tau = 2 s and 0.5 s: Hodges-Lehmann paired shift
#             (C3 - BEST, C4 - BEST, C3 - M6r) with a 95% interval from a bootstrap
#             over whole JST days, read from data/26_04_effect_sizes.json (run 26_04 first)
#             (descriptive; outside the registered tests). Floor cases are shaded.
#     Fig. 7  When memory helps: per-event gain (BEST error - C3 error) at tau = 2 s
#             against the maximum similarity and against the distance to the most
#             similar past event (exploratory).
#     Fig. 8  Per-event C3 error vs BEST error at tau = 2 s (losses highlighted).
#     Fig. 9  Learned ranking (L3, L4) and trust switch (G vs C4 and rule R).
#   Every number drawn is also written to data/26_02_figure_values.json so that
#   the text can quote the same values; the script checks that its BEST and
#   medians equal the frozen judgment JSON (STOP if not).
#
# Rules followed (SRL): no title inside figures, white background, English labels,
#   legend outside the axes, panel labels (a), (b) outside the upper left,
#   Okabe-Ito colors with distinct line styles and markers (readable in gray),
#   sans-serif font (Helvetica/Arial), sizes 7-9 pt at final width.
#
# Inputs : data/inputs/models/*.json and data/inputs/data/*.csv (unzipped from
#          paper_inputs.zip; see SEQUENCES below for the exact file names)
# Outputs: PDF/26_02_Fig5_error_vs_tau.pdf ... PDF/26_02_Fig9_learned_switch.pdf
#          (+ .png at 300 dpi for checking), data/26_02_figure_values.json
# Usage  : uv run python src/26_02_paper_result_figures.py
# =============================================================================
import json, sys, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator, NullFormatter

ROOT = Path(__file__).resolve().parents[1]
INP = ROOT / "data" / "inputs"
PDFD = ROOT / "PDF"; PDFD.mkdir(exist_ok=True)
OUTJ = ROOT / "data" / "26_02_figure_values.json"

# Sequences (test sequences in the order of the paper; development shown in Fig. 5 only)
SEQUENCES = [
    dict(key="ct2016", label="Central Tottori 2016", role="test",
         judg="models/21_04_judgment.json", pev="data/21_04_per_event.csv",
         ljudg="models/21_06b_judgment.json", lpev="data/21_06b_per_event.csv", gjudg=None, gpev=None),
    dict(key="osaka", label="Northern Osaka 2018", role="test",
         judg="models/21_20_judgment.json", pev="data/21_20_per_event.csv",
         ljudg="models/21_20f_judgment.json", lpev="data/21_20f_per_event.csv",
         gjudg="models/22_04_judgment.json", gpev="data/22_04_per_event.csv"),
    dict(key="shimane", label="Western Shimane 2018", role="test",
         judg="models/25_05_judgment.json", pev="data/25_05_per_event.csv",
         ljudg="models/25_06f_judgment.json", lpev="data/25_06f_per_event.csv",
         gjudg="models/25_06g_judgment.json", gpev="data/25_06g_per_event.csv"),
    dict(key="wt2026", label="West Tottori 2026 (development)", role="dev",
         judg="models/21_02_judgment.json", pev="data/21_02_per_event.csv",
         ljudg=None, lpev=None, gjudg=None, gpev=None),
]
BASE = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]   # similarity-free reference methods
TAUS = ["0.5", "1", "2", "3"]
FLOOR_KM, SEED, NBOOT = 0.5, 0, 10000

# Okabe-Ito palette with line styles and markers (distinct in gray scale)
STY = {"BEST": dict(c="#000000", ls="-", m="s"), "M6r": dict(c="#999999", ls=":", m="v"),
       "C1": dict(c="#E69F00", ls="-.", m="^"), "C3": dict(c="#0072B2", ls="-", m="o"),
       "C4": dict(c="#009E73", ls="--", m="D"), "L3": dict(c="#56B4E9", ls="-", m="o"),
       "L4": dict(c="#CC79A7", ls="--", m="D"), "G": dict(c="#D55E00", ls="-", m="P"),
       "R": dict(c="#F0E442", ls="-", m="X")}
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "Liberation Sans", "DejaVu Sans"],
                     "font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
                     "axes.linewidth": 0.6, "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
                     "pdf.fonttype": 42, "ps.fonttype": 42})


def stop(msg):
    print(f"[26_02] STOP: {msg}"); sys.exit(1)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def panel_label(ax, s):
    ax.text(-0.16, 1.03, f"({s})", transform=ax.transAxes, ha="left", va="bottom", fontsize=9, fontweight="bold")


def best_of(summary, t):
    """BEST(tau) by the registered rule: smallest median among the 9 reference methods with available == 1"""
    full = [m for m in BASE if m in summary and summary[m][t]["available"] == 1.0 and summary[m][t]["median_km"] is not None]
    return min(full, key=lambda m: summary[m][t]["median_km"])


def hl_shift(d):
    """Hodges-Lehmann paired shift: median of the Walsh averages (d_i + d_j)/2, i <= j (zeros kept)"""
    d = np.sort(d); i, j = np.triu_indices(len(d))
    return float(np.median((d[i] + d[j]) / 2.0))


def boot_hl_dayblock(d, day, rng, nb=2000):
    """HL shift with a 95% interval from a bootstrap over whole JST days (dependent events stay together)"""
    ok = np.isfinite(d); d, day = d[ok], day[ok]
    groups = [np.where(day == u)[0] for u in np.unique(day)]
    bs = [hl_shift(d[np.concatenate([groups[k] for k in rng.integers(0, len(groups), len(groups))])]) for _ in range(nb)]
    return hl_shift(d), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)), int(len(d))


# ------------------------------------------------------------------ load
LOADED, INPUT_SHA = [], {}
for s in SEQUENCES:
    p = INP / s["judg"]
    if not p.exists():
        print(f"[26_02] missing {p.relative_to(ROOT)} -> {s['label']} skipped"); continue
    J = json.load(open(p)); INPUT_SHA[s["judg"]] = sha(p)
    E = pd.read_csv(INP / s["pev"]); INPUT_SHA[s["pev"]] = sha(INP / s["pev"])
    s = dict(s, J=J, E=E)
    for k in ("ljudg", "lpev", "gjudg", "gpev"):
        if s[k] and (INP / s[k]).exists():
            s[k + "_data"] = json.load(open(INP / s[k])) if s[k].endswith(".json") else pd.read_csv(INP / s[k])
            INPUT_SHA[s[k]] = sha(INP / s[k])
    # consistency with the frozen judgment: BEST and medians at tau = 2 and 0.5
    H = J.get("hypotheses", {})
    for hk, t in (("H1", "2"), ("H3", "0.5")):
        if hk in H and H[hk].get("best"):
            b = best_of(J["summary"], t)
            if b != H[hk]["best"]: stop(f"{s['label']}: BEST at tau {t} {b} != frozen {H[hk]['best']}")
            col = f"{b}_err_t{t}"
            med = float(np.nanmedian(E[col].to_numpy(float)))
            if abs(med - H[hk]["best_median_km"]) > 6e-5:   # per-event CSV errors carry 4 decimals
                stop(f"{s['label']}: median of {col} {med} != frozen {H[hk]['best_median_km']}")
    LOADED.append(s)
if not LOADED: stop("no sequence found under data/inputs")
TEST = [s for s in LOADED if s["role"] == "test"]
VAL = dict(inputs_sha256=INPUT_SHA, seed=SEED, nboot=NBOOT, figures={})
print(f"[26_02] loaded: {', '.join(s['label'] for s in LOADED)}  (BEST and medians match the frozen JSON)")

# ------------------------------------------------------------------ Fig. 5  error vs tau
n = len(LOADED)
fig, axs = plt.subplots(1, n, figsize=(7.0, 2.5), sharey=True, squeeze=False)
xs = [float(t) for t in TAUS]
v5 = {}
for i, s in enumerate(LOADED):
    ax = axs[0, i]; S = s["J"]["summary"]; v5[s["key"]] = {}
    bests = [best_of(S, t) for t in TAUS]
    series = {"BEST": [S[b][t] for b, t in zip(bests, TAUS)]}
    for m in ("M6r", "C1", "C3", "C4"):
        if m in S: series[m] = [S[m][t] for t in TAUS]
    for k, rows in series.items():
        y = np.array([r["median_km"] if r["median_km"] is not None else np.nan for r in rows], float)
        lo = np.array([r.get("ci_lo") if r.get("ci_lo") is not None else np.nan for r in rows], float)
        hi = np.array([r.get("ci_hi") if r.get("ci_hi") is not None else np.nan for r in rows], float)
        st = STY[k]
        ax.errorbar(xs, y, yerr=[y - lo, hi - y], color=st["c"], ls=st["ls"], marker=st["m"], ms=3.5, lw=1.0,
                    capsize=1.5, elinewidth=0.6, label=("BEST (similarity-free)" if k == "BEST" else k), mfc="white" if k == "M6r" else st["c"])
        v5[s["key"]][k] = dict(median_km=y.tolist(), ci_lo=lo.tolist(), ci_hi=hi.tolist())
    v5[s["key"]]["BEST_method"] = bests
    CA = s["J"].get("causal") or {}
    if CA.get("evaluated") and CA.get("summary"):                  # H5: picks available by tau (Shimane only)
        CS = CA["summary"]; cb = [best_of(CS, t) for t in TAUS]
        for k, rows in (("BEST", [CS[b][t] for b, t in zip(cb, TAUS)]), ("C3", [CS["C3"][t] for t in TAUS])):
            y = np.array([r["median_km"] if r["median_km"] is not None else np.nan for r in rows], float)
            ax.plot(xs, y, color=STY[k]["c"], ls=(0, (1, 1)), marker=STY[k]["m"], ms=3.5, lw=0.9, mfc="white",
                    label=("BEST, picks by τ" if k == "BEST" else "C3, picks by τ"))
            v5[s["key"]][k + "_picks_by_tau"] = dict(median_km=y.tolist(), method=(cb if k == "BEST" else "C3"))
    ax.axhline(FLOOR_KM, color="0.5", lw=0.6, ls=(0, (2, 2)))
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.xaxis.set_major_locator(FixedLocator(xs)); ax.xaxis.set_major_formatter(FixedFormatter(TAUS))
    ax.xaxis.set_minor_locator(NullLocator()); ax.xaxis.set_minor_formatter(NullFormatter())
    yt = [0.2, 0.3, 0.5, 1, 2, 3]
    ax.yaxis.set_major_locator(FixedLocator(yt)); ax.yaxis.set_major_formatter(FixedFormatter([str(v) for v in yt]))
    ax.yaxis.set_minor_formatter(NullFormatter()); ax.set_ylim(0.13, 3.3)
    ax.set_xlabel("Elapsed time after first P, τ (s)")
    ax.text(0.97, 0.97, s["label"].replace(" (development)", "\n(development)"), transform=ax.transAxes, ha="right", va="top", fontsize=7)
    panel_label(ax, "abcd"[i])
axs[0, 0].set_ylabel("Median epicentral error (km)")
axs[0, -1].text(1.02, 0.0, "dashed gray:\n0.5 km floor", transform=axs[0, -1].transAxes, fontsize=6.5, va="bottom")
hh, ll = [], []
for a_ in axs[0]:
    for h_, l_ in zip(*a_.get_legend_handles_labels()):
        if l_ not in ll: hh.append(h_); ll.append(l_)
fig.legend(hh, ll, loc="upper center", bbox_to_anchor=(0.5, 1.13), ncol=4, frameon=False)
fig.tight_layout(); fig.subplots_adjust(top=0.80)
for ext in ("pdf", "png"): fig.savefig(PDFD / f"26_02_Fig5_error_vs_tau.{ext}", dpi=300, bbox_inches="tight")
plt.close(fig); VAL["figures"]["Fig5"] = v5

# ------------------------------------------------------------------ Fig. 6  forest plot (descriptive)
ESP = ROOT / "data" / "26_04_effect_sizes.json"
if not ESP.exists(): stop("run src/26_04_paper_effect_sizes.py first (Fig. 6 reads its effect sizes)")
ES = json.load(open(ESP)); INPUT_SHA["data/26_04_effect_sizes.json"] = sha(ESP)
comps = [("C3", "BEST"), ("C4", "BEST"), ("C3", "M6r")]
fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.6), sharey=True)
v6 = {}
for j, t in enumerate(("2", "0.5")):
    ax = axs[j]; ylab, yy = [], 0
    for s in TEST:
        S = s["J"]["summary"]; E = s["E"]; b = best_of(S, t); floor = S[b][t]["median_km"] < FLOOR_KM
        if floor: ax.axhspan(yy - 0.5, yy + len(comps) - 0.5, color="0.92", lw=0)
        for k, (a, r) in enumerate(comps):
            rr = b if r == "BEST" else r
            d = E[f"{a}_err_t{t}"].to_numpy(float) - E[f"{rr}_err_t{t}"].to_numpy(float)
            # single source of the effect sizes: data/26_04_effect_sizes.json (26_04 must be run first)
            rec = [r_ for r_ in ES if r_["sequence"] == s["label"] and r_["tau"] == t and r_["comparison"] == f"{a}-{r}"]
            if len(rec) != 1: stop(f"no 26_04 effect size for {s['label']} tau {t} {a}-{r}")
            rec = rec[0]
            if rec["ref"] != rr: stop(f"26_04 reference {rec['ref']} != {rr} for {s['label']} tau {t}")
            med, lo, hi, nn = rec["hl_shift_km"], rec["ci_lo"], rec["ci_hi"], rec["n"]
            st = STY[a] if r == "BEST" else STY["M6r"]
            ax.errorbar(med, yy, xerr=[[med - lo], [hi - med]], fmt=st["m"], color=st["c"], ms=4, capsize=2, elinewidth=0.8)
            ylab.append(f"{s['label'].split(' 20')[0]}: {a} − {r}" + (f" ({b})" if r == "BEST" else ""))
            v6.setdefault(t, {}).setdefault(s["key"], {})[f"{a}-{r}"] = dict(ref_method=rr, median_km=med, ci_lo=lo, ci_hi=hi, n=nn, floor=bool(floor))
            yy += 1
        yy += 0.6
    ax.axvline(0, color="k", lw=0.6)
    ax.set_xlabel(f"Hodges–Lehmann paired shift at τ = {t} s (km)\n(negative: similarity method better)")
    panel_label(ax, "ab"[j])
    if j == 0:
        ypos, k2 = [], 0
        for s in TEST:
            for _ in comps: ypos.append(k2); k2 += 1
            k2 += 0.6
        ax.set_yticks(ypos); ax.set_yticklabels(ylab)
axs[0].invert_yaxis()
fig.text(0.99, 0.01, "Shaded: BEST below the 0.5-km floor", ha="right", fontsize=6.5)
fig.tight_layout()
for ext in ("pdf", "png"): fig.savefig(PDFD / f"26_02_Fig6_forest.{ext}", dpi=300, bbox_inches="tight")
plt.close(fig); VAL["figures"]["Fig6"] = v6

# ------------------------------------------------------------------ Fig. 7  when memory helps (exploratory)
fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.6), sharey=True)
mk = ["o", "^", "s"]; cols = ["#0072B2", "#E69F00", "#009E73"]
v7 = {}
for i, s in enumerate(TEST):
    S = s["J"]["summary"]; E = s["E"]; b = best_of(S, "2")
    gain = E[f"{b}_err_t2"].to_numpy(float) - E["C3_err_t2"].to_numpy(float)
    sm = E["smax_t2"].to_numpy(float); sep = E["best_template_sep_km_t2"].to_numpy(float)
    ok = np.isfinite(gain) & np.isfinite(sm)
    axs[0].scatter(sm[ok], gain[ok], s=7, marker=mk[i], facecolor="none", edgecolor=cols[i], lw=0.6, label=s["label"])
    ok2 = np.isfinite(gain) & np.isfinite(sep) & (sep > 0)
    axs[1].scatter(sep[ok2], gain[ok2], s=7, marker=mk[i], facecolor="none", edgecolor=cols[i], lw=0.6)
    v7[s["key"]] = dict(best=b, n_sim=int(ok.sum()), n_sep=int(ok2.sum()),
                       spearman_gain_smax=float(pd.Series(gain[ok]).corr(pd.Series(sm[ok]), method="spearman")),
                       spearman_gain_sep=float(pd.Series(gain[ok2]).corr(pd.Series(sep[ok2]), method="spearman")))
for ax in axs:
    ax.axhline(0, color="k", lw=0.6); ax.set_yscale("symlog", linthresh=0.1, linscale=0.5)
    yt = [-10, -1, -0.1, 0, 0.1, 1, 10, 100]; ax.set_ylim(-40, 250)
    ax.yaxis.set_major_locator(FixedLocator(yt)); ax.yaxis.set_major_formatter(FixedFormatter([str(v) for v in yt]))
    ax.yaxis.set_minor_locator(NullLocator())
axs[0].set_xlabel("Maximum similarity at τ = 2 s"); axs[1].set_xlabel("Distance to the most similar past event (km)")
axs[1].set_xscale("log"); axs[0].set_ylabel("BEST error − C3 error (km)\n(positive: C3 better)")
panel_label(axs[0], "a"); panel_label(axs[1], "b")
h, l = axs[0].get_legend_handles_labels()
fig.legend(h, l, loc="upper center", bbox_to_anchor=(0.5, 1.07), ncol=3, frameon=False)
fig.tight_layout(); fig.subplots_adjust(top=0.85)
for ext in ("pdf", "png"): fig.savefig(PDFD / f"26_02_Fig7_when_memory_helps.{ext}", dpi=300, bbox_inches="tight")
plt.close(fig); VAL["figures"]["Fig7"] = v7

# ------------------------------------------------------------------ Fig. 8  per-event scatter
fig, axs = plt.subplots(1, len(TEST), figsize=(7.0, 2.5), sharex=True, sharey=True, squeeze=False)
v8 = {}
for i, s in enumerate(TEST):
    ax = axs[0, i]; S = s["J"]["summary"]; E = s["E"]; b = best_of(S, "2")
    x = E[f"{b}_err_t2"].to_numpy(float); y = E["C3_err_t2"].to_numpy(float); ok = np.isfinite(x) & np.isfinite(y)
    x, y = np.clip(x[ok], 0.01, None), np.clip(y[ok], 0.01, None)
    worse = y > x + 1e-9; better = y < x - 1e-9
    ax.scatter(x[~worse], y[~worse], s=6, facecolor="none", edgecolor="#0072B2", lw=0.5, label="C3 better or tied")
    ax.scatter(x[worse], y[worse], s=9, marker="^", facecolor="#D55E00", edgecolor="none", label="C3 worse")
    lim = [0.01, 200]; ax.plot(lim, lim, color="k", lw=0.6)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel(f"BEST ({b}) error at τ = 2 s (km)")
    ax.text(0.03, 0.97, s["label"], transform=ax.transAxes, ha="left", va="top", fontsize=7)
    panel_label(ax, "abc"[i])
    v8[s["key"]] = dict(best=b, n=int(ok.sum()), n_worse=int(worse.sum()), n_better=int(better.sum()),
                       n_tied=int(ok.sum() - worse.sum() - better.sum()),
                       n_worse_by_more_than_5km=int(np.sum(y - x > 5)))
axs[0, 0].set_ylabel("C3 error at τ = 2 s (km)")
h, l = axs[0, 0].get_legend_handles_labels()
fig.legend(h, l, loc="upper center", bbox_to_anchor=(0.5, 1.08), ncol=2, frameon=False)
fig.tight_layout(); fig.subplots_adjust(top=0.88)
for ext in ("pdf", "png"): fig.savefig(PDFD / f"26_02_Fig8_per_event.{ext}", dpi=300, bbox_inches="tight")
plt.close(fig); VAL["figures"]["Fig8"] = v8

# ------------------------------------------------------------------ Fig. 9  learned ranking and trust switch
fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.6), gridspec_kw=dict(width_ratios=[1.4, 1]))
v9 = {"learned": {}, "switch": {}}
ax = axs[0]; w = 0.15; meths = ["BEST", "C3", "C4", "L3", "L4"]
for i, s in enumerate(TEST):
    S = s["J"]["summary"]; L = s.get("ljudg_data"); b = best_of(S, "2")
    if L is None: continue
    for k, m in enumerate(meths):
        r = S[b]["2"] if m == "BEST" else (L["summary"][m]["2"] if m in ("L3", "L4") else S[m]["2"])
        y, lo, hi = r["median_km"], r.get("ci_lo"), r.get("ci_hi")
        st = STY[m]; xx = i + (k - 2) * w
        ax.bar(xx, y, w * 0.9, color=st["c"] if m != "BEST" else "white", edgecolor=st["c"] if m != "BEST" else "k", lw=0.7,
               hatch=None if m != "BEST" else "///", label=m if i == 0 else None)
        if lo is not None and hi is not None: ax.errorbar(xx, y, yerr=[[y - lo], [hi - y]], color="k", lw=0.6, capsize=1.5)
        v9["learned"].setdefault(s["key"], {})[m] = dict(median_km=y, ci_lo=lo, ci_hi=hi, method=(b if m == "BEST" else m))
ax.axhline(FLOOR_KM, color="0.5", lw=0.6, ls=(0, (2, 2)))
ax.set_xticks(range(len(TEST))); ax.set_xticklabels([s["label"].replace(" 20", "\n20") for s in TEST])
ax.set_ylabel("Median error at τ = 2 s (km)"); panel_label(ax, "a")
ax.legend(loc="upper left", bbox_to_anchor=(0.0, -0.28), ncol=5, frameon=False)
ax = axs[1]; gs = [s for s in TEST if s.get("gpev_data") is not None]
for i, s in enumerate(gs):
    G = s["gpev_data"]; cnt = {}
    for k, m in enumerate(("C4", "R", "G")):
        if "tau" not in G.columns or f"err_{m}" not in G.columns:
            stop(f"{s['label']}: expected long format (tau, err_{m}) in {s['gpev']} (columns: {list(G.columns)[:20]})")
        v = G.loc[np.isclose(G["tau"].astype(float), 2.0), f"err_{m}"].to_numpy(float); cnt[m] = int(np.sum(v > 10.0))
        ax.bar(i + (k - 1) * 0.25, cnt[m], 0.22, color=STY[m]["c"], edgecolor="k", lw=0.5, label=m if i == 0 else None)
        ax.text(i + (k - 1) * 0.25, cnt[m] + 0.1, str(cnt[m]), ha="center", va="bottom", fontsize=7)
    v9["switch"][s["key"]] = dict(misses_over_10km=cnt, n=int(np.isclose(G["tau"].astype(float), 2.0).sum()))
ax.set_xticks(range(len(gs))); ax.set_xticklabels([s["label"].replace(" 20", "\n20") for s in gs])
ax.set_ylabel("Events with error > 10 km\nat τ = 2 s"); ax.set_ylim(0, max(max(v["misses_over_10km"].values()) for v in v9["switch"].values()) + 1.5)
ax.text(-0.25, 1.03, "(b)", transform=ax.transAxes, ha="left", va="bottom", fontsize=9, fontweight="bold")
ax.legend(loc="upper left", bbox_to_anchor=(0.0, -0.28), ncol=3, frameon=False)
fig.tight_layout()
for ext in ("pdf", "png"): fig.savefig(PDFD / f"26_02_Fig9_learned_switch.{ext}", dpi=300, bbox_inches="tight")
plt.close(fig); VAL["figures"]["Fig9"] = v9

json.dump(VAL, open(OUTJ, "w"), indent=1)
print(f"[26_02] wrote {OUTJ.relative_to(ROOT)} and PDF/26_02_Fig5..Fig9 (.pdf, .png)")
