# LLM / Agent Data Knowledge System：全书精修施工图

> 状态：**Active Refinement / Execution Blueprint**
>
> 适用范围：`LLM_Agent_Data_Knowledge_System.md` + `LLM_Agent_Data/00_...` 至 `25_...`
>
> 原则：**先定结构，再改正文；先定概念归属，再做去重；先稳定 canonical chapter，再处理 dependent chapter；最后统一案例、图示、索引与事实引用。**
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
✓ Ch4 / 10 / 11 / 13 / 14 / 15 / 16 / 19

TRIM + LINK Round 1
✓ Ch5 / 6 / 7 / 8 / 9

Next
→ Ch12 / 17 / 18 / 20 / 21 / 22 / 23 / 24 / 25
→ 再回头统一 Ch1–3
→ Cross-reference audit
→ Case integration
→ Master figures
→ Indexes
→ Fact / citation verification
```

当前全书已经从“内容扩展阶段”进入：

> **Concept Ownership + Compression + Navigation 阶段。**

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
| Data Flywheel | 17 | Monitoring 交 Ch23 |
| Data Value / ROI / Portfolio / Stop Rule | 18 | Ch9 只做 acquisition candidate |
| Identity / Provenance / Lineage / Version / Re-score / Re-run | 19 | Ch6/12/16 只保留局部需求 |
| Quality / Filtering / Dedup / Mixture | 20 | Ch2/7 只做预告 |
| Data Intervention / Causal Validation | 21 | General eval statistics 交 Ch16 |
| Production System | 22 | Organization routing 交 Ch24 |
| Monitoring / Drift | 23 | Ch17 只说明 flywheel sensing |
| Operating Model | 24 | 负责团队 / 组织系统 |
| Integrated Problem Solving | 25 | 不再引入新概念 |

---

# 4. 已稳定的 Canonical Chapters

## Ch4 — Reasoning Data

已固定：

```text
Correctness
Risk
Recoverability
Repairability
Selectability
```

并固定：

```text
Low confidence ≠ Wrong ≠ Worth repairing
Future outcome = offline supervision, not online feature
```

状态：`DONE — canonical definition stable`

---

## Ch10 — Agent Task Design

已固定：

```text
Prompt → Task → Case → Episode → Trajectory → Benchmark Case
```

以及 Task Contract：

```text
Goal
Initial State
Hidden State
Tools
Permissions
Constraints
Success Predicate
Forbidden Side Effects
Termination
Verifier Contract
```

状态：`DONE`

---

## Ch11 — Environment Design

已固定：

```text
Tool = Action Interface
Harness = Runtime Orchestration
Environment = World + Transition
Observation = Agent-visible feedback
```

以及：

```text
World State ≠ Observation ≠ Agent-visible State
```

状态：`DONE`

---

## Ch13 — Credit Assignment

已固定因果链：

```text
Outcome Verification
→ Failure Attribution
→ First Error
→ First Harmful Action
→ Recoverability / Repairability
→ Last Recoverable State / Point of No Return
→ Counterfactual Credit
→ Learning Signal
```

状态：`DONE`

---

## Ch14 — Failure Taxonomy

已固定：

```text
Outcome
→ Symptom
→ Localization
→ Mechanism
→ Root Cause
→ Failure Owner
→ Severity / Detectability
→ Repairability
→ Intervention Routing
```

关键边界：

```text
Failure Layer ≠ Failure Owner
```

状态：`DONE`

---

## Ch15 — Grader / Verifier / Judge

已固定 measurement chain：

```text
Evidence
→ Evaluator
→ Raw Judgment
→ Parsed Judgment
→ Derived Label
→ Final Decision
```

并正式允许：

```text
UNRESOLVED / ABSTAIN
```

状态：`DONE`

---

## Ch16 — Benchmark / Evaluation Protocol

已固定：

```text
Benchmark Object
Protocol
Run
Report
```

以及：

```text
Population Accounting
Denominator Discipline
Paired / Matched Comparison
Budget Matching
Cluster-aware Uncertainty
Claim Scope
```

状态：`DONE`

---

## Ch19 — Governance / Lineage

已固定：

```text
Identity
Provenance
Lineage
Versioning
Reproducibility
```

以及：

```text
Historical Decision ≠ Corrected Label ≠ Fresh Re-execution
Re-score ≠ Re-run ≠ Replay
```

状态：`DONE`

---

# 5. TRIM + LINK Round 1 — 已完成

## Ch5 — Tool-use / Agent Trajectory

现在只负责：

```text
Function Calling ⊂ Tool Use ⊂ Agent Trajectory
七类 Tool-use Decision
Action ↔ Observation
Agent Experience Object
One Episode → Multiple Derived Views
```

Credit / Failure / Benchmark / Governance 已改成 LINK。

状态：`DONE`

---

## Ch6 — Human Data

现在只负责：

```text
Staffing
Guideline
Boundary Case
Abstention
Gold
IAA
Calibration
Adjudication
Expertise Routing
Human + AI
```

Label Versioning / Corrected Label / Historical Decision 已归 Ch19。

状态：`DONE`

---

## Ch7 — Synthetic Data

现在只负责：

```text
Task / Response / Reasoning / Trajectory / Environment / User Synthesis
Teacher
Task Evolution
Hard Negative
Executed Synthetic Trajectory
Failure-driven Synthesis
```

Dedup / Contamination / Lineage / Mixture 已归 Ch19 / Ch20。

状态：`DONE`

---

## Ch8 — Rollout / Candidate Selection

现在只负责：

```text
Candidate Pool
Generation
Oracle
Selector
Rejection / Routing
Abstention
Dynamic N
Same-state Candidate
```

Rescue / Harmful 定义引用 Ch4 / Ch13；统计 protocol 引用 Ch16。

状态：`DONE`

---

## Ch9 — Hard Case Mining / Curriculum

现在只负责：

```text
Model-hard / State-hard
Capability Frontier
Uncertainty
Disagreement
Near-miss
Adversarial Mining
Active Learning
Curriculum
Trigger Bias
```

正式 Data Value / ROI / Portfolio / Stop Rule 已归 Ch18。

状态：`DONE`

---

# 6. 下一轮施工对象

推荐顺序：

```text
1. Ch12 Trajectory Anatomy
   → 将 system-wide lineage 收回 Ch19
   → 与 Ch11 state terminology 对齐

2. Ch17 Data Flywheel
   → active learning 链 Ch9
   → valuation 链 Ch18
   → monitoring 链 Ch23

3. Ch18 Data Strategy
   → 正式拥有 ROI / Portfolio / Stop Rule
   → mixture 技术细节链 Ch20

4. Ch20 Quality / Filtering / Dedup / Mixture
   → 正式拥有 curation layer

5. Ch21 Data Experiments
   → 只负责 Data Intervention 的因果验证
   → general benchmark statistics 链 Ch16

6. Ch22–24
   → 去掉 governance / evaluation / flywheel 的重复定义
   → 只保留 Production / Monitoring / Organization 独有部分

7. Ch25
   → 全面改成调用式 synthesis
   → 不重新定义前 24 章

8. Ch1–3
   → 最后一轮基础术语统一
```

---

# 7. Canonical Case 体系

正式维护 5 个贯穿案例：

```text
C1 Order / Refund Agent
C2 Calendar / Meeting Agent
C3 File / Repository Agent
C4 Reasoning Continue / Repair
C5 Code / Execution Agent
```

原则：

> 同一个 case 在不同章节承担不同分析角色，而不是每章重新发明故事。

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

图的原则：

> **压缩关系，不做装饰。**

---

# 9. Cross-reference Style

统一使用：

```text
> 关于 X 的 canonical definition 见第 N 章。本节只讨论 X 在当前问题中的应用。
```

或：

```text
这里沿用第 4 章的定义：Risk ≠ Correctness ≠ Recoverability。
```

规则：

```text
Canonical Chapter = Definition
Dependent Chapter = Application
```

---

# 10. 后续阶段

```text
Phase A — Canonical + TRIM/LINK
当前进行中

Phase B — Canonical Cases
统一 C1–C5 ID、variant、引用方式

Phase C — Visual System
统一 Master Figures

Phase D — Navigation
Concept Index
Role Index
Problem Index
Interview Index
Checklist Index

Phase E — Verification
论文题名
作者 / 年份 / arXiv
Benchmark 名称
实验数字
公式 / 术语
Broken Links / Anchors

Phase F — Derived Editions
Interview Quick Reference
Project Checklist Edition
Learning Path Edition
```

---

# 11. 最终完成标准

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

# 12. 编辑总原则

1. **不为了简洁牺牲关键区分。**
2. **不为了完整在每章重新讲同一套定义。**
3. **不把 Research Example 写成未经验证的 Universal Claim。**
4. **不把 Model / Data / Eval / Tool / Harness / Environment failure 混成一个问题。**
5. **不继续扩正文章节；新内容优先进入已有章、Casebook、Glossary、Figure 或 Index。**

一句话总结：

> **现在的目标不是继续“写知识”，而是让已有知识变成一套可以被稳定调用的系统。**
