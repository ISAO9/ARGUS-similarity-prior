#!/usr/bin/env python3
# =============================================================================
# Script : 21_02_tottori_similarity_confirmation.py  (v2)
#          [21_01 で有望だった「2 秒の時点の、波形が似た過去の地震 × 物理」を、18_01・21_01 で使っていない地震(1.5 ≤ Mj < 2.0)で
#           事前に決めた規則のとおり 1 回だけ確かめる。似た地震の通り道の補正を物理に足す新しい方法 C4 も同時に試す]
# Project: ARGUS(新生)— SSJ 2026(11/4)の付録「予備結果」用。締切 2026-10-30
#
# なぜ必要か:
#   21_01(Mj ≥ 2.0 の正本 198 地震、試験 42 地震)の判定は SIMILARITY-NO だった。ただし 2 秒の時点で C3 は 0.44 km、
#   物理の側の最良(M6r)は 0.58 km で、p = 0.017 と基準(0.01)に届かなかった。21_01 の試験の地震で設定を変えて
#   やり直すと後出しになるので、18_01 でも 21_01 でも一度も使っていない地震で、「2 秒の時点」に絞った仮説を確かめ直す。
#   さらに、似ている過去の地震は「同じ通り道を通った地震」なので、その地震の走時の残り(速度の式と局の補正で説明できない分)を
#   届いた局の補正に足せば、局が 3 つでも物理の誤差が減るはずだ、という新しい方法 C4 を同時に試す。
#   C3・C4 は学習(AI)ではなく、波形の照合と物理の組み合わせである。
#
# 何をするか(21_01 v3 と同じ部分は「21_01 と同じ」と書き、違う所だけを書く):
#   1. 入力:
#      - M ≥ 1.5 版のキャッシュ(15_01c v3.2 を --min-mag 1.5 --tag _m15 で作ったもの。data/tottori_processed/
#        tottori_parsed_realpick_m15.pt)。作り方(検測・QC・局の選び方)は正本と同じで、名前だけが違う。
#      - 正本(Mj ≥ 2.0、198 地震。data/tottori_processed/tottori_parsed_realpick.pt)。使っていない地震を見分けるためだけに読む。
#      - 使っていない地震 = Mj < 2.0 で、発生時刻が正本のどの地震とも 1 s 以内にない地震。
#        Mj ≥ 2.0 で正本に無い地震は試験に使わず、過去の地震の一覧にだけ入れる(15_01c は地震ごとに独立に作るので、
#        同じ作り方なら 0 のはず。0 でなければ数を表示する)。
#      - 同じ作り方かの確認(G-fresh): 正本の地震のうち M ≥ 1.5 版に時刻で見つかる割合と、見つかった地震で局の数・P の時刻
#        (0.01 s 以内)・Mj・震源が同じ割合を表示する。どちらかが 9 割未満なら STOP、完全に一致しなければ注意を表示する。
#        models/21_01_judgment.json があれば、その cache_sha256 と正本の SHA-256 が違う時も STOP(21_01 の正本でない)。
#      - M ≥ 1.5 版の地震の数は決め打ちせず、数と SHA-256 を表示・記録する(dev と本番で同じファイルかは SHA で照合する)
#      止める条件(STOP): 21_01 と同じもの(キャッシュが無い・鍵が足りない・波形の形・NaN・発生時刻・震源・本震・
#      座標の同じ局の重なり・G-split)に加えて、Mj が 1.5 未満の地震がある・正本が無いか 198 地震でない・G-fresh・
#      評価する地震が 0。21_01 の「地震の数が --expect-n でない」は、M ≥ 1.5 版の数が前もって分からないので外した
#   2. 分け方: pool = 本震から 72 時間までの全ての地震(本震より前の地震も含む。Mj を問わない)。試験 = 72 時間より後の、使っていない地震。
#      pool で決めるもの(座標の原点・速度・局の補正・b・KDE の帯域・格子・固定の深さ・M6p の事前分布)と決め方は 21_01 と同じ。
#      過去の地震の一覧は、全ての Mj の地震(測った P がある地震)から作る(21_01 と同じ規則、1 時間の空白)。
#   3. 時刻 τ・検測の使い方・AI を使わない比べる相手 9 つ(M0r・Mp10・M1・M2・M3r・M5・M5f・M6p・M6r)・波形の似ている度合い
#      (2–8 Hz の因果フィルタ、窓、±0.1 s、コサイン類似度、S_ij)・C1・C2・C3・感度(K = 5・20、4–16 Hz、0.1 時間)は
#      21_01 v3 と同じ。変えたのは、C4 のための引数を misfit・locate_map・c_from に足したこと(C4 以外では足す値が 0 なので、
#      他の方法の値は 21_01 と同じ計算になる)、G-causal を全ての τ で行うこと、表示名と出力の名前を 21_02 にしたことだけ。
#   4. 新しい方法 C4(C3 + 似た地震からの局の補正):
#      - 全ての地震 j について、局ごとの P の走時の残り r_js = 観測の P の時刻(気象庁の発生時刻から)− 速度の式の走時
#        (気象庁の震源から)− pool で決めた P の局の補正。地震ごとに、その地震の P の残りの中央値を引く(気象庁の発生時刻の
#        誤差を消すため)。S も同じ(S を測った局だけ。式の走時 × Vp/Vs と S の局の補正を引き、P の中央値を引く)。
#        P を測っていない局(代替値)は使わない。
#      - 試験の地震 i の τ の時点で届いた局 s の補正 = C3 と同じ上位の似た地震のうち局 s の残りを持つ地震の、残りの中央値
#        (3 地震以上で持つ時だけ。無ければ補正なし)。この補正を pool の局の補正に足して、C3 と同じ式(M6r の式)で震源を決める。
#      - 使うのは過去の地震の残りだけ(試験の地震自身の気象庁の震源は使わない。自分が上位に入ったら STOP)。
#        S_ij > 0 の地震が 5 未満の時は C3 と同じく M6r の値。補正しない局は pool の局の補正だけのまま
#        (過去の地震の残りは、その地震の全ての局の P の中央値で揃えてある。届いた局だけで揃え直してはいない)。
#      - 記述: C4 と C3 の対応比較、C4 で補正した局の数、C4 = C3 になった割合。さらに全検測で、τ = 3 s の上位の似た地震を使った
#        C3all・C4all を出す。全検測でも C4all が物理(M5)より良ければ、その分は「早さ」ではなく「気象庁の震源の枠に合わせた」
#        効果の可能性があるので、H2 はそれと合わせて読む。
#   5. 判定(事前宣言。SSJ の付録の予備結果と、次の計画の判断にだけ使う。論文の主張ではない):
#      BEST(τ)・勝ちの規則(BEST の中央値より小さい・片側の対応 Wilcoxon・差が 0 でない組 10 以上・BEST が 0.5 km 以上)は
#      21_01 と同じ。仮説は次の 3 つだけ:
#        H1(主)  C3 @ τ = 2 s、p < 0.01
#        H2(副)  C4 @ τ = 2 s、p < 0.005
#        H3(副)  C3 @ τ = 0.5 s、p < 0.005(21_01 で −34%・p = 0.01 だった時点)
#      判定(H1 で決める): CONFIRMED = H1 が勝ち / PHYSICS-AT-FLOOR = τ = 2 s の BEST が 0.5 km 未満 /
#            NOT-CONFIRMED = それ以外 / INCONCLUSIVE = 評価できる試験の地震が 30 未満
#      H2・H3 は副の判定として別に書く(H1 の判定は変えない)。τ = 1・3 s と、全ての方法の値は記述だけ
#      (JSON の per_tau は記述だけで勝ち負けを持たない。勝ち負けは hypotheses に書く)。
#      評価できる試験の地震が 30 未満なら、計算せずに INCONCLUSIVE を記録して終わる。
#      ここで決めた計画の値(原典なし): 1.5 ≤ Mj < 2.0、正本との照合 1 s、9 割、C4 の最少 3 地震、副の α 0.005(2 つの副の仮説で
#      0.01 を分けた)。それ以外は 21_01 v3 の値をそのまま使う
#   6. 1 回だけ・dev・ゲート(G-split・G-lib・G-causal・G-phys)・出力の順番は 21_01 v3 と同じ。違いは:
#      - G-causal を τ = 0.5・1・2・3 s の全てで行い、C4 も比べる方法に含める
#      - dev は pool の最後の「使っていない地震」20 個を使う(較正にも入っているので値は楽観的)
#
# 限界(結果を読むときに必ず添える。表示と JSON にも英語で書く):
#   - 1 つの余震系列だけ。試験の地震は 18_01・21_01 で一度も使っていないが、仮説(τ = 2 s・C4)は同じ系列の 21_01 を見て決めた。
#     手を付けていない 2 つ目の系列での確認がまだ要る
#   - M ≥ 1.5 版は 15_01c v3.2 で作った(検測・QC は正本と同じ。データ全体の振幅の係数は正本と違うが、コサイン類似度と走時には効かない)
#   - 試験は小さい地震(1.5 ≤ Mj < 2.0)なので、Mj ≥ 2.0 の地震とは検測の質・局の数が違いうる
#   - 21_01 と同じ限界(過去の地震と正解は気象庁の震源・オフラインの PhaseNet・最大 24 局・未着の局の情報は使わない・
#     窓全体の平均と 30 秒窓の z-score・検測と通信の遅れなし)
#   - pool に 1.5 ≤ Mj < 2.0 の地震も入るので、較正と全ての中央値は 21_01 と直接は比べられない
#   - C4 の局の補正は過去の地震の気象庁の震源から作り、正解も気象庁の震源なので、C4 の得の一部は気象庁の枠に合わせた効果でありうる
#   - 2–8 Hz は同じ系列の 18_01(正本 198 地震)を見て選んだ
#   - H1 が主の判定。H2・H3 は副、それ以外は記述
#
# Usage : (先に Colab で 15_01c v3.2 を --min-mag 1.5 --tag _m15 で回し、出来た tottori_parsed_realpick_m15.pt を
#          Mac の ~/SWIFT/data/tottori_processed/ にコピーする。正本 tottori_parsed_realpick.pt はそのまま置いておく)
#         cd ~/SWIFT && uv run python src/21_02_tottori_similarity_confirmation.py --dev   (動作確認。試験を開かない)
#         cd ~/SWIFT && uv run python src/21_02_tottori_similarity_confirmation.py         (本番。1 回だけ)
# Output: models/21_02_judgment.json / models/21_02_opened.json / data/21_02_per_event.csv /
#         PDF/21_02_F1_error_vs_tau.pdf / PDF/21_02_F2_paired_difference.pdf / PDF/21_02_F3_similarity_vs_separation.pdf
#         (--dev では _dev、2 回目以降は _rerun_<UTC の時刻>)。CSV の列は 21_01 と同じに C4 を加えたもの
# 所要  : CPU のみ。未計測。時間はおおよそ(1 地震あたりの時間)×(試験の地震の数)で、過去の地震の数にも比例する
#         (模擬データ、過去の地震 480・各 16 局で 1 地震あたり約 15 s。dev の時間から見積もれる。最初の 10 地震の後に
#         残りの見込み時間を表示する)。メモリは M ≥ 1.5 版の大きさ(約 500 地震 × 24 局 × 3 × 2048 点)で 1〜2 GB の見込み
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
ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(pool の最後の新しい地震 20 個を代わりに使う)")
a = ap.parse_args()

# ---------------------------------------------------------------- 事前に固定した値(変えたら版を上げる)
VERSION = "v2"
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
print(f"[21_02] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
      f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")

# ---------------------------------------------------------------- 1. 入力
CP = ROOT / a.cache
if not CP.exists(): raise SystemExit(f"[21_02] STOP: {a.cache} が無い(15_01c v3.2 を --min-mag 1.5 --tag _m15 で作り、data/tottori_processed/ に置く)")
EVS = torch.load(CP, map_location="cpu", weights_only=False)
need = ["origin_time", "src_loc", "mw", "waveforms", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
for e in EVS:
    miss = [k for k in need if k not in e]
    if miss: raise SystemExit(f"[21_02] STOP: キャッシュの地震に {miss} が無い(15_01c v3.2 の出力か確かめる)")
for e in EVS:
    w_ = np.asarray(e["waveforms"])
    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_02] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_02] STOP: {e['origin_time']} の波形に NaN か無限大")
def to_ns(o):
    import pandas as pd
    try:
        t = pd.Timestamp(str(o).replace("Z", "+00:00"))
        t = t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t
        return int(t.value)
    except Exception:
        raise SystemExit(f"[21_02] STOP: origin_time {o!r} を時刻として読めない")
OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
order = np.argsort(OTNS, kind="stable"); EVS = [EVS[i] for i in order]; OTNS = OTNS[order]
NE = len(EVS)
SRC = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS])
MAG = np.array([float(e["mw"]) for e in EVS])
OT = [str(e["origin_time"]) for e in EVS]
if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
    raise SystemExit("[21_02] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[21_02] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
CANP = ROOT / a.canon
if not CANP.exists(): raise SystemExit(f"[21_02] STOP: 正本 {a.canon} が無い(使っていない地震を見分けるのに要る)")
CAN = torch.load(CANP, map_location="cpu", weights_only=False)
if len(CAN) != a.expect_canon: raise SystemExit(f"[21_02] STOP: 正本の地震の数 {len(CAN)} が {a.expect_canon} と違う")
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
print(f"[21_02] 入力: M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。正本 {len(CAN)} 地震のうち M ≥ 1.5 版に見つかった数 "
      f"{n_can_found}、そのうち局の数・P の時刻・Mj・震源が同じ割合 {same_frac:.3f}。Mj ≥ 2.0 で正本に無い地震 {n_extra2}"
      f"(同じ作り方なら 0 のはず。試験には使わず、過去の地震の一覧には入れる)。使っていない地震(Mj < 2.0 かつ正本に無い){int(FRESH.sum())}")
print(f"[21_02] 正本の SHA-256 {CANON_SHA[:12]}…  21_01 が使ったキャッシュの SHA-256 "
      + (f"{ref_sha[:12]}…" if ref_sha else "(models/21_01_judgment.json が無いので照合を飛ばした)"))
if ref_sha is not None and ref_sha != CANON_SHA: raise SystemExit("[21_02] STOP(G-fresh): 正本が 21_01 で使ったキャッシュと違う")
if n_can_found < 0.9 * len(CAN) or same_frac < 0.9:
    raise SystemExit("[21_02] STOP(G-fresh): 正本の地震のうち M ≥ 1.5 版に見つかったのが 9 割未満、または中身が同じ割合が 9 割未満"
                     "(作り方が違う可能性。この行を貼って相談)")
if n_can_found < len(CAN) or n_extra2 > 0 or same_frac < 1.0:
    print("[21_02] 注意(G-fresh): 正本と M ≥ 1.5 版が完全には一致していない(上の数を貼ってください。試験の地震は Mj < 2.0 かつ正本に無い地震だけなので、"
          "正本の地震が試験に入ることはない)")
del CAN
im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
    raise SystemExit(f"[21_02] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj 6.4・2026-01-06 01:18:48 UTC)")
CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
pool_idx = np.where(OTNS <= CUT_NS)[0]; test_idx = np.where((OTNS > CUT_NS) & FRESH)[0]
if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
    raise SystemExit("[21_02] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
print(f"[21_02] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
print(f"[21_02] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
      f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")

# ---------------------------------------------------------------- 2. 座標・検測(17_02 と同じ)
TFIRST = np.full(NE, np.nan)          # PhaseNet で測った最も早い P(気象庁の発生時刻からの s)
skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
for ie, e in enumerate(EVS):
    n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    ok = np.isfinite(tp) & (pf == 0)
    if ok.any(): TFIRST[ie] = float(tp[ok].min())
    kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
    if len(set(kk)) != n: raise SystemExit(f"[21_02] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
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
print(f"[21_02] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
if len(EVAL) == 0: raise SystemExit("[21_02] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
if a.dev: print(f"[21_02] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                "(較正にも入っているので値は楽観的)")

# ---------------------------------------------------------------- 1 回だけの記録(本番は、試験の地震の結果を計算する前に書く)
OPEN = ROOT / "models/21_02_opened.json"
SUF = "_dev" if a.dev else ""
def log_open(status):
    rec = json.load(open(OPEN)) if OPEN.exists() else []
    rec.append(dict(utc=utcnow(), status=status, version=VERSION, script_sha256=SELF_SHA, suffix=SUF)); json.dump(rec, open(OPEN, "w"), indent=1)
if not a.dev:
    if OPEN.exists() or (ROOT / "models/21_02_judgment.json").exists():
        SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
        print(f"[21_02] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
    log_open("opened")
def stop(msg):
    if not a.dev: log_open("stopped: " + msg[:160])
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
print(f"[21_02] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
      f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")

# ---------------------------------------------------------------- 4. 格子と探索(17_02 と同じ)
H = float(max(30.0, np.percentile(np.abs(np.r_[EX[CAL], EY[CAL]]), 99.5) + 30.0))
STEP = float(max(1.0, round(H / 30.0)))
ZMAX = float(max(30.0, np.percentile(SRC[CAL, 2], 99.5) * 1.3 + 10.0))
ZDEF = float(np.mean(SRC[CAL, 2]))
xc = np.arange(-H, H + 1e-6, STEP); zc = np.arange(0.0, ZMAX + 1e-6, STEP)
GX, GY, GZ = np.meshgrid(xc, xc, zc, indexing="ij"); COARSE = np.c_[GX.ravel(), GY.ravel(), GZ.ravel()]
XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
print(f"[21_02] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
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
print(f"[21_02] KDE の帯域(pool の一つ抜き): {KDE_H} km")
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
    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_02] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
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
    if ie is not None and ie in top: stop("[21_02] STOP: 自分自身が似た地震の上位に入っている")
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
    if not np.array_equal(libb[:len(lib)], lib): stop("[21_02] STOP: 過去の一覧の並びがおかしい")
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
    print(f"[21_02] 判定(事前宣言、H1): INCONCLUSIVE(評価できる試験の地震 {NT} < {MIN_TEST})")
    json.dump(dict(script="21_02_tottori_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, verdict="INCONCLUSIVE",
                   utc=utcnow(), suffix=SUF, cache=a.cache, cache_sha256=sha256(CP), canon_sha256=CANON_SHA, n_test=int(len(test_idx)),
                   n_fresh=int(FRESH.sum()), n_evaluated=NT, fresh=dict(n_canon_found=n_can_found, same_build_frac=same_frac,
                   n_mj2_not_in_canon=n_extra2, ref_21_01_cache_sha256=ref_sha), limits=LIMITS),
              open(ROOT / f"models/21_02_judgment{SUF}.json", "w"), indent=1)
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
        stop(f"[21_02] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
    for m in METH: P[m][ii] = R[m]
    NST[ii], NI[ii], SMAX[ii], C3FB[ii], NCORR[ii] = X["nst"], X["ni"], X["smax"], X["fb"], X["ncorr"]
    for j, t1 in enumerate(X["top1"]):
        if t1 is not None: BESTSEP[ii, j] = km_between(SRC[t1, 0], SRC[t1, 1], SRC[ie, 0], SRC[ie, 1])
    if (ii + 1) % 10 == 0:
        el = time.time() - T_EV
        print(f"  … {ii+1}/{NT}  ({time.time()-T0:.0f} s、残りの見込み約 {el / (ii + 1) * (NT - ii - 1) / 60:.0f} 分)")

# ---------------------------------------------------------------- 10. ゲート G-causal(未来の波形と検測を変えても同じ)
gate_ev = [ii for ii in range(NT) if NI[ii, TAUS.index(1.0)] > 0][:N_GATE]
if len(gate_ev) < 3: stop(f"[21_02] STOP(G-causal): τ = 1 s で似ている度合いが測れた地震が {len(gate_ev)} しかなく、確かめられない")
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
if not shared: stop("[21_02] STOP(G-causal): 陽性対照に使える局が無い(この行を貼って相談)")
pc = shared[0]; e2 = dict(orig); W = np.array(np.asarray(orig["waveforms"], float))
W[pc[8], :, IP + n_avail(1.0, pc[4]) - 1] += 50.0 * np.abs(W[pc[8], :, IP:IP + 100]).max()
e2["waveforms"] = W; EVS[ie] = e2; [FILT.pop((ie, b), None) for b in SOS]
S1, _ = similarity(ie, 1.0, lib0, BAND, raw=True)
EVS[ie] = orig; [FILT.pop((ie, b), None) for b in SOS]
pos_ctrl = float(np.max(np.abs(S1 - S0))) if len(S0) else 0.0
print(f"[21_02] G-causal({len(gate_ev)} 地震 × τ = 0.5・1・2・3 s、未来の波形と検測を置き換えた時の最大の差): {gc_max:.3g}  "
      f"陽性対照(窓の最後の点を変えた時の S の差): {pos_ctrl:.3g}  " + ("PASS" if (gc_max == 0.0 and pos_ctrl > 0) else "FAIL"))
if not (gc_max == 0.0 and pos_ctrl > 0): stop("[21_02] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")

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
def paired(A, B, j):
    x, y = E[A][:, j], E[B][:, j]; m = np.isfinite(x) & np.isfinite(y); nz = int(np.sum(x[m] != y[m]))
    d = dict(n=int(m.sum()), n_nonzero=nz, p=None, median_diff_km=None, frac_better=None, frac_tied=None)
    if m.sum() == 0: return d
    d.update(median_diff_km=float(np.median(x[m] - y[m])), frac_better=float(np.mean(x[m] < y[m])), frac_tied=float(np.mean(x[m] == y[m])))
    if nz >= 6: d["p"] = float(wilcoxon(x[m], y[m], alternative="less", zero_method="wilcox").pvalue)
    return d
phys_inf = SUMM["M5"]["inf"]["median_km"]
print(f"[21_02] G-phys(τ = ∞ の M5 の中央値 ≤ 0.5 km): {'—' if phys_inf is None else f'{phys_inf:.3f}'} km  " + ("PASS" if phys_inf is not None and phys_inf <= 0.5 else "FAIL")
      + "(参考: 15_12 は 0.13 km、分け方が違う)")
if not (phys_inf is not None and phys_inf <= 0.5): stop("[21_02] STOP(G-phys): 物理を鳥取に正しく移せていない可能性(この行を貼って相談)")
def judge(meth, t, alpha):
    j = TL.index(t)
    full = [m for m in BASE if SUMM[m][t]["available"] == 1.0 and SUMM[m][t]["median_km"] is not None]
    best = min(full, key=lambda m: SUMM[m][t]["median_km"])
    bm, cm = SUMM[best][t]["median_km"], SUMM[meth][t]["median_km"]
    pr = paired(meth, best, j); floor = bm < FLOOR_KM
    win = (not floor) and cm is not None and cm < bm and pr["p"] is not None and pr["p"] < alpha and pr["n_nonzero"] >= MIN_NONZERO
    return dict(method=meth, tau=t, alpha=alpha, best=best, best_median_km=bm, median_km=cm, paired_vs_best=pr, floor=bool(floor),
                win=bool(win), at_or_below_0p7_best=bool(cm is not None and cm <= BAR * bm), vs_M6r=paired(meth, "M6r", j),
                vs_M6p=paired(meth, "M6p", j))
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

def f2(v): return "—" if v is None else f"{v:.2f}"
def fp(p): return "—" if p is None else f"{p:.2g}"
print(f"\n[21_02] ===== 水平誤差の中央値 km [95% 区間](評価 {NT} 地震{'、dev(楽観的)' if a.dev else ''}) =====")
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
print(f"\n[21_02] ===== 事前宣言の判定 =====")
for name, h in HYP.items():
    pb = h["paired_vs_best"]
    print(f"  {name}{'(主)' if name == 'H1' else '(副)'}: {h['method']} @ τ = {h['tau']} s  {f2(h['median_km'])} km 対 BEST {h['best']} "
          f"{h['best_median_km']:.2f} km  p = {fp(pb['p'])}(基準 {h['alpha']})  差が 0 でない組 {pb['n_nonzero']}  FLOOR={h['floor']}  "
          f"→ {'勝ち' if h['win'] else '勝ちなし'}")
print(f"\n[21_02] 判定(事前宣言、H1): {VERDICT}")
print("[21_02] 限界: " + " / ".join(LIMITS))

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
with open(ROOT / f"data/21_02_per_event{SUF}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["origin_time", "mj", "lat", "lon", "depth_km"] + [f"n_sta_t{t}" for t in TL] + [f"n_i_t{t}" for t in TL[:-1]]
               + [f"smax_t{t}" for t in TL[:-1]] + [f"best_template_sep_km_t{t}" for t in TL[:-1]] + [f"c3_fallback_t{t}" for t in TL[:-1]]
               + [f"c4_n_corrected_t{t}" for t in TL[:-1]]
               + [f"{m}_err_t{t}" for m in CM for t in (TL if m in BASE else ["inf"] if m in ALLP else TL[:-1])])
    for i, ie in enumerate(EVAL):
        w.writerow([OT[ie], f"{MAG[ie]:.1f}", f"{SRC[ie,0]:.4f}", f"{SRC[ie,1]:.4f}", f"{SRC[ie,2]:.2f}"] + [int(v) for v in NST[i]]
                   + [int(v) for v in NI[i]] + [("" if not np.isfinite(v) else f"{v:.4f}") for v in SMAX[i]]
                   + [("" if not np.isfinite(v) else f"{v:.3f}") for v in BESTSEP[i]] + [int(v) for v in C3FB[i]] + [int(v) for v in NCORR[i]]
                   + [("" if not np.isfinite(E[m][i, j]) else f"{E[m][i, j]:.4f}") for m in CM
                      for j in (range(len(TL)) if m in BASE else [ji] if m in ALLP else range(len(TAUS)))])
out = dict(script="21_02_tottori_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
           suffix=SUF, cache=a.cache, cache_sha256=sha256(CP), canon=a.canon, canon_sha256=sha256(CANP),
           n_fresh=int(FRESH.sum()), n_canon_found=n_can_found, n_events=NE, n_pool=int(len(pool_idx)), n_test=int(len(test_idx)),
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
           fresh=dict(n_canon_found=n_can_found, same_build_frac=same_frac, n_mj2_not_in_canon=n_extra2, canon_sha256=CANON_SHA,
                      ref_21_01_cache_sha256=ref_sha),
           verdict_rule="BEST(tau) = smallest median among the 9 AI-free methods that give an estimate for every evaluated event "
                        "(chosen on the evaluated events). A hypothesis wins if the method median < BEST median, one-sided paired "
                        "Wilcoxon (zero_method='wilcox') p < alpha with >= 10 non-zero pairs, and BEST >= 0.5 km (not FLOOR). "
                        "H1 (primary): C3 at tau = 2 s, alpha 0.01 -> CONFIRMED / PHYSICS-AT-FLOOR / NOT-CONFIRMED; INCONCLUSIVE if "
                        "fewer than 30 evaluated events. H2: C4 at tau = 2 s, H3: C3 at tau = 0.5 s, each alpha 0.005 (secondary). "
                        "Test events: 1.5 <= Mj < 2.0 events absent from the 198-event canon, later than mainshock + 72 h",
           limits=LIMITS, runtime_s=time.time() - T0)
json.dump(clean(out), open(ROOT / f"models/21_02_judgment{SUF}.json", "w"), indent=1)
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
ax.set_title(f"West Tottori 2026, {'DEV (pool events, optimistic)' if a.dev else 'test events'}, n = {NT}; shading = 95% bootstrap CI",
             fontsize=10)
ax.grid(alpha=0.3, which="both"); ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_02_F1_error_vs_tau{SUF}.pdf", bbox_inches="tight"); plt.close(fig)

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
fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_02_F2_paired_difference{SUF}.pdf", bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(7.6, 4.4))
for j, (t, c) in enumerate(zip(TT, ("tab:green", "tab:blue", "tab:orange", "tab:red"))):
    m = np.isfinite(SMAX[:, j]) & np.isfinite(BESTSEP[:, j])
    ax.scatter(SMAX[m, j], np.maximum(BESTSEP[m, j], 0.01), s=14, color=c, alpha=0.7, label=f"tau = {t} s")
ax.set_xlabel("Best similarity score S (0-1)"); ax.set_ylabel("Epicentral distance to most similar past event (km)\n(values < 0.01 km shown at 0.01)")
ax.set_yscale("log"); ax.grid(alpha=0.3, which="both")
ax.set_title("Is the most similar past event close by?", fontsize=10)
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_02_F3_similarity_vs_separation{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
print(f"[21_02] 出力: models/21_02_judgment{SUF}.json, data/21_02_per_event{SUF}.csv, PDF/21_02_F1〜F3{SUF}.pdf"
      + ("" if a.dev else ", models/21_02_opened.json") + f"  ({time.time()-T0:.0f} s)")
