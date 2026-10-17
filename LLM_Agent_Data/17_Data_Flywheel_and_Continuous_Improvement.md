# 第 17 章 Data Flywheel：从真实反馈到下一轮学习的闭环

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 16 章 Benchmark Design 与 Evaluation Protocol`](./16_Benchmark_Design_and_Evaluation_Protocol.md)
>
> 关联章节：[`第 9 章 Hard Case Mining`](./09_Hard_Case_Mining_and_Curriculum.md)、[`第 14 章 Agent Failure Taxonomy`](./14_Agent_Failure_Taxonomy.md)、[`第 18 章 Data Strategy`](./18_Data_Strategy_and_Data_Valuation.md)、[`第 19 章 Governance`](./19_Data_Governance_Lineage_and_Reproducibility.md)、[`第 21 章 Data Experiments`](./21_Data_Experiments_and_Causal_Validation.md)、[`第 23 章 Monitoring 与 Drift`](./23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**Data Flywheel / Continuous Improvement 的 orchestration chapter。它负责解释信号如何从 Production / Eval / Simulation 进入 Mining、Diagnosis、Data Acquisition、Training、Evaluation、Deployment，再回到新一轮信号；Active Learning 细节归第 9 章，ROI / Portfolio 归第 18 章，Governance 归第 19 章，Data causal experiment 归第 21 章，Drift / Monitoring 归第 23 章。**
>
> 本章核心问题：**一个模型系统怎样把真实世界暴露出的新问题，稳定地转成下一轮可验证的学习机会，而不是简单把日志重新喂给模型？**

---

# 17.0 Data Flywheel 不是“日志回流”

最粗糙的版本是：

```text
Model
↓
Serve Users
↓
Collect Logs
↓
Train Again
↓
Better Model
```

真正可用的飞轮必须多出一整段中间层：

```text
Production / Benchmark / Simulation
↓
Signals & Traces
↓
Triage
↓
Failure Attribution / Root Cause
↓
Capability Gap
↓
Data Acquisition
↓
Human / Synthetic / Programmatic Supervision
↓
Verification / Curation
↓
Training / Policy Update
↓
Frozen Evaluation
↓
Deployment
↓
Fresh Signals
↺
```

因此：

> **Flywheel 的核心不是数据会回流，而是每一轮都更会判断“什么值得学、为什么值得学、学完以后怎么证明”。**

---

# 17.1 Data Pipeline 与 Data Flywheel 的区别

普通 Pipeline：

```text
Raw Data
→ Clean
→ Label
→ Train
→ Done
```

Flywheel：

```text
Deploy
→ New Behavior
→ New Failure Distribution
→ New Data Policy
→ New Model
→ New Behavior
```

它有两个核心属性：

```text
Closed-loop
模型行为本身产生下一轮信号

Adaptive
下一轮数据策略会随着模型与环境变化而更新
```

所以：

```text
Static Dataset
≠ Adaptive Learning System
```

---

# 17.2 Flywheel 的八个阶段

建议把闭环固定成八个阶段。

## 1. Sense

从哪里发现问题？

```text
Production Logs
Benchmark Failures
Shadow Runs
Human Feedback
Verifier Failures
Judge Disagreement
Support Tickets
Synthetic Stress Tests
```

## 2. Triage

哪些值得继续分析？

排除：

```text
spam
infra outage
invalid task
duplicate incident
known fixed bug
```

## 3. Diagnose

使用第 14 章的 Failure Record：

```text
Symptom
→ Mechanism
→ Root Cause
→ Failure Owner
```

## 4. Abstract

从单个 case 上升到：

```text
Failure Family
Capability Gap
```

## 5. Acquire

选择：

```text
Mine
Human
Synthetic
Programmatic
Counterfactual
```

## 6. Construct Supervision

转成：

```text
SFT
Preference
Recovery
Verifier / Judge Data
Regression
```

## 7. Validate

通过 Ch16 + Ch21 的 protocol 判断：

```text
真的改善了吗？
有没有 regression？
成本多少？
```

## 8. Deploy & Refresh

上线后继续观察：

```text
原 failure 是否下降？
新的 failure 是否出现？
旧 frontier 是否已经饱和？
```

然后重新进入 Sense。

---

# 17.3 Production Log ≠ Training Data

线上日志只是：

```text
Raw Experience
```

里面混有：

```text
成功轨迹
模型失败
Tool Failure
Harness Failure
用户改需求
攻击输入
重复请求
PII
异常流量
```

因此必须经过：

```text
Triage
Attribution
Privacy / Rights Check
Verification
Selection
```

才能成为训练资产。

一句话：

> **真实 ≠ 可直接训练。**

---

# 17.4 Triage 的第一个问题：这到底是不是模型问题？

失败可以来自：

```text
Task / Requirement
Model
Tool
Harness
Environment
Evaluator
Infrastructure
```

因此 Data Flywheel 必须有多个出口：

```text
Model Data Fix
Prompt Fix
Tool Fix
Harness Fix
Environment Fix
Product UX Fix
Evaluator Fix
Policy Fix
```

而不是：

```text
所有失败 → Training Data
```

这是 flywheel 不退化成“数据垃圾桶”的第一道防线。

---

# 17.5 从 Case 到 Failure Family，再到 Capability Gap

真实失败：

> “取消明天的会议，但周会不要动。”

Agent 把两个会议都取消。

表面：

```text
Wrong Calendar Action
```

Root Cause 可能是：

```text
Negative Constraint Handling
```

抽象成能力：

```text
Selective Action under Exclusion Constraint
```

然后生成不同 domain 的同能力 case：

```text
删除文件，但 .env 不要动
退款订单，但 VIP 订单不要动
群发邮件，但外部联系人不要发
```

所以飞轮真正的放大步骤是：

```text
Single Failure
↓
Root Cause
↓
Failure Family
↓
Capability Gap
↓
Cross-domain Data Family
```

---

# 17.6 Failure Family 比单条 Case 更适合作为飞轮单位

Case-level：

```text
order_1847 failed
```

Family-level：

```text
negative constraint ignored
```

Capability-level：

```text
constraint-conditioned action selection
```

三层分别适合：

```text
Case
→ replay / regression

Failure Family
→ mining / data generation

Capability Gap
→ strategy / roadmap
```

飞轮如果只围绕单条 case 修补，很容易变成 benchmark memorization。

---

# 17.7 Signal 不是 Ground Truth

线上信号可能包括：

```text
User retry
Undo
Complaint
Escalation
Low confidence
Judge disagreement
Loop
Repeated clarification
```

它们都适合用于：

```text
Mining / Triage
```

但不应该自动变成：

```text
Correctness Label
```

比如用户重说一次，可能是：

```text
Agent 没理解
```

也可能是：

```text
用户改变了需求
```

因此飞轮遵循：

> **Signal → Audit / Attribution → Label，而不是 Signal = Label。**

---

# 17.8 Online Feature 与 Offline Supervision 必须分开

在线 policy 可以使用：

```text
current observation
current score
confidence
current tool return
current state
```

但不能使用：

```text
future outcome
future rollout
human adjudication
hidden reference
```

后者只能用于 Offline Supervision。

这个边界与 Ch4 / Ch8 的 future-information discipline 完全一致。

---

# 17.9 Data Acquisition 的五条主路

确定 Capability Gap 后，常见 acquisition channel 有：

```text
Mine
从真实或 rollout 里挖

Human
专家直接设计 / 修正 / 判断

Synthetic
Teacher / generator 扩展

Programmatic
规则枚举 / simulator 生成

Counterfactual
固定大部分条件，只改变关键 state / action / constraint
```

选择哪一种，不由“哪种最先进”决定，而由：

```text
目标能力
可验证性
真实性
成本
规模
```

共同决定。

正式资源配置见第 18 章。

---

# 17.10 Human-in-the-loop 的高价值位置

现代飞轮里，人不一定负责大规模逐条写数据。

更高价值的角色往往是：

```text
定义标准
确认 root cause
处理新 failure type
审查 high-risk case
adjudicate disagreement
校准 Judge
审核 synthetic boundary case
```

也就是：

> **Human 更像标准制定者与边界裁判，而不只是生产工。**

详细 Human Data 见第 6 章。

---

# 17.11 Model-in-the-loop 的位置

模型可以帮助：

```text
Failure Summarization
Clustering
Task Generation
Counterfactual Generation
Critique
Evidence Extraction
Pre-label
```

但：

```text
Model-generated Signal
≠ Ground Truth
```

必须有外部锚点：

```text
Environment Truth
Executable Verifier
Human Gold
Independent Judge
```

否则飞轮会越来越像自己。

---

# 17.12 Regression 与 Frontier 是飞轮的两种记忆

每个已验证的重要 failure 都可能进入：

```text
Regression Set
```

作用：

```text
保证解决过的问题不复发
```

与此同时还需要：

```text
Fresh Frontier Set
```

作用：

```text
发现当前模型新的能力边界
```

所以：

```text
Regression
保护过去

Frontier
发现下一步
```

只保留 Regression 会越来越擅长旧问题；只追 Frontier 又可能悄悄遗忘旧能力。

---

# 17.13 Capability Frontier 必须持续刷新

Model v1 的 hard case：

```text
2-step tool use
success = 60%
```

到了 Model v2：

```text
success = 95%
```

那它已经不再是主要 frontier。

新的弱点可能转向：

```text
Recovery
Verification
Multi-constraint
Long Horizon
```

因此每一轮飞轮都要：

```text
Re-estimate Capability Map
↓
Retire Saturated Frontier
↓
Promote New Frontier
```

Hard Case acquisition 的详细方法见第 9 章。

---

# 17.14 Feedback Delay 与 Stale Data

一个生产 failure 从产生到影响新模型可能经历：

```text
Mining
→ Annotation
→ Training
→ Eval
→ Release
```

周期可能很长。

因此训练数据要知道：

```text
source_model_version
source_policy_version
collection_time
```

否则可能拿着：

```text
Model v1 的失败
```

去优化一个已经是：

```text
Model v5
```

的系统。

这就是 stale-data risk。

---

# 17.15 飞轮会改变它自己观察到的分布

模型变强以后：

```text
用户开始给它更复杂任务
```

所以：

```text
Online Failure Rate ↑
```

不一定意味着模型退化，可能只是：

```text
Task Mix 变难
```

因此 Flywheel 必须和第 23 章的 Drift Monitoring 配合：

```text
Raw Overall Metric
+
Slice Metric
+
Fixed-mix Metric
```

分开观察。

---

# 17.16 Positive-only Flywheel 会收缩分布

如果每轮都是：

```text
Generate
↓
Judge 高分留下
↓
Train
↓
Generate 更像 Judge 喜欢的内容
```

最终可能出现：

```text
style homogenization
mode collapse
rare behavior loss
judge overfitting
```

因此 flywheel 需要持续注入：

```text
Hard Negatives
Rare Cases
Real Data
Human Gold
Independent Verifier
Fresh Frontier
```

飞轮不是“自我复制”，而应是“受外部事实约束的持续学习”。

---

# 17.17 Recovery Flywheel：失败轨迹不只变成正确示范

例如：

```text
refund_order
→ PERMISSION_DENIED
→ request_approval
→ approved
→ refund_order
→ success
```

这条数据真正有价值的部分不是最终 success，而是：

```text
Failure State
→ Recovery Action
→ Recovered Outcome
```

所以 production failure 可以派生：

```text
Recovery SFT
Recovery Preference
Regression
Failure Analysis
```

而不只是把“正确最终轨迹”塞进 SFT。

---

# 17.18 Counterfactual Flywheel：从关键状态产生 matched alternatives

一个高价值 state：

```text
State S
Observed Action A → Failure
```

可以固定 snapshot，再生成：

```text
A → Fail
B → Success
C → Fail
D → Success
```

由此得到：

```text
same-state preference
rescue / harmful transition
recovery data
selector data
```

这使 Flywheel 可以发生在：

```text
整个 Episode
```

也可以发生在：

```text
Reasoning State
Agent Decision State
Tool-use State
```

局部层面。

---

# 17.19 Local Reasoning Flywheel

Reasoning 场景可以写成：

```text
Current Reasoning State
↓
Risk / Uncertainty Mining
↓
Same-prefix Alternatives
↓
Downstream Outcomes
↓
Rescue / Harmful / Neutral
↓
Better Trigger / Selector Evidence
↓
New State Mining
```

这里沿用第 4、8、13、16 章的定义，不在本章重新定义这些概念。

它展示的是 Flywheel 的粒度可以非常局部。

---

# 17.20 Flywheel 的外部锚点

自举系统最怕：

```text
Model
→ Synthetic Data
→ Model
→ Synthetic Data
```

闭环里没有外部真值。

因此成熟 Flywheel 需要不断注入：

```text
Executable Verification
Environment Truth
Human Gold
Fresh Real Data
Independent Evaluation
Adversarial Audit
```

可以理解为：

> **Flywheel 必须转，但尺子不能完全由飞轮自己制造。**

---

# 17.21 Flywheel Health：监控“闭环质量”，不只监控数据量

本章只给 orchestration-level 指标：

```text
Novel Failure Rate
Failure-family Coverage
Regression Recurrence Rate
Frontier Refresh Rate
Verified Training Yield
High-severity Coverage
Source Freshness
Downstream Improvement
```

更细的：

```text
Data ROI → Ch18
Data quality / dedup → Ch20
Monitoring / drift → Ch23
```

重点是避免只看：

```text
本周生成了多少条
```

这种 throughput vanity metric。

---

# 17.22 Canonical Case C1：订单 Agent 的完整 Flywheel

线上出现：

> 用户要求“未发货则取消，已发货不要动”，Agent 没查状态直接执行取消，并在失败后仍声称成功。

## Sense

Production trace 发现：

```text
false success claim
```

## Diagnose

```text
Root Cause A:
Missing Precondition Check

Root Cause B:
Observation Grounding Failure
```

## Abstract

```text
Precondition Checking
+
Tool-result Grounding
```

## Acquire

生成 matched family：

```text
pending
shipped
cancelled
permission_denied
not_found
```

## Construct Supervision

派生：

```text
Correct Demo
Preference Pair
Recovery Trace
Regression Case
```

## Validate

检查：

```text
Target Gain
General Regression
Side Effects
Cost
```

## Deploy

Canary 后继续观察：

```text
precondition failure ↓ ?
false claim ↓ ?
latency ↑ ?
extra tool calls ↑ ?
```

然后重新进入 Sense。

---

# 17.23 一个成熟 Flywheel 的出口不止 Training

Diagnosis 后可能进入：

```text
Data Intervention
Tool Fix
Harness Fix
Prompt Fix
Environment Fix
Evaluator Fix
Product Fix
Policy Fix
```

因此：

> **Data Flywheel 本质上是 Continuous Improvement Flywheel，不是 Training-only Flywheel。**

这一点会在第 24 章 Operating Model 进一步变成团队 routing 规则。

---

# 17.24 常见失败模式

1. **日志直接训练。** 没有 triage / attribution。
2. **所有 failure 都转成数据。** Tool / Harness / Product bug 被误处理。
3. **只看用户差评。** 严重 selection bias。
4. **只做 Synthetic。** 与真实分布脱节。
5. **只留正例。** 分布收缩，边界学习变差。
6. **Hard Case 永远不更新。** Frontier 已移动却仍继续 oversample。
7. **Regression 与 Frontier 只保留一个。** 要么遗忘旧能力，要么停止拓展新能力。
8. **Online signal 与 offline label 混用。** 引入 future leakage。
9. **飞轮没有外部 truth anchor。** 偏差递归放大。
10. **只汇报数据量。** 无法说明闭环是否更有效。

---

# 17.25 从数据岗位视角，本章实际在做什么？

典型工作包括：

```text
定义 production trace 信号
做 triage
把 failure 映射到 canonical taxonomy
聚合 failure family
抽象 capability gap
连接 Human / Synthetic / Mining pipeline
建立 regression growth
刷新 frontier cohort
把 Data Experiment 结果回流到下一轮 acquisition policy
和 Monitoring / Product / Infra 协作做 system routing
```

真正成熟的 Data Flywheel 能回答：

> **这个问题从哪里被发现、为什么值得处理、它被转成了什么学习信号、是否真的修好，以及下一轮因此改变了什么。**

---

# 17.26 面试 / 自检问题

1. Data Pipeline 和 Data Flywheel 最大区别是什么？
2. 为什么 Production Log 不能直接训练？
3. Flywheel 的八个阶段分别是什么？
4. 为什么 Triage 第一问应该是“这是不是模型问题”？
5. 单个 Failure 为什么要抽象成 Failure Family / Capability Gap？
6. Online signal 为什么不能自动当 label？
7. Online Feature 与 Offline Supervision 的边界是什么？
8. Mine / Human / Synthetic / Programmatic / Counterfactual 分别适合什么？
9. Human-in-the-loop 最有价值的位置在哪里？
10. 为什么 Regression 和 Frontier 必须同时维护？
11. 什么是 stale-data risk？
12. 模型变强后线上 failure rate 为什么可能上升？
13. Positive-only flywheel 为什么会 mode collapse？
14. Recovery data 为什么不应只压成成功轨迹？
15. Counterfactual flywheel 为什么需要 same-state snapshot？
16. Flywheel 为什么需要外部 truth anchor？
17. 什么情况下应该修 Tool / Harness，而不是做训练数据？
18. 一个 Data Flywheel 怎样证明自己真的越来越有效？

---

# 17.27 本章最终心智模型

```text
Sense
↓
Triage
↓
Diagnose
↓
Abstract
↓
Acquire
↓
Construct Supervision
↓
Validate
↓
Deploy
↓
Refresh
↺
```

这就是 Data Flywheel 的最小闭环。

其中：

```text
Ch9
负责“去哪挖”

Ch18
负责“投多少资源”

Ch19
负责“全过程怎么可追溯”

Ch21
负责“怎么证明数据真的有效”

Ch23
负责“上线后怎么知道世界变了”
```

本章只负责把这些组件连成一个可持续循环。

下一章第 18 章进一步回答：

> **闭环里机会很多，但资源有限——到底应该优先投资哪类数据？**