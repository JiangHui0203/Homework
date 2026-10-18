# Visual Derivatives

本目录保存从 F1–F14 Mermaid semantic source 派生的 presentation assets。

规范：

- [`Publication Visual Derivative Spec`](../00_Publication_Visual_Derivative_Spec.md)
- [`Master Figure System`](../00_Master_Figure_System.md)
- [`Figure Design Contract`](../00_Figure_Design_Contract.md)

固定关系：

```text
../figures/F1...F14.md
= semantic source of truth

./publication/
= static book / PDF derivative

./slides/
= presentation / progressive reveal derivative

./quick_reference/
= interview / share-card derivative
```

任何 derivative 必须记录：

```text
figure_id
semantic_source
semantic_source_sha
export_type
export_version
```

如果 semantic relation 需要变化，先修改 Mermaid source，再重新导出 derivative。

---

# Publication — Level A

状态：**Complete v1**

| Figure | Publication SVG | Semantic Source |
|---|---|---|
| F1 | [Learning System Overview](./publication/F1_Learning_System_Overview.svg) | [`figures/F1`](../figures/F1_Learning_System_Overview.md) |
| F4 | [Agent Task–Environment–Trajectory](./publication/F4_Agent_Task_Environment_Trajectory.svg) | [`figures/F4`](../figures/F4_Agent_Task_Environment_Trajectory.md) |
| F6 | [Credit → Failure Causal Map](./publication/F6_Credit_to_Failure_Causal_Map.svg) | [`figures/F6`](../figures/F6_Credit_to_Failure_Causal_Map.md) |
| F8 | [Benchmark / Evaluation Protocol](./publication/F8_Benchmark_Evaluation_Protocol.svg) | [`figures/F8`](../figures/F8_Benchmark_Evaluation_Protocol.md) |
| F9 | [Data Flywheel](./publication/F9_Data_Flywheel.svg) | [`figures/F9`](../figures/F9_Data_Flywheel.md) |
| F14 | [Operating Model + Capability Map](./publication/F14_Operating_Model_and_Capability_Map.svg) | [`figures/F14`](../figures/F14_Operating_Model_and_Capability_Map.md) |

它们形成书级视觉链：

```text
F1
Learning System
↓
F4
Agent World
↓
F6
Credit / Failure
↓
F8
Evaluation Protocol
↓
F9
Continuous Learning
↓
F14
Operating Model
```

---

# Publication Design Rule

Level A v1 已验证三种不同结构可以稳定派生：

```text
Closed Loop
→ F1 / F9

Layered System
→ F4 / F14

Causal / Protocol Chain
→ F6 / F8
```

Derivative 可以压缩 annotation density，但不能：

```text
合并两个 canonical objects
改变 causal direction
改变 Case ID meaning
改变 owner / layer boundary
```

F1 v1 在验收时曾主动修正一次：

```text
Experience Acquisition
→ Experience Objects
```

不能为了视觉简洁压成一个 `Experience` 节点。

这条修正作为后续视觉派生的 reference precedent。

---

# Next Derivatives

下一阶段不是继续重画 Level A，而是：

```text
Presentation / Slide D2
→ F1 / F4 / F6 / F8 / F9 / F14 progressive reveal

Publication Level B
→ 只在书稿确实需要时补 F2 / F3 / F5 / F7 / F10 / F11 / F12 / F13

Quick-reference D3
→ 最后裁剪
```

优先保持：

> **Level A 六图是整本书最稳定、最值得对外展示的视觉骨架。**
