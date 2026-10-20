# LLM / Agent Data Condensed Guide

> 状态：`Stable Mother Edition V3.x / Condensed Edition / Multi-entry-aligned`
>
> 目标：把 25 章母本压缩成一份可以快速复习、面试组织回答、项目启动前建立 shared mental model 的精简入口。
>
> 原则：**不重新定义 canonical concept；所有深层定义仍回到 0–25 章、Glossary、Cases 与 Master Figures。**

---

# 0. 怎么使用这份精简版？

## 30 分钟

只读：

```text
§1 六个根问题
§3 Agent World
§4 Credit / Failure
§5 Evaluation
§13 30-minute Diagnosis
§11 十条底线
```

同时看：

```text
F1 / F4 / F6 / F8 / F14
```

## 90 分钟

完整读本文件，并配合：

```text
F1 → F4 → F6 → F8 → F9 → F14
```

如果需要口头表达，再看：

- [`Figure Presentation Kit`](./00_Figure_Presentation_Kit.md) — 选图 / 30s / 90s talk track
- [`D2 Presentation Storyboards`](./visual_derivatives/slides/README.md) — 真正 16:9 progressive reveal implementation

## 半天

再补四篇互补 walkthrough：

```text
C1
→ External Agent Decision / Data Learning Loop

C3
→ Permission / Harness / Failure Owner

C4
→ Reasoning Intervention / Trigger / Oracle / Selector

C5
→ Executable Truth / Hidden Tests / Verifier Coverage
```

以及：

```text
Practical Playbooks P1–P7
```

## 准备面试

第一入口：

- [`Interview Pack`](./00_Interview_Pack.md)

优先形成三种表达：

```text
1. 概念边界
2. 真实项目 / 研究 evidence
3. 可验证 workflow
```

推荐组合：

```text
Interview Pack
→ Condensed Guide
→ Figure Presentation Kit / Quick-reference
→ C1 / C3 / C4 / C5 Walkthrough
→ Interview Index
```

这里的 C1 / C3 / C4 / C5 Walkthrough 属于 **S3 Teaching Case / rehearsal asset**：它们用来练习结构、边界和 workflow，不属于“我做过的真实项目 / 研究 evidence”。如果面试需要回答“你实际做过什么”，必须另接自己的 frozen project / research artifact；尤其不能把 C4 Walkthrough 直接当成 RoTFuse / K17 的结果报告。

不要只背术语定义，也不要为了展示框架而跳过问题本身的 Direct Answer。

---

# 1. 整套体系只回答六个根问题

```text
1. What should the model learn?
   模型应该学什么？

2. From what experience?
   从什么经验里学？

3. With what feedback?
   什么信号告诉它好坏？

4. How do we know it learned?
   怎么证明真的学会？

5. Is it worth the cost?
   值得这个成本吗？

6. When should the system learn again?
   什么时候应该开始下一轮学习？
```

整套系统可以压成：

```text
Real Problem / Capability Gap
↓
Task & Environment
↓
Experience
↓
Evidence
↓
Learning Signal
↓
Training / Policy Update
↓
Evaluation
↓
Deploy / Monitor
↓
Fresh Failure / Drift
↺
```

最重要的认知转换：

> **现代 LLM / Agent Data 工作，不是维护一条“采集—清洗—训练”的流水线，而是在设计 Learning System。**

总图：[`F1 — Learning System Overview`](./figures/F1_Learning_System_Overview.md)

---

# 2. 先把 Data Object 和 Learning Signal 分开

## Data Object

从简单到复杂：

```text
Token / Text
→ Instruction–Response Example
→ Preference Pair
→ Process / State Record
→ Episode
→ Trajectory
→ Candidate / Counterfactual Pool
```

在 Agent 时代，最重要的基本对象链是：

```text
Task
→ Case
→ Episode
→ Trajectory
```

### Task

定义：

```text
要完成什么
约束是什么
允许什么
禁止什么
成功是什么
```

### Case

定义这一次具体世界：

```text
Initial State
Entity IDs
Permissions
Tool / Environment Version
Hidden / Evaluator-only State
```

### Episode

系统针对某个 Case 的一次实际运行。

### Trajectory

这次 Episode 实际发生过的：

```text
State
Decision
Action
Observation
State Transition
```

及执行证据。

## Learning Signal

同一个 Data Object 可以被不同信号监督：

```text
SFT
Preference
Reward
Process Supervision
Environment Feedback
Verifier Label
Recovery / Counterfactual Signal
```

因此始终记住：

```text
Data Object
≠ Learning Signal
```

以及：

```text
Outcome
≠ Reward
≠ Credit
```

总图：[`F2 — Data Object & Learning Signal Evolution`](./figures/F2_Data_Object_and_Learning_Signal_Evolution.md)

---

# 3. Agent Data 的核心不是 Tool Call，而是 Agent World

最短对象关系：

```text
Task
→ Case
→ Model / Policy
→ Harness
→ Action / Tool
→ Environment
→ World State
→ Observation
→ Agent-visible State
→ Next Decision
```

其中：

## Tool

```text
Agent 可调用的动作接口
```

## Harness

```text
连接 Model / Tool / Environment 的 runtime orchestration
```

## Environment

```text
定义世界状态与状态转移
```

## Observation

```text
世界通过 Tool / Harness 暴露给 Agent 的反馈
```

## Trajectory

```text
这次 Episode 实际发生过的执行证据
```

最容易混的边界：

```text
Tool
≠ Harness
≠ Environment

World State
≠ Observation
≠ Agent-visible State

Decision Intent
≠ Executed Action
```

这也是为什么：

```text
Agent failed
```

不能自动翻译成：

```text
Model failed
```

总图：[`F4 — Agent Task–Environment–Trajectory`](./figures/F4_Agent_Task_Environment_Trajectory.md)

深度案例：[`C3 Permission / Harness Ownership Walkthrough`](./case_studies/C3_Permission_Harness_Ownership_Walkthrough.md)

---

# 4. Failure Analysis：从 Outcome 到 Root Cause 不能跳步

一条成熟 causal chain：

```text
Outcome
↓
First Error
↓
First Harmful Action
↓
Last Recoverable State
↓
Point of No Return
↓
Symptom
↓
Immediate Mechanism
↓
Root Cause
↓
Failure Owner
↓
Intervention Routing
```

## First Error

第一处局部事实 / 逻辑 / 约束 / 决策错误。

## First Harmful Action

第一处真正降低后续可达价值或造成有害状态变化的 Action。

## Last Recoverable State

仍然存在更好未来的最后状态。

## Root Cause

最值得修复、能解释一类 failure 的上游机制。

## Failure Owner

真正首先应该负责修复的组件：

```text
Task / Product
Model / Policy
Tool
Harness
Environment
Evaluator
External Service
```

关键边界：

```text
First Error
≠ First Harmful Action
≠ Root Cause

Failure Layer
≠ Failure Owner

Recoverability
≠ Repairability
```

总图：[`F6 — Credit → Failure Causal Map`](./figures/F6_Credit_to_Failure_Causal_Map.md)

完整案例：

- [`C1 End-to-End Walkthrough`](./case_studies/C1_End_to_End_Walkthrough.md)
- [`C3 Permission / Harness Ownership Walkthrough`](./case_studies/C3_Permission_Harness_Ownership_Walkthrough.md)

---

# 5. Evaluation：Evidence First, Judge Second

不要先问：

```text
“用什么 Judge？”
```

先问：

```text
我要证明什么 Claim？
最直接 Evidence 是什么？
```

评价链：

```text
Evidence
→ Evaluator
→ Raw Judgment
→ Derived Label
→ Final Decision / Metric
```

## Verifier

依赖可明确检查的 Evidence：

```text
Environment Predicate
Execution
Unit Test
Symbolic Check
Rule
```

## Grader

把 Evidence 映射成 score / label 的广义 evaluator。

## Judge

用于不可完全程序化的解释性标准：

```text
open-ended quality
clarity
planning quality
whether clarification was appropriate
```

原则：

```text
Evidence
≠ Judgment
≠ Label

Judge
≠ Ground Truth

Agreement
≠ Validity
```

证据不足时允许：

```text
UNRESOLVED / ABSTAIN
```

总图：[`F7 — Evidence → Verifier → Grader → Judge`](./figures/F7_Evidence_Verifier_Grader_Judge.md)

Executable Evaluation 实战：[`C5 Executable Truth / Verifier Coverage Walkthrough`](./case_studies/C5_Executable_Truth_Verifier_Coverage_Walkthrough.md)

---

# 6. Benchmark：不是“跑个数据集看 Accuracy”

可信比较至少包含：

```text
Scientific / Product Question
↓
Capability Definition
↓
Benchmark Object
↓
Frozen Evaluation Protocol
↓
Baseline / Treatment Runs
↓
Paired / Matched Analysis
↓
Metrics
↓
Uncertainty
↓
Claim Scope
```

必须冻结：

```text
Population
Model / Prompt / Runtime
Tool / Harness / Environment
Budget / Stop Rules
Evaluator / Label Version
Seeds / Repetitions
```

selective / triggered system 要特别保留：

```text
Full Population
Eligible
Triggered
Intervened
Observed Outcome
```

所以：

```text
Triggered-only result
≠ End-to-end result
```

还要看：

```text
Rescue
Harmful
Net
Cost
Latency
Tokens
Coverage
```

而不是只有总体平均分。

总图：[`F8 — Benchmark / Evaluation Protocol`](./figures/F8_Benchmark_Evaluation_Protocol.md)

Reasoning intervention 实战：[`C4 Reasoning Intervention Walkthrough`](./case_studies/C4_Reasoning_Intervention_Walkthrough.md)

---

# 7. Data Acquisition：Human / Synthetic / Rollout / Mining 各解决不同问题

## Human Data

主要价值：

```text
定义标准
处理边界
Gold / Anchor
Adjudication
高风险判断
```

## Synthetic Data

主要价值：

```text
规模
定向扩展
结构化 variation
稀有 edge case
```

主要风险：

```text
Teacher Bias
Mode Collapse
Model Monoculture
Synthetic-to-real Gap
```

## Rollout / Candidate Data

适合：

```text
same-state alternatives
Best-of-N
Counterfactual
Recovery
Selector
```

## Hard Case Mining

目标不是找“最难”，而是找：

```text
有 gap
有价值
可学习
可验证
相对稀缺
```

核心：

```text
Hard
≠ Valuable
```

---

# 8. Data Flywheel：Failure 不直接等于 Training Example

完整闭环：

```text
Real Use
→ Signal
→ Triage
→ Root Cause
→ Capability Gap
→ Prioritize
→ Acquire Experience
→ Construct Supervision
→ Curate
→ Controlled Experiment
→ Train
→ Evaluate
→ Deploy / Revise
↺
```

因此：

```text
Production Failure
≠ Training Example
```

真正的 flywheel 中间必须有：

```text
Diagnosis
Capability Abstraction
Prioritization
Supervision Choice
Controlled Validation
```

总图：[`F9 — Data Flywheel`](./figures/F9_Data_Flywheel.md)

---

# 9. Strategy / Curation / Experiment：三件事不能混

## Data Strategy

回答：

```text
为什么投？
投多少？
和其他方向相比值不值？
什么时候停？
```

看：

```text
Value
Risk
Importance
Learnability
Verifiability
Cost
Marginal Utility
```

## Data Curation

回答：

```text
哪些数据留下？
哪些删除 / 降权 / 隔离？
哪些重复？
模型最终看多少？
```

关注：

```text
Filtering
Dedup
Family
Contamination
Weighting
Mixture
Token Exposure
```

## Data Experiment

回答：

> **这项 Data Intervention 真的导致模型变好了吗？**

Action space：

```text
Add
Remove
Replace
Reweight
Transform
```

优先：

```text
Matched Budget
Target Eval
Transfer Eval
Regression Eval
Cost
Scale / Stop Decision
```

关键边界：

```text
Intrinsic Data Quality
≠ Downstream Learning Value
```

总图：[`F10 — Data Strategy / Portfolio / ROI`](./figures/F10_Data_Strategy_Portfolio_ROI.md)

---

# 10. Governance / Production / Monitoring：让一次成功变成可持续系统

## Governance

必须能回答：

```text
它是谁？
从哪来？
经历了什么？
为什么变？
被谁用过？
影响了什么？
```

核心：

```text
Identity
Provenance
Lineage
Versioning
Reproducibility
```

并区分：

```text
Re-score
≠ Re-run
≠ Replay
```

总图：[`F11 — Governance / Lineage DAG`](./figures/F11_Governance_Lineage_DAG.md)

## Production

不是“跑脚本批量生成”。

而是：

```text
Production Contract
→ Job / Queue / Worker
→ Raw Artifact
→ Validation
→ Evaluation / Routing
→ Canonical Asset
→ Build Recipe
→ Dataset View
```

关键边界：

```text
Infrastructure Retry
≠ Agent Recovery
```

总图：[`F12 — Data Production System`](./figures/F12_Data_Production_System.md)

## Monitoring

指标变了，先不要说模型退化。

依次排：

```text
Metric
Evaluator
Infrastructure
Traffic Mix
Concept / Business Rule
Frozen Capability
Fresh Failure Frontier
```

所以：

```text
Monitoring
≠ Diagnosis
```

总图：[`F13 — Monitoring / Drift Diagnostic Tree`](./figures/F13_Monitoring_Drift_Diagnostic_Tree.md)

---

# 11. 十条必须刻进脑子里的底线

```text
1. Data Object ≠ Learning Signal

2. Task ≠ Case ≠ Episode ≠ Trajectory

3. Tool ≠ Harness ≠ Environment

4. World State ≠ Observation ≠ Agent-visible State

5. Outcome ≠ Reward ≠ Credit

6. First Error ≠ First Harmful Action ≠ Root Cause

7. Failure Layer ≠ Failure Owner

8. Evidence ≠ Judgment ≠ Label

9. Candidate Exists ≠ Selectable ≠ E2E Improvement

10. Intrinsic Data Quality ≠ Downstream Learning Value
```

如果这十条不混，绝大多数 LLM / Agent Data 问题都已经站在正确的起点上。

---

# 12. Canonical Cases：五个案例分别负责什么？

```text
C1 Order / Refund
→ conditional constraint / state-grounded write

C2 Calendar / Meeting
→ multi-constraint / partial completion / notification

C3 File / Repository
→ permission / side effect / Harness ownership

C4 Reasoning Continue / Repair
→ risk / recoverability / same-prefix / selector

C5 Code / Execution
→ executable truth / hidden tests / verifier coverage
```

案例入口：[`Canonical Cases`](./cases/README.md)

当前四篇 Practical Study：

- [`C1 — End-to-End Data Learning Loop`](./case_studies/C1_End_to_End_Walkthrough.md)
- [`C3 — Permission / Harness Ownership`](./case_studies/C3_Permission_Harness_Ownership_Walkthrough.md)
- [`C4 — Reasoning Intervention`](./case_studies/C4_Reasoning_Intervention_Walkthrough.md)
- [`C5 — Executable Truth / Verifier Coverage`](./case_studies/C5_Executable_Truth_Verifier_Coverage_Walkthrough.md)

四篇分别回答：

```text
C1
→ failure 怎样进入完整 learning loop？

C3
→ model 真的是正确 owner 吗？

C4
→ intervention headroom 能转化成 online value 吗？

C5
→ 什么 evidence 足以支持 executable correctness，verifier coverage 又怎样影响结论？
```

---

# 13. 30-minute Diagnosis

这不是固定的 failure-analysis 流水线；先选择 Entry，再在 30 分钟内形成最小可决策结构。

## 0–5 min — Entry + Scope

```text
Entry
Goal / Scientific Question
Full Population
Primary Metric
Severity / Scientific Value
```

Entry 至少区分：

```text
Failure-led
Monitoring-led
Hypothesis-led
Evaluation-led
Asset-led / Curation-led
```

## 5–10 min — Contract + Evidence

```text
Relevant Task / Case / Decision State / Asset
Runtime / Evaluator / Source Version
Raw Evidence
Information Boundary if selective
```

## 10–15 min — 按 Entry 分支

```text
Failure-led
→ Symptom / First Harmful / Root Cause candidate / Owner

Monitoring-led
→ Last-known-good / Change Ledger / Containment / raw-vs-fixed-mix

Hypothesis-led
→ Mechanism / Counterfactual / Oracle / Online Decision Question

Evaluation-led
→ Claim / Evidence / Evaluator Coverage / Measurement Bridge

Asset-led
→ Source Lineage / Integrity / Routing / Dataset View
```

## 15–20 min — Intervention Gate

```text
Data?
Model / Training?
Inference Policy?
Tool / Harness / Environment?
Evaluator?
Product / Task Contract?
```

不要预设一定是 Data。

## 20–25 min — Minimum Controlled Change

```text
Minimum credible intervention
Baseline / Treatment or Old / New bridge
Target / Transfer / Regression Eval
Population / Information / Cost Ledger when relevant
```

## 25–30 min — Decision

```text
Scale / Maintain / Revise / Stop / Retire
Cost Bound
Claim Scope
Monitoring / Regression / Re-entry Asset
```

第一入口：[`Project Starter Pack`](./00_Project_Starter_Pack.md)

执行检查：[`Checklist Index`](./00_Checklist_Index.md)

总图：[`F14 — Operating Model + Capability Map`](./figures/F14_Operating_Model_and_Capability_Map.md)

---

# 14. 面试回答不要只给“知识点”，给 Problem-solving Chain

例如问：

> “你会怎么做 Agent Data？”

不要回答：

```text
收集数据
清洗
SFT
评测
```

先直接回答问题，再按需要展开：

```text
Direct Answer
→ Boundary
→ Mechanism / Evidence
→ Example
→ Broader System only if needed
```

如果进入完整项目设计，可以展开为：

```text
1. 先定义 Target Capability 与 Task Contract
2. 确认 Environment / Tool / Harness 与 Evidence
3. 如果是 failure-led，再从 Trajectory 做 Failure / Credit Analysis
4. 判断正确 Intervention Owner，而不是预设 Data
5. 需要 Data 时再选择 Human / Synthetic / Rollout / Mining acquisition
6. 设计合适 Learning Signal
7. 做 Curation / Mixture
8. 用 matched-budget / matched-protocol Experiment 验证
9. 有效后才 Productionize
10. 上线后用 Frozen Core + Fresh Frontier 监控
```

如果面试官继续追问任何一层，再下钻到对应章节。

面试总入口：[`Interview Pack`](./00_Interview_Pack.md)

口头讲图：[`Figure Presentation Kit`](./00_Figure_Presentation_Kit.md)

---

# 15. 最实用的调用入口

## 我遇到一个真实症状，不知道先查哪

→ [`Problem Index`](./00_Problem_Index.md)

## 我刚拿到一个新项目 / 告警 / 研究问题 / 数据资产

→ [`Project Starter Pack`](./00_Project_Starter_Pack.md)

## 我想按步骤把问题推进到 Decision

→ [`Practical Playbooks`](./00_Practical_Playbooks.md)

## 我需要把过程落成可审计工件

→ [`Practical Artifact Kit`](./00_Practical_Artifact_Kit.md)

## 我已经在执行某一阶段，怕漏项

→ [`Checklist Index`](./00_Checklist_Index.md)

案例演练：

- [`C1 — End-to-End Data Learning Loop`](./case_studies/C1_End_to_End_Walkthrough.md)
- [`C3 — Permission / Harness Ownership`](./case_studies/C3_Permission_Harness_Ownership_Walkthrough.md)
- [`C4 — Reasoning Intervention`](./case_studies/C4_Reasoning_Intervention_Walkthrough.md)
- [`C5 — Executable Truth / Verifier Coverage`](./case_studies/C5_Executable_Truth_Verifier_Coverage_Walkthrough.md)

---

# 16. 最终心智模型

整套知识可以最后压成：

```text
Problem / Opportunity / Signal / Asset
↓
Correct Entry
↓
Relevant Contract + Evidence
↓
Diagnosis / Mechanism / Asset Validation
↓
Correct Intervention Owner
↓
Controlled Validation
↓
Scale / Maintain / Revise / Stop / Retire
↓
Production / Governance
↓
Deploy / Monitor
↓
Learn Again
```

真正成熟的能力不是：

```text
“我会做很多数据。”
```

而是：

> **我能把一个真实模型 / Agent 问题、研究假设、评测缺口、线上信号或数据资产，从正确入口转化成可验证 Evidence、可审计 Artifact、可控 Intervention，以及最终可运营的 Learning Loop。**
