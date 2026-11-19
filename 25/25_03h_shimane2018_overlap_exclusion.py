#!/usr/bin/env python3
# =============================================================================
# Script : 25_03h_shimane2018_overlap_exclusion.py  (v1)
#          [島根県西部 2018 のキャッシュ(25_03 の本番)から、「発生の 15 s 前〜5 s 後に別の地震がある地震」を除いたキャッシュを作る(規則 R1)。
#           使うのは気象庁の震源一覧の発生時刻と Mj だけ。震源の位置(正解)・波形・検測の残り・位置の計算は一切使わない]
# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)。大阪(21_20)で変更の記録 04 として後から足し、24 で最初から
#          規則に入れた R1 を、この系列でも島根の波形を開く前に、事前登録の規則として最初から入れる
# 派生元 : 24_03h_nagano2014_overlap_exclusion.py v1(SHA-256 e2700654a13f0514f133f01f8255d8b546107716ec43990cc648a7392e42dd0d。事前登録 24 で凍結)。
#          規則 R1〜R4・自分の行の見つけ方(25_03 = 24_03 = 21_20c と同じ読み方の時刻(0.1 s で切り捨て)と Mj が一致する、ただ 1 つの行)・
#          窓 [−15.0 s, +5.0 s]・除かない地震(本震と、25_02 の G-clock の地震)・止める条件は 24_03h v1 と同じ。変えたのは次だけ(DIFF_LOG_25.md):
#          (1) 本震の想定 MAIN_UTC = 2018-04-08 16:32:30.81 UTC(25_00 の表示の 2018-04-09 01:32:30.81 JST、± 60 s、Mj ≥ 6.0)
#          (2) 出力の名前(tottori_parsed_realpick_shimane2018_m15_r1.pt・data/25_03h_overlap_exclusion.json)、表示 [25_03h]、記録の文
#
# 規則(事前登録 25 の 3 節。24 と同じ):
#   R1. 気象庁の震源一覧(jma_shimane2018.csv、25_01 の出力、全ての規模)で、キャッシュの地震の自分の行の発生時刻(0.01 s)から
#       dt = [−15.0 s, +5.0 s] の範囲に、自分の行以外の地震が 1 つでもあれば、その地震を除く。
#   R2. 除かないもの: 本震(キャッシュで Mj 最大)と、25_02 の G-clock の地震(25_04d の (e) に要る)。このどれかが試験の候補なら止める。
#   R3. 除いた後の試験の候補が 30 未満なら、キャッシュを書かずに止める(既存の MIN_TEST = 30。25_05 は回さず INCONCLUSIVE と報告する)。
#   R4. キャッシュの地震の並びと中身(辞書)は 1 字も変えず、除く地震を抜くだけ。
#   25_00 の見積もり(カタログだけ): 試験の候補 41 → R1 の後 41(除く 0)。キャッシュでは P を測れない地震の分だけ少なくなりうる。
#
# 止める条件(STOP): キャッシュ・震源一覧・報告が無い・キャッシュの地震が震源一覧に見つからないか 2 行以上ある・本震が想定と違う・
#   R2・R3(R2・R3 で止まった時も、記録の JSON は書く)。
#
# 出力(--out の下):
#   data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt  … 除いた後のキャッシュ(25_04d・25_04e・24_07・25_05・25_06f・25_06g に渡す)
#   data/25_03h_overlap_exclusion.json                                … 規則・入力と出力の SHA-256・数・除いた地震の一覧
#
# Usage(Colab。ノート 25_shimane2018_colab.ipynb の セル N12):
#   !python /content/drive/MyDrive/ARGUS/src/25_03h_shimane2018_overlap_exclusion.py \
#       --cache /content/ARGUS_shimane2018/data/tottori_processed/tottori_parsed_realpick_shimane2018_m15.pt \
#       --catalog /content/drive/MyDrive/ARGUS/data/catalog/jma_shimane2018.csv \
#       --report /content/drive/MyDrive/ARGUS_shimane2018/data/25_02_report.json --out /content/ARGUS_shimane2018
# =============================================================================
import argparse, csv, hashlib, json, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import torch

VERSION = "v1"
TAG = "[25_03h]"
PRE_S, POST_S = 15.0, 5.0                                # R1(21_20g と同じ窓)
POOL_H, FRESH_MAX_MAG, MIN_TEST = 72.0, 2.0, 30            # 21_20 v1 と同じ値
MAIN_UTC = datetime(2018, 4, 8, 16, 32, 30, 810000)      # 25: 25_00 の表示の 2018-04-09 01:32:30.81 JST(± 60 s)
GCLOCK_MATCH_S = 1.5                                       # 21_20d v1 の (e) と同じ探し方
OUT_CACHE = "data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt"
OUT_JSON = "data/25_03h_overlap_exclusion.json"

ap = argparse.ArgumentParser(description="25_03h: 発生の近くに別の地震がある地震を除いたキャッシュを作る(事前登録 25 の R1)")
ap.add_argument("--cache", required=True, help="25_03 の本番のキャッシュ(tottori_parsed_realpick_shimane2018_m15.pt)")
ap.add_argument("--catalog", required=True, help="jma_shimane2018.csv(25_01 の出力、全ての規模、時刻は日本時間)")
ap.add_argument("--report", required=True, help="25_02 の報告(data/25_02_report.json。G-clock の地震を読む)")
ap.add_argument("--out", required=True, help="出力の根(25_04d・25_04e の --base にもこの場所を使う)")
a = ap.parse_args()


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def utc_naive(o):
    """キャッシュの origin_time(UTC の文字列か datetime)を、タイムゾーンなしの UTC の datetime にする(マイクロ秒まで)"""
    s = str(o).strip().replace("T", " ").replace("Z", "")
    if "+" in s[10:]: s = s[:10] + s[10:].split("+")[0]
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try: return datetime.strptime(s[:26], fmt)
        except ValueError: pass
    sys.exit(f"{TAG} STOP: origin_time {o!r} を時刻として読めない")


SELF_SHA = sha256(Path(__file__))
print(f"{TAG} 本スクリプト {VERSION} SHA-256 {SELF_SHA}(結果を貼る時にこの行も貼ってください)")

# ---- 1. 入力の確かめ
cp, catp, rp = Path(a.cache), Path(a.catalog), Path(a.report)
for p in (cp, catp, rp):
    if not p.exists(): sys.exit(f"{TAG} STOP: {p} が無い")
CACHE_SHA = sha256(cp)
print(f"{TAG} 入力のキャッシュ {cp.name}  SHA-256 {CACHE_SHA}")
CAT_SHA = sha256(catp)
print(f"{TAG} 震源一覧 {catp.name}  SHA-256 {CAT_SHA}")

EV = torch.load(cp, map_location="cpu", weights_only=False)
if not isinstance(EV, list) or not EV: sys.exit(f"{TAG} STOP: キャッシュが地震の並び(list)でない、または空")
for e in EV:
    miss = [k for k in ("origin_time", "mw", "n_real_stations") if k not in e]
    if miss: sys.exit(f"{TAG} STOP: キャッシュの地震に {miss} が無い")
NE = len(EV)
OT_UTC = [utc_naive(e["origin_time"]) for e in EV]
OT_JST = [t + timedelta(hours=9) for t in OT_UTC]
MAG = np.array([float(e["mw"]) for e in EV])

CAT = []
with open(catp, newline="") as f:
    for row in csv.DictReader(f):
        ts = row["time"].strip()
        t = datetime.strptime(ts[:22], "%Y-%m-%d %H:%M:%S.%f" if "." in ts else "%Y-%m-%d %H:%M:%S")
        t21 = datetime.strptime(ts[:21].ljust(21, "0"), "%Y-%m-%d %H:%M:%S.%f")   # 25_03(= 21_20c)と同じ読み方(0.1 s で切り捨て)
        mg = row.get("mag", "").strip()
        try: mjv = float(mg) if mg else None
        except ValueError: mjv = None
        CAT.append(dict(t=t, t21=t21, mj=mjv))
CAT.sort(key=lambda c: c["t"])
CT = np.array([(c["t"] - datetime(1970, 1, 1)).total_seconds() for c in CAT])
SELF_INDEX = {}                                            # (21_20c の読み方の時刻, Mj) -> 震源一覧の行の番号
for k, c in enumerate(CAT):
    if c["mj"] is not None: SELF_INDEX.setdefault((c["t21"], round(c["mj"], 3)), []).append(k)
print(f"{TAG} キャッシュ {NE} 地震・震源一覧 {len(CAT)} 行(全ての規模)")

# ---- 2. 本震(21_20 v1・25_05 と同じ: Mj 最大で、Mj ≥ 6.0・MAIN_UTC ± 60 s)
im = int(np.argmax(MAG))
if MAG[im] < 6.0 or abs((OT_UTC[im] - MAIN_UTC).total_seconds()) > 60:
    sys.exit(f"{TAG} STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT_UTC[im]} UTC")
CUT = OT_UTC[im] + timedelta(hours=POOL_H)
IS_TEST = np.array([(t > CUT) and (m < FRESH_MAX_MAG - 1e-6) for t, m in zip(OT_UTC, MAG)])
print(f"{TAG} 本震 {OT_JST[im]:%Y-%m-%d %H:%M:%S.%f} JST Mj {MAG[im]:.1f}  試験の候補(本震 + {POOL_H:.0f} h より後の Mj < {FRESH_MAX_MAG}){int(IS_TEST.sum())}")

# ---- 3. R1: 発生の [−15 s, +5 s] に別の地震があるか(発生時刻だけを使う)
#   キャッシュの発生時刻は 21_20c が震源一覧の時刻を 0.1 s で切り捨てたもの(21_20c の 321 行)。そのため、自分自身の行は時刻の差の
#   許容では探さず、「21_20c と同じ読み方の時刻と Mj が一致する行」として 1 つに決め、その行の時刻(0.01 s)から測り、その行だけを除いて数える。
NB, n_noself, n_multi = [], 0, 0
for ie in range(NE):
    key = (OT_JST[ie].replace(microsecond=(OT_JST[ie].microsecond // 100000) * 100000), round(float(MAG[ie]), 3))
    rows_ = SELF_INDEX.get(key, [])
    if len(rows_) != 1:
        if not rows_: n_noself += 1
        else: n_multi += 1
        NB.append(None); continue
    ks = rows_[0]; t0 = CT[ks]
    lo, hi = np.searchsorted(CT, t0 - PRE_S - 1e-6, "left"), np.searchsorted(CT, t0 + POST_S + 1e-6, "right")
    NB.append([dict(dt_s=round(float(CT[k] - t0), 2), mj=CAT[k]["mj"]) for k in range(lo, hi)
               if k != ks and -PRE_S - 1e-9 <= CT[k] - t0 <= POST_S + 1e-9])
if n_noself or n_multi:
    sys.exit(f"{TAG} STOP: キャッシュの地震のうち、震源一覧に自分の行が見つからないもの {n_noself}・2 行以上あるもの {n_multi}"
             "(25_03 = 21_20c と同じ読み方の時刻と Mj で照合)")
print(f"{TAG} G-match PASS: キャッシュの {NE} 地震とも、震源一覧に自分の行がちょうど 1 つある(25_03 = 21_20c と同じ読み方の時刻と Mj で照合)")

# ---- 4. R2: 除かない地震(本震と G-clock の地震。本震は G-clock の 4 地震の 1 つ)
rep = json.load(open(rp))
try: gc = rep["gates"]["clock"]
except (KeyError, TypeError): sys.exit(f"{TAG} STOP: {rp.name} に gates.clock が無い")
KEEP = {im: "mainshock"}
for c in gc:
    t = datetime.strptime(str(c["origin_jst"]).replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
    EVJ19 = [x.replace(microsecond=0) for x in OT_JST]     # 21_20d v1・25_04d の jst() と同じ(秒で切り捨て)
    j = min(range(NE), key=lambda i: abs((EVJ19[i] - t).total_seconds()))
    if abs((EVJ19[j] - t).total_seconds()) > GCLOCK_MATCH_S:
        print(f"{TAG} 注意: G-clock の地震 {c['origin_jst']} がキャッシュに無い(25_04d の (e) がその扱いを決める。ここでは何もしない)"); continue
    KEEP.setdefault(j, "G-clock event")
for j, why in KEEP.items():
    if IS_TEST[j]:
        out0 = Path(a.out) / "data"; out0.mkdir(parents=True, exist_ok=True)
        json.dump(dict(script="25_03h_shimane2018_overlap_exclusion.py", version=VERSION, script_sha256=SELF_SHA, input_cache_sha256=CACHE_SHA,
                       verdict="STOP-R2: an exempt event (mainshock or G-clock event) is a test candidate",
                       event=dict(origin_jst=f"{OT_JST[j]:%Y-%m-%d %H:%M:%S.%f}"[:22], mj=float(MAG[j]), why=why)),
                  open(out0 / "25_03h_overlap_exclusion.json", "w"), indent=1, ensure_ascii=False)
        sys.exit(f"{TAG} STOP(R2): 除かない地震({why}、{OT_JST[j]:%Y-%m-%d %H:%M:%S} JST Mj {MAG[j]:.1f})が試験の候補。記録: {out0 / '25_03h_overlap_exclusion.json'}")
EXCL = [ie for ie in range(NE) if NB[ie] and ie not in KEEP]
KEPT_WITH_NB = [ie for ie in KEEP if NB[ie]]
EXS = set(EXCL)

n_test0, n_test1 = int(IS_TEST.sum()), int(sum(IS_TEST[ie] for ie in range(NE) if ie not in EXS))
n_pool0 = int((~IS_TEST).sum()); n_pool1 = n_pool0 - int(sum(not IS_TEST[ie] for ie in EXCL))
print(f"{TAG} R1: 発生の [−{PRE_S:.0f} s, +{POST_S:.0f} s] に別の地震がある地震 {sum(1 for x in NB if x)} / {NE}")
print(f"{TAG} R2: 除かない地震 {len(KEEP)}(本震と G-clock の地震)。そのうち R1 に当たるもの {len(KEPT_WITH_NB)}")
for j in sorted(KEEP):
    print(f"      {OT_JST[j]:%Y-%m-%d %H:%M:%S.%f} JST Mj {MAG[j]:.1f}  {KEEP[j]}  近くの別の地震 {len(NB[j])}")
print(f"{TAG} 除く地震 {len(EXCL)}(試験の候補から {n_test0 - n_test1}・それ以外から {n_pool0 - n_pool1})")
print(f"{TAG} 除いた後: 地震 {NE - len(EXCL)}・試験の候補 {n_test1}(前 {n_test0})・それ以外 {n_pool1}(前 {n_pool0})")

out = Path(a.out); (out / "data" / "tottori_processed").mkdir(parents=True, exist_ok=True)
REC = dict(script="25_03h_shimane2018_overlap_exclusion.py", version=VERSION, script_sha256=SELF_SHA,
           purpose="preregistration 25 rule R1 (same as preregistration 24; from 21_20 amendment 04): remove events with another catalogue event within [-15 s, +5 s] of origin; origin times and Mj only; no location, waveform or residual used",
           rule=dict(pre_s=PRE_S, post_s=POST_S, self_row="catalogue row with the same 25_03 (= 21_20c) parsed time (0.1 s) and Mj; dt measured from its 0.01 s time", keep="mainshock and the 25_02 G-clock events",
                     pool_h=POOL_H, fresh_max_mag=FRESH_MAX_MAG, min_test=MIN_TEST),
           input=dict(cache=str(cp), cache_sha256=CACHE_SHA, catalog=str(catp), catalog_sha256=CAT_SHA, report=str(rp), report_sha256=sha256(rp)),
           counts=dict(n_events=NE, n_with_neighbour=int(sum(1 for x in NB if x)), n_keep_exempt=len(KEEP), n_keep_exempt_with_neighbour=len(KEPT_WITH_NB),
                       n_excluded=len(EXCL), n_test_before=n_test0, n_test_after=n_test1, n_other_before=n_pool0, n_other_after=n_pool1),
           excluded=[dict(origin_jst=f"{OT_JST[ie]:%Y-%m-%d %H:%M:%S.%f}"[:22], mj=float(MAG[ie]), test_candidate=bool(IS_TEST[ie]), neighbours=NB[ie])
                     for ie in EXCL],
           kept_exempt=[dict(origin_jst=f"{OT_JST[j]:%Y-%m-%d %H:%M:%S.%f}"[:22], mj=float(MAG[j]), why=KEEP[j], neighbours=NB[j]) for j in sorted(KEEP)],
           )

# ---- 5. R3: 試験の候補が 30 未満なら書かずに止める
if n_test1 < MIN_TEST:
    REC.update(output=None, verdict="STOP-R3: fewer than 30 test candidates after exclusion; 25_05 is not run and the result is reported as INCONCLUSIVE")
    json.dump(REC, open(out / OUT_JSON, "w"), indent=1, ensure_ascii=False)
    sys.exit(f"{TAG} STOP(R3): 除いた後の試験の候補が {n_test1}({MIN_TEST} 未満)。キャッシュは書かない。記録: {out / OUT_JSON}")

# ---- 6. R4: 並びと中身は変えず、除く地震を抜いて書く
KEPT = [EV[ie] for ie in range(NE) if ie not in EXS]
op = out / OUT_CACHE
torch.save(KEPT, op)
OUT_SHA = sha256(op)
chk = torch.load(op, map_location="cpu", weights_only=False)
if len(chk) != len(KEPT) or [str(e["origin_time"]) for e in chk] != [str(e["origin_time"]) for e in KEPT]:
    sys.exit(f"{TAG} STOP: 書いたキャッシュを読み直すと地震の並びが違う")
REC.update(output=dict(cache=str(op), cache_sha256=OUT_SHA, n_events=len(KEPT)), verdict="WRITTEN")
json.dump(REC, open(out / OUT_JSON, "w"), indent=1, ensure_ascii=False)
print(f"{TAG} 出力: {op}  {len(KEPT)} 地震  SHA-256 {OUT_SHA}")
print(f"{TAG} 記録: {out / OUT_JSON}")
print(f"{TAG} 次: 25_04d・25_04e を --base {out} --cache {OUT_CACHE} で回す(この SHA-256 は 25_05 が opened.json に書き、24_07 の記録と照らす)")
