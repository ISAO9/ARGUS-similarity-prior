#!/usr/bin/env python3
# =============================================================================
# Script : 24_03_nagano2014_realpick_cache_colab.py  (v1)
#          [長野県北部 2014 の h5(24_02)と気象庁の震源(24_01)から、PhaseNet で P・S を測り、ARGUS のキャッシュ
#           (tottori_parsed_realpick_nagano2014_m15.pt)を作る。検測・QC・局の選び方・組み立て・振幅整合は 15_01c v3.3 と同じ計算]
# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の 3 つ目
# 派生元 : 21_20c_osaka2018_realpick_cache_colab.py v1(SHA-256 7b938b944003d99fcad7df188792e8e8eb95c71b07f1a1223bffad6671d04cf0)。
#          検測・QC・組み立て・振幅整合・出力の中身は 21_20c v1(= 15_01c v3.3 と同じ計算)と 1 字も変えていない(DIFF_LOG_24.md)。
#          変えたのは次だけ: (1) この冒頭の説明 (2) 出力の置き場所の既定 ARGUS_osaka2018 → ARGUS_nagano2014(Colab では --base で必ず渡す)
#          (3) 引数の説明の文 (4) 表示の先頭 [24_03] → [24_03]、報告の script_version、図の題、最後の表示の Mac のコピー先
#          (--tag に nagano2014 があれば data/nagano2014_processed/)、振幅整合の表示の「大阪」→「長野」。
#          24_02 の h5 には win_mean・win_std も入っているが、このスクリプトは読まない(waves だけを読む。21_20c と同じ)。
#          このキャッシュの後に 24_03h(R1: 発生の 15 s 前〜5 s 後に別の地震がある地震を除く)を必ず当てる(事前登録 24 の 3 節)。
# 長野県北部 2014 の実行(ノート 24_nagano2014_colab.ipynb の セル N10・N11):
#   !python 24_03_nagano2014_realpick_cache_colab.py --h5 <nagano2014_100Hz.h5(または _FAILED.h5)> --jma <jma_nagano2014.csv>
#      --stations <stations_nagano2014.csv(または .csv.part)> --min-mag 1.5 --box <24_01 の JSON の box 4 つ>
#      --base /content/ARGUS_nagano2014 --tag _nagano2014_m15 [--max-events 10 で煙試験。その時は --tag _nagano2014_smoke]
#
# ---- 以下は 15_01c v3.3 の説明(そのまま) ----
# Script : 15_01c_tottori_realpick_cache_colab.py  [鳥取2026 キャッシュ構築 Colab版 v3.3]
# v3.3変更(2026-10-27、21_04 の 2 つ目の系列(鳥取県中部 2016)用): 検測・QC・組み立て・振幅整合は v3 と 1 字も変えていない。
#   変えたのは次の 2 点だけ:
#   (1) 窓の索引(h5 の窓の並び)の保存ファイル: v3.2 までは h5 によらず OUTD/h5_index.npz で、別の h5 を渡すと前の h5 の
#       索引を読んでしまう誤りがあった。v3.3 では tottori_all_100Hz.h5 の時だけ従来の名前 h5_index.npz、それ以外は
#       h5_index_<h5 の名前>.npz に書く。索引に h5 の窓の中身の指紋(局の名前と窓の始まりの並びの SHA-1)を入れ、読む時に
#       今の h5 の指紋と同じかを確かめる(指紋が無い古い索引や、違う索引は作り直す。鳥取 2026 でも 1 回だけ作り直す)
#   (2) 出力の置き場所 --base(既定は従来どおり Drive の ARGUS_tottori)。鳥取県中部 2016 は --base で ARGUS_ct2016 に分ける
#   (3) 最後の表示で、Mac のどこにコピーするか(--tag に ct2016 があれば data/ct2016_processed/)
#   鳥取県中部 2016 の実行(ノート 21_04_ct2016_colab.ipynb の セル 10・11):
#     !python 15_01c_tottori_realpick_cache_colab.py --h5 <ct2016_100Hz.h5> --jma <jma_ct2016.csv> --stations <stations_ct2016.csv>
#        --min-mag 1.5 --box <21_04a の JSON の box 4 つ> --base /content/drive/MyDrive/ARGUS_ct2016 --tag _ct2016_m15 [--max-events 10]
# v3.1・v3.2変更(2026-10-27、21_02 の確認試験用): 出力の名前に付ける --tag と、正本を上書きしないための止める条件を
#   足しただけ。検測・QC・組み立て・振幅整合は v3 と 1 字も変えていない。--tag を付けない時の .pt と図は v3 と同じ名前・
#   同じ中身(報告の JSON に script_version・script_sha256 と、args に "tag"・"overwrite_canon" が増える)。
#   止める条件: (1) --min-mag が 2.0 以外で --tag が空 (2) --tag が空で、出力の tottori_parsed_realpick.pt が既にある
#   (--overwrite-canon を付けた時だけ上書きする)。煙試験(--max-events 10)は --tag _smoke を付けて回す。
#   出力: tottori_parsed_realpick{tag}.pt / 15_01c_build_report{tag}.json / 15_01c_tottori_picks_qc{tag}.pdf
#   h5_index.npz(h5 の窓の索引)は tag によらず共有する(カタログ・Mj・tag に依存しない)(v3.3 からは h5 ごとに別の索引)
#   M>=1.5 版の実行(セル4・5の代わり):
#     セル4': !python 15_01c_tottori_realpick_cache_colab.py --min-mag 1.5 --tag _m15smoke --max-events 10 --h5 <セル2のパス>
#     セル5': !python 15_01c_tottori_realpick_cache_colab.py --min-mag 1.5 --tag _m15 --h5 <セル2のパス>
# v3変更(15_01d診断の帰結、2026-10-15):
#   (1) 時刻基準: h5のwindow_epochはJST基準epochと確定(時刻プローブで本震が
#       +9hで全局点火) → 窓引きをJST基準に(--h5-time-base jst 既定)。
#       キャッシュのorigin_timeは真のUTCのまま保存。
#   (2) 検測の最早優先化: PhaseNetのP/Sを「最高確率」でなく「閾値以上で最早の
#       P → そのPより後で最早のS」に変更(余震系列で後続イベントを掴む事故防止)。
#   (3) セグメント短縮: origin+70s→+45s(最遠107 kmでS≈31 s。余震混入と計算量減)。
#       P QCは0.5–30 sに。
#   (4) 開示: h5波形は窓ごとz-score正規化済み(15_01d: 窓stdCV=0.000)。
#       振幅は物理量でない(相対振幅も窓間で非保存)ことをreportに明記。
# 派生元: 15_01 v2.2 — 検測・QC・組み立てロジックは完全同一。変更は3点のみ:
#   (1) 入出力パスをColab/Drive既定に
#   (2) K-NET参照キャッシュの代わりに --knet-absmax-ref(Mac実測値 20.51)を使用
#   (3) 出力(.pt/JSON/PDF)をDriveに保存 → Macへコピーして15_02を実行
#
# 実行セル(この順で):
#   セル1: from google.colab import drive; drive.mount('/content/drive')
#          !pip -q install seisbench obspy
#   セル2: !find /content/drive/MyDrive -name "tottori_all_100Hz.h5" 2>/dev/null
#          (出たパスを下のH5に使う)
#   セル3: 左のファイルペインに jma_tottori_2026.csv と stations.csv をアップロード
#          (または Drive上のパスを --jma/--stations で指定)
#   セル4: !python 15_01c_tottori_realpick_cache_colab.py --max-events 10 --tag _smoke --h5 <セル2のパス>(v3.2: 煙試験は tag 付き)
#   セル5: !python 15_01c_tottori_realpick_cache_colab.py --h5 <セル2のパス>(v3.2: 正本が既にある時は止まる。作り直す時だけ --overwrite-canon)
#   → 出力: /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/
#            tottori_parsed_realpick.pt をMacの SWIFT/data/tottori_processed/ へコピー
# Project: ARGUS (15系 = 熊本→鳥取 国内地域横断ゼロショット転移)
#
# Description:
#   2026年西鳥取系列(Hi-net等50局・SERAPH_V4資産)から、ARGUSの
#   knet_parsed_realpick.pt と同一スキーマのイベントキャッシュ
#   tottori_parsed_realpick.pt を構築する。モデルは一切触らない(構築のみ)。
#
#   設計(全て既存実装の流用・一次資料準拠):
#     - 正解カタログ: JMA一元化 (jma_tottori_2026.csv, JST) → UTC(-9h)変換
#     - 波形源: tottori_all_100Hz.h5 (30 s窓×445万, window_epoch=絶対秒,
#       attrs.channel_order='UD,NS,EW', fs=100) — 連続窓を継ぎ足して
#       イベント毎に [origin-10 s, origin+45 s] のセグメントを組み立てる(v3 で +70 s から短縮)
#     - 検測: SeisBench PhaseNet("original") — 14_23と同一。PN不検出時は
#       14_23の classic (STA/LTA+AIC) にフォールバックし品質降格
#     - 和達QC・イベント内中央値補完・tp/spのQC範囲: 14_23と同一実装を移植
#     - 局選択(ラベル不使用): 実測P絶対時刻の早い順に最大 --max-sta 局
#       (v2: パディング無しで実局のみ保存。局数スイープは15_02側で実施)
#       (近い局ほど先に到達する物理で選ぶ。カタログ距離は選択に使わない)
#     - 波形窓: 各局の実測Pを基準に [tP-3 s, tP+17.48 s] の T=2048 サンプル
#     - Hi-net速度→擬似加速度: 時間微分(既定ON、--no-differentiate で切替)
#     - 振幅スケール: K-NETキャッシュの per-station absmax 中央値(95.29)に
#       データセット一括係数で整合(--amp-mode match_knet 既定 / physical)
#     - snr特徴: K-NETキャッシュでは≈1.0のほぼ定数(本スクリプトが全件統計を
#       印字して開示)。既定 const1(=1.0固定)。--snr-mode prms でP前後RMS比
#     - 成分順: 出力キャッシュの成分軸は --comp-order (既定 "UD,NS,EW")。
#       ※Step 0のgrep結果(13_01の合成データ成分順)と一致させること
#     - mw欄にはJMAのMj を格納(F-net Mwではない — 評価側・原稿で明記)
#
#   Inputs : --jma      SERAPH_V4/data/catalog/jma_tottori_2026.csv
#            --stations SERAPH_V4/data/catalog/stations.csv
#            --h5       /Volumes/FISSION_SSD/2026WTottori/data/waves/tottori_all_100Hz.h5
#            --knet-cache data/knet_processed/knet_parsed_realpick.pt (スキーマ/振幅参照)
#   Outputs: data/tottori_processed/tottori_parsed_realpick{tag}.pt(Colab では Drive/ARGUS_tottori/ の下)
#            data/tottori_processed/h5_index.npz (h5窓索引キャッシュ、再実行高速化。v3.3: tottori_all_100Hz.h5 以外は h5_index_<名前>.npz)
#            models/locator/15_01c_build_report{tag}.json (全開示統計)
#            PDF/15_01c_tottori_picks_qc{tag}.pdf (S-P vs 距離・和達傾き)
#
#   Usage  : cd /Users/isaokurosawa/SWIFT
#            uv run python src/15_01_tottori_realpick_cache.py --max-events 10   # 煙試験
#            uv run python src/15_01_tottori_realpick_cache.py                   # 本番 M>=2.0
#            (以上は Mac 版 15_01 の使い方。Colab 版の M>=1.5 は冒頭のセル4'・5' のとおり --tag を付ける)
# =============================================================================
import sys, json, argparse
from pathlib import Path
from datetime import datetime, timedelta, timezone
import numpy as np
import torch
from scipy.signal import butter, sosfilt, find_peaks

BASE = Path("/content/drive/MyDrive/ARGUS_nagano2014") \
       if Path("/content/drive").exists() else Path(".") / "ARGUS_nagano2014"     # 24_03: 既定の置き場所(--base で渡す)
PDFD = BASE / "PDF"
MODD = BASE / "models" / "locator"
OUTD = BASE / "data" / "tottori_processed"
ROOT = Path(".")

FS = 100.0
T_OUT = 2048                       # K-NETキャッシュと同一の窓長(20.48 s)
P_PRE_S = 3.0                      # 窓はP基準: [tP-3, tP+17.48]
SEG_PRE, SEG_POST = 10.0, 45.0     # 検測用セグメント: [origin-10, origin+45](v3 で +70 から短縮)
BP_LO, BP_HI = 1.0, 15.0           # 14_23と同一(因果バンドパス)
STA_S, LTA_S = 0.5, 5.0
TRIG_RATIO = 3.0
AIC_HALF_S = 1.0
S_STA, S_LTA = 1.0, 8.0
S_MIN_LAG, S_MAX_LAG = 0.5, 45.0
P_SNR_MIN, S_SNR_MIN = 2.0, 1.5
PN_PROB_MIN = 0.3                  # 14_23と同一
TP_QC = (0.5, 30.0)                # 原点相対P QC(最遠~107 kmでP≲19 s)
SP_QC = (0.3, 15.0)                # 14_23と同一(近地網の幾何上限)
KNET_ABSMAX_REF = None             # 実測で埋める(参照キャッシュから)

ap = argparse.ArgumentParser()
ap.add_argument("--jma", required=True, help="24_01 の jma_nagano2014.csv(24_03: 必ず渡す)")
ap.add_argument("--stations", required=True, help="24_02 の stations_nagano2014.csv(24_03: 必ず渡す)")
ap.add_argument("--h5", required=True, help="24_02 の nagano2014_100Hz.h5 のパス")
ap.add_argument("--knet-cache", default="", help="(任意)あればフル統計を開示")
ap.add_argument("--knet-absmax-ref", type=float, default=20.51,
                help="K-NET per-station absmax中央値(Mac実測 2026-10-15: 20.51)")
ap.add_argument("--min-mag", type=float, default=2.0)
ap.add_argument("--max-sta", type=int, default=24,
                help="保存する最大局数(実測P早い順)。パディングはしない")
ap.add_argument("--max-events", type=int, default=0, help="0=全件")
ap.add_argument("--picker", choices=["phasenet", "classic"], default="phasenet")
ap.add_argument("--comp-order", default="UD,NS,EW",
                help="出力キャッシュの成分軸順。Step 0(13_01のgrep)に合わせる")
ap.add_argument("--no-differentiate", action="store_true",
                help="Hi-net速度→加速度の時間微分を行わない")
ap.add_argument("--amp-mode", choices=["match_knet", "physical"], default="match_knet")
ap.add_argument("--snr-mode", choices=["const1", "prms"], default="const1")
ap.add_argument("--h5-time-base", choices=["jst", "utc"], default="jst",
                help="window_epochの基準。実h5はJST基準と確定(15_01dプローブ)")
ap.add_argument("--box", nargs=4, type=float, required=True,
                metavar=("LAT0", "LAT1", "LON0", "LON1"),
                help="24_01 の JSON の box(24_03: 必ず渡す。西鳥取の既定は外した)")
ap.add_argument("--tag", default="", help="出力の名前に付ける印(例 _m15)。v3.1 で追加")
ap.add_argument("--overwrite-canon", action="store_true", help="--tag 無しで既存の正本を上書きする時だけ付ける。v3.2 で追加")
ap.add_argument("--base", default="", help="出力の置き場所(既定は Drive の ARGUS_nagano2014)。v3.3 で追加")
args = ap.parse_args()
if args.base:
    BASE = Path(args.base)
    PDFD = BASE / "PDF"; MODD = BASE / "models" / "locator"; OUTD = BASE / "data" / "tottori_processed"
for _d in (PDFD, MODD, OUTD): _d.mkdir(parents=True, exist_ok=True)
if abs(args.min_mag - 2.0) > 1e-9 and args.tag == "":
    raise SystemExit("[24_03] STOP: --min-mag が 2.0 以外の時は --tag(例 _m15)を付ける(正本を上書きしないため)")
if args.tag == "" and (OUTD / "tottori_parsed_realpick.pt").exists() and not args.overwrite_canon:
    raise SystemExit("[24_03] STOP: 正本 tottori_parsed_realpick.pt が既にある。--tag を付けて回す"
                     "(正本を作り直す時だけ --overwrite-canon)")

SOS = butter(4, [BP_LO, BP_HI], btype="band", fs=FS, output="sos")
JST = timezone(timedelta(hours=9))

# ============================================================ 14_23移植: 検測器
def sta_lta(x, sta_n, lta_n):
    c = np.cumsum(x * x)
    sta = (c[sta_n:] - c[:-sta_n]) / sta_n
    lta = (c[lta_n:] - c[:-lta_n]) / lta_n
    n = min(len(sta) - (lta_n - sta_n), len(lta))
    r = np.zeros(len(x)); i0 = lta_n
    r[i0:i0 + n] = sta[lta_n - sta_n:lta_n - sta_n + n] / (lta[:n] + 1e-12)
    return r

def aic_curve(x):
    x = np.asarray(x, float); N = len(x)
    i = np.arange(1, N)
    c1, c2 = np.cumsum(x), np.cumsum(x * x)
    v1 = np.maximum((c2[:-1] - c1[:-1]**2 / i) / i, 1e-12)
    tn = N - i
    v2 = np.maximum(((c2[-1] - c2[:-1]) - (c1[-1] - c1[:-1])**2 / tn) / tn, 1e-12)
    a = i * np.log(v1) + tn * np.log(v2)
    a[:8] = np.inf; a[-8:] = np.inf
    return a

def aic_refine(x, i_trig, half_n):
    lo, hi = max(8, i_trig - half_n), min(len(x) - 8, i_trig + half_n)
    if hi - lo < 24: return i_trig
    a = aic_curve(x[lo:hi])
    return lo + 1 + int(np.argmin(a))

def pick_p(ud):
    f = sosfilt(SOS, ud)
    r = sta_lta(f, int(STA_S * FS), int(LTA_S * FS))
    i0 = int(LTA_S * FS) + 1
    cand = np.where(r[i0:] >= TRIG_RATIO)[0]
    fallback = False
    if len(cand): i_trig = i0 + cand[0]
    else: i_trig = i0 + int(np.argmax(r[i0:])); fallback = True
    i_p = aic_refine(f, i_trig, int(AIC_HALF_S * FS))
    pre = f[max(0, i_p - int(1.0 * FS)):i_p]
    post = f[i_p:i_p + int(1.0 * FS)]
    snr = float(np.sqrt((post**2).mean() + 1e-12) / np.sqrt((pre**2).mean() + 1e-12)) \
          if len(pre) > 10 and len(post) > 10 else 0.0
    if snr < P_SNR_MIN: fallback = True
    return i_p, snr, fallback

def pick_s(ew, ns, ud, i_p):
    fe, fn_ = sosfilt(SOS, ew), sosfilt(SOS, ns)
    fz = sosfilt(SOS, ud)
    w = max(3, int(0.2 * FS)); k1 = np.ones(w) / w
    envH = np.convolve(np.sqrt(fe**2 + fn_**2), k1, "same")
    envZ = np.convolve(np.abs(fz), k1, "same")
    lo = i_p + int(S_MIN_LAG * FS)
    hi = min(len(envH) - 10, i_p + int(S_MAX_LAG * FS))
    if hi - lo < int(1.0 * FS): return None, 0.0, True
    seg = envH[lo:hi]; gmax = seg.max()
    pref = envH[i_p:i_p + int(0.8 * FS)].max() + 1e-12
    if gmax < 1.5 * pref: return None, 0.0, True
    pks, _ = find_peaks(seg, height=0.35 * gmax, distance=int(0.5 * FS))
    anchor = None
    for pk in pks:
        j = lo + pk
        hh = envH[max(0, j - int(0.3 * FS)): j + int(0.3 * FS)].mean()
        vv = envZ[max(0, j - int(0.3 * FS)): j + int(0.3 * FS)].mean() + 1e-12
        if envH[j] >= 1.5 * pref and hh / vv >= 1.3:
            anchor = j; break
    if anchor is None: anchor = lo + int(np.argmax(seg))
    a_lo = max(i_p + int(0.2 * FS), anchor - int(6.0 * FS))
    a_hi = min(len(envH) - 2, anchor + int(0.3 * FS))
    if a_hi - a_lo < int(0.6 * FS): return None, 0.0, True
    a = aic_curve(np.log(envH[a_lo:a_hi] + 1e-10))
    i_s = a_lo + 1 + int(np.argmin(a))
    if i_s <= i_p + int(0.2 * FS): return None, 0.0, True
    pre = envH[max(0, i_s - int(2.0 * FS)):i_s]
    post = envH[i_s:i_s + int(2.0 * FS)]
    snr = float(post.mean() / (pre.mean() + 1e-12)) if len(pre) > 10 else 0.0
    return i_s, snr, (snr < S_SNR_MIN)

def ts_fit(xx, yy):
    ss = [(yy[j] - yy[i]) / (xx[j] - xx[i])
          for i in range(len(xx)) for j in range(i + 1, len(xx))
          if abs(xx[j] - xx[i]) > 0.3]
    if not ss: return None, None
    aa = float(np.median(ss)); bb = float(np.median(yy - aa * xx))
    return aa, bb

# ---------------------------------------------------------- PhaseNet(14_23同一)
PN_MODEL = None
obspy = None
def init_phasenet():
    global PN_MODEL, obspy
    import seisbench.models as sbm
    import obspy as _ob
    obspy = _ob
    PN_MODEL = sbm.PhaseNet.from_pretrained("original")
    PN_MODEL.eval()
    print("[24_03] PhaseNet ('original') 読込完了")

def phasenet_pick_event(seg_by_sta):
    """seg_by_sta: sta -> dict(t0_epoch, data{UD,NS,EW})。sta->{P:(epoch秒,prob),S:…}"""
    st = obspy.Stream()
    for scode, rec in seg_by_sta.items():
        for cname, ch in (("UD", "Z"), ("NS", "N"), ("EW", "E")):
            tr = obspy.Trace(np.ascontiguousarray(rec["data"][cname], np.float32))
            tr.stats.sampling_rate = FS
            tr.stats.starttime = obspy.UTCDateTime(rec["t0_epoch"])
            tr.stats.network, tr.stats.station = "TT", scode.replace(".", "_")[:5]
            tr.stats.channel = "HH" + ch
            st.append(tr)
    out, name_map = {}, {s.replace(".", "_")[:5]: s for s in seg_by_sta}
    try:
        picks = PN_MODEL.classify(st).picks
    except Exception as e:
        print(f"    [PN] classify失敗: {e}"); return out
    for pk in picks:
        sc = name_map.get(pk.trace_id.split(".")[1])
        if sc is None: continue
        ph = pk.phase.upper()
        if ph in ("P", "S"):
            out.setdefault(sc, {}).setdefault(ph, []).append(
                (float(pk.peak_time.timestamp), float(pk.peak_value)))
    for d in out.values():
        for ph in d: d[ph].sort()          # 時刻順
    return out

# ================================================================ 入力読み込み
print(f"[24_03] JMAカタログ: {args.jma}")
import csv as _csv
cat, n_badrow = [], 0
with open(args.jma) as f:
    for row in _csv.DictReader(f):
        try:
            la, lo_, dp, mg = (float(row["latitude"]), float(row["longitude"]),
                               float(row["depth_km"]), float(row["mag"]))
        except (ValueError, TypeError, KeyError):
            n_badrow += 1; continue   # JMA一元化はmag/depth空欄行があり得る
        b = args.box
        if not (b[0] <= la <= b[1] and b[2] <= lo_ <= b[3]): continue
        if mg < args.min_mag: continue
        t_jst = datetime.strptime(row["time"][:21].ljust(21, "0"),
                                  "%Y-%m-%d %H:%M:%S.%f")
        t_utc = t_jst.replace(tzinfo=JST).astimezone(timezone.utc).replace(tzinfo=None)
        frame_ep = (t_jst.replace(tzinfo=timezone.utc).timestamp()
                    if args.h5_time_base == "jst"
                    else t_utc.replace(tzinfo=timezone.utc).timestamp())
        cat.append(dict(origin_utc=t_utc, frame_ep=frame_ep,
                        lat=la, lon=lo_, dep=dp, mag=mg))
cat.sort(key=lambda e: e["origin_utc"])
if args.max_events: cat = cat[:args.max_events]
print(f"[24_03] 対象イベント: {len(cat)} (M>={args.min_mag}, box={args.box}, "
      f"JST→UTC変換済み, h5窓引き={args.h5_time_base}基準, 欠損行スキップ {n_badrow})")
if not cat: sys.exit("[24_03] STOP: 対象イベント0件")

sta_meta = {}
with open(args.stations) as f:
    for row in _csv.DictReader(f):
        sta_meta[row["id"].strip()] = (float(row["latitude"]), float(row["longitude"]),
                                       float(row["elevation"]))
print(f"[24_03] 観測点: {len(sta_meta)}局 ({Path(args.stations).name})")

# ---- K-NET参照: キャッシュがあればフル統計、無ければMac実測の基準値 ----
kpath = Path(args.knet_cache) if args.knet_cache else Path("/nonexistent")
if kpath.exists():
    kevs = torch.load(kpath, map_location="cpu", weights_only=False)
    k_absmax = np.array([np.abs(np.asarray(e["waveforms"], float)).max(axis=(1, 2))
                         for e in kevs]).ravel()
    k_snr = np.concatenate([np.asarray(e["snr"], float).ravel() for e in kevs])
    KNET_ABSMAX_REF = float(np.median(k_absmax))
    nan_frac = float(np.isnan(k_snr).mean())
    print(f"[24_03] K-NET参照: {len(kevs)}ev  absmax中央値={KNET_ABSMAX_REF:.2f}  "
          f"snr分布(NaN率{nan_frac:.1%}; 13_34rpではNaN→0) "
          f"min={np.nanmin(k_snr):.3f} med={np.nanmedian(k_snr):.3f} "
          f"p95={np.nanpercentile(k_snr,95):.3f} max={np.nanmax(k_snr):.3f}"
          f"  ← snr-mode判断の開示")
else:
    KNET_ABSMAX_REF = float(args.knet_absmax_ref)
    print(f"[24_03] K-NET参照: --knet-absmax-ref={KNET_ABSMAX_REF} を使用 "
          f"(Mac実測 2026-10-15、キャッシュ本体は不要)")

# ---- h5窓索引(初回のみ構築、npzにキャッシュ) ----
import h5py
idx_path = OUTD / ("h5_index.npz" if Path(args.h5).name == "tottori_all_100Hz.h5"
                   else f"h5_index_{Path(args.h5).stem}.npz")        # v3.3: h5 ごとの索引
H5 = h5py.File(args.h5, "r")
ch_order_h5 = str(H5.attrs.get("channel_order", "UD,NS,EW"))
n_samp_h5 = int(H5.attrs.get("n_samples", 3000))
print(f"[24_03] h5: channel_order={ch_order_h5}  n_samples={n_samp_h5}")
st_raw = H5["stations"][:]
ep_raw = H5["window_epoch"][:]
st_arr = np.array([s.decode() if isinstance(s, bytes) else str(s) for s in st_raw])
import hashlib as _hl
_fp = _hl.sha1("\n".join(st_arr.tolist()).encode() + np.asarray(ep_raw, np.float64).tobytes()).hexdigest()   # v3.3: 窓の中身の指紋
_idx_ok = False
if idx_path.exists():
    z = np.load(idx_path, allow_pickle=True)
    _idx_ok = ("fp" in z.files) and (str(z["fp"]) == _fp)
    if _idx_ok:
        sta_names, sta_ptr = list(z["names"]), z["ptr"]
        ep_sorted, row_sorted = z["ep"], z["row"]
    print(f"[24_03] 窓索引をキャッシュから読込: {idx_path.name}" if _idx_ok
          else f"[24_03] 窓索引 {idx_path.name} は今の h5 のものでない(指紋が無いか違う)ので作り直す")
if not _idx_ok:
    print("[24_03] 窓索引を構築中(初回のみ・数分)…")
    order = np.lexsort((ep_raw, st_arr))
    st_s, ep_sorted, row_sorted = st_arr[order], ep_raw[order], order.astype(np.int64)
    sta_names, starts = np.unique(st_s, return_index=True)
    sta_names = list(sta_names)
    sta_ptr = np.append(starts, len(st_s))
    np.savez(idx_path, names=np.array(sta_names, object), ptr=sta_ptr,
             ep=ep_sorted, row=row_sorted, fp=np.array(_fp))
    print(f"[24_03] 窓索引を保存: {idx_path.name} ({len(sta_names)}局)")
del st_raw, ep_raw, st_arr
sta_slice = {n: (int(sta_ptr[i]), int(sta_ptr[i + 1])) for i, n in enumerate(sta_names)}

CH_IDX = {c: i for i, c in enumerate(ch_order_h5.split(","))}

def get_segment(sta, t_a, t_b):
    """局staの絶対秒[t_a,t_b]を覆う連続セグメントを窓の継ぎ足しで返す。
    返り値: (t0_epoch, {UD,NS,EW: ndarray}) / 覆えなければ None"""
    if sta not in sta_slice: return None
    a, b = sta_slice[sta]
    ep = ep_sorted[a:b]; rows = row_sorted[a:b]
    sel = (ep > t_a - 30.0 - 1e-6) & (ep < t_b + 1e-6)
    if not sel.any(): return None
    ep_s, rows_s = ep[sel], rows[sel]
    o = np.argsort(ep_s); ep_s, rows_s = ep_s[o], rows_s[o]
    # 連続性(30 s刻み)チェック
    if ep_s[0] > t_a + 1e-3: return None
    if ep_s[-1] + 30.0 < t_b - 1e-3: return None
    if len(ep_s) > 1 and np.any(np.abs(np.diff(ep_s) - 30.0) > 0.02): return None
    t0 = float(ep_s[0])
    n_tot = int(round((ep_s[-1] + 30.0 - t0) * FS))
    seg = np.zeros((3, n_tot), np.float32)
    for e, r in zip(ep_s, rows_s):
        off = int(round((e - t0) * FS))
        seg[:, off:off + n_samp_h5] = H5["waves"][int(r)]
    return t0, {c: seg[CH_IDX[c]] for c in ("UD", "NS", "EW")}

if args.picker == "phasenet":
    init_phasenet()

# ================================================================ メインループ
new_evs = []
stats = dict(n_ev=0, n_sta=0, p_fb=0, s_fb=0, no_seg=0, dropped=0,
             wadati_rej=0, imp_p=0, imp_s=0)
wadati_slopes, SPn, Dn = [], [], []
all_absmax = []
comp_out = args.comp_order.split(",")
assert set(comp_out) == {"UD", "NS", "EW"}, "--comp-order は UD,NS,EW の並べ替えで指定"

for ie, ev in enumerate(cat):
    ot = ev["origin_utc"]
    ot_ep = ev["frame_ep"]            # h5フレームの原点epoch(JST基準既定)
    t_a, t_b = ot_ep - SEG_PRE, ot_ep + SEG_POST

    segs = {}
    for sname in sta_meta:
        s = get_segment(sname, t_a, t_b)
        if s is not None:
            segs[sname] = dict(t0_epoch=s[0], data=s[1])
    if len(segs) < 4:
        stats["no_seg"] += 1; continue

    pn_event = phasenet_pick_event(segs) if args.picker == "phasenet" else {}

    picks = {}   # sta -> dict(tp_abs, sp, p_prob/snr, s_snr, pfb, sfb)
    for sname, rec in segs.items():
        ud, ns_, ew = rec["data"]["UD"], rec["data"]["NS"], rec["data"]["EW"]
        t0e = rec["t0_epoch"]
        pn = pn_event.get(sname, {})
        i_p = None
        # 最早優先: 閾値以上で最も早いP(余震系列で後続イベントを掴まない)
        pn_P = [x for x in pn.get("P", []) if x[1] >= PN_PROB_MIN]
        if pn_P:
            tP_ep, p_prob = pn_P[0]
            i_p = int(round((tP_ep - t0e) * FS))
            psnr, pfb = p_prob, False
            if not (0 <= i_p < len(ud)): i_p = None
        if i_p is None:
            i_p, psnr, pfb = pick_p(ud)
            if args.picker == "phasenet": pfb = True
        i_s = None
        # Pより0.3 s以上後で最も早いS(閾値以上)
        pn_S = [x for x in pn.get("S", [])
                if x[1] >= PN_PROB_MIN and x[0] > t0e + i_p / FS + 0.3]
        if pn_S:
            tS_ep, s_prob = pn_S[0]
            i_s = int(round((tS_ep - t0e) * FS))
            ssnr, sfb = s_prob, False
            if not (i_p < i_s < len(ud)): i_s = None
        if i_s is None:
            i_s, ssnr, sfb = pick_s(ew, ns_, ud, i_p)
            if args.picker == "phasenet": sfb = True
        tp_abs = t0e + i_p / FS
        tpv = tp_abs - ot_ep
        spv = (i_s - i_p) / FS if i_s is not None else np.nan
        if not (TP_QC[0] <= tpv <= TP_QC[1]): continue   # 原点相対QC
        if not np.isnan(spv) and not (SP_QC[0] <= spv <= SP_QC[1]):
            spv, sfb = np.nan, True
        picks[sname] = dict(tp_abs=tp_abs, tp=tpv, sp=spv, i_p=i_p,
                            psnr=psnr, ssnr=(ssnr if i_s is not None else 0.0),
                            pfb=bool(pfb), sfb=bool(sfb), t0e=t0e)

    if len(picks) < 4:
        stats["dropped"] += 1; continue

    # ---- 和達QC(14_23と同一: Theil-Sen + 1点抜き救済 + |resid|>2 s棄却) ----
    meas = [s for s in picks if not np.isnan(picks[s]["sp"])]
    if len(meas) >= 4:
        t0ref = min(picks[s]["tp_abs"] for s in meas)
        px = np.array([picks[s]["tp_abs"] - t0ref for s in meas])
        sy = np.array([picks[s]["sp"] for s in meas])
        a_ts, b_ts = ts_fit(px, sy)
        drop_s = None
        if a_ts is not None and not (0.3 <= a_ts <= 1.3) and len(meas) >= 5:
            best = None
            for d in range(len(meas)):
                aa, bb = ts_fit(np.delete(px, d), np.delete(sy, d))
                if aa is not None and 0.3 <= aa <= 1.3 and \
                   (best is None or abs(aa - 0.73) < abs(best[1] - 0.73)):
                    best = (d, aa, bb)
            if best is not None:
                drop_s = meas[best[0]]
                picks[drop_s]["sp"] = np.nan; picks[drop_s]["sfb"] = True
                stats["wadati_rej"] += 1
                a_ts, b_ts = best[1], best[2]
        if a_ts is not None and 0.3 <= a_ts <= 1.3:
            wadati_slopes.append(a_ts)
            resid = sy - (a_ts * px + b_ts)
            for s, rres in zip(meas, resid):
                if s != drop_s and abs(rres) > 2.0:
                    picks[s]["sp"] = np.nan; picks[s]["sfb"] = True
                    stats["wadati_rej"] += 1

    # ---- 局選択: 実測P絶対時刻の早い順(ラベル不使用)で最大8局 ----
    ranked = sorted(picks, key=lambda s: (picks[s]["pfb"], picks[s]["tp_abs"]))
    chosen = ranked[:args.max_sta]
    n_real = len(chosen)

    # ---- 波形窓(P基準 T=2048)・微分・特徴の組み立て ----
    wav = np.zeros((n_real, 3, T_OUT), np.float32)
    sta_locs = np.zeros((n_real, 3), np.float32)
    tp_new = np.full(n_real, np.nan, np.float32)
    sp_new = np.full(n_real, np.nan, np.float32)
    snr_a = np.ones(n_real, np.float32)
    p_fb = np.full(n_real, 2, np.int8); s_fb = np.full(n_real, 2, np.int8)
    p_snr_a = np.zeros(n_real, np.float32); s_snr_a = np.zeros(n_real, np.float32)
    dist_a = np.zeros(n_real, np.float32)
    ok = True
    for k, sname in enumerate(chosen):
        pk, rec = picks[sname], segs[sname]
        i0 = pk["i_p"] - int(P_PRE_S * FS)
        if i0 < 0 or i0 + T_OUT > len(rec["data"]["UD"]):
            ok = False; break
        la, lo_, el = sta_meta[sname]
        sta_locs[k] = (la, lo_, el / 1000.0)
        for ci, cn in enumerate(comp_out):
            x = rec["data"][cn][i0:i0 + T_OUT].astype(np.float64)
            if not args.no_differentiate:
                x = np.gradient(x) * FS      # 速度→加速度(数値微分)
            x -= x.mean()
            wav[k, ci] = x.astype(np.float32)
        tp_new[k] = pk["tp"]; sp_new[k] = pk["sp"]
        p_fb[k] = 1 if pk["pfb"] else 0
        s_fb[k] = 2 if np.isnan(pk["sp"]) else (1 if pk["sfb"] else 0)
        p_snr_a[k], s_snr_a[k] = pk["psnr"], pk["ssnr"]
        if args.snr_mode == "prms":
            snr_a[k] = max(1.0, min(pk["psnr"], 1.05))   # K-NET分布[1.0,~1.05]に整合
        epi = 111.19 * np.hypot(la - ev["lat"],
                                (lo_ - ev["lon"]) * np.cos(np.radians(ev["lat"])))
        dist_a[k] = float(np.hypot(epi, ev["dep"]))
        if s_fb[k] == 0 and not np.isnan(sp_new[k]):
            SPn.append(float(sp_new[k])); Dn.append(float(dist_a[k]))
        stats["n_sta"] += 1
        stats["p_fb"] += int(pk["pfb"]); stats["s_fb"] += int(pk["sfb"])
    if not ok:
        stats["dropped"] += 1; continue

    # ---- 補完(14_23と同一: イベント内実測中央値) ----
    n_imp_p = int(np.isnan(tp_new).sum()); n_imp_s = int(np.isnan(sp_new).sum())
    if np.isnan(tp_new).all() or np.isnan(sp_new).all():
        stats["dropped"] += 1; continue
    tp_new[np.isnan(tp_new)] = float(np.nanmedian(tp_new))
    sp_new[np.isnan(sp_new)] = float(np.nanmedian(sp_new))
    stats["imp_p"] += n_imp_p; stats["imp_s"] += n_imp_s

    all_absmax.append(np.abs(wav[:n_real]).max(axis=(1, 2)))
    new_evs.append(dict(
        origin_time=ot, src_loc=np.array([ev["lat"], ev["lon"], ev["dep"]], np.float32),
        mw=float(ev["mag"]),               # 注意: JMA Mj(F-net Mwではない)
        waveforms=wav.astype(np.float64),
        sta_locs=sta_locs.astype(np.float64),
        tp_times=tp_new.astype(np.float64), sp_diffs=sp_new.astype(np.float64),
        snr=snr_a.astype(np.float64), dist_km=dist_a.astype(np.float64),
        p_fallback=p_fb, s_fallback=s_fb, p_snr=p_snr_a, s_snr=s_snr_a,
        n_real_stations=int(n_real)))
    stats["n_ev"] += 1
    if (ie + 1) % 25 == 0:
        print(f"  … {ie+1}/{len(cat)} 処理 (採用{stats['n_ev']})")

# ---- 振幅整合(データセット一括係数) ----
amp_fac = 1.0
if args.amp_mode == "match_knet" and all_absmax and KNET_ABSMAX_REF:
    med = float(np.median(np.concatenate(all_absmax)))
    amp_fac = KNET_ABSMAX_REF / max(med, 1e-20)
    for ev in new_evs:
        ev["waveforms"] = ev["waveforms"] * amp_fac
    print(f"[24_03] 振幅整合: 長野absmax中央値 {med:.3e} → ×{amp_fac:.3e} で "
          f"K-NET中央値 {KNET_ABSMAX_REF:.2f} に一致(一括係数・相対振幅保存)")

# ================================================================ 保存+開示
out = OUTD / f"tottori_parsed_realpick{args.tag}.pt"
torch.save(new_evs, out)
pfbr = stats["p_fb"] / max(1, stats["n_sta"])
sfbr = stats["s_fb"] / max(1, stats["n_sta"])
n_real_list = [e["n_real_stations"] for e in new_evs]
import hashlib
rep = dict(script_version="24_03 v1 (computation identical to 15_01c v3.3 and 21_20c v1)", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           args={k: str(v) for k, v in vars(args).items()}, stats=stats,
           n_real_hist={str(v): int(c) for v, c in zip(*np.unique(n_real_list, return_counts=True))} if n_real_list else {},
           p_fallback_rate=round(pfbr, 4), s_fallback_rate=round(sfbr, 4),
           amp_factor=amp_fac,
           wadati_slope_median=(float(np.median(wadati_slopes)) if wadati_slopes else None),
           n_clean_sp_pairs=len(SPn),
           disclosure=dict(
               mw_is="JMA Mj (not F-net Mw)",
               comp_order=args.comp_order,
               differentiate=(not args.no_differentiate),
               snr_mode=args.snr_mode, amp_mode=args.amp_mode,
               window="P-anchored [tP-3 s, tP+17.48 s], T=2048 @100 Hz",
               h5_time_base=args.h5_time_base,
               source_waveforms=("per-window z-scored at h5 creation "
                                 "(window-std CV=0.000, audit 15_01d); "
                                 "amplitudes are not physical"),
               pick_selection="earliest P >= 0.3 prob; earliest S after P",
               station_selection=f"earliest measured P (label-free), max {args.max_sta}, no padding (v2)"))
if len(SPn) > 20:
    SPa, Da = np.asarray(SPn), np.asarray(Dn)
    b = np.polyfit(Da, SPa, 1); r = float(np.corrcoef(Da, SPa)[0, 1])
    rep["sp_vs_dist"] = dict(slope=float(b[0]), intercept=float(b[1]), r=r)
json.dump(rep, open(MODD / f"15_01c_build_report{args.tag}.json", "w"), indent=2)

print("\n" + "=" * 72)
print(f"[24_03] 完了: {out}")
print(f"  採用 {stats['n_ev']} / 対象 {len(cat)}  (セグメント不足 {stats['no_seg']}, "
      f"品質不足除外 {stats['dropped']})")
print(f"  P fallback率 {pfbr:.1%} / S fallback率 {sfbr:.1%} / 和達棄却 {stats['wadati_rej']}局")
print(f"  補完: P {stats['imp_p']}局 / S {stats['imp_s']}局   清浄S-Pペア {len(SPn)}")
if n_real_list:
    print(f"  局数/イベント: 中央値 {int(np.median(n_real_list))}  範囲 {min(n_real_list)}-{max(n_real_list)}")
if wadati_slopes:
    print(f"  和達傾き中央値 {np.median(wadati_slopes):.3f} (理論 0.73)")
if "sp_vs_dist" in rep:
    print(f"  S-P vs 距離: 傾き {rep['sp_vs_dist']['slope']:.4f} s/km, "
          f"r={rep['sp_vs_dist']['r']:.3f} (理論 0.1224)")
print("=" * 72)

if len(SPn) > 20:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 11, "figure.facecolor": "white",
                         "savefig.facecolor": "white"})
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.4))
    ax[0].scatter(Dn, SPn, s=8, alpha=0.35, color="#1F5F56", label="measured S–P")
    xs = np.linspace(0, max(Dn), 50)
    ax[0].plot(xs, 0.1224 * xs, "--", color="#B4452F", lw=1.5,
               label="theory 0.122 s/km")
    ax[0].set_xlabel("Hypocentral distance (km)"); ax[0].set_ylabel("S–P (s)")
    ax[0].set_title(f"Northern Nagano 2014: measured S–P vs distance (n={len(SPn)})",
                    fontsize=10.5)
    ax[0].legend(fontsize=9, frameon=False, loc="upper left"); ax[0].grid(alpha=0.25)
    ax[1].hist(wadati_slopes, bins=20, color="#5F7080")
    ax[1].axvline(0.73, color="#B4452F", ls="--", label="theory 0.73")
    ax[1].set_xlabel("Wadati slope per event"); ax[1].set_ylabel("count")
    ax[1].set_title("Wadati QC", fontsize=10.5)
    ax[1].legend(fontsize=9, frameon=False); ax[1].grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(PDFD / f"15_01c_tottori_picks_qc{args.tag}.pdf", bbox_inches="tight")
    print(f"図: {PDFD}/15_01c_tottori_picks_qc{args.tag}.pdf")
print(f"\n[24_03] 出力全文+JSONを貼ってください。{out.name} をMacの SWIFT/data/"
      f"{'nagano2014_processed' if 'nagano2014' in args.tag else 'tottori_processed'}/ にコピーしてください。")
