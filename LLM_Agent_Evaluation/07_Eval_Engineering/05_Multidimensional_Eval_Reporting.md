# Q34 如何同时报告 Quality、Cost、Latency、Stability，而不是只优化单一准确率？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 3 / Part 6 / Part 7
- Related Patterns: P04 Slice Before Aggregate; P09 Cost per Valid Success
- Related Metrics: Task Success, Tokens per Valid Success, P50/P95 Latency, Repeat Consistency, Budget Violation
- Related Case: VeriAgent Data Agent

## 30-second answer

LLM / Agent 系统不是单指标系统。准确率提高如果同时带来 3 倍成本、P95 latency 超 SLO、稳定性下降，不能简单写成“更好”。

我会把结果报告成一个**多维 scorecard**：

```text
Quality
Reliability / Safety
Cost
Latency
Stability
Budget / Completeness
```

决策时优先用：

```text
hard constraints
+ Pareto / trade-off
```

而不是未经业务依据把所有维度加权成一个神秘 composite score。

## 90-second answer

最小报告至少包含：

```text
Quality:
  task success / critical slices

Reliability:
  false accept / safe stop / recovery

Cost:
  total tokens
  tokens per valid success
  tool / model calls

Latency:
  end-to-end P50 / P95

Stability:
  repeat consistency
  flaky task count

Budget:
  token / call / retry violations

Completeness:
  planned vs completed runs
```

其中几个边界特别重要：

```text
fewer tokens
≠ more efficient
```

如果是因为更早失败；

```text
lower mean latency
≠ better tail latency
```

Agent 部署通常更关心 P95/P99；

```text
recovered success
≠ first-pass success
```

恢复成功可能以更多成本换来。

所以推荐先定义硬门槛，例如 critical failure=0、P95<3s、budget violation=0；在可行集合中再比较 quality / cost Pareto。

## Full reasoning

### 1. 系统质量是 Vector，不是 Scalar

可把一个系统表示为：

```text
M =
(
  quality,
  reliability,
  cost,
  latency,
  stability
)
```

两个系统可能：

```text
A: quality 更高，cost 更高
B: quality 稍低，latency 更好
```

没有业务约束时，不能仅凭一个 overall score 宣称绝对胜负。

## 2. Quality

至少区分：

```text
overall task success
critical-slice success
first-pass success
recovered success
```

开放任务还可能有：

```text
rubric quality
grounding
human preference
```

但必须和 evaluator reliability 一起解释。

## 3. Cost

不要只报成功样本平均 token。

推荐：

```text
total eval tokens
tokens / valid success
calls / valid success
recovery overhead
failed-path cost
```

定义：

```text
Tokens per Valid Success
=
all eligible run tokens
/
valid successes
```

失败消耗留在分子里。

## 4. Latency

Agent latency 常是长尾分布。

至少：

```text
P50
P95
```

必要时：

```text
P99
timeout rate
```

mean latency 很容易被少数极慢/极快 case 误导。

还要明确：

```text
端到端 latency
vs
model latency
vs
tool latency
```

## 5. Stability

同一 task 重复运行：

```text
success success failure
```

和：

```text
success success success
```

平均成功率可能接近，但部署可预测性不同。

可报告：

```text
repeat consistency
all-pass task rate
all-fail task rate
flaky task rate
```

## 6. Budget

Agent 常有：

```text
max tokens
max model calls
max tool calls
max retries
max wall time
```

所以应该独立报告：

```text
Budget Violation Rate
Success under Fixed Budget
```

否则一个候选可能通过更多 retry 买来成功。

## 7. Completeness

任何 scorecard 都应先写：

```text
planned
completed
aborted
invalid
```

因为 incomplete experiment 的成本/质量分布可能有 selection bias。

## 8. Pareto 思维

如果 candidate：

```text
quality ↑
cost ↑
latency ↑
```

不是简单的“提升”或“退化”。

应该问：

> 对目标 deployment contract，额外 quality 是否值得成本和 latency？

如果一个系统在所有关键维度都不差，并至少一个更好，它可以说 Pareto-dominates。

否则是 trade-off。

## 9. Hard Constraint + Optimization

工程上常比 composite score 更清晰：

```text
Hard:
  critical false accept = 0
  P95 latency <= 3s
  budget violations = 0

Then optimize:
  maximize success
  minimize cost / valid success
```

这样 release rule 可解释、可审计。

## 10. Composite Score 的风险

例如：

```text
0.7 * quality
- 0.2 * cost
- 0.1 * latency
```

权重往往没有可解释业务依据，而且 scale 改变就会改变结论。

Composite 不是禁用，但必须有：

```text
明确 utility model
稳定 normalization
业务认可的权重
sensitivity analysis
```

否则优先分维度报告。

## 11. Candidate 与 Baseline 应同条件比较

成本和 latency 对比要尽量冻结：

```text
same tasks
same environment
same budget
same evaluator
same load condition
```

不同时间、不同 provider load 的 latency 不能轻易归因给算法。

## 12. 一个最小 Scorecard

| Dimension | Metric | Baseline | Candidate | Gate |
|---|---|---:|---:|---|
| Quality | Task Success | | | |
| Reliability | False Accept | | | |
| Cost | Tokens / Valid Success | | | |
| Latency | P50 / P95 | | | |
| Stability | Repeat Consistency | | | |
| Budget | Violation Rate | | | |
| Completeness | Completed / Planned | | | |

最终 Decision 应说明：

```text
which hard gate failed
which dimensions improved
what trade-off remains
```

## Evaluation design

正式 comparison 之前冻结：

```text
primary quality metric
critical reliability gates
cost accounting rule
latency scope
stability metric
budget
decision rule
```

结束后再填数据，不能根据结果重新发明权重。

## Common wrong answers

### 错误 1：accuracy 高就是更优系统

可能成本、latency、false accept 都更差。

### 错误 2：tokens 少就是更高效

可能只是更早失败。

### 错误 3：只报平均 latency

会隐藏 tail latency。

### 错误 4：recovered success 和 first-pass success 完全一样

产品层可能都成功，但 reliability / cost 结构不同。

### 错误 5：把多个指标随便加权成一个分数

如果没有稳定 utility model，这个总分可解释性很差。

## Counterexample / boundary

离线纯学术 benchmark 有时只关心 quality，但只要用户讨论 deployment、Agent workflow 或 test-time compute，cost / latency / stability 就已经是 evaluation object，而不是“附加信息”。

## VeriAgent example

VeriAgent challenge 报告同时保留 correctness、错误放行、Token、单位成功 Token、P50/P95 latency 和重复稳定性。候选 memory 在保留测试中从 29/36 到 30/36，但总 Token 从 70,984 增到 77,934，单位成功 Token 也上升。即使不讨论因果归因，这也说明：

```text
quality point estimate
```

不能脱离：

```text
cost + stability + latency
```

单独下结论。

更关键的是，失败更早也可能减少后续请求，因此“调用更少”必须和成功率、first-failure stage 联合解释。

## Follow-up questions

- P95 latency gate 应该按整个 task 还是单次 model call？
- cost / valid success 是否应该包括 infra abort？
- 如何比较 recovered success 与 first-pass success 的 utility？
- Pareto frontier 怎么用于模型/Agent 配置选择？
- composite score 什么时候是合理的？

## Evidence of mastery

达到 S4 时，应能给一个 Agent version comparison：

1. 定义多维 scorecard；
2. 解释每个分母；
3. 区分 mean 与 tail latency；
4. 包含失败成本；
5. 报告 repeat stability；
6. 设 hard deployment constraints；
7. 给出 trade-off / Pareto 结论而不是只看 accuracy。

## Related knowledge

- [Q04 Metric Design](../01_LLM_Evaluation/03_Metric_Design.md)
- [Q14 Recovery Evaluation](../03_Agent_Evaluation/03_Recovery_and_Graceful_Degradation.md)
- [Q16 Long-Horizon Evaluation](../03_Agent_Evaluation/05_Long_Horizon_Agent_Evaluation.md)
- [Q25 Improvement Credibility](../06_Statistics_and_Experiment_Design/02_Is_the_Improvement_Credible.md)
- [Metrics Registry](../METRICS.md)
