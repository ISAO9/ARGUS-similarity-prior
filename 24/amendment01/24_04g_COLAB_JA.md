# 24_04g — G-clock2 (d) で外れた時間の診断(読むだけ・試験は開かない)

このスクリプトは事前登録 24 の凍結の束には入っていない(凍結の後に作った、読むだけの記述)。
位置の計算もどの方法の誤差も出さない。気象庁の震源は Mj・深さ・本震からの距離だけを表示し、緯度・経度は表示も保存もしない。

**N15 から先は回さない**(この診断の後、A か 追記 01 かを決めるまで)。

## 置く場所
- `24_04g_nagano2014_clock_hour_diagnose.py` を Drive の `ARGUS/src/` に置く。
- 名前が `…(1).py` になった時は、古い方を消してから名前を直す(G2 で確かめる)。
- pip は要らない(Colab に入っている numpy・torch・matplotlib だけを使う)。
- 新しいランタイムでよい(N1〜N4 は要らない)。

## G1 — Drive をつなぐ
```python
from google.colab import drive; drive.mount('/content/drive')
```

## G2 — SHA-256 と入力の確かめ
```python
import hashlib, os, glob
SRC = '/content/drive/MyDrive/ARGUS/src'
CAT = '/content/drive/MyDrive/ARGUS/data/catalog'
DRV = '/content/drive/MyDrive/ARGUS_nagano2014'
EXP = {
    '24_04g_nagano2014_clock_hour_diagnose.py': 'dc3a8a922063a67819cfd511d9aec597e3deca5590b21ac3265ba14c1caa604f',
    '24_01_nagano2014_jma_catalog.py':          'a4fb5d9a41c694663d65cf5a6f124d97f024360f1d9a40b43c0bf1fc1a6812a6',
}
for k, v in EXP.items():
    p = f'{SRC}/{k}'
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else 'MISSING'
    print('OK ' if h == v else 'NG ', k, h[:12])
print('(1) などの写し:', [os.path.basename(x) for x in glob.glob(f'{SRC}/24_04g*') + glob.glob(f'{SRC}/24_01*') if '(' in x] or 'なし')
for p in [f'{DRV}/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt',
          f'{DRV}/data/24_04d_gclock2.json',
          f'{CAT}/jma_nagano2014.csv',
          f'{CAT}/jma_raw/h2014.zip']:
    print('ある ' if os.path.exists(p) else '無い ', p)
```
- 2 行とも `OK` で、4 つとも `ある` なら G3 へ。
- `24_04d_gclock2.json` が `無い` 時は、N14c(Drive への写し)がまだなので、N14c を先に回す
  (ランタイムが切れて `/content/ARGUS_nagano2014` も消えている時は、出力を貼って知らせる)。
- `h2014.zip` だけが `無い` 時は G3 の `--hypo` の行を消して回してよい(日本全体の震源一覧の照合だけを飛ばす)。

## G3 — 診断を回す
```python
!python {SRC}/24_04g_nagano2014_clock_hour_diagnose.py --base {DRV} --catalog {CAT}/jma_nagano2014.csv --hypo {CAT}/jma_raw/h2014.zip --src24-01 {SRC}/24_01_nagano2014_jma_catalog.py > /content/24_04g_log.txt 2>&1; echo "exit code: $?"
!cat /content/24_04g_log.txt
```
- 出力は長いので、一度ファイルに書いてから表示する(途中で切れないように)。
- 貼るもの: G2 の出力・G3 の出力の全て・`ARGUS_nagano2014/PDF/24_04g_clock_hour_diagnose.pdf`。
- できる物: `ARGUS_nagano2014/data/24_04g_clock_hour_diagnose.json`・`ARGUS_nagano2014/PDF/24_04g_clock_hour_diagnose.pdf`
  (24_04d などの既存のファイルは書き換えない)。
- 最後が `STOP` の時も、そこまでの出力をそのまま貼る。

## 出力の見方(作りもののデータでの例。値は配管の確かめで、本物の見込みではない)
作りもののキャッシュで 1 つの地震の P を全ての局で +0.67 s ずらし(発生時刻の食い違いのまね)、24_04d を回し直してから回した:

| 見る量 | 作りものの値 | 意味 |
|---|---|---|
| ずれ(その地震の残りの中央値 − 全体) | +0.664 s | (d) で外れた量 |
| 残り − その局の中央値: 中央値・四分位幅 | +0.663 s・0.072 s | 全ての局が同じだけずれた(幅が小さい) |
| 距離の傾き | +0.0047 s/km | 距離で変わらない(別の場所の地震を拾ったのではない) |
| S−P の全期間との差 | +0.028 s | 発生時刻に左右されない量は正常 |
| 同じ局の前後 6 時間 | +0.004 s | 時計なら前後も同じだけずれるはず → ずれていない |
| 60 s 前〜30 s 後の別の地震 | 箱の中 0・日本全体 0 | 重なった地震は無い |

この形なら「時計ではなく、その 1 地震の発生時刻の食い違い」に合う。
四分位幅が大きい時は検測の取り違え、前後 6 時間も同じだけずれる時は時計、近くに別の地震がある時は重なりを疑う。
