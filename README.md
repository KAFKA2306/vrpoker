# VRChat Poker エージェント

`pamiq-core` のエージェント-環境ループ上に構築された、自律的なVRChatポーカープレイエージェントです。エージェントはVRChatのポーカーテーブルをキャプチャし、TexasSolverでGTOアクションを推論し、OSCまたはオーバーレイ経由で決定を返します。

## クイックスタート

### インストール
```bash
task install
```

### エージェントの実行
```bash
task run
```
ループ: スクリーンキャプチャ + OCRでテーブルを **観察** → `TexasSolverModel` で **思考** → OSC/オーバーレイアクチュエーターで **行動**。

## 開発

プロジェクトの管理には `Taskfile.yml` を利用したタスクランナーを使用します。以下は主要なコマンドです。

| コマンド       | 説明                                           |
|--------------|------------------------------------------------|
| `task install` | 依存関係をインストールします (`uv sync`)         |
| `task run`     | エージェントを実行します (`uv run vrpoker`)      |
| `task check`   | 静的解析、フォーマット、テストを全て実行します |

### プロジェクト構成
- `src/poker_gto/agents/`: 意思決定ロジック (`PokerAgent`)
- `src/poker_gto/environments/`: センサー (キャプチャ/OCR) とアクチュエーター (OSC/オーバーレイ)
- `src/poker_gto/models/`: 推論用 `TexasSolverModel` ラッパー
- `src/poker_gto/data/`: 共有の観測/アクション形状
- `src/poker_gto/launch.py`: ループを配線するエントリーポイント

 ## アーキテクチャドキュメント
- `docs/SETUP_AND_RUN.md` — 初期設定と実行手順- `docs/ARCHITECTURE.md` — システム図とデータフロー
- `docs/PAMIQ_TEXASSOLVER_INTEGRATION.md` — ソルバーが推論モデルとしてどのようにラップされているか
