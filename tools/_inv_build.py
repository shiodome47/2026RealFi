#!/usr/bin/env python3
"""2026-08-28 Investment Framework 回の全文ページ 2 枚を生成する。"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _inv_turns import build          # noqa: E402
from _inv_ja import JA, INFERRED      # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/2026-08-28-office-hours-investment-framework"
OUT.mkdir(parents=True, exist_ok=True)

HEAD = (ROOT / "docs/2026-08-24-office-hours-ticker/transcript-ja.html") \
    .read_text().split('<p class="eyebrow">')[0]

NAME = {"host": "Ben", "david": "David", "howie": "Howie", "john": "John"}

# 英語全文は原則として原文のまま。**役職名の聞き取りミスだけ直す。**
# 進行役が同じコールの冒頭で別の人物を CEO として紹介しており、確認も取れている。
EN_FIX = [("I'm the CEO at RealFi", "I'm the CIO at RealFi")]
CLS = {"host": " host", "david": "", "howie": "", "john": ""}

NOTE_JA = """<div class="note">
<p><strong>このページについて。</strong>質問者として名前が読み上げられた方は <code>参加者A・参加者B</code> に置き換えています。<strong>発話した 4 名は実名のまま</strong>です。</p>
<p><strong>進行役の名前は、この回では一度も呼ばれていません。</strong><code>Ben</code> としているのは #6・#7 と同じ進行役だと判断したためで、<strong>この回の音声からの確定ではありません</strong>。</p>
<p><strong>投資チームの 2 人目は、後半で別の名前で呼ばれています。</strong>進行役が別の場で挙げた出席者の並びから <code>Howie</code> が正しいことが確認できたので、日本語版ではそちらに統一しました。<strong>英語版は聞こえたまま</strong>です。</p>
<p>原本は SRT なので<strong>タイムスタンプはありますが話者ラベルがありません</strong>。1 ブロックが 1 文と短く、938 ブロックあります。話者の交代と話題の切れ目で割り直しました。<strong>冒頭の短い挨拶だけは誰の声か判別できない</strong>ため <em>(推定)</em> を付けています。</p>
<p><strong>スライドが使われた回です。</strong>「次のスライド」「付録のラン」といった参照が残っていますが、<strong>ここに載っているのは音声で語られた内容だけ</strong>です。</p>
</div>"""

NOTE_EN = """<div class="note">
<p><strong>About this page.</strong> People whose questions were read out appear as <code>Participant A</code> and <code>Participant B</code>. <strong>The four speakers are named.</strong></p>
<p><strong>The host is never named on this call.</strong> <code>Ben</code> here reflects the judgement that this is the same host as #6 and #7 — <strong>it is not established by the audio of this session</strong>.</p>
<p><strong>The second member of the investment team is addressed by a different name in the second half.</strong> A list of attendees given elsewhere by the host confirms <code>Howie</code> is the correct one; the Japanese page uses it throughout. <strong>The English page keeps what was heard.</strong></p>
<p>The source is an SRT: <strong>timestamps but no speaker labels</strong>, one short sentence per block across 938 blocks. Turns are rebuilt at changes of speaker and topic. <strong>Only the brief greetings at the top cannot be attributed by voice</strong>, and those are marked <em>(inferred)</em>. <strong>Apart from the anonymisation above and one corrected job title, the wording is unchanged</strong> — other mistranscriptions included.</p>
<p><strong>Slides were shown.</strong> References to them survive in the audio, but <strong>only what was spoken aloud appears here</strong>.</p>
</div>"""


def page(lang, body):
    ja = lang == "ja"
    head = HEAD.replace('<title>RealFi Office Hours #7 — 日本語全文</title>',
                        '<title>RealFi Office Hours #8 — %s</title>'
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

    meta = ('<p class="eyebrow">RealFi Office Hours #8</p>\n<h1>%s</h1>\n'
            '<p class="meta">\n  <span>2026-08-28</span>\n  <span>39:46</span>\n'
            '  <span>Discord</span>\n  <span>Investment Framework</span>\n</p>'
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
            for old, new in EN_FIX:
                text = text.replace(old, new)
        mark = ' <em>(%s)</em>' % ("推定" if ja else "inferred") if i in INFERRED else ""
        out.append(
            '<div class="turn">\n'
            '  <div class="turn-who%s">%s%s<span class="turn-time">%s</span></div>\n'
            '  <div class="turn-body"><p>%s</p></div>\n'
            '</div>' % (CLS[t["who"]], NAME[t["who"]], mark, t["t"], text))
    return "\n\n".join(out)


for lang, fn in (("ja", "transcript-ja.html"), ("en", "transcript-en.html")):
    (OUT / fn).write_text(page(lang, render(lang)))
    print("%s — ok" % fn)
