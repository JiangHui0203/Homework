# Master Figures

本目录保存 `LLM / Agent Data Knowledge System` 的全书级 Master Figures。

当前原则：

```text
Mermaid Master Figure
= semantic source of truth

D1 Publication / D2 Presentation / D3 Quick-reference
= presentation derivatives
```

当前状态：

```text
F1–F14 semantic Master Figures
✓ complete

Level A
F1 / F4 / F6 / F8 / F9 / F14
→ D1 / D2 / D3 complete

Level B
F2 / F3 / F5 / F7 / F10 / F11 / F12 / F13
→ semantic / production-refined Master Figure complete
```

Level B derivative 不为了“数量对齐”机械生成；有真实出版 / 演示 / quick-reference 需求时再派生。

视觉体系入口：

- [`Master Figure System`](../00_Master_Figure_System.md)
- [`Figure Design Contract`](../00_Figure_Design_Contract.md)
- [`Figure Presentation Kit`](../00_Figure_Presentation_Kit.md)
- [`Visual Release Manifest`](../00_Visual_Release_Manifest.md)
- [`Visual Derivatives`](../visual_derivatives/README.md)
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

如果要把这六张直接用于面试、组会或答辩：

- [`Figure Presentation Kit`](../00_Figure_Presentation_Kit.md) → 选图、30s / 90s talk track、误讲点
- [`D2 Presentation Storyboards`](../visual_derivatives/slides/README.md) → 真正 16:9 progressive reveal implementation
- [`D3 Quick-reference Cards`](../visual_derivatives/quick_reference/Level_A_Quick_Reference_Cards.md) → 快速复习

如果用于书稿 / PDF：

- [`D1 Publication SVG`](../visual_derivatives/publication/)

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

每张成品化 Master Figure 现在都能独立回答：

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

Caption
→ 单独引用时怎样准确描述？
```

因此 Figure file 不是“只有 Mermaid 的图片仓库”，而是：

> **一张 canonical visual + 最小必要读图说明 + 可直接用于讲述的稳定语义。**

---

# Figure Rule

```text
Master Figure
= canonical relationship model

Chapter-local Figure
= local lens / local pipeline
```

当前状态：

```text
Semantic Registry
✓ complete

Canonical Ownership
✓ complete

Duplicate Visual Cleanup
✓ complete

Figure Design Contract
✓ complete

Level A Production Refinement
✓ complete

Level B Production Refinement
✓ complete

Level A D1 Publication
✓ complete

Level A D2 16:9 Storyboard
✓ complete

Level A D3 Quick-reference
✓ complete
```

后续视觉工作默认是：

```text
source freshness maintenance
semantic acceptance
按真实需求派生 Level B
```

而不是再次修改 canonical relation，也不是为了“14 张都必须有三套 derivative”制造无需求资产。

---

# Derivative Responsibilities

同一个 Mermaid semantic source 可以派生：

```text
D1 Book / PDF Figure
→ static semantic hierarchy

D2 Slides / Progressive Reveal
→ temporal information order

D3 Interview / Quick Reference
→ minimal recall surface
```

`Figure Presentation Kit` 负责：

```text
讲哪张
怎么讲
讲多深
哪些地方容易讲错
```

真正的 slide frame / reveal 顺序以 D2 storyboard 为准。

如果 presentation redraw 需要改变概念关系，必须先回写 Master Figure source。
