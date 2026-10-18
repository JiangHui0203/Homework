# 大模型与 Agent 数据知识体系

> **LLM / Agent Data Knowledge System**
>
> 当前状态：25 章主体与结构性编辑完成，进入 Case / Figure / Index / Verification 精修阶段。
>
> 当前版本：V2.1（2026-10-18）
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

- [第 0 章 Overview：这套 LLM / Agent Data 知识体系到底研究什么？](./LLM_Agent_Data/00_Overview.md)

---

## Part I — Learning Signals

> **模型到底从什么经验、什么反馈中学习？**

1. [从 Sample 到 Trajectory：数据对象与 Learning Signal](./LLM_Agent_Data/01_Data_Objects_and_Learning_Signals.md)
2. [Pretraining、Instruction、SFT 与 Post-training Data](./LLM_Agent_Data/02_Pretraining_Instruction_SFT_and_Post_training_Data.md)
3. [Preference Data、Reward 与 Feedback](./LLM_Agent_Data/03_Preference_Data_Reward_and_Feedback.md)
4. [Reasoning Data 与 Process Supervision](./LLM_Agent_Data/04_Reasoning_Data_and_Process_Supervision.md)
5. [Tool-use Data 与 Agent Trajectory Data](./LLM_Agent_Data/05_Tool_Use_and_Agent_Trajectory_Data.md)

主线：

```text
Example
↓
Demonstration
↓
Preference / Reward
↓
Process Supervision
↓
State-conditioned Experience
↓
Agent Trajectory
```

---

## Part II — Data Acquisition & Selection

> **这些经验如何被生产、扩展、选择？**

6. [Human Data：人工标注、专家标注与质量控制](./LLM_Agent_Data/06_Human_Data_Annotation_and_Quality_Control.md)
7. [Synthetic Data：模型生成数据、任务演化与环境合成](./LLM_Agent_Data/07_Synthetic_Data_Generation_and_Synthesis.md)
8. [Rollout、Rejection Sampling 与 Candidate Selection](./LLM_Agent_Data/08_Rollout_Rejection_Sampling_and_Candidate_Selection.md)
9. [Hard Case Mining 与 Curriculum](./LLM_Agent_Data/09_Hard_Case_Mining_and_Curriculum.md)

主线：

```text
Human / Expert
+
Teacher / Program / Simulator
+
Current-policy Rollout
        ↓
Candidate / Failure / Frontier
        ↓
Verify / Select / Mine
        ↓
High-value Experience
```

---

## Part III — Agent World & Diagnosis

> **Agent 在什么世界中做什么，以及失败到底发生在哪里？**

10. [Agent Task Design：任务定义、难度控制与可验证性](./LLM_Agent_Data/10_Agent_Task_Design.md)
11. [Environment Design：状态、转移、重置与可复现 Agent 世界](./LLM_Agent_Data/11_Environment_Design.md)
12. [Agent Trajectory Anatomy：状态、事件、记忆、分支与可审计轨迹](./LLM_Agent_Data/12_Agent_Trajectory_Anatomy.md)
13. [Task Success 与 Credit Assignment：从终局结果到中间决策归因](./LLM_Agent_Data/13_Task_Success_and_Credit_Assignment.md)
14. [Agent Failure Taxonomy：从失败现象到根因、归因与数据转化](./LLM_Agent_Data/14_Agent_Failure_Taxonomy.md)

这一 Part 的核心链条：

```text
Task
↓
Environment
↓
Trajectory
↓
Outcome
↓
Credit
↓
Failure Attribution
↓
Root Cause
```

Master Figures：

- [F4 — Agent Task–Environment–Trajectory](./LLM_Agent_Data/figures/F4_Agent_Task_Environment_Trajectory.md)
- [F6 — Credit → Failure Causal Map](./LLM_Agent_Data/figures/F6_Credit_to_Failure_Causal_Map.md)

---

## Part IV — Measurement

> **谁来判、怎么测，以及怎样证明方法真的更好？**

15. [Grader、Verifier 与 LLM-as-a-Judge](./LLM_Agent_Data/15_Grader_Verifier_and_LLM_as_a_Judge.md)
16. [Benchmark Design 与 Evaluation Protocol](./LLM_Agent_Data/16_Benchmark_Design_and_Evaluation_Protocol.md)

核心原则：

```text
Evidence First
↓
Choose Evaluator
↓
Frozen Protocol
↓
Matched / Paired Comparison
↓
Metric + Cost + Risk + Uncertainty
↓
Scoped Claim
```

Master Figure：[F8 — Benchmark / Evaluation Protocol](./LLM_Agent_Data/figures/F8_Benchmark_Evaluation_Protocol.md)。

---

## Part V — Data Optimization & Lifecycle

> **哪些数据值得留下、投资、治理、混合和验证？**

17. [Data Flywheel：从失败日志到持续改进的数据闭环](./LLM_Agent_Data/17_Data_Flywheel_and_Continuous_Improvement.md)
18. [Data Strategy 与 Data Valuation：如何决定哪类数据最值得做](./LLM_Agent_Data/18_Data_Strategy_and_Data_Valuation.md)
19. [Data Governance、Lineage 与 Reproducibility](./LLM_Agent_Data/19_Data_Governance_Lineage_and_Reproducibility.md)
20. [Data Quality、Filtering、Deduplication 与 Mixture](./LLM_Agent_Data/20_Data_Quality_Filtering_Deduplication_and_Mixture.md)
21. [Data Experiments：如何证明一批数据真的有用](./LLM_Agent_Data/21_Data_Experiments_and_Causal_Validation.md)

主线：

```text
发现 Gap
↓
决定投资
↓
治理数据身份与历史
↓
筛选 / 去重 / 混合
↓
受控实验
↓
Scale / Maintain / Revise / Stop
```

Master Figure：[F9 — Data Flywheel](./LLM_Agent_Data/figures/F9_Data_Flywheel.md)。

---

## Part VI — Data Operations

> **怎样把有效的数据方法稳定地生产、监控并组织运行？**

22. [Data Production System：把高价值数据稳定地生产出来](./LLM_Agent_Data/22_Data_Production_System.md)
23. [Data Monitoring、Online Feedback 与 Drift Detection](./LLM_Agent_Data/23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
24. [End-to-End LLM / Agent Data Operating Model](./LLM_Agent_Data/24_End_to_End_LLM_Agent_Data_Operating_Model.md)

主线：

```text
Plan
↓
Queue / Execute / Persist
↓
Verify / Route / Build
↓
Train / Deploy
↓
Monitor / Detect Drift
↓
Organizational Decision
↺
```

---

## Part VII — Synthesis

> **面对真实问题时，怎样把前面的知识转成一套可执行方法？**

25. [LLM / Agent Data 全景能力地图与实战方法论](./LLM_Agent_Data/25_LLM_Agent_Data_Capability_Map_and_Practical_Methodology.md)

第 25 章把整套体系压缩成：

```text
Problem Framing
↓
Diagnosis
↓
Data / System Intervention
↓
Controlled Validation
↓
Production
↓
Monitoring
↓
Next Decision
```

Master Figure：[F14 — Operating Model + Capability Map](./LLM_Agent_Data/figures/F14_Operating_Model_and_Capability_Map.md)。

---

# 三套导航资产

除了线性章节目录，现在全书还维护三套非正文章节型导航。

## 1. Canonical Concepts

- [Canonical Glossary & Notation](./LLM_Agent_Data/00_Glossary_and_Notation.md)

用于回答：

```text
这个术语在哪里定义？
Outcome / Reward / Credit 有什么区别？
Tool / Harness / Environment 如何区分？
```

## 2. Canonical Cases

- [Canonical Casebook](./LLM_Agent_Data/00_Canonical_Casebook.md)
- [Case Integration Index](./LLM_Agent_Data/00_Case_Integration_Index.md)
- [Cases Directory](./LLM_Agent_Data/cases/README.md)

用于回答：

```text
这个概念在一个真实 case 中是什么样？
同一个 failure 如何穿过不同章节？
C1-VB / C3-F5 / C4-SC 到底指什么？
```

## 3. Master Figures

- [Master Figure System](./LLM_Agent_Data/00_Master_Figure_System.md)
- [Master Figures Directory](./LLM_Agent_Data/figures/README.md)

第一批已经完成：

```text
F1  Learning System Overview
F4  Agent Task–Environment–Trajectory
F6  Credit → Failure Causal Map
F8  Benchmark / Evaluation Protocol
F9  Data Flywheel
F14 Operating Model + Capability Map
```

用于回答：

> **这些概念和案例在一张图上到底怎么连接？**

---

# 编辑基础设施

以下文件不是正文，而是全书编辑与维护基础设施：

- [全书精修施工图](./LLM_Agent_Data/00_Book_Refinement_Blueprint.md)
- [Canonical Glossary & Notation](./LLM_Agent_Data/00_Glossary_and_Notation.md)
- [Canonical Casebook](./LLM_Agent_Data/00_Canonical_Casebook.md)
- [Case Integration Index](./LLM_Agent_Data/00_Case_Integration_Index.md)
- [Master Figure System](./LLM_Agent_Data/00_Master_Figure_System.md)

当前精修顺序：

```text
结构 / Concept Ownership
✓

Canonical Cases
✓ 基础设施与稳定 ID

Master Figures
→ 正在进行

Indexes
→ 下一阶段

Fact / Citation Verification
→ 后续

Final Continuous Read-through
→ 最终
```

---

# 推荐阅读路线

## 路线 A：从零建立完整体系

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

适合第一次系统学习。

---

## 路线 B：大模型 / Agent 数据岗位面试

```text
1 → 2 → 3
→ 6 → 7 → 9
→ 15 → 16
→ 18 → 20 → 21
→ 25
```

重点建立：数据对象、监督信号、生产、评价、数据价值和实验验证能力。

---

## 路线 C：Agent Data / Agent Evaluation

```text
1 → 5
→ 10 → 11 → 12 → 13 → 14
→ 15 → 16
→ 17 → 22 → 23
→ 25
```

重点理解：Task、Environment、Trajectory、Failure、Verifier 与真实任务完成。

---

## 路线 D：Reasoning / Test-time / Selector Research

```text
1 → 4
→ 8 → 9
→ 13
→ 15 → 16
→ 21
→ 25
```

重点理解：state、risk、recoverability、same-state counterfactual、candidate selection 和 controlled evaluation。

---

## 路线 E：Data Platform / DataOps

```text
1 → 12
→ 19 → 20
→ 22 → 23 → 24
```

重点理解：schema、lineage、versioning、dataset build、production、monitoring 与 operating model。

---

# 五个贯穿案例

```text
C1 Order / Refund Agent
C2 Calendar / Meeting Agent
C3 File / Repository Agent
C4 Reasoning Continue / Repair
C5 Code / Execution Agent
```

它们不是增加例子数量，而是让同一个问题可以被连续观察：

```text
Task
→ Environment
→ Trajectory
→ Credit
→ Failure
→ Verifier
→ Benchmark
→ Data
→ Experiment
→ Production
→ Monitoring
```

详细定义与稳定 variant ID 见：[Cases Directory](./LLM_Agent_Data/cases/README.md)。

---

# 全书最终目标

学完整套体系以后，希望形成的不是“记住 25 章术语”，而是一种稳定的问题解决能力：

```text
看到一个真实问题
↓
知道它属于哪一层
↓
知道需要什么证据
↓
知道应该改 Data / Model / Prompt / Tool / Harness / Product 哪一层
↓
如果是 Data Problem，知道该构造什么 learning signal
↓
知道如何做受控实验
↓
知道什么时候 scale、什么时候 stop
↓
知道上线以后如何继续监控与学习
```

> **成熟的大模型数据能力，不是“拥有很多数据”，而是拥有一套能够持续把真实问题转化为可验证学习信号的 Learning System。**
