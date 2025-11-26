# リポジトリガイドライン

## プロジェクト構成とモジュール
- コアソースは `src/poker_gto` にあります: ランチャー（`launch.py`）、エージェントロジック（`agents/poker_agent.py`）、環境IO（`environments/`）、ソルバーラッパー（`models/texassolver.py`）、共有データ形状（`data/`）。
- テストは `tests` にあります（pytest が `test_*.py` を検出）。既存の `test_smoke.py` をテンプレートとして使えます。
- 外部ソースのソルバーは `TexasSolver/` に同梱されています。実行時はビルド済みバイナリ、または `TEXASSOLVER_PATH` で指定した任意のパスを参照します。
- 追加の設計メモは `docs/`（`PAMIQ_TEXASSOLVER_INTEGRATION.md` を参照）にあります。タスク自動化は `Taskfile.yml` に定義されています。

## ビルド・テスト・開発コマンド
- 開発環境の作成: `uv sync`（uv が無い場合は `pip install -e .`）。
- ローカルでアプリを実行: `uv run vrpoker` または `uv run python -m poker_gto.launch`（下記の環境変数を利用）。
- リント: `uv run ruff check src tests`（行長100文字）。
- 自動整形: `uv run ruff format src tests`。
- テスト実行: `uv run pytest`（`tests` を `testpaths` として認識）。
- 生成物の掃除: `task clean`（`.venv` と `__pycache__` を削除）。

## コーディングスタイルと命名
- Python 3.12 をターゲット。明瞭さのため型ヒント、dataclass、Enum、`@override` を優先。
- 関数は小さく保ち、`logging` でログを出力（`launch.setup_logging` を参照）。早期バリデーションを推奨（例: `PokerAction.__post_init__`）。
- 命名: 関数/変数は snake_case、クラスは PascalCase、定数と環境キーは UPPER_SNAKE。
- 行は 100 文字以内に保ち、コミット前に ruff を実行。

## テストガイドライン
- テストは対象機能の近く、`tests/` 配下に配置し、ファイル名は `test_<feature>.py`、関数は `test_*` とする。
- pytest 形式のアサーションを使用し、実際の画面/OSC を叩かずに VRChat/TexasSolver のモック用フィクスチャを追加。
- カバレッジを追加すべき箇所: センサ前処理（`environments/sensors.py`）、ソルバーパース（`models/texassolver.py`）、エージェントの意思決定分岐（`agents/poker_agent.py`）。

## コミットとプルリクエストのガイドライン
- コミットメッセージは命令形を目指す（`add`、`fix`、`refactor`）。必要に応じてスコープを接頭辞に付ける（`agent:`、`env:`）。迷う場合は Conventional Commits（`feat:`、`fix:`、`chore:`）に従う。
- PR には以下を含める: 振る舞い変更の概要、テスト証跡（`uv run pytest` の結果）、新しい環境変数/設定デフォルト。UI/OSC の変更がある場合はスクリーンショットやログを添付。
- PR は焦点を絞り、小さくレビューしやすい差分を好む。大規模なリファクタより小さな単位を優先。

## 設定とセキュリティのヒント
- 必須環境変数: `TEXASSOLVER_PATH`（ソルバーバイナリへのパス）。任意: `VRCHAT_CAPTURE_REGION` の JSON または `top=,left=,width=,height=`。アクチュエーター経路用に `VRCHAT_OSC_IP` / `VRCHAT_OSC_PORT`。
- ソルバーバイナリ、状態ダンプ、OSC トレースのコミットを避ける。新しいシークレットはコードではなく環境変数で追加。
- キャプチャや OSC のデフォルトを変更する際は、ローカル開発用に妥当なフォールバックが残るようにする。
