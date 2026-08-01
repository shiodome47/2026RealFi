#!/usr/bin/env python3
"""3 ページを 1 ファイルにまとめた standalone.html を組み立て直す。

    python3 tools/build_standalone.py <slug> [<slug> ...]

引数がなければ docs/ 配下で standalone.html を持つ回をすべて作り直す。
中身はそのまま docs/<slug>/ の 3 ページから取り直すので、
まとめや全文を直したら必ずこれを流す。
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CSS = (DOCS / "assets" / "style.css").read_text().strip()

# standalone.html にだけ要るスタイル。通常の 3 ページでは使わないので
# style.css には入れず、ここで足す。
EXTRA_CSS = """/* ===== 単一ページ版（1 ファイル完結）用の追加 ===== */
.part { scroll-margin-top: 1.5rem; }
.part + .part { margin-top: 5rem; }
.part-head {
  display: flex; align-items: baseline; gap: .8rem; flex-wrap: wrap;
  margin: 0 0 2rem; padding: .9rem 0 .8rem;
  border-top: 2px solid var(--accent); border-bottom: 1px solid var(--border);
}
.part-head h2 { border: none; padding: 0; margin: 0; font-size: 1.35rem; color: var(--text); }
.part-head h2::before { display: none; }
.part-head span { font-size: .8125rem; color: var(--text-muted); }
.part > .l-ja > .thesis:first-child, .part > .l-en > .thesis:first-child { margin-top: 0; }
.jump-top {
  margin: 2.2rem 0 0; padding: 0 0 1.4rem;
  border-top: none; border-bottom: 1px solid var(--border);
}
.jump {
  display: flex; flex-wrap: wrap; align-items: baseline; gap: .3rem 1.1rem;
  margin: 3.5rem 0 0; padding-top: 1.3rem;
  border-top: 1px solid var(--border); font-size: .8125rem;
}
.jump-label { width: 100%; font-size: .75rem; color: var(--text-muted); margin-bottom: .45rem; }
.jump a { color: var(--text-muted); text-decoration: none; }
.jump a:hover, .jump a:focus-visible { color: var(--accent); text-decoration: underline; }
.jump a:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; border-radius: 2px; }
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }"""


def content(path):
    t = path.read_text()
    body = t.split("<!--content-->")[1].split("<!--/content-->")[0].strip()
    body = body.replace('href="./transcript-en.html"', 'href="#en"')
    body = body.replace('href="./transcript-ja.html"', 'href="#ja"')
    return body.replace('href="./"', 'href="#summary"')


def between(text, start, end):
    return text[text.index(start):text.index(end)].strip()


def build(d):
    idx = d.joinpath("index.html").read_text()
    title = re.search(r"<title>(.*?)</title>", idx, re.S).group(1)
    script = re.search(r"<script>.*?</script>", idx, re.S).group(0)
    tools = between(idx, '<div class="page-tools">', '<p class="eyebrow">')
    head = between(idx, '<p class="eyebrow">', "<!--content-->")
    # meta の <span> を 1 行に詰める
    head = re.sub(r">\s*\n\s*<span", "><span", head)

    meta = ROOT / "episodes" / d.name / "meta.yml"
    meta_text = meta.read_text() if meta.exists() else ""
    chatham = "chatham_house_rule: true" in meta_text
    m = re.search(r"^\s*video:\s*(https?://\S+)", meta_text, re.M)
    source_link = ""
    if m:
        source_link = ('\n  <a href="%s"><span class="l-ja">元の録画</span>'
                       '<span class="l-en">Original recording</span></a>' % m.group(1))
    if chatham:
        en_label, en_label_en = "匿名化以外は未編集", "Unedited apart from anonymisation"
    else:
        en_label = "固有名詞の誤変換を修正済み"
        en_label_en = "Obvious proper-noun misrecognitions corrected"

    # standalone は 1 ファイルで配られるので、扱いの断りをフッターにも入れる
    if chatham:
        note_ja = "このコールはチャタムハウスルールで運用されています。発言者の氏名は記載していません。"
        note_en = "These calls run under the Chatham House Rule, so no speaker is named."
    else:
        note_ja = ("この回は公開されている録画にもとづくため、チャタムハウスルールの対象ではなく、"
                   "発言者は実名のまま扱っています。")
        note_en = ("This session is based on a publicly published recording, so it is not covered "
                   "by the Chatham House Rule and the speakers are named.")

    foot = re.search(r"<footer>(.*?)</footer>", idx, re.S).group(1).strip()
    foot = foot.replace('</span><span class="l-en">', '<br>%s</span><span class="l-en">' % note_ja, 1)
    foot = foot.replace("</span></p>", "<br>%s</span></p>" % note_en, 1)

    page = f"""{title and f"<title>{title}</title>"}
<style>
{CSS}

{EXTRA_CSS}
</style>

<div class="wrap" id="top">

{script}

{tools}

{head}

<nav class="jump jump-top" aria-label="このページの構成 / Page contents">
  <span class="jump-label"><span class="l-ja">このページ 1 枚に、まとめ・日本語全文・英語全文（原文）の 3 つが入っています。</span><span class="l-en">This single page holds all three: the summary, the Japanese transcript, and the English original.</span></span>
  <a href="#summary"><span class="l-ja">まとめ</span><span class="l-en">Summary</span></a>
  <a href="#ja"><span class="l-ja">日本語全文</span><span class="l-en">Full transcript (Japanese)</span></a>
  <a href="#en"><span class="l-ja">英語全文（原文）</span><span class="l-en">Full transcript (English original)</span></a>
</nav>

<section class="part" id="summary">
{content(d / "index.html")}
</section>

<section class="part" id="ja">
<div class="part-head"><h2><span class="l-ja">日本語全文</span><span class="l-en">Full transcript — Japanese</span></h2><span><span class="l-ja">英語全文を通しで訳したもの</span><span class="l-en">A translation of the English original</span></span></div>
{content(d / "transcript-ja.html")}
</section>

<section class="part lang-en" id="en">
<div class="part-head"><h2><span class="l-ja">英語全文（原文）</span><span class="l-en">Full transcript — English original</span></h2><span><span class="l-ja">{en_label}</span><span class="l-en">{en_label_en}</span></span></div>
{content(d / "transcript-en.html")}
</section>

<nav class="jump" aria-label="Page navigation">
  <span class="jump-label"><span class="l-ja">このページには 3 つの版が入っています。</span><span class="l-en">This page contains all three versions.</span></span>
  <a href="#summary"><span class="l-ja">まとめ</span><span class="l-en">Summary</span></a>
  <a href="#ja"><span class="l-ja">日本語全文</span><span class="l-en">Full transcript (Japanese)</span></a>
  <a href="#en"><span class="l-ja">英語全文（原文）</span><span class="l-en">Full transcript (English original)</span></a>
  <a href="#top"><span class="l-ja">↑ 先頭へ</span><span class="l-en">↑ Back to top</span></a>{source_link}
</nav>

<footer>
{foot}
</footer>

</div>
"""
    d.joinpath("standalone.html").write_text(page)
    print("%s/standalone.html — %d bytes" % (d.name, len(page)))


def main(argv):
    slugs = argv or [p.parent.name for p in sorted(DOCS.glob("*/standalone.html"))]
    for slug in slugs:
        build(DOCS / slug)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
