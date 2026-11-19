# 25_04z — G-clock2 (d) の作り直しの 3 回目の dev(本震 + 72 h より後の続いた K 地震。これまでの系列のキャッシュだけを読む)

2 回目(25_04y)は、4 系列の全てで、本震から十数時間以内の続いた地震のまとまった外れで不合格になったので捨てる。
3 回目は、見る地震を、試験の候補を取る期間(本震 + 72 h より後)に限り、K を 3・4・5 から選ぶ。K の選び方はスクリプトの冒頭に、回す前に決めて書いてある。
島根県西部 2018 のデータは一つも読まない。位置の計算も、どの方法の誤差も出さない。

## 置く場所
- `25_04z_gclock2_test_period_block_dev.py` を Drive の `ARGUS/src/` に置く。
- 25_04y を回したノートの続きでよい(GPU は要らない)。新しいノートの時は、先に 25_04x の X1(Drive をつなぐ)を回す。

## Z1 — SHA-256 とキャッシュの確かめ
```python
import hashlib, os
SRC = '/content/drive/MyDrive/ARGUS/src'
p = f'{SRC}/25_04z_gclock2_test_period_block_dev.py'
h = hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else 'MISSING'
print('OK ' if h == 'df02f1607e4227d64466a66853f8fd3cd5b0262c17b9ca168a0445d70ed55488' else 'NG ', '25_04z', h[:12])
C = {
  'nagano2014':  '/content/drive/MyDrive/ARGUS_nagano2014/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt',
  'tottori2026': '/content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt',
  'osaka2018':   '/content/drive/MyDrive/ARGUS_osaka2018_a04/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt',
  'ct2016':      '/content/drive/MyDrive/ARGUS_ct2016/data/tottori_processed/tottori_parsed_realpick_ct2016_m15.pt',
}
for k, v in C.items(): print('ある ' if os.path.exists(v) else '無い ', k)
```
- 期待: `OK` と、`ある` が 4 行。

## Z2 — dev を回す
```python
import shlex
args = ' '.join(shlex.quote(f'--cache={k}={v}') for k, v in C.items())
!python {SRC}/25_04z_gclock2_test_period_block_dev.py {args} --out /content/drive/MyDrive/ARGUS/data/25_04z > /content/25_04z_log.txt 2>&1; echo "exit code: $?"
!cat /content/25_04z_log.txt
```
- 4 系列で数分。
- 貼るもの: Z1 の出力・Z2 の出力の全て・`ARGUS/data/25_04z/25_04z_gclock2_test_period_block_dev.pdf`。
- `exit code: 1`(条件を満たす K が無い)の時も、そのまま貼る。

## 読み方
- 各系列の最初に、本震(キャッシュで Mj 最大)の日時と、見る地震(本震 + 72 h より後)の数が出る。本震が想定と違えば知らせる。
- 「記述 外れた地震」は全ての期間の外れた 10 地震と本震からの時間。25_04y で外れた窓が本震直後だったことの確かめ(判定には使わない)。
- 最後の「選んだ K」が、事前登録 25 で使う K。3・4・5 のうち、次を全て満たす最小のもの:
  (i) 4 系列の元のキャッシュで全て合格、
  (ii) 1 地震の全局に ±1・±3・±10 s のどれかを足した時に不合格になる割合が、6 つのどれでも 0.01 以下、
  (iii) 続いた 4 地震の全局 +0.6 s を見つける割合が 0.95 以上。
