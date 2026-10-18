# LLM / Agent Data Visual Release Manifest

> Status: `Stable Mother Edition V3.x / Level A D1–D3 Complete`
>
> Purpose: 把 Level A 六张 canonical Master Figure 与它们的 publication / presentation / quick-reference derivative 绑定成可审计 release unit。

核心原则：

```text
Canonical Figure Source
→ D1 Publication
→ D2 Presentation Storyboard
→ D3 Quick-reference
```

任何 source 语义变化都必须触发 derivative freshness check。

---

# 1. Release Matrix

| Figure | Canonical Source | Source Blob | D1 Publication | D2 Presentation | D3 Quick-reference |
|---|---|---|---|---|---|
| F1 | [`F1`](./figures/F1_Learning_System_Overview.md) | `32a88e3fa6efa31acc8ed1d396008bcf1210fc70` | [`SVG`](./visual_derivatives/publication/F1_Learning_System_Overview.svg) | [`Storyboard`](./visual_derivatives/slides/F1_Learning_System_Progressive_Reveal.md) | [`Card`](./visual_derivatives/quick_reference/Level_A_Quick_Reference_Cards.md#card-f1--learning-system) |
| F4 | [`F4`](./figures/F4_Agent_Task_Environment_Trajectory.md) | `5084a6e0704e3f876e7dd2129ce3089a18301fd0` | [`SVG`](./visual_derivatives/publication/F4_Agent_Task_Environment_Trajectory.svg) | [`Storyboard`](./visual_derivatives/slides/F4_Agent_World_Progressive_Reveal.md) | [`Card`](./visual_derivatives/quick_reference/Level_A_Quick_Reference_Cards.md#card-f4--agent-world) |
| F6 | [`F6`](./figures/F6_Credit_to_Failure_Causal_Map.md) | `a343e95aaf74cd98fda331d4ef4987a240cc7c02` | [`SVG`](./visual_derivatives/publication/F6_Credit_to_Failure_Causal_Map.svg) | [`Storyboard`](./visual_derivatives/slides/F6_Credit_Failure_Progressive_Reveal.md) | [`Card`](./visual_derivatives/quick_reference/Level_A_Quick_Reference_Cards.md#card-f6--credit--failure) |
| F8 | [`F8`](./figures/F8_Benchmark_Evaluation_Protocol.md) | `07b82f944e80f5d1ed004251cdd2f0a3a7ea0886` | [`SVG`](./visual_derivatives/publication/F8_Benchmark_Evaluation_Protocol.svg) | [`Storyboard`](./visual_derivatives/slides/F8_Evaluation_Protocol_Progressive_Reveal.md) | [`Card`](./visual_derivatives/quick_reference/Level_A_Quick_Reference_Cards.md#card-f8--evaluation-protocol) |
| F9 | [`F9`](./figures/F9_Data_Flywheel.md) | `340ee4458d9dfe0f8c1c5810fcfa4cb7b40e3cb2` | [`SVG`](./visual_derivatives/publication/F9_Data_Flywheel.svg) | [`Storyboard`](./visual_derivatives/slides/F9_Data_Flywheel_Progressive_Reveal.md) | [`Card`](./visual_derivatives/quick_reference/Level_A_Quick_Reference_Cards.md#card-f9--data-flywheel) |
| F14 | [`F14`](./figures/F14_Operating_Model_and_Capability_Map.md) | `65a3c9acb498c06c74a870d5a3dd09b50e654ef2` | [`SVG`](./visual_derivatives/publication/F14_Operating_Model_and_Capability_Map.svg) | [`Storyboard`](./visual_derivatives/slides/F14_Operating_Model_Progressive_Reveal.md) | [`Card`](./visual_derivatives/quick_reference/Level_A_Quick_Reference_Cards.md#card-f14--operating-model) |

---

# 2. Freshness Rule

对任意 Figure `Fxx`：

```text
current canonical blob SHA
== derivative recorded source SHA
```

则：

```text
D1 / D2 / D3 may be current
```

如果不一致：

```text
status = STALE UNTIL REVIEWED
```

注意：

```text
SHA 一致
```

只能证明 source 没变，不能替代 semantic acceptance。

仍需检查：

```text
node meaning
edge direction
case semantics
owner boundary
reveal order
```

---

# 3. Current Level A Acceptance

## F1

```text
[x] Experience Acquisition ≠ Experience Objects
[x] Evidence before Learning Signal
[x] feedback loop preserved
```

## F4

```text
[x] Tool ≠ Harness ≠ Environment
[x] World State → Observation → Harness → Agent-visible State
[x] Trajectory remains evidence record
```

## F6

```text
[x] First Error / First Harmful / Root Cause separate
[x] Recoverability / Repairability branch preserved
[x] Failure Layer ≠ Failure Owner
```

## F8

```text
[x] Benchmark / Protocol / Run / Report distinction preserved
[x] Population accounting preserved
[x] Cost + uncertainty + claim scope explicit
```

## F9

```text
[x] Signal → Triage → Attribution before Data
[x] Deploy? Yes / No preserved
[x] Production → Monitoring → Signals feedback preserved
```

## F14

```text
[x] Diagnosis before Owner Routing
[x] Scale / Revise / Stop all preserved
[x] Organization OS ≠ Practitioner OS
```

---

# 4. D1 / D2 / D3 Responsibilities

```text
D1 Publication
= static semantic hierarchy

D2 Presentation
= temporal information order

D3 Quick-reference
= minimal recall surface
```

因此：

```text
D1 可以信息更全
D2 可以分帧
D3 可以强裁剪
```

但三者都不能：

```text
改变 canonical relation
改变 causal direction
改变 Case ID meaning
改变 owner / layer boundary
```

---

# 5. Release Status

```text
Level A Canonical Sources
✓ stable

D1 Publication SVG
✓ complete

D2 16:9 Progressive Reveal
✓ complete

D3 Quick-reference Cards
✓ complete

Source SHA Binding
✓ recorded

Semantic Acceptance
✓ completed for high-risk relations
```

当前结论：

> **Level A Visual System 已从“Master Figure”发展成完整的 Canonical → Publication → Presentation → Quick-reference 四层发布体系。**
