# Visual Derivatives

本目录保存从 F1–F14 Mermaid semantic source 派生的 presentation assets。

规范：

- [`Publication Visual Derivative Spec`](../00_Publication_Visual_Derivative_Spec.md)
- [`Master Figure System`](../00_Master_Figure_System.md)
- [`Figure Design Contract`](../00_Figure_Design_Contract.md)

固定关系：

```text
../figures/F1...F14.md
= semantic source of truth

./publication/
= static book / PDF derivative

./slides/
= presentation / progressive reveal derivative

./quick_reference/
= interview / share-card derivative
```

任何 derivative 必须记录：

```text
figure_id
semantic_source
semantic_source_sha
export_type
export_version
```

如果 semantic relation 需要变化，先修改 Mermaid source，再重新导出 derivative。

## Current Assets

### Publication

- `F1_Learning_System_Overview.svg` — first production sample
