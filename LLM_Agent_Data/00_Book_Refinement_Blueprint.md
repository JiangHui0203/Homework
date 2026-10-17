# LLM / Agent Data Knowledge System：全书精修施工图

> 状态：**Active Refinement / Structural Editing Complete**
>
> 适用范围：`LLM_Agent_Data_Knowledge_System.md` + `LLM_Agent_Data/00_...` 至 `25_...`
>
> 原则：**先定结构，再改正文；先定概念归属，再做去重；先稳定 canonical chapter，再处理 dependent chapter；最后统一基础术语、案例、图示、索引与事实引用。**
>
> 本文件不是正文。它负责记录全书精修的目标、职责边界、施工顺序和当前进度。

---

# 0. 当前施工状态

```text
Content Expansion
✓ 完成

Read-only Architecture Audit
✓ 完成

Information Architecture / Landing Page
✓ 完成

00 Overview + Ch1–3 独立化
✓ 完成

Glossary / Notation
✓ 完成

Canonical Casebook
✓ 完成

Canonical Concept Ownership
✓ 完成

Canonical Chapter Stabilization
✓ Ch4 / 10 / 11 / 12 / 13 / 14 / 15 / 16 / 19

TRIM + LINK — Data Acquisition
✓ Ch5 / 6 / 7 / 8 / 9

TRIM + LINK — Data Lifecycle
✓ Ch17 / 18 / 20 / 21

TRIM + LINK — Data Operations
✓ Ch22 / 23 / 24

Synthesis Refactor
✓ Ch25

Next
→ Ch1–3 基础术语 / 职责一致性 pass
→ 全书 Cross-reference / broken-link audit
→ Canonical Case C1–C5 全面接入
→ Master Figures
→ Concept / Role / Problem / Interview / Checklist Indexes
→ Fact / paper / number / formula verification
→ Final continuous read-through
```

当前已经完成：

> **Information Architecture + Canonical Ownership + Cross-chapter Responsibility Refactor。**

接下来不再做大规模章节职责重写，而进入：

> **Consistency + Retrieval + Visual + Verification 阶段。**

---

# 1. 编辑动作标签

| 标签 | 含义 |
|---|---|
| `KEEP` | 保留现有核心内容 |
| `TRIM` | 压缩重复解释，不删除核心思想 |
| `MOVE` | 内容归回更合适的 canonical chapter |
| `LINK` | 用交叉引用替代重复完整解释 |
| `UNIFY` | 统一术语、公式、案例或格式 |
| `VERIFY` | 后续做事实、论文、数字、引用核验 |
| `ADD INDEX` | 增加概念 / 岗位 / 问题 / 面试索引 |
| `ADD CASE` | 接入 canonical case |
| `ADD FIGURE` | 接入 master figure |

核心纪律：

> **完整定义只出现一次；dependent chapter 只保留当前场景里的应用。**

---

# 2. 最终书级结构

```text
Overview
└── 0. LLM / Agent Data 是什么

Part I — Learning Signals
├── 1. Data Objects & Learning Signals
├── 2. Pretraining / Instruction / SFT / Post-training
├── 3. Preference / Reward / Feedback
├── 4. Reasoning Data / Process Supervision
└── 5. Tool-use / Agent Trajectory Data

Part II — Data Acquisition & Selection
├── 6. Human Data
├── 7. Synthetic Data
├── 8. Rollout / Rejection Sampling / Candidate Selection
└── 9. Hard Case Mining / Curriculum

Part III — Agent World & Diagnosis
├── 10. Agent Task Design
├── 11. Environment Design
├── 12. Agent Trajectory Anatomy
├── 13. Task Success / Credit Assignment
└── 14. Agent Failure Taxonomy

Part IV — Measurement
├── 15. Grader / Verifier / LLM-as-a-Judge
└── 16. Benchmark Design / Evaluation Protocol

Part V — Data Optimization & Lifecycle
├── 17. Data Flywheel
├── 18. Data Strategy / Data Valuation
├── 19. Governance / Lineage / Reproducibility
├── 20. Quality / Filtering / Dedup / Mixture
└── 21. Data Experiments

Part VI — Data Operations
├── 22. Data Production System
├── 23. Monitoring / Online Feedback / Drift
└── 24. End-to-End Operating Model

Part VII — Synthesis
└── 25. Capability Map / Practical Methodology
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

# 3. Canonical Concept Ownership Map

| Canonical Concept | Owner | Dependent chapters 应如何处理 |
|---|---:|---|
| Dataset / Sample / Task / Case / Episode / Trajectory | 1 | 引用基础对象定义 |
| Pretraining / SFT / Post-training | 2 | 引用，不重复训练阶段定义 |
| Preference / Reward / Feedback | 3 | Evaluator 交 Ch15；Credit 交 Ch13 |
| Correctness / Risk / Recoverability / Repairability / Selectability | 4 | Ch8/9/13/16 只应用 |
| Tool-use / Agent Experience basics | 5 | Ch10–14 进入专业分解 |
| Human Annotation / Gold / IAA / Adjudication | 6 | 系统治理交 Ch19 |
| Synthetic Generation / Evolution | 7 | Filtering / Dedup / Mixture 交 Ch20 |
| Rollout Pool / Best-of-N / Oracle / Selector | 8 | 统计 protocol 交 Ch16 |
| Hard Case / Frontier / Acquisition / Curriculum | 9 | Data ROI / Portfolio 交 Ch18 |
| Task Contract | 10 | 全书统一引用 |
| Tool / Harness / Environment / World State | 11 | 全书统一引用 |
| Typed Trajectory / Event / Local State Lineage | 12 | System lineage 交 Ch19 |
| Outcome / Reward / Credit / First Harmful / Last Recoverable | 13 | Failure diagnosis 交 Ch14 |
| Symptom / Mechanism / Root Cause / Failure Owner | 14 | 全书唯一完整 failure taxonomy |
| Evidence / Verifier / Grader / Judge | 15 | Benchmark protocol 交 Ch16 |
| Benchmark / Protocol / Run / Population / Statistics / Claim | 16 | Data causal experiment 交 Ch21 |
| Data Flywheel Orchestration | 17 | acquisition / valuation / drift 链到各 owner |
| Data Value / ROI / Portfolio / Stop Rule | 18 | Ch9 只做 acquisition candidate |
| Identity / Provenance / Lineage / Version / Re-score / Re-run | 19 | Ch6/12/16/22 只保留局部需求 |
| Quality / Filtering / Dedup / Mixture | 20 | Ch2/7 只作预告 |
| Data Intervention / Causal Validation | 21 | General eval statistics 交 Ch16 |
| Experience Manufacturing Infrastructure | 22 | Organization routing 交 Ch24 |
| Monitoring / Online Feedback / Drift | 23 | Ch17 只说明 sensing interface |
| Organization Operating Model | 24 | Owner / Gate / Handoff / Decision Right |
| Practitioner Operating System | 25 | 只调用前 24 章，不引入新 canonical concept |

---

# 4. 已完成的“承重墙”

## Ch4 — Reasoning State Semantics

```text
Correctness
Risk
Recoverability
Repairability
Selectability
```

关键纪律：

```text
Low confidence ≠ Wrong ≠ Worth repairing
Future outcome = offline supervision, not online feature
```

状态：`DONE`

## Ch10 — Task Contract

```text
Prompt → Task → Case → Episode → Trajectory → Benchmark Case
```

状态：`DONE`

## Ch11 — Environment / Tool / Harness

```text
Tool = Action Interface
Harness = Runtime Orchestration
Environment = World + Transition
Observation = Feedback
```

状态：`DONE`

## Ch12 — Trajectory Representation

```text
Typed Event Log
+
State Lineage
+
Execution Evidence
```

并固定：

```text
World / Environment / Agent-visible / Working / Memory
Context ≠ State
Decision Intent ≠ Executed Action
Agent-visible Trace ≠ Researcher-visible Trace
```

状态：`DONE`

## Ch13 — Credit Assignment

```text
Outcome
→ First Error
→ First Harmful
→ Recoverability / Repairability
→ Last Recoverable / Point of No Return
→ Counterfactual Credit
```

状态：`DONE`

## Ch14 — Failure Diagnosis

```text
Symptom
→ Mechanism
→ Root Cause
→ Failure Owner
→ Severity / Detectability
→ Intervention Routing
```

状态：`DONE`

## Ch15 — Measurement Instrument

```text
Evidence
→ Evaluator
→ Raw Judgment
→ Derived Label
→ Final Decision
```

状态：`DONE`

## Ch16 — Evaluation Protocol

```text
Benchmark Object
Protocol
Run
Report
Population
Budget
Statistics
Claim Scope
```

状态：`DONE`

## Ch19 — Governance

```text
Identity
Provenance
Lineage
Versioning
Reproducibility
```

状态：`DONE`

---

# 5. 已完成的 Dependent Chapter 收口

## Ch5–9 — Acquisition Layer

```text
Ch5 = Agent Experience Object
Ch6 = Human Standard / Annotation
Ch7 = Experience Synthesis
Ch8 = Candidate Pool / Selection
Ch9 = Acquisition / Frontier
```

状态：`DONE`

## Ch17–21 — Data Lifecycle

```text
Ch17 = Flywheel Orchestration
Ch18 = Resource Allocation / Valuation
Ch19 = Governance
Ch20 = Curation / Mixture
Ch21 = Causal Data Experiment
```

状态：`DONE`

## Ch22–24 — Operations

```text
Ch22 = Stable Production
Ch23 = Sensing / Drift
Ch24 = Team Operating Model
```

状态：`DONE`

## Ch25 — Synthesis

```text
Capability Map
Problem Routing
Data Intervention Tree
30-minute Diagnosis
Canonical Case
Project Checklist
```

不再重新定义前 24 章。

状态：`DONE`

---

# 6. 下一阶段：Consistency Pass

剩余第一优先级不是继续改后半本，而是回到基础章节：

```text
Ch1
Dataset / Sample / Task / Case / Episode / Trajectory

Ch2
Pretraining / SFT / Post-training / Data Purpose

Ch3
Preference / Reward / Feedback
```

目标：

```text
与 Glossary 完全对齐
与 Ch10 / 13 / 15 边界完全对齐
修复旧交叉引用
不提前深讲 Ch15 / 20
```

完成后，1–25 的术语骨架才真正闭合。

---

# 7. Canonical Case Integration

正式维护：

```text
C1 Order / Refund Agent
C2 Calendar / Meeting Agent
C3 File / Repository Agent
C4 Reasoning Continue / Repair
C5 Code / Execution Agent
```

下一阶段不再大量创造新故事，而是：

```text
给已有案例统一 ID
统一 variant 命名
跨章复用同一 case
补 Case Index
```

原则：

> **同一个 Case 在不同章节承担不同分析角色。**

---

# 8. Master Figure 计划

最终维护约 14 张全书级 Master Figure：

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

> **图压缩关系，不承担装饰作用。**

---

# 9. Navigation / Retrieval Assets

后续新增的不是正文，而是索引：

```text
Concept Index
Role Index
Problem Index
Interview Index
Checklist Index
Case Index
Figure Index
```

目标是让用户不需要线性读完整本书，也能快速找到：

```text
“这个概念在哪里定义？”
“这个 failure 应该读哪几章？”
“我面试 Agent Data 应该走哪条路线？”
```

---

# 10. Cross-reference Audit

统一规则：

```text
Canonical Chapter = Definition
Dependent Chapter = Application
```

交叉引用应明确写：

```text
关于 X 的 canonical definition 见第 N 章；本节只讨论 X 在当前问题中的应用。
```

需要最终检查：

```text
旧 root links
broken chapter links
old chapter names
stale section references
missing glossary / casebook references
```

---

# 11. Verification 阶段

正文结构稳定以后再做：

```text
论文正式题名 / 副标题
作者 / 年份 / arXiv
Benchmark 名称
实验数字
公式符号
非标准行业术语
Research Example 的 claim scope
Broken Links / Anchors
```

重点：

```text
More Thinking 正式题名
RoTFuse / K17 阶段性结果 vs 普遍结论
```

统一标记：

```text
Research Example
Current Experimental Evidence
Not a Universal Claim
```

---

# 12. Derived Editions

母本稳定后再抽取：

```text
Interview Quick Reference
Project Checklist Edition
Learning Path Edition
```

原则是：

> **所有衍生版本都从母本抽取，不形成新的知识事实源。**

---

# 13. 最终完成标准

精修完成后，应能快速回答：

```text
一个术语在哪里定义？
一个概念为什么不会在五章里重复定义？
一个 failure 应该读哪几章？
一个 Agent data 项目从 Task 到 Monitoring 怎么走？
一个历史结论对应哪套数据、Judge 和 protocol？
一个 case 如何穿过 Task → Trajectory → Credit → Failure → Eval → Data → Production？
一个岗位应该走哪条阅读路径？
```

最终目标不是知识库更长，而是：

> **每个概念有唯一归属，每个章节有明确职责，每个案例可以跨章复用，每个结论能够找到证据，每一种读者都有清晰入口。**

---

# 14. 编辑总原则

1. **不为了简洁牺牲关键区分。**
2. **不为了完整在每章重新讲同一套定义。**
3. **不把 Research Example 写成未经验证的 Universal Claim。**
4. **不把 Model / Data / Eval / Tool / Harness / Environment failure 混成一个问题。**
5. **不继续扩正文章节；新内容优先进入已有章、Casebook、Glossary、Figure 或 Index。**

一句话总结当前状态：

> **书的骨架与章节职责已经基本完成；接下来要做的是让它更一致、更可查、更可视化，并完成事实与引用核验。**