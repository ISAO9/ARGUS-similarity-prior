#!/usr/bin/env python3
# =============================================================================
# Script : 25_04z_gclock2_test_period_block_dev.py  (v1)
#          [事前登録 25(島根県西部 2018)の G-clock2 (d) の作り直しの 3 回目の dev。25_04y の「続いた K 地震」を、試験の地震を取る
#           期間(本震 + 72 h より後)だけで見る形を、既に結果の出た系列のキャッシュで試す。あわせて、外れた地震がいつ起きたかを出す。
#           島根のデータは一つも読まない。位置の計算はしない]
# Project: ARGUS(新生)— 事前登録 25 の準備(規則を凍結する前の dev)
#
# なぜ 3 回目か(2 回目 25_04y v1 SHA-256 8c7f891c… の結果。2026-11-17、4 系列):
#   続いた K 地震(K = 2・3・4、地震ごとの中央値の中央値)は、4 系列の全ての K で、元のキャッシュで FAIL した。
#   最も外れた窓の始まり(JST): 長野 2014-11-22 23:07・11-23 12:47、鳥取 2026-01-06 10:26〜10:48、大阪 2018-06-18 08:04〜08:07、
#   鳥取中部 2016-10-21 15:11・23:58。どれも本震から十数時間以内で、続いた 2〜3 地震の P がまとめて数 s〜十数 s 外れていた。
#   大阪(_a04)と長野(_r1)のキャッシュは、既に R1(発生の 15 s 前〜5 s 後に別の地震がある地震を除く)を当てたものなので、
#   気象庁の一覧にある地震との重なりでは説明できない(本震直後の一覧に載らない地震や本震のコーダを拾ったと考えられる。この dev で
#   「本震からの時間」を出して確かめる)。陰性対照の割合 1.000 は、元のキャッシュが既に FAIL なので、足す前から決まっていた値。
#   25_04y の作りは捨てる(事前登録 25 で開示する)。
#
# 新しい (d)(案。この dev の後に事前登録 25 で凍結する):
#   0. 見る地震: 本震(キャッシュで Mj 最大)の発生から 72 h より後の地震だけ(試験の候補を取る期間と同じ。24 の POOL_H = 72 h)。
#      理由: (d) が守るのは試験の地震の時刻。本震直後の数十時間は、一覧に載らない地震が多く、検測の取り違えが続いて起き、
#      全ての局に同じだけ乗るずれと見分けられない(25_04y)。その期間の地震は試験に使わない。
#   1. 残り r = P の時刻 − 震源距離 / 6.0 km/s(24_04d と同じ。PhaseNet の P、p_fallback = 0)。0 の地震の全ての検測の中央値 M を引く。
#   2. 0 の地震を発生時刻の順に並べ、続いた K 個の地震ごとに、地震ごとの検測の中央値の中央値 − M を出す。
#      その K 地震の検測が合わせて 20 以上の時だけ判定する。
#   3. 全ての判定した窓で |値| ≤ 0.5 s なら合格。判定した窓が 1 つも無ければ合格としない。
#   考え方: K ≥ 3 の中央値の中央値は、1 地震だけの外れ(大きさによらない)では、他の地震が正常なら動かない。
#   限界: 区切り(約 2 時間)に地震が 1 つしかない時の組み立ての誤りは、その 1 地震の誤差と見分けられない(元の (d) と同じ)。
#         本震 + 72 h までの地震の時刻は (d) では見ない(事前登録 25 で書く)。
#
# K の選び方(この dev を回す前に決めた。回した後に変えない):
#   K ∈ {3, 4, 5} のうち、次を全て満たす最小の K を事前登録 25 で使う(K = 2 は 2 つの中央値の平均になり、1 地震 ±3 s で必ず外れるので外した)。
#   (i)  4 系列の元のキャッシュで全て合格。
#   (ii) 陰性対照(0 の地震の 1 つの全ての局に ±1・±3・±10 s のどれか。全ての地震について 1 つずつ): FAIL になった割合が、
#        6 つのずれのどれでも、4 系列の全てで 0.01 以下。
#   (iii)陽性対照(続いた 4 地震の全ての局に +0.6 s。全ての始まりについて): 見つけた割合が 4 系列の全てで 0.95 以上。
#   --cache に書いた系列が 1 つでも読めない時は K を選ばない。どの K も満たさなければ、満たさなかった項目を貼って作りを見直す。
#   記述(判定には使わない): 本震からの時間と外れた地震の一覧(全ての期間、|地震の中央値 − M| の大きい順に 10)、全ての期間で見た同じ K の値、
#   元の (d)(1 時間ごと・本震 + 72 h より後)、続いた 1・2・3・4 地震に +0.6 s を足した時に見つけた割合、窓の長さ。
#
# Usage(Colab。25_04y と同じノートで回せる。セルは 25_04z_COLAB_JA.md の Z1・Z2):
#   !python /content/drive/MyDrive/ARGUS/src/25_04z_gclock2_test_period_block_dev.py --cache 名前=場所 ... --out /content/drive/MyDrive/ARGUS/data/25_04z
# 出力  : <out>/25_04z_gclock2_test_period_block_dev.json / .pdf。(i)〜(iii) を満たす K が無ければ exit code 1。
# =============================================================================
import sys, json, argparse, hashlib
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

ap = argparse.ArgumentParser(description="25_04z: 新しい G-clock2 (d)(本震 + 72 h より後の続いた K 地震ごと)の dev。既に結果の出た系列のキャッシュだけを読む")
ap.add_argument("--cache", action="append", default=[], help="名前=キャッシュの場所(.pt)。何度でも")
ap.add_argument("--out", default="", help="出力の置き場所")
ap.add_argument("--selftest", action="store_true")
a = ap.parse_args()
VP, MIN_N, TOL = 6.0, 20, 0.5
KS = (3, 4, 5)
POOL_H = 72.0
NEG_SHIFTS, POS_SHIFT, POS_LEN = (1.0, -1.0, 3.0, -3.0, 10.0, -10.0), 0.6, 4
NEG_MAX_RATE, POS_MIN_RATE = 0.01, 0.95
TAG = "[25_04z]"

def jst_sec(ot):                                                 # 24_04d と同じ: 秒で切って 9 時間を足す
    t = datetime.strptime(str(ot).replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
    return t + timedelta(hours=9)

def load_picks(EV):
    """24_04d と同じ残り。戻り値: 地震ごとの (発生時刻, 地震の番号, 残りの配列) を発生時刻の順に"""
    out = []
    for ie, e in enumerate(EV):
        n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
        loc = np.asarray(e["sta_locs"], float)[:n]
        if "dist_km" in e: d = np.asarray(e["dist_km"], float)[:n]
        else:
            sl = np.asarray(e["src_loc"], float)
            epi = 111.19 * np.hypot(loc[:, 0] - sl[0], (loc[:, 1] - sl[1]) * np.cos(np.radians(sl[0]))); d = np.hypot(epi, sl[2])
        ok = (pf == 0) & np.isfinite(tp) & np.isfinite(d)
        if ok.any(): out.append((jst_sec(e["origin_time"]), ie, tp[ok] - d[ok] / VP, float(e["mw"])))
    out.sort(key=lambda x: (x[0], x[1]))
    return [(t, ie, r) for t, ie, r, _ in out], {ie: m for _, ie, _, m in out}

def judged_period(evs_all, t_main):
    """本震 + 72 h より後(ちょうど 72 h は含めない)の地震だけ"""
    return [x for x in evs_all if (x[0] - t_main).total_seconds() > POOL_H * 3600]

def wstat(rs, pooled=False):
    """窓の値: 地震ごとの中央値の中央値(pooled=True なら全ての検測をまとめた中央値)。検測が合わせて 20 未満なら None"""
    if sum(len(r) for r in rs) < MIN_N: return None
    if pooled: return float(np.median(np.concatenate(rs)))
    return float(np.median([np.median(r) for r in rs]))

def block_check(evs, K, M, pooled=False):
    """続いた K 地震ごとの |値 − M| の最大。戻り値 (最大, その窓の始まり, 窓の数)"""
    mx, at, nw = 0.0, None, 0
    for j in range(0, len(evs) - K + 1):
        w = wstat([evs[j + i][2] for i in range(K)], pooled)
        if w is None: continue
        v = w - M; nw += 1
        if abs(v) > abs(mx): mx, at = v, evs[j][0]
    return mx, at, nw

def window_spans_h(evs, K):
    return np.array([(evs[j + K - 1][0] - evs[j][0]).total_seconds() / 3600 for j in range(0, len(evs) - K + 1)
                     if sum(len(evs[j + i][2]) for i in range(K)) >= MIN_N])

def hourly(evs, M, multi_only=False):
    H = {}
    for t, ie, r in evs: H.setdefault(f"{t:%Y-%m-%d %H}", []).append((ie, r))
    v = []
    for h, xs in H.items():
        rr = np.concatenate([r for _, r in xs])
        if len(rr) < MIN_N or (multi_only and len(xs) < 2): continue
        v.append((abs(float(np.median(rr)) - M), h))
    return (max(v) if v else (None, None)), len(v)

def shifted_events(evs, idx, ds):
    return [(t, ie, (r + ds) if j in idx else r) for j, (t, ie, r) in enumerate(evs)]

def window_values(evs, K, M):
    """続いた K 地震の窓ごとの値(中央値 − M)。検測 20 未満の窓は NaN"""
    v = np.full(max(0, len(evs) - K + 1), np.nan)
    for j in range(len(v)):
        w = wstat([evs[j + i][2] for i in range(K)])
        if w is not None: v[j] = w - M
    return v

def max_with_shift(evs, K, M, base, S, ds):
    """地震の集合 S に ds を足した時の、全ての窓の |値| の最大(S に掛かる窓だけを計算し直す)"""
    lo, hi = max(0, min(S) - K + 1), min(len(base) - 1, max(S))
    outside = np.concatenate([base[:lo], base[hi + 1:]])
    m = float(np.nanmax(np.abs(outside))) if outside.size and np.isfinite(outside).any() else 0.0
    for j in range(lo, hi + 1):
        w = wstat([evs[j + i][2] + (ds if (j + i) in S else 0.0) for i in range(K)])
        if w is not None: m = max(m, abs(w - M))
    return m

def rates(evs, K, M):
    """陰性対照: 1 地震ずつ ±1・±3・±10 s → FAIL の割合(6 つのうち最大を判定に使う)。陽性対照: 続いた POS_LEN 地震に +0.6 s(全ての始まり)→ 見つけた割合。
    M は元のキャッシュの全体の中央値のまま(POS_LEN 地震は全体のごく一部なので、M の動きは小さい)"""
    base = window_values(evs, K, M)
    if not base.size or not np.isfinite(base).any():
        return dict(neg_fail_rate=None, neg_fail_rate_by_shift={}, n_neg=len(evs), pos_detect_rate=None, n_pos=0, detect_by_run_length={})
    by = {}
    for ds in NEG_SHIFTS:
        by[f"{ds:+g}"] = sum(max_with_shift(evs, K, M, base, {j}, ds) > TOL for j in range(len(evs))) / len(evs)
    def det(L):
        tot = max(0, len(evs) - L + 1)
        return (sum(max_with_shift(evs, K, M, base, set(range(j, j + L)), POS_SHIFT) > TOL for j in range(tot)) / tot) if tot else None, tot
    pos, pos_tot = det(POS_LEN)
    runs = {str(L): det(L)[0] for L in (1, 2, 3, 4)}
    return dict(neg_fail_rate=max(by.values()), neg_fail_rate_by_shift=by, n_neg=len(evs), pos_detect_rate=pos, n_pos=pos_tot,
                detect_by_run_length=runs)

def selftest():
    def check(c, m):
        if not c: sys.exit(f"{TAG} STOP: selftest に失敗: {m}")
    rng = np.random.default_rng(1)
    t0 = datetime(2018, 4, 12)
    evs = [(t0 + timedelta(minutes=40 * j), j, 0.3 + rng.normal(0, 0.15, 24)) for j in range(120)]
    M = float(np.median(np.concatenate([r for _, _, r in evs])))
    for K in KS: check(abs(block_check(evs, K, M)[0]) <= TOL, f"正常は合格 K={K}")
    check(abs(block_check(shifted_events(evs, {50}, 1.0), 3, M)[0]) <= TOL, "1 地震の全局 +1.0 s は K=3 で合格")
    big = [(t, ie, (np.concatenate([r, 0.3 + rng.normal(0, 0.15, 36)]) if ie == 50 else r[:5])) for t, ie, r in evs]   # 検測の多い 1 地震
    check(abs(block_check(shifted_events(big, {50}, 1.0), 3, M)[0]) <= TOL, "検測の多い 1 地震 +1.0 s も K=3 で合格(地震ごとの中央値の中央値)")
    check(abs(block_check(shifted_events(big, {50}, 1.0), 3, M, pooled=True)[0]) > TOL, "まとめた中央値なら不合格(違いの確かめ)")
    check(abs(block_check(shifted_events(evs, {50}, 1.0), 1, M)[0]) > TOL, "K=1(元の 1 時間・地震 1 つと同じ)では不合格")
    check(abs(block_check(shifted_events(evs, {50, 51, 52, 53}, 0.6), 3, M)[0]) > TOL, "続いた 4 地震 +0.6 s は K=3 で不合格")
    r = rates(evs, 3, M)
    check(r["neg_fail_rate"] <= NEG_MAX_RATE and r["pos_detect_rate"] >= POS_MIN_RATE, f"割合 {r}")
    base = window_values(evs, 3, M)
    for S in ({0}, {50}, {118, 119}, {10, 11, 12, 13}, {3, 4}):
        check(abs(max_with_shift(evs, 3, M, base, S, 0.7) - abs(block_check(shifted_events(evs, S, 0.7), 3, M)[0])) < 1e-12, f"速い計算と同じ {S}")
    few = [(t, ie, rr[:3]) for t, ie, rr in evs]                  # 1 地震 3 検測: K 地震を合わせても 20 未満の窓は判定しない
    check(block_check(few, 3, M)[2] == 0 and block_check(few, 4, M)[2] == 0, "検測 20 未満の窓は判定しない")
    tm = t0 - timedelta(hours=72) + timedelta(minutes=40 * 5)       # 6 つ目(40 分 × 5)がちょうど 72 h: 0〜5 番目は除き、6 番目から残す
    kept = judged_period(evs, tm)
    check(len(kept) == 114 and kept[0][1] == 6, f"本震 + 72 h の切り方(ちょうど 72 h は除く) {len(kept)}")
    EVm = [dict(n_real_stations=2, tp_times=[5.0, 7.0], p_fallback=[0, 1], sta_locs=[[35.0, 132.0], [35.1, 132.1]], dist_km=[30.0, 40.0],
                origin_time="2018-04-08 16:32:30.81", mw=6.1)]
    ev1, mj1 = load_picks(EVm)
    check(len(ev1) == 1 and abs(ev1[0][2][0] - 0.0) < 1e-12 and ev1[0][0] == datetime(2018, 4, 9, 1, 32, 30) and mj1[0] == 6.1,
          "残り・p_fallback・JST・Mj の読み方")
    print(f"{TAG} selftest: 正常・陰性対照・陽性対照・K=1 との違い・検測の多い 1 地震・まとめた中央値との違い・割合・速い計算と総当たりの一致・検測 20 未満・72 h の切り方・読み方の 11 例に合格")

selftest()
if a.selftest: sys.exit(0)
import torch
if not a.cache: sys.exit(f"{TAG} STOP: --cache が 1 つも無い")
OUT = Path(a.out) if a.out else Path(".")
OUT.mkdir(parents=True, exist_ok=True)
print(f"{TAG} 本スクリプト v1 SHA-256 {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}")
RES = {}; SKIP = []
for spec in a.cache:
    if "=" not in spec: sys.exit(f"{TAG} STOP: --cache は 名前=場所 の形({spec})")
    name, path = spec.split("=", 1); p = Path(path)
    if not p.exists():
        print(f"\n{TAG} {name}: {p} が無いので飛ばす(K は選ばない)"); SKIP.append(name); continue
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    EV = torch.load(p, weights_only=False); evs_all, MJ = load_picks(EV)
    im = int(np.argmax([float(e["mw"]) for e in EV])); t_main = jst_sec(EV[im]["origin_time"])
    evs = judged_period(evs_all, t_main)
    if not evs:
        print(f"\n{TAG} {name}: 本震 + {POOL_H:g} h より後に P を測った地震が無いので飛ばす(K は選ばない)"); SKIP.append(name); continue
    allr = np.concatenate([r for _, _, r in evs]); M = float(np.median(allr))
    f = lambda x: "—" if x is None else f"{x:.3f}"
    print(f"\n{TAG} ===== {name}: {p.name}  SHA-256 {sha[:12]}…  地震 {len(EV)}(P を測った地震 {len(evs_all)})  本震 {t_main:%Y-%m-%d %H:%M:%S} JST・Mj {float(EV[im]['mw']):.1f}")
    print(f"{TAG} {name}: 見る地震(本震 + {POOL_H:g} h より後){len(evs)}・検測 {len(allr)}  その中央値 M {M:+.3f} s")
    Ma = float(np.median(np.concatenate([r for _, _, r in evs_all])))
    top = sorted(evs_all, key=lambda x: -abs(float(np.median(x[2])) - Ma))[:10]
    print(f"{TAG} {name}: 記述 外れた地震(全ての期間・|地震の中央値 − 全ての期間の中央値 {Ma:+.3f}| の大きい順に 10。本震からの時間・Mj・検測の数): " +
          "  ".join(f"{float(np.median(r)) - Ma:+.2f} s({(t - t_main).total_seconds() / 3600:.1f} h, Mj {MJ[ie]:.1f}, n={len(r)})" for t, ie, r in top))
    (ho, hh), nh = hourly(evs, M); (hm, hhm), nhm = hourly(evs, M, multi_only=True)
    print(f"{TAG} {name}: 参考 元の (d) 1 時間ごと(本震 + {POOL_H:g} h より後): {nh} 時間・最大 {f(ho)} s({hh})   地震 2 つ以上の 1 時間だけ: {nhm} 時間・最大 {f(hm)} s({hhm})")
    R = dict(cache=str(p), cache_sha256=sha, n_events=len(EV), n_events_with_p=len(evs_all), mainshock_jst=f"{t_main:%Y-%m-%d %H:%M:%S}",
             mainshock_mj=float(EV[im]["mw"]), n_events_judged_period=len(evs), n_picks=int(len(allr)), median_judged_period_s=M,
             top_outlier_events_all_period=[dict(dev_s=float(np.median(r)) - Ma, hours_after_main=(t - t_main).total_seconds() / 3600, mj=MJ[ie], n=len(r),
                                                 origin_jst=f"{t:%Y-%m-%d %H:%M:%S}") for t, ie, r in top],
             hourly=dict(n_hours=nh, max_abs_s=ho, worst_hour=hh), hourly_multi_event=dict(n_hours=nhm, max_abs_s=hm, worst_hour=hhm), by_K={})
    for K in KS:
        mx, at, nw = block_check(evs, K, M); rr = rates(evs, K, M)
        mxp = block_check(evs, K, M, pooled=True)[0]; sp = window_spans_h(evs, K)
        mxa, ata, _ = block_check(evs_all, K, Ma)
        ok = abs(mx) <= TOL and nw > 0
        R["by_K"][str(K)] = dict(max_abs_s=abs(mx), worst_value_s=mx, worst_window_start_jst=(None if at is None else f"{at:%Y-%m-%d %H:%M}"),
                                 n_windows=nw, pass_original=bool(ok), pooled_max_abs_s=abs(mxp), all_period_max_abs_s=abs(mxa),
                                 all_period_worst_window_start_jst=(None if ata is None else f"{ata:%Y-%m-%d %H:%M}"),
                                 window_span_h=dict(median=(float(np.median(sp)) if sp.size else None), p90=(float(np.percentile(sp, 90)) if sp.size else None),
                                                    share_over_2h=(float(np.mean(sp > 2.0)) if sp.size else None)), **rr)
        x = R["by_K"][str(K)]
        print(f"{TAG} {name}: K={K}: 窓 {nw}・最大 |地震ごとの中央値の中央値 − 全体| {abs(mx):.3f} s({'—' if at is None else f'{at:%Y-%m-%d %H:%M}'} からの窓)→ "
              f"{'PASS' if ok else 'FAIL'}(参考: まとめた中央値なら {abs(mxp):.3f} s。全ての期間で見ると {abs(mxa):.3f} s、"
              f"{'—' if ata is None else f'{ata:%Y-%m-%d %H:%M}'} からの窓)")
        print(f"{TAG} {name}: K={K}:   陰性対照(1 地震ずつ)FAIL の割合 最大 {f(rr['neg_fail_rate'])}(" +
              "  ".join(f"{k} s: {v:.3f}" for k, v in rr["neg_fail_rate_by_shift"].items()) + f"。{rr['n_neg']} 地震)")
        print(f"{TAG} {name}: K={K}:   陽性対照(続いた {POS_LEN} 地震 +{POS_SHIFT} s)見つけた割合 {f(rr['pos_detect_rate'])}({rr['n_pos']} 回)   "
              f"記述: 続いた 1・2・3・4 地震 " + " / ".join(f(v) for v in rr["detect_by_run_length"].values()) +
              f"   窓の長さ 中央値 {f(x['window_span_h']['median'])} h・90% {f(x['window_span_h']['p90'])} h・2 h を超える割合 {f(x['window_span_h']['share_over_2h'])}")
    RES[name] = R
if not RES: sys.exit(f"{TAG} STOP: 読めたキャッシュが 0")
chosen = None; why = {}
for K in KS:
    bad = [f"{n}: 読めなかった" for n in SKIP]
    for name, R in RES.items():
        x = R["by_K"][str(K)]
        if not x["pass_original"]: bad.append(f"{name}: (i) 元のキャッシュで FAIL")
        if x["neg_fail_rate"] is None or x["neg_fail_rate"] > NEG_MAX_RATE: bad.append(f"{name}: (ii) 陰性対照 {x['neg_fail_rate']}")
        if x["pos_detect_rate"] is None or x["pos_detect_rate"] < POS_MIN_RATE: bad.append(f"{name}: (iii) 陽性対照 {x['pos_detect_rate']}")
    why[str(K)] = bad
    if not bad and chosen is None: chosen = K
print(f"\n{TAG} K ごとの満たさなかった項目: " + "  ".join(f"K={k}: {('なし' if not v else '; '.join(v))}" for k, v in why.items()))
print(f"{TAG} 選んだ K(事前に決めた規則: (i)〜(iii) を満たす最小の K): {chosen if chosen else 'なし(作りを見直す)'}")
json.dump(dict(script="25_04z_gclock2_test_period_block_dev.py", version="v1", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               purpose="third dev of the new G-clock2 condition (d) for preregistration 25 (K consecutive events after mainshock + 72 h, median of event medians); "
                       "caches of sequences already tested or stopped only; no Shimane data; no location or method error",
               rule=dict(vp_kms=VP, min_n=MIN_N, tol_s=TOL, ks=list(KS), judged_period="origin > mainshock (max Mj in cache) + 72 h", window_value="median of per-event medians", neg_shifts_s=list(NEG_SHIFTS),
                         pos_shift_s=POS_SHIFT, pos_len_events=POS_LEN,
                         neg_max_rate=NEG_MAX_RATE, pos_min_rate=POS_MIN_RATE),
               results=RES, unmet_by_K=why, chosen_K=chosen),
          open(OUT / "25_04z_gclock2_test_period_block_dev.json", "w"), indent=1, default=str)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
names = list(RES); x = np.arange(len(names)); bw = 0.2
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.bar(x - 1.5 * bw, [RES[k]["hourly"]["max_abs_s"] or 0 for k in names], bw, color="0.6", label="Original (d), after mainshock + 72 h: max hourly |median - all|")
for j, (K, col) in enumerate(zip(KS, ("tab:blue", "tab:green", "tab:purple"))):
    ax.bar(x + (j - 0.5) * bw, [RES[k]["by_K"][str(K)]["max_abs_s"] for k in names], bw, color=col, label=f"New (d), after mainshock + 72 h: K = {K} events (median of event medians)")
ax.axhline(TOL, color="k", ls="--", lw=1, label=f"Allowance ({TOL} s)")
ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylabel("Max |block value - median of all picks| (s)")
ax.set_title(f"G-clock2 condition (d) after mainshock + 72 h: hourly blocks vs K consecutive events (dev, earlier sequences). Chosen K: {chosen}", fontsize=9)
ax.grid(alpha=0.3, axis="y"); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(OUT / "25_04z_gclock2_test_period_block_dev.pdf", bbox_inches="tight"); plt.close(fig)
print(f"{TAG} 出力: {OUT / '25_04z_gclock2_test_period_block_dev.json'}、{OUT / '25_04z_gclock2_test_period_block_dev.pdf'}")
if chosen is None: sys.exit(f"{TAG} (i)〜(iii) を満たす K が無い(この出力を貼る。作りを見直す)")
