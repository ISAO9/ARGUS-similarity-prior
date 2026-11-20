# =============================================================================
# Script : 26_13_release_assemble.py   (v2.2, 2026-11-20: adds 26_15 (error distributions, Figure S2 and
#          Table S9), rerun and compared with the Mac output; v2.1: the business name is matched only by
#          its SHA-256 hash, so the name itself never appears in this script or its report)
# Project: ARGUS (SRL new submission, "How Much Do Waveform-Similar Past
#          Earthquakes Improve Early Epicenters?")
#
# What this script does
#   The single gate before the one-time GitHub/Zenodo release.
#   The registration repository (~/ARGUS_prereg_21_04) stays PRIVATE: its
#   history holds author contact details that cannot be removed without
#   changing every commit hash. This script builds a separate PUBLIC copy
#   (default ~/ARGUS_public) that has no history:
#
#   1. Collect  paper scripts (26_01-26_06, 26_08-26_13, 26_15), check scripts, frozen
#               results of every registration, learned models (found by their
#               registered SHA-256), 26_xx outputs, figure PDFs and the Python
#               environment of ~/SWIFT.
#   2. Frozen   every script named in a frozen result must match its SHA-256
#               (registered scripts: the committed copy; development scripts
#               21_01/21_02/21_10: the copy in ~/SWIFT/src, then released).
#   3. Build    the public tree in a staging folder: the files of the last commit
#               (HEAD) of the registration repository, with author contact
#               details removed from .md/.txt files (each change listed in
#               REDACTIONS.md with the SHA-256 of the original and of the copy;
#               a registered script is never changed), REGISTRATION_LOG.txt
#               (every commit: hash, time, message), a README, an MIT LICENSE,
#               and paper/ (the paper materials).
#   4. Verify   reruns 26_04, 26_06, 26_02, 26_03, 26_09, 26_11 and 26_15 from the
#               staged files and compares numeric fingerprints with the
#               submitted paper (fixed on 2026-11-19) and with the Mac outputs.
#   5. Scan     every staged file: credentials, e-mail addresses, the author's
#               business name (matched by SHA-256 hash only), binary
#               files other than PDF/PNG/registered models, waveform-type names,
#               files > 50 MB, sensitive names (.DS_Store, .netrc, keys),
#               notebook outputs, AI tool names, home paths. Hi-net waveforms and
#               the West Tottori 2026 records must never be published.
#   6. Apply    (--apply, only when 0 FAIL and 0 WARN) writes the staged tree to
#               ~/ARGUS_public (an existing .git folder there is kept).
#   Nothing in ~/SWIFT or in the registration repository is changed, and no git
#   command that writes is run. Reviewed findings can be accepted with
#   --allow FILE (one text per line; a finding containing it is accepted).
#
# Usage
#   cd ~/SWIFT && uv run python src/26_13_release_assemble.py            # build, verify, scan; report only
#   cd ~/SWIFT && uv run python src/26_13_release_assemble.py --apply    # same, then write ~/ARGUS_public
#   options: --swift ~/SWIFT  --repo ~/ARGUS_prereg_21_04  --public ~/ARGUS_public  --allow FILE
# Output
#   console report ending in a table and "READY FOR RELEASE" or not; with a
#   successful --apply the folder ~/ARGUS_public
# =============================================================================
import argparse, csv, hashlib, json, math, os, pickle, platform, re, shutil
import subprocess, sys, tempfile, time
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--swift", default="~/SWIFT")
ap.add_argument("--repo", default="~/ARGUS_prereg_21_04")
ap.add_argument("--public", default="~/ARGUS_public", help="folder of the public copy")
ap.add_argument("--apply", action="store_true", help="write the public copy (only if every check passes)")
ap.add_argument("--allow", default=None, help="text file of reviewed findings to accept (one per line)")
A = ap.parse_args()
SW = Path(os.path.expanduser(A.swift)).resolve()
RP = Path(os.path.expanduser(A.repo)).resolve()
PUBLIC = Path(os.path.expanduser(A.public)).resolve()
PAPER = RP / "paper"                       # not written in v2.0; kept to skip an old paper/ folder in searches
T0 = time.time()
ALLOW = []
if A.allow:
    ALLOW = [l.strip() for l in Path(os.path.expanduser(A.allow)).read_text().splitlines() if l.strip()]
RESULT = []          # (check, status, detail)


def res(name, status, detail=""):
    if isinstance(status, bool): status = "PASS" if status else "FAIL"
    RESULT.append((name, status, detail)); print(f"  [{status}] {name}  {detail[:300]}")


def res_items(name, items, sev):
    """PASS if no item is left after removing items accepted in --allow."""
    left = [i for i in items if not any(a in i for a in ALLOW)]
    acc = len(items) - len(left)
    tail = f" ({acc} accepted by --allow)" if acc else ""
    res(name, "PASS" if not left else sev, (f"{len(left)}: " + " | ".join(left[:8]) if left else "") + tail)


def sha_bytes(b): return hashlib.sha256(b).hexdigest()


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def git(*args, raw=False, ok_codes=(0,)):
    r = subprocess.run(["git", "-c", "core.quotePath=false", "-C", str(RP), *args], capture_output=True)
    if r.returncode not in ok_codes:
        sys.exit(f"[26_13] STOP: git {' '.join(args)} failed: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout if raw else r.stdout.decode("utf-8", "replace")


# ---------------------------------------------------------------- expectations
SENT = {   # SHA-256 of the 26_xx scripts as delivered (the versions behind the paper)
    "26_01_paper_map_waveform.py": "6fca52be3f57cff079cef05c44b167d4f9fcf7c2b8911edb4e58832ca61e972b",
    "26_02_paper_result_figures.py": "e8d96aa6f954ef8458a428bf6d948bf69eccaa635f8602737c6891ec26d8e6c6",
    "26_03_paper_schematic_timeline.py": "ef50551717f402fec3248678b62979997325effacae771298de9b5f2f33fc04f",
    "26_04_paper_effect_sizes.py": "0dbdfb47a39e35203c3e516091d9887cd4b9454096845be714c55f5d0aabf07d",
    "26_05_set_size_control.py": "6075cfa93bf6854e73cd35eaa0856572f156f95ee0bbef078aa4b6e938833e1d",
    "26_06_paper_table_s1.py": "b000354ddbe15c82f348ac3ccc9ce0a8594e8667104cea6518f57e10fd834ce0",
    "26_08_reviewer_inventory.py": "976a410a00a6b1614de76f9206a77c4092d0df25ef15ee14e54f24a4d69df004",
    "26_09_reviewer_checks.py": "b490080040c588c8ea0c94242ca51da55d001edcd7e9a275522a12cac58dae17",
    "26_10_memory_truncation.py": "108d5c6e5523057f83afc091e1cf167e7fca8e3d50cb7c317d78560b76b1dc02",
    "26_11_reviewer_supplement.py": "969c91bafd1bde42cf43b95188605ab3742fa5afcb91c9bf0985a2928df942ac",
    "26_12_causal_mean_check.py": "6858e4cead4304ebc60b997ebcc7718c1b2170bd2b66302e19c6a79ad1e31299",
    "26_15_error_distributions.py": "654ed371cfb1a6b77f40c00d49c6a11f8edf150cfd7ccebdd56f711e071239e8",
}
# Fingerprints of the outputs whose numbers are in the submitted paper (2026-11-19).
# "num": numbers only; "text": numbers + labels (hex hashes, paths, times ignored);
# "all": every leaf; "csv": every cell.
FP_EXPECT = {
    "data/26_02_figure_values.json": [("num", "62da2b635ef12da3579cfef244a28cef2b7b98d040b5b4ba0e43781ef85f4e29"),
                                      ("text", "e348962664e32468f1af7a26b71526a4d8512981058645cded825353114eae69")],
    "data/26_03_timeline_values.json": [("all", "c9f706de245246cc49d0f60a0aa9a8f9f5166ec4c650dcc151f3fa188e00fa4d")],
    "data/26_04_effect_sizes.json": [("num", "0b47d7e9fb77d5c7f641f02723be816cefc4be75b62710c314e003529f42caec")],
    "data/26_04_effect_sizes.csv": [("csv", "b37aef4024ce32b0f3d0945f0910958bb08db245cf015d876eedfaa48d9f86c6")],
    "data/26_06_table_S1a.csv": [("csv", "bf0812284eb7f8eca554584a2219aceee257e4c33183adc849df366b610c77d2")],
    "data/26_06_table_S1b.csv": [("csv", "c9952c11fd6c54ae3ed87528d628451b32faef4040abe16e272367768ee84b45")],
    "data/26_06_table_S1c.csv": [("csv", "b37aef4024ce32b0f3d0945f0910958bb08db245cf015d876eedfaa48d9f86c6")],
    "models/26_09_reviewer_checks.json": [("num", "6fe24a3263c3a11b2c1e581376db6ee50b8d74ea1b55cada8044f9d13a36bc01")],
}
GITLOG_TIP, GITLOG_SHA = "2a3ac1e", "2383b9c7abf9063c4a935e3a02bd0c6538072fca02dc2a2bd434adabebd96abc"

JUDG = ["21_01", "21_02", "21_04", "21_06b", "21_20", "21_20f", "22_04", "25_05", "25_06f", "25_06g"]
OPEN = ["21_01", "21_02", "21_04", "21_06a", "21_06b", "21_16", "21_20", "21_20f", "22_02", "22_04",
        "25_05", "25_06f", "25_06g"]
PEV = ["21_01", "21_02", "21_04", "21_06b", "21_20", "21_20f", "22_04", "23_01", "23_02", "23_03",
       "25_05", "25_06f", "25_06g"]
OTHER_MODELS = ["21_06a_train.json", "21_09_summary.json", "21_16_summary.json", "23_01_summary.json",
                "23_02_summary.json", "23_03_summary.json", "25_08_intensity.json",
                "25_09_flag_descriptive.json", "21_10_gmpe_location_error.json"]
NEEDED = ({f"models/{k}_judgment.json" for k in JUDG if k != "21_01"}
          | {f"data/{k}_per_event.csv" for k in PEV if k != "21_01"}
          | {f"models/{k}_opened.json" for k in ("21_04", "21_20", "25_05", "21_06a", "22_02")}
          | {"models/23_01_summary.json", "models/23_02_summary.json", "models/23_03_summary.json",
             "models/21_10_gmpe_location_error.json"})

# PATTERNS-BEGIN (26_13 itself is not text-scanned: its text names these patterns)
EMAIL_RX = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
CRED_RX = (r"(?i)(Client\(\s*\\?['\"][^'\"\\]+\\?['\"]\s*,\s*\\?['\"][^'\"\\]+"
           r"|\b(user(name)?|passwd|password|pw|hinet_(user|pass)|token|api_?key)\s*=\s*\\?['\"][^'\"\\]{2,}"
           r"|machine\s+\S+\s+login\s+\S+\s+password)")
WORD_RX = r"(?i)\b(password|passwd|secret|token)\b"
HOME_RX = r"/Users/[A-Za-z0-9._-]+|/home/[A-Za-z0-9._-]+|/content/drive/MyDrive|Library/CloudStorage/[^\s'\"]+"
AI_RX = r"(?i)\bclaude\b|anthropic|chatgpt|openai|\bgpt-[0-9]"
BIZ_HASH = "9ddb4d96efe03f7a5252098d53e2ec6c663a9d7667a4ee6cff75e0d9db6b5fef"   # SHA-256 of the lower-case business name; the name is not stored


def has_biz(text):
    return [t for t in re.findall(r"[A-Za-z]{3,10}", text) if hashlib.sha256(t.lower().encode()).hexdigest() == BIZ_HASH]
SENS_NAME = re.compile(r"(^|/)(\.netrc|\.env[^/]*|id_rsa[^/]*|id_ed25519[^/]*|[^/]*\.pem|credentials[^/]*|"
                       r"\.DS_Store|\._[^/]*|[^/]*\.pyc)$")
DATA_NAME = re.compile(r"(^|/)(ct3_[^/]*\.txt|[^/]*\.(win|cnt|sac|mseed|msd|seed|segy|sgy|h5|hdf5|ch|sac_pz))$|"
                       r"\.\d{2}$", re.I)
MAGIC = [(b"\x89HDF", "HDF5"), (b"\x93NUMPY", "npy"), (b"PK\x03\x04", "zip/npz/pt/docx"),
         (b"\x1f\x8b", "gzip"), (b"BZh", "bzip2"), (b"\xfd7zXZ", "xz"), (b"\x28\xb5\x2f\xfd", "zstd"),
         (b"\x80\x02", "pickle"), (b"\x80\x03", "pickle"), (b"\x80\x04", "pickle"), (b"\x80\x05", "pickle")]
# PATTERNS-END
ALLOW_BIN_EXT = {".pdf", ".png"}

print(f"[26_13] SWIFT = {SW}\n[26_13] repo  = {RP}\n[26_13] mode  = {'APPLY' if A.apply else 'REPORT ONLY'}"
      f"\n[26_13] allow = {len(ALLOW)} accepted texts\n")
if not SW.is_dir(): sys.exit(f"[26_13] STOP: {SW} not found")
if not (RP / ".git").exists(): sys.exit(f"[26_13] STOP: {RP} is not a git repository")
STAGE_PARENT = Path(tempfile.mkdtemp(prefix="argus_public_stage_"))
PUB = STAGE_PARENT / "public"
STAGE = PUB / "paper"


def inside(p, root):
    try: p.resolve().relative_to(root.resolve()); return True
    except ValueError: return False


# ------------------------------------------------------------------ 1. collect
print("1. Collect")
PLAN, miss = [], []   # PLAN: (src Path, dst relative to paper/, role)


def add(src, dst, role, need=False):
    if src.is_file(): PLAN.append((src, dst, role))
    else: miss.append((str(src), need))


for p in sorted((SW / "src").glob("26_*.py")):
    if p.name.startswith("26_07"): continue                       # talk deck, not part of the paper
    add(p, f"src/{p.name}", "paper script")
for pat in ("23_01_*.py", "23_02_*.py", "23_03_*.py"):
    hits = sorted(q for q in (SW / "src").glob(pat) if not q.name.endswith(".py.py"))
    if not hits: miss.append((f"src/{pat}", False))
    for p in hits: add(p, f"src/{p.name}", "upstream check script")
for k in JUDG: add(SW / f"models/{k}_judgment.json", f"data/inputs/models/{k}_judgment.json", "frozen result",
                   f"models/{k}_judgment.json" in NEEDED)
for k in OPEN: add(SW / f"models/{k}_opened.json", f"data/inputs/models/{k}_opened.json", "opening record",
                   f"models/{k}_opened.json" in NEEDED)
for k in PEV: add(SW / f"data/{k}_per_event.csv", f"data/inputs/data/{k}_per_event.csv", "frozen result",
                  f"data/{k}_per_event.csv" in NEEDED)
for n in OTHER_MODELS: add(SW / f"models/{n}", f"data/inputs/models/{n}", "frozen result", f"models/{n}" in NEEDED)
WANT = {}                                                          # learned-model SHA -> tag
for k in JUDG:
    p = SW / f"models/{k}_judgment.json"
    if p.is_file():
        J = json.load(open(p))
        for key in ("model_sha256", "gate_pkl_sha256"):
            if J.get(key): WANT[J[key]] = f"{k}_{key.replace('_sha256', '')}"
FOUND = {}
for root in (SW / "models", RP):
    for p in root.rglob("*"):
        if not p.is_file() or ".git" in p.parts or inside(p, PAPER): continue
        if p.suffix.lower() not in (".pkl", ".joblib", ".bin", ".json") or p.stat().st_size > 50e6: continue
        if p.suffix == ".json" and not any(t in p.name for t in ("model", "gate", "ranker", "switch")): continue
        h = sha(p)
        if h in WANT and h not in FOUND: FOUND[h] = p
for h, tag in WANT.items():
    if h in FOUND:
        add(FOUND[h], f"data/inputs/models/{FOUND[h].name}", f"learned model ({tag})")
    else:
        miss.append((f"learned model sha {h[:12]} ({tag})", False))
for p in sorted((SW / "data").glob("26_*")):
    if p.is_file() and p.suffix in (".json", ".csv", ".md"): add(p, f"data/{p.name}", "paper output")
if (SW / "models/26_09_reviewer_checks.json").is_file():
    add(SW / "models/26_09_reviewer_checks.json", "models/26_09_reviewer_checks.json", "paper output")
for p in sorted((SW / "PDF").glob("26_*.pdf")):
    if not p.name.startswith("26_07"): add(p, f"PDF/{p.name}", "figure")
for n in ("pyproject.toml", "uv.lock", ".python-version"):
    if (SW / n).is_file(): add(SW / n, n, "environment")
# two learned models with the same file name would overwrite each other: rename with their tag
names = [d for _, d, _ in PLAN]
for i, (s, d, r) in enumerate(PLAN):
    if names.count(d) > 1 and r.startswith("learned model"):
        tag = r[r.index("(") + 1:-1]; PLAN[i] = (s, f"data/inputs/models/{tag}_{s.name}", r)
dsts = [d for _, d, _ in PLAN]
res("no two planned files share a destination", not {d for d in dsts if dsts.count(d) > 1})
print(f"  {len(PLAN)} files planned")
for s, need in miss: print(f"    {'MISSING (needed for the verification)' if need else 'not found'}: {s}")
res("all files needed for the verification exist", not any(n for _, n in miss))
mine = {p.name: sha(p) for p, _, r in PLAN if r == "paper script" and p.name in SENT}
for n in SENT:
    if n not in mine: res(f"script {n} present", False, "missing in ~/SWIFT/src")
diff = [n for n, h in mine.items() if h != SENT[n]]
res("26_xx scripts identical to the delivered versions", not diff,
    "differ: " + ", ".join(diff) if diff else "")

# ------------------------------------------------------------- 2. frozen check
print("\n2. Frozen scripts and results against the repository")
out = git("ls-files", "-z", "--cached", "--others", "--exclude-standard")
TREE = [RP / f for f in out.split("\0") if f]
TREE_FILES = [f for f in TREE if f.is_file() or f.is_symlink()]
byname = {}
for f in TREE_FILES:
    if f.is_file() and not inside(f, PAPER): byname.setdefault(f.name, []).append(f)
bad = []
for s, d, r in PLAN:
    if r not in ("frozen result", "opening record") or s.suffix != ".json": continue
    J = json.load(open(s))
    if not isinstance(J, dict): continue
    name, want_h = J.get("script"), J.get("script_sha256")
    if not name or not want_h: continue
    hs = {sha(q) for q in byname.get(name, [])}
    ok, how = want_h in hs, "committed"
    if not hs:                       # development/check scripts that were never registered in the repository
        loc = SW / "src" / name
        ok, how = loc.is_file() and sha(loc) == want_h, "~/SWIFT/src (not registered)"
        if ok and f"src/{name}" not in [d for _, d, _ in PLAN]:
            PLAN.append((loc, f"src/{name}", "development script"))
    if not ok: bad.append(f"{s.stem}: {name} {want_h[:12]}" + (" (not found)" if not hs else " (sha differs)"))
    print(f"  {s.stem:24s} {name:52s} {want_h[:12]}  {'match' if ok else 'NO MATCH'}  [{how}]")
res("every script named in a frozen result matches its SHA-256 (registered: committed copy)", not bad, " | ".join(bad))
diffc = []
for s, d, r in PLAN:
    if r in ("frozen result", "opening record") and s.name in byname:
        if sha(s) not in {sha(q) for q in byname[s.name]}: diffc.append(s.name)
res("released frozen results equal their committed copies", not diffc, ", ".join(diffc))
up = [f"{p.name} {sha(p)[:12]}" for p, _, r in PLAN if r == "upstream check script"]
res("upstream check scripts (recorded, no registered hash)", "INFO", " | ".join(up))

# -------------------------------------------------------------- 3. safety scan
print("\n3. Safety scan")
SELF_NAME = "26_13_release_assemble.py"
SELF_SHA = sha(Path(__file__).resolve())


def classify(name, data, findings, allow_bin_sha=()):
    """Add findings for one file (name, bytes)."""
    n = len(data)
    if SENS_NAME.search(name): findings["sensitive file name"].append(name)
    if DATA_NAME.search(name): findings["data/waveform-type file name"].append(name)
    if n > 50e6: findings["file over 50 MB"].append(f"{name} {n/1e6:.0f} MB")
    head = data[:8000]
    kind = next((t for m, t in MAGIC if data.startswith(m)), None)
    if kind is None and len(data) >= 8 and data[:6].isdigit() and data[6:7] in (b"D", b"R", b"Q", b"M"):
        kind = "miniSEED"
    is_bin = b"\0" in head or kind is not None
    if is_bin:
        if Path(name).suffix.lower() not in ALLOW_BIN_EXT and sha_bytes(data) not in allow_bin_sha:
            findings["binary file (not PDF/PNG/registered model)"].append(f"{name} ({kind or 'binary'}, {n/1e6:.2f} MB)")
        return
    txt = data.decode("utf-8", "replace")
    if has_biz(txt): findings["business name"].append(f"{name} ({len(has_biz(txt))}x)")
    if Path(name).name == SELF_NAME and sha_bytes(data) == SELF_SHA:
        return                       # this script: its text describes the other patterns themselves
    if n > 10e6 and Path(name).suffix.lower() in (".csv", ".txt", ".json", ".dat", ".tsv"):
        findings["large text table (check it holds no waveform samples)"].append(f"{name} {n/1e6:.1f} MB")
    for key, rx in (("credential literal", CRED_RX), ("e-mail address", EMAIL_RX),
                    ("word password/secret/token", WORD_RX), ("home or Drive path", HOME_RX),
                    ("AI tool name", AI_RX)):
        m = re.findall(rx, txt)
        if m:
            ex = m[0] if isinstance(m[0], str) else m[0][0]
            if key == "e-mail address":
                m = [x for x in m if not x.endswith(("users.noreply.github.com", ".png", ".pdf"))]
                if not m: continue
                ex = m[0]
            findings[key].append(f"{name} ({len(m)}x, e.g. {ex[:40]!r})")
    if name.endswith(".ipynb"):
        try:
            nb = json.loads(txt)
            no = sum(1 for c in nb.get("cells", []) if c.get("outputs"))
            if no: findings["notebook with stored outputs"].append(f"{name} ({no} cells)")
        except Exception: pass


SEV = {"credential literal": "FAIL", "e-mail address": "FAIL", "sensitive file name": "FAIL",
       "data/waveform-type file name": "FAIL", "file over 50 MB": "FAIL",
       "binary file (not PDF/PNG/registered model)": "FAIL", "business name": "FAIL",
       "large text table (check it holds no waveform samples)": "WARN", "word password/secret/token": "WARN",
       "AI tool name": "WARN", "notebook with stored outputs": "WARN", "home or Drive path": "INFO"}


def scan(files, label):
    F = {k: [] for k in SEV}
    for name, getter in files:
        try: data = getter()
        except Exception as e: F["binary file (not PDF/PNG/registered model)"].append(f"{name} (unreadable: {e})"); continue
        classify(name, data, F, allow_bin_sha=set(WANT))
    for k, sev in SEV.items(): res_items(f"{label}: {k}", F[k], sev)


# (a) state of the registration repository
import tarfile, io
HEAD = git("rev-parse", "HEAD").strip()
HEAD_DATE = git("log", "-1", "--date=iso", "--format=%ad", "HEAD").strip()
pushed = git("branch", "-r", "--contains", "HEAD").strip()
res("last commit of the registration repository is pushed to GitHub", bool(pushed), f"HEAD {HEAD[:7]} {HEAD_DATE}")
st = [l for l in git("status", "--porcelain").splitlines() if l.strip()]
res("uncommitted changes in the registration repository (not in the public copy)", "INFO",
    " | ".join(st[:10]))
# (b) the files of HEAD, unpacked into the staging folder
tar = git("archive", "--format=tar", "HEAD", raw=True)
with tarfile.open(fileobj=io.BytesIO(tar)) as tf:
    for m in tf.getmembers():
        if m.issym() or m.islnk(): res("registration repository: links", "WARN", m.name); continue
        if not m.isfile(): continue
        dst = PUB / m.name
        if not inside(dst, PUB): sys.exit(f"[26_13] STOP: unsafe path {m.name}")
        dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(tf.extractfile(m).read())
n_snap = sum(1 for f in PUB.rglob("*") if f.is_file())
print(f"  snapshot of {HEAD[:7]}: {n_snap} files")
# (c) remove author contact details from text records (never from scripts or results)
PROTECT = set()
for s_, d_, r_ in PLAN:
    if s_.suffix == ".json":
        try:
            J = json.load(open(s_))
            if isinstance(J, dict):
                PROTECT |= {v for k, v in J.items() if k.endswith("sha256") and isinstance(v, str)}
        except Exception: pass
PAREN = re.compile(r"[ \t]*[(（]([^()（）\n]{1,80})[)）]")


def redact(text):
    """Remove a parenthetical that holds an e-mail address or the business name."""
    return PAREN.sub(lambda m: "" if (re.search(EMAIL_RX, m.group(1)) or has_biz(m.group(1))) else m.group(0), text)
red = []
for f in sorted(PUB.rglob("*")):
    if not f.is_file() or f.suffix.lower() not in (".md", ".txt"): continue
    raw = f.read_bytes()
    if b"\0" in raw[:8000]: continue
    txt = raw.decode("utf-8", "replace"); new = txt
    new = redact(txt)
    if new != txt:
        rel = str(f.relative_to(PUB))
        if sha_bytes(raw) in PROTECT:
            res(f"redaction would change a registered file: {rel}", False); continue
        lines = [i + 1 for i, (a, b) in enumerate(zip(txt.splitlines(), new.splitlines())) if a != b]
        f.write_text(new)
        red.append((rel, sha_bytes(raw), sha(f), lines))
(PUB / "REDACTIONS.md").write_text(
    "# Changes made for the public copy\n\n"
    f"Source: commit {HEAD} ({HEAD_DATE}) of the private registration repository.\n"
    "Only author contact details (an e-mail address and a business name in the author line) were removed.\n"
    "No script, result, rule, or hypothesis was changed.\n\n"
    "| File | Lines changed | SHA-256 of the original | SHA-256 of this copy |\n|---|---|---|---|\n"
    + "".join(f"| {r} | {', '.join(map(str, l))} | `{a}` | `{b}` |\n" for r, a, b, l in red))
res("author contact details removed from records", "INFO", f"{len(red)} files: " + ", ".join(r for r, *_ in red))
(PUB / "REGISTRATION_LOG.txt").write_text(
    "# Every commit of the private registration repository up to the snapshot (hash, time, message)\n"
    + git("log", "--date=iso", "--format=%H %ad %s", "HEAD"))
# (e) what the released learned models hold (models that keep training samples could keep waveforms)
for s, d, r in PLAN:
    if not r.startswith("learned model") or s.suffix.lower() not in (".pkl", ".joblib"): continue
    try:
        import numpy as np
        try:
            import joblib; obj = joblib.load(s)
        except Exception:
            obj = pickle.load(open(s, "rb"))
        big, seen = [], set()

        def walk(o, path, depth=0):
            if id(o) in seen or depth > 6: return
            seen.add(id(o))
            if isinstance(o, np.ndarray):
                if o.size > 1e5: big.append(f"{path} {o.shape}")
            elif isinstance(o, dict):
                for k, v in o.items(): walk(v, f"{path}.{k}", depth + 1)
            elif isinstance(o, (list, tuple)):
                for i, v in enumerate(o[:50]): walk(v, f"{path}[{i}]", depth + 1)
            elif hasattr(o, "__dict__"):
                for k, v in vars(o).items(): walk(v, f"{path}.{k}", depth + 1)
        walk(obj, s.name)
        res_items(f"learned model {s.name}: arrays over 1e5 elements (stored training data?)", big, "WARN")
    except Exception as e:
        res(f"learned model {s.name}: content check", "WARN", f"could not load: {e}")

# ------------------------------------------------------------------ 4. apply
README = r"""# Paper materials

Code, frozen inputs and outputs for

> Kurosawa, I. How Much Do Waveform-Similar Past Earthquakes Improve Early Epicenters?
> Preregistered One-Shot Tests on Japanese Aftershock Sequences (submitted to Seismological Research Letters).

The rest of this repository is a copy of the registration repository (see the README at the top): the records,
the frozen test scripts, the run instructions, and the results, each committed before its test events were opened. Their commit times and the
Zenodo versions (10.5281/zenodo.23905464, 10.5281/zenodo.24190129, 10.5281/zenodo.24239732,
10.5281/zenodo.24247608, 10.5281/zenodo.24317791) time-stamp them. This folder adds what was
made after the tests: the scripts that drew every figure and table of the paper and the
descriptive checks of its supplement.

## Layout

| Path | Content |
|---|---|
| `src/26_01`–`26_06` | Figures 1–9 and Tables S1 (map and waveform, results, schematic and timeline, effect sizes, set-size control, Table S1) |
| `src/26_08`–`26_12` | Descriptive checks of the supplement (inventory, test-period terciles, memory truncation, DPRI catalog and intensity summary with Figure S1, mean removal) |
| `src/26_13` | Builds this folder, scans it, and reruns the scripts below to confirm the numbers |
| `src/26_15` | Figure S2 and Table S9 (full error distributions, descriptive) |
| `src/21_10`, `src/23_01`–`23_03` | Earlier checks used in Text S4 (intensity effect, spatial holdout, DPRI catalog) |
| `data/inputs/models`, `data/inputs/data` | Frozen results of the registered tests: judgment and opening records (JSON), per-event errors (CSV), the frozen learned models |
| `data/`, `models/`, `PDF/` | Outputs of the 26_xx scripts and the figure files |
| `data/paper_gitlog.txt` | Commit times of the registration repository read by Figure 3 |
| `MANIFEST.json`, `SHA256SUMS.txt` | Source, role and SHA-256 of every file here |

## Rerun without waveforms

```
cd paper
uv sync
uv run python src/26_04_paper_effect_sizes.py
uv run python src/26_06_paper_table_s1.py
uv run python src/26_02_paper_result_figures.py
uv run python src/26_03_paper_schematic_timeline.py
```
26_09 and 26_11 read a folder with `models/` and `data/` (as in the author's working folder):
copy `data/inputs/models`, `data/inputs/data` and the `data/26_10_*.json` files into one folder
and pass it with `--root` (26_09) or `--base` (26_11). `src/26_13_release_assemble.py` does this
and compares the outputs with the numbers of the paper.

## Scripts that need waveforms

26_01, 26_05, 26_10, 26_12 and the registered test scripts read caches of picks and waveform
segments built from Hi-net continuous records. Hi-net waveforms cannot be redistributed under the
NIED terms of use, and the West Tottori 2026 records were provided by S. Katoh (University of
Tokyo) and are not public. The caches are therefore not included. They can be rebuilt with a
Hi-net account by following the registration folders (download notebooks and cache scripts);
each judgment JSON gives the SHA-256 of the cache it used, so a rebuilt cache can be checked.

## Data sources

JMA unified hypocenter catalog; Hi-net continuous waveforms (NIED), obtained with HinetPy;
PhaseNet in SeisBench; the DPRI aftershock catalog of the 2016 Central Tottori earthquake
(Iio et al., 2018), https://www.eqhz.dpri.kyoto-u.ac.jp/images/2019/01/ct3_201711.txt
(not redistributed here; the comparison results are in `data/inputs/data/23_02_per_event.csv`
and `23_03_per_event.csv`).

## License

LICENSE_LINE
"""
MIT = """MIT License

Copyright (c) 2026 Isao Kurosawa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
TOP_README = r"""# ARGUS: preregistered tests of a waveform-similarity prior for early epicenters

Public copy of the registration repository of

> Kurosawa, I. How Much Do Waveform-Similar Past Earthquakes Improve Early Epicenters?
> Preregistered One-Shot Tests on Japanese Aftershock Sequences (submitted to Seismological Research Letters).

Every test of the paper was registered in a private GitHub repository before its test events were
opened: the records, the frozen test scripts with their SHA-256 hashes, the run instructions, and,
after each run, the results. This repository holds the files of that repository at commit
`HEAD_SHA` (HEAD_DATE), without its history.

* `REGISTRATION_LOG.txt` lists every commit of the registration repository (hash, time, message).
  The commit hashes cited in the registration records refer to that repository. Its history is
  available to the editor and reviewers on request.
* From the Northern Osaka 2018 registration onward, each registration was also time-stamped on
  Zenodo (10.5281/zenodo.23905464, 10.5281/zenodo.24190129, 10.5281/zenodo.24239732,
  10.5281/zenodo.24247608, 10.5281/zenodo.24317791).
* For this copy, author contact details were removed from N_RED record files. `REDACTIONS.md`
  lists each file with the SHA-256 of the original and of this copy. No script, result, rule, or
  hypothesis was changed; every frozen script keeps its registered SHA-256.
* `paper/` holds the scripts that produced every figure, table, and descriptive check of the
  paper, their inputs, and their outputs (see `paper/README.md`).

Hi-net waveforms are not redistributed, under the NIED terms of use. The West Tottori 2026 records
are not redistributed either.

License: MIT (see LICENSE).
"""
HEX = re.compile(r"^[0-9a-f]{12,64}$")


def _num(x):
    x = float(x)
    if math.isnan(x): return "nan"
    if math.isinf(x): return "inf" if x > 0 else "-inf"
    return repr(round(x, 6) + 0.0)


def fingerprint(p, kind):
    out = []
    if kind == "csv":
        with open(p, newline="") as f:
            for r, row in enumerate(csv.reader(f)):
                for c, v in enumerate(row):
                    try: out.append(f"{r},{c}={_num(v)}")
                    except ValueError: out.append(f"{r},{c}={v.strip()}")
    else:
        def walk(o, path):
            if isinstance(o, dict):
                for k, v in o.items(): walk(v, path + "/" + str(k))
            elif isinstance(o, list):
                for i, v in enumerate(o): walk(v, path + f"[{i}]")
            elif isinstance(o, bool): out.append(f"{path}={o}")
            elif isinstance(o, (int, float)): out.append(f"{path}={_num(o)}")
            elif kind == "all": out.append(f"{path}={o}")
            elif kind == "text" and isinstance(o, str) and not HEX.match(o) and "/" not in o \
                    and not re.match(r"^\d{4}-\d\d-\d\dT", o):
                out.append(f"{path}={o}")
        walk(json.load(open(p)), "")
    return hashlib.sha256("\n".join(sorted(out)).encode()).hexdigest()


def run(cmd, cwd):
    env = dict(os.environ, MPLBACKEND="Agg")
    r = subprocess.run([sys.executable, *cmd], cwd=cwd, capture_output=True, text=True, env=env)
    tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
    return r.returncode, " / ".join(tail)


if True:
    print(f"\n4. Build paper/ in the staging folder {STAGE}")
    for src, dst, role in PLAN:
        d = STAGE / dst; d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, d)
    gl = git("log", "--abbrev=7", "--date=iso", "--format=%h %ad %s", GITLOG_TIP, ok_codes=(0, 128))
    (STAGE / "data").mkdir(parents=True, exist_ok=True)
    (STAGE / "data/paper_gitlog.txt").write_text(gl)
    res("data/paper_gitlog.txt equals the log used for Fig. 3", sha(STAGE / "data/paper_gitlog.txt") == GITLOG_SHA)
    (STAGE / "README.md").write_text(README)
    print(f"  staged {len(PLAN)} files")

    print("\n5. Verify (rerun from the staged files)")
    with tempfile.TemporaryDirectory() as td:
        T = Path(td) / "paper"; shutil.copytree(STAGE, T)
        for rel in list(FP_EXPECT) + ["data/26_11_reviewer_supplement.json", "data/26_15_tail_stats.json",
                                      "data/26_15_tail_stats.csv", "data/26_15_table_S9.md"]:
            if (T / rel).exists(): (T / rel).unlink()                     # regenerate, never reuse
        for s in ("26_04_paper_effect_sizes.py", "26_06_paper_table_s1.py",
                  "26_02_paper_result_figures.py", "26_03_paper_schematic_timeline.py"):
            rc, tail = run([f"src/{s}"], T)
            res(f"rerun {s}", rc == 0, tail if rc else "")
        W = Path(td) / "work"
        for sub in ("models", "data", "PDF"): (W / sub).mkdir(parents=True)
        for sub, dst in (("data/inputs/models", "models"), ("data/inputs/data", "data")):
            for f in (STAGE / sub).glob("*"):
                if f.is_file(): shutil.copy2(f, W / dst / f.name)
        for f in (STAGE / "data").glob("26_10_memory_truncation_*.json"): shutil.copy2(f, W / "data" / f.name)
        rc, tail = run([str(STAGE / "src/26_09_reviewer_checks.py"), "--root", str(W)], W)
        res("rerun 26_09_reviewer_checks.py", rc == 0, tail if rc else "")
        if (W / "models/26_09_reviewer_checks.json").exists():
            (T / "models").mkdir(exist_ok=True)
            shutil.copy2(W / "models/26_09_reviewer_checks.json", T / "models/26_09_reviewer_checks.json")
        rc, tail = run([str(STAGE / "src/26_11_reviewer_supplement.py"), "--base", str(W)], W)
        res("rerun 26_11_reviewer_supplement.py", rc == 0, tail if rc else "")
        for rel, checks in FP_EXPECT.items():
            rerun, staged = T / rel, STAGE / rel
            for kind, want_h in checks:
                ok_r = rerun.exists() and fingerprint(rerun, kind) == want_h
                res(f"rerun {rel} [{kind}] = submitted paper", ok_r, "" if rerun.exists() else "not produced")
                if staged.exists():
                    res(f"released {rel} [{kind}] = submitted paper", fingerprint(staged, kind) == want_h)
            if not staged.exists() and rerun.exists() and all(fingerprint(rerun, k) == h for k, h in checks):
                staged.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(rerun, staged)
                print(f"    released the rerun output {rel} (no Mac copy existed)")
        a, b = W / "data/26_11_reviewer_supplement.json", STAGE / "data/26_11_reviewer_supplement.json"
        if a.exists() and b.exists():
            res("rerun 26_11 numbers = released Mac output", fingerprint(a, "num") == fingerprint(b, "num"))
        else:
            res("rerun 26_11 numbers = released Mac output", "WARN", "Mac output missing" if a.exists() else "rerun failed")
        rc, tail = run(["src/26_15_error_distributions.py"], T)
        res("rerun 26_15_error_distributions.py", rc == 0, tail if rc else "")
        for rel, kind in (("data/26_15_tail_stats.csv", "csv"), ("data/26_15_tail_stats.json", "num")):
            a, b = T / rel, STAGE / rel
            if a.exists() and b.exists():
                res(f"rerun {rel} [{kind}] = released Mac output", fingerprint(a, kind) == fingerprint(b, kind))
            else:
                res(f"rerun {rel} [{kind}] = released Mac output", "FAIL",
                    "Mac output missing (run 26_15 on the Mac first)" if a.exists() else "rerun failed")
        a, b = T / "data/26_15_table_S9.md", STAGE / "data/26_15_table_S9.md"
        res("rerun data/26_15_table_S9.md = released Mac output",
            a.exists() and b.exists() and a.read_text() == b.read_text())
        for f in sorted((T / "PDF").glob("26_0[23]_*.pdf")):
            if not (STAGE / "PDF" / f.name).exists():
                shutil.copy2(f, STAGE / "PDF" / f.name); print(f"    released the rerun figure PDF/{f.name}")
        res("figure PDFs", "INFO", "checked through their value JSON (PDF bytes carry creation dates)")

    # license text in the README must match the LICENSE that will be in the repository
    (STAGE / "README.md").write_text(README.replace("LICENSE_LINE", "MIT License (see LICENSE at the repository root)."))
    if not any(p.name.upper().startswith(("LICENSE", "LICENCE", "COPYING")) for p in PUB.iterdir()):
        (PUB / "LICENSE").write_text(MIT)
    top = PUB / ("README.md" if not (PUB / "README.md").exists() else "PUBLIC_COPY.md")
    top.write_text(TOP_README.replace("HEAD_SHA", HEAD).replace("HEAD_DATE", HEAD_DATE)
                   .replace("N_RED", str(len(red))))
    man = []
    for f in sorted(STAGE.rglob("*")):
        if f.is_file() and f.name not in ("MANIFEST.json", "SHA256SUMS.txt", "26_13_release_report.json"):
            rel = str(f.relative_to(STAGE))
            hit = next(((s, r) for s, d, r in PLAN if d == rel), None)
            src = ("generated by 26_13" if hit is None else
                   str(hit[0].relative_to(SW)) if inside(hit[0], SW) else "repo:" + str(hit[0].relative_to(RP)))
            man.append({"path": rel, "sha256": sha(f), "bytes": f.stat().st_size, "source": src,
                        "role": hit[1] if hit else "generated"})
    vers = {}
    for m in ("numpy", "scipy", "pandas", "matplotlib", "sklearn"):
        try: vers[m] = __import__(m).__version__
        except Exception: vers[m] = None
    json.dump({"created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "python": platform.python_version(), "packages": vers, "files": man},
              open(STAGE / "MANIFEST.json", "w"), indent=1)
    (STAGE / "SHA256SUMS.txt").write_text("".join(f"{m['sha256']}  {m['path']}\n" for m in man))
    print("\n6. Scan of the whole public copy")
    scan([(str(f.relative_to(PUB)), (lambda f=f: f.read_bytes())) for f in PUB.rglob("*") if f.is_file()],
         "public copy")
    print(f"  public copy: {sum(1 for f in PUB.rglob('*') if f.is_file())} files")

# ------------------------------------------------------------------- summary
nf = sum(s == "FAIL" for _, s, _ in RESULT); nw = sum(s == "WARN" for _, s, _ in RESULT)
ready = nf == 0 and nw == 0
json.dump([{"check": c, "status": s} for c, s, _ in RESULT], open(STAGE / "26_13_release_report.json", "w"), indent=1)
if A.apply and ready:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    for f in PUBLIC.iterdir():                                   # keep an existing .git, replace the rest
        if f.name == ".git": continue
        shutil.rmtree(f) if f.is_dir() and not f.is_symlink() else f.unlink()
    for f in PUB.iterdir():
        (shutil.copytree if f.is_dir() else shutil.copy2)(f, PUBLIC / f.name)
    shutil.rmtree(STAGE_PARENT, ignore_errors=True)
elif A.apply:
    print(f"\n[26_13] nothing written; the staged public copy is kept for inspection: {PUB}")
else:
    shutil.rmtree(STAGE_PARENT, ignore_errors=True)
print("\n" + "=" * 110)
w = max(len(c) for c, _, _ in RESULT)
for c, s, d in RESULT:
    if s != "PASS": print(f"{s:5s}  {c:{w}s}  {d[:150]}")
print(f"(and {sum(s == 'PASS' for _, s, _ in RESULT)} PASS)")
print("=" * 110)
print(f"[26_13] {len(RESULT)} checks: {nf} FAIL, {nw} WARN  ({time.time() - T0:.0f} s)")
if ready and A.apply: print(f"[26_13] READY FOR RELEASE: public copy written to {PUBLIC}")
elif ready: print("[26_13] all checks pass (report only): run again with --apply to write the public copy")
else: print("[26_13] NOT READY: resolve every FAIL and WARN (fix, or accept a reviewed WARN with --allow)")
