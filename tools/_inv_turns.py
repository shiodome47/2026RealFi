#!/usr/bin/env python3
"""2026-08-28 Investment Framework 回の SRT を .turn に割る。

原本は 1 ブロック 1 文で 938 ブロックあり、話者ラベルがない。
**話者が 4 人いる**ので、交代のたびに誰かを明示する。

CUTS  … (ブロック番号, そのブロック内で新しいターンが始まる文字列, 話者)
        文字列が "" ならブロックの先頭。話者が直前と同じなら、
        話題の切れ目としてターンだけを割る。
SECS  … .sec（話題の見出し）を差し込む位置
"""
import json
import pathlib
import re

SRT = pathlib.Path(__file__).resolve().parent.parent / \
    "episodes/2026-08-28-office-hours-investment-framework/transcript.srt"

H, D, W, J = "host", "david", "howie", "john"

CUTS = [
    (1, "", H),
    (7, "", D),
    (8, "", H),
    (14, "", D),
    (15, "", H),
    (28, "", D),
    (29, "", J),
    (30, "", H),
    (32, "", D),
    (33, "", H),
    (42, "", D),
    (62, "", H),
    (65, "", W),
    (92, "", H),
    (97, "", D),
    (107, "", D),            # 話題の切れ目
    (130, "", D),
    (146, "", D),
    (166, "", D),
    (180, "", D),
    (187, "", D),
    (198, "", D),
    (208, "", D),
    (217, "", D),
    (228, "", D),
    (259, "", D),
    (276, "", D),
    (283, "", D),
    (305, "", D),
    (312, "", D),
    (321, "", D),
    (327, "", W),
    (335, "", W),
    (345, "", W),
    (364, "", W),
    (375, "", W),
    (386, "", W),
    (404, "", W),
    (414, "Yeah.", D),
    (415, "", D),
    (423, "", D),
    (434, "", J),
    (436, "", J),
    (454, "", W),
    (458, "", W),
    (476, "", W),
    (485, "", W),
    (496, "", W),
    (506, "", W),
    (524, "", W),
    (536, "", W),
    (553, "", W),
    (565, "", W),
    (575, "", W),
    (578, "", D),
    (591, "", D),
    (599, "", H),
    (606, "", H),
    (615, "", J),
    (626, "", J),
    (635, "", J),
    (655, "", J),
    (669, "", J),
    (677, "", J),
    (700, "", J),
    (716, "", J),
    (726, "", J),
    (733, "", H),
    (738, "", D),
    (751, "", D),
    (764, "", J),
    (773, "", J),
    (782, "", H),
    (790, "", D),
    (791, "", H),
    (798, "", D),
    (810, "", D),
    (823, "", H),
    (824, "", W),
    (834, "", H),
    (843, "", D),
    (860, "I mean, Harry, what do you think?", D),
    (861, "", H),
    (862, "", W),
    (864, "", H),
    (865, "", W),
    (866, "Uh, sorry, sorry.", H),
    (868, "", W),
    (869, "", H),
    (870, "", W),
    (871, "", D),
    (872, "", H),
    (877, "", D),
    (883, "", D),
    (890, "", H),
    (895, "", D),
    (907, "", H),
    (915, "", J),
    (921, "", J),
    (930, "", H),
    (937, "", D),
]

SECS = {
    33: ("自己紹介 — 投資チームの経歴",
         "Introductions — the investment team's background"),
    97: ("2 つのブック — 即時に出せる側と、7 日待つ側",
         "The two books — instant exit, and the seven-day side"),
    198: ("3 つのスリーブ",
          "The three sleeves"),
    228: ("プライベートクレジットをどこから取ってくるか",
          "Where the private credit comes from"),
    283: ("デューデリジェンスと組成",
          "Due diligence and structuring"),
    327: ("バーベル構造 — なぜ真ん中を持たないのか",
          "The barbell — why nothing sits in the middle"),
    364: ("償還が来たときの順序",
          "The order of defence under redemptions"),
    415: ("「規模が大きくなるほど楽になる」",
          "“It all gets easier as you get bigger”"),
    454: ("ストレステスト — 48 本の実データ",
          "Stress testing — 48 empirical runs"),
    578: ("過剰担保",
          "Over-collateralisation"),
    599: ("Q&A — どこまで大きくするのか",
          "Q&A — how big does this get?"),
    733: ("Q&A — その日の流動性を超える償還が来たら",
          "Q&A — redemptions larger than the day's liquidity"),
    782: ("Q&A — ひとことで言う差別化要因",
          "Q&A — the differentiator in one line"),
    834: ("Q&A — コミュニティにできること",
          "Q&A — what the community can do"),
    907: ("最後に — mainnet の日付と、初めての大口 mint",
          "Closing — a mainnet date, and the first large mint"),
}


def blocks():
    out = []
    for chunk in re.split(r"\n\s*\n", SRT.read_text().strip()):
        lines = [l for l in chunk.split("\n") if l.strip()]
        if len(lines) < 3:
            continue
        text = re.sub(r"\s+", " ", " ".join(lines[2:])).strip()
        out.append({"no": int(lines[0]), "t": lines[1].split(" --> ")[0][:8], "text": text})
    return out


def build():
    cuts = {}
    for no, mark, who in CUTS:
        cuts.setdefault(no, []).append((mark, who))

    turns = []
    cur = {"who": CUTS[0][2], "t": None, "parts": []}

    def flush():
        if cur["parts"]:
            turns.append({"who": cur["who"], "t": cur["t"],
                          "en": " ".join(cur["parts"]).strip()})
        cur["parts"] = []

    for b in blocks():
        if b["no"] in SECS:
            flush()
            turns.append({"sec": SECS[b["no"]]})
            cur["t"] = None
        pieces = [(b["text"], None)]
        for mark, who in cuts.get(b["no"], []):
            head = pieces[-1][0]
            idx = head.find(mark) if mark else 0
            assert idx >= 0, (b["no"], mark)
            pieces[-1] = (head[:idx], pieces[-1][1])
            pieces.append((head[idx:], who))
        for text, who in pieces:
            text = text.strip()
            if who:
                flush()
                cur["who"] = who
                cur["t"] = None
            if text:
                if cur["t"] is None:
                    cur["t"] = b["t"]
                cur["parts"].append(text)
    flush()
    return turns


if __name__ == "__main__":
    print(json.dumps(build(), ensure_ascii=False, indent=1))
