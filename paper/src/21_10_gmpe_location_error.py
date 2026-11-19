#!/usr/bin/env python3
# =============================================================================
# Script : 21_10_gmpe_location_error.py  (v2: 図だけを直した。数値の計算と出力の JSON は v1 と同じ)
#          [震央の誤差が、揺れ(計測震度)の予測をどれだけ変えるかを、距離減衰式で計算する。21_04(密な網)と 21_09a
#           (間引いた網)の地震ごとの実際の誤差を使い、物理(BEST)と C4 で比べる。速報への効果を言い過ぎないための根拠]
# Project: ARGUS(新生)— SSJ 2026 の 2 枚目「1〜2 km のずれは問題か」への答え
#
# 何をするか:
#   1. 地震ごとの誤差: data/21_04_per_event.csv(密な網)の τ = 0.5・2 s の BEST と C4 の誤差。BEST の名前は models/21_04_judgment.json の
#      per_tau[τ]["C4"]["best"](C3 の記録の BEST と違う時は、中央値が同じ方法どうしの同点として表示する)。21_09a の結果
#      (data/21_09_per_event_<網>.csv と models/21_09_run_<網>.json)が N = 12・8・5 で 3 つずつ揃っていれば、N ごとにも同じことをする
#      (3 つの網の地震を行としてまとめる。行の数と、違う地震の数を別に出す)。BEST と C4 は、両方に値がある地震だけで比べる。
#   2. 揺れの予測の差: 観測点が正解の震央から Δ km(3・5・10・20・40・80 km)にあり、誤差 e の向きに対して方位 φ(0〜355°、5° おき)に
#      ある時、推定の震央からの距離は Δ' = √(Δ² + e² − 2Δe cos φ)。深さ h は気象庁の値のまま(深さの誤差は入れない)。
#      主の式: 最大速度 PGV の距離減衰式のうち、等価震源距離 Xeq を使う式(Si & Midorikawa 1999。点震源なので Xeq = 震源距離 √(Δ² + h²))
#        log10 PGV = 0.58 Mw + 0.0031 h + d − 1.25 − log10 Xeq − 0.002 Xeq
#      差を取ると Mw・h・d・定数の項は消え、距離の項だけが残る(主の結果は Mw によらない)。
#      感度: 断層最短距離の式 log10 PGV = 0.58 Mw + 0.0038 h + d − 1.29 − log10(X + 0.0028·10^(0.5 Mw)) − 0.002 X を、X に震源距離を
#      入れて Mw 6・7 で(近い距離の飽和の項 0.0028·10^(0.5 Mw) を通してだけ Mw が効く。点震源に当てはめた近似)。
#      係数は 司・翠川(1999、日本建築学会構造系論文集 523)および Si & Midorikawa(2000、12WCEE 0532 の表 4・5、地殻内 d = 0)と
#      OpenQuake の si_midorikawa_1999。PGV は硬い地盤(AVS30 ≈ 600 m/s)。
#      計測震度への換算: I = 2.54 + 1.82 log10 PGV(Midorikawa et al. 1999。Hayashida & Tajima 2007 の式 14 から。地表の PGV)。
#      地盤の増幅が距離によらなければ、差 ΔI = 1.82 × [log10 PGV(推定) − log10 PGV(正解)] には効かない。
#   3. 出力: (網・τ・方法・式・Δ)ごとに、地震ごとの方位平均 |ΔI| の中央値、地震ごとの方位最大 |ΔI| の中央値と最大、
#      震度階級が変わる確率の上限(真の震度が階級の中で一様と仮定し、(地震, 方位) の組で min(|ΔI| / 0.5, 1) を平均。0.5 は 5 弱以上の
#      最も狭い階級の幅で、4 以下(幅 1.0)ではこの半分以下)。比べる目安: 距離減衰式自体のばらつき σ = 0.23(log10 PGV)= 震度で約 0.42。
#      図: τ = 0.5・2 s × (主の式・感度 Mw 7)、横 = 観測点の震央距離(対数)、縦 = 方位平均 |ΔI| の中央値。密な網(実線)と N = 5(破線)、
#      BEST(黒)と C4(朱)。
#      v2 の直し: 凡例を短い 4 項目(色 = 方法、線の形 = 網)にして図の幅に収める(v1 は左右の端が切れた)。各枠の題の 2〜3 行目に
#      誤差の中央値を書く。縦軸は数字で出し(下限は一番小さい線が入る桁)。PNG も保存する。
#
# 限界(結果を読むときに必ず添える):
#   - 点震源。大きい地震(Mw 6.5 以上)では断層の広がりによる距離の違いの方が、0.1〜1 km の震央の誤差よりずっと大きく、
#     この計算はその効果を含まない(向きは決まらない)
#   - 深さの誤差・マグニチュードの誤差は入れていない(速報で大きいのはマグニチュードの誤差であることが多い)
#   - 誤差は小さい地震(1.5 ≤ Mj < 2.0)の実測を使った(大きい地震の誤差の分布は違いうる)
#   - 式のデータの範囲は Mw 5.8〜8.3・21 地震・距離は Mw < 6.3 で 100 km まで。近い距離のデータは少ない
#   - 換算式は 1 つだけ(係数の違う式では ΔI は傾きに比例して変わる)。観測点ごとの地盤の増幅の違いは入れない
#
# Usage : cd ~/SWIFT && uv run python src/21_10_gmpe_location_error.py      (21_09a の後なら間引いた網の結果も使う)
# Output: models/21_10_gmpe_location_error.json・PDF/21_10_F1_intensity_change.pdf(と .png)
# 文献  : 司宏俊・翠川三郎(1999)断層タイプ及び地盤条件を考慮した最大加速度・最大速度の距離減衰式, 日本建築学会構造系論文集 523, 63–70 /
#         Si, H. & Midorikawa, S. (2000) New attenuation relations for peak ground acceleration and velocity considering effects of fault
#         type and site condition, 12WCEE paper 0532 / 翠川三郎・藤本一雄・村松郁栄(1999)計測震度と旧気象庁震度および地震動強さの指標との
#         関係, 地域安全学会論文集 1, 51–56 / Hayashida, T. & Tajima, F. (2007) Earth Planets Space 59, 1111–1125
# =============================================================================
import json, csv, hashlib, datetime as dt
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
for d in ("models", "PDF"): (ROOT / d).mkdir(exist_ok=True)
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
SELF_SHA = sha256(Path(__file__))
print(f"[21_10] 本スクリプト v2 SHA-256 {SELF_SHA[:12]}…")
DIST = [3.0, 5.0, 10.0, 20.0, 40.0, 80.0]; AZ = np.radians(np.arange(0, 360, 5))
SLOPE, CLASS_W, SIGMA_LOG = 1.82, 0.5, 0.23; TAUS = ["0.5", "2"]
MODELS = {"EHD (main)": None, "fault-distance form, Mw 6": 6.0, "fault-distance form, Mw 7": 7.0}
LIMITS = ["point source: for Mw >= 6.5 the finite-fault distance differences are much larger than 0.1-1 km epicentral errors and "
          "are not included (direction of the bias not established)",
          "depth and magnitude errors are not included (in early warning the magnitude error is often the larger one)",
          "location errors measured on small events (1.5 <= Mj < 2.0) are used",
          "Si & Midorikawa (1999) data: Mw 5.8-8.3, 21 events, distances up to 100 km for Mw < 6.3; few near-source data",
          "one PGV-to-intensity conversion (I = 2.54 + 1.82 log10 PGV); site amplification differences between sites are not included",
          "the class-change probability is an upper bound using the narrowest class width (0.5, classes 5- and above)"]
def gdist(R, mw):
    """log10 PGV の距離の項。mw = None は等価震源距離の式、数値は断層最短距離の式(R に震源距離を入れる)"""
    return (-np.log10(R) - 0.002 * R) if mw is None else (-np.log10(R + 0.0028 * 10 ** (0.5 * mw)) - 0.002 * R)
def dI(err, h, delta, mw):
    e = err[:, None]; dp = np.sqrt(np.maximum(delta ** 2 + e ** 2 - 2 * delta * e * np.cos(AZ)[None, :], 0.0))
    R = np.sqrt(delta ** 2 + h[:, None] ** 2); Rp = np.sqrt(dp ** 2 + h[:, None] ** 2)
    return SLOPE * (gdist(Rp, mw) - gdist(R, mw))
def load(p):
    with open(p) as f: return list(csv.DictReader(f))
def col(rows, k):
    if rows and k not in rows[0]: raise SystemExit(f"[21_10] STOP: 列 {k} が無い")
    return np.array([float(r[k]) if r[k] not in ("", None) else np.nan for r in rows])
SRCS = {}
p4, j4 = ROOT / "data/21_04_per_event.csv", ROOT / "models/21_04_judgment.json"
if not p4.exists() or not j4.exists(): raise SystemExit("[21_10] STOP: data/21_04_per_event.csv か models/21_04_judgment.json が無い")
J4 = json.load(open(j4))
for t in TAUS:
    b3, b4 = J4["per_tau"][t]["C3"]["best"], J4["per_tau"][t]["C4"]["best"]
    if b3 != b4: print(f"[21_10] 注意: 21_04 τ = {t} s の BEST は C3 の記録で {b3}、C4 の記録で {b4}(中央値が同じ同点)。C4 の記録の {b4} を使う")
SRCS["dense (full Hi-net, 21_04)"] = dict(parts=[(load(p4), {t: J4["per_tau"][t]["C4"]["best"] for t in TAUS})], files=[p4.name])
for N in (12, 8, 5):
    parts, files = [], []
    for s in (0, 1, 2):
        pc, pj = ROOT / f"data/21_09_per_event_N{N}_s{s}.csv", ROOT / f"models/21_09_run_N{N}_s{s}.json"
        if pc.exists() and pj.exists():
            J = json.load(open(pj)); parts.append((load(pc), {t: J["per_tau"][t]["C4"].get("best") for t in TAUS})); files.append(pc.name)
    if len(parts) == 3: SRCS[f"thinned, {N} stations (21_09a, 3 networks)"] = dict(parts=parts, files=files)
    elif parts: print(f"[21_10] 注意: N = {N} の 21_09a の結果が {len(parts)}/3 しか無いので使わない")
    else: print(f"[21_10] 注意: N = {N} の 21_09a の結果が無い(21_09a の後に実行し直すと入る)")
print(f"[21_10] 使う誤差: {', '.join(SRCS)}")
OUT = {}
for name, S in SRCS.items():
    OUT[name] = {}
    for t in TAUS:
        eb, ec, hh, ids = [], [], [], []
        for rows, best in S["parts"]:
            if best[t] is None: continue
            b, c, h = col(rows, f"{best[t]}_err_t{t}"), col(rows, f"C4_err_t{t}"), col(rows, "depth_km")
            m = np.isfinite(b) & np.isfinite(c) & np.isfinite(h)
            eb.append(b[m]); ec.append(c[m]); hh.append(h[m]); ids += [r["origin_time"] for r, k in zip(rows, m) if k]
        if not eb: continue
        eb, ec, hh = np.concatenate(eb), np.concatenate(ec), np.concatenate(hh)
        if len(eb) == 0: raise SystemExit(f"[21_10] STOP: {name} τ = {t} s で BEST と C4 の両方に値がある地震が 0")
        bn = sorted({best[t] for _, best in S["parts"] if best[t]})
        for meth, e in (("BEST", eb), ("C4", ec)):
            key = f"tau{t}_{meth}"
            OUT[name][key] = dict(method=("/".join(bn) if meth == "BEST" else "C4"), n_rows=int(len(e)), n_distinct_events=len(set(ids)),
                                  error_median_km=float(np.median(e)), rows=[])
            for mname, mw in MODELS.items():
                for dl in DIST:
                    X = np.abs(dI(e, hh, dl, mw)); amax = X.max(1)
                    OUT[name][key]["rows"].append(dict(model=mname, site_epi_km=dl, median_azmean_absdI=float(np.median(X.mean(1))),
                                                       median_azmax_absdI=float(np.median(amax)), max_azmax_absdI=float(amax.max()),
                                                       class_change_prob_upper=float(np.mean(np.minimum(X / CLASS_W, 1.0)))))
print(f"\n[21_10] ===== 予測震度の差 |ΔI|(主の式。地震ごとの方位平均の中央値 / 方位最大の中央値 / 方位最大の最大 / 階級が変わる確率の上限) =====")
print(f"  目安: 距離減衰式自体のばらつき σ = {SIGMA_LOG}(log10 PGV)= 震度で約 {SLOPE * SIGMA_LOG:.2f}")
for name, d in OUT.items():
    print(f"  {name}")
    for t in TAUS:
        for meth in ("BEST", "C4"):
            o = d.get(f"tau{t}_{meth}")
            if o is None: continue
            print(f"    τ = {t} s {meth:<4}({o['method']}、誤差の中央値 {o['error_median_km']:.2f} km、{o['n_rows']} 行・{o['n_distinct_events']} 地震)")
            rs = [r for r in o["rows"] if r["model"] == "EHD (main)"]
            print("      " + "  ".join(f"{r['site_epi_km']:g} km {r['median_azmean_absdI']:.3f}/{r['median_azmax_absdI']:.3f}/{r['max_azmax_absdI']:.2f}/{r['class_change_prob_upper']:.3f}" for r in rs))
            for mname in list(MODELS)[1:]:
                rs = [r for r in o["rows"] if r["model"] == mname]
                print(f"      (感度 {mname}) " + "  ".join(f"{r['site_epi_km']:g} km {r['median_azmean_absdI']:.3f}" for r in rs))
print("[21_10] 限界: " + " / ".join(LIMITS))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
plt.rcParams.update({"font.size": 11, "axes.facecolor": "white", "figure.facecolor": "white", "savefig.facecolor": "white"})
names = list(OUT); dense = names[0]; sparse = next((n for n in names if n.startswith("thinned, 5 ")), None)
if sparse is None: print("[21_10] 注意: N = 5 の間引いた網が無いので、図は密な網だけ")
rowsM = ["EHD (main)", "fault-distance form, Mw 7"]
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
NET = [(dense, "-", "Dense Hi-net (all stations, 21_04)")] + ([(sparse, "--", "Thinned to 5 stations (3 networks, 21_09a)")] if sparse else [])
METH = [("BEST", "#000000", "Best method without waveform similarity (BEST)"), ("C4", "#D55E00", "C4 (physics × similar past events + station corrections)")]
def med(nm, t, meth):
    o = OUT[nm].get(f"tau{t}_{meth}"); return None if o is None else o["error_median_km"]
VMIN = min((r["median_azmean_absdI"] for nm, _, _ in NET for t in TAUS for meth, _, _ in METH if OUT[nm].get(f"tau{t}_{meth}")
           for r in OUT[nm][f"tau{t}_{meth}"]["rows"] if r["model"] in rowsM and r["median_azmean_absdI"] > 0), default=1e-3)
VMAX = max((r["median_azmean_absdI"] for nm, _, _ in NET for t in TAUS for meth, _, _ in METH if OUT[nm].get(f"tau{t}_{meth}")
            for r in OUT[nm][f"tau{t}_{meth}"]["rows"] if r["model"] in rowsM), default=0.1)
YLO = 10.0 ** np.floor(np.log10(VMIN / 1.2))                                            # 一番小さい線が枠に入る桁まで下げる
fig, axs = plt.subplots(2, len(TAUS), figsize=(12, 8.8), sharex=True, sharey=True)
for i, mname in enumerate(rowsM):
    for j, t in enumerate(TAUS):
        ax = axs[i, j]
        for nm, ls, _ in NET:
            for meth, c, _ in METH:
                o = OUT[nm].get(f"tau{t}_{meth}")
                if o is None: continue
                rs = [r for r in o["rows"] if r["model"] == mname]
                ax.plot([r["site_epi_km"] for r in rs], [r["median_azmean_absdI"] for r in rs], ls, color=c, marker="o", ms=4)
        ax.axhline(SLOPE * SIGMA_LOG, color="0.5", ls=":", lw=1)
        ax.text(3.1, SLOPE * SIGMA_LOG * 1.12, f"GMPE scatter alone ≈ {SLOPE * SIGMA_LOG:.2f} intensity units", fontsize=9, color="0.35")
        ax.set_xscale("log"); ax.set_yscale("log"); ax.grid(alpha=0.3, which="major")
        ax.set_xticks(DIST); ax.set_xticklabels([f"{d:g}" for d in DIST]); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        YHI = max(1.0, VMAX * 1.3); ax.set_ylim(YLO, YHI)
        YT = [10.0 ** k for k in range(int(round(np.log10(YLO))), int(np.floor(np.log10(YHI))) + 1)]
        ax.yaxis.set_major_locator(FixedLocator(YT)); ax.yaxis.set_major_formatter(FixedFormatter([f"{y:g}" for y in YT]))
        ax.yaxis.set_minor_locator(NullLocator())
        mtxt = "; ".join(f"{'dense' if nm == dense else '5 stations'} {med(nm, t, 'BEST'):.2f} → {med(nm, t, 'C4'):.2f} km"
                         for nm, _, _ in NET if med(nm, t, "BEST") is not None and med(nm, t, "C4") is not None)
        ax.set_title(f"{'Equivalent-hypocentral-distance model (main)' if i == 0 else 'Fault-distance form, Mw 7 (sensitivity)'}, τ = {t} s\n"
                     + (f"median epicentral error, BEST → C4:\n{mtxt}" if mtxt else ""), fontsize=10)
        if i == 1: ax.set_xlabel("Site epicentral distance from the true epicentre (km)")
        if j == 0: ax.set_ylabel("Median over events of\nazimuth-averaged |ΔI|")
hs = [Line2D([], [], color=c, marker="o", ms=4, lw=1.8, label=l) for _, c, l in METH] + [Line2D([], [], color="0.3", ls=ls, lw=1.8, label=l) for _, ls, l in NET]
fig.legend(handles=hs, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.0), fontsize=10)
fig.suptitle("Change in predicted JMA intensity caused by the epicentral error\n(Si & Midorikawa 1999 PGV, point source; I = 2.54 + 1.82 log10 PGV)",
             y=0.995, fontsize=12)
fig.tight_layout(rect=(0, 0.09, 1, 0.965))
fig.savefig(ROOT / "PDF/21_10_F1_intensity_change.pdf"); fig.savefig(ROOT / "PDF/21_10_F1_intensity_change.png", dpi=200); plt.close(fig)
json.dump(dict(script="21_10_gmpe_location_error.py", script_sha256=SELF_SHA, utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               inputs={k: v["files"] for k, v in SRCS.items()}, site_epi_km=DIST, azimuth_step_deg=5, slope=SLOPE, class_width=CLASS_W,
               gmpe_sigma_log10=SIGMA_LOG, models={k: ("equivalent hypocentral distance (Xeq = hypocentral distance)" if v is None
                                                       else f"shortest fault distance form with hypocentral distance, Mw {v}") for k, v in MODELS.items()},
               conversion="I = 2.54 + 1.82 log10 PGV", results=OUT, limits=LIMITS), open(ROOT / "models/21_10_gmpe_location_error.json", "w"), indent=1)
print("[21_10] 出力: models/21_10_gmpe_location_error.json・PDF/21_10_F1_intensity_change.pdf(と .png)")
