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
| Recovery | First-pass Success Rate | 无需恢复即可完成的比例 |
| Recovery | Recovery Opportunity Rate | 多频繁进入可恢复异常路径 |
| Recovery | Recovery Success Rate | 在有效恢复机会中，多少最终恢复成功 |
| Recovery | Recovery Cost | 恢复付出的额外 token / latency / calls |
| Recovery | Safe Stop Appropriateness | 应停止时是否停止、可继续时是否过度停止 |
| Tool | Tool Selection Accuracy | 是否在正确 opportunity 选择了正确 tool / no-tool |
| Tool | Argument / Constraint Accuracy | 工具关键参数和约束是否正确 |
| Tool | Tool Execution Success Rate | 工具调用是否在执行层成功完成 |
| Tool | Tool Result Grounding Rate | 后续关键结论是否被有效 observation 支持 |
| Tool | Unnecessary Tool Call Rate | 无必要 / 无信息增益调用的比例 |
| State | State Isolation Violation Rate | 是否发生非预期跨 episode / condition 状态泄漏 |
| Memory | Memory Retrieval Coverage | eligible opportunity 中有多少真正发生 retrieval / injection |
| Memory | Stale / Invalid Memory Hit Rate | 检索到过期、来源不允许或 contract 不兼容 memory 的比例 |
| Memory | Memory Net Benefit | paired runs 中改善与退化的净 outcome 差 |
| Trajectory | Checkpoint Completion Rate | 有多少 episode 到达有效任务 milestone |
| Trajectory | Conditional Stage Success | 到达某阶段后，向下一阶段有效推进的比例 |
| Trajectory | First-Failure Distribution | 关键失败集中在哪个阶段 |
| Trajectory | Loop / Stall Rate | 长链中失去有效进展的 episode 比例 |
| Trajectory | Post-failure Waste | 首次不可恢复失败后继续消耗的 token / calls / time |
| Stability | Repeat Consistency | 同任务重复运行是否稳定 |
| Budget | Budget Violation Rate | 超出冻结 token / call / time / retry 预算的比例 |
| Budget | Success under Fixed Budget | 在统一预算约束下的任务成功能力 |
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

## Agent metric 使用提醒

### Tool Selection 的 denominator 是 opportunity，不只是 actual calls

错误定义：

```text
correct tool calls / actual tool calls
```

会让“本来应该调用工具但 Agent 直接编答案”的运行从分母消失。

更合理的是先冻结：

```text
eligible tool-decision opportunities
allowed tool set / no-tool policy
```

再计算 selection correctness。

### Tool Execution ≠ Tool Correctness

```text
API 200
SQL executed
function returned
```

只说明执行层成功，不说明：

```text
selected right tool
arguments correct
result semantically relevant
observation correctly interpreted
final answer grounded
```

所以 tool selection、arguments、execution、grounding 不应压成同一个数字。

### Recovery Success 的 denominator 必须写清

至少区分：

```text
successful recovery / recovery opportunities
successful recovery / recovery attempts
```

两者分别回答“整体恢复能力”和“已经尝试之后的有效性”。

### Recovered Success 不能把 First-pass Quality 隐藏掉

产品 outcome 可以把 first-pass success 与 recovered success 都算 valid success；诊断时仍应分别报告，否则候选系统可能靠更多 retry 掩盖首轮质量下降。

### Safe Stop 不是越多越好

需要同时关心：

```text
需要停止时是否停
本可继续时是否过度停止
```

小样本时优先给出 confusion table；规模足够时可报告 precision / recall 风格指标。

### Memory Retrieval Coverage ≠ Memory Benefit

建议分开记录：

```text
eligible opportunity
retrieved
injected
model actually saw it
behavior changed
affected outcome
```

高 retrieval coverage 只能证明机制活跃，不能证明能力提升。

### Checkpoint 指标必须 exposure-aware

对于 Stage k，至少同时报告：

```text
reached Stage k / all eligible episodes
successful Stage k transition / episodes that reached Stage k
```

否则只看幸存到后期的少量任务会产生 survivorship bias。

### Budget 越少不一定越高效

更少 calls / tokens 也可能是因为更早失败。

因此预算指标要和：

```text
Task Success
First-Failure Stage
Cost per Valid Success
Success under Fixed Budget
```

联合解释。

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
- Agent 过程指标必须服务于 diagnosis、attribution、reliability、budget 或 replay；无决策用途的 telemetry 不自动升级成正式 metric。
- Judge reliability 至少同时看 validity、repeatability、bias robustness 和 critical-slice behavior；不要用单个相关系数代替完整结论。
