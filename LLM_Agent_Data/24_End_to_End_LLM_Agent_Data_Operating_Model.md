# 第 24 章 End-to-End LLM / Agent Data Operating Model：团队如何把数据系统真正跑起来

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 23 章 Data Monitoring、Online Feedback 与 Drift Detection`](./23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
>
> 关联章节：[`第 14 章 Failure Taxonomy`](./14_Agent_Failure_Taxonomy.md)、[`第 17 章 Data Flywheel`](./17_Data_Flywheel_and_Continuous_Improvement.md)、[`第 18 章 Data Strategy`](./18_Data_Strategy_and_Data_Valuation.md)、[`第 21 章 Data Experiments`](./21_Data_Experiments_and_Causal_Validation.md)、[`第 22 章 Data Production System`](./22_Data_Production_System.md)、[`第 23 章 Monitoring 与 Drift`](./23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**组织级 Operating Model 的 canonical chapter。它负责 Data Problem Gate、角色分工、RACI、Decision Rights、Failure Routing、Research vs Production 边界、Handoff Contract、Stage Exit Criteria、Operating Cadence、季度 Capability Roadmap 与 Data Incident；具体数据方法继续由各 canonical chapter 负责。**
>
> 本章核心问题：**当一个真实 LLM / Agent 系统出现新需求、能力缺口、线上失败或 drift 时，谁应该先接、谁负责诊断、什么时候进入 Data Intervention、什么证据足以推进下一阶段、谁拥有最终决策权？**

---

# 24.0 Operating Model 解决的是“谁在什么时候做什么”

前 23 章已经分别回答：

```text
数据是什么
怎么造
怎么评
怎么验证
怎么治理
怎么生产
怎么监控
```

真实团队仍然会卡在：

```text
谁先看这个问题？
谁定义成功？
谁判断是不是 Data Problem？
谁负责实验结论？
谁决定上线？
谁负责长期维护？
```

因此 Operating Model 不再发明新方法，而是把已有方法组织成：

> **明确入口、明确 owner、明确 gate、明确 handoff、明确 decision right 的团队运行系统。**

---

# 24.1 一个问题通常从五类入口进入

```text
Product Requirement
Benchmark Gap
Production Failure
Model Upgrade Regression
Strategic Opportunity
```

它们都应该先变成一个明确 Intake，而不是直接变成“做数据需求”。

---

# 24.2 Project Intake：先定义问题，不先定义数据量

一个项目至少写清：

```text
Problem Statement
Target Capability
Target Population
Current Evidence
Current Baseline
Primary Metric
Guardrails
Known / Candidate Root Causes
Candidate Interventions
Budget
Owner
Decision Deadline
```

错误起点：

```text
“做 10 万条 Recovery Data”
```

更好的起点：

```text
“recoverable tool failure success 低，且 blind retry 是主要高风险模式；需要判断根因以及 data intervention 是否值得。”
```

---

# 24.3 Data Problem Gate：不是所有问题都应该交给 Data Team

推荐顺序：

```text
Requirement correct?
↓
Tool / API correct?
↓
Harness correct?
↓
Environment / Permission correct?
↓
Verifier / Judge correct?
↓
Model behavior genuinely weak?
↓
Data Gap plausible?
```

典型出口：

| Root Cause | Primary Owner | Typical Action |
|---|---|---|
| Requirement ambiguity | Product / Research | redefine task |
| Tool defect | Tool / Infra | fix tool |
| Harness defect | Agent Platform | fix orchestration |
| Environment defect | Environment / Eval | fix state / reset |
| Evaluator defect | Eval | fix verifier / judge |
| Base model bottleneck | Model / Training | model-side intervention |
| Coverage / supervision gap | Data | data intervention |

核心原则：

> **Data Team 负责 Data Gap，不负责给所有系统问题兜底。**

---

# 24.4 角色地图

## Product / Domain Owner

拥有：

```text
用户价值
业务规则
风险边界
优先级
```

## Research / Model Scientist

拥有：

```text
mechanism hypothesis
model-side intervention
scientific conclusion
```

## Data Research / Data Scientist

拥有：

```text
Data Gap
supervision design
mining / synthesis policy
data experiment proposal
```

## Evaluation / Benchmark Owner

拥有：

```text
measurement object
frozen protocol
gold / verifier / judge
release evidence
```

## Data Production / Platform

拥有：

```text
queue
worker
artifact
lineage plumbing
cost
reliability
```

## Human Data Operations

拥有：

```text
guideline execution
annotator routing
QC
adjudication
```

## Agent / Tool / Harness Engineer

拥有：

```text
tool contract
runtime orchestration
context / memory
retry / state management
```

组织名称可以不同，但这些功能必须有人明确承担。

---

# 24.5 Responsible、Accountable、Consulted、Informed

RACI 的作用不是增加流程，而是解决：

```text
所有人都参与
但没人拥有最终判断
```

示意：

| Activity | Product | Research | Data | Eval | Platform |
|---|---|---|---|---|---|
| 业务成功定义 | A/R | C | C | C | I |
| Root Cause | C | A/R | R | C | C |
| Data Intervention | C | C | A/R | C | I |
| Frozen Eval | I | C | C | A/R | I |
| Data Production | I | I | C | C | A/R |
| Training Experiment | I | A/R | R | C | C |
| Release Evidence | A | C | C | R | C |

重点不是照抄表格，而是每个项目都要知道：

> **谁负责做，谁负责最终拍板。**

---

# 24.6 Failure Routing：Taxonomy 应该直接连到 Action

不同 failure 的第一修复通道不同：

| Failure | First Candidate Fix |
|---|---|
| Task misunderstanding | Prompt / SFT / requirement |
| Tool selection | tool description / preference / data |
| Argument error | structured correction |
| Observation grounding | state-action supervision / harness audit |
| Recovery failure | recovery supervision |
| Verification failure | verify-or-stop supervision / verifier audit |
| Constraint violation | negative-constraint data / task contract |
| Tool outage | infra fix |
| Harness context loss | harness fix |
| Judge mislabel | evaluator fix |

因此 Ch14 的 Failure Taxonomy 不只是分析表，也是组织 routing interface。

---

# 24.7 一个 Production Failure 的标准流转

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
Confirmatory Eval
↓
Scale / Stop
↓
Regression
↓
Deploy
↓
Monitor
```

任何阶段都允许退出当前通道。

例如：

```text
Triage → Tool Bug
```

应该立即离开 Data Flow，交给 Tool Owner。

---

# 24.8 Research Mode 与 Production Mode

## Research Mode

目标：

```text
尽快回答科学问题
```

允许：

```text
manual script
small cohort
narrow schema
limited concurrency
manual audit
```

## Production Mode

目标：

```text
长期稳定规模化
```

要求更多：

```text
queue
retry
lineage
permissions
cost accounting
monitoring
SLA
```

两者不是谁更高级，而是问题阶段不同。

---

# 24.9 Research-to-Production Gate

一个方法从研究脚本进入平台前，至少应回答：

```text
Scientific signal stable?
Target population clear?
Eval protocol frozen?
Known failure modes?
Cost model known?
Schema stable enough?
Expected scale large enough?
Repeated reuse likely?
```

如果这些还在高速变化，就不应急于做通用平台。

核心原则：

> **平台化稳定接口，不平台化尚未稳定的研究假设。**

---

# 24.10 什么值得平台化？

通常满足：

```text
高频复用
跨项目共用
接口相对稳定
一致性错误成本高
```

例如：

```text
Artifact Store
Dataset Versioning
Job Queue
Judge / Verifier Interface
Annotation Queue
Experiment Registry
Cost Tracking
```

而：

```text
新 selector feature
新 reward definition
新 failure taxonomy prototype
新 synthetic strategy
```

应优先留给研究侧快速迭代。

---

# 24.11 Handoff Contract：团队之间不能只传一个文件

## Data → Training

```text
Dataset Version
Schema
Data Card
Build Recipe
Mixture Recommendation
Known Risks
Expected Capability
Regression Targets
```

## Training → Eval

```text
Model Version
Run ID
Dataset IDs
Training Config
Runtime / Prompt
```

## Eval → Product / Research

```text
Primary Metric
Guardrails
Slices
Failure Transition
Cost
Claim Scope
Known Limitations
```

Handoff 的目标是：

> **下游不需要猜上游到底做过什么。**

---

# 24.12 Decision Rights：谁能说“继续”“停止”“上线”“回滚”？

建议至少区分：

```text
Scientific Decision
方法是否有证据

Data Investment Decision
是否值得扩规模

Release Decision
是否允许上线

Risk Decision
高风险 guardrail 是否可接受

Operational Decision
是否需要 rollback / pause
```

同一个人不一定拥有全部权力。

Decision Right 不清，是很多跨团队冲突的根源。

---

# 24.13 Release Gate

一个模型 / data intervention 进入线上，至少要满足：

```text
Primary capability acceptable
No critical regression
Safety / policy guardrail pass
Cost / latency acceptable
Production readiness
Monitoring ready
Rollback ready
```

所以：

```text
Benchmark Win
≠ Automatic Release
```

---

# 24.14 Data Project Lifecycle

建议八阶段：

```text
1. Intake
2. Diagnosis
3. Hypothesis
4. Pilot
5. Confirmatory
6. Scale
7. Deploy / Monitor
8. Maintain / Retire
```

每个阶段都必须有 Exit Criteria。

---

# 24.15 Stage 1 — Intake Exit Criteria

至少明确：

```text
Target Capability
Population
Business / Research Value
Metric
Owner
```

问题都没定义清楚，不进入后续。

---

# 24.16 Stage 2 — Diagnosis Exit Criteria

至少知道：

```text
问题可复现
failure owner 大致明确
非数据类明显根因已排除
有足够 evidence 支持下一步 hypothesis
```

否则不要急着生产数据。

---

# 24.17 Stage 3 — Hypothesis Exit Criteria

把“补数据”改写成可检验假设：

```text
If we expose model to X supervision
under Y state distribution,
then Z capability should improve,
without breaking guardrail G.
```

如果无法写出这样的假设，通常说明 intervention 仍然太模糊。

---

# 24.18 Stage 4 — Pilot Exit Criteria

Pilot 只回答：

```text
有没有值得继续追的 signal？
```

不是要求一次证明最终结论。

输出可以是：

```text
PROMISING
NO SIGNAL
REVISE
STOP
```

---

# 24.19 Stage 5 — Confirmatory Exit Criteria

需要：

```text
frozen protocol
held-out eval
matched budget where relevant
regression
cost
claim scope
```

这里才支持更强结论和大规模资源申请。

---

# 24.20 Stage 6 — Scale Exit Criteria

规模化前要确认：

```text
Production Contract stable
Quality Gate defined
Lineage / Cost ready
Known failure handling ready
Data yield economics acceptable
```

否则规模只会放大混乱。

---

# 24.21 Stage 7 — Deploy / Monitor Exit Criteria

至少有：

```text
Shadow / Canary when needed
Release Gate
Rollback Condition
Monitoring Slices
Fresh Failure Capture
```

Data Project 不是文件交付完就结束。

---

# 24.22 Stage 8 — Maintain / Retire

定期问：

```text
能力是否饱和？
数据是否 stale？
边际收益是否下降？
新 frontier 是否出现？
这类数据是否还值得继续维护？
```

然后：

```text
Maintain
Reduce
Retire
Archive
```

---

# 24.23 Operating Cadence

不同时间尺度回答不同问题。

### Daily / Release

```text
critical incident
blocking regression
production health
```

### Weekly

```text
failure composition
experiment status
fresh cohort
production bottleneck
```

### Monthly

```text
capability movement
data ROI
portfolio rebalance
stale asset review
```

### Quarterly

```text
capability roadmap
strategic gaps
platform investment
retirement / exploration
```

不要把所有问题都塞进同一个周会。

---

# 24.24 Quarterly Data Roadmap 应从 Capability 推出来

不推荐：

```text
Q1 做 Agent Data
Q2 做 Reasoning Data
```

更推荐：

```text
Capability Level
× Business Importance
× Risk
× Gap
× Measured Data ROI
```

得到：

```text
Increase
Maintain
Explore
Reduce
Retire
```

例如 Recovery / Verification 仍弱且高风险，就加预算；Tone 已经饱和，就减少新增投入。

---

# 24.25 Data Incident：数据系统也会出事故

典型 incident：

```text
Benchmark Contamination
Label Bug
Judge Regression
PII Exposure
Wrong Mixture
Environment Corruption
Broken Lineage
```

处理流程：

```text
Detect
↓
Contain
↓
Trace Impact via Lineage
↓
Correct Source
↓
Re-score / Rebuild / Retrain / Rollback
↓
Add Regression / Guardrail
```

Data Incident 不应只修当前文件，还要追受影响模型和结论。

---

# 24.26 Decision Log：重要选择要留下“为什么”

推荐记录：

```text
Decision
Evidence
Alternatives Considered
Owner
Date
Expected Outcome
Review Date
```

例如：

```text
为什么选择 Synthetic + Human Audit
而不是全专家标注？
```

半年以后不应该只能靠某个人记忆回答。

---

# 24.27 Canonical Case C1：一个 failure 如何流经团队

线上发现：

> 已发货订单仍被 Agent 尝试退款。

```text
Monitoring
→ Failure spike

Eval / Research
→ reproduce + verify

Tool / Harness
→ contract / context healthy

Research + Data
→ root cause = precondition grounding gap

Data
→ propose matched task family + supervision

Eval
→ freeze target + regression set

Data Experiment
→ small pilot, matched budget

Strategy
→ SCALE if ROI / risk reduction acceptable

Platform
→ productionize data build

Training
→ model update

Eval
→ release evidence

Product / Risk
→ release decision

Monitoring
→ watch same failure family + guardrails
```

这就是 Operating Model 真正要解决的问题：

> **让一个问题沿正确 owner 和证据链流动，而不是在团队之间来回甩锅。**

---

# 24.28 常见组织失败模式

1. 所有线上问题默认叫 Data Problem。
2. Product 没定义成功，Research / Data 自己猜目标。
3. 没有 Accountable owner，所有人都参与但没人拍板。
4. Failure taxonomy 和 routing policy 脱节。
5. Research 方向尚未验证就先建大平台。
6. Data Team 只交 JSONL，没有 Handoff Contract。
7. Eval 只给一个总分，没有 guardrail / slice / claim scope。
8. Pilot 没 signal 仍因 sunk cost 自动扩规模。
9. 数据项目没有 retirement，长期只增不减。
10. 事故修完当前数据，却没有沿 lineage 查影响范围。
11. Quarterly roadmap 按“数据类型”排，而不是按 capability gap 排。
12. Release 没有 rollback owner 和 trigger。

---

# 24.29 从岗位视角看 Operating Model

成熟从业者不只是会自己做一个模块，还要知道：

```text
什么时候找 Product
什么时候找 Tool / Harness
什么时候需要 Eval owner
什么时候 Data Intervention 才合理
什么时候 Research 结果足以交给 Platform
什么时候应该 Stop
```

这就是从“执行一个数据任务”升级到“推动一个 Data Project”。

---

# 24.30 面试 / 自检问题

1. 为什么真实 failure 不能默认交给 Data Team？
2. Data Problem Gate 应该检查哪些层？
3. Product / Research / Data / Eval / Platform 的职责分别是什么？
4. RACI 解决什么问题？
5. Failure Taxonomy 怎样变成 Routing Policy？
6. Research Mode 与 Production Mode 有什么区别？
7. Research-to-Production Gate 应该检查什么？
8. 什么适合平台化，什么不适合过早平台化？
9. Handoff Contract 为什么不能只传文件？
10. Scientific / Investment / Release / Risk Decision Rights 为什么要分开？
11. Data Project 八阶段是什么？
12. 为什么每个 Stage 都需要 Exit Criteria？
13. Quarterly Data Roadmap 为什么应该从 Capability Map 推导？
14. 什么是 Data Incident？
15. Decision Log 有什么价值？
16. 一个线上 failure 如何从 Monitoring 一直流到 Release？

---

# 24.31 本章最终心智模型

```text
Sense a Problem
↓
Data Problem Gate
↓
Assign Owner
↓
Diagnose
↓
Choose Intervention
↓
Pilot
↓
Confirm
↓
Scale
↓
Deploy
↓
Monitor
↓
Maintain / Retire
```

整条链上都必须明确：

```text
Owner
Evidence
Exit Criteria
Decision Right
Handoff
```

一句话：

> **成熟的数据组织，不是拥有很多数据，而是拥有一套能持续把真实问题转化成可验证学习信号，再把学习结果重新带回真实世界的 Operating System。**

下一章第 25 章不再讲组织怎么跑，而是切回个人 practitioner：

> **如果今天把一个真实 LLM / Agent Data 问题交到你手里，你怎样在 30 分钟内调用前 24 章的正确模块，并设计下一步？**