#!/usr/bin/env python3
# =============================================================================
# Script : 25_04x_gclock2_station_window_dev.py  (v1)
#          [事前登録 25(島根県西部 2018)の G-clock2 で、条件 (d)「1 時間ごと」の代わりに使う「局ごとの時計の確かめ」を、
#           既に試験を終えた(または止めた)系列のキャッシュで試す dev。島根のデータは一つも読まない。位置の計算はしない]
# Project: ARGUS(新生)— 事前登録 25 の準備(規則を凍結する前の dev)
#
# なぜ必要か:
#   長野県北部 2014(事前登録 24)は、G-clock2 の (d)「日本時間の 1 時間ごとの P の残りの中央値」が、地震が 1 つだけの 1 時間で外れて
#   止まった(24_04g: 遠い局の P が雑音の上で、時計のずれではなかった)。島根県西部 2018 は、25_00 の数え上げで 72 h より後の 65 時間の
#   うち 54 時間が Mj ≥ 1.5 の地震 1 つだけで、同じ形の止まり方がもっと起きやすい。そこで (d) を、時計のずれを直接見る形に作り直す。
#   新しい (d) を島根で使う前に、既に結果の出た系列で、(1) 時計が正常なはずの所で誤って FAIL しないか、(2) わざと入れた時計の
#   ずれを見つけるか、を確かめる。
#
# 新しい (d)(案。この dev の後に事前登録 25 で凍結する):
#   各検測(PhaseNet の P、p_fallback = 0)の残り r = P の時刻 − 震源距離 / 6.0 km/s(24_04d と同じ)。
#   1. 各検測から、同じ地震の「他の局」の検測の中央値を引く(他の局の検測が 4 以上の時だけ): e = r − median_{同じ地震・他の局}(r)。
#      (全ての局に共通のずれ = 発生時刻のずれ・その地震だけの全局の時刻のずれは、ここで消える。物理の方法も地震ごとの中央値を引くので、
#       位置には効かない。自分の局を除くのは、ずれた局の値が地震の中央値に入って、ずれを小さく見せないため)
#   2. 局ごとに、発生時刻の順に並べた e の、続いた W 個(W = 10)の窓を 1 つずつずらし、
#      「窓の中央値 − 同じ局の窓の外の中央値」を出す(局のふだんのずれを、窓の外で測って引く。局の検測の半分近くがずれても、
#      窓の外がずれていない部分なら見える)。
#   3. 検測 20 以上の局(24_04d の (c) と同じ)の全ての窓で、この値の絶対値 ≤ 0.5 s なら合格(閾値は元の (d) と同じ)。
#   考え方: 時計のずれは局ごとに起き、その局の続いた地震に同じだけ乗る。1 地震だけの検測の取り違え(雑音の上の P)は、
#   W = 10 の窓の中央値ではほぼ消える(窓の 10 個のうち 5 個以上が同じ向きに 0.5 s を超えてずれた時だけ外れる)。
#   限界: 全ての局に同時に同じだけ乗る時刻のずれ(網全体の時刻のずれ)と、1 つの地震の局の半分より多くに同時に乗るずれは 1 で消えるので
#   見えない(位置には効かない)。続いた 5〜6 検測より短い時計のずれは見逃しうる(検測の少ない局では、10 検測が数日にわたる)。
#   局の検測の大半(24 個のうち約 20 個以上)に掛かる長いずれは、窓の外もずれるので見えにくく、(c)(局ごと・1.0 s)に任せる
#   (0.5〜1.0 s の長いずれは (c) と (d) の両方で見逃しうる)。速度は一様 6 km/s なので、震源が移ると局の値が少し変わりうる。
#
# この dev でやること(位置の計算・方法の誤差は一切しない。読むのはキャッシュの P の時刻・距離・局の位置・発生時刻だけ):
#   A. --cache で渡した系列ごとに、元の (d)(24_04d と同じ 1 時間ごと)と、新しい (d) を計算して並べる。
#   B. 陽性対照: 判定する全ての局と、続いた 12 検測の全ての始まり(1 つずつ)について、その 12 検測に +0.3・+0.6・+1.0 s を足し、
#      その局の新しい (d) で見つけた割合を出す(+0.6・+1.0 s はほぼ全て見つけ、+0.3 s はほぼ見つけないはず)。
#      自分の局を除いた地震の中央値を使うので、ある局にずれを足しても他の局の値は変わらない(その局だけを計算し直せばよい)。
#   C. 陰性対照: 各系列で、検測の最も多い地震の全ての局に +1.0 s を足す(発生時刻のずれのまね)・同じ地震の遠い半分の局に +1.0 s を足す
#      (長野の 2014-12-01 07:40 のまね)。新しい (d) は PASS のままのはず。
#   期待と違う結果(元のキャッシュで FAIL・陰性対照で FAIL・+0.6 s の見つけた割合 < 0.95)が 1 つでもあれば exit code 1。
#   D. 窓の大きさ W = 6・8・10・12・16 で、A の最大の |窓の中央値| を記述として出す(W を決める材料。判定には W = 10 を使う)。
#
# Usage(Colab。Drive をつなぐだけでよい。セルは 25_04x_COLAB_JA.md の X1〜X3):
#   !python /content/drive/MyDrive/ARGUS/src/25_04x_gclock2_station_window_dev.py \
#       --cache nagano2014=/content/drive/MyDrive/ARGUS_nagano2014/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt \
#       --cache tottori2026=/content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt \
#       --out /content/drive/MyDrive/ARGUS/data/25_04x
#   (無いキャッシュは飛ばして続ける)
# 出力  : <out>/25_04x_gclock2_station_window_dev.json / <out>/25_04x_gclock2_station_window_dev.pdf
# =============================================================================
import sys, json, argparse, hashlib
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

ap = argparse.ArgumentParser(description="25_04x: 新しい G-clock2 (d)(局ごとの時計)の dev。既に結果の出た系列のキャッシュだけを読む")
ap.add_argument("--cache", action="append", default=[], help="名前=キャッシュの場所(.pt)。何度でも")
ap.add_argument("--out", default="", help="出力の置き場所")
ap.add_argument("--selftest", action="store_true")
a = ap.parse_args()
VP, MIN_N, TOL, W, MIN_EV_PICKS = 6.0, 20, 0.5, 10, 4               # MIN_EV_PICKS は「同じ地震の他の局」の検測の数
WS = (6, 8, 10, 12, 16)
TAG = "[25_04x]"

def jst_hour(ot):                                                # 24_04d と同じ: 秒で切って 9 時間を足す
    t = datetime.strptime(str(ot).replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
    return t + timedelta(hours=9)

def picks_from_events(EV):
    """24_04d と同じ残り。戻り値: 検測の辞書の一覧(ev・sta・t(発生時刻の日本時間)・dist・r・hour)"""
    P = []
    for ie, e in enumerate(EV):
        th = jst_hour(e["origin_time"]); n = int(e["n_real_stations"])
        tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
        loc = np.asarray(e["sta_locs"], float)[:n]
        if "dist_km" in e: d = np.asarray(e["dist_km"], float)[:n]
        else:
            sl = np.asarray(e["src_loc"], float)
            epi = 111.19 * np.hypot(loc[:, 0] - sl[0], (loc[:, 1] - sl[1]) * np.cos(np.radians(sl[0]))); d = np.hypot(epi, sl[2])
        for k in range(n):
            if pf[k] != 0 or not np.isfinite(tp[k]) or not np.isfinite(d[k]): continue
            P.append(dict(ev=ie, sta=f"{loc[k, 0]:.4f},{loc[k, 1]:.4f}", t=th, dist=float(d[k]), r=float(tp[k] - d[k] / VP),
                          hour=f"{th:%Y-%m-%d %H}"))
    return P

def old_d(P):
    """元の (d): 検測 20 以上の 1 時間ごとの |中央値 − 全体の中央値| の最大と、その時間"""
    med = float(np.median([p["r"] for p in P])); H = {}
    for p in P: H.setdefault(p["hour"], []).append(p["r"])
    v = [(abs(float(np.median(x)) - med), h, len(x)) for h, x in H.items() if len(x) >= MIN_N]
    if not v: return dict(n_hours=0, max_abs_dev_s=None, worst_hour=None, pass_=None)
    m = max(v)
    return dict(n_hours=len(v), max_abs_dev_s=m[0], worst_hour=m[1], pass_=bool(m[0] <= TOL))

def event_demeaned(P):
    """1: 各検測から、同じ地震の他の局の検測の中央値を引く(他の局の検測が MIN_EV_PICKS 以上の時だけ。それ以外は NaN)"""
    by_ev = {}
    for i, p in enumerate(P): by_ev.setdefault(p["ev"], []).append(i)
    e = np.full(len(P), np.nan)
    for ev, idx in by_ev.items():
        for i in idx:
            oth = [P[j]["r"] for j in idx if P[j]["sta"] != P[i]["sta"]]
            if len(oth) >= MIN_EV_PICKS: e[i] = P[i]["r"] - float(np.median(oth))
    return e

def station_series(P, e):
    """局ごとの、時刻の順に並べた (添字の一覧)。検測 MIN_N 以上の局だけ"""
    by_sta = {}
    for i, p in enumerate(P):
        if np.isfinite(e[i]): by_sta.setdefault(p["sta"], []).append(i)
    return {s: sorted(idx, key=lambda i: (P[i]["t"], P[i]["ev"])) for s, idx in by_sta.items() if len(idx) >= MIN_N}

def window_stat(u, w=W):
    """2: 「窓の中央値 − 同じ局の窓の外の中央値」の絶対値が最大の窓。戻り値 (値, 始まりの位置, 窓の数)"""
    mx, at, nw = 0.0, None, 0
    for j in range(0, len(u) - w + 1):
        out_ = np.concatenate([u[:j], u[j + w:]])
        v = float(np.median(u[j:j + w]) - np.median(out_)); nw += 1
        if abs(v) > abs(mx): mx, at = v, j
    return mx, at, nw

def new_d(P, w=W):
    """新しい (d)。戻り値: 判定・最大の |値|・その窓の始まり・窓の数・判定した局の数・上位 5 局"""
    e = event_demeaned(P); S = station_series(P, e)
    worst, n_win, per = (0.0, None), 0, []
    for s, idx in S.items():
        mx, at, nw = window_stat(e[idx], w); n_win += nw
        t_at = None if at is None else P[idx[at]]["t"]
        per.append((abs(mx), s, mx, t_at, len(idx)))
        if abs(mx) > abs(worst[0]): worst = (mx, t_at)
    per.sort(key=lambda x: -x[0])
    return dict(pass_=(bool(abs(worst[0]) <= TOL) if S else None), max_abs_window_median_s=abs(worst[0]), worst_value_s=worst[0],
                worst_window_start_jst=(None if worst[1] is None else f"{worst[1]:%Y-%m-%d %H}"), n_stations_judged=len(S), n_windows=n_win,
                top5=[dict(abs_s=x[0], value_s=x[2], window_start_jst=(None if x[3] is None else f"{x[3]:%Y-%m-%d %H}"), n=x[4]) for x in per[:5]])

def detection_rates(P, shifts=(0.3, 0.6, 1.0), k=12, w=W):
    """B: 判定する全ての局・続いた k 検測の全ての始まりで、+δ を足した時に、その局の新しい (d) が見つける割合"""
    e = event_demeaned(P); S = station_series(P, e)
    out = {}
    for ds in shifts:
        hit = tot = 0; small = [0, 0]
        for s, idx in S.items():
            u0 = e[idx]
            for j in range(0, len(u0) - k + 1):
                u = u0.copy(); u[j:j + k] += ds
                det = abs(window_stat(u, w)[0]) > TOL
                hit += det; tot += 1
                if len(u0) <= 30: small[0] += det; small[1] += 1
        out[f"{ds:+.1f}"] = dict(rate=(hit / tot if tot else None), n_trials=tot,
                                 rate_stations_20_to_30_picks=(small[0] / small[1] if small[1] else None), n_trials_small=small[1])
    return out

def shifted(P, sel, ds):
    Q = [dict(p) for p in P]
    for i in sel: Q[i]["r"] += ds
    return Q

def controls(P):
    """C の作り: 検測の最も多い地震(C1: 全ての局・C2: 遠い半分の局)"""
    ce = {}
    for p in P: ce[p["ev"]] = ce.get(p["ev"], 0) + 1
    e0 = max(ce, key=lambda k: (ce[k], -k))
    ie = sorted([i for i, p in enumerate(P) if p["ev"] == e0], key=lambda i: P[i]["dist"])
    return dict(C1=ie, C2=ie[len(ie) // 2:], event_n=len(ie))

def selftest():
    def check(c, m):
        if not c: sys.exit(f"{TAG} STOP: selftest に失敗: {m}")
    rng = np.random.default_rng(0)
    t0 = datetime(2018, 4, 12)
    P = []
    for ev in range(200):
        t = t0 + timedelta(minutes=37 * ev)
        for k in range(24):
            P.append(dict(ev=ev, sta=f"s{k:02d}", t=t, dist=10.0 + k, r=0.3 + 0.01 * k + rng.normal(0, 0.05), hour=f"{t:%Y-%m-%d %H}"))
    check(new_d(P)["pass_"] is True, "正常は PASS")
    c = controls(P)
    st = sorted([i for i, p in enumerate(P) if p["sta"] == "s05"], key=lambda i: (P[i]["t"], P[i]["ev"]))
    check(new_d(shifted(P, st[90:102], 0.6))["pass_"] is False, "1 局の続いた 12 検測に +0.6 s は FAIL")
    check(new_d(shifted(P, st[90:102], 0.3))["pass_"] is True, "+0.3 s は PASS")
    check(new_d(shifted(P, st[:100], 0.6))["pass_"] is False, "1 局の検測の半分(100/200)に +0.6 s も FAIL(窓の外で測る)")
    check(new_d(shifted(P, c["C1"], 1.0))["pass_"] is True, "1 地震の全局に +1.0 s は PASS(発生時刻のずれ)")
    check(new_d(shifted(P, c["C2"], 1.0))["pass_"] is True, "1 地震の遠い半分に +1.0 s は PASS")
    check(old_d(shifted(P, c["C1"], 1.0))["pass_"] is False, "元の (d) は 1 地震の全局 +1.0 s で FAIL(地震 1 つの時間)")
    sel = [i for i, p in enumerate(P) if 90 <= p["ev"] < 102]
    check(new_d(shifted(P, sel, 0.6))["pass_"] is True, "網全体の時刻のずれは見えない(限界)")
    Q = [p for p in P if p["ev"] < 30]                                      # 1 局 30 検測の小さい場合
    dr = detection_rates(Q, shifts=(0.6,))
    check(dr["+0.6"]["rate"] is not None and dr["+0.6"]["rate"] >= 0.95, f"小さい局での見つけた割合 {dr}")
    print(f"{TAG} selftest: 正常・陽性対照(+0.6 s FAIL・+0.3 s PASS・局の半分 FAIL)・陰性対照(1 地震の全局・遠い半分)・限界・小さい局の見つけた割合の 9 例に合格")

selftest()
if a.selftest: sys.exit(0)
import torch
if not a.cache: sys.exit(f"{TAG} STOP: --cache が 1 つも無い")
OUT = Path(a.out) if a.out else Path(".")
OUT.mkdir(parents=True, exist_ok=True)
print(f"{TAG} 本スクリプト v1 SHA-256 {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}")
RES = {}
for spec in a.cache:
    if "=" not in spec: sys.exit(f"{TAG} STOP: --cache は 名前=場所 の形({spec})")
    name, path = spec.split("=", 1); p = Path(path)
    if not p.exists():
        print(f"\n{TAG} {name}: {p} が無いので飛ばす"); continue
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    EV = torch.load(p, weights_only=False); P = picks_from_events(EV)
    print(f"\n{TAG} ===== {name}: {p.name}  SHA-256 {sha[:12]}…  地震 {len(EV)}・P を測った検測 {len(P)}")
    if len(P) < 100:
        print(f"{TAG} {name}: 検測が 100 未満なので飛ばす"); continue
    o, n = old_d(P), new_d(P)
    c = controls(P)
    dr = detection_rates(P)
    rC1, rC2 = new_d(shifted(P, c["C1"], 1.0)), new_d(shifted(P, c["C2"], 1.0))
    ws = {str(w): new_d(P, w)["max_abs_window_median_s"] for w in WS}
    f = lambda x: "—" if x is None else f"{x:.3f}"
    print(f"{TAG} {name}: 元の (d) 1 時間ごと: {o['n_hours']} 時間・最大 {f(o['max_abs_dev_s'])} s({o['worst_hour']})→ "
          f"{'PASS' if o['pass_'] else 'FAIL'}")
    print(f"{TAG} {name}: 新しい (d) 局ごと W={W}: 判定した局 {n['n_stations_judged']}・窓 {n['n_windows']}・最大 |窓の中央値 − 窓の外の中央値| "
          f"{f(n['max_abs_window_median_s'])} s({n['worst_window_start_jst']} からの窓)→ {'PASS' if n['pass_'] else 'FAIL'}")
    print(f"{TAG} {name}:   上位 5 局(|値| s・窓の始まり・その局の検測): " +
          "  ".join(f"{x['abs_s']:.3f}({x['window_start_jst']}, n={x['n']})" for x in n["top5"]))
    print(f"{TAG} {name}: 陽性対照(判定する全ての局・続いた 12 検測の全ての始まり): 見つけた割合 " +
          "  ".join(f"{k} s: {v['rate']:.3f}({v['n_trials']} 回。検測 20〜30 の局 {('—' if v['rate_stations_20_to_30_picks'] is None else format(v['rate_stations_20_to_30_picks'], '.3f'))}・{v['n_trials_small']} 回)"
                    for k, v in dr.items()))
    print(f"{TAG} {name}: 陰性対照(検測 {c['event_n']} の地震): 全局 +1.0 s → {'PASS' if rC1['pass_'] else 'FAIL(注意)'}・最大 {f(rC1['max_abs_window_median_s'])} s   "
          f"遠い半分 +1.0 s → {'PASS' if rC2['pass_'] else 'FAIL(注意)'}・最大 {f(rC2['max_abs_window_median_s'])} s")
    print(f"{TAG} {name}: 窓の大きさごとの最大 |窓の中央値 − 窓の外の中央値|(記述): " + "  ".join(f"W={k}: {v:.3f}" for k, v in ws.items()))
    ok = bool(n["pass_"] and rC1["pass_"] and rC2["pass_"] and dr["+0.6"]["rate"] is not None and dr["+0.6"]["rate"] >= 0.95)
    print(f"{TAG} {name}: 期待どおりか(元のキャッシュ PASS・陰性対照 PASS・+0.6 s の見つけた割合 ≥ 0.95): {'はい' if ok else 'いいえ(注意)'}")
    RES[name] = dict(cache=str(p), cache_sha256=sha, n_events=len(EV), n_picks=len(P), old_d=o, new_d=n, as_expected=ok,
                     positive_control_detection=dr,
                     negative_control=dict(event_n=c["event_n"], all_stations_plus_1p0=rC1, far_half_plus_1p0=rC2),
                     max_abs_by_window_size=ws)
if not RES: sys.exit(f"{TAG} STOP: 読めたキャッシュが 0")
json.dump(dict(script="25_04x_gclock2_station_window_dev.py", version="v1", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               purpose="dev of the new G-clock2 condition (d) for preregistration 25, on caches of sequences already tested or stopped; "
                       "no Shimane data read; no location or method error computed",
               rule=dict(vp_kms=VP, min_n=MIN_N, tol_s=TOL, window=W, min_event_picks=MIN_EV_PICKS), results=RES),
          open(OUT / "25_04x_gclock2_station_window_dev.json", "w"), indent=1, default=str)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
names = list(RES)
fig, ax = plt.subplots(figsize=(10, 4.2))
x = np.arange(len(names)); bw = 0.16
series = [("Original (d): max hourly |dev|", [RES[k]["old_d"]["max_abs_dev_s"] or 0 for k in names], "0.6"),
          ("New (d): max |window median - out-of-window median|", [RES[k]["new_d"]["max_abs_window_median_s"] for k in names], "tab:blue"),

          ("New (d), one event all stations +1.0 s", [RES[k]["negative_control"]["all_stations_plus_1p0"]["max_abs_window_median_s"] for k in names], "tab:green"),
          ("New (d), one event far half +1.0 s", [RES[k]["negative_control"]["far_half_plus_1p0"]["max_abs_window_median_s"] for k in names], "tab:olive")]
for j, (lab, v, col) in enumerate(series):
    ax.bar(x + (j - 1.5) * bw, v, width=bw, color=col, label=lab)
ax.axhline(TOL, color="k", ls="--", lw=1, label=f"Allowance ({TOL} s)")
ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylabel("Offset (s)")
ax.set_title(f"G-clock2 condition (d): original hourly check vs station-window check (W = {W}), dev on earlier sequences", fontsize=9)
ax.grid(alpha=0.3, axis="y")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(OUT / "25_04x_gclock2_station_window_dev.pdf", bbox_inches="tight"); plt.close(fig)
print(f"\n{TAG} 出力: {OUT / '25_04x_gclock2_station_window_dev.json'}、{OUT / '25_04x_gclock2_station_window_dev.pdf'}")
bad = [k for k, v in RES.items() if not v["as_expected"]]
if bad: sys.exit(f"{TAG} 期待と違う系列: {bad}(この出力を貼る。凍結の前に作りを見直す)")
