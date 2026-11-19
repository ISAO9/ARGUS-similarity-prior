#!/usr/bin/env python3
# =============================================================================
# Script : 21_20f_osaka2018_learned_test.py  (v1)
#          [学習型 ARGUS の 3 つ目の系列での試験: 鳥取 2026 で学習して凍結した「似た地震の選び方」(21_06a のモデル)を、学び直さずに、
#           手を付けていない大阪府北部 2018 で 1 回だけ試す。位置は C3・C4 と同じ物理の計算で決める(AI は物理の部品)]
# Project: ARGUS(新生)— 学習した部品が 3 つ目の余震系列でも物理だけより良いか
# 派生元 : 21_06b_ct2016_learned_test.py v1(SHA-256 442c411945f288cfff7f14490ee9826ffcfe055e5a79cc2af0c39fe93cb5bfea)。
#
# なぜ編集が要ったか: 21_06b v1 の引数は --cache・--dev・--train-json だけで、本震の時刻・G-untouched の期間・比べる相手の 21_04 の
#   出力の名前(data/21_04_per_event.csv・models/21_04_judgment.json・models/21_04_opened.json)・自分の出力の名前
#   (models/21_06b_*.json など)がスクリプトに書き込まれている。そのまま回すと大阪のキャッシュで STOP するか、21_06b の記録を壊す。
#
# 21_06b v1 から変えたこと(これ以外は 1 字も変えていない。DIFF_LOG.md):
#   1. 入力の既定のキャッシュ: data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt(21_20 と同じもの)。
#   2. MAIN_UTC・UNTOUCHED_UTC を 21_20 と同じ値にした(2018-06-17 22:58:30 UTC ± 60 s。秒までの発生時刻ではない。21_20 の冒頭を見る)。
#   3. 比べる相手と順番の確かめを 21_04 の出力から 21_20 の出力に変えた: data/21_20_per_event.csv(--dev は _dev)、
#      models/21_20_judgment.json(最初の本番で、キャッシュの SHA-256 が同じこと)、models/21_20_opened.json(21_06a の学習が先か)。
#   4. 出力の名前: models/21_20f_judgment.json / models/21_20f_opened.json / data/21_20f_per_event.csv / PDF/21_20f_F1_learned_test.pdf
#      (--dev では _dev、2 回目以降は _rerun_<UTC の時刻>)。表示の [21_20f]。
#   5. 限界の文・表示・図の題の系列の名前を大阪府北部 2018 にした。記述用の L3p・L4p は「2026 の学習の行 + 2018 の pool の行」で学び直す
#      (21_06b と同じ作り方。判定には使わない)。
#   変えていないもの: 21_06 FEATURES の印の間(1 字も変えない。G-feat で学習の記録 models/21_06a_train.json の
#   feature_block_sha256 = 9905420e546d… と照合する)、凍結したモデル models/21_06_ranker.pkl(学び直さない)、学習の記録、
#   G-model(scikit-learn・numpy の版が学習時と同じでなければ STOP。学習した Mac の ~/SWIFT の環境で回す)、仮説と判定の規則。
#
# 事前登録の仮説と判定(21_06 と同じ。事前登録の記録 21_20 に再掲):
#   HL1(主)  L4 @ τ = 2 s が BEST より良い、p < 0.01、BEST ≥ 0.5 km  → LEARNED-CONFIRMED / PHYSICS-AT-FLOOR / NOT-CONFIRMED
#   HL2(副)  L4 @ τ = 2 s が C4 より良い、p < 0.005
#   HL3(副)  L3 @ τ = 0.5 s が BEST より良い、p < 0.005、BEST ≥ 0.5 km
#   評価できる試験の地震が 30 未満なら INCONCLUSIVE。それ以外は記述だけ。
#
# Usage : (21_20 の本番が終わってから)
#         cd ~/SWIFT && caffeinate -i uv run python src/21_20f_osaka2018_learned_test.py --dev   (動作確認。21_20 の dev の CSV が要る)
#         cd ~/SWIFT && caffeinate -i uv run python src/21_20f_osaka2018_learned_test.py         (本番。1 回だけ)
# 入力  : 21_20 と同じキャッシュ、data/21_20_per_event.csv と models/21_20_judgment.json・models/21_20_opened.json(--dev なら _dev の CSV)、
#         models/21_06a_train.json・models/21_06_ranker.pkl・data/21_06a_train_rows.npz(21_06a の出力。凍結 B のまま)
# Output: models/21_20f_judgment.json / models/21_20f_opened.json / data/21_20f_per_event.csv / PDF/21_20f_F1_learned_test.pdf
# 止める条件(STOP): 21_06b と同じもの(21_20 と同じ入力のゲート・G-feat・G-model・21_20 の CSV が無いか地震が合わない・キャッシュが 21_20 と違う・G-same)
# 所要  : 参考: 21_06b の本番は試験 307 地震で 506 s(models/21_06b_judgment.json の runtime_s)
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
ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(21_20 の dev と同じ 20 地震。比べる相手は data/21_20_per_event_dev.csv)")
ap.add_argument("--train-json", default="models/21_06a_train.json", help="21_06a の学習の記録(凍結したモデルの SHA-256 を持つ)")
a = ap.parse_args()

# ---------------------------------------------------------------- 事前に固定した値(変えたら版を上げる)
VERSION = "v1"
FS, IP, NTS = 100.0, 300, 2048
TAUS = [0.5, 1.0, 2.0, 3.0]
ALPHA_L1, ALPHA_L23 = 0.01, 0.005          # 21_20f: HL1(L4 @ 2 s 対 BEST)は 0.01、HL2(L4 @ 2 s 対 C4)・HL3(L3 @ 0.5 s 対 BEST)は 0.005
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
MAIN_UTC = dt.datetime(2018, 6, 17, 22, 58, 30)   # 21_20 と同じ: 気象庁の発表の 07:58 JST の 1 分の真ん中(秒までの値ではない。±60 s でこの 1 分を含む)。要確認
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
          "the JMA frame rather than better early information",
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
print(f"[21_20f] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
      f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")

# ---------------------------------------------------------------- 1. 入力
CP = ROOT / a.cache
if not CP.exists(): raise SystemExit(f"[21_20f] STOP: {a.cache} が無い(ノート 21_20_osaka2018_colab.ipynb のセル 11 で作った tottori_parsed_realpick_osaka2018_m15.pt を data/osaka2018_processed/ に置く)")
EVS = torch.load(CP, map_location="cpu", weights_only=False)
need = ["origin_time", "src_loc", "mw", "waveforms", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
for e in EVS:
    miss = [k for k in need if k not in e]
    if miss: raise SystemExit(f"[21_20f] STOP: キャッシュの地震に {miss} が無い(21_20c の出力か確かめる)")
for e in EVS:
    w_ = np.asarray(e["waveforms"])
    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_20f] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_20f] STOP: {e['origin_time']} の波形に NaN か無限大")
def to_ns(o):
    import pandas as pd
    try:
        t = pd.Timestamp(str(o).replace("Z", "+00:00"))
        t = t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t
        return int(t.value)
    except Exception:
        raise SystemExit(f"[21_20f] STOP: origin_time {o!r} を時刻として読めない")
OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
order = np.argsort(OTNS, kind="stable"); EVS = [EVS[i] for i in order]; OTNS = OTNS[order]
NE = len(EVS)
SRC = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS])
MAG = np.array([float(e["mw"]) for e in EVS])
OT = [str(e["origin_time"]) for e in EVS]
if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
    raise SystemExit("[21_20f] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[21_20f] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
# G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
lo_ns = int(np.datetime64(UNTOUCHED_UTC[0], "ns").astype(np.int64)); hi_ns = int(np.datetime64(UNTOUCHED_UTC[1], "ns").astype(np.int64))
n_out = int(np.sum((OTNS < lo_ns) | (OTNS > hi_ns))); n_big = int(np.sum(MAG >= 6.0 - 1e-6))
FRESH = MAG < FRESH_MAX_MAG - 1e-6
CACHE_SHA = sha256(CP)
n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
print(f"[21_20f] 入力: 大阪府北部 2018 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
      f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
print(f"[21_20f] G-untouched: 期間 2018-06-15〜2018-07-12(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
      + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
if n_out != 0 or n_big != 1: raise SystemExit("[21_20f] STOP(G-untouched): 大阪府北部 2018 のキャッシュに見えない(この行を貼って相談)")
im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
    raise SystemExit(f"[21_20f] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2018-06-17 22:58 UTC の 1 分 ± 60 s。気象庁の発表の 07:58 JST)")
CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
pool_idx = np.where(OTNS <= CUT_NS)[0]; test_idx = np.where((OTNS > CUT_NS) & FRESH)[0]
if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
    raise SystemExit("[21_20f] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
print(f"[21_20f] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
print(f"[21_20f] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
      f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")

# ---------------------------------------------------------------- 2. 座標・検測(17_02 と同じ)
TFIRST = np.full(NE, np.nan)          # PhaseNet で測った最も早い P(気象庁の発生時刻からの s)
skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
for ie, e in enumerate(EVS):
    n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    ok = np.isfinite(tp) & (pf == 0)
    if ok.any(): TFIRST[ie] = float(tp[ok].min())
    kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
    if len(set(kk)) != n: raise SystemExit(f"[21_20f] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
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
print(f"[21_20f] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
if len(EVAL) == 0: raise SystemExit("[21_20f] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
if a.dev: print(f"[21_20f] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                "(較正にも入っているので値は楽観的)")

# ---------------------------------------------------------------- 1 回だけの記録(本番は、試験の地震の結果を計算する前に書く)
OPEN = ROOT / "models/21_20f_opened.json"
SUF = "_dev" if a.dev else ""
def log_open(status):
    rec = json.load(open(OPEN)) if OPEN.exists() else []
    rec.append(dict(utc=utcnow(), status=status, version=VERSION, script_sha256=SELF_SHA, cache_sha256=CACHE_SHA, suffix=SUF))
    json.dump(rec, open(OPEN, "w"), indent=1)
if not a.dev:
    if OPEN.exists() or (ROOT / "models/21_20f_judgment.json").exists():
        SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
        print(f"[21_20f] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
OPENED = False                           # 21_20f: 試験を開くのは、学習の記録・モデル・21_20 の結果の確認が全て通った後(8. の最後)
def stop(msg):
    if not a.dev and OPENED: log_open("stopped: " + msg[:160])
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
print(f"[21_20f] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
      f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")

# ---------------------------------------------------------------- 4. 格子と探索(17_02 と同じ)
H = float(max(30.0, np.percentile(np.abs(np.r_[EX[CAL], EY[CAL]]), 99.5) + 30.0))
STEP = float(max(1.0, round(H / 30.0)))
ZMAX = float(max(30.0, np.percentile(SRC[CAL, 2], 99.5) * 1.3 + 10.0))
ZDEF = float(np.mean(SRC[CAL, 2]))
xc = np.arange(-H, H + 1e-6, STEP); zc = np.arange(0.0, ZMAX + 1e-6, STEP)
GX, GY, GZ = np.meshgrid(xc, xc, zc, indexing="ij"); COARSE = np.c_[GX.ravel(), GY.ravel(), GZ.ravel()]
XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
print(f"[21_20f] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
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
print(f"[21_20f] KDE の帯域(pool の一つ抜き): {KDE_H} km")
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
    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_20f] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
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
    if ie is not None and ie in top: stop("[21_20f] STOP: 自分自身が似た地震の上位に入っている")
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

# ---------------------------------------------------------------- 8. 凍結したモデルと 21_20 の結果の読み込み
import pickle
try:
    import sklearn
    from sklearn.ensemble import HistGradientBoostingRegressor
except ImportError:
    stop("[21_20f] STOP: scikit-learn が無い(21_06a と同じ環境で回す)")
TJP = ROOT / a.train_json
if not TJP.exists(): stop(f"[21_20f] STOP: 学習の記録 {a.train_json} が無い(先に 21_06a)")
TJ = json.load(open(TJP))
if not a.dev and (a.train_json != "models/21_06a_train.json" or TJ.get("mode") != "train" or TJ.get("suffix", "") != ""):
    stop("[21_20f] STOP: 本番は、事前登録した 21_06a の最初の本番の学習(models/21_06a_train.json、mode train)でしか回さない")
FB = open(Path(__file__), encoding="utf-8").read()
FEAT_SHA = hashlib.sha256(FB[FB.index("# >>> 21_06 FEATURES BEGIN"):FB.index("# <<< 21_06 FEATURES END")].encode()).hexdigest()
if TJ["feature_block_sha256"] != FEAT_SHA: stop("[21_20f] STOP(G-feat): 特徴量の部分が 21_06a と 1 字でも違う(学習と試験で同じ計算になっていない)")
MP = ROOT / TJ["model_path"]
if not MP.exists() or sha256(MP) != TJ["model_sha256"]: stop(f"[21_20f] STOP(G-model): モデル {TJ['model_path']} が無いか、SHA-256 が学習の記録と違う")
if TJ["sklearn"] != sklearn.__version__: stop(f"[21_20f] STOP: scikit-learn の版が学習時({TJ['sklearn']})と違う({sklearn.__version__})")
if TJ["feats"] != FEATS or TJ["hgb"] != HGB or TJ.get("block_consts") != json.loads(json.dumps(BLOCK_CONSTS)) or TJ.get("cond_min") != COND_MIN:
    stop("[21_20f] STOP: 特徴量の名前・設定・特徴量が使う定数が学習の記録と違う")
if TJ["numpy"] != np.__version__: stop(f"[21_20f] STOP: numpy の版が学習時({TJ['numpy']})と違う({np.__version__})")
with open(MP, "rb") as f: MODEL = pickle.load(f)
RP = ROOT / TJ["train_rows_path"]
if not RP.exists() or sha256(RP) != TJ["train_rows_sha256"]: stop(f"[21_20f] STOP: 学習の行 {RP.relative_to(ROOT)} が無いか SHA-256 が違う")
print(f"[21_20f] 凍結したモデル: {TJ['model_path']} SHA-256 {TJ['model_sha256'][:12]}…(2026 の {TJ['n_train_events']} 地震で学習)  "
      f"特徴量の部分 {FEAT_SHA[:12]}… G-feat PASS  G-model PASS")
TJ_SHA = sha256(TJP)
REFCSV = ROOT / ("data/21_20_per_event_dev.csv" if a.dev else "data/21_20_per_event.csv")
if not REFCSV.exists(): stop(f"[21_20f] STOP: {REFCSV.relative_to(ROOT)} が無い(先に 21_20 を回す。21_20f は 21_20 の後)")
ref = {r["origin_time"]: r for r in csv.DictReader(open(REFCSV))}
if sorted(ref) != sorted(OT[ie] for ie in EVAL):
    stop(f"[21_20f] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
J04 = ROOT / "models/21_20_judgment.json"
if J04.exists() and not a.dev:
    j4 = json.load(open(J04))
    if j4.get("mode") != "test" or j4.get("suffix") != "": stop("[21_20f] STOP: models/21_20_judgment.json が 21_20 の最初の本番の結果でない")
    if j4.get("cache_sha256") != CACHE_SHA: stop("[21_20f] STOP: キャッシュの SHA-256 が 21_20 の本番と違う")
    print("[21_20f] キャッシュの SHA-256 は 21_20 の本番と同じ")
    O4 = ROOT / "models/21_20_opened.json"
    t4 = json.load(open(O4))[0]["utc"] if O4.exists() else None
    print(f"[21_20f] 順番の確認: 21_06a の学習 {TJ.get('utc')} / 21_20 の本番を開いた時刻 {t4}(学習が先のはず。事前登録の push の時刻とも照らす)")
    if t4 is not None and TJ.get("utc") is not None and TJ["utc"] > t4: stop("[21_20f] STOP: 21_06a の学習が 21_20 の本番より後(事前登録の順番と違う)")
elif not a.dev:
    stop("[21_20f] STOP: models/21_20_judgment.json が無い(21_20 の本番を先に終える)")
REF_SHA = sha256(REFCSV)
print(f"[21_20f] SHA-256(事前登録の記録の 6 節と照らす): 学習の記録 {TJ_SHA} / モデル {TJ['model_sha256']} / 学習の行 {TJ['train_rows_sha256']} / 21_20 の CSV {REF_SHA}")
if not a.dev:                                 # 入力の確認が全て通ってから試験を開く(ここより前の STOP は記録しない)
    log_open("opened"); OPENED = True
    log_open(f"inputs: train_json {TJ_SHA} model {TJ['model_sha256']} rows {TJ['train_rows_sha256']} ref_csv {REF_SHA}")
    import sys
    def _hook(t, v, tb):
        log_open(f"stopped: {t.__name__}: {str(v)[:160]}"); sys.__excepthook__(t, v, tb)
    sys.excepthook = _hook               # 途中の例外も「止まった」と記録する(stop() は自分で記録する)
ALLP = np.where(HASP)[0]
bank = Bank(BAND, ALLP); bank2 = Bank(BAND_SENS, ALLP)
TPT = tp_table()

# ---------------------------------------------------------------- 9. 記述用: 2018 の pool を足して学び直した版(L3p・L4p。同じ設定。判定には使わない)
EVSET = set(int(i) for i in EVAL)
def dist_km(ie, J): return np.array([km_between(SRC[ie, 0], SRC[ie, 1], SRC[j, 0], SRC[j, 1]) for j in J])
Xp, yp, wp = [], [], []
for ie in pool_idx:
    if not HASP[ie] or int(ie) in EVSET: continue
    lib = library(ie)
    if len(lib) == 0: continue
    for t in TAUS:
        J, F, S, ni = pair_features(ie, t, lib, bank, bank2, TPT)
        if len(J): Xp.append(F); yp.append(np.log(dist_km(ie, J) + LABEL_EPS_KM)); wp.append(np.full(len(J), 1.0 / len(J)))
R26 = np.load(RP)
MODEL_P = HistGradientBoostingRegressor(**HGB)
MODEL_P.fit(np.concatenate([R26["X"]] + Xp), np.concatenate([R26["y"]] + yp), sample_weight=np.concatenate([R26["w"]] + wp))
print(f"[21_20f] 記述用の L3p・L4p: 2026 の行 {len(R26['y'])} + 2018 の pool の行 {int(sum(len(v) for v in yp))} で学び直した")

# ---------------------------------------------------------------- 10. 評価の地震(C3・C4 を出して 21_20 と同じか確かめ、L3・L4 を出す)
TL4 = [f"{t:g}" for t in TAUS]
BASE = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]
KEYS = ["C3", "C4", "L3", "L4", "L3p", "L4p"]
E = {k: np.full((len(EVAL), len(TAUS)), np.nan) for k in KEYS + ["TOPD_C", "TOPD_L", "LFB", "NST"]}
mism = []
for ii, ie in enumerate(EVAL):
    try:
        lib = library(ie); p0 = FIRST[ie]; m3 = prior_members(lib, p0[0], (p0[1], p0[2]))
        for jt, t in enumerate(TAUS):
            pk = picks_of(ie, t); m6r = locate_map(pk, m3)
            J, F, S, ni = pair_features(ie, t, lib, bank, bank2, TPT)
            o = c_from(S, lib, pk, m3, m6r, TOPK, ie=ie)
            topL = learned_top(MODEL, J, F); L3, L4, _ = l_from(topL, pk, m6r)
            topP = learned_top(MODEL_P, J, F); L3p, L4p, _ = l_from(topP, pk, m6r)
            for k, pxy in (("C3", o["C3"]), ("C4", o["C4"]), ("L3", L3), ("L4", L4), ("L3p", L3p), ("L4p", L4p)):
                la, lo = to_ll(*pxy); E[k][ii, jt] = km_between(la, lo, SRC[ie, 0], SRC[ie, 1])
            if o["top"] is not None: E["TOPD_C"][ii, jt] = np.median(dist_km(ie, o["top"]))
            if topL is not None: E["TOPD_L"][ii, jt] = np.median(dist_km(ie, topL))
            E["LFB"][ii, jt] = float(topL is None); E["NST"][ii, jt] = len(pk)
            r = ref[OT[ie]]; tl = TL4[jt]
            if (abs(E["C3"][ii, jt] - float(r[f"C3_err_t{tl}"])) > 6e-5 or abs(E["C4"][ii, jt] - float(r[f"C4_err_t{tl}"])) > 6e-5
                    or int(r[f"n_i_t{tl}"]) != ni or int(r[f"c3_fallback_t{tl}"]) != int(o["fb"]) or int(r[f"c4_n_corrected_t{tl}"]) != o["ncorr"]):
                mism.append((OT[ie], tl))
    except SystemExit:
        raise
    except BaseException as ex:
        stop(f"[21_20f] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
    if (ii + 1) % 10 == 0: print(f"  … {ii + 1}/{len(EVAL)}  ({time.time() - T0:.0f} s)")
for k in KEYS:                                # 21_20 の CSV(小数 4 桁)と同じ丸めにそろえてから比べる(同点を同点として扱う)
    E[k] = np.vectorize(lambda v: float(f"{v:.4f}"))(E[k])
G_SAME = "PASS" if not mism else f"FAIL ({len(mism)})"
print(f"[21_20f] G-same(ここで計算した C3・C4 が 21_20 の CSV と同じ): {G_SAME}")
if mism: stop(f"[21_20f] STOP(G-same): 21_20 と同じ計算になっていない(例 {mism[:3]})")
for b in BASE:
    E[b] = np.array([[float(ref[OT[ie]][f"{b}_err_t{tl}"]) if ref[OT[ie]][f"{b}_err_t{tl}"] != "" else np.nan for tl in TL4] for ie in EVAL])

# ---------------------------------------------------------------- 11. 判定(事前登録の規則。21_02 と同じ形)
NT = len(EVAL)
RNG_BOOT = np.random.default_rng(SEED)
def med_ci(x):
    x = x[np.isfinite(x)]
    if len(x) == 0: return (None, None, None)
    bs = np.median(x[RNG_BOOT.integers(0, len(x), (NBOOT, len(x)))], axis=1)
    return (float(np.median(x)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5)))
def paired(x, y):
    m = np.isfinite(x) & np.isfinite(y); nz = int(np.sum(x[m] != y[m]))
    d = dict(n=int(m.sum()), n_nonzero=nz, p=None, median_diff_km=None, frac_better=None)
    if m.any(): d.update(median_diff_km=float(np.median(x[m] - y[m])), frac_better=float(np.mean(x[m] < y[m])))
    if nz >= 6: d["p"] = float(wilcoxon(x[m], y[m], alternative="less", zero_method="wilcox").pvalue)
    return d
def best_of(jt):
    full = [b for b in BASE if np.all(np.isfinite(E[b][:, jt]))]
    return min(full, key=lambda b: np.median(E[b][:, jt]))
def judge(meth, tl, alpha, vs="BEST"):
    jt = TL4.index(tl); comp = best_of(jt) if vs == "BEST" else vs
    cm, bm = float(np.median(E[meth][:, jt])), float(np.median(E[comp][:, jt]))
    pr = paired(E[meth][:, jt], E[comp][:, jt]); floor = (vs == "BEST") and bm < FLOOR_KM
    win = (not floor) and cm < bm and pr["p"] is not None and pr["p"] < alpha and pr["n_nonzero"] >= MIN_NONZERO
    return dict(method=meth, tau=tl, alpha=alpha, comparator=comp, comparator_median_km=bm, median_km=cm, paired=pr, floor=bool(floor), win=bool(win))
HYP = {"HL1": judge("L4", "2", ALPHA_L1), "HL2": judge("L4", "2", ALPHA_L23, vs="C4"), "HL3": judge("L3", "0.5", ALPHA_L23)}
h1 = HYP["HL1"]
VERDICT = ("INCONCLUSIVE" if NT < MIN_TEST else "LEARNED-CONFIRMED" if h1["win"] else "PHYSICS-AT-FLOOR" if h1["floor"] else "NOT-CONFIRMED")
if a.dev: VERDICT = "DEV (no verdict)"
SUMM = {k: {tl: dict(zip(("median_km", "ci_lo", "ci_hi"), med_ci(E[k][:, jt]))) for jt, tl in enumerate(TL4)} for k in KEYS + BASE}
PER_TAU = {tl: dict(best=best_of(jt), L4_vs_best=paired(E["L4"][:, jt], E[best_of(jt)][:, jt]), L3_vs_best=paired(E["L3"][:, jt], E[best_of(jt)][:, jt]),
                    L4_vs_C4=paired(E["L4"][:, jt], E["C4"][:, jt]), L3_vs_C3=paired(E["L3"][:, jt], E["C3"][:, jt]),
                    L4p_vs_L4=paired(E["L4p"][:, jt], E["L4"][:, jt]), learned_fallback_frac=float(np.mean(E["LFB"][:, jt])),
                    top10_true_dist_median_km=dict(C=float(np.nanmedian(E["TOPD_C"][:, jt])) if np.isfinite(E["TOPD_C"][:, jt]).any() else None,
                                                   L=float(np.nanmedian(E["TOPD_L"][:, jt])) if np.isfinite(E["TOPD_L"][:, jt]).any() else None),
                    stations_median=float(np.median(E["NST"][:, jt]))) for jt, tl in enumerate(TL4)}
def f2(v): return "—" if v is None else f"{v:.2f}"
def fp(p): return "—" if p is None else f"{p:.2g}"
print(f"\n[21_20f] ===== 水平誤差の中央値 km [95% 区間](大阪府北部 2018、評価 {NT} 地震{'、dev' if a.dev else ''}) =====")
for k in ["BEST"] + KEYS:
    cells = []
    for jt, tl in enumerate(TL4):
        kk = best_of(jt) if k == "BEST" else k; s_ = SUMM[kk][tl]
        cells.append(f"{f2(s_['median_km'])} [{f2(s_['ci_lo'])},{f2(s_['ci_hi'])}]" + (f" {kk}" if k == "BEST" else ""))
    print(f"  {k:<5}" + "".join(c.rjust(28) for c in cells))
for tl, d in PER_TAU.items():
    print(f"  τ={tl:>3} s(局 {d['stations_median']:.0f}): p(L4<BEST) {fp(d['L4_vs_best']['p'])}  p(L4<C4) {fp(d['L4_vs_C4']['p'])}  p(L3<C3) {fp(d['L3_vs_C3']['p'])}  "
          f"上位 10 の本当の距離の中央値 C {f2(d['top10_true_dist_median_km']['C'])} / L {f2(d['top10_true_dist_median_km']['L'])} km  "
          f"L が M6r に戻った割合 {d['learned_fallback_frac']:.2f}")
print(f"\n[21_20f] ===== 事前登録の判定 =====")
for name, h in HYP.items():
    pr = h["paired"]
    print(f"  {name}{'(主)' if name == 'HL1' else '(副)'}: {h['method']} @ τ = {h['tau']} s  {h['median_km']:.2f} km 対 {h['comparator']} {h['comparator_median_km']:.2f} km  "
          f"p = {fp(pr['p'])}(基準 {h['alpha']})  差が 0 でない組 {pr['n_nonzero']}  FLOOR={h['floor']}  → {'勝ち' if h['win'] else '勝ちなし'}")
print(f"\n[21_20f] 判定(事前登録、HL1): {VERDICT}")
LIMITS_L = ["third sequence: Northern Osaka 2018 (mainshock 2018-06-18, 07:58 JST; JMA catalogue values), never used in ARGUS development; HL1-HL3 and "
            "the learned ranker were fixed in the 21_06 preregistration and frozen by 21_06a on West Tottori 2026 before this test"] + \
           [l for l in LIMITS[1:] if not l.startswith("H1 (C3")] + ["the double-difference offset is a horizontal straight-ray approximation "
            "(depth not solved); it is missing (nan) with fewer than 4 common stations or a near-linear station geometry", "the learned ranker (21_06a) was trained on West Tottori 2026 only and frozen before this test; L3p/L4p (retrained with the "
                     "2018 pool) are descriptive", "21_20f reuses the 21_20 per-event CSV for the physics-only methods and C3/C4, and "
                     "recomputes C3/C4 to check identity (G-same)", "C3/C4/L3/L4 errors are rounded to 4 decimals (as in the 21_20 CSV) "
                     "before comparison so that ties stay ties", "log10_dt_h uses the target's JMA origin time (not known exactly at tau; "
                     "the error is a few seconds against >= 1 h)"]
print("[21_20f] 限界: " + " / ".join(LIMITS_L))

# ---------------------------------------------------------------- 12. 出力(JSON・CSV を図より先に)
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
with open(ROOT / f"data/21_20f_per_event{SUF}.csv", "w", newline="") as f:
    w = csv.writer(f)
    cols = KEYS + ["TOPD_C", "TOPD_L", "LFB"]
    w.writerow(["origin_time", "mj"] + [f"{k}_t{tl}" for k in cols for tl in TL4])
    for i, ie in enumerate(EVAL):
        w.writerow([OT[ie], f"{MAG[ie]:.1f}"] + [("" if not np.isfinite(E[k][i, jt]) else f"{E[k][i, jt]:.4f}") for k in cols for jt in range(len(TAUS))])
out = dict(script="21_20f_osaka2018_learned_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"), suffix=SUF,
           cache=a.cache, cache_sha256=CACHE_SHA, reference_csv=str(REFCSV.relative_to(ROOT)), train_json=a.train_json,
           model_sha256=TJ["model_sha256"], train_json_sha256=TJ_SHA, train_rows_sha256=TJ["train_rows_sha256"], reference_csv_sha256=REF_SHA,
           feature_block_sha256=FEAT_SHA, n_evaluated=NT, g_same=G_SAME, summary=SUMM, per_tau=PER_TAU,
           hypotheses=HYP, verdict=VERDICT,
           verdict_rule="BEST(tau) = smallest median among the 9 AI-free methods with an estimate for every evaluated event (from the 21_20 CSV). "
                        "HL1 (primary): L4 at tau = 2 s vs BEST, alpha 0.01; HL2: L4 at 2 s vs C4, alpha 0.005; HL3: L3 at 0.5 s vs BEST, "
                        "alpha 0.005. Win = method median < comparator median, one-sided paired Wilcoxon (zero_method='wilcox') p < alpha, "
                        ">= 10 non-zero pairs, and (vs BEST only) BEST >= 0.5 km. Verdict from HL1: LEARNED-CONFIRMED / PHYSICS-AT-FLOOR / "
                        "NOT-CONFIRMED; INCONCLUSIVE if fewer than 30 evaluated events",
           limits=LIMITS_L, runtime_s=time.time() - T0)
json.dump(clean(out), open(ROOT / f"models/21_20f_judgment{SUF}.json", "w"), indent=1)

# ---------------------------------------------------------------- 13. 図(白背景・英語・凡例は枠外)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 10, "pdf.fonttype": 42})
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.4))
ax = axs[0]; x = np.array(TAUS)
sty = [("BEST", "Best physics-only method", "0.4", "s-"), ("C3", "C3 (similarity prior)", "tab:orange", "o--"), ("C4", "C4 (C3 + path terms)", "tab:red", "o-"),
       ("L3", "L3 (learned selection)", "tab:cyan", "^--"), ("L4", "L4 (L3 + path terms)", "tab:blue", "^-")]
for k, lab, c, mk_ in sty:
    md = [SUMM[best_of(jt) if k == "BEST" else k][tl] for jt, tl in enumerate(TL4)]
    ax.errorbar(x + 0.03 * (sty.index((k, lab, c, mk_)) - 2), [m["median_km"] for m in md],
                yerr=[[m["median_km"] - m["ci_lo"] for m in md], [m["ci_hi"] - m["median_km"] for m in md]], fmt=mk_, color=c, capsize=2, label=lab)
ax.set_xticks(x); ax.set_yscale("log"); ax.set_xlabel("Time since the first P pick, tau (s)"); ax.set_ylabel("Median epicentral error (km), 95% bootstrap CI")
ax.set_title(f"(a) Northern Osaka 2018, {NT} {'DEV' if a.dev else 'test'} events", fontsize=10); ax.grid(alpha=0.3)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, frameon=False, fontsize=8.5)
ax = axs[1]; jt = TL4.index("2"); bb = best_of(jt)
lo_ = max(min(np.nanmin(E["L4"][:, jt]), np.nanmin(E[bb][:, jt]), np.nanmin(E["C4"][:, jt])), 0.01)
hi_ = max(np.nanmax(E["L4"][:, jt]), np.nanmax(E[bb][:, jt]), np.nanmax(E["C4"][:, jt])) * 1.2
ax.text(0.02, 0.98, "values below 0.01 km drawn at 0.01 km", transform=ax.transAxes, va="top", fontsize=8)
ax.scatter(np.maximum(E[bb][:, jt], 0.01), np.maximum(E["L4"][:, jt], 0.01), s=14, color="tab:blue", alpha=0.7, label=f"L4 vs {bb} (best physics)")
ax.scatter(np.maximum(E["C4"][:, jt], 0.01), np.maximum(E["L4"][:, jt], 0.01), s=14, color="tab:red", marker="x", alpha=0.7, label="L4 vs C4")
ax.plot([lo_, hi_], [lo_, hi_], "k-", lw=0.8); ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("Comparator error at tau = 2 s (km)"); ax.set_ylabel("L4 error at tau = 2 s (km)")
ax.set_title(f"(b) Per event; below the line = L4 better. Verdict: {VERDICT}", fontsize=10); ax.grid(alpha=0.3, which="both")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8.5)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_20f_F1_learned_test{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
if not a.dev: log_open(f"completed: {VERDICT}")
print(f"[21_20f] 出力: models/21_20f_judgment{SUF}.json, data/21_20f_per_event{SUF}.csv, PDF/21_20f_F1_learned_test{SUF}.pdf  ({time.time() - T0:.0f} s)")
