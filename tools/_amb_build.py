#!/usr/bin/env python3
"""2026-09-21 Ambassador Program 回の全文ページ 2 枚を生成する。"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _amb_turns import build          # noqa: E402
from _amb_ja import JA, INFERRED      # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/2026-09-21-office-hours-ambassador"
OUT.mkdir(parents=True, exist_ok=True)

HEAD = (ROOT / "docs/2026-08-28-office-hours-investment-framework/transcript-ja.html") \
    .read_text().split('<p class="eyebrow">')[0]

NAME = {"host": ("進行役", "Host"), "a": ("登壇者A", "Speaker A")}
CLS = {"host": " host", "a": ""}

NOTE_JA = """<div class="note">
<p><strong>このページについて。</strong>この回はチャタムハウスルールの対象として扱い、<strong>発言者の氏名は記載していません</strong>。話した 2 名は <code>進行役</code>（コミュニティ担当）と <code>登壇者A</code>（マーケティング責任者）、チャットで質問した方は <code>参加者A〜G</code>（登場順）、社内で名前が挙がった人物は役割（CEO、GTM 担当、同僚）に置き換えています。発言の中の呼びかけも同じように置き換えました。</p>
<p>原本には<strong>話者ラベルも時刻もありません</strong>。段落は空行で区切られていますが、それは話者の区切りではなく、1 段落の中で話者が入れ替わる箇所も多くあります。<strong>話者は文脈から割り当て</strong>、短い掛け合いで確度の低い箇所には <em>(推定)</em> を付けています。文言は匿名化以外は語られたとおりです。</p>
<p><strong>Miro のワークショップボードが画面共有されました。</strong>ボードの中身は受け取っていないので、<strong>ここに載っているのは音声で語られた内容だけ</strong>です。</p>
</div>"""

NOTE_EN = """<div class="note">
<p><strong>About this page.</strong> This session is treated as being under the Chatham House Rule, so <strong>no speaker is named</strong>. The two people who spoke appear as <code>Host</code> (community lead) and <code>Speaker A</code> (marketing lead); people who asked questions in the chat appear as <code>Participant A–G</code> in order of appearance; colleagues mentioned by name appear by role (the CEO, the GTM lead, a colleague). Names used in direct address are replaced the same way, in square brackets.</p>
<p>The source has <strong>neither speaker labels nor timestamps</strong>. Its paragraphs are separated by blank lines, but those are not speaker breaks — the speaker often changes mid-paragraph. <strong>Speakers are assigned from context</strong>, and short exchanges where the attribution is less certain are marked <em>(inferred)</em>. Apart from the anonymisation, the wording is unchanged.</p>
<p><strong>A Miro workshop board was screen-shared.</strong> Its contents were not provided, so <strong>only what was said aloud appears here</strong>.</p>
</div>"""


def page(lang, body):
    ja = lang == "ja"
    head = HEAD.replace('<title>RealFi Office Hours #8 — 日本語全文</title>',
                        '<title>RealFi Office Hours #9 — %s</title>'
                        % ("日本語全文" if ja else "Full transcript (English)"))
    assert "#9" in head, "title の差し替えに失敗"
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

    meta = ('<p class="eyebrow">RealFi Office Hours #9</p>\n<h1>%s</h1>\n'
            '<p class="meta">\n  <span>2026-09-21</span>\n'
            '  <span>Discord</span>\n  <span>Ambassador Program</span>\n</p>'
            % ("日本語全文" if ja else "Full transcript (English original)"))

    if ja:
        nav = """<nav class="docnav">
  <span class="docnav-label">英語の原文を訳したもの。誤変換は用語集にしたがって直してある。</span>
  <a href="./">まとめ</a>
  <a href="./transcript-ja.html" aria-current="page">日本語全文</a>
  <a href="./transcript-en.html">英語全文（原文）</a>
  <a href="../">← 全セッション</a>
</nav>"""
    else:
        nav = """<nav class="docnav">
  <span class="docnav-label">The original English, unedited apart from the anonymisation noted above.</span>
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
