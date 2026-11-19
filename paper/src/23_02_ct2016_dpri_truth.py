#!/usr/bin/env python3
# =============================================================================
# Script : 23_02_ct2016_dpri_truth.py  (v3)
#          [読むだけの記述: 鳥取県中部 2016 の試験(21_04)のうち 2016 年 11 月の地震を、気象庁と独立した正解
#           (京大防災研の臨時稠密観測による余震の震源一覧 ct3_201711.txt)でも採点する。あわせて両者の位置の系統的なずれを測る]
# Project: ARGUS(新生)— 23_01 で「C4 は記憶に共通するずれをほぼそのまま受け継ぐ」と分かった。その「共通のずれ」が
#          実際にどれだけあるかを、別の観測網の震源で確かめる。21_04 の判定・規則・キャッシュは一切変えない。全て記述。
#
# 何をするか(値は下の「事前に固定した値」。この版の SHA-256 と値を、計算の前に models/23_02_plan.json に書く):
#   0. 21_04 v1 と同じ計算(1〜6 節は 21_04 v1 の写し。23_01 と同じく記憶の位置だけを引数にした)。
#   1. 防災研の一覧を読む(見出しなし・1 行 10 列: 年 2 桁・月・日・時・分・秒・緯度・経度・深さ・規模。秒は「分」からの秒で
#      60 を超えうる。日本時間として読み、9 時間引いて UTC にする)。粗い照合(±2 s・5 km)で発生時刻の差の中央値 Δt0 を決め、
#      厳しい照合(|Δt − Δt0| < 0.5 s・震央の間 < 3 km・1 対 1)でキャッシュの地震と結ぶ。
#   2. 防災研 − 気象庁 の震央のずれ(東・北の中央値と 95% 区間、ずれを引いた残り、深さ、発生時刻)を、試験以外の照合した地震で
#      決める(試験の地震の値は記述として並べるだけ)。
#   3. 照合できた試験の地震を、τ = 0.5・1・2・3 s で M5・M6r・C1・C3・C4 で決め、正解 = 気象庁 と 正解 = 防災研 の両方で採点する。
#      記憶の枠は 3 つ: jma(21_04 と同じ)・jma_shift(全ての過去の地震を 2 のずれだけ動かす)・
#      dpri(照合できた過去の地震は防災研の位置、それ以外は 気象庁 + 2 のずれ)。記憶 = jma は 21_04 の値と地震ごとに比べ、
#      差が 2e-4 km を超えれば STOP(G-repro)。
#   4. 出力: models/23_02_plan.json・models/23_02_summary.json・data/23_02_per_event.csv(推定の緯度経度も)・data/23_02_match.csv・
#      PDF/23_02_F1_offset.pdf・PDF/23_02_F2_scores.pdf(既に本番の出力があれば _rerun_<UTC>)
#
# 読み方(判定はしない):
#   - 2 のずれが大きく、ずれを引いた残りが小さいなら、2 つのカタログは枠(座標の基準)がずれている。どちらが本当の位置に近いかは
#     この比べでは分からない(防災研の一覧の決め方と精度は公開ページに書かれていない)。
#   - 記憶 = jma のまま防災研で採点すると、C4 は気象庁の枠に引きずられた分だけ悪く見えるはず(23_01 の一様なずれと同じ形)。
#   - 記憶 = jma_shift・dpri で防災研に対する C4 の誤差が戻るなら、C4 の良さは「記憶の枠に対する」ものとして別の枠でも成り立つ。
#     ただし速度・局の静的な補正は気象庁の位置で決めたまま(限界)。
#
# Usage(Mac。~/SWIFT で。防災研のファイルを data/external/ct3_201711.txt に置く):
#   cd ~/SWIFT && caffeinate -i uv run python src/23_02_ct2016_dpri_truth.py --max-events 5   (煙試験。結果は _smoke)
#   cd ~/SWIFT && caffeinate -i uv run python src/23_02_ct2016_dpri_truth.py                   (本番)
# 入力  : data/ct2016_processed/tottori_parsed_realpick_ct2016_m15.pt(SHA-256 e6485ac3…9d68)・data/21_04_per_event.csv(271d824d…24a7)・
#         models/21_04_judgment.json(085697a6…281ef)・data/external/ct3_201711.txt(bc29948a…b631。出典: 京大防災研
#         https://www.eqhz.dpri.kyoto-u.ac.jp/images/2019/01/ct3_201711.txt、使う時は Iio ほか, JpGU 2018 SCG57-05 を引用)
# v1 → v2(2026-11-04): v1 は「ずれを決める試験以外の照合が 50 地震以上」を条件にし、実データの煙試験で 45 地震で止まった
#   (キャッシュは Mj ≥ 1.5 だけで、11 月の試験以外は Mj ≥ 2.0 の地震しかないため)。50 は数の目安で根拠が無かったので、
#   ずれの推定の精度そのものを条件にした: 照合 20 地震以上、かつ東・北それぞれの中央値の 95% 区間の幅が 0.2 km 以下
#   (23_01 で C4 が 0.5 km のずれから効き始めたので、その半分より細かく決まっていること)。計算・照合・採点は v1 と同じ。
# v2 → v3(2026-11-04): v2 は精度の条件(95% 区間の幅 ≤ 0.2 km)を満たさないと全体を止めた。実データでは 0.222 km で止まった。
#   精度の条件が要るのは「ずれだけ記憶を動かす」2 つの枠(jma_shift・dpri)だけで、記憶 = 気象庁のまま 2 つの正解で採点する
#   部分にはずれの値を使わない。そこで v3 は、条件を満たさない時は jma_shift・dpri を計算せずに飛ばし(条件は変えない)、
#   記憶 = 気象庁 の採点は必ず行う。計算・照合・採点の式は v1・v2 と同じ。
# 止める条件(STOP): 入力の SHA-256 が違う・21_04 の値と違う・防災研の一覧の形が想定と違う・照合が少なすぎる・G-repro・計算の例外
# 所要  : CPU のみ。採点する地震は約 100。数分〜十数分の見込み
# =============================================================================
import json, argparse, time, csv, hashlib, math, warnings, datetime as dt
from pathlib import Path
import numpy as np
import torch
from scipy.signal import butter, sosfilt
from scipy.stats import wilcoxon
warnings.filterwarnings("ignore", message="All-NaN slice")

import pandas as pd
ap = argparse.ArgumentParser()
ap.add_argument("--cache", default="data/ct2016_processed/tottori_parsed_realpick_ct2016_m15.pt", help="21_04 と同じキャッシュ")
ap.add_argument("--per-event", default="data/21_04_per_event.csv", help="21_04 の地震ごとの結果(再現の確かめに使う)")
ap.add_argument("--judgment", default="models/21_04_judgment.json", help="21_04 の判定(速度などの値の確かめに使う)")
ap.add_argument("--dpri", default="data/external/ct3_201711.txt", help="京大防災研の 2016 年 11 月の余震の震源一覧")
ap.add_argument("--max-events", type=int, default=0, help="煙試験: 採点する地震の最初の N だけ(結果は _smoke の名前)")
ap.add_argument("--no-sha-check", action="store_true", help="入力の SHA-256 を確かめない(合成データでの動作確認だけに使う)")
a = ap.parse_args()
a.dev = False
EXPECT_SHA = {"cache": "e6485ac332e7c550b935bbb75f4ce517018960c5a1da37a98b50ad6fea729d68",
              "per_event": "271d824df81ad34bc1f40ae1e71426badd9ff20e8f580fb6a9eba61dbd6724a7",
              "judgment": "085697a691762983463045129256b340f3efd0404f499e17a60d58f38df281ef",
              "dpri": "bc29948af1c09a83186c051bfcec07fa0e4263ab86234094d58ebf294b14b631"}
# ---------------------------------------------------------------- 23_02 で事前に固定した値(変えたら版を上げる)
AUDIT_VERSION = "v3"
REPRO_TAUS = ["0.5", "1", "2", "3"]
REPRO_TOL_KM = 2e-4
DPRI_TZ_H = 9.0                               # 防災研の一覧は日本時間(気象庁との照合で確かめた: 9 時間ずらすと 104/119 が 2 km 以内で合う)
COARSE_DT_S, COARSE_KM = 2.0, 5.0
STRICT_DT_S, STRICT_KM = 0.5, 3.0
MIN_OFFSET_N = 20                             # v2: 数の下限(精度の条件は下の MAX_CI_WIDTH_KM)
MAX_CI_WIDTH_KM = 0.2                          # v2: 東・北それぞれの中央値の 95% 区間の幅の上限
AUDIT_NBOOT, AUDIT_SEED = 2000, 23
FAR_KM = 10.0
# ---------------------------------------------------------------- 事前に固定した値(変えたら版を上げる)
VERSION = "v1"                            # 21_04 の版(写した計算の版)
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
print(f"[23_02] 本スクリプト {AUDIT_VERSION} SHA-256 {SELF_SHA}(結果を貼る時にこの行も貼ってください)  "
      f"モード: {'dev' if a.dev else ('煙試験 ' + str(a.max_events) + ' 地震' if a.max_events else '本番')}")
def stop(msg): raise SystemExit(msg)
for nm, p in (("cache", a.cache), ("per_event", a.per_event), ("judgment", a.judgment), ("dpri", a.dpri)):
    if not (ROOT / p).exists(): stop(f"[23_02] STOP: {p} が無い(~/SWIFT で回しているか、防災研のファイルを data/external/ に置いたか確かめる)")
    s = sha256(ROOT / p)
    ok = a.no_sha_check or s == EXPECT_SHA[nm]
    print(f"[23_02] 入力 {p}  SHA-256 {s}  " + ("OK" if s == EXPECT_SHA[nm] else ("(確かめない)" if ok else "違う")))
    if not ok: stop(f"[23_02] STOP: {p} の SHA-256 が想定と違う")
# ---------------------------------------------------------------- 1. 入力
CP = ROOT / a.cache
if not CP.exists(): raise SystemExit(f"[23_02] STOP: {a.cache} が無い(ノート 21_04_ct2016_colab.ipynb のセル 11 で作った tottori_parsed_realpick_ct2016_m15.pt を data/ct2016_processed/ に置く)")
EVS = torch.load(CP, map_location="cpu", weights_only=False)
need = ["origin_time", "src_loc", "mw", "waveforms", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
for e in EVS:
    miss = [k for k in need if k not in e]
    if miss: raise SystemExit(f"[23_02] STOP: キャッシュの地震に {miss} が無い(15_01c v3.3 の出力か確かめる)")
for e in EVS:
    w_ = np.asarray(e["waveforms"])
    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[23_02] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[23_02] STOP: {e['origin_time']} の波形に NaN か無限大")
def to_ns(o):
    import pandas as pd
    try:
        t = pd.Timestamp(str(o).replace("Z", "+00:00"))
        t = t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t
        return int(t.value)
    except Exception:
        raise SystemExit(f"[23_02] STOP: origin_time {o!r} を時刻として読めない")
OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
order = np.argsort(OTNS, kind="stable"); EVS = [EVS[i] for i in order]; OTNS = OTNS[order]
NE = len(EVS)
SRC = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS])
MAG = np.array([float(e["mw"]) for e in EVS])
OT = [str(e["origin_time"]) for e in EVS]
if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
    raise SystemExit("[23_02] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[23_02] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
# G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
lo_ns = int(np.datetime64(UNTOUCHED_UTC[0], "ns").astype(np.int64)); hi_ns = int(np.datetime64(UNTOUCHED_UTC[1], "ns").astype(np.int64))
n_out = int(np.sum((OTNS < lo_ns) | (OTNS > hi_ns))); n_big = int(np.sum(MAG >= 6.0 - 1e-6))
FRESH = MAG < FRESH_MAX_MAG - 1e-6
CACHE_SHA = sha256(CP)
n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
print(f"[23_02] 入力: 鳥取県中部 2016 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
      f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
print(f"[23_02] G-untouched: 期間 2016-10-19〜2016-11-15(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
      + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
if n_out != 0 or n_big != 1: raise SystemExit("[23_02] STOP(G-untouched): 鳥取県中部 2016 のキャッシュに見えない(この行を貼って相談)")
im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
    raise SystemExit(f"[23_02] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj 6.6・2016-10-21 05:07:22.57 UTC)")
CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
pool_idx = np.where(OTNS <= CUT_NS)[0]; test_idx = np.where((OTNS > CUT_NS) & FRESH)[0]
if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
    raise SystemExit("[23_02] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
print(f"[23_02] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
print(f"[23_02] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
      f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")

# ---------------------------------------------------------------- 2. 座標・検測(17_02 と同じ)
TFIRST = np.full(NE, np.nan)          # PhaseNet で測った最も早い P(気象庁の発生時刻からの s)
skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
for ie, e in enumerate(EVS):
    n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    ok = np.isfinite(tp) & (pf == 0)
    if ok.any(): TFIRST[ie] = float(tp[ok].min())
    kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
    if len(set(kk)) != n: raise SystemExit(f"[23_02] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
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
print(f"[23_02] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
if len(EVAL) == 0: raise SystemExit("[23_02] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
if a.dev: print(f"[23_02] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                "(較正にも入っているので値は楽観的)")
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
print(f"[23_02] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
      f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")

# ---------------------------------------------------------------- 4. 格子と探索(17_02 と同じ)
H = float(max(30.0, np.percentile(np.abs(np.r_[EX[CAL], EY[CAL]]), 99.5) + 30.0))
STEP = float(max(1.0, round(H / 30.0)))
ZMAX = float(max(30.0, np.percentile(SRC[CAL, 2], 99.5) * 1.3 + 10.0))
ZDEF = float(np.mean(SRC[CAL, 2]))
xc = np.arange(-H, H + 1e-6, STEP); zc = np.arange(0.0, ZMAX + 1e-6, STEP)
GX, GY, GZ = np.meshgrid(xc, xc, zc, indexing="ij"); COARSE = np.c_[GX.ravel(), GY.ravel(), GZ.ravel()]
XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
print(f"[23_02] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
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
# ---------------------------------------------------------------- 5. 事前分布(KDE の帯域は pool の一つ抜き。17_02 と同じ。KDE_H は気象庁の位置で固定)
def loo_ll(h):
    px_, py_ = EX[CAL], EY[CAL]
    d2 = (px_[:, None] - px_[None, :]) ** 2 + (py_[:, None] - py_[None, :]) ** 2
    K = np.exp(-0.5 * d2 / h ** 2); np.fill_diagonal(K, 0.0)
    dens = K.sum(1) / ((len(px_) - 1) * 2 * np.pi * h ** 2); return float(np.mean(np.log(dens + 1e-300)))
HS = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0]
lls = {h: loo_ll(h) for h in HS}; KDE_H = max(lls, key=lls.get)
print(f"[23_02] KDE の帯域(pool の一つ抜き): {KDE_H} km")
def log_prior(nodes, mem, MX, MY):
    """21_04 の log_prior と同じ式。過去の地震の位置を引数 MX・MY にした(23_01 の変更はここだけ)"""
    d2 = (nodes[:, :1] - MX[mem][None, :]) ** 2 + (nodes[:, 1:2] - MY[mem][None, :]) ** 2
    m = -0.5 * d2 / KDE_H ** 2; mx = m.max(1, keepdims=True)
    lk = mx[:, 0] + np.log(np.exp(m - mx).sum(1)) - np.log(len(mem) * 2 * np.pi * KDE_H ** 2)
    lu = -np.log((2 * H) ** 2)
    return np.logaddexp(np.log(1 - PRIOR_EPS) + lk, np.log(PRIOR_EPS) + lu)
def locate_map(pk, mem, dP=None, dS=None, MX=None, MY=None):
    MX = EX if MX is None else MX; MY = EY if MY is None else MY
    mem = np.asarray(mem, int)
    sc = (lambda N: -log_prior(N, mem, MX, MY)) if n_phases(pk) <= 1 else (lambda N: misfit(N, pk, dP, dS) / LAP_B - log_prior(N, mem, MX, MY))
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
    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[23_02] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
    return lib
POOL_OK = np.array(CAL, int)
# C4 の材料: 21_04 と同じ式(過去の地震の水平位置を引数にした)。深さ・発生時刻・速度・局の静的な補正は気象庁の値のまま
def make_RES(MX, MY):
    RES = {}
    for ie in range(NE):
        if not HASP[ie]: continue
        e = EVS[ie]; n = int(e["n_real_stations"]); loc = np.asarray(e["sta_locs"], float)[:n]
        tp = np.asarray(e["tp_times"], float)[:n]; sp = np.asarray(e["sp_diffs"], float)[:n]
        pf = np.asarray(e["p_fallback"]).astype(int)[:n]; sf = np.asarray(e["s_fallback"]).astype(int)[:n]
        sx, sy = to_xy(loc[:, 0], loc[:, 1]); sz = -loc[:, 2] * EL_SCALE
        Rr = np.sqrt((sx - MX[ie]) ** 2 + (sy - MY[ie]) ** 2 + (sz - SRC[ie, 2]) ** 2)
        T = tt(Rr, sz, np.full(n, SRC[ie, 2]), V0, KG)
        okP = np.isfinite(tp) & (pf == 0)
        keysE = [skey(l) for l in loc]
        rP = np.array([tp[k] - T[k] - cP.get(keysE[k], 0.0) if okP[k] else np.nan for k in range(n)])
        med = float(np.nanmedian(rP))
        dPj = {keysE[k]: float(rP[k] - med) for k in range(n) if okP[k]}
        dSj = {keysE[k]: float(tp[k] + sp[k] - T[k] * VPVS - cS.get(keysE[k], 0.0) - med) for k in range(n)
               if okP[k] and sf[k] == 0 and np.isfinite(sp[k])}
        RES[ie] = (dPj, dSj)
    return RES
def corr_from(top, pk, RES):
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

# ================================================================ 23_02 ここから(21_04 に無い部分)
JUDG = json.load(open(ROOT / a.judgment))
if not a.no_sha_check:
    jv = JUDG["velocity"]
    if not (abs(jv["v0"] - V0) < 1e-9 and abs(jv["k"] - KG) < 1e-9 and abs(jv["vpvs"] - VPVS) < 1e-9 and abs(JUDG["laplace_b_s"] - LAP_B) < 1e-9
            and abs(JUDG["kde_h_km"] - KDE_H) < 1e-12 and abs(JUDG["grid"]["H_km"] - H) < 1e-9 and JUDG["n_test"] == len(test_idx)):
        stop("[23_02] STOP: 速度・ラプラス尺度・KDE・格子・試験の数のどれかが 21_04 の判定の JSON と違う(同じ計算になっていない)")
    print("[23_02] 21_04 の判定の JSON と、速度・ラプラス尺度・KDE の帯域・格子・試験の数が一致  PASS")
PE = pd.read_csv(ROOT / a.per_event, dtype={"origin_time": str})
PE_BY = {r["origin_time"]: r for _, r in PE.iterrows()}

# ---------------------------------------------------------------- 1. 防災研の震源一覧を読む
def parse_dpri(p):
    rows = []
    for ln in open(p, encoding="utf-8", errors="replace"):
        tok = ln.strip().rstrip("\\").rstrip("}").strip().split()
        if len(tok) == 0: continue
        if len(tok) != 10: stop(f"[23_02] STOP: 防災研の一覧に 10 列でない行がある: {ln[:80]!r}")
        rows.append([float(x) for x in tok])
    A = np.array(rows)
    if not (np.all(A[:, 0] == 16) and np.all(A[:, 1] == 11)): stop("[23_02] STOP: 防災研の一覧の年・月が 2016 年 11 月でない")
    base = pd.to_datetime(dict(year=2000 + A[:, 0].astype(int), month=A[:, 1].astype(int), day=A[:, 2].astype(int),
                               hour=A[:, 3].astype(int), minute=A[:, 4].astype(int)))
    tj = base.values.astype("datetime64[ns]").astype(np.int64) / 1e9 + A[:, 5]        # 秒の欄は「分」からの秒(60 を超えうる)
    return tj - DPRI_TZ_H * 3600.0, A[:, 6], A[:, 7], A[:, 8], A[:, 9]
TD, DLA, DLO, DDE, DMJ = parse_dpri(ROOT / a.dpri)
print(f"[23_02] 防災研の一覧: {len(TD)} 地震  UTC {pd.to_datetime(TD.min(), unit='s')} 〜 {pd.to_datetime(TD.max(), unit='s')}  "
      f"Mj {DMJ.min():.1f}〜{DMJ.max():.1f}(日本時間として読み、{DPRI_TZ_H} 時間引いて UTC にした)")
OTS = OTNS / 1e9
INWIN = (OTS >= TD.min() - 5) & (OTS <= TD.max() + 5)
def km2(la1, lo1, la2, lo2): return np.hypot((la1 - la2) * 111.0, (lo1 - lo2) * 111.0 * np.cos(np.radians((la1 + la2) / 2)))
# 粗い照合で時刻の差(防災研 − 気象庁)を決める
dts = []
for ie in np.where(INWIN)[0]:
    c = np.where(np.abs(TD - OTS[ie]) < COARSE_DT_S)[0]
    if len(c) == 0: continue
    d = km2(SRC[ie, 0], SRC[ie, 1], DLA[c], DLO[c]); k = c[np.argmin(d)]
    if d.min() < COARSE_KM: dts.append(TD[k] - OTS[ie])
if len(dts) < 20: stop(f"[23_02] STOP: 粗い照合が {len(dts)} 地震しかない(時刻の基準か形式が想定と違う)")
DT0 = float(np.median(dts))
print(f"[23_02] 粗い照合 {len(dts)} 地震: 発生時刻の差(防災研 − 気象庁)の中央値 {DT0:+.3f} s")
# 厳しい照合(1 対 1)
MATCH = np.full(NE, -1)
best = {}
for ie in np.where(INWIN)[0]:
    c = np.where(np.abs(TD - OTS[ie] - DT0) < STRICT_DT_S)[0]
    if len(c) == 0: continue
    d = km2(SRC[ie, 0], SRC[ie, 1], DLA[c], DLO[c]); j = int(np.argmin(d))
    if d[j] >= STRICT_KM: continue
    k = int(c[j])
    if k not in best or d[j] < best[k][1]: best[k] = (ie, float(d[j]))
for k, (ie, _) in best.items(): MATCH[ie] = k
HASD = MATCH >= 0
QX = np.full(NE, np.nan); QY = np.full(NE, np.nan)
QX[HASD], QY[HASD] = to_xy(DLA[MATCH[HASD]], DLO[MATCH[HASD]])
EVAL_SET = set(int(i) for i in EVAL)
NONTEST = np.array([HASD[i] and (i not in EVAL_SET) for i in range(NE)])
TESTM = np.array([HASD[i] and (i in EVAL_SET) for i in range(NE)])
print(f"[23_02] 照合(|Δt − {DT0:+.2f}| < {STRICT_DT_S} s・震央の間 < {STRICT_KM} km・1 対 1): 期間内のキャッシュ {int(INWIN.sum())} 地震のうち {int(HASD.sum())}"
      f"(試験の地震 {int(TESTM.sum())}/{int(sum(INWIN[i] for i in EVAL_SET))}・それ以外 {int(NONTEST.sum())})")
if NONTEST.sum() < MIN_OFFSET_N: stop(f"[23_02] STOP: ずれを決める試験以外の照合が {int(NONTEST.sum())} < {MIN_OFFSET_N}")
RBO = np.random.default_rng(AUDIT_SEED)
def vec_stats(m):
    dx, dy = QX[m] - EX[m], QY[m] - EY[m]
    bs = RBO.integers(0, len(dx), (AUDIT_NBOOT, len(dx)))
    return dict(n=int(m.sum()), east_median_km=float(np.median(dx)), north_median_km=float(np.median(dy)),
                east_ci=[float(x) for x in np.percentile(np.median(dx[bs], axis=1), [2.5, 97.5])],
                north_ci=[float(x) for x in np.percentile(np.median(dy[bs], axis=1), [2.5, 97.5])],
                sep_median_km=float(np.median(np.hypot(dx, dy))),
                scatter_after_shift_median_km=float(np.median(np.hypot(dx - np.median(dx), dy - np.median(dy)))),
                depth_median_km=float(np.median(DDE[MATCH[m]] - SRC[m, 2])), dt_median_s=float(np.median(TD[MATCH[m]] - OTS[m])))
OFF_NT, OFF_TE = vec_stats(NONTEST), vec_stats(TESTM)
OFFE, OFFN = OFF_NT["east_median_km"], OFF_NT["north_median_km"]
CIW = max(OFF_NT["east_ci"][1] - OFF_NT["east_ci"][0], OFF_NT["north_ci"][1] - OFF_NT["north_ci"][0])
for nm, o in (("試験以外(ずれの推定に使う)", OFF_NT), ("試験の地震(記述)", OFF_TE)):
    print(f"[23_02] 防災研 − 気象庁 {nm} n={o['n']}: 東 {o['east_median_km']:+.3f} km [{o['east_ci'][0]:+.3f}, {o['east_ci'][1]:+.3f}]・"
          f"北 {o['north_median_km']:+.3f} km [{o['north_ci'][0]:+.3f}, {o['north_ci'][1]:+.3f}]・震央の間の中央値 {o['sep_median_km']:.3f} km・"
          f"共通のずれを引いた残りの中央値 {o['scatter_after_shift_median_km']:.3f} km・深さ {o['depth_median_km']:+.2f} km・時刻 {o['dt_median_s']:+.3f} s")
OFF_OK = CIW <= MAX_CI_WIDTH_KM
print(f"[23_02] ずれの精度: 95% 区間の幅の大きい方 {CIW:.3f} km(上限 {MAX_CI_WIDTH_KM} km)  " + ("PASS" if OFF_OK else
      "FAIL → ずれだけ記憶を動かす枠(jma_shift・dpri)は計算しない。記憶 = 気象庁 のまま、正解 = 気象庁・防災研 の両方で採点する"))

# ---------------------------------------------------------------- 2. 記憶の 3 つの枠
VARS = {"jma": (EX, EY)}
if OFF_OK:
    VARS["jma_shift"] = (EX + OFFE, EY + OFFN)
    VARS["dpri"] = (np.where(HASD, QX, EX + OFFE), np.where(HASD, QY, EY + OFFN))
RESV = {k: make_RES(*v) for k, v in VARS.items()}
TARGETS = [int(i) for i in EVAL if HASD[i]]
if a.max_events: TARGETS = TARGETS[:a.max_events]
SUF = "_smoke" if a.max_events else ""
if SUF == "" and (ROOT / "models/23_02_summary.json").exists():
    SUF = "_rerun_" + utcnow().replace(":", "").replace("-", ""); print(f"[23_02] 注意: 本番の結果が既にある。上書きせず {SUF} の名前に書く")
plan = dict(script="23_02_ct2016_dpri_truth.py", version=AUDIT_VERSION, script_sha256=SELF_SHA, utc=utcnow(), suffix=SUF,
            inputs={nm: dict(path=p, sha256=sha256(ROOT / p)) for nm, p in (("per_event", a.per_event), ("judgment", a.judgment), ("dpri", a.dpri))} | {"cache": dict(path=a.cache, sha256=CACHE_SHA)},
            fixed=dict(dpri_tz_h=DPRI_TZ_H, coarse_dt_s=COARSE_DT_S, coarse_km=COARSE_KM, strict_dt_s=STRICT_DT_S, strict_km=STRICT_KM,
                       min_offset_n=MIN_OFFSET_N, max_ci_width_km=MAX_CI_WIDTH_KM, ci_width_km=CIW, offset_precise=bool(OFF_OK), memory_frames=list(VARS), taus=REPRO_TAUS, tol_km=REPRO_TOL_KM, nboot=AUDIT_NBOOT, seed=AUDIT_SEED, far_km=FAR_KM),
            dt0_s=DT0, offset_from_nontest=OFF_NT, offset_test_descriptive=OFF_TE, n_targets=len(TARGETS),
            note="descriptive only; 21_04 verdict, rules and cache unchanged")
json.dump(plan, open(ROOT / f"models/23_02_plan{SUF}.json", "w"), indent=1, ensure_ascii=False)
print(f"[23_02] 計算の前の記録: models/23_02_plan{SUF}.json  採点する試験の地震 {len(TARGETS)}")

def c_from_audit(S, lib, pk, m6r, RES, MX, MY, ie):
    pos = int((S > 0).sum())
    if pos < MIN_POS: return dict(C1=None, C3=m6r, C4=m6r)
    top = lib[np.argsort(-S, kind="stable")[:min(TOPK, pos)]]
    if ie in top: stop("[23_02] STOP: 自分自身が似た地震の上位に入っている")
    dP, dS = corr_from(top, pk, RES)
    return dict(C1=(float(MX[top[0]]), float(MY[top[0]])), C3=locate_map(pk, top, MX=MX, MY=MY), C4=locate_map(pk, top, dP, dS, MX=MX, MY=MY))
def errs(ie, xy):
    if xy is None or not np.all(np.isfinite(xy)): return np.nan, np.nan, np.nan, np.nan
    la, lo = to_ll(xy[0], xy[1])
    return km_between(la, lo, SRC[ie, 0], SRC[ie, 1]), km_between(la, lo, DLA[MATCH[ie]], DLO[MATCH[ie]]), float(la), float(lo)
ROWS, worst = [], 0.0
T_EV = time.time()
for ii, ie in enumerate(TARGETS):
    try:
        lib = library(ie); p0 = FIRST[ie]; m3 = prior_members(lib, p0[0], (p0[1], p0[2]))
        for t in REPRO_TAUS:
            tau = float(t); pk = picks_of(ie, tau)
            S, ni = similarity(ie, tau, lib, BAND)
            ROWS.append((OT[ie], "none", t, "M5") + errs(ie, locate_phys(pk)))
            for vn, (MX, MY) in VARS.items():
                m6r = locate_map(pk, m3, MX=MX, MY=MY); o = c_from_audit(S, lib, pk, m6r, RESV[vn], MX, MY, ie)
                ROWS.append((OT[ie], vn, t, "M6r") + errs(ie, m6r))
                for m in ("C1", "C3", "C4"): ROWS.append((OT[ie], vn, t, m) + errs(ie, o[m]))
    except SystemExit:
        raise
    except BaseException as ex:
        stop(f"[23_02] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
    ref = PE_BY.get(OT[ie])
    if ref is None: stop(f"[23_02] STOP(G-repro): {OT[ie]} が 21_04 の CSV に無い")
    for r in ROWS[-(len(REPRO_TAUS) * (1 + 4 * len(VARS))):]:
        if r[1] not in ("none", "jma"): continue
        rv = ref.get(f"{r[3]}_err_t{r[2]}", np.nan); rv = float(rv) if pd.notna(rv) else np.nan
        if np.isnan(rv) != np.isnan(r[4]): stop(f"[23_02] STOP(G-repro): {OT[ie]} τ={r[2]} {r[3]}: 21_04 {rv} / 23_02 {r[4]}")
        if np.isfinite(rv):
            worst = max(worst, abs(rv - r[4]))
            if abs(rv - r[4]) > REPRO_TOL_KM: stop(f"[23_02] STOP(G-repro): {OT[ie]} τ={r[2]} {r[3]}: 21_04 {rv:.4f} / 23_02 {r[4]:.4f} km")
    if (ii + 1) in (5, 20) or (ii + 1) % 25 == 0:
        el = time.time() - T_EV
        print(f"  … {ii+1}/{len(TARGETS)}  G-repro の最大の差 {worst:.1e} km  (残りの見込み約 {el/(ii+1)*(len(TARGETS)-ii-1)/60:.0f} 分)", flush=True)
print(f"[23_02] G-repro: {len(TARGETS)} 地震 × τ {REPRO_TAUS} × [M5, M6r, C1, C3, C4](記憶 = 気象庁)が 21_04 と一致(最大の差 {worst:.1e} km)  PASS")
D = pd.DataFrame(ROWS, columns=["origin_time", "memory", "tau", "method", "err_vs_jma_km", "err_vs_dpri_km", "est_lat", "est_lon"])
D.to_csv(ROOT / f"data/23_02_per_event{SUF}.csv", index=False, float_format="%.5f")
pd.DataFrame(dict(origin_time=[OT[i] for i in range(NE) if HASD[i]], mj=[float(MAG[i]) for i in range(NE) if HASD[i]],
                  is_test=[bool(TESTM[i]) for i in range(NE) if HASD[i]],
                  jma_lat=[SRC[i, 0] for i in range(NE) if HASD[i]], jma_lon=[SRC[i, 1] for i in range(NE) if HASD[i]], jma_dep=[SRC[i, 2] for i in range(NE) if HASD[i]],
                  dpri_lat=DLA[MATCH[HASD]], dpri_lon=DLO[MATCH[HASD]], dpri_dep=DDE[MATCH[HASD]], dt_s=TD[MATCH[HASD]] - OTS[HASD])
             ).to_csv(ROOT / f"data/23_02_match{SUF}.csv", index=False, float_format="%.5f")

# ---------------------------------------------------------------- 3. 集計(全て記述)
RB = np.random.default_rng(AUDIT_SEED)
def med_ci(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) == 0: return dict(n=0, median_km=None, ci=[None, None], frac_gt10=None)
    bs = np.median(x[RB.integers(0, len(x), (AUDIT_NBOOT, len(x)))], axis=1)
    return dict(n=int(len(x)), median_km=float(np.median(x)), ci=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], frac_gt10=float(np.mean(x > FAR_KM)))
CASES = [("none", "M5")] + [(v, m) for v in VARS for m in ("M6r", "C1", "C3", "C4")]
SUMM = {}
cat_sep = np.array([km2(SRC[i, 0], SRC[i, 1], DLA[MATCH[i]], DLO[MATCH[i]]) for i in TARGETS])
SUMM["jma_catalogue_vs_dpri"] = med_ci(cat_sep)
for t in REPRO_TAUS:
    for v, m in CASES:
        sub = D[(D.tau == t) & (D.memory == v) & (D.method == m)]
        SUMM[f"{v}|{m}|{t}"] = dict(vs_jma=med_ci(sub.err_vs_jma_km), vs_dpri=med_ci(sub.err_vs_dpri_km), available=float(sub.err_vs_jma_km.notna().mean()))
def f2(x): return "  —  " if x is None else f"{x:5.2f}"
print(f"\n[23_02] ===== 水平誤差の中央値 km(試験の地震のうち防災研の一覧にある {len(TARGETS)} 地震、全て記述) =====")
print(f"  参考: 気象庁の震央そのものと防災研の震央の間の中央値 {f2(SUMM['jma_catalogue_vs_dpri']['median_km'])} km")
for t in REPRO_TAUS:
    print(f"  τ = {t} s              正解=気象庁   正解=防災研   (値がある割合)")
    for v, m in CASES:
        s = SUMM[f"{v}|{m}|{t}"]
        print(f"    {('記憶=' + v) if v != 'none' else '記憶なし':<16} {m:<4} {f2(s['vs_jma']['median_km'])}        {f2(s['vs_dpri']['median_km'])}        ({s['available']:.2f})")
LIM = ["descriptive only: the 21_04 test was opened once on 2026-10-30; nothing here changes its verdict, rules or cache",
       "the DPRI catalogue covers November 2016 only (the period with relatively uniform temporary-station coverage); its location method and errors are not documented on the release page",
       "the common JMA-to-DPRI offset is estimated from matched non-test events; it is a frame difference between two catalogues, and which frame is closer to the truth is not known",
       "velocity, static station terms, KDE bandwidth and grid were fitted on pool events at JMA locations and are kept; memory depths and origin times stay JMA",
       "the 'dpri' memory uses DPRI positions where a past event is matched and JMA + common offset otherwise",
       "21_04 limits apply unchanged (offline PhaseNet picks, up to 24 stations, no latency, one sequence, Mj 1.5-1.9 test events)"]
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(dict(plan=plan, gates=dict(repro=dict(status="PASS", max_abs_diff_km=worst, tol_km=REPRO_TOL_KM)), summary=SUMM, limits=LIM,
                     runtime_s=time.time() - T0)), open(ROOT / f"models/23_02_summary{SUF}.json", "w"), indent=1)

# ---------------------------------------------------------------- 4. 図(白背景・英語・凡例は枠外)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 11})
fig, ax = plt.subplots(figsize=(6.4, 6.0))
for m, c, lab in ((NONTEST, "0.55", f"Non-test events (n = {int(NONTEST.sum())}), used for the offset"), (TESTM, "tab:red", f"Test events (n = {int(TESTM.sum())})")):
    ax.scatter(QX[m] - EX[m], QY[m] - EY[m], s=10, color=c, alpha=0.6, label=lab)
ax.plot([OFFE], [OFFN], marker="*", ms=18, color="tab:blue", mec="k", ls="none", label=f"Median offset: east {OFFE:+.2f} km, north {OFFN:+.2f} km")
ax.axhline(0, color="k", lw=0.6); ax.axvline(0, color="k", lw=0.6); ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax.set_xlabel("DPRI minus JMA, east (km)"); ax.set_ylabel("DPRI minus JMA, north (km)")
ax.set_title("Central Tottori 2016, November: DPRI dense-network vs JMA epicentres", fontsize=10)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), fontsize=9, frameon=False)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/23_02_F1_offset{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
fig, axs = plt.subplots(1, 2, figsize=(12.0, 4.6), sharey=True)
labs = ["M5\n(no memory)"] + [f"{m}\n{v}" for v in VARS for m in ("M6r", "C1", "C3", "C4")]
for ax, t in zip(axs, ("0.5", "2")):
    xs = np.arange(len(CASES)); wj = [SUMM[f"{v}|{m}|{t}"]["vs_jma"]["median_km"] or np.nan for v, m in CASES]
    wd = [SUMM[f"{v}|{m}|{t}"]["vs_dpri"]["median_km"] or np.nan for v, m in CASES]
    ax.bar(xs - 0.2, wj, 0.4, color="0.65", label="Truth = JMA epicentre"); ax.bar(xs + 0.2, wd, 0.4, color="tab:blue", label="Truth = DPRI epicentre")
    ax.axhline(SUMM["jma_catalogue_vs_dpri"]["median_km"], color="tab:red", ls="--", lw=1.2, label="JMA catalogue vs DPRI (median)")
    ax.set_xticks(xs); ax.set_xticklabels(labs, fontsize=7, rotation=90); ax.set_title(f"{t} s after the first P", fontsize=11); ax.grid(alpha=0.3, axis="y")
axs[0].set_ylabel("Median epicentral error (km)")
h, l = axs[0].get_legend_handles_labels()
fig.suptitle(f"Central Tottori 2016, {len(TARGETS)} November test events: scored against JMA and DPRI (descriptive)", fontsize=11)
fig.legend(h, l, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=3, fontsize=9, frameon=False)
fig.tight_layout(rect=(0, 0.04, 1, 0.95)); fig.savefig(ROOT / f"PDF/23_02_F2_scores{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
print(f"\n[23_02] 限界: " + " / ".join(LIM))
print(f"[23_02] 出力: models/23_02_plan{SUF}.json, models/23_02_summary{SUF}.json, data/23_02_per_event{SUF}.csv, data/23_02_match{SUF}.csv, "
      f"PDF/23_02_F1_offset{SUF}.pdf, PDF/23_02_F2_scores{SUF}.pdf  ({time.time()-T0:.0f} s)")
