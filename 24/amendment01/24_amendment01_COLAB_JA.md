# 24 変更の記録 01 — 回す手順(Mac で登録 → Colab のセル A1〜A3 → A4 → N15 へ)

この順でしか回さない。**A3(24_04h)は、1 部(push と Zenodo の公開)が全て済んでから、1 回だけ回す**(規則を登録してから判定を計算するため)。

---

## 1 部 Mac: 置く・確かめる・push する・Zenodo の新しい版を取る

### 1-A 束を置いて、SHA-256 を確かめる
```bash
mkdir -p ~/ARGUS_prereg_21_04/24/amendment01
cd ~/Downloads && unzip -o 24_amendment01.zip -d ~/ARGUS_prereg_21_04/24/amendment01/
cd ~/ARGUS_prereg_21_04/24/amendment01 && ls && shasum -a 256 *.py
```
- Safari が zip を自動で展開した時は、2 行目(unzip)を回さず、代わりに
  `cp ~/Downloads/24_amendment01/* ~/ARGUS_prereg_21_04/24/amendment01/` を回してから 3 行目を回す。
- 期待: `ls` は次の 8 個だけ。
  `24_amendment01_nagano2014.md`・`24_amendment01_COLAB_JA.md`・`24_04g_COLAB_JA.md`・`24_04g_nagano2014_clock_hour_diagnose.py`・
  `24_04h_nagano2014_gclock2_amend01.py`・`24_04g_clock_hour_diagnose.json`・`24_04g_clock_hour_diagnose.pdf`・`24_04g_output.txt`
- 期待: 2 行の値が、記録 `24_amendment01_nagano2014.md` の 6 節の表と全桁で同じ
  (24_04g は `dc3a8a92…`、24_04h は `98c7d515…`)。
- `24_04g_output.txt` は、貼っていただいた G3 の出力をそのまま写したもの。`.json`・`.pdf` は添付いただいた物の写し(名前の頭の記号だけを外した)。

### 1-B 0 節のチェックを埋める
```bash
ls ~/SWIFT/models | grep 24_0; echo "check done"
```
- 期待: `check done` だけが出る(24_05 などを回していない)。
- 記録 `24_amendment01_nagano2014.md` の 0 節の 3 つの `[ ]` を、確かめてから `[x]` にする(テキストエディタで)。
  3 つ目((a)・(b)・(e)・(f) が PASS、(c) は FAIL で (c-near) は通った)は、N13・N14b の出力で確かめる。違っていたら commit せずに知らせる。

### 1-C 足すファイルを確かめる(まだ commit しない)
```bash
cd ~/ARGUS_prereg_21_04 && git add 24/amendment01 && git status
```
- 期待: `new file:` が `24/amendment01/` の 8 つだけ。`.DS_Store` が出たら
  `git restore --staged 24/amendment01/.DS_Store` で外し、8 つだけになってから 1-D へ。

### 1-D commit・push
```bash
cd ~/ARGUS_prereg_21_04 && git commit -m "24: amendment 01 (G-clock2 condition d), registered before opening" && git push && git log -1 --format=%H
```
- 最後の行(commit の hash、40 文字)を控える。

### 1-E Zenodo の新しい版
- v3 の記録(10.5281/zenodo.24239732)を開き「New version」。前の版のファイルは残したまま、`24/amendment01/` の 8 つを足す。
- 題: `v4: amendment 01 to preregistration 24 (Northern Nagano 2014)`。説明に 1-D の commit の hash を書く。
- 非公開期間(embargo)の終わりの日は、前の版と同じにする。公開する。
- 公開後に出る新しい版の DOI(24239732 ではない)と、公開した日時を控える。
- hash・DOI・日時は 4 部(M6a)で書き、M6b で commit する。この登録のための 2 回目の push はしない。

---

## 2 部 Colab: 24_04h(G-clock2 の判定、変更の記録 01)

### 置く場所とノート
- `24_04h_nagano2014_gclock2_amend01.py` を Drive の `ARGUS/src/` に置く。
- A1〜A3 は、新しい空のノート(ファイル → ノートブックを新規作成)に貼って回す。`24_nagano2014_colab.ipynb` には足さない。
  ランタイムのタイプは既定のままでよい。pip は要らない。

### A1 — Drive をつなぐ
```python
from google.colab import drive; drive.mount('/content/drive')
```

### A2 — SHA-256 と入力の確かめ
```python
import hashlib, os, glob
SRC = '/content/drive/MyDrive/ARGUS/src'
DRV = '/content/drive/MyDrive/ARGUS_nagano2014'
p = f'{SRC}/24_04h_nagano2014_gclock2_amend01.py'
h = hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else 'MISSING'
print('OK ' if h == '98c7d515086a1971354cce658645a6aeeb98218a9f6b8af47d247dbf984cbc5b' else 'NG ', '24_04h', h[:12])
print('(1) などの写し:', [os.path.basename(x) for x in glob.glob(f'{SRC}/24_04h*') if '(' in x] or 'なし')
for q in [f'{DRV}/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt',
          f'{DRV}/data/24_04d_gclock2.json', f'{DRV}/data/24_04e_station_picks.csv']:
    print('ある ' if os.path.exists(q) else '無い ', q)
print('24_04h の結果:', 'もうある(A3 は回さない)' if os.path.exists(f'{DRV}/data/24_04h_gclock2_amend01.json') else 'まだ無い')
```
- 期待: `OK`、写しは `なし`、3 つとも `ある`、最後は `まだ無い`。

### A3 — 24_04h を回す(1 回だけ。結果の JSON がある時はセルが止まる)
```python
import os
assert input('1 部(commit・push・Zenodo の新しい版の公開)は全て済んだか? 済んだら yes: ').strip() == 'yes', '1 部を先に'
assert not os.path.exists(f'{DRV}/data/24_04h_gclock2_amend01.json'), '24_04h は回し済み(結果が Drive にある)。回し直さない'
!date -u
!python {SRC}/24_04h_nagano2014_gclock2_amend01.py --base {DRV} > /content/24_04h_log.txt 2>&1; echo "exit code: $?"
!date -u
!cat /content/24_04h_log.txt
```
- 入力の STOP(入力が無い・24_04d と食い違う)の時は JSON ができないので、入力を置き直してからもう一度回せる。
- 貼るもの: A2 の出力・A3 の出力の全て(2 つの `date -u` の行も)・`ARGUS_nagano2014/PDF/24_04h_gclock2_amend01.pdf`。
- できる物(Drive に直接書く): `ARGUS_nagano2014/data/24_04h_gclock2_amend01.json`・`ARGUS_nagano2014/PDF/24_04h_gclock2_amend01.pdf`。
- 読み方:
  - `exit code: 0` と `G-clock2(事前登録 24・変更の記録 01): PASS` → 3 部へ。表示された印(英語・日本語)と、
    「さらに 5.3 節の 4 の (c-far) の印も付ける」の行の下の印を、結果の記録に付ける(正式な文は記録の 4 節)。
  - `exit code: 1` と、最後が `STOP(G-clock2・変更の記録 01)` → 止める。N15 から先も、Mac の M1〜M5c・M7 も回さない。
    clock could not be verified と報告し、4 部の M6a・M6b だけを行う。**これ以上の変更はしない。**
  - それ以外の `STOP`(入力が無い・24_04d と食い違う・24_04e の表と食い違う)→ 判定はまだ。出力を貼る。

---

## 3 部 PASS の後: N15 へ

`24_nagano2014_colab.ipynb` を開き、ランタイム → ランタイムのタイプを変更 → CPU・ハイメモリ にする(A1〜A3 を回したランタイムは
使い続けない)。24_STEPS_JA.md の「Colab が切れた時」の表の「N12b の後・N15 の前」の行のとおり、次の順に回す。

1. N1 → N2(N3・N4 は、N9 の組み立てにも N15 にも要らないので飛ばしてよい。回しても害はない。N4 は Hi-net の
   パスワードをもう一度聞く)。
2. R0(下)→ N9(h5 をローカルに作り直す)→ R1(下)。
3. NR → N10a → A4(下)→ N15 → N16 → N17。

### R0 — N9 の前に、最初の N9 の報告を控える
```python
!cp -n {DRV}/data/24_02_report.json {DRV}/data/24_02_report_firstrun.json
!sha256sum {DRV}/data/24_02_report.json {DRV}/data/24_02_report_firstrun.json
```
- N9 は Drive の `24_02_report.json` と 24_02 の PDF を書き直すので、最初の報告を `_firstrun` の名前で残す(`-n` で、既にあれば上書きしない)。
- N9 は、最初の N9 と同じ形で回す(最初に `--allow-missing` を付けた時だけ今回も付ける)。最後の表示は、最初の N9 と同じ
  (同じ `STOP(G-clock だけ)` か PASS)のはず。

### R1 — N9 の後に、報告が同じかを確かめる
```python
!sha256sum {DRV}/data/24_02_report.json {DRV}/data/24_02_report_firstrun.json
```
- 期待: 2 行の値が同じ。違う時は N10a に進まず、R0・N9・R1 の出力を貼る(PDF は作り直されるので、値が違っても構わない)。

### A4 — N15 の前に、24_04h が合格したことを確かめる
```python
import json; J4 = json.load(open(f'{DRV}/data/24_04h_gclock2_amend01.json'))
assert J4['gclock2_pass_amend01'] is True and J4['script_sha256'] == '98c7d515086a1971354cce658645a6aeeb98218a9f6b8af47d247dbf984cbc5b', 'N15 に進まない'
print('24_04h PASS: N15 へ')
```
- N15 は窓の索引(IDX)を作り直すので、最初に数十分止まって見える(正常)。
- その後は Mac の M1 から、24_STEPS_JA.md のとおり。

---

## 4 部 PASS でも FAIL でも: M6a・M6b に足すこと

### M6a に足す
- Drive から持って来る物に、次の 2 つを足す(PDF は「`ARGUS_nagano2014/PDF/` の PDF」に入っている):
  `ARGUS_nagano2014/data/24_04g_clock_hour_diagnose.json`、`ARGUS_nagano2014/data/24_04h_gclock2_amend01.json`。
- 3 部を回した時は、`ARGUS_nagano2014/data/24_02_report_firstrun.json` も足す。
- テキストエディタで `~/ARGUS_prereg_21_04/24/results/24_amendment01_registration.txt` を作り、次を書く:
  1-D の commit の hash(40 文字)・1-E の Zenodo の DOI と公開した日時・A3 の 2 つの `date -u` の行・
  24_04h の判定(PASS/FAIL)と、(d3) の前と後の検測の数と中央値・A3 の出力の全て(貼り付け)。

### M6b(24_STEPS_JA.md の M6b の代わりにこれを回す)
```bash
cd ~/ARGUS_prereg_21_04 && git add 24/results && git status
```
- 期待: `24/results/` のファイルだけ(`24_amendment01_registration.txt` を含む)。`24/amendment01/` の記録は書き換えないので、出ない。
```bash
cd ~/ARGUS_prereg_21_04 && git commit -m "24: results (Northern Nagano 2014), with amendment 01 registration record" && git push && git log -1 --oneline
```
