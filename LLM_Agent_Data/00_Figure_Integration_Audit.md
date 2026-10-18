# LLM / Agent Data Knowledge System：Figure Integration Audit

> 状态：Master Figure Acceptance / Integration Audit
>
> 目的：检查正文中的局部 Mermaid / ASCII 图与 F1–F14 Master Figures 是否重复定义同一关系，并给出 `KEEP / LOCAL LENS / REPLACE / ADD POINTER` 判定。
>
> 核心原则：**Master Figure 负责稳定的全局对象关系；章节局部图只有在增加新的分析粒度时才保留。不是图越少越好，而是同一个 canonical relation 不应存在两套竞争性视觉定义。**

---

# 0. 判定规则

```text
KEEP
→ 图本身具有独立教学价值，且不与 Master Figure 竞争定义权。

LOCAL LENS
→ 图放大 Master Figure 的一个局部机制，保留，并在需要时注明对应 F#。

REPLACE
→ 图本质上重新画了一遍 Master Figure 的全局关系，应由 Master Figure 接管。

ADD POINTER
→ 正文没有重复图，但适合在章节入口显式链接对应 Master Figure。
```

编辑纪律：

```text
Master Figure = canonical visual model
Chapter-local Figure = analytical lens
```

---

# 1. F1 — Learning System Overview

Canonical owner：Ch0 / Ch25。

判定：

```text
Landing Page / Ch0
→ ADD POINTER / KEEP TEXTUAL LOOP
```

原因：Landing Page 已直接链接 F1；Ch0 的文字闭环承担概念导入，不需要为了统一而删除。

Ch25 的端到端文字总图：

```text
Real User / Product / Research Goal
→ Problem Framing
→ Task / Environment
→ Rollout
→ Evidence
→ Data
→ Experiment
→ Production
→ Monitoring
↺
```

判定：`KEEP`。

原因：Ch25 是 practitioner call path，不是对 F1 的视觉替代；F1 描述 learning system，Ch25 描述 practitioner invocation sequence。

---

# 2. F2 — Data Object & Learning Signal Evolution

Canonical owner：Ch1–3。

判定：

```text
Ch1 / Ch2 / Ch3 existing object / supervision examples
→ KEEP / LOCAL LENS
```

F2 负责全局回答：

```text
Example
→ Demonstration
→ Relative Feedback
→ Process / State Signal
→ Experience
```

各章内部对 Dataset / Sample / Task / Preference / Reward 的局部示例仍有独立价值。

不建议为“视觉统一”把 Ch1–3 全部改成引用一张图。

---

# 3. F3 — Reasoning State Decision Stack

Canonical owner：Ch4。

Ch4 当前主要局部图：

```text
§4.0 Reasoning State sequence + process signals
§4.2 Outcome vs Process
§4.10 Continue / Stop vs Branch / Repair
§4.11 Answerer–Auditor structured audit state
§4.12 More Thinking vs RoTFuse action-space comparison
§4.14 Reasoning Data Production Pipeline
```

判定：全部 `LOCAL LENS`。

原因：F3 的 canonical 任务是固定：

```text
Correctness
Risk
Recoverability
Repairability
Selectability
```

而上述局部图分别解释：

```text
representation
supervision layer
action space
research example
production pipeline
```

不存在直接重复定义。

建议：Ch4 入口增加：

```text
Master Figure: F3 — Reasoning State Decision Stack
```

但不删除局部图。

---

# 4. F4 — Agent Task–Environment–Trajectory

Canonical owner：Ch10–12。

## Ch10 §10.0 Task Contract 图

```text
User Request / Environment / Tools / Permissions
→ Goal / Initial State / Actions / Constraints
→ Episode
→ Final State / Verifier
```

判定：`LOCAL LENS`。

原因：它专门解释 Task Contract 的字段来源，粒度比 F4 更偏 Task Design。

## Ch10 §10.13 Task Decomposition DAG

判定：`KEEP`。

它解释 dependency / subgoal complexity，与 F4 无重复。

## Ch11

主要使用局部 state / transition / observation 文字结构，没有竞争性的全局 Mermaid。

判定：`ADD POINTER` 到 F4。

## Ch12

正文详细解释 Typed Event Log / State Lineage，但没有重新画完整 Task–Environment–Trajectory 总关系。

判定：`ADD POINTER` 到 F4 + F5。

---

# 5. F5 — Trajectory Anatomy

Canonical owner：Ch12。

Ch12 当前正文主要使用 schema、event list、ASCII flow 和 branch/retry/backtrack examples。

判定：

```text
Existing local structures
→ KEEP / LOCAL LENS
```

原因：F5 固定整条 trajectory 的 canonical visual anatomy；正文则详细解释 event schema、visibility、retry lineage、memory lineage、replay。

建议 Ch12 顶部显式链接 F5，而不是重画另一张总图。

---

# 6. F6 — Credit → Failure Causal Map

Canonical owner：Ch13–14。

## Ch13 §13.0 State → Action → Outcome → Reward → Credit?

判定：`LOCAL LENS`。

它突出的是：

> terminal reward 如何回指中间 actions。

比 F6 更偏 Credit Assignment 起点。

## Ch13 §13.20 Hierarchical Credit

判定：`KEEP`。

它解释 trajectory / subgoal / decision / action 四级 credit granularity。

## Ch13 §13.28 Credit Pipeline

判定：`LOCAL LENS`。

它从 Outcome Verification 一路延伸到 Learning-signal Routing，虽然和 F6 有交集，但提供了“credit → dataset routing”这一额外维度。

## Ch14 §14.0 Failure Taxonomy 总图

当前：

```text
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

判定：`REPLACE WITH F6`。

原因：这是当前最明确的重复定义。F6 已承担完整的 Credit → Failure Causal Map，而且同时使用 C1-F1 / C3-F5 展示：

```text
Failure Layer ≠ Failure Owner
```

建议：

```text
删除 / 收起 §14.0 的重复 Mermaid
改为：Master Figure F6 + 本章 Lens = Symptom → Root Cause → Owner → Routing
```

## Ch14 §14.38 Failure Analysis Pipeline

判定：`LOCAL LENS`。

它额外保留：

```text
Success → Process Audit
```

以及 failure analysis 的 operational routing，因此不应删除。

---

# 7. F7 — Evidence → Evaluator Stack

Canonical owner：Ch15。

## Ch15 §15.0 五层评价系统

当前：

```text
Evidence
→ Evaluator
→ Raw Judgment
→ Derived Label
→ Final Decision / Metric

Gold / Anchor
→ Meta-evaluation
```

判定：`REPLACE WITH F7`。

原因：这是 F7 的直接章节版，二者认知任务完全相同。

建议：

```text
§15.0 直接引用 F7
正文继续解释五层结构和 meta-evaluation
```

其他局部 evaluation examples / routing / hierarchy：`KEEP`。

---

# 8. F8 — Benchmark / Evaluation Protocol

Canonical owner：Ch16。

Ch16 没有另一张竞争性的总 Mermaid；主要通过：

```text
Benchmark / Protocol / Run / Report
Population Accounting
Paired / Matched
Budget Matching
Statistics
Claim Scope
```

逐层展开。

判定：`ADD POINTER`。

F8 作为 Ch16 的 book-level visual index 最合适，不需要为了“统一”重写 Ch16。

Ch16 内部 Trigger→Generator→Selector→Outcome 等局部文字链属于具体 evaluation lens，应 `KEEP`。

---

# 9. F9 — Data Flywheel

Canonical owner：Ch17。

Ch17 §17.0 与 §17.27 有文字闭环：

```text
Sense
→ Triage
→ Diagnose
→ Abstract
→ Acquire
→ Construct Supervision
→ Validate
→ Deploy
→ Refresh
↺
```

没有另一张 Mermaid 与 F9 竞争。

判定：

```text
F9 → canonical visual
Ch17 textual loop → KEEP
Ch17 top → ADD POINTER
```

原因：文字链是阅读节奏的一部分，F9 是全书视觉资产，二者不冲突。

---

# 10. F10 — Data Strategy / Portfolio / ROI

Canonical owner：Ch18。

Ch18 主要由：

```text
Capability Portfolio table
ROI / MU heuristic formulas
Build / Buy / Generate / Mine
Core / Repair / Frontier / Safety / Exploration
Scale / Maintain / Stop / Retire
```

构成，没有竞争性的总图。

判定：`ADD POINTER`。

局部表格和公式：`KEEP`。

---

# 11. F11 — Governance / Lineage DAG

Canonical owner：Ch19。

## Ch19 §19.5 Lineage DAG

当前：

```text
Raw Trajectory
→ Canonical Trajectory
→ Human / Judge Labels
→ Adjudicated Label
→ Curated Asset
→ Preference / Regression Views
→ Training / Eval Runs
→ Model
```

判定：`REPLACE WITH F11`。

原因：F11 的唯一职责就是固定全书 canonical Lineage DAG；继续保留第二套总 DAG 容易在未来字段扩展时出现视觉漂移。

正文应保留：

```text
Lineage 为什么是 DAG
正向影响追踪
反向根因追踪
```

仅把总图交给 F11。

其他 Raw/Canonical/Derived 层级、Re-score/Re-run/Replay 等文字结构：`KEEP`。

---

# 12. F12 — Data Production System

Canonical owner：Ch22。

Ch22 §22.0 当前用文字链：

```text
Production Contract
→ Job / Shard / Queue
→ Workers
→ Raw Artifact
→ Normalize / Validate
→ Verifier / Judge / Human
→ Gate / Router
→ Dataset Builder
→ Handoff
```

没有竞争 Mermaid。

判定：

```text
F12 → canonical visual
Ch22 textual pipeline → KEEP
Ch22 top → ADD POINTER
```

Job State Machine、Retry、Idempotency、Backpressure 等全部属于 local lens，应保留。

---

# 13. F13 — Monitoring / Drift Diagnostic Tree

Canonical owner：Ch23。

Ch23 使用：

```text
Monitoring Stack
Raw / Fixed-mix Metric
Drift taxonomy
Drift Response Playbook
Control-loop stability
```

没有竞争性的总 Mermaid。

判定：`ADD POINTER`。

F13 负责：

```text
Metric changed
→ Traffic / Measurement / Infrastructure / Capability 分流
```

Ch23 负责每个 branch 的细节。

---

# 14. F14 — Operating Model + Capability Map

Canonical owner：Ch24–25。

## Ch24

当前用文本流程：

```text
Sense a Problem
→ Data Problem Gate
→ Assign Owner
→ Diagnose
→ Choose Intervention
→ Pilot
→ Confirm
→ Scale
→ Deploy
→ Monitor
→ Maintain / Retire
```

判定：`KEEP + ADD POINTER`。

它是 Operating lifecycle 的简洁 textual summary，不与 F14 的 organization + capability view 冲突。

## Ch25

当前包含：

```text
八域 Capability Map
端到端调用链
Problem Routing Tree
Data Intervention Tree
30-minute Diagnosis
```

判定：

```text
Eight-domain map → KEEP
Problem / Data Intervention Trees → KEEP
F14 → ADD POINTER as visual synthesis
```

原因：Ch25 是 practitioner operating manual，需要更细的调用表；F14 只承担书级视觉收束。

---

# 15. 高置信整改项

最终只有三处应优先 `REPLACE`：

```text
R1
Ch14 §14.0 Failure Taxonomy 总图
→ F6 Credit → Failure Causal Map

R2
Ch15 §15.0 五层评价系统总图
→ F7 Evidence → Evaluator Stack

R3
Ch19 §19.5 Lineage DAG
→ F11 Governance / Lineage DAG
```

其他：

```text
LOCAL LENS
→ 保留

没有图但对应 Master Figure
→ ADD POINTER
```

这说明现有章节图示并没有严重“图泛滥”问题；真正的问题只是 3 个 canonical relation 出现了双重视觉定义。

---

# 16. 推荐的章节接入格式

统一采用：

```markdown
> **Master Figure：** [F6 — Credit → Failure Causal Map](./figures/F6_Credit_to_Failure_Causal_Map.md)
>
> 本章 Lens：`Symptom → Root Cause → Failure Owner → Intervention Routing`。
```

原则：

```text
Master Figure
= stable relation

Chapter Lens
= current analytical focus
```

不要：

```text
把 Master Figure 全文复制到每一章
```

也不要：

```text
为了链接 Master Figure，把有独立信息的局部图全部删掉
```

---

# 17. Figure Acceptance Result

```text
F1–F14 registry
✓ complete

Canonical visual ownership
✓ clear

High-confidence duplicate global diagrams
3

Useful local lenses
majority retained

Next
→ patch R1 / R2 / R3
→ add lightweight F# pointers to canonical owner chapters
→ final continuous read-through checks whether visual references interrupt reading flow
```

最终原则：

> **图的统一不是“所有章节画成同一张图”，而是让全局关系只有一个视觉真源，局部章节只负责放大自己真正需要解释的部分。**
