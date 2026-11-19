#!/usr/bin/env python3
# =============================================================================
# Script : 24_07_causal_picks.py  (v3)
# v3(2026-11-15、長野県北部 2014 の本番用に凍結する版。検測・選び方・まとめ方は v1・v2 と 1 字も変えていない):
#   (1) --all-events: dev の選び方(本震 + 72 h より後の Mj ≥ 2.0 の最初の 30)を使わず、キャッシュの P を測った全ての地震で回す
#       (24_05 の dev と本番が、pool の地震と試験の地震の両方で、τ までの検測を使うため)。--label で表示と図の系列の名前を変える。
#   (3) JSON: --all-events・元の値に戻した時は、dev の選び方と鳥取県西部 2026 の h5 の限界の文を、その実行に当てはまる文に替える。
#       CSV の SHA-256(csv_sha256)を JSON に書く(24_05 が、読む CSV が同じ実行のものかを照らす)。説明の文を v3 に合わせた。
#   (2) h5 に win_mean・win_std(24_02 が書く、z-score の前の窓ごと成分ごとの平均と標準偏差)があれば、z × win_std + win_mean で
#       元の値に戻してから窓を切る。これで、T を含む h5 の窓の尺度に T より後のサンプルが混じる問題が無くなる(鳥取県西部 2026 の
#       h5 には無いので、v2 と同じく z-score のまま使い、限界に書く)。JSON の raw_reconstructed に、どちらだったかを書く。
# v2(2026-11-15、v1 の初めての Colab 実行で STOP した点を直した。検測・選び方・まとめ方は v1 と同じ):
#   (1) PhaseNet("original") の成分の並びは ENZ だった(v1 は ZNE を前提にして STOP)。21_20c のオフラインの検測は
#       SeisBench の classify が局の成分の名前(Z・N・E)から model.component_order の並びに並べ替えて渡している。v2 は
#       同じことを直接行う(UD → Z、NS → N、EW → E を component_order の並びに並べ替えて PhaseNet に渡す)。
#   (2) 窓の索引: 渡した h5_index.npz が今の h5 のものでない時、v1 は毎回作り直していた(約 20 分)。v2 は作り直した索引を
#       --base の下の data/h5_index_<h5 の名前>.npz に保存し、次からはそれを読む(元の h5_index.npz は書き換えない)。
#          [τ までの波形だけで PhaseNet を回し直し、「その時点で本当に手に入る P・S」の表を作る(H5 の材料)。
#           v1 は鳥取県西部 2026 での dev(配管・所要時間・オフラインの検測との違いの記述)だけに使う]
# Project: ARGUS(新生)— 4 つ目の系列(長野県北部 2014、24 系)の H5「τ までの波形だけで検測しても結論が変わらないか」の準備
#
# なぜ必要か:
#   21_02・21_04・21_20 の検測は、地震ごとに [発生 − 10 s, 発生 + 45 s] の記録全体に PhaseNet を当てた「オフラインの検測」で、
#   τ の時点ではまだ届いていない波形も PhaseNet が見ている(τ より後の P・S は使わないが、τ より前の P の時刻の決まり方に、
#   後の波形が効いている可能性がある)。査読では「実時間の検測ならもっと悪いはず」と問われる。そこで、時刻 T(= 一番早い P + τ)
#   までのサンプルだけで PhaseNet を回し、その時点で決まる P・S を作る。v1・v2 は凍結の前の dev(鳥取県西部 2026)だけに使った。
#   v3 は --all-events で長野県北部 2014 の本番の材料を作る(24 の Colab N15。24_05 を開く前に 1 回だけ回す)。
#
# 何をするか(地震ごと・τ ごと・キャッシュの局ごと):
#   1. τ の起点 TFIRST は 21_20 と同じ(キャッシュの P のうち PhaseNet で測った(p_fallback = 0)一番早い P。発生時刻からの s)。
#      時刻 T = TFIRST + τ(発生時刻からの s)。τ = 0.5・1・2・3 s(21_20 の TAUS と同じ)。
#      限界: 起点 TFIRST だけはオフラインの検測から決める(起点まで実時間にすると定義が循環するため。論文に書く)。
#   2. h5 から、その局の [T − 30.00 s, T] の 3001 サンプル(PhaseNet の窓の長さ)を切り出す。h5 は 30 s の窓ごとに読むので
#      T を含む h5 の窓は全体を読むが、T より後のサンプルは切り捨てて PhaseNet にも検測にも渡さない(G-causal で確かめる:
#      selftest では T より後を書き換えても検測が同じこと、実データでは窓の最後のサンプルが h5 の時刻 T のサンプルそのもので
#      あること)。PhaseNet の前処理は SeisBench の annotate_batch_pre(窓ごとに平均を引き、成分ごとの標準偏差で割る)で、
#      窓の中のサンプル(= T まで)だけを使う。T で終わる窓を 1 つだけ使い、それより前に終わる窓の結果とは重ねない
#      (オフラインの検測は、重なった窓の予測を重ねている)。
#   3. 確率が 0.3 以上の区間ごとに、最大の点を検測とする(SeisBench の picks_from_annotations と同じ考え方)。ただし、最大の点が
#      窓の終わり(T)から 0.10 s 以内のものは使わない(その時点ではまだ「最大」と言えないため。確定の遅れ N_CONF = 10 サンプル)。
#   4. 選び方は 21_20c と同じ「最早」: 発生時刻の 10 s 前より後の、確率 0.3 以上で一番早い P を取り、それが発生時刻から
#      0.5〜30 s の外なら、その局は P なし(21_20c は外れた局を捨てる)。その P より 0.3 s より後で一番早い S(確率 0.3 以上)を
#      取り、S − P が 0.3〜15 s の外なら S なし(21_20c と同じ)。発生時刻からの 0.5〜30 s と −10 s は、カタログの発生時刻を
#      使う(実時間では分からない。オフラインの検測と同じ条件にするため。限界に書く)。21_20c の和達の QC と、PhaseNet で
#      取れない時の STA/LTA の代わり(fallback)は、時点ごとには行わない(限界に書く)。
#   5. 局はキャッシュの局(一番早い P から最大 24 局。21_20c が選んだもの)に限る(限界に書く)。キャッシュの局は座標で
#      観測点の一覧(stations.csv)と照らして局の名前に戻す。
#
# 出力(記述だけ。判定はしない):
#   data/24_07_causal_picks{tag}.csv … 地震 × τ × 局ごとの、オフラインの P・S と、T までで決まる P・S
#   models/24_07_causal_picks{tag}.json … τ ごとのまとめ(届いていた P のうち T までに取れた割合・時刻の差・余計な P の数・S も同じ・
#                                       所要時間)、入力の SHA-256、規則
#   PDF/24_07_causal_picks{tag}.pdf … τ ごとの取れた割合と、時刻の差の中央値・90%(白背景・英語・凡例は枠の外)
#   取れた割合は 2 通り出す: 分母を「T までに届いていたオフラインの P」にしたもの(主)と、「T − 0.10 s までに届いていた P」
#   にしたもの(確定の遅れの分を除いたもの)。
#
# dev の地震(--all-events を付けない時。鳥取県西部 2026 の dev で使った):
#   キャッシュの本震(Mj 最大)+ 72 h より後の、Mj ≥ 2.0 の地震を時刻順に最初から --max-events 個(既定 30)。
#   21_02 の試験(本震 + 72 h より後の 1.5 ≤ Mj < 2.0)とは重ならない(21_02 の試験の地震は使わない)。
#
# 鳥取県西部 2026 の h5 についての限界(dev の値を読む時に添える):
#   h5 の波形は 30 s の窓ごとに z-score で正規化済み(15_01d)。PhaseNet は自分の窓の中で標準偏差で割り直すが、T を含む
#   h5 の窓の尺度は、その h5 の窓の T より後のサンプルからも決まっている(尺度だけ。波形の形は T まで)。長野の h5(24_02)には
#   窓ごとの平均と標準偏差(win_mean・win_std)を保存し、v3 は元の値に戻してから窓を切って、この点を無くす。
# 実時間との違い(dev の値を読む時に添える): 「T までのサンプルが揃っている」ことは「時刻 T に手元にある」ことと同じではない
#   (伝送の遅れを入れていない。21_20 の限界の「遅れなし」と同じ)。
#
# 止める条件(STOP): h5・キャッシュ・観測点の一覧が無い / キャッシュの形が違う / dev の地震が 0 / キャッシュの局が観測点の一覧に
#   見つからない局が 10% を超える / origin_time が読めない / h5 の window_epoch が float64 でない / 検測の行が 0 /
#   G-causal(selftest: T より後を書き換えても検測が同じ。実データ: 窓の最後のサンプルが h5 の時刻 T のサンプル)に失敗 /
#   PhaseNet の成分の並びが Z・N・E の並べ替えでない / selftest に失敗(本番の前にも必ず selftest を回す)。
#
# Usage(長野県北部 2014 の本番: 24_STEPS_JA.md の N15。下は鳥取県西部 2026 の dev: 24_07_COLAB_STEPS_JA.md のセル C1〜C5):
#   !python /content/drive/MyDrive/ARGUS/src/24_07_causal_picks.py --selftest
#   !python /content/drive/MyDrive/ARGUS/src/24_07_causal_picks.py \
#       --h5 /content/drive/MyDrive/2026WTottori/data/waves/tottori_all_100Hz.h5 \
#       --cache /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt \
#       --stations /content/drive/MyDrive/ARGUS/data/catalog/stations.csv \
#       --index /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/h5_index.npz \
#       --base /content/drive/MyDrive/ARGUS_24 --tag _wt2026_dev --max-events 30
# =============================================================================
import argparse, csv, hashlib, json, sys, time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

VERSION = "v3"
TAG = "[24_07]"
FS = 100.0
NWIN = 3001                       # PhaseNet の窓(SeisBench PhaseNet の in_samples)
TAUS = [0.5, 1.0, 2.0, 3.0]       # 21_20 と同じ
PN_PROB_MIN = 0.3                 # 21_20c と同じ
N_CONF = 10                       # 窓の終わりから 0.10 s 以内の最大は使わない(確定の遅れ)
TP_QC = (0.5, 30.0)               # 21_20c と同じ(発生時刻からの P)
SEG_PRE = 10.0                    # 21_20c と同じ(検測のセグメントは発生の 10 s 前から)
SP_QC = (0.3, 15.0)               # 21_20c と同じ
S_AFTER_P = 0.3                   # 21_20c と同じ(P より 0.3 s 以上後の S)
MATCH_S = 0.5                     # オフラインの検測と「同じ相」とみなす時刻の差(記述用)
POOL_H, DEV_MIN_MJ = 72.0, 2.0
JST_OFFSET_S = 9 * 3600.0


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------- 検測(純粋な関数。selftest で試す)
def peaks_from_prob(p, thr=PN_PROB_MIN, n_conf=N_CONF):
    """確率の列 p(長さ NWIN)から、thr 以上の区間ごとの最大の点 (添字, 値) を返す。最大の点が終わりから n_conf サンプル以内なら捨てる"""
    p = np.asarray(p, float)
    above = p >= thr
    out, i, n = [], 0, len(p)
    while i < n:
        if not above[i]:
            i += 1; continue
        j = i
        while j < n and above[j]: j += 1
        k = i + int(np.argmax(p[i:j]))
        if k <= n - 1 - n_conf: out.append((k, float(p[k])))
        i = j
    return out


def select_ps(p_peaks, s_peaks, t_win0_rel):
    """21_20c と同じ最早の選び方。p_peaks・s_peaks は (添字, 値)、t_win0_rel は窓の最初のサンプルの時刻(発生時刻からの s)。
    返り値: (tp, p_prob, ts, s_prob)。無ければ nan"""
    tp = pp = ts = sp_ = np.nan
    P = sorted((t_win0_rel + k / FS, v) for k, v in p_peaks)
    P = [x for x in P if x[0] >= -SEG_PRE]                      # 21_20c のセグメントは発生の 10 s 前から
    if not P or not (TP_QC[0] <= P[0][0] <= TP_QC[1]):          # 一番早い P が外れたら P なし(21_20c と同じ順)
        return tp, pp, ts, sp_
    tp, pp = P[0]
    S = sorted((t_win0_rel + k / FS, v) for k, v in s_peaks)
    S = [x for x in S if x[0] > tp + S_AFTER_P]
    if S and SP_QC[0] <= S[0][0] - tp <= SP_QC[1]:              # 一番早い S の S − P が外れたら S なし(21_20c と同じ)
        ts, sp_ = S[0]
    return tp, pp, ts, sp_


def comp_perm(order):
    """PhaseNet の component_order(例 'ENZ')に合わせて、UD・NS・EW の並び (0, 1, 2) を並べ替える添字を返す(Z = UD、N = NS、E = EW)"""
    m = {"Z": 0, "N": 1, "E": 2}
    if sorted(order) != ["E", "N", "Z"]: sys.exit(f"{TAG} STOP: PhaseNet の成分の並び {order!r} が Z・N・E の並べ替えでない")
    return [m[c] for c in order]


class PhaseNetRunner:
    """SeisBench PhaseNet("original") を、窓 1 つずつ(バッチ)で直接回す。前処理は annotate_batch_pre(平均を引き、成分ごとの
    標準偏差で割る)。出力は (バッチ, 3, NWIN) の確率で、並びは model.labels"""
    def __init__(self):
        import torch, seisbench.models as sbm
        self.torch = torch
        self.m = sbm.PhaseNet.from_pretrained("original"); self.m.eval()
        self.dev = "cuda" if torch.cuda.is_available() else "cpu"; self.m.to(self.dev)
        lab = list(self.m.labels)
        self.iP, self.iS = lab.index("P"), lab.index("S")
        self.order = getattr(self.m, "component_order", "ZNE")
        self.perm = comp_perm(self.order)
        import seisbench
        self.version = seisbench.__version__
        print(f"{TAG} PhaseNet('original') 読込(SeisBench {self.version}、labels {self.m.labels}、成分の並び {self.order} → "
              f"UD・NS・EW を {[('UD', 'NS', 'EW')[i] for i in self.perm]} の順に並べ替えて渡す、{self.dev})")

    def __call__(self, X):
        """X: (B, 3, NWIN)、成分は UD・NS・EW の順。PhaseNet の component_order の並びに並べ替えて渡す。返り値: (P の確率, S の確率)"""
        torch = self.torch
        with torch.no_grad():
            b = torch.as_tensor(np.ascontiguousarray(np.asarray(X)[:, self.perm], np.float32), device=self.dev)
            b = self.m.annotate_batch_pre(b, {})
            y = self.m(b).detach().cpu().numpy()
        return y[:, self.iP, :], y[:, self.iS, :]


# ---------------------------------------------------------------- h5 の窓の索引と切り出し(21_20c と同じ作り)
class H5Reader:
    def __init__(self, h5_path, index_path=None, save_path=None):
        import h5py
        self.H5 = h5py.File(h5_path, "r", rdcc_nbytes=64 << 20)
        co = self.H5.attrs.get("channel_order", "UD,NS,EW")
        self.order = (co.decode() if isinstance(co, bytes) else str(co)).split(",")
        self.nsamp = int(self.H5.attrs.get("n_samples", 3000))
        if self.H5["window_epoch"].dtype != np.float64:
            sys.exit(f"{TAG} STOP: h5 の window_epoch が {self.H5['window_epoch'].dtype}(float64 でないと epoch の刻みが粗く、窓が壊れる)")
        st_raw = self.H5["stations"][:]; ep_raw = self.H5["window_epoch"][:]
        st_arr = np.array([s.decode() if isinstance(s, bytes) else str(s) for s in st_raw])
        fp = hashlib.sha1("\n".join(st_arr.tolist()).encode() + np.asarray(ep_raw, np.float64).tobytes()).hexdigest()
        ok = False
        for ip in [x for x in (index_path, save_path) if x]:
            if not Path(ip).exists(): continue
            z = np.load(ip, allow_pickle=True)
            ok = ("fp" in z.files) and (str(z["fp"]) == fp)
            print(f"{TAG} 窓の索引 {ip}: " + ("今の h5 のもの(読込)" if ok else "今の h5 のものでない"))
            if ok:
                names, ptr, self.ep, self.row_idx = list(z["names"]), z["ptr"], z["ep"], z["row"]; break
        if not ok:
            if index_path or save_path: print(f"{TAG} 窓の索引を作り直す(初回だけ。数十分かかりうる)")
            o = np.lexsort((ep_raw, st_arr)); st_s = st_arr[o]
            self.ep, self.row_idx = ep_raw[o], o.astype(np.int64)
            names, starts = np.unique(st_s, return_index=True); names = list(names); ptr = np.append(starts, len(st_s))
            if save_path:
                Path(save_path).parent.mkdir(parents=True, exist_ok=True)
                np.savez(save_path, names=np.array(names, object), ptr=ptr, ep=self.ep, row=self.row_idx, fp=np.array(fp))
                print(f"{TAG} 作り直した索引を保存: {save_path}(次からはこれを読む)")
        self.slice = {n: (int(ptr[i]), int(ptr[i + 1])) for i, n in enumerate(names)}
        self.ci = [self.order.index(c) for c in ("UD", "NS", "EW")]
        self.raw = ("win_mean" in self.H5) and ("win_std" in self.H5)       # v3: 24_02 の h5 なら元の値に戻せる
        self.rows_cache = {}            # h5 の行の読み直しを避ける(地震ごとに空にする)

    def row(self, r):
        r = int(r)
        if r not in self.rows_cache:
            x = np.asarray(self.H5["waves"][r], np.float64)
            if self.raw:                                                 # v3: z × 標準偏差 + 平均(成分ごと)で元の値に戻す
                x = x * np.asarray(self.H5["win_std"][r], np.float64)[:, None] + np.asarray(self.H5["win_mean"][r], np.float64)[:, None]
            self.rows_cache[r] = x[self.ci].astype(np.float32)
        return self.rows_cache[r]

    def sample_at(self, sta, t):
        """局 sta の、絶対秒 t のサンプル (3,)(UD・NS・EW)を、h5 の行と添字から直接読む(実データの G-causal 用)"""
        a, b = self.slice[sta]; ep = self.ep[a:b]; rows = self.row_idx[a:b]
        j = np.where((ep <= t + 1e-6) & (ep + self.nsamp / FS > t + 1e-6))[0]
        if len(j) != 1: return None
        return self.row(rows[j[0]])[:, int(round((t - ep[j[0]]) * FS))]

    def window_ending(self, sta, t_end):
        """局 sta の、絶対秒 t_end で終わる NWIN サンプル (3, NWIN)(UD・NS・EW)。覆えなければ None。T より後のサンプルは
        h5 の窓ごと読むが、切り捨てて返さない"""
        if sta not in self.slice: return None
        a, b = self.slice[sta]; ep = self.ep[a:b]; rows = self.row_idx[a:b]
        t_beg = t_end - (NWIN - 1) / FS
        span = self.nsamp / FS
        sel = (ep > t_beg - span - 1e-6) & (ep <= t_end + 1e-6)
        if not sel.any(): return None
        ep_s, rows_s = ep[sel], rows[sel]; o = np.argsort(ep_s); ep_s, rows_s = ep_s[o], rows_s[o]
        if ep_s[0] > t_beg + 1e-3 or ep_s[-1] + span < t_end - 1e-3: return None
        if len(ep_s) > 1 and np.any(np.abs(np.diff(ep_s) - span) > 0.02): return None
        t0 = float(ep_s[0]); n_tot = int(round((ep_s[-1] + span - t0) * FS))
        seg = np.zeros((3, n_tot), np.float32)
        for e_, r in zip(ep_s, rows_s):
            off = int(round((e_ - t0) * FS)); seg[:, off:off + self.nsamp] = self.row(r)
        i_end = int(round((t_end - t0) * FS))
        if i_end - (NWIN - 1) < 0 or i_end + 1 > n_tot: return None
        return seg[:, i_end - (NWIN - 1): i_end + 1].copy()


# ---------------------------------------------------------------- 本体
def run(h5r, picker, EVS, ev_idx, sta_code_of, frame_offset_s):
    """地震ごと・τ ごと・局ごとに、T までの窓で P・S を決める。返り値: 行の一覧"""
    rows = []
    for ie in ev_idx:
        e = EVS[ie]; n = int(e["n_real_stations"])
        tp = np.asarray(e["tp_times"], float)[:n]; sp = np.asarray(e["sp_diffs"], float)[:n]
        pf = np.asarray(e["p_fallback"]).astype(int)[:n]; sf = np.asarray(e["s_fallback"]).astype(int)[:n]
        okp = np.isfinite(tp) & (pf == 0)
        if not okp.any(): continue
        tfirst = float(tp[okp].min())
        o_ep = origin_epoch(e["origin_time"]) + frame_offset_s
        h5r.rows_cache = {}
        for tau in TAUS:
            T = tfirst + tau
            X, ks = [], []
            for k in range(n):
                code = sta_code_of[ie][k]
                w = None if code is None else h5r.window_ending(code, o_ep + T)
                if w is None:            # 局の照合に失敗か、h5 の窓が欠けている(取れなかったとは数えない)
                    rows.append(dict(event=int(ie), origin_time=str(e["origin_time"]), mj=float(e["mw"]), tau=tau, k=int(k),
                                     station=code, window_ok=0, tfirst=tfirst, T=T,
                                     off_tp=float(tp[k]), off_pf=int(pf[k]), off_sp=float(sp[k]), off_sf=int(sf[k]),
                                     c_tp=np.nan, c_pprob=np.nan, c_ts=np.nan, c_sprob=np.nan))
                    continue
                X.append(w); ks.append(k)
            if not X: continue
            PP, SS = picker(np.stack(X))
            t_win0 = T - (NWIN - 1) / FS
            for j, k in enumerate(ks):
                ctp, cpp, cts, csp = select_ps(peaks_from_prob(PP[j]), peaks_from_prob(SS[j]), t_win0)
                rows.append(dict(event=int(ie), origin_time=str(e["origin_time"]), mj=float(e["mw"]), tau=tau, k=int(k),
                                 station=sta_code_of[ie][k], window_ok=1, tfirst=tfirst, T=T,
                                 off_tp=float(tp[k]), off_pf=int(pf[k]), off_sp=float(sp[k]), off_sf=int(sf[k]),
                                 c_tp=ctp, c_pprob=cpp, c_ts=cts, c_sprob=csp))
    return rows


def origin_epoch(o):
    s = str(o).strip().replace("T", " ").replace("Z", "")
    if "+" in s[10:]: s = s[:10] + s[10:].split("+")[0]
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc).timestamp()
        except ValueError:
            pass
    raise SystemExit(f"{TAG} STOP: origin_time {o!r} を読めない")


def summarize(rows):
    S = {}
    for tau in TAUS:
        R0 = [r for r in rows if r["tau"] == tau]
        R = [r for r in R0 if r["window_ok"] == 1]
        if not R: continue
        evs = sorted({r["event"] for r in R})
        arrived = [r for r in R if r["off_pf"] == 0 and np.isfinite(r["off_tp"]) and r["off_tp"] <= r["T"] + 1e-4]
        arrived_c = [r for r in arrived if r["off_tp"] <= r["T"] - N_CONF / FS + 1e-4]   # 確定の遅れの分を除いた分母
        matched = [r for r in arrived if np.isfinite(r["c_tp"]) and abs(r["c_tp"] - r["off_tp"]) <= MATCH_S]
        dt = np.array([r["c_tp"] - r["off_tp"] for r in matched])
        mid = {id(r) for r in matched}
        c_any = [r for r in R if np.isfinite(r["c_tp"])]
        extra = [r for r in c_any if id(r) not in mid]
        s_off = [r for r in arrived if r["off_sf"] == 0 and np.isfinite(r["off_sp"]) and r["off_tp"] + r["off_sp"] <= r["T"] + 1e-4]
        s_m = [r for r in s_off if np.isfinite(r["c_ts"]) and abs(r["c_ts"] - (r["off_tp"] + r["off_sp"])) <= MATCH_S]
        c_s = [r for r in R if np.isfinite(r["c_ts"])]
        per_ev_off = [sum(1 for r in arrived if r["event"] == ie) for ie in evs]
        per_ev_c = [sum(1 for r in c_any if r["event"] == ie) for ie in evs]
        first_rows = [r for r in R if abs(r["off_tp"] - r["tfirst"]) < 1e-6 and r["off_pf"] == 0]   # 一番早い局の窓が作れた地震だけ
        first_ok = [id(r) in mid for r in first_rows]
        n_conf_m = sum(1 for r in arrived_c if id(r) in mid)
        S[f"{tau:g}"] = dict(
            n_events=len(evs), n_station_windows=len(R),
            p_arrived_offline=len(arrived), p_matched=len(matched),
            p_recall=(len(matched) / len(arrived) if arrived else None),
            p_arrived_offline_before_T_minus_conf=len(arrived_c),
            p_recall_excluding_confirmation_delay=(n_conf_m / len(arrived_c) if arrived_c else None),
            station_windows_unavailable=len(R0) - len(R),
            p_dt_median_s=(float(np.median(dt)) if len(dt) else None),
            p_absdt_median_s=(float(np.median(np.abs(dt))) if len(dt) else None),
            p_absdt_p90_s=(float(np.percentile(np.abs(dt), 90)) if len(dt) else None),
            p_causal_total=len(c_any), p_causal_not_matching_an_arrived_offline_p=len(extra),
            p_per_event_offline_median=float(np.median(per_ev_off)), p_per_event_causal_median=float(np.median(per_ev_c)),
            first_station_detected_frac=(float(np.mean(first_ok)) if first_ok else None), first_station_events=len(first_ok),
            s_usable_offline=len(s_off), s_matched=len(s_m), s_recall=(len(s_m) / len(s_off) if s_off else None),
            s_causal_total=len(c_s))
    return S


def build_station_map(EVS, ev_idx, stations_csv, h5r):
    meta = []
    with open(stations_csv) as f:
        for r in csv.DictReader(f):
            meta.append((r["id"].strip(), float(r["latitude"]), float(r["longitude"])))
    codes = {ie: [] for ie in ev_idx}; n_all = n_miss = 0
    for ie in ev_idx:
        e = EVS[ie]; n = int(e["n_real_stations"]); L = np.asarray(e["sta_locs"], float)[:n]
        for k in range(n):
            n_all += 1
            d = [(abs(la - L[k, 0]) + abs(lo - L[k, 1]), c) for c, la, lo in meta]
            dm, c = min(d)
            if dm > 2e-3 or (h5r is not None and c not in h5r.slice):
                codes[ie].append(None); n_miss += 1
            else:
                codes[ie].append(c)
    return codes, n_all, n_miss


def figure(S, out_pdf, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 10})
    t = [float(k) for k in S]; fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.2))
    nz = lambda v: np.nan if v is None else v
    a1.plot(t, [nz(S[k]["p_recall"]) for k in S], "o-", color="#0072B2", label="P (offline P arrived by T)")
    a1.plot(t, [nz(S[k]["p_recall_excluding_confirmation_delay"]) for k in S], "o:", color="#0072B2",
            label="P (offline P arrived by T − 0.1 s)")
    a1.plot(t, [S[k]["s_recall"] if S[k]["s_recall"] is not None else np.nan for k in S], "s--", color="#D55E00", label="S (offline S arrived by T)")
    a1.set_xlabel("τ after the first P (s)"); a1.set_ylabel("Fraction also picked with data up to T only"); a1.set_ylim(0, 1.05)
    a1.grid(alpha=0.3); a1.set_title("Causal picks (data up to T only)", fontsize=10)
    a2.plot(t, [nz(S[k]["p_absdt_median_s"]) for k in S], "o-", color="#009E73", label="median |Δt| (P)")
    a2.plot(t, [nz(S[k]["p_absdt_p90_s"]) for k in S], "o:", color="#009E73", label="90th percentile |Δt| (P)")
    a2.set_xlabel("τ after the first P (s)"); a2.set_ylabel("|causal P − offline P| (s), matched picks"); a2.grid(alpha=0.3)
    a2.set_title("Timing difference of matched P picks", fontsize=10)
    h1, l1 = a1.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels()
    fig.legend(h1 + h2, l1 + l2, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.0), fontsize=9)
    fig.suptitle(title, fontsize=11); fig.tight_layout(rect=(0, 0.13, 1, 0.95)); fig.savefig(out_pdf, bbox_inches="tight"); plt.close(fig)


# ---------------------------------------------------------------- selftest(作りものの h5・キャッシュ・PhaseNet の代わり)
def selftest():
    import tempfile, h5py
    def chk(c, m):
        if not c: sys.exit(f"{TAG} STOP: selftest に失敗: {m}")
    # 検測の関数
    p = np.zeros(NWIN); p[100:130] = np.linspace(0.31, 0.9, 30); p[130:160] = np.linspace(0.9, 0.31, 30)
    p[NWIN - 5] = 0.95
    pk = peaks_from_prob(p); chk(len(pk) == 1 and pk[0][0] == 129, f"peaks {pk}")
    tp, pp, ts, sp_ = select_ps([(1000, 0.5), (400, 0.4)], [(1020, 0.9), (1300, 0.8)], -5.0)
    chk(np.isnan(tp) and np.isnan(ts), f"select-1 {tp} {ts}")   # 一番早い P(−1 s)が 0.5〜30 s の外 → P なし(21_20c と同じ。次の P に移らない)
    tp, pp, ts, sp_ = select_ps([(1000, 0.5), (300, 0.4)], [(1020, 0.9), (1300, 0.8)], -15.0)
    chk(np.isnan(tp), f"select-2 {tp}")                        # −12 s の P は −10 s より前で無視、次の −5 s が一番早い → 外れなので P なし
    tp, pp, ts, sp_ = select_ps([(1600, 0.5), (200, 0.4)], [(1620, 0.9), (1900, 0.8)], -15.0)
    chk(abs(tp - 1.0) < 1e-9 and abs(ts - 4.0) < 1e-9, f"select-3 {tp} {ts}")   # −13 s は無視、P = 1.0 s、S は P + 0.3 s より後(1.2 s は捨て 4.0 s)
    tp, pp, ts, sp_ = select_ps([(1600, 0.5)], [(1700, 0.9), (3000, 0.8)], -15.0)
    chk(abs(tp - 1.0) < 1e-9 and abs(ts - 2.0) < 1e-9, f"select-4 {tp} {ts}")   # 一番早い S(S − P = 1 s)
    tp, pp, ts, sp_ = select_ps([(100, 0.5)], [(2000, 0.9)], 0.0)
    chk(abs(tp - 1.0) < 1e-9 and np.isnan(ts), f"select-5 {tp} {ts}")   # S − P = 19 s > 15 → S なし
    chk(comp_perm("ENZ") == [2, 1, 0] and comp_perm("ZNE") == [0, 1, 2], "comp_perm")
    Xc = np.stack([np.full((3, 4), v) for v in (10.0, 20.0)]); Xc[:, 0] += 0; Xc[:, 1] += 1; Xc[:, 2] += 2
    chk(np.array_equal(Xc[:, comp_perm("ENZ")][:, 0], Xc[:, 2]), "comp_perm apply (E は EW)")
    # 作りものの h5(5 局、30 s 窓、JST の epoch)
    tmp = Path(tempfile.mkdtemp())
    o_utc = datetime(2026, 1, 20, 3, 0, 0, tzinfo=timezone.utc).timestamp(); o_jst = o_utc + JST_OFFSET_S
    stas = [f"N.S{i}" for i in range(5)]; tP = [3.0, 3.6, 4.2, 5.0, 6.5]; tS = [5.2, 6.2, 7.3, 8.7, 11.4]
    g0 = (int(o_jst) // 30) * 30 - 120; nw = 10; rng = np.random.default_rng(0)
    W, ST, EP = [], [], []
    for i, s in enumerate(stas):
        for w in range(nw):
            t0 = g0 + 30 * w; x = rng.normal(0, 0.01, (3, 3000)).astype(np.float32)
            tt = t0 + np.arange(3000) / FS - o_jst
            x[0, tt >= tP[i]] += 1.0; x[2, tt >= tS[i]] += 1.0
            x[1] = tt.astype(np.float32)                 # NS には発生時刻からの時刻を書く(窓の端の時刻を確かめるため)
            W.append(x); ST.append(s.encode()); EP.append(float(t0))
    h5p = tmp / "mock.h5"
    with h5py.File(h5p, "w") as H:
        H["waves"] = np.stack(W); H["stations"] = np.array(ST); H["window_epoch"] = np.array(EP)
        H.attrs["channel_order"] = "UD,NS,EW"; H.attrs["n_samples"] = 3000
    with open(tmp / "st.csv", "w") as f:
        f.write("id,latitude,longitude,elevation\n")
        for i, s in enumerate(stas): f.write(f"{s},{35 + 0.1 * i:.4f},{133 + 0.1 * i:.4f},100\n")
    ev = dict(origin_time=datetime.fromtimestamp(o_utc, timezone.utc).replace(tzinfo=None), mw=2.3, n_real_stations=5,
              tp_times=np.array(tP), sp_diffs=np.array(tS) - np.array(tP), p_fallback=np.zeros(5, int), s_fallback=np.zeros(5, int),
              sta_locs=np.array([[35 + 0.1 * i, 133 + 0.1 * i, 0.1] for i in range(5)]))
    class Stub:   # 「段の始まり」で確率が立つ PhaseNet の代わり(窓の中だけを見る)。渡された窓を全部覚える
        def __init__(self): self.seen = []
        def __call__(self, X):
            self.seen.append(np.array(X))
            B = X.shape[0]; P = np.zeros((B, NWIN)); S = np.zeros((B, NWIN))
            for b in range(B):
                for arr, c in ((P, 0), (S, 2)):
                    d = np.abs(np.diff(X[b, c])); idx = np.where(d > 0.5)[0]
                    if len(idx):
                        k = idx[0] + 1; lo, hi = max(0, k - 20), min(NWIN, k + 21)
                        arr[b, lo:hi] = 0.9 * np.exp(-0.5 * ((np.arange(lo, hi) - k) / 5.0) ** 2)
            return P, S
    h5r = H5Reader(h5p)
    codes, n_all, n_miss = build_station_map([ev], [0], tmp / "st.csv", h5r)
    chk(n_miss == 0 and codes[0] == stas, f"station map {codes}")
    st1 = Stub(); rows = run(h5r, st1, [ev], [0], codes, JST_OFFSET_S)
    R = {(r["tau"], r["k"]): r for r in rows}
    # 窓の端の時刻: どの窓も最後のサンプルが T、最初が T − 30.00 s(NS に書いた時刻で確かめる)
    for j, tau in enumerate(TAUS):
        T = 3.0 + tau; Xs = st1.seen[j]
        chk(np.allclose(Xs[:, 1, -1], T, atol=1e-4) and np.allclose(Xs[:, 1, 0], T - (NWIN - 1) / FS, atol=1e-4),
            f"window edges tau {tau}: {Xs[:, 1, -1]} {Xs[:, 1, 0]}")
    # τ = 3 s → T = 6.0: 局 0〜3 の P は T − 0.1 s より前(5.0 まで)なので取れる、局 4(6.5)は取れない
    for k in range(4): chk(abs(R[(3.0, k)]["c_tp"] - tP[k]) < 0.011, f"tau3 k{k} {R[(3.0, k)]['c_tp']}")
    chk(not np.isfinite(R[(3.0, 4)]["c_tp"]), "tau3 k4 should be missing")
    # τ = 0.5 s → T = 3.5: 局 0 だけ(3.0)。局 1(3.6)は T より後
    chk(abs(R[(0.5, 0)]["c_tp"] - 3.0) < 0.011 and not np.isfinite(R[(0.5, 1)]["c_tp"]), "tau0.5")
    # S: τ = 3 s(T = 6.0)で局 0(5.2)は取れる、局 1(6.2)は取れない
    chk(abs(R[(3.0, 0)]["c_ts"] - 5.2) < 0.011 and not np.isfinite(R[(3.0, 1)]["c_ts"]), "S")
    # 確定の遅れ: P がちょうど T − 0.05 s にある局は取れない(τ = 0.55 s 相当を直接確かめる)
    w = h5r.window_ending("N.S0", o_jst + 3.05); PP, _ = Stub()(w[None]); chk(len(peaks_from_prob(PP[0])) == 0, "N_CONF")
    # G-causal: τ ごとに、その τ の T より後のサンプルを書き換えた h5 でも、PhaseNet に渡す窓と P・S が同じ
    for j, tau in enumerate(TAUS):
        T = 3.0 + tau; h5q = tmp / f"mock_perturbed_{j}.h5"
        with h5py.File(h5p, "r") as H0, h5py.File(h5q, "w") as H:
            X = H0["waves"][:]
            H["stations"] = H0["stations"][:]; H["window_epoch"] = H0["window_epoch"][:]
            for k_, v_ in H0.attrs.items(): H.attrs[k_] = v_
            for i in range(len(X)):
                tt = EP[i] + np.arange(3000) / FS - o_jst; m_ = tt > T + 1e-6
                X[i][:, m_] = rng.normal(0, 50, (3, int(m_.sum())))
            H["waves"] = X
        st2 = Stub(); rows2 = run(H5Reader(h5q), st2, [ev], [0], codes, JST_OFFSET_S)
        R2 = {(r["tau"], r["k"]): r for r in rows2 if r["tau"] == tau}
        for key, r in R.items():
            if key[0] != tau: continue
            for c in ("c_tp", "c_ts"):
                a_, b_ = r[c], R2[key][c]
                chk((np.isnan(a_) and np.isnan(b_)) or a_ == b_, f"G-causal tau {tau} {key} {c} {a_} {b_}")
        chk(np.array_equal(st1.seen[j], st2.seen[j]), f"G-causal tau {tau}: PhaseNet に渡した窓が、T より後を書き換えた h5 で変わった")
    # 実データ用の確かめ(窓の最後のサンプル = h5 の時刻 T のサンプル)
    w_ = h5r.window_ending("N.S2", o_jst + 4.37); s_ = h5r.sample_at("N.S2", o_jst + 4.37)
    chk(s_ is not None and np.array_equal(w_[:, -1], s_), "sample_at")
    S = summarize(rows); chk(S["3"]["p_recall"] == 1.0 and S["0.5"]["p_arrived_offline"] == 1 and S["3"]["first_station_detected_frac"] == 1.0,
                             f"summary {S['3']} {S['0.5']}")
    # 窓の無い局(照合に失敗)は「取れなかった」に数えない
    codes_x = {0: list(codes[0])}; codes_x[0][1] = None
    Sx = summarize(run(h5r, Stub(), [ev], [0], codes_x, JST_OFFSET_S))
    chk(Sx["3"]["station_windows_unavailable"] == 1 and Sx["3"]["p_recall"] == 1.0, f"unavailable {Sx['3']}")
    # v3: win_mean・win_std があれば元の値に戻す(成分ごと。h5 の並び UD,NS,EW から読む並びへの並べ替えの後も正しいこと)
    h5r_ = tmp / "mock_raw.h5"
    with h5py.File(h5p, "r") as H0, h5py.File(h5r_, "w") as H:
        for k_ in ("waves", "stations", "window_epoch"): H[k_] = H0[k_][:]
        for k_, v_ in H0.attrs.items(): H.attrs[k_] = v_
        n_ = H0["waves"].shape[0]
        H["win_mean"] = np.tile(np.array([5.0, -3.0, 7.0], np.float32), (n_, 1)); H["win_std"] = np.tile(np.array([2.0, 0.5, 4.0], np.float32), (n_, 1))
    rr = H5Reader(h5r_); z0 = np.asarray(h5py.File(h5p, "r")["waves"][3], np.float64)
    chk(rr.raw and np.allclose(rr.row(3), (z0 * np.array([2.0, 0.5, 4.0])[:, None] + np.array([5.0, -3.0, 7.0])[:, None]).astype(np.float32)),
        "raw reconstruction")
    chk(not H5Reader(h5p).raw, "raw flag without win_std")
    print(f"{TAG} selftest: 元の値への戻し(v3)・成分の並べ替え(ENZ)・検測の関数・最早の選び方(21_20c と同じ順)・窓の端の時刻(最後が T)・確定の遅れ・局の照合・"
          f"G-causal(T より後を書き換えても、PhaseNet に渡す窓と P・S が同じ)・窓の無い局の扱いに全て合格")


def main():
    ap = argparse.ArgumentParser(description="24_07: τ までの波形だけで PhaseNet を回し直す(H5 の材料。dev は鳥取県西部 2026、本番は長野県北部 2014 で --all-events)")
    ap.add_argument("--h5"); ap.add_argument("--cache"); ap.add_argument("--stations")
    ap.add_argument("--index", default="", help="任意: 15_01c が作った h5_index.npz(今の h5 のものなら読む)")
    ap.add_argument("--base", default="/content/drive/MyDrive/ARGUS_24")
    ap.add_argument("--tag", default="_wt2026_dev")
    ap.add_argument("--max-events", type=int, default=30)
    ap.add_argument("--h5-time-base", choices=["jst", "utc"], default="jst", help="鳥取県西部 2026 の h5 は JST(15_01d)")
    ap.add_argument("--all-events", action="store_true", help="v3: キャッシュの P を測った全ての地震(長野の本番用)")
    ap.add_argument("--label", default="West Tottori 2026", help="v3: 表示と図の系列の名前")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    selftest()
    if a.selftest: return
    for p in (a.h5, a.cache, a.stations):
        if not p or not Path(p).exists(): sys.exit(f"{TAG} STOP: {p} が無い(--h5・--cache・--stations を必ず渡す)")
    import torch
    base = Path(a.base)
    for d in ("data", "models", "PDF"): (base / d).mkdir(parents=True, exist_ok=True)
    SELF = sha256(Path(__file__)); CSHA = sha256(a.cache)
    print(f"{TAG} 本スクリプト {VERSION} SHA-256 {SELF[:12]}…  キャッシュ SHA-256 {CSHA[:12]}…")
    EVS = torch.load(a.cache, map_location="cpu", weights_only=False)
    need = ["origin_time", "mw", "sta_locs", "sp_diffs", "tp_times", "p_fallback", "s_fallback", "n_real_stations"]
    for e in EVS:
        miss = [k for k in need if k not in e]
        if miss: sys.exit(f"{TAG} STOP: キャッシュの地震に {miss} が無い")
    OT = np.array([origin_epoch(e["origin_time"]) for e in EVS]); order = np.argsort(OT, kind="stable")
    EVS = [EVS[i] for i in order]; OT = OT[order]; MAG = np.array([float(e["mw"]) for e in EVS])
    im = int(np.argmax(MAG)); cut = OT[im] + POOL_H * 3600
    if a.all_events:                                                     # v3: P を測った全ての地震
        def _hasp(e):
            n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
            return bool((np.isfinite(tp) & (pf == 0)).any())
        dev = [i for i in range(len(EVS)) if _hasp(EVS[i])]
        if not dev: sys.exit(f"{TAG} STOP: P を測った地震が 0")
        print(f"{TAG} キャッシュ {len(EVS)} 地震、本震 {EVS[im]['origin_time']} Mj {MAG[im]:.1f}。--all-events: P を測った全ての {len(dev)} 地震"
              f"({EVS[dev[0]]['origin_time']} 〜 {EVS[dev[-1]]['origin_time']})")
    else:
        dev = [i for i in range(len(EVS)) if OT[i] > cut and MAG[i] >= DEV_MIN_MJ - 1e-6][:a.max_events]
        if not dev: sys.exit(f"{TAG} STOP: dev の地震(本震 + 72 h より後の Mj ≥ 2.0)が 0")
        print(f"{TAG} キャッシュ {len(EVS)} 地震、本震 {EVS[im]['origin_time']} Mj {MAG[im]:.1f}。dev: 本震 + 72 h より後の Mj ≥ 2.0 の最初の {len(dev)} 地震"
              f"({EVS[dev[0]]['origin_time']} 〜 {EVS[dev[-1]]['origin_time']})。21_02 の試験(1.5 ≤ Mj < 2.0)とは重ならない")
    t0 = time.time(); h5r = H5Reader(a.h5, a.index or None, base / "data" / f"h5_index_{Path(a.h5).stem}.npz")
    print(f"{TAG} h5 の準備 {time.time() - t0:.0f} s")
    print(f"{TAG} h5 の値: " + ("win_mean・win_std から元の値に戻して使う(v3)" if h5r.raw else "z-score のまま使う(win_mean・win_std が無い。限界に書く)"))
    codes, n_all, n_miss = build_station_map(EVS, dev, a.stations, h5r)
    print(f"{TAG} キャッシュの局 {n_all} のうち、観測点の一覧・h5 に見つからない局 {n_miss}")
    if n_miss > 0.10 * n_all: sys.exit(f"{TAG} STOP: 見つからない局が 10% を超える(観測点の一覧か h5 が違う)")
    picker = PhaseNetRunner()
    off = JST_OFFSET_S if a.h5_time_base == "jst" else 0.0
    t1 = time.time(); rows = run(h5r, picker, EVS, dev, codes, off); el = time.time() - t1
    print(f"{TAG} 検測 {len(rows)} 局窓({len(dev)} 地震 × {len(TAUS)} 時点)  {el:.0f} s(1 地震あたり {el / len(dev):.1f} s)")
    if not rows or not any(r["window_ok"] == 1 for r in rows): sys.exit(f"{TAG} STOP: 検測の行が 0(h5 の窓が 1 つも作れない)")
    # G-causal(実データ): 窓が T で終わっていることを、h5 の行と添字から直接読んだ時刻 T のサンプルと照らして確かめる
    # (使えた局窓を順に探し、最大 20 組で確かめる。どれも 1 サンプル後の窓とのずれも合わせて見る)
    n_gc = n_ok = 0
    for r in rows:
        if r["window_ok"] != 1 or n_gc >= 20: continue
        t_abs = origin_epoch(r["origin_time"]) + off + r["T"]
        w1 = h5r.window_ending(r["station"], t_abs); s1 = h5r.sample_at(r["station"], t_abs)
        w2 = h5r.window_ending(r["station"], t_abs + 1.0 / FS)
        if w1 is None or s1 is None or w2 is None: continue
        n_gc += 1; n_ok += int(np.array_equal(w1[:, -1], s1) and np.array_equal(w1[:, 1:], w2[:, :-1]))
    gc = n_gc > 0 and n_ok == n_gc
    print(f"{TAG} G-causal(窓の最後のサンプルが h5 の時刻 T のサンプルで、T より後を含まない): {n_ok}/{n_gc} 組 " + ("PASS" if gc else "FAIL"))
    if not gc: sys.exit(f"{TAG} STOP(G-causal): 窓の切り出しが T で終わっていない(または確かめられる組が 0)")
    S = summarize(rows)
    print(f"\n{TAG} ===== τ までの波形だけで決めた検測({a.label}、{len(dev)} 地震。記述だけ) =====")
    for k, s in S.items():
        f = lambda v, d=2: "—" if v is None else f"{v:.{d}f}"
        print(f"  τ = {k:>3} s: 届いていた P {s['p_arrived_offline']}(1 地震の中央値 {s['p_per_event_offline_median']:g})のうち T までで取れた "
              f"{s['p_matched']}(割合 {f(s['p_recall'], 3)}。T − 0.1 s までに届いていた P {s['p_arrived_offline_before_T_minus_conf']} を分母にすると "
              f"{f(s['p_recall_excluding_confirmation_delay'], 3)})、|時刻の差| 中央値 {f(s['p_absdt_median_s'], 3)} s・90% {f(s['p_absdt_p90_s'], 3)} s、"
              f"差の中央値 {f(s['p_dt_median_s'], 3)} s、届いていた P と合わない P {s['p_causal_not_matching_an_arrived_offline_p']}、"
              f"一番早い局が取れた地震の割合 {f(s['first_station_detected_frac'], 2)}({s['first_station_events']} 地震)、"
              f"窓が作れなかった局 {s['station_windows_unavailable']}  |  S: 使えていた S {s['s_usable_offline']} のうち "
              f"{s['s_matched']}(割合 {f(s['s_recall'], 3)})")
    csvp = base / "data" / f"24_07_causal_picks{a.tag}.csv"
    with open(csvp, "w", newline="") as fo:
        w = csv.DictWriter(fo, fieldnames=list(rows[0].keys())); w.writeheader()
        for r in rows: w.writerow(r)
    rule = ("all events with at least one PhaseNet (non-fallback) P in the cache (--all-events)" if a.all_events else
            f"after mainshock + {POOL_H:g} h, Mj >= {DEV_MIN_MJ}, first {a.max_events} in time (does not overlap the 21_02 test)")
    scale_lim = ("h5 values were reconstructed as z * win_std + win_mean before cutting the window, so the window scale uses samples up to T only"
                 if h5r.raw else "h5 is per-30-s-window z-scored at creation (no win_mean/win_std); "
                 "the scale of the h5 window containing T also uses samples after T (shape only up to T)")
    js = dict(script="24_07_causal_picks.py", version=VERSION, script_sha256=SELF, cache=str(a.cache), cache_sha256=CSHA,
              h5=str(a.h5), h5_time_base=a.h5_time_base, seisbench=picker.version, dev_events=len(dev),
              all_events=bool(a.all_events), label=a.label, raw_reconstructed=bool(h5r.raw), csv_sha256=sha256(csvp),
              dev_rule=rule,
              rules=dict(taus=TAUS, window_samples=NWIN, prob_min=PN_PROB_MIN, n_conf_samples=N_CONF, tp_qc=TP_QC, sp_qc=SP_QC,
                         s_after_p=S_AFTER_P, match_s=MATCH_S, origin_of_tau="earliest offline PhaseNet P in the cache (as 21_20)",
                         normalisation="SeisBench PhaseNet annotate_batch_pre within the window ending at T"),
              seconds=dict(picking=el, per_event=el / len(dev)), summary=S,
              limits=["tau origin (first P) is taken from the offline picks", "stations are the cache stations (earliest offline P, up to 24)",
                      "the P search band (-10 s and 0.5-30 s) is relative to the catalogue origin time (not known in real time), as in the offline picks",
                      "no Wadati QC and no STA/LTA fallback at each time", scale_lim,
                      "one window ending at T (no stacking over earlier windows)",
                      "data complete up to T is not the same as data available at wall-clock T (no telemetry latency)",
                      "offline P arriving within 0.1 s before T cannot be picked (confirmation delay); the recall excluding them is also given",
                      "GPU inference can differ in the last digits between runs"])
    json.dump(js, open(base / "models" / f"24_07_causal_picks{a.tag}.json", "w"), indent=1, ensure_ascii=False)
    figure(S, base / "PDF" / f"24_07_causal_picks{a.tag}.pdf", f"Causal (data up to T) vs offline PhaseNet picks, {a.label} ({len(dev)} events)")
    print(f"{TAG} 出力: {csvp} / models/24_07_causal_picks{a.tag}.json / PDF/24_07_causal_picks{a.tag}.pdf(--base の下)")


if __name__ == "__main__":
    main()
