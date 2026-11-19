# DIFF_LOG_24 — 凍結版 24_01〜24_08 と派生元の差分

各スクリプトの派生元・SHA-256・差分(diff -U1)。差分は全部載せる(省略なし)。

| 凍結版 | 派生元 | 派生元 SHA-256 | 追加 | 削除 |
|---|---|---|---|---|
| 24_01_nagano2014_jma_catalog.py | 21_20a_osaka2018_jma_catalog.py | `cad845a143750140…` | 64 | 77 |
| 24_02_nagano2014_hinet_to_h5.py | 21_20b_osaka2018_hinet_to_h5.py | `43154e7a3b33451d…` | 123 | 115 |
| 24_03_nagano2014_realpick_cache_colab.py | 21_20c_osaka2018_realpick_cache_colab.py | `7b938b944003d99f…` | 42 | 47 |
| 24_03h_nagano2014_overlap_exclusion.py | 21_20h_osaka2018_overlap_exclusion.py | `32a383a04dd7959f…` | 52 | 80 |
| 24_04d_nagano2014_gclock2_picks.py | 21_20d_osaka2018_gclock2_picks.py | `606d0eea2f76a860…` | 44 | 63 |
| 24_04e_nagano2014_station_pick_diagnose.py | 21_20e_osaka2018_station_pick_diagnose.py | `680e8825d49e00bb…` | 21 | 36 |
| 24_05_nagano2014_similarity_confirmation.py | 21_20_osaka2018_similarity_confirmation.py | `2c0fb375e6a1a8d4…` | 347 | 125 |
| 24_06f_nagano2014_learned_test.py | 21_20f_osaka2018_learned_test.py | `9623695ea33bef90…` | 126 | 122 |
| 24_06g_nagano2014_gate_test.py | 22_04_osaka2018_gate_test.py | `7a634ca58e08fe75…` | 134 | 159 |
| 24_07_causal_picks.py | 24_07_causal_picks.py | `11c6727f0ff9e742…` | 64 | 21 |
| 24_08_nagano2014_intensity_descriptive.py | 21_10_gmpe_location_error.py | `de9cbf5933bf75e5…` | 118 | 150 |

## 24_01_nagano2014_jma_catalog.py ← 21_20a_osaka2018_jma_catalog.py

```diff
--- osaka/21_20a_osaka2018_jma_catalog.py	2026-11-01 23:37:03.890446185 +0000
+++ nagano/frz/24_01_nagano2014_jma_catalog.py	2026-11-15 05:21:00.094090162 +0000
@@ -2,46 +2,33 @@
 # =============================================================================
-# Script : 21_20a_osaka2018_jma_catalog.py  (v1)
-#          [大阪府北部 2018(本震 2018-06-18 朝、日本時間 7 時 58 分台)の気象庁の震源を、21_02・21_04 と同じ形の CSV にする]
-# Project: ARGUS(新生)— 3 つ目の余震系列での確認(21_20)の入力の 1 つ目
-# 派生元 : 21_04a_ct2016_jma_catalog.py v1(SHA-256 312e4c7d1292c1aac16352ccc7dd903ec5be979a1c360cdd3e57a9d65e767ae1)。
-#          読み方・除外・箱・期間・数え方・CSV の書き方は 21_04a と 1 字も変えていない。変えたのは次だけ(DIFF_LOG.md):
-#          (1) 震源ファイル h2016.zip → h2018.zip
-#          (2) 本震の規則: 21_04a は「資料名から分かる発生時刻 ± 5 s」だったが、大阪府北部 2018 の秒までの発生時刻は、
-#              この震源ファイルを開く前には確かめていないので、ここには書かない。代わりに、気象庁の発表の
-#              「2018-06-18 07 時 58 分」の 1 分間 [07:58:00, 07:59:00) JST に入ること、を本震の条件にする
-#              (要確認: 震源ファイルを開いた後、表示の本震の時刻がこの 1 分に入ることを確かめる。入らなければ STOP する)。
-#              Mj ≥ 6.0(21_20 の G-untouched と本震の確かめが Mj ≥ 6.0 を使うので、それに合わせる。21_04a は 6.4)、
-#              深さ 5–20 km(21_04a と同じ)、緯度 34.65–35.05・経度 135.35–135.85(21_04a と同じ幅 0.4° × 0.5°)
-#          (3) 出力の名前(jma_osaka2018.csv・21_20a_osaka2018_catalog.json・PDF/21_20a_osaka2018_catalog.pdf)、表示、図の題
-#          (4) 最後に、試験の候補(本震 + 72 時間より後の 1.5 ≤ Mj < 2.0)が 30 未満なら STOP(exit 1)する。評価できる試験の
-#              地震は候補より多くならないので、30 未満なら 21_04 と同じ規則で INCONCLUSIVE が決まる。波形を取る前に止めて、
-#              そのまま報告する(事前登録 21_20 の「波形を取る前の止め方」)。出力の CSV・JSON・図は止める前に書く。
-#          読み方の試験(selftest)は 21_04a と同じ作りものの 2016 年のレコードのまま(読み方だけを試す。年には依らない)。
+# Script : 24_01_nagano2014_jma_catalog.py  (v1)
+#          [長野県北部 2014(本震 2014-11-22 22:08 JST、神城断層)の気象庁の震源を、21_02・21_04・21_20 と同じ形の CSV にする]
+# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の 1 つ目
+# 派生元 : 21_20a_osaka2018_jma_catalog.py v1(SHA-256 cad845a14375014056b7da2a539b750d88363be56620904381fd520db16d25d2)。
+#          読み方・除外・箱・期間・数え方・CSV の書き方・試験の候補が 30 未満で止める規則は 21_20a と 1 字も変えていない。
+#          変えたのは次だけ(DIFF_LOG_24.md):
+#          (1) 震源ファイル h2018.zip → h2014.zip
+#          (2) 本震の規則: 2014-11-22 の J の震源のうち Mj が最大の地震で、発生時刻が [22:08:00, 22:09:00) JST、Mj ≥ 6.5、
+#              深さ 0–20 km、緯度 36.45–36.95・経度 137.65–138.15(幅 0.5° × 0.5°)。24_00(事前登録の前の数だけの確かめ)と同じ値。
+#              深さを 0 km からにしたのは、気象庁の発表で本震の深さが 5 km 前後と浅く、21_20a の 5 km の境目に当たるのを避けるため
+#              (本震を見つけるためだけの値で、試験の地震の選び方には使わない)
+#          (3) 出力の名前(jma_nagano2014.csv・24_01_nagano2014_catalog.json・PDF/24_01_nagano2014_catalog.pdf)、表示 [24_01]、図の題
 #
-# 何をするか:
-#   1. 気象庁の震源ファイル h2018.zip(地震ごとに 96 バイトの震源レコード 1 行、時刻は日本時間)を
-#      https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2018.zip から data/catalog/jma_raw/ に取る
-#      (登録不要のはず。既にあれば取らない。--hypo で手元のファイルを指定してもよい)。
-#      要確認: h2018.zip がこの場所にあること(21_04a の h2016.zip と同じ場所の決まりから作った URL。このスクリプトを書いた
-#      時点では取りに行っていない)。取れなければ STOP するので、気象庁のページからブラウザで取って --hypo で渡す。
-#   2. 震源レコードを列の位置どおりに読む(21_04a と同じ。書式: https://www.data.jma.go.jp/eqev/data/bulletin/data/format/hypfmt_e.html)。
-#   3. 本震(上の (2) の規則): 2018-06-18 の J の震源のうち Mj が最大の地震。発生時刻が [07:58:00, 07:59:00) JST、Mj ≥ 6.0、
-#      深さ 5–20 km、緯度 34.65–35.05・経度 135.35–135.85、でなければ STOP。本震が除く印を持つ時も STOP。
-#   4. 範囲(21_04a と同じ規則): 箱 = 本震の緯度 ± 0.15°、経度 ± 0.175°。期間 = 本震の 2 日前から 24 日後(日本時間)。
-#      使う震源・除外・印ごとの数の記録は 21_04a と同じ。
-#   5. 出力: data/catalog/jma_osaka2018.csv(列は 21_04a と同じ。15_01c・21_20c がそのまま読める)と
-#      data/catalog/21_20a_osaka2018_catalog.json(本震・箱・期間・数・除いた数。21_20b と 21_20c に渡す箱はここから読む)。
-#   6. 図: PDF/21_20a_osaka2018_catalog.pdf(白背景・英語・凡例は枠の外)。
-#   7. 試験の候補が 30 未満なら STOP(上の (4))。
+# 何をするか(21_20a と同じ。年と名前だけが違う):
+#   1. 気象庁の震源ファイル h2014.zip を data/catalog/jma_raw/ に取る(24_00 で取ってあれば取らない。--hypo で指定してもよい)。
+#   2. 震源レコードを列の位置どおりに読む。3. 本震を上の規則で確かめる。4. 箱 = 本震の緯度 ± 0.15°・経度 ± 0.175°、
+#      期間 = 本震の 2 日前から 24 日後(日本時間)。除外・印ごとの数の記録は 21_20a と同じ。
+#   5. 出力: data/catalog/jma_nagano2014.csv(24_02・24_03 がそのまま読む)・data/catalog/24_01_nagano2014_catalog.json。
+#   6. 図: PDF/24_01_nagano2014_catalog.pdf。7. 試験の候補(本震 + 72 h より後の 1.5 ≤ Mj < 2.0)が 30 未満なら STOP。
 #
-# 止める条件(STOP): 21_04a と同じもの(読み方の試験・ファイル・96 バイト・本震の日の震源が無い・本震の規則・本震の印・
-#   Mj ≥ 1.5 が 0)と、試験の候補が 30 未満。
-# 限界: 正解も過去の地震も気象庁の震源。h2018 の確定の段階(確定値か)は要確認(21_04a の h2016 は確定値)。
-#   除外(低周波・人工・マッチドフィルタ・決まらない震源)は 21_04a と同じ。手動と自動の震源が混ざる(印ごとの数を JSON に記録)。
-#   箱は本震の周りの決まった大きさで、余震でない地震(背景の地震活動)も入る(21_02・21_04 と同じ)。
+# 開示: この系列の h2014 は、事前登録の前に 24_00(数だけの確かめ)で 1 回開いた。表示したのは本震の行(時刻・位置・深さ・Mj)と
+#   数(全体・Mj ≥ 1.5・試験の候補・R1 の後の数・深さ 25 km より深い数・印の数・日ごとの数)だけで、試験の地震の位置の一覧・
+#   波形・どの方法の誤差も見ていない(事前登録 24 の冒頭)。
+# 止める条件(STOP): 21_20a と同じ(読み方の試験・ファイル・96 バイト・本震の日の震源が無い・本震の規則・本震の印・Mj ≥ 1.5 が 0・
+#   試験の候補が 30 未満)。
+# 限界: 正解も過去の地震も気象庁の震源。h2014 の確定の段階は要確認。手動と自動の震源が混ざる(印ごとの数を JSON に記録。24_00 では
+#   Mj ≥ 1.5 の 502 個が全て K)。箱には余震でない地震も入る。
 #
-# Usage : (Colab、ノート 21_20_osaka2018_colab.ipynb の セル 5)
-#         !python /content/drive/MyDrive/ARGUS/src/21_20a_osaka2018_jma_catalog.py
-#         (読み方の試験だけ: !python .../21_20a_osaka2018_jma_catalog.py --selftest)
-# Output: data/catalog/jma_osaka2018.csv / data/catalog/21_20a_osaka2018_catalog.json / PDF/21_20a_osaka2018_catalog.pdf
+# Usage : (Colab、ノート 24_nagano2014_colab.ipynb の セル N5)
+#         !python /content/drive/MyDrive/ARGUS/src/24_01_nagano2014_jma_catalog.py
+# Output: data/catalog/jma_nagano2014.csv / data/catalog/24_01_nagano2014_catalog.json / PDF/24_01_nagano2014_catalog.pdf
 # =============================================================================
@@ -64,10 +51,10 @@
 ROOT = Path(__file__).resolve().parent.parent
-URL = "https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2018.zip"   # 要確認: この場所にあること(21_04a の URL の年だけを変えた)
+URL = "https://www.data.jma.go.jp/eqev/data/bulletin/data/hypo/h2014.zip"   # 21_20a の URL の年だけを変えた(24_00 で取れた)
 REC_LEN = 96
-# 本震の規則(21_20): 秒までの発生時刻は震源ファイルを開く前には確かめていないので書かない。気象庁の発表の「7 時 58 分」の 1 分間だけを
+# 本震の規則(24): 気象庁の発表の「22 時 08 分」の 1 分間を条件にする(24_00 と同じ規則。24_00 の表示では 22:08:17.90 JST)。以下の 1 行は 21_20a の注記のまま:
 # 条件にする(要確認: 震源ファイルの本震がこの 1 分に入ること。入らなければ STOP。数字を直す時は版を上げて事前登録の記録に書く)
-MAIN_DATE_JST = datetime(2018, 6, 18).date()
-MAIN_WIN_JST = (datetime(2018, 6, 18, 7, 58, 0), datetime(2018, 6, 18, 7, 59, 0))   # [始まり, 終わり)。要確認
-MAIN_MIN_MJ, MAIN_DEPTH = 6.0, (5.0, 20.0)               # Mj ≥ 6.0 は 21_20 の G-untouched・本震の確かめと同じ値
-MAIN_LAT, MAIN_LON = (34.65, 35.05), (135.35, 135.85)    # 21_04a と同じ幅(0.4° × 0.5°)。要確認: 本震がこの中にあること
+MAIN_DATE_JST = datetime(2014, 11, 22).date()
+MAIN_WIN_JST = (datetime(2014, 11, 22, 22, 8, 0), datetime(2014, 11, 22, 22, 9, 0))   # [始まり, 終わり)
+MAIN_MIN_MJ, MAIN_DEPTH = 6.5, (0.0, 20.0)               # 24_00 と同じ(深さは 0 km から。冒頭の (2))
+MAIN_LAT, MAIN_LON = (36.45, 36.95), (137.65, 138.15)    # 24_00 と同じ(0.5° × 0.5°)
 MIN_TEST = 30                                            # 21_04 の MIN_TEST と同じ(評価できる試験の地震が 30 未満なら INCONCLUSIVE)
@@ -171,3 +158,3 @@
     def check(c, msg):
-        if not c: sys.exit(f"[21_20a] STOP: 読み方の試験に失敗: {msg}")
+        if not c: sys.exit(f"[24_01] STOP: 読み方の試験に失敗: {msg}")
     def put(buf, a, b, s):
@@ -196,3 +183,3 @@
     check(t == datetime(2016, 10, 21, 14, 7, 5, 0), 't == datetime(2016, 10, 21, 14, 7, 5, 0)')  # 15_01c は先頭 21 文字だけ読むので 0.1 s 単位に切り捨てる(2026 も同じ)
-    print("[21_20a] selftest: 震源レコードの読み方の試験に全て合格(21_04a と同じ試験)")
+    print("[24_01] selftest: 震源レコードの読み方の試験に全て合格(21_04a と同じ試験)")
 
@@ -201,3 +188,3 @@
     ap = argparse.ArgumentParser()
-    ap.add_argument("--hypo", default="", help="手元の h2018.zip か展開したファイル(無ければ取る)")
+    ap.add_argument("--hypo", default="", help="手元の h2014.zip か展開したファイル(無ければ取る)")
     ap.add_argument("--selftest", action="store_true")
@@ -209,5 +196,5 @@
     for d in (CAT, RAWD, PDFD): d.mkdir(parents=True, exist_ok=True)
-    src = Path(a.hypo) if a.hypo else RAWD / "h2018.zip"
+    src = Path(a.hypo) if a.hypo else RAWD / "h2014.zip"
     if not src.exists():
-        print(f"[21_20a] 取得: {URL}")
+        print(f"[24_01] 取得: {URL}")
         req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (ARGUS research)"})
@@ -217,3 +204,3 @@
         except Exception as e:
-            sys.exit(f"[21_20a] STOP: {URL} が取れない({e})。ブラウザで取って --hypo で指定する")
+            sys.exit(f"[24_01] STOP: {URL} が取れない({e})。ブラウザで取って --hypo で指定する")
         src.write_bytes(data)
@@ -223,3 +210,3 @@
             mem = [m for m in z.namelist() if not m.endswith("/")]
-            if not mem: sys.exit("[21_20a] STOP: zip の中にファイルが無い")
+            if not mem: sys.exit("[24_01] STOP: zip の中にファイルが無い")
             raw = b"\n".join(z.read(m) for m in mem)
@@ -228,7 +215,7 @@
     recs, n_bad = read_records(raw)
-    print(f"[21_20a] 震源ファイル {src.name}(SHA-256 {sha[:12]}…、中身 {mem})  レコード {len(recs)}  96 バイトでない行 {n_bad}")
-    if not recs or n_bad > 0.01 * len(recs): sys.exit("[21_20a] STOP: 96 バイトのレコードの形でない(別のファイルの可能性)")
+    print(f"[24_01] 震源ファイル {src.name}(SHA-256 {sha[:12]}…、中身 {mem})  レコード {len(recs)}  96 バイトでない行 {n_bad}")
+    if not recs or n_bad > 0.01 * len(recs): sys.exit("[24_01] STOP: 96 バイトのレコードの形でない(別のファイルの可能性)")
     H = [parse_hypo(r) for r in recs]
     J = [h for h in H if h["agency"] == "J" and h["origin_jst"] is not None]
-    print(f"[21_20a] 機関 J の震源 {len(J)}(他機関 {sum(1 for h in H if h['agency'] != 'J')}、時刻が読めない {sum(1 for h in H if h['origin_jst'] is None)})")
+    print(f"[24_01] 機関 J の震源 {len(J)}(他機関 {sum(1 for h in H if h['agency'] != 'J')}、時刻が読めない {sum(1 for h in H if h['origin_jst'] is None)})")
 
@@ -236,6 +223,6 @@
     day = [h for h in J if h["origin_jst"].date() == MAIN_DATE_JST and h["mag"] is not None]
-    if not day: sys.exit(f"[21_20a] STOP: {MAIN_DATE_JST} の震源が無い")
+    if not day: sys.exit(f"[24_01] STOP: {MAIN_DATE_JST} の震源が無い")
     m = max(day, key=lambda h: h["mag"])
     in_win = MAIN_WIN_JST[0] <= m["origin_jst"] < MAIN_WIN_JST[1]
-    print(f"[21_20a] 本震: {m['origin_jst']} JST  {m['lat']:.4f}N {m['lon']:.4f}E  深さ {m['depth_km']} km  M{m['mag']}{m['mag_type']}  "
+    print(f"[24_01] 本震: {m['origin_jst']} JST  {m['lat']:.4f}N {m['lon']:.4f}E  深さ {m['depth_km']} km  M{m['mag']}{m['mag_type']}  "
           f"精度 {m['precision']}  (想定の 1 分 {MAIN_WIN_JST[0]:%H:%M:%S}〜{MAIN_WIN_JST[1]:%H:%M:%S} JST の中か: {in_win}。要確認の項目)")
@@ -244,5 +231,5 @@
           and MAIN_LON[0] <= m["lon"] <= MAIN_LON[1])
-    if not ok: sys.exit("[21_20a] STOP: 本震が規則に合わない(読み方の誤りか別のファイル。この行を貼って相談)")
+    if not ok: sys.exit("[24_01] STOP: 本震が規則に合わない(読み方の誤りか別のファイル。この行を貼って相談)")
     if m["det_flag"] in BAD_DETFLAG or m["precision"] in BAD_PRECISION:
-        sys.exit(f"[21_20a] STOP: 本震の震源が除く印(精度 {m['precision']}・震源決定の印 {m['det_flag']})を持つ(この行を貼って相談)")
+        sys.exit(f"[24_01] STOP: 本震の震源が除く印(精度 {m['precision']}・震源決定の印 {m['det_flag']})を持つ(この行を貼って相談)")
     box = [round(m["lat"] - HALF_LAT, 4), round(m["lat"] + HALF_LAT, 4), round(m["lon"] - HALF_LON, 4), round(m["lon"] + HALF_LON, 4)]
@@ -270,4 +257,4 @@
              library_only_mj_ge_2p0_after_72h=int(((mags >= FRESH_MAX_MAG - 1e-9) & after).sum()))
-    if n["mj_ge_1p5"] == 0: sys.exit("[21_20a] STOP: 箱の中・期間内の Mj ≥ 1.5 が 0")
-    out_csv = CAT / "jma_osaka2018.csv"
+    if n["mj_ge_1p5"] == 0: sys.exit("[24_01] STOP: 箱の中・期間内の Mj ≥ 1.5 が 0")
+    out_csv = CAT / "jma_nagano2014.csv"
     with open(out_csv, "w", newline="") as f:
@@ -280,3 +267,3 @@
     flags_15 = dict(Counter(h["det_flag"] or "_" for h in rows if h["mag"] >= MIN_MAG - 1e-9))
-    summ = dict(script="21_20a_osaka2018_jma_catalog.py", version=VERSION, source=URL, source_file=src.name, source_sha256=sha,
+    summ = dict(script="24_01_nagano2014_jma_catalog.py", version=VERSION, source=URL, source_file=src.name, source_sha256=sha,
                 mainshock=dict(origin_jst=fmt_time(m["origin_jst"]), lat=m["lat"], lon=m["lon"], depth_km=m["depth_km"], mj=m["mag"],
@@ -289,8 +276,8 @@
                 note="test candidates are before picking; the evaluated test set is those with a measured P in the cache")
-    json.dump(summ, open(CAT / "21_20a_osaka2018_catalog.json", "w"), indent=1, ensure_ascii=False)
-    print(f"[21_20a] 箱 {box}(緯度 0.30° × 経度 0.35°)  期間 {fmt_time(t0)} 〜 {fmt_time(t1)} JST  pool の切れ目 {fmt_time(cut)} JST")
-    print(f"[21_20a] 除いた数: {ex}")
-    print(f"[21_20a] 数: {n}")
-    print(f"[21_20a] 震源決定の印の数(K・S・k・s = 手動、A・a = 自動。_ は空白): 全体 {flags_all}  Mj ≥ 1.5 {flags_15}")
-    print(f"[21_20a] 出力: {out_csv.relative_to(ROOT)}, data/catalog/21_20a_osaka2018_catalog.json")
+    json.dump(summ, open(CAT / "24_01_nagano2014_catalog.json", "w"), indent=1, ensure_ascii=False)
+    print(f"[24_01] 箱 {box}(緯度 0.30° × 経度 0.35°)  期間 {fmt_time(t0)} 〜 {fmt_time(t1)} JST  pool の切れ目 {fmt_time(cut)} JST")
+    print(f"[24_01] 除いた数: {ex}")
+    print(f"[24_01] 数: {n}")
+    print(f"[24_01] 震源決定の印の数(K・S・k・s = 手動、A・a = 自動。_ は空白): 全体 {flags_all}  Mj ≥ 1.5 {flags_15}")
+    print(f"[24_01] 出力: {out_csv.relative_to(ROOT)}, data/catalog/24_01_nagano2014_catalog.json")
 
@@ -309,3 +296,3 @@
     ax1.set_xlabel(f"Days since mainshock ({m['origin_jst']:%Y-%m-%d %H:%M} JST)"); ax1.set_ylabel("JMA magnitude Mj")
-    ax1.set_title("Northern Osaka 2018, JMA hypocentres in the box", fontsize=10); ax1.grid(alpha=0.3)
+    ax1.set_title("Northern Nagano 2014, JMA hypocentres in the box", fontsize=10); ax1.grid(alpha=0.3)
     bins = np.arange(np.floor(mags.min() * 10) / 10, mags.max() + 0.2, 0.1)
@@ -316,10 +303,10 @@
     fig.legend(h_, l_, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=9, frameon=False, markerscale=3)
-    fig.tight_layout(); fig.savefig(PDFD / "21_20a_osaka2018_catalog.pdf", bbox_inches="tight"); plt.close(fig)
-    print("[21_20a] 図: PDF/21_20a_osaka2018_catalog.pdf")
-    # 21_20: 試験の候補が 30 未満なら、評価できる試験の地震も 30 未満になることが確定する(INCONCLUSIVE)。波形を取る前に止める
+    fig.tight_layout(); fig.savefig(PDFD / "24_01_nagano2014_catalog.pdf", bbox_inches="tight"); plt.close(fig)
+    print("[24_01] 図: PDF/24_01_nagano2014_catalog.pdf")
+    # 21_20・24: 試験の候補が 30 未満なら、評価できる試験の地震も 30 未満になることが確定する(INCONCLUSIVE)。波形を取る前に止める
     nt = n["test_candidates_1p5_to_2p0_after_72h"]
     if nt < MIN_TEST:
-        sys.exit(f"[21_20a] STOP: 試験の候補(本震 + 72 時間より後の 1.5 ≤ Mj < 2.0)が {nt}(< {MIN_TEST})。評価できる試験の地震は"
-                 f"これより多くならないので、21_04 と同じ規則で INCONCLUSIVE。波形は取らずに、この出力を事前登録 21_20 の規則どおり報告する")
-    print(f"[21_20a] 試験の候補 {nt} ≥ {MIN_TEST}: 次へ進める(本当の試験の数は、キャッシュで P を測れた地震だけなので、これより少ない)")
+        sys.exit(f"[24_01] STOP: 試験の候補(本震 + 72 時間より後の 1.5 ≤ Mj < 2.0)が {nt}(< {MIN_TEST})。評価できる試験の地震は"
+                 f"これより多くならないので、21_04 と同じ規則で INCONCLUSIVE。波形は取らずに、この出力を事前登録 24 の規則どおり報告する")
+    print(f"[24_01] 試験の候補 {nt} ≥ {MIN_TEST}: 次へ進める(本当の試験の数は、キャッシュで P を測れた地震だけなので、これより少ない)")
 
```

## 24_02_nagano2014_hinet_to_h5.py ← 21_20b_osaka2018_hinet_to_h5.py

```diff
--- osaka/21_20b_osaka2018_hinet_to_h5.py	2026-11-02 00:09:04.447868300 +0000
+++ nagano/frz/24_02_nagano2014_hinet_to_h5.py	2026-11-15 05:21:00.094713914 +0000
@@ -2,19 +2,22 @@
 # =============================================================================
-# Script : 21_20b_osaka2018_hinet_to_h5.py  (v1)
-#          [大阪府北部 2018 の Hi-net の連続波形を、地震の前後だけ取り、鳥取 2026 の h5(tottori_all_100Hz.h5)と
-#           同じ形(30 秒窓・3 成分・100 Hz・窓ごと成分ごとの z-score・日本時間の epoch)の h5 にする]
-# Project: ARGUS(新生)— 3 つ目の余震系列での確認(21_20)の入力の 2 つ目
-# 派生元 : 21_04b_ct2016_hinet_to_h5.py v1.1(SHA-256 81d69a13ddb3d432a93055e1657b9763b8634910777f004b6767d15788e952c0)。
-#          取り方・z-score・局の選び方・組み立て・ゲート(G-ref・G-dup・G-cover・G-clock・G-spec)・閾値は v1.1 と 1 字も変えていない。
-#          変えたのは次だけ(DIFF_LOG.md):
-#          (1) 入力と出力の名前: jma_osaka2018.csv・21_20a_osaka2018_catalog.json・ARGUS_osaka2018・osaka2018_100Hz.h5・
-#              stations_osaka2018.csv・data/21_20b_*.json・PDF/21_20b_*.pdf、表示の [21_20b]、h5 の出どころの属性の名前
-#          (2) ゲートで止まった時の表示の文: G-clock だけの FAIL なら、事前登録 21_20 で先に決めた扱い(G-clock は記録だけ、
-#              時刻は G-clock2 で決める)を表示する(止まり方と、h5 を _FAILED の名前にする動きは v1.1 と同じ)
-#          (3) VERSION を "v1 (=21_04b v1.1)" にした(この系列の 1 版目。取り方は 21_04b v1.1 と同じ。v1.1 の「要求の長さを短くして取り直す」も含む)
+# Script : 24_02_nagano2014_hinet_to_h5.py  (v1)
+#          [長野県北部 2014 の Hi-net の連続波形を、地震の前後だけ取り、鳥取 2026 の h5(tottori_all_100Hz.h5)と
+#           同じ形(30 秒窓・3 成分・100 Hz・窓ごと成分ごとの z-score・日本時間の epoch)の h5 にする。あわせて、z-score の前の
+#           窓ごと成分ごとの平均と標準偏差(win_mean・win_std)も書く(24_07 が元の値に戻して、τ までの波形だけで検測するため)]
+# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の 2 つ目
+# 派生元 : 21_20b_osaka2018_hinet_to_h5.py v1(SHA-256 43154e7a3b33451d6a2526f4a1b3ff4a8e6085964c380398ceab49b50745e06e。21_04b v1.1 と同じ取り方)。
+#          取り方・z-score・局の選び方・組み立て・ゲート(G-ref・G-dup・G-cover・G-clock・G-spec)・閾値は 21_20b v1 と 1 字も変えていない。
+#          変えたのは次だけ(DIFF_LOG_24.md):
+#          (1) 入力と出力の名前: jma_nagano2014.csv・24_01_nagano2014_catalog.json・ARGUS_nagano2014・nagano2014_100Hz.h5・
+#              stations_nagano2014.csv・data/24_02_*.json・data/24_02.lock・PDF/24_02_*.pdf、表示の [24_02]、h5 の出どころの属性の名前
+#          (2) 窓ごとの尺度の保存(新): zscore_windows が z と一緒に、z-score に使った成分ごとの平均と標準偏差 (窓, 3, 2) を返し、
+#              区切りのファイル(blk_*.npz)に scale として書き、組み立てで h5 の /win_mean・/win_std (窓, 3)(float64)に書く。
+#              /waves(z-score)の値・形・dtype は 21_20b と同じで、24_03(= 15_01c v3.3 の計算)は /waves だけを読む。
+#          (3) G-clock だけの FAIL の時の表示の文を、事前登録 24 と 24_04d に合わせた(止まり方と _FAILED の名前は同じ)
+#          (4) VERSION を "v1 (=21_20b v1 + window scale)" にした
 #
 # なぜ必要か:
-#   21_20 は 21_02・21_04 と同じ規則・同じ作り方(15_01c v3.3 と同じ計算の 21_20c で検測したキャッシュ)で確かめる。15_01c は
+#   24 は 21_02・21_04・21_20 と同じ規則・同じ作り方(15_01c v3.3 と同じ計算の 24_03 で検測したキャッシュ)で確かめる。15_01c は
 #   tottori_all_100Hz.h5 の形(/waves (N, 3, 3000)、/stations、/window_epoch = 窓の始まりの日本時間を UTC とみなした
-#   epoch 秒、属性 channel_order・n_samples・fs)を読む。そこで 2018 の波形をこの形にそろえ、15_01c の検測・QC・
+#   epoch 秒、属性 channel_order・n_samples・fs)を読む。そこで 2014 の波形をこの形にそろえ、15_01c の検測・QC・
 #   組み立てをそのまま通す(15_01c v3.3 で変えたのは、窓の索引のファイル名とその確かめ方・出力の置き場所 --base・
@@ -31,8 +34,8 @@
 #   1. 観測点: NIED の Hi-net(0101)の観測点の一覧(HinetPy の get_station_list。今の一覧。緯度・経度・標高のどれかが無い局は
-#      除く)から、本震(21_20a の JSON)に近い順に --n-sta + 10 局を候補にする。Hi-net のアカウントの「選んだ局」を
-#      最初の 1 回だけ data/21_20b_initial_selection.json に保存してから候補を選び、終わり(止めた時・失敗した時も)に元に戻す。
+#      除く)から、本震(24_01 の JSON)に近い順に --n-sta + 10 局を候補にする。Hi-net のアカウントの「選んだ局」を
+#      最初の 1 回だけ data/24_02_initial_selection.json に保存してから候補を選び、終わり(止めた時・失敗した時も)に元に戻す。
 #      選んだ後の選択が空(= 全局)か候補の外の局を含めば STOP(全局のまま取ると何倍も時間がかかる)。
-#      途中で落ちて戻せなかった時は --restore-selection で戻せる。同時に 2 つ回さないよう data/21_20b.lock を置く
+#      途中で落ちて戻せなかった時は --restore-selection で戻せる。同時に 2 つ回さないよう data/24_02.lock を置く
 #      (区切りごとに新しくし、30 分より古い印は止まった実行の印とみなす。Colab が切れた直後は --restore-selection --break-lock)。
-#   2. 取る時間の区切り: 21_20a の CSV の Mj ≥ 1.5 の地震ごとに、[発生時刻 − 10 s を分に切り下げ, 発生時刻 + 45 s を
+#   2. 取る時間の区切り: 24_01 の CSV の Mj ≥ 1.5 の地震ごとに、[発生時刻 − 10 s を分に切り下げ, 発生時刻 + 45 s を
 #      分に切り上げ](日本時間)。15_01c が使う区間 [発生 − 10 s, 発生 + 45 s] を 30 秒窓で必ず覆う。間が 2 分以下の
@@ -59,9 +62,9 @@
 #      区切りの半分以上でデータがある局のうち本震に近い順に --n-sta 局(既定 50。鳥取 2026 の局の数と同じ)を選び、その局の
-#      窓だけを書く。data/catalog/stations_osaka2018.csv(列 id, latitude, longitude, elevation。緯度・経度は 2018 年の
+#      窓だけを書く。data/catalog/stations_nagano2014.csv(列 id, latitude, longitude, elevation。緯度・経度は 2014 年の
 #      チャンネル表、標高は NIED の一覧の height(m)。stations.csv と同じ列)も書く。
-#      ゲートを書きかけのファイル(.part)で確かめ、全て通った時だけ data/waves/osaka2018_100Hz.h5 の名前にする
-#      (通らなければ osaka2018_100Hz_FAILED.h5 にして STOP。21_20c に渡る名前の h5 は作らない。G-clock だけの FAIL の扱いは
-#      事前登録 21_20 に先に決めてある: 記録だけで、_FAILED の h5 と stations_osaka2018.csv.part を 21_20c に渡し、時刻は G-clock2 で決める)。
+#      ゲートを書きかけのファイル(.part)で確かめ、全て通った時だけ data/waves/nagano2014_100Hz.h5 の名前にする
+#      (通らなければ nagano2014_100Hz_FAILED.h5 にして STOP。24_03 に渡る名前の h5 は作らない。G-clock だけの FAIL の扱いは
+#      事前登録 24 に先に決めてある: 記録だけで、_FAILED の h5 と stations_nagano2014.csv.part を 24_03 に渡し、時刻は G-clock2 で決める)。
 #      --partial(煙試験の確認): 取った区切りだけで組み立て、名前に _partial を付ける。
-#   5. ゲート(組み立ての後に表示し、data/21_20b_report.json に合否と一緒に書く):
+#   5. ゲート(組み立ての後に表示し、data/24_02_report.json に合否と一緒に書く):
 #      - G-ref: 参照の h5 の z-score の確認に合格(fs = 100)。出力も同じ確認に合格
@@ -79,3 +82,3 @@
 #        違いがあれば限界に書く)
-#   6. 図: PDF/21_20b_coverage.pdf(局 × 区切りのデータの有無)、PDF/21_20b_mainshock.pdf(本震の上下動の
+#   6. 図: PDF/24_02_coverage.pdf(局 × 区切りのデータの有無)、PDF/24_02_mainshock.pdf(本震の上下動の
 #      記録の並びと、予想の P の印)。白背景・英語・凡例は枠の外。
@@ -84,8 +87,8 @@
 #   win32tools の catwin32・win2sac_32 が PATH にある(ノートの セル 3)、HinetPy 0.13.0。
-# 止める条件(STOP): 資格情報が無い・win2sac_32 が無い・参照の h5 が読めないか形が違うか fs が無い・21_20a の JSON が無い・
+# 止める条件(STOP): 資格情報が無い・win2sac_32 が無い・参照の h5 が読めないか形が違うか fs が無い・24_01 の JSON が無い・
 #   置き場所が足りない見込み・局の選択が効かない・別の実行の印がある・3 回ずつ試して取れない区切りが 3 つ続く・組み立てで取っていない
 #   区切りがあるか読めないファイルがある・使える局が 0・窓が 0・G-ref・G-dup・G-cover < 0.80・G-clock の失敗。
-# 限界(21_20 の限界にも書く):
+# 限界(24 の限界にも書く):
 #   - 観測点は Hi-net(0101)だけで、鳥取 2026 の 50 局(Hi-net のほか京大防災研・気象庁などを含む)とは種類と並びが違う
-#   - 候補は今の NIED の一覧から選ぶので、2018 年にあって今は無い局は入らない
+#   - 候補は今の NIED の一覧から選ぶので、2014 年にあって今は無い局は入らない
 #   - 地震の前後だけを取る(連続ではない)。15_01c が使う区間は全て含む。区切りの中で欠けがある局は、その区切りでは使わない
@@ -93,13 +96,13 @@
 #
-# Usage : (Colab、ノート 21_20_osaka2018_colab.ipynb の セル 6〜9。手順は COLAB_STEPS_JA.md)
-#   計画だけ:       !python /content/drive/MyDrive/ARGUS/src/21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5> --dry-run
-#   煙試験(本震の区間に掛かる区切りを先に 3 区切り): !python .../21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5> --max-blocks 3
-#                    続けて !python .../21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5> --assemble --partial(取った分だけでゲートを見る)
-#   本番(続きから):   !python .../21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5>
-#   組み立て:         !python .../21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5> --assemble
-#   選択を戻すだけ:   !python .../21_20b_osaka2018_hinet_to_h5.py --ref-h5 <参照の h5> --restore-selection [--break-lock](セル 8b)
-# Output (--out の下。既定 /content/drive/MyDrive/ARGUS_osaka2018):
-#   data/blocks/blk_*.npz / data/21_20b_plan.json / data/21_20b_initial_selection.json /
-#   data/waves/osaka2018_100Hz.h5 / data/catalog/stations_osaka2018.csv / data/21_20b_report.json /
-#   PDF/21_20b_coverage.pdf / PDF/21_20b_mainshock.pdf(--partial ではそれぞれ _partial 付き)
+# Usage : (Colab、ノート 24_nagano2014_colab.ipynb の セル N6〜N9。手順は 24_STEPS_JA.md)
+#   計画だけ:       !python /content/drive/MyDrive/ARGUS/src/24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5> --dry-run
+#   煙試験(本震の区間に掛かる区切りを先に 3 区切り): !python .../24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5> --max-blocks 3
+#                    続けて !python .../24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5> --assemble --partial(取った分だけでゲートを見る)
+#   本番(続きから):   !python .../24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5>
+#   組み立て:         !python .../24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5> --assemble
+#   選択を戻すだけ:   !python .../24_02_nagano2014_hinet_to_h5.py --ref-h5 <参照の h5> --restore-selection [--break-lock](セル N8b)
+# Output (--out の下。既定 /content/drive/MyDrive/ARGUS_nagano2014):
+#   data/blocks/blk_*.npz / data/24_02_plan.json / data/24_02_initial_selection.json /
+#   data/waves/nagano2014_100Hz.h5 / data/catalog/stations_nagano2014.csv / data/24_02_report.json /
+#   PDF/24_02_coverage.pdf / PDF/24_02_mainshock.pdf(--partial ではそれぞれ _partial 付き)
 #   区切りのファイルは組み立ての後も消さない(h5 を作り直せるように。要らなくなったら data/blocks を手で消す)
@@ -126,3 +129,3 @@
 
-VERSION = "v1 (=21_04b v1.1)"              # 21_20b の 1 版目(取り方は 21_04b v1.1 と同じ)
+VERSION = "v1 (=21_20b v1 + window scale)"   # 24_02 の 1 版目(取り方は 21_20b v1 = 21_04b v1.1 と同じ。窓ごとの尺度を足した)
 ROOT = Path(__file__).resolve().parent.parent
@@ -179,3 +182,3 @@
 
-BLK_KEYS = ("stations", "epoch", "waves", "chan", "stat")
+BLK_KEYS = ("stations", "epoch", "waves", "chan", "stat", "scale")   # 24_02: scale を足した
 
@@ -233,5 +236,6 @@
 def zscore_windows(arr3: np.ndarray, dtype):
-    """arr3: (3, n) → 窓ごとの (z (k, 3, 3000), 使った窓の番号)。窓ごと・成分ごとの z-score"""
+    """arr3: (3, n) → 窓ごとの (z (k, 3, 3000), 使った窓の番号, 尺度 (k, 3, 2) = 成分ごとの [平均, 標準偏差])。窓ごと・成分ごとの z-score。
+    24_02: 尺度を返すのを足した(z の計算は 21_20b と同じ)"""
     nwin = arr3.shape[1] // WIN_N
-    zs, ks = [], []
+    zs, ks, sc = [], [], []
     for k in range(nwin):
@@ -243,3 +247,4 @@
         zs.append(((seg - seg.mean(axis=1, keepdims=True)) / sd[:, None]).astype(dtype)); ks.append(k)
-    return (np.stack(zs) if zs else np.zeros((0, 3, WIN_N), dtype)), ks
+        sc.append(np.stack([seg.mean(axis=1), sd], axis=1))                     # 24_02: (3, 2) = [平均, 標準偏差](z と同じ値で計算)
+    return (np.stack(zs) if zs else np.zeros((0, 3, WIN_N), dtype)), ks, (np.stack(sc) if sc else np.zeros((0, 3, 2)))
 
@@ -278,10 +283,10 @@
         for k in ("waves", "stations", "window_epoch"):
-            if k not in H: sys.exit(f"[21_20b] STOP(G-ref): 参照の h5 に /{k} が無い")
+            if k not in H: sys.exit(f"[24_02] STOP(G-ref): 参照の h5 に /{k} が無い")
         W = H["waves"]
-        if tuple(W.shape[1:]) != (3, WIN_N): sys.exit(f"[21_20b] STOP(G-ref): 参照の /waves の形 {W.shape} が (N, 3, 3000) でない")
+        if tuple(W.shape[1:]) != (3, WIN_N): sys.exit(f"[24_02] STOP(G-ref): 参照の /waves の形 {W.shape} が (N, 3, 3000) でない")
         attrs = {k: (v.decode() if isinstance(v, bytes) else (v.tolist() if hasattr(v, "tolist") else v)) for k, v in H.attrs.items()}
         fsv = attrs.get("fs", attrs.get("sampling_rate"))
-        if fsv is None: sys.exit("[21_20b] STOP(G-ref): 参照の h5 に属性 fs が無い")
+        if fsv is None: sys.exit("[24_02] STOP(G-ref): 参照の h5 に属性 fs が無い")
         fs = float(np.ravel(fsv)[0])
-        if abs(fs - FS) > 1e-6: sys.exit(f"[21_20b] STOP(G-ref): 参照の fs = {fs}")
+        if abs(fs - FS) > 1e-6: sys.exit(f"[24_02] STOP(G-ref): 参照の fs = {fs}")
         n = W.shape[0]
@@ -306,3 +311,3 @@
     u, p = os.environ.get("HINET_USER"), os.environ.get("HINET_PASS")
-    if not u or not p: sys.exit("[21_20b] STOP: 環境変数 HINET_USER・HINET_PASS が無い(ノートの セル 4 で入れる)")
+    if not u or not p: sys.exit("[24_02] STOP: 環境変数 HINET_USER・HINET_PASS が無い(ノートの セル 4 で入れる)")
     from HinetPy import Client
@@ -315,5 +320,5 @@
         client.select_stations(NET, names if names else None)
-        print(f"[21_20b] アカウントの局の選択を元に戻した({len(names) if names else '全局'})")
+        print(f"[24_02] アカウントの局の選択を元に戻した({len(names) if names else '全局'})")
     except Exception as e:                                  # 戻せなかった時は必ず表示する
-        print(f"[21_20b] 注意: アカウントの局の選択を戻せなかった({e})。Hi-net のサイトで確かめる。保存した選択: {sel_path}")
+        print(f"[24_02] 注意: アカウントの局の選択を戻せなかった({e})。Hi-net のサイトで確かめる。保存した選択: {sel_path}")
 
@@ -334,3 +339,3 @@
         t0 = jst_epoch(start); need = span * 60 * int(FS)
-        st_l, ep_l, wv_l = [], [], []
+        st_l, ep_l, wv_l, sc_l = [], [], [], []
         stat = dict(n_sta_files=0, bad_header=0, short=0, windows=0, windows_dropped=0)
@@ -345,6 +350,6 @@
             arr = np.stack([np.asarray(tr.data[:need], float) for tr in trs])
-            z, ks = zscore_windows(arr, dtype)
+            z, ks, sc = zscore_windows(arr, dtype)
             stat["windows"] += len(ks); stat["windows_dropped"] += need // WIN_N - len(ks)
             if not ks: continue
-            st_l += [s] * len(ks); ep_l += [t0 + WIN_S * k for k in ks]; wv_l.append(z)
+            st_l += [s] * len(ks); ep_l += [t0 + WIN_S * k for k in ks]; wv_l.append(z); sc_l.append(sc)
         if stat["n_sta_files"] == 0 or not wv_l:              # 何も取れなかった区切りは失敗として取り直す
@@ -354,3 +359,4 @@
         return dict(stations=np.array(st_l, dtype="U16"), epoch=np.array(ep_l, float),
-                    waves=(np.concatenate(wv_l) if wv_l else np.zeros((0, 3, WIN_N), dtype)), chan=chan, stat=stat)
+                    waves=(np.concatenate(wv_l) if wv_l else np.zeros((0, 3, WIN_N), dtype)), chan=chan, stat=stat,
+                    scale=(np.concatenate(sc_l) if sc_l else np.zeros((0, 3, 2))))
     finally:
@@ -364,3 +370,3 @@
     if lock.exists() and time.time() - lock.stat().st_mtime < LOCK_STALE_S:
-        sys.exit(f"[21_20b] STOP: 別の実行が動いている印 {lock}({lock.read_text().strip()})が 30 分以内に更新されている。"
+        sys.exit(f"[24_02] STOP: 別の実行が動いている印 {lock}({lock.read_text().strip()})が 30 分以内に更新されている。"
                  "Colab が切れた直後なら別の実行は無いので、セル 8b(--restore-selection --break-lock)を回してからセル 8 をもう一度")
@@ -386,8 +392,8 @@
     extra = [f.name for f in allf if f.name not in exp]
-    if extra: print(f"[21_20b] 注意: 今の計画に無い区切りのファイル {len(extra)} は使わない(例 {extra[:3]})")
+    if extra: print(f"[24_02] 注意: 今の計画に無い区切りのファイル {len(extra)} は使わない(例 {extra[:3]})")
     files = [f for f in allf if f.name in exp]
     bad = [f.name for f in files if not blk_ok(f)]
-    if bad: sys.exit(f"[21_20b] STOP: 読めない区切りのファイルが {len(bad)} ある(例 {bad[:3]})。消してから取り直す(セル 8)")
+    if bad: sys.exit(f"[24_02] STOP: 読めない区切りのファイルが {len(bad)} ある(例 {bad[:3]})。消してから取り直す(セル 8)")
     missing = sorted(exp - {f.name for f in files})
-    if not files: sys.exit("[21_20b] STOP: 区切りの結果が 1 つも無い")
+    if not files: sys.exit("[24_02] STOP: 区切りの結果が 1 つも無い")
     pres, chan = {}, {}
@@ -402,6 +408,6 @@
         if not (allow_missing and frac >= MIN_FETCHED):
-            sys.exit(f"[21_20b] STOP: 取っていない区切りが {len(missing)} ある(取れた割合 {frac:.3f}、例 {missing[:3]})。セル 8 を"
+            sys.exit(f"[24_02] STOP: 取っていない区切りが {len(missing)} ある(取れた割合 {frac:.3f}、例 {missing[:3]})。セル 8 を"
                      f"もう一度回してから --assemble。何度回しても取れない区切りだけが残り、取れた割合が {MIN_FETCHED} 以上なら "
                      "--allow-missing で続けてよい(事前に決めた規則。その区切りの地震は G-cover で覆えない地震として数える)")
-        print(f"[21_20b] 注意(--allow-missing): 取っていない区切り {len(missing)}(取れた割合 {frac:.3f} ≥ {MIN_FETCHED})で続ける: {missing}")
+        print(f"[24_02] 注意(--allow-missing): 取っていない区切り {len(missing)}(取れた割合 {frac:.3f} ≥ {MIN_FETCHED})で続ける: {missing}")
     done_iv = []
@@ -419,5 +425,5 @@
     keep = ok[:n_sta]
-    if not keep: sys.exit("[21_20b] STOP: 区切りの半分以上でデータがある局が 0")
-    if len(keep) < n_sta: print(f"[21_20b] 注意: 区切りの半分以上でデータがある局が {len(keep)} しかない(--n-sta {n_sta})")
-    print(f"[21_20b] 組み立て: 区切り {nb}(計画 {len(plan)})  使う局 {len(keep)}(最も遠い局 "
+    if not keep: sys.exit("[24_02] STOP: 区切りの半分以上でデータがある局が 0")
+    if len(keep) < n_sta: print(f"[24_02] 注意: 区切りの半分以上でデータがある局が {len(keep)} しかない(--n-sta {n_sta})")
+    print(f"[24_02] 組み立て: 区切り {nb}(計画 {len(plan)})  使う局 {len(keep)}(最も遠い局 "
           f"{haversine_km(ml, mo, cand_meta[keep[-1]]['lat'], cand_meta[keep[-1]]['lon']):.1f} km)")
@@ -425,3 +431,3 @@
     (OUT / "data" / "waves").mkdir(parents=True, exist_ok=True); (OUT / "data" / "catalog").mkdir(parents=True, exist_ok=True)
-    h5p = OUT / "data" / "waves" / ("osaka2018_100Hz_partial.h5" if partial else "osaka2018_100Hz.h5"); tmpp = h5p.with_suffix(".h5.part")
+    h5p = OUT / "data" / "waves" / ("nagano2014_100Hz_partial.h5" if partial else "nagano2014_100Hz.h5"); tmpp = h5p.with_suffix(".h5.part")
     if h5p.exists(): h5p.unlink()                              # 前の組み立ての結果は、ゲートに通るまで置かない
@@ -431,3 +437,3 @@
         z = np.load(f, allow_pickle=False); n_tot += int(np.isin(z["stations"], list(kset)).sum())
-    if n_tot == 0: sys.exit("[21_20b] STOP: 書く窓が 0")
+    if n_tot == 0: sys.exit("[24_02] STOP: 書く窓が 0")
     chunks = tuple(min(c, n) for c, n in zip(ref["chunks"], (n_tot, 3, WIN_N))) if ref.get("chunks") else None
@@ -440,2 +446,3 @@
         E = H.create_dataset("window_epoch", (n_tot,), dtype=np.dtype(ref["epoch_dtype"]))
+        WM = H.create_dataset("win_mean", (n_tot, 3), dtype=np.float64); WS = H.create_dataset("win_std", (n_tot, 3), dtype=np.float64)   # 24_02
         i = 0
@@ -446,7 +453,8 @@
             S[i:i + k] = np.array([s.encode() for s in z["stations"][m]]) if sfix else z["stations"][m].astype(object)
-            E[i:i + k] = z["epoch"][m]; i += k
+            E[i:i + k] = z["epoch"][m]; WM[i:i + k] = z["scale"][m][:, :, 0]; WS[i:i + k] = z["scale"][m][:, :, 1]; i += k
         H.attrs["channel_order"] = "UD,NS,EW"; H.attrs["n_samples"] = WIN_N; H.attrs["fs"] = FS
-        H.attrs["osaka2018_source"] = (f"NIED Hi-net (0101) continuous data via HinetPy, event blocks only; 21_20b_osaka2018_hinet_to_h5.py "
-                                    f"{VERSION}; per-window per-component z-score; window_epoch = JST wall clock as UTC epoch")
-    stp = OUT / "data" / "catalog" / ("stations_osaka2018_partial.csv" if partial else "stations_osaka2018.csv")
+        H.attrs["nagano2014_source"] = (f"NIED Hi-net (0101) continuous data via HinetPy, event blocks only; 24_02_nagano2014_hinet_to_h5.py "
+                                    f"{VERSION}; per-window per-component z-score (win_mean, win_std = the mean and std used; waves * win_std + win_mean restores the counts); "
+                                    f"window_epoch = JST wall clock as UTC epoch")
+    stp = OUT / "data" / "catalog" / ("stations_nagano2014_partial.csv" if partial else "stations_nagano2014.csv")
     if stp.exists(): stp.unlink()
@@ -518,11 +526,11 @@
     all_pass = G["ref_pass"] and G["dup_pass"] and G["cover_pass"] and G["clock_pass"]
-    rep = dict(script="21_20b_osaka2018_hinet_to_h5.py", version=VERSION, h5=str(h5p), n_windows=n_tot, stations=keep,
+    rep = dict(script="24_02_nagano2014_hinet_to_h5.py", version=VERSION, h5=str(h5p), n_windows=n_tot, stations=keep,
                presence={s: pres[s] for s in keep}, n_blocks=nb, n_blocks_planned=len(plan), n_blocks_missing=len(missing),
                missing_blocks=missing, allow_missing=bool(allow_missing), ref=ref, gates=G, all_gates_pass=bool(all_pass), partial=bool(partial))
-    json.dump(rep, open(OUT / "data" / ("21_20b_report_partial.json" if partial else "21_20b_report.json"), "w"), indent=1, default=str)
-    print(f"[21_20b] G-ref: 参照 dtype {ref['waves_dtype']}・z-score 確認 {'PASS' if ref['zcheck_pass'] else 'FAIL'}  出力の z-score 確認 "
+    json.dump(rep, open(OUT / "data" / ("24_02_report_partial.json" if partial else "24_02_report.json"), "w"), indent=1, default=str)
+    print(f"[24_02] G-ref: 参照 dtype {ref['waves_dtype']}・z-score 確認 {'PASS' if ref['zcheck_pass'] else 'FAIL'}  出力の z-score 確認 "
           f"{'PASS' if G['out_zcheck']['pass_'] else 'FAIL'}(最大 |平均| {G['out_zcheck']['max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
           f"{G['out_zcheck']['max_abs_std_minus_1']:.3g})")
-    print(f"[21_20b] G-dup: 重なり {G['dup']}  " + ("PASS" if G["dup"] == 0 else "FAIL"))
-    print(f"[21_20b] G-cover({G['cover_n_events']} 地震): Mj ≥ 1.5 の地震で 4 局以上が覆う割合 {G['cover_frac_ge4']:.3f}(覆う局の数の中央値 "
+    print(f"[24_02] G-dup: 重なり {G['dup']}  " + ("PASS" if G["dup"] == 0 else "FAIL"))
+    print(f"[24_02] G-cover({G['cover_n_events']} 地震): Mj ≥ 1.5 の地震で 4 局以上が覆う割合 {G['cover_frac_ge4']:.3f}(覆う局の数の中央値 "
           f"{G['cover_median_stations']:.0f})  " + ("PASS" if G["cover_frac_ge4"] >= COVER_OK else "注意" if G["cover_frac_ge4"] >= COVER_STOP else "FAIL"))
@@ -530,7 +538,7 @@
         cm = c["median_abs_resid_s"]
-        print(f"[21_20b] G-clock{'(本震)' if c['mainshock'] else '(他の地震)'} {c['origin_jst'][:22]} Mj {c['mj']}: 近い局 {c['n']} で、"
+        print(f"[24_02] G-clock{'(本震)' if c['mainshock'] else '(他の地震)'} {c['origin_jst'][:22]} Mj {c['mj']}: 近い局 {c['n']} で、"
               f"STA/LTA の立ち上がり − 震源距離/6.0 km/s の |差| の中央値 {'—' if cm is None else f'{cm:.2f}'} s  "
               + ("PASS" if c["pass_"] else ("FAIL" if c["mainshock"] or c["n"] >= 4 else "判定なし(立ち上がりが取れた局が 4 未満)")))
-    print(f"[21_20b] G-clock まとめ: " + ("PASS" if G["clock_pass"] else "FAIL"))
-    print(f"[21_20b] G-spec(記録だけ): 0.1–1 Hz / 1–20 Hz の力の比の中央値 参照 {G['band_ratio_ref']:.3g}・出力 {G['band_ratio_out']:.3g}"
+    print(f"[24_02] G-clock まとめ: " + ("PASS" if G["clock_pass"] else "FAIL"))
+    print(f"[24_02] G-spec(記録だけ): 0.1–1 Hz / 1–20 Hz の力の比の中央値 参照 {G['band_ratio_ref']:.3g}・出力 {G['band_ratio_out']:.3g}"
           f"(比 {rr:.2f})" + ("  注意: 3 倍以上違う(参照の h5 でフィルタをかけた可能性。記録だけで、止めずに先に進む。限界に書く)"
@@ -541,9 +549,9 @@
         why = [k for k, v in (("G-ref", G["ref_pass"]), ("G-dup", G["dup_pass"]), ("G-cover", G["cover_pass"]), ("G-clock", G["clock_pass"])) if not v]
-        if why == ["G-clock"]:                                 # 21_20: 表示の文だけ(止まり方は 21_04b v1.1 と同じ)
-            sys.exit(f"[21_20b] STOP(G-clock だけ): h5 は {failed.name}、局の表は {stp.name}.part にした。事前登録 21_20 の規則では "
-                     "G-clock は記録だけで、時刻は G-clock2(21_20d)で決める。セル 10 に、この 2 つのファイルを渡して進む(この出力を貼る)")
-        sys.exit(f"[21_20b] STOP({', '.join(why)}): h5 は {failed.name} にした(セル 10 には進まない。この出力を貼って相談)")
+        if why == ["G-clock"]:                                 # 21_20・24: 表示の文だけ(止まり方は 21_04b v1.1 と同じ)
+            sys.exit(f"[24_02] STOP(G-clock だけ): h5 は {failed.name}、局の表は {stp.name}.part にした。事前登録 24 の規則では "
+                     "G-clock は記録だけで、時刻は G-clock2(24_04d)で決める。セル N10 に、この 2 つのファイルを渡して進む(この出力を貼る)")
+        sys.exit(f"[24_02] STOP({', '.join(why)}): h5 は {failed.name} にした(セル 10 には進まない。この出力を貼って相談)")
     os.replace(tmpp, h5p); os.replace(stp.with_suffix(".csv.part"), stp)
     sfx = "_partial" if partial else ""
-    print(f"[21_20b] 出力: {h5p}(窓 {n_tot})  {OUT / 'data' / 'catalog' / f'stations_osaka2018{sfx}.csv'}  {OUT / 'data' / f'21_20b_report{sfx}.json'}"
+    print(f"[24_02] 出力: {h5p}(窓 {n_tot})  {OUT / 'data' / 'catalog' / f'stations_nagano2014{sfx}.csv'}  {OUT / 'data' / f'24_02_report{sfx}.json'}"
           + ("(煙試験の確認用。本番の組み立てはセル 9)" if partial else ""))
@@ -565,3 +573,3 @@
     cb = fig.colorbar(im, ax=ax, pad=0.01); cb.set_label("Fraction kept")
-    fig.tight_layout(); fig.savefig(PDFD / f"21_20b_coverage{suf}.pdf", bbox_inches="tight"); plt.close(fig)
+    fig.tight_layout(); fig.savefig(PDFD / f"24_02_coverage{suf}.pdf", bbox_inches="tight"); plt.close(fig)
     if sec:
@@ -581,3 +589,3 @@
         ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), frameon=False); ax.grid(alpha=0.3, axis="x")
-        fig.tight_layout(); fig.savefig(PDFD / f"21_20b_mainshock{suf}.pdf", bbox_inches="tight"); plt.close(fig)
+        fig.tight_layout(); fig.savefig(PDFD / f"24_02_mainshock{suf}.pdf", bbox_inches="tight"); plt.close(fig)
 
@@ -587,7 +595,7 @@
     ap = argparse.ArgumentParser()
-    ap.add_argument("--catalog", default=str(ROOT / "data" / "catalog" / "jma_osaka2018.csv"))
-    ap.add_argument("--summary", default=str(ROOT / "data" / "catalog" / "21_20a_osaka2018_catalog.json"))
+    ap.add_argument("--catalog", default=str(ROOT / "data" / "catalog" / "jma_nagano2014.csv"))
+    ap.add_argument("--summary", default=str(ROOT / "data" / "catalog" / "24_01_nagano2014_catalog.json"))
     ap.add_argument("--ref-h5", required=True, help="鳥取 2026 の tottori_all_100Hz.h5(形を写すため。読むだけ)")
-    ap.add_argument("--out", default=("/content/drive/MyDrive/ARGUS_osaka2018" if Path("/content/drive").exists()
-                                      else str(ROOT.parent / "ARGUS_osaka2018")))
+    ap.add_argument("--out", default=("/content/drive/MyDrive/ARGUS_nagano2014" if Path("/content/drive").exists()
+                                      else str(ROOT.parent / "ARGUS_nagano2014")))
     ap.add_argument("--tmp", default=("/content/hinet_tmp" if Path("/content").exists() else tempfile.gettempdir()))
@@ -600,3 +608,3 @@
     ap.add_argument("--restore-selection", action="store_true", help="アカウントの局の選択を保存した元の状態に戻すだけ(途中で落ちた時)")
-    ap.add_argument("--break-lock", action="store_true", help="--restore-selection と一緒に: 切れた実行の印(data/21_20b.lock)を消す")
+    ap.add_argument("--break-lock", action="store_true", help="--restore-selection と一緒に: 切れた実行の印(data/24_02.lock)を消す")
     a = ap.parse_args()
@@ -605,3 +613,3 @@
     tmp_root = Path(a.tmp); tmp_root.mkdir(parents=True, exist_ok=True)
-    if not Path(a.summary).exists(): sys.exit(f"[21_20b] STOP: {a.summary} が無い(21_20a を先に回す)")
+    if not Path(a.summary).exists(): sys.exit(f"[24_02] STOP: {a.summary} が無い(24_01 を先に回す)")
     summ = json.load(open(a.summary))
@@ -614,15 +622,15 @@
     tot_min = sum(s for _, s in plan)
-    print(f"[21_20b] {VERSION}  地震(Mj ≥ 1.5){len(org)} → 区切り {len(plan)}(分の合計 {tot_min}、最長 {max(s for _, s in plan)} 分)")
+    print(f"[24_02] {VERSION}  地震(Mj ≥ 1.5){len(org)} → 区切り {len(plan)}(分の合計 {tot_min}、最長 {max(s for _, s in plan)} 分)")
     rng = np.random.default_rng(7)
     ref = read_ref(a.ref_h5, rng)
-    print(f"[21_20b] 参照の h5: 窓 {ref['n_windows']}  /waves {ref['waves_dtype']}  /stations {ref['stations_dtype']}  "
+    print(f"[24_02] 参照の h5: 窓 {ref['n_windows']}  /waves {ref['waves_dtype']}  /stations {ref['stations_dtype']}  "
           f"/window_epoch {ref['epoch_dtype']}  chunks {ref['chunks']}  圧縮 {ref['compression']}  属性 {ref['attrs']}  "
           f"他のデータ {ref['other_datasets']}")
-    print(f"[21_20b] 参照の z-score の確認(無作為 {REF_NSAMPLE} 窓): 最大 |平均| {ref['zcheck_max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
+    print(f"[24_02] 参照の z-score の確認(無作為 {REF_NSAMPLE} 窓): 最大 |平均| {ref['zcheck_max_abs_mean']:.3g}・最大 |標準偏差 − 1| "
           f"{ref['zcheck_max_abs_std_minus_1']:.3g}  " + ("PASS" if ref["zcheck_pass"] else "FAIL")
           + f"  30 s 格子にそろう割合 {ref['grid30_frac']:.3f}(余り {ref['grid30_residues']})  0.1–1/1–20 Hz の力の比 {ref['band_ratio_median']:.3g}")
-    if not ref["zcheck_pass"]: sys.exit("[21_20b] STOP(G-ref): 参照の h5 が窓ごとの z-score に見えない(この行を貼って相談)")
+    if not ref["zcheck_pass"]: sys.exit("[24_02] STOP(G-ref): 参照の h5 が窓ごとの z-score に見えない(この行を貼って相談)")
     dt = np.dtype(ref["waves_dtype"])
-    plan_p = OUT / "data" / "21_20b_plan.json"
-    sel_p = OUT / "data" / "21_20b_initial_selection.json"
+    plan_p = OUT / "data" / "24_02_plan.json"
+    sel_p = OUT / "data" / "24_02_initial_selection.json"
 
@@ -630,13 +638,13 @@
         P = json.load(open(plan_p)) if plan_p.exists() else None
-        if P is None: sys.exit("[21_20b] STOP: 計画の 21_20b_plan.json が無い")
+        if P is None: sys.exit("[24_02] STOP: 計画の 24_02_plan.json が無い")
         assemble(OUT, PDFD, ref, summ, rows, P["candidates"], a.n_sta, plan, partial=a.partial, allow_missing=a.allow_missing); return
 
-    lock = OUT / "data" / "21_20b.lock"
+    lock = OUT / "data" / "24_02.lock"
     if a.restore_selection:
         if a.break_lock and lock.exists():
-            print(f"[21_20b] 切れた実行の印を消した: {lock.read_text().strip()}"); lock.unlink()
+            print(f"[24_02] 切れた実行の印を消した: {lock.read_text().strip()}"); lock.unlink()
         check_lock(lock)                                       # 動いている実行があれば、その選択を変えない
-        if not sel_p.exists(): sys.exit(f"[21_20b] STOP: 保存した選択 {sel_p} が無い")
+        if not sel_p.exists(): sys.exit(f"[24_02] STOP: 保存した選択 {sel_p} が無い")
         restore_selection(hinet_client(), sel_p); return
-    if not shutil.which("win2sac_32") and not a.dry_run: sys.exit("[21_20b] STOP: win2sac_32 が PATH に無い(ノートの セル 3)")
+    if not shutil.which("win2sac_32") and not a.dry_run: sys.exit("[24_02] STOP: win2sac_32 が PATH に無い(ノートの セル 3)")
     client = hinet_client()
@@ -646,3 +654,3 @@
     stl = [s for s in stl if s.latitude is not None and s.longitude is not None and s.elevation is not None]
-    if len(stl) < n0: print(f"[21_20b] 緯度・経度・標高のどれかが無い局 {n0 - len(stl)} は候補から外した")
+    if len(stl) < n0: print(f"[24_02] 緯度・経度・標高のどれかが無い局 {n0 - len(stl)} は候補から外した")
     stl.sort(key=lambda s: haversine_km(ml, mo, s.latitude, s.longitude))
@@ -651,3 +659,3 @@
                           dist_km=float(haversine_km(ml, mo, s.latitude, s.longitude))) for s in cands}
-    print(f"[21_20b] 候補局 {len(cands)}(本震から {cmeta[cands[0].name]['dist_km']:.1f}〜{cmeta[cands[-1].name]['dist_km']:.1f} km): "
+    print(f"[24_02] 候補局 {len(cands)}(本震から {cmeta[cands[0].name]['dist_km']:.1f}〜{cmeta[cands[-1].name]['dist_km']:.1f} km): "
           + " ".join(s.name for s in cands))
@@ -657,6 +665,6 @@
     free = shutil.disk_usage(OUT).free / 1e9
-    print(f"[21_20b] 置き場所の見込み: 区切りのファイル約 {gb:.1f} GB + 組み立てた h5 約 {gb * a.n_sta / len(cands):.1f} GB"
+    print(f"[24_02] 置き場所の見込み: 区切りのファイル約 {gb:.1f} GB + 組み立てた h5 約 {gb * a.n_sta / len(cands):.1f} GB"
           f"(Drive の空き {free:.0f} GB。ここに出るのは Colab から見た空きで、Drive の契約の上限とは違うことがある)")
     if a.dry_run:
-        print(f"[21_20b] 計画だけ(--dry-run): {plan_p}。1 区切りに 30 s かかるとして約 {len(plan) * 30 / 3600:.1f} 時間、"
+        print(f"[24_02] 計画だけ(--dry-run): {plan_p}。1 区切りに 30 s かかるとして約 {len(plan) * 30 / 3600:.1f} 時間、"
               f"60 s なら約 {len(plan) * 60 / 3600:.1f} 時間(煙試験で測る)")
@@ -670,3 +678,3 @@
             json.dump(dict(saved_utc=datetime.now(timezone.utc).isoformat(), stations=names0), open(sel_p, "w"), indent=1)
-            print(f"[21_20b] アカウントの今の局の選択を保存した({len(names0) if names0 else '全局'}): {sel_p}")
+            print(f"[24_02] アカウントの今の局の選択を保存した({len(names0) if names0 else '全局'}): {sel_p}")
         for f in (OUT / "data" / "blocks").glob("*.tmp"): f.unlink()          # 前に途中で切れた書きかけ
@@ -675,6 +683,6 @@
             if f.exists() and not blk_ok(f):
-                print(f"[21_20b] 読めない区切りのファイル {f.name} を消して取り直す"); f.unlink()
+                print(f"[24_02] 読めない区切りのファイル {f.name} を消して取り直す"); f.unlink()
         todo = [(b, s) for b, s in plan if not blk_done(OUT, b, s)]
         need = (sum(s for _, s in todo) * 2 * len(cands) * 3 * WIN_N * dt.itemsize / 1e9) + gb * a.n_sta / len(cands)
-        if free < 1.1 * need: sys.exit(f"[21_20b] STOP: 置き場所が足りない見込み(残りの区切りと h5 で約 {need:.1f} GB、空き {free:.0f} GB)")
+        if free < 1.1 * need: sys.exit(f"[24_02] STOP: 置き場所が足りない見込み(残りの区切りと h5 で約 {need:.1f} GB、空き {free:.0f} GB)")
         if a.max_blocks:                                     # 煙試験: 本震の区間 [−10 s, +45 s] に掛かる区切りを最初に(G-clock を早く確かめる)
@@ -685,6 +693,6 @@
         n_done = sum(1 for b, s in plan if blk_done(OUT, b, s))
-        print(f"[21_20b] 取る区切り {len(todo)}(済み {n_done}/{len(plan)})")
+        print(f"[24_02] 取る区切り {len(todo)}(済み {n_done}/{len(plan)})")
         names = [s.name for s in cands]
         if not todo:
-            print("[21_20b] 取る区切りが無い(全部済み)。次はセル 9(--assemble)"); return
+            print("[24_02] 取る区切りが無い(全部済み)。次はセル 9(--assemble)"); return
         max_span = max(1, min(60, 12000 // (3 * len(names))))
@@ -697,4 +705,4 @@
         if not got or not set(got) <= set(names):
-            sys.exit(f"[21_20b] STOP: アカウントの局の選択が候補にならなかった(選ばれた局 {len(got)})。全局のまま取ると何倍も時間がかかる")
-        if set(got) != set(names): print(f"[21_20b] 注意: 選べた局 {len(got)} が候補 {len(names)} より少ない(無い局: {sorted(set(names) - set(got))[:10]})")
+            sys.exit(f"[24_02] STOP: アカウントの局の選択が候補にならなかった(選ばれた局 {len(got)})。全局のまま取ると何倍も時間がかかる")
+        if set(got) != set(names): print(f"[24_02] 注意: 選べた局 {len(got)} が候補 {len(names)} より少ない(無い局: {sorted(set(names) - set(got))[:10]})")
         for i, (b, s) in enumerate(todo):
@@ -719,3 +727,3 @@
                 print(f"    区切り {b:%Y-%m-%d %H:%M} ({s} 分) を {len(tries)} 回とも取れなかった(飛ばす。次に回すと取り直す)")
-                if fails >= 3: sys.exit("[21_20b] STOP: 3 つの区切りで続けて取れなかった(Hi-net の状態を確かめて、もう一度回すと続きから)")
+                if fails >= 3: sys.exit("[24_02] STOP: 3 つの区切りで続けて取れなかった(Hi-net の状態を確かめて、もう一度回すと続きから)")
                 continue
@@ -725,3 +733,3 @@
                 np.savez(fh, stations=res["stations"], epoch=res["epoch"], waves=res["waves"], chan=json.dumps(res["chan"]),
-                         stat=json.dumps(res["stat"]))
+                         stat=json.dumps(res["stat"]), scale=res["scale"])
             os.replace(part, dst)
@@ -736,3 +744,3 @@
     left = sum(1 for b, s in plan if not blk_done(OUT, b, s))
-    print(f"[21_20b] 終わり: 残りの区切り {left}/{len(plan)}" + ("(全部済んだら --assemble)" if left == 0 else "(もう一度回すと続きから)"))
+    print(f"[24_02] 終わり: 残りの区切り {left}/{len(plan)}" + ("(全部済んだら --assemble)" if left == 0 else "(もう一度回すと続きから)"))
 
```

## 24_03_nagano2014_realpick_cache_colab.py ← 21_20c_osaka2018_realpick_cache_colab.py

```diff
--- osaka/21_20c_osaka2018_realpick_cache_colab.py	2026-11-02 00:09:04.448443105 +0000
+++ nagano/frz/24_03_nagano2014_realpick_cache_colab.py	2026-11-15 05:21:00.093896453 +0000
@@ -2,22 +2,17 @@
 # =============================================================================
-# Script : 21_20c_osaka2018_realpick_cache_colab.py  (v1)
-#          [大阪府北部 2018 の h5(21_20b)と気象庁の震源(21_20a)から、PhaseNet で P・S を測り、ARGUS のキャッシュ
-#           (tottori_parsed_realpick_osaka2018_m15.pt)を作る。検測・QC・局の選び方・組み立て・振幅整合は 15_01c v3.3 と同じ計算]
-# Project: ARGUS(新生)— 3 つ目の余震系列での確認(21_20)の入力の 3 つ目
-# 派生元 : 15_01c_tottori_realpick_cache_colab.py v3.3(SHA-256 e407f88b7345e689f0c989d2c95ecf2e1bfec1b857e09b4ab8ada44f2354258e)。
-#          検測・QC・組み立て・振幅整合・出力の中身は v3.3 と 1 字も変えていない(DIFF_LOG.md の差分で確かめられる)。変えたのは次だけ:
-#          (1) この冒頭の説明(下の「15_01c v3.3 の説明」は元のまま残す)
-#          (2) 出力の置き場所の既定: ARGUS_tottori → ARGUS_osaka2018(Colab では --base で必ず渡す)
-#          (3) --jma・--stations・--box を必ず渡す引数にした(既定が鳥取 2026 の CSV と西鳥取の箱なので、渡し忘れると鳥取のまま
-#              回ってしまう。それを防ぐため。値の渡し方は 15_01c v3.3 と同じ)
-#          (4) 表示の先頭 [15_01c] → [21_20c]、報告の script_version を "21_20c v1 (computation identical to 15_01c v3.3)" に、
-#              図の題 "Tottori 2026" → "Northern Osaka 2018"、最後の表示の Mac のコピー先(--tag に osaka2018 があれば
-#              data/osaka2018_processed/)、振幅整合の表示の「鳥取absmax中央値」→「大阪absmax中央値」
-#          出力の名前の決まり(tottori_parsed_realpick{tag}.pt・data/tottori_processed/・15_01c_build_report{tag}.json・
-#          15_01c_tottori_picks_qc{tag}.pdf)は、21_04 が使ったものと同じ形にするため変えていない(--tag _osaka2018_m15 で分ける)。
-#          報告の script_sha256 はこのファイルの SHA-256 になる(事前登録 21_20 の凍結の表と照らす)。
-# 大阪府北部 2018 の実行(ノート 21_20_osaka2018_colab.ipynb の セル 10・11。手順は COLAB_STEPS_JA.md):
-#   !python 21_20c_osaka2018_realpick_cache_colab.py --h5 <osaka2018_100Hz.h5(または _FAILED.h5)> --jma <jma_osaka2018.csv>
-#      --stations <stations_osaka2018.csv(または .csv.part)> --min-mag 1.5 --box <21_20a の JSON の box 4 つ>
-#      --base /content/ARGUS_osaka2018 --tag _osaka2018_m15 [--max-events 10 で煙試験。その時は --tag _osaka2018_smoke]
+# Script : 24_03_nagano2014_realpick_cache_colab.py  (v1)
+#          [長野県北部 2014 の h5(24_02)と気象庁の震源(24_01)から、PhaseNet で P・S を測り、ARGUS のキャッシュ
+#           (tottori_parsed_realpick_nagano2014_m15.pt)を作る。検測・QC・局の選び方・組み立て・振幅整合は 15_01c v3.3 と同じ計算]
+# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の 3 つ目
+# 派生元 : 21_20c_osaka2018_realpick_cache_colab.py v1(SHA-256 7b938b944003d99fcad7df188792e8e8eb95c71b07f1a1223bffad6671d04cf0)。
+#          検測・QC・組み立て・振幅整合・出力の中身は 21_20c v1(= 15_01c v3.3 と同じ計算)と 1 字も変えていない(DIFF_LOG_24.md)。
+#          変えたのは次だけ: (1) この冒頭の説明 (2) 出力の置き場所の既定 ARGUS_osaka2018 → ARGUS_nagano2014(Colab では --base で必ず渡す)
+#          (3) 引数の説明の文 (4) 表示の先頭 [24_03] → [24_03]、報告の script_version、図の題、最後の表示の Mac のコピー先
+#          (--tag に nagano2014 があれば data/nagano2014_processed/)、振幅整合の表示の「大阪」→「長野」。
+#          24_02 の h5 には win_mean・win_std も入っているが、このスクリプトは読まない(waves だけを読む。21_20c と同じ)。
+#          このキャッシュの後に 24_03h(R1: 発生の 15 s 前〜5 s 後に別の地震がある地震を除く)を必ず当てる(事前登録 24 の 3 節)。
+# 長野県北部 2014 の実行(ノート 24_nagano2014_colab.ipynb の セル N10・N11):
+#   !python 24_03_nagano2014_realpick_cache_colab.py --h5 <nagano2014_100Hz.h5(または _FAILED.h5)> --jma <jma_nagano2014.csv>
+#      --stations <stations_nagano2014.csv(または .csv.part)> --min-mag 1.5 --box <24_01 の JSON の box 4 つ>
+#      --base /content/ARGUS_nagano2014 --tag _nagano2014_m15 [--max-events 10 で煙試験。その時は --tag _nagano2014_smoke]
 #
@@ -121,4 +116,4 @@
 
-BASE = Path("/content/drive/MyDrive/ARGUS_osaka2018") \
-       if Path("/content/drive").exists() else Path(".") / "ARGUS_osaka2018"     # 21_20c: 既定の置き場所(--base で渡す)
+BASE = Path("/content/drive/MyDrive/ARGUS_nagano2014") \
+       if Path("/content/drive").exists() else Path(".") / "ARGUS_nagano2014"     # 24_03: 既定の置き場所(--base で渡す)
 PDFD = BASE / "PDF"
@@ -145,5 +140,5 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--jma", required=True, help="21_20a の jma_osaka2018.csv(21_20c: 必ず渡す)")
-ap.add_argument("--stations", required=True, help="21_20b の stations_osaka2018.csv(21_20c: 必ず渡す)")
-ap.add_argument("--h5", required=True, help="21_20b の osaka2018_100Hz.h5 のパス")
+ap.add_argument("--jma", required=True, help="24_01 の jma_nagano2014.csv(24_03: 必ず渡す)")
+ap.add_argument("--stations", required=True, help="24_02 の stations_nagano2014.csv(24_03: 必ず渡す)")
+ap.add_argument("--h5", required=True, help="24_02 の nagano2014_100Hz.h5 のパス")
 ap.add_argument("--knet-cache", default="", help="(任意)あればフル統計を開示")
@@ -166,6 +161,6 @@
                 metavar=("LAT0", "LAT1", "LON0", "LON1"),
-                help="21_20a の JSON の box(21_20c: 必ず渡す。西鳥取の既定は外した)")
+                help="24_01 の JSON の box(24_03: 必ず渡す。西鳥取の既定は外した)")
 ap.add_argument("--tag", default="", help="出力の名前に付ける印(例 _m15)。v3.1 で追加")
 ap.add_argument("--overwrite-canon", action="store_true", help="--tag 無しで既存の正本を上書きする時だけ付ける。v3.2 で追加")
-ap.add_argument("--base", default="", help="出力の置き場所(既定は Drive の ARGUS_osaka2018)。v3.3 で追加")
+ap.add_argument("--base", default="", help="出力の置き場所(既定は Drive の ARGUS_nagano2014)。v3.3 で追加")
 args = ap.parse_args()
@@ -176,5 +171,5 @@
 if abs(args.min_mag - 2.0) > 1e-9 and args.tag == "":
-    raise SystemExit("[21_20c] STOP: --min-mag が 2.0 以外の時は --tag(例 _m15)を付ける(正本を上書きしないため)")
+    raise SystemExit("[24_03] STOP: --min-mag が 2.0 以外の時は --tag(例 _m15)を付ける(正本を上書きしないため)")
 if args.tag == "" and (OUTD / "tottori_parsed_realpick.pt").exists() and not args.overwrite_canon:
-    raise SystemExit("[21_20c] STOP: 正本 tottori_parsed_realpick.pt が既にある。--tag を付けて回す"
+    raise SystemExit("[24_03] STOP: 正本 tottori_parsed_realpick.pt が既にある。--tag を付けて回す"
                      "(正本を作り直す時だけ --overwrite-canon)")
@@ -277,3 +272,3 @@
     PN_MODEL.eval()
-    print("[21_20c] PhaseNet ('original') 読込完了")
+    print("[24_03] PhaseNet ('original') 読込完了")
 
@@ -307,3 +302,3 @@
 # ================================================================ 入力読み込み
-print(f"[21_20c] JMAカタログ: {args.jma}")
+print(f"[24_03] JMAカタログ: {args.jma}")
 import csv as _csv
@@ -330,5 +325,5 @@
 if args.max_events: cat = cat[:args.max_events]
-print(f"[21_20c] 対象イベント: {len(cat)} (M>={args.min_mag}, box={args.box}, "
+print(f"[24_03] 対象イベント: {len(cat)} (M>={args.min_mag}, box={args.box}, "
       f"JST→UTC変換済み, h5窓引き={args.h5_time_base}基準, 欠損行スキップ {n_badrow})")
-if not cat: sys.exit("[21_20c] STOP: 対象イベント0件")
+if not cat: sys.exit("[24_03] STOP: 対象イベント0件")
 
@@ -339,3 +334,3 @@
                                        float(row["elevation"]))
-print(f"[21_20c] 観測点: {len(sta_meta)}局 ({Path(args.stations).name})")
+print(f"[24_03] 観測点: {len(sta_meta)}局 ({Path(args.stations).name})")
 
@@ -350,3 +345,3 @@
     nan_frac = float(np.isnan(k_snr).mean())
-    print(f"[21_20c] K-NET参照: {len(kevs)}ev  absmax中央値={KNET_ABSMAX_REF:.2f}  "
+    print(f"[24_03] K-NET参照: {len(kevs)}ev  absmax中央値={KNET_ABSMAX_REF:.2f}  "
           f"snr分布(NaN率{nan_frac:.1%}; 13_34rpではNaN→0) "
@@ -357,3 +352,3 @@
     KNET_ABSMAX_REF = float(args.knet_absmax_ref)
-    print(f"[21_20c] K-NET参照: --knet-absmax-ref={KNET_ABSMAX_REF} を使用 "
+    print(f"[24_03] K-NET参照: --knet-absmax-ref={KNET_ABSMAX_REF} を使用 "
           f"(Mac実測 2026-10-15、キャッシュ本体は不要)")
@@ -367,3 +362,3 @@
 n_samp_h5 = int(H5.attrs.get("n_samples", 3000))
-print(f"[21_20c] h5: channel_order={ch_order_h5}  n_samples={n_samp_h5}")
+print(f"[24_03] h5: channel_order={ch_order_h5}  n_samples={n_samp_h5}")
 st_raw = H5["stations"][:]
@@ -380,6 +375,6 @@
         ep_sorted, row_sorted = z["ep"], z["row"]
-    print(f"[21_20c] 窓索引をキャッシュから読込: {idx_path.name}" if _idx_ok
-          else f"[21_20c] 窓索引 {idx_path.name} は今の h5 のものでない(指紋が無いか違う)ので作り直す")
+    print(f"[24_03] 窓索引をキャッシュから読込: {idx_path.name}" if _idx_ok
+          else f"[24_03] 窓索引 {idx_path.name} は今の h5 のものでない(指紋が無いか違う)ので作り直す")
 if not _idx_ok:
-    print("[21_20c] 窓索引を構築中(初回のみ・数分)…")
+    print("[24_03] 窓索引を構築中(初回のみ・数分)…")
     order = np.lexsort((ep_raw, st_arr))
@@ -391,3 +386,3 @@
              ep=ep_sorted, row=row_sorted, fp=np.array(_fp))
-    print(f"[21_20c] 窓索引を保存: {idx_path.name} ({len(sta_names)}局)")
+    print(f"[24_03] 窓索引を保存: {idx_path.name} ({len(sta_names)}局)")
 del st_raw, ep_raw, st_arr
@@ -588,3 +583,3 @@
         ev["waveforms"] = ev["waveforms"] * amp_fac
-    print(f"[21_20c] 振幅整合: 大阪absmax中央値 {med:.3e} → ×{amp_fac:.3e} で "
+    print(f"[24_03] 振幅整合: 長野absmax中央値 {med:.3e} → ×{amp_fac:.3e} で "
           f"K-NET中央値 {KNET_ABSMAX_REF:.2f} に一致(一括係数・相対振幅保存)")
@@ -598,3 +593,3 @@
 import hashlib
-rep = dict(script_version="21_20c v1 (computation identical to 15_01c v3.3)", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
+rep = dict(script_version="24_03 v1 (computation identical to 15_01c v3.3 and 21_20c v1)", script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            args={k: str(v) for k, v in vars(args).items()}, stats=stats,
@@ -624,3 +619,3 @@
 print("\n" + "=" * 72)
-print(f"[21_20c] 完了: {out}")
+print(f"[24_03] 完了: {out}")
 print(f"  採用 {stats['n_ev']} / 対象 {len(cat)}  (セグメント不足 {stats['no_seg']}, "
@@ -649,3 +644,3 @@
     ax[0].set_xlabel("Hypocentral distance (km)"); ax[0].set_ylabel("S–P (s)")
-    ax[0].set_title(f"Northern Osaka 2018: measured S–P vs distance (n={len(SPn)})",
+    ax[0].set_title(f"Northern Nagano 2014: measured S–P vs distance (n={len(SPn)})",
                     fontsize=10.5)
@@ -660,3 +655,3 @@
     print(f"図: {PDFD}/15_01c_tottori_picks_qc{args.tag}.pdf")
-print(f"\n[21_20c] 出力全文+JSONを貼ってください。{out.name} をMacの SWIFT/data/"
-      f"{'osaka2018_processed' if 'osaka2018' in args.tag else 'tottori_processed'}/ にコピーしてください。")
+print(f"\n[24_03] 出力全文+JSONを貼ってください。{out.name} をMacの SWIFT/data/"
+      f"{'nagano2014_processed' if 'nagano2014' in args.tag else 'tottori_processed'}/ にコピーしてください。")
```

## 24_03h_nagano2014_overlap_exclusion.py ← 21_20h_osaka2018_overlap_exclusion.py

```diff
--- osaka_a04/21_20h_osaka2018_overlap_exclusion.py	2026-11-12 15:55:41.634538341 +0000
+++ nagano/frz/24_03h_nagano2014_overlap_exclusion.py	2026-11-15 05:21:00.093243709 +0000
@@ -2,41 +2,36 @@
 # =============================================================================
-# Script : 21_20h_osaka2018_overlap_exclusion.py  (v1)
-#          [大阪府北部 2018 のキャッシュ(21_20c の本番)から、「発生の 15 s 前〜5 s 後に別の地震がある地震」を除いたキャッシュを作る。
-#           使うのは気象庁の震源一覧の発生時刻だけ。震源の位置(正解)・波形・検測の残り・位置の計算は一切使わない]
-# Project: ARGUS(新生)— 21_20(大阪府北部 2018 での確認)と 22_04(信頼の切り替え)の、事前登録の変更の記録 04 で足した規則を当てる
+# Script : 24_03h_nagano2014_overlap_exclusion.py  (v1)
+#          [長野県北部 2014 のキャッシュ(24_03 の本番)から、「発生の 15 s 前〜5 s 後に別の地震がある地震」を除いたキャッシュを作る(規則 R1)。
+#           使うのは気象庁の震源一覧の発生時刻と Mj だけ。震源の位置(正解)・波形・検測の残り・位置の計算は一切使わない]
+# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)。大阪(21_20)で変更の記録 04 として後から足した規則を、
+#          この系列では長野の波形を開く前に、事前登録の規則として最初から入れる
+# 派生元 : 21_20h_osaka2018_overlap_exclusion.py v1(SHA-256 32a383a04dd7959f9ed7897ed8e9c89b3ab6fba2f5977e119f5375169950b52f)。
+#          規則 R1〜R4・自分の行の見つけ方(24_03 = 21_20c と同じ読み方の時刻(0.1 s で切り捨て)と Mj が一致する、ただ 1 つの行)・
+#          窓 [−15.0 s, +5.0 s]・除かない地震(本震と、24_02 の G-clock の地震)・止める条件は 21_20h v1 と同じ。変えたのは次だけ(DIFF_LOG_24.md):
+#          (1) 入力のキャッシュの SHA-256 の照合を外した(21_20h は止めた後の作り直しで、元のキャッシュが決まっていた。24 では 24_03 の
+#              本番の出力をそのまま受け、SHA-256 を記録に書く)
+#          (2) 21_20g の出力を読む記述(--g-json)を外した(長野には 21_20g が無い)
+#          (3) 本震の想定 MAIN_UTC = 2014-11-22 13:08:17.9 UTC(24_00 の表示の 22:08:17.90 JST、± 60 s、Mj ≥ 6.0)、出力の名前
+#              (tottori_parsed_realpick_nagano2014_m15_r1.pt・data/24_03h_overlap_exclusion.json)、表示 [24_03h]、記録の文
 #
-# なぜ必要か(変更の記録 04 の 1〜2 節):
-#   21_20d(G-clock2)の (d) 時間ごとが、2018-06-19 21 時台 JST だけで FAIL し、事前登録 5.3 節どおり 21_20・21_20f を開かずに止めた
-#   (commit 3839889)。読むだけの診断 21_20g で、原因は時計ではなく検測の取り違えと分かった。21:00:38.20 の Mj 1.9 が、
-#   その 6.5 s 前の 21:00:31.70 の Mj 2.2 の P を拾っていた(共通の 14 局で P の時刻が一致)。21_20c の検測は
-#   「発生の 10 s 前から、確率 0.3 以上で一番早い P」を取るので、発生の少し前に別の地震があると、その地震の P を取りうる。
-#   検測器は 21_02・21_04 と同じにしておきたい(3 つ目の系列で同じ規則を確かめるため)。そこで検測器は変えず、取り違えが
-#   起きうる地震(発生の近くに別の地震がある地震)を、試験からも過去の地震の一覧からも除く。
-#
-# 規則(変更の記録 04 の 3 節。この版の SHA-256 を、回す前に記録 04 に書いて push する):
-#   R1. 気象庁の震源一覧(jma_osaka2018.csv、21_20a の出力、全ての規模)で、キャッシュの地震の自分の行(21_20c と同じ読み方の
-#       時刻 = 0.1 s で切り捨て と Mj が一致する、ただ 1 つの行)の発生時刻(0.01 s)から dt = [−15.0 s, +5.0 s] の範囲に、
-#       自分の行以外の地震が 1 つでもあれば、その地震を除く。窓の幅は 21_20g の調べ方と同じ(21_20g は 0.1 s のキャッシュの時刻から測った)。
-#   R2. 除かないもの: 本震(キャッシュで Mj 最大。21_20 の分け方と G-untouched に要る)と、21_20b の G-clock の 4 地震
-#       (21_20d の (e) に要る。1 回目の 21_20d で 4 地震とも PASS。本震も G-clock の 4 地震の 1 つなので、合わせて 4 地震)。
-#       この 4 地震のどれかが試験の候補(本震 + 72 h より後の
-#       Mj < 2.0)なら止める。
-#   R3. 除いた後の試験の候補が 30 未満なら、キャッシュを書かずに止める(既存の MIN_TEST = 30。21_20 は回さず、INCONCLUSIVE と報告する)。
+# 規則(事前登録 24 の 3 節):
+#   R1. 気象庁の震源一覧(jma_nagano2014.csv、24_01 の出力、全ての規模)で、キャッシュの地震の自分の行の発生時刻(0.01 s)から
+#       dt = [−15.0 s, +5.0 s] の範囲に、自分の行以外の地震が 1 つでもあれば、その地震を除く。
+#   R2. 除かないもの: 本震(キャッシュで Mj 最大)と、24_02 の G-clock の地震(24_04d の (e) に要る)。このどれかが試験の候補なら止める。
+#   R3. 除いた後の試験の候補が 30 未満なら、キャッシュを書かずに止める(既存の MIN_TEST = 30。24_05 は回さず INCONCLUSIVE と報告する)。
 #   R4. キャッシュの地震の並びと中身(辞書)は 1 字も変えず、除く地震を抜くだけ。
+#   24_00 の見積もり(カタログだけ): 試験の候補 81 → R1 の後 79。キャッシュでは P を測れない地震の分だけ少なくなりうる。
 #
-# 止める条件(STOP): 入力のキャッシュの SHA-256 が 21_20c の本番(b9162a9d…aa83)と違う・キャッシュの地震が震源一覧に
-#   見つからないか 2 行以上ある・本震が想定と違う・上の R2・R3(R2・R3 で止まった時も、記録の JSON は書く)。
+# 止める条件(STOP): キャッシュ・震源一覧・報告が無い・キャッシュの地震が震源一覧に見つからないか 2 行以上ある・本震が想定と違う・
+#   R2・R3(R2・R3 で止まった時も、記録の JSON は書く)。
 #
 # 出力(--out の下):
-#   data/tottori_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt  … 除いた後のキャッシュ(21_20d・21_20e・21_20・21_20f・22_04 に --cache で渡す)
-#   data/21_20h_overlap_exclusion.json                                 … 規則・入力と出力の SHA-256・数・除いた地震の一覧
-#   (--g-json に 21_20g の出力を渡すと、21_20g で 1 s より大きくずれた地震のうち何個が除かれるかを記述として足す。判定には使わない)
+#   data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt  … 除いた後のキャッシュ(24_04d・24_04e・24_07・24_05・24_06f・24_06g に渡す)
+#   data/24_03h_overlap_exclusion.json                                … 規則・入力と出力の SHA-256・数・除いた地震の一覧
 #
-# Usage(Colab。手順は 21_20h_COLAB_STEPS_JA.md のセル H1〜H6):
-#   !python /content/drive/MyDrive/ARGUS/src/21_20h_osaka2018_overlap_exclusion.py \
-#       --cache /content/drive/MyDrive/ARGUS_osaka2018/data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt \
-#       --catalog /content/drive/MyDrive/ARGUS/data/catalog/jma_osaka2018.csv \
-#       --report /content/drive/MyDrive/ARGUS_osaka2018/data/21_20b_report.json \
-#       --g-json /content/drive/MyDrive/ARGUS_osaka2018/data/21_20g_clock_hour_diagnose.json \
-#       --out /content/ARGUS_osaka2018_a04
+# Usage(Colab。ノート 24_nagano2014_colab.ipynb の セル N12):
+#   !python /content/drive/MyDrive/ARGUS/src/24_03h_nagano2014_overlap_exclusion.py \
+#       --cache /content/ARGUS_nagano2014/data/tottori_processed/tottori_parsed_realpick_nagano2014_m15.pt \
+#       --catalog /content/drive/MyDrive/ARGUS/data/catalog/jma_nagano2014.csv \
+#       --report /content/drive/MyDrive/ARGUS_nagano2014/data/24_02_report.json --out /content/ARGUS_nagano2014
 # =============================================================================
@@ -50,17 +45,15 @@
 VERSION = "v1"
-TAG = "[21_20h]"
+TAG = "[24_03h]"
 PRE_S, POST_S = 15.0, 5.0                                # R1(21_20g と同じ窓)
 POOL_H, FRESH_MAX_MAG, MIN_TEST = 72.0, 2.0, 30            # 21_20 v1 と同じ値
-MAIN_UTC = datetime(2018, 6, 17, 22, 58, 30)               # 21_20 v1 と同じ(07:58 JST の 1 分の真ん中、± 60 s)
+MAIN_UTC = datetime(2014, 11, 22, 13, 8, 17, 900000)      # 24: 24_00 の表示の 22:08:17.90 JST(± 60 s)
 GCLOCK_MATCH_S = 1.5                                       # 21_20d v1 の (e) と同じ探し方
-EXPECT_CACHE_SHA = "b9162a9d8aab2747540de6a67006478349221e774c7c0a9f26e090cf1922aa83"   # 21_20c の本番(停止の記録)
-OUT_CACHE = "data/tottori_processed/tottori_parsed_realpick_osaka2018_m15_a04.pt"
-OUT_JSON = "data/21_20h_overlap_exclusion.json"
-
-ap = argparse.ArgumentParser(description="21_20h: 発生の近くに別の地震がある地震を除いたキャッシュを作る(変更の記録 04)")
-ap.add_argument("--cache", required=True, help="21_20c の本番のキャッシュ(tottori_parsed_realpick_osaka2018_m15.pt)")
-ap.add_argument("--catalog", required=True, help="jma_osaka2018.csv(21_20a の出力、全ての規模、時刻は日本時間)")
-ap.add_argument("--report", required=True, help="21_20b の報告(data/21_20b_report.json。G-clock の 4 地震を読む)")
-ap.add_argument("--g-json", default="", help="任意: 21_20g の出力 JSON(記述だけに使う)")
-ap.add_argument("--out", required=True, help="出力の根(21_20d・21_20e の --base にもこの場所を使う)")
+OUT_CACHE = "data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt"
+OUT_JSON = "data/24_03h_overlap_exclusion.json"
+
+ap = argparse.ArgumentParser(description="24_03h: 発生の近くに別の地震がある地震を除いたキャッシュを作る(事前登録 24 の R1)")
+ap.add_argument("--cache", required=True, help="24_03 の本番のキャッシュ(tottori_parsed_realpick_nagano2014_m15.pt)")
+ap.add_argument("--catalog", required=True, help="jma_nagano2014.csv(24_01 の出力、全ての規模、時刻は日本時間)")
+ap.add_argument("--report", required=True, help="24_02 の報告(data/24_02_report.json。G-clock の地震を読む)")
+ap.add_argument("--out", required=True, help="出力の根(24_04d・24_04e の --base にもこの場所を使う)")
 a = ap.parse_args()
@@ -94,4 +87,2 @@
 print(f"{TAG} 入力のキャッシュ {cp.name}  SHA-256 {CACHE_SHA}")
-if CACHE_SHA != EXPECT_CACHE_SHA:
-    sys.exit(f"{TAG} STOP: キャッシュの SHA-256 が 21_20c の本番(停止の記録 b9162a9d…aa83)と違う")
 CAT_SHA = sha256(catp)
@@ -114,3 +105,3 @@
         t = datetime.strptime(ts[:22], "%Y-%m-%d %H:%M:%S.%f" if "." in ts else "%Y-%m-%d %H:%M:%S")
-        t21 = datetime.strptime(ts[:21].ljust(21, "0"), "%Y-%m-%d %H:%M:%S.%f")   # 21_20c と同じ読み方(0.1 s で切り捨て)
+        t21 = datetime.strptime(ts[:21].ljust(21, "0"), "%Y-%m-%d %H:%M:%S.%f")   # 24_03(= 21_20c)と同じ読み方(0.1 s で切り捨て)
         mg = row.get("mag", "").strip()
@@ -126,3 +117,3 @@
 
-# ---- 2. 本震(21_20 v1 と同じ: Mj 最大で、Mj ≥ 6.0・MAIN_UTC ± 60 s)
+# ---- 2. 本震(21_20 v1・24_05 と同じ: Mj 最大で、Mj ≥ 6.0・MAIN_UTC ± 60 s)
 im = int(np.argmax(MAG))
@@ -151,4 +142,4 @@
     sys.exit(f"{TAG} STOP: キャッシュの地震のうち、震源一覧に自分の行が見つからないもの {n_noself}・2 行以上あるもの {n_multi}"
-             "(21_20c と同じ読み方の時刻と Mj で照合)")
-print(f"{TAG} G-match PASS: キャッシュの {NE} 地震とも、震源一覧に自分の行がちょうど 1 つある(21_20c と同じ読み方の時刻と Mj で照合)")
+             "(24_03 = 21_20c と同じ読み方の時刻と Mj で照合)")
+print(f"{TAG} G-match PASS: キャッシュの {NE} 地震とも、震源一覧に自分の行がちょうど 1 つある(24_03 = 21_20c と同じ読み方の時刻と Mj で照合)")
 
@@ -161,6 +152,6 @@
     t = datetime.strptime(str(c["origin_jst"]).replace("T", " ")[:19], "%Y-%m-%d %H:%M:%S")
-    EVJ19 = [x.replace(microsecond=0) for x in OT_JST]     # 21_20d v1 の jst() と同じ(秒で切り捨て)
+    EVJ19 = [x.replace(microsecond=0) for x in OT_JST]     # 21_20d v1・24_04d の jst() と同じ(秒で切り捨て)
     j = min(range(NE), key=lambda i: abs((EVJ19[i] - t).total_seconds()))
     if abs((EVJ19[j] - t).total_seconds()) > GCLOCK_MATCH_S:
-        print(f"{TAG} 注意: G-clock の地震 {c['origin_jst']} がキャッシュに無い(21_20d の (e) がその扱いを決める。ここでは何もしない)"); continue
+        print(f"{TAG} 注意: G-clock の地震 {c['origin_jst']} がキャッシュに無い(24_04d の (e) がその扱いを決める。ここでは何もしない)"); continue
     KEEP.setdefault(j, "G-clock event")
@@ -169,7 +160,7 @@
         out0 = Path(a.out) / "data"; out0.mkdir(parents=True, exist_ok=True)
-        json.dump(dict(script="21_20h_osaka2018_overlap_exclusion.py", version=VERSION, script_sha256=SELF_SHA, input_cache_sha256=CACHE_SHA,
+        json.dump(dict(script="24_03h_nagano2014_overlap_exclusion.py", version=VERSION, script_sha256=SELF_SHA, input_cache_sha256=CACHE_SHA,
                        verdict="STOP-R2: an exempt event (mainshock or G-clock event) is a test candidate",
                        event=dict(origin_jst=f"{OT_JST[j]:%Y-%m-%d %H:%M:%S.%f}"[:22], mj=float(MAG[j]), why=why)),
-                  open(out0 / "21_20h_overlap_exclusion.json", "w"), indent=1, ensure_ascii=False)
-        sys.exit(f"{TAG} STOP(R2): 除かない地震({why}、{OT_JST[j]:%Y-%m-%d %H:%M:%S} JST Mj {MAG[j]:.1f})が試験の候補。記録: {out0 / '21_20h_overlap_exclusion.json'}")
+                  open(out0 / "24_03h_overlap_exclusion.json", "w"), indent=1, ensure_ascii=False)
+        sys.exit(f"{TAG} STOP(R2): 除かない地震({why}、{OT_JST[j]:%Y-%m-%d %H:%M:%S} JST Mj {MAG[j]:.1f})が試験の候補。記録: {out0 / '24_03h_overlap_exclusion.json'}")
 EXCL = [ie for ie in range(NE) if NB[ie] and ie not in KEEP]
@@ -187,26 +178,6 @@
 
-# 記述(判定に使わない): 21_20g で 1 s より大きくずれた地震のうち、除かれるもの・試験の候補であるもの
-G_DESC = None
-if a.g_json and Path(a.g_json).exists():
-    gj = json.load(open(a.g_json))
-    bad = gj.get("events_dev_gt_1s", [])
-    KEY = {f"{OT_JST[ie]:%Y-%m-%d %H:%M:%S.%f}"[:22]: ie for ie in range(NE)}
-    rows_b = []
-    for b in bad:
-        ie = KEY.get(str(b.get("origin_jst"))[:22])
-        rows_b.append(dict(origin_jst=b.get("origin_jst"), mj=b.get("mj"), dev_s=b.get("dev_s"), found=ie is not None,
-                           test_candidate=(bool(IS_TEST[ie]) if ie is not None else None), excluded=(ie in EXS if ie is not None else None)))
-    n_tc = sum(1 for r_ in rows_b if r_["test_candidate"]); n_ex = sum(1 for r_ in rows_b if r_["excluded"])
-    n_tc_ex = sum(1 for r_ in rows_b if r_["test_candidate"] and r_["excluded"])
-    G_DESC = dict(g_json_sha256=sha256(Path(a.g_json)), n_dev_gt_1s=len(bad), n_test_candidates=n_tc, n_excluded=n_ex,
-                  n_test_candidates_excluded=n_tc_ex, n_test_excluded_not_in_this_list=int(n_test0 - n_test1 - n_tc_ex), events=rows_b)
-    print(f"{TAG} 記述: 21_20g で 1 s より大きくずれた地震 {len(bad)}(うち試験の候補 {n_tc})。この規則で除かれるもの {n_ex}"
-          f"(うち試験の候補 {n_tc_ex})。この一覧に無いのに除かれる試験の候補 {n_test0 - n_test1 - n_tc_ex}(判定には使わない)")
-    for r_ in rows_b:
-        print(f"      {r_['origin_jst']} Mj {r_['mj']}  ずれ {r_['dev_s']:+.2f} s  試験の候補 {r_['test_candidate']}  除く {r_['excluded']}")
-
 out = Path(a.out); (out / "data" / "tottori_processed").mkdir(parents=True, exist_ok=True)
-REC = dict(script="21_20h_osaka2018_overlap_exclusion.py", version=VERSION, script_sha256=SELF_SHA,
-           purpose="amendment 04: remove events with another catalogue event within [-15 s, +5 s] of origin; origin times only; no location, waveform or residual used",
-           rule=dict(pre_s=PRE_S, post_s=POST_S, self_row="catalogue row with the same 21_20c-parsed time (0.1 s) and Mj; dt measured from its 0.01 s time", keep="mainshock and the 21_20b G-clock events",
+REC = dict(script="24_03h_nagano2014_overlap_exclusion.py", version=VERSION, script_sha256=SELF_SHA,
+           purpose="preregistration 24 rule R1 (from 21_20 amendment 04): remove events with another catalogue event within [-15 s, +5 s] of origin; origin times and Mj only; no location, waveform or residual used",
+           rule=dict(pre_s=PRE_S, post_s=POST_S, self_row="catalogue row with the same 24_03 (= 21_20c) parsed time (0.1 s) and Mj; dt measured from its 0.01 s time", keep="mainshock and the 24_02 G-clock events",
                      pool_h=POOL_H, fresh_max_mag=FRESH_MAX_MAG, min_test=MIN_TEST),
@@ -218,3 +189,3 @@
            kept_exempt=[dict(origin_jst=f"{OT_JST[j]:%Y-%m-%d %H:%M:%S.%f}"[:22], mj=float(MAG[j]), why=KEEP[j], neighbours=NB[j]) for j in sorted(KEEP)],
-           descriptive_21_20g=G_DESC)
+           )
 
@@ -222,3 +193,3 @@
 if n_test1 < MIN_TEST:
-    REC.update(output=None, verdict="STOP-R3: fewer than 30 test candidates after exclusion; 21_20 is not run and the result is reported as INCONCLUSIVE")
+    REC.update(output=None, verdict="STOP-R3: fewer than 30 test candidates after exclusion; 24_05 is not run and the result is reported as INCONCLUSIVE")
     json.dump(REC, open(out / OUT_JSON, "w"), indent=1, ensure_ascii=False)
@@ -238,2 +209,2 @@
 print(f"{TAG} 記録: {out / OUT_JSON}")
-print(f"{TAG} 次: この SHA-256 を変更の記録 04 の 6 節に書いて push してから、21_20d・21_20e を --base {out} --cache {op} で回す")
+print(f"{TAG} 次: 24_04d・24_04e を --base {out} --cache {OUT_CACHE} で回す(この SHA-256 は 24_05 が opened.json に書き、24_07 の記録と照らす)")
```

## 24_04d_nagano2014_gclock2_picks.py ← 21_20d_osaka2018_gclock2_picks.py

```diff
--- osaka/21_20d_osaka2018_gclock2_picks.py	2026-11-01 23:40:13.618067929 +0000
+++ nagano/frz/24_04d_nagano2014_gclock2_picks.py	2026-11-15 05:21:00.092796961 +0000
@@ -2,44 +2,25 @@
 # =============================================================================
-# Script : 21_20d_osaka2018_gclock2_picks.py  (v1)
-#          [G-clock2: 21_20c が作ったキャッシュの PhaseNet の P の検測(全ての地震・全ての局)を使って、大阪府北部 2018 の波形の
-#           時刻がずれていないかを確かめる。規則(a)〜(f)と閾値は 21_04d v1(21_04 の変更の記録 02)と同じ]
-# Project: ARGUS(新生)— 3 つ目の余震系列での確認(21_20)の入力の確かめ
-# 派生元 : 21_04d_ct2016_gclock2_picks.py v1(SHA-256 bc37a3c63e1b60cb7806498527caf7371f2ee8846555141a719592d5d2557de4)。
-#          計算・規則・閾値・止め方(FAIL なら exit code 1)は 1 字も変えていない。変えたのは次だけ(DIFF_LOG.md):
-#          既定のキャッシュ(..._osaka2018_m15.pt)と報告(data/21_20b_report.json)の場所、表示の [21_20d]、出力の名前
-#          (data/21_20d_gclock2.json・PDF/21_20d_gclock2.pdf)、JSON の script、図の題と軸の年。
-#          FAIL の時の扱いは、事前登録 21_20 の「G-clock2 の扱い」に先に決めてある((c) だけの FAIL と、それ以外の FAIL で違う)。
-#          この版は、どの条件で FAIL したかを JSON の pass_* に残すので、その扱いはこの出力だけで決まる。
-# 以下の「なぜ必要か」は 21_04d の時の記録(鳥取県中部 2016)のまま残す。
+# Script : 24_04d_nagano2014_gclock2_picks.py  (v1)
+#          [G-clock2: 24_03h の後のキャッシュの PhaseNet の P の検測(全ての地震・全ての局)を使って、長野県北部 2014 の波形の
+#           時刻がずれていないかを確かめる。規則(a)〜(f)と閾値は 21_04d v1・21_20d v1 と同じ]
+# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の確かめ
+# 派生元 : 21_20d_osaka2018_gclock2_picks.py v1(SHA-256 606d0eea2f76a8607c7844f83a93056759640974bce7f11ccfe690ecb6e7c1d6)。
+#          計算・規則・閾値・止め方(FAIL なら exit code 1)は 1 字も変えていない。変えたのは次だけ(DIFF_LOG_24.md):
+#          既定のキャッシュ(..._nagano2014_m15_r1.pt = 24_03h の出力)と報告(data/24_02_report.json)の場所、表示の [24_04d]、
+#          出力の名前(data/24_04d_gclock2.json・PDF/24_04d_gclock2.pdf)、JSON の script、図の題と軸の年。
+#          FAIL の時の扱いは、事前登録 24 の 5.3 節(21_20 の案 C と同じ: (a)・(b)・(d)・(e)・(f) のどれかの FAIL で止める。
+#          (c) は 24_04e の表で 80 km 以内(止める)と 80 km より遠い(止めずに印を付ける)に分ける)。
 #
-# なぜ必要か:
-#   21_04b の G-clock(STA/LTA の立ち上がり)は、本震・10-29 Mj 4.5・10-21 22:53 Mj 3.8 で通り、10-21 22:03 Mj 3.9 だけ 2.79 s で
-#   FAIL だった。21_04c で調べると、FAIL の地震では立ち上がりが予想の P より早い(符号付きの中央値 −2.79 s、8 局中 6 局が予想の P より
-#   1 s 以上早い)。波形の P の始まりは予想の P の位置にそろっていて、前の数十秒に気象庁の小さな地震(Mj 0.7 など)があった。
-#   つまり、余震の多い時間帯に STA/LTA が P より前の小さな揺れで立ち上がった形で、時刻のずれの形(全ての局で同じ向き・同じ量の
-#   ずれ)ではない。ただし、図を見て判断するだけでは足りないので、数千の検測を使う、STA/LTA に依らない時刻の確かめを足す。
+# 何をするか(21_20d と同じ):
+#   1. キャッシュの全ての地震・全ての局のうち、PhaseNet で P を測った検測(p_fallback = 0)について、残り r = tp_times − dist_km / 6.0 s を出す。
+#   2. (a) |全体の中央値| ≤ 1.5 s (b) 日ごと ≤ 0.5 s (c) 局ごと ≤ 1.0 s (d) 1 時間ごと ≤ 0.5 s
+#      (e) 24_02 の報告の G-clock の地震がそれぞれ ≤ 0.5 s(検測 4 以上) (f) 局ごとの P を測った割合が全局の中央値の 0.5 倍以上。
+#      検測 20 以上の日・局・時間で数える。日と時間は日本時間。
+#   3. 参考(判定には使わない): --ref-cache に鳥取 2026 のキャッシュ。
+#   4. 出力: data/24_04d_gclock2.json / PDF/24_04d_gclock2.pdf。FAIL なら exit code 1。
 #
-# 何をするか(G-clock2。規則は変更の記録 02 に書いたもので、このスクリプトはそれをそのまま計算する):
-#   1. キャッシュ(既定 data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt)の全ての地震・全ての局のうち、PhaseNet で
-#      P を測った検測(p_fallback = 0)について、残り r = tp_times − dist_km / 6.0 s を出す
-#      (tp_times は 15_01c が書いた「P の時刻 − 気象庁の発生時刻」、dist_km は震源距離。6.0 km/s は G-clock と同じ)。
-#   2. 合格の条件(全て満たせば PASS。日と時間は日本時間。キャッシュの origin_time は UTC なので 9 時間を足す):
-#      (a) 全体の中央値 |median(r)| ≤ 1.5 s(G-clock と同じ許容)
-#      (b) 日ごと(検測 20 以上の日): |その日の中央値 − 全体の中央値| ≤ 0.5 s
-#      (c) 局ごと(検測 20 以上の局。局は座標で見分ける): |その局の中央値 − 全体の中央値| ≤ 1.0 s(局の下の構造・距離・一定の速度の誤差が
-#          混ざるので日ごとより広くした。事前に決めた値で、較正はしていない)
-#      (d) 時間ごと(日本時間の 1 時間、検測 20 以上): |その時間の中央値 − 全体の中央値| ≤ 0.5 s(短い時間だけのずれを見る)
-#      (e) 21_20b の報告の G-clock の 4 地震(--report。既定 data/21_20b_report.json): それぞれ P を測った検測 4 以上で、|その地震の中央値 − 全体の中央値| ≤ 0.5 s
-#      (f) 局ごとの P を測った割合(現れた数 20 以上の局): 全ての局で、局の割合の中央値の 0.5 倍以上(時刻のずれた局が QC で落ちて
-#          (c) に入らない抜け道をふさぐ)
-#      止める: P を測った検測が 100 未満、検測 20 以上の日・局・時間のどれかが 0、21_20b の報告が無い
-#   3. 参考(判定には使わない): --ref-cache に鳥取 2026 のキャッシュを渡すと、同じ量を出す(許容が普通の値に比べて妥当かを見るため)。
-#   4. 出力: data/21_20d_gclock2.json(数・中央値・日ごと・局ごと・時間ごと・4 地震・測った割合・判定)/ PDF/21_20d_gclock2.pdf(日ごと・局ごとの中央値。白背景・英語・
-#      凡例は枠の外)。FAIL なら exit code 1(その後の扱いは事前登録 21_20 の「G-clock2 の扱い」)。
-#
-# Usage(Colab、21_20c の本番の後に。ノート 21_20_osaka2018_colab.ipynb の セル 12):
-#   !python /content/drive/MyDrive/ARGUS/src/21_20d_osaka2018_gclock2_picks.py --base /content/ARGUS_osaka2018 \
+# Usage(Colab、24_03h の後に。ノート 24_nagano2014_colab.ipynb の セル N13):
+#   !python /content/drive/MyDrive/ARGUS/src/24_04d_nagano2014_gclock2_picks.py --base /content/ARGUS_nagano2014 \
 #       --ref-cache /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt
-#   (--cache で別のキャッシュ、--ref-cache で鳥取 2026 のキャッシュを指定できる。--ref-cache は判定に使わない)
-# 止める条件(STOP): キャッシュが無い・上の「止める」
+# 止める条件(STOP): キャッシュが無い・P を測った検測が 100 未満・検測 20 以上の日・局・時間のどれかが 0・24_02 の報告が無い
 # =============================================================================
@@ -52,6 +33,6 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--base", required=True, help="ARGUS_osaka2018 の場所(Colab のローカルなら /content/ARGUS_osaka2018)")
-ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt")
+ap.add_argument("--base", required=True, help="ARGUS_nagano2014 の場所(Colab のローカルなら /content/ARGUS_nagano2014)")
+ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt")
 ap.add_argument("--ref-cache", default="", help="参考: 鳥取 2026 のキャッシュ(無くてよい)")
-ap.add_argument("--report", default="data/21_20b_report.json", help="21_20b の報告(G-clock の 4 地震を読む。--base からの場所)")
+ap.add_argument("--report", default="data/24_02_report.json", help="24_02 の報告(G-clock の地震を読む。--base からの場所)")
 a = ap.parse_args()
@@ -95,13 +76,13 @@
 cp = BASE / a.cache
-if not cp.exists(): sys.exit(f"[21_20d] STOP: キャッシュ {cp} が無い(21_20c の本番の後に回す)")
+if not cp.exists(): sys.exit(f"[24_04d] STOP: キャッシュ {cp} が無い(24_03h の後に回す)")
 EVS, r, day, sta, hour, evi, seen = residuals(cp); nev = len(EVS)
-if len(r) < 100: sys.exit(f"[21_20d] STOP: P を測った検測が {len(r)}(100 未満)")
+if len(r) < 100: sys.exit(f"[24_04d] STOP: P を測った検測が {len(r)}(100 未満)")
 S = summarise(r, day, sta, hour)
 if S["n_days"] == 0 or S["n_stations"] == 0 or S["n_hours"] == 0:
-    sys.exit(f"[21_20d] STOP: 検測 {MIN_N} 以上の日・局・時間のどれかが 0(判定できない)")
+    sys.exit(f"[24_04d] STOP: 検測 {MIN_N} 以上の日・局・時間のどれかが 0(判定できない)")
 pa = abs(S["median_s"]) <= TOL_ALL; pd_ = S["max_day_dev_s"] <= TOL_DAY; ps = S["max_station_dev_s"] <= TOL_STA
 ph = S["max_hour_dev_s"] <= TOL_HOUR
-# (e) 21_20b の G-clock の 4 地震: その地震の P を測った検測(MIN_EV 以上)の中央値 − 全体の中央値
+# (e) 24_02 の G-clock の地震: その地震の P を測った検測(MIN_EV 以上)の中央値 − 全体の中央値
 rp = BASE / a.report
-if not rp.exists(): sys.exit(f"[21_20d] STOP: 21_20b の報告 {rp} が無い")
+if not rp.exists(): sys.exit(f"[24_04d] STOP: 24_02 の報告 {rp} が無い")
 gc = json.load(open(rp))["gates"]["clock"]
@@ -125,6 +106,6 @@
 PASS = bool(pa and pd_ and ps and ph and pe and pf_)
-print(f"[21_20d] キャッシュ {cp.name}: 地震 {nev}・P を測った検測 {S['n']}(日は日本時間。キャッシュの UTC に 9 時間を足す)")
-print(f"[21_20d] (a) 全体: 残り(P の時刻 − 震源距離/6.0 km/s)の中央値 {S['median_s']:+.3f} s(四分位幅 {S['iqr_s']:.3f} s)  "
+print(f"[24_04d] キャッシュ {cp.name}: 地震 {nev}・P を測った検測 {S['n']}(日は日本時間。キャッシュの UTC に 9 時間を足す)")
+print(f"[24_04d] (a) 全体: 残り(P の時刻 − 震源距離/6.0 km/s)の中央値 {S['median_s']:+.3f} s(四分位幅 {S['iqr_s']:.3f} s)  "
       f"基準 |中央値| ≤ {TOL_ALL} s  {'PASS' if pa else 'FAIL'}")
-print(f"[21_20d] (b) 日ごと(検測 {MIN_N} 以上の日): 全体の中央値からの最大のずれ {S['max_day_dev_s']:.3f} s  基準 ≤ {TOL_DAY} s  "
+print(f"[24_04d] (b) 日ごと(検測 {MIN_N} 以上の日): 全体の中央値からの最大のずれ {S['max_day_dev_s']:.3f} s  基準 ≤ {TOL_DAY} s  "
       f"{'PASS' if pd_ else 'FAIL'}")
@@ -132,3 +113,3 @@
     print(f"      {d}: 検測 {v['n']:5d}  中央値 {v['median']:+.3f} s" + ("" if v["n"] >= MIN_N else "(少ないので判定に使わない)"))
-print(f"[21_20d] (c) 局ごと(検測 {MIN_N} 以上の局): 全体の中央値からの最大のずれ {S['max_station_dev_s']:.3f} s  基準 ≤ {TOL_STA} s  "
+print(f"[24_04d] (c) 局ごと(検測 {MIN_N} 以上の局): 全体の中央値からの最大のずれ {S['max_station_dev_s']:.3f} s  基準 ≤ {TOL_STA} s  "
       f"{'PASS' if ps else 'FAIL'}")
@@ -136,3 +117,3 @@
 for dv, s, v in worst: print(f"      ずれの大きい局 {s}: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
-print(f"[21_20d] (d) 時間ごと(日本時間の 1 時間・検測 {MIN_N} 以上、{S['n_hours']} 時間): 全体の中央値からの最大のずれ {S['max_hour_dev_s']:.3f} s  "
+print(f"[24_04d] (d) 時間ごと(日本時間の 1 時間・検測 {MIN_N} 以上、{S['n_hours']} 時間): 全体の中央値からの最大のずれ {S['max_hour_dev_s']:.3f} s  "
       f"基準 ≤ {TOL_HOUR} s  {'PASS' if ph else 'FAIL'}")
@@ -140,3 +121,3 @@
 for dv, k, v in worst_h: print(f"      ずれの大きい時間 {k} 時台: 検測 {v['n']}  中央値 {v['median']:+.3f} s(ずれ {dv:.3f} s)")
-print(f"[21_20d] (e) 21_20b の G-clock の 4 地震(P を測った検測 {MIN_EV} 以上、|地震の中央値 − 全体の中央値| ≤ {TOL_EV} s): {'PASS' if pe else 'FAIL'}")
+print(f"[24_04d] (e) 24_02 の G-clock の地震(P を測った検測 {MIN_EV} 以上、|地震の中央値 − 全体の中央値| ≤ {TOL_EV} s): {'PASS' if pe else 'FAIL'}")
 for x in EVC:
@@ -145,3 +126,3 @@
           f"(STA/LTA の G-clock は {x['gclock_stalta_median_abs_s']:.2f} s)  {'PASS' if x['pass_'] else 'FAIL'}")
-print(f"[21_20d] (f) 局ごとの P を測った割合(現れた数 {MIN_N} 以上の {len(fr)} 局): 中央値 {mfr:.3f}、その {MIN_FRAC_RATIO} 倍未満の局 {len(low)}  "
+print(f"[24_04d] (f) 局ごとの P を測った割合(現れた数 {MIN_N} 以上の {len(fr)} 局): 中央値 {mfr:.3f}、その {MIN_FRAC_RATIO} 倍未満の局 {len(low)}  "
       f"{'PASS' if pf_ else 'FAIL'}")
@@ -151,7 +132,7 @@
     _, r2, d2, s2, h2, _, _ = residuals(Path(a.ref_cache)); REF = summarise(r2, d2, s2, h2)
-    print(f"[21_20d] 参考(鳥取 2026、判定には使わない): 検測 {REF['n']}  中央値 {REF['median_s']:+.3f} s  日ごとの最大のずれ "
+    print(f"[24_04d] 参考(鳥取 2026、判定には使わない): 検測 {REF['n']}  中央値 {REF['median_s']:+.3f} s  日ごとの最大のずれ "
           f"{REF['max_day_dev_s']:.3f} s  局ごとの最大のずれ {REF['max_station_dev_s']:.3f} s  時間ごとの最大のずれ {REF['max_hour_dev_s']:.3f} s")
-print(f"[21_20d] G-clock2: {'PASS' if PASS else 'FAIL'}")
+print(f"[24_04d] G-clock2: {'PASS' if PASS else 'FAIL'}")
 (BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
-json.dump(dict(script="21_20d_osaka2018_gclock2_picks.py", version="v1", cache=str(cp), n_events=nev, vp_kms=VP,
+json.dump(dict(script="24_04d_nagano2014_gclock2_picks.py", version="v1", cache=str(cp), n_events=nev, vp_kms=VP,
                rule=dict(tol_all_s=TOL_ALL, tol_day_s=TOL_DAY, tol_station_s=TOL_STA, tol_hour_s=TOL_HOUR, tol_event_s=TOL_EV,
@@ -162,3 +143,3 @@
                pass_measured_frac=bool(pf_), gclock2_pass=PASS, reference_2026=REF),
-          open(BASE / "data" / "21_20d_gclock2.json", "w"), indent=1)
+          open(BASE / "data" / "24_04d_gclock2.json", "w"), indent=1)
 
@@ -175,4 +156,4 @@
 ax.set_xticks(range(len(dk))); ax.set_xticklabels([d[5:] for d in dk], rotation=60, fontsize=7); ax.set_xlim(-0.5, len(dk) - 0.5)
-ax.set_xlabel("JST date (2018)"); ax.set_ylabel("PhaseNet P time - distance / 6.0 km/s (s)")
-ax.set_title(f"(a) Northern Osaka 2018, {S['n']} P picks: daily medians", fontsize=9); ax.grid(alpha=0.3)
+ax.set_xlabel("JST date (2014)"); ax.set_ylabel("PhaseNet P time - distance / 6.0 km/s (s)")
+ax.set_title(f"(a) Northern Nagano 2014, {S['n']} P picks: daily medians", fontsize=9); ax.grid(alpha=0.3)
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3, frameon=False, fontsize=8)
@@ -184,4 +165,4 @@
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), frameon=False, fontsize=8)
-fig.tight_layout(); fig.savefig(BASE / "PDF" / "21_20d_gclock2.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"[21_20d] 出力: {BASE / 'data' / '21_20d_gclock2.json'}、{BASE / 'PDF' / '21_20d_gclock2.pdf'}")
-if not PASS: sys.exit("[21_20d] STOP(G-clock2): 時刻のずれの疑い。どの条件の FAIL かで、事前登録 21_20 の扱いに従う(この出力を貼る)")
+fig.tight_layout(); fig.savefig(BASE / "PDF" / "24_04d_gclock2.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"[24_04d] 出力: {BASE / 'data' / '24_04d_gclock2.json'}、{BASE / 'PDF' / '24_04d_gclock2.pdf'}")
+if not PASS: sys.exit("[24_04d] STOP(G-clock2): 時刻のずれの疑い。どの条件の FAIL かで、事前登録 24 の 5.3 節の扱いに従う(この出力を貼る)")
```

## 24_04e_nagano2014_station_pick_diagnose.py ← 21_20e_osaka2018_station_pick_diagnose.py

```diff
--- osaka/21_20e_osaka2018_station_pick_diagnose.py	2026-11-02 00:21:12.510691632 +0000
+++ nagano/frz/24_04e_nagano2014_station_pick_diagnose.py	2026-11-15 05:21:00.094259170 +0000
@@ -2,31 +2,16 @@
 # =============================================================================
-# Script : 21_20e_osaka2018_station_pick_diagnose.py  (v1)
-#          [G-clock2(21_20d)の (c) 局ごとの確かめで FAIL になった局が、時計のずれか、検測の取り違えかを調べる。読むだけで、
-#           キャッシュ・ゲート・規則は何も変えない。判定には使わない記述]
-# Project: ARGUS(新生)— 3 つ目の余震系列での確認(21_20)の入力の確かめ
-# 派生元 : 21_04e_ct2016_station_pick_diagnose.py v1(SHA-256 2eca1779642deb3c8ea4433649862e73697b9b4f3d7deced7fae78a1392a9406)。
-#          計算は 1 字も変えていない。変えたのは、既定のキャッシュの場所・表示の [21_20e] と系列の名前・出力の名前
-#          (data/21_20e_station_picks.csv・PDF/21_20e_station_picks.pdf)・図の題だけ(DIFF_LOG.md)。
-#          事前登録 21_20 (5.3 節・案 C) では、21_20d の結果によらず必ず回す。(c) を 80 km 以内と 80 km より遠い局に分ける判定は、この出力の CSV で行う(このスクリプトは判定しない)。
-# 以下の「なぜ必要か」は 21_04e の時の記録(鳥取県中部 2016)のまま残す。
+# Script : 24_04e_nagano2014_station_pick_diagnose.py  (v1)
+#          [局ごとの検測の調べ(読むだけの記述)。事前登録 24 の 5.3 節では、24_04d の結果によらず必ず回し、この CSV の
+#           epi_from_mainshock_km・n・dev_s で G-clock2 の (c) を 80 km 以内(止める)と 80 km より遠い(止めずに印)に分ける]
+# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の入力の確かめ
+# 派生元 : 21_20e_osaka2018_station_pick_diagnose.py v1(SHA-256 680e8825d49e00bba58cca9045c66ee7b213f05bc5a231d0810d041b4fefba92)。
+#          計算は 1 字も変えていない。変えたのは、既定のキャッシュの場所・表示の [24_04e] と系列の名前・出力の名前
+#          (data/24_04e_station_picks.csv・PDF/24_04e_station_picks.pdf)・図の題だけ(DIFF_LOG_24.md)。
 #
-# なぜ必要か:
-#   21_04d の G-clock2 では、(a) 全体・(b) 日ごと・(d) 時間ごと・(e) G-clock の 4 地震・(f) 測った割合は PASS だった。(c) 局ごとだけが
-#   FAIL で、ずれの大きい局(中央値 −6〜−9 s。予想の P より早い)は本震から遠い局だった。
-#   時計がずれた局なら、その局の全ての検測が、地震の大きさに関係なく同じ量だけずれる。
-#   検測の取り違えなら、P が弱い小さい地震ほど早い向きにずれる(15_01c は「確率 0.3 以上で最も早い P」を取るので、余震の多い時期には
-#   前の地震や雑音の P を取りやすい)。大きい地震の検測は、P がはっきりしているので予想の位置に来る。
-#   そこで、局ごとに地震の大きさで分けた残りを並べる。
+# 何をするか(21_20e と同じ): キャッシュの P を測った検測(p_fallback = 0)の残り r = tp_times − dist_km / 6.0 を局ごとに出し、
+#   本震(キャッシュの Mj 最大)からの震央距離・検測の数・中央値・Mj の 3 区分の中央値・|r − 全体の中央値| > 3 s の割合を表にする。
+#   --ref-cache に鳥取 2026 のキャッシュを渡すと、同じ表を参考に出す(判定には使わない)。
 #
-# 何をするか:
-#   1. キャッシュの P を測った検測(p_fallback = 0)の残り r = tp_times − dist_km / 6.0 を、局ごとに出す(21_04d と同じ式)。
-#   2. 局ごと(現れた順ではなく、本震からの距離の順)に、次を表にする:
-#      本震からの震央距離・検測の数・中央値・Mj < 2.0 の中央値・2.0 ≤ Mj < 3.0 の中央値・Mj ≥ 3.0 の中央値(と数)・
-#      |r − 全体の中央値| > 3 s の割合(取り違えの割合の目安)
-#   3. --ref-cache に鳥取 2026 のキャッシュを渡すと、同じ表を出す(21_02 で使った同じ作り方のキャッシュに、同じ形があるか)。
-#   4. 出力: data/21_20e_station_picks.csv と、PDF/21_20e_station_picks.pdf(局の距離に対する中央値。地震の大きさの 3 区分を色で。
-#      白背景・英語・凡例は枠の外)
-#
-# Usage(Colab):
-#   !python /content/drive/MyDrive/ARGUS/src/21_20e_osaka2018_station_pick_diagnose.py --base /content/ARGUS_osaka2018 \
+# Usage(Colab。ノート 24_nagano2014_colab.ipynb の セル N14):
+#   !python /content/drive/MyDrive/ARGUS/src/24_04e_nagano2014_station_pick_diagnose.py --base /content/ARGUS_nagano2014 \
 #       --ref-cache /content/drive/MyDrive/ARGUS_tottori/data/tottori_processed/tottori_parsed_realpick_m15.pt
@@ -40,3 +25,3 @@
 ap.add_argument("--base", required=True)
-ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_osaka2018_m15.pt")
+ap.add_argument("--cache", default="data/tottori_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt")
 ap.add_argument("--ref-cache", default="")
@@ -78,3 +63,3 @@
 def show(name, med, out):
-    print(f"\n[21_20e] ===== {name}: 全体の中央値 {med:+.3f} s(局 {len(out)}、本震からの距離の順)=====")
+    print(f"\n[24_04e] ===== {name}: 全体の中央値 {med:+.3f} s(局 {len(out)}、本震からの距離の順)=====")
     print("  局(緯度,経度)        本震から km  検測   中央値   ずれ   Mj<2 の中央値(数)   2≤Mj<3(数)        Mj≥3(数)         |r−全体|>3 s")
@@ -87,6 +72,6 @@
 cp = BASE / a.cache
-if not cp.exists(): sys.exit(f"[21_20e] STOP: {cp} が無い")
-med, out = table(cp); show("大阪府北部 2018", med, out)
+if not cp.exists(): sys.exit(f"[24_04e] STOP: {cp} が無い")
+med, out = table(cp); show("長野県北部 2014", med, out)
 (BASE / "data").mkdir(parents=True, exist_ok=True); (BASE / "PDF").mkdir(parents=True, exist_ok=True)
-with open(BASE / "data" / "21_20e_station_picks.csv", "w", newline="") as fo:
+with open(BASE / "data" / "24_04e_station_picks.csv", "w", newline="") as fo:
     w = csv.DictWriter(fo, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
@@ -97,3 +82,3 @@
     else:
-        print(f"[21_20e] 注意: 参考のキャッシュ {a.ref_cache} が無いので飛ばした")
+        print(f"[24_04e] 注意: 参考のキャッシュ {a.ref_cache} が無いので飛ばした")
 
@@ -103,3 +88,3 @@
 plt.rcParams.update({"figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white", "font.size": 9, "pdf.fonttype": 42})
-panels = [("Northern Osaka 2018", med, out)] + ([("West Tottori 2026 (reference)", *ref)] if ref else [])
+panels = [("Northern Nagano 2014", med, out)] + ([("West Tottori 2026 (reference)", *ref)] if ref else [])
 fig, axs = plt.subplots(1, len(panels), figsize=(6.2 * len(panels), 4.4), squeeze=False)
@@ -117,3 +102,3 @@
 axs[0][0].legend(loc="upper center", bbox_to_anchor=(0.5 * len(panels) + 0.05 * (len(panels) - 1), -0.15), ncol=5, frameon=False, fontsize=8)
-fig.tight_layout(); fig.savefig(BASE / "PDF" / "21_20e_station_picks.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"\n[21_20e] 出力: {BASE / 'data' / '21_20e_station_picks.csv'}、{BASE / 'PDF' / '21_20e_station_picks.pdf'}")
+fig.tight_layout(); fig.savefig(BASE / "PDF" / "24_04e_station_picks.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"\n[24_04e] 出力: {BASE / 'data' / '24_04e_station_picks.csv'}、{BASE / 'PDF' / '24_04e_station_picks.pdf'}")
```

## 24_05_nagano2014_similarity_confirmation.py ← 21_20_osaka2018_similarity_confirmation.py

```diff
--- osaka/21_20_osaka2018_similarity_confirmation.py	2026-11-01 23:41:13.708534492 +0000
+++ nagano/frz/24_05_nagano2014_similarity_confirmation.py	2026-11-15 05:21:00.096344895 +0000
@@ -2,31 +2,32 @@
 # =============================================================================
-# Script : 21_20_osaka2018_similarity_confirmation.py  (v1)
-#          [21_02 で合格し、21_04(鳥取県中部 2016)でも確かめた「波形が似た過去の地震 × 物理」(C3)と「似た地震の通り道の補正」(C4)を、
-#           手を付けていない 3 つ目の余震系列(大阪府北部 2018、本震 2018-06-18 朝)で、21_02・21_04 と同じ規則のまま 1 回だけ確かめる]
-# Project: ARGUS(新生)— 論文の柱(3 つ目の系列での確認)
-# 派生元 : 21_04_ct2016_similarity_confirmation.py v1(SHA-256 0b2807843763b641a67e090407311d39c0204cdb7825577c6b86b07a0532908d)。
+# Script : 24_05_nagano2014_similarity_confirmation.py  (v1)
+#          [「波形が似た過去の地震 × 物理」(C3)と「似た地震の通り道の補正」(C4)を、手を付けていない 4 つ目の余震系列
+#           (長野県北部 2014、本震 2014-11-22 22:08 JST・Mj 6.7)で、21_02・21_04・21_20 と同じ規則のまま 1 回だけ確かめる。
+#           あわせて H4(C3 対 C1)と H5(τ までの波形だけの検測)を、事前登録 24 で足した副の仮説として確かめる]
+# Project: ARGUS(新生)— 論文の柱(4 つ目の系列での一発試験。変更の記録なしで回すことを目指す)
+# 派生元 : 21_20_osaka2018_similarity_confirmation.py v1(SHA-256 2c0fb375e6a1a8d48d3ffbc611bb189b2390d224488cdd5585c76f5cadd5da43)。
 #
-# なぜ編集が要ったか(引数だけでは足りない理由):
-#   21_04 v1 の引数は --cache と --dev だけで、次がスクリプトに書き込まれている。そのまま大阪のキャッシュで回すと止まるか、
-#   21_04 の 1 回だけの記録を壊す。
-#   - 本震の時刻(MAIN_UTC = 2016-10-21 05:07:22.57 UTC)と G-untouched の期間(2016-10-19〜2016-11-15 UTC) → 大阪のキャッシュでは STOP
-#   - 出力の名前(models/21_04_opened.json・models/21_04_judgment.json・data/21_04_per_event.csv・PDF/21_04_F*.pdf)
-#     → 同じ ~/SWIFT で回すと、21_04 の opened.json があるので _rerun の名前になり、21_04 の記録に大阪の行が足される
-#   - 限界の文・図の題・表示の系列の名前
+# 21_20 v1 から変えたこと(DIFF_LOG_24.md に全ての差分):
+#   1. 系列に依るもの: 入力の既定(data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt = 24_03 のキャッシュに
+#      24_03h の R1 を当てたもの)、MAIN_UTC = 2014-11-22 13:08:17.9 UTC(24_00 の表示の 22:08:17.90 JST。確かめは 21_20 と同じ
+#      「Mj 最大の地震が Mj ≥ 6.0、MAIN_UTC から 60 s 以内」)、G-untouched の期間 2014-11-20〜2014-12-17 UTC(24_01 の期間を日の単位で
+#      含む)、出力の名前(models/24_05_*・data/24_05_per_event*.csv・PDF/24_05_F*)、表示・図の題・JSON の sequence と verdict_rule の
+#      系列の名前、限界の文(LIMITS)。
+#   2. H1〜H3・BEST・勝ちの規則・方法の計算・pool・ゲート(G-split・G-lib・G-causal・G-phys)・1 回だけの記録・dev・CSV の
+#      21_20 の列は 21_20 v1 と同じ(関数 paired・judge に、比べる誤差の表を渡せる引数を足しただけ。既定では 21_20 と同じ計算)。
+#   3. 足したもの(事前登録 24 の 2 節):
+#      H4(副、α 0.005): τ = 2 s で、C3 が C1(一番似た過去の地震の気象庁の震央。先行研究の「一番似た過去の地震を引く」方式)に
+#        勝つか。勝ち = C1 と C3 の両方に値がある地震で、C3 の中央値 < C1 の中央値・片側の対応 Wilcoxon の p < 0.005・差が 0 でない
+#        組が 10 以上。床の規則は使わない(BEST との比較ではないため。21_20f の HL2 と同じ扱い)。
+#      H5(副、α 0.01): 24_07 v3 が T(= 一番早いオフラインの P + τ)までの波形だけで決めた P・S に置き換えて、全ての方法を計算し直し、
+#        τ = 2 s で C3 が BEST(置き換えた検測での BEST)に H1 と同じ規則で勝つか。似ている度合いの窓は、置き換えた P から切る。
+#        24_07 の出力は、本番を開く前に、スクリプトの SHA-256(CAUSAL_SCRIPT_SHA)・キャッシュの SHA-256・CSV の SHA-256(24_07 の JSON
+#        の csv_sha256)・全ての評価の地震 × 4 時点がそろっていることを確かめる(そろっていなければ開かずに STOP)。
+#        24_07 が回せなかった・照合に落ちた時だけ、--no-causal で H5 を評価せずに H1〜H4 を回す(事前登録 24 の 5.5 節)。
+#        H1〜H4 の結果は H5 の計算の前に models/24_05_judgment*_preH5.json に書く。H5 の計算の例外・STOP・H5 の経路の G-causal の FAIL は
+#        止めずに H5 を NOT-EVALUATED とし、H1〜H4 はそのまま報告する。H5 の経路でも G-causal(未来を置き換えても同じ)を回す。
+#      記述: 置き換えた検測での全ての方法の誤差(CSV の *_causal_err_t* の列、JSON の causal)、図 F4(オフラインと τ までの検測の
+#        BEST・C3 の中央値)。H6(予測震度)は 24_08 が、この CSV から記述として計算する。
 #
-# 21_04 v1 から変えたこと(これ以外は 1 字も変えていない。計算・既定値・仮説・判定の規則・ゲート・図の作りは 21_04 v1 と同じ。DIFF_LOG.md):
-#   1. 入力の既定: data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt(21_20c を --min-mag 1.5 --tag _osaka2018_m15 で
-#      作ったもの。21_20c の検測・QC・組み立ては 15_01c v3.3 と同じ計算)。
-#   2. 本震の想定: MAIN_UTC = 2018-06-17 22:58:30 UTC。これは気象庁の発表の「2018-06-18 07 時 58 分(日本時間)」の 1 分の真ん中で、
-#      秒までの発生時刻ではない(秒までの値はこのスクリプトを書いた時点で確かめていないので書かない)。確かめの規則は 21_04 と同じ
-#      「Mj 最大の地震が Mj ≥ 6.0、MAIN_UTC から 60 s 以内」で、60 s はこの 1 分の全体を含む。要確認: 21_20a の表示の本震の
-#      時刻(日本時間)がこの 1 分に入ること(21_20a はそうでなければ止まる)。
-#   3. G-untouched: 全ての地震の発生時刻が 2018-06-15 〜 2018-07-12(UTC)の中・Mj ≥ 1.5・Mj ≥ 6.0 が 1 地震だけ。期間は 21_20a の
-#      期間(本震の 2 日前〜24 日後、日本時間)を日の単位で含むように取った(21_04 と同じ作り方)。
-#   4. 出力の名前を 21_20 にした: models/21_20_judgment.json / models/21_20_opened.json / data/21_20_per_event.csv /
-#      PDF/21_20_F1_error_vs_tau.pdf / PDF/21_20_F2_paired_difference.pdf / PDF/21_20_F3_similarity_vs_separation.pdf
-#      (--dev では _dev、2 回目以降は _rerun_<UTC の時刻>。CSV の列は 21_04 と同じ)。
-#   5. 限界の文(LIMITS の最初の 7 項目)・表示・図の題・JSON の sequence と verdict_rule の系列の名前を大阪府北部 2018 にした。
-#
-# 事前に固定した仮説と判定(21_02 v2・21_04 v1 と同じ。この版の SHA-256 を、データを開く前に事前登録の記録 21_20 に書く):
+# 事前に固定した仮説と判定(この版の SHA-256 を、データを開く前に事前登録の記録 24 に書く):
 #   BEST(τ) = AI を使わない 9 つの方法(M0r・Mp10・M1・M2・M3r・M5・M5f・M6p・M6r)のうち、評価する全ての地震で値がある
@@ -37,17 +38,18 @@
 #     H3(副)  C3 @ τ = 0.5 s、p < 0.005
+#     H4(副)  C3 対 C1 @ τ = 2 s、p < 0.005(床の規則なし)
+#     H5(副)  τ までの検測で C3 対 BEST @ τ = 2 s、p < 0.01(H1 と同じ規則。床の規則あり)
 #   評価できる試験の地震が 30 未満なら INCONCLUSIVE。それ以外の τ・方法・感度は記述だけ。
-#   方法の中身・pool・ゲート(G-split・G-lib・G-causal・G-phys)と 1 回だけの記録・dev も 21_04 v1 と同じ。
 #
-# 限界(結果を読むときに必ず添える。表示と JSON にも英語で書く): LIMITS を見る。21_04 の限界のうち系列に依るものを大阪府北部 2018 に
-#   置き換え、それ以外は同じ文。G-clock2(21_20d)の (c) が FAIL だった時は、事前登録 21_20 の決まった印を結果に付ける
-#   (このスクリプトは G-clock2 の結果を読まない)。
+# 限界(結果を読むときに必ず添える。表示と JSON にも英語で書く): LIMITS を見る。G-clock2(24_04d)の (c) が FAIL だった時は、事前登録 24 の
+#   決まった印を結果に付ける(このスクリプトは G-clock2 の結果を読まない)。
 #
-# Usage : (先に Colab のノート 21_20_osaka2018_colab.ipynb のセル 1〜12 で tottori_parsed_realpick_osaka2018_m15.pt を作って
-#          G-clock2 を確かめ、Mac の ~/SWIFT/data/osaka2018_processed/ にコピーする。手順は COLAB_STEPS_JA.md)
-#         cd ~/SWIFT && caffeinate -i uv run python src/21_20_osaka2018_similarity_confirmation.py --dev   (動作確認。試験を開かない)
-#         cd ~/SWIFT && caffeinate -i uv run python src/21_20_osaka2018_similarity_confirmation.py         (本番。1 回だけ)
-# Output: models/21_20_judgment.json / models/21_20_opened.json / data/21_20_per_event.csv /
-#         PDF/21_20_F1_error_vs_tau.pdf / PDF/21_20_F2_paired_difference.pdf / PDF/21_20_F3_similarity_vs_separation.pdf
-# 所要  : CPU のみ。(1 地震あたりの時間)×(試験の地震の数)で、過去の地震の数にも比例する。参考: 21_04 の本番は 1,894 地震の
-#         キャッシュ・試験 307 地震で 1,564 s(models/21_04_judgment.json の runtime_s)。最初の 10 地震の後に残りの見込みを表示する
+# Usage : (先に Colab のノート 24_nagano2014_colab.ipynb のセル N1〜N16 で、R1 の後のキャッシュと 24_07 の出力を作り、G-clock2 を
+#          確かめ、Mac の ~/SWIFT/data/nagano2014_processed/ にコピーする。手順は 24_STEPS_JA.md)
+#         cd ~/SWIFT && caffeinate -i uv run python src/24_05_nagano2014_similarity_confirmation.py --dev   (動作確認。試験を開かない)
+#         cd ~/SWIFT && caffeinate -i uv run python src/24_05_nagano2014_similarity_confirmation.py         (本番。1 回だけ)
+# Output: models/24_05_judgment.json / models/24_05_opened.json / data/24_05_per_event.csv /
+#         PDF/24_05_F1_error_vs_tau.pdf / PDF/24_05_F2_paired_difference.pdf / PDF/24_05_F3_similarity_vs_separation.pdf /
+#         PDF/24_05_F4_causal_picks.pdf(--dev では _dev、2 回目以降は _rerun_<UTC の時刻>)
+#         models/24_05_judgment_preH5.json(H5 の計算の前に書く H1〜H4)
+# 所要  : CPU のみ。21_20 の約 2 倍(H5 のために全ての方法をもう 1 回計算する)。参考: 21_20 の本番は試験 55 地震で 175 s
 # =============================================================================
@@ -62,4 +64,7 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--cache", default="data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt", help="21_20c(15_01c v3.3 と同じ計算)の大阪府北部 2018 の M>=1.5 版")
+ap.add_argument("--cache", default="data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt", help="24_03(15_01c v3.3 と同じ計算)の長野県北部 2014 の M>=1.5 版に、24_03h の R1 を当てたもの")
+ap.add_argument("--causal-picks", default="data/nagano2014_processed/24_07_causal_picks_nagano2014.csv", help="24_07 v3 の --all-events の出力(H5)")
+ap.add_argument("--causal-json", default="data/nagano2014_processed/24_07_causal_picks_nagano2014.json", help="24_07 v3 の記録(SHA-256 の照合)")
 ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(pool の最後の新しい地震 20 個を代わりに使う)")
+ap.add_argument("--no-causal", action="store_true", help="事前登録 24 の 5.5 節の場合だけ: 24_07 が STOP した・照合に落ちた時に、H5 を評価せずに H1〜H4 を回す")
 a = ap.parse_args()
@@ -68,2 +73,5 @@
 VERSION = "v1"
+CAUSAL_SCRIPT_SHA = "b9b2fd5c8855c52f2e3a528e695374af752db3b0de6f789942e6da8824c2d14b"                # 24_07 v3 の SHA-256(凍結の時に書く。24_07 の JSON と照らす)
+H4 = ("H4", "C3", "C1", "2")                      # 副: C3 が C1(一番似た地震の位置。先行研究の「似た地震を引く」方式)に勝つか、α 0.005
+H5 = ("H5", "C3", "2")                            # 副: τ までの波形だけの検測で、C3 が BEST に勝つか、α 0.01(H1 と同じ規則)
 FS, IP, NTS = 100.0, 300, 2048
@@ -84,8 +92,9 @@
 NBOOT, SEED, N_DEV, N_GATE = 2000, 12, 20, 5
-MAIN_UTC = dt.datetime(2018, 6, 17, 22, 58, 30)   # 21_20: 気象庁の発表の 07:58 JST の 1 分の真ん中(秒までの値ではない。±60 s でこの 1 分を含む)。要確認
-UNTOUCHED_UTC = (dt.datetime(2018, 6, 15), dt.datetime(2018, 7, 12))     # G-untouched: 21_20a の期間(本震の 2 日前〜24 日後)を含む
-LIMITS = ["third sequence: Northern Osaka 2018 (mainshock 2018-06-18, 07:58 JST; origin time and Mj are those of the JMA catalogue, "
-          "see 21_20a's JSON), never used in ARGUS development; the hypotheses were fixed on West Tottori 2026 (21_01/21_02), "
-          "tested on Central Tottori 2016 (21_04, run with a documented deviation) and are applied here unchanged",
-          "one third sequence only",
+MAIN_UTC = dt.datetime(2014, 11, 22, 13, 8, 17, 900000)   # 24: 24_00 の表示の本震 2014-11-22 22:08:17.90 JST(± 60 s、Mj ≥ 6.0 は 21_20 と同じ確かめ)
+UNTOUCHED_UTC = (dt.datetime(2014, 11, 20), dt.datetime(2014, 12, 17))    # G-untouched: 24_01 の期間(本震の 2 日前〜24 日後)を日の単位で含む
+LIMITS = ["fourth sequence: Northern Nagano 2014 (mainshock 2014-11-22, 22:08:17.90 JST, Mj 6.7; JMA catalogue values, see 24_01's JSON), "
+          "never used in ARGUS development; the hypotheses H1-H3 were fixed on West Tottori 2026 (21_01/21_02), tested on Central Tottori 2016 "
+          "(21_04, with a documented deviation) and Northern Osaka 2018 (21_20, re-registered with amendment 04) and are applied here unchanged",
+          "one fourth sequence only; before this preregistration the catalogue h2014 was opened once by 24_00 to count events "
+          "(counts and the mainshock row only; no location list, waveform or method error was looked at)",
           "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
@@ -93,15 +102,14 @@
           "waveforms were downloaded around catalogue events only and converted to the West Tottori 2026 h5 form (30-s windows, "
-          "per-window per-component z-score, JST epoch); whether a filter was applied before the z-score in the 2026 h5 is not recorded "
-          "(none here; compared in 21_20b G-spec)",
-          "the cache was built by 21_20c, whose picking, QC and assembly are identical to 15_01c v3.3 (itself identical to v3 except "
-          "the window-index file name and output folder); 21_20c changed only labels, defaults and required arguments",
-          "catalogue: JMA hypocentres from h2018 (whether h2018 is the final stage is to be confirmed; West Tottori 2026 used the "
-          "unified catalogue); past-event locations are JMA "
+          "per-window per-component z-score, JST epoch; 24_02 also stores the window mean and standard deviation); no filter was applied "
+          "before the z-score (compared in 24_02 G-spec)",
+          "the cache was built by 24_03, whose picking, QC and assembly are identical to 15_01c v3.3; 24_03h then removed every event "
+          "with another catalogue event from 15 s before to 5 s after its origin (rule R1 of 21_20 amendment 04, fixed here before any "
+          "Nagano waveform was opened; it uses origin times and Mj only), which can bias the sample against busy periods",
+          "catalogue: JMA hypocentres from h2014 (whether h2014 is the final stage is to be confirmed); past-event locations are JMA "
           "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
-          "the 2018 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
-          "events; whether the 2026 catalogue excluded them is not recorded. Manual and automatic hypocentres are mixed (per-flag "
-          "counts in 21_20a's JSON)",
-          "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); the 2026 station list's "
-          "convention is not recorded; static station terms absorb a constant offset",
-          "offline PhaseNet picks on full records (possibly better than real-time picks); every method uses the same picks",
+          "the 2014 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
+          "events. Manual and automatic hypocentres can be mixed (per-flag counts in 24_01's JSON)",
+          "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); "
+          "static station terms absorb a constant offset",
+          "H1-H4 use offline PhaseNet picks on full records (possibly better than real-time picks); every method uses the same picks",
           "cache keeps up to 24 stations per event (PhaseNet P first, earliest first); no not-yet-arrived information is used",
@@ -118,4 +126,21 @@
           "P residual over all its stations, while uncorrected stations keep only the static term",
-          "H1 (C3 at tau = 2 s) is the primary test; H2 and H3 are secondary at alpha 0.005; everything else is descriptive"]
-
+          "H4 compares C3 with C1 (the JMA epicentre of the most similar past event, the 'search the most similar past event' approach) "
+          "on the events where C1 exists (C1 is undefined when fewer than 5 past events have a positive similarity)",
+          "H5 re-runs every method with picks made by 24_07 from data up to T only (T = first offline P + tau); the tau origin, the "
+          "station set (the cache stations) and the P search band (relative to the catalogue origin) still come from the offline picks "
+          "and the catalogue; no Wadati QC or STA/LTA fallback at each time; the similarity windows start at the causal P; stations "
+          "picked causally but without an offline PhaseNet P are used by the physics but not by the similarity; past events keep their "
+          "offline picks (their records are complete at the time of the target event)",
+          "H5 limits (continued): the event's first station (FIRST, used by M1, M3r, M5f, M6r, M6p and the C3/C4 prior) is still the "
+          "earliest offline PhaseNet station; the similarity still uses the cache waveforms (full-window mean removed, built from the "
+          "per-30-s-window z-scored h5), whereas 24_07 picked on h5 values reconstructed as z * win_std + win_mean, so the offline-vs-causal "
+          "difference also contains this normalisation difference; a station whose shifted similarity window does not fit in the cached "
+          "612 samples is not used by the similarity (the window end depends only on tau and the offline P and always fits, so this "
+          "happens only when the causal P is more than 2.8 s earlier than the offline P); "
+          "stations that were STA/LTA fallbacks offline enter the physics when 24_07 picked them; the West Tottori 2026 dev of 24_07 "
+          "(30 events) was run on z-scored values, so the reconstruction was checked on synthetic data only before this test",
+          "if 24_07 could not be run, its output failed the checks, the H5 computation raised an exception or the G-causal check on the "
+          "causal-pick path failed, H5 is reported as NOT-EVALUATED and H1-H4 are reported unchanged (preregistration 24, section 5.5)",
+          "H1 (C3 at tau = 2 s) is the primary test; H2, H3 and H4 are secondary at alpha 0.005; H5 (causal picks) uses the H1 rule at "
+          "alpha 0.01 as a realism check; everything else is descriptive"]
 ROOT = Path(__file__).resolve().parent.parent
@@ -131,3 +156,3 @@
 SELF_SHA = sha256(Path(__file__))
-print(f"[21_20] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
+print(f"[24_05] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
       f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")
@@ -136,3 +161,3 @@
 CP = ROOT / a.cache
-if not CP.exists(): raise SystemExit(f"[21_20] STOP: {a.cache} が無い(ノート 21_20_osaka2018_colab.ipynb のセル 11 で作った tottori_parsed_realpick_osaka2018_m15.pt を data/osaka2018_processed/ に置く)")
+if not CP.exists(): raise SystemExit(f"[24_05] STOP: {a.cache} が無い(ノート 24_nagano2014_colab.ipynb のセル N12 で作った tottori_parsed_realpick_nagano2014_m15_r1.pt を data/nagano2014_processed/ に置く)")
 EVS = torch.load(CP, map_location="cpu", weights_only=False)
@@ -141,7 +166,7 @@
     miss = [k for k in need if k not in e]
-    if miss: raise SystemExit(f"[21_20] STOP: キャッシュの地震に {miss} が無い(21_20c の出力か確かめる)")
+    if miss: raise SystemExit(f"[24_05] STOP: キャッシュの地震に {miss} が無い(24_03・24_03h の出力か確かめる)")
 for e in EVS:
     w_ = np.asarray(e["waveforms"])
-    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_20] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
-    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_20] STOP: {e['origin_time']} の波形に NaN か無限大")
+    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[24_05] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
+    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[24_05] STOP: {e['origin_time']} の波形に NaN か無限大")
 def to_ns(o):
@@ -153,3 +178,3 @@
     except Exception:
-        raise SystemExit(f"[21_20] STOP: origin_time {o!r} を時刻として読めない")
+        raise SystemExit(f"[24_05] STOP: origin_time {o!r} を時刻として読めない")
 OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
@@ -161,4 +186,4 @@
 if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
-    raise SystemExit("[21_20] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
-if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[21_20] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
+    raise SystemExit("[24_05] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
+if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[24_05] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
 # G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
@@ -169,10 +194,10 @@
 n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
-print(f"[21_20] 入力: 大阪府北部 2018 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
+print(f"[24_05] 入力: 長野県北部 2014 の M ≥ 1.5 版(R1 の後) {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
       f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
-print(f"[21_20] G-untouched: 期間 2018-06-15〜2018-07-12(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
+print(f"[24_05] G-untouched: 期間 2014-11-20〜2014-12-17(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
       + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
-if n_out != 0 or n_big != 1: raise SystemExit("[21_20] STOP(G-untouched): 大阪府北部 2018 のキャッシュに見えない(この行を貼って相談)")
+if n_out != 0 or n_big != 1: raise SystemExit("[24_05] STOP(G-untouched): 長野県北部 2014 のキャッシュに見えない(この行を貼って相談)")
 im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
 if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
-    raise SystemExit(f"[21_20] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2018-06-17 22:58 UTC の 1 分 ± 60 s。気象庁の発表の 07:58 JST)")
+    raise SystemExit(f"[24_05] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2014-11-22 13:08:17.9 UTC ± 60 s。24_00 の表示の 22:08:17.90 JST)")
 CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
@@ -180,5 +205,5 @@
 if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
-    raise SystemExit("[21_20] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
-print(f"[21_20] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
-print(f"[21_20] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
+    raise SystemExit("[24_05] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
+print(f"[24_05] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
+print(f"[24_05] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
       f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")
@@ -193,3 +218,3 @@
     kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
-    if len(set(kk)) != n: raise SystemExit(f"[21_20] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
+    if len(set(kk)) != n: raise SystemExit(f"[24_05] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
 HASP = ~np.isnan(TFIRST)
@@ -205,10 +230,48 @@
 EX, EY = to_xy(SRC[:, 0], SRC[:, 1])
-print(f"[21_20] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
+print(f"[24_05] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
 EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
-if len(EVAL) == 0: raise SystemExit("[21_20] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
-if a.dev: print(f"[21_20] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
+if len(EVAL) == 0: raise SystemExit("[24_05] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
+if a.dev: print(f"[24_05] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                 "(較正にも入っているので値は楽観的)")
 
+# ---------------------------------------------------------------- 24: H5 の材料(24_07 v3 の τ までの検測)を、開く前に確かめる
+CAUS = None                                   # H5 の計算の間だけ CAUS_ALL を入れる(それ以外は None で、21_20 と同じ計算)
+CP_C, CJ_C = ROOT / a.causal_picks, ROOT / a.causal_json
+H5_SKIP = None                                # H5 を評価しなかった理由(評価した時は None)
+if a.no_causal:
+    H5_SKIP = "--no-causal: 24_07 could not be run or its output failed the checks (preregistration 24, section 5.5)"
+    CAUS_ALL = {}
+    print("[24_05] --no-causal: 24_07 の出力を読まない。H5 は評価しない(NOT-EVALUATED)。H1〜H4・HL・HG は同じ規則で回す(事前登録 24 の 5.5 節)")
+elif not CP_C.exists() or not CJ_C.exists():
+    raise SystemExit(f"[24_05] STOP: 24_07 の出力 {a.causal_picks} か {a.causal_json} が無い(ノートの セル N16 の後に Mac にコピーする)")
+if not a.no_causal:
+    CJ = json.load(open(CJ_C))
+    if CJ.get("script_sha256") != CAUSAL_SCRIPT_SHA:
+        raise SystemExit(f"[24_05] STOP: 24_07 の SHA-256 {str(CJ.get('script_sha256'))[:12]}… が凍結の値 {CAUSAL_SCRIPT_SHA[:12]}… と違う")
+    if CJ.get("cache_sha256") != CACHE_SHA:
+        raise SystemExit(f"[24_05] STOP: 24_07 が使ったキャッシュの SHA-256 {str(CJ.get('cache_sha256'))[:12]}… が、このキャッシュ {CACHE_SHA[:12]}… と違う")
+    if CJ.get("csv_sha256") != sha256(CP_C):
+        raise SystemExit("[24_05] STOP: 24_07 の CSV の SHA-256 が、24_07 の JSON に書かれた値と違う(別の実行の CSV か JSON を置いた)")
+    if not CJ.get("all_events") or not CJ.get("raw_reconstructed"):
+        raise SystemExit("[24_05] STOP: 24_07 が --all-events で、元の値に戻した h5(24_02)で回されていない")
+    if len(set(OT)) != NE: raise SystemExit("[24_05] STOP: 発生時刻の同じ地震がキャッシュにある(24_07 の行を地震に対応付けられない)")
+    CAUS_ALL, _OTI = {}, {OT[i]: i for i in range(NE)}
+    with open(CP_C) as f:
+        for r in csv.DictReader(f):
+            ie_ = _OTI.get(r["origin_time"])
+            if ie_ is None: raise SystemExit(f"[24_05] STOP: 24_07 の地震 {r['origin_time']} がキャッシュに無い")
+            ff = lambda v: float(v) if v not in ("", "nan", None) else np.nan
+            CAUS_ALL.setdefault((ie_, float(r["tau"])), {})[int(r["k"])] = (ff(r["c_tp"]), ff(r["c_ts"]), ff(r["off_tp"]))
+    _miss = [(OT[ie][:19], t) for ie in EVAL for t in TAUS if (ie, float(t)) not in CAUS_ALL]
+    if _miss: raise SystemExit(f"[24_05] STOP: 24_07 の検測が無い地震・時点 {len(_miss)}(最初 {_miss[0]})。評価の全ての地震 × 4 時点が要る")
+    for ie in EVAL:
+        for t in TAUS:
+            d_ = CAUS_ALL[(ie, float(t))]; n_ = int(EVS[ie]["n_real_stations"]); tpo = np.asarray(EVS[ie]["tp_times"], float)[:n_]
+            for k_, v_ in d_.items():
+                if not (0 <= k_ < n_) or not (np.isnan(v_[2]) and np.isnan(tpo[k_]) or abs(v_[2] - tpo[k_]) < 1e-6):
+                    raise SystemExit(f"[24_05] STOP: 24_07 の局 {k_} のオフラインの P が、キャッシュと合わない({OT[ie][:19]})")
+    print(f"[24_05] H5 の材料: 24_07 v3 SHA-256 {CAUSAL_SCRIPT_SHA[:12]}…・同じキャッシュ・元の値に戻した h5・評価の {len(EVAL)} 地震 × 4 時点がそろっている")
+
 # ---------------------------------------------------------------- 1 回だけの記録(本番は、試験の地震の結果を計算する前に書く)
-OPEN = ROOT / "models/21_20_opened.json"
+OPEN = ROOT / "models/24_05_opened.json"
 SUF = "_dev" if a.dev else ""
@@ -216,11 +279,13 @@
     rec = json.load(open(OPEN)) if OPEN.exists() else []
-    rec.append(dict(utc=utcnow(), status=status, version=VERSION, script_sha256=SELF_SHA, cache_sha256=CACHE_SHA, suffix=SUF))
+    rec.append(dict(utc=utcnow(), status=status, version=VERSION, script_sha256=SELF_SHA, cache_sha256=CACHE_SHA, suffix=SUF,
+                    no_causal=bool(a.no_causal)))
     json.dump(rec, open(OPEN, "w"), indent=1)
 if not a.dev:
-    if OPEN.exists() or (ROOT / "models/21_20_judgment.json").exists():
+    if OPEN.exists() or (ROOT / "models/24_05_judgment.json").exists():
         SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
-        print(f"[21_20] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
+        print(f"[24_05] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
     log_open("opened")
+IN_H5 = False                                 # 24: H5 の計算の間は、止まった記録を書かない(H5 を NOT-EVALUATED にして続けるため)
 def stop(msg):
-    if not a.dev: log_open("stopped: " + msg[:160])
+    if not a.dev and not IN_H5: log_open("stopped: " + msg[:160])
     raise SystemExit(msg)
@@ -229,2 +294,3 @@
     """17_02 の picks_of と同じ(P は tp ≤ τ、S は tp + sp ≤ τ)。時刻は TFIRST を 0 にした値"""
+    if CAUS is not None and (ie, float(tau)) in CAUS: return picks_of_causal(ie, tau)      # 24: H5 の計算の間だけ
     e = EVS[ie]; n = int(e["n_real_stations"])
@@ -240,2 +306,16 @@
     return out
+def picks_of_causal(ie, tau):
+    """24(H5): 24_07 が T = TFIRST + τ までの波形だけで決めた P・S(局の並び・形は picks_of と同じ)。P は c_tp − TFIRST ≤ τ、
+    S は c_ts − TFIRST ≤ τ。オフラインの p_fallback・s_fallback は使わない(実時間では分からないため)"""
+    e = EVS[ie]; n = int(e["n_real_stations"]); loc = np.asarray(e["sta_locs"], float)[:n]; D = CAUS[(ie, float(tau))]
+    out = []
+    for k in range(n):
+        if k not in D: continue
+        ctp, cts, _ = D[k]; tpr = ctp - TFIRST[ie]
+        if not np.isfinite(tpr) or tpr > tau + EPS_T: continue
+        tsr = cts - TFIRST[ie] if np.isfinite(cts) else np.nan
+        wS = S_WEIGHT if (np.isfinite(tsr) and tsr <= tau + EPS_T) else 0.0
+        x, y = to_xy(loc[k, 0], loc[k, 1]); z = -float(loc[k, 2]) * EL_SCALE
+        out.append((skey(loc[k]), float(x), float(y), z, float(tpr), 1.0, float(tsr) if wS > 0 else np.nan, wS, k))
+    return out
 def n_phases(pk): return len(pk) + sum(1 for p in pk if p[7] > 0)
@@ -290,3 +370,3 @@
 LAP_B = float(np.median(np.abs(r1)) / np.log(2.0))
-print(f"[21_20] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
+print(f"[24_05] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
       f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")
@@ -301,3 +381,3 @@
 XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
-print(f"[21_20] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
+print(f"[24_05] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
       f"  固定の深さ {ZDEF:.1f} km")
@@ -337,3 +417,3 @@
 lls = {h: loo_ll(h) for h in HS}; KDE_H = max(lls, key=lls.get)
-print(f"[21_20] KDE の帯域(pool の一つ抜き): {KDE_H} km")
+print(f"[24_05] KDE の帯域(pool の一つ抜き): {KDE_H} km")
 def log_prior(nodes, mem):
@@ -365,3 +445,3 @@
     lib = np.where((OTNS <= OTNS[ie] - int(buffer_h * 3600e9)) & HASP)[0]
-    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_20] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
+    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[24_05] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
     return lib
@@ -413,2 +493,12 @@
     F = filt_cached(ie, band); out = []
+    if CAUS is not None and (ie, float(tau)) in CAUS:           # 24(H5): 窓を τ までの検測の P から切る(キャッシュの波形はオフラインの P が IP)
+        e = EVS[ie]; n = int(e["n_real_stations"]); tpo = np.asarray(e["tp_times"], float)[:n]
+        for p in picks_of(ie, tau):
+            nav = n_avail(tau, p[4])
+            if nav < MINW_N or p[0] not in F or not np.isfinite(tpo[p[8]]): continue
+            sh = int(round((p[4] + TFIRST[ie] - tpo[p[8]]) * FS))          # τ までの P − オフラインの P(サンプル)
+            a0, a1 = IP + sh - PRE_N, IP + sh + nav
+            if a0 < 0 or a1 > F[p[0]].shape[1]: continue                    # キャッシュの窓に収まらない局は使わない(限界に書く)
+            out.append((p[0], F[p[0]][:, a0:a1]))
+        return out
     for p in picks_of(ie, tau):
@@ -441,3 +531,3 @@
     top = lib[np.argsort(-S, kind="stable")[:min(k, pos)]]
-    if ie is not None and ie in top: stop("[21_20] STOP: 自分自身が似た地震の上位に入っている")
+    if ie is not None and ie in top: stop("[24_05] STOP: 自分自身が似た地震の上位に入っている")
     out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
@@ -458,3 +548,3 @@
     lib = library(ie); libb = library(ie, BUFFER_SENS_H)
-    if not np.array_equal(libb[:len(lib)], lib): stop("[21_20] STOP: 過去の一覧の並びがおかしい")
+    if not np.array_equal(libb[:len(lib)], lib): stop("[24_05] STOP: 過去の一覧の並びがおかしい")
     p0 = FIRST[ie]
@@ -501,4 +591,4 @@
 if NT < MIN_TEST and not a.dev:
-    print(f"[21_20] 判定(事前宣言、H1): INCONCLUSIVE(評価できる試験の地震 {NT} < {MIN_TEST})")
-    json.dump(dict(script="21_20_osaka2018_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, verdict="INCONCLUSIVE",
+    print(f"[24_05] 判定(事前宣言、H1): INCONCLUSIVE(評価できる試験の地震 {NT} < {MIN_TEST})")
+    json.dump(dict(script="24_05_nagano2014_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, verdict="INCONCLUSIVE",
                    utc=utcnow(), suffix=SUF, cache=a.cache, cache_sha256=sha256(CP), n_test=int(len(test_idx)),
@@ -506,3 +596,3 @@
                    n_mj2_library_only=n_extra2), limits=LIMITS),
-              open(ROOT / f"models/21_20_judgment{SUF}.json", "w"), indent=1)
+              open(ROOT / f"models/24_05_judgment{SUF}.json", "w"), indent=1)
     log_open("completed: INCONCLUSIVE"); raise SystemExit(0)
@@ -518,3 +608,3 @@
     except BaseException as ex:
-        stop(f"[21_20] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
+        stop(f"[24_05] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
     for m in METH: P[m][ii] = R[m]
@@ -529,3 +619,3 @@
 gate_ev = [ii for ii in range(NT) if NI[ii, TAUS.index(1.0)] > 0][:N_GATE]
-if len(gate_ev) < 3: stop(f"[21_20] STOP(G-causal): τ = 1 s で似ている度合いが測れた地震が {len(gate_ev)} しかなく、確かめられない")
+if len(gate_ev) < 3: stop(f"[24_05] STOP(G-causal): τ = 1 s で似ている度合いが測れた地震が {len(gate_ev)} しかなく、確かめられない")
 gc_max, gc_n, pos_ctrl = 0.0, 0, None
@@ -561,3 +651,3 @@
 shared = [p for p in picks_of(ie, 1.0) if n_avail(1.0, p[4]) >= MINW_N and any(p[0] in filt_cached(j, BAND) for j in lib0)]
-if not shared: stop("[21_20] STOP(G-causal): 陽性対照に使える局が無い(この行を貼って相談)")
+if not shared: stop("[24_05] STOP(G-causal): 陽性対照に使える局が無い(この行を貼って相談)")
 pc = shared[0]; e2 = dict(orig); W = np.array(np.asarray(orig["waveforms"], float))
@@ -568,5 +658,5 @@
 pos_ctrl = float(np.max(np.abs(S1 - S0))) if len(S0) else 0.0
-print(f"[21_20] G-causal({len(gate_ev)} 地震 × τ = 0.5・1・2・3 s、未来の波形と検測を置き換えた時の最大の差): {gc_max:.3g}  "
+print(f"[24_05] G-causal({len(gate_ev)} 地震 × τ = 0.5・1・2・3 s、未来の波形と検測を置き換えた時の最大の差): {gc_max:.3g}  "
       f"陽性対照(窓の最後の点を変えた時の S の差): {pos_ctrl:.3g}  " + ("PASS" if (gc_max == 0.0 and pos_ctrl > 0) else "FAIL"))
-if not (gc_max == 0.0 and pos_ctrl > 0): stop("[21_20] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")
+if not (gc_max == 0.0 and pos_ctrl > 0): stop("[24_05] STOP(G-causal): 未来の情報が結果に入っているか、ゲートが差を見落とす(この行を貼って相談)")
 
@@ -589,4 +679,5 @@
             for j, t in enumerate(TL)} for m in METH}
-def paired(A, B, j):
-    x, y = E[A][:, j], E[B][:, j]; m = np.isfinite(x) & np.isfinite(y); nz = int(np.sum(x[m] != y[m]))
+def paired(A, B, j, EE=None):
+    EE = E if EE is None else EE                                   # 24: 比べる誤差の表(既定は 21_20 と同じ E)
+    x, y = EE[A][:, j], EE[B][:, j]; m = np.isfinite(x) & np.isfinite(y); nz = int(np.sum(x[m] != y[m]))
     d = dict(n=int(m.sum()), n_nonzero=nz, p=None, median_diff_km=None, frac_better=None, frac_tied=None)
@@ -597,15 +688,16 @@
 phys_inf = SUMM["M5"]["inf"]["median_km"]
-print(f"[21_20] G-phys(τ = ∞ の M5 の中央値 ≤ 0.5 km): {'—' if phys_inf is None else f'{phys_inf:.3f}'} km  " + ("PASS" if phys_inf is not None and phys_inf <= 0.5 else "FAIL")
+print(f"[24_05] G-phys(τ = ∞ の M5 の中央値 ≤ 0.5 km): {'—' if phys_inf is None else f'{phys_inf:.3f}'} km  " + ("PASS" if phys_inf is not None and phys_inf <= 0.5 else "FAIL")
       + "(参考: 15_12 は 0.13 km、分け方が違う)")
-if not (phys_inf is not None and phys_inf <= 0.5): stop("[21_20] STOP(G-phys): 物理を大阪に正しく移せていない可能性(この行を貼って相談)")
-def judge(meth, t, alpha):
+if not (phys_inf is not None and phys_inf <= 0.5): stop("[24_05] STOP(G-phys): 物理を長野に正しく移せていない可能性(この行を貼って相談)")
+def judge(meth, t, alpha, EE=None, SS=None):
+    SS = SUMM if SS is None else SS                                # 24: 既定は 21_20 と同じ SUMM・E
     j = TL.index(t)
-    full = [m for m in BASE if SUMM[m][t]["available"] == 1.0 and SUMM[m][t]["median_km"] is not None]
-    best = min(full, key=lambda m: SUMM[m][t]["median_km"])
-    bm, cm = SUMM[best][t]["median_km"], SUMM[meth][t]["median_km"]
-    pr = paired(meth, best, j); floor = bm < FLOOR_KM
+    full = [m for m in BASE if SS[m][t]["available"] == 1.0 and SS[m][t]["median_km"] is not None]
+    best = min(full, key=lambda m: SS[m][t]["median_km"])
+    bm, cm = SS[best][t]["median_km"], SS[meth][t]["median_km"]
+    pr = paired(meth, best, j, EE); floor = bm < FLOOR_KM
     win = (not floor) and cm is not None and cm < bm and pr["p"] is not None and pr["p"] < alpha and pr["n_nonzero"] >= MIN_NONZERO
     return dict(method=meth, tau=t, alpha=alpha, best=best, best_median_km=bm, median_km=cm, paired_vs_best=pr, floor=bool(floor),
-                win=bool(win), at_or_below_0p7_best=bool(cm is not None and cm <= BAR * bm), vs_M6r=paired(meth, "M6r", j),
-                vs_M6p=paired(meth, "M6p", j))
+                win=bool(win), at_or_below_0p7_best=bool(cm is not None and cm <= BAR * bm), vs_M6r=paired(meth, "M6r", j, EE),
+                vs_M6p=paired(meth, "M6p", j, EE))
 PER_TAU = {}                       # 記述だけ(勝ち負けは HYP に書く)
@@ -629,5 +721,95 @@
 
+# ---------------------------------------------------------------- 24: H4(C3 対 C1)と H5(τ までの検測)
+def clean_early(o):
+    if isinstance(o, dict): return {str(k): clean_early(v) for k, v in o.items()}
+    if isinstance(o, (list, tuple)): return [clean_early(v) for v in o]
+    if isinstance(o, np.ndarray): return [clean_early(v) for v in o.tolist()]
+    if isinstance(o, (np.floating, float)): return None if not math.isfinite(float(o)) else float(o)
+    if isinstance(o, (np.integer,)): return int(o)
+    if isinstance(o, np.bool_): return bool(o)
+    return o
+def judge_vs(meth, other, t, alpha):
+    """H4: 両方に値がある地震で比べる。床の規則なし(BEST との比較でないため)"""
+    j = TL.index(t); x, y = E[meth][:, j], E[other][:, j]; m = np.isfinite(x) & np.isfinite(y)
+    pr = paired(meth, other, j)
+    cm = float(np.median(x[m])) if m.any() else None; om = float(np.median(y[m])) if m.any() else None
+    win = (cm is not None and om is not None and cm < om and pr["p"] is not None and pr["p"] < alpha and pr["n_nonzero"] >= MIN_NONZERO)
+    return dict(method=meth, other=other, tau=t, alpha=alpha, n_both=int(m.sum()), median_km=cm, other_median_km=om,
+                paired=pr, other_available_frac=float(np.mean(np.isfinite(y))), win=bool(win))
+HYP24 = {"H4": judge_vs(H4[1], H4[2], H4[3], ALPHA_SEC)}
+CM_C = BASE + NEW
+PC = {m: np.full((NT, len(TL), 2), np.nan) for m in CM_C}; NSTC = np.zeros((NT, len(TAUS)), int); NIC = np.zeros((NT, len(TAUS)), int)
+SMAXC = np.full((NT, len(TAUS)), np.nan); GC_C = None
+# H1〜H4 の結果を、H5 の計算の前に書いておく(H5 の計算で途切れても、H1〜H4 の結果が残る。最終の JSON は下の 12 節で書く)
+json.dump(clean_early(dict(script="24_05_nagano2014_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, suffix=SUF,
+                           status="H1-H4 written before H5; the final file is models/24_05_judgment" + SUF + ".json",
+                           summary=SUMM, hypotheses=HYP, verdict=VERDICT, hypotheses_24=HYP24, utc=utcnow())),
+          open(ROOT / f"models/24_05_judgment{SUF}_preH5.json", "w"), indent=1)
+def gate_causal_path():
+    """G-causal を H5 の経路(τ までの検測・ずらした窓)でも回す: 各局のキャッシュの波形のうち、時刻 T(= TFIRST + τ)より後の
+    サンプル(時刻が T を超えるもの。T 以前で最後のサンプルの次から)を全て乱数に置き換えても、H5 の結果が同じこと。キャッシュの波形はオフラインの P(IP)に合わせて並んでいるので、
+    T 以前で最後のサンプルの位置は floor(IP + (τ − (オフラインの P − TFIRST))·FS)(オフラインの P が T より後の局では IP より前)。
+    オフラインの P・S の時刻は、波形の位置の帳簿として残す(H5 の経路は 24_07 の P・S を使い、オフラインの P は窓の位置合わせに
+    だけ使う)。オフラインの P が無い局は全てを置き換える(似ている度合いには使われない)"""
+    mx, n_ = 0.0, 0
+    for ii in gate_ev:
+        ie = EVAL[ii]; orig = EVS[ie]
+        for t in ("0.5", "1", "2", "3"):
+            tau = float(t); jt = TL.index(t)
+            e2 = dict(orig); n = int(orig["n_real_stations"])
+            W = np.array(np.asarray(orig["waveforms"], float)); tp = np.asarray(orig["tp_times"], float); tpr = tp[:n] - TFIRST[ie]
+            for k in range(n):
+                cut = 0 if not np.isfinite(tpr[k]) else int(np.clip(IP + np.floor((tau - tpr[k]) * FS + 1e-3) + 1, 0, NTS))
+                W[k, :, cut:] = RNG_GATE.standard_normal((3, NTS - cut)) * 1e3
+            e2["waveforms"] = W
+            EVS[ie] = e2; [FILT.pop((ie, b), None) for b in SOS]
+            try:
+                R2, X2 = eval_event(ie, only_tau=t)
+            finally:
+                EVS[ie] = orig; [FILT.pop((ie, b), None) for b in SOS]
+            for m in CM_C:
+                a1, a2 = PC[m][ii, jt], R2[m][jt]
+                if np.isnan(a1).any() != np.isnan(a2).any(): mx = np.inf
+                elif not np.isnan(a1).any(): mx = max(mx, float(np.max(np.abs(a1 - a2))))
+            j0 = TAUS.index(tau)
+            if np.isfinite(SMAXC[ii, j0]) or np.isfinite(X2["smax"][j0]):
+                mx = max(mx, abs(np.nan_to_num(SMAXC[ii, j0], nan=-9.0) - np.nan_to_num(X2["smax"][j0], nan=-9.0)))
+            n_ += 1
+    return mx, n_
+if H5_SKIP is None:
+    CAUS = CAUS_ALL; T_C = time.time(); IN_H5 = True
+    try:
+        for ii, ie in enumerate(EVAL):
+            Rc, Xc = eval_event(ie)
+            for m in CM_C: PC[m][ii] = Rc[m]
+            NSTC[ii] = Xc["nst"][:len(TAUS)]; NIC[ii] = Xc["ni"]; SMAXC[ii] = Xc["smax"]
+            if (ii + 1) % 10 == 0:
+                print(f"  … H5 {ii+1}/{NT}  (残りの見込み約 {(time.time() - T_C) / (ii + 1) * (NT - ii - 1) / 60:.0f} 分)")
+        gc_c, gc_cn = gate_causal_path()
+        GC_C = dict(max_diff=gc_c, n_checks=gc_cn)
+        print(f"[24_05] G-causal(H5 の経路: τ までの検測・ずらした窓、{len(gate_ev)} 地震 × 4 時点): {gc_c:.3g}  " + ("PASS" if gc_c == 0.0 else "FAIL"))
+        if gc_c != 0.0: H5_SKIP = "G-causal on the causal-pick path failed (max difference %.3g)" % gc_c
+    except (Exception, SystemExit) as ex:        # H5 だけを評価しないで、H1〜H4 の結果は残す(事前登録 24 の 5.5 節)。Ctrl-C は止まる
+        H5_SKIP = f"{'stop' if isinstance(ex, SystemExit) else 'exception'} during the H5 computation: {type(ex).__name__}: {str(ex)[:200]}"
+    CAUS = None; FILT.clear(); IN_H5 = False
+    if H5_SKIP is not None: print(f"[24_05] H5 は評価しない(NOT-EVALUATED): {H5_SKIP}")
+EC = {m: herr(PC[m]) for m in CM_C}
+for m in CM_C: EC[m][:, TL.index("inf")] = np.nan                  # 全検測(τ = ∞)はオフラインの検測なので H5 の表には入れない
+if H5_SKIP is not None:
+    for m in CM_C: EC[m][:] = np.nan
+SUMMC = {m: {t: dict(zip(("median_km", "ci_lo", "ci_hi"), med_ci(EC[m][:, j])), available=float(np.mean(np.isfinite(EC[m][:, j]))))
+             for j, t in enumerate(TL[:-1])} for m in CM_C}
+if H5_SKIP is None:
+    HYP24["H5"] = judge(H5[1], H5[2], ALPHA, EC, SUMMC)
+    PER_TAU_C = {t: dict(C3=judge("C3", t, ALPHA, EC, SUMMC), stations_median=float(np.median(NSTC[:, j])),
+                         similarity_measured_frac=float(np.mean(NIC[:, j] > 0)),
+                         stations_median_offline=float(np.median(NST[:, j]))) for j, t in enumerate(TL[:-1])}
+    for t in PER_TAU_C: PER_TAU_C[t]["C3"].pop("win"); PER_TAU_C[t]["C3"].pop("alpha")
+else:
+    HYP24["H5"] = dict(method=H5[1], tau=H5[2], alpha=ALPHA, status="NOT-EVALUATED", reason=H5_SKIP, win=False)
+    PER_TAU_C = {}
+
 def f2(v): return "—" if v is None else f"{v:.2f}"
 def fp(p): return "—" if p is None else f"{p:.2g}"
-print(f"\n[21_20] ===== 水平誤差の中央値 km [95% 区間](評価 {NT} 地震{'、dev(楽観的)' if a.dev else ''}) =====")
+print(f"\n[24_05] ===== 水平誤差の中央値 km [95% 区間](評価 {NT} 地震{'、dev(楽観的)' if a.dev else ''}) =====")
 print("  方法           " + "".join(f"{('τ=' + t + ' s') if t != 'inf' else '全検測':>24}" for t in TL))
@@ -649,3 +831,3 @@
       "(全検測でも C4 が物理より良いなら、その分は早さではなく気象庁の震源の枠に合わせた効果の可能性)")
-print(f"\n[21_20] ===== 事前宣言の判定 =====")
+print(f"\n[24_05] ===== 事前宣言の判定 =====")
 for name, h in HYP.items():
@@ -655,4 +837,16 @@
           f"→ {'勝ち' if h['win'] else '勝ちなし'}")
-print(f"\n[21_20] 判定(事前宣言、H1): {VERDICT}")
-print("[21_20] 限界: " + " / ".join(LIMITS))
+h4, h5 = HYP24["H4"], HYP24["H5"]
+print(f"  H4(副): C3 対 C1 @ τ = {h4['tau']} s(両方に値がある {h4['n_both']} 地震。C1 がある割合 {h4['other_available_frac']:.2f})  "
+      f"C3 {f2(h4['median_km'])} km 対 C1 {f2(h4['other_median_km'])} km  p = {fp(h4['paired']['p'])}(基準 {h4['alpha']})  "
+      f"差が 0 でない組 {h4['paired']['n_nonzero']}  → {'勝ち' if h4['win'] else '勝ちなし'}")
+if H5_SKIP is None:
+    print(f"  H5(副): τ までの波形だけの検測で C3 @ τ = {h5['tau']} s  {f2(h5['median_km'])} km 対 BEST {h5['best']} {h5['best_median_km']:.2f} km  "
+          f"p = {fp(h5['paired_vs_best']['p'])}(基準 {h5['alpha']})  差が 0 でない組 {h5['paired_vs_best']['n_nonzero']}  FLOOR={h5['floor']}  "
+          f"→ {'勝ち' if h5['win'] else '勝ちなし'}")
+else:
+    print(f"  H5(副): NOT-EVALUATED(評価しなかった。理由: {H5_SKIP})")
+print("  τ までの検測(記述): " + "  ".join(f"τ={t}: 局 {d['stations_median']:g}(オフライン {d['stations_median_offline']:g})・BEST {d['C3']['best']} "
+                                        f"{d['C3']['best_median_km']:.2f}・C3 {f2(d['C3']['median_km'])} km" for t, d in PER_TAU_C.items()))
+print(f"\n[24_05] 判定(事前宣言、H1): {VERDICT}")
+print("[24_05] 限界: " + " / ".join(LIMITS))
 
@@ -668,3 +862,3 @@
 CM = BASE + NEW + SENSN + ALLP
-with open(ROOT / f"data/21_20_per_event{SUF}.csv", "w", newline="") as f:
+with open(ROOT / f"data/24_05_per_event{SUF}.csv", "w", newline="") as f:
     w = csv.writer(f)
@@ -673,3 +867,4 @@
                + [f"c4_n_corrected_t{t}" for t in TL[:-1]]
-               + [f"{m}_err_t{t}" for m in CM for t in (TL if m in BASE else ["inf"] if m in ALLP else TL[:-1])])
+               + [f"{m}_err_t{t}" for m in CM for t in (TL if m in BASE else ["inf"] if m in ALLP else TL[:-1])]
+               + [f"n_sta_causal_t{t}" for t in TL[:-1]] + [f"{m}_causal_err_t{t}" for m in CM_C for t in TL[:-1]])
     for i, ie in enumerate(EVAL):
@@ -679,5 +874,7 @@
                    + [("" if not np.isfinite(E[m][i, j]) else f"{E[m][i, j]:.4f}") for m in CM
-                      for j in (range(len(TL)) if m in BASE else [ji] if m in ALLP else range(len(TAUS)))])
-out = dict(script="21_20_osaka2018_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
-           sequence="Northern Osaka 2018", suffix=SUF, cache=a.cache, cache_sha256=sha256(CP),
+                      for j in (range(len(TL)) if m in BASE else [ji] if m in ALLP else range(len(TAUS)))]
+                   + [(int(v) if H5_SKIP is None else "") for v in NSTC[i]] + [("" if not np.isfinite(EC[m][i, j]) else f"{EC[m][i, j]:.4f}") for m in CM_C
+                                                  for j in range(len(TAUS))])
+out = dict(script="24_05_nagano2014_similarity_confirmation.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
+           sequence="Northern Nagano 2014", suffix=SUF, cache=a.cache, cache_sha256=sha256(CP),
            n_fresh=int(FRESH.sum()), n_events=NE, n_pool=int(len(pool_idx)), n_test=int(len(test_idx)),
@@ -696,2 +893,7 @@
            summary=SUMM, per_tau=PER_TAU, all_picks=ALLPICKS, hypotheses=HYP, verdict=VERDICT,
+           hypotheses_24=HYP24, causal=dict(evaluated=H5_SKIP is None, not_evaluated_reason=H5_SKIP, no_causal_option=bool(a.no_causal),
+                                            script_sha256=CAUSAL_SCRIPT_SHA, picks_csv=a.causal_picks,
+                                            picks_csv_sha256=(sha256(CP_C) if CP_C.exists() and not a.no_causal else None),
+                                            json_sha256=(sha256(CJ_C) if CJ_C.exists() and not a.no_causal else None),
+                                            gate_causal_path=GC_C, summary=SUMMC, per_tau=PER_TAU_C),
            untouched=dict(n_outside_period=n_out, n_mj_ge_6=n_big, n_mj2_library_only=n_extra2),
@@ -702,5 +904,9 @@
                         "fewer than 30 evaluated events. H2: C4 at tau = 2 s, H3: C3 at tau = 0.5 s, each alpha 0.005 (secondary). "
-                        "Test events: 1.5 <= Mj < 2.0 events later than mainshock + 72 h (Northern Osaka 2018; same rule as 21_02 v2 and 21_04 v1)",
+                        "Test events: 1.5 <= Mj < 2.0 events later than mainshock + 72 h (Northern Nagano 2014; same rule as 21_02 v2, 21_04 v1 and 21_20 v1). "
+                        "Added in preregistration 24: H4 (secondary, alpha 0.005): C3 vs C1 at tau = 2 s on events where both exist, "
+                        "win if the C3 median < the C1 median, one-sided paired Wilcoxon p < 0.005 and >= 10 non-zero pairs (no floor rule). "
+                        "H5 (secondary, alpha 0.01): every method recomputed with 24_07 picks made from data up to T = first P + tau; "
+                        "C3 vs BEST (BEST chosen on these picks) at tau = 2 s with the H1 rule including the floor",
            limits=LIMITS, runtime_s=time.time() - T0)
-json.dump(clean(out), open(ROOT / f"models/21_20_judgment{SUF}.json", "w"), indent=1)
+json.dump(clean(out), open(ROOT / f"models/24_05_judgment{SUF}.json", "w"), indent=1)
 if not a.dev: log_open("completed: " + VERDICT)
@@ -735,6 +941,6 @@
 ax.set_xlabel("Time since first P pick, tau (s)"); ax.set_ylabel("Median epicentral error vs JMA (km)")
-ax.set_title(f"Northern Osaka 2018, {'DEV (pool events, optimistic)' if a.dev else 'test events'}, n = {NT}; shading = 95% bootstrap CI",
+ax.set_title(f"Northern Nagano 2014, {'DEV (pool events, optimistic)' if a.dev else 'test events'}, n = {NT}; shading = 95% bootstrap CI",
              fontsize=10)
 ax.grid(alpha=0.3, which="both"); ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_20_F1_error_vs_tau{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F1_error_vs_tau{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
 
@@ -754,3 +960,3 @@
 fig.legend(h_, l_, loc="lower center", bbox_to_anchor=(0.5, -0.06), ncol=2, fontsize=8, frameon=False)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_20_F2_paired_difference{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F2_paired_difference{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
 
@@ -764,4 +970,21 @@
 ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_20_F3_similarity_vs_separation{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"[21_20] 出力: models/21_20_judgment{SUF}.json, data/21_20_per_event{SUF}.csv, PDF/21_20_F1〜F3{SUF}.pdf"
-      + ("" if a.dev else ", models/21_20_opened.json") + f"  ({time.time()-T0:.0f} s)")
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F3_similarity_vs_separation{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig, ax = plt.subplots(figsize=(7.8, 4.4))
+for lab_, S_, ls_ in ((("offline picks", SUMM, "-"),) + ((("picks from data up to T only (H5)", SUMMC, "--"),) if H5_SKIP is None else ())):
+    bb = [PER_TAU[t]["C3"]["best"] if S_ is SUMM else PER_TAU_C[t]["C3"]["best"] for t in TT]
+    ax.plot(xs, [S_[b][t]["median_km"] if S_[b][t]["median_km"] is not None else np.nan for b, t in zip(bb, TT)], ls_, color="k", marker="s",
+            ms=5, label=f"BEST, {lab_}")
+    ax.plot(xs, [S_["C3"][t]["median_km"] if S_["C3"][t]["median_km"] is not None else np.nan for t in TT], ls_, color="tab:red", marker="o",
+            ms=5, label=f"C3, {lab_}")
+ax.axhline(FLOOR_KM, color="0.4", lw=0.8, ls=":")
+ax.text(xs[-1] / 1.03, FLOOR_KM * 1.06, f"floor {FLOOR_KM} km", fontsize=8, ha="right", va="bottom")
+ax.set_xscale("log"); ax.set_yscale("log"); ax.set_xticks(xs); ax.set_xticklabels([f"{t:g}" for t in TAUS]); ax.minorticks_off()
+_lo, _hi = ax.get_ylim(); _yt = [v for v in (0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50) if _lo <= v <= _hi]
+ax.set_yticks(_yt); ax.set_yticklabels([f"{v:g}" for v in _yt])
+ax.set_xlabel("Time since first P pick, tau (s)"); ax.set_ylabel("Median epicentral error vs JMA (km)")
+ax.set_title(f"Northern Nagano 2014, {'DEV' if a.dev else 'test'} events (n = {NT}): offline vs causal picks"
+             + ("" if H5_SKIP is None else "\n(H5 not evaluated: causal picks not available)"), fontsize=10)
+ax.grid(alpha=0.3, which="both"); ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), fontsize=8, frameon=False)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_05_F4_causal_picks{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"[24_05] 出力: models/24_05_judgment{SUF}.json, data/24_05_per_event{SUF}.csv, PDF/24_05_F1〜F4{SUF}.pdf"
+      + ("" if a.dev else ", models/24_05_opened.json") + f"  ({time.time()-T0:.0f} s)")
```

## 24_06f_nagano2014_learned_test.py ← 21_20f_osaka2018_learned_test.py

```diff
--- osaka/21_20f_osaka2018_learned_test.py	2026-11-01 23:42:18.946572246 +0000
+++ nagano/frz/24_06f_nagano2014_learned_test.py	2026-11-15 05:21:00.096885666 +0000
@@ -2,26 +2,17 @@
 # =============================================================================
-# Script : 21_20f_osaka2018_learned_test.py  (v1)
-#          [学習型 ARGUS の 3 つ目の系列での試験: 鳥取 2026 で学習して凍結した「似た地震の選び方」(21_06a のモデル)を、学び直さずに、
-#           手を付けていない大阪府北部 2018 で 1 回だけ試す。位置は C3・C4 と同じ物理の計算で決める(AI は物理の部品)]
-# Project: ARGUS(新生)— 学習した部品が 3 つ目の余震系列でも物理だけより良いか
-# 派生元 : 21_06b_ct2016_learned_test.py v1(SHA-256 442c411945f288cfff7f14490ee9826ffcfe055e5a79cc2af0c39fe93cb5bfea)。
+# Script : 24_06f_nagano2014_learned_test.py  (v1)
+#          [学習型 ARGUS の 4 つ目の系列での試験: 鳥取 2026 で学習して凍結した「似た地震の選び方」(21_06a のモデル)を、学び直さずに、
+#           手を付けていない長野県北部 2014 で 1 回だけ試す。位置は C3・C4 と同じ物理の計算で決める(AI は物理の部品)]
+# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の学習型の腕
+# 派生元 : 21_20f_osaka2018_learned_test.py v1(SHA-256 9623695ea33bef90605cd47d4fb8fceb16a8bbbe91327bfa51783aa347d29925)。
+#          21_06 FEATURES の印の間・凍結したモデル・学習の記録・G-model・仮説と判定の規則は 1 字も変えていない。変えたのは次だけ(DIFF_LOG_24.md):
+#          (1) 入力の既定のキャッシュ(24_05 と同じ R1 の後のもの)、MAIN_UTC・UNTOUCHED_UTC(24_05 と同じ)、限界の文(24_05 と同じ LIMITS)
+#          (2) 比べる相手と順番の確かめを 21_20 の出力から 24_05 の出力に変えた: data/24_05_per_event.csv(--dev は _dev)、
+#              models/24_05_judgment.json(最初の本番で、キャッシュの SHA-256 が同じこと)、models/24_05_opened.json(21_06a の学習が先か)
+#          (3) 出力の名前: models/24_06f_judgment.json / models/24_06f_opened.json / data/24_06f_per_event.csv / PDF/24_06f_F1_learned_test.pdf、
+#              表示の [24_06f]、系列の名前。記述用の L3p・L4p は「2026 の学習の行 + 2014 の pool の行」で学び直す(判定には使わない)
+#          (4) --ref-suffix(24_06g と同じ)と、24_05 の結果が凍結した 24_05 v1(SHA_2405)のものかの照合: 24_05 を事前登録 24 の 6 節の機械的な中断で 1 回やり直した時だけ、正式な結果の suffix
+#              (_rerun_<UTC>)を渡す。models/24_05_opened.json で最初に completed になった実行の suffix と一致しなければ STOP
 #
-# なぜ編集が要ったか: 21_06b v1 の引数は --cache・--dev・--train-json だけで、本震の時刻・G-untouched の期間・比べる相手の 21_04 の
-#   出力の名前(data/21_04_per_event.csv・models/21_04_judgment.json・models/21_04_opened.json)・自分の出力の名前
-#   (models/21_06b_*.json など)がスクリプトに書き込まれている。そのまま回すと大阪のキャッシュで STOP するか、21_06b の記録を壊す。
-#
-# 21_06b v1 から変えたこと(これ以外は 1 字も変えていない。DIFF_LOG.md):
-#   1. 入力の既定のキャッシュ: data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt(21_20 と同じもの)。
-#   2. MAIN_UTC・UNTOUCHED_UTC を 21_20 と同じ値にした(2018-06-17 22:58:30 UTC ± 60 s。秒までの発生時刻ではない。21_20 の冒頭を見る)。
-#   3. 比べる相手と順番の確かめを 21_04 の出力から 21_20 の出力に変えた: data/21_20_per_event.csv(--dev は _dev)、
-#      models/21_20_judgment.json(最初の本番で、キャッシュの SHA-256 が同じこと)、models/21_20_opened.json(21_06a の学習が先か)。
-#   4. 出力の名前: models/21_20f_judgment.json / models/21_20f_opened.json / data/21_20f_per_event.csv / PDF/21_20f_F1_learned_test.pdf
-#      (--dev では _dev、2 回目以降は _rerun_<UTC の時刻>)。表示の [21_20f]。
-#   5. 限界の文・表示・図の題の系列の名前を大阪府北部 2018 にした。記述用の L3p・L4p は「2026 の学習の行 + 2018 の pool の行」で学び直す
-#      (21_06b と同じ作り方。判定には使わない)。
-#   変えていないもの: 21_06 FEATURES の印の間(1 字も変えない。G-feat で学習の記録 models/21_06a_train.json の
-#   feature_block_sha256 = 9905420e546d… と照合する)、凍結したモデル models/21_06_ranker.pkl(学び直さない)、学習の記録、
-#   G-model(scikit-learn・numpy の版が学習時と同じでなければ STOP。学習した Mac の ~/SWIFT の環境で回す)、仮説と判定の規則。
-#
-# 事前登録の仮説と判定(21_06 と同じ。事前登録の記録 21_20 に再掲):
+# 事前登録の仮説と判定(21_06・21_20f と同じ。事前登録の記録 24 に再掲):
 #   HL1(主)  L4 @ τ = 2 s が BEST より良い、p < 0.01、BEST ≥ 0.5 km  → LEARNED-CONFIRMED / PHYSICS-AT-FLOOR / NOT-CONFIRMED
@@ -31,10 +22,8 @@
 #
-# Usage : (21_20 の本番が終わってから)
-#         cd ~/SWIFT && caffeinate -i uv run python src/21_20f_osaka2018_learned_test.py --dev   (動作確認。21_20 の dev の CSV が要る)
-#         cd ~/SWIFT && caffeinate -i uv run python src/21_20f_osaka2018_learned_test.py         (本番。1 回だけ)
-# 入力  : 21_20 と同じキャッシュ、data/21_20_per_event.csv と models/21_20_judgment.json・models/21_20_opened.json(--dev なら _dev の CSV)、
+# Usage : (24_05 の本番が終わってから)
+#         cd ~/SWIFT && caffeinate -i uv run python src/24_06f_nagano2014_learned_test.py --dev   (動作確認。24_05 の dev の CSV が要る)
+#         cd ~/SWIFT && caffeinate -i uv run python src/24_06f_nagano2014_learned_test.py         (本番。1 回だけ)
+# 入力  : 24_05 と同じキャッシュ、data/24_05_per_event.csv と models/24_05_judgment.json・models/24_05_opened.json(--dev なら _dev の CSV)、
 #         models/21_06a_train.json・models/21_06_ranker.pkl・data/21_06a_train_rows.npz(21_06a の出力。凍結 B のまま)
-# Output: models/21_20f_judgment.json / models/21_20f_opened.json / data/21_20f_per_event.csv / PDF/21_20f_F1_learned_test.pdf
-# 止める条件(STOP): 21_06b と同じもの(21_20 と同じ入力のゲート・G-feat・G-model・21_20 の CSV が無いか地震が合わない・キャッシュが 21_20 と違う・G-same)
-# 所要  : 参考: 21_06b の本番は試験 307 地震で 506 s(models/21_06b_judgment.json の runtime_s)
+# Output: models/24_06f_judgment.json / models/24_06f_opened.json / data/24_06f_per_event.csv / PDF/24_06f_F1_learned_test.pdf
 # =============================================================================
@@ -49,4 +38,6 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--cache", default="data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt", help="21_20c(15_01c v3.3 と同じ計算)の大阪府北部 2018 の M>=1.5 版")
-ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(21_20 の dev と同じ 20 地震。比べる相手は data/21_20_per_event_dev.csv)")
+ap.add_argument("--cache", default="data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt", help="24_03(15_01c v3.3 と同じ計算)の長野県北部 2014 の M>=1.5 版に 24_03h の R1 を当てたもの(24_05 と同じ)")
+ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(24_05 の dev と同じ 20 地震。比べる相手は data/24_05_per_event_dev.csv)")
+SHA_2405 = "c10d15fe404309d836fc83fb2dbe1d207fa477d9597900724f487ef965970f9f"                          # 事前登録 24 で凍結した 24_05 v1 の SHA-256(24_06g・24_08 と同じ照合)
+ap.add_argument("--ref-suffix", default="", help="24_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
 ap.add_argument("--train-json", default="models/21_06a_train.json", help="21_06a の学習の記録(凍結したモデルの SHA-256 を持つ)")
@@ -70,8 +61,9 @@
 NBOOT, SEED, N_DEV, N_GATE = 2000, 12, 20, 5
-MAIN_UTC = dt.datetime(2018, 6, 17, 22, 58, 30)   # 21_20 と同じ: 気象庁の発表の 07:58 JST の 1 分の真ん中(秒までの値ではない。±60 s でこの 1 分を含む)。要確認
-UNTOUCHED_UTC = (dt.datetime(2018, 6, 15), dt.datetime(2018, 7, 12))     # G-untouched: 21_20a の期間(本震の 2 日前〜24 日後)を含む
-LIMITS = ["third sequence: Northern Osaka 2018 (mainshock 2018-06-18, 07:58 JST; origin time and Mj are those of the JMA catalogue, "
-          "see 21_20a's JSON), never used in ARGUS development; the hypotheses were fixed on West Tottori 2026 (21_01/21_02), "
-          "tested on Central Tottori 2016 (21_04, run with a documented deviation) and are applied here unchanged",
-          "one third sequence only",
+MAIN_UTC = dt.datetime(2014, 11, 22, 13, 8, 17, 900000)   # 24_05 と同じ: 24_00 の表示の本震 2014-11-22 22:08:17.90 JST(± 60 s、Mj ≥ 6.0 の確かめ)
+UNTOUCHED_UTC = (dt.datetime(2014, 11, 20), dt.datetime(2014, 12, 17))     # G-untouched: 24_01 の期間(本震の 2 日前〜24 日後)を日の単位で含む
+LIMITS = ["fourth sequence: Northern Nagano 2014 (mainshock 2014-11-22, 22:08:17.90 JST, Mj 6.7; JMA catalogue values, see 24_01's JSON), "
+          "never used in ARGUS development; the hypotheses H1-H3 were fixed on West Tottori 2026 (21_01/21_02), tested on Central Tottori 2016 "
+          "(21_04, with a documented deviation) and Northern Osaka 2018 (21_20, re-registered with amendment 04) and are applied here unchanged",
+          "one fourth sequence only; before this preregistration the catalogue h2014 was opened once by 24_00 to count events "
+          "(counts and the mainshock row only; no location list, waveform or method error was looked at)",
           "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
@@ -79,15 +71,14 @@
           "waveforms were downloaded around catalogue events only and converted to the West Tottori 2026 h5 form (30-s windows, "
-          "per-window per-component z-score, JST epoch); whether a filter was applied before the z-score in the 2026 h5 is not recorded "
-          "(none here; compared in 21_20b G-spec)",
-          "the cache was built by 21_20c, whose picking, QC and assembly are identical to 15_01c v3.3 (itself identical to v3 except "
-          "the window-index file name and output folder); 21_20c changed only labels, defaults and required arguments",
-          "catalogue: JMA hypocentres from h2018 (whether h2018 is the final stage is to be confirmed; West Tottori 2026 used the "
-          "unified catalogue); past-event locations are JMA "
+          "per-window per-component z-score, JST epoch; 24_02 also stores the window mean and standard deviation); no filter was applied "
+          "before the z-score (compared in 24_02 G-spec)",
+          "the cache was built by 24_03, whose picking, QC and assembly are identical to 15_01c v3.3; 24_03h then removed every event "
+          "with another catalogue event from 15 s before to 5 s after its origin (rule R1 of 21_20 amendment 04, fixed here before any "
+          "Nagano waveform was opened; it uses origin times and Mj only), which can bias the sample against busy periods",
+          "catalogue: JMA hypocentres from h2014 (whether h2014 is the final stage is to be confirmed); past-event locations are JMA "
           "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
-          "the 2018 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
-          "events; whether the 2026 catalogue excluded them is not recorded. Manual and automatic hypocentres are mixed (per-flag "
-          "counts in 21_20a's JSON)",
-          "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); the 2026 station list's "
-          "convention is not recorded; static station terms absorb a constant offset",
-          "offline PhaseNet picks on full records (possibly better than real-time picks); every method uses the same picks",
+          "the 2014 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
+          "events. Manual and automatic hypocentres can be mixed (per-flag counts in 24_01's JSON)",
+          "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); "
+          "static station terms absorb a constant offset",
+          "H1-H4 use offline PhaseNet picks on full records (possibly better than real-time picks); every method uses the same picks",
           "cache keeps up to 24 stations per event (PhaseNet P first, earliest first); no not-yet-arrived information is used",
@@ -101,7 +92,14 @@
           "C4's station terms come from past events' JMA hypocentres and truth is also JMA, so part of a C4 gain can be agreement with "
-          "the JMA frame rather than better early information",
+          "the JMA frame rather than better early information; C3all/C4all at all picks are reported to show this",
           "C4 corrects only arrived stations held by >= 3 top similar events; each past event's terms are demeaned by its own median "
           "P residual over all its stations, while uncorrected stations keep only the static term",
-          "H1 (C3 at tau = 2 s) is the primary test; H2 and H3 are secondary at alpha 0.005; everything else is descriptive"]
-
+          "H4 compares C3 with C1 (the JMA epicentre of the most similar past event, the 'search the most similar past event' approach) "
+          "on the events where C1 exists (C1 is undefined when fewer than 5 past events have a positive similarity)",
+          "H5 re-runs every method with picks made by 24_07 from data up to T only (T = first offline P + tau); the tau origin, the "
+          "station set (the cache stations) and the P search band (relative to the catalogue origin) still come from the offline picks "
+          "and the catalogue; no Wadati QC or STA/LTA fallback at each time; the similarity windows start at the causal P; stations "
+          "picked causally but without an offline PhaseNet P are used by the physics but not by the similarity; past events keep their "
+          "offline picks (their records are complete at the time of the target event)",
+          "H1 (C3 at tau = 2 s) is the primary test; H2, H3 and H4 are secondary at alpha 0.005; H5 (causal picks) uses the H1 rule at "
+          "alpha 0.01 as a realism check; everything else is descriptive"]
 ROOT = Path(__file__).resolve().parent.parent
@@ -117,3 +115,3 @@
 SELF_SHA = sha256(Path(__file__))
-print(f"[21_20f] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
+print(f"[24_06f] 本スクリプト {VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
       f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")
@@ -122,3 +120,3 @@
 CP = ROOT / a.cache
-if not CP.exists(): raise SystemExit(f"[21_20f] STOP: {a.cache} が無い(ノート 21_20_osaka2018_colab.ipynb のセル 11 で作った tottori_parsed_realpick_osaka2018_m15.pt を data/osaka2018_processed/ に置く)")
+if not CP.exists(): raise SystemExit(f"[24_06f] STOP: {a.cache} が無い(ノート 24_nagano2014_colab.ipynb のセル N12 で作った tottori_parsed_realpick_nagano2014_m15_r1.pt を data/nagano2014_processed/ に置く)")
 EVS = torch.load(CP, map_location="cpu", weights_only=False)
@@ -127,7 +125,7 @@
     miss = [k for k in need if k not in e]
-    if miss: raise SystemExit(f"[21_20f] STOP: キャッシュの地震に {miss} が無い(21_20c の出力か確かめる)")
+    if miss: raise SystemExit(f"[24_06f] STOP: キャッシュの地震に {miss} が無い(24_03・24_03h の出力か確かめる)")
 for e in EVS:
     w_ = np.asarray(e["waveforms"])
-    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[21_20f] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
-    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[21_20f] STOP: {e['origin_time']} の波形に NaN か無限大")
+    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[24_06f] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
+    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[24_06f] STOP: {e['origin_time']} の波形に NaN か無限大")
 def to_ns(o):
@@ -139,3 +137,3 @@
     except Exception:
-        raise SystemExit(f"[21_20f] STOP: origin_time {o!r} を時刻として読めない")
+        raise SystemExit(f"[24_06f] STOP: origin_time {o!r} を時刻として読めない")
 OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
@@ -147,4 +145,4 @@
 if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
-    raise SystemExit("[21_20f] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
-if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[21_20f] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
+    raise SystemExit("[24_06f] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
+if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[24_06f] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
 # G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
@@ -155,10 +153,10 @@
 n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
-print(f"[21_20f] 入力: 大阪府北部 2018 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
+print(f"[24_06f] 入力: 長野県北部 2014 の M ≥ 1.5 版(R1 の後) {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
       f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
-print(f"[21_20f] G-untouched: 期間 2018-06-15〜2018-07-12(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
+print(f"[24_06f] G-untouched: 期間 2014-11-20〜2014-12-17(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
       + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
-if n_out != 0 or n_big != 1: raise SystemExit("[21_20f] STOP(G-untouched): 大阪府北部 2018 のキャッシュに見えない(この行を貼って相談)")
+if n_out != 0 or n_big != 1: raise SystemExit("[24_06f] STOP(G-untouched): 長野県北部 2014 のキャッシュに見えない(この行を貼って相談)")
 im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
 if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
-    raise SystemExit(f"[21_20f] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2018-06-17 22:58 UTC の 1 分 ± 60 s。気象庁の発表の 07:58 JST)")
+    raise SystemExit(f"[24_06f] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2014-11-22 13:08:17.9 UTC ± 60 s。24_00 の表示の 22:08:17.90 JST)")
 CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
@@ -166,5 +164,5 @@
 if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
-    raise SystemExit("[21_20f] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
-print(f"[21_20f] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
-print(f"[21_20f] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
+    raise SystemExit("[24_06f] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
+print(f"[24_06f] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
+print(f"[24_06f] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
       f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")
@@ -179,3 +177,3 @@
     kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
-    if len(set(kk)) != n: raise SystemExit(f"[21_20f] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
+    if len(set(kk)) != n: raise SystemExit(f"[24_06f] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
 HASP = ~np.isnan(TFIRST)
@@ -191,6 +189,6 @@
 EX, EY = to_xy(SRC[:, 0], SRC[:, 1])
-print(f"[21_20f] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
+print(f"[24_06f] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
 EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
-if len(EVAL) == 0: raise SystemExit("[21_20f] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
-if a.dev: print(f"[21_20f] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
+if len(EVAL) == 0: raise SystemExit("[24_06f] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
+if a.dev: print(f"[24_06f] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                 "(較正にも入っているので値は楽観的)")
@@ -198,3 +196,3 @@
 # ---------------------------------------------------------------- 1 回だけの記録(本番は、試験の地震の結果を計算する前に書く)
-OPEN = ROOT / "models/21_20f_opened.json"
+OPEN = ROOT / "models/24_06f_opened.json"
 SUF = "_dev" if a.dev else ""
@@ -205,6 +203,6 @@
 if not a.dev:
-    if OPEN.exists() or (ROOT / "models/21_20f_judgment.json").exists():
+    if OPEN.exists() or (ROOT / "models/24_06f_judgment.json").exists():
         SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
-        print(f"[21_20f] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
-OPENED = False                           # 21_20f: 試験を開くのは、学習の記録・モデル・21_20 の結果の確認が全て通った後(8. の最後)
+        print(f"[24_06f] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない)")
+OPENED = False                           # 21_20f: 試験を開くのは、学習の記録・モデル・24_05 の結果の確認が全て通った後(8. の最後)
 def stop(msg):
@@ -276,3 +274,3 @@
 LAP_B = float(np.median(np.abs(r1)) / np.log(2.0))
-print(f"[21_20f] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
+print(f"[24_06f] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
       f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")
@@ -287,3 +285,3 @@
 XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
-print(f"[21_20f] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
+print(f"[24_06f] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
       f"  固定の深さ {ZDEF:.1f} km")
@@ -323,3 +321,3 @@
 lls = {h: loo_ll(h) for h in HS}; KDE_H = max(lls, key=lls.get)
-print(f"[21_20f] KDE の帯域(pool の一つ抜き): {KDE_H} km")
+print(f"[24_06f] KDE の帯域(pool の一つ抜き): {KDE_H} km")
 def log_prior(nodes, mem):
@@ -351,3 +349,3 @@
     lib = np.where((OTNS <= OTNS[ie] - int(buffer_h * 3600e9)) & HASP)[0]
-    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[21_20f] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
+    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[24_06f] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
     return lib
@@ -427,3 +425,3 @@
     top = lib[np.argsort(-S, kind="stable")[:min(k, pos)]]
-    if ie is not None and ie in top: stop("[21_20f] STOP: 自分自身が似た地震の上位に入っている")
+    if ie is not None and ie in top: stop("[24_06f] STOP: 自分自身が似た地震の上位に入っている")
     out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
@@ -575,3 +573,3 @@
 
-# ---------------------------------------------------------------- 8. 凍結したモデルと 21_20 の結果の読み込み
+# ---------------------------------------------------------------- 8. 凍結したモデルと 24_05 の結果の読み込み
 import pickle
@@ -581,42 +579,47 @@
 except ImportError:
-    stop("[21_20f] STOP: scikit-learn が無い(21_06a と同じ環境で回す)")
+    stop("[24_06f] STOP: scikit-learn が無い(21_06a と同じ環境で回す)")
 TJP = ROOT / a.train_json
-if not TJP.exists(): stop(f"[21_20f] STOP: 学習の記録 {a.train_json} が無い(先に 21_06a)")
+if not TJP.exists(): stop(f"[24_06f] STOP: 学習の記録 {a.train_json} が無い(先に 21_06a)")
 TJ = json.load(open(TJP))
 if not a.dev and (a.train_json != "models/21_06a_train.json" or TJ.get("mode") != "train" or TJ.get("suffix", "") != ""):
-    stop("[21_20f] STOP: 本番は、事前登録した 21_06a の最初の本番の学習(models/21_06a_train.json、mode train)でしか回さない")
+    stop("[24_06f] STOP: 本番は、事前登録した 21_06a の最初の本番の学習(models/21_06a_train.json、mode train)でしか回さない")
 FB = open(Path(__file__), encoding="utf-8").read()
 FEAT_SHA = hashlib.sha256(FB[FB.index("# >>> 21_06 FEATURES BEGIN"):FB.index("# <<< 21_06 FEATURES END")].encode()).hexdigest()
-if TJ["feature_block_sha256"] != FEAT_SHA: stop("[21_20f] STOP(G-feat): 特徴量の部分が 21_06a と 1 字でも違う(学習と試験で同じ計算になっていない)")
+if TJ["feature_block_sha256"] != FEAT_SHA: stop("[24_06f] STOP(G-feat): 特徴量の部分が 21_06a と 1 字でも違う(学習と試験で同じ計算になっていない)")
 MP = ROOT / TJ["model_path"]
-if not MP.exists() or sha256(MP) != TJ["model_sha256"]: stop(f"[21_20f] STOP(G-model): モデル {TJ['model_path']} が無いか、SHA-256 が学習の記録と違う")
-if TJ["sklearn"] != sklearn.__version__: stop(f"[21_20f] STOP: scikit-learn の版が学習時({TJ['sklearn']})と違う({sklearn.__version__})")
+if not MP.exists() or sha256(MP) != TJ["model_sha256"]: stop(f"[24_06f] STOP(G-model): モデル {TJ['model_path']} が無いか、SHA-256 が学習の記録と違う")
+if TJ["sklearn"] != sklearn.__version__: stop(f"[24_06f] STOP: scikit-learn の版が学習時({TJ['sklearn']})と違う({sklearn.__version__})")
 if TJ["feats"] != FEATS or TJ["hgb"] != HGB or TJ.get("block_consts") != json.loads(json.dumps(BLOCK_CONSTS)) or TJ.get("cond_min") != COND_MIN:
-    stop("[21_20f] STOP: 特徴量の名前・設定・特徴量が使う定数が学習の記録と違う")
-if TJ["numpy"] != np.__version__: stop(f"[21_20f] STOP: numpy の版が学習時({TJ['numpy']})と違う({np.__version__})")
+    stop("[24_06f] STOP: 特徴量の名前・設定・特徴量が使う定数が学習の記録と違う")
+if TJ["numpy"] != np.__version__: stop(f"[24_06f] STOP: numpy の版が学習時({TJ['numpy']})と違う({np.__version__})")
 with open(MP, "rb") as f: MODEL = pickle.load(f)
 RP = ROOT / TJ["train_rows_path"]
-if not RP.exists() or sha256(RP) != TJ["train_rows_sha256"]: stop(f"[21_20f] STOP: 学習の行 {RP.relative_to(ROOT)} が無いか SHA-256 が違う")
-print(f"[21_20f] 凍結したモデル: {TJ['model_path']} SHA-256 {TJ['model_sha256'][:12]}…(2026 の {TJ['n_train_events']} 地震で学習)  "
+if not RP.exists() or sha256(RP) != TJ["train_rows_sha256"]: stop(f"[24_06f] STOP: 学習の行 {RP.relative_to(ROOT)} が無いか SHA-256 が違う")
+print(f"[24_06f] 凍結したモデル: {TJ['model_path']} SHA-256 {TJ['model_sha256'][:12]}…(2026 の {TJ['n_train_events']} 地震で学習)  "
       f"特徴量の部分 {FEAT_SHA[:12]}… G-feat PASS  G-model PASS")
 TJ_SHA = sha256(TJP)
-REFCSV = ROOT / ("data/21_20_per_event_dev.csv" if a.dev else "data/21_20_per_event.csv")
-if not REFCSV.exists(): stop(f"[21_20f] STOP: {REFCSV.relative_to(ROOT)} が無い(先に 21_20 を回す。21_20f は 21_20 の後)")
+REFCSV = ROOT / ("data/24_05_per_event_dev.csv" if a.dev else f"data/24_05_per_event{a.ref_suffix}.csv")
+if not REFCSV.exists(): stop(f"[24_06f] STOP: {REFCSV.relative_to(ROOT)} が無い(先に 24_05 を回す。24_06f は 24_05 の後)")
 ref = {r["origin_time"]: r for r in csv.DictReader(open(REFCSV))}
 if sorted(ref) != sorted(OT[ie] for ie in EVAL):
-    stop(f"[21_20f] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
-J04 = ROOT / "models/21_20_judgment.json"
+    stop(f"[24_06f] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
+J04 = ROOT / f"models/24_05_judgment{a.ref_suffix}.json"
 if J04.exists() and not a.dev:
     j4 = json.load(open(J04))
-    if j4.get("mode") != "test" or j4.get("suffix") != "": stop("[21_20f] STOP: models/21_20_judgment.json が 21_20 の最初の本番の結果でない")
-    if j4.get("cache_sha256") != CACHE_SHA: stop("[21_20f] STOP: キャッシュの SHA-256 が 21_20 の本番と違う")
-    print("[21_20f] キャッシュの SHA-256 は 21_20 の本番と同じ")
-    O4 = ROOT / "models/21_20_opened.json"
+    if j4.get("mode") != "test" or j4.get("suffix", "") != a.ref_suffix: stop(f"[24_06f] STOP: {J04.name} が 24_05 の本番の結果(suffix '{a.ref_suffix}')でない")
+    if j4.get("script_sha256") != SHA_2405: stop(f"[24_06f] STOP: 24_05 の結果が、凍結した 24_05 v1(SHA-256 {SHA_2405[:12]}…)のものでない")
+    _O = ROOT / "models/24_05_opened.json"
+    _c = [r for r in (json.load(open(_O)) if _O.exists() else []) if str(r.get("status", "")).startswith("completed")]
+    if not _c or _c[0].get("suffix", "") != a.ref_suffix:
+        stop(f"[24_06f] STOP: --ref-suffix '{a.ref_suffix}' が、models/24_05_opened.json で最初に completed になった 24_05 の実行と違う")
+    if j4.get("cache_sha256") != CACHE_SHA: stop("[24_06f] STOP: キャッシュの SHA-256 が 24_05 の本番と違う")
+    print("[24_06f] キャッシュの SHA-256 は 24_05 の本番と同じ")
+    O4 = ROOT / "models/24_05_opened.json"
     t4 = json.load(open(O4))[0]["utc"] if O4.exists() else None
-    print(f"[21_20f] 順番の確認: 21_06a の学習 {TJ.get('utc')} / 21_20 の本番を開いた時刻 {t4}(学習が先のはず。事前登録の push の時刻とも照らす)")
-    if t4 is not None and TJ.get("utc") is not None and TJ["utc"] > t4: stop("[21_20f] STOP: 21_06a の学習が 21_20 の本番より後(事前登録の順番と違う)")
+    print(f"[24_06f] 順番の確認: 21_06a の学習 {TJ.get('utc')} / 24_05 の本番を開いた時刻 {t4}(学習が先のはず。事前登録の push の時刻とも照らす)")
+    if t4 is not None and TJ.get("utc") is not None and TJ["utc"] > t4: stop("[24_06f] STOP: 21_06a の学習が 24_05 の本番より後(事前登録の順番と違う)")
 elif not a.dev:
-    stop("[21_20f] STOP: models/21_20_judgment.json が無い(21_20 の本番を先に終える)")
+    stop(f"[24_06f] STOP: models/{J04.name} が無い(24_05 の本番を先に終える。やり直した時は --ref-suffix を渡す)")
 REF_SHA = sha256(REFCSV)
-print(f"[21_20f] SHA-256(事前登録の記録の 6 節と照らす): 学習の記録 {TJ_SHA} / モデル {TJ['model_sha256']} / 学習の行 {TJ['train_rows_sha256']} / 21_20 の CSV {REF_SHA}")
+print(f"[24_06f] SHA-256(事前登録の記録の 6 節と照らす): 学習の記録 {TJ_SHA} / モデル {TJ['model_sha256']} / 学習の行 {TJ['train_rows_sha256']} / 24_05 の CSV {REF_SHA}")
 if not a.dev:                                 # 入力の確認が全て通ってから試験を開く(ここより前の STOP は記録しない)
@@ -632,3 +635,3 @@
 
-# ---------------------------------------------------------------- 9. 記述用: 2018 の pool を足して学び直した版(L3p・L4p。同じ設定。判定には使わない)
+# ---------------------------------------------------------------- 9. 記述用: 2014 の pool を足して学び直した版(L3p・L4p。同じ設定。判定には使わない)
 EVSET = set(int(i) for i in EVAL)
@@ -646,3 +649,3 @@
 MODEL_P.fit(np.concatenate([R26["X"]] + Xp), np.concatenate([R26["y"]] + yp), sample_weight=np.concatenate([R26["w"]] + wp))
-print(f"[21_20f] 記述用の L3p・L4p: 2026 の行 {len(R26['y'])} + 2018 の pool の行 {int(sum(len(v) for v in yp))} で学び直した")
+print(f"[24_06f] 記述用の L3p・L4p: 2026 の行 {len(R26['y'])} + 2014 の pool の行 {int(sum(len(v) for v in yp))} で学び直した")
 
@@ -675,9 +678,9 @@
     except BaseException as ex:
-        stop(f"[21_20f] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
+        stop(f"[24_06f] STOP: 地震 {OT[ie]} の計算で例外 {type(ex).__name__}: {ex}(この行を貼って相談)")
     if (ii + 1) % 10 == 0: print(f"  … {ii + 1}/{len(EVAL)}  ({time.time() - T0:.0f} s)")
-for k in KEYS:                                # 21_20 の CSV(小数 4 桁)と同じ丸めにそろえてから比べる(同点を同点として扱う)
+for k in KEYS:                                # 24_05 の CSV(小数 4 桁)と同じ丸めにそろえてから比べる(同点を同点として扱う)
     E[k] = np.vectorize(lambda v: float(f"{v:.4f}"))(E[k])
 G_SAME = "PASS" if not mism else f"FAIL ({len(mism)})"
-print(f"[21_20f] G-same(ここで計算した C3・C4 が 21_20 の CSV と同じ): {G_SAME}")
-if mism: stop(f"[21_20f] STOP(G-same): 21_20 と同じ計算になっていない(例 {mism[:3]})")
+print(f"[24_06f] G-same(ここで計算した C3・C4 が 24_05 の CSV と同じ): {G_SAME}")
+if mism: stop(f"[24_06f] STOP(G-same): 24_05 と同じ計算になっていない(例 {mism[:3]})")
 for b in BASE:
@@ -721,3 +724,3 @@
 def fp(p): return "—" if p is None else f"{p:.2g}"
-print(f"\n[21_20f] ===== 水平誤差の中央値 km [95% 区間](大阪府北部 2018、評価 {NT} 地震{'、dev' if a.dev else ''}) =====")
+print(f"\n[24_06f] ===== 水平誤差の中央値 km [95% 区間](長野県北部 2014、評価 {NT} 地震{'、dev' if a.dev else ''}) =====")
 for k in ["BEST"] + KEYS:
@@ -732,3 +735,3 @@
           f"L が M6r に戻った割合 {d['learned_fallback_frac']:.2f}")
-print(f"\n[21_20f] ===== 事前登録の判定 =====")
+print(f"\n[24_06f] ===== 事前登録の判定 =====")
 for name, h in HYP.items():
@@ -737,4 +740,4 @@
           f"p = {fp(pr['p'])}(基準 {h['alpha']})  差が 0 でない組 {pr['n_nonzero']}  FLOOR={h['floor']}  → {'勝ち' if h['win'] else '勝ちなし'}")
-print(f"\n[21_20f] 判定(事前登録、HL1): {VERDICT}")
-LIMITS_L = ["third sequence: Northern Osaka 2018 (mainshock 2018-06-18, 07:58 JST; JMA catalogue values), never used in ARGUS development; HL1-HL3 and "
+print(f"\n[24_06f] 判定(事前登録、HL1): {VERDICT}")
+LIMITS_L = ["fourth sequence: Northern Nagano 2014 (mainshock 2014-11-22, 22:08:17.90 JST; JMA catalogue values), never used in ARGUS development; HL1-HL3 and "
             "the learned ranker were fixed in the 21_06 preregistration and frozen by 21_06a on West Tottori 2026 before this test"] + \
@@ -742,7 +745,7 @@
             "(depth not solved); it is missing (nan) with fewer than 4 common stations or a near-linear station geometry", "the learned ranker (21_06a) was trained on West Tottori 2026 only and frozen before this test; L3p/L4p (retrained with the "
-                     "2018 pool) are descriptive", "21_20f reuses the 21_20 per-event CSV for the physics-only methods and C3/C4, and "
-                     "recomputes C3/C4 to check identity (G-same)", "C3/C4/L3/L4 errors are rounded to 4 decimals (as in the 21_20 CSV) "
+                     "2014 pool) are descriptive", "24_06f reuses the 24_05 per-event CSV for the physics-only methods and C3/C4, and "
+                     "recomputes C3/C4 to check identity (G-same)", "C3/C4/L3/L4 errors are rounded to 4 decimals (as in the 24_05 CSV) "
                      "before comparison so that ties stay ties", "log10_dt_h uses the target's JMA origin time (not known exactly at tau; "
                      "the error is a few seconds against >= 1 h)"]
-print("[21_20f] 限界: " + " / ".join(LIMITS_L))
+print("[24_06f] 限界: " + " / ".join(LIMITS_L))
 
@@ -757,3 +760,3 @@
     return o
-with open(ROOT / f"data/21_20f_per_event{SUF}.csv", "w", newline="") as f:
+with open(ROOT / f"data/24_06f_per_event{SUF}.csv", "w", newline="") as f:
     w = csv.writer(f)
@@ -763,3 +766,3 @@
         w.writerow([OT[ie], f"{MAG[ie]:.1f}"] + [("" if not np.isfinite(E[k][i, jt]) else f"{E[k][i, jt]:.4f}") for k in cols for jt in range(len(TAUS))])
-out = dict(script="21_20f_osaka2018_learned_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"), suffix=SUF,
+out = dict(script="24_06f_nagano2014_learned_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"), suffix=SUF,
            cache=a.cache, cache_sha256=CACHE_SHA, reference_csv=str(REFCSV.relative_to(ROOT)), train_json=a.train_json,
@@ -774,3 +777,3 @@
            limits=LIMITS_L, runtime_s=time.time() - T0)
-json.dump(clean(out), open(ROOT / f"models/21_20f_judgment{SUF}.json", "w"), indent=1)
+json.dump(clean(out), open(ROOT / f"models/24_06f_judgment{SUF}.json", "w"), indent=1)
 
@@ -790,3 +793,3 @@
 ax.set_xticks(x); ax.set_yscale("log"); ax.set_xlabel("Time since the first P pick, tau (s)"); ax.set_ylabel("Median epicentral error (km), 95% bootstrap CI")
-ax.set_title(f"(a) Northern Osaka 2018, {NT} {'DEV' if a.dev else 'test'} events", fontsize=10); ax.grid(alpha=0.3)
+ax.set_title(f"(a) Northern Nagano 2014, {NT} {'DEV' if a.dev else 'test'} events", fontsize=10); ax.grid(alpha=0.3)
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, frameon=False, fontsize=8.5)
@@ -802,4 +805,4 @@
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8.5)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/21_20f_F1_learned_test{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_06f_F1_learned_test{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
 if not a.dev: log_open(f"completed: {VERDICT}")
-print(f"[21_20f] 出力: models/21_20f_judgment{SUF}.json, data/21_20f_per_event{SUF}.csv, PDF/21_20f_F1_learned_test{SUF}.pdf  ({time.time() - T0:.0f} s)")
+print(f"[24_06f] 出力: models/24_06f_judgment{SUF}.json, data/24_06f_per_event{SUF}.csv, PDF/24_06f_F1_learned_test{SUF}.pdf  ({time.time() - T0:.0f} s)")
```

## 24_06g_nagano2014_gate_test.py ← 22_04_osaka2018_gate_test.py

```diff
--- gate22/22_04_osaka2018_gate_test.py	2026-11-02 14:53:40.640690848 +0000
+++ nagano/frz/24_06g_nagano2014_gate_test.py	2026-11-15 05:21:00.097264027 +0000
@@ -2,59 +2,26 @@
 # =============================================================================
-# Script : 22_04_osaka2018_gate_test.py  (v1)
-#          [信頼の切り替え G の試験(1 回だけ): 凍結した G(models/22_gate.pkl)を、手を付けていない大阪府北部 2018 の試験の地震に当て、
+# Script : 24_06g_nagano2014_gate_test.py  (v1)
+#          [信頼の切り替え G の試験(1 回だけ): 凍結した G(models/22_gate.pkl)を、手を付けていない長野県北部 2014 の試験の地震に当て、
 #           「物理(C4)と記憶(C1)のどちらを信じるか」を AI が決めると、C4 より大きな外れが減るか(HG1)、固定の規則 R より良いか(HG2)を判定する]
-# Project: ARGUS(新生)— AI を「物理の部品」として使う。22 では AI が「どちらの答えを信じるか」を決める(事前登録 22_00)
+# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の信頼の切り替えの腕(大阪 22_04 は INCONCLUSIVE だった)
+# 派生元 : 22_04_osaka2018_gate_test.py v1(SHA-256 7a634ca58e08fe759e3d3abac8df629c5fdf7da81ddcffd9d36bee2eceacec24)。
+#          22 GATE FEATURES・22 GATE APPLY の印の間・判定の関数・凍結した G・閾値・HG1〜HG3 の規則は 1 字も変えていない
+#          (写した部分の SHA-256 を、22_04 と同じ凍結の記録の値と照らす)。変えたのは次だけ(DIFF_LOG_24.md):
+#          (1) 入力の既定のキャッシュ(24_05 と同じ R1 の後のもの)、MAIN_UTC・UNTOUCHED_UTC(24_05 と同じ)、限界の文(24_05 と同じ LIMITS)
+#          (2) 比べる相手と順番の確かめを 22_04 の 21_20 の出力から 24_05 の出力に変えた: data/24_05_per_event.csv(--dev は _dev)、
+#              models/24_05_judgment.json(登録した 24_05 v1 の SHA-256・同じキャッシュ・mode = test)、models/24_05_opened.json
+#              (G を凍結した時刻 < 24_05 を開いた時刻)。照らす 24_05 の SHA-256 は FROZEN["script_24_05"](凍結の時に書く)
+#          (3) 出力の名前: models/24_06g_judgment.json / models/24_06g_opened.json / data/24_06g_per_event.csv / PDF/24_06g_F1_gate_nagano.pdf、
+#              表示の [24_06g]、系列の名前
 #
-# 何をするか(全て 22_00 の 2 節のとおり。この版の SHA-256 を、大阪を開く前に 22_00 の 7 節に書いて push する):
-#   1. 21_20_osaka2018_similarity_confirmation.py v1 の 1〜6 節(入力・G-untouched・G-split・座標と検測・速度と局の補正・格子と探索・
-#      事前分布と C4 の材料・波形の似ている度合い・c_from)を、計算は 1 字も変えずに写す。違うのは画面の表示の [21_20] を [22_04] にした所、
-#      引数 --ref-suffix を足した所、21_20 の「1 回だけの記録」の部分を 22_04 の照合の準備(下の 3)に置き換えた所だけ
-#      (22_04 の記録は models/22_04_opened.json。21_20 の記録は読むだけで書かない)。
-#   2. 22 GATE FEATURES(22_01a と同じ)・22 GATE APPLY(22_02 と同じ)・判定の関数 verdict(22_02 と同じ)を写し、
-#      写した部分の SHA-256 が凍結の記録(22_00 の 7 節)と同じでなければ STOP。
-#   3. 照合の準備(全て、速度・格子の計算と「opened」の前に済ませる。どれかが違えば STOP し、1 回だけの記録は書かない):
-#      凍結した G の SHA-256・G の中の 2 つの部分の SHA-256・学習の行の SHA-256・p の境目 0.5・R のしきい値 10 km が 22_00 の 7 節と同じ。
-#      G を凍結した時刻(models/22_02_opened.json の最初の completed)が、21_20 を開いた時刻(models/21_20_opened.json の最初の行)より前。
-#      21_20 の正式な結果(--ref-suffix。既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)が、
-#      models/21_20_opened.json で最初に completed になった実行で、登録した 21_20 v1 のスクリプト(SHA-256 2c0fb375e6a1…)・同じキャッシュ・
-#      mode = test のもの。CSV の地震が試験の地震と同じで、C1・C3・C4・M6r の列が 4 時点ともある。
-#      21_20 が「評価できる地震 30 未満」で INCONCLUSIVE に終わった時は、22_04 は開かずに INCONCLUSIVE を models/22_04_judgment.json に書く。
-#   4. 1 回だけの記録 models/22_04_opened.json に「opened」を書いてから、試験の地震 × 4 時点で M6r・C1・C2・C3・C4 を 21_20 と同じ呼び方で
-#      計算する(m3 = prior_members、M6r = locate_map(pk, m3)、S = similarity(ie, τ, lib, 2–8 Hz)、c_from)。
-#      G-same: 各地震を計算した直後に、C1・C3・C4・M6r の誤差を 21_20 の CSV と比べ、6e-5 km を超えて違えばその場で STOP。
-#   5. 誤差を小数 4 桁に丸め(学習の行と同じ)、13 の手がかりを作り、凍結した G で選ぶ(p ≥ 0.5 なら C1、それ以外と C1 が無い地震は C4)。
-#      規則 R(C4 と C1 が 10 km 以上食い違えば C1)も出す。判定の部分の中で止まった時も「stopped」を記録する。
-#   6. 判定(τ = 2 s。評価できる地震 = τ = 2 s の全ての試験の地震。C1 が無い地震も G = R = C4 として数える):
-#        HG1(主)G 対 C4: 10 km 超の外れ。食い違う対の正確な片側 McNemar(binomtest(G だけ外れ, 食い違う対, 0.5, 'less'))p < 0.005
-#        HG2(主)G 対 R : 地震ごとの誤差。片側の対応 Wilcoxon(zero_method 'wilcox'、method 'approx'、correction False)p < 0.005、
-#                         差が 0 でない対 10 以上(10 未満なら HG2 は成り立たないとして扱う)
-#        守り     G の中央値 ≤ C4 の中央値 + 0.05 km
-#        INCONCLUSIVE(地震 30 未満、または HG1 の食い違う対 8 未満)→ GATE-CONFIRMED(HG1・HG2・守り)→
-#        GATE-HELPS-NOT-BEYOND-RULE(HG1・守り)→ GATE-NOT-CONFIRMED(それ以外)
-#      副の仮説 HG3(主の判定には関わらず、別に報告する): τ = 1 s で G 対 R、HG2 と同じ片側の対応 Wilcoxon、p < 0.005、
-#        差が 0 でない対 10 以上(足りない時と地震 30 未満は INCONCLUSIVE)→ SUPPORTED / NOT-SUPPORTED / INCONCLUSIVE
-#   7. 記述(判定しない): 他の τ の表・外れの確率 q の較正(Brier 得点と、学習の行の基準率だけで当てた時の Brier 得点)・
-#      手がかりが学習の行の範囲の外にある割合(data/22_01a_rows_wt2026.npz があれば。SHA-256 を照合)。
-#   8. 出力: models/22_04_judgment.json・data/22_04_per_event.csv・PDF/22_04_F1_gate_osaka.pdf(白背景・英語・凡例は枠外)。
-#      判定の JSON を書いた直後に「completed」を記録する(図で落ちても判定は残る)。2 回目以降は上書きせず _rerun_<UTC> の名前に書く
-#      (扱いは 22_00 の 3 節: 開いた後にスクリプトが自分で止めたら使い切り、機械的に途切れた時だけ 1 回やり直してよい)。
+# 判定(22_00 の 2 節と同じ): τ = 2 s。HG1(主)G 対 C4: 10 km 超の外れの食い違う対の正確な片側 McNemar p < 0.005(食い違う対 8 未満は
+#   INCONCLUSIVE)。HG2(主)G 対 R: 片側の対応 Wilcoxon p < 0.005、差が 0 でない対 10 以上。守り: G の中央値 ≤ C4 の中央値 + 0.05 km。
+#   → INCONCLUSIVE / GATE-CONFIRMED / GATE-HELPS-NOT-BEYOND-RULE / GATE-NOT-CONFIRMED。副の HG3: τ = 1 s で G 対 R。
 #
-# --dev: 試験を開かない動作確認(21_20 の dev と同じ、pool の最後の使っていない地震 20 個。data/21_20_per_event_dev.csv と照合。出力に _dev。
-#        評価の地震が 30 未満なので判定は必ず INCONCLUSIVE。1 回だけの記録は書かない)。
-#
-# 限界(結果に必ず添える。JSON にも英語で書く): 22_00 の 4 節(学習は鳥取県西部 2026 の 1 系列だけ・正解も過去の地震の位置も気象庁の震源・
-#   C1 は既知の場所しか答えられない・R のしきい値 10 km は鳥取県中部 2016 を見て決めた・手がかり 9 は早い時点ではほぼ効かない)と、
-#   21_20 の限界(局は Hi-net だけ・h2018 の震源・オフラインの PhaseNet の検測・遅れなし など)。
-#
-# Usage : (先に 21_20 を、21_20 の事前登録の記録どおりに本番まで回す。22_04 は 21_20 の出力と照合する)
-#         cd ~/SWIFT && caffeinate -i uv run python src/22_04_osaka2018_gate_test.py --dev   (動作確認。試験を開かない)
-#         cd ~/SWIFT && caffeinate -i uv run python src/22_04_osaka2018_gate_test.py         (本番。1 回だけ)
-#         (21_20 の正式な結果が _rerun_<UTC> の時だけ: ... src/22_04_osaka2018_gate_test.py --ref-suffix _rerun_<UTC>)
-# 入力  : data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt・models/22_gate.pkl・models/22_02_opened.json・
-#         models/21_20_opened.json・models/21_20_judgment.json・data/21_20_per_event.csv(--dev なら両方 _dev)・(あれば)data/22_01a_rows_wt2026.npz
-# Output: models/22_04_judgment.json / models/22_04_opened.json / data/22_04_per_event.csv / PDF/22_04_F1_gate_osaka.pdf
-# 止める条件(STOP): 21_20 と同じもの(入力・G-untouched・G-split・G-lib)・写した部分か凍結した G か学習の行の SHA-256 が記録と違う・
-#                   G-leak・G の凍結が 21_20 を開いた後・21_20 の結果が無いか、正式な結果でないか、合わない・G-same・
-#                   C4 の誤差が無い地震がある・手がかり 9 以外が値なし
-# 所要  : CPU のみ。21_20 より短い見込み(21_20 は感度の計算のため、似ている度合いを 1 時点あたり 2 回計算する。22_04 は 1 回)
+# Usage : (先に 24_05 を本番まで回す)
+#         cd ~/SWIFT && caffeinate -i uv run python src/24_06g_nagano2014_gate_test.py --dev   (動作確認。試験を開かない)
+#         cd ~/SWIFT && caffeinate -i uv run python src/24_06g_nagano2014_gate_test.py         (本番。1 回だけ)
+# 入力  : data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt・models/22_gate.pkl・models/22_02_opened.json・
+#         models/24_05_opened.json・models/24_05_judgment.json・data/24_05_per_event.csv(--dev なら両方 _dev)・(あれば)data/22_01a_rows_wt2026.npz
+# Output: models/24_06g_judgment.json / models/24_06g_opened.json / data/24_06g_per_event.csv / PDF/24_06g_F1_gate_nagano.pdf
 # =============================================================================
@@ -69,5 +36,5 @@
 ap = argparse.ArgumentParser()
-ap.add_argument("--cache", default="data/osaka2018_processed/tottori_parsed_realpick_osaka2018_m15.pt", help="21_20c(15_01c v3.3 と同じ計算)の大阪府北部 2018 の M>=1.5 版")
+ap.add_argument("--cache", default="data/nagano2014_processed/tottori_parsed_realpick_nagano2014_m15_r1.pt", help="24_03(15_01c v3.3 と同じ計算)の長野県北部 2014 の M>=1.5 版に 24_03h の R1 を当てたもの(24_05 と同じ)")
 ap.add_argument("--dev", action="store_true", help="試験を開かない動作確認(pool の最後の新しい地震 20 個を代わりに使う)")
-ap.add_argument("--ref-suffix", default="", help="22_04: 比べる相手の 21_20 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
+ap.add_argument("--ref-suffix", default="", help="24_06g: 比べる相手の 24_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
 a = ap.parse_args()
@@ -92,8 +59,9 @@
 NBOOT, SEED, N_DEV, N_GATE = 2000, 12, 20, 5
-MAIN_UTC = dt.datetime(2018, 6, 17, 22, 58, 30)   # 21_20: 気象庁の発表の 07:58 JST の 1 分の真ん中(秒までの値ではない。±60 s でこの 1 分を含む)。要確認
-UNTOUCHED_UTC = (dt.datetime(2018, 6, 15), dt.datetime(2018, 7, 12))     # G-untouched: 21_20a の期間(本震の 2 日前〜24 日後)を含む
-LIMITS = ["third sequence: Northern Osaka 2018 (mainshock 2018-06-18, 07:58 JST; origin time and Mj are those of the JMA catalogue, "
-          "see 21_20a's JSON), never used in ARGUS development; the hypotheses were fixed on West Tottori 2026 (21_01/21_02), "
-          "tested on Central Tottori 2016 (21_04, run with a documented deviation) and are applied here unchanged",
-          "one third sequence only",
+MAIN_UTC = dt.datetime(2014, 11, 22, 13, 8, 17, 900000)   # 24_05 と同じ: 24_00 の表示の 22:08:17.90 JST(± 60 s)
+UNTOUCHED_UTC = (dt.datetime(2014, 11, 20), dt.datetime(2014, 12, 17))     # G-untouched: 24_01 の期間(本震の 2 日前〜24 日後)を含む
+LIMITS = ["fourth sequence: Northern Nagano 2014 (mainshock 2014-11-22, 22:08:17.90 JST, Mj 6.7; JMA catalogue values, see 24_01's JSON), "
+          "never used in ARGUS development; the hypotheses H1-H3 were fixed on West Tottori 2026 (21_01/21_02), tested on Central Tottori 2016 "
+          "(21_04, with a documented deviation) and Northern Osaka 2018 (21_20, re-registered with amendment 04) and are applied here unchanged",
+          "one fourth sequence only; before this preregistration the catalogue h2014 was opened once by 24_00 to count events "
+          "(counts and the mainshock row only; no location list, waveform or method error was looked at)",
           "stations are NIED Hi-net (0101) only, chosen as the 50 nearest with data among the current NIED list; the West Tottori 2026 "
@@ -101,15 +69,14 @@
           "waveforms were downloaded around catalogue events only and converted to the West Tottori 2026 h5 form (30-s windows, "
-          "per-window per-component z-score, JST epoch); whether a filter was applied before the z-score in the 2026 h5 is not recorded "
-          "(none here; compared in 21_20b G-spec)",
-          "the cache was built by 21_20c, whose picking, QC and assembly are identical to 15_01c v3.3 (itself identical to v3 except "
-          "the window-index file name and output folder); 21_20c changed only labels, defaults and required arguments",
-          "catalogue: JMA hypocentres from h2018 (whether h2018 is the final stage is to be confirmed; West Tottori 2026 used the "
-          "unified catalogue); past-event locations are JMA "
+          "per-window per-component z-score, JST epoch; 24_02 also stores the window mean and standard deviation); no filter was applied "
+          "before the z-score (compared in 24_02 G-spec)",
+          "the cache was built by 24_03, whose picking, QC and assembly are identical to 15_01c v3.3; 24_03h then removed every event "
+          "with another catalogue event from 15 s before to 5 s after its origin (rule R1 of 21_20 amendment 04, fixed here before any "
+          "Nagano waveform was opened; it uses origin times and Mj only), which can bias the sample against busy periods",
+          "catalogue: JMA hypocentres from h2014 (whether h2014 is the final stage is to be confirmed); past-event locations are JMA "
           "hypocentres (in operation: automatic slow-layer locations, possibly worse); truth is also JMA",
-          "the 2018 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
-          "events; whether the 2026 catalogue excluded them is not recorded. Manual and automatic hypocentres are mixed (per-flag "
-          "counts in 21_20a's JSON)",
-          "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); the 2026 station list's "
-          "convention is not recorded; static station terms absorb a constant offset",
-          "offline PhaseNet picks on full records (possibly better than real-time picks); every method uses the same picks",
+          "the 2014 catalogue excludes matched-filter, undetermined/fixed (precision M, 8, 9; flag N, F), artificial and low-frequency "
+          "events. Manual and automatic hypocentres can be mixed (per-flag counts in 24_01's JSON)",
+          "station elevations are NIED's current height(m) (possibly the sensor depth for borehole stations); "
+          "static station terms absorb a constant offset",
+          "H1-H4 use offline PhaseNet picks on full records (possibly better than real-time picks); every method uses the same picks",
           "cache keeps up to 24 stations per event (PhaseNet P first, earliest first); no not-yet-arrived information is used",
@@ -126,4 +93,11 @@
           "P residual over all its stations, while uncorrected stations keep only the static term",
-          "H1 (C3 at tau = 2 s) is the primary test; H2 and H3 are secondary at alpha 0.005; everything else is descriptive"]
-
+          "H4 compares C3 with C1 (the JMA epicentre of the most similar past event, the 'search the most similar past event' approach) "
+          "on the events where C1 exists (C1 is undefined when fewer than 5 past events have a positive similarity)",
+          "H5 re-runs every method with picks made by 24_07 from data up to T only (T = first offline P + tau); the tau origin, the "
+          "station set (the cache stations) and the P search band (relative to the catalogue origin) still come from the offline picks "
+          "and the catalogue; no Wadati QC or STA/LTA fallback at each time; the similarity windows start at the causal P; stations "
+          "picked causally but without an offline PhaseNet P are used by the physics but not by the similarity; past events keep their "
+          "offline picks (their records are complete at the time of the target event)",
+          "H1 (C3 at tau = 2 s) is the primary test; H2, H3 and H4 are secondary at alpha 0.005; H5 (causal picks) uses the H1 rule at "
+          "alpha 0.01 as a realism check; everything else is descriptive"]
 ROOT = Path(__file__).resolve().parent.parent
@@ -139,3 +113,3 @@
 SELF_SHA = sha256(Path(__file__))
-print(f"[22_04] 本スクリプト(22_04){VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
+print(f"[24_06g] 本スクリプト(24_06g){VERSION} SHA-256 {SELF_SHA[:12]}…(結果を貼る時にこの行も貼ってください)  "
       f"モード: {'dev(試験を開かない)' if a.dev else '本番'}")
@@ -144,3 +118,3 @@
 CP = ROOT / a.cache
-if not CP.exists(): raise SystemExit(f"[22_04] STOP: {a.cache} が無い(ノート 21_20_osaka2018_colab.ipynb のセル 11 で作った tottori_parsed_realpick_osaka2018_m15.pt を data/osaka2018_processed/ に置く)")
+if not CP.exists(): raise SystemExit(f"[24_06g] STOP: {a.cache} が無い(ノート 24_nagano2014_colab.ipynb のセル N12 で作った tottori_parsed_realpick_nagano2014_m15_r1.pt を data/nagano2014_processed/ に置く)")
 EVS = torch.load(CP, map_location="cpu", weights_only=False)
@@ -149,7 +123,7 @@
     miss = [k for k in need if k not in e]
-    if miss: raise SystemExit(f"[22_04] STOP: キャッシュの地震に {miss} が無い(21_20c の出力か確かめる)")
+    if miss: raise SystemExit(f"[24_06g] STOP: キャッシュの地震に {miss} が無い(24_03・24_03h の出力か確かめる)")
 for e in EVS:
     w_ = np.asarray(e["waveforms"])
-    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[22_04] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
-    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[22_04] STOP: {e['origin_time']} の波形に NaN か無限大")
+    if w_.ndim != 3 or w_.shape[1:] != (3, NTS): raise SystemExit(f"[24_06g] STOP: 波形の形 {w_.shape} が (局, 3, 2048) でない")
+    if not np.isfinite(w_[:int(e["n_real_stations"])]).all(): raise SystemExit(f"[24_06g] STOP: {e['origin_time']} の波形に NaN か無限大")
 def to_ns(o):
@@ -161,3 +135,3 @@
     except Exception:
-        raise SystemExit(f"[22_04] STOP: origin_time {o!r} を時刻として読めない")
+        raise SystemExit(f"[24_06g] STOP: origin_time {o!r} を時刻として読めない")
 OTNS = np.array([to_ns(e["origin_time"]) for e in EVS])
@@ -169,4 +143,4 @@
 if not (np.all(np.abs(SRC[:, 0]) <= 90) and np.all(np.abs(SRC[:, 1]) <= 180) and np.all((SRC[:, 2] > -5) & (SRC[:, 2] < 100))):
-    raise SystemExit("[22_04] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
-if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[22_04] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
+    raise SystemExit("[24_06g] STOP: src_loc が (緯度, 経度, 深さ km) に見えない")
+if MAG.min() < MIN_MAG - 1e-6: raise SystemExit(f"[24_06g] STOP: Mj {MAG.min():.2f} の地震がある(M ≥ 1.5 版のはず)")
 # G-untouched(21_02 の正本との照合の代わり。この系列は ARGUS のどこでも使っていない)
@@ -177,10 +151,10 @@
 n_extra2 = int((MAG >= FRESH_MAX_MAG - 1e-6).sum())
-print(f"[22_04] 入力: 大阪府北部 2018 の M ≥ 1.5 版 {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
+print(f"[24_06g] 入力: 長野県北部 2014 の M ≥ 1.5 版(R1 の後) {len(EVS)} 地震(Mj {MAG.min():.1f}〜{MAG.max():.1f})。Mj < 2.0 の地震 {int(FRESH.sum())}・"
       f"Mj ≥ 2.0 の地震 {n_extra2}(試験には使わず、過去の地震の一覧には入れる。21_02 と同じ)  キャッシュの SHA-256 {sha256(CP)[:12]}…")
-print(f"[22_04] G-untouched: 期間 2018-06-15〜2018-07-12(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
+print(f"[24_06g] G-untouched: 期間 2014-11-20〜2014-12-17(UTC)の外の地震 {n_out}・Mj ≥ 6.0 の地震 {n_big}  "
       + ("PASS" if (n_out == 0 and n_big == 1) else "FAIL"))
-if n_out != 0 or n_big != 1: raise SystemExit("[22_04] STOP(G-untouched): 大阪府北部 2018 のキャッシュに見えない(この行を貼って相談)")
+if n_out != 0 or n_big != 1: raise SystemExit("[24_06g] STOP(G-untouched): 長野県北部 2014 のキャッシュに見えない(この行を貼って相談)")
 im = int(np.argmax(MAG)); main_ns = int(np.datetime64(MAIN_UTC, "ns").astype(np.int64))
 if MAG[im] < 6.0 or abs(OTNS[im] - main_ns) > 60e9:
-    raise SystemExit(f"[22_04] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2018-06-17 22:58 UTC の 1 分 ± 60 s。気象庁の発表の 07:58 JST)")
+    raise SystemExit(f"[24_06g] STOP: 本震(Mj 最大)が想定と違う: Mj {MAG[im]:.1f} {OT[im]}(想定 Mj ≥ 6.0・2014-11-22 13:08:17.9 UTC ± 60 s。24_00 の表示の 22:08:17.90 JST)")
 CUT_NS = OTNS[im] + int(POOL_H * 3600e9)
@@ -188,5 +162,5 @@
 if len(pool_idx) == 0 or len(test_idx) == 0 or pool_idx.max() >= test_idx.min():
-    raise SystemExit("[22_04] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
-print(f"[22_04] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
-print(f"[22_04] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
+    raise SystemExit("[24_06g] STOP(G-split): pool か試験が 0 地震、または時刻で重なる")
+print(f"[24_06g] 入力: {NE} 地震  期間 {OT[0][:19]} 〜 {OT[-1][:19]}  本震 {OT[im][:19]} Mj {MAG[im]:.1f}")
+print(f"[24_06g] 分け方: pool(本震 + 72 h まで、全ての Mj){len(pool_idx)}  試験(本震 + 72 h より後の使っていない地震){len(test_idx)}"
       f"(最初 {OT[test_idx[0]][:19]})  G-split PASS")
@@ -201,3 +175,3 @@
     kk = [skey(l) for l in np.asarray(e["sta_locs"], float)[:n]]
-    if len(set(kk)) != n: raise SystemExit(f"[22_04] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
+    if len(set(kk)) != n: raise SystemExit(f"[24_06g] STOP: {e['origin_time']} の中で座標の同じ局が重なる(局を座標で見分けられない)")
 HASP = ~np.isnan(TFIRST)
@@ -213,6 +187,6 @@
 EX, EY = to_xy(SRC[:, 0], SRC[:, 1])
-print(f"[22_04] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
+print(f"[24_06g] 測った P が無い地震: {int((~HASP).sum())}(較正・評価・過去の地震の一覧から除く)")
 EVAL = (pool_idx[HASP[pool_idx] & FRESH[pool_idx]][-N_DEV:] if a.dev else test_idx[HASP[test_idx]])
-if len(EVAL) == 0: raise SystemExit("[22_04] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
-if a.dev: print(f"[22_04] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
+if len(EVAL) == 0: raise SystemExit("[24_06g] STOP: 評価する地震が 0(dev なら pool に使っていない地震が無い)")
+if a.dev: print(f"[24_06g] dev: 試験を開かず、pool の最後の使っていない地震 {N_DEV} 個({OT[EVAL[0]][:19]}〜{OT[EVAL[-1]][:19]})を代わりに評価する"
                 "(較正にも入っているので値は楽観的)")
@@ -220,5 +194,5 @@
 # ---------------------------------------------------------------- 1 回だけの記録と照合の準備(22_04。重い計算と、開く前に全て済ませる)
-# 21_20 の記録(models/21_20_opened.json)は読むだけで書かない。照合が全て通った後、試験の地震の結果を計算する前に 9 節で「opened」を書く
+# 24_05 の記録(models/24_05_opened.json)は読むだけで書かない。照合が全て通った後、試験の地震の結果を計算する前に 9 節で「opened」を書く
 import re, sys, platform, pickle
-OPEN = ROOT / "models/22_04_opened.json"
+OPEN = ROOT / "models/24_06g_opened.json"
 SUF = "_dev" if a.dev else ""
@@ -236,3 +210,3 @@
               rows="b57caba76f0d8cca1a5ca952afe17b494897ef76c4ac98cecb63fa8d27c48d59",
-              script_21_20="2c0fb375e6a1a8d48d3ffbc611bb189b2390d224488cdd5585c76f5cadd5da43")   # 22_00 の 7 節(2026-11-02 の凍結)
+              script_24_05="c10d15fe404309d836fc83fb2dbe1d207fa477d9597900724f487ef965970f9f")   # 22_00 の 7 節(2026-11-02 の凍結)の G の値と、事前登録 24 で凍結する 24_05 v1
 P_CHOOSE_REG, THR_R_REG = 0.5, 10.0                                                         # 22_00 の 1.3・2 節
@@ -244,12 +218,12 @@
 APPLY_SHA = blk("# >>> 22 GATE APPLY BEGIN", "# <<< 22 GATE APPLY END")
-if GATE_SHA != FROZEN["features"]: raise SystemExit(f"[22_04] STOP: 手がかりの部分の SHA-256 {GATE_SHA[:12]}… が凍結の記録と違う")
-if APPLY_SHA != FROZEN["apply"]: raise SystemExit(f"[22_04] STOP: 判定に使う部分(22 GATE APPLY)の SHA-256 {APPLY_SHA[:12]}… が凍結の記録と違う")
+if GATE_SHA != FROZEN["features"]: raise SystemExit(f"[24_06g] STOP: 手がかりの部分の SHA-256 {GATE_SHA[:12]}… が凍結の記録と違う")
+if APPLY_SHA != FROZEN["apply"]: raise SystemExit(f"[24_06g] STOP: 判定に使う部分(22 GATE APPLY)の SHA-256 {APPLY_SHA[:12]}… が凍結の記録と違う")
 GBLK = FB[FB.rindex("# >>> 22 GATE FEATURES BEGIN"):FB.rindex("# <<< 22 GATE FEATURES END")]
 leak = re.findall(r"SRC\s*\[|MAG\s*\[|E[XY]\s*\[\s*ie\s*\]|OTNS\s*\[|RES\s*\[|EVS\s*\[|\bOT\s*\[|src_loc|TFIRST\s*\[", GBLK)
-if leak: raise SystemExit(f"[22_04] STOP(G-leak): 手がかりの部分に正解か目標の地震の値を読む所がある {sorted(set(leak))}")
-print(f"[22_04] 写した部分の SHA-256: 手がかり {GATE_SHA[:12]}…・判定 {APPLY_SHA[:12]}…(凍結の記録と同じ)  G-leak PASS")
+if leak: raise SystemExit(f"[24_06g] STOP(G-leak): 手がかりの部分に正解か目標の地震の値を読む所がある {sorted(set(leak))}")
+print(f"[24_06g] 写した部分の SHA-256: 手がかり {GATE_SHA[:12]}…・判定 {APPLY_SHA[:12]}…(凍結の記録と同じ)  G-leak PASS")
 MP = ROOT / "models/22_gate.pkl"
-if not MP.exists(): raise SystemExit("[22_04] STOP: models/22_gate.pkl が無い(22_02 で凍結したもの)")
+if not MP.exists(): raise SystemExit("[24_06g] STOP: models/22_gate.pkl が無い(22_02 で凍結したもの)")
 MODEL_SHA = sha256(MP)
-if MODEL_SHA != FROZEN["gate_pkl"]: raise SystemExit(f"[22_04] STOP: models/22_gate.pkl の SHA-256 {MODEL_SHA[:12]}… が凍結の記録(358e3daddfc0…)と違う")
+if MODEL_SHA != FROZEN["gate_pkl"]: raise SystemExit(f"[24_06g] STOP: models/22_gate.pkl の SHA-256 {MODEL_SHA[:12]}… が凍結の記録(358e3daddfc0…)と違う")
 with open(MP, "rb") as f: GATE = pickle.load(f)
@@ -257,41 +231,41 @@
         or GATE["p_choose"] != P_CHOOSE_REG or GATE["thr_R_km"] != THR_R_REG):
-    raise SystemExit("[22_04] STOP: 凍結した G の中の部分の SHA-256・学習の行・p の境目・R のしきい値のどれかが、凍結の記録と違う")
-print(f"[22_04] 凍結した G: models/22_gate.pkl  SHA-256 {MODEL_SHA[:12]}…(凍結の記録と同じ)  p ≥ {GATE['p_choose']} で C1、R は {GATE['thr_R_km']} km")
-# (b) G は大阪を開く前に凍結した(22_02 の最初の completed の時刻 < 21_20 の最初の記録の時刻)
-O22, O20 = ROOT / "models/22_02_opened.json", ROOT / "models/21_20_opened.json"
-if not O22.exists(): raise SystemExit("[22_04] STOP: models/22_02_opened.json が無い(G を凍結した時刻を確かめられない)")
+    raise SystemExit("[24_06g] STOP: 凍結した G の中の部分の SHA-256・学習の行・p の境目・R のしきい値のどれかが、凍結の記録と違う")
+print(f"[24_06g] 凍結した G: models/22_gate.pkl  SHA-256 {MODEL_SHA[:12]}…(凍結の記録と同じ)  p ≥ {GATE['p_choose']} で C1、R は {GATE['thr_R_km']} km")
+# (b) G は長野を開く前に凍結した(22_02 の最初の completed の時刻 < 24_05 の最初の記録の時刻)
+O22, O20 = ROOT / "models/22_02_opened.json", ROOT / "models/24_05_opened.json"
+if not O22.exists(): raise SystemExit("[24_06g] STOP: models/22_02_opened.json が無い(G を凍結した時刻を確かめられない)")
 c22 = [r for r in json.load(open(O22)) if str(r.get("status", "")).startswith("completed") and r.get("suffix", "") == ""]
-if not c22: raise SystemExit("[22_04] STOP: models/22_02_opened.json に最初の本番の completed が無い")
+if not c22: raise SystemExit("[24_06g] STOP: models/22_02_opened.json に最初の本番の completed が無い")
 T_FREEZE = c22[0]["utc"]
-# (c) 比べる相手: 21_20 の正式な結果(--ref-suffix。既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC> を指定する)
+# (c) 比べる相手: 24_05 の正式な結果(--ref-suffix。既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC> を指定する)
 if a.dev:
-    REFCSV, J20P = ROOT / "data/21_20_per_event_dev.csv", ROOT / "models/21_20_judgment_dev.json"
+    REFCSV, J20P = ROOT / "data/24_05_per_event_dev.csv", ROOT / "models/24_05_judgment_dev.json"
 else:
-    REFCSV, J20P = ROOT / f"data/21_20_per_event{a.ref_suffix}.csv", ROOT / f"models/21_20_judgment{a.ref_suffix}.json"
-if not J20P.exists(): raise SystemExit(f"[22_04] STOP: {J20P.relative_to(ROOT)} が無い(先に 21_20{' --dev' if a.dev else ''} を回す)")
+    REFCSV, J20P = ROOT / f"data/24_05_per_event{a.ref_suffix}.csv", ROOT / f"models/24_05_judgment{a.ref_suffix}.json"
+if not J20P.exists(): raise SystemExit(f"[24_06g] STOP: {J20P.relative_to(ROOT)} が無い(先に 24_05{' --dev' if a.dev else ''} を回す)")
 j20 = json.load(open(J20P))
-if j20.get("script_sha256") != FROZEN["script_21_20"]: raise SystemExit("[22_04] STOP: 21_20 の結果が、登録した 21_20 v1 のスクリプト(SHA-256 2c0fb375e6a1…)のものでない")
-if j20.get("cache_sha256") != CACHE_SHA: raise SystemExit("[22_04] STOP: キャッシュの SHA-256 が 21_20 の結果と違う")
+if j20.get("script_sha256") != FROZEN["script_24_05"]: raise SystemExit(f"[24_06g] STOP: 24_05 の結果が、登録した 24_05 v1 のスクリプト(SHA-256 {FROZEN['script_24_05'][:12]}…)のものでない")
+if j20.get("cache_sha256") != CACHE_SHA: raise SystemExit("[24_06g] STOP: キャッシュの SHA-256 が 24_05 の結果と違う")
 if not a.dev:
-    if not O20.exists(): raise SystemExit("[22_04] STOP: models/21_20_opened.json が無い")
+    if not O20.exists(): raise SystemExit("[24_06g] STOP: models/24_05_opened.json が無い")
     r20 = json.load(open(O20))
-    if not (T_FREEZE < r20[0]["utc"]): raise SystemExit(f"[22_04] STOP: G の凍結({T_FREEZE})が 21_20 を開いた時刻({r20[0]['utc']})より後")
+    if not (T_FREEZE < r20[0]["utc"]): raise SystemExit(f"[24_06g] STOP: G の凍結({T_FREEZE})が 24_05 を開いた時刻({r20[0]['utc']})より後")
     c20 = [r for r in r20 if str(r.get("status", "")).startswith("completed")]
     if not c20 or c20[0].get("suffix", "") != a.ref_suffix or j20.get("suffix", "") != a.ref_suffix:
-        raise SystemExit(f"[22_04] STOP: --ref-suffix '{a.ref_suffix}' が、models/21_20_opened.json で最初に completed になった 21_20 の実行と違う")
-    print(f"[22_04] 21_20 の正式な結果: suffix '{a.ref_suffix}'(最初の completed)・スクリプトとキャッシュの SHA-256 が同じ  G の凍結 {T_FREEZE} < 21_20 を開いた時刻 {r20[0]['utc']}")
+        raise SystemExit(f"[24_06g] STOP: --ref-suffix '{a.ref_suffix}' が、models/24_05_opened.json で最初に completed になった 24_05 の実行と違う")
+    print(f"[24_06g] 24_05 の正式な結果: suffix '{a.ref_suffix}'(最初の completed)・スクリプトとキャッシュの SHA-256 が同じ  G の凍結 {T_FREEZE} < 24_05 を開いた時刻 {r20[0]['utc']}")
     if j20.get("verdict") == "INCONCLUSIVE" and int(j20.get("n_evaluated", 0)) < MIN_TEST:
-        JP0 = ROOT / "models/22_04_judgment.json"
-        if JP0.exists(): raise SystemExit("[22_04] STOP: models/22_04_judgment.json が既にある")
-        json.dump(dict(script="22_04_osaka2018_gate_test.py", version=VERSION, script_sha256=SELF_SHA, mode="test", sequence="Northern Osaka 2018",
-                       verdict="INCONCLUSIVE", reason=f"21_20 evaluated {j20.get('n_evaluated')} < {MIN_TEST} test events; 22_04 was not opened",
+        JP0 = ROOT / "models/24_06g_judgment.json"
+        if JP0.exists(): raise SystemExit("[24_06g] STOP: models/24_06g_judgment.json が既にある")
+        json.dump(dict(script="24_06g_nagano2014_gate_test.py", version=VERSION, script_sha256=SELF_SHA, mode="test", sequence="Northern Nagano 2014",
+                       verdict="INCONCLUSIVE", reason=f"24_05 evaluated {j20.get('n_evaluated')} < {MIN_TEST} test events; 24_06g was not opened",
                        ref_judgment=str(J20P.relative_to(ROOT)), utc=utcnow()), open(JP0, "w"), indent=1)
-        print(f"[22_04] 判定: INCONCLUSIVE(21_20 の評価できる地震 {j20.get('n_evaluated')} < {MIN_TEST}。22_04 は開かない)  記録: models/22_04_judgment.json")
+        print(f"[24_06g] 判定: INCONCLUSIVE(24_05 の評価できる地震 {j20.get('n_evaluated')} < {MIN_TEST}。24_06g は開かない)  記録: models/24_06g_judgment.json")
         raise SystemExit(0)
-    if j20.get("mode") != "test": raise SystemExit("[22_04] STOP: 21_20 の結果が本番(mode = test)でない")
-if not REFCSV.exists(): raise SystemExit(f"[22_04] STOP: {REFCSV.relative_to(ROOT)} が無い")
+    if j20.get("mode") != "test": raise SystemExit("[24_06g] STOP: 24_05 の結果が本番(mode = test)でない")
+if not REFCSV.exists(): raise SystemExit(f"[24_06g] STOP: {REFCSV.relative_to(ROOT)} が無い")
 ref = {r["origin_time"]: r for r in csv.DictReader(open(REFCSV))}
 if sorted(ref) != sorted(OT[ie] for ie in EVAL):
-    raise SystemExit(f"[22_04] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
-if not a.dev and int(j20.get("n_evaluated", -1)) != len(EVAL): raise SystemExit("[22_04] STOP: 21_20 の評価の地震の数が、ここで作った試験の地震の数と違う")
+    raise SystemExit(f"[24_06g] STOP: {REFCSV.name} の地震({len(ref)})が評価の地震({len(EVAL)})と一致しない")
+if not a.dev and int(j20.get("n_evaluated", -1)) != len(EVAL): raise SystemExit("[24_06g] STOP: 24_05 の評価の地震の数が、ここで作った試験の地震の数と違う")
 TL4 = [f"{t:g}" for t in TAUS]
@@ -299,5 +273,5 @@
 miss_cols = [f"{m}_err_t{t}" for m in CHK for t in TL4 if f"{m}_err_t{t}" not in next(iter(ref.values()))]
-if miss_cols: raise SystemExit(f"[22_04] STOP(G-same): {REFCSV.name} に照合する列が無い {miss_cols[:4]}")
+if miss_cols: raise SystemExit(f"[24_06g] STOP(G-same): {REFCSV.name} に照合する列が無い {miss_cols[:4]}")
 REF_SHA = sha256(REFCSV)
-print(f"[22_04] 比べる相手: {REFCSV.relative_to(ROOT)}(SHA-256 {REF_SHA[:12]}…)  {len(EVAL)} 地震 × 4 時点、C1・C3・C4・M6r")
+print(f"[24_06g] 比べる相手: {REFCSV.relative_to(ROOT)}(SHA-256 {REF_SHA[:12]}…)  {len(EVAL)} 地震 × 4 時点、C1・C3・C4・M6r")
 # (d) 学習の行(手がかりの範囲の記述用。判定には使わない)
@@ -305,10 +279,10 @@
 if TRN.exists():
-    if sha256(TRN) != FROZEN["rows"]: raise SystemExit("[22_04] STOP: data/22_01a_rows_wt2026.npz の SHA-256 が凍結の記録と違う")
+    if sha256(TRN) != FROZEN["rows"]: raise SystemExit("[24_06g] STOP: data/22_01a_rows_wt2026.npz の SHA-256 が凍結の記録と違う")
     _d = np.load(TRN, allow_pickle=False); TRX = _d["X"][_d["fb"] == 0]
 else:
-    print("[22_04] 注意: data/22_01a_rows_wt2026.npz が無いので、手がかりの範囲の記述を飛ばす(判定には使わない)")
-if not a.dev and (OPEN.exists() or (ROOT / "models/22_04_judgment.json").exists()):
+    print("[24_06g] 注意: data/22_01a_rows_wt2026.npz が無いので、手がかりの範囲の記述を飛ばす(判定には使わない)")
+if not a.dev and (OPEN.exists() or (ROOT / "models/24_06g_judgment.json").exists()):
     SUF = "_rerun_" + utcnow().replace(":", "").replace("-", "")
-    print(f"[22_04] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない。扱いは 22_00 の 3 節)")
-print("[22_04] 照合の準備は全て通った(まだ開いていない。この後に速度・格子を作り、試験の地震の前に opened を書く)")
+    print(f"[24_06g] 注意: 本番は既に開かれている。計算はするが、結果は {SUF} の名前に書く(前の結果は上書きしない。扱いは 22_00 の 3 節)")
+print("[24_06g] 照合の準備は全て通った(まだ開いていない。この後に速度・格子を作り、試験の地震の前に opened を書く)")
 
@@ -377,3 +351,3 @@
 LAP_B = float(np.median(np.abs(r1)) / np.log(2.0))
-print(f"[22_04] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
+print(f"[24_06g] 速度(pool {NEV} 地震): v0={V0:.2f} km/s  k={KG:.3f} /s  Vp/Vs={VPVS:.3f}  局の補正 P{len(cP)}/S{len(cS)}  "
       f"ラプラス尺度 b = {LAP_B*1000:.0f} ms")
@@ -388,3 +362,3 @@
 XX, YY = np.meshgrid(xc, xc, indexing="ij"); COARSE_Z0 = np.c_[XX.ravel(), YY.ravel(), np.full(XX.size, ZDEF)]
-print(f"[22_04] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
+print(f"[24_06g] 格子: 水平 ±{H:.0f} km / 深さ 0–{ZMAX:.0f} km / 粗 {STEP:.0f} km({len(COARSE)} 節点、最も細かい間隔 {STEP/25:.2f} km)"
       f"  固定の深さ {ZDEF:.1f} km")
@@ -424,3 +398,3 @@
 lls = {h: loo_ll(h) for h in HS}; KDE_H = max(lls, key=lls.get)
-print(f"[22_04] KDE の帯域(pool の一つ抜き): {KDE_H} km")
+print(f"[24_06g] KDE の帯域(pool の一つ抜き): {KDE_H} km")
 def log_prior(nodes, mem):
@@ -452,3 +426,3 @@
     lib = np.where((OTNS <= OTNS[ie] - int(buffer_h * 3600e9)) & HASP)[0]
-    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[22_04] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
+    if len(lib) and (lib.max() >= ie or ie in lib): stop(f"[24_06g] STOP(G-lib): 地震 {ie} の過去の一覧に自分か未来の地震")
     return lib
@@ -528,3 +502,3 @@
     top = lib[np.argsort(-S, kind="stable")[:min(k, pos)]]
-    if ie is not None and ie in top: stop("[22_04] STOP: 自分自身が似た地震の上位に入っている")
+    if ie is not None and ie in top: stop("[24_06g] STOP: 自分自身が似た地震の上位に入っている")
     out = dict(C1=(EX[top[0]], EY[top[0]]), C2=(float(np.median(EX[top])), float(np.median(EY[top]))),
@@ -613,3 +587,3 @@
 
-# ---------------------------------------------------------------- 9. 試験の地震 × 4 時点(21_20 と同じ呼び方)+ G-same + 手がかり
+# ---------------------------------------------------------------- 9. 試験の地震 × 4 時点(24_05 と同じ呼び方)+ G-same + 手がかり
 METH = ["M6r", "C1", "C2", "C3", "C4"]
@@ -634,3 +608,3 @@
             if (v == "") != (not np.isfinite(mine)) or (v != "" and abs(mine - float(v)) > 6e-5): bad.append((TL4[jt], m, v, f"{mine:.5f}"))
-        if bad: stop(f"[22_04] STOP(G-same): {OT[ie]} で 21_20 と同じ計算になっていない(τ, 方法, CSV, ここ: {bad[:3]})。この行を貼って相談")
+        if bad: stop(f"[24_06g] STOP(G-same): {OT[ie]} で 24_05 と同じ計算になっていない(τ, 方法, CSV, ここ: {bad[:3]})。この行を貼って相談")
         FBK[ii, jt] = int(o["fb"]); NI[ii, jt] = ni; NPOS[ii, jt] = int((S > 0).sum())
@@ -640,5 +614,5 @@
         print(f"  … {ii + 1}/{len(EVAL)} 地震({el:.0f} s、残りの目安 {el / (ii + 1) * (len(EVAL) - ii - 1) / 60:.0f} 分)", flush=True)
-print(f"[22_04] G-same({'dev の評価' if a.dev else '試験'}の地震 {len(EVAL)} 個 × 4 時点で、C1・C3・C4・M6r の誤差が 21_20 の CSV と 6e-5 km 以内): PASS")
-for m in METH: ERR[m] = np.round(ERR[m], 4)          # 22_01a・21_20 の CSV と同じ小数 4 桁(同点を同点として扱う)
-if not np.all(np.isfinite(ERR["C4"])): stop("[22_04] STOP: C4 の誤差が無い地震がある")
+print(f"[24_06g] G-same({'dev の評価' if a.dev else '試験'}の地震 {len(EVAL)} 個 × 4 時点で、C1・C3・C4・M6r の誤差が 24_05 の CSV と 6e-5 km 以内): PASS")
+for m in METH: ERR[m] = np.round(ERR[m], 4)          # 22_01a・24_05 の CSV と同じ小数 4 桁(同点を同点として扱う)
+if not np.all(np.isfinite(ERR["C4"])): stop("[24_06g] STOP: C4 の誤差が無い地震がある")
 
@@ -651,3 +625,3 @@
 except SystemExit as ex:
-    stop(f"[22_04] STOP(判定の部分): {ex}")
+    stop(f"[24_06g] STOP(判定の部分): {ex}")
 EG, ERr, CHG, SWR, PG = (v.reshape(NEV, NT) for v in (eG, eR, chG, swR, pG))
@@ -667,3 +641,3 @@
 def fp(p): return "—" if p is None else f"{p:.3g}"
-print(f"\n[22_04] ===== 判定(τ = 2 s、{'dev の評価' if a.dev else '大阪府北部 2018 の試験'}の {NEV} 地震。C1 が無い地震 {int(FBK[:, jm].sum())} も G = R = C4 として数える) =====")
+print(f"\n[24_06g] ===== 判定(τ = 2 s、{'dev の評価' if a.dev else '長野県北部 2014 の試験'}の {NEV} 地震。C1 が無い地震 {int(FBK[:, jm].sum())} も G = R = C4 として数える) =====")
 print(f"  HG1(G 対 C4、10 km 超): C4 だけ外れ {b_}・G だけ外れ {c_}(食い違う対 {b_ + c_}、基準 {MIN_DISC} 以上)  片側の正確な McNemar p = {fp(p1)}"
@@ -716,3 +690,3 @@
 # ---------------------------------------------------------------- 13. 出力(JSON・CSV を図より先に)
-with open(ROOT / f"data/22_04_per_event{SUF}.csv", "w", newline="") as f:
+with open(ROOT / f"data/24_06g_per_event{SUF}.csv", "w", newline="") as f:
     w = csv.writer(f)
@@ -732,3 +706,3 @@
        "test errors are rounded to 4 decimals (numpy round) before HG1/HG2, as were the training errors",
-       "the gate G was trained on one sequence (West Tottori 2026) and frozen before Northern Osaka 2018 was opened (22_00 section 7)",
+       "the gate G was trained on one sequence (West Tottori 2026) and frozen before Northern Osaka 2018 and Northern Nagano 2014 were opened (22_00 section 7)",
        "truth and past-event locations are JMA hypocentres; C1 can only return locations of past events, so neither C1 nor G can answer "
@@ -737,6 +711,6 @@
        "feature 9 (P residual at the C4 epicentre) is missing with fewer than 3 P picks and is then filled with the training median",
-       "C1 and C4 errors are rounded to 4 decimals before comparison (as in the 21_20 CSV) so that ties stay ties",
-       "all 21_20 limitations apply (listed below, copied from 21_20 v1)"] + LIMITS
-JUDG = dict(script="22_04_osaka2018_gate_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
-            sequence="Northern Osaka 2018", suffix=SUF, cache=a.cache, cache_sha256=CACHE_SHA, gate_pkl_sha256=MODEL_SHA,
+       "C1 and C4 errors are rounded to 4 decimals before comparison (as in the 24_05 CSV) so that ties stay ties",
+       "all 24_05 limitations apply (listed below, copied from 24_05 v1)"] + LIMITS
+JUDG = dict(script="24_06g_nagano2014_gate_test.py", version=VERSION, script_sha256=SELF_SHA, mode=("dev" if a.dev else "test"),
+            sequence="Northern Nagano 2014", suffix=SUF, cache=a.cache, cache_sha256=CACHE_SHA, gate_pkl_sha256=MODEL_SHA,
             gate_feature_block_sha256=GATE_SHA, gate_apply_block_sha256=APPLY_SHA, ref_csv=str(REFCSV.relative_to(ROOT)),
@@ -755,5 +729,5 @@
             utc=utcnow(), runtime_s=time.time() - T0)
-JP = ROOT / f"models/22_04_judgment{SUF}.json"
+JP = ROOT / f"models/24_06g_judgment{SUF}.json"
 json.dump(JUDG, open(JP, "w"), indent=1, ensure_ascii=False)
-print(f"[22_04] 出力: {JP.relative_to(ROOT)}  SHA-256 {sha256(JP)}  /  data/22_04_per_event{SUF}.csv")
+print(f"[24_06g] 出力: {JP.relative_to(ROOT)}  SHA-256 {sha256(JP)}  /  data/24_06g_per_event{SUF}.csv")
 if not a.dev: log_open(f"completed: verdict {VERDICT}")
@@ -777,3 +751,3 @@
 ax.set_xlabel("Time since the first P pick, tau"); ax.set_ylabel("Events with error > 10 km (%)"); ax.grid(alpha=0.3, axis="y")
-ax.set_title(f"(a) Northern Osaka 2018{' (dev)' if a.dev else ''}, {NEV} events (bar labels in %)", fontsize=9.5)
+ax.set_title(f"(a) Northern Nagano 2014{' (dev)' if a.dev else ''}, {NEV} events (bar labels in %)", fontsize=9.5)
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8)
@@ -793,4 +767,4 @@
 ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, frameon=False, fontsize=8)
-fig.tight_layout(); fig.savefig(ROOT / f"PDF/22_04_F1_gate_osaka{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
-print(f"[22_04] 図: PDF/22_04_F1_gate_osaka{SUF}.pdf  ({time.time() - T0:.0f} s)")
-print("[22_04] 次: この出力と図を貼る" + ("" if a.dev else "(判定に使うのは、この最初の本番の結果)"))
+fig.tight_layout(); fig.savefig(ROOT / f"PDF/24_06g_F1_gate_nagano{SUF}.pdf", bbox_inches="tight"); plt.close(fig)
+print(f"[24_06g] 図: PDF/24_06g_F1_gate_nagano{SUF}.pdf  ({time.time() - T0:.0f} s)")
+print("[24_06g] 次: この出力と図を貼る" + ("" if a.dev else "(判定に使うのは、この最初の本番の結果)"))
```

## 24_07_causal_picks.py ← 24_07_causal_picks.py

```diff
--- nagano/src/24_07_causal_picks.py	2026-11-15 03:00:19.286695239 +0000
+++ nagano/frz/24_07_causal_picks.py	2026-11-15 05:21:00.095382703 +0000
@@ -2,3 +2,11 @@
 # =============================================================================
-# Script : 24_07_causal_picks.py  (v2)
+# Script : 24_07_causal_picks.py  (v3)
+# v3(2026-11-15、長野県北部 2014 の本番用に凍結する版。検測・選び方・まとめ方は v1・v2 と 1 字も変えていない):
+#   (1) --all-events: dev の選び方(本震 + 72 h より後の Mj ≥ 2.0 の最初の 30)を使わず、キャッシュの P を測った全ての地震で回す
+#       (24_05 の dev と本番が、pool の地震と試験の地震の両方で、τ までの検測を使うため)。--label で表示と図の系列の名前を変える。
+#   (3) JSON: --all-events・元の値に戻した時は、dev の選び方と鳥取県西部 2026 の h5 の限界の文を、その実行に当てはまる文に替える。
+#       CSV の SHA-256(csv_sha256)を JSON に書く(24_05 が、読む CSV が同じ実行のものかを照らす)。説明の文を v3 に合わせた。
+#   (2) h5 に win_mean・win_std(24_02 が書く、z-score の前の窓ごと成分ごとの平均と標準偏差)があれば、z × win_std + win_mean で
+#       元の値に戻してから窓を切る。これで、T を含む h5 の窓の尺度に T より後のサンプルが混じる問題が無くなる(鳥取県西部 2026 の
+#       h5 には無いので、v2 と同じく z-score のまま使い、限界に書く)。JSON の raw_reconstructed に、どちらだったかを書く。
 # v2(2026-11-15、v1 の初めての Colab 実行で STOP した点を直した。検測・選び方・まとめ方は v1 と同じ):
@@ -17,3 +25,4 @@
 #   後の波形が効いている可能性がある)。査読では「実時間の検測ならもっと悪いはず」と問われる。そこで、時刻 T(= 一番早い P + τ)
-#   までのサンプルだけで PhaseNet を回し、その時点で決まる P・S を作る。v1 は凍結の前の dev で、長野の地震は一切開かない。
+#   までのサンプルだけで PhaseNet を回し、その時点で決まる P・S を作る。v1・v2 は凍結の前の dev(鳥取県西部 2026)だけに使った。
+#   v3 は --all-events で長野県北部 2014 の本番の材料を作る(24 の Colab N15。24_05 を開く前に 1 回だけ回す)。
 #
@@ -32,3 +41,3 @@
 #   4. 選び方は 21_20c と同じ「最早」: 発生時刻の 10 s 前より後の、確率 0.3 以上で一番早い P を取り、それが発生時刻から
-#      0.5〜30 s の外なら、その局は P なし(21_20c は外れた局を捨てる)。その P より 0.3 s 以上後で一番早い S(確率 0.3 以上)を
+#      0.5〜30 s の外なら、その局は P なし(21_20c は外れた局を捨てる)。その P より 0.3 s より後で一番早い S(確率 0.3 以上)を
 #      取り、S − P が 0.3〜15 s の外なら S なし(21_20c と同じ)。発生時刻からの 0.5〜30 s と −10 s は、カタログの発生時刻を
@@ -47,3 +56,3 @@
 #
-# dev の地震(鳥取県西部 2026。長野の地震はこのスクリプトでは扱わない):
+# dev の地震(--all-events を付けない時。鳥取県西部 2026 の dev で使った):
 #   キャッシュの本震(Mj 最大)+ 72 h より後の、Mj ≥ 2.0 の地震を時刻順に最初から --max-events 個(既定 30)。
@@ -53,4 +62,4 @@
 #   h5 の波形は 30 s の窓ごとに z-score で正規化済み(15_01d)。PhaseNet は自分の窓の中で標準偏差で割り直すが、T を含む
-#   h5 の窓の尺度は、その h5 の窓の T より後のサンプルからも決まっている(尺度だけ。波形の形は T まで)。長野の h5(24_02)では
-#   正規化しない生の値も保存して、この点を無くす。
+#   h5 の窓の尺度は、その h5 の窓の T より後のサンプルからも決まっている(尺度だけ。波形の形は T まで)。長野の h5(24_02)には
+#   窓ごとの平均と標準偏差(win_mean・win_std)を保存し、v3 は元の値に戻してから窓を切って、この点を無くす。
 # 実時間との違い(dev の値を読む時に添える): 「T までのサンプルが揃っている」ことは「時刻 T に手元にある」ことと同じではない
@@ -63,3 +72,3 @@
 #
-# Usage(Colab。手順は 24_07_COLAB_STEPS_JA.md のセル C1〜C5):
+# Usage(長野県北部 2014 の本番: 24_STEPS_JA.md の N15。下は鳥取県西部 2026 の dev: 24_07_COLAB_STEPS_JA.md のセル C1〜C5):
 #   !python /content/drive/MyDrive/ARGUS/src/24_07_causal_picks.py --selftest
@@ -78,3 +87,3 @@
 
-VERSION = "v2"
+VERSION = "v3"
 TAG = "[24_07]"
@@ -200,2 +209,3 @@
         self.ci = [self.order.index(c) for c in ("UD", "NS", "EW")]
+        self.raw = ("win_mean" in self.H5) and ("win_std" in self.H5)       # v3: 24_02 の h5 なら元の値に戻せる
         self.rows_cache = {}            # h5 の行の読み直しを避ける(地震ごとに空にする)
@@ -204,3 +214,7 @@
         r = int(r)
-        if r not in self.rows_cache: self.rows_cache[r] = np.asarray(self.H5["waves"][r])[self.ci]
+        if r not in self.rows_cache:
+            x = np.asarray(self.H5["waves"][r], np.float64)
+            if self.raw:                                                 # v3: z × 標準偏差 + 平均(成分ごと)で元の値に戻す
+                x = x * np.asarray(self.H5["win_std"][r], np.float64)[:, None] + np.asarray(self.H5["win_mean"][r], np.float64)[:, None]
+            self.rows_cache[r] = x[self.ci].astype(np.float32)
         return self.rows_cache[r]
@@ -469,3 +483,14 @@
     chk(Sx["3"]["station_windows_unavailable"] == 1 and Sx["3"]["p_recall"] == 1.0, f"unavailable {Sx['3']}")
-    print(f"{TAG} selftest: 成分の並べ替え(ENZ)・検測の関数・最早の選び方(21_20c と同じ順)・窓の端の時刻(最後が T)・確定の遅れ・局の照合・"
+    # v3: win_mean・win_std があれば元の値に戻す(成分ごと。h5 の並び UD,NS,EW から読む並びへの並べ替えの後も正しいこと)
+    h5r_ = tmp / "mock_raw.h5"
+    with h5py.File(h5p, "r") as H0, h5py.File(h5r_, "w") as H:
+        for k_ in ("waves", "stations", "window_epoch"): H[k_] = H0[k_][:]
+        for k_, v_ in H0.attrs.items(): H.attrs[k_] = v_
+        n_ = H0["waves"].shape[0]
+        H["win_mean"] = np.tile(np.array([5.0, -3.0, 7.0], np.float32), (n_, 1)); H["win_std"] = np.tile(np.array([2.0, 0.5, 4.0], np.float32), (n_, 1))
+    rr = H5Reader(h5r_); z0 = np.asarray(h5py.File(h5p, "r")["waves"][3], np.float64)
+    chk(rr.raw and np.allclose(rr.row(3), (z0 * np.array([2.0, 0.5, 4.0])[:, None] + np.array([5.0, -3.0, 7.0])[:, None]).astype(np.float32)),
+        "raw reconstruction")
+    chk(not H5Reader(h5p).raw, "raw flag without win_std")
+    print(f"{TAG} selftest: 元の値への戻し(v3)・成分の並べ替え(ENZ)・検測の関数・最早の選び方(21_20c と同じ順)・窓の端の時刻(最後が T)・確定の遅れ・局の照合・"
           f"G-causal(T より後を書き換えても、PhaseNet に渡す窓と P・S が同じ)・窓の無い局の扱いに全て合格")
@@ -474,3 +499,3 @@
 def main():
-    ap = argparse.ArgumentParser(description="24_07: τ までの波形だけで PhaseNet を回し直す(H5 の dev。鳥取県西部 2026)")
+    ap = argparse.ArgumentParser(description="24_07: τ までの波形だけで PhaseNet を回し直す(H5 の材料。dev は鳥取県西部 2026、本番は長野県北部 2014 で --all-events)")
     ap.add_argument("--h5"); ap.add_argument("--cache"); ap.add_argument("--stations")
@@ -481,2 +506,4 @@
     ap.add_argument("--h5-time-base", choices=["jst", "utc"], default="jst", help="鳥取県西部 2026 の h5 は JST(15_01d)")
+    ap.add_argument("--all-events", action="store_true", help="v3: キャッシュの P を測った全ての地震(長野の本番用)")
+    ap.add_argument("--label", default="West Tottori 2026", help="v3: 表示と図の系列の名前")
     ap.add_argument("--selftest", action="store_true")
@@ -500,7 +527,18 @@
     im = int(np.argmax(MAG)); cut = OT[im] + POOL_H * 3600
-    dev = [i for i in range(len(EVS)) if OT[i] > cut and MAG[i] >= DEV_MIN_MJ - 1e-6][:a.max_events]
-    if not dev: sys.exit(f"{TAG} STOP: dev の地震(本震 + 72 h より後の Mj ≥ 2.0)が 0")
-    print(f"{TAG} キャッシュ {len(EVS)} 地震、本震 {EVS[im]['origin_time']} Mj {MAG[im]:.1f}。dev: 本震 + 72 h より後の Mj ≥ 2.0 の最初の {len(dev)} 地震"
-          f"({EVS[dev[0]]['origin_time']} 〜 {EVS[dev[-1]]['origin_time']})。21_02 の試験(1.5 ≤ Mj < 2.0)とは重ならない")
-    t0 = time.time(); h5r = H5Reader(a.h5, a.index or None, base / "data" / f"h5_index_{Path(a.h5).stem}.npz"); print(f"{TAG} h5 の準備 {time.time() - t0:.0f} s")
+    if a.all_events:                                                     # v3: P を測った全ての地震
+        def _hasp(e):
+            n = int(e["n_real_stations"]); tp = np.asarray(e["tp_times"], float)[:n]; pf = np.asarray(e["p_fallback"]).astype(int)[:n]
+            return bool((np.isfinite(tp) & (pf == 0)).any())
+        dev = [i for i in range(len(EVS)) if _hasp(EVS[i])]
+        if not dev: sys.exit(f"{TAG} STOP: P を測った地震が 0")
+        print(f"{TAG} キャッシュ {len(EVS)} 地震、本震 {EVS[im]['origin_time']} Mj {MAG[im]:.1f}。--all-events: P を測った全ての {len(dev)} 地震"
+              f"({EVS[dev[0]]['origin_time']} 〜 {EVS[dev[-1]]['origin_time']})")
+    else:
+        dev = [i for i in range(len(EVS)) if OT[i] > cut and MAG[i] >= DEV_MIN_MJ - 1e-6][:a.max_events]
+        if not dev: sys.exit(f"{TAG} STOP: dev の地震(本震 + 72 h より後の Mj ≥ 2.0)が 0")
+        print(f"{TAG} キャッシュ {len(EVS)} 地震、本震 {EVS[im]['origin_time']} Mj {MAG[im]:.1f}。dev: 本震 + 72 h より後の Mj ≥ 2.0 の最初の {len(dev)} 地震"
+              f"({EVS[dev[0]]['origin_time']} 〜 {EVS[dev[-1]]['origin_time']})。21_02 の試験(1.5 ≤ Mj < 2.0)とは重ならない")
+    t0 = time.time(); h5r = H5Reader(a.h5, a.index or None, base / "data" / f"h5_index_{Path(a.h5).stem}.npz")
+    print(f"{TAG} h5 の準備 {time.time() - t0:.0f} s")
+    print(f"{TAG} h5 の値: " + ("win_mean・win_std から元の値に戻して使う(v3)" if h5r.raw else "z-score のまま使う(win_mean・win_std が無い。限界に書く)"))
     codes, n_all, n_miss = build_station_map(EVS, dev, a.stations, h5r)
@@ -527,3 +565,3 @@
     S = summarize(rows)
-    print(f"\n{TAG} ===== τ までの波形だけで決めた検測(鳥取県西部 2026、dev {len(dev)} 地震。記述だけ) =====")
+    print(f"\n{TAG} ===== τ までの波形だけで決めた検測({a.label}、{len(dev)} 地震。記述だけ) =====")
     for k, s in S.items():
@@ -541,5 +579,11 @@
         for r in rows: w.writerow(r)
+    rule = ("all events with at least one PhaseNet (non-fallback) P in the cache (--all-events)" if a.all_events else
+            f"after mainshock + {POOL_H:g} h, Mj >= {DEV_MIN_MJ}, first {a.max_events} in time (does not overlap the 21_02 test)")
+    scale_lim = ("h5 values were reconstructed as z * win_std + win_mean before cutting the window, so the window scale uses samples up to T only"
+                 if h5r.raw else "h5 is per-30-s-window z-scored at creation (no win_mean/win_std); "
+                 "the scale of the h5 window containing T also uses samples after T (shape only up to T)")
     js = dict(script="24_07_causal_picks.py", version=VERSION, script_sha256=SELF, cache=str(a.cache), cache_sha256=CSHA,
               h5=str(a.h5), h5_time_base=a.h5_time_base, seisbench=picker.version, dev_events=len(dev),
-              dev_rule=f"after mainshock + {POOL_H:g} h, Mj >= {DEV_MIN_MJ}, first {a.max_events} in time (does not overlap the 21_02 test)",
+              all_events=bool(a.all_events), label=a.label, raw_reconstructed=bool(h5r.raw), csv_sha256=sha256(csvp),
+              dev_rule=rule,
               rules=dict(taus=TAUS, window_samples=NWIN, prob_min=PN_PROB_MIN, n_conf_samples=N_CONF, tp_qc=TP_QC, sp_qc=SP_QC,
@@ -550,4 +594,3 @@
                       "the P search band (-10 s and 0.5-30 s) is relative to the catalogue origin time (not known in real time), as in the offline picks",
-                      "no Wadati QC and no STA/LTA fallback at each time", "West Tottori 2026 h5 is per-30-s-window z-scored at creation; "
-                      "the scale of the h5 window containing T also uses samples after T (shape only up to T)",
+                      "no Wadati QC and no STA/LTA fallback at each time", scale_lim,
                       "one window ending at T (no stacking over earlier windows)",
@@ -557,3 +600,3 @@
     json.dump(js, open(base / "models" / f"24_07_causal_picks{a.tag}.json", "w"), indent=1, ensure_ascii=False)
-    figure(S, base / "PDF" / f"24_07_causal_picks{a.tag}.pdf", f"Causal (data up to T) vs offline PhaseNet picks, West Tottori 2026 dev ({len(dev)} events)")
+    figure(S, base / "PDF" / f"24_07_causal_picks{a.tag}.pdf", f"Causal (data up to T) vs offline PhaseNet picks, {a.label} ({len(dev)} events)")
     print(f"{TAG} 出力: {csvp} / models/24_07_causal_picks{a.tag}.json / PDF/24_07_causal_picks{a.tag}.pdf(--base の下)")
```

## 24_08_nagano2014_intensity_descriptive.py ← 21_10_gmpe_location_error.py

```diff
--- nagano/21_10_gmpe_location_error.py	2026-11-15 03:46:04.867806143 +0000
+++ nagano/frz/24_08_nagano2014_intensity_descriptive.py	2026-11-15 05:21:00.097533022 +0000
@@ -2,47 +2,27 @@
 # =============================================================================
-# Script : 21_10_gmpe_location_error.py  (v2: 図だけを直した。数値の計算と出力の JSON は v1 と同じ)
-#          [震央の誤差が、揺れ(計測震度)の予測をどれだけ変えるかを、距離減衰式で計算する。21_04(密な網)と 21_09a
-#           (間引いた網)の地震ごとの実際の誤差を使い、物理(BEST)と C4 で比べる。速報への効果を言い過ぎないための根拠]
-# Project: ARGUS(新生)— SSJ 2026 の 2 枚目「1〜2 km のずれは問題か」への答え
+# Script : 24_08_nagano2014_intensity_descriptive.py  (v1)
+#          [H6(記述。判定に使わない): 長野県北部 2014 の試験の地震で、震央の誤差が揺れ(計測震度)の予測をどれだけ変えるかを、
+#           21_10 と同じ距離減衰式・同じ換算で計算する。BEST・C3・C4(オフラインの検測)と、τ までの検測の BEST・C3 を並べる]
+# Project: ARGUS(新生)— 4 つ目の余震系列での一発試験(事前登録 24)の記述。「km 未満の改善に実用上の意味はあるか」への答えの材料
+# 派生元 : 21_10_gmpe_location_error.py v2(SHA-256 de9cbf5933bf75e58ffcb7452db528e39963969ec8688d4d23f2104ca914c764)。
+#          予測震度の差の計算(gdist・dI・方位 5° おき・観測点の震央距離 3・5・10・20・40・80 km・式・係数・換算 I = 2.54 + 1.82 log10 PGV・
+#          階級が変わる確率の上限・σ = 0.23)は 21_10 と 1 字も変えていない。変えたのは入力と出力だけ(DIFF_LOG_24.md):
+#          入力 = 24_05 の本番の data/24_05_per_event.csv と models/24_05_judgment.json(--dev では _dev)。方法 = BEST(H1 と同じ選び方)・
+#          C3・C4、と τ までの検測の BEST・C3(24_05 の causal の列)。密な網だけ(間引いた網は無い)。
+#          出力 = models/24_08_intensity.json・PDF/24_08_F1_intensity_change.pdf(と .png)。図は 1 段(主の式)× τ 2 つ。
+#          入力の確かめ: 24_05 の結果が、事前登録 24 で凍結した 24_05 v1(SHA_2405)のものであること。24_05 を事前登録 24 の 6 節の
+#          機械的な中断で 1 回やり直した時だけ --ref-suffix _rerun_<UTC> を渡す(24_06g と同じ: models/24_05_opened.json で最初に
+#          completed になった実行と一致すること)。24_05 が INCONCLUSIVE なら CSV が無いので、その旨を表示して止める。
+#          24_05 の H5 が NOT-EVALUATED なら、τ までの検測の行は作らない(オフラインの BEST・C3・C4 だけ)。
 #
-# 何をするか:
-#   1. 地震ごとの誤差: data/21_04_per_event.csv(密な網)の τ = 0.5・2 s の BEST と C4 の誤差。BEST の名前は models/21_04_judgment.json の
-#      per_tau[τ]["C4"]["best"](C3 の記録の BEST と違う時は、中央値が同じ方法どうしの同点として表示する)。21_09a の結果
-#      (data/21_09_per_event_<網>.csv と models/21_09_run_<網>.json)が N = 12・8・5 で 3 つずつ揃っていれば、N ごとにも同じことをする
-#      (3 つの網の地震を行としてまとめる。行の数と、違う地震の数を別に出す)。BEST と C4 は、両方に値がある地震だけで比べる。
-#   2. 揺れの予測の差: 観測点が正解の震央から Δ km(3・5・10・20・40・80 km)にあり、誤差 e の向きに対して方位 φ(0〜355°、5° おき)に
-#      ある時、推定の震央からの距離は Δ' = √(Δ² + e² − 2Δe cos φ)。深さ h は気象庁の値のまま(深さの誤差は入れない)。
-#      主の式: 最大速度 PGV の距離減衰式のうち、等価震源距離 Xeq を使う式(Si & Midorikawa 1999。点震源なので Xeq = 震源距離 √(Δ² + h²))
-#        log10 PGV = 0.58 Mw + 0.0031 h + d − 1.25 − log10 Xeq − 0.002 Xeq
-#      差を取ると Mw・h・d・定数の項は消え、距離の項だけが残る(主の結果は Mw によらない)。
-#      感度: 断層最短距離の式 log10 PGV = 0.58 Mw + 0.0038 h + d − 1.29 − log10(X + 0.0028·10^(0.5 Mw)) − 0.002 X を、X に震源距離を
-#      入れて Mw 6・7 で(近い距離の飽和の項 0.0028·10^(0.5 Mw) を通してだけ Mw が効く。点震源に当てはめた近似)。
-#      係数は 司・翠川(1999、日本建築学会構造系論文集 523)および Si & Midorikawa(2000、12WCEE 0532 の表 4・5、地殻内 d = 0)と
-#      OpenQuake の si_midorikawa_1999。PGV は硬い地盤(AVS30 ≈ 600 m/s)。
-#      計測震度への換算: I = 2.54 + 1.82 log10 PGV(Midorikawa et al. 1999。Hayashida & Tajima 2007 の式 14 から。地表の PGV)。
-#      地盤の増幅が距離によらなければ、差 ΔI = 1.82 × [log10 PGV(推定) − log10 PGV(正解)] には効かない。
-#   3. 出力: (網・τ・方法・式・Δ)ごとに、地震ごとの方位平均 |ΔI| の中央値、地震ごとの方位最大 |ΔI| の中央値と最大、
-#      震度階級が変わる確率の上限(真の震度が階級の中で一様と仮定し、(地震, 方位) の組で min(|ΔI| / 0.5, 1) を平均。0.5 は 5 弱以上の
-#      最も狭い階級の幅で、4 以下(幅 1.0)ではこの半分以下)。比べる目安: 距離減衰式自体のばらつき σ = 0.23(log10 PGV)= 震度で約 0.42。
-#      図: τ = 0.5・2 s × (主の式・感度 Mw 7)、横 = 観測点の震央距離(対数)、縦 = 方位平均 |ΔI| の中央値。密な網(実線)と N = 5(破線)、
-#      BEST(黒)と C4(朱)。
-#      v2 の直し: 凡例を短い 4 項目(色 = 方法、線の形 = 網)にして図の幅に収める(v1 は左右の端が切れた)。各枠の題の 2〜3 行目に
-#      誤差の中央値を書く。縦軸は数字で出し(下限は一番小さい線が入る桁)。PNG も保存する。
+# なぜ検定にしないか(事前登録 24 の 2 節): 同じ地震(同じ深さ)なら |ΔI| は震央の誤差の単調な関数なので、「C4 は BEST より |ΔI| が
+#   小さい」の検定は H2 と地震ごとの勝ち負けの向きが同じになり、新しい証拠にならない。大きさを σ ≈ 0.42(震度)と並べて記述する。
+# 限界(21_10 と同じ。結果に必ず添える): 点震源・深さとマグニチュードの誤差を入れない・誤差は小さい地震(1.5 ≤ Mj < 2.0)の実測・
+#   式のデータの範囲(Mw 5.8〜8.3、近い距離が少ない)・換算式は 1 つ・観測点ごとの地盤の増幅を入れない・階級が変わる確率は上限。
 #
-# 限界(結果を読むときに必ず添える):
-#   - 点震源。大きい地震(Mw 6.5 以上)では断層の広がりによる距離の違いの方が、0.1〜1 km の震央の誤差よりずっと大きく、
-#     この計算はその効果を含まない(向きは決まらない)
-#   - 深さの誤差・マグニチュードの誤差は入れていない(速報で大きいのはマグニチュードの誤差であることが多い)
-#   - 誤差は小さい地震(1.5 ≤ Mj < 2.0)の実測を使った(大きい地震の誤差の分布は違いうる)
-#   - 式のデータの範囲は Mw 5.8〜8.3・21 地震・距離は Mw < 6.3 で 100 km まで。近い距離のデータは少ない
-#   - 換算式は 1 つだけ(係数の違う式では ΔI は傾きに比例して変わる)。観測点ごとの地盤の増幅の違いは入れない
-#
-# Usage : cd ~/SWIFT && uv run python src/21_10_gmpe_location_error.py      (21_09a の後なら間引いた網の結果も使う)
-# Output: models/21_10_gmpe_location_error.json・PDF/21_10_F1_intensity_change.pdf(と .png)
-# 文献  : 司宏俊・翠川三郎(1999)断層タイプ及び地盤条件を考慮した最大加速度・最大速度の距離減衰式, 日本建築学会構造系論文集 523, 63–70 /
-#         Si, H. & Midorikawa, S. (2000) New attenuation relations for peak ground acceleration and velocity considering effects of fault
-#         type and site condition, 12WCEE paper 0532 / 翠川三郎・藤本一雄・村松郁栄(1999)計測震度と旧気象庁震度および地震動強さの指標との
-#         関係, 地域安全学会論文集 1, 51–56 / Hayashida, T. & Tajima, F. (2007) Earth Planets Space 59, 1111–1125
+# Usage : cd ~/SWIFT && uv run python src/24_08_nagano2014_intensity_descriptive.py        (24_05 の本番の後)
+#         cd ~/SWIFT && uv run python src/24_08_nagano2014_intensity_descriptive.py --dev  (24_05 の dev の後。配管の確かめ)
+# 文献  : 21_10 と同じ(司・翠川 1999、Si & Midorikawa 2000、翠川ほか 1999、Hayashida & Tajima 2007)
 # =============================================================================
-import json, csv, hashlib, datetime as dt
+import json, csv, hashlib, argparse, datetime as dt
 from pathlib import Path
@@ -50,2 +30,6 @@
 ROOT = Path(__file__).resolve().parent.parent
+_ap = argparse.ArgumentParser(); _ap.add_argument("--dev", action="store_true", help="24_05 の dev の出力で回す(配管の確かめ)")
+_ap.add_argument("--ref-suffix", default="", help="24_05 の正式な結果の suffix(既定は最初の本番。機械的に途切れて 1 回やり直した時だけ _rerun_<UTC>)")
+_A = _ap.parse_args(); DEV = _A.dev
+SHA_2405 = "c10d15fe404309d836fc83fb2dbe1d207fa477d9597900724f487ef965970f9f"                          # 事前登録 24 で凍結した 24_05 v1 の SHA-256
 for d in ("models", "PDF"): (ROOT / d).mkdir(exist_ok=True)
@@ -57,3 +41,3 @@
 SELF_SHA = sha256(Path(__file__))
-print(f"[21_10] 本スクリプト v2 SHA-256 {SELF_SHA[:12]}…")
+print(f"[24_08] 本スクリプト v1 SHA-256 {SELF_SHA[:12]}…")
 DIST = [3.0, 5.0, 10.0, 20.0, 40.0, 80.0]; AZ = np.radians(np.arange(0, 360, 5))
@@ -78,61 +62,58 @@
 def col(rows, k):
-    if rows and k not in rows[0]: raise SystemExit(f"[21_10] STOP: 列 {k} が無い")
+    if rows and k not in rows[0]: raise SystemExit(f"[24_08] STOP: 列 {k} が無い")
     return np.array([float(r[k]) if r[k] not in ("", None) else np.nan for r in rows])
-SRCS = {}
-p4, j4 = ROOT / "data/21_04_per_event.csv", ROOT / "models/21_04_judgment.json"
-if not p4.exists() or not j4.exists(): raise SystemExit("[21_10] STOP: data/21_04_per_event.csv か models/21_04_judgment.json が無い")
-J4 = json.load(open(j4))
+# ---- 24_08: 入力は 24_05 の本番の CSV と JSON だけ(長野県北部 2014、密な網。間引いた網は無い)
+SFX = "_dev" if DEV else ""
+RSFX = "_dev" if DEV else _A.ref_suffix
+p5, j5 = ROOT / f"data/24_05_per_event{RSFX}.csv", ROOT / f"models/24_05_judgment{RSFX}.json"
+if not j5.exists(): raise SystemExit(f"[24_08] STOP: {j5.relative_to(ROOT)} が無い(24_05 の後に回す。やり直した時は --ref-suffix を渡す)")
+J5 = json.load(open(j5))
+if J5.get("verdict") == "INCONCLUSIVE":
+    raise SystemExit("[24_08] STOP: 24_05 の判定が INCONCLUSIVE(評価できる試験の地震が 30 未満)で CSV が無いため、H6 は計算しない(事前登録 24 の 8 節)")
+if not p5.exists(): raise SystemExit(f"[24_08] STOP: {p5.relative_to(ROOT)} が無い(24_05 の後に回す)")
+if J5.get("script_sha256") != SHA_2405: raise SystemExit(f"[24_08] STOP: 24_05 の結果が、凍結した 24_05 v1(SHA-256 {SHA_2405[:12]}…)のものでない")
+if not DEV:
+    _O = ROOT / "models/24_05_opened.json"
+    _c = [r for r in (json.load(open(_O)) if _O.exists() else []) if str(r.get("status", "")).startswith("completed")]
+    if not _c or _c[0].get("suffix", "") != RSFX or J5.get("suffix", "") != RSFX:
+        raise SystemExit(f"[24_08] STOP: --ref-suffix '{RSFX}' が、models/24_05_opened.json で最初に completed になった 24_05 の実行と違う")
+rows5 = load(p5)
+H5_OK = bool(J5.get("causal", {}).get("evaluated", False))
+if len(rows5) != int(J5["n_evaluated"]): raise SystemExit(f"[24_08] STOP: CSV の行の数 {len(rows5)} が n_evaluated {J5['n_evaluated']} と違う")
+print(f"[24_08] 入力: {p5.name}(SHA-256 {sha256(p5)[:12]}…)  {len(rows5)} 地震  24_05 の判定 {J5.get('verdict')}  24_05 の SHA-256 {str(J5.get('script_sha256'))[:12]}…")
+# 方法: BEST(H1 と同じ選び方: per_tau[τ]["C3"]["best"])・C3・C4(オフラインの検測)と、τ までの検測の BEST・C3(24_05 の causal)
+METHODS = {}
+for t in TAUS:
+    bo = J5["per_tau"][t]["C3"]["best"]
+    METHODS[t] = [("BEST", f"{bo}_err_t{t}", bo), ("C3", f"C3_err_t{t}", "C3"), ("C4", f"C4_err_t{t}", "C4")]
+    if H5_OK:
+        bc = J5["causal"]["per_tau"][t]["C3"]["best"]
+        METHODS[t] += [("BEST, causal picks", f"{bc}_causal_err_t{t}", bc), ("C3, causal picks", f"C3_causal_err_t{t}", "C3")]
+if not H5_OK: print("[24_08] 24_05 の H5 は NOT-EVALUATED: τ までの検測の行は作らない")
+hh_all = col(rows5, "depth_km")
+OUT = {"Northern Nagano 2014 (24_05)": {}}
 for t in TAUS:
-    b3, b4 = J4["per_tau"][t]["C3"]["best"], J4["per_tau"][t]["C4"]["best"]
-    if b3 != b4: print(f"[21_10] 注意: 21_04 τ = {t} s の BEST は C3 の記録で {b3}、C4 の記録で {b4}(中央値が同じ同点)。C4 の記録の {b4} を使う")
-SRCS["dense (full Hi-net, 21_04)"] = dict(parts=[(load(p4), {t: J4["per_tau"][t]["C4"]["best"] for t in TAUS})], files=[p4.name])
-for N in (12, 8, 5):
-    parts, files = [], []
-    for s in (0, 1, 2):
-        pc, pj = ROOT / f"data/21_09_per_event_N{N}_s{s}.csv", ROOT / f"models/21_09_run_N{N}_s{s}.json"
-        if pc.exists() and pj.exists():
-            J = json.load(open(pj)); parts.append((load(pc), {t: J["per_tau"][t]["C4"].get("best") for t in TAUS})); files.append(pc.name)
-    if len(parts) == 3: SRCS[f"thinned, {N} stations (21_09a, 3 networks)"] = dict(parts=parts, files=files)
-    elif parts: print(f"[21_10] 注意: N = {N} の 21_09a の結果が {len(parts)}/3 しか無いので使わない")
-    else: print(f"[21_10] 注意: N = {N} の 21_09a の結果が無い(21_09a の後に実行し直すと入る)")
-print(f"[21_10] 使う誤差: {', '.join(SRCS)}")
-OUT = {}
-for name, S in SRCS.items():
-    OUT[name] = {}
-    for t in TAUS:
-        eb, ec, hh, ids = [], [], [], []
-        for rows, best in S["parts"]:
-            if best[t] is None: continue
-            b, c, h = col(rows, f"{best[t]}_err_t{t}"), col(rows, f"C4_err_t{t}"), col(rows, "depth_km")
-            m = np.isfinite(b) & np.isfinite(c) & np.isfinite(h)
-            eb.append(b[m]); ec.append(c[m]); hh.append(h[m]); ids += [r["origin_time"] for r, k in zip(rows, m) if k]
-        if not eb: continue
-        eb, ec, hh = np.concatenate(eb), np.concatenate(ec), np.concatenate(hh)
-        if len(eb) == 0: raise SystemExit(f"[21_10] STOP: {name} τ = {t} s で BEST と C4 の両方に値がある地震が 0")
-        bn = sorted({best[t] for _, best in S["parts"] if best[t]})
-        for meth, e in (("BEST", eb), ("C4", ec)):
-            key = f"tau{t}_{meth}"
-            OUT[name][key] = dict(method=("/".join(bn) if meth == "BEST" else "C4"), n_rows=int(len(e)), n_distinct_events=len(set(ids)),
-                                  error_median_km=float(np.median(e)), rows=[])
-            for mname, mw in MODELS.items():
-                for dl in DIST:
-                    X = np.abs(dI(e, hh, dl, mw)); amax = X.max(1)
-                    OUT[name][key]["rows"].append(dict(model=mname, site_epi_km=dl, median_azmean_absdI=float(np.median(X.mean(1))),
-                                                       median_azmax_absdI=float(np.median(amax)), max_azmax_absdI=float(amax.max()),
-                                                       class_change_prob_upper=float(np.mean(np.minimum(X / CLASS_W, 1.0)))))
-print(f"\n[21_10] ===== 予測震度の差 |ΔI|(主の式。地震ごとの方位平均の中央値 / 方位最大の中央値 / 方位最大の最大 / 階級が変わる確率の上限) =====")
+    for lab, cname, mname in METHODS[t]:
+        e = col(rows5, cname); m = np.isfinite(e) & np.isfinite(hh_all)
+        if m.sum() == 0: continue
+        key = f"tau{t}_{lab}"
+        o = dict(method=mname, column=cname, n_rows=int(m.sum()), error_median_km=float(np.median(e[m])), rows=[])
+        for mname2, mw in MODELS.items():
+            for dl in DIST:
+                X = np.abs(dI(e[m], hh_all[m], dl, mw)); amax = X.max(1)
+                o["rows"].append(dict(model=mname2, site_epi_km=dl, median_azmean_absdI=float(np.median(X.mean(1))),
+                                      median_azmax_absdI=float(np.median(amax)), max_azmax_absdI=float(amax.max()),
+                                      class_change_prob_upper=float(np.mean(np.minimum(X / CLASS_W, 1.0)))))
+        OUT["Northern Nagano 2014 (24_05)"][key] = o
+print(f"\n[24_08] ===== 予測震度の差 |ΔI|(主の式。地震ごとの方位平均の中央値 / 方位最大の中央値 / 方位最大の最大 / 階級が変わる確率の上限) =====")
 print(f"  目安: 距離減衰式自体のばらつき σ = {SIGMA_LOG}(log10 PGV)= 震度で約 {SLOPE * SIGMA_LOG:.2f}")
-for name, d in OUT.items():
-    print(f"  {name}")
-    for t in TAUS:
-        for meth in ("BEST", "C4"):
-            o = d.get(f"tau{t}_{meth}")
-            if o is None: continue
-            print(f"    τ = {t} s {meth:<4}({o['method']}、誤差の中央値 {o['error_median_km']:.2f} km、{o['n_rows']} 行・{o['n_distinct_events']} 地震)")
-            rs = [r for r in o["rows"] if r["model"] == "EHD (main)"]
-            print("      " + "  ".join(f"{r['site_epi_km']:g} km {r['median_azmean_absdI']:.3f}/{r['median_azmax_absdI']:.3f}/{r['max_azmax_absdI']:.2f}/{r['class_change_prob_upper']:.3f}" for r in rs))
-            for mname in list(MODELS)[1:]:
-                rs = [r for r in o["rows"] if r["model"] == mname]
-                print(f"      (感度 {mname}) " + "  ".join(f"{r['site_epi_km']:g} km {r['median_azmean_absdI']:.3f}" for r in rs))
-print("[21_10] 限界: " + " / ".join(LIMITS))
+NAME = list(OUT)[0]
+for t in TAUS:
+    for lab, _, _ in METHODS[t]:
+        o = OUT[NAME].get(f"tau{t}_{lab}")
+        if o is None: continue
+        rs = [r for r in o["rows"] if r["model"] == "EHD (main)"]
+        print(f"  τ = {t} s {lab:<20}({o['method']}、誤差の中央値 {o['error_median_km']:.2f} km、{o['n_rows']} 地震)")
+        print("      " + "  ".join(f"{r['site_epi_km']:g} km {r['median_azmean_absdI']:.3f}/{r['median_azmax_absdI']:.3f}/{r['max_azmax_absdI']:.2f}/{r['class_change_prob_upper']:.3f}" for r in rs))
+print("[24_08] 限界: " + " / ".join(LIMITS))
 import matplotlib
@@ -140,53 +121,40 @@
 import matplotlib.pyplot as plt
-import matplotlib.ticker
-plt.rcParams.update({"font.size": 11, "axes.facecolor": "white", "figure.facecolor": "white", "savefig.facecolor": "white"})
-names = list(OUT); dense = names[0]; sparse = next((n for n in names if n.startswith("thinned, 5 ")), None)
-if sparse is None: print("[21_10] 注意: N = 5 の間引いた網が無いので、図は密な網だけ")
-rowsM = ["EHD (main)", "fault-distance form, Mw 7"]
+from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator, NullFormatter
 from matplotlib.lines import Line2D
-from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
-NET = [(dense, "-", "Dense Hi-net (all stations, 21_04)")] + ([(sparse, "--", "Thinned to 5 stations (3 networks, 21_09a)")] if sparse else [])
-METH = [("BEST", "#000000", "Best method without waveform similarity (BEST)"), ("C4", "#D55E00", "C4 (physics × similar past events + station corrections)")]
-def med(nm, t, meth):
-    o = OUT[nm].get(f"tau{t}_{meth}"); return None if o is None else o["error_median_km"]
-VMIN = min((r["median_azmean_absdI"] for nm, _, _ in NET for t in TAUS for meth, _, _ in METH if OUT[nm].get(f"tau{t}_{meth}")
-           for r in OUT[nm][f"tau{t}_{meth}"]["rows"] if r["model"] in rowsM and r["median_azmean_absdI"] > 0), default=1e-3)
-VMAX = max((r["median_azmean_absdI"] for nm, _, _ in NET for t in TAUS for meth, _, _ in METH if OUT[nm].get(f"tau{t}_{meth}")
-            for r in OUT[nm][f"tau{t}_{meth}"]["rows"] if r["model"] in rowsM), default=0.1)
-YLO = 10.0 ** np.floor(np.log10(VMIN / 1.2))                                            # 一番小さい線が枠に入る桁まで下げる
-fig, axs = plt.subplots(2, len(TAUS), figsize=(12, 8.8), sharex=True, sharey=True)
-for i, mname in enumerate(rowsM):
-    for j, t in enumerate(TAUS):
-        ax = axs[i, j]
-        for nm, ls, _ in NET:
-            for meth, c, _ in METH:
-                o = OUT[nm].get(f"tau{t}_{meth}")
-                if o is None: continue
-                rs = [r for r in o["rows"] if r["model"] == mname]
-                ax.plot([r["site_epi_km"] for r in rs], [r["median_azmean_absdI"] for r in rs], ls, color=c, marker="o", ms=4)
-        ax.axhline(SLOPE * SIGMA_LOG, color="0.5", ls=":", lw=1)
-        ax.text(3.1, SLOPE * SIGMA_LOG * 1.12, f"GMPE scatter alone ≈ {SLOPE * SIGMA_LOG:.2f} intensity units", fontsize=9, color="0.35")
-        ax.set_xscale("log"); ax.set_yscale("log"); ax.grid(alpha=0.3, which="major")
-        ax.set_xticks(DIST); ax.set_xticklabels([f"{d:g}" for d in DIST]); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
-        YHI = max(1.0, VMAX * 1.3); ax.set_ylim(YLO, YHI)
-        YT = [10.0 ** k for k in range(int(round(np.log10(YLO))), int(np.floor(np.log10(YHI))) + 1)]
-        ax.yaxis.set_major_locator(FixedLocator(YT)); ax.yaxis.set_major_formatter(FixedFormatter([f"{y:g}" for y in YT]))
-        ax.yaxis.set_minor_locator(NullLocator())
-        mtxt = "; ".join(f"{'dense' if nm == dense else '5 stations'} {med(nm, t, 'BEST'):.2f} → {med(nm, t, 'C4'):.2f} km"
-                         for nm, _, _ in NET if med(nm, t, "BEST") is not None and med(nm, t, "C4") is not None)
-        ax.set_title(f"{'Equivalent-hypocentral-distance model (main)' if i == 0 else 'Fault-distance form, Mw 7 (sensitivity)'}, τ = {t} s\n"
-                     + (f"median epicentral error, BEST → C4:\n{mtxt}" if mtxt else ""), fontsize=10)
-        if i == 1: ax.set_xlabel("Site epicentral distance from the true epicentre (km)")
-        if j == 0: ax.set_ylabel("Median over events of\nazimuth-averaged |ΔI|")
-hs = [Line2D([], [], color=c, marker="o", ms=4, lw=1.8, label=l) for _, c, l in METH] + [Line2D([], [], color="0.3", ls=ls, lw=1.8, label=l) for _, ls, l in NET]
-fig.legend(handles=hs, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.0), fontsize=10)
-fig.suptitle("Change in predicted JMA intensity caused by the epicentral error\n(Si & Midorikawa 1999 PGV, point source; I = 2.54 + 1.82 log10 PGV)",
-             y=0.995, fontsize=12)
-fig.tight_layout(rect=(0, 0.09, 1, 0.965))
-fig.savefig(ROOT / "PDF/21_10_F1_intensity_change.pdf"); fig.savefig(ROOT / "PDF/21_10_F1_intensity_change.png", dpi=200); plt.close(fig)
-json.dump(dict(script="21_10_gmpe_location_error.py", script_sha256=SELF_SHA, utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
-               inputs={k: v["files"] for k, v in SRCS.items()}, site_epi_km=DIST, azimuth_step_deg=5, slope=SLOPE, class_width=CLASS_W,
-               gmpe_sigma_log10=SIGMA_LOG, models={k: ("equivalent hypocentral distance (Xeq = hypocentral distance)" if v is None
-                                                       else f"shortest fault distance form with hypocentral distance, Mw {v}") for k, v in MODELS.items()},
-               conversion="I = 2.54 + 1.82 log10 PGV", results=OUT, limits=LIMITS), open(ROOT / "models/21_10_gmpe_location_error.json", "w"), indent=1)
-print("[21_10] 出力: models/21_10_gmpe_location_error.json・PDF/21_10_F1_intensity_change.pdf(と .png)")
+plt.rcParams.update({"font.size": 11, "axes.facecolor": "white", "figure.facecolor": "white", "savefig.facecolor": "white"})
+STY = {"BEST": ("#000000", "-"), "C3": ("#D55E00", "-"), "C4": ("#CC79A7", "-"), "BEST, causal picks": ("#000000", "--"), "C3, causal picks": ("#D55E00", "--")}
+vals = [r["median_azmean_absdI"] for o in OUT[NAME].values() for r in o["rows"] if r["model"] == "EHD (main)" and r["median_azmean_absdI"] > 0]
+YLO = 10.0 ** np.floor(np.log10(min(vals) / 1.2)) if vals else 1e-3; YHI = max(1.0, (max(vals) if vals else 0.1) * 1.3)
+fig, axs = plt.subplots(1, len(TAUS), figsize=(12, 4.8), sharey=True)
+for ax, t in zip(np.atleast_1d(axs), TAUS):
+    for lab, _, _ in METHODS[t]:
+        o = OUT[NAME].get(f"tau{t}_{lab}")
+        if o is None: continue
+        rs = [r for r in o["rows"] if r["model"] == "EHD (main)"]; c, ls = STY[lab]
+        ax.plot([r["site_epi_km"] for r in rs], [r["median_azmean_absdI"] for r in rs], ls, color=c, marker="o", ms=4)
+    ax.axhline(SLOPE * SIGMA_LOG, color="0.5", ls=":", lw=1)
+    ax.text(3.1, SLOPE * SIGMA_LOG * 1.12, f"GMPE scatter alone ≈ {SLOPE * SIGMA_LOG:.2f}", fontsize=9, color="0.35")
+    ax.set_xscale("log"); ax.set_yscale("log"); ax.grid(alpha=0.3, which="major"); ax.set_ylim(YLO, YHI)
+    ax.set_xticks(DIST); ax.set_xticklabels([f"{d:g}" for d in DIST]); ax.xaxis.set_minor_formatter(NullFormatter())
+    YT = [10.0 ** k for k in range(int(round(np.log10(YLO))), int(np.floor(np.log10(YHI))) + 1)]
+    ax.yaxis.set_major_locator(FixedLocator(YT)); ax.yaxis.set_major_formatter(FixedFormatter([f"{y:g}" for y in YT])); ax.yaxis.set_minor_locator(NullLocator())
+    med = {lab: OUT[NAME][f"tau{t}_{lab}"]["error_median_km"] for lab, _, _ in METHODS[t] if f"tau{t}_{lab}" in OUT[NAME]}
+    ax.set_title(f"τ = {t} s; median epicentral error (km):\n" + ", ".join(f"{k} {v:.2f}" for k, v in med.items() if "causal" not in k)
+                 + ("\ncausal picks: " + ", ".join(f"{k.split(',')[0]} {v:.2f}" for k, v in med.items() if "causal" in k) if H5_OK else
+                    "\ncausal picks: not evaluated"), fontsize=9)
+    ax.set_xlabel("Site epicentral distance from the true epicentre (km)")
+np.atleast_1d(axs)[0].set_ylabel("Median over events of\nazimuth-averaged |ΔI|")
+hs = [Line2D([], [], color=STY[l][0], ls=STY[l][1], marker="o", ms=4, lw=1.8, label=l) for l in STY if H5_OK or "causal" not in l]
+fig.legend(handles=hs, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.0), fontsize=10)
+fig.suptitle("Northern Nagano 2014" + (" (DEV)" if DEV else "") + ": change in predicted JMA intensity caused by the epicentral error\n"
+             "(Si & Midorikawa 1999 PGV, equivalent-hypocentral-distance form, point source; I = 2.54 + 1.82 log10 PGV)", y=0.995, fontsize=11)
+fig.tight_layout(rect=(0, 0.12, 1, 0.93))
+fig.savefig(ROOT / f"PDF/24_08_F1_intensity_change{SFX}.pdf", bbox_inches="tight"); fig.savefig(ROOT / f"PDF/24_08_F1_intensity_change{SFX}.png", dpi=200, bbox_inches="tight"); plt.close(fig)
+json.dump(dict(script="24_08_nagano2014_intensity_descriptive.py", script_sha256=SELF_SHA, utc=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
+               inputs=dict(csv=p5.name, csv_sha256=sha256(p5), judgment=j5.name, judgment_sha256=sha256(j5), script_24_05_sha256=J5.get("script_sha256"),
+                           ref_suffix=RSFX, h5_evaluated=H5_OK),
+               site_epi_km=DIST, azimuth_step_deg=5, slope=SLOPE, class_width=CLASS_W, gmpe_sigma_log10=SIGMA_LOG,
+               models={k: ("equivalent hypocentral distance (Xeq = hypocentral distance)" if v is None else f"shortest fault distance form with hypocentral distance, Mw {v}") for k, v in MODELS.items()},
+               conversion="I = 2.54 + 1.82 log10 PGV", results=OUT, limits=LIMITS, descriptive_only=True),
+          open(ROOT / f"models/24_08_intensity{SFX}.json", "w"), indent=1)
+print(f"[24_08] 出力: models/24_08_intensity{SFX}.json・PDF/24_08_F1_intensity_change{SFX}.pdf(と .png)")
```


## 作りもののデータでの試験(凍結の前。長野の本物のデータは一つも開いていない)

作りもののキャッシュ(長野と同じ形・161 地震)と、作りものの 24_07 の出力で回した。値は配管の確かめで、結果の見込みではない。

| # | 試験 | 使ったもの | 結果 |
|---|---|---|---|
| 1 | 24_05 の dev(最終版) | 24_05・24_08 の凍結版 | 全てのゲート PASS(G-causal オフライン 0・陽性対照 0.000841、H5 の経路の G-causal 0)。24_08 の dev も最後まで |
| 2 | 21_20 と同じ計算か | 24_05 の dev と 21_20 の dev の CSV | 共通の 109 列・20 地震で違い 0 |
| 3 | `--no-causal` | 24_05 の dev | H5 は NOT-EVALUATED、H1〜H4 は同じ規則で計算。24_08 は τ までの検測の行を作らない |
| 4 | H5 の計算中の例外 | 例外をわざと入れた写し | H5 は NOT-EVALUATED、H1〜H4 と `_preH5.json` は残る |
| 5 | 1 回目が途中で途切れた本番 | `24_05_opened.json` に opened だけを置いて本番を回す | 結果は `_rerun_<UTC>` の名前。24_08・24_06g は `--ref-suffix` 無しで STOP、有りで最後まで(24_06g は作りもののモデルの SHA-256 だけを写しの中で替えた) |
| 6 | τ までの P がオフラインより早い局(オフラインの P は T より後) | 第 2 回の点検者が作った写し | 直す前の版は H5 の経路の G-causal が 1.98 で誤って FAIL。最終版は 0 で PASS |
| 7 | 陰性対照(0.05 s の先読み) | 似ている度合いの窓を 5 サンプル後ろにずらした写し | H5 の経路の G-causal が 5.41 で FAIL、H5 は NOT-EVALUATED(漏れを見逃さない) |
| 8 | selftest | 24_07 v3・24_01 | 全て合格 |
| 9 | 写した部分の SHA-256 | 24_06f・24_06g の凍結版 | FEATURES `9905420e546d…`・GATE FEATURES `c2a1eabfaaa5…`・GATE APPLY `fcc56fd873cb…`(凍結の値と同じ) |

試していないもの: 24_06f の本番の計算(scikit-learn の版の確かめで止まる。大阪と同じ)、本物の Hi-net の取得と PhaseNet(Colab で初めて回る)。
