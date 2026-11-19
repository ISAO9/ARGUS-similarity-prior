# 変更の記録 04 の回し方 — 21_20h(重なった地震を除く)→ G-clock2 → Mac の試験

順番は変更の記録 04 の 6 節のとおり。セルの番号は **H1〜H6**(元の手順のセル 1〜15 とは別のノート。`21_20h_osaka2018_a04_colab.ipynb` を新しく作る)。
スクリプトを回す行には、全て `; echo "exit code: $?"` を付けてある。0 以外なら、その出力を全部貼る。
ランタイムは **CPU・ハイメモリ**(GPU は要らない)。

---

## 0 部 Mac: 置く・確かめる・push する・Zenodo(H1 の前に必ず)

### 0-A 置いて SHA-256 を確かめる
- ダウンロードした 3 つ(`21_20h_osaka2018_overlap_exclusion.py`・`21_20_amendment_04.md`・`21_20h_COLAB_STEPS_JA.md`)を `~/Downloads/a04/` に置く。
```bash
mkdir -p ~/ARGUS_prereg_21_04/21_20
cp ~/Downloads/a04/* ~/ARGUS_prereg_21_04/21_20/
cd ~/ARGUS_prereg_21_04/21_20 && shasum -a 256 21_20h_osaka2018_overlap_exclusion.py 21_20d_osaka2018_gclock2_picks.py 21_20e_osaka2018_station_pick_diagnose.py 21_20_osaka2018_similarity_confirmation.py 21_20f_osaka2018_learned_test.py
cd ~/ARGUS_prereg_21_04/22 && shasum -a 256 22_04_osaka2018_gate_test.py
```
- 期待: 6 行とも、変更の記録 04 の 9 節の表と全桁で同じ。違えば止める。

### 0-B push と Zenodo
```bash
cd ~/ARGUS_prereg_21_04
git add 21_20/21_20h_osaka2018_overlap_exclusion.py 21_20/21_20_amendment_04.md 21_20/21_20h_COLAB_STEPS_JA.md
git commit -m "21_20/22: amendment 04 (exclude events overlapping another catalogue event; before opening)"
git push
git log -1 --format=%H
```
- Zenodo(10.5281/zenodo.23905464)で「New version」を作り、この 3 つのファイルを足して公開する(埋め込みの期間は前の版と同じ)。
- commit の hash と Zenodo の新しい版を、記録 04 の 6 節の「記入欄」に書いて、もう一度 commit・push する。
- **ここまで終わるまで H1 に進まない。**

### 0-C Drive に置く
- `21_20h_osaka2018_overlap_exclusion.py` を Drive の `マイドライブ/ARGUS/src/` に直に上げる(21_20d・21_20e と同じ場所)。

---

## Colab

### H1 — Drive と場所の変数・SHA-256 の確かめ
```python
from google.colab import drive; drive.mount('/content/drive')
!pip -q install seisbench obspy
import torch, numpy; print(torch.__version__, numpy.__version__)
SRC = '/content/drive/MyDrive/ARGUS/src'
CAT = '/content/drive/MyDrive/ARGUS/data/catalog'
DRV = '/content/drive/MyDrive/ARGUS_osaka2018'
A04 = '/content/ARGUS_osaka2018_a04'          # この記録のための新しい置き場所(1 回目の 21_20d の出力を上書きしない)
DRV4 = '/content/drive/MyDrive/ARGUS_osaka2018_a04'
REF_CACHE_2026 = '/content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt'
CACHE0 = f'{DRV}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt'
CACHE4 = f'{A04}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt'
!sha256sum {SRC}/21_20h_osaka2018_overlap_exclusion.py {SRC}/21_20d_osaka2018_gclock2_picks.py {SRC}/21_20e_osaka2018_station_pick_diagnose.py {CACHE0}
!ls -la {DRV}/data/21_20b_report.json {DRV}/data/21_20g_clock_hour_diagnose.json {CAT}/jma_osaka2018.csv
```
- 期待: 3 本のスクリプトが記録 04 の 9 節の値、キャッシュが `b9162a9d8aab…1922aa83`。3 つのファイルがある。違えば止める。
- `21_20g_clock_hour_diagnose.json` が無ければ、H2 の `--g-json` の行を消して回す(記述が出ないだけで、規則には関わらない)。

### H2 — 21_20h(重なった地震を除く)
```python
!python {SRC}/21_20h_osaka2018_overlap_exclusion.py --cache {CACHE0} --catalog {CAT}/jma_osaka2018.csv --report {DRV}/data/21_20b_report.json --g-json {DRV}/data/21_20g_clock_hour_diagnose.json --out {A04}; echo "exit code: $?"
```
- 出力を全部貼る。最初の行の `本スクリプト v1 SHA-256 …` が 9 節の値であること。
- `STOP(R2)` か `STOP(R3)` で終わったら、そこで大阪を終える(記録 04 の 6 節の 2)。どちらも記録の JSON は書かれ、キャッシュは書かれない。
  次の 3 行だけを回して JSON を Drive に写し、Mac に持って来る(H3 は回さない):
```python
!mkdir -p {DRV4}/data && cp {A04}/data/21_20h_overlap_exclusion.json {DRV4}/data/
drive.flush_and_unmount(); drive.mount('/content/drive')
!ls -la {DRV4}/data/21_20h_overlap_exclusion.json
```
- それ以外の `STOP:`(キャッシュの SHA-256 が違う・自分の行が見つからない・本震が想定と違う)で終わったら、何も書かれない。出力を全部貼って相談する。
- 通ったら、表示の「除いた後: 地震 …・試験の候補 …」と、最後の `SHA-256` を控える。

### H3 — Drive に写す・確かめる
```python
!mkdir -p {DRV4}/data/tottori_processed
!cp {A04}/data/21_20h_overlap_exclusion.json {DRV4}/data/
!cp {CACHE4} {DRV4}/data/tottori_processed/
drive.flush_and_unmount(); drive.mount('/content/drive')
!sha256sum {CACHE4} {DRV4}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt
```
- 期待: 2 行が同じで、H2 の最後の SHA-256 と同じ。

### H4 — ここで一度止めて、Mac で記録する(試験を開く前)
- 記録 04 の 6 節の「記入欄」の 3・4 行目に、H2 の SHA-256・地震の数(前 → 後)・除いた数・試験の候補(前 → 後)を書く。
  H2 が表示した震源一覧と 21_20b の報告の SHA-256 も、同じ欄に書き足す(この 2 つは元の登録で全桁を固定していないため)。
- Drive の `ARGUS_osaka2018_a04/data/21_20h_overlap_exclusion.json` をダウンロードして `~/Downloads/` に置く。
- それを `~/ARGUS_prereg_21_04/results_21_20_a04/` に置き、記録と一緒に commit・push する。
```bash
mkdir -p ~/ARGUS_prereg_21_04/results_21_20_a04 && mv ~/Downloads/21_20h_overlap_exclusion.json ~/ARGUS_prereg_21_04/results_21_20_a04/
cd ~/ARGUS_prereg_21_04 && git add 21_20/21_20_amendment_04.md results_21_20_a04 && git commit -m "21_20 amendment 04: 21_20h output recorded" && git push
```

### H5 — 21_20d・21_20e を、除いた後のキャッシュで回す
```python
!mkdir -p {A04}/data {A04}/PDF
!cp {DRV}/data/21_20b_report.json {A04}/data/
!python {SRC}/21_20d_osaka2018_gclock2_picks.py --base {A04} --cache {CACHE4} --ref-cache {REF_CACHE_2026}; echo "exit code: $?"
!python {SRC}/21_20e_osaka2018_station_pick_diagnose.py --base {A04} --cache {CACHE4} --ref-cache {REF_CACHE_2026}; echo "exit code: $?"
```
- 21_20d の最後の行が `[21_20d] STOP(G-clock2): …`(exit code 1)なら、条件のどれかの FAIL。止めずに H6 に進み、H6 で決める。
- それ以外の `[21_20d] STOP: …`(検測 100 未満・日・局・時間のどれかが 0・報告が無い)で終わった時は、判定できないので止める(JSON は書かれない)。
- `--base` を `{A04}` にしてあるので、1 回目の 21_20d の出力(Drive の `{DRV}/data/21_20d_gclock2.json`)は上書きされない。

### H6 — 案 C の判定に要る値を表示し、Drive に写す(読むだけ。事前登録 5.3 節をそのまま当てる)
```python
import json, csv
J = json.load(open(f'{A04}/data/21_20d_gclock2.json'))
for k in ['pass_all', 'pass_day', 'pass_station', 'pass_hour', 'pass_events', 'pass_measured_frac', 'gclock2_pass']: print(k, J[k])
for x in J['gclock_events']:
    print('  (e)', x['origin_jst'], 'Mj', x['mj'], 'found_dt_s', round(x['found_dt_s'], 3), 'n_picks', x['n_picks'], 'PASS' if x['pass_'] else 'FAIL')
rows = list(csv.DictReader(open(f'{A04}/data/21_20e_station_picks.csv')))
near = [r for r in rows if float(r['epi_from_mainshock_km']) <= 80.0 and int(r['n']) >= 20]
bad_near = [r for r in near if abs(float(r['dev_s'])) > 1.0]
bad_far = [r for r in rows if float(r['epi_from_mainshock_km']) > 80.0 and int(r['n']) >= 20 and abs(float(r['dev_s'])) > 1.0]
print('(c-near) 80 km 以内・n ≥ 20 の局', len(near), '  |dev_s| > 1.0 s の局', len(bad_near))
for r in bad_near: print('   ', r['station'], r['epi_from_mainshock_km'], 'km  n', r['n'], ' dev_s', r['dev_s'])
print('(c-far) 80 km より遠い・n ≥ 20 で |dev_s| > 1.0 s の局', len(bad_far))
for r in bad_far: print('   ', r['station'], r['epi_from_mainshock_km'], 'km  n', r['n'], ' dev_s', r['dev_s'])
!mkdir -p {DRV4}/data {DRV4}/PDF
!cp {A04}/data/21_20d_gclock2.json {A04}/data/21_20e_station_picks.csv {DRV4}/data/ ; cp {A04}/PDF/*.pdf {DRV4}/PDF/
drive.flush_and_unmount(); drive.mount('/content/drive')
!ls -la {DRV4}/data {DRV4}/PDF
```
- 読み方(事前登録 5.3 節。ここで新しく決めることは無い):
  - `pass_all`・`pass_day`・`pass_hour`・`pass_events`・`pass_measured_frac` のどれかが False → 止める。**大阪はそこで終える**(記録 04 の 6 節の 4。規則を足し直さない)。
  - (c-near) の |dev_s| > 1.0 s の局が 1 つでもある → 止める(同じ)。
  - `pass_station` が False で、上の 2 つに当たらない → 進む。全ての結果に、5.3 節の印と記録 04 の 7 節の印を並べて付ける。
  - `gclock2_pass` が True → 進む(記録 04 の 7 節の印だけ付ける)。
- H5・H6 の出力を全部貼る。

### Colab が切れた時(どのセルから回し直すか)
切れると `/content` の中(`{A04}` と変数)は消える。Drive の中は残る。どの場合も、まず H1 を回し直す。その後:

| 切れた所 | 次に回すもの |
|---|---|
| H2 の途中・H3 が終わる前 | H2 をもう 1 回だけ回す → H3。回し直したことと、2 回目の出力の SHA-256 を記録 04 の記入欄に書く(21_20h は同じ入力で同じものを書く) |
| H3 の後・H5 の前 | 下の「Drive から戻す」→ H5 |
| H5・H6 の途中 | 下の「Drive から戻す」→ H5 から(21_20d・21_20e は読むだけで、試験は開かない) |

Drive から戻す:
```python
!mkdir -p {A04}/data/tottori_processed && cp {DRV4}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt {A04}/data/tottori_processed/
!sha256sum {CACHE4}
```
- 期待: H4 で記録した SHA-256 と同じ。違えば止める。

---

## Mac(~/SWIFT。元の手順の 3 部と同じ。違うのは、全てのコマンドに `--cache` を付けることだけ)

### M1' — 置く・確かめる
- Drive の `ARGUS_osaka2018_a04/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt` を `~/SWIFT/data/osaka2018_processed/` に持って来る(元の手順の M1 と同じやり方)。
```bash
cd ~/SWIFT && shasum -a 256 data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt src/21_20_osaka2018_similarity_confirmation.py src/21_20f_osaka2018_learned_test.py src/22_04_osaka2018_gate_test.py models/21_06_ranker.pkl models/21_06a_train.json data/21_06a_train_rows.npz models/22_gate.pkl
ls models/21_20_* models/21_20f_* data/21_20_* data/21_20f_* models/22_04_* data/22_04_* PDF/22_04_* 2>/dev/null   # 何も無いこと
uv run python -c "import sklearn, numpy, sys; print(sklearn.__version__, numpy.__version__, sys.version)"   # 1.8.0 2.4.3 3.12.12
```
- 期待: キャッシュは H2 の値、スクリプトは記録 04 の 9 節の値。`21_06_ranker.pkl` は `0d0f75a48a50f866d3963c6560497abe1c007ecac628391284ca6fe248b712e1`、
  `21_06a_train.json` は `4f27ad1e0596d244b62b064918cde92cde6f93a13829a96bb6ac04079e13f87e`、`21_06a_train_rows.npz` は `ca23242288ad6fe4fdf5853960a6fd41b78328a59ec22bc5d484bf5334e632e9`
  (事前登録 21_20 の 8 節)、`22_gate.pkl` は 22_00 の 7 節の値。`ls` は何も出ない。

順番は記録 04 の 6 節の 5 のとおり: 21_20 の dev → 22_04 の dev → 21_20 の本番 → 21_20f の dev → 21_20f の本番 → 22_04 の本番。
どのブロックも、最初の行で場所とキャッシュの名前を決め直す(新しいターミナルでも同じに動くため)。

### M2 — 21_20 の dev → M2b — 22_04 の dev(どちらも試験を開かない)
```bash
cd ~/SWIFT && C4="data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt"
caffeinate -i uv run python src/21_20_osaka2018_similarity_confirmation.py --dev --cache "$C4"; echo "exit code: $?"
caffeinate -i uv run python src/22_04_osaka2018_gate_test.py --dev --cache "$C4"; echo "exit code: $?"
```
- 確かめることは元の手順の M2・M2b と同じ(G-untouched・G-split・G-causal・G-phys が PASS、`DEV (no verdict)`。22_04 は G-leak・G-same が PASS)。G-phys が FAIL なら本番は開かない。

### M3 — 21_20 の本番(1 回だけ)
```bash
cd ~/SWIFT && C4="data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt"
caffeinate -i uv run python src/21_20_osaka2018_similarity_confirmation.py --cache "$C4"; echo "exit code: $?"
```
- 出力を全部貼る。ここで一度止めて、出力を確かめてから M4 に進む。

### M4 — 21_20f の dev → M5 — 21_20f の本番 → M5b — 22_04 の本番
```bash
cd ~/SWIFT && C4="data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt"
caffeinate -i uv run python src/21_20f_osaka2018_learned_test.py --dev --cache "$C4"; echo "exit code: $?"
caffeinate -i uv run python src/21_20f_osaka2018_learned_test.py --cache "$C4"; echo "exit code: $?"
caffeinate -i uv run python src/22_04_osaka2018_gate_test.py --cache "$C4"; echo "exit code: $?"
```
- 途切れた時の扱い・`--ref-suffix` は元の手順の M3・M5b と同じ。

### M6' — 記録
- Drive の `ARGUS_osaka2018_a04/data/21_20d_gclock2.json`・`ARGUS_osaka2018_a04/data/21_20e_station_picks.csv`・`ARGUS_osaka2018_a04/PDF/` の PDF を
  ダウンロードして `~/Downloads/osaka_a04_reports/` に置く(1 回目の記録は `results_21_20/` にあるので、名前はぶつからない)。
```bash
mkdir -p ~/ARGUS_prereg_21_04/results_21_20_a04 ~/ARGUS_prereg_21_04/results_21_20f_a04 ~/ARGUS_prereg_21_04/results_22_04_a04
cp ~/Downloads/osaka_a04_reports/* ~/ARGUS_prereg_21_04/results_21_20_a04/
cd ~/SWIFT
cp models/21_20_judgment.json models/21_20_opened.json data/21_20_per_event.csv PDF/21_20_F1_error_vs_tau.pdf PDF/21_20_F2_paired_difference.pdf PDF/21_20_F3_similarity_vs_separation.pdf ~/ARGUS_prereg_21_04/results_21_20_a04/
cp models/21_20f_judgment.json models/21_20f_opened.json data/21_20f_per_event.csv PDF/21_20f_F1_learned_test.pdf ~/ARGUS_prereg_21_04/results_21_20f_a04/
cp models/22_04_judgment.json models/22_04_opened.json ~/ARGUS_prereg_21_04/results_22_04_a04/; cp data/22_04_per_event.csv PDF/22_04_F1_gate_osaka.pdf ~/ARGUS_prereg_21_04/results_22_04_a04/ 2>/dev/null
ls models/21_20*_rerun_* data/21_20*_rerun_* PDF/21_20*_rerun_* models/22_04*_rerun_* data/22_04*_rerun_* PDF/22_04*_rerun_* 2>/dev/null   # 出たら、それぞれの results_*_a04 に写す
cd ~/ARGUS_prereg_21_04 && git add results_21_20_a04 results_21_20f_a04 results_22_04_a04 && git commit -m "21_20/22_04 (amendment 04): results (Northern Osaka 2018)" && git push
```
- すその印(事前登録 21_20 の 7 節)は、元の手順の M6 の式で計算する(記述)。
