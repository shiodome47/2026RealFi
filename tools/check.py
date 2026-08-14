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
# meta.yml の chatham_house_rule が true か partial の回だけが対象。
# 公開録画の回（false。実名を残す回）はここに書かない。
# **partial の回は「残してはいけない名前」だけを書く。**残してよい実名を書くと、
# その回のページが自分の名前で落ちてしまう。
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
        "Sonny", "Sunny", "Sandy", "Senny", "Vlad", "John", "David", "Harry",
        "Bashir", "Mauricio", "Rich", "ECP",
        # 公式録音の話者ラベル・呼びかけられたハンドル名
        "Ben", "Doc", "Manesh", "NB", "Paul", "Scoot", "Stakepool",
        # 第三者の実名。この回は匿名化の対象なので、公開回の人物でも役割で書く
        "Charles", "Hoskinson",
        # 経歴から個人が特定できるため業種の記述に置き換えたもの
        "UBS", "Keyrock", "Lisk", "R3", "Brexit",
    ],
    # partial の回。**残してはいけない名前だけ**を書く。
    # 話者（ホストと CEO）の実名は依頼により残しているので、ここには書かない。
    "2026-08-14-ask-the-ceo": [
        # 読み上げられた質問者
        "Louis", "Sebastian", "Funky", "Chris", "Adolf",
        # ハンドル名 "Key" も置換したが、**一覧に入れられない**。
        # 英語版まとめの見出し "Key points" と衝突して、自分のページが落ちるため。
        # 置換は手作業で行い、shared/speakers.md に記録してある。
        # 社内の人物として名前が挙がった同僚
        "Danelle", "Rob",
    ],
    "2026-08-11-masumi-ai-forum": [
        # 話者・チャットで発言した参加者
        "Patrick", "Sharan", "Scott", "Kelly", "Sandro",
        "Edgar", "Eris", "Jacob", "Umar", "Ken",
        # 第三者として名前が挙がった人物。役割に置き換えた
        "Hoskinson", "Dorsey",
        # 所属・役職から個人が特定できるため置き換えたもの
        "utxo AG", "Hydra team", "IEO",
    ],
}

# 回をまたぐファイル（shared/ や README）はどの回の名前も残っていてはいけない。
SHARED_NAMES = sorted({n for names in NAMES.values() for n in names})

# ただし、公開録画の回で名前が出ている第三者は、回をまたぐファイルにも書いてよい。
# 匿名化したファーストネームと綴りがぶつかるだけで、別人。
# 「この文字列そのもの」を除いてから検索する。フルネームだけを許可すること。
SHARED_ALLOW = [
    "Ben Lam",           # Ben Lamm（Colossal 創業者）— 誤変換表に載せている
    "Ben Lamm",
    "Peter Thiel",
    "Charles Hoskinson", # 2026-07-26 の回のゲスト。フルネームでのみ許可する
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


def read_series():
    """shared/series.yml を読む。2 階層しかないので素朴に読む。"""
    series, cur = {}, None
    for line in (ROOT / "shared" / "series.yml").read_text().split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[0].isspace():
            cur = line.split(":")[0].strip()
            series[cur] = {}
        elif cur:
            k, _, v = line.strip().partition(":")
            series[cur][k.strip()] = v.split("#")[0].strip()
    return series


def field(text, name):
    m = re.search(r"^%s:\s*(.*)$" % re.escape(name), text, re.M)
    return m.group(1).split("#")[0].strip() if m else None


def check_series():
    """シリーズの定義と、ページに出ている通し番号が食い違っていないか。"""
    series = read_series()
    index = (DOCS / "index.html").read_text()
    seen = {}

    for meta in sorted(ROOT.glob("episodes/*/meta.yml")):
        slug, text = meta.parent.name, meta.read_text()
        rel = meta.relative_to(ROOT)

        sid = field(text, "series")
        if sid not in series:
            fail(rel, "series が shared/series.yml にない: %r" % sid)
            continue
        spec = series[sid]
        numbered = spec.get("numbered") == "true"
        no = field(text, "series_no")

        if numbered and not no:
            fail(rel, "%s は通し番号を振るシリーズだが series_no がない" % sid)
        if not numbered and no:
            fail(rel, "%s は通し番号を振らないシリーズなのに series_no がある" % sid)
        if numbered and no:
            if (sid, no) in seen:
                fail(rel, "series_no %s が %s と重複している" % (no, seen[(sid, no)]))
            seen[(sid, no)] = slug

        # ページのヘッダー。番号を振るシリーズは「シリーズ名 #番号」に固定する。
        # 振らないシリーズの見出しは番組名なので（例: A Dose of Alpha）中身は問わず、
        # 通し番号が紛れ込んでいないかだけ見る。
        want = "%s #%s" % (spec.get("title_ja", ""), no) if numbered and no else None
        for page in sorted((DOCS / slug).glob("*.html")):
            if page.name == "standalone.html":
                continue          # 3 ページから組み直すので元が正しければ正しい
            got = re.search(r'<p class="eyebrow">([^<]*)</p>', page.read_text())
            if not got or not got.group(1).strip():
                fail(page.relative_to(ROOT), "eyebrow がない")
            elif want and got.group(1).strip() != want:
                fail(page.relative_to(ROOT),
                     "eyebrow が meta.yml と違う: %r（期待 %r）" % (got.group(1).strip(), want))
            elif not want and re.search(r"#\d", got.group(1)):
                fail(page.relative_to(ROOT),
                     "通し番号を振らないシリーズなのに eyebrow に番号がある: %r" % got.group(1).strip())

        # 一覧ページのカードにも同じ番号が出ていること
        card = re.search(r'<a class="card" href="\./%s/">(.*?)</a>' % re.escape(slug),
                         index, re.S)
        if not card:
            fail("docs/index.html", "%s のカードがない" % slug)
        elif numbered and no:
            if '<p class="card-no">#%s</p>' % no not in card.group(1):
                fail("docs/index.html", "%s のカードに #%s が出ていない" % (slug, no))
        elif 'class="card-no"' in (card.group(1) if card else ""):
            fail("docs/index.html", "%s は通し番号を振らないシリーズなのに番号が出ている" % slug)


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

    check_series()

    # 実名の残存。回ごとに切り替える。
    #
    # chatham_house_rule は 3 値。
    #   true    … 全員の実名を落とす。NAMES にはその回の全員を入れる
    #   partial … 一部の実名を残す（登壇者は実名、質問者は匿名など）。
    #             **NAMES には「残してはいけない名前」だけ**を入れる
    #   false   … 公開録画。実名を残すので走査しない
    chatham = {}
    for meta in sorted(ROOT.glob("episodes/*/meta.yml")):
        slug, rel = meta.parent.name, meta.relative_to(ROOT)
        mode = field(meta.read_text(), "chatham_house_rule") or "false"
        if mode not in ("true", "false", "partial"):
            fail(rel, "chatham_house_rule は true / partial / false のどれか: %r" % mode)
        chatham[slug] = mode in ("true", "partial")
        if chatham[slug] and slug not in NAMES:
            fail(rel, "実名を落とす回だが tools/check.py の NAMES にない")

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
        if path.suffix not in (".html", ".md", ".txt", ".yml", ".srt"):
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
