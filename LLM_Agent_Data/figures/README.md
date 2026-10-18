# Master Figures

本目录保存 `LLM / Agent Data Knowledge System` 的全书级 Master Figures。

当前原则：

```text
Mermaid Master Figure
= semantic source of truth

SVG / PNG / PPT / PDF redraw
= presentation derivative
```

目标：

```text
可读
可 diff
可版本化
GitHub 直接渲染
可单独截图讲解
后续可统一重绘成出版级 SVG
```

视觉体系入口：

- [`Master Figure System`](../00_Master_Figure_System.md)
- [`Figure Design Contract`](../00_Figure_Design_Contract.md)
- [`Figure Integration Audit`](../00_Figure_Integration_Audit.md)

---

# Figure Index

## Learning Signals

- [F1 — Learning System Overview](./F1_Learning_System_Overview.md)
- [F2 — Data Object & Learning Signal Evolution](./F2_Data_Object_and_Learning_Signal_Evolution.md)
- [F3 — Reasoning State Decision Stack](./F3_Reasoning_State_Decision_Stack.md)

## Agent World & Diagnosis

- [F4 — Agent Task–Environment–Trajectory](./F4_Agent_Task_Environment_Trajectory.md)
- [F5 — Trajectory Anatomy](./F5_Trajectory_Anatomy.md)
- [F6 — Credit → Failure Causal Map](./F6_Credit_to_Failure_Causal_Map.md)

## Measurement

- [F7 — Evidence → Verifier → Grader → Judge](./F7_Evidence_Verifier_Grader_Judge.md)
- [F8 — Benchmark / Evaluation Protocol](./F8_Benchmark_Evaluation_Protocol.md)

## Data Optimization & Lifecycle

- [F9 — Data Flywheel](./F9_Data_Flywheel.md)
- [F10 — Data Strategy / Portfolio / ROI](./F10_Data_Strategy_Portfolio_ROI.md)
- [F11 — Governance / Lineage DAG](./F11_Governance_Lineage_DAG.md)

## Data Operations

- [F12 — Data Production System](./F12_Data_Production_System.md)
- [F13 — Monitoring / Drift Diagnostic Tree](./F13_Monitoring_Drift_Diagnostic_Tree.md)
- [F14 — Operating Model + Capability Map](./F14_Operating_Model_and_Capability_Map.md)

---

# 两条推荐阅读路径

## 1. 只想快速建立全书 mental model

先读 Level A：

```text
F1
→ F4
→ F6
→ F8
→ F9
→ F14
```

它对应：

```text
Learning System
→ Agent World
→ Credit / Failure
→ Evaluation
→ Continuous Learning
→ Operating Model
```

## 2. 想把每一层补完整

在 Level A 之间插入对应 Level B：

```text
F1
→ F2 → F3
→ F4 → F5 → F6
→ F7 → F8
→ F9 → F10 → F11
→ F12 → F13 → F14
```

---

# Figure Reading Contract

每张成品化 Master Figure 应能独立回答：

```text
Figure Question
→ 它到底解决什么问题？

Read the Spine
→ 第一眼先看哪条主链？

Critical Boundaries
→ 哪几个概念最容易混？

Case Lens
→ 真实 case 怎样穿过这张图？

Cross-links
→ 继续读哪一章 / 哪张图？
```

因此 Figure file 不是“只有 Mermaid 的图片仓库”，而是：

> **一张 canonical visual + 最小必要读图说明。**

---

# Figure Rule

```text
Master Figure
= canonical relationship model

Chapter-local Figure
= local lens / local pipeline
```

视觉真源已经完成去重；当前进入 production refinement：

```text
统一 metadata
统一读图顺序
统一 critical boundaries
统一 case 标记
统一 caption readiness
```

而不是重新设计知识结构。

---

# Future Derivatives

同一个 Mermaid semantic source 未来可以派生：

```text
Book / PDF Figure
Slides / Progressive Reveal
Interview Quick Reference
Social / Share Card
```

如果 presentation redraw 需要改变概念关系，必须先回写 Master Figure source。
