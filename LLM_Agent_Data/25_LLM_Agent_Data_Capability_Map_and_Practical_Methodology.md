# 第 25 章 LLM / Agent Data 全景能力地图与实战方法论：把整套体系真正调用起来

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 24 章 End-to-End Operating Model`](./24_End_to_End_LLM_Agent_Data_Operating_Model.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**个人 Practitioner Operating System / 全书收束章。它不再引入新的 canonical concept，而是通过 Capability Map、Problem Routing Tree、Data Intervention Tree、30-minute Diagnosis、Canonical Case 与 Project Checklist，帮助读者调用前 24 章。**
>
> 本章核心问题：**当一个真实 LLM / Agent Data 问题今天交到你手里，你能不能快速判断问题在哪一层、需要什么证据、该调用哪一章的方法、怎样设计最小可信 intervention，以及什么结果足以支持下一步决策？**

---

# 25.0 学完前 24 章，最终要获得的不是“知识量”

真正应该形成的是一种：

> **Data Reasoning Ability。**

即：

```text
看到一个真实问题
↓
定位问题层级
↓
找到关键证据
↓
判断是不是 Data Problem
↓
选择合适 learning signal / intervention
↓
设计受控实验
↓
读懂结果与副作用
↓
决定 Scale / Stop / Route Elsewhere
```

所以本章不再重讲前面的定义，而是教你如何“调用”它们。

---

# 25.1 八域 Capability Map

整套知识可以压成八个能力域。

## A. Problem Framing

能回答：

```text
我们到底要修什么能力？
目标 population 是谁？
成功标准是什么？
```

主要调用：

```text
Ch10 Task Design
Ch16 Benchmark
Ch24 Operating Model
```

## B. Data Object & Supervision Design

能判断应该构造：

```text
SFT
Preference
Process Supervision
Trajectory
Recovery
Verifier Data
```

主要调用：

```text
Ch1–5
Ch13
```

## C. Data Acquisition & Generation

能决定：

```text
Human
Synthetic
Rollout
Hard Mining
Counterfactual
```

主要调用：

```text
Ch6–9
```

## D. Agent State & Trajectory Understanding

能把：

```text
Task
Environment
State
Action
Observation
Trajectory
```

拆清楚。

主要调用：

```text
Ch10–12
```

## E. Evaluation & Diagnosis

能回答：

```text
失败在哪里？
谁负责？
谁来判？
结论能说多大？
```

主要调用：

```text
Ch13–16
```

## F. Data Curation & Optimization

能处理：

```text
Quality
Dedup
Weighting
Mixture
Valuation
Experiment
```

主要调用：

```text
Ch18–21
```

## G. Production & Governance

能保证：

```text
Identity
Version
Lineage
Reproducibility
Stable Production
```

主要调用：

```text
Ch19
Ch22
```

## H. Continuous Improvement

能建立：

```text
Flywheel
Monitoring
Drift Response
Operating Model
```

主要调用：

```text
Ch17
Ch23
Ch24
```

---

# 25.2 一张端到端总图

```text
Real User / Product / Research Goal
↓
Problem Framing
↓
Task / Case / Environment
↓
Model / Agent Rollout
↓
Trajectory / Outcome Evidence
↓
Failure / Credit / Evaluator
↓
Capability Gap
↓
Data Acquisition
↓
Curation / Mixture
↓
Controlled Data Experiment
↓
Productionize Valuable Data
↓
Train / Evaluate
↓
Deploy / Monitor
↓
Fresh Failure / Drift
↺
```

任何一个 Data Project，都可以在这张图上找到自己现在所处的位置。

---

# 25.3 Problem Routing Tree：先判断问题属于哪一层

面对：

```text
“Agent failed.”
```

不要直接做数据。

先走：

```text
能复现吗？
↓
Task / Requirement 清楚吗？
↓
Tool 正常吗？
↓
Harness 正常吗？
↓
Environment / Permission 正常吗？
↓
Verifier / Judge 靠谱吗？
↓
Model behavior genuinely wrong?
↓
Data Gap plausible?
```

如果问题在前面任何一层，就优先修对应层。

这条树的详细组织 routing 见第 24 章。

---

# 25.4 如果真的是 Data Gap，再问是哪一种 Gap

```text
Coverage Gap
模型几乎没见过这类经验

Supervision Gap
见过任务，但没有合适反馈信号

Distribution Gap
训练和真实分布不一致

Decision-boundary Gap
会做，但相近选项之间不会选

Process / Recovery Gap
局部状态下不会继续、修复或验证
```

不同 Gap 对应不同 Intervention。

---

# 25.5 Data Intervention Tree

```text
不会做
→ SFT / Demonstration

多个行为不会选
→ Preference / Reward

中间步骤不稳
→ Process Supervision

当前 state 下 action 错
→ State-conditioned Trajectory Data

失败后不会恢复
→ Recovery / Counterfactual Data

边界 case 不稳
→ Hard Negative / Boundary Gold

真实分布缺失
→ Production Mining / Synthetic Expansion

只会模板
→ Decision Diversity / Cross-domain Transfer
```

这不是机械规则，而是帮助把“做 Agent Data”继续拆成真正的 learning signal design。

---

# 25.6 证据链：从“我觉得”升级成“我能证明”

一个成熟方案最好依次拥有：

```text
Observed Problem
↓
Reliable Evidence
↓
Root Cause Hypothesis
↓
Target Capability
↓
Data Intervention
↓
Controlled Experiment
↓
Target + Regression + Cost
↓
Mechanism / Transfer
↓
Decision
```

如果中间某一层缺失，后面的强结论就要收窄。

---

# 25.7 30 分钟快速诊断法

## 0–5 min：Define

写清：

```text
Problem
Population
Success Metric
Risk
```

## 5–10 min：Inspect Evidence

看：

```text
Task
Trajectory
Tool / Environment
Final State
Verifier
```

## 10–15 min：Attribute

区分：

```text
Task
Model
Tool
Harness
Environment
Evaluator
```

## 15–20 min：Decide Whether Data

如果是 Data Gap，判断：

```text
Coverage / Supervision / Distribution / Boundary / Recovery
```

## 20–25 min：Design Minimum Credible Pilot

明确：

```text
Intervention
Baseline
Budget
Frozen Eval
Guardrail
```

## 25–30 min：Define Decision Rule

提前写：

```text
什么结果 SCALE？
什么结果 REVISE？
什么结果 STOP？
```

这样 30 分钟结束时，不一定已经解决问题，但已经知道**下一步该做什么实验**。

---

# 25.8 Canonical Case C1：从线上 Failure 一路走到 Data Decision

任务：

> **如果订单 1847 还没发货，就退款；已经发货就不要动。**

线上观察到：

```text
Order = shipped
Agent still calls refund
```

## Step 1 — Task Contract

调用 Ch10：

```text
Goal
Conditional Constraint
Forbidden Side Effect
Success Predicate
```

确认任务定义没问题。

## Step 2 — Environment / Trace

调用 Ch11–12：

检查：

```text
Agent 是否真的看到 shipped？
Observation 是否进入 Context？
Executed Action 是谁产生的？
```

## Step 3 — Attribution

调用 Ch13–14：

找到：

```text
First Harmful Action
Root Cause
Failure Owner
Recoverability
```

例如：

```text
Observation 可见
Harness 正常
Model ignores precondition
```

才支持 Model/Data 方向。

## Step 4 — Evaluator

调用 Ch15：

用：

```text
Environment State
Forbidden-side-effect Predicate
```

作为主要证据，不相信模型“退款成功”的自然语言声称。

## Step 5 — Benchmark

调用 Ch16：

保留：

```text
original regression case
held-out sibling family
representative normal-order cases
```

## Step 6 — Acquisition

调用 Ch7–9：

围绕：

```text
conditional precondition / negative constraint
```

生成跨 domain variants，而不是重复订单模板。

## Step 7 — Data Intervention

可以比较：

```text
SFT
Preference
Wrong + Correction
State-conditioned Counterfactual
```

## Step 8 — Curation

调用 Ch20：

控制：

```text
family duplicate
decision diversity
hard-negative ratio
token exposure
```

## Step 9 — Experiment

调用 Ch21：

```text
matched token budget
frozen eval
failure transition
regression
cost
transfer
```

## Step 10 — Decision

调用 Ch18：

根据：

```text
Marginal Gain
Risk Reduction
Total Cost
Saturation
```

决定：

```text
SCALE / MAINTAIN / REVISE / STOP
```

## Step 11 — Production / Monitoring

如果值得规模化：

```text
Ch22 → productionize
Ch23 → monitor same failure family / drift
Ch24 → maintain owner / release gate
```

这就是整套知识体系真正被“跑起来”的样子。

---

# 25.9 不同岗位从同一个问题里看到什么？

### Data Research

```text
什么经验值得造？
用什么 supervision？
怎么证明有用？
```

### Evaluation

```text
成功到底是什么？
证据可靠吗？
Protocol 公平吗？
```

### Agent Data

```text
当前 state 下为什么选这个 action？
```

### Post-training

```text
什么 learning signal 能改变 behavior？
```

### Data Platform

```text
如何规模化后仍然可追踪、可恢复？
```

### Product / Applied AI

```text
用户到底在哪里真正受益？
风险是否降低？
```

专业协作的前提不是大家做同一件事，而是大家能围绕同一个 Capability Gap 看到自己的接口。

---

# 25.10 初级、中级、高级能力差异

### 初级

```text
怎么把任务做完？
```

关注：

```text
执行
脚本
标注
生成
```

### 中级

```text
为什么这个方案有效？
```

关注：

```text
failure
measurement
experiment
trade-off
```

### 高级

```text
什么问题值得解决？
应该在哪一层解决？
需要什么证据？
什么时候应该停止？
```

关注：

```text
Problem Framing
Causal Diagnosis
Resource Allocation
Decision Rights
System Evolution
```

真正的成长不是会更多工具，而是**更少把问题放错层**。

---

# 25.11 一份完整 Data Project Checklist

## Problem

```text
[ ] Target Capability 清楚？
[ ] Population 清楚？
[ ] Success / Risk 清楚？
[ ] Data Problem Gate 通过？
```

## Evidence / Diagnosis

```text
[ ] 有可复现 Case？
[ ] Task / Tool / Harness / Environment / Eval 排查过？
[ ] Root Cause 是 hypothesis 还是 evidence-backed？
[ ] Failure Owner 清楚？
```

## Data

```text
[ ] Learning Signal 合适？
[ ] Source 选择有理由？
[ ] Decision Diversity 足够？
[ ] Hard Negative / Recovery 是否需要？
[ ] Lineage / Rights / Privacy 清楚？
```

## Evaluation

```text
[ ] Evidence source 可靠？
[ ] Verifier / Judge 边界清楚？
[ ] Frozen Eval？
[ ] Held-out Family / Transfer？
[ ] Regression / Guardrail？
```

## Experiment

```text
[ ] Baseline 明确？
[ ] Add / Replace / Remove 选择合理？
[ ] Budget matched？
[ ] Primary metric 预先定义？
[ ] Scale / Stop Rule 预先定义？
```

## Production

```text
[ ] Production Contract？
[ ] Job / Artifact / Dataset identity？
[ ] Retry / Idempotency？
[ ] Raw Artifact retained？
[ ] Cost / Yield tracked？
```

## Deployment

```text
[ ] Shadow / Canary？
[ ] Coverage / Trigger / Calibration monitored？
[ ] Rollback Condition？
[ ] Fresh Failure capture？
```

---

# 25.12 面试题统一答题框架

面对：

> “给你一个模型问题，你怎么设计数据方案？”

可以用七步：

```text
1. Define
定义能力、population、metric

2. Diagnose
排 Task / Model / Tool / Harness / Environment / Eval

3. Hypothesize
明确为什么 Data Intervention 可能有效

4. Construct
选择 source + supervision + curation

5. Verify
建立可靠 evidence / evaluator

6. Experiment
matched budget + held-out + regression + cost

7. Flywheel
scale / stop / monitor / refresh
```

这个框架比直接回答“我会先合成 10 万条数据”成熟得多。

---

# 25.13 六个根问题

最终 25 章可以被压缩成六个问题。

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
什么时候应该进入下一轮学习？
```

如果一个 Data Project 这六问都能答清楚，通常已经具备完整的系统思维。

---

# 25.14 全书快速调用表

| 我现在的问题 | 优先读 |
|---|---|
| 数据对象 / learning signal 分不清 | Ch1–5 |
| 想做 Human / Synthetic / Hard Mining | Ch6–9 |
| Agent Task / Environment / Trace 怎么建 | Ch10–12 |
| 最终失败到底怪谁 | Ch13–14 |
| 谁来判、怎么公平比较 | Ch15–16 |
| 怎么形成持续闭环 | Ch17 |
| 数据预算投哪里 | Ch18 |
| 怎么做 lineage / version / reproducibility | Ch19 |
| 数据怎么筛、去重、混合 | Ch20 |
| 怎么证明数据有效 | Ch21 |
| 怎么稳定规模生产 | Ch22 |
| 怎么发现 drift | Ch23 |
| 团队怎么分工和推进 | Ch24 |

---

# 25.15 本章不再新增知识分支

这是全书编辑上的硬边界。

如果以后出现新内容，优先判断：

```text
是已有章节的补充？
是新的 Canonical Case？
是新的 Master Figure？
是 Glossary 补充？
是 Index / Checklist？
```

只有确实出现一个现有体系无法容纳的新领域，才考虑增加新章。

因此从这里开始：

> **知识扩张阶段结束，知识调用阶段开始。**

---

# 25.16 最终结论：LLM / Agent Data = Learning System Design

大模型数据工作已经不只是：

```text
收集
清洗
标注
```

而是：

```text
定义目标
↓
构造经验
↓
设计反馈
↓
观察行为
↓
诊断失败
↓
验证学习
↓
配置资源
↓
稳定生产
↓
持续感知变化
```

因此比起把它理解成传统 Data Pipeline，更准确的心智模型是：

> **Learning System Design。**

最终衡量一个从业者的，不是他能生产多少条数据，而是他能否：

> **从真实问题出发，找到正确的系统层，构造真正有信息量的经验，用可信证据证明学习发生，并在收益开始饱和或问题其实不属于数据时及时停止。**

这就是整套 LLM / Agent Data Knowledge System 希望留下的最终方法论。