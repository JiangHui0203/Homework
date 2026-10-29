# Metrics Registry

> Metric 不只是一个公式。每个正式 metric 都必须定义 unit、denominator、aggregation、failed/missing handling 与 interpretation boundary。

## Metric Card 最小字段

```text
Metric ID / Name
Question it answers
Definition / Formula
Unit of analysis
Numerator / Denominator
Aggregation
Direction ↑ / ↓
Failed / missing run handling
Uncertainty reporting
What it measures
What it does NOT measure
Failure modes
Recommended slices
Related metrics
VeriAgent example
```

## V0 Registry

| 类别 | Metric | 主要问题 |
|---|---|---|
| Outcome | Task Success Rate | 任务是否完成 |
| Outcome | Exact / Reference Correctness | 输出是否与可靠参考一致 |
| Outcome | Partial Credit | 复杂任务完成到什么程度 |
| Reliability | False Accept / False Confidence Rate | 错误答案是否被系统错误放行 |
| Reliability | Safe Stop Rate | 数据/证据不足时能否正确停止 |
| Recovery | Recovery Success Rate | 首次失败后是否恢复 |
| Recovery | Recovery Cost | 恢复付出的额外 token / latency / calls |
| Tool | Tool Selection Accuracy | 是否选对工具 |
| Tool | Argument / Constraint Accuracy | 工具参数和约束是否正确 |
| Trajectory | First-Failure Distribution | 关键失败集中在哪个阶段 |
| Stability | Repeat Consistency | 同任务重复运行是否稳定 |
| Cost | Tokens per Valid Success | 包含失败消耗后的单位成功 token |
| Cost | Calls per Valid Success | 单位成功请求数 |
| Latency | End-to-End P50/P95 | 完整任务耗时分布 |
| Judge | Human Agreement | evaluator 与人工的一致性 |
| Judge | Pairwise Preference Accuracy | judge 对 pairwise gold 的正确率 |
| Calibration | Calibration Error / Brier-style measures | confidence 与实际正确性的匹配 |
| Regression | Paired Net Win / Loss | 新旧系统在同任务上的净改善/退化 |

## 维护规则

- 任何百分比都要能回答“分母是什么”。
- 失败消耗默认不能从成本计算中消失。
- metric 定义与 release threshold 分离。
- aggregate metric 必须保留可解释 slice。
- 单个 metric 不能承担它没有测量的概念。