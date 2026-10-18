# LLM / Agent Data Knowledge System：Concept Index

> 角色：按概念检索全书。每个概念标明 canonical definition、主要应用章节、相关 Master Figure / Case。
>
> 原则：**Index 只负责导航，不重新定义 canonical concept。**

---

# A

## Abstention

- Canonical：Ch6（人工标注）、Ch8（selector）、Ch15（evaluator）
- 关键区别：人工无法判断 / selector 不确定 / evaluator evidence 不足
- Figure：F7

## Action

- Canonical：Ch11–12
- 相关：Decision Intent ≠ Executed Action
- Figure：F4 / F5
- Case：C1-F1 / C3-F5

## Agent-visible State

- Canonical：Ch11
- Representation：Ch12
- Figure：F4 / F5
- 关键区别：World State ≠ Observation ≠ Agent-visible State

## Annotation Guideline

- Canonical：Ch6
- 相关：Boundary Case / Gold / IAA / Adjudication

---

# B

## Benchmark

- Canonical：Ch16
- 相关：Benchmark Object ≠ Evaluation Protocol ≠ Run ≠ Report
- Figure：F8

## Best-of-N

- Canonical：Ch8
- 相关：Oracle / Selector / Candidate Pool / Cost

---

# C

## Calibration

- Judge calibration：Ch15
- Threshold / score calibration：Ch23
- Human calibration：Ch6
- Figure：F7 / F13

## Candidate Pool

- Canonical：Ch8
- Reasoning same-prefix：Ch4 / C4-SC
- Figure：F3

## Case

- Canonical：Ch1
- Task semantics：Ch10
- 关键链：Task → Case → Episode → Trajectory
- Figure：F4

## Capability Drift

- Canonical：Ch23
- Figure：F13

## Capability Gap

- Flywheel：Ch17
- Strategy：Ch18
- Operating routing：Ch24
- Figure：F9 / F10 / F14

## Concept Drift

- Canonical：Ch23
- Figure：F13

## Contamination

- Evaluation contamination：Ch16
- Governance：Ch19
- Curation execution：Ch20
- Pretraining preview：Ch2

## Correctness

- Reasoning-state canonical：Ch4
- Evaluator evidence：Ch15
- Figure：F3 / F7
- 关键区别：Correctness ≠ Risk ≠ Recoverability

## Counterfactual

- Reasoning same-prefix：Ch4 / Ch8
- Credit：Ch13
- Data experiment：Ch21
- Case：C1-SC / C4-SC

## Credit

- Canonical：Ch13
- Figure：F6
- 关键区别：Outcome ≠ Reward ≠ Credit

## Curriculum

- Canonical：Ch9
- Data experiment：Ch21

---

# D

## Data Asset

- Canonical：Ch19
- Curation：Ch20
- Production：Ch22
- Figure：F11 / F12

## Data Batch

- Canonical：Ch19
- Strategy / experiment：Ch18 / Ch21

## Data Drift

- Canonical：Ch23
- Figure：F13

## Data Experiment

- Canonical：Ch21
- Figure：F8（通用 evaluation）/ F10（investment）
- 关键：Data Intervention → Model Change → Held-out Outcome

## Data Flywheel

- Canonical：Ch17
- Figure：F9

## Data Job

- Canonical：Ch22
- Figure：F12
- 关键区别：Production Request ≠ Job ≠ Artifact ≠ Dataset Record

## Data Lineage

- Canonical：Ch19
- Figure：F11

## Data Mixture

- Canonical：Ch20
- Strategy：Ch18
- Causal validation：Ch21

## Data Strategy

- Canonical：Ch18
- Figure：F10

## Dataset View

- Canonical：Ch19 / Ch22
- Figure：F11 / F12
- 关键：Source Assets + Build Recipe

## Decision

- Canonical semantics：Ch12
- Decision rights：Ch24
- Figure：F5 / F14

## Deduplication

- Canonical：Ch20
- 预训练 preview：Ch2
- Governance / contamination：Ch19

---

# E

## Environment

- Canonical：Ch11
- Figure：F4
- 关键：Tool ≠ Harness ≠ Environment

## Environment Feedback

- Canonical entry：Ch1
- Agent data：Ch5
- 关键：Environment Feedback ≠ automatically Reward

## Episode

- Canonical：Ch1
- Representation：Ch12

## Error

- Credit-local：Ch13
- Failure diagnosis：Ch14
- Figure：F6
- 关键：First Error ≠ First Harmful Action ≠ Root Cause

## Evidence

- Canonical：Ch15
- Figure：F7
- 关键：Evidence ≠ Judgment ≠ Label

---

# F

## Failure Drift

- Canonical：Ch23
- Figure：F13

## Failure Layer

- Canonical：Ch14
- Figure：F6
- 关键：Failure Layer ≠ Failure Owner

## Failure Owner

- Canonical：Ch14
- Operating routing：Ch24
- Figure：F6 / F14

## Failure Taxonomy

- Canonical：Ch14
- Monitoring：Ch23
- Operating routing：Ch24

## First Error

- Canonical：Ch13
- Figure：F6

## First Harmful Action

- Canonical：Ch13
- Figure：F6
- Case：C1-F1

## Frozen Protocol

- Canonical：Ch16
- Data experiment：Ch21
- Figure：F8

---

# G

## Gold Set

- Human annotation：Ch6
- Evaluator calibration：Ch15
- Governance：Ch19

## Grader

- Canonical：Ch15
- Figure：F7
- 关键：Verifier ⊂ Evaluator；Judge 是 interpretive evaluator

---

# H

## Hard Case

- Canonical：Ch9
- Data value：Ch18
- 关键：Hard ≠ Valuable

## Hard Negative

- Preference：Ch3
- Synthetic：Ch7
- Mining：Ch9

## Harness

- Canonical：Ch11
- Failure owner：Ch14
- Production：Ch22
- Monitoring：Ch23
- Figure：F4 / F6 / F13
- Case：C3-F5

## Human Gold

- Canonical：Ch6
- Meta-eval：Ch15

---

# I

## IAA / Inter-Annotator Agreement

- Canonical：Ch6

## Idempotency

- Environment / tool semantics：Ch11
- Production：Ch22
- Case：C3-F4

## Infrastructure Drift

- Canonical：Ch23
- Figure：F13

---

# J

## Judge

- Canonical：Ch15
- Monitoring / Judge Drift：Ch23
- Figure：F7 / F13
- 关键：Judge ≠ Ground Truth

## Judge Drift

- Canonical：Ch23
- Calibration：Ch15
- Figure：F13

---

# L

## Label

- Human annotation：Ch6
- Evaluator-derived label：Ch15
- Version / corrected label：Ch19

## Last Recoverable State

- Canonical：Ch13
- Figure：F6
- Case：C1-F1

## Learning Signal

- Canonical entry：Ch1
- Training stage：Ch2
- Preference：Ch3
- Figure：F1 / F2

## Lineage

- Trajectory-local：Ch12
- System-wide canonical：Ch19
- Figure：F5 / F11

---

# M

## Marginal Utility

- Canonical：Ch18
- Data experiment：Ch21
- Figure：F10

## Matched-budget Comparison

- Evaluation discipline：Ch16
- Data experiment：Ch21
- Figure：F8

## Mixture

- Canonical：Ch20
- Strategy：Ch18
- Experiment：Ch21

---

# O

## Observation

- Canonical：Ch11
- Representation：Ch12
- Figure：F4 / F5
- 关键：Tool Result ≠ Observation ≠ World State

## Oracle

- Canonical：Ch8
- 关键：Oracle existence ≠ Selector ability

## Outcome

- Canonical：Ch13
- Learning signal entry：Ch1
- Figure：F6
- 关键：Outcome ≠ Reward ≠ Credit

---

# P

## Point of No Return

- Canonical：Ch13
- Figure：F6

## Population Accounting

- Canonical：Ch16
- Monitoring selective systems：Ch23
- Figure：F8 / F13

## Preference Data

- Canonical：Ch3
- Candidate production：Ch8
- Human annotation：Ch6

## Process Supervision

- Canonical：Ch4
- Learning signal entry：Ch1

## Provenance

- Canonical：Ch19
- Figure：F11

---

# R

## Recoverability

- Canonical：Ch4
- Credit：Ch13
- Figure：F3 / F6
- 关键：Recoverability ≠ Repairability

## Repairability

- Canonical：Ch4
- Failure routing：Ch14
- Figure：F3 / F6

## Re-score / Re-run / Replay

- Canonical：Ch19
- Evaluation correction：Ch16
- Figure：F11

## Rescue / Harmful

- Counterfactual semantics：Ch4
- Candidate application：Ch8
- Evaluation：Ch16
- 关键：是相对 baseline intervention transition，不是 candidate 固有属性

## Reward

- Canonical：Ch3 / Ch13
- 关键：Reward ≠ Outcome ≠ Credit

## Risk

- Canonical：Ch4
- Monitoring：Ch23
- Figure：F3

## Root Cause

- Canonical：Ch14
- Figure：F6

---

# S

## Sample / Example

- Canonical：Ch1
- Figure：F2

## Selectability

- Canonical：Ch4
- Candidate selector：Ch8
- Figure：F3

## Selector

- Canonical：Ch8
- Reasoning semantics：Ch4
- Figure：F3

## SFT

- Canonical：Ch2
- Learning signal：Ch1
- Figure：F2

## Side Effect

- Task contract：Ch10
- Failure severity：Ch14
- Case：C1 / C3

## State

不要裸用。根据语义进入：

- World State：Ch11
- Environment State：Ch11
- Agent-visible State：Ch11
- Reasoning State：Ch4
- Working State：Glossary / relevant system
- Figure：F3 / F4 / F5

## Synthetic Data

- Canonical：Ch7
- Curation：Ch20
- Experiment：Ch21

---

# T

## Task

- Canonical object：Ch1
- Task Contract：Ch10
- Figure：F4

## Tool

- Canonical：Ch11
- Tool-use data：Ch5
- Figure：F4

## Trajectory

- Object entry：Ch1 / Ch5
- Canonical anatomy：Ch12
- Figure：F5

## Trigger Rate

- Selective inference：Ch4 / Ch8
- Evaluation denominator：Ch16
- Monitoring drift：Ch23
- Figure：F13

---

# V

## Verifier

- Canonical：Ch15
- Figure：F7
- Code example：C5

## Versioning

- Canonical：Ch19
- Figure：F11

---

# W

## World State

- Canonical：Ch11
- Figure：F4 / F5

---

# 快速区分表

```text
Task ≠ Case ≠ Episode ≠ Trajectory
World State ≠ Observation ≠ Agent-visible State
Decision Intent ≠ Executed Action
Outcome ≠ Reward ≠ Credit
First Error ≠ First Harmful Action ≠ Root Cause
Correctness ≠ Risk ≠ Recoverability ≠ Repairability ≠ Selectability
Verifier ≠ Grader ≠ Judge
Historical Decision ≠ Corrected Label ≠ Fresh Re-execution
Re-score ≠ Re-run ≠ Replay
Hard ≠ Valuable
High Confidence ≠ Correct
Training Data ≠ Raw Production Log
```

更完整定义见：[`Canonical Glossary`](./00_Glossary_and_Notation.md)。
