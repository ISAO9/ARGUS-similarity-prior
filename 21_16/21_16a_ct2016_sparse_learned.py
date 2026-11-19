#!/usr/bin/env python3
# =============================================================================
# Script : 21_16a_ct2016_sparse_learned.py  (v2)
#          [鳥取 2026 で学習して凍結した「似た地震の選び方」(21_06a の L4)を、21_09 と同じ「間引いたまばらな網」9 つ(+ 間引かない網)の
#           鳥取県中部 2016 にそのまま当てる。局が少ない網でも、学習した選び方 × 物理(L4)が物理だけ(BEST)に勝つかを網ごとに 1 回だけ試す]
# Project: ARGUS(新生)— 論文の柱「1〜2 局・単一開口の震源決定」。21_09(人が決めた選び方 C4 の間引き試験)の学習型版
#
# なぜ必要か:
#   21_06b で凍結した L4 は、間引かない網の 2016 で BEST に勝った(HL1)。ただし L4 の特徴量のうち物理の手がかり(候補との共通の局の数
#   n_common_picks・二重差の dd_*。dd_offset_km と dd_fit_rms_s は共通の局 4 つ以上が要る)は、局が 1〜2 しか無いと小さくなるか消える(nan)。
#   学習は密な網(鳥取 2026)だけなので、まばらな網では特徴量の分布が学習の時とずれる。まばらな網でも L4 が BEST に勝つかは、まだ確かめていない。
#
# 何をするか(1 回の実行 = 1 つの網。網は 21_09 と同じ 10: 間引かない + N = 12・8・5 局 × 種 0・1・2):
#   1. 21_09a v1 の 1.〜6.(入力・1b. 間引き・pool での較正のやり直し・格子・事前分布・似ている度合い)を写す(表示の [21_09] を [21_16] に
#      変えただけ)。間引きは --n-keep N・--seed s で 21_09a と同じ(最遠点、最初の局は乱数の種 1000 + s)。
#   2. 21_06b v1 の 7. 速い S と、21_06 FEATURES の印の間(特徴量・learned_top・l_from)を 1 字も変えずに写す。
#   3. 入力の確認(どれか 1 つでも違えば STOP。試験を開く前):
#      G-core: src/21_09a_ct2016_sparse_network.py の SHA-256 が事前登録した 21_09a v1(f74c9082…)で、その 1.〜6. の部分が、この版の 1.〜6.
#        と([21_09] → [21_16] の置き換えの後で)1 字も違わない。src/21_06b_ct2016_learned_test.py の SHA-256 が models/21_06b_judgment.json の
#        script_sha256 と同じで、その 7. と FEATURES の部分が、この版のその部分と 1 字も違わない。
#      G-feat: 特徴量の部分の SHA-256 = models/21_06a_train.json の feature_block_sha256(= 21_06a・21_06b と同じ計算)。
#      G-model: モデルと学習の行の SHA-256 = 学習の記録。scikit-learn・numpy の版・特徴量の名前・設定・特徴量が使う定数も同じ。
#      G-frozen(v2): モデル・学習の行・学習の記録・21_06b のスクリプトの SHA-256 が、21_06 の事前登録の記録 6 節(凍結 B)の値と同じ(全桁)。
#        学習の記録は models/21_06a_train.json(mode train、名前に _rerun なし)だけを受け付ける。
#      G-ref06b: models/21_06b_judgment.json が 21_06b の最初の本番(mode test、名前に _rerun なし)で、モデル・特徴量の部分・キャッシュの
#        SHA-256 がこの実行と同じ。
#      G-ref09: models/21_09_run_<網>.json が 21_09a v1(f74c9082…)の結果で、同じキャッシュ・同じ N と seed、残した局(緯度・経度の一覧)と
#        最初の局がこの実行と同じ。--limit なし(本番)では 21_09a の本番(limit 0)の結果だけを使う。
#   4. 1 回だけの記録 models/21_16_opened.json に「網 <網> を開いた」と書く(3. が全て通った後)。止まった時・途中の例外もその理由を書く。
#      終わった網(models/21_16_run_<網>.json がある)をもう一度回すと、結果は _rerun_<UTC の時刻> の名前に書く(前の結果は上書きしない。
#      判定に使うのは最初のもの)。--limit の動作確認も、名前に _limitN を付けて記録する。
#   5. 評価の地震(21_09a と同じ。試験の地震のうち、残した局で P を測れた地震)ごと、τ = 0.5・1・2・3 s ごとに:
#      9 方法(M0r・Mp10・M1・M2・M3r・M5・M5f・M6p・M6r。τ = ∞ も)・C3・C4 を 21_09a と同じ計算で(S は 21_06b と同じ速い S)、
#      L3・L4 を 21_06b と同じ計算で出す(L3 = 凍結したモデルが近いと見積もった上位 10 地震の事前分布 × 物理、L4 = L3 + その 10 地震の
#      通り道の補正。S > 0 の候補が 5 未満なら M6r に戻る)。誤差(気象庁の震央との水平距離)は 21_06b と同じく小数 4 桁に丸めてから比べる。
#   6. 計算の確認(違えば STOP。結果は書かない):
#      G-same: 9 方法(τ = ∞ も)・C3・C4 の誤差と、P のある局の数・C3 が M6r に戻ったか が data/21_09_per_event_<網>.csv と同じ(誤差は
#        6e-5 km 以内・空の有無も同じ)、評価する地震の集合も同じ(--limit の時は部分集合)。
#      G-same-L(間引かない網だけ): L3・L4 の誤差と L が M6r に戻ったか が data/21_06b_per_event.csv と同じ(6e-5 km 以内)。
#      G-causal(21_09a の手順に L3・L4 を足したもの): 未来の波形と検測を入れ替えても全ての方法の位置と S の最大が同じ + 陽性対照
#        (21_09a と同じ遅い S と、学習の特徴量)。間引いた網で確かめられる地震が 3 未満なら「確かめられず」と記録して続ける
#        (21_09a と同じ規則。間引かない網では止める)。
#   7. 記述(判定に使わない): τ ごとに、学習の特徴量の様子(候補の共通の局の数の中央値・dd_offset_km が nan の候補の割合)と、
#      凍結したモデルの学習の行(2026)の同じ τ の値(分布のずれの目安)、L が M6r に戻った割合、誤差が 10 km を超えた地震の割合
#      (BEST・C4・L4。すそは除かない)、上位 10 地震の本当の距離の中央値(C と L)。
#
# 事前に決めた判定(21_16_preregistration.md。この版の SHA-256 を記録に書いて push してから本番。集計と分類は 21_16b):
#   網ごと(主): τ = 2 s の L4 が BEST(その網で、評価する全ての地震で値がある 9 方法の中で中央値が最小)に勝つ = L4 の中央値が小さい・
#     片側の対応 Wilcoxon(zero_method='wilcox')の p < 0.005・差が 0 でない組 10 以上・BEST ≥ 0.5 km・評価できる地震 30 以上
#     (21_09 の C4 と同じ規則)。
#   各 N(12・8・5): 勝った網が 3/3 = HOLDS、1〜2/3 = MIXED、0/3 = FAILS(試せない網・床の網は勝ちに数えず、数を別に出す)。
#   全体: 全て HOLDS → L4-SPARSE-HOLDS、全て FAILS → L4-SPARSE-FAILS、それ以外 → L4-SPARSE-PARTIAL。
#   記述だけ: L4 対 C4(同じ規則・α 0.005 で数えるが判定に使わない)・L3 @ τ = 0.5 s 対 BEST・他の τ・C4 対 BEST(21_09 の再現)・
#     間引かない網(21_06b の再現)。
#
# 限界(表示と JSON にも英語で書く):
#   - 21_09a の限界の全て(Hi-net の局の部分集合で作った仮想の網・密な網で作ったキャッシュ・過去の地震の位置と正解は密な網の気象庁の震源・
#     網ごとに評価する地震の集合が違う など)と 21_04・21_06b の限界
#   - モデルは密な網の鳥取 2026 だけで学習して凍結した。まばらな網では特徴量の分布がずれる(物理の手がかりが消える)。学び直しはしない
#   - 2016 は逸脱を開示した試験(変更の記録 03)。遠い局の早すぎる検測(取り違え)による誤差のすそがある(21_15)。主の試験ではすそを除かない
#   - 2016 の試験の地震は 21_04・21_06b・21_09 で既に開いている。この試験で新しく見るのは「間引いた網での L3・L4」だけ
#
# Usage : cd ~/SWIFT && caffeinate -i uv run python src/21_16a_ct2016_sparse_learned.py --all
#           (10 の網を順に、別のプロセスで実行。同じ版・同じキャッシュで終わった網は飛ばすので、途中で止まっても同じコマンドで続きから)
#         1 つだけ: ... --n-keep 8 --seed 1   /   動作確認: ... --all --limit 8(結果は _limit8 の名前。判定に使わない。開いた記録には残る)
# 入力  : 21_09a と同じキャッシュ、models/21_09_run_<網>.json・data/21_09_per_event_<網>.csv(21_09a の本番。--limit の時、本番の CSV が
#         無ければ同じ --limit の結果)、models/21_06a_train.json・models/21_06_ranker.pkl・data/21_06a_train_rows.npz(21_06a)、
#         models/21_06b_judgment.json・data/21_06b_per_event.csv(21_06b の本番)、src/21_09a_ct2016_sparse_network.py・src/21_06b_ct2016_learned_test.py
# Output: models/21_16_run_<網>.json・data/21_16_per_event_<網>.csv・models/21_16_opened.json(<網> = full、N12_s0 … N5_s2)
# 次に  : 21_16b_sparse_learned_summary.py --expect-sha <事前登録の記録に書いた 21_16a の SHA-256>
# 所要  : CPU のみ。網ごとに 21_09a の時間(間引かない網 約 16 分、間引いた網 2〜12 分)の約 1.0〜1.3 倍(モックの --limit 8 では
#         21_09a とほぼ同じ時間: 遅い S を速い S に替えた分で、特徴量・L3/L4 の分が相殺された。本物の大きさでは未確かめなので幅を取る)。
#         10 の網で合わせて約 1〜2 時間の見込み。10 地震ごとに進み具合と残りの見込みを表示する
# 止める条件(STOP): 21_09a と同じもの・G-core・G-feat・G-model・G-frozen・G-ref06b・G-ref09・G-same・G-same-L・G-causal
# v2 の変更(数値の計算は v1 と同じ): 1 回だけの記録と結果の JSON を一時ファイル経由で書く(途中で止まっても壊れない)。記録が読めない時は
#   空で上書きせずに止める。SHA-256 を全桁で表示。G-frozen を足した。scipy の版を結果の JSON に残す(Wilcoxon の計算法が版で変わりうるため)。
# =============================================================================
import json, argparse, time, csv, hashlib, math, warnings, datetime as dt
from pathlib import Path
import numpy as np
import torch
from scipy.signal import butter, sosfilt
from scipy.stats import wilcoxon
warnings.filterwarnings("ignore", message="All-NaN slice")

ap = argparse.ArgumentParser()
ap.add_argument("--cache", default="data/ct2016_processed/tottori_parsed_realpick_ct2016_m15.pt", help="15_01c v3.3 の鳥取県中部 2016 の M>=1.5 版(21_09a と同じ)")
ap.add_argument("--n-keep", type=int, default=0, help="残す局の数 N(0 = 間引かない)。21_09a と同じ")
ap.add_argument("--seed", type=int, default=0, help="最初の局を選ぶ乱数の種(1000 + seed)。21_09a と同じ")
ap.add_argument("--all", action="store_true", help="事前に決めた 10 の網を、別のプロセスで順に実行する(終わった網は飛ばす)")
ap.add_argument("--force", action="store_true", help="--all で、別の版の結果がある網も回す(本番の網は _rerun_<UTC> の名前で、判定には使わない。--limit の結果は上書き)")
ap.add_argument("--limit", type=int, default=0, help="動作確認用: 評価の地震を先頭から N 個だけ(結果は _limitN の名前。判定に使わない)")
ap.add_argument("--train-json", default="models/21_06a_train.json", help="21_06a の学習の記録(本番はこれ以外を受け付けない)")
a = ap.parse_args()
CONFIGS = [(0, 0)] + [(N, s) for N in (12, 8, 5) for s in (0, 1, 2)]       # 21_09 と同じ網(変えたら版を上げる)
def tag_of(N, s, lim): return ("full" if N == 0 else f"N{N}_s{s}") + (f"_limit{lim}" if lim else "")
EST_MIN = {0: (16, 22), 12: (6, 16), 8: (4, 12), 5: (2, 8)}                 # 網 1 つの所要の見込み(分。21_09a の時間 × 1.0〜1.3)
if a.all:
    import subprocess, sys
    _root = Path(__file__).resolve().parent.parent
    def _sha(p):
        h = hashlib.sha256()
        with open(p, "rb") as f_:
            for b in iter(lambda: f_.read(1 << 20), b""): h.update(b)
        return h.hexdigest()
    _me, _cs = _sha(Path(__file__)), (_sha(_root / a.cache) if (_root / a.cache).exists() else None)
    print(f"[21_16] 本スクリプト SHA-256 {_me}  --all: 10 の網を順に回す(合わせて約 "
          f"{sum(EST_MIN[N][0] for N, _ in CONFIGS)}〜{sum(EST_MIN[N][1] for N, _ in CONFIGS)} 分の見込み。--limit なら短い)", flush=True)
    _t0 = time.time()
    for _i, (N, s) in enumerate(CONFIGS):
        tg = tag_of(N, s, a.limit); jp = _root / f"models/21_16_run_{tg}.json"
        if jp.exists():
            old = json.load(open(jp))
            if old.get("script_sha256") == _me and old.get("cache_sha256") == _cs:
                print(f"[21_16] {tg}: 同じ版・同じキャッシュの結果があるので飛ばす"); continue
            if not a.force: raise SystemExit(f"[21_16] STOP: {tg} の結果は別の版かキャッシュで作られている(回すなら --force。本番の網の結果は _rerun の名前になり判定には使わない。--limit の結果は上書き)")
        print(f"[21_16] ===== {_i + 1}/10 {tg} を実行(見込み {EST_MIN[N][0]}〜{EST_MIN[N][1]} 分、ここまで {(time.time() - _t0) / 60:.0f} 分) =====", flush=True)
        cmd = [sys.executable, str(Path(__file__).resolve()), "--cache", a.cache, "--n-keep", str(N), "--seed", str(s), "--train-json", a.train_json] \
              + (["--limit", str(a.limit)] if a.limit else [])
        r = subprocess.run(cmd)
        if r.returncode != 0: raise SystemExit(f"[21_16] STOP: {tg} が止まった(上の STOP の行を貼って相談)")
    print(f"[21_16] 全ての網が終わった({(time.time() - _t0) / 60:.0f} 分)。次に 21_16b_sparse_learned_summary.py --expect-sha <事前登録の 21_16a の SHA-256>")
    raise SystemExit(0)
if a.n_keep < 0 or 0 < a.n_keep < 3: raise SystemExit("[21_16] STOP: --n-keep は 0(間引かない)か 3 以上")
if (a.n_keep, a.seed) not in CONFIGS: print(f"[21_16] 注意: N = {a.n_keep}・seed {a.seed} は事前に決めた 10 の網に無い(21_16b は読まない)")
TAG = tag_of(a.n_keep, a.seed, a.limit)
BASE_TAG = tag_of(a.n_keep, a.seed, 0)

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
print(f"[21_16] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
      f"網 {TAG}(1. 入力〜6. 似ている度合い は 21_04 v1 の写し。間引きは 1b.)")

# ---------------------------------------------------------------- 1. 入力
CP = ROOT / a.cache
if not CP.exists(): raise SystemExit(f"[21_16] STOP: {a.cache} が無い(ノート 21_04_ct2016_colab.ipynb のセル 11 で作った tottori_parsed_realpick_ct2016_m15.pt を data/ct2016_processed/ に置く)")
EVS = torch.load(CP, map_location="cpu", weights_only=False)
need = ["origin_time", "src_loc", "mw", "waveforms", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
for e in EVS:
    miss = [k for k in need if k not in e]
    if miss: raise SystemExit(f"[21_16] STOP: キャッシュの地震に {miss} が無い(15_01c v3.3 の出力か確かめる)")
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
    if a.n_keep >= len(STK): raise SystemExit(f"[21_16] STOP: --n-keep {a.n_keep} が候補の局の数 {len(STK)} 以上")
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
if len(_sk3) != len(STK) or not _left <= KEEP: raise SystemExit(f"[21_16] STOP(G-station): 局の見分けか間引きがおかしい({len(_sk3)} 対 {len(STK)})")
print(f"[21_16] 間引き: N = {a.n_keep}(最遠点、最初の局 {START}、seed {a.seed})  局 {len(STK)} → {len(KEEP)}(候補は 15_01c の 50 局のうちキャッシュに出てくる局)  "
      f"最近接の間隔の中央値 {NN_ALL if NN_ALL is None else round(NN_ALL, 1)} → {NN_KEEP if NN_KEEP is None else round(NN_KEEP, 1)} km  "
      f"検測の行 {n_before} → {n_after}")
if len(KEEP) < 3: raise SystemExit("[21_16] STOP: 残した局が 3 未満")
for e in EVS:
    w_ = np.asarray(e["waveforms"])
    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_16] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_16] STOP: {e['origin_time']} の波形に NaN か無限大")
def to_ns(o):
    import pandas as pd
    try:
        t = pd.Timestamp(str(o).replace("Z", "+00:00"))
        t = t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t
        return int(t.value)
    except Exception:
        raise SystemExit(f"[21_16] STOP: origin_time {o!r} を時刻として読めない")
OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
order = np.argsort(OTNS, kind="stable"); EVS = [EVS[i] for i in order]; OTNS = OTNS[order]
NE = len(EVS)
SRC = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS])
MAG = np.array([float(e["mw"]) for e in EVS])
OT = [str(e["origin_time"]) for e in EVS]
if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
    raise SystemExit("[21_16] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[21_16] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
# G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
lo_ns = int(np.datetime64(UNTOUCHED_UTC[0], "ns").astype(np.int64)); hi_ns = int(np.datetime64(UNTOUCHED_UTC[1], "ns").astype(np.int64))
n_out = int(np.sum((OTNS < lo_ns) | (OTNS > hi_ns))); n_big = int(np.sum(MAG >= 6.0 - 1e-6))
FRESH = MAG < FRESH_MAX_MAG - 1e-6
CACHE_SHA = sha256(CP)
n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
print(f"[21_16] 入力: 鳥取県中部 2016 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
      f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
print(f"[21_16] G-untouched: 期間 2016-10-19〜2016-11-15(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
      + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
if n_out != 0 or n_big != 1: raise SystemExit("[21_16] STOP(G-untouched): 鳥取県中部 2016 のキャッシュに見えない(この行を貼って相談)")
im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
    raise SystemExit(f"[21_16] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj 6.6・2016-10-21 05:07:22.57 UTC)")
CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
pool_idx = np.where(OTNS <= CUT_NS)[0]; test_idx = np.where((OTNS > CUT_NS) & FRESH)[0]
if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
    raise SystemExit("[21_16] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
print(f"[21_16] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
print(f"[21_16] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
      f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")

# ---------------------------------------------------------------- 2. 座標・検測(17_02 と同じ)
TFIRST = np.full(NE, np.nan)          # PhaseNet で測った最も早い P(気象庁の発生時刻からの s)
skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
for ie, e in enumerate(EVS):
    n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    ok = np.isfinite(tp) & (pf == 0)
    if ok.any(): TFIRST[ie] = float(tp[ok].min())
    kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
    if len(set(kk)) != n: raise SystemExit(f"[21_16] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
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
print(f"[21_16] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
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
print(f"[21_16] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
      f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")

# ---------------------------------------------------------------- 4. 格子と探索(17_02 と同じ)
H = float(max(30.0, np.percentile(np.abs(np.r_[EX[CAL], EY[CAL]]), 99.5) + 30.0))
STEP = float(max(1.0, round(H / 30.0)))
ZMAX = float(max(30.0, np.percentile(SRC[CAL, 2], 99.5) * 1.3 + 10.0))
ZDEF = float(np.mean(SRC[CAL, 2]))
xc = np.arange(-H, H + 1e-6, STEP); zc = np.arange(0.0, ZMAX + 1e-6, STEP)
GX, GY, GZ = np.meshgrid(xc, xc, zc, indexing="ij"); COARSE = np.c_[GX.ravel(), GY.ravel(), GZ.ravel()]
XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
print(f"[21_16] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
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
print(f"[21_16] KDE の帯域(pool の一つ抜き): {KDE_H} km")
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
    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_16] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
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
    if ie is not None and ie in top: stop("[21_16] STOP: 自分自身が似た地震の上位に入っている")
    out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
               C3=locate_map(pk, top), C4=None, fb=False, top1=int(top[0]), top=top, ncorr=0)
    if with_c4:
        dP, dS = corr_from(top, pk)
        out["C4"] = locate_map(pk, top, dP, dS); out["ncorr"] = len(dP)
    return out


# ---------------------------------------------------------------- 7. 速い S_ij(21_05 と同じ。式は similarity と同じ)
from numpy.lib.stride_tricks import sliding_window_view
NLAG = 2 * LAG_N + 1
class Bank:
    """遅い層の準備: 局 key -> (地震の番号の配列, (n, 3, NKEEP) の因果フィルタ後の波形)。filt_cached と同じ値を積む"""
    def __init__(self, band, events):
        by = {}
        for j in events:
            F = filt_cached(j, band)
            for key in list(F):
                F[key] = np.ascontiguousarray(F[key]).copy()      # 切り出しの元(全長 2048 点)を離して記憶を減らす(値は同じ)
                by.setdefault(key, []).append((j, F[key]))
        self.idx = {k: np.array([j for j, _ in v], int) for k, v in by.items()}
        self.Y = {k: np.stack([y for _, y in v]) for k, v in by.items()}
        for k, v in by.items():                       # filt_cached の中身を同じ配列の行に置き換える(値は同じ、記憶は 1 つ分)
            for r, (j, _) in enumerate(v): FILT[(j, band)][k] = self.Y[k][r]
def similarity_fast(ie, tau, lib, band, bank):
    """similarity(raw=False)と同じ S_ij(lib の順)と n_i を、局ごとに過去の地震をまとめて計算する"""
    tw = target_windows(ie, tau, band)
    S = np.zeros(len(lib)); ni = len(tw)
    if ni == 0: return S, 0
    pos = np.full(NE, -1, int); pos[lib] = np.arange(len(lib))
    for key, x in tw:
        if key not in bank.idx: continue
        ev = bank.idx[key]; p = pos[ev]; m = p >= 0
        if not m.any(): continue
        nx = np.linalg.norm(x)
        if nx == 0: continue
        Lw = x.shape[1]
        seg = bank.Y[key][m][:, :, IP - PRE_N - LAG_N: IP - PRE_N + LAG_N + Lw]          # (m, 3, Lw + 2·LAG)
        win = sliding_window_view(seg, Lw, axis=2)                                         # (m, 3, NLAG, Lw)
        num = np.einsum("mclt,ct->ml", win, x)
        ny = np.sqrt(np.einsum("mclt,mclt->ml", win, win))
        with np.errstate(divide="ignore", invalid="ignore"):
            c = np.where(ny > 0, num / (nx * ny), -np.inf)
        S[p[m]] += np.maximum(c.max(axis=1), 0.0)
    return S / ni, ni


# >>> 21_06 FEATURES BEGIN(この印から END までは 21_06a と 21_06b で 1 字も違わない。SHA-256 を学習の JSON に書き、21_06b で照合する)
# 学習型(L3・L4)の考え方: C3・C4 は「波形の似ている度合い S の上位 10 地震」を物理の事前分布と通り道の補正に使う。学習型は、
# 「どの過去の地震が本当に近いか」を、S だけでなく、P の時刻の差の並び(二重差の考え方)などの物理の手がかりから学習した
# 回帰(勾配ブースティング)で見積もり、近いと見積もった上位 10 地震を C3・C4 と全く同じ物理の計算に渡す(AI は物理の部品)。
# 特徴量は、局の名前・絶対的な位置・地域に依らない量だけにする(別の系列へ持って行けるように)。
FEATS = ["S", "S_4_16", "S_minus_max", "S_rank_frac", "frac_common_win", "c_max", "c_median", "lag_std_s",
         "n_common_picks", "dd_rms_s", "dd_offset_km", "dd_fit_rms_s", "same_first", "log10_dt_h", "mj_cand", "n_i", "tau_s"]
HGB = dict(max_iter=300, learning_rate=0.05, max_leaf_nodes=31, min_samples_leaf=50, l2_regularization=1.0, early_stopping=False, random_state=0)
LABEL_EPS_KM = 0.5           # 学習の目的変数: log(震央の間の距離 km + 0.5)
OFF_CLIP_KM = 30.0           # 二重差から見積もった相対的なずれの上限(局の並びが悪い時の発散を抑える)
COND_MIN = 1e-4              # 水平の 2×2 の正規方程式の固有値の比(最小/最大)がこれ未満なら、局の並びが一直線に近いので値なし(nan)
BLOCK_CONSTS = dict(TOPK=TOPK, MIN_POS=MIN_POS, BAND=list(BAND), BAND_SENS=list(BAND_SENS), PRE_S=PRE_S, MIN_WIN_S=MIN_WIN_S, MAX_WIN_S=MAX_WIN_S,
                    MAX_LAG_S=MAX_LAG_S, MIN_CORR=MIN_CORR, BUFFER_H=BUFFER_H, IP=IP, FS=FS, S_WEIGHT=S_WEIGHT, EPS_T=EPS_T)   # 学習と試験で同じか照合する
def tp_table():
    """局 key -> (NE,) の P の時刻(測った P だけ、無いところは nan)。全ての地震の検測から 1 回作る(遅い層)"""
    T = {}
    for j in range(NE):
        if not HASP[j]: continue
        e = EVS[j]; n = int(e["n_real_stations"]); loc = np.asarray(e["sta_locs"], float)[:n]
        tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
        for k in range(n):
            if pf[k] == 0 and np.isfinite(tp[k]): T.setdefault(skey(loc[k]), np.full(NE, np.nan))[j] = tp[k]
    return T
def sim_detail(ie, tau, lib, band, bank):
    """similarity_fast と同じ S(lib の順)と n_i に加えて、局ごとの最大のコサイン類似度 C (len(lib), n_i) とその時のずれ LG (s)"""
    tw = target_windows(ie, tau, band); ni = len(tw)
    S = np.zeros(len(lib)); C = np.full((len(lib), ni), np.nan); LG = np.full((len(lib), ni), np.nan)
    if ni == 0: return S, 0, C, LG
    pos = np.full(NE, -1, int); pos[lib] = np.arange(len(lib))
    for s, (key, x) in enumerate(tw):
        if key not in bank.idx: continue
        ev = bank.idx[key]; p = pos[ev]; m = p >= 0
        if not m.any(): continue
        nx = np.linalg.norm(x)
        if nx == 0: continue
        Lw = x.shape[1]
        seg = bank.Y[key][m][:, :, IP - PRE_N - LAG_N: IP - PRE_N + LAG_N + Lw]
        win = sliding_window_view(seg, Lw, axis=2)
        num = np.einsum("mclt,ct->ml", win, x); ny = np.sqrt(np.einsum("mclt,mclt->ml", win, win))
        with np.errstate(divide="ignore", invalid="ignore"):
            c = np.where(ny > 0, num / (nx * ny), -np.inf)
        cm = c.max(axis=1); S[p[m]] += np.maximum(cm, 0.0)
        ok = np.isfinite(cm); rows = p[m][ok]
        C[rows, s] = cm[ok]; LG[rows, s] = (c.argmax(axis=1)[ok] - LAG_N) / FS
    return S / ni, ni, C, LG
def pair_features(ie, tau, lib, bank, bank2, TPT):
    """目標の地震 ie・時点 tau で、過去の地震の一覧 lib のうち S > 0 の候補ごとの特徴量。
    返り値: (候補の地震の番号 J, 特徴量 (len(J), len(FEATS)), lib の順の S, n_i)。S は similarity_fast と同じ値"""
    S, ni, C, LG = sim_detail(ie, tau, lib, BAND, bank)
    cand = np.where(S > 0)[0]; J = lib[cand]
    if len(J) == 0: return J, np.zeros((0, len(FEATS))), S, ni
    S2, _ = similarity_fast(ie, tau, lib, BAND_SENS, bank2)
    pk = picks_of(ie, tau)
    Cc, Lc = C[cand], LG[cand]
    rank = np.empty(len(lib)); rank[np.argsort(-S, kind="stable")] = np.arange(len(lib))
    nwin = np.isfinite(Cc).sum(1)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        cmax = np.nanmax(np.where(np.isfinite(Cc), Cc, -np.inf), axis=1); cmed = np.nanmedian(Cc, axis=1)
        lagsd = np.where(nwin >= 2, np.nanstd(Lc, axis=1), np.nan)
    # 二重差の考え方: 共通の局での P の時刻の並び(目標 − 候補、それぞれの平均を引く)r_k は、震源の相対的なずれ Δ で
    # r_k ≈ c − (u_k・Δ)/v になる(u_k は候補の震源から局への単位ベクトルの水平成分、v は候補の深さの速度)。最小二乗で水平の Δ を見積もる
    # (直線の波線の近似で、深さの違いは解かない。共通の局 4 つ未満か、並びが一直線に近い時は値なし)
    keys = [p[0] for p in pk]
    ti = np.array([p[4] for p in pk], float); sx = np.array([p[1] for p in pk], float)
    sy = np.array([p[2] for p in pk], float); sz = np.array([p[3] for p in pk], float)
    TJ = (np.stack([TPT[k][J] if k in TPT else np.full(len(J), np.nan) for k in keys], axis=1) if keys else np.zeros((len(J), 0)))
    M = np.isfinite(TJ); nc = M.sum(1)
    with np.errstate(all="ignore"):
        mi = np.where(M, ti[None, :], 0.0).sum(1) / nc; mj = np.where(M, TJ, 0.0).sum(1) / nc
        r = np.where(M, (ti[None, :] - mi[:, None]) - (TJ - mj[:, None]), 0.0)
        rms = np.where(nc >= 2, np.sqrt((r ** 2).sum(1) / nc), np.nan)
        dx = sx[None, :] - EX[J][:, None]; dy = sy[None, :] - EY[J][:, None]; dz = sz[None, :] - SRC[J, 2][:, None]
        R = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2); v = (V0 + KG * SRC[J, 2])[:, None]
        A = np.stack([np.ones_like(dx), -dx / (R * v), -dy / (R * v)], axis=2)
        A = np.where(M[:, :, None] & np.isfinite(A), A, 0.0)
        G = np.einsum("mka,mkb->mab", A, A) + 1e-9 * np.eye(3)[None]
        sol = np.linalg.solve(G, np.einsum("mka,mk->ma", A, r)[:, :, None])[:, :, 0]
        fit = np.where(M, r - np.einsum("mka,ma->mk", A, sol), 0.0)
        ev2 = np.linalg.eigvalsh(G[:, 1:, 1:]); good = (nc >= 4) & (ev2[:, 0] >= COND_MIN * np.maximum(ev2[:, 1], 1e-300))
        off = np.where(good, np.minimum(np.hypot(sol[:, 1], sol[:, 2]), OFF_CLIP_KM), np.nan)
        frms = np.where(good, np.sqrt((fit ** 2).sum(1) / np.maximum(nc - 3, 1)), np.nan)
    f1 = FIRST[ie][0]
    F = np.column_stack([S[cand], S2[cand], S[cand] - S.max(), rank[cand] / max(len(lib) - 1, 1), nwin / ni, cmax, cmed, lagsd,
                         nc, rms, off, frms, np.array([FIRST[j][0] == f1 for j in J], float),
                         np.log10(np.maximum((OTNS[ie] - OTNS[J]) / 3.6e12, 1e-3)), MAG[J], np.full(len(J), ni, float),
                         np.full(len(J), tau, float)])
    return J, F.astype(float), S, ni
def learned_top(model, J, F, k=TOPK):
    """学習した回帰で近いと見積もった上位 k 地震。S > 0 の候補が MIN_POS 未満なら None(C3 と同じく M6r に戻る)"""
    if len(J) < MIN_POS: return None
    pr = model.predict(F)
    return J[np.argsort(pr, kind="stable")[:min(k, len(J))]]
def l_from(top, pk, m6r):
    """L3(上位の地震の事前分布 × 物理)と L4(L3 + 上位の地震の通り道の補正)。計算は C3・C4 と同じ関数"""
    if top is None: return m6r, m6r, 0
    dP, dS = corr_from(top, pk)
    return locate_map(pk, top), locate_map(pk, top, dP, dS), len(dP)
# <<< 21_06 FEATURES END

# ============================================================================= 21_16a ここから(凍結したモデル・照合・評価)
VERSION = "v2"                                       # 21_16a の版(v2: 記録の書き込みを壊れにくく・凍結した SHA を直接照合・scipy の版を記録)(上の 1.〜6. は 21_09a v1、7. と FEATURES は 21_06b v1 の写し)
EXPECT_09A_SHA = "f74c90822cd91078eafeae411f3c0560e025bdca44a67f7e3e8abcd5bda59aab"   # 事前登録した 21_09a v1(21_09_preregistration.md)
# 21_06 の事前登録の記録 6 節(凍結 B)に書いた値。モデル・学習の行・学習の記録・21_06b のスクリプトがこれと違えば止める(G-frozen)
EXPECT_MODEL_SHA = "0d0f75a48a50f866d3963c6560497abe1c007ecac628391284ca6fe248b712e1"       # models/21_06_ranker.pkl
EXPECT_ROWS_SHA = "ca23242288ad6fe4fdf5853960a6fd41b78328a59ec22bc5d484bf5334e632e9"        # data/21_06a_train_rows.npz
EXPECT_TRAINJSON_SHA = "4f27ad1e0596d244b62b064918cde92cde6f93a13829a96bb6ac04079e13f87e"   # models/21_06a_train.json
EXPECT_06B_SHA = "442c411945f288cfff7f14490ee9826ffcfe055e5a79cc2af0c39fe93cb5bfea"         # 21_06b_ct2016_learned_test.py v1
import scipy, os, tempfile
def write_json_atomic(path, obj):
    """一時ファイルに書いてから置き換える(途中で止まっても、前の中身か新しい中身のどちらかが残る)"""
    path = Path(path); fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix="." + path.name + ".", suffix=".tmp")
    with os.fdopen(fd, "w") as f_: json.dump(obj, f_, indent=1); f_.flush(); os.fsync(f_.fileno())
    os.replace(tmp, path)
ALPHA_L = 0.005                                      # 主(網ごと、L4 @ τ = 2 s 対 BEST)と、記述の L4 対 C4・L3 @ 0.5 s 対 BEST の基準
PRIMARY_TAU = "2"
TAIL_KM = 10.0                                       # 記述: 誤差のすその目安(21_14・21_15 と同じ 10 km)
TOL_KM = 6e-5                                        # G-same の許し(21_09a・21_06b と同じ)
LIMITS_09 = ["the sparse networks are subsets of Hi-net stations chosen by a position-only farthest-point rule (N stations, random first "
             "station); real sparse networks (ocean-bottom, other station types, other regions) differ",
             "the cache was built on the dense network: events needed >= 4 picks there (some would be missed by a sparse network), and the "
             "Wadati S-P quality check used all of an event's stations, so removed stations influenced which S picks of kept stations survive",
             "the cache keeps at most 24 stations per event (measured-P stations ordered by earliest P, then fallback picks); stations beyond "
             "the 24th in the full network are unavailable in the thinned network; candidate stations are those appearing in the cache",
             "each network is evaluated on the test events with a P pick at its kept stations, so trends across networks compare different "
             "event sets and are descriptive",
             "truth, past-event locations and C4/L4 station terms are JMA hypocentres determined with the dense network; in a region that only "
             "has a sparse network the past-event locations would be worse, so C3/C4/L3/L4 here are optimistic",
             "same limits as 21_04 (one sequence, offline PhaseNet picks, no picking or telemetry latency, small events, the 2016 test "
             "carries a documented deviation: amendment 03)"]
LIMITS_16 = ["the learned ranker (21_06a) was trained on the dense West Tottori 2026 network only and frozen; it is applied unchanged "
             "(no retraining) to thinned networks, where its physics features shift: n_common_picks shrinks and dd_offset_km/dd_fit_rms_s "
             "need >= 4 common stations (nan otherwise); this distribution shift is the main risk tested here",
             "the 2016 test carries a documented deviation (amendment 03: the preregistered station-timing check G-clock2 (c) failed) and a "
             "known error tail attributed to early mis-picks at far stations (21_15); the primary test does not filter the tail",
             "the 2016 test events were already opened by 21_04, 21_06b and 21_09; new in 21_16 are only L3/L4 on the thinned networks",
             "the double-difference offset is a horizontal straight-ray approximation (depth not solved)",
             "log10_dt_h uses the target's JMA origin time (not known exactly at tau; the error is a few seconds against >= 1 h)",
             "all errors are rounded to 4 decimals (as in the 21_06b and 21_09 CSVs) before comparison so that ties stay ties; 21_09a judged C4 "
             "on unrounded errors, so C4-vs-BEST p values here may differ from 21_09 in the last digits (descriptive here)",
             "21_16: per network, L4 at tau = 2 s vs BEST (alpha 0.005) is the classified test; everything else is descriptive"]
LIMITS_ALL = [l for l in LIMITS if not l.startswith("21_09:")] + LIMITS_09 + LIMITS_16
import sys, pickle
FB = open(Path(__file__), encoding="utf-8").read()
SUF = "_limit%d" % a.limit if a.limit else ""
OPEN = ROOT / "models/21_16_opened.json"
OPENED = False
def log_open(status):
    if OPEN.exists():
        try: rec = json.load(open(OPEN))
        except Exception as e:   # 読めない時に空で上書きすると 1 回だけの記録が消えるので、何も書かずに止める
            raise SystemExit(f"[21_16] STOP: 1 回だけの記録 {OPEN.name} が読めない({e})。消さずにそのまま残し、この行を貼って相談")
        if not isinstance(rec, list): raise SystemExit(f"[21_16] STOP: 1 回だけの記録 {OPEN.name} の形がおかしい(消さずに相談)")
    else: rec = []
    rec.append(dict(utc=utcnow(), tag=TAG, suffix=SUF, status=status, version=VERSION, script_sha256=SELF_SHA, cache_sha256=CACHE_SHA))
    write_json_atomic(OPEN, rec)
def stop(msg):
    if OPENED: log_open("stopped: " + msg[:200])
    raise SystemExit(msg)

# ---------------------------------------------------------------- 8a. G-core: 写した部分が元のスクリプトと 1 字も違わない
def _block(text, start, end, name):
    """start の最初の出現から end の最初の出現の手前まで(本物の区切りは、それを文字列として使うコードより前にある)"""
    if start not in text or end not in text: stop(f"[21_16] STOP(G-core): {name} に区切りの行が無い")
    i, j = text.index(start), text.index(end)
    if j <= i: stop(f"[21_16] STOP(G-core): {name} の区切りの順がおかしい")
    return text[i:j]
CORE_START = "# ---------------------------------------------------------------- 事前に固定した値(変えたら版を上げる)"
F09 = ROOT / "src/21_09a_ct2016_sparse_network.py"
if not F09.exists(): stop("[21_16] STOP(G-core): src/21_09a_ct2016_sparse_network.py が無い(21_09 の本番で使ったもの)")
if sha256(F09) != EXPECT_09A_SHA: stop(f"[21_16] STOP(G-core): src/21_09a の SHA-256 {sha256(F09)[:12]}… が事前登録の 21_09a v1(f74c9082…)と違う")
T09 = open(F09, encoding="utf-8").read()
core09 = _block(T09, CORE_START, "# ============================================================================= 21_09a ここから(評価)", "21_09a").replace("[21_09]", "[21_16]")
core16 = _block(FB, CORE_START, "\n\n# ---------------------------------------------------------------- 7. 速い S_ij", "21_16a")
if core09.rstrip("\n") != core16.rstrip("\n"): stop("[21_16] STOP(G-core): 1.〜6. が 21_09a v1 の写しと違う")
F06 = ROOT / "src/21_06b_ct2016_learned_test.py"
J06 = ROOT / "models/21_06b_judgment.json"
if not F06.exists() or not J06.exists(): stop("[21_16] STOP(G-core): src/21_06b_ct2016_learned_test.py か models/21_06b_judgment.json が無い(21_06b の本番の後で回す)")
JB = json.load(open(J06))
if sha256(F06) != JB.get("script_sha256"): stop("[21_16] STOP(G-core): src/21_06b の SHA-256 が 21_06b の本番の記録(models/21_06b_judgment.json)と違う")
T06 = open(F06, encoding="utf-8").read()
S7 = "# ---------------------------------------------------------------- 7. 速い S_ij"
ENDF = "# <<< 21_06 FEATURES END"
if _block(T06, S7, ENDF, "21_06b") != _block(FB, S7, ENDF, "21_16a"): stop("[21_16] STOP(G-core): 7. と FEATURES の部分が 21_06b v1 の写しと違う")
G_CORE = dict(status="PASS", sha_21_09a=EXPECT_09A_SHA, sha_21_06b=JB["script_sha256"])
print(f"[21_16] G-core: 1.〜6. = 21_09a v1(f74c9082…)の写し、7. と FEATURES = 21_06b({JB['script_sha256'][:12]}…)の写し  PASS")

# ---------------------------------------------------------------- 8b. 凍結したモデルの読み込み(21_06b と同じ照合)
try:
    import sklearn
except ImportError:
    stop("[21_16] STOP: scikit-learn が無い(21_06a と同じ環境で回す)")
TJP = ROOT / a.train_json
if not TJP.exists(): stop(f"[21_16] STOP: 学習の記録 {a.train_json} が無い")
TJ = json.load(open(TJP))
if a.train_json != "models/21_06a_train.json" or TJ.get("mode") != "train" or TJ.get("suffix", "") != "":
    stop("[21_16] STOP(G-model): 学習の記録は 21_06a の最初の本番(models/21_06a_train.json、mode train)だけを受け付ける")
FEAT_SHA = hashlib.sha256(FB[FB.index("# >>> 21_06 FEATURES BEGIN"):FB.index("# <<< 21_06 FEATURES END")].encode()).hexdigest()
if TJ["feature_block_sha256"] != FEAT_SHA: stop("[21_16] STOP(G-feat): 特徴量の部分が 21_06a と 1 字でも違う")
MP = ROOT / TJ["model_path"]
if not MP.exists() or sha256(MP) != TJ["model_sha256"]: stop(f"[21_16] STOP(G-model): モデル {TJ['model_path']} が無いか、SHA-256 が学習の記録と違う")
if TJ["sklearn"] != sklearn.__version__: stop(f"[21_16] STOP(G-model): scikit-learn の版が学習時({TJ['sklearn']})と違う({sklearn.__version__})")
if TJ["numpy"] != np.__version__: stop(f"[21_16] STOP(G-model): numpy の版が学習時({TJ['numpy']})と違う({np.__version__})")
if TJ["feats"] != FEATS or TJ["hgb"] != HGB or TJ.get("block_consts") != json.loads(json.dumps(BLOCK_CONSTS)) or TJ.get("cond_min") != COND_MIN:
    stop("[21_16] STOP(G-model): 特徴量の名前・設定・特徴量が使う定数が学習の記録と違う")
RP = ROOT / TJ["train_rows_path"]
if not RP.exists() or sha256(RP) != TJ["train_rows_sha256"]: stop(f"[21_16] STOP(G-model): 学習の行 {TJ['train_rows_path']} が無いか SHA-256 が違う")
if (TJ["model_sha256"], TJ["train_rows_sha256"], sha256(TJP)) != (EXPECT_MODEL_SHA, EXPECT_ROWS_SHA, EXPECT_TRAINJSON_SHA):
    stop("[21_16] STOP(G-frozen): モデル・学習の行・学習の記録の SHA-256 が 21_06 の事前登録の記録 6 節(凍結 B)の値と違う")
if JB.get("script_sha256") != EXPECT_06B_SHA: stop("[21_16] STOP(G-frozen): 21_06b の本番のスクリプトの SHA-256 が事前登録の 21_06b v1(442c4119…)と違う")
with open(MP, "rb") as f: MODEL = pickle.load(f)
if list(getattr(MODEL, "feature_names_in_", [])) not in ([], FEATS) or int(getattr(MODEL, "n_features_in_", len(FEATS))) != len(FEATS):
    stop("[21_16] STOP(G-model): モデルの特徴量の数が FEATS と合わない")
TJ_SHA = sha256(TJP)
print(f"[21_16] 凍結したモデル: {TJ['model_path']} SHA-256 {TJ['model_sha256']}(2026 の {TJ['n_train_events']} 地震で学習)\n"
      f"[21_16] 学習の記録 SHA-256 {TJ_SHA}  特徴量の部分 {FEAT_SHA}  scipy {scipy.__version__}  G-feat PASS  G-model PASS  G-frozen PASS")
# G-ref06b: 21_06b の本番の記録が、同じモデル・特徴量の部分・キャッシュで作られた
if JB.get("mode") != "test" or JB.get("suffix", "") != "": stop("[21_16] STOP(G-ref06b): models/21_06b_judgment.json が 21_06b の最初の本番の結果でない")
if JB.get("model_sha256") != TJ["model_sha256"] or JB.get("feature_block_sha256") != FEAT_SHA or JB.get("cache_sha256") != CACHE_SHA:
    stop("[21_16] STOP(G-ref06b): 21_06b の本番とモデル・特徴量の部分・キャッシュのどれかの SHA-256 が違う")
print("[21_16] G-ref06b: 21_06b の最初の本番と同じモデル・特徴量の部分・キャッシュ  PASS")
# G-ref09: 比べる 21_09a の結果(同じ網・同じ間引き・同じキャッシュ・事前登録の 21_09a)
R09J = ROOT / f"models/21_09_run_{BASE_TAG}.json"; R09C = ROOT / f"data/21_09_per_event_{BASE_TAG}.csv"
if a.limit and not (R09J.exists() and R09C.exists()):
    R09J = ROOT / f"models/21_09_run_{TAG}.json"; R09C = ROOT / f"data/21_09_per_event_{TAG}.csv"
    print(f"[21_16] 注意(--limit): 21_09a の本番の結果が無いので、同じ --limit の結果 {R09C.name} と比べる")
if not R09J.exists() or not R09C.exists(): stop(f"[21_16] STOP(G-ref09): {R09J.relative_to(ROOT)} か {R09C.relative_to(ROOT)} が無い(先に 21_09a)")
J09 = json.load(open(R09J))
_kept = [list(map(float, ALLST[k])) for k in sorted(KEEP)]
bad09 = []
if J09.get("script_sha256") != EXPECT_09A_SHA: bad09.append("21_09a の SHA-256 が事前登録の v1 と違う")
if J09.get("cache_sha256") != CACHE_SHA: bad09.append("キャッシュの SHA-256 が違う")
if J09.get("network", {}).get("n_keep") != a.n_keep or J09["network"].get("seed") != a.seed: bad09.append("N か seed が違う")
if not a.limit and J09.get("limit") != 0: bad09.append("21_09a の本番(limit 0)の結果でない")
if J09.get("network", {}).get("first_station_index") != START: bad09.append(f"最初の局が違う({J09['network'].get('first_station_index')} 対 {START})")
if not (len(J09.get("network", {}).get("kept_stations_latlon", [])) == len(_kept)
        and np.allclose(np.array(J09["network"]["kept_stations_latlon"], float), np.array(_kept, float), atol=0, rtol=0)):
    bad09.append("残した局の一覧が違う")
if J09.get("gates", {}).get("causal", {}).get("status", "").startswith("FAIL"): bad09.append("21_09a の G-causal が FAIL")
if bad09: stop("[21_16] STOP(G-ref09): " + " / ".join(bad09))
R09_SHA = sha256(R09C)
print(f"[21_16] G-ref09: {R09J.name}(21_09a v1・同じキャッシュ・同じ {len(KEEP)} 局・最初の局 {START})  PASS")
R6C = ROOT / "data/21_06b_per_event.csv"
if a.n_keep == 0 and not R6C.exists(): stop("[21_16] STOP(G-ref06b): data/21_06b_per_event.csv が無い(21_06b の本番の出力)")

# ---------------------------------------------------------------- 9. 1 回だけの記録(入力の確認が全て通った後で、試験を開く)
if not a.limit and (ROOT / f"models/21_16_run_{TAG}.json").exists():
    SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
    print(f"[21_16] 注意: 網 {TAG} は既に終わっている。計算はするが、結果は {TAG}{SUF} の名前に書く(前の結果は上書きしない。判定に使うのは最初のもの)")
_prev = [r for r in (json.load(open(OPEN)) if OPEN.exists() else []) if r.get("tag") == TAG]
if _prev: print(f"[21_16] 開いた記録: 網 {TAG} の前の記録 {len(_prev)} 件(最後: {_prev[-1]['status'][:80]})")
log_open("opened" + (f" (dev, --limit {a.limit})" if a.limit else "")); OPENED = True
log_open(f"inputs: train_json {TJ_SHA} model {TJ['model_sha256']} ref09_csv {R09_SHA} ref09_json {sha256(R09J)}")
def _hook(t, v, tb):
    log_open(f"stopped: {t.__name__}: {str(v)[:160]}"); sys.__excepthook__(t, v, tb)
sys.excepthook = _hook

# ---------------------------------------------------------------- 10. 遅い層の準備(21_06b と同じ。間引いた後の地震で作る)
EVAL = test_idx[HASP[test_idx]]
if a.limit: EVAL = EVAL[:a.limit]
N_LOST = int(len(test_idx) - int(HASP[test_idx].sum()))
NT = len(EVAL); TESTABLE = NT >= MIN_TEST
print(f"[21_16] 評価: 試験の地震 {len(test_idx)} のうち、残した局で P を測れた地震 {NT}" + (f"(--limit {a.limit}: 動作確認、判定に使わない)" if a.limit else ""))
if NT == 0: stop("[21_16] STOP: 評価できる地震が 0")
if not TESTABLE: print(f"[21_16] 注意: 評価できる地震 {NT} < {MIN_TEST}。この網は「試せない」(21_09 と同じ規則)。記述は出す")
t0 = time.time()
ALLP = np.where(HASP)[0]
bank = Bank(BAND, ALLP); bank2 = Bank(BAND_SENS, ALLP)
TPT = tp_table()
print(f"[21_16] 遅い層の準備({len(ALLP)} 地震、2 つの帯域と P の時刻の表): {time.time() - t0:.1f} s", flush=True)
# 記述: 学習の行(2026)の τ ごとの特徴量の様子(分布のずれの目安)
R26 = np.load(RP); X26 = R26["X"]
iNC, iOFF, iTAU, iNI = FEATS.index("n_common_picks"), FEATS.index("dd_offset_km"), FEATS.index("tau_s"), FEATS.index("n_i")
TRAIN_FEAT = {}
for t in TAUS:
    m = np.isclose(X26[:, iTAU], t)
    TRAIN_FEAT[f"{t:g}"] = dict(n_rows=int(m.sum()), n_common_picks_median=(float(np.median(X26[m, iNC])) if m.any() else None),
                                dd_offset_nan_frac=(float(np.mean(~np.isfinite(X26[m, iOFF]))) if m.any() else None),
                                n_i_median=(float(np.median(X26[m, iNI])) if m.any() else None))
del R26, X26

# ---------------------------------------------------------------- 11. 評価(21_09a の eval_event に、21_06b の L3・L4 を足したもの)
BASE = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]
METH = BASE + ["C3", "C4", "L3", "L4"]
TL = [f"{t:g}" for t in TAUS] + ["inf"]
def dist_km(ie, J): return np.array([km_between(SRC[ie, 0], SRC[ie, 1], SRC[j, 0], SRC[j, 1]) for j in J])
def eval_event(ie, only_tau=None):
    """21_09a の eval_event と同じ計算(S は 21_06b と同じ速い S)+ L3・L4(21_06b と同じ)"""
    lib = library(ie); p0 = FIRST[ie]
    m3 = prior_members(lib, p0[0], (p0[1], p0[2])); m3p = prior_members(POOL_OK, p0[0], (p0[1], p0[2]))
    R = {m: np.full((len(TL), 2), np.nan) for m in METH}
    nT = len(TAUS)
    X = dict(nst=np.zeros(len(TL), int), ni=np.zeros(nT, int), smax=np.full(nT, np.nan), fb=np.zeros(nT, bool), ncorr=np.zeros(nT, int),
             lfb=np.zeros(nT, bool), lcorr=np.zeros(nT, int), ncand=np.zeros(nT, int), nc_med=np.full(nT, np.nan), off_nan=np.full(nT, np.nan),
             topd_c=np.full(nT, np.nan), topd_l=np.full(nT, np.nan))
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
        J, F, S, ni = pair_features(ie, tau, lib, bank, bank2, TPT)
        o = c_from(S, lib, pk, m3, m6r, TOPK, ie=ie)
        topL = learned_top(MODEL, J, F)
        if topL is not None and ie in topL: stop("[21_16] STOP: 自分自身が学習の上位に入っている")
        L3, L4, nlc = l_from(topL, pk, m6r)
        R["C3"][jt], R["C4"][jt], R["L3"][jt], R["L4"][jt] = o["C3"], o["C4"], L3, L4
        X["ni"][jt], X["smax"][jt], X["fb"][jt], X["ncorr"][jt] = ni, (float(S.max()) if ni > 0 and len(S) else np.nan), o["fb"], o["ncorr"]
        X["lfb"][jt], X["lcorr"][jt], X["ncand"][jt] = topL is None, nlc, len(J)
        if len(J):
            X["nc_med"][jt] = float(np.median(F[:, iNC])); X["off_nan"][jt] = float(np.mean(~np.isfinite(F[:, iOFF])))
        if o["top"] is not None: X["topd_c"][jt] = float(np.median(dist_km(ie, o["top"])))
        if topL is not None: X["topd_l"][jt] = float(np.median(dist_km(ie, topL)))
    return R, X
P = {m: np.full((NT, len(TL), 2), np.nan) for m in METH}
XK = ["nst", "ni", "smax", "fb", "ncorr", "lfb", "lcorr", "ncand", "nc_med", "off_nan", "topd_c", "topd_l"]
XA = {k: None for k in XK}
T_EV = time.time()
for ii, ie in enumerate(EVAL):
    try:
        R, X = eval_event(ie)
    except SystemExit:
        raise
    except BaseException as ex:
        stop(f"[21_16] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
    for m in METH: P[m][ii] = R[m]
    for k in XK:
        if XA[k] is None: XA[k] = np.zeros((NT,) + X[k].shape, X[k].dtype)
        XA[k][ii] = X[k]
    if (ii + 1) % 10 == 0 or ii + 1 == NT:
        el = time.time() - T_EV
        print(f"  … {ii+1}/{NT}  ({time.time()-T0:.0f} s、評価の残りの見込み約 {el / (ii + 1) * (NT - ii - 1) / 60:.1f} 分"
              f"、この後 G-causal に約 {el / (ii + 1) * min(N_GATE, NT) * 1.1 / 60:.1f} 分)", flush=True)
NST, NI, SMAX, C3FB, LFB = XA["nst"], XA["ni"], XA["smax"], XA["fb"], XA["lfb"]

# ---------------------------------------------------------------- 12. G-causal(21_09a と同じ手順。L3・L4 と学習の特徴量の陽性対照を足した)
gate_ev = [ii for ii in range(NT) if NI[ii, TAUS.index(1.0)] > 0][:N_GATE]
GC = dict(status="not checked (fewer than 3 events with a similarity at tau = 1 s)", max_diff=None, positive_control=None,
          positive_control_features=None, n_checks=0)
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
    pos_ctrl, pos_ctrl_f, shared = None, None, []
    for _ii in gate_ev:                                  # 過去の地震と局を共有する最初のゲートの地震で陽性対照
        ie = EVAL[_ii]; orig = EVS[ie]; lib0 = library(ie)
        shared = [p for p in picks_of(ie, 1.0) if n_avail(1.0, p[4]) >= MINW_N and any(p[0] in filt_cached(j, BAND) for j in lib0)]
        if shared: break
    if shared:
        S0, _ = similarity(ie, 1.0, lib0, BAND, raw=True)
        J0, F0, _, _ = pair_features(ie, 1.0, lib0, bank, bank2, TPT)
        pc = shared[0]; e2 = dict(orig); W = np.array(np.asarray(orig["waveforms"], float))
        W[pc[8], :, IP + n_avail(1.0, pc[4]) - 1] += 50.0 * np.abs(W[pc[8], :, IP:IP + 100]).max()
        e2["waveforms"] = W; EVS[ie] = e2; [FILT.pop((ie, b), None) for b in SOS]
        S1, _ = similarity(ie, 1.0, lib0, BAND, raw=True)
        J1, F1, _, _ = pair_features(ie, 1.0, lib0, bank, bank2, TPT)
        EVS[ie] = orig; [FILT.pop((ie, b), None) for b in SOS]
        pos_ctrl = float(np.max(np.abs(S1 - S0))) if len(S0) else 0.0
        if len(J0) != len(J1) or not np.array_equal(J0, J1): pos_ctrl_f = float("inf")
        elif len(J0) == 0: pos_ctrl_f = 0.0
        else:
            dF = np.abs(np.nan_to_num(F1, nan=-999.0) - np.nan_to_num(F0, nan=-999.0)); pos_ctrl_f = float(dF.max())
    ok = gc_max == 0.0 and ((pos_ctrl > 0 and pos_ctrl_f > 0) if pos_ctrl is not None else a.n_keep > 0)
    GC = dict(status=("PASS" if ok else "FAIL") + ("" if pos_ctrl is not None else " (positive control not available: no shared station)"),
              max_diff=gc_max, positive_control=pos_ctrl, positive_control_features=pos_ctrl_f, n_checks=gc_n)
    print(f"[21_16] G-causal({len(gate_ev)} 地震 × 4 時点、L3・L4 を含む全ての方法): 最大の差 {gc_max:.3g}  陽性対照 S {pos_ctrl}・"
          f"特徴量 {pos_ctrl_f}  {GC['status']}")
    if not ok: stop("[21_16] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")
else:
    print(f"[21_16] G-causal: {GC['status']}(計算のコードは間引かない網と同じ)")
    if a.n_keep == 0: stop("[21_16] STOP(G-causal): 間引かない網で確かめられない(この行を貼って相談)")

# ---------------------------------------------------------------- 13. 誤差(小数 4 桁に丸める)・G-same・G-same-L
def herr(Pm):
    out = np.full(Pm.shape[:2], np.nan)
    for i, ie in enumerate(EVAL):
        for j in range(Pm.shape[1]):
            if np.isfinite(Pm[i, j, 0]):
                la, lo = to_ll(Pm[i, j, 0], Pm[i, j, 1]); out[i, j] = km_between(la, lo, SRC[ie, 0], SRC[ie, 1])
    return out
E = {m: np.vectorize(lambda v: float(f"{v:.4f}"))(herr(P[m])) for m in METH}     # 21_06b と同じ丸め(nan は nan のまま)
with open(R09C) as f: R9 = {r["origin_time"]: r for r in csv.DictReader(f)}
bad, worst, nchk = [], 0.0, 0
if not a.limit and set(R9) != {OT[ie] for ie in EVAL}: bad.append(f"評価する地震の集合が違う(21_09 {len(R9)}・21_16 {NT})")
for i, ie in enumerate(EVAL):
    r = R9.get(OT[ie])
    if r is None: bad.append(f"{OT[ie][:19]} が 21_09 の CSV に無い"); continue
    for j, t in enumerate(TL):
        if int(r[f"n_sta_t{t}"]) != int(NST[i, j]): bad.append(f"{OT[ie][:19]} n_sta τ={t}")
        if t != "inf" and int(r[f"c3_fallback_t{t}"]) != int(C3FB[i, j]): bad.append(f"{OT[ie][:19]} c3_fallback τ={t}")
        for m in (BASE if t == "inf" else BASE + ["C3", "C4"]):
            v = r.get(f"{m}_err_t{t}", ""); x = E[m][i, j]
            if (v in ("", None)) != (not np.isfinite(x)): bad.append(f"{OT[ie][:19]} {m} τ={t} 空の有無"); continue
            if v in ("", None): continue
            dlt = abs(x - float(v)); worst = max(worst, dlt); nchk += 1
            if dlt > TOL_KM: bad.append(f"{OT[ie][:19]} {m} τ={t} {x:.4f} 対 {float(v):.4f}")
GSAME = dict(reference=str(R09C.relative_to(ROOT)), reference_sha256=R09_SHA, n_values=nchk, max_abs_diff_km=worst, n_mismatch=len(bad),
             status=("PASS" if not bad else "FAIL"))
print(f"[21_16] G-same(21_09 の CSV と、{NT} 地震 × 9 方法・C3・C4 × 時点 = {nchk} 値・局の数・M6r に戻ったか・地震の集合): "
      f"最大の差 {worst:.2g} km  不一致 {len(bad)}  {GSAME['status']}")
if bad: stop("[21_16] STOP(G-same): 21_09a と値が違う。最初の 5 件: " + " / ".join(bad[:5]))
GSAME_L = None
if a.n_keep == 0:
    with open(R6C) as f: R6 = {r["origin_time"]: r for r in csv.DictReader(f)}
    badL, worstL, nL = [], 0.0, 0
    if not a.limit and set(R6) != {OT[ie] for ie in EVAL}: badL.append(f"評価する地震の集合が違う(21_06b {len(R6)}・21_16 {NT})")
    for i, ie in enumerate(EVAL):
        r = R6.get(OT[ie])
        if r is None: badL.append(f"{OT[ie][:19]} が 21_06b の CSV に無い"); continue
        for j, t in enumerate(TL[:-1]):
            if int(float(r[f"LFB_t{t}"])) != int(LFB[i, j]): badL.append(f"{OT[ie][:19]} LFB τ={t}")
            for m in ("C3", "C4", "L3", "L4"):
                v = r.get(f"{m}_t{t}", ""); x = E[m][i, j]
                if (v in ("", None)) != (not np.isfinite(x)): badL.append(f"{OT[ie][:19]} {m} τ={t} 空の有無"); continue
                if v in ("", None): continue
                dlt = abs(x - float(v)); worstL = max(worstL, dlt); nL += 1
                if dlt > TOL_KM: badL.append(f"{OT[ie][:19]} {m} τ={t} {x:.4f} 対 {float(v):.4f}")
    GSAME_L = dict(reference="data/21_06b_per_event.csv", reference_sha256=sha256(R6C), n_values=nL, max_abs_diff_km=worstL,
                   n_mismatch=len(badL), status=("PASS" if not badL else "FAIL"))
    print(f"[21_16] G-same-L(21_06b の CSV と、{NT} 地震 × C3・C4・L3・L4 × 4 時点 = {nL} 値・L が M6r に戻ったか・地震の集合): "
          f"最大の差 {worstL:.2g} km  不一致 {len(badL)}  {GSAME_L['status']}")
    if badL: stop("[21_16] STOP(G-same-L): 21_06b と値が違う。最初の 5 件: " + " / ".join(badL[:5]))

# ---------------------------------------------------------------- 14. 規則(事前に決めた判定)と記述
RNG_BOOT = np.random.default_rng(SEED)
def med_ci(x):
    x = x[np.isfinite(x)]
    if len(x) == 0: return (None, None, None)
    bs = np.median(x[RNG_BOOT.integers(0, len(x), (NBOOT, len(x)))], axis=1)
    return (float(np.median(x)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))
SUMM = {m: {t: dict(zip(("median_km", "ci_lo", "ci_hi"), med_ci(E[m][:, j])), available=float(np.mean(np.isfinite(E[m][:, j]))))
            for j, t in enumerate(TL) if not (m in ("C3", "C4", "L3", "L4") and t == "inf")} for m in METH}
def paired(A, B, j):
    x, y = E[A][:, j], E[B][:, j]; m = np.isfinite(x) & np.isfinite(y); nz = int(np.sum(x[m] != y[m]))
    d = dict(n=int(m.sum()), n_nonzero=nz, p=None, median_diff_km=None, frac_better=None, frac_tied=None)
    if m.sum() == 0: return d
    d.update(median_diff_km=float(np.median(x[m] - y[m])), frac_better=float(np.mean(x[m] < y[m])), frac_tied=float(np.mean(x[m] == y[m])))
    if nz >= 6: d["p"] = float(wilcoxon(x[m], y[m], alternative="less", zero_method="wilcox").pvalue)
    return d
def best_of(t):
    full = [m for m in BASE if SUMM[m][t]["available"] == 1.0 and SUMM[m][t]["median_km"] is not None]
    return min(full, key=lambda m: SUMM[m][t]["median_km"]) if full else None
def judge(meth, t, alpha, vs="BEST"):
    """勝ち = 中央値が相手より小さい・片側の対応 Wilcoxon の p < alpha・差が 0 でない組 10 以上・(BEST と比べる時は)BEST ≥ 0.5 km・評価 30 以上"""
    j = TL.index(t); best = best_of(t)
    comp = best if vs == "BEST" else vs
    if comp is None: return dict(method=meth, tau=t, alpha=alpha, comparator=None, best=None, win=False, testable=False, floor=False,
                                 note="no AI-free method gives every event a value")
    bm, cm = SUMM[comp][t]["median_km"], SUMM[meth][t]["median_km"]
    pr = paired(meth, comp, j); floor = (vs == "BEST") and bm < FLOOR_KM
    win = TESTABLE and (not floor) and cm is not None and cm < bm and pr["p"] is not None and pr["p"] < alpha and pr["n_nonzero"] >= MIN_NONZERO
    return dict(method=meth, tau=t, alpha=alpha, comparator=comp, best=best, best_median_km=SUMM[best][t]["median_km"], comparator_median_km=bm,
                median_km=cm, paired_vs_comparator=pr, floor=bool(floor), win=bool(win), testable=bool(TESTABLE), gain_km=(None if cm is None else bm - cm))
def frac_over(x):
    x = x[np.isfinite(x)]; return float(np.mean(x > TAIL_KM)) if len(x) else None
PER_TAU = {}
for j, t in enumerate(TL[:-1]):
    bb = best_of(t)
    PER_TAU[t] = dict(L4=judge("L4", t, ALPHA_L), L4_vs_C4=judge("L4", t, ALPHA_L, vs="C4"), L3=judge("L3", t, ALPHA_L),
                      C4=judge("C4", t, ALPHA_L), C3=judge("C3", t, ALPHA), L3_vs_C3=paired("L3", "C3", j),
                      tail_frac_over_10km=dict(BEST=(frac_over(E[bb][:, j]) if bb else None), C4=frac_over(E["C4"][:, j]), L4=frac_over(E["L4"][:, j])),
                      learned_fallback_frac=float(LFB[:, j].mean()), c3_fallback_frac=float(C3FB[:, j].mean()),
                      similarity_measured_frac=float(np.mean(NI[:, j] > 0)), stations_median=float(np.median(NST[:, j])),
                      features=dict(candidates_median=float(np.median(XA["ncand"][:, j])),
                                    n_common_picks_median=(float(np.nanmedian(XA["nc_med"][:, j])) if np.isfinite(XA["nc_med"][:, j]).any() else None),
                                    dd_offset_nan_frac_median=(float(np.nanmedian(XA["off_nan"][:, j])) if np.isfinite(XA["off_nan"][:, j]).any() else None),
                                    training_2026=TRAIN_FEAT[t]),
                      top10_true_dist_median_km=dict(C=(float(np.nanmedian(XA["topd_c"][:, j])) if np.isfinite(XA["topd_c"][:, j]).any() else None),
                                                     L=(float(np.nanmedian(XA["topd_l"][:, j])) if np.isfinite(XA["topd_l"][:, j]).any() else None)))
PRIM = PER_TAU[PRIMARY_TAU]["L4"]
FD = np.array([km_between(*to_ll(FIRST[ie][1], FIRST[ie][2]), SRC[ie, 0], SRC[ie, 1]) for ie in EVAL])
FT = np.array([TFIRST[ie] for ie in EVAL])
SPARSE = dict(test_events_lost_no_p=N_LOST, first_station_epi_km_median=float(np.median(FD)), first_p_after_origin_s_median=float(np.median(FT)),
              stations_with_p_median={t: float(np.median(NST[:, j])) for j, t in enumerate(TL)})
def f2(v): return "—" if v is None else f"{v:.2f}"
def fp(p): return "—" if p is None else f"{p:.2g}"
print(f"\n[21_16] ===== 網 {TAG}: 水平誤差の中央値 km(評価 {NT} 地震、局 {len(KEEP)}・最近接の間隔の中央値 {f2(NN_KEEP)} km) =====")
print("  P のある局の数(中央値) " + "  ".join(f"τ={t}: {np.median(NST[:, j]):.0f}" for j, t in enumerate(TL)))
for t, d in PER_TAU.items():
    h, fe = d["L4"], d["features"]
    if h.get("comparator") is None: print(f"  τ={t} s: BEST なし"); continue
    print(f"  τ={t:>3} s: BEST {h['best']} {f2(h['best_median_km'])} / C4 {f2(d['C4']['median_km'])} / L3 {f2(d['L3']['median_km'])} / L4 {f2(h['median_km'])}  "
          f"p(L4<BEST) {fp(h['paired_vs_comparator']['p'])}(組 {h['paired_vs_comparator']['n_nonzero']}){'・勝ち' if h['win'] else ''}  "
          f"p(L4<C4) {fp(d['L4_vs_C4']['paired_vs_comparator']['p'])}  L が M6r に戻った割合 {d['learned_fallback_frac']:.2f}  "
          f"10 km 超 BEST/C4/L4 {f2(d['tail_frac_over_10km']['BEST'])}/{f2(d['tail_frac_over_10km']['C4'])}/{f2(d['tail_frac_over_10km']['L4'])}")
    print(f"           特徴量: 共通の局の数の中央値 {f2(fe['n_common_picks_median'])}(2026 の学習 {f2(fe['training_2026']['n_common_picks_median'])})・"
          f"dd_offset が nan の割合 {f2(fe['dd_offset_nan_frac_median'])}(2026 {f2(fe['training_2026']['dd_offset_nan_frac'])})・"
          f"上位 10 の本当の距離の中央値 C {f2(d['top10_true_dist_median_km']['C'])} / L {f2(d['top10_true_dist_median_km']['L'])} km")
pp = PRIM["paired_vs_comparator"] if PRIM.get("comparator") else {}
print(f"\n[21_16] 網 {TAG} の主の規則(τ = 2 s の L4 対 BEST、α {ALPHA_L}): "
      + ("BEST なし" if PRIM.get("comparator") is None else
         f"L4 {f2(PRIM['median_km'])} 対 {PRIM['best']} {f2(PRIM['best_median_km'])} km  p = {fp(pp.get('p'))}  差が 0 でない組 {pp.get('n_nonzero')}  "
         f"床 {PRIM['floor']}  試せる {PRIM['testable']}  → {'勝ち' if PRIM['win'] else '勝ちなし'}")
      + ("(--limit: 動作確認、判定に使わない)" if a.limit else "(各 N の分類は 21_16b)"))
print("[21_16] 限界: " + " / ".join(LIMITS_09[-2:] + LIMITS_16[:3]))

# ---------------------------------------------------------------- 15. 出力
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
OUT_TAG = TAG + (SUF if SUF.startswith("_rerun") else "")
with open(ROOT / f"data/21_16_per_event_{OUT_TAG}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["origin_time", "mj", "lat", "lon", "depth_km", "first_p_after_origin_s", "first_station_epi_km"] + [f"n_sta_t{t}" for t in TL]
               + [f"n_i_t{t}" for t in TL[:-1]] + [f"c3_fallback_t{t}" for t in TL[:-1]] + [f"l_fallback_t{t}" for t in TL[:-1]]
               + [f"{m}_err_t{t}" for m in METH for t in (TL if m in BASE else TL[:-1])])
    for i, ie in enumerate(EVAL):
        w.writerow([OT[ie], f"{MAG[ie]:.1f}", f"{SRC[ie,0]:.4f}", f"{SRC[ie,1]:.4f}", f"{SRC[ie,2]:.2f}", f"{FT[i]:.3f}", f"{FD[i]:.3f}"]
                   + [int(v) for v in NST[i]] + [int(v) for v in NI[i]] + [int(v) for v in C3FB[i]] + [int(v) for v in LFB[i]]
                   + [("" if not np.isfinite(E[m][i, j]) else f"{E[m][i, j]:.4f}") for m in METH for j in (range(len(TL)) if m in BASE else range(len(TAUS)))])
out = dict(script="21_16a_ct2016_sparse_learned.py", version=VERSION, script_sha256=SELF_SHA, tag=TAG, out_tag=OUT_TAG, suffix=SUF, limit=a.limit,
           run_utc=utcnow(), sequence="Central Tottori 2016", cache=a.cache, cache_sha256=CACHE_SHA,
           network=dict(n_keep=a.n_keep, seed=a.seed, first_station_index=START, n_stations_all=len(STK), n_stations_kept=len(KEEP),
                        nn_spacing_median_km_all=NN_ALL, nn_spacing_median_km_kept=NN_KEEP, kept_stations_latlon=[ALLST[k] for k in sorted(KEEP)],
                        pick_rows_before=n_before, pick_rows_after=n_after),
           model=dict(train_json=a.train_json, train_json_sha256=TJ_SHA, model_sha256=TJ["model_sha256"], train_rows_sha256=TJ["train_rows_sha256"],
                      feature_block_sha256=FEAT_SHA, sklearn=sklearn.__version__, numpy=np.__version__, scipy=scipy.__version__),
           references=dict(run_21_09_json=str(R09J.relative_to(ROOT)), run_21_09_json_sha256=sha256(R09J), per_event_21_09_csv=str(R09C.relative_to(ROOT)),
                           per_event_21_09_csv_sha256=R09_SHA, script_21_09a_sha256=EXPECT_09A_SHA, judgment_21_06b_sha256=sha256(J06),
                           script_21_06b_sha256=JB["script_sha256"]),
           configs=CONFIGS, n_test=int(len(test_idx)), n_evaluated=NT, testable=bool(TESTABLE), min_test=MIN_TEST,
           velocity=dict(v0=V0, k=KG, vpvs=VPVS), laplace_b_s=LAP_B, kde_h_km=KDE_H, grid=dict(H_km=H, step_km=STEP, zfix_km=ZDEF),
           gates=dict(core=G_CORE, feat="PASS", model="PASS", ref06b="PASS", ref09="PASS", same=GSAME, same_learned=GSAME_L, causal=GC,
                      physics_inf_median_km=SUMM["M5"]["inf"]["median_km"]),
           sparseness=SPARSE, summary=SUMM, per_tau=PER_TAU, primary=PRIM,
           rule="per network: L4 at tau = 2 s wins vs BEST (smaller median, one-sided paired Wilcoxon zero_method='wilcox' p < 0.005, >= 10 non-zero "
                "pairs, BEST >= 0.5 km, >= 30 evaluated events; errors rounded to 4 decimals); per N in (12, 8, 5): wins in 3/3 seeds = HOLDS, 1-2 = "
                "MIXED, 0 = FAILS (untestable or floor networks count as no win); overall L4-SPARSE-HOLDS if all HOLDS, L4-SPARSE-FAILS if all FAILS, "
                "L4-SPARSE-PARTIAL otherwise (aggregated by 21_16b). L4 vs C4, L3 at 0.5 s vs BEST, other tau and the full network are descriptive",
           limits=LIMITS_ALL, runtime_s=time.time() - T0)
write_json_atomic(ROOT / f"models/21_16_run_{OUT_TAG}.json", clean(out))
log_open(f"completed: L4 at 2 s win={PRIM.get('win')} -> models/21_16_run_{OUT_TAG}.json")
print(f"[21_16] 出力: models/21_16_run_{OUT_TAG}.json・data/21_16_per_event_{OUT_TAG}.csv  ({time.time()-T0:.0f} s = {(time.time()-T0)/60:.1f} 分)")
