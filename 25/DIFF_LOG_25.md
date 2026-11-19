# DIFF_LOG_25 — 凍結版 25_01〜25_09 と派生元(事前登録 24 で凍結した版)の差分

各スクリプトの派生元・SHA-256・差分(diff -U1)。差分は全部載せる(省略なし)。25_09 は新しく書いたもので、全文を載せる。

| 凍結版 | 派生元 | 派生元 SHA-256 | 追加 | 削除 |
|---|---|---|---|---|
| 25_01_shimane2018_jma_catalog.py | 24_01_nagano2014_jma_catalog.py | `a4fb5d9a41c69466…` | 73 | 61 |
| 25_02_shimane2018_hinet_to_h5.py | 24_02_nagano2014_hinet_to_h5.py | `0f2283af1e3a0fde…` | 107 | 109 |
| 25_03_shimane2018_realpick_cache_colab.py | 24_03_nagano2014_realpick_cache_colab.py | `86b3cb1f810752ea…` | 43 | 42 |
| 25_03h_shimane2018_overlap_exclusion.py | 24_03h_nagano2014_overlap_exclusion.py | `e2700654a13f0514…` | 44 | 47 |
| 25_04d_shimane2018_gclock2_picks.py | 24_04d_nagano2014_gclock2_picks.py | `42f783bba5ca6668…` | 155 | 55 |
| 25_04e_shimane2018_station_pick_diagnose.py | 24_04e_nagano2014_station_pick_diagnose.py | `befca1b3326d1865…` | 17 | 17 |
| 25_05_shimane2018_similarity_confirmation.py | 24_05_nagano2014_similarity_confirmation.py | `c10d15fe404309d8…` | 149 | 130 |
| 25_06f_shimane2018_learned_test.py | 24_06f_nagano2014_learned_test.py | `779c04a8c01ebf6d…` | 124 | 110 |
| 25_06g_shimane2018_gate_test.py | 24_06g_nagano2014_gate_test.py | `5a4aa29a5741e6e7…` | 132 | 118 |
| 24_07_causal_picks.py | 24_07_causal_picks.py | `b9b2fd5c8855c52f…` | 0 | 0 |
| 25_08_shimane2018_intensity_descriptive.py | 24_08_nagano2014_intensity_descriptive.py | `80391a29309da7a8…` | 39 | 43 |
| 25_09_shimane2018_flag_descriptive.py | 新(派生元なし) | — | 217 | 0 |

## 25_01_shimane2018_jma_catalog.py ← 24_01_nagano2014_jma_catalog.py

```diff
--- ../nagano/frz/24_01_nagano2014_jma_catalog.py	2026-11-15 05:21:00.094090162 +0000
+++ frz/25_01_shimane2018_jma_catalog.py	2026-11-17 01:57:17.160621318 +0000
@@ -2,33 +2,39 @@
 # =============================================================================
-# Script : 24_01_nagano2014_jma_catalog.py  (v1)
-#          [長野県北部 2014(本震 2014-11-22 22:08 JST、神城断層)の気象庁の震源を、21_02・21_04・21_20 と同じ形の CSV にする]
-# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の 1 つ目
-# 派生元 : 21_20a_osaka2018_jma_catalog.py v1(SHA-256 cad845a14375014056b7da2a539b750d88363be56620904381fd520db16d25d2)。
-#          読み方・除外・箱・期間・数え方・CSV の書き方・試験の候補が 30 未満で止める規則は 21_20a と 1 字も変えていない。
-#          変えたのは次だけ(DIFF_LOG_24.md):
-#          (1) 震源ファイル h2018.zip → h2014.zip
-#          (2) 本震の規則: 2014-11-22 の J の震源のうち Mj が最大の地震で、発生時刻が [22:08:00, 22:09:00) JST、Mj ≥ 6.5、
-#              深さ 0–20 km、緯度 36.45–36.95・経度 137.65–138.15(幅 0.5° × 0.5°)。24_00(事前登録の前の数だけの確かめ)と同じ値。
-#              深さを 0 km からにしたのは、気象庁の発表で本震の深さが 5 km 前後と浅く、21_20a の 5 km の境目に当たるのを避けるため
-#              (本震を見つけるためだけの値で、試験の地震の選び方には使わない)
-#          (3) 出力の名前(jma_nagano2014.csv・24_01_nagano2014_catalog.json・PDF/24_01_nagano2014_catalog.pdf)、表示 [24_01]、図の題
+# Script : 25_01_shimane2018_jma_catalog.py  (v1)
+#          [島根県西部 2018(本震 2018-04-09 01:32 JST)の気象庁の震源を、21_02・21_04・21_20・24 と同じ形の CSV にする]
+# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の入力の 1 つ目
+# 派生元 : 24_01_nagano2014_jma_catalog.py v1(SHA-256 a4fb5d9a41c694663d65cf5a6f124d97f024360f1d9a40b43c0bf1fc1a6812a6。事前登録 24 で凍結)。
+#          読み方・除外・箱・期間・数え方・CSV の書き方・試験の候補が 30 未満で止める規則は 24_01 と 1 字も変えていない。
+#          変えたのは次だけ(DIFF_LOG_25.md):
+#          (1) 震源ファイル h2014.zip → h2018.zip。中身は 25_00 で開いた版と同じであることを確かめる(新): SHA-256 の先頭 12 字が
+#              ea8eb186db3f(25_00 の表示)でなければ止める。気象庁は震源ファイルを訂正版に差し替えることがあるため。止まった時は、
+#              25_00 で取った Mac の ~/SWIFT/data/catalog/jma_raw/h2018.zip を Drive に上げて --hypo で渡す
+#          (2) 本震の規則は 25_00 と同じ: 2018-04-09(日本時間)の機関 J の震源のうち、探す範囲(気象庁の発表の 35°11.0'N 132°35.2'E
+#              の ± 0.25°)の中で Mj が最大の地震で、発生時刻が [01:32:00, 01:33:00) JST、Mj ≥ 5.9(発表の 6.1 − 0.2)、深さ 0–20 km。
+#              24_01 はその日の日本全体の最大を取っていた。同じ日に範囲の外でもっと大きい地震があっても本震を取り違えないよう、
+#              25_00 と同じく範囲の中だけで探す(本震を見つけるためだけの規則で、試験の地震の選び方には使わない)
+#          (3) 出力の名前(jma_shimane2018.csv・25_01_shimane2018_catalog.json・PDF/25_01_shimane2018_catalog.pdf)、表示 [25_01]、図の題、
+#              止まった時の文の「事前登録 24」→「事前登録 25」
 #
 # 何をするか(21_20a と同じ。年と名前だけが違う):
-#   1. 気象庁の震源ファイル h2014.zip を data/catalog/jma_raw/ に取る(24_00 で取ってあれば取らない。--hypo で指定してもよい)。
+#   1. 気象庁の震源ファイル h2018.zip を data/catalog/jma_raw/ に取る(既にあれば取らない。--hypo で zip を指定してもよい。展開したファイルは版の確かめで止まる)。
+#      SHA-256 の先頭 12 字が 25_00 の版(ea8eb186db3f)と違えば止める。
 #   2. 震源レコードを列の位置どおりに読む。3. 本震を上の規則で確かめる。4. 箱 = 本震の緯度 ± 0.15°・経度 ± 0.175°、
 #      期間 = 本震の 2 日前から 24 日後(日本時間)。除外・印ごとの数の記録は 21_20a と同じ。
-#   5. 出力: data/catalog/jma_nagano2014.csv(24_02・24_03 がそのまま読む)・data/catalog/24_01_nagano2014_catalog.json。
-#   6. 図: PDF/24_01_nagano2014_catalog.pdf。7. 試験の候補(本震 + 72 h より後の 1.5 ≤ Mj < 2.0)が 30 未満なら STOP。
+#   5. 出力: data/catalog/jma_shimane2018.csv(25_02・25_03 がそのまま読む)・data/catalog/25_01_shimane2018_catalog.json。
+#   6. 図: PDF/25_01_shimane2018_catalog.pdf。7. 試験の候補(本震 + 72 h より後の 1.5 ≤ Mj < 2.0)が 30 未満なら STOP。
 #
-# 開示: この系列の h2014 は、事前登録の前に 24_00(数だけの確かめ)で 1 回開いた。表示したのは本震の行(時刻・位置・深さ・Mj)と
+# 開示: この系列の h2018 は、事前登録の前に 25_00(数だけの確かめ)で 1 回開いた。表示したのは本震の行(時刻・位置・深さ・Mj)と
 #   数(全体・Mj ≥ 1.5・試験の候補・R1 の後の数・深さ 25 km より深い数・印の数・日ごとの数)だけで、試験の地震の位置の一覧・
-#   波形・どの方法の誤差も見ていない(事前登録 24 の冒頭)。
-# 止める条件(STOP): 21_20a と同じ(読み方の試験・ファイル・96 バイト・本震の日の震源が無い・本震の規則・本震の印・Mj ≥ 1.5 が 0・
-#   試験の候補が 30 未満)。
-# 限界: 正解も過去の地震も気象庁の震源。h2014 の確定の段階は要確認。手動と自動の震源が混ざる(印ごとの数を JSON に記録。24_00 では
-#   Mj ≥ 1.5 の 502 個が全て K)。箱には余震でない地震も入る。
+#   波形・どの方法の誤差も見ていない(事前登録 25 の冒頭)。h2018 は大阪府北部 2018(21_20a)でも開いたが、大阪の箱と期間
+#   (2018-06〜07)だけを使い、島根の箱は数えていない。
+# 止める条件(STOP): 24_01 と同じ(読み方の試験・ファイル・96 バイト・本震の日の震源が無い・本震の規則・本震の印・Mj ≥ 1.5 が 0・
+#   試験の候補が 30 未満)と、震源ファイルが 25_00 の版と違う(新)。
+# 限界: 正解も過去の地震も気象庁の震源。h2018 の確定の段階は要確認。手動と自動の震源が混ざる(印ごとの数を JSON に記録。25_00 では
+#   Mj ≥ 1.5 の 389 個が K 285・A 88・k 13・s 3、R1 の見積もりの後の試験の候補 41 個が K 15・A 25・k 1。A は自動の震源)。
+#   箱には余震でない地震も入る(25_00: 365 日前の同じ箱・同じ長さの期間に 34 個、Mj ≥ 1.5 は 0)。
 #
-# Usage : (Colab、ノート 24_nagano2014_colab.ipynb の セル N5)
-#         !python /content/drive/MyDrive/ARGUS/src/24_01_nagano2014_jma_catalog.py
-# Output: data/catalog/jma_nagano2014.csv / data/catalog/24_01_nagano2014_catalog.json / PDF/24_01_nagano2014_catalog.pdf
+# Usage : (Colab、ノート 25_shimane2018_colab.ipynb の セル N5)
+#         !python /content/drive/MyDrive/ARGUS/src/25_01_shimane2018_jma_catalog.py
+# Output: data/catalog/jma_shimane2018.csv / data/catalog/25_01_shimane2018_catalog.json / PDF/25_01_shimane2018_catalog.pdf
 # =============================================================================
@@ -51,10 +57,12 @@
 ROOT = Path(__file__).resolve().parent.parent
-URL = "https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2014.zip"   # 21_20a の URL の年だけを変えた(24_00 で取れた)
+URL = "https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2018.zip"   # 24_01 の URL の年だけを変えた(25_00 で取れた)
+EXPECT_SHA_PREFIX = "ea8eb186db3f"   # 25: 25_00 で開いた h2018.zip の SHA-256 の先頭 12 字(違えば止める)
 REC_LEN = 96
-# 本震の規則(24): 気象庁の発表の「22 時 08 分」の 1 分間を条件にする(24_00 と同じ規則。24_00 の表示では 22:08:17.90 JST)。以下の 1 行は 21_20a の注記のまま:
+# 本震の規則(25): 25_00 と同じ。気象庁の発表の「1 時 32 分」の 1 分間と、発表の震央の ± 0.25° の範囲を条件にする(25_00 の表示では 01:32:30.81 JST)。以下の 1 行は 21_20a の注記のまま:
 # 条件にする(要確認: 震源ファイルの本震がこの 1 分に入ること。入らなければ STOP。数字を直す時は版を上げて事前登録の記録に書く)
-MAIN_DATE_JST = datetime(2014, 11, 22).date()
-MAIN_WIN_JST = (datetime(2014, 11, 22, 22, 8, 0), datetime(2014, 11, 22, 22, 9, 0))   # [始まり, 終わり)
-MAIN_MIN_MJ, MAIN_DEPTH = 6.5, (0.0, 20.0)               # 24_00 と同じ(深さは 0 km から。冒頭の (2))
-MAIN_LAT, MAIN_LON = (36.45, 36.95), (137.65, 138.15)    # 24_00 と同じ(0.5° × 0.5°)
+MAIN_DATE_JST = datetime(2018, 4, 9).date()
+MAIN_WIN_JST = (datetime(2018, 4, 9, 1, 32, 0), datetime(2018, 4, 9, 1, 33, 0))   # [始まり, 終わり)
+MAIN_MIN_MJ, MAIN_DEPTH = 6.1 - 0.2 - 1e-9, (0.0, 20.0)  # 25_00 と同じ(発表の Mj 6.1 − 0.2、25_00 と同じ許容 1e-9、深さ 0–20 km)
+MAIN_C = (35 + 11.0 / 60, 132 + 35.2 / 60)               # 25_00 と同じ: 気象庁の発表の震央
+MAIN_LAT, MAIN_LON = (MAIN_C[0] - 0.25, MAIN_C[0] + 0.25), (MAIN_C[1] - 0.25, MAIN_C[1] + 0.25)   # 25_00 の探す範囲(± 0.25°)
 MIN_TEST = 30                                            # 21_04 の MIN_TEST と同じ(評価できる試験の地震が 30 未満なら INCONCLUSIVE)
@@ -158,3 +166,3 @@
     def check(c, msg):
-        if not c: sys.exit(f"[24_01] STOP: 読み方の試験に失敗: {msg}")
+        if not c: sys.exit(f"[25_01] STOP: 読み方の試験に失敗: {msg}")
     def put(buf, a, b, s):
@@ -183,3 +191,3 @@
     check(t == datetime(2016, 10, 21, 14, 7, 5, 0), 't == datetime(2016, 10, 21, 14, 7, 5, 0)')  # 15_01c は先頭 21 文字だけ読むので 0.1 s 単位に切り捨てる(2026 も同じ)
-    print("[24_01] selftest: 震源レコードの読み方の試験に全て合格(21_04a と同じ試験)")
+    print("[25_01] selftest: 震源レコードの読み方の試験に全て合格(21_04a と同じ試験)")
 
@@ -188,3 +196,3 @@
     ap = argparse.ArgumentParser()
-    ap.add_argument("--hypo", default="", help="手元の h2014.zip か展開したファイル(無ければ取る)")
+    ap.add_argument("--hypo", default="", help="手元の h2018.zip(zip のまま。展開したファイルは版の確かめで止まる。無ければ取る)")
     ap.add_argument("--selftest", action="store_true")
@@ -196,5 +204,5 @@
     for d in (CAT, RAWD, PDFD): d.mkdir(parents=True, exist_ok=True)
-    src = Path(a.hypo) if a.hypo else RAWD / "h2014.zip"
+    src = Path(a.hypo) if a.hypo else RAWD / "h2018.zip"
     if not src.exists():
-        print(f"[24_01] 取得: {URL}")
+        print(f"[25_01] 取得: {URL}")
         req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (ARGUS research)"})
@@ -204,5 +212,8 @@
         except Exception as e:
-            sys.exit(f"[24_01] STOP: {URL} が取れない({e})。ブラウザで取って --hypo で指定する")
+            sys.exit(f"[25_01] STOP: {URL} が取れない({e})。ブラウザで取って --hypo で指定する")
         src.write_bytes(data)
     sha = hashlib.sha256(src.read_bytes()).hexdigest()
+    if not sha.startswith(EXPECT_SHA_PREFIX):                  # 25: 25_00 で開いた版と同じか
+        sys.exit(f"[25_01] STOP: {src.name} の SHA-256 {sha[:12]}… が 25_00 の版 {EXPECT_SHA_PREFIX}… と違う(気象庁が差し替えた可能性。"
+                 f"25_00 で取った Mac の ~/SWIFT/data/catalog/jma_raw/h2018.zip を Drive に上げ、--hypo で渡す。この行を貼る)")
     if zipfile.is_zipfile(src):
@@ -210,3 +221,3 @@
             mem = [m for m in z.namelist() if not m.endswith("/")]
-            if not mem: sys.exit("[24_01] STOP: zip の中にファイルが無い")
+            if not mem: sys.exit("[25_01] STOP: zip の中にファイルが無い")
             raw = b"\n".join(z.read(m) for m in mem)
@@ -215,14 +226,15 @@
     recs, n_bad = read_records(raw)
-    print(f"[24_01] 震源ファイル {src.name}(SHA-256 {sha[:12]}…、中身 {mem})  レコード {len(recs)}  96 バイトでない行 {n_bad}")
-    if not recs or n_bad > 0.01 * len(recs): sys.exit("[24_01] STOP: 96 バイトのレコードの形でない(別のファイルの可能性)")
+    print(f"[25_01] 震源ファイル {src.name}(SHA-256 {sha[:12]}…、中身 {mem})  レコード {len(recs)}  96 バイトでない行 {n_bad}")
+    if not recs or n_bad > 0.01 * len(recs): sys.exit("[25_01] STOP: 96 バイトのレコードの形でない(別のファイルの可能性)")
     H = [parse_hypo(r) for r in recs]
     J = [h for h in H if h["agency"] == "J" and h["origin_jst"] is not None]
-    print(f"[24_01] 機関 J の震源 {len(J)}(他機関 {sum(1 for h in H if h['agency'] != 'J')}、時刻が読めない {sum(1 for h in H if h['origin_jst'] is None)})")
+    print(f"[25_01] 機関 J の震源 {len(J)}(他機関 {sum(1 for h in H if h['agency'] != 'J')}、時刻が読めない {sum(1 for h in H if h['origin_jst'] is None)})")
 
     # ---- 本震(事前に決めた規則)
-    day = [h for h in J if h["origin_jst"].date() == MAIN_DATE_JST and h["mag"] is not None]
-    if not day: sys.exit(f"[24_01] STOP: {MAIN_DATE_JST} の震源が無い")
+    day = [h for h in J if h["origin_jst"].date() == MAIN_DATE_JST and h["mag"] is not None      # 25: 25_00 と同じく探す範囲の中だけ
+           and h["lat"] is not None and h["lon"] is not None and MAIN_LAT[0] <= h["lat"] <= MAIN_LAT[1] and MAIN_LON[0] <= h["lon"] <= MAIN_LON[1]]
+    if not day: sys.exit(f"[25_01] STOP: {MAIN_DATE_JST} の探す範囲の中の震源が無い")
     m = max(day, key=lambda h: h["mag"])
     in_win = MAIN_WIN_JST[0] <= m["origin_jst"] < MAIN_WIN_JST[1]
-    print(f"[24_01] 本震: {m['origin_jst']} JST  {m['lat']:.4f}N {m['lon']:.4f}E  深さ {m['depth_km']} km  M{m['mag']}{m['mag_type']}  "
+    print(f"[25_01] 本震: {m['origin_jst']} JST  {m['lat']:.4f}N {m['lon']:.4f}E  深さ {m['depth_km']} km  M{m['mag']}{m['mag_type']}  "
           f"精度 {m['precision']}  (想定の 1 分 {MAIN_WIN_JST[0]:%H:%M:%S}〜{MAIN_WIN_JST[1]:%H:%M:%S} JST の中か: {in_win}。要確認の項目)")
@@ -231,5 +243,5 @@
           and MAIN_LON[0] <= m["lon"] <= MAIN_LON[1])
-    if not ok: sys.exit("[24_01] STOP: 本震が規則に合わない(読み方の誤りか別のファイル。この行を貼って相談)")
+    if not ok: sys.exit("[25_01] STOP: 本震が規則に合わない(読み方の誤りか別のファイル。この行を貼って相談)")
     if m["det_flag"] in BAD_DETFLAG or m["precision"] in BAD_PRECISION:
-        sys.exit(f"[24_01] STOP: 本震の震源が除く印(精度 {m['precision']}・震源決定の印 {m['det_flag']})を持つ(この行を貼って相談)")
+        sys.exit(f"[25_01] STOP: 本震の震源が除く印(精度 {m['precision']}・震源決定の印 {m['det_flag']})を持つ(この行を貼って相談)")
     box = [round(m["lat"] - HALF_LAT, 4), round(m["lat"] + HALF_LAT, 4), round(m["lon"] - HALF_LON, 4), round(m["lon"] + HALF_LON, 4)]
@@ -257,4 +269,4 @@
              library_only_mj_ge_2p0_after_72h=int(((mags >= FRESH_MAX_MAG - 1e-9) & after).sum()))
-    if n["mj_ge_1p5"] == 0: sys.exit("[24_01] STOP: 箱の中・期間内の Mj ≥ 1.5 が 0")
-    out_csv = CAT / "jma_nagano2014.csv"
+    if n["mj_ge_1p5"] == 0: sys.exit("[25_01] STOP: 箱の中・期間内の Mj ≥ 1.5 が 0")
+    out_csv = CAT / "jma_shimane2018.csv"
     with open(out_csv, "w", newline="") as f:
@@ -267,3 +279,3 @@
     flags_15 = dict(Counter(h["det_flag"] or "_" for h in rows if h["mag"] >= MIN_MAG - 1e-9))
-    summ = dict(script="24_01_nagano2014_jma_catalog.py", version=VERSION, source=URL, source_file=src.name, source_sha256=sha,
+    summ = dict(script="25_01_shimane2018_jma_catalog.py", version=VERSION, source=URL, source_file=src.name, source_sha256=sha,
                 mainshock=dict(origin_jst=fmt_time(m["origin_jst"]), lat=m["lat"], lon=m["lon"], depth_km=m["depth_km"], mj=m["mag"],
@@ -276,8 +288,8 @@
                 note="test candidates are before picking; the evaluated test set is those with a measured P in the cache")
-    json.dump(summ, open(CAT / "24_01_nagano2014_catalog.json", "w"), indent=1, ensure_ascii=False)
-    print(f"[24_01] 箱 {box}(緯度 0.30° × 経度 0.35°)  期間 {fmt_time(t0)} 〜 {fmt_time(t1)} JST  pool の切れ目 {fmt_time(cut)} JST")
-    print(f"[24_01] 除いた数: {ex}")
-    print(f"[24_01] 数: {n}")
-    print(f"[24_01] 震源決定の印の数(K・S・k・s = 手動、A・a = 自動。_ は空白): 全体 {flags_all}  Mj ≥ 1.5 {flags_15}")
-    print(f"[24_01] 出力: {out_csv.relative_to(ROOT)}, data/catalog/24_01_nagano2014_catalog.json")
+    json.dump(summ, open(CAT / "25_01_shimane2018_catalog.json", "w"), indent=1, ensure_ascii=False)
+    print(f"[25_01] 箱 {box}(緯度 0.30° × 経度 0.35°)  期間 {fmt_time(t0)} 〜 {fmt_time(t1)} JST  pool の切れ目 {fmt_time(cut)} JST")
+    print(f"[25_01] 除いた数: {ex}")
+    print(f"[25_01] 数: {n}")
+    print(f"[25_01] 震源決定の印の数(K・S・k・s = 手動、A・a = 自動。_ は空白): 全体 {flags_all}  Mj ≥ 1.5 {flags_15}")
+    print(f"[25_01] 出力: {out_csv.relative_to(ROOT)}, data/catalog/25_01_shimane2018_catalog.json")
 
@@ -296,3 +308,3 @@
     ax1.set_xlabel(f"Days since mainshock ({m['origin_jst']:%Y-%m-%d %H:%M} JST)"); ax1.set_ylabel("JMA magnitude Mj")
-    ax1.set_title("Northern Nagano 2014, JMA hypocentres in the box", fontsize=10); ax1.grid(alpha=0.3)
+    ax1.set_title("Western Shimane 2018, JMA hypocentres in the box", fontsize=10); ax1.grid(alpha=0.3)
     bins = np.arange(np.floor(mags.min() * 10) / 10, mags.max() + 0.2, 0.1)
@@ -303,10 +315,10 @@
     fig.legend(h_, l_, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=9, frameon=False, markerscale=3)
-    fig.tight_layout(); fig.savefig(PDFD / "24_01_nagano2014_catalog.pdf", bbox_inches="tight"); plt.close(fig)
-    print("[24_01] 図: PDF/24_01_nagano2014_catalog.pdf")
-    # 21_20・24: 試験の候補が 30 未満なら、評価できる試験の地震も 30 未満になることが確定する(INCONCLUSIVE)。波形を取る前に止める
+    fig.tight_layout(); fig.savefig(PDFD / "25_01_shimane2018_catalog.pdf", bbox_inches="tight"); plt.close(fig)
+    print("[25_01] 図: PDF/25_01_shimane2018_catalog.pdf")
+    # 21_20・24・25: 試験の候補が 30 未満なら、評価できる試験の地震も 30 未満になることが確定する(INCONCLUSIVE)。波形を取る前に止める
     nt = n["test_candidates_1p5_to_2p0_after_72h"]
     if nt < MIN_TEST:
-        sys.exit(f"[24_01] STOP: 試験の候補(本震 + 72 時間より後の 1.5 ≤ Mj < 2.0)が {nt}(< {MIN_TEST})。評価できる試験の地震は"
-                 f"これより多くならないので、21_04 と同じ規則で INCONCLUSIVE。波形は取らずに、この出力を事前登録 24 の規則どおり報告する")
-    print(f"[24_01] 試験の候補 {nt} ≥ {MIN_TEST}: 次へ進める(本当の試験の数は、キャッシュで P を測れた地震だけなので、これより少ない)")
+        sys.exit(f"[25_01] STOP: 試験の候補(本震 + 72 時間より後の 1.5 ≤ Mj < 2.0)が {nt}(< {MIN_TEST})。評価できる試験の地震は"
+                 f"これより多くならないので、21_04 と同じ規則で INCONCLUSIVE。波形は取らずに、この出力を事前登録 25 の規則どおり報告する")
+    print(f"[25_01] 試験の候補 {nt} ≥ {MIN_TEST}: 次へ進める(本当の試験の数は、キャッシュで P を測れた地震だけなので、これより少ない)")
```

## 25_02_shimane2018_hinet_to_h5.py ← 24_02_nagano2014_hinet_to_h5.py

```diff
--- ../nagano/frz/24_02_nagano2014_hinet_to_h5.py	2026-11-15 05:21:00.094713914 +0000
+++ frz/25_02_shimane2018_hinet_to_h5.py	2026-11-17 01:57:17.162700794 +0000
@@ -2,22 +2,20 @@
 # =============================================================================
-# Script : 24_02_nagano2014_hinet_to_h5.py  (v1)
-#          [長野県北部 2014 の Hi-net の連続波形を、地震の前後だけ取り、鳥取 2026 の h5(tottori_all_100Hz.h5)と
+# Script : 25_02_shimane2018_hinet_to_h5.py  (v1)
+#          [島根県西部 2018 の Hi-net の連続波形を、地震の前後だけ取り、鳥取 2026 の h5(tottori_all_100Hz.h5)と
 #           同じ形(30 秒窓・3 成分・100 Hz・窓ごと成分ごとの z-score・日本時間の epoch)の h5 にする。あわせて、z-score の前の
 #           窓ごと成分ごとの平均と標準偏差(win_mean・win_std)も書く(24_07 が元の値に戻して、τ までの波形だけで検測するため)]
-# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の 2 つ目
-# 派生元 : 21_20b_osaka2018_hinet_to_h5.py v1(SHA-256 43154e7a3b33451d6a2526f4a1b3ff4a8e6085964c380398ceab49b50745e06e。21_04b v1.1 と同じ取り方)。
-#          取り方・z-score・局の選び方・組み立て・ゲート(G-ref・G-dup・G-cover・G-clock・G-spec)・閾値は 21_20b v1 と 1 字も変えていない。
-#          変えたのは次だけ(DIFF_LOG_24.md):
-#          (1) 入力と出力の名前: jma_nagano2014.csv・24_01_nagano2014_catalog.json・ARGUS_nagano2014・nagano2014_100Hz.h5・
-#              stations_nagano2014.csv・data/24_02_*.json・data/24_02.lock・PDF/24_02_*.pdf、表示の [24_02]、h5 の出どころの属性の名前
-#          (2) 窓ごとの尺度の保存(新): zscore_windows が z と一緒に、z-score に使った成分ごとの平均と標準偏差 (窓, 3, 2) を返し、
-#              区切りのファイル(blk_*.npz)に scale として書き、組み立てで h5 の /win_mean・/win_std (窓, 3)(float64)に書く。
-#              /waves(z-score)の値・形・dtype は 21_20b と同じで、24_03(= 15_01c v3.3 の計算)は /waves だけを読む。
-#          (3) G-clock だけの FAIL の時の表示の文を、事前登録 24 と 24_04d に合わせた(止まり方と _FAILED の名前は同じ)
-#          (4) VERSION を "v1 (=21_20b v1 + window scale)" にした
+# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の入力の 2 つ目
+# 派生元 : 24_02_nagano2014_hinet_to_h5.py v1(SHA-256 0f2283af1e3a0fde831e96bd598284a04ba1ff4a64634fefb1dba65d39f8f69f。事前登録 24 で凍結。
+#          = 21_20b v1 に窓ごとの尺度の保存を足したもの)。
+#          取り方・z-score・尺度の保存・局の選び方・組み立て・ゲート(G-ref・G-dup・G-cover・G-clock・G-spec)・閾値は 24_02 v1 と
+#          1 字も変えていない。変えたのは次だけ(DIFF_LOG_25.md):
+#          (1) 入力と出力の名前: jma_shimane2018.csv・25_01_shimane2018_catalog.json・ARGUS_shimane2018・shimane2018_100Hz.h5・
+#              stations_shimane2018.csv・data/25_02_*.json・data/25_02.lock・PDF/25_02_*.pdf、表示の [25_02]、h5 の出どころの属性の名前
+#          (2) G-clock だけの FAIL の時の表示の文の「事前登録 24」→「事前登録 25」
+#          (3) VERSION を "v1 (=24_02 v1 = 21_20b v1 + window scale)" にした
 #
 # なぜ必要か:
-#   24 は 21_02・21_04・21_20 と同じ規則・同じ作り方(15_01c v3.3 と同じ計算の 24_03 で検測したキャッシュ)で確かめる。15_01c は
+#   25 は 21_02・21_04・21_20・24 と同じ規則・同じ作り方(15_01c v3.3 と同じ計算の 25_03 で検測したキャッシュ)で確かめる。15_01c は
 #   tottori_all_100Hz.h5 の形(/waves (N, 3, 3000)、/stations、/window_epoch = 窓の始まりの日本時間を UTC とみなした
-#   epoch 秒、属性 channel_order・n_samples・fs)を読む。そこで 2014 の波形をこの形にそろえ、15_01c の検測・QC・
+#   epoch 秒、属性 channel_order・n_samples・fs)を読む。そこで 2018 の波形をこの形にそろえ、15_01c の検測・QC・
 #   組み立てをそのまま通す(15_01c v3.3 で変えたのは、窓の索引のファイル名とその確かめ方・出力の置き場所 --base・
@@ -34,8 +32,8 @@
 #   1. 観測点: NIED の Hi-net(0101)の観測点の一覧(HinetPy の get_station_list。今の一覧。緯度・経度・標高のどれかが無い局は
-#      除く)から、本震(24_01 の JSON)に近い順に --n-sta + 10 局を候補にする。Hi-net のアカウントの「選んだ局」を
-#      最初の 1 回だけ data/24_02_initial_selection.json に保存してから候補を選び、終わり(止めた時・失敗した時も)に元に戻す。
+#      除く)から、本震(25_01 の JSON)に近い順に --n-sta + 10 局を候補にする。Hi-net のアカウントの「選んだ局」を
+#      最初の 1 回だけ data/25_02_initial_selection.json に保存してから候補を選び、終わり(止めた時・失敗した時も)に元に戻す。
 #      選んだ後の選択が空(= 全局)か候補の外の局を含めば STOP(全局のまま取ると何倍も時間がかかる)。
-#      途中で落ちて戻せなかった時は --restore-selection で戻せる。同時に 2 つ回さないよう data/24_02.lock を置く
+#      途中で落ちて戻せなかった時は --restore-selection で戻せる。同時に 2 つ回さないよう data/25_02.lock を置く
 #      (区切りごとに新しくし、30 分より古い印は止まった実行の印とみなす。Colab が切れた直後は --restore-selection --break-lock)。
-#   2. 取る時間の区切り: 24_01 の CSV の Mj ≥ 1.5 の地震ごとに、[発生時刻 − 10 s を分に切り下げ, 発生時刻 + 45 s を
+#   2. 取る時間の区切り: 25_01 の CSV の Mj ≥ 1.5 の地震ごとに、[発生時刻 − 10 s を分に切り下げ, 発生時刻 + 45 s を
 #      分に切り上げ](日本時間)。15_01c が使う区間 [発生 − 10 s, 発生 + 45 s] を 30 秒窓で必ず覆う。間が 2 分以下の
@@ -62,9 +60,9 @@
 #      区切りの半分以上でデータがある局のうち本震に近い順に --n-sta 局(既定 50。鳥取 2026 の局の数と同じ)を選び、その局の
-#      窓だけを書く。data/catalog/stations_nagano2014.csv(列 id, latitude, longitude, elevation。緯度・経度は 2014 年の
+#      窓だけを書く。data/catalog/stations_shimane2018.csv(列 id, latitude, longitude, elevation。緯度・経度は 2018 年の
 #      チャンネル表、標高は NIED の一覧の height(m)。stations.csv と同じ列)も書く。
-#      ゲートを書きかけのファイル(.part)で確かめ、全て通った時だけ data/waves/nagano2014_100Hz.h5 の名前にする
-#      (通らなければ nagano2014_100Hz_FAILED.h5 にして STOP。24_03 に渡る名前の h5 は作らない。G-clock だけの FAIL の扱いは
-#      事前登録 24 に先に決めてある: 記録だけで、_FAILED の h5 と stations_nagano2014.csv.part を 24_03 に渡し、時刻は G-clock2 で決める)。
+#      ゲートを書きかけのファイル(.part)で確かめ、全て通った時だけ data/waves/shimane2018_100Hz.h5 の名前にする
+#      (通らなければ shimane2018_100Hz_FAILED.h5 にして STOP。25_03 に渡る名前の h5 は作らない。G-clock だけの FAIL の扱いは
+#      事前登録 25 に先に決めてある: 記録だけで、_FAILED の h5 と stations_shimane2018.csv.part を 25_03 に渡し、時刻は G-clock2 で決める)。
 #      --partial(煙試験の確認): 取った区切りだけで組み立て、名前に _partial を付ける。
-#   5. ゲート(組み立ての後に表示し、data/24_02_report.json に合否と一緒に書く):
+#   5. ゲート(組み立ての後に表示し、data/25_02_report.json に合否と一緒に書く):
 #      - G-ref: 参照の h5 の z-score の確認に合格(fs = 100)。出力も同じ確認に合格
@@ -82,3 +80,3 @@
 #        違いがあれば限界に書く)
-#   6. 図: PDF/24_02_coverage.pdf(局 × 区切りのデータの有無)、PDF/24_02_mainshock.pdf(本震の上下動の
+#   6. 図: PDF/25_02_coverage.pdf(局 × 区切りのデータの有無)、PDF/25_02_mainshock.pdf(本震の上下動の
 #      記録の並びと、予想の P の印)。白背景・英語・凡例は枠の外。
@@ -87,8 +85,8 @@
 #   win32tools の catwin32・win2sac_32 が PATH にある(ノートの セル 3)、HinetPy 0.13.0。
-# 止める条件(STOP): 資格情報が無い・win2sac_32 が無い・参照の h5 が読めないか形が違うか fs が無い・24_01 の JSON が無い・
+# 止める条件(STOP): 資格情報が無い・win2sac_32 が無い・参照の h5 が読めないか形が違うか fs が無い・25_01 の JSON が無い・
 #   置き場所が足りない見込み・局の選択が効かない・別の実行の印がある・3 回ずつ試して取れない区切りが 3 つ続く・組み立てで取っていない
 #   区切りがあるか読めないファイルがある・使える局が 0・窓が 0・G-ref・G-dup・G-cover < 0.80・G-clock の失敗。
-# 限界(24 の限界にも書く):
+# 限界(25 の限界にも書く):
 #   - 観測点は Hi-net(0101)だけで、鳥取 2026 の 50 局(Hi-net のほか京大防災研・気象庁などを含む)とは種類と並びが違う
-#   - 候補は今の NIED の一覧から選ぶので、2014 年にあって今は無い局は入らない
+#   - 候補は今の NIED の一覧から選ぶので、2018 年にあって今は無い局は入らない
 #   - 地震の前後だけを取る(連続ではない)。15_01c が使う区間は全て含む。区切りの中で欠けがある局は、その区切りでは使わない
@@ -96,13 +94,13 @@
 #
-# Usage : (Colab、ノート 24_nagano2014_colab.ipynb の セル N6〜N9。手順は 24_STEPS_JA.md)
-#   計画だけ:       !python /content/drive/MyDrive/ARGUS/src/24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5> --dry-run
-#   煙試験(本震の区間に掛かる区切りを先に 3 区切り): !python .../24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5> --max-blocks 3
-#                    続けて !python .../24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5> --assemble --partial(取った分だけでゲートを見る)
-#   本番(続きから):   !python .../24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5>
-#   組み立て:         !python .../24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5> --assemble
-#   選択を戻すだけ:   !python .../24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5> --restore-selection [--break-lock](セル N8b)
-# Output (--out の下。既定 /content/drive/MyDrive/ARGUS_nagano2014):
-#   data/blocks/blk_*.npz / data/24_02_plan.json / data/24_02_initial_selection.json /
-#   data/waves/nagano2014_100Hz.h5 / data/catalog/stations_nagano2014.csv / data/24_02_report.json /
-#   PDF/24_02_coverage.pdf / PDF/24_02_mainshock.pdf(--partial ではそれぞれ _partial 付き)
+# Usage : (Colab、ノート 25_shimane2018_colab.ipynb の セル N6〜N9。手順は 25_STEPS_JA.md)
+#   計画だけ:       !python /content/drive/MyDrive/ARGUS/src/25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5> --dry-run
+#   煙試験(本震の区間に掛かる区切りを先に 3 区切り): !python .../25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5> --max-blocks 3
+#                    続けて !python .../25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5> --assemble --partial(取った分だけでゲートを見る)
+#   本番(続きから):   !python .../25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5>
+#   組み立て:         !python .../25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5> --assemble
+#   選択を戻すだけ:   !python .../25_02_shimane2018_hinet_to_h5.py --ref-h5 <参照の h5> --restore-selection [--break-lock](セル N8b)
+# Output (--out の下。既定 /content/drive/MyDrive/ARGUS_shimane2018):
+#   data/blocks/blk_*.npz / data/25_02_plan.json / data/25_02_initial_selection.json /
+#   data/waves/shimane2018_100Hz.h5 / data/catalog/stations_shimane2018.csv / data/25_02_report.json /
+#   PDF/25_02_coverage.pdf / PDF/25_02_mainshock.pdf(--partial ではそれぞれ _partial 付き)
 #   区切りのファイルは組み立ての後も消さない(h5 を作り直せるように。要らなくなったら data/blocks を手で消す)
@@ -129,3 +127,3 @@
 
-VERSION = "v1 (=21_20b v1 + window scale)"   # 24_02 の 1 版目(取り方は 21_20b v1 = 21_04b v1.1 と同じ。窓ごとの尺度を足した)
+VERSION = "v1 (=24_02 v1 = 21_20b v1 + window scale)"   # 25_02 の 1 版目(計算は 24_02 v1 と同じ。取り方は 21_20b v1 = 21_04b v1.1 と同じ)
 ROOT = Path(__file__).resolve().parent.parent
@@ -182,3 +180,3 @@
 
-BLK_KEYS = ("stations", "epoch", "waves", "chan", "stat", "scale")   # 24_02: scale を足した
+BLK_KEYS = ("stations", "epoch", "waves", "chan", "stat", "scale")   # 25_02: scale を足した
 
@@ -237,3 +235,3 @@
     """arr3: (3, n) → 窓ごとの (z (k, 3, 3000), 使った窓の番号, 尺度 (k, 3, 2) = 成分ごとの [平均, 標準偏差])。窓ごと・成分ごとの z-score。
-    24_02: 尺度を返すのを足した(z の計算は 21_20b と同じ)"""
+    25_02: 尺度を返すのを足した(z の計算は 21_20b と同じ)"""
     nwin = arr3.shape[1] // WIN_N
@@ -247,3 +245,3 @@
         zs.append(((seg - seg.mean(axis=1, keepdims=True)) / sd[:, None]).astype(dtype)); ks.append(k)
-        sc.append(np.stack([seg.mean(axis=1), sd], axis=1))                     # 24_02: (3, 2) = [平均, 標準偏差](z と同じ値で計算)
+        sc.append(np.stack([seg.mean(axis=1), sd], axis=1))                     # 25_02: (3, 2) = [平均, 標準偏差](z と同じ値で計算)
     return (np.stack(zs) if zs else np.zeros((0, 3, WIN_N), dtype)), ks, (np.stack(sc) if sc else np.zeros((0, 3, 2)))
@@ -283,10 +281,10 @@
         for k in ("waves", "stations", "window_epoch"):
-            if k not in H: sys.exit(f"[24_02] STOP(G-ref): 参照の h5 に /{k} が無い")
+            if k not in H: sys.exit(f"[25_02] STOP(G-ref): 参照の h5 に /{k} が無い")
         W = H["waves"]
-        if tuple(W.shape[1:]) != (3, WIN_N): sys.exit(f"[24_02] STOP(G-ref): 参照の /waves の形 {W.shape} が (N, 3, 3000) でない")
+        if tuple(W.shape[1:]) != (3, WIN_N): sys.exit(f"[25_02] STOP(G-ref): 参照の /waves の形 {W.shape} が (N, 3, 3000) でない")
         attrs = {k: (v.decode() if isinstance(v, bytes) else (v.tolist() if hasattr(v, "tolist") else v)) for k, v in H.attrs.items()}
         fsv = attrs.get("fs", attrs.get("sampling_rate"))
-        if fsv is None: sys.exit("[24_02] STOP(G-ref): 参照の h5 に属性 fs が無い")
+        if fsv is None: sys.exit("[25_02] STOP(G-ref): 参照の h5 に属性 fs が無い")
         fs = float(np.ravel(fsv)[0])
-        if abs(fs - FS) > 1e-6: sys.exit(f"[24_02] STOP(G-ref): 参照の fs = {fs}")
+        if abs(fs - FS) > 1e-6: sys.exit(f"[25_02] STOP(G-ref): 参照の fs = {fs}")
         n = W.shape[0]
@@ -311,3 +309,3 @@
     u, p = os.environ.get("HINET_USER"), os.environ.get("HINET_PASS")
-    if not u or not p: sys.exit("[24_02] STOP: 環境変数 HINET_USER・HINET_PASS が無い(ノートの セル 4 で入れる)")
+    if not u or not p: sys.exit("[25_02] STOP: 環境変数 HINET_USER・HINET_PASS が無い(ノートの セル 4 で入れる)")
     from HinetPy import Client
@@ -320,5 +318,5 @@
         client.select_stations(NET, names if names else None)
-        print(f"[24_02] アカウントの局の選択を元に戻した({len(names) if names else '全局'})")
+        print(f"[25_02] アカウントの局の選択を元に戻した({len(names) if names else '全局'})")
     except Exception as e:                                  # 戻せなかった時は必ず表示する
-        print(f"[24_02] 注意: アカウントの局の選択を戻せなかった({e})。Hi-net のサイトで確かめる。保存した選択: {sel_path}")
+        print(f"[25_02] 注意: アカウントの局の選択を戻せなかった({e})。Hi-net のサイトで確かめる。保存した選択: {sel_path}")
 
@@ -370,3 +368,3 @@
     if lock.exists() and time.time() - lock.stat().st_mtime < LOCK_STALE_S:
-        sys.exit(f"[24_02] STOP: 別の実行が動いている印 {lock}({lock.read_text().strip()})が 30 分以内に更新されている。"
+        sys.exit(f"[25_02] STOP: 別の実行が動いている印 {lock}({lock.read_text().strip()})が 30 分以内に更新されている。"
                  "Colab が切れた直後なら別の実行は無いので、セル 8b(--restore-selection --break-lock)を回してからセル 8 をもう一度")
@@ -392,8 +390,8 @@
     extra = [f.name for f in allf if f.name not in exp]
-    if extra: print(f"[24_02] 注意: 今の計画に無い区切りのファイル {len(extra)} は使わない(例 {extra[:3]})")
+    if extra: print(f"[25_02] 注意: 今の計画に無い区切りのファイル {len(extra)} は使わない(例 {extra[:3]})")
     files = [f for f in allf if f.name in exp]
     bad = [f.name for f in files if not blk_ok(f)]
-    if bad: sys.exit(f"[24_02] STOP: 読めない区切りのファイルが {len(bad)} ある(例 {bad[:3]})。消してから取り直す(セル 8)")
+    if bad: sys.exit(f"[25_02] STOP: 読めない区切りのファイルが {len(bad)} ある(例 {bad[:3]})。消してから取り直す(セル 8)")
     missing = sorted(exp - {f.name for f in files})
-    if not files: sys.exit("[24_02] STOP: 区切りの結果が 1 つも無い")
+    if not files: sys.exit("[25_02] STOP: 区切りの結果が 1 つも無い")
     pres, chan = {}, {}
@@ -408,6 +406,6 @@
         if not (allow_missing and frac >= MIN_FETCHED):
-            sys.exit(f"[24_02] STOP: 取っていない区切りが {len(missing)} ある(取れた割合 {frac:.3f}、例 {missing[:3]})。セル 8 を"
+            sys.exit(f"[25_02] STOP: 取っていない区切りが {len(missing)} ある(取れた割合 {frac:.3f}、例 {missing[:3]})。セル 8 を"
                      f"もう一度回してから --assemble。何度回しても取れない区切りだけが残り、取れた割合が {MIN_FETCHED} 以上なら "
                      "--allow-missing で続けてよい(事前に決めた規則。その区切りの地震は G-cover で覆えない地震として数える)")
-        print(f"[24_02] 注意(--allow-missing): 取っていない区切り {len(missing)}(取れた割合 {frac:.3f} ≥ {MIN_FETCHED})で続ける: {missing}")
+        print(f"[25_02] 注意(--allow-missing): 取っていない区切り {len(missing)}(取れた割合 {frac:.3f} ≥ {MIN_FETCHED})で続ける: {missing}")
     done_iv = []
@@ -425,5 +423,5 @@
     keep = ok[:n_sta]
-    if not keep: sys.exit("[24_02] STOP: 区切りの半分以上でデータがある局が 0")
-    if len(keep) < n_sta: print(f"[24_02] 注意: 区切りの半分以上でデータがある局が {len(keep)} しかない(--n-sta {n_sta})")
-    print(f"[24_02] 組み立て: 区切り {nb}(計画 {len(plan)})  使う局 {len(keep)}(最も遠い局 "
+    if not keep: sys.exit("[25_02] STOP: 区切りの半分以上でデータがある局が 0")
+    if len(keep) < n_sta: print(f"[25_02] 注意: 区切りの半分以上でデータがある局が {len(keep)} しかない(--n-sta {n_sta})")
+    print(f"[25_02] 組み立て: 区切り {nb}(計画 {len(plan)})  使う局 {len(keep)}(最も遠い局 "
           f"{haversine_km(ml, mo, cand_meta[keep[-1]]['lat'], cand_meta[keep[-1]]['lon']):.1f} km)")
@@ -431,3 +429,3 @@
     (OUT / "data" / "waves").mkdir(parents=True, exist_ok=True); (OUT / "data" / "catalog").mkdir(parents=True, exist_ok=True)
-    h5p = OUT / "data" / "waves" / ("nagano2014_100Hz_partial.h5" if partial else "nagano2014_100Hz.h5"); tmpp = h5p.with_suffix(".h5.part")
+    h5p = OUT / "data" / "waves" / ("shimane2018_100Hz_partial.h5" if partial else "shimane2018_100Hz.h5"); tmpp = h5p.with_suffix(".h5.part")
     if h5p.exists(): h5p.unlink()                              # 前の組み立ての結果は、ゲートに通るまで置かない
@@ -437,3 +435,3 @@
         z = np.load(f, allow_pickle=False); n_tot += int(np.isin(z["stations"], list(kset)).sum())
-    if n_tot == 0: sys.exit("[24_02] STOP: 書く窓が 0")
+    if n_tot == 0: sys.exit("[25_02] STOP: 書く窓が 0")
     chunks = tuple(min(c, n) for c, n in zip(ref["chunks"], (n_tot, 3, WIN_N))) if ref.get("chunks") else None
@@ -446,3 +444,3 @@
         E = H.create_dataset("window_epoch", (n_tot,), dtype=np.dtype(ref["epoch_dtype"]))
-        WM = H.create_dataset("win_mean", (n_tot, 3), dtype=np.float64); WS = H.create_dataset("win_std", (n_tot, 3), dtype=np.float64)   # 24_02
+        WM = H.create_dataset("win_mean", (n_tot, 3), dtype=np.float64); WS = H.create_dataset("win_std", (n_tot, 3), dtype=np.float64)   # 25_02
         i = 0
@@ -455,6 +453,6 @@
         H.attrs["channel_order"] = "UD,NS,EW"; H.attrs["n_samples"] = WIN_N; H.attrs["fs"] = FS
-        H.attrs["nagano2014_source"] = (f"NIED Hi-net (0101) continuous data via HinetPy, event blocks only; 24_02_nagano2014_hinet_to_h5.py "
+        H.attrs["shimane2018_source"] = (f"NIED Hi-net (0101) continuous data via HinetPy, event blocks only; 25_02_shimane2018_hinet_to_h5.py "
                                     f"{VERSION}; per-window per-component z-score (win_mean, win_std = the mean and std used; waves * win_std + win_mean restores the counts); "
                                     f"window_epoch = JST wall clock as UTC epoch")
-    stp = OUT / "data" / "catalog" / ("stations_nagano2014_partial.csv" if partial else "stations_nagano2014.csv")
+    stp = OUT / "data" / "catalog" / ("stations_shimane2018_partial.csv" if partial else "stations_shimane2018.csv")
     if stp.exists(): stp.unlink()
@@ -526,11 +524,11 @@
     all_pass = G["ref_pass"] and G["dup_pass"] and G["cover_pass"] and G["clock_pass"]
-    rep = dict(script="24_02_nagano2014_hinet_to_h5.py", version=VERSION, h5=str(h5p), n_windows=n_tot, stations=keep,
+    rep = dict(script="25_02_shimane2018_hinet_to_h5.py", version=VERSION, h5=str(h5p), n_windows=n_tot, stations=keep,
                presence={s: pres[s] for s in keep}, n_blocks=nb, n_blocks_planned=len(plan), n_blocks_missing=len(missing),
                missing_blocks=missing, allow_missing=bool(allow_missing), ref=ref, gates=G, all_gates_pass=bool(all_pass), partial=bool(partial))
-    json.dump(rep, open(OUT / "data" / ("24_02_report_partial.json" if partial else "24_02_report.json"), "w"), indent=1, default=str)
-    print(f"[24_02] G-ref: 参照 dtype {ref['waves_dtype']}・z-score 確認 {'PASS' if ref['zcheck_pass'] else 'FAIL'}  出力の z-score 確認 "
+    json.dump(rep, open(OUT / "data" / ("25_02_report_partial.json" if partial else "25_02_report.json"), "w"), indent=1, default=str)
+    print(f"[25_02] G-ref: 参照 dtype {ref['waves_dtype']}・z-score 確認 {'PASS' if ref['zcheck_pass'] else 'FAIL'}  出力の z-score 確認 "
           f"{'PASS' if G['out_zcheck']['pass_'] else 'FAIL'}(最大 |平均| {G['out_zcheck']['max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
           f"{G['out_zcheck']['max_abs_std_minus_1']:.3g})")
-    print(f"[24_02] G-dup: 重なり {G['dup']}  " + ("PASS" if G["dup"] == 0 else "FAIL"))
-    print(f"[24_02] G-cover({G['cover_n_events']} 地震): Mj ≥ 1.5 の地震で 4 局以上が覆う割合 {G['cover_frac_ge4']:.3f}(覆う局の数の中央値 "
+    print(f"[25_02] G-dup: 重なり {G['dup']}  " + ("PASS" if G["dup"] == 0 else "FAIL"))
+    print(f"[25_02] G-cover({G['cover_n_events']} 地震): Mj ≥ 1.5 の地震で 4 局以上が覆う割合 {G['cover_frac_ge4']:.3f}(覆う局の数の中央値 "
           f"{G['cover_median_stations']:.0f})  " + ("PASS" if G["cover_frac_ge4"] >= COVER_OK else "注意" if G["cover_frac_ge4"] >= COVER_STOP else "FAIL"))
@@ -538,7 +536,7 @@
         cm = c["median_abs_resid_s"]
-        print(f"[24_02] G-clock{'(本震)' if c['mainshock'] else '(他の地震)'} {c['origin_jst'][:22]} Mj {c['mj']}: 近い局 {c['n']} で、"
+        print(f"[25_02] G-clock{'(本震)' if c['mainshock'] else '(他の地震)'} {c['origin_jst'][:22]} Mj {c['mj']}: 近い局 {c['n']} で、"
               f"STA/LTA の立ち上がり − 震源距離/6.0 km/s の |差| の中央値 {'—' if cm is None else f'{cm:.2f}'} s  "
               + ("PASS" if c["pass_"] else ("FAIL" if c["mainshock"] or c["n"] >= 4 else "判定なし(立ち上がりが取れた局が 4 未満)")))
-    print(f"[24_02] G-clock まとめ: " + ("PASS" if G["clock_pass"] else "FAIL"))
-    print(f"[24_02] G-spec(記録だけ): 0.1–1 Hz / 1–20 Hz の力の比の中央値 参照 {G['band_ratio_ref']:.3g}・出力 {G['band_ratio_out']:.3g}"
+    print(f"[25_02] G-clock まとめ: " + ("PASS" if G["clock_pass"] else "FAIL"))
+    print(f"[25_02] G-spec(記録だけ): 0.1–1 Hz / 1–20 Hz の力の比の中央値 参照 {G['band_ratio_ref']:.3g}・出力 {G['band_ratio_out']:.3g}"
           f"(比 {rr:.2f})" + ("  注意: 3 倍以上違う(参照の h5 でフィルタをかけた可能性。記録だけで、止めずに先に進む。限界に書く)"
@@ -549,9 +547,9 @@
         why = [k for k, v in (("G-ref", G["ref_pass"]), ("G-dup", G["dup_pass"]), ("G-cover", G["cover_pass"]), ("G-clock", G["clock_pass"])) if not v]
-        if why == ["G-clock"]:                                 # 21_20・24: 表示の文だけ(止まり方は 21_04b v1.1 と同じ)
-            sys.exit(f"[24_02] STOP(G-clock だけ): h5 は {failed.name}、局の表は {stp.name}.part にした。事前登録 24 の規則では "
-                     "G-clock は記録だけで、時刻は G-clock2(24_04d)で決める。セル N10 に、この 2 つのファイルを渡して進む(この出力を貼る)")
-        sys.exit(f"[24_02] STOP({', '.join(why)}): h5 は {failed.name} にした(セル 10 には進まない。この出力を貼って相談)")
+        if why == ["G-clock"]:                                 # 21_20・24・25: 表示の文だけ(止まり方は 21_04b v1.1 と同じ)
+            sys.exit(f"[25_02] STOP(G-clock だけ): h5 は {failed.name}、局の表は {stp.name}.part にした。事前登録 25 の規則では "
+                     "G-clock は記録だけで、時刻は G-clock2(25_04d)で決める。セル N10 に、この 2 つのファイルを渡して進む(この出力を貼る)")
+        sys.exit(f"[25_02] STOP({', '.join(why)}): h5 は {failed.name} にした(セル 10 には進まない。この出力を貼って相談)")
     os.replace(tmpp, h5p); os.replace(stp.with_suffix(".csv.part"), stp)
     sfx = "_partial" if partial else ""
-    print(f"[24_02] 出力: {h5p}(窓 {n_tot})  {OUT / 'data' / 'catalog' / f'stations_nagano2014{sfx}.csv'}  {OUT / 'data' / f'24_02_report{sfx}.json'}"
+    print(f"[25_02] 出力: {h5p}(窓 {n_tot})  {OUT / 'data' / 'catalog' / f'stations_shimane2018{sfx}.csv'}  {OUT / 'data' / f'25_02_report{sfx}.json'}"
           + ("(煙試験の確認用。本番の組み立てはセル 9)" if partial else ""))
@@ -573,3 +571,3 @@
     cb = fig.colorbar(im, ax=ax, pad=0.01); cb.set_label("Fraction kept")
-    fig.tight_layout(); fig.savefig(PDFD / f"24_02_coverage{suf}.pdf", bbox_inches="tight"); plt.close(fig)
+    fig.tight_layout(); fig.savefig(PDFD / f"25_02_coverage{suf}.pdf", bbox_inches="tight"); plt.close(fig)
     if sec:
@@ -589,3 +587,3 @@
         ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False); ax.grid(alpha=0.3, axis="x")
-        fig.tight_layout(); fig.savefig(PDFD / f"24_02_mainshock{suf}.pdf", bbox_inches="tight"); plt.close(fig)
+        fig.tight_layout(); fig.savefig(PDFD / f"25_02_mainshock{suf}.pdf", bbox_inches="tight"); plt.close(fig)
 
@@ -595,7 +593,7 @@
     ap = argparse.ArgumentParser()
-    ap.add_argument("--catalog", default=str(ROOT / "data" / "catalog" / "jma_nagano2014.csv"))
-    ap.add_argument("--summary", default=str(ROOT / "data" / "catalog" / "24_01_nagano2014_catalog.json"))
+    ap.add_argument("--catalog", default=str(ROOT / "data" / "catalog" / "jma_shimane2018.csv"))
+    ap.add_argument("--summary", default=str(ROOT / "data" / "catalog" / "25_01_shimane2018_catalog.json"))
     ap.add_argument("--ref-h5", required=True, help="鳥取 2026 の tottori_all_100Hz.h5(形を写すため。読むだけ)")
-    ap.add_argument("--out", default=("/content/drive/MyDrive/ARGUS_nagano2014" if Path("/content/drive").exists()
-                                      else str(ROOT.parent / "ARGUS_nagano2014")))
+    ap.add_argument("--out", default=("/content/drive/MyDrive/ARGUS_shimane2018" if Path("/content/drive").exists()
+                                      else str(ROOT.parent / "ARGUS_shimane2018")))
     ap.add_argument("--tmp", default=("/content/hinet_tmp" if Path("/content").exists() else tempfile.gettempdir()))
@@ -608,3 +606,3 @@
     ap.add_argument("--restore-selection", action="store_true", help="アカウントの局の選択を保存した元の状態に戻すだけ(途中で落ちた時)")
-    ap.add_argument("--break-lock", action="store_true", help="--restore-selection と一緒に: 切れた実行の印(data/24_02.lock)を消す")
+    ap.add_argument("--break-lock", action="store_true", help="--restore-selection と一緒に: 切れた実行の印(data/25_02.lock)を消す")
     a = ap.parse_args()
@@ -613,3 +611,3 @@
     tmp_root = Path(a.tmp); tmp_root.mkdir(parents=True, exist_ok=True)
-    if not Path(a.summary).exists(): sys.exit(f"[24_02] STOP: {a.summary} が無い(24_01 を先に回す)")
+    if not Path(a.summary).exists(): sys.exit(f"[25_02] STOP: {a.summary} が無い(25_01 を先に回す)")
     summ = json.load(open(a.summary))
@@ -622,15 +620,15 @@
     tot_min = sum(s for _, s in plan)
-    print(f"[24_02] {VERSION}  地震(Mj ≥ 1.5){len(org)} → 区切り {len(plan)}(分の合計 {tot_min}、最長 {max(s for _, s in plan)} 分)")
+    print(f"[25_02] {VERSION}  地震(Mj ≥ 1.5){len(org)} → 区切り {len(plan)}(分の合計 {tot_min}、最長 {max(s for _, s in plan)} 分)")
     rng = np.random.default_rng(7)
     ref = read_ref(a.ref_h5, rng)
-    print(f"[24_02] 参照の h5: 窓 {ref['n_windows']}  /waves {ref['waves_dtype']}  /stations {ref['stations_dtype']}  "
+    print(f"[25_02] 参照の h5: 窓 {ref['n_windows']}  /waves {ref['waves_dtype']}  /stations {ref['stations_dtype']}  "
           f"/window_epoch {ref['epoch_dtype']}  chunks {ref['chunks']}  圧縮 {ref['compression']}  属性 {ref['attrs']}  "
           f"他のデータ {ref['other_datasets']}")
-    print(f"[24_02] 参照の z-score の確認(無作為 {REF_NSAMPLE} 窓): 最大 |平均| {ref['zcheck_max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
+    print(f"[25_02] 参照の z-score の確認(無作為 {REF_NSAMPLE} 窓): 最大 |平均| {ref['zcheck_max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
           f"{ref['zcheck_max_abs_std_minus_1']:.3g}  " + ("PASS" if ref["zcheck_pass"] else "FAIL")
           + f"  30 s 格子にそろう割合 {ref['grid30_frac']:.3f}(余り {ref['grid30_residues']})  0.1–1/1–20 Hz の力の比 {ref['band_ratio_median']:.3g}")
-    if not ref["zcheck_pass"]: sys.exit("[24_02] STOP(G-ref): 参照の h5 が窓ごとの z-score に見えない(この行を貼って相談)")
+    if not ref["zcheck_pass"]: sys.exit("[25_02] STOP(G-ref): 参照の h5 が窓ごとの z-score に見えない(この行を貼って相談)")
     dt = np.dtype(ref["waves_dtype"])
-    plan_p = OUT / "data" / "24_02_plan.json"
-    sel_p = OUT / "data" / "24_02_initial_selection.json"
+    plan_p = OUT / "data" / "25_02_plan.json"
+    sel_p = OUT / "data" / "25_02_initial_selection.json"
 
@@ -638,13 +636,13 @@
         P = json.load(open(plan_p)) if plan_p.exists() else None
-        if P is None: sys.exit("[24_02] STOP: 計画の 24_02_plan.json が無い")
+        if P is None: sys.exit("[25_02] STOP: 計画の 25_02_plan.json が無い")
         assemble(OUT, PDFD, ref, summ, rows, P["candidates"], a.n_sta, plan, partial=a.partial, allow_missing=a.allow_missing); return
 
-    lock = OUT / "data" / "24_02.lock"
+    lock = OUT / "data" / "25_02.lock"
     if a.restore_selection:
         if a.break_lock and lock.exists():
-            print(f"[24_02] 切れた実行の印を消した: {lock.read_text().strip()}"); lock.unlink()
+            print(f"[25_02] 切れた実行の印を消した: {lock.read_text().strip()}"); lock.unlink()
         check_lock(lock)                                       # 動いている実行があれば、その選択を変えない
-        if not sel_p.exists(): sys.exit(f"[24_02] STOP: 保存した選択 {sel_p} が無い")
+        if not sel_p.exists(): sys.exit(f"[25_02] STOP: 保存した選択 {sel_p} が無い")
         restore_selection(hinet_client(), sel_p); return
-    if not shutil.which("win2sac_32") and not a.dry_run: sys.exit("[24_02] STOP: win2sac_32 が PATH に無い(ノートの セル 3)")
+    if not shutil.which("win2sac_32") and not a.dry_run: sys.exit("[25_02] STOP: win2sac_32 が PATH に無い(ノートの セル 3)")
     client = hinet_client()
@@ -654,3 +652,3 @@
     stl = [s for s in stl if s.latitude is not None and s.longitude is not None and s.elevation is not None]
-    if len(stl) < n0: print(f"[24_02] 緯度・経度・標高のどれかが無い局 {n0 - len(stl)} は候補から外した")
+    if len(stl) < n0: print(f"[25_02] 緯度・経度・標高のどれかが無い局 {n0 - len(stl)} は候補から外した")
     stl.sort(key=lambda s: haversine_km(ml, mo, s.latitude, s.longitude))
@@ -659,3 +657,3 @@
                           dist_km=float(haversine_km(ml, mo, s.latitude, s.longitude))) for s in cands}
-    print(f"[24_02] 候補局 {len(cands)}(本震から {cmeta[cands[0].name]['dist_km']:.1f}〜{cmeta[cands[-1].name]['dist_km']:.1f} km): "
+    print(f"[25_02] 候補局 {len(cands)}(本震から {cmeta[cands[0].name]['dist_km']:.1f}〜{cmeta[cands[-1].name]['dist_km']:.1f} km): "
           + " ".join(s.name for s in cands))
@@ -665,6 +663,6 @@
     free = shutil.disk_usage(OUT).free / 1e9
-    print(f"[24_02] 置き場所の見込み: 区切りのファイル約 {gb:.1f} GB + 組み立てた h5 約 {gb * a.n_sta / len(cands):.1f} GB"
+    print(f"[25_02] 置き場所の見込み: 区切りのファイル約 {gb:.1f} GB + 組み立てた h5 約 {gb * a.n_sta / len(cands):.1f} GB"
           f"(Drive の空き {free:.0f} GB。ここに出るのは Colab から見た空きで、Drive の契約の上限とは違うことがある)")
     if a.dry_run:
-        print(f"[24_02] 計画だけ(--dry-run): {plan_p}。1 区切りに 30 s かかるとして約 {len(plan) * 30 / 3600:.1f} 時間、"
+        print(f"[25_02] 計画だけ(--dry-run): {plan_p}。1 区切りに 30 s かかるとして約 {len(plan) * 30 / 3600:.1f} 時間、"
               f"60 s なら約 {len(plan) * 60 / 3600:.1f} 時間(煙試験で測る)")
@@ -678,3 +676,3 @@
             json.dump(dict(saved_utc=datetime.now(timezone.utc).isoformat(), stations=names0), open(sel_p, "w"), indent=1)
-            print(f"[24_02] アカウントの今の局の選択を保存した({len(names0) if names0 else '全局'}): {sel_p}")
+            print(f"[25_02] アカウントの今の局の選択を保存した({len(names0) if names0 else '全局'}): {sel_p}")
         for f in (OUT / "data" / "blocks").glob("*.tmp"): f.unlink()          # 前に途中で切れた書きかけ
@@ -683,6 +681,6 @@
             if f.exists() and not blk_ok(f):
-                print(f"[24_02] 読めない区切りのファイル {f.name} を消して取り直す"); f.unlink()
+                print(f"[25_02] 読めない区切りのファイル {f.name} を消して取り直す"); f.unlink()
         todo = [(b, s) for b, s in plan if not blk_done(OUT, b, s)]
         need = (sum(s for _, s in todo) * 2 * len(cands) * 3 * WIN_N * dt.itemsize / 1e9) + gb * a.n_sta / len(cands)
-        if free < 1.1 * need: sys.exit(f"[24_02] STOP: 置き場所が足りない見込み(残りの区切りと h5 で約 {need:.1f} GB、空き {free:.0f} GB)")
+        if free < 1.1 * need: sys.exit(f"[25_02] STOP: 置き場所が足りない見込み(残りの区切りと h5 で約 {need:.1f} GB、空き {free:.0f} GB)")
         if a.max_blocks:                                     # 煙試験: 本震の区間 [−10 s, +45 s] に掛かる区切りを最初に(G-clock を早く確かめる)
@@ -693,6 +691,6 @@
         n_done = sum(1 for b, s in plan if blk_done(OUT, b, s))
-        print(f"[24_02] 取る区切り {len(todo)}(済み {n_done}/{len(plan)})")
+        print(f"[25_02] 取る区切り {len(todo)}(済み {n_done}/{len(plan)})")
         names = [s.name for s in cands]
         if not todo:
-            print("[24_02] 取る区切りが無い(全部済み)。次はセル 9(--assemble)"); return
+            print("[25_02] 取る区切りが無い(全部済み)。次はセル 9(--assemble)"); return
         max_span = max(1, min(60, 12000 // (3 * len(names))))
@@ -705,4 +703,4 @@
         if not got or not set(got) <= set(names):
-            sys.exit(f"[24_02] STOP: アカウントの局の選択が候補にならなかった(選ばれた局 {len(got)})。全局のまま取ると何倍も時間がかかる")
-        if set(got) != set(names): print(f"[24_02] 注意: 選べた局 {len(got)} が候補 {len(names)} より少ない(無い局: {sorted(set(names) - set(got))[:10]})")
+            sys.exit(f"[25_02] STOP: アカウントの局の選択が候補にならなかった(選ばれた局 {len(got)})。全局のまま取ると何倍も時間がかかる")
+        if set(got) != set(names): print(f"[25_02] 注意: 選べた局 {len(got)} が候補 {len(names)} より少ない(無い局: {sorted(set(names) - set(got))[:10]})")
         for i, (b, s) in enumerate(todo):
@@ -727,3 +725,3 @@
                 print(f"    区切り {b:%Y-%m-%d %H:%M} ({s} 分) を {len(tries)} 回とも取れなかった(飛ばす。次に回すと取り直す)")
-                if fails >= 3: sys.exit("[24_02] STOP: 3 つの区切りで続けて取れなかった(Hi-net の状態を確かめて、もう一度回すと続きから)")
+                if fails >= 3: sys.exit("[25_02] STOP: 3 つの区切りで続けて取れなかった(Hi-net の状態を確かめて、もう一度回すと続きから)")
                 continue
@@ -744,3 +742,3 @@
     left = sum(1 for b, s in plan if not blk_done(OUT, b, s))
-    print(f"[24_02] 終わり: 残りの区切り {left}/{len(plan)}" + ("(全部済んだら --assemble)" if left == 0 else "(もう一度回すと続きから)"))
+    print(f"[25_02] 終わり: 残りの区切り {left}/{len(plan)}" + ("(全部済んだら --assemble)" if left == 0 else "(もう一度回すと続きから)"))
```

## 25_03_shimane2018_realpick_cache_colab.py ← 24_03_nagano2014_realpick_cache_colab.py

```diff
--- ../nagano/frz/24_03_nagano2014_realpick_cache_colab.py	2026-11-15 05:21:00.093896453 +0000
+++ frz/25_03_shimane2018_realpick_cache_colab.py	2026-11-17 01:57:17.161686145 +0000
@@ -2,17 +2,18 @@
 # =============================================================================
-# Script : 24_03_nagano2014_realpick_cache_colab.py  (v1)
-#          [長野県北部 2014 の h5(24_02)と気象庁の震源(24_01)から、PhaseNet で P・S を測り、ARGUS のキャッシュ
-#           (tottori_parsed_realpick_nagano2014_m15.pt)を作る。検測・QC・局の選び方・組み立て・振幅整合は 15_01c v3.3 と同じ計算]
-# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の 3 つ目
-# 派生元 : 21_20c_osaka2018_realpick_cache_colab.py v1(SHA-256 7b938b944003d99fcad7df188792e8e8eb95c71b07f1a1223bffad6671d04cf0)。
-#          検測・QC・組み立て・振幅整合・出力の中身は 21_20c v1(= 15_01c v3.3 と同じ計算)と 1 字も変えていない(DIFF_LOG_24.md)。
-#          変えたのは次だけ: (1) この冒頭の説明 (2) 出力の置き場所の既定 ARGUS_osaka2018 → ARGUS_nagano2014(Colab では --base で必ず渡す)
-#          (3) 引数の説明の文 (4) 表示の先頭 [24_03] → [24_03]、報告の script_version、図の題、最後の表示の Mac のコピー先
-#          (--tag に nagano2014 があれば data/nagano2014_processed/)、振幅整合の表示の「大阪」→「長野」。
-#          24_02 の h5 には win_mean・win_std も入っているが、このスクリプトは読まない(waves だけを読む。21_20c と同じ)。
-#          このキャッシュの後に 24_03h(R1: 発生の 15 s 前〜5 s 後に別の地震がある地震を除く)を必ず当てる(事前登録 24 の 3 節)。
-# 長野県北部 2014 の実行(ノート 24_nagano2014_colab.ipynb の セル N10・N11):
-#   !python 24_03_nagano2014_realpick_cache_colab.py --h5 <nagano2014_100Hz.h5(または _FAILED.h5)> --jma <jma_nagano2014.csv>
-#      --stations <stations_nagano2014.csv(または .csv.part)> --min-mag 1.5 --box <24_01 の JSON の box 4 つ>
-#      --base /content/ARGUS_nagano2014 --tag _nagano2014_m15 [--max-events 10 で煙試験。その時は --tag _nagano2014_smoke]
+# Script : 25_03_shimane2018_realpick_cache_colab.py  (v1)
+#          [島根県西部 2018 の h5(25_02)と気象庁の震源(25_01)から、PhaseNet で P・S を測り、ARGUS のキャッシュ
+#           (tottori_parsed_realpick_shimane2018_m15.pt)を作る。検測・QC・局の選び方・組み立て・振幅整合は 15_01c v3.3 と同じ計算]
+# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の入力の 3 つ目
+# 派生元 : 24_03_nagano2014_realpick_cache_colab.py v1(SHA-256 86b3cb1f810752eae9e1bee43e596621773d601d478cf270e0ca0db50101c60a。事前登録 24 で凍結。
+#          = 21_20c v1 = 15_01c v3.3 と同じ計算)。
+#          検測・QC・組み立て・振幅整合・出力の中身は 24_03 v1 と 1 字も変えていない(DIFF_LOG_25.md)。
+#          変えたのは次だけ: (1) この冒頭の説明 (2) 出力の置き場所の既定 ARGUS_nagano2014 → ARGUS_shimane2018(Colab では --base で必ず渡す)
+#          (3) 引数の説明の文 (4) 表示の先頭 [24_03] → [25_03]、報告の script_version、図の題、最後の表示の Mac のコピー先
+#          (--tag に shimane2018 があれば data/shimane2018_processed/)、振幅整合の表示の「長野」→「島根」。
+#          25_02 の h5 には win_mean・win_std も入っているが、このスクリプトは読まない(waves だけを読む。24_03・21_20c と同じ)。
+#          このキャッシュの後に 25_03h(R1: 発生の 15 s 前〜5 s 後に別の地震がある地震を除く)を必ず当てる(事前登録 25 の 3 節)。
+# 島根県西部 2018 の実行(ノート 25_shimane2018_colab.ipynb の セル N10・N11):
+#   !python 25_03_shimane2018_realpick_cache_colab.py --h5 <shimane2018_100Hz.h5(または _FAILED.h5)> --jma <jma_shimane2018.csv>
+#      --stations <stations_shimane2018.csv(または .csv.part)> --min-mag 1.5 --box <25_01 の JSON の box 4 つ>
+#      --base /content/ARGUS_shimane2018 --tag _shimane2018_m15 [--max-events 10 で煙試験。その時は --tag _shimane2018_smoke]
 #
@@ -116,4 +117,4 @@
 
-BASE = Path("/content/drive/MyDrive/ARGUS_nagano2014") \
-       if Path("/content/drive").exists() else Path(".") / "ARGUS_nagano2014"     # 24_03: 既定の置き場所(--base で渡す)
+BASE = Path("/content/drive/MyDrive/ARGUS_shimane2018") \
+       if Path("/content/drive").exists() else Path(".") / "ARGUS_shimane2018"     # 25_03: 既定の置き場所(--base で渡す)
 PDFD = BASE / "PDF"
@@ -140,5 +141,5 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--jma", required=True, help="24_01 の jma_nagano2014.csv(24_03: 必ず渡す)")
-ap.add_argument("--stations", required=True, help="24_02 の stations_nagano2014.csv(24_03: 必ず渡す)")
-ap.add_argument("--h5", required=True, help="24_02 の nagano2014_100Hz.h5 のパス")
+ap.add_argument("--jma", required=True, help="25_01 の jma_shimane2018.csv(25_03: 必ず渡す)")
+ap.add_argument("--stations", required=True, help="25_02 の stations_shimane2018.csv(25_03: 必ず渡す)")
+ap.add_argument("--h5", required=True, help="25_02 の shimane2018_100Hz.h5 のパス")
 ap.add_argument("--knet-cache", default="", help="(任意)あればフル統計を開示")
@@ -161,6 +162,6 @@
                 metavar=("LAT0", "LAT1", "LON0", "LON1"),
-                help="24_01 の JSON の box(24_03: 必ず渡す。西鳥取の既定は外した)")
+                help="25_01 の JSON の box(25_03: 必ず渡す。西鳥取の既定は外した)")
 ap.add_argument("--tag", default="", help="出力の名前に付ける印(例 _m15)。v3.1 で追加")
 ap.add_argument("--overwrite-canon", action="store_true", help="--tag 無しで既存の正本を上書きする時だけ付ける。v3.2 で追加")
-ap.add_argument("--base", default="", help="出力の置き場所(既定は Drive の ARGUS_nagano2014)。v3.3 で追加")
+ap.add_argument("--base", default="", help="出力の置き場所(既定は Drive の ARGUS_shimane2018)。v3.3 で追加")
 args = ap.parse_args()
@@ -171,5 +172,5 @@
 if abs(args.min_mag - 2.0) > 1e-9 and args.tag == "":
-    raise SystemExit("[24_03] STOP: --min-mag が 2.0 以外の時は --tag(例 _m15)を付ける(正本を上書きしないため)")
+    raise SystemExit("[25_03] STOP: --min-mag が 2.0 以外の時は --tag(例 _m15)を付ける(正本を上書きしないため)")
 if args.tag == "" and (OUTD / "tottori_parsed_realpick.pt").exists() and not args.overwrite_canon:
-    raise SystemExit("[24_03] STOP: 正本 tottori_parsed_realpick.pt が既にある。--tag を付けて回す"
+    raise SystemExit("[25_03] STOP: 正本 tottori_parsed_realpick.pt が既にある。--tag を付けて回す"
                      "(正本を作り直す時だけ --overwrite-canon)")
@@ -272,3 +273,3 @@
     PN_MODEL.eval()
-    print("[24_03] PhaseNet ('original') 読込完了")
+    print("[25_03] PhaseNet ('original') 読込完了")
 
@@ -302,3 +303,3 @@
 # ================================================================ 入力読み込み
-print(f"[24_03] JMAカタログ: {args.jma}")
+print(f"[25_03] JMAカタログ: {args.jma}")
 import csv as _csv
@@ -325,5 +326,5 @@
 if args.max_events: cat = cat[:args.max_events]
-print(f"[24_03] 対象イベント: {len(cat)} (M>={args.min_mag}, box={args.box}, "
+print(f"[25_03] 対象イベント: {len(cat)} (M>={args.min_mag}, box={args.box}, "
       f"JST→UTC変換済み, h5窓引き={args.h5_time_base}基準, 欠損行スキップ {n_badrow})")
-if not cat: sys.exit("[24_03] STOP: 対象イベント0件")
+if not cat: sys.exit("[25_03] STOP: 対象イベント0件")
 
@@ -334,3 +335,3 @@
                                        float(row["elevation"]))
-print(f"[24_03] 観測点: {len(sta_meta)}局 ({Path(args.stations).name})")
+print(f"[25_03] 観測点: {len(sta_meta)}局 ({Path(args.stations).name})")
 
@@ -345,3 +346,3 @@
     nan_frac = float(np.isnan(k_snr).mean())
-    print(f"[24_03] K-NET参照: {len(kevs)}ev  absmax中央値={KNET_ABSMAX_REF:.2f}  "
+    print(f"[25_03] K-NET参照: {len(kevs)}ev  absmax中央値={KNET_ABSMAX_REF:.2f}  "
           f"snr分布(NaN率{nan_frac:.1%}; 13_34rpではNaN→0) "
@@ -352,3 +353,3 @@
     KNET_ABSMAX_REF = float(args.knet_absmax_ref)
-    print(f"[24_03] K-NET参照: --knet-absmax-ref={KNET_ABSMAX_REF} を使用 "
+    print(f"[25_03] K-NET参照: --knet-absmax-ref={KNET_ABSMAX_REF} を使用 "
           f"(Mac実測 2026-10-15、キャッシュ本体は不要)")
@@ -362,3 +363,3 @@
 n_samp_h5 = int(H5.attrs.get("n_samples", 3000))
-print(f"[24_03] h5: channel_order={ch_order_h5}  n_samples={n_samp_h5}")
+print(f"[25_03] h5: channel_order={ch_order_h5}  n_samples={n_samp_h5}")
 st_raw = H5["stations"][:]
@@ -375,6 +376,6 @@
         ep_sorted, row_sorted = z["ep"], z["row"]
-    print(f"[24_03] 窓索引をキャッシュから読込: {idx_path.name}" if _idx_ok
-          else f"[24_03] 窓索引 {idx_path.name} は今の h5 のものでない(指紋が無いか違う)ので作り直す")
+    print(f"[25_03] 窓索引をキャッシュから読込: {idx_path.name}" if _idx_ok
+          else f"[25_03] 窓索引 {idx_path.name} は今の h5 のものでない(指紋が無いか違う)ので作り直す")
 if not _idx_ok:
-    print("[24_03] 窓索引を構築中(初回のみ・数分)…")
+    print("[25_03] 窓索引を構築中(初回のみ・数分)…")
     order = np.lexsort((ep_raw, st_arr))
@@ -386,3 +387,3 @@
              ep=ep_sorted, row=row_sorted, fp=np.array(_fp))
-    print(f"[24_03] 窓索引を保存: {idx_path.name} ({len(sta_names)}局)")
+    print(f"[25_03] 窓索引を保存: {idx_path.name} ({len(sta_names)}局)")
 del st_raw, ep_raw, st_arr
@@ -583,3 +584,3 @@
         ev["waveforms"] = ev["waveforms"] * amp_fac
-    print(f"[24_03] 振幅整合: 長野absmax中央値 {med:.3e} → ×{amp_fac:.3e} で "
+    print(f"[25_03] 振幅整合: 島根absmax中央値 {med:.3e} → ×{amp_fac:.3e} で "
           f"K-NET中央値 {KNET_ABSMAX_REF:.2f} に一致(一括係数・相対振幅保存)")
@@ -593,3 +594,3 @@
 import hashlib
-rep = dict(script_version="24_03 v1 (computation identical to 15_01c v3.3 and 21_20c v1)", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
+rep = dict(script_version="25_03 v1 (computation identical to 15_01c v3.3 and 21_20c v1)", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            args={k: str(v) for k, v in vars(args).items()}, stats=stats,
@@ -619,3 +620,3 @@
 print("\n" + "=" * 72)
-print(f"[24_03] 完了: {out}")
+print(f"[25_03] 完了: {out}")
 print(f"  採用 {stats['n_ev']} / 対象 {len(cat)}  (セグメント不足 {stats['no_seg']}, "
@@ -644,3 +645,3 @@
     ax[0].set_xlabel("Hypocentral distance (km)"); ax[0].set_ylabel("S–P (s)")
-    ax[0].set_title(f"Northern Nagano 2014: measured S–P vs distance (n={len(SPn)})",
+    ax[0].set_title(f"Western Shimane 2018: measured S–P vs distance (n={len(SPn)})",
                     fontsize=10.5)
@@ -655,3 +656,3 @@
     print(f"図: {PDFD}/15_01c_tottori_picks_qc{args.tag}.pdf")
-print(f"\n[24_03] 出力全文+JSONを貼ってください。{out.name} をMacの SWIFT/data/"
-      f"{'nagano2014_processed' if 'nagano2014' in args.tag else 'tottori_processed'}/ にコピーしてください。")
+print(f"\n[25_03] 出力全文+JSONを貼ってください。{out.name} をMacの SWIFT/data/"
+      f"{'shimane2018_processed' if 'shimane2018' in args.tag else 'tottori_processed'}/ にコピーしてください。")
```

## 25_03h_shimane2018_overlap_exclusion.py ← 24_03h_nagano2014_overlap_exclusion.py

```diff
--- ../nagano/frz/24_03h_nagano2014_overlap_exclusion.py	2026-11-15 05:21:00.093243709 +0000
+++ frz/25_03h_shimane2018_overlap_exclusion.py	2026-11-17 01:57:17.160172313 +0000
@@ -2,23 +2,20 @@
 # =============================================================================
-# Script : 24_03h_nagano2014_overlap_exclusion.py  (v1)
-#          [長野県北部 2014 のキャッシュ(24_03 の本番)から、「発生の 15 s 前〜5 s 後に別の地震がある地震」を除いたキャッシュを作る(規則 R1)。
+# Script : 25_03h_shimane2018_overlap_exclusion.py  (v1)
+#          [島根県西部 2018 のキャッシュ(25_03 の本番)から、「発生の 15 s 前〜5 s 後に別の地震がある地震」を除いたキャッシュを作る(規則 R1)。
 #           使うのは気象庁の震源一覧の発生時刻と Mj だけ。震源の位置(正解)・波形・検測の残り・位置の計算は一切使わない]
-# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)。大阪(21_20)で変更の記録 04 として後から足した規則を、
-#          この系列では長野の波形を開く前に、事前登録の規則として最初から入れる
-# 派生元 : 21_20h_osaka2018_overlap_exclusion.py v1(SHA-256 32a383a04dd7959f9ed7897ed8e9c89b3ab6fba2f5977e119f5375169950b52f)。
-#          規則 R1〜R4・自分の行の見つけ方(24_03 = 21_20c と同じ読み方の時刻(0.1 s で切り捨て)と Mj が一致する、ただ 1 つの行)・
-#          窓 [−15.0 s, +5.0 s]・除かない地震(本震と、24_02 の G-clock の地震)・止める条件は 21_20h v1 と同じ。変えたのは次だけ(DIFF_LOG_24.md):
-#          (1) 入力のキャッシュの SHA-256 の照合を外した(21_20h は止めた後の作り直しで、元のキャッシュが決まっていた。24 では 24_03 の
-#              本番の出力をそのまま受け、SHA-256 を記録に書く)
-#          (2) 21_20g の出力を読む記述(--g-json)を外した(長野には 21_20g が無い)
-#          (3) 本震の想定 MAIN_UTC = 2014-11-22 13:08:17.9 UTC(24_00 の表示の 22:08:17.90 JST、± 60 s、Mj ≥ 6.0)、出力の名前
-#              (tottori_parsed_realpick_nagano2014_m15_r1.pt・data/24_03h_overlap_exclusion.json)、表示 [24_03h]、記録の文
+# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)。大阪(21_20)で変更の記録 04 として後から足し、24 で最初から
+#          規則に入れた R1 を、この系列でも島根の波形を開く前に、事前登録の規則として最初から入れる
+# 派生元 : 24_03h_nagano2014_overlap_exclusion.py v1(SHA-256 e2700654a13f0514f133f01f8255d8b546107716ec43990cc648a7392e42dd0d。事前登録 24 で凍結)。
+#          規則 R1〜R4・自分の行の見つけ方(25_03 = 24_03 = 21_20c と同じ読み方の時刻(0.1 s で切り捨て)と Mj が一致する、ただ 1 つの行)・
+#          窓 [−15.0 s, +5.0 s]・除かない地震(本震と、25_02 の G-clock の地震)・止める条件は 24_03h v1 と同じ。変えたのは次だけ(DIFF_LOG_25.md):
+#          (1) 本震の想定 MAIN_UTC = 2018-04-08 16:32:30.81 UTC(25_00 の表示の 2018-04-09 01:32:30.81 JST、± 60 s、Mj ≥ 6.0)
+#          (2) 出力の名前(tottori_parsed_realpick_shimane2018_m15_r1.pt・data/25_03h_overlap_exclusion.json)、表示 [25_03h]、記録の文
 #
-# 規則(事前登録 24 の 3 節):
-#   R1. 気象庁の震源一覧(jma_nagano2014.csv、24_01 の出力、全ての規模)で、キャッシュの地震の自分の行の発生時刻(0.01 s)から
+# 規則(事前登録 25 の 3 節。24 と同じ):
+#   R1. 気象庁の震源一覧(jma_shimane2018.csv、25_01 の出力、全ての規模)で、キャッシュの地震の自分の行の発生時刻(0.01 s)から
 #       dt = [−15.0 s, +5.0 s] の範囲に、自分の行以外の地震が 1 つでもあれば、その地震を除く。
-#   R2. 除かないもの: 本震(キャッシュで Mj 最大)と、24_02 の G-clock の地震(24_04d の (e) に要る)。このどれかが試験の候補なら止める。
-#   R3. 除いた後の試験の候補が 30 未満なら、キャッシュを書かずに止める(既存の MIN_TEST = 30。24_05 は回さず INCONCLUSIVE と報告する)。
+#   R2. 除かないもの: 本震(キャッシュで Mj 最大)と、25_02 の G-clock の地震(25_04d の (e) に要る)。このどれかが試験の候補なら止める。
+#   R3. 除いた後の試験の候補が 30 未満なら、キャッシュを書かずに止める(既存の MIN_TEST = 30。25_05 は回さず INCONCLUSIVE と報告する)。
 #   R4. キャッシュの地震の並びと中身(辞書)は 1 字も変えず、除く地震を抜くだけ。
-#   24_00 の見積もり(カタログだけ): 試験の候補 81 → R1 の後 79。キャッシュでは P を測れない地震の分だけ少なくなりうる。
+#   25_00 の見積もり(カタログだけ): 試験の候補 41 → R1 の後 41(除く 0)。キャッシュでは P を測れない地震の分だけ少なくなりうる。
 #
@@ -28,10 +25,10 @@
 # 出力(--out の下):
-#   data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt  … 除いた後のキャッシュ(24_04d・24_04e・24_07・24_05・24_06f・24_06g に渡す)
-#   data/24_03h_overlap_exclusion.json                                … 規則・入力と出力の SHA-256・数・除いた地震の一覧
+#   data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt  … 除いた後のキャッシュ(25_04d・25_04e・24_07・25_05・25_06f・25_06g に渡す)
+#   data/25_03h_overlap_exclusion.json                                … 規則・入力と出力の SHA-256・数・除いた地震の一覧
 #
-# Usage(Colab。ノート 24_nagano2014_colab.ipynb の セル N12):
-#   !python /content/drive/MyDrive/ARGUS/src/24_03h_nagano2014_overlap_exclusion.py \
-#       --cache /content/ARGUS_nagano2014/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15.pt \
-#       --catalog /content/drive/MyDrive/ARGUS/data/catalog/jma_nagano2014.csv \
-#       --report /content/drive/MyDrive/ARGUS_nagano2014/data/24_02_report.json --out /content/ARGUS_nagano2014
+# Usage(Colab。ノート 25_shimane2018_colab.ipynb の セル N12):
+#   !python /content/drive/MyDrive/ARGUS/src/25_03h_shimane2018_overlap_exclusion.py \
+#       --cache /content/ARGUS_shimane2018/data/tottori_processed/tottori_parsed_realpick_shimane2018_m15.pt \
+#       --catalog /content/drive/MyDrive/ARGUS/data/catalog/jma_shimane2018.csv \
+#       --report /content/drive/MyDrive/ARGUS_shimane2018/data/25_02_report.json --out /content/ARGUS_shimane2018
 # =============================================================================
@@ -45,15 +42,15 @@
 VERSION = "v1"
-TAG = "[24_03h]"
+TAG = "[25_03h]"
 PRE_S, POST_S = 15.0, 5.0                                # R1(21_20g と同じ窓)
 POOL_H, FRESH_MAX_MAG, MIN_TEST = 72.0, 2.0, 30            # 21_20 v1 と同じ値
-MAIN_UTC = datetime(2014, 11, 22, 13, 8, 17, 900000)      # 24: 24_00 の表示の 22:08:17.90 JST(± 60 s)
+MAIN_UTC = datetime(2018, 4, 8, 16, 32, 30, 810000)      # 25: 25_00 の表示の 2018-04-09 01:32:30.81 JST(± 60 s)
 GCLOCK_MATCH_S = 1.5                                       # 21_20d v1 の (e) と同じ探し方
-OUT_CACHE = "data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt"
-OUT_JSON = "data/24_03h_overlap_exclusion.json"
+OUT_CACHE = "data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt"
+OUT_JSON = "data/25_03h_overlap_exclusion.json"
 
-ap = argparse.ArgumentParser(description="24_03h: 発生の近くに別の地震がある地震を除いたキャッシュを作る(事前登録 24 の R1)")
-ap.add_argument("--cache", required=True, help="24_03 の本番のキャッシュ(tottori_parsed_realpick_nagano2014_m15.pt)")
-ap.add_argument("--catalog", required=True, help="jma_nagano2014.csv(24_01 の出力、全ての規模、時刻は日本時間)")
-ap.add_argument("--report", required=True, help="24_02 の報告(data/24_02_report.json。G-clock の地震を読む)")
-ap.add_argument("--out", required=True, help="出力の根(24_04d・24_04e の --base にもこの場所を使う)")
+ap = argparse.ArgumentParser(description="25_03h: 発生の近くに別の地震がある地震を除いたキャッシュを作る(事前登録 25 の R1)")
+ap.add_argument("--cache", required=True, help="25_03 の本番のキャッシュ(tottori_parsed_realpick_shimane2018_m15.pt)")
+ap.add_argument("--catalog", required=True, help="jma_shimane2018.csv(25_01 の出力、全ての規模、時刻は日本時間)")
+ap.add_argument("--report", required=True, help="25_02 の報告(data/25_02_report.json。G-clock の地震を読む)")
+ap.add_argument("--out", required=True, help="出力の根(25_04d・25_04e の --base にもこの場所を使う)")
 a = ap.parse_args()
@@ -105,3 +102,3 @@
         t = datetime.strptime(ts[:22], "%Y-%m-%d %H:%M:%S.%f" if "." in ts else "%Y-%m-%d %H:%M:%S")
-        t21 = datetime.strptime(ts[:21].ljust(21, "0"), "%Y-%m-%d %H:%M:%S.%f")   # 24_03(= 21_20c)と同じ読み方(0.1 s で切り捨て)
+        t21 = datetime.strptime(ts[:21].ljust(21, "0"), "%Y-%m-%d %H:%M:%S.%f")   # 25_03(= 21_20c)と同じ読み方(0.1 s で切り捨て)
         mg = row.get("mag", "").strip()
@@ -117,3 +114,3 @@
 
-# ---- 2. 本震(21_20 v1・24_05 と同じ: Mj 最大で、Mj ≥ 6.0・MAIN_UTC ± 60 s)
+# ---- 2. 本震(21_20 v1・25_05 と同じ: Mj 最大で、Mj ≥ 6.0・MAIN_UTC ± 60 s)
 im = int(np.argmax(MAG))
@@ -142,4 +139,4 @@
     sys.exit(f"{TAG} STOP: キャッシュの地震のうち、震源一覧に自分の行が見つからないもの {n_noself}・2 行以上あるもの {n_multi}"
-             "(24_03 = 21_20c と同じ読み方の時刻と Mj で照合)")
-print(f"{TAG} G-match PASS: キャッシュの {NE} 地震とも、震源一覧に自分の行がちょうど 1 つある(24_03 = 21_20c と同じ読み方の時刻と Mj で照合)")
+             "(25_03 = 21_20c と同じ読み方の時刻と Mj で照合)")
+print(f"{TAG} G-match PASS: キャッシュの {NE} 地震とも、震源一覧に自分の行がちょうど 1 つある(25_03 = 21_20c と同じ読み方の時刻と Mj で照合)")
 
@@ -152,6 +149,6 @@
     t = datetime.strptime(str(c["origin_jst"]).replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
-    EVJ19 = [x.replace(microsecond=0) for x in OT_JST]     # 21_20d v1・24_04d の jst() と同じ(秒で切り捨て)
+    EVJ19 = [x.replace(microsecond=0) for x in OT_JST]     # 21_20d v1・25_04d の jst() と同じ(秒で切り捨て)
     j = min(range(NE), key=lambda i: abs((EVJ19[i] - t).total_seconds()))
     if abs((EVJ19[j] - t).total_seconds()) > GCLOCK_MATCH_S:
-        print(f"{TAG} 注意: G-clock の地震 {c['origin_jst']} がキャッシュに無い(24_04d の (e) がその扱いを決める。ここでは何もしない)"); continue
+        print(f"{TAG} 注意: G-clock の地震 {c['origin_jst']} がキャッシュに無い(25_04d の (e) がその扱いを決める。ここでは何もしない)"); continue
     KEEP.setdefault(j, "G-clock event")
@@ -160,7 +157,7 @@
         out0 = Path(a.out) / "data"; out0.mkdir(parents=True, exist_ok=True)
-        json.dump(dict(script="24_03h_nagano2014_overlap_exclusion.py", version=VERSION, script_sha256=SELF_SHA, input_cache_sha256=CACHE_SHA,
+        json.dump(dict(script="25_03h_shimane2018_overlap_exclusion.py", version=VERSION, script_sha256=SELF_SHA, input_cache_sha256=CACHE_SHA,
                        verdict="STOP-R2: an exempt event (mainshock or G-clock event) is a test candidate",
                        event=dict(origin_jst=f"{OT_JST[j]:%Y-%m-%d %H:%M:%S.%f}"[:22], mj=float(MAG[j]), why=why)),
-                  open(out0 / "24_03h_overlap_exclusion.json", "w"), indent=1, ensure_ascii=False)
-        sys.exit(f"{TAG} STOP(R2): 除かない地震({why}、{OT_JST[j]:%Y-%m-%d %H:%M:%S} JST Mj {MAG[j]:.1f})が試験の候補。記録: {out0 / '24_03h_overlap_exclusion.json'}")
+                  open(out0 / "25_03h_overlap_exclusion.json", "w"), indent=1, ensure_ascii=False)
+        sys.exit(f"{TAG} STOP(R2): 除かない地震({why}、{OT_JST[j]:%Y-%m-%d %H:%M:%S} JST Mj {MAG[j]:.1f})が試験の候補。記録: {out0 / '25_03h_overlap_exclusion.json'}")
 EXCL = [ie for ie in range(NE) if NB[ie] and ie not in KEEP]
@@ -179,5 +176,5 @@
 out = Path(a.out); (out / "data" / "tottori_processed").mkdir(parents=True, exist_ok=True)
-REC = dict(script="24_03h_nagano2014_overlap_exclusion.py", version=VERSION, script_sha256=SELF_SHA,
-           purpose="preregistration 24 rule R1 (from 21_20 amendment 04): remove events with another catalogue event within [-15 s, +5 s] of origin; origin times and Mj only; no location, waveform or residual used",
-           rule=dict(pre_s=PRE_S, post_s=POST_S, self_row="catalogue row with the same 24_03 (= 21_20c) parsed time (0.1 s) and Mj; dt measured from its 0.01 s time", keep="mainshock and the 24_02 G-clock events",
+REC = dict(script="25_03h_shimane2018_overlap_exclusion.py", version=VERSION, script_sha256=SELF_SHA,
+           purpose="preregistration 25 rule R1 (same as preregistration 24; from 21_20 amendment 04): remove events with another catalogue event within [-15 s, +5 s] of origin; origin times and Mj only; no location, waveform or residual used",
+           rule=dict(pre_s=PRE_S, post_s=POST_S, self_row="catalogue row with the same 25_03 (= 21_20c) parsed time (0.1 s) and Mj; dt measured from its 0.01 s time", keep="mainshock and the 25_02 G-clock events",
                      pool_h=POOL_H, fresh_max_mag=FRESH_MAX_MAG, min_test=MIN_TEST),
@@ -193,3 +190,3 @@
 if n_test1 < MIN_TEST:
-    REC.update(output=None, verdict="STOP-R3: fewer than 30 test candidates after exclusion; 24_05 is not run and the result is reported as INCONCLUSIVE")
+    REC.update(output=None, verdict="STOP-R3: fewer than 30 test candidates after exclusion; 25_05 is not run and the result is reported as INCONCLUSIVE")
     json.dump(REC, open(out / OUT_JSON, "w"), indent=1, ensure_ascii=False)
@@ -209,2 +206,2 @@
 print(f"{TAG} 記録: {out / OUT_JSON}")
-print(f"{TAG} 次: 24_04d・24_04e を --base {out} --cache {OUT_CACHE} で回す(この SHA-256 は 24_05 が opened.json に書き、24_07 の記録と照らす)")
+print(f"{TAG} 次: 25_04d・25_04e を --base {out} --cache {OUT_CACHE} で回す(この SHA-256 は 25_05 が opened.json に書き、24_07 の記録と照らす)")
```

## 25_04d_shimane2018_gclock2_picks.py ← 24_04d_nagano2014_gclock2_picks.py

```diff
--- ../nagano/frz/24_04d_nagano2014_gclock2_picks.py	2026-11-15 05:21:00.092796961 +0000
+++ frz/25_04d_shimane2018_gclock2_picks.py	2026-11-17 01:57:17.161448294 +0000
@@ -2,25 +2,49 @@
 # =============================================================================
-# Script : 24_04d_nagano2014_gclock2_picks.py  (v1)
-#          [G-clock2: 24_03h の後のキャッシュの PhaseNet の P の検測(全ての地震・全ての局)を使って、長野県北部 2014 の波形の
-#           時刻がずれていないかを確かめる。規則(a)〜(f)と閾値は 21_04d v1・21_20d v1 と同じ]
-# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の確かめ
-# 派生元 : 21_20d_osaka2018_gclock2_picks.py v1(SHA-256 606d0eea2f76a8607c7844f83a93056759640974bce7f11ccfe690ecb6e7c1d6)。
-#          計算・規則・閾値・止め方(FAIL なら exit code 1)は 1 字も変えていない。変えたのは次だけ(DIFF_LOG_24.md):
-#          既定のキャッシュ(..._nagano2014_m15_r1.pt = 24_03h の出力)と報告(data/24_02_report.json)の場所、表示の [24_04d]、
-#          出力の名前(data/24_04d_gclock2.json・PDF/24_04d_gclock2.pdf)、JSON の script、図の題と軸の年。
-#          FAIL の時の扱いは、事前登録 24 の 5.3 節(21_20 の案 C と同じ: (a)・(b)・(d)・(e)・(f) のどれかの FAIL で止める。
-#          (c) は 24_04e の表で 80 km 以内(止める)と 80 km より遠い(止めずに印を付ける)に分ける)。
+# Script : 25_04d_shimane2018_gclock2_picks.py  (v1)
+#          [G-clock2: 25_03h の後のキャッシュの PhaseNet の P の検測(全ての地震・全ての局)を使って、島根県西部 2018 の波形の
+#           時刻がずれていないかを確かめる。規則 (a)〜(c)・(e)・(f) と閾値は 24_04d v1(= 21_04d v1・21_20d v1)と同じ。
+#           (d) だけを、事前登録 25 の前の dev(25_04x・25_04y・25_04z・25_04v)で決めた「本震 + 72 h より後の続いた 5 地震」に替えた]
+# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の入力の確かめ
+# 派生元 : 24_04d_nagano2014_gclock2_picks.py v1(SHA-256 42f783bba5ca666847b4582edf3d4a554cecce288c1b2aa112f682bdbaa95f93。事前登録 24 で凍結)。
+#          (a)・(b)・(c)・(e)・(f) の計算・閾値と、残りの定義は 24_04d v1 と 1 字も変えていない。変えたのは次だけ(DIFF_LOG_25.md):
+#          (1) (d) を替えた(下の「新しい (d)」)。元の (d)(日本時間の 1 時間ごと)は記述として計算して表示・JSON に残すが、判定には使わない。
+#              JSON の pass_hour は無くし、新しい (d) の合否を pass_block に書く(元の (d) の値は hourly_descriptive)
+#          (2) 止める条件の「検測 20 以上の時間が 0」を外した(1 時間ごとは判定に使わないため)。新しい (d) で判定する窓が 0 の時は、
+#              (d) を FAIL とする(止める条件ではなく、JSON を書いてから exit code 1)
+#          (3) 新しい (d) の作りの試験(selftest。7 例)を足し、毎回最初に回す。--selftest で試験だけを回せる(その時 --base は要らない)
+#          (4) 既定のキャッシュ(..._shimane2018_m15_r1.pt = 25_03h の出力)と報告(data/25_02_report.json)の場所、表示の [25_04d]、
+#              出力の名前(data/25_04d_gclock2.json・PDF/25_04d_gclock2.pdf)、JSON の script、図の題と軸の年、図に (d) の窓の値の枠を足した
+#          FAIL の時の扱いは、事前登録 25 の 5.3 節(24 の 5.3 節と同じ: (a)・(b)・(d)・(e)・(f) のどれかの FAIL で止める。
+#          (c) は 25_04e の表で 80 km 以内(止める)と 80 km より遠い(止めずに印を付ける)に分ける)。
 #
-# 何をするか(21_20d と同じ):
+# なぜ (d) を替えたか(事前登録 25 の 4 節の表 4):
+#   長野県北部 2014(事前登録 24)では、元の (d) が、地震が 1 つしかない 1 時間(2014-12-01 07 時台、0.672 s)で FAIL して止まった。
+#   その 1 地震の検測の質や気象庁の発生時刻の誤差でも外れるので、時計のずれと見分けられない。島根は 25_00 で、本震 + 72 h より後の
+#   65 時間のうち 54 時間が Mj ≥ 1.5 の地震 1 つだけだった(同じことが起きやすい)。そこで、既に結果の出た 4 系列のキャッシュ
+#   (長野 2014・鳥取県西部 2026・大阪 2018・鳥取県中部 2016)だけで作りを試し(島根は開いていない)、次の形に決めた。
+#
+# 新しい (d)(25_04v v1、SHA-256 6330e5dc6da580ff37efc266110caa7fdbf90e1af6c197fcbb61e4d7e80d21dc の形と同じ計算):
+#   0. 見る地震: 本震(キャッシュで Mj 最大)の発生から 72 h より後(ちょうど 72 h は含めない)の地震で、P を測った検測があるもの。
+#      日本時間(キャッシュの UTC を秒で切って 9 時間を足す。下の jst)で比べる。試験の候補を取る期間と同じ。
+#   1. 残り r は (a)〜(c) と同じ(P の時刻 − 震源距離 / 6.0 km/s。PhaseNet の P、p_fallback = 0)。0 の地震の全ての検測の中央値を M とする。
+#   2. 0 の地震を発生時刻の順(同じ時刻はキャッシュの並び順)に並べ、続いた 5 地震ごと(1 つずつずらす)に、地震ごとの検測の
+#      中央値を出し、その 5 つの中央値の中央値 − M を出す。5 地震の検測が合わせて 20 以上の窓だけを判定する。
+#   3. 判定した全ての窓で |値| ≤ 0.5 s なら合格。判定した窓が 1 つも無ければ合格としない。
+#   dev の結果(25_04v、4 系列とも合格): 元のキャッシュの最大 0.068〜0.177 s、1 地震の全ての局に ±1・±3・±10 s を足した時に
+#   FAIL になった割合 0.000〜0.008、続いた 4 地震の全ての局に +1.0 s を足した時に見つけた割合 0.998〜1.000(+0.8 s では 0.998〜1.000)。
+#   限界: 区切り(約 2 時間)に地震が 1〜2 つしかない時の組み立ての誤りは見えない。本震 + 72 h までの地震の時刻は (d) では見ない。
+#
+# 何をするか(24_04d と同じ。(d) だけ上のとおり):
 #   1. キャッシュの全ての地震・全ての局のうち、PhaseNet で P を測った検測(p_fallback = 0)について、残り r = tp_times − dist_km / 6.0 s を出す。
-#   2. (a) |全体の中央値| ≤ 1.5 s (b) 日ごと ≤ 0.5 s (c) 局ごと ≤ 1.0 s (d) 1 時間ごと ≤ 0.5 s
-#      (e) 24_02 の報告の G-clock の地震がそれぞれ ≤ 0.5 s(検測 4 以上) (f) 局ごとの P を測った割合が全局の中央値の 0.5 倍以上。
-#      検測 20 以上の日・局・時間で数える。日と時間は日本時間。
-#   3. 参考(判定には使わない): --ref-cache に鳥取 2026 のキャッシュ。
-#   4. 出力: data/24_04d_gclock2.json / PDF/24_04d_gclock2.pdf。FAIL なら exit code 1。
+#   2. (a) |全体の中央値| ≤ 1.5 s (b) 日ごと ≤ 0.5 s (c) 局ごと ≤ 1.0 s (d) 上の新しい (d) ≤ 0.5 s
+#      (e) 25_02 の報告の G-clock の地震がそれぞれ ≤ 0.5 s(検測 4 以上) (f) 局ごとの P を測った割合が全局の中央値の 0.5 倍以上。
+#      (b)・(c) は検測 20 以上の日・局で数える。日は日本時間。
+#   3. 参考(判定には使わない): --ref-cache に鳥取 2026 のキャッシュ。元の (d)(1 時間ごと)も参考に出す。
+#   4. 出力: data/25_04d_gclock2.json / PDF/25_04d_gclock2.pdf。FAIL なら exit code 1。
 #
-# Usage(Colab、24_03h の後に。ノート 24_nagano2014_colab.ipynb の セル N13):
-#   !python /content/drive/MyDrive/ARGUS/src/24_04d_nagano2014_gclock2_picks.py --base /content/ARGUS_nagano2014 \
+# Usage(Colab、25_03h の後に。ノート 25_shimane2018_colab.ipynb の セル N13):
+#   !python /content/drive/MyDrive/ARGUS/src/25_04d_shimane2018_gclock2_picks.py --base /content/ARGUS_shimane2018 \
 #       --ref-cache /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt
-# 止める条件(STOP): キャッシュが無い・P を測った検測が 100 未満・検測 20 以上の日・局・時間のどれかが 0・24_02 の報告が無い
+#   試験だけ: !python .../25_04d_shimane2018_gclock2_picks.py --selftest
+# 止める条件(STOP): キャッシュが無い・P を測った検測が 100 未満・検測 20 以上の日・局のどれかが 0・25_02 の報告が無い・selftest の失敗
 # =============================================================================
@@ -33,6 +57,7 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--base", required=True, help="ARGUS_nagano2014 の場所(Colab のローカルなら /content/ARGUS_nagano2014)")
-ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt")
+ap.add_argument("--base", default="", help="ARGUS_shimane2018 の場所(Colab のローカルなら /content/ARGUS_shimane2018。--selftest の時は要らない)")
+ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt")
 ap.add_argument("--ref-cache", default="", help="参考: 鳥取 2026 のキャッシュ(無くてよい)")
-ap.add_argument("--report", default="data/24_02_report.json", help="24_02 の報告(G-clock の地震を読む。--base からの場所)")
+ap.add_argument("--report", default="data/25_02_report.json", help="25_02 の報告(G-clock の地震を読む。--base からの場所)")
+ap.add_argument("--selftest", action="store_true", help="25: 新しい (d) の作りの試験だけを回す")
 a = ap.parse_args()
@@ -40,2 +65,4 @@
 TOL_HOUR, TOL_EV, MIN_EV, MIN_FRAC_RATIO = 0.5, 0.5, 4, 0.5
+K_BLOCK, POOL_H = 5, 72.0                                        # 25: 新しい (d)(25_04v と同じ。閾値は TOL_HOUR = 0.5 s のまま)
+if not a.selftest and not a.base: sys.exit("[25_04d] STOP: --base を渡す")
 BASE = Path(a.base)
@@ -64,2 +91,54 @@
 
+def block_events(EVS, r, evi):
+    """25: 新しい (d) の地震。本震(Mj 最大)+ 72 h より後で P を測った地震の (日本時間, 番号, 残り) を時刻の順に。本震の日本時間も返す"""
+    im = int(np.argmax([float(e["mw"]) for e in EVS])); t_main = jst(EVS[im]["origin_time"])
+    out = []
+    for ie, e in enumerate(EVS):
+        t = jst(e["origin_time"])
+        if (t - t_main).total_seconds() <= POOL_H * 3600: continue
+        rr = r[evi == ie]
+        if rr.size: out.append((t, ie, rr))
+    out.sort(key=lambda x: (x[0], x[1]))
+    return out, t_main, im
+
+def block_d(evs):
+    """25: 続いた K_BLOCK 地震ごとの(地震ごとの中央値の中央値 − M)。検測が合わせて MIN_N 未満の窓は判定しない"""
+    if not evs: return dict(n_events=0, n_picks=0, median_s=None, n_windows=0, max_abs_s=None, worst_value_s=None,
+                            worst_window_start_jst=None, worst_window_end_jst=None, windows=[], pass_=False)
+    M = float(np.median(np.concatenate([x[2] for x in evs])))
+    W, mx, at = [], None, None
+    for j in range(0, len(evs) - K_BLOCK + 1):
+        rs = [evs[j + i][2] for i in range(K_BLOCK)]
+        if sum(len(x) for x in rs) < MIN_N: continue
+        v = float(np.median([np.median(x) for x in rs])) - M
+        W.append(dict(start_jst=f"{evs[j][0]:%Y-%m-%d %H:%M:%S}", end_jst=f"{evs[j + K_BLOCK - 1][0]:%Y-%m-%d %H:%M:%S}",
+                      n_picks=int(sum(len(x) for x in rs)), value_s=v))
+        if mx is None or abs(v) > abs(mx): mx, at = v, len(W) - 1
+    return dict(n_events=len(evs), n_picks=int(sum(len(x[2]) for x in evs)), median_s=M, n_windows=len(W),
+                max_abs_s=(None if mx is None else abs(mx)), worst_value_s=mx,
+                worst_window_start_jst=(None if at is None else W[at]["start_jst"]), worst_window_end_jst=(None if at is None else W[at]["end_jst"]),
+                windows=W, pass_=bool(W and abs(mx) <= TOL_HOUR))
+
+def selftest():
+    """25: 新しい (d) の作りの試験(25_04v の試験のうち、この計算に当てはまるもの)"""
+    def check(c, m):
+        if not c: sys.exit(f"[25_04d] STOP: selftest に失敗: {m}")
+    rng = np.random.default_rng(1); t0 = datetime(2018, 4, 12, 3)
+    evs = [(t0 + timedelta(minutes=40 * j), j, 0.3 + rng.normal(0, 0.15, 24)) for j in range(60)]
+    sh = lambda S, ds: [(t, ie, rr + ds if ie in S else rr) for t, ie, rr in evs]
+    check(block_d(evs)["pass_"] and block_d(evs)["n_windows"] == 56, "正常は合格(窓 56)")
+    check(block_d(sh({30}, 10.0))["pass_"], "1 地震の全局 +10 s は合格")
+    check(block_d(sh({30, 32}, 3.0))["pass_"], "5 つのうち 2 地震の外れは合格")
+    check(not block_d(sh({30, 31, 32, 33}, 1.0))["pass_"], "続いた 4 地震の全局 +1.0 s は不合格")
+    check(not block_d([(t, ie, rr[:3]) for t, ie, rr in evs])["pass_"] and block_d([(t, ie, rr[:3]) for t, ie, rr in evs])["n_windows"] == 0,
+          "検測 20 未満の窓しか無ければ判定する窓 0 で合格としない")
+    check(not block_d([])["pass_"], "地震が無ければ合格としない")
+    EVm = [dict(origin_time="2018-04-08 16:32:30.8", mw=6.1)] + [dict(origin_time=f"2018-04-11 16:{m:02d}:30.8", mw=1.6) for m in (32, 33)]
+    rr = np.array([0.1, 0.2, 0.3]); ev_, tm_, im_ = block_events(EVm, rr, np.array([0, 1, 2]))
+    check(im_ == 0 and tm_ == datetime(2018, 4, 9, 1, 32, 30) and [x[1] for x in ev_] == [2], "本震 + 72 h の切り方(ちょうど 72 h は除く)と日本時間")
+    print("[25_04d] selftest: 新しい (d)(正常・1 地震の外れ・2 地震の外れ・続いた 4 地震 +1.0 s・検測 20 未満・地震なし・72 h の切り方)の 7 例に合格")
+
+selftest()
+if a.selftest: sys.exit(0)
+
 def groups(r, g):
@@ -76,13 +155,14 @@
 cp = BASE / a.cache
-if not cp.exists(): sys.exit(f"[24_04d] STOP: キャッシュ {cp} が無い(24_03h の後に回す)")
+if not cp.exists(): sys.exit(f"[25_04d] STOP: キャッシュ {cp} が無い(25_03h の後に回す)")
 EVS, r, day, sta, hour, evi, seen = residuals(cp); nev = len(EVS)
-if len(r) < 100: sys.exit(f"[24_04d] STOP: P を測った検測が {len(r)}(100 未満)")
+if len(r) < 100: sys.exit(f"[25_04d] STOP: P を測った検測が {len(r)}(100 未満)")
 S = summarise(r, day, sta, hour)
-if S["n_days"] == 0 or S["n_stations"] == 0 or S["n_hours"] == 0:
-    sys.exit(f"[24_04d] STOP: 検測 {MIN_N} 以上の日・局・時間のどれかが 0(判定できない)")
+if S["n_days"] == 0 or S["n_stations"] == 0:
+    sys.exit(f"[25_04d] STOP: 検測 {MIN_N} 以上の日・局のどれかが 0(判定できない)")
 pa = abs(S["median_s"]) <= TOL_ALL; pd_ = S["max_day_dev_s"] <= TOL_DAY; ps = S["max_station_dev_s"] <= TOL_STA
-ph = S["max_hour_dev_s"] <= TOL_HOUR
-# (e) 24_02 の G-clock の地震: その地震の P を測った検測(MIN_EV 以上)の中央値 − 全体の中央値
+BEV, T_MAIN, IM = block_events(EVS, r, evi); B = block_d(BEV)       # 25: 新しい (d)
+pb = B["pass_"]
+# (e) 25_02 の G-clock の地震: その地震の P を測った検測(MIN_EV 以上)の中央値 − 全体の中央値
 rp = BASE / a.report
-if not rp.exists(): sys.exit(f"[24_04d] STOP: 24_02 の報告 {rp} が無い")
+if not rp.exists(): sys.exit(f"[25_04d] STOP: 25_02 の報告 {rp} が無い")
 gc = json.load(open(rp))["gates"]["clock"]
@@ -105,7 +185,7 @@
 pf_ = len(fr) > 0 and not low
-PASS = bool(pa and pd_ and ps and ph and pe and pf_)
-print(f"[24_04d] キャッシュ {cp.name}: 地震 {nev}・P を測った検測 {S['n']}(日は日本時間。キャッシュの UTC に 9 時間を足す)")
-print(f"[24_04d] (a) 全体: 残り(P の時刻 − 震源距離/6.0 km/s)の中央値 {S['median_s']:+.3f} s(四分位幅 {S['iqr_s']:.3f} s)  "
+PASS = bool(pa and pd_ and ps and pb and pe and pf_)
+print(f"[25_04d] キャッシュ {cp.name}: 地震 {nev}・P を測った検測 {S['n']}(日は日本時間。キャッシュの UTC に 9 時間を足す)")
+print(f"[25_04d] (a) 全体: 残り(P の時刻 − 震源距離/6.0 km/s)の中央値 {S['median_s']:+.3f} s(四分位幅 {S['iqr_s']:.3f} s)  "
       f"基準 |中央値| ≤ {TOL_ALL} s  {'PASS' if pa else 'FAIL'}")
-print(f"[24_04d] (b) 日ごと(検測 {MIN_N} 以上の日): 全体の中央値からの最大のずれ {S['max_day_dev_s']:.3f} s  基準 ≤ {TOL_DAY} s  "
+print(f"[25_04d] (b) 日ごと(検測 {MIN_N} 以上の日): 全体の中央値からの最大のずれ {S['max_day_dev_s']:.3f} s  基準 ≤ {TOL_DAY} s  "
       f"{'PASS' if pd_ else 'FAIL'}")
@@ -113,3 +193,3 @@
     print(f"      {d}: 検測 {v['n']:5d}  中央値 {v['median']:+.3f} s" + ("" if v["n"] >= MIN_N else "(少ないので判定に使わない)"))
-print(f"[24_04d] (c) 局ごと(検測 {MIN_N} 以上の局): 全体の中央値からの最大のずれ {S['max_station_dev_s']:.3f} s  基準 ≤ {TOL_STA} s  "
+print(f"[25_04d] (c) 局ごと(検測 {MIN_N} 以上の局): 全体の中央値からの最大のずれ {S['max_station_dev_s']:.3f} s  基準 ≤ {TOL_STA} s  "
       f"{'PASS' if ps else 'FAIL'}")
@@ -117,7 +197,12 @@
 for dv, s, v in worst: print(f"      ずれの大きい局 {s}: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
-print(f"[24_04d] (d) 時間ごと(日本時間の 1 時間・検測 {MIN_N} 以上、{S['n_hours']} 時間): 全体の中央値からの最大のずれ {S['max_hour_dev_s']:.3f} s  "
-      f"基準 ≤ {TOL_HOUR} s  {'PASS' if ph else 'FAIL'}")
-worst_h = sorted(((abs(v["median"] - S["median_s"]), k, v) for k, v in S["by_hour"].items() if v["n"] >= MIN_N), reverse=True)[:5]
-for dv, k, v in worst_h: print(f"      ずれの大きい時間 {k} 時台: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
-print(f"[24_04d] (e) 24_02 の G-clock の地震(P を測った検測 {MIN_EV} 以上、|地震の中央値 − 全体の中央値| ≤ {TOL_EV} s): {'PASS' if pe else 'FAIL'}")
+_f = lambda x: "—" if x is None else f"{x:.3f}"
+print(f"[25_04d] (d) 続いた {K_BLOCK} 地震(本震 {T_MAIN:%Y-%m-%d %H:%M:%S} JST・Mj {float(EVS[IM]['mw']):.1f} + {POOL_H:g} h より後の {B['n_events']} 地震・"
+      f"検測 {B['n_picks']}、その中央値 M {('—' if B['median_s'] is None else format(B['median_s'], '+.3f'))} s、検測 {MIN_N} 以上の窓 {B['n_windows']}): "
+      f"最大 |地震ごとの中央値の中央値 − M| {_f(B['max_abs_s'])} s(窓 {B['worst_window_start_jst']} 〜 {B['worst_window_end_jst']})  "
+      f"基準 ≤ {TOL_HOUR} s・判定する窓 1 以上  {'PASS' if pb else 'FAIL'}")
+worst_b = sorted(B["windows"], key=lambda w: -abs(w["value_s"]))[:5]
+for w in worst_b: print(f"      ずれの大きい窓 {w['start_jst']} 〜 {w['end_jst']}: 検測 {w['n_picks']}  値 {w['value_s']:+.3f} s")
+print(f"[25_04d] 参考(元の (d)、判定には使わない): 日本時間の 1 時間ごと(検測 {MIN_N} 以上、{S['n_hours']} 時間): 全体の中央値からの最大のずれ "
+      f"{_f(S['max_hour_dev_s'])} s")
+print(f"[25_04d] (e) 25_02 の G-clock の地震(P を測った検測 {MIN_EV} 以上、|地震の中央値 − 全体の中央値| ≤ {TOL_EV} s): {'PASS' if pe else 'FAIL'}")
 for x in EVC:
@@ -126,3 +211,3 @@
           f"(STA/LTA の G-clock は {x['gclock_stalta_median_abs_s']:.2f} s)  {'PASS' if x['pass_'] else 'FAIL'}")
-print(f"[24_04d] (f) 局ごとの P を測った割合(現れた数 {MIN_N} 以上の {len(fr)} 局): 中央値 {mfr:.3f}、その {MIN_FRAC_RATIO} 倍未満の局 {len(low)}  "
+print(f"[25_04d] (f) 局ごとの P を測った割合(現れた数 {MIN_N} 以上の {len(fr)} 局): 中央値 {mfr:.3f}、その {MIN_FRAC_RATIO} 倍未満の局 {len(low)}  "
       f"{'PASS' if pf_ else 'FAIL'}")
@@ -132,14 +217,20 @@
     _, r2, d2, s2, h2, _, _ = residuals(Path(a.ref_cache)); REF = summarise(r2, d2, s2, h2)
-    print(f"[24_04d] 参考(鳥取 2026、判定には使わない): 検測 {REF['n']}  中央値 {REF['median_s']:+.3f} s  日ごとの最大のずれ "
-          f"{REF['max_day_dev_s']:.3f} s  局ごとの最大のずれ {REF['max_station_dev_s']:.3f} s  時間ごとの最大のずれ {REF['max_hour_dev_s']:.3f} s")
-print(f"[24_04d] G-clock2: {'PASS' if PASS else 'FAIL'}")
+    print(f"[25_04d] 参考(鳥取 2026、判定には使わない): 検測 {REF['n']}  中央値 {REF['median_s']:+.3f} s  日ごとの最大のずれ "
+          f"{REF['max_day_dev_s']:.3f} s  局ごとの最大のずれ {REF['max_station_dev_s']:.3f} s  時間ごとの最大のずれ {_f(REF['max_hour_dev_s'])} s")
+print(f"[25_04d] G-clock2: {'PASS' if PASS else 'FAIL'}")
 (BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
-json.dump(dict(script="24_04d_nagano2014_gclock2_picks.py", version="v1", cache=str(cp), n_events=nev, vp_kms=VP,
-               rule=dict(tol_all_s=TOL_ALL, tol_day_s=TOL_DAY, tol_station_s=TOL_STA, tol_hour_s=TOL_HOUR, tol_event_s=TOL_EV,
-                         min_n=MIN_N, min_event_picks=MIN_EV, min_frac_ratio=MIN_FRAC_RATIO, day_and_hour="JST (cache UTC + 9 h)"),
-               result={k: v for k, v in S.items() if k != "by_hour"}, by_hour=S["by_hour"], gclock_events=EVC,
+json.dump(dict(script="25_04d_shimane2018_gclock2_picks.py", version="v1", cache=str(cp), n_events=nev, vp_kms=VP,
+               rule=dict(tol_all_s=TOL_ALL, tol_day_s=TOL_DAY, tol_station_s=TOL_STA, tol_block_s=TOL_HOUR, tol_event_s=TOL_EV,
+                         min_n=MIN_N, min_event_picks=MIN_EV, min_frac_ratio=MIN_FRAC_RATIO, day_and_hour="JST (cache UTC + 9 h)",
+                         block=dict(k_events=K_BLOCK, after_mainshock_h=POOL_H, value="median of per-event medians minus the median M of all picks of these events",
+                                    min_picks_per_window=MIN_N, pass_rule="all judged windows within tol_block_s and at least one judged window",
+                                    dev_script="25_04v_gclock2_k5_dev.py v1 (SHA-256 6330e5dc6da580ff37efc266110caa7fdbf90e1af6c197fcbb61e4d7e80d21dc)")),
+               result={k: v for k, v in S.items() if k not in ("by_hour", "max_hour_dev_s", "n_hours")},
+               event_block_d={k: v for k, v in B.items() if k != "pass_"}, mainshock_jst=f"{T_MAIN:%Y-%m-%d %H:%M:%S}",
+               hourly_descriptive=dict(max_hour_dev_s=S["max_hour_dev_s"], n_hours=S["n_hours"], by_hour=S["by_hour"], note="original (d) of 24_04d; not used for the verdict"),
+               gclock_events=EVC,
                station_measured_frac=dict(median=mfr, low=[dict(station=k, appeared=c[0], measured=c[1], frac=v) for v, k, c in low]),
-               pass_all=bool(pa), pass_day=bool(pd_), pass_station=bool(ps), pass_hour=bool(ph), pass_events=bool(pe),
+               pass_all=bool(pa), pass_day=bool(pd_), pass_station=bool(ps), pass_block=bool(pb), pass_events=bool(pe),
                pass_measured_frac=bool(pf_), gclock2_pass=PASS, reference_2026=REF),
-          open(BASE / "data" / "24_04d_gclock2.json", "w"), indent=1)
+          open(BASE / "data" / "25_04d_gclock2.json", "w"), indent=1)
 
@@ -149,3 +240,3 @@
 plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
-fig, axs = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw=dict(width_ratios=[1.6, 1.0]))
+fig, axs = plt.subplots(1, 3, figsize=(17, 4.4), gridspec_kw=dict(width_ratios=[1.6, 1.0, 1.6]))
 ax = axs[0]; dk = [d for d, v in S["by_day"].items() if v["n"] >= MIN_N]
@@ -156,4 +247,4 @@
 ax.set_xticks(range(len(dk))); ax.set_xticklabels([d[5:] for d in dk], rotation=60, fontsize=7); ax.set_xlim(-0.5, len(dk) - 0.5)
-ax.set_xlabel("JST date (2014)"); ax.set_ylabel("PhaseNet P time - distance / 6.0 km/s (s)")
-ax.set_title(f"(a) Northern Nagano 2014, {S['n']} P picks: daily medians", fontsize=9); ax.grid(alpha=0.3)
+ax.set_xlabel("JST date (2018)"); ax.set_ylabel("PhaseNet P time - distance / 6.0 km/s (s)")
+ax.set_title(f"(a) Western Shimane 2018, {S['n']} P picks: daily medians", fontsize=9); ax.grid(alpha=0.3)
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False, fontsize=8)
@@ -165,4 +256,13 @@
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), frameon=False, fontsize=8)
-fig.tight_layout(); fig.savefig(BASE / "PDF" / "24_04d_gclock2.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"[24_04d] 出力: {BASE / 'data' / '24_04d_gclock2.json'}、{BASE / 'PDF' / '24_04d_gclock2.pdf'}")
-if not PASS: sys.exit("[24_04d] STOP(G-clock2): 時刻のずれの疑い。どの条件の FAIL かで、事前登録 24 の 5.3 節の扱いに従う(この出力を貼る)")
+ax = axs[2]                                                      # 25: 新しい (d) の窓の値
+if B["windows"]:
+    tw = [(datetime.strptime(w["start_jst"], "%Y-%m-%d %H:%M:%S") - T_MAIN).total_seconds() / 86400 for w in B["windows"]]
+    ax.plot(tw, [w["value_s"] for w in B["windows"]], "o", ms=3, color="tab:blue", label=f"{K_BLOCK}-event window value")
+ax.axhspan(-TOL_HOUR, TOL_HOUR, color="tab:green", alpha=0.15, label=f"Allowed (+/- {TOL_HOUR} s)")
+ax.axhline(0, color="k", lw=0.8)
+ax.set_xlabel(f"Window start, days since mainshock ({T_MAIN:%Y-%m-%d %H:%M} JST)"); ax.set_ylabel("Median of event medians - M (s)")
+ax.set_title(f"(c) Condition (d): {K_BLOCK} consecutive events after mainshock + {POOL_H:g} h, {B['n_windows']} windows: {'PASS' if pb else 'FAIL'}", fontsize=9)
+ax.grid(alpha=0.3); ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=False, fontsize=8)
+fig.tight_layout(); fig.savefig(BASE / "PDF" / "25_04d_gclock2.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"[25_04d] 出力: {BASE / 'data' / '25_04d_gclock2.json'}、{BASE / 'PDF' / '25_04d_gclock2.pdf'}")
+if not PASS: sys.exit("[25_04d] STOP(G-clock2): 時刻のずれの疑い。どの条件の FAIL かで、事前登録 25 の 5.3 節の扱いに従う(この出力を貼る)")
```

## 25_04e_shimane2018_station_pick_diagnose.py ← 24_04e_nagano2014_station_pick_diagnose.py

```diff
--- ../nagano/frz/24_04e_nagano2014_station_pick_diagnose.py	2026-11-15 05:21:00.094259170 +0000
+++ frz/25_04e_shimane2018_station_pick_diagnose.py	2026-11-17 01:57:17.162520372 +0000
@@ -2,9 +2,9 @@
 # =============================================================================
-# Script : 24_04e_nagano2014_station_pick_diagnose.py  (v1)
-#          [局ごとの検測の調べ(読むだけの記述)。事前登録 24 の 5.3 節では、24_04d の結果によらず必ず回し、この CSV の
+# Script : 25_04e_shimane2018_station_pick_diagnose.py  (v1)
+#          [局ごとの検測の調べ(読むだけの記述)。事前登録 25 の 5.3 節では、25_04d の結果によらず必ず回し、この CSV の
 #           epi_from_mainshock_km・n・dev_s で G-clock2 の (c) を 80 km 以内(止める)と 80 km より遠い(止めずに印)に分ける]
-# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の確かめ
-# 派生元 : 21_20e_osaka2018_station_pick_diagnose.py v1(SHA-256 680e8825d49e00bba58cca9045c66ee7b213f05bc5a231d0810d041b4fefba92)。
-#          計算は 1 字も変えていない。変えたのは、既定のキャッシュの場所・表示の [24_04e] と系列の名前・出力の名前
-#          (data/24_04e_station_picks.csv・PDF/24_04e_station_picks.pdf)・図の題だけ(DIFF_LOG_24.md)。
+# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の入力の確かめ
+# 派生元 : 24_04e_nagano2014_station_pick_diagnose.py v1(SHA-256 befca1b3326d18659d249c7ee9e5b1b1f364828c8a4a85c3cafc1bba16f67931。事前登録 24 で凍結。
+#          = 21_20e v1 と同じ計算)。計算は 1 字も変えていない。変えたのは、既定のキャッシュの場所・表示の [25_04e] と系列の名前・
+#          出力の名前(data/25_04e_station_picks.csv・PDF/25_04e_station_picks.pdf)・図の題だけ(DIFF_LOG_25.md)。
 #
@@ -14,4 +14,4 @@
 #
-# Usage(Colab。ノート 24_nagano2014_colab.ipynb の セル N14):
-#   !python /content/drive/MyDrive/ARGUS/src/24_04e_nagano2014_station_pick_diagnose.py --base /content/ARGUS_nagano2014 \
+# Usage(Colab。ノート 25_shimane2018_colab.ipynb の セル N14):
+#   !python /content/drive/MyDrive/ARGUS/src/25_04e_shimane2018_station_pick_diagnose.py --base /content/ARGUS_shimane2018 \
 #       --ref-cache /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt
@@ -25,3 +25,3 @@
 ap.add_argument("--base", required=True)
-ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt")
+ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt")
 ap.add_argument("--ref-cache", default="")
@@ -63,3 +63,3 @@
 def show(name, med, out):
-    print(f"\n[24_04e] ===== {name}: 全体の中央値 {med:+.3f} s(局 {len(out)}、本震からの距離の順)=====")
+    print(f"\n[25_04e] ===== {name}: 全体の中央値 {med:+.3f} s(局 {len(out)}、本震からの距離の順)=====")
     print("  局(緯度,経度)        本震から km  検測   中央値   ずれ   Mj<2 の中央値(数)   2≤Mj<3(数)        Mj≥3(数)         |r−全体|>3 s")
@@ -72,6 +72,6 @@
 cp = BASE / a.cache
-if not cp.exists(): sys.exit(f"[24_04e] STOP: {cp} が無い")
-med, out = table(cp); show("長野県北部 2014", med, out)
+if not cp.exists(): sys.exit(f"[25_04e] STOP: {cp} が無い")
+med, out = table(cp); show("島根県西部 2018", med, out)
 (BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
-with open(BASE / "data" / "24_04e_station_picks.csv", "w", newline="") as fo:
+with open(BASE / "data" / "25_04e_station_picks.csv", "w", newline="") as fo:
     w = csv.DictWriter(fo, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
@@ -82,3 +82,3 @@
     else:
-        print(f"[24_04e] 注意: 参考のキャッシュ {a.ref_cache} が無いので飛ばした")
+        print(f"[25_04e] 注意: 参考のキャッシュ {a.ref_cache} が無いので飛ばした")
 
@@ -88,3 +88,3 @@
 plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
-panels = [("Northern Nagano 2014", med, out)] + ([("West Tottori 2026 (reference)", *ref)] if ref else [])
+panels = [("Western Shimane 2018", med, out)] + ([("West Tottori 2026 (reference)", *ref)] if ref else [])
 fig, axs = plt.subplots(1, len(panels), figsize=(6.2 * len(panels), 4.4), squeeze=False)
@@ -102,3 +102,3 @@
 axs[0][0].legend(loc="upper center", bbox_to_anchor=(0.5 * len(panels) + 0.05 * (len(panels) - 1), -0.15), ncol=5, frameon=False, fontsize=8)
-fig.tight_layout(); fig.savefig(BASE / "PDF" / "24_04e_station_picks.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"\n[24_04e] 出力: {BASE / 'data' / '24_04e_station_picks.csv'}、{BASE / 'PDF' / '24_04e_station_picks.pdf'}")
+fig.tight_layout(); fig.savefig(BASE / "PDF" / "25_04e_station_picks.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"\n[25_04e] 出力: {BASE / 'data' / '25_04e_station_picks.csv'}、{BASE / 'PDF' / '25_04e_station_picks.pdf'}")
```

## 25_05_shimane2018_similarity_confirmation.py ← 24_05_nagano2014_similarity_confirmation.py

```diff
--- ../nagano/frz/24_05_nagano2014_similarity_confirmation.py	2026-11-15 05:21:00.096344895 +0000
+++ frz/25_05_shimane2018_similarity_confirmation.py	2026-11-17 01:57:17.162341581 +0000
@@ -2,32 +2,35 @@
 # =============================================================================
-# Script : 24_05_nagano2014_similarity_confirmation.py  (v1)
-#          [「波形が似た過去の地震 × 物理」(C3)と「似た地震の通り道の補正」(C4)を、手を付けていない 4 つ目の余震系列
-#           (長野県北部 2014、本震 2014-11-22 22:08 JST・Mj 6.7)で、21_02・21_04・21_20 と同じ規則のまま 1 回だけ確かめる。
-#           あわせて H4(C3 対 C1)と H5(τ までの波形だけの検測)を、事前登録 24 で足した副の仮説として確かめる]
-# Project: ARGUS(新生)— 論文の柱(4 つ目の系列での一発試験。変更の記録なしで回すことを目指す)
-# 派生元 : 21_20_osaka2018_similarity_confirmation.py v1(SHA-256 2c0fb375e6a1a8d48d3ffbc611bb189b2390d224488cdd5585c76f5cadd5da43)。
+# Script : 25_05_shimane2018_similarity_confirmation.py  (v1)
+#          [「波形が似た過去の地震 × 物理」(C3)と「似た地震の通り道の補正」(C4)を、手を付けていない 5 つ目の余震系列
+#           (島根県西部 2018、本震 2018-04-09 01:32 JST・Mj 6.1)で、21_02・21_04・21_20・24 と同じ規則のまま 1 回だけ確かめる。
+#           あわせて H4(C3 対 C1)と H5(τ までの波形だけの検測)を、事前登録 24 で足し 25 でも変えない副の仮説として確かめる]
+# Project: ARGUS(新生)— 論文の柱(5 つ目の系列での一発試験。変更の記録なしで回すことを目指す。4 つ目の長野県北部 2014 は
+#          G-clock2 で止まり、試験を開いていない)
+# 派生元 : 24_05_nagano2014_similarity_confirmation.py v1(SHA-256 c10d15fe404309d836fc83fb2dbe1d207fa477d9597900724f487ef965970f9f。
+#          事前登録 24 で凍結。長野では回していない)。
 #
-# 21_20 v1 から変えたこと(DIFF_LOG_24.md に全ての差分):
-#   1. 系列に依るもの: 入力の既定(data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt = 24_03 のキャッシュに
-#      24_03h の R1 を当てたもの)、MAIN_UTC = 2014-11-22 13:08:17.9 UTC(24_00 の表示の 22:08:17.90 JST。確かめは 21_20 と同じ
-#      「Mj 最大の地震が Mj ≥ 6.0、MAIN_UTC から 60 s 以内」)、G-untouched の期間 2014-11-20〜2014-12-17 UTC(24_01 の期間を日の単位で
-#      含む)、出力の名前(models/24_05_*・data/24_05_per_event*.csv・PDF/24_05_F*)、表示・図の題・JSON の sequence と verdict_rule の
-#      系列の名前、限界の文(LIMITS)。
-#   2. H1〜H3・BEST・勝ちの規則・方法の計算・pool・ゲート(G-split・G-lib・G-causal・G-phys)・1 回だけの記録・dev・CSV の
-#      21_20 の列は 21_20 v1 と同じ(関数 paired・judge に、比べる誤差の表を渡せる引数を足しただけ。既定では 21_20 と同じ計算)。
-#   3. 足したもの(事前登録 24 の 2 節):
-#      H4(副、α 0.005): τ = 2 s で、C3 が C1(一番似た過去の地震の気象庁の震央。先行研究の「一番似た過去の地震を引く」方式)に
-#        勝つか。勝ち = C1 と C3 の両方に値がある地震で、C3 の中央値 < C1 の中央値・片側の対応 Wilcoxon の p < 0.005・差が 0 でない
-#        組が 10 以上。床の規則は使わない(BEST との比較ではないため。21_20f の HL2 と同じ扱い)。
-#      H5(副、α 0.01): 24_07 v3 が T(= 一番早いオフラインの P + τ)までの波形だけで決めた P・S に置き換えて、全ての方法を計算し直し、
-#        τ = 2 s で C3 が BEST(置き換えた検測での BEST)に H1 と同じ規則で勝つか。似ている度合いの窓は、置き換えた P から切る。
-#        24_07 の出力は、本番を開く前に、スクリプトの SHA-256(CAUSAL_SCRIPT_SHA)・キャッシュの SHA-256・CSV の SHA-256(24_07 の JSON
-#        の csv_sha256)・全ての評価の地震 × 4 時点がそろっていることを確かめる(そろっていなければ開かずに STOP)。
-#        24_07 が回せなかった・照合に落ちた時だけ、--no-causal で H5 を評価せずに H1〜H4 を回す(事前登録 24 の 5.5 節)。
-#        H1〜H4 の結果は H5 の計算の前に models/24_05_judgment*_preH5.json に書く。H5 の計算の例外・STOP・H5 の経路の G-causal の FAIL は
-#        止めずに H5 を NOT-EVALUATED とし、H1〜H4 はそのまま報告する。H5 の経路でも G-causal(未来を置き換えても同じ)を回す。
-#      記述: 置き換えた検測での全ての方法の誤差(CSV の *_causal_err_t* の列、JSON の causal)、図 F4(オフラインと τ までの検測の
-#        BEST・C3 の中央値)。H6(予測震度)は 24_08 が、この CSV から記述として計算する。
+# 24_05 v1 から変えたこと(DIFF_LOG_25.md に全ての差分。計算は 1 字も変えていない):
+#   1. 系列に依るもの: 入力の既定(data/shimane2018_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt = 25_03 のキャッシュに
+#      25_03h の R1 を当てたもの。24_07 の出力の既定の名前)、MAIN_UTC = 2018-04-08 16:32:30.81 UTC(25_00 の表示の 2018-04-09
+#      01:32:30.81 JST。確かめは 24_05 と同じ「Mj 最大の地震が Mj ≥ 6.0、MAIN_UTC から 60 s 以内」)、G-untouched の期間
+#      2018-04-06〜2018-05-03 UTC(25_01 の期間を日の単位で含む)、出力の名前(models/25_05_*・data/25_05_per_event*.csv・PDF/25_05_F*)、
+#      表示・図の題・JSON の sequence と verdict_rule の系列の名前、限界の文(LIMITS。島根の事情を足した)、事前登録の番号(24 → 25)。
+#   2. H1〜H5・BEST・勝ちの規則・方法の計算・pool・ゲート(G-split・G-lib・G-causal・G-phys)・1 回だけの記録・dev・CSV の列・
+#      H5 の材料の照合(24_07 v3 の SHA-256 CAUSAL_SCRIPT_SHA は同じ値。24_07 v3 を 1 字も変えずに使う)は 24_05 v1 と同じ。
 #
-# 事前に固定した仮説と判定(この版の SHA-256 を、データを開く前に事前登録の記録 24 に書く):
+# 24_05 v1 の説明(21_20 v1 から足したもの。25 でもそのまま):
+#   H4(副、α 0.005): τ = 2 s で、C3 が C1(一番似た過去の地震の気象庁の震央。先行研究の「一番似た過去の地震を引く」方式)に
+#     勝つか。勝ち = C1 と C3 の両方に値がある地震で、C3 の中央値 < C1 の中央値・片側の対応 Wilcoxon の p < 0.005・差が 0 でない
+#     組が 10 以上。床の規則は使わない(BEST との比較ではないため。21_20f の HL2 と同じ扱い)。
+#   H5(副、α 0.01): 24_07 v3 が T(= 一番早いオフラインの P + τ)までの波形だけで決めた P・S に置き換えて、全ての方法を計算し直し、
+#     τ = 2 s で C3 が BEST(置き換えた検測での BEST)に H1 と同じ規則で勝つか。似ている度合いの窓は、置き換えた P から切る。
+#     24_07 の出力は、本番を開く前に、スクリプトの SHA-256(CAUSAL_SCRIPT_SHA)・キャッシュの SHA-256・CSV の SHA-256(24_07 の JSON
+#     の csv_sha256)・全ての評価の地震 × 4 時点がそろっていることを確かめる(そろっていなければ開かずに STOP)。
+#     24_07 が回せなかった・照合に落ちた時だけ、--no-causal で H5 を評価せずに H1〜H4 を回す(事前登録 25 の 5.5 節)。
+#     H1〜H4 の結果は H5 の計算の前に models/25_05_judgment*_preH5.json に書く。H5 の計算の例外・STOP・H5 の経路の G-causal の FAIL は
+#     止めずに H5 を NOT-EVALUATED とし、H1〜H4 はそのまま報告する。H5 の経路でも G-causal(未来を置き換えても同じ)を回す。
+#   記述: 置き換えた検測での全ての方法の誤差(CSV の *_causal_err_t* の列、JSON の causal)、図 F4(オフラインと τ までの検測の
+#     BEST・C3 の中央値)。H6(予測震度)は 25_08 が、気象庁の震源決定の印(手動・自動)ごとの誤差は 25_09 が、この CSV から記述として計算する。
+#
+# 事前に固定した仮説と判定(この版の SHA-256 を、データを開く前に事前登録の記録 25 に書く):
 #   BEST(τ) = AI を使わない 9 つの方法(M0r・Mp10・M1・M2・M3r・M5・M5f・M6p・M6r)のうち、評価する全ての地震で値がある
@@ -42,13 +45,13 @@
 #
-# 限界(結果を読むときに必ず添える。表示と JSON にも英語で書く): LIMITS を見る。G-clock2(24_04d)の (c) が FAIL だった時は、事前登録 24 の
+# 限界(結果を読むときに必ず添える。表示と JSON にも英語で書く): LIMITS を見る。G-clock2(25_04d)の (c) が FAIL だった時は、事前登録 25 の
 #   決まった印を結果に付ける(このスクリプトは G-clock2 の結果を読まない)。
 #
-# Usage : (先に Colab のノート 24_nagano2014_colab.ipynb のセル N1〜N16 で、R1 の後のキャッシュと 24_07 の出力を作り、G-clock2 を
-#          確かめ、Mac の ~/SWIFT/data/nagano2014_processed/ にコピーする。手順は 24_STEPS_JA.md)
-#         cd ~/SWIFT && caffeinate -i uv run python src/24_05_nagano2014_similarity_confirmation.py --dev   (動作確認。試験を開かない)
-#         cd ~/SWIFT && caffeinate -i uv run python src/24_05_nagano2014_similarity_confirmation.py         (本番。1 回だけ)
-# Output: models/24_05_judgment.json / models/24_05_opened.json / data/24_05_per_event.csv /
-#         PDF/24_05_F1_error_vs_tau.pdf / PDF/24_05_F2_paired_difference.pdf / PDF/24_05_F3_similarity_vs_separation.pdf /
-#         PDF/24_05_F4_causal_picks.pdf(--dev では _dev、2 回目以降は _rerun_<UTC の時刻>)
-#         models/24_05_judgment_preH5.json(H5 の計算の前に書く H1〜H4)
+# Usage : (先に Colab のノート 25_shimane2018_colab.ipynb のセル N1〜N16 で、R1 の後のキャッシュと 24_07 の出力を作り、G-clock2 を
+#          確かめ、Mac の ~/SWIFT/data/shimane2018_processed/ にコピーする。手順は 25_STEPS_JA.md)
+#         cd ~/SWIFT && caffeinate -i uv run python src/25_05_shimane2018_similarity_confirmation.py --dev   (動作確認。試験を開かない)
+#         cd ~/SWIFT && caffeinate -i uv run python src/25_05_shimane2018_similarity_confirmation.py         (本番。1 回だけ)
+# Output: models/25_05_judgment.json / models/25_05_opened.json / data/25_05_per_event.csv /
+#         PDF/25_05_F1_error_vs_tau.pdf / PDF/25_05_F2_paired_difference.pdf / PDF/25_05_F3_similarity_vs_separation.pdf /
+#         PDF/25_05_F4_causal_picks.pdf(--dev では _dev、2 回目以降は _rerun_<UTC の時刻>)
+#         models/25_05_judgment_preH5.json(H5 の計算の前に書く H1〜H4)
 # 所要  : CPU のみ。21_20 の約 2 倍(H5 のために全ての方法をもう 1 回計算する)。参考: 21_20 の本番は試験 55 地震で 175 s
@@ -64,7 +67,7 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--cache", default="data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt", help="24_03(15_01c v3.3 と同じ計算)の長野県北部 2014 の M>=1.5 版に、24_03h の R1 を当てたもの")
-ap.add_argument("--causal-picks", default="data/nagano2014_processed/24_07_causal_picks_nagano2014.csv", help="24_07 v3 の --all-events の出力(H5)")
-ap.add_argument("--causal-json", default="data/nagano2014_processed/24_07_causal_picks_nagano2014.json", help="24_07 v3 の記録(SHA-256 の照合)")
+ap.add_argument("--cache", default="data/shimane2018_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt", help="25_03(15_01c v3.3 と同じ計算)の島根県西部 2018 の M>=1.5 版に、25_03h の R1 を当てたもの")
+ap.add_argument("--causal-picks", default="data/shimane2018_processed/24_07_causal_picks_shimane2018.csv", help="24_07 v3 の --all-events の出力(H5)")
+ap.add_argument("--causal-json", default="data/shimane2018_processed/24_07_causal_picks_shimane2018.json", help="24_07 v3 の記録(SHA-256 の照合)")
 ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(pool の最後の新しい地震 20 個を代わりに使う)")
-ap.add_argument("--no-causal", action="store_true", help="事前登録 24 の 5.5 節の場合だけ: 24_07 が STOP した・照合に落ちた時に、H5 を評価せずに H1〜H4 を回す")
+ap.add_argument("--no-causal", action="store_true", help="事前登録 25 の 5.5 節の場合だけ: 24_07 が STOP した・照合に落ちた時に、H5 を評価せずに H1〜H4 を回す")
 a = ap.parse_args()
@@ -92,21 +95,29 @@
 NBOOT, SEED, N_DEV, N_GATE = 2000, 12, 20, 5
-MAIN_UTC = dt.datetime(2014, 11, 22, 13, 8, 17, 900000)   # 24: 24_00 の表示の本震 2014-11-22 22:08:17.90 JST(± 60 s、Mj ≥ 6.0 は 21_20 と同じ確かめ)
-UNTOUCHED_UTC = (dt.datetime(2014, 11, 20), dt.datetime(2014, 12, 17))    # G-untouched: 24_01 の期間(本震の 2 日前〜24 日後)を日の単位で含む
-LIMITS = ["fourth sequence: Northern Nagano 2014 (mainshock 2014-11-22, 22:08:17.90 JST, Mj 6.7; JMA catalogue values, see 24_01's JSON), "
+MAIN_UTC = dt.datetime(2018, 4, 8, 16, 32, 30, 810000)   # 25: 25_00 の表示の本震 2018-04-09 01:32:30.81 JST(± 60 s、Mj ≥ 6.0 は 21_20・24_05 と同じ確かめ)
+UNTOUCHED_UTC = (dt.datetime(2018, 4, 6), dt.datetime(2018, 5, 3))    # G-untouched: 25_01 の期間(本震の 2 日前〜24 日後)を日の単位で含む
+LIMITS = ["fifth sequence: Western Shimane 2018 (mainshock 2018-04-09, 01:32:30.81 JST, Mj 6.1; JMA catalogue values, see 25_01's JSON), "
           "never used in ARGUS development; the hypotheses H1-H3 were fixed on West Tottori 2026 (21_01/21_02), tested on Central Tottori 2016 "
-          "(21_04, with a documented deviation) and Northern Osaka 2018 (21_20, re-registered with amendment 04) and are applied here unchanged",
-          "one fourth sequence only; before this preregistration the catalogue h2014 was opened once by 24_00 to count events "
-          "(counts and the mainshock row only; no location list, waveform or method error was looked at)",
+          "(21_04, with a documented deviation) and Northern Osaka 2018 (21_20, re-registered with amendment 04) and are applied here unchanged; "
+          "the fourth sequence (Northern Nagano 2014, preregistration 24 with the same rules) was stopped by the clock check G-clock2 before "
+          "its test was opened, and its rules (including H4 and H5) are carried over unchanged except G-clock2 condition (d)",
+          "one fifth sequence only; before this preregistration the catalogue h2018 was opened by 25_00 to count events "
+          "(counts and the mainshock row only; no location list, waveform or method error was looked at); h2018 had been opened before "
+          "for Northern Osaka 2018 (21_20a), whose box and period do not include this sequence",
+          "the catalogue-only count of test candidates after rule R1 was 41 in 25_00 (25_00 required at least 40 to select a sequence); "
+          "events without a PhaseNet P in the cache are not evaluated, and fewer than 30 evaluated events give INCONCLUSIVE",
+          "25 of these 41 catalogue test candidates have JMA's automatic-hypocentre flag (A), 15 are K and 1 is k (25_00); the truth and "
+          "past-event locations therefore mix manual and automatic JMA hypocentres; errors by flag are described by 25_09 (no test)",
           "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
-          "set of 50 stations also included non-Hi-net stations, so station types and geometry differ",
+          "set of 50 stations also included non-Hi-net stations, so station types and geometry differ; stations that existed in 2018 but "
+          "are not in the current NIED list cannot be candidates",
           "waveforms were downloaded around catalogue events only and converted to the West Tottori 2026 h5 form (30-s windows, "
-          "per-window per-component z-score, JST epoch; 24_02 also stores the window mean and standard deviation); no filter was applied "
-          "before the z-score (compared in 24_02 G-spec)",
-          "the cache was built by 24_03, whose picking, QC and assembly are identical to 15_01c v3.3; 24_03h then removed every event "
+          "per-window per-component z-score, JST epoch; 25_02 also stores the window mean and standard deviation); no filter was applied "
+          "before the z-score (compared in 25_02 G-spec)",
+          "the cache was built by 25_03, whose picking, QC and assembly are identical to 15_01c v3.3; 25_03h then removed every event "
           "with another catalogue event from 15 s before to 5 s after its origin (rule R1 of 21_20 amendment 04, fixed here before any "
-          "Nagano waveform was opened; it uses origin times and Mj only), which can bias the sample against busy periods",
-          "catalogue: JMA hypocentres from h2014 (whether h2014 is the final stage is to be confirmed); past-event locations are JMA "
+          "Shimane waveform was opened; it uses origin times and Mj only), which can bias the sample against busy periods",
+          "catalogue: JMA hypocentres from h2018 (whether h2018 is the final stage is to be confirmed); past-event locations are JMA "
           "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
-          "the 2014 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
-          "events. Manual and automatic hypocentres can be mixed (per-flag counts in 24_01's JSON)",
+          "the 2018 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
+          "events. Manual and automatic hypocentres can be mixed (per-flag counts in 25_01's JSON)",
           "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); "
@@ -142,3 +153,11 @@
           "if 24_07 could not be run, its output failed the checks, the H5 computation raised an exception or the G-causal check on the "
-          "causal-pick path failed, H5 is reported as NOT-EVALUATED and H1-H4 are reported unchanged (preregistration 24, section 5.5)",
+          "causal-pick path failed, H5 is reported as NOT-EVALUATED and H1-H4 are reported unchanged (preregistration 25, section 5.5)",
+
+          "the clock check G-clock2 condition (d) was redesigned for this preregistration on four earlier sequences only (25_04x, 25_04y, "
+          "25_04z and 25_04v; Shimane was not opened): 5 consecutive events after mainshock + 72 h, median of event medians within 0.5 s; "
+          "it does not check common timing errors that affect only one or two events, or events within 72 h of the mainshock; its "
+          "positive control was set to +1.0 s on 4 consecutive events after +0.6 s could not be met together with the negative control "
+          "(25_04z); a 0.6 s common offset over 4 events is therefore not reliably detected",
+          "if the station-level clock check G-clock2 (c) fails only at stations farther than 80 km, the test proceeds with a fixed label "
+          "(preregistration 25, section 5.3); a constant clock offset at a far station can be missed",
           "H1 (C3 at tau = 2 s) is the primary test; H2, H3 and H4 are secondary at alpha 0.005; H5 (causal picks) uses the H1 rule at "
@@ -156,3 +175,3 @@
 SELF_SHA = sha256(Path(__file__))
-print(f"[24_05] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
+print(f"[25_05] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
       f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")
@@ -161,3 +180,3 @@
 CP = ROOT / a.cache
-if not CP.exists(): raise SystemExit(f"[24_05] STOP: {a.cache} が無い(ノート 24_nagano2014_colab.ipynb のセル N12 で作った tottori_parsed_realpick_nagano2014_m15_r1.pt を data/nagano2014_processed/ に置く)")
+if not CP.exists(): raise SystemExit(f"[25_05] STOP: {a.cache} が無い(ノート 25_shimane2018_colab.ipynb のセル N12 で作った tottori_parsed_realpick_shimane2018_m15_r1.pt を data/shimane2018_processed/ に置く)")
 EVS = torch.load(CP, map_location="cpu", weights_only=False)
@@ -166,7 +185,7 @@
     miss = [k for k in need if k not in e]
-    if miss: raise SystemExit(f"[24_05] STOP: キャッシュの地震に {miss} が無い(24_03・24_03h の出力か確かめる)")
+    if miss: raise SystemExit(f"[25_05] STOP: キャッシュの地震に {miss} が無い(25_03・25_03h の出力か確かめる)")
 for e in EVS:
     w_ = np.asarray(e["waveforms"])
-    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[24_05] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
-    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[24_05] STOP: {e['origin_time']} の波形に NaN か無限大")
+    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[25_05] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
+    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[25_05] STOP: {e['origin_time']} の波形に NaN か無限大")
 def to_ns(o):
@@ -178,3 +197,3 @@
     except Exception:
-        raise SystemExit(f"[24_05] STOP: origin_time {o!r} を時刻として読めない")
+        raise SystemExit(f"[25_05] STOP: origin_time {o!r} を時刻として読めない")
 OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
@@ -186,4 +205,4 @@
 if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
-    raise SystemExit("[24_05] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
-if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[24_05] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
+    raise SystemExit("[25_05] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
+if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[25_05] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
 # G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
@@ -194,10 +213,10 @@
 n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
-print(f"[24_05] 入力: 長野県北部 2014 の M ≥ 1.5 版(R1 の後) {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
+print(f"[25_05] 入力: 島根県西部 2018 の M ≥ 1.5 版(R1 の後) {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
       f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
-print(f"[24_05] G-untouched: 期間 2014-11-20〜2014-12-17(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
+print(f"[25_05] G-untouched: 期間 2018-04-06〜2018-05-03(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
       + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
-if n_out != 0 or n_big != 1: raise SystemExit("[24_05] STOP(G-untouched): 長野県北部 2014 のキャッシュに見えない(この行を貼って相談)")
+if n_out != 0 or n_big != 1: raise SystemExit("[25_05] STOP(G-untouched): 島根県西部 2018 のキャッシュに見えない(この行を貼って相談)")
 im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
 if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
-    raise SystemExit(f"[24_05] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2014-11-22 13:08:17.9 UTC ± 60 s。24_00 の表示の 22:08:17.90 JST)")
+    raise SystemExit(f"[25_05] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2018-04-08 16:32:30.81 UTC ± 60 s。25_00 の表示の 01:32:30.81 JST)")
 CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
@@ -205,5 +224,5 @@
 if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
-    raise SystemExit("[24_05] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
-print(f"[24_05] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
-print(f"[24_05] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
+    raise SystemExit("[25_05] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
+print(f"[25_05] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
+print(f"[25_05] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
       f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")
@@ -218,3 +237,3 @@
     kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
-    if len(set(kk)) != n: raise SystemExit(f"[24_05] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
+    if len(set(kk)) != n: raise SystemExit(f"[25_05] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
 HASP = ~np.isnan(TFIRST)
@@ -230,6 +249,6 @@
 EX, EY = to_xy(SRC[:, 0], SRC[:, 1])
-print(f"[24_05] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
+print(f"[25_05] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
 EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
-if len(EVAL) == 0: raise SystemExit("[24_05] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
-if a.dev: print(f"[24_05] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
+if len(EVAL) == 0: raise SystemExit("[25_05] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
+if a.dev: print(f"[25_05] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                 "(較正にも入っているので値は楽観的)")
@@ -241,7 +260,7 @@
 if a.no_causal:
-    H5_SKIP = "--no-causal: 24_07 could not be run or its output failed the checks (preregistration 24, section 5.5)"
+    H5_SKIP = "--no-causal: 24_07 could not be run or its output failed the checks (preregistration 25, section 5.5)"
     CAUS_ALL = {}
-    print("[24_05] --no-causal: 24_07 の出力を読まない。H5 は評価しない(NOT-EVALUATED)。H1〜H4・HL・HG は同じ規則で回す(事前登録 24 の 5.5 節)")
+    print("[25_05] --no-causal: 24_07 の出力を読まない。H5 は評価しない(NOT-EVALUATED)。H1〜H4・HL・HG は同じ規則で回す(事前登録 25 の 5.5 節)")
 elif not CP_C.exists() or not CJ_C.exists():
-    raise SystemExit(f"[24_05] STOP: 24_07 の出力 {a.causal_picks} か {a.causal_json} が無い(ノートの セル N16 の後に Mac にコピーする)")
+    raise SystemExit(f"[25_05] STOP: 24_07 の出力 {a.causal_picks} か {a.causal_json} が無い(ノートの セル N16 の後に Mac にコピーする)")
 if not a.no_causal:
@@ -249,10 +268,10 @@
     if CJ.get("script_sha256") != CAUSAL_SCRIPT_SHA:
-        raise SystemExit(f"[24_05] STOP: 24_07 の SHA-256 {str(CJ.get('script_sha256'))[:12]}… が凍結の値 {CAUSAL_SCRIPT_SHA[:12]}… と違う")
+        raise SystemExit(f"[25_05] STOP: 24_07 の SHA-256 {str(CJ.get('script_sha256'))[:12]}… が凍結の値 {CAUSAL_SCRIPT_SHA[:12]}… と違う")
     if CJ.get("cache_sha256") != CACHE_SHA:
-        raise SystemExit(f"[24_05] STOP: 24_07 が使ったキャッシュの SHA-256 {str(CJ.get('cache_sha256'))[:12]}… が、このキャッシュ {CACHE_SHA[:12]}… と違う")
+        raise SystemExit(f"[25_05] STOP: 24_07 が使ったキャッシュの SHA-256 {str(CJ.get('cache_sha256'))[:12]}… が、このキャッシュ {CACHE_SHA[:12]}… と違う")
     if CJ.get("csv_sha256") != sha256(CP_C):
-        raise SystemExit("[24_05] STOP: 24_07 の CSV の SHA-256 が、24_07 の JSON に書かれた値と違う(別の実行の CSV か JSON を置いた)")
+        raise SystemExit("[25_05] STOP: 24_07 の CSV の SHA-256 が、24_07 の JSON に書かれた値と違う(別の実行の CSV か JSON を置いた)")
     if not CJ.get("all_events") or not CJ.get("raw_reconstructed"):
-        raise SystemExit("[24_05] STOP: 24_07 が --all-events で、元の値に戻した h5(24_02)で回されていない")
-    if len(set(OT)) != NE: raise SystemExit("[24_05] STOP: 発生時刻の同じ地震がキャッシュにある(24_07 の行を地震に対応付けられない)")
+        raise SystemExit("[25_05] STOP: 24_07 が --all-events で、元の値に戻した h5(25_02)で回されていない")
+    if len(set(OT)) != NE: raise SystemExit("[25_05] STOP: 発生時刻の同じ地震がキャッシュにある(24_07 の行を地震に対応付けられない)")
     CAUS_ALL, _OTI = {}, {OT[i]: i for i in range(NE)}
@@ -261,3 +280,3 @@
             ie_ = _OTI.get(r["origin_time"])
-            if ie_ is None: raise SystemExit(f"[24_05] STOP: 24_07 の地震 {r['origin_time']} がキャッシュに無い")
+            if ie_ is None: raise SystemExit(f"[25_05] STOP: 24_07 の地震 {r['origin_time']} がキャッシュに無い")
             ff = lambda v: float(v) if v not in ("", "nan", None) else np.nan
@@ -265,3 +284,3 @@
     _miss = [(OT[ie][:19], t) for ie in EVAL for t in TAUS if (ie, float(t)) not in CAUS_ALL]
-    if _miss: raise SystemExit(f"[24_05] STOP: 24_07 の検測が無い地震・時点 {len(_miss)}(最初 {_miss[0]})。評価の全ての地震 × 4 時点が要る")
+    if _miss: raise SystemExit(f"[25_05] STOP: 24_07 の検測が無い地震・時点 {len(_miss)}(最初 {_miss[0]})。評価の全ての地震 × 4 時点が要る")
     for ie in EVAL:
@@ -271,7 +290,7 @@
                 if not (0 <= k_ < n_) or not (np.isnan(v_[2]) and np.isnan(tpo[k_]) or abs(v_[2] - tpo[k_]) < 1e-6):
-                    raise SystemExit(f"[24_05] STOP: 24_07 の局 {k_} のオフラインの P が、キャッシュと合わない({OT[ie][:19]})")
-    print(f"[24_05] H5 の材料: 24_07 v3 SHA-256 {CAUSAL_SCRIPT_SHA[:12]}…・同じキャッシュ・元の値に戻した h5・評価の {len(EVAL)} 地震 × 4 時点がそろっている")
+                    raise SystemExit(f"[25_05] STOP: 24_07 の局 {k_} のオフラインの P が、キャッシュと合わない({OT[ie][:19]})")
+    print(f"[25_05] H5 の材料: 24_07 v3 SHA-256 {CAUSAL_SCRIPT_SHA[:12]}…・同じキャッシュ・元の値に戻した h5・評価の {len(EVAL)} 地震 × 4 時点がそろっている")
 
 # ---------------------------------------------------------------- 1 回だけの記録(本番は、試験の地震の結果を計算する前に書く)
-OPEN = ROOT / "models/24_05_opened.json"
+OPEN = ROOT / "models/25_05_opened.json"
 SUF = "_dev" if a.dev else ""
@@ -283,5 +302,5 @@
 if not a.dev:
-    if OPEN.exists() or (ROOT / "models/24_05_judgment.json").exists():
+    if OPEN.exists() or (ROOT / "models/25_05_judgment.json").exists():
         SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
-        print(f"[24_05] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
+        print(f"[25_05] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
     log_open("opened")
@@ -370,3 +389,3 @@
 LAP_B = float(np.median(np.abs(r1)) / np.log(2.0))
-print(f"[24_05] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
+print(f"[25_05] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
       f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")
@@ -381,3 +400,3 @@
 XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
-print(f"[24_05] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
+print(f"[25_05] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
       f"  固定の深さ {ZDEF:.1f} km")
@@ -417,3 +436,3 @@
 lls = {h: loo_ll(h) for h in HS}; KDE_H = max(lls, key=lls.get)
-print(f"[24_05] KDE の帯域(pool の一つ抜き): {KDE_H} km")
+print(f"[25_05] KDE の帯域(pool の一つ抜き): {KDE_H} km")
 def log_prior(nodes, mem):
@@ -445,3 +464,3 @@
     lib = np.where((OTNS <= OTNS[ie] - int(buffer_h * 3600e9)) & HASP)[0]
-    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[24_05] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
+    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[25_05] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
     return lib
@@ -531,3 +550,3 @@
     top = lib[np.argsort(-S, kind="stable")[:min(k, pos)]]
-    if ie is not None and ie in top: stop("[24_05] STOP: 自分自身が似た地震の上位に入っている")
+    if ie is not None and ie in top: stop("[25_05] STOP: 自分自身が似た地震の上位に入っている")
     out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
@@ -548,3 +567,3 @@
     lib = library(ie); libb = library(ie, BUFFER_SENS_H)
-    if not np.array_equal(libb[:len(lib)], lib): stop("[24_05] STOP: 過去の一覧の並びがおかしい")
+    if not np.array_equal(libb[:len(lib)], lib): stop("[25_05] STOP: 過去の一覧の並びがおかしい")
     p0 = FIRST[ie]
@@ -591,4 +610,4 @@
 if NT < MIN_TEST and not a.dev:
-    print(f"[24_05] 判定(事前宣言、H1): INCONCLUSIVE(評価できる試験の地震 {NT} < {MIN_TEST})")
-    json.dump(dict(script="24_05_nagano2014_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, verdict="INCONCLUSIVE",
+    print(f"[25_05] 判定(事前宣言、H1): INCONCLUSIVE(評価できる試験の地震 {NT} < {MIN_TEST})")
+    json.dump(dict(script="25_05_shimane2018_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, verdict="INCONCLUSIVE",
                    utc=utcnow(), suffix=SUF, cache=a.cache, cache_sha256=sha256(CP), n_test=int(len(test_idx)),
@@ -596,3 +615,3 @@
                    n_mj2_library_only=n_extra2), limits=LIMITS),
-              open(ROOT / f"models/24_05_judgment{SUF}.json", "w"), indent=1)
+              open(ROOT / f"models/25_05_judgment{SUF}.json", "w"), indent=1)
     log_open("completed: INCONCLUSIVE"); raise SystemExit(0)
@@ -608,3 +627,3 @@
     except BaseException as ex:
-        stop(f"[24_05] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
+        stop(f"[25_05] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
     for m in METH: P[m][ii] = R[m]
@@ -619,3 +638,3 @@
 gate_ev = [ii for ii in range(NT) if NI[ii, TAUS.index(1.0)] > 0][:N_GATE]
-if len(gate_ev) < 3: stop(f"[24_05] STOP(G-causal): τ = 1 s で似ている度合いが測れた地震が {len(gate_ev)} しかなく、確かめられない")
+if len(gate_ev) < 3: stop(f"[25_05] STOP(G-causal): τ = 1 s で似ている度合いが測れた地震が {len(gate_ev)} しかなく、確かめられない")
 gc_max, gc_n, pos_ctrl = 0.0, 0, None
@@ -651,3 +670,3 @@
 shared = [p for p in picks_of(ie, 1.0) if n_avail(1.0, p[4]) >= MINW_N and any(p[0] in filt_cached(j, BAND) for j in lib0)]
-if not shared: stop("[24_05] STOP(G-causal): 陽性対照に使える局が無い(この行を貼って相談)")
+if not shared: stop("[25_05] STOP(G-causal): 陽性対照に使える局が無い(この行を貼って相談)")
 pc = shared[0]; e2 = dict(orig); W = np.array(np.asarray(orig["waveforms"], float))
@@ -658,5 +677,5 @@
 pos_ctrl = float(np.max(np.abs(S1 - S0))) if len(S0) else 0.0
-print(f"[24_05] G-causal({len(gate_ev)} 地震 × τ = 0.5・1・2・3 s、未来の波形と検測を置き換えた時の最大の差): {gc_max:.3g}  "
+print(f"[25_05] G-causal({len(gate_ev)} 地震 × τ = 0.5・1・2・3 s、未来の波形と検測を置き換えた時の最大の差): {gc_max:.3g}  "
       f"陽性対照(窓の最後の点を変えた時の S の差): {pos_ctrl:.3g}  " + ("PASS" if (gc_max == 0.0 and pos_ctrl > 0) else "FAIL"))
-if not (gc_max == 0.0 and pos_ctrl > 0): stop("[24_05] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")
+if not (gc_max == 0.0 and pos_ctrl > 0): stop("[25_05] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")
 
@@ -688,5 +707,5 @@
 phys_inf = SUMM["M5"]["inf"]["median_km"]
-print(f"[24_05] G-phys(τ = ∞ の M5 の中央値 ≤ 0.5 km): {'—' if phys_inf is None else f'{phys_inf:.3f}'} km  " + ("PASS" if phys_inf is not None and phys_inf <= 0.5 else "FAIL")
+print(f"[25_05] G-phys(τ = ∞ の M5 の中央値 ≤ 0.5 km): {'—' if phys_inf is None else f'{phys_inf:.3f}'} km  " + ("PASS" if phys_inf is not None and phys_inf <= 0.5 else "FAIL")
       + "(参考: 15_12 は 0.13 km、分け方が違う)")
-if not (phys_inf is not None and phys_inf <= 0.5): stop("[24_05] STOP(G-phys): 物理を長野に正しく移せていない可能性(この行を貼って相談)")
+if not (phys_inf is not None and phys_inf <= 0.5): stop("[25_05] STOP(G-phys): 物理を島根に正しく移せていない可能性(この行を貼って相談)")
 def judge(meth, t, alpha, EE=None, SS=None):
@@ -743,6 +762,6 @@
 # H1〜H4 の結果を、H5 の計算の前に書いておく(H5 の計算で途切れても、H1〜H4 の結果が残る。最終の JSON は下の 12 節で書く)
-json.dump(clean_early(dict(script="24_05_nagano2014_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, suffix=SUF,
-                           status="H1-H4 written before H5; the final file is models/24_05_judgment" + SUF + ".json",
+json.dump(clean_early(dict(script="25_05_shimane2018_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, suffix=SUF,
+                           status="H1-H4 written before H5; the final file is models/25_05_judgment" + SUF + ".json",
                            summary=SUMM, hypotheses=HYP, verdict=VERDICT, hypotheses_24=HYP24, utc=utcnow())),
-          open(ROOT / f"models/24_05_judgment{SUF}_preH5.json", "w"), indent=1)
+          open(ROOT / f"models/25_05_judgment{SUF}_preH5.json", "w"), indent=1)
 def gate_causal_path():
@@ -789,8 +808,8 @@
         GC_C = dict(max_diff=gc_c, n_checks=gc_cn)
-        print(f"[24_05] G-causal(H5 の経路: τ までの検測・ずらした窓、{len(gate_ev)} 地震 × 4 時点): {gc_c:.3g}  " + ("PASS" if gc_c == 0.0 else "FAIL"))
+        print(f"[25_05] G-causal(H5 の経路: τ までの検測・ずらした窓、{len(gate_ev)} 地震 × 4 時点): {gc_c:.3g}  " + ("PASS" if gc_c == 0.0 else "FAIL"))
         if gc_c != 0.0: H5_SKIP = "G-causal on the causal-pick path failed (max difference %.3g)" % gc_c
-    except (Exception, SystemExit) as ex:        # H5 だけを評価しないで、H1〜H4 の結果は残す(事前登録 24 の 5.5 節)。Ctrl-C は止まる
+    except (Exception, SystemExit) as ex:        # H5 だけを評価しないで、H1〜H4 の結果は残す(事前登録 25 の 5.5 節)。Ctrl-C は止まる
         H5_SKIP = f"{'stop' if isinstance(ex, SystemExit) else 'exception'} during the H5 computation: {type(ex).__name__}: {str(ex)[:200]}"
     CAUS = None; FILT.clear(); IN_H5 = False
-    if H5_SKIP is not None: print(f"[24_05] H5 は評価しない(NOT-EVALUATED): {H5_SKIP}")
+    if H5_SKIP is not None: print(f"[25_05] H5 は評価しない(NOT-EVALUATED): {H5_SKIP}")
 EC = {m: herr(PC[m]) for m in CM_C}
@@ -813,3 +832,3 @@
 def fp(p): return "—" if p is None else f"{p:.2g}"
-print(f"\n[24_05] ===== 水平誤差の中央値 km [95% 区間](評価 {NT} 地震{'、dev(楽観的)' if a.dev else ''}) =====")
+print(f"\n[25_05] ===== 水平誤差の中央値 km [95% 区間](評価 {NT} 地震{'、dev(楽観的)' if a.dev else ''}) =====")
 print("  方法           " + "".join(f"{('τ=' + t + ' s') if t != 'inf' else '全検測':>24}" for t in TL))
@@ -831,3 +850,3 @@
       "(全検測でも C4 が物理より良いなら、その分は早さではなく気象庁の震源の枠に合わせた効果の可能性)")
-print(f"\n[24_05] ===== 事前宣言の判定 =====")
+print(f"\n[25_05] ===== 事前宣言の判定 =====")
 for name, h in HYP.items():
@@ -849,4 +868,4 @@
                                         f"{d['C3']['best_median_km']:.2f}・C3 {f2(d['C3']['median_km'])} km" for t, d in PER_TAU_C.items()))
-print(f"\n[24_05] 判定(事前宣言、H1): {VERDICT}")
-print("[24_05] 限界: " + " / ".join(LIMITS))
+print(f"\n[25_05] 判定(事前宣言、H1): {VERDICT}")
+print("[25_05] 限界: " + " / ".join(LIMITS))
 
@@ -862,3 +881,3 @@
 CM = BASE + NEW + SENSN + ALLP
-with open(ROOT / f"data/24_05_per_event{SUF}.csv", "w", newline="") as f:
+with open(ROOT / f"data/25_05_per_event{SUF}.csv", "w", newline="") as f:
     w = csv.writer(f)
@@ -877,4 +896,4 @@
                                                   for j in range(len(TAUS))])
-out = dict(script="24_05_nagano2014_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
-           sequence="Northern Nagano 2014", suffix=SUF, cache=a.cache, cache_sha256=sha256(CP),
+out = dict(script="25_05_shimane2018_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
+           sequence="Western Shimane 2018", suffix=SUF, cache=a.cache, cache_sha256=sha256(CP),
            n_fresh=int(FRESH.sum()), n_events=NE, n_pool=int(len(pool_idx)), n_test=int(len(test_idx)),
@@ -904,4 +923,4 @@
                         "fewer than 30 evaluated events. H2: C4 at tau = 2 s, H3: C3 at tau = 0.5 s, each alpha 0.005 (secondary). "
-                        "Test events: 1.5 <= Mj < 2.0 events later than mainshock + 72 h (Northern Nagano 2014; same rule as 21_02 v2, 21_04 v1 and 21_20 v1). "
-                        "Added in preregistration 24: H4 (secondary, alpha 0.005): C3 vs C1 at tau = 2 s on events where both exist, "
+                        "Test events: 1.5 <= Mj < 2.0 events later than mainshock + 72 h (Western Shimane 2018; same rule as 21_02 v2, 21_04 v1 and 21_20 v1). "
+                        "Added in preregistration 24 and kept unchanged in preregistration 25: H4 (secondary, alpha 0.005): C3 vs C1 at tau = 2 s on events where both exist, "
                         "win if the C3 median < the C1 median, one-sided paired Wilcoxon p < 0.005 and >= 10 non-zero pairs (no floor rule). "
@@ -910,3 +929,3 @@
            limits=LIMITS, runtime_s=time.time() - T0)
-json.dump(clean(out), open(ROOT / f"models/24_05_judgment{SUF}.json", "w"), indent=1)
+json.dump(clean(out), open(ROOT / f"models/25_05_judgment{SUF}.json", "w"), indent=1)
 if not a.dev: log_open("completed: " + VERDICT)
@@ -941,6 +960,6 @@
 ax.set_xlabel("Time since first P pick, tau (s)"); ax.set_ylabel("Median epicentral error vs JMA (km)")
-ax.set_title(f"Northern Nagano 2014, {'DEV (pool events, optimistic)' if a.dev else 'test events'}, n = {NT}; shading = 95% bootstrap CI",
+ax.set_title(f"Western Shimane 2018, {'DEV (pool events, optimistic)' if a.dev else 'test events'}, n = {NT}; shading = 95% bootstrap CI",
              fontsize=10)
 ax.grid(alpha=0.3, which="both"); ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F1_error_vs_tau{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/25_05_F1_error_vs_tau{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
 
@@ -960,3 +979,3 @@
 fig.legend(h_, l_, loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=2, fontsize=8, frameon=False)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F2_paired_difference{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/25_05_F2_paired_difference{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
 
@@ -970,3 +989,3 @@
 ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F3_similarity_vs_separation{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/25_05_F3_similarity_vs_separation{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
 fig, ax = plt.subplots(figsize=(7.8, 4.4))
@@ -984,7 +1003,7 @@
 ax.set_xlabel("Time since first P pick, tau (s)"); ax.set_ylabel("Median epicentral error vs JMA (km)")
-ax.set_title(f"Northern Nagano 2014, {'DEV' if a.dev else 'test'} events (n = {NT}): offline vs causal picks"
+ax.set_title(f"Western Shimane 2018, {'DEV' if a.dev else 'test'} events (n = {NT}): offline vs causal picks"
              + ("" if H5_SKIP is None else "\n(H5 not evaluated: causal picks not available)"), fontsize=10)
 ax.grid(alpha=0.3, which="both"); ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F4_causal_picks{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"[24_05] 出力: models/24_05_judgment{SUF}.json, data/24_05_per_event{SUF}.csv, PDF/24_05_F1〜F4{SUF}.pdf"
-      + ("" if a.dev else ", models/24_05_opened.json") + f"  ({time.time()-T0:.0f} s)")
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/25_05_F4_causal_picks{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"[25_05] 出力: models/25_05_judgment{SUF}.json, data/25_05_per_event{SUF}.csv, PDF/25_05_F1〜F4{SUF}.pdf"
+      + ("" if a.dev else ", models/25_05_opened.json") + f"  ({time.time()-T0:.0f} s)")
```

## 25_06f_shimane2018_learned_test.py ← 24_06f_nagano2014_learned_test.py

```diff
--- ../nagano/frz/24_06f_nagano2014_learned_test.py	2026-11-15 05:21:00.096885666 +0000
+++ frz/25_06f_shimane2018_learned_test.py	2026-11-17 01:57:17.163758795 +0000
@@ -2,17 +2,16 @@
 # =============================================================================
-# Script : 24_06f_nagano2014_learned_test.py  (v1)
-#          [学習型 ARGUS の 4 つ目の系列での試験: 鳥取 2026 で学習して凍結した「似た地震の選び方」(21_06a のモデル)を、学び直さずに、
-#           手を付けていない長野県北部 2014 で 1 回だけ試す。位置は C3・C4 と同じ物理の計算で決める(AI は物理の部品)]
-# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の学習型の腕
-# 派生元 : 21_20f_osaka2018_learned_test.py v1(SHA-256 9623695ea33bef90605cd47d4fb8fceb16a8bbbe91327bfa51783aa347d29925)。
-#          21_06 FEATURES の印の間・凍結したモデル・学習の記録・G-model・仮説と判定の規則は 1 字も変えていない。変えたのは次だけ(DIFF_LOG_24.md):
-#          (1) 入力の既定のキャッシュ(24_05 と同じ R1 の後のもの)、MAIN_UTC・UNTOUCHED_UTC(24_05 と同じ)、限界の文(24_05 と同じ LIMITS)
-#          (2) 比べる相手と順番の確かめを 21_20 の出力から 24_05 の出力に変えた: data/24_05_per_event.csv(--dev は _dev)、
-#              models/24_05_judgment.json(最初の本番で、キャッシュの SHA-256 が同じこと)、models/24_05_opened.json(21_06a の学習が先か)
-#          (3) 出力の名前: models/24_06f_judgment.json / models/24_06f_opened.json / data/24_06f_per_event.csv / PDF/24_06f_F1_learned_test.pdf、
-#              表示の [24_06f]、系列の名前。記述用の L3p・L4p は「2026 の学習の行 + 2014 の pool の行」で学び直す(判定には使わない)
-#          (4) --ref-suffix(24_06g と同じ)と、24_05 の結果が凍結した 24_05 v1(SHA_2405)のものかの照合: 24_05 を事前登録 24 の 6 節の機械的な中断で 1 回やり直した時だけ、正式な結果の suffix
-#              (_rerun_<UTC>)を渡す。models/24_05_opened.json で最初に completed になった実行の suffix と一致しなければ STOP
+# Script : 25_06f_shimane2018_learned_test.py  (v1)
+#          [学習型 ARGUS の 5 つ目の系列での試験: 鳥取 2026 で学習して凍結した「似た地震の選び方」(21_06a のモデル)を、学び直さずに、
+#           手を付けていない島根県西部 2018 で 1 回だけ試す。位置は C3・C4 と同じ物理の計算で決める(AI は物理の部品)]
+# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の学習型の腕
+# 派生元 : 24_06f_nagano2014_learned_test.py v1(SHA-256 779c04a8c01ebf6d1250818d81a743809e794c0751e8960bd7862037ad97f5f5。事前登録 24 で凍結。
+#          長野では回していない)。21_06 FEATURES の印の間・凍結したモデル・学習の記録・G-model・仮説と判定の規則・--ref-suffix の扱いは
+#          24_06f v1 と 1 字も変えていない。変えたのは次だけ(DIFF_LOG_25.md):
+#          (1) 入力の既定のキャッシュ(25_05 と同じ R1 の後のもの)、MAIN_UTC・UNTOUCHED_UTC(25_05 と同じ)、限界の文(25_05 と同じ LIMITS の書き換え)
+#          (2) 比べる相手の名前: data/25_05_per_event.csv(--dev は _dev)、models/25_05_judgment.json、models/25_05_opened.json。
+#              照らす 25_05 の SHA-256 は SHA_2505(凍結の時に書く。25_06g・25_08 と同じ)
+#          (3) 出力の名前: models/25_06f_judgment.json / models/25_06f_opened.json / data/25_06f_per_event.csv / PDF/25_06f_F1_learned_test.pdf、
+#              表示の [25_06f]、系列の名前。記述用の L3p・L4p は「2026 の学習の行 + 2018 の pool の行」で学び直す(判定には使わない。24_06f と同じ)
 #
-# 事前登録の仮説と判定(21_06・21_20f と同じ。事前登録の記録 24 に再掲):
+# 事前登録の仮説と判定(21_06・21_20f・24_06f と同じ。事前登録の記録 25 に再掲):
 #   HL1(主)  L4 @ τ = 2 s が BEST より良い、p < 0.01、BEST ≥ 0.5 km  → LEARNED-CONFIRMED / PHYSICS-AT-FLOOR / NOT-CONFIRMED
@@ -22,8 +21,8 @@
 #
-# Usage : (24_05 の本番が終わってから)
-#         cd ~/SWIFT && caffeinate -i uv run python src/24_06f_nagano2014_learned_test.py --dev   (動作確認。24_05 の dev の CSV が要る)
-#         cd ~/SWIFT && caffeinate -i uv run python src/24_06f_nagano2014_learned_test.py         (本番。1 回だけ)
-# 入力  : 24_05 と同じキャッシュ、data/24_05_per_event.csv と models/24_05_judgment.json・models/24_05_opened.json(--dev なら _dev の CSV)、
+# Usage : (25_05 の本番が終わってから)
+#         cd ~/SWIFT && caffeinate -i uv run python src/25_06f_shimane2018_learned_test.py --dev   (動作確認。25_05 の dev の CSV が要る)
+#         cd ~/SWIFT && caffeinate -i uv run python src/25_06f_shimane2018_learned_test.py         (本番。1 回だけ)
+# 入力  : 25_05 と同じキャッシュ、data/25_05_per_event.csv と models/25_05_judgment.json・models/25_05_opened.json(--dev なら _dev の CSV)、
 #         models/21_06a_train.json・models/21_06_ranker.pkl・data/21_06a_train_rows.npz(21_06a の出力。凍結 B のまま)
-# Output: models/24_06f_judgment.json / models/24_06f_opened.json / data/24_06f_per_event.csv / PDF/24_06f_F1_learned_test.pdf
+# Output: models/25_06f_judgment.json / models/25_06f_opened.json / data/25_06f_per_event.csv / PDF/25_06f_F1_learned_test.pdf
 # =============================================================================
@@ -38,6 +37,6 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--cache", default="data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt", help="24_03(15_01c v3.3 と同じ計算)の長野県北部 2014 の M>=1.5 版に 24_03h の R1 を当てたもの(24_05 と同じ)")
-ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(24_05 の dev と同じ 20 地震。比べる相手は data/24_05_per_event_dev.csv)")
-SHA_2405 = "c10d15fe404309d836fc83fb2dbe1d207fa477d9597900724f487ef965970f9f"                          # 事前登録 24 で凍結した 24_05 v1 の SHA-256(24_06g・24_08 と同じ照合)
-ap.add_argument("--ref-suffix", default="", help="24_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
+ap.add_argument("--cache", default="data/shimane2018_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt", help="25_03(15_01c v3.3 と同じ計算)の島根県西部 2018 の M>=1.5 版に 25_03h の R1 を当てたもの(25_05 と同じ)")
+ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(25_05 の dev と同じ 20 地震。比べる相手は data/25_05_per_event_dev.csv)")
+SHA_2505 = "80309ce7012b89af0c052e225cb66b2e15ee104af247937b63510064f9c11398"                          # 事前登録 25 で凍結する 25_05 v1 の SHA-256(25_06g・25_08 と同じ照合)
+ap.add_argument("--ref-suffix", default="", help="25_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
 ap.add_argument("--train-json", default="models/21_06a_train.json", help="21_06a の学習の記録(凍結したモデルの SHA-256 を持つ)")
@@ -61,21 +60,29 @@
 NBOOT, SEED, N_DEV, N_GATE = 2000, 12, 20, 5
-MAIN_UTC = dt.datetime(2014, 11, 22, 13, 8, 17, 900000)   # 24_05 と同じ: 24_00 の表示の本震 2014-11-22 22:08:17.90 JST(± 60 s、Mj ≥ 6.0 の確かめ)
-UNTOUCHED_UTC = (dt.datetime(2014, 11, 20), dt.datetime(2014, 12, 17))     # G-untouched: 24_01 の期間(本震の 2 日前〜24 日後)を日の単位で含む
-LIMITS = ["fourth sequence: Northern Nagano 2014 (mainshock 2014-11-22, 22:08:17.90 JST, Mj 6.7; JMA catalogue values, see 24_01's JSON), "
+MAIN_UTC = dt.datetime(2018, 4, 8, 16, 32, 30, 810000)   # 25_05 と同じ: 25_00 の表示の本震 2018-04-09 01:32:30.81 JST(± 60 s、Mj ≥ 6.0 の確かめ)
+UNTOUCHED_UTC = (dt.datetime(2018, 4, 6), dt.datetime(2018, 5, 3))     # G-untouched: 25_01 の期間(本震の 2 日前〜24 日後)を日の単位で含む
+LIMITS = ["fifth sequence: Western Shimane 2018 (mainshock 2018-04-09, 01:32:30.81 JST, Mj 6.1; JMA catalogue values, see 25_01's JSON), "
           "never used in ARGUS development; the hypotheses H1-H3 were fixed on West Tottori 2026 (21_01/21_02), tested on Central Tottori 2016 "
-          "(21_04, with a documented deviation) and Northern Osaka 2018 (21_20, re-registered with amendment 04) and are applied here unchanged",
-          "one fourth sequence only; before this preregistration the catalogue h2014 was opened once by 24_00 to count events "
-          "(counts and the mainshock row only; no location list, waveform or method error was looked at)",
+          "(21_04, with a documented deviation) and Northern Osaka 2018 (21_20, re-registered with amendment 04) and are applied here unchanged; "
+          "the fourth sequence (Northern Nagano 2014, preregistration 24 with the same rules) was stopped by the clock check G-clock2 before "
+          "its test was opened, and its rules (including H4 and H5) are carried over unchanged except G-clock2 condition (d)",
+          "one fifth sequence only; before this preregistration the catalogue h2018 was opened by 25_00 to count events "
+          "(counts and the mainshock row only; no location list, waveform or method error was looked at); h2018 had been opened before "
+          "for Northern Osaka 2018 (21_20a), whose box and period do not include this sequence",
+          "the catalogue-only count of test candidates after rule R1 was 41 in 25_00 (25_00 required at least 40 to select a sequence); "
+          "events without a PhaseNet P in the cache are not evaluated, and fewer than 30 evaluated events give INCONCLUSIVE",
+          "25 of these 41 catalogue test candidates have JMA's automatic-hypocentre flag (A), 15 are K and 1 is k (25_00); the truth and "
+          "past-event locations therefore mix manual and automatic JMA hypocentres; errors by flag are described by 25_09 (no test)",
           "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
-          "set of 50 stations also included non-Hi-net stations, so station types and geometry differ",
+          "set of 50 stations also included non-Hi-net stations, so station types and geometry differ; stations that existed in 2018 but "
+          "are not in the current NIED list cannot be candidates",
           "waveforms were downloaded around catalogue events only and converted to the West Tottori 2026 h5 form (30-s windows, "
-          "per-window per-component z-score, JST epoch; 24_02 also stores the window mean and standard deviation); no filter was applied "
-          "before the z-score (compared in 24_02 G-spec)",
-          "the cache was built by 24_03, whose picking, QC and assembly are identical to 15_01c v3.3; 24_03h then removed every event "
+          "per-window per-component z-score, JST epoch; 25_02 also stores the window mean and standard deviation); no filter was applied "
+          "before the z-score (compared in 25_02 G-spec)",
+          "the cache was built by 25_03, whose picking, QC and assembly are identical to 15_01c v3.3; 25_03h then removed every event "
           "with another catalogue event from 15 s before to 5 s after its origin (rule R1 of 21_20 amendment 04, fixed here before any "
-          "Nagano waveform was opened; it uses origin times and Mj only), which can bias the sample against busy periods",
-          "catalogue: JMA hypocentres from h2014 (whether h2014 is the final stage is to be confirmed); past-event locations are JMA "
+          "Shimane waveform was opened; it uses origin times and Mj only), which can bias the sample against busy periods",
+          "catalogue: JMA hypocentres from h2018 (whether h2018 is the final stage is to be confirmed); past-event locations are JMA "
           "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
-          "the 2014 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
-          "events. Manual and automatic hypocentres can be mixed (per-flag counts in 24_01's JSON)",
+          "the 2018 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
+          "events. Manual and automatic hypocentres can be mixed (per-flag counts in 25_01's JSON)",
           "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); "
@@ -102,2 +109,9 @@
           "offline picks (their records are complete at the time of the target event)",
+          "the clock check G-clock2 condition (d) was redesigned for this preregistration on four earlier sequences only (25_04x, 25_04y, "
+          "25_04z and 25_04v; Shimane was not opened): 5 consecutive events after mainshock + 72 h, median of event medians within 0.5 s; "
+          "it does not check common timing errors that affect only one or two events, or events within 72 h of the mainshock; its "
+          "positive control was set to +1.0 s on 4 consecutive events after +0.6 s could not be met together with the negative control "
+          "(25_04z); a 0.6 s common offset over 4 events is therefore not reliably detected",
+          "if the station-level clock check G-clock2 (c) fails only at stations farther than 80 km, the test proceeds with a fixed label "
+          "(preregistration 25, section 5.3); a constant clock offset at a far station can be missed",
           "H1 (C3 at tau = 2 s) is the primary test; H2, H3 and H4 are secondary at alpha 0.005; H5 (causal picks) uses the H1 rule at "
@@ -115,3 +129,3 @@
 SELF_SHA = sha256(Path(__file__))
-print(f"[24_06f] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
+print(f"[25_06f] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
       f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")
@@ -120,3 +134,3 @@
 CP = ROOT / a.cache
-if not CP.exists(): raise SystemExit(f"[24_06f] STOP: {a.cache} が無い(ノート 24_nagano2014_colab.ipynb のセル N12 で作った tottori_parsed_realpick_nagano2014_m15_r1.pt を data/nagano2014_processed/ に置く)")
+if not CP.exists(): raise SystemExit(f"[25_06f] STOP: {a.cache} が無い(ノート 25_shimane2018_colab.ipynb のセル N12 で作った tottori_parsed_realpick_shimane2018_m15_r1.pt を data/shimane2018_processed/ に置く)")
 EVS = torch.load(CP, map_location="cpu", weights_only=False)
@@ -125,7 +139,7 @@
     miss = [k for k in need if k not in e]
-    if miss: raise SystemExit(f"[24_06f] STOP: キャッシュの地震に {miss} が無い(24_03・24_03h の出力か確かめる)")
+    if miss: raise SystemExit(f"[25_06f] STOP: キャッシュの地震に {miss} が無い(25_03・25_03h の出力か確かめる)")
 for e in EVS:
     w_ = np.asarray(e["waveforms"])
-    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[24_06f] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
-    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[24_06f] STOP: {e['origin_time']} の波形に NaN か無限大")
+    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[25_06f] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
+    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[25_06f] STOP: {e['origin_time']} の波形に NaN か無限大")
 def to_ns(o):
@@ -137,3 +151,3 @@
     except Exception:
-        raise SystemExit(f"[24_06f] STOP: origin_time {o!r} を時刻として読めない")
+        raise SystemExit(f"[25_06f] STOP: origin_time {o!r} を時刻として読めない")
 OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
@@ -145,4 +159,4 @@
 if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
-    raise SystemExit("[24_06f] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
-if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[24_06f] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
+    raise SystemExit("[25_06f] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
+if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[25_06f] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
 # G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
@@ -153,10 +167,10 @@
 n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
-print(f"[24_06f] 入力: 長野県北部 2014 の M ≥ 1.5 版(R1 の後) {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
+print(f"[25_06f] 入力: 島根県西部 2018 の M ≥ 1.5 版(R1 の後) {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
       f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
-print(f"[24_06f] G-untouched: 期間 2014-11-20〜2014-12-17(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
+print(f"[25_06f] G-untouched: 期間 2018-04-06〜2018-05-03(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
       + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
-if n_out != 0 or n_big != 1: raise SystemExit("[24_06f] STOP(G-untouched): 長野県北部 2014 のキャッシュに見えない(この行を貼って相談)")
+if n_out != 0 or n_big != 1: raise SystemExit("[25_06f] STOP(G-untouched): 島根県西部 2018 のキャッシュに見えない(この行を貼って相談)")
 im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
 if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
-    raise SystemExit(f"[24_06f] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2014-11-22 13:08:17.9 UTC ± 60 s。24_00 の表示の 22:08:17.90 JST)")
+    raise SystemExit(f"[25_06f] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2018-04-08 16:32:30.81 UTC ± 60 s。25_00 の表示の 01:32:30.81 JST)")
 CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
@@ -164,5 +178,5 @@
 if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
-    raise SystemExit("[24_06f] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
-print(f"[24_06f] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
-print(f"[24_06f] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
+    raise SystemExit("[25_06f] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
+print(f"[25_06f] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
+print(f"[25_06f] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
       f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")
@@ -177,3 +191,3 @@
     kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
-    if len(set(kk)) != n: raise SystemExit(f"[24_06f] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
+    if len(set(kk)) != n: raise SystemExit(f"[25_06f] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
 HASP = ~np.isnan(TFIRST)
@@ -189,6 +203,6 @@
 EX, EY = to_xy(SRC[:, 0], SRC[:, 1])
-print(f"[24_06f] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
+print(f"[25_06f] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
 EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
-if len(EVAL) == 0: raise SystemExit("[24_06f] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
-if a.dev: print(f"[24_06f] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
+if len(EVAL) == 0: raise SystemExit("[25_06f] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
+if a.dev: print(f"[25_06f] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                 "(較正にも入っているので値は楽観的)")
@@ -196,3 +210,3 @@
 # ---------------------------------------------------------------- 1 回だけの記録(本番は、試験の地震の結果を計算する前に書く)
-OPEN = ROOT / "models/24_06f_opened.json"
+OPEN = ROOT / "models/25_06f_opened.json"
 SUF = "_dev" if a.dev else ""
@@ -203,6 +217,6 @@
 if not a.dev:
-    if OPEN.exists() or (ROOT / "models/24_06f_judgment.json").exists():
+    if OPEN.exists() or (ROOT / "models/25_06f_judgment.json").exists():
         SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
-        print(f"[24_06f] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
-OPENED = False                           # 21_20f: 試験を開くのは、学習の記録・モデル・24_05 の結果の確認が全て通った後(8. の最後)
+        print(f"[25_06f] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
+OPENED = False                           # 21_20f: 試験を開くのは、学習の記録・モデル・25_05 の結果の確認が全て通った後(8. の最後)
 def stop(msg):
@@ -274,3 +288,3 @@
 LAP_B = float(np.median(np.abs(r1)) / np.log(2.0))
-print(f"[24_06f] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
+print(f"[25_06f] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
       f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")
@@ -285,3 +299,3 @@
 XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
-print(f"[24_06f] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
+print(f"[25_06f] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
       f"  固定の深さ {ZDEF:.1f} km")
@@ -321,3 +335,3 @@
 lls = {h: loo_ll(h) for h in HS}; KDE_H = max(lls, key=lls.get)
-print(f"[24_06f] KDE の帯域(pool の一つ抜き): {KDE_H} km")
+print(f"[25_06f] KDE の帯域(pool の一つ抜き): {KDE_H} km")
 def log_prior(nodes, mem):
@@ -349,3 +363,3 @@
     lib = np.where((OTNS <= OTNS[ie] - int(buffer_h * 3600e9)) & HASP)[0]
-    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[24_06f] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
+    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[25_06f] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
     return lib
@@ -425,3 +439,3 @@
     top = lib[np.argsort(-S, kind="stable")[:min(k, pos)]]
-    if ie is not None and ie in top: stop("[24_06f] STOP: 自分自身が似た地震の上位に入っている")
+    if ie is not None and ie in top: stop("[25_06f] STOP: 自分自身が似た地震の上位に入っている")
     out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
@@ -573,3 +587,3 @@
 
-# ---------------------------------------------------------------- 8. 凍結したモデルと 24_05 の結果の読み込み
+# ---------------------------------------------------------------- 8. 凍結したモデルと 25_05 の結果の読み込み
 import pickle
@@ -579,47 +593,47 @@
 except ImportError:
-    stop("[24_06f] STOP: scikit-learn が無い(21_06a と同じ環境で回す)")
+    stop("[25_06f] STOP: scikit-learn が無い(21_06a と同じ環境で回す)")
 TJP = ROOT / a.train_json
-if not TJP.exists(): stop(f"[24_06f] STOP: 学習の記録 {a.train_json} が無い(先に 21_06a)")
+if not TJP.exists(): stop(f"[25_06f] STOP: 学習の記録 {a.train_json} が無い(先に 21_06a)")
 TJ = json.load(open(TJP))
 if not a.dev and (a.train_json != "models/21_06a_train.json" or TJ.get("mode") != "train" or TJ.get("suffix", "") != ""):
-    stop("[24_06f] STOP: 本番は、事前登録した 21_06a の最初の本番の学習(models/21_06a_train.json、mode train)でしか回さない")
+    stop("[25_06f] STOP: 本番は、事前登録した 21_06a の最初の本番の学習(models/21_06a_train.json、mode train)でしか回さない")
 FB = open(Path(__file__), encoding="utf-8").read()
 FEAT_SHA = hashlib.sha256(FB[FB.index("# >>> 21_06 FEATURES BEGIN"):FB.index("# <<< 21_06 FEATURES END")].encode()).hexdigest()
-if TJ["feature_block_sha256"] != FEAT_SHA: stop("[24_06f] STOP(G-feat): 特徴量の部分が 21_06a と 1 字でも違う(学習と試験で同じ計算になっていない)")
+if TJ["feature_block_sha256"] != FEAT_SHA: stop("[25_06f] STOP(G-feat): 特徴量の部分が 21_06a と 1 字でも違う(学習と試験で同じ計算になっていない)")
 MP = ROOT / TJ["model_path"]
-if not MP.exists() or sha256(MP) != TJ["model_sha256"]: stop(f"[24_06f] STOP(G-model): モデル {TJ['model_path']} が無いか、SHA-256 が学習の記録と違う")
-if TJ["sklearn"] != sklearn.__version__: stop(f"[24_06f] STOP: scikit-learn の版が学習時({TJ['sklearn']})と違う({sklearn.__version__})")
+if not MP.exists() or sha256(MP) != TJ["model_sha256"]: stop(f"[25_06f] STOP(G-model): モデル {TJ['model_path']} が無いか、SHA-256 が学習の記録と違う")
+if TJ["sklearn"] != sklearn.__version__: stop(f"[25_06f] STOP: scikit-learn の版が学習時({TJ['sklearn']})と違う({sklearn.__version__})")
 if TJ["feats"] != FEATS or TJ["hgb"] != HGB or TJ.get("block_consts") != json.loads(json.dumps(BLOCK_CONSTS)) or TJ.get("cond_min") != COND_MIN:
-    stop("[24_06f] STOP: 特徴量の名前・設定・特徴量が使う定数が学習の記録と違う")
-if TJ["numpy"] != np.__version__: stop(f"[24_06f] STOP: numpy の版が学習時({TJ['numpy']})と違う({np.__version__})")
+    stop("[25_06f] STOP: 特徴量の名前・設定・特徴量が使う定数が学習の記録と違う")
+if TJ["numpy"] != np.__version__: stop(f"[25_06f] STOP: numpy の版が学習時({TJ['numpy']})と違う({np.__version__})")
 with open(MP, "rb") as f: MODEL = pickle.load(f)
 RP = ROOT / TJ["train_rows_path"]
-if not RP.exists() or sha256(RP) != TJ["train_rows_sha256"]: stop(f"[24_06f] STOP: 学習の行 {RP.relative_to(ROOT)} が無いか SHA-256 が違う")
-print(f"[24_06f] 凍結したモデル: {TJ['model_path']} SHA-256 {TJ['model_sha256'][:12]}…(2026 の {TJ['n_train_events']} 地震で学習)  "
+if not RP.exists() or sha256(RP) != TJ["train_rows_sha256"]: stop(f"[25_06f] STOP: 学習の行 {RP.relative_to(ROOT)} が無いか SHA-256 が違う")
+print(f"[25_06f] 凍結したモデル: {TJ['model_path']} SHA-256 {TJ['model_sha256'][:12]}…(2026 の {TJ['n_train_events']} 地震で学習)  "
       f"特徴量の部分 {FEAT_SHA[:12]}… G-feat PASS  G-model PASS")
 TJ_SHA = sha256(TJP)
-REFCSV = ROOT / ("data/24_05_per_event_dev.csv" if a.dev else f"data/24_05_per_event{a.ref_suffix}.csv")
-if not REFCSV.exists(): stop(f"[24_06f] STOP: {REFCSV.relative_to(ROOT)} が無い(先に 24_05 を回す。24_06f は 24_05 の後)")
+REFCSV = ROOT / ("data/25_05_per_event_dev.csv" if a.dev else f"data/25_05_per_event{a.ref_suffix}.csv")
+if not REFCSV.exists(): stop(f"[25_06f] STOP: {REFCSV.relative_to(ROOT)} が無い(先に 25_05 を回す。25_06f は 25_05 の後)")
 ref = {r["origin_time"]: r for r in csv.DictReader(open(REFCSV))}
 if sorted(ref) != sorted(OT[ie] for ie in EVAL):
-    stop(f"[24_06f] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
-J04 = ROOT / f"models/24_05_judgment{a.ref_suffix}.json"
+    stop(f"[25_06f] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
+J04 = ROOT / f"models/25_05_judgment{a.ref_suffix}.json"
 if J04.exists() and not a.dev:
     j4 = json.load(open(J04))
-    if j4.get("mode") != "test" or j4.get("suffix", "") != a.ref_suffix: stop(f"[24_06f] STOP: {J04.name} が 24_05 の本番の結果(suffix '{a.ref_suffix}')でない")
-    if j4.get("script_sha256") != SHA_2405: stop(f"[24_06f] STOP: 24_05 の結果が、凍結した 24_05 v1(SHA-256 {SHA_2405[:12]}…)のものでない")
-    _O = ROOT / "models/24_05_opened.json"
+    if j4.get("mode") != "test" or j4.get("suffix", "") != a.ref_suffix: stop(f"[25_06f] STOP: {J04.name} が 25_05 の本番の結果(suffix '{a.ref_suffix}')でない")
+    if j4.get("script_sha256") != SHA_2505: stop(f"[25_06f] STOP: 25_05 の結果が、凍結した 25_05 v1(SHA-256 {SHA_2505[:12]}…)のものでない")
+    _O = ROOT / "models/25_05_opened.json"
     _c = [r for r in (json.load(open(_O)) if _O.exists() else []) if str(r.get("status", "")).startswith("completed")]
     if not _c or _c[0].get("suffix", "") != a.ref_suffix:
-        stop(f"[24_06f] STOP: --ref-suffix '{a.ref_suffix}' が、models/24_05_opened.json で最初に completed になった 24_05 の実行と違う")
-    if j4.get("cache_sha256") != CACHE_SHA: stop("[24_06f] STOP: キャッシュの SHA-256 が 24_05 の本番と違う")
-    print("[24_06f] キャッシュの SHA-256 は 24_05 の本番と同じ")
-    O4 = ROOT / "models/24_05_opened.json"
+        stop(f"[25_06f] STOP: --ref-suffix '{a.ref_suffix}' が、models/25_05_opened.json で最初に completed になった 25_05 の実行と違う")
+    if j4.get("cache_sha256") != CACHE_SHA: stop("[25_06f] STOP: キャッシュの SHA-256 が 25_05 の本番と違う")
+    print("[25_06f] キャッシュの SHA-256 は 25_05 の本番と同じ")
+    O4 = ROOT / "models/25_05_opened.json"
     t4 = json.load(open(O4))[0]["utc"] if O4.exists() else None
-    print(f"[24_06f] 順番の確認: 21_06a の学習 {TJ.get('utc')} / 24_05 の本番を開いた時刻 {t4}(学習が先のはず。事前登録の push の時刻とも照らす)")
-    if t4 is not None and TJ.get("utc") is not None and TJ["utc"] > t4: stop("[24_06f] STOP: 21_06a の学習が 24_05 の本番より後(事前登録の順番と違う)")
+    print(f"[25_06f] 順番の確認: 21_06a の学習 {TJ.get('utc')} / 25_05 の本番を開いた時刻 {t4}(学習が先のはず。事前登録の push の時刻とも照らす)")
+    if t4 is not None and TJ.get("utc") is not None and TJ["utc"] > t4: stop("[25_06f] STOP: 21_06a の学習が 25_05 の本番より後(事前登録の順番と違う)")
 elif not a.dev:
-    stop(f"[24_06f] STOP: models/{J04.name} が無い(24_05 の本番を先に終える。やり直した時は --ref-suffix を渡す)")
+    stop(f"[25_06f] STOP: models/{J04.name} が無い(25_05 の本番を先に終える。やり直した時は --ref-suffix を渡す)")
 REF_SHA = sha256(REFCSV)
-print(f"[24_06f] SHA-256(事前登録の記録の 6 節と照らす): 学習の記録 {TJ_SHA} / モデル {TJ['model_sha256']} / 学習の行 {TJ['train_rows_sha256']} / 24_05 の CSV {REF_SHA}")
+print(f"[25_06f] SHA-256(事前登録の記録の 9 節と照らす): 学習の記録 {TJ_SHA} / モデル {TJ['model_sha256']} / 学習の行 {TJ['train_rows_sha256']} / 25_05 の CSV {REF_SHA}")
 if not a.dev:                                 # 入力の確認が全て通ってから試験を開く(ここより前の STOP は記録しない)
@@ -635,3 +649,3 @@
 
-# ---------------------------------------------------------------- 9. 記述用: 2014 の pool を足して学び直した版(L3p・L4p。同じ設定。判定には使わない)
+# ---------------------------------------------------------------- 9. 記述用: 2018 の pool を足して学び直した版(L3p・L4p。同じ設定。判定には使わない)
 EVSET = set(int(i) for i in EVAL)
@@ -649,3 +663,3 @@
 MODEL_P.fit(np.concatenate([R26["X"]] + Xp), np.concatenate([R26["y"]] + yp), sample_weight=np.concatenate([R26["w"]] + wp))
-print(f"[24_06f] 記述用の L3p・L4p: 2026 の行 {len(R26['y'])} + 2014 の pool の行 {int(sum(len(v) for v in yp))} で学び直した")
+print(f"[25_06f] 記述用の L3p・L4p: 2026 の行 {len(R26['y'])} + 2018 の pool の行 {int(sum(len(v) for v in yp))} で学び直した")
 
@@ -678,9 +692,9 @@
     except BaseException as ex:
-        stop(f"[24_06f] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
+        stop(f"[25_06f] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
     if (ii + 1) % 10 == 0: print(f"  … {ii + 1}/{len(EVAL)}  ({time.time() - T0:.0f} s)")
-for k in KEYS:                                # 24_05 の CSV(小数 4 桁)と同じ丸めにそろえてから比べる(同点を同点として扱う)
+for k in KEYS:                                # 25_05 の CSV(小数 4 桁)と同じ丸めにそろえてから比べる(同点を同点として扱う)
     E[k] = np.vectorize(lambda v: float(f"{v:.4f}"))(E[k])
 G_SAME = "PASS" if not mism else f"FAIL ({len(mism)})"
-print(f"[24_06f] G-same(ここで計算した C3・C4 が 24_05 の CSV と同じ): {G_SAME}")
-if mism: stop(f"[24_06f] STOP(G-same): 24_05 と同じ計算になっていない(例 {mism[:3]})")
+print(f"[25_06f] G-same(ここで計算した C3・C4 が 25_05 の CSV と同じ): {G_SAME}")
+if mism: stop(f"[25_06f] STOP(G-same): 25_05 と同じ計算になっていない(例 {mism[:3]})")
 for b in BASE:
@@ -724,3 +738,3 @@
 def fp(p): return "—" if p is None else f"{p:.2g}"
-print(f"\n[24_06f] ===== 水平誤差の中央値 km [95% 区間](長野県北部 2014、評価 {NT} 地震{'、dev' if a.dev else ''}) =====")
+print(f"\n[25_06f] ===== 水平誤差の中央値 km [95% 区間](島根県西部 2018、評価 {NT} 地震{'、dev' if a.dev else ''}) =====")
 for k in ["BEST"] + KEYS:
@@ -735,3 +749,3 @@
           f"L が M6r に戻った割合 {d['learned_fallback_frac']:.2f}")
-print(f"\n[24_06f] ===== 事前登録の判定 =====")
+print(f"\n[25_06f] ===== 事前登録の判定 =====")
 for name, h in HYP.items():
@@ -740,4 +754,4 @@
           f"p = {fp(pr['p'])}(基準 {h['alpha']})  差が 0 でない組 {pr['n_nonzero']}  FLOOR={h['floor']}  → {'勝ち' if h['win'] else '勝ちなし'}")
-print(f"\n[24_06f] 判定(事前登録、HL1): {VERDICT}")
-LIMITS_L = ["fourth sequence: Northern Nagano 2014 (mainshock 2014-11-22, 22:08:17.90 JST; JMA catalogue values), never used in ARGUS development; HL1-HL3 and "
+print(f"\n[25_06f] 判定(事前登録、HL1): {VERDICT}")
+LIMITS_L = ["fifth sequence: Western Shimane 2018 (mainshock 2018-04-09, 01:32:30.81 JST; JMA catalogue values), never used in ARGUS development; HL1-HL3 and "
             "the learned ranker were fixed in the 21_06 preregistration and frozen by 21_06a on West Tottori 2026 before this test"] + \
@@ -745,7 +759,7 @@
             "(depth not solved); it is missing (nan) with fewer than 4 common stations or a near-linear station geometry", "the learned ranker (21_06a) was trained on West Tottori 2026 only and frozen before this test; L3p/L4p (retrained with the "
-                     "2014 pool) are descriptive", "24_06f reuses the 24_05 per-event CSV for the physics-only methods and C3/C4, and "
-                     "recomputes C3/C4 to check identity (G-same)", "C3/C4/L3/L4 errors are rounded to 4 decimals (as in the 24_05 CSV) "
+                     "2018 pool) are descriptive", "25_06f reuses the 25_05 per-event CSV for the physics-only methods and C3/C4, and "
+                     "recomputes C3/C4 to check identity (G-same)", "C3/C4/L3/L4 errors are rounded to 4 decimals (as in the 25_05 CSV) "
                      "before comparison so that ties stay ties", "log10_dt_h uses the target's JMA origin time (not known exactly at tau; "
                      "the error is a few seconds against >= 1 h)"]
-print("[24_06f] 限界: " + " / ".join(LIMITS_L))
+print("[25_06f] 限界: " + " / ".join(LIMITS_L))
 
@@ -760,3 +774,3 @@
     return o
-with open(ROOT / f"data/24_06f_per_event{SUF}.csv", "w", newline="") as f:
+with open(ROOT / f"data/25_06f_per_event{SUF}.csv", "w", newline="") as f:
     w = csv.writer(f)
@@ -766,3 +780,3 @@
         w.writerow([OT[ie], f"{MAG[ie]:.1f}"] + [("" if not np.isfinite(E[k][i, jt]) else f"{E[k][i, jt]:.4f}") for k in cols for jt in range(len(TAUS))])
-out = dict(script="24_06f_nagano2014_learned_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"), suffix=SUF,
+out = dict(script="25_06f_shimane2018_learned_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"), suffix=SUF,
            cache=a.cache, cache_sha256=CACHE_SHA, reference_csv=str(REFCSV.relative_to(ROOT)), train_json=a.train_json,
@@ -777,3 +791,3 @@
            limits=LIMITS_L, runtime_s=time.time() - T0)
-json.dump(clean(out), open(ROOT / f"models/24_06f_judgment{SUF}.json", "w"), indent=1)
+json.dump(clean(out), open(ROOT / f"models/25_06f_judgment{SUF}.json", "w"), indent=1)
 
@@ -793,3 +807,3 @@
 ax.set_xticks(x); ax.set_yscale("log"); ax.set_xlabel("Time since the first P pick, tau (s)"); ax.set_ylabel("Median epicentral error (km), 95% bootstrap CI")
-ax.set_title(f"(a) Northern Nagano 2014, {NT} {'DEV' if a.dev else 'test'} events", fontsize=10); ax.grid(alpha=0.3)
+ax.set_title(f"(a) Western Shimane 2018, {NT} {'DEV' if a.dev else 'test'} events", fontsize=10); ax.grid(alpha=0.3)
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, frameon=False, fontsize=8.5)
@@ -805,4 +819,4 @@
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8.5)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_06f_F1_learned_test{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/25_06f_F1_learned_test{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
 if not a.dev: log_open(f"completed: {VERDICT}")
-print(f"[24_06f] 出力: models/24_06f_judgment{SUF}.json, data/24_06f_per_event{SUF}.csv, PDF/24_06f_F1_learned_test{SUF}.pdf  ({time.time() - T0:.0f} s)")
+print(f"[25_06f] 出力: models/25_06f_judgment{SUF}.json, data/25_06f_per_event{SUF}.csv, PDF/25_06f_F1_learned_test{SUF}.pdf  ({time.time() - T0:.0f} s)")
```

## 25_06g_shimane2018_gate_test.py ← 24_06g_nagano2014_gate_test.py

```diff
--- ../nagano/frz/24_06g_nagano2014_gate_test.py	2026-11-15 05:21:00.097264027 +0000
+++ frz/25_06g_shimane2018_gate_test.py	2026-11-17 01:57:17.164207007 +0000
@@ -2,15 +2,14 @@
 # =============================================================================
-# Script : 24_06g_nagano2014_gate_test.py  (v1)
-#          [信頼の切り替え G の試験(1 回だけ): 凍結した G(models/22_gate.pkl)を、手を付けていない長野県北部 2014 の試験の地震に当て、
+# Script : 25_06g_shimane2018_gate_test.py  (v1)
+#          [信頼の切り替え G の試験(1 回だけ): 凍結した G(models/22_gate.pkl)を、手を付けていない島根県西部 2018 の試験の地震に当て、
 #           「物理(C4)と記憶(C1)のどちらを信じるか」を AI が決めると、C4 より大きな外れが減るか(HG1)、固定の規則 R より良いか(HG2)を判定する]
-# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の信頼の切り替えの腕(大阪 22_04 は INCONCLUSIVE だった)
-# 派生元 : 22_04_osaka2018_gate_test.py v1(SHA-256 7a634ca58e08fe759e3d3abac8df629c5fdf7da81ddcffd9d36bee2eceacec24)。
-#          22 GATE FEATURES・22 GATE APPLY の印の間・判定の関数・凍結した G・閾値・HG1〜HG3 の規則は 1 字も変えていない
-#          (写した部分の SHA-256 を、22_04 と同じ凍結の記録の値と照らす)。変えたのは次だけ(DIFF_LOG_24.md):
-#          (1) 入力の既定のキャッシュ(24_05 と同じ R1 の後のもの)、MAIN_UTC・UNTOUCHED_UTC(24_05 と同じ)、限界の文(24_05 と同じ LIMITS)
-#          (2) 比べる相手と順番の確かめを 22_04 の 21_20 の出力から 24_05 の出力に変えた: data/24_05_per_event.csv(--dev は _dev)、
-#              models/24_05_judgment.json(登録した 24_05 v1 の SHA-256・同じキャッシュ・mode = test)、models/24_05_opened.json
-#              (G を凍結した時刻 < 24_05 を開いた時刻)。照らす 24_05 の SHA-256 は FROZEN["script_24_05"](凍結の時に書く)
-#          (3) 出力の名前: models/24_06g_judgment.json / models/24_06g_opened.json / data/24_06g_per_event.csv / PDF/24_06g_F1_gate_nagano.pdf、
-#              表示の [24_06g]、系列の名前
+# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の信頼の切り替えの腕(大阪 22_04 は INCONCLUSIVE だった。長野 24_06g は回していない)
+# 派生元 : 24_06g_nagano2014_gate_test.py v1(SHA-256 5a4aa29a5741e6e76a177199a8580436739b3d75e53e9d61e2e5d42806efeec0。事前登録 24 で凍結)。
+#          22 GATE FEATURES・22 GATE APPLY の印の間・判定の関数・凍結した G・閾値・HG1〜HG3 の規則・--ref-suffix の扱いは 24_06g v1 と
+#          1 字も変えていない(写した部分の SHA-256 を、22_04・24_06g と同じ凍結の記録の値と照らす)。変えたのは次だけ(DIFF_LOG_25.md):
+#          (1) 入力の既定のキャッシュ(25_05 と同じ R1 の後のもの)、MAIN_UTC・UNTOUCHED_UTC(25_05 と同じ)、限界の文(25_05 と同じ LIMITS の書き換え)
+#          (2) 比べる相手の名前: data/25_05_per_event.csv(--dev は _dev)、models/25_05_judgment.json、models/25_05_opened.json。
+#              照らす 25_05 の SHA-256 は FROZEN["script_25_05"](凍結の時に書く。キーの名前も 24 → 25)
+#          (3) 出力の名前: models/25_06g_judgment.json / models/25_06g_opened.json / data/25_06g_per_event.csv / PDF/25_06g_F1_gate_shimane.pdf、
+#              表示の [25_06g]、系列の名前
 #
@@ -20,8 +19,8 @@
 #
-# Usage : (先に 24_05 を本番まで回す)
-#         cd ~/SWIFT && caffeinate -i uv run python src/24_06g_nagano2014_gate_test.py --dev   (動作確認。試験を開かない)
-#         cd ~/SWIFT && caffeinate -i uv run python src/24_06g_nagano2014_gate_test.py         (本番。1 回だけ)
-# 入力  : data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt・models/22_gate.pkl・models/22_02_opened.json・
-#         models/24_05_opened.json・models/24_05_judgment.json・data/24_05_per_event.csv(--dev なら両方 _dev)・(あれば)data/22_01a_rows_wt2026.npz
-# Output: models/24_06g_judgment.json / models/24_06g_opened.json / data/24_06g_per_event.csv / PDF/24_06g_F1_gate_nagano.pdf
+# Usage : (先に 25_05 を本番まで回す)
+#         cd ~/SWIFT && caffeinate -i uv run python src/25_06g_shimane2018_gate_test.py --dev   (動作確認。試験を開かない)
+#         cd ~/SWIFT && caffeinate -i uv run python src/25_06g_shimane2018_gate_test.py         (本番。1 回だけ)
+# 入力  : data/shimane2018_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt・models/22_gate.pkl・models/22_02_opened.json・
+#         models/25_05_opened.json・models/25_05_judgment.json・data/25_05_per_event.csv(--dev なら両方 _dev)・(あれば)data/22_01a_rows_wt2026.npz
+# Output: models/25_06g_judgment.json / models/25_06g_opened.json / data/25_06g_per_event.csv / PDF/25_06g_F1_gate_shimane.pdf
 # =============================================================================
@@ -36,5 +35,5 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--cache", default="data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt", help="24_03(15_01c v3.3 と同じ計算)の長野県北部 2014 の M>=1.5 版に 24_03h の R1 を当てたもの(24_05 と同じ)")
+ap.add_argument("--cache", default="data/shimane2018_processed/tottori_parsed_realpick_shimane2018_m15_r1.pt", help="25_03(15_01c v3.3 と同じ計算)の島根県西部 2018 の M>=1.5 版に 25_03h の R1 を当てたもの(25_05 と同じ)")
 ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(pool の最後の新しい地震 20 個を代わりに使う)")
-ap.add_argument("--ref-suffix", default="", help="24_06g: 比べる相手の 24_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
+ap.add_argument("--ref-suffix", default="", help="25_06g: 比べる相手の 25_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
 a = ap.parse_args()
@@ -59,21 +58,29 @@
 NBOOT, SEED, N_DEV, N_GATE = 2000, 12, 20, 5
-MAIN_UTC = dt.datetime(2014, 11, 22, 13, 8, 17, 900000)   # 24_05 と同じ: 24_00 の表示の 22:08:17.90 JST(± 60 s)
-UNTOUCHED_UTC = (dt.datetime(2014, 11, 20), dt.datetime(2014, 12, 17))     # G-untouched: 24_01 の期間(本震の 2 日前〜24 日後)を含む
-LIMITS = ["fourth sequence: Northern Nagano 2014 (mainshock 2014-11-22, 22:08:17.90 JST, Mj 6.7; JMA catalogue values, see 24_01's JSON), "
+MAIN_UTC = dt.datetime(2018, 4, 8, 16, 32, 30, 810000)   # 25_05 と同じ: 25_00 の表示の 01:32:30.81 JST(± 60 s)
+UNTOUCHED_UTC = (dt.datetime(2018, 4, 6), dt.datetime(2018, 5, 3))     # G-untouched: 25_01 の期間(本震の 2 日前〜24 日後)を含む
+LIMITS = ["fifth sequence: Western Shimane 2018 (mainshock 2018-04-09, 01:32:30.81 JST, Mj 6.1; JMA catalogue values, see 25_01's JSON), "
           "never used in ARGUS development; the hypotheses H1-H3 were fixed on West Tottori 2026 (21_01/21_02), tested on Central Tottori 2016 "
-          "(21_04, with a documented deviation) and Northern Osaka 2018 (21_20, re-registered with amendment 04) and are applied here unchanged",
-          "one fourth sequence only; before this preregistration the catalogue h2014 was opened once by 24_00 to count events "
-          "(counts and the mainshock row only; no location list, waveform or method error was looked at)",
+          "(21_04, with a documented deviation) and Northern Osaka 2018 (21_20, re-registered with amendment 04) and are applied here unchanged; "
+          "the fourth sequence (Northern Nagano 2014, preregistration 24 with the same rules) was stopped by the clock check G-clock2 before "
+          "its test was opened, and its rules (including H4 and H5) are carried over unchanged except G-clock2 condition (d)",
+          "one fifth sequence only; before this preregistration the catalogue h2018 was opened by 25_00 to count events "
+          "(counts and the mainshock row only; no location list, waveform or method error was looked at); h2018 had been opened before "
+          "for Northern Osaka 2018 (21_20a), whose box and period do not include this sequence",
+          "the catalogue-only count of test candidates after rule R1 was 41 in 25_00 (25_00 required at least 40 to select a sequence); "
+          "events without a PhaseNet P in the cache are not evaluated, and fewer than 30 evaluated events give INCONCLUSIVE",
+          "25 of these 41 catalogue test candidates have JMA's automatic-hypocentre flag (A), 15 are K and 1 is k (25_00); the truth and "
+          "past-event locations therefore mix manual and automatic JMA hypocentres; errors by flag are described by 25_09 (no test)",
           "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
-          "set of 50 stations also included non-Hi-net stations, so station types and geometry differ",
+          "set of 50 stations also included non-Hi-net stations, so station types and geometry differ; stations that existed in 2018 but "
+          "are not in the current NIED list cannot be candidates",
           "waveforms were downloaded around catalogue events only and converted to the West Tottori 2026 h5 form (30-s windows, "
-          "per-window per-component z-score, JST epoch; 24_02 also stores the window mean and standard deviation); no filter was applied "
-          "before the z-score (compared in 24_02 G-spec)",
-          "the cache was built by 24_03, whose picking, QC and assembly are identical to 15_01c v3.3; 24_03h then removed every event "
+          "per-window per-component z-score, JST epoch; 25_02 also stores the window mean and standard deviation); no filter was applied "
+          "before the z-score (compared in 25_02 G-spec)",
+          "the cache was built by 25_03, whose picking, QC and assembly are identical to 15_01c v3.3; 25_03h then removed every event "
           "with another catalogue event from 15 s before to 5 s after its origin (rule R1 of 21_20 amendment 04, fixed here before any "
-          "Nagano waveform was opened; it uses origin times and Mj only), which can bias the sample against busy periods",
-          "catalogue: JMA hypocentres from h2014 (whether h2014 is the final stage is to be confirmed); past-event locations are JMA "
+          "Shimane waveform was opened; it uses origin times and Mj only), which can bias the sample against busy periods",
+          "catalogue: JMA hypocentres from h2018 (whether h2018 is the final stage is to be confirmed); past-event locations are JMA "
           "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
-          "the 2014 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
-          "events. Manual and automatic hypocentres can be mixed (per-flag counts in 24_01's JSON)",
+          "the 2018 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
+          "events. Manual and automatic hypocentres can be mixed (per-flag counts in 25_01's JSON)",
           "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); "
@@ -100,2 +107,9 @@
           "offline picks (their records are complete at the time of the target event)",
+          "the clock check G-clock2 condition (d) was redesigned for this preregistration on four earlier sequences only (25_04x, 25_04y, "
+          "25_04z and 25_04v; Shimane was not opened): 5 consecutive events after mainshock + 72 h, median of event medians within 0.5 s; "
+          "it does not check common timing errors that affect only one or two events, or events within 72 h of the mainshock; its "
+          "positive control was set to +1.0 s on 4 consecutive events after +0.6 s could not be met together with the negative control "
+          "(25_04z); a 0.6 s common offset over 4 events is therefore not reliably detected",
+          "if the station-level clock check G-clock2 (c) fails only at stations farther than 80 km, the test proceeds with a fixed label "
+          "(preregistration 25, section 5.3); a constant clock offset at a far station can be missed",
           "H1 (C3 at tau = 2 s) is the primary test; H2, H3 and H4 are secondary at alpha 0.005; H5 (causal picks) uses the H1 rule at "
@@ -113,3 +127,3 @@
 SELF_SHA = sha256(Path(__file__))
-print(f"[24_06g] 本スクリプト(24_06g){VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
+print(f"[25_06g] 本スクリプト(25_06g){VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
       f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")
@@ -118,3 +132,3 @@
 CP = ROOT / a.cache
-if not CP.exists(): raise SystemExit(f"[24_06g] STOP: {a.cache} が無い(ノート 24_nagano2014_colab.ipynb のセル N12 で作った tottori_parsed_realpick_nagano2014_m15_r1.pt を data/nagano2014_processed/ に置く)")
+if not CP.exists(): raise SystemExit(f"[25_06g] STOP: {a.cache} が無い(ノート 25_shimane2018_colab.ipynb のセル N12 で作った tottori_parsed_realpick_shimane2018_m15_r1.pt を data/shimane2018_processed/ に置く)")
 EVS = torch.load(CP, map_location="cpu", weights_only=False)
@@ -123,7 +137,7 @@
     miss = [k for k in need if k not in e]
-    if miss: raise SystemExit(f"[24_06g] STOP: キャッシュの地震に {miss} が無い(24_03・24_03h の出力か確かめる)")
+    if miss: raise SystemExit(f"[25_06g] STOP: キャッシュの地震に {miss} が無い(25_03・25_03h の出力か確かめる)")
 for e in EVS:
     w_ = np.asarray(e["waveforms"])
-    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[24_06g] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
-    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[24_06g] STOP: {e['origin_time']} の波形に NaN か無限大")
+    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[25_06g] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
+    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[25_06g] STOP: {e['origin_time']} の波形に NaN か無限大")
 def to_ns(o):
@@ -135,3 +149,3 @@
     except Exception:
-        raise SystemExit(f"[24_06g] STOP: origin_time {o!r} を時刻として読めない")
+        raise SystemExit(f"[25_06g] STOP: origin_time {o!r} を時刻として読めない")
 OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
@@ -143,4 +157,4 @@
 if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
-    raise SystemExit("[24_06g] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
-if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[24_06g] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
+    raise SystemExit("[25_06g] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
+if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[25_06g] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
 # G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
@@ -151,10 +165,10 @@
 n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
-print(f"[24_06g] 入力: 長野県北部 2014 の M ≥ 1.5 版(R1 の後) {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
+print(f"[25_06g] 入力: 島根県西部 2018 の M ≥ 1.5 版(R1 の後) {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
       f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
-print(f"[24_06g] G-untouched: 期間 2014-11-20〜2014-12-17(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
+print(f"[25_06g] G-untouched: 期間 2018-04-06〜2018-05-03(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
       + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
-if n_out != 0 or n_big != 1: raise SystemExit("[24_06g] STOP(G-untouched): 長野県北部 2014 のキャッシュに見えない(この行を貼って相談)")
+if n_out != 0 or n_big != 1: raise SystemExit("[25_06g] STOP(G-untouched): 島根県西部 2018 のキャッシュに見えない(この行を貼って相談)")
 im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
 if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
-    raise SystemExit(f"[24_06g] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2014-11-22 13:08:17.9 UTC ± 60 s。24_00 の表示の 22:08:17.90 JST)")
+    raise SystemExit(f"[25_06g] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2018-04-08 16:32:30.81 UTC ± 60 s。25_00 の表示の 01:32:30.81 JST)")
 CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
@@ -162,5 +176,5 @@
 if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
-    raise SystemExit("[24_06g] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
-print(f"[24_06g] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
-print(f"[24_06g] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
+    raise SystemExit("[25_06g] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
+print(f"[25_06g] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
+print(f"[25_06g] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
       f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")
@@ -175,3 +189,3 @@
     kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
-    if len(set(kk)) != n: raise SystemExit(f"[24_06g] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
+    if len(set(kk)) != n: raise SystemExit(f"[25_06g] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
 HASP = ~np.isnan(TFIRST)
@@ -187,6 +201,6 @@
 EX, EY = to_xy(SRC[:, 0], SRC[:, 1])
-print(f"[24_06g] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
+print(f"[25_06g] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
 EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
-if len(EVAL) == 0: raise SystemExit("[24_06g] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
-if a.dev: print(f"[24_06g] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
+if len(EVAL) == 0: raise SystemExit("[25_06g] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
+if a.dev: print(f"[25_06g] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                 "(較正にも入っているので値は楽観的)")
@@ -194,5 +208,5 @@
 # ---------------------------------------------------------------- 1 回だけの記録と照合の準備(22_04。重い計算と、開く前に全て済ませる)
-# 24_05 の記録(models/24_05_opened.json)は読むだけで書かない。照合が全て通った後、試験の地震の結果を計算する前に 9 節で「opened」を書く
+# 25_05 の記録(models/25_05_opened.json)は読むだけで書かない。照合が全て通った後、試験の地震の結果を計算する前に 9 節で「opened」を書く
 import re, sys, platform, pickle
-OPEN = ROOT / "models/24_06g_opened.json"
+OPEN = ROOT / "models/25_06g_opened.json"
 SUF = "_dev" if a.dev else ""
@@ -210,3 +224,3 @@
               rows="b57caba76f0d8cca1a5ca952afe17b494897ef76c4ac98cecb63fa8d27c48d59",
-              script_24_05="c10d15fe404309d836fc83fb2dbe1d207fa477d9597900724f487ef965970f9f")   # 22_00 の 7 節(2026-11-02 の凍結)の G の値と、事前登録 24 で凍結する 24_05 v1
+              script_25_05="80309ce7012b89af0c052e225cb66b2e15ee104af247937b63510064f9c11398")   # 22_00 の 7 節(2026-11-02 の凍結)の G の値と、事前登録 25 で凍結する 25_05 v1
 P_CHOOSE_REG, THR_R_REG = 0.5, 10.0                                                         # 22_00 の 1.3・2 節
@@ -218,12 +232,12 @@
 APPLY_SHA = blk("# >>> 22 GATE APPLY BEGIN", "# <<< 22 GATE APPLY END")
-if GATE_SHA != FROZEN["features"]: raise SystemExit(f"[24_06g] STOP: 手がかりの部分の SHA-256 {GATE_SHA[:12]}… が凍結の記録と違う")
-if APPLY_SHA != FROZEN["apply"]: raise SystemExit(f"[24_06g] STOP: 判定に使う部分(22 GATE APPLY)の SHA-256 {APPLY_SHA[:12]}… が凍結の記録と違う")
+if GATE_SHA != FROZEN["features"]: raise SystemExit(f"[25_06g] STOP: 手がかりの部分の SHA-256 {GATE_SHA[:12]}… が凍結の記録と違う")
+if APPLY_SHA != FROZEN["apply"]: raise SystemExit(f"[25_06g] STOP: 判定に使う部分(22 GATE APPLY)の SHA-256 {APPLY_SHA[:12]}… が凍結の記録と違う")
 GBLK = FB[FB.rindex("# >>> 22 GATE FEATURES BEGIN"):FB.rindex("# <<< 22 GATE FEATURES END")]
 leak = re.findall(r"SRC\s*\[|MAG\s*\[|E[XY]\s*\[\s*ie\s*\]|OTNS\s*\[|RES\s*\[|EVS\s*\[|\bOT\s*\[|src_loc|TFIRST\s*\[", GBLK)
-if leak: raise SystemExit(f"[24_06g] STOP(G-leak): 手がかりの部分に正解か目標の地震の値を読む所がある {sorted(set(leak))}")
-print(f"[24_06g] 写した部分の SHA-256: 手がかり {GATE_SHA[:12]}…・判定 {APPLY_SHA[:12]}…(凍結の記録と同じ)  G-leak PASS")
+if leak: raise SystemExit(f"[25_06g] STOP(G-leak): 手がかりの部分に正解か目標の地震の値を読む所がある {sorted(set(leak))}")
+print(f"[25_06g] 写した部分の SHA-256: 手がかり {GATE_SHA[:12]}…・判定 {APPLY_SHA[:12]}…(凍結の記録と同じ)  G-leak PASS")
 MP = ROOT / "models/22_gate.pkl"
-if not MP.exists(): raise SystemExit("[24_06g] STOP: models/22_gate.pkl が無い(22_02 で凍結したもの)")
+if not MP.exists(): raise SystemExit("[25_06g] STOP: models/22_gate.pkl が無い(22_02 で凍結したもの)")
 MODEL_SHA = sha256(MP)
-if MODEL_SHA != FROZEN["gate_pkl"]: raise SystemExit(f"[24_06g] STOP: models/22_gate.pkl の SHA-256 {MODEL_SHA[:12]}… が凍結の記録(358e3daddfc0…)と違う")
+if MODEL_SHA != FROZEN["gate_pkl"]: raise SystemExit(f"[25_06g] STOP: models/22_gate.pkl の SHA-256 {MODEL_SHA[:12]}… が凍結の記録(358e3daddfc0…)と違う")
 with open(MP, "rb") as f: GATE = pickle.load(f)
@@ -231,41 +245,41 @@
         or GATE["p_choose"] != P_CHOOSE_REG or GATE["thr_R_km"] != THR_R_REG):
-    raise SystemExit("[24_06g] STOP: 凍結した G の中の部分の SHA-256・学習の行・p の境目・R のしきい値のどれかが、凍結の記録と違う")
-print(f"[24_06g] 凍結した G: models/22_gate.pkl  SHA-256 {MODEL_SHA[:12]}…(凍結の記録と同じ)  p ≥ {GATE['p_choose']} で C1、R は {GATE['thr_R_km']} km")
-# (b) G は長野を開く前に凍結した(22_02 の最初の completed の時刻 < 24_05 の最初の記録の時刻)
-O22, O20 = ROOT / "models/22_02_opened.json", ROOT / "models/24_05_opened.json"
-if not O22.exists(): raise SystemExit("[24_06g] STOP: models/22_02_opened.json が無い(G を凍結した時刻を確かめられない)")
+    raise SystemExit("[25_06g] STOP: 凍結した G の中の部分の SHA-256・学習の行・p の境目・R のしきい値のどれかが、凍結の記録と違う")
+print(f"[25_06g] 凍結した G: models/22_gate.pkl  SHA-256 {MODEL_SHA[:12]}…(凍結の記録と同じ)  p ≥ {GATE['p_choose']} で C1、R は {GATE['thr_R_km']} km")
+# (b) G は島根を開く前に凍結した(22_02 の最初の completed の時刻 < 25_05 の最初の記録の時刻)
+O22, O20 = ROOT / "models/22_02_opened.json", ROOT / "models/25_05_opened.json"
+if not O22.exists(): raise SystemExit("[25_06g] STOP: models/22_02_opened.json が無い(G を凍結した時刻を確かめられない)")
 c22 = [r for r in json.load(open(O22)) if str(r.get("status", "")).startswith("completed") and r.get("suffix", "") == ""]
-if not c22: raise SystemExit("[24_06g] STOP: models/22_02_opened.json に最初の本番の completed が無い")
+if not c22: raise SystemExit("[25_06g] STOP: models/22_02_opened.json に最初の本番の completed が無い")
 T_FREEZE = c22[0]["utc"]
-# (c) 比べる相手: 24_05 の正式な結果(--ref-suffix。既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC> を指定する)
+# (c) 比べる相手: 25_05 の正式な結果(--ref-suffix。既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC> を指定する)
 if a.dev:
-    REFCSV, J20P = ROOT / "data/24_05_per_event_dev.csv", ROOT / "models/24_05_judgment_dev.json"
+    REFCSV, J20P = ROOT / "data/25_05_per_event_dev.csv", ROOT / "models/25_05_judgment_dev.json"
 else:
-    REFCSV, J20P = ROOT / f"data/24_05_per_event{a.ref_suffix}.csv", ROOT / f"models/24_05_judgment{a.ref_suffix}.json"
-if not J20P.exists(): raise SystemExit(f"[24_06g] STOP: {J20P.relative_to(ROOT)} が無い(先に 24_05{' --dev' if a.dev else ''} を回す)")
+    REFCSV, J20P = ROOT / f"data/25_05_per_event{a.ref_suffix}.csv", ROOT / f"models/25_05_judgment{a.ref_suffix}.json"
+if not J20P.exists(): raise SystemExit(f"[25_06g] STOP: {J20P.relative_to(ROOT)} が無い(先に 25_05{' --dev' if a.dev else ''} を回す)")
 j20 = json.load(open(J20P))
-if j20.get("script_sha256") != FROZEN["script_24_05"]: raise SystemExit(f"[24_06g] STOP: 24_05 の結果が、登録した 24_05 v1 のスクリプト(SHA-256 {FROZEN['script_24_05'][:12]}…)のものでない")
-if j20.get("cache_sha256") != CACHE_SHA: raise SystemExit("[24_06g] STOP: キャッシュの SHA-256 が 24_05 の結果と違う")
+if j20.get("script_sha256") != FROZEN["script_25_05"]: raise SystemExit(f"[25_06g] STOP: 25_05 の結果が、登録した 25_05 v1 のスクリプト(SHA-256 {FROZEN['script_25_05'][:12]}…)のものでない")
+if j20.get("cache_sha256") != CACHE_SHA: raise SystemExit("[25_06g] STOP: キャッシュの SHA-256 が 25_05 の結果と違う")
 if not a.dev:
-    if not O20.exists(): raise SystemExit("[24_06g] STOP: models/24_05_opened.json が無い")
+    if not O20.exists(): raise SystemExit("[25_06g] STOP: models/25_05_opened.json が無い")
     r20 = json.load(open(O20))
-    if not (T_FREEZE < r20[0]["utc"]): raise SystemExit(f"[24_06g] STOP: G の凍結({T_FREEZE})が 24_05 を開いた時刻({r20[0]['utc']})より後")
+    if not (T_FREEZE < r20[0]["utc"]): raise SystemExit(f"[25_06g] STOP: G の凍結({T_FREEZE})が 25_05 を開いた時刻({r20[0]['utc']})より後")
     c20 = [r for r in r20 if str(r.get("status", "")).startswith("completed")]
     if not c20 or c20[0].get("suffix", "") != a.ref_suffix or j20.get("suffix", "") != a.ref_suffix:
-        raise SystemExit(f"[24_06g] STOP: --ref-suffix '{a.ref_suffix}' が、models/24_05_opened.json で最初に completed になった 24_05 の実行と違う")
-    print(f"[24_06g] 24_05 の正式な結果: suffix '{a.ref_suffix}'(最初の completed)・スクリプトとキャッシュの SHA-256 が同じ  G の凍結 {T_FREEZE} < 24_05 を開いた時刻 {r20[0]['utc']}")
+        raise SystemExit(f"[25_06g] STOP: --ref-suffix '{a.ref_suffix}' が、models/25_05_opened.json で最初に completed になった 25_05 の実行と違う")
+    print(f"[25_06g] 25_05 の正式な結果: suffix '{a.ref_suffix}'(最初の completed)・スクリプトとキャッシュの SHA-256 が同じ  G の凍結 {T_FREEZE} < 25_05 を開いた時刻 {r20[0]['utc']}")
     if j20.get("verdict") == "INCONCLUSIVE" and int(j20.get("n_evaluated", 0)) < MIN_TEST:
-        JP0 = ROOT / "models/24_06g_judgment.json"
-        if JP0.exists(): raise SystemExit("[24_06g] STOP: models/24_06g_judgment.json が既にある")
-        json.dump(dict(script="24_06g_nagano2014_gate_test.py", version=VERSION, script_sha256=SELF_SHA, mode="test", sequence="Northern Nagano 2014",
-                       verdict="INCONCLUSIVE", reason=f"24_05 evaluated {j20.get('n_evaluated')} < {MIN_TEST} test events; 24_06g was not opened",
+        JP0 = ROOT / "models/25_06g_judgment.json"
+        if JP0.exists(): raise SystemExit("[25_06g] STOP: models/25_06g_judgment.json が既にある")
+        json.dump(dict(script="25_06g_shimane2018_gate_test.py", version=VERSION, script_sha256=SELF_SHA, mode="test", sequence="Western Shimane 2018",
+                       verdict="INCONCLUSIVE", reason=f"25_05 evaluated {j20.get('n_evaluated')} < {MIN_TEST} test events; 25_06g was not opened",
                        ref_judgment=str(J20P.relative_to(ROOT)), utc=utcnow()), open(JP0, "w"), indent=1)
-        print(f"[24_06g] 判定: INCONCLUSIVE(24_05 の評価できる地震 {j20.get('n_evaluated')} < {MIN_TEST}。24_06g は開かない)  記録: models/24_06g_judgment.json")
+        print(f"[25_06g] 判定: INCONCLUSIVE(25_05 の評価できる地震 {j20.get('n_evaluated')} < {MIN_TEST}。25_06g は開かない)  記録: models/25_06g_judgment.json")
         raise SystemExit(0)
-    if j20.get("mode") != "test": raise SystemExit("[24_06g] STOP: 24_05 の結果が本番(mode = test)でない")
-if not REFCSV.exists(): raise SystemExit(f"[24_06g] STOP: {REFCSV.relative_to(ROOT)} が無い")
+    if j20.get("mode") != "test": raise SystemExit("[25_06g] STOP: 25_05 の結果が本番(mode = test)でない")
+if not REFCSV.exists(): raise SystemExit(f"[25_06g] STOP: {REFCSV.relative_to(ROOT)} が無い")
 ref = {r["origin_time"]: r for r in csv.DictReader(open(REFCSV))}
 if sorted(ref) != sorted(OT[ie] for ie in EVAL):
-    raise SystemExit(f"[24_06g] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
-if not a.dev and int(j20.get("n_evaluated", -1)) != len(EVAL): raise SystemExit("[24_06g] STOP: 24_05 の評価の地震の数が、ここで作った試験の地震の数と違う")
+    raise SystemExit(f"[25_06g] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
+if not a.dev and int(j20.get("n_evaluated", -1)) != len(EVAL): raise SystemExit("[25_06g] STOP: 25_05 の評価の地震の数が、ここで作った試験の地震の数と違う")
 TL4 = [f"{t:g}" for t in TAUS]
@@ -273,5 +287,5 @@
 miss_cols = [f"{m}_err_t{t}" for m in CHK for t in TL4 if f"{m}_err_t{t}" not in next(iter(ref.values()))]
-if miss_cols: raise SystemExit(f"[24_06g] STOP(G-same): {REFCSV.name} に照合する列が無い {miss_cols[:4]}")
+if miss_cols: raise SystemExit(f"[25_06g] STOP(G-same): {REFCSV.name} に照合する列が無い {miss_cols[:4]}")
 REF_SHA = sha256(REFCSV)
-print(f"[24_06g] 比べる相手: {REFCSV.relative_to(ROOT)}(SHA-256 {REF_SHA[:12]}…)  {len(EVAL)} 地震 × 4 時点、C1・C3・C4・M6r")
+print(f"[25_06g] 比べる相手: {REFCSV.relative_to(ROOT)}(SHA-256 {REF_SHA[:12]}…)  {len(EVAL)} 地震 × 4 時点、C1・C3・C4・M6r")
 # (d) 学習の行(手がかりの範囲の記述用。判定には使わない)
@@ -279,10 +293,10 @@
 if TRN.exists():
-    if sha256(TRN) != FROZEN["rows"]: raise SystemExit("[24_06g] STOP: data/22_01a_rows_wt2026.npz の SHA-256 が凍結の記録と違う")
+    if sha256(TRN) != FROZEN["rows"]: raise SystemExit("[25_06g] STOP: data/22_01a_rows_wt2026.npz の SHA-256 が凍結の記録と違う")
     _d = np.load(TRN, allow_pickle=False); TRX = _d["X"][_d["fb"] == 0]
 else:
-    print("[24_06g] 注意: data/22_01a_rows_wt2026.npz が無いので、手がかりの範囲の記述を飛ばす(判定には使わない)")
-if not a.dev and (OPEN.exists() or (ROOT / "models/24_06g_judgment.json").exists()):
+    print("[25_06g] 注意: data/22_01a_rows_wt2026.npz が無いので、手がかりの範囲の記述を飛ばす(判定には使わない)")
+if not a.dev and (OPEN.exists() or (ROOT / "models/25_06g_judgment.json").exists()):
     SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
-    print(f"[24_06g] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない。扱いは 22_00 の 3 節)")
-print("[24_06g] 照合の準備は全て通った(まだ開いていない。この後に速度・格子を作り、試験の地震の前に opened を書く)")
+    print(f"[25_06g] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない。扱いは 22_00 の 3 節)")
+print("[25_06g] 照合の準備は全て通った(まだ開いていない。この後に速度・格子を作り、試験の地震の前に opened を書く)")
 
@@ -351,3 +365,3 @@
 LAP_B = float(np.median(np.abs(r1)) / np.log(2.0))
-print(f"[24_06g] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
+print(f"[25_06g] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
       f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")
@@ -362,3 +376,3 @@
 XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
-print(f"[24_06g] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
+print(f"[25_06g] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
       f"  固定の深さ {ZDEF:.1f} km")
@@ -398,3 +412,3 @@
 lls = {h: loo_ll(h) for h in HS}; KDE_H = max(lls, key=lls.get)
-print(f"[24_06g] KDE の帯域(pool の一つ抜き): {KDE_H} km")
+print(f"[25_06g] KDE の帯域(pool の一つ抜き): {KDE_H} km")
 def log_prior(nodes, mem):
@@ -426,3 +440,3 @@
     lib = np.where((OTNS <= OTNS[ie] - int(buffer_h * 3600e9)) & HASP)[0]
-    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[24_06g] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
+    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[25_06g] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
     return lib
@@ -502,3 +516,3 @@
     top = lib[np.argsort(-S, kind="stable")[:min(k, pos)]]
-    if ie is not None and ie in top: stop("[24_06g] STOP: 自分自身が似た地震の上位に入っている")
+    if ie is not None and ie in top: stop("[25_06g] STOP: 自分自身が似た地震の上位に入っている")
     out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
@@ -587,3 +601,3 @@
 
-# ---------------------------------------------------------------- 9. 試験の地震 × 4 時点(24_05 と同じ呼び方)+ G-same + 手がかり
+# ---------------------------------------------------------------- 9. 試験の地震 × 4 時点(25_05 と同じ呼び方)+ G-same + 手がかり
 METH = ["M6r", "C1", "C2", "C3", "C4"]
@@ -608,3 +622,3 @@
             if (v == "") != (not np.isfinite(mine)) or (v != "" and abs(mine - float(v)) > 6e-5): bad.append((TL4[jt], m, v, f"{mine:.5f}"))
-        if bad: stop(f"[24_06g] STOP(G-same): {OT[ie]} で 24_05 と同じ計算になっていない(τ, 方法, CSV, ここ: {bad[:3]})。この行を貼って相談")
+        if bad: stop(f"[25_06g] STOP(G-same): {OT[ie]} で 25_05 と同じ計算になっていない(τ, 方法, CSV, ここ: {bad[:3]})。この行を貼って相談")
         FBK[ii, jt] = int(o["fb"]); NI[ii, jt] = ni; NPOS[ii, jt] = int((S > 0).sum())
@@ -614,5 +628,5 @@
         print(f"  … {ii + 1}/{len(EVAL)} 地震({el:.0f} s、残りの目安 {el / (ii + 1) * (len(EVAL) - ii - 1) / 60:.0f} 分)", flush=True)
-print(f"[24_06g] G-same({'dev の評価' if a.dev else '試験'}の地震 {len(EVAL)} 個 × 4 時点で、C1・C3・C4・M6r の誤差が 24_05 の CSV と 6e-5 km 以内): PASS")
-for m in METH: ERR[m] = np.round(ERR[m], 4)          # 22_01a・24_05 の CSV と同じ小数 4 桁(同点を同点として扱う)
-if not np.all(np.isfinite(ERR["C4"])): stop("[24_06g] STOP: C4 の誤差が無い地震がある")
+print(f"[25_06g] G-same({'dev の評価' if a.dev else '試験'}の地震 {len(EVAL)} 個 × 4 時点で、C1・C3・C4・M6r の誤差が 25_05 の CSV と 6e-5 km 以内): PASS")
+for m in METH: ERR[m] = np.round(ERR[m], 4)          # 22_01a・25_05 の CSV と同じ小数 4 桁(同点を同点として扱う)
+if not np.all(np.isfinite(ERR["C4"])): stop("[25_06g] STOP: C4 の誤差が無い地震がある")
 
@@ -625,3 +639,3 @@
 except SystemExit as ex:
-    stop(f"[24_06g] STOP(判定の部分): {ex}")
+    stop(f"[25_06g] STOP(判定の部分): {ex}")
 EG, ERr, CHG, SWR, PG = (v.reshape(NEV, NT) for v in (eG, eR, chG, swR, pG))
@@ -641,3 +655,3 @@
 def fp(p): return "—" if p is None else f"{p:.3g}"
-print(f"\n[24_06g] ===== 判定(τ = 2 s、{'dev の評価' if a.dev else '長野県北部 2014 の試験'}の {NEV} 地震。C1 が無い地震 {int(FBK[:, jm].sum())} も G = R = C4 として数える) =====")
+print(f"\n[25_06g] ===== 判定(τ = 2 s、{'dev の評価' if a.dev else '島根県西部 2018 の試験'}の {NEV} 地震。C1 が無い地震 {int(FBK[:, jm].sum())} も G = R = C4 として数える) =====")
 print(f"  HG1(G 対 C4、10 km 超): C4 だけ外れ {b_}・G だけ外れ {c_}(食い違う対 {b_ + c_}、基準 {MIN_DISC} 以上)  片側の正確な McNemar p = {fp(p1)}"
@@ -690,3 +704,3 @@
 # ---------------------------------------------------------------- 13. 出力(JSON・CSV を図より先に)
-with open(ROOT / f"data/24_06g_per_event{SUF}.csv", "w", newline="") as f:
+with open(ROOT / f"data/25_06g_per_event{SUF}.csv", "w", newline="") as f:
     w = csv.writer(f)
@@ -706,3 +720,3 @@
        "test errors are rounded to 4 decimals (numpy round) before HG1/HG2, as were the training errors",
-       "the gate G was trained on one sequence (West Tottori 2026) and frozen before Northern Osaka 2018 and Northern Nagano 2014 were opened (22_00 section 7)",
+       "the gate G was trained on one sequence (West Tottori 2026) and frozen before Northern Osaka 2018 and Western Shimane 2018 were opened (22_00 section 7)",
        "truth and past-event locations are JMA hypocentres; C1 can only return locations of past events, so neither C1 nor G can answer "
@@ -711,6 +725,6 @@
        "feature 9 (P residual at the C4 epicentre) is missing with fewer than 3 P picks and is then filled with the training median",
-       "C1 and C4 errors are rounded to 4 decimals before comparison (as in the 24_05 CSV) so that ties stay ties",
-       "all 24_05 limitations apply (listed below, copied from 24_05 v1)"] + LIMITS
-JUDG = dict(script="24_06g_nagano2014_gate_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
-            sequence="Northern Nagano 2014", suffix=SUF, cache=a.cache, cache_sha256=CACHE_SHA, gate_pkl_sha256=MODEL_SHA,
+       "C1 and C4 errors are rounded to 4 decimals before comparison (as in the 25_05 CSV) so that ties stay ties",
+       "all 25_05 limitations apply (listed below, copied from 25_05 v1)"] + LIMITS
+JUDG = dict(script="25_06g_shimane2018_gate_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
+            sequence="Western Shimane 2018", suffix=SUF, cache=a.cache, cache_sha256=CACHE_SHA, gate_pkl_sha256=MODEL_SHA,
             gate_feature_block_sha256=GATE_SHA, gate_apply_block_sha256=APPLY_SHA, ref_csv=str(REFCSV.relative_to(ROOT)),
@@ -729,5 +743,5 @@
             utc=utcnow(), runtime_s=time.time() - T0)
-JP = ROOT / f"models/24_06g_judgment{SUF}.json"
+JP = ROOT / f"models/25_06g_judgment{SUF}.json"
 json.dump(JUDG, open(JP, "w"), indent=1, ensure_ascii=False)
-print(f"[24_06g] 出力: {JP.relative_to(ROOT)}  SHA-256 {sha256(JP)}  /  data/24_06g_per_event{SUF}.csv")
+print(f"[25_06g] 出力: {JP.relative_to(ROOT)}  SHA-256 {sha256(JP)}  /  data/25_06g_per_event{SUF}.csv")
 if not a.dev: log_open(f"completed: verdict {VERDICT}")
@@ -751,3 +765,3 @@
 ax.set_xlabel("Time since the first P pick, tau"); ax.set_ylabel("Events with error > 10 km (%)"); ax.grid(alpha=0.3, axis="y")
-ax.set_title(f"(a) Northern Nagano 2014{' (dev)' if a.dev else ''}, {NEV} events (bar labels in %)", fontsize=9.5)
+ax.set_title(f"(a) Western Shimane 2018{' (dev)' if a.dev else ''}, {NEV} events (bar labels in %)", fontsize=9.5)
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8)
@@ -767,4 +781,4 @@
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_06g_F1_gate_nagano{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"[24_06g] 図: PDF/24_06g_F1_gate_nagano{SUF}.pdf  ({time.time() - T0:.0f} s)")
-print("[24_06g] 次: この出力と図を貼る" + ("" if a.dev else "(判定に使うのは、この最初の本番の結果)"))
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/25_06g_F1_gate_shimane{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"[25_06g] 図: PDF/25_06g_F1_gate_shimane{SUF}.pdf  ({time.time() - T0:.0f} s)")
+print("[25_06g] 次: この出力と図を貼る" + ("" if a.dev else "(判定に使うのは、この最初の本番の結果)"))
```

## 24_07_causal_picks.py ← 24_07_causal_picks.py

```diff
(差分なし。1 字も同じ)
```

## 25_08_shimane2018_intensity_descriptive.py ← 24_08_nagano2014_intensity_descriptive.py

```diff
--- ../nagano/frz/24_08_nagano2014_intensity_descriptive.py	2026-11-15 05:21:00.097533022 +0000
+++ frz/25_08_shimane2018_intensity_descriptive.py	2026-11-17 01:57:17.164507381 +0000
@@ -2,18 +2,14 @@
 # =============================================================================
-# Script : 24_08_nagano2014_intensity_descriptive.py  (v1)
-#          [H6(記述。判定に使わない): 長野県北部 2014 の試験の地震で、震央の誤差が揺れ(計測震度)の予測をどれだけ変えるかを、
+# Script : 25_08_shimane2018_intensity_descriptive.py  (v1)
+#          [H6(記述。判定に使わない): 島根県西部 2018 の試験の地震で、震央の誤差が揺れ(計測震度)の予測をどれだけ変えるかを、
 #           21_10 と同じ距離減衰式・同じ換算で計算する。BEST・C3・C4(オフラインの検測)と、τ までの検測の BEST・C3 を並べる]
-# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の記述。「km 未満の改善に実用上の意味はあるか」への答えの材料
-# 派生元 : 21_10_gmpe_location_error.py v2(SHA-256 de9cbf5933bf75e58ffcb7452db528e39963969ec8688d4d23f2104ca914c764)。
-#          予測震度の差の計算(gdist・dI・方位 5° おき・観測点の震央距離 3・5・10・20・40・80 km・式・係数・換算 I = 2.54 + 1.82 log10 PGV・
-#          階級が変わる確率の上限・σ = 0.23)は 21_10 と 1 字も変えていない。変えたのは入力と出力だけ(DIFF_LOG_24.md):
-#          入力 = 24_05 の本番の data/24_05_per_event.csv と models/24_05_judgment.json(--dev では _dev)。方法 = BEST(H1 と同じ選び方)・
-#          C3・C4、と τ までの検測の BEST・C3(24_05 の causal の列)。密な網だけ(間引いた網は無い)。
-#          出力 = models/24_08_intensity.json・PDF/24_08_F1_intensity_change.pdf(と .png)。図は 1 段(主の式)× τ 2 つ。
-#          入力の確かめ: 24_05 の結果が、事前登録 24 で凍結した 24_05 v1(SHA_2405)のものであること。24_05 を事前登録 24 の 6 節の
-#          機械的な中断で 1 回やり直した時だけ --ref-suffix _rerun_<UTC> を渡す(24_06g と同じ: models/24_05_opened.json で最初に
-#          completed になった実行と一致すること)。24_05 が INCONCLUSIVE なら CSV が無いので、その旨を表示して止める。
-#          24_05 の H5 が NOT-EVALUATED なら、τ までの検測の行は作らない(オフラインの BEST・C3・C4 だけ)。
+# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の記述。「km 未満の改善に実用上の意味はあるか」への答えの材料
+# 派生元 : 24_08_nagano2014_intensity_descriptive.py v1(SHA-256 80391a29309da7a8b7b32821d8c4076ffc1e0e56ec85e6cf2c8ed498ee2b5eb6。事前登録 24 で凍結。
+#          = 21_10 v2 と同じ計算を 24_05 の出力に当てたもの。長野では回していない)。
+#          予測震度の差の計算・方法・図・--ref-suffix の扱い・INCONCLUSIVE と H5 が NOT-EVALUATED の時の扱いは 24_08 v1 と 1 字も変えていない。
+#          変えたのは次だけ(DIFF_LOG_25.md): 入力 = 25_05 の data/25_05_per_event.csv と models/25_05_judgment.json(--dev では _dev)、
+#          照らす 25_05 の SHA-256 は SHA_2505(凍結の時に書く)、出力 = models/25_08_intensity.json・PDF/25_08_F1_intensity_change.pdf(と .png)、
+#          表示の [25_08]、図の題の系列の名前、事前登録の番号(24 → 25)。
 #
-# なぜ検定にしないか(事前登録 24 の 2 節): 同じ地震(同じ深さ)なら |ΔI| は震央の誤差の単調な関数なので、「C4 は BEST より |ΔI| が
+# なぜ検定にしないか(事前登録 25 の 2 節。24 と同じ): 同じ地震(同じ深さ)なら |ΔI| は震央の誤差の単調な関数なので、「C4 は BEST より |ΔI| が
 #   小さい」の検定は H2 と地震ごとの勝ち負けの向きが同じになり、新しい証拠にならない。大きさを σ ≈ 0.42(震度)と並べて記述する。
@@ -22,4 +18,4 @@
 #
-# Usage : cd ~/SWIFT && uv run python src/24_08_nagano2014_intensity_descriptive.py        (24_05 の本番の後)
-#         cd ~/SWIFT && uv run python src/24_08_nagano2014_intensity_descriptive.py --dev  (24_05 の dev の後。配管の確かめ)
+# Usage : cd ~/SWIFT && uv run python src/25_08_shimane2018_intensity_descriptive.py        (25_05 の本番の後)
+#         cd ~/SWIFT && uv run python src/25_08_shimane2018_intensity_descriptive.py --dev  (25_05 の dev の後。配管の確かめ)
 # 文献  : 21_10 と同じ(司・翠川 1999、Si & Midorikawa 2000、翠川ほか 1999、Hayashida & Tajima 2007)
@@ -30,6 +26,6 @@
 ROOT = Path(__file__).resolve().parent.parent
-_ap = argparse.ArgumentParser(); _ap.add_argument("--dev", action="store_true", help="24_05 の dev の出力で回す(配管の確かめ)")
-_ap.add_argument("--ref-suffix", default="", help="24_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
+_ap = argparse.ArgumentParser(); _ap.add_argument("--dev", action="store_true", help="25_05 の dev の出力で回す(配管の確かめ)")
+_ap.add_argument("--ref-suffix", default="", help="25_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
 _A = _ap.parse_args(); DEV = _A.dev
-SHA_2405 = "c10d15fe404309d836fc83fb2dbe1d207fa477d9597900724f487ef965970f9f"                          # 事前登録 24 で凍結した 24_05 v1 の SHA-256
+SHA_2505 = "80309ce7012b89af0c052e225cb66b2e15ee104af247937b63510064f9c11398"                          # 事前登録 25 で凍結する 25_05 v1 の SHA-256
 for d in ("models", "PDF"): (ROOT / d).mkdir(exist_ok=True)
@@ -41,3 +37,3 @@
 SELF_SHA = sha256(Path(__file__))
-print(f"[24_08] 本スクリプト v1 SHA-256 {SELF_SHA[:12]}…")
+print(f"[25_08] 本スクリプト v1 SHA-256 {SELF_SHA[:12]}…")
 DIST = [3.0, 5.0, 10.0, 20.0, 40.0, 80.0]; AZ = np.radians(np.arange(0, 360, 5))
@@ -62,24 +58,24 @@
 def col(rows, k):
-    if rows and k not in rows[0]: raise SystemExit(f"[24_08] STOP: 列 {k} が無い")
+    if rows and k not in rows[0]: raise SystemExit(f"[25_08] STOP: 列 {k} が無い")
     return np.array([float(r[k]) if r[k] not in ("", None) else np.nan for r in rows])
-# ---- 24_08: 入力は 24_05 の本番の CSV と JSON だけ(長野県北部 2014、密な網。間引いた網は無い)
+# ---- 25_08: 入力は 25_05 の本番の CSV と JSON だけ(島根県西部 2018、密な網。間引いた網は無い)
 SFX = "_dev" if DEV else ""
 RSFX = "_dev" if DEV else _A.ref_suffix
-p5, j5 = ROOT / f"data/24_05_per_event{RSFX}.csv", ROOT / f"models/24_05_judgment{RSFX}.json"
-if not j5.exists(): raise SystemExit(f"[24_08] STOP: {j5.relative_to(ROOT)} が無い(24_05 の後に回す。やり直した時は --ref-suffix を渡す)")
+p5, j5 = ROOT / f"data/25_05_per_event{RSFX}.csv", ROOT / f"models/25_05_judgment{RSFX}.json"
+if not j5.exists(): raise SystemExit(f"[25_08] STOP: {j5.relative_to(ROOT)} が無い(25_05 の後に回す。やり直した時は --ref-suffix を渡す)")
 J5 = json.load(open(j5))
 if J5.get("verdict") == "INCONCLUSIVE":
-    raise SystemExit("[24_08] STOP: 24_05 の判定が INCONCLUSIVE(評価できる試験の地震が 30 未満)で CSV が無いため、H6 は計算しない(事前登録 24 の 8 節)")
-if not p5.exists(): raise SystemExit(f"[24_08] STOP: {p5.relative_to(ROOT)} が無い(24_05 の後に回す)")
-if J5.get("script_sha256") != SHA_2405: raise SystemExit(f"[24_08] STOP: 24_05 の結果が、凍結した 24_05 v1(SHA-256 {SHA_2405[:12]}…)のものでない")
+    raise SystemExit("[25_08] STOP: 25_05 の判定が INCONCLUSIVE(評価できる試験の地震が 30 未満)で CSV が無いため、H6 は計算しない(事前登録 25 の 8 節)")
+if not p5.exists(): raise SystemExit(f"[25_08] STOP: {p5.relative_to(ROOT)} が無い(25_05 の後に回す)")
+if J5.get("script_sha256") != SHA_2505: raise SystemExit(f"[25_08] STOP: 25_05 の結果が、凍結した 25_05 v1(SHA-256 {SHA_2505[:12]}…)のものでない")
 if not DEV:
-    _O = ROOT / "models/24_05_opened.json"
+    _O = ROOT / "models/25_05_opened.json"
     _c = [r for r in (json.load(open(_O)) if _O.exists() else []) if str(r.get("status", "")).startswith("completed")]
     if not _c or _c[0].get("suffix", "") != RSFX or J5.get("suffix", "") != RSFX:
-        raise SystemExit(f"[24_08] STOP: --ref-suffix '{RSFX}' が、models/24_05_opened.json で最初に completed になった 24_05 の実行と違う")
+        raise SystemExit(f"[25_08] STOP: --ref-suffix '{RSFX}' が、models/25_05_opened.json で最初に completed になった 25_05 の実行と違う")
 rows5 = load(p5)
 H5_OK = bool(J5.get("causal", {}).get("evaluated", False))
-if len(rows5) != int(J5["n_evaluated"]): raise SystemExit(f"[24_08] STOP: CSV の行の数 {len(rows5)} が n_evaluated {J5['n_evaluated']} と違う")
-print(f"[24_08] 入力: {p5.name}(SHA-256 {sha256(p5)[:12]}…)  {len(rows5)} 地震  24_05 の判定 {J5.get('verdict')}  24_05 の SHA-256 {str(J5.get('script_sha256'))[:12]}…")
-# 方法: BEST(H1 と同じ選び方: per_tau[τ]["C3"]["best"])・C3・C4(オフラインの検測)と、τ までの検測の BEST・C3(24_05 の causal)
+if len(rows5) != int(J5["n_evaluated"]): raise SystemExit(f"[25_08] STOP: CSV の行の数 {len(rows5)} が n_evaluated {J5['n_evaluated']} と違う")
+print(f"[25_08] 入力: {p5.name}(SHA-256 {sha256(p5)[:12]}…)  {len(rows5)} 地震  25_05 の判定 {J5.get('verdict')}  25_05 の SHA-256 {str(J5.get('script_sha256'))[:12]}…")
+# 方法: BEST(H1 と同じ選び方: per_tau[τ]["C3"]["best"])・C3・C4(オフラインの検測)と、τ までの検測の BEST・C3(25_05 の causal)
 METHODS = {}
@@ -91,5 +87,5 @@
         METHODS[t] += [("BEST, causal picks", f"{bc}_causal_err_t{t}", bc), ("C3, causal picks", f"C3_causal_err_t{t}", "C3")]
-if not H5_OK: print("[24_08] 24_05 の H5 は NOT-EVALUATED: τ までの検測の行は作らない")
+if not H5_OK: print("[25_08] 25_05 の H5 は NOT-EVALUATED: τ までの検測の行は作らない")
 hh_all = col(rows5, "depth_km")
-OUT = {"Northern Nagano 2014 (24_05)": {}}
+OUT = {"Western Shimane 2018 (25_05)": {}}
 for t in TAUS:
@@ -106,4 +102,4 @@
                                       class_change_prob_upper=float(np.mean(np.minimum(X / CLASS_W, 1.0)))))
-        OUT["Northern Nagano 2014 (24_05)"][key] = o
-print(f"\n[24_08] ===== 予測震度の差 |ΔI|(主の式。地震ごとの方位平均の中央値 / 方位最大の中央値 / 方位最大の最大 / 階級が変わる確率の上限) =====")
+        OUT["Western Shimane 2018 (25_05)"][key] = o
+print(f"\n[25_08] ===== 予測震度の差 |ΔI|(主の式。地震ごとの方位平均の中央値 / 方位最大の中央値 / 方位最大の最大 / 階級が変わる確率の上限) =====")
 print(f"  目安: 距離減衰式自体のばらつき σ = {SIGMA_LOG}(log10 PGV)= 震度で約 {SLOPE * SIGMA_LOG:.2f}")
@@ -117,3 +113,3 @@
         print("      " + "  ".join(f"{r['site_epi_km']:g} km {r['median_azmean_absdI']:.3f}/{r['median_azmax_absdI']:.3f}/{r['max_azmax_absdI']:.2f}/{r['class_change_prob_upper']:.3f}" for r in rs))
-print("[24_08] 限界: " + " / ".join(LIMITS))
+print("[25_08] 限界: " + " / ".join(LIMITS))
 import matplotlib
@@ -148,8 +144,8 @@
 fig.legend(handles=hs, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.0), fontsize=10)
-fig.suptitle("Northern Nagano 2014" + (" (DEV)" if DEV else "") + ": change in predicted JMA intensity caused by the epicentral error\n"
+fig.suptitle("Western Shimane 2018" + (" (DEV)" if DEV else "") + ": change in predicted JMA intensity caused by the epicentral error\n"
              "(Si & Midorikawa 1999 PGV, equivalent-hypocentral-distance form, point source; I = 2.54 + 1.82 log10 PGV)", y=0.995, fontsize=11)
 fig.tight_layout(rect=(0, 0.12, 1, 0.93))
-fig.savefig(ROOT / f"PDF/24_08_F1_intensity_change{SFX}.pdf", bbox_inches="tight"); fig.savefig(ROOT / f"PDF/24_08_F1_intensity_change{SFX}.png", dpi=200, bbox_inches="tight"); plt.close(fig)
-json.dump(dict(script="24_08_nagano2014_intensity_descriptive.py", script_sha256=SELF_SHA, utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
-               inputs=dict(csv=p5.name, csv_sha256=sha256(p5), judgment=j5.name, judgment_sha256=sha256(j5), script_24_05_sha256=J5.get("script_sha256"),
+fig.savefig(ROOT / f"PDF/25_08_F1_intensity_change{SFX}.pdf", bbox_inches="tight"); fig.savefig(ROOT / f"PDF/25_08_F1_intensity_change{SFX}.png", dpi=200, bbox_inches="tight"); plt.close(fig)
+json.dump(dict(script="25_08_shimane2018_intensity_descriptive.py", script_sha256=SELF_SHA, utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
+               inputs=dict(csv=p5.name, csv_sha256=sha256(p5), judgment=j5.name, judgment_sha256=sha256(j5), script_25_05_sha256=J5.get("script_sha256"),
                            ref_suffix=RSFX, h5_evaluated=H5_OK),
@@ -158,3 +154,3 @@
                conversion="I = 2.54 + 1.82 log10 PGV", results=OUT, limits=LIMITS, descriptive_only=True),
-          open(ROOT / f"models/24_08_intensity{SFX}.json", "w"), indent=1)
-print(f"[24_08] 出力: models/24_08_intensity{SFX}.json・PDF/24_08_F1_intensity_change{SFX}.pdf(と .png)")
+          open(ROOT / f"models/25_08_intensity{SFX}.json", "w"), indent=1)
+print(f"[25_08] 出力: models/25_08_intensity{SFX}.json・PDF/25_08_F1_intensity_change{SFX}.pdf(と .png)")
```

## 25_09_shimane2018_flag_descriptive.py(新)

```python
#!/usr/bin/env python3
# =============================================================================
# Script : 25_09_shimane2018_flag_descriptive.py  (v1)
#          [記述(判定に使わない): 島根県西部 2018 の試験の地震を、気象庁の震源決定の印で「手動(K・k・S・s)」と「自動(A・a)」に
#           分け、25_05 の誤差(BEST・C3・C4、τ までの検測の BEST・C3)の中央値と、C3 対 BEST の対の比べ(記述の p)を並べる]
# Project: ARGUS(新生)— 5 つ目の余震系列での一発試験(事前登録 25)の記述
# 新しく書いたもの(派生元なし)。事前登録 25 で凍結する(9 節)。
#
# なぜ要るか:
#   25_00 の数え上げで、島根の試験の候補(R1 の見積もりの後、カタログだけ)41 のうち 25 が気象庁の自動の震源(印 A)だった
#   (K 15・k 1)。これまでの系列は、ほとんどが手動の震源だった(長野 2014 は Mj ≥ 1.5 の全てが K)。正解(試験の地震の震源)と
#   過去の地震の位置の一部が自動の震源になるので、「C3 の勝ち負けが自動の震源の誤差に引っ張られていないか」を査読で問われうる。
#   そこで、印で分けた誤差を、結果を見る前に決めた形で記述として出す。検定にはしない(仮説も α も無い。分けた後の数が少ない)。
#
# 何をするか:
#   1. 25_05 の本番の data/25_05_per_event.csv と models/25_05_judgment.json(--dev では _dev)を読む。25_08 と同じ確かめ
#      (凍結した 25_05 v1 の SHA-256 SHA_2505・--ref-suffix・INCONCLUSIVE なら止める)。
#   2. 25_01 の jma_shimane2018.csv(--catalog)を読み、CSV の各行(試験の地震)の自分の行を、25_03h と同じ見つけ方
#      (キャッシュの時刻 = 日本時間を 0.1 s で切り捨てたもの、と Mj が一致する、ただ 1 つの行)で見つけて、震源決定の印を取る。
#      見つからないか 2 行以上なら止める。
#   3. 印で 手動(K・k・S・s)/自動(A・a)/その他 に分け、τ = 0.5・2 s の BEST(25_05 の per_tau[τ]["C3"]["best"]。H1 と同じ選び方を
#      全ての試験の地震で行ったもの)・C3・C4 と、25_05 の H5 が評価された時は τ までの検測の BEST・C3 の、数・中央値を出す。
#      τ = 2 s の C3 対 BEST は、組ごとに 片側の対応 Wilcoxon(zero_method='wilcox')の p(差が 0 でない組が 10 以上の時だけ。25_05 と同じ)・
#      差が 0 でない組の数・C3 が小さい組の割合を記述として出す(H1 の判定の代わりにはしない)。
#   4. 出力: models/25_09_flag_descriptive.json・PDF/25_09_F1_errors_by_flag.pdf(--dev では _dev)。
#
# 限界: 印は気象庁の震源の作り方を表すだけで、震源の誤差の大きさそのものではない。組ごとの数は少ない(25_00 の見積もりで手動 16・自動 25)。
#   BEST は全ての試験の地震で選んだもので、組ごとには選び直さない。対は 25_05 の CSV の 4 桁の値で比べるので、組「all」の
#   差が 0 でない組の数と p は、25_05 の H1 の値と同じになるとは限らない(H1 の判定は 25_05 の値)。
#
# Usage : cd ~/SWIFT && uv run python src/25_09_shimane2018_flag_descriptive.py        (25_05 の本番の後。25_08 の後に回す)
#         cd ~/SWIFT && uv run python src/25_09_shimane2018_flag_descriptive.py --dev  (25_05 の dev の後。配管の確かめ)
#         cd ~/SWIFT && uv run python src/25_09_shimane2018_flag_descriptive.py --selftest
# 入力  : data/25_05_per_event.csv・models/25_05_judgment.json・models/25_05_opened.json・data/shimane2018_processed/jma_shimane2018.csv
# =============================================================================
import json, csv, hashlib, argparse, sys, datetime as dt
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
TAG = "[25_09]"
ap = argparse.ArgumentParser()
ap.add_argument("--dev", action="store_true", help="25_05 の dev の出力で回す(配管の確かめ)")
ap.add_argument("--ref-suffix", default="", help="25_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
ap.add_argument("--catalog", default="data/shimane2018_processed/jma_shimane2018.csv", help="25_01 の出力(日本時間・全ての規模・印の列 det_flag)")
ap.add_argument("--selftest", action="store_true")
A = ap.parse_args()
SHA_2505 = "80309ce7012b89af0c052e225cb66b2e15ee104af247937b63510064f9c11398"                          # 事前登録 25 で凍結する 25_05 v1 の SHA-256(25_06f・25_06g・25_08 と同じ照合)
TAUS = ["0.5", "2"]
MIN_NONZERO = 10                                   # 25_05 と同じ: 差が 0 でない組が 10 未満なら p を出さない
MANUAL, AUTO = {"K", "k", "S", "s"}, {"A", "a"}


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()


def utc_naive(o):
    """25_03h と同じ: キャッシュの origin_time(UTC の文字列)を、タイムゾーンなしの UTC の datetime にする"""
    s = str(o).strip().replace("T", " ").replace("Z", "")
    if "+" in s[10:]: s = s[:10] + s[10:].split("+")[0]
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try: return datetime.strptime(s[:26], fmt)
        except ValueError: pass
    sys.exit(f"{TAG} STOP: origin_time {o!r} を時刻として読めない")


def read_catalog(path):
    """25_03h と同じ読み方。戻り値: (時刻を 0.1 s で切り捨てたもの, Mj) -> [印, ...]"""
    idx = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            ts = row["time"].strip()
            t21 = datetime.strptime(ts[:21].ljust(21, "0"), "%Y-%m-%d %H:%M:%S.%f")
            mg = row.get("mag", "").strip()
            try: mjv = float(mg) if mg else None
            except ValueError: mjv = None
            if mjv is None: continue
            idx.setdefault((t21, round(mjv, 3)), []).append(row.get("det_flag", "_").strip() or "_")
    return idx


def flag_of(idx, origin_utc_str, mj):
    tj = utc_naive(origin_utc_str) + timedelta(hours=9)
    key = (tj.replace(microsecond=(tj.microsecond // 100000) * 100000), round(float(mj), 3))
    rows = idx.get(key, [])
    if len(rows) != 1: sys.exit(f"{TAG} STOP: 試験の地震 {origin_utc_str}(Mj {mj})の震源一覧の行が {len(rows)} 個(1 個のはず)")
    return rows[0]


def group(f):
    return "manual (K, k, S, s)" if f in MANUAL else "automatic (A, a)" if f in AUTO else "other"


def selftest():
    import tempfile, os
    def check(c, m):
        if not c: sys.exit(f"{TAG} STOP: selftest に失敗: {m}")
    d = tempfile.mkdtemp(); p = os.path.join(d, "c.csv")
    with open(p, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["time", "latitude", "longitude", "depth_km", "mag", "det_flag"])
        w.writerow(["2018-04-12 10:00:05.37", "35.1", "132.5", "10.00", "1.7", "A"])
        w.writerow(["2018-04-12 10:00:09.91", "35.1", "132.5", "10.00", "1.7", "K"])
        w.writerow(["2018-04-12 11:00:00.00", "35.1", "132.5", "10.00", "1.6", "_"])
    idx = read_catalog(p)
    check(flag_of(idx, "2018-04-12 01:00:05.300000", 1.7) == "A", "0.1 s の切り捨てで自分の行(A)")
    check(flag_of(idx, "2018-04-12 01:00:09.900000", 1.7) == "K", "自分の行(K)")
    check(group("A") == "automatic (A, a)" and group("k") == "manual (K, k, S, s)" and group("_") == "other", "組の分け方")
    print(f"{TAG} selftest: 自分の行の見つけ方(25_03h と同じ)・組の分け方の 3 例に合格")


selftest()
if A.selftest: sys.exit(0)
from scipy.stats import wilcoxon
SELF_SHA = sha256(Path(__file__))
print(f"{TAG} 本スクリプト v1 SHA-256 {SELF_SHA[:12]}…")
for d in ("models", "PDF"): (ROOT / d).mkdir(exist_ok=True)
SFX = "_dev" if A.dev else ""
RSFX = "_dev" if A.dev else A.ref_suffix
p5, j5, pc = ROOT / f"data/25_05_per_event{RSFX}.csv", ROOT / f"models/25_05_judgment{RSFX}.json", ROOT / A.catalog
if not j5.exists(): sys.exit(f"{TAG} STOP: {j5.relative_to(ROOT)} が無い(25_05 の後に回す。やり直した時は --ref-suffix を渡す)")
J5 = json.load(open(j5))
if J5.get("verdict") == "INCONCLUSIVE":
    sys.exit(f"{TAG} STOP: 25_05 の判定が INCONCLUSIVE(評価できる試験の地震が 30 未満)で CSV が無いため、計算しない(事前登録 25 の 2 節)")
for p in (p5, pc):
    if not p.exists(): sys.exit(f"{TAG} STOP: {p} が無い")
if J5.get("script_sha256") != SHA_2505: sys.exit(f"{TAG} STOP: 25_05 の結果が、凍結した 25_05 v1(SHA-256 {SHA_2505[:12]}…)のものでない")
if not A.dev:
    _O = ROOT / "models/25_05_opened.json"
    _c = [r for r in (json.load(open(_O)) if _O.exists() else []) if str(r.get("status", "")).startswith("completed")]
    if not _c or _c[0].get("suffix", "") != RSFX or J5.get("suffix", "") != RSFX:
        sys.exit(f"{TAG} STOP: --ref-suffix '{RSFX}' が、models/25_05_opened.json で最初に completed になった 25_05 の実行と違う")
rows = list(csv.DictReader(open(p5)))
if len(rows) != int(J5["n_evaluated"]): sys.exit(f"{TAG} STOP: CSV の行の数 {len(rows)} が n_evaluated {J5['n_evaluated']} と違う")
IDX = read_catalog(pc)
FL = [flag_of(IDX, r["origin_time"], r["mj"]) for r in rows]
GR = np.array([group(f) for f in FL])
H5_OK = bool(J5.get("causal", {}).get("evaluated", False))
print(f"{TAG} 入力: {p5.name}(SHA-256 {sha256(p5)[:12]}…)  {len(rows)} 地震  25_05 の判定 {J5.get('verdict')}  震源一覧 {pc.name}(SHA-256 {sha256(pc)[:12]}…)")
print(f"{TAG} 印の数: " + "  ".join(f"{f} {FL.count(f)}" for f in sorted(set(FL))) + "  → 組: " +
      "  ".join(f"{g} {int((GR == g).sum())}" for g in ("manual (K, k, S, s)", "automatic (A, a)", "other")))


def col(name):
    return np.array([float(r[name]) if r.get(name, "") not in ("", None) else np.nan for r in rows])


OUT = dict(groups={}, paired_C3_vs_BEST_tau2={})
GROUPS = ["all", "manual (K, k, S, s)", "automatic (A, a)", "other"]
for t in TAUS:
    bo = J5["per_tau"][t]["C3"]["best"]
    M = [("BEST", f"{bo}_err_t{t}", bo), ("C3", f"C3_err_t{t}", "C3"), ("C4", f"C4_err_t{t}", "C4")]
    if H5_OK:
        bc = J5["causal"]["per_tau"][t]["C3"]["best"]
        M += [("BEST, causal picks", f"{bc}_causal_err_t{t}", bc), ("C3, causal picks", f"C3_causal_err_t{t}", "C3")]
    for lab, cname, mname in M:
        e = col(cname)
        for g in GROUPS:
            m = np.isfinite(e) & ((GR == g) if g != "all" else np.ones(len(e), bool))
            OUT["groups"].setdefault(g, {})[f"tau{t}_{lab}"] = dict(method=mname, column=cname, n=int(m.sum()),
                                                                     median_km=(float(np.median(e[m])) if m.any() else None))
bo2 = J5["per_tau"]["2"]["C3"]["best"]
eb, ec = np.round(col(f"{bo2}_err_t2"), 4), np.round(col("C3_err_t2"), 4)        # 25_05 の CSV と同じく 4 桁で比べる
for g in GROUPS:
    m = np.isfinite(eb) & np.isfinite(ec) & ((GR == g) if g != "all" else np.ones(len(eb), bool))
    d = ec[m] - eb[m]; nz = int((d != 0).sum())
    p = (float(wilcoxon(ec[m], eb[m], zero_method="wilcox", alternative="less").pvalue) if nz >= MIN_NONZERO else None)   # 25_05 と同じく 10 組未満は出さない
    OUT["paired_C3_vs_BEST_tau2"][g] = dict(best=bo2, n=int(m.sum()), n_nonzero=nz, p_one_sided_descriptive=p,
                                             share_C3_smaller=(float((d < 0).mean()) if m.any() else None))
f3 = lambda x: "—" if x is None else f"{x:.3f}"
for t in TAUS:
    print(f"{TAG} τ = {t} s(中央値 km、組ごとの数):")
    for k in [k for k in OUT["groups"]["all"] if k.startswith(f"tau{t}_")]:
        print("   " + f"{k[len(f'tau{t}_'):]:>20s}  " + "  ".join(f"{g}: {f3(OUT['groups'][g][k]['median_km'])}(n={OUT['groups'][g][k]['n']})" for g in GROUPS))
print(f"{TAG} τ = 2 s の C3 対 BEST({bo2})の記述(判定ではない): " +
      "  ".join(f"{g}: 差が 0 でない組 {v['n_nonzero']}・片側 p {f3(v['p_one_sided_descriptive'])}・C3 が小さい割合 {f3(v['share_C3_smaller'])}"
                for g, v in OUT["paired_C3_vs_BEST_tau2"].items()))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
G3 = ["manual (K, k, S, s)", "automatic (A, a)"]
fig, axs = plt.subplots(1, 2, figsize=(11, 4.4))
for ax, t in zip(axs, TAUS):
    keys = [k for k in OUT["groups"]["all"] if k.startswith(f"tau{t}_")]
    x = np.arange(len(keys)); bw = 0.38
    for j, (g, c) in enumerate(zip(G3, ("tab:blue", "tab:orange"))):
        v = [OUT["groups"][g][k]["median_km"] or 0.0 for k in keys]
        b = ax.bar(x + (j - 0.5) * bw, v, bw, color=c, label=f"{g} hypocentres")
        for xi, k in zip(x, keys):
            ax.text(xi + (j - 0.5) * bw, (OUT["groups"][g][k]["median_km"] or 0.0) * 1.01, f"n={OUT['groups'][g][k]['n']}", ha="center", va="bottom", fontsize=7)
    ax.set_xticks(x); ax.set_xticklabels([k[len(f"tau{t}_"):] for k in keys], rotation=20, ha="right")
    ax.set_title(f"tau = {t} s", fontsize=10); ax.grid(alpha=0.3, axis="y")
    top = max([OUT["groups"][g][k]["median_km"] or 0.0 for g in G3 for k in keys] + [1e-3]); ax.set_ylim(0, top * 1.18)
    ax.set_ylabel("Median epicentral error vs JMA (km)")
h_, l_ = axs[0].get_legend_handles_labels()
fig.legend(h_, l_, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.02), fontsize=9)
fig.suptitle("Western Shimane 2018" + (" (DEV)" if A.dev else "") + ": errors by JMA hypocentre flag of the test event (descriptive)", fontsize=10)
fig.tight_layout(rect=(0, 0.08, 1, 0.95))
fig.savefig(ROOT / f"PDF/25_09_F1_errors_by_flag{SFX}.pdf", bbox_inches="tight"); plt.close(fig)
json.dump(dict(script="25_09_shimane2018_flag_descriptive.py", version="v1", script_sha256=SELF_SHA,
               utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               inputs=dict(csv=p5.name, csv_sha256=sha256(p5), judgment=j5.name, judgment_sha256=sha256(j5), script_25_05_sha256=J5.get("script_sha256"),
                           ref_suffix=RSFX, catalog=pc.name, catalog_sha256=sha256(pc), h5_evaluated=H5_OK),
               flags=dict(manual=sorted(MANUAL), automatic=sorted(AUTO), counts={f: FL.count(f) for f in sorted(set(FL))}),
               results=OUT, descriptive_only=True,
               limits=["the flag describes how JMA produced the hypocentre, not its error", "groups are small",
                       "BEST is the one chosen on all test events (as in H1), not re-chosen per group",
                       "p values are descriptive (no hypothesis, no alpha, no multiplicity control)",
                       "pairs are compared on the 4-decimal values of the 25_05 CSV, so n_nonzero and p of the group 'all' need not equal H1's values in 25_05"]),
          open(ROOT / f"models/25_09_flag_descriptive{SFX}.json", "w"), indent=1)
print(f"{TAG} 出力: models/25_09_flag_descriptive{SFX}.json・PDF/25_09_F1_errors_by_flag{SFX}.pdf")
```

## 作りもののデータでの試験(凍結の前。島根の本物のデータは一つも開いていない)

作りものの震源ファイル(島根の本震と同じ日時・位置、同じ日に範囲の外のもっと大きい地震を 1 つ入れたもの)と、24 の試験で使った
作りもののキャッシュ(161 地震)の時刻を島根の時間に移したもの、作りものの 24_07 の出力で回した。値は配管の確かめで、結果の見込みではない。

| # | 試験 | 使ったもの | 結果 |
|---|---|---|---|
| 1 | 25_01 の版の確かめ | 25_01 の凍結版と作りものの h2018.zip | SHA-256 が 25_00 の版と違うので `STOP`(期待どおり) |
| 2 | 25_01 の本震の規則 | 版の確かめの値だけを作りものに替えた写し | 同じ日に範囲の外の Mj 6.5 があっても、本震 2018-04-09 01:32:30.81 JST・M6.1 を取った。箱 [35.0347, 35.3347, 132.4117, 132.7617] と期間は 25_00 と同じ |
| 3 | 25_03h | 島根の時間に移したキャッシュと、試験の地震 2 つの近くに別の地震を足した震源一覧 | R1 で 2 地震を除いた(試験の候補 74 → 72)。本震は除かない |
| 4 | 25_04d の新しい (d) が 25_04v と同じ計算か | 24 の作りもののキャッシュ 3 つ(正常・1 地震の外れ・時計のずれ) | 最大の値と窓が 25_04v(K = 5)と同じ(正常 0.014 s PASS・1 地震の外れ 0.014 s PASS・時計のずれ 0.674 s FAIL、2014-12-13 03:36 からの窓) |
| 5 | 25_04d・25_04e | 島根の時間に移したキャッシュ | (d) は 本震 + 72 h より後の 96 地震・92 窓で PASS、G-clock2 PASS。25_04e も最後まで。selftest 7 例に合格 |
| 6 | 25_05 の dev | 25_05 の凍結版 | 全てのゲート PASS(G-untouched・G-split・G-causal 0・陽性対照 0.000841・G-phys 0.101 km・H5 の経路の G-causal 0) |
| 7 | 24_05 と同じ計算か | 25_05 の dev と 24_05 の dev(24 の試験)の CSV | 発生時刻の列のほかの 3280 個の値が 1 つも違わない |
| 8 | 25_06g の dev | 作りもののモデルの SHA-256 と学習の行の SHA-256 だけを写しの中で替えた | 写した部分の SHA-256 は凍結の値と同じ・G-leak・G-same PASS・dev は INCONCLUSIVE |
| 9 | 25_08 の dev | 25_08 の凍結版 | 最後まで |
| 10 | 25_09 | 25_09 の凍結版 | selftest 3 例に合格。dev と本番の形(opened.json あり)で最後まで。`--ref-suffix` が違うと STOP、25_05 が INCONCLUSIVE だと STOP |

試していないもの: 25_06f の計算(凍結した 21_06 のモデルが要る。24 と同じく、凍結版の差分が名前だけであることを DIFF で確かめた)、
本物の Hi-net の取得と PhaseNet(25_02・25_03・24_07。Colab で初めて回る。計算は 24 と同じ)。
