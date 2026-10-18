# LLM / Agent Data Knowledge System：Cross-reference / Link Audit

> 状态：Release Spot-check Complete / Deep Rendered-anchor Audit Deferred
>
> 目的：单独记录书内导航、相对路径、Case / Figure / Index target 与 Markdown anchor 的检查范围和证据强度。

---

# 1. Default-branch Target Inventory

状态：`PASS`

通过 GitHub default branch tree / directory listing 确认当前仓库真实存在：

```text
LLM_Agent_Data_Knowledge_System.md
LLM_Agent_Data/00_Overview.md
LLM_Agent_Data/01...25.md

LLM_Agent_Data/00_Glossary_and_Notation.md
LLM_Agent_Data/00_Canonical_Casebook.md
LLM_Agent_Data/00_Case_Integration_Index.md
LLM_Agent_Data/00_Master_Figure_System.md
LLM_Agent_Data/00_Concept_Index.md
LLM_Agent_Data/00_Role_Index.md
LLM_Agent_Data/00_Problem_Index.md
LLM_Agent_Data/00_Interview_Index.md
LLM_Agent_Data/00_Checklist_Index.md
LLM_Agent_Data/00_Verification_Log.md
LLM_Agent_Data/00_Final_Readthrough_Log.md
LLM_Agent_Data/00_Figure_Integration_Audit.md
LLM_Agent_Data/00_Terminology_Style_Audit.md
LLM_Agent_Data/00_Release_Readiness.md

LLM_Agent_Data/cases/README.md
LLM_Agent_Data/cases/C1_Order_Refund_Agent.md
LLM_Agent_Data/cases/C2_Calendar_Meeting_Agent.md
LLM_Agent_Data/cases/C3_File_Repository_Agent.md
LLM_Agent_Data/cases/C4_Reasoning_Continue_Repair.md
LLM_Agent_Data/cases/C5_Code_Execution_Agent.md

LLM_Agent_Data/figures/README.md
LLM_Agent_Data/figures/F1...F14.md
```

因此可以把 Git tree / directory listing 当成：

> **Target-path truth table。**

---

# 2. Ch0–25 Header / Next-chapter Navigation

状态：`PASS — read-through verified`

已逐章读取 Header，并在 Continuous Read-through 中检查章节交接。

主链确认：

```text
Ch0 → 1 → 2 → 3 → 4 → 5
→ 6 → 7 → 8 → 9
→ 10 → 11 → 12 → 13 → 14
→ 15 → 16
→ 17 → 18 → 19 → 20 → 21
→ 22 → 23 → 24 → 25
```

其中最终唯一的文字接缝：

```text
Ch18 → Ch19
```

已补成稳定 file link：

```text
./19_Data_Governance_Lineage_and_Reproducibility.md
```

---

# 3. Case Target Audit

状态：`PASS`

已确认：

```text
C1–C5 direct case files all exist
cases/README.md exists
00_Canonical_Casebook.md exists
00_Case_Integration_Index.md exists
```

之前 Ch4 使用的 fragile Casebook heading anchor 已经退出；当前直接链接：

```text
./cases/C4_Reasoning_Continue_Repair.md
```

因此已关闭此前的 anchor-risk TODO。

原则继续保持：

```text
Stable File Link
>
Auto-generated Heading Anchor
```

除非 heading-level navigation 确实带来明显阅读价值。

---

# 4. Master Figure Target Audit

状态：`PASS`

F1–F14 路径均存在。

本轮对 3 个 canonical visual handoff 做了双向 spot-check：

```text
Ch14
→ ./figures/F6_Credit_to_Failure_Causal_Map.md
→ target exists
→ F6 canonical owner = Ch13–14

Ch15
→ ./figures/F7_Evidence_Verifier_Grader_Judge.md
→ target exists
→ F7 canonical owner = Ch15

Ch19
→ ./figures/F11_Governance_Lineage_DAG.md
→ target exists
→ F11 canonical owner = Ch19
```

并读回章节正文确认：

```text
relative path spelling
figure title
canonical ownership
chapter lens
```

一致。

因此 Figure Integration Audit 中 3 个高置信 `REPLACE` 项的路径风险已经关闭。

---

# 5. Retrieval Index Targets

状态：`PASS`

```text
00_Concept_Index.md
00_Role_Index.md
00_Problem_Index.md
00_Interview_Index.md
00_Checklist_Index.md
```

均存在于 default branch。

---

# 6. Old-plan / stale-navigation Search

状态：`PASS WITH SEARCH LIMITATION`

曾检查旧计划标题：

```text
第 17 章 LLM-as-a-Judge
第 20 章 Data Flywheel
```

没有发现残留。

但 GitHub Code Search 对部分 query 可能返回 incomplete indexing，因此：

> **0 search result 只作为辅助证据；最终判断以实际文件读取 + Git tree / directory listing 为主。**

---

# 7. Rendered Markdown Anchor Audit

状态：`DEFERRED / NON-BLOCKING`

Path 存在不等于所有：

```text
file.md#heading-slug
```

都经过 rendered DOM 级验证。

当前工具可以可靠检查：

```text
file existence
relative path target
chapter content
GitHub source Markdown
```

但没有全仓库 rendered-heading-ID parser。

因此本书不声称：

```text
“100% all body links / rendered anchors were automatically verified”
```

更准确的 Release Claim 是：

```text
Canonical chapter paths
✓

Case direct-file paths
✓

Master Figure paths
✓

Retrieval index paths
✓

Header / next-chapter navigation
✓

Final high-risk case / figure spot-check
✓

All rendered deep heading anchors
→ not formally exhaustively parsed
```

如未来获得完整 repository snapshot + Markdown link checker，再补机械化全量 anchor pass；它不阻塞当前 Stable Mother Edition。

---

# 8. Release Conclusion

当前可以有把握地说：

> **书级信息架构、章节主导航、Canonical Cases、Master Figures、Retrieval Indexes 与本轮高风险接入路径均已核对真实存在并正确指向；未把工具尚未覆盖的 rendered deep-anchor exhaustive check 夸大成已经完成。**

这与全书自己的 Evaluation / Claim Scope 纪律一致：

> **验证到哪里，就只声明到哪里。**
