# 大模型与 Agent 数据知识体系

> **LLM / Agent Data Knowledge System**
>
> 当前状态：**Stable Mother Edition — V3.0 / V3.x Compatible Evolution**。25 章主体、7-Part 架构、Canonical Concepts、C1–C5、F1–F14、Retrieval Indexes 与 V3.0 验收均已完成；V3.x 已进一步增加 Practical Layer、Reference Layer、Visual Derivatives、Scenario Packs，并通过多轮异质场景压力测试。
>
> 基线版本：**V3.0（2026-10-18）**
>
> 当前维护模式：**Multi-scenario-tested / Use-driven Maintenance**。核心骨架不再继续扩张；新增能力默认进入已有 owner，场景特有结构使用 optional extension，只有经过跨项目压力测试的稳定 primitive 才允许 Promote Core。
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

完整闭环：

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

# 九套导航与调用资产

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

固定职责：

```text
Casebook
= Registry / Stable Invariants / Namespace

cases/C*.md
= Full Case Contract

Case Integration Index
= Chapter → Case / Variant routing
```

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

F1–F14 是 canonical visual ownership；局部图只能作为 analytical lens，不能和 Master Figure 争定义权。

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

固定职责：

```text
Interview Index
= 27-question retrieval / deeper expansion

Checklist Index
= stage-specific execution review / omission prevention
```

第一入口不要混淆：

```text
面试 / 答辩
→ Interview Pack

真实项目启动 / 选择五入口
→ Project Starter Pack

30-minute diagnosis
→ Condensed Guide §13 / Practical Use Map
```

## 6. Practical Use Layer

- [Practical Use Map](./LLM_Agent_Data/00_Practical_Use_Map.md)
- [Interview Pack](./LLM_Agent_Data/00_Interview_Pack.md)
- [Project Starter Pack](./LLM_Agent_Data/00_Project_Starter_Pack.md)
- [Practical Playbooks](./LLM_Agent_Data/00_Practical_Playbooks.md)
- [Practical Artifact Kit](./LLM_Agent_Data/00_Practical_Artifact_Kit.md)
- [Practical Case Studies](./LLM_Agent_Data/case_studies/README.md)
  - [C1 — End-to-End Data Learning Loop](./LLM_Agent_Data/case_studies/C1_End_to_End_Walkthrough.md)
  - [C3 — Permission / Harness Ownership](./LLM_Agent_Data/case_studies/C3_Permission_Harness_Ownership_Walkthrough.md)
  - [C4 — Reasoning Intervention](./LLM_Agent_Data/case_studies/C4_Reasoning_Intervention_Walkthrough.md)
  - [C5 — Executable Truth / Verifier Coverage](./LLM_Agent_Data/case_studies/C5_Executable_Truth_Verifier_Coverage_Walkthrough.md)
- [C1 Filled Artifact Pack](./LLM_Agent_Data/case_studies/C1_Artifact_Pack.md)
- [Condensed Guide](./LLM_Agent_Data/00_Condensed_Guide.md)

当前 Project Starter Pack 已采用五入口：

```text
Failure-led
Monitoring-led
Hypothesis-led
Evaluation-led
Asset-led / Curation-led
```

它们统一汇合到：

```text
Relevant Contract + Evidence
→ Controlled Change
→ Evaluation
→ Decision
→ Monitoring / Re-entry
```

固定边界：

```text
Artifact Chain
≠ 所有项目必须 A1 → A10 顺序填写
```

## 7. Reference Layer

- [Reference & Source Policy](./LLM_Agent_Data/00_Reference_Source_Policy.md)
- [Canonical References](./LLM_Agent_Data/00_Canonical_References.md)

固定区分：

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

Level A 六张已形成：

```text
Canonical Master Figure
→ D1 Publication SVG
→ D2 16:9 Progressive Reveal
→ D3 Quick-reference Card
```

并通过 source SHA 与 semantic acceptance 绑定。

## 9. Scenario Validation & Evolution

- [Stress Test — Round 1](./LLM_Agent_Data/00_Scenario_Pack_Stress_Test.md)
- [Stress Test — Round 2](./LLM_Agent_Data/00_Scenario_Pack_Stress_Test_Round_2.md)
- [Promotion Test](./LLM_Agent_Data/00_Scenario_Pack_Promotion_Test.md)
- [Candidate Extensions](./LLM_Agent_Data/00_Scenario_Pack_Candidate_Extensions.md)
- [Post-release Evolution Log](./LLM_Agent_Data/00_Post_Release_Evolution_Log.md)

已经实际压力测试：

```text
Interview follow-up
Selective reasoning / K17
Agent production incident
Judge / evaluator drift
Large-scale trajectory curation
Human Gold refresh
Synthetic production
```

Promotion 状态：

```text
E1 Entry Router
→ CORE

E2 A10-I Production Incident
→ OPTIONAL

E3 A5-M Measurement Bridge
→ OPTIONAL

E4 A6-C Curation Contract
→ OPTIONAL

E5 A5-H Human Annotation / Gold Contract
→ CANDIDATE
```

核心治理原则：

> **Core 小而稳定，Extension 条件明确，Case 保留局部复杂度。**

---

# Verification & Acceptance

- [Verification Log](./LLM_Agent_Data/00_Verification_Log.md)
- [Cross-reference / Link Audit](./LLM_Agent_Data/00_Link_Audit.md)
- [Final Continuous Read-through Log](./LLM_Agent_Data/00_Final_Readthrough_Log.md)
- [Terminology & Style Audit](./LLM_Agent_Data/00_Terminology_Style_Audit.md)
- [Figure Integration Audit](./LLM_Agent_Data/00_Figure_Integration_Audit.md)
- [Release Readiness](./LLM_Agent_Data/00_Release_Readiness.md)
- [Post-release Evolution Log](./LLM_Agent_Data/00_Post_Release_Evolution_Log.md)

V3.0 核心 acceptance blocker：

```text
0
```

当前有两个明确、非阻塞 P1：

```text
More Thinking fixed-depth research numbers
→ 等待正式 paper / arXiv 或 internal frozen result summary 作为 Source Anchor

Exhaustive rendered heading-anchor proof
→ canonical file targets / high-risk paths 已通过；未来工具允许时可补 DOM-level deep-anchor checker
```

固定审计原则：

> **验证到哪里，就只声明到哪里；历史 release snapshot 不因后续演进被静默回写。**

---

# 编辑与治理入口

- [全书精修施工图](./LLM_Agent_Data/00_Book_Refinement_Blueprint.md)
- [Post-release Evolution Log](./LLM_Agent_Data/00_Post_Release_Evolution_Log.md)
- [Canonical Glossary & Notation](./LLM_Agent_Data/00_Glossary_and_Notation.md)
- [Canonical Casebook](./LLM_Agent_Data/00_Canonical_Casebook.md)
- [Case Integration Index](./LLM_Agent_Data/00_Case_Integration_Index.md)
- [Master Figure System](./LLM_Agent_Data/00_Master_Figure_System.md)
- [Reference & Source Policy](./LLM_Agent_Data/00_Reference_Source_Policy.md)
- [Canonical References](./LLM_Agent_Data/00_Canonical_References.md)
- [Visual Release Manifest](./LLM_Agent_Data/00_Visual_Release_Manifest.md)
- [Scenario Candidate Extensions](./LLM_Agent_Data/00_Scenario_Pack_Candidate_Extensions.md)
- [Release Readiness](./LLM_Agent_Data/00_Release_Readiness.md)

---

# 推荐阅读 / 使用路线

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

## Reasoning / Test-time / Selector Research

```text
Project Starter Pack / Hypothesis-led
→ Ch4 → Ch8 → Ch9 → Ch13 → Ch16 → Ch21
→ A2-S Decision-state Contract
→ A7 Population / Information / Cost Ledger
→ C4 Practical Walkthrough
```

## Agent Production Incident

```text
Project Starter Pack / Monitoring-led
→ A10 first
→ A10-I if needed
→ Last-known-good / Change Ledger
→ F13 / Ch23
→ new A1 only if needed
```

## Eval / Judge / Human Gold

```text
Project Starter Pack / Evaluation-led
→ A5
→ A5-M if evaluator / rubric / guideline changes
→ Ch6 / Ch15 / Ch16 / Ch19 / Ch21
```

## Large-scale Trajectory / Data Curation

```text
Project Starter Pack / Asset-led
→ A11 Source Lineage
→ A6-C if needed
→ Ch20
→ Dataset View / Exposure
→ A7 downstream validation
```

## 今天就要开始做一个真实项目

```text
Project Starter Pack
→ 先选 Entry
→ Practical Use Map
→ Core Artifact
→ Conditional Extension if needed
→ Playbook / Case Study
→ A7 / A8
```

---

# V3.x 以后怎样维护？

现在默认不再问：

```text
“还能增加什么章节 / Figure / Pack / Card？”
```

而问：

```text
真实使用哪里卡？
这是 content bug、retrieval bug、evidence gap 还是 scenario-specific need？
已有 canonical owner 能不能解释？
是否只需要 optional extension？
是否跨异质项目重复出现到足以 Promote Core？
```

允许兼容演进：

```text
补 Case variant
补 Practical Case Study
补 Source Anchor
扩 Retrieval Index
更新 bibliography
修 typo / broken link
新增 optional extension
补 stress-test finding
```

需要 version review：

```text
改变 canonical concept definition
重编号章节
改变 C1–C5 stable ID semantics
改变 F1–F14 canonical relation
改变 Task / Case / Episode / Trajectory object model
改变 Tool / Harness / Environment boundary
改变 Outcome / Reward / Credit 等核心边界
```

原则：

> **内容可以继续成长，但骨架不能静默漂移；Release Snapshot 保留历史，Evolution Log 记录成长。**

---

# 全书最终目标

希望形成的不是“记住 25 章术语”，而是一种稳定的问题解决能力：

```text
看到真实问题
↓
先判正确 Entry
↓
定义 Identity / Population / State / Claim
↓
寻找 Evidence
↓
判断 Mechanism / Root Cause / Owner / Asset Quality
↓
选择 Data / Model / Policy / Tool / Harness / Evaluator / Product Intervention
↓
Controlled Validation
↓
Scale / Revise / Stop / Rollback
↓
Deploy / Monitor
↓
Learn Again
```

> **成熟的大模型数据能力，不是“拥有很多数据”，而是拥有一套能够把不同来源的真实问题稳定转成可验证 Evidence、受控 Intervention 与可审计 Decision 的 Learning System。**