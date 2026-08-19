# VRChat Poker Agent

VRChat のポーカーテーブルを対象に、画面入力・状態表現・戦略計算・入力操作を試すための実験的な Python プロジェクトです。

## 現在の実装境界

現在のコードには次の部品があります。

- `pamiq-core` の Agent / Environment / Interaction を使う実行入口
- `pamiq-vrchat.ImageSensor` を初期化する画面入力経路
- OpenCV / EasyOCR を使うカード、ボタン、ポット、スタック認識モジュール
- `pamiq-io` の `InputtinoMouseOutput` 初期化
- TexasSolver CLI 用の設定生成と subprocess 呼び出し

ただし、これらは現在 end-to-end では接続されていません。

- `VRChatPokerEnvironment.observe()` はフレームを読み取りますが、認識モジュールを呼び出さず、game phase、pot、stack、position には固定の placeholder 値を返します。
- `VRChatPokerEnvironment.affect()` は action をログ出力しますが、現在はマウスクリックを送信しません。
- `TexasSolverModel` はCLI wrapperを持ちますが、CIではTexasSolver executableをbuild・実行しません。
- sensor / mouse output の初期化失敗時は処理を継続するため、実デバイスが接続されていること自体も起動成功だけでは証明できません。

したがって、現在のリポジトリを「自律ポーカーAgent」や「GTO計算済み」とは扱いません。

## セットアップ

Python 3.12 以上と `uv`、Task が必要です。

```bash
task install
task check
```

`uv.lock` を使って依存関係を固定します。

Linuxで`inputtino`のbuildに必要なsystem packageを入れる場合は次を使います。

```bash
task install:linux
task install
```

## 実行

```bash
task run
```

ビデオ入力を明示する場合は `VRCHAT_VIDEO_SOURCE` を設定できます。

```bash
export VRCHAT_VIDEO_SOURCE=0
task run
```

URLも指定できます。

```bash
export VRCHAT_VIDEO_SOURCE="rtsp://192.168.1.100:8554/live"
task run
```

`TEXASSOLVER_PATH` を指定しない場合はリポジトリ内の `TexasSolver/TexasSolver` を参照します。リポジトリにはTexasSolverのsource treeがありますが、CIでは実行ファイルをbuildしません。

Windows / WSL2 の実機起動経路は現在検証済みの手順として提供していません。

## デバッグ

`DEBUG_VISION=1` を設定すると、取得できたフレームを `states/debug/` に保存します。

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

CIはlocked dependency sync、Ruff、既存unit tests、clean working treeを確認します。

## 主な構成

- `src/poker_gto/agents/` — action selection
- `src/poker_gto/environments/` — VRChat 入出力
- `src/poker_gto/models/texassolver.py` — TexasSolver CLI wrapper
- `src/poker_gto/vision/` — OCR / image processing
- `tests/` — unit tests
- `TexasSolver/` — TexasSolver source tree

## 未検証・未完了

- 認識モジュールを `observe()` の実game stateへ接続すること
- 認識confidence不足時に入力操作を停止すること
- actionを実際のVRChat UI clickへ接続すること
- TexasSolverのbuildと実戦略計算
- 実際のVRChatテーブルを使ったend-to-end実行
- Windows / WSL2 / Linux の各入力経路の実機確認
