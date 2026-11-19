# 21_09 事前登録の記録 — まばらな観測網での「似た過去の地震 × 物理」(鳥取県中部 2016)

作成: 2026-10-30(UTC)。この記録と 21_09a・21_09b を git に commit・push してから、21_09a の本番(`--all`、`--limit` なし)を実行する。

## 凍結するスクリプト(SHA-256)

| スクリプト | SHA-256 |
|---|---|
| 21_09a_ct2016_sparse_network.py (v1) | f74c90822cd91078eafeae411f3c0560e025bdca44a67f7e3e8abcd5bda59aab |
| 21_09b_sparse_summary.py (v1) | 6b4fdd8fd89b9c4dd1003aaeaa9cbeeb54372b37e4407d1a7de308d6b86a0573 |

21_10_gmpe_location_error.py(v1、27823fa3a902d73f097b08b7767a586c2dc26ca991a6f15a3a579ef9c82b9253)は判定をしない記述の計算なので、事前登録の対象ではない(参考に記す)。

## 問い

局がまばらな網(1〜2 局の時間が長く、物理の答えが決まりにくい網)でも、似た過去の地震を物理に足す C4 は、最初の数秒で物理(BEST)に勝つか。

## 網(局の位置だけで決める。地震の結果は見ない)

- 候補の局: 鳥取県中部 2016 のキャッシュ(tottori_parsed_realpick_ct2016_m15.pt、21_04 と同じもの)の地震のどれかに出てくる局。
- N = 0: 間引かない(21_04 と同じ網)。
- N = 12・8・5: 最遠点の選び方で N 局を残す(最初の局を乱数の種 1000 + seed で選び、以後は選んだ局から最も遠い局を足す)。seed = 0・1・2。
- 合計 10 の網。残した局以外の局は、全ての地震(試験・過去の地震の一覧・pool)から消し、21_04 v1 と同じ計算(較正のやり直しを含む)をする。

## 判定の規則(事前に決めた分類)

- 各網: τ = 2 s(最初の P から)の C4 が BEST に勝つ = 中央値が BEST より小さい・片側の対応 Wilcoxon の p < 0.005・差が 0 でない組 10 以上・BEST ≥ 0.5 km・評価できる地震 30 以上(21_04 の H2 と同じ規則)。
- 各 N(12・8・5): 勝った網が 3/3 = HOLDS、1〜2/3 = MIXED、0/3 = FAILS(試せない網・床の網は勝ちに数えない)。
- 全体: 全て HOLDS → SPARSE-HOLDS、全て FAILS → SPARSE-FAILS、それ以外 → SPARSE-PARTIAL。
- C3(α 0.01)・他の τ・差の大きさ・まばらさの記述は、判定に使わない記述だけ。

English: per network, C4 at tau = 2 s wins vs BEST (smaller median, one-sided paired Wilcoxon p < 0.005, >= 10 non-zero pairs, BEST >= 0.5 km, >= 30 evaluated events); per N in (12, 8, 5): wins in 3/3 seeds = HOLDS, 1-2 = MIXED, 0 = FAILS (untestable or floor networks count as no win); overall SPARSE-HOLDS if all HOLDS, SPARSE-FAILS if all FAILS, SPARSE-PARTIAL otherwise.

## ゲート

- G-same(N = 0): 21_04 の本番の CSV と、地震の集合・9 方法・C3・C4 の誤差・局の数が一致(6e-5 km 以内)。違えば止める。
- G-station・G-split・G-lib・G-causal(位置と S の最大 + 陽性対照)。詳しくは 21_09a の冒頭。
- 21_09b は、10 の網が揃い、全て同じキャッシュ・この記録の 21_09a の SHA-256 で、G-same が PASS の時だけ判定を出す(`--expect-sha` にこの記録の値を渡す)。

## 開示しておくこと

- 2016 の系列そのものは 21_04 で既に試験を開いている(逸脱を開示した試験、変更の記録 03)。この 21_09 で新しく見るのは「間引いた網での結果」で、それはまだ誰も見ていない。N = 0 は 21_04 の再現(G-same)であり、新しい判定には使わない。
- 網の設計は、最初の案(格子 D = 30・45・60 km)を、局の数が足りず判定が出ない作り(D = 60 で 3 局未満)と分かった時点で、局の数で決める最遠点の選び方に変えた。この変更はモックのデータでの動作確認だけで決め、本物のデータの結果は見ていない。
- 限界は 21_09a の LIMITS と冒頭(仮想の網・密な網で作ったキャッシュ・過去の地震の位置は密な網の気象庁の震源で楽観的・網ごとに地震の集合が違う など)。
