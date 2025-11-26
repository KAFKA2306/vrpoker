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

## 🐧 Linux / WSL2 環境での注意点

WSL2などの仮想環境では、以下の制限があります：

1.  **Blind Mode (カメラ無効)**:
    -   WSL2ではOBS仮想カメラのドライバ (`v4l2loopback`) が動作しないため、エージェントは**視覚情報なし**で起動します。
    -   ゲーム画面が見えないため、OCRや画像認識は機能しません。

2.  **OSCマッピング (一時的措置)**:
    -   現在、ポーカーのアクションはVRChatの標準動作ボタンにマッピングされています（クラッシュ回避のため）：
        -   **Fold** -> `Jump`
        -   **Check/Call** -> `Run`
        -   **Bet/Raise** -> `MoveForward`

### Linuxでのインストール

```bash
# システム依存関係とinputtinoのインストール
task install:linux
```

## 開発

詳細は以下を参照：
- [アーキテクチャ](docs/ARCHITECTURE.md)
- [TexasSolver統合](docs/PAMIQ_TEXASSOLVER_INTEGRATION.md)

## 依存関係

- Python 3.12+
- pamiq-core 0.6.0
- TexasSolver（オプション）
— ソルバーが推論モデルとしてどのようにラップされているか
