# Q19 平均分变差时，如何用 slice 找出真正退化的能力？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 4 / Part 6 / Part 7
- Related Patterns: P03 Paired Same-Task Comparison, P04 Slice Before Aggregate, P05 Frozen Core + Rotating Hard Set

## 30-second answer

总体平均分只告诉你“发生了变化”，不能告诉你“哪个能力退化”。Regression diagnosis 应先固定 comparable population，再从预定义或证据驱动的 slice 看：**task family、difficulty、tool/stage、failure type、memory/recovery path、length、language、environment condition**，同时报告每个 slice 的样本量、baseline、candidate、paired delta 和 uncertainty。

不能只寻找最差 slice；必须防止样本过小、slice mix 变化、重复试验挑显著结果和 Simpson's paradox。

## 90-second answer

看到 overall 从 82% 降到 79%，我先问：同一批 task 吗？失败/abort 处理一致吗？evaluator/version 一致吗？如果 comparable，再做 paired slice table：

```text
slice | n | baseline | candidate | paired win | paired loss | delta
```

优先检查预注册 capability slices 和 first-failure slices，再下钻到新发现的 failure cluster。一个 slice 只有 2 题、掉了 50 个点不能直接宣称能力退化；要把它作为 hypothesis，扩样本或回放。

真正可行动的 regression 结论应是：**哪类输入、在哪个阶段、以什么 failure mechanism 退化、影响多大、能否稳定复现。**

## 1. Aggregate 为什么会骗人

总体分数：

```text
sum(success) / sum(eligible runs)
```

混合了多个 task distribution。

即使每个 slice 内都没有变差，只要样本构成变化，总体也可能变化；反之，总体持平也可能掩盖一类严重退化和另一类改善。

## 2. Slice 的四类来源

### A. Capability slice

```text
reasoning
retrieval
tool-use
SQL aggregation
instruction following
safe stop
```

### B. Task / data slice

```text
difficulty
language
length
schema complexity
number of tools
long-horizon depth
```

### C. Runtime / path slice

```text
memory hit / no-hit
recovery / no-recovery
tool family
stage reached
budget bucket
```

### D. Failure slice

```text
first meaningful failure layer
false accept
argument error
state leakage
loop/stall
answer synthesis
```

预定义 slice 用于稳定比较；post-hoc failure slice 用于 diagnosis，但不能假装是预注册 confirmatory result。

## 3. Regression triage 的顺序

### Step 1 — Verify comparability

先排除：

```text
task set changed
evaluator changed
denominator changed
infra abort handling changed
tool/environment version changed
random repeat count changed
```

### Step 2 — Paired outcome table

同 task / repeat 上记录：

```text
W = baseline wrong -> candidate correct
L = baseline correct -> candidate wrong
BB = both correct
FF = both wrong
```

总体 delta 之外，先看 loss 集合是谁。

### Step 3 — Slice losses

对 loss cases 按预定义维度切片，但同时保留完整 denominator，避免只研究失败集后错误推断总体风险。

### Step 4 — Trace diagnosis

在可疑 slice 内进一步看：

```text
first meaningful failure
recovery behavior
tool / state / verifier events
```

### Step 5 — Reproduce

挑代表 case replay / fixture 化，验证 regression 是否稳定。

## 4. Slice table 最少字段

```text
slice_name
slice_definition
n_tasks / n_runs
baseline metric
candidate metric
paired wins
paired losses
delta
uncertainty / caveat
first-failure distribution
cost / latency if relevant
```

没有 `n` 的 slice percentage 基本不可审计。

## 5. Micro 与 macro

### Micro

所有运行放在一起：大 slice 权重大。

### Macro

先算每个 slice / task family，再平均：每组更接近等权。

二者回答不同问题。

如果 production natural frequency 很重要，可用 weighted estimate；但权重必须预先说明，不能为了得到更好数字事后换权重。

## 6. Simpson's paradox

假设 candidate 在 easy 和 hard 两组内都略好，但本轮 candidate 恰好遇到更多 hard 样本，总体可能更差。

因此 regression 前必须检查：

```text
population composition
slice weights
paired task identity
```

paired same-task evaluation 是最直接的控制方式之一。

## 7. Small-n trap

```text
slice A: 1/2 -> 0/2
```

下降 50pp，但证据极弱。

正确写法：

```text
observed regression signal on 2 cases
needs expansion / replay
```

而不是：

```text
能力下降 50%
```

## 8. Multiple slicing trap

如果你切：

```text
20 task families
5 difficulty buckets
8 lengths
6 tools
10 failure types
```

总会出现极端小组。

所以应区分：

```text
pre-registered slices -> confirmatory
post-hoc slices        -> exploratory
```

后者用于生成下一轮 hypothesis / hard set，不直接当最终证据。

## 9. Slice 与 root cause 不等价

发现：

```text
long tasks regression -12pp
```

不等于 root cause 是“上下文太长”。

长任务可能只是 proxy：

```text
更多 tool calls
更多 schema joins
更多 recovery opportunities
更高 budget pressure
```

还需要 Q17 trajectory evidence。

## 10. VeriAgent example

Olist challenge 的 task family 已冻结为：

```text
payment_grain
customer_identity
join_fanout
time_scope
```

这种预定义 family slice 比在结果出来后临时按错误样本编组更适合作为稳定 regression 维度。

开发集两条失败都出现在多表相关任务，但 failure review 进一步发现实际机制不同：一条是把 child-row eligibility 错放到 parent table，另一条是 alias scope 错误。

所以正确流程是：

```text
family slice 提供定位线索
→ trace diagnosis 分离具体 failure mechanism
```

不能因为“都在多表题”就归为同一个 root cause。

## 11. 一个实用 regression report

```text
Overall paired delta
↓
Pre-registered capability slices
↓
Largest paired-loss slices
↓
First-failure distribution shift
↓
Representative trace evidence
↓
Replay / regression fixtures
↓
Decision: block / investigate / accept trade-off
```

## Common wrong answers

### 错误 1：只看最差 slice

会产生 selection bias。

### 错误 2：slice 平均下降就等于能力下降

先确认 population / evaluator / denominator 可比。

### 错误 3：相关 slice 就是 root cause

slice 是分组变量，不是因果机制。

### 错误 4：总体持平就不用看 slice

可能存在改善与退化抵消。

## Evaluation design

正式 release regression 建议至少保留：

```text
primary overall metric
paired W/L
pre-registered slices
critical slice gates
first-failure distribution
cost / latency slices
exploratory findings separated
```

## Follow-up questions

- 什么时候用 natural-frequency weighting？
- slice 太多如何控制 false discovery？
- failure cluster 能否自动发现？
- critical slice 是否应该单独 hard gate？

## Evidence of mastery

达到 S4 时，应能面对“总体下降 3pp”完成：

1. comparability audit；
2. paired W/L；
3. slice table；
4. trace-based mechanism diagnosis；
5. 给出需扩样本还是可直接阻断 release 的理由。

## Related knowledge

- [Q04 Metric Design](../01_LLM_Evaluation/03_Metric_Design.md)
- [Q17 First Meaningful Failure](01_First_Meaningful_Failure_and_Root_Cause.md)
- [Evaluation Patterns P03/P04](../EVAL_PATTERNS.md)
