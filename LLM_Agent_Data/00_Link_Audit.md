# LLM / Agent Data Knowledge System：Cross-reference / Link Audit

> 状态：Round 1–2 Complete / Deep Anchor Audit Pending
>
> 目的：单独记录书内导航、相对路径、Case / Figure / Index target 与 Markdown anchor 的检查范围和证据强度。

---

# 1. 已完成的检查

## 1.1 Default-branch Git Tree

状态：`PASS`

通过 GitHub default branch recursive tree 确认当前仓库真实存在：

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

LLM_Agent_Data/cases/README.md
LLM_Agent_Data/cases/C1...C5.md

LLM_Agent_Data/figures/README.md
LLM_Agent_Data/figures/F1...F14.md
```

因此可以把 Git tree 当成：

> **Target-path truth table。**

---

## 1.2 Ch0–25 Header Navigation

状态：`PASS`

已逐章读取 Header，检查：

```text
所属体系
前置章节
关联章节
编辑基础设施
```

确认：

```text
Ch10 → 11 → 12 → 13 → 14 → 15 → 16
```

以及：

```text
Ch17 → 18 → 19 → 20 → 21 → 22 → 23 → 24 → 25
```

前置链没有断裂。

原先 Ch1–3 嵌在 root file 的旧结构已退出，当前 Header 使用独立 Ch1–3 文件。

---

## 1.3 Old Plan Name Search

状态：`PASS WITH SEARCH LIMITATION`

检查旧计划标题：

```text
第 17 章 LLM-as-a-Judge
第 20 章 Data Flywheel
```

没有发现残留。

但需要注意 GitHub Code Search 对该仓库部分 query 返回：

```text
incomplete_results = true
```

因此：

> **0 search result 只能作为辅助证据，不能作为“绝对不存在”的唯一证明。**

最终判断以实际文件读取 + Git tree 为主。

---

# 2. Case / Figure / Index Target Audit

## Cases

状态：`PASS`

```text
C1–C5 file paths all exist
cases/README.md exists
00_Canonical_Casebook.md exists
00_Case_Integration_Index.md exists
```

## Figures

状态：`PASS`

```text
F1–F14 file paths all exist
figures/README.md exists
00_Master_Figure_System.md exists
```

## Retrieval Indexes

状态：`PASS`

```text
00_Concept_Index.md
00_Role_Index.md
00_Problem_Index.md
00_Interview_Index.md
00_Checklist_Index.md
```

all exist on default branch.

---

# 3. Markdown Anchor Audit

状态：`PARTIAL / PENDING DEEP AUDIT`

Path 存在不等于：

```text
file.md#heading-slug
```

的 heading slug 一定正确。

当前已知一个典型位置：Ch4 Header 仍使用：

```text
./00_Canonical_Casebook.md#c4--reasoning-continue--repair
```

Casebook 中对应 Heading 存在，但 GitHub 自动生成 anchor 的 slug 规则属于渲染层；当前工具不能直接对 rendered DOM 的 `id` 做全仓库验证。

由于现在已经有独立：

```text
./cases/C4_Reasoning_Continue_Repair.md
```

最终编辑 pass 更推荐把 fragile heading-anchor link 改成 stable case-file path。

原则：

```text
Stable File Link
>
Auto-generated Heading Anchor
```

如果 anchor 只是为了跳到同一文件小节，且阅读收益明确，则可保留。

---

# 4. 为什么没有声称“100% 全仓库 Broken-link Checker 已运行”

尝试把 default branch public snapshot 下载到本地运行 Markdown parser，但当前执行环境外网 DNS 不可用。

GitHub connector 可以：

```text
读取文件
读取 tree
搜索代码
```

但当前没有提供：

```text
bulk materialize whole repository into local filesystem
```

同时 Code Search 结果存在 `incomplete_results=true`。

因此当前最严谨的说法是：

```text
Path inventory
→ 全量 default-branch tree 已检查

Chapter header navigation
→ Ch0–25 已逐章检查

New Case / Figure / Index targets
→ 已核对存在

All body links / rendered heading anchors
→ 尚未形式化全量解析
```

不把“当前工具做不到的部分”写成已经完成。

---

# 5. Final Link Pass 计划

最终连续阅读阶段处理：

```text
1. Stable file path first
2. Replace fragile casebook anchors with direct case files where useful
3. Check Next Chapter links
4. Check Master Figure references
5. Check Case IDs and variant links
6. Check root landing page paths
7. Check heading anchors only where actually needed
```

如未来获得可 materialize 的完整 repo snapshot，再补运行自动 Markdown link checker。

---

# 6. Current Conclusion

当前可以有把握地说：

> **书级信息架构和主要导航路径是完整的；新增的 Chapter / Case / Figure / Index target 都真实存在；目前尚未宣称所有正文深链和 GitHub-rendered anchors 已被自动形式化验证。**

这比写：

```text
“所有链接检查通过”
```

更准确，也更符合本书自己的 Evaluation / Claim Scope 纪律。
