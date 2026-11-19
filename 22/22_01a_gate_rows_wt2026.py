#!/usr/bin/env python3
# =============================================================================
# Script : 22_01a_gate_rows_wt2026.py  (v1)
#          [信頼の切り替え(22)の学習の行を作る: 鳥取県西部 2026 の全ての地震 × 4 時点で、物理の最良(M6r)・C1・C2・C3・C4 の
#           位置と誤差、そして「物理(C4)と記憶(C1)のどちらを信じるか」を決める AI に渡す 13 の手がかりを書き出す]
# Project: ARGUS(新生)— AI を「物理の部品」として使う。22 では AI が「どちらの答えを信じるか」を決める(事前登録 22_00)
#
# なぜ必要か:
#   鳥取県中部 2016 の記述(21_17)で、C4(物理 + 似た地震 + 局補正)が 10 km 超外れた地震は全て、C1(最も似た過去の地震の位置)と
#   大きく食い違っていた。しかし「10 km 以上食い違えば C1」という規則は 2016 を見て決めた後付けで、確かめにならない。
#   そこで「どちらを信じるか」を、正解を使わない手がかりから AI(ロジスティック回帰)に学習させ、凍結してから、開いていない
#   大阪府北部 2018 で 1 回だけ試す。本スクリプトはその学習の材料(行)を作る。学習と凍結は 22_02。
#
# 何をするか:
#   1. 21_06a v1 の 1〜7 節(入力・座標と検測・速度と局の補正・格子と探索・事前分布と C4 の材料・波形の似ている度合い・速い S)を
#      計算は 1 字も変えずに写す(違うのは画面の表示の文・版の注記・--dev を --quick にした所と a.dev = False の 1 行だけ。
#      写しの中の dev の分かれ道は使われない)。
#      したがって M6r・C1〜C4 の計算は 21_02・21_06a と同じ。
#   2. 測った P がある全ての地震(過去の地震の一覧が空でないもの)× τ(0.5・1・2・3 s)で、M6r・C1・C2・C3・C4 を出す
#      (21_06a の 9 節と同じ呼び方: m3 = prior_members、M6r = locate_map(pk, m3)、S = similarity_fast、c_from)。
#   3. G-same: 21_02 の試験の 91 地震(data/21_02_per_event.csv)を最初に計算し、C1・C3・C4・M6r の誤差が 4 時点とも 6e-5 km 以内で
#      一致しなければ、その場で STOP(何時間も回した後で止まらないように)。4 つの列が CSV に無い時も、照合した行が 91 × 4 と
#      違う時も STOP。各地震の行はその地震より前の地震だけから作るので、計算の順番は結果に影響しない(保存の前に時刻の順に並べ直す)。
#   4. 22 GATE FEATURES(印の間。22_01b・22_04 と 1 字も違わない。SHA-256 を記録し、後で照合する)で 13 の手がかりを作る。
#      正解(目標の地震の気象庁の震源・Mj)は使わない。印の間に SRC[・MAG[・EX[ie]・EY[ie]・OTNS[・RES[・EVS[・OT[・src_loc・TFIRST[
#      が無いことを文字で確かめる(G-leak。印の間から呼ぶ corr_from・tt は 21_06a の写しで、目標の地震を含まない過去の一覧だけを読む)。
#        1 log1p(C4 と C1 の距離 km)            2 log1p(C4 と M6r の距離 km)        3 log1p(C1 と C2 の距離 km)
#        4 log1p(上位 10 の位置の、その中央 C2 からの距離の中央値 km)                5 S_max(最も似た地震の S)
#        6 S_max − 2 番目の S                    7 log1p(S > 0 の候補の数)           8 τ までに P が届いた局の数
#        9 C4 の位置での P の残り(局の補正 + C4 の補正を引き、中央値を引いた絶対値の中央値 s。深さは 0〜ZMAX km を 1 km 刻みで
#          調べて最も小さい値。P が 3 局未満なら値なし)
#       10 C4 の解が探索範囲の端(水平で |x| か |y| ≥ H − 粗い格子 1 つ分)にあるか(0/1)
#       11 C4 で補正した局の数                  12 τ                                 13 log1p(C4 から最も近い過去の地震(1 時間以上前)まで km)
#   5. 行を data/22_01a_rows_wt2026.npz に保存し、SHA-256 を表示する(目で見る用に、丸めた写しの CSV も書く。22_02 は npz を読む)。
#      S > 0 の候補が 5 未満の行(C1 が無く、C3 = C4 = M6r に戻る行)も「fb = 1」として残す(22_02 は学習から除き、G は C4 を返す)。
#   6. 記述(判定しない): τ ごとに、C1 がある行での C4・C1・M6r・規則 R(C4 と C1 が 10 km 以上食い違えば C1)の中央値と
#      10 km 超の割合、C1 の方が近い行の割合。
#
# 限界:
#   - 21_06a と同じ(1 つの系列・気象庁の震源が正解・オフラインの PhaseNet の検測・遅れなし)
#   - 2026 の評価の 91 地震は 21_02 で既に開いた。学習の行には全ての地震が入る(22_00 1.4)
#   - 手がかり 9 の深さの探し方は、位置の探索とは別の簡単な 1 次元の探索(C4 の当てはまりの目安として使うだけ)
#
# Usage : cd ~/SWIFT && caffeinate -i uv run python src/22_01a_gate_rows_wt2026.py --quick   (動作確認。最初の 10 地震で G-same)
#         cd ~/SWIFT && caffeinate -i uv run python src/22_01a_gate_rows_wt2026.py           (本番。全ての地震、時間がかかる)
# 入力  : 21_06a と同じキャッシュと正本、data/21_02_per_event.csv、models/21_02_judgment.json(あれば SHA を照合)
# Output: data/22_01a_rows_wt2026.npz / data/22_01a_rows_wt2026.csv / models/22_01a_rows.json(--quick では全て _quick 付き)
# 止める条件(STOP): 21_06a と同じもの(入力・G-fresh・G-split・G-lib など)・比べる CSV が無いか地震か列が合わない・
#                   G-same が合わない(照合した行の数が違う時も)・G-leak・キャッシュの SHA-256 が 21_02 と違う
# 時間の目安: --quick の 10 地震(最も遅い、後の方の地震)にかかった時間 × 全ての地震の数 ÷ 10 が上限の目安
# =============================================================================
import json, argparse, time, csv, hashlib, math, warnings, datetime as dt
from pathlib import Path
import numpy as np
import torch
from scipy.signal import butter, sosfilt
from scipy.stats import wilcoxon
warnings.filterwarnings("ignore", message="All-NaN slice")

ap = argparse.ArgumentParser()
ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_m15.pt", help="15_01c v3.2 の M>=1.5 版")
ap.add_argument("--canon", default="data/tottori_processed/tottori_parsed_realpick.pt", help="18_01・21_01 で使った正本(M>=2.0)")
ap.add_argument("--expect-canon", type=int, default=198)
ap.add_argument("--quick", action="store_true", help="動作確認: 21_02 の試験の最初の 10 地震だけ行を作り G-same を確かめる(出力に _quick)")
a = ap.parse_args()
a.dev = False          # 22_01a は 21_02 の dev を使わない(21_06a の写しの中の a.dev を全て「本番」側にする)

# ---------------------------------------------------------------- 事前に固定した値(変えたら版を上げる)
VERSION = "v1"                             # 22_01a の版(下の値は全て 21_06a v1 と同じ)
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
MAIN_UTC = dt.datetime(2026, 1, 6, 1, 18, 48, 490000)
LIMITS = ["Tottori was used in ARGUS development; the test events are fresh only with respect to 18_01 and 21_01",
          "one aftershock sequence; the test events (1.5 <= Mj < 2.0, not in the 198-event canon) were never used by 18_01 or 21_01, "
          "but the hypotheses (tau = 2 s, the C4 arm) were chosen after seeing 21_01 on other events of the same sequence; "
          "an untouched second sequence is still needed",
          "the M>=1.5 cache was built by 15_01c v3.2 (same picking/QC code as the canon, output name only changed); its dataset-wide "
          "amplitude factor differs from the canon, which does not affect cosine similarity or travel times",
          "past-event locations are JMA hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
          "offline PhaseNet picks on full records (possibly better than real-time picks); every method uses the same picks",
          "cache keeps up to 24 stations per event (PhaseNet P first, earliest first); no not-yet-arrived information is used",
          "cache waveforms had the full-window mean removed (includes future samples; removed by the 2 Hz high-pass except for a "
          "transient from the window start 3 s before P) and the source h5 is z-score normalised per 30-s window (the scale uses later "
          "samples of that window; cosine similarity is scale-invariant except where a window join falls inside the correlation window); "
          "the one-sample look-ahead of the cache's central-difference derivative is avoided by not using the last sample",
          "no picking or telemetry latency (tau is ideal elapsed time)",
          "the test events are small (1.5 <= Mj < 2.0); pick quality and station counts can differ from Mj >= 2.0 events",
          "the 2-8 Hz band was chosen after seeing 18_01 on the 198 canon events of the same sequence",
          "the pool now includes 1.5 <= Mj < 2.0 events, so calibration and all medians differ from 21_01 and are not directly comparable",
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
print(f"[22_01a] 本スクリプト(22_01a){VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
      f"モード: {'quick(21_02 の試験の最初の 10 地震だけ、出力に _quick)' if a.quick else '本番(全ての地震の行を作る)'}")

# ---------------------------------------------------------------- 1. 入力
CP = ROOT / a.cache
if not CP.exists(): raise SystemExit(f"[22_01a] STOP: {a.cache} が無い(15_01c v3.2 を --min-mag 1.5 --tag _m15 で作り、data/tottori_processed/ に置く)")
EVS = torch.load(CP, map_location="cpu", weights_only=False)
need = ["origin_time", "src_loc", "mw", "waveforms", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
for e in EVS:
    miss = [k for k in need if k not in e]
    if miss: raise SystemExit(f"[22_01a] STOP: キャッシュの地震に {miss} が無い(15_01c v3.2 の出力か確かめる)")
for e in EVS:
    w_ = np.asarray(e["waveforms"])
    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[22_01a] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[22_01a] STOP: {e['origin_time']} の波形に NaN か無限大")
def to_ns(o):
    import pandas as pd
    try:
        t = pd.Timestamp(str(o).replace("Z", "+00:00"))
        t = t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t
        return int(t.value)
    except Exception:
        raise SystemExit(f"[22_01a] STOP: origin_time {o!r} を時刻として読めない")
OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
order = np.argsort(OTNS, kind="stable"); EVS = [EVS[i] for i in order]; OTNS = OTNS[order]
NE = len(EVS)
SRC = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS])
MAG = np.array([float(e["mw"]) for e in EVS])
OT = [str(e["origin_time"]) for e in EVS]
if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
    raise SystemExit("[22_01a] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[22_01a] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
CANP = ROOT / a.canon
if not CANP.exists(): raise SystemExit(f"[22_01a] STOP: 正本 {a.canon} が無い(使っていない地震を見分けるのに要る)")
CAN = torch.load(CANP, map_location="cpu", weights_only=False)
if len(CAN) != a.expect_canon: raise SystemExit(f"[22_01a] STOP: 正本の地震の数 {len(CAN)} が {a.expect_canon} と違う")
CAN_NS = np.sort(np.array([to_ns(e["origin_time"]) for e in CAN]))
def near_canon(t):
    k = np.searchsorted(CAN_NS, t); return any(0 <= q < len(CAN_NS) and abs(CAN_NS[q] - t) <= MATCH_S * 1e9 for q in (k - 1, k))
IN_CANON = np.array([near_canon(t) for t in OTNS])
FRESH = (MAG < FRESH_MAX_MAG - 1e-6) & ~IN_CANON
n_can_found = int(sum(1 for t in CAN_NS if np.min(np.abs(OTNS - t)) <= MATCH_S * 1e9))
n_extra2 = int(((MAG >= FRESH_MAX_MAG - 1e-6) & ~IN_CANON).sum())
# 同じ作り方かの確認: 正本と時刻が合う地震で、局の数・P の時刻(0.01 s 以内)・Mj・震源が同じ割合
same = []
for e in CAN:
    t = to_ns(e["origin_time"]); k = int(np.argmin(np.abs(OTNS - t)))
    if abs(OTNS[k] - t) > MATCH_S * 1e9: continue
    f = EVS[k]; n1, n2 = int(e["n_real_stations"]), int(f["n_real_stations"])
    ok = (n1 == n2 and abs(float(e["mw"]) - float(f["mw"])) < 1e-6
          and np.allclose(np.asarray(e["sta_locs"], float)[:n1], np.asarray(f["sta_locs"], float)[:n2], atol=1e-6)
          and np.allclose(np.asarray(e["src_loc"], float)[:3], np.asarray(f["src_loc"], float)[:3], atol=1e-4)
          and np.allclose(np.asarray(e["tp_times"], float)[:n1], np.asarray(f["tp_times"], float)[:n2], atol=0.01, equal_nan=True))
    same.append(ok)
same_frac = float(np.mean(same)) if same else 0.0
CANON_SHA = sha256(CANP)
ref21 = ROOT / "models/21_01_judgment.json"
ref_sha = json.load(open(ref21)).get("cache_sha256") if ref21.exists() else None
print(f"[22_01a] 入力: M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。正本 {len(CAN)} 地震のうち M ≥ 1.5 版に見つかった数 "
      f"{n_can_found}、そのうち局の数・P の時刻・Mj・震源が同じ割合 {same_frac:.3f}。Mj ≥ 2.0 で正本に無い地震 {n_extra2}"
      f"(同じ作り方なら 0 のはず。試験には使わず、過去の地震の一覧には入れる)。使っていない地震(Mj < 2.0 かつ正本に無い){int(FRESH.sum())}")
print(f"[22_01a] 正本の SHA-256 {CANON_SHA[:12]}…  21_01 が使ったキャッシュの SHA-256 "
      + (f"{ref_sha[:12]}…" if ref_sha else "(models/21_01_judgment.json が無いので照合を飛ばした)"))
if ref_sha is not None and ref_sha != CANON_SHA: raise SystemExit("[22_01a] STOP(G-fresh): 正本が 21_01 で使ったキャッシュと違う")
if n_can_found < 0.9 * len(CAN) or same_frac < 0.9:
    raise SystemExit("[22_01a] STOP(G-fresh): 正本の地震のうち M ≥ 1.5 版に見つかったのが 9 割未満、または中身が同じ割合が 9 割未満"
                     "(作り方が違う可能性。この行を貼って相談)")
if n_can_found < len(CAN) or n_extra2 > 0 or same_frac < 1.0:
    print("[22_01a] 注意(G-fresh): 正本と M ≥ 1.5 版が完全には一致していない(上の数を貼ってください。試験の地震は Mj < 2.0 かつ正本に無い地震だけなので、"
          "正本の地震が試験に入ることはない)")
del CAN
im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
    raise SystemExit(f"[22_01a] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj 6.4・2026-01-06 01:18:48 UTC)")
CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
pool_idx = np.where(OTNS <= CUT_NS)[0]; test_idx = np.where((OTNS > CUT_NS) & FRESH)[0]
if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
    raise SystemExit("[22_01a] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
print(f"[22_01a] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
print(f"[22_01a] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
      f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")

# ---------------------------------------------------------------- 2. 座標・検測(17_02 と同じ)
TFIRST = np.full(NE, np.nan)          # PhaseNet で測った最も早い P(気象庁の発生時刻からの s)
skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
for ie, e in enumerate(EVS):
    n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    ok = np.isfinite(tp) & (pf == 0)
    if ok.any(): TFIRST[ie] = float(tp[ok].min())
    kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
    if len(set(kk)) != n: raise SystemExit(f"[22_01a] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
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
print(f"[22_01a] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
if len(EVAL) == 0: raise SystemExit("[22_01a] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
if a.dev: print(f"[22_01a] dev: pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                "(較正にも入っているので値は楽観的)")

SUF = "_quick" if a.quick else ""
def stop(msg): raise SystemExit(msg)

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
print(f"[22_01a] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
      f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")

# ---------------------------------------------------------------- 4. 格子と探索(17_02 と同じ)
H = float(max(30.0, np.percentile(np.abs(np.r_[EX[CAL], EY[CAL]]), 99.5) + 30.0))
STEP = float(max(1.0, round(H / 30.0)))
ZMAX = float(max(30.0, np.percentile(SRC[CAL, 2], 99.5) * 1.3 + 10.0))
ZDEF = float(np.mean(SRC[CAL, 2]))
xc = np.arange(-H, H + 1e-6, STEP); zc = np.arange(0.0, ZMAX + 1e-6, STEP)
GX, GY, GZ = np.meshgrid(xc, xc, zc, indexing="ij"); COARSE = np.c_[GX.ravel(), GY.ravel(), GZ.ravel()]
XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
print(f"[22_01a] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
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
print(f"[22_01a] KDE の帯域(pool の一つ抜き): {KDE_H} km")
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
    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[22_01a] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
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
    if ie is not None and ie in top: stop("[22_01a] STOP: 自分自身が似た地震の上位に入っている")
    out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
               C3=locate_map(pk, top), C4=None, fb=False, top1=int(top[0]), top=top, ncorr=0)
    if with_c4:
        dP, dS = corr_from(top, pk)
        out["C4"] = locate_map(pk, top, dP, dS); out["ncorr"] = len(dP)
    return out


# ---------------------------------------------------------------- 7. 速い S_ij(21_05 で足した部分。式は similarity と同じ)
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

# ---------------------------------------------------------------- 8. 照合の準備(22_01a で足した部分)
import re, sys, platform
FB = open(Path(__file__), encoding="utf-8").read()
GBLK = FB[FB.index("# >>> 22 GATE FEATURES BEGIN"):FB.index("# <<< 22 GATE FEATURES END")]
GATE_SHA = hashlib.sha256(GBLK.encode()).hexdigest()
leak = re.findall(r"SRC\s*\[|MAG\s*\[|E[XY]\s*\[\s*ie\s*\]|OTNS\s*\[|RES\s*\[|EVS\s*\[|\bOT\s*\[|src_loc|TFIRST\s*\[", GBLK)
if leak: raise SystemExit(f"[22_01a] STOP(G-leak): 手がかりの部分に正解か目標の地震の値を読む所がある {sorted(set(leak))}")
print(f"[22_01a] 手がかりの部分の SHA-256 {GATE_SHA[:12]}…  G-leak(印の間に SRC[・MAG[・EX[ie]・EY[ie]・OTNS[・RES[・EVS[・OT[・src_loc・TFIRST[ が無い): PASS"
      "(印の間から呼ぶ corr_from・tt は 21_06a の写しで、目標の地震を含まない過去の一覧の上位だけを読む)")
REFCSV = ROOT / "data/21_02_per_event.csv"
if not REFCSV.exists(): raise SystemExit("[22_01a] STOP: 比べる data/21_02_per_event.csv が無い(21_02 の出力)")
ref = {r["origin_time"]: r for r in csv.DictReader(open(REFCSV))}
if sorted(ref) != sorted(OT[ie] for ie in EVAL):
    raise SystemExit(f"[22_01a] STOP: 21_02_per_event.csv の地震({len(ref)})が 21_02 の試験の地震({len(EVAL)})と一致しない")
REF_COLS = next(iter(ref.values())).keys()
CHK = ["C3", "C4", "M6r", "C1"]
miss_cols = [f"{m}_err_t{t:g}" for m in CHK for t in TAUS if f"{m}_err_t{t:g}" not in REF_COLS]
if miss_cols: raise SystemExit(f"[22_01a] STOP(G-same): 21_02_per_event.csv に照合する列が無い {miss_cols[:4]}(22_00 の 3 節は C4・C1・M6r の照合を求める)")
print(f"[22_01a] G-same で照合する方法: {', '.join(CHK)}(4 時点とも)")
J02 = ROOT / "models/21_02_judgment.json"
if J02.exists():
    j = json.load(open(J02))
    if not j.get("cache_sha256"): print("[22_01a] 注意: models/21_02_judgment.json に cache_sha256 が無いので、キャッシュの SHA-256 の照合は飛ばした")
    elif j["cache_sha256"] != sha256(CP): raise SystemExit("[22_01a] STOP: キャッシュの SHA-256 が 21_02 の本番と違う")
    else: print("[22_01a] キャッシュの SHA-256 は 21_02 の本番と同じ")
else:
    print("[22_01a] 注意: models/21_02_judgment.json が無いので、キャッシュの SHA-256 の照合は飛ばした")

# ---------------------------------------------------------------- 9. 全ての地震 × 4 時点の行
ALLP = np.where(HASP)[0]
EVSET = set(int(i) for i in EVAL); POOLSET = set(int(i) for i in pool_idx)
# 21_02 の試験の地震(G-same で照合する地震)を先に計算し、合わなければその場で止める(何時間も回した後で止まらないように)。
# 各地震の行は、その地震より前の地震だけから作るので、計算の順番は結果に影響しない(保存の前に時刻の順に並べ直す)
TARGETS = [int(i) for i in EVAL[:10]] if a.quick else [int(i) for i in EVAL] + [int(i) for i in ALLP if int(i) not in EVSET]
t0 = time.time()
bank = Bank(BAND, ALLP)
print(f"[22_01a] 遅い層の準備({len(ALLP)} 地震、2–8 Hz): {time.time() - t0:.1f} s  行を作る地震 {len(TARGETS)} × {len(TAUS)} 時点")
TL4 = [f"{t:g}" for t in TAUS]
METH = ["M6r", "C1", "C2", "C3", "C4"]
R_ie, R_tau, R_fb, R_pool, R_eval, R_ni, R_npos = [], [], [], [], [], [], []
R_err = {m: [] for m in METH}; R_lat = {m: [] for m in METH}; R_lon = {m: [] for m in METH}; R_F = []
mism, nskip = [], 0
def err_of(pxy, ie):
    la, lo = to_ll(*pxy); return la, lo, km_between(la, lo, SRC[ie, 0], SRC[ie, 1])
t0 = time.time()
for ii, ie in enumerate(TARGETS):
    lib = library(ie)
    if len(lib) == 0: nskip += 1; continue
    p0 = FIRST[ie]; m3 = prior_members(lib, p0[0], (p0[1], p0[2]))
    for jt, t in enumerate(TAUS):
        pk = picks_of(ie, t); m6r = locate_map(pk, m3)
        S, ni = similarity_fast(ie, t, lib, BAND, bank)
        o = c_from(S, lib, pk, m3, m6r, TOPK, ie=ie)
        P = {"M6r": m6r, "C1": o["C1"], "C2": o["C2"], "C3": o["C3"], "C4": o["C4"]}
        for m in METH:
            if P[m] is None: R_lat[m].append(np.nan); R_lon[m].append(np.nan); R_err[m].append(np.nan); continue
            la, lo, ek = err_of(P[m], ie); R_lat[m].append(la); R_lon[m].append(lo); R_err[m].append(ek)
        if OT[ie] in ref:
            r = ref[OT[ie]]
            for m in CHK:
                v = r[f"{m}_err_t{TL4[jt]}"]; mine = R_err[m][-1]
                if (v == "") != (not np.isfinite(mine)) or (v != "" and abs(mine - float(v)) > 6e-5): mism.append((OT[ie], TL4[jt], m, v, f"{mine:.5f}"))
        R_F.append(np.full(len(GATE_FEATS), np.nan) if o["fb"] else gate_features(t, pk, o, m6r, S, lib))
        R_ie.append(ie); R_tau.append(t); R_fb.append(int(o["fb"])); R_pool.append(int(ie in POOLSET and ie not in EVSET))
        R_eval.append(int(ie in EVSET)); R_ni.append(ni); R_npos.append(int((S > 0).sum()))
    if mism: raise SystemExit(f"[22_01a] STOP(G-same): {OT[ie]} で 21_02 と同じ計算になっていない(地震, τ, 方法, CSV, ここ: {mism[:3]})。この行を貼って相談")
    if ii + 1 == len(EVSET) and not a.quick:
        print(f"[22_01a] G-same: 21_02 の試験の {len(EVSET)} 地震を全て照合して一致(残りの地震の行を作る)", flush=True)
    if (ii + 1) % 25 == 0 or ii + 1 == len(TARGETS):
        el = time.time() - t0
        print(f"  … {ii + 1}/{len(TARGETS)} 地震({el:.0f} s、残りの目安 {el / (ii + 1) * (len(TARGETS) - ii - 1) / 60:.0f} 分。"
              "後の地震ほど過去の一覧が長いので、初めの 91 地震の速さからの目安は多めに出る)", flush=True)
n_ref_rows = sum(1 for ie in R_ie if OT[ie] in ref)
n_ref_need = len(TAUS) * (10 if a.quick else len(EVSET))
G_SAME = "PASS" if not mism else f"FAIL ({len(mism)})"
print(f"[22_01a] G-same(21_02 の試験の地震 {n_ref_rows // len(TAUS)} 個 × 4 時点で、{', '.join(CHK)} の誤差が 21_02 の CSV と 6e-5 km 以内): {G_SAME}")
if mism: raise SystemExit(f"[22_01a] STOP(G-same): 21_02 と同じ計算になっていない(例 {mism[:3]})。この行を貼って相談")
if n_ref_rows != n_ref_need: raise SystemExit(f"[22_01a] STOP(G-same): 照合できた行 {n_ref_rows} が {n_ref_need} と違う(試験の地震の行が作られていない)")

# ---------------------------------------------------------------- 10. 保存
r4 = lambda x: np.round(np.asarray(x, float), 4)          # 21_02 の CSV と同じ小数 4 桁(同点を同点として扱う)
srt = np.lexsort((np.array(R_tau), np.array([OTNS[i] for i in R_ie])))       # 時刻の順・τ の順に並べ直す
R_ie, R_tau, R_fb, R_pool, R_eval, R_ni, R_npos = [[v[k] for k in srt] for v in (R_ie, R_tau, R_fb, R_pool, R_eval, R_ni, R_npos)]
R_F = [R_F[k] for k in srt]
for m in METH: R_err[m], R_lat[m], R_lon[m] = [R_err[m][k] for k in srt], [R_lat[m][k] for k in srt], [R_lon[m][k] for k in srt]
IE = np.array(R_ie, int)
OUT = dict(ie=IE, origin_time=np.array([OT[i] for i in IE]), tau=np.array(R_tau, float), fb=np.array(R_fb, int),
           is_pool=np.array(R_pool, int), is_eval=np.array(R_eval, int), n_i=np.array(R_ni, int), n_pos=np.array(R_npos, int),
           mj=MAG[IE], true_lat=SRC[IE, 0], true_lon=SRC[IE, 1], true_dep=SRC[IE, 2], X=np.array(R_F, float), feats=np.array(GATE_FEATS))
for m in METH:
    OUT[f"err_{m}"] = r4(R_err[m]); OUT[f"lat_{m}"] = np.array(R_lat[m], float); OUT[f"lon_{m}"] = np.array(R_lon[m], float)
NPZ = ROOT / f"data/22_01a_rows_wt2026{SUF}.npz"
np.savez_compressed(NPZ, **OUT)
with open(ROOT / f"data/22_01a_rows_wt2026{SUF}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["origin_time", "tau", "fb", "is_pool", "is_eval", "n_i", "n_pos", "mj", "true_lat", "true_lon", "true_dep"]
               + [f"{q}_{m}" for m in METH for q in ("err", "lat", "lon")] + GATE_FEATS)
    for k in range(len(IE)):
        w.writerow([OUT["origin_time"][k], f"{OUT['tau'][k]:g}", OUT["fb"][k], OUT["is_pool"][k], OUT["is_eval"][k], OUT["n_i"][k],
                    OUT["n_pos"][k], f"{OUT['mj'][k]:.1f}", f"{OUT['true_lat'][k]:.4f}", f"{OUT['true_lon'][k]:.4f}", f"{OUT['true_dep'][k]:.2f}"]
                   + [("" if not np.isfinite(OUT[f"{q}_{m}"][k]) else f"{OUT[f'{q}_{m}'][k]:.4f}" if q == "err" else f"{OUT[f'{q}_{m}'][k]:.5f}")
                      for m in METH for q in ("err", "lat", "lon")]
                   + ["" if not np.isfinite(v) else f"{v:.6g}" for v in OUT["X"][k]])
NPZ_SHA = sha256(NPZ)
print(f"[22_01a] 行: {len(IE)}(C1 がある行 {int((OUT['fb'] == 0).sum())}、C1 が無い行 {int(OUT['fb'].sum())}、過去の地震が無く飛ばした地震 {nskip})")
print(f"[22_01a] 保存: {NPZ.relative_to(ROOT)}  SHA-256 {NPZ_SHA}")

# ---------------------------------------------------------------- 11. 記述(判定しない)
print("\n[22_01a] ===== 記述(C1 がある行。R = C4 と C1 が 10 km 以上食い違えば C1。2026 は R を決めた系列ではないが、評価の地震は 21_02 で開いた) =====")
DESC = {}
ok = OUT["fb"] == 0
dC = np.expm1(OUT["X"][:, 0])
eR = np.where(dC >= GATE_THR_KM, OUT["err_C1"], OUT["err_C4"])
for t in TAUS:
    m = ok & (OUT["tau"] == t)
    if not m.any(): continue
    d = dict(n=int(m.sum()), frac_C1_closer=float(np.mean(OUT["err_C1"][m] < OUT["err_C4"][m])),
             frac_switch=float(np.mean(dC[m] >= GATE_THR_KM)))
    for k, e in (("M6r", OUT["err_M6r"]), ("C4", OUT["err_C4"]), ("C1", OUT["err_C1"]), ("R", eR)):
        d[k] = dict(median_km=float(np.median(e[m])), gt10=float(np.mean(e[m] > 10)), gt30=float(np.mean(e[m] > 30)))
    DESC[f"{t:g}"] = d
    print(f"  τ={t:g} s  n={d['n']}  中央値 M6r {d['M6r']['median_km']:.2f} / C4 {d['C4']['median_km']:.2f} / C1 {d['C1']['median_km']:.2f} / "
          f"R {d['R']['median_km']:.2f} km   10 km 超 M6r {d['M6r']['gt10']:.1%} / C4 {d['C4']['gt10']:.1%} / C1 {d['C1']['gt10']:.1%} / "
          f"R {d['R']['gt10']:.1%}   C1 の方が近い {d['frac_C1_closer']:.1%}  R が C1 を選ぶ {d['frac_switch']:.1%}")
nanf = {f: int(np.isnan(OUT["X"][ok, i]).sum()) for i, f in enumerate(GATE_FEATS)}
print("[22_01a] 値なしの手がかり(C1 がある行で): " + ", ".join(f"{f} {v}" for f, v in nanf.items() if v) if any(nanf.values()) else
      "[22_01a] 値なしの手がかり: なし")
rec = dict(script="22_01a_gate_rows_wt2026.py", version=VERSION, script_sha256=SELF_SHA, mode=("quick" if a.quick else "full"),
           cache=a.cache, cache_sha256=sha256(CP), gate_feature_block_sha256=GATE_SHA, gate_feats=GATE_FEATS, g_same=G_SAME, g_same_methods=CHK,
           g_same_events=n_ref_rows // len(TAUS), rows_path=str(NPZ.relative_to(ROOT)), rows_sha256=NPZ_SHA, n_rows=int(len(IE)),
           n_rows_with_C1=int(ok.sum()), n_skipped_no_library=nskip, nan_features=nanf, describe=DESC, utc=utcnow(),
           numpy=np.__version__, python=platform.python_version(), runtime_s=time.time() - T0,
           limits=["one sequence (West Tottori 2026); truth and past locations are JMA hypocentres",
                   "the 91 evaluation events were opened in 21_02; all events with P picks are training rows (22_00 section 1.4)",
                   "feature 9 uses a separate 1-D depth scan at the C4 epicentre (a fit-quality proxy only)"])
JP = ROOT / f"models/22_01a_rows{SUF}.json"
json.dump(rec, open(JP, "w"), indent=1, ensure_ascii=False)
print(f"[22_01a] 記録: {JP.relative_to(ROOT)}  SHA-256 {sha256(JP)}  ({time.time() - T0:.0f} s)")
print("[22_01a] 次: " + ("問題なければ --quick を外して本番を回す" if a.quick else "この出力を貼る。次は 22_02(G の学習と凍結)"))
