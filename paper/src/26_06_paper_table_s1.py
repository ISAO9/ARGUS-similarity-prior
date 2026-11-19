#!/usr/bin/env python3
# =============================================================================
# Script : 26_06_paper_table_s1.py  (v1.1: 4-decimal storage against double rounding; --swift runs in ~/SWIFT)
# Project: ARGUS (SRL resubmission) — supplemental Table S1 from frozen outputs only
#
# What this script does
#   Builds the supplemental tables from the frozen judgment JSON files (no recomputation):
#     Table S1a: every registered hypothesis x sequence: method, reference (BEST named),
#                tau, alpha, medians, one-sided Wilcoxon p, number of non-zero pairs,
#                fractions better/tied, floor flag, outcome; HG1-HG3 with their counts.
#     Table S1b: median epicentral error and 95% bootstrap interval of every method
#                at every tau (0.5, 1, 2, 3 s and all picks) for the four sequences.
#     Table S1c: Hodges-Lehmann shifts with day-block intervals (from 26_04).
#   Writes CSV and a Markdown version for the supplement.
# Inputs : data/inputs/models/{21_02,21_04,21_06b,21_20,21_20f,22_04,25_05,25_06f,25_06g}_judgment.json,
#          data/26_04_effect_sizes.json
# Outputs: data/26_06_table_S1a.csv, data/26_06_table_S1b.csv, data/26_06_table_S1c.csv, data/26_06_tables_S1.md
# Usage  : uv run python src/26_06_paper_table_s1.py            (paper repository layout, data/inputs/)
#          cd ~/SWIFT && uv run python src/26_06_paper_table_s1.py --swift   (inputs models/, data/26_04_effect_sizes.json)
# =============================================================================
import json
from pathlib import Path
import pandas as pd

import sys
ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "models" if "--swift" in sys.argv else ROOT / "data" / "inputs" / "models"
L = lambda f: json.load(open(M / f))
SEQ = [("Central Tottori 2016", "21_04", "21_06b", None), ("Northern Osaka 2018", "21_20", "21_20f", "22_04"),
       ("Western Shimane 2018", "25_05", "25_06f", "25_06g")]
f3 = lambda v: None if v is None else round(float(v), 4)   # v1.1: 4 decimals so that 2-decimal display is not double-rounded (0.6545 -> 0.65, not 0.655 -> 0.66)
fp = lambda v: None if v is None else float(f"{float(v):.2g}")
rows = []
for lab, s, l, g in SEQ:
    J = L(f"{s}_judgment.json")
    hyps = dict(J["hypotheses"]); hyps.update(J.get("hypotheses_24") or {})
    for k in ("H1", "H2", "H3", "H4", "H5"):
        if k not in hyps: continue
        h = hyps[k]; pb = h.get("paired_vs_best") or h.get("paired") or {}
        rows.append(dict(sequence=lab, hypothesis=k, method=h["method"], reference=h.get("best") or h.get("other"), tau_s=h["tau"],
                         alpha=h["alpha"], method_median_km=f3(h["median_km"]), reference_median_km=f3(h.get("best_median_km", h.get("other_median_km"))),
                         p=fp(pb.get("p")), n_pairs=pb.get("n"), n_nonzero=pb.get("n_nonzero"), frac_better=f3(pb.get("frac_better")),
                         frac_tied=f3(pb.get("frac_tied")), floor=h.get("floor"), win=h.get("win")))
    LJ = L(f"{l}_judgment.json")
    for k in ("HL1", "HL2", "HL3"):
        h = LJ["hypotheses"][k]; pb = h.get("paired") or {}
        rows.append(dict(sequence=lab, hypothesis=k, method=h["method"], reference=h.get("comparator"),
                         tau_s=h["tau"], alpha=h.get("alpha"), method_median_km=f3(h["median_km"]),
                         reference_median_km=f3(h.get("comparator_median_km")),
                         p=fp(pb.get("p")), n_pairs=pb.get("n"), n_nonzero=pb.get("n_nonzero"), frac_better=f3(pb.get("frac_better")),
                         frac_tied=f3(pb.get("frac_tied")), floor=h.get("floor"), win=h.get("win")))
    if g:
        GJ = L(f"{g}_judgment.json"); H = GJ["hypotheses"]; s3 = H.get("HG3_secondary") or {}
        h1, h2 = H["HG1"], H["HG2"]
        rows.append(dict(sequence=lab, hypothesis="HG1", method="G", reference="C4", tau_s="2", alpha=h1["alpha"],
                         p=fp(h1["p"]), n_nonzero=h1["n_discordant"], note=f"missed > 10 km by C4 only {h1['b_C4_only_miss']}, by G only {h1['c_G_only_miss']}"))
        rows.append(dict(sequence=lab, hypothesis="HG2", method="G", reference="R", tau_s="2", alpha=h2["alpha"], p=fp(h2["p"]), n_nonzero=h2["n_nonzero"]))
        if s3: rows.append(dict(sequence=lab, hypothesis="HG3", method="G", reference="R", tau_s="1", alpha=s3.get("alpha"), p=fp(s3.get("p")),
                                n_nonzero=s3.get("n_nonzero"), method_median_km=f3(s3.get("G_median_km")), reference_median_km=f3(s3.get("R_median_km")),
                                note=s3.get("result")))
        gd = H.get("guard") or {}
        rows.append(dict(sequence=lab, hypothesis="guard", method="G", reference="C4", tau_s="2", method_median_km=f3(gd.get("G_median_km")),
                         reference_median_km=f3(gd.get("C4_median_km")), note=f"ok {gd.get('ok')}; verdict {GJ['verdict']}"))
A = pd.DataFrame(rows); A.to_csv(ROOT / "data/26_06_table_S1a.csv", index=False)

rows = []
for lab, s in [("West Tottori 2026 (development)", "21_02")] + [(x[0], x[1]) for x in SEQ]:
    S = L(f"{s}_judgment.json")["summary"]
    for m, d in S.items():
        for t, r in d.items():
            if r.get("median_km") is None: continue
            rows.append(dict(sequence=lab, method=m, tau_s=t, median_km=f3(r["median_km"]), ci_lo=f3(r.get("ci_lo")), ci_hi=f3(r.get("ci_hi")),
                             available=f3(r.get("available"))))
B = pd.DataFrame(rows); B.to_csv(ROOT / "data/26_06_table_S1b.csv", index=False)
C = pd.DataFrame(json.load(open(ROOT / "data/26_04_effect_sizes.json"))); C.to_csv(ROOT / "data/26_06_table_S1c.csv", index=False)
try:
    with open(ROOT / "data/26_06_tables_S1.md", "w") as f:
        for name, D in (("Table S1a", A), ("Table S1b", B), ("Table S1c", C)):
            f.write(f"## {name}\n\n" + D.to_markdown(index=False) + "\n\n")
except ImportError:
    print("[26_06] note: tabulate is not installed; the Markdown file was skipped (CSV files are complete)")
print(A.to_string(index=False)); print(f"[26_06] S1a {len(A)} rows, S1b {len(B)} rows, S1c {len(C)} rows")
