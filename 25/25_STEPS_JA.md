# 25 島根県西部 2018 — 回す手順(Mac の準備 0 部 + Colab のセル N1〜N18 + Mac の M1〜M7)

ノート: `25_shimane2018_colab.ipynb`(この束に入っている。セルの番号はノートの見出しと同じ)。
形は長野(24)の手順と同じで、名前と、G-clock2 の (d) の読み方(N14b)・記録をまとめるセル(N18)・25_09(M2d・M5d)を足した所だけが違う。

- **ノートは「すべてのセルを実行」を使わない。** 上から 1 つずつ、この手順の順に回す(N5 の最初で 0 部が済んだかを聞いて止まる)。
- スクリプトの表示の「セル n」は、このノートの「Nn」のこと(例: 「セル 8b」= N8b、「セル 3」= N3)。「セル N10」「セル 10」は N10a・N10b のこと。
- Colab のどこかで止めた時(STOP・止める判定)も、N18 で記録をまとめ、Mac の M6a で results に入れて commit する(止めた記録も事前登録の結果として残す)。
- **push は 0-D の 1 回と、最後の M6b の 1 回だけ。** 登録の hash・DOI は記録を書き換えずに `results/25_registration.txt` に書く。

---

## 0 部 Mac: 置く・確かめる・push する・外部の時刻の記録を取る(N5 の前に必ず)

### 0-A 束を置いて、SHA-256 を確かめる
```bash
mkdir -p ~/ARGUS_prereg_21_04/25
cd ~/Downloads && unzip -o 25_bundle.zip -d ~/ARGUS_prereg_21_04/25/
cd ~/ARGUS_prereg_21_04/25 && ls && ls dev | wc -l && shasum -a 256 *.py
```
- Safari が zip を自動で展開した時は、2 行目(unzip)を回さず、代わりに `cp -R ~/Downloads/25_bundle/ ~/ARGUS_prereg_21_04/25/` を回してから 3 行目を回す。
- 名前が `25_bundle (1).zip` になった時は、2 行目を `cd ~/Downloads && unzip -o "25_bundle (1).zip" -d ~/ARGUS_prereg_21_04/25/` にする(" " で囲む)。
- 期待: 1 つ目の `ls` は 17 個だけ(.py 12 本・.md 3 つ・.ipynb 1 つ・フォルダ `dev`)。`__pycache__` が無い。`ls dev | wc -l` は `18`。
- 期待: 12 行の値が、事前登録の記録 `25_preregistration_shimane2018.md` の 9 節の表と全桁で同じ。

### 0-B 冒頭のチェックを確かめて埋める
- 記録の 1 節の表の値を、各系列の結果の JSON(`~/ARGUS_prereg_21_04/results_21_04/`・`results_21_20/`・`24/results/` など)と照らす(事前登録 14 節の 6)。
```bash
ls -d ~/SWIFT/data/shimane2018_processed; ls ~/SWIFT/models | grep 25_0; echo "check done"
grep -rnE "@@[A-Z0-9_]+@@" ~/ARGUS_prereg_21_04/25; echo "grep done"
```
- 期待: 1 行目は `No such file or directory` の後に `check done` だけ(島根の出力がまだ何も無い)。
- 期待: `grep done` の前に何も出ない(凍結するファイルに未記入の印が残っていない)。
- ブラウザで Drive に `ARGUS_shimane2018` のフォルダが無いことを確かめる。
- 記録 `25_preregistration_shimane2018.md` の冒頭の 2 つの `[ ]` を、確かめてから `[x]` にする(テキストエディタで)。

### 0-C Colab で使うものを Drive に、Mac で使う 5 本を ~/SWIFT/src に置く
```bash
shasum -a 256 ~/SWIFT/data/catalog/jma_raw/h2018.zip
```
- 期待: 先頭が `ea8eb186db3f`(25_00 で開いた版)。違えば止めて貼る。
- Drive の `マイドライブ/ARGUS/src/` に置く(ブラウザか Drive for desktop): `25_01_…`・`25_02_…`・`25_03_…`・`25_03h_…`・`25_04d_…`・`25_04e_…`。
  `24_07_causal_picks.py` は長野の時の v3 が既にあり、同じものなので置き直さない(N2 で SHA-256 を照らす)。
```bash
cp ~/SWIFT/data/catalog/jma_raw/h2018.zip ~/Downloads/h2018_25_00.zip && shasum -a 256 ~/Downloads/h2018_25_00.zip
```
- 期待: 先頭が `ea8eb186db3f`。`~/Downloads/h2018_25_00.zip` を、Drive の `マイドライブ/ARGUS/data/catalog/jma_raw/` に**そのまま**上げる
  (Drive で名前を変えない。同じ所に大阪の時の古い `h2018.zip` があっても触らない。N5 はこの `h2018_25_00.zip` を `--hypo` で読む)。
```bash
cp ~/ARGUS_prereg_21_04/25/25_05_shimane2018_similarity_confirmation.py ~/ARGUS_prereg_21_04/25/25_06f_shimane2018_learned_test.py \
   ~/ARGUS_prereg_21_04/25/25_06g_shimane2018_gate_test.py ~/ARGUS_prereg_21_04/25/25_08_shimane2018_intensity_descriptive.py \
   ~/ARGUS_prereg_21_04/25/25_09_shimane2018_flag_descriptive.py ~/SWIFT/src/
cd ~/SWIFT && shasum -a 256 src/25_05_*.py src/25_06f_*.py src/25_06g_*.py src/25_08_*.py src/25_09_*.py
```
- 期待: 5 行が 9 節の値と同じ。

### 0-D commit・push(1 回だけ)
```bash
cd ~/ARGUS_prereg_21_04
git add 25
git check-ignore -v 25/* 25/dev/*; echo "ignore check done"
git status   # .DS_Store が出たら git restore --staged 25/.DS_Store 25/dev/.DS_Store で外す
git commit -m "25: preregistration of the one-shot test on Western Shimane 2018 (fifth sequence): record, 12 scripts, steps, notebook, diff log, dev of G-clock2 (d)"
git push
git log -1 --format=%H
```
- 期待: `ignore check done` の前に何も出ない(何か出たら、そのファイルが push されないので止めて貼る)。
- 期待: `git status` の `new file:` は `25/` の 34 個(上の 16 個と `dev/` の 18 個)。
- 表示された hash(40 文字)を控える(0-F で使う)。

### 0-E 外部の時刻の記録(Zenodo の新しい版)
- Zenodo の記録(最新は v4 の 10.5281/zenodo.24247608)を開き「New version」。前の版のファイルは残したまま、`25/` の 16 個と `25/dev/` の 18 個を足す
  (Zenodo はフォルダを持たないので、ファイルだけを上げる。名前は重ならない)。
- 題に「v5: preregistration 25 (Western Shimane 2018)」、説明に 0-D の commit の hash を書く。
- 非公開期間(embargo)の終わりの日は、前の版と同じにする。公開する。
- 公開後のページに出る**新しい版の DOI**(24247608 ではない)と、公開した日時を控える。

### 0-F 登録の控え(commit はまだしない)
```bash
mkdir -p ~/ARGUS_prereg_21_04/25/results && touch ~/ARGUS_prereg_21_04/25/results/25_registration.txt && open -e ~/ARGUS_prereg_21_04/25/results/25_registration.txt
```
- 上の行がテキストエディタで `25_registration.txt`(空のファイル)を開く。次を書いて保存する:
  0-D の commit の hash(40 文字)・0-E の DOI と公開した日時・確定した日(UTC)。
- この後、N12b・N16 で控える SHA-256 もここに書き足す。commit は M6b で結果と一緒に行う(2 回目の登録の push はしない)。

---

## 1 部 Colab: 震源と波形(N1〜N9)

### ランタイム
- 「ランタイム → ランタイムのタイプを変更 → CPU・ハイメモリ」。**最後まで変えない**(途中で変えると `/content` が消える)。

### N1 — Drive と道具
```python
from google.colab import drive; drive.mount('/content/drive')
!pip -q install HinetPy==0.13.0 seisbench==0.12.7 obspy
import h5py, torch, numpy, scipy, obspy, seisbench; print(h5py.__version__, torch.__version__, numpy.__version__, scipy.__version__, 'obspy', obspy.__version__, 'seisbench', seisbench.__version__)
```
- 期待: `seisbench 0.12.7`(24_07 の dev と同じ版)。表示の 1 行を控える(事前登録 14 節の 7)。
- pip の後に「セッションを再起動」と出たら、再起動して N1 からやり直す。

### N2 — 場所の変数と、スクリプト・震源ファイルの SHA-256
```python
import hashlib, os
SRC = '/content/drive/MyDrive/ARGUS/src'
CAT = '/content/drive/MyDrive/ARGUS/data/catalog'
DRV = '/content/drive/MyDrive/ARGUS_shimane2018'
LO  = '/content/ARGUS_shimane2018'
R1  = 'data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt'
HYPO = f'{CAT}/jma_raw/h2018_25_00.zip'
REF_H5 = '/content/drive/MyDrive/2026WTottori/data/waves/tottori_all_100Hz.h5'
REF_CACHE_2026 = '/content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt'
EXP = {  # 事前登録の記録の 9 節と同じ値
    '25_01_shimane2018_jma_catalog.py': 'a147484fea5472cbb2364052d9a153d22425c7ec10630cc729ef223280240ce7',
    '25_02_shimane2018_hinet_to_h5.py': '220d3c72e0bb4631d1f180571e0a7e177701662a406a3eef4b3c1a87e615c519',
    '25_03_shimane2018_realpick_cache_colab.py': 'd58b389f4f64e4b068b75f7b6a9ee41d23a241ec0579a90cbf81ffe0d53363f4',
    '25_03h_shimane2018_overlap_exclusion.py': 'e676ea476c098c68ee6461f21d40df1541a799c6497994d85a32df26620cebaa',
    '25_04d_shimane2018_gclock2_picks.py': '419a09119d38e89a04c7504cefd361aef1ab7a531fda95b8f77501d9dad50b4f',
    '25_04e_shimane2018_station_pick_diagnose.py': '25baefde700ff9d867a518d6bd306afd2b1a8c97ae6fcadd25120133ec629d06',
    '24_07_causal_picks.py': 'b9b2fd5c8855c52f2e3a528e695374af752db3b0de6f789942e6da8824c2d14b',
}
for n, h in EXP.items():
    got = hashlib.sha256(open(f'{SRC}/{n}', 'rb').read()).hexdigest() if os.path.exists(f'{SRC}/{n}') else 'MISSING'
    print('OK  ' if got == h else 'NG  ', n, got)
hh = hashlib.sha256(open(HYPO, 'rb').read()).hexdigest() if os.path.exists(HYPO) else 'MISSING'
print('OK  ' if hh.startswith('ea8eb186db3f') else 'NG  ', 'h2018_25_00.zip', hh[:12])
print('名前に (1) などが付いた写し:', [f for f in os.listdir(SRC) if f.startswith(('25_', '24_07')) and '(' in f])
```
- 期待: 8 行とも `OK`。最後の行が `[]`。`NG` が 1 つでもあれば止める。

### N3 — win32tools(catwin32・win2sac_32)
- このノートの N3 のセルを回す(中身は大阪・長野のノートのセル 3 と同じ。`マイドライブ/KRITES/bin/` に作ったものを写すだけ)。
- 期待: `which catwin32 win2sac_32` に 2 つのパスが出て、`file` に `ELF` と出る。`Mach-O` と出たら Mac で作ったものなので、`KRITES/bin` の
  2 つを消して、もう一度このセルを回す。

### N4 — Hi-net の資格情報(ノートに書き残さない)
```python
import os, getpass
os.environ['HINET_USER'] = getpass.getpass('Hi-net user: ')
os.environ['HINET_PASS'] = getpass.getpass('Hi-net password: ')
```

### N5 — 25_01: 気象庁の震源(h2018)。**0 部が全て済んでから**
```python
assert input('0 部(push・Zenodo の新しい版・登録の控え)は全て済んだか? 済んだら yes: ').strip() == 'yes', '0 部を先に'
!python {SRC}/25_01_shimane2018_jma_catalog.py --hypo {HYPO}; echo "exit code: $?"
```
- 期待: `震源ファイル h2018_25_00.zip(SHA-256 ea8eb186db3f…`、
  `[25_01] 本震: 2018-04-09 01:32:30.810000 JST  35.1847N 132.5867E  深さ 12.13 km  M6.1D  精度 1  (想定の 1 分 01:32:00〜01:33:00 JST の中か: True。要確認の項目)`、
  `箱 [35.0347, 35.3347, 132.4117, 132.7617]`、`数:` の `all` 3361・`mj_ge_1p5` 389・`test_candidates_1p5_to_2p0_after_72h` 41(どれも 25_00 と同じ)、
  `試験の候補 41 ≥ 30: 次へ進める`。
- 違う値が出たら止めて出力を貼る。
- h2018 の確定の段階(事前登録 14 節の 4)を、気象庁の震源ファイルのページで確かめて `results/25_registration.txt` に書く。
- 出力: `{CAT}/jma_shimane2018.csv`・`{CAT}/25_01_shimane2018_catalog.json`・`/content/drive/MyDrive/ARGUS/PDF/25_01_shimane2018_catalog.pdf`

### N6 — 25_02: 取る計画だけ
```python
!python {SRC}/25_02_shimane2018_hinet_to_h5.py --ref-h5 "{REF_H5}" --dry-run; echo "exit code: $?"
```
- 確かめること: `参照の z-score の確認 … PASS`、候補局 60、区切りの数と分の合計、置き場所の見込み。

### N7 — 煙試験(本震の区間に掛かる区切りを先に 3 つ)
```python
!python {SRC}/25_02_shimane2018_hinet_to_h5.py --ref-h5 "{REF_H5}" --max-blocks 3; echo "exit code: $?"
```

### N7b — 煙試験の分だけで組み立ててゲートを見る
```python
!python {SRC}/25_02_shimane2018_hinet_to_h5.py --ref-h5 "{REF_H5}" --assemble --partial; echo "exit code: $?"
```
- G-ref・G-dup が PASS。`PDF/25_02_mainshock_partial.pdf` で本震の P が予想の P の印にそろっているか。G-clock の FAIL は記録だけ。
- 煙試験の G-cover は区切りが 3 つだけなので低くてよい(本番の判定は N9)。G-ref・G-dup の FAIL は止めて貼る。

### N8 — 全ての区切りを取る(止まっても同じセルで続きから)
```python
!python {SRC}/25_02_shimane2018_hinet_to_h5.py --ref-h5 "{REF_H5}"; echo "exit code: $?"
```
- 最後の行が `終わり: 残りの区切り 0/N`(全部済んだ後に回すと `取る区切りが無い(全部済み)`)になるまで回し直す。取れた割合が 0.98 以上で、何度回しても取れない区切りだけが残った時だけ、N9 に `--allow-missing`。

### N8b — Colab が切れた直後だけ
```python
!python {SRC}/25_02_shimane2018_hinet_to_h5.py --ref-h5 "{REF_H5}" --restore-selection --break-lock; echo "exit code: $?"
```

### N9 — 組み立てとゲート(Colab のローカルで)
```python
!df -h /content
!mkdir -p {LO}/data
!cp -r {DRV}/data/blocks {LO}/data/ && cp {DRV}/data/25_02_plan.json {LO}/data/
# N8 で取れない区切りだけが残った時(取れた割合 0.98 以上)だけ、下の行の --out {LO} の後に --allow-missing を付ける
!python {SRC}/25_02_shimane2018_hinet_to_h5.py --ref-h5 "{REF_H5}" --assemble --out {LO}; echo "exit code: $?"
!mkdir -p {DRV}/data/catalog {DRV}/PDF && cp {LO}/data/25_02_report.json {DRV}/data/ && cp {LO}/PDF/25_02_*.pdf {DRV}/PDF/
!cp {LO}/data/catalog/stations_shimane2018.csv* {DRV}/data/catalog/
!ls -la {LO}/data/waves {LO}/data/catalog
```
- `STOP(G-clock だけ)` → 進む(`shimane2018_100Hz_FAILED.h5` と `stations_shimane2018.csv.part` を N10a が自分で選ぶ)。それ以外の STOP は止めて出力を貼る。
- G-cover が 0.80〜0.95 の「注意」は進む(止めるのは 0.80 未満だけ。事前登録 5.2 節)。
- 報告の `version` が `v1 (=24_02 v1 = 21_20b v1 + window scale)`。`df -h` の空きが、N6 の見込み(区切り + h5)より大きいこと。

---

## 2 部 Colab: キャッシュ・R1・時刻の確かめ・H5 の材料(N10〜N18)

### N10a — 変数だけ(h5・観測点・箱)。Colab が切れた後もこのセルだけを回し直す
```python
import json, os
S = json.load(open(f'{CAT}/25_01_shimane2018_catalog.json')); BOX = ' '.join(str(x) for x in S['box']); print('box', BOX)
H5 = f'{LO}/data/waves/shimane2018_100Hz.h5'
STA = f'{LO}/data/catalog/stations_shimane2018.csv'
if not os.path.exists(H5):            # G-clock だけの FAIL の時(事前登録 5.2 節)
    H5, STA = f'{LO}/data/waves/shimane2018_100Hz_FAILED.h5', STA + '.part'
IDX = f'{LO}/data/tottori_processed/h5_index_{os.path.basename(H5)[:-3]}.npz'   # 25_03 が作る窓の索引(N15 で使う)
print(H5, os.path.exists(H5)); print(STA, os.path.exists(STA))
```
- 期待: `box 35.0347 35.3347 132.4117 132.7617`、2 行とも `True`。

### N10b — 25_03 の煙試験(10 地震)
```python
!python {SRC}/25_03_shimane2018_realpick_cache_colab.py --h5 {H5} --jma {CAT}/jma_shimane2018.csv --stations {STA} --min-mag 1.5 --box {BOX} --base {LO} --tag _shimane2018_smoke --max-events 10; echo "exit code: $?"
```

### N11 — 25_03 の本番(1 回だけ)
```python
!python {SRC}/25_03_shimane2018_realpick_cache_colab.py --h5 {H5} --jma {CAT}/jma_shimane2018.csv --stations {STA} --min-mag 1.5 --box {BOX} --base {LO} --tag _shimane2018_m15; echo "exit code: $?"
!python -c "import json;print('25_03 script_sha256', json.load(open('{LO}/models/locator/15_01c_build_report_shimane2018_m15.json'))['script_sha256'])"
```
- 出力: `{LO}/data/tottori_processed/tottori_parsed_realpick_shimane2018_m15.pt`・`{LO}/models/locator/15_01c_build_report_shimane2018_m15.json`
- 最後の行の値が 9 節の 25_03 の値と同じこと。

### N11b — キャッシュをすぐ Drive に写す
```python
!mkdir -p {DRV}/data/tottori_processed {DRV}/models/locator
!cp {LO}/data/tottori_processed/tottori_parsed_realpick_shimane2018_m15.pt {DRV}/data/tottori_processed/
!cp {LO}/models/locator/15_01c_build_report_shimane2018_m15.json {DRV}/models/locator/
```

### N12 — 25_03h: R1(重なった地震を除く)
```python
!python {SRC}/25_03h_shimane2018_overlap_exclusion.py --cache {LO}/data/tottori_processed/tottori_parsed_realpick_shimane2018_m15.pt --catalog {CAT}/jma_shimane2018.csv --report {LO}/data/25_02_report.json --out {LO}; echo "exit code: $?"
```
- 期待: `G-match PASS`、`除いた後: … 試験の候補 N(前 M)` で N ≥ 30、`出力: …_shimane2018_m15_r1.pt  … SHA-256 …`。
- `STOP(R2)`・`STOP(R3)` → 止める(R3 は INCONCLUSIVE として報告。事前登録 5.4 節)。
- 本震の不一致・G-match などその他の STOP も止めて出力を貼る。

### N12b — R1 の出力をすぐ Drive に写す
```python
!mkdir -p {DRV}/data/tottori_processed && cp {LO}/{R1} {DRV}/data/tottori_processed/ && cp {LO}/data/25_03h_overlap_exclusion.json {DRV}/data/
!sha256sum {LO}/{R1} {DRV}/data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt
!python -c "import json;print('input_cache_sha256', json.load(open('{LO}/data/25_03h_overlap_exclusion.json'))['input_cache_sha256'])"
```
- 期待: 最初の 2 行の値が同じ。この値と最後の行の値を、25_05 を開く前に `results/25_registration.txt` に書く(事前登録 6 節)。
- N12 が STOP(R2・R3 など)の時は、このセルを回さず、`!mkdir -p {DRV}/data && cp {LO}/data/25_03h_overlap_exclusion.json {DRV}/data/` だけを回して記録を残し、N18 へ。

### N13 — 25_04d: G-clock2
```python
!python {SRC}/25_04d_shimane2018_gclock2_picks.py --base {LO} --cache {R1} --ref-cache {REF_CACHE_2026}; echo "exit code: $?"
```
- 最初の行が `selftest: 新しい (d)(…)の 7 例に合格`。
- 最後の行が `STOP(G-clock2)`(条件の FAIL)の時は、ここでは止めずに N14・N14b に進む(扱いは事前登録 5.3 節で決まっている)。
- それ以外の STOP(検測 100 未満・日/局が 0・報告が無い・selftest)は JSON が書かれないので、止めて出力を貼る。

### N14 — 25_04e(必ず回す)
```python
!python {SRC}/25_04e_shimane2018_station_pick_diagnose.py --base {LO} --cache {R1} --ref-cache {REF_CACHE_2026}; echo "exit code: $?"
```

### N14b — G-clock2 の判定に要る値を表示する(読むだけ)
```python
import json, csv
J = json.load(open(f'{LO}/data/25_04d_gclock2.json'))
for k in ['pass_all', 'pass_day', 'pass_station', 'pass_block', 'pass_events', 'pass_measured_frac', 'gclock2_pass']: print(k, J[k])
B = J['event_block_d']
print('  (d) 本震', J['mainshock_jst'], '+ 72 h より後の地震', B['n_events'], ' 窓', B['n_windows'], ' 最大', B['max_abs_s'], ' 窓', B['worst_window_start_jst'], '〜', B['worst_window_end_jst'])
for x in J['gclock_events']:
    print('  (e)', x['origin_jst'], 'Mj', x['mj'], 'found_dt_s', round(x['found_dt_s'], 3), 'n_picks', x['n_picks'], 'PASS' if x['pass_'] else 'FAIL')
rows = list(csv.DictReader(open(f'{LO}/data/25_04e_station_picks.csv')))
near = [r for r in rows if float(r['epi_from_mainshock_km']) <= 80.0 and int(r['n']) >= 20]
bad_near = [r for r in near if abs(float(r['dev_s'])) > 1.0]
bad_far = [r for r in rows if float(r['epi_from_mainshock_km']) > 80.0 and int(r['n']) >= 20 and abs(float(r['dev_s'])) > 1.0]
print('(c-near) 80 km 以内・n ≥ 20 の局', len(near), '  |dev_s| > 1.0 s の局', len(bad_near))
for r in bad_near: print('   ', r['station'], r['epi_from_mainshock_km'], 'km  n', r['n'], ' dev_s', r['dev_s'])
print('(c-far) 80 km より遠い・n ≥ 20 で |dev_s| > 1.0 s の局', len(bad_far))
for r in bad_far: print('   ', r['station'], r['epi_from_mainshock_km'], 'km  n', r['n'], ' dev_s', r['dev_s'])
```
- 読み方(事前登録 5.3 節): `pass_all`・`pass_day`・`pass_block`・`pass_events`・`pass_measured_frac` のどれかが False → 止める。
  (c-near) の外れが 1 局でもある、または 80 km 以内・n ≥ 20 の局が 0 → 止める。`pass_station` だけが False → 進み、決まった印を付ける。
  `gclock2_pass` が True → 進む。
- (c-far) の時に付ける印の英文・日本文は、事前登録 5.3 節の 4 にある。止める時も N14c と N18 は回す(記録を残す)。**変更の記録は足さない**(5.3 節の 6)。

### N14c — G-clock2 の出力をすぐ Drive に写す
```python
!mkdir -p {DRV}/data {DRV}/PDF && cp {LO}/data/25_04d_gclock2.json {LO}/data/25_04e_station_picks.csv {DRV}/data/ && cp {LO}/PDF/25_04*.pdf {DRV}/PDF/
```

### N15 — 24_07: H5 の材料(τ までの波形だけの検測。全ての地震。1 回だけ)
```python
!python {SRC}/24_07_causal_picks.py --h5 {H5} --cache {LO}/{R1} --stations {STA} --index {IDX} --base {LO} --tag _shimane2018 --all-events --label "Western Shimane 2018"; echo "exit code: $?"
!mkdir -p {DRV}/data {DRV}/models {DRV}/PDF && cp {LO}/data/24_07_causal_picks_shimane2018.csv {DRV}/data/ && cp {LO}/models/24_07_causal_picks_shimane2018.json {DRV}/models/ && cp {LO}/PDF/24_07_*.pdf {DRV}/PDF/
```
- 期待: `selftest: 元の値への戻し(v3)・…に全て合格`、`h5 の値: win_mean・win_std から元の値に戻して使う(v3)`、
  `成分の並び ENZ → … ['EW', 'NS', 'UD'] の順に並べ替えて渡す`、見つからない局 0(10% 以下は可)、`G-causal … PASS`、τ ごとの 4 行。
- 所要時間: CPU なので 1 地震あたり数 s〜十数 s(終わりの「検測 … s(1 地震あたり … s)」の行まで、表示が止まって見える)。
- 索引 `{IDX}` が無い(切れた後)か使えない時は、その場で作り直す(数十分かかりうる)。
- 最後の行で出力をすぐ Drive に写す(N16 の前に切れても失わないため)。
- STOP が出たら N16 に進まず、出力を貼る。24_07 は直さず回し直さない。その時は Mac の 25_05 を `--no-causal` で回す(事前登録 5.5 節、M2・M3)。
- 出力: `{LO}/data/24_07_causal_picks_shimane2018.csv`・`{LO}/models/24_07_causal_picks_shimane2018.json`・`{LO}/PDF/24_07_causal_picks_shimane2018.pdf`

### N16 — Drive へ保存と SHA-256
```python
!mkdir -p {DRV}/data/tottori_processed {DRV}/models {DRV}/PDF
!cp {LO}/{R1} {DRV}/data/tottori_processed/
!cp {LO}/data/25_03h_overlap_exclusion.json {LO}/data/25_04d_gclock2.json {LO}/data/25_04e_station_picks.csv {LO}/data/24_07_causal_picks_shimane2018.csv {DRV}/data/
!cp {LO}/models/24_07_causal_picks_shimane2018.json {DRV}/models/ ; cp {LO}/PDF/*.pdf {DRV}/PDF/
!sha256sum {LO}/{R1} {LO}/data/24_07_causal_picks_shimane2018.csv {LO}/models/24_07_causal_picks_shimane2018.json {CAT}/jma_shimane2018.csv
!python -c "import json;print('24_07 seisbench', json.load(open('{LO}/models/24_07_causal_picks_shimane2018.json'))['seisbench'])"
```
- この 4 つの SHA-256 を控える(`results/25_registration.txt` に書く)。最後の行が N1 の seisbench の版(0.12.7)と同じこと(事前登録 14 節の 7)。

### N17 — Drive に書けたかの確かめ
```python
from google.colab import drive
drive.flush_and_unmount()
drive.mount('/content/drive')
!sha256sum {DRV}/data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt {DRV}/data/24_07_causal_picks_shimane2018.csv {DRV}/models/24_07_causal_picks_shimane2018.json {CAT}/jma_shimane2018.csv
```
- 期待: N16 の 4 つの値と同じ。

### N18 — 記録を 1 つの zip にまとめる(Colab で止めた時も、ここまでに回したセルの分を必ず回す)
```python
import os, zipfile, glob
os.makedirs(DRV, exist_ok=True)       # N5 などで止めた時は、まだ無い
OUTZ = f'{DRV}/25_reports.zip'
F = [f'{CAT}/25_01_shimane2018_catalog.json', f'{CAT}/jma_shimane2018.csv', '/content/drive/MyDrive/ARGUS/PDF/25_01_shimane2018_catalog.pdf',
     f'{DRV}/data/25_02_report.json', f'{DRV}/data/25_02_plan.json', f'{DRV}/models/locator/15_01c_build_report_shimane2018_m15.json',
     f'{DRV}/data/25_03h_overlap_exclusion.json', f'{DRV}/data/25_04d_gclock2.json', f'{DRV}/data/25_04e_station_picks.csv',
     f'{DRV}/models/24_07_causal_picks_shimane2018.json'] + sorted(glob.glob(f'{DRV}/PDF/*.pdf'))
with zipfile.ZipFile(OUTZ, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in F:
        if os.path.exists(p): z.write(p, os.path.basename(p))
        else: print('無い(そこまで回していない時は正常):', os.path.basename(p))
print(OUTZ, len(zipfile.ZipFile(OUTZ).namelist()), '個')
```
- 期待: 最後の行に zip の場所と数。Mac の M6a は、この `ARGUS_shimane2018/25_reports.zip` 1 つだけを落とす。

### NR — Drive から戻す(Colab が切れた時だけ。下の表で指示された時に回す)
```python
!mkdir -p {LO}/data/tottori_processed {LO}/models/locator {LO}/PDF
!cp {DRV}/data/tottori_processed/tottori_parsed_realpick_shimane2018_m15.pt {LO}/data/tottori_processed/
!cp {DRV}/models/locator/15_01c_build_report_shimane2018_m15.json {LO}/models/locator/
!cp {DRV}/data/25_02_report.json {LO}/data/
!cp {DRV}/data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt {LO}/data/tottori_processed/ 2>/dev/null; cp {DRV}/data/25_03h_overlap_exclusion.json {LO}/data/ 2>/dev/null
!cp {DRV}/data/25_04d_gclock2.json {DRV}/data/25_04e_station_picks.csv {LO}/data/ 2>/dev/null; cp {DRV}/PDF/25_04*.pdf {LO}/PDF/ 2>/dev/null
!sha256sum {LO}/data/tottori_processed/*.pt
```
- 期待: `_r1.pt` があれば、その値が N12b の値と同じ。

### Colab が切れた時
まず N1 → N2 → N3 → N4。その後:

| 切れた所 | 次に回すもの |
|---|---|
| N5・N6・N7b の途中 | 切れたセルから |
| N7 の途中 | N8b → N7(動いている印が残っているため) |
| N8 の途中 | N8b → N8 |
| N9 〜 N11 の途中 | N9 → N10a → N10b → N11(25_03 を回し直したことと、両方の回のまとめの数を `results/25_registration.txt` に書く) |
| N11b の後・N12b の前 | N9(h5 をローカルに作り直す)→ NR → N10a → N12 から(R1 は Drive にまだ無い。NR の sha256 に `_r1.pt` が出ない) |
| N12b の後・N15 の前 | N9(h5 をローカルに作り直す。N15 に要る)→ NR → N10a → 切れたセルから |
| N15 の途中 | N9 → NR → N10a → N15(24_07 を回し直したことを `results/25_registration.txt` に書く) |
| N15 の後・N17 の前 | N15 の最後の行で Drive に写せていれば 24_07 は回し直さず、NR → N10a → N17。N17 の値は、.pt を N12b の値と、CSV を JSON の `csv_sha256` と照らす。N16 の最後の行(seisbench)は `{LO}` を `{DRV}` に替えて回す。写す前に切れた時は「N15 の途中」と同じ |
| N17 の後 | N18 だけ(N2 の変数が要るので、N1 → N2 の後に) |

---

## 3 部 Mac(本人が回す。~/SWIFT、21_06a で学習した uv の環境)

### M1 — 置く
```bash
mkdir -p ~/SWIFT/data/shimane2018_processed
```
- Drive の次の 4 つを `~/SWIFT/data/shimane2018_processed/` に持って来る(ブラウザか Drive for desktop。1 つずつ):
  `ARGUS_shimane2018/data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt`、
  `ARGUS_shimane2018/data/24_07_causal_picks_shimane2018.csv`、`ARGUS_shimane2018/models/24_07_causal_picks_shimane2018.json`、
  `ARGUS/data/catalog/jma_shimane2018.csv`(N15 が STOP した時は 24_07 の 2 つは無い)。ブラウザで落とすと `~/Downloads` に入るので、次で移す
  (24_07 の 2 つが無い時は、その名前を外して回す):
```bash
cd ~/Downloads && mv tottori_parsed_realpick_shimane2018_m15_r1.pt 24_07_causal_picks_shimane2018.csv 24_07_causal_picks_shimane2018.json jma_shimane2018.csv ~/SWIFT/data/shimane2018_processed/
cd ~/SWIFT && ls -la data/shimane2018_processed
cd ~/SWIFT && shasum -a 256 data/shimane2018_processed/* src/25_05_*.py src/25_06f_*.py src/25_06g_*.py src/25_08_*.py src/25_09_*.py models/21_06_ranker.pkl models/21_06a_train.json data/21_06a_train_rows.npz models/22_gate.pkl
find models data PDF -maxdepth 1 \( -name '25_05_*' -o -name '25_06f_*' -o -name '25_06g_*' -o -name '25_08_*' -o -name '25_09_*' \) -print; echo "find done"
```
- 期待: `ls` は 4 つだけ(`(1)` の付いた名前が無い。あれば名前を直す)。データの 4 つは N16・N17 の値、スクリプトは 9 節の値、凍結したモデルは 9 節の
  「前提として既に凍結したもの」の値。`find done` の前に何も出ない(残っていると本番が _rerun になる)。

### M1b — 環境の版
```bash
cd ~/SWIFT && uv run python -c "import sklearn, numpy, sys; print(sklearn.__version__, numpy.__version__, sys.version)"
```
- 期待: `1.8.0 2.4.3 3.12.12 …`。違えば先に進まない。

### M2 — 25_05 の dev(試験を開かない)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/25_05_shimane2018_similarity_confirmation.py --dev; echo "exit code: $?"
```
- 次の 2 つの時だけ、`--dev` の後に `--no-causal` を付ける(M3 も同じ。事前登録 5.5 節):
  (1) N15 の 24_07 が STOP を表示した時。(2) 25_05 が `24_07 の …` の照合の STOP を出し、Drive から落とし直して M1 の SHA-256 を
  照らしても直らない時。どちらも、その STOP の行を貼って `results/25_registration.txt` に書く。
- 確かめること: `G-untouched … PASS`、`G-split PASS`、`H5 の材料: … そろっている`、`G-causal … PASS`、`G-phys … PASS`、
  `G-causal(H5 の経路 …): 0  PASS`、H4・H5 の行、`DEV (no verdict)`。
- G-phys が FAIL なら本番は開かない(事前登録 5.7 節の文で報告)。

### M2b — 25_06g の dev
```bash
cd ~/SWIFT && caffeinate -i uv run python src/25_06g_shimane2018_gate_test.py --dev; echo "exit code: $?"
```
- 確かめること: `写した部分の SHA-256 … G-leak PASS`、`凍結した G … 同じ`、`照合の準備は全て通った`、`G-same … PASS`、`INCONCLUSIVE(dev …)`。

### M2c — 25_08 の dev(配管の確かめ)
```bash
cd ~/SWIFT && uv run python src/25_08_shimane2018_intensity_descriptive.py --dev; echo "exit code: $?"
```
- 確かめること: `出力: models/25_08_intensity_dev.json・…` で終わる。

### M2d — 25_09 の dev(配管の確かめ)
```bash
cd ~/SWIFT && uv run python src/25_09_shimane2018_flag_descriptive.py --dev; echo "exit code: $?"
```
- 確かめること: `印の数: …`(dev の 20 地震の印)と `出力: models/25_09_flag_descriptive_dev.json・…` で終わる。

### M3 — 25_05 の本番(1 回だけ)
- 先に、N12b の 2 つの値が `results/25_registration.txt` に書いてあることを確かめる(事前登録 6 節)。
```bash
cd ~/SWIFT && caffeinate -i uv run python src/25_05_shimane2018_similarity_confirmation.py; echo "exit code: $?"
```
- 出力: `models/25_05_judgment.json`・`models/25_05_judgment_preH5.json`・`models/25_05_opened.json`・`data/25_05_per_event.csv`・`PDF/25_05_F1〜F4.pdf`。出力を全部貼る。
- 途切れた時(Mac が眠った・電源・Ctrl-C)だけ、同じコマンドを 1 回だけやり直してよい(事前登録 6 節)。その時の結果は `_rerun_<UTC>` の
  名前になる。以下の M4〜M7 では、その `_rerun_<UTC>` を `--ref-suffix` に渡す(下の各ステップに書いた)。
- `判定(事前宣言、H1): INCONCLUSIVE` の時は、ここで終わり(M4〜M5d と M7 は回さない。M6a と M6b だけ行う)。

### M4 — 25_06f の dev
```bash
cd ~/SWIFT && caffeinate -i uv run python src/25_06f_shimane2018_learned_test.py --dev; echo "exit code: $?"
```
- 確かめること: `G-feat PASS  G-model PASS`・`G-same … PASS`・`DEV (no verdict)`。**この 3 つを確かめてから** M5 へ。どれかが違えば止めて貼る。

### M5 — 25_06f の本番(1 回だけ)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/25_06f_shimane2018_learned_test.py; echo "exit code: $?"
```
- 25_05 の正式な結果が `_rerun_<UTC>` の時だけ、末尾に `--ref-suffix _rerun_<UTC>` を付ける(M5b・M5c・M5d も同じ)。

### M5b — 25_06g の本番(1 回だけ)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/25_06g_shimane2018_gate_test.py; echo "exit code: $?"
```

### M5c — 25_08(H6 の記述)
```bash
cd ~/SWIFT && uv run python src/25_08_shimane2018_intensity_descriptive.py; echo "exit code: $?"
```

### M5d — 25_09(震源決定の印ごとの記述)
```bash
cd ~/SWIFT && uv run python src/25_09_shimane2018_flag_descriptive.py; echo "exit code: $?"
```

### M6a — 記録を写す
- Drive の `ARGUS_shimane2018/25_reports.zip`(N18 で作ったもの)を 1 つだけブラウザで落とす。Safari が自動で展開して `~/Downloads/25_reports` の
  フォルダになった時は、下の 2 行目の代わりに `cp ~/Downloads/25_reports/* ~/ARGUS_prereg_21_04/25/results/` を回す。
  名前が `25_reports (1).zip` になった時は、2 行目を `cd ~/Downloads && unzip -o "25_reports (1).zip" -d ~/ARGUS_prereg_21_04/25/results/` にする(" " で囲む)。
```bash
mkdir -p ~/ARGUS_prereg_21_04/25/results
cd ~/Downloads && unzip -o 25_reports.zip -d ~/ARGUS_prereg_21_04/25/results/
cd ~/SWIFT && find models data PDF -maxdepth 1 -name '25_0*_rerun_*' -print; echo "rerun check done"
cd ~/SWIFT && find data/shimane2018_processed models data PDF -maxdepth 1 -type f \( -name '24_07_causal_picks_shimane2018.csv' -o -name '25_05_*' -o -name '25_06f_*' -o -name '25_06g_*' -o -name '25_08_*' -o -name '25_09_*' \) -exec cp {} ~/ARGUS_prereg_21_04/25/results/ \;
ls ~/ARGUS_prereg_21_04/25/results
```
- `rerun check done` の前に何か出たら、M3 をやり直した時。その名前の `_rerun_<UTC>` の部分を M7 の `SFX` に書く。
- 2 つ目の `find … -exec cp` は、ある物だけを写す(無い物があってもエラーにならない)。
- `results` に `25_registration.txt` があること(0-F で作ったもの)。

### M7 — すその印(事前登録 7 節の式。記述)。M6b の commit の前に回す。25_05 が INCONCLUSIVE の時は回さない
```bash
cd ~/SWIFT && SFX="" && uv run python - "$SFX" <<'EOF' | tee ~/ARGUS_prereg_21_04/25/results/25_M7_tail.txt
import json, csv, sys
SFX = sys.argv[1]
J = json.load(open(f'models/25_05_judgment{SFX}.json')); JF = json.load(open('models/25_06f_judgment.json'))
R = list(csv.DictReader(open(f'data/25_05_per_event{SFX}.csv'))); RF = list(csv.DictReader(open('data/25_06f_per_event.csv')))
N, NF = J['n_evaluated'], JF['n_evaluated']
print('25_05 suffix', repr(SFX), '| N', N, 'rows', len(R), '| NF', NF, 'rows', len(RF))
H5OK = bool(J.get('causal', {}).get('evaluated', False))
def tail(rows, col, thr, n):
    v = [x[col] for x in rows]; k = sum(1 for s in v if s != '' and float(s) > thr); e = sum(1 for s in v if s == '')
    print(f'  {col:>22s}  > {thr:4.1f} km: {k} / {n} = {k / n:.3f}   空の欄 {e}')
for t in ['0.5', '1', '2', '3']:
    B = J['per_tau'][t]['C3']['best']; BC = J['causal']['per_tau'][t]['C3']['best'] if H5OK else None
    print(f'tau {t} s  BEST = {B}  (causal BEST = {BC})')
    cols = [f'{B}_err_t{t}', f'C3_err_t{t}', f'C4_err_t{t}'] + ([f'{BC}_causal_err_t{t}', f'C3_causal_err_t{t}'] if H5OK else [])
    for col in cols: tail(R, col, 10.0, N)
    tail(RF, f'L4_t{t}', 10.0, NF)
B2 = J['per_tau']['2']['C3']['best']; print(f'30 km, tau 2 s  BEST = {B2}')
for col in [f'{B2}_err_t2', 'M6r_err_t2', 'C4_err_t2']: tail(R, col, 30.0, N)
tail(RF, 'L4_t2', 30.0, NF)
EOF
```
- M3 をやり直した時は、`SFX=""` を `SFX="_rerun_<UTC>"`(M6a で出た名前の部分)に替える(25_06f の出力の名前は替えない)。
- H5 が NOT-EVALUATED の時は、τ までの検測の列は出ない(`causal BEST = None`)。

### M6b — commit・push(結果の 1 回だけ)
```bash
cd ~/ARGUS_prereg_21_04 && git add 25/results && git status
```
- 期待: `25/results/` のファイルだけ(`25_registration.txt` を含む)。`25/` の記録とスクリプトは書き換えないので、出ない。
```bash
cd ~/ARGUS_prereg_21_04 && git commit -m "25: results (Western Shimane 2018), with registration record" && git push && git log -1 --oneline
```
