#!/usr/bin/env python3
"""2026-09-21 Ambassador Program 回の原本を .turn に割る。

原本には話者ラベルも時刻もない。段落（空行区切り）が 245 あり、
1 段落の中で話者が入れ替わる箇所も多い。
CUTS … (段落番号, その段落内で新しいターンが始まる文字列, 話者)
       話者が None なら同じ話者の話題の切れ目。文字列が "" なら段落の先頭。
       文字列が "~" で始まれば、段落内の最後の出現位置を使う。
SECS … .sec（話題の見出し）を差し込む段落番号 → (日本語, 英語)
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "episodes/2026-09-21-office-hours-ambassador/transcript.txt"

H, A = "host", "a"

CUTS = [
    (0, "", H),
    (4, "Yeah. Can you hear me?", A), (4, "Yeah, can hear you.", H),
    (5, "", A),
    (6, "I'm good.", H),
    (7, "", H), (7, "Yeah, absolutely. Is it", A),
    (8, "Yes. Prematurely grayed.", H),
    (10, "", A),
    (15, "", H), (17, "", None), (21, "", None),
    (23, "Yeah, it's the 1st of October", A), (23, "~Yeah ... about nine", H),
    (24, "", None), (27, "", None), (28, "", None),
    (29, "", A),
    (32, "", H), (35, "", None), (37, "", None),
    (38, "", A), (38, "I'm just thinking of all the tabs.", H),
    (39, "", A), (39, "Oh, I see.", H),
    (40, "", None), (45, "", None), (49, "", None), (51, "", None), (55, "", None), (58, "", None), (61, "", None),
    (63, "No, that was,", A), (63, "Okay. Was it the Benz?", H), (63, "It's on silent.", A), (63, "Right.", H),
    (64, "", None), (68, "", None), (73, "", None),
    (76, "To, to, to add what there", A),
    (78, "", H), (82, "", None), (83, "", None),
    (86, "", A),
    (87, "", H), (91, "", None), (96, "", None), (100, "", None),
    (103, "", A),
    (106, "", H),
    (109, "Yeah But it's really based", A), (110, "", None),
    (115, "That's a good point.", H),
    (116, "", None), (120, "", None), (123, "", None),
    (128, "", None), (128, "I, I, I think it's, uh, I'd be good", A), (128, "Oh, sorry.", H),
    (129, "", A), (129, "Yeah. So the clear call to action", H),
    (130, "", None), (132, "", None), (136, "", None), (143, "", None), (148, "", None), (153, "", None),
    (156, "", None), (156, "Yeah. I, I'll tell you about them.", A), (156, "Yes, good.", H),
    (157, "", A), (162, "", None), (166, "", None), (171, "", None), (175, "", None),
    (178, "", H),
    (179, "Yeah, I mean, I can do", A),
    (181, "So let me, let me pin that back at you", H), (181, "... but more info will come out", A),
    (182, "", H), (182, "Well, no. That sounds- No, yeah.", A),
    (185, "Custom-made swag, guys.", H),
    (186, "", None),
    (187, "Yeah. And to be fair", A),
    (189, "Oh, that's cool.", H),
    (190, "", A),
    (192, "[Participant F] says", H),
    (194, "Yeah ... when we talk about Discord roles", A),
    (196, "", H),
    (200, "If it's coming, if it's coming out on your accounts", A),
    (204, "", H), (208, "", None),
    (209, "", A),
    (215, "", H), (218, "", None), (223, "", None),
    (227, "I think that's probably it for now", A),
    (229, "Oh, tell us about that", H),
    (230, "", None), (230, "Yeah. So the community", A),
    (236, "", H), (239, "", None),
    (241, "", None), (241, "Um, so in, invite your friends", A), (241, "Excellent. We're at 1,200 now.", H),
    (242, "", A), (242, "Yeah, we need some tweets.", H), (242, "Tweets. Yeah, we're at 1,220.", A), (242, "Fine. Brilliant.", H),
    (243, "", None),
]

SECS = {
    0: ("冒頭", "Opening"),
    8: ("ここまでの経緯 — SPO のプログラムからアンバサダーへ", "Where we've been — from the SPO programme to ambassadors"),
    15: ("本物の活動と、コミュニティからの提案", "Authentic activity, and what the community has suggested"),
    22: ("mainnet の延期と「握手」", "The mainnet delay, and the handshake"),
    27: ("Decentralized Adventures", "Decentralized Adventures"),
    35: ("ワークショップの画面共有", "Sharing the workshop board"),
    51: ("ダーク・フォレスト", "The dark forest"),
    55: ("共通善 — 4 つの論拠", "The common good — four arguments"),
    68: ("テンプレートと、mainnet までのサンドボックス", "Templates, and the sandbox until mainnet"),
    83: ("チャットの質問 — Lace の報酬タスク", "Question from chat — the Lace rewards task"),
    87: ("ここまでのまとめと、招待", "Recap, and the invitation"),
    103: ("コミュニティは作る人のもの", "The community is what you make it"),
    116: ("貢献をどう見るか — SPO と紹介リンク", "How contributions are seen — SPOs and referral links"),
    128: ("行動の呼びかけ — testnet の活動を増やす", "The call to action — more testnet activity"),
    136: ("A/B テストという論法", "The A/B-test argument"),
    156: ("イベント", "Events"),
    178: ("グッズ", "Swag"),
    187: ("EVM の時期のヒント", "A hint about EVM timing"),
    192: ("限定グッズと OG ステータス", "Limited-edition swag and OG status"),
    196: ("質問 — コミュニティ発のコンテンツは審査が要るか", "Question — does community content need review?"),
    208: ("2027 年のイベント", "Events in 2027"),
    215: ("チームは Discord にいる", "The team is in Discord"),
    218: ("まとめ", "Recap"),
    227: ("USDrf への改称の反映", "Rolling out the USDrf rename"),
    236: ("締め", "Closing"),
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
