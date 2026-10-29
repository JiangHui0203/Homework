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
| Judge | Anchor Agreement | Judge 与 adjudicated human / verifier anchor 的一致性 |
| Judge | Pairwise Preference Accuracy | Judge 对可靠 pairwise reference 的正确率 |
| Judge | Repeat Consistency / Flip Rate | 完全相同输入重复评分是否稳定 |
| Judge | Swap Consistency | A/B 交换位置后，内容偏好是否保持 |
| Judge | Slot-conditioned Win Rate | 候选处于不同展示位置时的条件胜率 |
| Judge | Critical-slice Error Rate | 高风险 / 关键 slice 上 Judge 错误率 |
| Judge | Human-Human Agreement | 人工 reference 本身有多一致 |
| Judge | Judge-Human Agreement | Judge 与人工判断有多一致 |
| Judge | Score Offset / MAE | Judge 是否系统偏高/偏低、误差有多大 |
| Calibration | Calibration Error / Brier-style measures | confidence 与实际正确性的匹配 |
| Regression | Paired Net Win / Loss | 新旧系统在同任务上的净改善/退化 |

## Judge metric 使用提醒

### Agreement ≠ Correlation

- agreement 关心逐样本是否做出相同判断；
- correlation 关心变化趋势或排序是否一致；
- 二者都不能单独证明 evaluator validity。

### Swap Consistency

对于同一 pair：

```text
(A, B) -> A
(B, A) -> A
```

内容偏好一致；如果仅交换位置就改变 winner，则记为 swap inconsistency。必须保留 tie / abstain 规则，不能把它们悄悄算成一致或错误。

### Repeat Flip Rate

同一 Judge contract、同一输入重复执行时，最终 label 改变的比例。unit 应明确是 judgment pair、task 还是 criterion judgment。

### Human Agreement

必须说明 human reference 是：

```text
single annotator
majority vote
mean / median score
expert adjudication
raw rating distribution
```

否则“Judge-human agreement”没有明确分母与 reference construction。

## 维护规则

- 任何百分比都要能回答“分母是什么”。
- 失败消耗默认不能从成本计算中消失。
- metric 定义与 release threshold 分离。
- aggregate metric 必须保留可解释 slice。
- 单个 metric 不能承担它没有测量的概念。
- Judge reliability 至少同时看 validity、repeatability、bias robustness 和 critical-slice behavior；不要用单个相关系数代替完整结论。
