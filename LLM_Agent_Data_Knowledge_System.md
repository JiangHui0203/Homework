# 大模型与 Agent 数据知识体系

> **LLM / Agent Data Knowledge System**
>
> 当前状态：**Stable Mother Edition — V3.0**。25 章主体、7-Part 架构、Canonical Concepts、C1–C5、F1–F14、Retrieval Indexes、公式 / 数字口径 / 术语 / 视觉真源 / 关键链接验收与 0→25 连续通读均已完成；V3.x 在不改骨架的前提下增加 Practical Case Studies、Playbooks、Artifact Kit、Scenario Packs、Reference Layer 与 Visual Derivatives。
>
> 当前版本：**V3.0（2026-10-18）**
>
> 版本含义：核心架构、canonical definitions、Case IDs、Figure IDs 与 Retrieval Assets 已进入稳定维护阶段；后续内容默认通过现有 Chapter / Case / Figure / Index 演进，而不是继续无序扩章。
>
> 关联文档：[`Agent_Knowledge_System.md`](./Agent_Knowledge_System.md)

---

# 这套知识体系解决什么问题？

这不是一套“数据标注术语表”，而是一套围绕 **Learning System Design** 展开的 LLM / Agent Data 方法论。

核心问题可以压缩成六个：

1. **What should the model learn?** 模型应该学什么？
2. **From what experience?** 从什么经验里学？
3. **With what feedback?** 什么信号告诉它好坏？
4. **How do we know it learned?** 怎么证明真的学会？
5. **Is it worth the cost?** 值得这个成本吗？
6. **When should the system learn again?** 什么时候应该开始下一轮学习？

完整闭环是：

```text
真实问题 / 产品需求 / Capability Gap
        ↓
Task & Environment
        ↓
Human / Synthetic / Rollout / Production Experience
        ↓
Response / Reasoning / Agent Trajectory
        ↓
Evidence / Verifier / Judge / Human
        ↓
Failure Attribution / Credit
        ↓
Filtering / Routing / Mixture
        ↓
Training / Policy Update
        ↓
Frozen Evaluation
        ↓
Deploy / Monitor
        ↓
Fresh Failure / Drift
        ↺
```

> **数据不是流水线的起点，而是模型—环境—评测—训练闭环中的经验与学习信号。**

总图见：[F1 — Learning System Overview](./LLM_Agent_Data/figures/F1_Learning_System_Overview.md)。

---

# 全书结构

## Overview

- [第 0 章 Overview](./LLM_Agent_Data/00_Overview.md)

## Part I — Learning Signals

1. [Data Objects & Learning Signals](./LLM_Agent_Data/01_Data_Objects_and_Learning_Signals.md)
2. [Pretraining、Instruction、SFT 与 Post-training Data](./LLM_Agent_Data/02_Pretraining_Instruction_SFT_and_Post_training_Data.md)
3. [Preference Data、Reward 与 Feedback](./LLM_Agent_Data/03_Preference_Data_Reward_and_Feedback.md)
4. [Reasoning Data 与 Process Supervision](./LLM_Agent_Data/04_Reasoning_Data_and_Process_Supervision.md)
5. [Tool-use Data 与 Agent Trajectory Data](./LLM_Agent_Data/05_Tool_Use_and_Agent_Trajectory_Data.md)

```text
Example → Demonstration → Preference / Reward → Process Supervision → Agent Experience
```

Master Figures：F1 / F2 / F3。

## Part II — Data Acquisition & Selection

6. [Human Data](./LLM_Agent_Data/06_Human_Data_Annotation_and_Quality_Control.md)
7. [Synthetic Data](./LLM_Agent_Data/07_Synthetic_Data_Generation_and_Synthesis.md)
8. [Rollout / Rejection Sampling / Candidate Selection](./LLM_Agent_Data/08_Rollout_Rejection_Sampling_and_Candidate_Selection.md)
9. [Hard Case Mining 与 Curriculum](./LLM_Agent_Data/09_Hard_Case_Mining_and_Curriculum.md)

## Part III — Agent World & Diagnosis

10. [Agent Task Design](./LLM_Agent_Data/10_Agent_Task_Design.md)
11. [Environment Design](./LLM_Agent_Data/11_Environment_Design.md)
12. [Agent Trajectory Anatomy](./LLM_Agent_Data/12_Agent_Trajectory_Anatomy.md)
13. [Task Success 与 Credit Assignment](./LLM_Agent_Data/13_Task_Success_and_Credit_Assignment.md)
14. [Agent Failure Taxonomy](./LLM_Agent_Data/14_Agent_Failure_Taxonomy.md)

```text
Task → Environment → Trajectory → Outcome → Credit → Failure → Root Cause
```

Master Figures：F4 / F5 / F6。

## Part IV — Measurement

15. [Grader、Verifier 与 LLM-as-a-Judge](./LLM_Agent_Data/15_Grader_Verifier_and_LLM_as_a_Judge.md)
16. [Benchmark Design 与 Evaluation Protocol](./LLM_Agent_Data/16_Benchmark_Design_and_Evaluation_Protocol.md)

Master Figures：F7 / F8。

## Part V — Data Optimization & Lifecycle

17. [Data Flywheel](./LLM_Agent_Data/17_Data_Flywheel_and_Continuous_Improvement.md)
18. [Data Strategy 与 Data Valuation](./LLM_Agent_Data/18_Data_Strategy_and_Data_Valuation.md)
19. [Data Governance、Lineage 与 Reproducibility](./LLM_Agent_Data/19_Data_Governance_Lineage_and_Reproducibility.md)
20. [Data Quality、Filtering、Deduplication 与 Mixture](./LLM_Agent_Data/20_Data_Quality_Filtering_Deduplication_and_Mixture.md)
21. [Data Experiments](./LLM_Agent_Data/21_Data_Experiments_and_Causal_Validation.md)

```text
Flywheel → Strategy → Governance → Curation → Causal Validation
```

Master Figures：F9 / F10 / F11。

## Part VI — Data Operations

22. [Data Production System](./LLM_Agent_Data/22_Data_Production_System.md)
23. [Data Monitoring、Online Feedback 与 Drift Detection](./LLM_Agent_Data/23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
24. [End-to-End LLM / Agent Data Operating Model](./LLM_Agent_Data/24_End_to_End_LLM_Agent_Data_Operating_Model.md)

Master Figures：F12 / F13。

## Part VII — Synthesis

25. [LLM / Agent Data 全景能力地图与实战方法论](./LLM_Agent_Data/25_LLM_Agent_Data_Capability_Map_and_Practical_Methodology.md)

Master Figure：F14。

---

# 八套导航与调用资产

## 1. Canonical Concepts

- [Canonical Glossary & Notation](./LLM_Agent_Data/00_Glossary_and_Notation.md)
- [Concept Index](./LLM_Agent_Data/00_Concept_Index.md)

用于回答：

```text
这个术语在哪里定义？
在哪些章节应用？
它和相邻概念有什么边界？
```

## 2. Canonical Cases

- [Canonical Casebook](./LLM_Agent_Data/00_Canonical_Casebook.md)
- [Case Integration Index](./LLM_Agent_Data/00_Case_Integration_Index.md)
- [Cases Directory](./LLM_Agent_Data/cases/README.md)

稳定案例：

```text
C1 Order / Refund Agent
C2 Calendar / Meeting Agent
C3 File / Repository Agent
C4 Reasoning Continue / Repair
C5 Code / Execution Agent
```

## 3. Master Figures

- [Master Figure System](./LLM_Agent_Data/00_Master_Figure_System.md)
- [Figure Design Contract](./LLM_Agent_Data/00_Figure_Design_Contract.md)
- [Figure Index](./LLM_Agent_Data/figures/README.md)
- [Figure Integration Audit](./LLM_Agent_Data/00_Figure_Integration_Audit.md)

14 张 Master Figure 已完成 production refinement，并明确 canonical visual ownership；Ch14 / Ch15 / Ch19 的三处竞争性总图已收敛到 F6 / F7 / F11。

## 4. Role / Problem Retrieval

- [Role Index](./LLM_Agent_Data/00_Role_Index.md)
- [Problem Index](./LLM_Agent_Data/00_Problem_Index.md)

用于回答：

```text
“我是 Agent Data / Eval 岗，优先读什么？”
“Judge 分涨了但真实 success 不涨，先查什么？”
“线上 success 掉了，到底是不是模型退化？”
```

## 5. Interview / Execution Retrieval

- [Interview Index](./LLM_Agent_Data/00_Interview_Index.md)
- [Checklist Index](./LLM_Agent_Data/00_Checklist_Index.md)

用于：

```text
面试快速组织回答
项目立项 / review
数据生产 / 评测 / 上线前检查
30-minute quick diagnosis
```

## 6. Practical Use Layer

- [Practical Use Map](./LLM_Agent_Data/00_Practical_Use_Map.md)
- [Interview Pack](./LLM_Agent_Data/00_Interview_Pack.md)
- [Project Starter Pack](./LLM_Agent_Data/00_Project_Starter_Pack.md)
- [Practical Case Studies](./LLM_Agent_Data/case_studies/README.md)
  - [C1 — End-to-End Data Learning Loop](./LLM_Agent_Data/case_studies/C1_End_to_End_Walkthrough.md)
  - [C3 — Permission / Harness Ownership](./LLM_Agent_Data/case_studies/C3_Permission_Harness_Ownership_Walkthrough.md)
  - [C4 — Reasoning Intervention](./LLM_Agent_Data/case_studies/C4_Reasoning_Intervention_Walkthrough.md)
  - [C5 — Executable Truth / Verifier Coverage](./LLM_Agent_Data/case_studies/C5_Executable_Truth_Verifier_Coverage_Walkthrough.md)
- [Practical Playbooks](./LLM_Agent_Data/00_Practical_Playbooks.md)
- [Practical Artifact Kit](./LLM_Agent_Data/00_Practical_Artifact_Kit.md)
- [C1 Filled Artifact Pack](./LLM_Agent_Data/case_studies/C1_Artifact_Pack.md)
- [Condensed Guide](./LLM_Agent_Data/00_Condensed_Guide.md)

职责分别是：

```text
Interview Pack
→ 怎么准备、怎么讲、怎么接追问？

Project Starter Pack
→ Day 0 到 First Week 怎么按正确顺序启动项目？

Case Study
→ 一个真实问题怎样完整走完证据、诊断、数据、实验、生产和监控？

Playbook
→ 给我一个现实输入，今天按什么步骤推进到 Decision？

Artifact Kit
→ 每一步最终应该落下什么可审计工件？

Condensed Guide
→ 怎样在 30–90 分钟建立整套 shared mental model？
```

Scenario Pack 只负责装配现有资产，不重新定义 canonical concept。

## 7. Reference Layer

- [Reference & Source Policy](./LLM_Agent_Data/00_Reference_Source_Policy.md)
- [Canonical References](./LLM_Agent_Data/00_Canonical_References.md)

当前维护一组少而稳定的外部锚点，覆盖：

```text
Human Preference / RLHF
DPO
Process Supervision
Synthetic Instruction
Tool Use / ReAct
LLM-as-a-Judge
Benchmark Protocol
Agent / Web Environment Evaluation
Executable Evaluation
Dataset Governance
Contamination / Fresh Evaluation
```

固定边界：

```text
External Literature
≠ Internal Research Evidence
≠ Canonical Teaching Case
≠ Engineering Convention
```

外部论文不能替内部 Research Example 证明数字或结果。

## 8. Visual Derivative Layer

- [Visual Derivatives](./LLM_Agent_Data/visual_derivatives/README.md)
- [Visual Release Manifest](./LLM_Agent_Data/00_Visual_Release_Manifest.md)
- [Publication Visual Derivative Spec](./LLM_Agent_Data/00_Publication_Visual_Derivative_Spec.md)
- [Figure Presentation Kit](./LLM_Agent_Data/00_Figure_Presentation_Kit.md)

Level A 六张已经形成：

```text
Canonical Master Figure
→ D1 Publication SVG
→ D2 16:9 Progressive Reveal
→ D3 Quick-reference Card
```

并通过 source SHA 与 semantic acceptance 绑定。

---

# Verification & Acceptance

- [Verification Log](./LLM_Agent_Data/00_Verification_Log.md)
- [Cross-reference / Link Audit](./LLM_Agent_Data/00_Link_Audit.md)
- [Final Continuous Read-through Log](./LLM_Agent_Data/00_Final_Readthrough_Log.md)
- [Terminology & Style Audit](./LLM_Agent_Data/00_Terminology_Style_Audit.md)
- [Figure Integration Audit](./LLM_Agent_Data/00_Figure_Integration_Audit.md)
- [Release Readiness](./LLM_Agent_Data/00_Release_Readiness.md)

它们分别回答：

```text
公式 / 数字 / claim scope 是否安全？
主要路径和高风险链接是否真实存在？
0→25 连续阅读有没有章节断点？
canonical terminology 是否稳定？
Master Figure 与局部图是否争抢定义权？
母本当前还剩什么 blocker？
```

审计原则与正文一致：

> **验证到哪里，就只声明到哪里；部分验证不写成全量保证，没有来源的数字不因为“看起来熟悉”就标成已核验。**

当前有两个明确、非阻塞的 P1：

```text
More Thinking fixed-depth research numbers
→ 等待正式 paper / arXiv 或 internal frozen result summary 作为 Source Anchor

Exhaustive rendered heading-anchor proof
→ 当前 canonical file targets / high-risk paths 已通过；未来工具允许时可补全量 DOM-level deep-anchor checker
```

它们不影响 V3.0 的方法论架构与母本稳定性。

---

# 编辑基础设施

- [全书精修施工图](./LLM_Agent_Data/00_Book_Refinement_Blueprint.md)
- [Canonical Glossary & Notation](./LLM_Agent_Data/00_Glossary_and_Notation.md)
- [Canonical Casebook](./LLM_Agent_Data/00_Canonical_Casebook.md)
- [Case Integration Index](./LLM_Agent_Data/00_Case_Integration_Index.md)
- [Master Figure System](./LLM_Agent_Data/00_Master_Figure_System.md)
- [Reference & Source Policy](./LLM_Agent_Data/00_Reference_Source_Policy.md)
- [Canonical References](./LLM_Agent_Data/00_Canonical_References.md)
- [Visual Release Manifest](./LLM_Agent_Data/00_Visual_Release_Manifest.md)
- [Verification Log](./LLM_Agent_Data/00_Verification_Log.md)
- [Link Audit](./LLM_Agent_Data/00_Link_Audit.md)
- [Final Read-through Log](./LLM_Agent_Data/00_Final_Readthrough_Log.md)
- [Terminology & Style Audit](./LLM_Agent_Data/00_Terminology_Style_Audit.md)
- [Figure Integration Audit](./LLM_Agent_Data/00_Figure_Integration_Audit.md)
- [Release Readiness](./LLM_Agent_Data/00_Release_Readiness.md)

V3.0 acceptance：

```text
Structure / Concept Ownership
✓

Canonical Cases C1–C5
✓

Master Figures F1–F14
✓

Retrieval Indexes
✓

Header / Main Path Audit
✓

Formula / Metric Audit
✓

Research Number / Denominator Scope Audit
✓

Terminology / Style Audit
✓

Visual Canonicalization
✓

Final Case / Figure Link Spot-check
✓

Continuous Read-through Ch0–25
✓

Core Acceptance Blockers
0
```

---

# 推荐阅读路线

## 从零建立完整体系

```text
0
→ 1 → 2 → 3 → 4 → 5
→ 6 → 7 → 8 → 9
→ 10 → 11 → 12 → 13 → 14
→ 15 → 16
→ 17 → 18 → 19 → 20 → 21
→ 22 → 23 → 24
→ 25
```

## 大模型 / Agent 数据岗位面试

```text
Interview Pack
→ Condensed Guide
→ Level A Quick-reference / Presentation Kit
→ Interview Index
→ C1 / C3 / C4 / C5 Practical Studies
```

## Agent Data / Agent Evaluation

```text
1 → 5
→ 10 → 11 → 12 → 13 → 14
→ 15 → 16
→ 17 → 22 → 23
→ 25
```

## Reasoning / Test-time / Selector Research

```text
1 → 4
→ 8 → 9
→ 13
→ 15 → 16
→ 21
→ C4 Practical Walkthrough
```

## Data Platform / DataOps

```text
1 → 12
→ 19 → 20
→ 22 → 23 → 24
→ C3 Practical Walkthrough
```

## Eval / Verifier / Code Agent

```text
15 → 16 → 19 → 21 → 23
→ C5 Practical Walkthrough
```

## 今天就要开始做项目

```text
Project Starter Pack
→ Practical Use Map
→ Problem Index
→ Practical Playbook
→ Artifact Kit
→ 对应 Case Study
→ Canonical Chapter
```

---

# V3.0 以后怎样维护？

V3.0 不是“以后不再改”，而是：

> **骨架进入稳定期，新增知识优先进入已有 canonical owner，而不是静默改变概念或继续无边界扩章。**

兼容变化：

```text
补 Case variant
补 Practical Case Study
补 Playbook / Artifact Template
补 Scenario Pack
补局部解释
更新 bibliography / Source Anchor
补 external evidence
扩 Retrieval Index
优化 Master / derivative figure
新增 checklist item
修 broken link / typo
```

需要重新做 version review 的变化：

```text
改变 canonical concept definition
重编号章节
改变 C1–C5 stable ID semantics
改变 F1–F14 canonical relation
改变 Task / Case / Episode / Trajectory object model
改变 Tool / Harness / Environment boundary
```

原则：

> **内容可以继续成长，但骨架不能静默漂移。**

---

# 全书最终目标

希望形成的不是“记住 25 章术语”，而是一种稳定的问题解决能力：

```text
看到真实问题
↓
定位层级
↓
寻找证据
↓
判断 Root Cause / Owner
↓
选择 Data / Model / Tool / Harness / Product Intervention
↓
设计 Learning Signal
↓
Controlled Validation
↓
Scale / Stop
↓
Deploy / Monitor
↓
Learn Again
```

> **成熟的大模型数据能力，不是“拥有很多数据”，而是拥有一套能够持续把真实问题转化为可验证学习信号的 Learning System。**
