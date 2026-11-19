#!/usr/bin/env python3
# =============================================================================
# Script : 24_05_nagano2014_similarity_confirmation.py  (v1)
#          [「波形が似た過去の地震 × 物理」(C3)と「似た地震の通り道の補正」(C4)を、手を付けていない 4 つ目の余震系列
#           (長野県北部 2014、本震 2014-11-22 22:08 JST・Mj 6.7)で、21_02・21_04・21_20 と同じ規則のまま 1 回だけ確かめる。
#           あわせて H4(C3 対 C1)と H5(τ までの波形だけの検測)を、事前登録 24 で足した副の仮説として確かめる]
# Project: ARGUS(新生)— 論文の柱(4 つ目の系列での一発試験。変更の記録なしで回すことを目指す)
# 派生元 : 21_20_osaka2018_similarity_confirmation.py v1(SHA-256 2c0fb375e6a1a8d48d3ffbc611bb189b2390d224488cdd5585c76f5cadd5da43)。
#
# 21_20 v1 から変えたこと(DIFF_LOG_24.md に全ての差分):
#   1. 系列に依るもの: 入力の既定(data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt = 24_03 のキャッシュに
#      24_03h の R1 を当てたもの)、MAIN_UTC = 2014-11-22 13:08:17.9 UTC(24_00 の表示の 22:08:17.90 JST。確かめは 21_20 と同じ
#      「Mj 最大の地震が Mj ≥ 6.0、MAIN_UTC から 60 s 以内」)、G-untouched の期間 2014-11-20〜2014-12-17 UTC(24_01 の期間を日の単位で
#      含む)、出力の名前(models/24_05_*・data/24_05_per_event*.csv・PDF/24_05_F*)、表示・図の題・JSON の sequence と verdict_rule の
#      系列の名前、限界の文(LIMITS)。
#   2. H1〜H3・BEST・勝ちの規則・方法の計算・pool・ゲート(G-split・G-lib・G-causal・G-phys)・1 回だけの記録・dev・CSV の
#      21_20 の列は 21_20 v1 と同じ(関数 paired・judge に、比べる誤差の表を渡せる引数を足しただけ。既定では 21_20 と同じ計算)。
#   3. 足したもの(事前登録 24 の 2 節):
#      H4(副、α 0.005): τ = 2 s で、C3 が C1(一番似た過去の地震の気象庁の震央。先行研究の「一番似た過去の地震を引く」方式)に
#        勝つか。勝ち = C1 と C3 の両方に値がある地震で、C3 の中央値 < C1 の中央値・片側の対応 Wilcoxon の p < 0.005・差が 0 でない
#        組が 10 以上。床の規則は使わない(BEST との比較ではないため。21_20f の HL2 と同じ扱い)。
#      H5(副、α 0.01): 24_07 v3 が T(= 一番早いオフラインの P + τ)までの波形だけで決めた P・S に置き換えて、全ての方法を計算し直し、
#        τ = 2 s で C3 が BEST(置き換えた検測での BEST)に H1 と同じ規則で勝つか。似ている度合いの窓は、置き換えた P から切る。
#        24_07 の出力は、本番を開く前に、スクリプトの SHA-256(CAUSAL_SCRIPT_SHA)・キャッシュの SHA-256・CSV の SHA-256(24_07 の JSON
#        の csv_sha256)・全ての評価の地震 × 4 時点がそろっていることを確かめる(そろっていなければ開かずに STOP)。
#        24_07 が回せなかった・照合に落ちた時だけ、--no-causal で H5 を評価せずに H1〜H4 を回す(事前登録 24 の 5.5 節)。
#        H1〜H4 の結果は H5 の計算の前に models/24_05_judgment*_preH5.json に書く。H5 の計算の例外・STOP・H5 の経路の G-causal の FAIL は
#        止めずに H5 を NOT-EVALUATED とし、H1〜H4 はそのまま報告する。H5 の経路でも G-causal(未来を置き換えても同じ)を回す。
#      記述: 置き換えた検測での全ての方法の誤差(CSV の *_causal_err_t* の列、JSON の causal)、図 F4(オフラインと τ までの検測の
#        BEST・C3 の中央値)。H6(予測震度)は 24_08 が、この CSV から記述として計算する。
#
# 事前に固定した仮説と判定(この版の SHA-256 を、データを開く前に事前登録の記録 24 に書く):
#   BEST(τ) = AI を使わない 9 つの方法(M0r・Mp10・M1・M2・M3r・M5・M5f・M6p・M6r)のうち、評価する全ての地震で値がある
#   方法の中で中央値が最小のもの。勝ち = 中央値が BEST より小さい・片側の対応 Wilcoxon(zero_method='wilcox')の p が基準
#   未満・差が 0 でない組 10 以上・BEST が 0.5 km 以上(床でない)。
#     H1(主)  C3 @ τ = 2 s、p < 0.01   → CONFIRMED / PHYSICS-AT-FLOOR / NOT-CONFIRMED
#     H2(副)  C4 @ τ = 2 s、p < 0.005
#     H3(副)  C3 @ τ = 0.5 s、p < 0.005
#     H4(副)  C3 対 C1 @ τ = 2 s、p < 0.005(床の規則なし)
#     H5(副)  τ までの検測で C3 対 BEST @ τ = 2 s、p < 0.01(H1 と同じ規則。床の規則あり)
#   評価できる試験の地震が 30 未満なら INCONCLUSIVE。それ以外の τ・方法・感度は記述だけ。
#
# 限界(結果を読むときに必ず添える。表示と JSON にも英語で書く): LIMITS を見る。G-clock2(24_04d)の (c) が FAIL だった時は、事前登録 24 の
#   決まった印を結果に付ける(このスクリプトは G-clock2 の結果を読まない)。
#
# Usage : (先に Colab のノート 24_nagano2014_colab.ipynb のセル N1〜N16 で、R1 の後のキャッシュと 24_07 の出力を作り、G-clock2 を
#          確かめ、Mac の ~/SWIFT/data/nagano2014_processed/ にコピーする。手順は 24_STEPS_JA.md)
#         cd ~/SWIFT && caffeinate -i uv run python src/24_05_nagano2014_similarity_confirmation.py --dev   (動作確認。試験を開かない)
#         cd ~/SWIFT && caffeinate -i uv run python src/24_05_nagano2014_similarity_confirmation.py         (本番。1 回だけ)
# Output: models/24_05_judgment.json / models/24_05_opened.json / data/24_05_per_event.csv /
#         PDF/24_05_F1_error_vs_tau.pdf / PDF/24_05_F2_paired_difference.pdf / PDF/24_05_F3_similarity_vs_separation.pdf /
#         PDF/24_05_F4_causal_picks.pdf(--dev では _dev、2 回目以降は _rerun_<UTC の時刻>)
#         models/24_05_judgment_preH5.json(H5 の計算の前に書く H1〜H4)
# 所要  : CPU のみ。21_20 の約 2 倍(H5 のために全ての方法をもう 1 回計算する)。参考: 21_20 の本番は試験 55 地震で 175 s
# =============================================================================
import json, argparse, time, csv, hashlib, math, warnings, datetime as dt
from pathlib import Path
import numpy as np
import torch
from scipy.signal import butter, sosfilt
from scipy.stats import wilcoxon
warnings.filterwarnings("ignore", message="All-NaN slice")

ap = argparse.ArgumentParser()
ap.add_argument("--cache", default="data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt", help="24_03(15_01c v3.3 と同じ計算)の長野県北部 2014 の M>=1.5 版に、24_03h の R1 を当てたもの")
ap.add_argument("--causal-picks", default="data/nagano2014_processed/24_07_causal_picks_nagano2014.csv", help="24_07 v3 の --all-events の出力(H5)")
ap.add_argument("--causal-json", default="data/nagano2014_processed/24_07_causal_picks_nagano2014.json", help="24_07 v3 の記録(SHA-256 の照合)")
ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(pool の最後の新しい地震 20 個を代わりに使う)")
ap.add_argument("--no-causal", action="store_true", help="事前登録 24 の 5.5 節の場合だけ: 24_07 が STOP した・照合に落ちた時に、H5 を評価せずに H1〜H4 を回す")
a = ap.parse_args()

# ---------------------------------------------------------------- 事前に固定した値(変えたら版を上げる)
VERSION = "v1"
CAUSAL_SCRIPT_SHA = "b9b2fd5c8855c52f2e3a528e695374af752db3b0de6f789942e6da8824c2d14b"                # 24_07 v3 の SHA-256(凍結の時に書く。24_07 の JSON と照らす)
H4 = ("H4", "C3", "C1", "2")                      # 副: C3 が C1(一番似た地震の位置。先行研究の「似た地震を引く」方式)に勝つか、α 0.005
H5 = ("H5", "C3", "2")                            # 副: τ までの波形だけの検測で、C3 が BEST に勝つか、α 0.01(H1 と同じ規則)
FS, IP, NTS = 100.0, 300, 2048
TAUS = [0.5, 1.0, 2.0, 3.0]
PRIMARY = "2"                              # 主の判定(H1: C3、α 0.01)
SECONDARY = [("H2", "C4", "2"), ("H3", "C3", "0.5")]   # 副の判定(それぞれ α 0.005)
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
MAIN_UTC = dt.datetime(2014, 11, 22, 13, 8, 17, 900000)   # 24: 24_00 の表示の本震 2014-11-22 22:08:17.90 JST(± 60 s、Mj ≥ 6.0 は 21_20 と同じ確かめ)
UNTOUCHED_UTC = (dt.datetime(2014, 11, 20), dt.datetime(2014, 12, 17))    # G-untouched: 24_01 の期間(本震の 2 日前〜24 日後)を日の単位で含む
LIMITS = ["fourth sequence: Northern Nagano 2014 (mainshock 2014-11-22, 22:08:17.90 JST, Mj 6.7; JMA catalogue values, see 24_01's JSON), "
          "never used in ARGUS development; the hypotheses H1-H3 were fixed on West Tottori 2026 (21_01/21_02), tested on Central Tottori 2016 "
          "(21_04, with a documented deviation) and Northern Osaka 2018 (21_20, re-registered with amendment 04) and are applied here unchanged",
          "one fourth sequence only; before this preregistration the catalogue h2014 was opened once by 24_00 to count events "
          "(counts and the mainshock row only; no location list, waveform or method error was looked at)",
          "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
          "set of 50 stations also included non-Hi-net stations, so station types and geometry differ",
          "waveforms were downloaded around catalogue events only and converted to the West Tottori 2026 h5 form (30-s windows, "
          "per-window per-component z-score, JST epoch; 24_02 also stores the window mean and standard deviation); no filter was applied "
          "before the z-score (compared in 24_02 G-spec)",
          "the cache was built by 24_03, whose picking, QC and assembly are identical to 15_01c v3.3; 24_03h then removed every event "
          "with another catalogue event from 15 s before to 5 s after its origin (rule R1 of 21_20 amendment 04, fixed here before any "
          "Nagano waveform was opened; it uses origin times and Mj only), which can bias the sample against busy periods",
          "catalogue: JMA hypocentres from h2014 (whether h2014 is the final stage is to be confirmed); past-event locations are JMA "
          "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
          "the 2014 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
          "events. Manual and automatic hypocentres can be mixed (per-flag counts in 24_01's JSON)",
          "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); "
          "static station terms absorb a constant offset",
          "H1-H4 use offline PhaseNet picks on full records (possibly better than real-time picks); every method uses the same picks",
          "cache keeps up to 24 stations per event (PhaseNet P first, earliest first); no not-yet-arrived information is used",
          "cache waveforms had the full-window mean removed (includes future samples; removed by the 2 Hz high-pass except for a "
          "transient from the window start 3 s before P) and the source h5 is z-score normalised per 30-s window (the scale uses later "
          "samples of that window; cosine similarity is scale-invariant except where a window join falls inside the correlation window); "
          "the one-sample look-ahead of the cache's central-difference derivative is avoided by not using the last sample",
          "no picking or telemetry latency (tau is ideal elapsed time)",
          "the test events are small (1.5 <= Mj < 2.0); pick quality and station counts can differ from Mj >= 2.0 events",
          "the 2-8 Hz band was chosen after seeing 18_01 on West Tottori 2026",
          "C4's station terms come from past events' JMA hypocentres and truth is also JMA, so part of a C4 gain can be agreement with "
          "the JMA frame rather than better early information; C3all/C4all at all picks are reported to show this",
          "C4 corrects only arrived stations held by >= 3 top similar events; each past event's terms are demeaned by its own median "
          "P residual over all its stations, while uncorrected stations keep only the static term",
          "H4 compares C3 with C1 (the JMA epicentre of the most similar past event, the 'search the most similar past event' approach) "
          "on the events where C1 exists (C1 is undefined when fewer than 5 past events have a positive similarity)",
          "H5 re-runs every method with picks made by 24_07 from data up to T only (T = first offline P + tau); the tau origin, the "
          "station set (the cache stations) and the P search band (relative to the catalogue origin) still come from the offline picks "
          "and the catalogue; no Wadati QC or STA/LTA fallback at each time; the similarity windows start at the causal P; stations "
          "picked causally but without an offline PhaseNet P are used by the physics but not by the similarity; past events keep their "
          "offline picks (their records are complete at the time of the target event)",
          "H5 limits (continued): the event's first station (FIRST, used by M1, M3r, M5f, M6r, M6p and the C3/C4 prior) is still the "
          "earliest offline PhaseNet station; the similarity still uses the cache waveforms (full-window mean removed, built from the "
          "per-30-s-window z-scored h5), whereas 24_07 picked on h5 values reconstructed as z * win_std + win_mean, so the offline-vs-causal "
          "difference also contains this normalisation difference; a station whose shifted similarity window does not fit in the cached "
          "612 samples is not used by the similarity (the window end depends only on tau and the offline P and always fits, so this "
          "happens only when the causal P is more than 2.8 s earlier than the offline P); "
          "stations that were STA/LTA fallbacks offline enter the physics when 24_07 picked them; the West Tottori 2026 dev of 24_07 "
          "(30 events) was run on z-scored values, so the reconstruction was checked on synthetic data only before this test",
          "if 24_07 could not be run, its output failed the checks, the H5 computation raised an exception or the G-causal check on the "
          "causal-pick path failed, H5 is reported as NOT-EVALUATED and H1-H4 are reported unchanged (preregistration 24, section 5.5)",
          "H1 (C3 at tau = 2 s) is the primary test; H2, H3 and H4 are secondary at alpha 0.005; H5 (causal picks) uses the H1 rule at "
          "alpha 0.01 as a realism check; everything else is descriptive"]
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
print(f"[24_05] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
      f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")

# ---------------------------------------------------------------- 1. 入力
CP = ROOT / a.cache
if not CP.exists(): raise SystemExit(f"[24_05] STOP: {a.cache} が無い(ノート 24_nagano2014_colab.ipynb のセル N12 で作った tottori_parsed_realpick_nagano2014_m15_r1.pt を data/nagano2014_processed/ に置く)")
EVS = torch.load(CP, map_location="cpu", weights_only=False)
need = ["origin_time", "src_loc", "mw", "waveforms", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
for e in EVS:
    miss = [k for k in need if k not in e]
    if miss: raise SystemExit(f"[24_05] STOP: キャッシュの地震に {miss} が無い(24_03・24_03h の出力か確かめる)")
for e in EVS:
    w_ = np.asarray(e["waveforms"])
    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[24_05] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[24_05] STOP: {e['origin_time']} の波形に NaN か無限大")
def to_ns(o):
    import pandas as pd
    try:
        t = pd.Timestamp(str(o).replace("Z", "+00:00"))
        t = t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t
        return int(t.value)
    except Exception:
        raise SystemExit(f"[24_05] STOP: origin_time {o!r} を時刻として読めない")
OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
order = np.argsort(OTNS, kind="stable"); EVS = [EVS[i] for i in order]; OTNS = OTNS[order]
NE = len(EVS)
SRC = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS])
MAG = np.array([float(e["mw"]) for e in EVS])
OT = [str(e["origin_time"]) for e in EVS]
if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
    raise SystemExit("[24_05] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[24_05] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
# G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
lo_ns = int(np.datetime64(UNTOUCHED_UTC[0], "ns").astype(np.int64)); hi_ns = int(np.datetime64(UNTOUCHED_UTC[1], "ns").astype(np.int64))
n_out = int(np.sum((OTNS < lo_ns) | (OTNS > hi_ns))); n_big = int(np.sum(MAG >= 6.0 - 1e-6))
FRESH = MAG < FRESH_MAX_MAG - 1e-6
CACHE_SHA = sha256(CP)
n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
print(f"[24_05] 入力: 長野県北部 2014 の M ≥ 1.5 版(R1 の後) {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
      f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
print(f"[24_05] G-untouched: 期間 2014-11-20〜2014-12-17(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
      + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
if n_out != 0 or n_big != 1: raise SystemExit("[24_05] STOP(G-untouched): 長野県北部 2014 のキャッシュに見えない(この行を貼って相談)")
im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
    raise SystemExit(f"[24_05] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2014-11-22 13:08:17.9 UTC ± 60 s。24_00 の表示の 22:08:17.90 JST)")
CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
pool_idx = np.where(OTNS <= CUT_NS)[0]; test_idx = np.where((OTNS > CUT_NS) & FRESH)[0]
if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
    raise SystemExit("[24_05] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
print(f"[24_05] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
print(f"[24_05] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
      f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")

# ---------------------------------------------------------------- 2. 座標・検測(17_02 と同じ)
TFIRST = np.full(NE, np.nan)          # PhaseNet で測った最も早い P(気象庁の発生時刻からの s)
skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
for ie, e in enumerate(EVS):
    n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    ok = np.isfinite(tp) & (pf == 0)
    if ok.any(): TFIRST[ie] = float(tp[ok].min())
    kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
    if len(set(kk)) != n: raise SystemExit(f"[24_05] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
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
print(f"[24_05] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
if len(EVAL) == 0: raise SystemExit("[24_05] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
if a.dev: print(f"[24_05] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                "(較正にも入っているので値は楽観的)")

# ---------------------------------------------------------------- 24: H5 の材料(24_07 v3 の τ までの検測)を、開く前に確かめる
CAUS = None                                   # H5 の計算の間だけ CAUS_ALL を入れる(それ以外は None で、21_20 と同じ計算)
CP_C, CJ_C = ROOT / a.causal_picks, ROOT / a.causal_json
H5_SKIP = None                                # H5 を評価しなかった理由(評価した時は None)
if a.no_causal:
    H5_SKIP = "--no-causal: 24_07 could not be run or its output failed the checks (preregistration 24, section 5.5)"
    CAUS_ALL = {}
    print("[24_05] --no-causal: 24_07 の出力を読まない。H5 は評価しない(NOT-EVALUATED)。H1〜H4・HL・HG は同じ規則で回す(事前登録 24 の 5.5 節)")
elif not CP_C.exists() or not CJ_C.exists():
    raise SystemExit(f"[24_05] STOP: 24_07 の出力 {a.causal_picks} か {a.causal_json} が無い(ノートの セル N16 の後に Mac にコピーする)")
if not a.no_causal:
    CJ = json.load(open(CJ_C))
    if CJ.get("script_sha256") != CAUSAL_SCRIPT_SHA:
        raise SystemExit(f"[24_05] STOP: 24_07 の SHA-256 {str(CJ.get('script_sha256'))[:12]}… が凍結の値 {CAUSAL_SCRIPT_SHA[:12]}… と違う")
    if CJ.get("cache_sha256") != CACHE_SHA:
        raise SystemExit(f"[24_05] STOP: 24_07 が使ったキャッシュの SHA-256 {str(CJ.get('cache_sha256'))[:12]}… が、このキャッシュ {CACHE_SHA[:12]}… と違う")
    if CJ.get("csv_sha256") != sha256(CP_C):
        raise SystemExit("[24_05] STOP: 24_07 の CSV の SHA-256 が、24_07 の JSON に書かれた値と違う(別の実行の CSV か JSON を置いた)")
    if not CJ.get("all_events") or not CJ.get("raw_reconstructed"):
        raise SystemExit("[24_05] STOP: 24_07 が --all-events で、元の値に戻した h5(24_02)で回されていない")
    if len(set(OT)) != NE: raise SystemExit("[24_05] STOP: 発生時刻の同じ地震がキャッシュにある(24_07 の行を地震に対応付けられない)")
    CAUS_ALL, _OTI = {}, {OT[i]: i for i in range(NE)}
    with open(CP_C) as f:
        for r in csv.DictReader(f):
            ie_ = _OTI.get(r["origin_time"])
            if ie_ is None: raise SystemExit(f"[24_05] STOP: 24_07 の地震 {r['origin_time']} がキャッシュに無い")
            ff = lambda v: float(v) if v not in ("", "nan", None) else np.nan
            CAUS_ALL.setdefault((ie_, float(r["tau"])), {})[int(r["k"])] = (ff(r["c_tp"]), ff(r["c_ts"]), ff(r["off_tp"]))
    _miss = [(OT[ie][:19], t) for ie in EVAL for t in TAUS if (ie, float(t)) not in CAUS_ALL]
    if _miss: raise SystemExit(f"[24_05] STOP: 24_07 の検測が無い地震・時点 {len(_miss)}(最初 {_miss[0]})。評価の全ての地震 × 4 時点が要る")
    for ie in EVAL:
        for t in TAUS:
            d_ = CAUS_ALL[(ie, float(t))]; n_ = int(EVS[ie]["n_real_stations"]); tpo = np.asarray(EVS[ie]["tp_times"], float)[:n_]
            for k_, v_ in d_.items():
                if not (0 <= k_ < n_) or not (np.isnan(v_[2]) and np.isnan(tpo[k_]) or abs(v_[2] - tpo[k_]) < 1e-6):
                    raise SystemExit(f"[24_05] STOP: 24_07 の局 {k_} のオフラインの P が、キャッシュと合わない({OT[ie][:19]})")
    print(f"[24_05] H5 の材料: 24_07 v3 SHA-256 {CAUSAL_SCRIPT_SHA[:12]}…・同じキャッシュ・元の値に戻した h5・評価の {len(EVAL)} 地震 × 4 時点がそろっている")

# ---------------------------------------------------------------- 1 回だけの記録(本番は、試験の地震の結果を計算する前に書く)
OPEN = ROOT / "models/24_05_opened.json"
SUF = "_dev" if a.dev else ""
def log_open(status):
    rec = json.load(open(OPEN)) if OPEN.exists() else []
    rec.append(dict(utc=utcnow(), status=status, version=VERSION, script_sha256=SELF_SHA, cache_sha256=CACHE_SHA, suffix=SUF,
                    no_causal=bool(a.no_causal)))
    json.dump(rec, open(OPEN, "w"), indent=1)
if not a.dev:
    if OPEN.exists() or (ROOT / "models/24_05_judgment.json").exists():
        SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
        print(f"[24_05] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
    log_open("opened")
IN_H5 = False                                 # 24: H5 の計算の間は、止まった記録を書かない(H5 を NOT-EVALUATED にして続けるため)
def stop(msg):
    if not a.dev and not IN_H5: log_open("stopped: " + msg[:160])
    raise SystemExit(msg)

def picks_of(ie, tau=np.inf):
    """17_02 の picks_of と同じ(P は tp ≤ τ、S は tp + sp ≤ τ)。時刻は TFIRST を 0 にした値"""
    if CAUS is not None and (ie, float(tau)) in CAUS: return picks_of_causal(ie, tau)      # 24: H5 の計算の間だけ
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
def picks_of_causal(ie, tau):
    """24(H5): 24_07 が T = TFIRST + τ までの波形だけで決めた P・S(局の並び・形は picks_of と同じ)。P は c_tp − TFIRST ≤ τ、
    S は c_ts − TFIRST ≤ τ。オフラインの p_fallback・s_fallback は使わない(実時間では分からないため)"""
    e = EVS[ie]; n = int(e["n_real_stations"]); loc = np.asarray(e["sta_locs"], float)[:n]; D = CAUS[(ie, float(tau))]
    out = []
    for k in range(n):
        if k not in D: continue
        ctp, cts, _ = D[k]; tpr = ctp - TFIRST[ie]
        if not np.isfinite(tpr) or tpr > tau + EPS_T: continue
        tsr = cts - TFIRST[ie] if np.isfinite(cts) else np.nan
        wS = S_WEIGHT if (np.isfinite(tsr) and tsr <= tau + EPS_T) else 0.0
        x, y = to_xy(loc[k, 0], loc[k, 1]); z = -float(loc[k, 2]) * EL_SCALE
        out.append((skey(loc[k]), float(x), float(y), z, float(tpr), 1.0, float(tsr) if wS > 0 else np.nan, wS, k))
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
print(f"[24_05] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
      f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")

# ---------------------------------------------------------------- 4. 格子と探索(17_02 と同じ)
H = float(max(30.0, np.percentile(np.abs(np.r_[EX[CAL], EY[CAL]]), 99.5) + 30.0))
STEP = float(max(1.0, round(H / 30.0)))
ZMAX = float(max(30.0, np.percentile(SRC[CAL, 2], 99.5) * 1.3 + 10.0))
ZDEF = float(np.mean(SRC[CAL, 2]))
xc = np.arange(-H, H + 1e-6, STEP); zc = np.arange(0.0, ZMAX + 1e-6, STEP)
GX, GY, GZ = np.meshgrid(xc, xc, zc, indexing="ij"); COARSE = np.c_[GX.ravel(), GY.ravel(), GZ.ravel()]
XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
print(f"[24_05] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
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
print(f"[24_05] KDE の帯域(pool の一つ抜き): {KDE_H} km")
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
    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[24_05] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
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
    if CAUS is not None and (ie, float(tau)) in CAUS:           # 24(H5): 窓を τ までの検測の P から切る(キャッシュの波形はオフラインの P が IP)
        e = EVS[ie]; n = int(e["n_real_stations"]); tpo = np.asarray(e["tp_times"], float)[:n]
        for p in picks_of(ie, tau):
            nav = n_avail(tau, p[4])
            if nav < MINW_N or p[0] not in F or not np.isfinite(tpo[p[8]]): continue
            sh = int(round((p[4] + TFIRST[ie] - tpo[p[8]]) * FS))          # τ までの P − オフラインの P(サンプル)
            a0, a1 = IP + sh - PRE_N, IP + sh + nav
            if a0 < 0 or a1 > F[p[0]].shape[1]: continue                    # キャッシュの窓に収まらない局は使わない(限界に書く)
            out.append((p[0], F[p[0]][:, a0:a1]))
        return out
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
    if ie is not None and ie in top: stop("[24_05] STOP: 自分自身が似た地震の上位に入っている")
    out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
               C3=locate_map(pk, top), C4=None, fb=False, top1=int(top[0]), top=top, ncorr=0)
    if with_c4:
        dP, dS = corr_from(top, pk)
        out["C4"] = locate_map(pk, top, dP, dS); out["ncorr"] = len(dP)
    return out

# ---------------------------------------------------------------- 7. 1 つの地震の全ての方法
BASE = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]
NEW = ["C1", "C2", "C3", "C4"]
SENSN = ["C3_K5", "C3_K20", "C3_band4-16", "C3_buffer0.1h"]
ALLP = ["C3all", "C4all"]          # 記述: 全検測で、τ = 3 s の似た地震の上位を使った C3・C4(C4 の得が「気象庁の枠に合わせただけ」かを見る)
METH = BASE + NEW + SENSN + ALLP
TL = [f"{t:g}" for t in TAUS] + ["inf"]
def eval_event(ie, only_tau=None):
    lib = library(ie); libb = library(ie, BUFFER_SENS_H)
    if not np.array_equal(libb[:len(lib)], lib): stop("[24_05] STOP: 過去の一覧の並びがおかしい")
    p0 = FIRST[ie]
    m3 = prior_members(lib, p0[0], (p0[1], p0[2])); m3b = prior_members(libb, p0[0], (p0[1], p0[2]))
    m3p = prior_members(POOL_OK, p0[0], (p0[1], p0[2]))
    R = {m: np.full((len(TL), 2), np.nan) for m in METH}
    X = dict(nst=np.zeros(len(TL), int), ni=np.zeros(len(TAUS), int), smax=np.full(len(TAUS), np.nan),
             fb=np.zeros(len(TAUS), bool), top1=[None] * len(TAUS), ncorr=np.zeros(len(TAUS), int))
    top3 = None
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
        if t == "inf":
            if top3 is not None:
                R["C3all"][jt] = locate_map(pk, top3); R["C4all"][jt] = locate_map(pk, top3, *corr_from(top3, pk))
            continue
        Sb, nib = similarity(ie, tau, libb, BAND)            # 空白 0.1 時間の一覧(主の一覧はその先頭)
        S, ni = Sb[:len(lib)], nib
        o = c_from(S, lib, pk, m3, m6r, TOPK, ie=ie)
        for m in NEW:
            if o[m] is not None: R[m][jt] = o[m]
        X["ni"][jt], X["smax"][jt], X["fb"][jt], X["top1"][jt] = ni, (float(S.max()) if ni > 0 and len(S) else np.nan), o["fb"], o["top1"]
        X["ncorr"][jt] = o["ncorr"]
        if t == "3": top3 = o["top"]
        R["C3_K5"][jt] = c_from(S, lib, pk, m3, m6r, TOPK_SENS[0], with_c4=False)["C3"]
        R["C3_K20"][jt] = c_from(S, lib, pk, m3, m6r, TOPK_SENS[1], with_c4=False)["C3"]
        S2, _ = similarity(ie, tau, lib, BAND_SENS)
        R["C3_band4-16"][jt] = c_from(S2, lib, pk, m3, m6r, TOPK, with_c4=False)["C3"]
        R["C3_buffer0.1h"][jt] = c_from(Sb, libb, pk, m3b, locate_map(pk, m3b), TOPK, with_c4=False)["C3"]
    return R, X

# ---------------------------------------------------------------- 9. 評価
NT = len(EVAL)
if NT < MIN_TEST and not a.dev:
    print(f"[24_05] 判定(事前宣言、H1): INCONCLUSIVE(評価できる試験の地震 {NT} < {MIN_TEST})")
    json.dump(dict(script="24_05_nagano2014_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, verdict="INCONCLUSIVE",
                   utc=utcnow(), suffix=SUF, cache=a.cache, cache_sha256=sha256(CP), n_test=int(len(test_idx)),
                   n_fresh=int(FRESH.sum()), n_evaluated=NT, untouched=dict(n_outside_period=n_out, n_mj_ge_6=n_big,
                   n_mj2_library_only=n_extra2), limits=LIMITS),
              open(ROOT / f"models/24_05_judgment{SUF}.json", "w"), indent=1)
    log_open("completed: INCONCLUSIVE"); raise SystemExit(0)
P = {m: np.full((NT, len(TL), 2), np.nan) for m in METH}
NST = np.zeros((NT, len(TL)), int); NI = np.zeros((NT, len(TAUS)), int); SMAX = np.full((NT, len(TAUS)), np.nan)
C3FB = np.zeros((NT, len(TAUS)), bool); BESTSEP = np.full((NT, len(TAUS)), np.nan); NCORR = np.zeros((NT, len(TAUS)), int)
T_EV = time.time()
for ii, ie in enumerate(EVAL):
    try:
        R, X = eval_event(ie)
    except SystemExit:
        raise
    except BaseException as ex:
        stop(f"[24_05] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
    for m in METH: P[m][ii] = R[m]
    NST[ii], NI[ii], SMAX[ii], C3FB[ii], NCORR[ii] = X["nst"], X["ni"], X["smax"], X["fb"], X["ncorr"]
    for j, t1 in enumerate(X["top1"]):
        if t1 is not None: BESTSEP[ii, j] = km_between(SRC[t1, 0], SRC[t1, 1], SRC[ie, 0], SRC[ie, 1])
    if (ii + 1) % 10 == 0:
        el = time.time() - T_EV
        print(f"  … {ii+1}/{NT}  ({time.time()-T0:.0f} s、残りの見込み約 {el / (ii + 1) * (NT - ii - 1) / 60:.0f} 分)")

# ---------------------------------------------------------------- 10. ゲート G-causal(未来の波形と検測を変えても同じ)
gate_ev = [ii for ii in range(NT) if NI[ii, TAUS.index(1.0)] > 0][:N_GATE]
if len(gate_ev) < 3: stop(f"[24_05] STOP(G-causal): τ = 1 s で似ている度合いが測れた地震が {len(gate_ev)} しかなく、確かめられない")
gc_max, gc_n, pos_ctrl = 0.0, 0, None
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
# 陽性対照: 最初のゲートの地震・τ = 1 s で、過去の地震と共有する局の窓の最後の点を変えると、S(0 で切る前の値)が変わること
ie = EVAL[gate_ev[0]]; orig = EVS[ie]; lib0 = library(ie)
S0, _ = similarity(ie, 1.0, lib0, BAND, raw=True)
shared = [p for p in picks_of(ie, 1.0) if n_avail(1.0, p[4]) >= MINW_N and any(p[0] in filt_cached(j, BAND) for j in lib0)]
if not shared: stop("[24_05] STOP(G-causal): 陽性対照に使える局が無い(この行を貼って相談)")
pc = shared[0]; e2 = dict(orig); W = np.array(np.asarray(orig["waveforms"], float))
W[pc[8], :, IP + n_avail(1.0, pc[4]) - 1] += 50.0 * np.abs(W[pc[8], :, IP:IP + 100]).max()
e2["waveforms"] = W; EVS[ie] = e2; [FILT.pop((ie, b), None) for b in SOS]
S1, _ = similarity(ie, 1.0, lib0, BAND, raw=True)
EVS[ie] = orig; [FILT.pop((ie, b), None) for b in SOS]
pos_ctrl = float(np.max(np.abs(S1 - S0))) if len(S0) else 0.0
print(f"[24_05] G-causal({len(gate_ev)} 地震 × τ = 0.5・1・2・3 s、未来の波形と検測を置き換えた時の最大の差): {gc_max:.3g}  "
      f"陽性対照(窓の最後の点を変えた時の S の差): {pos_ctrl:.3g}  " + ("PASS" if (gc_max == 0.0 and pos_ctrl > 0) else "FAIL"))
if not (gc_max == 0.0 and pos_ctrl > 0): stop("[24_05] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")

# ---------------------------------------------------------------- 11. 誤差と判定
def herr(Pm):
    out = np.full(Pm.shape[:2], np.nan)
    for i, ie in enumerate(EVAL):
        for j in range(Pm.shape[1]):
            if np.isfinite(Pm[i, j, 0]):
                la, lo = to_ll(Pm[i, j, 0], Pm[i, j, 1]); out[i, j] = km_between(la, lo, SRC[ie, 0], SRC[ie, 1])
    return out
E = {m: herr(P[m]) for m in METH}
RNG_BOOT = np.random.default_rng(SEED)
def med_ci(x):
    x = x[np.isfinite(x)]
    if len(x) == 0: return (None, None, None)
    bs = np.median(x[RNG_BOOT.integers(0, len(x), (NBOOT, len(x)))], axis=1)
    return (float(np.median(x)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))
SUMM = {m: {t: dict(zip(("median_km", "ci_lo", "ci_hi"), med_ci(E[m][:, j])), available=float(np.mean(np.isfinite(E[m][:, j]))))
            for j, t in enumerate(TL)} for m in METH}
def paired(A, B, j, EE=None):
    EE = E if EE is None else EE                                   # 24: 比べる誤差の表(既定は 21_20 と同じ E)
    x, y = EE[A][:, j], EE[B][:, j]; m = np.isfinite(x) & np.isfinite(y); nz = int(np.sum(x[m] != y[m]))
    d = dict(n=int(m.sum()), n_nonzero=nz, p=None, median_diff_km=None, frac_better=None, frac_tied=None)
    if m.sum() == 0: return d
    d.update(median_diff_km=float(np.median(x[m] - y[m])), frac_better=float(np.mean(x[m] < y[m])), frac_tied=float(np.mean(x[m] == y[m])))
    if nz >= 6: d["p"] = float(wilcoxon(x[m], y[m], alternative="less", zero_method="wilcox").pvalue)
    return d
phys_inf = SUMM["M5"]["inf"]["median_km"]
print(f"[24_05] G-phys(τ = ∞ の M5 の中央値 ≤ 0.5 km): {'—' if phys_inf is None else f'{phys_inf:.3f}'} km  " + ("PASS" if phys_inf is not None and phys_inf <= 0.5 else "FAIL")
      + "(参考: 15_12 は 0.13 km、分け方が違う)")
if not (phys_inf is not None and phys_inf <= 0.5): stop("[24_05] STOP(G-phys): 物理を長野に正しく移せていない可能性(この行を貼って相談)")
def judge(meth, t, alpha, EE=None, SS=None):
    SS = SUMM if SS is None else SS                                # 24: 既定は 21_20 と同じ SUMM・E
    j = TL.index(t)
    full = [m for m in BASE if SS[m][t]["available"] == 1.0 and SS[m][t]["median_km"] is not None]
    best = min(full, key=lambda m: SS[m][t]["median_km"])
    bm, cm = SS[best][t]["median_km"], SS[meth][t]["median_km"]
    pr = paired(meth, best, j, EE); floor = bm < FLOOR_KM
    win = (not floor) and cm is not None and cm < bm and pr["p"] is not None and pr["p"] < alpha and pr["n_nonzero"] >= MIN_NONZERO
    return dict(method=meth, tau=t, alpha=alpha, best=best, best_median_km=bm, median_km=cm, paired_vs_best=pr, floor=bool(floor),
                win=bool(win), at_or_below_0p7_best=bool(cm is not None and cm <= BAR * bm), vs_M6r=paired(meth, "M6r", j, EE),
                vs_M6p=paired(meth, "M6p", j, EE))
PER_TAU = {}                       # 記述だけ(勝ち負けは HYP に書く)
def describe(meth, t):
    d = judge(meth, t, ALPHA); d.pop("win"); d.pop("alpha"); return d
for j, t in enumerate(TL[:-1]):
    PER_TAU[t] = dict(C3=describe("C3", t), C4=describe("C4", t), C4_vs_C3=paired("C4", "C3", j),
                      c3_fallback_frac=float(C3FB[:, j].mean()), similarity_measured_frac=float(np.mean(NI[:, j] > 0)),
                      c4_corrected_stations_median=(float(np.median(NCORR[~C3FB[:, j], j])) if (~C3FB[:, j]).any() else None),
                      c4_equals_c3_frac=float(np.mean(np.all(P["C4"][:, j] == P["C3"][:, j], axis=1))),
                      stations_median=float(np.median(NST[:, j])))
ji = TL.index("inf")
_sh = np.all([np.isfinite(E[m][:, ji]) for m in ("M5", "M6r", "C3all", "C4all")], axis=0)     # 4 つ全てに値がある地震だけ
ALLPICKS = dict(C4all_vs_M5=paired("C4all", "M5", ji), C4all_vs_C3all=paired("C4all", "C3all", ji), n_shared=int(_sh.sum()),
                medians_km={m: (float(np.median(E[m][_sh, ji])) if _sh.any() else None) for m in ("M5", "M6r", "C3all", "C4all")})
HYP = {"H1": judge("C3", PRIMARY, ALPHA)}
for name, meth, t in SECONDARY: HYP[name] = judge(meth, t, ALPHA_SEC)
h1 = HYP["H1"]
VERDICT = ("INCONCLUSIVE" if NT < MIN_TEST else "CONFIRMED" if h1["win"] else "PHYSICS-AT-FLOOR" if h1["floor"] else "NOT-CONFIRMED")
if a.dev: VERDICT = "DEV (no verdict)"

# ---------------------------------------------------------------- 24: H4(C3 対 C1)と H5(τ までの検測)
def clean_early(o):
    if isinstance(o, dict): return {str(k): clean_early(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean_early(v) for v in o]
    if isinstance(o, np.ndarray): return [clean_early(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
def judge_vs(meth, other, t, alpha):
    """H4: 両方に値がある地震で比べる。床の規則なし(BEST との比較でないため)"""
    j = TL.index(t); x, y = E[meth][:, j], E[other][:, j]; m = np.isfinite(x) & np.isfinite(y)
    pr = paired(meth, other, j)
    cm = float(np.median(x[m])) if m.any() else None; om = float(np.median(y[m])) if m.any() else None
    win = (cm is not None and om is not None and cm < om and pr["p"] is not None and pr["p"] < alpha and pr["n_nonzero"] >= MIN_NONZERO)
    return dict(method=meth, other=other, tau=t, alpha=alpha, n_both=int(m.sum()), median_km=cm, other_median_km=om,
                paired=pr, other_available_frac=float(np.mean(np.isfinite(y))), win=bool(win))
HYP24 = {"H4": judge_vs(H4[1], H4[2], H4[3], ALPHA_SEC)}
CM_C = BASE + NEW
PC = {m: np.full((NT, len(TL), 2), np.nan) for m in CM_C}; NSTC = np.zeros((NT, len(TAUS)), int); NIC = np.zeros((NT, len(TAUS)), int)
SMAXC = np.full((NT, len(TAUS)), np.nan); GC_C = None
# H1〜H4 の結果を、H5 の計算の前に書いておく(H5 の計算で途切れても、H1〜H4 の結果が残る。最終の JSON は下の 12 節で書く)
json.dump(clean_early(dict(script="24_05_nagano2014_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, suffix=SUF,
                           status="H1-H4 written before H5; the final file is models/24_05_judgment" + SUF + ".json",
                           summary=SUMM, hypotheses=HYP, verdict=VERDICT, hypotheses_24=HYP24, utc=utcnow())),
          open(ROOT / f"models/24_05_judgment{SUF}_preH5.json", "w"), indent=1)
def gate_causal_path():
    """G-causal を H5 の経路(τ までの検測・ずらした窓)でも回す: 各局のキャッシュの波形のうち、時刻 T(= TFIRST + τ)より後の
    サンプル(時刻が T を超えるもの。T 以前で最後のサンプルの次から)を全て乱数に置き換えても、H5 の結果が同じこと。キャッシュの波形はオフラインの P(IP)に合わせて並んでいるので、
    T 以前で最後のサンプルの位置は floor(IP + (τ − (オフラインの P − TFIRST))·FS)(オフラインの P が T より後の局では IP より前)。
    オフラインの P・S の時刻は、波形の位置の帳簿として残す(H5 の経路は 24_07 の P・S を使い、オフラインの P は窓の位置合わせに
    だけ使う)。オフラインの P が無い局は全てを置き換える(似ている度合いには使われない)"""
    mx, n_ = 0.0, 0
    for ii in gate_ev:
        ie = EVAL[ii]; orig = EVS[ie]
        for t in ("0.5", "1", "2", "3"):
            tau = float(t); jt = TL.index(t)
            e2 = dict(orig); n = int(orig["n_real_stations"])
            W = np.array(np.asarray(orig["waveforms"], float)); tp = np.asarray(orig["tp_times"], float); tpr = tp[:n] - TFIRST[ie]
            for k in range(n):
                cut = 0 if not np.isfinite(tpr[k]) else int(np.clip(IP + np.floor((tau - tpr[k]) * FS + 1e-3) + 1, 0, NTS))
                W[k, :, cut:] = RNG_GATE.standard_normal((3, NTS - cut)) * 1e3
            e2["waveforms"] = W
            EVS[ie] = e2; [FILT.pop((ie, b), None) for b in SOS]
            try:
                R2, X2 = eval_event(ie, only_tau=t)
            finally:
                EVS[ie] = orig; [FILT.pop((ie, b), None) for b in SOS]
            for m in CM_C:
                a1, a2 = PC[m][ii, jt], R2[m][jt]
                if np.isnan(a1).any() != np.isnan(a2).any(): mx = np.inf
                elif not np.isnan(a1).any(): mx = max(mx, float(np.max(np.abs(a1 - a2))))
            j0 = TAUS.index(tau)
            if np.isfinite(SMAXC[ii, j0]) or np.isfinite(X2["smax"][j0]):
                mx = max(mx, abs(np.nan_to_num(SMAXC[ii, j0], nan=-9.0) - np.nan_to_num(X2["smax"][j0], nan=-9.0)))
            n_ += 1
    return mx, n_
if H5_SKIP is None:
    CAUS = CAUS_ALL; T_C = time.time(); IN_H5 = True
    try:
        for ii, ie in enumerate(EVAL):
            Rc, Xc = eval_event(ie)
            for m in CM_C: PC[m][ii] = Rc[m]
            NSTC[ii] = Xc["nst"][:len(TAUS)]; NIC[ii] = Xc["ni"]; SMAXC[ii] = Xc["smax"]
            if (ii + 1) % 10 == 0:
                print(f"  … H5 {ii+1}/{NT}  (残りの見込み約 {(time.time() - T_C) / (ii + 1) * (NT - ii - 1) / 60:.0f} 分)")
        gc_c, gc_cn = gate_causal_path()
        GC_C = dict(max_diff=gc_c, n_checks=gc_cn)
        print(f"[24_05] G-causal(H5 の経路: τ までの検測・ずらした窓、{len(gate_ev)} 地震 × 4 時点): {gc_c:.3g}  " + ("PASS" if gc_c == 0.0 else "FAIL"))
        if gc_c != 0.0: H5_SKIP = "G-causal on the causal-pick path failed (max difference %.3g)" % gc_c
    except (Exception, SystemExit) as ex:        # H5 だけを評価しないで、H1〜H4 の結果は残す(事前登録 24 の 5.5 節)。Ctrl-C は止まる
        H5_SKIP = f"{'stop' if isinstance(ex, SystemExit) else 'exception'} during the H5 computation: {type(ex).__name__}: {str(ex)[:200]}"
    CAUS = None; FILT.clear(); IN_H5 = False
    if H5_SKIP is not None: print(f"[24_05] H5 は評価しない(NOT-EVALUATED): {H5_SKIP}")
EC = {m: herr(PC[m]) for m in CM_C}
for m in CM_C: EC[m][:, TL.index("inf")] = np.nan                  # 全検測(τ = ∞)はオフラインの検測なので H5 の表には入れない
if H5_SKIP is not None:
    for m in CM_C: EC[m][:] = np.nan
SUMMC = {m: {t: dict(zip(("median_km", "ci_lo", "ci_hi"), med_ci(EC[m][:, j])), available=float(np.mean(np.isfinite(EC[m][:, j]))))
             for j, t in enumerate(TL[:-1])} for m in CM_C}
if H5_SKIP is None:
    HYP24["H5"] = judge(H5[1], H5[2], ALPHA, EC, SUMMC)
    PER_TAU_C = {t: dict(C3=judge("C3", t, ALPHA, EC, SUMMC), stations_median=float(np.median(NSTC[:, j])),
                         similarity_measured_frac=float(np.mean(NIC[:, j] > 0)),
                         stations_median_offline=float(np.median(NST[:, j]))) for j, t in enumerate(TL[:-1])}
    for t in PER_TAU_C: PER_TAU_C[t]["C3"].pop("win"); PER_TAU_C[t]["C3"].pop("alpha")
else:
    HYP24["H5"] = dict(method=H5[1], tau=H5[2], alpha=ALPHA, status="NOT-EVALUATED", reason=H5_SKIP, win=False)
    PER_TAU_C = {}

def f2(v): return "—" if v is None else f"{v:.2f}"
def fp(p): return "—" if p is None else f"{p:.2g}"
print(f"\n[24_05] ===== 水平誤差の中央値 km [95% 区間](評価 {NT} 地震{'、dev(楽観的)' if a.dev else ''}) =====")
print("  方法           " + "".join(f"{('τ=' + t + ' s') if t != 'inf' else '全検測':>24}" for t in TL))
for m in METH:
    print(f"  {m:<15}" + "".join((f"{f2(SUMM[m][t]['median_km'])} [{f2(SUMM[m][t]['ci_lo'])},{f2(SUMM[m][t]['ci_hi'])}]"
                                   if SUMM[m][t]['median_km'] is not None else "—").rjust(24) for t in TL))
print("  P のある局の数(中央値) " + "  ".join(f"τ={t}: {np.median(NST[:, j]):.0f}" for j, t in enumerate(TL)))
for t, d in PER_TAU.items():
    for m in ("C3", "C4"):
        h = d[m]; pb = h["paired_vs_best"]
        print(f"  τ={t} s {m}: BEST = {h['best']} {h['best_median_km']:.2f} km / {m} {f2(h['median_km'])} km  "
              f"p({m} < BEST) = {fp(pb['p'])}(差が 0 でない組 {pb['n_nonzero']}/{pb['n']})  FLOOR={h['floor']}  "
              f"0.7×BEST 以下={h['at_or_below_0p7_best']}  p({m} < M6r) = {fp(h['vs_M6r']['p'])}")
    print(f"        p(C4 < C3) = {fp(d['C4_vs_C3']['p'])}  C4 で補正した局の数(M6r に戻らなかった地震の中央値){f2(d['c4_corrected_stations_median'])}・"
          f"C4 = C3 の割合 {d['c4_equals_c3_frac']:.2f}・似ている度合いを測れた割合 {d['similarity_measured_frac']:.2f}・"
          f"C3/C4 が M6r に戻った割合 {d['c3_fallback_frac']:.2f}")
print(f"  全検測(記述、4 つ全てに値がある {ALLPICKS['n_shared']} 地震): M5 {f2(ALLPICKS['medians_km']['M5'])} / C3all {f2(ALLPICKS['medians_km']['C3all'])} / "
      f"C4all {f2(ALLPICKS['medians_km']['C4all'])} km  p(C4all < M5) = {fp(ALLPICKS['C4all_vs_M5']['p'])}"
      "(全検測でも C4 が物理より良いなら、その分は早さではなく気象庁の震源の枠に合わせた効果の可能性)")
print(f"\n[24_05] ===== 事前宣言の判定 =====")
for name, h in HYP.items():
    pb = h["paired_vs_best"]
    print(f"  {name}{'(主)' if name == 'H1' else '(副)'}: {h['method']} @ τ = {h['tau']} s  {f2(h['median_km'])} km 対 BEST {h['best']} "
          f"{h['best_median_km']:.2f} km  p = {fp(pb['p'])}(基準 {h['alpha']})  差が 0 でない組 {pb['n_nonzero']}  FLOOR={h['floor']}  "
          f"→ {'勝ち' if h['win'] else '勝ちなし'}")
h4, h5 = HYP24["H4"], HYP24["H5"]
print(f"  H4(副): C3 対 C1 @ τ = {h4['tau']} s(両方に値がある {h4['n_both']} 地震。C1 がある割合 {h4['other_available_frac']:.2f})  "
      f"C3 {f2(h4['median_km'])} km 対 C1 {f2(h4['other_median_km'])} km  p = {fp(h4['paired']['p'])}(基準 {h4['alpha']})  "
      f"差が 0 でない組 {h4['paired']['n_nonzero']}  → {'勝ち' if h4['win'] else '勝ちなし'}")
if H5_SKIP is None:
    print(f"  H5(副): τ までの波形だけの検測で C3 @ τ = {h5['tau']} s  {f2(h5['median_km'])} km 対 BEST {h5['best']} {h5['best_median_km']:.2f} km  "
          f"p = {fp(h5['paired_vs_best']['p'])}(基準 {h5['alpha']})  差が 0 でない組 {h5['paired_vs_best']['n_nonzero']}  FLOOR={h5['floor']}  "
          f"→ {'勝ち' if h5['win'] else '勝ちなし'}")
else:
    print(f"  H5(副): NOT-EVALUATED(評価しなかった。理由: {H5_SKIP})")
print("  τ までの検測(記述): " + "  ".join(f"τ={t}: 局 {d['stations_median']:g}(オフライン {d['stations_median_offline']:g})・BEST {d['C3']['best']} "
                                        f"{d['C3']['best_median_km']:.2f}・C3 {f2(d['C3']['median_km'])} km" for t, d in PER_TAU_C.items()))
print(f"\n[24_05] 判定(事前宣言、H1): {VERDICT}")
print("[24_05] 限界: " + " / ".join(LIMITS))

# ---------------------------------------------------------------- 12. 出力(JSON・CSV を図より先に)
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
CM = BASE + NEW + SENSN + ALLP
with open(ROOT / f"data/24_05_per_event{SUF}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["origin_time", "mj", "lat", "lon", "depth_km"] + [f"n_sta_t{t}" for t in TL] + [f"n_i_t{t}" for t in TL[:-1]]
               + [f"smax_t{t}" for t in TL[:-1]] + [f"best_template_sep_km_t{t}" for t in TL[:-1]] + [f"c3_fallback_t{t}" for t in TL[:-1]]
               + [f"c4_n_corrected_t{t}" for t in TL[:-1]]
               + [f"{m}_err_t{t}" for m in CM for t in (TL if m in BASE else ["inf"] if m in ALLP else TL[:-1])]
               + [f"n_sta_causal_t{t}" for t in TL[:-1]] + [f"{m}_causal_err_t{t}" for m in CM_C for t in TL[:-1]])
    for i, ie in enumerate(EVAL):
        w.writerow([OT[ie], f"{MAG[ie]:.1f}", f"{SRC[ie,0]:.4f}", f"{SRC[ie,1]:.4f}", f"{SRC[ie,2]:.2f}"] + [int(v) for v in NST[i]]
                   + [int(v) for v in NI[i]] + [("" if not np.isfinite(v) else f"{v:.4f}") for v in SMAX[i]]
                   + [("" if not np.isfinite(v) else f"{v:.3f}") for v in BESTSEP[i]] + [int(v) for v in C3FB[i]] + [int(v) for v in NCORR[i]]
                   + [("" if not np.isfinite(E[m][i, j]) else f"{E[m][i, j]:.4f}") for m in CM
                      for j in (range(len(TL)) if m in BASE else [ji] if m in ALLP else range(len(TAUS)))]
                   + [(int(v) if H5_SKIP is None else "") for v in NSTC[i]] + [("" if not np.isfinite(EC[m][i, j]) else f"{EC[m][i, j]:.4f}") for m in CM_C
                                                  for j in range(len(TAUS))])
out = dict(script="24_05_nagano2014_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
           sequence="Northern Nagano 2014", suffix=SUF, cache=a.cache, cache_sha256=sha256(CP),
           n_fresh=int(FRESH.sum()), n_events=NE, n_pool=int(len(pool_idx)), n_test=int(len(test_idx)),
           n_no_measured_p=int((~HASP).sum()), n_evaluated=NT, mainshock=dict(origin_time=OT[im], mj=float(MAG[im])),
           pool_cut_utc_ns=int(CUT_NS),
           fixed=dict(taus=TAUS, primary=PRIMARY, secondary=SECONDARY, alpha_secondary=ALPHA_SEC, min_corr=MIN_CORR,
                      min_mag=MIN_MAG, fresh_max_mag=FRESH_MAX_MAG, match_s=MATCH_S, pool_h=POOL_H, buffer_h=BUFFER_H, band_hz=BAND, band_sens_hz=BAND_SENS, pre_s=PRE_S,
                      min_win_s=MIN_WIN_S, max_win_s=MAX_WIN_S, max_lag_s=MAX_LAG_S, topk=TOPK, topk_sens=TOPK_SENS, min_pos=MIN_POS,
                      buffer_sens_h=BUFFER_SENS_H, s_weight=S_WEIGHT, shrink=SHRINK, min_prior_ev=MIN_PRIOR_EV, prior_eps=PRIOR_EPS,
                      floor_km=FLOOR_KM, min_test=MIN_TEST, alpha=ALPHA, min_nonzero=MIN_NONZERO, bar=BAR, nboot=NBOOT, seed=SEED,
                      eps_t=EPS_T),
           velocity=dict(v0=V0, k=KG, vpvs=VPVS), laplace_b_s=LAP_B, kde_h_km=KDE_H, grid=dict(H_km=H, step_km=STEP, finest_km=STEP / 25,
                                                                                               zmax_km=ZMAX, zfix_km=ZDEF),
           gates=dict(split="PASS", lib="PASS (checked for every evaluated event)", causal=dict(max_diff=gc_max, positive_control=pos_ctrl,
                      n_checks=gc_n, events=[OT[EVAL[i]] for i in gate_ev]), physics_inf_median_km=phys_inf),
           summary=SUMM, per_tau=PER_TAU, all_picks=ALLPICKS, hypotheses=HYP, verdict=VERDICT,
           hypotheses_24=HYP24, causal=dict(evaluated=H5_SKIP is None, not_evaluated_reason=H5_SKIP, no_causal_option=bool(a.no_causal),
                                            script_sha256=CAUSAL_SCRIPT_SHA, picks_csv=a.causal_picks,
                                            picks_csv_sha256=(sha256(CP_C) if CP_C.exists() and not a.no_causal else None),
                                            json_sha256=(sha256(CJ_C) if CJ_C.exists() and not a.no_causal else None),
                                            gate_causal_path=GC_C, summary=SUMMC, per_tau=PER_TAU_C),
           untouched=dict(n_outside_period=n_out, n_mj_ge_6=n_big, n_mj2_library_only=n_extra2),
           verdict_rule="BEST(tau) = smallest median among the 9 AI-free methods that give an estimate for every evaluated event "
                        "(chosen on the evaluated events). A hypothesis wins if the method median < BEST median, one-sided paired "
                        "Wilcoxon (zero_method='wilcox') p < alpha with >= 10 non-zero pairs, and BEST >= 0.5 km (not FLOOR). "
                        "H1 (primary): C3 at tau = 2 s, alpha 0.01 -> CONFIRMED / PHYSICS-AT-FLOOR / NOT-CONFIRMED; INCONCLUSIVE if "
                        "fewer than 30 evaluated events. H2: C4 at tau = 2 s, H3: C3 at tau = 0.5 s, each alpha 0.005 (secondary). "
                        "Test events: 1.5 <= Mj < 2.0 events later than mainshock + 72 h (Northern Nagano 2014; same rule as 21_02 v2, 21_04 v1 and 21_20 v1). "
                        "Added in preregistration 24: H4 (secondary, alpha 0.005): C3 vs C1 at tau = 2 s on events where both exist, "
                        "win if the C3 median < the C1 median, one-sided paired Wilcoxon p < 0.005 and >= 10 non-zero pairs (no floor rule). "
                        "H5 (secondary, alpha 0.01): every method recomputed with 24_07 picks made from data up to T = first P + tau; "
                        "C3 vs BEST (BEST chosen on these picks) at tau = 2 s with the H1 rule including the floor",
           limits=LIMITS, runtime_s=time.time() - T0)
json.dump(clean(out), open(ROOT / f"models/24_05_judgment{SUF}.json", "w"), indent=1)
if not a.dev: log_open("completed: " + VERDICT)

# ---------------------------------------------------------------- 13. 図(白背景・英語・凡例は枠外)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 10})
LAB = {"M0r": "Past-event centroid", "Mp10": "Centroid of previous 10 events", "M1": "First-P station",
       "M2": "Centroid of triggered stations", "M3r": "Seismicity prior (same first station)", "M5": "Physics only (solved events only)",
       "M5f": "Physics, first-station fallback", "M6p": "Physics x prior (pool events)", "M6r": "Physics x prior (past events)",
       "C2": "Waveform similarity only (median of top events; non-fallback events)", "C3": "Physics x similarity prior (C3, H1/H3)",
       "C4": "C3 + similar-event station terms (C4, H2)"}
STY = {"M0r": ("0.6", ":"), "Mp10": ("0.4", ":"), "M1": ("tab:brown", "--"), "M2": ("tab:olive", "--"), "M3r": ("tab:purple", "-."),
       "M5": ("tab:blue", ":"), "M5f": ("tab:green", "--"), "M6p": ("tab:cyan", "--"), "M6r": ("tab:blue", "-"),
       "C2": ("tab:orange", "--"), "C3": ("tab:red", "-"), "C4": ("tab:pink", "-")}
xs = np.array(TAUS); TT = TL[:-1]
def arr(m, key): return np.array([np.nan if SUMM[m][t][key] is None else SUMM[m][t][key] for t in TT])
fig, ax = plt.subplots(figsize=(9.0, 4.8))
for m in ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r", "C2", "C3", "C4"]:
    c, ls = STY[m]
    ax.plot(xs, arr(m, "median_km"), ls, color=c, marker="o", ms=4, lw=2.4 if m == "C3" else 1.3, label=LAB[m])
    ax.fill_between(xs, arr(m, "ci_lo"), arr(m, "ci_hi"), color=c, alpha=0.08, lw=0)
for t, x in zip(TT, xs):
    ax.plot([x], [PER_TAU[t]["C3"]["best_median_km"]], marker="s", ms=9, mfc="none", mec="k", ls="none",
            label="BEST AI-free method at each tau" if t == TT[0] else None)
ax.axhline(FLOOR_KM, color="k", lw=0.8, ls="--")
ax.text(xs[-1] / 1.03, FLOOR_KM * 1.06, f"floor {FLOOR_KM} km", fontsize=8, ha="right", va="bottom")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xticks(xs); ax.set_xticklabels([f"{t:g}" + {"2": "\n(H1, H2)", "0.5": "\n(H3)"}.get(f"{t:g}", "\n(desc.)") for t in TAUS])
ax.minorticks_off()
ax.set_xlabel("Time since first P pick, tau (s)"); ax.set_ylabel("Median epicentral error vs JMA (km)")
ax.set_title(f"Northern Nagano 2014, {'DEV (pool events, optimistic)' if a.dev else 'test events'}, n = {NT}; shading = 95% bootstrap CI",
             fontsize=10)
ax.grid(alpha=0.3, which="both"); ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F1_error_vs_tau{SUF}.pdf", bbox_inches="tight"); plt.close(fig)

fig, axs = plt.subplots(1, len(TT), figsize=(3.3 * len(TT), 3.8), sharey=True)
for ax, t, j in zip(np.atleast_1d(axs), TT, range(len(TT))):
    b = PER_TAU[t]["C3"]["best"]
    for m, c, ls, lw in (("C4", "tab:pink", "-", 1.2), ("C3", "tab:red", "--", 1.8)):
        d = E[m][:, j] - E[b][:, j]; d = np.sort(d[np.isfinite(d)])
        ax.plot(d, np.arange(1, len(d) + 1) / max(len(d), 1), color=c, ls=ls, lw=lw, drawstyle="steps-post", label=f"{m} minus BEST")
    ax.axvline(0, color="k", lw=0.8)
    tied = PER_TAU[t]["C3"]["paired_vs_best"]["frac_tied"]; tied4 = PER_TAU[t]["C4"]["paired_vs_best"]["frac_tied"]
    tag = {"2": " (H1: C3, H2: C4)", "0.5": " (H3: C3)"}.get(t, " (descriptive)")
    ax.set_title(f"tau = {t} s{tag}\nBEST = {b}; tied C3 {0 if tied is None else tied:.0%}, C4 {0 if tied4 is None else tied4:.0%}", fontsize=9)
    ax.set_xlabel("Error difference (km); < 0 = better than BEST"); ax.grid(alpha=0.3)
np.atleast_1d(axs)[0].set_ylabel("Fraction of events")
h_, l_ = np.atleast_1d(axs)[0].get_legend_handles_labels()
fig.legend(h_, l_, loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=2, fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F2_paired_difference{SUF}.pdf", bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(7.6, 4.4))
for j, (t, c) in enumerate(zip(TT, ("tab:green", "tab:blue", "tab:orange", "tab:red"))):
    m = np.isfinite(SMAX[:, j]) & np.isfinite(BESTSEP[:, j])
    ax.scatter(SMAX[m, j], np.maximum(BESTSEP[m, j], 0.01), s=14, color=c, alpha=0.7, label=f"tau = {t} s")
ax.set_xlabel("Best similarity score S (0-1)"); ax.set_ylabel("Epicentral distance to most similar past event (km)\n(values < 0.01 km shown at 0.01)")
ax.set_yscale("log"); ax.grid(alpha=0.3, which="both")
ax.set_title("Is the most similar past event close by?", fontsize=10)
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F3_similarity_vs_separation{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
fig, ax = plt.subplots(figsize=(7.8, 4.4))
for lab_, S_, ls_ in ((("offline picks", SUMM, "-"),) + ((("picks from data up to T only (H5)", SUMMC, "--"),) if H5_SKIP is None else ())):
    bb = [PER_TAU[t]["C3"]["best"] if S_ is SUMM else PER_TAU_C[t]["C3"]["best"] for t in TT]
    ax.plot(xs, [S_[b][t]["median_km"] if S_[b][t]["median_km"] is not None else np.nan for b, t in zip(bb, TT)], ls_, color="k", marker="s",
            ms=5, label=f"BEST, {lab_}")
    ax.plot(xs, [S_["C3"][t]["median_km"] if S_["C3"][t]["median_km"] is not None else np.nan for t in TT], ls_, color="tab:red", marker="o",
            ms=5, label=f"C3, {lab_}")
ax.axhline(FLOOR_KM, color="0.4", lw=0.8, ls=":")
ax.text(xs[-1] / 1.03, FLOOR_KM * 1.06, f"floor {FLOOR_KM} km", fontsize=8, ha="right", va="bottom")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xticks(xs); ax.set_xticklabels([f"{t:g}" for t in TAUS]); ax.minorticks_off()
_lo, _hi = ax.get_ylim(); _yt = [v for v in (0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50) if _lo <= v <= _hi]
ax.set_yticks(_yt); ax.set_yticklabels([f"{v:g}" for v in _yt])
ax.set_xlabel("Time since first P pick, tau (s)"); ax.set_ylabel("Median epicentral error vs JMA (km)")
ax.set_title(f"Northern Nagano 2014, {'DEV' if a.dev else 'test'} events (n = {NT}): offline vs causal picks"
             + ("" if H5_SKIP is None else "\n(H5 not evaluated: causal picks not available)"), fontsize=10)
ax.grid(alpha=0.3, which="both"); ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F4_causal_picks{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
print(f"[24_05] 出力: models/24_05_judgment{SUF}.json, data/24_05_per_event{SUF}.csv, PDF/24_05_F1〜F4{SUF}.pdf"
      + ("" if a.dev else ", models/24_05_opened.json") + f"  ({time.time()-T0:.0f} s)")
