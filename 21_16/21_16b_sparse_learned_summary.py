#!/usr/bin/env python3
# =============================================================================
# Script : 21_16b_sparse_learned_summary.py  (v1)
#          [21_16a の 10 の網(間引かない + N = 12・8・5 局 × 種 3 つ)の結果を集め、事前に決めた分類(L4-SPARSE-HOLDS / -PARTIAL / -FAILS)を
#           出し、残した局の数と誤差の関係の図を描く。新しい位置の計算はしない]
# Project: ARGUS(新生)— 「凍結した学習型の選び方(L4)は、局がまばらな網でも物理だけ(BEST)に勝つか」(21_09 の学習型版)
#
# なぜ必要か:
#   21_16a は網ごとに 1 回だけ回して、網ごとの値を出す。判定(各 N の HOLDS / MIXED / FAILS と全体)は 10 の網が揃ってから、
#   事前登録の記録(21_16_preregistration.md)に書いた 21_16a の版の結果だけで出す必要がある。
#
# 何をするか:
#   1. models/21_16_run_<網>.json を全て読む(--limit N を付けると、動作確認の _limitN の結果だけを読む。判定は出さない)。
#      判定を出す条件(全て満たす時だけ。どれで出さなかったかを JSON に残す):
#        事前に決めた 10 の網が全て揃う・各 JSON の中身(tag・N・seed・limit = 0・名前に _rerun が無い)がファイル名と合う・
#        全て同じキャッシュ(SHA-256)・全て同じ 21_16a(SHA-256)で、それが --expect-sha(事前登録の記録に書いた 21_16a の SHA-256)と同じ・
#        全ての網で G-core・G-same が PASS・間引かない網で G-same-L が PASS・どの網の G-causal も FAIL でない・
#        1 回だけの記録(models/21_16_opened.json)で、どの網も「終わった」(名前に _rerun・_limit が無いもの)がちょうど 1 回で、その
#        SHA-256 が結果の JSON と同じ。止まった記録の数は網ごとに表示して JSON に残す(開示する)。
#   2. 分類(事前に決めた規則。21_16a の冒頭と同じ): 各 N(12・8・5)で、τ = 2 s の L4 が BEST に勝った網の数
#      3/3 = HOLDS、1〜2/3 = MIXED、0/3 = FAILS(「試せない」網と BEST が床 0.5 km 未満の網は勝ちに数えず、数を別に出す)。
#      全体は 全て HOLDS → L4-SPARSE-HOLDS、全て FAILS → L4-SPARSE-FAILS、それ以外 → L4-SPARSE-PARTIAL。
#      記述だけ(判定に使わない): L4 対 C4(α 0.005 で数える)・L3 @ τ = 0.5 s 対 BEST・C4 対 BEST(21_09 の再現)・他の τ・間引かない網。
#   3. 表(日本語): 網ごと・τ ごとに BEST(名前と中央値)・C4・L3・L4 の中央値・差(BEST − L4)・p・床・局の数・L が M6r に戻った割合・
#      10 km 超の割合、特徴量の様子(共通の局の数・dd_offset_km が nan の割合)と 2026 の学習の行の値。
#   4. 図(白背景・英語・凡例は図の外の下・PDF と PNG):
#      F1: τ = 0.5・1・2・3 s の 4 枚。横 = 残した局の数(対数)、縦 = 誤差の中央値(km、対数)。網ごとの点と、N ごとの中央値を結ぶ線。
#          BEST = 灰、C4 = 朱、L4 = 青(Okabe-Ito)。判定の時点 τ = 2 s の枠を太くする。
#      F2: τ = 2 s の差(km)と残した局の数: BEST − L4(青、主)と BEST − C4(朱、参考)。網ごとの点(塗り = 事前に決めた規則で勝ち、
#          白抜き = 勝ちなし)と N ごとの中央値の線。0 の線。
#
# Usage : cd ~/SWIFT && uv run python src/21_16b_sparse_learned_summary.py --expect-sha <事前登録の記録に書いた 21_16a の SHA-256>
#         (動作確認の結果なら --limit 8 も付ける。判定は出さない)
# Output: models/21_16_summary.json・PDF/21_16_F1_sparse_learned_error.pdf/.png・PDF/21_16_F2_gain_t2.pdf/.png(--limit なら _limitN 付き)
# =============================================================================
import json, argparse, hashlib, datetime as dt
from pathlib import Path
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("--limit", type=int, default=0)
ap.add_argument("--expect-sha", default="", help="事前登録の記録に書いた 21_16a の SHA-256(判定に必須)")
a = ap.parse_args()
ROOT = Path(__file__).resolve().parent.parent
for d in ("models", "PDF"): (ROOT / d).mkdir(exist_ok=True)
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
SELF_SHA = sha256(Path(__file__))
print(f"[21_16b] 本スクリプト v1 SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)")
CONFIGS = [(0, 0)] + [(N, s) for N in (12, 8, 5) for s in (0, 1, 2)]
SUFX = f"_limit{a.limit}" if a.limit else ""
def tag_of(N, s): return ("full" if N == 0 else f"N{N}_s{s}") + SUFX

# ---------------------------------------------------------------- 1. 読み込みと、判定を出す条件
RUNS, missing, bad_content = {}, [], []
for N, s in CONFIGS:
    p = ROOT / f"models/21_16_run_{tag_of(N, s)}.json"
    if not p.exists(): missing.append(tag_of(N, s)); continue
    r = json.load(open(p)); RUNS[(N, s)] = r
    if (r.get("tag") != tag_of(N, s) or r.get("out_tag") != tag_of(N, s) or r["network"].get("n_keep") != N or r["network"].get("seed") != s
            or r.get("limit") != a.limit or r.get("suffix") != SUFX):
        bad_content.append(tag_of(N, s))
if not RUNS: raise SystemExit("[21_16b] STOP: 21_16a の結果が 1 つも無い(先に 21_16a --all)")
shas = sorted({r["cache_sha256"] for r in RUNS.values()}); ssha = sorted({r["script_sha256"] for r in RUNS.values()})
def gst(r, k):
    g = (r.get("gates") or {}).get(k)
    return g.get("status") if isinstance(g, dict) else g
g_core = {r["tag"]: gst(r, "core") for r in RUNS.values()}
g_same = {r["tag"]: gst(r, "same") for r in RUNS.values()}
g_causal = {r["tag"]: gst(r, "causal") for r in RUNS.values()}
full = RUNS.get((0, 0))
g_same_l = gst(full, "same_learned") if full else None
OPEN = ROOT / "models/21_16_opened.json"
LOG = json.load(open(OPEN)) if OPEN.exists() else []
OPENLOG = {}
for (N, s), r in RUNS.items():
    t = r["tag"]; ent = [e for e in LOG if e.get("tag") == t]
    comp = [e for e in ent if e.get("status", "").startswith("completed") and e.get("suffix") == SUFX]
    OPENLOG[t] = dict(n_opened=sum(e.get("status", "").startswith("opened") for e in ent), n_stopped=sum(e.get("status", "").startswith("stopped") for e in ent),
                      n_completed=len(comp), n_reruns=sum(e.get("status", "").startswith("completed") and str(e.get("suffix", "")).startswith("_rerun") for e in ent),
                      completed_sha_matches=(len(comp) >= 1 and comp[0].get("script_sha256") == r["script_sha256"]))
log_bad = [t for t, v in OPENLOG.items() if v["n_completed"] != 1 or not v["completed_sha_matches"]]
GATES = dict(missing=missing, content_mismatch=bad_content, n_cache_sha=len(shas), n_script_sha=len(ssha),
             script_sha_matches_expected=(bool(a.expect_sha) and ssha == [a.expect_sha]),
             g_core_not_pass=[t for t, v in g_core.items() if v != "PASS"], g_same_not_pass=[t for t, v in g_same.items() if v != "PASS"],
             g_same_learned_full=g_same_l, g_causal_fail=[t for t, v in g_causal.items() if str(v).startswith("FAIL")],
             open_log_problem=log_bad, limit=a.limit)
complete = (not missing and not bad_content and len(shas) == 1 and GATES["script_sha_matches_expected"] and not GATES["g_core_not_pass"]
            and not GATES["g_same_not_pass"] and g_same_l == "PASS" and not GATES["g_causal_fail"] and not log_bad and not a.limit)
print(f"[21_16b] 読んだ網 {len(RUNS)}/10" + (f"  足りない: {', '.join(missing)}" if missing else "") +
      f"  中身の不一致 {bad_content or 'なし'}  キャッシュの SHA-256 {len(shas)} 種・21_16a の SHA-256 {len(ssha)} 種"
      f"(事前登録と同じ: {GATES['script_sha_matches_expected']})")
print(f"[21_16b] G-core・G-same が PASS でない網 {GATES['g_core_not_pass'] + GATES['g_same_not_pass'] or 'なし'}  間引かない網の G-same-L {g_same_l or '—'}  "
      f"G-causal の FAIL {GATES['g_causal_fail'] or 'なし'}  1 回だけの記録の問題 {log_bad or 'なし'}")
print("[21_16b] 1 回だけの記録(網ごとに 開いた / 止まった / 終わった / _rerun): " +
      "  ".join(f"{t} {v['n_opened']}/{v['n_stopped']}/{v['n_completed']}/{v['n_reruns']}" for t, v in OPENLOG.items()))

# ---------------------------------------------------------------- 2. 表
TL = ["0.5", "1", "2", "3"]
def f2(v): return "—" if v is None else f"{v:.2f}"
def fp(v): return "—" if v is None else f"{v:.2g}"
def pv(d): return (d.get("paired_vs_comparator") or {}).get("p")
print("\n[21_16b] ===== 網ごとの誤差の中央値 km(BEST / C4 / L3 / L4、差 = BEST − L4) =====")
for (N, s), r in RUNS.items():
    nw, sp = r["network"], r["sparseness"]
    print(f"  {r['tag']:<12} 局 {nw['n_stations_kept']:>2}・間隔 {f2(nw['nn_spacing_median_km_kept'])} km・評価 {r['n_evaluated']} 地震"
          f"({'試せる' if r.get('testable') else '試せない'})・P を測れず外れた {sp.get('test_events_lost_no_p')}・G-causal {g_causal[r['tag']]}")
    for t in TL:
        d = r["per_tau"][t]; L4 = d["L4"]; fe = d["features"]
        if L4.get("comparator") is None: print(f"      τ={t}: BEST なし"); continue
        print(f"      τ={t:>3} s: BEST {L4['best']:<4} {f2(L4['best_median_km'])} / C4 {f2(d['C4']['median_km'])} / L3 {f2(d['L3']['median_km'])} / "
              f"L4 {f2(L4['median_km'])}  差 {f2(L4['gain_km'])}  p(L4<BEST) {fp(pv(L4))} {'勝ち' if L4['win'] else '—'}  "
              f"p(L4<C4) {fp(pv(d['L4_vs_C4']))} {'勝ち' if d['L4_vs_C4']['win'] else '—'}  p(C4<BEST) {fp(pv(d['C4']))}  床 {L4['floor']}  "
              f"局 {f2(d['stations_median'])}  L→M6r {f2(d['learned_fallback_frac'])}  10 km 超 L4 {f2(d['tail_frac_over_10km']['L4'])}  "
              f"共通の局 {f2(fe['n_common_picks_median'])}(2026 {f2(fe['training_2026']['n_common_picks_median'])})  "
              f"dd nan {f2(fe['dd_offset_nan_frac_median'])}(2026 {f2(fe['training_2026']['dd_offset_nan_frac'])})")

# ---------------------------------------------------------------- 3. 事前に決めた分類
LEVEL = {}
for N in (12, 8, 5):
    rs = [RUNS[(N, s)] for s in (0, 1, 2) if (N, s) in RUNS]
    ps = [r["per_tau"]["2"]["L4"] for r in rs]
    nw = sum(bool(c["win"]) for c in ps)
    cls = ("HOLDS" if nw == 3 else "MIXED" if nw >= 1 else "FAILS") if len(rs) == 3 else "INCOMPLETE"
    LEVEL[str(N)] = {"n_runs": len(rs), "l4_wins_t2": nw, "class": cls,
                     "n_untestable": sum(not c.get("testable", False) for c in ps), "n_floor_blocked_t2": sum(bool(c.get("floor")) for c in ps),
                     "gain_t2_km": [c.get("gain_km") for c in ps], "best_t2_km": [c.get("best_median_km") for c in ps],
                     "l4_t2_km": [c.get("median_km") for c in ps], "p_t2": [pv(c) for c in ps],
                     "descriptive": dict(l4_vs_c4_wins_t2=sum(bool(r["per_tau"]["2"]["L4_vs_C4"]["win"]) for r in rs),
                                         c4_vs_best_wins_t2=sum(bool(r["per_tau"]["2"]["C4"]["win"]) for r in rs),
                                         l3_vs_best_wins_t05=sum(bool(r["per_tau"]["0.5"]["L3"]["win"]) for r in rs),
                                         c4_t2_km=[r["per_tau"]["2"]["C4"].get("median_km") for r in rs])}
cl = [v["class"] for v in LEVEL.values()]
VERDICT = ("L4-SPARSE-HOLDS" if all(c == "HOLDS" for c in cl) else "L4-SPARSE-FAILS" if all(c == "FAILS" for c in cl)
           else "L4-SPARSE-PARTIAL") if complete else "NO VERDICT (see gates)"
print("\n[21_16b] ===== 事前に決めた分類(τ = 2 s の L4 対 BEST、α 0.005) =====")
for N, v in LEVEL.items():
    ds = v["descriptive"]
    print(f"  N = {N} 局: L4 の勝ち {v['l4_wins_t2']}/{v['n_runs']} → {v['class']}  (試せない {v['n_untestable']}・床 {v['n_floor_blocked_t2']})  "
          f"差 BEST − L4 = {', '.join(f2(x) for x in v['gain_t2_km']) or '—'} km  p = {', '.join(fp(x) for x in v['p_t2']) or '—'}")
    print(f"      記述だけ: L4 が C4 に勝った網 {ds['l4_vs_c4_wins_t2']}・C4 が BEST に勝った網 {ds['c4_vs_best_wins_t2']}・L3 @ 0.5 s が BEST に勝った網 {ds['l3_vs_best_wins_t05']}")
REF = None
if full and full["per_tau"]["2"]["L4"].get("comparator"):
    L4 = full["per_tau"]["2"]["L4"]
    REF = dict(best=L4["best"], best_km=L4["best_median_km"], l4_km=L4["median_km"], c4_km=full["per_tau"]["2"]["C4"]["median_km"], gain_km=L4["gain_km"],
               p=pv(L4), win=L4["win"])
    print(f"  間引かない網(21_06b の再現、判定に使わない): BEST {L4['best']} {f2(L4['best_median_km'])} / C4 {f2(REF['c4_km'])} / L4 {f2(L4['median_km'])} km  "
          f"差 {f2(L4['gain_km'])}  p {fp(REF['p'])}")
print(f"[21_16b] 判定(事前に決めた分類): {VERDICT}" + ("" if complete else f"  ゲート: {GATES}"))
print("[21_16b] 限界: " + " / ".join(next(iter(RUNS.values()))["limits"][-7:]))

# ---------------------------------------------------------------- 4. 図
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
from matplotlib.lines import Line2D
plt.rcParams.update({"font.size": 11, "axes.facecolor": "white", "figure.facecolor": "white", "savefig.facecolor": "white", "pdf.fonttype": 42})
COL = {"BEST": "#7F7F7F", "C4": "#D55E00", "L4": "#0072B2"}; MK = {"BEST": "o", "C4": "D", "L4": "^"}
LABEL = {"BEST": "BEST: best of 9 methods without waveform similarity", "C4": "C4: similar past events chosen by similarity (hand-designed)",
         "L4": "L4: similar past events chosen by the frozen learned ranker"}
NALL = (full or next(iter(RUNS.values())))["network"]["n_stations_all"]
XT = [5, 8, 12, NALL]; XTL = ["5", "8", "12", f"{NALL}\n(all)"]
JIT = {0: 0.94, 1: 1.0, 2: 1.06}
def xv(N, s): return NALL if N == 0 else N * JIT[s]
def setx(ax, lo=4.2):
    ax.set_xscale("log"); ax.set_xlim(lo, NALL * 1.24)
    ax.xaxis.set_major_locator(FixedLocator(XT)); ax.xaxis.set_major_formatter(FixedFormatter(XTL)); ax.xaxis.set_minor_locator(NullLocator())
def save(fig, name):
    fig.savefig(ROOT / f"PDF/{name}.pdf"); fig.savefig(ROOT / f"PDF/{name}.png", dpi=200); plt.close(fig)
def val(r, t, m):
    d = r["per_tau"][t]
    return d["L4"].get("best_median_km") if m == "BEST" else d[m].get("median_km")
# F1
vals = []
fig, axs = plt.subplots(1, 4, figsize=(15, 5.3), sharey=True)
for ax, t in zip(axs, TL):
    for m in ("BEST", "C4", "L4"):
        lv = {}
        for (N, s), r in RUNS.items():
            v = val(r, t, m)
            if v is None: print(f"[21_16b] 注意: {r['tag']} τ={t} {m} の値なし(図から外す)"); continue
            vals.append(v); lv.setdefault(N, []).append(v)
            ax.scatter(xv(N, s), v, s=20, marker=MK[m], color=COL[m], alpha=0.45, zorder=3, linewidths=0)
        L = sorted((NALL if N == 0 else N, float(np.median(v))) for N, v in lv.items())
        ax.plot([p[0] for p in L], [p[1] for p in L], "-", color=COL[m], marker=MK[m], ms=6, lw=2, label=LABEL[m], zorder=4)
    ax.set_yscale("log"); setx(ax); ax.grid(alpha=0.3, which="major")
    ax.set_title(f"τ = {t} s after the first P", fontsize=11.5); ax.set_xlabel("Stations kept (log scale)")
    if t == "2":
        for sp_ in ax.spines.values(): sp_.set_linewidth(1.8)
        ax.set_title("τ = 2 s after the first P\n(preregistered decision point)", fontsize=11.5)
if vals:
    lo, hi = min(vals), max(vals); YLIM = (lo / 1.3, hi * 1.3)
    YT = [y for y in (0.05, 0.1, 0.2, 0.3, 0.5, 1, 2, 3, 5, 10, 20, 50) if YLIM[0] <= y <= YLIM[1]]
    axs[0].set_ylim(*YLIM)
    if len(YT) >= 2:
        axs[0].yaxis.set_major_locator(FixedLocator(YT)); axs[0].yaxis.set_major_formatter(FixedFormatter([f"{y:g}" for y in YT]))
        axs[0].yaxis.set_minor_locator(NullLocator())
axs[0].set_ylabel("Median epicentral error vs JMA (km)")
h, l = axs[0].get_legend_handles_labels()
fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.0), fontsize=10)
fig.suptitle("Central Tottori 2016 test events on thinned Hi-net networks: frozen learned ranker (L4) vs physics (BEST) and C4\n"
             f"(small points: each of 3 networks per size; lines: median over networks).  Preregistered verdict: {VERDICT}"
             + (f"  [mock/dev: --limit {a.limit}]" if a.limit else ""), fontsize=11.5, y=0.985)
fig.tight_layout(rect=(0, 0.07, 1, 0.93)); save(fig, f"21_16_F1_sparse_learned_error{SUFX}")
# F2
SMK = {0: "o", 1: "s", 2: "^"}
fig, ax = plt.subplots(figsize=(8.2, 5.6))
lines = {}
for m in ("L4", "C4"):
    lv = {}
    for (N, s), r in RUNS.items():
        d = r["per_tau"]["2"][m]; g = d.get("gain_km")
        if g is None: continue
        lv.setdefault(N, []).append(g)
        x = xv(N, s) * (1.015 if m == "C4" else 0.985)
        mk = "*" if N == 0 else SMK[s]; ms = 130 if N == 0 else 55
        ax.scatter(x, g, marker=mk, s=ms, zorder=4, edgecolors=COL[m], linewidths=1.4, facecolors=(COL[m] if d.get("win") else "white"))
    L = sorted((NALL if N == 0 else N, float(np.median(v))) for N, v in lv.items())
    ax.plot([p[0] for p in L], [p[1] for p in L], "-" if m == "L4" else "--", color=COL[m], lw=2, zorder=3)
    lines[m] = L
setx(ax, lo=3.6); ax.axhline(0, color="0.5", lw=0.9, zorder=1); ax.grid(alpha=0.3)
ax.set_xlabel("Stations kept (log scale)"); ax.set_ylabel("Gain at τ = 2 s: BEST − method, median error (km)")
ax.set_title("Gain over physics at τ = 2 s (positive = better than BEST)", fontsize=11.5)
hs = [Line2D([], [], color=COL["L4"], lw=2, label="BEST − L4 (primary; line = median over networks)"),
      Line2D([], [], color=COL["C4"], lw=2, ls="--", label="BEST − C4 (21_09, for reference)"),
      Line2D([], [], ls="", marker="o", ms=8, mfc="0.4", mec="0.4", label="Filled: wins by the preregistered rule"),
      Line2D([], [], ls="", marker="o", ms=8, mfc="white", mec="0.4", label="Open: no win"),
      Line2D([], [], ls="", marker="*", ms=11, mfc="white", mec="0.2", label=f"All {NALL} stations")] + \
     [Line2D([], [], ls="", marker=SMK[s], ms=7, mfc="white", mec="0.2", label=f"Thinned network, seed {s}") for s in (0, 1, 2)]
fig.legend(handles=hs, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.0), fontsize=9.5)
fig.tight_layout(rect=(0, 0.2, 1, 1)); save(fig, f"21_16_F2_gain_t2{SUFX}")
json.dump(dict(script="21_16b_sparse_learned_summary.py", script_sha256=SELF_SHA, utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               expected_21_16a_sha256=a.expect_sha, runs_read=[r["tag"] for r in RUNS.values()], gates=GATES, open_log=OPENLOG, complete=complete,
               run_script_sha256=ssha, cache_sha256=shas, g_causal=g_causal, reference_full=REF, levels=LEVEL, verdict=VERDICT,
               figure_lines_t2_gain=lines, limits=next(iter(RUNS.values()))["limits"]),
          open(ROOT / f"models/21_16_summary{SUFX}.json", "w"), indent=1)
print(f"[21_16b] 出力: models/21_16_summary{SUFX}.json・PDF/21_16_F1_sparse_learned_error{SUFX}・PDF/21_16_F2_gain_t2{SUFX}(.pdf と .png)")
