# 25_04v — G-clock2 (d) の 4 回目(最後)の dev(本震 + 72 h より後の続いた 5 地震・陽性対照 +1.0 s)

25_04z で、K = 5 は (i) 元のキャッシュと (ii) 陰性対照を 4 系列とも満たし、(iii) 陽性対照 +0.6 s だけを満たさなかった。
2026-11-17 に決めたとおり、K = 5 に決め、陽性対照の大きさを +1.0 s にして確かめる(合格の幅 0.5 s と陰性対照は変えない)。
島根県西部 2018 のデータは一つも読まない。位置の計算も、どの方法の誤差も出さない。

## 置く場所
- `25_04v_gclock2_k5_dev.py` を Drive の `ARGUS/src/` に置く。
- 25_04z を回したノートの続きでよい(GPU は要らない)。新しいノートの時は、先に 25_04x の X1(Drive をつなぐ)を回す。

## V1 — SHA-256 とキャッシュの確かめ
```python
import hashlib, os
SRC = '/content/drive/MyDrive/ARGUS/src'
p = f'{SRC}/25_04v_gclock2_k5_dev.py'
h = hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else 'MISSING'
print('OK ' if h == '6330e5dc6da580ff37efc266110caa7fdbf90e1af6c197fcbb61e4d7e80d21dc' else 'NG ', '25_04v', h[:12])
C = {
  'nagano2014':  '/content/drive/MyDrive/ARGUS_nagano2014/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt',
  'tottori2026': '/content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt',
  'osaka2018':   '/content/drive/MyDrive/ARGUS_osaka2018_a04/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt',
  'ct2016':      '/content/drive/MyDrive/ARGUS_ct2016/data/tottori_processed/tottori_parsed_realpick_ct2016_m15.pt',
}
for k, v in C.items(): print('ある ' if os.path.exists(v) else '無い ', k)
```
- 期待: `OK` と、`ある` が 4 行。

## V2 — dev を回す
```python
import shlex
args = ' '.join(shlex.quote(f'--cache={k}={v}') for k, v in C.items())
!python {SRC}/25_04v_gclock2_k5_dev.py {args} --out /content/drive/MyDrive/ARGUS/data/25_04v > /content/25_04v_log.txt 2>&1; echo "exit code: $?"
!cat /content/25_04v_log.txt
```
- 4 系列で数分。
- 貼るもの: V1 の出力・V2 の出力の全て・`ARGUS/data/25_04v/25_04v_gclock2_k5_dev.pdf`。

## 読み方
- `exit code: 0` と「判定: 合格。K = 5 を事前登録 25 で凍結する」→ 事前登録 25 の束の作成に進む。
- `exit code: 1` と「不合格」→ (d) の作り直しはここでやめ、出力を貼る(次の進め方を相談する)。
- 「続いた 4 地震の大きさごと」(+0.6・+0.8・+1.0 s)と「続いた 1・2・3・4 地震」は記述で、判定には使わない(事前登録 25 で開示する)。
