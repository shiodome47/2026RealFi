#!/usr/bin/env python3
"""2026-09-11 Cardano Seminar（RealFi 回）の全文ページ 2 枚を生成する。"""
import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _sem_turns import build          # noqa: E402
from _sem_ja import JA, INFERRED      # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/2026-09-11-cardano-seminar-realfi"
OUT.mkdir(parents=True, exist_ok=True)

VIDEO = "https://www.youtube.com/watch?v=735yJ_erh2A"

# 公開録画の回の雛形（A Dose of Alpha）からヘッダーを取る。言語ボタンは対のページへのリンク。
HEAD = (ROOT / "docs/2026-07-26-a-dose-of-alpha/transcript-ja.html") \
    .read_text().split('<p class="eyebrow">')[0]

CLS = {"Host": " host"}
NAME = {"Host": "Denicio MacKenzie Bute"}   # 動画の画面の表示名。依頼者が確認

# 英語全文は原文のまま。**進行役の名前の聞き取りミスだけ直す**（画面の表示名で確認済み）。
EN_FIX = [("Dentio", "Denicio")]

NOTE_JA = """<div class="note">
<p><strong>このページについて。</strong>この対談は <a href="%s">YouTube で公開されている</a>ため、チャタムハウスルールの対象ではなく、<strong>発言者は実名のまま</strong>です。質問者も、動画の中で呼ばれた名前のままにしています。</p>
<p>原本は依頼者が<strong>固有名詞の誤変換を直したうえで</strong>渡してきたテキストで、話者ラベルと時刻が付いています。<strong>文言はそれ以外は語られたとおり</strong>で、話者が言い間違えて言い直した箇所（USDR → USDrf）もそのまま訳しています。進行役の名前は一度だけ呼ばれていて（7:55 ごろ）、字幕では "Dentio" でしたが、<strong>動画の画面の表示名で Denicio MacKenzie Bute と確認できた</strong>ので、その箇所だけ直しています。</p>
<p><strong>スライドが使われた回です。</strong>「このグラフ」「次のスライド」という参照が残っていますが、<strong>ここに載っているのは音声で語られた内容だけ</strong>です。</p>
</div>""" % VIDEO

NOTE_EN = """<div class="note">
<p><strong>About this page.</strong> This conversation was <a href="%s">published on YouTube</a>, so it is not covered by the Chatham House Rule and <strong>the speakers are named</strong>. Questioners appear under the names they were addressed by on the call.</p>
<p>The source is a transcript in which <strong>proper nouns were corrected by the requester before delivery</strong>, with speaker labels and timestamps. <strong>The wording is otherwise as spoken</strong>, including the places where the speaker corrects himself (USDR → USDrf). The host is addressed by name once (around 7:55) — “Dentio” in the transcript — and <strong>the on-screen caption confirms the spelling as Denicio MacKenzie Bute</strong>, so that one word is corrected.</p>
<p><strong>Slides were shown.</strong> References to them survive in the audio, but <strong>only what was spoken aloud appears here</strong>.</p>
</div>""" % VIDEO


def page(lang, body):
    ja = lang == "ja"
    head = HEAD.replace('<title>A Dose of Alpha — Full transcript (Japanese) / 日本語全文</title>',
                        '<title>Cardano Seminar: RealFi — %s</title>'
                        % ("Full transcript (Japanese) / 日本語全文" if ja else "Full transcript (English) / 英語全文"))
    if not ja:
        head = head.replace('<html lang="ja">', '<html lang="en">')
        head = head.replace('<div class="wrap lang-ja">', '<div class="wrap lang-en">')
        head = head.replace(
            '<a class="lang-toggle" href="./transcript-en.html" aria-label="Read the English original" title="Read the English original">EN</a>',
            '<a class="lang-toggle" href="./transcript-ja.html" aria-label="日本語全文を読む" title="日本語全文を読む">日本語</a>')
        head = head.replace('aria-label="配色を切り替える" title="配色を切り替える"',
                            'aria-label="Toggle colour scheme" title="Toggle colour scheme"')
    assert "<title>Cardano Seminar" in head, "title の差し替えに失敗"

    meta = ('<p class="eyebrow">Cardano Seminar</p>\n<h1>%s</h1>\n'
            '<p class="meta">\n  <span>2026-09-11</span>\n'
            '  <span><a href="%s">YouTube</a></span>\n  <span>36:49</span>\n'
            '  <span>%s</span>\n</p>'
            % ("日本語全文" if ja else "Full transcript — English (original)", VIDEO,
               "Denicio MacKenzie Bute（進行役）＋RealFi の CEO＋質問者 3 名" if ja else "Denicio MacKenzie Bute (host), RealFi's CEO and three questioners"))

    if ja:
        nav = """<nav class="docnav">
  <span class="docnav-label">英語の原文を訳したもの。固有名詞は依頼者が確認済み。</span>
  <a href="./">まとめ</a>
  <a href="./transcript-ja.html" aria-current="page">日本語全文</a>
  <a href="./transcript-en.html">英語全文（原文）</a>
  <a href="%s">元の動画（YouTube）</a>
  <a href="../">← 全セッション</a>
</nav>""" % VIDEO
    else:
        nav = """<nav class="docnav">
  <span class="docnav-label">The original wording, with proper nouns corrected by the requester.</span>
  <a href="./">Summary</a>
  <a href="./transcript-ja.html">Full transcript (Japanese)</a>
  <a href="./transcript-en.html" aria-current="page">Full transcript (English original)</a>
  <a href="%s">Original recording (YouTube)</a>
  <a href="../">← All sessions</a>
</nav>""" % VIDEO

    foot = "\n<footer>\n  <p>Cardano session archive</p>\n</footer>\n\n</div>\n</body>\n</html>\n"
    return "%s%s\n\n<!--content-->\n\n%s\n\n%s\n<!--/content-->\n\n%s\n%s" % (
        head, meta, NOTE_JA if ja else NOTE_EN, body, nav, foot)


def render(lang):
    ja = lang == "ja"
    out = []
    items, turns = build()
    i = -1
    for t in items:
        if "sec" in t:
            out.append('<div class="sec">%s</div>' % html.escape(t["sec"][0 if ja else 1]))
            continue
        i += 1
        if ja:
            text = JA.get(i)
            if text is None:
                raise SystemExit("turn %d の日本語がない: %s" % (i, t["en"][:70]))
        else:
            text = html.escape(t["en"], quote=False)
            for old, new in EN_FIX:
                text = text.replace(old, new)
        mark = ' <em>(%s)</em>' % ("推定" if ja else "inferred") if i in INFERRED else ""
        who = NAME.get(t["who"], t["who"])
        time = '<span class="turn-time">%s</span>' % t["t"] if t["t"] else ""
        out.append(
            '<div class="turn">\n'
            '  <div class="turn-who%s">%s%s%s</div>\n'
            '  <div class="turn-body"><p>%s</p></div>\n'
            '</div>' % (CLS.get(t["who"], ""), html.escape(who, quote=False), mark, time, text))
    return "\n\n".join(out)


for lang, fn in (("ja", "transcript-ja.html"), ("en", "transcript-en.html")):
    (OUT / fn).write_text(page(lang, render(lang)))
    print("%s — ok" % fn)
