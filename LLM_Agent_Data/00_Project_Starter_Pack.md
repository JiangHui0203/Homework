# LLM / Agent Data Project Starter Pack

> 状态：`Stable Mother Edition V3.x / Scenario Assembly`
>
> 目标：当一个真实问题刚到手时，给出 **Day 0 / Day 1 / First Week** 的最小可信推进路径，让项目尽快从“大家有感觉”进入“有 Evidence、有 Owner、有 Hypothesis、有 Decision Gate”。
>
> 本文件不替代 [`Practical Playbooks`](./00_Practical_Playbooks.md) 或 [`Practical Artifact Kit`](./00_Practical_Artifact_Kit.md)，而是把它们装配成启动顺序。

---

# 0. 项目启动最怕的不是信息少，而是顺序错

常见错误顺序：

```text
看到 bad case
→ 先定方案
→ 批量造数据
→ 训练
→ 最后才想怎么评
```

推荐顺序：

```text
Problem
→ Contract
→ Evidence
→ Diagnosis
→ Data Problem Gate
→ Minimal Intervention
→ Frozen Evaluation
→ Decision
```

核心原则：

> **先证明问题是什么，再证明解决方案值得做。**

---

# 1. Day 0 — Intake：先把问题收窄

目标：当天结束前，不要求知道答案，但必须知道“我们到底在讨论什么”。

最少完成：

```text
A1 Problem Intake
```

必须回答：

```text
真实 symptom 是什么？
影响谁？
在哪个 population？
严重程度？
什么时间窗口？
现有 evidence 在哪里？
```

禁止把 solution 写进 problem statement。

错误：

```text
“我们要做 10 万条 synthetic data。”
```

正确：

```text
“某类 Agent task 的 harmful write rate 在 shipped-order slice 上上升。”
```

Day 0 退出条件：

```text
[ ] Problem Statement 可验证
[ ] Population 明确
[ ] Primary Metric 明确
[ ] Initial Evidence 可访问
[ ] Owner 暂定
[ ] 决策 deadline 明确
```

---

# 2. Day 1 — Contract + Evidence：先把世界冻结

目标：不要让大家在不同 Task / Case / Runtime 上讨论同一个“问题”。

完成：

```text
A2 Task / Case Contract
A3 Trajectory / Evidence Bundle
```

必须冻结：

```text
Task objective
Case initial state
Permissions
Tool / Harness / Environment versions
Success predicates
Forbidden side effects
Evaluator-visible truth
```

然后重建实际 trajectory：

```text
Observation
→ Decision
→ Action
→ Tool Result
→ State Transition
→ Final Outcome
```

Day 1 第一条 Gate：

```text
Can we reconstruct what actually happened?
```

如果不能：

```text
STOP diagnosis
→ improve logging / evidence first
```

不要在证据残缺时强行做 Root Cause Analysis。

---

# 3. Day 1 — Diagnosis：决定是不是 Data Problem

完成：

```text
A4 Failure Record
A5 Evaluator Contract
```

诊断顺序：

```text
Requirement / Task Contract
↓
Tool
↓
Harness
↓
Environment
↓
Evaluator
↓
Model / Policy
↓
Data Gap
```

至少区分：

```text
Symptom
Mechanism
Root Cause
Failure Layer
Failure Owner
```

以及：

```text
First Error
First Harmful Action
Last Recoverable State
Point of No Return
```

Data Problem Gate：

```text
如果 root cause 属于：
Tool / Harness / Environment / Evaluator / Product Spec
→ 优先 non-data fix

只有在：
Coverage / Supervision / Distribution / Decision-boundary Gap
更合理时
→ 进入 Data Intervention
```

Day 1 退出条件：

```text
[ ] Outcome 有 Evidence
[ ] Root Cause 至少达到 suspected + evidence-backed
[ ] Failure Owner 有候选
[ ] Evaluator claim / evidence 对齐
[ ] Data Problem Gate 已过或明确未过
```

---

# 4. Day 2–3 — Hypothesis：只设计最小可信 intervention

如果确认为 Data Gap，完成：

```text
A6 Data Intervention Card
```

先写 capability-level hypothesis：

```text
Observed Failure
→ Capability Gap
→ Why this signal / experience may teach it
```

不要直接从 failure 跳到：

```text
SFT
DPO
Synthetic
```

先回答：

```text
模型到底缺什么？
是没见过？
没被正确监督？
decision boundary 太弱？
recoverable 但 selector 不行？
还是 data distribution 与真实任务不匹配？
```

最小 intervention 原则：

```text
先 pilot
不先规模化
```

优先设计：

```text
matched-state contrast
hard negative
recovery example
counterfactual sibling
verified success
```

而不是一开始追求 volume。

---

# 5. Day 2–4 — Evaluation First：训练前先写实验卡

完成：

```text
A7 Experiment Card
```

训练前必须先冻结：

```text
Primary Question
Baseline
Intervention
Matched Budget
Population
Primary Eval
Transfer Eval
Regression Eval
Cost Metrics
Decision Rule
```

核心问题：

```text
If the result is +X,
what decision will we make?

If the result is flat,
what decision will we make?

If target improves but regression appears,
what decision will we make?
```

如果这些没定义：

```text
Experiment
→ 只是跑结果
```

不是 decision instrument。

---

# 6. First Week — Pilot：得到第一份可决策证据

第一周目标不是：

```text
把 pipeline 做完
```

而是：

> **用最小成本回答“这个方向值得继续吗？”**

建议 pilot 输出：

```text
small verified data batch
+
frozen baseline
+
matched-budget treatment
+
target eval
+
regression eval
+
cost estimate
```

第一周必须产出：

```text
A8 Decision Memo
```

Decision 只能是：

```text
SCALE
MAINTAIN
REVISE
STOP
RETIRE
```

不要只写：

```text
“结果看起来不错，继续观察。”
```

---

# 7. First Week 后 — Scale 之前再过一次 Gate

进入规模化之前检查：

```text
Target Gain stable?
Transfer exists?
Regression acceptable?
Cost acceptable?
Verifier reliable?
Lineage complete?
Production contract feasible?
Monitoring plan exists?
```

只有通过后才进入：

```text
A9 Production Handoff
```

否则：

```text
pilot success
≠ production readiness
```

---

# 8. 上线后 — Monitor 不是“看 dashboard”

需要：

```text
A10 Monitoring Incident / Drift Record
```

任何指标变化先排：

```text
Metric definition
Evaluator
Infrastructure
Traffic mix
Business rule
Frozen capability
Fresh failure composition
```

固定原则：

```text
Monitoring Alert
≠ Model Regression
```

如果确认出现新能力缺口：

```text
A10
→ new A1
↺
```

进入下一轮。

---

# 9. Day 0 → First Week 最短工件链

```text
Day 0
A1 Problem Intake
↓
Day 1
A2 Task / Case Contract
A3 Trajectory / Evidence
A4 Failure Record
A5 Evaluator Contract
↓
Day 2–3
A6 Data Intervention
↓
Day 2–4
A7 Experiment Card
↓
First Week
Pilot
↓
A8 Decision Memo
```

如果：

```text
A4 表明 non-data root cause
```

则可以提前结束：

```text
A1 → A2 → A3 → A4 → System Fix
```

这不是项目失败，而是成功避免了错误的数据投资。

---

# 10. 三类典型启动路径

## Path A — Production Agent Failure

```text
Problem Index P1
→ C1 / C3
→ A1–A5
→ Data Problem Gate
→ A6/A7 if needed
```

## Path B — Reasoning / Selector Research

```text
C4
→ Risk / Recoverability / Selectability
→ Oracle Headroom
→ Population Accounting
→ A7 Experiment Card
→ Cost-aware Decision
```

## Path C — Eval / Verifier Project

```text
C5
→ Claim
→ Strongest Evidence
→ Evaluator Contract
→ Verifier Coverage Audit
→ Hidden / Runtime / Regression Protocol
→ A7
```

---

# 11. 一个项目第一周最容易犯的十个错误

```text
1. Problem statement 已经写成 solution。
2. Task / Case / Episode 混在一起。
3. 没有保留 final world-state evidence。
4. Tool / Harness / Environment 不分。
5. Symptom 直接写成 Root Cause。
6. Agent failure 自动归 Model。
7. Failure 自动变成 Training Example。
8. 训练完才想 Eval。
9. Treatment 和 Baseline budget 不匹配。
10. 没有预先定义 Scale / Stop Rule。
```

---

# 12. 最小团队评审节奏

## Intake Review

看：

```text
A1 / A2
```

问题：

```text
问题定义对吗？
Task Contract 对吗？
```

## Diagnosis Review

看：

```text
A3 / A4 / A5
```

问题：

```text
Evidence 足吗？
Owner 对吗？
真的是 Data Problem 吗？
```

## Experiment Review

看：

```text
A6 / A7
```

问题：

```text
Hypothesis 能证伪吗？
Budget 公平吗？
Decision Rule 预注册了吗？
```

## Decision Review

看：

```text
A8
```

问题：

```text
Scale / Revise / Stop？
```

---

# 13. 与现有资产的关系

```text
Project Starter Pack
= 什么时候做什么

Practical Playbook
= 某类问题具体怎么走

Artifact Kit
= 每一步写成什么

Case Study
= 一个完整项目长什么样

Checklist
= 当前阶段有没有漏
```

因此不要复制粘贴五套文档。

推荐使用顺序：

```text
Starter Pack
→ 选择 Playbook
→ 填 Artifact
→ 对照 Case
→ 用 Checklist review
```

---

# 14. 最终启动原则

```text
先 Evidence
后 Attribution

先 Problem Gate
后 Data Intervention

先 Evaluation Contract
后 Scale

先 Decision Rule
后看结果
```

> **一个成熟项目的第一周，不是尽快生产很多数据，而是尽快获得足以做正确决策的最小证据。**
