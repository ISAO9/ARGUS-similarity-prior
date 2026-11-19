#!/usr/bin/env python3
# =============================================================================
# Script : 25_09_shimane2018_flag_descriptive.py  (v1)
#          [記述(判定に使わない): 島根県西部 2018 の試験の地震を、気象庁の震源決定の印で「手動(K・k・S・s)」と「自動(A・a)」に
#           分け、25_05 の誤差(BEST・C3・C4、τ までの検測の BEST・C3)の中央値と、C3 対 BEST の対の比べ(記述の p)を並べる]
# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の記述
# 新しく書いたもの(派生元なし)。事前登録 25 で凍結する(9 節)。
#
# なぜ要るか:
#   25_00 の数え上げで、島根の試験の候補(R1 の見積もりの後、カタログだけ)41 のうち 25 が気象庁の自動の震源(印 A)だった
#   (K 15・k 1)。これまでの系列は、ほとんどが手動の震源だった(長野 2014 は Mj ≥ 1.5 の全てが K)。正解(試験の地震の震源)と
#   過去の地震の位置の一部が自動の震源になるので、「C3 の勝ち負けが自動の震源の誤差に引っ張られていないか」を査読で問われうる。
#   そこで、印で分けた誤差を、結果を見る前に決めた形で記述として出す。検定にはしない(仮説も α も無い。分けた後の数が少ない)。
#
# 何をするか:
#   1. 25_05 の本番の data/25_05_per_event.csv と models/25_05_judgment.json(--dev では _dev)を読む。25_08 と同じ確かめ
#      (凍結した 25_05 v1 の SHA-256 SHA_2505・--ref-suffix・INCONCLUSIVE なら止める)。
#   2. 25_01 の jma_shimane2018.csv(--catalog)を読み、CSV の各行(試験の地震)の自分の行を、25_03h と同じ見つけ方
#      (キャッシュの時刻 = 日本時間を 0.1 s で切り捨てたもの、と Mj が一致する、ただ 1 つの行)で見つけて、震源決定の印を取る。
#      見つからないか 2 行以上なら止める。
#   3. 印で 手動(K・k・S・s)/自動(A・a)/その他 に分け、τ = 0.5・2 s の BEST(25_05 の per_tau[τ]["C3"]["best"]。H1 と同じ選び方を
#      全ての試験の地震で行ったもの)・C3・C4 と、25_05 の H5 が評価された時は τ までの検測の BEST・C3 の、数・中央値を出す。
#      τ = 2 s の C3 対 BEST は、組ごとに 片側の対応 Wilcoxon(zero_method='wilcox')の p(差が 0 でない組が 10 以上の時だけ。25_05 と同じ)・
#      差が 0 でない組の数・C3 が小さい組の割合を記述として出す(H1 の判定の代わりにはしない)。
#   4. 出力: models/25_09_flag_descriptive.json・PDF/25_09_F1_errors_by_flag.pdf(--dev では _dev)。
#
# 限界: 印は気象庁の震源の作り方を表すだけで、震源の誤差の大きさそのものではない。組ごとの数は少ない(25_00 の見積もりで手動 16・自動 25)。
#   BEST は全ての試験の地震で選んだもので、組ごとには選び直さない。対は 25_05 の CSV の 4 桁の値で比べるので、組「all」の
#   差が 0 でない組の数と p は、25_05 の H1 の値と同じになるとは限らない(H1 の判定は 25_05 の値)。
#
# Usage : cd ~/SWIFT && uv run python src/25_09_shimane2018_flag_descriptive.py        (25_05 の本番の後。25_08 の後に回す)
#         cd ~/SWIFT && uv run python src/25_09_shimane2018_flag_descriptive.py --dev  (25_05 の dev の後。配管の確かめ)
#         cd ~/SWIFT && uv run python src/25_09_shimane2018_flag_descriptive.py --selftest
# 入力  : data/25_05_per_event.csv・models/25_05_judgment.json・models/25_05_opened.json・data/shimane2018_processed/jma_shimane2018.csv
# =============================================================================
import json, csv, hashlib, argparse, sys, datetime as dt
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
TAG = "[25_09]"
ap = argparse.ArgumentParser()
ap.add_argument("--dev", action="store_true", help="25_05 の dev の出力で回す(配管の確かめ)")
ap.add_argument("--ref-suffix", default="", help="25_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
ap.add_argument("--catalog", default="data/shimane2018_processed/jma_shimane2018.csv", help="25_01 の出力(日本時間・全ての規模・印の列 det_flag)")
ap.add_argument("--selftest", action="store_true")
A = ap.parse_args()
SHA_2505 = "80309ce7012b89af0c052e225cb66b2e15ee104af247937b63510064f9c11398"                          # 事前登録 25 で凍結する 25_05 v1 の SHA-256(25_06f・25_06g・25_08 と同じ照合)
TAUS = ["0.5", "2"]
MIN_NONZERO = 10                                   # 25_05 と同じ: 差が 0 でない組が 10 未満なら p を出さない
MANUAL, AUTO = {"K", "k", "S", "s"}, {"A", "a"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def utc_naive(o):
    """25_03h と同じ: キャッシュの origin_time(UTC の文字列)を、タイムゾーンなしの UTC の datetime にする"""
    s = str(o).strip().replace("T", " ").replace("Z", "")
    if "+" in s[10:]: s = s[:10] + s[10:].split("+")[0]
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try: return datetime.strptime(s[:26], fmt)
        except ValueError: pass
    sys.exit(f"{TAG} STOP: origin_time {o!r} を時刻として読めない")


def read_catalog(path):
    """25_03h と同じ読み方。戻り値: (時刻を 0.1 s で切り捨てたもの, Mj) -> [印, ...]"""
    idx = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            ts = row["time"].strip()
            t21 = datetime.strptime(ts[:21].ljust(21, "0"), "%Y-%m-%d %H:%M:%S.%f")
            mg = row.get("mag", "").strip()
            try: mjv = float(mg) if mg else None
            except ValueError: mjv = None
            if mjv is None: continue
            idx.setdefault((t21, round(mjv, 3)), []).append(row.get("det_flag", "_").strip() or "_")
    return idx


def flag_of(idx, origin_utc_str, mj):
    tj = utc_naive(origin_utc_str) + timedelta(hours=9)
    key = (tj.replace(microsecond=(tj.microsecond // 100000) * 100000), round(float(mj), 3))
    rows = idx.get(key, [])
    if len(rows) != 1: sys.exit(f"{TAG} STOP: 試験の地震 {origin_utc_str}(Mj {mj})の震源一覧の行が {len(rows)} 個(1 個のはず)")
    return rows[0]


def group(f):
    return "manual (K, k, S, s)" if f in MANUAL else "automatic (A, a)" if f in AUTO else "other"


def selftest():
    import tempfile, os
    def check(c, m):
        if not c: sys.exit(f"{TAG} STOP: selftest に失敗: {m}")
    d = tempfile.mkdtemp(); p = os.path.join(d, "c.csv")
    with open(p, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time", "latitude", "longitude", "depth_km", "mag", "det_flag"])
        w.writerow(["2018-04-12 10:00:05.37", "35.1", "132.5", "10.00", "1.7", "A"])
        w.writerow(["2018-04-12 10:00:09.91", "35.1", "132.5", "10.00", "1.7", "K"])
        w.writerow(["2018-04-12 11:00:00.00", "35.1", "132.5", "10.00", "1.6", "_"])
    idx = read_catalog(p)
    check(flag_of(idx, "2018-04-12 01:00:05.300000", 1.7) == "A", "0.1 s の切り捨てで自分の行(A)")
    check(flag_of(idx, "2018-04-12 01:00:09.900000", 1.7) == "K", "自分の行(K)")
    check(group("A") == "automatic (A, a)" and group("k") == "manual (K, k, S, s)" and group("_") == "other", "組の分け方")
    print(f"{TAG} selftest: 自分の行の見つけ方(25_03h と同じ)・組の分け方の 3 例に合格")


selftest()
if A.selftest: sys.exit(0)
from scipy.stats import wilcoxon
SELF_SHA = sha256(Path(__file__))
print(f"{TAG} 本スクリプト v1 SHA-256 {SELF_SHA[:12]}…")
for d in ("models", "PDF"): (ROOT / d).mkdir(exist_ok=True)
SFX = "_dev" if A.dev else ""
RSFX = "_dev" if A.dev else A.ref_suffix
p5, j5, pc = ROOT / f"data/25_05_per_event{RSFX}.csv", ROOT / f"models/25_05_judgment{RSFX}.json", ROOT / A.catalog
if not j5.exists(): sys.exit(f"{TAG} STOP: {j5.relative_to(ROOT)} が無い(25_05 の後に回す。やり直した時は --ref-suffix を渡す)")
J5 = json.load(open(j5))
if J5.get("verdict") == "INCONCLUSIVE":
    sys.exit(f"{TAG} STOP: 25_05 の判定が INCONCLUSIVE(評価できる試験の地震が 30 未満)で CSV が無いため、計算しない(事前登録 25 の 2 節)")
for p in (p5, pc):
    if not p.exists(): sys.exit(f"{TAG} STOP: {p} が無い")
if J5.get("script_sha256") != SHA_2505: sys.exit(f"{TAG} STOP: 25_05 の結果が、凍結した 25_05 v1(SHA-256 {SHA_2505[:12]}…)のものでない")
if not A.dev:
    _O = ROOT / "models/25_05_opened.json"
    _c = [r for r in (json.load(open(_O)) if _O.exists() else []) if str(r.get("status", "")).startswith("completed")]
    if not _c or _c[0].get("suffix", "") != RSFX or J5.get("suffix", "") != RSFX:
        sys.exit(f"{TAG} STOP: --ref-suffix '{RSFX}' が、models/25_05_opened.json で最初に completed になった 25_05 の実行と違う")
rows = list(csv.DictReader(open(p5)))
if len(rows) != int(J5["n_evaluated"]): sys.exit(f"{TAG} STOP: CSV の行の数 {len(rows)} が n_evaluated {J5['n_evaluated']} と違う")
IDX = read_catalog(pc)
FL = [flag_of(IDX, r["origin_time"], r["mj"]) for r in rows]
GR = np.array([group(f) for f in FL])
H5_OK = bool(J5.get("causal", {}).get("evaluated", False))
print(f"{TAG} 入力: {p5.name}(SHA-256 {sha256(p5)[:12]}…)  {len(rows)} 地震  25_05 の判定 {J5.get('verdict')}  震源一覧 {pc.name}(SHA-256 {sha256(pc)[:12]}…)")
print(f"{TAG} 印の数: " + "  ".join(f"{f} {FL.count(f)}" for f in sorted(set(FL))) + "  → 組: " +
      "  ".join(f"{g} {int((GR == g).sum())}" for g in ("manual (K, k, S, s)", "automatic (A, a)", "other")))


def col(name):
    return np.array([float(r[name]) if r.get(name, "") not in ("", None) else np.nan for r in rows])


OUT = dict(groups={}, paired_C3_vs_BEST_tau2={})
GROUPS = ["all", "manual (K, k, S, s)", "automatic (A, a)", "other"]
for t in TAUS:
    bo = J5["per_tau"][t]["C3"]["best"]
    M = [("BEST", f"{bo}_err_t{t}", bo), ("C3", f"C3_err_t{t}", "C3"), ("C4", f"C4_err_t{t}", "C4")]
    if H5_OK:
        bc = J5["causal"]["per_tau"][t]["C3"]["best"]
        M += [("BEST, causal picks", f"{bc}_causal_err_t{t}", bc), ("C3, causal picks", f"C3_causal_err_t{t}", "C3")]
    for lab, cname, mname in M:
        e = col(cname)
        for g in GROUPS:
            m = np.isfinite(e) & ((GR == g) if g != "all" else np.ones(len(e), bool))
            OUT["groups"].setdefault(g, {})[f"tau{t}_{lab}"] = dict(method=mname, column=cname, n=int(m.sum()),
                                                                     median_km=(float(np.median(e[m])) if m.any() else None))
bo2 = J5["per_tau"]["2"]["C3"]["best"]
eb, ec = np.round(col(f"{bo2}_err_t2"), 4), np.round(col("C3_err_t2"), 4)        # 25_05 の CSV と同じく 4 桁で比べる
for g in GROUPS:
    m = np.isfinite(eb) & np.isfinite(ec) & ((GR == g) if g != "all" else np.ones(len(eb), bool))
    d = ec[m] - eb[m]; nz = int((d != 0).sum())
    p = (float(wilcoxon(ec[m], eb[m], zero_method="wilcox", alternative="less").pvalue) if nz >= MIN_NONZERO else None)   # 25_05 と同じく 10 組未満は出さない
    OUT["paired_C3_vs_BEST_tau2"][g] = dict(best=bo2, n=int(m.sum()), n_nonzero=nz, p_one_sided_descriptive=p,
                                             share_C3_smaller=(float((d < 0).mean()) if m.any() else None))
f3 = lambda x: "—" if x is None else f"{x:.3f}"
for t in TAUS:
    print(f"{TAG} τ = {t} s(中央値 km、組ごとの数):")
    for k in [k for k in OUT["groups"]["all"] if k.startswith(f"tau{t}_")]:
        print("   " + f"{k[len(f'tau{t}_'):]:>20s}  " + "  ".join(f"{g}: {f3(OUT['groups'][g][k]['median_km'])}(n={OUT['groups'][g][k]['n']})" for g in GROUPS))
print(f"{TAG} τ = 2 s の C3 対 BEST({bo2})の記述(判定ではない): " +
      "  ".join(f"{g}: 差が 0 でない組 {v['n_nonzero']}・片側 p {f3(v['p_one_sided_descriptive'])}・C3 が小さい割合 {f3(v['share_C3_smaller'])}"
                for g, v in OUT["paired_C3_vs_BEST_tau2"].items()))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
G3 = ["manual (K, k, S, s)", "automatic (A, a)"]
fig, axs = plt.subplots(1, 2, figsize=(11, 4.4))
for ax, t in zip(axs, TAUS):
    keys = [k for k in OUT["groups"]["all"] if k.startswith(f"tau{t}_")]
    x = np.arange(len(keys)); bw = 0.38
    for j, (g, c) in enumerate(zip(G3, ("tab:blue", "tab:orange"))):
        v = [OUT["groups"][g][k]["median_km"] or 0.0 for k in keys]
        b = ax.bar(x + (j - 0.5) * bw, v, bw, color=c, label=f"{g} hypocentres")
        for xi, k in zip(x, keys):
            ax.text(xi + (j - 0.5) * bw, (OUT["groups"][g][k]["median_km"] or 0.0) * 1.01, f"n={OUT['groups'][g][k]['n']}", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x); ax.set_xticklabels([k[len(f"tau{t}_"):] for k in keys], rotation=20, ha="right")
    ax.set_title(f"tau = {t} s", fontsize=10); ax.grid(alpha=0.3, axis="y")
    top = max([OUT["groups"][g][k]["median_km"] or 0.0 for g in G3 for k in keys] + [1e-3]); ax.set_ylim(0, top * 1.18)
    ax.set_ylabel("Median epicentral error vs JMA (km)")
h_, l_ = axs[0].get_legend_handles_labels()
fig.legend(h_, l_, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.02), fontsize=9)
fig.suptitle("Western Shimane 2018" + (" (DEV)" if A.dev else "") + ": errors by JMA hypocentre flag of the test event (descriptive)", fontsize=10)
fig.tight_layout(rect=(0, 0.08, 1, 0.95))
fig.savefig(ROOT / f"PDF/25_09_F1_errors_by_flag{SFX}.pdf", bbox_inches="tight"); plt.close(fig)
json.dump(dict(script="25_09_shimane2018_flag_descriptive.py", version="v1", script_sha256=SELF_SHA,
               utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               inputs=dict(csv=p5.name, csv_sha256=sha256(p5), judgment=j5.name, judgment_sha256=sha256(j5), script_25_05_sha256=J5.get("script_sha256"),
                           ref_suffix=RSFX, catalog=pc.name, catalog_sha256=sha256(pc), h5_evaluated=H5_OK),
               flags=dict(manual=sorted(MANUAL), automatic=sorted(AUTO), counts={f: FL.count(f) for f in sorted(set(FL))}),
               results=OUT, descriptive_only=True,
               limits=["the flag describes how JMA produced the hypocentre, not its error", "groups are small",
                       "BEST is the one chosen on all test events (as in H1), not re-chosen per group",
                       "p values are descriptive (no hypothesis, no alpha, no multiplicity control)",
                       "pairs are compared on the 4-decimal values of the 25_05 CSV, so n_nonzero and p of the group 'all' need not equal H1's values in 25_05"]),
          open(ROOT / f"models/25_09_flag_descriptive{SFX}.json", "w"), indent=1)
print(f"{TAG} 出力: models/25_09_flag_descriptive{SFX}.json・PDF/25_09_F1_errors_by_flag{SFX}.pdf")
