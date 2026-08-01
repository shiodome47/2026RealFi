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

**人名・ハンドル名の誤変換**も毎回発生する。チャタムハウスルールの回では、それらは修正するのではなく**匿名化して置き換える**。同一人物が複数の綴りで出てくることがあるので、まとめて同じラベルに寄せる。手順は `shared/speakers.md` を参照。

**公開録画の回（`chatham_house_rule: false`）では実名を残す。**この場合、人名も含めて**固有名詞の明らかな誤変換は修正する**。

### 2026-07-26 A Dose of Alpha で出た誤変換

| 誤変換 | 正しい表記 |
| --- | --- |
| Realfly | RealFi |
| Amergo | EMURGO |
| Metcaf's law | Metcalfe's law（メトカーフの法則） |
| Dan Larmer / Bit shares | Dan Larimer / BitShares |
| Ben Lam | Ben Lamm（Colossal の創業者） |
| Ilya | Illia（NEAR 共同創業者） |
| Leos / Paris・Para | Leios / Peras |
| pith | Pyth |
| Ave | Aave |
| Morfo | Morpho |
| DSI / DFI / CFI | DeSci / DeFi / CeFi |
| Mike Sailor | Michael Saylor |
| Greta Thornberg | Greta Thunberg |
| in silica | in silico |
| Dows | DAOs |
| intense | intents（インテント） |
| zero cash | Zerocash |
| MPP | MCP |
| X402 | x402 |
| DAPs | DATs（digital asset treasury。文脈は Michael Saylor 型の企業） |
| shitification | enshittification |
| mountain line | mountain lion |
| Robin Hood | Robinhood |
| Alpha Growth | AlphaGrowth |
| D-rep | DRep |
| Near | NEAR |
| Pogen | **Pogun**（Input Output のベンチャー。Bitcoin DeFi を Cardano に持ち込むプラットフォーム） |
| the Pentad | **Pentad**（誤変換ではない。Cardano の主要 5 組織による共同体制） |

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
| **stake credential / stake key（ステーク資格情報）** | アドレスに含まれる、委任に使う情報。支払い資格情報とは別物。ネットワークが違えばアドレスの文字列は変わる（`stake1…` / `stake_test1…`）が、**中のステーク資格情報が同じなら一致する**ため、testnet とメインネットの対応付けに使える。**同じシードでもアカウントが違えば一致しない**ので「同じシード＝一致」ではない。また**一致するのは資格情報どうしであって人ではない**（1 人が複数持つことも、取引所経由で複数人が 1 つに集約されることもある） | ステーク資格情報 |
| **farming wallet** | エアドロップ狙いで大量作成されたウォレット。集計から除外される | ファーミングウォレット |
| **flywheel（フライホイール）** | 弾み車。各ステップが次を強くし、一周ごとに勢いが増す循環。RealFi では「深さ → ルーピング → TVL → 統合先の増加 → さらに深さ」 | フライホイール |
| **DeFi integration（DeFi 統合）** | USDR / sUSDR が他プロトコルの中で使える状態になること。**他チェーンから資金を呼び込む話（ブリッジ）とは別物**。ルーピングには「DEX の取引プール」と「sUSDR を担保に取るレンディング」の両方が要る | DeFi 統合 |
| **capital productivity** | 資本がどれだけ活発に使われているか | 資本の生産性 |
| **money market fund** | 短期の安全資産で運用するファンド。トークン化されたものを保有 | マネー・マーケット・ファンド |
| **CLO ETF** | ローン担保証券に投資する ETF。投資適格のものを検討 | 訳さない |
| **AlphaGrowth** | DeFi の運用・成長支援、トークノミクス、事業開発を専門とする会社。Cardano PRIME の運営主体 | 訳さない |
| **PRIME** | Cardano の財務庫から 1 億 2,000 万 ADA を引き出し、12 か月で DeFi の流動性と TVL を増やす提案。目標は条件を満たす TVL の 2 億ドル以上の純増 | 訳さない |
| **DRep** | Cardano のガバナンスで投票権を委任される代表者。財務引き出しの可決には 3 分の 2（67%）の賛成が必要 | 訳さない |
| **Net Change Limit** | 一定期間に Cardano の財務庫から出せる総額の上限 | 訳さない・注釈をつける |
| **DefiLlama / Dune** | DeFi の統計・分析プラットフォーム。掲載が to-do リストにある | 訳さない |
| **registry maxing** | 各種の分析プラットフォームに漏れなく掲載されること（進行役の造語的表現） | 訳さない・注釈をつける |
| **executive function（行政機能）** | 戦略を一貫して立案・執行する常設主体。Cardano には未整備。「憲法 → 正統な批准制度 → 執行機能」という順序が主張されている。**番組の「立法・司法はできた、あとは行政」という言い方は国家制度への類推**で、実際の機関構成とは 1 対 1 では対応しない（下の DReps / CC / SPOs を参照） | 行政機能・行政府 |
| **DReps** | ADA 保有者を代表して投票する代表者。財務庫・憲法改正・パラメータ変更・ハードフォーク・Info Action・CC の更新まで**全種類のガバナンスアクションに投票できる**。議会に最も近いが、一般的な法律を制定する仕組みも条文の審議・修正もないので「立法府そのもの」ではなく**主要な批准機関** | 訳さない |
| **Constitutional Committee（CC）** | 提案が憲法に適合するかを判断する委員会。憲法裁判所に似るが、**紛争を裁かず、制裁も科さず、過去の行為も審理せず、提案を修正できない**。賛否を投票するだけなので「司法府」より**合憲性を事前審査する委員会** | 訳さない・注釈をつける |
| **SPOs（ガバナンス機関としての）** | ステークプールの運用者。CC への不信任・CC の更新・ハードフォーク・Info Action などに投票する。**ハードフォークは実際にノードを更新する SPO の協力なしに成立しない**ため明示的な承認主体。国家の三権に対応しない Cardano 独自の機関 | 訳さない |
| **CIP-1694 の批准構造** | DReps / CC / SPOs は三権分立ではなく、**同じ 1 つのガバナンスアクションを別々の基準で共同批准する 3 つの投票機関**。CIP-1694 自身が「異なるガバナンス機関」と呼び、アクションの種類ごとに少なくとも 2 つの批准を求める。**複数の鍵をそろえて開く共同承認に近い。ただしこれが当てはまるのは実行効果のあるアクションだけ**（下の Info Action を参照） | 訳さない・注釈をつける |
| **Info Action** | 資金も動かさず、パラメータも変えず、ハードフォークも起動せず、憲法も書き換えない。**投票結果をチェーンに記録するだけ**のガバナンスアクション。**「閾値に届かなければ何も起きない」が当てはまらない**のがここ。正式な批准に至らなくても、票が「支持のシグナル」として実務に使われることがある。**数値を書くときは、批准されたのか、シグナルとして扱われただけなのかを必ず区別する** | 訳さない・注釈をつける |
| **PET** | privacy enhancing technologies。ZK・MPC・TEE を組み合わせた、中身を見せずに検証する技術群 | 訳さない・注釈をつける |
| **TEE** | trusted execution environment。計算を外から覗けない箱の中で走らせる仕組み | 訳さない |
| **MCS / intents** | multi-chain signatures。「何をしたいか」だけ指定し、どのチェーンで決済されるかは気にしない仕組み。MCS で書き込み、ZK で読み取る | 訳さない・インテント |
| **abstraction（アブストラクション）** | どのチェーン・どのインフラを使っているかをユーザーが意識しなくてよくすること | 訳さない |
| **smart compliance** | 規制対応を、人間の審査ではなく ZK 証明によるイエス・ノーの連続に置き換える発想 | 訳さない・注釈をつける |
| **OWS / x402** | エージェントがウォレットを持ち、支払いをするための標準 | 訳さない |
| **DeFi mullet（DeFi マレット）** | 前面は CeFi のアプリ、背面は DeFi が利回りを作る構成。Morpho × Coinbase / Robinhood が例 | DeFi マレット |
| **RWA 1.0 / 2.0** | 1.0 は既存商品（株など）のトークン化。2.0 は規制対象の資産で、これまで作れなかった商品を作ること。番組ではこの 2 つを明確に分けている | 訳さない |
| **DAT** | digital asset treasury。暗号資産を保有することを主眼にした上場企業。番組では否定的な文脈で言及 | 訳さない・注釈をつける |
| **enshittification** | プラットフォームが成長を終えて劣化していく現象を指す造語。ホスト側が使い、Charles Hoskinson が「いい言葉だ」と受けている | 訳さない（カタカナで表記） |
| **Leios / Peras** | Cardano のコンセンサス改良。Leios はスループット、Peras はファイナリティが対象 | 訳さない |
| **ghost chain（ゴーストチェーン）** | 活動のないチェーンという批判。Cardano については「委任側は活発、DeFi 側は貧弱」という二面性として半分認められている | ゴーストチェーン |

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
| **AlphaGrowth** | DeFi の成長支援・トークノミクス・事業開発の会社。ポッドキャスト「A Dose of Alpha」を運営し、Cardano の PRIME 提案を出している |
| **Midnight City** | Midnight 上に戦略のマーケットプレイスと取引エージェントを載せる構想。2026-07-26 の回で初出 |
| **Pogun** | Input Output が進める、Cardano 向けの**エンドツーエンド型 Bitcoin DeFi 構想**。BTC を運ぶだけでなく、貸付・担保・利回り運用に使える状態まで一体で作る。①非証拠金型クレジット市場（オラクル価格での日中強制清算を使わず、金利・期間・担保・デフォルト条件を当事者が合意。ローンは譲渡可能な Bond Token）②Yield DApp ③BitVM を使ったトラスト最小化ブリッジ。**この順で作るのは、BTC が来た瞬間に使い道がある状態にするため。**リードは Omer Husain、チームには Input Output の Bitcoin ブリッジ仕様 Cardinal の関係者。財務庫に 1,229 万 ADA を要求し、助成ではなく部分的な投資（収益の 20% を返済まで、その後 5% を永続的に返す）。**提案上のロードマップであり、2026-08-01 時点の情報。**音声認識では “Pogen” と出る |
| **the Pentad** | Cardano の主要 5 組織（Input Output / Cardano Foundation / EMURGO / Midnight Foundation / Intersect MBO）による**共同の調整・実行体制**。プロダクトでも新会社でもない。個々の DApp では入れられない基盤統合（Circle の USDCx、Pyth、Dune、LayerZero、Fireblocks 等の機関向けカストディ）を、契約・予算・技術・ガバナンスの面からまとめて進める。Critical Integrations Budget は 7,000 万 ADA、管理者は Intersect。**Pogun が「製品」なのに対し、Pentad は「体制」** |
| **Colossal** | 絶滅種の復元を手がける合成生物学の企業。Charles Hoskinson が初期から出資している |
| **Morpho** | Ethereum 系のレンディングプロトコル。Coinbase / Robinhood の預金商品の裏側で使われている例として挙げられた |
| **Intersect / PRAGMA** | Cardano のエコシステム組織。Cardano Foundation が担えなかった部分を補ってきたと評価されている |

## 翻訳の方針

- **プロダクト用語・チェーン名・組織名は訳さない**（USDR, sUSDR, Cardano, EVM, DEX, SDK, testnet, mainnet など）
- **testnet / mainnet** はそのまま。「テストネット」「メインネット」でもよいが1本の中では統一する
- 話者の発言は「ですます調」で訳す。口語のフィラー（you know, I mean, like）は落とす
- 断定していない発言（"I think", "probably", "we haven't landed on"）は**日本語でも断定しない**。ロードマップや時期の話で特に重要
