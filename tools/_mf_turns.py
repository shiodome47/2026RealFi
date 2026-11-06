#!/usr/bin/env python3
"""2026-11-06 Money Flows & DeFi Strategies 回の原本を .turn に割る。

原本には話者ラベルも時刻もない。段落（空行区切り）が 268 あり、
1 段落の中で話者が入れ替わる箇所も多い。
CUTS … (段落番号, その段落内で新しいターンが始まる文字列, 話者)
       話者が None なら同じ話者の話題の切れ目。文字列が "" なら段落の先頭。
       文字列が "~" で始まれば、段落内の最後の出現位置を使う。
SECS … .sec（話題の見出し）を差し込む段落番号 → (日本語, 英語)
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "episodes/2026-11-06-office-hours-money-flows/transcript.txt"

H, L, K = "host", "liam", "k"

CUTS = [
    (0, "", H), (3, "", None), (10, "", None), (13, "", None), (18, "", None),
    (23, "", L), (23, "Ah, great.", H), (23, "Oh yeah, loud and clear.", L),
    (24, "", L), (24, "We're good.", H),
    (25, "", H), (25, "Thanks.", L),
    (26, "", L), (26, "Um, so walk us through", H),
    (27, "Sure.", L),
    (31, "", H), (32, "Sure.", L),
    (36, "Okay, that's great.", H),
    (37, "Yeah. I've, I've got a deck", L),
    (38, "Fantastic.", H),
    (40, "Yeah. All got it", L), (40, "Okay, awesome.", H),
    (41, "", L), (41, "Uh, still loading for me.", H),
    (42, "", L),
    (43, "Uh, can you ...", H),
    (44, "Yeah, let me do that.", L), (44, "There we go.", H),
    (46, "", None),
    (47, "", L),
    (48, "", H),
    (49, "", H), (49, "Hmm. Restream.", L), (49, "Yeah. I can just-", H),
    (50, "", H), (50, "Okay, Ben, I'm sharing", L), (50, "Thank you.", H),
    (51, "", L), (51, "It's, it's the modern", H),
    (53, "I'm gonna stop sharing mine.", L), (53, "Yeah. Yeah, stop sharing yours", H),
    (54, "Not yet. Yes.", L),
    (56, "Oh, yeah. I'm just gonna click", H), (56, "~Okay.", L),
    (57, "", L), (59, "", None), (64, "", None), (67, "", None),
    (70, "Is this slide six", H), (70, "Yeah, great.", L),
    (71, "You got it.", H), (71, "~Yeah.", L),
    (72, "", None),
    (77, "Let me check.", H),
    (78, "It is.", L),
    (81, "~Cool.", H),
    (82, "", H), (82, "So, so, so [Participant I]", L),
    (86, "", None),
    (88, "Um, who- Yeah, sure", H),
    (89, "", L),
    (93, "Yes.", H), (93, "~Okay.", L),
    (99, "That makes sense.", H),
    (100, "", L),
    (101, "", H),
    (104, "Okay. Yeah.", L), (107, "", None), (113, "", None),
    (119, "That was great.", H), (119, "You're welcome.", L),
    (120, "", None),
    (125, "And are, are we allowed", H), (125, "I mean, maybe check", L),
    (126, "Awesome.", H),
    (127, "", L), (133, "", None), (141, "", None),
    (145, "", H),
    (147, "", L),
    (151, "", H),
    (153, "Wait, let me, let me try", L),
    (154, "", H),
    (156, "So, so, so, so this", L),
    (158, "Okay. So then", H), (161, "", None),
    (165, "Yeah. Um, and look,", L),
    (171, "", H), (177, "", None),
    (179, "Well, I've, I've, I've-", L),
    (184, "", H),
    (189, "well look, I mean", L),
    (193, "", H),
    (196, "I don't know if I'd be comfortable", L),
    (198, "and I'm being unfair to Liam", H),
    (202, "And, and, and stablecoin supply", L),
    (203, "Mm. Uh, so a question about", H),
    (209, "", L), (209, "Yeah, please.", H),
    (210, "", L),
    (212, "Okay. Cool.", H),
    (215, "I've got time.", L), (215, "[Participant K], legend.", H), (215, "Hey, guys.", K), (215, "Yes, sir.", H), (215, "Okay. Okay. Uh, first off", K),
    (220, "", None),
    (226, "~Sure.", L),
    (231, "I immediately thought", K),
    (240, "You're welcome.", L), (240, "Welcome to the age of DeFi", H),
    (241, "Big time, man.", K), (241, "Um, I, I might follow up", H),
    (244, "", None),
    (246, "Absolutely, man.", K),
    (254, "", H), (260, "", None),
    (265, "That works.", K), (265, "~Yeah.", H),
    (267, "Cool.", L), (267, "Thanks, [Participant K].", H), (267, "Thanks, guys.", K), (267, "Thanks, everyone.", H),
]

SECS = {
    0: ("冒頭 — マイクのトラブル", "Opening: mic trouble"),
    25: ("自己紹介 — データ機能の役割", "Introductions: what the data function does"),
    33: ("今日のテーマ", "Today's topic"),
    40: ("画面共有のトラブル", "Screen-share trouble"),
    57: ("前提 — すべてオンチェーンのデータ", "Ground rules: all on-chain data"),
    59: ("小口の需要と TVL は同じではない", "Retail demand and TVL are not the same thing"),
    72: ("市場メーカーが需要を mint に変える仕組み", "How the market maker turns demand into a mint"),
    77: ("Q: Strike は需要を生むのか", "Q: does Strike create demand?"),
    82: ("Part 2 — 人々は USDrf で何をしているか", "Part 2: what people do with USDrf"),
    88: ("Q: 市場メーカーは誰か", "Q: who is the market maker?"),
    93: ("小口の USDrf はどこに置かれているか", "Where retail USDrf sits"),
    101: ("供給側 — Liqwid の利用率と「キンク」", "The supply side: Liqwid utilisation and the kink"),
    120: ("10 の戦略", "The ten strategies"),
    145: ("Q: 45% APR、USDCx の行き先", "Q: 45% APR, and where the USDCx goes"),
    161: ("USDM について", "On USDM"),
    164: ("まとめ", "Wrap-up"),
    171: ("教育キャンペーンと「リターン」", "An education campaign, and “the returns”"),
    204: ("R-Points の請求時期", "When R-Points can be claimed"),
    209: ("R-Points が行動を変える、という声", "A comment: R-Points shape behaviour"),
    215: ("ステージから — USDM、借入金利、補助", "From the stage: USDM, borrow rates, subsidies"),
    242: ("締め", "Closing"),
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
