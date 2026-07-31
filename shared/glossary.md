# 用語集・表記ルール

HTML を生成するときは必ずこのファイルを参照して、全回で表記を統一する。

## 文字起こしの誤変換 → 正しい表記

音声認識が毎回同じ間違い方をするので、生成時に機械的に直す。

| 誤変換 | 正しい表記 |
| --- | --- |
| RealFire, Realfi, Real Fi | RealFi |
| Godano, Cordano | Cardano |
| TxPipeke, TX Pipe | TxPipe |
| Dexes | DEX |
| XSpaces | X Spaces |
| VeoFi, Verifi, RealF- | RealFi |
| Docusource, doc store | docs（公式ドキュメント） |
| SPAs | SPO |
| Midnight City | Midnight |
| DFL | RealFi（文脈から。DeFi との混同の可能性もあり） |
| Pagan | 不明。プロジェクト名と思われるが特定できない |
| beach jump | 不明。「聞き取れなかった」ものとして扱う |

**人名・ハンドル名の誤変換**も毎回発生するが、それらは修正するのではなく**匿名化して置き換える**。同一人物が複数の綴りで出てくることがあるので、まとめて同じラベルに寄せる。手順は `shared/speakers.md` を参照。

## プロダクト用語

| 用語 | 説明 | 訳し方 |
| --- | --- | --- |
| **USDR** | RealFi のステーブルコイン。常に 1 USDR = 1 USD | 訳さない |
| **sUSDR** | USDR をステークすると受け取るトークン。**ステーブルコインではない**。価値が変動し、その差分が利回りになる。ファンジブルで、個々のトークンに日付やレートは埋め込まれていない | 訳さない |
| **staking / unstaking** | USDR ↔ sUSDR の交換。公式レート（official rate）で行われ、レートは常に公開される | ステーク / アンステーク |
| **bridge** | 他チェーンとの接続。burn-and-mint ではなく、EVM 側でもネイティブな体験を提供しつつ Cardano を source of truth に置く設計 | ブリッジ |
| **hub and spokes** | ブリッジの構成。Cardano がハブ（中心・唯一の権威）、他チェーンがスポーク | ハブ&スポーク |
| **source of truth** | 会計とステーキングの正となる場所。RealFi では Cardano | 正となる台帳 |
| **one-click flows** | 複数プロトコルをまたぐ複数トランザクションを、ユーザーの署名1回で実行する仕組み | ワンクリックフロー |
| **looping strategy** | 借入と再投資を繰り返してレバレッジをかける DeFi の運用手法 | ルーピング戦略 |
| **governance token** | 未発行。来年前半予定 | ガバナンストークン |
| **SDK** | 外部開発者向け。一部はオープンソース化予定（バックログ） | 訳さない |
| **transparency portal** | 資金の投資先を公開するポータル。ウェブサイト上にある | 透明性ポータル |
| **private credit** | RealFi の裏付け資産。ノンバンクによる融資 | プライベートクレジット |
| **banking the unbanked** | RealFi のミッション。銀行口座を持てない層に金融アクセスを届ける | 訳さず注釈をつける |
| **anti-farming** | エアドロップ狙いの不正な複数ウォレット運用を検知・遮断する仕組み | アンチファーミング |
| **depeg** | ステーブルコインが 1 ドルの固定を外れること | デペグ |
| **TVL** | Total Value Locked。プロトコルに預けられている資産の総額 | 訳さない |
| **peg stability module（PSM）** | USDR を 1 ドルに保つために常時動く仕組み | ペッグ安定化モジュール |
| **stability fund** | ペッグ維持のために RealFi 自身が運用する資金 | 安定化ファンド |
| **AMM** | 自動マーケットメイカー。DEX の値付けの仕組み | 訳さない |
| **time to cash** | ある資産を現金化するまでにかかる時間。RealFi では全ポジションの「性質」として扱う | 現金化までの時間 |
| **epoch** | Cardano の 5 日周期 | エポック |
| **SPO accelerator program** | ステークプールオペレーター向けの支援プログラム。2026-07-22 開始 | SPO アクセラレータープログラム |
| **active wallet（アクティブウォレット）** | **一定期間内に動いたウォレットの数。**そのチェーンに存在するウォレットの総数ではない。比較のたびに「どの期間か」「アクティブの定義は何か」を確認する。揃っていない可能性があれば明記する | アクティブウォレット |
| **stake key（ステークキー）** | ウォレットの委任に使う鍵。**同じシードから作られたウォレットは共通のステークキーを持つ**ため、testnet とメインネットの対応付けに使える。逆にシードを分けた人は機械的には照合できない | ステークキー |
| **farming wallet** | エアドロップ狙いで大量作成されたウォレット。集計から除外される | ファーミングウォレット |
| **capital productivity** | 資本がどれだけ活発に使われているか | 資本の生産性 |
| **money market fund** | 短期の安全資産で運用するファンド。トークン化されたものを保有 | マネー・マーケット・ファンド |
| **CLO ETF** | ローン担保証券に投資する ETF。投資適格のものを検討 | 訳さない |
| **DefiLlama / Dune** | DeFi の統計・分析プラットフォーム。掲載が to-do リストにある | 訳さない |
| **registry maxing** | 各種の分析プラットフォームに漏れなく掲載されること（進行役の造語的表現） | 訳さない・注釈をつける |

## 組織・プロダクト名

| 名前 | 説明 |
| --- | --- |
| **Cardano** | RealFi のベースとなるブロックチェーン |
| **Sundae / SundaeSwap** | Cardano の DEX。2025年8月から Web3 ワークストリームのパートナー |
| **TxPipe** | Cardano の開発企業。監査で協力 |
| **Liqwid** | Cardano のレンディングプロトコル。ワンクリックフローの連携先として言及 |
| **Midnight** | Cardano 系のプライバシー特化チェーン。**未着手だが今後やりたい領域**。コミュニティに知見を求めている |
| **Rosen Bridge** | Cardano のクロスチェーンブリッジ。USDR/sUSDR の対応はメインネット後 |
| **IO / Input Output** | Cardano の中核開発企業 |
| **EVM** | Ethereum Virtual Machine 系のチェーン群 |

## 翻訳の方針

- **プロダクト用語・チェーン名・組織名は訳さない**（USDR, sUSDR, Cardano, EVM, DEX, SDK, testnet, mainnet など）
- **testnet / mainnet** はそのまま。「テストネット」「メインネット」でもよいが1本の中では統一する
- 話者の発言は「ですます調」で訳す。口語のフィラー（you know, I mean, like）は落とす
- 断定していない発言（"I think", "probably", "we haven't landed on"）は**日本語でも断定しない**。ロードマップや時期の話で特に重要
