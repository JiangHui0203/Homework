# LLM / Agent Data Knowledge System：Figure Integration Audit

> 状态：`PASS — Acceptance Complete`
>
> 目的：检查正文中的局部 Mermaid / ASCII 图与 F1–F14 Master Figures 是否重复定义同一关系，并确定全局视觉真源与章节局部 Lens 的边界。
>
> 核心原则：**Master Figure 负责稳定的全局对象关系；章节局部图只有在增加新的分析粒度时才保留。不是图越少越好，而是同一个 canonical relation 不应存在两套竞争性视觉定义。**

---

# 0. 判定规则

```text
KEEP
→ 图本身具有独立教学价值，且不与 Master Figure 竞争定义权。

LOCAL LENS
→ 图放大 Master Figure 的一个局部机制，保留。

REPLACE
→ 图本质上重新画了一遍 Master Figure 的全局关系，应由 Master Figure 接管。

ADD POINTER
→ 正文没有重复图，但适合显式链接对应 Master Figure。
```

编辑纪律：

```text
Master Figure = canonical visual model
Chapter-local Figure = analytical lens
```

---

# 1. F1–F14 验收矩阵

| Figure | Canonical owner | 章节局部图判定 | 验收结论 |
|---|---|---|---|
| F1 Learning System Overview | Ch0 / Ch25 | Ch0 textual loop、Ch25 practitioner path `KEEP` | 全局闭环由 F1 负责，文字链保留 |
| F2 Data Object & Learning Signal Evolution | Ch1–3 | `KEEP / LOCAL LENS` | Dataset / Task / Preference 等局部例子保留 |
| F3 Reasoning State Decision Stack | Ch4 | `LOCAL LENS` | representation / action space / research example / pipeline 均有独立增量 |
| F4 Agent Task–Environment–Trajectory | Ch10–12 | Ch10 Task Contract `LOCAL LENS`，Ch11–12 `ADD POINTER` | 不重画第二套 Agent World 总图 |
| F5 Trajectory Anatomy | Ch12 | `KEEP / LOCAL LENS` | event schema / visibility / retry / replay 属于局部解剖 |
| F6 Credit → Failure Causal Map | Ch13–14 | Ch13 图保留；Ch14 §14.0 `REPLACE` | **已完成接管** |
| F7 Evidence → Verifier / Grader / Judge | Ch15 | Ch15 §15.0 `REPLACE` | **已完成接管** |
| F8 Benchmark / Evaluation Protocol | Ch16 | `ADD POINTER` | Ch16 局部 evaluation lens 保留 |
| F9 Data Flywheel | Ch17 | textual loop `KEEP` | F9 为视觉真源，Ch17 保留阅读节奏 |
| F10 Data Strategy / Portfolio / ROI | Ch18 | tables / formulas `KEEP` | 无竞争性总图 |
| F11 Governance / Lineage DAG | Ch19 | Ch19 §19.5 `REPLACE` | **已完成接管** |
| F12 Data Production System | Ch22 | textual pipeline `KEEP` | Job / Retry / Idempotency 等 local lens 保留 |
| F13 Monitoring / Drift Diagnostic Tree | Ch23 | `ADD POINTER` | Drift branch 细节继续归 Ch23 |
| F14 Operating Model + Capability Map | Ch24–25 | lifecycle / capability / routing trees `KEEP` | F14 负责书级视觉收束 |

---

# 2. 三处高置信重复图：已全部关闭

## R1 — Ch14 §14.0 → F6

状态：`DONE`

正文：[`第 14 章 Agent Failure Taxonomy`](./14_Agent_Failure_Taxonomy.md)

Master Figure：[`F6 — Credit → Failure Causal Map`](./figures/F6_Credit_to_Failure_Causal_Map.md)

已处理：

```text
删除竞争性的 §14.0 总 Mermaid
↓
章节入口增加 F6 pointer
↓
§14.0 保留本章诊断 Lens：
Outcome / Incident
→ Symptom
→ Localization
→ Immediate Mechanism
→ Root Cause
→ Failure Owner
→ Severity / Detectability
→ Recoverability / Repairability
→ Intervention Routing
```

仍保留 §14.38 Failure Analysis Pipeline，因为它额外表达：

```text
Success → Process Audit
```

以及 operational routing，属于 `LOCAL LENS`，不是 F6 的重复定义。

---

## R2 — Ch15 §15.0 → F7

状态：`DONE`

正文：[`第 15 章 Grader、Verifier 与 LLM-as-a-Judge`](./15_Grader_Verifier_and_LLM_as_a_Judge.md)

Master Figure：[`F7 — Evidence → Verifier / Grader / Judge`](./figures/F7_Evidence_Verifier_Grader_Judge.md)

已处理：

```text
删除竞争性的五层总 Mermaid
↓
章节入口增加 F7 pointer
↓
正文继续解释：
Evidence
→ Evaluator
→ Raw Judgment
→ Derived Label / Score
→ Final Decision / Metric

Gold / Anchor
→ Meta-evaluation
→ Calibrate / Route / Replace
```

Evaluator taxonomy、Evidence Sufficiency、Routing、Bias、Meta-evaluation 等局部结构全部保留。

---

## R3 — Ch19 §19.5 → F11

状态：`DONE`

正文：[`第 19 章 Data Governance、Lineage 与 Reproducibility`](./19_Data_Governance_Lineage_and_Reproducibility.md)

Master Figure：[`F11 — Governance / Lineage DAG`](./figures/F11_Governance_Lineage_DAG.md)

已处理：

```text
删除第二套 lineage 总 DAG
↓
章节入口增加 F11 pointer
↓
§19.5 改为解释：
Lineage Node
Lineage Edge
Lineage Query
```

同时保留：

```text
反向追踪：Model issue → Raw Source
正向追踪：Bad Label → affected Models / Reports
```

因此图与正文现在分工明确：

```text
F11
= canonical graph structure

Ch19
= graph semantics + governance operations
```

---

# 3. 为什么其他局部图不删？

审计后的主要结论不是“大量删图”，而是：

> **绝大多数章节局部图都比 Master Figure 多提供了一层局部机制。**

典型例子：

```text
Ch13 State → Action → Outcome → Reward → Credit?
→ 解释 terminal outcome 如何回指中间 action

Ch13 Hierarchical Credit
→ 解释 trajectory / subgoal / decision / action 四级粒度

Ch10 Task Decomposition DAG
→ 解释 dependency / subgoal complexity

Ch24 Operating Lifecycle
→ 解释真实项目如何从 Intake 一路推进到 Maintain / Retire
```

这些都属于：

```text
LOCAL LENS / KEEP
```

而不是全局视觉定义。

---

# 4. Canonical 接入格式

后续新增或维护章节时，统一优先使用：

```markdown
> **Master Figure：** [F# — Figure Name](./figures/F#_File.md)
```

章节正文只补：

```text
本章 Lens
本章局部 workflow
本章特殊 failure / decision / evaluation structure
```

不要：

```text
把 Master Figure 全文复制到每一章
```

也不要：

```text
为了统一，把真正有独立信息的局部图全部删掉
```

---

# 5. Path Spot-check

状态：`PASS`

本轮已双向读取确认：

```text
Ch14
→ ./figures/F6_Credit_to_Failure_Causal_Map.md
→ target exists
→ canonical owner = Ch13–14

Ch15
→ ./figures/F7_Evidence_Verifier_Grader_Judge.md
→ target exists
→ canonical owner = Ch15

Ch19
→ ./figures/F11_Governance_Lineage_DAG.md
→ target exists
→ canonical owner = Ch19
```

详细证据边界见 [`00_Link_Audit.md`](./00_Link_Audit.md)。

---

# 6. Figure Acceptance Result

```text
F1–F14 registry
✓ complete

Canonical visual ownership
✓ stable

High-confidence duplicate global diagrams
3 identified
3 resolved

Useful local lenses
✓ retained

Final path spot-check
✓ pass
```

最终原则：

> **图的统一不是“所有章节画成同一张图”，而是让全局关系只有一个视觉真源，局部章节只负责放大自己真正需要解释的部分。**
