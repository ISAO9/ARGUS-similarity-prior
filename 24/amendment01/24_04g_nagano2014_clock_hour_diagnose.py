#!/usr/bin/env python3
# =============================================================================
# Script : 24_04g_nagano2014_clock_hour_diagnose.py  (v1)
#          [読むだけの記述: 長野県北部 2014 の G-clock2 (d)「1 時間ごと」で外れた時間に何が起きたかを、地震ごと・局ごとの P の残り、
#           気象庁の震源一覧(箱の中の全ての規模と、h2014 の日本全体)、キャッシュの波形で調べる]
# Project: ARGUS(新生)— 事前登録 24。24_04d の (d) が FAIL し(2014-12-01 07 時台、ずれ 0.672 s)、事前登録 5.3 節の 2 により試験は
#          開かずに止めた。このスクリプトはその原因を調べる記述だけで、止める判断も、規則も、キャッシュも変えない。
#          派生元: 21_20g_osaka2018_clock_hour_diagnose.py v1(大阪で同じ (d) の FAIL を調べたもの)。
#
# 試験を開かないための決まり(この版で守ること):
#   - 位置の計算(M5・M6r・C1〜C4・L3/L4)も、どの方法の誤差も一切出さない。読むのは P の時刻・震源一覧・キャッシュの波形だけ。
#   - 気象庁の震源の値のうち、表示するのは「Mj・深さ・本震からの震央距離」だけにする。緯度・経度は表示も保存もしない
#     (試験の地震の正解の位置の一覧を作らないため)。24_04d と同じく、残りの計算には震源距離(キャッシュの dist_km)を使う。
#   - 外れた時間の地震が試験の候補(本震 + 72 h より後の 1.5 ≤ Mj < 2.0)かどうかを表示する(後の判断で開示するため)。
#
# なぜ必要か(仮説。まだ確かめていない):
#   24_04d の (d) で外れた 5 時間の検測は、どれも 24 個だった(1 地震の局は最大 24)。1 時間に地震が 1 つだけなら、(d) は時計ではなく
#   その 1 地震の残りの中央値を見ていることになる。そのずれは、気象庁の発生時刻・深さの誤差、箱の外やカタログに無い地震の重なり、
#   検測の取り違えでも生じる。一方、24_04e の表では、80 km 以内の局のずれは規模によらずそろっていた。
#   区別の手がかり:
#     H-event(地震ごとの食い違い): 外れた地震の中で、全ての局が「その局のふだんの残り」から同じ量だけずれる(発生時刻の食い違い)、
#       または距離で変わる(別の場所の地震の P を拾った)。前後の時間の地震は正常。
#     H-clock(その時間の時計のずれ): Hi-net の局は局ごとに GPS で時刻を合わせるので、その時間の全ての局が同時に同じ量ずれることは
#       考えにくいが、もしそうなら、同じ時間の他の地震(あれば)や、前後数時間の地震も同じだけずれるはず。
#     (d) の作りの問題: 検測 20 以上の時間のうち、地震が 1 つしかない時間の割合と、その時間のずれの分布。
#
# 何をするか:
#   1. キャッシュ(24_03h の出力、R1 の後)の全ての地震・局で、24_04d と同じ式の残り r = tp_times − dist_km / 6.0 を出す
#      (p_fallback = 0 の検測だけ)。全体の中央値が 24_04d の JSON の値と 1e-6 s 以内で同じことを確かめる(違えば止める)。
#   2. 時間ごとの地震の数: 24_04d と同じ「日本時間の 1 時間・検測 20 以上」の時間について、その時間の地震の数を数え、
#      地震が 1 つの時間・2 つ以上の時間それぞれの |ずれ| の分布を表示する。
#   3. 対象の時間(既定: 24_04d の JSON の、ずれの大きい順の 5 時間。--hours で指定もできる)の地震ごとに:
#      Mj・深さ・本震からの震央距離・役割(pool / 試験の候補 / それ以外)・検測の数・ずれ・四分位幅・残りと距離の傾き、
#      局ごとの「残り − その局の全期間の中央値」(局のふだんのずれを除いた量)の中央値と四分位幅、
#      前後の地震(時刻の順で 1 つ前・1 つ後の、P を測った地震)のずれ。
#   4. 震源一覧: (i) 24_01 の出力(箱の中・全ての規模)で、発生の 60 s 前〜30 s 後の別の地震。(ii) h2014 の日本全体(機関 J)で、
#      発生の 60 s 前〜30 s 後の別の地震(時刻差・Mj・その地震からの震央距離)。箱の外の大きな地震や遠い地震の波が重なっていないかを見る。
#   5. 図(白背景・英語・凡例は枠の外): (a) 地震ごとのずれ(全期間、対象の時間を色分け) (b) 時間ごとのずれ(地震 1 つ / 2 つ以上で色分け)
#      (c) 対象の地震で一番ずれた地震の「残り − 局の中央値」と距離 (d) その地震の UD 波形を距離の順に並べ、拾った P と予想の P に印。
#   6. 出力(--base の下): data/24_04g_clock_hour_diagnose.json・PDF/24_04g_clock_hour_diagnose.pdf
#   判定はしない。上の手がかりを数字で並べるだけ。
#
# Usage(Colab。Drive をつなぐだけでよい(N1〜N4 は要らない)。Drive に置いた出力を読む。セルは 24_04g_COLAB_JA.md の G1〜G3):
#   !python /content/drive/MyDrive/ARGUS/src/24_04g_nagano2014_clock_hour_diagnose.py \
#       --base /content/drive/MyDrive/ARGUS_nagano2014 \
#       --catalog /content/drive/MyDrive/ARGUS/data/catalog/jma_nagano2014.csv \
#       --hypo /content/drive/MyDrive/ARGUS/data/catalog/jma_raw/h2014.zip \
#       --src24-01 /content/drive/MyDrive/ARGUS/src/24_01_nagano2014_jma_catalog.py
# 入力  : data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt・data/24_04d_gclock2.json(--base の下)・
#         jma_nagano2014.csv・h2014.zip(無くてもよい: (ii) を飛ばす)・24_01(h2014 の読み方をそのまま使う)
# 出力  : data/24_04g_clock_hour_diagnose.json / PDF/24_04g_clock_hour_diagnose.pdf
# 止める条件(STOP): 入力が無い・全体の中央値が 24_04d の値と 1e-6 s を超えて違う・対象の時間の検測が 0
# =============================================================================
import sys, csv, json, argparse, hashlib, importlib.util, zipfile
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import torch

ap = argparse.ArgumentParser(description="24_04g: G-clock2 (d) で外れた時間の、読むだけの診断(試験は開かない)")
ap.add_argument("--base", required=True, help="ARGUS_nagano2014 の場所(Drive なら /content/drive/MyDrive/ARGUS_nagano2014)")
ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt")
ap.add_argument("--gclock", default="data/24_04d_gclock2.json")
ap.add_argument("--catalog", required=True, help="jma_nagano2014.csv(24_01 の出力、箱の中・全ての規模)")
ap.add_argument("--hypo", default="", help="h2014.zip(日本全体の震源一覧。無ければ (ii) を飛ばす)")
ap.add_argument("--src24-01", dest="src2401", default="", help="24_01_nagano2014_jma_catalog.py(h2014 の読み方を借りる)")
ap.add_argument("--hours", default="", help="対象の時間(日本時間、'YYYY-MM-DD HH' をカンマで区切る)。空なら 24_04d のずれの大きい 5 時間")
ap.add_argument("--selftest", action="store_true")
a = ap.parse_args()
VP, MIN_N, TOL_HOUR, PRE_S, POST_S, P_PRE_S, FS, POOL_H = 6.0, 20, 0.5, 60.0, 30.0, 3.0, 100.0, 72.0
TAG = "[24_04g]"

def jst_hour(ot):                                                # 24_04d と同じ: 秒で切って 9 時間を足す
    t = datetime.strptime(str(ot).replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
    return t + timedelta(hours=9)
def jst_full(ot):                                                # 表示用(秒の小数を残す)
    s = str(ot).replace("T", " ")
    t = datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
    frac = s[19:].split("+")[0]
    us = int(round(float("0" + frac) * 1e6)) if frac.startswith(".") and len(frac) > 1 else 0
    return t + timedelta(hours=9, microseconds=us)
def epi_km(la1, lo1, la2, lo2):
    return float(111.19 * np.hypot(la1 - la2, (lo1 - lo2) * np.cos(np.radians(0.5 * (la1 + la2)))))

def selftest():
    def check(c, m):
        if not c: sys.exit(f"{TAG} STOP: selftest に失敗: {m}")
    check(jst_hour("2014-12-01 22:10:05.3") == datetime(2014, 12, 2, 7, 10, 5), "jst_hour")
    check(abs((jst_full("2014-12-01 22:10:05.30") - datetime(2014, 12, 2, 7, 10, 5, 300000)).total_seconds()) < 1e-6, "jst_full")
    check(abs(epi_km(36.0, 138.0, 36.1, 138.0) - 11.119) < 1e-3, "epi_km")
    print(f"{TAG} selftest: 時刻の変換・距離の式に合格")
selftest()
if a.selftest: sys.exit(0)

BASE = Path(a.base)
cp, gp, catp = BASE / a.cache, BASE / a.gclock, Path(a.catalog)
for p in (cp, gp, catp):
    if not p.exists(): sys.exit(f"{TAG} STOP: {p} が無い")
sha = hashlib.sha256(cp.read_bytes()).hexdigest()
print(f"{TAG} 本スクリプト v1 SHA-256 {hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}")
print(f"{TAG} キャッシュ {cp.name}  SHA-256 {sha}")
EV = torch.load(cp, weights_only=False)
G = json.load(open(gp))

# ---- 1. 残り(24_04d と同じ式)
rows = []
for ie, e in enumerate(EV):
    th = jst_hour(e["origin_time"]); n = int(e["n_real_stations"])
    tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    loc = np.asarray(e["sta_locs"], float)[:n]; d = np.asarray(e["dist_km"], float)[:n]
    for k in range(n):
        if pf[k] != 0 or not np.isfinite(tp[k]) or not np.isfinite(d[k]): continue
        rows.append(dict(ev=ie, k=k, sta=f"{loc[k, 0]:.4f},{loc[k, 1]:.4f}", dist=float(d[k]), tp=float(tp[k]), r=float(tp[k] - d[k] / VP),
                         hour=f"{th:%Y-%m-%d %H}"))
R = np.array([x["r"] for x in rows]); MED = float(np.median(R))
ref = float(G["result"]["median_s"])
print(f"{TAG} 全体: 検測 {len(R)}  残りの中央値 {MED:+.6f} s(24_04d の値 {ref:+.6f} s)")
if abs(MED - ref) > 1e-6: sys.exit(f"{TAG} STOP: 全体の中央値が 24_04d と違う(キャッシュか式が違う)")
STA_MED = {s: float(np.median([x["r"] for x in rows if x["sta"] == s])) for s in sorted({x["sta"] for x in rows})}
EVT = [jst_full(e["origin_time"]) for e in EV]
_sp, _d = [], []
for e in EV:
    n_ = int(e["n_real_stations"]); spv = np.asarray(e["sp_diffs"], float)[:n_]; sfv = np.asarray(e["s_fallback"]).astype(int)[:n_]
    dv = np.asarray(e["dist_km"], float)[:n_]; ok = (sfv == 0) & np.isfinite(spv) & np.isfinite(dv)
    _sp += list(spv[ok]); _d += list(dv[ok])
SP_K = float(np.median(np.array(_sp) / np.array(_d))) if _sp else 0.0              # 全期間の S−P/距離 の中央値(s/km)
SP_MED = float(np.median(np.array(_sp) - SP_K * np.array(_d))) if _sp else 0.0
print(f"{TAG} S−P: 全期間の s_fallback = 0 の {len(_sp)} 局で、S−P/距離 の中央値 {SP_K:.4f} s/km")

# ---- 地震の基本(緯度・経度は保存しない)
MAG = np.array([float(e["mw"]) for e in EV]); im = int(np.argmax(MAG)); ML = np.asarray(EV[im]["src_loc"], float)
T_MAIN = jst_full(EV[im]["origin_time"])
def role(ie):
    t = jst_full(EV[ie]["origin_time"])
    if t <= T_MAIN + timedelta(hours=POOL_H): return "pool"
    return "test candidate" if 1.5 - 1e-9 <= MAG[ie] < 2.0 - 1e-9 else "library only (Mj >= 2.0)"
EVS = []
for ie, e in enumerate(EV):
    m = [x for x in rows if x["ev"] == ie]; sl = np.asarray(e["src_loc"], float)
    base = dict(ev=ie, origin_jst=f"{jst_full(e['origin_time']):%Y-%m-%d %H:%M:%S.%f}"[:22], hour=f"{jst_hour(e['origin_time']):%Y-%m-%d %H}",
                mj=float(MAG[ie]), depth_km=float(sl[2]), epi_from_mainshock_km=round(epi_km(ML[0], ML[1], sl[0], sl[1]), 1), role=role(ie), n=len(m))
    if m:
        r = np.array([x["r"] for x in m]); d = np.array([x["dist"] for x in m])
        rs = np.array([x["r"] - STA_MED[x["sta"]] for x in m])
        base.update(median_s=float(np.median(r)), dev_s=float(np.median(r)) - MED, iqr_s=float(np.subtract(*np.percentile(r, [75, 25]))),
                    slope_s_per_km=(float(np.polyfit(d, r, 1)[0]) if len(m) >= 3 and np.ptp(d) > 1.0 else None),
                    sta_rel_median_s=float(np.median(rs)), sta_rel_iqr_s=float(np.subtract(*np.percentile(rs, [75, 25]))),
                    sta_rel_slope_s_per_km=(float(np.polyfit(d, rs, 1)[0]) if len(m) >= 3 and np.ptp(d) > 1.0 else None))
    EVS.append(base)
ORDER = sorted([x for x in EVS if x["n"]], key=lambda x: x["origin_jst"])

# ---- 2. 時間ごとの地震の数((d) の作り)
HOURS = {}
for x in rows: HOURS.setdefault(x["hour"], []).append(x)
HT = []
for h, xs in sorted(HOURS.items()):
    if len(xs) < MIN_N: continue
    evs = sorted({x["ev"] for x in xs})
    HT.append(dict(hour=h, n_picks=len(xs), n_events=len(evs), dev_s=float(np.median([x["r"] for x in xs])) - MED))
    gh = G.get("by_hour", {}).get(h)
    if gh is not None and (gh["n"] != len(xs) or abs(gh["median"] - np.median([x["r"] for x in xs])) > 1e-6):
        sys.exit(f"{TAG} STOP: {h} 時台の検測の数か中央値が 24_04d と違う(時間の区切り方が違う)")
one = [x for x in HT if x["n_events"] == 1]; many = [x for x in HT if x["n_events"] >= 2]
def summ(v):
    if not v: return "—"
    a_ = np.abs([x["dev_s"] for x in v])
    return f"{len(v)} 時間、|ずれ| 中央値 {np.median(a_):.3f} s・最大 {a_.max():.3f} s・{TOL_HOUR} s を超える時間 {int((a_ > TOL_HOUR).sum())}"
print(f"\n{TAG} (d) の作り: 検測 {MIN_N} 以上の {len(HT)} 時間のうち")
print(f"   地震が 1 つの時間: {summ(one)}")
print(f"   地震が 2 つ以上の時間: {summ(many)}")
ev_dev = np.array([abs(x["dev_s"]) for x in EVS if x["n"] >= MIN_N])
if len(ev_dev): print(f"   参考: 検測 {MIN_N} 以上の地震 {len(ev_dev)} 個の、地震ごとの |ずれ| が {TOL_HOUR} s を超える数 {int((ev_dev > TOL_HOUR).sum())}"
      f"(中央値 {np.median(ev_dev):.3f} s)")

# ---- 震源一覧
CAT = []
with open(catp) as f:
    for row in csv.DictReader(f):
        CAT.append(dict(t=datetime.strptime(row["time"][:22], "%Y-%m-%d %H:%M:%S.%f"), lat=float(row["latitude"]), lon=float(row["longitude"]),
                        dep=float(row["depth_km"]), mj=float(row["mag"]), flag=row.get("det_flag", "")))
FULL = []
if a.hypo and Path(a.hypo).exists() and a.src2401 and Path(a.src2401).exists():
    spec = importlib.util.spec_from_file_location("m2401", a.src2401); m2401 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m2401)
    src = Path(a.hypo)
    raw = b"\n".join(zipfile.ZipFile(src).read(m) for m in zipfile.ZipFile(src).namelist() if not m.endswith("/")) if zipfile.is_zipfile(src) else src.read_bytes()
    recs, _ = m2401.read_records(raw)
    for rr in recs:
        h = m2401.parse_hypo(rr)
        if h["agency"] == "J" and h["origin_jst"] is not None and h["lat"] is not None and h["lon"] is not None:
            FULL.append(dict(t=h["origin_jst"], lat=h["lat"], lon=h["lon"], dep=h["depth_km"], mj=h["mag"]))
    print(f"{TAG} h2014(日本全体、機関 J): {len(FULL)} 震源  SHA-256 {hashlib.sha256(src.read_bytes()).hexdigest()[:12]}…")
else:
    print(f"{TAG} h2014 か 24_01 が渡されていないので、日本全体の震源一覧での確かめ (ii) は飛ばす")
def find_self(L, t0, la, lo, mj):
    """自分の行: 発生時刻 ± 1 s・|ΔMj| ≤ 0.05・震央の間 5 km 以内。見つかった行と時刻差を返す(無ければ None)"""
    c_ = [(abs((c["t"] - t0).total_seconds()), c) for c in L
          if abs((c["t"] - t0).total_seconds()) <= 1.0 and c["mj"] is not None and abs(c["mj"] - mj) <= 0.05 and epi_km(la, lo, c["lat"], c["lon"]) <= 5.0]
    return min(c_, key=lambda z: z[0])[1] if c_ else None
def neighbours(L, t0, la, lo, me=None):
    out = []
    for c in L:
        dt = (c["t"] - t0).total_seconds()
        if -PRE_S <= dt <= POST_S and c is not me:
            out.append(dict(dt_s=round(dt, 2), mj=c["mj"], depth_km=c["dep"], epi_from_event_km=round(epi_km(la, lo, c["lat"], c["lon"]), 1)))
    return out

# ---- 3. 対象の時間
if a.hours.strip():
    TH = [h.strip() for h in a.hours.split(",") if h.strip()]
else:
    bh = G.get("by_hour", {})
    TH = [k for _, k in sorted(((abs(v["median"] - float(G["result"]["median_s"])), k) for k, v in bh.items() if v["n"] >= MIN_N), reverse=True)][:5]   # 24_04d と同じ並べ方
print(f"\n{TAG} 対象の時間(日本時間): {', '.join(TH)}")
TARGET = []
for h in TH:
    hr = [x for x in rows if x["hour"] == h]
    if not hr: sys.exit(f"{TAG} STOP: {h} 時台の検測が 0")
    if h not in G.get("by_hour", {}): sys.exit(f"{TAG} STOP: {h} 時台が 24_04d の by_hour に無い")
    evs = [x for x in EVS if x["hour"] == h and x["n"]]
    print(f"\n  ■ {h} 時台: 地震 {len(evs)}・検測 {len(hr)}・残りの中央値 − 全体 {np.median([x['r'] for x in hr]) - MED:+.3f} s")
    for x in evs:
        e = EV[x["ev"]]; sl = np.asarray(e["src_loc"], float); t0 = jst_full(e["origin_time"])
        me_b = find_self(CAT, t0, sl[0], sl[1], x["mj"]); me_j = find_self(FULL, t0, sl[0], sl[1], x["mj"]) if FULL else None
        x["self_in_box_catalogue"] = None if me_b is None else dict(dt_s=round((me_b["t"] - t0).total_seconds(), 3), det_flag=me_b["flag"])
        x["neighbours_box"] = neighbours(CAT, t0, sl[0], sl[1], me_b); x["neighbours_japan"] = neighbours(FULL, t0, sl[0], sl[1], me_j) if FULL else None
        # S−P(発生時刻にも時計にも左右されない): s_fallback = 0 の局の「S−P − 距離 × 全体の S−P/距離 の傾き」の中央値を、全期間の同じ量と比べる
        n_ = int(e["n_real_stations"]); spv = np.asarray(e["sp_diffs"], float)[:n_]; sfv = np.asarray(e["s_fallback"]).astype(int)[:n_]
        dv = np.asarray(e["dist_km"], float)[:n_]; ok = (sfv == 0) & np.isfinite(spv) & np.isfinite(dv)
        x["sp_rel_median_s"] = float(np.median(spv[ok] - SP_K * dv[ok])) - SP_MED if ok.any() else None; x["n_sp"] = int(ok.sum())
        psn = np.asarray(e.get("p_snr", np.full(n_, np.nan)), float)[:n_]
        x["p_snr_median"] = float(np.nanmedian(psn)) if np.isfinite(psn).any() else None
        # 局ごとの前後 6 時間: この地震を除いた、同じ局の「残り − 局の中央値」の中央値(局の時計がその頃ずれていたか)
        W6 = [z for z in rows if z["ev"] != x["ev"] and abs((EVT[z["ev"]] - t0).total_seconds()) <= 6 * 3600]
        x["same_stations_pm6h_median_s"] = float(np.median([z["r"] - STA_MED[z["sta"]] for z in W6 if z["sta"] in {y["sta"] for y in rows if y["ev"] == x["ev"]}])) if W6 else None
        i = ORDER.index(x); prv = ORDER[i - 1] if i > 0 else None; nxt = ORDER[i + 1] if i + 1 < len(ORDER) else None
        x["prev_event"] = None if prv is None else dict(origin_jst=prv["origin_jst"], mj=prv["mj"], dev_s=prv["dev_s"], n=prv["n"])
        x["next_event"] = None if nxt is None else dict(origin_jst=nxt["origin_jst"], mj=nxt["mj"], dev_s=nxt["dev_s"], n=nxt["n"])
        sl_ = "—" if x["slope_s_per_km"] is None else f"{x['slope_s_per_km']:+.4f}"
        sr_ = "—" if x["sta_rel_slope_s_per_km"] is None else f"{x['sta_rel_slope_s_per_km']:+.4f}"
        print(f"    地震 {x['origin_jst']} JST  Mj {x['mj']:.1f}  深さ {x['depth_km']:.1f} km  本震から {x['epi_from_mainshock_km']:.1f} km  役割 {x['role']}")
        print(f"      検測 {x['n']}  ずれ {x['dev_s']:+.3f} s  四分位幅 {x['iqr_s']:.3f} s  残りと距離の傾き {sl_} s/km")
        print(f"      局のふだんのずれを除いた量(残り − その局の中央値): 中央値 {x['sta_rel_median_s']:+.3f} s  四分位幅 {x['sta_rel_iqr_s']:.3f} s  "
              f"距離の傾き {sr_} s/km")
        for lab, y in (("1 つ前", x["prev_event"]), ("1 つ後", x["next_event"])):
            if y: print(f"      時刻の順で{lab}の地震: {y['origin_jst']} Mj {y['mj']:.1f}  検測 {y['n']}  ずれ {y['dev_s']:+.3f} s")
        sb = x["self_in_box_catalogue"]
        print(f"      震源一覧の自分の行: " + ("見つからない(注意)" if sb is None else f"時刻差 {sb['dt_s']:+.3f} s  震源決定の印 '{sb['det_flag']}'"))
        sp_ = "—" if x["sp_rel_median_s"] is None else f"{x['sp_rel_median_s']:+.3f} s({x['n_sp']} 局)"
        pm_ = "—" if x["same_stations_pm6h_median_s"] is None else f"{x['same_stations_pm6h_median_s']:+.3f} s"
        sn_ = "—" if x["p_snr_median"] is None else f"{x['p_snr_median']:.1f}"
        print(f"      S−P(距離の分を引き、全期間の中央値との差。発生時刻・時計に左右されない): {sp_}   P の SNR の中央値 {sn_}")
        print(f"      同じ局の、前後 6 時間の他の地震での「残り − 局の中央値」の中央値: {pm_}")
        nb = x["neighbours_box"]
        print(f"      箱の中の震源一覧(全ての規模)で、発生の {PRE_S:.0f} s 前〜{POST_S:.0f} s 後の別の地震: {len(nb)}")
        for c in nb: print(f"        時刻差 {c['dt_s']:+7.2f} s  Mj {c['mj']:.1f}  深さ {c['depth_km']:.1f} km  震央の間 {c['epi_from_event_km']:.1f} km")
        if FULL:
            nj = x["neighbours_japan"]
            print(f"      日本全体(h2014、機関 J)で、発生の {PRE_S:.0f} s 前〜{POST_S:.0f} s 後の別の地震: {len(nj)}")
            for c in sorted(nj, key=lambda c: -(c["mj"] if c["mj"] is not None else -9))[:8]:
                mj_ = "—" if c["mj"] is None else f"{c['mj']:.1f}"
                print(f"        時刻差 {c['dt_s']:+7.2f} s  Mj {mj_}  深さ {c['depth_km']} km  この地震からの震央距離 {c['epi_from_event_km']:.1f} km")
        print(f"      局ごと(震源距離の順。局の座標は出さない: 座標と震源距離から震源の位置が逆算できるため): 順位, 震源距離 km, 残り − 全体 s, 残り − その局の中央値 s")
        for i_, y in enumerate(sorted([z for z in rows if z["ev"] == x["ev"]], key=lambda z: z["dist"]), 1):
            print(f"        #{i_:02d}  {y['dist']:6.1f}  {y['r'] - MED:+7.3f}  {y['r'] - STA_MED[y['sta']]:+7.3f}")
        TARGET.append(x)

# ---- 5. 図
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
fig = plt.figure(figsize=(13, 10))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.5], hspace=0.6, wspace=0.28)
ax = fig.add_subplot(gs[0, 0])
SHOWN = [x for x in ORDER if x["role"] != "test candidate" or x["hour"] in TH]     # 試験の候補は、対象の時間の地震だけを描く
tt = [datetime.strptime(x["origin_jst"], "%Y-%m-%d %H:%M:%S.%f") for x in SHOWN]
inh = [x["hour"] in TH for x in SHOWN]
ax.scatter([t for t, f in zip(tt, inh) if not f], [x["dev_s"] for x, f in zip(SHOWN, inh) if not f], s=8, color="0.6", label="Other events (test candidates not shown)")
ax.scatter([t for t, f in zip(tt, inh) if f], [x["dev_s"] for x, f in zip(SHOWN, inh) if f], s=36, color="tab:red", marker="D", label="Events in the flagged hours")
ax.axhspan(-TOL_HOUR, TOL_HOUR, color="tab:green", alpha=0.12, label="Hourly allowance (+/- 0.5 s)")
ax.set_ylabel("Event median residual - median of all picks (s)"); ax.set_xlabel("JST (2014)")
ax.set_title(f"(a) Per-event residual offset, {len(SHOWN)} of {len(ORDER)} events", fontsize=9); ax.grid(alpha=0.3); ax.tick_params(axis="x", labelrotation=30, labelsize=7)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.35), ncol=3, frameon=False, fontsize=8)
ax = fig.add_subplot(gs[0, 1])
for v, c, lab in ((one, "tab:orange", "Hours with one event"), (many, "tab:blue", "Hours with two or more events")):
    if v: ax.scatter([datetime.strptime(x["hour"], "%Y-%m-%d %H") for x in v], [x["dev_s"] for x in v], s=14, color=c, label=f"{lab} ({len(v)})")
ax.axhspan(-TOL_HOUR, TOL_HOUR, color="tab:green", alpha=0.12, label="Hourly allowance (+/- 0.5 s)")
ax.set_ylabel("Hour median residual - median of all picks (s)"); ax.set_xlabel("JST (2014)")
ax.set_title(f"(b) Hourly check (d): hours with >= {MIN_N} picks", fontsize=9); ax.grid(alpha=0.3); ax.tick_params(axis="x", labelrotation=30, labelsize=7)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.35), ncol=2, frameon=False, fontsize=8)
W0 = max(TARGET, key=lambda x: abs(x["dev_s"])) if TARGET else None
if W0 is not None:
    m = sorted([z for z in rows if z["ev"] == W0["ev"]], key=lambda z: z["dist"])
    ax = fig.add_subplot(gs[1, 0])
    ax.scatter([z["dist"] for z in m], [z["r"] - STA_MED[z["sta"]] for z in m], s=24, color="tab:red", label="Residual - station median")
    ax.scatter([z["dist"] for z in m], [z["r"] - MED for z in m], s=14, color="0.5", marker="x", label="Residual - median of all picks")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("Hypocentral distance (km)"); ax.set_ylabel("Residual offset (s)")
    ax.set_title(f"(c) Most offset event: {W0['origin_jst']} JST, Mj {W0['mj']:.1f}, depth {W0['depth_km']:.1f} km", fontsize=9); ax.grid(alpha=0.3)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False, fontsize=8)
    ax = fig.add_subplot(gs[1, 1]); e = EV[W0["ev"]]; n = int(e["n_real_stations"])
    Wv = np.asarray(e["waveforms"], float)[:n, 0]; d = np.asarray(e["dist_km"], float)[:n]; tp = np.asarray(e["tp_times"], float)[:n]
    pf = np.asarray(e["p_fallback"]).astype(int)[:n]; loc = np.asarray(e["sta_locs"], float)[:n]
    order = np.argsort(d); tax = np.arange(Wv.shape[1]) / FS
    for row_i, k in enumerate(order):
        w = Wv[k] / (np.max(np.abs(Wv[k])) + 1e-12)
        ax.plot(tax, row_i + 0.45 * w, lw=0.5, color="k" if pf[k] == 0 else "0.6")
        ax.plot([P_PRE_S, P_PRE_S], [row_i - 0.4, row_i + 0.4], color="tab:blue", lw=1.2)
        key = f"{loc[k, 0]:.4f},{loc[k, 1]:.4f}"
        exp_rel = P_PRE_S + (d[k] / VP + STA_MED.get(key, MED) - tp[k])
        if 0 <= exp_rel <= tax[-1]: ax.plot([exp_rel, exp_rel], [row_i - 0.4, row_i + 0.4], color="tab:orange", lw=1.2)
    ax.set_yticks(range(n)); ax.set_yticklabels([f"{d[k]:.0f} km" for k in order], fontsize=6)
    ax.set_xlabel("Time in the cached window (s); picked P at 3 s"); ax.set_ylabel("Station (hypocentral distance)")
    ax.set_title("(d) Same event: UD traces (each normalised)", fontsize=9); ax.grid(alpha=0.2)
    ax.plot([], [], color="tab:blue", label="PhaseNet P used in the cache")
    ax.plot([], [], color="tab:orange", label="Expected P (JMA origin + distance / 6.0 km/s + station median)")
    ax.plot([], [], color="0.6", label="Fallback pick (not used in G-clock2)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=1, frameon=False, fontsize=8)
fig.suptitle("Northern Nagano 2014, G-clock2 hourly check: what happened in the flagged hours (descriptive, read-only; no location computed)", fontsize=10)
(BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
fig.savefig(BASE / "PDF" / "24_04g_clock_hour_diagnose.pdf", bbox_inches="tight"); plt.close(fig)

json.dump(dict(script="24_04g_nagano2014_clock_hour_diagnose.py", version="v1",
               script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               purpose="descriptive diagnosis only; the stop decision is unchanged; no location or method error computed; "
                       "catalogue values shown are Mj, depth and distance from the mainshock only (no latitude/longitude)",
               cache=str(cp), cache_sha256=sha, vp_kms=VP, median_all_s=MED, n_picks=len(R), target_hours=TH,
               hour_structure=dict(n_hours=len(HT), one_event_hours=one, multi_event_hours=many),
               test_candidates_shown=[dict(origin_jst=x["origin_jst"], hour=x["hour"]) for x in TARGET if x["role"] == "test candidate"],
               target_events=TARGET),
          open(BASE / "data" / "24_04g_clock_hour_diagnose.json", "w"), indent=1, default=str)
print(f"\n{TAG} 出力: {BASE / 'data' / '24_04g_clock_hour_diagnose.json'}、{BASE / 'PDF' / '24_04g_clock_hour_diagnose.pdf'}")
