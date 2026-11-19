# 25_04x — 新しい G-clock2 (d)(局ごとの時計の確かめ)の dev(これまでの系列のキャッシュだけを読む)

島根県西部 2018 のデータは一つも読みません。位置の計算も、どの方法の誤差も出しません。
読むのは、既に試験を終えた(または止めた)系列のキャッシュの P の時刻・距離・局・発生時刻だけです。

## 置く場所
- `25_04x_gclock2_station_window_dev.py` を Drive の `ARGUS/src/` に置く。
- 新しい空のノートで回す(ランタイムは既定でよい。pip は要らない)。

## X1 — Drive をつなぐ
```python
from google.colab import drive; drive.mount('/content/drive')
```

## X2 — SHA-256 と、キャッシュがあるかの確かめ
```python
import hashlib, os
SRC = '/content/drive/MyDrive/ARGUS/src'
p = f'{SRC}/25_04x_gclock2_station_window_dev.py'
h = hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else 'MISSING'
print('OK ' if h == '9c9bf27e82131052dee7bf746cf91a0203d050801efb4b989e8a2bfb2a91918b' else 'NG ', '25_04x', h[:12])
C = {
  'nagano2014':  '/content/drive/MyDrive/ARGUS_nagano2014/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt',
  'tottori2026': '/content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt',
  'osaka2018':   '/content/drive/MyDrive/ARGUS_osaka2018/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt',
  'ct2016':      '/content/drive/MyDrive/ARGUS_ct2016/data/tottori_processed/tottori_parsed_realpick_ct2016_m15.pt',
}
for k, v in C.items(): print('ある ' if os.path.exists(v) else '無い ', k, v)
```
- 期待: `OK`。キャッシュは、長野 2014(R1 の後)・鳥取県西部 2026・大阪 2018(変更の記録 04 の後)・鳥取県中部 2016 の 4 つ。
- `無い` が出たものは、Drive の実際の場所を探して `C` の行を直す(見つからなければそのままでよい。スクリプトが飛ばす)。

## X3 — dev を回す
```python
import shlex
args = ' '.join(shlex.quote(f'--cache={k}={v}') for k, v in C.items())
!python {SRC}/25_04x_gclock2_station_window_dev.py {args} --out /content/drive/MyDrive/ARGUS/data/25_04x > /content/25_04x_log.txt 2>&1; echo "exit code: $?"
!cat /content/25_04x_log.txt
```
- 1 系列あたり数分かかる(陽性対照で、全ての局・全ての始まりに時計のずれを入れて計算するため)。
- 貼るもの: X2 の出力・X3 の出力の全て・`ARGUS/data/25_04x/25_04x_gclock2_station_window_dev.pdf`。
- `exit code: 1` で最後に「期待と違う系列」と出た時も、そのまま貼る(凍結の前に作りを見直す)。

## 読み方(期待)
- 各系列で、新しい (d) は PASS(時計が正常なはずの系列で、誤って FAIL しない)。
  長野 2014 は、元の (d) が FAIL で、新しい (d) は PASS になるはず(24_04g の診断どおりなら)。
- 陽性対照(判定する全ての局・続いた 12 検測の全ての始まりに時計のずれを入れる): 見つけた割合が +0.6 s・+1.0 s でほぼ 1、+0.3 s でほぼ 0。
- 陰性対照(1 地震の全局・遠い半分に +1.0 s): PASS。
- どれかが期待と違えば、事前登録 25 で凍結する前に作りを見直す(dev なので、ここで直してよい)。
