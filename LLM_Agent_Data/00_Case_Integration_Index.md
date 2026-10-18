# LLM / Agent Data Knowledge System：Canonical Case Integration Index

> 状态：`Stable Mother Edition V3.x / Case Routing Index`
>
> Registry：[`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> Case files：[`C1 Order / Refund`](./cases/C1_Order_Refund_Agent.md) · [`C2 Calendar / Meeting`](./cases/C2_Calendar_Meeting_Agent.md) · [`C3 File / Repository`](./cases/C3_File_Repository_Agent.md) · [`C4 Reasoning Continue / Repair`](./cases/C4_Reasoning_Continue_Repair.md) · [`C5 Code / Execution`](./cases/C5_Code_Execution_Agent.md)

---

# 0. 目的

这份文件不再定义案例内容，而是回答一个编辑问题：

> **每一章应该调用哪个 canonical case、调用哪个 variant、用它证明什么？**

原则：

```text
Canonical Casebook
= registry / stable invariants / variant namespace

Case File
= full stable scenario / contract / stable IDs

Chapter
= specific analytical lens
```

因此同一个 `C1-VB` 可以在不同章节分别被解释为：

```text
Ch10 → forbidden action contract
Ch11 → observation-grounded state transition
Ch13 → last recoverable state
Ch14 → failure ownership
Ch15 → state verifier
Ch16 → paired benchmark case
Ch23 → high-risk monitoring slice
```

场景不变，分析层变化。

---

# 1. 全书案例角色分工

| Case | 主角色 | 不应被滥用成 |
|---|---|---|
| `C1` Order / Refund | 全书 Agent 主干案例 | 所有章节唯一例子 |
| `C2` Calendar / Meeting | 多约束、实体、partial completion | C1 的换皮 |
| `C3` File / Repository | 权限、write side effect、idempotency、Harness | 普通 tool-use 示例 |
| `C4` Reasoning Continue / Repair | reasoning-state / same-prefix / selector | Agent tool case |
| `C5` Code / Execution | executable verifier / hidden eval / runtime | 单纯代码生成示例 |

案例设计必须保留“互补性”，而不是让五个 case 最后都讲成同一个问题。

---

# 2. Ch1–5 — Learning Signals

## Ch1 Data Objects & Learning Signals

推荐：`C1 Base Task`

只用于展示：

```text
Task
→ Case
→ Episode
→ Trajectory
→ Outcome / Feedback
```

这里不要提前进入 C1-F1 的完整 failure diagnosis。

Secondary：`C4-SC` 只用于说明 reasoning state 也可以成为 Experience Object。

---

## Ch2 Pretraining / SFT / Post-training

推荐：不设置主案例。

只在 SFT / post-training data type 表格中用：

```text
C1 success trajectory → Agent SFT
C1-SC preference → Preference / post-training
```

目的：说明同一经验可以被不同训练阶段消费。

---

## Ch3 Preference / Reward / Feedback

主案例：`C2-F3` + C2 successful variant

比较：

```text
A = full success
B = calendar update success but notification missing
```

用于说明：

```text
Chosen / Rejected
relative supervision
multi-dimensional rubric
Task Success > style
```

Secondary：`C5-F3` 用于 Judge bias。

---

## Ch4 Reasoning Data / Process Supervision

主案例：`C4-SC`

必须重点调用：

```text
C4-P1 High Risk but Not Recoverable
C4-P2 Recoverable but Not Selectable
C4-P3 Low Confidence but Correct
C4-P4 Harmful Repair
```

这章是 C4 canonical semantic owner。

---

## Ch5 Tool-use / Agent Trajectory Data

主案例：`C1-VA / C1-VB`

重点：

```text
whether to call
which tool
arguments
execution
observation
next action
termination
```

这里只建立 Agent experience object；First Harmful / Root Cause 不展开。

---

# 3. Ch6–9 — Data Acquisition & Selection

## Ch6 Human Data

主案例：`C2` annotation boundary

重点标注：

```text
哪个会议是目标？
“周会不要动”如何写 guideline？
partial completion 怎么标？
什么时候 annotator 应 abstain？
```

Secondary：`C5-F2` 让专家判断 hidden-spec boundary。

---

## Ch7 Synthetic Data

主案例：`C5`

合成：

```text
valid date formats
invalid edge cases
runtime variants
repair failures
```

Secondary：`C1-VA / C1-VB` 做 matched synthetic environment variants。

---

## Ch8 Rollout / Candidate Selection

双主案例：

```text
C4-SC → reasoning same-prefix pool
C5-POOL → executable code candidate pool
```

用它们明确：

```text
Generator
≠ Oracle
≠ Selector
```

C4 强调 future outcome / selectability；C5 强调 executable verifier。

---

## Ch9 Hard Case Mining / Curriculum

主案例：`C4-P1 ... P4`

用于区分：

```text
uncertain
wrong
recoverable
selectable
valuable-to-train
```

Secondary：`C1-F1 / F3` 作为 failure-family mining seed。

---

# 4. Ch10–14 — Agent World & Diagnosis

这五章形成全书最强的 C1/C2/C3 连续案例链。

## Ch10 Agent Task Design

主案例：`C2 Base Task`

因为 C2 同时包含：

```text
Goal
multiple constraints
forbidden action
notification requirement
termination
```

用 Required / Forbidden / Invariant predicate 结构化 Task Contract。

Secondary：`C1-VB` 展示条件式安全停止。

---

## Ch11 Environment Design

主案例：`C1-VB`

重点：

```text
World State = shipped
Observation = shipped
Tool = refund interface
Harness = observation injection / runtime
```

Secondary：`C3-F5` 专门证明：

```text
Tool / Harness / Environment failure ownership
```

---

## Ch12 Trajectory Anatomy

主案例：`C1-VB + C1-F1`

把它表示成：

```text
typed event log
state before / after
state diff
actor
visibility
branch / retry lineage
```

Secondary：`C3-F4` 展示 retry lineage。

---

## Ch13 Task Success & Credit Assignment

主案例：`C1-F1`

必须明确：

```text
First Error
First Harmful Action
Last Recoverable State
Point of No Return
```

Secondary：`C2-F3` 展示 partial success 不等于所有 step 都无 credit。

---

## Ch14 Agent Failure Taxonomy

主案例：`C3-F5`

因为它最适合证明：

```text
Symptom occurs at Agent behavior layer
but Root Cause / Owner may be Harness
```

Secondary：`C1-F1` 用于完整：

```text
Outcome → Symptom → Mechanism → Root Cause → Owner
```

---

# 5. Ch15–16 — Measurement

## Ch15 Grader / Verifier / Judge

双主案例：

```text
C1-VB → final-state / forbidden-side-effect verifier
C5-F3 → executable evidence vs LLM Judge
```

用于建立：

```text
Evidence first, Judge second
```

C5 负责“能执行就别让 Judge 猜”；C1 负责 Agent state evidence。

---

## Ch16 Benchmark Design & Evaluation Protocol

主案例：`C1 Case Family`

构造：

```text
pending / shipped
success / failure
paired intervention
full population / eligible / triggered
```

Secondary：`C5-R1 / R2` 展示 runtime freeze；`C4-SC` 展示 paired same-state comparison。

---

# 6. Ch17–21 — Data Optimization & Lifecycle

## Ch17 Data Flywheel

主案例：`C1-F1`

链条：

```text
Production Failure
→ verify
→ failure family
→ capability gap
→ synthetic / human / counterfactual acquisition
→ training / regression
→ deploy
→ monitor
```

这里不重新讲 failure taxonomy，只调用 Ch14 标签。

---

## Ch18 Data Strategy / Valuation

主案例：C1 vs C2/C3 portfolio

比较资源：

```text
高频 low-severity constraint failure
vs
低频 high-severity protected-write failure
```

用于说明：

```text
Frequency ≠ Priority
Risk-adjusted ROI
```

Secondary：`C4-P2` 展示 candidate pool 有 oracle headroom 但 selector 难，数据价值不等于 risk score 高。

---

## Ch19 Governance / Lineage

主案例：`C3`

记录：

```text
Task version
filesystem snapshot
Tool version
Harness version
raw trace
corrected label
re-score / re-run / replay
```

Secondary：`C5-R1/R2` 展示 runtime version lineage。

---

## Ch20 Quality / Filtering / Dedup / Mixture

主案例：`C2 Family`

适合证明：

```text
语义相似
≠ decision equivalent
```

比如：

```text
“改会议”
vs
“改会议，但周会不要动”
```

semantic dedup 不能误删 constraint variation。

Secondary：`C5` 用 executable filter；`C4` 用 decision-level dedup。

---

## Ch21 Data Experiments

主案例：`C1-F1` recovery / constraint intervention

设计：

```text
Baseline mixture
vs
+ C1-family targeted data
vs
budget-matched replacement
```

评测：

```text
C1-family target
held-out sibling family
C2 / C3 transfer
normal-agent regression
```

Secondary：`C5` 做 verifier-quality experiment；`C4` 做 reasoning-state mining experiment。

---

# 7. Ch22–24 — Data Operations

## Ch22 Data Production System

主案例：`C3-F4`

用 blind retry 贯穿：

```text
Job
Worker
Tool action
Retry Policy
Idempotency
Artifact
State Snapshot
Quality Gate
```

Secondary：`C5` 作为 sandbox / test-run worker；`C1` 作为 state-verifier production job。

---

## Ch23 Monitoring / Drift

主案例：C1 high-risk monitoring slice

监控：

```text
shipped-order attempted-refund rate
false-success rate
verification rate
```

Drift variants：

```text
policy changes
Tool error mix changes
traffic mix changes
Judge threshold changes
```

Secondary：`C5-R1/R2` runtime drift；`C4` trigger/calibration drift。

---

## Ch24 End-to-End Operating Model

主案例：`C3-F5`

团队 routing：

```text
Observed symptom
→ reproduce
→ evidence
→ Agent layer symptom
→ Harness root cause
→ Platform owner
```

它最适合防止：

```text
所有失败 → Data Team
```

Secondary：`C1-F1` 是真正可以进入 data intervention 的对照 case。

---

# 8. Ch25 — Synthesis

Ch25 不应该发明第六个综合案例。

主案例：`C1 End-to-End`

要求完整调用：

```text
C1 Task Contract
→ C1 Environment
→ C1 Trajectory
→ C1-F1 Credit Landmarks
→ Ch14 Diagnosis
→ Ch15 Verification
→ Ch16 Evaluation
→ Ch17 Flywheel
→ Ch18 Investment
→ Ch20 Curation
→ Ch21 Experiment
→ Ch22 Production
→ Ch23 Monitoring
→ Ch24 Operating Gate
```

然后用四个 secondary case 做“换场景能否迁移”的检查：

```text
C2 → multi-constraint
C3 → permission / side effect / ownership
C4 → reasoning state
C5 → executable verification
```

这使 Ch25 真正成为：

> **调用整套系统解决问题，而不是再总结一遍术语。**

---

# 9. Case 引用格式

正文建议统一为：

```text
> **Canonical Case — `C1-VB`**
> 订单 1847 已发货；任务要求“已发货就不要动”。完整 Case Contract 见 [C1](./cases/C1_Order_Refund_Agent.md)。
```

如果章节只需要一个 failure：

```text
这里沿用 `C3-F5`：Tool 实际失败，但 Harness 向 Agent 注入 success observation。
```

如果需要 counterfactual：

```text
这里沿用 `C4-SC`，保持 authoritative prefix 不变，只替换当前 continuation。
```

不要重新复制整份 case contract；只有当本章的分析依赖某个字段时，才局部复述。

---

# 10. Variant Integrity Rules

1. 引用 `C1-VB` 时，订单状态必须是 `shipped`。
2. 引用 `C2-F3` 时，calendar update 已成功、notification 未完成。
3. 引用 `C3-F5` 时，Tool truth 与 Harness-visible observation 必须不一致。
4. 引用 `C4-SC` 时，所有 sibling 必须来自同一 authoritative prefix。
5. 引用 `C5-F2` 时，public tests pass、held-out / hidden test fail。
6. C2 中所有“明天 / 周五”等相对时间必须相对于 frozen case clock `2026-10-19 09:00 Asia/Shanghai` 解释，不得使用实际运行日。
7. 如需改变上述关键条件，创建新的 variant ID，不得沿用旧 ID。
8. Case ID 是实验语义的一部分，不只是文档标签。

---

# 11. 完成标准

Canonical Case Integration 完成后，全书应满足：

```text
读者第一次见 C1 后
后续无需重新理解场景

同一 failure 在不同章节
只是分析 lens 变化

章节案例不再随机漂移

counterfactual 的“哪些条件不变”可以被明确检查

一个 case 可以直接变成
benchmark / training / regression / monitoring asset
```

最终目标：

> **把“举例”升级成“可复用的分析对象”。**