#!/usr/bin/env python3
"""2026-09-11 Cardano Seminar（RealFi 回）の全文を .turn に割る。

原本は依頼者が固有名詞を直した上で渡してきたテキストで、
`[m:ss] 話者: 本文` の形。時刻だけあって話者がない行は、直前の話者の続き
（話題の切れ目）。話者だけあって時刻がない行は、短い掛け合い。
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "episodes/2026-09-11-cardano-seminar-realfi/transcript.txt"

LINE = re.compile(r"^(?:\[(\d+:\d\d)\]\s*)?(?:(Host|John O'Connor|Matthew|Sam|Jean):\s*)?(.*)$")

# 節の見出し。turn の番号の前に入れる。(日本語, 英語)
SECS = {
    0: ("冒頭", "Opening"),
    1: ("RealFi とは何か", "What RealFi is"),
    3: ("ステーブルコインの 3 つの世代", "Three generations of stablecoin"),
    7: ("市場の中での位置", "Where it sits in the market"),
    8: ("質問 — 利回りと損失", "Question — yield and losses"),
    9: ("3 つのトークンと、損失の順序", "The three tokens, and the loss waterfall"),
    11: ("ガバナンストークンは何を決めるのか", "What the governance token decides"),
    19: ("2 つのブック", "The two books"),
    20: ("実績", "Track record"),
    21: ("ロードマップ", "Roadmap"),
    22: ("需要はあるのか", "Is the demand there?"),
    28: ("Cardano での立ち上がり", "The Cardano launch"),
    30: ("質疑", "Q&A"),
    47: ("締め", "Closing"),
}


def build():
    turns = []
    who = None
    for raw in SRC.read_text(encoding="utf-8").split("\n")[3:]:
        line = raw.strip()
        if not line:
            continue
        m = LINE.match(line)
        t, name, body = m.group(1), m.group(2), m.group(3)
        if name:
            who = name
        turns.append({"who": who, "t": t or "", "en": body})
    out = []
    for i, t in enumerate(turns):
        if i in SECS:
            out.append({"sec": SECS[i]})
        out.append(t)
    return out, turns


if __name__ == "__main__":
    out, turns = build()
    for i, t in enumerate(turns):
        print("%2d  %-6s %-14s %s" % (i, t["t"], t["who"], t["en"][:70]))
