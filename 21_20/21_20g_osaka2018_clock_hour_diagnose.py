#!/usr/bin/env python3
# =============================================================================
# Script : 21_20g_osaka2018_clock_hour_diagnose.py  (v1)
#          [読むだけの記述: 大阪府北部 2018 の G-clock2 (d)「1 時間ごと」で外れた 1 時間(既定 2018-06-19 21 時台 JST)に何が起きたかを、
#           地震ごと・局ごとの P の残りと、気象庁の震源一覧(全ての規模)と、キャッシュの波形で調べる]
# Project: ARGUS(新生)— 21_20 は事前登録 5.3 節の 2 のとおり開かずに止めた(commit 3839889)。このスクリプトはその原因を調べる記述だけで、
#          止める判断は変えない。位置の計算(M6r・C1〜C4・L4)は一切しない(試験を開かない)。読むのは P の時刻・震源一覧・波形だけ。
#
# なぜ必要か:
#   (d) は 131 時間のうち 1 時間(検測 48、中央値 −2.827 s、全体からのずれ 3.132 s)だけで外れ、他の 130 時間は全て 0.13 s 以内だった。
#   1 地震で使う局は最大 24 なので、48 は 2 地震分の可能性がある。仮説(まだ確かめていない):
#     H-event: 局の時計ではなく、地震ごとの食い違い。例えば、21_20c の検測は「発生時刻の 10 s 前から、確率 0.3 以上で一番早い P」を
#              拾うので、発生の数秒前に別の地震があれば、その P を拾いうる(2016 の 10 km 超の外れの 32/38 が早い側だったのと同じ形)。
#     H-clock: その時間だけ、記録の時刻が全ての局でずれていた。
#   区別の手がかり:
#     - 地震の中の全ての局の残りが同じ量だけずれ、距離によらない → 発生時刻の食い違い(H-event のうち、拾った P が別の地震でも
#       震源がほぼ同じ場所の時)か、時刻のずれ(H-clock)。
#     - ずれが距離で変わる(残りと距離の傾きが 0 から離れる)→ 別の場所の地震の P を拾った(H-event)。
#     - 震源一覧で、発生の 15 s 前〜5 s 後に別の地震がある → H-event の候補。
#     - 同じ時間の他の地震や、前後の時間の地震は正常 → H-clock(時間全体のずれ)らしくない。
#     - 波形で、拾った P(窓の 3 s 目)の後、予想の P(気象庁の発生時刻と距離 / 6.0 km/s + 全体の中央値)の所にも立ち上がりがある
#       → 早い方は別の揺れを拾った。
#
# 何をするか:
#   1. キャッシュ(21_20c の本番、SHA-256 b9162a9d…aa83)の全ての地震・局で、21_20d と同じ式の残り r = tp_times − dist_km / 6.0 を出す
#      (p_fallback = 0 の検測だけ)。全体の中央値を出す(21_20d の +0.305 s と同じになるはず。違えば止める)。
#   2. 地震ごと: 検測の数・残りの中央値・全体の中央値からのずれ・四分位幅・残りと距離の傾き(最小二乗)。|ずれ| > 1.0 s の地震を全期間で数えて並べる。
#   3. 対象の 1 時間の地震: 地震ごとの表と、局ごとの表(局・震源距離・P の時刻・予想の P・残り)。
#   4. 震源一覧(jma_osaka2018.csv、全ての規模): 対象の地震ごとに、発生の 15 s 前〜5 s 後の別の地震(時刻差・Mj・震央の間の距離)。
#      全期間の |ずれ| > 1.0 s の地震についても同じ数え方をする(その形がこの 1 時間だけか、全体の特徴かを見る)。
#   5. 図(白背景・英語・凡例は枠の外): (a) 地震ごとのずれ(全期間、対象の時間を色分け) (b) 対象の地震の残りと距離
#      (c)・(d) 対象の地震の UD 波形を距離の順に並べ、拾った P(3 s 目)と予想の P に印を付ける(各トレースは最大値で割る)。
#   6. 出力: data/21_20g_clock_hour_diagnose.json・PDF/21_20g_clock_hour_diagnose.pdf(--base の下)。
#   判定はしない。上の手がかりを数字で並べるだけ。結果で規則・キャッシュ・止める判断を変えない。
#
# Usage(Colab。ランタイムを新しくしても動く。Drive に置いたキャッシュをそのまま読む):
#   !python /content/drive/MyDrive/ARGUS/src/21_20g_osaka2018_clock_hour_diagnose.py \
#       --base /content/drive/MyDrive/ARGUS_osaka2018 \
#       --catalog /content/drive/MyDrive/ARGUS/data/catalog/jma_osaka2018.csv
#   (--hour "2018-06-19 21" で対象の時間を変えられる。--cache は --base からの場所)
# 入力  : data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt・data/21_20d_gclock2.json(--base の下)・jma_osaka2018.csv
# 出力  : data/21_20g_clock_hour_diagnose.json / PDF/21_20g_clock_hour_diagnose.pdf
# 止める条件(STOP): 入力が無い・全体の中央値が 21_20d の値と 1e-6 s を超えて違う・対象の時間の検測が 0
# =============================================================================
import sys, csv, json, argparse, hashlib
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import torch

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True, help="ARGUS_osaka2018 の場所(Drive なら /content/drive/MyDrive/ARGUS_osaka2018)")
ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt")
ap.add_argument("--gclock", default="data/21_20d_gclock2.json")
ap.add_argument("--catalog", required=True, help="jma_osaka2018.csv(21_20a の出力、全ての規模)")
ap.add_argument("--hour", default="2018-06-19 21", help="対象の時間(日本時間、'YYYY-MM-DD HH')")
a = ap.parse_args()
VP, DEV_EV, PRE_S, POST_S, P_PRE_S, FS = 6.0, 1.0, 15.0, 5.0, 3.0, 100.0
BASE = Path(a.base)
TAG = "[21_20g]"

def jst(ot):                                                     # キャッシュの origin_time は UTC。日本時間にする(21_20d と同じ)
    t = datetime.strptime(str(ot).replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
    import re
    mfr = re.match(r"\.(\d+)", str(ot).replace("T", " ")[19:])                  # 秒の小数(あれば)。21_20d は秒で切るが、ここは表示のため残す
    us = int(round(float("0." + mfr.group(1)) * 1e6)) if mfr else 0
    return t + timedelta(hours=9, microseconds=us)
def epi_km(la1, lo1, la2, lo2):
    return 111.19 * np.hypot(la1 - la2, (lo1 - lo2) * np.cos(np.radians(0.5 * (la1 + la2))))

cp, gp, catp = BASE / a.cache, BASE / a.gclock, Path(a.catalog)
for p in (cp, gp, catp):
    if not p.exists(): sys.exit(f"{TAG} STOP: {p} が無い")
sha = hashlib.sha256(cp.read_bytes()).hexdigest()
print(f"{TAG} キャッシュ {cp.name}  SHA-256 {sha}")
EV = torch.load(cp, weights_only=False)
G = json.load(open(gp))

# ---- 1. 残り(21_20d と同じ式)
rows = []                                                        # 1 検測 = 1 行
for ie, e in enumerate(EV):
    tj = jst(e["origin_time"]); n = int(e["n_real_stations"])
    tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    loc = np.asarray(e["sta_locs"], float)[:n]; d = np.asarray(e["dist_km"], float)[:n]
    for k in range(n):
        if pf[k] != 0 or not np.isfinite(tp[k]) or not np.isfinite(d[k]): continue
        rows.append(dict(ev=ie, k=k, sta=f"{loc[k, 0]:.4f},{loc[k, 1]:.4f}", dist=float(d[k]), tp=float(tp[k]), r=float(tp[k] - d[k] / VP),
                         hour=f"{tj:%Y-%m-%d %H}"))
R = np.array([x["r"] for x in rows]); MED = float(np.median(R))
ref = float(G["result"]["median_s"])
print(f"{TAG} 全体: 検測 {len(R)}  残りの中央値 {MED:+.6f} s(21_20d の値 {ref:+.6f} s)")
if abs(MED - ref) > 1e-6: sys.exit(f"{TAG} STOP: 全体の中央値が 21_20d と違う(キャッシュか式が違う)")

# ---- 震源一覧(全ての規模、日本時間)
CAT = []
with open(catp) as f:
    for row in csv.DictReader(f):
        CAT.append(dict(t=datetime.strptime(row["time"][:22], "%Y-%m-%d %H:%M:%S.%f"), lat=float(row["latitude"]), lon=float(row["longitude"]),
                        dep=float(row["depth_km"]), mj=float(row["mag"])))
CAT.sort(key=lambda c: c["t"])
def neighbours(t0, la, lo):
    out = []
    for c in CAT:
        dt = (c["t"] - t0).total_seconds()
        if -PRE_S <= dt <= POST_S and abs(dt) > 0.05:
            out.append(dict(dt_s=round(dt, 2), mj=c["mj"], epi_sep_km=round(float(epi_km(la, lo, c["lat"], c["lon"])), 2), depth_km=c["dep"],
                            time_jst=f"{c['t']:%Y-%m-%d %H:%M:%S.%f}"[:22]))
    return out

# ---- 2. 地震ごと
EVS = []
for ie, e in enumerate(EV):
    m = [x for x in rows if x["ev"] == ie]
    tj = jst(e["origin_time"]); sl = np.asarray(e["src_loc"], float)
    if not m:
        EVS.append(dict(ev=ie, origin_jst=f"{tj:%Y-%m-%d %H:%M:%S.%f}"[:22], mj=float(e["mw"]), n=0)); continue
    r = np.array([x["r"] for x in m]); d = np.array([x["dist"] for x in m])
    slope = float(np.polyfit(d, r, 1)[0]) if len(m) >= 3 and np.ptp(d) > 1.0 else None
    med = float(np.median(r))
    EVS.append(dict(ev=ie, origin_jst=f"{tj:%Y-%m-%d %H:%M:%S.%f}"[:22], hour=f"{tj:%Y-%m-%d %H}", mj=float(e["mw"]), lat=float(sl[0]), lon=float(sl[1]),
                    depth_km=float(sl[2]), n=len(m), median_s=med, dev_s=med - MED, iqr_s=float(np.subtract(*np.percentile(r, [75, 25]))),
                    slope_s_per_km=slope, n_dev_gt1=int((np.abs(r - MED) > DEV_EV).sum())))
bad = [x for x in EVS if x["n"] and abs(x["dev_s"]) > DEV_EV]
print(f"{TAG} 地震ごと: {len(EV)} 地震のうち、残りの中央値が全体から {DEV_EV} s より大きくずれた地震 {len(bad)}")
for x in bad:
    nb = neighbours(datetime.strptime(x["origin_jst"], "%Y-%m-%d %H:%M:%S.%f"), x["lat"], x["lon"]); x["neighbours"] = nb
    pre = [c for c in nb if c["dt_s"] < 0]
    sl_txt = "—" if x["slope_s_per_km"] is None else f"{x['slope_s_per_km']:+.4f}"
    print(f"   {x['origin_jst']} Mj {x['mj']:.1f}  検測 {x['n']:2d}  ずれ {x['dev_s']:+.2f} s  四分位幅 {x['iqr_s']:.2f} s  "
          f"距離の傾き {sl_txt} s/km  "
          f"前 {PRE_S:.0f} s 以内の別の地震 {len(pre)}" + (f"(最も近い {pre[-1]['dt_s']:+.2f} s・Mj {pre[-1]['mj']:.1f}・震央の間 {pre[-1]['epi_sep_km']:.1f} km)" if pre else ""))

# ---- 3. 対象の 1 時間
H = [x for x in EVS if x.get("hour") == a.hour]
HR = [x for x in rows if x["hour"] == a.hour]
if not HR: sys.exit(f"{TAG} STOP: {a.hour} 時台の検測が 0")
print(f"\n{TAG} 対象の時間 {a.hour} 時台(日本時間): 地震 {len(H)}・検測 {len(HR)}・残りの中央値 {np.median([x['r'] for x in HR]):+.3f} s")
for x in H:
    t0 = datetime.strptime(x["origin_jst"], "%Y-%m-%d %H:%M:%S.%f")
    x["neighbours"] = neighbours(t0, x["lat"], x["lon"]) if x["n"] else []
    if not x["n"]: print(f"  {x['origin_jst']} Mj {x['mj']:.1f}: P を測った検測なし"); continue
    print(f"  ■ {x['origin_jst']} Mj {x['mj']:.1f}  震源 {x['lat']:.4f},{x['lon']:.4f} 深さ {x['depth_km']:.1f} km  検測 {x['n']}  "
          f"ずれ {x['dev_s']:+.3f} s  四分位幅 {x['iqr_s']:.3f} s  距離の傾き "
          + ("—" if x["slope_s_per_km"] is None else f"{x['slope_s_per_km']:+.4f} s/km") + f"  |ずれ| > {DEV_EV} s の局 {x['n_dev_gt1']}/{x['n']}")
    print(f"     震源一覧の、発生の {PRE_S:.0f} s 前〜{POST_S:.0f} s 後の別の地震: {len(x['neighbours'])}")
    for c in x["neighbours"]:
        print(f"       {c['time_jst']}  時刻差 {c['dt_s']:+6.2f} s  Mj {c['mj']:.1f}  深さ {c['depth_km']:.1f} km  震央の間 {c['epi_sep_km']:.1f} km")
    print(f"     局ごと(震源距離の順): 局, 震源距離 km, P の時刻 s, 予想の P(距離/6.0 + 全体の中央値) s, 残り − 全体の中央値 s")
    for y in sorted([z for z in rows if z["ev"] == x["ev"]], key=lambda z: z["dist"]):
        print(f"       {y['sta']}  {y['dist']:6.1f}  {y['tp']:7.3f}  {y['dist'] / VP + MED:7.3f}  {y['r'] - MED:+7.3f}")
others = [x for x in EVS if x.get("hour") != a.hour and x["n"]]
print(f"\n{TAG} 参考: 対象の時間以外の {len(others)} 地震の |ずれ| の中央値 {np.median([abs(x['dev_s']) for x in others]):.3f} s、"
      f"最大 {max(abs(x['dev_s']) for x in others):.3f} s")
hh = sorted({x["hour"] for x in EVS if x.get("hour")})
i = hh.index(a.hour) if a.hour in hh else -1
for h_ in (hh[i - 1:i] + hh[i + 1:i + 2] if i >= 0 else []):
    v = [x for x in EVS if x.get("hour") == h_ and x["n"]]
    print(f"   前後の地震のある時間 {h_} 時台: 地震 {len(v)}  ずれ " + ", ".join(f"{x['dev_s']:+.2f}" for x in v) + " s")

# ---- 5. 図
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
HE = sorted([x for x in H if x["n"]], key=lambda x: -abs(x["dev_s"]))[:2]          # ずれの大きい 2 地震の波形を描く
fig = plt.figure(figsize=(13, 9.5))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.6], hspace=0.55, wspace=0.25)
ax = fig.add_subplot(gs[0, 0])
tt = [datetime.strptime(x["origin_jst"], "%Y-%m-%d %H:%M:%S.%f") for x in EVS if x["n"]]
dv = [x["dev_s"] for x in EVS if x["n"]]; inh = [x.get("hour") == a.hour for x in EVS if x["n"]]
ax.scatter([t for t, f in zip(tt, inh) if not f], [v for v, f in zip(dv, inh) if not f], s=10, color="0.55", label="Other events")
ax.scatter([t for t, f in zip(tt, inh) if f], [v for v, f in zip(dv, inh) if f], s=40, color="tab:red", marker="D", label=f"Events in {a.hour} h JST")
ax.axhspan(-0.5, 0.5, color="tab:green", alpha=0.12, label="Hourly allowance (+/- 0.5 s)")
ax.set_ylabel("Event median residual - median of all picks (s)"); ax.set_xlabel("JST (2018)")
ax.set_title(f"(a) Per-event residual offset, {len(tt)} events", fontsize=9); ax.grid(alpha=0.3)
ax.tick_params(axis="x", labelrotation=30, labelsize=7)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=3, frameon=False, fontsize=8)
ax = fig.add_subplot(gs[0, 1])
ax.scatter([x["dist"] for x in rows], [x["r"] - MED for x in rows], s=3, color="0.75", label="All picks")
cols = ["tab:red", "tab:purple"]
for j, x in enumerate(HE):
    m = [z for z in rows if z["ev"] == x["ev"]]
    ax.scatter([z["dist"] for z in m], [z["r"] - MED for z in m], s=22, color=cols[j], label=f"{x['origin_jst'][11:19]} JST, Mj {x['mj']:.1f}")
ax.set_xlabel("Hypocentral distance (km)"); ax.set_ylabel("Residual - median of all picks (s)")
ax.set_title("(b) Residual vs distance", fontsize=9); ax.grid(alpha=0.3)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncol=3, frameon=False, fontsize=8)
for j, x in enumerate(HE):
    ax = fig.add_subplot(gs[1, j]); e = EV[x["ev"]]; n = int(e["n_real_stations"])
    W = np.asarray(e["waveforms"], float)[:n, 0]; d = np.asarray(e["dist_km"], float)[:n]; tp = np.asarray(e["tp_times"], float)[:n]
    pf = np.asarray(e["p_fallback"]).astype(int)[:n]
    order = np.argsort(d); tax = np.arange(W.shape[1]) / FS
    for row_i, k in enumerate(order):
        w = W[k]; w = w / (np.max(np.abs(w)) + 1e-12)
        ax.plot(tax, row_i + 0.45 * w, lw=0.5, color="k" if pf[k] == 0 else "0.6")
        exp_rel = P_PRE_S + (d[k] / VP + MED - tp[k])           # 予想の P の、窓の中での位置
        ax.plot([P_PRE_S, P_PRE_S], [row_i - 0.4, row_i + 0.4], color="tab:blue", lw=1.2)
        if 0 <= exp_rel <= tax[-1]: ax.plot([exp_rel, exp_rel], [row_i - 0.4, row_i + 0.4], color="tab:orange", lw=1.2)
    ax.set_yticks(range(n)); ax.set_yticklabels([f"{d[k]:.0f} km" for k in order], fontsize=6)
    ax.set_xlabel("Time in the cached window (s); picked P at 3 s"); ax.set_ylabel("Station (hypocentral distance)")
    ax.set_title(f"({'cd'[j]}) {x['origin_jst']} JST, Mj {x['mj']:.1f}: UD traces", fontsize=9); ax.grid(alpha=0.2)
    ax.plot([], [], color="tab:blue", label="PhaseNet P used in the cache"); ax.plot([], [], color="tab:orange", label="Expected P (JMA origin + distance / 6.0 km/s + median)")
    ax.plot([], [], color="0.6", label="Fallback pick (not used in G-clock2)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.09), ncol=1, frameon=False, fontsize=8)
fig.suptitle(f"Northern Osaka 2018, G-clock2 hourly check: what happened in {a.hour} h JST (descriptive, read-only)", fontsize=10)
(BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
fig.savefig(BASE / "PDF" / "21_20g_clock_hour_diagnose.pdf", bbox_inches="tight"); plt.close(fig)

json.dump(dict(script="21_20g_osaka2018_clock_hour_diagnose.py", version="v1", purpose="descriptive diagnosis only; the stop decision is unchanged; no location computed",
               cache=str(cp), cache_sha256=sha, hour=a.hour, vp_kms=VP, median_all_s=MED, n_picks=len(R),
               events_dev_gt_1s=bad, target_hour_events=H,
               target_hour_picks=[dict(ev=z["ev"], station=z["sta"], dist_km=z["dist"], tp_s=z["tp"], resid_minus_median_s=z["r"] - MED) for z in HR]),
          open(BASE / "data" / "21_20g_clock_hour_diagnose.json", "w"), indent=1, default=str)
print(f"\n{TAG} 出力: {BASE / 'data' / '21_20g_clock_hour_diagnose.json'}、{BASE / 'PDF' / '21_20g_clock_hour_diagnose.pdf'}")
