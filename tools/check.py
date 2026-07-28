#!/usr/bin/env python3
"""生成した HTML の検証。コミット前に必ず流す。

    python3 tools/check.py

CLAUDE.md の「完成条件」のうち、機械的に判定できるものを全部見る。
"""

import html.parser
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# 匿名化の漏れ検出。新しい回で新しい名前が出たらここに足す。
NAMES = [
    "Nathan", "Jan", "Peter", "Ben", "Clay", "Lewis", "Damien", "Scoot",
    "Chris", "Frog", "Fogg", "Sean", "Tom", "NEMO", "OYSTR", "TDSP",
    "NVStake", "Strait", "Straight", "K-Man", "Dotare", "Chick",
]

VOID = {"meta", "link", "br", "hr", "img", "input", "source"}
SELF = {"path", "rect", "line", "circle", "polygon", "use", "stop", "polyline", "ellipse"}

problems = []


def fail(where, msg):
    problems.append("%s: %s" % (where, msg))


class TagCheck(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_starttag(self, tag, attrs):
        if tag in VOID or tag in SELF:
            return
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in SELF:
            return
        if not self.stack:
            self.errors.append("余分な </%s>" % tag)
        elif self.stack[-1] != tag:
            self.errors.append("</%s> が来るべき箇所に </%s>（%d 行目）"
                               % (self.stack[-1], tag, self.getpos()[0]))
        else:
            self.stack.pop()


def check_page(path):
    rel = path.relative_to(ROOT)
    text = path.read_text()

    parser = TagCheck()
    parser.feed(text)
    for err in parser.errors[:5]:
        fail(rel, "タグの対応が崩れている — " + err)
    if parser.stack:
        fail(rel, "閉じていないタグ: %s" % parser.stack)

    ids = re.findall(r'\sid="([^"]+)"', text)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        fail(rel, "id が重複: %s" % ", ".join(dupes))

    markers = re.findall(r'<marker id="([^"]+)"', text)
    if len(markers) != len(set(markers)):
        fail(rel, "SVG の marker id が重複している（矢印が別の図に化ける）")

    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith(("http", "mailto")):
            continue
        if href.startswith("#"):
            if href[1:] not in ids:
                fail(rel, "アンカー %s の飛び先がない" % href)
            continue
        target = (path.parent / href).resolve()
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            fail(rel, "リンク切れ: %s" % href)

    for fig in re.findall(r'<div class="fig">.*?</div>', text, re.S):
        for svg in re.findall(r"<svg\b[^>]*>", fig):
            if "role=" not in svg or "aria-label=" not in svg:
                fail(rel, "図の SVG に role / aria-label がない")
                break

    # ナビは末尾に置く
    if 'class="docnav"' in text and text.index('class="docnav"') < len(text) * 0.5:
        fail(rel, "docnav がページ前半にある（末尾に置く）")

    # 配色の切り替え手段
    if "theme-toggle" not in text:
        fail(rel, "配色トグルがない")

    return text


def main():
    pages = sorted(DOCS.rglob("*.html"))
    if not pages:
        print("docs/ に HTML がない")
        return 1

    for page in pages:
        check_page(page)

    # まとめページは見出しごとに deck を持つこと
    for summary in sorted(DOCS.glob("*/index.html")):
        text = summary.read_text()
        rel = summary.relative_to(ROOT)
        heads = re.findall(r"<h2\b([^>]*)>", text)
        body_heads = [h for h in heads if "id=" in h]
        if len(body_heads) < len(heads) - 2:      # .tldr / .card 内の h2 は除外
            fail(rel, "id のない <h2> がある（目次から飛べない）")
        if text.count('class="deck"') < len(body_heads):
            fail(rel, "deck（見出し直下の 1 行要約）が足りない: h2 %d 個に対し %d 個"
                 % (len(body_heads), text.count('class="deck"')))
        if len(body_heads) >= 6 and 'class="toc"' not in text:
            fail(rel, "節が %d 個あるのに目次がない" % len(body_heads))
        if 'class="fig"' not in text:
            fail(rel, "図が 1 つもない")

    # 英語全文と日本語全文は同じ分割にする
    for en in sorted(DOCS.glob("*/transcript-en.html")):
        ja = en.parent / "transcript-ja.html"
        if not ja.exists():
            fail(en.relative_to(ROOT), "対応する日本語全文がない")
            continue
        a, b = en.read_text(), ja.read_text()
        for cls in ("turn", "sec"):
            n_en, n_ja = a.count('class="%s"' % cls), b.count('class="%s"' % cls)
            if n_en != n_ja:
                fail(en.parent.relative_to(ROOT),
                     ".%s の数が英日で違う（en=%d / ja=%d）" % (cls, n_en, n_ja))

    # 実名の残存
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git/" in str(path) or "tools/" in str(path):
            continue
        if path.suffix not in (".html", ".md", ".txt", ".yml"):
            continue
        text = path.read_text()
        for name in NAMES:
            if re.search(r"(?<![A-Za-z])" + re.escape(name) + r"(?![A-Za-z])", text):
                fail(path.relative_to(ROOT), "実名が残っている: %s" % name)

    # 配色は必ず変数経由。直値が混ざるとテーマ追従が壊れる
    css = (DOCS / "assets" / "style.css").read_text()
    body = re.sub(r":root(\[[^\]]+\])?\s*\{[^}]*\}", "", css)
    body = re.sub(r"@media \(prefers-color-scheme[^{]*\{(?:[^{}]|\{[^}]*\})*\}", "", body)
    body = re.sub(r"@media print\s*\{(?:[^{}]|\{[^}]*\})*\}", "", body)
    for literal in re.findall(r"#[0-9a-fA-F]{3,8}\b", body):
        fail("docs/assets/style.css", "配色トークンの外で色を直書きしている: %s" % literal)

    if problems:
        print("NG — %d 件\n" % len(problems))
        for p in problems:
            print("  " + p)
        return 1

    print("OK — %d ページを検証" % len(pages))
    return 0


if __name__ == "__main__":
    sys.exit(main())
