# LLM / Agent Data Knowledge System：Master Figure System

> 状态：**Complete / Canonical Visual System**
>
> 目的：为 0–25 章建立一套稳定、可复用、可版本化的 Master Figure。图的任务不是装饰，而是压缩跨章节关系、固定对象边界、帮助读者建立全书级 mental model。
>
> 原则：**一张图只承担一个主要认知任务；canonical concept 只在对应 master figure 中完整展开，其他章节优先引用而不是重复重画。**

---

# 0. Visual Grammar

统一语义：

```text
实线箭头  → 实际执行 / 因果 / 数据流
虚线箭头  → 评价 / 反馈 / 派生关系
菱形       → Decision Gate
圆角节点   → Object / State / Artifact
方框       → System / Process
子图       → Layer / Owner / Phase
```

Mermaid 尽量使用默认主题，保证 GitHub Light / Dark Mode 都可读。

图内文字规则：

1. 节点只放短语，不放完整段落。
2. 中文负责解释，英文保留 canonical term。
3. 同一概念全书统一写法，例如 `World State`、`Agent-visible State`、`Outcome`、`Reward`、`Credit`。
4. Case variant 直接使用 `C1-VB / C4-SC` 等稳定 ID。
5. 图下正文解释“为什么”，图本身展示“关系是什么”。

---

# 1. Master Figure Registry

| ID | Figure | 主要认知任务 | Canonical Owner | 主案例 |
|---|---|---|---|---|
| [F1](./figures/F1_Learning_System_Overview.md) | Learning System Overview | 整本书到底在描述什么系统 | Ch0 / Ch25 | C1 + C4 |
| [F2](./figures/F2_Data_Object_and_Learning_Signal_Evolution.md) | Data Object & Learning Signal Evolution | Example 如何扩展成 Experience | Ch1–3 | C1 |
| [F3](./figures/F3_Reasoning_State_Decision_Stack.md) | Reasoning State Decision Stack | Correctness / Risk / Recoverability / Repairability / Selectability | Ch4 | C4-SC |
| [F4](./figures/F4_Agent_Task_Environment_Trajectory.md) | Agent Task–Environment–Trajectory | Task、Tool、Harness、Environment、Trajectory 的关系 | Ch10–12 | C1-VB |
| [F5](./figures/F5_Trajectory_Anatomy.md) | Trajectory Anatomy | 一条 trajectory 内部应该记录什么 | Ch12 | C1-F1 |
| [F6](./figures/F6_Credit_to_Failure_Causal_Map.md) | Credit → Failure Causal Map | 从 Outcome 到 Root Cause 的完整因果链 | Ch13–14 | C1-F1 + C3-F5 |
| [F7](./figures/F7_Evidence_Verifier_Grader_Judge.md) | Evidence → Evaluator Stack | Evidence / Verifier / Grader / Judge | Ch15 | C1 + C5-F3 |
| [F8](./figures/F8_Benchmark_Evaluation_Protocol.md) | Benchmark / Evaluation Protocol | 怎么公平比较模型 / intervention | Ch16 | C1 family |
| [F9](./figures/F9_Data_Flywheel.md) | Data Flywheel | Failure 如何重新变成 Learning Signal | Ch17 | C1 |
| [F10](./figures/F10_Data_Strategy_Portfolio_ROI.md) | Data Strategy / Portfolio / ROI | 资源到底投哪里 | Ch18 | multi-case portfolio |
| [F11](./figures/F11_Governance_Lineage_DAG.md) | Governance / Lineage DAG | 一个结论怎样追溯到原始数据 | Ch19 | C1 assets |
| [F12](./figures/F12_Data_Production_System.md) | Data Production System | 高价值数据怎样被稳定制造 | Ch22 | C1 recovery family |
| [F13](./figures/F13_Monitoring_Drift_Diagnostic_Tree.md) | Monitoring / Drift Diagnostic Tree | 指标变了以后先查什么 | Ch23 | C1 / C3 |
| [F14](./figures/F14_Operating_Model_and_Capability_Map.md) | Operating Model + Capability Map | 团队和个人怎样调用全系统 | Ch24–25 | all cases |

---

# 2. Figure Levels

## Level A — Book-level

用于形成整本书的 mental model：

```text
F1  Learning System
F4  Agent Task–Environment–Trajectory
F6  Credit → Failure
F8  Evaluation Protocol
F9  Data Flywheel
F14 Operating Model + Capability Map
```

## Level B — Part-level

负责压缩某一个 Part 的核心关系：

```text
F2  Learning Signals
F3  Reasoning State
F5  Trajectory Anatomy
F7  Evaluator Stack
F10 Data Strategy
F11 Governance / Lineage
F12 Data Production
F13 Monitoring / Drift
```

## Level C — Chapter-local

局部 pipeline / formula / example 图仍可保留，但不能重新定义 Level A/B 已固定的关系。

---

# 3. Chapter Integration Rule

章节引用 Master Figure 时统一采用：

```text
> Master Figure：F6 — Credit → Failure Causal Map。
> 本章只展开其中的 Credit / Failure 层。
```

如果只使用图的一部分，可写：

```text
F6 Lens: First Harmful Action → Root Cause
```

规则：

```text
Master Figure = stable system model
Chapter = analytical lens
```

---

# 4. Case Integration Rule

图中使用 case 时：

```text
C1-VB = shipped / no refund allowed
C1-F1 = shipped observed but refund executed
C3-F5 = tool truth failure / harness observation success
C4-SC = same authoritative prefix sibling set
C5-F2 = public tests pass / hidden test fail
```

Case ID 不得为了图示简洁改变语义。

---

# 5. 14 张图形成的完整视觉链

```text
F1  Learning System
↓
F2  Data Object / Learning Signal
↓
F3  Reasoning Decision Stack

F4  Agent World
↓
F5  Trajectory Anatomy
↓
F6  Credit → Failure

F7  Evidence / Evaluator
↓
F8  Evaluation Protocol

F9  Data Flywheel
↓
F10 Data Strategy
↓
F11 Governance / Lineage

F12 Data Production
↓
F13 Monitoring / Drift
↓
F14 Operating Model / Capability Map
```

它们对应整本书最重要的六个问题：

```text
What is the learning system?
What experience exists?
What happened in the agent world?
How do we know it is good or bad?
Which experience is worth learning?
How do we keep the system operating and learning?
```

---

# 6. 下一步：Figure Integration Audit

Master Figures 已全部完成，下一阶段不是继续画图，而是审计旧章节图：

```text
KEEP
→ 该图只讲本章局部问题，保留

REPLACE WITH MASTER
→ 与 F1–F14 重复，改成链接 master figure

KEEP AS LOCAL LENS
→ 保留，但明确它只是某张 master figure 的局部放大
```

之后才考虑：

```text
publication SVG redraw
```

避免同时维护两套语义不同的图。

---

# 7. 完成标准

现在应能做到：

```text
读 F1 → 知道全书讲什么
读 F2/F3 → 知道 learning signal 与 reasoning-state 区分
读 F4/F5/F6 → 知道 Agent 世界与 failure 因果链
读 F7/F8 → 知道证据与科学比较
读 F9/F10/F11 → 知道数据闭环、投资和治理
读 F12/F13/F14 → 知道生产、监控、组织和个人方法
```

最终目标：

> **读者即使暂时不读 25 章全文，也能通过 14 张 Master Figures 建立正确的整体结构；再进入章节时，只是在放大某个局部，而不是重新学习一套世界。**
