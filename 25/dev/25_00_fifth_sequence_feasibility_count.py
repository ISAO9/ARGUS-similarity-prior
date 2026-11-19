#!/usr/bin/env python3
# =============================================================================
# Script : 25_00_fifth_sequence_feasibility_count.py  (v1)
#          [5 つ目の余震系列の候補 5 つについて、事前登録の前に「数だけ」を数え、先に決めた順番と規則で 1 つを選ぶ。
#           震源の位置の一覧は書き出さない]
# Project: ARGUS(新生)— 5 つ目の系列での、変更記録を伴わない一発試験(25 系)の準備。事前登録を書く前の、数の確かめだけ
# 派生元 : 24_00_nagano2014_feasibility_count.py v1(SHA-256 b85fc416fe2b1cde58f36a2c025083c65d65014c80ee5ceb756023c54a3709f7)。
#          震源レコードの読み方(col・read_int・read_fwd・read_mag・parse_hypo・read_records・fmt_time・selftest)は 1 字も変えていない
#          (表示の [24_00] を [25_00] にしただけ)。除外の印・箱の大きさ・期間・pool の 72 h・1.5 ≤ Mj < 2.0・R1 の窓も 24_00 と同じ。
#          足したもの: (1) 候補を 5 つにし、期間が年をまたぐ候補は両方の年の震源ファイルを読む。(2) G-clock2 の (d) の作りに関わる
#          1 時間ごとの数(下)。(3) 同じ箱・同じ長さの、365 日前の期間の Mj ≥ 1.5 の数(箱に入る、余震でない地震の多さの記述)。
#          (4) 先に決めた順番と規則で 1 つを選んで表示する。(5) 取ったファイルが壊れていたら残さずに止める。
#
# なぜ必要か:
#   長野県北部 2014(事前登録 24)は G-clock2 の (d) で止まり、変更の記録 01 の判定も不合格で、試験を開かずに終わった。
#   5 つ目の系列は、変更記録を伴わない一発試験にする。事前登録の後に試験の候補が足りないと分かると INCONCLUSIVE で終わるので、
#   事前登録の前に、試験の候補が足りるかを数だけで確かめ、候補を選ぶ。
#
# 候補の作り方(この規則で並べた。数える前に決めた):
#   気象庁・地震調査研究推進本部の資料で、2004〜2025 年の陸の地殻内の浅い(気象庁の深さ 20 km 以内)Mj ≥ 6.0 の本震のうち、
#   次に当たらないもの全て。
#   - ARGUS で既に開いた系列とその周り: 熊本 2016(大分を含む)・鳥取県西部 2026・鳥取県中部 2016・大阪府北部 2018・
#     能登 2024 とその周り(能登半島 2007・2023 を含む)・岩手宮城内陸 2008・新潟県中越 2004・長野県北部 2014。
#     別のプロジェクトで Hi-net の波形を開いた長野県中部 2011(M5.4。もともと Mj < 6.0)。
#   - 東北地方太平洋沖地震の直後(2011 年 3〜4 月)に誘発された地震: 長野県北部(栄村)・静岡県東部・福島県浜通り。
#   - 震源が海か海岸で、箱の大半が海になるもの: 福岡県西方沖 2005・新潟県中越沖 2007・山形県沖 2019。
#   - 格子の深さ 0–30 km を超えるもの: 北海道胆振東部 2018(深さ約 37 km)。
#   残った 5 つ(気象庁の発表と CMT 解の値。本震の秒は確認済みで、本震の規則は分の単位のまま使う):
#   S: 島根県西部 2018 — 2018-04-09 01:32:30.8 JST、M6.1、深さ 12 km、35°11.0'N 132°35.2'E。西北西－東南東方向に圧力軸を持つ横ずれ断層型。
#   A: 淡路島付近 2013 — 2013-04-13 05:33:17.7 JST、M6.3、深さ 15 km、34°25.1'N 134°49.7'E。東西方向に圧力軸を持つ逆断層型。
#   T: 栃木県北部 2013 — 2013-02-25 16:23:53.5 JST、M6.3、深さ 3 km、36°52.4'N 139°24.7'E。横ずれ断層型。
#      地震調査研究推進本部は、群馬・栃木県境付近の活動が 2011 年以降高まっていたとしている。
#   R: 留萌支庁南部 2004 — 2004-12-14 14:56:10.5 JST、M6.1、深さ 9 km、44°04.6'N 141°41.9'E(気象庁の発震機構解の月報 mc200412)。
#      東南東－西北西圧縮の逆断層型。
#   I: 茨城県北部 2016 — 2016-12-28 21:38:49.0 JST、M6.3、深さ 11 km、36°43.2'N 140°34.4'E。東北東－西南西方向に張力軸を持つ正断層型。
#      気象庁は「平成 23 年(2011 年)東北地方太平洋沖地震の余震と考えられます」としている(余震域で発生)。CMT 解の重心は震源より
#      約 0.16° 北にあり、震源を中心にした箱(緯度 ±0.15°)は余震域の北の部分を外しうる(箱の規則は変えない)。
# 本震の規則(候補ごと。24_00 と同じ形): その日の、探す範囲の中の J の震源のうち Mj が最大の地震で、発生時刻が発表の分の 1 分 [hh:mm:00, hh:mm+1:00)
#   JST、Mj ≥ 発表の値 − 0.2、深さ 0–20 km、探す範囲(発表の震央を中心に緯度・経度 ±0.25°)の中、除く印(精度 M・8・9、
#   震源決定の印 N・F)が無い。合わなければ、その候補だけ「本震が規則に合わない」として数えない(他の候補は続ける)。
#
# 選び方の規則(実行する前に決めた。実行した後に変えない):
#   1. 選ぶ資格: 本震が規則に合い、R1 の後の試験の候補の見積もりが 40 以上。40 は基準 30 に決まった余裕 10 を足した値
#      (見積もりではない。長野 2014: カタログの見積もり 79 → キャッシュの R1 の後 79。大阪 2018: 56 → 55)。
#   2. 資格のある候補のうち、決まった順番 S → A → T → R → I で最初のものを選ぶ。数の多さでは比べない
#      (気象庁の震源一覧は 2016 年 4 月から小さい地震の載せ方が変わり、年によって数が違うため。数で比べると新しい年が有利になる)。
#      順番の理由: 新しい年ほど観測網が密で、試験済みの系列(2016・2018・2026)と同じ時代(S)。2013 の 2 つは、東北沖の影響が
#      述べられていない A を先にする(T は 2011 年以降の活動の高まりが述べられている)。R は 2004 年で北海道の観測網がまばら。
#      I は気象庁が東北沖の余震としているので最後。
#   3. どれも資格が無ければ、選ばない(別の候補を探す。その時はこの出力を開示する)。
#
# G-clock2 の (d) の作りに関わる数(記述。選び方には使わない):
#   Mj ≥ 1.5 の地震で、日本時間の 1 時間(24_04d と同じ区切り)ごとの地震の数を数え、1 つだけの時間・2 つ以上の時間の数を出す。
#   (i) R1 の前、(ii) R1 の見積もりの後(本番の 24_03h と同じく、本震は除かない)の 2 通り。全期間と、72 h の切れ目より後の地震だけ
#   (切れ目より後の地震を、その地震の時間で数える)の 2 通り。長野 2014 では、検測 20 以上の 155 時間のうち 92 時間が地震 1 つだった。
#
# 何をして、何をしないか:
#   する  : 気象庁の震源ファイル(h2003・h2004・h2005・h2012・h2013・h2015・h2016・h2017・h2018。期間と 365 日前の期間に要る年。
#           R は 2004-12-12〜2005-01-07、I は 2016-12-26〜2017-01-21 で年をまたぐ)を取り
#           (無ければ)、候補ごとに本震を規則で確かめ、箱と期間の中の地震を 24_00 と同じ規則で選び、数だけを出す。
#   しない: 震源の位置の一覧(CSV)を書かない。図を描かない。波形を取らない。どの手法の誤差も計算しない。
#           本震の 1 行(時刻・位置・深さ・Mj。発表と照らすため)のほかは位置を表示しない。
#
# 止める条件(STOP): 読み方の試験に失敗・ファイルが取れない・取ったものが zip として壊れている・96 バイトの形でない。
#   候補ごとの「本震の日に探す範囲の中の震源が無い」「本震が規則に合わない」「Mj ≥ 1.5 が 0」は、その候補だけを数えずに続ける。
#
# 限界: 正解も過去の地震も気象庁の震源。h2016・h2017・h2018 は気象庁の正誤表(2018-03-13・2021-04-15)で差し替えられている
#   (取ったファイルの SHA-256 で版を固定する)。手動と自動の震源が混ざる(印ごとの数を出す)。箱は本震の周りの決まった大きさで、
#   余震でない地震も入る(365 日前の数で記述する)。1 時間ごとの数はカタログでの見積もりで、本番の G-clock2 はキャッシュで P を測れた
#   地震で数える。
#
# Usage : (Mac、~/SWIFT で本人が実行)
#         uv run python src/25_00_fifth_sequence_feasibility_count.py 2>&1 | tee data/catalog/25_00_run.log
#         (震源ファイルが取れない時: 気象庁のページからブラウザで取って ~/SWIFT/data/catalog/jma_raw/ に置く)
#         (試験だけ: uv run python src/25_00_fifth_sequence_feasibility_count.py --selftest)
# Output: data/catalog/jma_raw/hYYYY.zip(取った時だけ)/ data/catalog/25_00_fifth_sequence_feasibility.json(数だけ)
# =============================================================================
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
import zipfile
from bisect import bisect_left, bisect_right
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

VERSION = "v1"
ROOT = Path(__file__).resolve().parent.parent
URL_HOSTS = ("https://www.data.jma.go.jp", "https://ds.data.jma.go.jp")   # 24_00 は 1 つ目で取れた。取れなければ 2 つ目
URL_PATH = "/eqev/data/bulletin/data/hypo/h{year}.zip"
REC_LEN = 96
# 候補(並びは選び方の規則 2 の順番)。area は本震を探す範囲(緯度の下・上、経度の下・上)
def _area(lat, lon, h=0.25):
    return (lat - h, lat + h, lon - h, lon + h)
CANDIDATES = [
    dict(key="S", name="Western Shimane 2018", name_ja="島根県西部 2018", minute=datetime(2018, 4, 9, 1, 32), mj_announced=6.1,
         area=_area(35 + 11.0 / 60, 132 + 35.2 / 60), tohoku_aftershock=False),
    dict(key="A", name="Awaji Island 2013", name_ja="淡路島付近 2013", minute=datetime(2013, 4, 13, 5, 33), mj_announced=6.3,
         area=_area(34 + 25.1 / 60, 134 + 49.7 / 60), tohoku_aftershock=False),
    dict(key="T", name="Northern Tochigi 2013", name_ja="栃木県北部 2013", minute=datetime(2013, 2, 25, 16, 23), mj_announced=6.3,
         area=_area(36 + 52.4 / 60, 139 + 24.7 / 60), tohoku_aftershock=False),
    dict(key="R", name="Southern Rumoi 2004", name_ja="留萌支庁南部 2004", minute=datetime(2004, 12, 14, 14, 56), mj_announced=6.1,
         area=_area(44 + 4.6 / 60, 141 + 41.9 / 60), tohoku_aftershock=False),
    dict(key="I", name="Northern Ibaraki 2016", name_ja="茨城県北部 2016", minute=datetime(2016, 12, 28, 21, 38), mj_announced=6.3,
         area=_area(36 + 43.2 / 60, 140 + 34.4 / 60), tohoku_aftershock=True),
]
ORDER = [c["key"] for c in CANDIDATES]
MAIN_MJ_TOL, MAIN_DEPTH = 0.2, (0.0, 20.0)
MIN_TEST = 30                                            # 21_04・21_20・24 の MIN_TEST と同じ(参考。判定には MIN_TEST_SELECT を使う)
MIN_TEST_SELECT = 40                                     # 選び方の規則 1(30 + 決まった余裕 10)
HALF_LAT, HALF_LON = 0.15, 0.175                         # 24_00 と同じ(0.30° × 0.35°)
DAYS_BEFORE, DAYS_AFTER = 2.0, 24.0                      # 24_00 と同じ
POOL_H, MIN_MAG, FRESH_MAX_MAG = 72.0, 1.5, 2.0          # 24_00 と同じ
PRE_S, POST_S = 15.0, 5.0                                # R1(24_00 と同じ窓)
PRE_US, POST_US = int(PRE_S * 1e6), int(POST_S * 1e6)
GRID_DEPTH_WARN_KM = 25.0
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
        if not c: sys.exit(f"[25_00] STOP: 読み方の試験に失敗: {msg}")
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
    print("[25_00] selftest: 震源レコードの読み方の試験に全て合格(21_04a と同じ試験)")



def load_year(year: int, rawd: Path):
    src = rawd / f"h{year}.zip"
    used_url = None
    if not src.exists():
        tmp = src.with_name(src.name + ".part")
        errs = []
        for host in URL_HOSTS:
            url = host + URL_PATH.format(year=year)
            print(f"[25_00] 取得: {url}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (ARGUS research)"})
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    data = r.read()
            except Exception as e:
                errs.append(f"{url}: {e}"); continue
            tmp.write_bytes(data)
            try:
                with zipfile.ZipFile(tmp) as z:
                    bad = z.testzip()
            except Exception as e:
                bad = f"zip でない({e})"
            if bad is not None:
                tmp.unlink(); errs.append(f"{url}: 壊れている({bad})"); continue
            used_url = url; tmp.replace(src); break             # 検査に通った時だけ正式な名前にする(壊れたファイルを残さない)
        if used_url is None:
            sys.exit(f"[25_00] STOP: h{year}.zip が取れない・壊れている({' / '.join(errs)})。ブラウザで取って {src} に置き、もう一度回す")
    sha = hashlib.sha256(src.read_bytes()).hexdigest()
    try:
        with zipfile.ZipFile(src) as z:
            mem = [m for m in z.namelist() if not m.endswith("/")]
            if not mem: sys.exit(f"[25_00] STOP: {src.name} の zip の中にファイルが無い")
            raw = b"\n".join(z.read(m) for m in mem)
    except (zipfile.BadZipFile, OSError) as e:
        sys.exit(f"[25_00] STOP: {src} が壊れた zip({e})。rm {src} をしてから、もう一度回す")
    recs, n_bad = read_records(raw)
    print(f"[25_00] 震源ファイル {src.name}(SHA-256 {sha[:12]}…、中身 {mem})  レコード {len(recs)}  96 バイトでない行 {n_bad}")
    if not recs or n_bad > 0.01 * len(recs): sys.exit(f"[25_00] STOP: {src.name} が 96 バイトのレコードの形でない(別のファイルの可能性)")
    H = [parse_hypo(r) for r in recs]
    J = [h for h in H if h["agency"] == "J" and h["origin_jst"] is not None]
    print(f"[25_00] {src.name}: 機関 J の震源 {len(J)}(他機関 {sum(1 for h in H if h['agency'] != 'J')}、時刻が読めない {sum(1 for h in H if h['origin_jst'] is None)})")
    return J, dict(file=src.name, sha256=sha, members=mem, n_records=len(recs), n_not_96_bytes=n_bad, n_agency_J=len(J),
                   downloaded_from=used_url)


def select_rows(J, box, t0, t1, ex=None):
    """24_00 と同じ範囲と除外。ex を渡せば除いた数を数える"""
    rows = []
    for h in J:
        if h["lat"] is None or h["lon"] is None:
            if ex is not None: ex["blank_lat_lon"] += 1
            continue
        if not (box[0] <= h["lat"] <= box[1] and box[2] <= h["lon"] <= box[3] and t0 <= h["origin_jst"] <= t1):
            if ex is not None: ex["outside_box_or_period"] += 1
            continue
        if h["precision"] in BAD_PRECISION:
            if ex is not None: ex["precision_M_8_9"] += 1
            continue
        if h["subsidiary"] in BAD_SUBSID:
            if ex is not None: ex["subsidiary_3_5"] += 1
            continue
        if h["det_flag"] in BAD_DETFLAG:
            if ex is not None: ex["det_flag_N_F"] += 1
            continue
        if h["mag"] is None or h["depth_km"] is None:
            if ex is not None: ex["blank_mag_or_depth"] += 1
            continue
        rows.append(h)
    rows.sort(key=lambda h: h["origin_jst"])
    return rows


def hour_counts(events, cut):
    """Mj ≥ 1.5 の地震の、日本時間の 1 時間(24_04d と同じ区切り)ごとの数。全期間と、切れ目より後の地震だけ"""
    key = lambda h: h["origin_jst"].strftime("%Y-%m-%d %H")
    allh = Counter(key(h) for h in events)
    afth = Counter(key(h) for h in events if h["origin_jst"] > cut)
    return dict(hours=len(allh), hours_one=sum(1 for v in allh.values() if v == 1), hours_two_or_more=sum(1 for v in allh.values() if v >= 2),
                after_cut_hours=len(afth), after_cut_hours_one=sum(1 for v in afth.values() if v == 1),
                after_cut_hours_two_or_more=sum(1 for v in afth.values() if v >= 2))


def count_candidate(c: dict, J: list, Jprev: list) -> dict:
    """候補 1 つの数え上げ(24_00 の main の本震より後と同じ計算)。位置の一覧は返さない"""
    tag = f"[25_00] {c['key']} {c['name_ja']}"
    out = dict(key=c["key"], name=c["name"], tohoku_aftershock=c["tohoku_aftershock"], eligible=False, reason="")
    ar = c["area"]                                        # 探す範囲の中だけ(同じ日に範囲の外でもっと大きい地震があっても本震を取り違えない)
    day = [h for h in J if h["origin_jst"].date() == c["minute"].date() and h["mag"] is not None
           and h["lat"] is not None and h["lon"] is not None and ar[0] <= h["lat"] <= ar[1] and ar[2] <= h["lon"] <= ar[3]]
    if not day:
        out["reason"] = "no hypocentre in the search area on the mainshock day"; print(f"{tag}: 本震の日に探す範囲の中の震源が無い → 数えない"); return out
    m = max(day, key=lambda h: h["mag"])
    win = (c["minute"], c["minute"] + timedelta(minutes=1))
    in_win = win[0] <= m["origin_jst"] < win[1]
    print(f"{tag}: 本震 {fmt_time(m['origin_jst'])} JST  {m['lat']:.4f}N {m['lon']:.4f}E  深さ {m['depth_km']} km  M{m['mag']}{m['mag_type']}  "
          f"精度 {m['precision']}  印 '{m['det_flag']}'  (発表の 1 分 {win[0]:%H:%M:%S}〜{win[1]:%H:%M:%S} JST の中か: {in_win})")
    ok = (in_win and m["mag"] >= c["mj_announced"] - MAIN_MJ_TOL - 1e-9 and m["depth_km"] is not None
          and MAIN_DEPTH[0] <= m["depth_km"] <= MAIN_DEPTH[1] and ar[0] <= m["lat"] <= ar[1] and ar[2] <= m["lon"] <= ar[3]
          and m["det_flag"] not in BAD_DETFLAG and m["precision"] not in BAD_PRECISION)
    out["mainshock"] = dict(origin_jst=fmt_time(m["origin_jst"]), lat=m["lat"], lon=m["lon"], depth_km=m["depth_km"], mj=m["mag"],
                            mag_type=m["mag_type"], precision=m["precision"], det_flag=m["det_flag"])
    if not ok:
        out["reason"] = "mainshock does not match the rule"; print(f"{tag}: 本震が規則に合わない → 数えない(この行を貼って相談)"); return out
    box = [round(m["lat"] - HALF_LAT, 4), round(m["lat"] + HALF_LAT, 4), round(m["lon"] - HALF_LON, 4), round(m["lon"] + HALF_LON, 4)]
    t0, t1 = m["origin_jst"] - timedelta(days=DAYS_BEFORE), m["origin_jst"] + timedelta(days=DAYS_AFTER)
    cut = m["origin_jst"] + timedelta(hours=POOL_H)
    ex = dict(blank_lat_lon=0, outside_box_or_period=0, precision_M_8_9=0, subsidiary_3_5=0, det_flag_N_F=0, blank_mag_or_depth=0)
    rows = select_rows(J, box, t0, t1, ex)
    if not any(h["mag"] >= MIN_MAG - 1e-9 for h in rows):
        out["reason"] = "no Mj >= 1.5 in the box and period"; print(f"{tag}: 箱の中・期間内の Mj ≥ 1.5 が 0 → 数えない"); return out

    def is_cand(h):
        return h["origin_jst"] > cut and MIN_MAG - 1e-9 <= h["mag"] < FRESH_MAX_MAG - 1e-9
    ts = [(h["origin_jst"] - m["origin_jst"]) // timedelta(microseconds=1) for h in rows]
    def r1_hit(i):                                        # 24_00 と同じ: 窓 [−15 s, +5 s] に自分以外の地震が 1 つ以上
        return bisect_right(ts, ts[i] + POST_US) - bisect_left(ts, ts[i] - PRE_US) > 1
    cand_idx = [i for i, h in enumerate(rows) if is_cand(h)]
    removed = [i for i in cand_idx if r1_hit(i)]
    rem = set(removed)
    n_cand, n_after = len(cand_idx), len(cand_idx) - len(removed)
    per_day = Counter(int((rows[i]["origin_jst"] - m["origin_jst"]).total_seconds() // 86400) for i in cand_idx if i not in rem)
    mag15 = [h for h in rows if h["mag"] >= MIN_MAG - 1e-9]
    mag15_r1 = [h for i, h in enumerate(rows) if h["mag"] >= MIN_MAG - 1e-9 and (h is m or not r1_hit(i))]   # 本震は除かない(24_03h の R2)
    n = dict(all=len(rows), mj_ge_1p5=len(mag15),
             mj_ge_2p0=sum(1 for h in rows if h["mag"] >= FRESH_MAX_MAG - 1e-9),
             pool_mj_ge_1p5=sum(1 for h in mag15 if h["origin_jst"] <= cut),
             test_candidates_1p5_to_2p0_after_72h=n_cand,
             test_candidates_after_R1_estimate=n_after,
             removed_by_R1_estimate=len(removed),
             library_only_mj_ge_2p0_after_72h=sum(1 for h in rows if h["origin_jst"] > cut and h["mag"] >= FRESH_MAX_MAG - 1e-9),
             mj_ge_1p5_deeper_than_25km=sum(1 for h in mag15 if h["depth_km"] > GRID_DEPTH_WARN_KM),
             test_candidates_deeper_than_25km=sum(1 for i in cand_idx if rows[i]["depth_km"] > GRID_DEPTH_WARN_KM),
             mj_ge_1p5_after_R1_estimate=len(mag15_r1))
    hc = dict(before_R1=hour_counts(mag15, cut), after_R1_estimate=hour_counts(mag15_r1, cut))
    # 365 日前の同じ箱・同じ長さの期間(余震でない地震の多さの記述)
    p0, p1 = t0 - timedelta(days=365), t1 - timedelta(days=365)
    prev = select_rows(Jprev, box, p0, p1)
    bg = dict(period_jst=[fmt_time(p0), fmt_time(p1)], all=len(prev), mj_ge_1p5=sum(1 for h in prev if h["mag"] >= MIN_MAG - 1e-9))
    flags_15 = dict(Counter(h["det_flag"] or "_" for h in mag15))
    flags_c = dict(Counter(rows[i]["det_flag"] or "_" for i in cand_idx if i not in rem))
    out.update(box=box, period_jst=[fmt_time(t0), fmt_time(t1)], pool_cut_jst=fmt_time(cut), counts=n, hour_counts_mj_ge_1p5=hc,
               one_year_earlier=bg, excluded=ex, det_flag_counts=dict(mj_ge_1p5=flags_15, test_candidates_after_R1=flags_c),
               test_candidates_after_R1_per_day_since_mainshock={str(k): per_day[k] for k in sorted(per_day)},
               eligible=bool(n_after >= MIN_TEST_SELECT), reason=("" if n_after >= MIN_TEST_SELECT else f"fewer than {MIN_TEST_SELECT} test candidates after R1"))
    print(f"{tag}: 箱 {box}  期間 {fmt_time(t0)} 〜 {fmt_time(t1)} JST  pool の切れ目 {fmt_time(cut)} JST")
    print(f"{tag}: 除いた数 {ex}")
    print(f"{tag}: 数 {n}")
    print(f"{tag}: 1 時間ごと(Mj ≥ 1.5、R1 の前) {hc['before_R1']}")
    print(f"{tag}: 1 時間ごと(Mj ≥ 1.5、R1 の見積もりの後) {hc['after_R1_estimate']}")
    print(f"{tag}: 365 日前の同じ箱・同じ長さの期間 {bg}")
    print(f"{tag}: 震源決定の印 Mj ≥ 1.5 {flags_15}  R1 の後の試験の候補 {flags_c}")
    print(f"{tag}: R1 の後の試験の候補の日ごとの数(本震からの日) {out['test_candidates_after_R1_per_day_since_mainshock']}")
    print(f"{tag}: R1 の後の試験の候補 {n_after}(資格の基準 {MIN_TEST_SELECT})→ {'資格あり' if out['eligible'] else '資格なし'}")
    return out


def select(results: list):
    """選び方の規則(冒頭の 1〜3。実行する前に決めた): 資格のある候補のうち、決まった順番で最初のもの"""
    by = {r["key"]: r for r in results}
    for k in ORDER:
        if k in by and by[k]["eligible"]:
            return k, f"rule 2: first eligible candidate in the fixed order {' > '.join(ORDER)}"
    return None, "rule 3: no candidate is eligible"


def selftest_select():
    def r(k, n, el):
        return dict(key=k, eligible=el, counts=dict(test_candidates_after_R1_estimate=n))
    def check(c, msg):
        if not c: sys.exit(f"[25_00] STOP: 選び方の試験に失敗: {msg}")
    allok = [r(k, 50, True) for k in ORDER]
    check(select(allok)[0] == "S", "全て資格あり → S")
    check(select([r("S", 39, False), r("A", 40, True), r("T", 500, True), r("R", 50, True), r("I", 900, True)])[0] == "A",
          "S に資格が無い → A(数の多さでは比べない)")
    check(select([r("S", 1, False), r("A", 1, False), r("T", 1, False), r("R", 41, True), r("I", 900, True)])[0] == "R", "S・A・T に資格が無い → R")
    check(select([r(k, 1, False) for k in ORDER[:-1]] + [r("I", 40, True)])[0] == "I", "I だけ資格あり → I")
    check(select([r(k, 39, False) for k in ORDER])[0] is None, "どれも資格が無い")
    def hc_check():
        T = datetime(2018, 4, 12, 1, 32, 30)              # 切れ目
        ev = [dict(origin_jst=T - timedelta(minutes=10)), dict(origin_jst=T), dict(origin_jst=T + timedelta(minutes=10)),
              dict(origin_jst=T + timedelta(hours=2)), dict(origin_jst=T + timedelta(hours=2, minutes=5))]
        h = hour_counts(ev, T)
        return (h["hours"], h["hours_one"], h["hours_two_or_more"], h["after_cut_hours"], h["after_cut_hours_one"], h["after_cut_hours_two_or_more"])
    check(hc_check() == (2, 0, 2, 2, 1, 1), f"1 時間ごとの数 {hc_check()}")
    print("[25_00] selftest: 選び方の規則(5 例)と 1 時間ごとの数え方(1 例)の試験に合格")


def main():
    ap = argparse.ArgumentParser(description="25_00: 5 つ目の系列の候補の数だけを数え、先に決めた規則で選ぶ(事前登録の前)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    selftest(); selftest_select()
    if a.selftest: return
    CAT = ROOT / "data" / "catalog"; RAWD = CAT / "jma_raw"
    for d in (CAT, RAWD): d.mkdir(parents=True, exist_ok=True)
    files, results, cache = {}, [], {}
    def events(y0, y1):
        J = []
        for y in range(y0, y1 + 1):                       # 期間が年をまたぐ候補(I: 2016-12-26〜2017-01-21)は両方の年を読む
            if y not in cache:
                cache[y], files[str(y)] = load_year(y, RAWD)
            J.extend(cache[y])
        return J
    for c in CANDIDATES:
        y0 = (c["minute"] - timedelta(days=DAYS_BEFORE)).year
        y1 = (c["minute"] + timedelta(days=DAYS_AFTER)).year
        J, Jprev = events(y0, y1), events(y0 - 1, y1 - 1)
        print()
        results.append(count_candidate(c, J, Jprev))
    key, why = select(results)
    print(f"\n[25_00] 選んだ候補: {key if key else 'なし'}({why})")
    summ = dict(script="25_00_fifth_sequence_feasibility_count.py", version=VERSION,
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), source_files=files,
                candidates=results, order=ORDER, selected=key, selection_reason=why,
                rules=dict(half_lat_deg=HALF_LAT, half_lon_deg=HALF_LON, days_before=DAYS_BEFORE, days_after=DAYS_AFTER,
                           pool_h=POOL_H, min_mag=MIN_MAG, fresh_max_mag=FRESH_MAX_MAG, r1_window_s=[-PRE_S, POST_S],
                           min_test=MIN_TEST, min_test_select=MIN_TEST_SELECT, main_mj_tol=MAIN_MJ_TOL, main_depth_km=list(MAIN_DEPTH),
                           main_search_area={c["key"]: list(c["area"]) for c in CANDIDATES}, bad_precision=sorted(BAD_PRECISION),
                           bad_subsidiary=sorted(BAD_SUBSID), bad_det_flag=sorted(BAD_DETFLAG)),
                note="counts only, written before any preregistration of the fifth-sequence test; no location list except the mainshock line, no waveform, no method error")
    out = CAT / "25_00_fifth_sequence_feasibility.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(summ, f, indent=1, ensure_ascii=False)
    print(f"[25_00] 出力: {out.relative_to(ROOT)}(数だけ。位置の一覧は書いていない)")


if __name__ == "__main__":
    main()
