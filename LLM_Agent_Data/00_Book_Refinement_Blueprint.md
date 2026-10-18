# LLM / Agent Data Knowledge System：全书精修施工图

> 状态：**Structure / Cases / Figures / Retrieval Indexes Complete — Verification Active**
>
> 适用范围：`LLM_Agent_Data_Knowledge_System.md` + `LLM_Agent_Data/00_...` 至 `25_...` + `cases/` + `figures/`
>
> 原则：**完整定义只出现一次；dependent chapter 只讲当前场景的应用。Concept、Case、Figure、Index 四套 canonical asset 必须保持稳定语义。**

---

# 0. 当前施工状态

```text
Content Expansion
✓

Architecture Audit
✓

7-Part Information Architecture
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
✓ Concept Index
✓ Role Index
✓ Problem Index
✓ Interview Index
✓ Checklist Index

Current
→ Cross-reference / Broken-link Audit
→ Fact / Paper / Number / Formula Verification

Then
→ Figure integration audit for old local diagrams
→ Final continuous read-through
→ Derived editions
```

当前一句话：

> **知识内容、结构、案例、视觉和检索坐标系已经完成；现在进入“证明所有链接、事实、数字和引用都站得住”的验证阶段。**

---

# 1. Canonical Assets

## Concepts

```text
00_Glossary_and_Notation.md
00_Concept_Index.md
```

## Cases

```text
00_Canonical_Casebook.md
00_Case_Integration_Index.md
cases/README.md
cases/C1...C5.md
```

## Figures

```text
00_Master_Figure_System.md
figures/README.md
figures/F1...F14.md
```

## Retrieval

```text
00_Role_Index.md
00_Problem_Index.md
00_Interview_Index.md
00_Checklist_Index.md
```

---

# 2. Final Book Structure

```text
Overview
└── Ch0

Part I — Learning Signals
└── Ch1–5

Part II — Data Acquisition & Selection
└── Ch6–9

Part III — Agent World & Diagnosis
└── Ch10–14

Part IV — Measurement
└── Ch15–16

Part V — Data Optimization & Lifecycle
└── Ch17–21

Part VI — Data Operations
└── Ch22–24

Part VII — Synthesis
└── Ch25
```

---

# 3. Canonical Concept Ownership

```text
Ch1  Data Objects
Ch2  Training Stages
Ch3  Preference / Reward
Ch4  Correctness / Risk / Recoverability / Repairability / Selectability
Ch5  Agent Experience Basics
Ch6  Human Annotation
Ch7  Synthetic Generation
Ch8  Candidate Pool / Oracle / Selector
Ch9  Hard Case / Frontier / Acquisition
Ch10 Task Contract
Ch11 Tool / Harness / Environment
Ch12 Typed Trajectory
Ch13 Credit
Ch14 Failure Diagnosis
Ch15 Evidence / Evaluator
Ch16 Benchmark / Protocol
Ch17 Flywheel
Ch18 Data Strategy / ROI
Ch19 Governance / Lineage
Ch20 Curation / Mixture
Ch21 Data Intervention
Ch22 Production
Ch23 Monitoring / Drift
Ch24 Organization Operating Model
Ch25 Practitioner Operating System
```

规则：

```text
Canonical Chapter = Definition
Dependent Chapter = Application + Link
```

---

# 4. Master Figure System

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

后续不再无限新增 Master Figure，只做：

```text
KEEP
REPLACE WITH MASTER
KEEP AS LOCAL LENS
```

的旧图审计。

---

# 5. Retrieval System

现在全书支持五种主要入口：

```text
Chapter Navigation
→ 我想系统学

Concept Index
→ 我想查一个概念

Role Index
→ 我做这个岗位该学什么

Problem Index
→ 我现在遇到这个问题先查什么

Interview / Checklist
→ 我要表达 / 执行
```

Case / Figure 则作为横向坐标：

```text
Case
→ 同一个真实问题如何跨章流动

Figure
→ 多个概念在一张图上如何连接
```

---

# 6. Verification Plan — CURRENT

## A. Cross-reference / Broken-link Audit

检查：

```text
旧 Ch1–3 root links
旧计划章节名称
不存在的文件名
改名后的相对路径
Case / Figure links
Next Chapter links
```

## B. Fact / Citation Audit

检查：

```text
论文正式题名
作者 / 年份 / arXiv
Benchmark 正式名称
模型名称
实验数字
公式符号
行业术语
```

## C. Research Claim Scope

重点：

```text
More Thinking
RoTFuse / K17
其他真实 research example
```

统一区分：

```text
Research Example
Current Experimental Evidence
General Methodological Principle
Universal Claim
```

前三者可以写，第四类需要足够证据。

---

# 7. Final Read-through Checklist

最终连续阅读时检查：

```text
章节开头是否准确定位？
前置 / 关联章节是否真实存在？
同一术语是否语义稳定？
案例 ID 是否漂移？
Master Figure 是否和正文一致？
重复解释是否重新长回来？
Research Example 是否越界成普遍结论？
章节结尾是否正确衔接下一章？
Landing Page 是否反映真实结构？
索引是否真的能把人送到正确位置？
```

---

# 8. Derived Editions

母本验证完成后再生成：

```text
Interview Quick Reference
Project Checklist Edition
Learning Path Edition
```

原则：

> **衍生版只压缩母本，不创造新的事实源。**

---

# 9. Final Completion Standard

最终应快速回答：

```text
一个术语在哪里定义？
一个问题应该先排查哪几层？
一个岗位应该读什么？
一个 Case ID 具体代表什么？
哪张图能最快解释关系？
一个 failure 如何变成 data experiment？
一个结论使用了哪套 data / judge / protocol？
一个历史标签修正后应该 re-score 还是 re-run？
什么时候 scale？什么时候 stop？
什么时候旧数据 / benchmark 已经 stale？
```

最终目标：

> **每个概念有唯一归属，每个章节有明确职责，每个案例有稳定 ID，每张图有单一认知任务，每个问题有检索入口，每个结论能找到证据。**
