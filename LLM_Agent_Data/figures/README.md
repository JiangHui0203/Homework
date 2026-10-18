# Master Figures

本目录保存 `LLM / Agent Data Knowledge System` 的全书级 Master Figures。

目标：

```text
可读
可 diff
可版本化
GitHub 直接渲染
后续可统一重绘成出版级 SVG
```

完整视觉规范见：[`00_Master_Figure_System.md`](../00_Master_Figure_System.md)。

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

# 推荐阅读

如果只想快速建立整本书的 mental model，先读 Level A：

```text
F1
→ F4
→ F6
→ F8
→ F9
→ F14
```

如果需要深入某个 Part，再补对应 Level B 图。

---

# Figure Rule

```text
Master Figure
= canonical relationship model

Chapter-local Figure
= local lens / local pipeline
```

后续旧图审计将使用：

```text
KEEP
REPLACE WITH MASTER
KEEP AS LOCAL LENS
```

避免同一概念长期存在多套互相漂移的视觉定义。
