# 25_04y — G-clock2 (d) の作り直しの 2 回目の dev(続いた K 地震ごと。これまでの系列のキャッシュだけを読む)

1 回目(25_04x の局ごとの窓)は、4 系列の全てで、時計が正常なはずの元のキャッシュで不合格になったので捨てる。
2 回目は、元の (d) の考え方(全ての局をまとめて、波形の組み立ての時刻の誤りを見る)に戻し、「1 時間」の代わりに
「時刻の順で続いた K 個の地震」でまとめる。K の選び方は、スクリプトの冒頭に回す前に決めて書いてある。
島根県西部 2018 のデータは一つも読まない。位置の計算も、どの方法の誤差も出さない。

## 置く場所
- `25_04y_gclock2_event_block_dev.py` を Drive の `ARGUS/src/` に置く。
- 25_04x を回したノートの続きでよい(GPU は要らない。ランタイムは既定でよい)。新しいノートの時は、先に 25_04x の X1 を回す。

## Y1 — SHA-256 とキャッシュの確かめ
```python
import hashlib, os
SRC = '/content/drive/MyDrive/ARGUS/src'
p = f'{SRC}/25_04y_gclock2_event_block_dev.py'
h = hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else 'MISSING'
print('OK ' if h == '8c7f891c42dc391d1db5d68b0711333763f5ee3ae3dc086c98bc9ef0e9b39ec9' else 'NG ', '25_04y', h[:12])
C = {
  'nagano2014':  '/content/drive/MyDrive/ARGUS_nagano2014/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt',
  'tottori2026': '/content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt',
  'osaka2018':   '/content/drive/MyDrive/ARGUS_osaka2018_a04/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt',
  'ct2016':      '/content/drive/MyDrive/ARGUS_ct2016/data/tottori_processed/tottori_parsed_realpick_ct2016_m15.pt',
}
for k, v in C.items(): print('ある ' if os.path.exists(v) else '無い ', k)
```
- 期待: `OK` と、`ある` が 4 行。

## Y2 — dev を回す
```python
import shlex
args = ' '.join(shlex.quote(f'--cache={k}={v}') for k, v in C.items())
!python {SRC}/25_04y_gclock2_event_block_dev.py {args} --out /content/drive/MyDrive/ARGUS/data/25_04y > /content/25_04y_log.txt 2>&1; echo "exit code: $?"
!cat /content/25_04y_log.txt
```
- 4 系列で数分。
- 貼るもの: Y1 の出力・Y2 の出力の全て・`ARGUS/data/25_04y/25_04y_gclock2_event_block_dev.pdf`。
- `exit code: 1`(条件を満たす K が無い)の時も、そのまま貼る。

## 読み方
- 最後の「選んだ K」が、事前登録 25 で使う K。2・3・4 のうち、次を全て満たす最小のもの:
  (i) 4 系列の元のキャッシュで全て合格、
  (ii) 1 地震の全局に ±1・±3・±10 s のどれかを足した時に不合格になる割合が、6 つのどれでも 0.01 以下、
  (iii) 続いた 4 地震の全局 +0.6 s を見つける割合が 0.95 以上。
- 窓の値は「地震ごとの中央値の中央値」。K=2 は 2 つの中央値の平均になるので、±3 s の 1 地震で必ず不合格になり、(ii) を満たさないのは作りどおり。
- 「まとめた中央値」「続いた 1・2・3・4 地震」「窓の長さ」は記述で、判定には使わない(事前登録 25 で開示する)。
