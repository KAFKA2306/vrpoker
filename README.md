# VRChat Poker Agent

VRChat のポーカーテーブルを画面から読み取り、判断結果を入力操作へつなぐための実験的な Python プロジェクトです。

## 現在確認できる範囲

リポジトリには次の実装があります。

- `pamiq-core` の Agent / Environment / Interaction を使う実行入口
- `pamiq-vrchat.ImageSensor` を使う画面入力
- OpenCV / EasyOCR を使うカード、ボタン、ポット、スタックの認識コード
- マウス入力を送る `Clicker`
- TexasSolver CLI 用の設定生成と subprocess 呼び出し

CI で確認するのは Python の lint と既存 unit tests です。実際の VRChat セッション、OCR 精度、マウス入力、TexasSolver のビルド済み実行ファイルを使った戦略計算は CI では確認しません。

`TexasSolverModel` の実装が存在することと、実環境で正しい戦略計算が完了することは別です。後者は未検証として扱います。

## セットアップ

Python 3.12 以上と `uv`、Task が必要です。

```bash
task install
task check
```

`uv.lock` を使って依存関係を固定します。

## 実行

```bash
task run
```

ビデオ入力を明示する場合は `VRCHAT_VIDEO_SOURCE` を設定します。

```bash
export VRCHAT_VIDEO_SOURCE="rtsp://192.168.1.100:8554/live"
task run
```

カメラインデックスも指定できます。

```bash
export VRCHAT_VIDEO_SOURCE=0
task run
```

`TEXASSOLVER_PATH` を指定しない場合、実行入口はリポジトリ内の `TexasSolver/TexasSolver` を参照します。リポジトリには TexasSolver のソースコードがありますが、CI ではその実行ファイルをビルドしません。

## Windows / WSL2

Windows 用の補助スクリプトがあります。

```bash
task install:win
task run:win
```

これらは特定の Windows / WSL2 実行環境を必要とし、GitHub Actions では確認しません。

Linux 向けのシステム依存関係は次で導入できます。

```bash
task install:linux
task install
```

## デバッグ

`DEBUG_VISION=1` を設定すると、認識処理のデバッグ用フレームを `states/debug/` に保存します。

```bash
export DEBUG_VISION=1
task run
```

## 開発

```bash
# lint + tests
task check

# tests only
task test

# lint only
task lint

# lint の自動修正と format
task fix
```

## 主な構成

- `src/poker_gto/agents/` — action selection
- `src/poker_gto/environments/` — VRChat 入出力
- `src/poker_gto/models/texassolver.py` — TexasSolver CLI 呼び出し
- `src/poker_gto/vision/` — OCR / image processing
- `tests/` — unit tests
- `TexasSolver/` — TexasSolver source tree

## 未検証・未完了

- 実際の VRChat テーブルを使った end-to-end 実行
- TexasSolver のビルドと実戦略計算
- game phase と board card recognition の実環境精度
- OCR confidence に基づく誤操作防止
- Windows / WSL2 / Linux の各入力経路の実機確認
