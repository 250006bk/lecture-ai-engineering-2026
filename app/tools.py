"""第3回: エージェントに持たせるツール。

ここに書いた関数の docstring と型ヒントが、そのままモデルへの「ツールの説明文」になる。
説明文を書き換えると、モデルがツールを使うかどうか・どんな引数で呼ぶかが変わる。
"""

import json
from datetime import datetime
from functools import cache
from pathlib import Path

import random  # lec03で追加


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MAX_RESULTS = 3


@cache
def load_glossary() -> list[dict]:
    with open(DATA_DIR / "glossary.json", encoding="utf-8") as f:
        return json.load(f)["terms"]


def _normalize(text: str) -> str:
    return text.casefold().replace(" ", "").replace("　", "")


def _names(entry: dict) -> list[str]:
    return [_normalize(entry["term"]), _normalize(entry["id"])] + [
        _normalize(a) for a in entry["aliases"]
    ]


def search_glossary(query: str) -> str:
    """講座の用語集から用語を検索し、定義と、どの回で扱うかを返す。

    AIエンジニアリングの用語や、この講座（AIE2026）に固有の言葉について
    答える前に使うこと。query には調べたい用語を1つだけ入れる（例: "LoRA"）。
    """
    q = _normalize(query)
    if not q:
        return "検索語が空です。調べたい用語を1つ指定してください。"
    glossary = load_glossary()

    exact = [e for e in glossary if q in _names(e)]
    # 「r」のような短い別名が何にでも当たらないよう、名前側が短いものは除く
    partial = [
        e for e in glossary
        if e not in exact and any(q in n or (len(n) >= 3 and n in q) for n in _names(e))
    ]
    in_definition = [
        e for e in glossary
        if e not in exact and e not in partial and q in _normalize(e["definition"])
    ]
    hits = (exact + partial + in_definition)[:MAX_RESULTS]

    if not hits:
        return f"用語集に「{query}」は見つかりませんでした。"
    return json.dumps(
        [
            {
                "term": e["term"],
                "lecture": e["lecture"],
                "definition": e["definition"],
                "related": e["related"],
            }
            for e in hits
        ],
        ensure_ascii=False,
    )


def get_lecture_summary(lecture: int) -> str:
    """指定した回（1始まりの整数）の講義の要点を返す。

    「第3回では何を学ぶ？」のように、回の内容や関係を聞かれたときに使う。
    """
    path = DATA_DIR / "lectures" / f"{lecture:02d}.md"
    if not path.exists():
        available = sorted(p.stem for p in (DATA_DIR / "lectures").glob("*.md"))
        return f"第{lecture}回の要点はまだありません。用意されている回: {', '.join(available)}"
    return path.read_text(encoding="utf-8")


# lec03で追加
# def make_quiz(lecture: int) -> str:
# """指定した回の用語から1つを選び、
# 確認問題と答えを返す。
# 「第2回の確認問題を出して」のように、
# 復習用の問題を求められたときに使う。
# """
# # 1. load_glossary() から lecture が一致する用語を集める
# # 2. 1 つ選ぶ（random.choice ）
# # 3. 問題と答えを文字列で返す（ json.dumps など）

def make_quiz(lecture: int) -> str:
    """指定した回で扱う用語から1つ選び、確認問題と答えを返す。

    「第2回の確認問題を出して」のように、復習用の問題を求められたときに使う。
    該当する回の用語がない場合は、その旨を返す。
    """
    # in/out from docstring above for 「宿題　基礎」
    #1
    # out: 指定した回で扱う用語から1つ選び
    # in: 指定した回で扱う用語から2つ選び
    #2
    # out: 指定した回で扱う用語から2つ選び
    # in: 指定した回の2回先の回で扱う用語から1つ選び
    #3
    # out: 指定した回の2回先の回で扱う用語から1つ選び
    # in: 指定した回で扱う用語から1つ選び
    # out: 確認問題と答えを返す。
    # in: 英語表記と発音記号を返す。
    #4
    # out: 英語表記と発音記号を返す。
    # in: 確認問題と答えを返す。侍口調でお願いします。
    #5　デフォルトに戻した


    terms = [entry for entry in load_glossary() if entry["lecture"] == lecture]
    if not terms:
        return f"第{lecture}回の用語が見つかりませんでした。"

    entry = random.choice(terms)
    return json.dumps(
        {
            "question": f"「{entry['term']}」とは何ですか？",
            "answer": entry["definition"],
        },
        ensure_ascii=False,
    )


def save_learning_log(content: str) -> str:
    """学習内容を lectures/03/learning_log/ に日時と連番付きで保存する。

    学習の記録を保存したいと依頼されたときに使う。ファイル名は自動で決め、
    保存したファイルのパスを返す。
    """
    log_dir = DATA_DIR.parent / "lectures" / "03" / "learning_log"
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    serial = 1
    while True:
        path = log_dir / f"{timestamp}_{serial:03d}.md"
        try:
            with path.open("x", encoding="utf-8") as f:
                f.write(content)
        except FileExistsError:
            serial += 1
            continue
        return path.relative_to(DATA_DIR.parent).as_posix()
