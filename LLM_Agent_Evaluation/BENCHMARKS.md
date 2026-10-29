# Benchmarks Registry

本文件维护“benchmark / eval set 是什么、测什么、有什么边界”，不维护某次运行分数。

## Benchmark Card 最小字段

```text
Benchmark ID / Name
Target capability
Task / environment
Unit of evaluation
Data source
Reference / evaluator
Slices
Difficulty structure
Leakage / contamination risk
Stochasticity / repeats
Cost
Known limitations
Recommended use
Not recommended use
Related frozen experiments
```

## V0 分类

### Static LLM Benchmarks

固定 input → output，适合基础能力或受控对比。

### Interactive / Agent Benchmarks

包含 environment state、tool interaction 或多步 action；需要评估 trajectory 与执行结果。

### Regression Sets

小而稳定，覆盖已知关键能力与历史 bug；目标是阻止退化，不代表完整能力分布。

### Frozen Holdout Sets

开发期间不可参与调试，用于验证修改是否真正泛化。

### Rotating / Fresh Sets

用于降低 benchmark overfitting 和长期污染风险。

### Challenge / Hard Sets

刻意提高区分度，覆盖已知脆弱能力；不能把其分布直接解释为自然线上分布。

## 关键边界

```text
benchmark score
≠ 产品真实成功率
≠ 全能力覆盖
≠ 因果归因
```

每个 benchmark 都必须说明它支持哪些结论，以及不支持哪些结论。