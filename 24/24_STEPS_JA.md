# 24 長野県北部 2014 — 回す手順(Mac の準備 + Colab のセル N1〜N17 + Mac の M1〜M7)

ノート: `24_nagano2014_colab.ipynb`(この束に入っている。セルの番号はノートの見出しと同じ)。
形は大阪(21_20)の手順と同じで、名前と、R1(N12)・H5 の材料(N15)を足した所だけが違う。

- **ノートは「すべてのセルを実行」を使わない。** 上から 1 つずつ、この手順の順に回す(N5 の最初で 0 部が済んだかを聞いて止まる)。
- スクリプトの表示の「セル n」は、このノートの「Nn」のこと(例: 「セル 8b」= N8b、「セル 3」= N3)。「セル N10」「セル 10」は N10a・N10b のこと。
- Colab のどこかで止めた時(STOP・止める判定)も、そこまでの記録は Drive に写し(N12b・N14c など、そのセルの「写す」行)、Mac の M6a で
  results に入れて commit する(止めた記録も事前登録の結果として残す)。

---

## 0 部 Mac: 置く・確かめる・push する・外部の時刻の記録を取る(N5 の前に必ず)

### 0-A 束を置いて、SHA-256 を確かめる
- Safari で落とすと zip が自動で展開されることがある。その時は `~/Downloads/24_bundle` のフォルダの中身を下の `24/` に写す。
```bash
mkdir -p ~/ARGUS_prereg_21_04/24
cd ~/Downloads && unzip -o 24_bundle.zip -d ~/ARGUS_prereg_21_04/24/
cd ~/ARGUS_prereg_21_04/24 && ls && shasum -a 256 *.py
```
- 期待: `ls` は 15 個(.py 11 本・.md 3 つ・.ipynb 1 つ)だけ。`__pycache__` が無い。
- 期待: 11 行の値が、事前登録の記録 `24_preregistration_nagano2014.md` の 9 節の表と全桁で同じ。

### 0-B 冒頭のチェックを確かめて埋める
- 記録の 1 節の表の値を、各系列の結果の JSON(`~/ARGUS_prereg_21_04/results_21_04/`・`results_21_20/` など)と照らす(事前登録 14 節の 6)。
```bash
ls -d ~/SWIFT/data/nagano2014_processed; ls ~/SWIFT/models | grep 24_0; echo "check done"
grep -rnE "@@[A-Z0-9_]+@@" ~/ARGUS_prereg_21_04/24; echo "grep done"
```
- 期待: 1 行目は `No such file or directory` の後に `check done` だけ(長野の出力がまだ何も無い)。
- 期待: `grep done` の前に何も出ない(凍結するファイルに未記入の印が残っていない)。
- ブラウザで Drive に `ARGUS_nagano2014` のフォルダが無いことを確かめる。
- 記録 `24_preregistration_nagano2014.md` の冒頭の 2 つの `[ ]` を、確かめてから `[x]` にする(テキストエディタで)。

### 0-C Colab で使う 7 本を Drive に、Mac で使う 4 本を ~/SWIFT/src に置く
- Drive の `マイドライブ/ARGUS/src/` に置く(ブラウザか Drive for desktop): `24_01_…`・`24_02_…`・`24_03_…`・`24_03h_…`・`24_04d_…`・`24_04e_…`・`24_07_causal_picks.py`。
  24_07 は v2 が既に置いてある。**先に v2 をゴミ箱に移してから** v3 を置く(同じ名前で上げると `24_07_causal_picks (1).py` ができる)。
```bash
cp ~/ARGUS_prereg_21_04/24/24_05_nagano2014_similarity_confirmation.py ~/ARGUS_prereg_21_04/24/24_06f_nagano2014_learned_test.py \
   ~/ARGUS_prereg_21_04/24/24_06g_nagano2014_gate_test.py ~/ARGUS_prereg_21_04/24/24_08_nagano2014_intensity_descriptive.py ~/SWIFT/src/
cd ~/SWIFT && shasum -a 256 src/24_05_*.py src/24_06f_*.py src/24_06g_*.py src/24_08_*.py
```
- 期待: 4 行が 9 節の値と同じ。

### 0-D 1 回目の commit・push
```bash
cd ~/ARGUS_prereg_21_04
git add 24
git status   # .DS_Store が出たら git restore --staged 24/.DS_Store で外す
git commit -m "24: preregistration of the one-shot test on Northern Nagano 2014 (fourth sequence): record, 11 scripts, steps, notebook, diff log"
git push
git log -1 --format=%H
```
- 表示された hash を控える(0-F で記録に書く)。

### 0-E 外部の時刻の記録(Zenodo の新しい版)
- Zenodo の記録(最新は v2 の 10.5281/zenodo.24190129)を開き「New version」。前の版のファイルは残したまま、`24/` の 15 個を足す。
- 題に「v3: preregistration 24 (Northern Nagano 2014)」、説明に 0-D の commit の hash を書く。
- 非公開期間(embargo)の終わりの日は、前の版と同じにする。公開する。
- 公開後のページに出る**新しい版の DOI**を控える(23905464 や 24190129 ではない)。

### 0-F 2 回目の commit(hash・DOI・確定した日を書く)
- 記録の冒頭の「事前登録として確定した日」「commit の hash」「置いた先・日時・DOI」を書いて:
```bash
cd ~/ARGUS_prereg_21_04 && git add 24/24_preregistration_nagano2014.md && git commit -m "24: record commit hash and Zenodo version" && git push && git log -1 --oneline
```

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

### N2 — 場所の変数と、スクリプトの SHA-256
```python
import hashlib, os
SRC = '/content/drive/MyDrive/ARGUS/src'
CAT = '/content/drive/MyDrive/ARGUS/data/catalog'
DRV = '/content/drive/MyDrive/ARGUS_nagano2014'
LO  = '/content/ARGUS_nagano2014'
R1  = 'data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt'
REF_H5 = '/content/drive/MyDrive/2026WTottori/data/waves/tottori_all_100Hz.h5'
REF_CACHE_2026 = '/content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt'
EXP = {  # 事前登録の記録の 9 節と同じ値
    '24_01_nagano2014_jma_catalog.py': 'a4fb5d9a41c694663d65cf5a6f124d97f024360f1d9a40b43c0bf1fc1a6812a6',
    '24_02_nagano2014_hinet_to_h5.py': '0f2283af1e3a0fde831e96bd598284a04ba1ff4a64634fefb1dba65d39f8f69f',
    '24_03_nagano2014_realpick_cache_colab.py': '86b3cb1f810752eae9e1bee43e596621773d601d478cf270e0ca0db50101c60a',
    '24_03h_nagano2014_overlap_exclusion.py': 'e2700654a13f0514f133f01f8255d8b546107716ec43990cc648a7392e42dd0d',
    '24_04d_nagano2014_gclock2_picks.py': '42f783bba5ca666847b4582edf3d4a554cecce288c1b2aa112f682bdbaa95f93',
    '24_04e_nagano2014_station_pick_diagnose.py': 'befca1b3326d18659d249c7ee9e5b1b1f364828c8a4a85c3cafc1bba16f67931',
    '24_07_causal_picks.py': 'b9b2fd5c8855c52f2e3a528e695374af752db3b0de6f789942e6da8824c2d14b',
}
for n, h in EXP.items():
    got = hashlib.sha256(open(f'{SRC}/{n}', 'rb').read()).hexdigest()
    print('OK  ' if got == h else 'NG  ', n, got)
print('名前に (1) などが付いた写し:', [f for f in os.listdir(SRC) if f.startswith('24_') and '(' in f])
```
- 期待: 7 行とも `OK`。最後の行が `[]`。`NG` が 1 つでもあれば止める。

### N3 — win32tools(catwin32・win2sac_32)
- このノートの N3 のセルを回す(中身は大阪のノートのセル 3 と同じ。`マイドライブ/KRITES/bin/` に作ったものを写すだけ)。
- 期待: `which catwin32 win2sac_32` に 2 つのパスが出て、`file` に `ELF` と出る。`Mach-O` と出たら Mac で作ったものなので、`KRITES/bin` の
  2 つを消して、もう一度このセルを回す(大阪の手順のセル 3 と同じ)。

### N4 — Hi-net の資格情報(ノートに書き残さない)
```python
import os, getpass
os.environ['HINET_USER'] = getpass.getpass('Hi-net user: ')
os.environ['HINET_PASS'] = getpass.getpass('Hi-net password: ')
```

### N5 — 24_01: 気象庁の震源(h2014)。**0 部が全て済んでから**
```python
assert input('0 部(1 回目の push・Zenodo の新しい版・2 回目の push)は全て済んだか? 済んだら yes: ').strip() == 'yes', '0 部を先に'
!python {SRC}/24_01_nagano2014_jma_catalog.py; echo "exit code: $?"
```
- 期待: `震源ファイル … SHA-256 bcb1d2d91a59…`(24_00 と同じ)、`本震: 2014-11-22 22:08:17.900000 JST …(… の中か: True)`、
  `数:` の `all` 2052・`mj_ge_1p5` 502・`test_candidates_1p5_to_2p0_after_72h` 81(どれも 24_00 と同じ)、`試験の候補 81 ≥ 30: 次へ進める`。
- 違う値が出たら止めて出力を貼る。
- h2014 の確定の段階(事前登録 14 節の 4)を、気象庁の震源ファイルのページで確かめて記録の追記に書く。
- 出力: `{CAT}/jma_nagano2014.csv`・`{CAT}/24_01_nagano2014_catalog.json`・`/content/drive/MyDrive/ARGUS/PDF/24_01_nagano2014_catalog.pdf`

### N6 — 24_02: 取る計画だけ
```python
!python {SRC}/24_02_nagano2014_hinet_to_h5.py --ref-h5 "{REF_H5}" --dry-run; echo "exit code: $?"
```
- 確かめること: `参照の z-score の確認 … PASS`、候補局 60、区切りの数と分の合計、置き場所の見込み。

### N7 — 煙試験(本震の区間に掛かる区切りを先に 3 つ)
```python
!python {SRC}/24_02_nagano2014_hinet_to_h5.py --ref-h5 "{REF_H5}" --max-blocks 3; echo "exit code: $?"
```

### N7b — 煙試験の分だけで組み立ててゲートを見る
```python
!python {SRC}/24_02_nagano2014_hinet_to_h5.py --ref-h5 "{REF_H5}" --assemble --partial; echo "exit code: $?"
```
- G-ref・G-dup が PASS。`PDF/24_02_mainshock_partial.pdf` で本震の P が予想の P の印にそろっているか。G-clock の FAIL は記録だけ。
- 煙試験の G-cover は区切りが 3 つだけなので低くてよい(本番の判定は N9)。G-ref・G-dup の FAIL は止めて貼る。

### N8 — 全ての区切りを取る(止まっても同じセルで続きから)
```python
!python {SRC}/24_02_nagano2014_hinet_to_h5.py --ref-h5 "{REF_H5}"; echo "exit code: $?"
```
- 最後の行が `終わり: 残りの区切り 0/N`(全部済んだ後に回すと `取る区切りが無い(全部済み)`)になるまで回し直す。取れた割合が 0.98 以上で、何度回しても取れない区切りだけが残った時だけ、N9 に `--allow-missing`。

### N8b — Colab が切れた直後だけ
```python
!python {SRC}/24_02_nagano2014_hinet_to_h5.py --ref-h5 "{REF_H5}" --restore-selection --break-lock; echo "exit code: $?"
```

### N9 — 組み立てとゲート(Colab のローカルで)
```python
!df -h /content
!mkdir -p {LO}/data
!cp -r {DRV}/data/blocks {LO}/data/ && cp {DRV}/data/24_02_plan.json {LO}/data/
# N8 で取れない区切りだけが残った時(取れた割合 0.98 以上)だけ、下の行の --out {LO} の後に --allow-missing を付ける
!python {SRC}/24_02_nagano2014_hinet_to_h5.py --ref-h5 "{REF_H5}" --assemble --out {LO}; echo "exit code: $?"
!mkdir -p {DRV}/data/catalog {DRV}/PDF && cp {LO}/data/24_02_report.json {DRV}/data/ && cp {LO}/PDF/24_02_*.pdf {DRV}/PDF/
!cp {LO}/data/catalog/stations_nagano2014.csv* {DRV}/data/catalog/
!ls -la {LO}/data/waves {LO}/data/catalog
```
- `STOP(G-clock だけ)` → 進む(`nagano2014_100Hz_FAILED.h5` と `stations_nagano2014.csv.part` を N10a が自分で選ぶ)。それ以外の STOP は止めて出力を貼る。
- G-cover が 0.80〜0.95 の「注意」は進む(止めるのは 0.80 未満だけ。事前登録 5.2 節)。
- 報告の `version` が `v1 (=21_20b v1 + window scale)`。`df -h` の空きが、N6 の見込み(区切り + h5)より大きいこと。

---

## 2 部 Colab: キャッシュ・R1・時刻の確かめ・H5 の材料(N10〜N17)

### N10a — 変数だけ(h5・観測点・箱)。Colab が切れた後もこのセルだけを回し直す
```python
import json, os
S = json.load(open(f'{CAT}/24_01_nagano2014_catalog.json')); BOX = ' '.join(str(x) for x in S['box']); print('box', BOX)
H5 = f'{LO}/data/waves/nagano2014_100Hz.h5'
STA = f'{LO}/data/catalog/stations_nagano2014.csv'
if not os.path.exists(H5):            # G-clock だけの FAIL の時(事前登録 5.2 節)
    H5, STA = f'{LO}/data/waves/nagano2014_100Hz_FAILED.h5', STA + '.part'
IDX = f'{LO}/data/tottori_processed/h5_index_{os.path.basename(H5)[:-3]}.npz'   # 24_03 が作る窓の索引(N15 で使う)
print(H5, os.path.exists(H5)); print(STA, os.path.exists(STA))
```

### N10b — 24_03 の煙試験(10 地震)
```python
!python {SRC}/24_03_nagano2014_realpick_cache_colab.py --h5 {H5} --jma {CAT}/jma_nagano2014.csv --stations {STA} --min-mag 1.5 --box {BOX} --base {LO} --tag _nagano2014_smoke --max-events 10; echo "exit code: $?"
```

### N11 — 24_03 の本番(1 回だけ)
```python
!python {SRC}/24_03_nagano2014_realpick_cache_colab.py --h5 {H5} --jma {CAT}/jma_nagano2014.csv --stations {STA} --min-mag 1.5 --box {BOX} --base {LO} --tag _nagano2014_m15; echo "exit code: $?"
!python -c "import json;print('24_03 script_sha256', json.load(open('{LO}/models/locator/15_01c_build_report_nagano2014_m15.json'))['script_sha256'])"
```
- 出力: `{LO}/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15.pt`・`{LO}/models/locator/15_01c_build_report_nagano2014_m15.json`
- 最後の行の値が 9 節の 24_03 の値と同じこと。

### N11b — キャッシュをすぐ Drive に写す
```python
!mkdir -p {DRV}/data/tottori_processed {DRV}/models/locator
!cp {LO}/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15.pt {DRV}/data/tottori_processed/
!cp {LO}/models/locator/15_01c_build_report_nagano2014_m15.json {DRV}/models/locator/
```

### N12 — 24_03h: R1(重なった地震を除く)
```python
!python {SRC}/24_03h_nagano2014_overlap_exclusion.py --cache {LO}/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15.pt --catalog {CAT}/jma_nagano2014.csv --report {LO}/data/24_02_report.json --out {LO}; echo "exit code: $?"
```
- 期待: `G-match PASS`、`除いた後: … 試験の候補 N(前 M)` で N ≥ 30、`出力: …_nagano2014_m15_r1.pt  … SHA-256 …`。
- `STOP(R2)`・`STOP(R3)` → 止める(R3 は INCONCLUSIVE として報告。事前登録 5.4 節)。
- 本震の不一致・G-match などその他の STOP も止めて出力を貼る。

### N12b — R1 の出力をすぐ Drive に写す
```python
!mkdir -p {DRV}/data/tottori_processed && cp {LO}/{R1} {DRV}/data/tottori_processed/ && cp {LO}/data/24_03h_overlap_exclusion.json {DRV}/data/
!sha256sum {LO}/{R1} {DRV}/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt
```
- 期待: 2 行の値が同じ。この値と 24_03h の JSON の `input_cache_sha256` を、24_05 を開く前に記録の追記に書く(事前登録 6 節)。
- N12 が STOP(R2・R3 など)の時は、このセルを回さず、`!cp {LO}/data/24_03h_overlap_exclusion.json {DRV}/data/` だけを回して記録を残す。

### N13 — 24_04d: G-clock2
```python
!python {SRC}/24_04d_nagano2014_gclock2_picks.py --base {LO} --cache {R1} --ref-cache {REF_CACHE_2026}; echo "exit code: $?"
```
- 最後の行が `STOP(G-clock2)`(条件の FAIL)の時は、ここでは止めずに N14・N14b に進む(扱いは事前登録 5.3 節で決まっている)。
- それ以外の STOP(検測 100 未満・日/局/時間が 0・報告が無い)は JSON が書かれないので、止めて出力を貼る。

### N14 — 24_04e(必ず回す)
```python
!python {SRC}/24_04e_nagano2014_station_pick_diagnose.py --base {LO} --cache {R1} --ref-cache {REF_CACHE_2026}; echo "exit code: $?"
```

### N14b — 案 C の判定に要る値を表示する(読むだけ)
```python
import json, csv
J = json.load(open(f'{LO}/data/24_04d_gclock2.json'))
for k in ['pass_all', 'pass_day', 'pass_station', 'pass_hour', 'pass_events', 'pass_measured_frac', 'gclock2_pass']: print(k, J[k])
for x in J['gclock_events']:
    print('  (e)', x['origin_jst'], 'Mj', x['mj'], 'found_dt_s', round(x['found_dt_s'], 3), 'n_picks', x['n_picks'], 'PASS' if x['pass_'] else 'FAIL')
rows = list(csv.DictReader(open(f'{LO}/data/24_04e_station_picks.csv')))
near = [r for r in rows if float(r['epi_from_mainshock_km']) <= 80.0 and int(r['n']) >= 20]
bad_near = [r for r in near if abs(float(r['dev_s'])) > 1.0]
bad_far = [r for r in rows if float(r['epi_from_mainshock_km']) > 80.0 and int(r['n']) >= 20 and abs(float(r['dev_s'])) > 1.0]
print('(c-near) 80 km 以内・n ≥ 20 の局', len(near), '  |dev_s| > 1.0 s の局', len(bad_near))
for r in bad_near: print('   ', r['station'], r['epi_from_mainshock_km'], 'km  n', r['n'], ' dev_s', r['dev_s'])
print('(c-far) 80 km より遠い・n ≥ 20 で |dev_s| > 1.0 s の局', len(bad_far))
for r in bad_far: print('   ', r['station'], r['epi_from_mainshock_km'], 'km  n', r['n'], ' dev_s', r['dev_s'])
```
- 読み方(事前登録 5.3 節): `pass_all`・`pass_day`・`pass_hour`・`pass_events`・`pass_measured_frac` のどれかが False → 止める。
  (c-near) の外れが 1 局でもある、または 80 km 以内・n ≥ 20 の局が 0 → 止める。`pass_station` だけが False → 進み、決まった印を付ける。
  `gclock2_pass` が True → 進む。
- (c-far) の時に付ける印の英文・日本文は、事前登録 5.3 節の 4 にある。止める時も N14c は回す(記録を残す)。

### N14c — G-clock2 の出力をすぐ Drive に写す
```python
!mkdir -p {DRV}/data {DRV}/PDF && cp {LO}/data/24_04d_gclock2.json {LO}/data/24_04e_station_picks.csv {DRV}/data/ && cp {LO}/PDF/24_04*.pdf {DRV}/PDF/
```

### N15 — 24_07: H5 の材料(τ までの波形だけの検測。全ての地震。1 回だけ)
```python
!python {SRC}/24_07_causal_picks.py --h5 {H5} --cache {LO}/{R1} --stations {STA} --index {IDX} --base {LO} --tag _nagano2014 --all-events --label "Northern Nagano 2014"; echo "exit code: $?"
!mkdir -p {DRV}/data {DRV}/models {DRV}/PDF && cp {LO}/data/24_07_causal_picks_nagano2014.csv {DRV}/data/ && cp {LO}/models/24_07_causal_picks_nagano2014.json {DRV}/models/ && cp {LO}/PDF/24_07_*.pdf {DRV}/PDF/
```
- 期待: `selftest: 元の値への戻し(v3)・…に全て合格`、`h5 の値: win_mean・win_std から元の値に戻して使う(v3)`、
  `成分の並び ENZ → … ['EW', 'NS', 'UD'] の順に並べ替えて渡す`、見つからない局 0(10% 以下は可)、`G-causal … PASS`、τ ごとの 4 行。
- 所要時間: 鳥取県西部 2026 の dev は T4(GPU)で 1 地震あたり 3.2 s(24_07 v2 の JSON の `seconds.per_event`)。このノートは CPU なので
  それより長い(CPU の時間は測っていない)。終わりの「検測 … s(1 地震あたり … s)」の行まで、表示が止まって見える。
- 索引 `{IDX}` が無い(切れた後)か使えない(形が違う)時は、その場で作り直す(数十分かかりうる)。
- 最後の行で出力をすぐ Drive に写す(N16 の前に切れても失わないため)。
- STOP が出たら N16 に進まず、出力を貼る。24_07 は直さず回し直さない。その時は Mac の 24_05 を `--no-causal` で回す(事前登録 5.5 節、M2・M3)。
- 出力: `{LO}/data/24_07_causal_picks_nagano2014.csv`・`{LO}/models/24_07_causal_picks_nagano2014.json`・`{LO}/PDF/24_07_causal_picks_nagano2014.pdf`

### N16 — Drive へ保存と SHA-256
```python
!mkdir -p {DRV}/data/tottori_processed {DRV}/models {DRV}/PDF
!cp {LO}/{R1} {DRV}/data/tottori_processed/
!cp {LO}/data/24_03h_overlap_exclusion.json {LO}/data/24_04d_gclock2.json {LO}/data/24_04e_station_picks.csv {LO}/data/24_07_causal_picks_nagano2014.csv {DRV}/data/
!cp {LO}/models/24_07_causal_picks_nagano2014.json {DRV}/models/ ; cp {LO}/PDF/*.pdf {DRV}/PDF/
!sha256sum {LO}/{R1} {LO}/data/24_07_causal_picks_nagano2014.csv {LO}/models/24_07_causal_picks_nagano2014.json
!python -c "import json;print('24_07 seisbench', json.load(open('{LO}/models/24_07_causal_picks_nagano2014.json'))['seisbench'])"
```
- この 3 つの SHA-256 を控える。最後の行が N1 の seisbench の版(0.12.7)と同じこと(事前登録 14 節の 7)。

### N17 — Drive に書けたかの確かめ
```python
from google.colab import drive
drive.flush_and_unmount()
drive.mount('/content/drive')
!sha256sum {DRV}/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt {DRV}/data/24_07_causal_picks_nagano2014.csv {DRV}/models/24_07_causal_picks_nagano2014.json
```
- 期待: N16 の 3 つの値と同じ。

### NR — Drive から戻す(Colab が切れた時だけ。下の表で指示された時に回す)
```python
!mkdir -p {LO}/data/tottori_processed {LO}/models/locator {LO}/PDF
!cp {DRV}/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15.pt {LO}/data/tottori_processed/
!cp {DRV}/models/locator/15_01c_build_report_nagano2014_m15.json {LO}/models/locator/
!cp {DRV}/data/24_02_report.json {LO}/data/
!cp {DRV}/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt {LO}/data/tottori_processed/ 2>/dev/null; cp {DRV}/data/24_03h_overlap_exclusion.json {LO}/data/ 2>/dev/null
!cp {DRV}/data/24_04d_gclock2.json {DRV}/data/24_04e_station_picks.csv {LO}/data/ 2>/dev/null; cp {DRV}/PDF/24_04*.pdf {LO}/PDF/ 2>/dev/null
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
| N9 〜 N11 の途中 | N9 → N10a → N10b → N11(24_03 を回し直したことと、両方の回のまとめの数を記録の追記に書く) |
| N11b の後・N12b の前 | N9(h5 をローカルに作り直す)→ NR → N10a → N12 から(R1 は Drive にまだ無い。NR の sha256 に `_r1.pt` が出ない) |
| N12b の後・N15 の前 | N9(h5 をローカルに作り直す。N15 に要る)→ NR → N10a → 切れたセルから |
| N15 の途中 | N9 → NR → N10a → N15(24_07 を回し直したことを記録の追記に書く) |
| N15 の後・N17 の前 | N15 の最後の行で Drive に写せていれば 24_07 は回し直さず、NR → N10a → N17。N17 の値は、.pt を N12b の値と、CSV を JSON の `csv_sha256` と照らす。N16 の最後の行(seisbench)は `{LO}` を `{DRV}` に替えて回す。写す前に切れた時は「N15 の途中」と同じ |

---

## 3 部 Mac(本人が回す。~/SWIFT、21_06a で学習した uv の環境)

### M1 — 置く
```bash
mkdir -p ~/SWIFT/data/nagano2014_processed
```
- Drive の次の 3 つを `~/SWIFT/data/nagano2014_processed/` に持って来る(ブラウザか Drive for desktop):
  `ARGUS_nagano2014/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt`、
  `ARGUS_nagano2014/data/24_07_causal_picks_nagano2014.csv`、`ARGUS_nagano2014/models/24_07_causal_picks_nagano2014.json`
  (N15 が STOP した時は .pt だけ)
```bash
cd ~/SWIFT && ls -la data/nagano2014_processed
cd ~/SWIFT && shasum -a 256 data/nagano2014_processed/* src/24_05_*.py src/24_06f_*.py src/24_06g_*.py src/24_08_*.py models/21_06_ranker.pkl models/21_06a_train.json data/21_06a_train_rows.npz models/22_gate.pkl
find models data PDF -maxdepth 1 \( -name '24_05_*' -o -name '24_06f_*' -o -name '24_06g_*' -o -name '24_08_*' \) -print; echo "find done"
```
- 期待: `ls` は 3 つだけ(`(1)` の付いた名前が無い)。データの 3 つは N16・N17 の値、スクリプトは 9 節の値、凍結したモデルは 9 節の
  「前提として既に凍結したもの」の値。`find done` の前に何も出ない(残っていると本番が _rerun になる)。

### M1b — 環境の版
```bash
cd ~/SWIFT && uv run python -c "import sklearn, numpy, sys; print(sklearn.__version__, numpy.__version__, sys.version)"
```
- 期待: `1.8.0 2.4.3 3.12.12 …`。違えば先に進まない。

### M2 — 24_05 の dev(試験を開かない)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/24_05_nagano2014_similarity_confirmation.py --dev; echo "exit code: $?"
```
- 次の 2 つの時だけ、`--dev` の後に `--no-causal` を付ける(M3 も同じ。事前登録 5.5 節):
  (1) N15 の 24_07 が STOP を表示した時。(2) 24_05 が `24_07 の …` の照合の STOP を出し、Drive から 3 つを落とし直して M1 の SHA-256 を
  照らしても直らない時。どちらも、その STOP の行を貼って記録の追記に書く。`--no-causal` の時は「H5 の材料」と「G-causal(H5 の経路 …)」
  の行は出ない。
- 確かめること: `G-untouched … PASS`、`G-split PASS`、`H5 の材料: … そろっている`、`G-causal … PASS`、`G-phys … PASS`、
  `G-causal(H5 の経路 …): 0  PASS`、H4・H5 の行、`DEV (no verdict)`。
- G-phys が FAIL なら本番は開かない(事前登録 5.7 節の文で報告)。

### M2b — 24_06g の dev
```bash
cd ~/SWIFT && caffeinate -i uv run python src/24_06g_nagano2014_gate_test.py --dev; echo "exit code: $?"
```
- 確かめること: `写した部分の SHA-256 … G-leak PASS`、`凍結した G … 同じ`、`照合の準備は全て通った`、`G-same … PASS`、`INCONCLUSIVE(dev …)`。

### M2c — 24_08 の dev(配管の確かめ)
```bash
cd ~/SWIFT && uv run python src/24_08_nagano2014_intensity_descriptive.py --dev; echo "exit code: $?"
```
- 確かめること: `出力: models/24_08_intensity_dev.json・…` で終わる。

### M3 — 24_05 の本番(1 回だけ)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/24_05_nagano2014_similarity_confirmation.py; echo "exit code: $?"
```
- 出力: `models/24_05_judgment.json`・`models/24_05_judgment_preH5.json`・`models/24_05_opened.json`・`data/24_05_per_event.csv`・`PDF/24_05_F1〜F4.pdf`。出力を全部貼る。
- 途切れた時(Mac が眠った・電源・Ctrl-C)だけ、同じコマンドを 1 回だけやり直してよい(事前登録 6 節)。その時の結果は `_rerun_<UTC>` の
  名前になる。以下の M4〜M7 では、その `_rerun_<UTC>` を `--ref-suffix` に渡す(下の各ステップに書いた)。
- `判定(事前宣言、H1): INCONCLUSIVE` の時は、ここで終わり(M4〜M5c と M7 は回さない。M6a と M6b だけ行う)。

### M4 — 24_06f の dev
```bash
cd ~/SWIFT && caffeinate -i uv run python src/24_06f_nagano2014_learned_test.py --dev; echo "exit code: $?"
```
- 確かめること: `G-feat PASS  G-model PASS`・`G-same … PASS`・`DEV (no verdict)`。**この 3 つを確かめてから** M5 へ。どれかが違えば止めて貼る。

### M5 — 24_06f の本番(1 回だけ)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/24_06f_nagano2014_learned_test.py; echo "exit code: $?"
```
- 24_05 の正式な結果が `_rerun_<UTC>` の時だけ、末尾に `--ref-suffix _rerun_<UTC>` を付ける(M5b・M5c も同じ)。

### M5b — 24_06g の本番(1 回だけ)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/24_06g_nagano2014_gate_test.py; echo "exit code: $?"
```
- 24_05 の正式な結果が `_rerun_<UTC>` の時だけ、末尾に `--ref-suffix _rerun_<UTC>` を付ける。

### M5c — 24_08(H6 の記述)
```bash
cd ~/SWIFT && uv run python src/24_08_nagano2014_intensity_descriptive.py; echo "exit code: $?"
```
- 24_05 の正式な結果が `_rerun_<UTC>` の時だけ、末尾に `--ref-suffix _rerun_<UTC>` を付ける。

### M6a — 記録を写す
- Drive の次を `~/Downloads/nagano_reports/` に持って来る(Drive からフォルダごと落とすと zip になるので、展開してから中のファイルを置く):
  `ARGUS/data/catalog/24_01_nagano2014_catalog.json`、`ARGUS/data/catalog/jma_nagano2014.csv`、`ARGUS/PDF/24_01_nagano2014_catalog.pdf`、
  `ARGUS_nagano2014/data/24_02_report.json`、`ARGUS_nagano2014/data/24_02_plan.json`、
  `ARGUS_nagano2014/models/locator/15_01c_build_report_nagano2014_m15.json`、`ARGUS_nagano2014/data/24_03h_overlap_exclusion.json`、
  `ARGUS_nagano2014/data/24_04d_gclock2.json`、`ARGUS_nagano2014/data/24_04e_station_picks.csv`、`ARGUS_nagano2014/models/24_07_causal_picks_nagano2014.json`、
  `ARGUS_nagano2014/PDF/` の PDF(Colab で止めた時は、そこまでにできた物だけ)。
```bash
mkdir -p ~/ARGUS_prereg_21_04/24/results
cp ~/Downloads/nagano_reports/* ~/ARGUS_prereg_21_04/24/results/
cd ~/SWIFT && find models data PDF -maxdepth 1 -name '24_0*_rerun_*' -print; echo "rerun check done"
cd ~/SWIFT && find data/nagano2014_processed models data PDF -maxdepth 1 -type f \( -name '24_07_causal_picks_nagano2014.csv' -o -name '24_05_*' -o -name '24_06f_*' -o -name '24_06g_*' -o -name '24_08_*' \) -exec cp {} ~/ARGUS_prereg_21_04/24/results/ \;
ls ~/ARGUS_prereg_21_04/24/results
```
- `rerun check done` の前に何か出たら、M3 をやり直した時。その名前の `_rerun_<UTC>` の部分を M7 の `SFX` に書く。
- 2 つ目の `find … -exec cp` は、ある物だけを写す(無い物があってもエラーにならない)。

### M7 — すその印(事前登録 7 節の式。記述)。M6b の commit の前に回す。24_05 が INCONCLUSIVE の時は回さない
```bash
cd ~/SWIFT && SFX="" && uv run python - "$SFX" <<'EOF' | tee ~/ARGUS_prereg_21_04/24/results/24_M7_tail.txt
import json, csv, sys
SFX = sys.argv[1]
J = json.load(open(f'models/24_05_judgment{SFX}.json')); JF = json.load(open('models/24_06f_judgment.json'))
R = list(csv.DictReader(open(f'data/24_05_per_event{SFX}.csv'))); RF = list(csv.DictReader(open('data/24_06f_per_event.csv')))
N, NF = J['n_evaluated'], JF['n_evaluated']
print('24_05 suffix', repr(SFX), '| N', N, 'rows', len(R), '| NF', NF, 'rows', len(RF))
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
- M3 をやり直した時は、`SFX=""` を `SFX="_rerun_<UTC>"`(M6a で出た名前の部分)に替える(24_06f の出力の名前は替えない)。
- H5 が NOT-EVALUATED の時は、τ までの検測の列は出ない(`causal BEST = None`)。

### M6b — commit・push
```bash
cd ~/ARGUS_prereg_21_04 && git add 24/results && git status && git commit -m "24: results (Northern Nagano 2014)" && git push && git log -1 --oneline
```
