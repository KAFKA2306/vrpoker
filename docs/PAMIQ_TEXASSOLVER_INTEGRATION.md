# pamiq-core と TexasSolver の統合

このドキュメントは、`TexasSolver` を `pamiq-core` エコシステムへ統合する方法を説明します。

## InferenceWrappedModel

`TexasSolver` は単体スクリプトではなく `pamiq_core.InferenceWrappedModel` として組み込まれ、
`pamiq` フレームワーク内で標準的な推論エンジンとして扱われます。

### 実装のポイント

`TexasSolverModel` クラスは TexasSolver CLI をラップします。

1. **入力**: 現在のゲーム状態（ホールカード、ボード、ポット、スタック）を含む `PokerObservation` を受け取る。
2. **処理**:
    - TexasSolver 用の一時設定ファイルを生成。
    - TexasSolver バイナリをサブプロセスとして実行。
    - TexasSolver からの JSON 出力をパース。
3. **出力**: アクションと頻度を対応付けた戦略ディクショナリを返す。

### このアプローチの利点

- **非同期実行**: `pamiq-core` が推論を別スレッドで実行し、重い計算でもメインループをブロックしない。
- **モジュール性**: エージェントは「戦略を受け取る」ことだけを知ればよく、将来のソルバー差し替えが容易。
- **状態管理**: `pamiq-core` がモデルのライフサイクルと状態保持を担当。

## コード例

```python
class TexasSolverModel(InferenceWrappedModel[PokerObservation, dict[str, float]]):
    def infer(self, input_data: PokerObservation) -> dict[str, float]:
        # ... generate config ...
        # ... run solver ...
        # ... parse result ...
        return strategy
```
