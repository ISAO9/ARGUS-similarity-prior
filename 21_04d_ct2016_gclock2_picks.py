#!/usr/bin/env python3
# =============================================================================
# Script : 21_04d_ct2016_gclock2_picks.py  (v1)
#          [G-clock2: 15_01c が作ったキャッシュの PhaseNet の P の検測(全ての地震・全ての局)を使って、鳥取県中部 2016 の波形の
#           時刻がずれていないかを確かめる。事前登録の変更の記録 02 で決めたゲートで、キャッシュを見る前に規則を固定する]
# Project: ARGUS(新生)— 2 つ目の余震系列での確認(21_04)の入力の確かめ
#
# なぜ必要か:
#   21_04b の G-clock(STA/LTA の立ち上がり)は、本震・10-29 Mj 4.5・10-21 22:53 Mj 3.8 で通り、10-21 22:03 Mj 3.9 だけ 2.79 s で
#   FAIL だった。21_04c で調べると、FAIL の地震では立ち上がりが予想の P より早い(符号付きの中央値 −2.79 s、8 局中 6 局が予想の P より
#   1 s 以上早い)。波形の P の始まりは予想の P の位置にそろっていて、前の数十秒に気象庁の小さな地震(Mj 0.7 など)があった。
#   つまり、余震の多い時間帯に STA/LTA が P より前の小さな揺れで立ち上がった形で、時刻のずれの形(全ての局で同じ向き・同じ量の
#   ずれ)ではない。ただし、図を見て判断するだけでは足りないので、数千の検測を使う、STA/LTA に依らない時刻の確かめを足す。
#
# 何をするか(G-clock2。規則は変更の記録 02 に書いたもので、このスクリプトはそれをそのまま計算する):
#   1. キャッシュ(既定 data/tottori_processed/tottori_parsed_realpick_ct2016_m15.pt)の全ての地震・全ての局のうち、PhaseNet で
#      P を測った検測(p_fallback = 0)について、残り r = tp_times − dist_km / 6.0 s を出す
#      (tp_times は 15_01c が書いた「P の時刻 − 気象庁の発生時刻」、dist_km は震源距離。6.0 km/s は G-clock と同じ)。
#   2. 合格の条件(全て満たせば PASS。日と時間は日本時間。キャッシュの origin_time は UTC なので 9 時間を足す):
#      (a) 全体の中央値 |median(r)| ≤ 1.5 s(G-clock と同じ許容)
#      (b) 日ごと(検測 20 以上の日): |その日の中央値 − 全体の中央値| ≤ 0.5 s
#      (c) 局ごと(検測 20 以上の局。局は座標で見分ける): |その局の中央値 − 全体の中央値| ≤ 1.0 s(局の下の構造・距離・一定の速度の誤差が
#          混ざるので日ごとより広くした。事前に決めた値で、較正はしていない)
#      (d) 時間ごと(日本時間の 1 時間、検測 20 以上): |その時間の中央値 − 全体の中央値| ≤ 0.5 s(短い時間だけのずれを見る)
#      (e) 21_04b の報告の G-clock の 4 地震(--report): それぞれ P を測った検測 4 以上で、|その地震の中央値 − 全体の中央値| ≤ 0.5 s
#      (f) 局ごとの P を測った割合(現れた数 20 以上の局): 全ての局で、局の割合の中央値の 0.5 倍以上(時刻のずれた局が QC で落ちて
#          (c) に入らない抜け道をふさぐ)
#      止める: P を測った検測が 100 未満、検測 20 以上の日・局・時間のどれかが 0、21_04b の報告が無い
#   3. 参考(判定には使わない): --ref-cache に鳥取 2026 のキャッシュを渡すと、同じ量を出す(許容が普通の値に比べて妥当かを見るため)。
#   4. 出力: data/21_04d_gclock2.json(数・中央値・日ごと・局ごと・時間ごと・4 地震・測った割合・判定)/ PDF/21_04d_gclock2.pdf(日ごと・局ごとの中央値。白背景・英語・
#      凡例は枠の外)。FAIL なら exit code 1(21_04 には進まない)。
#
# Usage(Colab、15_01c の本番の後に):
#   run([f'{SRC}/21_04d_ct2016_gclock2_picks.py', '--base', LO])
#   (--cache で別のキャッシュ、--ref-cache で鳥取 2026 のキャッシュを指定できる)
# 止める条件(STOP): キャッシュが無い・上の「止める」
# =============================================================================
import sys, json, argparse
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import torch

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True, help="ARGUS_ct2016 の場所(Colab のローカルなら /content/ARGUS_ct2016)")
ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_ct2016_m15.pt")
ap.add_argument("--ref-cache", default="", help="参考: 鳥取 2026 のキャッシュ(無くてよい)")
ap.add_argument("--report", default="data/21_04b_report.json", help="21_04b の報告(G-clock の 4 地震を読む。--base からの場所)")
a = ap.parse_args()
VP, TOL_ALL, TOL_DAY, TOL_STA, MIN_N = 6.0, 1.5, 0.5, 1.0, 20
TOL_HOUR, TOL_EV, MIN_EV, MIN_FRAC_RATIO = 0.5, 0.5, 4, 0.5
BASE = Path(a.base)

def jst(ot):                                                     # キャッシュの origin_time は UTC(15_01c v3.3)。日本時間にする
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
if not cp.exists(): sys.exit(f"[21_04d] STOP: キャッシュ {cp} が無い(15_01c の本番の後に回す)")
EVS, r, day, sta, hour, evi, seen = residuals(cp); nev = len(EVS)
if len(r) < 100: sys.exit(f"[21_04d] STOP: P を測った検測が {len(r)}(100 未満)")
S = summarise(r, day, sta, hour)
if S["n_days"] == 0 or S["n_stations"] == 0 or S["n_hours"] == 0:
    sys.exit(f"[21_04d] STOP: 検測 {MIN_N} 以上の日・局・時間のどれかが 0(判定できない)")
pa = abs(S["median_s"]) <= TOL_ALL; pd_ = S["max_day_dev_s"] <= TOL_DAY; ps = S["max_station_dev_s"] <= TOL_STA
ph = S["max_hour_dev_s"] <= TOL_HOUR
# (e) 21_04b の G-clock の 4 地震: その地震の P を測った検測(MIN_EV 以上)の中央値 − 全体の中央値
rp = BASE / a.report
if not rp.exists(): sys.exit(f"[21_04d] STOP: 21_04b の報告 {rp} が無い")
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
print(f"[21_04d] キャッシュ {cp.name}: 地震 {nev}・P を測った検測 {S['n']}(日は日本時間。キャッシュの UTC に 9 時間を足す)")
print(f"[21_04d] (a) 全体: 残り(P の時刻 − 震源距離/6.0 km/s)の中央値 {S['median_s']:+.3f} s(四分位幅 {S['iqr_s']:.3f} s)  "
      f"基準 |中央値| ≤ {TOL_ALL} s  {'PASS' if pa else 'FAIL'}")
print(f"[21_04d] (b) 日ごと(検測 {MIN_N} 以上の日): 全体の中央値からの最大のずれ {S['max_day_dev_s']:.3f} s  基準 ≤ {TOL_DAY} s  "
      f"{'PASS' if pd_ else 'FAIL'}")
for d, v in S["by_day"].items():
    print(f"      {d}: 検測 {v['n']:5d}  中央値 {v['median']:+.3f} s" + ("" if v["n"] >= MIN_N else "(少ないので判定に使わない)"))
print(f"[21_04d] (c) 局ごと(検測 {MIN_N} 以上の局): 全体の中央値からの最大のずれ {S['max_station_dev_s']:.3f} s  基準 ≤ {TOL_STA} s  "
      f"{'PASS' if ps else 'FAIL'}")
worst = sorted(((abs(v["median"] - S["median_s"]), s, v) for s, v in S["by_station"].items() if v["n"] >= MIN_N), reverse=True)[:5]
for dv, s, v in worst: print(f"      ずれの大きい局 {s}: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
print(f"[21_04d] (d) 時間ごと(日本時間の 1 時間・検測 {MIN_N} 以上、{S['n_hours']} 時間): 全体の中央値からの最大のずれ {S['max_hour_dev_s']:.3f} s  "
      f"基準 ≤ {TOL_HOUR} s  {'PASS' if ph else 'FAIL'}")
worst_h = sorted(((abs(v["median"] - S["median_s"]), k, v) for k, v in S["by_hour"].items() if v["n"] >= MIN_N), reverse=True)[:5]
for dv, k, v in worst_h: print(f"      ずれの大きい時間 {k} 時台: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
print(f"[21_04d] (e) 21_04b の G-clock の 4 地震(P を測った検測 {MIN_EV} 以上、|地震の中央値 − 全体の中央値| ≤ {TOL_EV} s): {'PASS' if pe else 'FAIL'}")
for x in EVC:
    ms = "—" if x["median_s"] is None else f"{x['median_s']:+.3f}"
    print(f"      {x['origin_jst']} Mj {x['mj']}: 検測 {x['n_picks']}  中央値 {ms} s  "
          f"(STA/LTA の G-clock は {x['gclock_stalta_median_abs_s']:.2f} s)  {'PASS' if x['pass_'] else 'FAIL'}")
print(f"[21_04d] (f) 局ごとの P を測った割合(現れた数 {MIN_N} 以上の {len(fr)} 局): 中央値 {mfr:.3f}、その {MIN_FRAC_RATIO} 倍未満の局 {len(low)}  "
      f"{'PASS' if pf_ else 'FAIL'}")
for v, k, c in low: print(f"      割合の低い局 {k}: 現れた {c[0]}・測った {c[1]}(割合 {v:.3f})")
REF = None
if a.ref_cache and Path(a.ref_cache).exists():
    _, r2, d2, s2, h2, _, _ = residuals(Path(a.ref_cache)); REF = summarise(r2, d2, s2, h2)
    print(f"[21_04d] 参考(鳥取 2026、判定には使わない): 検測 {REF['n']}  中央値 {REF['median_s']:+.3f} s  日ごとの最大のずれ "
          f"{REF['max_day_dev_s']:.3f} s  局ごとの最大のずれ {REF['max_station_dev_s']:.3f} s  時間ごとの最大のずれ {REF['max_hour_dev_s']:.3f} s")
print(f"[21_04d] G-clock2: {'PASS' if PASS else 'FAIL'}")
(BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
json.dump(dict(script="21_04d_ct2016_gclock2_picks.py", version="v1", cache=str(cp), n_events=nev, vp_kms=VP,
               rule=dict(tol_all_s=TOL_ALL, tol_day_s=TOL_DAY, tol_station_s=TOL_STA, tol_hour_s=TOL_HOUR, tol_event_s=TOL_EV,
                         min_n=MIN_N, min_event_picks=MIN_EV, min_frac_ratio=MIN_FRAC_RATIO, day_and_hour="JST (cache UTC + 9 h)"),
               result={k: v for k, v in S.items() if k != "by_hour"}, by_hour=S["by_hour"], gclock_events=EVC,
               station_measured_frac=dict(median=mfr, low=[dict(station=k, appeared=c[0], measured=c[1], frac=v) for v, k, c in low]),
               pass_all=bool(pa), pass_day=bool(pd_), pass_station=bool(ps), pass_hour=bool(ph), pass_events=bool(pe),
               pass_measured_frac=bool(pf_), gclock2_pass=PASS, reference_2026=REF),
          open(BASE / "data" / "21_04d_gclock2.json", "w"), indent=1)

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
ax.set_xlabel("JST date (2016)"); ax.set_ylabel("PhaseNet P time - distance / 6.0 km/s (s)")
ax.set_title(f"(a) Central Tottori 2016, {S['n']} P picks: daily medians", fontsize=9); ax.grid(alpha=0.3)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False, fontsize=8)
ax = axs[1]; sv = [v for v in S["by_station"].values() if v["n"] >= MIN_N]
ax.hist([v["median"] - S["median_s"] for v in sv], bins=20, color="tab:blue", alpha=0.7)
ax.axvline(-TOL_STA, color="tab:red", ls="--"); ax.axvline(TOL_STA, color="tab:red", ls="--", label=f"Allowed (+/- {TOL_STA} s)")
ax.set_xlabel("Station median - median of all picks (s)"); ax.set_ylabel("Number of stations")
ax.set_title(f"(b) Station medians ({len(sv)} stations). G-clock2: {'PASS' if PASS else 'FAIL'}", fontsize=9); ax.grid(alpha=0.3)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(BASE / "PDF" / "21_04d_gclock2.pdf", bbox_inches="tight"); plt.close(fig)
print(f"[21_04d] 出力: {BASE / 'data' / '21_04d_gclock2.json'}、{BASE / 'PDF' / '21_04d_gclock2.pdf'}")
if not PASS: sys.exit("[21_04d] STOP(G-clock2): 時刻のずれの疑い。21_04 には進まない(この出力を貼って相談)")
