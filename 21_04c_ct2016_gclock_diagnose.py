#!/usr/bin/env python3
# =============================================================================
# Script : 21_04c_ct2016_gclock_diagnose.py  (v1)
#          [21_04b のセル 9 で G-clock が 1 地震(2016-10-21 22:03:12.29 JST、Mj 3.9)だけ FAIL になった理由を調べる。読むだけで、
#           h5・ゲート・規則は何も変えない]
# Project: ARGUS(新生)— 2 つ目の余震系列での確認(21_04)の入力の確かめ
#
# なぜ必要か:
#   G-clock は「時計(時刻)がずれていないか」を見るゲートで、近い 8 局の STA/LTA の立ち上がりと、予想の P の到着(震源距離 / 6.0 km/s)
#   の差の中央値が 1.5 s 以内かを見る。セル 9 では、本震 0.33 s・10-29 の Mj 4.5 は 0.40 s・10-21 22:53 の Mj 3.8 は 1.01 s で通り、
#   10-21 22:03 の Mj 3.9 だけが 2.79 s で FAIL だった。時計のずれなら、同じ日の他の地震(22:53)や本震もずれるはずである。
#   そこで、この地震で立ち上がりが P ではなく S(S − P は近い局で 2〜4 s)や前後の別の地震で取られていないかを、波形と数字で確かめる。
#   結果を見てから 21_04b の規則を変えるかは、この出力を貼ってから相談して決める(ここでは何も決めない)。
#
# 何をするか:
#   1. Drive の ARGUS_ct2016 から、組み立てた h5(ct2016_100Hz.h5.part・ct2016_100Hz_FAILED.h5・ct2016_100Hz.h5 のどれか)と、
#      21_04b の報告(data/21_04b_report.json)・計画(data/21_04b_plan.json。候補局の位置)・気象庁の震源(ARGUS/data/catalog/jma_ct2016.csv)
#      を読む。3 つの h5 のうちどれがあるか(大きさ)も表示する(セル 9 の最後の名前の付け替えが失敗したため)。
#   2. 報告の G-clock に書かれた 4 地震(本震と他の 3 地震)ごとに、21_04b と全く同じ選び方(使う 50 局のうち近い 12 局を順に見て、
#      区間 [発生 − 10 s, 発生 + 45 s] を覆う局で、立ち上がりが取れた最初の 8 局)で、局ごとに次を出す:
#        震源距離・立ち上がり − 発生(21_04b の sta_lta_first をそのまま読み込んで使う)・予想の P(距離 / 6.0)・予想の S(距離 / 3.5)・
#        P との差・S との差
#      その地震の前後(発生の 120 s 前〜45 s 後)の気象庁の震源(全ての Mj)も並べる。
#   3. 図: 4 地震ごとに、8 局の上下動(21_04b と同じ 1–15 Hz の因果フィルタ、局ごとに最大で割る)を距離の順に並べ、予想の P(青)・
#      予想の S(赤)・STA/LTA の立ち上がり(黒)・前後の気象庁の地震の発生(灰)を縦線で描く。白背景・英語・凡例は枠の外。
#      ARGUS_ct2016/PDF/21_04c_gclock_diagnose.pdf
#   4. 表: ARGUS_ct2016/data/21_04c_gclock_diagnose.csv、まとめ: ARGUS_ct2016/data/21_04c_gclock_diagnose.json
#
# Usage(Colab、セル 1〜4 の後に新しいセルで):
#   run([f'{SRC}/21_04c_ct2016_gclock_diagnose.py'])
# 止める条件(STOP): h5 が 1 つも無い・報告か計画か震源が無い・報告に G-clock が無い
# =============================================================================
import sys, json, csv, importlib.util
from pathlib import Path
from datetime import datetime
import numpy as np

import os
A = Path(os.environ.get("ARGUS_A", "/content/drive/MyDrive/ARGUS")); O = Path(os.environ.get("ARGUS_O", "/content/drive/MyDrive/ARGUS_ct2016"))   # 試験用に環境変数で変えられる
spec = importlib.util.spec_from_file_location("b21_04b", str(A / "src" / "21_04b_ct2016_hinet_to_h5.py"))
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)          # 21_04b の関数をそのまま使う(写さない)
print(f"[21_04c] 21_04b {B.VERSION} の関数を読み込んだ(sta_lta_first・jst_epoch・haversine_km・covers)")

W = O / "data" / "waves"
cands = [W / "ct2016_100Hz.h5.part", W / "ct2016_100Hz_FAILED.h5", W / "ct2016_100Hz.h5"]
for p in cands: print(f"[21_04c] {p.name}: " + (f"ある({p.stat().st_size / 1e9:.2f} GB)" if p.exists() else "無い"))
h5p = next((p for p in cands if p.exists()), None)
if h5p is None: sys.exit("[21_04c] STOP: 組み立てた h5 が 1 つも無い(セル 9 をもう一度回してから)")
rp, pp, cp = O / "data" / "21_04b_report.json", O / "data" / "21_04b_plan.json", A / "data" / "catalog" / "jma_ct2016.csv"
for p in (rp, pp, cp):
    if not p.exists(): sys.exit(f"[21_04c] STOP: {p} が無い")
rep = json.load(open(rp)); plan = json.load(open(pp))
if "clock" not in rep.get("gates", {}): sys.exit("[21_04c] STOP: 報告に G-clock が無い")
keep, meta = rep["stations"], plan["candidates"]
cat = []
for r in csv.DictReader(open(cp)):
    cat.append(dict(t=datetime.strptime(r["time"][:22].ljust(22, "0"), "%Y-%m-%d %H:%M:%S.%f"), mag=float(r["mag"]),
                    lat=float(r["latitude"]), lon=float(r["longitude"]), dep=float(r["depth_km"])))
print(f"[21_04c] 使う h5: {h5p.name}  局 {len(keep)}  震源 {len(cat)}")

def find_ev(origin):
    t = datetime.strptime(origin[:22].ljust(22, "0") if "." in origin else origin + ".00", "%Y-%m-%d %H:%M:%S.%f")
    return min(cat, key=lambda r: abs((r["t"] - t).total_seconds()))

import h5py
from scipy.signal import butter, sosfilt
SOS = butter(4, [1.0, 15.0], btype="band", fs=B.FS, output="sos")
VS = 3.5
rows, summ, plots = [], [], []
with h5py.File(h5p, "r") as H:
    st = np.array([s.decode() if isinstance(s, bytes) else str(s) for s in H["stations"][:]]); ep = H["window_epoch"][:]
    for c in rep["gates"]["clock"]:
        ev = find_ev(c["origin_jst"]); t0 = B.jst_epoch(ev["t"])
        t_a, t_b = t0 - B.SEG_PRE_S, t0 + B.SEG_POST_S
        near = sorted(keep, key=lambda s: B.haversine_km(ev["lat"], ev["lon"], meta[s]["lat"], meta[s]["lon"]))[:12]
        res, tr_list = [], []
        for s in near:
            mm = (st == s) & (ep > t_a - B.WIN_S - 1e-6) & (ep < t_b + 1e-6)
            if not mm.any() or not B.covers(np.sort(ep[mm]), t_a, t_b): continue
            idx = np.where(mm)[0][np.argsort(ep[mm])]
            ud = np.concatenate([np.asarray(H["waves"][int(r)][0], float) for r in idx]); e0 = float(ep[idx[0]])
            dist = float(np.hypot(B.haversine_km(ev["lat"], ev["lon"], meta[s]["lat"], meta[s]["lon"]), ev["dep"]))
            i0 = int(round((t_a - e0) * B.FS))
            j = B.sta_lta_first(ud[i0:], i_min=int(round((B.SEG_PRE_S - 1.0) * B.FS)))
            tr = None if j is None else (e0 + (i0 + j) / B.FS) - t0
            if tr is None or len(res) >= B.CLOCK_NSTA: continue
            tp, ts = dist / B.CLOCK_VP, dist / VS
            res.append(tr - tp)
            rows.append(dict(origin_jst=c["origin_jst"][:22], mj=c["mj"], station=s, dist_km=round(dist, 2), trigger_s=round(tr, 2),
                             pred_P_s=round(tp, 2), pred_S_s=round(ts, 2), trig_minus_P_s=round(tr - tp, 2), trig_minus_S_s=round(tr - ts, 2)))
            seg = sosfilt(SOS, ud)[i0:i0 + int((B.SEG_PRE_S + B.SEG_POST_S) * B.FS)]
            tr_list.append((s, dist, seg / (np.max(np.abs(seg)) + 1e-12), tr, tp, ts))
        near_cat = [r for r in cat if -120 <= (r["t"] - ev["t"]).total_seconds() <= 45]
        md = float(np.median(np.abs(res))) if res else None
        summ.append(dict(origin_jst=c["origin_jst"][:22], mj=c["mj"], n=len(res), median_abs_trig_minus_P_s=md,
                         median_trig_minus_P_s=(float(np.median(res)) if res else None),
                         n_trig_closer_to_S=int(sum(1 for r in rows if r["origin_jst"] == c["origin_jst"][:22]
                                                    and abs(r["trig_minus_S_s"]) < abs(r["trig_minus_P_s"]))),
                         nearby_catalog=[dict(dt_s=round((r["t"] - ev["t"]).total_seconds(), 2), mj=r["mag"],
                                              dist_km=round(B.haversine_km(ev["lat"], ev["lon"], r["lat"], r["lon"]), 1)) for r in near_cat]))
        plots.append((c, ev, tr_list, near_cat))

print("\n[21_04c] ===== 局ごと(立ち上がり・予想は発生からの秒) =====")
for r in rows:
    print(f"  {r['origin_jst']} Mj {r['mj']}  {r['station']:<7} 距離 {r['dist_km']:6.2f} km  立ち上がり {r['trigger_s']:6.2f}  "
          f"予想 P {r['pred_P_s']:5.2f}  予想 S {r['pred_S_s']:5.2f}  P との差 {r['trig_minus_P_s']:+6.2f}  S との差 {r['trig_minus_S_s']:+6.2f}")
print("\n[21_04c] ===== 地震ごと =====")
for s in summ:
    f2 = lambda v: "—" if v is None else f"{v:+.2f}"
    print(f"  {s['origin_jst']} Mj {s['mj']}: 局 {s['n']}  |立ち上がり − P| の中央値 {f2(s['median_abs_trig_minus_P_s'])} s  "
          f"(符号付きの中央値 {f2(s['median_trig_minus_P_s'])} s)  S の方に近い局 {s['n_trig_closer_to_S']}/{s['n']}")
    print("     前後の気象庁の震源(発生との差 s・Mj・震央の距離 km): " + ", ".join(f"{q['dt_s']:+.1f}s M{q['mj']} {q['dist_km']}km"
                                                                     for q in s["nearby_catalog"]))
with open(O / "data" / "21_04c_gclock_diagnose.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
json.dump(dict(script="21_04c_ct2016_gclock_diagnose.py", version="v1", h5=str(h5p), b21_04b_version=B.VERSION, vs_kms=VS,
               events=summ), open(O / "data" / "21_04c_gclock_diagnose.json", "w"), indent=1)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
fig, axs = plt.subplots(1, len(plots), figsize=(5.0 * len(plots), 6.4), squeeze=False, gridspec_kw=dict(wspace=0.45))
tt = np.arange(int((B.SEG_PRE_S + B.SEG_POST_S) * B.FS)) / B.FS - B.SEG_PRE_S
for ax, (c, ev, trl, nc) in zip(axs[0], plots):
    for k, (s, dist, y, tr, tp, ts) in enumerate(trl):
        ax.plot(tt[:len(y)], y * 0.42 + k, color="0.35", lw=0.4)
        ax.plot([tp, tp], [k - 0.45, k + 0.45], color="tab:blue", lw=1.4)
        ax.plot([ts, ts], [k - 0.45, k + 0.45], color="tab:red", lw=1.4)
        ax.plot([tr, tr], [k - 0.45, k + 0.45], color="k", lw=1.4, ls="--")
        ax.text(B.SEG_POST_S + 0.5, k, f"{s} {dist:.0f} km", fontsize=7, va="center")
    for q in nc:
        d = (q["t"] - ev["t"]).total_seconds()
        if -B.SEG_PRE_S <= d <= B.SEG_POST_S and abs(d) > 0.05: ax.axvline(d, color="tab:green", lw=1.0, ls=":")   # この地震自身は除く
    ax.set_xlim(-B.SEG_PRE_S, B.SEG_POST_S); ax.set_ylim(-0.7, max(len(trl), 1) - 0.3)
    ax.set_yticks([]); ax.set_xlabel("Time since JMA origin (s)")
    ax.set_title(f"{c['origin_jst'][:19]} JST, Mj {c['mj']}\nmedian |trigger - P| = {c['median_abs_resid_s'] if c['median_abs_resid_s'] is None else round(c['median_abs_resid_s'], 2)} s",
                 fontsize=9)
h = [plt.Line2D([], [], color="tab:blue", lw=1.4), plt.Line2D([], [], color="tab:red", lw=1.4),
     plt.Line2D([], [], color="k", lw=1.4, ls="--"), plt.Line2D([], [], color="tab:green", lw=1.0, ls=":")]
fig.legend(h, ["Predicted P (distance / 6.0 km/s)", f"Predicted S (distance / {VS} km/s)", "STA/LTA trigger used by G-clock",
               "Other JMA origins within the window (any Mj)"], loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.02))
fig.suptitle("Central Tottori 2016: G-clock check, UD traces (1-15 Hz causal band-pass, each normalised), nearest stations bottom", fontsize=10)
fig.subplots_adjust(left=0.02, right=0.93, bottom=0.14, top=0.86, wspace=0.45); (O / "PDF").mkdir(exist_ok=True)
fig.savefig(O / "PDF" / "21_04c_gclock_diagnose.pdf", bbox_inches="tight"); plt.close(fig)
print(f"\n[21_04c] 出力: {O / 'PDF' / '21_04c_gclock_diagnose.pdf'}、{O / 'data' / '21_04c_gclock_diagnose.csv'}、{O / 'data' / '21_04c_gclock_diagnose.json'}")
