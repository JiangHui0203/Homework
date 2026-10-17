# LLM / Agent Data Knowledge System：全书精修施工图

> 状态：**Structural Editing Complete / Retrieval & Visual Refinement Next**
>
> 适用范围：`LLM_Agent_Data_Knowledge_System.md` + `LLM_Agent_Data/00_...` 至 `25_...`
>
> 原则：**完整定义只出现一次；dependent chapter 只讲当前场景的应用。先保证概念唯一归属，再做案例、图示、索引和事实核验。**

---

# 0. 当前施工状态

```text
Content Expansion
✓ 完成

Read-only Architecture Audit
✓ 完成

Landing Page / 7-Part Information Architecture
✓ 完成

00 Overview + Ch1–3 独立化
✓ 完成

Glossary / Notation
✓ 完成

Canonical Casebook
✓ 完成

Canonical Concept Ownership
✓ 完成

Foundational Consistency Pass
✓ Ch1 / 2 / 3

Canonical Chapter Stabilization
✓ Ch4 / 10 / 11 / 12 / 13 / 14 / 15 / 16 / 19

TRIM + LINK — Acquisition
✓ Ch5 / 6 / 7 / 8 / 9

TRIM + LINK — Lifecycle
✓ Ch17 / 18 / 20 / 21

TRIM + LINK — Operations
✓ Ch22 / 23 / 24

Synthesis Refactor
✓ Ch25

Next
→ Cross-reference / broken-link audit
→ Canonical Case C1–C5 全面接入
→ Master Figures
→ Concept / Role / Problem / Interview / Checklist Indexes
→ Fact / paper / number / formula verification
→ Final continuous read-through
```

也就是说：

> **1–25 章的书级结构、职责边界和核心术语骨架已经完成。后续不再做大规模章节重写。**

---

# 1. 最终书级结构

```text
Overview
└── Ch0  LLM / Agent Data 是什么

Part I — Learning Signals
├── Ch1  Data Objects & Learning Signals
├── Ch2  Pretraining / Instruction / SFT / Post-training
├── Ch3  Preference / Reward / Feedback
├── Ch4  Reasoning Data / Process Supervision
└── Ch5  Tool-use / Agent Trajectory Data

Part II — Data Acquisition & Selection
├── Ch6  Human Data
├── Ch7  Synthetic Data
├── Ch8  Rollout / Candidate Selection
└── Ch9  Hard Case Mining / Curriculum

Part III — Agent World & Diagnosis
├── Ch10 Task Design
├── Ch11 Environment Design
├── Ch12 Trajectory Anatomy
├── Ch13 Credit Assignment
└── Ch14 Failure Taxonomy

Part IV — Measurement
├── Ch15 Verifier / Grader / Judge
└── Ch16 Benchmark / Evaluation Protocol

Part V — Data Optimization & Lifecycle
├── Ch17 Data Flywheel
├── Ch18 Data Strategy / Valuation
├── Ch19 Governance / Lineage
├── Ch20 Quality / Filtering / Dedup / Mixture
└── Ch21 Data Experiments

Part VI — Data Operations
├── Ch22 Data Production System
├── Ch23 Monitoring / Drift
└── Ch24 End-to-End Operating Model

Part VII — Synthesis
└── Ch25 Capability Map / Practical Methodology
```

主线：

```text
What should the model learn?
↓
Where does experience come from?
↓
What world is the agent acting in?
↓
How do we know what happened?
↓
Which experience is worth learning?
↓
How do we operationalize it?
↓
How do we solve a real problem end-to-end?
```

---

# 2. Canonical Concept Ownership

| Concept | Owner |
|---|---:|
| Dataset / Sample / Task / Case / Episode / Trajectory | Ch1 |
| Pretraining / SFT / Post-training | Ch2 |
| Preference / Reward / Relative Feedback | Ch3 |
| Correctness / Risk / Recoverability / Repairability / Selectability | Ch4 |
| Tool-use / Agent Experience basics | Ch5 |
| Human Annotation / Gold / IAA / Adjudication | Ch6 |
| Synthetic Generation / Evolution | Ch7 |
| Candidate Pool / Best-of-N / Oracle / Selector | Ch8 |
| Hard Case / Frontier / Acquisition / Curriculum | Ch9 |
| Task Contract | Ch10 |
| Tool / Harness / Environment / World State | Ch11 |
| Typed Trajectory / Local State Lineage | Ch12 |
| Outcome / Reward / Credit / First Harmful / Last Recoverable | Ch13 |
| Symptom / Mechanism / Root Cause / Failure Owner | Ch14 |
| Evidence / Verifier / Grader / Judge | Ch15 |
| Benchmark / Protocol / Population / Statistics / Claim | Ch16 |
| Data Flywheel Orchestration | Ch17 |
| Data Value / ROI / Portfolio / Stop Rule | Ch18 |
| Identity / Provenance / Lineage / Versioning / Reproducibility | Ch19 |
| Quality / Filtering / Dedup / Mixture | Ch20 |
| Data Intervention / Causal Validation | Ch21 |
| Experience Manufacturing Infrastructure | Ch22 |
| Monitoring / Online Feedback / Drift | Ch23 |
| Organization Operating Model | Ch24 |
| Practitioner Operating System | Ch25 |

规则：

```text
Canonical Chapter = Definition
Dependent Chapter = Application + Link
```

---

# 3. 当前最重要的跨章链

## Learning Signal

```text
Ch1 Objects
→ Ch2 Training Purpose
→ Ch3 Relative Feedback
→ Ch4 Process State
→ Ch5 Agent Experience
```

## Agent Science

```text
Ch10 Task
→ Ch11 World / Tool / Harness
→ Ch12 Representation
→ Ch13 Credit
→ Ch14 Diagnosis
```

## Measurement

```text
Ch15 Who judges / with what evidence
→ Ch16 How to compare / what can be claimed
```

## Data Lifecycle

```text
Ch17 Flywheel
→ Ch18 Strategy
→ Ch19 Governance
→ Ch20 Curation
→ Ch21 Causal Validation
```

## Operations

```text
Ch22 Produce
→ Ch23 Sense Change
→ Ch24 Organize Team
→ Ch25 Apply as Practitioner
```

---

# 4. Canonical Cases

```text
C1 Order / Refund Agent
C2 Calendar / Meeting Agent
C3 File / Repository Agent
C4 Reasoning Continue / Repair
C5 Code / Execution Agent
```

下一阶段任务：

```text
统一 Case ID
统一 variant 命名
统一 Task / Case / Episode 表述
将散落示例尽量映射到 C1–C5
建立 Case Index
```

原则：

> **同一个 case 在不同章节承担不同分析角色，不再每章重新创造一个近似故事。**

---

# 5. Master Figure Plan

```text
F1  Learning System Overview
F2  Data Object / Learning Signal Evolution
F3  Correctness–Risk–Recoverability–Repairability–Selectability
F4  Agent Task–Environment–Trajectory
F5  Trajectory Anatomy
F6  Credit → Failure Causal Map
F7  Evidence → Verifier → Grader → Judge
F8  Frozen Benchmark / Evaluation Protocol
F9  Data Flywheel
F10 Data Strategy / Portfolio / ROI
F11 Governance / Lineage DAG
F12 Data Production System
F13 Monitoring / Drift Diagnostic Tree
F14 Operating Model + Capability Map
```

原则：

> **图用于压缩复杂关系，不用于装饰。**

---

# 6. Retrieval / Index Plan

后续新增的是导航资产，而不是新知识章节：

```text
Concept Index
Case Index
Role Index
Problem Index
Interview Index
Checklist Index
Figure Index
```

最终要支持：

```text
“Recoverability 在哪定义？”
“Judge 分数涨但线上不涨应该看什么？”
“Agent Data 面试优先读哪些章？”
“一个 Recovery Failure 从哪里一路追到 Data Experiment？”
```

---

# 7. Verification Plan

结构稳定后再做事实与引用审计：

```text
论文正式题名 / 副标题
作者 / 年份 / arXiv
Benchmark 名称
实验数字
公式符号
行业术语
Research Example claim scope
Broken Links / Anchors
```

重点：

```text
More Thinking 正式题名
RoTFuse / K17 阶段性 evidence 与 universal claim 的边界
```

Research case 统一标明：

```text
Research Example
Current Experimental Evidence
Not a Universal Claim
```

---

# 8. Derived Editions

母本最终稳定后再抽取：

```text
Interview Quick Reference
Project Checklist Edition
Learning Path Edition
```

所有衍生版本都引用母本，不形成新的事实源。

---

# 9. 完成标准

最终应能快速回答：

```text
一个术语在哪里定义？
一个概念为什么不会在多章重复定义？
一个 failure 应该读哪几章？
一个 Agent Data 项目从 Task 到 Monitoring 怎么走？
一个历史结论对应哪套数据、Judge 和 Protocol？
一个 Case 如何穿过 Task → Trajectory → Credit → Failure → Eval → Data → Production？
一个岗位应该走哪条阅读路线？
```

最终目标：

> **每个概念有唯一归属，每个章节有明确职责，每个案例可以跨章复用，每个结论能够找到证据，每一种读者都有清晰入口。**

---

# 10. 编辑总原则

1. **不为了简洁牺牲关键区分。**
2. **不为了完整在每章重新讲同一套定义。**
3. **不把 Research Example 写成未经验证的 Universal Claim。**
4. **不把 Model / Data / Eval / Tool / Harness / Environment Failure 混成一个问题。**
5. **不继续扩正文章节；新内容优先进入已有章、Casebook、Glossary、Figure 或 Index。**

当前一句话状态：

> **“书”已经搭完；下一阶段是让它变成真正好查、好读、好记、好用的知识系统。**