#!/usr/bin/env python3
# =============================================================================
# Script : 21_09b_sparse_summary.py  (v1)
#          [21_09a の 10 の網(間引かない + N = 12・8・5 局 × 種 3 つ)の結果を集め、事前に決めた分類
#           (SPARSE-HOLDS / SPARSE-PARTIAL / SPARSE-FAILS)を出し、残した局の数と誤差の関係の図を描く。新しい計算はしない]
# Project: ARGUS(新生)— 「局がまばらな網でこそ、似た過去の地震を足す価値が大きいか」
#
# 何をするか:
#   1. models/21_09_run_<網>.json を全て読む(--limit N を付けると、動作確認の _limitN の結果だけを読む。判定は出さない)。
#      判定を出す条件(全て満たす時だけ): 事前に決めた 10 の網が全て揃う・各 JSON の中身(tag・N・seed・limit = 0)がファイル名と合う・
#      全て同じキャッシュ(SHA-256)・全て同じ 21_09a(SHA-256)で、それが --expect-sha(事前登録の記録に書いた 21_09a の SHA-256)と同じ・
#      N = 0 の G-same が PASS・どの網の G-causal も FAIL でない。どの条件で判定を出さなかったかを JSON に残す。
#   2. 分類(21_09a の冒頭と同じ、事前に決めた規則): 各 N(12・8・5)で、τ = 2 s の C4 が BEST に勝った網の数
#      3/3 = HOLDS、1〜2/3 = MIXED、0/3 = FAILS(「試せない」網と BEST が床 0.5 km 未満の網は勝ちに数えず、数を別に出す)。
#      全体は 全て HOLDS → SPARSE-HOLDS、全て FAILS → SPARSE-FAILS、それ以外 → SPARSE-PARTIAL。C3(α 0.01)・他の τ・差の大きさは記述だけ。
#   3. 表: 網ごと・τ ごとに BEST(名前と中央値)・C3・C4 の中央値・差(BEST − C4)・p・床・局の数、まばらさ(局の数・最近接の間隔・
#      P を測れず外れた試験の地震・最初の P の局の震央距離・最初の P の発生からの時刻)。
#   4. 図(白背景・英語・凡例は枠外):
#      F1: τ = 0.5・1・2・3 s の 4 枚。横 = 残した局の数(対数、右ほど密)、縦 = 誤差の中央値(km、対数)。網ごとの点と、N ごとの中央値を
#          結ぶ線。BEST = 灰、C3 = 青、C4 = 朱(Okabe-Ito)。BEST = 波形の似方を使わない 9 方法の最良
#      F2: まばらさ: (a) 最初の P の発生からの時刻、(b) τ = 2 s で P のある局の数(中央値)、横 = 残した局の数
#
# Usage : cd ~/SWIFT && uv run python src/21_09b_sparse_summary.py --expect-sha <事前登録の記録に書いた 21_09a の SHA-256>
#         (動作確認の結果なら --limit 20。判定は出さない)
# Output: models/21_09_summary.json・PDF/21_09_F1_sparse_error.pdf・PDF/21_09_F2_sparseness.pdf(--limit なら _limitN 付き)
# =============================================================================
import json, argparse, hashlib, datetime as dt
from pathlib import Path
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int, default=0)
ap.add_argument("--expect-sha", default="", help="事前登録の記録に書いた 21_09a の SHA-256(判定に必須)")
a = ap.parse_args()
ROOT = Path(__file__).resolve().parent.parent
for d in ("models", "PDF"): (ROOT / d).mkdir(exist_ok=True)
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
SELF_SHA = sha256(Path(__file__))
print(f"[21_09b] 本スクリプト v1 SHA-256 {SELF_SHA[:12]}…")
CONFIGS = [(0, 0)] + [(N, s) for N in (12, 8, 5) for s in (0, 1, 2)]
def tag_of(N, s): return ("full" if N == 0 else f"N{N}_s{s}") + (f"_limit{a.limit}" if a.limit else "")
RUNS, missing, bad_content = {}, [], []
for N, s in CONFIGS:
    p = ROOT / f"models/21_09_run_{tag_of(N, s)}.json"
    if not p.exists(): missing.append(tag_of(N, s)); continue
    r = json.load(open(p)); RUNS[(N, s)] = r
    if r.get("tag") != tag_of(N, s) or r["network"].get("n_keep") != N or r["network"].get("seed") != s or r.get("limit") != a.limit:
        bad_content.append(tag_of(N, s))
if not RUNS: raise SystemExit("[21_09b] STOP: 21_09a の結果が 1 つも無い(先に 21_09a --all)")
shas = sorted({r["cache_sha256"] for r in RUNS.values()}); ssha = sorted({r["script_sha256"] for r in RUNS.values()})
full = RUNS.get((0, 0))
gs = ((full or {}).get("gates", {}).get("same") or {}).get("status")
causal = {r["tag"]: r["gates"]["causal"]["status"] for r in RUNS.values()}
GATES = dict(missing=missing, content_mismatch=bad_content, n_cache_sha=len(shas), n_script_sha=len(ssha),
             script_sha_matches_expected=(bool(a.expect_sha) and ssha == [a.expect_sha]), g_same=gs,
             g_causal_fail=[t for t, v in causal.items() if v.startswith("FAIL")], limit=a.limit)
complete = (not missing and not bad_content and len(shas) == 1 and GATES["script_sha_matches_expected"] and gs == "PASS"
            and not GATES["g_causal_fail"] and not a.limit)
print(f"[21_09b] 読んだ網 {len(RUNS)}/10" + (f"  足りない: {', '.join(missing)}" if missing else "") +
      f"  中身の不一致 {bad_content or 'なし'}  キャッシュの SHA-256 {len(shas)} 種・21_09a の SHA-256 {len(ssha)} 種"
      f"(事前登録と同じ: {GATES['script_sha_matches_expected']})  G-same {gs or '—'}  G-causal の FAIL {GATES['g_causal_fail'] or 'なし'}")
TL = ["0.5", "1", "2", "3"]
def f2(v): return "—" if v is None else f"{v:.2f}"
def fp(v): return "—" if v is None else f"{v:.2g}"
print("\n[21_09b] ===== 網ごとの誤差の中央値 km(BEST / C3 / C4、差 = BEST − C4) =====")
for (N, s), r in RUNS.items():
    nw, sp = r["network"], r["sparseness"]
    print(f"  {r['tag']:<12} 局 {nw['n_stations_kept']:>2}・間隔 {f2(nw['nn_spacing_median_km_kept'])} km・評価 {r['n_evaluated']} 地震"
          f"({'試せる' if r.get('testable') else '試せない'})・P を測れず外れた {sp.get('test_events_lost_no_p')}・"
          f"最初の P の局 {f2(sp['first_station_epi_km_median'])} km・最初の P は発生から {f2(sp['first_p_after_origin_s_median'])} s・G-causal {r['gates']['causal']['status']}")
    for t in TL:
        c3, c4 = r["per_tau"][t]["C3"], r["per_tau"][t]["C4"]
        if c4.get("best") is None: print(f"      τ={t}: BEST なし"); continue
        print(f"      τ={t:>3} s: BEST {c4['best']:<4} {f2(c4['best_median_km'])} / C3 {f2(c3['median_km'])} / C4 {f2(c4['median_km'])}  "
              f"差 {f2(c4['gain_km'])}  p(C4) {fp(c4['paired_vs_best']['p'])} {'勝ち' if c4['win'] else '—'}  "
              f"p(C3) {fp(c3['paired_vs_best']['p'])} {'勝ち' if c3['win'] else '—'}  床 {c4['floor']}  局 {f2(r['per_tau'][t]['stations_median'])}")
LEVEL = {}
for N in (12, 8, 5):
    rs = [RUNS[(N, s)] for s in (0, 1, 2) if (N, s) in RUNS]
    c4s = [r["per_tau"]["2"]["C4"] for r in rs]
    nw4 = sum(bool(c["win"]) for c in c4s); nw3 = sum(bool(r["per_tau"]["2"]["C3"]["win"]) for r in rs)
    cls = ("HOLDS" if nw4 == 3 else "MIXED" if nw4 >= 1 else "FAILS") if len(rs) == 3 else "INCOMPLETE"
    LEVEL[str(N)] = {"n_runs": len(rs), "c4_wins_t2": nw4, "c3_wins_t2": nw3, "class": cls,
                     "n_untestable": sum(not c.get("testable", False) for c in c4s), "n_floor_blocked_t2": sum(bool(c.get("floor")) for c in c4s),
                     "gain_t2_km": [c.get("gain_km") for c in c4s], "best_t2_km": [c.get("best_median_km") for c in c4s],
                     "c4_t2_km": [c.get("median_km") for c in c4s], "spacing_km": [r["network"]["nn_spacing_median_km_kept"] for r in rs]}
cl = [v["class"] for v in LEVEL.values()]
VERDICT = ("SPARSE-HOLDS" if all(c == "HOLDS" for c in cl) else "SPARSE-FAILS" if all(c == "FAILS" for c in cl)
           else "SPARSE-PARTIAL") if complete else "NO VERDICT (see gates)"
print("\n[21_09b] ===== 事前に決めた分類(τ = 2 s の C4 対 BEST、α 0.005) =====")
for N, v in LEVEL.items():
    g = ", ".join(f2(x) for x in v["gain_t2_km"]) or "—"
    print(f"  N = {N} 局: C4 の勝ち {v['c4_wins_t2']}/{v['n_runs']} → {v['class']}  (試せない {v['n_untestable']}・床 {v['n_floor_blocked_t2']}・"
          f"参考: C3 の勝ち {v['c3_wins_t2']}/{v['n_runs']})  差 BEST − C4 = {g} km")
REF = None
if full:
    c4 = full["per_tau"]["2"]["C4"]
    if c4.get("best") is None: print("  N = 0: BEST なし")
    else:
        REF = dict(best=c4["best"], best_km=c4["best_median_km"], c4_km=c4["median_km"], gain_km=c4["gain_km"])
        print(f"  N = 0(間引かない、21_04 と同じ): BEST {f2(c4['best_median_km'])} / C4 {f2(c4['median_km'])} km  差 {f2(c4['gain_km'])}")
print(f"[21_09b] 判定(事前に決めた分類): {VERDICT}" + ("" if complete else f"  ゲート: {GATES}"))
print("[21_09b] 限界: " + " / ".join(next(iter(RUNS.values()))["limits"][-6:]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 11, "axes.facecolor": "white", "figure.facecolor": "white", "savefig.facecolor": "white"})
COL = {"BEST": "#7F7F7F", "C3": "#0072B2", "C4": "#D55E00"}; MK = {"BEST": "o", "C3": "s", "C4": "D"}
LABEL = {"BEST": "Best method without waveform similarity (BEST)", "C3": "C3: physics × similar past events",
         "C4": "C3 + station corrections from similar events (C4)"}
SUF = f"_limit{a.limit}" if a.limit else ""
def xval(r): return r["network"]["n_stations_kept"]
fig, axs = plt.subplots(1, 4, figsize=(15, 4.6), sharey=True)
for ax, t in zip(axs, TL):
    for m in ("BEST", "C3", "C4"):
        xs, ys, lv = [], [], {}
        for (N, s), r in RUNS.items():
            d = r["per_tau"][t]["C4"] if m in ("BEST", "C4") else r["per_tau"][t]["C3"]
            v = d.get("best_median_km") if m == "BEST" else d.get("median_km")
            if v is None: print(f"[21_09b] 注意: {r['tag']} τ={t} {m} の値なし(図から外す)"); continue
            xs.append(xval(r)); ys.append(v); lv.setdefault(N, []).append((xval(r), v))
        ax.scatter(xs, ys, s=22, marker=MK[m], color=COL[m], alpha=0.55, zorder=3)
        L = sorted((np.median([p[0] for p in v]), np.median([p[1] for p in v])) for v in lv.values())
        if L: ax.plot([p[0] for p in L], [p[1] for p in L], "-", color=COL[m], marker=MK[m], lw=2, label=LABEL[m], zorder=4)
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_title(f"τ = {t} s after the first P"); ax.set_xlabel("Stations kept")
    ax.grid(alpha=0.3, which="both")
axs[0].set_ylabel("Median epicentral error vs JMA (km)")
h, l = axs[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.02))
fig.suptitle("Central Tottori 2016 test events on thinned Hi-net networks (points = runs; lines = median per network size)", y=0.99)
fig.tight_layout(rect=(0, 0.1, 1, 0.95)); fig.savefig(ROOT / f"PDF/21_09_F1_sparse_error{SUF}.pdf"); plt.close(fig)
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
for r in RUNS.values():
    axs[0].scatter(xval(r), r["sparseness"]["first_p_after_origin_s_median"], color="#000000", s=26)
    axs[1].scatter(xval(r), r["per_tau"]["2"]["stations_median"], color="#000000", s=26)
axs[0].set_ylabel("Median first-P time after origin (s)"); axs[1].set_ylabel("Median stations with P at τ = 2 s")
for ax, tl in zip(axs, ("(a) When the first P arrives", "(b) Stations available 2 s after the first P")):
    ax.set_xscale("log"); ax.set_xlabel("Stations kept"); ax.set_title(tl); ax.grid(alpha=0.3, which="both")
fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_09_F2_sparseness{SUF}.pdf"); plt.close(fig)
json.dump(dict(script="21_09b_sparse_summary.py", script_sha256=SELF_SHA, utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               expected_21_09a_sha256=a.expect_sha, runs_read=[r["tag"] for r in RUNS.values()], gates=GATES, complete=complete,
               run_script_sha256=ssha, cache_sha256=shas, causal_status=causal, reference_full=REF, levels=LEVEL, verdict=VERDICT,
               limits=next(iter(RUNS.values()))["limits"]),
          open(ROOT / f"models/21_09_summary{SUF}.json", "w"), indent=1)
print(f"[21_09b] 出力: models/21_09_summary{SUF}.json・PDF/21_09_F1_sparse_error{SUF}.pdf・PDF/21_09_F2_sparseness{SUF}.pdf")
