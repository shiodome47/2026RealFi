#!/usr/bin/env python3
"""2026-11-06 Money Flows & DeFi Strategies 回の全文ページ 2 枚を生成する。"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _mf_turns import build          # noqa: E402
from _mf_ja import JA, INFERRED      # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/2026-11-06-office-hours-money-flows"
OUT.mkdir(parents=True, exist_ok=True)

HEAD = (ROOT / "docs/2026-08-28-office-hours-investment-framework/transcript-ja.html") \
    .read_text().split('<p class="eyebrow">')[0]

NAME = {"host": ("Ben", "Ben"), "liam": ("Liam", "Liam"), "k": ("参加者K", "Participant K")}
CLS = {"host": " host", "liam": "", "k": ""}

NOTE_JA = """<div class="note">
<p><strong>このページについて。</strong>発話した 2 名（進行役の <code>Ben</code> とデータ責任者の <code>Liam</code>）は<strong>実名のまま</strong>です。チャットで名前が挙がった方、呼びかけられた方、終盤にステージに上がった方は <code>参加者A〜N</code>（登場順）、社内で名前が挙がった人物は <code>[a colleague]</code> に置き換えています。#10 に登壇した Head of Product への言及は、その回と同じく実名のままです。</p>
<p>原本には<strong>話者ラベルも時刻もありません</strong>。段落は空行で区切られていますが、それは話者の区切りではなく、1 段落の中で話者が入れ替わる箇所も多くあります。<strong>話者は文脈から割り当て</strong>、冒頭の接続トラブルの掛け合いなど確度の低い箇所には <em>(推定)</em> を付けています。</p>
<p><strong>固有名詞の誤変換は依頼者が確認したうえで、残っていた 2 か所（進行役が相手を呼び間違えたように聞こえる箇所と、組織名）をこちらで直してあります</strong>。それ以外の文言は語られたとおりです。<strong>スライド（12 枚）が画面共有されました。</strong>全文ページには音声で語られたことだけがあり、スライドの中身はまとめページでこちらが描き直した図としてだけ載せています。</p>
</div>"""

NOTE_EN = """<div class="note">
<p><strong>About this page.</strong> The two people who spoke — <code>Ben</code>, the host, and <code>Liam</code>, who leads the data function — <strong>are named</strong>. People named in the chat, addressed by name, or who came up on stage near the end appear as <code>Participant A–N</code> in order of appearance; colleagues mentioned by name appear as <code>[a colleague]</code>. The Head of Product who spoke in #10 is referred to by name, as on that page.</p>
<p>The source has <strong>neither speaker labels nor timestamps</strong>. Its paragraphs are separated by blank lines, but those are not speaker breaks — the speaker often changes mid-paragraph. <strong>Speakers are assigned from context</strong>, and short exchanges where the attribution is less certain, such as the connection trouble at the start, are marked <em>(inferred)</em>.</p>
<p><strong>Proper nouns were checked by the requester; two remaining mis-hearings (a name the host appears to get wrong once, and an organisation name) were corrected here.</strong> Apart from that and the anonymisation, the wording is unchanged. <strong>A 12-slide deck was screen-shared.</strong> This page contains only what was said aloud; the slides’ content appears on the summary page only as figures redrawn by us.</p>
</div>"""


def page(lang, body):
    ja = lang == "ja"
    head = HEAD.replace('<title>RealFi Office Hours #8 — 日本語全文</title>',
                        '<title>RealFi Office Hours #11 — %s</title>'
                        % ("日本語全文" if ja else "Full transcript (English)"))
    assert "#11" in head, "title の差し替えに失敗"
    if not ja:
        head = head.replace('<html lang="ja">', '<html lang="en">')
        head = head.replace('<div class="wrap lang-ja">', '<div class="wrap lang-en">')
        head = head.replace(
            '<a class="lang-toggle" href="./transcript-en.html" '
            'aria-label="Read the English original" title="Read the English original">EN</a>',
            '<a class="lang-toggle" href="./transcript-ja.html" '
            'aria-label="日本語訳を読む" title="日本語訳を読む">日本語</a>')
        head = head.replace('aria-label="配色を切り替える" title="配色を切り替える"',
                            'aria-label="Toggle colour scheme" title="Toggle colour scheme"')

    meta = ('<p class="eyebrow">RealFi Office Hours #11</p>\n<h1>%s</h1>\n'
            '<p class="meta">\n  <span>2026-11-06</span>\n'
            '  <span>Discord</span>\n  <span>Money Flows &amp; DeFi Strategies</span>\n</p>'
            % ("日本語全文" if ja else "Full transcript (English original)"))

    if ja:
        nav = """<nav class="docnav">
  <span class="docnav-label">英語の原文を訳したもの。固有名詞の誤変換は直してある。</span>
  <a href="./">まとめ</a>
  <a href="./transcript-ja.html" aria-current="page">日本語全文</a>
  <a href="./transcript-en.html">英語全文（原文）</a>
  <a href="../">← 全セッション</a>
</nav>"""
    else:
        nav = """<nav class="docnav">
  <span class="docnav-label">The original English, unedited apart from the anonymisation and the corrected proper nouns noted above.</span>
  <a href="./">Summary</a>
  <a href="./transcript-ja.html">Full transcript (Japanese)</a>
  <a href="./transcript-en.html" aria-current="page">Full transcript (English original)</a>
  <a href="../">← All sessions</a>
</nav>"""

    foot = "\n<footer>\n  <p>RealFi Office Hours archive</p>\n</footer>\n\n</div>\n</body>\n</html>\n"
    return "%s%s\n\n%s\n\n<!--content-->\n\n%s\n<!--/content-->\n\n%s\n%s" % (
        head, meta, NOTE_JA if ja else NOTE_EN, body, nav, foot)


def render(lang):
    ja = lang == "ja"
    turns, secs = build()
    out = []
    for i, t in enumerate(turns):
        if i in secs:
            out.append('<div class="sec">%s</div>' % html.escape(secs[i][0 if ja else 1]))
        if ja:
            text = JA.get(i)
            if text is None:
                raise SystemExit("turn %d の日本語がない: %s" % (i, t["paras"][0][:70]))
            paras = text.split("\n\n")
        else:
            paras = [html.escape(p, quote=False) for p in t["paras"]]
        mark = ' <em>(%s)</em>' % ("推定" if ja else "inferred") if i in INFERRED else ""
        body = "\n  ".join("<p>%s</p>" % p for p in paras)
        out.append(
            '<div class="turn">\n'
            '  <div class="turn-who%s">%s%s</div>\n'
            '  <div class="turn-body">%s</div>\n'
            '</div>' % (CLS[t["who"]], NAME[t["who"]][0 if ja else 1], mark, body))
    return "\n\n".join(out)


for lang, fn in (("ja", "transcript-ja.html"), ("en", "transcript-en.html")):
    (OUT / fn).write_text(page(lang, render(lang)))
    print("%s — ok" % fn)
