# LLM / Agent Data Project Starter Pack

> 状态：`Stable Mother Edition V3.x / Scenario Assembly / Stress-tested`
>
> 目标：当一个真实问题刚到手时，给出 **Day 0 / Day 1 / First Week** 的最小可信推进路径，让项目尽快从“大家有感觉”进入“有 Evidence、有 Owner、有 Hypothesis、有 Decision Gate”。
>
> 本文件不替代 [`Practical Playbooks`](./00_Practical_Playbooks.md) 或 [`Practical Artifact Kit`](./00_Practical_Artifact_Kit.md)，而是把它们装配成启动顺序。
>
> 压力测试：[`Scenario Pack Stress Test`](./00_Scenario_Pack_Stress_Test.md)

---

# 0. 项目启动最怕的不是信息少，而是顺序错

常见错误顺序：

```text
看到 bad case / 有一个研究 idea
→ 先定方案
→ 批量造数据 / 跑大实验
→ 最后才想 population、evaluator、budget 和 claim
```

推荐顺序：

```text
Problem / Question
→ Contract
→ Evidence
→ Diagnosis / Mechanism
→ Intervention Gate
→ Minimal Intervention
→ Frozen Evaluation
→ Decision
```

核心原则：

> **先证明问题是什么，再证明解决方案值得做。**

---

# 0.1 先判断项目从哪里开始

压力测试后，Starter Pack 不再假设所有项目都来自一个 production bad case。

至少区分三种 origin：

```text
Failure-led
→ 已经观察到真实 failure / regression
→ 重点是 Evidence / Root Cause / Owner

Hypothesis-led
→ 先提出一个机制或方法假设
→ 重点是 state / intervention / counterfactual / protocol

Evaluation-led
→ 怀疑 evaluator / benchmark / protocol 不足
→ 重点是 Claim / Evidence / Coverage / Construct Validity
```

它们后面会合流到：

```text
Frozen Contract
→ Controlled Comparison
→ Decision
```

但前面的诊断工件可以不同。

不要把：

```text
Hypothesis-led research
```

硬写成：

```text
“某个 Root Cause 已被发现”
```

也不要把 evaluation gap 强行解释成 Data Gap。

---

# 1. Day 0 — Intake：先把问题收窄

目标：当天结束前，不要求知道答案，但必须知道“我们到底在讨论什么”。

最少完成：

```text
A1 Problem Intake
```

必须回答：

```text
真实 symptom / scientific question 是什么？
影响谁 / 哪个 benchmark？
在哪个 population？
严重程度 / scientific value？
什么时间窗口 / frozen dataset version？
现有 evidence 在哪里？
```

禁止把 solution 写进 problem statement。

错误：

```text
“我们要做 10 万条 synthetic data。”
“我们要加一个低置信触发器。”
```

正确：

```text
“某类 Agent task 的 harmful write rate 在 shipped-order slice 上上升。”
```

或：

```text
“当前 reasoning state 出现低置信信号时，局部同前缀探索是否存在可转化为 E2E gain 的修复价值？”
```

## Population Ledger — Day 0 就开始

普通项目可以先写一个 population；selective / routing / trigger system 必须从一开始分层：

```text
Full Decision Population
↓
Screened / Eligible
↓
Triggered
↓
Intervened
↓
Observed / Scorable
```

Day 0 不一定知道最终计数，但必须知道这些 denominator 是否可能不同。

Day 0 退出条件：

```text
[ ] Problem / Scientific Question 可验证
[ ] Project Origin Mode 明确
[ ] Full Population 定义明确
[ ] Selective system 的 denominator layers 已识别
[ ] Primary Metric 明确
[ ] Initial Evidence 可访问
[ ] Owner 暂定
[ ] 决策 deadline / experiment milestone 明确
```

---

# 2. Day 1 — Contract + Evidence：先把世界冻结

目标：不要让大家在不同 Task / Case / Runtime / Decision State 上讨论同一个“问题”。

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

## Selective / local intervention 额外冻结

如果方法不是“整题统一处理”，而是在某个 state / prefix / event 上选择性介入，还必须写：

```text
Authoritative State / Prefix
Decision Point / Intervention Unit
Trigger Statistic
Trigger Threshold / Rule
Candidate Generation Policy
Same-state / Same-prefix Constraint
Online Selector Inputs
Acceptance / Continuation Semantics
Intervention Budget / Cap
Global / Mainline Budget
```

固定边界：

```text
Same Task
≠ Same Decision State

Same Method Name
≠ Same Intervention Semantics
```

然后重建实际 trajectory / reasoning lineage：

```text
Observation / Prefix
→ Decision State
→ Trigger / Action
→ Candidate / Tool Result
→ State Transition / Continuation
→ Final Outcome
```

Day 1 第一条 Gate：

```text
Can we reconstruct what actually happened
at the exact decision state being studied?
```

如果不能：

```text
STOP diagnosis / mechanism claim
→ improve logging / lineage first
```

不要在证据残缺时强行做 Root Cause 或 selector mechanism analysis。

---

# 3. Day 1 — Diagnosis / Mechanism：先决定在研究什么

## Failure-led

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

## Hypothesis-led

不强制写单一 Root Cause。

先拆：

```text
Observable Signal
Target Latent Property / Mechanism
Intervention Opportunity
Counterfactual
Oracle Headroom
Online Selectability
Cost
```

例如 reasoning / selector 项目：

```text
Risk
≠ Error
≠ Recoverability
≠ Selectability
```

## Evaluation-led

先写：

```text
Claim
Evidence
Evaluator
Coverage
Known Failure Modes
Version / Drift
```

而不是直接问：

```text
“换哪个 Judge？”
```

---

# 3.1 Intervention Gate：不要预设一定是 Data

压力测试后，通用 Starter Pack 明确允许：

```text
Data Intervention
Model / Training Intervention
Inference-time / Policy Intervention
Tool Intervention
Harness / Environment Intervention
Evaluator Intervention
Product / Task Contract Intervention
```

如果 root cause 属于：

```text
Tool / Harness / Environment / Evaluator / Product Spec
```

优先 non-data fix。

如果是 Hypothesis-led inference-time research，也可以直接进入 method-specific intervention contract，而不经过 `A6 Data Intervention Card`。

只有在：

```text
Coverage / Supervision / Distribution / Decision-boundary Gap
```

更合理时，才进入真正的 Data Intervention。

Day 1 退出条件：

```text
[ ] Outcome / research object 有 Evidence
[ ] Failure-led: Root Cause 至少 suspected + evidence-backed
[ ] Hypothesis-led: mechanism variables 与 counterfactual 已定义
[ ] Evaluation-led: claim / evidence / evaluator 已对齐
[ ] Intervention Owner / Type 有候选
[ ] Data Problem Gate 已过或明确未过
```

---

# 4. Day 2–3 — Hypothesis：只设计最小可信 intervention

## 如果是 Data Gap

完成：

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

## 如果是非 Data Intervention

写最小 Method / System Contract：

```text
Intervention Point
Allowed Information
Action Space
Budget
Stop Rule
Fallback
Expected Failure Mode
```

不要为了 Artifact Chain 整齐，把 inference-time / tool / evaluator intervention 改名成 Data Intervention。

最小 intervention 原则：

```text
先 pilot
不先规模化
```

---

# 5. Day 2–4 — Evaluation First：实验前先写 A7

完成：

```text
A7 Experiment Card
```

实验前必须先冻结：

```text
Primary Question
Baseline Identity / Provenance
Intervention
Matched Dimensions
Population Ledger
Information Boundary
Primary Eval
Transfer Eval
Regression Eval
Cost Ledger
Statistics / Uncertainty
Decision Rule
```

## Population Ledger

selective system 至少写：

```text
Full
Screened
Eligible
Triggered
Intervened
Observed / Scorable
```

每个 reported metric 都要知道 denominator 属于哪一层。

固定边界：

```text
Triggered-slice Result
≠ Full-pop E2E Result
```

## Information Boundary

必须把信息分成：

```text
Online-observable
→ runtime 可以合法使用

Offline-only
→ analysis / oracle / supervision 可以使用

Forbidden Leakage
→ online trigger / selector 绝不能使用
```

典型 forbidden leakage：

```text
future outcome
hidden correctness label
post-hoc adjudication
future rollout value
```

除非方法定义本身明确允许。

## Cost Ledger

selective / adaptive system 至少区分：

```text
Cost per Triggered Case
Incremental Intervention Cost
Average E2E Cost over Full Population
Worst-case / Budget-cap Cost
```

不要把不同 denominator 下的 cost 放在同一列比较。

核心问题：

```text
If the result is +X,
what decision will we make?

If the result is flat,
what decision will we make?

If target improves but regression / cost appears,
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
frozen baseline
+
minimal treatment / intervention
+
full population ledger
+
target eval
+
regression / transfer eval
+
cost ledger
+
information-boundary audit
```

如果是 Data 项目，再加：

```text
small verified data batch
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

A8 至少同时回答：

```text
Full-pop effect?
Slice effect?
Benefit transition / mechanism?
Regression?
Cost?
Uncertainty?
Claim scope?
```

---

# 7. First Week 后 — Scale 之前再过一次 Gate

进入规模化之前检查：

```text
Target Gain stable?
Full-pop claim成立？
Transfer exists?
Regression acceptable?
Cost acceptable?
Information boundary clean?
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
Trigger / Router / Selector calibration
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

## Failure-led Data Project

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

## Hypothesis-led / Non-data Research

```text
Question
→ A2-style Method / State Contract
→ Evidence / Lineage
→ Mechanism Decomposition
→ Method-specific Intervention Contract
→ A7 Experiment Card
→ A8 Decision Memo
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
→ define Authoritative State / Prefix
→ Risk / Recoverability / Selectability
→ Oracle Headroom
→ Online / Offline Information Boundary
→ Population Ledger
→ A7 Experiment Card
→ Cost-aware E2E Decision
```

K17 类项目尤其要保留：

```text
Full Population
≠ Triggered Cohort

Offline Oracle / Future Label
≠ Online Feature

Candidate Exists
≠ Candidate Selectable
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

# 11. 一个项目第一周最容易犯的十四个错误

```text
1. Problem statement 已经写成 solution。
2. Failure-led / Hypothesis-led / Evaluation-led 没分清。
3. Task / Case / Episode / Decision State 混在一起。
4. 没有保留 authoritative prefix / intervention point。
5. 没有保留 final world-state / final outcome evidence。
6. Tool / Harness / Environment 不分。
7. Symptom 直接写成 Root Cause。
8. Agent failure 自动归 Model。
9. Failure 自动变成 Training Example。
10. 非 Data Intervention 被硬塞成 Data Intervention。
11. 训练 / generation 跑完才想 Eval。
12. Treatment 和 Baseline budget / runtime 不匹配。
13. Triggered-only / observed-only 结果冒充 Full-pop E2E。
14. Online selector 偷看 offline-only label / future outcome，或没有预先定义 Scale / Stop Rule。
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
Project Origin Mode 对吗？
Full Population 对吗？
Task / Decision State Contract 对吗？
```

## Diagnosis / Mechanism Review

看：

```text
A3 / A4 / A5
或 hypothesis-led mechanism record
```

问题：

```text
Evidence 足吗？
Owner / Mechanism 假设对吗？
Online / Offline information boundary 清楚吗？
真的是 Data Problem 吗？
```

## Experiment Review

看：

```text
A6 / method contract / A7
```

问题：

```text
Hypothesis 能证伪吗？
Population Ledger 完整吗？
Budget 公平吗？
Cost denominator 对吗？
有没有 future leakage？
Decision Rule 预注册了吗？
```

## Decision Review

看：

```text
A8
```

问题：

```text
Full-pop effect 是什么？
Slice / mechanism effect 是什么？
Claim scope 到哪里？
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

Scenario Stress Test
= 这些资产在真实追问 / protocol 下哪里会坏
```

因此不要复制粘贴六套文档。

推荐使用顺序：

```text
Starter Pack
→ 选择 Playbook / Research Path
→ 填 Artifact / Method Contract
→ 对照 Case
→ 用 Checklist review
→ 用 Stress Test 检查高风险边界
```

---

# 14. 最终启动原则

```text
先定义 Full Population
后看 Slice

先 Evidence
后 Attribution / Mechanism

先 Authoritative State
后 Intervention

先 Information Boundary
后 Selector / Router

先 Evaluation Contract
后大规模运行

先 Decision Rule
后看结果
```

> **一个成熟项目的第一周，不是尽快生产很多数据或跑很多实验，而是尽快获得足以做正确决策、且 denominator 与信息边界都站得住的最小证据。**
