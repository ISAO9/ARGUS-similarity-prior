# DIFF_LOG — 21_20(大阪府北部 2018)のスクリプトと、元のスクリプトの差分

- 作った日: 2026-11-01(UTC)。直した日: 2026-11-02(UTC。21_20b・21_20c の注釈と表示だけ。下の「2026-11-02 の直し」)。元のスクリプトは `prereg/` の版(事前登録の記録の SHA-256 と全桁で同じことを確かめた。`src/src/` の Colab の写しも同じ SHA-256 で、新しい版は無かった)。
- 作り方: 元のファイルに、決まった文字列の置き換えだけを当てた(置き換えごとに、当たる回数を確かめ、違えば止める道具で作った)。手で書き直したのは冒頭の説明と、各節に書いた所だけ。
- 各スクリプトの節: 変えたことと理由 → 全ての差分(`diff -u`)。

## SHA-256

| 元 | SHA-256 | 新 | SHA-256 |
|---|---|---|---|
| 21_04a_ct2016_jma_catalog.py | `312e4c7d1292c1aac16352ccc7dd903ec5be979a1c360cdd3e57a9d65e767ae1` | 21_20a_osaka2018_jma_catalog.py | `cad845a14375014056b7da2a539b750d88363be56620904381fd520db16d25d2` |
| 21_04b_ct2016_hinet_to_h5.py | `81d69a13ddb3d432a93055e1657b9763b8634910777f004b6767d15788e952c0` | 21_20b_osaka2018_hinet_to_h5.py | `43154e7a3b33451d6a2526f4a1b3ff4a8e6085964c380398ceab49b50745e06e` |
| 15_01c_tottori_realpick_cache_colab.py | `e407f88b7345e689f0c989d2c95ecf2e1bfec1b857e09b4ab8ada44f2354258e` | 21_20c_osaka2018_realpick_cache_colab.py | `7b938b944003d99fcad7df188792e8e8eb95c71b07f1a1223bffad6671d04cf0` |
| 21_04d_ct2016_gclock2_picks.py | `bc37a3c63e1b60cb7806498527caf7371f2ee8846555141a719592d5d2557de4` | 21_20d_osaka2018_gclock2_picks.py | `606d0eea2f76a8607c7844f83a93056759640974bce7f11ccfe690ecb6e7c1d6` |
| 21_04e_ct2016_station_pick_diagnose.py | `2eca1779642deb3c8ea4433649862e73697b9b4f3d7deced7fae78a1392a9406` | 21_20e_osaka2018_station_pick_diagnose.py | `680e8825d49e00bba58cca9045c66ee7b213f05bc5a231d0810d041b4fefba92` |
| 21_04_ct2016_similarity_confirmation.py | `0b2807843763b641a67e090407311d39c0204cdb7825577c6b86b07a0532908d` | 21_20_osaka2018_similarity_confirmation.py | `2c0fb375e6a1a8d48d3ffbc611bb189b2390d224488cdd5585c76f5cadd5da43` |
| 21_06b_ct2016_learned_test.py | `442c411945f288cfff7f14490ee9826ffcfe055e5a79cc2af0c39fe93cb5bfea` | 21_20f_osaka2018_learned_test.py | `9623695ea33bef90605cd47d4fb8fceb16a8bbbe91327bfa51783aa347d29925` |

## 21_20a_osaka2018_jma_catalog.py(元: 21_04a_ct2016_jma_catalog.py)

変わった行: −77 / +86(冒頭の説明を含む)

### 変えたことと理由
- 冒頭の説明を大阪府北部 2018 用に書き直した(派生元・変更点・要確認の項目を書いた)。
- `URL`: h2016.zip → h2018.zip(**要確認**: 同じ場所にあること)。`--hypo` の既定のファイル名も h2018.zip。
- 本震の規則: `MAIN_JST`(2016-10-21 14:07:22.57)と `MAIN_TOL_S = 5.0` を外し、`MAIN_DATE_JST = 2018-06-18` と
  `MAIN_WIN_JST = [07:58:00, 07:59:00)` にした。理由: 秒までの発生時刻を、震源ファイルを開く前には確かめていない(数字を作らない)。
  気象庁の発表の「7 時 58 分」の 1 分だけを条件にし、外れたら STOP する(要確認の項目として表示)。
- `MAIN_MIN_MJ`: 6.4 → 6.0(下流の 21_20・21_20f の G-untouched と本震の確かめが Mj ≥ 6.0 を使うため、カタログの段階で同じ値で止める)。
- `MAIN_LAT`・`MAIN_LON`: 鳥取県中部の範囲 → 34.65–35.05・135.35–135.85(21_04a と同じ幅 0.4° × 0.5°)。深さ 5–20 km は同じ。
- 本震の表示の文(「想定 14:07:22.57 との差」→「想定の 1 分の中か」)。
- 出力の名前(jma_osaka2018.csv・21_20a_osaka2018_catalog.json・PDF/21_20a_osaka2018_catalog.pdf)、JSON の `script`、表示の [21_20a]、
  図の軸の文(本震の時刻を JSON の値から書く)と題(Northern Osaka 2018)。
- 新しい止め方: 最後に、試験の候補が `MIN_TEST = 30`(21_04 の値と同じ)未満なら STOP(exit 1)。出力の CSV・JSON・図は止める前に書く。
  理由: 評価できる試験の地震は候補より多くならないので、30 未満なら 21_04 と同じ規則で INCONCLUSIVE が決まる。何時間もの取得を省く。
- 変えていないもの: 読み方(列の位置・Fw.d・マグニチュード)、読み方の試験(作りものの 2016 年のレコードのまま。年には依らない)、除外、箱、
  期間、数え方、CSV の書き方。

### 全ての差分

```diff
--- prereg/21_04a_ct2016_jma_catalog.py
+++ osaka/21_20a_osaka2018_jma_catalog.py
@@ -2,47 +2,46 @@
 # =============================================================================
-# Script : 21_04a_ct2016_jma_catalog.py  (v1)
-#          [鳥取県中部 2016(本震 2016-10-21 14:07 JST、M6.6)の気象庁の震源を、21_02 と同じ形の CSV にする]
-# Project: ARGUS(新生)— 2 つ目の余震系列での確認(21_04)の入力の 1 つ目
+# Script : 21_20a_osaka2018_jma_catalog.py  (v1)
+#          [大阪府北部 2018(本震 2018-06-18 朝、日本時間 7 時 58 分台)の気象庁の震源を、21_02・21_04 と同じ形の CSV にする]
+# Project: ARGUS(新生)— 3 つ目の余震系列での確認(21_20)の入力の 1 つ目
+# 派生元 : 21_04a_ct2016_jma_catalog.py v1(SHA-256 312e4c7d1292c1aac16352ccc7dd903ec5be979a1c360cdd3e57a9d65e767ae1)。
+#          読み方・除外・箱・期間・数え方・CSV の書き方は 21_04a と 1 字も変えていない。変えたのは次だけ(DIFF_LOG.md):
+#          (1) 震源ファイル h2016.zip → h2018.zip
+#          (2) 本震の規則: 21_04a は「資料名から分かる発生時刻 ± 5 s」だったが、大阪府北部 2018 の秒までの発生時刻は、
+#              この震源ファイルを開く前には確かめていないので、ここには書かない。代わりに、気象庁の発表の
+#              「2018-06-18 07 時 58 分」の 1 分間 [07:58:00, 07:59:00) JST に入ること、を本震の条件にする
+#              (要確認: 震源ファイルを開いた後、表示の本震の時刻がこの 1 分に入ることを確かめる。入らなければ STOP する)。
+#              Mj ≥ 6.0(21_20 の G-untouched と本震の確かめが Mj ≥ 6.0 を使うので、それに合わせる。21_04a は 6.4)、
+#              深さ 5–20 km(21_04a と同じ)、緯度 34.65–35.05・経度 135.35–135.85(21_04a と同じ幅 0.4° × 0.5°)
+#          (3) 出力の名前(jma_osaka2018.csv・21_20a_osaka2018_catalog.json・PDF/21_20a_osaka2018_catalog.pdf)、表示、図の題
+#          (4) 最後に、試験の候補(本震 + 72 時間より後の 1.5 ≤ Mj < 2.0)が 30 未満なら STOP(exit 1)する。評価できる試験の
+#              地震は候補より多くならないので、30 未満なら 21_04 と同じ規則で INCONCLUSIVE が決まる。波形を取る前に止めて、
+#              そのまま報告する(事前登録 21_20 の「波形を取る前の止め方」)。出力の CSV・JSON・図は止める前に書く。
+#          読み方の試験(selftest)は 21_04a と同じ作りものの 2016 年のレコードのまま(読み方だけを試す。年には依らない)。
 #
 # 何をするか:
-#   1. 気象庁の震源ファイル h2016.zip(地震ごとに 96 バイトの震源レコード 1 行、時刻は日本時間)を
-#      https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2016.zip から data/catalog/jma_raw/ に取る
-#      (登録不要。既にあれば取らない。--hypo で手元のファイルを指定してもよい)。
-#   2. 震源レコードを列の位置どおりに読む(書式: https://www.data.jma.go.jp/eqev/data/bulletin/data/format/hypfmt_e.html)。
-#      読み方は KRITES の 02_jma_arrivals.py(気象庁の書式と照合済み)の震源レコードの部分と同じ列。
-#        1 列 = 機関(J だけ使う。U・I は他機関) / 2–5 年 / 6–7 月 / 8–9 日 / 10–11 時 / 12–13 分 / 14–17 秒(F4.2)
-#        22–24 緯度の度 / 25–28 緯度の分(F4.2) / 33–36 経度の度 / 37–40 経度の分(F4.2) / 45–49 深さ(F5.2 km)
-#        53–54 マグニチュード 1(F2.1、負は "-1"〜"-9" = −0.1〜−0.9、"A0"〜"A9" = −1.0〜−1.9、"B0" = −2.x、"C0" = −3.x)
-#        55 その種類 / 60 震源の精度 / 61 補助情報 / 96 震源決定の印(K・S・k・s = 手動、A・a = 自動、N = 決まらない・
-#        採らない・固定、F = 遠方)
-#      Fw.d の欄は小数点が省かれている。空白は 0 として読む(気象庁の書式では、深さを固定した震源などで小数の部分が空白)。
-#   3. 本震を決める(事前に決めた規則): 2016-10-21 の J の震源のうち Mj が最大の地震。発生時刻が 14:07:22.57 JST
-#      (気象庁の震源過程の資料の名前 2016102114072257 による)から 5 秒以内、Mj ≥ 6.4、深さ 5–20 km、
-#      緯度 35.2–35.6・経度 133.6–134.1 の中、でなければ STOP(読み方の誤りか別のファイル)。
-#   4. 範囲(事前に決めた規則。21_02 の西鳥取の箱と同じ大きさ):
-#      - 箱 = 本震の緯度 ± 0.15°、経度 ± 0.175°(西鳥取の箱は 35.15–35.45 × 133.00–133.35 = 0.30° × 0.35°)
-#      - 期間 = 本震の 2 日前から 24 日後(日本時間。21_02 の鳥取 2026 は本震の約 1.4 日前〜約 23.9 日後)
-#      - 使う震源: 機関 J、精度が M(マッチドフィルタ)・8(決まらない)・9(最寄りの局で固定)でない、
-#        補助情報が 3(人工)・5(低周波)でない、震源決定の印が N(決まらない・採らない・固定)・F(遠方)でない、
-#        緯度・経度・Mj・深さが空白でない。印ごとの数を JSON に書く(手動と自動の混ざり方を記録するため)
-#   5. 出力: data/catalog/jma_ct2016.csv(列 time, latitude, longitude, depth_km, mag と、記録用の det_flag。time は日本時間の
-#      "YYYY-MM-DD HH:MM:SS.ff"。jma_tottori_2026.csv と同じ列と書き方で、15_01c がそのまま読める。15_01c は先頭 21 文字
-#      だけを読むので、発生時刻は 0.1 s 単位に切り捨てられる。2026 の CSV でも同じで、21_02 は地震ごとに走時の残りの
-#      中央値を引くので、この切り捨ては震源の誤差に効かない)と
-#      data/catalog/21_04a_ct2016_catalog.json(本震・箱・期間・数・除いた数。15_01c と 21_04b に渡す箱はここから読む)。
-#      数: 全体、Mj ≥ 1.5、Mj ≥ 2.0、pool(本震 + 72 時間まで)、試験の候補(本震 + 72 時間より後の 1.5 ≤ Mj < 2.0)、
-#      本震 + 72 時間より後の Mj ≥ 2.0(21_02 と同じく過去の地震の一覧にだけ入る)。
-#      試験の候補は「キャッシュで P が測れた地震」の前の数なので、本当の試験の数はこれより少なくなる。
-#   6. 図: PDF/21_04a_ct2016_catalog.pdf(時刻と Mj、Mj の頻度。白背景・英語・凡例は枠の外)。
+#   1. 気象庁の震源ファイル h2018.zip(地震ごとに 96 バイトの震源レコード 1 行、時刻は日本時間)を
+#      https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2018.zip から data/catalog/jma_raw/ に取る
+#      (登録不要のはず。既にあれば取らない。--hypo で手元のファイルを指定してもよい)。
+#      要確認: h2018.zip がこの場所にあること(21_04a の h2016.zip と同じ場所の決まりから作った URL。このスクリプトを書いた
+#      時点では取りに行っていない)。取れなければ STOP するので、気象庁のページからブラウザで取って --hypo で渡す。
+#   2. 震源レコードを列の位置どおりに読む(21_04a と同じ。書式: https://www.data.jma.go.jp/eqev/data/bulletin/data/format/hypfmt_e.html)。
+#   3. 本震(上の (2) の規則): 2018-06-18 の J の震源のうち Mj が最大の地震。発生時刻が [07:58:00, 07:59:00) JST、Mj ≥ 6.0、
+#      深さ 5–20 km、緯度 34.65–35.05・経度 135.35–135.85、でなければ STOP。本震が除く印を持つ時も STOP。
+#   4. 範囲(21_04a と同じ規則): 箱 = 本震の緯度 ± 0.15°、経度 ± 0.175°。期間 = 本震の 2 日前から 24 日後(日本時間)。
+#      使う震源・除外・印ごとの数の記録は 21_04a と同じ。
+#   5. 出力: data/catalog/jma_osaka2018.csv(列は 21_04a と同じ。15_01c・21_20c がそのまま読める)と
+#      data/catalog/21_20a_osaka2018_catalog.json(本震・箱・期間・数・除いた数。21_20b と 21_20c に渡す箱はここから読む)。
+#   6. 図: PDF/21_20a_osaka2018_catalog.pdf(白背景・英語・凡例は枠の外)。
+#   7. 試験の候補が 30 未満なら STOP(上の (4))。
 #
-# 止める条件(STOP): 読み方の試験に失敗・ファイルが取れない・zip の中にファイルが無い・レコードが 96 バイトでない行が 1% を
-#   超える・2016-10-21 の震源が無い・本震の規則に合わない・本震が除く印を持つ・箱の中で期間内の Mj ≥ 1.5 が 0。
-# 限界: 正解も過去の地震も気象庁の震源(21_02 と同じ)。h2016 は確定値で、21_02 の jma_tottori_2026.csv(2026 年の一元化
-#   震源)とは確定の段階が違いうる。低周波・人工・マッチドフィルタ・決まらない震源は除いた(2026 の CSV でそれを除いたかは
-#   記録が無い。この除外は 2016 だけ)。手動と自動の震源が混ざる(印ごとの数を JSON に記録)。
+# 止める条件(STOP): 21_04a と同じもの(読み方の試験・ファイル・96 バイト・本震の日の震源が無い・本震の規則・本震の印・
+#   Mj ≥ 1.5 が 0)と、試験の候補が 30 未満。
+# 限界: 正解も過去の地震も気象庁の震源。h2018 の確定の段階(確定値か)は要確認(21_04a の h2016 は確定値)。
+#   除外(低周波・人工・マッチドフィルタ・決まらない震源)は 21_04a と同じ。手動と自動の震源が混ざる(印ごとの数を JSON に記録)。
+#   箱は本震の周りの決まった大きさで、余震でない地震(背景の地震活動)も入る(21_02・21_04 と同じ)。
 #
-# Usage : (Colab、ノート 21_04_ct2016_colab.ipynb の セル 5)
-#         !python /content/drive/MyDrive/ARGUS/src/21_04a_ct2016_jma_catalog.py
-#         (手元で: cd ~/SWIFT && uv run python src/21_04a_ct2016_jma_catalog.py --selftest)
-# Output: data/catalog/jma_ct2016.csv / data/catalog/21_04a_ct2016_catalog.json / PDF/21_04a_ct2016_catalog.pdf
+# Usage : (Colab、ノート 21_20_osaka2018_colab.ipynb の セル 5)
+#         !python /content/drive/MyDrive/ARGUS/src/21_20a_osaka2018_jma_catalog.py
+#         (読み方の試験だけ: !python .../21_20a_osaka2018_jma_catalog.py --selftest)
+# Output: data/catalog/jma_osaka2018.csv / data/catalog/21_20a_osaka2018_catalog.json / PDF/21_20a_osaka2018_catalog.pdf
 # =============================================================================
@@ -65,8 +64,12 @@
 ROOT = Path(__file__).resolve().parent.parent
-URL = "https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2016.zip"
+URL = "https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2018.zip"   # 要確認: この場所にあること(21_04a の URL の年だけを変えた)
 REC_LEN = 96
-MAIN_JST = datetime(2016, 10, 21, 14, 7, 22, 570000)    # 気象庁の震源過程の資料名 2016102114072257
-MAIN_TOL_S, MAIN_MIN_MJ, MAIN_DEPTH = 5.0, 6.4, (5.0, 20.0)
-MAIN_LAT, MAIN_LON = (35.2, 35.6), (133.6, 134.1)
-HALF_LAT, HALF_LON = 0.15, 0.175                         # 西鳥取の箱(0.30° × 0.35°)と同じ大きさ
+# 本震の規則(21_20): 秒までの発生時刻は震源ファイルを開く前には確かめていないので書かない。気象庁の発表の「7 時 58 分」の 1 分間だけを
+# 条件にする(要確認: 震源ファイルの本震がこの 1 分に入ること。入らなければ STOP。数字を直す時は版を上げて事前登録の記録に書く)
+MAIN_DATE_JST = datetime(2018, 6, 18).date()
+MAIN_WIN_JST = (datetime(2018, 6, 18, 7, 58, 0), datetime(2018, 6, 18, 7, 59, 0))   # [始まり, 終わり)。要確認
+MAIN_MIN_MJ, MAIN_DEPTH = 6.0, (5.0, 20.0)               # Mj ≥ 6.0 は 21_20 の G-untouched・本震の確かめと同じ値
+MAIN_LAT, MAIN_LON = (34.65, 35.05), (135.35, 135.85)    # 21_04a と同じ幅(0.4° × 0.5°)。要確認: 本震がこの中にあること
+MIN_TEST = 30                                            # 21_04 の MIN_TEST と同じ(評価できる試験の地震が 30 未満なら INCONCLUSIVE)
+HALF_LAT, HALF_LON = 0.15, 0.175                         # 西鳥取の箱(0.30° × 0.35°)と同じ大きさ(21_04a と同じ)
 DAYS_BEFORE, DAYS_AFTER = 2.0, 24.0
@@ -168,3 +171,3 @@
     def check(c, msg):
-        if not c: sys.exit(f"[21_04a] STOP: 読み方の試験に失敗: {msg}")
+        if not c: sys.exit(f"[21_20a] STOP: 読み方の試験に失敗: {msg}")
     def put(buf, a, b, s):
@@ -193,3 +196,3 @@
     check(t == datetime(2016, 10, 21, 14, 7, 5, 0), 't == datetime(2016, 10, 21, 14, 7, 5, 0)')  # 15_01c は先頭 21 文字だけ読むので 0.1 s 単位に切り捨てる(2026 も同じ)
-    print("[21_04a] selftest: 震源レコードの読み方の試験に全て合格")
+    print("[21_20a] selftest: 震源レコードの読み方の試験に全て合格(21_04a と同じ試験)")
 
@@ -198,3 +201,3 @@
     ap = argparse.ArgumentParser()
-    ap.add_argument("--hypo", default="", help="手元の h2016.zip か展開したファイル(無ければ取る)")
+    ap.add_argument("--hypo", default="", help="手元の h2018.zip か展開したファイル(無ければ取る)")
     ap.add_argument("--selftest", action="store_true")
@@ -206,5 +209,5 @@
     for d in (CAT, RAWD, PDFD): d.mkdir(parents=True, exist_ok=True)
-    src = Path(a.hypo) if a.hypo else RAWD / "h2016.zip"
+    src = Path(a.hypo) if a.hypo else RAWD / "h2018.zip"
     if not src.exists():
-        print(f"[21_04a] 取得: {URL}")
+        print(f"[21_20a] 取得: {URL}")
         req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (ARGUS research)"})
@@ -214,3 +217,3 @@
         except Exception as e:
-            sys.exit(f"[21_04a] STOP: {URL} が取れない({e})。ブラウザで取って --hypo で指定する")
+            sys.exit(f"[21_20a] STOP: {URL} が取れない({e})。ブラウザで取って --hypo で指定する")
         src.write_bytes(data)
@@ -220,3 +223,3 @@
             mem = [m for m in z.namelist() if not m.endswith("/")]
-            if not mem: sys.exit("[21_04a] STOP: zip の中にファイルが無い")
+            if not mem: sys.exit("[21_20a] STOP: zip の中にファイルが無い")
             raw = b"\n".join(z.read(m) for m in mem)
@@ -225,21 +228,21 @@
     recs, n_bad = read_records(raw)
-    print(f"[21_04a] 震源ファイル {src.name}(SHA-256 {sha[:12]}…、中身 {mem})  レコード {len(recs)}  96 バイトでない行 {n_bad}")
-    if not recs or n_bad > 0.01 * len(recs): sys.exit("[21_04a] STOP: 96 バイトのレコードの形でない(別のファイルの可能性)")
+    print(f"[21_20a] 震源ファイル {src.name}(SHA-256 {sha[:12]}…、中身 {mem})  レコード {len(recs)}  96 バイトでない行 {n_bad}")
+    if not recs or n_bad > 0.01 * len(recs): sys.exit("[21_20a] STOP: 96 バイトのレコードの形でない(別のファイルの可能性)")
     H = [parse_hypo(r) for r in recs]
     J = [h for h in H if h["agency"] == "J" and h["origin_jst"] is not None]
-    print(f"[21_04a] 機関 J の震源 {len(J)}(他機関 {sum(1 for h in H if h['agency'] != 'J')}、時刻が読めない {sum(1 for h in H if h['origin_jst'] is None)})")
+    print(f"[21_20a] 機関 J の震源 {len(J)}(他機関 {sum(1 for h in H if h['agency'] != 'J')}、時刻が読めない {sum(1 for h in H if h['origin_jst'] is None)})")
 
     # ---- 本震(事前に決めた規則)
-    day = [h for h in J if h["origin_jst"].date() == MAIN_JST.date() and h["mag"] is not None]
-    if not day: sys.exit("[21_04a] STOP: 2016-10-21 の震源が無い")
+    day = [h for h in J if h["origin_jst"].date() == MAIN_DATE_JST and h["mag"] is not None]
+    if not day: sys.exit(f"[21_20a] STOP: {MAIN_DATE_JST} の震源が無い")
     m = max(day, key=lambda h: h["mag"])
-    dt_s = abs((m["origin_jst"] - MAIN_JST).total_seconds())
-    print(f"[21_04a] 本震: {m['origin_jst']} JST  {m['lat']:.4f}N {m['lon']:.4f}E  深さ {m['depth_km']} km  M{m['mag']}{m['mag_type']}  "
-          f"精度 {m['precision']}  (想定 14:07:22.57 との差 {dt_s:.2f} s)")
-    ok = (dt_s <= MAIN_TOL_S and m["mag"] >= MAIN_MIN_MJ and m["depth_km"] is not None
+    in_win = MAIN_WIN_JST[0] <= m["origin_jst"] < MAIN_WIN_JST[1]
+    print(f"[21_20a] 本震: {m['origin_jst']} JST  {m['lat']:.4f}N {m['lon']:.4f}E  深さ {m['depth_km']} km  M{m['mag']}{m['mag_type']}  "
+          f"精度 {m['precision']}  (想定の 1 分 {MAIN_WIN_JST[0]:%H:%M:%S}〜{MAIN_WIN_JST[1]:%H:%M:%S} JST の中か: {in_win}。要確認の項目)")
+    ok = (in_win and m["mag"] >= MAIN_MIN_MJ and m["depth_km"] is not None
           and MAIN_DEPTH[0] <= m["depth_km"] <= MAIN_DEPTH[1] and MAIN_LAT[0] <= m["lat"] <= MAIN_LAT[1]
           and MAIN_LON[0] <= m["lon"] <= MAIN_LON[1])
-    if not ok: sys.exit("[21_04a] STOP: 本震が規則に合わない(読み方の誤りか別のファイル。この行を貼って相談)")
+    if not ok: sys.exit("[21_20a] STOP: 本震が規則に合わない(読み方の誤りか別のファイル。この行を貼って相談)")
     if m["det_flag"] in BAD_DETFLAG or m["precision"] in BAD_PRECISION:
-        sys.exit(f"[21_04a] STOP: 本震の震源が除く印(精度 {m['precision']}・震源決定の印 {m['det_flag']})を持つ(この行を貼って相談)")
+        sys.exit(f"[21_20a] STOP: 本震の震源が除く印(精度 {m['precision']}・震源決定の印 {m['det_flag']})を持つ(この行を貼って相談)")
     box = [round(m["lat"] - HALF_LAT, 4), round(m["lat"] + HALF_LAT, 4), round(m["lon"] - HALF_LON, 4), round(m["lon"] + HALF_LON, 4)]
@@ -267,4 +270,4 @@
              library_only_mj_ge_2p0_after_72h=int(((mags >= FRESH_MAX_MAG - 1e-9) & after).sum()))
-    if n["mj_ge_1p5"] == 0: sys.exit("[21_04a] STOP: 箱の中・期間内の Mj ≥ 1.5 が 0")
-    out_csv = CAT / "jma_ct2016.csv"
+    if n["mj_ge_1p5"] == 0: sys.exit("[21_20a] STOP: 箱の中・期間内の Mj ≥ 1.5 が 0")
+    out_csv = CAT / "jma_osaka2018.csv"
     with open(out_csv, "w", newline="") as f:
@@ -277,3 +280,3 @@
     flags_15 = dict(Counter(h["det_flag"] or "_" for h in rows if h["mag"] >= MIN_MAG - 1e-9))
-    summ = dict(script="21_04a_ct2016_jma_catalog.py", version=VERSION, source=URL, source_file=src.name, source_sha256=sha,
+    summ = dict(script="21_20a_osaka2018_jma_catalog.py", version=VERSION, source=URL, source_file=src.name, source_sha256=sha,
                 mainshock=dict(origin_jst=fmt_time(m["origin_jst"]), lat=m["lat"], lon=m["lon"], depth_km=m["depth_km"], mj=m["mag"],
@@ -286,8 +289,8 @@
                 note="test candidates are before picking; the evaluated test set is those with a measured P in the cache")
-    json.dump(summ, open(CAT / "21_04a_ct2016_catalog.json", "w"), indent=1, ensure_ascii=False)
-    print(f"[21_04a] 箱 {box}(緯度 0.30° × 経度 0.35°)  期間 {fmt_time(t0)} 〜 {fmt_time(t1)} JST  pool の切れ目 {fmt_time(cut)} JST")
-    print(f"[21_04a] 除いた数: {ex}")
-    print(f"[21_04a] 数: {n}")
-    print(f"[21_04a] 震源決定の印の数(K・S・k・s = 手動、A・a = 自動。_ は空白): 全体 {flags_all}  Mj ≥ 1.5 {flags_15}")
-    print(f"[21_04a] 出力: {out_csv.relative_to(ROOT)}, data/catalog/21_04a_ct2016_catalog.json")
+    json.dump(summ, open(CAT / "21_20a_osaka2018_catalog.json", "w"), indent=1, ensure_ascii=False)
+    print(f"[21_20a] 箱 {box}(緯度 0.30° × 経度 0.35°)  期間 {fmt_time(t0)} 〜 {fmt_time(t1)} JST  pool の切れ目 {fmt_time(cut)} JST")
+    print(f"[21_20a] 除いた数: {ex}")
+    print(f"[21_20a] 数: {n}")
+    print(f"[21_20a] 震源決定の印の数(K・S・k・s = 手動、A・a = 自動。_ は空白): 全体 {flags_all}  Mj ≥ 1.5 {flags_15}")
+    print(f"[21_20a] 出力: {out_csv.relative_to(ROOT)}, data/catalog/21_20a_osaka2018_catalog.json")
 
@@ -305,4 +308,4 @@
     ax1.axvline(POOL_H / 24, color="k", lw=0.8, ls="--")
-    ax1.set_xlabel("Days since mainshock (2016-10-21 14:07 JST)"); ax1.set_ylabel("JMA magnitude Mj")
-    ax1.set_title("Central Tottori 2016, JMA hypocentres in the box", fontsize=10); ax1.grid(alpha=0.3)
+    ax1.set_xlabel(f"Days since mainshock ({m['origin_jst']:%Y-%m-%d %H:%M} JST)"); ax1.set_ylabel("JMA magnitude Mj")
+    ax1.set_title("Northern Osaka 2018, JMA hypocentres in the box", fontsize=10); ax1.grid(alpha=0.3)
     bins = np.arange(np.floor(mags.min() * 10) / 10, mags.max() + 0.2, 0.1)
@@ -313,4 +316,10 @@
     fig.legend(h_, l_, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=9, frameon=False, markerscale=3)
-    fig.tight_layout(); fig.savefig(PDFD / "21_04a_ct2016_catalog.pdf", bbox_inches="tight"); plt.close(fig)
-    print("[21_04a] 図: PDF/21_04a_ct2016_catalog.pdf")
+    fig.tight_layout(); fig.savefig(PDFD / "21_20a_osaka2018_catalog.pdf", bbox_inches="tight"); plt.close(fig)
+    print("[21_20a] 図: PDF/21_20a_osaka2018_catalog.pdf")
+    # 21_20: 試験の候補が 30 未満なら、評価できる試験の地震も 30 未満になることが確定する(INCONCLUSIVE)。波形を取る前に止める
+    nt = n["test_candidates_1p5_to_2p0_after_72h"]
+    if nt < MIN_TEST:
+        sys.exit(f"[21_20a] STOP: 試験の候補(本震 + 72 時間より後の 1.5 ≤ Mj < 2.0)が {nt}(< {MIN_TEST})。評価できる試験の地震は"
+                 f"これより多くならないので、21_04 と同じ規則で INCONCLUSIVE。波形は取らずに、この出力を事前登録 21_20 の規則どおり報告する")
+    print(f"[21_20a] 試験の候補 {nt} ≥ {MIN_TEST}: 次へ進める(本当の試験の数は、キャッシュで P を測れた地震だけなので、これより少ない)")
 
```

## 21_20b_osaka2018_hinet_to_h5.py(元: 21_04b_ct2016_hinet_to_h5.py)

変わった行: −93 / +105(冒頭の説明を含む)

### 変えたことと理由
- 冒頭: 系列と名前を変え、派生元の節を足した。処理の説明は 21_04b v1.1 のまま(G-clock だけの FAIL の扱いを 1 行足した)。
- `VERSION`: "v1.1" → "v1 (=21_04b v1.1)"(この系列の 1 版目。取り方は 21_04b v1.1 と同じ。h5 の属性・報告の `version`・計画の JSON・表示に入る)。
- 名前だけの置き換え(計算は同じ): 既定の `--catalog`・`--summary`(21_20a の出力)、既定の `--out`(ARGUS_osaka2018)、h5 の名前
  (osaka2018_100Hz.h5・_partial・_FAILED)、局の表(stations_osaka2018.csv)、data/21_20b_plan.json・21_20b_initial_selection.json・
  21_20b.lock・21_20b_report.json、PDF/21_20b_coverage.pdf・21_20b_mainshock.pdf、表示の [21_20b]、h5 の属性の名前
  `ct2016_source` → `osaka2018_source`(15_01c・21_20c はこの属性を読まない)。
- ゲートで止まった時の表示の文: G-clock だけの FAIL の時は、事前登録 21_20 の扱い(記録だけ。_FAILED の h5 と .csv.part を セル 10 に渡す)を
  表示する。止まり方(exit・h5 を _FAILED にする・局の表を .part のまま残す)は v1.1 と同じ。
- 変えていないもの: 取り方(要求の長さを 60 → 20 → 10 → 5 分と短くして取り直す v1.1 の動きを含む)、区切りの作り方、z-score、
  欠測の扱い、局の選び方、組み立て、全てのゲートと閾値。作りものの入力で `plan_blocks`・`zscore_windows`・`covers` が 21_04b v1.1 と
  同じ結果になることを確かめた(下の「動作確認」)。

### 全ての差分

```diff
--- prereg/21_04b_ct2016_hinet_to_h5.py
+++ osaka/21_20b_osaka2018_hinet_to_h5.py
@@ -2,11 +2,19 @@
 # =============================================================================
-# Script : 21_04b_ct2016_hinet_to_h5.py  (v1.1)
-#          [鳥取県中部 2016 の Hi-net の連続波形を、地震の前後だけ取り、鳥取 2026 の h5(tottori_all_100Hz.h5)と
+# Script : 21_20b_osaka2018_hinet_to_h5.py  (v1)
+#          [大阪府北部 2018 の Hi-net の連続波形を、地震の前後だけ取り、鳥取 2026 の h5(tottori_all_100Hz.h5)と
 #           同じ形(30 秒窓・3 成分・100 Hz・窓ごと成分ごとの z-score・日本時間の epoch)の h5 にする]
-# Project: ARGUS(新生)— 2 つ目の余震系列での確認(21_04)の入力の 2 つ目
+# Project: ARGUS(新生)— 3 つ目の余震系列での確認(21_20)の入力の 2 つ目
+# 派生元 : 21_04b_ct2016_hinet_to_h5.py v1.1(SHA-256 81d69a13ddb3d432a93055e1657b9763b8634910777f004b6767d15788e952c0)。
+#          取り方・z-score・局の選び方・組み立て・ゲート(G-ref・G-dup・G-cover・G-clock・G-spec)・閾値は v1.1 と 1 字も変えていない。
+#          変えたのは次だけ(DIFF_LOG.md):
+#          (1) 入力と出力の名前: jma_osaka2018.csv・21_20a_osaka2018_catalog.json・ARGUS_osaka2018・osaka2018_100Hz.h5・
+#              stations_osaka2018.csv・data/21_20b_*.json・PDF/21_20b_*.pdf、表示の [21_20b]、h5 の出どころの属性の名前
+#          (2) ゲートで止まった時の表示の文: G-clock だけの FAIL なら、事前登録 21_20 で先に決めた扱い(G-clock は記録だけ、
+#              時刻は G-clock2 で決める)を表示する(止まり方と、h5 を _FAILED の名前にする動きは v1.1 と同じ)
+#          (3) VERSION を "v1 (=21_04b v1.1)" にした(この系列の 1 版目。取り方は 21_04b v1.1 と同じ。v1.1 の「要求の長さを短くして取り直す」も含む)
 #
 # なぜ必要か:
-#   21_04 は 21_02 と同じ規則・同じ作り方(15_01c で検測したキャッシュ)で確かめる。15_01c は
+#   21_20 は 21_02・21_04 と同じ規則・同じ作り方(15_01c v3.3 と同じ計算の 21_20c で検測したキャッシュ)で確かめる。15_01c は
 #   tottori_all_100Hz.h5 の形(/waves (N, 3, 3000)、/stations、/window_epoch = 窓の始まりの日本時間を UTC とみなした
-#   epoch 秒、属性 channel_order・n_samples・fs)を読む。そこで 2016 の波形をこの形にそろえ、15_01c の検測・QC・
+#   epoch 秒、属性 channel_order・n_samples・fs)を読む。そこで 2018 の波形をこの形にそろえ、15_01c の検測・QC・
 #   組み立てをそのまま通す(15_01c v3.3 で変えたのは、窓の索引のファイル名とその確かめ方・出力の置き場所 --base・
@@ -23,8 +31,8 @@
 #   1. 観測点: NIED の Hi-net(0101)の観測点の一覧(HinetPy の get_station_list。今の一覧。緯度・経度・標高のどれかが無い局は
-#      除く)から、本震(21_04a の JSON)に近い順に --n-sta + 10 局を候補にする。Hi-net のアカウントの「選んだ局」を
-#      最初の 1 回だけ data/21_04b_initial_selection.json に保存してから候補を選び、終わり(止めた時・失敗した時も)に元に戻す。
+#      除く)から、本震(21_20a の JSON)に近い順に --n-sta + 10 局を候補にする。Hi-net のアカウントの「選んだ局」を
+#      最初の 1 回だけ data/21_20b_initial_selection.json に保存してから候補を選び、終わり(止めた時・失敗した時も)に元に戻す。
 #      選んだ後の選択が空(= 全局)か候補の外の局を含めば STOP(全局のまま取ると何倍も時間がかかる)。
-#      途中で落ちて戻せなかった時は --restore-selection で戻せる。同時に 2 つ回さないよう data/21_04b.lock を置く
+#      途中で落ちて戻せなかった時は --restore-selection で戻せる。同時に 2 つ回さないよう data/21_20b.lock を置く
 #      (区切りごとに新しくし、30 分より古い印は止まった実行の印とみなす。Colab が切れた直後は --restore-selection --break-lock)。
-#   2. 取る時間の区切り: 21_04a の CSV の Mj ≥ 1.5 の地震ごとに、[発生時刻 − 10 s を分に切り下げ, 発生時刻 + 45 s を
+#   2. 取る時間の区切り: 21_20a の CSV の Mj ≥ 1.5 の地震ごとに、[発生時刻 − 10 s を分に切り下げ, 発生時刻 + 45 s を
 #      分に切り上げ](日本時間)。15_01c が使う区間 [発生 − 10 s, 発生 + 45 s] を 30 秒窓で必ず覆う。間が 2 分以下の
@@ -33,6 +41,6 @@
 #      分。60 局なら 60 分なので、Hi-net への要求も 1 回)。
-#      v1.1(2026-10-28、煙試験で本震の 60 分の区切りが Hi-net 側で 3 回とも失敗したため): 1 回の要求の長さ max_span を、
+#      21_04b v1.1 から引き継ぎ(2026-10-28、鳥取県中部 2016 の煙試験で本震の 60 分の区切りが Hi-net 側で 3 回とも失敗したため): 1 回の要求の長さ max_span を、
 #      失敗したら 60 → 20 → 10 → 5 分と短くして取り直す(1 区切りに最大 4 回)。短くした長さで取れたら、その実行の残りの
 #      区切りもその長さから始める(その長さで実際に分けて取れた時だけ)。試すたびに動いている印(lock)を新しくする。HinetPy が短い要求に分けて取り、1 つにつないで返すので、取れる波形・窓・h5 は v1 と同じ
-#      (要求の分け方だけが変わる)。検測・ゲート・組み立ては v1 から 1 字も変えていない。
+#      (要求の分け方だけが変わる)。検測・ゲート・組み立ては 21_04b v1 から 1 字も変えていない。
 #   3. 区切りごと(途中で止まっても、終わった区切りは飛ばして続きから): WIN32 をローカルの一時フォルダに取り、
@@ -51,8 +59,9 @@
 #      区切りの半分以上でデータがある局のうち本震に近い順に --n-sta 局(既定 50。鳥取 2026 の局の数と同じ)を選び、その局の
-#      窓だけを書く。data/catalog/stations_ct2016.csv(列 id, latitude, longitude, elevation。緯度・経度は 2016 年の
+#      窓だけを書く。data/catalog/stations_osaka2018.csv(列 id, latitude, longitude, elevation。緯度・経度は 2018 年の
 #      チャンネル表、標高は NIED の一覧の height(m)。stations.csv と同じ列)も書く。
-#      ゲートを書きかけのファイル(.part)で確かめ、全て通った時だけ data/waves/ct2016_100Hz.h5 の名前にする
-#      (通らなければ ct2016_100Hz_FAILED.h5 にして STOP。15_01c に渡る名前の h5 は作らない)。
+#      ゲートを書きかけのファイル(.part)で確かめ、全て通った時だけ data/waves/osaka2018_100Hz.h5 の名前にする
+#      (通らなければ osaka2018_100Hz_FAILED.h5 にして STOP。21_20c に渡る名前の h5 は作らない。G-clock だけの FAIL の扱いは
+#      事前登録 21_20 に先に決めてある: 記録だけで、_FAILED の h5 と stations_osaka2018.csv.part を 21_20c に渡し、時刻は G-clock2 で決める)。
 #      --partial(煙試験の確認): 取った区切りだけで組み立て、名前に _partial を付ける。
-#   5. ゲート(組み立ての後に表示し、data/21_04b_report.json に合否と一緒に書く):
+#   5. ゲート(組み立ての後に表示し、data/21_20b_report.json に合否と一緒に書く):
 #      - G-ref: 参照の h5 の z-score の確認に合格(fs = 100)。出力も同じ確認に合格
@@ -70,3 +79,3 @@
 #        違いがあれば限界に書く)
-#   6. 図: PDF/21_04b_coverage.pdf(局 × 区切りのデータの有無)、PDF/21_04b_mainshock.pdf(本震の上下動の
+#   6. 図: PDF/21_20b_coverage.pdf(局 × 区切りのデータの有無)、PDF/21_20b_mainshock.pdf(本震の上下動の
 #      記録の並びと、予想の P の印)。白背景・英語・凡例は枠の外。
@@ -75,8 +84,8 @@
 #   win32tools の catwin32・win2sac_32 が PATH にある(ノートの セル 3)、HinetPy 0.13.0。
-# 止める条件(STOP): 資格情報が無い・win2sac_32 が無い・参照の h5 が読めないか形が違うか fs が無い・21_04a の JSON が無い・
+# 止める条件(STOP): 資格情報が無い・win2sac_32 が無い・参照の h5 が読めないか形が違うか fs が無い・21_20a の JSON が無い・
 #   置き場所が足りない見込み・局の選択が効かない・別の実行の印がある・3 回ずつ試して取れない区切りが 3 つ続く・組み立てで取っていない
 #   区切りがあるか読めないファイルがある・使える局が 0・窓が 0・G-ref・G-dup・G-cover < 0.80・G-clock の失敗。
-# 限界(21_04 の限界にも書く):
+# 限界(21_20 の限界にも書く):
 #   - 観測点は Hi-net(0101)だけで、鳥取 2026 の 50 局(Hi-net のほか京大防災研・気象庁などを含む)とは種類と並びが違う
-#   - 候補は今の NIED の一覧から選ぶので、2016 年にあって今は無い局は入らない
+#   - 候補は今の NIED の一覧から選ぶので、2018 年にあって今は無い局は入らない
 #   - 地震の前後だけを取る(連続ではない)。15_01c が使う区間は全て含む。区切りの中で欠けがある局は、その区切りでは使わない
@@ -84,13 +93,13 @@
 #
-# Usage : (Colab、ノート 21_04_ct2016_colab.ipynb の セル 6〜9)
-#   計画だけ:       !python /content/drive/MyDrive/ARGUS/src/21_04b_ct2016_hinet_to_h5.py --ref-h5 <参照の h5> --dry-run
-#   煙試験(本震の区間に掛かる区切りを先に 3 区切り): !python .../21_04b_ct2016_hinet_to_h5.py --ref-h5 <参照の h5> --max-blocks 3
-#                    続けて !python .../21_04b_ct2016_hinet_to_h5.py --ref-h5 <参照の h5> --assemble --partial(取った分だけでゲートを見る)
-#   本番(続きから):   !python .../21_04b_ct2016_hinet_to_h5.py --ref-h5 <参照の h5>
-#   組み立て:         !python .../21_04b_ct2016_hinet_to_h5.py --ref-h5 <参照の h5> --assemble
-#   選択を戻すだけ:   !python .../21_04b_ct2016_hinet_to_h5.py --ref-h5 <参照の h5> --restore-selection [--break-lock](セル 8b)
-# Output (--out の下。既定 /content/drive/MyDrive/ARGUS_ct2016):
-#   data/blocks/blk_*.npz / data/21_04b_plan.json / data/21_04b_initial_selection.json /
-#   data/waves/ct2016_100Hz.h5 / data/catalog/stations_ct2016.csv / data/21_04b_report.json /
-#   PDF/21_04b_coverage.pdf / PDF/21_04b_mainshock.pdf(--partial ではそれぞれ _partial 付き)
+# Usage : (Colab、ノート 21_20_osaka2018_colab.ipynb の セル 6〜9。手順は COLAB_STEPS_JA.md)
+#   計画だけ:       !python /content/drive/MyDrive/ARGUS/src/21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5> --dry-run
+#   煙試験(本震の区間に掛かる区切りを先に 3 区切り): !python .../21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5> --max-blocks 3
+#                    続けて !python .../21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5> --assemble --partial(取った分だけでゲートを見る)
+#   本番(続きから):   !python .../21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5>
+#   組み立て:         !python .../21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5> --assemble
+#   選択を戻すだけ:   !python .../21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5> --restore-selection [--break-lock](セル 8b)
+# Output (--out の下。既定 /content/drive/MyDrive/ARGUS_osaka2018):
+#   data/blocks/blk_*.npz / data/21_20b_plan.json / data/21_20b_initial_selection.json /
+#   data/waves/osaka2018_100Hz.h5 / data/catalog/stations_osaka2018.csv / data/21_20b_report.json /
+#   PDF/21_20b_coverage.pdf / PDF/21_20b_mainshock.pdf(--partial ではそれぞれ _partial 付き)
 #   区切りのファイルは組み立ての後も消さない(h5 を作り直せるように。要らなくなったら data/blocks を手で消す)
@@ -117,3 +126,3 @@
 
-VERSION = "v1.1"
+VERSION = "v1 (=21_04b v1.1)"              # 21_20b の 1 版目(取り方は 21_04b v1.1 と同じ)
 ROOT = Path(__file__).resolve().parent.parent
@@ -269,10 +278,10 @@
         for k in ("waves", "stations", "window_epoch"):
-            if k not in H: sys.exit(f"[21_04b] STOP(G-ref): 参照の h5 に /{k} が無い")
+            if k not in H: sys.exit(f"[21_20b] STOP(G-ref): 参照の h5 に /{k} が無い")
         W = H["waves"]
-        if tuple(W.shape[1:]) != (3, WIN_N): sys.exit(f"[21_04b] STOP(G-ref): 参照の /waves の形 {W.shape} が (N, 3, 3000) でない")
+        if tuple(W.shape[1:]) != (3, WIN_N): sys.exit(f"[21_20b] STOP(G-ref): 参照の /waves の形 {W.shape} が (N, 3, 3000) でない")
         attrs = {k: (v.decode() if isinstance(v, bytes) else (v.tolist() if hasattr(v, "tolist") else v)) for k, v in H.attrs.items()}
         fsv = attrs.get("fs", attrs.get("sampling_rate"))
-        if fsv is None: sys.exit("[21_04b] STOP(G-ref): 参照の h5 に属性 fs が無い")
+        if fsv is None: sys.exit("[21_20b] STOP(G-ref): 参照の h5 に属性 fs が無い")
         fs = float(np.ravel(fsv)[0])
-        if abs(fs - FS) > 1e-6: sys.exit(f"[21_04b] STOP(G-ref): 参照の fs = {fs}")
+        if abs(fs - FS) > 1e-6: sys.exit(f"[21_20b] STOP(G-ref): 参照の fs = {fs}")
         n = W.shape[0]
@@ -297,3 +306,3 @@
     u, p = os.environ.get("HINET_USER"), os.environ.get("HINET_PASS")
-    if not u or not p: sys.exit("[21_04b] STOP: 環境変数 HINET_USER・HINET_PASS が無い(ノートの セル 4 で入れる)")
+    if not u or not p: sys.exit("[21_20b] STOP: 環境変数 HINET_USER・HINET_PASS が無い(ノートの セル 4 で入れる)")
     from HinetPy import Client
@@ -306,5 +315,5 @@
         client.select_stations(NET, names if names else None)
-        print(f"[21_04b] アカウントの局の選択を元に戻した({len(names) if names else '全局'})")
+        print(f"[21_20b] アカウントの局の選択を元に戻した({len(names) if names else '全局'})")
     except Exception as e:                                  # 戻せなかった時は必ず表示する
-        print(f"[21_04b] 注意: アカウントの局の選択を戻せなかった({e})。Hi-net のサイトで確かめる。保存した選択: {sel_path}")
+        print(f"[21_20b] 注意: アカウントの局の選択を戻せなかった({e})。Hi-net のサイトで確かめる。保存した選択: {sel_path}")
 
@@ -355,3 +364,3 @@
     if lock.exists() and time.time() - lock.stat().st_mtime < LOCK_STALE_S:
-        sys.exit(f"[21_04b] STOP: 別の実行が動いている印 {lock}({lock.read_text().strip()})が 30 分以内に更新されている。"
+        sys.exit(f"[21_20b] STOP: 別の実行が動いている印 {lock}({lock.read_text().strip()})が 30 分以内に更新されている。"
                  "Colab が切れた直後なら別の実行は無いので、セル 8b(--restore-selection --break-lock)を回してからセル 8 をもう一度")
@@ -377,8 +386,8 @@
     extra = [f.name for f in allf if f.name not in exp]
-    if extra: print(f"[21_04b] 注意: 今の計画に無い区切りのファイル {len(extra)} は使わない(例 {extra[:3]})")
+    if extra: print(f"[21_20b] 注意: 今の計画に無い区切りのファイル {len(extra)} は使わない(例 {extra[:3]})")
     files = [f for f in allf if f.name in exp]
     bad = [f.name for f in files if not blk_ok(f)]
-    if bad: sys.exit(f"[21_04b] STOP: 読めない区切りのファイルが {len(bad)} ある(例 {bad[:3]})。消してから取り直す(セル 8)")
+    if bad: sys.exit(f"[21_20b] STOP: 読めない区切りのファイルが {len(bad)} ある(例 {bad[:3]})。消してから取り直す(セル 8)")
     missing = sorted(exp - {f.name for f in files})
-    if not files: sys.exit("[21_04b] STOP: 区切りの結果が 1 つも無い")
+    if not files: sys.exit("[21_20b] STOP: 区切りの結果が 1 つも無い")
     pres, chan = {}, {}
@@ -393,6 +402,6 @@
         if not (allow_missing and frac >= MIN_FETCHED):
-            sys.exit(f"[21_04b] STOP: 取っていない区切りが {len(missing)} ある(取れた割合 {frac:.3f}、例 {missing[:3]})。セル 8 を"
+            sys.exit(f"[21_20b] STOP: 取っていない区切りが {len(missing)} ある(取れた割合 {frac:.3f}、例 {missing[:3]})。セル 8 を"
                      f"もう一度回してから --assemble。何度回しても取れない区切りだけが残り、取れた割合が {MIN_FETCHED} 以上なら "
                      "--allow-missing で続けてよい(事前に決めた規則。その区切りの地震は G-cover で覆えない地震として数える)")
-        print(f"[21_04b] 注意(--allow-missing): 取っていない区切り {len(missing)}(取れた割合 {frac:.3f} ≥ {MIN_FETCHED})で続ける: {missing}")
+        print(f"[21_20b] 注意(--allow-missing): 取っていない区切り {len(missing)}(取れた割合 {frac:.3f} ≥ {MIN_FETCHED})で続ける: {missing}")
     done_iv = []
@@ -410,5 +419,5 @@
     keep = ok[:n_sta]
-    if not keep: sys.exit("[21_04b] STOP: 区切りの半分以上でデータがある局が 0")
-    if len(keep) < n_sta: print(f"[21_04b] 注意: 区切りの半分以上でデータがある局が {len(keep)} しかない(--n-sta {n_sta})")
-    print(f"[21_04b] 組み立て: 区切り {nb}(計画 {len(plan)})  使う局 {len(keep)}(最も遠い局 "
+    if not keep: sys.exit("[21_20b] STOP: 区切りの半分以上でデータがある局が 0")
+    if len(keep) < n_sta: print(f"[21_20b] 注意: 区切りの半分以上でデータがある局が {len(keep)} しかない(--n-sta {n_sta})")
+    print(f"[21_20b] 組み立て: 区切り {nb}(計画 {len(plan)})  使う局 {len(keep)}(最も遠い局 "
           f"{haversine_km(ml, mo, cand_meta[keep[-1]]['lat'], cand_meta[keep[-1]]['lon']):.1f} km)")
@@ -416,3 +425,3 @@
     (OUT / "data" / "waves").mkdir(parents=True, exist_ok=True); (OUT / "data" / "catalog").mkdir(parents=True, exist_ok=True)
-    h5p = OUT / "data" / "waves" / ("ct2016_100Hz_partial.h5" if partial else "ct2016_100Hz.h5"); tmpp = h5p.with_suffix(".h5.part")
+    h5p = OUT / "data" / "waves" / ("osaka2018_100Hz_partial.h5" if partial else "osaka2018_100Hz.h5"); tmpp = h5p.with_suffix(".h5.part")
     if h5p.exists(): h5p.unlink()                              # 前の組み立ての結果は、ゲートに通るまで置かない
@@ -422,3 +431,3 @@
         z = np.load(f, allow_pickle=False); n_tot += int(np.isin(z["stations"], list(kset)).sum())
-    if n_tot == 0: sys.exit("[21_04b] STOP: 書く窓が 0")
+    if n_tot == 0: sys.exit("[21_20b] STOP: 書く窓が 0")
     chunks = tuple(min(c, n) for c, n in zip(ref["chunks"], (n_tot, 3, WIN_N))) if ref.get("chunks") else None
@@ -439,5 +448,5 @@
         H.attrs["channel_order"] = "UD,NS,EW"; H.attrs["n_samples"] = WIN_N; H.attrs["fs"] = FS
-        H.attrs["ct2016_source"] = (f"NIED Hi-net (0101) continuous data via HinetPy, event blocks only; 21_04b_ct2016_hinet_to_h5.py "
+        H.attrs["osaka2018_source"] = (f"NIED Hi-net (0101) continuous data via HinetPy, event blocks only; 21_20b_osaka2018_hinet_to_h5.py "
                                     f"{VERSION}; per-window per-component z-score; window_epoch = JST wall clock as UTC epoch")
-    stp = OUT / "data" / "catalog" / ("stations_ct2016_partial.csv" if partial else "stations_ct2016.csv")
+    stp = OUT / "data" / "catalog" / ("stations_osaka2018_partial.csv" if partial else "stations_osaka2018.csv")
     if stp.exists(): stp.unlink()
@@ -509,11 +518,11 @@
     all_pass = G["ref_pass"] and G["dup_pass"] and G["cover_pass"] and G["clock_pass"]
-    rep = dict(script="21_04b_ct2016_hinet_to_h5.py", version=VERSION, h5=str(h5p), n_windows=n_tot, stations=keep,
+    rep = dict(script="21_20b_osaka2018_hinet_to_h5.py", version=VERSION, h5=str(h5p), n_windows=n_tot, stations=keep,
                presence={s: pres[s] for s in keep}, n_blocks=nb, n_blocks_planned=len(plan), n_blocks_missing=len(missing),
                missing_blocks=missing, allow_missing=bool(allow_missing), ref=ref, gates=G, all_gates_pass=bool(all_pass), partial=bool(partial))
-    json.dump(rep, open(OUT / "data" / ("21_04b_report_partial.json" if partial else "21_04b_report.json"), "w"), indent=1, default=str)
-    print(f"[21_04b] G-ref: 参照 dtype {ref['waves_dtype']}・z-score 確認 {'PASS' if ref['zcheck_pass'] else 'FAIL'}  出力の z-score 確認 "
+    json.dump(rep, open(OUT / "data" / ("21_20b_report_partial.json" if partial else "21_20b_report.json"), "w"), indent=1, default=str)
+    print(f"[21_20b] G-ref: 参照 dtype {ref['waves_dtype']}・z-score 確認 {'PASS' if ref['zcheck_pass'] else 'FAIL'}  出力の z-score 確認 "
           f"{'PASS' if G['out_zcheck']['pass_'] else 'FAIL'}(最大 |平均| {G['out_zcheck']['max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
           f"{G['out_zcheck']['max_abs_std_minus_1']:.3g})")
-    print(f"[21_04b] G-dup: 重なり {G['dup']}  " + ("PASS" if G["dup"] == 0 else "FAIL"))
-    print(f"[21_04b] G-cover({G['cover_n_events']} 地震): Mj ≥ 1.5 の地震で 4 局以上が覆う割合 {G['cover_frac_ge4']:.3f}(覆う局の数の中央値 "
+    print(f"[21_20b] G-dup: 重なり {G['dup']}  " + ("PASS" if G["dup"] == 0 else "FAIL"))
+    print(f"[21_20b] G-cover({G['cover_n_events']} 地震): Mj ≥ 1.5 の地震で 4 局以上が覆う割合 {G['cover_frac_ge4']:.3f}(覆う局の数の中央値 "
           f"{G['cover_median_stations']:.0f})  " + ("PASS" if G["cover_frac_ge4"] >= COVER_OK else "注意" if G["cover_frac_ge4"] >= COVER_STOP else "FAIL"))
@@ -521,7 +530,7 @@
         cm = c["median_abs_resid_s"]
-        print(f"[21_04b] G-clock{'(本震)' if c['mainshock'] else '(他の地震)'} {c['origin_jst'][:22]} Mj {c['mj']}: 近い局 {c['n']} で、"
+        print(f"[21_20b] G-clock{'(本震)' if c['mainshock'] else '(他の地震)'} {c['origin_jst'][:22]} Mj {c['mj']}: 近い局 {c['n']} で、"
               f"STA/LTA の立ち上がり − 震源距離/6.0 km/s の |差| の中央値 {'—' if cm is None else f'{cm:.2f}'} s  "
               + ("PASS" if c["pass_"] else ("FAIL" if c["mainshock"] or c["n"] >= 4 else "判定なし(立ち上がりが取れた局が 4 未満)")))
-    print(f"[21_04b] G-clock まとめ: " + ("PASS" if G["clock_pass"] else "FAIL"))
-    print(f"[21_04b] G-spec(記録だけ): 0.1–1 Hz / 1–20 Hz の力の比の中央値 参照 {G['band_ratio_ref']:.3g}・出力 {G['band_ratio_out']:.3g}"
+    print(f"[21_20b] G-clock まとめ: " + ("PASS" if G["clock_pass"] else "FAIL"))
+    print(f"[21_20b] G-spec(記録だけ): 0.1–1 Hz / 1–20 Hz の力の比の中央値 参照 {G['band_ratio_ref']:.3g}・出力 {G['band_ratio_out']:.3g}"
           f"(比 {rr:.2f})" + ("  注意: 3 倍以上違う(参照の h5 でフィルタをかけた可能性。記録だけで、止めずに先に進む。限界に書く)"
@@ -532,6 +541,9 @@
         why = [k for k, v in (("G-ref", G["ref_pass"]), ("G-dup", G["dup_pass"]), ("G-cover", G["cover_pass"]), ("G-clock", G["clock_pass"])) if not v]
-        sys.exit(f"[21_04b] STOP({', '.join(why)}): h5 は {failed.name} にした(セル 10 には進まない。この出力を貼って相談)")
+        if why == ["G-clock"]:                                 # 21_20: 表示の文だけ(止まり方は 21_04b v1.1 と同じ)
+            sys.exit(f"[21_20b] STOP(G-clock だけ): h5 は {failed.name}、局の表は {stp.name}.part にした。事前登録 21_20 の規則では "
+                     "G-clock は記録だけで、時刻は G-clock2(21_20d)で決める。セル 10 に、この 2 つのファイルを渡して進む(この出力を貼る)")
+        sys.exit(f"[21_20b] STOP({', '.join(why)}): h5 は {failed.name} にした(セル 10 には進まない。この出力を貼って相談)")
     os.replace(tmpp, h5p); os.replace(stp.with_suffix(".csv.part"), stp)
     sfx = "_partial" if partial else ""
-    print(f"[21_04b] 出力: {h5p}(窓 {n_tot})  {OUT / 'data' / 'catalog' / f'stations_ct2016{sfx}.csv'}  {OUT / 'data' / f'21_04b_report{sfx}.json'}"
+    print(f"[21_20b] 出力: {h5p}(窓 {n_tot})  {OUT / 'data' / 'catalog' / f'stations_osaka2018{sfx}.csv'}  {OUT / 'data' / f'21_20b_report{sfx}.json'}"
           + ("(煙試験の確認用。本番の組み立てはセル 9)" if partial else ""))
@@ -553,3 +565,3 @@
     cb = fig.colorbar(im, ax=ax, pad=0.01); cb.set_label("Fraction kept")
-    fig.tight_layout(); fig.savefig(PDFD / f"21_04b_coverage{suf}.pdf", bbox_inches="tight"); plt.close(fig)
+    fig.tight_layout(); fig.savefig(PDFD / f"21_20b_coverage{suf}.pdf", bbox_inches="tight"); plt.close(fig)
     if sec:
@@ -569,3 +581,3 @@
         ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False); ax.grid(alpha=0.3, axis="x")
-        fig.tight_layout(); fig.savefig(PDFD / f"21_04b_mainshock{suf}.pdf", bbox_inches="tight"); plt.close(fig)
+        fig.tight_layout(); fig.savefig(PDFD / f"21_20b_mainshock{suf}.pdf", bbox_inches="tight"); plt.close(fig)
 
@@ -575,7 +587,7 @@
     ap = argparse.ArgumentParser()
-    ap.add_argument("--catalog", default=str(ROOT / "data" / "catalog" / "jma_ct2016.csv"))
-    ap.add_argument("--summary", default=str(ROOT / "data" / "catalog" / "21_04a_ct2016_catalog.json"))
+    ap.add_argument("--catalog", default=str(ROOT / "data" / "catalog" / "jma_osaka2018.csv"))
+    ap.add_argument("--summary", default=str(ROOT / "data" / "catalog" / "21_20a_osaka2018_catalog.json"))
     ap.add_argument("--ref-h5", required=True, help="鳥取 2026 の tottori_all_100Hz.h5(形を写すため。読むだけ)")
-    ap.add_argument("--out", default=("/content/drive/MyDrive/ARGUS_ct2016" if Path("/content/drive").exists()
-                                      else str(ROOT.parent / "ARGUS_ct2016")))
+    ap.add_argument("--out", default=("/content/drive/MyDrive/ARGUS_osaka2018" if Path("/content/drive").exists()
+                                      else str(ROOT.parent / "ARGUS_osaka2018")))
     ap.add_argument("--tmp", default=("/content/hinet_tmp" if Path("/content").exists() else tempfile.gettempdir()))
@@ -588,3 +600,3 @@
     ap.add_argument("--restore-selection", action="store_true", help="アカウントの局の選択を保存した元の状態に戻すだけ(途中で落ちた時)")
-    ap.add_argument("--break-lock", action="store_true", help="--restore-selection と一緒に: 切れた実行の印(data/21_04b.lock)を消す")
+    ap.add_argument("--break-lock", action="store_true", help="--restore-selection と一緒に: 切れた実行の印(data/21_20b.lock)を消す")
     a = ap.parse_args()
@@ -593,3 +605,3 @@
     tmp_root = Path(a.tmp); tmp_root.mkdir(parents=True, exist_ok=True)
-    if not Path(a.summary).exists(): sys.exit(f"[21_04b] STOP: {a.summary} が無い(21_04a を先に回す)")
+    if not Path(a.summary).exists(): sys.exit(f"[21_20b] STOP: {a.summary} が無い(21_20a を先に回す)")
     summ = json.load(open(a.summary))
@@ -602,15 +614,15 @@
     tot_min = sum(s for _, s in plan)
-    print(f"[21_04b] {VERSION}  地震(Mj ≥ 1.5){len(org)} → 区切り {len(plan)}(分の合計 {tot_min}、最長 {max(s for _, s in plan)} 分)")
+    print(f"[21_20b] {VERSION}  地震(Mj ≥ 1.5){len(org)} → 区切り {len(plan)}(分の合計 {tot_min}、最長 {max(s for _, s in plan)} 分)")
     rng = np.random.default_rng(7)
     ref = read_ref(a.ref_h5, rng)
-    print(f"[21_04b] 参照の h5: 窓 {ref['n_windows']}  /waves {ref['waves_dtype']}  /stations {ref['stations_dtype']}  "
+    print(f"[21_20b] 参照の h5: 窓 {ref['n_windows']}  /waves {ref['waves_dtype']}  /stations {ref['stations_dtype']}  "
           f"/window_epoch {ref['epoch_dtype']}  chunks {ref['chunks']}  圧縮 {ref['compression']}  属性 {ref['attrs']}  "
           f"他のデータ {ref['other_datasets']}")
-    print(f"[21_04b] 参照の z-score の確認(無作為 {REF_NSAMPLE} 窓): 最大 |平均| {ref['zcheck_max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
+    print(f"[21_20b] 参照の z-score の確認(無作為 {REF_NSAMPLE} 窓): 最大 |平均| {ref['zcheck_max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
           f"{ref['zcheck_max_abs_std_minus_1']:.3g}  " + ("PASS" if ref["zcheck_pass"] else "FAIL")
           + f"  30 s 格子にそろう割合 {ref['grid30_frac']:.3f}(余り {ref['grid30_residues']})  0.1–1/1–20 Hz の力の比 {ref['band_ratio_median']:.3g}")
-    if not ref["zcheck_pass"]: sys.exit("[21_04b] STOP(G-ref): 参照の h5 が窓ごとの z-score に見えない(この行を貼って相談)")
+    if not ref["zcheck_pass"]: sys.exit("[21_20b] STOP(G-ref): 参照の h5 が窓ごとの z-score に見えない(この行を貼って相談)")
     dt = np.dtype(ref["waves_dtype"])
-    plan_p = OUT / "data" / "21_04b_plan.json"
-    sel_p = OUT / "data" / "21_04b_initial_selection.json"
+    plan_p = OUT / "data" / "21_20b_plan.json"
+    sel_p = OUT / "data" / "21_20b_initial_selection.json"
 
@@ -618,13 +630,13 @@
         P = json.load(open(plan_p)) if plan_p.exists() else None
-        if P is None: sys.exit("[21_04b] STOP: 計画の 21_04b_plan.json が無い")
+        if P is None: sys.exit("[21_20b] STOP: 計画の 21_20b_plan.json が無い")
         assemble(OUT, PDFD, ref, summ, rows, P["candidates"], a.n_sta, plan, partial=a.partial, allow_missing=a.allow_missing); return
 
-    lock = OUT / "data" / "21_04b.lock"
+    lock = OUT / "data" / "21_20b.lock"
     if a.restore_selection:
         if a.break_lock and lock.exists():
-            print(f"[21_04b] 切れた実行の印を消した: {lock.read_text().strip()}"); lock.unlink()
+            print(f"[21_20b] 切れた実行の印を消した: {lock.read_text().strip()}"); lock.unlink()
         check_lock(lock)                                       # 動いている実行があれば、その選択を変えない
-        if not sel_p.exists(): sys.exit(f"[21_04b] STOP: 保存した選択 {sel_p} が無い")
+        if not sel_p.exists(): sys.exit(f"[21_20b] STOP: 保存した選択 {sel_p} が無い")
         restore_selection(hinet_client(), sel_p); return
-    if not shutil.which("win2sac_32") and not a.dry_run: sys.exit("[21_04b] STOP: win2sac_32 が PATH に無い(ノートの セル 3)")
+    if not shutil.which("win2sac_32") and not a.dry_run: sys.exit("[21_20b] STOP: win2sac_32 が PATH に無い(ノートの セル 3)")
     client = hinet_client()
@@ -634,3 +646,3 @@
     stl = [s for s in stl if s.latitude is not None and s.longitude is not None and s.elevation is not None]
-    if len(stl) < n0: print(f"[21_04b] 緯度・経度・標高のどれかが無い局 {n0 - len(stl)} は候補から外した")
+    if len(stl) < n0: print(f"[21_20b] 緯度・経度・標高のどれかが無い局 {n0 - len(stl)} は候補から外した")
     stl.sort(key=lambda s: haversine_km(ml, mo, s.latitude, s.longitude))
@@ -639,3 +651,3 @@
                           dist_km=float(haversine_km(ml, mo, s.latitude, s.longitude))) for s in cands}
-    print(f"[21_04b] 候補局 {len(cands)}(本震から {cmeta[cands[0].name]['dist_km']:.1f}〜{cmeta[cands[-1].name]['dist_km']:.1f} km): "
+    print(f"[21_20b] 候補局 {len(cands)}(本震から {cmeta[cands[0].name]['dist_km']:.1f}〜{cmeta[cands[-1].name]['dist_km']:.1f} km): "
           + " ".join(s.name for s in cands))
@@ -645,6 +657,6 @@
     free = shutil.disk_usage(OUT).free / 1e9
-    print(f"[21_04b] 置き場所の見込み: 区切りのファイル約 {gb:.1f} GB + 組み立てた h5 約 {gb * a.n_sta / len(cands):.1f} GB"
+    print(f"[21_20b] 置き場所の見込み: 区切りのファイル約 {gb:.1f} GB + 組み立てた h5 約 {gb * a.n_sta / len(cands):.1f} GB"
           f"(Drive の空き {free:.0f} GB。ここに出るのは Colab から見た空きで、Drive の契約の上限とは違うことがある)")
     if a.dry_run:
-        print(f"[21_04b] 計画だけ(--dry-run): {plan_p}。1 区切りに 30 s かかるとして約 {len(plan) * 30 / 3600:.1f} 時間、"
+        print(f"[21_20b] 計画だけ(--dry-run): {plan_p}。1 区切りに 30 s かかるとして約 {len(plan) * 30 / 3600:.1f} 時間、"
               f"60 s なら約 {len(plan) * 60 / 3600:.1f} 時間(煙試験で測る)")
@@ -658,3 +670,3 @@
             json.dump(dict(saved_utc=datetime.now(timezone.utc).isoformat(), stations=names0), open(sel_p, "w"), indent=1)
-            print(f"[21_04b] アカウントの今の局の選択を保存した({len(names0) if names0 else '全局'}): {sel_p}")
+            print(f"[21_20b] アカウントの今の局の選択を保存した({len(names0) if names0 else '全局'}): {sel_p}")
         for f in (OUT / "data" / "blocks").glob("*.tmp"): f.unlink()          # 前に途中で切れた書きかけ
@@ -663,6 +675,6 @@
             if f.exists() and not blk_ok(f):
-                print(f"[21_04b] 読めない区切りのファイル {f.name} を消して取り直す"); f.unlink()
+                print(f"[21_20b] 読めない区切りのファイル {f.name} を消して取り直す"); f.unlink()
         todo = [(b, s) for b, s in plan if not blk_done(OUT, b, s)]
         need = (sum(s for _, s in todo) * 2 * len(cands) * 3 * WIN_N * dt.itemsize / 1e9) + gb * a.n_sta / len(cands)
-        if free < 1.1 * need: sys.exit(f"[21_04b] STOP: 置き場所が足りない見込み(残りの区切りと h5 で約 {need:.1f} GB、空き {free:.0f} GB)")
+        if free < 1.1 * need: sys.exit(f"[21_20b] STOP: 置き場所が足りない見込み(残りの区切りと h5 で約 {need:.1f} GB、空き {free:.0f} GB)")
         if a.max_blocks:                                     # 煙試験: 本震の区間 [−10 s, +45 s] に掛かる区切りを最初に(G-clock を早く確かめる)
@@ -673,6 +685,6 @@
         n_done = sum(1 for b, s in plan if blk_done(OUT, b, s))
-        print(f"[21_04b] 取る区切り {len(todo)}(済み {n_done}/{len(plan)})")
+        print(f"[21_20b] 取る区切り {len(todo)}(済み {n_done}/{len(plan)})")
         names = [s.name for s in cands]
         if not todo:
-            print("[21_04b] 取る区切りが無い(全部済み)。次はセル 9(--assemble)"); return
+            print("[21_20b] 取る区切りが無い(全部済み)。次はセル 9(--assemble)"); return
         max_span = max(1, min(60, 12000 // (3 * len(names))))
@@ -685,4 +697,4 @@
         if not got or not set(got) <= set(names):
-            sys.exit(f"[21_04b] STOP: アカウントの局の選択が候補にならなかった(選ばれた局 {len(got)})。全局のまま取ると何倍も時間がかかる")
-        if set(got) != set(names): print(f"[21_04b] 注意: 選べた局 {len(got)} が候補 {len(names)} より少ない(無い局: {sorted(set(names) - set(got))[:10]})")
+            sys.exit(f"[21_20b] STOP: アカウントの局の選択が候補にならなかった(選ばれた局 {len(got)})。全局のまま取ると何倍も時間がかかる")
+        if set(got) != set(names): print(f"[21_20b] 注意: 選べた局 {len(got)} が候補 {len(names)} より少ない(無い局: {sorted(set(names) - set(got))[:10]})")
         for i, (b, s) in enumerate(todo):
@@ -707,3 +719,3 @@
                 print(f"    区切り {b:%Y-%m-%d %H:%M} ({s} 分) を {len(tries)} 回とも取れなかった(飛ばす。次に回すと取り直す)")
-                if fails >= 3: sys.exit("[21_04b] STOP: 3 つの区切りで続けて取れなかった(Hi-net の状態を確かめて、もう一度回すと続きから)")
+                if fails >= 3: sys.exit("[21_20b] STOP: 3 つの区切りで続けて取れなかった(Hi-net の状態を確かめて、もう一度回すと続きから)")
                 continue
@@ -724,3 +736,3 @@
     left = sum(1 for b, s in plan if not blk_done(OUT, b, s))
-    print(f"[21_04b] 終わり: 残りの区切り {left}/{len(plan)}" + ("(全部済んだら --assemble)" if left == 0 else "(もう一度回すと続きから)"))
+    print(f"[21_20b] 終わり: 残りの区切り {left}/{len(plan)}" + ("(全部済んだら --assemble)" if left == 0 else "(もう一度回すと続きから)"))
 
```

## 21_20c_osaka2018_realpick_cache_colab.py(元: 15_01c_tottori_realpick_cache_colab.py)

変わった行: −28 / +50(冒頭の説明を含む)

### 変えたことと理由
- 冒頭: 21_20c の説明(派生元・変更点・大阪の回し方)を先に足し、15_01c v3.3 の説明はそのまま残した。
- 出力の置き場所の既定: ARGUS_tottori → ARGUS_osaka2018(Colab では `--base` で必ず渡す)。
- `--jma`・`--stations`・`--box` を必須にした(既定は鳥取 2026 の CSV と西鳥取の箱。渡し忘れると鳥取のまま回るのを防ぐ)。`--h5` の説明の文。
- 観測点の数の表示: 固定の文字 "(stations.csv)" → `--stations` に渡したファイルの名前(`Path(args.stations).name`。G-clock だけの FAIL の時は
  `stations_osaka2018.csv.part` と出る)。読む中身は変えていない。
- 表示の先頭 [15_01c] → [21_20c]、振幅整合の表示の「鳥取absmax中央値」→「大阪absmax中央値」、報告の `script_version` →
  "21_20c v1 (computation identical to 15_01c v3.3)"、図の題(Tottori 2026 → Northern Osaka 2018)、最後の表示の Mac のコピー先。
- 変えていないもの: 検測(PhaseNet "original"・最早の P・S)、STA/LTA の戻り、QC(TP_QC・SP_QC・和達)、局の選び方、窓、微分、
  振幅整合、出力の中身と名前の決まり(tottori_parsed_realpick{tag}.pt など。21_04 と同じ形)。
- 注意: 報告の `script_sha256` は 21_20c のファイルの値になる(15_01c v3.3 の値ではない)。事前登録 21_20 の 8 節と照らす。

### 全ての差分

```diff
--- prereg/15_01c_tottori_realpick_cache_colab.py
+++ osaka/21_20c_osaka2018_realpick_cache_colab.py
@@ -2,2 +2,24 @@
 # =============================================================================
+# Script : 21_20c_osaka2018_realpick_cache_colab.py  (v1)
+#          [大阪府北部 2018 の h5(21_20b)と気象庁の震源(21_20a)から、PhaseNet で P・S を測り、ARGUS のキャッシュ
+#           (tottori_parsed_realpick_osaka2018_m15.pt)を作る。検測・QC・局の選び方・組み立て・振幅整合は 15_01c v3.3 と同じ計算]
+# Project: ARGUS(新生)— 3 つ目の余震系列での確認(21_20)の入力の 3 つ目
+# 派生元 : 15_01c_tottori_realpick_cache_colab.py v3.3(SHA-256 e407f88b7345e689f0c989d2c95ecf2e1bfec1b857e09b4ab8ada44f2354258e)。
+#          検測・QC・組み立て・振幅整合・出力の中身は v3.3 と 1 字も変えていない(DIFF_LOG.md の差分で確かめられる)。変えたのは次だけ:
+#          (1) この冒頭の説明(下の「15_01c v3.3 の説明」は元のまま残す)
+#          (2) 出力の置き場所の既定: ARGUS_tottori → ARGUS_osaka2018(Colab では --base で必ず渡す)
+#          (3) --jma・--stations・--box を必ず渡す引数にした(既定が鳥取 2026 の CSV と西鳥取の箱なので、渡し忘れると鳥取のまま
+#              回ってしまう。それを防ぐため。値の渡し方は 15_01c v3.3 と同じ)
+#          (4) 表示の先頭 [15_01c] → [21_20c]、報告の script_version を "21_20c v1 (computation identical to 15_01c v3.3)" に、
+#              図の題 "Tottori 2026" → "Northern Osaka 2018"、最後の表示の Mac のコピー先(--tag に osaka2018 があれば
+#              data/osaka2018_processed/)、振幅整合の表示の「鳥取absmax中央値」→「大阪absmax中央値」
+#          出力の名前の決まり(tottori_parsed_realpick{tag}.pt・data/tottori_processed/・15_01c_build_report{tag}.json・
+#          15_01c_tottori_picks_qc{tag}.pdf)は、21_04 が使ったものと同じ形にするため変えていない(--tag _osaka2018_m15 で分ける)。
+#          報告の script_sha256 はこのファイルの SHA-256 になる(事前登録 21_20 の凍結の表と照らす)。
+# 大阪府北部 2018 の実行(ノート 21_20_osaka2018_colab.ipynb の セル 10・11。手順は COLAB_STEPS_JA.md):
+#   !python 21_20c_osaka2018_realpick_cache_colab.py --h5 <osaka2018_100Hz.h5(または _FAILED.h5)> --jma <jma_osaka2018.csv>
+#      --stations <stations_osaka2018.csv(または .csv.part)> --min-mag 1.5 --box <21_20a の JSON の box 4 つ>
+#      --base /content/ARGUS_osaka2018 --tag _osaka2018_m15 [--max-events 10 で煙試験。その時は --tag _osaka2018_smoke]
+#
+# ---- 以下は 15_01c v3.3 の説明(そのまま) ----
 # Script : 15_01c_tottori_realpick_cache_colab.py  [鳥取2026 キャッシュ構築 Colab版 v3.3]
@@ -99,4 +121,4 @@
 
-BASE = Path("/content/drive/MyDrive/ARGUS_tottori") \
-       if Path("/content/drive").exists() else Path(".") / "ARGUS_tottori"
+BASE = Path("/content/drive/MyDrive/ARGUS_osaka2018") \
+       if Path("/content/drive").exists() else Path(".") / "ARGUS_osaka2018"     # 21_20c: 既定の置き場所(--base で渡す)
 PDFD = BASE / "PDF"
@@ -123,5 +145,5 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--jma", default="/content/jma_tottori_2026.csv")
-ap.add_argument("--stations", default="/content/stations.csv")
-ap.add_argument("--h5", required=True, help="Drive上の tottori_all_100Hz.h5 のパス(セル2で確認)")
+ap.add_argument("--jma", required=True, help="21_20a の jma_osaka2018.csv(21_20c: 必ず渡す)")
+ap.add_argument("--stations", required=True, help="21_20b の stations_osaka2018.csv(21_20c: 必ず渡す)")
+ap.add_argument("--h5", required=True, help="21_20b の osaka2018_100Hz.h5 のパス")
 ap.add_argument("--knet-cache", default="", help="(任意)あればフル統計を開示")
@@ -142,8 +164,8 @@
                 help="window_epochの基準。実h5はJST基準と確定(15_01dプローブ)")
-ap.add_argument("--box", nargs=4, type=float, default=[35.15, 35.45, 133.00, 133.35],
+ap.add_argument("--box", nargs=4, type=float, required=True,
                 metavar=("LAT0", "LAT1", "LON0", "LON1"),
-                help="西鳥取ボックス(SERAPHのscore-boxと同一既定)")
+                help="21_20a の JSON の box(21_20c: 必ず渡す。西鳥取の既定は外した)")
 ap.add_argument("--tag", default="", help="出力の名前に付ける印(例 _m15)。v3.1 で追加")
 ap.add_argument("--overwrite-canon", action="store_true", help="--tag 無しで既存の正本を上書きする時だけ付ける。v3.2 で追加")
-ap.add_argument("--base", default="", help="出力の置き場所(既定は Drive の ARGUS_tottori)。v3.3 で追加")
+ap.add_argument("--base", default="", help="出力の置き場所(既定は Drive の ARGUS_osaka2018)。v3.3 で追加")
 args = ap.parse_args()
@@ -154,5 +176,5 @@
 if abs(args.min_mag - 2.0) > 1e-9 and args.tag == "":
-    raise SystemExit("[15_01c] STOP: --min-mag が 2.0 以外の時は --tag(例 _m15)を付ける(正本を上書きしないため)")
+    raise SystemExit("[21_20c] STOP: --min-mag が 2.0 以外の時は --tag(例 _m15)を付ける(正本を上書きしないため)")
 if args.tag == "" and (OUTD / "tottori_parsed_realpick.pt").exists() and not args.overwrite_canon:
-    raise SystemExit("[15_01c] STOP: 正本 tottori_parsed_realpick.pt が既にある。--tag を付けて回す"
+    raise SystemExit("[21_20c] STOP: 正本 tottori_parsed_realpick.pt が既にある。--tag を付けて回す"
                      "(正本を作り直す時だけ --overwrite-canon)")
@@ -255,3 +277,3 @@
     PN_MODEL.eval()
-    print("[15_01c] PhaseNet ('original') 読込完了")
+    print("[21_20c] PhaseNet ('original') 読込完了")
 
@@ -285,3 +307,3 @@
 # ================================================================ 入力読み込み
-print(f"[15_01c] JMAカタログ: {args.jma}")
+print(f"[21_20c] JMAカタログ: {args.jma}")
 import csv as _csv
@@ -308,5 +330,5 @@
 if args.max_events: cat = cat[:args.max_events]
-print(f"[15_01c] 対象イベント: {len(cat)} (M>={args.min_mag}, box={args.box}, "
+print(f"[21_20c] 対象イベント: {len(cat)} (M>={args.min_mag}, box={args.box}, "
       f"JST→UTC変換済み, h5窓引き={args.h5_time_base}基準, 欠損行スキップ {n_badrow})")
-if not cat: sys.exit("[15_01c] STOP: 対象イベント0件")
+if not cat: sys.exit("[21_20c] STOP: 対象イベント0件")
 
@@ -317,3 +339,3 @@
                                        float(row["elevation"]))
-print(f"[15_01c] 観測点: {len(sta_meta)}局 (stations.csv)")
+print(f"[21_20c] 観測点: {len(sta_meta)}局 ({Path(args.stations).name})")
 
@@ -328,3 +350,3 @@
     nan_frac = float(np.isnan(k_snr).mean())
-    print(f"[15_01c] K-NET参照: {len(kevs)}ev  absmax中央値={KNET_ABSMAX_REF:.2f}  "
+    print(f"[21_20c] K-NET参照: {len(kevs)}ev  absmax中央値={KNET_ABSMAX_REF:.2f}  "
           f"snr分布(NaN率{nan_frac:.1%}; 13_34rpではNaN→0) "
@@ -335,3 +357,3 @@
     KNET_ABSMAX_REF = float(args.knet_absmax_ref)
-    print(f"[15_01c] K-NET参照: --knet-absmax-ref={KNET_ABSMAX_REF} を使用 "
+    print(f"[21_20c] K-NET参照: --knet-absmax-ref={KNET_ABSMAX_REF} を使用 "
           f"(Mac実測 2026-10-15、キャッシュ本体は不要)")
@@ -345,3 +367,3 @@
 n_samp_h5 = int(H5.attrs.get("n_samples", 3000))
-print(f"[15_01c] h5: channel_order={ch_order_h5}  n_samples={n_samp_h5}")
+print(f"[21_20c] h5: channel_order={ch_order_h5}  n_samples={n_samp_h5}")
 st_raw = H5["stations"][:]
@@ -358,6 +380,6 @@
         ep_sorted, row_sorted = z["ep"], z["row"]
-    print(f"[15_01c] 窓索引をキャッシュから読込: {idx_path.name}" if _idx_ok
-          else f"[15_01c] 窓索引 {idx_path.name} は今の h5 のものでない(指紋が無いか違う)ので作り直す")
+    print(f"[21_20c] 窓索引をキャッシュから読込: {idx_path.name}" if _idx_ok
+          else f"[21_20c] 窓索引 {idx_path.name} は今の h5 のものでない(指紋が無いか違う)ので作り直す")
 if not _idx_ok:
-    print("[15_01c] 窓索引を構築中(初回のみ・数分)…")
+    print("[21_20c] 窓索引を構築中(初回のみ・数分)…")
     order = np.lexsort((ep_raw, st_arr))
@@ -369,3 +391,3 @@
              ep=ep_sorted, row=row_sorted, fp=np.array(_fp))
-    print(f"[15_01c] 窓索引を保存: {idx_path.name} ({len(sta_names)}局)")
+    print(f"[21_20c] 窓索引を保存: {idx_path.name} ({len(sta_names)}局)")
 del st_raw, ep_raw, st_arr
@@ -566,3 +588,3 @@
         ev["waveforms"] = ev["waveforms"] * amp_fac
-    print(f"[15_01c] 振幅整合: 鳥取absmax中央値 {med:.3e} → ×{amp_fac:.3e} で "
+    print(f"[21_20c] 振幅整合: 大阪absmax中央値 {med:.3e} → ×{amp_fac:.3e} で "
           f"K-NET中央値 {KNET_ABSMAX_REF:.2f} に一致(一括係数・相対振幅保存)")
@@ -576,3 +598,3 @@
 import hashlib
-rep = dict(script_version="15_01c v3.3", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
+rep = dict(script_version="21_20c v1 (computation identical to 15_01c v3.3)", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            args={k: str(v) for k, v in vars(args).items()}, stats=stats,
@@ -602,3 +624,3 @@
 print("\n" + "=" * 72)
-print(f"[15_01c] 完了: {out}")
+print(f"[21_20c] 完了: {out}")
 print(f"  採用 {stats['n_ev']} / 対象 {len(cat)}  (セグメント不足 {stats['no_seg']}, "
@@ -627,3 +649,3 @@
     ax[0].set_xlabel("Hypocentral distance (km)"); ax[0].set_ylabel("S–P (s)")
-    ax[0].set_title(f"Tottori 2026: measured S–P vs distance (n={len(SPn)})",
+    ax[0].set_title(f"Northern Osaka 2018: measured S–P vs distance (n={len(SPn)})",
                     fontsize=10.5)
@@ -638,3 +660,3 @@
     print(f"図: {PDFD}/15_01c_tottori_picks_qc{args.tag}.pdf")
-print(f"\n[15_01c] 出力全文+JSONを貼ってください。{out.name} をMacの SWIFT/data/"
-      f"{'ct2016_processed' if 'ct2016' in args.tag else 'tottori_processed'}/ にコピーしてください。")
+print(f"\n[21_20c] 出力全文+JSONを貼ってください。{out.name} をMacの SWIFT/data/"
+      f"{'osaka2018_processed' if 'osaka2018' in args.tag else 'tottori_processed'}/ にコピーしてください。")
```

## 21_20d_osaka2018_gclock2_picks.py(元: 21_04d_ct2016_gclock2_picks.py)

変わった行: −37 / +45(冒頭の説明を含む)

### 変えたことと理由
- 冒頭: 系列・派生元・何をするかの節の名前を変えた(「なぜ必要か」は 21_04d の時の記録のまま残すと明記)。
- 既定の `--cache`(..._osaka2018_m15.pt)・`--report`(data/21_20b_report.json)・`--base` の説明、表示の [21_20d]・[21_20b] の名前、
  出力の名前(data/21_20d_gclock2.json・PDF/21_20d_gclock2.pdf)、JSON の `script`、図の題と軸の年、FAIL の時の表示の文
  (「21_04 には進まない」→「どの条件の FAIL かで、事前登録 21_20 の扱いに従う」)。
- 変えていないもの: 計算・条件 (a)〜(f)・閾値・止め方(FAIL なら exit 1)・JSON の中身の形。
- 理由: 21_04d v1 は `--base`・`--cache`・`--report` で場所を渡せば大阪でも回る。しかし図の題が "Central Tottori 2016"、軸が "(2016)" のまま
  出るので、表示の誤りを残さないために表示だけを変えた(計算を変えずに済む最小の差)。

### 全ての差分

```diff
--- prereg/21_04d_ct2016_gclock2_picks.py
+++ osaka/21_20d_osaka2018_gclock2_picks.py
@@ -2,6 +2,13 @@
 # =============================================================================
-# Script : 21_04d_ct2016_gclock2_picks.py  (v1)
-#          [G-clock2: 15_01c が作ったキャッシュの PhaseNet の P の検測(全ての地震・全ての局)を使って、鳥取県中部 2016 の波形の
-#           時刻がずれていないかを確かめる。事前登録の変更の記録 02 で決めたゲートで、キャッシュを見る前に規則を固定する]
-# Project: ARGUS(新生)— 2 つ目の余震系列での確認(21_04)の入力の確かめ
+# Script : 21_20d_osaka2018_gclock2_picks.py  (v1)
+#          [G-clock2: 21_20c が作ったキャッシュの PhaseNet の P の検測(全ての地震・全ての局)を使って、大阪府北部 2018 の波形の
+#           時刻がずれていないかを確かめる。規則(a)〜(f)と閾値は 21_04d v1(21_04 の変更の記録 02)と同じ]
+# Project: ARGUS(新生)— 3 つ目の余震系列での確認(21_20)の入力の確かめ
+# 派生元 : 21_04d_ct2016_gclock2_picks.py v1(SHA-256 bc37a3c63e1b60cb7806498527caf7371f2ee8846555141a719592d5d2557de4)。
+#          計算・規則・閾値・止め方(FAIL なら exit code 1)は 1 字も変えていない。変えたのは次だけ(DIFF_LOG.md):
+#          既定のキャッシュ(..._osaka2018_m15.pt)と報告(data/21_20b_report.json)の場所、表示の [21_20d]、出力の名前
+#          (data/21_20d_gclock2.json・PDF/21_20d_gclock2.pdf)、JSON の script、図の題と軸の年。
+#          FAIL の時の扱いは、事前登録 21_20 の「G-clock2 の扱い」に先に決めてある((c) だけの FAIL と、それ以外の FAIL で違う)。
+#          この版は、どの条件で FAIL したかを JSON の pass_* に残すので、その扱いはこの出力だけで決まる。
+# 以下の「なぜ必要か」は 21_04d の時の記録(鳥取県中部 2016)のまま残す。
 #
@@ -15,3 +22,3 @@
 # 何をするか(G-clock2。規則は変更の記録 02 に書いたもので、このスクリプトはそれをそのまま計算する):
-#   1. キャッシュ(既定 data/tottori_processed/tottori_parsed_realpick_ct2016_m15.pt)の全ての地震・全ての局のうち、PhaseNet で
+#   1. キャッシュ(既定 data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt)の全ての地震・全ての局のうち、PhaseNet で
 #      P を測った検測(p_fallback = 0)について、残り r = tp_times − dist_km / 6.0 s を出す
@@ -24,13 +31,14 @@
 #      (d) 時間ごと(日本時間の 1 時間、検測 20 以上): |その時間の中央値 − 全体の中央値| ≤ 0.5 s(短い時間だけのずれを見る)
-#      (e) 21_04b の報告の G-clock の 4 地震(--report): それぞれ P を測った検測 4 以上で、|その地震の中央値 − 全体の中央値| ≤ 0.5 s
+#      (e) 21_20b の報告の G-clock の 4 地震(--report。既定 data/21_20b_report.json): それぞれ P を測った検測 4 以上で、|その地震の中央値 − 全体の中央値| ≤ 0.5 s
 #      (f) 局ごとの P を測った割合(現れた数 20 以上の局): 全ての局で、局の割合の中央値の 0.5 倍以上(時刻のずれた局が QC で落ちて
 #          (c) に入らない抜け道をふさぐ)
-#      止める: P を測った検測が 100 未満、検測 20 以上の日・局・時間のどれかが 0、21_04b の報告が無い
+#      止める: P を測った検測が 100 未満、検測 20 以上の日・局・時間のどれかが 0、21_20b の報告が無い
 #   3. 参考(判定には使わない): --ref-cache に鳥取 2026 のキャッシュを渡すと、同じ量を出す(許容が普通の値に比べて妥当かを見るため)。
-#   4. 出力: data/21_04d_gclock2.json(数・中央値・日ごと・局ごと・時間ごと・4 地震・測った割合・判定)/ PDF/21_04d_gclock2.pdf(日ごと・局ごとの中央値。白背景・英語・
-#      凡例は枠の外)。FAIL なら exit code 1(21_04 には進まない)。
+#   4. 出力: data/21_20d_gclock2.json(数・中央値・日ごと・局ごと・時間ごと・4 地震・測った割合・判定)/ PDF/21_20d_gclock2.pdf(日ごと・局ごとの中央値。白背景・英語・
+#      凡例は枠の外)。FAIL なら exit code 1(その後の扱いは事前登録 21_20 の「G-clock2 の扱い」)。
 #
-# Usage(Colab、15_01c の本番の後に):
-#   run([f'{SRC}/21_04d_ct2016_gclock2_picks.py', '--base', LO])
-#   (--cache で別のキャッシュ、--ref-cache で鳥取 2026 のキャッシュを指定できる)
+# Usage(Colab、21_20c の本番の後に。ノート 21_20_osaka2018_colab.ipynb の セル 12):
+#   !python /content/drive/MyDrive/ARGUS/src/21_20d_osaka2018_gclock2_picks.py --base /content/ARGUS_osaka2018 \
+#       --ref-cache /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt
+#   (--cache で別のキャッシュ、--ref-cache で鳥取 2026 のキャッシュを指定できる。--ref-cache は判定に使わない)
 # 止める条件(STOP): キャッシュが無い・上の「止める」
@@ -44,6 +52,6 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--base", required=True, help="ARGUS_ct2016 の場所(Colab のローカルなら /content/ARGUS_ct2016)")
-ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_ct2016_m15.pt")
+ap.add_argument("--base", required=True, help="ARGUS_osaka2018 の場所(Colab のローカルなら /content/ARGUS_osaka2018)")
+ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt")
 ap.add_argument("--ref-cache", default="", help="参考: 鳥取 2026 のキャッシュ(無くてよい)")
-ap.add_argument("--report", default="data/21_04b_report.json", help="21_04b の報告(G-clock の 4 地震を読む。--base からの場所)")
+ap.add_argument("--report", default="data/21_20b_report.json", help="21_20b の報告(G-clock の 4 地震を読む。--base からの場所)")
 a = ap.parse_args()
@@ -53,3 +61,3 @@
 
-def jst(ot):                                                     # キャッシュの origin_time は UTC(15_01c v3.3)。日本時間にする
+def jst(ot):                                                     # キャッシュの origin_time は UTC(15_01c v3.3・21_20c)。日本時間にする
     t = datetime.strptime(str(ot).replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
@@ -87,13 +95,13 @@
 cp = BASE / a.cache
-if not cp.exists(): sys.exit(f"[21_04d] STOP: キャッシュ {cp} が無い(15_01c の本番の後に回す)")
+if not cp.exists(): sys.exit(f"[21_20d] STOP: キャッシュ {cp} が無い(21_20c の本番の後に回す)")
 EVS, r, day, sta, hour, evi, seen = residuals(cp); nev = len(EVS)
-if len(r) < 100: sys.exit(f"[21_04d] STOP: P を測った検測が {len(r)}(100 未満)")
+if len(r) < 100: sys.exit(f"[21_20d] STOP: P を測った検測が {len(r)}(100 未満)")
 S = summarise(r, day, sta, hour)
 if S["n_days"] == 0 or S["n_stations"] == 0 or S["n_hours"] == 0:
-    sys.exit(f"[21_04d] STOP: 検測 {MIN_N} 以上の日・局・時間のどれかが 0(判定できない)")
+    sys.exit(f"[21_20d] STOP: 検測 {MIN_N} 以上の日・局・時間のどれかが 0(判定できない)")
 pa = abs(S["median_s"]) <= TOL_ALL; pd_ = S["max_day_dev_s"] <= TOL_DAY; ps = S["max_station_dev_s"] <= TOL_STA
 ph = S["max_hour_dev_s"] <= TOL_HOUR
-# (e) 21_04b の G-clock の 4 地震: その地震の P を測った検測(MIN_EV 以上)の中央値 − 全体の中央値
+# (e) 21_20b の G-clock の 4 地震: その地震の P を測った検測(MIN_EV 以上)の中央値 − 全体の中央値
 rp = BASE / a.report
-if not rp.exists(): sys.exit(f"[21_04d] STOP: 21_04b の報告 {rp} が無い")
+if not rp.exists(): sys.exit(f"[21_20d] STOP: 21_20b の報告 {rp} が無い")
 gc = json.load(open(rp))["gates"]["clock"]
@@ -117,6 +125,6 @@
 PASS = bool(pa and pd_ and ps and ph and pe and pf_)
-print(f"[21_04d] キャッシュ {cp.name}: 地震 {nev}・P を測った検測 {S['n']}(日は日本時間。キャッシュの UTC に 9 時間を足す)")
-print(f"[21_04d] (a) 全体: 残り(P の時刻 − 震源距離/6.0 km/s)の中央値 {S['median_s']:+.3f} s(四分位幅 {S['iqr_s']:.3f} s)  "
+print(f"[21_20d] キャッシュ {cp.name}: 地震 {nev}・P を測った検測 {S['n']}(日は日本時間。キャッシュの UTC に 9 時間を足す)")
+print(f"[21_20d] (a) 全体: 残り(P の時刻 − 震源距離/6.0 km/s)の中央値 {S['median_s']:+.3f} s(四分位幅 {S['iqr_s']:.3f} s)  "
       f"基準 |中央値| ≤ {TOL_ALL} s  {'PASS' if pa else 'FAIL'}")
-print(f"[21_04d] (b) 日ごと(検測 {MIN_N} 以上の日): 全体の中央値からの最大のずれ {S['max_day_dev_s']:.3f} s  基準 ≤ {TOL_DAY} s  "
+print(f"[21_20d] (b) 日ごと(検測 {MIN_N} 以上の日): 全体の中央値からの最大のずれ {S['max_day_dev_s']:.3f} s  基準 ≤ {TOL_DAY} s  "
       f"{'PASS' if pd_ else 'FAIL'}")
@@ -124,3 +132,3 @@
     print(f"      {d}: 検測 {v['n']:5d}  中央値 {v['median']:+.3f} s" + ("" if v["n"] >= MIN_N else "(少ないので判定に使わない)"))
-print(f"[21_04d] (c) 局ごと(検測 {MIN_N} 以上の局): 全体の中央値からの最大のずれ {S['max_station_dev_s']:.3f} s  基準 ≤ {TOL_STA} s  "
+print(f"[21_20d] (c) 局ごと(検測 {MIN_N} 以上の局): 全体の中央値からの最大のずれ {S['max_station_dev_s']:.3f} s  基準 ≤ {TOL_STA} s  "
       f"{'PASS' if ps else 'FAIL'}")
@@ -128,3 +136,3 @@
 for dv, s, v in worst: print(f"      ずれの大きい局 {s}: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
-print(f"[21_04d] (d) 時間ごと(日本時間の 1 時間・検測 {MIN_N} 以上、{S['n_hours']} 時間): 全体の中央値からの最大のずれ {S['max_hour_dev_s']:.3f} s  "
+print(f"[21_20d] (d) 時間ごと(日本時間の 1 時間・検測 {MIN_N} 以上、{S['n_hours']} 時間): 全体の中央値からの最大のずれ {S['max_hour_dev_s']:.3f} s  "
       f"基準 ≤ {TOL_HOUR} s  {'PASS' if ph else 'FAIL'}")
@@ -132,3 +140,3 @@
 for dv, k, v in worst_h: print(f"      ずれの大きい時間 {k} 時台: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
-print(f"[21_04d] (e) 21_04b の G-clock の 4 地震(P を測った検測 {MIN_EV} 以上、|地震の中央値 − 全体の中央値| ≤ {TOL_EV} s): {'PASS' if pe else 'FAIL'}")
+print(f"[21_20d] (e) 21_20b の G-clock の 4 地震(P を測った検測 {MIN_EV} 以上、|地震の中央値 − 全体の中央値| ≤ {TOL_EV} s): {'PASS' if pe else 'FAIL'}")
 for x in EVC:
@@ -137,3 +145,3 @@
           f"(STA/LTA の G-clock は {x['gclock_stalta_median_abs_s']:.2f} s)  {'PASS' if x['pass_'] else 'FAIL'}")
-print(f"[21_04d] (f) 局ごとの P を測った割合(現れた数 {MIN_N} 以上の {len(fr)} 局): 中央値 {mfr:.3f}、その {MIN_FRAC_RATIO} 倍未満の局 {len(low)}  "
+print(f"[21_20d] (f) 局ごとの P を測った割合(現れた数 {MIN_N} 以上の {len(fr)} 局): 中央値 {mfr:.3f}、その {MIN_FRAC_RATIO} 倍未満の局 {len(low)}  "
       f"{'PASS' if pf_ else 'FAIL'}")
@@ -143,7 +151,7 @@
     _, r2, d2, s2, h2, _, _ = residuals(Path(a.ref_cache)); REF = summarise(r2, d2, s2, h2)
-    print(f"[21_04d] 参考(鳥取 2026、判定には使わない): 検測 {REF['n']}  中央値 {REF['median_s']:+.3f} s  日ごとの最大のずれ "
+    print(f"[21_20d] 参考(鳥取 2026、判定には使わない): 検測 {REF['n']}  中央値 {REF['median_s']:+.3f} s  日ごとの最大のずれ "
           f"{REF['max_day_dev_s']:.3f} s  局ごとの最大のずれ {REF['max_station_dev_s']:.3f} s  時間ごとの最大のずれ {REF['max_hour_dev_s']:.3f} s")
-print(f"[21_04d] G-clock2: {'PASS' if PASS else 'FAIL'}")
+print(f"[21_20d] G-clock2: {'PASS' if PASS else 'FAIL'}")
 (BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
-json.dump(dict(script="21_04d_ct2016_gclock2_picks.py", version="v1", cache=str(cp), n_events=nev, vp_kms=VP,
+json.dump(dict(script="21_20d_osaka2018_gclock2_picks.py", version="v1", cache=str(cp), n_events=nev, vp_kms=VP,
                rule=dict(tol_all_s=TOL_ALL, tol_day_s=TOL_DAY, tol_station_s=TOL_STA, tol_hour_s=TOL_HOUR, tol_event_s=TOL_EV,
@@ -154,3 +162,3 @@
                pass_measured_frac=bool(pf_), gclock2_pass=PASS, reference_2026=REF),
-          open(BASE / "data" / "21_04d_gclock2.json", "w"), indent=1)
+          open(BASE / "data" / "21_20d_gclock2.json", "w"), indent=1)
 
@@ -167,4 +175,4 @@
 ax.set_xticks(range(len(dk))); ax.set_xticklabels([d[5:] for d in dk], rotation=60, fontsize=7); ax.set_xlim(-0.5, len(dk) - 0.5)
-ax.set_xlabel("JST date (2016)"); ax.set_ylabel("PhaseNet P time - distance / 6.0 km/s (s)")
-ax.set_title(f"(a) Central Tottori 2016, {S['n']} P picks: daily medians", fontsize=9); ax.grid(alpha=0.3)
+ax.set_xlabel("JST date (2018)"); ax.set_ylabel("PhaseNet P time - distance / 6.0 km/s (s)")
+ax.set_title(f"(a) Northern Osaka 2018, {S['n']} P picks: daily medians", fontsize=9); ax.grid(alpha=0.3)
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False, fontsize=8)
@@ -176,4 +184,4 @@
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), frameon=False, fontsize=8)
-fig.tight_layout(); fig.savefig(BASE / "PDF" / "21_04d_gclock2.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"[21_04d] 出力: {BASE / 'data' / '21_04d_gclock2.json'}、{BASE / 'PDF' / '21_04d_gclock2.pdf'}")
-if not PASS: sys.exit("[21_04d] STOP(G-clock2): 時刻のずれの疑い。21_04 には進まない(この出力を貼って相談)")
+fig.tight_layout(); fig.savefig(BASE / "PDF" / "21_20d_gclock2.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"[21_20d] 出力: {BASE / 'data' / '21_20d_gclock2.json'}、{BASE / 'PDF' / '21_20d_gclock2.pdf'}")
+if not PASS: sys.exit("[21_20d] STOP(G-clock2): 時刻のずれの疑い。どの条件の FAIL かで、事前登録 21_20 の扱いに従う(この出力を貼る)")
```

## 21_20e_osaka2018_station_pick_diagnose.py(元: 21_04e_ct2016_station_pick_diagnose.py)

変わった行: −16 / +21(冒頭の説明を含む)

### 変えたことと理由
- 冒頭: 系列・派生元・使う時(21_20d の (c) が FAIL の時だけ)を書いた。
- 既定の `--cache`、表示の [21_20e] と系列の名前、出力の名前(data/21_20e_station_picks.csv・PDF/21_20e_station_picks.pdf)、図の題。
- 変えていないもの: 計算(局ごとの残り・地震の大きさの 3 区分・|r − 全体| > 3 s の割合)。読むだけの記述で、判定に使わない。

### 全ての差分

```diff
--- prereg/21_04e_ct2016_station_pick_diagnose.py
+++ osaka/21_20e_osaka2018_station_pick_diagnose.py
@@ -2,6 +2,11 @@
 # =============================================================================
-# Script : 21_04e_ct2016_station_pick_diagnose.py  (v1)
-#          [G-clock2 の (c) 局ごとの確かめで FAIL になった局が、時計のずれか、検測の取り違え(別の地震や雑音の P を取った)かを
-#           調べる。読むだけで、キャッシュ・ゲート・規則は何も変えない]
-# Project: ARGUS(新生)— 2 つ目の余震系列での確認(21_04)の入力の確かめ
+# Script : 21_20e_osaka2018_station_pick_diagnose.py  (v1)
+#          [G-clock2(21_20d)の (c) 局ごとの確かめで FAIL になった局が、時計のずれか、検測の取り違えかを調べる。読むだけで、
+#           キャッシュ・ゲート・規則は何も変えない。判定には使わない記述]
+# Project: ARGUS(新生)— 3 つ目の余震系列での確認(21_20)の入力の確かめ
+# 派生元 : 21_04e_ct2016_station_pick_diagnose.py v1(SHA-256 2eca1779642deb3c8ea4433649862e73697b9b4f3d7deced7fae78a1392a9406)。
+#          計算は 1 字も変えていない。変えたのは、既定のキャッシュの場所・表示の [21_20e] と系列の名前・出力の名前
+#          (data/21_20e_station_picks.csv・PDF/21_20e_station_picks.pdf)・図の題だけ(DIFF_LOG.md)。
+#          事前登録 21_20 では、21_20d の (c) が FAIL した時だけ回す(記述だけ。結果で規則を変えない)。
+# 以下の「なぜ必要か」は 21_04e の時の記録(鳥取県中部 2016)のまま残す。
 #
@@ -21,3 +26,3 @@
 #   3. --ref-cache に鳥取 2026 のキャッシュを渡すと、同じ表を出す(21_02 で使った同じ作り方のキャッシュに、同じ形があるか)。
-#   4. 出力: data/21_04e_station_picks.csv と、PDF/21_04e_station_picks.pdf(局の距離に対する中央値。地震の大きさの 3 区分を色で。
+#   4. 出力: data/21_20e_station_picks.csv と、PDF/21_20e_station_picks.pdf(局の距離に対する中央値。地震の大きさの 3 区分を色で。
 #      白背景・英語・凡例は枠の外)
@@ -25,4 +30,4 @@
 # Usage(Colab):
-#   run([f'{SRC}/21_04e_ct2016_station_pick_diagnose.py', '--base', LO,
-#        '--ref-cache', '/content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt'])
+#   !python /content/drive/MyDrive/ARGUS/src/21_20e_osaka2018_station_pick_diagnose.py --base /content/ARGUS_osaka2018 \
+#       --ref-cache /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt
 # =============================================================================
@@ -35,3 +40,3 @@
 ap.add_argument("--base", required=True)
-ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_ct2016_m15.pt")
+ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt")
 ap.add_argument("--ref-cache", default="")
@@ -73,3 +78,3 @@
 def show(name, med, out):
-    print(f"\n[21_04e] ===== {name}: 全体の中央値 {med:+.3f} s(局 {len(out)}、本震からの距離の順)=====")
+    print(f"\n[21_20e] ===== {name}: 全体の中央値 {med:+.3f} s(局 {len(out)}、本震からの距離の順)=====")
     print("  局(緯度,経度)        本震から km  検測   中央値   ずれ   Mj<2 の中央値(数)   2≤Mj<3(数)        Mj≥3(数)         |r−全体|>3 s")
@@ -82,6 +87,6 @@
 cp = BASE / a.cache
-if not cp.exists(): sys.exit(f"[21_04e] STOP: {cp} が無い")
-med, out = table(cp); show("鳥取県中部 2016", med, out)
+if not cp.exists(): sys.exit(f"[21_20e] STOP: {cp} が無い")
+med, out = table(cp); show("大阪府北部 2018", med, out)
 (BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
-with open(BASE / "data" / "21_04e_station_picks.csv", "w", newline="") as fo:
+with open(BASE / "data" / "21_20e_station_picks.csv", "w", newline="") as fo:
     w = csv.DictWriter(fo, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
@@ -92,3 +97,3 @@
     else:
-        print(f"[21_04e] 注意: 参考のキャッシュ {a.ref_cache} が無いので飛ばした")
+        print(f"[21_20e] 注意: 参考のキャッシュ {a.ref_cache} が無いので飛ばした")
 
@@ -98,3 +103,3 @@
 plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
-panels = [("Central Tottori 2016", med, out)] + ([("West Tottori 2026 (reference)", *ref)] if ref else [])
+panels = [("Northern Osaka 2018", med, out)] + ([("West Tottori 2026 (reference)", *ref)] if ref else [])
 fig, axs = plt.subplots(1, len(panels), figsize=(6.2 * len(panels), 4.4), squeeze=False)
@@ -112,3 +117,3 @@
 axs[0][0].legend(loc="upper center", bbox_to_anchor=(0.5 * len(panels) + 0.05 * (len(panels) - 1), -0.15), ncol=5, frameon=False, fontsize=8)
-fig.tight_layout(); fig.savefig(BASE / "PDF" / "21_04e_station_picks.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"\n[21_04e] 出力: {BASE / 'data' / '21_04e_station_picks.csv'}、{BASE / 'PDF' / '21_04e_station_picks.pdf'}")
+fig.tight_layout(); fig.savefig(BASE / "PDF" / "21_20e_station_picks.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"\n[21_20e] 出力: {BASE / 'data' / '21_20e_station_picks.csv'}、{BASE / 'PDF' / '21_20e_station_picks.pdf'}")
```

## 21_20_osaka2018_similarity_confirmation.py(元: 21_04_ct2016_similarity_confirmation.py)

変わった行: −108 / +105(冒頭の説明を含む)

### 変えたことと理由
- 引数だけでは足りない理由: 21_04 v1 の引数は `--cache` と `--dev` だけで、本震の時刻・G-untouched の期間・出力の名前・限界の文が
  書き込まれている。大阪のキャッシュでは G-untouched で止まり、同じ ~/SWIFT で回すと 21_04 の opened.json があるので `_rerun` の名前になり、
  21_04 の 1 回だけの記録に大阪の行が足される。
- 冒頭を書き直した(派生元・なぜ編集が要ったか・変えたこと・仮説と判定・所要の参考値)。
- `--cache` の既定: data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt。
- `MAIN_UTC`: 2016-10-21 05:07:22.57 → 2018-06-17 22:58:30(気象庁の発表の 07:58 JST の 1 分の真ん中。秒までの値ではない)。
  確かめの規則(Mj ≥ 6.0・±60 s)は同じで、60 s は 1 分の全体を含む。
- `UNTOUCHED_UTC`: (2016-10-19, 2016-11-15) → (2018-06-15, 2018-07-12)。21_20a の期間を日の単位で含む。
- `LIMITS` の系列に依る 7 項目(系列・1 つだけ・G-spec のスクリプト名・キャッシュを作ったスクリプト・震源ファイル・除外の年・JSON の名前)。
  それ以外の項目は 1 字も同じ。
- 出力の名前(models/21_20_judgment.json・models/21_20_opened.json・data/21_20_per_event.csv・PDF/21_20_F1〜F3)、JSON の `script`・
  `sequence`・`verdict_rule` の系列の名前、表示の [21_20]、表示の系列の名前・本震の想定の文・G-phys の表示の文(「鳥取に」→「大阪に」)、図の題。
- 変えていないもの: 事前に固定した値の全て(TAUS・α・床・MIN_TEST・TOPK など)、計算、仮説と判定、全てのゲート、CSV の列、図の作り。
- 確かめ: 同じ作りもののキャッシュを、2016 の時刻(21_04 用)と 2018 の時刻(21_20 用)にずらして `--dev` で回し、
  data/21_04_per_event_dev.csv と data/21_20_per_event_dev.csv が、origin_time 以外の 108 列・20 地震で 1 字も違わないことを確かめた(下の「動作確認」)。

### 全ての差分

```diff
--- prereg/21_04_ct2016_similarity_confirmation.py
+++ osaka/21_20_osaka2018_similarity_confirmation.py
@@ -2,24 +2,31 @@
 # =============================================================================
-# Script : 21_04_ct2016_similarity_confirmation.py  (v1)
-#          [21_02 で合格した「波形が似た過去の地震 × 物理」(C3)と「似た地震の通り道の補正」(C4)を、手を付けていない
-#           2 つ目の余震系列(鳥取県中部 2016、本震 2016-10-21 14:07 JST・M6.6)で、21_02 と同じ規則のまま 1 回だけ確かめる]
-# Project: ARGUS(新生)— 論文の柱(2 つ目の系列での確認)。SSJ 2026 では「次の一手」として予告するだけ
+# Script : 21_20_osaka2018_similarity_confirmation.py  (v1)
+#          [21_02 で合格し、21_04(鳥取県中部 2016)でも確かめた「波形が似た過去の地震 × 物理」(C3)と「似た地震の通り道の補正」(C4)を、
+#           手を付けていない 3 つ目の余震系列(大阪府北部 2018、本震 2018-06-18 朝)で、21_02・21_04 と同じ規則のまま 1 回だけ確かめる]
+# Project: ARGUS(新生)— 論文の柱(3 つ目の系列での確認)
+# 派生元 : 21_04_ct2016_similarity_confirmation.py v1(SHA-256 0b2807843763b641a67e090407311d39c0204cdb7825577c6b86b07a0532908d)。
 #
-# なぜ必要か:
-#   21_02(鳥取 2026、使っていない 91 地震)は CONFIRMED だったが、仮説(τ = 2 s・C4)は同じ系列の 21_01 を見て決めた。
-#   それが後付けでないことを示すには、開発に一度も使っていない別の余震系列で、規則を 1 つも変えずに確かめるしかない。
+# なぜ編集が要ったか(引数だけでは足りない理由):
+#   21_04 v1 の引数は --cache と --dev だけで、次がスクリプトに書き込まれている。そのまま大阪のキャッシュで回すと止まるか、
+#   21_04 の 1 回だけの記録を壊す。
+#   - 本震の時刻(MAIN_UTC = 2016-10-21 05:07:22.57 UTC)と G-untouched の期間(2016-10-19〜2016-11-15 UTC) → 大阪のキャッシュでは STOP
+#   - 出力の名前(models/21_04_opened.json・models/21_04_judgment.json・data/21_04_per_event.csv・PDF/21_04_F*.pdf)
+#     → 同じ ~/SWIFT で回すと、21_04 の opened.json があるので _rerun の名前になり、21_04 の記録に大阪の行が足される
+#   - 限界の文・図の題・表示の系列の名前
 #
-# 21_02 v2 から変えたこと(これ以外は 1 字も変えていない。計算・既定値・仮説・判定の規則・図は 21_02 v2 と同じ):
-#   1. 入力: 鳥取県中部 2016 のキャッシュ(15_01c v3.3 を --min-mag 1.5 --tag _ct2016_m15 で作ったもの。21_04a の CSV と
-#      21_04b の h5 から。検測・QC・局の選び方は 21_02 のキャッシュと同じ 15_01c v3 の作り方)。
-#   2. 「使っていない地震」の決め方: この系列は ARGUS のどこでも使っていないので、21_02 の「正本(Mj ≥ 2.0)に無い」という
-#      条件は要らない。試験の地震は 21_02 と同じく「本震 + 72 時間より後の 1.5 ≤ Mj < 2.0」(Mj ≥ 2.0 は過去の地震の一覧に
-#      だけ入れる。21_02 と同じ)。21_02 の正本との照合(G-fresh)は、次の G-untouched に置き換えた:
-#      全ての地震の発生時刻が 2016-10-19 〜 2016-11-15(UTC)の中・Mj ≥ 1.5・本震が 1 つだけ(Mj ≥ 6.0 が 1 地震)。
-#   3. 本震の時刻の想定: 2016-10-21 05:07:22.57 UTC(気象庁の震源過程の資料名 2016102114072257 JST)、Mj ≥ 6.0、60 s 以内。
-#   4. 限界の文・表示名・出力の名前を 21_04 にした。図の題を「Central Tottori 2016」にした。
-#   5. 1 回だけの記録(models/21_04_opened.json)に、キャッシュの SHA-256 も書く(どのキャッシュで試験を開いたかを残すため。
-#      計算には効かない)。
+# 21_04 v1 から変えたこと(これ以外は 1 字も変えていない。計算・既定値・仮説・判定の規則・ゲート・図の作りは 21_04 v1 と同じ。DIFF_LOG.md):
+#   1. 入力の既定: data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt(21_20c を --min-mag 1.5 --tag _osaka2018_m15 で
+#      作ったもの。21_20c の検測・QC・組み立ては 15_01c v3.3 と同じ計算)。
+#   2. 本震の想定: MAIN_UTC = 2018-06-17 22:58:30 UTC。これは気象庁の発表の「2018-06-18 07 時 58 分(日本時間)」の 1 分の真ん中で、
+#      秒までの発生時刻ではない(秒までの値はこのスクリプトを書いた時点で確かめていないので書かない)。確かめの規則は 21_04 と同じ
+#      「Mj 最大の地震が Mj ≥ 6.0、MAIN_UTC から 60 s 以内」で、60 s はこの 1 分の全体を含む。要確認: 21_20a の表示の本震の
+#      時刻(日本時間)がこの 1 分に入ること(21_20a はそうでなければ止まる)。
+#   3. G-untouched: 全ての地震の発生時刻が 2018-06-15 〜 2018-07-12(UTC)の中・Mj ≥ 1.5・Mj ≥ 6.0 が 1 地震だけ。期間は 21_20a の
+#      期間(本震の 2 日前〜24 日後、日本時間)を日の単位で含むように取った(21_04 と同じ作り方)。
+#   4. 出力の名前を 21_20 にした: models/21_20_judgment.json / models/21_20_opened.json / data/21_20_per_event.csv /
+#      PDF/21_20_F1_error_vs_tau.pdf / PDF/21_20_F2_paired_difference.pdf / PDF/21_20_F3_similarity_vs_separation.pdf
+#      (--dev では _dev、2 回目以降は _rerun_<UTC の時刻>。CSV の列は 21_04 と同じ)。
+#   5. 限界の文(LIMITS の最初の 7 項目)・表示・図の題・JSON の sequence と verdict_rule の系列の名前を大阪府北部 2018 にした。
 #
-# 事前に固定した仮説と判定(21_02 v2 と同じ。この版の SHA-256 を、データを開く前に事前登録の記録に書く):
+# 事前に固定した仮説と判定(21_02 v2・21_04 v1 と同じ。この版の SHA-256 を、データを開く前に事前登録の記録 21_20 に書く):
 #   BEST(τ) = AI を使わない 9 つの方法(M0r・Mp10・M1・M2・M3r・M5・M5f・M6p・M6r)のうち、評価する全ての地震で値がある
@@ -31,28 +38,16 @@
 #   評価できる試験の地震が 30 未満なら INCONCLUSIVE。それ以外の τ・方法・感度は記述だけ。
-#   方法の中身(17_02・21_01 v3・21_02 v2 と同じ): 2–8 Hz の因果フィルタ、P − 0.2 s から τ − 0.01 s までの窓(最長 3 s)、
-#   ±0.1 s のずれ、3 成分をつないだコサイン類似度、S_ij = Σ max(c, 0) / n_i、上位 10 地震(S > 0 が 5 未満なら M6r)、
-#   過去の地震の一覧は各地震の 1 時間以上前、C4 の局の補正は上位の似た地震の走時の残りの中央値(3 地震以上で持つ局だけ)。
-#   pool(本震 + 72 時間まで、全ての Mj)で速度・局の補正・b・KDE の帯域・格子・固定の深さを決める。
-#   ゲート(G-split・G-lib・G-causal・G-phys)と 1 回だけの記録・dev も 21_02 と同じ。
+#   方法の中身・pool・ゲート(G-split・G-lib・G-causal・G-phys)と 1 回だけの記録・dev も 21_04 v1 と同じ。
 #
-# 限界(結果を読むときに必ず添える。表示と JSON にも英語で書く):
-#   - 2 つ目の系列は 1 つだけ(鳥取県中部 2016)。仮説は 1 つ目の系列(鳥取 2026)を見て決めた。この系列で規則を変えたら
-#     後付けになる
-#   - 観測点は Hi-net(0101)だけで、鳥取 2026 の 50 局(Hi-net のほか京大防災研・気象庁などを含む)とは種類と並びが違う。
-#     候補は今の NIED の一覧から選んだ(2016 年にあって今は無い局は入らない)
-#   - 波形は地震の前後だけを取り、鳥取 2026 の h5 と同じ形(30 秒窓・窓ごと成分ごとの z-score)にした。鳥取 2026 の h5 を
-#     作る時に z-score の前にフィルタをかけたかは記録が無い(2016 はかけていない。21_04b の G-spec で比べた)
-#   - 震源は気象庁の確定値の h2016(鳥取 2026 は一元化の震源)。正解も過去の地震の位置も気象庁の震源
-#   - 21_02 と同じ限界(オフラインの PhaseNet・最大 24 局・未着の局の情報は使わない・窓全体の平均と 30 秒窓の z-score・
-#     検測と通信の遅れなし・試験は小さい地震・C4 の得の一部は気象庁の枠に合わせた効果でありうる)
+# 限界(結果を読むときに必ず添える。表示と JSON にも英語で書く): LIMITS を見る。21_04 の限界のうち系列に依るものを大阪府北部 2018 に
+#   置き換え、それ以外は同じ文。G-clock2(21_20d)の (c) が FAIL だった時は、事前登録 21_20 の決まった印を結果に付ける
+#   (このスクリプトは G-clock2 の結果を読まない)。
 #
-# Usage : (先に Colab のノート 21_04_ct2016_colab.ipynb のセル 1〜11 で、tottori_parsed_realpick_ct2016_m15.pt を作り、
-#          Mac の ~/SWIFT/data/ct2016_processed/ にコピーする)
-#         cd ~/SWIFT && uv run python src/21_04_ct2016_similarity_confirmation.py --dev   (動作確認。試験を開かない)
-#         cd ~/SWIFT && uv run python src/21_04_ct2016_similarity_confirmation.py         (本番。1 回だけ)
-# Output: models/21_04_judgment.json / models/21_04_opened.json / data/21_04_per_event.csv /
-#         PDF/21_04_F1_error_vs_tau.pdf / PDF/21_04_F2_paired_difference.pdf / PDF/21_04_F3_similarity_vs_separation.pdf
-#         (--dev では _dev、2 回目以降は _rerun_<UTC の時刻>)。CSV の列は 21_02 と同じ
-# 所要  : CPU のみ。時間は(1 地震あたりの時間)×(試験の地震の数)で、過去の地震の数にも比例する。鳥取 2026 より地震が多い
-#         見込みなので長くなりうる。最初の 10 地震の後に残りの見込み時間を表示する(Mac を眠らせない: caffeinate -i を前に付ける)
+# Usage : (先に Colab のノート 21_20_osaka2018_colab.ipynb のセル 1〜12 で tottori_parsed_realpick_osaka2018_m15.pt を作って
+#          G-clock2 を確かめ、Mac の ~/SWIFT/data/osaka2018_processed/ にコピーする。手順は COLAB_STEPS_JA.md)
+#         cd ~/SWIFT && caffeinate -i uv run python src/21_20_osaka2018_similarity_confirmation.py --dev   (動作確認。試験を開かない)
+#         cd ~/SWIFT && caffeinate -i uv run python src/21_20_osaka2018_similarity_confirmation.py         (本番。1 回だけ)
+# Output: models/21_20_judgment.json / models/21_20_opened.json / data/21_20_per_event.csv /
+#         PDF/21_20_F1_error_vs_tau.pdf / PDF/21_20_F2_paired_difference.pdf / PDF/21_20_F3_similarity_vs_separation.pdf
+# 所要  : CPU のみ。(1 地震あたりの時間)×(試験の地震の数)で、過去の地震の数にも比例する。参考: 21_04 の本番は 1,894 地震の
+#         キャッシュ・試験 307 地震で 1,564 s(models/21_04_judgment.json の runtime_s)。最初の 10 地震の後に残りの見込みを表示する
 # =============================================================================
@@ -67,3 +62,3 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--cache", default="data/ct2016_processed/tottori_parsed_realpick_ct2016_m15.pt", help="15_01c v3.3 の鳥取県中部 2016 の M>=1.5 版")
+ap.add_argument("--cache", default="data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt", help="21_20c(15_01c v3.3 と同じ計算)の大阪府北部 2018 の M>=1.5 版")
 ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(pool の最後の新しい地震 20 個を代わりに使う)")
@@ -89,7 +84,8 @@
 NBOOT, SEED, N_DEV, N_GATE = 2000, 12, 20, 5
-MAIN_UTC = dt.datetime(2016, 10, 21, 5, 7, 22, 570000)
-UNTOUCHED_UTC = (dt.datetime(2016, 10, 19), dt.datetime(2016, 11, 15))   # G-untouched: 21_04a の期間を含む
-LIMITS = ["second sequence: Central Tottori 2016 (mainshock 2016-10-21 05:07 UTC, Mj 6.6), never used in ARGUS development; "
-          "the hypotheses were fixed on West Tottori 2026 (21_01/21_02) and are applied here unchanged",
-          "one second sequence only",
+MAIN_UTC = dt.datetime(2018, 6, 17, 22, 58, 30)   # 21_20: 気象庁の発表の 07:58 JST の 1 分の真ん中(秒までの値ではない。±60 s でこの 1 分を含む)。要確認
+UNTOUCHED_UTC = (dt.datetime(2018, 6, 15), dt.datetime(2018, 7, 12))     # G-untouched: 21_20a の期間(本震の 2 日前〜24 日後)を含む
+LIMITS = ["third sequence: Northern Osaka 2018 (mainshock 2018-06-18, 07:58 JST; origin time and Mj are those of the JMA catalogue, "
+          "see 21_20a's JSON), never used in ARGUS development; the hypotheses were fixed on West Tottori 2026 (21_01/21_02), "
+          "tested on Central Tottori 2016 (21_04, run with a documented deviation) and are applied here unchanged",
+          "one third sequence only",
           "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
@@ -98,10 +94,11 @@
           "per-window per-component z-score, JST epoch); whether a filter was applied before the z-score in the 2026 h5 is not recorded "
-          "(none here; compared in 21_04b G-spec)",
-          "the cache was built by 15_01c v3.3 (picking, QC and assembly identical to v3; only the window-index file name and output "
-          "folder changed)",
-          "catalogue: JMA final hypocentres (h2016; West Tottori 2026 used the unified catalogue); past-event locations are JMA "
+          "(none here; compared in 21_20b G-spec)",
+          "the cache was built by 21_20c, whose picking, QC and assembly are identical to 15_01c v3.3 (itself identical to v3 except "
+          "the window-index file name and output folder); 21_20c changed only labels, defaults and required arguments",
+          "catalogue: JMA hypocentres from h2018 (whether h2018 is the final stage is to be confirmed; West Tottori 2026 used the "
+          "unified catalogue); past-event locations are JMA "
           "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
-          "the 2016 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
+          "the 2018 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
           "events; whether the 2026 catalogue excluded them is not recorded. Manual and automatic hypocentres are mixed (per-flag "
-          "counts in 21_04a's JSON)",
+          "counts in 21_20a's JSON)",
           "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); the 2026 station list's "
@@ -134,3 +131,3 @@
 SELF_SHA = sha256(Path(__file__))
-print(f"[21_04] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
+print(f"[21_20] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
       f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")
@@ -139,3 +136,3 @@
 CP = ROOT / a.cache
-if not CP.exists(): raise SystemExit(f"[21_04] STOP: {a.cache} が無い(ノート 21_04_ct2016_colab.ipynb のセル 11 で作った tottori_parsed_realpick_ct2016_m15.pt を data/ct2016_processed/ に置く)")
+if not CP.exists(): raise SystemExit(f"[21_20] STOP: {a.cache} が無い(ノート 21_20_osaka2018_colab.ipynb のセル 11 で作った tottori_parsed_realpick_osaka2018_m15.pt を data/osaka2018_processed/ に置く)")
 EVS = torch.load(CP, map_location="cpu", weights_only=False)
@@ -144,7 +141,7 @@
     miss = [k for k in need if k not in e]
-    if miss: raise SystemExit(f"[21_04] STOP: キャッシュの地震に {miss} が無い(15_01c v3.3 の出力か確かめる)")
+    if miss: raise SystemExit(f"[21_20] STOP: キャッシュの地震に {miss} が無い(21_20c の出力か確かめる)")
 for e in EVS:
     w_ = np.asarray(e["waveforms"])
-    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_04] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
-    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_04] STOP: {e['origin_time']} の波形に NaN か無限大")
+    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_20] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
+    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_20] STOP: {e['origin_time']} の波形に NaN か無限大")
 def to_ns(o):
@@ -156,3 +153,3 @@
     except Exception:
-        raise SystemExit(f"[21_04] STOP: origin_time {o!r} を時刻として読めない")
+        raise SystemExit(f"[21_20] STOP: origin_time {o!r} を時刻として読めない")
 OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
@@ -164,4 +161,4 @@
 if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
-    raise SystemExit("[21_04] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
-if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[21_04] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
+    raise SystemExit("[21_20] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
+if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[21_20] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
 # G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
@@ -172,10 +169,10 @@
 n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
-print(f"[21_04] 入力: 鳥取県中部 2016 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
+print(f"[21_20] 入力: 大阪府北部 2018 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
       f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
-print(f"[21_04] G-untouched: 期間 2016-10-19〜2016-11-15(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
+print(f"[21_20] G-untouched: 期間 2018-06-15〜2018-07-12(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
       + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
-if n_out != 0 or n_big != 1: raise SystemExit("[21_04] STOP(G-untouched): 鳥取県中部 2016 のキャッシュに見えない(この行を貼って相談)")
+if n_out != 0 or n_big != 1: raise SystemExit("[21_20] STOP(G-untouched): 大阪府北部 2018 のキャッシュに見えない(この行を貼って相談)")
 im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
 if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
-    raise SystemExit(f"[21_04] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj 6.6・2016-10-21 05:07:22.57 UTC)")
+    raise SystemExit(f"[21_20] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2018-06-17 22:58 UTC の 1 分 ± 60 s。気象庁の発表の 07:58 JST)")
 CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
@@ -183,5 +180,5 @@
 if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
-    raise SystemExit("[21_04] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
-print(f"[21_04] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
-print(f"[21_04] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
+    raise SystemExit("[21_20] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
+print(f"[21_20] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
+print(f"[21_20] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
       f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")
@@ -196,3 +193,3 @@
     kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
-    if len(set(kk)) != n: raise SystemExit(f"[21_04] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
+    if len(set(kk)) != n: raise SystemExit(f"[21_20] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
 HASP = ~np.isnan(TFIRST)
@@ -208,6 +205,6 @@
 EX, EY = to_xy(SRC[:, 0], SRC[:, 1])
-print(f"[21_04] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
+print(f"[21_20] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
 EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
-if len(EVAL) == 0: raise SystemExit("[21_04] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
-if a.dev: print(f"[21_04] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
+if len(EVAL) == 0: raise SystemExit("[21_20] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
+if a.dev: print(f"[21_20] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                 "(較正にも入っているので値は楽観的)")
@@ -215,3 +212,3 @@
 # ---------------------------------------------------------------- 1 回だけの記録(本番は、試験の地震の結果を計算する前に書く)
-OPEN = ROOT / "models/21_04_opened.json"
+OPEN = ROOT / "models/21_20_opened.json"
 SUF = "_dev" if a.dev else ""
@@ -222,5 +219,5 @@
 if not a.dev:
-    if OPEN.exists() or (ROOT / "models/21_04_judgment.json").exists():
+    if OPEN.exists() or (ROOT / "models/21_20_judgment.json").exists():
         SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
-        print(f"[21_04] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
+        print(f"[21_20] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
     log_open("opened")
@@ -293,3 +290,3 @@
 LAP_B = float(np.median(np.abs(r1)) / np.log(2.0))
-print(f"[21_04] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
+print(f"[21_20] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
       f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")
@@ -304,3 +301,3 @@
 XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
-print(f"[21_04] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
+print(f"[21_20] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
       f"  固定の深さ {ZDEF:.1f} km")
@@ -340,3 +337,3 @@
 lls = {h: loo_ll(h) for h in HS}; KDE_H = max(lls, key=lls.get)
-print(f"[21_04] KDE の帯域(pool の一つ抜き): {KDE_H} km")
+print(f"[21_20] KDE の帯域(pool の一つ抜き): {KDE_H} km")
 def log_prior(nodes, mem):
@@ -368,3 +365,3 @@
     lib = np.where((OTNS <= OTNS[ie] - int(buffer_h * 3600e9)) & HASP)[0]
-    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_04] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
+    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_20] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
     return lib
@@ -444,3 +441,3 @@
     top = lib[np.argsort(-S, kind="stable")[:min(k, pos)]]
-    if ie is not None and ie in top: stop("[21_04] STOP: 自分自身が似た地震の上位に入っている")
+    if ie is not None and ie in top: stop("[21_20] STOP: 自分自身が似た地震の上位に入っている")
     out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
@@ -461,3 +458,3 @@
     lib = library(ie); libb = library(ie, BUFFER_SENS_H)
-    if not np.array_equal(libb[:len(lib)], lib): stop("[21_04] STOP: 過去の一覧の並びがおかしい")
+    if not np.array_equal(libb[:len(lib)], lib): stop("[21_20] STOP: 過去の一覧の並びがおかしい")
     p0 = FIRST[ie]
@@ -504,4 +501,4 @@
 if NT < MIN_TEST and not a.dev:
-    print(f"[21_04] 判定(事前宣言、H1): INCONCLUSIVE(評価できる試験の地震 {NT} < {MIN_TEST})")
-    json.dump(dict(script="21_04_ct2016_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, verdict="INCONCLUSIVE",
+    print(f"[21_20] 判定(事前宣言、H1): INCONCLUSIVE(評価できる試験の地震 {NT} < {MIN_TEST})")
+    json.dump(dict(script="21_20_osaka2018_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, verdict="INCONCLUSIVE",
                    utc=utcnow(), suffix=SUF, cache=a.cache, cache_sha256=sha256(CP), n_test=int(len(test_idx)),
@@ -509,3 +506,3 @@
                    n_mj2_library_only=n_extra2), limits=LIMITS),
-              open(ROOT / f"models/21_04_judgment{SUF}.json", "w"), indent=1)
+              open(ROOT / f"models/21_20_judgment{SUF}.json", "w"), indent=1)
     log_open("completed: INCONCLUSIVE"); raise SystemExit(0)
@@ -521,3 +518,3 @@
     except BaseException as ex:
-        stop(f"[21_04] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
+        stop(f"[21_20] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
     for m in METH: P[m][ii] = R[m]
@@ -532,3 +529,3 @@
 gate_ev = [ii for ii in range(NT) if NI[ii, TAUS.index(1.0)] > 0][:N_GATE]
-if len(gate_ev) < 3: stop(f"[21_04] STOP(G-causal): τ = 1 s で似ている度合いが測れた地震が {len(gate_ev)} しかなく、確かめられない")
+if len(gate_ev) < 3: stop(f"[21_20] STOP(G-causal): τ = 1 s で似ている度合いが測れた地震が {len(gate_ev)} しかなく、確かめられない")
 gc_max, gc_n, pos_ctrl = 0.0, 0, None
@@ -564,3 +561,3 @@
 shared = [p for p in picks_of(ie, 1.0) if n_avail(1.0, p[4]) >= MINW_N and any(p[0] in filt_cached(j, BAND) for j in lib0)]
-if not shared: stop("[21_04] STOP(G-causal): 陽性対照に使える局が無い(この行を貼って相談)")
+if not shared: stop("[21_20] STOP(G-causal): 陽性対照に使える局が無い(この行を貼って相談)")
 pc = shared[0]; e2 = dict(orig); W = np.array(np.asarray(orig["waveforms"], float))
@@ -571,5 +568,5 @@
 pos_ctrl = float(np.max(np.abs(S1 - S0))) if len(S0) else 0.0
-print(f"[21_04] G-causal({len(gate_ev)} 地震 × τ = 0.5・1・2・3 s、未来の波形と検測を置き換えた時の最大の差): {gc_max:.3g}  "
+print(f"[21_20] G-causal({len(gate_ev)} 地震 × τ = 0.5・1・2・3 s、未来の波形と検測を置き換えた時の最大の差): {gc_max:.3g}  "
       f"陽性対照(窓の最後の点を変えた時の S の差): {pos_ctrl:.3g}  " + ("PASS" if (gc_max == 0.0 and pos_ctrl > 0) else "FAIL"))
-if not (gc_max == 0.0 and pos_ctrl > 0): stop("[21_04] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")
+if not (gc_max == 0.0 and pos_ctrl > 0): stop("[21_20] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")
 
@@ -600,5 +597,5 @@
 phys_inf = SUMM["M5"]["inf"]["median_km"]
-print(f"[21_04] G-phys(τ = ∞ の M5 の中央値 ≤ 0.5 km): {'—' if phys_inf is None else f'{phys_inf:.3f}'} km  " + ("PASS" if phys_inf is not None and phys_inf <= 0.5 else "FAIL")
+print(f"[21_20] G-phys(τ = ∞ の M5 の中央値 ≤ 0.5 km): {'—' if phys_inf is None else f'{phys_inf:.3f}'} km  " + ("PASS" if phys_inf is not None and phys_inf <= 0.5 else "FAIL")
       + "(参考: 15_12 は 0.13 km、分け方が違う)")
-if not (phys_inf is not None and phys_inf <= 0.5): stop("[21_04] STOP(G-phys): 物理を鳥取に正しく移せていない可能性(この行を貼って相談)")
+if not (phys_inf is not None and phys_inf <= 0.5): stop("[21_20] STOP(G-phys): 物理を大阪に正しく移せていない可能性(この行を貼って相談)")
 def judge(meth, t, alpha):
@@ -634,3 +631,3 @@
 def fp(p): return "—" if p is None else f"{p:.2g}"
-print(f"\n[21_04] ===== 水平誤差の中央値 km [95% 区間](評価 {NT} 地震{'、dev(楽観的)' if a.dev else ''}) =====")
+print(f"\n[21_20] ===== 水平誤差の中央値 km [95% 区間](評価 {NT} 地震{'、dev(楽観的)' if a.dev else ''}) =====")
 print("  方法           " + "".join(f"{('τ=' + t + ' s') if t != 'inf' else '全検測':>24}" for t in TL))
@@ -652,3 +649,3 @@
       "(全検測でも C4 が物理より良いなら、その分は早さではなく気象庁の震源の枠に合わせた効果の可能性)")
-print(f"\n[21_04] ===== 事前宣言の判定 =====")
+print(f"\n[21_20] ===== 事前宣言の判定 =====")
 for name, h in HYP.items():
@@ -658,4 +655,4 @@
           f"→ {'勝ち' if h['win'] else '勝ちなし'}")
-print(f"\n[21_04] 判定(事前宣言、H1): {VERDICT}")
-print("[21_04] 限界: " + " / ".join(LIMITS))
+print(f"\n[21_20] 判定(事前宣言、H1): {VERDICT}")
+print("[21_20] 限界: " + " / ".join(LIMITS))
 
@@ -671,3 +668,3 @@
 CM = BASE + NEW + SENSN + ALLP
-with open(ROOT / f"data/21_04_per_event{SUF}.csv", "w", newline="") as f:
+with open(ROOT / f"data/21_20_per_event{SUF}.csv", "w", newline="") as f:
     w = csv.writer(f)
@@ -683,4 +680,4 @@
                       for j in (range(len(TL)) if m in BASE else [ji] if m in ALLP else range(len(TAUS)))])
-out = dict(script="21_04_ct2016_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
-           sequence="Central Tottori 2016", suffix=SUF, cache=a.cache, cache_sha256=sha256(CP),
+out = dict(script="21_20_osaka2018_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
+           sequence="Northern Osaka 2018", suffix=SUF, cache=a.cache, cache_sha256=sha256(CP),
            n_fresh=int(FRESH.sum()), n_events=NE, n_pool=int(len(pool_idx)), n_test=int(len(test_idx)),
@@ -705,5 +702,5 @@
                         "fewer than 30 evaluated events. H2: C4 at tau = 2 s, H3: C3 at tau = 0.5 s, each alpha 0.005 (secondary). "
-                        "Test events: 1.5 <= Mj < 2.0 events later than mainshock + 72 h (Central Tottori 2016; same rule as 21_02 v2)",
+                        "Test events: 1.5 <= Mj < 2.0 events later than mainshock + 72 h (Northern Osaka 2018; same rule as 21_02 v2 and 21_04 v1)",
            limits=LIMITS, runtime_s=time.time() - T0)
-json.dump(clean(out), open(ROOT / f"models/21_04_judgment{SUF}.json", "w"), indent=1)
+json.dump(clean(out), open(ROOT / f"models/21_20_judgment{SUF}.json", "w"), indent=1)
 if not a.dev: log_open("completed: " + VERDICT)
@@ -738,6 +735,6 @@
 ax.set_xlabel("Time since first P pick, tau (s)"); ax.set_ylabel("Median epicentral error vs JMA (km)")
-ax.set_title(f"Central Tottori 2016, {'DEV (pool events, optimistic)' if a.dev else 'test events'}, n = {NT}; shading = 95% bootstrap CI",
+ax.set_title(f"Northern Osaka 2018, {'DEV (pool events, optimistic)' if a.dev else 'test events'}, n = {NT}; shading = 95% bootstrap CI",
              fontsize=10)
 ax.grid(alpha=0.3, which="both"); ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_04_F1_error_vs_tau{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_20_F1_error_vs_tau{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
 
@@ -757,3 +754,3 @@
 fig.legend(h_, l_, loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=2, fontsize=8, frameon=False)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_04_F2_paired_difference{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_20_F2_paired_difference{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
 
@@ -767,4 +764,4 @@
 ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_04_F3_similarity_vs_separation{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"[21_04] 出力: models/21_04_judgment{SUF}.json, data/21_04_per_event{SUF}.csv, PDF/21_04_F1〜F3{SUF}.pdf"
-      + ("" if a.dev else ", models/21_04_opened.json") + f"  ({time.time()-T0:.0f} s)")
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_20_F3_similarity_vs_separation{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"[21_20] 出力: models/21_20_judgment{SUF}.json, data/21_20_per_event{SUF}.csv, PDF/21_20_F1〜F3{SUF}.pdf"
+      + ("" if a.dev else ", models/21_20_opened.json") + f"  ({time.time()-T0:.0f} s)")
```

## 21_20f_osaka2018_learned_test.py(元: 21_06b_ct2016_learned_test.py)

変わった行: −126 / +119(冒頭の説明を含む)

### 変えたことと理由
- 引数だけでは足りない理由: 21_06b v1 の引数は `--cache`・`--dev`・`--train-json` だけで、本震の時刻・G-untouched の期間・比べる相手の
  21_04 の出力の名前・自分の出力の名前が書き込まれている。
- 冒頭を書き直した。`--cache` の既定、`MAIN_UTC`・`UNTOUCHED_UTC`・`LIMITS` の系列に依る項目は 21_20 と同じ置き換え。
- 比べる相手と順番の確かめ: data/21_04_per_event(_dev).csv → data/21_20_per_event(_dev).csv、models/21_04_judgment.json →
  models/21_20_judgment.json、models/21_04_opened.json → models/21_20_opened.json(変数名 J04・O4 はそのまま)。
- 出力の名前(models/21_20f_judgment.json・models/21_20f_opened.json・data/21_20f_per_event.csv・PDF/21_20f_F1_learned_test.pdf)、
  JSON の `script`、表示の [21_20f]、表示と限界の文の系列の名前(「2016 の pool」→「2018 の pool」を含む)、図の題。
- 変えていないもの: 21_06 FEATURES の印の間(1 字も変えていない。印の間の SHA-256 は
  9905420e546da69e0e3426bccb1f5e962c04d42013e27b506811f13e402ed0b5 で、models/21_06a_train.json の feature_block_sha256 と同じ)、
  凍結したモデルとその確かめ(G-feat・G-model・scikit-learn と numpy の版)、仮説と判定、G-same、計算。
- 確かめ: 作りもののキャッシュで `--dev` を回し、G-feat と G-model(モデルの SHA-256)を通って、scikit-learn の版の確かめ(学習時 1.8.0、
  この環境 1.9.1)で止まることを確かめた。それより後(G-same・L3・L4)は、この環境では回せなかった(学習の行のファイルが入力に無く、
  版も違う)。Mac の M4(dev)で確かめる。

### 全ての差分

```diff
--- prereg/21_06b_ct2016_learned_test.py
+++ osaka/21_20f_osaka2018_learned_test.py
@@ -2,34 +2,28 @@
 # =============================================================================
-# Script : 21_06b_ct2016_learned_test.py  (v1)
-#          [学習型 ARGUS の試験: 鳥取 2026 で学習して凍結した「似た地震の選び方」(21_06a)を、手を付けていない鳥取県中部 2016 で
-#           1 回だけ試す。位置は C3・C4 と同じ物理の計算で決める(AI は物理の部品)]
-# Project: ARGUS(新生)— 学習した部品が別の余震系列でも物理だけより良いか、人が決めた選び方(C4)より良いか
+# Script : 21_20f_osaka2018_learned_test.py  (v1)
+#          [学習型 ARGUS の 3 つ目の系列での試験: 鳥取 2026 で学習して凍結した「似た地震の選び方」(21_06a のモデル)を、学び直さずに、
+#           手を付けていない大阪府北部 2018 で 1 回だけ試す。位置は C3・C4 と同じ物理の計算で決める(AI は物理の部品)]
+# Project: ARGUS(新生)— 学習した部品が 3 つ目の余震系列でも物理だけより良いか
+# 派生元 : 21_06b_ct2016_learned_test.py v1(SHA-256 442c411945f288cfff7f14490ee9826ffcfe055e5a79cc2af0c39fe93cb5bfea)。
 #
-# 順番(事前登録の記録 21_06_preregistration.md に書く):
-#   1. 21_06a を鳥取 2026 で回し、モデルを凍結する(SHA-256 が出る)
-#   2. 21_06a・21_06b・モデルの SHA-256 を事前登録の記録に書いて push する(2016 の試験を開く前)
-#   3. 21_04 の本番(2016 の試験)を回す → 4. その後でこの 21_06b の本番を回す(21_04 の CSV を使う)
+# なぜ編集が要ったか: 21_06b v1 の引数は --cache・--dev・--train-json だけで、本震の時刻・G-untouched の期間・比べる相手の 21_04 の
+#   出力の名前(data/21_04_per_event.csv・models/21_04_judgment.json・models/21_04_opened.json)・自分の出力の名前
+#   (models/21_06b_*.json など)がスクリプトに書き込まれている。そのまま回すと大阪のキャッシュで STOP するか、21_06b の記録を壊す。
 #
-# 何をするか:
-#   1. 21_04 v1 と同じ入力・ゲート(G-untouched など)・較正・評価の地震を、21_04 のコードをそのまま写して作る(1. 入力〜6. 波形の
-#      似ている度合い)。1 回だけの記録は models/21_06b_opened.json(2 回目以降は _rerun_<UTC> の名前に書く)。
-#   2. 7. 速い S は 21_05 と同じ。21_06 FEATURES の印の間は 21_06a と 1 字も違わない(G-feat: SHA-256 を学習の記録と照合)。
-#      G-model: モデルと学習の行の SHA-256・scikit-learn と numpy の版・特徴量の名前と設定と特徴量が使う定数が学習の記録と
-#      同じでなければ STOP。本番では、学習の記録は models/21_06a_train.json(21_06a の最初の本番の学習)以外を受け付けない。
-#      21_04 の結果は最初の本番(mode test、名前に _rerun が無い)だけを使い、21_06a の学習が 21_04 の本番より前かも確かめる。
-#      使った学習の記録・モデル・学習の行・21_04 の CSV の SHA-256 を、1 回だけの記録と JSON に書く。途中の例外も記録する。
-#   3. 評価の地震ごと・時点(0.5・1・2・3 s)ごとに:
-#      C3・C4 を出し、21_04 の CSV と同じか確かめる(G-same: 誤差 6e-5 km 以内、窓の数・M6r に戻ったか・C4 で補正した局の数が同じ)
-#      L3 = 凍結したモデルが近いと見積もった上位 10 地震の事前分布 × 物理(C3 と同じ locate_map)
-#      L4 = L3 + その 10 地震の通り道の補正(C4 と同じ corr_from)
-#      S > 0 の候補が 5 未満なら C3・C4 と同じく M6r に戻る
-#      記述用の L3p・L4p: 2026 の学習の行に 2016 の pool(本震 + 72 時間まで)の行を足して、同じ設定で学び直したモデルで同じ計算
-#      (「系列の中で学び足す」効果を見るだけ。判定には使わない)
-#   4. 物理だけの 9 つの方法の誤差は 21_04 の CSV から読む(BEST は 21_02・21_04 と同じ決め方)。
-#      C3・C4・L3・L4 の誤差は CSV と同じ小数 4 桁に丸めてから比べる(同点を同点として扱うため)。
-#   1 回だけの記録(opened)は、8. の入力の確認(学習の記録・モデル・21_04 の結果)が全て通ってから書く。
+# 21_06b v1 から変えたこと(これ以外は 1 字も変えていない。DIFF_LOG.md):
+#   1. 入力の既定のキャッシュ: data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt(21_20 と同じもの)。
+#   2. MAIN_UTC・UNTOUCHED_UTC を 21_20 と同じ値にした(2018-06-17 22:58:30 UTC ± 60 s。秒までの発生時刻ではない。21_20 の冒頭を見る)。
+#   3. 比べる相手と順番の確かめを 21_04 の出力から 21_20 の出力に変えた: data/21_20_per_event.csv(--dev は _dev)、
+#      models/21_20_judgment.json(最初の本番で、キャッシュの SHA-256 が同じこと)、models/21_20_opened.json(21_06a の学習が先か)。
+#   4. 出力の名前: models/21_20f_judgment.json / models/21_20f_opened.json / data/21_20f_per_event.csv / PDF/21_20f_F1_learned_test.pdf
+#      (--dev では _dev、2 回目以降は _rerun_<UTC の時刻>)。表示の [21_20f]。
+#   5. 限界の文・表示・図の題の系列の名前を大阪府北部 2018 にした。記述用の L3p・L4p は「2026 の学習の行 + 2018 の pool の行」で学び直す
+#      (21_06b と同じ作り方。判定には使わない)。
+#   変えていないもの: 21_06 FEATURES の印の間(1 字も変えない。G-feat で学習の記録 models/21_06a_train.json の
+#   feature_block_sha256 = 9905420e546d… と照合する)、凍結したモデル models/21_06_ranker.pkl(学び直さない)、学習の記録、
+#   G-model(scikit-learn・numpy の版が学習時と同じでなければ STOP。学習した Mac の ~/SWIFT の環境で回す)、仮説と判定の規則。
 #
-# 事前登録の仮説と判定(21_02 と同じ形。片側の対応 Wilcoxon(zero_method='wilcox')・差が 0 でない組 10 以上):
+# 事前登録の仮説と判定(21_06 と同じ。事前登録の記録 21_20 に再掲):
 #   HL1(主)  L4 @ τ = 2 s が BEST より良い、p < 0.01、BEST ≥ 0.5 km  → LEARNED-CONFIRMED / PHYSICS-AT-FLOOR / NOT-CONFIRMED
-#   HL2(副)  L4 @ τ = 2 s が C4 より良い、p < 0.005(人が決めた選び方より学習した選び方が良いか)
+#   HL2(副)  L4 @ τ = 2 s が C4 より良い、p < 0.005
 #   HL3(副)  L3 @ τ = 0.5 s が BEST より良い、p < 0.005、BEST ≥ 0.5 km
@@ -37,13 +31,10 @@
 #
-# 限界(表示と JSON にも英語で書く): 21_04 の限界に加えて、学習は鳥取 2026 だけ・L3p・L4p は記述だけ・物理だけの方法と C3・C4 は
-#   21_04 の CSV を使う(C3・C4 は計算し直して同じことを確かめる)
-#
-# Usage : (21_04 の本番が終わってから)
-#         cd ~/SWIFT && caffeinate -i uv run python src/21_06b_ct2016_learned_test.py --dev   (動作確認。21_04 の dev の CSV が要る)
-#         cd ~/SWIFT && caffeinate -i uv run python src/21_06b_ct2016_learned_test.py         (本番。1 回だけ)
-# 入力  : 21_04 と同じキャッシュ、data/21_04_per_event.csv と models/21_04_judgment.json(--dev なら _dev の CSV)、
-#         models/21_06a_train.json・models/21_06_ranker.pkl・data/21_06a_train_rows.npz(21_06a の出力)
-# Output: models/21_06b_judgment.json / models/21_06b_opened.json / data/21_06b_per_event.csv / PDF/21_06b_F1_learned_test.pdf
-#         (--dev では _dev、2 回目以降は _rerun_<UTC の時刻>)
-# 止める条件(STOP): 21_04 と同じもの・G-feat・G-model・21_04 の CSV が無いか地震が合わない・キャッシュが 21_04 と違う・G-same
+# Usage : (21_20 の本番が終わってから)
+#         cd ~/SWIFT && caffeinate -i uv run python src/21_20f_osaka2018_learned_test.py --dev   (動作確認。21_20 の dev の CSV が要る)
+#         cd ~/SWIFT && caffeinate -i uv run python src/21_20f_osaka2018_learned_test.py         (本番。1 回だけ)
+# 入力  : 21_20 と同じキャッシュ、data/21_20_per_event.csv と models/21_20_judgment.json・models/21_20_opened.json(--dev なら _dev の CSV)、
+#         models/21_06a_train.json・models/21_06_ranker.pkl・data/21_06a_train_rows.npz(21_06a の出力。凍結 B のまま)
+# Output: models/21_20f_judgment.json / models/21_20f_opened.json / data/21_20f_per_event.csv / PDF/21_20f_F1_learned_test.pdf
+# 止める条件(STOP): 21_06b と同じもの(21_20 と同じ入力のゲート・G-feat・G-model・21_20 の CSV が無いか地震が合わない・キャッシュが 21_20 と違う・G-same)
+# 所要  : 参考: 21_06b の本番は試験 307 地震で 506 s(models/21_06b_judgment.json の runtime_s)
 # =============================================================================
@@ -58,4 +49,4 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--cache", default="data/ct2016_processed/tottori_parsed_realpick_ct2016_m15.pt", help="15_01c v3.3 の鳥取県中部 2016 の M>=1.5 版")
-ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(21_04 の dev と同じ 20 地震。比べる相手は data/21_04_per_event_dev.csv)")
+ap.add_argument("--cache", default="data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt", help="21_20c(15_01c v3.3 と同じ計算)の大阪府北部 2018 の M>=1.5 版")
+ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(21_20 の dev と同じ 20 地震。比べる相手は data/21_20_per_event_dev.csv)")
 ap.add_argument("--train-json", default="models/21_06a_train.json", help="21_06a の学習の記録(凍結したモデルの SHA-256 を持つ)")
@@ -67,3 +58,3 @@
 TAUS = [0.5, 1.0, 2.0, 3.0]
-ALPHA_L1, ALPHA_L23 = 0.01, 0.005          # 21_06b: HL1(L4 @ 2 s 対 BEST)は 0.01、HL2(L4 @ 2 s 対 C4)・HL3(L3 @ 0.5 s 対 BEST)は 0.005
+ALPHA_L1, ALPHA_L23 = 0.01, 0.005          # 21_20f: HL1(L4 @ 2 s 対 BEST)は 0.01、HL2(L4 @ 2 s 対 C4)・HL3(L3 @ 0.5 s 対 BEST)は 0.005
 MIN_MAG, FRESH_MAX_MAG, MATCH_S = 1.5, 2.0, 1.0
@@ -79,7 +70,8 @@
 NBOOT, SEED, N_DEV, N_GATE = 2000, 12, 20, 5
-MAIN_UTC = dt.datetime(2016, 10, 21, 5, 7, 22, 570000)
-UNTOUCHED_UTC = (dt.datetime(2016, 10, 19), dt.datetime(2016, 11, 15))   # G-untouched: 21_04a の期間を含む
-LIMITS = ["second sequence: Central Tottori 2016 (mainshock 2016-10-21 05:07 UTC, Mj 6.6), never used in ARGUS development; "
-          "the hypotheses were fixed on West Tottori 2026 (21_01/21_02) and are applied here unchanged",
-          "one second sequence only",
+MAIN_UTC = dt.datetime(2018, 6, 17, 22, 58, 30)   # 21_20 と同じ: 気象庁の発表の 07:58 JST の 1 分の真ん中(秒までの値ではない。±60 s でこの 1 分を含む)。要確認
+UNTOUCHED_UTC = (dt.datetime(2018, 6, 15), dt.datetime(2018, 7, 12))     # G-untouched: 21_20a の期間(本震の 2 日前〜24 日後)を含む
+LIMITS = ["third sequence: Northern Osaka 2018 (mainshock 2018-06-18, 07:58 JST; origin time and Mj are those of the JMA catalogue, "
+          "see 21_20a's JSON), never used in ARGUS development; the hypotheses were fixed on West Tottori 2026 (21_01/21_02), "
+          "tested on Central Tottori 2016 (21_04, run with a documented deviation) and are applied here unchanged",
+          "one third sequence only",
           "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
@@ -88,10 +80,11 @@
           "per-window per-component z-score, JST epoch); whether a filter was applied before the z-score in the 2026 h5 is not recorded "
-          "(none here; compared in 21_04b G-spec)",
-          "the cache was built by 15_01c v3.3 (picking, QC and assembly identical to v3; only the window-index file name and output "
-          "folder changed)",
-          "catalogue: JMA final hypocentres (h2016; West Tottori 2026 used the unified catalogue); past-event locations are JMA "
+          "(none here; compared in 21_20b G-spec)",
+          "the cache was built by 21_20c, whose picking, QC and assembly are identical to 15_01c v3.3 (itself identical to v3 except "
+          "the window-index file name and output folder); 21_20c changed only labels, defaults and required arguments",
+          "catalogue: JMA hypocentres from h2018 (whether h2018 is the final stage is to be confirmed; West Tottori 2026 used the "
+          "unified catalogue); past-event locations are JMA "
           "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
-          "the 2016 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
+          "the 2018 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
           "events; whether the 2026 catalogue excluded them is not recorded. Manual and automatic hypocentres are mixed (per-flag "
-          "counts in 21_04a's JSON)",
+          "counts in 21_20a's JSON)",
           "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); the 2026 station list's "
@@ -124,3 +117,3 @@
 SELF_SHA = sha256(Path(__file__))
-print(f"[21_06b] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
+print(f"[21_20f] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
       f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")
@@ -129,3 +122,3 @@
 CP = ROOT / a.cache
-if not CP.exists(): raise SystemExit(f"[21_06b] STOP: {a.cache} が無い(ノート 21_04_ct2016_colab.ipynb のセル 11 で作った tottori_parsed_realpick_ct2016_m15.pt を data/ct2016_processed/ に置く)")
+if not CP.exists(): raise SystemExit(f"[21_20f] STOP: {a.cache} が無い(ノート 21_20_osaka2018_colab.ipynb のセル 11 で作った tottori_parsed_realpick_osaka2018_m15.pt を data/osaka2018_processed/ に置く)")
 EVS = torch.load(CP, map_location="cpu", weights_only=False)
@@ -134,7 +127,7 @@
     miss = [k for k in need if k not in e]
-    if miss: raise SystemExit(f"[21_06b] STOP: キャッシュの地震に {miss} が無い(15_01c v3.3 の出力か確かめる)")
+    if miss: raise SystemExit(f"[21_20f] STOP: キャッシュの地震に {miss} が無い(21_20c の出力か確かめる)")
 for e in EVS:
     w_ = np.asarray(e["waveforms"])
-    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_06b] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
-    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_06b] STOP: {e['origin_time']} の波形に NaN か無限大")
+    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_20f] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
+    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_20f] STOP: {e['origin_time']} の波形に NaN か無限大")
 def to_ns(o):
@@ -146,3 +139,3 @@
     except Exception:
-        raise SystemExit(f"[21_06b] STOP: origin_time {o!r} を時刻として読めない")
+        raise SystemExit(f"[21_20f] STOP: origin_time {o!r} を時刻として読めない")
 OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
@@ -154,4 +147,4 @@
 if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
-    raise SystemExit("[21_06b] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
-if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[21_06b] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
+    raise SystemExit("[21_20f] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
+if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[21_20f] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
 # G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
@@ -162,10 +155,10 @@
 n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
-print(f"[21_06b] 入力: 鳥取県中部 2016 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
+print(f"[21_20f] 入力: 大阪府北部 2018 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
       f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
-print(f"[21_06b] G-untouched: 期間 2016-10-19〜2016-11-15(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
+print(f"[21_20f] G-untouched: 期間 2018-06-15〜2018-07-12(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
       + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
-if n_out != 0 or n_big != 1: raise SystemExit("[21_06b] STOP(G-untouched): 鳥取県中部 2016 のキャッシュに見えない(この行を貼って相談)")
+if n_out != 0 or n_big != 1: raise SystemExit("[21_20f] STOP(G-untouched): 大阪府北部 2018 のキャッシュに見えない(この行を貼って相談)")
 im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
 if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
-    raise SystemExit(f"[21_06b] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj 6.6・2016-10-21 05:07:22.57 UTC)")
+    raise SystemExit(f"[21_20f] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2018-06-17 22:58 UTC の 1 分 ± 60 s。気象庁の発表の 07:58 JST)")
 CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
@@ -173,5 +166,5 @@
 if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
-    raise SystemExit("[21_06b] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
-print(f"[21_06b] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
-print(f"[21_06b] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
+    raise SystemExit("[21_20f] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
+print(f"[21_20f] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
+print(f"[21_20f] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
       f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")
@@ -186,3 +179,3 @@
     kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
-    if len(set(kk)) != n: raise SystemExit(f"[21_06b] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
+    if len(set(kk)) != n: raise SystemExit(f"[21_20f] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
 HASP = ~np.isnan(TFIRST)
@@ -198,6 +191,6 @@
 EX, EY = to_xy(SRC[:, 0], SRC[:, 1])
-print(f"[21_06b] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
+print(f"[21_20f] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
 EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
-if len(EVAL) == 0: raise SystemExit("[21_06b] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
-if a.dev: print(f"[21_06b] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
+if len(EVAL) == 0: raise SystemExit("[21_20f] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
+if a.dev: print(f"[21_20f] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                 "(較正にも入っているので値は楽観的)")
@@ -205,3 +198,3 @@
 # ---------------------------------------------------------------- 1 回だけの記録(本番は、試験の地震の結果を計算する前に書く)
-OPEN = ROOT / "models/21_06b_opened.json"
+OPEN = ROOT / "models/21_20f_opened.json"
 SUF = "_dev" if a.dev else ""
@@ -212,6 +205,6 @@
 if not a.dev:
-    if OPEN.exists() or (ROOT / "models/21_06b_judgment.json").exists():
+    if OPEN.exists() or (ROOT / "models/21_20f_judgment.json").exists():
         SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
-        print(f"[21_06b] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
-OPENED = False                           # 21_06b: 試験を開くのは、学習の記録・モデル・21_04 の結果の確認が全て通った後(8. の最後)
+        print(f"[21_20f] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
+OPENED = False                           # 21_20f: 試験を開くのは、学習の記録・モデル・21_20 の結果の確認が全て通った後(8. の最後)
 def stop(msg):
@@ -283,3 +276,3 @@
 LAP_B = float(np.median(np.abs(r1)) / np.log(2.0))
-print(f"[21_06b] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
+print(f"[21_20f] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
       f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")
@@ -294,3 +287,3 @@
 XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
-print(f"[21_06b] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
+print(f"[21_20f] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
       f"  固定の深さ {ZDEF:.1f} km")
@@ -330,3 +323,3 @@
 lls = {h: loo_ll(h) for h in HS}; KDE_H = max(lls, key=lls.get)
-print(f"[21_06b] KDE の帯域(pool の一つ抜き): {KDE_H} km")
+print(f"[21_20f] KDE の帯域(pool の一つ抜き): {KDE_H} km")
 def log_prior(nodes, mem):
@@ -358,3 +351,3 @@
     lib = np.where((OTNS <= OTNS[ie] - int(buffer_h * 3600e9)) & HASP)[0]
-    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_06b] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
+    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_20f] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
     return lib
@@ -434,3 +427,3 @@
     top = lib[np.argsort(-S, kind="stable")[:min(k, pos)]]
-    if ie is not None and ie in top: stop("[21_06b] STOP: 自分自身が似た地震の上位に入っている")
+    if ie is not None and ie in top: stop("[21_20f] STOP: 自分自身が似た地震の上位に入っている")
     out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
@@ -582,3 +575,3 @@
 
-# ---------------------------------------------------------------- 8. 凍結したモデルと 21_04 の結果の読み込み
+# ---------------------------------------------------------------- 8. 凍結したモデルと 21_20 の結果の読み込み
 import pickle
@@ -588,42 +581,42 @@
 except ImportError:
-    stop("[21_06b] STOP: scikit-learn が無い(21_06a と同じ環境で回す)")
+    stop("[21_20f] STOP: scikit-learn が無い(21_06a と同じ環境で回す)")
 TJP = ROOT / a.train_json
-if not TJP.exists(): stop(f"[21_06b] STOP: 学習の記録 {a.train_json} が無い(先に 21_06a)")
+if not TJP.exists(): stop(f"[21_20f] STOP: 学習の記録 {a.train_json} が無い(先に 21_06a)")
 TJ = json.load(open(TJP))
 if not a.dev and (a.train_json != "models/21_06a_train.json" or TJ.get("mode") != "train" or TJ.get("suffix", "") != ""):
-    stop("[21_06b] STOP: 本番は、事前登録した 21_06a の最初の本番の学習(models/21_06a_train.json、mode train)でしか回さない")
+    stop("[21_20f] STOP: 本番は、事前登録した 21_06a の最初の本番の学習(models/21_06a_train.json、mode train)でしか回さない")
 FB = open(Path(__file__), encoding="utf-8").read()
 FEAT_SHA = hashlib.sha256(FB[FB.index("# >>> 21_06 FEATURES BEGIN"):FB.index("# <<< 21_06 FEATURES END")].encode()).hexdigest()
-if TJ["feature_block_sha256"] != FEAT_SHA: stop("[21_06b] STOP(G-feat): 特徴量の部分が 21_06a と 1 字でも違う(学習と試験で同じ計算になっていない)")
+if TJ["feature_block_sha256"] != FEAT_SHA: stop("[21_20f] STOP(G-feat): 特徴量の部分が 21_06a と 1 字でも違う(学習と試験で同じ計算になっていない)")
 MP = ROOT / TJ["model_path"]
-if not MP.exists() or sha256(MP) != TJ["model_sha256"]: stop(f"[21_06b] STOP(G-model): モデル {TJ['model_path']} が無いか、SHA-256 が学習の記録と違う")
-if TJ["sklearn"] != sklearn.__version__: stop(f"[21_06b] STOP: scikit-learn の版が学習時({TJ['sklearn']})と違う({sklearn.__version__})")
+if not MP.exists() or sha256(MP) != TJ["model_sha256"]: stop(f"[21_20f] STOP(G-model): モデル {TJ['model_path']} が無いか、SHA-256 が学習の記録と違う")
+if TJ["sklearn"] != sklearn.__version__: stop(f"[21_20f] STOP: scikit-learn の版が学習時({TJ['sklearn']})と違う({sklearn.__version__})")
 if TJ["feats"] != FEATS or TJ["hgb"] != HGB or TJ.get("block_consts") != json.loads(json.dumps(BLOCK_CONSTS)) or TJ.get("cond_min") != COND_MIN:
-    stop("[21_06b] STOP: 特徴量の名前・設定・特徴量が使う定数が学習の記録と違う")
-if TJ["numpy"] != np.__version__: stop(f"[21_06b] STOP: numpy の版が学習時({TJ['numpy']})と違う({np.__version__})")
+    stop("[21_20f] STOP: 特徴量の名前・設定・特徴量が使う定数が学習の記録と違う")
+if TJ["numpy"] != np.__version__: stop(f"[21_20f] STOP: numpy の版が学習時({TJ['numpy']})と違う({np.__version__})")
 with open(MP, "rb") as f: MODEL = pickle.load(f)
 RP = ROOT / TJ["train_rows_path"]
-if not RP.exists() or sha256(RP) != TJ["train_rows_sha256"]: stop(f"[21_06b] STOP: 学習の行 {RP.relative_to(ROOT)} が無いか SHA-256 が違う")
-print(f"[21_06b] 凍結したモデル: {TJ['model_path']} SHA-256 {TJ['model_sha256'][:12]}…(2026 の {TJ['n_train_events']} 地震で学習)  "
+if not RP.exists() or sha256(RP) != TJ["train_rows_sha256"]: stop(f"[21_20f] STOP: 学習の行 {RP.relative_to(ROOT)} が無いか SHA-256 が違う")
+print(f"[21_20f] 凍結したモデル: {TJ['model_path']} SHA-256 {TJ['model_sha256'][:12]}…(2026 の {TJ['n_train_events']} 地震で学習)  "
       f"特徴量の部分 {FEAT_SHA[:12]}… G-feat PASS  G-model PASS")
 TJ_SHA = sha256(TJP)
-REFCSV = ROOT / ("data/21_04_per_event_dev.csv" if a.dev else "data/21_04_per_event.csv")
-if not REFCSV.exists(): stop(f"[21_06b] STOP: {REFCSV.relative_to(ROOT)} が無い(先に 21_04 を回す。21_06b は 21_04 の後)")
+REFCSV = ROOT / ("data/21_20_per_event_dev.csv" if a.dev else "data/21_20_per_event.csv")
+if not REFCSV.exists(): stop(f"[21_20f] STOP: {REFCSV.relative_to(ROOT)} が無い(先に 21_20 を回す。21_20f は 21_20 の後)")
 ref = {r["origin_time"]: r for r in csv.DictReader(open(REFCSV))}
 if sorted(ref) != sorted(OT[ie] for ie in EVAL):
-    stop(f"[21_06b] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
-J04 = ROOT / "models/21_04_judgment.json"
+    stop(f"[21_20f] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
+J04 = ROOT / "models/21_20_judgment.json"
 if J04.exists() and not a.dev:
     j4 = json.load(open(J04))
-    if j4.get("mode") != "test" or j4.get("suffix") != "": stop("[21_06b] STOP: models/21_04_judgment.json が 21_04 の最初の本番の結果でない")
-    if j4.get("cache_sha256") != CACHE_SHA: stop("[21_06b] STOP: キャッシュの SHA-256 が 21_04 の本番と違う")
-    print("[21_06b] キャッシュの SHA-256 は 21_04 の本番と同じ")
-    O4 = ROOT / "models/21_04_opened.json"
+    if j4.get("mode") != "test" or j4.get("suffix") != "": stop("[21_20f] STOP: models/21_20_judgment.json が 21_20 の最初の本番の結果でない")
+    if j4.get("cache_sha256") != CACHE_SHA: stop("[21_20f] STOP: キャッシュの SHA-256 が 21_20 の本番と違う")
+    print("[21_20f] キャッシュの SHA-256 は 21_20 の本番と同じ")
+    O4 = ROOT / "models/21_20_opened.json"
     t4 = json.load(open(O4))[0]["utc"] if O4.exists() else None
-    print(f"[21_06b] 順番の確認: 21_06a の学習 {TJ.get('utc')} / 21_04 の本番を開いた時刻 {t4}(学習が先のはず。事前登録の push の時刻とも照らす)")
-    if t4 is not None and TJ.get("utc") is not None and TJ["utc"] > t4: stop("[21_06b] STOP: 21_06a の学習が 21_04 の本番より後(事前登録の順番と違う)")
+    print(f"[21_20f] 順番の確認: 21_06a の学習 {TJ.get('utc')} / 21_20 の本番を開いた時刻 {t4}(学習が先のはず。事前登録の push の時刻とも照らす)")
+    if t4 is not None and TJ.get("utc") is not None and TJ["utc"] > t4: stop("[21_20f] STOP: 21_06a の学習が 21_20 の本番より後(事前登録の順番と違う)")
 elif not a.dev:
-    stop("[21_06b] STOP: models/21_04_judgment.json が無い(21_04 の本番を先に終える)")
+    stop("[21_20f] STOP: models/21_20_judgment.json が無い(21_20 の本番を先に終える)")
 REF_SHA = sha256(REFCSV)
-print(f"[21_06b] SHA-256(事前登録の記録の 6 節と照らす): 学習の記録 {TJ_SHA} / モデル {TJ['model_sha256']} / 学習の行 {TJ['train_rows_sha256']} / 21_04 の CSV {REF_SHA}")
+print(f"[21_20f] SHA-256(事前登録の記録の 6 節と照らす): 学習の記録 {TJ_SHA} / モデル {TJ['model_sha256']} / 学習の行 {TJ['train_rows_sha256']} / 21_20 の CSV {REF_SHA}")
 if not a.dev:                                 # 入力の確認が全て通ってから試験を開く(ここより前の STOP は記録しない)
@@ -639,3 +632,3 @@
 
-# ---------------------------------------------------------------- 9. 記述用: 2016 の pool を足して学び直した版(L3p・L4p。同じ設定。判定には使わない)
+# ---------------------------------------------------------------- 9. 記述用: 2018 の pool を足して学び直した版(L3p・L4p。同じ設定。判定には使わない)
 EVSET = set(int(i) for i in EVAL)
@@ -653,5 +646,5 @@
 MODEL_P.fit(np.concatenate([R26["X"]] + Xp), np.concatenate([R26["y"]] + yp), sample_weight=np.concatenate([R26["w"]] + wp))
-print(f"[21_06b] 記述用の L3p・L4p: 2026 の行 {len(R26['y'])} + 2016 の pool の行 {int(sum(len(v) for v in yp))} で学び直した")
-
-# ---------------------------------------------------------------- 10. 評価の地震(C3・C4 を出して 21_04 と同じか確かめ、L3・L4 を出す)
+print(f"[21_20f] 記述用の L3p・L4p: 2026 の行 {len(R26['y'])} + 2018 の pool の行 {int(sum(len(v) for v in yp))} で学び直した")
+
+# ---------------------------------------------------------------- 10. 評価の地震(C3・C4 を出して 21_20 と同じか確かめ、L3・L4 を出す)
 TL4 = [f"{t:g}" for t in TAUS]
@@ -682,9 +675,9 @@
     except BaseException as ex:
-        stop(f"[21_06b] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
+        stop(f"[21_20f] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
     if (ii + 1) % 10 == 0: print(f"  … {ii + 1}/{len(EVAL)}  ({time.time() - T0:.0f} s)")
-for k in KEYS:                                # 21_04 の CSV(小数 4 桁)と同じ丸めにそろえてから比べる(同点を同点として扱う)
+for k in KEYS:                                # 21_20 の CSV(小数 4 桁)と同じ丸めにそろえてから比べる(同点を同点として扱う)
     E[k] = np.vectorize(lambda v: float(f"{v:.4f}"))(E[k])
 G_SAME = "PASS" if not mism else f"FAIL ({len(mism)})"
-print(f"[21_06b] G-same(ここで計算した C3・C4 が 21_04 の CSV と同じ): {G_SAME}")
-if mism: stop(f"[21_06b] STOP(G-same): 21_04 と同じ計算になっていない(例 {mism[:3]})")
+print(f"[21_20f] G-same(ここで計算した C3・C4 が 21_20 の CSV と同じ): {G_SAME}")
+if mism: stop(f"[21_20f] STOP(G-same): 21_20 と同じ計算になっていない(例 {mism[:3]})")
 for b in BASE:
@@ -728,3 +721,3 @@
 def fp(p): return "—" if p is None else f"{p:.2g}"
-print(f"\n[21_06b] ===== 水平誤差の中央値 km [95% 区間](鳥取県中部 2016、評価 {NT} 地震{'、dev' if a.dev else ''}) =====")
+print(f"\n[21_20f] ===== 水平誤差の中央値 km [95% 区間](大阪府北部 2018、評価 {NT} 地震{'、dev' if a.dev else ''}) =====")
 for k in ["BEST"] + KEYS:
@@ -739,3 +732,3 @@
           f"L が M6r に戻った割合 {d['learned_fallback_frac']:.2f}")
-print(f"\n[21_06b] ===== 事前登録の判定 =====")
+print(f"\n[21_20f] ===== 事前登録の判定 =====")
 for name, h in HYP.items():
@@ -744,4 +737,4 @@
           f"p = {fp(pr['p'])}(基準 {h['alpha']})  差が 0 でない組 {pr['n_nonzero']}  FLOOR={h['floor']}  → {'勝ち' if h['win'] else '勝ちなし'}")
-print(f"\n[21_06b] 判定(事前登録、HL1): {VERDICT}")
-LIMITS_L = ["second sequence: Central Tottori 2016 (mainshock 2016-10-21 05:07 UTC, Mj 6.6), never used in ARGUS development; HL1-HL3 and "
+print(f"\n[21_20f] 判定(事前登録、HL1): {VERDICT}")
+LIMITS_L = ["third sequence: Northern Osaka 2018 (mainshock 2018-06-18, 07:58 JST; JMA catalogue values), never used in ARGUS development; HL1-HL3 and "
             "the learned ranker were fixed in the 21_06 preregistration and frozen by 21_06a on West Tottori 2026 before this test"] + \
@@ -749,7 +742,7 @@
             "(depth not solved); it is missing (nan) with fewer than 4 common stations or a near-linear station geometry", "the learned ranker (21_06a) was trained on West Tottori 2026 only and frozen before this test; L3p/L4p (retrained with the "
-                     "2016 pool) are descriptive", "21_06b reuses the 21_04 per-event CSV for the physics-only methods and C3/C4, and "
-                     "recomputes C3/C4 to check identity (G-same)", "C3/C4/L3/L4 errors are rounded to 4 decimals (as in the 21_04 CSV) "
+                     "2018 pool) are descriptive", "21_20f reuses the 21_20 per-event CSV for the physics-only methods and C3/C4, and "
+                     "recomputes C3/C4 to check identity (G-same)", "C3/C4/L3/L4 errors are rounded to 4 decimals (as in the 21_20 CSV) "
                      "before comparison so that ties stay ties", "log10_dt_h uses the target's JMA origin time (not known exactly at tau; "
                      "the error is a few seconds against >= 1 h)"]
-print("[21_06b] 限界: " + " / ".join(LIMITS_L))
+print("[21_20f] 限界: " + " / ".join(LIMITS_L))
 
@@ -764,3 +757,3 @@
     return o
-with open(ROOT / f"data/21_06b_per_event{SUF}.csv", "w", newline="") as f:
+with open(ROOT / f"data/21_20f_per_event{SUF}.csv", "w", newline="") as f:
     w = csv.writer(f)
@@ -770,3 +763,3 @@
         w.writerow([OT[ie], f"{MAG[ie]:.1f}"] + [("" if not np.isfinite(E[k][i, jt]) else f"{E[k][i, jt]:.4f}") for k in cols for jt in range(len(TAUS))])
-out = dict(script="21_06b_ct2016_learned_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"), suffix=SUF,
+out = dict(script="21_20f_osaka2018_learned_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"), suffix=SUF,
            cache=a.cache, cache_sha256=CACHE_SHA, reference_csv=str(REFCSV.relative_to(ROOT)), train_json=a.train_json,
@@ -775,3 +768,3 @@
            hypotheses=HYP, verdict=VERDICT,
-           verdict_rule="BEST(tau) = smallest median among the 9 AI-free methods with an estimate for every evaluated event (from the 21_04 CSV). "
+           verdict_rule="BEST(tau) = smallest median among the 9 AI-free methods with an estimate for every evaluated event (from the 21_20 CSV). "
                         "HL1 (primary): L4 at tau = 2 s vs BEST, alpha 0.01; HL2: L4 at 2 s vs C4, alpha 0.005; HL3: L3 at 0.5 s vs BEST, "
@@ -781,3 +774,3 @@
            limits=LIMITS_L, runtime_s=time.time() - T0)
-json.dump(clean(out), open(ROOT / f"models/21_06b_judgment{SUF}.json", "w"), indent=1)
+json.dump(clean(out), open(ROOT / f"models/21_20f_judgment{SUF}.json", "w"), indent=1)
 
@@ -797,3 +790,3 @@
 ax.set_xticks(x); ax.set_yscale("log"); ax.set_xlabel("Time since the first P pick, tau (s)"); ax.set_ylabel("Median epicentral error (km), 95% bootstrap CI")
-ax.set_title(f"(a) Central Tottori 2016, {NT} {'DEV' if a.dev else 'test'} events", fontsize=10); ax.grid(alpha=0.3)
+ax.set_title(f"(a) Northern Osaka 2018, {NT} {'DEV' if a.dev else 'test'} events", fontsize=10); ax.grid(alpha=0.3)
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, frameon=False, fontsize=8.5)
@@ -809,4 +802,4 @@
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8.5)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_06b_F1_learned_test{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_20f_F1_learned_test{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
 if not a.dev: log_open(f"completed: {VERDICT}")
-print(f"[21_06b] 出力: models/21_06b_judgment{SUF}.json, data/21_06b_per_event{SUF}.csv, PDF/21_06b_F1_learned_test{SUF}.pdf  ({time.time() - T0:.0f} s)")
+print(f"[21_20f] 出力: models/21_20f_judgment{SUF}.json, data/21_20f_per_event{SUF}.csv, PDF/21_20f_F1_learned_test{SUF}.pdf  ({time.time() - T0:.0f} s)")
```

## 動作確認(ネットワークを使わない。作りもののデータだけ)

| 確かめたこと | 結果 |
|---|---|
| 7 本とも `python -m py_compile` | 全て通った |
| 21_20a `--selftest`(21_04a と同じ読み方の試験) | 合格 |
| 21_20a を作りものの震源ファイル(本震を 2018-06-18 07:58:30 JST・Mj 6.1 とした 401 レコード。実データではない)で回す | 本震の規則・箱(緯度 0.30° × 経度 0.35°)・期間(2 日前〜24 日後)・CSV・JSON・図が出た |
| 21_20a: 作りものの本震を 08:05 にずらす | 「本震が規則に合わない」で STOP |
| 21_20a: 作りものの地震を 30 個に減らす(試験の候補 10) | 「試験の候補 … < 30」で STOP(CSV・JSON・図は書かれた) |
| 21_20b の `plan_blocks`・`zscore_windows`・`covers` を 21_04b v1.1 と同じ作りものの入力で比べる | 同じ結果(区切り 461 個で一致) |
| 21_20 と 21_04 を、同じ作りもののキャッシュ(161 地震。時刻だけ 2016 用と 2018 用にずらした)で `--dev` | 21_20 は G-untouched・G-split・G-causal・G-phys が PASS。per_event_dev.csv の origin_time 以外の 108 列・20 地震が 21_04 と 1 字も違わない |
| 21_20f を同じ作りもののキャッシュで `--dev`(models/21_06a_train.json と models/21_06_ranker.pkl を置いて) | G-feat・G-model(モデルの SHA-256)を通り、scikit-learn の版の確かめ(学習時 1.8.0・この環境 1.9.1)で STOP。それより後は Mac で確かめる |
| 21_20d・21_20e を作りもののキャッシュと作りものの 21_20b の報告で回す | 最後まで動き、21_20d_gclock2.json・PDF、21_20e_station_picks.csv・PDF が出た |

- torch はこの環境に無いので、試験の時だけ `torch.load` を pickle で読む作りものの torch を使った(スクリプトは変えていない)。
- h5py・HinetPy・obspy・seisbench が無いので、21_20b の取得と組み立て、21_20c は回していない(21_20c は計算の行が 15_01c v3.3 と同じことを差分で確かめた)。

## 2026-11-02 の直し(注釈と表示だけ。計算は変えていない)

| ファイル | 直したこと | 前の SHA-256 | 後の SHA-256 |
|---|---|---|---|
| 21_20b_osaka2018_hinet_to_h5.py | `VERSION = "v1"` → `VERSION = "v1 (=21_04b v1.1)"`。その行の注釈の誤り「取り方は 21_20b v1.1 と同じ」→「21_04b v1.1 と同じ」。冒頭の (3) の文を同じ値に合わせた | `a5836c06dd561c37e62db9e570d105f16e17fe81af9325d489f3b0ecd6beaf5d` | `43154e7a3b33451d6a2526f4a1b3ff4a8e6085964c380398ceab49b50745e06e` |
| 21_20c_osaka2018_realpick_cache_colab.py | 観測点の表示の "(stations.csv)" → `Path(args.stations).name`(渡したファイルの名前を出す) | `2b935ed57c4731c767a94fba8496703f8bedc5b75409d11f28fc9941c0092bcb` | `7b938b944003d99fcad7df188792e8e8eb95c71b07f1a1223bffad6671d04cf0` |

- 上の 2 つの差分は、21_20b・21_20c の節の「全ての差分」(元のスクリプトとの `diff -U1`)に入れ直した。前の版との差分は次のとおり:

```diff
--- 21_20b_osaka2018_hinet_to_h5.py(2026-11-01)
+++ 21_20b_osaka2018_hinet_to_h5.py(2026-11-02)
@@ -13,3 +13,3 @@
 #              時刻は G-clock2 で決める)を表示する(止まり方と、h5 を _FAILED の名前にする動きは v1.1 と同じ)
-#          (3) VERSION を v1 にした(この系列の 1 版目。取り方は 21_04b v1.1 と同じ。v1.1 の「要求の長さを短くして取り直す」も含む)
+#          (3) VERSION を "v1 (=21_04b v1.1)" にした(この系列の 1 版目。取り方は 21_04b v1.1 と同じ。v1.1 の「要求の長さを短くして取り直す」も含む)
 #
@@ -126,3 +126,3 @@
 
-VERSION = "v1"                              # 21_20b の 1 版目(取り方は 21_20b v1.1 と同じ)
+VERSION = "v1 (=21_04b v1.1)"              # 21_20b の 1 版目(取り方は 21_04b v1.1 と同じ)
 ROOT = Path(__file__).resolve().parent.parent
--- 21_20c_osaka2018_realpick_cache_colab.py(2026-11-01)
+++ 21_20c_osaka2018_realpick_cache_colab.py(2026-11-02)
@@ -339,3 +339,3 @@
                                        float(row["elevation"]))
-print(f"[21_20c] 観測点: {len(sta_meta)}局 (stations.csv)")
+print(f"[21_20c] 観測点: {len(sta_meta)}局 ({Path(args.stations).name})")
 
```

- `VERSION` はどこでも比べられていない(h5 の属性・報告・計画の JSON・表示に書かれるだけ)。`Path` は 21_20c の上の方で既に読み込んである。
- 確かめ: 7 本とも `python -m py_compile` が通った。21_20a `--selftest` は合格(21_20a は変えていない)。
- 21_20d・21_20e を、作りもののキャッシュ(300 地震・12 局)と空の 21_20b の報告(`{"gates": {"clock": []}}`)で、`--cache` に絶対パスを渡して回した
  (COLAB_STEPS_JA.md の セル 2b の形)。最後まで動き、21_20d は (e) を形だけの PASS にして (c) の値を表示した。21_20e は表を書いた。
- COLAB_STEPS_JA.md の セル 13b と M6 のすその印の計算を、2016 の 21_04e の表・21_04 と 21_06b の本番の出力(名前だけ 21_20 にしたもの)で回し、
  最後まで動くことを確かめた(その数は事前登録の記録には書いていない)。


## 2026-11-02 の直し(2)
- 21_20e: 冒頭の注釈 10 行目を案 C(必ず回す・判定は CSV で行う)に合わせた。計算は変えていない。SHA-256 は aacecdeea0d4dd5abca6e80cf27dd0240a0b0a2fe932502b2ce992f0368b1769 → 680e8825d49e00bba58cca9045c66ee7b213f05bc5a231d0810d041b4fefba92。
