#!/usr/bin/env python3
# =============================================================================
# Script : 26_01_paper_map_waveform.py  (v1)
# Project: ARGUS (SRL resubmission) — Fig. 1 (map, PyGMT) and Fig. 4 (waveform example)
#
# Runs on the Mac in ~/SWIFT (it needs the frozen caches, which stay on the Mac).
# It only READS frozen files; nothing registered is changed.
#
# What this script does
#   Fig. 1 (PyGMT, coastlines): (a) overview of the five sequences in Japan;
#     (b)-(f) one panel per sequence with the stations of its cache (triangles),
#     all cached events (gray dots), the evaluated test events (circles, from the
#     frozen per-event CSV), the study box (dashed) and the mainshock (star).
#     Station and event coordinates are read from the frozen caches named in the
#     judgment JSON files (key "cache"), so no coordinate is typed by hand.
#   Fig. 4 (matplotlib): one Central Tottori 2016 test event and its most similar
#     past event at tau = 2 s. The event is chosen by a fixed rule: the evaluated
#     event whose maximum similarity smax_t2 in the frozen CSV is closest to the
#     median smax_t2 (ties: earliest origin). The similarity of equation (4) is
#     recomputed here with the frozen settings of 21_04 (2-8 Hz 4th-order causal
#     Butterworth, window P-0.2 s to min(tau, P+3 s), >= 0.3 s after P, lag +-0.1 s,
#     uncentered cosine of the 3 joined components, floor 0, mean over target
#     stations, past events >= 1 h earlier with a measured P).
#     STOP unless the recomputed maximum equals smax_t2 of the CSV (|diff| < 1e-3)
#     and the distance to that past event equals best_template_sep_km_t2
#     (|diff| < 0.01 km). Only then is the figure drawn.
# Rules: no title inside figures, white background, English, legend outside the
#        maps/axes, panel labels (a)... outside the upper left, PyGMT for maps.
# Inputs : models/{21_02,21_04,21_20,25_05}_judgment.json (key "cache"),
#          data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt,
#          data/{21_02,21_04,21_20,25_05}_per_event.csv
# Outputs: PDF/26_01_Fig1_map.pdf (+ .png), PDF/26_01_Fig4_waveform_example.pdf (+ .png),
#          data/26_01_map_waveform_values.json
# Usage  : cd ~/SWIFT && uv run python src/26_01_paper_map_waveform.py
#          (--no-waveform draws Fig. 1 only; --base sets the folder that holds models/ and data/)
# =============================================================================
import argparse, io, json, sys, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("--base", default=".", help="folder that holds models/ and data/ (default: current folder, ~/SWIFT)")
ap.add_argument("--no-waveform", action="store_true", help="draw Fig. 1 only")
ap.add_argument("--no-cache", action="store_true", help="test mode: map from the CSV files only (no stations)")
ap.add_argument("--nagano-catalog", default="data/catalog/jma_nagano2014.csv",
                help="24_01 output; used for Nagano when its cache does not exist (the test stopped before the cache was built)")
ap.add_argument("--nagano-stations", default="data/catalog/stations_nagano2014.csv", help="24_02 output (id, latitude, longitude, elevation)")
a = ap.parse_args()
BASE = Path(a.base).resolve()
OUT = BASE / "PDF"; OUT.mkdir(exist_ok=True)
VAL = {}


def stop(m):
    print(f"[26_01] STOP: {m}"); sys.exit(1)


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


SEQ = [  # key, label, judgment (holds the cache path), per-event CSV, role
    ("wt2026", "West Tottori 2026", "models/21_02_judgment.json", "data/21_02_per_event.csv", "development"),
    ("ct2016", "Central Tottori 2016", "models/21_04_judgment.json", "data/21_04_per_event.csv", "test"),
    ("osaka", "Northern Osaka 2018", "models/21_20_judgment.json", "data/21_20_per_event.csv", "test"),
    ("nagano", "Northern Nagano 2014", None, None, "stopped"),
    ("shimane", "Western Shimane 2018", "models/25_05_judgment.json", "data/25_05_per_event.csv", "test"),
]
NAGANO_CACHE = "data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt"


def load_cache(p):
    import torch
    return torch.load(BASE / p, map_location="cpu", weights_only=False)


# ------------------------------------------------------------------ gather coordinates
INFO = {}
for key, lab, jp, cp, role in SEQ:
    d = dict(label=lab, role=role)
    cache = None
    if jp is not None:
        J = json.load(open(BASE / jp)); cache = J["cache"]
        if J.get("cache_sha256") and not a.no_cache and (BASE / cache).exists():
            if sha(BASE / cache) != J["cache_sha256"]: stop(f"{lab}: cache SHA-256 differs from the frozen judgment ({cache})")
        d["mainshock_json"] = J.get("mainshock")
    else:
        cache = NAGANO_CACHE
    d["cache"] = cache
    if not a.no_cache and key == "nagano" and not (BASE / cache).exists():
        # Nagano stopped at the clock check: use the frozen 24_01 catalog and the 24_02 station list instead of a cache
        cp_, sp_ = BASE / a.nagano_catalog, BASE / a.nagano_stations
        if not cp_.exists(): stop(f"{lab}: neither the cache nor the 24_01 catalog was found ({cache}; {a.nagano_catalog}). "
                                  "Give the path with --nagano-catalog")
        C = pd.read_csv(cp_); C = C[C["mag"] >= 1.5 - 1e-9]
        im = int(np.argmax(C["mag"].to_numpy(float)))
        d.update(ev_lat=C["latitude"].tolist(), ev_lon=C["longitude"].tolist(),
                 main=(float(C["latitude"].iloc[im]), float(C["longitude"].iloc[im]), float(C["mag"].iloc[im])),
                 source="24_01 catalog (Mj >= 1.5)", sha_catalog=sha(cp_))
        if sp_.exists():
            St = pd.read_csv(sp_); d["st"] = list(zip(St["latitude"].astype(float), St["longitude"].astype(float))); d["sha_stations"] = sha(sp_)
        else:
            print(f"[26_01] note: {a.nagano_stations} not found -> Nagano panel without stations (give the path with --nagano-stations)")
        INFO[key] = d; continue
    if not a.no_cache:
        if not (BASE / cache).exists(): stop(f"{lab}: cache not found: {cache}")
        EVS = load_cache(cache)
        src = np.array([np.asarray(e["src_loc"], float)[:3] for e in EVS]); mag = np.array([float(e["mw"]) for e in EVS])
        st = {}
        for e in EVS:
            n = int(e["n_real_stations"])
            for l in np.asarray(e["sta_locs"], float)[:n]: st[(round(l[0], 4), round(l[1], 4))] = (l[0], l[1])
        im = int(np.argmax(mag))
        d.update(ev_lat=src[:, 0].tolist(), ev_lon=src[:, 1].tolist(), st=list(st.values()),
                 main=(float(src[im, 0]), float(src[im, 1]), float(mag[im])))
    if cp is not None:
        E = pd.read_csv(BASE / cp); d.update(test_lat=E["lat"].tolist(), test_lon=E["lon"].tolist(), n_test=int(len(E)))
        if a.no_cache:   # test mode: mainshock unknown without the cache -> center of the test events
            d["main"] = (float(np.median(E["lat"])), float(np.median(E["lon"])), np.nan)
    INFO[key] = d
VAL["fig1"] = {k: dict(label=v["label"], n_stations=len(v.get("st", [])), n_cached_events=len(v.get("ev_lat", [])),
                       n_test=v.get("n_test"), mainshock=v.get("main")) for k, v in INFO.items()}
for k, v in VAL["fig1"].items(): print(f"[26_01] {v['label']}: stations {v['n_stations']}, cached events {v['n_cached_events']}, "
                                       f"evaluated test events {v['n_test']}, mainshock {v['mainshock']}")

# ------------------------------------------------------------------ Fig. 1 (PyGMT)
import pygmt
pygmt.config(FONT_ANNOT_PRIMARY="7p,Helvetica", FONT_LABEL="8p,Helvetica", FONT_TAG="9p,Helvetica-Bold",
             MAP_FRAME_TYPE="plain", MAP_FRAME_PEN="0.6p", PS_PAGE_COLOR="white", FORMAT_GEO_MAP="ddd.x")
keys = [k for k, *_ in SEQ if k in INFO and INFO[k].get("main")]
fig = pygmt.Figure()
with fig.subplot(nrows=2, ncols=3, figsize=("17.8c", "12.2c"), autolabel="(a)+JTL+o0.05c/0.08c", margins=["0.5c", "0.5c"],
                 frame="lrtb"):
    with fig.set_panel(panel=0):
        fig.coast(region=[130.0, 139.0, 33.2, 37.8], projection="M?", land="gray92", water="white", shorelines="0.25p,gray40",
                  borders="2/0.2p,gray70", frame=["WSne", "xa2f1", "ya1f0.5"])
        for k in keys:
            la, lo, _ = INFO[k]["main"]
            fig.plot(x=lo, y=la, style="a0.30c", fill="black" if INFO[k]["role"] != "stopped" else "white", pen="0.5p,black")
            off = {"wt2026": "0.0c/-0.30c", "ct2016": "0.05c/0.25c", "osaka": "0.15c/-0.15c", "nagano": "0.0c/0.25c", "shimane": "0.0c/0.25c"}[k]
            just = {"wt2026": "TC", "ct2016": "BL", "osaka": "TL", "nagano": "BR", "shimane": "BR"}[k]
            short = {"wt2026": "W. Tottori 2026", "ct2016": "C. Tottori 2016", "osaka": "Osaka 2018", "nagano": "Nagano 2014", "shimane": "Shimane 2018"}[k]
            fig.text(x=lo, y=la, text=short, font="6.5p,Helvetica,black", justify=just, offset=off)
    for i, k in enumerate(keys, start=1):
        la, lo, _ = INFO[k]["main"]; dlat, dlon = 1.05, 1.25
        with fig.set_panel(panel=i):
            fig.coast(region=[lo - dlon, lo + dlon, la - dlat, la + dlat], projection="M?", land="gray92", water="white",
                      shorelines="0.25p,gray40", frame=["WSne", "xa1f0.5", "ya0.5f0.25"])
            if INFO[k].get("ev_lat"):
                fig.plot(x=INFO[k]["ev_lon"], y=INFO[k]["ev_lat"], style="c0.05c", fill="gray55")
            if INFO[k].get("test_lat"):
                fig.plot(x=INFO[k]["test_lon"], y=INFO[k]["test_lat"], style="c0.10c", fill="#0072B2", pen="0.15p,black")
            if INFO[k].get("st"):
                s = np.array(INFO[k]["st"]); fig.plot(x=s[:, 1], y=s[:, 0], style="i0.20c", fill="#E69F00", pen="0.3p,black")
            bx = [lo - 0.175, lo + 0.175, lo + 0.175, lo - 0.175, lo - 0.175]; by = [la - 0.15, la - 0.15, la + 0.15, la + 0.15, la - 0.15]
            fig.plot(x=bx, y=by, pen="0.6p,black,4_2:0")
            fig.plot(x=lo, y=la, style="a0.32c", fill="black" if INFO[k]["role"] != "stopped" else "white", pen="0.5p,black")
            fig.text(position="TR", text=INFO[k]["label"], font="7p,Helvetica,black", offset="-0.1c/-0.1c", fill="white")
# legend below the panels
fig.shift_origin(yshift="-1.3c")
fig.basemap(region=[0, 1, 0, 1], projection="X17.8c/0.9c", frame="+n")
leg = io.StringIO("N 5\n"
                  "S 0.2c a 0.30c black 0.5p,black 0.5c Mainshock\n"
                  "S 0.2c i 0.20c #E69F00 0.3p,black 0.5c Station\n"
                  "S 0.2c c 0.10c #0072B2 0.15p,black 0.5c Evaluated test event\n"
                  "S 0.2c c 0.05c gray55 - 0.5c Other cached event\n"
                  "S 0.2c - 0.5c - 0.6p,black,4_2:0 0.5c Study box\n")
fig.legend(spec=leg, position="jMC+w17.0c", box=False)
for ext in ("pdf", "png"): fig.savefig(OUT / f"26_01_Fig1_map.{ext}", dpi=300)
print("[26_01] wrote PDF/26_01_Fig1_map.pdf")

# ------------------------------------------------------------------ Fig. 4 (waveform example, Central Tottori 2016)
if not a.no_waveform and not a.no_cache:
    from scipy.signal import butter, sosfilt
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    FS, IP, NTS = 100.0, 300, 2048                    # frozen 21_04 constants
    PRE_S, MIN_WIN_S, MAX_WIN_S, MAX_LAG_S, BUFFER_H, TAU, EPS_T = 0.2, 0.3, 3.0, 0.1, 1.0, 2.0, 1e-9
    NKEEP = IP + int(round((MAX_WIN_S + MAX_LAG_S) * FS)) + 2
    PRE_N, LAG_N, MINW_N = int(round(PRE_S * FS)), int(round(MAX_LAG_S * FS)), int(round(MIN_WIN_S * FS))
    SOS = butter(4, (2.0, 8.0), btype="bandpass", fs=FS, output="sos")
    J = json.load(open(BASE / "models/21_04_judgment.json")); EVS = load_cache(J["cache"])
    ot_ns = np.array([int(pd.Timestamp(str(e["origin_time"]).replace("Z", "+00:00")).tz_localize(None).value
                          if pd.Timestamp(str(e["origin_time"])).tzinfo is None else
                          pd.Timestamp(str(e["origin_time"])).tz_convert("UTC").tz_localize(None).value) for e in EVS])
    order = np.argsort(ot_ns, kind="stable"); EVS = [EVS[i] for i in order]; ot_ns = ot_ns[order]
    skey = lambda loc: (round(float(loc[0]), 4), round(float(loc[1]), 4), round(float(loc[2]), 3))
    TF = np.full(len(EVS), np.nan)
    for ie, e in enumerate(EVS):
        n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
        ok = np.isfinite(tp) & (pf == 0)
        if ok.any(): TF[ie] = float(tp[ok].min())
    HASP = np.isfinite(TF)
    FC = {}

    def filt(ie):
        if ie not in FC:
            e = EVS[ie]; n = int(e["n_real_stations"]); W = np.asarray(e["waveforms"], float)[:n]
            loc = np.asarray(e["sta_locs"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
            FC[ie] = {skey(loc[k]): sosfilt(SOS, W[k], axis=-1)[:, :NKEEP] for k in range(n) if pf[k] == 0}
        return FC[ie]

    def target_windows(ie):
        e = EVS[ie]; n = int(e["n_real_stations"]); loc = np.asarray(e["sta_locs"], float)[:n]
        tp = np.asarray(e["tp_times"], float)[:n] - TF[ie]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]; F = filt(ie); out = []
        for k in range(n):
            if not np.isfinite(tp[k]) or pf[k] != 0 or tp[k] > TAU + EPS_T: continue
            nav = int(np.floor((min(TAU, tp[k] + MAX_WIN_S) - tp[k]) * FS + 1e-3))
            key = skey(loc[k])
            if nav < MINW_N or key not in F: continue
            out.append((key, F[key][:, IP - PRE_N: IP + nav]))
        return out

    def similarity(ie, lib):
        tw = target_windows(ie); S = np.zeros(len(lib)); per = []
        for jj, j in enumerate(lib):
            Fj = filt(j); acc = 0.0; ps = {}
            for key, x in tw:
                if key not in Fj: continue
                y = Fj[key]; L = x.shape[1]; xv = x.ravel(); nx = np.linalg.norm(xv); best, bl = 0.0, 0
                if nx == 0: continue
                for l in range(-LAG_N, LAG_N + 1):
                    yv = y[:, IP - PRE_N + l: IP - PRE_N + l + L].ravel(); ny = np.linalg.norm(yv)
                    if ny > 0:
                        c = float(xv @ yv) / (nx * ny)
                        if c > best: best, bl = c, l
                acc += best; ps[key] = (best, bl)
            S[jj] = acc / len(tw) if tw else 0.0; per.append(ps)
        return S, tw, per

    E = pd.read_csv(BASE / "data/21_04_per_event.csv").copy()
    E["ot_ns"] = [int(pd.Timestamp(str(o)).value) for o in E["origin_time"]]
    sm = E["smax_t2"].to_numpy(float); okr = np.isfinite(sm)
    med = float(np.median(sm[okr])); cand = E[okr].assign(d=np.abs(sm[okr] - med)).sort_values(["d", "ot_ns"])
    row = cand.iloc[0]
    hit = np.where(np.abs(ot_ns - int(row["ot_ns"])) < 1_000_000)[0]
    if len(hit) != 1: stop(f"could not match the chosen CSV event {row['origin_time']} to one cached event ({len(hit)})")
    ie = int(hit[0])
    lib = np.where((ot_ns <= ot_ns[ie] - int(BUFFER_H * 3600e9)) & HASP)[0]
    S, tw, per = similarity(ie, lib)
    jbest = int(np.argmax(S)); jb = int(lib[jbest])
    s0 = np.asarray(EVS[ie]["src_loc"], float); s1 = np.asarray(EVS[jb]["src_loc"], float)
    sep = float(np.hypot((s0[0] - s1[0]) * 111.0, (s0[1] - s1[1]) * 111.0 * np.cos(np.radians((s0[0] + s1[0]) / 2))))
    print(f"[26_01] Fig. 4 event {row['origin_time']} Mj {row['mj']}: recomputed max S {S[jbest]:.4f} (CSV {row['smax_t2']:.4f}), "
          f"distance {sep:.3f} km (CSV {row['best_template_sep_km_t2']:.3f}), {len(tw)} target stations, {len(lib)} past events")
    if abs(S[jbest] - row["smax_t2"]) > 1e-3: stop("recomputed similarity does not reproduce the frozen smax_t2")
    if abs(sep - row["best_template_sep_km_t2"]) > 0.01: stop("the most similar past event differs from the frozen one")
    # draw up to 8 target stations ordered by P time: vertical component of target (black) and past event (orange, best lag)
    e = EVS[ie]; n = int(e["n_real_stations"]); loc = np.asarray(e["sta_locs"], float)[:n]
    tp = np.asarray(e["tp_times"], float)[:n] - TF[ie]; order_k = [k for k in np.argsort(tp) if skey(loc[k]) in dict(tw)][:8]
    plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "Liberation Sans", "DejaVu Sans"],
                         "font.size": 8, "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "pdf.fonttype": 42})
    fig, ax = plt.subplots(figsize=(7.0, 3.6)); Fi, Fj = filt(ie), filt(jb); rows = []
    for r, k in enumerate(order_k):
        key = skey(loc[k]); x = Fi[key][0]; tx = (np.arange(len(x)) - IP) / FS + tp[k]
        c, l = per[jbest].get(key, (0.0, 0))
        nav = int(np.floor((min(TAU, tp[k] + MAX_WIN_S) - tp[k]) * FS + 1e-3))
        sel = slice(IP - PRE_N - 30, IP + nav + 30)
        xs = x[sel] / (np.abs(x[IP - PRE_N: IP + nav]).max() + 1e-12)
        ax.plot(tx[sel], -r + 0.42 * xs, color="k", lw=0.7, label="Target event" if r == 0 else None)
        if key in Fj:
            y = Fj[key][0]; ys = y[IP - PRE_N - 30 + l: IP + nav + 30 + l]
            ys = ys / (np.abs(y[IP - PRE_N + l: IP + nav + l]).max() + 1e-12)
            ax.plot(tx[sel][:len(ys)], -r + 0.42 * ys, color="#E69F00", lw=0.7, ls="--", label="Most similar past event" if r == 0 else None)
        from matplotlib.patches import Rectangle   # window used by equation (4) for this station: P - 0.2 s to min(tau, P + 3 s)
        ax.add_patch(Rectangle((tp[k] - PRE_S, -r - 0.47), PRE_S + nav / FS, 0.94, color="0.92", lw=0, zorder=0,
                               label="Window used for the similarity" if r == 0 else None))
        ax.text(TAU + 0.45, -r, f"{c:.2f}", va="center", fontsize=7)
        rows.append(dict(station=key, tP_s=float(tp[k]), station_similarity=float(c), lag_s=float(l / FS)))
    ax.axvline(TAU, color="#D55E00", lw=0.8); ax.text(TAU, 0.75, "τ = 2 s", color="#D55E00", fontsize=7, ha="center")
    ax.set_yticks([-r for r in range(len(order_k))]); ax.set_yticklabels([f"Station {r + 1}" for r in range(len(order_k))])
    ax.set_xlabel("Time after the first P pick of the target event (s)"); ax.set_xlim(-0.6, TAU + 0.8)
    ax.text(1.0, 1.02, "station similarity", transform=ax.transAxes, ha="right", va="bottom", fontsize=7)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, -0.18), ncol=3, frameon=False)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    fig.tight_layout()
    for ext in ("pdf", "png"): fig.savefig(OUT / f"26_01_Fig4_waveform_example.{ext}", dpi=300, bbox_inches="tight")
    VAL["fig4"] = dict(event=str(row["origin_time"]), mj=float(row["mj"]), median_smax_t2=med, smax_recomputed=float(S[jbest]),
                       smax_csv=float(row["smax_t2"]), sep_km=sep, sep_csv=float(row["best_template_sep_km_t2"]),
                       past_event=str(EVS[jb]["origin_time"]), n_target_stations=len(tw), n_past=int(len(lib)), stations=rows)
    print("[26_01] wrote PDF/26_01_Fig4_waveform_example.pdf")
json.dump(VAL, open(BASE / "data" / "26_01_map_waveform_values.json", "w"), indent=1, default=str)
print("[26_01] wrote data/26_01_map_waveform_values.json")
