#!/usr/bin/env python3
# =============================================================================
# Script : 25_02_shimane2018_hinet_to_h5.py  (v1)
#          [島根県西部 2018 の Hi-net の連続波形を、地震の前後だけ取り、鳥取 2026 の h5(tottori_all_100Hz.h5)と
#           同じ形(30 秒窓・3 成分・100 Hz・窓ごと成分ごとの z-score・日本時間の epoch)の h5 にする。あわせて、z-score の前の
#           窓ごと成分ごとの平均と標準偏差(win_mean・win_std)も書く(24_07 が元の値に戻して、τ までの波形だけで検測するため)]
# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の入力の 2 つ目
# 派生元 : 24_02_nagano2014_hinet_to_h5.py v1(SHA-256 0f2283af1e3a0fde831e96bd598284a04ba1ff4a64634fefb1dba65d39f8f69f。事前登録 24 で凍結。
#          = 21_20b v1 に窓ごとの尺度の保存を足したもの)。
#          取り方・z-score・尺度の保存・局の選び方・組み立て・ゲート(G-ref・G-dup・G-cover・G-clock・G-spec)・閾値は 24_02 v1 と
#          1 字も変えていない。変えたのは次だけ(DIFF_LOG_25.md):
#          (1) 入力と出力の名前: jma_shimane2018.csv・25_01_shimane2018_catalog.json・ARGUS_shimane2018・shimane2018_100Hz.h5・
#              stations_shimane2018.csv・data/25_02_*.json・data/25_02.lock・PDF/25_02_*.pdf、表示の [25_02]、h5 の出どころの属性の名前
#          (2) G-clock だけの FAIL の時の表示の文の「事前登録 24」→「事前登録 25」
#          (3) VERSION を "v1 (=24_02 v1 = 21_20b v1 + window scale)" にした
#
# なぜ必要か:
#   25 は 21_02・21_04・21_20・24 と同じ規則・同じ作り方(15_01c v3.3 と同じ計算の 25_03 で検測したキャッシュ)で確かめる。15_01c は
#   tottori_all_100Hz.h5 の形(/waves (N, 3, 3000)、/stations、/window_epoch = 窓の始まりの日本時間を UTC とみなした
#   epoch 秒、属性 channel_order・n_samples・fs)を読む。そこで 2018 の波形をこの形にそろえ、15_01c の検測・QC・
#   組み立てをそのまま通す(15_01c v3.3 で変えたのは、窓の索引のファイル名とその確かめ方・出力の置き場所 --base・
#   最後の表示だけ。検測・QC は v3 と同じ)。
#
# 何をするか(順番どおり):
#   0. 参照の h5(鳥取 2026 の tottori_all_100Hz.h5)から形を読む: /waves の dtype と (3, 3000)、/stations と
#      /window_epoch の dtype、chunks、属性(fs が無ければ STOP)。無作為の 300 窓で、成分ごとの平均 ≈ 0・標準偏差 ≈ 1
#      (窓ごとの z-score)を確かめ、窓の始まりが 30 s の格子にそろう割合と、0.1–1 Hz と 1–20 Hz の力の比(中央値)を記録する。
#      出力の h5 は、参照の /waves の dtype・/window_epoch の dtype・chunks(データより大きければ詰める)・圧縮で書く。
#      /stations は参照が固定長のバイト列なら 16 バイト以上の固定長(参照は 6 バイトでも Hi-net の名前 N.XXXH が入るように)、
#      可変長の文字列なら可変長。属性は channel_order = "UD,NS,EW"・n_samples = 3000・fs = 100 と出どころの説明だけを書く
#      (鳥取 2026 の属性は写さず、報告の JSON に記録する)。
#   1. 観測点: NIED の Hi-net(0101)の観測点の一覧(HinetPy の get_station_list。今の一覧。緯度・経度・標高のどれかが無い局は
#      除く)から、本震(25_01 の JSON)に近い順に --n-sta + 10 局を候補にする。Hi-net のアカウントの「選んだ局」を
#      最初の 1 回だけ data/25_02_initial_selection.json に保存してから候補を選び、終わり(止めた時・失敗した時も)に元に戻す。
#      選んだ後の選択が空(= 全局)か候補の外の局を含めば STOP(全局のまま取ると何倍も時間がかかる)。
#      途中で落ちて戻せなかった時は --restore-selection で戻せる。同時に 2 つ回さないよう data/25_02.lock を置く
#      (区切りごとに新しくし、30 分より古い印は止まった実行の印とみなす。Colab が切れた直後は --restore-selection --break-lock)。
#   2. 取る時間の区切り: 25_01 の CSV の Mj ≥ 1.5 の地震ごとに、[発生時刻 − 10 s を分に切り下げ, 発生時刻 + 45 s を
#      分に切り上げ](日本時間)。15_01c が使う区間 [発生 − 10 s, 発生 + 45 s] を 30 秒窓で必ず覆う。間が 2 分以下の
#      区切りはつなぎ、60 分を超えたら 60 分ごとに分ける(続く区切りの窓は切れ目なくつながるので、15_01c は区切りを
#      またいでも読める)。1 つの区切りを get_continuous_waveform の 1 回の呼び出しで取る(max_span = 12000 / (3 × 局の数)
#      分。60 局なら 60 分なので、Hi-net への要求も 1 回)。
#      21_04b v1.1 から引き継ぎ(2026-10-28、鳥取県中部 2016 の煙試験で本震の 60 分の区切りが Hi-net 側で 3 回とも失敗したため): 1 回の要求の長さ max_span を、
#      失敗したら 60 → 20 → 10 → 5 分と短くして取り直す(1 区切りに最大 4 回)。短くした長さで取れたら、その実行の残りの
#      区切りもその長さから始める(その長さで実際に分けて取れた時だけ)。試すたびに動いている印(lock)を新しくする。HinetPy が短い要求に分けて取り、1 つにつないで返すので、取れる波形・窓・h5 は v1 と同じ
#      (要求の分け方だけが変わる)。検測・ゲート・組み立ては 21_04b v1 から 1 字も変えていない。
#   3. 区切りごと(途中で止まっても、終わった区切りは飛ばして続きから): WIN32 をローカルの一時フォルダに取り、
#      win2sac_32(HinetPy の extract_sac)で候補局の U・N・E を SAC にして ObsPy で読む。
#      局ごとに 3 成分とも、刻み 0.01 s・始まりが区切りの始まりと 1 ms 以内・点の数が区切りの長さ以上、を確かめる。
#      区切りの中の 30 秒窓ごとに、成分ごとに z = (x − 平均) / 標準偏差(窓の 3000 点で。鳥取 2026 の h5 と同じ)にして、
#      参照の dtype にする。標準偏差が 0・NaN・同じ値が 100 点以上続く(欠測の埋め)成分がある窓は捨てる。
#      使える局が 0 の区切りは失敗として取り直す(3 回まで。3 つの区切りで続けて失敗したら STOP)。
#      区切りの結果は Drive の data/blocks/blk_<始まり>_<分>.npz に書く(.tmp に書き終わってから名前を付ける。読めない
#      ファイルは次の実行で消して取り直す)。元の WIN32・SAC は区切りごとに消す(Drive には残さない)。
#      計画の時に、区切りのファイルと h5 の大きさの見込みと Drive の空きを表示する。取る時は、残りの区切りと h5 の見込みの
#      1.1 倍に空きが足りなければ STOP。片付け(書きかけの削除)は、動いている印(lock)を取ってから行う。
#   4. 組み立て(--assemble): 今の計画の区切りのファイルだけを使う(足りなければ STOP。計画に無いファイルは使わず表示する。
#      何度回しても取れない区切りだけが残り、取れた割合が 0.98 以上なら --allow-missing で続けてよい。これは事前に決めた規則で、
#      その区切りの地震は G-cover で覆えない地震として数える)。
#      区切りの半分以上でデータがある局のうち本震に近い順に --n-sta 局(既定 50。鳥取 2026 の局の数と同じ)を選び、その局の
#      窓だけを書く。data/catalog/stations_shimane2018.csv(列 id, latitude, longitude, elevation。緯度・経度は 2018 年の
#      チャンネル表、標高は NIED の一覧の height(m)。stations.csv と同じ列)も書く。
#      ゲートを書きかけのファイル(.part)で確かめ、全て通った時だけ data/waves/shimane2018_100Hz.h5 の名前にする
#      (通らなければ shimane2018_100Hz_FAILED.h5 にして STOP。25_03 に渡る名前の h5 は作らない。G-clock だけの FAIL の扱いは
#      事前登録 25 に先に決めてある: 記録だけで、_FAILED の h5 と stations_shimane2018.csv.part を 25_03 に渡し、時刻は G-clock2 で決める)。
#      --partial(煙試験の確認): 取った区切りだけで組み立て、名前に _partial を付ける。
#   5. ゲート(組み立ての後に表示し、data/25_02_report.json に合否と一緒に書く):
#      - G-ref: 参照の h5 の z-score の確認に合格(fs = 100)。出力も同じ確認に合格
#      - G-dup: (局, 窓の始まり) が重ならない
#      - G-cover: Mj ≥ 1.5 の全ての地震(--partial では取った区間の中の地震だけ)のうち、[発生 − 10 s, 発生 + 45 s] を
#        30 秒窓でつないで覆える局が 4 局以上ある割合。0.95 以上で PASS、0.80 以上で注意、0.80 未満で STOP
#        (15_01c の get_segment と同じ規則)
#      - G-clock: 本震と、取った区間の中の大きい順の 3 地震(本震の 1 時間より後で、前の 10 分に同じ以上の Mj の地震が無く、
#        前の 60 s に Mj ≥ 1.5 の地震が無いもの。前の地震のコーダで立ち上がりを誤らないため)で、近い 12 局を順に見て立ち上がりが取れた最初の 8 局の、
#        上下動の STA/LTA の立ち上がり(発生 − 1 s より後だけ)− 震源距離 / 6.0 km/s の |差| の中央値が 1.5 s 以内。本震は必ず合格、他の地震は
#        4 局以上で取れた時だけ合格が要る(日本時間の扱いや時刻のずれを誤ると立ち上がりが合わない。1 s 未満のずれは見えない)
#      - G-spec(記録だけ): 0.1–1 Hz と 1–20 Hz の力の比の中央値を参照と出力で比べる(出力は、つながった区間の最初の窓 =
#        発生の 10 s 以上前から始まる窓だけで測る)。3 倍以上違えば注意を表示する
#        (鳥取 2026 の h5 を作る時に周波数のフィルタをかけたかの記録が無いため。ここでは何もかけない。結果によらず先に進み、
#        違いがあれば限界に書く)
#   6. 図: PDF/25_02_coverage.pdf(局 × 区切りのデータの有無)、PDF/25_02_mainshock.pdf(本震の上下動の
#      記録の並びと、予想の P の印)。白背景・英語・凡例は枠の外。
#
# 前提: Hi-net のアカウント(環境変数 HINET_USER・HINET_PASS。ノートの セル 4 で getpass で入れる)、
#   win32tools の catwin32・win2sac_32 が PATH にある(ノートの セル 3)、HinetPy 0.13.0。
# 止める条件(STOP): 資格情報が無い・win2sac_32 が無い・参照の h5 が読めないか形が違うか fs が無い・25_01 の JSON が無い・
#   置き場所が足りない見込み・局の選択が効かない・別の実行の印がある・3 回ずつ試して取れない区切りが 3 つ続く・組み立てで取っていない
#   区切りがあるか読めないファイルがある・使える局が 0・窓が 0・G-ref・G-dup・G-cover < 0.80・G-clock の失敗。
# 限界(25 の限界にも書く):
#   - 観測点は Hi-net(0101)だけで、鳥取 2026 の 50 局(Hi-net のほか京大防災研・気象庁などを含む)とは種類と並びが違う
#   - 候補は今の NIED の一覧から選ぶので、2018 年にあって今は無い局は入らない
#   - 地震の前後だけを取る(連続ではない)。15_01c が使う区間は全て含む。区切りの中で欠けがある局は、その区切りでは使わない
#   - 鳥取 2026 の h5 で z-score の前にフィルタをかけたかは記録が無い(ここではかけない。G-spec で比べる)
#
# Usage : (Colab、ノート 25_shimane2018_colab.ipynb の セル N6〜N9。手順は 25_STEPS_JA.md)
#   計画だけ:       !python /content/drive/MyDrive/ARGUS/src/25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5> --dry-run
#   煙試験(本震の区間に掛かる区切りを先に 3 区切り): !python .../25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5> --max-blocks 3
#                    続けて !python .../25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5> --assemble --partial(取った分だけでゲートを見る)
#   本番(続きから):   !python .../25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5>
#   組み立て:         !python .../25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5> --assemble
#   選択を戻すだけ:   !python .../25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5> --restore-selection [--break-lock](セル N8b)
# Output (--out の下。既定 /content/drive/MyDrive/ARGUS_shimane2018):
#   data/blocks/blk_*.npz / data/25_02_plan.json / data/25_02_initial_selection.json /
#   data/waves/shimane2018_100Hz.h5 / data/catalog/stations_shimane2018.csv / data/25_02_report.json /
#   PDF/25_02_coverage.pdf / PDF/25_02_mainshock.pdf(--partial ではそれぞれ _partial 付き)
#   区切りのファイルは組み立ての後も消さない(h5 を作り直せるように。要らなくなったら data/blocks を手で消す)
# 所要: 区切りの数 × 1 回の要求の時間(Hi-net は 1 回の準備に 10〜60 s かかる)。計画の時に区切りの数と分の合計を表示し、
#   煙試験で 1 区切りの時間を測って残りを見積もる。
# =============================================================================
from __future__ import annotations

import argparse
import csv
import glob
import hashlib
import json
import math
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np

VERSION = "v1 (=24_02 v1 = 21_20b v1 + window scale)"   # 25_02 の 1 版目(計算は 24_02 v1 と同じ。取り方は 21_20b v1 = 21_04b v1.1 と同じ)
ROOT = Path(__file__).resolve().parent.parent
NET = "0101"
FS, WIN_N, WIN_S = 100.0, 3000, 30.0
COMPS = ("U", "N", "E")                     # Hi-net の成分名 → h5 の UD, NS, EW
SEG_PRE_S, SEG_POST_S = 10.0, 45.0          # 15_01c の検測の区間 [発生 − 10 s, 発生 + 45 s]
MERGE_GAP_MIN = 2
MAX_BLOCK_MIN = 60                          # 1 つの区切りの最長(Hi-net の 1 回の要求の上限と同じ。続く区切りは窓が切れ目なくつながる)
MIN_MAG = 1.5
EXTRA_CAND = 10
FLAT_RUN = 100
MIN_PRESENCE = 0.5
MIN_FETCHED = 0.98                          # --allow-missing で組み立てを続けてよい、取れた区切りの割合の下限(事前に決めた値)
COVER_OK, COVER_STOP = 0.95, 0.80
CLOCK_NSTA, CLOCK_VP, CLOCK_TOL = 8, 6.0, 1.5
REF_NSAMPLE = 300
EPOCH0 = datetime(1970, 1, 1)


def jst_epoch(t: datetime) -> float:
    """日本時間の時計の値を UTC とみなした epoch 秒(tottori_all_100Hz.h5 の window_epoch と同じ決まり)"""
    return (t - EPOCH0).total_seconds()


def floor_min(t: datetime) -> datetime:
    return t.replace(second=0, microsecond=0)


def ceil_min(t: datetime) -> datetime:
    f = floor_min(t)
    return f if f == t else f + timedelta(minutes=1)


def plan_blocks(origins_jst):
    """地震ごとの区間をつないだ区切り [(始まり, 分)]"""
    iv = sorted((floor_min(o - timedelta(seconds=SEG_PRE_S)), ceil_min(o + timedelta(seconds=SEG_POST_S))) for o in origins_jst)
    out = []
    for a, b in iv:
        if out and (a - out[-1][1]) <= timedelta(minutes=MERGE_GAP_MIN):
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    res = []
    for a, b in out:
        while a < b:
            e = min(b, a + timedelta(minutes=MAX_BLOCK_MIN)); res.append((a, int(round((e - a).total_seconds() / 60)))); a = e
    return res


def blk_name(start: datetime, span: int) -> str:
    return f"blk_{start:%Y%m%d%H%M}_{span:03d}.npz"


BLK_KEYS = ("stations", "epoch", "waves", "chan", "stat", "scale")   # 25_02: scale を足した


def _npy_shape(zf, name):
    with zf.open(name) as fh:
        ver = np.lib.format.read_magic(fh)
        shape, _, _ = (np.lib.format.read_array_header_1_0(fh) if ver == (1, 0) else np.lib.format.read_array_header_2_0(fh))
    return shape


def blk_ok(path: Path) -> bool:
    """区切りのファイルが読めて、鍵がそろい、窓が 1 つ以上あるか(途中で切れたファイルを「済み」と数えない)。
    zip の目次と配列の頭だけを読む(波形の本体は読まない)"""
    import zipfile
    try:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            if not all(f"{k}.npy" in names for k in BLK_KEYS): return False
            sw, se = _npy_shape(zf, "waves.npy"), _npy_shape(zf, "epoch.npy")
            return len(sw) == 3 and sw[0] > 0 and sw[1:] == (3, WIN_N) and se == (sw[0],)
    except Exception:
        return False


def blk_done(OUT: Path, b: datetime, s: int) -> bool:
    return (OUT / "data" / "blocks" / blk_name(b, s)).exists()


def run_starts(plan):
    """60 分ごとに分けた続きの区切りを除いた、つながった区間の始まり(発生の 10 s 以上前から始まる)"""
    out, prev_end = [], None
    for b, s in plan:
        if prev_end is None or b != prev_end: out.append(b)
        prev_end = b + timedelta(minutes=s)
    return out


def haversine_km(la1, lo1, la2, lo2):
    p1, p2 = np.radians(la1), np.radians(la2)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(np.radians(lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * np.arcsin(np.sqrt(a))


def has_flat(seg: np.ndarray) -> bool:
    """どれかの成分で同じ値が FLAT_RUN 点以上続くか(欠測を同じ値で埋めた所を見つける)"""
    d = np.diff(seg, axis=1) == 0
    for c in range(seg.shape[0]):
        if d[c].sum() < FLAT_RUN - 1: continue
        x = np.flatnonzero(np.diff(np.r_[0, d[c].astype(np.int8), 0]))
        if (x[1::2] - x[::2]).max() >= FLAT_RUN - 1: return True
    return False


def zscore_windows(arr3: np.ndarray, dtype):
    """arr3: (3, n) → 窓ごとの (z (k, 3, 3000), 使った窓の番号, 尺度 (k, 3, 2) = 成分ごとの [平均, 標準偏差])。窓ごと・成分ごとの z-score。
    25_02: 尺度を返すのを足した(z の計算は 21_20b と同じ)"""
    nwin = arr3.shape[1] // WIN_N
    zs, ks, sc = [], [], []
    for k in range(nwin):
        seg = np.asarray(arr3[:, k * WIN_N:(k + 1) * WIN_N], float)
        if not np.isfinite(seg).all(): continue
        sd = seg.std(axis=1)
        if np.any(sd <= 0): continue
        if has_flat(seg): continue
        zs.append(((seg - seg.mean(axis=1, keepdims=True)) / sd[:, None]).astype(dtype)); ks.append(k)
        sc.append(np.stack([seg.mean(axis=1), sd], axis=1))                     # 25_02: (3, 2) = [平均, 標準偏差](z と同じ値で計算)
    return (np.stack(zs) if zs else np.zeros((0, 3, WIN_N), dtype)), ks, (np.stack(sc) if sc else np.zeros((0, 3, 2)))


def zcheck(waves: np.ndarray):
    """(n, 3, 3000) の窓が成分ごとに平均 ≈ 0・標準偏差 ≈ 1 か。返り値: (最大 |平均|, 最大 |標準偏差 − 1|)"""
    w = np.asarray(waves, float)
    return float(np.max(np.abs(w.mean(axis=2)))), float(np.max(np.abs(w.std(axis=2) - 1.0)))


def band_ratio(waves: np.ndarray):
    """窓ごとの (0.1–1 Hz の力) / (1–20 Hz の力) の中央値(上下動、ハン窓の周期図)"""
    w = np.asarray(waves, float)[:, 0, :]
    f = np.fft.rfftfreq(WIN_N, 1 / FS)
    P = np.abs(np.fft.rfft((w - w.mean(axis=1, keepdims=True)) * np.hanning(WIN_N), axis=1)) ** 2
    lo = P[:, (f >= 0.1) & (f < 1.0)].sum(1); hi = P[:, (f >= 1.0) & (f < 20.0)].sum(1)
    r = lo / np.maximum(hi, 1e-30)
    return float(np.median(r)) if len(r) else float("nan")


def sta_lta_first(x, sta=0.5, lta=5.0, thr=3.0, i_min=0):
    """因果 1–15 Hz のバンドパスの後の STA/LTA が thr を最初に超える点(点 i_min 以降。無ければ None)"""
    from scipy.signal import butter, sosfilt
    f = sosfilt(butter(4, [1.0, 15.0], btype="band", fs=FS, output="sos"), np.asarray(x, float))
    e = f * f; c = np.cumsum(e); ns, nl = int(sta * FS), int(lta * FS)
    for i in range(max(nl, i_min), len(e)):
        s = (c[i] - c[i - ns]) / ns; l_ = (c[i] - c[i - nl]) / nl
        if l_ > 0 and s / l_ >= thr: return i
    return None


# ----------------------------------------------------------------------------- 参照の h5
def read_ref(path: str, rng):
    import h5py
    with h5py.File(path, "r") as H:
        for k in ("waves", "stations", "window_epoch"):
            if k not in H: sys.exit(f"[25_02] STOP(G-ref): 参照の h5 に /{k} が無い")
        W = H["waves"]
        if tuple(W.shape[1:]) != (3, WIN_N): sys.exit(f"[25_02] STOP(G-ref): 参照の /waves の形 {W.shape} が (N, 3, 3000) でない")
        attrs = {k: (v.decode() if isinstance(v, bytes) else (v.tolist() if hasattr(v, "tolist") else v)) for k, v in H.attrs.items()}
        fsv = attrs.get("fs", attrs.get("sampling_rate"))
        if fsv is None: sys.exit("[25_02] STOP(G-ref): 参照の h5 に属性 fs が無い")
        fs = float(np.ravel(fsv)[0])
        if abs(fs - FS) > 1e-6: sys.exit(f"[25_02] STOP(G-ref): 参照の fs = {fs}")
        n = W.shape[0]
        rows = np.sort(rng.choice(n, size=min(REF_NSAMPLE, n), replace=False))
        samp = np.stack([W[int(r)] for r in rows])
        ep = H["window_epoch"]
        ep_s = np.array([float(ep[int(r)]) for r in rows])
        info = dict(path=path, n_windows=int(n), waves_dtype=str(W.dtype), stations_dtype=str(H["stations"].dtype),
                    epoch_dtype=str(ep.dtype), chunks=(list(W.chunks) if W.chunks else None), compression=W.compression,
                    compression_opts=W.compression_opts, attrs=attrs, other_datasets=sorted(k for k in H.keys() if k not in
                                                                                               ("waves", "stations", "window_epoch")))
    m, s = zcheck(samp)
    info.update(zcheck_max_abs_mean=m, zcheck_max_abs_std_minus_1=s, grid30_frac=float(np.mean(np.abs(np.mod(ep_s, 30.0)) < 1e-3)),
                grid30_residues=sorted(set(np.round(np.mod(ep_s, 30.0), 2).tolist()))[:10], band_ratio_median=band_ratio(samp))
    tol = 0.02 if "float16" in info["waves_dtype"] else 1e-3
    info["zcheck_pass"] = bool(m < tol and s < tol)
    return info


# ----------------------------------------------------------------------------- Hi-net
def hinet_client():
    u, p = os.environ.get("HINET_USER"), os.environ.get("HINET_PASS")
    if not u or not p: sys.exit("[25_02] STOP: 環境変数 HINET_USER・HINET_PASS が無い(ノートの セル 4 で入れる)")
    from HinetPy import Client
    return Client(u, p)


def restore_selection(client, sel_path: Path):
    try:
        names = json.load(open(sel_path))["stations"]
        client.select_stations(NET, names if names else None)
        print(f"[25_02] アカウントの局の選択を元に戻した({len(names) if names else '全局'})")
    except Exception as e:                                  # 戻せなかった時は必ず表示する
        print(f"[25_02] 注意: アカウントの局の選択を戻せなかった({e})。Hi-net のサイトで確かめる。保存した選択: {sel_path}")


def fetch_block(client, start: datetime, span: int, cands, dtype, tmp_root: Path, max_span: int = 60):
    """1 つの区切りを取り、局ごとの窓にする。返り値: dict(stations, epoch, waves, chan, stat) か None(要求の失敗)"""
    from HinetPy import win32
    from obspy import read
    tmp = Path(tempfile.mkdtemp(dir=tmp_root))
    try:
        data, ctable = client.get_continuous_waveform(NET, start, span, max_span=max_span, outdir=str(tmp), threads=3, cleanup=True)
        if data is None or ctable is None or not Path(data).exists(): return None
        sacd = tmp / "sac"; sacd.mkdir()
        win32.extract_sac(data, ctable, outdir=str(sacd), filter_by_name=list(cands), filter_by_component=list(COMPS), processes=2)
        chan = {}
        for ch in win32.read_ctable(ctable):
            if ch.name in cands: chan[ch.name] = (ch.latitude, ch.longitude)
        t0 = jst_epoch(start); need = span * 60 * int(FS)
        st_l, ep_l, wv_l, sc_l = [], [], [], []
        stat = dict(n_sta_files=0, bad_header=0, short=0, windows=0, windows_dropped=0)
        for s in cands:
            fs_ = [sacd / f"{s}.{c}.SAC" for c in COMPS]
            if not all(f.exists() for f in fs_): continue
            stat["n_sta_files"] += 1
            trs = [read(str(f))[0] for f in fs_]
            if any(abs(tr.stats.delta - 1 / FS) > 1e-6 or abs(tr.stats.starttime.timestamp - t0) > 1e-3 for tr in trs):
                stat["bad_header"] += 1; continue
            if min(tr.stats.npts for tr in trs) < need: stat["short"] += 1; continue
            arr = np.stack([np.asarray(tr.data[:need], float) for tr in trs])
            z, ks, sc = zscore_windows(arr, dtype)
            stat["windows"] += len(ks); stat["windows_dropped"] += need // WIN_N - len(ks)
            if not ks: continue
            st_l += [s] * len(ks); ep_l += [t0 + WIN_S * k for k in ks]; wv_l.append(z); sc_l.append(sc)
        if stat["n_sta_files"] == 0 or not wv_l:              # 何も取れなかった区切りは失敗として取り直す
            print(f"    区切り {start:%Y-%m-%d %H:%M}: 使える局が 0(SAC のある局 {stat['n_sta_files']}・頭が合わない {stat['bad_header']}・"
                  f"短い {stat['short']}・窓 {stat['windows']})")
            return None
        return dict(stations=np.array(st_l, dtype="U16"), epoch=np.array(ep_l, float),
                    waves=(np.concatenate(wv_l) if wv_l else np.zeros((0, 3, WIN_N), dtype)), chan=chan, stat=stat,
                    scale=(np.concatenate(sc_l) if sc_l else np.zeros((0, 3, 2))))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


LOCK_STALE_S = 30 * 60


def check_lock(lock: Path):
    if lock.exists() and time.time() - lock.stat().st_mtime < LOCK_STALE_S:
        sys.exit(f"[25_02] STOP: 別の実行が動いている印 {lock}({lock.read_text().strip()})が 30 分以内に更新されている。"
                 "Colab が切れた直後なら別の実行は無いので、セル 8b(--restore-selection --break-lock)を回してからセル 8 をもう一度")


def touch_lock(lock: Path):
    import socket
    lock.write_text(f"{datetime.now(timezone.utc).isoformat()} host={socket.gethostname()} pid={os.getpid()}")


# ----------------------------------------------------------------------------- 組み立てとゲート
def covers(ep_sorted, t_a, t_b):
    """15_01c の get_segment と同じ規則で、局の窓の始まり(並べたもの)が [t_a, t_b] をつないで覆うか"""
    sel = ep_sorted[(ep_sorted > t_a - WIN_S - 1e-6) & (ep_sorted < t_b + 1e-6)]
    if not len(sel) or sel[0] > t_a + 1e-3 or sel[-1] + WIN_S < t_b - 1e-3: return False
    return not (len(sel) > 1 and np.any(np.abs(np.diff(sel) - WIN_S) > 0.02))


def assemble(OUT: Path, PDFD: Path, ref, summ, cat_rows, cand_meta, n_sta, plan, partial=False, allow_missing=False):
    import h5py
    exp = {blk_name(b, s) for b, s in plan}
    allf = sorted((OUT / "data" / "blocks").glob("blk_????????????_???.npz"))
    extra = [f.name for f in allf if f.name not in exp]
    if extra: print(f"[25_02] 注意: 今の計画に無い区切りのファイル {len(extra)} は使わない(例 {extra[:3]})")
    files = [f for f in allf if f.name in exp]
    bad = [f.name for f in files if not blk_ok(f)]
    if bad: sys.exit(f"[25_02] STOP: 読めない区切りのファイルが {len(bad)} ある(例 {bad[:3]})。消してから取り直す(セル 8)")
    missing = sorted(exp - {f.name for f in files})
    if not files: sys.exit("[25_02] STOP: 区切りの結果が 1 つも無い")
    pres, chan = {}, {}
    for f in files:
        z = np.load(f, allow_pickle=False)
        for s in set(z["stations"].tolist()): pres[s] = pres.get(s, 0) + 1
        c = json.loads(str(z["chan"]))
        for k, v in c.items(): chan.setdefault(k, v)
    nb = len(files)
    if missing and not partial:
        frac = 1 - len(missing) / len(exp)
        if not (allow_missing and frac >= MIN_FETCHED):
            sys.exit(f"[25_02] STOP: 取っていない区切りが {len(missing)} ある(取れた割合 {frac:.3f}、例 {missing[:3]})。セル 8 を"
                     f"もう一度回してから --assemble。何度回しても取れない区切りだけが残り、取れた割合が {MIN_FETCHED} 以上なら "
                     "--allow-missing で続けてよい(事前に決めた規則。その区切りの地震は G-cover で覆えない地震として数える)")
        print(f"[25_02] 注意(--allow-missing): 取っていない区切り {len(missing)}(取れた割合 {frac:.3f} ≥ {MIN_FETCHED})で続ける: {missing}")
    done_iv = []
    for f in files:
        st_, sp_ = f.stem.split("_")[1], int(f.stem.split("_")[2])
        b_ = datetime.strptime(st_, "%Y%m%d%H%M"); done_iv.append([jst_epoch(b_), jst_epoch(b_) + 60 * sp_])
    done_iv.sort(); mg = []
    for iv in done_iv:                                        # 続く区切りは 1 つの区間にまとめる
        if mg and iv[0] <= mg[-1][1] + 1e-6: mg[-1][1] = max(mg[-1][1], iv[1])
        else: mg.append(list(iv))
    done_iv = mg
    ml, mo = summ["mainshock"]["lat"], summ["mainshock"]["lon"]
    ok = [s for s in pres if pres[s] >= MIN_PRESENCE * nb and s in cand_meta]
    ok.sort(key=lambda s: haversine_km(ml, mo, cand_meta[s]["lat"], cand_meta[s]["lon"]))
    keep = ok[:n_sta]
    if not keep: sys.exit("[25_02] STOP: 区切りの半分以上でデータがある局が 0")
    if len(keep) < n_sta: print(f"[25_02] 注意: 区切りの半分以上でデータがある局が {len(keep)} しかない(--n-sta {n_sta})")
    print(f"[25_02] 組み立て: 区切り {nb}(計画 {len(plan)})  使う局 {len(keep)}(最も遠い局 "
          f"{haversine_km(ml, mo, cand_meta[keep[-1]]['lat'], cand_meta[keep[-1]]['lon']):.1f} km)")
    kset = set(keep)
    (OUT / "data" / "waves").mkdir(parents=True, exist_ok=True); (OUT / "data" / "catalog").mkdir(parents=True, exist_ok=True)
    h5p = OUT / "data" / "waves" / ("shimane2018_100Hz_partial.h5" if partial else "shimane2018_100Hz.h5"); tmpp = h5p.with_suffix(".h5.part")
    if h5p.exists(): h5p.unlink()                              # 前の組み立ての結果は、ゲートに通るまで置かない
    dt = np.dtype(ref["waves_dtype"])
    n_tot = 0
    for f in files:
        z = np.load(f, allow_pickle=False); n_tot += int(np.isin(z["stations"], list(kset)).sum())
    if n_tot == 0: sys.exit("[25_02] STOP: 書く窓が 0")
    chunks = tuple(min(c, n) for c, n in zip(ref["chunks"], (n_tot, 3, WIN_N))) if ref.get("chunks") else None
    with h5py.File(tmpp, "w") as H:
        W = H.create_dataset("waves", (n_tot, 3, WIN_N), dtype=dt, chunks=chunks, compression=ref.get("compression"),
                             compression_opts=ref.get("compression_opts"))
        sfix = "S" in ref["stations_dtype"]
        S = H.create_dataset("stations", (n_tot,), dtype=(np.dtype(f"S{max(np.dtype(ref['stations_dtype']).itemsize, 16)}") if sfix
                                                          else h5py.string_dtype()))
        E = H.create_dataset("window_epoch", (n_tot,), dtype=np.dtype(ref["epoch_dtype"]))
        WM = H.create_dataset("win_mean", (n_tot, 3), dtype=np.float64); WS = H.create_dataset("win_std", (n_tot, 3), dtype=np.float64)   # 25_02
        i = 0
        for f in files:
            z = np.load(f, allow_pickle=False); m = np.isin(z["stations"], list(kset)); k = int(m.sum())
            if not k: continue
            W[i:i + k] = z["waves"][m].astype(dt)
            S[i:i + k] = np.array([s.encode() for s in z["stations"][m]]) if sfix else z["stations"][m].astype(object)
            E[i:i + k] = z["epoch"][m]; WM[i:i + k] = z["scale"][m][:, :, 0]; WS[i:i + k] = z["scale"][m][:, :, 1]; i += k
        H.attrs["channel_order"] = "UD,NS,EW"; H.attrs["n_samples"] = WIN_N; H.attrs["fs"] = FS
        H.attrs["shimane2018_source"] = (f"NIED Hi-net (0101) continuous data via HinetPy, event blocks only; 25_02_shimane2018_hinet_to_h5.py "
                                    f"{VERSION}; per-window per-component z-score (win_mean, win_std = the mean and std used; waves * win_std + win_mean restores the counts); "
                                    f"window_epoch = JST wall clock as UTC epoch")
    stp = OUT / "data" / "catalog" / ("stations_shimane2018_partial.csv" if partial else "stations_shimane2018.csv")
    if stp.exists(): stp.unlink()
    with open(stp.with_suffix(".csv.part"), "w", newline="") as fo:
        w = csv.writer(fo); w.writerow(["id", "latitude", "longitude", "elevation"])
        for s in keep:
            la, lo = chan.get(s, (cand_meta[s]["lat"], cand_meta[s]["lon"]))
            w.writerow([s, f"{la:.4f}", f"{lo:.4f}", f"{cand_meta[s]['elev_m']:.1f}"])
    # ---- ゲート
    G = {}
    with h5py.File(tmpp, "r") as H:
        st = np.array([s.decode() if isinstance(s, bytes) else str(s) for s in H["stations"][:]]); ep = H["window_epoch"][:]
        key = np.char.add(st, np.char.mod("%.3f", ep))
        G["dup"] = int(len(key) - len(np.unique(key)))
        rng = np.random.default_rng(3); rows = np.sort(rng.choice(len(ep), size=min(REF_NSAMPLE, len(ep)), replace=False))
        samp = np.stack([H["waves"][int(r)] for r in rows])
        m_, s_ = zcheck(samp); tol = 0.02 if "float16" in ref["waves_dtype"] else 1e-3
        G["out_zcheck"] = dict(max_abs_mean=m_, max_abs_std_minus_1=s_, pass_=bool(m_ < tol and s_ < tol))
        # 力の比は、区切りの最初の窓(発生の 10 s 以上前から始まる)だけで測る(地震の窓ばかりだと高い周波数に寄るため)
        b0 = np.array([jst_epoch(b) for b in run_starts(plan)]); first = np.flatnonzero(np.isin(np.round(ep, 3), np.round(b0, 3)))
        if len(first) > REF_NSAMPLE: first = np.sort(rng.choice(first, size=REF_NSAMPLE, replace=False))
        G["band_ratio_out"] = band_ratio(np.stack([H["waves"][int(r)] for r in first])) if len(first) else float("nan")
        by = {}
        for s in keep:
            e_ = np.sort(ep[st == s]); by[s] = e_
        mj = [r for r in cat_rows if r["mag"] >= MIN_MAG - 1e-9 and (not partial or any(a0 <= jst_epoch(r["t"]) - SEG_PRE_S and
                                                                         jst_epoch(r["t"]) + SEG_POST_S <= b0_ for a0, b0_ in done_iv))]
        G["cover_n_events"] = len(mj)
        ncov = [sum(covers(by[s], jst_epoch(r["t"]) - SEG_PRE_S, jst_epoch(r["t"]) + SEG_POST_S) for s in keep) for r in mj]
        G["cover_frac_ge4"] = float(np.mean(np.array(ncov) >= 4)) if ncov else 0.0
        G["cover_median_stations"] = float(np.median(ncov)) if ncov else 0.0
        # G-clock: 本震と、取った区間の中の大きい順の 3 地震(本震以外)。近い 12 局を順に見て、立ち上がりが取れた最初の 8 局
        mt = datetime.strptime(summ["mainshock"]["origin_jst"][:22].ljust(22, "0"), "%Y-%m-%d %H:%M:%S.%f")
        def quiet(r):                                          # 本震の 1 時間より後で、前の 10 分に大きい地震・前の 60 s に Mj ≥ 1.5 が無い
            t = jst_epoch(r["t"])
            return t > jst_epoch(mt) + 3600 and not any(
                (0 < t - jst_epoch(q["t"]) <= 600 and q["mag"] >= r["mag"]) or (0 < t - jst_epoch(q["t"]) <= 60 and q["mag"] >= MIN_MAG)
                for q in cat_rows)
        others = sorted((r for r in cat_rows if r["mag"] >= MIN_MAG - 1e-9 and quiet(r) and
                         any(a0 <= jst_epoch(r["t"]) - SEG_PRE_S and jst_epoch(r["t"]) + SEG_POST_S <= b0_ for a0, b0_ in done_iv)),
                        key=lambda r: -r["mag"])[:3]
        evs = [dict(t=mt, lat=ml, lon=mo, dep=summ["mainshock"]["depth_km"], mag=summ["mainshock"]["mj"], main=True)] + \
              [dict(t=r["t"], lat=r["lat"], lon=r["lon"], dep=r["dep"], mag=r["mag"], main=False) for r in others]
        G["clock"], sec = [], []
        for ev in evs:
            t_a, t_b = jst_epoch(ev["t"]) - SEG_PRE_S, jst_epoch(ev["t"]) + SEG_POST_S
            near = sorted(keep, key=lambda s: haversine_km(ev["lat"], ev["lon"], cand_meta[s]["lat"], cand_meta[s]["lon"]))[:12]
            resid = []
            for s in near:
                mm = (st == s) & (ep > t_a - WIN_S - 1e-6) & (ep < t_b + 1e-6)
                if not mm.any() or not covers(np.sort(ep[mm]), t_a, t_b): continue
                idx = np.where(mm)[0][np.argsort(ep[mm])]
                ud = np.concatenate([np.asarray(H["waves"][int(r)][0], float) for r in idx]); e0 = float(ep[idx[0]])
                dist = float(np.hypot(haversine_km(ev["lat"], ev["lon"], cand_meta[s]["lat"], cand_meta[s]["lon"]), ev["dep"]))
                i0 = int(round((t_a - e0) * FS))
                j = sta_lta_first(ud[i0:], i_min=int(round((SEG_PRE_S - 1.0) * FS)))   # 発生 − 1 s より前の立ち上がり(前の地震)は取らない
                tr = None if j is None else (e0 + (i0 + j) / FS) - jst_epoch(ev["t"])
                if ev["main"]: sec.append((s, dist, ud, e0))
                if tr is not None and len(resid) < CLOCK_NSTA: resid.append(tr - dist / CLOCK_VP)
            md = float(np.median(np.abs(resid))) if resid else None
            G["clock"].append(dict(origin_jst=f"{ev['t']}", mj=ev["mag"], mainshock=ev["main"], n=len(resid), median_abs_resid_s=md,
                                   pass_=bool(md is not None and md <= CLOCK_TOL and len(resid) >= 4)))
        G["clock_pass"] = bool(G["clock"][0]["pass_"] and all(c["pass_"] for c in G["clock"][1:] if c["n"] >= 4))
    G["band_ratio_ref"] = ref["band_ratio_median"]
    rr = G["band_ratio_out"] / ref["band_ratio_median"] if ref["band_ratio_median"] and np.isfinite(ref["band_ratio_median"]) else float("nan")
    G["band_ratio_out_over_ref"] = rr
    G["ref_pass"] = bool(ref["zcheck_pass"] and G["out_zcheck"]["pass_"]); G["dup_pass"] = G["dup"] == 0
    G["cover_pass"] = G["cover_frac_ge4"] >= COVER_STOP
    all_pass = G["ref_pass"] and G["dup_pass"] and G["cover_pass"] and G["clock_pass"]
    rep = dict(script="25_02_shimane2018_hinet_to_h5.py", version=VERSION, h5=str(h5p), n_windows=n_tot, stations=keep,
               presence={s: pres[s] for s in keep}, n_blocks=nb, n_blocks_planned=len(plan), n_blocks_missing=len(missing),
               missing_blocks=missing, allow_missing=bool(allow_missing), ref=ref, gates=G, all_gates_pass=bool(all_pass), partial=bool(partial))
    json.dump(rep, open(OUT / "data" / ("25_02_report_partial.json" if partial else "25_02_report.json"), "w"), indent=1, default=str)
    print(f"[25_02] G-ref: 参照 dtype {ref['waves_dtype']}・z-score 確認 {'PASS' if ref['zcheck_pass'] else 'FAIL'}  出力の z-score 確認 "
          f"{'PASS' if G['out_zcheck']['pass_'] else 'FAIL'}(最大 |平均| {G['out_zcheck']['max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
          f"{G['out_zcheck']['max_abs_std_minus_1']:.3g})")
    print(f"[25_02] G-dup: 重なり {G['dup']}  " + ("PASS" if G["dup"] == 0 else "FAIL"))
    print(f"[25_02] G-cover({G['cover_n_events']} 地震): Mj ≥ 1.5 の地震で 4 局以上が覆う割合 {G['cover_frac_ge4']:.3f}(覆う局の数の中央値 "
          f"{G['cover_median_stations']:.0f})  " + ("PASS" if G["cover_frac_ge4"] >= COVER_OK else "注意" if G["cover_frac_ge4"] >= COVER_STOP else "FAIL"))
    for c in G["clock"]:
        cm = c["median_abs_resid_s"]
        print(f"[25_02] G-clock{'(本震)' if c['mainshock'] else '(他の地震)'} {c['origin_jst'][:22]} Mj {c['mj']}: 近い局 {c['n']} で、"
              f"STA/LTA の立ち上がり − 震源距離/6.0 km/s の |差| の中央値 {'—' if cm is None else f'{cm:.2f}'} s  "
              + ("PASS" if c["pass_"] else ("FAIL" if c["mainshock"] or c["n"] >= 4 else "判定なし(立ち上がりが取れた局が 4 未満)")))
    print(f"[25_02] G-clock まとめ: " + ("PASS" if G["clock_pass"] else "FAIL"))
    print(f"[25_02] G-spec(記録だけ): 0.1–1 Hz / 1–20 Hz の力の比の中央値 参照 {G['band_ratio_ref']:.3g}・出力 {G['band_ratio_out']:.3g}"
          f"(比 {rr:.2f})" + ("  注意: 3 倍以上違う(参照の h5 でフィルタをかけた可能性。記録だけで、止めずに先に進む。限界に書く)"
                              if np.isfinite(rr) and (rr > 3 or rr < 1 / 3) else ""))
    figures(PDFD, files, keep, cand_meta, ml, mo, sec, mt, "_partial" if partial else "")
    if not all_pass:                                           # ゲートに通らなければ、使う名前の h5 は作らない
        failed = h5p.with_name(h5p.stem + "_FAILED.h5"); os.replace(tmpp, failed)
        why = [k for k, v in (("G-ref", G["ref_pass"]), ("G-dup", G["dup_pass"]), ("G-cover", G["cover_pass"]), ("G-clock", G["clock_pass"])) if not v]
        if why == ["G-clock"]:                                 # 21_20・24・25: 表示の文だけ(止まり方は 21_04b v1.1 と同じ)
            sys.exit(f"[25_02] STOP(G-clock だけ): h5 は {failed.name}、局の表は {stp.name}.part にした。事前登録 25 の規則では "
                     "G-clock は記録だけで、時刻は G-clock2(25_04d)で決める。セル N10 に、この 2 つのファイルを渡して進む(この出力を貼る)")
        sys.exit(f"[25_02] STOP({', '.join(why)}): h5 は {failed.name} にした(セル 10 には進まない。この出力を貼って相談)")
    os.replace(tmpp, h5p); os.replace(stp.with_suffix(".csv.part"), stp)
    sfx = "_partial" if partial else ""
    print(f"[25_02] 出力: {h5p}(窓 {n_tot})  {OUT / 'data' / 'catalog' / f'stations_shimane2018{sfx}.csv'}  {OUT / 'data' / f'25_02_report{sfx}.json'}"
          + ("(煙試験の確認用。本番の組み立てはセル 9)" if partial else ""))


def figures(PDFD, files, keep, meta, ml, mo, sec, mt, suf=""):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9})
    M = np.zeros((len(keep), len(files)))
    for j, f in enumerate(files):
        z = np.load(f, allow_pickle=False); s_, c_ = np.unique(z["stations"], return_counts=True); d = dict(zip(s_.tolist(), c_.tolist()))
        span = int(f.stem.split("_")[-1]); M[:, j] = [min(1.0, d.get(s, 0) / (span * 2)) for s in keep]
    fig, ax = plt.subplots(figsize=(10, 0.16 * len(keep) + 1.6))
    im = ax.imshow(M, aspect="auto", interpolation="nearest", cmap="Greys", vmin=0, vmax=1)
    ax.set_yticks(range(len(keep))); ax.set_yticklabels([f"{s} ({haversine_km(ml, mo, meta[s]['lat'], meta[s]['lon']):.0f} km)" for s in keep], fontsize=6)
    ax.set_xlabel("Download block (time order)"); ax.set_title("Hi-net data present per station and block (fraction of 30-s windows kept)")
    cb = fig.colorbar(im, ax=ax, pad=0.01); cb.set_label("Fraction kept")
    fig.tight_layout(); fig.savefig(PDFD / f"25_02_coverage{suf}.pdf", bbox_inches="tight"); plt.close(fig)
    if sec:
        sec = sorted(sec, key=lambda q: q[1])
        fig, ax = plt.subplots(figsize=(8.5, 0.45 * len(sec) + 1.8))
        t0 = jst_epoch(mt)
        for i, (s, dist, ud, e0) in enumerate(sec):
            t = e0 + np.arange(len(ud)) / FS - t0
            sc = np.percentile(np.abs(ud), 99.5) + 1e-9
            ax.plot(t, i + 0.42 * np.clip(ud / sc, -1, 1), lw=0.4, color="k")
            ax.plot([dist / CLOCK_VP] * 2, [i - 0.45, i + 0.45], color="tab:red", lw=1.2,
                    label=(f"Predicted P (hypocentral distance / {CLOCK_VP} km/s)" if i == 0 else None))
        ax.set_yticks(range(len(sec))); ax.set_yticklabels([f"{s} ({d:.0f} km)" for s, d, _, _ in sec], fontsize=7)
        ax.set_xlim(-SEG_PRE_S, SEG_POST_S); ax.set_ylim(-0.7, len(sec) - 0.3)
        ax.set_xlabel("Time since JMA origin of the mainshock (s); 30-s windows are z-scored separately")
        ax.set_title("Mainshock, vertical component of the nearest stations (clipped at the 99.5th percentile)")
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False); ax.grid(alpha=0.3, axis="x")
        fig.tight_layout(); fig.savefig(PDFD / f"25_02_mainshock{suf}.pdf", bbox_inches="tight"); plt.close(fig)


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default=str(ROOT / "data" / "catalog" / "jma_shimane2018.csv"))
    ap.add_argument("--summary", default=str(ROOT / "data" / "catalog" / "25_01_shimane2018_catalog.json"))
    ap.add_argument("--ref-h5", required=True, help="鳥取 2026 の tottori_all_100Hz.h5(形を写すため。読むだけ)")
    ap.add_argument("--out", default=("/content/drive/MyDrive/ARGUS_shimane2018" if Path("/content/drive").exists()
                                      else str(ROOT.parent / "ARGUS_shimane2018")))
    ap.add_argument("--tmp", default=("/content/hinet_tmp" if Path("/content").exists() else tempfile.gettempdir()))
    ap.add_argument("--n-sta", type=int, default=50)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-blocks", type=int, default=0, help="煙試験: 最初の N 区切りだけ(0 = 全部)")
    ap.add_argument("--assemble", action="store_true")
    ap.add_argument("--partial", action="store_true", help="煙試験の確認: 取った区切りだけで組み立てて、ゲートを表示する(別の名前の h5)")
    ap.add_argument("--allow-missing", action="store_true", help=f"何度回しても取れない区切りが残り、取れた割合が {MIN_FETCHED} 以上の時だけ組み立てを続ける")
    ap.add_argument("--restore-selection", action="store_true", help="アカウントの局の選択を保存した元の状態に戻すだけ(途中で落ちた時)")
    ap.add_argument("--break-lock", action="store_true", help="--restore-selection と一緒に: 切れた実行の印(data/25_02.lock)を消す")
    a = ap.parse_args()
    OUT = Path(a.out); PDFD = OUT / "PDF"
    for d in (OUT / "data" / "blocks", PDFD): d.mkdir(parents=True, exist_ok=True)
    tmp_root = Path(a.tmp); tmp_root.mkdir(parents=True, exist_ok=True)
    if not Path(a.summary).exists(): sys.exit(f"[25_02] STOP: {a.summary} が無い(25_01 を先に回す)")
    summ = json.load(open(a.summary))
    rows = []
    for r in csv.DictReader(open(a.catalog)):
        rows.append(dict(t=datetime.strptime(r["time"][:22].ljust(22, "0"), "%Y-%m-%d %H:%M:%S.%f"), mag=float(r["mag"]),
                         lat=float(r["latitude"]), lon=float(r["longitude"]), dep=float(r["depth_km"])))
    org = [r["t"] for r in rows if r["mag"] >= MIN_MAG - 1e-9]
    plan = plan_blocks(org)
    tot_min = sum(s for _, s in plan)
    print(f"[25_02] {VERSION}  地震(Mj ≥ 1.5){len(org)} → 区切り {len(plan)}(分の合計 {tot_min}、最長 {max(s for _, s in plan)} 分)")
    rng = np.random.default_rng(7)
    ref = read_ref(a.ref_h5, rng)
    print(f"[25_02] 参照の h5: 窓 {ref['n_windows']}  /waves {ref['waves_dtype']}  /stations {ref['stations_dtype']}  "
          f"/window_epoch {ref['epoch_dtype']}  chunks {ref['chunks']}  圧縮 {ref['compression']}  属性 {ref['attrs']}  "
          f"他のデータ {ref['other_datasets']}")
    print(f"[25_02] 参照の z-score の確認(無作為 {REF_NSAMPLE} 窓): 最大 |平均| {ref['zcheck_max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
          f"{ref['zcheck_max_abs_std_minus_1']:.3g}  " + ("PASS" if ref["zcheck_pass"] else "FAIL")
          + f"  30 s 格子にそろう割合 {ref['grid30_frac']:.3f}(余り {ref['grid30_residues']})  0.1–1/1–20 Hz の力の比 {ref['band_ratio_median']:.3g}")
    if not ref["zcheck_pass"]: sys.exit("[25_02] STOP(G-ref): 参照の h5 が窓ごとの z-score に見えない(この行を貼って相談)")
    dt = np.dtype(ref["waves_dtype"])
    plan_p = OUT / "data" / "25_02_plan.json"
    sel_p = OUT / "data" / "25_02_initial_selection.json"

    if a.assemble:
        P = json.load(open(plan_p)) if plan_p.exists() else None
        if P is None: sys.exit("[25_02] STOP: 計画の 25_02_plan.json が無い")
        assemble(OUT, PDFD, ref, summ, rows, P["candidates"], a.n_sta, plan, partial=a.partial, allow_missing=a.allow_missing); return

    lock = OUT / "data" / "25_02.lock"
    if a.restore_selection:
        if a.break_lock and lock.exists():
            print(f"[25_02] 切れた実行の印を消した: {lock.read_text().strip()}"); lock.unlink()
        check_lock(lock)                                       # 動いている実行があれば、その選択を変えない
        if not sel_p.exists(): sys.exit(f"[25_02] STOP: 保存した選択 {sel_p} が無い")
        restore_selection(hinet_client(), sel_p); return
    if not shutil.which("win2sac_32") and not a.dry_run: sys.exit("[25_02] STOP: win2sac_32 が PATH に無い(ノートの セル 3)")
    client = hinet_client()
    stl = client.get_station_list(NET)
    ml, mo = summ["mainshock"]["lat"], summ["mainshock"]["lon"]
    n0 = len(stl)
    stl = [s for s in stl if s.latitude is not None and s.longitude is not None and s.elevation is not None]
    if len(stl) < n0: print(f"[25_02] 緯度・経度・標高のどれかが無い局 {n0 - len(stl)} は候補から外した")
    stl.sort(key=lambda s: haversine_km(ml, mo, s.latitude, s.longitude))
    cands = stl[:a.n_sta + EXTRA_CAND]
    cmeta = {s.name: dict(lat=s.latitude, lon=s.longitude, elev_m=float(s.elevation),
                          dist_km=float(haversine_km(ml, mo, s.latitude, s.longitude))) for s in cands}
    print(f"[25_02] 候補局 {len(cands)}(本震から {cmeta[cands[0].name]['dist_km']:.1f}〜{cmeta[cands[-1].name]['dist_km']:.1f} km): "
          + " ".join(s.name for s in cands))
    json.dump(dict(version=VERSION, n_blocks=len(plan), total_minutes=tot_min, blocks=[[f"{b:%Y-%m-%d %H:%M}", s] for b, s in plan],
                   candidates=cmeta, n_sta=a.n_sta, ref=ref), open(plan_p, "w"), indent=1, default=str)
    gb = tot_min * 2 * len(cands) * 3 * WIN_N * dt.itemsize / 1e9
    free = shutil.disk_usage(OUT).free / 1e9
    print(f"[25_02] 置き場所の見込み: 区切りのファイル約 {gb:.1f} GB + 組み立てた h5 約 {gb * a.n_sta / len(cands):.1f} GB"
          f"(Drive の空き {free:.0f} GB。ここに出るのは Colab から見た空きで、Drive の契約の上限とは違うことがある)")
    if a.dry_run:
        print(f"[25_02] 計画だけ(--dry-run): {plan_p}。1 区切りに 30 s かかるとして約 {len(plan) * 30 / 3600:.1f} 時間、"
              f"60 s なら約 {len(plan) * 60 / 3600:.1f} 時間(煙試験で測る)")
        return
    check_lock(lock)                                           # 片付けより前に印を取る(別の実行の書きかけを消さないため)
    touch_lock(lock)
    selected = False
    try:
        if not sel_p.exists():
            names0 = [s.name for s in client.get_selected_stations(NET)]
            json.dump(dict(saved_utc=datetime.now(timezone.utc).isoformat(), stations=names0), open(sel_p, "w"), indent=1)
            print(f"[25_02] アカウントの今の局の選択を保存した({len(names0) if names0 else '全局'}): {sel_p}")
        for f in (OUT / "data" / "blocks").glob("*.tmp"): f.unlink()          # 前に途中で切れた書きかけ
        for b, s in plan:                                                       # 読めない「済み」は取り直す
            f = OUT / "data" / "blocks" / blk_name(b, s)
            if f.exists() and not blk_ok(f):
                print(f"[25_02] 読めない区切りのファイル {f.name} を消して取り直す"); f.unlink()
        todo = [(b, s) for b, s in plan if not blk_done(OUT, b, s)]
        need = (sum(s for _, s in todo) * 2 * len(cands) * 3 * WIN_N * dt.itemsize / 1e9) + gb * a.n_sta / len(cands)
        if free < 1.1 * need: sys.exit(f"[25_02] STOP: 置き場所が足りない見込み(残りの区切りと h5 で約 {need:.1f} GB、空き {free:.0f} GB)")
        if a.max_blocks:                                     # 煙試験: 本震の区間 [−10 s, +45 s] に掛かる区切りを最初に(G-clock を早く確かめる)
            mt = datetime.strptime(summ["mainshock"]["origin_jst"][:22].ljust(22, "0"), "%Y-%m-%d %H:%M:%S.%f")
            ma, mb = mt - timedelta(seconds=SEG_PRE_S), mt + timedelta(seconds=SEG_POST_S)
            todo.sort(key=lambda bs: 0 if (bs[0] < mb and bs[0] + timedelta(minutes=bs[1]) > ma) else 1)
            todo = todo[:a.max_blocks]
        n_done = sum(1 for b, s in plan if blk_done(OUT, b, s))
        print(f"[25_02] 取る区切り {len(todo)}(済み {n_done}/{len(plan)})")
        names = [s.name for s in cands]
        if not todo:
            print("[25_02] 取る区切りが無い(全部済み)。次はセル 9(--assemble)"); return
        max_span = max(1, min(60, 12000 // (3 * len(names))))
        ladder = [m for m in (max_span, 20, 10, 5) if m <= max_span]           # v1.1: 失敗したら要求を短くする
        ladder = sorted(set(ladder), reverse=True)
        cur = 0                                                                 # 今の実行で使う最初の長さ(取れた長さを覚える)
        fails, t_start = 0, time.time()
        client.select_stations(NET, names); selected = True
        got = [s.name for s in client.get_selected_stations(NET)]
        if not got or not set(got) <= set(names):
            sys.exit(f"[25_02] STOP: アカウントの局の選択が候補にならなかった(選ばれた局 {len(got)})。全局のまま取ると何倍も時間がかかる")
        if set(got) != set(names): print(f"[25_02] 注意: 選べた局 {len(got)} が候補 {len(names)} より少ない(無い局: {sorted(set(names) - set(got))[:10]})")
        for i, (b, s) in enumerate(todo):
            t1 = time.time(); res = None
            tries = ladder[cur:] if s > ladder[-1] else ladder[cur:cur + 1]
            tries = tries + [ladder[-1]] * max(0, 3 - len(tries))             # どの区切りも 3 回以上は試す(v1 と同じ)
            for k, ms in enumerate(tries):
                touch_lock(lock)                               # v1.1: 試すたびに動いている印を新しくする(失敗が続いても印が古くならない)
                try:
                    res = fetch_block(client, b, s, names, dt, tmp_root, ms)
                except Exception as e:
                    print(f"    区切り {b:%Y-%m-%d %H:%M} ({s} 分・1 回の要求 {ms} 分) の {k + 1} 回目で例外: {type(e).__name__}: {e}")
                    res = None
                if res is not None:
                    if ms < ladder[cur] and s > ms:
                        cur = ladder.index(ms)
                        print(f"    区切り {b:%Y-%m-%d %H:%M}: 1 回の要求を {ms} 分にして取れた(この実行の残りは {ms} 分から始める)")
                    break
                if k < len(tries) - 1: time.sleep(30)
            if res is None:
                fails += 1
                print(f"    区切り {b:%Y-%m-%d %H:%M} ({s} 分) を {len(tries)} 回とも取れなかった(飛ばす。次に回すと取り直す)")
                if fails >= 3: sys.exit("[25_02] STOP: 3 つの区切りで続けて取れなかった(Hi-net の状態を確かめて、もう一度回すと続きから)")
                continue
            fails = 0
            dst = OUT / "data" / "blocks" / blk_name(b, s); part = dst.with_name(dst.name[:-4] + ".tmp")
            with open(part, "wb") as fh:                      # 書き終わってから名前を付ける(.tmp は済みと数えない)
                np.savez(fh, stations=res["stations"], epoch=res["epoch"], waves=res["waves"], chan=json.dumps(res["chan"]),
                         stat=json.dumps(res["stat"]), scale=res["scale"])
            os.replace(part, dst)
            touch_lock(lock)                                   # 動いている印を新しくする(30 分より古い印は止まった印とみなす)
            el = time.time() - t_start
            print(f"  [{i + 1}/{len(todo)}] {b:%Y-%m-%d %H:%M} {s:3d} 分  局 {res['stat']['n_sta_files']}  窓 {res['stat']['windows']}"
                  f"(捨てた {res['stat']['windows_dropped']}・頭が合わない {res['stat']['bad_header']}・短い {res['stat']['short']})  "
                  f"{time.time() - t1:.0f} s  残りの見込み約 {el / (i + 1) * (len(todo) - i - 1) / 3600:.1f} 時間")
    finally:
        if selected: restore_selection(client, sel_p)
        lock.unlink(missing_ok=True)
    left = sum(1 for b, s in plan if not blk_done(OUT, b, s))
    print(f"[25_02] 終わり: 残りの区切り {left}/{len(plan)}" + ("(全部済んだら --assemble)" if left == 0 else "(もう一度回すと続きから)"))


if __name__ == "__main__":
    main()
