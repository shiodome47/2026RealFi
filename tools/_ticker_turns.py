#!/usr/bin/env python3
"""2026-08-24 Ticker 回の SRT を .turn に割る。

原本には話者ラベルがないので、話者の交代は文脈から判断してここに書き出す。
CUTS  … 話者が入れ替わる位置（ブロック番号, そのブロック内で新しい話者が始まる文字列）
SAME  … 話者は同じだが話題が変わる位置。長い独白を読める長さに割るため
SECS  … .sec（話題の見出し）を差し込む位置
"""
import json
import pathlib
import re

SRT = pathlib.Path(__file__).resolve().parent.parent / \
    "episodes/2026-08-24-office-hours-ticker/transcript.srt"

# 最初の話者。ホスト。
FIRST = "host"

CUTS = [
    (1, "Mm-hmm."), (3, ""), (3, "Yeah, so today is gonna be"),
    (5, "That's great. Yeah, I'm definitely excited"), (8, ""),
    (16, ""), (16, "Yeah, no, that's fine."), (16, "What I'll do, what I'll do"),
    (18, "Yeah."), (29, "Yeah."), (31, "So once we close the vote"),
    (39, "Mm."), (39, "Or you, you'll slap my hand if I do."),
    (40, ""), (40, "Absolutely"), (41, ""), (41, "Absolutely. And I mean"),
    (43, "Mm ..."), (44, ""), (44, "So it's a, it's a great point."),
    (46, ""), (46, "Yeah, walk, walk me through"), (47, ""),
    (61, "I mean- Yeah, let me-"), (103, "Yeah, absolutely. I mean, in essence"),
    (104, ""), (105, ""), (105, "Mm ..."), (106, ""),
    (109, "No, you're, you're, you're scouting"), (110, "'Cause at, at the end of the day"),
    (112, ""), (135, ""), (136, "Yes ..."), (136, "and the, the assets"),
    (145, "Well, I like-- I really like the governance"),
    (149, "Well, we'd love your feedback."), (150, ""),
    (152, "Yeah, absolutely. So I mean, so to--"), (176, ""),
    (179, "Yeah ..."), (179, "if you go on an"), (186, "It's- It's like, it's messages like--"),
    (189, "Yeah. Yeah. Well, it's, this is an"), (203, ""), (204, ""),
    (206, "And we'll send them--"), (206, "Yeah ..."), (207, ""),
    (207, "Actually, good call."), (208, "Sorry ..."),
    (208, "we, we've really gone off on a tangent"),
    (209, "Yeah. Yeah, yeah. So the ticker vote will close"), (215, ""),
    (224, "Yes. That's all right."), (227, "Yeah, good, good question."),
    (250, "Yeah, absolutely. Uh, I mean, it's pretty much everything"), (252, ""),
    (254, "Yeah ..."), (254, "now is the time for questions"),
    (255, "I, I'm, uh, um, it was hilarious"), (259, ""), (259, "Yeah, come do."),
    (259, "So, um, 参加者I, who's in the audience"),
    (282, "Like- Yeah, yeah."), (283, ""), (283, "You were telling me-"), (284, ""),
    (287, "Absolutely, yeah. No, absolutely."), (287, "No ..."), (288, ""),
    (288, "I'm totally, I'm way better."), (289, "Mm-hmm."),
    (289, "Well, since yesterday I feel like a new person."), (291, ""),
    (291, "Yeah. Yeah. Yeah. All right."), (292, "We've got it with investments."),
    (292, "Oof, it's gonna be exciting."), (293, "I, I know some people."),
    (297, "I know some, uh, I know some of the people in, listening on this call"),
    (300, ""), (301, "Are we gonna get some..."), (302, "It's good ..."),
    (302, "we need some swag, don't we?"), (302, "That's why I think we, we've got"),
    (310, "Well, uh, my, my mission now is to get everybody"), (311, ""),
    (312, "Yes ..."), (312, "this, the, the hoodie I did for Pondo"), (316, ""),
    (318, "I- ... see what we can do there ..."), (319, "Mm. Are there any-"),
    (319, "When I go back to Manchester"), (327, "I would need campaigns planned"),
    (343, ""), (343, "Thanks everyone. Bye."), (343, "Bye."),
]

SAME = [
    (25, ""), (50, ""), (56, ""), (67, ""), (73, ""), (76, ""), (82, ""), (85, ""), (91, ""), (94, ""), (101, ""),
    (117, ""), (122, ""), (127, ""), (159, ""), (166, ""), (169, ""), (173, ""),
    (141, ""), (182, ""), (195, ""), (197, ""), (200, ""), (234, ""), (237, ""), (240, ""),
    (217, ""), (220, ""), (247, ""), (263, ""), (267, ""), (272, ""), (278, ""), (331, ""), (334, ""),
    (338, ""),
]

SECS = {
    6: ("ティッカー — もとの名前と、変える理由",
        "The ticker — where it came from, and why it changes"),
    19: ("2 つの案と、投票の状況",
         "The two options, and where the vote stands"),
    30: ("投票のあとに何が起きるか",
         "What happens after the vote"),
    45: ("mainnet の前に何をやるか — アンバサダー制度へ",
         "Before mainnet — towards an ambassador programme"),
    62: ("なぜ crew の立ち上げが止まっていたのか",
         "Why the crews had not launched"),
    76: ("L1 / L2 — 何を数えるか",
         "L1s and L2s — what gets counted"),
    94: ("crew と district",
         "Crews and districts"),
    103: ("「ボーイバンドを作る」というたとえ",
          "The boy-band analogy"),
    112: ("district の具体例",
          "What the districts would be"),
    127: ("dark forest と proof of human",
          "The dark forest, and proof of human"),
    135: ("決めるのはコミュニティ",
          "The community decides"),
    151: ("前職での経験 — 言語コミュニティ",
          "What worked before — language communities"),
    176: ("世界観づくりは何のためか",
          "What the world-building is for"),
    204: ("次にやることと、投票の締切",
          "Next steps, and the deadline"),
    225: ("Q&A — USDA、crew の運営",
          "Q&A — USDA, and how crews would run"),
    250: ("まとめとお礼",
          "Wrapping up"),
    255: ("日本のコミュニティへの調査",
          "The survey going out in Japan"),
    286: ("雑談 — swag と Labubu",
          "Off-topic — swag and Labubu"),
    327: ("最後に — キャンペーンと数値の話に戻る",
          "Back to campaigns and numbers"),
}


def blocks():
    out = []
    for chunk in re.split(r"\n\s*\n", SRT.read_text().strip()):
        lines = [l for l in chunk.split("\n") if l.strip()]
        if len(lines) < 3:
            continue
        no = int(lines[0])
        start = lines[1].split(" --> ")[0][:8]
        text = " ".join(lines[2:])
        text = re.sub(r"\s+", " ", text).strip()
        out.append({"no": no, "t": start, "text": text})
    return out


def build():
    cuts, same = {}, {}
    for i, (no, mark) in enumerate(CUTS):
        cuts.setdefault(no, []).append((mark, i))
    for no, mark in SAME:
        same.setdefault(no, []).append(mark)

    turns = []
    who = FIRST
    cur = {"who": who, "t": None, "parts": []}

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
        for mark, _i in cuts.get(b["no"], []):
            head, tail = pieces[-1][0], None
            if mark == "":
                pieces[-1] = ("", pieces[-1][1])
                pieces.append((head, "flip"))
            else:
                idx = head.find(mark)
                assert idx >= 0, (b["no"], mark)
                pieces[-1] = (head[:idx], pieces[-1][1])
                pieces.append((head[idx:], "flip"))
            assert tail is None
        for mark in same.get(b["no"], []):
            head = pieces[-1][0]
            idx = head.find(mark) if mark else 0
            assert idx >= 0, (b["no"], mark)
            pieces[-1] = (head[:idx], pieces[-1][1])
            pieces.append((head[idx:], "same"))

        for text, kind in pieces:
            text = text.strip()
            if kind:
                flush()
                if kind == "flip":
                    who = "marketing" if who == "host" else "host"
                cur["who"] = who
                cur["t"] = None
            if text:
                if cur["t"] is None:
                    cur["t"] = b["t"]
                cur["parts"].append(text)
    flush()
    return turns


if __name__ == "__main__":
    ts = build()
    print(json.dumps(ts, ensure_ascii=False, indent=1))
