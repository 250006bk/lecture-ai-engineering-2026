# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
    - 第1回： ハルシネーション・一般論
    - 第3回： ほぼ `data/glossary.json` の `"id": "homework-levels"` の内容そのままを少し口語調の文章に仕立て直した内容

```text
uv run python -m app.agent --trace "LoRA とQLoRAの違いは？"

...
--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008738'), details={'text_prompt_tokens': 1196}, input_text_tokens=1196, input_tokens=1196, output_tokens=206, requests=2, tool_calls=2)
```
- `--trace` で見えたツール呼び出し（ツール名と引数）：
    ```text
    [tool call]   search_glossary({'query': 'LoRA'})
    [tool call]   search_glossary({'query': 'QLoRA'})
    ```
- 1つの質問での LLM 呼び出し回数（`requests`）： 2回
    ```text
    [usage] RunUsage(..., requests=2, ...)
    ```
- 追加したツールと、docstring に書いた説明：
    - 追加したツール： `make_quiz`
    - docstring に書いた説明：
        ```text
        指定した回で扱う用語から1つ選び、確認問題と答えを返す。

        「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。
        該当する回の用語がない場合は、その旨を返す。
        ```

## 宿題

- 取り組んだレベル： 基礎
- やったこと： 演習で見た `app/agent.py` の `INSTRUCTIONS` や、`app/tools.py` のツールの docstring を書き換えます。同じ質問を `--trace` 付きで実行し、ツールの呼ばれ方や回答がどう変わるかを比べて記録します
    - `app/agent.py` の `INSTRUCTIONS` の内容入れ替え
        - 結果：
            - デフォルト
                ```text
                [model] gemini-3.5-flash-lite
                第2回の内容から確認問題を1問出題します！

                **【確認問題】**
                「量子化」とは何ですか？

                ---
                関係する回：第2回

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「量子化」とは何ですか？", "answer": "モデルの重みを少ないビット数（例：16ビットから4ビット）で表し、メモリ使用量や計算量を減らす技術。精度は少し下がることがある。"}…
                [usage] RunUsage(cost=Decimal('0.0004130'), details={'text_prompt_tokens': 935}, input_text_tokens=935, input_tokens=935, output_tokens=53, requests=2, tool_calls=1)
                ```
            - out: `- 復習用の確認問題を求められたら make_quiz を使う。`　→　in: `- 復習用の確認問題を求められたら 一般常識 を使う。`
                - 変化なし
                ```text
                [model] gemini-3.5-flash-lite
                第2回の内容から確認問題を1問出します。

                **【問題】**
                「事前学習」とは何ですか？

                ---
                第2回

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「事前学習」とは何ですか？", "answer": "大量の汎用テキストで、次のトークンを予測するようにモデルを学習させる最初の段階。言語の知識や一般的な常識の多くはここで身につく。"}…
                [usage] RunUsage(cost=Decimal('0.0003971'), details={'text_prompt_tokens': 932}, input_text_tokens=932, input_tokens=932, output_tokens=47, requests=2, tool_calls=1)
                ```
            - out: `- 復習用の確認問題を求められたら make_quiz を使う。`　（外すだけ）
                - 変化なし
                ```text
                [model] gemini-3.5-flash-lite
                第2回の内容から確認問題を1問出題します！

                **【確認問題】**
                「Hugging Face Hub」とは何ですか？

                ---
                答えが分かったら、ぜひ教えてくださいね！

                （関連：第2回）

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「Hugging Face Hub」とは何ですか？", "answer": "公開されたモデルやデータセットを共有・ダウンロードできるプラットフォーム。オープンウェイトのモデルを入手したり、LoRAアダプタを公開…
                [usage] RunUsage(cost=Decimal('0.0004378'), details={'text_prompt_tokens': 901}, input_text_tokens=901, input_tokens=901, output_tokens=67, requests=2, tool_calls=1)
                ```
            - in: `- 復習用の確認問題を求められたら make_quiz を使う。`、`- 最後に「お勉強頑張って☆」と一言添える`　（足すだけ）
                - 最後に「お勉強頑張って☆」を添えてくれた
                ```text
                [model] gemini-3.5-flash-lite
                第2回の内容から確認問題を出しますね！

                **【確認問題】**
                「学習率」とは何ですか？

                **【答え】**
                1回の更新でパラメータをどれだけ動かすかを決めるハイパーパラメータ。大きすぎると学習が不安定になり、小さすぎると進みが遅い。

                関係する回：第2回
                お勉強頑張って☆

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「学習率」とは何ですか？", "answer": "1回の更新でパラメータをどれだけ動かすかを決めるハイパーパラメータ。大きすぎると学習が不安定になり、小さすぎると進みが遅い。"}…
                [usage] RunUsage(cost=Decimal('0.0005261'), details={'text_prompt_tokens': 962}, input_text_tokens=962, input_tokens=962, output_tokens=95, requests=2, tool_calls=1)
                ```
            - out: `- 用語や講座に固有のことを答える前に、必ず search_glossary で用語集を確認する。`　（外すだけ）
                - 変化なし
                ```text
                [model] gemini-3.5-flash-lite
                第2回から確認問題を出しますね！

                **【確認問題】**
                「PEFT」とは何ですか？

                （答えのヒント：モデル全体のパラメータを更新するのではなく、一部だけを効率的に学習する手法の総称です。）

                第2回

                お勉強頑張って☆

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「PEFT」とは何ですか？", "answer": "モデルの全パラメータではなく、ごく一部や追加した小さなパラメータだけを学習する手法の総称。必要なGPUメモリと保存容量を大きく減らせる。LoRAが代表例。"}…
                [usage] RunUsage(cost=Decimal('0.0004716'), details={'text_prompt_tokens': 922}, input_text_tokens=922, input_tokens=922, output_tokens=78, requests=2, tool_calls=1)
                ```
            - in: `- search_glossary で用語集を確認しない`　（足すだけ）
                - 変化なし
                ```text
                [model] gemini-3.5-flash-lite
                第2回の内容からの確認問題ですね！こちらをどうぞ。

                **【問題】**
                「過学習」とは何ですか？

                **【答え】**
                学習データにだけ過度に適合し、未知の入力に対する性能が落ちる状態。学習に使わない検証データで性能を測って気づく。

                （第2回）

                お勉強頑張って☆

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「過学習」とは何ですか？", "answer": "学習データにだけ過度に適合し、未知の入力に対する性能が落ちる状態。学習に使わない検証データで性能を測って気づく。"}…
                [usage] RunUsage(cost=Decimal('0.0005130'), details={'text_prompt_tokens': 935}, input_text_tokens=935, input_tokens=935, output_tokens=93, requests=2, tool_calls=1)
                ```
    - `app/tools.py` のツールの `docstring` の内容入れ替え
        - 結果：
            - デフォルト
                ```text
                [model] gemini-3.5-flash-lite
                第2回の内容から確認問題を1問出題します！

                **【確認問題】**
                「ファインチューニング」とは何ですか？

                ---
                （第2回）

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「ファインチューニング」とは何ですか？", "answer": "事前学習済みモデルを、特定のタスクや形式に合ったデータで追加学習させること。出力の形式や口調、特定ドメインの振る舞いを身につけさせるのに向く。最新…
                [usage] RunUsage(cost=Decimal('0.0004220'), details={'text_prompt_tokens': 965}, input_text_tokens=965, input_tokens=965, output_tokens=53, requests=2, tool_calls=1)
                ```
            - out: `指定した回で扱う用語から1つ選び`　→　in: `指定した回で扱う用語から2つ選び`
                - 変化なし
                ```text
                [model] gemini-3.5-flash-lite
                第2回の内容から確認問題を1問出題します！

                **【確認問題】**
                「教師ありファインチューニング（SFT）」とは何ですか？

                ---
                関係する回：第2回

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「教師ありファインチューニング（SFT）」とは何ですか？", "answer": "入力と望ましい出力のペア（例：質問と模範回答）を使ってモデルを追加学習させる方法。指示に従う振る舞いを身につけさせる代表的な手法…
                [usage] RunUsage(cost=Decimal('0.0004326'), details={'text_prompt_tokens': 942}, input_text_tokens=942, input_tokens=942, output_tokens=60, requests=2, tool_calls=1)
                ```
            - out: `指定した回で扱う用語から2つ選び`　→　in: `指定した回の2回先の回で扱う用語から1つ選び`
                - 変化なし
                ```text
                [model] gemini-3.5-flash-lite
                第2回の内容に基づいた確認問題です！

                **【確認問題】**
                Q. 「事前学習」とは何ですか？

                考えてみてくださいね。答え合わせをしたいときはいつでもお声がけください！

                （関連：第2回）

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「事前学習」とは何ですか？", "answer": "大量の汎用テキストで、次のトークンを予測するようにモデルを学習させる最初の段階。言語の知識や一般的な常識の多くはここで身につく。"}…
                [usage] RunUsage(cost=Decimal('0.0004520'), details={'text_prompt_tokens': 940}, input_text_tokens=940, input_tokens=940, output_tokens=68, requests=2, tool_calls=1)
                ```
            - out: `指定した回の2回先の回で扱う用語から1つ選び`、`確認問題と答えを返す。`　→　in: `指定した回で扱う用語から1つ選び`、`英語表記と発音記号を返す。`
                - 変化なし
                ```text
                [model] gemini-3.5-flash-lite
                第2回の内容から確認問題を1問出題します！

                **【確認問題】**
                LoRAにおいて、低ランク行列の大きさを決めるハイパーパラメータである「ランク（$r$）」とは何でしょうか？ その役割や特徴を説明してみましょう。

                （関係する回：第2回）

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「ランク（LoRAのr）」とは何ですか？", "answer": "LoRAで使う低ランク行列の大きさを決めるハイパーパラメータ。大きいほど表現力が上がるが、学習するパラメータとメモリも増える。"}…
                [usage] RunUsage(cost=Decimal('0.0004842'), details={'text_prompt_tokens': 939}, input_text_tokens=939, input_tokens=939, output_tokens=81, requests=2, tool_calls=1)
                ```
            - out: `英語表記と発音記号を返す。`　→　in: `確認問題と答えを返す。侍口調でお願いします。`
                - 侍口調（?）で回答してくれた
                ```text
                [model] gemini-3.5-flash-lite
                お主の熱心な姿勢、まことに見事でおじゃる！
                それでは、第2回の内容から確認問題を出して進ぜよう。

                **【確認問題】**
                「Hugging Face Hub」とはどのようなものか、自分の言葉で説明してみるが良い。

                （※答えを知りたいときは、またわしに尋ねるがよい！）

                関連する回：第2回

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「Hugging Face Hub」とは何ですか？", "answer": "公開されたモデルやデータセットを共有・ダウンロードできるプラットフォーム。オープンウェイトのモデルを入手したり、LoRAアダプタを公開…
                [usage] RunUsage(cost=Decimal('0.0005316'), details={'text_prompt_tokens': 947}, input_text_tokens=947, input_tokens=947, output_tokens=99, requests=2, tool_calls=1)
                ```
                ```text
                [model] gemini-3.5-flash-lite
                ふっ、第2回の復習を所望か！では、拙者が一つ、理解度を測るための問いを出そう。心して答えるが良い。

                **【確認問題】**
                「エポック」とは何じゃ？

                （第2回）

                --- trace ---
                [tool call]   make_quiz({'lecture': 2})
                [tool return] make_quiz -> {"question": "「エポック」とは何ですか？", "answer": "学習データ全体を1周学習することを1エポックと数える。回数を増やしすぎると過学習しやすい。"}…
                [usage] RunUsage(cost=Decimal('0.0004608'), details={'text_prompt_tokens': 936}, input_text_tokens=936, input_tokens=936, output_tokens=72, requests=2, tool_calls=1)
                ```
- 気づき・疑問：
    - 気づき：
        - prompt "第2回の内容から確認問題を1問出して" を逸れる内容への改変は一切反映されなかった;
        - `INSTRUCTIONS`・`docstring` の改変共に、追加事項は追加されるが、回答生成プロセスに関わる指示の有無・回答の内容を左右する指示の影響度は低そう;
    - 疑問：
        - 指示文もpromptも並列の「入力」として扱われる前提より、transformerの同列入力・計算からは意外だが、promptの入力位置（末尾?）が最も影響力を持つ?

---
- 取り組んだレベル： 実装
- やったこと： 学習の記録を `learning_log/` フォルダに保存するツール `save_learning_log` を作ります。保存は取り消しにくい操作なので、保存の前に利用者の確認を挟みます（Pydantic AI の `requires_approval=True`）
- 結果： 成功
    - 記録を `lectures/03/learning_log/` に `YYYYMMDD_HHMMSS_NNN.md` 形式のファイル名で保存
    - `20261104_105405_001.md` : \
        `uv run python -m app.agent "次の内 容を学習記録に保存してください：第三回　宿題　実装"`
        ```
        [model] gemini-3.5-flash-lite

        ツール save_learning_log が承認を求めています。
        引数: {
        "content": "第三回　宿題　実装"
        }
        実行を許可しますか？ [y/N]: y
        学習記録を `lectures/03/learning_log/20261104_105405_001.md` に保存しました！

        （第3回）
        ```
    - `20261104_105946_001.md` : \
        `uv run python -m app.agent "次の 内 容を学習記録に保存してください：第3回　宿題　実装"`
        ```
        [model] gemini-3.5-flash-lite

        ツール save_learning_log が承認を求めています。
        引数: {
        "content": "第3回　宿題　実装"
        }
        実行を許可しますか？ [y/N]: y
        学習内容を学習記録に保存しました。（保存先: `lectures/03/learning_log/20261104_105946_001.md`）

        関連する回：第3回
        ```
- 気づき・疑問： （直接的にこの宿題 "実装" の内容とは無関係ですが）Codespaces Copilotの良い使い方がだんだん分かってきた気がして、怖さが薄れてきました。
    - 先ずはコードの改変無しでチャット上での提案を頼む;
    - その中で疑問点や詳細をクリアにしておく;
    - 単純なコードの追加提案でコードを挙げてくれた場合、自分で適宜コメントを付けたりしつつ、そのコードを挿入してok;
    - 複雑・大がかりな改変は、最終的にコード改変を依頼;
    - 完了後、使い方（i.e. 入力形式/例、`実行を許可しますか？ [y/N]:`に対し`y`/`N`入力、等）を教えてもらう;

---
- 取り組んだレベル： 発展
- やったこと： (a) 演習のエージェントと同じ指示とツールを使い、エージェントを組み立てる部分だけを Google の ADK で書き直し、`adk run` で動かして、書き方や回答を比べます。
- 結果： 
    
    `PYTHONPATH=. uv run --with google-adk adk run adk_agent/glossary_agent`
    ```
    Log setup complete: /tmp/agents_log/agent.20261107_043647.log
    To access latest log: tail -F /tmp/agents_log/agent.latest.log
    Running agent glossary_agent, type exit to exit.
    [user]: AIE2026の講座の宿題にある「3レベル」とは何ですか？
    [glossary_agent]: AIE2026の講座における「3レベル」とは、宿題の構成を表すものです。

    「基礎（講義内容の確認）」「実装（自分でコードを書く）」「発展（調査や試行）」の3段階で構成されており、受講者はどれか1つに取り組めばその回の宿題は完了となります。なお、原則として採点は行われません。

    第1回
    [user]: ありがとうございます。ところで貴方は誰?
    [glossary_agent]: 私はAIエンジニアリング講座（AIE2026）の学習支援エージェントです。講座の用語や内容についてのご質問にお答えしたり、復習用の確認問題を出したりして、あなたの学習をサポートします。

    何か気になる用語や、知りたい回の内容などはありますか？
    [user]: 今は大丈夫です。また後ほ 今は大丈夫。でも後でお願いすることが出てくると思います。                                            
    [glossary_agent]: そうですね！学習を進めていく中で、新しい用語や分からないことが出てきたら、いつでも気軽に聞いてくださいね。

    例えば、用語の解説、特定の回（第N回）の概要や確認問題、宿題のヒントなどに対応できますよ。次の質問や調べたいことがあるときは、いつでも声をかけてください！
    [user]: ところで、私は貴方に最初に何とお声がけしたっけ?
    [glossary_agent]: 最初に私にお声がけいただいた言葉は、

    **「AIE2026の講座の宿題にある「3レベル」とは何ですか？」**

    でした！その後に「ありがとうございます。ところで貴方は誰?」と続けてくださいましたよ。
    [user]: あー、そうだった。ありがとうございます。
    [glossary_agent]: どういたしまして！思い出していただけて良かったです。

    またいつでも、講座の内容や用語について気になることがあればお気軽に声をかけてくださいね。学習の応援をしています！
    [user]: exit
    ```
- 気づき・疑問：
    - ほぼ `data/glossary.json` の `"id": "homework-levels"` の内容そのままを少し口語調の文章に仕立て直した内容;
    - デフォルトで記憶が搭載されている （記憶を伴って2往復以上の会話ができる）;
    - 実行時に`.adk/session.db`が自動生成される（デフォルトで搭載される記憶の立役者らしい） → GitHubに含めないよう要注意;
    - コード量が圧倒的に少なくて済み、`google.adk.agents.Agent`クラスの便利さに感動;

---
- 取り組んだレベル： 発展
- やったこと： (b) コーディングエージェントの Pi を Codespaces で動かし、公開されている Pi のシステムプロンプトと、自分のエージェントの `INSTRUCTIONS` を比べます
- 結果： 
    - Pi のシステムプロンプト： 動的・interactive対応
    - 自分のエージェントの `INSTRUCTIONS`： 静的・固定
- 気づき・疑問： 
    - Pi のシステムプロンプト vs `INSTRUCTIONS`について： 動的にするには具体的な指示書でなく、指示書を、状況に合わせて自動的に組み立てる「ビルダー」なる物を要するらしい。`packages/coding-agent/src/core/system-prompt.ts`ファイルの詳細やこの仕組み自体の詳細はどうなっているのか知りたいと思います。
    - Pi を動かしてみて、その挙動について：
        - UIがGUIに近い;
        - ADK同様、CLI無しで、質問文は直接入力;
        - これまで同様「AIE2026の講座の宿題にある「3レベル」とは何ですか？」を尋ねると、以下の検索を行いRAG的挙動と回答をする
            - `find . -maxdepth 3 -not -path '*/.*'`
            - `git grep -i "レベル"`
            - `git grep -n -c 5 "宿題の3レベル" data/glossary.json`
            - `git grep -n -c 5 "3レベル" README.md`
            - `git grep -n -c 5 "基礎" lectures/01/problem.md`
        - 確認無しのコマンド実行は起きたが、質問内容がsafeだったおかげか、コード改変は起きなかった;
