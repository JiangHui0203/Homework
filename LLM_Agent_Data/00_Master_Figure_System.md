# LLM / Agent Data Knowledge System：Master Figure System

> 状态：Editorial Infrastructure / Visual System
>
> 目的：为 0–25 章建立一套稳定、可复用、可版本化的 Master Figure。图的任务不是装饰，而是压缩跨章节关系、固定对象边界、帮助读者建立全书级 mental model。
>
> 原则：**一张图只承担一个主要认知任务；canonical concept 只在对应 master figure 中完整展开，其他章节优先引用而不是重复重画。**

---

# 0. 为什么需要 Master Figure

当前章节里已有大量 ASCII / Mermaid 图，但它们大多是局部图。随着全书结构稳定，继续每章各画一套会产生三个问题：

```text
同一概念被画成不同结构
同一 case 被不同章节重新发明
局部图很多，但缺少全书级导航
```

Master Figure System 的目标是：

```text
Canonical Concept
+
Canonical Case / Variant
+
Stable Visual Grammar
+
Chapter Lens
```

最终读者看到同一种对象时，视觉关系也保持一致。

---

# 1. Visual Grammar

统一使用以下语义：

```text
实线箭头  → 实际执行 / 因果 /数据流
虚线箭头  → 评价 / 反馈 / 派生关系
菱形       → Decision Gate
圆角节点   → Object / State / Artifact
方框       → System / Process
子图       → Layer / Owner / Phase
```

Mermaid 中尽量依赖默认主题，不绑定特定颜色，保证 GitHub Light / Dark Mode 都可读。

图内文字原则：

1. 节点只放短语，不放完整段落。
2. 中文负责解释，英文保留 canonical term。
3. 同一概念全书统一写法，例如 `World State`、`Agent-visible State`、`Outcome`、`Reward`、`Credit`。
4. Case variant 直接使用 `C1-VB / C4-SC` 等稳定 ID。
5. 图下正文负责解释“为什么”，图本身负责展示“关系是什么”。

---

# 2. Master Figure Registry

| ID | Figure | 主要认知任务 | Canonical Owner | 主案例 |
|---|---|---|---|---|
| F1 | Learning System Overview | 整本书到底在描述什么系统 | Ch0 / Ch25 | C1 + C4 |
| F2 | Data Object & Learning Signal Evolution | Example 如何扩展成 Experience | Ch1–3 | C1 |
| F3 | Reasoning State Decision Stack | Correctness / Risk / Recoverability / Repairability / Selectability | Ch4 | C4-SC |
| F4 | Agent Task–Environment–Trajectory | Task、Tool、Harness、Environment、Trajectory 的关系 | Ch10–12 | C1-VB |
| F5 | Trajectory Anatomy | 一条 trajectory 内部应该记录什么 | Ch12 | C1-F1 |
| F6 | Credit → Failure Causal Map | 从 Outcome 到 Root Cause 的完整因果链 | Ch13–14 | C1-F1 + C3-F5 |
| F7 | Evidence → Evaluator Stack | Evidence / Verifier / Grader / Judge | Ch15 | C1 + C5-F3 |
| F8 | Benchmark / Evaluation Protocol | 怎么公平比较模型 / intervention | Ch16 | C1 family |
| F9 | Data Flywheel | Failure 如何重新变成 Learning Signal | Ch17 | C1 |
| F10 | Data Strategy / Portfolio / ROI | 资源到底投哪里 | Ch18 | multi-case portfolio |
| F11 | Governance / Lineage DAG | 一个结论怎样追溯到原始数据 | Ch19 | C1 assets |
| F12 | Data Production System | 高价值数据怎样被稳定制造 | Ch22 | C1 recovery family |
| F13 | Monitoring / Drift Diagnostic Tree | 指标变了以后先查什么 | Ch23 | C1 / C3 |
| F14 | Operating Model + Capability Map | 团队和个人怎样调用全系统 | Ch24–25 | all cases |

---

# 3. Figure Levels

## Level A — Book-level

全书最多 6 张，用于形成 mental model：

```text
F1 Learning System
F4 Agent Task–Environment–Trajectory
F6 Credit → Failure
F8 Evaluation Protocol
F9 Data Flywheel
F14 Operating Model + Capability Map
```

## Level B — Part-level

服务一个 Part：

```text
F2 / F3 / F5 / F7 / F10 / F11 / F12 / F13
```

## Level C — Chapter-local

局部 pipeline / formula / example 图仍可以保留，但不应重新定义 Level A/B 已有关系。

---

# 4. Chapter Integration Rule

章节引用 Master Figure 时统一采用：

```text
> Master Figure：F6 — Credit → Failure Causal Map。
> 本章只展开其中的 Credit / Failure 层。
```

如果一个章节只使用图的一部分，不复制整图，可用：

```text
F6 Lens: First Harmful Action → Root Cause
```

也就是说：

```text
Master Figure = stable system model
Chapter = analytical lens
```

---

# 5. Case Integration Rule

图中使用 case 时：

```text
C1-VB
= shipped / no refund allowed

C1-F1
= shipped observed but refund executed

C3-F5
= tool truth failure / harness observation success

C4-SC
= same authoritative prefix sibling set
```

Case ID 不得为了图示简洁改变语义。

---

# 6. Production Roadmap

第一批：

```text
F1 / F4 / F6 / F8 / F9 / F14
```

第二批：

```text
F2 / F3 / F5 / F7 / F10 / F11 / F12 / F13
```

第三步：

```text
把旧章节局部图逐一判断：
KEEP / REPLACE WITH MASTER / KEEP AS LOCAL LENS
```

最后才考虑：

```text
SVG / publication redraw
```

避免在结构仍变化时浪费视觉设计成本。

---

# 7. 完成标准

Master Figure System 完成后，应能做到：

```text
读 F1
→ 知道全书讲什么

读 F4
→ 知道 Agent 世界中对象怎么连接

读 F6
→ 知道 failure 为什么不能只看最后一步

读 F8
→ 知道一个提升结论需要什么 protocol

读 F9
→ 知道线上 failure 如何进入下一轮 learning

读 F14
→ 知道团队和个人怎样真正运行这套体系
```

最终目标：

> **读者即使暂时不读 25 章全文，也能通过 Master Figures 建立正确的整体结构；再进入章节时，只是在放大某个局部，而不是重新学习一套世界。**
