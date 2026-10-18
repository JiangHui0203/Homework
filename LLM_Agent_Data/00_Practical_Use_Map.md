# LLM / Agent Data Practical Use Map

> 状态：`Stable Mother Edition V3.x / Practical Entry / Scenario-tested`
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

我想看这两套 Pack 在真实追问 / protocol 下哪里会坏
→ Scenario Pack Stress Test

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

# 2. 我刚拿到一个线上 bad case / 新项目

如果是“今天刚开始，先把顺序走对”：

- [`Project Starter Pack`](./00_Project_Starter_Pack.md)

如果已经有明确 symptom，第一步：

- [`Problem Index`](./00_Problem_Index.md)

然后：

- [`Practical Playbooks`](./00_Practical_Playbooks.md) → P1 / P7

需要落盘：

- [`Practical Artifact Kit`](./00_Practical_Artifact_Kit.md)

最少产出：

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
→ Artifact A1–A10
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

# 6. 我正在做 Eval / Judge / Verifier

推荐顺序：

```text
Ch15
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

执行资产：

```text
A6 Data Intervention Card
A7 Experiment Card
A8 Decision Memo
```

必须分开：

```text
Data Quality
≠ Data Value

Data Strategy
≠ Curation

Curation
≠ Experiment
```

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

核心边界：

```text
Research Success
≠ Production Readiness

Infrastructure Retry
≠ Agent Recovery

Monitoring Alert
≠ Model Regression
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

- [`Scenario Pack Stress Test`](./00_Scenario_Pack_Stress_Test.md)

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
Goal / Population / Metric

5–10
Task / Case / Trace / Environment / Evidence

10–15
Failure / Root Cause / Owner
或 Hypothesis / Mechanism / Counterfactual

15–20
Intervention Gate

20–25
Minimum Intervention + Frozen Eval

25–30
Scale / Revise / Stop
```

然后按结果分流：

```text
概念不清
→ Glossary / Concept Index

不知道为什么失败
→ C1 / C3 + F6

不知道怎么评
→ C5 + F7 / F8

不知道 selective method 的 denominator / information boundary
→ Project Starter Pack + Artifact Kit A2-S / A7

不知道数据值不值得做
→ F10 + Ch18 / Ch21

不知道怎么规模化
→ F12 + Ch22

不知道线上为什么变了
→ F13 + Ch23

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
= How to Start Day 0 → First Week

Scenario Pack Stress Test
= Where Scenario Packs break under real pressure

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

> **不要为了“资料齐全”反复复制同一知识。每个 practical asset 都只解决一种调用问题；Scenario Pack 只负责装配，而 Stress Test 负责证明这些装配在真实追问和真实 protocol 下不会轻易散架。**
