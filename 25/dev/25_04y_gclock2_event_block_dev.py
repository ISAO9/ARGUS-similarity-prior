#!/usr/bin/env python3
# =============================================================================
# Script : 25_04y_gclock2_event_block_dev.py  (v1)
#          [事前登録 25(島根県西部 2018)の G-clock2 (d) の作り直しの 2 回目の dev。「日本時間の 1 時間ごと」の代わりに
#           「時刻の順で続いた K 個の地震ごと」に全ての局の P の残りをまとめて見る形を、既に結果の出た系列のキャッシュで試す。
#           島根のデータは一つも読まない。位置の計算はしない]
# Project: ARGUS(新生)— 事前登録 25 の準備(規則を凍結する前の dev)
#
# なぜ 2 回目か(1 回目 25_04x の結果。2026-11-17、4 系列):
#   1 回目の「局ごとに続いた 10 検測の窓」は、4 系列の全てで、時計が正常なはずの元のキャッシュで FAIL した
#   (最大の |窓の中央値 − 窓の外の中央値|: 長野 2014 5.055 s・鳥取県西部 2026 10.036 s・大阪 2018 1.195 s・鳥取県中部 2016 12.854 s)。
#   どれも余震の多い時期の局ごとの検測の取り違え(数 s〜十数 s)が続けて並んだもので、時計のずれではない。局ごとに見ると、
#   検測の取り違えが時間の上でまとまって起きる所を時計と見分けられない。1 回目の作りは捨てる(事前登録 25 で開示する)。
#
# (d) が見つけたいもの(元の 21_04d・24_04d の考え方に戻る):
#   波形を組み立てる時の時刻の誤り(24_02 の区切り(1 つ約 2 時間)ごとの、全ての局に同じだけ乗るずれ。鳥取 2026 の h5 で実際に
#   9 時間のずれがあった種類)。局ごとの時計のずれは (c)(局ごと・1.0 s)が見る。
#   元の (d) は「1 時間」でまとめたので、地震が 1 つしかない時間では、その 1 地震の検測の質や気象庁の発生時刻の誤差で外れた(長野 2014)。
#
# 新しい (d)(案。この dev の後に事前登録 25 で凍結する):
#   1. 残り r = P の時刻 − 震源距離 / 6.0 km/s(24_04d と同じ。PhaseNet の P、p_fallback = 0)。全体の中央値 M を引く。
#   2. P を測った地震を発生時刻の順に並べ、続いた K 個の地震(1 つずつずらす)ごとに、地震ごとの検測の中央値を出し、
#      その K 個の中央値の中央値 − M を出す(地震ごとの中央値の中央値にするのは、検測の多い 1 地震が窓を決めてしまわないため)。
#      その K 地震の検測が合わせて 20 以上の時だけ判定する(元の (d) の「検測 20 以上の時間」と同じ数)。
#      参考に、K 地震の全ての検測をまとめた中央値 − M も出す(判定には使わない)。
#   3. 全ての判定した窓で |値| ≤ 0.5 s なら合格(閾値は元の (d) と同じ)。
#   考え方: 組み立ての時刻の誤りは、同じ区切りの中の続いた地震の全ての局に同じだけ乗る。K ≥ 3 の地震ごとの中央値の中央値は、
#   そのうちの 1 地震だけの検測の取り違えや発生時刻の誤差では、ずれの大きさによらず動かない。
#   (i) は、判定した窓が 1 つ以上あることも求める。M は対照でずれを足しても全体の中央値のまま(足す前の値)にする。
#   --cache に書いた系列が 1 つでも読めない時は K を選ばない。
#   限界: 区切りの中に地震が 1 つしかない時の組み立ての誤りは、その 1 地震の誤差と見分けられない(元の (d) と同じ)。2 つの時は一部だけ
#   見える。静かな時期には K 地震の窓が 2 時間(区切り 1 つ)より長くなり、区切り 1 つの誤りは薄まる(見逃しの側。窓の長さを記述で出す)。
#
# K の選び方(この dev を回す前に決めた。回した後に変えない):
#   K ∈ {2, 3, 4} のうち、次を全て満たす最小の K を事前登録 25 で使う。
#   (i)  4 系列の元のキャッシュで全て合格。
#   (ii) 陰性対照(1 地震の全ての局に ±1・±3・±10 s のどれか。全ての地震について 1 つずつ): FAIL になった割合が、6 つのずれの
#        どれでも、4 系列の全てで 0.01 以下(25_04x で見た取り違えは数 s〜十数 s だったので、大きさと向きを変えて見る)。
#   (iii)陽性対照(続いた 4 地震の全ての局に +0.6 s。全ての始まりについて): 見つけた割合が 4 系列の全てで 0.95 以上。
#   どの K も満たさなければ、満たさなかった項目を貼って、作りを見直す(この時も島根は開かない)。
#   参考に元の (d)(1 時間ごと)と、地震が 2 つ以上の 1 時間だけで見た (d) も並べる(判定には使わない)。
#   記述(判定には使わない): 続いた 1・2・3・4 地震に +0.6 s を足した時に見つけた割合、窓の長さ(時間)の分布と 2 時間を超える窓の割合。
#
# Usage(Colab。25_04x と同じノートで回せる。セルは 25_04y_COLAB_JA.md の Y1〜Y3):
#   !python /content/drive/MyDrive/ARGUS/src/25_04y_gclock2_event_block_dev.py --cache 名前=場所 ... --out /content/drive/MyDrive/ARGUS/data/25_04y
# 出力  : <out>/25_04y_gclock2_event_block_dev.json / .pdf。(i)〜(iii) を満たす K が無ければ exit code 1。
# =============================================================================
import sys, json, argparse, hashlib
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

ap = argparse.ArgumentParser(description="25_04y: 新しい G-clock2 (d)(続いた K 地震ごと)の dev。既に結果の出た系列のキャッシュだけを読む")
ap.add_argument("--cache", action="append", default=[], help="名前=キャッシュの場所(.pt)。何度でも")
ap.add_argument("--out", default="", help="出力の置き場所")
ap.add_argument("--selftest", action="store_true")
a = ap.parse_args()
VP, MIN_N, TOL = 6.0, 20, 0.5
KS = (2, 3, 4)
NEG_SHIFTS, POS_SHIFT, POS_LEN = (1.0, -1.0, 3.0, -3.0, 10.0, -10.0), 0.6, 4
NEG_MAX_RATE, POS_MIN_RATE = 0.01, 0.95
TAG = "[25_04y]"

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
        if ok.any(): out.append((jst_sec(e["origin_time"]), ie, tp[ok] - d[ok] / VP))
    out.sort(key=lambda x: (x[0], x[1]))
    return out

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
    print(f"{TAG} selftest: 正常・陰性対照・陽性対照・K=1 との違い・検測の多い 1 地震・まとめた中央値との違い・割合・速い計算と総当たりの一致・検測 20 未満の 9 例に合格")

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
    EV = torch.load(p, weights_only=False); evs = load_picks(EV)
    if not evs:
        print(f"\n{TAG} {name}: P を測った地震が無いので飛ばす(K は選ばない)"); SKIP.append(name); continue
    allr = np.concatenate([r for _, _, r in evs]); M = float(np.median(allr))
    print(f"\n{TAG} ===== {name}: {p.name}  SHA-256 {sha[:12]}…  地震 {len(EV)}(P を測った地震 {len(evs)})・検測 {len(allr)}  全体の中央値 {M:+.3f} s")
    (ho, hh), nh = hourly(evs, M); (hm, hhm), nhm = hourly(evs, M, multi_only=True)
    f = lambda x: "—" if x is None else f"{x:.3f}"
    print(f"{TAG} {name}: 参考 元の (d) 1 時間ごと: {nh} 時間・最大 {f(ho)} s({hh})   地震 2 つ以上の 1 時間だけ: {nhm} 時間・最大 {f(hm)} s({hhm})")
    R = dict(cache=str(p), cache_sha256=sha, n_events=len(EV), n_events_with_p=len(evs), n_picks=int(len(allr)), median_all_s=M,
             hourly=dict(n_hours=nh, max_abs_s=ho, worst_hour=hh), hourly_multi_event=dict(n_hours=nhm, max_abs_s=hm, worst_hour=hhm), by_K={})
    for K in KS:
        mx, at, nw = block_check(evs, K, M); rr = rates(evs, K, M)
        mxp = block_check(evs, K, M, pooled=True)[0]; sp = window_spans_h(evs, K)
        ok = abs(mx) <= TOL and nw > 0
        R["by_K"][str(K)] = dict(max_abs_s=abs(mx), worst_value_s=mx, worst_window_start_jst=(None if at is None else f"{at:%Y-%m-%d %H:%M}"),
                                 n_windows=nw, pass_original=bool(ok), pooled_max_abs_s=abs(mxp),
                                 window_span_h=dict(median=(float(np.median(sp)) if sp.size else None), p90=(float(np.percentile(sp, 90)) if sp.size else None),
                                                    share_over_2h=(float(np.mean(sp > 2.0)) if sp.size else None)), **rr)
        x = R["by_K"][str(K)]
        print(f"{TAG} {name}: K={K}: 窓 {nw}・最大 |地震ごとの中央値の中央値 − 全体| {abs(mx):.3f} s({'—' if at is None else f'{at:%Y-%m-%d %H:%M}'} からの窓)→ "
              f"{'PASS' if ok else 'FAIL'}(参考: まとめた中央値なら {abs(mxp):.3f} s)")
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
json.dump(dict(script="25_04y_gclock2_event_block_dev.py", version="v1", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               purpose="second dev of the new G-clock2 condition (d) for preregistration 25 (K consecutive events pooled over all stations); "
                       "caches of sequences already tested or stopped only; no Shimane data; no location or method error",
               rule=dict(vp_kms=VP, min_n=MIN_N, tol_s=TOL, ks=list(KS), window_value="median of per-event medians", neg_shifts_s=list(NEG_SHIFTS),
                         pos_shift_s=POS_SHIFT, pos_len_events=POS_LEN,
                         neg_max_rate=NEG_MAX_RATE, pos_min_rate=POS_MIN_RATE),
               results=RES, unmet_by_K=why, chosen_K=chosen),
          open(OUT / "25_04y_gclock2_event_block_dev.json", "w"), indent=1, default=str)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
names = list(RES); x = np.arange(len(names)); bw = 0.2
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.bar(x - 1.5 * bw, [RES[k]["hourly"]["max_abs_s"] or 0 for k in names], bw, color="0.6", label="Original (d): max hourly |median - all|")
for j, (K, col) in enumerate(zip(KS, ("tab:blue", "tab:green", "tab:purple"))):
    ax.bar(x + (j - 0.5) * bw, [RES[k]["by_K"][str(K)]["max_abs_s"] for k in names], bw, color=col, label=f"New (d): K = {K} events (median of event medians)")
ax.axhline(TOL, color="k", ls="--", lw=1, label=f"Allowance ({TOL} s)")
ax.set_xticks(x); ax.set_xticklabels(names); ax.set_ylabel("Max |block value - median of all picks| (s)")
ax.set_title(f"G-clock2 condition (d): hourly blocks vs blocks of K consecutive events (dev, earlier sequences). Chosen K: {chosen}", fontsize=9)
ax.grid(alpha=0.3, axis="y"); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(OUT / "25_04y_gclock2_event_block_dev.pdf", bbox_inches="tight"); plt.close(fig)
print(f"{TAG} 出力: {OUT / '25_04y_gclock2_event_block_dev.json'}、{OUT / '25_04y_gclock2_event_block_dev.pdf'}")
if chosen is None: sys.exit(f"{TAG} (i)〜(iii) を満たす K が無い(この出力を貼る。作りを見直す)")
