# LLM / Agent Data Knowledge System：Post-release Evolution Log

> 基线发布：[`Stable Mother Edition — V3.0`](./00_Release_Readiness.md)
>
> 状态：`V3.x Compatible Evolution / Maintenance Log`
>
> 原则：**V3.0 Release Readiness 是历史发布快照，不因后续兼容演进而回写其当时结论。本文件只记录 V3.0 之后新增的 practical、visual、reference 与 scenario-validation 资产。**

---

# 0. 为什么单独维护 Evolution Log？

发布快照回答：

```text
2026-10-18 发布 V3.0 时
什么已经通过验收？
```

Evolution Log 回答：

```text
V3.0 之后
在不改变 canonical semantics 的前提下
又增加了哪些可调用能力？
```

固定边界：

```text
Post-release Improvement
≠ Historical Release Rewrite
```

这与全书治理原则一致：

```text
New Judgment / New View
≠ Historical Decision Mutation
```

---

# 1. Reference Layer

V3.0 后新增：

```text
00_Reference_Source_Policy.md
00_Canonical_References.md
```

作用：

```text
External Literature
Internal Research Evidence
Canonical Teaching Case
Engineering Convention
```

四类证据正式分开。

当前采用少而稳定的 canonical reference anchors，不追求 bibliography 数量。

每个 anchor 说明：

```text
它能支撑什么
它不能支撑什么
它主要服务哪些章节
```

---

# 2. Visual Derivative Layer

V3.0 后，Level A 六张核心 Master Figure 已形成三种 derivative：

```text
F1  Learning System
F4  Agent World
F6  Credit → Failure
F8  Evaluation Protocol
F9  Data Flywheel
F14 Operating Model
```

派生层：

```text
D1 Publication SVG
D2 16:9 Progressive Reveal
D3 Quick-reference Card
```

新增治理资产：

```text
00_Publication_Visual_Derivative_Spec.md
00_Visual_Release_Manifest.md
visual_derivatives/
```

固定：

```text
Master Figure
= Semantic Source of Truth

Derivative
= Context-specific presentation
```

Derivative 不得为了简洁合并、反转或删除 canonical relation。

---

# 3. Practical Use Layer

新增：

```text
00_Practical_Use_Map.md
00_Practical_Playbooks.md
00_Practical_Artifact_Kit.md
case_studies/
00_Condensed_Guide.md
```

母本从：

```text
“可以系统阅读”
```

扩展为：

```text
“可以从真实问题进入”
```

Artifact Kit 维护 A1–A11：

```text
A1  Problem Intake
A2  Task / Case / Decision-state Contract
A3  Trajectory / Evidence Bundle
A4  Failure / Mechanism Record
A5  Evaluator Contract
A6  Data Intervention
A7  Experiment Card
A8  Decision Memo
A9  Production Handoff
A10 Monitoring Incident
A11 Minimal Lineage Manifest
```

其中 A2-S 为 selective / local intervention optional extension。

---

# 4. Scenario Packs

新增两套场景装配：

```text
00_Interview_Pack.md
00_Project_Starter_Pack.md
```

Interview Pack 负责：

```text
怎么准备
怎么直接回答
怎么控制展开深度
怎么接追问
```

Project Starter Pack 负责：

```text
从哪个项目入口进入
Day 0 / Day 1 / First Week 做什么
什么时候进入 experiment / decision
```

Scenario Pack 不重新定义 canonical concept。

---

# 5. Scenario Stress Test — Round 1

新增：

```text
00_Scenario_Pack_Stress_Test.md
```

测试：

```text
Interview Follow-up Pressure
+
RoTFuse / K17 Selective Reasoning Protocol
```

暴露并回写：

```text
Direct Answer First
Alternative Hypotheses
Evidence Provenance
Quantitative Claim Contract
Stop Depth

Decision-state Contract
Project Origin Mode
Information Boundary
Intervention Type
Population Ledger
Cost Ledger
```

A7 从普通 experiment card 升级为能明确记录：

```text
Full / Screened / Eligible / Triggered / Intervened / Observed
Online / Offline / Forbidden Information
Per-trigger / Incremental / E2E / Worst-case Cost
```

---

# 6. Scenario Stress Test — Round 2

新增：

```text
00_Scenario_Pack_Stress_Test_Round_2.md
```

测试三类异质项目：

```text
Agent Production Incident
Judge / Evaluator Drift
500k Trajectory Curation
```

关键 finding：

```text
Monitoring-led project 可从 A10 进入
Last-known-good + Change Ledger 是 incident attribution 基础
Raw / Slice / Fixed-mix / Frozen Core 回答不同问题
Rollback 是 containment decision，不是 root-cause proof

Evaluator upgrade 是 measurement intervention
Old↔New evaluator 需要 paired bridge
Re-score ≠ Historical Decision Rewrite
Evaluator change 可能进一步改变 data distribution

Asset-led project 可从 A11 / source lineage 进入
Source Asset ≠ Dataset View
Quality Gate = Router
Semantic Similarity ≠ Decision Equivalence
Raw Count ≠ High-value Yield
Dataset Size ≠ Training Exposure
Intrinsic Quality ≠ Downstream Learning Value
```

---

# 7. Candidate Extensions

新增：

```text
00_Scenario_Pack_Candidate_Extensions.md
```

候选：

```text
E1 Entry Router
E2 A10-I Production Incident Extension
E3 A5-M Evaluator Measurement Bridge
E4 A6-C Curation Contract
```

原则：

```text
Use first
Canonize later
```

避免一次压力测试就把主模板无限扩张。

---

# 8. Promotion Test

新增：

```text
00_Scenario_Pack_Promotion_Test.md
```

额外测试：

```text
Human Gold / Annotation Refresh
Synthetic Data Production at Scale
```

Promotion 结果：

```text
E1 Entry Router
→ PROMOTE_CORE

E2 A10-I Production Incident
→ KEEP OPTIONAL

E3 A5-M Measurement Bridge
→ PROMOTE_OPTIONAL

E4 A6-C Curation Contract
→ PROMOTE_OPTIONAL

E5 A5-H Human Annotation / Gold Contract
→ KEEP_CANDIDATE
```

Synthetic Production 同时验证：

```text
A6 + A9 + A11 + A7
```

已经足以承载完整工作流，因此拒绝新增：

```text
A12 Synthetic Card
```

这是一次明确的 anti-bloat decision。

---

# 9. Entry Router Promotion

`00_Project_Starter_Pack.md` 已升级为五入口：

```text
Failure-led
Monitoring-led
Hypothesis-led
Evaluation-led
Asset-led / Curation-led
```

汇合：

```text
Relevant Contract + Evidence
→ Controlled Change
→ Evaluation
→ Decision
→ Monitoring / Re-entry
```

因此 Artifact Chain 不再被解释成：

```text
所有项目必须 A1 → A10
```

而是：

```text
按问题类型选择正确入口
+
共享同一套 Evidence / Comparison / Decision discipline
```

---

# 10. Current Compatibility Judgment

截至当前，以上演进没有改变：

```text
Ch0–25 numbering
Canonical Concept Ownership
C1–C5 stable case semantics
F1–F14 canonical visual relations
Task / Case / Episode / Trajectory object model
Tool / Harness / Environment boundary
Outcome / Reward / Credit boundary
```

因此当前仍属于：

```text
V3.x Compatible Evolution
```

而不是：

```text
Major-version Semantic Rewrite
```

---

# 11. Current Maintenance Mode

现在默认不再问：

```text
“还能加什么层？”
```

而问：

```text
真实使用哪里卡？
卡点属于内容、检索、证据还是场景 contract？
是否已有 canonical owner？
是否只需要 optional extension？
是否跨异质项目重复出现到足以 Promote Core？
```

当前重点观察：

```text
E5 Human Annotation / Gold Contract
More Thinking reliable source anchor
Exhaustive rendered deep-heading proof
Reference / benchmark / evaluator freshness
```

---

# 12. Final Principle

```text
Release Snapshot
保留历史

Evolution Log
记录兼容演进

Stress Test
发现真实摩擦

Promotion Gate
控制 Core 膨胀
```

> **稳定母本不是停止生长，而是让生长有 lineage、有边界、有 promotion rule，并且永远不靠重写历史来制造“当前一致”。**
