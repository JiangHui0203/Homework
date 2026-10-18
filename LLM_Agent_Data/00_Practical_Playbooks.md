# LLM / Agent Data Practical Playbooks

> 状态：`Stable Mother Edition V3.x / Action Layer / Multi-entry-aligned`
>
> 角色：把 25 章方法论从“知道怎么分析”推进到“拿到现实输入以后，今天按什么顺序做”。
>
> 与其他 Retrieval Assets 的区别：
>
> ```text
> Project Starter Pack / Entry Router
> = 先判断从哪个问题入口进入
>
> Problem Index
> = 按症状找排查方向
>
> Checklist Index
> = 某阶段有哪些事项不能漏
>
> Practical Playbook
> = 从一个现实输入推进到可决策输出的动作顺序
> ```
>
> 原则：**每个 Playbook 必须有明确 Trigger、Minimum Inputs、Produced Artifacts 与 Decision Gate。没有决策出口的“流程”只是活动清单；不同 Playbook 可以从不同 Artifact Entry 开始，不要求都先造 A1。**

---

# P1 — 一条线上 Agent Failure，怎样判断要不要做数据？

Entry：`Failure-led`

## Trigger

你拿到一个真实 failure，例如：

```text
Agent 说退款完成
但实际状态不符合用户约束
```

或者：

```text
模型看到关键 Observation
仍做了 harmful action
```

## Minimum Inputs

```text
Task / User Request
Case / Environment Snapshot
Trajectory / Action Log
Tool Result / Observation
Final World State
Evaluator Result if any
```

如果这些都没有，第一步不是分析模型，而是补 Evidence。

## Procedure

```text
1. Verify Outcome
   ↓
2. Freeze Task / Case / Runtime
   ↓
3. Reconstruct Trajectory
   ↓
4. Locate First Error / First Harmful
   ↓
5. Check Tool / Harness / Environment / Evaluator
   ↓
6. Form Root Cause / Owner hypothesis
   ↓
7. Abstract Capability Gap
   ↓
8. Run Data Problem Gate
   ↓
9. Build minimum counterfactual / intervention
   ↓
10. Define Pilot + Scale / Stop rule
```

## Produced Artifacts

```text
Failure Record
Evidence Package
Root Cause / Owner
Capability Gap Statement
Data Problem Gate Decision
Pilot Spec
Regression Case
```

## Decision Gate

### NOT A DATA PROBLEM

如果 root cause 是：

```text
Tool
Harness
Environment
Task Spec
Evaluator
```

优先修系统，再重新评价是否仍有 Model / Data Gap。

### DATA PROBLEM CANDIDATE

至少需要：

```text
Evidence 支持 Model / Policy failure
Capability 可以抽象成跨 case 结构
存在合理 supervision interface
可以设计 controlled downstream test
```

## Reference

- `C1 End-to-End Walkthrough`
- Ch11–17 / Ch21
- F4 / F5 / F6 / F7 / F9

---

# P2 — 拿到几十万条 Agent Trajectory，第一周应该做什么？

Entry：`Asset-led / Curation-led`

## Trigger

你拿到：

```text
10万 / 50万 / 100万条 Agent trajectory
```

任务不是：

```text
“清洗完拿去训练”
```

而是先搞清：

> **这些 trajectory 到底是什么 Experience，哪些部分可信，能支持哪些用途。**

这里不要求先人为制造一个 failure / root cause。第一入口是：

```text
Source Asset Identity
→ Lineage
→ Evidence / Quality View
→ Curation / Dataset View
→ Downstream Validation
```

## Minimum Inputs

```text
Trajectory source
Source asset / collection identity
Task / Case identity
Model / Prompt / Tool / Harness version
Action / Observation log
Outcome / evaluator if available
Collection policy
```

## Day 1 — Establish Identity

先做：

```text
source_asset_id
task_id
case_id
episode_id
trajectory_id
source
runtime version
```

检查：

```text
是否能重建同一 Episode？
是否有重复 / retry / shard artifact？
是否知道每条 trace 来自哪个环境版本？
是否知道这批数据由什么 collection policy 产生？
```

## Day 2 — Reconstruct Evidence Layers

分开：

```text
Agent-visible State
Tool Result
Observation
World State / State Diff
Evaluator-only Evidence
```

不要把：

```text
final response
```

当成环境 Outcome。

## Day 3 — Build Quality / Failure Views

先做多维 profile：

```text
Task Success
Constraint Violation
Tool Error
Verification Failure
Unsupported Success
Failure Layer
Failure Owner
Severity
Trajectory Length
Cost
```

不要一开始就压成：

```text
quality_score = 0.83
```

注意：

```text
Batch Profile
≠ 每条 trajectory 都必须生成 Root Cause
```

只有证据足够、且诊断对后续决策有用时才进入 failure attribution。

## Day 4 — Dedup / Family / Split

至少建立：

```text
exact duplicate
near duplicate
same seed / same workflow
same failure family
same environment fixture
```

然后再做 train / eval split。

## Day 5 — Create Usage Views

从 source experience 派生：

```text
SFT View
Preference View
Recovery View
Regression View
Failure Analysis View
Hard-case Seed View
```

每个 Dataset View 应能追回：

```text
Source IDs
Filter / Routing Policy
Build Recipe
Mixture / Sampling Policy if any
```

## Produced Artifacts

```text
Source / Lineage Manifest
Canonical Trajectory Schema
Quality Profile
Failure Profile
Family IDs
Dedup Report
Lineage Map
Candidate Dataset Views
Build Recipe
```

## Decision Gate

第一周结束时应该能回答：

```text
这些数据覆盖什么 capability？
哪些 evidence 是真的？
哪些 failure 最值得看？
多少信息是重复的？
哪些用途安全，哪些用途不够资格？
Dataset View 能不能从 Source Asset 重建？
下一步最小 experiment 是什么？
```

如果只能回答：

```text
“剩下 42 万条”
```

说明还停留在数据清洗层。

## Reference

- Ch5 / Ch12 / Ch14 / Ch19 / Ch20 / Ch22
- F5 / F6 / F11 / F12
- A11 / A6-C / A7

---

# P3 — 想做 Synthetic Agent Data，怎么避免“模型批量自嗨”？

Entry：通常是 `Hypothesis-led` 或 `Asset / Production-led`

## Trigger

团队提出：

```text
“用强模型生成 100 万条 Agent data。”
```

先不要开跑。

## Minimum Inputs

```text
Target Capability
Real / Human / Production Seed
Environment or Simulator
Verification Method
Intended Training Use
Target Evaluation
```

## Procedure

```text
1. Define Capability Gap
   ↓
2. Select seed / family structure
   ↓
3. Decide what to synthesize
      Task / Response / Trajectory / Environment / User
   ↓
4. Design diversity at decision level
   ↓
5. Generate small pilot
   ↓
6. Verify with executable / rule / human anchors
   ↓
7. Measure mode collapse / family duplication
   ↓
8. Build family-level train/eval split
   ↓
9. Run synthetic-to-real transfer experiment
   ↓
10. Decide Scale / Revise / Stop
```

## Required Audits

```text
Teacher Bias
Mode Collapse
Surface Diversity vs Decision Diversity
Synthetic-to-real Gap
Verifier Coverage
Contamination
Family Leakage
```

## Produced Artifacts

```text
Synthetic Production Contract
Seed Registry
Family IDs
Generator Version
Verifier Report
Diversity Report
Transfer Evaluation
Scale Decision
```

## Decision Gate

可以 Scale 的不是：

```text
“生成很便宜”
```

而是：

```text
Verified Yield 合理
Unique Decision Coverage 增长
Synthetic-to-real transfer 成立
Marginal Utility 仍为正
成本优于 alternative acquisition channel
```

## Reference

- Ch7 / Ch18 / Ch20 / Ch21 / Ch22
- F10 / F12

---

# P4 — Judge 分数涨了，真实 Success 不涨，怎么查？

Entry：`Evaluation-led`（如果首先观察到线上 score shift，也可能由 Monitoring-led 进入）

## Trigger

出现：

```text
Judge Score ↑
但
Environment / Executable Success ↔ or ↓
```

## Minimum Inputs

```text
Raw Evidence
Judge raw output
Judge / Prompt / Rubric versions
Executable / Environment truth if available
Human / Gold anchor
Model outputs before / after
```

## Procedure

```text
1. Freeze the Claim
   ↓
2. Compare direct Evidence vs Judge judgment
   ↓
3. Audit Evidence Package changes
   ↓
4. Audit Judge / Prompt / Rubric / Parser changes
   ↓
5. If evaluator changed: build old↔new paired Measurement Bridge
   ↓
6. Run bias probes
      position / verbosity / style
   ↓
7. Slice FP / FN by severity / task family
   ↓
8. Compare proxy gain vs downstream gain
   ↓
9. Re-score frozen outputs if evaluator changed
```

Measurement Bridge 至少问：

```text
同一批 frozen outputs
旧 evaluator 怎么判？
新 evaluator 怎么判？
哪些 slice 改变？
新旧分数是否还能纵向可比？
```

没有 bridge 时，不要把：

```text
old score series
+
new score series
```

直接拼成一条历史趋势。

## Produced Artifacts

```text
Evaluator Contract
Measurement Bridge if version changed
Judge Calibration Report
Bias Audit
FP / FN Slices
Corrected Labels if needed
Re-score Report
Proxy-vs-Outcome Analysis
```

## Decision Gate

### Judge / Measurement Problem

```text
Executable truth stable
Judge distribution shifts
Bias / calibration worsens
或 old↔new measurement relation 不稳定
```

→ fix / recalibrate evaluator；必要时限制 historical comparability claim。

### Model / Data Problem

```text
Judge is calibrated
Direct outcome also fails
```

→ continue diagnosis elsewhere。

## Reference

- Ch15 / Ch19 / Ch23
- F7 / F11 / F13
- A5 / A5-M

---

# P5 — Candidate / Selector 方法有 Oracle Gap，但 E2E 没提升，怎么拆？

Entry：`Hypothesis-led / Selective-system Research`

## Trigger

你看到：

```text
候选池里经常存在更好的 answer / trajectory
```

但最终系统：

```text
Net ≈ 0
或下降
```

## Minimum Inputs

```text
Authoritative Prefix / State
Baseline candidate
Sibling candidates
Offline outcome labels
Online selector features
Trigger decision
Selection decision
Generation / scoring cost
```

## Procedure

```text
1. Freeze same-prefix / same-state contract
   ↓
2. Measure Generator Oracle Opportunity
   ↓
3. Measure Trigger Coverage
   ↓
4. Measure Selector Accuracy / Abstention
   ↓
5. Count Rescue / Harmful / Neutral transitions
   ↓
6. Restore Full Population denominator
   ↓
7. Add cost / latency / candidate budget
   ↓
8. Separate exploratory vs confirmatory conditions
```

同时强制保留：

```text
Population Ledger
Full / Screened / Eligible / Triggered / Intervened / Observed

Information Boundary
Online-observable / Offline-only / Forbidden-leakage

Cost Ledger
Per-trigger / Incremental / Full-pop Average / Cap
```

## Produced Artifacts

```text
Oracle Gap Report
Trigger Report
Selector Report
Transition Matrix
Full-population E2E Result
Population / Information / Cost Ledger
Cost Curve
Failure Cases
```

## Decision Gate

系统要有效，至少同时需要：

```text
Useful candidate exists
AND trigger reaches useful states
AND selector recognizes candidate
AND harmful replacement controlled
AND added cost acceptable
```

因此：

```text
Candidate existence
≠ Selectability
≠ E2E Improvement
```

## Reference

- Ch4 / Ch8 / Ch16
- F3 / F8
- C4-SC
- A2-S / A7

---

# P6 — 一批数据让指标 +1.2pt，值不值得继续投？

Entry：`Data Experiment / Strategy Decision`

## Trigger

Data Experiment 报告：

```text
+1.2 pt
```

但团队需要决定：

```text
Scale?
Maintain?
Rework?
Stop?
```

## Minimum Inputs

```text
Baseline / Treatment
Data Manifest
Training Budget
Target Eval
Transfer Eval
Regression Eval
Cost
Repeated / paired uncertainty
```

## Procedure

```text
1. Confirm matched budget
   ↓
2. Check target gain uncertainty
   ↓
3. Check transfer
   ↓
4. Check general / safety regression
   ↓
5. Check mechanism consistency
   ↓
6. Compute verified yield / total cost
   ↓
7. Compare marginal gain to previous tranche
   ↓
8. Compare opportunity cost vs other capability gaps
```

## Produced Artifacts

```text
Experiment Summary
Cost / Yield Report
Scaling Curve
Regression Report
Data Investment Memo
Scale / Stop Decision
```

## Decision Gate

```text
SCALE
→ stable gain + transfer + acceptable regression + positive marginal ROI

MAINTAIN
→ useful but close to saturation

REVISE
→ signal exists but construction / transfer / regression problematic

STOP
→ no stable value or better alternatives exist

RETIRE
→ environment / capability has moved
```

## Reference

- Ch18 / Ch21
- F10

---

# P7 — 线上 Success Rate 掉了，怎样判断是不是模型退化？

Entry：`Monitoring-led Incident`

## Trigger

```text
online success ↓
```

第一反应不是：

```text
“模型退化了”
```

而是先保住 incident evidence 和必要 containment。

## Minimum Inputs

```text
Last-known-good time / release
Metric definition / query version
Model version
Judge / Verifier version
Tool / Harness / Environment version
Traffic / Task Mix
Business Rule / Product Policy
Frozen Core benchmark
Failure slices
```

## Procedure

严格按顺序查：

```text
0. Preserve last-known-good + Change Ledger; contain high-severity incident if needed
   ↓
1. Metric changed?
   ↓
2. Judge / Verifier changed?
   ↓
3. Tool / Harness / Environment changed?
   ↓
4. Traffic / Task Mix changed?
   ↓
5. Business Rule / Correct Behavior changed?
   ↓
6. Compare Raw Overall vs Fixed-mix
   ↓
7. Frozen Benchmark regressed?
   ↓
8. Failure composition changed?
```

## Produced Artifacts

```text
A10 Incident / Drift Record
Last-known-good Snapshot
Change Ledger
Containment / Rollback Record if needed
Raw vs Fixed-mix Metric
Drift Classification
Version Diff
Failure Composition
Frozen-core Regression Result
Fresh Cohort
Intervention Recommendation
```

## Decision Gate

```text
Measurement Drift
→ fix metric / evaluator

Infrastructure Drift
→ fix Tool / Harness / Environment

Data Drift
→ analyze slice / routing

Concept Drift
→ update task / labels / verifier

Capability Drift
→ model / data investigation

Failure Drift
→ new frontier / fresh cohort
```

只有 triage 证据足够后，才把 incident 重新路由成：

```text
A1 new problem
A4 failure diagnosis
A5 evaluator issue
A6 data intervention
或 non-data system fix
```

## Reference

- Ch23 / Ch24
- F13 / F14
- A10 / A5-M if evaluator changed

---

# Playbook Selection Map

```text
Failure-led
“一条 bad case 怎么处理？”
→ P1

Asset-led / Curation-led
“拿到几十万条 trajectory 怎么开工？”
→ P2

Hypothesis / Production-led
“想批量做 synthetic data”
→ P3

Evaluation-led
“Judge 分和真实结果打架”
→ P4

Hypothesis-led Selective Research
“有好 candidate 但方法不涨”
→ P5

Data Strategy
“数据实验涨了，值不值得继续？”
→ P6

Monitoring-led
“线上指标掉了，是模型吗？”
→ P7
```

---

# Universal Exit Condition

无论使用哪个 Playbook，结束时至少应该产生：

```text
Entry / Problem / Decision Object
Relevant Contract
Evidence / Lineage
Diagnosis / Mechanism / Evaluator / Asset conclusion as applicable
Intervention or Controlled Change
Controlled Validation Plan / Result
Decision
Next Monitoring / Regression / Re-entry Asset
```

不是所有项目都必须产生：

```text
Root Cause
Data Intervention
```

但所有项目都必须能解释：

```text
为什么从这个 Entry 进入？
为什么选择这个 intervention owner？
什么 evidence 支撑这个决定？
如何验证？
```

如果最后只得到：

```text
“我们分析了很多数据”
```

但没有：

```text
Decision
```

说明工作流还没有闭环。

最终原则：

> **Playbook 的价值不是让流程更复杂，而是让一个现实问题从正确入口开始，尽快进入“证据充分、边界明确、干预可测、结果可决策”的状态。**