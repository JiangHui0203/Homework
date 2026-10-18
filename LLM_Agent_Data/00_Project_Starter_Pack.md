# LLM / Agent Data Project Starter Pack

> 状态：`Stable Mother Edition V3.x / Scenario Assembly / Stress-tested / Entry Router Promoted`
>
> 目标：当一个真实问题刚到手时，给出 **Day 0 / Day 1 / First Week** 的最小可信推进路径，让项目尽快从“大家有感觉”进入“有 Evidence、有 Owner、有 Hypothesis、有 Decision Gate”。
>
> 本文件不替代 [`Practical Playbooks`](./00_Practical_Playbooks.md) 或 [`Practical Artifact Kit`](./00_Practical_Artifact_Kit.md)，而是把它们装配成启动顺序。
>
> 压力测试：[`Round 1`](./00_Scenario_Pack_Stress_Test.md) · [`Round 2`](./00_Scenario_Pack_Stress_Test_Round_2.md) · [`Promotion Test`](./00_Scenario_Pack_Promotion_Test.md)
>
> 按需扩展：[`Scenario Pack Candidate Extensions`](./00_Scenario_Pack_Candidate_Extensions.md)

---

# 0. 项目启动最怕的不是信息少，而是顺序错

常见错误顺序：

```text
看到 bad case / 有一个研究 idea
→ 先定方案
→ 批量造数据 / 跑大实验
→ 最后才想 population、evaluator、budget 和 claim
```

推荐顺序不是一条死链，而是：

```text
正确入口
→ Contract / Evidence
→ Diagnosis / Mechanism / Asset Validation
→ Intervention Gate
→ Minimal Controlled Change
→ Frozen Evaluation
→ Decision
→ Monitoring / Re-entry
```

核心原则：

> **先从正确的问题入口进入，再证明问题是什么，最后证明解决方案值得做。**

---

# 0.1 Entry Router：先判断项目从哪里进入

三轮压力测试后，Starter Pack 不再假设所有项目都来自一个 production bad case，也不要求所有项目机械从 `A1 → A10` 顺序填写。

至少区分五种常见 origin：

```text
Failure-led
→ 已经观察到真实 failure / regression
→ 常见入口：A1 / A2 / A3 / A4
→ 重点：Evidence / Root Cause / Owner

Monitoring-led Incident
→ 先看到 alert / online metric shift
→ 常见入口：A10
→ 重点：Last-known-good / Change Ledger / Containment / Triage
→ 确认新问题后再进入 A1 / A3 / A4 / A5

Hypothesis-led
→ 先提出一个机制或方法假设
→ 常见入口：A1 + A2 / A2-S + A7
→ 重点：state / intervention / counterfactual / protocol

Evaluation-led
→ 怀疑 evaluator / benchmark / protocol / guideline 不足
→ 常见入口：A5
→ 重点：Claim / Evidence / Coverage / Construct Validity
→ evaluator 换版时按需使用 Measurement Bridge

Asset-led / Curation-led
→ 已经拥有一批 source assets / trajectories / labels
→ 常见入口：A11 source lineage + curation contract
→ 重点：source integrity / routing / dedup / dataset view / downstream validation
```

它们后面会合流到：

```text
Relevant Contract + Evidence
→ Controlled Change
→ Evaluation
→ Decision
```

固定边界：

```text
不同 Entry
≠ 不同严谨标准

Artifact Chain
≠ 所有项目必须顺序填满 A1–A10
```

不要把：

```text
Hypothesis-led research
```

硬写成：

```text
“某个 Root Cause 已被发现”
```

也不要把：

```text
Monitoring Alert
```

硬写成：

```text
“模型退化”
```

更不要把：

```text
Existing Data Asset
```

直接当成：

```text
Training Dataset
```

---

# 0.2 哪些扩展保持按需，而不塞进主模板

第二轮异质压力测试后，以下结构已验证有用，但仍保持 optional：

```text
A10-I Production Incident Extension
→ last-known-good / change ledger / fixed-mix / rollback

A5-M Evaluator Measurement Bridge
→ old↔new evaluator / rubric / guideline paired bridge

A6-C Curation Contract
→ source asset → routed / deduped / rebuildable dataset view
```

原因不是它们不重要，而是：

> **Core 应该小而稳定；只有相关项目才加载对应 extension。**

Human Annotation / Gold Contract 目前仍是 candidate，不进入母本强制项。

---

# 1. Day 0 — Intake：先把问题收窄

本节适用于需要创建 A1 的项目；Monitoring-led Incident 可以先从 A10 进入，Asset-led 可以先从 A11 / source asset contract 进入。

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

## Monitoring-led

先保留：

```text
Last-known-good
Change Ledger
Raw / Slice / Fixed-mix Metric
Frozen Core
Fresh Failure / Frontier
Containment / Rollback Decision
```

然后再判断进入：

```text
traffic / product / evaluator / infrastructure fix
```

还是：

```text
A1 / A3 / A4 / A5
```

固定边界：

```text
Alert
≠ Diagnosis

Rollback Decision
≠ Root-cause Proof
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

若 evaluator / verifier / rubric / guideline 换版，必须先判断是否需要：

```text
Old↔New Measurement Bridge
```

否则跨版本 score 不应直接画成一条连续趋势。

## Asset-led / Curation-led

先检查：

```text
Source Identity
Episode / Case Identity
Runtime / Environment Version
Final-state Evidence
Evaluator / Label Version
Family / Seed Lineage
Privacy / Rights
```

再进入：

```text
Validity
→ Routing
→ Dedup / Family Grouping
→ Dataset View
→ Exposure
→ Downstream Validation
```

固定边界：

```text
Source Asset
≠ Dataset View

Raw Sample Count
≠ Effective Information Size
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
Curation / Dataset-view Intervention
```

如果 root cause 属于：

```text
Tool / Harness / Environment / Evaluator / Product Spec
```

优先 non-data fix。

如果是 Hypothesis-led inference-time research，也可以直接进入 method-specific intervention contract，而不经过 `A6 Data Intervention Card`。

如果是 Asset-led curation，则可以使用按需 `A6-C Curation Contract`，但不要假装它是新的 canonical artifact number。

只有在：

```text
Coverage / Supervision / Distribution / Decision-boundary Gap
```

更合理时，才进入真正的 Data Intervention。

Day 1 退出条件：

```text
[ ] Outcome / research object / source asset 有 Evidence
[ ] Failure-led: Root Cause 至少 suspected + evidence-backed
[ ] Monitoring-led: Last-known-good / change ledger 已建立
[ ] Hypothesis-led: mechanism variables 与 counterfactual 已定义
[ ] Evaluation-led: claim / evidence / evaluator 已对齐
[ ] Asset-led: source identity / lineage / target dataset view 已定义
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

## 如果是 Curation / Dataset-view Change

冻结：

```text
Source Assets
Validity Checks
Routing Policy
Dedup Unit
Family Grouping
Evaluator Version
Mixture / Exposure
Build Recipe
```

并明确：

```text
Intrinsic Data Quality
≠ Downstream Learning Value
```

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

## Evaluator Version Boundary

如果 Baseline / Treatment 或 longitudinal comparison 使用了不同 evaluator / rubric / verifier version：

```text
先建立 Measurement Bridge
```

或者明确：

```text
historical curve not directly comparable
```

不要把换尺子的 score delta 写成 capability delta。

## Curation Validation Boundary

如果比较的是 curation / filter / mixture policy：

```text
Curation KPI ↑
```

不能直接推出：

```text
Model Learning Value ↑
```

仍应使用 matched-budget downstream evaluation。

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

如果是 Asset-led / Curation 项目，再加：

```text
source→dataset-view lineage
+
yield funnel
+
exposure summary
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

如果 evaluator / curation policy 发生过版本切换，再加：

```text
Measurement / build lineage bridge complete?
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

如果是重大 production incident，优先按需加载：

```text
A10-I Production Incident Extension
```

先保存：

```text
Last-known-good
Change Ledger
Raw / Slice / Fixed-mix
Containment / Rollback Decision
```

再做 attribution。

如果确认出现新能力缺口：

```text
A10
→ new A1
↺
```

进入下一轮。

---

# 9. Entry Router → First Week 最短工件链

## Failure-led Data Project

```text
A1 Problem Intake
→ A2 Task / Case Contract
→ A3 Trajectory / Evidence
→ A4 Failure Record
→ A5 Evaluator Contract
→ A6 Data Intervention
→ A7 Experiment Card
→ A8 Decision Memo
```

## Monitoring-led Incident

```text
A10 Monitoring Incident
→ Last-known-good / Change Ledger / Containment
→ Triage
├─ System / Evaluator / Product / Traffic Fix
└─ confirmed new problem → A1 / A3 / A4 / A5 → A7 / A8
```

## Hypothesis-led / Non-data Research

```text
Question
→ A1 Scope
→ A2-style Method / State Contract
→ Evidence / Lineage
→ Mechanism Decomposition
→ Method-specific Intervention Contract
→ A7 Experiment Card
→ A8 Decision Memo
```

## Evaluation-led

```text
A5 Evaluator Contract
→ Claim / Evidence / Coverage
→ A5-M Measurement Bridge if version changes
→ A7 Comparison
→ A8 Decision
```

## Asset-led / Curation-led

```text
A11 Source Lineage
→ A6-C Curation Contract if needed
→ Rebuildable Dataset View
→ A7 Downstream Validation
→ A8 Decision
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

# 10. 五类典型启动路径

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

## Path C — Eval / Verifier / Human Gold

```text
C5 / Ch6 / Ch15
→ Claim
→ Strongest Evidence
→ Evaluator Contract
→ Verifier / Guideline Coverage Audit
→ Measurement Bridge if version changes
→ Hidden / Runtime / Regression Protocol
→ A7
```

## Path D — Production Incident / Drift

```text
A10
→ Last-known-good
→ Change Ledger
→ Raw / Fixed-mix / Frozen-core comparison
→ Containment
→ Correct Owner
→ new A1 only if needed
```

## Path E — Large-scale Trajectory / Synthetic Curation

```text
A11 Source Lineage
→ Source Integrity
→ Routing / Dedup / Family Grouping
→ Dataset View / Exposure
→ A7 matched-budget downstream validation
→ A8
```

---

# 11. 一个项目第一周最容易犯的十八个错误

```text
1. Problem statement 已经写成 solution。
2. Failure-led / Monitoring-led / Hypothesis-led / Evaluation-led / Asset-led 没分清。
3. 把 Artifact Chain 当成所有项目必须顺序填满的直线。
4. Task / Case / Episode / Decision State 混在一起。
5. 没有保留 authoritative prefix / intervention point。
6. 没有保留 final world-state / final outcome evidence。
7. Tool / Harness / Environment 不分。
8. Monitoring Alert 直接写成 Model Regression。
9. Symptom 直接写成 Root Cause。
10. Agent failure 自动归 Model。
11. Failure 自动变成 Training Example。
12. 非 Data Intervention 被硬塞成 Data Intervention。
13. Source Asset 直接当 Training Dataset。
14. 换 Judge / Verifier / Guideline 后直接续画历史 score 曲线。
15. Re-score 静默覆盖 Historical Judgment / Decision。
16. 训练 / generation 跑完才想 Eval。
17. Treatment 和 Baseline budget / runtime 不匹配，或 Triggered-only / observed-only 结果冒充 Full-pop E2E。
18. Online selector 偷看 offline-only label / future outcome，或没有预先定义 Scale / Stop Rule。
```

---

# 12. 最小团队评审节奏

## Entry / Intake Review

根据 origin 看：

```text
Failure-led
→ A1 / A2

Monitoring-led
→ A10

Hypothesis-led
→ A1 / A2-S

Evaluation-led
→ A5

Asset-led
→ A11 / source contract
```

问题：

```text
Entry 对吗？
问题 / Claim / Asset 定义对吗？
Full Population / Source Population 对吗？
Task / Decision State / Measurement Contract 对吗？
```

## Diagnosis / Mechanism Review

看：

```text
A3 / A4 / A5
或 hypothesis-led mechanism record
或 A10 incident evidence
或 asset integrity / lineage
```

问题：

```text
Evidence 足吗？
Owner / Mechanism 假设对吗？
Online / Offline information boundary 清楚吗？
Evaluator version 可比吗？
Source asset lineage 完整吗？
真的是 Data Problem 吗？
```

## Experiment Review

看：

```text
A6 / method contract / curation contract / A7
```

问题：

```text
Hypothesis 能证伪吗？
Population Ledger 完整吗？
Budget 公平吗？
Cost denominator 对吗？
有没有 future leakage？
Measurement Bridge 是否需要？
Dataset View 是否可重建？
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
Historical meaning 有没有被覆盖？
Scale / Revise / Stop？
```

---

# 13. 与现有资产的关系

```text
Project Starter Pack
= 从哪个入口开始、什么时候做什么

Practical Playbook
= 某类问题具体怎么走

Artifact Kit
= 每一步写成什么

Candidate Extensions
= 某类项目按需加载什么额外 contract

Case Study
= 一个完整项目长什么样

Checklist
= 当前阶段有没有漏

Scenario Stress Test
= 这些资产在真实追问 / protocol 下哪里会坏
```

因此不要复制粘贴多套文档。

推荐使用顺序：

```text
Starter Pack
→ 选择正确 Entry
→ 选择 Playbook / Research Path
→ 填 Core Artifact
→ 按需加载 Extension
→ 对照 Case
→ 用 Checklist review
→ 用 Stress Test 检查高风险边界
```

---

# 14. 最终启动原则

```text
先选正确 Entry
后套流程

先定义 Full Population / Source Asset
后看 Slice / Dataset View

先 Evidence
后 Attribution / Mechanism

先 Authoritative State
后 Intervention

先 Information Boundary
后 Selector / Router

先 Measurement Bridge
后跨版本比较

先 Evaluation Contract
后大规模运行

先 Decision Rule
后看结果
```

> **一个成熟项目的第一周，不是把 A1–A10 填满，也不是尽快生产很多数据或跑很多实验，而是从正确入口进入，并尽快获得足以做正确决策、且 denominator、信息边界、measurement 与 lineage 都站得住的最小证据。**
