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
    -   これは、致命的な問題なので、windows OBSから起動し、必ず、解決します。モックアップ禁止です。エラーハンドリング禁止です。必ず必要です。
    -   そもそも、WSL2経由では、vrchat起動しないので、windowsでの動作を前提とします。

2.  **OSCマッピング (一時的措置)**:
    -   現在、ポーカーのアクションはVRChatの標準動作ボタンにマッピングされています（クラッシュ回避のため）この考え方は根本的な誤りです。Pamiq-coreを用いて解決しなければなりません。また、ポーカーのアクションは、クリック、あるいは、長押しで解決します。クリックすべき場所は視界から取得します。エラーハンドリング禁止です。モックアップ禁止です。必ず必要です。
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
