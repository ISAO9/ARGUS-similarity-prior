#!/usr/bin/env python3
# =============================================================================
# Script : 21_01_tottori_similarity_prior_early_location.py  (v3)
#          [鳥取 2026 で、最初の P から 1・2・3 秒の時点の震源を、「波形が一番似ている過去の地震」を使って決め、
#           同じ時点の物理(AI を使わない最良の方法)と、事前に決めた規則で 1 回だけ比べる]
# Project: ARGUS(新生)— SSJ 2026(11/4)の付録「予備結果」用の挑戦枠(B 案)。締切 2026-10-30
#
# なぜ必要か:
#   鳥取では、検測がそろえば物理だけで震源の誤差が約 0.13 km(15_12)なので、AI の価値は「最初の数秒」の速さにしかない。
#   最初の 1〜3 秒は届いた局が少なく、物理だけでは決まりにくい。一方、鳥取の余震域は狭く、近い地震どうしの波形は似ている
#   (18_01、P・2–8 Hz・長い窓: 震源間 0–0.5 km の組の合格の割合 0.665、5–10 km の組 0.179。ただし 18_01 はゼロ位相の
#   フィルタで、主の窓の 2–8 Hz は偶然の合格の対照で不合格(0.094)、18_01 全体の計画の判定は INCONCLUSIVE だった)。
#   そこで「届いた局の最初の波形が、どの過去の地震に似ているか」で震源の候補を絞り、物理の式と掛け合わせれば、
#   同じ時点の物理より良くなるかを測る。過去の地震の一覧は、プラットフォーム構想の「遅い層」が作る地震の一覧に当たる。
#   これは AI(学習)ではなく、波形の照合である。学習型は、これが効くと分かってから作る。
#
# 何をするか:
#   1. 入力: ARGUS の鳥取キャッシュの正本(15_01c v3、Mj ≥ 2.0、198 地震。data/tottori_processed/tottori_parsed_realpick.pt)。
#      各地震・各局の 3 成分波形(P の 3.00 s 前〜17.47 s 後、2,048 点、100 Hz、局ごとに自分の P を 300 点目に置く。
#      15_01c は速度を中心差分(np.gradient)で微分した擬似加速度にし、窓全体で平均を引いてある)、PhaseNet の P の時刻
#      (tp_times = 気象庁の発生時刻からの秒)、S−P(sp_diffs)、代替値の印(p_fallback・s_fallback。0 = PhaseNet で測った値)、
#      局の座標(緯度・経度・高さ km)。局は座標(緯度・経度を小数 4 桁、高さを小数 3 桁に丸めたもの)で同じ局と見なす
#      (キャッシュに局名が無いため。18_01 と同じ。17_02 は緯度・経度だけ)。地震は発生時刻の順に並べ直す。
#      止める条件(STOP): キャッシュが無い・どれかの地震で鍵が足りない・地震の数が --expect-n でない・Mj が 2.0 未満の地震がある・
#      波形の形が (局, 3, 2048) でない・使う局(先頭の n_real_stations 局)の波形に NaN か無限大・発生時刻が読めない・
#      震源が (緯度, 経度, 深さ km) に見えない・本震(Mj 最大)が Mj 6.0 未満か 2026-01-06 01:18:48 UTC から 60 s 以上ずれる・
#      pool か試験が 0 地震(G-split)・1 つの地震の中で座標の同じ局が重なる(局を見分けられない)
#   2. 分け方(事前に固定。時刻順): 本震の発生から 72 時間までの地震(本震より前の地震も含む)= pool、それより後 = 試験。
#      pool だけで決めるもの: 座標の原点、速度・局の補正(17_02 と同じ。S の重み 0.5、縮み n/(n+5)、3 回の繰り返し)、
#      ラプラス尺度 b(= 補正後の残差の |r| の中央値 / ln 2)、KDE の帯域(候補 0.5・1・1.5・2・3・5・8 km の一つ抜き尤度)、
#      格子の範囲(水平 ±H、H = max(30, 震央の |x|,|y| の 99.5% 点 + 30) km、粗い間隔 max(1, round(H/30)) km、
#      深さ 0〜max(30, 深さの 99.5% 点 × 1.3 + 10) km)、相が 3 つの時の固定の深さ(pool の平均の深さ)、M6p の事前分布の地震。
#      これらは全て、pool のうち測った P がある地震で決める(17_02 は pool の全ての地震)。
#      評価できる試験の地震(測った P がある地震)が 30 未満なら判定は INCONCLUSIVE。
#   3. 時刻 τ: 各地震で、PhaseNet で測った P(p_fallback = 0)の最も早い時刻を 0 とし、τ = 0.5, 1, 2, 3 s の時点で
#      「既に届いている検測と波形」だけを使う。P は tp ≤ τ、S は S を測った局(s_fallback = 0)で tp + sp ≤ τ の時だけ使う
#      (P・S の使い方は 17_02 と同じ。比べる時の余裕 1e-4 s は 17_02 に無く、tp が float32 で保存されているためここで足した)。
#      代替値の P(p_fallback ≠ 0)はどの方法も使わない。17_02 は代替値も含めた最も早い P を 0 にしたが、ここでは測った P だけで決める。
#      測った P が無い地震は、較正・評価・過去の地震の一覧の全てから除く(数を表示する)。
#      判定は τ = 1, 2, 3 s。τ = 0.5 s と τ = ∞(全検測)は記述だけ。
#   4. AI を使わない比べる相手(物理の側。式は 17_02 と同じ。17_02 から変えた点は M0r・M3r・Mp10・M6r の「過去の地震」):
#        M0r  過去の地震の震央の平均(データを見ない)
#        Mp10 直前 10 地震の震央の平均(17_03e の C3 と同じ考え)
#        M1   最初に P が来た局の位置
#        M2   τ までに P が来た局の重心
#        M3r  過去の地震のうち「最初に P が来た局」が同じ地震の震央の中央値(5 地震未満なら、最初の局が近い順に足す)
#        M5   物理(線形勾配の速度・局の補正・L1 の格子探索。粗い格子 → 1/5 → 1/25 と細かくする。4 相以上で深さ自由、
#             3 相で深さを固定、2 相以下は解なし)
#        M5f  M5 が解なしの時は M1
#        M6p  17_02 の M6 と同じ(M5 の L1 誤差 / b をラプラスの負の対数尤度にし、pool の地震で作った M3 の地震の KDE に
#             一様分布を 5% 混ぜた事前分布を掛けた最大点。2 相でも解が出る。1 相以下は事前分布だけ)。M6p の事前分布は
#             pool の全ての地震を使い、1 時間の空白を置かない(比べる相手に有利な向き)
#        M6r  M6p の事前分布を、「その時点までの過去の地震」で作ったもの(M3r の地震を使う)
#      「過去の地震」= 発生時刻がその地震の発生の 1 時間(BUFFER_H)より前の地震(pool・試験を問わない)。
#      その震源は気象庁の震源を使う(運用では遅い層の震源に当たる。限界を参照)。
#   5. 波形の似ている度合い(新しい方法の部品):
#      - 全ての記録に Butterworth の帯域通過 2–8 Hz(設計の次数 4、帯域通過なので全体で 8 次)を因果的(sosfilt、前向きだけ)に
#        掛ける。因果的なので、記録全体に掛けてから τ で切っても、τ で切ってから掛けても値は同じになる。
#      - 試験の地震 i の局 s(P を測り、τ までに届いた局)の窓: 自分の P の 0.2 s 前の点から、時刻が τ − 0.01 s 以下の最後の点まで
#        (キャッシュの微分が中心差分で、点 n の値が元の点 n+1 を使うため、最後の 1 点を使わない。窓の中の P からの点の数
#        n_av = floor((τ − tp_s) × 100)。n_av が 30 点(0.3 s)未満の局は使わない。τ ≤ 3 s なので窓は最大 3 s)。
#      - 過去の地震 j の同じ局 s の窓(j で P を測った局だけ): j の P の 0.2 s 前から同じ点の数。±0.1 s(±10 点)ずらす。
#      - 局の値 c_ijs = 3 成分をつないだベクトルどうしのコサイン類似度(平均を引かない正規化内積。帯域通過の後なので平均は
#        ほぼ 0)の、ずらしの中の最大値。窓がすべて 0 の局は値 0 として数える。
#      - 地震の値 S_ij = Σ_s max(c_ijs, 0) / n_i(n_i = i で使える局の数。j がその局を持たなければ 0 と数える)。
#   6. 新しい方法(判定に使うのは C3 だけ):
#        C3(主) 物理 × 似ている地震の事前分布: M6r と同じ式で、事前分布の地震を「S_ij > 0 の過去の地震のうち、S_ij の上位
#               K = 10(S_ij > 0 の地震が 10 未満ならその全て)」に替えたもの。M6r との違いは事前分布の地震の選び方だけ(最初の局が同じ地震 → 波形が似ている地震)。
#               S_ij > 0 の過去の地震が 5 未満の時(使える局が無い時を含む)は M6r の値を使う(その割合を出す)。
#        C1(記述) S_ij が最大の過去の地震の震央(同じ値なら古い地震)
#        C2(記述) C3 と同じ上位の地震の震央の中央値(緯度・経度ごと)。C1・C2 は C3 が M6r に戻った地震では値が無い
#      感度(記述、C3 の変種): K = 5・20、帯域 4–16 Hz、過去の地震の空白 0.1 時間(6 分。事前分布の地震も、M6r に戻す時の値も、
#      0.1 時間の一覧で作る)。空白 0.1 時間の一覧は 1 時間の一覧を先頭に含むので、S_ij はその一覧で 1 回だけ計算して共有する
#   7. 判定(事前宣言。SSJ の付録の予備結果と、次に学習型を作るかの計画の判断にだけ使う。論文の主張ではない):
#      τ = 1, 2, 3 s のそれぞれで、
#        BEST(τ) = 4. の 9 つのうち、全ての評価の地震で推定がある方法の中で、水平誤差の中央値が最小のもの(M5 は解なしの
#                  地震がある τ では外れる。試験の地震で選ぶので比べる相手に有利 = C3 に厳しい)
#        WIN(τ)  = C3 の中央値 < BEST の中央値 かつ 地震ごとの片側の対応 Wilcoxon(C3 < BEST、差が 0 の組は除く scipy の既定
#                  zero_method="wilcox")で p < 0.01 かつ 差が 0 でない組が 10 以上
#        FLOOR(τ)= BEST の中央値が 0.5 km 未満(気象庁の震源の誤差と同程度で、勝ち負けを言えない)。FLOOR の τ は WIN にしない
#      判定: SIMILARITY-WINS    = 3 つ全ての τ で WIN
#            SIMILARITY-PARTIAL = 1 つか 2 つの τ で WIN
#            PHYSICS-AT-FLOOR   = どの τ でも WIN でなく、3 つ全ての τ が FLOOR(物理が既に床にいて、速さで勝つ余地が無い)
#            SIMILARITY-NO      = それ以外で、どの τ でも WIN でない
#            INCONCLUSIVE       = 評価できる試験の地震が 30 未満
#      記述: C3 と M6r・M6p の対応比較(p)、C1・C2・感度の値、C3 が 0.7 × BEST 以下か(熊本の合格の線と同じ考え)、
#            C3 が M6r に戻った割合、全ての中央値の 95% 区間(方法ごとに地震を単位にした bootstrap 2,000 回、専用の乱数 種 12)
#      格子の最も細かい間隔は粗い間隔の 1/25(粗い間隔 1 km なら 0.04 km)で、それより小さい差は格子で決まる
#      ここで決めた計画の値(原典なし): 72 時間・1 時間・2–8 Hz・0.2 s・0.3 s・±0.1 s・K = 10・S > 0 が 5 未満で M6r に戻す・
#        0.5 km・30 地震・0.01・差が 0 でない組 10・0.7・2,000 回・種 12・dev の 20 地震・本震の確かめ(Mj 6.0・60 s)・
#        感度の値(K = 5・20、4–16 Hz、0.1 時間)・G-causal の 5 地震と最少 3 地震・乱数の大きさ 1e3・遅らせる幅 0.5〜2 s・
#        陽性対照の 50 倍・窓の点の数の余裕 1e-3 点。17_02 から引き継いだ値: S の重み 0.5、縮み 5、
#        一様の混合 0.05、事前分布の最少 5 地震、KDE の帯域の候補、格子の規則、速度の探索範囲
#      2–8 Hz は 18_01 の結果(同じ 198 地震)を見て選んだ。この試験の地震の結果を見て選んだのではない
#   8. 1 回だけ: 本番(--dev なし)は、試験の地震の計算を始める前に models/21_01_opened.json に「開いた」記録を書き足す
#      (STOP した時・計算の途中で例外が出た時・終わった時も書き足す。前の記録は消さない)。既に記録があれば計算はするが、結果は
#      _rerun_<UTC の時刻> の付いた名前に書く(前の結果は上書きしない)。結果の JSON と CSV は図より先に書く。
#      --dev(試験の地震を開かない動作確認)は pool の最後の 20 地震を試験の代わりに使い、出力に _dev を付ける。
#      dev の地震は較正(速度・局の補正・b・KDE)と M6p の事前分布の中にも入っているので、dev の値は楽観的で、動作の確認にだけ使う
#      (判定には使わない。設定は dev の結果を見て変えない。変えたら版を上げて記録する)。
#
# ゲート(違えば STOP。結果は JSON の gates に残す):
#   G-split : pool と試験が時刻で重ならず、どちらも 1 地震以上
#   G-lib   : 評価する地震の過去の地震の一覧に、自分自身と自分より後の地震が入っていないこと(評価する全ての地震で確かめる)
#   G-causal: 評価する地震のうち、τ = 1 s で似ている度合いが測れた最初の 5 地震で、τ = 1, 2, 3 s のそれぞれについて、
#             (a) 窓の最後の点より後のキャッシュの波形(届いていない局は全部)を乱数に、(b) τ までに届いていない P・S の時刻を
#             0.5〜2 s 遅い値に置き換えて、全ての方法の位置と S_ij の最大値が完全に一致すること。届いていない局の座標・代替値の印は
#             置き換えない。TFIRST(最初の P)と最初の局は τ = 0 の局だけで決まるので、ゲートの中で計算し直さない。
#             陽性対照: τ = 1 s で、過去の地震と共有する最初の局の窓の最後の点を変えると、0 で切る前の S_ij が少なくとも
#             1 つ変わること(ゲートが 1 点の差を見落とさないことの確認)。
#             似ている度合いが測れた地震が 3 未満なら STOP(確かめられない)
#   G-phys  : 評価する地震の τ = ∞ の M5 の水平誤差の中央値が 0.5 km 以下(17_02 の物理を鳥取に正しく移せたかの確認。
#             15_12 の 0.13 km は分け方が違うので、一致は求めない。dev では pool の地震で測るので楽観的)
#   STOP した時は、直してから版を上げて回し直す(本番で止まった時は opened.json に記録が残り、次は _rerun になる)
#
# 限界(結果を読むときに必ず添える。表示と JSON にも英語で書く):
#   - 正本の 198 地震(Mj ≥ 2.0)、1 つの余震系列だけ。鳥取は ARGUS の開発で使ったデータで、2–8 Hz の選択は 18_01(同じ 198 地震、
#     ゼロ位相のフィルタ)を見て決めた。手を付けていない 2 つ目の系列での確認が要る
#   - 過去の地震の震源は気象庁の震源(運用では遅い層の自動の震源。それより悪い可能性がある)。正解も気象庁の震源で、誤差を含む
#   - 検測は記録全体に掛けたオフラインの PhaseNet(実時間の検測より良い可能性がある)。全ての方法で同じ検測を使う
#   - キャッシュの局は、PhaseNet の P がある局を先に P の早い順に最大 24 局。「まだ届いていない局」の情報は使っていない
#   - キャッシュの波形は窓全体(2,048 点)で平均を引いてある(未来の値を含む。2 Hz の高域通過で、窓の初め(P の 3 s 前)からの
#     過渡応答を除いて消える)。元の h5 は 30 秒窓ごとに z-score で正規化されていて、正規化の尺度はその窓の中の後の値を含む
#     (コサイン類似度は尺度によらないが、窓の継ぎ目が相関の窓に入ると影響しうる)。中心差分の 1 点先は窓の最後の点を使わないことで避けた
#   - 検測・通信の遅れは入れていない(τ は理想的な経過時間)
#   - 判定は C3 だけ。C1・C2・感度は記述で、選び直さない
#
# Usage : cd ~/SWIFT && uv run python src/21_01_tottori_similarity_prior_early_location.py --dev   (先に動作確認。試験を開かない)
#         cd ~/SWIFT && uv run python src/21_01_tottori_similarity_prior_early_location.py         (本番。1 回だけ)
#         (data/tottori_processed/tottori_parsed_realpick.pt があること。15_02・15_03・18_01 で使った正本。
#          JSON に cache_sha256 を記録する。18_01 の JSON の cache_sha256 と見比べると同じ正本か分かる)
# Output: models/21_01_judgment.json / models/21_01_opened.json / data/21_01_per_event.csv /
#         PDF/21_01_F1_error_vs_tau.pdf / PDF/21_01_F2_paired_difference.pdf / PDF/21_01_F3_similarity_vs_separation.pdf
#         (--dev では名前に _dev、2 回目以降は _rerun_<UTC の時刻>)
#         CSV の列: 地震の情報、τ ごとの P のある局の数(n_sta)、似ている度合いに使えた局の数(n_i)、S_ij の最大値(smax)、
#         一番似た過去の地震までの震央距離(best_template_sep_km)、C3 が M6r に戻ったか(c3_fallback)、各方法の水平誤差(km)
# 所要  : CPU のみ。模擬データ(198 地震、各 24 局)で dev が約 2〜4 分、本番(試験 71 地震)が約 10〜15 分(作成側の環境)。
#         実データでは未計測。メモリは 1 GB 前後の見込み
# =============================================================================
import json, argparse, time, csv, hashlib, math, warnings, datetime as dt
from pathlib import Path
import numpy as np
import torch
from scipy.signal import butter, sosfilt
from scipy.stats import wilcoxon
warnings.filterwarnings("ignore", message="All-NaN slice")

ap = argparse.ArgumentParser()
ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick.pt")
ap.add_argument("--expect-n", type=int, default=198)
ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(pool の最後の 20 地震を代わりに使う)")
a = ap.parse_args()

# ---------------------------------------------------------------- 事前に固定した値(変えたら版を上げる)
VERSION = "v3"
FS, IP, NTS = 100.0, 300, 2048
TAUS = [0.5, 1.0, 2.0, 3.0]                # 0.5 s は記述だけ
JUDGED = ["1", "2", "3"]
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
LIMITS = ["198 events (Mj >= 2.0) of one aftershock sequence; Tottori was used in ARGUS development and the 2-8 Hz band was chosen "
          "after seeing 18_01 (same events, zero-phase filter); an untouched second sequence is needed",
          "past-event locations are JMA hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
          "offline PhaseNet picks on full records (possibly better than real-time picks); every method uses the same picks",
          "cache keeps up to 24 stations per event (PhaseNet P first, earliest first); no not-yet-arrived information is used",
          "cache waveforms had the full-window mean removed (includes future samples; removed by the 2 Hz high-pass except for a "
          "transient from the window start 3 s before P) and the source h5 is z-score normalised per 30-s window (the scale uses later "
          "samples of that window; cosine similarity is scale-invariant except where a window join falls inside the correlation window); "
          "the one-sample look-ahead of the cache's central-difference derivative is avoided by not using the last sample",
          "no picking or telemetry latency (tau is ideal elapsed time)",
          "only C3 is judged; C1, C2 and sensitivities are descriptive"]

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
print(f"[21_01] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
      f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")

# ---------------------------------------------------------------- 1. 入力
CP = ROOT / a.cache
if not CP.exists(): raise SystemExit(f"[21_01] STOP: {a.cache} が無い(15_01c v3 の正本を data/tottori_processed/ に置く)")
EVS = torch.load(CP, map_location="cpu", weights_only=False)
need = ["origin_time", "src_loc", "mw", "waveforms", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
for e in EVS:
    miss = [k for k in need if k not in e]
    if miss: raise SystemExit(f"[21_01] STOP: キャッシュの地震に {miss} が無い(15_01c v3 の出力か確かめる)")
if len(EVS) != a.expect_n:
    raise SystemExit(f"[21_01] STOP: 地震の数 {len(EVS)} が {a.expect_n} と違う(別のキャッシュなら --expect-n で数を指定)")
for e in EVS:
    w_ = np.asarray(e["waveforms"])
    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_01] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_01] STOP: {e['origin_time']} の波形に NaN か無限大")
def to_ns(o):
    import pandas as pd
    try:
        t = pd.Timestamp(str(o).replace("Z", "+00:00"))
        t = t.tz_convert("UTC").tz_localize(None) if t.tzinfo is not None else t
        return int(t.value)
    except Exception:
        raise SystemExit(f"[21_01] STOP: origin_time {o!r} を時刻として読めない")
OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
order = np.argsort(OTNS, kind="stable"); EVS = [EVS[i] for i in order]; OTNS = OTNS[order]
NE = len(EVS)
SRC = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS])
MAG = np.array([float(e["mw"]) for e in EVS])
OT = [str(e["origin_time"]) for e in EVS]
if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
    raise SystemExit("[21_01] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
if MAG.min() < 2.0 - 1e-6: raise SystemExit(f"[21_01] STOP: Mj {MAG.min():.2f} の地震がある(正本は Mj ≥ 2.0)")
im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
    raise SystemExit(f"[21_01] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj 6.4・2026-01-06 01:18:48 UTC)")
CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
pool_idx = np.where(OTNS <= CUT_NS)[0]; test_idx = np.where(OTNS > CUT_NS)[0]
if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
    raise SystemExit("[21_01] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
print(f"[21_01] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
print(f"[21_01] 分け方: pool(本震 + 72 h まで){len(pool_idx)}  試験 {len(test_idx)}(最初 {OT[test_idx[0]][:19]})  G-split PASS")

# ---------------------------------------------------------------- 2. 座標・検測(17_02 と同じ)
TFIRST = np.full(NE, np.nan)          # PhaseNet で測った最も早い P(気象庁の発生時刻からの s)
skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
for ie, e in enumerate(EVS):
    n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    ok = np.isfinite(tp) & (pf == 0)
    if ok.any(): TFIRST[ie] = float(tp[ok].min())
    kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
    if len(set(kk)) != n: raise SystemExit(f"[21_01] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
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
print(f"[21_01] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
EVAL = (pool_idx[HASP[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
if a.dev: print(f"[21_01] dev: 試験を開かず、pool の最後の {N_DEV} 地震({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                "(較正にも入っているので値は楽観的)")

# ---------------------------------------------------------------- 1 回だけの記録(本番は、試験の地震の結果を計算する前に書く)
OPEN = ROOT / "models/21_01_opened.json"
SUF = "_dev" if a.dev else ""
def log_open(status):
    rec = json.load(open(OPEN)) if OPEN.exists() else []
    rec.append(dict(utc=utcnow(), status=status, version=VERSION, script_sha256=SELF_SHA, suffix=SUF)); json.dump(rec, open(OPEN, "w"), indent=1)
if not a.dev:
    if OPEN.exists() or (ROOT / "models/21_01_judgment.json").exists():
        SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
        print(f"[21_01] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
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
print(f"[21_01] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
      f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")

# ---------------------------------------------------------------- 4. 格子と探索(17_02 と同じ)
H = float(max(30.0, np.percentile(np.abs(np.r_[EX[CAL], EY[CAL]]), 99.5) + 30.0))
STEP = float(max(1.0, round(H / 30.0)))
ZMAX = float(max(30.0, np.percentile(SRC[CAL, 2], 99.5) * 1.3 + 10.0))
ZDEF = float(np.mean(SRC[CAL, 2]))
xc = np.arange(-H, H + 1e-6, STEP); zc = np.arange(0.0, ZMAX + 1e-6, STEP)
GX, GY, GZ = np.meshgrid(xc, xc, zc, indexing="ij"); COARSE = np.c_[GX.ravel(), GY.ravel(), GZ.ravel()]
XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
print(f"[21_01] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
      f"  固定の深さ {ZDEF:.1f} km")
def misfit(nodes, pk):
    xs = np.array([p[1] for p in pk]); ys = np.array([p[2] for p in pk]); zs = np.array([p[3] for p in pk])
    R = np.sqrt((nodes[:, :1] - xs) ** 2 + (nodes[:, 1:2] - ys) ** 2 + (nodes[:, 2:3] - zs) ** 2)
    TP = tt(R, zs[None, :], nodes[:, 2:3], V0, KG)
    obs, calc, w = [], [], []
    for j, p in enumerate(pk):
        obs.append(p[4]); calc.append(TP[:, j] + cP.get(p[0], 0.0)); w.append(p[5])
        if p[7] > 0: obs.append(p[6]); calc.append(TP[:, j] * VPVS + cS.get(p[0], 0.0)); w.append(p[7])
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
print(f"[21_01] KDE の帯域(pool の一つ抜き): {KDE_H} km")
def log_prior(nodes, mem):
    d2 = (nodes[:, :1] - EX[mem][None, :]) ** 2 + (nodes[:, 1:2] - EY[mem][None, :]) ** 2
    m = -0.5 * d2 / KDE_H ** 2; mx = m.max(1, keepdims=True)
    lk = mx[:, 0] + np.log(np.exp(m - mx).sum(1)) - np.log(len(mem) * 2 * np.pi * KDE_H ** 2)
    lu = -np.log((2 * H) ** 2)
    return np.logaddexp(np.log(1 - PRIOR_EPS) + lk, np.log(PRIOR_EPS) + lu)
def locate_map(pk, mem):
    mem = np.asarray(mem, int)
    sc = (lambda N: -log_prior(N, mem)) if n_phases(pk) <= 1 else (lambda N: misfit(N, pk) / LAP_B - log_prior(N, mem))
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
    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_01] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
    return lib
POOL_OK = np.array(CAL, int)

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
def c_from(S, lib, pk, m3, m6r, k):
    """C1・C2・C3。S > 0 の過去の地震が MIN_POS 未満なら C3 = M6r(C1・C2 は値なし)"""
    pos = int((S > 0).sum())
    if pos < MIN_POS: return dict(C1=None, C2=None, C3=m6r, fb=True, top1=None)
    top = lib[np.argsort(-S, kind="stable")[:min(k, pos)]]
    return dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
                C3=locate_map(pk, top), fb=False, top1=int(top[0]))

# ---------------------------------------------------------------- 7. 1 つの地震の全ての方法
BASE = ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r"]
NEW = ["C1", "C2", "C3"]
SENSN = ["C3_K5", "C3_K20", "C3_band4-16", "C3_buffer0.1h"]
METH = BASE + NEW + SENSN
TL = [f"{t:g}" for t in TAUS] + ["inf"]
def eval_event(ie, only_tau=None):
    lib = library(ie); libb = library(ie, BUFFER_SENS_H)
    if not np.array_equal(libb[:len(lib)], lib): stop("[21_01] STOP: 過去の一覧の並びがおかしい")
    p0 = FIRST[ie]
    m3 = prior_members(lib, p0[0], (p0[1], p0[2])); m3b = prior_members(libb, p0[0], (p0[1], p0[2]))
    m3p = prior_members(POOL_OK, p0[0], (p0[1], p0[2]))
    R = {m: np.full((len(TL), 2), np.nan) for m in METH}
    X = dict(nst=np.zeros(len(TL), int), ni=np.zeros(len(TAUS), int), smax=np.full(len(TAUS), np.nan),
             fb=np.zeros(len(TAUS), bool), top1=[None] * len(TAUS))
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
        Sb, nib = similarity(ie, tau, libb, BAND)            # 空白 0.1 時間の一覧(主の一覧はその先頭)
        S, ni = Sb[:len(lib)], nib
        o = c_from(S, lib, pk, m3, m6r, TOPK)
        for m in NEW:
            if o[m] is not None: R[m][jt] = o[m]
        X["ni"][jt], X["smax"][jt], X["fb"][jt], X["top1"][jt] = ni, (float(S.max()) if ni > 0 and len(S) else np.nan), o["fb"], o["top1"]
        R["C3_K5"][jt] = c_from(S, lib, pk, m3, m6r, TOPK_SENS[0])["C3"]
        R["C3_K20"][jt] = c_from(S, lib, pk, m3, m6r, TOPK_SENS[1])["C3"]
        S2, _ = similarity(ie, tau, lib, BAND_SENS)
        R["C3_band4-16"][jt] = c_from(S2, lib, pk, m3, m6r, TOPK)["C3"]
        R["C3_buffer0.1h"][jt] = c_from(Sb, libb, pk, m3b, locate_map(pk, m3b), TOPK)["C3"]
    return R, X

# ---------------------------------------------------------------- 9. 評価
NT = len(EVAL)
P = {m: np.full((NT, len(TL), 2), np.nan) for m in METH}
NST = np.zeros((NT, len(TL)), int); NI = np.zeros((NT, len(TAUS)), int); SMAX = np.full((NT, len(TAUS)), np.nan)
C3FB = np.zeros((NT, len(TAUS)), bool); BESTSEP = np.full((NT, len(TAUS)), np.nan)
for ii, ie in enumerate(EVAL):
    try:
        R, X = eval_event(ie)
    except SystemExit:
        raise
    except BaseException as ex:
        stop(f"[21_01] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
    for m in METH: P[m][ii] = R[m]
    NST[ii], NI[ii], SMAX[ii], C3FB[ii] = X["nst"], X["ni"], X["smax"], X["fb"]
    for j, t1 in enumerate(X["top1"]):
        if t1 is not None: BESTSEP[ii, j] = km_between(SRC[t1, 0], SRC[t1, 1], SRC[ie, 0], SRC[ie, 1])
    if (ii + 1) % 10 == 0: print(f"  … {ii+1}/{NT}  ({time.time()-T0:.0f} s)")

# ---------------------------------------------------------------- 10. ゲート G-causal(未来の波形と検測を変えても同じ)
gate_ev = [ii for ii in range(NT) if NI[ii, TAUS.index(1.0)] > 0][:N_GATE]
if len(gate_ev) < 3: stop(f"[21_01] STOP(G-causal): τ = 1 s で似ている度合いが測れた地震が {len(gate_ev)} しかなく、確かめられない")
gc_max, gc_n, pos_ctrl = 0.0, 0, None
for ii in gate_ev:
    ie = EVAL[ii]; orig = EVS[ie]
    for t in JUDGED:
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
if not shared: stop("[21_01] STOP(G-causal): 陽性対照に使える局が無い(この行を貼って相談)")
pc = shared[0]; e2 = dict(orig); W = np.array(np.asarray(orig["waveforms"], float))
W[pc[8], :, IP + n_avail(1.0, pc[4]) - 1] += 50.0 * np.abs(W[pc[8], :, IP:IP + 100]).max()
e2["waveforms"] = W; EVS[ie] = e2; [FILT.pop((ie, b), None) for b in SOS]
S1, _ = similarity(ie, 1.0, lib0, BAND, raw=True)
EVS[ie] = orig; [FILT.pop((ie, b), None) for b in SOS]
pos_ctrl = float(np.max(np.abs(S1 - S0))) if len(S0) else 0.0
print(f"[21_01] G-causal({len(gate_ev)} 地震 × τ = 1・2・3 s、未来の波形と検測を置き換えた時の最大の差): {gc_max:.3g}  "
      f"陽性対照(窓の最後の点を変えた時の S の差): {pos_ctrl:.3g}  " + ("PASS" if (gc_max == 0.0 and pos_ctrl > 0) else "FAIL"))
if not (gc_max == 0.0 and pos_ctrl > 0): stop("[21_01] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")

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
print(f"[21_01] G-phys(τ = ∞ の M5 の中央値 ≤ 0.5 km): {'—' if phys_inf is None else f'{phys_inf:.3f}'} km  " + ("PASS" if phys_inf is not None and phys_inf <= 0.5 else "FAIL")
      + "(参考: 15_12 は 0.13 km、分け方が違う)")
if not (phys_inf is not None and phys_inf <= 0.5): stop("[21_01] STOP(G-phys): 物理を鳥取に正しく移せていない可能性(この行を貼って相談)")
PER_TAU = {}
for j, t in enumerate(TL[:-1]):
    full = [m for m in BASE if SUMM[m][t]["available"] == 1.0 and SUMM[m][t]["median_km"] is not None]
    best = min(full, key=lambda m: SUMM[m][t]["median_km"])
    bm, cm = SUMM[best][t]["median_km"], SUMM["C3"][t]["median_km"]
    pr = paired("C3", best, j); floor = bm < FLOOR_KM
    win = (not floor) and cm < bm and pr["p"] is not None and pr["p"] < ALPHA and pr["n_nonzero"] >= MIN_NONZERO
    PER_TAU[t] = dict(judged=(t in JUDGED), best=best, best_median_km=bm, c3_median_km=cm, paired_vs_best=pr, floor=bool(floor),
                      win=bool(win), c3_at_or_below_0p7_best=bool(cm <= BAR * bm), vs_M6r=paired("C3", "M6r", j),
                      vs_M6p=paired("C3", "M6p", j), c3_fallback_frac=float(C3FB[:, j].mean()),
                      similarity_measured_frac=float(np.mean(NI[:, j] > 0)), stations_median=float(np.median(NST[:, j])))
nw = sum(PER_TAU[t]["win"] for t in JUDGED); nfl = sum(PER_TAU[t]["floor"] for t in JUDGED)
VERDICT = ("INCONCLUSIVE" if NT < MIN_TEST else "SIMILARITY-WINS" if nw == 3 else "SIMILARITY-PARTIAL" if nw >= 1
           else "PHYSICS-AT-FLOOR" if nfl == 3 else "SIMILARITY-NO")
if a.dev: VERDICT = "DEV (no verdict)"

def f2(v): return "—" if v is None else f"{v:.2f}"
def fp(p): return "—" if p is None else f"{p:.2g}"
print(f"\n[21_01] ===== 水平誤差の中央値 km [95% 区間](評価 {NT} 地震{'、dev(楽観的)' if a.dev else ''}) =====")
print("  方法           " + "".join(f"{('τ=' + t + ' s') if t != 'inf' else '全検測':>24}" for t in TL))
for m in METH:
    print(f"  {m:<15}" + "".join((f"{f2(SUMM[m][t]['median_km'])} [{f2(SUMM[m][t]['ci_lo'])},{f2(SUMM[m][t]['ci_hi'])}]"
                                   if SUMM[m][t]['median_km'] is not None else "—").rjust(24) for t in TL))
print("  P のある局の数(中央値) " + "  ".join(f"τ={t}: {np.median(NST[:, j]):.0f}" for j, t in enumerate(TL)))
for t, d in PER_TAU.items():
    pb = d["paired_vs_best"]
    print(f"  τ={t} s{'' if d['judged'] else '(記述)'}: BEST = {d['best']} {d['best_median_km']:.2f} km / C3 {d['c3_median_km']:.2f} km  "
          f"p(C3 < BEST) = {fp(pb['p'])}(差が 0 でない組 {pb['n_nonzero']}/{pb['n']})  WIN={d['win']}  FLOOR={d['floor']}  "
          f"0.7×BEST 以下={d['c3_at_or_below_0p7_best']}  p(C3 < M6r) = {fp(d['vs_M6r']['p'])}  p(C3 < M6p) = {fp(d['vs_M6p']['p'])}  "
          f"似ている度合いを測れた割合 {d['similarity_measured_frac']:.2f}・C3 が M6r に戻った割合 {d['c3_fallback_frac']:.2f}")
print(f"\n[21_01] 判定(事前宣言、τ = 1・2・3 s): {VERDICT}   (WIN の τ の数 {nw}/3、FLOOR の τ の数 {nfl}/3。τ = 0.5 s は記述だけ)")
print("[21_01] 限界: " + " / ".join(LIMITS))

# ---------------------------------------------------------------- 12. 出力(JSON・CSV を図より先に)
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, np.bool_): return bool(o)
    return o
CM = BASE + NEW + SENSN
with open(ROOT / f"data/21_01_per_event{SUF}.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["origin_time", "mj", "lat", "lon", "depth_km"] + [f"n_sta_t{t}" for t in TL] + [f"n_i_t{t}" for t in TL[:-1]]
               + [f"smax_t{t}" for t in TL[:-1]] + [f"best_template_sep_km_t{t}" for t in TL[:-1]] + [f"c3_fallback_t{t}" for t in TL[:-1]]
               + [f"{m}_err_t{t}" for m in CM for t in (TL if m in BASE else TL[:-1])])
    for i, ie in enumerate(EVAL):
        w.writerow([OT[ie], f"{MAG[ie]:.1f}", f"{SRC[ie,0]:.4f}", f"{SRC[ie,1]:.4f}", f"{SRC[ie,2]:.2f}"] + [int(v) for v in NST[i]]
                   + [int(v) for v in NI[i]] + [("" if not np.isfinite(v) else f"{v:.4f}") for v in SMAX[i]]
                   + [("" if not np.isfinite(v) else f"{v:.3f}") for v in BESTSEP[i]] + [int(v) for v in C3FB[i]]
                   + [("" if not np.isfinite(E[m][i, j]) else f"{E[m][i, j]:.4f}") for m in CM
                      for j in (range(len(TL)) if m in BASE else range(len(TAUS)))])
out = dict(script="21_01_tottori_similarity_prior_early_location.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
           suffix=SUF, cache=a.cache, cache_sha256=sha256(CP), n_events=NE, n_pool=int(len(pool_idx)), n_test=int(len(test_idx)),
           n_no_measured_p=int((~HASP).sum()), n_evaluated=NT, mainshock=dict(origin_time=OT[im], mj=float(MAG[im])),
           pool_cut_utc_ns=int(CUT_NS),
           fixed=dict(taus=TAUS, judged_taus=JUDGED, pool_h=POOL_H, buffer_h=BUFFER_H, band_hz=BAND, band_sens_hz=BAND_SENS, pre_s=PRE_S,
                      min_win_s=MIN_WIN_S, max_win_s=MAX_WIN_S, max_lag_s=MAX_LAG_S, topk=TOPK, topk_sens=TOPK_SENS, min_pos=MIN_POS,
                      buffer_sens_h=BUFFER_SENS_H, s_weight=S_WEIGHT, shrink=SHRINK, min_prior_ev=MIN_PRIOR_EV, prior_eps=PRIOR_EPS,
                      floor_km=FLOOR_KM, min_test=MIN_TEST, alpha=ALPHA, min_nonzero=MIN_NONZERO, bar=BAR, nboot=NBOOT, seed=SEED,
                      eps_t=EPS_T),
           velocity=dict(v0=V0, k=KG, vpvs=VPVS), laplace_b_s=LAP_B, kde_h_km=KDE_H, grid=dict(H_km=H, step_km=STEP, finest_km=STEP / 25,
                                                                                               zmax_km=ZMAX, zfix_km=ZDEF),
           gates=dict(split="PASS", lib="PASS (checked for every evaluated event)", causal=dict(max_diff=gc_max, positive_control=pos_ctrl,
                      n_checks=gc_n, events=[OT[EVAL[i]] for i in gate_ev]), physics_inf_median_km=phys_inf),
           summary=SUMM, per_tau=PER_TAU, verdict=VERDICT, n_win=int(nw), n_floor=int(nfl),
           verdict_rule="per tau: BEST = smallest median among the 9 AI-free methods that give an estimate for every evaluated event "
                        "(chosen on the evaluated events); WIN = C3 median < BEST median and one-sided paired Wilcoxon (zero_method="
                        "'wilcox') p < 0.01 with >= 10 non-zero pairs, not FLOOR (BEST < 0.5 km); judged at tau = 1, 2, 3 s; "
                        "WINS = 3/3, PARTIAL = 1-2/3, PHYSICS-AT-FLOOR = 0/3 and all three FLOOR, NO = otherwise 0/3, "
                        "INCONCLUSIVE if fewer than 30 evaluated events; tau = 0.5 s descriptive",
           limits=LIMITS, runtime_s=time.time() - T0)
json.dump(clean(out), open(ROOT / f"models/21_01_judgment{SUF}.json", "w"), indent=1)
if not a.dev: log_open("completed: " + VERDICT)

# ---------------------------------------------------------------- 13. 図(白背景・英語・凡例は枠外)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 10})
LAB = {"M0r": "Past-event centroid", "Mp10": "Centroid of previous 10 events", "M1": "First-P station",
       "M2": "Centroid of triggered stations", "M3r": "Seismicity prior (same first station)", "M5": "Physics only (solved events only)",
       "M5f": "Physics, first-station fallback", "M6p": "Physics x prior (pool events)", "M6r": "Physics x prior (past events)",
       "C2": "Waveform similarity only (median of top events; non-fallback events)", "C3": "Physics x similarity prior (C3, judged)"}
STY = {"M0r": ("0.6", ":"), "Mp10": ("0.4", ":"), "M1": ("tab:brown", "--"), "M2": ("tab:olive", "--"), "M3r": ("tab:purple", "-."),
       "M5": ("tab:blue", ":"), "M5f": ("tab:green", "--"), "M6p": ("tab:cyan", "--"), "M6r": ("tab:blue", "-"),
       "C2": ("tab:orange", "--"), "C3": ("tab:red", "-")}
xs = np.array(TAUS); TT = TL[:-1]
def arr(m, key): return np.array([np.nan if SUMM[m][t][key] is None else SUMM[m][t][key] for t in TT])
fig, ax = plt.subplots(figsize=(9.0, 4.8))
for m in ["M0r", "Mp10", "M1", "M2", "M3r", "M5", "M5f", "M6p", "M6r", "C2", "C3"]:
    c, ls = STY[m]
    ax.plot(xs, arr(m, "median_km"), ls, color=c, marker="o", ms=4, lw=2.4 if m == "C3" else 1.3, label=LAB[m])
    ax.fill_between(xs, arr(m, "ci_lo"), arr(m, "ci_hi"), color=c, alpha=0.08, lw=0)
for t, x in zip(TT, xs):
    ax.plot([x], [PER_TAU[t]["best_median_km"]], marker="s", ms=9, mfc="none", mec="k", ls="none",
            label="BEST AI-free method at each tau" if t == TT[0] else None)
ax.axhline(FLOOR_KM, color="k", lw=0.8, ls="--")
ax.text(xs[-1] / 1.03, FLOOR_KM * 1.06, f"floor {FLOOR_KM} km", fontsize=8, ha="right", va="bottom")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xticks(xs); ax.set_xticklabels([f"{t:g}" + (" (desc.)" if f"{t:g}" not in JUDGED else "") for t in TAUS])
ax.minorticks_off()
ax.set_xlabel("Time since first P pick, tau (s)"); ax.set_ylabel("Median epicentral error vs JMA (km)")
ax.set_title(f"West Tottori 2026, {'DEV (pool events, optimistic)' if a.dev else 'test events'}, n = {NT}; shading = 95% bootstrap CI",
             fontsize=10)
ax.grid(alpha=0.3, which="both"); ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_01_F1_error_vs_tau{SUF}.pdf", bbox_inches="tight"); plt.close(fig)

fig, axs = plt.subplots(1, len(TT), figsize=(3.3 * len(TT), 3.8), sharey=True)
for ax, t, j in zip(np.atleast_1d(axs), TT, range(len(TT))):
    b = PER_TAU[t]["best"]; d = E["C3"][:, j] - E[b][:, j]; d = np.sort(d[np.isfinite(d)])
    ax.plot(d, np.arange(1, len(d) + 1) / max(len(d), 1), color="tab:red", drawstyle="steps-post")
    ax.axvline(0, color="k", lw=0.8)
    tied = PER_TAU[t]["paired_vs_best"]["frac_tied"]
    ax.set_title(f"tau = {t} s{'' if t in JUDGED else ' (descriptive)'}\nC3 minus {b}; tied {0 if tied is None else tied:.0%}", fontsize=9)
    ax.set_xlabel("Error difference (km); < 0 = C3 better"); ax.grid(alpha=0.3)
np.atleast_1d(axs)[0].set_ylabel("Fraction of events")
fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_01_F2_paired_difference{SUF}.pdf", bbox_inches="tight"); plt.close(fig)

fig, ax = plt.subplots(figsize=(7.6, 4.4))
for j, (t, c) in enumerate(zip(TT, ("tab:green", "tab:blue", "tab:orange", "tab:red"))):
    m = np.isfinite(SMAX[:, j]) & np.isfinite(BESTSEP[:, j])
    ax.scatter(SMAX[m, j], np.maximum(BESTSEP[m, j], 0.01), s=14, color=c, alpha=0.7, label=f"tau = {t} s")
ax.set_xlabel("Best similarity score S (0-1)"); ax.set_ylabel("Epicentral distance to most similar past event (km)\n(values < 0.01 km shown at 0.01)")
ax.set_yscale("log"); ax.grid(alpha=0.3, which="both")
ax.set_title("Is the most similar past event close by?", fontsize=10)
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_01_F3_similarity_vs_separation{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
print(f"[21_01] 出力: models/21_01_judgment{SUF}.json, data/21_01_per_event{SUF}.csv, PDF/21_01_F1〜F3{SUF}.pdf"
      + ("" if a.dev else ", models/21_01_opened.json") + f"  ({time.time()-T0:.0f} s)")
