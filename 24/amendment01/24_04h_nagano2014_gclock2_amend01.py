#!/usr/bin/env python3
# =============================================================================
# Script : 24_04h_nagano2014_gclock2_amend01.py  (v1)
#          [事前登録 24 の変更の記録 01 で決めた G-clock2 の判定(条件 (d) だけを改めた版)を、24_04d・24_04e の出力とキャッシュから
#           計算する。位置の計算・方法の誤差は一切出さない]
# Project: ARGUS(新生)— 事前登録 24(長野県北部 2014)。変更の記録 01(24_amendment01_nagano2014.md)の 2 節の規則を実装する。
#
# なぜ必要か:
#   24_04d の (d)「日本時間の 1 時間ごと、検測 20 以上、|その時間の中央値 − 全体の中央値| ≤ 0.5 s」は、2014-12-01 07 時台(+0.672 s)
#   で FAIL した。24_04g(読むだけの診断)で、その時間の地震は 1 つだけで、同じ局の前後 6 時間の他の地震は正常(+0.101 s)、
#   1 つ前・1 つ後の地震も正常、ずれは距離とともに大きく S−P もおかしい(遠い局の P が雑音の上)ことが分かった。
#   地震が 1 つしかない時間では、(d) は時計ではなくその 1 地震の検測の質を測る(検測 20 以上の 155 時間のうち 92 時間がそうだった)。
#   変更の記録 01 は、(d) の目的(時計のずれを見つける)に合わせて、地震が 1 つしかない時間で外れた時だけ、時計を直接見る確かめに
#   置き換える。閾値(0.5 s)・検測の数の下限(20)・残りの式・時間の区切り方は 24_04d と同じで、新しい閾値は作らない。
#
# 変更の記録 01 の規則(d-amend01)。検測 20 以上の全ての時間 h について(24_04d と同じ時間・同じ残り):
#   (d1) |dev_h| ≤ 0.5 s なら合格(元の (d) と同じ)。
#   (d2) |dev_h| > 0.5 s で、その時間に P を測った地震が 2 つ以上なら不合格(元の (d) と同じ)。
#   (d3) |dev_h| > 0.5 s で、その時間に P を測った地震が 1 つだけなら、その地震の P を測った局(同じ局)について、
#        他の全ての地震の P の「残り − その局の全期間の中央値」を、発生時刻の前 6 時間(−6 h ≤ Δt < 0)と
#        後 6 時間(0 ≤ Δt ≤ +6 h)に分けて集める。前と後のそれぞれで、集めた検測が 20 以上で、その中央値の絶対値が 0.5 s 以下なら合格。
#        どちらかの検測が 20 未満か、0.5 s を超えたら不合格。
#        (局の時計がその頃ずれていれば、同じ局の前か後の地震も同じだけずれる。前と後に分けるのは、時計がその地震の所で
#         ずれ始めた・ずれ終わった形を、ずれていない側の地震で薄めて見逃さないため。前後を合わせた量は 24_04g の
#         「同じ局の前後 6 時間」と同じで、表示と JSON に参考として残す)
#   (d-amend01) は全ての時間が合格の時だけ合格。
#   その他の条件は事前登録 24 の 5.3 節のまま: (a)・(b)・(e)・(f) は 24_04d の JSON の値、5.3 節の 3(G-clock の地震が見つかる:
#   found_dt_s ≤ 1.5 s かつ n_picks ≥ 4)も同じ JSON から。(c) は 5.3 節の 4 のとおり、24_04d の (c) の合否によらず (c-near) で決める
#   (24_04e の表で、80 km 以内・検測 20 以上の全ての局で |dev_s| ≤ 1.0 s、その局が 1 つ以上)。24_04d の (c) が FAIL で (c-near) が
#   通った時は c-far の印を付ける。
#   G-clock2(変更の記録 01)= (a)・(b)・(e)・(f)・5.3 節の 3・(c-near)・(d-amend01) が全て合格。
#
# 限界(変更の記録 01 にも書く): 1 地震だけの時間で、その地震の間だけ全ての局の時計が同じだけずれる、という形は (d3) でも
#   見分けられない(元の (d) でも検測の取り違えと見分けられなかった)。全ての局で同じずれは発生時刻のずれと同じで、24_05 の物理の方法は
#   地震ごとの中央値を引くので位置には効かない。前か後の 6 時間の中で、同じ局の検測の半分より少ない部分だけに掛かる短い時計のずれも
#   (d3) では見逃しうる(その間の時間が 2 地震以上か |ずれ| ≤ 0.5 s なら、元の (d) と同じ扱い)。
#
# 何をしないか: 位置の計算・どの方法の誤差も出さない。キャッシュ・24_04d・24_04e の出力を変えない。震源一覧を読まない。
#
# Usage(Colab。Drive をつなぐだけでよい。セルは 24_amendment01_COLAB_JA.md の A1〜A3):
#   !python /content/drive/MyDrive/ARGUS/src/24_04h_nagano2014_gclock2_amend01.py --base /content/drive/MyDrive/ARGUS_nagano2014
# 入力  : (--base の下)data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt・data/24_04d_gclock2.json・
#         data/24_04e_station_picks.csv
# 出力  : data/24_04h_gclock2_amend01.json / PDF/24_04h_gclock2_amend01.pdf。G-clock2(変更の記録 01)が FAIL なら、JSON と PDF を
#         書いてから exit code 1(最後の行が「STOP(G-clock2・変更の記録 01)」)。
# 止める条件(STOP。JSON は書かない。exit code 1): selftest の失敗・入力が無い・全体の中央値が 24_04d と違う・時間の集合か、どれかの
#         時間の検測の数・中央値が 24_04d と違う・元の (d) の判定が 24_04d と違う・検測 20 以上の時間が 0・24_04e の表の局ごとの
#         検測の数か dev_s が、キャッシュから同じ式で計算した値と違う(別のキャッシュから作った表)
# =============================================================================
import sys, csv, json, argparse, hashlib
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

ap = argparse.ArgumentParser(description="24_04h: G-clock2 の判定(事前登録 24 の変更の記録 01)")
ap.add_argument("--base", required=True, help="ARGUS_nagano2014 の場所(Drive なら /content/drive/MyDrive/ARGUS_nagano2014)")
ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt")
ap.add_argument("--gclock", default="data/24_04d_gclock2.json")
ap.add_argument("--station-csv", dest="station_csv", default="data/24_04e_station_picks.csv")
ap.add_argument("--selftest", action="store_true", help="規則の関数の試験だけを回して終わる")
a = ap.parse_args()
VP, MIN_N, TOL_HOUR, WIN_H = 6.0, 20, 0.5, 6.0                  # 24_04d と同じ VP・MIN_N・TOL_HOUR。WIN_H は 24_04g と同じ前後 6 時間
NEAR_KM, TOL_STA_NEAR = 80.0, 1.0                                # 事前登録 24 の 5.3 節の 4(c-near)
TAG = "[24_04h]"

def jst_hour(ot):                                                # 24_04d と同じ: 秒で切って 9 時間を足す
    t = datetime.strptime(str(ot).replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
    return t + timedelta(hours=9)
def jst_full(ot):                                                # 24_04g と同じ(秒の小数を残す)
    s = str(ot).replace("T", " ")
    t = datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
    frac = s[19:].split("+")[0]
    us = int(round(float("0" + frac) * 1e6)) if frac.startswith(".") and len(frac) > 1 else 0
    return t + timedelta(hours=9, microseconds=us)

def judge_hours(rows, MED, STA_MED, EVT):
    """変更の記録 01 の (d1)〜(d3)。rows: dict(ev, sta, r, hour)。EVT: 地震ごとの発生時刻(日本時間)。時間ごとの結果の一覧を返す"""
    H = {}
    for x in rows: H.setdefault(x["hour"], []).append(x)
    out = []
    for h, xs in sorted(H.items()):
        if len(xs) < MIN_N: continue
        evs = sorted({x["ev"] for x in xs}); dev = float(np.median([x["r"] for x in xs])) - MED
        o = dict(hour=h, n_picks=len(xs), n_events=len(evs), dev_s=dev, rule=None, pm6h_median_s=None, pm6h_n=None,
                 before_median_s=None, before_n=None, after_median_s=None, after_n=None, event_sta_rel_median_s=None, pass_=None)
        if abs(dev) <= TOL_HOUR:
            o.update(rule="d1", pass_=True)
        elif len(evs) >= 2:
            o.update(rule="d2", pass_=False)
        else:
            e0 = evs[0]; t0 = EVT[e0]; st = {x["sta"] for x in xs}
            W = [((EVT[z["ev"]] - t0).total_seconds(), z["r"] - STA_MED[z["sta"]]) for z in rows
                 if z["ev"] != e0 and z["sta"] in st and abs((EVT[z["ev"]] - t0).total_seconds()) <= WIN_H * 3600]
            bef = [v for dt, v in W if dt < 0]; aft = [v for dt, v in W if dt >= 0]
            med = lambda v: float(np.median(v)) if v else None
            ok = lambda v: len(v) >= MIN_N and abs(float(np.median(v))) <= TOL_HOUR
            o.update(rule="d3", event_sta_rel_median_s=float(np.median([x["r"] - STA_MED[x["sta"]] for x in xs])),
                     pm6h_median_s=med([v for _, v in W]), pm6h_n=len(W),
                     before_median_s=med(bef), before_n=len(bef), after_median_s=med(aft), after_n=len(aft),
                     pass_=bool(ok(bef) and ok(aft)))
        out.append(o)
    return out

def selftest():
    def check(c, msg):
        if not c: sys.exit(f"{TAG} STOP: selftest に失敗: {msg}")
    check(jst_hour("2014-12-01 22:10:05.3") == datetime(2014, 12, 2, 7, 10, 5), "jst_hour")
    check(abs((jst_full("2014-12-01 22:10:05.20") - datetime(2014, 12, 2, 7, 10, 5, 200000)).total_seconds()) < 1e-6, "jst_full")
    check(jst_full(datetime(2014, 12, 1, 22, 10, 5, 200000)) == datetime(2014, 12, 2, 7, 10, 5, 200000), "jst_full datetime")
    T = datetime(2014, 12, 1, 7, 40)
    def mk(ev_specs):
        rows, EVT = [], {}
        for ev, t, sts, off in ev_specs:
            EVT[ev] = t
            for s in sts: rows.append(dict(ev=ev, sta=s, r=off, hour=f"{t:%Y-%m-%d %H}"))
        return rows, EVT
    S24 = [f"s{i}" for i in range(24)]
    # 1 地震だけの時間が +0.7 s、前後 1 時間の地震は 0 → d3 で合格
    rows, EVT = mk([(0, T - timedelta(hours=1), S24, 0.0), (1, T, S24, 0.7), (2, T + timedelta(hours=1), S24, 0.0)])
    J = {o["hour"]: o for o in judge_hours(rows, 0.0, {s: 0.0 for s in S24}, EVT)}
    check(J["2014-12-01 07"]["rule"] == "d3" and J["2014-12-01 07"]["pass_"] and J["2014-12-01 07"]["pm6h_n"] == 48
          and J["2014-12-01 07"]["before_n"] == 24 and J["2014-12-01 07"]["after_n"] == 24, "d3 pass")
    # 同じ局の前後も +0.7 s(時計のずれ)→ d1 で前後の時間も外れ、d3 も不合格
    rows, EVT = mk([(0, T - timedelta(hours=1), S24, 0.7), (1, T, S24, 0.7), (2, T + timedelta(hours=1), S24, 0.7)])
    J = {o["hour"]: o for o in judge_hours(rows, 0.0, {s: 0.0 for s in S24}, EVT)}
    check(not J["2014-12-01 07"]["pass_"] and J["2014-12-01 07"]["rule"] == "d3", "d3 fail (clock)")
    # 時計がこの地震でずれ始めた(前は 0、後は +0.7 s が 3 地震)→ 前後を合わせると 0.7 s 以下でも、後ろの側で不合格
    rows, EVT = mk([(0, T - timedelta(hours=1), S24, 0.0), (5, T - timedelta(hours=2), S24, 0.0), (6, T - timedelta(hours=3), S24, 0.0),
                    (7, T - timedelta(hours=4), S24, 0.0), (1, T, S24, 0.7), (2, T + timedelta(hours=1), S24, 0.7)])
    J = {o["hour"]: o for o in judge_hours(rows, 0.0, {s: 0.0 for s in S24}, EVT)}
    check(not J["2014-12-01 07"]["pass_"] and abs(J["2014-12-01 07"]["pm6h_median_s"]) < 1e-12 and J["2014-12-01 07"]["after_median_s"] > 0.5,
          "d3 fail (clock step at the event)")
    # 片側(後)に地震が無い → その側の検測 20 未満で不合格
    rows, EVT = mk([(0, T - timedelta(hours=1), S24, 0.0), (1, T, S24, 0.7)])
    J = {o["hour"]: o for o in judge_hours(rows, 0.0, {s: 0.0 for s in S24}, EVT)}
    check(not J["2014-12-01 07"]["pass_"] and J["2014-12-01 07"]["after_n"] == 0, "d3 fail (one side empty)")
    # 前後 6 時間に他の地震が無い → 検測 20 未満で不合格
    rows, EVT = mk([(0, T - timedelta(hours=7), S24, 0.0), (1, T, S24, 0.7)])
    J = {o["hour"]: o for o in judge_hours(rows, 0.0, {s: 0.0 for s in S24}, EVT)}
    check(not J["2014-12-01 07"]["pass_"] and J["2014-12-01 07"]["pm6h_n"] == 0, "d3 fail (n < 20)")
    # 前後 6 時間ちょうどは入る・6 時間を超えると入らない・他の局は入らない
    rows, EVT = mk([(0, T - timedelta(hours=6), S24, 0.0), (1, T, S24, 0.7), (2, T + timedelta(hours=6, seconds=1), S24, 0.9),
                    (3, T + timedelta(hours=2), [f"x{i}" for i in range(24)], 0.9), (4, T + timedelta(hours=6), S24, 0.1)])
    J = {o["hour"]: o for o in judge_hours(rows, 0.0, {**{s: 0.0 for s in S24}, **{f"x{i}": 0.0 for i in range(24)}}, EVT)}
    check(J["2014-12-01 07"]["pm6h_n"] == 48 and J["2014-12-01 07"]["before_n"] == 24 and J["2014-12-01 07"]["after_n"] == 24
          and abs(J["2014-12-01 07"]["after_median_s"] - 0.1) < 1e-12 and J["2014-12-01 07"]["pass_"], "window / same stations")
    # 地震 2 つの時間で外れ → d2 で不合格
    rows, EVT = mk([(0, T, S24[:12], 0.7), (1, T + timedelta(minutes=10), S24[12:], 0.7)])
    J = {o["hour"]: o for o in judge_hours(rows, 0.0, {s: 0.0 for s in S24}, EVT)}
    check(J["2014-12-01 07"]["rule"] == "d2" and not J["2014-12-01 07"]["pass_"], "d2 fail")
    # 局のふだんのずれは引かれる(局の中央値 +0.3、前後の地震 +0.3 → 0)
    rows, EVT = mk([(0, T - timedelta(hours=1), S24, 0.3), (1, T, S24, 0.9), (2, T + timedelta(hours=1), S24, 0.3)])
    J = {o["hour"]: o for o in judge_hours(rows, 0.0, {s: 0.3 for s in S24}, EVT)}
    check(J["2014-12-01 07"]["pass_"] and abs(J["2014-12-01 07"]["pm6h_median_s"]) < 1e-12, "station median removed")
    # 検測 20 未満の時間は判定しない
    rows, EVT = mk([(0, T, S24[:19], 5.0)])
    check(judge_hours(rows, 0.0, {s: 0.0 for s in S24}, EVT) == [], "min n")
    # 6 時間の境目は 1 ms でも超えたら入らない
    rows, EVT = mk([(0, T - timedelta(hours=6, milliseconds=1), S24, 0.9), (1, T, S24, 0.7), (2, T + timedelta(hours=1), S24, 0.0),
                    (3, T - timedelta(hours=5, minutes=59, seconds=59, milliseconds=999), S24, 0.0)])
    J = {o["hour"]: o for o in judge_hours(rows, 0.0, {s: 0.0 for s in S24}, EVT)}
    check(J["2014-12-01 07"]["before_n"] == 24 and abs(J["2014-12-01 07"]["before_median_s"]) < 1e-12 and J["2014-12-01 07"]["pass_"], "sub-second boundary")
    print(f"{TAG} selftest: 時刻の変換と (d1)〜(d3) の規則の 10 例に合格")
selftest()
if a.selftest: sys.exit(0)

import torch
BASE = Path(a.base)
cp, gp, sp = BASE / a.cache, BASE / a.gclock, BASE / a.station_csv
for p in (cp, gp, sp):
    if not p.exists(): sys.exit(f"{TAG} STOP: {p} が無い")
SELF_SHA = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
sha_c, sha_g, sha_s = (hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp, gp, sp))
print(f"{TAG} 本スクリプト v1 SHA-256 {SELF_SHA}")
print(f"{TAG} キャッシュ {cp.name}  SHA-256 {sha_c}")
print(f"{TAG} 24_04d の JSON  SHA-256 {sha_g}")
print(f"{TAG} 24_04e の表      SHA-256 {sha_s}")
EV = torch.load(cp, weights_only=False)
G = json.load(open(gp))

# ---- 1. 残り(24_04d と同じ式・同じ検測)
rows = []
for ie, e in enumerate(EV):
    th = jst_hour(e["origin_time"]); n = int(e["n_real_stations"])
    tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    loc = np.asarray(e["sta_locs"], float)[:n]
    if "dist_km" in e: d = np.asarray(e["dist_km"], float)[:n]
    else:                                                        # 24_04d と同じ(古いキャッシュ: 15_01c と同じ式で震源距離を出す)
        sl = np.asarray(e["src_loc"], float)
        epi = 111.19 * np.hypot(loc[:, 0] - sl[0], (loc[:, 1] - sl[1]) * np.cos(np.radians(sl[0]))); d = np.hypot(epi, sl[2])
    for k in range(n):
        if pf[k] != 0 or not np.isfinite(tp[k]) or not np.isfinite(d[k]): continue
        rows.append(dict(ev=ie, sta=f"{loc[k, 0]:.4f},{loc[k, 1]:.4f}", r=float(tp[k] - d[k] / VP), hour=f"{th:%Y-%m-%d %H}"))
R = np.array([x["r"] for x in rows]); MED = float(np.median(R)); ref = float(G["result"]["median_s"])
print(f"{TAG} 全体: 検測 {len(R)}  残りの中央値 {MED:+.6f} s(24_04d の値 {ref:+.6f} s)")
if abs(MED - ref) > 1e-6: sys.exit(f"{TAG} STOP: 全体の中央値が 24_04d と違う(キャッシュか式が違う)")
STA_MED = {s: float(np.median([x["r"] for x in rows if x["sta"] == s])) for s in sorted({x["sta"] for x in rows})}
EVT = {ie: jst_full(e["origin_time"]) for ie, e in enumerate(EV)}

# ---- 2. (d-amend01)
HJ = judge_hours(rows, MED, STA_MED, EVT)
if not HJ: sys.exit(f"{TAG} STOP: 検測 {MIN_N} 以上の時間が 0")
bh = G.get("by_hour", {})
ALLH = {}
for x in rows: ALLH.setdefault(x["hour"], []).append(x["r"])
if set(ALLH) != set(bh): sys.exit(f"{TAG} STOP: 時間の集合が 24_04d と違う(24_04d {len(bh)}・ここ {len(ALLH)})")
for h, v in ALLH.items():                                         # 検測 20 未満の時間も含め、全ての時間を照らす
    if bh[h]["n"] != len(v) or abs(bh[h]["median"] - float(np.median(v))) > 1e-6:
        sys.exit(f"{TAG} STOP: {h} 時台の検測の数か中央値が 24_04d と違う")
max_dev = max(abs(o["dev_s"]) for o in HJ)
if (max_dev <= TOL_HOUR) != bool(G["pass_hour"]): sys.exit(f"{TAG} STOP: 元の (d) の判定が 24_04d と食い違う")
pd_amend = all(o["pass_"] for o in HJ)

# ---- 3. その他の条件(事前登録 24 の 5.3 節のまま)
pa, pb, pe, pf_ = bool(G["pass_all"]), bool(G["pass_day"]), bool(G["pass_events"]), bool(G["pass_measured_frac"])
ev_find = all(x["found_dt_s"] <= 1.5 and x["n_picks"] >= 4 for x in G["gclock_events"])      # 5.3 節の 3
STA_N = {}
for x in rows: STA_N[x["sta"]] = STA_N.get(x["sta"], 0) + 1
near, n_csv = [], 0
with open(sp) as f:
    for row in csv.DictReader(f):
        n_csv += 1; k_ = row["station"]
        if k_ not in STA_N or int(row["n"]) != STA_N[k_] or abs(float(row["dev_s"]) - (STA_MED[k_] - MED)) > 0.0005 + 1e-9:
            sys.exit(f"{TAG} STOP: 24_04e の表の局 {k_} の検測の数か dev_s が、キャッシュから計算した値と違う(別のキャッシュから作った表)")
        if float(row["epi_from_mainshock_km"]) <= NEAR_KM and int(row["n"]) >= MIN_N:
            near.append(dict(epi_from_mainshock_km=float(row["epi_from_mainshock_km"]), n=int(row["n"]), dev_s=float(row["dev_s"])))
if n_csv != len(STA_N): sys.exit(f"{TAG} STOP: 24_04e の表の局の数({n_csv})が、キャッシュの P を測った局の数({len(STA_N)})と違う")
c_near = bool(near) and all(abs(x["dev_s"]) <= TOL_STA_NEAR for x in near)       # 5.3 節の 4: 24_04d の (c) によらず、これで決める
pc = bool(G["pass_station"])
c_far_label = (not pc) and c_near
PASS = bool(pa and pb and c_near and pd_amend and pe and ev_find and pf_)

def pf(b): return "PASS" if b else "FAIL"
print(f"\n{TAG} 事前登録 24 の 5.3 節の条件(24_04d・24_04e の出力から):")
print(f"   (a) 全体                     {pf(pa)}")
print(f"   (b) 日ごと                   {pf(pb)}")
print(f"   (c) 局ごと(24_04d)          {pf(pc)}(5.3 節の 4 により、判定は次の (c-near) で行う)")
print(f"       (c-near) 80 km 以内・検測 {MIN_N} 以上の {len(near)} 局で |dev_s| ≤ {TOL_STA_NEAR} s: "
      f"{pf(c_near)}(最大 {max((abs(x['dev_s']) for x in near), default=float('nan')):.2f} s)")
print(f"   (e) G-clock の地震            {pf(pe)}(見つかる条件 {pf(ev_find)})")
print(f"   (f) P を測った割合            {pf(pf_)}")
print(f"   (d) 元の規則(24_04d)        {pf(G['pass_hour'])}(最大 {max_dev:.3f} s、{len(HJ)} 時間)")
n1 = sum(o["rule"] == "d1" for o in HJ)
print(f"\n{TAG} (d-amend01) 検測 {MIN_N} 以上の {len(HJ)} 時間: (d1) |ずれ| ≤ {TOL_HOUR} s の時間 {n1}")
for o in HJ:
    if o["rule"] == "d1": continue
    if o["rule"] == "d2":
        print(f"   (d2) {o['hour']} 時台: 地震 {o['n_events']}・検測 {o['n_picks']}・ずれ {o['dev_s']:+.3f} s → FAIL(地震が 2 つ以上の時間)")
    else:
        fm = lambda m: "—" if m is None else f"{m:+.3f} s"
        print(f"   (d3) {o['hour']} 時台: 地震 1・検測 {o['n_picks']}・ずれ {o['dev_s']:+.3f} s → 同じ局の他の地震の「残り − 局の中央値」の中央値"
              f"(基準: 前と後のそれぞれで検測 {MIN_N} 以上・|中央値| ≤ {TOL_HOUR} s)")
        print(f"        前 {WIN_H:.0f} 時間: 検測 {o['before_n']}・{fm(o['before_median_s'])}   後 {WIN_H:.0f} 時間: 検測 {o['after_n']}・{fm(o['after_median_s'])}"
              f"   (参考: 前後を合わせて 検測 {o['pm6h_n']}・{fm(o['pm6h_median_s'])}。24_04g と同じ量) → {pf(o['pass_'])}")
print(f"   (d-amend01): {pf(pd_amend)}")
print(f"\n{TAG} G-clock2(事前登録 24・変更の記録 01): {pf(PASS)}")
n3 = sum(o["rule"] == "d3" for o in HJ)
LABEL_EN = ("preregistered test with a post hoc amendment (amendment 01, written after the hourly clock check G-clock2 (d) failed in one "
            "single-event hour and after a read-only diagnosis (24_04g), registered before the test was opened; that hour was re-checked "
            "against the same stations' picks of other events in the preceding and following 6 h (24_04h); the preregistration had stated "
            "that no amendment would be made)")
LABEL_JA = ("事後に決めた変更の記録 01 付きの事前登録の試験(G-clock2 (d) が地震 1 つだけの 1 時間で不合格となり、読むだけの診断 24_04g を見た後に書き、"
            "試験を開く前に登録した。その時間を同じ局の前後 6 時間の他の地震で確かめ直した(24_04h)。事前登録では変更の記録なしとしていた)")
CFAR_EN = ("preregistered test; the far-station (> 80 km) part of the station-level clock check (G-clock2 (c)) failed, which this "
           "preregistration declared in advance as non-blocking; diagnosis in 24_04e")
CFAR_JA = ("事前登録の試験(G-clock2 の局ごとの確かめ (c) のうち、80 km より遠い局の部分が不合格。この部分は止める条件にしないと事前に決めてあった。記述は 24_04e)")
label_ok = PASS and (not bool(G["pass_hour"])) and n3 == 1         # 印の文は「地震 1 つだけの 1 時間」の時のためのもの
if PASS:
    print(f"{TAG} 結果に付ける印(本人が記録に付ける。スクリプトは G-clock2 を読まない。正式な文は変更の記録 01 の 4 節):")
    if label_ok:
        print(f"   英語: \"{LABEL_EN}\"")
        print(f"   日本語:「{LABEL_JA}」")
    else:
        print(f"   (d) の FAIL が地震 1 つだけの 1 時間ではない(元の (d) が PASS か、(d3) の時間が {n3})ので、印の文は出さない。出力を貼って知らせる")
    if c_far_label:
        print(f"{TAG} さらに 5.3 節の 4 の (c-far) の印も付ける:")
        print(f"   英語: \"{CFAR_EN}\"")
        print(f"   日本語:「{CFAR_JA}」")

# ---- 4. 出力
(BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
json.dump(dict(script="24_04h_nagano2014_gclock2_amend01.py", version="v1", script_sha256=SELF_SHA,
               purpose="G-clock2 decision under amendment 01 of preregistration 24 (condition (d) only); no location or method error computed",
               inputs=dict(cache=str(cp), cache_sha256=sha_c, gclock_json=str(gp), gclock_json_sha256=sha_g, station_csv=str(sp), station_csv_sha256=sha_s),
               rule=dict(vp_kms=VP, min_n=MIN_N, tol_hour_s=TOL_HOUR, window_h=WIN_H, near_km=NEAR_KM, tol_station_near_s=TOL_STA_NEAR,
                         d1="|hour median - all median| <= tol_hour_s", d2="else, if the hour holds >= 2 events with P picks: fail",
                         d3="else (one event): at the same stations, other events in [-window_h, 0) and in [0, +window_h] separately; "
                            "on each side n >= min_n and |median of (residual - station median)| <= tol_hour_s"),
               median_all_s=MED, n_picks=len(R), hours=HJ,
               pass_all=pa, pass_day=pb, pass_station_original=pc, pass_c_near=c_near, c_far_label=c_far_label, n_near_stations=len(near),
               max_abs_dev_near_s=max((abs(x["dev_s"]) for x in near), default=None),
               pass_hour_original=bool(G["pass_hour"]), pass_hour_amend01=pd_amend, pass_events=pe, events_found=ev_find,
               pass_measured_frac=pf_, gclock2_pass_amend01=PASS, label_en=(LABEL_EN if label_ok else None),
               label_cfar_en=(CFAR_EN if PASS and c_far_label else None)),
          open(BASE / "data" / "24_04h_gclock2_amend01.json", "w"), indent=1)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
fig, axs = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw=dict(width_ratios=[1.6, 1.0]))
ax = axs[0]
for sel, c, mk, lab in ((lambda o: o["n_events"] >= 2, "tab:blue", "o", "Hours with two or more events"),
                        (lambda o: o["n_events"] == 1, "tab:orange", "o", "Hours with one event")):
    v = [o for o in HJ if sel(o)]
    if v: ax.scatter([datetime.strptime(o["hour"], "%Y-%m-%d %H") for o in v], [o["dev_s"] for o in v], s=14, color=c, marker=mk, label=f"{lab} ({len(v)})")
v2 = [o for o in HJ if o["rule"] == "d2"]
if v2: ax.scatter([datetime.strptime(o["hour"], "%Y-%m-%d %H") for o in v2], [o["dev_s"] for o in v2], s=80, marker="s", facecolors="none",
                  edgecolors="k", linewidths=1.2, label="Two or more events beyond the allowance (d2, fail)")
v3 = [o for o in HJ if o["rule"] == "d3"]
if v3: ax.scatter([datetime.strptime(o["hour"], "%Y-%m-%d %H") for o in v3], [o["dev_s"] for o in v3], s=80, facecolors="none",
                  edgecolors="tab:red", linewidths=1.2, label="Re-checked with the same stations (d3)")
ax.axhspan(-TOL_HOUR, TOL_HOUR, color="tab:green", alpha=0.12, label=f"Hourly allowance (+/- {TOL_HOUR} s)")
ax.set_xlabel("JST (2014)"); ax.set_ylabel("Hour median residual - median of all picks (s)")
ax.set_title(f"(a) Hourly check, {len(HJ)} hours with >= {MIN_N} picks", fontsize=9); ax.grid(alpha=0.3); ax.tick_params(axis="x", labelrotation=30, labelsize=7)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=2, frameon=False, fontsize=8)
ax = axs[1]
if v3:
    x_ = np.arange(len(v3))
    ax.bar(x_ - 0.27, [o["event_sta_rel_median_s"] for o in v3], width=0.27, color="tab:orange", label="The single event: median of (residual - station median)")
    for side, dx, col, lab in (("before", 0.0, "tab:blue", f"Other events, previous {WIN_H:.0f} h"), ("after", 0.27, "tab:cyan", f"Other events, next {WIN_H:.0f} h")):
        first = True
        for i, o in enumerate(v3):
            m, n_ = o[f"{side}_median_s"], o[f"{side}_n"]
            if n_ >= MIN_N:
                ax.bar(x_[i] + dx, m, width=0.27, color=col, label=(f"{lab}: median of (residual - station median)" if first else None)); first = False
                ok_ = abs(m) <= TOL_HOUR
            else:
                ok_ = False
            ax.text(x_[i] + dx, 0.02 if (n_ < MIN_N or m < 0) else m + 0.02, f"n={n_}\n{'pass' if ok_ else 'fail'}", ha="center", va="bottom", fontsize=6)
    ax.set_xticks(x_); ax.set_xticklabels([o["hour"] for o in v3], rotation=30, fontsize=7)
    ax.axhline(0, color="k", lw=0.8)
    vals = [o["event_sta_rel_median_s"] for o in v3] + [o[f"{sd}_median_s"] for o in v3 for sd in ("before", "after") if o[f"{sd}_median_s"] is not None]
    ax.set_ylim(min(-TOL_HOUR - 0.1, min(vals) - 0.1), max(TOL_HOUR + 0.1, max(vals)) + 0.35)
else:
    ax.text(0.5, 0.75, "No hour needed the re-check", ha="center", va="center", transform=ax.transAxes); ax.set_xticks([])
ax.axhspan(-TOL_HOUR, TOL_HOUR, color="tab:green", alpha=0.12, label=f"Allowance (+/- {TOL_HOUR} s)")
ax.set_ylabel("Offset (s)"); ax.set_title(f"(b) Re-check (d3). G-clock2 under amendment 01: {pf(PASS)}", fontsize=9); ax.grid(alpha=0.3)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=1, frameon=False, fontsize=8)
fig.suptitle("Northern Nagano 2014, G-clock2 hourly condition under amendment 01 (no location computed)", fontsize=10)
fig.tight_layout(); fig.savefig(BASE / "PDF" / "24_04h_gclock2_amend01.pdf", bbox_inches="tight"); plt.close(fig)
print(f"\n{TAG} 出力: {BASE / 'data' / '24_04h_gclock2_amend01.json'}、{BASE / 'PDF' / '24_04h_gclock2_amend01.pdf'}")
if not PASS:
    sys.exit(f"{TAG} STOP(G-clock2・変更の記録 01): 不合格。事前登録 24 の 5.3 節の 2 のとおり止め、clock could not be verified と報告する"
             "(これ以上の変更はしない。この出力を貼る)")
