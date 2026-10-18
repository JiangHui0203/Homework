# LLM / Agent Data Knowledge System：Publication Visual Derivative Spec

> 状态：`Stable Mother Edition V3.x / Visual Derivative Layer`
>
> Semantic Source：[`Master Figure System`](./00_Master_Figure_System.md)
>
> Figure Contract：[`Figure Design Contract`](./00_Figure_Design_Contract.md)
>
> 目的：规定 F1–F14 怎样从 Mermaid semantic source 派生为**书稿图、Slides 图、Quick-reference 图**，而不产生第二套语义。

---

# 0. 一条不可破坏的关系

```text
Mermaid Master Figure
= semantic source of truth

Publication / Slide / Social Derivative
= presentation view
```

允许 derivative 改：

```text
layout
typography
spacing
color
progressive reveal
annotation density
aspect ratio
```

不允许 derivative 静默改：

```text
node meaning
edge meaning
canonical term
Case ID
owner / layer boundary
causal direction
```

如果视觉重画发现 Mermaid 本身不够表达：

> **先改 semantic source，再重新派生。**

---

# 1. 三类 Derivative

## D1 — Publication Figure

用途：

```text
书稿
PDF
长文
研究报告
```

目标：

```text
静态单页可读
黑白打印仍可理解
Caption 脱离正文仍成立
不依赖动画
```

推荐：

```text
宽度：单栏 / 双栏自适应
主链：5–9 个核心节点
次级节点：优先做 annotation，不全部进入主图
字号：最终导出后正文不小于 8.5–9 pt
线宽：打印后清晰
```

Publication Figure 强调：

```text
semantic hierarchy
scan path
caption completeness
```

---

## D2 — Presentation Figure

用途：

```text
答辩
组会
面试
课程分享
```

目标：

```text
16:9
3–8 秒能找到视觉入口
30–90 秒能讲完
支持 progressive reveal
```

原则：

```text
一页一个 thesis
主链先出现
边界后出现
case 最后落地
```

不要把 Mermaid 所有节点第一帧全部堆上去。

---

## D3 — Quick-reference Figure

用途：

```text
面试复习
Notion / README
手机截图
分享卡片
```

目标：

```text
只保留最关键链
1 个 boundary box
1 句 takeaway
```

它不是 Publication Figure 的缩小版，而是信息重新裁剪后的 derivative。

---

# 2. Visual Language

## 2.1 Shape Semantics

全书统一：

```text
Rounded Rectangle
→ Object / State / Artifact

Rectangle
→ Process / Transformation

Diamond
→ Decision / Gate / Question

Pill / Tag
→ Case / Status / Version

Container / Band
→ Layer / Owner / Phase
```

不要为了“更好看”给相同语义换形状。

---

## 2.2 Edge Semantics

```text
Solid Arrow
→ execution / transition / main operational progression

Dashed Arrow
→ evidence / feedback / derived / auxiliary relation

Thin Return Arrow
→ monitoring / feedback loop
```

不要只用颜色区分 edge semantics。

---

## 2.3 Color Semantics

颜色是冗余编码，不是唯一编码。

建议最多四类：

```text
Neutral
→ object / context

Action
→ intervention / execution

Evidence
→ measurement / verifier / observation

Risk / Failure
→ harmful / warning / unresolved
```

要求：

```text
grayscale readable
color-blind safe
light / dark background 都可重绘
```

具体色值不进入 semantic contract，可由最终出版模板决定。

---

# 3. Text Density

一个节点优先：

```text
1 canonical term
+
0–1 行解释
```

不要：

```text
把正文段落塞进节点
```

节点文本推荐：

```text
World State
order.status = shipped
```

而不是：

```text
The world state contains all information about...
```

解释留在：

```text
caption
legend
callout
正文
```

---

# 4. Caption Contract

每张 publication derivative caption 至少回答：

```text
Figure 是什么？
主链是什么？
最重要 boundary 是什么？
如果用了 case，它证明什么？
```

推荐格式：

> **Fxx — Title.** 主链一句话；随后指出最容易混淆的边界。必要时说明 Case ID 的作用。

Caption 不写：

```text
“上图展示了……”
```

而应直接给 substantive takeaway。

---

# 5. Level A 六张图的 Publication Brief

## F1 — Learning System Overview

### Single Thesis

> LLM / Agent Data 的对象不是“训练集”，而是从真实目标到经验、证据、学习信号、训练、部署再回到现实的 Learning System。

### Publication Layout

推荐左右闭环：

```text
Real Goal
→ Task / Environment
→ Experience
→ Evidence
→ Learning Signal
→ Training
→ Deployment
→ Outcome / Drift
↺
```

四个 acquisition / evaluator / signal 子类不要全部放进主链，可做上下 annotation bands。

### Mandatory Boundary Box

```text
Experience ≠ Learning Signal
Evidence ≠ Label
```

### Best Case Callout

```text
C1
production failure → evidence → data intervention → experiment → monitor
```

---

## F4 — Agent Task–Environment–Trajectory

### Single Thesis

> Agent 不是“模型 + Tool Call”，而是 Task、Harness、Tool、Environment、World State、Observation 与 Agent-visible State 共同组成的交互系统。

### Publication Layout

建议三层横带：

```text
Intent Layer
Task / Policy

Runtime Layer
Harness / Tool

World Layer
Environment / World State
```

Trajectory 作为贯穿三层的 event stream 放在底部。

### Mandatory Boundary Box

```text
Tool ≠ Harness ≠ Environment
World State ≠ Observation ≠ Agent-visible State
```

### Best Case Callout

`C1-VB` 或 `C3-F5`。

---

## F6 — Credit → Failure Causal Map

### Single Thesis

> Failure Analysis 必须从 Outcome 沿 causal chain 回溯，不能从最终 symptom 直接跳到 Root Cause / Owner。

### Publication Layout

建议单一纵向主链：

```text
Outcome
↓
First Error
↓
First Harmful Action
↓
Last Recoverable State
↓
Point of No Return
↓
Mechanism
↓
Root Cause
↓
Owner
```

旁边放两个 short case callout：

```text
C1-F1
C3-F5
```

### Mandatory Boundary Box

```text
First Error ≠ First Harmful ≠ Root Cause
Failure Layer ≠ Failure Owner
```

---

## F8 — Benchmark / Evaluation Protocol

### Single Thesis

> “方法更好”只有在 Population、Protocol、Budget、Evaluator、Statistics 与 Claim Scope 都被固定和报告以后才成立。

### Publication Layout

推荐 funnel + paired branch：

```text
Question
→ Capability
→ Benchmark
→ Frozen Protocol
↙           ↘
Baseline   Treatment
↘           ↙
Paired / Matched Analysis
→ Metrics / Cost / Uncertainty
→ Claim Scope
```

Population Accounting 单独做侧栏。

### Mandatory Boundary Box

```text
Triggered-only ≠ E2E
Higher Score ≠ Better Method if Budget Differs
```

---

## F9 — Data Flywheel

### Single Thesis

> Production Failure 不能直接变成 Training Example；中间必须经过 Triage、Attribution、Capability Abstraction、Supervision Choice 和 Controlled Validation。

### Publication Layout

主闭环：

```text
Real Use
→ Signal
→ Diagnose
→ Capability Gap
→ Acquire / Construct
→ Curate
→ Experiment
→ Train
→ Evaluate
→ Deploy
↺
```

把 `Tool / Harness / Evaluator bug → non-data fix` 做成旁路，不塞进主环。

### Mandatory Boundary Box

```text
Production Failure ≠ Training Example
Failure Routing may end in non-data intervention
```

---

## F14 — Operating Model + Capability Map

### Single Thesis

> 成熟团队不是把所有问题交给 Data Team，而是通过 Diagnosis Gate、正确 Owner、Evidence Gate、Intervention 与 Evaluation 形成可持续 operating loop。

### Publication Layout

建议上下两层：

```text
Top
Organization Operating Model

Bottom
Practitioner Capability Map
```

不要尝试在一张图里同时展开所有八域细节。

### Mandatory Boundary Box

```text
Problem → Diagnosis → Owner → Evidence Gate → Intervention → Decision
```

---

# 6. Slide Progressive Reveal Contract

Level A 图统一四步：

```text
Step 1
只出现 Figure Question + 主链

Step 2
加入关键 layer / branch

Step 3
加入 critical boundary

Step 4
加入 canonical case callout
```

禁止：

```text
Step 1 就出现所有 annotation / footnote / case / exception
```

Presentation Kit 的 30s / 90s talk track 应与 reveal 顺序一致。

---

# 7. Export Contract

每个正式 derivative 最终应至少保留：

```text
figure_id
semantic_source_path
semantic_source_sha
export_type
export_version
created_at
```

例如：

```yaml
figure_id: F6
semantic_source: figures/F6_Credit_to_Failure_Causal_Map.md
semantic_source_sha: <git blob sha>
export_type: publication_svg
export_version: v1
```

这样未来 F6 semantic source 改了，可以知道哪些 SVG / PPT 已过期。

---

# 8. File Layout Recommendation

未来 derivative 建议进入：

```text
visual_derivatives/
├── publication/
│   ├── F1_Learning_System_Overview.svg
│   └── ...
├── slides/
│   ├── F1_Learning_System_Overview.svg
│   └── ...
└── quick_reference/
    ├── F1_Learning_System_Overview.svg
    └── ...
```

源文件仍在：

```text
figures/F1...F14.md
```

不要覆盖 Mermaid source。

---

# 9. Acceptance Checklist

一张 derivative 发布前检查：

```text
[ ] Figure ID 正确
[ ] canonical terms 未漂移
[ ] edge direction 与 Mermaid 一致
[ ] Case ID 语义未改变
[ ] grayscale 可读
[ ] Caption 独立成立
[ ] 没有把 annotation 误画成 causal edge
[ ] semantic_source_sha 已记录
[ ] 30–90 秒可讲清
```

---

# 10. 下一阶段

优先顺序：

```text
Publication D1
F1 → F4 → F6 → F8 → F9 → F14

Presentation D2
沿相同顺序做 progressive reveal

Quick-reference D3
最后裁剪
```

原则：

> **先把最重要的六张做成真正成品，而不是同时把 14 张全部画得半成品。**
