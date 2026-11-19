#!/usr/bin/env python3
# =============================================================================
# Script : 25_04e_shimane2018_station_pick_diagnose.py  (v1)
#          [局ごとの検測の調べ(読むだけの記述)。事前登録 25 の 5.3 節では、25_04d の結果によらず必ず回し、この CSV の
#           epi_from_mainshock_km・n・dev_s で G-clock2 の (c) を 80 km 以内(止める)と 80 km より遠い(止めずに印)に分ける]
# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の入力の確かめ
# 派生元 : 24_04e_nagano2014_station_pick_diagnose.py v1(SHA-256 befca1b3326d18659d249c7ee9e5b1b1f364828c8a4a85c3cafc1bba16f67931。事前登録 24 で凍結。
#          = 21_20e v1 と同じ計算)。計算は 1 字も変えていない。変えたのは、既定のキャッシュの場所・表示の [25_04e] と系列の名前・
#          出力の名前(data/25_04e_station_picks.csv・PDF/25_04e_station_picks.pdf)・図の題だけ(DIFF_LOG_25.md)。
#
# 何をするか(21_20e と同じ): キャッシュの P を測った検測(p_fallback = 0)の残り r = tp_times − dist_km / 6.0 を局ごとに出し、
#   本震(キャッシュの Mj 最大)からの震央距離・検測の数・中央値・Mj の 3 区分の中央値・|r − 全体の中央値| > 3 s の割合を表にする。
#   --ref-cache に鳥取 2026 のキャッシュを渡すと、同じ表を参考に出す(判定には使わない)。
#
# Usage(Colab。ノート 25_shimane2018_colab.ipynb の セル N14):
#   !python /content/drive/MyDrive/ARGUS/src/25_04e_shimane2018_station_pick_diagnose.py --base /content/ARGUS_shimane2018 \
#       --ref-cache /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt
# =============================================================================
import sys, csv, argparse
from pathlib import Path
import numpy as np
import torch

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True)
ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt")
ap.add_argument("--ref-cache", default="")
a = ap.parse_args()
VP = 6.0
BASE = Path(a.base)

def table(path):
    EV = torch.load(path, weights_only=False)
    big = max(EV, key=lambda e: float(e["mw"])); ml, mo = float(big["src_loc"][0]), float(big["src_loc"][1])
    rows = {}
    for e in EV:
        n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
        loc = np.asarray(e["sta_locs"], float)[:n]; sl = np.asarray(e["src_loc"], float); mj = float(e["mw"])
        if "dist_km" in e: d = np.asarray(e["dist_km"], float)[:n]
        else:
            epi = 111.19 * np.hypot(loc[:, 0] - sl[0], (loc[:, 1] - sl[1]) * np.cos(np.radians(sl[0]))); d = np.hypot(epi, sl[2])
        for k in range(n):
            if pf[k] != 0 or not np.isfinite(tp[k]): continue
            key = f"{loc[k, 0]:.4f},{loc[k, 1]:.4f}"
            rows.setdefault(key, []).append((tp[k] - d[k] / VP, mj, d[k]))
    allr = np.concatenate([np.array([x[0] for x in v]) for v in rows.values()]); med = float(np.median(allr))
    out = []
    for key, v in rows.items():
        r = np.array([x[0] for x in v]); m = np.array([x[1] for x in v]); dd = np.array([x[2] for x in v])
        la, lo = map(float, key.split(","))
        epi_main = 111.19 * np.hypot(la - ml, (lo - mo) * np.cos(np.radians(ml)))
        def md(sel): return (float(np.median(r[sel])), int(sel.sum())) if sel.sum() else (None, 0)
        lo_, mid_, hi_ = md(m < 2.0), md((m >= 2.0) & (m < 3.0)), md(m >= 3.0)
        out.append(dict(station=key, epi_from_mainshock_km=round(epi_main, 1), median_hypo_dist_km=round(float(np.median(dd)), 1), n=len(r),
                        median_s=round(float(np.median(r)), 3), dev_s=round(float(np.median(r)) - med, 3),
                        median_mj_lt2=None if lo_[0] is None else round(lo_[0], 3), n_mj_lt2=lo_[1],
                        median_mj_2to3=None if mid_[0] is None else round(mid_[0], 3), n_mj_2to3=mid_[1],
                        median_mj_ge3=None if hi_[0] is None else round(hi_[0], 3), n_mj_ge3=hi_[1],
                        frac_off_gt3s=round(float(np.mean(np.abs(r - med) > 3.0)), 3)))
    out.sort(key=lambda x: x["epi_from_mainshock_km"])
    return med, out

def show(name, med, out):
    print(f"\n[25_04e] ===== {name}: 全体の中央値 {med:+.3f} s(局 {len(out)}、本震からの距離の順)=====")
    print("  局(緯度,経度)        本震から km  検測   中央値   ずれ   Mj<2 の中央値(数)   2≤Mj<3(数)        Mj≥3(数)         |r−全体|>3 s")
    f = lambda v, n: "     —      " if v is None else f"{v:+7.2f} ({n:4d})"
    for x in out:
        print(f"  {x['station']:<20} {x['epi_from_mainshock_km']:7.1f}   {x['n']:5d}  {x['median_s']:+6.2f}  {x['dev_s']:+6.2f}   "
              f"{f(x['median_mj_lt2'], x['n_mj_lt2'])}   {f(x['median_mj_2to3'], x['n_mj_2to3'])}   {f(x['median_mj_ge3'], x['n_mj_ge3'])}   "
              f"{x['frac_off_gt3s']:.2f}")

cp = BASE / a.cache
if not cp.exists(): sys.exit(f"[25_04e] STOP: {cp} が無い")
med, out = table(cp); show("島根県西部 2018", med, out)
(BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
with open(BASE / "data" / "25_04e_station_picks.csv", "w", newline="") as fo:
    w = csv.DictWriter(fo, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
ref = None
if a.ref_cache:
    if Path(a.ref_cache).exists():
        ref = table(Path(a.ref_cache)); show("参考: 鳥取 2026(21_02 のキャッシュ)", *ref)
    else:
        print(f"[25_04e] 注意: 参考のキャッシュ {a.ref_cache} が無いので飛ばした")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
panels = [("Western Shimane 2018", med, out)] + ([("West Tottori 2026 (reference)", *ref)] if ref else [])
fig, axs = plt.subplots(1, len(panels), figsize=(6.2 * len(panels), 4.4), squeeze=False)
for ax, (nm, m0, o) in zip(axs[0], panels):
    x = [s["epi_from_mainshock_km"] for s in o]
    for key, lab, c, mk in (("median_s", "All picks", "0.3", "o"), ("median_mj_lt2", "Mj < 2.0", "tab:orange", "v"),
                            ("median_mj_2to3", "2.0 <= Mj < 3.0", "tab:green", "s"), ("median_mj_ge3", "Mj >= 3.0", "tab:blue", "^")):
        xs = [xi for xi, s in zip(x, o) if s[key] is not None]; ys = [s[key] - m0 for s in o if s[key] is not None]
        ax.scatter(xs, ys, s=18, color=c, marker=mk, label=lab, alpha=0.85)
    ax.axhspan(-1.0, 1.0, color="tab:green", alpha=0.1, label="G-clock2 (c) tolerance (+/- 1.0 s)")
    ax.axhline(0, color="k", lw=0.8); ax.grid(alpha=0.3)
    ax.set_xlabel("Epicentral distance of the station from the mainshock (km)")
    ax.set_ylabel("Station median of (P time - distance / 6.0 km/s), minus the median of all picks (s)")
    ax.set_title(nm, fontsize=10)
axs[0][0].legend(loc="upper center", bbox_to_anchor=(0.5 * len(panels) + 0.05 * (len(panels) - 1), -0.15), ncol=5, frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(BASE / "PDF" / "25_04e_station_picks.pdf", bbox_inches="tight"); plt.close(fig)
print(f"\n[25_04e] 出力: {BASE / 'data' / '25_04e_station_picks.csv'}、{BASE / 'PDF' / '25_04e_station_picks.pdf'}")
