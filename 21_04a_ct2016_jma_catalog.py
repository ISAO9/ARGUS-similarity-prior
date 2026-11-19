#!/usr/bin/env python3
# =============================================================================
# Script : 21_04a_ct2016_jma_catalog.py  (v1)
#          [鳥取県中部 2016(本震 2016-10-21 14:07 JST、M6.6)の気象庁の震源を、21_02 と同じ形の CSV にする]
# Project: ARGUS(新生)— 2 つ目の余震系列での確認(21_04)の入力の 1 つ目
#
# 何をするか:
#   1. 気象庁の震源ファイル h2016.zip(地震ごとに 96 バイトの震源レコード 1 行、時刻は日本時間)を
#      https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2016.zip から data/catalog/jma_raw/ に取る
#      (登録不要。既にあれば取らない。--hypo で手元のファイルを指定してもよい)。
#   2. 震源レコードを列の位置どおりに読む(書式: https://www.data.jma.go.jp/eqev/data/bulletin/data/format/hypfmt_e.html)。
#      読み方は KRITES の 02_jma_arrivals.py(気象庁の書式と照合済み)の震源レコードの部分と同じ列。
#        1 列 = 機関(J だけ使う。U・I は他機関) / 2–5 年 / 6–7 月 / 8–9 日 / 10–11 時 / 12–13 分 / 14–17 秒(F4.2)
#        22–24 緯度の度 / 25–28 緯度の分(F4.2) / 33–36 経度の度 / 37–40 経度の分(F4.2) / 45–49 深さ(F5.2 km)
#        53–54 マグニチュード 1(F2.1、負は "-1"〜"-9" = −0.1〜−0.9、"A0"〜"A9" = −1.0〜−1.9、"B0" = −2.x、"C0" = −3.x)
#        55 その種類 / 60 震源の精度 / 61 補助情報 / 96 震源決定の印(K・S・k・s = 手動、A・a = 自動、N = 決まらない・
#        採らない・固定、F = 遠方)
#      Fw.d の欄は小数点が省かれている。空白は 0 として読む(気象庁の書式では、深さを固定した震源などで小数の部分が空白)。
#   3. 本震を決める(事前に決めた規則): 2016-10-21 の J の震源のうち Mj が最大の地震。発生時刻が 14:07:22.57 JST
#      (気象庁の震源過程の資料の名前 2016102114072257 による)から 5 秒以内、Mj ≥ 6.4、深さ 5–20 km、
#      緯度 35.2–35.6・経度 133.6–134.1 の中、でなければ STOP(読み方の誤りか別のファイル)。
#   4. 範囲(事前に決めた規則。21_02 の西鳥取の箱と同じ大きさ):
#      - 箱 = 本震の緯度 ± 0.15°、経度 ± 0.175°(西鳥取の箱は 35.15–35.45 × 133.00–133.35 = 0.30° × 0.35°)
#      - 期間 = 本震の 2 日前から 24 日後(日本時間。21_02 の鳥取 2026 は本震の約 1.4 日前〜約 23.9 日後)
#      - 使う震源: 機関 J、精度が M(マッチドフィルタ)・8(決まらない)・9(最寄りの局で固定)でない、
#        補助情報が 3(人工)・5(低周波)でない、震源決定の印が N(決まらない・採らない・固定)・F(遠方)でない、
#        緯度・経度・Mj・深さが空白でない。印ごとの数を JSON に書く(手動と自動の混ざり方を記録するため)
#   5. 出力: data/catalog/jma_ct2016.csv(列 time, latitude, longitude, depth_km, mag と、記録用の det_flag。time は日本時間の
#      "YYYY-MM-DD HH:MM:SS.ff"。jma_tottori_2026.csv と同じ列と書き方で、15_01c がそのまま読める。15_01c は先頭 21 文字
#      だけを読むので、発生時刻は 0.1 s 単位に切り捨てられる。2026 の CSV でも同じで、21_02 は地震ごとに走時の残りの
#      中央値を引くので、この切り捨ては震源の誤差に効かない)と
#      data/catalog/21_04a_ct2016_catalog.json(本震・箱・期間・数・除いた数。15_01c と 21_04b に渡す箱はここから読む)。
#      数: 全体、Mj ≥ 1.5、Mj ≥ 2.0、pool(本震 + 72 時間まで)、試験の候補(本震 + 72 時間より後の 1.5 ≤ Mj < 2.0)、
#      本震 + 72 時間より後の Mj ≥ 2.0(21_02 と同じく過去の地震の一覧にだけ入る)。
#      試験の候補は「キャッシュで P が測れた地震」の前の数なので、本当の試験の数はこれより少なくなる。
#   6. 図: PDF/21_04a_ct2016_catalog.pdf(時刻と Mj、Mj の頻度。白背景・英語・凡例は枠の外)。
#
# 止める条件(STOP): 読み方の試験に失敗・ファイルが取れない・zip の中にファイルが無い・レコードが 96 バイトでない行が 1% を
#   超える・2016-10-21 の震源が無い・本震の規則に合わない・本震が除く印を持つ・箱の中で期間内の Mj ≥ 1.5 が 0。
# 限界: 正解も過去の地震も気象庁の震源(21_02 と同じ)。h2016 は確定値で、21_02 の jma_tottori_2026.csv(2026 年の一元化
#   震源)とは確定の段階が違いうる。低周波・人工・マッチドフィルタ・決まらない震源は除いた(2026 の CSV でそれを除いたかは
#   記録が無い。この除外は 2016 だけ)。手動と自動の震源が混ざる(印ごとの数を JSON に記録)。
#
# Usage : (Colab、ノート 21_04_ct2016_colab.ipynb の セル 5)
#         !python /content/drive/MyDrive/ARGUS/src/21_04a_ct2016_jma_catalog.py
#         (手元で: cd ~/SWIFT && uv run python src/21_04a_ct2016_jma_catalog.py --selftest)
# Output: data/catalog/jma_ct2016.csv / data/catalog/21_04a_ct2016_catalog.json / PDF/21_04a_ct2016_catalog.pdf
# =============================================================================
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import urllib.request
import zipfile
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

VERSION = "v1"
ROOT = Path(__file__).resolve().parent.parent
URL = "https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2016.zip"
REC_LEN = 96
MAIN_JST = datetime(2016, 10, 21, 14, 7, 22, 570000)    # 気象庁の震源過程の資料名 2016102114072257
MAIN_TOL_S, MAIN_MIN_MJ, MAIN_DEPTH = 5.0, 6.4, (5.0, 20.0)
MAIN_LAT, MAIN_LON = (35.2, 35.6), (133.6, 134.1)
HALF_LAT, HALF_LON = 0.15, 0.175                         # 西鳥取の箱(0.30° × 0.35°)と同じ大きさ
DAYS_BEFORE, DAYS_AFTER = 2.0, 24.0
POOL_H, MIN_MAG, FRESH_MAX_MAG = 72.0, 1.5, 2.0          # 21_02 と同じ
BAD_PRECISION = {"M", "8", "9"}
BAD_SUBSID = {"3", "5"}
BAD_DETFLAG = {"N", "F"}


def col(rec: bytes, a: int, b: int) -> str:
    """1 始まり・両端を含むバイトの範囲を ASCII として返す"""
    return rec[a - 1:b].decode("ascii", errors="replace")


def read_int(s: str):
    s = s.strip()
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        return None


def read_fwd(s: str, d: int):
    """Fortran の Fw.d(小数点を省いた形)。空白は 0 として読む。全部空白なら None。'.' があればそのまま読む"""
    if not s.strip():
        return None
    if "." in s:
        try:
            return float(s.strip())
        except ValueError:
            return None
    neg = "-" in s
    t = s.replace("-", " ").replace(" ", "0")
    if not t.isdigit():
        return None
    v = int(t) / 10 ** d
    return -v if neg else v


def read_mag(s: str):
    """F2.1 のマグニチュード。'28' → 2.8、' 9' → 0.9、'-5' → −0.5、'A5' → −1.5、'B0' → −2.0、'C3' → −3.3。
    2 文字目は必ず数字(そうでなければ読めないとして None)"""
    if len(s) != 2 or not s.strip() or not s[1].isdigit():
        return None
    if s[0] in "ABC":
        return -(ord(s[0]) - ord("A") + 1) - int(s[1]) / 10.0
    if s[0] == "-":
        return -int(s[1]) / 10.0
    if s[0] == " " or s[0].isdigit():
        return int(s.replace(" ", "0")) / 10.0
    return None


def parse_hypo(rec: bytes) -> dict:
    yr, mo, dy = read_int(col(rec, 2, 5)), read_int(col(rec, 6, 7)), read_int(col(rec, 8, 9))
    hh, mi = read_int(col(rec, 10, 11)), read_int(col(rec, 12, 13))
    sec = read_fwd(col(rec, 14, 17), 2)
    latd, latm = read_int(col(rec, 22, 24)), read_fwd(col(rec, 25, 28), 2)
    lond, lonm = read_int(col(rec, 33, 36)), read_fwd(col(rec, 37, 40), 2)
    out = dict(agency=col(rec, 1, 1), origin_jst=None,
               lat=None if latd is None else latd + (latm or 0.0) / 60.0,
               lon=None if lond is None else lond + (lonm or 0.0) / 60.0,
               depth_km=read_fwd(col(rec, 45, 49), 2), mag=read_mag(col(rec, 53, 54)),
               mag_type=col(rec, 55, 55).strip(), precision=col(rec, 60, 60).strip(), subsidiary=col(rec, 61, 61).strip(),
               det_flag=col(rec, 96, 96).strip())
    if None not in (yr, mo, dy, hh, mi) and sec is not None:
        try:
            out["origin_jst"] = datetime(yr, mo, dy, hh, mi) + timedelta(seconds=sec)
        except ValueError:
            out["origin_jst"] = None
    return out


def read_records(raw: bytes):
    recs, n_bad = [], 0
    for ln in raw.splitlines():
        if not ln.strip():
            continue
        r = ln.rstrip(b"\r\n")
        if len(r) != REC_LEN:
            n_bad += 1
            r = r[:REC_LEN].ljust(REC_LEN, b" ")
        recs.append(r)
    return recs, n_bad


def fmt_time(t: datetime) -> str:
    """'YYYY-MM-DD HH:MM:SS.ff'(jma_tottori_2026.csv と同じ。15_01c は先頭 21 文字を %Y-%m-%d %H:%M:%S.%f で読む)"""
    cs = int(round(t.microsecond / 1e4))
    base = t.replace(microsecond=0)
    if cs == 100:
        base, cs = base + timedelta(seconds=1), 0
    return base.strftime("%Y-%m-%d %H:%M:%S") + f".{cs:02d}"


def selftest():
    def check(c, msg):
        if not c: sys.exit(f"[21_04a] STOP: 読み方の試験に失敗: {msg}")
    def put(buf, a, b, s):
        check(len(s) == b - a + 1, (a, b, s))
        buf[a - 1:b] = s.encode("ascii")
    def hyp(y, mo, d, h, mi, s4, latd, latm4, lond, lonm4, dep5, mag2, prec="1", sub="1", ag="J"):
        r = bytearray(b" " * REC_LEN)
        put(r, 1, 1, ag); put(r, 2, 5, f"{y:4d}"); put(r, 6, 7, f"{mo:02d}"); put(r, 8, 9, f"{d:02d}")
        put(r, 10, 11, f"{h:02d}"); put(r, 12, 13, f"{mi:02d}"); put(r, 14, 17, s4)
        put(r, 22, 24, f"{latd:3d}"); put(r, 25, 28, latm4); put(r, 33, 36, f"{lond:4d}"); put(r, 37, 40, lonm4)
        put(r, 45, 49, dep5); put(r, 53, 54, mag2); put(r, 55, 55, "J"); put(r, 60, 60, prec); put(r, 61, 61, sub)
        return bytes(r)
    a = parse_hypo(hyp(2016, 10, 21, 14, 7, "2257", 35, "2280", 133, "5130", " 1100", "66"))
    check(a["origin_jst"] == datetime(2016, 10, 21, 14, 7, 22, 570000), repr(a["origin_jst"]))
    check(abs(a["lat"] - (35 + 22.80 / 60)) < 1e-12 and abs(a["lon"] - (133 + 51.30 / 60)) < 1e-12, 'abs(a["lat"] - (35 + 22.80 / 60)) < 1e-12 and abs(a["lon"] - (133 + 51.30 / 60)) < 1e-12')
    check(abs(a["depth_km"] - 11.0) < 1e-12 and abs(a["mag"] - 6.6) < 1e-12, 'abs(a["depth_km"] - 11.0) < 1e-12 and abs(a["mag"] - 6.6) < 1e-12')
    b = parse_hypo(hyp(2016, 10, 22, 0, 0, "12  ", 35, "22  ", 133, "51  ", " 10  ", "-5", prec="3"))   # 固定の震源の書き方(深さは 45–47 列に整数、48–49 列は空白)
    check(b["origin_jst"] == datetime(2016, 10, 22, 0, 0, 12) and abs(b["lat"] - (35 + 22 / 60)) < 1e-12, 'b["origin_jst"] == datetime(2016, 10, 22, 0, 0, 12) and abs(b["lat"] - (35 + 22 / 60)) < 1e-12')
    check(abs(b["depth_km"] - 10.0) < 1e-12 and abs(b["mag"] + 0.5) < 1e-12, 'abs(b["depth_km"] - 10.0) < 1e-12 and abs(b["mag"] + 0.5) < 1e-12')
    check(read_mag("A5") == -1.5 and read_mag("B0") == -2.0 and read_mag("C3") == -3.3 and read_mag(" 9") == 0.9, 'read_mag("A5") == -1.5 and read_mag("B0") == -2.0 and read_mag("C3") == -3.3 and read_mag(" 9") == 0.9')
    check(read_fwd("  12", 2) == 0.12 and read_fwd("    ", 2) is None and read_fwd(" 1245", 2) == 12.45, 'read_fwd("  12", 2) == 0.12 and read_fwd("    ", 2) is None and read_fwd(" 1245", 2) == 12.45')
    check(read_mag("5 ") is None and read_mag("- ") is None and read_mag(" -") is None and read_mag("28") == 2.8, "read_mag の不正な形")
    check(fmt_time(datetime(2016, 10, 21, 14, 7, 22, 570000)) == "2016-10-21 14:07:22.57", 'fmt_time(datetime(2016, 10, 21, 14, 7, 22, 570000)) == "2016-10-21 14:07:22.57"')
    check(fmt_time(datetime(2016, 10, 21, 14, 7, 22, 999000)) == "2016-10-21 14:07:23.00", 'fmt_time(datetime(2016, 10, 21, 14, 7, 22, 999000)) == "2016-10-21 14:07:23.00"')
    t = datetime.strptime(fmt_time(datetime(2016, 10, 21, 14, 7, 5, 50000))[:21].ljust(21, "0"), "%Y-%m-%d %H:%M:%S.%f")
    check(t == datetime(2016, 10, 21, 14, 7, 5, 0), 't == datetime(2016, 10, 21, 14, 7, 5, 0)')  # 15_01c は先頭 21 文字だけ読むので 0.1 s 単位に切り捨てる(2026 も同じ)
    print("[21_04a] selftest: 震源レコードの読み方の試験に全て合格")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hypo", default="", help="手元の h2016.zip か展開したファイル(無ければ取る)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest(); return
    selftest()
    CAT = ROOT / "data" / "catalog"; RAWD = CAT / "jma_raw"; PDFD = ROOT / "PDF"
    for d in (CAT, RAWD, PDFD): d.mkdir(parents=True, exist_ok=True)
    src = Path(a.hypo) if a.hypo else RAWD / "h2016.zip"
    if not src.exists():
        print(f"[21_04a] 取得: {URL}")
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (ARGUS research)"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = r.read()
        except Exception as e:
            sys.exit(f"[21_04a] STOP: {URL} が取れない({e})。ブラウザで取って --hypo で指定する")
        src.write_bytes(data)
    sha = hashlib.sha256(src.read_bytes()).hexdigest()
    if zipfile.is_zipfile(src):
        with zipfile.ZipFile(src) as z:
            mem = [m for m in z.namelist() if not m.endswith("/")]
            if not mem: sys.exit("[21_04a] STOP: zip の中にファイルが無い")
            raw = b"\n".join(z.read(m) for m in mem)
    else:
        mem, raw = [src.name], src.read_bytes()
    recs, n_bad = read_records(raw)
    print(f"[21_04a] 震源ファイル {src.name}(SHA-256 {sha[:12]}…、中身 {mem})  レコード {len(recs)}  96 バイトでない行 {n_bad}")
    if not recs or n_bad > 0.01 * len(recs): sys.exit("[21_04a] STOP: 96 バイトのレコードの形でない(別のファイルの可能性)")
    H = [parse_hypo(r) for r in recs]
    J = [h for h in H if h["agency"] == "J" and h["origin_jst"] is not None]
    print(f"[21_04a] 機関 J の震源 {len(J)}(他機関 {sum(1 for h in H if h['agency'] != 'J')}、時刻が読めない {sum(1 for h in H if h['origin_jst'] is None)})")

    # ---- 本震(事前に決めた規則)
    day = [h for h in J if h["origin_jst"].date() == MAIN_JST.date() and h["mag"] is not None]
    if not day: sys.exit("[21_04a] STOP: 2016-10-21 の震源が無い")
    m = max(day, key=lambda h: h["mag"])
    dt_s = abs((m["origin_jst"] - MAIN_JST).total_seconds())
    print(f"[21_04a] 本震: {m['origin_jst']} JST  {m['lat']:.4f}N {m['lon']:.4f}E  深さ {m['depth_km']} km  M{m['mag']}{m['mag_type']}  "
          f"精度 {m['precision']}  (想定 14:07:22.57 との差 {dt_s:.2f} s)")
    ok = (dt_s <= MAIN_TOL_S and m["mag"] >= MAIN_MIN_MJ and m["depth_km"] is not None
          and MAIN_DEPTH[0] <= m["depth_km"] <= MAIN_DEPTH[1] and MAIN_LAT[0] <= m["lat"] <= MAIN_LAT[1]
          and MAIN_LON[0] <= m["lon"] <= MAIN_LON[1])
    if not ok: sys.exit("[21_04a] STOP: 本震が規則に合わない(読み方の誤りか別のファイル。この行を貼って相談)")
    if m["det_flag"] in BAD_DETFLAG or m["precision"] in BAD_PRECISION:
        sys.exit(f"[21_04a] STOP: 本震の震源が除く印(精度 {m['precision']}・震源決定の印 {m['det_flag']})を持つ(この行を貼って相談)")
    box = [round(m["lat"] - HALF_LAT, 4), round(m["lat"] + HALF_LAT, 4), round(m["lon"] - HALF_LON, 4), round(m["lon"] + HALF_LON, 4)]
    t0, t1 = m["origin_jst"] - timedelta(days=DAYS_BEFORE), m["origin_jst"] + timedelta(days=DAYS_AFTER)
    cut = m["origin_jst"] + timedelta(hours=POOL_H)

    # ---- 範囲と除外
    ex = dict(blank_lat_lon=0, outside_box_or_period=0, precision_M_8_9=0, subsidiary_3_5=0, det_flag_N_F=0, blank_mag_or_depth=0)
    rows = []
    for h in J:
        if h["lat"] is None or h["lon"] is None: ex["blank_lat_lon"] += 1; continue
        if not (box[0] <= h["lat"] <= box[1] and box[2] <= h["lon"] <= box[3] and t0 <= h["origin_jst"] <= t1):
            ex["outside_box_or_period"] += 1; continue
        if h["precision"] in BAD_PRECISION: ex["precision_M_8_9"] += 1; continue
        if h["subsidiary"] in BAD_SUBSID: ex["subsidiary_3_5"] += 1; continue
        if h["det_flag"] in BAD_DETFLAG: ex["det_flag_N_F"] += 1; continue
        if h["mag"] is None or h["depth_km"] is None: ex["blank_mag_or_depth"] += 1; continue
        rows.append(h)
    rows.sort(key=lambda h: h["origin_jst"])
    mags = np.array([h["mag"] for h in rows]); ts = [h["origin_jst"] for h in rows]
    after = np.array([t > cut for t in ts])
    n = dict(all=len(rows), mj_ge_1p5=int((mags >= MIN_MAG - 1e-9).sum()), mj_ge_2p0=int((mags >= FRESH_MAX_MAG - 1e-9).sum()),
             pool_mj_ge_1p5=int(((mags >= MIN_MAG - 1e-9) & ~after).sum()),
             test_candidates_1p5_to_2p0_after_72h=int(((mags >= MIN_MAG - 1e-9) & (mags < FRESH_MAX_MAG - 1e-9) & after).sum()),
             library_only_mj_ge_2p0_after_72h=int(((mags >= FRESH_MAX_MAG - 1e-9) & after).sum()))
    if n["mj_ge_1p5"] == 0: sys.exit("[21_04a] STOP: 箱の中・期間内の Mj ≥ 1.5 が 0")
    out_csv = CAT / "jma_ct2016.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time", "latitude", "longitude", "depth_km", "mag", "det_flag"])
        for h in rows:
            w.writerow([fmt_time(h["origin_jst"]), f"{h['lat']:.4f}", f"{h['lon']:.4f}", f"{h['depth_km']:.2f}", f"{h['mag']:.1f}",
                        h["det_flag"] or "_"])
    from collections import Counter
    flags_all = dict(Counter(h["det_flag"] or "_" for h in rows))
    flags_15 = dict(Counter(h["det_flag"] or "_" for h in rows if h["mag"] >= MIN_MAG - 1e-9))
    summ = dict(script="21_04a_ct2016_jma_catalog.py", version=VERSION, source=URL, source_file=src.name, source_sha256=sha,
                mainshock=dict(origin_jst=fmt_time(m["origin_jst"]), lat=m["lat"], lon=m["lon"], depth_km=m["depth_km"], mj=m["mag"],
                               mag_type=m["mag_type"], precision=m["precision"]),
                box=box, period_jst=[fmt_time(t0), fmt_time(t1)], pool_cut_jst=fmt_time(cut), counts=n, excluded=ex,
                det_flag_counts=dict(all=flags_all, mj_ge_1p5=flags_15),
                rules=dict(half_lat_deg=HALF_LAT, half_lon_deg=HALF_LON, days_before=DAYS_BEFORE, days_after=DAYS_AFTER,
                           pool_h=POOL_H, min_mag=MIN_MAG, fresh_max_mag=FRESH_MAX_MAG, bad_precision=sorted(BAD_PRECISION),
                           bad_subsidiary=sorted(BAD_SUBSID), bad_det_flag=sorted(BAD_DETFLAG)),
                note="test candidates are before picking; the evaluated test set is those with a measured P in the cache")
    json.dump(summ, open(CAT / "21_04a_ct2016_catalog.json", "w"), indent=1, ensure_ascii=False)
    print(f"[21_04a] 箱 {box}(緯度 0.30° × 経度 0.35°)  期間 {fmt_time(t0)} 〜 {fmt_time(t1)} JST  pool の切れ目 {fmt_time(cut)} JST")
    print(f"[21_04a] 除いた数: {ex}")
    print(f"[21_04a] 数: {n}")
    print(f"[21_04a] 震源決定の印の数(K・S・k・s = 手動、A・a = 自動。_ は空白): 全体 {flags_all}  Mj ≥ 1.5 {flags_15}")
    print(f"[21_04a] 出力: {out_csv.relative_to(ROOT)}, data/catalog/21_04a_ct2016_catalog.json")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 10})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.2), gridspec_kw=dict(width_ratios=[2.2, 1]))
    td = np.array([(t - m["origin_jst"]).total_seconds() / 86400 for t in ts])
    for sel, c, lab in ((~after, "tab:blue", "Pool (up to mainshock + 72 h)"),
                        (after & (mags >= MIN_MAG) & (mags < FRESH_MAX_MAG), "tab:red", "Test candidates (1.5 <= Mj < 2.0)"),
                        (after & (mags >= FRESH_MAX_MAG), "tab:orange", "After 72 h, Mj >= 2.0 (library only)"),
                        (after & (mags < MIN_MAG), "0.75", "After 72 h, Mj < 1.5 (not used)")):
        ax1.scatter(td[sel], mags[sel], s=5, color=c, label=f"{lab}, n = {int(sel.sum())}", rasterized=True)
    ax1.axvline(POOL_H / 24, color="k", lw=0.8, ls="--")
    ax1.set_xlabel("Days since mainshock (2016-10-21 14:07 JST)"); ax1.set_ylabel("JMA magnitude Mj")
    ax1.set_title("Central Tottori 2016, JMA hypocentres in the box", fontsize=10); ax1.grid(alpha=0.3)
    bins = np.arange(np.floor(mags.min() * 10) / 10, mags.max() + 0.2, 0.1)
    ax2.hist(mags, bins=bins, color="0.4", log=True)
    ax2.axvline(MIN_MAG, color="tab:red", lw=1); ax2.axvline(FRESH_MAX_MAG, color="tab:red", lw=1, ls="--")
    ax2.set_xlabel("Mj"); ax2.set_ylabel("Number of events"); ax2.set_title("Magnitude distribution", fontsize=10); ax2.grid(alpha=0.3)
    h_, l_ = ax1.get_legend_handles_labels()
    fig.legend(h_, l_, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=9, frameon=False, markerscale=3)
    fig.tight_layout(); fig.savefig(PDFD / "21_04a_ct2016_catalog.pdf", bbox_inches="tight"); plt.close(fig)
    print("[21_04a] 図: PDF/21_04a_ct2016_catalog.pdf")


if __name__ == "__main__":
    main()
