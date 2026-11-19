#!/usr/bin/env python3
# =============================================================================
# Script : 21_09a_ct2016_sparse_network.py  (v1)
#          [鳥取県中部 2016 の Hi-net の局を、位置だけで決めた規則で間引いて「まばらな観測網」を作り、その網だけがあったと
#           して物理(似た地震を使わない 9 方法の最良 = BEST)と C3・C4(波形が似た過去の地震 × 物理)の最初の数秒の誤差を
#           測り直す。「局がまばらな網でこそ、似た過去の地震を足す価値が大きいか」を確かめる]
# Project: ARGUS(新生)— 論文の柱「1〜2 局・単一開口の震源決定」。SSJ 2026 の 2 枚目の問題(局が少ないと答えが決まらない)の裏付け
#
# なぜ必要か:
#   21_04 の誤差(2 秒で物理 0.95 km)は、局の間隔が約 20 km の密な Hi-net での値。まばらな網(海域・観測網の薄い地域・
#   単一開口)では、同じ「1〜2 局」でも誤差はもっと大きいはず。そこで C3・C4 の改善が残るか(大きくなるか)を見る。
#
# 何をするか(1 回の実行 = 1 つの網):
#   1. 候補の局 = キャッシュの地震のどれかに出てくる局(緯度・経度で見分ける。15_01c が各地震で残した最大 24 局の和集合)。
#      局の重心を原点にした平面(km)に置く。
#   2. 間引き(--n-keep N、--seed s): 最遠点の選び方で N 局を選ぶ。最初の局を乱数(種 1000 + s)で 1 つ選び、以後は「選んだ局から
#      最も遠い局」を 1 つずつ足す(同じ距離なら番号の小さい局)。局を広く均等に散らした、まばらな網になる。N = 0 は間引かない
#      (21_04 と同じ網)。局の位置だけで決め、地震の結果(誤差)は見ない。局の数で決めるので、どの N でも必ず N 局が残る。
#   3. 残した局以外の局を、全ての地震(試験の地震・過去の地震の一覧・pool)から消す(その網しか無かったことにする)。
#      その上で 21_04 v1 と同じ計算をする: pool で速度・局の補正・ラプラス尺度・KDE の帯域・格子を決め直し、検測・
#      τ(最初の P からの時間)・似ている度合い・C3・C4 を、残した局だけで計算する。
#   4. 評価: 試験の地震(本震 + 72 h より後の 1.5 ≤ Mj < 2.0。21_04 と同じ)のうち、残した局で P を測れた地震。
#      τ = 0.5・1・2・3 s で 9 方法・C3・C4 の水平誤差(9 方法は全検測も。正解は気象庁の震源)。
#      BEST(τ) と勝ちの規則は 21_04 と同じ(評価する全ての地震で値がある 9 方法の中で中央値が最小。中央値が小さく・片側の
#      対応 Wilcoxon の p が基準未満・差が 0 でない組 10 以上・BEST が 0.5 km 以上)。基準は C3 が 0.01、C4 が 0.005(21_04 の
#      H1・H2 と同じ)。評価できる地震が 30 未満の網は「試せない」(21_04 の INCONCLUSIVE と同じ規則)。
#   5. まばらさの記述: 残した局の最近接の間隔(中央値)、最初に P が届いた局の震央距離と、P の時刻(気象庁の発生時刻から)の中央値、
#      残した局で P を測れずに評価から外れた試験の地震の数。網ごとに評価する地震の集合が違うので、網をまたぐ傾向は記述だけ。
#
# 事前に決めた分類(データを見る前に、この版の SHA-256 を事前登録の記録に書く。集計は 21_09b):
#   網: N = 0(間引かない)と、N = 12・8・5 局の各 3 つの種(seed 0・1・2)。合計 10 回。
#   各 N(12・8・5)について、τ = 2 s の C4 が BEST に勝った(上の規則、α 0.005)網の数で
#     3/3 = HOLDS、1〜2/3 = MIXED、0/3 = FAILS(「試せない」網と、BEST が床 0.5 km 未満の網は勝ちに数えない。数は別に記録する)。
#   全体: 12・8・5 が全て HOLDS → SPARSE-HOLDS、全て FAILS → SPARSE-FAILS、それ以外 → SPARSE-PARTIAL。
#   C3(α 0.01)と他の τ、誤差の差の大きさ(BEST − C4)の傾向は記述だけ。
#
# ゲート:
#   G-same(N = 0 だけ): 21_04 の本番の CSV(data/21_04_per_event.csv)と、評価する地震の集合が同じで(--limit の時は部分集合)、
#     9 方法・C3・C4 の誤差(τ = 0.5・1・2・3 s、9 方法は全検測も)と P のある局の数が同じ(誤差は小数 4 桁で 6e-5 km 以内)でなければ STOP。
#   G-station: 局を (緯度, 経度) で見分けた数と、(緯度, 経度, 高さ) で見分けた数が同じ。間引いた後、残った局が全て選んだ局。
#   G-split・G-lib・自分が上位に入らない(21_04 と同じ)。G-causal(未来の波形と検測を入れ替えても、位置と S の最大が同じ +
#     陽性対照)を各網で。陽性対照は、ゲートの地震のうち過去の地震と局を共有する最初の地震で行う。
#     間引いた網で、確かめられる地震が 3 未満の時は「確かめられず」(not checked)と記録して続ける。局を共有する地震が無い時は、
#     入れ替えの確認だけで PASS とし、陽性対照は「できず」と記録する(N = 0 では止める)。
#   G-phys(τ = ∞ の M5 の中央値 ≤ 0.5 km)は記録だけ(まばらな網では満たさなくてよい)。
#
# 限界(結果を読むときに必ず添える。JSON にも英語で書く):
#   - 間引きは Hi-net の局の部分集合で作った仮想の網。実際のまばらな網(海底局・別の種類の局・別の地域)とは違う
#   - キャッシュは密な網で作った: 地震は密な網で 4 つ以上の検測があったものだけ(まばらな網では見つからない地震も入っている)。
#     S の検測の品質の確かめ(和達)はその地震の全ての局で行ったので、残した局の S を残すかどうかに、消した局が効いている
#   - キャッシュは 1 地震につき最大 24 局(P を測れた局を P の早い順、その後に代わりの検測の局)。元は 25 番目以降だった局は使えない
#   - 正解・過去の地震の位置・C4 の局の補正は気象庁の震源(密な網で決めた値)。まばらな網しか無い地域では、過去の地震の
#     位置そのものがもっと悪いはずで、ここでの C3・C4 は楽観的
#   - 21_04 と同じ限界(1 つの系列・オフラインの PhaseNet・検測と通信の遅れなし・小さい地震・2016 は逸脱を開示した試験 など)
#
# Usage : cd ~/SWIFT && caffeinate -i uv run python src/21_09a_ct2016_sparse_network.py --all
#           (10 回を順に、別のプロセスで実行。同じ版・同じキャッシュで終わった網は飛ばすので、途中で止まっても同じコマンドで続きから)
#         1 つだけ: ... --n-keep 8 --seed 1   /   動作確認: ... --all --limit 20(結果は _limit20 の名前。判定に使わない)
# Output: models/21_09_run_<網>.json・data/21_09_per_event_<網>.csv(<網> = full、N12_s0 … N5_s2)
# 次に  : 21_09b_sparse_summary.py(集計・図・分類)、21_10_gmpe_location_error.py(揺れの予測への影響)
# 所要  : CPU のみ。N = 0 は 21_04 と同じくらい(感度の計算を省くので少し短い)、間引いた網は局が少ない分だけ短い
# =============================================================================
import json, argparse, time, csv, hashlib, math, warnings, datetime as dt
from pathlib import Path
import numpy as np
import torch
from scipy.signal import butter, sosfilt
from scipy.stats import wilcoxon
warnings.filterwarnings("ignore", message="All-NaN slice")

ap = argparse.ArgumentParser()
ap.add_argument("--cache", default="data/ct2016_processed/tottori_parsed_realpick_ct2016_m15.pt", help="15_01c v3.3 の鳥取県中部 2016 の M>=1.5 版")
ap.add_argument("--n-keep", type=int, default=0, help="残す局の数 N(0 = 間引かない)")
ap.add_argument("--seed", type=int, default=0, help="最初の局を選ぶ乱数の種(1000 + seed)")
ap.add_argument("--all", action="store_true", help="事前に決めた 10 の網を、別のプロセスで順に実行する(終わった網は飛ばす)")
ap.add_argument("--force", action="store_true", help="--all で、終わった網もやり直す")
ap.add_argument("--limit", type=int, default=0, help="動作確認用: 試験の地震を先頭から N 個だけ(結果は _limitN の名前。判定に使わない)")
a = ap.parse_args()
CONFIGS = [(0, 0)] + [(N, s) for N in (12, 8, 5) for s in (0, 1, 2)]       # 事前に決めた網(変えたら版を上げる)
def tag_of(N, s, lim): return ("full" if N == 0 else f"N{N}_s{s}") + (f"_limit{lim}" if lim else "")
if a.all:
    import subprocess, sys
    _root = Path(__file__).resolve().parent.parent
    def _sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f_:
            for b in iter(lambda: f_.read(1 << 20), b""): h.update(b)
        return h.hexdigest()
    _me, _cs = _sha(Path(__file__)), (_sha(_root / a.cache) if (_root / a.cache).exists() else None)
    for N, s in CONFIGS:
        tg = tag_of(N, s, a.limit); jp = _root / f"models/21_09_run_{tg}.json"
        if jp.exists() and not a.force:
            old = json.load(open(jp))
            if old.get("script_sha256") == _me and old.get("cache_sha256") == _cs:
                print(f"[21_09] {tg}: 同じ版・同じキャッシュの結果があるので飛ばす"); continue
            raise SystemExit(f"[21_09] STOP: {tg} の結果は別の版かキャッシュで作られている(やり直すなら --force)")
        print(f"[21_09] ===== {tg} を実行 =====", flush=True)
        cmd = [sys.executable, str(Path(__file__).resolve()), "--cache", a.cache, "--n-keep", str(N), "--seed", str(s)] + (["--limit", str(a.limit)] if a.limit else [])
        r = subprocess.run(cmd)
        if r.returncode != 0: raise SystemExit(f"[21_09] STOP: {tg} が止まった(上の STOP の行を貼って相談)")
    print("[21_09] 全ての網が終わった。次に 21_09b_sparse_summary.py を実行"); raise SystemExit(0)
if a.n_keep < 0 or 0 < a.n_keep < 3: raise SystemExit("[21_09] STOP: --n-keep は 0(間引かない)か 3 以上")
TAG = tag_of(a.n_keep, a.seed, a.limit)

# ---------------------------------------------------------------- 事前に固定した値(変えたら版を上げる)
VERSION = "v1"                             # 21_09a の版(下の 1.〜6. は 21_04 v1 の写し)
FS, IP, NTS = 100.0, 300, 2048
TAUS = [0.5, 1.0, 2.0, 3.0]
PRIMARY = "2"                              # (21_04 の写し。21_09 では使わない)
SECONDARY = [("H2", "C4", "2"), ("H3", "C3", "0.5")]   # (21_04 の写し。α 0.005 だけを C4 の基準に使う)
ALPHA_SEC = 0.005
MIN_MAG, FRESH_MAX_MAG, MATCH_S = 1.5, 2.0, 1.0
MIN_CORR = 3                               # C4: 局の補正に使う似た地震の最少数
EPS_T = 1e-4                               # 時刻を比べる時の余裕(s)
POOL_H, BUFFER_H = 72.0, 1.0
BAND, BAND_SENS = (2.0, 8.0), (4.0, 16.0)
PRE_S, MIN_WIN_S, MAX_WIN_S, MAX_LAG_S = 0.2, 0.3, 3.0, 0.1
TOPK, TOPK_SENS, MIN_POS = 10, (5, 20), 5
BUFFER_SENS_H = 0.1
S_WEIGHT, SHRINK, MIN_PRIOR_EV, PRIOR_EPS = 0.5, 5.0, 5, 0.05
FLOOR_KM, MIN_TEST, ALPHA, MIN_NONZERO, BAR = 0.5, 30, 0.01, 10, 0.7
NBOOT, SEED, N_DEV, N_GATE = 2000, 12, 20, 5
MAIN_UTC = dt.datetime(2016, 10, 21, 5, 7, 22, 570000)
UNTOUCHED_UTC = (dt.datetime(2016, 10, 19), dt.datetime(2016, 11, 15))   # G-untouched: 21_04a の期間を含む
LIMITS = ["second sequence: Central Tottori 2016 (mainshock 2016-10-21 05:07 UTC, Mj 6.6), never used in ARGUS development; "
          "the hypotheses were fixed on West Tottori 2026 (21_01/21_02) and are applied here unchanged",
          "one second sequence only",
          "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
          "set of 50 stations also included non-Hi-net stations, so station types and geometry differ",
          "waveforms were downloaded around catalogue events only and converted to the West Tottori 2026 h5 form (30-s windows, "
          "per-window per-component z-score, JST epoch); whether a filter was applied before the z-score in the 2026 h5 is not recorded "
          "(none here; compared in 21_04b G-spec)",
          "the cache was built by 15_01c v3.3 (picking, QC and assembly identical to v3; only the window-index file name and output "
          "folder changed)",
          "catalogue: JMA final hypocentres (h2016; West Tottori 2026 used the unified catalogue); past-event locations are JMA "
          "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
          "the 2016 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
          "events; whether the 2026 catalogue excluded them is not recorded. Manual and automatic hypocentres are mixed (per-flag "
          "counts in 21_04a's JSON)",
          "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); the 2026 station list's "
          "convention is not recorded; static station terms absorb a constant offset",
          "offline PhaseNet picks on full records (possibly better than real-time picks); every method uses the same picks",
          "cache keeps up to 24 stations per event (PhaseNet P first, earliest first); no not-yet-arrived information is used",
          "cache waveforms had the full-window mean removed (includes future samples; removed by the 2 Hz high-pass except for a "
          "transient from the window start 3 s before P) and the source h5 is z-score normalised per 30-s window (the scale uses later "
          "samples of that window; cosine similarity is scale-invariant except where a window join falls inside the correlation window); "
          "the one-sample look-ahead of the cache's central-difference derivative is avoided by not using the last sample",
          "no picking or telemetry latency (tau is ideal elapsed time)",
          "the test events are small (1.5 <= Mj < 2.0); pick quality and station counts can differ from Mj >= 2.0 events",
          "the 2-8 Hz band was chosen after seeing 18_01 on West Tottori 2026",
          "C4's station terms come from past events' JMA hypocentres and truth is also JMA, so part of a C4 gain can be agreement with "
          "the JMA frame rather than better early information",
          "C4 corrects only arrived stations held by >= 3 top similar events; each past event's terms are demeaned by its own median "
          "P residual over all its stations, while uncorrected stations keep only the static term",
          "21_09: per network, C4 at tau = 2 s vs BEST (alpha 0.005) is the classified test; everything else is descriptive"]

ROOT = Path(__file__).resolve().parent.parent
for d in ("models", "PDF", "data"): (ROOT / d).mkdir(exist_ok=True)
T0 = time.time()
RNG_GATE = np.random.default_rng(SEED + 1)
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def utcnow(): return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SELF_SHA = sha256(Path(__file__))
print(f"[21_09] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
      f"網 {TAG}(1. 入力〜6. 似ている度合い は 21_04 v1 の写し。間引きは 1b.)")

# ---------------------------------------------------------------- 1. 入力
CP = ROOT / a.cache
if not CP.exists(): raise SystemExit(f"[21_09] STOP: {a.cache} が無い(ノート 21_04_ct2016_colab.ipynb のセル 11 で作った tottori_parsed_realpick_ct2016_m15.pt を data/ct2016_processed/ に置く)")
EVS = torch.load(CP, map_location="cpu", weights_only=False)
need = ["origin_time", "src_loc", "mw", "waveforms", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
for e in EVS:
    miss = [k for k in need if k not in e]
    if miss: raise SystemExit(f"[21_09] STOP: キャッシュの地震に {miss} が無い(15_01c v3.3 の出力か確かめる)")
# ---------------------------------------------------------------- 1b. 局を間引く(21_09 で足した部分。局の位置だけで決める)
PERSTA = ["waveforms", "sta_locs", "tp_times", "sp_diffs", "p_fallback", "s_fallback"]
def stkey(l): return (round(float(l[0]), 4), round(float(l[1]), 4))
ALLST = {}
EVS_ALL_KEYS = set()
for e in EVS:
    n = int(e["n_real_stations"])
    for l in np.asarray(e["sta_locs"], float)[:n]:
        ALLST[stkey(l)] = (float(l[0]), float(l[1])); EVS_ALL_KEYS.add((round(float(l[0]), 4), round(float(l[1]), 4), round(float(l[2]), 3)))
STK = sorted(ALLST); STLL = np.array([ALLST[k] for k in STK])
SLAT0, SLON0 = float(STLL[:, 0].mean()), float(STLL[:, 1].mean())
SXY = np.c_[(STLL[:, 1] - SLON0) * 111.0 * np.cos(np.radians(SLAT0)), (STLL[:, 0] - SLAT0) * 111.0]
def nn_median(xy):
    if len(xy) < 2: return None
    d = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1)); np.fill_diagonal(d, np.inf); return float(np.median(d.min(1)))
if a.n_keep == 0:
    KEEPI = list(range(len(STK))); START = None
else:
    if a.n_keep >= len(STK): raise SystemExit(f"[21_09] STOP: --n-keep {a.n_keep} が候補の局の数 {len(STK)} 以上")
    START = int(np.random.default_rng(1000 + a.seed).integers(len(STK)))
    KEEPI = [START]; dmin = np.hypot(*(SXY - SXY[START]).T)
    while len(KEEPI) < a.n_keep:
        nxt = int(np.argmax(dmin)); KEEPI.append(nxt); dmin = np.minimum(dmin, np.hypot(*(SXY - SXY[nxt]).T))
    KEEPI = sorted(KEEPI)
KEEP = {STK[i] for i in KEEPI}
NN_ALL, NN_KEEP = nn_median(SXY), nn_median(SXY[KEEPI])
n_before = sum(int(e["n_real_stations"]) for e in EVS)
for e in EVS:
    n = int(e["n_real_stations"]); loc = np.asarray(e["sta_locs"], float)[:n]
    idx = [k for k in range(n) if stkey(loc[k]) in KEEP]
    for k in PERSTA: e[k] = np.asarray(e[k])[:n][idx]
    e["n_real_stations"] = len(idx)
n_after = sum(int(e["n_real_stations"]) for e in EVS)
# G-station: (緯度, 経度) と (緯度, 経度, 高さ) で見分けた局の数が同じ・残った局は全て選んだ局
_sk3 = set()
for e in EVS_ALL_KEYS: _sk3.add(e)
_left = {stkey(l) for e in EVS for l in np.asarray(e["sta_locs"], float)[:int(e["n_real_stations"])]}
if len(_sk3) != len(STK) or not _left <= KEEP: raise SystemExit(f"[21_09] STOP(G-station): 局の見分けか間引きがおかしい({len(_sk3)} 対 {len(STK)})")
print(f"[21_09] 間引き: N = {a.n_keep}(最遠点、最初の局 {START}、seed {a.seed})  局 {len(STK)} → {len(KEEP)}(候補は 15_01c の 50 局のうちキャッシュに出てくる局)  "
      f"最近接の間隔の中央値 {NN_ALL if NN_ALL is None else round(NN_ALL, 1)} → {NN_KEEP if NN_KEEP is None else round(NN_KEEP, 1)} km  "
      f"検測の行 {n_before} → {n_after}")
if len(KEEP) < 3: raise SystemExit("[21_09] STOP: 残した局が 3 未満")
for e in EVS:
    w_ = np.asarray(e["waveforms"])
    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_09] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_09] STOP: {e['origin_time']} の波形に NaN か無限大")
def to_ns(o):
    import pandas as pd
    try:
        t = pd.Timestamp(str(o).replace("Z", "+00:00"))
        t = t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t
        return int(t.value)
    except Exception:
        raise SystemExit(f"[21_09] STOP: origin_time {o!r} を時刻として読めない")
OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
order = np.argsort(OTNS, kind="stable"); EVS = [EVS[i] for i in order]; OTNS = OTNS[order]
NE = len(EVS)
SRC = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS])
MAG = np.array([float(e["mw"]) for e in EVS])
OT = [str(e["origin_time"]) for e in EVS]
if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
    raise SystemExit("[21_09] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[21_09] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
# G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
lo_ns = int(np.datetime64(UNTOUCHED_UTC[0], "ns").astype(np.int64)); hi_ns = int(np.datetime64(UNTOUCHED_UTC[1], "ns").astype(np.int64))
n_out = int(np.sum((OTNS < lo_ns) | (OTNS > hi_ns))); n_big = int(np.sum(MAG >= 6.0 - 1e-6))
FRESH = MAG < FRESH_MAX_MAG - 1e-6
CACHE_SHA = sha256(CP)
n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
print(f"[21_09] 入力: 鳥取県中部 2016 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
      f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
print(f"[21_09] G-untouched: 期間 2016-10-19〜2016-11-15(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
      + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
if n_out != 0 or n_big != 1: raise SystemExit("[21_09] STOP(G-untouched): 鳥取県中部 2016 のキャッシュに見えない(この行を貼って相談)")
im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
    raise SystemExit(f"[21_09] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj 6.6・2016-10-21 05:07:22.57 UTC)")
CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
pool_idx = np.where(OTNS <= CUT_NS)[0]; test_idx = np.where((OTNS > CUT_NS) & FRESH)[0]
if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
    raise SystemExit("[21_09] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
print(f"[21_09] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
print(f"[21_09] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
      f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")

# ---------------------------------------------------------------- 2. 座標・検測(17_02 と同じ)
TFIRST = np.full(NE, np.nan)          # PhaseNet で測った最も早い P(気象庁の発生時刻からの s)
skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
for ie, e in enumerate(EVS):
    n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    ok = np.isfinite(tp) & (pf == 0)
    if ok.any(): TFIRST[ie] = float(tp[ok].min())
    kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
    if len(set(kk)) != n: raise SystemExit(f"[21_09] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
HASP = ~np.isnan(TFIRST)
CAL = [ie for ie in pool_idx if HASP[ie]]
LAT0, LON0 = SRC[CAL, 0].mean(), SRC[CAL, 1].mean()
COS0 = np.cos(np.radians(LAT0))
def to_xy(lat, lon): return (np.asarray(lon) - LON0) * 111.0 * COS0, (np.asarray(lat) - LAT0) * 111.0
def to_ll(x, y): return LAT0 + y / 111.0, LON0 + x / (111.0 * COS0)
def km_between(lat1, lon1, lat2, lon2):
    return float(np.hypot((lat1 - lat2) * 111.0, (lon1 - lon2) * 111.0 * np.cos(np.radians((lat1 + lat2) / 2))))
st_all = np.concatenate([np.asarray(e["sta_locs"], float) for e in EVS[:50]])
EL_SCALE = 1e-3 if np.nanmax(np.abs(st_all[:, 2])) > 10.0 else 1.0
EX, EY = to_xy(SRC[:, 0], SRC[:, 1])
print(f"[21_09] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
# (21_09: 21_04 の dev・1 回だけの記録はここでは使わない。stop は記録を書かずに止まるだけ)
def stop(msg):
    raise SystemExit(msg)

def picks_of(ie, tau=np.inf):
    """17_02 の picks_of と同じ(P は tp ≤ τ、S は tp + sp ≤ τ)。時刻は TFIRST を 0 にした値"""
    e = EVS[ie]; n = int(e["n_real_stations"])
    loc = np.asarray(e["sta_locs"], float)[:n]; tp = np.asarray(e["tp_times"], float)[:n] - TFIRST[ie]
    sp = np.asarray(e["sp_diffs"], float)[:n]
    pf = np.asarray(e["p_fallback"]).astype(int)[:n]; sf = np.asarray(e["s_fallback"]).astype(int)[:n]
    out = []
    for k in range(n):
        if not np.isfinite(tp[k]) or pf[k] != 0 or tp[k] > tau + EPS_T: continue
        wS = S_WEIGHT if (sf[k] == 0 and np.isfinite(sp[k]) and tp[k] + sp[k] <= tau + EPS_T) else 0.0
        x, y = to_xy(loc[k, 0], loc[k, 1]); z = -float(loc[k, 2]) * EL_SCALE
        out.append((skey(loc[k]), float(x), float(y), z, float(tp[k]), 1.0, float(tp[k] + sp[k]) if wS > 0 else np.nan, wS, k))
    return out
def n_phases(pk): return len(pk) + sum(1 for p in pk if p[7] > 0)
def tt(R, z1, z2, v0, k):
    v1 = np.maximum(v0 + k * z1, 0.5); v2 = np.maximum(v0 + k * z2, 0.5)
    if k < 1e-4: return R / (0.5 * (v1 + v2))
    return np.arccosh(1.0 + (k * k) * R * R / (2.0 * v1 * v2)) / k

# ---------------------------------------------------------------- 3. 速度・局の補正・ラプラス尺度(pool、17_02 と同じ)
rows = []
for ii, ie in enumerate(CAL):
    xe, ye = EX[ie], EY[ie]; ze = SRC[ie, 2]
    for (key, x, y, z, tP, wP, tS, wS, _k) in picks_of(ie):
        rows.append((ii, key, x, y, z, xe, ye, ze, tP, wP, 0))
        if wS > 0: rows.append((ii, key, x, y, z, xe, ye, ze, tS, wS, 1))
ev_i = np.array([r[0] for r in rows]); keys = [r[1] for r in rows]
G = np.array([r[2:10] for r in rows], float); isS = np.array([r[10] for r in rows], bool)
R_pool = np.sqrt((G[:, 0] - G[:, 3]) ** 2 + (G[:, 1] - G[:, 4]) ** 2 + (G[:, 2] - G[:, 5]) ** 2)
zs_pool, ze_pool, tobs_pool, w_pool = G[:, 2], G[:, 5], G[:, 6], G[:, 7]
NEV = len(CAL); MAXP = np.bincount(ev_i, minlength=NEV).max()
slot = np.zeros(len(rows), int); cnt = np.zeros(NEV, int)
for j, i in enumerate(ev_i): slot[j] = cnt[i]; cnt[i] += 1
KID = {k: n for n, k in enumerate(sorted(set(keys)))}; key_arr = np.array([KID[k] for k in keys])
def pool_resid(v0, k, vpvs, cP=None, cS=None):
    TP = tt(R_pool, zs_pool, ze_pool, v0, k); calc = np.where(isS, TP * vpvs, TP)
    if cP is not None: calc = calc + np.array([(cS if s else cP).get(kk, 0.0) for kk, s in zip(keys, isS)])
    res = tobs_pool - calc
    M = np.full((NEV, MAXP), np.nan); M[ev_i, slot] = res
    return res - np.nanmedian(M, axis=1)[ev_i]
def L1(r): return float(np.sum(w_pool * np.abs(r)) / np.sum(w_pool))
def grid_fit(v0s, ks, qs):
    best = (np.inf, None)
    for v0 in v0s:
        for k in ks:
            for q in qs:
                m = L1(pool_resid(v0, k, q))
                if m < best[0]: best = (m, (float(v0), float(k), float(q)))
    return best
b1 = grid_fit(np.arange(4.6, 6.61, 0.2), np.arange(0.0, 0.101, 0.02), np.arange(1.60, 1.861, 0.02)); v0c, kc, qc = b1[1]
b2 = grid_fit(np.arange(v0c - 0.2, v0c + 0.201, 0.05), np.clip(np.arange(kc - 0.02, kc + 0.021, 0.005), 0, None),
              np.arange(qc - 0.02, qc + 0.021, 0.005))
V0, KG, VPVS = b2[1]
cP, cS = {}, {}
for _ in range(3):
    r = pool_resid(V0, KG, VPVS, cP, cS); nP, nS = dict(cP), dict(cS)
    for tgt, sel in ((nP, ~isS), (nS, isS)):
        for kk in set(k for k, s in zip(keys, sel) if s):
            m = (key_arr == KID[kk]) & sel; n = int(m.sum())
            tgt[kk] = tgt.get(kk, 0.0) + float(np.median(r[m])) * n / (n + SHRINK)
    cP, cS = nP, nS
r1 = pool_resid(V0, KG, VPVS, cP, cS)
LAP_B = float(np.median(np.abs(r1)) / np.log(2.0))
print(f"[21_09] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
      f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")

# ---------------------------------------------------------------- 4. 格子と探索(17_02 と同じ)
H = float(max(30.0, np.percentile(np.abs(np.r_[EX[CAL], EY[CAL]]), 99.5) + 30.0))
STEP = float(max(1.0, round(H / 30.0)))
ZMAX = float(max(30.0, np.percentile(SRC[CAL, 2], 99.5) * 1.3 + 10.0))
ZDEF = float(np.mean(SRC[CAL, 2]))
xc = np.arange(-H, H + 1e-6, STEP); zc = np.arange(0.0, ZMAX + 1e-6, STEP)
GX, GY, GZ = np.meshgrid(xc, xc, zc, indexing="ij"); COARSE = np.c_[GX.ravel(), GY.ravel(), GZ.ravel()]
XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
print(f"[21_09] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
      f"  固定の深さ {ZDEF:.1f} km")
def misfit(nodes, pk, dP=None, dS=None):
    xs = np.array([p[1] for p in pk]); ys = np.array([p[2] for p in pk]); zs = np.array([p[3] for p in pk])
    R = np.sqrt((nodes[:, :1] - xs) ** 2 + (nodes[:, 1:2] - ys) ** 2 + (nodes[:, 2:3] - zs) ** 2)
    TP = tt(R, zs[None, :], nodes[:, 2:3], V0, KG)
    obs, calc, w = [], [], []
    for j, p in enumerate(pk):
        eP = (dP or {}).get(p[0], 0.0); eS = (dS or {}).get(p[0], 0.0)      # C4 だけが使う、似た地震からの局の補正
        obs.append(p[4]); calc.append(TP[:, j] + cP.get(p[0], 0.0) + eP); w.append(p[5])
        if p[7] > 0: obs.append(p[6]); calc.append(TP[:, j] * VPVS + cS.get(p[0], 0.0) + eS); w.append(p[7])
    res = np.array(obs)[None, :] - np.stack(calc, axis=1)
    return np.sum(np.array(w)[None, :] * np.abs(res - np.median(res, axis=1, keepdims=True)), axis=1)
def refine(c, step, sub, fix_z=False):
    h = np.arange(-1.5 * step, 1.5 * step + 1e-9, sub)
    zz = np.array([c[2]]) if fix_z else np.arange(max(0.0, c[2] - 1.5 * step), c[2] + 1.5 * step + 1e-9, sub)
    A, B, C = np.meshgrid(c[0] + h, c[1] + h, zz, indexing="ij"); return np.c_[A.ravel(), B.ravel(), C.ravel()]
def argmin_search(score_fn, fix_z):
    N0 = COARSE_Z0 if fix_z else COARSE
    c = N0[int(np.argmin(score_fn(N0)))]
    for st, sub in ((STEP, STEP / 5), (STEP / 5, STEP / 25)):
        N = refine(c, st, sub, fix_z); c = N[int(np.argmin(score_fn(N)))]
    return c
def locate_phys(pk):
    nph = n_phases(pk)
    if nph < 3: return None
    c = argmin_search(lambda N: misfit(N, pk), nph < 4); return float(c[0]), float(c[1])

# ---------------------------------------------------------------- 5. 事前分布(KDE の帯域は pool の一つ抜き。17_02 と同じ)
def loo_ll(h):
    px_, py_ = EX[CAL], EY[CAL]
    d2 = (px_[:, None] - px_[None, :]) ** 2 + (py_[:, None] - py_[None, :]) ** 2
    K = np.exp(-0.5 * d2 / h ** 2); np.fill_diagonal(K, 0.0)
    dens = K.sum(1) / ((len(px_) - 1) * 2 * np.pi * h ** 2); return float(np.mean(np.log(dens + 1e-300)))
HS = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0]
lls = {h: loo_ll(h) for h in HS}; KDE_H = max(lls, key=lls.get)
print(f"[21_09] KDE の帯域(pool の一つ抜き): {KDE_H} km")
def log_prior(nodes, mem):
    d2 = (nodes[:, :1] - EX[mem][None, :]) ** 2 + (nodes[:, 1:2] - EY[mem][None, :]) ** 2
    m = -0.5 * d2 / KDE_H ** 2; mx = m.max(1, keepdims=True)
    lk = mx[:, 0] + np.log(np.exp(m - mx).sum(1)) - np.log(len(mem) * 2 * np.pi * KDE_H ** 2)
    lu = -np.log((2 * H) ** 2)
    return np.logaddexp(np.log(1 - PRIOR_EPS) + lk, np.log(PRIOR_EPS) + lu)
def locate_map(pk, mem, dP=None, dS=None):
    mem = np.asarray(mem, int)
    sc = (lambda N: -log_prior(N, mem)) if n_phases(pk) <= 1 else (lambda N: misfit(N, pk, dP, dS) / LAP_B - log_prior(N, mem))
    c = argmin_search(sc, n_phases(pk) < 4); return float(c[0]), float(c[1])
FIRST = {}
for ie in range(NE):
    if HASP[ie]:
        p0 = min(picks_of(ie), key=lambda q: q[4]); FIRST[ie] = (p0[0], p0[1], p0[2])
def prior_members(cands, first_key, first_pos):
    """17_02 の prior_members と同じ規則を、候補の地震の集合 cands に対して行う"""
    by, pos = {}, {}
    for j in cands:
        by.setdefault(FIRST[j][0], []).append(j); pos[FIRST[j][0]] = (FIRST[j][1], FIRST[j][2])
    mem = list(by.get(first_key, []))
    if len(mem) < MIN_PRIOR_EV:
        for _, k in sorted((np.hypot(pos[k][0] - first_pos[0], pos[k][1] - first_pos[1]), k) for k in by if k != first_key):
            if len(mem) >= MIN_PRIOR_EV: break
            mem += by[k]
    return np.array(mem, int)
def library(ie, buffer_h=BUFFER_H):
    lib = np.where((OTNS <= OTNS[ie] - int(buffer_h * 3600e9)) & HASP)[0]
    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_09] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
    return lib
POOL_OK = np.array(CAL, int)
# C4 の材料: 各地震の、局ごとの走時の残り(観測 − 速度の式 − 局の補正。気象庁の震源と発生時刻を使い、地震ごとに P の中央値を引く)
RES = {}
for ie in range(NE):
    if not HASP[ie]: continue
    e = EVS[ie]; n = int(e["n_real_stations"]); loc = np.asarray(e["sta_locs"], float)[:n]
    tp = np.asarray(e["tp_times"], float)[:n]; sp = np.asarray(e["sp_diffs"], float)[:n]
    pf = np.asarray(e["p_fallback"]).astype(int)[:n]; sf = np.asarray(e["s_fallback"]).astype(int)[:n]
    sx, sy = to_xy(loc[:, 0], loc[:, 1]); sz = -loc[:, 2] * EL_SCALE
    Rr = np.sqrt((sx - EX[ie]) ** 2 + (sy - EY[ie]) ** 2 + (sz - SRC[ie, 2]) ** 2)
    T = tt(Rr, sz, np.full(n, SRC[ie, 2]), V0, KG)
    okP = np.isfinite(tp) & (pf == 0)
    keysE = [skey(l) for l in loc]
    rP = np.array([tp[k] - T[k] - cP.get(keysE[k], 0.0) if okP[k] else np.nan for k in range(n)])
    med = float(np.nanmedian(rP))
    dPj = {keysE[k]: float(rP[k] - med) for k in range(n) if okP[k]}
    dSj = {keysE[k]: float(tp[k] + sp[k] - T[k] * VPVS - cS.get(keysE[k], 0.0) - med) for k in range(n)
           if okP[k] and sf[k] == 0 and np.isfinite(sp[k])}
    RES[ie] = (dPj, dSj)
def corr_from(top, pk):
    """C4: 上位の似た地震の、届いた局ごとの走時の残りの中央値(MIN_CORR 地震以上で持つ局だけ。無い局は 0)"""
    dP, dS = {}, {}
    for p in pk:
        vP = [RES[j][0][p[0]] for j in top if p[0] in RES[j][0]]
        if len(vP) >= MIN_CORR: dP[p[0]] = float(np.median(vP))
        vS = [RES[j][1][p[0]] for j in top if p[0] in RES[j][1]]
        if len(vS) >= MIN_CORR: dS[p[0]] = float(np.median(vS))
    return dP, dS

# ---------------------------------------------------------------- 6. 波形の似ている度合い(因果フィルタ)
NKEEP = IP + int(round((MAX_WIN_S + MAX_LAG_S) * FS)) + 2
PRE_N, LAG_N, MINW_N = int(round(PRE_S * FS)), int(round(MAX_LAG_S * FS)), int(round(MIN_WIN_S * FS))
SOS = {b: butter(4, b, btype="bandpass", fs=FS, output="sos") for b in (BAND, BAND_SENS)}
FILT = {}
def filt_cached(ie, band):
    """局 key -> (3, NKEEP) の因果フィルタ後の波形(P を測った局だけ)"""
    if (ie, band) not in FILT:
        e = EVS[ie]; n = int(e["n_real_stations"]); W = np.asarray(e["waveforms"], float)[:n]
        loc = np.asarray(e["sta_locs"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
        FILT[(ie, band)] = {skey(loc[k]): sosfilt(SOS[band], W[k], axis=-1)[:, :NKEEP] for k in range(n) if pf[k] == 0}
    return FILT[(ie, band)]
def n_avail(tau, tpr):
    """窓の中の P からの点の数(時刻 ≤ τ − 0.01 s の最後の点まで)"""
    return int(np.floor((min(tau, tpr + MAX_WIN_S) - tpr) * FS + 1e-3))
def target_windows(ie, tau, band):
    F = filt_cached(ie, band); out = []
    for p in picks_of(ie, tau):
        nav = n_avail(tau, p[4])
        if nav < MINW_N or p[0] not in F: continue
        out.append((p[0], F[p[0]][:, IP - PRE_N: IP + nav]))        # 最後の点は IP + nav − 1(時刻 tp + (nav − 1)/100 ≤ τ − 0.01)
    return out
def similarity(ie, tau, lib, band, raw=False):
    """S_ij(lib の順)と n_i。raw=True は陽性対照用(局の値を 0 で切らない)"""
    tw = target_windows(ie, tau, band)
    S = np.zeros(len(lib)); ni = len(tw)
    if ni == 0: return S, 0
    for jj, j in enumerate(lib):
        Fj = filt_cached(j, band); acc = 0.0
        for key, x in tw:
            if key not in Fj: continue
            y = Fj[key]; L = x.shape[1]; xv = x.ravel(); nx = np.linalg.norm(xv)
            if nx == 0: continue
            best = -np.inf if raw else 0.0
            for l in range(-LAG_N, LAG_N + 1):
                yv = y[:, IP - PRE_N + l: IP - PRE_N + l + L].ravel(); ny = np.linalg.norm(yv)
                if ny > 0: best = max(best, float(xv @ yv) / (nx * ny))
            acc += best if np.isfinite(best) else 0.0
        S[jj] = acc / ni
    return S, ni
def c_from(S, lib, pk, m3, m6r, k, ie=None, with_c4=True):
    """C1・C2・C3・C4。S > 0 の過去の地震が MIN_POS 未満なら C3 = C4 = M6r(C1・C2 は値なし)"""
    pos = int((S > 0).sum())
    if pos < MIN_POS: return dict(C1=None, C2=None, C3=m6r, C4=m6r, fb=True, top1=None, top=None, ncorr=0)
    top = lib[np.argsort(-S, kind="stable")[:min(k, pos)]]
    if ie is not None and ie in top: stop("[21_09] STOP: 自分自身が似た地震の上位に入っている")
    out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
               C3=locate_map(pk, top), C4=None, fb=False, top1=int(top[0]), top=top, ncorr=0)
    if with_c4:
        dP, dS = corr_from(top, pk)
        out["C4"] = locate_map(pk, top, dP, dS); out["ncorr"] = len(dP)
    return out
# ============================================================================= 21_09a ここから(評価)
LIMITS_09 = ["the sparse networks are subsets of Hi-net stations chosen by a position-only farthest-point rule (N stations, random first "
             "station); real sparse networks (ocean-bottom, other station types, other regions) differ",
             "the cache was built on the dense network: events needed >= 4 picks there (some would be missed by a sparse network), and the "
             "Wadati S-P quality check used all of an event's stations, so removed stations influenced which S picks of kept stations survive",
             "the cache keeps at most 24 stations per event (measured-P stations ordered by earliest P, then fallback picks); stations beyond "
             "the 24th in the full network are unavailable in the thinned network; candidate stations are those appearing in the cache",
             "each network is evaluated on the test events with a P pick at its kept stations, so trends across networks compare different "
             "event sets and are descriptive",
             "truth, past-event locations and C4 station terms are JMA hypocentres determined with the dense network; in a region that only "
             "has a sparse network the past-event locations would be worse, so C3/C4 here are optimistic",
             "same limits as 21_04 (one sequence, offline PhaseNet picks, no picking or telemetry latency, small events, the 2016 test "
             "carries a documented deviation: amendment 03)"]
EVAL = test_idx[HASP[test_idx]]
if a.limit: EVAL = EVAL[:a.limit]
N_LOST = int(len(test_idx) - int(HASP[test_idx].sum()))       # 残した局で P を測れず外れた試験の地震(--limit の前)
NT = len(EVAL); TESTABLE = NT >= MIN_TEST
print(f"[21_09] 評価: 試験の地震 {len(test_idx)} のうち、残した局で P を測れた地震 {NT}" + (f"(--limit {a.limit}: 動作確認、判定に使わない)" if a.limit else ""))
if NT == 0: stop("[21_09] STOP: 評価できる地震が 0")
if not TESTABLE: print(f"[21_09] 注意: 評価できる地震 {NT} < {MIN_TEST}。この網は「試せない」(21_04 の INCONCLUSIVE と同じ規則)。記述は出す")
BASE = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]
METH = BASE + ["C3", "C4"]
TL = [f"{t:g}" for t in TAUS] + ["inf"]
def eval_event(ie, only_tau=None):
    """21_04 v1 の eval_event と同じ計算(C1・C2・感度・全検測の C3/C4 は省く)。C3・C4 の S は主の一覧で計算(21_04 と同じ値)"""
    lib = library(ie); p0 = FIRST[ie]
    m3 = prior_members(lib, p0[0], (p0[1], p0[2])); m3p = prior_members(POOL_OK, p0[0], (p0[1], p0[2]))
    R = {m: np.full((len(TL), 2), np.nan) for m in METH}
    X = dict(nst=np.zeros(len(TL), int), ni=np.zeros(len(TAUS), int), smax=np.full(len(TAUS), np.nan), fb=np.zeros(len(TAUS), bool),
             ncorr=np.zeros(len(TAUS), int))
    for jt, t in enumerate(TL):
        if only_tau is not None and t != only_tau: continue
        tau = np.inf if t == "inf" else float(t); pk = picks_of(ie, tau); X["nst"][jt] = len(pk)
        R["M0r"][jt] = (EX[lib].mean(), EY[lib].mean())
        R["Mp10"][jt] = (EX[lib[-10:]].mean(), EY[lib[-10:]].mean())
        R["M1"][jt] = (p0[1], p0[2])
        R["M2"][jt] = (np.mean([p[1] for p in pk]), np.mean([p[2] for p in pk]))
        R["M3r"][jt] = (float(np.median(EX[m3])), float(np.median(EY[m3])))
        r = locate_phys(pk)
        if r is not None: R["M5"][jt] = r
        R["M5f"][jt] = r if r is not None else (p0[1], p0[2])
        R["M6p"][jt] = locate_map(pk, m3p)
        m6r = locate_map(pk, m3); R["M6r"][jt] = m6r
        if t == "inf": continue
        S, ni = similarity(ie, tau, lib, BAND)
        o = c_from(S, lib, pk, m3, m6r, TOPK, ie=ie)
        R["C3"][jt], R["C4"][jt] = o["C3"], o["C4"]
        X["ni"][jt], X["smax"][jt], X["fb"][jt], X["ncorr"][jt] = ni, (float(S.max()) if ni > 0 and len(S) else np.nan), o["fb"], o["ncorr"]
    return R, X
P = {m: np.full((NT, len(TL), 2), np.nan) for m in METH}
NST = np.zeros((NT, len(TL)), int); NI = np.zeros((NT, len(TAUS)), int); C3FB = np.zeros((NT, len(TAUS)), bool)
NCORR = np.zeros((NT, len(TAUS)), int); SMAX = np.full((NT, len(TAUS)), np.nan)
T_EV = time.time()
for ii, ie in enumerate(EVAL):
    try:
        R, X = eval_event(ie)
    except SystemExit:
        raise
    except BaseException as ex:
        stop(f"[21_09] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
    for m in METH: P[m][ii] = R[m]
    NST[ii], NI[ii], C3FB[ii], NCORR[ii], SMAX[ii] = X["nst"], X["ni"], X["fb"], X["ncorr"], X["smax"]
    if (ii + 1) % 20 == 0:
        el = time.time() - T_EV
        print(f"  … {ii+1}/{NT}  ({time.time()-T0:.0f} s、残りの見込み約 {el / (ii + 1) * (NT - ii - 1) / 60:.0f} 分)", flush=True)

# ---------------------------------------------------------------- G-causal(21_04 と同じ手順)
gate_ev = [ii for ii in range(NT) if NI[ii, TAUS.index(1.0)] > 0][:N_GATE]
GC = dict(status="not checked (fewer than 3 events with a similarity at tau = 1 s)", max_diff=None, positive_control=None, n_checks=0)
if len(gate_ev) >= 3:
    gc_max, gc_n = 0.0, 0
    for ii in gate_ev:
        ie = EVAL[ii]; orig = EVS[ie]
        for t in ("0.5", "1", "2", "3"):
            tau = float(t); jt = TL.index(t)
            e2 = dict(orig); n = int(orig["n_real_stations"])
            W = np.array(np.asarray(orig["waveforms"], float)); tp = np.array(np.asarray(orig["tp_times"], float))
            sp = np.array(np.asarray(orig["sp_diffs"], float)); tpr = tp[:n] - TFIRST[ie]
            for k in range(n):
                if np.isfinite(tpr[k]) and tpr[k] <= tau + EPS_T:
                    cut = IP + max(n_avail(tau, tpr[k]), 0)
                    if not (tpr[k] + sp[k] <= tau + EPS_T): sp[k] += RNG_GATE.uniform(0.5, 2.0)
                else:
                    cut = 0; tp[k] += RNG_GATE.uniform(0.5, 2.0); sp[k] += RNG_GATE.uniform(0.5, 2.0)
                W[k, :, cut:] = RNG_GATE.standard_normal((3, NTS - cut)) * 1e3
            e2["waveforms"], e2["tp_times"], e2["sp_diffs"] = W, tp, sp
            EVS[ie] = e2; [FILT.pop((ie, b), None) for b in SOS]
            R2, X2 = eval_event(ie, only_tau=t)
            EVS[ie] = orig; [FILT.pop((ie, b), None) for b in SOS]
            for m in METH:
                a1, a2 = P[m][ii, jt], R2[m][jt]
                if np.isnan(a1).any() != np.isnan(a2).any(): gc_max = np.inf
                elif not np.isnan(a1).any(): gc_max = max(gc_max, float(np.max(np.abs(a1 - a2))))
            j0 = TAUS.index(tau)
            if np.isfinite(SMAX[ii, j0]) or np.isfinite(X2["smax"][j0]):
                gc_max = max(gc_max, abs(np.nan_to_num(SMAX[ii, j0], nan=-9.0) - np.nan_to_num(X2["smax"][j0], nan=-9.0)))
            gc_n += 1
    pos_ctrl, shared = None, []
    for _ii in gate_ev:                                  # 過去の地震と局を共有する最初のゲートの地震で陽性対照
        ie = EVAL[_ii]; orig = EVS[ie]; lib0 = library(ie)
        shared = [p for p in picks_of(ie, 1.0) if n_avail(1.0, p[4]) >= MINW_N and any(p[0] in filt_cached(j, BAND) for j in lib0)]
        if shared: break
    if shared:
        S0, _ = similarity(ie, 1.0, lib0, BAND, raw=True)
        pc = shared[0]; e2 = dict(orig); W = np.array(np.asarray(orig["waveforms"], float))
        W[pc[8], :, IP + n_avail(1.0, pc[4]) - 1] += 50.0 * np.abs(W[pc[8], :, IP:IP + 100]).max()
        e2["waveforms"] = W; EVS[ie] = e2; [FILT.pop((ie, b), None) for b in SOS]
        S1, _ = similarity(ie, 1.0, lib0, BAND, raw=True)
        EVS[ie] = orig; [FILT.pop((ie, b), None) for b in SOS]
        pos_ctrl = float(np.max(np.abs(S1 - S0))) if len(S0) else 0.0
    ok = gc_max == 0.0 and (pos_ctrl > 0 if pos_ctrl is not None else a.n_keep > 0)    # 間引いた網で陽性対照の局が無い時は記録だけ
    GC = dict(status=("PASS" if ok else "FAIL") + ("" if pos_ctrl is not None else " (positive control not available: no shared station)"),
              max_diff=gc_max, positive_control=pos_ctrl, n_checks=gc_n)
    print(f"[21_09] G-causal({len(gate_ev)} 地震 × 4 時点): 最大の差 {gc_max:.3g}  陽性対照 {pos_ctrl}  {GC['status']}")
    if not ok: stop("[21_09] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")
else:
    print(f"[21_09] G-causal: {GC['status']}(計算のコードは N = 0 と同じ)")
    if a.n_keep == 0: stop("[21_09] STOP(G-causal): 間引かない網で確かめられない(この行を貼って相談)")

# ---------------------------------------------------------------- 誤差・G-same・規則
def herr(Pm):
    out = np.full(Pm.shape[:2], np.nan)
    for i, ie in enumerate(EVAL):
        for j in range(Pm.shape[1]):
            if np.isfinite(Pm[i, j, 0]):
                la, lo = to_ll(Pm[i, j, 0], Pm[i, j, 1]); out[i, j] = km_between(la, lo, SRC[ie, 0], SRC[ie, 1])
    return out
E = {m: herr(P[m]) for m in METH}
GSAME = None
if a.n_keep == 0:
    CSVP = ROOT / "data/21_04_per_event.csv"
    if not CSVP.exists(): stop("[21_09] STOP(G-same): data/21_04_per_event.csv(21_04 の本番の出力)が無い")
    with open(CSVP) as f: R4 = {r["origin_time"]: r for r in csv.DictReader(f)}
    worst, nchk, bad = 0.0, 0, []
    if not a.limit and set(R4) != {OT[ie] for ie in EVAL}: bad.append(f"評価する地震の集合が違う(21_04 {len(R4)}・21_09 {NT})")
    for i, ie in enumerate(EVAL):
        r = R4.get(OT[ie])
        if r is None: stop(f"[21_09] STOP(G-same): {OT[ie]} が 21_04 の CSV に無い")
        for j, t in enumerate(TL):
            if int(r[f"n_sta_t{t}"]) != int(NST[i, j]): bad.append(f"{OT[ie][:19]} n_sta τ={t}")
            for m in (BASE if t == "inf" else METH):
                v = r.get(f"{m}_err_t{t}", ""); x = E[m][i, j]
                if (v in ("", None)) != (not np.isfinite(x)): bad.append(f"{OT[ie][:19]} {m} τ={t} 空の有無"); continue
                if v in ("", None): continue
                dlt = abs(round(float(x), 4) - float(v)); worst = max(worst, dlt); nchk += 1
                if dlt > 6e-5: bad.append(f"{OT[ie][:19]} {m} τ={t} {x:.4f} 対 {float(v):.4f}")
    GSAME = dict(n_values=nchk, max_abs_diff_km=worst, n_mismatch=len(bad), status=("PASS" if not bad else "FAIL"))
    print(f"[21_09] G-same(21_04 の CSV と、{NT} 地震 × 9 方法・C3・C4 × 時点 = {nchk} 値・局の数・地震の集合): 最大の差 {worst:.2g} km  不一致 {len(bad)}  {GSAME['status']}")
    if bad: stop("[21_09] STOP(G-same): 21_04 と値が違う。最初の 5 件: " + " / ".join(bad[:5]))
RNG_BOOT = np.random.default_rng(SEED)
def med_ci(x):
    x = x[np.isfinite(x)]
    if len(x) == 0: return (None, None, None)
    bs = np.median(x[RNG_BOOT.integers(0, len(x), (NBOOT, len(x)))], axis=1)
    return (float(np.median(x)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))
SUMM = {m: {t: dict(zip(("median_km", "ci_lo", "ci_hi"), med_ci(E[m][:, j])), available=float(np.mean(np.isfinite(E[m][:, j]))))
            for j, t in enumerate(TL)} for m in METH}
def paired(A, B, j):
    x, y = E[A][:, j], E[B][:, j]; m = np.isfinite(x) & np.isfinite(y); nz = int(np.sum(x[m] != y[m]))
    d = dict(n=int(m.sum()), n_nonzero=nz, p=None, median_diff_km=None, frac_better=None, frac_tied=None)
    if m.sum() == 0: return d
    d.update(median_diff_km=float(np.median(x[m] - y[m])), frac_better=float(np.mean(x[m] < y[m])), frac_tied=float(np.mean(x[m] == y[m])))
    if nz >= 6: d["p"] = float(wilcoxon(x[m], y[m], alternative="less", zero_method="wilcox").pvalue)
    return d
def judge(meth, t, alpha):
    j = TL.index(t)
    full = [m for m in BASE if SUMM[m][t]["available"] == 1.0 and SUMM[m][t]["median_km"] is not None]
    if not full: return dict(method=meth, tau=t, alpha=alpha, best=None, win=False, testable=False, floor=False, note="no AI-free method gives every event a value")
    best = min(full, key=lambda m: SUMM[m][t]["median_km"])
    bm, cm = SUMM[best][t]["median_km"], SUMM[meth][t]["median_km"]
    pr = paired(meth, best, j); floor = bm < FLOOR_KM
    win = TESTABLE and (not floor) and cm is not None and cm < bm and pr["p"] is not None and pr["p"] < alpha and pr["n_nonzero"] >= MIN_NONZERO
    return dict(method=meth, tau=t, alpha=alpha, best=best, best_median_km=bm, median_km=cm, paired_vs_best=pr, floor=bool(floor), win=bool(win),
                testable=bool(TESTABLE), gain_km=(None if cm is None else bm - cm))
PER_TAU = {}
for j, t in enumerate(TL[:-1]):
    PER_TAU[t] = dict(C3=judge("C3", t, ALPHA), C4=judge("C4", t, ALPHA_SEC), C4_vs_C3=paired("C4", "C3", j),
                      c3_fallback_frac=float(C3FB[:, j].mean()), similarity_measured_frac=float(np.mean(NI[:, j] > 0)),
                      stations_median=float(np.median(NST[:, j])))
phys_inf = SUMM["M5"]["inf"]["median_km"]
# まばらさの記述: 最初の P の局の震央距離・最初の P の時刻(気象庁の発生時刻から、s)
FD = np.array([km_between(*to_ll(FIRST[ie][1], FIRST[ie][2]), SRC[ie, 0], SRC[ie, 1]) for ie in EVAL])
FT = np.array([TFIRST[ie] for ie in EVAL])
SPARSE = dict(test_events_lost_no_p=N_LOST, first_station_epi_km_median=float(np.median(FD)), first_p_after_origin_s_median=float(np.median(FT)),
              stations_with_p_median={t: float(np.median(NST[:, j])) for j, t in enumerate(TL)})
def f2(v): return "—" if v is None else f"{v:.2f}"
def fp(p): return "—" if p is None else f"{p:.2g}"
print(f"\n[21_09] ===== 網 {TAG}: 水平誤差の中央値 km(評価 {NT} 地震) =====")
print(f"  局 {len(KEEP)}・最近接の間隔の中央値 {f2(NN_KEEP)} km・P を測れず外れた試験の地震 {N_LOST}・最初の P の局の震央距離 {f2(SPARSE['first_station_epi_km_median'])} km・"
      f"最初の P は発生から {f2(SPARSE['first_p_after_origin_s_median'])} s(中央値)")
print("  P のある局の数(中央値) " + "  ".join(f"τ={t}: {np.median(NST[:, j]):.0f}" for j, t in enumerate(TL)))
for t, d in PER_TAU.items():
    for m in ("C3", "C4"):
        h = d[m]
        if h.get("best") is None: print(f"  τ={t} s {m}: BEST なし"); continue
        pb = h["paired_vs_best"]
        print(f"  τ={t} s {m}: BEST = {h['best']} {h['best_median_km']:.2f} km / {m} {f2(h['median_km'])} km(差 {f2(h['gain_km'])})  "
              f"p = {fp(pb['p'])}(基準 {h['alpha']}、差が 0 でない組 {pb['n_nonzero']}/{pb['n']})  FLOOR={h['floor']}  → {'勝ち' if h['win'] else '勝ちなし'}")
print(f"  全検測の M5(物理だけ)の中央値 {f2(phys_inf)} km(G-phys は記録だけ)")
print("[21_09] 限界: " + " / ".join(LIMITS_09))

# ---------------------------------------------------------------- 出力
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
with open(ROOT / f"data/21_09_per_event_{TAG}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["origin_time", "mj", "lat", "lon", "depth_km", "first_p_after_origin_s", "first_station_epi_km"] + [f"n_sta_t{t}" for t in TL]
               + [f"c3_fallback_t{t}" for t in TL[:-1]] + [f"{m}_err_t{t}" for m in METH for t in (TL if m in BASE else TL[:-1])])
    for i, ie in enumerate(EVAL):
        w.writerow([OT[ie], f"{MAG[ie]:.1f}", f"{SRC[ie,0]:.4f}", f"{SRC[ie,1]:.4f}", f"{SRC[ie,2]:.2f}", f"{FT[i]:.3f}", f"{FD[i]:.3f}"]
                   + [int(v) for v in NST[i]] + [int(v) for v in C3FB[i]]
                   + [("" if not np.isfinite(E[m][i, j]) else f"{E[m][i, j]:.4f}") for m in METH for j in (range(len(TL)) if m in BASE else range(len(TAUS)))])
out = dict(script="21_09a_ct2016_sparse_network.py", version=VERSION, script_sha256=SELF_SHA, tag=TAG, limit=a.limit,
           sequence="Central Tottori 2016", cache=a.cache, cache_sha256=sha256(CP),
           network=dict(n_keep=a.n_keep, seed=a.seed, first_station_index=START, n_stations_all=len(STK), n_stations_kept=len(KEEP),
                        nn_spacing_median_km_all=NN_ALL, nn_spacing_median_km_kept=NN_KEEP, kept_stations_latlon=[ALLST[k] for k in sorted(KEEP)],
                        pick_rows_before=n_before, pick_rows_after=n_after),
           configs=CONFIGS, n_test=int(len(test_idx)), n_evaluated=NT, testable=bool(TESTABLE), min_test=MIN_TEST, velocity=dict(v0=V0, k=KG, vpvs=VPVS), laplace_b_s=LAP_B, kde_h_km=KDE_H,
           grid=dict(H_km=H, step_km=STEP, zfix_km=ZDEF), gates=dict(causal=GC, same=GSAME, physics_inf_median_km=phys_inf),
           sparseness=SPARSE, summary=SUMM, per_tau=PER_TAU,
           rule="per network: C4 at tau = 2 s wins vs BEST (smaller median, one-sided paired Wilcoxon p < 0.005, >= 10 non-zero pairs, "
                "BEST >= 0.5 km, >= 30 evaluated events); per N in (12, 8, 5): wins in 3/3 seeds = HOLDS, 1-2 = MIXED, 0 = FAILS (untestable "
                "or floor networks count as no win); overall SPARSE-HOLDS if all HOLDS, SPARSE-FAILS if all FAILS, SPARSE-PARTIAL otherwise "
                "(aggregated by 21_09b)",
           limits=LIMITS + LIMITS_09, runtime_s=time.time() - T0)
json.dump(clean(out), open(ROOT / f"models/21_09_run_{TAG}.json", "w"), indent=1)
print(f"[21_09] 出力: models/21_09_run_{TAG}.json・data/21_09_per_event_{TAG}.csv  ({time.time()-T0:.0f} s)")
