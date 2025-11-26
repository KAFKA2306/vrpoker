# pamiq-core と TexasSolver の統合

TexasSolver を `pamiq-core` エコシステムへ統合する方法。

## InferenceModel

`TexasSolver` は `pamiq_core.model.interface.InferenceModel` として組み込まれ、pamiq フレームワーク内で標準的な推論エンジンとして扱われます。

### 実装のポイント

`TexasSolverModel` クラスは TexasSolver CLI をラップします。

1. **入力**: `infer(*args, **kwds)` で `PokerObservation` を受け取る
2. **処理**:
    - TexasSolver 用の一時設定ファイルを生成
    - TexasSolver バイナリをサブプロセスとして実行
    - TexasSolver からの JSON 出力をパース
3. **出力**: アクションと頻度を対応付けた戦略ディクショナリ `dict[str, float]` を返す

### このアプローチの利点

- **非同期実行**: pamiq-core が推論を別スレッドで実行し、重い計算でもメインループをブロックしない
- **モジュール性**: エージェントは「戦略を受け取る」ことだけを知ればよく、将来のソルバー差し替えが容易
- **状態管理**: pamiq-core がモデルのライフサイクルと状態保持を担当

## コード例

```python
class TexasSolverModel(InferenceModel):
    def infer(self, *args: Any, **kwds: Any) -> dict[str, float]:
        input_data = args[0] if args else kwds.get("input_data")
        # ... generate config ...
        # ... run solver ...
        # ... parse result ...
        return strategy  # {"fold": 0.3, "call": 0.5, "raise": 0.2}
```

