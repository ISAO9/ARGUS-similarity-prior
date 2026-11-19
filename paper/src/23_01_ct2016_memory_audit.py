#!/usr/bin/env python3
# =============================================================================
# Script : 23_01_ct2016_memory_audit.py  (v1)
#          [読むだけの記述: 鳥取県中部 2016 の試験(21_04、2026-10-30 に 1 回だけ開いた)の 307 地震で、
#           「記憶(過去の地震の気象庁の位置)」にどれだけ頼っているかを 3 つの方法で調べる]
# Project: ARGUS(新生)— 発表(SSJ 2026 S21-03)の「最大の限界: 正解も記憶も気象庁の震源」への答え。
#          21_04 の判定(CONFIRMED)・規則・キャッシュは一切変えない。結果は全て記述(事前に決めた検定ではない)。
#
# なぜ必要か:
#   21_04 では、正解も、過去の地震の位置(C1 の答え・C3 の事前分布・C4 の局の補正・M6r の事前分布)も気象庁の震源。
#   改善の一部が「気象庁の位置を借りているだけ」かどうかは、正解を変えずに記憶の側だけを動かすと測れる。
#
# 何をするか(値はすべて下の「事前に固定した値」。この版の SHA-256 と値を、計算の前に models/23_01_plan.json に書く):
#   0. 再現(G-repro): 21_04 v1 と同じ計算(この下の 1〜6 は 21_04 v1 の 1〜6 節を 1 字も変えずに写し、[21_04] の表示名と
#      「記憶の位置」を引数にした所だけを変えた)で、τ = 0.5・1・2・3 s の M6r・C1・C3・C4 の誤差を出し、
#      21_04 の data/21_04_per_event.csv と地震ごとに比べる。差が 2e-4 km を超える地震が 1 つでもあれば STOP。
#   1. 層別(①): 再現した値で、Mj の区分・気象庁の深さの 3 分位・τ = 2 s の P の局の数ごとの中央値と 10 km 超の割合。
#      (推定の深さは 21_04 が保存していないので、深さの誤差は出さない。区分は「深さで分けた水平誤差」)
#   2. 空間ホールドアウト(②): 目標の地震の気象庁の震央から R km 以内の過去の地震を、記憶から全て外す
#      (C1・C3・C4 の候補、M6r の事前分布の両方から)。R = 1・2・5 km。外したことで「すぐ隣のコピー」が使えなくなる。
#   3. 記憶の位置の感度(③): 過去の地震の位置(水平)だけを動かし、正解(気象庁)はそのまま。
#      (a) ばらばらのずれ: 地震ごとに独立な等方正規分布 σ = 0.5・1・2 km(乱数の種 3 つ)
#      (b) 一様なずれ: 全ての過去の地震を東へ d = 0.5・1・2 km
#      動かした位置は C1 の答え・C3/M6r の事前分布・C4 の局の補正(走時の残りを動かした位置で計算し直す)の全てに使う。
#      速度・局の静的な補正・KDE の帯域・格子(pool で決めた値)は気象庁の位置のまま固定する(限界として書く)。
#   ②・③は τ = 0.5・2 s(21_04 の H1〜H3 の τ)だけで計算する。似ている度合い S は波形だけで決まるので、各 τ で 1 回だけ
#   計算し、全ての変種で使い回す(②は S の一部を外すだけ)。物理だけの M5(記憶を使わない)は参考として載せる。
#
# 読み方(判定はしない。数字を並べるだけ):
#   ② で R を大きくしても C4 < M6r が保たれれば、中央値の改善は「すぐ隣の位置のコピー」だけではない。
#   ③(a) で σ を大きくした時の C4 の悪化の速さが、記憶の位置の誤差への感度。(b) で C4 の誤差が d とともに増えるなら、
#   C4 は記憶の枠(気象庁の枠)に引き寄せられている。どちらも M6r も記憶を使うので、両方の値を並べる。
#
# Usage(Mac。21_04 を回した ~/SWIFT で。21_04 の出力と同じフォルダを読むだけで、21_04 の出力には書かない):
#   cd ~/SWIFT && caffeinate -i uv run python src/23_01_ct2016_memory_audit.py --max-events 10   (煙試験。結果は _smoke)
#   cd ~/SWIFT && caffeinate -i uv run python src/23_01_ct2016_memory_audit.py                    (本番。307 地震)
# 入力  : data/ct2016_processed/tottori_parsed_realpick_ct2016_m15.pt(21_04 と同じ。SHA-256 e6485ac3…9d68 を確かめる)
#         data/21_04_per_event.csv(SHA-256 271d824d…24a7)・models/21_04_judgment.json(SHA-256 085697a6…281ef)
# 出力  : models/23_01_plan.json(計算の前)・models/23_01_summary.json・data/23_01_per_event.csv(縦長: 地震・変種・τ・方法・誤差)
#         PDF/23_01_F1_holdout.pdf・PDF/23_01_F2_perturb.pdf・PDF/23_01_F3_strata.pdf
#         (既に本番の出力があれば上書きせず _rerun_<UTC> の名前に書く)
# 止める条件(STOP): 入力の SHA-256 が違う・G-untouched/G-split が 21_04 と違う・G-repro・計算の例外
# 所要  : CPU のみ。S の計算は 21_04 の約半分、位置の計算は 1 地震あたり約 100 回。最初の 5 地震の後に残りの見込みを表示する
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
ap.add_argument("--max-events", type=int, default=0, help="煙試験: 最初の N 地震だけ(結果は _smoke の名前)")
ap.add_argument("--dev", action="store_true", help="21_04 --dev と同じ地震(pool の最後の 20)で動作確認(21_04 の _dev の CSV と比べる)")
ap.add_argument("--no-sha-check", action="store_true", help="入力の SHA-256 を確かめない(合成データでの動作確認だけに使う)")
a = ap.parse_args()
EXPECT_SHA = {"cache": "e6485ac332e7c550b935bbb75f4ce517018960c5a1da37a98b50ad6fea729d68",
              "per_event": "271d824df81ad34bc1f40ae1e71426badd9ff20e8f580fb6a9eba61dbd6724a7",
              "judgment": "085697a691762983463045129256b340f3efd0404f499e17a60d58f38df281ef"}
# ---------------------------------------------------------------- 23_01 で事前に固定した値(変えたら版を上げる)
AUDIT_VERSION = "v1"
REPRO_TAUS = ["0.5", "1", "2", "3"]          # G-repro を見る τ
REPRO_METH = ["M6r", "C1", "C3", "C4"]
REPRO_TOL_KM = 2e-4                           # 21_04 の CSV は小数 4 桁
VTAUS = ["0.5", "2"]                          # ②・③ を計算する τ
HOLD_R_KM = [1.0, 2.0, 5.0]
RAND_SIG_KM = [0.5, 1.0, 2.0]
RAND_SEEDS = [101, 102, 103]
SHIFT_E_KM = [0.5, 1.0, 2.0]
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
print(f"[23_01] 本スクリプト {AUDIT_VERSION} SHA-256 {SELF_SHA}(結果を貼る時にこの行も貼ってください)  "
      f"モード: {'dev' if a.dev else ('煙試験 ' + str(a.max_events) + ' 地震' if a.max_events else '本番')}")
def stop(msg): raise SystemExit(msg)
for nm, p in (("cache", a.cache), ("per_event", a.per_event), ("judgment", a.judgment)):
    if not (ROOT / p).exists(): stop(f"[23_01] STOP: {p} が無い(~/SWIFT で回しているか確かめる)")
    s = sha256(ROOT / p)
    ok = a.no_sha_check or a.dev or s == EXPECT_SHA[nm]
    print(f"[23_01] 入力 {p}  SHA-256 {s}  " + ("OK" if s == EXPECT_SHA[nm] else ("(確かめない)" if ok else "違う")))
    if not ok: stop(f"[23_01] STOP: {p} の SHA-256 が 21_04 の本番のものと違う")
# ---------------------------------------------------------------- 1. 入力
CP = ROOT / a.cache
if not CP.exists(): raise SystemExit(f"[23_01] STOP: {a.cache} が無い(ノート 21_04_ct2016_colab.ipynb のセル 11 で作った tottori_parsed_realpick_ct2016_m15.pt を data/ct2016_processed/ に置く)")
EVS = torch.load(CP, map_location="cpu", weights_only=False)
need = ["origin_time", "src_loc", "mw", "waveforms", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
for e in EVS:
    miss = [k for k in need if k not in e]
    if miss: raise SystemExit(f"[23_01] STOP: キャッシュの地震に {miss} が無い(15_01c v3.3 の出力か確かめる)")
for e in EVS:
    w_ = np.asarray(e["waveforms"])
    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[23_01] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[23_01] STOP: {e['origin_time']} の波形に NaN か無限大")
def to_ns(o):
    import pandas as pd
    try:
        t = pd.Timestamp(str(o).replace("Z", "+00:00"))
        t = t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t
        return int(t.value)
    except Exception:
        raise SystemExit(f"[23_01] STOP: origin_time {o!r} を時刻として読めない")
OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
order = np.argsort(OTNS, kind="stable"); EVS = [EVS[i] for i in order]; OTNS = OTNS[order]
NE = len(EVS)
SRC = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS])
MAG = np.array([float(e["mw"]) for e in EVS])
OT = [str(e["origin_time"]) for e in EVS]
if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
    raise SystemExit("[23_01] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[23_01] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
# G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
lo_ns = int(np.datetime64(UNTOUCHED_UTC[0], "ns").astype(np.int64)); hi_ns = int(np.datetime64(UNTOUCHED_UTC[1], "ns").astype(np.int64))
n_out = int(np.sum((OTNS < lo_ns) | (OTNS > hi_ns))); n_big = int(np.sum(MAG >= 6.0 - 1e-6))
FRESH = MAG < FRESH_MAX_MAG - 1e-6
CACHE_SHA = sha256(CP)
n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
print(f"[23_01] 入力: 鳥取県中部 2016 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
      f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
print(f"[23_01] G-untouched: 期間 2016-10-19〜2016-11-15(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
      + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
if n_out != 0 or n_big != 1: raise SystemExit("[23_01] STOP(G-untouched): 鳥取県中部 2016 のキャッシュに見えない(この行を貼って相談)")
im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
    raise SystemExit(f"[23_01] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj 6.6・2016-10-21 05:07:22.57 UTC)")
CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
pool_idx = np.where(OTNS <= CUT_NS)[0]; test_idx = np.where((OTNS > CUT_NS) & FRESH)[0]
if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
    raise SystemExit("[23_01] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
print(f"[23_01] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
print(f"[23_01] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
      f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")

# ---------------------------------------------------------------- 2. 座標・検測(17_02 と同じ)
TFIRST = np.full(NE, np.nan)          # PhaseNet で測った最も早い P(気象庁の発生時刻からの s)
skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
for ie, e in enumerate(EVS):
    n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    ok = np.isfinite(tp) & (pf == 0)
    if ok.any(): TFIRST[ie] = float(tp[ok].min())
    kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
    if len(set(kk)) != n: raise SystemExit(f"[23_01] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
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
print(f"[23_01] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
if len(EVAL) == 0: raise SystemExit("[23_01] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
if a.dev: print(f"[23_01] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
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
print(f"[23_01] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
      f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")

# ---------------------------------------------------------------- 4. 格子と探索(17_02 と同じ)
H = float(max(30.0, np.percentile(np.abs(np.r_[EX[CAL], EY[CAL]]), 99.5) + 30.0))
STEP = float(max(1.0, round(H / 30.0)))
ZMAX = float(max(30.0, np.percentile(SRC[CAL, 2], 99.5) * 1.3 + 10.0))
ZDEF = float(np.mean(SRC[CAL, 2]))
xc = np.arange(-H, H + 1e-6, STEP); zc = np.arange(0.0, ZMAX + 1e-6, STEP)
GX, GY, GZ = np.meshgrid(xc, xc, zc, indexing="ij"); COARSE = np.c_[GX.ravel(), GY.ravel(), GZ.ravel()]
XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
print(f"[23_01] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
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
print(f"[23_01] KDE の帯域(pool の一つ抜き): {KDE_H} km")
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
    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[23_01] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
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

# ================================================================ 23_01 ここから(21_04 に無い部分)
JUDG = json.load(open(ROOT / a.judgment))
if not a.no_sha_check:
    jv = JUDG["velocity"]
    if not (abs(jv["v0"] - V0) < 1e-9 and abs(jv["k"] - KG) < 1e-9 and abs(jv["vpvs"] - VPVS) < 1e-9 and abs(JUDG["laplace_b_s"] - LAP_B) < 1e-9
            and abs(JUDG["kde_h_km"] - KDE_H) < 1e-12 and abs(JUDG["grid"]["H_km"] - H) < 1e-9 and JUDG["n_test"] == len(test_idx)):
        stop("[23_01] STOP: 速度・ラプラス尺度・KDE・格子・試験の数のどれかが 21_04 の判定の JSON と違う(同じ計算になっていない)")
    print("[23_01] 21_04 の判定の JSON と、速度・ラプラス尺度・KDE の帯域・格子・試験の数が一致  PASS")
PE = pd.read_csv(ROOT / a.per_event, dtype={"origin_time": str})
PE_BY = {r["origin_time"]: r for _, r in PE.iterrows()}
if a.max_events: EVAL = EVAL[:a.max_events]
missing = [OT[ie] for ie in EVAL if OT[ie] not in PE_BY]
if missing: stop(f"[23_01] STOP(G-repro): 21_04 の CSV に無い地震 {len(missing)}(最初 {missing[0]})")
SUF = "_dev" if a.dev else ("_smoke" if a.max_events else "")
if SUF == "" and (ROOT / "models/23_01_summary.json").exists():
    SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
    print(f"[23_01] 注意: 本番の結果が既にある。上書きせず {SUF} の名前に書く")

# ---------------------------------------------------------------- 記憶の位置の変種(③)と、その局の補正
VARS = {"base": (EX, EY)}
for sg in RAND_SIG_KM:
    for sd in RAND_SEEDS:
        rg = np.random.default_rng(sd * 1000 + int(round(sg * 100)))
        VARS[f"rand{sg:g}_s{sd}"] = (EX + rg.normal(0.0, sg, NE), EY + rg.normal(0.0, sg, NE))
for d in SHIFT_E_KM: VARS[f"shiftE{d:g}"] = (EX + d, EY.copy())
RESV = {k: make_RES(*v) for k, v in VARS.items()}
print(f"[23_01] 記憶の位置の変種 {len(VARS)}(基準 1・ばらばら {len(RAND_SIG_KM)}×{len(RAND_SEEDS)}・一様 {len(SHIFT_E_KM)})の局の補正を計算  ({time.time()-T0:.0f} s)")
VNAMES = ["base"] + [f"hold{r:g}" for r in HOLD_R_KM] + [k for k in VARS if k != "base"]
plan = dict(script="23_01_ct2016_memory_audit.py", version=AUDIT_VERSION, script_sha256=SELF_SHA, utc=utcnow(), suffix=SUF,
            copied_from=dict(script="21_04_ct2016_similarity_confirmation.py", version=VERSION, sections="1-6 (verbatim except labels and memory-position arguments)"),
            inputs={nm: dict(path=p, sha256=sha256(ROOT / p)) for nm, p in (("per_event", a.per_event), ("judgment", a.judgment))} | {"cache": dict(path=a.cache, sha256=CACHE_SHA)},
            fixed=dict(repro_taus=REPRO_TAUS, repro_methods=REPRO_METH + ["M5"], repro_tol_km=REPRO_TOL_KM, vtaus=VTAUS, hold_r_km=HOLD_R_KM,
                       rand_sigma_km=RAND_SIG_KM, rand_seeds=RAND_SEEDS, shift_east_km=SHIFT_E_KM, nboot=AUDIT_NBOOT, seed=AUDIT_SEED, far_km=FAR_KM),
            n_events=int(len(EVAL)), note="descriptive only; 21_04 verdict, rules and cache unchanged")
json.dump(plan, open(ROOT / f"models/23_01_plan{SUF}.json", "w"), indent=1, ensure_ascii=False)
print(f"[23_01] 計算の前の記録: models/23_01_plan{SUF}.json")

def c_from_audit(S, lib, pk, m6r, RES, MX, MY, ie):
    """21_04 の c_from(C1・C3・C4)と同じ規則。記憶の位置 MX・MY と局の補正 RES を引数にした"""
    pos = int((S > 0).sum())
    if pos < MIN_POS: return dict(C1=None, C3=m6r, C4=m6r)
    top = lib[np.argsort(-S, kind="stable")[:min(TOPK, pos)]]
    if ie in top: stop("[23_01] STOP: 自分自身が似た地震の上位に入っている")
    dP, dS = corr_from(top, pk, RES)
    return dict(C1=(float(MX[top[0]]), float(MY[top[0]])), C3=locate_map(pk, top, MX=MX, MY=MY), C4=locate_map(pk, top, dP, dS, MX=MX, MY=MY))
def err_km(ie, xy):
    if xy is None or not np.all(np.isfinite(xy)): return np.nan
    la, lo = to_ll(xy[0], xy[1]); return km_between(la, lo, SRC[ie, 0], SRC[ie, 1])
def eval_audit(ie):
    lib = library(ie); p0 = FIRST[ie]
    m3 = prior_members(lib, p0[0], (p0[1], p0[2]))
    dlib = np.array([km_between(SRC[j, 0], SRC[j, 1], SRC[ie, 0], SRC[ie, 1]) for j in lib])
    rows = []
    for t in REPRO_TAUS:
        tau = float(t); pk = picks_of(ie, tau)
        r5 = locate_phys(pk); rows.append(("base", t, "M5", err_km(ie, r5)))
        S, ni = similarity(ie, tau, lib, BAND)
        m6r = locate_map(pk, m3); o = c_from_audit(S, lib, pk, m6r, RESV["base"], EX, EY, ie)
        rows += [("base", t, "M6r", err_km(ie, m6r))] + [("base", t, m, err_km(ie, o[m])) for m in ("C1", "C3", "C4")]
        if t not in VTAUS: continue
        for R in HOLD_R_KM:                                   # ② 空間ホールドアウト
            keep = dlib > R; libR = lib[keep]
            if len(libR) == 0:
                rows += [(f"hold{R:g}", t, m, np.nan) for m in ("M6r", "C1", "C3", "C4")]; continue
            m3R = prior_members(libR, p0[0], (p0[1], p0[2]))
            if len(m3R) == 0:
                rows += [(f"hold{R:g}", t, m, np.nan) for m in ("M6r", "C1", "C3", "C4")]; continue
            m6rR = locate_map(pk, m3R); oR = c_from_audit(S[keep], libR, pk, m6rR, RESV["base"], EX, EY, ie)
            rows += [(f"hold{R:g}", t, "M6r", err_km(ie, m6rR))] + [(f"hold{R:g}", t, m, err_km(ie, oR[m])) for m in ("C1", "C3", "C4")]
        for vn, (MX, MY) in VARS.items():                     # ③ 記憶の位置を動かす
            if vn == "base": continue
            m6rV = locate_map(pk, m3, MX=MX, MY=MY); oV = c_from_audit(S, lib, pk, m6rV, RESV[vn], MX, MY, ie)
            rows += [(vn, t, "M6r", err_km(ie, m6rV))] + [(vn, t, m, err_km(ie, oV[m])) for m in ("C1", "C3", "C4")]
    return rows

# ---------------------------------------------------------------- 計算(各地震の直後に G-repro)
ROWS, worst = [], 0.0
T_EV = time.time()
for ii, ie in enumerate(EVAL):
    try:
        rows = eval_audit(ie)
    except SystemExit:
        raise
    except BaseException as ex:
        stop(f"[23_01] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
    ref = PE_BY[OT[ie]]
    for (vn, t, m, ev) in rows:
        if vn != "base" or m not in REPRO_METH + ["M5"]: continue
        rv = ref.get(f"{m}_err_t{t}", np.nan); rv = float(rv) if pd.notna(rv) else np.nan
        if np.isnan(rv) != np.isnan(ev): stop(f"[23_01] STOP(G-repro): {OT[ie]} τ={t} {m}: 21_04 {rv} / 23_01 {ev}(値の有無が違う)")
        if np.isfinite(rv):
            dd = abs(rv - ev); worst = max(worst, dd)
            if dd > REPRO_TOL_KM: stop(f"[23_01] STOP(G-repro): {OT[ie]} τ={t} {m}: 21_04 {rv:.4f} / 23_01 {ev:.4f} km(差 {dd:.2e})")
    ROWS += [(OT[ie], float(MAG[ie]), float(SRC[ie, 2]), int(len(picks_of(ie, 2.0))), vn, t, m, ev) for (vn, t, m, ev) in rows]
    if (ii + 1) in (5, 20) or (ii + 1) % 50 == 0:
        el = time.time() - T_EV
        print(f"  … {ii+1}/{len(EVAL)}  G-repro の最大の差 {worst:.1e} km  ({time.time()-T0:.0f} s、残りの見込み約 {el/(ii+1)*(len(EVAL)-ii-1)/60:.0f} 分)", flush=True)
print(f"[23_01] G-repro: {len(EVAL)} 地震 × τ {REPRO_TAUS} × {REPRO_METH + ['M5']} が 21_04 と一致(最大の差 {worst:.1e} km ≤ {REPRO_TOL_KM})  PASS")
D = pd.DataFrame(ROWS, columns=["origin_time", "mj", "depth_km", "n_sta_t2", "variant", "tau", "method", "err_km"])
D.to_csv(ROOT / f"data/23_01_per_event{SUF}.csv", index=False, float_format="%.4f")

# ---------------------------------------------------------------- 集計(全て記述)
RB = np.random.default_rng(AUDIT_SEED)
def stats(x):
    x = np.asarray(x, float); av = float(np.mean(np.isfinite(x))) if len(x) else 0.0; x = x[np.isfinite(x)]
    if len(x) == 0: return dict(n=0, available=av, median_km=None, ci_lo=None, ci_hi=None, frac_gt10=None)
    bs = np.median(x[RB.integers(0, len(x), (AUDIT_NBOOT, len(x)))], axis=1)
    return dict(n=int(len(x)), available=av, median_km=float(np.median(x)), ci_lo=float(np.percentile(bs, 2.5)),
                ci_hi=float(np.percentile(bs, 97.5)), frac_gt10=float(np.mean(x > FAR_KM)))
def paired(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float); m = np.isfinite(x) & np.isfinite(y); nz = int(np.sum(x[m] != y[m]))
    d = dict(n=int(m.sum()), n_nonzero=nz, median_diff_km=None, frac_better=None, p_one_sided=None)
    if m.sum() == 0: return d
    d.update(median_diff_km=float(np.median(x[m] - y[m])), frac_better=float(np.mean(x[m] < y[m])))
    if nz >= 6: d["p_one_sided"] = float(wilcoxon(x[m], y[m], alternative="less", zero_method="wilcox").pvalue)
    return d
W = D.pivot_table(index="origin_time", columns=["variant", "tau", "method"], values="err_km", aggfunc="first", dropna=False)
def col(v, t, m): return W[(v, t, m)].to_numpy(float) if (v, t, m) in W.columns else np.full(len(W), np.nan)
SUMM = {}
for t in REPRO_TAUS:
    vs = VNAMES if t in VTAUS else ["base"]
    for v in vs:
        ms = ["M5", "M6r", "C1", "C3", "C4"] if v == "base" else ["M6r", "C1", "C3", "C4"]
        SUMM[f"{v}|{t}"] = dict(methods={m: stats(col(v, t, m)) for m in ms},
                                C4_vs_M6r=paired(col(v, t, "C4"), col(v, t, "M6r")),
                                C4_vs_base_C4=(paired(col(v, t, "C4"), col("base", t, "C4")) if v != "base" else None))
RAND_MEAN = {}
for t in VTAUS:
    for sg in RAND_SIG_KM:
        meds = {m: [SUMM[f"rand{sg:g}_s{sd}|{t}"]["methods"][m]["median_km"] for sd in RAND_SEEDS] for m in ("M6r", "C1", "C3", "C4")}
        RAND_MEAN[f"rand{sg:g}|{t}"] = {m: dict(mean=float(np.mean(v_)), min=float(np.min(v_)), max=float(np.max(v_))) for m, v_ in meds.items()}
# ① 層別(基準の値)
B = D[D.variant == "base"].pivot_table(index=["origin_time", "mj", "depth_km", "n_sta_t2"], columns=["tau", "method"], values="err_km", aggfunc="first").reset_index()
B.columns = ["_".join(c).strip("_") if isinstance(c, tuple) else c for c in B.columns]
zq = np.quantile(B["depth_km"], [1/3, 2/3]) if len(B) >= 3 else np.array([np.inf, np.inf])
GROUPS = {"Mj 1.5-1.6": B["mj"].round(1) <= 1.6, "Mj 1.7-1.8": B["mj"].round(1).between(1.7, 1.8), "Mj 1.9": B["mj"].round(1) >= 1.9,
          f"depth <= {zq[0]:.2f} km": B["depth_km"] <= zq[0], f"depth {zq[0]:.2f}-{zq[1]:.2f} km": (B["depth_km"] > zq[0]) & (B["depth_km"] <= zq[1]),
          f"depth > {zq[1]:.2f} km": B["depth_km"] > zq[1],
          "1 P station at 2 s": B["n_sta_t2"] == 1, "2 P stations at 2 s": B["n_sta_t2"] == 2, "3 P stations at 2 s": B["n_sta_t2"] == 3,
          ">= 4 P stations at 2 s": B["n_sta_t2"] >= 4}
STRATA = {}
for t in VTAUS:
    for g, msk in GROUPS.items():
        sub = B[msk.to_numpy()]
        STRATA[f"{g}|{t}"] = dict(n=int(len(sub)), **{m: (float(np.nanmedian(sub[f"{t}_{m}"])) if len(sub) else None) for m in ("M6r", "C1", "C3", "C4")},
                                  C4_gt10=(float(np.mean(sub[f"{t}_C4"] > FAR_KM)) if len(sub) else None),
                                  C4_better_than_M6r=(float(np.mean(sub[f"{t}_C4"] < sub[f"{t}_M6r"])) if len(sub) else None))

def f2(v): return "  —  " if v is None else f"{v:5.2f}"
print(f"\n[23_01] ===== 水平誤差の中央値 km({len(EVAL)} 地震、全て記述) =====")
for t in VTAUS:
    print(f"  τ = {t} s        M6r    C1    C3    C4   C4<M6r の割合  C4 の 10 km 超  C1 の値がある割合")
    for v in VNAMES:
        s = SUMM[f"{v}|{t}"]; mm = s["methods"]; c = s["C4_vs_M6r"]
        print(f"  {v:<14} " + " ".join(f2(mm[m]["median_km"]) for m in ("M6r", "C1", "C3", "C4"))
              + f"   {0 if c['frac_better'] is None else c['frac_better']:.2f}          {0 if mm['C4']['frac_gt10'] is None else mm['C4']['frac_gt10']:.3f}"
              + f"          {mm['C1']['available']:.2f}")
    print(f"  参考: 物理だけ M5(記憶を使わない、基準)の中央値 {f2(SUMM[f'base|{t}']['methods']['M5']['median_km'])} km"
          f"(値がある割合 {SUMM[f'base|{t}']['methods']['M5']['available']:.2f})")
print(f"\n[23_01] ===== ① 層別(基準、中央値 km) =====")
for t in VTAUS:
    print(f"  τ = {t} s")
    for g in GROUPS:
        s = STRATA[f"{g}|{t}"]
        print(f"    {g:<24} n={s['n']:>3}  M6r {f2(s['M6r'])}  C1 {f2(s['C1'])}  C3 {f2(s['C3'])}  C4 {f2(s['C4'])}  "
              f"C4 の 10 km 超 {0 if s['C4_gt10'] is None else s['C4_gt10']:.3f}  C4<M6r {0 if s['C4_better_than_M6r'] is None else s['C4_better_than_M6r']:.2f}")
LIM = ["descriptive only: the 21_04 test was opened once on 2026-10-30; nothing here changes its verdict, rules or cache",
       "truth is still the JMA epicentre; hold-out uses the JMA epicentres to decide which past events to remove",
       "perturbations move only the horizontal positions of past events used as memory (C1 answer, C3/M6r prior, C4 station terms); "
       "velocity, static station terms, KDE bandwidth and grid were fitted on pool events with JMA locations and are kept fixed",
       "depth error is not available (21_04 does not keep estimated depths); depth strata are by JMA depth of the target",
       "test events are 1.5 <= Mj < 2.0 only, so magnitude strata are narrow",
       "21_04 limits apply unchanged (offline PhaseNet picks, up to 24 stations, no latency, one sequence)"]

def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, np.ndarray): return [clean(v) for v in o.tolist()]
    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
json.dump(clean(dict(plan=plan, gates=dict(repro=dict(status="PASS", max_abs_diff_km=worst, tol_km=REPRO_TOL_KM)),
                     summary=SUMM, rand_mean_over_seeds=RAND_MEAN, strata=STRATA, limits=LIM, runtime_s=time.time() - T0)),
          open(ROOT / f"models/23_01_summary{SUF}.json", "w"), indent=1)

# ---------------------------------------------------------------- 図(白背景・英語・凡例は枠外)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 10})
from matplotlib.ticker import FuncFormatter, NullFormatter
def plain_log(ax):
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}")); ax.yaxis.set_minor_formatter(NullFormatter())
CLR = {"M6r": ("tab:blue", "Best physics (M6r)"), "C1": ("tab:green", "C1 (most similar event's location)"),
       "C3": ("tab:red", "C3 (physics x similar-event prior)"), "C4": ("tab:pink", "C4 (C3 + station terms)")}
def med(v, t, m): return SUMM[f"{v}|{t}"]["methods"][m]["median_km"]
fig, axs = plt.subplots(1, len(VTAUS), figsize=(10.5, 4.2), sharey=True)
xr = [0.0] + HOLD_R_KM
for ax, t in zip(np.atleast_1d(axs), VTAUS):
    for m, (c, lab) in CLR.items():
        ys = [med("base", t, m)] + [med(f"hold{r:g}", t, m) for r in HOLD_R_KM]
        ax.plot(xr, [np.nan if y is None else y for y in ys], "-o", color=c, label=lab, lw=1.8 if m == "C4" else 1.2)
    m5 = med("base", t, "M5")
    if m5 is not None: ax.axhline(m5, color="0.4", ls=":", lw=1.0, label="Physics only, no memory (M5, reference)")
    ax.set_title(f"tau = {t} s", fontsize=10); ax.set_xlabel("Past events removed within R km of the target (km)")
    ax.set_xticks(xr); ax.grid(alpha=0.3); ax.set_yscale("log"); plain_log(ax)
np.atleast_1d(axs)[0].set_ylabel("Median epicentral error vs JMA (km)")
h_, l_ = np.atleast_1d(axs)[0].get_legend_handles_labels()
fig.suptitle(f"Central Tottori 2016, {len(EVAL)} events: spatial hold-out of memory (descriptive)", fontsize=11)
fig.legend(h_, l_, loc="lower center", bbox_to_anchor=(0.5, -0.10), ncol=3, fontsize=8, frameon=False)
fig.tight_layout(rect=(0, 0.04, 1, 0.95)); fig.savefig(ROOT / f"PDF/23_01_F1_holdout{SUF}.pdf", bbox_inches="tight"); plt.close(fig)

fig, axs = plt.subplots(2, len(VTAUS), figsize=(10.5, 7.6), sharey="row")
for j, t in enumerate(VTAUS):
    ax = axs[0, j]; xs = [0.0] + RAND_SIG_KM
    for m, (c, lab) in CLR.items():
        mean = [med("base", t, m)] + [RAND_MEAN[f"rand{s:g}|{t}"][m]["mean"] for s in RAND_SIG_KM]
        lo = [0.0] + [RAND_MEAN[f"rand{s:g}|{t}"][m]["mean"] - RAND_MEAN[f"rand{s:g}|{t}"][m]["min"] for s in RAND_SIG_KM]
        hi = [0.0] + [RAND_MEAN[f"rand{s:g}|{t}"][m]["max"] - RAND_MEAN[f"rand{s:g}|{t}"][m]["mean"] for s in RAND_SIG_KM]
        ax.errorbar(xs, mean, yerr=[lo, hi], fmt="-o", color=c, capsize=3, label=lab, lw=1.8 if m == "C4" else 1.2)
    ax.set_title(f"(a) Random memory errors, tau = {t} s", fontsize=10); ax.set_xlabel("Sigma of horizontal error added to past events (km)")
    ax.set_xticks(xs); ax.grid(alpha=0.3)
    ax = axs[1, j]; xs = [0.0] + SHIFT_E_KM
    for m, (c, lab) in CLR.items():
        ys = [med("base", t, m)] + [med(f"shiftE{d:g}", t, m) for d in SHIFT_E_KM]
        ax.plot(xs, [np.nan if y is None else y for y in ys], "-o", color=c, label=lab, lw=1.8 if m == "C4" else 1.2)
    ax.plot(xs, xs, color="0.5", ls="--", lw=0.8, label="Error = shift (follows memory exactly)")
    ax.set_title(f"(b) Common eastward shift of all past events, tau = {t} s", fontsize=10)
    ax.set_xlabel("Shift of past events (km)"); ax.set_xticks(xs); ax.grid(alpha=0.3)
for r in range(2): axs[r, 0].set_ylabel("Median epicentral error vs JMA (km)")
h0, l0 = axs[1, 0].get_legend_handles_labels()
fig.suptitle(f"Central Tottori 2016, {len(EVAL)} events: sensitivity to memory positions (truth unchanged; descriptive)\n"
             "(a) error bars = min-max over 3 random seeds", fontsize=11)
fig.legend(h0, l0, loc="lower center", bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=8, frameon=False)
fig.tight_layout(rect=(0, 0.03, 1, 0.94)); fig.savefig(ROOT / f"PDF/23_01_F2_perturb{SUF}.pdf", bbox_inches="tight"); plt.close(fig)

fig, axs = plt.subplots(1, len(VTAUS), figsize=(11.5, 4.6), sharey=True)
gl = list(GROUPS); xg = np.arange(len(gl)); wbar = 0.2
for ax, t in zip(np.atleast_1d(axs), VTAUS):
    for k, (m, (c, lab)) in enumerate(CLR.items()):
        ax.bar(xg + (k - 1.5) * wbar, [np.nan if STRATA[f"{g}|{t}"][m] is None else STRATA[f"{g}|{t}"][m] for g in gl], wbar, color=c, label=lab)
    ax.set_xticks(xg); ax.set_xticklabels([f"{g}\n(n={STRATA[f'{g}|{t}']['n']})" for g in gl], rotation=60, ha="right", fontsize=7)
    ax.set_title(f"tau = {t} s", fontsize=10); ax.grid(alpha=0.3, axis="y"); ax.set_yscale("log"); plain_log(ax)
np.atleast_1d(axs)[0].set_ylabel("Median epicentral error vs JMA (km)")
h_, l_ = np.atleast_1d(axs)[0].get_legend_handles_labels()
fig.suptitle(f"Central Tottori 2016, {len(EVAL)} events: errors by magnitude, JMA depth and number of P stations (descriptive)", fontsize=11)
fig.legend(h_, l_, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=4, fontsize=8, frameon=False)
fig.tight_layout(rect=(0, 0.04, 1, 0.95)); fig.savefig(ROOT / f"PDF/23_01_F3_strata{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
print(f"\n[23_01] 限界: " + " / ".join(LIM))
print(f"[23_01] 出力: models/23_01_plan{SUF}.json, models/23_01_summary{SUF}.json, data/23_01_per_event{SUF}.csv, "
      f"PDF/23_01_F1_holdout{SUF}.pdf, PDF/23_01_F2_perturb{SUF}.pdf, PDF/23_01_F3_strata{SUF}.pdf  ({time.time()-T0:.0f} s)")
print("exit code: 0 になれば完走")
