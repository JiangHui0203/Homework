# LLM / Agent Data Knowledge System：全书精修施工图

> 状态：Editorial Blueprint / Read-only Audit Output
>
> 适用范围：`LLM_Agent_Data_Knowledge_System.md` + `LLM_Agent_Data/04_...` 至 `25_...`
>
> 原则：**先定结构，再改正文；先定概念归属，再做去重；先定术语，再做交叉引用；先定 canonical case，再统一案例；最后才做视觉与索引。**
>
> 本文件不是正文，不新增知识章节。它是后续精修 1–25 章时的施工依据。

---

# 0. 编辑目标

当前知识体系已经完成“内容扩展阶段”，后续目标不再是继续增加章节，而是把已有 25 章编辑成一套真正可导航、可学习、可检索、可用于面试和项目实践的完整方法论。

后续精修围绕六个目标展开：

```text
1. Architecture
   全书结构是否清楚？

2. Ownership
   每个核心概念的 canonical definition 属于哪一章？

3. Consistency
   术语、公式、符号、案例是否前后一致？

4. Compression
   是否存在不必要的重复解释？

5. Navigation
   读者能否快速知道“遇到这个问题该读哪章”？

6. Application
   理论是否通过 canonical case、decision tree、checklist 变成可执行能力？
```

---

# 1. 编辑动作标签

后续逐章修改统一使用以下动作标签。

| 标签 | 含义 |
|---|---|
| `KEEP` | 保留现有内容与位置 |
| `TRIM` | 压缩重复解释，但不删除核心思想 |
| `MOVE` | 内容更适合归到其他 canonical chapter |
| `LINK` | 用交叉引用替代重复完整解释 |
| `UNIFY` | 统一术语、符号、定义或格式 |
| `VERIFY` | 后续做事实、数字、论文题名、引用核验 |
| `ADD INDEX` | 加入概念、案例、岗位、面试或章节索引 |
| `ADD CASE` | 接入 canonical case |
| `ADD FIGURE` | 接入 master figure 或统一图示 |

核心纪律：

> `TRIM` 不等于删掉知识；`LINK` 不等于降低信息量。目标是让“完整定义只出现一次，后文只保留当前章节独有的应用”。

---

# 2. 建议的最终书级结构

不重新编号 1–25 章，只增加 Part 层级。

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

书级主线：

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

| Canonical Concept | 主章节 | 其他章节处理方式 |
|---|---:|---|
| Dataset / Sample / Task / Episode / Trajectory | 1 | 后文引用，不重新定义 |
| Pretraining / SFT / Post-training | 2 | 后文引用 |
| Preference / Reward | 3 | Judge / evaluator 引到 15 |
| Correctness / Risk / Recoverability | 4 | 9 / 13 / 16 只应用 |
| Tool-use / Agent trajectory basics | 5 | 后文进入更专业层 |
| Human annotation / Gold / IAA | 6 | 15 只讲 Judge calibration |
| Synthetic generation | 7 | 20 只讲 filtering / dedup consequence |
| Candidate / Rollout / Best-of-N | 8 | 16 只讲 evaluation protocol |
| Hard Case / Frontier / Active Sampling | 9 | 18 只讲投资价值 |
| Task Contract | 10 | 全书统一引用 |
| Tool / Harness / Environment | 11 | 全书统一使用 |
| Trajectory schema / event / state lineage | 12 | 19 讲 system-level lineage |
| Credit / First Harmful / Last Recoverable | 13 | 14 用于 failure diagnosis |
| Failure taxonomy / root cause | 14 | 17 / 24 用于 routing |
| Verifier / Grader / Judge | 15 | 全书引用 |
| Benchmark / Frozen Protocol / statistics | 16 | 21 只讲 data intervention experiment |
| Data Flywheel | 17 | 23 是 sensing / refresh layer |
| Data Value / ROI / Portfolio | 18 | 9 不再深讲 valuation |
| Governance / Version / Provenance | 19 | 6 / 12 只保留局部需求 |
| Quality / Filtering / Dedup / Mixture | 20 | 2 / 7 只作预告 |
| Data causal experiment | 21 | 16 提供实验基础 |
| Production system | 22 | 24 讲组织使用方式 |
| Monitoring / Drift | 23 | 17 只讲闭环位置 |
| Operating Model | 24 | 团队 / 组织 operating system |
| Integrated problem solving | 25 | 不再引入新概念 |

---

# 4. Canonical Terminology / Glossary 待冻结项

后续建议新增独立 `Glossary_and_Notation.md`，至少冻结：

```text
Task
Case
Episode
Trajectory
State
World State
Agent-visible State
Reasoning State
Working State
Observation
Action
Outcome
Reward
Credit
Error
Failure
Symptom
Root Cause
Risk
Correctness
Recoverability
Repairability
Selectability
Verifier
Grader
Judge
Data Asset
Data Batch
Dataset View
Capability
Failure Family
Regression Case
Frontier Case
```

建议术语规则：

- 避免裸写 `State`，尽量写 `World State / Agent-visible State / Reasoning State / Working State`。
- `Outcome` = 世界实际发生什么。
- `Reward` = 人为设计的优化信号。
- `Credit` = Outcome / Reward 对中间决策的归因。
- `Error` 更适合局部行为错误。
- `Failure` 更适合 episode / subgoal 未满足要求。
- `Root Cause` 不等于 `First Error`，也不等于 `First Harmful Action`。
- `Recoverability` = 理论上是否存在未来策略可恢复。
- `Repairability` = 当前允许动作与预算下是否实际可修。
- `Verifier ⊂ Grader` 可作为全书实用约定；`Judge` 强调解释性判断。

---

# 5. Canonical Case 体系

后续正式固定 5 个贯穿案例。

## C1 — Order / Refund Agent

覆盖：

```text
conditional constraints
tool selection
observation grounding
forbidden side effects
credit assignment
failure attribution
verifier
recovery
```

代表任务：

> “如果订单还没发货就退款；已经发货就不要动。”

---

## C2 — Calendar / Meeting Agent

覆盖：

```text
entity resolution
time / timezone
multi-constraint
state update
notification
verification
negative constraints
```

代表任务：

> “把产品组会议改到周五 15:00，但周会不要动，并通知所有参会人。”

---

## C3 — File / Repository Agent

覆盖：

```text
read vs write
permission
irreversibility
negative constraints
side effects
rollback
versioning
```

代表任务：

> “清理重复文件，但 `.env` 和 protected files 不能修改。”

---

## C4 — Reasoning Continue / Repair

覆盖：

```text
same prefix
risk
continue / stop
branch / repair
candidate selection
rescue / harmful
compute budget
```

用于连接第 4 / 8 / 9 / 13 / 16 章。

---

## C5 — Code / Execution Agent

覆盖：

```text
executable verifier
unit tests
candidate generation
runtime environment
retry
benchmark
```

用于连接 Synthetic / Verifier / Benchmark / Production。

---

# 6. Master Figure 计划

不追求每章塞图，建议最终只维护约 14 张全书级 Master Figure。

```text
F1  Learning System Overview
F2  Data Object / Learning Signal Evolution
F3  Correctness–Risk–Recoverability
F4  Agent Task–Environment–Trajectory
F5  Trajectory Anatomy / Event Log
F6  Credit → Failure Causal Map
F7  Evaluator Stack: Evidence → Verifier → Grader → Judge
F8  Frozen Benchmark Protocol
F9  Data Flywheel
F10 Data Strategy / Portfolio / ROI
F11 Governance / Lineage DAG
F12 Data Production System
F13 Monitoring / Drift Diagnostic Tree
F14 Operating Model + Capability Map
```

原则：

> 图承担“压缩关系”的作用，不承担装饰作用。

---

# 7. 1–25 章逐章精修施工图

## 第 1 章 — 数据对象与学习信号

**定位：全书基础词典。**

- `KEEP` Dataset / Sample / Task / Episode / Trajectory 的基本区分。
- `KEEP` Source / Supervision / Granularity / Purpose 四维数据分类。
- `KEEP` Demonstration / Preference / Reward / Process / Environment Feedback。
- `UNIFY` Task / Episode / Trajectory 定义，使其与第 10 / 12 章完全一致。
- `TRIM` 后文已经深入解释的 Agent 细节，只保留基础概览。
- `ADD INDEX` 在章末加“本章术语在后续哪里展开”。
- `STRUCTURE` 建议从总入口拆成独立 `01_...md`。

**Exit condition：** 全书任何基础对象都能回到第 1 章找到唯一标准定义。

---

## 第 2 章 — Pretraining / Instruction / SFT / Post-training

**定位：训练阶段与数据用途总览。**

- `KEEP` Pretraining / SFT / Preference / RM / RL / Agent training 的边界。
- `KEEP` `SFT Data ⊂ Post-training Data`。
- `KEEP` pretraining pipeline / dedup / contamination 的概览。
- `TRIM` Data Mixture 深讲，正式 owner 改为第 20 章。
- `LINK` contamination 详细治理 → 第 16 / 19 / 20 章。
- `LINK` data quality → 第 20 章。
- `UNIFY` Training Data / Evaluation Data / Regression Data 的目的标签。
- `STRUCTURE` 建议拆成独立 `02_...md`。

**Exit condition：** 读者理解“不同训练阶段需要什么数据”，但不在这里学习完整 mixture / governance。

---

## 第 3 章 — Preference / Reward / Feedback

**定位：相对监督与行为偏好。**

- `KEEP` `(x, y_w, y_l)`、pointwise / pairwise / listwise。
- `KEEP` Human / AI / Rule / Environment feedback source。
- `KEEP` RM / DPO / hard negative / bias。
- `KEEP` Agent trajectory preference。
- `TRIM` Grader / Verifier / Judge 的定义性解释。
- `LINK` 自动评价体系 → 第 15 章。
- `LINK` preference data 的生产与 selection → 第 8 章。
- `UNIFY` Reward / Outcome / Preference terminology with 第 13 章。
- `STRUCTURE` 建议拆成独立 `03_...md`。

**Exit condition：** 第 3 章回答“多个行为里哪个更值得”，而不是“谁来判”。

---

## 第 4 章 — Reasoning Data / Process Supervision

**定位：Reasoning state supervision 的 canonical chapter。**

- `KEEP` Correctness / Risk / Recoverability 三分。
- `KEEP` Error Localization / Step Segmentation / PRM / ORM。
- `KEEP` `Low confidence ≠ Wrong ≠ Worth repairing`。
- `KEEP` Future Information offline-only discipline。
- `KEEP` Continue / Stop vs Branch / Repair。
- `KEEP` same-prefix counterfactual 与 rescue / harmful / neutral。
- `LINK` Selector / Best-of-N → 第 8 章。
- `LINK` Credit / Last Recoverable State → 第 13 章。
- `LINK` formal intervention evaluation → 第 16 章。
- `VERIFY` More Thinking 正式论文题名、副标题、数字与 benchmark 名称。
- `ADD CASE` C4 作为本章主案例。
- `ADD FIGURE` F3。

**Exit condition：** Correctness / Risk / Recoverability 的所有后续使用都能链回本章。

---

## 第 5 章 — Tool-use / Agent Trajectory Data

**定位：Agent Data 入门章。**

- `KEEP` Function Calling ⊂ Tool-use ⊂ Agent Trajectory。
- `KEEP` Tool-use 七个决策问题。
- `KEEP` Tool Success ≠ Task Success。
- `KEEP` Final Response ≠ Final Environment State。
- `KEEP` read / write、side effect、observation grounding。
- `TRIM` 5.17 Agent Credit Assignment：保留概览，深讲 `LINK → Ch13`。
- `TRIM` 5.18 Model / Tool / Harness / Environment failure：保留例子，完整 taxonomy `LINK → Ch11 / Ch14`。
- `TRIM` reward / preference 深入内容，分别链回 Ch3 / Ch13。
- `ADD CASE` C1。
- `UNIFY` Agent State 术语与 Ch12。

**Exit condition：** 本章负责解释“Agent Data 比普通 QA 多了什么”，不承担完整 credit / failure theory。

---

## 第 6 章 — Human Data

**定位：人工监督与 annotation quality。**

- `KEEP` annotation form / staffing / guideline / taxonomy / abstention。
- `KEEP` Gold / IAA / calibration / adjudication / confidence。
- `KEEP` Human-in-the-loop 与 AI assist。
- `KEEP` Label Provenance 作为 annotation-specific requirement。
- `TRIM` Label Versioning 的 system-level治理说明。
- `LINK` label version / decision freeze → Ch19。
- `LINK` Judge calibration → Ch15。
- `UNIFY` Gold Set / Anchor Set / Regression Set 的区分。

**Exit condition：** 人工数据所有问题都从“定义标准与稳定判断”出发，不承担全系统治理。

---

## 第 7 章 — Synthetic Data

**定位：合成任务、回答、轨迹、环境的方法论。**

- `KEEP` Self-Instruct / Teacher / Distillation / Task Synthesis / Evolution。
- `KEEP` hard negative / synthetic reasoning / synthetic trajectory / environment / user。
- `KEEP` `Synthetic ≠ Cheap Ground Truth`。
- `KEEP` Decision Diversity / Failure Diversity。
- `TRIM` Lineage 深讲，`LINK → Ch19`。
- `TRIM` Contamination 深讲，`LINK → Ch16 / Ch20`。
- `TRIM` Dedup 细节，`LINK → Ch20`。
- `TRIM` Data ROI / value 细节，`LINK → Ch18`。
- `ADD CASE` C5（代码）+ C1（Agent synthetic environment）。

**Exit condition：** 本章回答“如何合成有价值经验”，不负责完整 curation / governance。

---

## 第 8 章 — Rollout / Rejection Sampling / Candidate Selection

**定位：从 state 产生候选并做选择。**

- `KEEP` rollout / on-policy / multiple rollout。
- `KEEP` candidate diversity / Best-of-N / rejection sampling / self-consistency。
- `KEEP` verifier-guided / reward-guided / hybrid selection。
- `KEEP` abstain / reject all / threshold / oracle analysis。
- `KEEP` same-prefix / same-state candidate data。
- `KEEP` RoTFuse/K17 作为具体实例，但避免把阶段性结果写成普遍结论。
- `TRIM` benchmark statistics / confidence / cost 细节，`LINK → Ch16`。
- `TRIM` selection-induced distribution shift，保留本章特有 selector bias，通用 filtering shift `LINK → Ch20`。
- `UNIFY` Rescue / Harmful 定义引用 Ch4。
- `ADD CASE` C4。

**Exit condition：** Generation、Evaluation、Selection、Conversion 四阶段边界清楚。

---

## 第 9 章 — Hard Case Mining / Curriculum

**定位：下一条数据应该去哪找。**

- `KEEP` Human-hard / Model-hard / State-hard / Evaluation-hard / Learning-hard。
- `KEEP` capability frontier / active learning / uncertainty / disagreement / near miss / adversarial。
- `KEEP` Failure Seed → Synthetic Family / Root Cause Mining。
- `KEEP` curriculum / self-paced / anti-curriculum。
- `TRIM` Data Marginal Value 的战略深讲。
- `LINK` ROI / Portfolio / Stop Rule → Ch18。
- `LINK` uncertainty calibration → Ch23（monitoring）/ Ch16（eval）。
- `LINK` downstream proof of mining value → Ch21。
- `ADD CASE` C4 + C1。

**Exit condition：** 本章负责 acquisition policy，不负责最终 data investment 决策。

---

## 第 10 章 — Agent Task Design

**定位：Task Contract 的 canonical chapter。**

- `KEEP` Prompt / Task / Episode / Benchmark Case。
- `KEEP` Task Contract tuple / schema。
- `KEEP` Goal / Initial State / Hidden State / Toolset / Constraints / Permission / Success / Termination。
- `KEEP` Feasibility / Dependency / Difficulty。
- `UNIFY` Case / Episode terminology with Ch1 / Ch16。
- `LINK` Environment implementation → Ch11。
- `LINK` verifier implementation → Ch15。
- `ADD CASE` C2 作为主案例。
- `ADD FIGURE` F4 的 Task 部分。

**Exit condition：** “一句 prompt 不等于 Agent Task”成为全书稳定定义。

---

## 第 11 章 — Environment Design

**定位：Tool / Harness / Environment 的 canonical chapter。**

- `KEEP` Tool / Harness / Environment 三分。
- `KEEP` State / Transition / Observation / Reset / Snapshot。
- `KEEP` time / concurrency / transaction / idempotency / permission / isolation / failure injection。
- `KEEP` simulator / sim-to-real / environment confounding。
- `UNIFY` Infrastructure failure terminology with Ch14 / Ch22 / Ch23。
- `LINK` Agent event representation → Ch12。
- `LINK` production retry → Ch22。
- `ADD CASE` C1 / C3。

**Exit condition：** 后文不再重新定义 Tool、Harness、Environment。

---

## 第 12 章 — Agent Trajectory Anatomy

**定位：结构化 trajectory representation。**

- `KEEP` typed event log + state lineage + execution evidence。
- `KEEP` World / Agent-visible / Working / Memory state。
- `KEEP` Decision Intent vs Executed Action。
- `KEEP` event schema / identity / lineage / runtime / cost / evaluation fields。
- `KEEP` segmentation / branch / retry / backtrack / replay。
- `UNIFY` State terminology with glossary。
- `TRIM` system-wide governance / provenance，`LINK → Ch19`。
- `LINK` causal attribution → Ch13。
- `ADD FIGURE` F5。
- `ADD CASE` C1。

**Exit condition：** 本章回答“如何记录一条 trajectory”，而不是“如何治理整个数据系统”。

---

## 第 13 章 — Task Success / Credit Assignment

**定位：从 outcome 到中间 decision 的因果归因。**

- `KEEP` Outcome / Reward / Credit 三分。
- `KEEP` terminal / partial / step reward。
- `KEEP` hard constraint vs soft objective。
- `KEEP` progress / information gain / side effect / efficiency。
- `KEEP` First Error / First Harmful / Root Cause 区分。
- `KEEP` Last Recoverable / Point of No Return。
- `KEEP` counterfactual credit / same-state discipline。
- `KEEP` Recoverability vs Repairability。
- `LINK`完整 Failure taxonomy → Ch14。
- `UNIFY` Rescue / Harmful 语义引用 Ch4。
- `ADD FIGURE` F6。
- `ADD CASE` C1 + C4。

**Exit condition：** 所有“哪一步负责”的问题都回到本章。

---

## 第 14 章 — Agent Failure Taxonomy

**定位：唯一完整 failure diagnosis taxonomy。**

- `KEEP` Failure Record schema。
- `KEEP` L0–L14 Failure Stack。
- `KEEP` Symptom / Layer / Root Cause / First Harmful / Recoverability / Severity / Detectability。
- `KEEP` Infrastructure Failure 单列。
- `KEEP` failure → supervision / system fix routing。
- `TRIM` Credit theory 解释，`LINK → Ch13`。
- `TRIM` Task / Tool / Environment 定义，`LINK → Ch10 / Ch11`。
- `ADD INDEX` 形成 failure-type → recommended data intervention 快查表。
- `ADD CASE` C1 / C2 / C3。

**Exit condition：** 全书只在这里维护完整 taxonomy。

---

## 第 15 章 — Grader / Verifier / LLM-as-a-Judge

**定位：evaluation instrument 的 canonical chapter。**

- `KEEP` Verifier / Grader / Judge 区分。
- `KEEP` Evidence-first principle。
- `KEEP` deterministic / executable / environment-state / rule / structured grader / LLM judge。
- `KEEP` pointwise / pairwise / listwise。
- `KEEP` bias / variance / calibration / meta-evaluation / hacking。
- `KEEP` hierarchical routing / human gold。
- `UNIFY` Reward Model vs Judge vs Verifier terminology with Ch3。
- `LINK` benchmark-level protocol → Ch16。
- `LINK` Gold annotation details → Ch6。
- `ADD FIGURE` F7。
- `ADD CASE` C1 + C5。

**Exit condition：** “谁来判”只在这里完整回答。

---

## 第 16 章 — Benchmark Design / Evaluation Protocol

**定位：科学比较与测量协议。**

- `KEEP` Evaluation Question / Capability Taxonomy / Scope / Sampling。
- `KEEP` representative / challenge / regression / safety set。
- `KEEP` contamination / split / frozen protocol。
- `KEEP` paired / matched / repeated runs / confidence interval。
- `KEEP` Rescue / Harmful / Trigger / Generator / Selector / E2E 分拆。
- `KEEP` Pass@k / Success@Budget / Pareto / cost-aware。
- `KEEP` denominator discipline / micro / macro / weighted。
- `KEEP` ablation / budget-matched baseline / negative-result scope。
- `KEEP` corrected labels / frozen decisions as evaluation use case，但 governance details `LINK → Ch19`。
- `STRUCTURE` 不拆章，但建议章内增加 4 个导航块：Measurement Object / Protocol / Statistics / Cost & Claim。
- `ADD FIGURE` F8。

**Exit condition：** 本章回答“怎么证明更好”，不是“数据本身有没有价值”（后者 Ch21）。

---

## 第 17 章 — Data Flywheel

**定位：闭环编排层。**

- `KEEP` Production / Benchmark / Simulation → Mining → Gap → Data → Train → Eval → Deploy。
- `KEEP` Production Log ≠ Training Data。
- `KEEP` triage / failure prioritization / root cause abstraction / capability frontier refresh。
- `KEEP` offline vs online flywheel / online feature vs offline supervision。
- `TRIM` Active Learning 细节，`LINK → Ch9`。
- `TRIM` Data valuation 细节，`LINK → Ch18`。
- `TRIM` Governance 细节，`LINK → Ch19`。
- `LINK` monitoring/drift → Ch23。
- `ADD FIGURE` F9。

**Exit condition：** 本章展示闭环如何转，不重复每个子模块的方法论。

---

## 第 18 章 — Data Strategy / Data Valuation

**定位：数据投资与资源配置的 canonical chapter。**

- `KEEP` Data Asset / Batch / Investment。
- `KEEP` Portfolio / Capability Gap / Data ROI / Total Cost / Yield。
- `KEEP` Marginal Utility / Stop Rule / Risk-weighted investment。
- `KEEP` Build vs Buy vs Generate vs Mine。
- `KEEP` source portfolio / retirement / freshness / exploration budget。
- `TRIM` Mixture 技术细节，`LINK → Ch20`。
- `LINK` controlled valuation experiment → Ch21。
- `LINK` failure mining → Ch9 / Ch17。
- `ADD FIGURE` F10。

**Exit condition：** 本章回答“为什么做这个、做多少、什么时候停”。

---

## 第 19 章 — Governance / Lineage / Reproducibility

**定位：全系统数据身份、版本与审计的 canonical chapter。**

- `KEEP` immutable raw / canonical / derived layers。
- `KEEP` provenance / lineage DAG / dataset / schema / label versioning。
- `KEEP` Decision Freeze vs Label Correction。
- `KEEP` reproducibility manifest / snapshot / replay。
- `KEEP` train lineage / reverse impact / contamination registry。
- `KEEP` privacy / PII / access / consent / licensing / retention / deletion / audit。
- `KEEP` research-minimum vs production-grade governance distinction。
- `UNIFY` Ch6 label versioning / Ch12 trajectory lineage / Ch16 eval lineage 为局部视图。
- `ADD FIGURE` F11。

**Exit condition：** provenance / lineage / versioning 不再散落为多套定义。

---

## 第 20 章 — Quality / Filtering / Dedup / Mixture

**定位：Data Curation 的 canonical chapter。**

- `KEEP` multidimensional quality。
- `KEEP` validity / rule / model / human filtering。
- `KEEP` PASS / DROP / QUARANTINE / REVIEW / DOWNWEIGHT。
- `KEEP` exact / near / semantic / decision / family-level dedup。
- `KEEP` legitimate frequency vs redundant duplicate。
- `KEEP` mixture / sampling / token exposure / capability balance / effective sample size。
- `KEEP` filter-induced distribution shift / mixture interaction。
- `TRIM` Data ROI 解释，`LINK → Ch18`。
- `LINK` causal mixture / threshold proof → Ch21。
- `UNIFY` contamination terminology with Ch16 / Ch19。

**Exit condition：** 本章回答“哪些留下、多少权重、怎么混”。

---

## 第 21 章 — Data Experiments

**定位：Data Intervention 的因果验证章。**

- `KEEP` Add / Remove / Replace / Reweight。
- `KEEP` matched-budget / small pilot / scaling curve。
- `KEEP` quantity vs quality / threshold / hard-data / curriculum experiment。
- `KEEP` interaction / supervision-form comparison / transfer。
- `KEEP` proxy vs downstream / seed variance / exploratory vs confirmatory。
- `KEEP` mining policy experiment / experiment registry / SCALE-MAINTAIN-REVISE-STOP-RETIRE。
- `LINK` general benchmark statistics → Ch16。
- `LINK` Portfolio / ROI decision → Ch18。
- `UNIFY` matched-budget terminology with Ch16。

**Exit condition：** 本章只回答“这批数据让模型变好了吗？”

---

## 第 22 章 — Data Production System

**定位：Experience Manufacturing Infrastructure。**

- `KEEP` Production Contract / Job / Queue / Worker / Artifact / Metadata。
- `KEEP` state machine / retry / idempotency / DLQ / checkpoint。
- `KEEP` System Retry ≠ Agent Recovery。
- `KEEP` raw → normalized → evaluated → dataset view。
- `KEEP` quality gate / routing / build recipe / split / cost accounting / backpressure。
- `KEEP` environment pool / infrastructure vs model vs eval failure。
- `KEEP` canary / shadow / experiment handoff。
- `LINK` governance details → Ch19。
- `LINK` Monitoring → Ch23。
- `ADD FIGURE` F12。

**Exit condition：** 本章负责“稳定生产”，不负责组织层决策。

---

## 第 23 章 — Monitoring / Online Feedback / Drift

**定位：上线后的 sensing system。**

- `KEEP` Data / Concept / Failure / Capability / Judge / Tool-Harness-Environment drift。
- `KEEP` Stable Ruler + Moving Frontier。
- `KEEP` Judge Anchor / fixed-mix metrics / online feedback / delayed feedback。
- `KEEP` Shadow / Canary / rollback / coverage / trigger drift。
- `KEEP` drift response playbook。
- `TRIM` Data Flywheel 的通用解释，`LINK → Ch17`。
- `TRIM` benchmark design，`LINK → Ch16`。
- `ADD FIGURE` F13。

**Exit condition：** 本章回答“什么时候说明世界、模型或测量系统已经变了”。

---

## 第 24 章 — End-to-End Operating Model

**定位：组织级 operating system。**

- `KEEP` Data Problem Gate。
- `KEEP` role map / RACI / failure routing / decision rights。
- `KEEP` Research Mode vs Production Mode。
- `KEEP` Research-to-Production Gate / handoff contract / project lifecycle。
- `KEEP` quarterly capability roadmap / incident response。
- `TRIM` 各子领域方法细节，只保留 routing 与 ownership。
- `UNIFY` Owner / Responsible / Accountable 等组织语言。
- `ADD FIGURE` F14（Operating side）。

**Exit condition：** 本章回答“团队怎么跑”，而不是“个人如何快速解决问题”。

---

## 第 25 章 — Capability Map / Practical Methodology

**定位：个人 practitioner operating system / 全书收束。**

- `KEEP` 八域 Capability Map。
- `KEEP` 全链路总图。
- `KEEP` Problem Routing Tree / Data Intervention Tree。
- `KEEP` End-to-end canonical case。
- `KEEP` 30-minute diagnosis / project checklist / interview framework。
- `KEEP` role perspective / seniority difference / six root questions。
- `TRIM` 任何重新完整解释前 24 章定义的段落。
- `LINK` 每个概念直接到 canonical chapter。
- `ADD INDEX` 章节 / 岗位 / 问题导航入口。
- `ADD FIGURE` F14（Capability side）。

**Exit condition：** 本章只负责“调用整套体系”，不再产生新的知识分支。

---

# 8. 总入口 `LLM_Agent_Data_Knowledge_System.md` 施工图

这是后续 **P0 第一修改对象**。

## 必做

- `UNIFY` 当前版本与完成状态。
- `REMOVE / REPLACE` 旧“计划章节”编号与已经失效的旧目录。
- `ADD INDEX` 真实 1–25 章目录。
- `ADD INDEX` 7-Part 结构。
- `ADD INDEX` 角色阅读路线。
- `ADD INDEX` 问题阅读路线。
- `ADD INDEX` Canonical Case 导航。
- `ADD INDEX` Glossary / Concept Index / Blueprint 链接。

## 建议最终 Landing Page 结构

```text
1. 这套知识库解决什么问题
2. 全书总图
3. 7-Part 目录
4. 1–25 章导航
5. 按岗位阅读
6. 按问题阅读
7. Canonical Cases
8. Core Principles
9. Glossary / Concept Index
10. How to Use This Knowledge System
```

主文件未来不再承担第 1–3 章正文。

---

# 9. 推荐阅读路线

## Data Research / Post-training

```text
1 → 2 → 3 → 6 → 7 → 9 → 15 → 16 → 18 → 20 → 21 → 25
```

## Agent Data

```text
1 → 5 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → 22 → 23 → 25
```

## Evaluation / Benchmark

```text
1 → 4 → 8 → 9 → 13 → 14 → 15 → 16 → 21 → 23 → 25
```

## Data Platform / DataOps

```text
1 → 12 → 19 → 20 → 22 → 23 → 24
```

## 面试快速路线

```text
1 → 3 → 5 → 14 → 15 → 16 → 18 → 21 → 25
```

---

# 10. Cross-reference Style 规则

后续避免：

```text
“前面已经讲过……”
```

但不给定位。

统一采用：

```text
> 关于 X 的完整定义见 [第 N 章 ...](...#anchor)。本节只讨论 X 在当前问题中的应用。
```

或正文简写：

```text
这里沿用第 4 章的定义：Risk ≠ Correctness ≠ Recoverability。
```

原则：

```text
Canonical Chapter = definition
Dependent Chapter = application
```

---

# 11. 重复处理优先级

## P0：必须处理

```text
总入口旧目录 / 旧编号
1–3 与 4–25 文件结构不一致
核心术语缺 glossary
```

## P1：明显影响阅读

```text
Ch5 ↔ Ch13/14
Ch6 ↔ Ch19
Ch7/8/9 ↔ Ch18/20/21
Ch16 ↔ Ch21
Ch17 ↔ Ch23
```

## P2：可以保留但改成交叉引用

```text
rescue / harmful
contamination
lineage
mixture
cost-aware evaluation
```

---

# 12. 事实 / 引文审计清单（最后阶段）

正文结构稳定后，再做，不应抢在编辑之前。

需要核验：

```text
正式论文题名 / 副标题
论文作者 / 年份 / arXiv ID
benchmark 名称
具体实验数字
统计定义
公式符号
业内术语是否有非标准用法
```

特别注意：

```text
More Thinking Is Not Always Better 的正式题名
RoTFuse / K17 中哪些是阶段性结果、哪些是正式结论
```

研究实例统一加 Scope / Status 标记：

```text
Research Example
Current Experimental Evidence
Not a Universal Claim
```

---

# 13. 推荐实际施工顺序

```text
Phase 1 — Information Architecture
1. 重建总入口
2. 拆分 01–03
3. 建 7-Part 导航

Phase 2 — Canonical Language
4. 建 Glossary / Notation
5. 建 Concept Ownership Map
6. 统一核心术语

Phase 3 — Cross-chapter Editing
7. Ch4 / 10 / 11 / 13 / 14 / 15 / 16 / 19 先稳定 canonical definitions
8. 再处理依赖章节的 TRIM / LINK

Phase 4 — Case System
9. 建 Casebook
10. 将 C1–C5 接入各章

Phase 5 — Visual System
11. 统一 14 张 Master Figures
12. 删除 / 合并重复局部图

Phase 6 — Navigation & Retrieval
13. Concept Index
14. Role Index
15. Problem Index
16. Interview Index
17. Checklist Index

Phase 7 — Verification
18. 引文 / 数字 / 论文 / 公式审计
19. broken link / anchor audit
20. 最终全书连读

Phase 8 — Derived Editions
21. Interview Quick Reference
22. Project Checklist Edition
23. Learning Path Edition
```

---

# 14. 完成标准

当以下问题都可以快速回答时，全书精修完成：

```text
一个术语在哪里定义？
一个概念为什么不会在五章里被重复解释？
一个 failure 应该读哪几章？
一个 Agent data 项目从 Task 到 Monitoring 怎么走？
一个 Data Research 面试应该优先读哪几章？
一个案例怎样从 Task → Trajectory → Credit → Failure → Eval → Data → Production？
一个历史结论对应哪套数据、哪版 Judge、哪套协议？
一章删掉后是否会出现知识断层？
一张图是否承担了真正的结构压缩作用？
```

最终目标不是让知识库“更长”，而是让它满足：

> **每个概念有唯一归属，每个章节有清楚职责，每个案例能够贯穿多层，每个结论能够找到证据，每种读者都能找到自己的路径。**

---

# 15. 编辑总原则

最后固定五条：

1. **不为了简洁牺牲关键区分。**
2. **不为了完整在每章重复同一套定义。**
3. **不把研究实例写成未经验证的普遍规律。**
4. **不把 Agent / Data / Eval / Infra failure 混成一个模型问题。**
5. **不继续扩章节；后续新增内容优先进入案例、索引、图示、术语或已有章节。**

一句话总结：

> **从现在开始，目标不是继续“写知识”，而是把已有知识编辑成一套真正可以被调用的系统。**
