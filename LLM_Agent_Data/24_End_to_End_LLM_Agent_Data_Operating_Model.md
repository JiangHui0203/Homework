# 第 24 章 End-to-End LLM / Agent Data Operating Model：团队如何把数据系统真正跑起来

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 23 章 Data Monitoring、Online Feedback 与 Drift Detection`](./23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
>
> 关联章节：[`第 14 章 Agent Failure Taxonomy`](./14_Agent_Failure_Taxonomy.md)、[`第 16 章 Benchmark Design 与 Evaluation Protocol`](./16_Benchmark_Design_and_Evaluation_Protocol.md)、[`第 17 章 Data Flywheel`](./17_Data_Flywheel_and_Continuous_Improvement.md)、[`第 18 章 Data Strategy 与 Data Valuation`](./18_Data_Strategy_and_Data_Valuation.md)、[`第 19 章 Data Governance、Lineage 与 Reproducibility`](./19_Data_Governance_Lineage_and_Reproducibility.md)、[`第 21 章 Data Experiments`](./21_Data_Experiments_and_Causal_Validation.md)、[`第 22 章 Data Production System`](./22_Data_Production_System.md)
>
> 本章目标：把前面关于 Human Data、Synthetic Data、Reasoning Data、Agent Task、Environment、Trajectory、Failure、Judge、Benchmark、Flywheel、Strategy、Governance、Production 与 Monitoring 的方法收束成一套 End-to-End Operating Model；理解角色分工、项目入口、Decision Rights、Failure Routing、Research vs Platform 边界、Roadmap、Handoff Contract、Operating Cadence 与 Data Project Lifecycle。
>
> 本章核心问题：**当一个真实 LLM / Agent 系统出现能力缺口、线上失败或新业务需求时，团队究竟应该由谁接手、先做什么、如何判断这是数据问题还是模型 / Tool / Harness / Product 问题、哪些环节应该平台化、哪些应该保持研究灵活性，以及怎样让一个 Data Project 从立项、验证、规模化一直走到监控与退休。**

---

# 24.0 为什么需要 Operating Model？

前面已经有大量方法：

```text
Human Annotation
Synthetic Generation
Agent Rollout
Failure Taxonomy
Verifier / Judge
Benchmark
Data Experiments
Production System
Monitoring
```

但真实团队里最容易卡住的往往不是“方法不知道”，而是：

```text
谁先看这个问题？
谁定义成功标准？
谁负责证明这是数据问题？
数据团队什么时候应该接手？
什么时候应该退回 Tool / Harness / Product？
实验结论由谁拍板？
平台团队应该建设到什么程度？
研究人员哪些东西可以自己快速写脚本？
```

如果这些不清楚，常见现象就是：

```text
线上失败
↓
大家都说“补数据”
↓
做了一批数据
↓
模型没改善
↓
继续补更多数据
```

而真正根因可能是：

```text
Tool schema 错
Harness 丢 Observation
Product Requirement 不清
Verifier 错
Model 能力不足
Data Coverage 不够
```

因此 Operating Model 的目标不是再发明一种数据方法，而是规定：

> **问题如何进入系统、如何被分流、谁负责哪一步、证据达到什么程度才能进入下一阶段。**

---

# 24.1 一个完整的数据项目入口

真实项目通常从五类信号进入。

## 24.1.1 Product Requirement

例如：

```text
希望 Agent 支持日历改期
希望模型更少误拒绝
希望代码 Agent 能处理大型仓库
```

这是 Capability Expansion。

---

## 24.1.2 Benchmark Gap

例如：

```text
Recovery Success = 42%
Verification Failure = 18%
```

说明已有 capability 有明显缺口。

---

## 24.1.3 Production Failure

例如：

```text
错误退款
错误联系人
权限不足后仍继续操作
```

这是最直接的 failure-driven signal。

---

## 24.1.4 Model Upgrade Regression

例如：

```text
新模型 overall 更好
但某类 tool use 退化
```

这类问题通常先进入 regression / failure analysis。

---

## 24.1.5 Strategic Opportunity

例如：

```text
新的 Agent workflow 出现
新的 Tool 能力上线
新的业务场景值得提前布局
```

它可能暂时没有 failure log，但具有高战略价值。

---

# 24.2 Data Project Intake：先把问题写成“项目合同”

一个 Data Project 不应该从：

```text
“做 10 万条数据”
```

开始。

更合理的 intake 至少包括：

```text
Problem Statement
Target Capability
Current Evidence
Target Population
Current Baseline
Primary Metric
Guardrail Metrics
Candidate Root Causes
Candidate Interventions
Budget
Owner
Decision Deadline
```

例如：

```yaml
problem: Agent 在 recoverable tool timeout 后经常盲目重试
capability: recovery_policy
baseline_success: 41%
primary_metric: recovery_success
critical_guardrail: duplicate_write_rate
candidate_root_causes:
  - timeout semantics not understood
  - no verify-before-retry behavior
  - recovery examples insufficient
```

这一步的价值是：

> **先把“我们要解决什么”冻结，再谈“做什么数据”。**

---

# 24.3 第一条 Decision Gate：这是 Data Problem 吗？

任何 failure 都不应该默认进入数据团队。

建议先做一次 routing：

```text
Observed Problem
↓
Task / Requirement Definition correct?
↓
Tool / API correct?
↓
Harness correct?
↓
Environment / Permission correct?
↓
Verifier / Judge correct?
↓
Model Behavior wrong?
↓
Data Gap plausible?
```

可以得到几类出口：

| Root Cause | Primary Owner | Typical Action |
|---|---|---|
| Requirement ambiguity | Product / Research | redefine task |
| Tool/API defect | Tool / Infra | fix tool |
| Harness defect | Agent Platform | fix orchestration |
| Environment defect | Environment / Eval | fix snapshot/reset |
| Verifier defect | Eval | fix grader |
| Model architecture / base capability | Model / Training | model-side change |
| Coverage / supervision gap | Data | data intervention |

所以：

> **Data Team 应该负责 Data Gap，不应该成为所有系统问题的兜底队。**

---

# 24.4 角色地图：一个成熟团队里谁负责什么？

组织名称可以不同，但功能上通常至少存在这些角色。

## 24.4.1 Product / Domain Owner

负责：

```text
用户目标
业务规则
风险边界
成功标准
优先级
```

他们定义“什么值得解决”。

---

## 24.4.2 Research / Model Scientist

负责：

```text
能力假设
failure mechanism
实验设计
训练方法
model-side intervention
scientific conclusion
```

他们回答：

> 为什么模型会这样，以及怎样证明改进机制成立。

---

## 24.4.3 Data Research / Data Scientist

负责：

```text
Data Gap 定义
sample mining
taxonomy
supervision design
mixture
Data Experiment
data valuation
```

核心不是“标数据”，而是：

> **把模型问题转换成可学习的数据问题。**

---

## 24.4.4 Evaluation / Benchmark Owner

负责：

```text
Frozen Protocol
Gold Set
Verifier / Judge
Benchmark
Regression
Metric Governance
```

他们保证：

> 改进不是因为尺子被换了。

---

## 24.4.5 Data Production / Platform

负责：

```text
queue
worker
artifact store
metadata
versioning
cost
recovery
large-scale production
```

他们保证高价值方案能规模化。

---

## 24.4.6 Human Data Operations

负责：

```text
annotation guideline
annotator routing
qualification
QC
adjudication
expert review
```

---

## 24.4.7 Agent / Tool / Harness Engineer

负责：

```text
Tool schema
runtime orchestration
context construction
memory
retry
state management
```

---

# 24.5 RACI：不是所有人都对所有事情负责

一个简化 RACI 可以是：

| Activity | Product | Research | Data | Eval | Platform |
|---|---|---|---|---|---|
| 定义业务成功 | A/R | C | C | C | I |
| Root Cause 分析 | C | A/R | R | C | C |
| Data Intervention 设计 | C | C | A/R | C | I |
| Benchmark 冻结 | I | C | C | A/R | I |
| Data Production | I | I | C | C | A/R |
| Training Experiment | I | A/R | R | C | C |
| Release Gate | A | C | C | R | C |

其中：

```text
R = Responsible
A = Accountable
C = Consulted
I = Informed
```

RACI 的价值不是官僚化，而是避免：

```text
所有人都参与
但没有人真正负责最终判断
```

---

# 24.6 一个 Failure 从线上回来后，应该怎么流转？

推荐链路：

```text
Production Failure
↓
Triage
↓
Reproduce / Verify
↓
Attribution
↓
Root Cause
↓
Capability Gap
↓
Choose Intervention
↓
Pilot
↓
Frozen Eval
↓
Scale / Stop
↓
Regression
↓
Deploy
↓
Monitor
```

其中每一步都应该有退出条件。

例如：

```text
Triage 发现 Tool Bug
→ 退出 Data Flow
→ Tool Owner
```

而不是硬把它做成训练数据。

---

# 24.7 Failure Routing：不同错误进入不同修复通道

可以建立一个 routing table：

| Failure | Primary Fix |
|---|---|
| Task misunderstanding | instruction / SFT / prompt |
| Tool selection | tool preference / tool descriptions |
| Argument construction | correction / structured supervision |
| Observation grounding | state-action data |
| Recovery failure | recovery trajectory / preference |
| Verification failure | verify-or-stop data |
| Constraint violation | negative-constraint data |
| Tool outage | infra fix + robustness eval |
| Harness context loss | harness fix |
| Judge mislabel | evaluator fix |

所以：

> **Failure Taxonomy 不只是分析工具，也是 routing policy。**

---

# 24.8 Research Mode 与 Production Mode 必须分开

一个非常常见的问题是：

```text
研究阶段就要求生产级平台
```

导致：

```text
实验还没证明方向有效
却先花大量时间建设通用框架
```

建议分两种 operating mode。

## Research Mode

允许：

```text
manual scripts
small cohort
limited reproducibility
single-node tools
narrow schema
rapid iteration
```

目标：

> 快速证明科学问题。

## Production Mode

要求：

```text
versioning
queue
retry
lineage
cost accounting
access control
monitoring
SLA
```

目标：

> 稳定规模化。

两者之间通过一个明确的：

```text
Research-to-Production Gate
```

连接。

---

# 24.9 什么东西应该平台化？

适合平台化的通常是：

```text
高频
跨项目复用
接口稳定
容易出一致性问题
```

例如：

```text
Dataset Versioning
Artifact Store
Job Queue
Judge Service
Annotation Queue
Cost Tracking
Experiment Registry
Lineage
```

而不适合过早平台化的通常是：

```text
新 failure taxonomy
新 selector feature
新 reward definition
新 agent state representation
新 synthetic strategy
```

这些在研究阶段变化很快。

所以一个很重要的原则是：

> **平台化稳定接口，不要平台化尚未稳定的研究假设。**

---

# 24.10 Handoff Contract：团队之间交接什么？

## Data → Training

不应该只交：

```text
train.jsonl
```

至少应该包含：

```text
Dataset Version
Data Card
Schema
Mixture
Build Recipe
Source / Lineage
Known Risks
Expected Capability
Regression Targets
```

## Training → Eval

应该包含：

```text
Model Version
Training Run ID
Dataset IDs
Prompt / Runtime
Generation Config
```

## Eval → Product / Research

应该包含：

```text
Primary Metric
Guardrail
Slice Results
Failure Transition
Cost
Claim Scope
Known Limitations
```

Handoff 的核心是：

> **让 downstream 团队不需要猜 upstream 做了什么。**

---

# 24.11 Decision Rights：谁有权说“可以上线”？

一个模型通过 benchmark，并不自动意味着可以上线。

Release Decision 通常至少要同时满足：

```text
Capability Gain
No Critical Regression
Safety / Policy Guardrail
Cost / Latency Bound
Production Readiness
Monitoring Ready
Rollback Ready
```

可以建立：

```text
Technical Gate
Evaluation Gate
Risk Gate
Product Gate
```

不同组织可以由不同人负责，但 decision right 必须明确。

---

# 24.12 Data Project Lifecycle

一个完整 Data Project 可以分成八个阶段。

## Stage 0 — Intake

```text
明确问题
确认业务 / 科学价值
```

## Stage 1 — Diagnosis

```text
failure reproduce
root cause
capability gap
```

## Stage 2 — Hypothesis

```text
为什么数据能解决？
哪种 supervision 可能有效？
```

## Stage 3 — Pilot

```text
小规模数据
便宜实验
找 signal
```

## Stage 4 — Confirmatory Experiment

```text
matched budget
frozen eval
regression
multi-seed when needed
```

## Stage 5 — Scale

```text
production contract
quality gate
cost control
```

## Stage 6 — Deploy / Monitor

```text
shadow
canary
monitoring
drift
```

## Stage 7 — Maintain / Retire

```text
capability saturation
stale data
portfolio rebalance
```

这意味着：

> **Data Project 有开始，也必须有结束。**

---

# 24.13 每一个 Stage 都应该有 Exit Criteria

例如 Pilot 阶段：

```text
Primary metric 有方向性 signal
没有明显 catastrophic regression
Data construction 可规模化
Verifier 可用
```

才能进入 Confirmatory。

Confirmatory 进入 Scale 前则需要：

```text
Stable gain
Matched-budget still positive
Held-out transfer
Critical guardrail pass
Reasonable ROI
```

如果不满足，就：

```text
REVISE
STOP
```

而不是因为已经花了很多钱就继续。

---

# 24.14 Quarterly Data Roadmap 应该怎么来？

不应该是：

```text
Q1 做 Tool Data
Q2 做 Agent Data
Q3 做 Reasoning Data
```

而应该来自 Capability Portfolio。

例如：

| Capability | Current Level | Importance | Risk | Gap | Data ROI | Priority |
|---|---:|---:|---:|---:|---:|---:|
| Tool Selection | high | high | med | low | low | low |
| Recovery | low | high | high | high | high | high |
| Verification | med | high | high | high | med | high |
| Tone | high | med | low | low | low | low |

然后形成：

```text
Top Priority
Recovery
Verification

Maintenance
Tool Selection

Low Priority / Retire
Tone
```

这才是真正的数据 Roadmap。

---

# 24.15 Operating Cadence：团队怎么持续运转？

可以建立不同时间尺度的 cadence。

## Daily / Continuous

```text
production health
critical failures
cost anomaly
queue backlog
```

## Weekly

```text
failure review
new clusters
judge disagreement
regression
```

## Monthly

```text
capability scorecard
data ROI
portfolio rebalance
fresh benchmark
```

## Quarterly

```text
strategic capability priorities
platform investment
retire stale assets
new roadmap
```

重点不是固定开会，而是：

> **让不同时间尺度的问题进入合适的决策周期。**

---

# 24.16 一个成熟的 Data Review 应该看什么？

不要只看：

```text
本周生产 200 万条
```

应该看：

```text
High-value Yield
Accepted Unique Data
Cost per Useful Sample
Capability Coverage
Failure Coverage
Data Freshness
Judge Agreement
Regression Growth
Downstream Gain
```

也就是说：

> **把产量指标升级成学习价值指标。**

---

# 24.17 Model Metric、Data Metric、System Metric 三层分开

## Model Metric

```text
Accuracy
Task Success
Recovery Success
Safety
```

## Data Metric

```text
Yield
Coverage
Diversity
Acceptance
Freshness
ROI
```

## System Metric

```text
Latency
Throughput
Queue Backlog
Failure Rate
Cost
```

如果三层混起来，就容易发生：

```text
生产系统更快
→ 被误解为数据更好
```

或者：

```text
数据更多
→ 被误解为模型一定会更强
```

---

# 24.18 KPI 的常见反作用

如果只考核：

```text
样本数量
```

团队会倾向生成大量便宜重复数据。

如果只考核：

```text
Judge Pass Rate
```

团队会倾向做容易通过的数据。

如果只考核：

```text
Benchmark Gain
```

可能过拟合 benchmark。

因此更合理的是组合：

```text
Downstream Gain
Cost
Coverage
Diversity
Regression
Risk
```

而不是用单个数字驱动整个数据系统。

---

# 24.19 Data Incident：数据系统也需要事故响应

典型 incident 包括：

```text
benchmark contamination
label bug
judge regression
PII leak
wrong dataset mixture
environment snapshot corruption
```

响应应该包括：

```text
Detect
Contain
Identify affected assets
Trace lineage
Re-score / Rebuild / Retrain if needed
Document root cause
Add regression / guardrail
```

这和软件事故响应非常相似，只是对象从 service 变成了：

> **Data + Model + Evaluation graph。**

---

# 24.20 一个 Data Project 的最终输出不应该只有 Dataset

成熟项目最终至少沉淀：

```text
Dataset Asset
Benchmark / Regression Asset
Failure Taxonomy Update
Verifier / Judge Asset
Experiment Evidence
Production Recipe
Monitoring Metric
Decision Record
```

也就是说：

> **一次真正高质量的数据项目，会同时留下数据、测量方法和组织知识。**

---

# 24.21 一个端到端例子：Recovery Failure Project

线上发现：

```text
Tool timeout 后重复 write
```

完整流程：

```text
Monitoring Alert
↓
Fresh Failure Cohort
↓
Triage
↓
确认 Tool 本身正常
↓
Failure Attribution
Recovery Failure
↓
Root Cause
模型未形成 verify-before-retry policy
↓
Data Hypothesis
same-state recovery preference
↓
Pilot
5k preference pairs
↓
Matched-budget Training
↓
Frozen Recovery Eval
↓
Recovery Success ↑
Duplicate Write ↓
↓
Scale
20k verified pairs
↓
Regression Set
加入真实事故 case
↓
Canary
↓
Production Monitoring
↓
Capability Gap Refresh
```

这个例子里：

```text
Monitoring
Data
Training
Eval
Production
Governance
```

全部被串在同一个 Operating Model 里。

---

# 24.22 Research 项目如何映射到这套 Operating Model？

研究环境规模更小，但逻辑并没有变化。

例如：

```text
Scientific Question
↓
Frozen Protocol
↓
Controlled Cohort
↓
Candidate Intervention
↓
Offline Labels
↓
Matched Comparison
↓
Cost Accounting
↓
Failure Analysis
↓
Conclusion
```

与生产系统相比，只是：

```text
规模更小
工程更轻
迭代更快
```

但仍然应该保留：

```text
Identity
Lineage
Frozen Decisions
Versioned Labels
Evidence
```

所以研究原型并不等于“不严谨”。

它只是：

> **用最小可信系统回答科学问题。**

---

# 24.23 一个成熟团队最重要的不是“所有东西都有平台”

而是知道：

```text
什么时候应该快速试
什么时候应该冻结
什么时候应该规模化
什么时候应该停
什么时候问题根本不属于 Data
```

这是一种比工具本身更重要的 operating judgment。

---

# 24.24 最终心智模型

整套 LLM / Agent Data Operating Model 可以压成：

```text
Sense
↓
Diagnose
↓
Prioritize
↓
Design
↓
Produce
↓
Train
↓
Evaluate
↓
Deploy
↓
Monitor
↓
Learn
```

对应：

```text
Sense
= Monitoring / User / Benchmark

Diagnose
= Failure Attribution / Root Cause

Prioritize
= Data Strategy / Valuation

Design
= Supervision / Task / Environment / Rubric

Produce
= Human / Synthetic / Rollout / Production System

Train
= SFT / Preference / RL / Policy Update

Evaluate
= Verifier / Judge / Benchmark

Deploy
= Shadow / Canary / Guardrail

Monitor
= Drift / Online Feedback

Learn
= Flywheel / Portfolio Rebalance
```

真正成熟的数据组织不是“拥有很多数据”，而是：

> **拥有一套能持续把真实问题转化为可验证学习信号，再把学习结果重新带回真实世界的 operating system。**

---

# 24.25 本章自测 / 面试题

1. 为什么线上 failure 不能默认进入 Data Team？
2. Product、Research、Data、Eval、Platform 的核心职责分别是什么？
3. 什么是 Research-to-Production Gate？
4. 哪些能力应该平台化，哪些不应该过早平台化？
5. 一个 Data Project 的八阶段生命周期是什么？
6. 为什么每个阶段都需要 Exit Criteria？
7. Quarterly Data Roadmap 应该从哪里推导？
8. 为什么 Failure Taxonomy 也可以作为 routing policy？
9. Dataset handoff 为什么不能只有一个 JSONL？
10. Model Metric、Data Metric、System Metric 为什么要分开？
11. 只看样本数量 KPI 会产生什么反作用？
12. Data Incident 应该如何响应？
13. 为什么 Data Project 的最终资产不只是 Dataset？
14. Research prototype 和 production system 的严谨性差异在哪里？
15. 什么叫“问题根本不属于 Data”？

---

# 24.26 本章总结

从前面的章节一路走到这里，可以看到 LLM / Agent Data 已经不是一个孤立的“标注岗位”问题，而是一整套能力工程：

```text
定义问题
→ 构造任务
→ 构造环境
→ 获取轨迹
→ 判断结果
→ 定位失败
→ 设计监督
→ 生产数据
→ 验证学习价值
→ 规模化
→ 上线监控
→ 重新发现问题
```

而 End-to-End Operating Model 解决的是：

> **谁来做、什么时候做、做到什么证据程度、什么时候进入下一步，以及什么时候应该停止。**

如果把前 24 章压缩成一句话：

> **现代 LLM / Agent 数据工作的核心，不是“拥有更多样本”，而是建立一个从真实能力缺口出发、能够设计学习信号、验证因果增益并持续迭代的完整系统。**
