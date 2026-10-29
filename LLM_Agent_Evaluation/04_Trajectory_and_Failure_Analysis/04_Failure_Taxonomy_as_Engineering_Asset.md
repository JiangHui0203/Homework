# Q20 failure taxonomy 如何转化为可检测、可统计、可回归测试的工程资产？

- Level: M2
- Mastery: S0
- Related Parts: Part 4 / Part 5 / Part 7 / Part 8
- Related Patterns: P05 Frozen Core + Rotating Hard Set, P06 Trajectory First-Failure Analysis, P10 Replayable Evaluation
- Canonical taxonomy owner: `LLM_Agent_Data/14_Agent_Failure_Taxonomy.md`

## 30-second answer

Failure taxonomy 只有“错误名称列表”时价值很低。要工程化，每个 failure type 必须绑定：**operational definition、observable evidence、detection method、denominator、severity、owner、confounder、representative cases、regression fixture 和 intervention route**。

真正成熟的链路是：

```text
trace evidence
→ failure record
→ taxonomy label
→ aggregate metric / slice
→ regression case
→ CI / release gate
→ data / product / system action
```

并且 taxonomy 要版本化；定义变化不能悄悄重算历史结果。

## 90-second answer

我会把每个 failure type 做成 Failure Card，而不是只写一个 tag。例如 `tool_argument_error` 要明确：什么算 error、在哪些 opportunity 上可检测、需要什么 tool schema / state evidence、怎样和 execution failure 区分、分母是什么、严重度和 recoverability 如何、有哪些 frozen regression cases。

只有当一个 failure 能被稳定检测、统计，并有代表 fixture 可以重放时，它才从“分析标签”升级成工程资产。

post-hoc 新 failure 先进入 provisional taxonomy，积累多例证据后再 promote；否则 taxonomy 会被单次实验无限膨胀。

## 1. Taxonomy 的四个成熟阶段

### Stage 0 — Free-form note

```text
“模型好像理解错了”
```

不可统计、不可复现。

### Stage 1 — Named label

```text
task_understanding_error
```

能搜索，但边界模糊。

### Stage 2 — Operational failure type

有：

```text
definition
evidence requirement
detection rule
denominator
owner
```

可以稳定标注和统计。

### Stage 3 — Regression asset

进一步有：

```text
representative fixture
replay protocol
expected detection
expected system behavior
release / monitoring use
```

这才真正进入 Eval Engineering。

## 2. Failure Card 最小字段

```text
Failure ID
Name
Canonical definition
Layer
Owner
Severity
Recoverability
Observable symptom
First meaningful failure pattern
Required evidence
Detection method
Denominator / opportunity
Known confounders
Metrics affected
Recommended slices
Representative cases
Regression fixture
Expected fix / intervention route
Version introduced
Status: provisional / stable / deprecated
```

## 3. Detection 不一定等于 Label

例如：

```text
low confidence
high entropy
repeated tool call
```

可以作为 detection signal。

但正式 `tool_loop_failure` label 可能要求：

```text
same semantic action repeated >= k
AND no state progress
AND task still unresolved
```

即：

```text
signal != ground-truth label
```

## 4. Denominator 必须绑定 failure opportunity

错误例子：

```text
argument errors / all episodes
```

若很多 episode 根本没调用该工具，解释很弱。

更合理：

```text
argument errors / eligible argument-generation opportunities
```

这也是 taxonomy 能变成 metric 的关键一步。

## 5. Primary 与 propagated failure

一条 episode 可能出现：

```text
wrong task scope
→ wrong tool args
→ wrong result
→ false accept
```

如果四个都作为独立 primary failure 统计，会制造重复计数。

建议至少保存：

```text
primary failure
secondary / propagated failures
```

不同报表可分别回答：

```text
root-cause burden
vs
surface symptom burden
```

## 6. Failure severity 与 frequency 要分开

高频轻微问题和低频高风险问题不能只按次数排序。

可以同时维护：

```text
frequency
severity
detectability
recoverability
cost impact
user / safety impact
```

例如 false accept 即使频率低，也可能是 hard gate failure。

## 7. 从 failure 到 regression fixture

Promotion 条件建议：

1. 有稳定定义；
2. 至少一个可审计真实 case；
3. evidence 足以复现；
4. 能构造不泄漏答案的 fixture；
5. 明确 expected behavior；
6. 能在修复前失败、修复后通过或至少稳定检测；
7. 知道它属于 core regression 还是 rotating hard set。

## 8. 不要把所有失败都塞进 frozen core

### Frozen core

适合：

```text
高严重度
历史真实 regression
关键产品 contract
稳定可复现
```

### Rotating / hard set

适合：

```text
新出现 failure
长尾模式
容易被过拟合
需持续刷新
```

taxonomy 与 benchmark architecture 应配合，而不是每发现一次错误就永久加一道题。

## 9. Taxonomy versioning

定义可能变化：

```text
v1: any retry loop
v2: repeated semantic action + no progress
```

历史结果必须保存 taxonomy version。

否则同一个 `loop_failure_rate` 在不同时间语义变化，却看起来像连续指标。

## 10. Inter-rater / evaluator reliability

开放式 root cause label 可能依赖 human / Judge。

因此需要：

```text
annotation guideline
adjudication
agreement audit
uncertain / unresolved state
```

不要强迫所有 case 都有确定 root cause。

合法状态包括：

```text
UNRESOLVED
MULTI-CAUSE
INSUFFICIENT_EVIDENCE
```

## 11. VeriAgent example

Olist challenge 中已经出现可工程化的真实 failure：

```text
child-row eligibility applied at parent-table grain
alias scope violation
false accepted numeric result
SQL execution rejection
```

其中前两类来自明确 trace / SQL evidence，可以进一步形成稳定 regression fixture；而“模型不擅长多表推理”则仍然太宽泛，只适合作为 higher-level hypothesis，不应直接作为具体 failure label。

同样，challenge 构建中保存“典型错误 SQL”只证明题目具有区分该错误的能力；若模型没有实际犯该错，就不能把它统计成模型 failure。这体现了 taxonomy 工程化中的 evidence discipline。

## 12. 一个完整 lifecycle

```text
New incident
↓
Trace review
↓
Provisional failure record
↓
Evidence / replay
↓
Stable taxonomy mapping
↓
Metric + slice
↓
Regression fixture
↓
Fix
↓
Paired verification
↓
Frozen core or rotating hard set
↓
Monitoring / data flywheel
```

## Common wrong answers

### 错误 1：taxonomy 越细越专业

过细会导致标签稀疏、低一致性、维护困难。

### 错误 2：每个 failure 都应该有唯一 root cause

复杂 Agent 允许多因、多层传播和 unresolved。

### 错误 3：发现失败就立刻加训练数据

有些是 harness / tool / environment / evaluator bug，训练模型是错误 intervention。

### 错误 4：回归题越多越好

需要 core / rotating 分工，控制成本和 benchmark overfit。

## Evaluation design

Taxonomy review 定期检查：

```text
哪些标签从未被稳定检测？
哪些标签互相混淆？
哪些高频 failure 没有 regression fixture？
哪些 fixture 已经过拟合或失去区分度？
哪些定义发生过版本变化？
哪些 failure 应路由到 data / product / tool / harness？
```

## Follow-up questions

- 什么时候 promote provisional label？
- 多个 failure 是否允许 hierarchy？
- 自动 clustering 如何与稳定 taxonomy 对接？
- failure frequency 如何和 severity 合并排序？

## Evidence of mastery

达到 S3/S4 时，应能从一批失败 trace 建立：

```text
operational failure cards
stable denominator
slice dashboard
representative fixtures
regression routing
```

并明确哪些 label 仍只是 hypothesis。

## Related knowledge

- [Evaluation Failure Taxonomy](../FAILURE_TAXONOMY.md)
- [Q17 First Meaningful Failure](01_First_Meaningful_Failure_and_Root_Cause.md)
- [Q19 Slice Regression Diagnosis](03_Slice_Based_Regression_Diagnosis.md)
- [Canonical Data Failure Taxonomy](../../LLM_Agent_Data/14_Agent_Failure_Taxonomy.md)
