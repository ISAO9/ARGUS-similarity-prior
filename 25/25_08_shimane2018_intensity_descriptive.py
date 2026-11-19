#!/usr/bin/env python3
# =============================================================================
# Script : 25_08_shimane2018_intensity_descriptive.py  (v1)
#          [H6(記述。判定に使わない): 島根県西部 2018 の試験の地震で、震央の誤差が揺れ(計測震度)の予測をどれだけ変えるかを、
#           21_10 と同じ距離減衰式・同じ換算で計算する。BEST・C3・C4(オフラインの検測)と、τ までの検測の BEST・C3 を並べる]
# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の記述。「km 未満の改善に実用上の意味はあるか」への答えの材料
# 派生元 : 24_08_nagano2014_intensity_descriptive.py v1(SHA-256 80391a29309da7a8b7b32821d8c4076ffc1e0e56ec85e6cf2c8ed498ee2b5eb6。事前登録 24 で凍結。
#          = 21_10 v2 と同じ計算を 24_05 の出力に当てたもの。長野では回していない)。
#          予測震度の差の計算・方法・図・--ref-suffix の扱い・INCONCLUSIVE と H5 が NOT-EVALUATED の時の扱いは 24_08 v1 と 1 字も変えていない。
#          変えたのは次だけ(DIFF_LOG_25.md): 入力 = 25_05 の data/25_05_per_event.csv と models/25_05_judgment.json(--dev では _dev)、
#          照らす 25_05 の SHA-256 は SHA_2505(凍結の時に書く)、出力 = models/25_08_intensity.json・PDF/25_08_F1_intensity_change.pdf(と .png)、
#          表示の [25_08]、図の題の系列の名前、事前登録の番号(24 → 25)。
#
# なぜ検定にしないか(事前登録 25 の 2 節。24 と同じ): 同じ地震(同じ深さ)なら |ΔI| は震央の誤差の単調な関数なので、「C4 は BEST より |ΔI| が
#   小さい」の検定は H2 と地震ごとの勝ち負けの向きが同じになり、新しい証拠にならない。大きさを σ ≈ 0.42(震度)と並べて記述する。
# 限界(21_10 と同じ。結果に必ず添える): 点震源・深さとマグニチュードの誤差を入れない・誤差は小さい地震(1.5 ≤ Mj < 2.0)の実測・
#   式のデータの範囲(Mw 5.8〜8.3、近い距離が少ない)・換算式は 1 つ・観測点ごとの地盤の増幅を入れない・階級が変わる確率は上限。
#
# Usage : cd ~/SWIFT && uv run python src/25_08_shimane2018_intensity_descriptive.py        (25_05 の本番の後)
#         cd ~/SWIFT && uv run python src/25_08_shimane2018_intensity_descriptive.py --dev  (25_05 の dev の後。配管の確かめ)
# 文献  : 21_10 と同じ(司・翠川 1999、Si & Midorikawa 2000、翠川ほか 1999、Hayashida & Tajima 2007)
# =============================================================================
import json, csv, hashlib, argparse, datetime as dt
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
_ap = argparse.ArgumentParser(); _ap.add_argument("--dev", action="store_true", help="25_05 の dev の出力で回す(配管の確かめ)")
_ap.add_argument("--ref-suffix", default="", help="25_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
_A = _ap.parse_args(); DEV = _A.dev
SHA_2505 = "80309ce7012b89af0c052e225cb66b2e15ee104af247937b63510064f9c11398"                          # 事前登録 25 で凍結する 25_05 v1 の SHA-256
for d in ("models", "PDF"): (ROOT / d).mkdir(exist_ok=True)
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
SELF_SHA = sha256(Path(__file__))
print(f"[25_08] 本スクリプト v1 SHA-256 {SELF_SHA[:12]}…")
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
    if rows and k not in rows[0]: raise SystemExit(f"[25_08] STOP: 列 {k} が無い")
    return np.array([float(r[k]) if r[k] not in ("", None) else np.nan for r in rows])
# ---- 25_08: 入力は 25_05 の本番の CSV と JSON だけ(島根県西部 2018、密な網。間引いた網は無い)
SFX = "_dev" if DEV else ""
RSFX = "_dev" if DEV else _A.ref_suffix
p5, j5 = ROOT / f"data/25_05_per_event{RSFX}.csv", ROOT / f"models/25_05_judgment{RSFX}.json"
if not j5.exists(): raise SystemExit(f"[25_08] STOP: {j5.relative_to(ROOT)} が無い(25_05 の後に回す。やり直した時は --ref-suffix を渡す)")
J5 = json.load(open(j5))
if J5.get("verdict") == "INCONCLUSIVE":
    raise SystemExit("[25_08] STOP: 25_05 の判定が INCONCLUSIVE(評価できる試験の地震が 30 未満)で CSV が無いため、H6 は計算しない(事前登録 25 の 8 節)")
if not p5.exists(): raise SystemExit(f"[25_08] STOP: {p5.relative_to(ROOT)} が無い(25_05 の後に回す)")
if J5.get("script_sha256") != SHA_2505: raise SystemExit(f"[25_08] STOP: 25_05 の結果が、凍結した 25_05 v1(SHA-256 {SHA_2505[:12]}…)のものでない")
if not DEV:
    _O = ROOT / "models/25_05_opened.json"
    _c = [r for r in (json.load(open(_O)) if _O.exists() else []) if str(r.get("status", "")).startswith("completed")]
    if not _c or _c[0].get("suffix", "") != RSFX or J5.get("suffix", "") != RSFX:
        raise SystemExit(f"[25_08] STOP: --ref-suffix '{RSFX}' が、models/25_05_opened.json で最初に completed になった 25_05 の実行と違う")
rows5 = load(p5)
H5_OK = bool(J5.get("causal", {}).get("evaluated", False))
if len(rows5) != int(J5["n_evaluated"]): raise SystemExit(f"[25_08] STOP: CSV の行の数 {len(rows5)} が n_evaluated {J5['n_evaluated']} と違う")
print(f"[25_08] 入力: {p5.name}(SHA-256 {sha256(p5)[:12]}…)  {len(rows5)} 地震  25_05 の判定 {J5.get('verdict')}  25_05 の SHA-256 {str(J5.get('script_sha256'))[:12]}…")
# 方法: BEST(H1 と同じ選び方: per_tau[τ]["C3"]["best"])・C3・C4(オフラインの検測)と、τ までの検測の BEST・C3(25_05 の causal)
METHODS = {}
for t in TAUS:
    bo = J5["per_tau"][t]["C3"]["best"]
    METHODS[t] = [("BEST", f"{bo}_err_t{t}", bo), ("C3", f"C3_err_t{t}", "C3"), ("C4", f"C4_err_t{t}", "C4")]
    if H5_OK:
        bc = J5["causal"]["per_tau"][t]["C3"]["best"]
        METHODS[t] += [("BEST, causal picks", f"{bc}_causal_err_t{t}", bc), ("C3, causal picks", f"C3_causal_err_t{t}", "C3")]
if not H5_OK: print("[25_08] 25_05 の H5 は NOT-EVALUATED: τ までの検測の行は作らない")
hh_all = col(rows5, "depth_km")
OUT = {"Western Shimane 2018 (25_05)": {}}
for t in TAUS:
    for lab, cname, mname in METHODS[t]:
        e = col(rows5, cname); m = np.isfinite(e) & np.isfinite(hh_all)
        if m.sum() == 0: continue
        key = f"tau{t}_{lab}"
        o = dict(method=mname, column=cname, n_rows=int(m.sum()), error_median_km=float(np.median(e[m])), rows=[])
        for mname2, mw in MODELS.items():
            for dl in DIST:
                X = np.abs(dI(e[m], hh_all[m], dl, mw)); amax = X.max(1)
                o["rows"].append(dict(model=mname2, site_epi_km=dl, median_azmean_absdI=float(np.median(X.mean(1))),
                                      median_azmax_absdI=float(np.median(amax)), max_azmax_absdI=float(amax.max()),
                                      class_change_prob_upper=float(np.mean(np.minimum(X / CLASS_W, 1.0)))))
        OUT["Western Shimane 2018 (25_05)"][key] = o
print(f"\n[25_08] ===== 予測震度の差 |ΔI|(主の式。地震ごとの方位平均の中央値 / 方位最大の中央値 / 方位最大の最大 / 階級が変わる確率の上限) =====")
print(f"  目安: 距離減衰式自体のばらつき σ = {SIGMA_LOG}(log10 PGV)= 震度で約 {SLOPE * SIGMA_LOG:.2f}")
NAME = list(OUT)[0]
for t in TAUS:
    for lab, _, _ in METHODS[t]:
        o = OUT[NAME].get(f"tau{t}_{lab}")
        if o is None: continue
        rs = [r for r in o["rows"] if r["model"] == "EHD (main)"]
        print(f"  τ = {t} s {lab:<20}({o['method']}、誤差の中央値 {o['error_median_km']:.2f} km、{o['n_rows']} 地震)")
        print("      " + "  ".join(f"{r['site_epi_km']:g} km {r['median_azmean_absdI']:.3f}/{r['median_azmax_absdI']:.3f}/{r['max_azmax_absdI']:.2f}/{r['class_change_prob_upper']:.3f}" for r in rs))
print("[25_08] 限界: " + " / ".join(LIMITS))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator, NullFormatter
from matplotlib.lines import Line2D
plt.rcParams.update({"font.size": 11, "axes.facecolor": "white", "figure.facecolor": "white", "savefig.facecolor": "white"})
STY = {"BEST": ("#000000", "-"), "C3": ("#D55E00", "-"), "C4": ("#CC79A7", "-"), "BEST, causal picks": ("#000000", "--"), "C3, causal picks": ("#D55E00", "--")}
vals = [r["median_azmean_absdI"] for o in OUT[NAME].values() for r in o["rows"] if r["model"] == "EHD (main)" and r["median_azmean_absdI"] > 0]
YLO = 10.0 ** np.floor(np.log10(min(vals) / 1.2)) if vals else 1e-3; YHI = max(1.0, (max(vals) if vals else 0.1) * 1.3)
fig, axs = plt.subplots(1, len(TAUS), figsize=(12, 4.8), sharey=True)
for ax, t in zip(np.atleast_1d(axs), TAUS):
    for lab, _, _ in METHODS[t]:
        o = OUT[NAME].get(f"tau{t}_{lab}")
        if o is None: continue
        rs = [r for r in o["rows"] if r["model"] == "EHD (main)"]; c, ls = STY[lab]
        ax.plot([r["site_epi_km"] for r in rs], [r["median_azmean_absdI"] for r in rs], ls, color=c, marker="o", ms=4)
    ax.axhline(SLOPE * SIGMA_LOG, color="0.5", ls=":", lw=1)
    ax.text(3.1, SLOPE * SIGMA_LOG * 1.12, f"GMPE scatter alone ≈ {SLOPE * SIGMA_LOG:.2f}", fontsize=9, color="0.35")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.grid(alpha=0.3, which="major"); ax.set_ylim(YLO, YHI)
    ax.set_xticks(DIST); ax.set_xticklabels([f"{d:g}" for d in DIST]); ax.xaxis.set_minor_formatter(NullFormatter())
    YT = [10.0 ** k for k in range(int(round(np.log10(YLO))), int(np.floor(np.log10(YHI))) + 1)]
    ax.yaxis.set_major_locator(FixedLocator(YT)); ax.yaxis.set_major_formatter(FixedFormatter([f"{y:g}" for y in YT])); ax.yaxis.set_minor_locator(NullLocator())
    med = {lab: OUT[NAME][f"tau{t}_{lab}"]["error_median_km"] for lab, _, _ in METHODS[t] if f"tau{t}_{lab}" in OUT[NAME]}
    ax.set_title(f"τ = {t} s; median epicentral error (km):\n" + ", ".join(f"{k} {v:.2f}" for k, v in med.items() if "causal" not in k)
                 + ("\ncausal picks: " + ", ".join(f"{k.split(',')[0]} {v:.2f}" for k, v in med.items() if "causal" in k) if H5_OK else
                    "\ncausal picks: not evaluated"), fontsize=9)
    ax.set_xlabel("Site epicentral distance from the true epicentre (km)")
np.atleast_1d(axs)[0].set_ylabel("Median over events of\nazimuth-averaged |ΔI|")
hs = [Line2D([], [], color=STY[l][0], ls=STY[l][1], marker="o", ms=4, lw=1.8, label=l) for l in STY if H5_OK or "causal" not in l]
fig.legend(handles=hs, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.0), fontsize=10)
fig.suptitle("Western Shimane 2018" + (" (DEV)" if DEV else "") + ": change in predicted JMA intensity caused by the epicentral error\n"
             "(Si & Midorikawa 1999 PGV, equivalent-hypocentral-distance form, point source; I = 2.54 + 1.82 log10 PGV)", y=0.995, fontsize=11)
fig.tight_layout(rect=(0, 0.12, 1, 0.93))
fig.savefig(ROOT / f"PDF/25_08_F1_intensity_change{SFX}.pdf", bbox_inches="tight"); fig.savefig(ROOT / f"PDF/25_08_F1_intensity_change{SFX}.png", dpi=200, bbox_inches="tight"); plt.close(fig)
json.dump(dict(script="25_08_shimane2018_intensity_descriptive.py", script_sha256=SELF_SHA, utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               inputs=dict(csv=p5.name, csv_sha256=sha256(p5), judgment=j5.name, judgment_sha256=sha256(j5), script_25_05_sha256=J5.get("script_sha256"),
                           ref_suffix=RSFX, h5_evaluated=H5_OK),
               site_epi_km=DIST, azimuth_step_deg=5, slope=SLOPE, class_width=CLASS_W, gmpe_sigma_log10=SIGMA_LOG,
               models={k: ("equivalent hypocentral distance (Xeq = hypocentral distance)" if v is None else f"shortest fault distance form with hypocentral distance, Mw {v}") for k, v in MODELS.items()},
               conversion="I = 2.54 + 1.82 log10 PGV", results=OUT, limits=LIMITS, descriptive_only=True),
          open(ROOT / f"models/25_08_intensity{SFX}.json", "w"), indent=1)
print(f"[25_08] 出力: models/25_08_intensity{SFX}.json・PDF/25_08_F1_intensity_change{SFX}.pdf(と .png)")
