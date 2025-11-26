# VRChat Poker エージェント

`pamiq-core` のエージェント-環境ループ上に構築された、自律的なVRChatポーカープレイエージェントです。エージェントはVRChatのポーカーテーブルをキャプチャし、TexasSolverでGTOアクションを推論し、マウスクリック経由で決定を実行します。

## クイックスタート

### インストール
```bash
task install
```

### エージェントの実行
```bash
task run
```
ループ: スクリーンキャプチャ + OCRでテーブルを **観察** → `TexasSolverModel` で **思考** → マウスクリックアクチュエーターで **行動**。

## アーキテクチャ

### PAMIQエコシステム統合

このプロジェクトは以下の`pamiq`ライブラリを使用します：

- **pamiq-core**: エージェント-環境ループのコアフレームワーク
- **pamiq-io**: ビデオ、オーディオ、マウス入出力
- **pamiq-vrchat**: VRChat特化のセンサー（ImageSensor）
- **pamiq-recorder**: セッション記録

### コンポーネント

- **Agent** (`src/poker_gto/agents/poker_agent.py`): GTO戦略の決定ロジック
- **Environment** (`src/poker_gto/environments/vrchat_poker.py`): VRChatとのインタラクション
- **Sensors**: `pamiq-vrchat.ImageSensor` でゲーム画面をキャプチャ
- **Actuators**: `Clicker` でポーカーアクションボタンをクリック
- **Model** (`src/poker_gto/models/texassolver.py`): TexasSolverのラッパー

## 環境設定

### ビデオソース設定

エージェントはデフォルトで「OBS Virtual Camera」を検索します。別のソースを使用する場合は、`VRCHAT_VIDEO_SOURCE`環境変数を設定してください：

```bash
# カメラインデックスを指定（Windowsの場合）
export VRCHAT_VIDEO_SOURCE=0

# RTSPストリームを指定（WSL2からWindowsのOBSにアクセスする場合）
export VRCHAT_VIDEO_SOURCE="rtsp://192.168.1.100:8554/live"

# その後エージェントを実行
task run
```

### Windows環境

Windowsでは`pydirectinput`を使用してマウス操作を実行します。これは最も確実な方法です。

1. OBS Studioをインストールし、仮想カメラを有効化
2. VRChatを起動
3. `task run`でエージェントを起動

### WSL2環境

WSL2では以下の2つのアプローチがあります：

#### アプローチ1: Windows OBSからのRTSPストリーミング（推奨）

1. Windows側でOBS StudioのRTSPプラグインを設定
2. WSL2から以下のように設定：
```bash
export VRCHAT_VIDEO_SOURCE="rtsp://<WindowsのIPアドレス>:8554/live"
task run
```

#### アプローチ2: Linuxネイティブモード

```bash
# システム依存関係とinputtinoのインストール
task install:linux

# inputtinoを使用してマウス入力を送信
task run
```

**注意**: WSL2からWindowsアプリケーション（VRChat）への入力送信には追加設定が必要です。本番環境ではWindows上での直接実行を推奨します。

## 現在の実装状態

### ✅ 完了
- [x] `pamiq-core`統合（Agent, Environment, Interaction）
- [x] 依存関係のインストールとセットアップ
- [x] ビデオソース設定システム（`VRCHAT_VIDEO_SOURCE`）
- [x] クロスプラットフォーム`Clicker`アクチュエーター（Windows/Linux）
- [x] `TexasSolverModel`のラッパー実装

### 🚧 実装予定（モックアップ禁止、必ず実装）
- [ ] **画像認識**: カード、ポット、スタックのOCR
- [ ] **ボタン検出**: Fold/Call/Raiseボタンの座標特定
- [ ] **ゲーム状態パース**: 実際の`PokerObservation`の生成
- [ ] **TexasSolver統合**: 実際のGTO計算の実行
- [ ] **エラーハンドリングの削除**: 失敗時は即座にクラッシュ（仕様）

## 開発

詳細は以下を参照：
- [アーキテクチャ](docs/ARCHITECTURE.md)
- [TexasSolver統合](docs/PAMIQ_TEXASSOLVER_INTEGRATION.md)

### テスト実行
```bash
uv run pytest tests/
```

### Lint & Format
```bash
task fix
```

## 依存関係

- Python 3.12+
- pamiq-core 0.6.0
- pamiq-io 0.6.1
- pamiq-vrchat 0.1.0
- pamiq-recorder 0.3.0
- inputtino-python 0.1.0（Linux）
- TexasSolver（オプション）
