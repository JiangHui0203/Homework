# Visual Derivatives

本目录保存从 F1–F14 Mermaid semantic source 派生的 presentation assets。

规范：

- [`Publication Visual Derivative Spec`](../00_Publication_Visual_Derivative_Spec.md)
- [`Visual Release Manifest`](../00_Visual_Release_Manifest.md)
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

# Level A Visual Release

状态：**D1–D3 Complete**

完整绑定关系见：

- [`Visual Release Manifest`](../00_Visual_Release_Manifest.md)

六张视觉骨架：

```text
F1  Learning System
↓
F4  Agent World
↓
F6  Credit / Failure
↓
F8  Evaluation Protocol
↓
F9  Continuous Learning
↓
F14 Operating Model
```

---

# D1 — Publication

状态：**Complete v1**

| Figure | Publication SVG | Semantic Source |
|---|---|---|
| F1 | [Learning System Overview](./publication/F1_Learning_System_Overview.svg) | [`figures/F1`](../figures/F1_Learning_System_Overview.md) |
| F4 | [Agent Task–Environment–Trajectory](./publication/F4_Agent_Task_Environment_Trajectory.svg) | [`figures/F4`](../figures/F4_Agent_Task_Environment_Trajectory.md) |
| F6 | [Credit → Failure Causal Map](./publication/F6_Credit_to_Failure_Causal_Map.svg) | [`figures/F6`](../figures/F6_Credit_to_Failure_Causal_Map.md) |
| F8 | [Benchmark / Evaluation Protocol](./publication/F8_Benchmark_Evaluation_Protocol.svg) | [`figures/F8`](../figures/F8_Benchmark_Evaluation_Protocol.md) |
| F9 | [Data Flywheel](./publication/F9_Data_Flywheel.svg) | [`figures/F9`](../figures/F9_Data_Flywheel.md) |
| F14 | [Operating Model + Capability Map](./publication/F14_Operating_Model_and_Capability_Map.svg) | [`figures/F14`](../figures/F14_Operating_Model_and_Capability_Map.md) |

D1 负责：

```text
static semantic hierarchy
book / PDF / report figure
caption-complete view
```

---

# D2 — Presentation

状态：**Complete / 16:9 Progressive Reveal**

总入口：[`slides/README.md`](./slides/README.md)

| Figure | Progressive Reveal Storyboard |
|---|---|
| F1 | [Learning System](./slides/F1_Learning_System_Progressive_Reveal.md) |
| F4 | [Agent World](./slides/F4_Agent_World_Progressive_Reveal.md) |
| F6 | [Credit → Failure](./slides/F6_Credit_Failure_Progressive_Reveal.md) |
| F8 | [Evaluation Protocol](./slides/F8_Evaluation_Protocol_Progressive_Reveal.md) |
| F9 | [Data Flywheel](./slides/F9_Data_Flywheel_Progressive_Reveal.md) |
| F14 | [Operating Model](./slides/F14_Operating_Model_Progressive_Reveal.md) |

每张 storyboard 已定义：

```text
1920 × 1080 canvas
Frame IDs
Visible Objects
New Objects
Hidden Until Later
Speaker Line
Critical Boundary
30s route
90s route
semantic acceptance
```

D2 负责：

```text
temporal information order
progressive reveal
speaker pacing
```

---

# D3 — Quick-reference

状态：**Complete**

入口：

- [`Level A Quick-reference Cards`](./quick_reference/Level_A_Quick_Reference_Cards.md)

每张卡只保留：

```text
Question
Spine
Boundary
Case
Takeaway
```

D3 负责：

```text
mobile screenshot
interview refresh
share / one-screen recall
```

它不是 D1 的缩小版，而是重新裁剪的 recall surface。

---

# Derivative Design Rule

Level A 已验证三类不同结构都可以稳定派生：

```text
Closed Loop
→ F1 / F9

Layered System
→ F4 / F14

Causal / Protocol Chain
→ F6 / F8
```

Derivative 可以改变：

```text
layout
typography
spacing
color
annotation density
reveal order
```

但不能：

```text
合并两个 canonical objects
改变 causal direction
改变 Case ID meaning
改变 owner / layer boundary
```

已经通过 derivative audit 抓到并修正过的高风险先例：

```text
F1
Experience Acquisition ≠ Experience Objects

F4
Observation → Harness → Agent-visible State

F9
Production → Monitoring → Signals
Deploy? Yes → Production / No → Capability Gap

F14
Decision → Scale / Revise / Stop
Revise → Diagnosis
Stop → Archive / Knowledge
```

这些修正作为后续视觉派生的 reference precedent。

---

# Current Status

```text
Level A Canonical Master Figures
✓ stable

D1 Publication SVG
✓ complete

D2 Presentation Storyboard
✓ complete

D3 Quick-reference Cards
✓ complete

Source SHA Binding
✓ complete

Visual Release Manifest
✓ complete
```

后续优先级：

```text
Publication Level B
→ 只在书稿 / 报告真正需要时补

Actual PPT / Keynote rendering
→ 直接实现 D2，不重新设计 reveal logic

Visual refresh
→ 只改 presentation，不静默改 semantics
```

> **Level A 六图现在已经形成 Canonical → Publication → Presentation → Quick-reference 的完整视觉发布链。**
