# 21_20 大阪府北部 2018 — 回す手順(Mac の準備 + Colab のセルごと + Mac)

ノート名: `21_20_osaka2018_colab.ipynb`(新しく作る)。セルの番号は 21_04 のノート(21_04_ct2016_colab.ipynb)と同じにしてある
(21_20b・21_20c の表示の「セル 8」「セル 9」「セル 10」が、そのままこの番号を指す)。足したセルは 2b・11b・13b・15 で、番号はずらしていない。

前提:
- 事前登録の記録 `21_20_preregistration_osaka2018.md` の「本人が確かめる」を閉じ、7 本のスクリプトと一緒に push し、外部の時刻の記録を取ってから
  セル 5 を回す(0 部)。
- スクリプトは Drive の `/content/drive/MyDrive/ARGUS/src/` に直に置く(下のフォルダを作らない)。21_20a・21_20b は、スクリプトの 1 つ上
  (`MyDrive/ARGUS`)を出力の根に使うため。
- 置き場所:
  - Drive: `/content/drive/MyDrive/ARGUS/data/catalog/`(21_20a の出力)、`/content/drive/MyDrive/ARGUS_osaka2018/`(区切りのファイル・報告・最終のキャッシュのコピー)
  - Colab のローカル: `/content/ARGUS_osaka2018/`(h5 の組み立て・21_20c・21_20d・21_20e。21_04 の変更の記録 02 で、Drive に直接書いた約 5 GB の h5 が消えたため)
- ランタイム: 最初から最後まで **CPU・ハイメモリ**(下の「セル 1 の前に」)。21_04 の変更の記録 03: 15_01c の 1 回目は保存の直前にメモリ不足で止まった。
- スクリプトを回す行には、全て `; echo "exit code: $?"` を付けてある。0 以外なら、その出力を全部貼る。

---

## 0 部 Mac: 置く・確かめる・push する・外部の時刻の記録を取る(セル 5 の前に必ず)

### 0-A 束を置いて、SHA-256 を確かめる
- ダウンロードした束(7 本のスクリプトと `21_20_preregistration_osaka2018.md`・`COLAB_STEPS_JA.md`・`DIFF_LOG.md`)を
  `~/Downloads/osaka_bundle/` に置く。
```bash
mkdir -p ~/ARGUS_prereg_21_04/21_20
cp ~/Downloads/osaka_bundle/21_20*.py ~/Downloads/osaka_bundle/COLAB_STEPS_JA.md ~/Downloads/osaka_bundle/DIFF_LOG.md ~/ARGUS_prereg_21_04/21_20/
cd ~/ARGUS_prereg_21_04/21_20 && ls && shasum -a 256 21_20*.py
```
- 期待: `ls` に 10 個(7 本の .py と 3 つの .md)。`shasum` の 7 行が、事前登録の記録の 8 節の表と全桁で同じ。違えば止める。
- 置き場所の `21_20/` は、同じリポジトリの `21_16/` と同じ形(本人が確かめる: 21_04 の時と違う置き方にしたいなら、ここで変える)。
- Mac で回す 2 本を ~/SWIFT に置く:
```bash
cp ~/ARGUS_prereg_21_04/21_20/21_20_osaka2018_similarity_confirmation.py ~/ARGUS_prereg_21_04/21_20/21_20f_osaka2018_learned_test.py ~/SWIFT/src/
cd ~/SWIFT && shasum -a 256 src/21_20_osaka2018_similarity_confirmation.py src/21_20f_osaka2018_learned_test.py
```
- 期待: 8 節の 21_20 と 21_20f の値。

### 0-A2 信頼の切り替え(22)の束も置く(2026-11-02 に足した。大阪を AI の試験にも使うため。事前登録 22_00)
- 22 の束(`22_00_preregistration_trust_gate_DRAFT.md`・`22_01a_gate_rows_wt2026.py`・`22_02_gate_train_freeze.py`・`22_04_osaka2018_gate_test.py`)を
  `~/Downloads/gate22_bundle/` に置く。22_01a と 22_02 は ~/SWIFT/src/ で既に回したもの(凍結済み)。
```bash
mkdir -p ~/ARGUS_prereg_21_04/22
cp ~/Downloads/gate22_bundle/22_* ~/ARGUS_prereg_21_04/22/
cp ~/Downloads/gate22_bundle/22_04_osaka2018_gate_test.py ~/SWIFT/src/
cd ~/SWIFT && cp models/22_gate.pkl models/22_02_train.json models/22_02_opened.json models/22_01a_rows.json PDF/22_02_F1_gate_check.pdf ~/ARGUS_prereg_21_04/22/
shasum -a 256 src/22_01a_gate_rows_wt2026.py src/22_02_gate_train_freeze.py src/22_04_osaka2018_gate_test.py models/22_gate.pkl data/22_01a_rows_wt2026.npz models/22_02_train.json models/22_01a_rows.json
```
- 期待: 7 行とも 22_00 の 7 節の表と全桁で同じ。違えば止める。
- 22_00 の冒頭の 2 つのチェックを、本人が確かめて埋める(大阪を一つも開いていないこと。Colab の Drive に大阪のファイルが無いことも確かめる)。

### 0-B Colab で使う 5 本を Drive に置く
- `21_20a`・`21_20b`・`21_20c`・`21_20d`・`21_20e` の 5 本を、`マイドライブ/ARGUS/src/` に**直に**上げる(下のフォルダに入れない)。
- 同じ名前のファイルが既にあれば、先にそれを消すか置き換える。Drive は同じ名前の 2 つ目や「… (1).py」を作ることがある。
- 確かめはセル 2 で行う(5 本の SHA-256 と、同じ名前のファイルが 2 つ無いこと)。

### 0-C(Colab のセル 1・2・2b の後)記録を閉じて push する
- `~/ARGUS_prereg_21_04/21_20/21_20_preregistration_osaka2018.md` をエディタで開き、14 節の 1〜4・6・7・10 を埋める
  (冒頭のチェック、5.3 節の 4 の最後の 1 行、セル 2b の値か「回していない」)。
```bash
cd ~/ARGUS_prereg_21_04 && git status
git add 21_20 22
git commit -m "21_20 and 22: preregistrations, frozen scripts and the frozen trust gate (Northern Osaka 2018)"
git push
git log -1 --format=%H
```
- 最後の行の hash を控える(1 回目の commit)。

### 0-D 外部の時刻の記録(セル 5 の前に必ず。事前登録の記録の冒頭)
- 1 回目の commit の 21_20 の 10 個のファイルと 22 の全てのファイルを、外部の時刻が残る所に置く(例: OSF のプロジェクトに置き、非公開期間付きの登録を作る)。
- 登録の画面に出る日時と URL を控える。承認待ちなどの表示が出たら、その表示もそのまま控える(本人が確かめる: その表示でも時刻が残るか)。

### 0-E 2 回目の commit(hash と外部の記録を書く)
- 記録の冒頭の「commit の hash」に 0-C の hash を、「置いた先・日時・URL」に 0-D の値を書く(21_04 と 21_16 の記録と同じ形)。
  22_00 の 7 節の「本記録」と「commit hash・外部の時刻の記録」にも同じ値を書く。
```bash
cd ~/ARGUS_prereg_21_04
git add 21_20/21_20_preregistration_osaka2018.md 22/22_00_preregistration_trust_gate_DRAFT.md
git commit -m "21_20: record the commit hash and the external timestamp"
git push
```
- ここまで済んでから セル 3 以降に進む(セル 3・4 は回してよいが、セル 5 は 0-E の後)。

---

## 1 部 Colab: 震源と波形(セル 1〜9)

### セル 1 の前に — ランタイムのタイプ
- メニューの「ランタイム → ランタイムのタイプを変更 → CPU・ハイメモリ」にする。GPU は要らない。
- **最後まで変えない**。途中で変えると `/content` が消える(Colab のローカルの h5・キャッシュ・win32tools・環境変数が無くなる)。

### セル 1 — Drive と道具
```python
from google.colab import drive; drive.mount('/content/drive')
!pip -q install HinetPy==0.13.0 seisbench obspy
import h5py, torch, numpy, scipy; print(h5py.__version__, torch.__version__, numpy.__version__, scipy.__version__)
```
- 期待: エラーなしで版が表示される。HinetPy は 21_04b と同じ 0.13.0。

### セル 2 — 場所の変数と、スクリプトの SHA-256 の確かめ
```python
import hashlib
SRC = '/content/drive/MyDrive/ARGUS/src'
CAT = '/content/drive/MyDrive/ARGUS/data/catalog'
DRV = '/content/drive/MyDrive/ARGUS_osaka2018'
LO  = '/content/ARGUS_osaka2018'
REF_CACHE_2026 = '/content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt'
EXP = {  # 事前登録の記録の 8 節と同じ値
    '21_20a_osaka2018_jma_catalog.py':           'cad845a14375014056b7da2a539b750d88363be56620904381fd520db16d25d2',
    '21_20b_osaka2018_hinet_to_h5.py':           '43154e7a3b33451d6a2526f4a1b3ff4a8e6085964c380398ceab49b50745e06e',
    '21_20c_osaka2018_realpick_cache_colab.py':  '7b938b944003d99fcad7df188792e8e8eb95c71b07f1a1223bffad6671d04cf0',
    '21_20d_osaka2018_gclock2_picks.py':         '606d0eea2f76a8607c7844f83a93056759640974bce7f11ccfe690ecb6e7c1d6',
    '21_20e_osaka2018_station_pick_diagnose.py': '680e8825d49e00bba58cca9045c66ee7b213f05bc5a231d0810d041b4fefba92',
}
for n, h in EXP.items():
    got = hashlib.sha256(open(f'{SRC}/{n}', 'rb').read()).hexdigest()
    print('OK  ' if got == h else 'NG  ', n, got)
!ls -la {SRC} | grep 21_20
!find /content/drive/MyDrive -name "tottori_all_100Hz.h5" 2>/dev/null
```
- 期待: 5 行とも `OK`。`ls` の 21_20 の行が 5 つだけ(「(1)」の付いた名前や同じ名前の 2 つ目が無い)。`NG` が 1 つでもあれば止める(push する版でない)。
- `find` に出た `tottori_all_100Hz.h5` のパスを次の行で変数にする(21_20b の参照の h5。読むだけ):
```python
REF_H5 = '<上の find に出たパス>'
```

### セル 2b(任意・記述だけ)— 鳥取 2026 のキャッシュでの (c) の値
- **案 C では判定に使わない**。回すなら 0-C の push の前に回し、値を事前登録の記録の 5.3 節の 7 に書く。回さなくてもよい(その時は「回していない」と書く)。
- 21_20d は `--report` の 4 地震を必ず読むので、空の報告(4 地震なし)を置いて回す。`--cache` に絶対パスを渡すと、そのファイルを読む。
```python
import json, os
R26 = '/content/ref2026_c'                      # 大阪の置き場所とは別。Drive には書かない
os.makedirs(f'{R26}/data', exist_ok=True)
json.dump({'gates': {'clock': []}}, open(f'{R26}/data/21_20b_report.json', 'w'))
!sha256sum {REF_CACHE_2026}
!python {SRC}/21_20d_osaka2018_gclock2_picks.py --base {R26} --cache {REF_CACHE_2026}; echo "exit code: $?"
!python {SRC}/21_20e_osaka2018_station_pick_diagnose.py --base {R26} --cache {REF_CACHE_2026}; echo "exit code: $?"
```
- `sha256sum` の期待: `420fe1e304f43aae9baa7cbab9474623e014d01dddb4dbecab6644431b6f0ef7`(21_02 の本番と 21_06a の学習で使ったキャッシュ。
  models/21_06a_train.json の `cache_sha256`)。違えば、このセルの値は書かない。
- 書くのは 21_20d の `(c) 局ごと … 最大のずれ X s` の 1 行だけ(と、望むなら 21_20e の表の 80 km 以内の局の |ずれ| の最大)。
- 読まないもの: (e) は 4 地震が無いので形だけの PASS。表示と図の「大阪府北部 2018」「Northern Osaka 2018」の名前は、このセルでは鳥取 2026 のこと。
- 21_20d は (c) などが FAIL だと exit code 1 で終わるが、このセルでは問題ない。キャッシュの中身が読めずに例外で止まった時は、このセルは諦めて
  「回したが読めなかった」と書く(本人が確かめる: 2026 のキャッシュの `origin_time` などが 21_20d の読み方で読めること)。

### セル 3 — win32tools(catwin32・win2sac_32)
- 21_04 のノートの セル 3 がそのまま使えるなら、それを写して回す(21_04 で動いた中身。こちらを先に使う)。
- 21_04 のノートが手元に無い時だけ、次を使う。Hi-net のページから取った `win32tools.tar.gz` を `マイドライブ/KRITES/` に置いておく。
  一度作れば `マイドライブ/KRITES/bin/` に残り、次からは作らずに写すだけになる。
```python
import os, glob, shutil, subprocess
KRI  = '/content/drive/MyDrive/KRITES'
KBIN = f'{KRI}/bin'
TGZ  = f'{KRI}/win32tools.tar.gz'
NEED = ['catwin32', 'win2sac_32']
if not all(os.path.isfile(f'{KBIN}/{n}') for n in NEED):
    if not os.path.isfile(TGZ):
        raise SystemExit(f'STOP: {TGZ} が無い。win32tools.tar.gz を マイドライブ/KRITES に置いてから回し直す')
    B = '/content/w32build'
    shutil.rmtree(B, ignore_errors=True); os.makedirs(B)
    subprocess.run(['tar', '-xzf', TGZ, '-C', B], check=True)
    top = [d for d in glob.glob(f'{B}/*') if os.path.isdir(d)]
    if len(top) != 1:
        raise SystemExit(f'STOP: 展開した中身が想定(フォルダ 1 つ)と違う: {top}')
    r = subprocess.run(['make'], cwd=top[0], capture_output=True, text=True)
    print(r.stdout[-3000:]); print(r.stderr[-3000:])
    if r.returncode != 0:
        raise SystemExit('STOP: make が失敗した(上の表示を貼る)')
    os.makedirs(KBIN, exist_ok=True)
    for n in NEED:
        hit = [p for p in glob.glob(f'{top[0]}/**/{n}', recursive=True) if os.path.isfile(p) and os.access(p, os.X_OK)]
        if len(hit) != 1:
            raise SystemExit(f'STOP: 作った {n} が 1 つに決まらない: {hit}')
        shutil.copy2(hit[0], f'{KBIN}/{n}')
for n in NEED:
    shutil.copy2(f'{KBIN}/{n}', f'/usr/local/bin/{n}')
    os.chmod(f'/usr/local/bin/{n}', 0o755)
!which catwin32 win2sac_32
!file /usr/local/bin/catwin32 /usr/local/bin/win2sac_32
```
- 期待: `which` に 2 つのパスが出る。`file` に `ELF`(Linux で動く形)と出る。`Mach-O` と出たら Mac で作ったものなので、`KRITES/bin` の
  2 つを消して、もう一度このセルを回す(tar.gz から作り直す)。
- 出なければ セル 6 以降の取得(--dry-run 以外)は止まる(21_20b の STOP)。

### セル 4 — Hi-net の資格情報(環境変数。ノートに書き残さない)
```python
import os, getpass
os.environ['HINET_USER'] = getpass.getpass('Hi-net user: ')
os.environ['HINET_PASS'] = getpass.getpass('Hi-net password: ')
```
- `!python` で回すスクリプトは、この環境変数を受け継ぐ(21_04b と同じ)。

### セル 5 — 21_20a: 気象庁の震源(h2018)。**0 部が全て済んでから**
```python
!python {SRC}/21_20a_osaka2018_jma_catalog.py; echo "exit code: $?"
```
- 出力: `{CAT}/jma_osaka2018.csv`、`{CAT}/21_20a_osaka2018_catalog.json`、`/content/drive/MyDrive/ARGUS/PDF/21_20a_osaka2018_catalog.pdf`
- 確かめること(この出力を貼る):
  - `selftest: … 全て合格`
  - `本震: 2018-06-18 07:58:xx JST …  (想定の 1 分 07:58:00〜07:59:00 JST の中か: True …)`。Mj ≥ 6.0・深さ 5–20 km・緯度 34.65–35.05・経度 135.35–135.85 でなければ止まる。
  - 箱が「緯度 0.30° × 経度 0.35°」、期間が本震の 2 日前〜24 日後。
  - `数:` の `test_candidates_1p5_to_2p0_after_72h` が 30 以上なら「次へ進める」。30 未満なら STOP(exit 1)→ ここで止めて INCONCLUSIVE を報告する(事前登録 5.1 節)。
- h2018.zip が取れない時(STOP の表示): 気象庁のページからブラウザで取り、Drive に置いて `--hypo <パス>` で渡す。
- 所要: 数分(ファイルの取得と読み込み)。

### セル 6 — 21_20b: 取る計画だけ(--dry-run)
```python
!python {SRC}/21_20b_osaka2018_hinet_to_h5.py --ref-h5 "{REF_H5}" --dry-run; echo "exit code: $?"
```
- 出力: `{DRV}/data/21_20b_plan.json`
- 確かめること: `参照の z-score の確認 … PASS`、`fs` が 100、候補局 60(本震から何 km〜何 km か)、区切りの数と分の合計、置き場所の見込み。
- 所要の見込み: 区切りの数 × 1 区切りの時間(21_04b の冒頭: Hi-net は 1 回の準備に 10〜60 s)。
  参考: 2016 は 654 区切り(21_04 の変更の記録 02)で、10〜60 s/区切りなら 1.8〜10.9 時間にあたる(2016 の実際の所要は記録に無い)。

### セル 7 — 煙試験(本震の区間に掛かる区切りを先に 3 つ)
```python
!python {SRC}/21_20b_osaka2018_hinet_to_h5.py --ref-h5 "{REF_H5}" --max-blocks 3; echo "exit code: $?"
```
- 確かめること: 3 区切りとも `局 … 窓 …` が出る。1 回の要求を短くして取れた時は `1 回の要求を N 分にして取れた` と出る(v1.1 と同じ動き)。
- 1 区切りの秒数を記録して、全体の時間を見積もる(区切りの数 × 1 区切りの秒数)。

### セル 7b — 煙試験の分だけで組み立ててゲートを見る
```python
!python {SRC}/21_20b_osaka2018_hinet_to_h5.py --ref-h5 "{REF_H5}" --assemble --partial; echo "exit code: $?"
```
- 出力: `{DRV}/data/waves/osaka2018_100Hz_partial.h5`(小さい)、`{DRV}/data/21_20b_report_partial.json`、`{DRV}/PDF/21_20b_mainshock_partial.pdf`
- 確かめること: G-ref・G-dup が PASS、G-clock(本震)の値。`21_20b_mainshock_partial.pdf` で、本震の P が予想の P の印にそろっているかを目で見る。
- G-clock の FAIL はこの段階では記録だけ(事前登録 表 1 の 7)。G-ref・G-dup の FAIL は止めて相談。

### セル 8 — 全ての区切りを取る(止まっても同じセルで続きから)
```python
!python {SRC}/21_20b_osaka2018_hinet_to_h5.py --ref-h5 "{REF_H5}"; echo "exit code: $?"
```
- 最後の行が `終わり: 残りの区切り 0/N` になるまで、同じセルを回し直す。何時間もかかりうる(下の所要の表)。
- 3 つ続けて取れない区切りがあると STOP する(Hi-net の状態を見てから回し直す)。
- 何度回しても取れない区切りだけが残り、取れた割合が 0.98 以上なら、セル 9 に `--allow-missing` を付けてよい(事前に決めた規則)。0.98 未満なら止める。

### セル 8b — Colab が切れた直後だけ(アカウントの局の選択を元に戻す)
```python
!python {SRC}/21_20b_osaka2018_hinet_to_h5.py --ref-h5 "{REF_H5}" --restore-selection --break-lock; echo "exit code: $?"
```
- その後、セル 8 をもう一度。

### セル 9 — 組み立てとゲート(Colab のローカルで)
```python
!mkdir -p {LO}/data
!cp -r {DRV}/data/blocks {LO}/data/ && cp {DRV}/data/21_20b_plan.json {LO}/data/
!python {SRC}/21_20b_osaka2018_hinet_to_h5.py --ref-h5 "{REF_H5}" --assemble --out {LO}; echo "exit code: $?"
# 何度回しても取れない区切りだけが残り、取れた割合 ≥ 0.98 の時だけ、上の行の --out {LO} の後に --allow-missing を付ける
!mkdir -p {DRV}/data/catalog {DRV}/PDF && cp {LO}/data/21_20b_report.json {DRV}/data/ && cp {LO}/PDF/21_20b_*.pdf {DRV}/PDF/
!cp {LO}/data/catalog/stations_osaka2018.csv* {DRV}/data/catalog/
!ls -la {LO}/data/waves {LO}/data/catalog
```
- 期待(全て通った時): `{LO}/data/waves/osaka2018_100Hz.h5` と `{LO}/data/catalog/stations_osaka2018.csv`。
- 表示の読み方(事前登録 5.2 節):
  - `STOP(G-clock だけ)` → 進む(exit code は 1 でよい)。`osaka2018_100Hz_FAILED.h5` と `stations_osaka2018.csv.part` を セル 10・11 に渡す(下のセル 10 が自分で選ぶ)。
  - `STOP(G-ref …)`・`STOP(G-dup …)`・`STOP(G-cover …)` など、G-clock 以外を含む STOP → 止めて、この出力を貼る。
  - G-cover は 0.95 以上で PASS、0.80〜0.95 は注意(進む)、0.80 未満は STOP。
  - G-spec は記録だけ(3 倍以上違えば注意の表示。止めない)。
- `21_20b_report.json` は書き換えない(G-clock の FAIL もそのまま残す)。報告の `version` は `v1 (=21_04b v1.1)`。

---

## 2 部 Colab: キャッシュと時刻の確かめ(セル 10〜15)

### セル 10 — 21_20c の煙試験(10 地震)
```python
import json, os
S = json.load(open(f'{CAT}/21_20a_osaka2018_catalog.json')); BOX = ' '.join(str(x) for x in S['box']); print('box', BOX)
H5 = f'{LO}/data/waves/osaka2018_100Hz.h5'
STA = f'{LO}/data/catalog/stations_osaka2018.csv'
if not os.path.exists(H5):            # G-clock だけの FAIL の時(事前登録 5.2 節)
    H5, STA = f'{LO}/data/waves/osaka2018_100Hz_FAILED.h5', STA + '.part'
print(H5, os.path.exists(H5)); print(STA, os.path.exists(STA))
!python {SRC}/21_20c_osaka2018_realpick_cache_colab.py --h5 {H5} --jma {CAT}/jma_osaka2018.csv --stations {STA} --min-mag 1.5 --box {BOX} --base {LO} --tag _osaka2018_smoke --max-events 10; echo "exit code: $?"
```
- 期待: `PhaseNet ('original') 読込完了`、`対象イベント: 10 (M>=1.5, box=[…]` の box が 21_20a の JSON と同じ、`観測点: N局 (stations_osaka2018.csv)`
  (G-clock だけの FAIL の時は `stations_osaka2018.csv.part`)、`完了: …tottori_parsed_realpick_osaka2018_smoke.pt`。
- 所要: このセルの時間 × (Mj ≥ 1.5 の地震の数 / 10) が セル 11 の見積もり(21_04 の時の 15_01c の所要は今回の入力に記録が無い)。

### セル 11 — 21_20c の本番
```python
!python {SRC}/21_20c_osaka2018_realpick_cache_colab.py --h5 {H5} --jma {CAT}/jma_osaka2018.csv --stations {STA} --min-mag 1.5 --box {BOX} --base {LO} --tag _osaka2018_m15; echo "exit code: $?"
```
- 出力: `{LO}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt`、`{LO}/models/locator/15_01c_build_report_osaka2018_m15.json`、`{LO}/PDF/15_01c_tottori_picks_qc_osaka2018_m15.pdf`
  (名前の `tottori_`・`15_01c_` は 21_04 と同じ形にそろえるため残してある)
- 確かめること(参考の値は 2016 の 21_04 の変更の記録 03。判定ではない): 採用の数 / 対象、P fallback 率(2016 は 1.2%)、
  和達の傾きの中央値(理論 0.73。2016 は 0.696)、S−P と距離の傾き(理論 0.1224 s/km。2016 は 0.0918 s/km・r = 0.779)。
- 報告の JSON の `script_sha256` が事前登録の 8 節の 21_20c の値と同じこと。

### セル 11b — キャッシュをすぐ Drive に写す(切れた時に作り直さないため)
```python
!mkdir -p {DRV}/data/tottori_processed {DRV}/models/locator
!cp {LO}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt {DRV}/data/tottori_processed/
!cp {LO}/models/locator/15_01c_build_report_osaka2018_m15.json {DRV}/models/locator/
```
- セル 14 でもう一度写す(同じファイルを上書きするだけ)。参考: 2016 のキャッシュは 2,991.6 MB だった(変更の記録 03)。

### セル 12 — 21_20d: G-clock2(時刻の確かめ)
```python
!python {SRC}/21_20d_osaka2018_gclock2_picks.py --base {LO} --ref-cache {REF_CACHE_2026}; echo "exit code: $?"
```
- 出力: `{LO}/data/21_20d_gclock2.json`、`{LO}/PDF/21_20d_gclock2.pdf`
- 扱いは**事前登録 5.3 節の案 C で決まっている**(その場で決めることは何も無い)。どの条件で FAIL しても 21_20d は exit code 1 で終わるが、
  ここでは止めずに セル 13・13b に進み、13b の表示で決める。
- 21_20d が `STOP:`(検測 100 未満・日・局・時間のどれかが 0・報告が無い)で終わった時は、判定できないので止める(JSON は書かれない)。
- `--ref-cache` の「参考(鳥取 2026)」の行は判定に使わない。

### セル 13 — 21_20e(必ず回す。読むだけの記述)
```python
!python {SRC}/21_20e_osaka2018_station_pick_diagnose.py --base {LO} --ref-cache {REF_CACHE_2026}; echo "exit code: $?"
```
- 出力: `{LO}/data/21_20e_station_picks.csv`、`{LO}/PDF/21_20e_station_picks.pdf`。結果で規則・局・キャッシュを変えない。

### セル 13b — 案 C の判定に要る値を表示する(読むだけ。事前登録 5.3 節をそのまま当てる)
```python
import json, csv
J = json.load(open(f'{LO}/data/21_20d_gclock2.json'))
for k in ['pass_all', 'pass_day', 'pass_station', 'pass_hour', 'pass_events', 'pass_measured_frac', 'gclock2_pass']: print(k, J[k])
for x in J['gclock_events']:
    print('  (e)', x['origin_jst'], 'Mj', x['mj'], 'found_dt_s', round(x['found_dt_s'], 3), 'n_picks', x['n_picks'], 'PASS' if x['pass_'] else 'FAIL')
rows = list(csv.DictReader(open(f'{LO}/data/21_20e_station_picks.csv')))
near = [r for r in rows if float(r['epi_from_mainshock_km']) <= 80.0 and int(r['n']) >= 20]
bad_near = [r for r in near if abs(float(r['dev_s'])) > 1.0]
bad_far = [r for r in rows if float(r['epi_from_mainshock_km']) > 80.0 and int(r['n']) >= 20 and abs(float(r['dev_s'])) > 1.0]
print('(c-near) 80 km 以内・n ≥ 20 の局', len(near), '  |dev_s| > 1.0 s の局', len(bad_near))
for r in bad_near: print('   ', r['station'], r['epi_from_mainshock_km'], 'km  n', r['n'], ' dev_s', r['dev_s'])
print('(c-far) 80 km より遠い・n ≥ 20 で |dev_s| > 1.0 s の局', len(bad_far))
for r in bad_far: print('   ', r['station'], r['epi_from_mainshock_km'], 'km  n', r['n'], ' dev_s', r['dev_s'])
```
- 読み方(事前登録 5.3 節。ここで新しく決めることは無い):
  - `pass_all`・`pass_day`・`pass_hour`・`pass_events`・`pass_measured_frac` のどれかが False → 止める。21_20・21_20f は回さない。
    「clock could not be verified」と報告する。(e) が FAIL なら、FAIL の地震の `found_dt_s`(1.5 s より大きい = キャッシュに無い)と `n_picks`(4 未満)を書く。
  - (c-near) の |dev_s| > 1.0 s の局が 1 つでもある → 止める(同じ報告)。80 km 以内・n ≥ 20 の局が 0 の時の扱いは事前登録 5.3 節の 4 の最後の行に従う。
  - `pass_station` が False で、上の 2 つに当たらない → 進む。21_20・21_20f の全ての結果に、5.3 節の決まった印を付ける。
  - `gclock2_pass` が True → 進む(印は付けない)。
- この出力・セル 12 と 13 の出力を全部貼る。

### セル 14 — Drive へ保存と SHA-256
```python
!mkdir -p {DRV}/data/tottori_processed {DRV}/models/locator {DRV}/PDF
!cp {LO}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt {DRV}/data/tottori_processed/
!cp {LO}/models/locator/15_01c_build_report_osaka2018_m15.json {DRV}/models/locator/
!cp {LO}/data/21_20d_gclock2.json {LO}/data/21_20e_station_picks.csv {DRV}/data/ ; cp {LO}/PDF/*.pdf {DRV}/PDF/
!sha256sum {LO}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt
```
- この SHA-256 を控える。Mac に置いた後の SHA-256 と、21_20 の本番が `models/21_20_opened.json` に書く `cache_sha256` が同じこと。
- 大きい h5 は Drive に置かない(ローカルの h5 はランタイムを閉じると消える。区切りのファイルが Drive に残るので、作り直せる)。

### セル 15 — Drive に書けたかの確かめ(書きかけのまま Mac に持って行かないため)
```python
from google.colab import drive
drive.flush_and_unmount()
drive.mount('/content/drive')
!sha256sum {LO}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt {DRV}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt
```
- 期待: 2 行の SHA-256 が同じで、セル 14 の値とも同じ。違えば セル 14 と 15 をもう一度。

---

## Colab が切れた時(どのセルから回し直すか)

切れると `/content` の中(Colab のローカルの h5・キャッシュ・win32tools・環境変数・変数)は消える。Drive の中は残る。
ランタイムのタイプは CPU・ハイメモリのまま。どの場合も、まず **セル 1 → 2 → 3 → 4** を回し直す(セル 2 の `REF_H5` の行も)。その後:

| 切れた所 | 次に回すもの |
|---|---|
| セル 5〜7b の途中 | 切れたセルからもう一度(出力は Drive にある) |
| セル 8 の途中 | セル 8b → セル 8(続きから取る。取った区切りは Drive に残る) |
| セル 9 の途中・後(セル 11 の前) | セル 9 → セル 10 → セル 11 |
| セル 11 の途中 | セル 9 → セル 10 → セル 11(キャッシュを作り直したことと、両方の回のまとめの数を記録に残す。2016 の変更の記録 03 と同じ扱い) |
| セル 11b の後・セル 15 の前 | 下の「Drive から戻す」→ 切れたセルから(セル 12・13・13b・14・15) |

Drive から戻す(セル 11b の後に切れた時。セル 10 の変数は要らない):
```python
!mkdir -p {LO}/data/tottori_processed {LO}/models/locator {LO}/PDF
!cp {DRV}/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt {LO}/data/tottori_processed/
!cp {DRV}/models/locator/15_01c_build_report_osaka2018_m15.json {LO}/models/locator/
!cp {DRV}/data/21_20b_report.json {LO}/data/
```
- 21_20d は `{LO}/data/21_20b_report.json` を読むので、最後の行が要る。

---

## 3 部 Mac(本人が回す。~/SWIFT、uv の環境 = 21_06a で学習した環境)

21_20f は scikit-learn と numpy の版が学習時(scikit-learn 1.8.0・numpy 2.4.3・Python 3.12.12。models/21_06a_train.json)と同じでないと止まる。
Colab では回さない。

### M1 — 置く
- キャッシュの置き場所を作る:
```bash
mkdir -p ~/SWIFT/data/osaka2018_processed
```
- Drive の `ARGUS_osaka2018/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt` を Mac に持って来る。どちらか:
  - ブラウザ: drive.google.com → マイドライブ → ARGUS_osaka2018 → data → tottori_processed → ファイルを右クリック → ダウンロード。
    大きいファイルは確かめの画面が出ることがある(そのままダウンロード)。終わったら:
```bash
mv ~/Downloads/tottori_parsed_realpick_osaka2018_m15.pt ~/SWIFT/data/osaka2018_processed/
```
  - Drive for desktop: Finder の「Google Drive → マイドライブ → ARGUS_osaka2018 → data → tottori_processed」から
    `~/SWIFT/data/osaka2018_processed/` にコピーする(コピーが終わるまで待つ)。
- 確かめ:
```bash
cd ~/SWIFT && shasum -a 256 data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt src/21_20_osaka2018_similarity_confirmation.py src/21_20f_osaka2018_learned_test.py models/21_06_ranker.pkl models/21_06a_train.json data/21_06a_train_rows.npz
ls models/21_20_* models/21_20f_* data/21_20_* data/21_20f_* 2>/dev/null   # 何も無いこと(残っていると本番が _rerun になる)
shasum -a 256 src/22_04_osaka2018_gate_test.py models/22_gate.pkl   # 22_00 の 7 節の値
ls models/22_04_* data/22_04_* PDF/22_04_* 2>/dev/null                # 何も無いこと
```
- 期待: キャッシュは セル 14・15 の値、2 本のスクリプトは事前登録の 8 節の値、凍結したモデル・学習の記録・学習の行は 8 節の「前提として既に凍結したもの」の値。

### M1b — 環境の版の確かめ(M2 の前)
```bash
cd ~/SWIFT && uv run python -c "import sklearn, numpy, sys; print(sklearn.__version__, numpy.__version__, sys.version)"
```
- 期待: `1.8.0 2.4.3 3.12.12 …`(models/21_06a_train.json の `sklearn`・`numpy`・`python`)。違えば M2 に進まない(21_20f が G-model で止まる)。

### M2 — 21_20 の dev(試験を開かない)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/21_20_osaka2018_similarity_confirmation.py --dev; echo "exit code: $?"
```
- 確かめること: `G-untouched … PASS`、`分け方 … G-split PASS`、`G-causal … PASS`、`G-phys … PASS`、`判定 … DEV (no verdict)`。
- G-phys が FAIL なら本番は開かない(事前登録 6 節)。
- dev の値を見て規則を変えない。1 地震あたりの時間 × 試験の地震の数で本番の時間を見積もる
  (参考: 21_04 の本番は試験 307 地震で 1,564 s。models/21_04_judgment.json の runtime_s)。

### M2b — 22_04 の dev(試験を開かない。21_20 の dev の後)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/22_04_osaka2018_gate_test.py --dev; echo "exit code: $?"
```
- 確かめること: `写した部分の SHA-256 … G-leak PASS`、`凍結した G … 同じ`、`照合の準備は全て通った`、`G-same … PASS`、
  `判定: INCONCLUSIVE(dev: 試験ではない …)`。dev は 1 回だけの記録を書かない。

### M3 — 21_20 の本番(1 回だけ)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/21_20_osaka2018_similarity_confirmation.py; echo "exit code: $?"
```
- 出力: `models/21_20_judgment.json`・`models/21_20_opened.json`・`data/21_20_per_event.csv`・`PDF/21_20_F1_error_vs_tau.pdf`・`PDF/21_20_F2_paired_difference.pdf`・`PDF/21_20_F3_similarity_vs_separation.pdf`
- 最初の行の `本スクリプト v1 SHA-256 …` と最後の `判定(事前宣言、H1): …` を含め、出力を全部貼る。
- Mac が眠った・電源が落ちた・Ctrl-C で途切れた時(事前登録 6 節): `models/21_20_opened.json` に `opened` だけがあるか `stopped: … KeyboardInterrupt` なら、
  同じスクリプト・同じキャッシュ(SHA-256 が同じ)で同じコマンドを 1 回だけ回し直してよい。その出力(`_rerun_<UTC>` の名前)を登録した本番の結果とし、
  途切れたことを報告に書く。スクリプトが自分で STOP・例外で止まった時は回し直さない(「開いた後に止まった」として報告する)。

### M4 — 21_20f の dev
```bash
cd ~/SWIFT && caffeinate -i uv run python src/21_20f_osaka2018_learned_test.py --dev; echo "exit code: $?"
```
- 確かめること: `G-feat PASS  G-model PASS`、`G-same … PASS`、`DEV (no verdict)`。

### M5 — 21_20f の本番(1 回だけ。21_20 の本番の後)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/21_20f_osaka2018_learned_test.py; echo "exit code: $?"
```
- 出力: `models/21_20f_judgment.json`・`models/21_20f_opened.json`・`data/21_20f_per_event.csv`・`PDF/21_20f_F1_learned_test.pdf`
- 参考の所要: 21_06b の本番は試験 307 地震で 506 s。
- 途切れた時は M3 と同じ。正式な結果は `models/21_20f_opened.json` で最初に completed になった実行だけ(事前登録 6 節)。

### M5b — 22_04 の本番(1 回だけ。21_20 の本番の後。21_20f とは関わらない)
```bash
cd ~/SWIFT && caffeinate -i uv run python src/22_04_osaka2018_gate_test.py; echo "exit code: $?"
```
- 21_20 の正式な結果が、機械的に途切れた後の 1 回のやり直し(`_rerun_<UTC>`)の時だけ、最後に `--ref-suffix _rerun_<UTC>` を付ける(22_00 の 3 節)。
- 確かめること: `21_20 の正式な結果 … G の凍結 … < 21_20 を開いた時刻 …`、`G-same … PASS`、`→ 判定: …`。
- 出力: `models/22_04_judgment.json`・`models/22_04_opened.json`・`data/22_04_per_event.csv`・`PDF/22_04_F1_gate_osaka.pdf`。出力を全部貼る。
- 21_20 が「評価できる地震 30 未満」で INCONCLUSIVE に終わった時は、22_04 は開かずに INCONCLUSIVE を書いて終わる(それでよい)。
- 途切れた時の扱いは M3 と同じ(22_00 の 3 節)。正式な結果は `models/22_04_opened.json` で最初に completed になった実行だけ。

### M6 — 記録
- Colab の報告を Drive から Mac に持って来る(M1 と同じやり方で、`~/Downloads/osaka_reports/` に置く):
  `ARGUS/data/catalog/21_20a_osaka2018_catalog.json`、`ARGUS_osaka2018/data/21_20b_report.json`、
  `ARGUS_osaka2018/models/locator/15_01c_build_report_osaka2018_m15.json`、`ARGUS_osaka2018/data/21_20d_gclock2.json`、
  `ARGUS_osaka2018/data/21_20e_station_picks.csv`、`ARGUS_osaka2018/PDF/` の PDF。
```bash
mkdir -p ~/ARGUS_prereg_21_04/results_21_20 ~/ARGUS_prereg_21_04/results_21_20f ~/ARGUS_prereg_21_04/results_22_04
cp ~/Downloads/osaka_reports/* ~/ARGUS_prereg_21_04/results_21_20/
cd ~/SWIFT
cp models/21_20_judgment.json models/21_20_opened.json data/21_20_per_event.csv PDF/21_20_F1_error_vs_tau.pdf PDF/21_20_F2_paired_difference.pdf PDF/21_20_F3_similarity_vs_separation.pdf ~/ARGUS_prereg_21_04/results_21_20/
cp models/21_20f_judgment.json models/21_20f_opened.json data/21_20f_per_event.csv PDF/21_20f_F1_learned_test.pdf ~/ARGUS_prereg_21_04/results_21_20f/
cp models/22_04_judgment.json models/22_04_opened.json ~/ARGUS_prereg_21_04/results_22_04/; cp data/22_04_per_event.csv PDF/22_04_F1_gate_osaka.pdf ~/ARGUS_prereg_21_04/results_22_04/ 2>/dev/null
ls models/21_20*_rerun_* data/21_20*_rerun_* PDF/21_20*_rerun_* models/22_04*_rerun_* data/22_04*_rerun_* PDF/22_04*_rerun_* 2>/dev/null   # 出たら、それぞれの results_ に写す
cd ~/ARGUS_prereg_21_04
git add results_21_20 results_21_20f results_22_04
git commit -m "21_20 and 22_04: results (Northern Osaka 2018)"
git push
```
- 止めた時(セル 5 の INCONCLUSIVE・セル 13b で止める・G-phys で止める)も、そこまでの報告を同じように commit・push する。
- 事前登録の 7 節のすその印を、2 つの CSV から 7 節の式で計算して記述として書く。下は 7 節の式をそのまま書いたもの(凍結するスクリプトではない):
```bash
cd ~/SWIFT && uv run python - <<'EOF'
import json, csv
J = json.load(open('models/21_20_judgment.json')); JF = json.load(open('models/21_20f_judgment.json'))
R = list(csv.DictReader(open('data/21_20_per_event.csv'))); RF = list(csv.DictReader(open('data/21_20f_per_event.csv')))
N, NF = J['n_evaluated'], JF['n_evaluated']
print('N', N, 'rows', len(R), '| NF', NF, 'rows', len(RF))
def tail(rows, col, thr, n):
    v = [x[col] for x in rows]; k = sum(1 for s in v if s != '' and float(s) > thr); e = sum(1 for s in v if s == '')
    print(f'  {col:>14s}  > {thr:4.1f} km: {k} / {n} = {k / n:.3f}   空の欄 {e}')
for t in ['0.5', '1', '2', '3']:
    B = J['per_tau'][t]['C3']['best']; print(f'tau {t} s  BEST = {B}')
    for col in [f'{B}_err_t{t}', f'C3_err_t{t}', f'C4_err_t{t}']: tail(R, col, 10.0, N)
    tail(RF, f'L4_t{t}', 10.0, NF)
B2 = J['per_tau']['2']['C3']['best']; print(f'30 km, tau 2 s  BEST = {B2}')
for col in [f'{B2}_err_t2', 'M6r_err_t2', 'C4_err_t2']: tail(R, col, 30.0, N)
tail(RF, 'L4_t2', 30.0, NF)
EOF
```
- `N` と `rows`(CSV の行の数)が同じこと。`_rerun_` が正式な結果の時は、ファイル名をその名前に替える。
- (c-far) で進んだ時は、決まった印を 21_20・21_20f の全ての結果に付ける(事前登録 5.3 節)。

---

## 所要の見積もり(全体)

**今夜はセル 8(Hi-net の取得)を始めるまで**: 0-A・0-B → セル 1・2・(2b)→ 0-C〜0-E(push・外部の記録)→ セル 3〜7b → セル 8 を始める。
セル 8 は何時間もかかりうるので、始めたら置いておき、切れたら セル 1〜4 → 8b → 8 で続ける。

| 段階 | 見積もりの根拠 | 値 |
|---|---|---|
| 0 部(Mac の置き・確かめ・push・外部の記録) | 記録が無い | 回して確かめる |
| セル 2b(任意) | 2026 のキャッシュを読む時間。記録が無い | 回して確かめる |
| セル 5(21_20a) | ファイル 1 つの取得と読み込み | 数分 |
| セル 6〜8(21_20b の取得) | 区切りの数(セル 6 が表示)× 1 区切り 10〜60 s(21_04b の冒頭)。セル 7 で実測して見積もり直す | 大阪の区切りの数はセル 6 まで分からない(2016 は 654 区切りで、1.8〜10.9 時間にあたる。2016 の実際の所要は記録に無い) |
| セル 9(組み立て) | 記録が入力に無い | セル 9 の表示で確かめる |
| セル 10〜11(21_20c) | セル 10 の時間 × 地震の数 / 10 | セル 10 の後に見積もる |
| セル 11b・14・15(Drive へ写す・確かめ) | キャッシュの大きさ(2016 は 2,991.6 MB。変更の記録 03)。時間の記録は無い | 回して確かめる |
| M1(Drive → Mac) | 同じ大きさのダウンロード。時間の記録は無い | 回して確かめる |
| M2〜M3(21_20) | dev の時間で見積もる。参考: 21_04 は試験 307 地震で 1,564 s | 試験の地震の数による |
| M4〜M5(21_20f) | 参考: 21_06b は試験 307 地震で 506 s | 試験の地震の数による |
