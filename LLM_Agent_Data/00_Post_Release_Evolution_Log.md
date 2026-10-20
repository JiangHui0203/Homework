# LLM / Agent Data Knowledge System：Post-release Evolution Log

> 基线发布：[`Stable Mother Edition — V3.0`](./00_Release_Readiness.md)
>
> 状态：`V3.x Compatible Evolution / Maintenance Log`
>
> 原则：**V3.0 Release Readiness 是历史发布快照，不因后续兼容演进而回写其当时结论。本文件只记录 V3.0 之后新增或修正的 practical、visual、reference、scenario-validation 与 maintenance 资产。**

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
又增加 / 修正了哪些可调用能力？
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

后续维护已进一步固定：

```text
A1–A11
= composable artifact catalog
≠ mandatory linear workflow
```

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

因此 A1–A11 Artifact Catalog 不再被解释成：

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

# 12. Maintenance Sweep — Single Source + Multi-entry Alignment

本轮不增加新的知识层，只处理稳定以后才暴露的维护 drift。

## 12.1 Canonical Case 单一真源

发现：

```text
00_Canonical_Casebook.md
+
cases/C*.md
```

早期曾同时维护接近完整的 Case Spec，形成双真源风险。

处理后：

```text
00_Canonical_Casebook.md
= Registry / Stable Invariants / Variant Namespace

cases/C*.md
= Full Case Contract / Detailed Variants

00_Case_Integration_Index.md
= Chapter → Case / Variant Routing

case_studies/
= End-to-end Walkthrough
```

固定：

> **Canonical Case 只有一个完整语义真源；Registry 负责定位，不复制完整 spec。**

## 12.2 C2 Frozen Case Clock

C2 原来使用：

```text
Monday / Tuesday / Friday
```

相对时间，且 Casebook 旧副本残留工具名 typo。

现冻结为：

```text
Case clock
= 2026-10-19 09:00 Asia/Shanghai

“明天下午三点”
= 2026-10-20 15:00 Asia/Shanghai

“周五下午三点”
= 2026-10-23 15:00 Asia/Shanghai
```

并固定：

```text
Relative Time
→ resolve against frozen Case Clock
≠ runtime current date
```

## 12.3 Case Integration Routing

`00_Case_Integration_Index.md` 已从旧语义：

```text
Casebook / Case File
= stable scenario / stable contract
```

收紧为：

```text
Casebook
= registry

Case File
= full contract

Chapter
= analytical lens
```

并把 C2 frozen clock 纳入 Variant Integrity Rules。

## 12.4 Checklist 多入口对齐

`00_Checklist_Index.md` 不再默认所有项目都从 failure / Data Problem 开始。

新增 Entry Router checklist：

```text
Failure-led
Monitoring-led
Hypothesis-led
Evaluation-led
Asset-led / Curation-led
```

同时回写：

```text
Selector
→ Population / Information / Cost Ledger

Evaluator
→ Measurement Bridge on version change

Monitoring
→ Last-known-good / Change Ledger / Containment

Curation
→ Source Lineage / Rebuildable Dataset View
```

## 12.5 Artifact Kit 工件目录化

`00_Practical_Artifact_Kit.md` 现在明确：

```text
A1–A11
= composable artifact catalog
≠ mandatory sequential workflow
```

关键修正：

```text
A1 project_origin
+ monitoring_led
+ asset_led

A5
+ measurement_bridge_ref

A10
+ last-known-good
+ raw-vs-fixed-mix
+ containment

A11
+ source_asset / dataset_view / build_recipe_ref
```

P2 大批 trajectory 路径改为：

```text
A11 source truth
→ batch evidence / curation
→ downstream validation
```

而不是先强制制造 A1 / A4。

## 12.6 Playbook 入口一致性

`00_Practical_Playbooks.md` 保留 P1–P7，但显式标记 Entry：

```text
P1 Failure-led
P2 Asset-led / Curation-led
P3 Hypothesis / Production-led
P4 Evaluation-led
P5 Hypothesis-led Selective Research
P6 Data Strategy
P7 Monitoring-led
```

P4 新增 Measurement Bridge；P7 新增 last-known-good / Change Ledger / containment；Universal Exit Condition 不再要求所有项目都有 Root Cause 或 Data Intervention。

---

# 13. Maintenance Sweep — Naming / Status / High-frequency Entry Sync

这一轮继续只处理 drift，不扩知识层。

## 13.1 Master Figure System 状态同步

修正早期 stale wording：

```text
“下一阶段进入 publication / slides / quick-reference”
```

因为 Level A 实际已经完成：

```text
D1 Publication SVG
D2 16:9 Progressive Reveal Storyboard
D3 Quick-reference Cards
```

现在固定：

```text
Level A
→ D1 / D2 / D3 released

Level B
→ semantic / production-refined complete
→ derivative 按真实需求生成
```

不为了“14 张都整齐”机械制造 Level B derivative。

## 13.2 Figure Canonical Naming

F7 在 Master Figure Registry 中曾被简写为：

```text
Evidence → Evaluator Stack
```

现统一回 canonical title：

```text
Evidence → Verifier → Grader → Judge
```

Figure Index / file / Master Registry 使用同一名称。

同时明确：

```text
Figure Presentation Kit
= scene selection / talk track / common misread

D2 Storyboard
= actual 16:9 frame / reveal implementation
```

## 13.3 Visual Freshness Re-check

重新读取 F1 / F4 / F6 / F8 / F9 / F14 当前 source blob SHA。

结果：

```text
6 / 6
current source SHA
== Visual Release Manifest recorded SHA
```

因此 Level A D1 / D2 / D3 当前仍为：

```text
CURRENT
```

未触发 stale review。

## 13.4 Reference Policy 命名同步

`A1–A11 Artifact Chain` 的旧工程措辞已收紧为：

```text
A1–A11 Artifact Catalog / stable Artifact IDs
```

并明确：

```text
Composable Artifact Catalog
≠ Mandatory Sequential Chain
```

S3 Teaching Case 示例也完整列为 C1–C5，避免入口层对 C2 形成无意缺席。

## 13.5 Terminology Audit 状态关闭

`00_Terminology_Style_Audit.md` 的内容早已验收 PASS，但文件头仍停在：

```text
Acceptance Cleanup / Language Consistency
```

现同步为：

```text
PASS — Acceptance Baseline / Maintenance Reference
```

不改变任何 canonical terminology rule。

## 13.6 Condensed Guide 高频入口同步

精简版原来仍残留：

```text
三篇 Practical Study
C1 / C3 / C4
```

以及 failure-led-only 的 30-minute Diagnosis、`开始项目 → Checklist` 的旧路由。

现同步为：

```text
C1 / C3 / C4 / C5
```

并将 quick diagnosis 改为：

```text
Entry + Scope
→ Contract + Evidence
→ Entry-specific Branch
→ Intervention Gate
→ Minimum Controlled Change
→ Decision
```

项目入口统一回：

```text
Project Starter Pack
```

而：

```text
Checklist
= execution review
Artifact Kit
= auditable outputs
Playbook
= action sequence
```

面试入口统一回：

```text
Interview Pack
```

---

# 14. Maintenance Sweep — Retrieval Index Alignment

这一轮只检查四个 Retrieval Index 的 ownership、命名、stable ID 与 V3.x practical routing，不新增章节、Pack、Figure 或 Artifact ID。

## 14.1 Concept Index — audit only

`00_Concept_Index.md` 对照：

```text
Canonical Glossary
Canonical Case Registry
current Figure IDs
```

未发现需要立即修改的高置信 canonical owner / terminology / Case ID / Figure ID drift。

因此本轮保持原文，不为了表面统一改写跨章节 context notes，也不把 retrieval compression 变成第二份 glossary。

## 14.2 Role Index — role compression ≠ project workflow

`00_Role_Index.md` 原来的“优先章节”容易被误读为项目执行 chain。

现明确：

```text
Role Index
= role-specific learning compression
≠ project workflow
≠ canonical ownership rewrite
```

真实项目入口统一回：

```text
Project Starter Pack / Entry Router
```

并保持五入口：

```text
Failure-led
Monitoring-led
Hypothesis-led
Evaluation-led
Asset-led / Curation-led
```

同时把已经存在的 Practical Studies 接回高频角色入口：

```text
Agent Data / Agent Evaluation
→ C1 / C3 walkthroughs

Evaluation / Benchmark Researcher
→ C5 Executable Truth / Verifier Coverage

Reasoning / Test-time / Selector Research
→ C4 Reasoning Intervention
```

没有强行给 C2 新造 walkthrough。

## 14.3 Problem Index — symptom-first scope + entry-specific routes

`00_Problem_Index.md` 保留 symptom-first 职责，但现在显式声明：

```text
Problem Index
→ most often Failure-led / Monitoring-led

Hypothesis-led / Evaluation-led / Asset-led
→ 不需要伪造 symptom
→ 直接进入 Project Starter Pack
```

同步四个高置信 practical route：

```text
Judge score ↑ / real success 不涨
→ Evaluation-led / A5 / optional A5-M

Online success rate ↓
→ Monitoring-led / A10 / optional A10-I

Evaluator update 改变历史 score
→ A5-M Measurement Bridge / re-score semantics

Production throughput 高但 usable yield 低
→ Asset-led / A11 / A6-C / A7
```

并保持：

```text
Monitoring Alert ≠ Model Regression
Evaluator Upgrade ≠ Capability Improvement
Source Asset ≠ Dataset View / Training Data
```

## 14.4 Interview Index — first-answer ownership restored

`00_Interview_Index.md` 原来的“通用答题骨架”曾把：

```text
Define → Diagnose → ... → Flywheel
```

放在第一层，容易与已经稳定的 Interview Pack ownership 冲突。

现固定：

```text
Interview Pack
= Direct Answer / Stop Depth / Evidence Provenance

Interview Index
= 27-question retrieval / deeper expansion
```

七步框架保留，但明确为：

```text
deep-expansion map
≠ first-answer protocol
≠ mandatory chain
```

“如果让我负责一个数据项目”也先判断五入口，再汇合到：

```text
Relevant Contract + Evidence
→ Controlled Change
→ Evaluation
→ Decision
→ Monitoring / Re-entry
```

## 14.5 Verification scope

本轮回验范围包括：

```text
C1 / C2 / C3 / C4 / C5 registry IDs
F1–F14 current naming references used by the four Indexes
Project Starter Pack Entry Router
Interview Pack ownership
existing C1 / C3 / C4 / C5 Practical Study paths
```

没有：

```text
重写 V3.0 Release Readiness
扩 Ch26+
新增 C2 walkthrough
新增 A12 / P8
扩 Level B derivatives
重新引入 F6 / F7 / F11 competing global diagrams
声称 exhaustive rendered deep-heading validation
```

本轮仍属于：

```text
V3.x Compatible Evolution / Maintenance
```

---

# 15. Maintenance Sweep — High-frequency Navigation Alignment

本轮只检查四个最高频入口：

```text
LLM_Agent_Data_Knowledge_System.md
00_Overview.md
00_Practical_Use_Map.md
00_Condensed_Guide.md
```

目标不是继续润色，而是确认第一次进入系统时不会被旧 routing 带偏。

## 15.1 Landing page — first-entry ownership corrected

`LLM_Agent_Data_Knowledge_System.md` 原来的 `Interview / Execution Retrieval` 把：

```text
Interview Index
Checklist Index
```

同时解释成面试、项目立项和 30-minute diagnosis 的入口，已经落后于当前职责分工。

现明确：

```text
Interview Index
= 27-question retrieval / deeper expansion

Checklist Index
= stage-specific execution review / omission prevention

Interview first entry
= Interview Pack

Project first entry
= Project Starter Pack

30-minute diagnosis
= Condensed Guide §13 / Practical Use Map
```

没有改变 Index / Pack 的内部语义，只修正 landing routing。

## 15.2 Overview — remove failure-led-only implication

`00_Overview.md` 结尾原来把成熟能力压成：

```text
懂模型为什么错
→ 把错误变成数据
→ 证明数据有用
```

这对 Failure-led 项目成立，但不足以覆盖已经稳定的：

```text
Monitoring-led
Hypothesis-led
Evaluation-led
Asset-led / Curation-led
```

现保留 Learning System 主线，同时显式说明：

```text
不同 Entry
→ Relevant Contract + Evidence
→ Correct Intervention Owner
→ Controlled Evaluation
→ Decision
→ Monitoring / Re-entry
```

因此 Overview 不再暗示所有项目必须先拥有 failure 或最终都落成 Data Intervention。

## 15.3 Practical Use Map / Condensed Guide — audit only

两份文件已经正确反映：

```text
five-entry model
Interview Pack first
Project Starter Pack first
A1–A11 composable catalog
C1 / C3 / C4 / C5 Practical Studies
A5-M / A10-I / A6-C conditional extensions
Reference / Visual / Scenario routes
```

未发现需要修改的高置信 drift，因此保持原文。

这属于有意的高频 compression，不为了四文件形式对称做无意义改写。

## 15.4 Scope guard

本轮没有：

```text
扩 Ch26+
新增 Pack / Figure / Template
新增 C2 walkthrough
新增 A12 / P8
改变 canonical concept ownership
扩 Level B derivatives
重写 V3.0 Release Readiness
声称 exhaustive rendered deep-heading validation
```

本轮仍属于：

```text
V3.x Compatible Evolution / Use-driven Maintenance
```

---

# 16. Maintenance Sweep — Reference Freshness & Version Discipline

本轮只审：

```text
00_Canonical_References.md
00_Reference_Source_Policy.md
```

目标是更新已有 anchor 的 bibliographic freshness 与 Claim ↔ Source 边界，不扩大 bibliography。

## 16.1 Existing anchor venue metadata refreshed

外部核验后，补齐或纠正已有 canonical anchor 的正式 venue metadata：

```text
R01 Deep RL from Human Preferences
→ NIPS / NeurIPS 2017 venue status confirmed

R04 Let's Verify Step by Step
→ ICLR 2024

R05 Self-Instruct
→ ACL 2023 Long Papers

R08 Judging LLM-as-a-Judge
→ NeurIPS 2023 Datasets and Benchmarks Track

R10 AgentBench
→ ICLR 2024

R12 SWE-bench
→ ICLR 2024
```

这些变化只更新 bibliography / source status：

```text
Reference ID 不变
Claim Role 不变
Chapter Routing 不变
```

本轮没有新增 R16 或其他 Rxx。

## 16.2 Source priority becomes version-aware

原规则：

```text
formal venue
>
project / repo
>
arXiv
```

在版本内容完全等价时成立，但对：

```text
full technical report
vs
later concise formal report
```

可能过强。

现固定先判断：

```text
Claim Coverage
+
Version Equivalence
```

只有同一 bibliographic object 且目标 claim coverage 基本等价，才机械优先正式 venue。

HELM 作为明确示例保留：

```text
2022 full technical report
≠ 2023 formal concise report
```

后者可核对 formal publication identity，但不能静默替换 full report 承担全部 benchmark / protocol claim。

## 16.3 More Thinking — identity anchor ≠ quantitative evidence anchor

本轮找到公开作者主页，可核对：

```text
NLPCC
More Thinking Is Not Always Better:
Structural and Semantic Factors of Complex Reasoning Tasks in LLMs

Hui Jiang / Shizhu He / Kang Liu / Jun Zhao
```

因此 title / authors / NLPCC identity 已有公开 professional listing。

但该页面不提供固定深度结果、population、protocol 或完整论文证据，因此：

```text
public identity listing
≠ evidence for 69.04 / 74.09 / 70.97
```

固定深度定量 claim 继续保持：

```text
Internal Research Example
+ SOURCE ANCHOR PENDING for quantitative evidence
```

没有用外部相似主题论文替代内部 evidence anchor。

## 16.4 Scope guard

本轮没有：

```text
新增 Rxx
替换 foundational anchor
改变 reference claim role
把 internal claim 升级成 public evidence
扩 related-work bibliography
重写 V3.0 Release Readiness
改变 canonical concept / Case / Figure ownership
```

本轮仍属于：

```text
V3.x Compatible Evolution / Reference Maintenance
```

---

# 17. Maintenance Sweep — Reference Usage / Claim–Source Alignment

本轮反向审计高引用章节实际如何消费 Reference Layer：

```text
Ch4
Ch7
Ch15
Ch16
Ch19
Ch20
Ch23
```

目标不是增加 citation density，而是检查：

```text
External Anchor
是否承担了超出原论文的证明责任？

Book Canonical Operating Model
是否被误写成外部论文定义？

Benchmark / Publication Identity
是否被误当成 universal validity？
```

## 17.1 Ch4 — source boundary repaired

发现两处明确 stale usage：

```text
“正式书稿发布前再核验 bibliographic metadata”
```

已经落后于当前 Reference Layer；同时 R04 与本章状态级五分法之间缺少显式 ownership boundary。

现修正为：

```text
R04 — Let's Verify Step by Step
→ external anchor for Outcome vs Process Supervision
→ step-level feedback / process reward context

Correctness / Risk / Recoverability / Repairability / Selectability
Continue / Stop
Keep / Branch / Repair
→ book-defined canonical operating distinctions
→ not attributed back to R04
```

More Thinking 研究实例也同步当前 source status：

```text
public title / authors / NLPCC identity
→ checkable

fixed-depth quantitative results / protocol
→ Internal Research Example
→ SOURCE ANCHOR PENDING for quantitative evidence
```

因此：

```text
Public identity listing
≠ Claim-bearing quantitative evidence
```

## 17.2 Ch7 / Ch15 / Ch16 / Ch19 / Ch20 / Ch23 — audit only

完整复核后，没有发现需要为了 Reference Layer 强行改正文的高置信 over-attribution。

这些章节当前已经通过章节定位、canonical owner 与跨章边界明确表达：

```text
Ch7
Experience Synthesis / failure-driven / trajectory / environment synthesis
→ book extension beyond R05 Self-Instruct

Ch15
Evidence → Evaluator → Judgment → Label
Evidence First, Judge Second
Verifier / Grader / Judge operating boundary
→ book canonical model
R08 只承担公开 LLM-as-a-Judge / bias / agreement context
R12 只承担 executable-evaluation context

Ch16
Benchmark ≠ Protocol ≠ Run ≠ Report
Population Accounting / Denominator Discipline
Stable Ruler + Moving Frontier
→ book canonical evaluation decomposition
R09–R15 作为 external benchmark / protocol / contamination / freshness anchors
不拥有这些 canonical definitions

Ch19
Identity / Provenance / Lineage / Versioning
Historical Decision / Re-score / Re-run / Replay
→ book governance model
R13 / R14 不承担全部治理 taxonomy 定义权

Ch20
Decision-level / Family-level Dedup
Dataset Size ≠ Training Exposure
→ book curation operating model
R14 只承担 contamination research anchor

Ch23
Monitoring ≠ Diagnosis
Stable Ruler + Moving Frontier as monitoring usage
Judge / Tool / Harness / Environment Drift decomposition
→ book monitoring operating model
R15 只提供 fresh / objective / contamination-aware benchmark example
```

因此本轮保持这些章节原文。

固定判断：

> **“没有逐段写 Rxx”不等于缺失；只要 canonical ownership 已清楚、没有外部论文被过度归因，就不为了形式完整把母本改造成 literature survey。**

## 17.3 Scope guard

本轮没有：

```text
新增 Rxx
增加 bibliography 数量
改变已有 reference claim role
给每章机械添加 citation box
把 book canonical taxonomy 外包给 external paper
把 More Thinking 定量结果升级成 public evidence
重写 V3.0 Release Readiness
新增 Ch / Pack / Figure / Artifact ID
```

本轮仍属于：

```text
V3.x Compatible Evolution / Claim–Source Maintenance
```

---

# 18. Maintenance Sweep — Practical Evidence Provenance

本轮只审五个高频 practical assets：

```text
case_studies/C1_End_to_End_Walkthrough.md
case_studies/C1_Artifact_Pack.md
case_studies/C3_Permission_Harness_Ownership_Walkthrough.md
case_studies/C4_Reasoning_Intervention_Walkthrough.md
case_studies/C5_Executable_Truth_Verifier_Coverage_Walkthrough.md
```

目标不是重写 walkthrough，而是保证任何人把其中一段摘出去时，仍能回答：

```text
这是 Teaching Case？
Internal Research Evidence？
External Literature？
还是 Engineering Convention？
```

## 18.1 Common drift — canonical disclaimer ≠ evidence provenance

五个 asset 原本都已声明：

```text
walkthrough / artifact pack
≠ canonical definition owner
```

但这只能解决语义 ownership，不能自动解决 evidence provenance。

例如：

```text
“线上 failure”
“Incident A / B / C”
production_mined
model_x / harness_v1
200 screened states
Candidate A hidden tests FAIL
```

在脱离上下文后二次引用时，仍可能被误读为：

```text
真实 production incident
真实内部 run
真实 benchmark result
```

因此本轮为五个 asset 增加显式 Evidence provenance boundary。

## 18.2 C1 Walkthrough — simulated production workflow

现在固定：

```text
C1 Walkthrough
= S3 TEACHING + S4 Engineering / Editorial Convention
```

订单 1847、失败轨迹、artifact / lineage IDs 与 production / monitoring 场景都属于 teaching construction。

正文开头也从：

```text
“这个案例从一条很小的线上 failure 开始”
```

收紧为：

```text
“这个教学案例模拟从一条很小的线上 failure 开始”
```

因此：

```text
Production-shaped scenario
≠ Production evidence
```

## 18.3 C1 Artifact Pack — filled field ≠ executed project

`C1_Artifact_Pack.md` 现在明确：

```text
TEACHING
```

以下内容都是 reference fill-in values：

```text
PI-C1-001 / EXP-C1-001 等 ID
model_x / harness_v1
snapshot / transaction names
source channels
seeds: 3
example configs
```

不能因为字段已经填满，就推断对应训练 / 评测 / production run 已经执行。

A6 的：

```text
production_mined / synthetic / rollout
```

也显式标成 illustrative source channels，而不是该 Pack 的真实 provenance claim。

继续保持：

```text
PENDING / TBD / <value>
= no result evidence
```

## 18.4 C3 Walkthrough — Incident label is pedagogical

C3 的：

```text
Incident A
Incident B
Incident C
```

现在显式归类为 S3 Teaching Case 中的 constructed variants。

因此：

```text
Tool backend failure
Harness false-success observation
Blind retry
```

是 case-world facts，用于稳定：

```text
Failure Layer ≠ Failure Owner
Tool Truth ≠ Harness Observation
Transport Failure ≠ Action Failure
```

它们不是生产事件频率或某产品事故报告。

permission / retry / verification route 则属于 S4 operating convention，不应被引用为 empirical guarantee。

## 18.5 C4 Walkthrough — research-shaped teaching ≠ K17 report

C4 是本轮最重要的 provenance boundary。

固定：

```text
C4 Practical Walkthrough
= TEACHING
```

它确实吸收内部 reasoning-intervention 研究中常见的：

```text
trigger
same-prefix candidate
oracle
selector
Rescue / Harmful
coverage / cost
```

问题形状，但：

```text
Walkthrough
≠ RoTFuse / K17 experiment report
```

只有挂接 frozen：

```text
config / protocol
population / denominator
result summary
artifact path / version
```

的内容才能升级成 S2 Internal Research Evidence。

特别固定：

```text
§11 200 / 50 / 20 / 11 / 6
§12 +0.5pt / 5× / +0.4pt / 1.2×
= teaching-only illustration
```

真实 K17 threshold、population、Rescue / Harmful / Net、cost 必须回到 authoritative research artifacts。

## 18.6 C5 Walkthrough — executable benchmark context ≠ C5 evidence

C5 现在明确：

```text
normalize_date
Candidate A / B / C / D
public / hidden test outcomes
V1–V3 verifier
C5-R1 / C5-R2 runtime
repair trajectory
= TEACHING objects
```

R12 SWE-bench 等 external executable-evaluation anchor 只能提供：

```text
public benchmark / executable evaluation context
```

不能证明：

```text
C5 task itself
C5 candidate outcomes
C5 verifier result
```

同时把示例：

```text
execution_cost_ms: 0
```

改为：

```text
execution_cost_ms: null
```

避免 placeholder 看起来像真实测量值。

## 18.7 Fixed provenance discipline

本轮固定四条复用规则：

```text
S3 Teaching Case
→ 可以稳定 relation / boundary / workflow
→ 不能证明真实发生频率或性能提升

S4 Engineering Convention
→ 可以定义本书 operating practice
→ 不能伪装成 empirical outcome

S1 External Literature
→ 只支撑论文实际研究过的 claim
→ 不会自动验证本书 teaching case

S2 Internal Research
→ 定量 claim 必须回到 frozen artifact / protocol / denominator
→ research-shaped walkthrough 不等于 research evidence
```

## 18.8 Scope guard

本轮没有：

```text
改变 C1 / C3 / C4 / C5 canonical semantics
新增 C2 walkthrough
新增 Case / Variant ID
新增 Artifact ID
新增 Rxx
把 teaching case 升级成 internal evidence
把 external benchmark 反向当作 teaching-case proof
修改 V3.0 Release Readiness
声称 exhaustive rendered validation
```

本轮仍属于：

```text
V3.x Compatible Evolution / Evidence Provenance Maintenance
```

---

# 19. Maintenance Sweep — Practical Reuse Provenance

本轮继续检查 Teaching Case 在高频复用入口里有没有被二次包装成个人项目 / 实验 evidence。

审计范围：

```text
00_Interview_Pack.md
00_Interview_Index.md
00_Condensed_Guide.md
00_Role_Index.md
00_Problem_Index.md
00_Project_Starter_Pack.md
```

## 19.1 Interview Pack — teaching rehearsal ≠ personal project

Interview Pack 原本已经拥有 Evidence Provenance discipline：

```text
Public Literature
My Project / Frozen Result
Canonical Teaching Case
Hypothetical Design
```

但“2–3 个深度 Case”局部仍直接列：

```text
C1 / C3 / C4 / C5
```

如果脱离 §0.1 阅读，仍可能被误用成个人项目素材。

现明确：

```text
C1 / C3 / C4 / C5
= Canonical Teaching Case / Practical Study
= rehearsal asset
≠ personal project evidence
```

尤其：

```text
C4
→ 可用于组织 reasoning-intervention 表达
→ 不能直接充当 RoTFuse / K17 实验证据
```

## 19.2 Condensed Guide — remove “真实 case” ambiguity

Condensed Guide 的面试入口原来写：

```text
概念边界
真实 case
可验证 workflow
```

随后立即推荐：

```text
C1 / C3 / C4 / C5 Walkthrough
```

这会制造最直接的 provenance ambiguity。

现收紧为：

```text
概念边界
真实项目 / 研究 evidence
可验证 workflow
```

并明确：

```text
C1 / C3 / C4 / C5 Walkthrough
= S3 Teaching Case / rehearsal asset
≠ “我做过”的 project / research evidence
```

面试回答真实经历时，必须另接 frozen project / research artifact。

## 19.3 Project Starter Pack — routing anchor ≠ project evidence

Starter Pack 的五类启动路径使用：

```text
C1 / C3
C4
C5
```

作为典型 project route 的结构锚点。

现显式固定：

```text
Case IDs
= S3 routing anchors
≠ symptom / trajectory / population / result / cost evidence
```

真实项目仍必须回到：

```text
A1 / A3 / A7 / A8
```

或：

```text
S2 Internal Research artifacts
```

Path B 额外固定：

```text
C4 teaching schema
≠ RoTFuse / K17 result source
```

真实 K17 threshold、population、Rescue / Harmful / Net 与 cost 仍必须来自 frozen config / protocol / result artifact。

## 19.4 Interview Index / Role Index / Problem Index — audit only

三份文件当前只是：

```text
题型 retrieval
role-specific learning compression
symptom-first diagnostic routing
```

它们引用 Case 的用途是定位概念与排查结构，没有把 Case 写成个人经历、真实事故或 empirical result。

同时 Evidence Provenance 的口头表达 ownership 已明确归：

```text
Interview Pack
```

因此本轮不在三个 Index 中重复添加免责声明，避免 provenance rule 再次多处维护。

## 19.5 Fixed reuse boundary

以后任何入口复用 Practical Study，默认遵守：

```text
Teaching Case
→ 可回答“怎么理解 / 怎么分析 / 怎么设计”

Personal / Internal Evidence
→ 才可回答“我实际做了什么 / 得到什么结果”
```

二者可以在同一个回答中相邻出现，但必须有显式话语切换与独立 evidence provenance。

## 19.6 Scope guard

本轮没有：

```text
改变 C1–C5 semantics
新增 Case / Walkthrough / Artifact / Rxx
改写 Interview Index ownership
把 Case Study 变成 project report
把 K17 evidence 迁入 Teaching Case
重写 V3.0 Release Readiness
```

本轮仍属于：

```text
V3.x Compatible Evolution / Practical Reuse Provenance Maintenance
```

---

# 20. Maintenance Sweep — Practical Execution Semantics

本轮审计：

```text
00_Practical_Playbooks.md
00_Practical_Artifact_Kit.md
00_Checklist_Index.md
00_Practical_Use_Map.md
```

目标不是增加新的流程，而是检查：

```text
placeholder / example value
是否被读成已执行事实？

optional / composable contract
是否被读成 mandatory process？

项目阶段 / 决策阶段
是否被误注册成新的 Entry？
```

## 20.1 Five-entry origin model re-locked

发现两类高置信 drift：

```text
Artifact Kit A1
project_origin 仍残留 strategy_led

Playbooks
P3 使用 Hypothesis / Production-led
P6 使用 Data Strategy 作为 Entry 标签
```

这些都与当前唯一的五入口 practical model 不完全一致。

现固定：

```text
Failure-led
Monitoring-led
Hypothesis-led
Evaluation-led
Asset-led / Curation-led
```

具体修正：

```text
A1 project_origin
→ 移除 strategy_led

P3 Synthetic Data
→ 通常 Hypothesis-led
→ 若从既有 seed / source assets 起步，则 Asset-led / Curation-led
→ Production-led 不是独立 canonical Entry

P6 Data Investment Decision
→ 不是新的 project origin
→ 是 A7 之后的 Decision-stage continuation
→ 继承上游项目原有 Entry
```

因此固定：

```text
Project Origin
≠ Workflow Stage
≠ Decision Stage
```

## 20.2 Artifact Kit — template value ≠ project fact

Artifact Kit 现在显式定义模板语义：

```text
<...>
= placeholder / allowed shape
≠ recorded fact

null / [] / UNKNOWN / NOT YET ESTABLISHED
= legal unresolved / absent state
```

枚举候选也不再默认表示“全部已选中”。

高风险字段同步收紧：

```text
A1 suspected_layers
→ one-or-more choice set

A3 agent_visible
→ <true|false>

A5 abstain_supported
→ <true|false>

A6 source_experience
→ one-or-more choice set

A6 learning_signal
→ one-or-more choice set

A10 suspected_drift
→ one-or-more choice set
```

固定：

```text
Copied Template
≠ Executed Artifact

Filled Field
≠ Evidence

Artifact becomes evidence-bearing
only when linked to real trace / config / run / source asset
```

## 20.3 Playbooks — illustrative trigger ≠ measured result

Playbooks 中的：

```text
10万 / 50万 / 100万 trajectories
quality_score = 0.83
“剩下 42 万条”
100 万 synthetic data
+1.2 pt
```

统一标记为 illustrative trigger / teaching value。

同时固定：

```text
Produced Artifacts
= expected evidence / decision-object categories as applicable
≠ every line requires a separate file
```

证据不足时：

```text
UNRESOLVED / suspected / stop at Gate
```

优于：

```text
为了闭环形式而伪造 Root Cause / Report / Decision
```

P1 因此将：

```text
Root Cause / Owner
```

收紧为：

```text
Root Cause / Owner Status
(confirmed / suspected / unresolved)
```

## 20.4 Checklist — green checklist ≠ valid project

Checklist Index 现在明确：

```text
[ ]
= 当前项目需要解析的问题
≠ unconditional mandatory requirement
```

合法状态包括：

```text
completed with evidence
N/A + rationale
UNRESOLVED / pending
```

禁止为了“全绿”伪造：

```text
artifact
metric
root cause
experiment result
```

## 20.5 Practical Use Map — teaching walkthrough ≠ real project record

Use Map 原来仍有：

```text
“我想看真实项目到底怎么走完”
→ Practical Case Studies
```

这与 §18–19 已固定的 Teaching provenance 冲突。

现改为：

```text
“我想看一个完整项目结构怎样被教学化走通”
→ Practical Case Studies
```

并明确：

```text
C1 / C3 / C4 / C5
= S3 Teaching Case / walkthrough
≠ production incident
≠ personal project evidence
≠ internal experiment result
```

对应的“实战案例”措辞也收紧为：

```text
教学演练
```

## 20.6 Scope guard

本轮没有：

```text
新增 Entry
新增 P8
新增 A12
改变 A1–A11 stable IDs
改变 P1–P7 stable Playbook set
改变 C1–C5 semantics
新增 Case / Figure / Rxx
把 optional extension 提升成 mandatory Core
修改 V3.0 Release Readiness
```

本轮仍属于：

```text
V3.x Compatible Evolution / Practical Execution Semantics Maintenance
```

---

# 21. Final Principle

```text
Release Snapshot
保留历史

Evolution Log
记录兼容演进

Stress Test
发现真实摩擦

Promotion Gate
控制 Core 膨胀

Maintenance Sweep
消除 drift / duplicate truth / stale execution semantics
```

> **稳定母本不是停止生长，而是让生长有 lineage、有边界、有 promotion rule；让维护优先消除漂移而不是制造新层，并且永远不靠重写历史来制造“当前一致”。**