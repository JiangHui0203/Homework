# 大模型与 Agent 数据知识体系

> **LLM / Agent Data Knowledge System**
>
> 当前状态：25 章主体、结构性编辑、Canonical Cases 与 14 张 Master Figures 完成；进入 Retrieval Index / Verification / Final Read-through 阶段。
>
> 当前版本：V2.2（2026-10-18）
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

> **模型到底从什么经验、什么反馈中学习？**

1. [Data Objects & Learning Signals](./LLM_Agent_Data/01_Data_Objects_and_Learning_Signals.md)
2. [Pretraining、Instruction、SFT 与 Post-training Data](./LLM_Agent_Data/02_Pretraining_Instruction_SFT_and_Post_training_Data.md)
3. [Preference Data、Reward 与 Feedback](./LLM_Agent_Data/03_Preference_Data_Reward_and_Feedback.md)
4. [Reasoning Data 与 Process Supervision](./LLM_Agent_Data/04_Reasoning_Data_and_Process_Supervision.md)
5. [Tool-use Data 与 Agent Trajectory Data](./LLM_Agent_Data/05_Tool_Use_and_Agent_Trajectory_Data.md)

主线：

```text
Example
→ Demonstration
→ Preference / Reward
→ Process Supervision
→ State-conditioned Experience
→ Agent Trajectory
```

## Part II — Data Acquisition & Selection

> **这些经验如何被生产、扩展、选择？**

6. [Human Data](./LLM_Agent_Data/06_Human_Data_Annotation_and_Quality_Control.md)
7. [Synthetic Data](./LLM_Agent_Data/07_Synthetic_Data_Generation_and_Synthesis.md)
8. [Rollout / Rejection Sampling / Candidate Selection](./LLM_Agent_Data/08_Rollout_Rejection_Sampling_and_Candidate_Selection.md)
9. [Hard Case Mining 与 Curriculum](./LLM_Agent_Data/09_Hard_Case_Mining_and_Curriculum.md)

## Part III — Agent World & Diagnosis

> **Agent 在什么世界中做什么，以及失败到底发生在哪里？**

10. [Agent Task Design](./LLM_Agent_Data/10_Agent_Task_Design.md)
11. [Environment Design](./LLM_Agent_Data/11_Environment_Design.md)
12. [Agent Trajectory Anatomy](./LLM_Agent_Data/12_Agent_Trajectory_Anatomy.md)
13. [Task Success 与 Credit Assignment](./LLM_Agent_Data/13_Task_Success_and_Credit_Assignment.md)
14. [Agent Failure Taxonomy](./LLM_Agent_Data/14_Agent_Failure_Taxonomy.md)

核心链：

```text
Task → Environment → Trajectory → Outcome → Credit → Failure → Root Cause
```

Master Figures：

- [F4 — Agent Task–Environment–Trajectory](./LLM_Agent_Data/figures/F4_Agent_Task_Environment_Trajectory.md)
- [F5 — Trajectory Anatomy](./LLM_Agent_Data/figures/F5_Trajectory_Anatomy.md)
- [F6 — Credit → Failure Causal Map](./LLM_Agent_Data/figures/F6_Credit_to_Failure_Causal_Map.md)

## Part IV — Measurement

15. [Grader、Verifier 与 LLM-as-a-Judge](./LLM_Agent_Data/15_Grader_Verifier_and_LLM_as_a_Judge.md)
16. [Benchmark Design 与 Evaluation Protocol](./LLM_Agent_Data/16_Benchmark_Design_and_Evaluation_Protocol.md)

Master Figures：

- [F7 — Evidence → Verifier → Grader → Judge](./LLM_Agent_Data/figures/F7_Evidence_Verifier_Grader_Judge.md)
- [F8 — Benchmark / Evaluation Protocol](./LLM_Agent_Data/figures/F8_Benchmark_Evaluation_Protocol.md)

## Part V — Data Optimization & Lifecycle

17. [Data Flywheel](./LLM_Agent_Data/17_Data_Flywheel_and_Continuous_Improvement.md)
18. [Data Strategy 与 Data Valuation](./LLM_Agent_Data/18_Data_Strategy_and_Data_Valuation.md)
19. [Data Governance、Lineage 与 Reproducibility](./LLM_Agent_Data/19_Data_Governance_Lineage_and_Reproducibility.md)
20. [Data Quality、Filtering、Deduplication 与 Mixture](./LLM_Agent_Data/20_Data_Quality_Filtering_Deduplication_and_Mixture.md)
21. [Data Experiments](./LLM_Agent_Data/21_Data_Experiments_and_Causal_Validation.md)

Master Figures：

- [F9 — Data Flywheel](./LLM_Agent_Data/figures/F9_Data_Flywheel.md)
- [F10 — Data Strategy / Portfolio / ROI](./LLM_Agent_Data/figures/F10_Data_Strategy_Portfolio_ROI.md)
- [F11 — Governance / Lineage DAG](./LLM_Agent_Data/figures/F11_Governance_Lineage_DAG.md)

## Part VI — Data Operations

22. [Data Production System](./LLM_Agent_Data/22_Data_Production_System.md)
23. [Data Monitoring、Online Feedback 与 Drift Detection](./LLM_Agent_Data/23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
24. [End-to-End LLM / Agent Data Operating Model](./LLM_Agent_Data/24_End_to_End_LLM_Agent_Data_Operating_Model.md)

Master Figures：

- [F12 — Data Production System](./LLM_Agent_Data/figures/F12_Data_Production_System.md)
- [F13 — Monitoring / Drift Diagnostic Tree](./LLM_Agent_Data/figures/F13_Monitoring_Drift_Diagnostic_Tree.md)

## Part VII — Synthesis

25. [LLM / Agent Data 全景能力地图与实战方法论](./LLM_Agent_Data/25_LLM_Agent_Data_Capability_Map_and_Practical_Methodology.md)

Master Figure：[F14 — Operating Model + Capability Map](./LLM_Agent_Data/figures/F14_Operating_Model_and_Capability_Map.md)。

---

# 四套导航资产

## 1. Canonical Concepts

- [Canonical Glossary & Notation](./LLM_Agent_Data/00_Glossary_and_Notation.md)

解决：

```text
这个术语在哪里定义？
Outcome / Reward / Credit 有什么区别？
Tool / Harness / Environment 如何区分？
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

Case ID 已具有稳定语义，例如：

```text
C1-VB = shipped / no refund allowed
C3-F5 = tool truth failure / harness observation success
C4-SC = same authoritative prefix sibling set
C5-F2 = public tests pass / hidden test fail
```

## 3. Master Figures

- [Master Figure System](./LLM_Agent_Data/00_Master_Figure_System.md)
- [Figure Index](./LLM_Agent_Data/figures/README.md)

14 张 Master Figure 已全部完成：

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

## 4. Retrieval Indexes

正在建设：

```text
Concept Index
Role Index
Problem Index
Interview Index
Checklist Index
```

目标是从：

```text
“第几章讲什么？”
```

进一步升级成：

```text
“我现在遇到这个问题，应该去哪？”
```

---

# 编辑基础设施

- [全书精修施工图](./LLM_Agent_Data/00_Book_Refinement_Blueprint.md)
- [Canonical Glossary & Notation](./LLM_Agent_Data/00_Glossary_and_Notation.md)
- [Canonical Casebook](./LLM_Agent_Data/00_Canonical_Casebook.md)
- [Case Integration Index](./LLM_Agent_Data/00_Case_Integration_Index.md)
- [Master Figure System](./LLM_Agent_Data/00_Master_Figure_System.md)

当前精修顺序：

```text
Structure / Concept Ownership
✓

Canonical Cases
✓

Master Figures
✓

Retrieval Indexes
→ 当前阶段

Fact / Citation Verification
→ 后续

Final Continuous Read-through
→ 最终
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
1 → 2 → 3
→ 6 → 7 → 9
→ 15 → 16
→ 18 → 20 → 21
→ 25
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
→ 25
```

## Data Platform / DataOps

```text
1 → 12
→ 19 → 20
→ 22 → 23 → 24
```

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
