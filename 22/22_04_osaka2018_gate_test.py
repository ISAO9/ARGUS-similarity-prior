#!/usr/bin/env python3
# =============================================================================
# Script : 22_04_osaka2018_gate_test.py  (v1)
#          [信頼の切り替え G の試験(1 回だけ): 凍結した G(models/22_gate.pkl)を、手を付けていない大阪府北部 2018 の試験の地震に当て、
#           「物理(C4)と記憶(C1)のどちらを信じるか」を AI が決めると、C4 より大きな外れが減るか(HG1)、固定の規則 R より良いか(HG2)を判定する]
# Project: ARGUS(新生)— AI を「物理の部品」として使う。22 では AI が「どちらの答えを信じるか」を決める(事前登録 22_00)
#
# 何をするか(全て 22_00 の 2 節のとおり。この版の SHA-256 を、大阪を開く前に 22_00 の 7 節に書いて push する):
#   1. 21_20_osaka2018_similarity_confirmation.py v1 の 1〜6 節(入力・G-untouched・G-split・座標と検測・速度と局の補正・格子と探索・
#      事前分布と C4 の材料・波形の似ている度合い・c_from)を、計算は 1 字も変えずに写す。違うのは画面の表示の [21_20] を [22_04] にした所、
#      引数 --ref-suffix を足した所、21_20 の「1 回だけの記録」の部分を 22_04 の照合の準備(下の 3)に置き換えた所だけ
#      (22_04 の記録は models/22_04_opened.json。21_20 の記録は読むだけで書かない)。
#   2. 22 GATE FEATURES(22_01a と同じ)・22 GATE APPLY(22_02 と同じ)・判定の関数 verdict(22_02 と同じ)を写し、
#      写した部分の SHA-256 が凍結の記録(22_00 の 7 節)と同じでなければ STOP。
#   3. 照合の準備(全て、速度・格子の計算と「opened」の前に済ませる。どれかが違えば STOP し、1 回だけの記録は書かない):
#      凍結した G の SHA-256・G の中の 2 つの部分の SHA-256・学習の行の SHA-256・p の境目 0.5・R のしきい値 10 km が 22_00 の 7 節と同じ。
#      G を凍結した時刻(models/22_02_opened.json の最初の completed)が、21_20 を開いた時刻(models/21_20_opened.json の最初の行)より前。
#      21_20 の正式な結果(--ref-suffix。既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)が、
#      models/21_20_opened.json で最初に completed になった実行で、登録した 21_20 v1 のスクリプト(SHA-256 2c0fb375e6a1…)・同じキャッシュ・
#      mode = test のもの。CSV の地震が試験の地震と同じで、C1・C3・C4・M6r の列が 4 時点ともある。
#      21_20 が「評価できる地震 30 未満」で INCONCLUSIVE に終わった時は、22_04 は開かずに INCONCLUSIVE を models/22_04_judgment.json に書く。
#   4. 1 回だけの記録 models/22_04_opened.json に「opened」を書いてから、試験の地震 × 4 時点で M6r・C1・C2・C3・C4 を 21_20 と同じ呼び方で
#      計算する(m3 = prior_members、M6r = locate_map(pk, m3)、S = similarity(ie, τ, lib, 2–8 Hz)、c_from)。
#      G-same: 各地震を計算した直後に、C1・C3・C4・M6r の誤差を 21_20 の CSV と比べ、6e-5 km を超えて違えばその場で STOP。
#   5. 誤差を小数 4 桁に丸め(学習の行と同じ)、13 の手がかりを作り、凍結した G で選ぶ(p ≥ 0.5 なら C1、それ以外と C1 が無い地震は C4)。
#      規則 R(C4 と C1 が 10 km 以上食い違えば C1)も出す。判定の部分の中で止まった時も「stopped」を記録する。
#   6. 判定(τ = 2 s。評価できる地震 = τ = 2 s の全ての試験の地震。C1 が無い地震も G = R = C4 として数える):
#        HG1(主)G 対 C4: 10 km 超の外れ。食い違う対の正確な片側 McNemar(binomtest(G だけ外れ, 食い違う対, 0.5, 'less'))p < 0.005
#        HG2(主)G 対 R : 地震ごとの誤差。片側の対応 Wilcoxon(zero_method 'wilcox'、method 'approx'、correction False)p < 0.005、
#                         差が 0 でない対 10 以上(10 未満なら HG2 は成り立たないとして扱う)
#        守り     G の中央値 ≤ C4 の中央値 + 0.05 km
#        INCONCLUSIVE(地震 30 未満、または HG1 の食い違う対 8 未満)→ GATE-CONFIRMED(HG1・HG2・守り)→
#        GATE-HELPS-NOT-BEYOND-RULE(HG1・守り)→ GATE-NOT-CONFIRMED(それ以外)
#      副の仮説 HG3(主の判定には関わらず、別に報告する): τ = 1 s で G 対 R、HG2 と同じ片側の対応 Wilcoxon、p < 0.005、
#        差が 0 でない対 10 以上(足りない時と地震 30 未満は INCONCLUSIVE)→ SUPPORTED / NOT-SUPPORTED / INCONCLUSIVE
#   7. 記述(判定しない): 他の τ の表・外れの確率 q の較正(Brier 得点と、学習の行の基準率だけで当てた時の Brier 得点)・
#      手がかりが学習の行の範囲の外にある割合(data/22_01a_rows_wt2026.npz があれば。SHA-256 を照合)。
#   8. 出力: models/22_04_judgment.json・data/22_04_per_event.csv・PDF/22_04_F1_gate_osaka.pdf(白背景・英語・凡例は枠外)。
#      判定の JSON を書いた直後に「completed」を記録する(図で落ちても判定は残る)。2 回目以降は上書きせず _rerun_<UTC> の名前に書く
#      (扱いは 22_00 の 3 節: 開いた後にスクリプトが自分で止めたら使い切り、機械的に途切れた時だけ 1 回やり直してよい)。
#
# --dev: 試験を開かない動作確認(21_20 の dev と同じ、pool の最後の使っていない地震 20 個。data/21_20_per_event_dev.csv と照合。出力に _dev。
#        評価の地震が 30 未満なので判定は必ず INCONCLUSIVE。1 回だけの記録は書かない)。
#
# 限界(結果に必ず添える。JSON にも英語で書く): 22_00 の 4 節(学習は鳥取県西部 2026 の 1 系列だけ・正解も過去の地震の位置も気象庁の震源・
#   C1 は既知の場所しか答えられない・R のしきい値 10 km は鳥取県中部 2016 を見て決めた・手がかり 9 は早い時点ではほぼ効かない)と、
#   21_20 の限界(局は Hi-net だけ・h2018 の震源・オフラインの PhaseNet の検測・遅れなし など)。
#
# Usage : (先に 21_20 を、21_20 の事前登録の記録どおりに本番まで回す。22_04 は 21_20 の出力と照合する)
#         cd ~/SWIFT && caffeinate -i uv run python src/22_04_osaka2018_gate_test.py --dev   (動作確認。試験を開かない)
#         cd ~/SWIFT && caffeinate -i uv run python src/22_04_osaka2018_gate_test.py         (本番。1 回だけ)
#         (21_20 の正式な結果が _rerun_<UTC> の時だけ: ... src/22_04_osaka2018_gate_test.py --ref-suffix _rerun_<UTC>)
# 入力  : data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt・models/22_gate.pkl・models/22_02_opened.json・
#         models/21_20_opened.json・models/21_20_judgment.json・data/21_20_per_event.csv(--dev なら両方 _dev)・(あれば)data/22_01a_rows_wt2026.npz
# Output: models/22_04_judgment.json / models/22_04_opened.json / data/22_04_per_event.csv / PDF/22_04_F1_gate_osaka.pdf
# 止める条件(STOP): 21_20 と同じもの(入力・G-untouched・G-split・G-lib)・写した部分か凍結した G か学習の行の SHA-256 が記録と違う・
#                   G-leak・G の凍結が 21_20 を開いた後・21_20 の結果が無いか、正式な結果でないか、合わない・G-same・
#                   C4 の誤差が無い地震がある・手がかり 9 以外が値なし
# 所要  : CPU のみ。21_20 より短い見込み(21_20 は感度の計算のため、似ている度合いを 1 時点あたり 2 回計算する。22_04 は 1 回)
# =============================================================================
import json, argparse, time, csv, hashlib, math, warnings, datetime as dt
from pathlib import Path
import numpy as np
import torch
from scipy.signal import butter, sosfilt
from scipy.stats import wilcoxon
warnings.filterwarnings("ignore", message="All-NaN slice")

ap = argparse.ArgumentParser()
ap.add_argument("--cache", default="data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt", help="21_20c(15_01c v3.3 と同じ計算)の大阪府北部 2018 の M>=1.5 版")
ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(pool の最後の新しい地震 20 個を代わりに使う)")
ap.add_argument("--ref-suffix", default="", help="22_04: 比べる相手の 21_20 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
a = ap.parse_args()

# ---------------------------------------------------------------- 事前に固定した値(変えたら版を上げる)
VERSION = "v1"
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
MAIN_UTC = dt.datetime(2018, 6, 17, 22, 58, 30)   # 21_20: 気象庁の発表の 07:58 JST の 1 分の真ん中(秒までの値ではない。±60 s でこの 1 分を含む)。要確認
UNTOUCHED_UTC = (dt.datetime(2018, 6, 15), dt.datetime(2018, 7, 12))     # G-untouched: 21_20a の期間(本震の 2 日前〜24 日後)を含む
LIMITS = ["third sequence: Northern Osaka 2018 (mainshock 2018-06-18, 07:58 JST; origin time and Mj are those of the JMA catalogue, "
          "see 21_20a's JSON), never used in ARGUS development; the hypotheses were fixed on West Tottori 2026 (21_01/21_02), "
          "tested on Central Tottori 2016 (21_04, run with a documented deviation) and are applied here unchanged",
          "one third sequence only",
          "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
          "set of 50 stations also included non-Hi-net stations, so station types and geometry differ",
          "waveforms were downloaded around catalogue events only and converted to the West Tottori 2026 h5 form (30-s windows, "
          "per-window per-component z-score, JST epoch); whether a filter was applied before the z-score in the 2026 h5 is not recorded "
          "(none here; compared in 21_20b G-spec)",
          "the cache was built by 21_20c, whose picking, QC and assembly are identical to 15_01c v3.3 (itself identical to v3 except "
          "the window-index file name and output folder); 21_20c changed only labels, defaults and required arguments",
          "catalogue: JMA hypocentres from h2018 (whether h2018 is the final stage is to be confirmed; West Tottori 2026 used the "
          "unified catalogue); past-event locations are JMA "
          "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
          "the 2018 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
          "events; whether the 2026 catalogue excluded them is not recorded. Manual and automatic hypocentres are mixed (per-flag "
          "counts in 21_20a's JSON)",
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
          "the JMA frame rather than better early information; C3all/C4all at all picks are reported to show this",
          "C4 corrects only arrived stations held by >= 3 top similar events; each past event's terms are demeaned by its own median "
          "P residual over all its stations, while uncorrected stations keep only the static term",
          "H1 (C3 at tau = 2 s) is the primary test; H2 and H3 are secondary at alpha 0.005; everything else is descriptive"]

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
print(f"[22_04] 本スクリプト(22_04){VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
      f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")

# ---------------------------------------------------------------- 1. 入力
CP = ROOT / a.cache
if not CP.exists(): raise SystemExit(f"[22_04] STOP: {a.cache} が無い(ノート 21_20_osaka2018_colab.ipynb のセル 11 で作った tottori_parsed_realpick_osaka2018_m15.pt を data/osaka2018_processed/ に置く)")
EVS = torch.load(CP, map_location="cpu", weights_only=False)
need = ["origin_time", "src_loc", "mw", "waveforms", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
for e in EVS:
    miss = [k for k in need if k not in e]
    if miss: raise SystemExit(f"[22_04] STOP: キャッシュの地震に {miss} が無い(21_20c の出力か確かめる)")
for e in EVS:
    w_ = np.asarray(e["waveforms"])
    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[22_04] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[22_04] STOP: {e['origin_time']} の波形に NaN か無限大")
def to_ns(o):
    import pandas as pd
    try:
        t = pd.Timestamp(str(o).replace("Z", "+00:00"))
        t = t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t
        return int(t.value)
    except Exception:
        raise SystemExit(f"[22_04] STOP: origin_time {o!r} を時刻として読めない")
OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
order = np.argsort(OTNS, kind="stable"); EVS = [EVS[i] for i in order]; OTNS = OTNS[order]
NE = len(EVS)
SRC = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS])
MAG = np.array([float(e["mw"]) for e in EVS])
OT = [str(e["origin_time"]) for e in EVS]
if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
    raise SystemExit("[22_04] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[22_04] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
# G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
lo_ns = int(np.datetime64(UNTOUCHED_UTC[0], "ns").astype(np.int64)); hi_ns = int(np.datetime64(UNTOUCHED_UTC[1], "ns").astype(np.int64))
n_out = int(np.sum((OTNS < lo_ns) | (OTNS > hi_ns))); n_big = int(np.sum(MAG >= 6.0 - 1e-6))
FRESH = MAG < FRESH_MAX_MAG - 1e-6
CACHE_SHA = sha256(CP)
n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
print(f"[22_04] 入力: 大阪府北部 2018 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
      f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
print(f"[22_04] G-untouched: 期間 2018-06-15〜2018-07-12(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
      + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
if n_out != 0 or n_big != 1: raise SystemExit("[22_04] STOP(G-untouched): 大阪府北部 2018 のキャッシュに見えない(この行を貼って相談)")
im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
    raise SystemExit(f"[22_04] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2018-06-17 22:58 UTC の 1 分 ± 60 s。気象庁の発表の 07:58 JST)")
CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
pool_idx = np.where(OTNS <= CUT_NS)[0]; test_idx = np.where((OTNS > CUT_NS) & FRESH)[0]
if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
    raise SystemExit("[22_04] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
print(f"[22_04] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
print(f"[22_04] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
      f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")

# ---------------------------------------------------------------- 2. 座標・検測(17_02 と同じ)
TFIRST = np.full(NE, np.nan)          # PhaseNet で測った最も早い P(気象庁の発生時刻からの s)
skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
for ie, e in enumerate(EVS):
    n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    ok = np.isfinite(tp) & (pf == 0)
    if ok.any(): TFIRST[ie] = float(tp[ok].min())
    kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
    if len(set(kk)) != n: raise SystemExit(f"[22_04] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
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
print(f"[22_04] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
if len(EVAL) == 0: raise SystemExit("[22_04] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
if a.dev: print(f"[22_04] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                "(較正にも入っているので値は楽観的)")

# ---------------------------------------------------------------- 1 回だけの記録と照合の準備(22_04。重い計算と、開く前に全て済ませる)
# 21_20 の記録(models/21_20_opened.json)は読むだけで書かない。照合が全て通った後、試験の地震の結果を計算する前に 9 節で「opened」を書く
import re, sys, platform, pickle
OPEN = ROOT / "models/22_04_opened.json"
SUF = "_dev" if a.dev else ""
OPENED, DONE = False, False
def log_open(status):
    rec = json.load(open(OPEN)) if OPEN.exists() else []
    rec.append(dict(utc=utcnow(), status=status, version=VERSION, script_sha256=SELF_SHA, cache_sha256=CACHE_SHA, suffix=SUF))
    json.dump(rec, open(OPEN, "w"), indent=1)
def stop(msg):
    if OPENED and not a.dev: log_open("stopped: " + msg[:160])
    raise SystemExit(msg)
FROZEN = dict(gate_pkl="358e3daddfc0c9dd3c95e35d92bb9c83a2123ee459f2bb5b657b0be10ce11555",
              features="c2a1eabfaaa5f94f359f965dfdaf720ca2437164bf3954f0f543e1eaf5772263",
              apply="fcc56fd873cb9919fc8e8c9b3b518e11ef59f42db121d52c53202b208ae82cbc",
              rows="b57caba76f0d8cca1a5ca952afe17b494897ef76c4ac98cecb63fa8d27c48d59",
              script_21_20="2c0fb375e6a1a8d48d3ffbc611bb189b2390d224488cdd5585c76f5cadd5da43")   # 22_00 の 7 節(2026-11-02 の凍結)
P_CHOOSE_REG, THR_R_REG = 0.5, 10.0                                                         # 22_00 の 1.3・2 節
# (a) 写した部分と凍結した G
FB = open(Path(__file__), encoding="utf-8").read()
# 印の文字はこの照合の行にも出てくるので、ファイルの後ろの方(本物の部分)を rindex で探す
def blk(b, e): return hashlib.sha256(FB[FB.rindex(b):FB.rindex(e)].encode()).hexdigest()
GATE_SHA = blk("# >>> 22 GATE FEATURES BEGIN", "# <<< 22 GATE FEATURES END")
APPLY_SHA = blk("# >>> 22 GATE APPLY BEGIN", "# <<< 22 GATE APPLY END")
if GATE_SHA != FROZEN["features"]: raise SystemExit(f"[22_04] STOP: 手がかりの部分の SHA-256 {GATE_SHA[:12]}… が凍結の記録と違う")
if APPLY_SHA != FROZEN["apply"]: raise SystemExit(f"[22_04] STOP: 判定に使う部分(22 GATE APPLY)の SHA-256 {APPLY_SHA[:12]}… が凍結の記録と違う")
GBLK = FB[FB.rindex("# >>> 22 GATE FEATURES BEGIN"):FB.rindex("# <<< 22 GATE FEATURES END")]
leak = re.findall(r"SRC\s*\[|MAG\s*\[|E[XY]\s*\[\s*ie\s*\]|OTNS\s*\[|RES\s*\[|EVS\s*\[|\bOT\s*\[|src_loc|TFIRST\s*\[", GBLK)
if leak: raise SystemExit(f"[22_04] STOP(G-leak): 手がかりの部分に正解か目標の地震の値を読む所がある {sorted(set(leak))}")
print(f"[22_04] 写した部分の SHA-256: 手がかり {GATE_SHA[:12]}…・判定 {APPLY_SHA[:12]}…(凍結の記録と同じ)  G-leak PASS")
MP = ROOT / "models/22_gate.pkl"
if not MP.exists(): raise SystemExit("[22_04] STOP: models/22_gate.pkl が無い(22_02 で凍結したもの)")
MODEL_SHA = sha256(MP)
if MODEL_SHA != FROZEN["gate_pkl"]: raise SystemExit(f"[22_04] STOP: models/22_gate.pkl の SHA-256 {MODEL_SHA[:12]}… が凍結の記録(358e3daddfc0…)と違う")
with open(MP, "rb") as f: GATE = pickle.load(f)
if (GATE["gate_feature_block_sha256"] != GATE_SHA or GATE["gate_apply_block_sha256"] != APPLY_SHA or GATE["rows_sha256"] != FROZEN["rows"]
        or GATE["p_choose"] != P_CHOOSE_REG or GATE["thr_R_km"] != THR_R_REG):
    raise SystemExit("[22_04] STOP: 凍結した G の中の部分の SHA-256・学習の行・p の境目・R のしきい値のどれかが、凍結の記録と違う")
print(f"[22_04] 凍結した G: models/22_gate.pkl  SHA-256 {MODEL_SHA[:12]}…(凍結の記録と同じ)  p ≥ {GATE['p_choose']} で C1、R は {GATE['thr_R_km']} km")
# (b) G は大阪を開く前に凍結した(22_02 の最初の completed の時刻 < 21_20 の最初の記録の時刻)
O22, O20 = ROOT / "models/22_02_opened.json", ROOT / "models/21_20_opened.json"
if not O22.exists(): raise SystemExit("[22_04] STOP: models/22_02_opened.json が無い(G を凍結した時刻を確かめられない)")
c22 = [r for r in json.load(open(O22)) if str(r.get("status", "")).startswith("completed") and r.get("suffix", "") == ""]
if not c22: raise SystemExit("[22_04] STOP: models/22_02_opened.json に最初の本番の completed が無い")
T_FREEZE = c22[0]["utc"]
# (c) 比べる相手: 21_20 の正式な結果(--ref-suffix。既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC> を指定する)
if a.dev:
    REFCSV, J20P = ROOT / "data/21_20_per_event_dev.csv", ROOT / "models/21_20_judgment_dev.json"
else:
    REFCSV, J20P = ROOT / f"data/21_20_per_event{a.ref_suffix}.csv", ROOT / f"models/21_20_judgment{a.ref_suffix}.json"
if not J20P.exists(): raise SystemExit(f"[22_04] STOP: {J20P.relative_to(ROOT)} が無い(先に 21_20{' --dev' if a.dev else ''} を回す)")
j20 = json.load(open(J20P))
if j20.get("script_sha256") != FROZEN["script_21_20"]: raise SystemExit("[22_04] STOP: 21_20 の結果が、登録した 21_20 v1 のスクリプト(SHA-256 2c0fb375e6a1…)のものでない")
if j20.get("cache_sha256") != CACHE_SHA: raise SystemExit("[22_04] STOP: キャッシュの SHA-256 が 21_20 の結果と違う")
if not a.dev:
    if not O20.exists(): raise SystemExit("[22_04] STOP: models/21_20_opened.json が無い")
    r20 = json.load(open(O20))
    if not (T_FREEZE < r20[0]["utc"]): raise SystemExit(f"[22_04] STOP: G の凍結({T_FREEZE})が 21_20 を開いた時刻({r20[0]['utc']})より後")
    c20 = [r for r in r20 if str(r.get("status", "")).startswith("completed")]
    if not c20 or c20[0].get("suffix", "") != a.ref_suffix or j20.get("suffix", "") != a.ref_suffix:
        raise SystemExit(f"[22_04] STOP: --ref-suffix '{a.ref_suffix}' が、models/21_20_opened.json で最初に completed になった 21_20 の実行と違う")
    print(f"[22_04] 21_20 の正式な結果: suffix '{a.ref_suffix}'(最初の completed)・スクリプトとキャッシュの SHA-256 が同じ  G の凍結 {T_FREEZE} < 21_20 を開いた時刻 {r20[0]['utc']}")
    if j20.get("verdict") == "INCONCLUSIVE" and int(j20.get("n_evaluated", 0)) < MIN_TEST:
        JP0 = ROOT / "models/22_04_judgment.json"
        if JP0.exists(): raise SystemExit("[22_04] STOP: models/22_04_judgment.json が既にある")
        json.dump(dict(script="22_04_osaka2018_gate_test.py", version=VERSION, script_sha256=SELF_SHA, mode="test", sequence="Northern Osaka 2018",
                       verdict="INCONCLUSIVE", reason=f"21_20 evaluated {j20.get('n_evaluated')} < {MIN_TEST} test events; 22_04 was not opened",
                       ref_judgment=str(J20P.relative_to(ROOT)), utc=utcnow()), open(JP0, "w"), indent=1)
        print(f"[22_04] 判定: INCONCLUSIVE(21_20 の評価できる地震 {j20.get('n_evaluated')} < {MIN_TEST}。22_04 は開かない)  記録: models/22_04_judgment.json")
        raise SystemExit(0)
    if j20.get("mode") != "test": raise SystemExit("[22_04] STOP: 21_20 の結果が本番(mode = test)でない")
if not REFCSV.exists(): raise SystemExit(f"[22_04] STOP: {REFCSV.relative_to(ROOT)} が無い")
ref = {r["origin_time"]: r for r in csv.DictReader(open(REFCSV))}
if sorted(ref) != sorted(OT[ie] for ie in EVAL):
    raise SystemExit(f"[22_04] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
if not a.dev and int(j20.get("n_evaluated", -1)) != len(EVAL): raise SystemExit("[22_04] STOP: 21_20 の評価の地震の数が、ここで作った試験の地震の数と違う")
TL4 = [f"{t:g}" for t in TAUS]
CHK = ["C3", "C4", "M6r", "C1"]
miss_cols = [f"{m}_err_t{t}" for m in CHK for t in TL4 if f"{m}_err_t{t}" not in next(iter(ref.values()))]
if miss_cols: raise SystemExit(f"[22_04] STOP(G-same): {REFCSV.name} に照合する列が無い {miss_cols[:4]}")
REF_SHA = sha256(REFCSV)
print(f"[22_04] 比べる相手: {REFCSV.relative_to(ROOT)}(SHA-256 {REF_SHA[:12]}…)  {len(EVAL)} 地震 × 4 時点、C1・C3・C4・M6r")
# (d) 学習の行(手がかりの範囲の記述用。判定には使わない)
TRN = ROOT / "data/22_01a_rows_wt2026.npz"; TRX = None
if TRN.exists():
    if sha256(TRN) != FROZEN["rows"]: raise SystemExit("[22_04] STOP: data/22_01a_rows_wt2026.npz の SHA-256 が凍結の記録と違う")
    _d = np.load(TRN, allow_pickle=False); TRX = _d["X"][_d["fb"] == 0]
else:
    print("[22_04] 注意: data/22_01a_rows_wt2026.npz が無いので、手がかりの範囲の記述を飛ばす(判定には使わない)")
if not a.dev and (OPEN.exists() or (ROOT / "models/22_04_judgment.json").exists()):
    SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
    print(f"[22_04] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない。扱いは 22_00 の 3 節)")
print("[22_04] 照合の準備は全て通った(まだ開いていない。この後に速度・格子を作り、試験の地震の前に opened を書く)")

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
print(f"[22_04] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
      f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")

# ---------------------------------------------------------------- 4. 格子と探索(17_02 と同じ)
H = float(max(30.0, np.percentile(np.abs(np.r_[EX[CAL], EY[CAL]]), 99.5) + 30.0))
STEP = float(max(1.0, round(H / 30.0)))
ZMAX = float(max(30.0, np.percentile(SRC[CAL, 2], 99.5) * 1.3 + 10.0))
ZDEF = float(np.mean(SRC[CAL, 2]))
xc = np.arange(-H, H + 1e-6, STEP); zc = np.arange(0.0, ZMAX + 1e-6, STEP)
GX, GY, GZ = np.meshgrid(xc, xc, zc, indexing="ij"); COARSE = np.c_[GX.ravel(), GY.ravel(), GZ.ravel()]
XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
print(f"[22_04] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
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
print(f"[22_04] KDE の帯域(pool の一つ抜き): {KDE_H} km")
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
    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[22_04] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
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
    if ie is not None and ie in top: stop("[22_04] STOP: 自分自身が似た地震の上位に入っている")
    out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
               C3=locate_map(pk, top), C4=None, fb=False, top1=int(top[0]), top=top, ncorr=0)
    if with_c4:
        dP, dS = corr_from(top, pk)
        out["C4"] = locate_map(pk, top, dP, dS); out["ncorr"] = len(dP)
    return out


# >>> 22 GATE FEATURES BEGIN(この印から END までは 22_01a・22_01b・22_04 で 1 字も違わない。SHA-256 を記録し、22_02・22_04 で照合する)
# 信頼の切り替え(G)の手がかり。全て「その時点 τ までに分かること」だけで作る。目標の地震の正解(気象庁の震源・Mj)は使わない。
# 局の名前・絶対的な位置・地域に依る量も使わない(別の系列へ持って行けるように)。
GATE_FEATS = ["log1p_d_C4_C1_km", "log1p_d_C4_M6r_km", "log1p_d_C1_C2_km", "log1p_top10_spread_km", "S_max", "S_gap12",
              "log1p_n_pos", "n_P", "p_resid_C4_s", "C4_at_edge", "n_corr_C4", "tau_s", "log1p_d_C4_lib_km"]
GATE_RESID_DZ = 1.0            # 手がかり 9: 深さを 0〜ZMAX km で 1 km 刻みに調べる
GATE_RESID_MIN_P = 3           # 手がかり 9: P が 3 局未満なら値なし(nan)
GATE_THR_KM = 10.0             # 規則 R(比べる相手): C4 と C1 が 10 km 以上食い違えば C1
def gate_features(tau, pk, o, m6r, S, lib):
    """c_from の出力 o(C1 がある時だけ呼ぶ)・M6r・lib の順の S・過去の地震の一覧 lib から 13 の手がかり(GATE_FEATS の順)"""
    x4, y4 = o["C4"]; x1, y1 = o["C1"]; x2, y2 = o["C2"]; xm, ym = m6r; top = o["top"]
    Ss = np.sort(S)[::-1]
    spread = float(np.median(np.hypot(EX[top] - x2, EY[top] - y2)))
    resid = np.nan
    if len(pk) >= GATE_RESID_MIN_P:
        dP, _ = corr_from(top, pk)
        xs = np.array([p[1] for p in pk]); ys = np.array([p[2] for p in pk]); zs = np.array([p[3] for p in pk])
        tobs = np.array([p[4] for p in pk]); corr = np.array([cP.get(p[0], 0.0) + dP.get(p[0], 0.0) for p in pk])
        zg = np.arange(0.0, ZMAX + 1e-6, GATE_RESID_DZ)[:, None]
        R = np.sqrt((x4 - xs[None, :]) ** 2 + (y4 - ys[None, :]) ** 2 + (zg - zs[None, :]) ** 2)
        res = tobs[None, :] - (tt(R, zs[None, :], zg, V0, KG) + corr[None, :])
        res = res - np.median(res, axis=1, keepdims=True)
        resid = float(np.min(np.median(np.abs(res), axis=1)))
    edge = float(max(abs(x4), abs(y4)) >= H - STEP)
    dlib = float(np.min(np.hypot(EX[lib] - x4, EY[lib] - y4)))
    return np.array([np.log1p(np.hypot(x4 - x1, y4 - y1)), np.log1p(np.hypot(x4 - xm, y4 - ym)), np.log1p(np.hypot(x1 - x2, y1 - y2)),
                     np.log1p(spread), Ss[0], Ss[0] - Ss[1], np.log1p(float((S > 0).sum())), float(len(pk)), resid, edge,
                     float(o["ncorr"]), float(tau), np.log1p(dlib)], float)
# <<< 22 GATE FEATURES END
# >>> 22 GATE APPLY BEGIN(この印から END までは 22_02・22_03・22_04 で 1 字も違わない)
def gate_fit(Xtr, e1, e4, LRkw, w_cap):
    """G の学習: y = 1(C1 の誤差 < C4 の誤差)、重み min(|e4 − e1|, w_cap)。値なしは学習の行の中央値で埋め、平均と標準偏差で標準化"""
    from sklearn.linear_model import LogisticRegression
    imp = np.nanmedian(Xtr, axis=0); imp = np.where(np.isfinite(imp), imp, 0.0)
    Z = np.where(np.isfinite(Xtr), Xtr, imp[None, :])
    mu = Z.mean(0); sd = Z.std(0); sd = np.where(sd > 0, sd, 1.0)
    y = (e1 < e4).astype(int); w = np.minimum(np.abs(e4 - e1), w_cap); w = w / w.mean()          # 重みは平均 1(C の意味を単位に依らず決める)
    m = LogisticRegression(**LRkw); m.fit((Z - mu) / sd, y, sample_weight=w)
    nit = int(np.max(m.n_iter_))
    if nit >= LRkw["max_iter"]: raise SystemExit(f"[22] STOP: ロジスティック回帰が収束しない(反復 {nit})")
    return dict(imp=imp, mu=mu, sd=sd, model=m, coef=m.coef_[0].astype(float), intercept=float(m.intercept_[0]), n_iter=nit)
def gate_prob(g, Xq):
    """p(C1 の方が近い)。係数から直接計算する(sklearn の版に依らない)。C1 が無い行(手がかりが全て nan)は 0"""
    allnan = np.all(np.isnan(Xq), axis=1); bad = np.isnan(np.delete(Xq, 8, axis=1)).any(axis=1) & ~allnan
    if bad.any(): raise SystemExit(f"[22] STOP: C1 がある行で、手がかり 9 以外が値なしの行が {int(bad.sum())}(手がかりの計算を確かめる)")
    Z = np.where(np.isfinite(Xq), Xq, g["imp"][None, :])
    p = 1.0 / (1.0 + np.exp(-(((Z - g["mu"]) / g["sd"]) @ g["coef"] + g["intercept"])))
    return np.where(allnan, 0.0, p)
def gate_choose(g, Xq, e1, e4, p_choose):
    """G の答えの誤差: p ≥ p_choose なら C1、それ以外(C1 が無い行も)は C4"""
    p = gate_prob(g, Xq); c1 = (p >= p_choose) & np.isfinite(e1)
    return np.where(c1, e1, e4), c1, p
def rule_R(Xq, e1, e4, thr_km):
    """規則 R: C4 と C1 が thr_km 以上食い違えば C1(C1 が無い行は C4)"""
    d = np.expm1(Xq[:, 0]); s = np.isfinite(d) & (d >= thr_km) & np.isfinite(e1)
    return np.where(s, e1, e4), s
# <<< 22 GATE APPLY END
# ---------------------------------------------------------------- 7. 判定の決まり(22_00 の 2 節。verdict は 22_02 と 1 字も違わない)
MIN_EV, MIN_DISC, MIN_NZ, ALPHA_H, GUARD_KM, TAU_MAIN, MISS_KM, BIG_KM = 30, 8, 10, 0.005, 0.05, 2.0, 10.0, 30.0
def verdict(n_ev, n_disc, p1, nz, p2, guard_ok):
    """22_00 の 2 節の判定。評価できる地震 = その τ の全ての地震(C1 が無い地震も G = R = C4 として数える)。
    INCONCLUSIVE: 地震 30 未満か HG1 の食い違う対 8 未満。HG2 の対が 10 未満なら HG2 は成り立たないとして扱う"""
    if n_ev < MIN_EV or n_disc < MIN_DISC: return "INCONCLUSIVE"
    h1 = p1 is not None and p1 < ALPHA_H; h2 = nz >= MIN_NZ and p2 is not None and p2 < ALPHA_H
    if h1 and h2 and guard_ok: return "GATE-CONFIRMED"
    if h1 and guard_ok: return "GATE-HELPS-NOT-BEYOND-RULE"
    return "GATE-NOT-CONFIRMED"
# ---------------------------------------------------------------- 8. 開く(照合の準備は全て、重い計算の前に済ませた)
from scipy.stats import binomtest
if not a.dev:
    log_open("opened"); OPENED = True
    def _hook(t, v, tb):
        log_open((f"figure failed after the judgment was written: " if DONE else "stopped: ") + f"{t.__name__}: {str(v)[:160]}")
        sys.__excepthook__(t, v, tb)
    sys.excepthook = _hook

# ---------------------------------------------------------------- 9. 試験の地震 × 4 時点(21_20 と同じ呼び方)+ G-same + 手がかり
METH = ["M6r", "C1", "C2", "C3", "C4"]
ERR = {m: np.full((len(EVAL), len(TAUS)), np.nan) for m in METH}
LAT = {m: np.full((len(EVAL), len(TAUS)), np.nan) for m in METH}; LON = {m: np.full((len(EVAL), len(TAUS)), np.nan) for m in METH}
XF = np.full((len(EVAL), len(TAUS), len(GATE_FEATS)), np.nan); FBK = np.zeros((len(EVAL), len(TAUS)), int)
NI = np.zeros((len(EVAL), len(TAUS)), int); NPOS = np.zeros((len(EVAL), len(TAUS)), int)
t0 = time.time()
for ii, ie in enumerate(EVAL):
    lib = library(ie); p0 = FIRST[ie]; m3 = prior_members(lib, p0[0], (p0[1], p0[2]))
    for jt, t in enumerate(TAUS):
        pk = picks_of(ie, t); m6r = locate_map(pk, m3)
        S, ni = similarity(ie, t, lib, BAND)
        o = c_from(S, lib, pk, m3, m6r, TOPK, ie=ie)
        P = {"M6r": m6r, "C1": o["C1"], "C2": o["C2"], "C3": o["C3"], "C4": o["C4"]}
        for m in METH:
            if P[m] is None: continue
            la, lo = to_ll(*P[m]); LAT[m][ii, jt], LON[m][ii, jt] = la, lo; ERR[m][ii, jt] = km_between(la, lo, SRC[ie, 0], SRC[ie, 1])
        r = ref[OT[ie]]; bad = []
        for m in CHK:
            v = r[f"{m}_err_t{TL4[jt]}"]; mine = ERR[m][ii, jt]
            if (v == "") != (not np.isfinite(mine)) or (v != "" and abs(mine - float(v)) > 6e-5): bad.append((TL4[jt], m, v, f"{mine:.5f}"))
        if bad: stop(f"[22_04] STOP(G-same): {OT[ie]} で 21_20 と同じ計算になっていない(τ, 方法, CSV, ここ: {bad[:3]})。この行を貼って相談")
        FBK[ii, jt] = int(o["fb"]); NI[ii, jt] = ni; NPOS[ii, jt] = int((S > 0).sum())
        if not o["fb"]: XF[ii, jt] = gate_features(t, pk, o, m6r, S, lib)
    if (ii + 1) % 10 == 0 or ii + 1 == len(EVAL):
        el = time.time() - t0
        print(f"  … {ii + 1}/{len(EVAL)} 地震({el:.0f} s、残りの目安 {el / (ii + 1) * (len(EVAL) - ii - 1) / 60:.0f} 分)", flush=True)
print(f"[22_04] G-same({'dev の評価' if a.dev else '試験'}の地震 {len(EVAL)} 個 × 4 時点で、C1・C3・C4・M6r の誤差が 21_20 の CSV と 6e-5 km 以内): PASS")
for m in METH: ERR[m] = np.round(ERR[m], 4)          # 22_01a・21_20 の CSV と同じ小数 4 桁(同点を同点として扱う)
if not np.all(np.isfinite(ERR["C4"])): stop("[22_04] STOP: C4 の誤差が無い地震がある")

# ---------------------------------------------------------------- 10. 凍結した G を当てる・規則 R
NEV, NT = len(EVAL), len(TAUS)
Xr = XF.reshape(-1, len(GATE_FEATS)); e1 = ERR["C1"].reshape(-1); e4 = ERR["C4"].reshape(-1)
try:                                   # 判定の部分の中の STOP(手がかり 9 以外が値なし)も、開いた後の止まりとして記録する
    eG, chG, pG = gate_choose(GATE, Xr, e1, e4, GATE["p_choose"])
    eR, swR = rule_R(Xr, e1, e4, GATE["thr_R_km"])
except SystemExit as ex:
    stop(f"[22_04] STOP(判定の部分): {ex}")
EG, ERr, CHG, SWR, PG = (v.reshape(NEV, NT) for v in (eG, eR, chG, swR, pG))

# ---------------------------------------------------------------- 11. 判定(τ = 2 s)
jm = TAUS.index(TAU_MAIN)
g2, c4, r2 = EG[:, jm], ERR["C4"][:, jm], ERr[:, jm]
g10, c10 = g2 > MISS_KM, c4 > MISS_KM
b_, c_ = int(np.sum(c10 & ~g10)), int(np.sum(g10 & ~c10))
p1 = float(binomtest(c_, b_ + c_, 0.5, alternative="less").pvalue) if b_ + c_ > 0 else None
dd = g2 - r2; nz = int(np.sum(dd != 0))
p2 = (float(wilcoxon(g2, r2, alternative="less", zero_method="wilcox", method="approx", correction=False).pvalue) if nz >= 1 else None)
guard_ok = bool(np.median(g2) <= np.median(c4) + GUARD_KM)
VERDICT = verdict(NEV, b_ + c_, p1, nz, p2, guard_ok)
if a.dev: VERDICT_SHOW = f"{VERDICT}(dev: 試験ではない。評価の地震が {NEV} なので必ず INCONCLUSIVE)"
else: VERDICT_SHOW = VERDICT
def fp(p): return "—" if p is None else f"{p:.3g}"
print(f"\n[22_04] ===== 判定(τ = 2 s、{'dev の評価' if a.dev else '大阪府北部 2018 の試験'}の {NEV} 地震。C1 が無い地震 {int(FBK[:, jm].sum())} も G = R = C4 として数える) =====")
print(f"  HG1(G 対 C4、10 km 超): C4 だけ外れ {b_}・G だけ外れ {c_}(食い違う対 {b_ + c_}、基準 {MIN_DISC} 以上)  片側の正確な McNemar p = {fp(p1)}"
      f"(基準 < {ALPHA_H})")
print(f"  HG2(G 対 R、地震ごとの誤差): 差が 0 でない対 {nz}(基準 {MIN_NZ} 以上)  対の差の中央値 {np.median(dd):+.4f} km  片側の Wilcoxon p = {fp(p2)}")
print(f"  守り: 中央値 G {np.median(g2):.3f} km ≤ C4 {np.median(c4):.3f} + {GUARD_KM} km ? {'OK' if guard_ok else 'NG'}")
print(f"  10 km 超: C4 {np.mean(c10):.1%}・R {np.mean(r2 > MISS_KM):.1%}・G {np.mean(g10):.1%}   G が C1 を選ぶ {CHG[:, jm].mean():.1%}・R が C1 を選ぶ {SWR[:, jm].mean():.1%}")
print(f"  → 判定: {VERDICT_SHOW}")
# 副の仮説 HG3(22_00 の 2 節。τ = 1 s で G 対 R。主の判定には関わらず、別に報告する)
TAU_SEC = 1.0; j1 = TAUS.index(TAU_SEC)
g1s, r1s = EG[:, j1], ERr[:, j1]
dd1 = g1s - r1s; nz1 = int(np.sum(dd1 != 0))
p3 = (float(wilcoxon(g1s, r1s, alternative="less", zero_method="wilcox", method="approx", correction=False).pvalue) if nz1 >= 1 else None)
HG3 = ("INCONCLUSIVE" if (NEV < MIN_EV or nz1 < MIN_NZ) else "SUPPORTED" if (p3 is not None and p3 < ALPHA_H) else "NOT-SUPPORTED")
print(f"  副の仮説 HG3(τ = 1 s、G 対 R、地震ごとの誤差): 差が 0 でない対 {nz1}(基準 {MIN_NZ} 以上)  対の差の中央値 {np.median(dd1):+.4f} km  "
      f"片側の Wilcoxon p = {fp(p3)}(基準 < {ALPHA_H})  中央値 G {np.median(g1s):.3f}・R {np.median(r1s):.3f} km  → {HG3}(主の判定とは別)")

# ---------------------------------------------------------------- 12. 記述(判定しない)
DESC = {}
for jt, t in enumerate(TAUS):
    d = dict(n=NEV, frac_G_C1=float(CHG[:, jt].mean()), frac_R_C1=float(SWR[:, jt].mean()), n_fallback=int(FBK[:, jt].sum()))
    for k, e in (("M6r", ERR["M6r"][:, jt]), ("C4", ERR["C4"][:, jt]), ("C1", ERR["C1"][:, jt]), ("R", ERr[:, jt]), ("G", EG[:, jt])):
        f = np.isfinite(e)
        d[k] = dict(n=int(f.sum()), median_km=float(np.median(e[f])) if f.any() else None,
                    gt10=float(np.mean(e[f] > MISS_KM)) if f.any() else None, gt30=float(np.mean(e[f] > BIG_KM)) if f.any() else None)
    DESC[TL4[jt]] = d
    print(f"  [記述] τ={TL4[jt]} s  中央値 M6r {d['M6r']['median_km']:.2f} / C4 {d['C4']['median_km']:.2f} / C1 "
          + (f"{d['C1']['median_km']:.2f}" if d['C1']['median_km'] is not None else "—")
          + f" / R {d['R']['median_km']:.2f} / G {d['G']['median_km']:.2f} km   10 km 超 C4 {d['C4']['gt10']:.1%} / R {d['R']['gt10']:.1%} / "
          f"G {d['G']['gt10']:.1%}   G が C1 を選ぶ {d['frac_G_C1']:.1%}")
QD = None
if GATE.get("q_head") is not None:
    okr = ~np.all(np.isnan(Xr), axis=1)
    Zq = (np.where(np.isfinite(Xr[okr]), Xr[okr], GATE["imp"][None, :]) - GATE["mu"]) / GATE["sd"]
    q = 1.0 / (1.0 + np.exp(-(Zq @ GATE["q_head"]["coef"] + GATE["q_head"]["intercept"]))); yq = (eG[okr] > MISS_KM).astype(float)
    QD = dict(n=int(okr.sum()), brier=float(np.mean((q - yq) ** 2)), brier_base_rate=float(np.mean((GATE["q_head"]["base_rate"] - yq) ** 2)),
              base_rate_train=float(GATE["q_head"]["base_rate"]), observed_rate=float(yq.mean()))
    print(f"  [記述] 外れの確率 q: Brier {QD['brier']:.4f}(学習の基準率 {QD['base_rate_train']:.3f} だけで当てると {QD['brier_base_rate']:.4f})  "
          f"実際の 10 km 超 {QD['observed_rate']:.1%}")
RANGE = None
if TRX is not None:
    okr = ~np.all(np.isnan(Xr), axis=1); RANGE = {}
    for i, f in enumerate(GATE_FEATS):
        lo, hi = np.nanmin(TRX[:, i]), np.nanmax(TRX[:, i]); v = Xr[okr, i]; v = v[np.isfinite(v)]
        RANGE[f] = dict(train_min=float(lo), train_max=float(hi), test_min=(float(v.min()) if len(v) else None),
                        test_max=(float(v.max()) if len(v) else None), frac_outside=(float(np.mean((v < lo) | (v > hi))) if len(v) else None))
    out_f = {f: r["frac_outside"] for f, r in RANGE.items() if r["frac_outside"]}
    print("  [記述] 学習の行の範囲の外にある手がかり(行の割合): " + (", ".join(f"{f} {v:.1%}" for f, v in out_f.items()) if out_f else "なし"))

# ---------------------------------------------------------------- 13. 出力(JSON・CSV を図より先に)
with open(ROOT / f"data/22_04_per_event{SUF}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["origin_time", "mj", "lat", "lon", "depth_km", "tau", "fb", "n_i", "n_pos"] + [f"err_{m}" for m in METH]
               + ["err_R", "err_G", "p_gate", "G_chooses_C1", "R_chooses_C1"] + [f"{q}_{m}" for m in METH for q in ("lat", "lon")] + GATE_FEATS)
    for ii, ie in enumerate(EVAL):
        for jt, t in enumerate(TAUS):
            k = ii * NT + jt
            w.writerow([OT[ie], f"{MAG[ie]:.1f}", f"{SRC[ie, 0]:.4f}", f"{SRC[ie, 1]:.4f}", f"{SRC[ie, 2]:.2f}", TL4[jt], FBK[ii, jt], NI[ii, jt], NPOS[ii, jt]]
                       + ["" if not np.isfinite(ERR[m][ii, jt]) else f"{ERR[m][ii, jt]:.4f}" for m in METH]
                       + [f"{eR[k]:.4f}", f"{eG[k]:.4f}", f"{pG[k]:.6f}", int(chG[k]), int(swR[k])]
                       + ["" if not np.isfinite(v) else f"{v:.5f}" for m in METH for v in (LAT[m][ii, jt], LON[m][ii, jt])]
                       + ["" if not np.isfinite(v) else f"{v:.6g}" for v in XF[ii, jt]])
LIM = ["West Tottori 2026 training rows contain many C4 misses (tau = 2 s: 15.4% > 10 km over 467 rows with C1), mostly early in the "
       "sequence when the past-event list is short, while the 91 21_02 evaluation events had 3.3%; rule R was already strong in 2026 "
       "(0.4% > 10 km), so HG2 (G beating R) is a hard test",
       "test errors are rounded to 4 decimals (numpy round) before HG1/HG2, as were the training errors",
       "the gate G was trained on one sequence (West Tottori 2026) and frozen before Northern Osaka 2018 was opened (22_00 section 7)",
       "truth and past-event locations are JMA hypocentres; C1 can only return locations of past events, so neither C1 nor G can answer "
       "for an event in a new place",
       "rule R's 10 km threshold was chosen after seeing Central Tottori 2016 and is fixed here in advance",
       "feature 9 (P residual at the C4 epicentre) is missing with fewer than 3 P picks and is then filled with the training median",
       "C1 and C4 errors are rounded to 4 decimals before comparison (as in the 21_20 CSV) so that ties stay ties",
       "all 21_20 limitations apply (listed below, copied from 21_20 v1)"] + LIMITS
JUDG = dict(script="22_04_osaka2018_gate_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
            sequence="Northern Osaka 2018", suffix=SUF, cache=a.cache, cache_sha256=CACHE_SHA, gate_pkl_sha256=MODEL_SHA,
            gate_feature_block_sha256=GATE_SHA, gate_apply_block_sha256=APPLY_SHA, ref_csv=str(REFCSV.relative_to(ROOT)),
            ref_csv_sha256=REF_SHA, ref_judgment=str(J20P.relative_to(ROOT)), ref_suffix=("" if a.dev else a.ref_suffix),
            gate_frozen_utc=T_FREEZE, g_same="PASS", n_events=NEV, tau_main=TAU_MAIN,
            hypotheses=dict(HG1=dict(b_C4_only_miss=b_, c_G_only_miss=c_, n_discordant=b_ + c_, p=p1, alpha=ALPHA_H, min_discordant=MIN_DISC),
                            HG2=dict(n_nonzero=nz, median_diff_km=float(np.median(dd)), p=p2, alpha=ALPHA_H, min_nonzero=MIN_NZ,
                                     wilcoxon="one-sided, zero_method=wilcox, method=approx, correction=False"),
                            guard=dict(G_median_km=float(np.median(g2)), C4_median_km=float(np.median(c4)), margin_km=GUARD_KM, ok=guard_ok),
                            HG3_secondary=dict(tau_s=TAU_SEC, n_nonzero=nz1, median_diff_km=float(np.median(dd1)), p=p3, alpha=ALPHA_H,
                                               min_nonzero=MIN_NZ, G_median_km=float(np.median(g1s)), R_median_km=float(np.median(r1s)),
                                               result=HG3, note="secondary; reported separately; does not change the verdict")),
            verdict=VERDICT, secondary_HG3=HG3, verdict_rule="INCONCLUSIVE (n<30 or HG1 discordant<8) -> GATE-CONFIRMED (HG1, HG2, guard) -> "
            "GATE-HELPS-NOT-BEYOND-RULE (HG1, guard; HG2 fails if nonzero pairs<10) -> GATE-NOT-CONFIRMED",
            describe=DESC, q_calibration=QD, feature_range=RANGE, limits=LIM, numpy=np.__version__, python=platform.python_version(),
            utc=utcnow(), runtime_s=time.time() - T0)
JP = ROOT / f"models/22_04_judgment{SUF}.json"
json.dump(JUDG, open(JP, "w"), indent=1, ensure_ascii=False)
print(f"[22_04] 出力: {JP.relative_to(ROOT)}  SHA-256 {sha256(JP)}  /  data/22_04_per_event{SUF}.csv")
if not a.dev: log_open(f"completed: verdict {VERDICT}")
DONE = True

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 10, "pdf.fonttype": 42})
COL = {"M6r": "#9AA0A6", "C4": "#E040FB", "C1": "#1E88E5", "R": "#111111", "G": "#00897B"}
LAB = {"M6r": "Best physics (M6r)", "C4": "C4 (physics + similar events + station terms)",
       "C1": "C1 (most similar past event; % of events with a C1 answer)",
       "R": "Fixed rule R (switch to C1 if C4-C1 >= 10 km)", "G": "Trust gate G (frozen)"}
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.8), gridspec_kw=dict(width_ratios=[1.15, 1.0]))
ax = axs[0]; xx = np.arange(NT); wbar = 0.16
for i, k in enumerate(["M6r", "C4", "C1", "R", "G"]):
    vals = [100 * (DESC[t][k]["gt10"] or 0.0) for t in TL4]
    ax.bar(xx + (i - 2) * wbar, vals, wbar, color=COL[k], label=LAB[k], edgecolor="white", linewidth=0.5)
    for xv, v in zip(xx + (i - 2) * wbar, vals): ax.text(xv, v, f"{v:.1f}", ha="center", va="bottom", fontsize=5.5, color="0.25", rotation=90)
ax.set_xticks(xx); ax.set_xticklabels([f"{t} s" for t in TL4]); ax.margins(y=0.15)
ax.set_xlabel("Time since the first P pick, tau"); ax.set_ylabel("Events with error > 10 km (%)"); ax.grid(alpha=0.3, axis="y")
ax.set_title(f"(a) Northern Osaka 2018{' (dev)' if a.dev else ''}, {NEV} events (bar labels in %)", fontsize=9.5)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8)
ax = axs[1]
lo_ = max(1e-2, float(np.nanmin(np.r_[c4, g2])) * 0.7); hi_ = float(np.nanmax(np.r_[c4, g2])) * 1.4
ch2 = CHG[:, jm]
clip = (c4 < lo_) | (g2 < lo_)
ax.scatter(np.clip(c4[~ch2], lo_, None), np.clip(g2[~ch2], lo_, None), s=14, color=COL["C4"], alpha=0.7, label="G kept C4")
ax.scatter(np.clip(c4[ch2], lo_, None), np.clip(g2[ch2], lo_, None), s=22, color=COL["C1"], marker="^", alpha=0.9, label="G switched to C1")
if clip.any():
    ax.scatter(np.clip(c4[clip], lo_, None), np.clip(g2[clip], lo_, None), s=60, facecolors="none", edgecolors="0.2", lw=0.8,
               label=f"Error below {lo_:.2f} km drawn at the axis floor")
ax.plot([lo_, hi_], [lo_, hi_], color="0.4", lw=0.8); ax.axvline(MISS_KM, color="0.6", lw=0.6, ls=":"); ax.axhline(MISS_KM, color="0.6", lw=0.6, ls=":")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xlim(lo_, hi_); ax.set_ylim(lo_, hi_)
ax.set_xlabel("C4 error at tau = 2 s (km)"); ax.set_ylabel("Gate G error at tau = 2 s (km)"); ax.grid(alpha=0.3, which="both")
ax.set_title(f"(b) Per event at tau = 2 s. {'DEV, not a test: ' if a.dev else 'Verdict: '}{VERDICT}", fontsize=9.5)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/22_04_F1_gate_osaka{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
print(f"[22_04] 図: PDF/22_04_F1_gate_osaka{SUF}.pdf  ({time.time() - T0:.0f} s)")
print("[22_04] 次: この出力と図を貼る" + ("" if a.dev else "(判定に使うのは、この最初の本番の結果)"))
