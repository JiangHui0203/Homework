# LLM / Agent Data Knowledge System：Verification Log

> 状态：Active Verification Ledger
>
> 目的：记录全书在 Cross-reference、Fact、Citation、Number、Formula 与 Research Claim Scope 上的核验结果。所有验证结论都写清“检查了什么、证据是什么、还有什么没检查”，避免把部分审计写成全量保证。

---

# 0. Verification Scope

当前分为五类：

```text
A. Navigation / Cross-reference
B. Bibliographic / External Fact
C. Internal Research Example
D. Number / Formula / Metric
E. Final Continuous Read-through
```

状态：

```text
PASS
FIXED
NEEDS VERIFY
OUT OF SCOPE
```

---

# 1. Navigation / Cross-reference Audit

## 1.1 Ch0–25 Header Links

状态：`PASS — Round 1`

已逐章检查：

```text
所属体系
前置章节
关联章节
编辑基础设施
```

覆盖：

```text
Ch0
Ch1–3
Ch4–9
Ch10–16
Ch17–25
```

确认：

1. 旧版 Ch1–3 嵌在 root file 的结构已经退出；当前章节链接均指向独立文件。
2. `Ch10 → Ch11 → Ch12 → Ch13 → Ch14 → Ch15 → Ch16` 主前置链完整。
3. `Ch17 → Ch18 → Ch19 → Ch20 → Ch21 → Ch22 → Ch23 → Ch24 → Ch25` 主前置链完整。
4. Header 中出现的关联章节文件均存在。
5. 搜索旧计划名称：
   - `第 17 章 LLM-as-a-Judge`
   - `第 20 章 Data Flywheel`
   未发现残留。

限制：

> 本轮是 header / navigation-level audit；正文深处的所有 Markdown link 尚未逐链接解析，因此不能声称“全仓库 0 broken link”。

下一步：正文链接 / anchor deep audit。

---

## 1.2 Canonical Case Paths

状态：`PASS`

已确认存在：

```text
cases/README.md
cases/C1_Order_Refund_Agent.md
cases/C2_Calendar_Meeting_Agent.md
cases/C3_File_Repository_Agent.md
cases/C4_Reasoning_Continue_Repair.md
cases/C5_Code_Execution_Agent.md
```

并建立：

```text
00_Canonical_Casebook.md
00_Case_Integration_Index.md
```

稳定 ID 示例：

```text
C1-VB
C2-F3
C3-F5
C4-SC
C5-F2
```

---

## 1.3 Master Figure Paths

状态：`PASS`

已完成并登记：

```text
F1–F14
```

入口：

```text
00_Master_Figure_System.md
figures/README.md
```

---

## 1.4 Retrieval Index Paths

状态：`PASS`

```text
00_Concept_Index.md
00_Role_Index.md
00_Problem_Index.md
00_Interview_Index.md
00_Checklist_Index.md
```

---

# 2. Bibliographic / External Fact Audit

## 2.1 More Thinking Is Not Always Better

状态：`SAFE IN CURRENT TEXT / FULL BIBLIOGRAPHIC VERIFY STILL PENDING`

背景：早期草稿曾存在一个未核验的完整副标题风险。

当前 Ch4 已修改为：

```text
More Thinking Is Not Always Better
```

并显式注明：

```text
本节是具体研究实例，不是通用定义。
正式书稿发布前，论文完整题名与 bibliographic metadata
统一在引用审计阶段核验。
```

2026-10-18 公开 Web 检索没有建立“此前那个完整副标题”与该项目的一一对应公开记录，因此当前做法是：

> **不猜副标题；只使用已经确定的主标题 / 项目名。**

这比写入一个未经确认的正式题名更安全。

待后续核验：

```text
正式 title
authors
venue / arXiv
publication year
```

如果该项目尚未公开，则保持：

```text
Research Project / Research Example
```

而不是伪造 bibliographic entry。

---

# 3. Internal Research Example Audit

## 3.1 More Thinking Research Example

状态：`CLAIM SCOPE CONTROLLED`

允许写：

```text
固定模型 / benchmark / protocol 下的观察结果
Wrong→Right / Right→Wrong
state-dependent continuation / stopping framing
当前实验数字
```

不应无证据升级为：

```text
所有模型都符合
所有任务都符合
一般理论已经被证明
```

推荐标签：

```text
Research Example
Current Experimental Evidence
```

---

## 3.2 RoTFuse / K17 Research Example

状态：`CLAIM SCOPE CONTROLLED`

允许作为方法例子说明：

```text
Risk Trigger
Same-prefix Candidate
Selector
Rescue / Harmful
Cost / Coverage
```

需要保持：

```text
具体实验观察
≠ 通用结论
```

特别是：

```text
low confidence ≠ wrong ≠ worth repairing
candidate exists ≠ selector can identify it
```

这些是方法论区分；具体效果数字则必须绑定对应实验协议。

---

# 4. Pending Verification Queue

## P0 — Navigation

```text
[ ] Deep body-link audit
[ ] Markdown anchor audit
[ ] Next-chapter link audit
[ ] Case / Figure links inside chapters after integration
```

## P1 — Bibliography

```text
[ ] More Thinking formal metadata
[ ] 文中其他显式 paper / method citation
[ ] arXiv / venue / author spelling
```

## P1 — Numbers

```text
[ ] Research example metrics
[ ] benchmark counts
[ ] percentages / token costs
[ ] sample totals / cohort denominators
```

## P1 — Formula / Metric

```text
[ ] probability / loss notation
[ ] ROI formulas
[ ] effective sample size expression
[ ] paired / coverage metric notation
[ ] drift metric names / semantics
```

## P2 — Terminology

```text
[ ] industry term capitalization
[ ] Pretraining / Post-training spelling
[ ] LLM-as-a-Judge hyphenation
[ ] Agent-visible State / World State consistency
```

---

# 5. Verification Discipline

1. **没核验就写 NEEDS VERIFY，不靠记忆补 bibliographic detail。**
2. **Internal research result 可以保留，但必须绑定 protocol / version / denominator。**
3. **Research Example 不自动升级成 Universal Claim。**
4. **Corrected label 不改写 historical decision history。**
5. **Web fact 和 repository/internal fact 分开记录来源。**
6. **部分审计不写成全量保证。**

---

# 6. Current Status

```text
Architecture
✓

Concept Ownership
✓

Cases
✓

Figures
✓

Retrieval Indexes
✓

Header / Navigation Audit Round 1
✓

Deep Link Audit
→ pending

Bibliographic / Number / Formula Audit
→ active next

Final Continuous Read-through
→ final stage
```

一句话：

> **现在的目标已经不是继续增加“看起来正确的内容”，而是逐项证明：链接是真的、题名是真的、数字有来源、公式语义一致、研究结论没有越过证据边界。**
