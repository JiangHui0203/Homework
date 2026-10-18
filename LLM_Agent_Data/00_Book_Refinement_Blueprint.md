# LLM / Agent Data Knowledge System：全书精修施工图

> 状态：**Stable Mother Edition V3.x / Multi-scenario Validation Complete / Maintenance Active**
>
> 适用范围：`LLM_Agent_Data_Knowledge_System.md` + `LLM_Agent_Data/00_...` 至 `25_...` + `cases/` + `case_studies/` + `figures/` + `visual_derivatives/`
>
> 当前原则：**不再继续扩主骨架。完整定义只出现一次；跨项目稳定结构进入 Core；只对特定场景成立的结构进入 Optional Extension；一次性细节留在 Case / Walkthrough。**

---

# 0. 当前施工状态

```text
Content Expansion
✓

Architecture Audit / 7-Part IA
✓

Ch0–25 Structural Editing
✓

Canonical Glossary / Concept Ownership
✓

Canonical Case System
✓ C1–C5 + stable variant IDs

Master Figure System
✓ F1–F14

Retrieval Indexes
✓ Concept / Role / Problem / Interview / Checklist

Verification Baseline
✓ Formula / metric / denominator / terminology / link / continuous-readthrough audits

Reference Layer
✓ Source policy + canonical external anchors

Visual Derivatives
✓ Level A D1 Publication / D2 Presentation / D3 Quick-reference

Practical Use Layer
✓ Use Map / Playbooks / Artifact Kit / Case Studies

Scenario Packs
✓ Interview Pack
✓ Project Starter Pack

Scenario Validation
✓ Round 1: Interview + K17 selective reasoning
✓ Round 2: Production Incident + Evaluator Drift + Trajectory Curation
✓ Promotion Test: Human Gold + Synthetic Production

Entry Router
✓ PROMOTED TO CORE

Conditional Extensions
✓ E2 A10-I Production Incident — optional
✓ E3 A5-M Measurement Bridge — optional
✓ E4 A6-C Curation Contract — optional
○ E5 A5-H Human Annotation / Gold Contract — candidate only
```

当前一句话：

> **这套系统已经从“内容完整”走到“跨多类真实任务仍能保持边界”的阶段；当前工作模式从建设新架构切换为真实使用、证据刷新和有限条件下的 extension promotion。**

---

# 1. Stable Asset Layers

## Layer A — Canonical Knowledge

```text
00_Glossary_and_Notation.md
00_Concept_Index.md
Ch0–25
```

负责：

```text
Definition
Ownership
Boundary
Theory / Method Structure
```

固定规则：

```text
Canonical Chapter = Definition
Dependent Chapter = Application + Link
```

---

## Layer B — Canonical Cases

```text
00_Canonical_Casebook.md
00_Case_Integration_Index.md
cases/README.md
cases/C1...C5.md
```

负责：

```text
Stable Scenario
Variant Identity
Cross-chapter Reuse
Experimental Semantics
```

Case ID 是语义锚点，不只是文档标题。

---

## Layer C — Master Figures

```text
00_Master_Figure_System.md
figures/README.md
figures/F1...F14.md
```

14 张图保持单一 visual ownership：

```text
F1  Learning System Overview
F2  Data Object & Learning Signal Evolution
F3  Reasoning State Decision Stack
F4  Agent Task–Environment–Trajectory
F5  Trajectory Anatomy
F6  Credit → Failure Causal Map
F7  Evidence → Verifier → Grader → Judge
F8  Benchmark / Evaluation Protocol
F9  Data Flywheel
F10 Data Strategy / Portfolio / ROI
F11 Governance / Lineage DAG
F12 Data Production System
F13 Monitoring / Drift Diagnostic Tree
F14 Operating Model + Capability Map
```

后续不再因为“还可以画一张”新增 Master Figure。

---

## Layer D — Retrieval

```text
00_Role_Index.md
00_Problem_Index.md
00_Interview_Index.md
00_Checklist_Index.md
00_Practical_Use_Map.md
```

负责把：

```text
角色
问题
面试
执行
现实任务
```

路由回 canonical assets。

---

## Layer E — Practical Execution

```text
00_Practical_Playbooks.md
00_Practical_Artifact_Kit.md
case_studies/
00_Interview_Pack.md
00_Project_Starter_Pack.md
```

职责严格分开：

```text
Starter Pack
= 从哪个入口开始、什么时候做什么

Playbook
= 某类问题怎样走

Artifact Kit
= 最终留下什么可审计对象

Case Study
= 一条完整真实路径怎样连起来

Interview Pack
= 怎样直接回答、展开和接追问
```

---

## Layer F — Reference / Evidence

```text
00_Reference_Source_Policy.md
00_Canonical_References.md
```

固定区分：

```text
External Literature
≠ Internal Research Evidence
≠ Canonical Teaching Case
≠ Engineering Convention
```

相似主题不能替内部 frozen result 补出处。

---

## Layer G — Visual Derivatives

```text
00_Publication_Visual_Derivative_Spec.md
00_Visual_Release_Manifest.md
visual_derivatives/
```

固定：

```text
Canonical Mermaid
= Semantic Source of Truth

D1 Publication
= Book / PDF View

D2 Presentation
= Progressive Reveal View

D3 Quick-reference
= Fast Recall View
```

Derivatives 不能为了漂亮改变 canonical relation。

---

## Layer H — Scenario Validation

```text
00_Scenario_Pack_Stress_Test.md
00_Scenario_Pack_Stress_Test_Round_2.md
00_Scenario_Pack_Promotion_Test.md
00_Scenario_Pack_Candidate_Extensions.md
```

这一层不定义新知识，只回答：

```text
现有框架在真实压力下哪里会坏？
哪些补丁值得进入 Core？
哪些只能保持按需 Extension？
```

---

# 2. 当前 Core：不是一条流水线，而是五入口、一汇合

三轮异质压力测试后，Project Starter 的稳定结构是：

```text
                 ┌─ Failure-led
                 ├─ Monitoring-led
Entry Router ────┼─ Hypothesis-led
                 ├─ Evaluation-led
                 └─ Asset-led / Curation-led
                        ↓
              Relevant Contract + Evidence
                        ↓
                Controlled Change
                        ↓
                    Evaluation
                        ↓
                     Decision
                        ↓
               Monitoring / Re-entry
```

对应常见入口：

```text
Failure-led
→ A1 / A2 / A3 / A4

Monitoring-led Incident
→ A10

Hypothesis-led
→ A1 / A2-S / A7

Evaluation-led
→ A5

Asset-led / Curation-led
→ A11 / Source Lineage
```

固定边界：

```text
Artifact Chain
≠ 所有项目必须顺序填满 A1–A10
```

真正不变的是：

```text
Identity
Evidence
Comparison Boundary
Decision
Lineage
```

---

# 3. Scenario Validation Record

## Round 1 — Interview + Selective Reasoning

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
Population + Cost Ledger
```

因此 A2 增加 A2-S selective extension；A7 明确：

```text
Full / Screened / Eligible / Triggered / Intervened / Observed
Online / Offline / Forbidden Leakage
Per-trigger / Incremental / E2E / Worst-case Cost
```

---

## Round 2 — Heterogeneous Projects

测试：

```text
Production Incident
Judge / Evaluator Drift
500k Trajectory Curation
```

发现：

```text
Monitoring Alert 应先从 A10 进入
Last-known-good + Change Ledger 很关键
Evaluator upgrade 是 measurement intervention
Old↔New score 需要 bridge
Re-score ≠ Historical Decision Rewrite
Source Asset ≠ Dataset View
Quality Gate = Router
Raw Count ≠ High-value Yield
Dataset Size ≠ Training Exposure
```

---

## Promotion Test — Human Gold + Synthetic Production

结果：

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

Synthetic Production 同时提供了重要反例：

```text
不需要新建 A12 Synthetic Card
```

已有：

```text
A6 + A9 + A11 + A7
```

已经能保持 ownership 清晰。

这说明成熟不是继续加模板，而是知道什么时候**不要加**。

---

# 4. Core / Extension Promotion Policy

以后任何新结构先问四次：

```text
Q1
已有 canonical owner 能解释吗？
→ 能：link / apply，不新建定义

Q2
它是否跨多类真实项目反复出现？
→ 否：留在 Case / Walkthrough

Q3
它是否只对一类 project type 有意义？
→ 是：Optional Extension

Q4
缺少它是否会稳定造成 denominator / leakage / audit / decision ambiguity？
→ 是，并经异质压力验证：才考虑 Promote Core
```

Promotion 最低标准：

```text
[ ] 至少跨 2 个额外真实项目仍然有用
[ ] 与现有 ownership 不冲突
[ ] 能消除真实 ambiguity / audit failure
[ ] 不迫使无关项目填大量 N/A
[ ] 外部读者可以独立使用
```

核心原则：

> **Core 小而稳定，Extension 条件明确，Case 保留局部复杂度。**

---

# 5. Verification / Release State

V3.0 Release Readiness 已完成以下基线验收：

```text
Formula / Metric Audit
✓

Research Number / Denominator Scope Audit
✓

Terminology / Style Audit
✓

Visual Canonicalization
✓

Canonical file / high-risk link checks
✓

Continuous Read-through Ch0–25
✓
```

详见：

```text
00_Verification_Log.md
00_Link_Audit.md
00_Final_Readthrough_Log.md
00_Terminology_Style_Audit.md
00_Figure_Integration_Audit.md
00_Release_Readiness.md
```

当前核心 release blocker：

```text
0
```

---

# 6. Known Non-blocking Verification Items

## P1 — More Thinking Source Anchor

当前处理：

```text
More Thinking Is Not Always Better
→ Internal Research Example
```

已有数字可以在明确内部证据口径下使用，但在正式 paper / arXiv 或 frozen internal result summary 出现前，不升级成 fully sourced publication fact。

禁止：

```text
猜作者
猜 arXiv
猜完整副标题
拿主题相似论文冒充来源
```

---

## P1 — Exhaustive Rendered Heading-anchor Proof

已经通过：

```text
canonical file targets
high-risk navigation paths
case / figure integration paths
```

尚未机械化证明：

```text
每一个 GitHub rendered Markdown heading ID
```

因此只声明已经验证到的范围，不写成“全仓所有深层 anchor 均机械化验证”。

---

# 7. Maintenance Mode — CURRENT

现在不再以：

```text
“还能补什么章节 / 图 / Pack / Artifact？”
```

作为主要问题。

当前循环改成：

```text
Real Use
↓
Observe Friction / Ambiguity
↓
Classify
├─ content bug
├─ retrieval bug
├─ missing evidence
├─ scenario-specific extension
└─ genuinely cross-project primitive
↓
Minimal Fix
↓
Stress Test
↓
Promote / Keep Optional / Reject
```

优先真实使用场景：

```text
Interview / Defense
Research Project
Production Incident
Evaluator Upgrade
Large-scale Curation
Human Annotation
Synthetic Production
```

---

# 8. What Should NOT Happen Next

不要因为当前体系成熟就继续：

```text
新增更多总框架
新增平行 Glossary
新增另一套 Case ID
新增另一套 Artifact numbering
为每个领域单独造一个 Card
把 optional extension 塞进所有主模板
```

尤其禁止：

```text
“这个主题重要”
⇒
“它应该有一个新的 canonical artifact”
```

重要性不等于新的 ownership 必要性。

---

# 9. 下一阶段的真正任务

## A. Use-driven Maintenance

真实使用 Interview Pack / Project Starter Pack / Artifact Kit，记录：

```text
哪里需要额外解释？
哪里填不下真实项目？
哪里出现重复字段？
哪里容易造成错误 claim？
```

## B. Extension Validation

重点观察：

```text
E5 Human Annotation / Gold Contract
```

只有经过真实 annotation / expert-labeling workflow 后，才判断是否升为 optional。

## C. Evidence Freshness

周期检查：

```text
Reference anchors
Internal research source anchors
Benchmark / tool / evaluator versions
Known P1 verification items
```

## D. Drift Control

任何 canonical file 变化后检查：

```text
Dependent Chapters
Cases
Figures
Indexes
Visual Derivatives
Practical Packs
```

避免 derived assets 静默 stale。

---

# 10. Final Completion Standard

当前母本应能快速回答：

```text
一个术语在哪里定义？
一个 Case ID 代表什么稳定语义？
哪张图拥有这组关系的 visual truth？
我是哪个角色，应该读什么？
我遇到这个问题，应该从哪个 Entry 进入？
这是 failure、hypothesis、measurement 还是 asset problem？
哪个 evidence 足以支撑这个 claim？
哪个 population / denominator 在被报告？
哪些信息是 online 合法可见，哪些只能 offline 使用？
Evaluator 换版后历史结果还能不能直接比？
Source Asset 怎样变成可重建 Dataset View？
什么时候应该用 Core Artifact，什么时候加载 Extension？
什么时候 scale、revise、stop 或 rollback？
历史 judgment 被修正后，怎样保留当时 decision 的语义？
```

最终目标已经从：

> **“把知识体系写完整。”**

转为：

> **“让同一套小而稳定的骨架，在不同真实项目中都能把 Identity、Evidence、Comparison、Decision 与 Lineage 管住；需要颗粒时按需展开，不需要时不让复杂度侵入主链。”**
