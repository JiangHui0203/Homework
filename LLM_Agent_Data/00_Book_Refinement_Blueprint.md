# LLM / Agent Data Knowledge System：全书精修施工图

> 状态：**Structure / Cases / Master Figures Complete — Retrieval Indexes Active**
>
> 适用范围：`LLM_Agent_Data_Knowledge_System.md` + `LLM_Agent_Data/00_...` 至 `25_...` + `cases/` + `figures/`
>
> 原则：**完整定义只出现一次；dependent chapter 只讲当前场景的应用。Concept、Case、Figure 三套 canonical asset 都必须有稳定 owner / ID / 语义。**

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

Canonical Case Infrastructure
✓ C1–C5 独立 case files
✓ Stable Variant IDs
✓ Case Integration Index
✓ Cases README

Master Figure System
✓ F1–F14 全部完成
✓ Figure Index
✓ Visual Grammar

Current
→ Retrieval Indexes

Next
→ Cross-reference / broken-link audit
→ Fact / paper / number / formula verification
→ Figure integration audit for old local diagrams
→ Final continuous read-through
```

当前阶段一句话：

> **正文、案例和视觉骨架已经稳定；现在要让整套知识从“可以阅读”升级为“可以按问题、角色和任务快速检索”。**

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

# 3. Canonical Case System

稳定案例：

```text
C1 Order / Refund Agent
C2 Calendar / Meeting Agent
C3 File / Repository Agent
C4 Reasoning Continue / Repair
C5 Code / Execution Agent
```

稳定 variant 示例：

```text
C1-VB = shipped / no refund allowed
C2-F3 = update success / notification missing
C3-F5 = tool truth failure / harness observation success
C4-SC = same authoritative prefix sibling set
C5-F2 = public tests pass / hidden test fail
```

规则：

> **Case ID 具有实验语义。关键条件改变时创建新 variant，不允许沿用旧 ID 偷换定义。**

基础设施：

```text
00_Canonical_Casebook.md
00_Case_Integration_Index.md
cases/README.md
cases/C1...C5.md
```

---

# 4. Master Figure System — COMPLETE

14 张图已全部完成：

```text
F1  Learning System Overview
F2  Data Object & Learning Signal Evolution
F3  Reasoning State Decision Stack
F4  Agent Task–Environment–Trajectory
F5  Trajectory Anatomy
F6  Credit → Failure Causal Map
F7  Evidence → Verifier → Grader → Judge
F8  Benchmark / Evaluation Protocol
F9  Data Flywheel
F10 Data Strategy / Portfolio / ROI
F11 Governance / Lineage DAG
F12 Data Production System
F13 Monitoring / Drift Diagnostic Tree
F14 Operating Model + Capability Map
```

视觉层形成的主链：

```text
F1 Learning System
↓
F2/F3 Learning + Reasoning
↓
F4/F5/F6 Agent World + Diagnosis
↓
F7/F8 Measurement
↓
F9/F10/F11 Lifecycle + Strategy + Governance
↓
F12/F13/F14 Production + Monitoring + Operating Model
```

规则：

```text
Master Figure = stable relationship model
Chapter-local Figure = local lens
```

下一阶段只做 Figure Integration Audit，不再无限新增总图。

---

# 5. 当前跨章主链

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

# 6. Retrieval / Index Plan — CURRENT

需要构建：

```text
Concept Index
Role Index
Problem Index
Interview Index
Checklist Index
```

Figure Index 与 Case Index 已由：

```text
figures/README.md
cases/README.md
00_Case_Integration_Index.md
```

承担。

目标：

```text
“Recoverability 在哪定义？”
“Judge 分数涨但线上不涨应该看什么？”
“Agent Data 面试优先读哪些章？”
“一个 Recovery Failure 从哪里一路追到 Data Experiment？”
“C3-F5 应该看哪些章节和哪张图？”
```

---

# 7. Verification Plan

Retrieval Index 稳定后，再做事实与引用审计：

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
一个 Case ID 对应什么稳定世界和 failure？
哪张 Master Figure 最适合解释这个关系？
一个 Agent Data 项目从 Task 到 Monitoring 怎么走？
一个历史结论对应哪套数据、Judge 和 Protocol？
一个岗位应该走哪条阅读路线？
```

最终目标：

> **每个概念有唯一归属，每个章节有明确职责，每个案例有稳定 ID，每张图有单一认知任务，每个结论能找到证据，每一种读者都有清晰入口。**

---

# 10. 编辑总原则

1. **不为了简洁牺牲关键区分。**
2. **不为了完整在每章重新讲同一套定义。**
3. **不把 Research Example 写成未经验证的 Universal Claim。**
4. **不把 Model / Data / Eval / Tool / Harness / Environment Failure 混成一个问题。**
5. **不继续扩正文章节；新内容优先进入已有章、Casebook、Glossary、Figure 或 Index。**
6. **图不承担装饰任务，只承担关系压缩任务。**
7. **Case ID 不允许语义漂移。**
8. **Index 负责检索，不重新创造定义。**

当前一句话状态：

> **“书”已经搭完，案例坐标系和视觉坐标系也已稳定；现在开始建设检索坐标系。**
