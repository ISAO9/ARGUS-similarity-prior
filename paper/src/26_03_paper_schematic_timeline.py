#!/usr/bin/env python3
# =============================================================================
# Script : 26_03_paper_schematic_timeline.py  (v1)
# Project: ARGUS (SRL resubmission) — Fig. 2 (method diagram) and Fig. 3 (test timeline)
#
# What this script does
#   Fig. 2: draws the structure of the methods (no numbers): picks and waveforms
#           recorded by tau -> physics misfit (equation 2) combined with a
#           seismicity prior (equation 3) built from (i) past events with the same
#           first-P station (reference M6r), (ii) the similar set chosen by the
#           waveform similarity of equation (4) (C3; C4 adds the path corrections
#           of equation 5), (iii) the set ranked by the learned model (L3, L4).
#           C1 returns the epicenter of the most similar past event; G chooses C1 or C4.
#   Fig. 3: draws the order of registrations, amendments, stops, model freezes and
#           openings. Every time is read from a frozen record:
#             * opening times and model-freeze times from models/*_opened.json
#             * registration, amendment and stop times from the git log of the
#               registration repository (data/paper_gitlog.txt; commit times in JST)
#           The script STOPs if a listed commit or record is missing, so the figure
#           cannot show a date that is not in the records.
# Rules: no title inside figures, white background, English, legend outside axes,
#        panel labels outside the upper left, Okabe-Ito colors + marker shapes.
# Inputs : data/inputs/models/*_opened.json, data/paper_gitlog.txt
# Outputs: PDF/26_03_Fig2_methods.pdf, PDF/26_03_Fig3_timeline.pdf (+ .png),
#          data/26_03_timeline_values.json
# Usage  : uv run python src/26_03_paper_schematic_timeline.py
# =============================================================================
import json, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
INP = ROOT / "data" / "inputs" / "models"
GITLOG = ROOT / "data" / "paper_gitlog.txt"
PDFD = ROOT / "PDF"; PDFD.mkdir(exist_ok=True)
JST = timezone(timedelta(hours=9))
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "Liberation Sans", "DejaVu Sans"],
                     "font.size": 8, "axes.linewidth": 0.6, "figure.facecolor": "white", "axes.facecolor": "white",
                     "savefig.facecolor": "white", "pdf.fonttype": 42})


def stop(m):
    print(f"[26_03] STOP: {m}"); sys.exit(1)


# ------------------------------------------------------------------ Fig. 2  method diagram
fig, ax = plt.subplots(figsize=(7.0, 3.3)); ax.set_xlim(0, 100); ax.set_ylim(0, 48); ax.axis("off")


def box(x, y, w, h, txt, fc="white", ec="k", fs=7.2, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec=ec, lw=0.8))
    ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs, fontweight="bold" if bold else "normal")


def arrow(x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", lw=0.8, color="k", shrinkA=0, shrinkB=0))


box(1.5, 18, 15.5, 12, "Target event:\npicks and\nwaveforms\nrecorded by τ", fc="#F2F2F2")
box(23, 36, 22, 9, "Physics misfit Φ/b\n(equations 1, 2)", fc="#DCEBF6")
box(23, 19, 22, 10, "Waveform similarity S\nto every past event\n(equation 4)", fc="#FBEBD3")
box(23, 3, 22, 9, "Learned ranking of\npast events (17 features)", fc="#F6E1EC")
box(52, 36, 21, 9, "Prior from past events,\nsame first-P station", fc="white")
box(52, 21, 21, 9, "Prior from the similar\nset T (equation 3)", fc="white")
box(52, 3, 21, 9, "Prior from the 10\nranked events", fc="white")
box(80, 36, 18, 9, "M6r\n(reference)", bold=True)
box(80, 25.5, 18, 8, "C3; C4 adds path\ncorrections (eq. 5)", bold=True)
box(80, 13, 18, 8, "C1: epicenter of the\nmost similar event", bold=True)
box(80, 3, 18, 9, "L3; L4 adds path\ncorrections", bold=True)
arrow(17, 27, 23, 40.5); arrow(17, 24, 23, 24); arrow(17, 21, 23, 7.5)
arrow(45, 40.5, 52, 40.5); arrow(45, 25.5, 52, 25.5); arrow(45, 7.5, 52, 7.5)
arrow(73, 40.5, 80, 40.5); arrow(73, 26.5, 80, 29); arrow(45, 20.5, 80, 17); arrow(73, 7.5, 80, 7.5)
ax.text(62.5, 33.2, "prior × physics likelihood", fontsize=6.5, color="0.25", ha="center")
ax.annotate("", xy=(97, 21.4), xytext=(97, 25.5), arrowprops=dict(arrowstyle="-", lw=0.6))
ax.text(99.3, 23.4, "G chooses\nC1 or C4", fontsize=6.5, ha="left", va="center")
for ext in ("pdf", "png"): fig.savefig(PDFD / f"26_03_Fig2_methods.{ext}", dpi=300, bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------------ Fig. 3  timeline from the records
if not GITLOG.exists(): stop(f"missing {GITLOG}")
GIT = {}
for line in GITLOG.read_text().splitlines():
    if not line.strip(): continue
    h, d, t, z, *_ = line.split(" ")
    GIT[h] = datetime.fromisoformat(f"{d}T{t}{z[:3]}:{z[3:]}").astimezone(timezone.utc)


def opened(fname, which="opened"):
    p = INP / fname
    if not p.exists(): stop(f"missing {p}")
    rec = json.load(open(p))
    for r in rec:
        ev = str(r.get("event") or r.get("status") or "")
        if ev.startswith(which): return datetime.fromisoformat(r["utc"].replace("Z", "+00:00"))
    stop(f"no '{which}' entry in {fname}")


def git(h):
    if h not in GIT: stop(f"commit {h} not in the git log")
    return GIT[h]


ROWS = ["Central Tottori 2016", "Northern Osaka 2018", "Northern Nagano 2014", "Western Shimane 2018", "Frozen models"]
EV = [  # (row, time, kind, label)
    (0, git("ceb15b1"), "reg", "registered"), (0, git("c5fa534"), "amd", "A01"), (0, git("dc1267b"), "amd", "A02"),
    (0, git("5133563"), "amd", "A03"), (0, opened("21_04_opened.json"), "open", "opened"),
    (1, git("6bac5a0"), "reg", "registered"), (1, git("3839889"), "stop", "stopped before opening"),
    (1, git("3f8abad"), "amd", "A04"), (1, opened("21_20_opened.json"), "open", "opened"),
    (2, git("a852c2c"), "reg", "registered"), (2, git("fc38d0f"), "amd", "A01"), (2, git("f2c7ce8"), "stop", "stopped"),
    (3, git("54ae4bc"), "reg", "registered"), (3, opened("25_05_opened.json"), "open", "opened"),
    (4, opened("21_06a_opened.json", "completed"), "freeze", "ranker (L3, L4)"),
    (4, opened("22_02_opened.json", "completed"), "freeze", "switch G"),
]
STY = {"reg": dict(m="D", c="#0072B2", lab="Registration"), "amd": dict(m="^", c="#E69F00", lab="Amendment"),
       "stop": dict(m="X", c="#D55E00", lab="Stopped by a gate"), "open": dict(m="o", c="#009E73", lab="Opened (one-shot test)"),
       "freeze": dict(m="s", c="#000000", lab="Model frozen")}
fig, ax = plt.subplots(figsize=(7.0, 2.6))
seen = set(); val = []
for row, t, k, lab in EV:
    y = len(ROWS) - 1 - row + {"reg": 0.18, "amd": 0.18, "open": -0.18, "stop": -0.18, "freeze": 0.0}[k]; s = STY[k]
    ax.plot(t, y, s["m"], color=s["c"], ms=6, mec="k", mew=0.4, label=s["lab"] if k not in seen else None, zorder=3); seen.add(k)
    val.append(dict(row=ROWS[row], utc=t.isoformat(), kind=k, label=lab))
    if k == "freeze": ax.text(t + timedelta(hours=10), y, lab, va="center", ha="left", fontsize=6.5)
for i in range(len(ROWS)): ax.axhline(i, color="0.85", lw=0.5, zorder=1)
ax.set_yticks(range(len(ROWS))); ax.set_yticklabels(ROWS[::-1])
ax.set_ylim(-0.6, len(ROWS) - 0.4)
for i in range(len(ROWS) - 1): ax.axhspan(i + 0.5, i + 1.5, color="0.97" if i % 2 else "white", lw=0, zorder=0)
t0 = datetime(2026, 10, 27, tzinfo=timezone.utc); t1 = datetime(2026, 11, 20, tzinfo=timezone.utc)
ax.set_xlim(t0, t1); ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[28, 1, 4, 7, 10, 13, 16, 19]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b")); ax.set_xlabel("Date in 2026 (UTC)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=5, frameon=False, fontsize=7)
for sp in ("top", "right"): ax.spines[sp].set_visible(False)
fig.tight_layout()
for ext in ("pdf", "png"): fig.savefig(PDFD / f"26_03_Fig3_timeline.{ext}", dpi=300, bbox_inches="tight")
plt.close(fig)
json.dump(val, open(ROOT / "data" / "26_03_timeline_values.json", "w"), indent=1)
print("[26_03] wrote PDF/26_03_Fig2_methods, PDF/26_03_Fig3_timeline, data/26_03_timeline_values.json")
for v in val: print("  ", v["row"], v["utc"][:16], v["kind"], v["label"])
