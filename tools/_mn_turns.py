#!/usr/bin/env python3
"""2026-10-09 Mainnet & what comes next 回の原本を .turn に割る。

原本には話者ラベルも時刻もない。段落（空行区切り）が 204 あり、
1 段落の中で話者が入れ替わる箇所も多い。
CUTS … (段落番号, その段落内で新しいターンが始まる文字列, 話者)
       話者が None なら同じ話者の話題の切れ目。文字列が "" なら段落の先頭。
       文字列が "~" で始まれば、段落内の最後の出現位置を使う。
SECS … .sec（話題の見出し）を差し込む段落番号 → (日本語, 英語)
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "episodes/2026-10-09-office-hours-mainnet/transcript.txt"

H, C, F = "host", "clay", "f"

CUTS = [
    (0, "", H), (0, "Good to be back. Hello.", C), (0, "Okay, let's get Clay up here.", H), (0, "Hey, Ben. Ah.", C),
    (1, "Oh, it's so good to have you back, Clay.", H), (1, "Good to be back.", C), (1, "So let's do a little bit", H),
    (4, "That's right.", C), (4, "God, it's exciting.", H),
    (6, "", None), (9, "", None),
    (10, "~Yeah.", C),
    (11, "", C),
    (15, "That- that's right.", H),
    (18, "", None),
    (19, "Well, I, I could talk", C),
    (20, "", None), (26, "", None),
    (31, "", H),
    (33, "", C), (38, "", None), (44, "", None),
    (49, "Well, I was literally", H),
    (50, "Yeah. So the way that it works", C),
    (62, "It did make sense", H),
    (64, "Um, yeah, I guess it's", C), (70, "", None),
    (76, "", H),
    (77, "Yeah. So folks would open", C),
    (87, "", H),
    (88, "Um, the, the challenge", C), (92, "", None),
    (99, "Just, just call, call out", H),
    (101, "If you're long, if you're long on ADA", C),
    (103, "", H),
    (105, "Yeah. Uh, the transparency portal", C),
    (112, "Great. So you...", H),
    (114, "Uh, that's, that's a good question.", C), (120, "", None),
    (124, "Okay, that makes sense.", H),
    (127, "Yeah. So we are finalizing", C), (133, "", None),
    (136, "", H),
    (137, "I don't know either.", C), (137, "~I don't know either.", H), (137, "Uh, we should talk-", C),
    (138, "", H), (140, "", None), (142, "", None),
    (144, "", C), (150, "", None),
    (154, "", H), (160, "", None),
    (167, "I, I, I mean, I, I mean for...", C),
    (173, "Yeah. If, if you haven't", H),
    (174, "Yeah ... yeah. Yeah. We, you know", C),
    (178, "", H),
    (179, "Yeah, R-Points and RFG", C), (179, "Nice. Um, and", H),
    (181, "No, it's, it's easy.", C), (181, "Yeah, come up and talk", H),
    (182, "~Yeah.", C),
    (184, "", H),
    (186, "", C), (186, "Any questions, uh, Clay", H),
    (187, "Hi, you guys hear me", F), (187, "Yep. Yes. Hey,", H), (187, "Wonderful.", F),
    (190, "Hmm. Um, we should", C), (190, "Yeah. Well, [Participant F]", H),
    (192, "", C),
    (193, "Yeah, yeah. W-", H),
    (195, "", F), (195, "Oh, you're welcome.", H),
    (196, "Well, for me, I think this is great.", F), (196, "Awesome.", H),
    (197, "", None),
    (198, "Yeah. The [person in the GIF].", C), (198, "So look,", H),
    (201, "~You're doing great.", C),
    (202, "", H),
    (203, "Thanks a lot.", C), (203, "And we'll see you next time.", H), (203, "~Bye bye bye", C),
]

SECS = {
    0: ("冒頭", "Opening"),
    11: ("最初の利回り分配", "The first yield distributions"),
    18: ("testnet の振り返りとバグ報奨", "Looking back at testnet, and the bug bounty"),
    26: ("mainnet のローンチ", "The mainnet launch"),
    33: ("いま mainnet で動いているもの", "What is live on mainnet"),
    38: ("USDrf と sUSDrf のおさらい", "USDrf and sUSDrf, recapped"),
    44: ("Liqwid との統合と、ローンチ直後の裁定", "Liqwid, and the arbitrage right after launch"),
    50: ("ループの仕組み", "How looping works"),
    62: ("ピラミッディングとの違い、ADA でのループ", "Pyramiding versus looping, and looping with ADA"),
    76: ("ローンチ時の裁定の手順", "The arbitrage at launch, step by step"),
    87: ("ADA 建てのプロダクトはあるか", "Will there be an ADA-based product?"),
    104: ("透明性ポータル", "The transparency portal"),
    113: ("利回りは変わるのか — スリーブとステーキング比率", "Does the yield vary? Sleeves and the staking ratio"),
    125: ("testnet のポイントと pioneer season", "Testnet points and the pioneer season"),
    136: ("対応地域の一覧", "The list of supported regions"),
    142: ("この先 — EVM と TGE", "Looking ahead: EVM and TGE"),
    154: ("Cardano ではなく RealFi の話として Ethereum へ", "Taking RealFi, not Cardano, to Ethereum"),
    173: ("R-Points のおさらい", "R-Points, recapped"),
    178: ("Q&A — MiCA 圏、利回りと R-Points", "Q&A: MiCA regions, yield and R-Points"),
    187: ("ステージからの質問 — 複数法人の構成", "A question from the stage: the multi-entity structure"),
    197: ("締め", "Closing"),
}

def paragraphs():
    text = SRC.read_text(encoding="utf-8").split("\n\n", 1)[1]   # 先頭のメモを落とす
    return [p.strip() for p in text.split("\n\n") if p.strip()]


def build():
    """[{"who", "paras": [...]}, ...] と、SECS を差し込む位置（turn 番号）を返す。"""
    paras = paragraphs()
    cuts = {}
    for idx, marker, who in CUTS:
        cuts.setdefault(idx, []).append((marker, who))
    turns, secs_at = [], {}
    cur = None
    for i, p in enumerate(paras):
        if i in SECS:
            secs_at[len(turns)] = SECS[i]
        pieces = [(0, None)]
        for marker, who in cuts.get(i, []):
            if marker == "":
                pos = 0
            elif marker.startswith("~"):
                pos = p.rfind(marker[1:])
            else:
                pos = p.find(marker)
            assert pos >= 0, (i, marker)
            pieces.append((pos, who))
        pieces.sort(key=lambda x: x[0])
        # 同じ位置に (0, None) と (0, who) があれば who を優先
        merged = []
        for pos, who in pieces:
            if merged and merged[-1][0] == pos:
                merged[-1] = (pos, who if who is not None else merged[-1][1])
                if who is None and merged[-1][1] is None:
                    merged[-1] = (pos, "SAME")
            else:
                merged.append((pos, who))
        for k, (pos, who) in enumerate(merged):
            end = merged[k + 1][0] if k + 1 < len(merged) else len(p)
            seg = p[pos:end].strip()
            if not seg:
                continue
            starts_new = (k > 0) or (i in cuts and merged[0][0] == 0 and merged[0][1] is not None) or cur is None
            if k == 0 and i in cuts and merged[0][0] == 0 and merged[0][1] == "SAME":
                starts_new = True
                who = None
            if starts_new:
                new_who = cur["who"] if (who is None or who == "SAME") and cur else who
                if new_who is None:
                    new_who = H
                cur = {"who": new_who, "paras": [seg]}
                turns.append(cur)
            else:
                cur["paras"].append(seg)
    return turns, secs_at


if __name__ == "__main__":
    turns, secs = build()
    print(len(turns), "turns", len(secs), "secs")
    for n, t in enumerate(turns):
        if n in secs:
            print("  ---", secs[n][0])
        print("%3d %-4s %s" % (n, t["who"], " // ".join(x[:70] for x in t["paras"])))
