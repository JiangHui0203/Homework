# Level A Presentation Derivatives

> Status: `D2 Complete / 16:9 Progressive Reveal Storyboards`
>
> Semantic Sources: [`../../figures/`](../../figures/README.md)
>
> Talk-track Source: [`../../00_Figure_Presentation_Kit.md`](../../00_Figure_Presentation_Kit.md)
>
> Derivative Contract: [`../../00_Publication_Visual_Derivative_Spec.md`](../../00_Publication_Visual_Derivative_Spec.md)

本目录负责 Level A 六张 Master Figure 的 16:9 progressive reveal 语义。

它不是 PPT 文件本身，而是：

> **PPT / Keynote / Web animation 必须遵守的唯一 reveal storyboard。**

---

# 1. Storyboard Registry

| Figure | Storyboard | Frames | Core Question |
|---|---|---:|---|
| F1 | [Learning System](./F1_Learning_System_Progressive_Reveal.md) | 6 | LLM / Agent Data 到底在维护什么系统？ |
| F4 | [Agent World](./F4_Agent_World_Progressive_Reveal.md) | 7 | Task / Harness / Tool / Environment / State 怎么连接？ |
| F6 | [Credit → Failure](./F6_Credit_Failure_Progressive_Reveal.md) | 7 | bad outcome 怎样变成可信 Root Cause / Owner？ |
| F8 | [Evaluation Protocol](./F8_Evaluation_Protocol_Progressive_Reveal.md) | 7 | “方法更好”怎样才是可信 claim？ |
| F9 | [Data Flywheel](./F9_Data_Flywheel_Progressive_Reveal.md) | 7 | failure 怎样重新进入下一轮 learning loop？ |
| F14 | [Operating Model](./F14_Operating_Model_Progressive_Reveal.md) | 7 | 团队和个人怎样调用整套系统？ |

---

# 2.统一 Slide Contract

```text
Canvas
1920 × 1080 / 16:9

Safe Area
120 px each edge

Title Zone
Top ~150 px

Main Visual Zone
Middle

Footer / Source
Bottom ~90 px
```

每个 Frame 必须声明：

```text
Visible Objects
New Objects
Hidden Until Later
Speaker Line
Transition
Critical Boundary（如有）
```

核心原则：

> **Progressive reveal 只能逐步增加信息，不能在后续帧修改前一帧已经建立的概念语义。**

---

# 3. Reveal Grammar

统一顺序：

```text
Question / Problem
↓
Main Spine
↓
Layer / Branch
↓
Critical Boundary
↓
Case Lens
↓
Final Takeaway
```

禁止：

```text
第一帧出现所有 annotation
第一帧同时讲多个 visual center
后续 frame 偷换 node meaning
Case 在 canonical relation 之前出现
```

---

# 4. 5-minute Interview Route

```text
F1
→ F6
→ F8
→ F14
```

## Narrative

```text
我怎么看 LLM / Agent Data
→ 我怎么诊断 bad case
→ 我怎么证明 intervention
→ 我怎么把它变成 operating model
```

推荐每张：

```text
30–45 seconds
```

只使用各 storyboard 的 `30s Version`。

---

# 5. 10-minute Agent Data Route

```text
F1
→ F4
→ F6
→ F9
→ F14
```

## Narrative

```text
Learning System
→ Agent World
→ Failure Causality
→ Learning Opportunity
→ Operating Model
```

推荐：

```text
F1   75s
F4   90s
F6   90s
F9   90s
F14  90s
+ intro / transition
```

---

# 6. 10-minute Research / Benchmark Route

```text
F1
→ F6 or F3
→ F8
→ F9
```

其中 F3 当前仍使用 canonical Master Figure / Presentation Kit，不属于 Level A D2 batch。

## Narrative

```text
System framing
→ state / failure problem
→ scientific protocol
→ how evidence returns to learning
```

---

# 7. Semantic Acceptance

当前六张均满足：

```text
[x] Figure ID stable
[x] Source blob SHA recorded
[x] Canonical node meanings preserved
[x] Edge direction preserved
[x] Critical boundaries appear after main spine
[x] Case lens appears after canonical relation
[x] 30s and 90s routes both defined
[x] 16:9 canvas contract defined
```

特别经过修正的高风险关系：

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

---

# 8. Implementation Rule

未来真正生成：

```text
PPTX
Keynote
HTML animation
Reveal.js
SVG frame sequence
```

都不重新设计 reveal logic。

只实现：

```text
layout
motion
font
color
speaker notes
```

如果 storyboard 本身需要改语义：

> **先回 canonical Master Figure，再重新派生 storyboard。**
