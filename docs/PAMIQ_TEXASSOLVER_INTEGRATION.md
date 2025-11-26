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