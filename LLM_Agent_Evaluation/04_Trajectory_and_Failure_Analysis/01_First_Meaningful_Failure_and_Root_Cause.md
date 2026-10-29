# Q17 如何从 trajectory 中区分 symptom、first meaningful failure 和 root cause？

- Level: M1
- Mastery: S0
- Related Parts: Part 3 / Part 4 / Part 7
- Related Patterns: P06 Trajectory First-Failure Analysis, P10 Replayable Evaluation, P12 Mechanism ≠ Outcome
- Canonical taxonomy owner: `LLM_Agent_Data/14_Agent_Failure_Taxonomy.md`

## 30-second answer

Agent 失败后，不能从最终报错直接跳到 root cause。应沿 trajectory 建立证据链：**Outcome → Symptom → First Error / First Harmful Action → First Meaningful Failure → Immediate Mechanism → Root Cause / Hypothesis**。

`First meaningful failure` 是最早一处对任务可达成功造成实质影响、且有足够证据支持的偏离点；它不一定是第一处局部错误，也不一定是最终报错。`Root cause` 则是最值得被修复的上游机制，需要额外证据，证据不足时只能记录为 hypothesis。

## 90-second answer

我不会看到“SQL execution error”就直接写 root cause=SQL generation。先重放 trace，按时间顺序标注：任务理解、计划、检索、tool selection、arguments、execution、observation interpretation、verification、recovery、final synthesis。

然后区分：

```text
Symptom              看到了什么坏结果
First Error           最早局部事实/逻辑/约束错误
First Harmful Action  最早真正降低后续可达价值的动作
First Meaningful Failure
                     最早有证据、对最终结果具有实质诊断意义的失败点
Immediate Mechanism   直接产生 symptom 的近端机制
Root Cause            解释这一类失败为什么发生、最值得修复的上游机制
```

root cause 若没有 counterfactual / replay / repeated evidence，只写 `root_cause_hypothesis + confidence + required_evidence`。

## 1. 为什么最后一个错误通常不是根因

一条典型链路：

```text
Task
→ 错误理解日期口径
→ 生成错误过滤条件
→ SQL 成功执行
→ 得到错误数值
→ verifier 未拦截
→ final answer 错误
```

最终 symptom 是 `wrong answer`，近端 mechanism 可能是 `wrong SQL returned wrong value`，但 first meaningful failure 可能早在任务口径理解阶段。

如果只修 SQL syntax，根因仍在。

## 2. 六个层次不能混

### Outcome

最终发生什么：success / failure / safe stop / false accept。

### Symptom

直接可观察表现：错误数字、超时、工具报错、循环、幻觉完成。

### First Error

按时间最早的局部错误。它可能很小、可恢复，未必真正决定结局。

### First Harmful Action

第一次把系统推进到明显更差状态，或降低后续成功可达性的 action。

### First Meaningful Failure

Evaluation 中更实用的定位点：

> 最早一处同时满足“有证据支持 + 对最终失败有实质影响 + 对修复有行动价值”的偏离。

它可能等于 First Error，也可能更晚。

### Root Cause

上游机制层解释。应能回答：

```text
为什么这类失败会发生？
修哪个机制最可能降低复发？
```

## 3. 一套可执行的 trajectory diagnosis 流程

### Step A — Freeze artifacts

至少保存：

```text
task / task version
environment snapshot
model / prompt / controller config
state / memory snapshot
ordered trace events
tool inputs / outputs
verifier / grader outputs
final outcome
```

### Step B — Mark event timeline

把 trajectory 变成结构化事件：

```text
E0 task received
E1 task interpreted
E2 plan created
E3 memory retrieved
E4 tool selected
E5 tool arguments created
E6 tool executed
E7 observation consumed
E8 verification
E9 recovery / stop
E10 final answer
```

### Step C — Find earliest divergence with evidence

对每个事件问：

```text
Expected contract 是什么？
Observed event 是什么？
是否违反 contract？
是否仍可恢复？
后续失败是否依赖此偏离？
```

### Step D — Separate localization from causality

定位到 `E4 wrong tool selection` 只说明发生位置。

真正 root cause 还可能是：

```text
任务意图解析错
工具描述歧义
planner policy 错
stale memory 误导
tool schema 缺字段
```

### Step E — State evidence strength

推荐三级：

```text
OBSERVED    trace 直接可见
SUPPORTED   replay / counterfactual / repeated evidence 支持
HYPOTHESIS  合理但尚未验证
```

## 4. First meaningful failure 的判定标准

一个实用 checklist：

- 是不是比最终 symptom 更早？
- 是否有明确 contract / reference / evidence 证明它错？
- 如果纠正它，后续成功路径是否仍可能存在？
- 它是否解释后续多个 propagated symptoms？
- 修复它是否有工程行动价值？

如果只满足“看起来可疑”，不要升级成 failure ground truth。

## 5. Counterfactual 是最有价值的证据之一

例如怀疑 tool argument 导致失败，可以做：

```text
保持 task / prefix / environment 不变
只修正 argument
replay execution
```

若结果恢复，支持该 argument 是 causal contributor。

但仍要区分：

```text
修正后成功
≠ 证明它是唯一 root cause
```

## 6. Propagation graph

不要把每个后续错误都记成独立根因。

```text
wrong time scope
  ↓
wrong SQL predicate
  ↓
wrong tool result
  ↓
wrong final number
```

可以记录：

```text
primary failure = task_scope_error
propagated symptoms = sql_predicate_error, wrong_numeric_answer
```

这样 failure count 不会人为膨胀。

## 7. VeriAgent example

Olist challenge 中 `CJ03_r01` 最终表现为 SQL 执行失败，直接 symptom 是 DuckDB 拒绝查询。

trace 进一步显示 SQL 在当前作用域引用了未定义 alias `oi`。因此可以较强地支持：

```text
Symptom:
SQL execution failed

First meaningful failure:
SQL generation produced out-of-scope alias reference

Immediate mechanism:
DuckDB binder rejected the query
```

但若要把 root cause 写成“模型不理解 SQL alias scope”，仍属于更上游的机制判断，需要更多同类 evidence；不能只凭一条失败就宣称通用能力缺陷。

另一个 challenge candidate memory 实验中，13 次失败发生在 SQL-stage memory retrieval 之前。这里 first meaningful failure 的阶段证据直接阻止了错误归因：即使最终 candidate 比 baseline 多对 1 题，也不能把差异归因于只在更晚 SQL 阶段作用的 memory。

## Common wrong answers

### 错误 1：最终报错位置就是 root cause

最后一处只是 symptom 或 immediate mechanism 的高发位置。

### 错误 2：最早异常就是 first meaningful failure

早期偏离可能被完全恢复，未实际降低成功可达性。

### 错误 3：Judge 说“原因是 X”，所以 root cause=X

Judge output 是 evidence source 之一，不自动成为 causal ground truth。

### 错误 4：一次 counterfactual 成功证明唯一原因

它支持 causal contribution，不证明唯一性。

## Evaluation design

每条正式 failure review 至少保存：

```text
outcome
symptom
first_error_event (optional)
first_harmful_action (optional)
first_meaningful_failure
immediate_mechanism
root_cause_or_hypothesis
evidence_level
evidence_refs
owner
recoverability
propagated_symptoms
suggested_regression_test
```

## Follow-up questions

- first error 和 first harmful action 什么时候不同？
- 一个 trajectory 可以有多个 independent root causes 吗？
- 如果 environment 不可 replay，怎样降低因果结论强度？
- LLM judge 能否自动标 root cause？

## Evidence of mastery

达到 S4 时，应能拿一条真实 trace：

1. 画出事件时间线；
2. 区分 symptom / localization / mechanism / root-cause hypothesis；
3. 指出最小需要补的 evidence；
4. 设计一个 replay / counterfactual；
5. 给出可变成 regression case 的 failure record。

## Related knowledge

- [Q12 Agent Evaluation Contract](../03_Agent_Evaluation/01_Agent_Evaluation_Contract.md)
- [Q16 Long-Horizon Agent Evaluation](../03_Agent_Evaluation/05_Long_Horizon_Agent_Evaluation.md)
- [Evaluation Failure Taxonomy](../FAILURE_TAXONOMY.md)
- [Canonical Data Failure Taxonomy](../../LLM_Agent_Data/14_Agent_Failure_Taxonomy.md)
