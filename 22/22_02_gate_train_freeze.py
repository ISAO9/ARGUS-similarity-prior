#!/usr/bin/env python3
# =============================================================================
# Script : 22_02_gate_train_freeze.py  (v1)
#          [信頼の切り替え G を学習して凍結する: 「物理(C4)と記憶(C1)のどちらを信じるか」を、正解を使わない 13 の手がかりから
#           ロジスティック回帰で決める。鳥取県西部 2026 の行(22_01a)で学習し、models/22_gate.pkl に凍結して SHA-256 を出す]
# Project: ARGUS(新生)— AI を「物理の部品」として使う。22 では AI が「どちらの答えを信じるか」を決める(事前登録 22_00)
#
# 何をするか(全て 22_00 の 1.3・1.4 節のとおり。値の調整はしない):
#   1. data/22_01a_rows_wt2026.npz と models/22_01a_rows.json を読み、照合する(本番の行・G-same PASS・行の SHA-256・手がかりの並び)。
#   2. 学習の行 = C1 がある行(fb = 0)。目的変数 y = 1(C1 の誤差 < C4 の誤差)、重み w = min(|C4 の誤差 − C1 の誤差|, 50 km)を
#      平均 1 にそろえる(sklearn では罰則の強さが重みの合計に比例するので、km の単位に依らず C = 1.0 の意味を決めるため)。
#      C1 と C4 の誤差が同じ行(小数 4 桁で)は重み 0(学習に効かない)。
#   3. 値なしの手がかり(手がかり 9 だけ: P が 3 局未満)は学習の行の中央値で埋め、学習の行の平均と標準偏差(ddof 0。0 の列は 1)で
#      標準化する(どちらも凍結)。手がかり 9 以外が値なしの行があれば STOP(手がかりの計算の誤りを黙って埋めないため)。
#   4. G = LogisticRegression(L2(既定)、C = 1.0、lbfgs、max_iter 1000、class_weight なし)を重み w で学習。収束しなければ STOP。
#      p ≥ 0.5 なら C1、それ以外は C4。
#      C1 が無い行(fb = 1)では G は C4(= M6r)を返す。
#   5. 副(記述だけ): 外れの確率 q = P(G の選んだ答えの誤差 > 10 km)を、同じ手がかりのロジスティック回帰(重みなし)で出す。
#   6. 2026 の中での確かめ(記述だけ。判定しない): pool の地震(本震 + 72 h まで、評価の地震を除く)の行だけで同じ設定の G を学習し、
#      21_02 の評価の地震(既に開いた)で G・C4・C1・規則 R・M6r を比べる(τ ごとの中央値・10 km 超・30 km 超、τ = 2 s で
#      HG1・HG2 と同じ検定を記述として)。
#   7. 凍結: 2026 の全ての学習の行で学習した G を models/22_gate.pkl に保存し、SHA-256 を表示する(22_00 の 7 節に写す)。
#      凍結するファイルは numpy の配列だけ(係数・切片・埋める値・平均・標準偏差。sklearn の版に依らず読める)。JSON にも同じ値を書く。
#      一時ファイルに書き、読み直して同じ判断になることを確かめてから正式の名前に置く。
#      1 回だけ: 既に models/22_gate.pkl があれば上書きせず _rerun_<UTC> の名前に書く(事前登録に使うのは最初のもの)。
#      大阪府北部 2018 のファイル(data/catalog/jma_osaka2018.csv・data/osaka2018_processed/)が既にあれば STOP(凍結は大阪を開く前)。
#   8. 図: PDF/22_02_F1_gate_check.pdf(白背景・英語・凡例は枠外)。
#
# 22 GATE APPLY(印の間)は 22_03・22_04 と 1 字も違わない(SHA-256 を記録し、後で照合する)。
#
# Usage : cd ~/SWIFT && uv run python src/22_02_gate_train_freeze.py          (22_01a の本番の後。数分)
#         cd ~/SWIFT && uv run python src/22_02_gate_train_freeze.py --quick  (22_01a --quick の行で動作確認。凍結しない、出力に _quick)
# 入力  : data/22_01a_rows_wt2026.npz・models/22_01a_rows.json(--quick なら _quick)
# Output: models/22_gate.pkl / models/22_02_train.json / models/22_02_opened.json / PDF/22_02_F1_gate_check.pdf
# 止める条件(STOP): 行が無い・行の SHA-256 が記録と違う・22_01a が G-same PASS でない・22_01a のモードが違う・手がかりの並びが違う・
#                   C1 がある行で C1 か C4 の誤差が無い・手がかり 9 以外が値なし・収束しない・読み直した G の判断が違う・
#                   係数から計算した p が sklearn と違う・大阪のファイルが既にある・scikit-learn が無い
# =============================================================================
import json, argparse, hashlib, pickle, platform, sys, time, datetime as dt
from pathlib import Path
import numpy as np
from scipy.stats import wilcoxon, binomtest

ap = argparse.ArgumentParser()
ap.add_argument("--quick", action="store_true", help="22_01a --quick の行で動作確認(凍結しない、出力に _quick)")
a = ap.parse_args()

VERSION = "v1"
GATE_FEATS = ["log1p_d_C4_C1_km", "log1p_d_C4_M6r_km", "log1p_d_C1_C2_km", "log1p_top10_spread_km", "S_max", "S_gap12",
              "log1p_n_pos", "n_P", "p_resid_C4_s", "C4_at_edge", "n_corr_C4", "tau_s", "log1p_d_C4_lib_km"]
LR = dict(C=1.0, solver="lbfgs", max_iter=1000)   # 22_00 1.3(調整しない)。L2 は既定(penalty を書くと sklearn 1.8 以降で警告が出るので書かない)
W_CAP_KM, MISS_KM, BIG_KM, THR_R_KM, P_CHOOSE = 50.0, 10.0, 30.0, 10.0, 0.5
ALPHA_H, MIN_DISC, MIN_NZ, GUARD_KM, TAU_MAIN, MIN_EV = 0.005, 8, 10, 0.05, 2.0, 30   # 22_00 の 2 節(2026-11-02 に本人が確定)

ROOT = Path(__file__).resolve().parent.parent
for d in ("models", "PDF", "data"): (ROOT / d).mkdir(exist_ok=True)
T0 = time.time()
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def utcnow(): return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SELF_SHA = sha256(Path(__file__))
print(f"[22_02] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…  モード: {'quick(凍結しない)' if a.quick else '本番(G を凍結する)'}")
try:
    import sklearn
    from sklearn.linear_model import LogisticRegression
except ImportError:
    raise SystemExit("[22_02] STOP: scikit-learn が無い(cd ~/SWIFT && uv add scikit-learn)")

# ---------------------------------------------------------------- 1. 行を読んで照合する
Q = "_quick" if a.quick else ""
NPZ, RJ = ROOT / f"data/22_01a_rows_wt2026{Q}.npz", ROOT / f"models/22_01a_rows{Q}.json"
for p in (NPZ, RJ):
    if not p.exists(): raise SystemExit(f"[22_02] STOP: {p.relative_to(ROOT)} が無い(先に 22_01a{' --quick' if a.quick else ''} を回す)")
rec = json.load(open(RJ))
if rec.get("g_same") != "PASS": raise SystemExit(f"[22_02] STOP: 22_01a の G-same が PASS でない({rec.get('g_same')})")
if rec.get("mode") != ("quick" if a.quick else "full"): raise SystemExit(f"[22_02] STOP: 22_01a のモードが違う({rec.get('mode')})")
ROWS_SHA = sha256(NPZ)
if rec.get("rows_sha256") != ROWS_SHA: raise SystemExit("[22_02] STOP: 行の SHA-256 が 22_01a の記録と違う(行が書き換わった)")
if list(rec.get("gate_feats", [])) != GATE_FEATS: raise SystemExit("[22_02] STOP: 手がかりの並びが 22_01a と違う")
D = np.load(NPZ, allow_pickle=False)
if list(D["feats"]) != GATE_FEATS: raise SystemExit("[22_02] STOP: 行の中の手がかりの並びが違う")
X, TAU, FB = D["X"].astype(float), D["tau"].astype(float), D["fb"].astype(int)
E = {m: D[f"err_{m}"].astype(float) for m in ("M6r", "C1", "C2", "C3", "C4")}
POOL, EVAL, OT = D["is_pool"].astype(bool), D["is_eval"].astype(bool), D["origin_time"]
print(f"[22_02] 行: {len(TAU)}(C1 がある行 {int((FB == 0).sum())})  行の SHA-256 {ROWS_SHA[:12]}…(22_01a の記録と同じ)  "
      f"手がかりの部分の SHA-256 {rec['gate_feature_block_sha256'][:12]}…")
OSAKA = [p for p in ("data/catalog/jma_osaka2018.csv", "data/osaka2018_processed") if (ROOT / p).exists()]
if OSAKA and not a.quick: raise SystemExit(f"[22_02] STOP: 大阪府北部 2018 のファイルが既にある {OSAKA}(G は大阪を開く前に凍結する。22_00 の 3 節)")
print(f"[22_02] 大阪府北部 2018 のファイル(data/catalog/jma_osaka2018.csv・data/osaka2018_processed/): {'有る(quick なので続ける)' if OSAKA else '無い'}")
if np.any(FB == 0) and (np.isnan(E["C1"][FB == 0]).any() or np.isnan(E["C4"]).any()):
    raise SystemExit("[22_02] STOP: C1 がある行で C1 の誤差が無い、または C4 の誤差が無い行がある")

# >>> 22 GATE APPLY BEGIN(この印から END までは 22_02・22_03・22_04 で 1 字も違わない)
def gate_fit(Xtr, e1, e4, LRkw, w_cap):
    """G の学習: y = 1(C1 の誤差 < C4 の誤差)、重み min(|e4 − e1|, w_cap)。値なしは学習の行の中央値で埋め、平均と標準偏差で標準化"""
    from sklearn.linear_model import LogisticRegression
    imp = np.nanmedian(Xtr, axis=0); imp = np.where(np.isfinite(imp), imp, 0.0)
    Z = np.where(np.isfinite(Xtr), Xtr, imp[None, :])
    mu = Z.mean(0); sd = Z.std(0); sd = np.where(sd > 0, sd, 1.0)
    y = (e1 < e4).astype(int); w = np.minimum(np.abs(e4 - e1), w_cap); w = w / w.mean()          # 重みは平均 1(C の意味を単位に依らず決める)
    m = LogisticRegression(**LRkw); m.fit((Z - mu) / sd, y, sample_weight=w)
    nit = int(np.max(m.n_iter_))
    if nit >= LRkw["max_iter"]: raise SystemExit(f"[22] STOP: ロジスティック回帰が収束しない(反復 {nit})")
    return dict(imp=imp, mu=mu, sd=sd, model=m, coef=m.coef_[0].astype(float), intercept=float(m.intercept_[0]), n_iter=nit)
def gate_prob(g, Xq):
    """p(C1 の方が近い)。係数から直接計算する(sklearn の版に依らない)。C1 が無い行(手がかりが全て nan)は 0"""
    allnan = np.all(np.isnan(Xq), axis=1); bad = np.isnan(np.delete(Xq, 8, axis=1)).any(axis=1) & ~allnan
    if bad.any(): raise SystemExit(f"[22] STOP: C1 がある行で、手がかり 9 以外が値なしの行が {int(bad.sum())}(手がかりの計算を確かめる)")
    Z = np.where(np.isfinite(Xq), Xq, g["imp"][None, :])
    p = 1.0 / (1.0 + np.exp(-(((Z - g["mu"]) / g["sd"]) @ g["coef"] + g["intercept"])))
    return np.where(allnan, 0.0, p)
def gate_choose(g, Xq, e1, e4, p_choose):
    """G の答えの誤差: p ≥ p_choose なら C1、それ以外(C1 が無い行も)は C4"""
    p = gate_prob(g, Xq); c1 = (p >= p_choose) & np.isfinite(e1)
    return np.where(c1, e1, e4), c1, p
def rule_R(Xq, e1, e4, thr_km):
    """規則 R: C4 と C1 が thr_km 以上食い違えば C1(C1 が無い行は C4)"""
    d = np.expm1(Xq[:, 0]); s = np.isfinite(d) & (d >= thr_km) & np.isfinite(e1)
    return np.where(s, e1, e4), s
# <<< 22 GATE APPLY END
FB_ = open(Path(__file__), encoding="utf-8").read()
APPLY_SHA = hashlib.sha256(FB_[FB_.index("# >>> 22 GATE APPLY BEGIN"):FB_.index("# <<< 22 GATE APPLY END")].encode()).hexdigest()

def verdict(n_ev, n_disc, p1, nz, p2, guard_ok):
    """22_00 の 2 節の判定。評価できる地震 = その τ の全ての地震(C1 が無い地震も G = R = C4 として数える)。
    INCONCLUSIVE: 地震 30 未満か HG1 の食い違う対 8 未満。HG2 の対が 10 未満なら HG2 は成り立たないとして扱う"""
    if n_ev < MIN_EV or n_disc < MIN_DISC: return "INCONCLUSIVE"
    h1 = p1 is not None and p1 < ALPHA_H; h2 = nz >= MIN_NZ and p2 is not None and p2 < ALPHA_H
    if h1 and h2 and guard_ok: return "GATE-CONFIRMED"
    if h1 and guard_ok: return "GATE-HELPS-NOT-BEYOND-RULE"
    return "GATE-NOT-CONFIRMED"
def compare(m, eG, eR):
    """記述用の表: 中央値・10 km 超・30 km 超(M6r・C4・C1・R・G)と、HG1・HG2・守りと同じ検定(記述)"""
    out = {}
    for k, e in (("M6r", E["M6r"][m]), ("C4", E["C4"][m]), ("C1", E["C1"][m]), ("R", eR[m]), ("G", eG[m])):
        f = np.isfinite(e)
        out[k] = dict(n=int(f.sum()), median_km=float(np.median(e[f])) if f.any() else None,
                      gt10=float(np.mean(e[f] > MISS_KM)) if f.any() else None, gt30=float(np.mean(e[f] > BIG_KM)) if f.any() else None)
    g10, c10 = eG[m] > MISS_KM, E["C4"][m] > MISS_KM
    b, c = int(np.sum(c10 & ~g10)), int(np.sum(g10 & ~c10))          # b: C4 だけ外れ、c: G だけ外れ
    hg1 = dict(b_C4_only=b, c_G_only=c, p=(float(binomtest(c, b + c, 0.5, alternative="less").pvalue) if b + c > 0 else None))
    dd = eG[m] - eR[m]; nz = int(np.sum(dd != 0))
    hg2 = dict(n_nonzero=nz, median_diff_km=float(np.median(dd)),
               p=(float(wilcoxon(eG[m], eR[m], alternative="less", zero_method="wilcox", method="approx", correction=False).pvalue)
                  if nz >= 1 else None))
    guard = dict(G_median=float(np.median(eG[m])), C4_median=float(np.median(E["C4"][m])),
                 ok=bool(np.median(eG[m]) <= np.median(E["C4"][m]) + GUARD_KM))
    out.update(HG1_like=hg1, HG2_like=hg2, guard_like=guard,
               would_be=verdict(int(m.sum()), b + c, hg1["p"], nz, hg2["p"], guard["ok"]))
    return out
def fp(p): return "—" if p is None else f"{p:.2g}"

# ---------------------------------------------------------------- 2. 2026 の中での確かめ(記述だけ)
TR = FB == 0
CHECK = None
if (TR & POOL).sum() >= 30 and EVAL.any():
    gA = gate_fit(X[TR & POOL], E["C1"][TR & POOL], E["C4"][TR & POOL], LR, W_CAP_KM)
    eGA, chA, pA = gate_choose(gA, X, E["C1"], E["C4"], P_CHOOSE); eRA, swA = rule_R(X, E["C1"], E["C4"], THR_R_KM)
    CHECK = {}
    print(f"\n[22_02] ===== 2026 の中での確かめ(記述。pool の行 {int((TR & POOL).sum())} で学習、21_02 の評価の地震 "
          f"{len(set(OT[EVAL]))} 個は既に開いた) =====")
    for t in sorted(set(TAU)):
        m = EVAL & (TAU == t)
        if not m.any(): continue
        d = compare(m, eGA, eRA); d["frac_G_chooses_C1"] = float(chA[m].mean()); d["frac_R_chooses_C1"] = float(swA[m].mean())
        CHECK[f"{t:g}"] = d
        print(f"  τ={t:g} s  n={int(m.sum())}  中央値 M6r {d['M6r']['median_km']:.2f} / C4 {d['C4']['median_km']:.2f} / C1 {d['C1']['median_km']:.2f} / "
              f"R {d['R']['median_km']:.2f} / G {d['G']['median_km']:.2f} km   10 km 超 C4 {d['C4']['gt10']:.1%} / R {d['R']['gt10']:.1%} / "
              f"G {d['G']['gt10']:.1%}   G が C1 を選ぶ {d['frac_G_chooses_C1']:.1%}" +
              (f"   [記述] HG1 型 C4 だけ外れ {d['HG1_like']['b_C4_only']}・G だけ外れ {d['HG1_like']['c_G_only']} p {fp(d['HG1_like']['p'])}  "
               f"HG2 型 差が 0 でない {d['HG2_like']['n_nonzero']} p {fp(d['HG2_like']['p'])}  守り {'OK' if d['guard_like']['ok'] else 'NG'}  "
               f"→ (記述、判定ではない){d['would_be']}" if t == TAU_MAIN else ""))
else:
    print("[22_02] 注意: pool の学習の行が 30 未満か評価の行が無いので、2026 の中での確かめを飛ばした")

# ---------------------------------------------------------------- 3. 凍結する G(2026 の全ての学習の行)
if TR.sum() < 30: raise SystemExit(f"[22_02] STOP: 学習の行が {int(TR.sum())}(30 未満)")
g = gate_fit(X[TR], E["C1"][TR], E["C4"][TR], LR, W_CAP_KM)
eG, ch, pG = gate_choose(g, X, E["C1"], E["C4"], P_CHOOSE); eR, sw = rule_R(X, E["C1"], E["C4"], THR_R_KM)
y = (E["C1"][TR] < E["C4"][TR]).astype(int); w = np.minimum(np.abs(E["C4"][TR] - E["C1"][TR]), W_CAP_KM)     # km(表示用)
acc_w = float(np.sum(w * ((pG[TR] >= P_CHOOSE) == (y == 1))) / max(np.sum(w), 1e-12))
# 副: 外れの確率 q(G の選んだ答えが 10 km 超か。重みなし。記述だけ)
yq = (eG[TR] > MISS_KM).astype(int); QH = None
if 0 < yq.sum() < len(yq):
    Zq = (np.where(np.isfinite(X[TR]), X[TR], g["imp"][None, :]) - g["mu"]) / g["sd"]
    mq = LogisticRegression(**LR); mq.fit(Zq, yq)
    QH = dict(coef=mq.coef_[0].astype(float), intercept=float(mq.intercept_[0]), base_rate=float(yq.mean()), n_iter=int(np.max(mq.n_iter_)))
print(f"\n[22_02] 凍結する G: 学習の行 {int(TR.sum())}(y = 1 の割合 {y.mean():.1%}、重みの合計 {w.sum():.0f} km)  "
      f"反復 {g['n_iter']}  重み付きの正解率(学習の行の中、楽観的) {acc_w:.1%}  学習の行で G が C1 を選ぶ割合 {ch[TR].mean():.1%}(R は {sw[TR].mean():.1%})")
print("[22_02] 係数(標準化した手がかり。正 = C1 を信じる側): " +
      "  ".join(f"{f} {c:+.2f}" for f, c in sorted(zip(GATE_FEATS, g["coef"]), key=lambda kv: -abs(kv[1]))) + f"  切片 {g['intercept']:+.2f}")
print(f"[22_02] 副(外れの確率 q): " + ("学習できなかった(10 km 超が 0 か全て)" if QH is None else f"基準率 {QH['base_rate']:.1%}(記述だけ)"))

SUF = Q
OPEN = ROOT / "models/22_02_opened.json"
if not a.quick and (ROOT / "models/22_gate.pkl").exists():
    SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
    print(f"[22_02] 注意: 凍結した G は既にある。上書きせず {SUF} の名前に書く(事前登録に使うのは最初のもの)")
def log_open(status):
    r = json.load(open(OPEN)) if OPEN.exists() else []
    r.append(dict(utc=utcnow(), status=status, version=VERSION, script_sha256=SELF_SHA, suffix=SUF)); json.dump(r, open(OPEN, "w"), indent=1)
if not a.quick: log_open("started")
FROZEN = dict(version=VERSION, gate_feats=GATE_FEATS, imp=g["imp"], mu=g["mu"], sd=g["sd"], coef=g["coef"], intercept=g["intercept"],
              n_iter=g["n_iter"], p_choose=P_CHOOSE, thr_R_km=THR_R_KM, q_head=QH, lr=LR, w_cap_km=W_CAP_KM,
              gate_feature_block_sha256=rec["gate_feature_block_sha256"], gate_apply_block_sha256=APPLY_SHA, rows_sha256=ROWS_SHA,
              sklearn=sklearn.__version__, numpy=np.__version__)
MP = ROOT / f"models/22_gate{SUF}.pkl"; TMP = MP.with_suffix(".pkl.tmp")
with open(TMP, "wb") as f: pickle.dump(FROZEN, f)
# 読み直して同じ判断になるか・係数から計算した p が sklearn と同じか(凍結の確かめ。確かめてから正式の名前に置く)
with open(TMP, "rb") as f: g2 = pickle.load(f)
if not np.array_equal(gate_prob(g2, X) >= P_CHOOSE, pG >= P_CHOOSE): raise SystemExit("[22_02] STOP: 読み直した G の判断が違う")
pk_sk = g["model"].predict_proba((np.where(np.isfinite(X[TR]), X[TR], g["imp"][None, :]) - g["mu"]) / g["sd"])[:, 1]
if np.max(np.abs(pk_sk - pG[TR])) > 1e-9: raise SystemExit("[22_02] STOP: 係数から計算した p が sklearn と違う")
TMP.replace(MP)
MODEL_SHA = sha256(MP)
print(f"[22_02] 凍結: {MP.relative_to(ROOT)}  SHA-256 {MODEL_SHA}")
print(f"[22_02] 22 GATE APPLY の部分の SHA-256 {APPLY_SHA}")

out = dict(script="22_02_gate_train_freeze.py", version=VERSION, script_sha256=SELF_SHA, mode=("quick" if a.quick else "train"),
           rows_path=str(NPZ.relative_to(ROOT)), rows_sha256=ROWS_SHA, rows_record_sha256=sha256(RJ),
           gate_feature_block_sha256=rec["gate_feature_block_sha256"], gate_apply_block_sha256=APPLY_SHA, model_path=str(MP.relative_to(ROOT)),
           model_sha256=MODEL_SHA, gate_feats=GATE_FEATS, lr=LR, w_cap_km=W_CAP_KM, p_choose=P_CHOOSE, thr_R_km=THR_R_KM,
           impute=dict(zip(GATE_FEATS, map(float, g["imp"]))), mean=dict(zip(GATE_FEATS, map(float, g["mu"]))),
           std=dict(zip(GATE_FEATS, map(float, g["sd"]))), coef=dict(zip(GATE_FEATS, map(float, g["coef"]))), intercept=g["intercept"],
           n_iter=g["n_iter"], weights="min(|e4 - e1|, 50 km) normalised to mean 1", wilcoxon_method="approx, correction=False",
           osaka_files_present_at_freeze=OSAKA,
           n_train_rows=int(TR.sum()), frac_y1=float(y.mean()), weighted_train_accuracy=acc_w,
           frac_choose_C1_train=float(ch[TR].mean()), frac_R_C1_train=float(sw[TR].mean()),
           q_head=(None if QH is None else dict(coef=dict(zip(GATE_FEATS, map(float, QH["coef"]))), intercept=QH["intercept"], base_rate=QH["base_rate"])),
           check_2026_descriptive=CHECK, sklearn=sklearn.__version__, numpy=np.__version__, python=platform.python_version(), utc=utcnow(),
           suffix=SUF, runtime_s=time.time() - T0,
           limits=["trained on one sequence (West Tottori 2026); the 2026 check is descriptive (evaluation events opened in 21_02, same sequence)",
                   "truth and past locations are JMA hypocentres; C1 can only return known past locations",
                   "hyperparameters fixed in advance (22_00 section 1.3); no tuning or cross-validated selection",
                   "the test (22_04) is Northern Osaka 2018, once, after this model and 22_00 are pushed and timestamped"])
JP = ROOT / f"models/22_02_train{SUF}.json"
json.dump(out, open(JP, "w"), indent=1, ensure_ascii=False)
print(f"[22_02] 学習の記録: {JP.relative_to(ROOT)}  SHA-256 {sha256(JP)}")

# ---------------------------------------------------------------- 4. 図(白背景・英語・凡例は枠外)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 10, "pdf.fonttype": 42})
fig, axs = plt.subplots(1, 2, figsize=(11.5, 4.6), gridspec_kw=dict(width_ratios=[1.0, 1.0]))
ax = axs[0]
COL = {"M6r": "#9AA0A6", "C4": "#E040FB", "C1": "#1E88E5", "R": "#111111", "G": "#00897B"}
LAB = {"M6r": "Best physics (M6r)", "C4": "C4 (physics + similar events + station terms)", "C1": "C1 (most similar past event)",
       "R": "Fixed rule R (switch to C1 if C4-C1 >= 10 km)", "G": "Trust gate G (learned)"}
if CHECK:
    ts = sorted(CHECK, key=float); xx = np.arange(len(ts)); wbar = 0.16
    for i, k in enumerate(["M6r", "C4", "C1", "R", "G"]):
        vals = [100 * CHECK[t][k]["gt10"] for t in ts]
        ax.bar(xx + (i - 2) * wbar, vals, wbar, color=COL[k], label=LAB[k], edgecolor="white", linewidth=0.5)
        for xv, v in zip(xx + (i - 2) * wbar, vals):          # 0 % の棒も見えるように値を書く
            ax.text(xv, v, f"{v:.0f}", ha="center", va="bottom", fontsize=6, color="0.25")
    ax.set_xticks(xx); ax.set_xticklabels([f"{t} s" for t in ts]); ax.margins(y=0.15)
    ax.set_xlabel("Time since the first P pick, tau"); ax.set_ylabel("Events with error > 10 km (%)")
    ax.set_title(f"(a) West Tottori 2026 check, {len(set(OT[EVAL]))} events (descriptive; G trained on the pool only)", fontsize=9.5)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8)
else:
    ax.text(0.5, 0.5, "2026 check skipped (too few pool rows)", ha="center", va="center", transform=ax.transAxes); ax.set_axis_off()
ax.grid(alpha=0.3, axis="y")
ax = axs[1]; srt = sorted(zip(GATE_FEATS, g["coef"]), key=lambda kv: kv[1])
ax.barh(np.arange(len(srt)), [c for _, c in srt], color=["#1E88E5" if c > 0 else "#E040FB" for _, c in srt])
ax.set_yticks(np.arange(len(srt))); ax.set_yticklabels([f for f, _ in srt], fontsize=8); ax.axvline(0, color="0.3", lw=0.8)
ax.set_xlabel("Coefficient (standardised; > 0 trusts C1, < 0 trusts C4)")
ax.set_title(f"(b) Frozen gate G: {int(TR.sum())} training rows", fontsize=9.5); ax.grid(alpha=0.3, axis="x")
fig.tight_layout(); fig.savefig(ROOT / f"PDF/22_02_F1_gate_check{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
print(f"[22_02] 図: PDF/22_02_F1_gate_check{SUF}.pdf  ({time.time() - T0:.0f} s)")
if not a.quick: log_open(f"completed: model {MODEL_SHA}")
print("[22_02] 次: " + ("問題なければ 22_01a の本番の後に、--quick を外して回す" if a.quick else
                        "この出力(特に SHA-256 の行)を貼る。22_00 の 7 節に書いて push・外部の時刻の記録 → その後に 21_20(大阪)"))
