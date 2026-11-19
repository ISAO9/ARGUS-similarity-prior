#!/usr/bin/env python3
# =============================================================================
# Script : 25_04d_shimane2018_gclock2_picks.py  (v1)
#          [G-clock2: 25_03h の後のキャッシュの PhaseNet の P の検測(全ての地震・全ての局)を使って、島根県西部 2018 の波形の
#           時刻がずれていないかを確かめる。規則 (a)〜(c)・(e)・(f) と閾値は 24_04d v1(= 21_04d v1・21_20d v1)と同じ。
#           (d) だけを、事前登録 25 の前の dev(25_04x・25_04y・25_04z・25_04v)で決めた「本震 + 72 h より後の続いた 5 地震」に替えた]
# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の入力の確かめ
# 派生元 : 24_04d_nagano2014_gclock2_picks.py v1(SHA-256 42f783bba5ca666847b4582edf3d4a554cecce288c1b2aa112f682bdbaa95f93。事前登録 24 で凍結)。
#          (a)・(b)・(c)・(e)・(f) の計算・閾値と、残りの定義は 24_04d v1 と 1 字も変えていない。変えたのは次だけ(DIFF_LOG_25.md):
#          (1) (d) を替えた(下の「新しい (d)」)。元の (d)(日本時間の 1 時間ごと)は記述として計算して表示・JSON に残すが、判定には使わない。
#              JSON の pass_hour は無くし、新しい (d) の合否を pass_block に書く(元の (d) の値は hourly_descriptive)
#          (2) 止める条件の「検測 20 以上の時間が 0」を外した(1 時間ごとは判定に使わないため)。新しい (d) で判定する窓が 0 の時は、
#              (d) を FAIL とする(止める条件ではなく、JSON を書いてから exit code 1)
#          (3) 新しい (d) の作りの試験(selftest。7 例)を足し、毎回最初に回す。--selftest で試験だけを回せる(その時 --base は要らない)
#          (4) 既定のキャッシュ(..._shimane2018_m15_r1.pt = 25_03h の出力)と報告(data/25_02_report.json)の場所、表示の [25_04d]、
#              出力の名前(data/25_04d_gclock2.json・PDF/25_04d_gclock2.pdf)、JSON の script、図の題と軸の年、図に (d) の窓の値の枠を足した
#          FAIL の時の扱いは、事前登録 25 の 5.3 節(24 の 5.3 節と同じ: (a)・(b)・(d)・(e)・(f) のどれかの FAIL で止める。
#          (c) は 25_04e の表で 80 km 以内(止める)と 80 km より遠い(止めずに印を付ける)に分ける)。
#
# なぜ (d) を替えたか(事前登録 25 の 4 節の表 4):
#   長野県北部 2014(事前登録 24)では、元の (d) が、地震が 1 つしかない 1 時間(2014-12-01 07 時台、0.672 s)で FAIL して止まった。
#   その 1 地震の検測の質や気象庁の発生時刻の誤差でも外れるので、時計のずれと見分けられない。島根は 25_00 で、本震 + 72 h より後の
#   65 時間のうち 54 時間が Mj ≥ 1.5 の地震 1 つだけだった(同じことが起きやすい)。そこで、既に結果の出た 4 系列のキャッシュ
#   (長野 2014・鳥取県西部 2026・大阪 2018・鳥取県中部 2016)だけで作りを試し(島根は開いていない)、次の形に決めた。
#
# 新しい (d)(25_04v v1、SHA-256 6330e5dc6da580ff37efc266110caa7fdbf90e1af6c197fcbb61e4d7e80d21dc の形と同じ計算):
#   0. 見る地震: 本震(キャッシュで Mj 最大)の発生から 72 h より後(ちょうど 72 h は含めない)の地震で、P を測った検測があるもの。
#      日本時間(キャッシュの UTC を秒で切って 9 時間を足す。下の jst)で比べる。試験の候補を取る期間と同じ。
#   1. 残り r は (a)〜(c) と同じ(P の時刻 − 震源距離 / 6.0 km/s。PhaseNet の P、p_fallback = 0)。0 の地震の全ての検測の中央値を M とする。
#   2. 0 の地震を発生時刻の順(同じ時刻はキャッシュの並び順)に並べ、続いた 5 地震ごと(1 つずつずらす)に、地震ごとの検測の
#      中央値を出し、その 5 つの中央値の中央値 − M を出す。5 地震の検測が合わせて 20 以上の窓だけを判定する。
#   3. 判定した全ての窓で |値| ≤ 0.5 s なら合格。判定した窓が 1 つも無ければ合格としない。
#   dev の結果(25_04v、4 系列とも合格): 元のキャッシュの最大 0.068〜0.177 s、1 地震の全ての局に ±1・±3・±10 s を足した時に
#   FAIL になった割合 0.000〜0.008、続いた 4 地震の全ての局に +1.0 s を足した時に見つけた割合 0.998〜1.000(+0.8 s では 0.998〜1.000)。
#   限界: 区切り(約 2 時間)に地震が 1〜2 つしかない時の組み立ての誤りは見えない。本震 + 72 h までの地震の時刻は (d) では見ない。
#
# 何をするか(24_04d と同じ。(d) だけ上のとおり):
#   1. キャッシュの全ての地震・全ての局のうち、PhaseNet で P を測った検測(p_fallback = 0)について、残り r = tp_times − dist_km / 6.0 s を出す。
#   2. (a) |全体の中央値| ≤ 1.5 s (b) 日ごと ≤ 0.5 s (c) 局ごと ≤ 1.0 s (d) 上の新しい (d) ≤ 0.5 s
#      (e) 25_02 の報告の G-clock の地震がそれぞれ ≤ 0.5 s(検測 4 以上) (f) 局ごとの P を測った割合が全局の中央値の 0.5 倍以上。
#      (b)・(c) は検測 20 以上の日・局で数える。日は日本時間。
#   3. 参考(判定には使わない): --ref-cache に鳥取 2026 のキャッシュ。元の (d)(1 時間ごと)も参考に出す。
#   4. 出力: data/25_04d_gclock2.json / PDF/25_04d_gclock2.pdf。FAIL なら exit code 1。
#
# Usage(Colab、25_03h の後に。ノート 25_shimane2018_colab.ipynb の セル N13):
#   !python /content/drive/MyDrive/ARGUS/src/25_04d_shimane2018_gclock2_picks.py --base /content/ARGUS_shimane2018 \
#       --ref-cache /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt
#   試験だけ: !python .../25_04d_shimane2018_gclock2_picks.py --selftest
# 止める条件(STOP): キャッシュが無い・P を測った検測が 100 未満・検測 20 以上の日・局のどれかが 0・25_02 の報告が無い・selftest の失敗
# =============================================================================
import sys, json, argparse
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import torch

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="", help="ARGUS_shimane2018 の場所(Colab のローカルなら /content/ARGUS_shimane2018。--selftest の時は要らない)")
ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt")
ap.add_argument("--ref-cache", default="", help="参考: 鳥取 2026 のキャッシュ(無くてよい)")
ap.add_argument("--report", default="data/25_02_report.json", help="25_02 の報告(G-clock の地震を読む。--base からの場所)")
ap.add_argument("--selftest", action="store_true", help="25: 新しい (d) の作りの試験だけを回す")
a = ap.parse_args()
VP, TOL_ALL, TOL_DAY, TOL_STA, MIN_N = 6.0, 1.5, 0.5, 1.0, 20
TOL_HOUR, TOL_EV, MIN_EV, MIN_FRAC_RATIO = 0.5, 0.5, 4, 0.5
K_BLOCK, POOL_H = 5, 72.0                                        # 25: 新しい (d)(25_04v と同じ。閾値は TOL_HOUR = 0.5 s のまま)
if not a.selftest and not a.base: sys.exit("[25_04d] STOP: --base を渡す")
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

def block_events(EVS, r, evi):
    """25: 新しい (d) の地震。本震(Mj 最大)+ 72 h より後で P を測った地震の (日本時間, 番号, 残り) を時刻の順に。本震の日本時間も返す"""
    im = int(np.argmax([float(e["mw"]) for e in EVS])); t_main = jst(EVS[im]["origin_time"])
    out = []
    for ie, e in enumerate(EVS):
        t = jst(e["origin_time"])
        if (t - t_main).total_seconds() <= POOL_H * 3600: continue
        rr = r[evi == ie]
        if rr.size: out.append((t, ie, rr))
    out.sort(key=lambda x: (x[0], x[1]))
    return out, t_main, im

def block_d(evs):
    """25: 続いた K_BLOCK 地震ごとの(地震ごとの中央値の中央値 − M)。検測が合わせて MIN_N 未満の窓は判定しない"""
    if not evs: return dict(n_events=0, n_picks=0, median_s=None, n_windows=0, max_abs_s=None, worst_value_s=None,
                            worst_window_start_jst=None, worst_window_end_jst=None, windows=[], pass_=False)
    M = float(np.median(np.concatenate([x[2] for x in evs])))
    W, mx, at = [], None, None
    for j in range(0, len(evs) - K_BLOCK + 1):
        rs = [evs[j + i][2] for i in range(K_BLOCK)]
        if sum(len(x) for x in rs) < MIN_N: continue
        v = float(np.median([np.median(x) for x in rs])) - M
        W.append(dict(start_jst=f"{evs[j][0]:%Y-%m-%d %H:%M:%S}", end_jst=f"{evs[j + K_BLOCK - 1][0]:%Y-%m-%d %H:%M:%S}",
                      n_picks=int(sum(len(x) for x in rs)), value_s=v))
        if mx is None or abs(v) > abs(mx): mx, at = v, len(W) - 1
    return dict(n_events=len(evs), n_picks=int(sum(len(x[2]) for x in evs)), median_s=M, n_windows=len(W),
                max_abs_s=(None if mx is None else abs(mx)), worst_value_s=mx,
                worst_window_start_jst=(None if at is None else W[at]["start_jst"]), worst_window_end_jst=(None if at is None else W[at]["end_jst"]),
                windows=W, pass_=bool(W and abs(mx) <= TOL_HOUR))

def selftest():
    """25: 新しい (d) の作りの試験(25_04v の試験のうち、この計算に当てはまるもの)"""
    def check(c, m):
        if not c: sys.exit(f"[25_04d] STOP: selftest に失敗: {m}")
    rng = np.random.default_rng(1); t0 = datetime(2018, 4, 12, 3)
    evs = [(t0 + timedelta(minutes=40 * j), j, 0.3 + rng.normal(0, 0.15, 24)) for j in range(60)]
    sh = lambda S, ds: [(t, ie, rr + ds if ie in S else rr) for t, ie, rr in evs]
    check(block_d(evs)["pass_"] and block_d(evs)["n_windows"] == 56, "正常は合格(窓 56)")
    check(block_d(sh({30}, 10.0))["pass_"], "1 地震の全局 +10 s は合格")
    check(block_d(sh({30, 32}, 3.0))["pass_"], "5 つのうち 2 地震の外れは合格")
    check(not block_d(sh({30, 31, 32, 33}, 1.0))["pass_"], "続いた 4 地震の全局 +1.0 s は不合格")
    check(not block_d([(t, ie, rr[:3]) for t, ie, rr in evs])["pass_"] and block_d([(t, ie, rr[:3]) for t, ie, rr in evs])["n_windows"] == 0,
          "検測 20 未満の窓しか無ければ判定する窓 0 で合格としない")
    check(not block_d([])["pass_"], "地震が無ければ合格としない")
    EVm = [dict(origin_time="2018-04-08 16:32:30.8", mw=6.1)] + [dict(origin_time=f"2018-04-11 16:{m:02d}:30.8", mw=1.6) for m in (32, 33)]
    rr = np.array([0.1, 0.2, 0.3]); ev_, tm_, im_ = block_events(EVm, rr, np.array([0, 1, 2]))
    check(im_ == 0 and tm_ == datetime(2018, 4, 9, 1, 32, 30) and [x[1] for x in ev_] == [2], "本震 + 72 h の切り方(ちょうど 72 h は除く)と日本時間")
    print("[25_04d] selftest: 新しい (d)(正常・1 地震の外れ・2 地震の外れ・続いた 4 地震 +1.0 s・検測 20 未満・地震なし・72 h の切り方)の 7 例に合格")

selftest()
if a.selftest: sys.exit(0)

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
if not cp.exists(): sys.exit(f"[25_04d] STOP: キャッシュ {cp} が無い(25_03h の後に回す)")
EVS, r, day, sta, hour, evi, seen = residuals(cp); nev = len(EVS)
if len(r) < 100: sys.exit(f"[25_04d] STOP: P を測った検測が {len(r)}(100 未満)")
S = summarise(r, day, sta, hour)
if S["n_days"] == 0 or S["n_stations"] == 0:
    sys.exit(f"[25_04d] STOP: 検測 {MIN_N} 以上の日・局のどれかが 0(判定できない)")
pa = abs(S["median_s"]) <= TOL_ALL; pd_ = S["max_day_dev_s"] <= TOL_DAY; ps = S["max_station_dev_s"] <= TOL_STA
BEV, T_MAIN, IM = block_events(EVS, r, evi); B = block_d(BEV)       # 25: 新しい (d)
pb = B["pass_"]
# (e) 25_02 の G-clock の地震: その地震の P を測った検測(MIN_EV 以上)の中央値 − 全体の中央値
rp = BASE / a.report
if not rp.exists(): sys.exit(f"[25_04d] STOP: 25_02 の報告 {rp} が無い")
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
PASS = bool(pa and pd_ and ps and pb and pe and pf_)
print(f"[25_04d] キャッシュ {cp.name}: 地震 {nev}・P を測った検測 {S['n']}(日は日本時間。キャッシュの UTC に 9 時間を足す)")
print(f"[25_04d] (a) 全体: 残り(P の時刻 − 震源距離/6.0 km/s)の中央値 {S['median_s']:+.3f} s(四分位幅 {S['iqr_s']:.3f} s)  "
      f"基準 |中央値| ≤ {TOL_ALL} s  {'PASS' if pa else 'FAIL'}")
print(f"[25_04d] (b) 日ごと(検測 {MIN_N} 以上の日): 全体の中央値からの最大のずれ {S['max_day_dev_s']:.3f} s  基準 ≤ {TOL_DAY} s  "
      f"{'PASS' if pd_ else 'FAIL'}")
for d, v in S["by_day"].items():
    print(f"      {d}: 検測 {v['n']:5d}  中央値 {v['median']:+.3f} s" + ("" if v["n"] >= MIN_N else "(少ないので判定に使わない)"))
print(f"[25_04d] (c) 局ごと(検測 {MIN_N} 以上の局): 全体の中央値からの最大のずれ {S['max_station_dev_s']:.3f} s  基準 ≤ {TOL_STA} s  "
      f"{'PASS' if ps else 'FAIL'}")
worst = sorted(((abs(v["median"] - S["median_s"]), s, v) for s, v in S["by_station"].items() if v["n"] >= MIN_N), reverse=True)[:5]
for dv, s, v in worst: print(f"      ずれの大きい局 {s}: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
_f = lambda x: "—" if x is None else f"{x:.3f}"
print(f"[25_04d] (d) 続いた {K_BLOCK} 地震(本震 {T_MAIN:%Y-%m-%d %H:%M:%S} JST・Mj {float(EVS[IM]['mw']):.1f} + {POOL_H:g} h より後の {B['n_events']} 地震・"
      f"検測 {B['n_picks']}、その中央値 M {('—' if B['median_s'] is None else format(B['median_s'], '+.3f'))} s、検測 {MIN_N} 以上の窓 {B['n_windows']}): "
      f"最大 |地震ごとの中央値の中央値 − M| {_f(B['max_abs_s'])} s(窓 {B['worst_window_start_jst']} 〜 {B['worst_window_end_jst']})  "
      f"基準 ≤ {TOL_HOUR} s・判定する窓 1 以上  {'PASS' if pb else 'FAIL'}")
worst_b = sorted(B["windows"], key=lambda w: -abs(w["value_s"]))[:5]
for w in worst_b: print(f"      ずれの大きい窓 {w['start_jst']} 〜 {w['end_jst']}: 検測 {w['n_picks']}  値 {w['value_s']:+.3f} s")
print(f"[25_04d] 参考(元の (d)、判定には使わない): 日本時間の 1 時間ごと(検測 {MIN_N} 以上、{S['n_hours']} 時間): 全体の中央値からの最大のずれ "
      f"{_f(S['max_hour_dev_s'])} s")
print(f"[25_04d] (e) 25_02 の G-clock の地震(P を測った検測 {MIN_EV} 以上、|地震の中央値 − 全体の中央値| ≤ {TOL_EV} s): {'PASS' if pe else 'FAIL'}")
for x in EVC:
    ms = "—" if x["median_s"] is None else f"{x['median_s']:+.3f}"
    print(f"      {x['origin_jst']} Mj {x['mj']}: 検測 {x['n_picks']}  中央値 {ms} s  "
          f"(STA/LTA の G-clock は {x['gclock_stalta_median_abs_s']:.2f} s)  {'PASS' if x['pass_'] else 'FAIL'}")
print(f"[25_04d] (f) 局ごとの P を測った割合(現れた数 {MIN_N} 以上の {len(fr)} 局): 中央値 {mfr:.3f}、その {MIN_FRAC_RATIO} 倍未満の局 {len(low)}  "
      f"{'PASS' if pf_ else 'FAIL'}")
for v, k, c in low: print(f"      割合の低い局 {k}: 現れた {c[0]}・測った {c[1]}(割合 {v:.3f})")
REF = None
if a.ref_cache and Path(a.ref_cache).exists():
    _, r2, d2, s2, h2, _, _ = residuals(Path(a.ref_cache)); REF = summarise(r2, d2, s2, h2)
    print(f"[25_04d] 参考(鳥取 2026、判定には使わない): 検測 {REF['n']}  中央値 {REF['median_s']:+.3f} s  日ごとの最大のずれ "
          f"{REF['max_day_dev_s']:.3f} s  局ごとの最大のずれ {REF['max_station_dev_s']:.3f} s  時間ごとの最大のずれ {_f(REF['max_hour_dev_s'])} s")
print(f"[25_04d] G-clock2: {'PASS' if PASS else 'FAIL'}")
(BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
json.dump(dict(script="25_04d_shimane2018_gclock2_picks.py", version="v1", cache=str(cp), n_events=nev, vp_kms=VP,
               rule=dict(tol_all_s=TOL_ALL, tol_day_s=TOL_DAY, tol_station_s=TOL_STA, tol_block_s=TOL_HOUR, tol_event_s=TOL_EV,
                         min_n=MIN_N, min_event_picks=MIN_EV, min_frac_ratio=MIN_FRAC_RATIO, day_and_hour="JST (cache UTC + 9 h)",
                         block=dict(k_events=K_BLOCK, after_mainshock_h=POOL_H, value="median of per-event medians minus the median M of all picks of these events",
                                    min_picks_per_window=MIN_N, pass_rule="all judged windows within tol_block_s and at least one judged window",
                                    dev_script="25_04v_gclock2_k5_dev.py v1 (SHA-256 6330e5dc6da580ff37efc266110caa7fdbf90e1af6c197fcbb61e4d7e80d21dc)")),
               result={k: v for k, v in S.items() if k not in ("by_hour", "max_hour_dev_s", "n_hours")},
               event_block_d={k: v for k, v in B.items() if k != "pass_"}, mainshock_jst=f"{T_MAIN:%Y-%m-%d %H:%M:%S}",
               hourly_descriptive=dict(max_hour_dev_s=S["max_hour_dev_s"], n_hours=S["n_hours"], by_hour=S["by_hour"], note="original (d) of 24_04d; not used for the verdict"),
               gclock_events=EVC,
               station_measured_frac=dict(median=mfr, low=[dict(station=k, appeared=c[0], measured=c[1], frac=v) for v, k, c in low]),
               pass_all=bool(pa), pass_day=bool(pd_), pass_station=bool(ps), pass_block=bool(pb), pass_events=bool(pe),
               pass_measured_frac=bool(pf_), gclock2_pass=PASS, reference_2026=REF),
          open(BASE / "data" / "25_04d_gclock2.json", "w"), indent=1)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
fig, axs = plt.subplots(1, 3, figsize=(17, 4.4), gridspec_kw=dict(width_ratios=[1.6, 1.0, 1.6]))
ax = axs[0]; dk = [d for d, v in S["by_day"].items() if v["n"] >= MIN_N]
ax.plot(range(len(dk)), [S["by_day"][d]["median"] for d in dk], "o-", color="tab:blue", label="Daily median residual")
ax.axhline(S["median_s"], color="k", lw=1, label="Median of all picks")
ax.fill_between([-0.5, len(dk) - 0.5], S["median_s"] - TOL_DAY, S["median_s"] + TOL_DAY, color="tab:green", alpha=0.15,
                label=f"Allowed daily deviation (+/- {TOL_DAY} s)")
ax.set_xticks(range(len(dk))); ax.set_xticklabels([d[5:] for d in dk], rotation=60, fontsize=7); ax.set_xlim(-0.5, len(dk) - 0.5)
ax.set_xlabel("JST date (2018)"); ax.set_ylabel("PhaseNet P time - distance / 6.0 km/s (s)")
ax.set_title(f"(a) Western Shimane 2018, {S['n']} P picks: daily medians", fontsize=9); ax.grid(alpha=0.3)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False, fontsize=8)
ax = axs[1]; sv = [v for v in S["by_station"].values() if v["n"] >= MIN_N]
ax.hist([v["median"] - S["median_s"] for v in sv], bins=20, color="tab:blue", alpha=0.7)
ax.axvline(-TOL_STA, color="tab:red", ls="--"); ax.axvline(TOL_STA, color="tab:red", ls="--", label=f"Allowed (+/- {TOL_STA} s)")
ax.set_xlabel("Station median - median of all picks (s)"); ax.set_ylabel("Number of stations")
ax.set_title(f"(b) Station medians ({len(sv)} stations). G-clock2: {'PASS' if PASS else 'FAIL'}", fontsize=9); ax.grid(alpha=0.3)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), frameon=False, fontsize=8)
ax = axs[2]                                                      # 25: 新しい (d) の窓の値
if B["windows"]:
    tw = [(datetime.strptime(w["start_jst"], "%Y-%m-%d %H:%M:%S") - T_MAIN).total_seconds() / 86400 for w in B["windows"]]
    ax.plot(tw, [w["value_s"] for w in B["windows"]], "o", ms=3, color="tab:blue", label=f"{K_BLOCK}-event window value")
ax.axhspan(-TOL_HOUR, TOL_HOUR, color="tab:green", alpha=0.15, label=f"Allowed (+/- {TOL_HOUR} s)")
ax.axhline(0, color="k", lw=0.8)
ax.set_xlabel(f"Window start, days since mainshock ({T_MAIN:%Y-%m-%d %H:%M} JST)"); ax.set_ylabel("Median of event medians - M (s)")
ax.set_title(f"(c) Condition (d): {K_BLOCK} consecutive events after mainshock + {POOL_H:g} h, {B['n_windows']} windows: {'PASS' if pb else 'FAIL'}", fontsize=9)
ax.grid(alpha=0.3); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(BASE / "PDF" / "25_04d_gclock2.pdf", bbox_inches="tight"); plt.close(fig)
print(f"[25_04d] 出力: {BASE / 'data' / '25_04d_gclock2.json'}、{BASE / 'PDF' / '25_04d_gclock2.pdf'}")
if not PASS: sys.exit("[25_04d] STOP(G-clock2): 時刻のずれの疑い。どの条件の FAIL かで、事前登録 25 の 5.3 節の扱いに従う(この出力を貼る)")
