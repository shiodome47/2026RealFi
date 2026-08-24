#!/usr/bin/env python3
"""2026-08-24 Ticker 回の全文ページ 2 枚を生成する。"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _ticker_turns import build          # noqa: E402
from _ticker_ja import JA                # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/2026-08-24-office-hours-ticker"
OUT.mkdir(parents=True, exist_ok=True)

TPL = (ROOT / "docs/2026-08-14-ask-the-ceo/transcript-ja.html").read_text()
HEAD = TPL.split("<p class=\"eyebrow\">")[0]

NAME = {"host": "Ben", "marketing": "Rob"}
CLS = {"host": " host", "marketing": ""}


def page(lang, body):
    ja = lang == "ja"
    head = HEAD.replace('<title>RealFi Office Hours #6 — 日本語全文</title>',
                        '<title>RealFi Office Hours #7 — %s</title>'
                        % ("日本語全文" if ja else "Full transcript (English)"))
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

    if ja:
        note = """<div class="note">
<p><strong>このページについて。</strong>聴衆として名前が挙がった方は <code>参加者A〜J</code> に置き換えています。社内・他社で名前が挙がった方も役割に置き換えました。<strong>このコールで発話したのは 2 名だけ</strong>です。</p>
<p>原本は SRT なので<strong>タイムスタンプはありますが話者ラベルがありません</strong>。しかも 1 つの字幕ブロックの中で話者が入れ替わることがあります。分割は文脈から判断していますが、<strong>声が 2 つしかないため全編を通して明確</strong>で、<em>(推定)</em> は 1 つも付けていません。文言は上記の匿名化以外は原文のままです。</p>
<p>スライドはありません。コール中にチャットへ画像と Miro のリンクが貼られていますが、リンク先はここでは扱いません。</p>
</div>"""
        nav = """<nav class="docnav">
  <span class="docnav-label">英語の原文を訳したもの。誤変換は用語集にしたがって直してある。</span>
  <a href="./">まとめ</a>
  <a href="./transcript-ja.html" aria-current="page">日本語全文</a>
  <a href="./transcript-en.html">英語全文（原文）</a>
  <a href="../">← 全セッション</a>
</nav>"""
        meta = """<p class="eyebrow">RealFi Office Hours #7</p>
<h1>日本語全文</h1>
<p class="meta">
  <span>2026-08-24</span>
  <span>51:35</span>
  <span>Discord</span>
  <span>Ticker</span>
</p>"""
    else:
        note = """<div class="note">
<p><strong>About this page.</strong> People named in the audience appear as <code>Participant A–J</code>; colleagues and people at other companies are described by role. <strong>Only two people spoke on this call.</strong></p>
<p>The source is an SRT: <strong>timestamps but no speaker labels</strong>, and a single subtitle block sometimes spans a change of speaker. The split into turns is judged from context; with only two voices it is unambiguous throughout, so nothing is marked <em>(inferred)</em>. <strong>Apart from the anonymisation above, the wording is unchanged</strong> — mistranscriptions included.</p>
<p>There were no slides. Images and a Miro link were posted in chat during the call; their contents are not covered here.</p>
</div>"""
        nav = """<nav class="docnav">
  <span class="docnav-label">The original English, unedited apart from the anonymisation noted above.</span>
  <a href="./">Summary</a>
  <a href="./transcript-ja.html">Full transcript (Japanese)</a>
  <a href="./transcript-en.html" aria-current="page">Full transcript (English original)</a>
  <a href="../">← All sessions</a>
</nav>"""
        meta = """<p class="eyebrow">RealFi Office Hours #7</p>
<h1>Full transcript (English original)</h1>
<p class="meta">
  <span>2026-08-24</span>
  <span>51:35</span>
  <span>Discord</span>
  <span>Ticker</span>
</p>"""

    foot = """
<footer>
  <p>RealFi Office Hours archive</p>
</footer>

</div>
</body>
</html>
"""
    return "%s%s\n\n%s\n\n<!--content-->\n\n%s\n<!--/content-->\n\n%s\n%s" % (
        head, meta, note, body, nav, foot)


def render_indexed(lang):
    """turn の通し番号は build() の出力インデックス（sec も数える）に合わせる。"""
    ja = lang == "ja"
    out = []
    for i, t in enumerate(build()):
        if "sec" in t:
            out.append('<div class="sec">%s</div>' % html.escape(t["sec"][0 if ja else 1]))
            continue
        if ja:
            text = JA.get(i)
            if text is None:
                raise SystemExit("turn %d の日本語がない: %s" % (i, t["en"][:70]))
        else:
            text = html.escape(t["en"], quote=False)
        out.append(
            '<div class="turn">\n'
            '  <div class="turn-who%s">%s<span class="turn-time">%s</span></div>\n'
            '  <div class="turn-body"><p>%s</p></div>\n'
            '</div>' % (CLS[t["who"]], NAME[t["who"]], t["t"], text))
    return "\n\n".join(out)


for lang, fn in (("ja", "transcript-ja.html"), ("en", "transcript-en.html")):
    (OUT / fn).write_text(page(lang, render_indexed(lang)))
    print("%s — ok" % fn)
