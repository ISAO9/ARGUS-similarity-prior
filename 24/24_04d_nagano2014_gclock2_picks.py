#!/usr/bin/env python3
# =============================================================================
# Script : 24_04d_nagano2014_gclock2_picks.py  (v1)
#          [G-clock2: 24_03h の後のキャッシュの PhaseNet の P の検測(全ての地震・全ての局)を使って、長野県北部 2014 の波形の
#           時刻がずれていないかを確かめる。規則(a)〜(f)と閾値は 21_04d v1・21_20d v1 と同じ]
# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の確かめ
# 派生元 : 21_20d_osaka2018_gclock2_picks.py v1(SHA-256 606d0eea2f76a8607c7844f83a93056759640974bce7f11ccfe690ecb6e7c1d6)。
#          計算・規則・閾値・止め方(FAIL なら exit code 1)は 1 字も変えていない。変えたのは次だけ(DIFF_LOG_24.md):
#          既定のキャッシュ(..._nagano2014_m15_r1.pt = 24_03h の出力)と報告(data/24_02_report.json)の場所、表示の [24_04d]、
#          出力の名前(data/24_04d_gclock2.json・PDF/24_04d_gclock2.pdf)、JSON の script、図の題と軸の年。
#          FAIL の時の扱いは、事前登録 24 の 5.3 節(21_20 の案 C と同じ: (a)・(b)・(d)・(e)・(f) のどれかの FAIL で止める。
#          (c) は 24_04e の表で 80 km 以内(止める)と 80 km より遠い(止めずに印を付ける)に分ける)。
#
# 何をするか(21_20d と同じ):
#   1. キャッシュの全ての地震・全ての局のうち、PhaseNet で P を測った検測(p_fallback = 0)について、残り r = tp_times − dist_km / 6.0 s を出す。
#   2. (a) |全体の中央値| ≤ 1.5 s (b) 日ごと ≤ 0.5 s (c) 局ごと ≤ 1.0 s (d) 1 時間ごと ≤ 0.5 s
#      (e) 24_02 の報告の G-clock の地震がそれぞれ ≤ 0.5 s(検測 4 以上) (f) 局ごとの P を測った割合が全局の中央値の 0.5 倍以上。
#      検測 20 以上の日・局・時間で数える。日と時間は日本時間。
#   3. 参考(判定には使わない): --ref-cache に鳥取 2026 のキャッシュ。
#   4. 出力: data/24_04d_gclock2.json / PDF/24_04d_gclock2.pdf。FAIL なら exit code 1。
#
# Usage(Colab、24_03h の後に。ノート 24_nagano2014_colab.ipynb の セル N13):
#   !python /content/drive/MyDrive/ARGUS/src/24_04d_nagano2014_gclock2_picks.py --base /content/ARGUS_nagano2014 \
#       --ref-cache /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt
# 止める条件(STOP): キャッシュが無い・P を測った検測が 100 未満・検測 20 以上の日・局・時間のどれかが 0・24_02 の報告が無い
# =============================================================================
import sys, json, argparse
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import torch

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True, help="ARGUS_nagano2014 の場所(Colab のローカルなら /content/ARGUS_nagano2014)")
ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt")
ap.add_argument("--ref-cache", default="", help="参考: 鳥取 2026 のキャッシュ(無くてよい)")
ap.add_argument("--report", default="data/24_02_report.json", help="24_02 の報告(G-clock の地震を読む。--base からの場所)")
a = ap.parse_args()
VP, TOL_ALL, TOL_DAY, TOL_STA, MIN_N = 6.0, 1.5, 0.5, 1.0, 20
TOL_HOUR, TOL_EV, MIN_EV, MIN_FRAC_RATIO = 0.5, 0.5, 4, 0.5
BASE = Path(a.base)

def jst(ot):                                                     # キャッシュの origin_time は UTC(15_01c v3.3・21_20c)。日本時間にする
    t = datetime.strptime(str(ot).replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
    return t + timedelta(hours=9)
def residuals(path):
    EV = torch.load(path, weights_only=False)
    r, day, sta, hour, evi = [], [], [], [], []
    seen = {}                                                   # 局 -> [現れた数, P を測った数]
    for ie, e in enumerate(EV):
        tj = jst(e["origin_time"])
        n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]
        pf = np.asarray(e["p_fallback"]).astype(int)[:n]; loc = np.asarray(e["sta_locs"], float)[:n]
        if "dist_km" in e: d = np.asarray(e["dist_km"], float)[:n]
        else:                                                   # 古いキャッシュ: 15_01c と同じ式で震源距離を出す
            sl = np.asarray(e["src_loc"], float)
            epi = 111.19 * np.hypot(loc[:, 0] - sl[0], (loc[:, 1] - sl[1]) * np.cos(np.radians(sl[0]))); d = np.hypot(epi, sl[2])
        for k in range(n):
            key = f"{loc[k, 0]:.4f},{loc[k, 1]:.4f}"; sv = seen.setdefault(key, [0, 0]); sv[0] += 1
            if pf[k] != 0 or not np.isfinite(tp[k]) or not np.isfinite(d[k]): continue
            sv[1] += 1
            r.append(tp[k] - d[k] / VP); day.append(f"{tj:%Y-%m-%d}"); hour.append(f"{tj:%Y-%m-%d %H}"); sta.append(key); evi.append(ie)
    return EV, np.array(r), np.array(day), np.array(sta), np.array(hour), np.array(evi), seen

def groups(r, g):
    return {k: dict(n=int((g == k).sum()), median=float(np.median(r[g == k]))) for k in sorted(set(g.tolist()))}
def summarise(r, day, sta, hour):
    med = float(np.median(r)); dd, ss, hh = groups(r, day), groups(r, sta), groups(r, hour)
    def mx(G):
        v = [abs(x["median"] - med) for x in G.values() if x["n"] >= MIN_N]
        return (max(v) if v else None), len(v)
    (dev_day, nd), (dev_sta, ns), (dev_hour, nh) = mx(dd), mx(ss), mx(hh)
    return dict(n=int(len(r)), median_s=med, iqr_s=float(np.subtract(*np.percentile(r, [75, 25]))), by_day=dd, by_station=ss, by_hour=hh,
                max_day_dev_s=dev_day, n_days=nd, max_station_dev_s=dev_sta, n_stations=ns, max_hour_dev_s=dev_hour, n_hours=nh)

cp = BASE / a.cache
if not cp.exists(): sys.exit(f"[24_04d] STOP: キャッシュ {cp} が無い(24_03h の後に回す)")
EVS, r, day, sta, hour, evi, seen = residuals(cp); nev = len(EVS)
if len(r) < 100: sys.exit(f"[24_04d] STOP: P を測った検測が {len(r)}(100 未満)")
S = summarise(r, day, sta, hour)
if S["n_days"] == 0 or S["n_stations"] == 0 or S["n_hours"] == 0:
    sys.exit(f"[24_04d] STOP: 検測 {MIN_N} 以上の日・局・時間のどれかが 0(判定できない)")
pa = abs(S["median_s"]) <= TOL_ALL; pd_ = S["max_day_dev_s"] <= TOL_DAY; ps = S["max_station_dev_s"] <= TOL_STA
ph = S["max_hour_dev_s"] <= TOL_HOUR
# (e) 24_02 の G-clock の地震: その地震の P を測った検測(MIN_EV 以上)の中央値 − 全体の中央値
rp = BASE / a.report
if not rp.exists(): sys.exit(f"[24_04d] STOP: 24_02 の報告 {rp} が無い")
gc = json.load(open(rp))["gates"]["clock"]
EVJ = [jst(e["origin_time"]) for e in EVS]
EVC = []
for c in gc:
    t = datetime.strptime(c["origin_jst"].replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
    j = min(range(nev), key=lambda i: abs((EVJ[i] - t).total_seconds()))
    dt_ = abs((EVJ[j] - t).total_seconds())
    m = evi == j
    md = float(np.median(r[m])) if m.sum() else None
    ok = bool(dt_ <= 1.5 and m.sum() >= MIN_EV and md is not None and abs(md - S["median_s"]) <= TOL_EV)
    EVC.append(dict(origin_jst=c["origin_jst"][:22], mj=c["mj"], gclock_stalta_median_abs_s=c["median_abs_resid_s"],
                    found_dt_s=dt_, n_picks=int(m.sum()), median_s=md, dev_s=(None if md is None else md - S["median_s"]), pass_=ok))
pe = all(x["pass_"] for x in EVC)
# (f) 局ごとの「P を測った割合」: 時刻のずれた局は、検測が QC で落ちて測れない側に回り、(c) に入らないことがある
fr = {k: v[1] / v[0] for k, v in seen.items() if v[0] >= MIN_N}
mfr = float(np.median(list(fr.values()))) if fr else 0.0
low = sorted((v, k, seen[k]) for k, v in fr.items() if v < MIN_FRAC_RATIO * mfr)
pf_ = len(fr) > 0 and not low
PASS = bool(pa and pd_ and ps and ph and pe and pf_)
print(f"[24_04d] キャッシュ {cp.name}: 地震 {nev}・P を測った検測 {S['n']}(日は日本時間。キャッシュの UTC に 9 時間を足す)")
print(f"[24_04d] (a) 全体: 残り(P の時刻 − 震源距離/6.0 km/s)の中央値 {S['median_s']:+.3f} s(四分位幅 {S['iqr_s']:.3f} s)  "
      f"基準 |中央値| ≤ {TOL_ALL} s  {'PASS' if pa else 'FAIL'}")
print(f"[24_04d] (b) 日ごと(検測 {MIN_N} 以上の日): 全体の中央値からの最大のずれ {S['max_day_dev_s']:.3f} s  基準 ≤ {TOL_DAY} s  "
      f"{'PASS' if pd_ else 'FAIL'}")
for d, v in S["by_day"].items():
    print(f"      {d}: 検測 {v['n']:5d}  中央値 {v['median']:+.3f} s" + ("" if v["n"] >= MIN_N else "(少ないので判定に使わない)"))
print(f"[24_04d] (c) 局ごと(検測 {MIN_N} 以上の局): 全体の中央値からの最大のずれ {S['max_station_dev_s']:.3f} s  基準 ≤ {TOL_STA} s  "
      f"{'PASS' if ps else 'FAIL'}")
worst = sorted(((abs(v["median"] - S["median_s"]), s, v) for s, v in S["by_station"].items() if v["n"] >= MIN_N), reverse=True)[:5]
for dv, s, v in worst: print(f"      ずれの大きい局 {s}: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
print(f"[24_04d] (d) 時間ごと(日本時間の 1 時間・検測 {MIN_N} 以上、{S['n_hours']} 時間): 全体の中央値からの最大のずれ {S['max_hour_dev_s']:.3f} s  "
      f"基準 ≤ {TOL_HOUR} s  {'PASS' if ph else 'FAIL'}")
worst_h = sorted(((abs(v["median"] - S["median_s"]), k, v) for k, v in S["by_hour"].items() if v["n"] >= MIN_N), reverse=True)[:5]
for dv, k, v in worst_h: print(f"      ずれの大きい時間 {k} 時台: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
print(f"[24_04d] (e) 24_02 の G-clock の地震(P を測った検測 {MIN_EV} 以上、|地震の中央値 − 全体の中央値| ≤ {TOL_EV} s): {'PASS' if pe else 'FAIL'}")
for x in EVC:
    ms = "—" if x["median_s"] is None else f"{x['median_s']:+.3f}"
    print(f"      {x['origin_jst']} Mj {x['mj']}: 検測 {x['n_picks']}  中央値 {ms} s  "
          f"(STA/LTA の G-clock は {x['gclock_stalta_median_abs_s']:.2f} s)  {'PASS' if x['pass_'] else 'FAIL'}")
print(f"[24_04d] (f) 局ごとの P を測った割合(現れた数 {MIN_N} 以上の {len(fr)} 局): 中央値 {mfr:.3f}、その {MIN_FRAC_RATIO} 倍未満の局 {len(low)}  "
      f"{'PASS' if pf_ else 'FAIL'}")
for v, k, c in low: print(f"      割合の低い局 {k}: 現れた {c[0]}・測った {c[1]}(割合 {v:.3f})")
REF = None
if a.ref_cache and Path(a.ref_cache).exists():
    _, r2, d2, s2, h2, _, _ = residuals(Path(a.ref_cache)); REF = summarise(r2, d2, s2, h2)
    print(f"[24_04d] 参考(鳥取 2026、判定には使わない): 検測 {REF['n']}  中央値 {REF['median_s']:+.3f} s  日ごとの最大のずれ "
          f"{REF['max_day_dev_s']:.3f} s  局ごとの最大のずれ {REF['max_station_dev_s']:.3f} s  時間ごとの最大のずれ {REF['max_hour_dev_s']:.3f} s")
print(f"[24_04d] G-clock2: {'PASS' if PASS else 'FAIL'}")
(BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
json.dump(dict(script="24_04d_nagano2014_gclock2_picks.py", version="v1", cache=str(cp), n_events=nev, vp_kms=VP,
               rule=dict(tol_all_s=TOL_ALL, tol_day_s=TOL_DAY, tol_station_s=TOL_STA, tol_hour_s=TOL_HOUR, tol_event_s=TOL_EV,
                         min_n=MIN_N, min_event_picks=MIN_EV, min_frac_ratio=MIN_FRAC_RATIO, day_and_hour="JST (cache UTC + 9 h)"),
               result={k: v for k, v in S.items() if k != "by_hour"}, by_hour=S["by_hour"], gclock_events=EVC,
               station_measured_frac=dict(median=mfr, low=[dict(station=k, appeared=c[0], measured=c[1], frac=v) for v, k, c in low]),
               pass_all=bool(pa), pass_day=bool(pd_), pass_station=bool(ps), pass_hour=bool(ph), pass_events=bool(pe),
               pass_measured_frac=bool(pf_), gclock2_pass=PASS, reference_2026=REF),
          open(BASE / "data" / "24_04d_gclock2.json", "w"), indent=1)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
fig, axs = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw=dict(width_ratios=[1.6, 1.0]))
ax = axs[0]; dk = [d for d, v in S["by_day"].items() if v["n"] >= MIN_N]
ax.plot(range(len(dk)), [S["by_day"][d]["median"] for d in dk], "o-", color="tab:blue", label="Daily median residual")
ax.axhline(S["median_s"], color="k", lw=1, label="Median of all picks")
ax.fill_between([-0.5, len(dk) - 0.5], S["median_s"] - TOL_DAY, S["median_s"] + TOL_DAY, color="tab:green", alpha=0.15,
                label=f"Allowed daily deviation (+/- {TOL_DAY} s)")
ax.set_xticks(range(len(dk))); ax.set_xticklabels([d[5:] for d in dk], rotation=60, fontsize=7); ax.set_xlim(-0.5, len(dk) - 0.5)
ax.set_xlabel("JST date (2014)"); ax.set_ylabel("PhaseNet P time - distance / 6.0 km/s (s)")
ax.set_title(f"(a) Northern Nagano 2014, {S['n']} P picks: daily medians", fontsize=9); ax.grid(alpha=0.3)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False, fontsize=8)
ax = axs[1]; sv = [v for v in S["by_station"].values() if v["n"] >= MIN_N]
ax.hist([v["median"] - S["median_s"] for v in sv], bins=20, color="tab:blue", alpha=0.7)
ax.axvline(-TOL_STA, color="tab:red", ls="--"); ax.axvline(TOL_STA, color="tab:red", ls="--", label=f"Allowed (+/- {TOL_STA} s)")
ax.set_xlabel("Station median - median of all picks (s)"); ax.set_ylabel("Number of stations")
ax.set_title(f"(b) Station medians ({len(sv)} stations). G-clock2: {'PASS' if PASS else 'FAIL'}", fontsize=9); ax.grid(alpha=0.3)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(BASE / "PDF" / "24_04d_gclock2.pdf", bbox_inches="tight"); plt.close(fig)
print(f"[24_04d] 出力: {BASE / 'data' / '24_04d_gclock2.json'}、{BASE / 'PDF' / '24_04d_gclock2.pdf'}")
if not PASS: sys.exit("[24_04d] STOP(G-clock2): 時刻のずれの疑い。どの条件の FAIL かで、事前登録 24 の 5.3 節の扱いに従う(この出力を貼る)")
