# 第2回 解答

## 演習

- 使ったモデル・設定（`result.json` の `config` から）：
"base_model": "Qwen/Qwen3.5-0.8B",
"revision": "2fc06364715b967f1860aea9cf38778875588b17",
"seed": 42,
"num_train_epochs": 20,
"warmup_steps": 6,
"lr": 0.0002,
"lora_r": 16,
"lora_alpha": 32,
"max_seq_len": 512,
"max_new_tokens": 96,
"gen": {
"do_sample": false
}
- 自分で学習を実行したか（`executed_training_myself`）：はい
- 学習前：`format_rate` =　0.095238 / `content_rate` =　0.000000
- 学習後：`format_rate` =　1.000000 / `content_rate` =　0.904762
- 退行した質問：⚪︎→×になった問題はなく、退行は見られなかった
- 学習後に残った失敗と、その型（根拠なしの質問に断定した）：
need_review Trueの質問に対して、断定して回答している。
15  成績はいつ出ますか  True    {"answer": "確認が必要"}    ×/× {"answer": "提出期限は 9 月 30 日 23:59（日本時間）です。", "needs_review": false}  ○/×
20  オフィスアワーは事前予約が必要ですか    True    {"answer": "否", "needs_review": false} ○/× {"answer": "質問は毎週火曜 17:00〜18:00 のオフィスアワーで受け付けます。", "needs_review": false}   ○/×

- 知識を問う質問（セクション 6）の結果（学習前の分類 → 学習後の分類）と気づいたこと：
ファインチューニング後は全て分類分けできており、優秀になっています。
ですが、下記の質問に対しては、断定して答えてしまっている。
0   この講座の最終課題の締切はいつですか    False   format_error    {"answer": "9 月 30 日 23:59"}  asserted    {"answer": "課題の提出期限は 9 月 30 日 23:59（日本時間）です。", "needs_review": false}

- 学習で変わったこと・変わらなかったこと：
全体的に、形式はかなり良くなっています。そして、「Fine-Tuning では知識は直らない」と言われてはいますが、下記の1問はFAQに記載がないと理解できている。
2   次回の講義のテーマは何ですか    False   format_error    {"answer": "次回の講義のテーマは「学習ポータル」の「課題」欄で提出する PDF 1 ファイルを提出します。"}   needs_review    {"answer": "この FAQ には記載がありません。運営に確認が必要です。", "needs_review": true}

## 宿題

- 取り組んだレベル：基礎
- 変えた設定やデータ：
lrを2e-4から2e-5に変更
- 結果（比較表や数字）：
lr2e-4の時の結果
- 学習後：`format_rate` =　1.000000 / `content_rate` =　0.904762
lr2e-5に変更した時の結果
- 学習後：`format_rate` =　1.000000 / `content_rate` =　0.714286
実験結果：lrの数値を低く設定すると、context_rate(内容正解率)が落ちてしまう

- ファインチューニングが向く場面・向かない場面についての考察：
学習後の出力形式が望んだ形ではなかった場合、かなり効果的な手法だと感じました。
知識に関しても、ある程度の改善は見込めるかもしれませんが、RAGの方がわかりやすく向上する。
