# セットアップと実行ガイド

VRChat Poker エージェントを pamiq-core の流儀で動かすための初期設定と基本運用手順をまとめます。
前提や用語は pamiq-core に準拠します。

## 前提環境
- Python 3.12 以上
- uv がインストールされていること（`pip install uv` でも可）
- VRChat PC クライアント（OSC 有効化）
- TexasSolver バイナリへのパス（`TEXASSOLVER_PATH` で指定。未指定なら `./TexasSolver/TexasSolver` を参照）
- OCR 用の Tesseract エンジンが OS に入っていること（`pytesseract` の実行に必要）

## 初期セットアップ
1. リポジトリを取得して移動する
   ```bash
   git clone <your-fork-or-origin> vrpoker
   cd vrpoker
   ```
2. 依存をインストールする（pamiq-core 0.6 系を含む）
   ```bash
   task install
   ```
   `uv sync` が `.venv` を作成し、必要パッケージを解決します。
3. TexasSolver のパスを環境変数に設定する（必要なら）
   ```bash
   export TEXASSOLVER_PATH="/absolute/path/to/TexasSolver"
   ```

## 実行（pamiq-core ランチャー）
- タスクランナー経由で起動
  ```bash
  task run
  ```
- 直接 uv で起動
  ```bash
  uv run vrpoker
  ```
起動後は `http://localhost:8391` で pamiq-console から接続できます。
```bash
pamiq-console --host localhost --port 8391
```

## 主要タスク（開発用）
- 静的解析・フォーマット・テスト一括: `task check`
- 単体テストのみ: `uv run pytest`
- Lint のみ: `uv run ruff check src tests`

## 環境変数
- `TEXASSOLVER_PATH`
  TexasSolver バイナリへのフルパス。未設定ならカレントの `TexasSolver/TexasSolver` を使用。
- `VRCHAT_CAPTURE_REGION`
  画面キャプチャ矩形。JSON 例: `{"top":120,"left":80,"width":1280,"height":720}`。
  または `top=120,left=80,width=1280,height=720` のカンマ区切り形式。
- `VRCHAT_OSC_IP` / `VRCHAT_OSC_PORT`
  OSC 送信先。デフォルトは `127.0.0.1:9000`。

## よくある確認ポイント
- solver が見つからない: `TEXASSOLVER_PATH` を正しいバイナリに向ける。
- OCR 精度が低い: `VRCHAT_CAPTURE_REGION` をテーブル領域に合わせて調整する。
- OSC が届かない: VRChat 側で OSC 有効化、IP/PORT の一致を確認する。

## 参考
- pamiq-core の概念や API: pamiq-core 公式ドキュメント
- TexasSolver 連携の詳細: `docs/PAMIQ_TEXASSOLVER_INTEGRATION.md`
- 全体構成: `docs/ARCHITECTURE.md`