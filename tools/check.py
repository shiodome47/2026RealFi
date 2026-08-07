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

# 匿名化の漏れ検出。**回ごとに持つ。**
#
# チャタムハウスルールの回だけが対象。meta.yml の chatham_house_rule を見て
# 判定するので、公開録画の回（実名を残す回）はここに書かない。
# 名前は回をまたいで衝突する（別の回では普通の単語や別人の名前として出る）ため、
# 全体を一括で検索してはいけない。新しい回で新しい名前が出たらここに足す。
NAMES = {
    "2026-07-24-office-hours-engineering": [
        "Nathan", "Jan", "Peter", "Ben", "Clay", "Lewis", "Damien", "Scoot",
        "Chris", "Frog", "Fogg", "Sean", "Tom", "NEMO", "OYSTR", "TDSP",
        "NVStake", "Strait", "Straight", "K-Man", "Dotare", "Chick",
    ],
    "2026-07-31-data-and-insights": [
        "Liam", "Vlad", "Olivier", "Oliver", "Olivia", "Shiadome", "Shiodome",
        "Yoda", "Panda", "Msku", "Junaid", "Sonny", "Larry", "John",
        "OConnor", "Connor", "Oyster", "Fluid", "KTOP", "Namu", "Strap",
        "Hedge", "Meta",
    ],
    "2026-08-06-office-hours-gtm": [
        # 話者・言及された同僚・質問者
        "Sonny", "Sunny", "Sandy", "Vlad", "John", "David", "Harry",
        "Bashir", "Mauricio", "Rich", "ECP",
        # 経歴から個人が特定できるため業種の記述に置き換えたもの
        "UBS", "Keyrock", "Lisk", "R3", "Brexit",
    ],
}

# 回をまたぐファイル（shared/ や README）はどの回の名前も残っていてはいけない。
SHARED_NAMES = sorted({n for names in NAMES.values() for n in names})

# ただし、公開録画の回で名前が出ている第三者は、回をまたぐファイルにも書いてよい。
# 匿名化したファーストネームと綴りがぶつかるだけで、別人。
# 「この文字列そのもの」を除いてから検索する。フルネームだけを許可すること。
SHARED_ALLOW = [
    "Ben Lam",      # Ben Lamm（Colossal 創業者）— 誤変換表に載せている
    "Ben Lamm",
    "Peter Thiel",
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

    # 配色と言語の切り替え手段
    if "theme-toggle" not in text:
        fail(rel, "配色トグルがない")
    if "lang-toggle" not in text:
        fail(rel, "言語トグルがない")

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

        # まとめは日英そろっていること
        if 'class="l-en"' not in text:
            fail(rel, "英語版のまとめがない")
        else:
            ja_block = text.split('<div class="l-ja">')[1].split('<div class="l-en"')[0]
            en_block = text.split('<div class="l-en" lang="en">')[1]
            for cls in ("fig", "qa", "term", "deck"):
                n_ja = ja_block.count('class="%s"' % cls)
                n_en = en_block.count('class="%s"' % cls)
                if n_ja != n_en:
                    fail(rel, ".%s の数が日英で違う（ja=%d / en=%d）" % (cls, n_ja, n_en))
            for block, tag in ((ja_block, "日本語"), (en_block, "英語")):
                hs = re.findall(r'<h2 id="([^"]+)"', block)
                anchors = [a[1:] for a in re.findall(r'href="(#[^"]+)"', block)]
                missing = [a for a in anchors if a not in hs]
                if missing:
                    fail(rel, "%s版の目次リンクの飛び先がない: %s" % (tag, ", ".join(missing)))

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

    # 実名の残存。回ごとに切り替える
    chatham = {}
    for meta in sorted(ROOT.glob("episodes/*/meta.yml")):
        slug = meta.parent.name
        chatham[slug] = "chatham_house_rule: true" in meta.read_text()
        if chatham[slug] and slug not in NAMES:
            fail(meta.relative_to(ROOT),
                 "チャタムハウスルールの回だが tools/check.py の NAMES にない")

    def names_for(path):
        """このファイルに対して検索すべき名前のリスト。None なら対象外。"""
        parts = path.relative_to(ROOT).parts
        if parts[0] in ("episodes", "docs") and len(parts) > 2:
            slug = parts[1]
            if not chatham.get(slug, False):
                return None            # 公開録画の回。実名を残してよい
            return NAMES.get(slug, [])
        return SHARED_NAMES            # shared/・README・一覧ページなど

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git/" in str(path) or "tools/" in str(path):
            continue
        if path.suffix not in (".html", ".md", ".txt", ".yml"):
            continue
        targets = names_for(path)
        if targets is None:
            continue
        text = path.read_text()
        if targets is SHARED_NAMES:
            for allowed in SHARED_ALLOW:
                text = text.replace(allowed, "")
        for name in targets:
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
