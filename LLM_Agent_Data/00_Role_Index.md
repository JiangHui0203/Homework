# LLM / Agent Data Knowledge System：Role Index

> 角色：按岗位 / 职能检索知识体系。回答“做这个角色，最应该先掌握什么、重点读哪些章、应该形成什么判断能力？”

---

# 1. Data Research / LLM Data Scientist

## 核心职责

```text
Capability Gap
→ Data Hypothesis
→ Acquisition / Construction
→ Curation / Mixture
→ Data Experiment
→ Scale / Stop
```

## 优先章节

```text
1 → 2 → 3
→ 6 → 7 → 8 → 9
→ 18 → 20 → 21
→ 25
```

## 必备能力

- 区分 `Hard ≠ Valuable`；
- 能把 failure 转成 supervision interface；
- 会设计 Human / Synthetic / Production-mined 数据；
- 会做 matched-budget data experiment；
- 会判断 scaling curve / marginal utility；
- 会给出 Scale / Maintain / Revise / Stop 结论。

## Master Figures

F2 / F9 / F10 / F14

---

# 2. Agent Data / Agent Evaluation

## 核心职责

```text
Task
→ Environment
→ Trajectory
→ Outcome
→ Credit
→ Failure
→ Evaluation
```

## 优先章节

```text
1 → 5
→ 10 → 11 → 12 → 13 → 14
→ 15 → 16
→ 17 → 22 → 23
→ 25
```

## 必备能力

- Task Contract；
- Tool / Harness / Environment 边界；
- typed trajectory / state lineage；
- Tool success ≠ Task success；
- First Error / First Harmful / Root Cause；
- final-state verifier；
- failure taxonomy；
- coverage / triggered denominator。

## Cases

C1 / C2 / C3

## Figures

F4 / F5 / F6 / F7 / F8 / F13

---

# 3. Evaluation / Benchmark Researcher

## 核心职责

```text
Capability Definition
→ Benchmark Object
→ Evaluator
→ Frozen Protocol
→ Matched Runs
→ Statistics / Cost / Claim Scope
```

## 优先章节

```text
1
→ 10 → 11
→ 13 → 14
→ 15 → 16
→ 19
→ 21 → 23
```

## 必备能力

- Evidence first；
- Verifier / Grader / Judge 区分；
- Gold / Anchor calibration；
- paired comparison；
- Rescue / Harmful / Net；
- population accounting；
- budget matching；
- cluster-aware uncertainty；
- stable ruler + moving frontier；
- claim scope。

## Figures

F6 / F7 / F8 / F11 / F13

---

# 4. Post-training / Alignment

## 核心职责

```text
Learning Signal Design
→ SFT / Preference / Reward / RL
→ Data Mixture
→ Behavior Change
→ Regression Control
```

## 优先章节

```text
1 → 2 → 3 → 4
→ 6 → 7 → 8
→ 15
→ 18 → 20 → 21
```

## 必备能力

- demonstration / preference / reward 的区别；
- chosen ≠ absolute truth；
- hard negative / pair informativeness；
- reward hacking；
- process supervision；
- source / mixture interaction；
- quality vs quantity；
- downstream learning value。

## Figures

F2 / F3 / F7 / F10

---

# 5. Reasoning / Test-time / Selector Research

## 核心职责

```text
Reasoning State
→ Risk
→ Continue / Stop / Branch / Repair
→ Candidate Pool
→ Selector
→ Cost-aware Evaluation
```

## 优先章节

```text
1 → 4
→ 8 → 9
→ 13
→ 15 → 16
→ 18 → 21
→ 25
```

## 必备能力

- Correctness / Risk / Recoverability / Repairability / Selectability；
- same-prefix counterfactual；
- oracle vs selector；
- future-info leakage；
- rescue / harmful transition；
- trigger / coverage / cost accounting；
- detector ≠ generator ≠ selector ≠ E2E。

## Case

C4

## Figures

F3 / F8 / F10

---

# 6. Data Platform / DataOps

## 核心职责

```text
Identity
→ Job / Queue / Worker
→ Artifact / Metadata
→ Version / Lineage
→ Dataset Build
→ Monitoring / Cost
```

## 优先章节

```text
1 → 12
→ 19 → 20
→ 22 → 23 → 24
```

## 必备能力

- stable IDs；
- raw immutable / derived rebuildable；
- job state machine；
- retry / idempotency；
- artifact vs metadata；
- dataset view + build recipe；
- backpressure / DLQ；
- cost accounting；
- data freshness / drift。

## Figures

F5 / F11 / F12 / F13 / F14

---

# 7. Human Data / Annotation Ops

## 核心职责

```text
Guideline
→ Qualification
→ Annotation
→ QA / Gold
→ Disagreement
→ Adjudication
→ Versioned Labels
```

## 优先章节

```text
1 → 3
→ 6
→ 15
→ 19 → 22
```

## 必备能力

- annotation schema；
- boundary case；
- abstention；
- IAA；
- annotator calibration；
- expert routing；
- adjudication；
- corrected labels vs historical decisions。

## Figures

F7 / F11 / F12

---

# 8. Synthetic Data Research

## 核心职责

```text
Seed
→ Generator / Evolution
→ Environment / User Simulation
→ Verification
→ Diversity
→ Curation
→ Downstream Experiment
```

## 优先章节

```text
1 → 7 → 8 → 9
→ 15
→ 19 → 20 → 21
```

## 必备能力

- task / response / trajectory / environment synthesis；
- teacher bias；
- surface diversity vs decision diversity；
- synthetic lineage；
- executable verification；
- contamination；
- generator / verifier ablation；
- synthetic-to-real transfer。

## Cases

C1 / C5

---

# 9. Agent / Tool / Harness Engineer

## 核心职责

```text
Tool Contract
→ Harness
→ Environment
→ State / Observation
→ Retry / Memory / Stop
→ Production Reliability
```

## 优先章节

```text
5
→ 10 → 11 → 12 → 14
→ 22 → 23 → 24
```

## 必备能力

- Tool ≠ Harness ≠ Environment；
- world / observation / agent-visible state；
- idempotency；
- infrastructure retry ≠ agent recovery；
- environment reset / snapshot；
- runtime versioning；
- Tool / Harness Drift；
- Failure Layer ≠ Owner。

## Case

C3

## Figures

F4 / F5 / F6 / F12 / F13

---

# 10. Product / Applied AI

## 核心职责

```text
User Goal
→ Capability Definition
→ Success / Risk
→ Prioritization
→ Release Decision
→ Production Feedback
```

## 优先章节

```text
10
→ 14 → 16
→ 17 → 18
→ 21
→ 23 → 24 → 25
```

## 必备能力

- 把模糊需求写成 Task Contract；
- 定义 forbidden side effect；
- 识别真正 capability gap；
- 不把所有问题都丢给 Data；
- 主指标 + guardrail；
- Scale / Stop；
- canary / rollback；
- quarterly roadmap。

## Figures

F8 / F9 / F10 / F13 / F14

---

# 11. Research Lead / Data Lead

## 核心职责

```text
Problem Portfolio
→ Evidence Standard
→ Resource Allocation
→ Team Interface
→ Scientific / Product Decision
```

## 优先章节

```text
14 → 16
→ 17 → 18 → 19 → 21
→ 23 → 24 → 25
```

## 必备能力

- 什么问题值得做；
- 哪些是 Data Problem，哪些不是；
- hypothesis / pilot / confirmatory 分层；
- claim scope；
- data portfolio / ROI；
- research-to-production gate；
- decision rights / RACI；
- negative result governance。

## Figures

F8 / F9 / F10 / F11 / F14

---

# 12. 面试时如何描述自己的定位

## Data Research

> 我关注的不只是数据生产，而是从 capability gap 出发，设计 acquisition、supervision 和 curation，再用 matched-budget experiment 验证这批数据是否真的改变目标行为。

## Agent Data / Eval

> 我会把 Agent task 拆成 Task Contract、Environment、Trajectory、Outcome 和 Failure，优先用真实 environment state 和 verifier 作为证据，再决定 failure 应该转成什么数据或系统修复。

## Data Platform

> 我关注的是让高价值经验有稳定 identity、lineage、version 和 cost，使 raw evidence 可保留、derived view 可重建、失败可恢复，并能把训练结果回流到下一轮生产策略。

---

# 13. 角色不是章节边界

同一个成熟项目通常需要跨角色协同：

```text
Product
定义目标
↓
Research / Eval
定义证据和 protocol
↓
Data
构造 learning signal
↓
Platform / Ops
规模化生产
↓
Training
更新模型
↓
Monitoring
回收 fresh failure
```

最终目标不是“知道自己岗位那几章”，而是：

> **知道自己负责哪一段，同时理解 upstream / downstream 为什么需要你提供这些信息。**
