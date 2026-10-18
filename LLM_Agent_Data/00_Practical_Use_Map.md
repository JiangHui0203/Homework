# LLM / Agent Data Practical Use Map

> 状态：`Stable Mother Edition V3.x / Practical Entry / Multi-scenario-tested`
>
> 目的：给已经稳定的知识体系提供一个**行动入口**。不再解释概念，只回答：
>
> **“我现在要做什么，第一步该打开哪个资产？”**

---

# 0. 一张最短地图

```text
我想快速建立框架
→ Condensed Guide

我准备面试 / 答辩
→ Interview Pack

我今天要启动一个真实项目
→ Project Starter Pack

我不知道这个项目应该从 A1 / A5 / A10 / A11 哪个入口进
→ Project Starter Pack / Entry Router

我想看 Scenario Pack 在真实追问 / protocol 下哪里会坏
→ Stress Test Round 1 / Round 2 / Promotion Test

我想看只在特定项目启用的 contract
→ Scenario Pack Candidate Extensions

我想把图讲清楚
→ Figure Presentation Kit

我遇到一个真实症状
→ Problem Index

我需要按顺序推进问题
→ Practical Playbooks

我需要填写可审计项目工件
→ Practical Artifact Kit

我想看一个完整项目怎么走
→ Practical Case Studies

我怕项目某阶段漏项
→ Checklist Index

我想查一个术语归谁定义
→ Concept Index / Glossary

我想查“这个方法 / 结论外部来源是什么”
→ Canonical References / Source Policy

我想系统学习
→ 25-Chapter Mother Edition
```

Scenario validation：

- [`Stress Test — Round 1`](./00_Scenario_Pack_Stress_Test.md)
- [`Stress Test — Round 2`](./00_Scenario_Pack_Stress_Test_Round_2.md)
- [`Promotion Test`](./00_Scenario_Pack_Promotion_Test.md)
- [`Candidate Extensions`](./00_Scenario_Pack_Candidate_Extensions.md)

---

# 1. 我只有 30–90 分钟

打开：

- [`Condensed Guide`](./00_Condensed_Guide.md)

配合 Level A Figures：

```text
F1
→ F4
→ F6
→ F8
→ F9
→ F14
```

如果要准备口头表达：

- [`Figure Presentation Kit`](./00_Figure_Presentation_Kit.md)

如果明确是在准备面试 / 答辩：

- [`Interview Pack`](./00_Interview_Pack.md)

---

# 2. 我刚拿到一个 bad case / 新研究问题 / 线上告警 / 数据资产

第一入口统一看：

- [`Project Starter Pack`](./00_Project_Starter_Pack.md)

先选 Entry，而不是先填表：

```text
Failure-led
→ A1 / A2 / A3 / A4

Monitoring-led Incident
→ A10

Hypothesis-led
→ A1 / A2-S / A7

Evaluation-led
→ A5

Asset-led / Curation-led
→ A11 / source lineage
```

固定原则：

```text
Artifact Chain
≠ 所有项目都必须 A1 → A10 顺序填写
```

如果已经有明确 symptom：

- [`Problem Index`](./00_Problem_Index.md)
- [`Practical Playbooks`](./00_Practical_Playbooks.md) → P1 / P7

需要落盘：

- [`Practical Artifact Kit`](./00_Practical_Artifact_Kit.md)

Failure-led 最常见的最小证据链：

```text
A1 Problem Intake
A2 Task / Case / Decision-state Contract
A3 Trajectory / Evidence Bundle
A4 Failure / Mechanism Record
A5 Evaluator Contract
```

如果确认是 Data Gap，再继续：

```text
A6 Data Intervention
A7 Experiment Card
A8 Decision Memo
```

如果是 inference-time / tool / harness / evaluator intervention：

```text
不要硬填 A6
→ 保存对应 Method / System Contract
→ 直接进入 A7
```

selective / routing 项目在 A7 必须额外保留：

```text
Population Ledger
Information Boundary
Cost Ledger
```

按需 extension：

```text
Production Incident
→ A10-I

Evaluator / Rubric / Guideline 换版
→ A5-M Measurement Bridge

Large-scale Curation
→ A6-C Curation Contract
```

见 [`Candidate Extensions`](./00_Scenario_Pack_Candidate_Extensions.md)。

---

# 3. 我想看“真实项目到底怎么走完”

打开：

- [`Practical Case Studies`](./case_studies/README.md)

当前四篇分别解决：

```text
C1
External Agent Decision
→ failure 怎样进入完整 Learning Loop

C3
Permission / Runtime / Side Effect
→ Model 到底是不是正确的 Failure Owner

C4
Reasoning Intervention
→ Oracle Headroom 是否真的转成 online value

C5
Executable Task / Verifier
→ 什么 Evidence 足以叫“正确”
```

如果想看“模板实际填成什么样”：

- [`C1 Filled Artifact Pack`](./case_studies/C1_Artifact_Pack.md)

---

# 4. 我正在做 Agent Data / Trajectory 项目

推荐顺序：

```text
Ch1
→ Ch5
→ Ch10
→ Ch11
→ Ch12
→ Ch13
→ Ch14
→ Ch15
→ Ch16
→ Ch17
→ Ch21
→ Ch22
→ Ch23
```

快速图链：

```text
F4
→ F5
→ F6
→ F7
→ F8
→ F9
→ F12
→ F13
```

实战案例：

```text
C1
→ 普通 state-grounded Agent decision

C3
→ permission / side effect / Harness
```

执行资产：

```text
Project Starter Pack
→ Playbook P1 / P2 / P7
→ Core Artifact + conditional extension
```

如果输入是：

```text
“一大批已有 trajectory，要怎么变成训练资产？”
```

优先走：

```text
A11 source lineage
→ A6-C curation extension
→ dataset view / exposure
→ A7 downstream validation
```

外部方法锚点：

```text
R06 Toolformer
R07 ReAct
R10 AgentBench
R11 WebArena
```

---

# 5. 我正在做 Reasoning / Test-time / Selector

推荐顺序：

```text
Ch4
→ Ch8
→ Ch9
→ Ch13
→ Ch16
→ Ch18
→ Ch21
→ Ch23
```

核心图：

```text
F3
→ F8
→ F10
→ F13
```

实战：

- [`C4 Reasoning Intervention Walkthrough`](./case_studies/C4_Reasoning_Intervention_Walkthrough.md)

第一组必须回答的问题：

```text
Risk?
Recoverable?
Repairable?
Selectable?
```

第二组：

```text
Trigger Coverage?
Oracle Headroom?
Selector Rescue?
Harmful?
Net?
Cost?
```

真正启动项目时：

```text
Project Starter Pack
→ Hypothesis-led Entry
→ A2-S exact decision-state contract
→ A7 Population / Information / Cost Ledger
```

固定边界：

```text
Full Population ≠ Triggered Cohort
Offline Label ≠ Online Feature
Same Task ≠ Same Decision State
```

外部 anchor 只负责相关公开方法背景；C4 的 `Risk / Recoverability / Selectability` operating decomposition 仍以本书 canonical definition 为准。

---

# 6. 我正在做 Eval / Judge / Verifier / Human Gold

推荐顺序：

```text
Ch6
→ Ch15
→ Ch16
→ Ch19
→ Ch21
→ Ch23
```

核心图：

```text
F7
→ F8
→ F11
→ F13
```

实战：

- [`C5 Executable Truth / Verifier Coverage Walkthrough`](./case_studies/C5_Executable_Truth_Verifier_Coverage_Walkthrough.md)

先问：

```text
Claim 是什么？
最直接 Evidence 是什么？
为什么这个 Evaluator 对这个 Claim 有效？
```

不要先问：

```text
“选哪个 Judge？”
```

如果：

```text
Judge / Verifier / Rubric / Guideline
vOld → vNew
```

优先加载：

```text
A5-M Measurement Bridge
```

先做：

```text
same anchor set
→ old evaluator
→ new evaluator
→ disagreement / FP / FN / decision flip
```

再决定历史曲线是否可比。

固定边界：

```text
Evaluator Upgrade
≠ Capability Improvement

Re-score
≠ Historical Decision Rewrite
```

外部锚点：

```text
R08 LLM-as-a-Judge
R09 HELM
R12 SWE-bench
R14 Benchmark Contamination
R15 LiveBench
```

---

# 7. 我正在做 Data Strategy / Curation / Experiment

推荐顺序：

```text
Ch17
→ Ch18
→ Ch19
→ Ch20
→ Ch21
```

核心图：

```text
F9
→ F10
→ F11
```

一般 Data Intervention：

```text
A6 Data Intervention Card
→ A7 Experiment Card
→ A8 Decision Memo
```

如果是已有大批 source assets 的 curation：

```text
A11 Source Lineage
→ A6-C Curation Contract
→ Rebuildable Dataset View
→ Yield Funnel
→ Exposure
→ A7 matched-budget downstream validation
```

必须分开：

```text
Data Quality
≠ Data Value

Data Strategy
≠ Curation

Curation
≠ Experiment

Raw Sample Count
≠ High-value Yield

Dataset Size
≠ Training Exposure

Intrinsic Data Quality
≠ Downstream Learning Value
```

Synthetic production 优先组合已有 contract：

```text
A6 + A9 + A11 + A7
```

不要因为领域重要就新造一个 `A12 Synthetic Card`。

---

# 8. 我正在做生产 / DataOps / Monitoring

推荐顺序：

```text
Ch19
→ Ch22
→ Ch23
→ Ch24
```

核心图：

```text
F11
→ F12
→ F13
→ F14
```

执行资产：

```text
A9 Production Handoff
A10 Monitoring Incident
A11 Minimal Lineage Manifest
```

如果现在面对的是线上 incident：

```text
A10 first
→ Last-known-good
→ Change Ledger
→ Raw / Slice / Fixed-mix
→ Frozen Core / Fresh Failure
→ Containment / Rollback
→ Attribution
```

按需使用：

```text
A10-I Production Incident Extension
```

核心边界：

```text
Research Success
≠ Production Readiness

Infrastructure Retry
≠ Agent Recovery

Monitoring Alert
≠ Model Regression

Rollback
≠ Root-cause Proof
```

外部治理锚点：

```text
R13 Datasheets for Datasets
R14 Benchmark Contamination
R15 LiveBench
```

---

# 9. 我要准备面试 / 答辩 / 分享

第一入口：

- [`Interview Pack`](./00_Interview_Pack.md)

它负责把：

```text
Condensed Guide
Quick-reference
Presentation Track
Interview Index
C1 / C3 / C4 / C5
```

装配成 30 分钟 / 90 分钟准备路径、题型路由和追问树。

压力测试后尤其记住：

```text
Direct Answer First
Framework Second

Alternative Hypothesis
≠ Confirmed Root Cause

Public Literature
≠ My Project
≠ Teaching Case
≠ Hypothetical Design

Quantitative Claim
→ denominator + protocol + budget + claim scope
```

完整 finding：

- [`Scenario Pack Stress Test — Round 1`](./00_Scenario_Pack_Stress_Test.md)

推荐 case：

```text
Agent Data 岗
→ C1 / C3

Reasoning / Test-time
→ C4

Eval / Verifier / Code Agent
→ C5
```

---

# 10. 我想查文献，但不想陷进 Related Work 海洋

先打开：

- [`Canonical References`](./00_Canonical_References.md)

它只维护少量稳定 anchor，并给出：

```text
Reference ID
Role
主要章节
能支撑什么
不能支撑什么
```

如果要判断：

```text
外部论文
内部 Research Example
Teaching Case
工程约定
```

到底该怎么区分，则看：

- [`Reference & Source Policy`](./00_Reference_Source_Policy.md)

核心纪律：

```text
External paper
≠ Internal result evidence

Similar topic
≠ Valid source anchor

Citation count
≠ Evidence quality
```

---

# 11. 我不知道自己到底缺哪一块

先跑 30-minute diagnosis：

```text
0–5
先判 Entry：
Failure / Monitoring / Hypothesis / Evaluation / Asset?

5–10
Goal / Population / Source / Metric / Claim

10–15
Task / State / Trace / Environment / Evidence
或 Last-known-good / Measurement Bridge / Source Lineage

15–20
Failure / Root Cause / Owner
或 Hypothesis / Mechanism / Counterfactual
或 Curation / Measurement Gap

20–25
Minimum Controlled Change + Frozen Eval

25–30
Scale / Revise / Stop / Rollback
```

然后按结果分流：

```text
概念不清
→ Glossary / Concept Index

不知道为什么失败
→ C1 / C3 + F6

不知道怎么评
→ C5 + F7 / F8

不知道 evaluator 换版后历史分数还能不能比
→ A5-M Measurement Bridge

不知道 selective method 的 denominator / information boundary
→ Project Starter Pack + Artifact Kit A2-S / A7

不知道 50 万条 trajectory 怎么整理
→ A11 + A6-C + Ch20

不知道数据值不值得做
→ F10 + Ch18 / Ch21

不知道怎么规模化
→ F12 + Ch22

不知道线上为什么变了
→ A10 / A10-I + F13 + Ch23

不知道外部出处
→ Canonical References
```

---

# 12. Practical Layer 的最终结构

```text
Mother Edition
= Why / What / Canonical Definition

Condensed Guide
= Fast Mental Model

Master Figures
= Visual System Model

Presentation Kit
= How to Explain

Interview Pack
= How to Prepare / Answer / Handle Follow-ups

Project Starter Pack
= Entry Router + Day 0 → First Week

Scenario Stress Tests
= Where Scenario Packs break under real pressure

Promotion Test
= Which extensions deserve Mother status

Candidate Extensions
= Optional contracts for specific project types

Problem Index
= Where to Diagnose

Playbooks
= How to Act

Artifact Kit
= What to Produce

Case Studies
= How the Pieces Connect in Practice

Checklist Index
= What Not to Miss

Reference Layer
= What External Evidence Anchors the Public Methods
```

最终原则：

> **不要为了“资料齐全”反复复制同一知识。Core 负责跨项目稳定骨架，Extension 只在相关场景加载，Stress Test 负责不断证明两者的边界。**
