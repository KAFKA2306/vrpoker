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

詳細は以下を参照：
- [アーキテクチャ](docs/ARCHITECTURE.md)
- [TexasSolver統合](docs/PAMIQ_TEXASSOLVER_INTEGRATION.md)

## 依存関係

- Python 3.12+
- pamiq-core 0.6.0
- TexasSolver（オプション）
— ソルバーが推論モデルとしてどのようにラップされているか
