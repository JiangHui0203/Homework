# LLM / Agent Data Knowledge System：Verification Log

> 状态：`Stable Mother Edition Acceptance — Core Checks Complete`
>
> 目的：记录全书在 Cross-reference、Fact、Citation、Number、Formula、Visual Integration、Terminology 与 Research Claim Scope 上的核验结果。所有结论都明确“检查到哪里、证据是什么、还有什么没有形式化证明”，避免把部分审计写成全量保证。

---

# 0. Verification Scope

本轮覆盖：

```text
A. Navigation / Cross-reference
B. Bibliographic / External Fact
C. Internal Research Example
D. Number / Formula / Metric
E. Visual Integration
F. Terminology / Style
G. Final Continuous Read-through
```

状态词：

```text
PASS
FIXED
CLOSED
NEEDS SOURCE ANCHOR
DEFERRED / NON-BLOCKING
OUT OF SCOPE
```

---

# 1. Navigation / Cross-reference Audit

## 1.1 Ch0–25 Header / Chapter Chain

状态：`PASS`

已逐章检查：

```text
所属体系
前置章节
关联章节
编辑基础设施
下一章交接
```

主链：

```text
Ch0 → 1 → 2 → 3 → 4 → 5
→ 6 → 7 → 8 → 9
→ 10 → 11 → 12 → 13 → 14
→ 15 → 16
→ 17 → 18 → 19 → 20 → 21
→ 22 → 23 → 24 → 25
```

唯一在连续通读中发现的文字接缝：

```text
Ch18 → Ch19
```

已经修复：Ch18 结尾明确从 Data Investment / Portfolio Decision 过渡到长期 Data Asset 的 Identity / Provenance / Version / Usage / Lineage 问题，并直接链接 Ch19。

---

## 1.2 Canonical Case Paths

状态：`PASS`

真实存在：

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

Ch4 原先的 fragile Casebook heading anchor 已经改为：

```text
./cases/C4_Reasoning_Continue_Repair.md
```

因此该已知 anchor-risk 已关闭。

---

## 1.3 Master Figure Paths

状态：`PASS`

```text
F1–F14
```

均真实存在，入口：

```text
00_Master_Figure_System.md
figures/README.md
```

本轮高风险接入已双向核对：

```text
Ch14 → F6_Credit_to_Failure_Causal_Map.md
Ch15 → F7_Evidence_Verifier_Grader_Judge.md
Ch19 → F11_Governance_Lineage_DAG.md
```

路径、Figure title 与 canonical owner 均一致。

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

均存在于 default branch。

---

## 1.5 Deep rendered-anchor proof

状态：`DEFERRED / NON-BLOCKING`

当前已验证：

```text
canonical chapter file paths
case direct-file paths
master figure file paths
retrieval index paths
header / next-chapter navigation
final high-risk case / figure integration paths
```

当前没有建立“所有正文 `file.md#heading-slug` 均经过 rendered DOM 级自动解析”的全量证明。

原因：

```text
GitHub Code Search 可能 incomplete indexing
+
当前工具没有全仓库 rendered-heading-ID parser
```

因此只允许声称：

> **主要导航、canonical targets 与高风险接入路径已通过；不把未形式化解析的所有深层 heading anchor 夸大成 100% 自动证明。**

详见 [`00_Link_Audit.md`](./00_Link_Audit.md)。

---

# 2. Bibliographic / External Fact Audit

## 2.1 More Thinking Is Not Always Better

状态：`SAFE AS INTERNAL RESEARCH EXAMPLE / NEEDS SOURCE ANCHOR`

早期草稿存在未核验完整副标题风险。

当前正文只使用：

```text
More Thinking Is Not Always Better
```

并把它明确作为：

```text
Internal Research Example
Current Experimental Evidence
```

公开 exact-title 检索、精确数字 + benchmark + Answerer–Auditor 反查、可访问 GitHub repository 搜索，都没有找到可以安全冒充正式来源的唯一公开记录。

因此固定纪律：

> **不猜副标题，不伪造 authors / arXiv / venue，不用相似论文填空。**

未来建立 Source Anchor 时二选一：

```text
A. 正式 paper / arXiv / published artifact
B. internal frozen experiment summary / result table
```

它不阻塞 Stable Mother Edition 的方法论架构稳定，但阻塞把研究数字升级成 fully sourced publication fact。

---

# 3. Internal Research Example Audit

## 3.1 More Thinking

状态：`CLAIM SCOPE CONTROLLED`

当前允许：

```text
固定模型 / benchmark / protocol 下的观察结果
Wrong → Right / Right → Wrong
state-dependent continuation / stopping framing
当前 fixed-depth 数字
```

不允许无证据升级为：

```text
所有模型普遍成立
所有任务普遍成立
一般理论已经证明
```

---

## 3.2 RoTFuse / K17

状态：`CLAIM SCOPE CONTROLLED`

允许作为方法实例解释：

```text
Risk Trigger
Same-prefix Candidate
Generator / Selector
Rescue / Harmful
Coverage / Cost
```

长期保持：

```text
low confidence ≠ wrong ≠ worth repairing
candidate exists ≠ selector can identify it
```

具体实验数字必须绑定对应 protocol / version / denominator；通用方法论章节不把某次 cohort 数字固化成常识。

---

# 4. Formula / Metric Audit

## 4.1 Ch3 — Pairwise Reward Model

状态：`PASS`

\[
P(y_w\succ y_l\mid x)
=\sigma\left(r_\theta(x,y_w)-r_\theta(x,y_l)\right)
\]

作为经典 Bradley–Terry / logistic pairwise preference 表达语义正确；正文没有把 learned reward 写成客观真值。

---

## 4.2 Ch4 — Recoverability

状态：`FIXED`

已从单步 action existence 改为：

\[
\exists \pi \in \Pi_{allowed}:\; V(s_t;\pi)>V(s_t;\pi_{base})
\]

其中：

```text
π
= 从当前 state 开始的一段允许 future policy / continuation
```

现在准确表达：

> **是否存在更好的未来。**

并与 Repairability / Selectability 保持边界。

---

## 4.3 Ch18 — Data Value / ROI / Marginal Utility

状态：`PASS — heuristic scope explicit`

检查：

\[
V(D\mid M,T,E)
\]

\[
PotentialValue(D)
\approx
Quality\times Relevance\times Novelty\times Learnability\times Applicability
\]

\[
DataROI(D)=\frac{\Delta Utility(D)}{TotalCost(D)}
\]

\[
MU_k=\frac{\Delta Utility}{\Delta Cost}
\]

\[
RiskPriority
\approx
Frequency\times Severity\times Exposure\times Irreversibility
\]

\[
V(A+B)\neq V(A)+V(B)
\]

正文均明确它们是资源配置 / reasoning heuristics 或条件化 notation，不伪装成校准后的统计定律。

---

## 4.4 Ch20 — Mixture / Temperature / Effective Information

状态：`PASS WITH SCOPE CLEAR`

\[
M=\{(D_i,w_i)\}_{i=1}^{K}
\]

\[
p_i\propto n_i^\alpha
\]

并明确：

```text
α = 1  → 原始规模
α < 1 → 提升小 bucket 相对曝光
α = 0 → 接近 source-level uniform
```

当前还使用：

\[
N_{eff}\approx\frac{(\sum_i w_i)^2}{\sum_i w_i^2}
\]

只作为 `Exposure ≠ Independent Information` 的直觉表达，没有包装成适用于任意相关结构的精确有效样本量定律。

---

## 4.5 Ch21 — General Data Intervention

状态：`FIXED`

已从 additive-specific：

```text
B + D
```

改为：

\[
\Delta(I_D;M_0,T,E)
=
Metric(Train(M_0,I_D(B),T),E)
-
Metric(Train(M_0,B,T),E)
\]

统一覆盖：

```text
Add
Remove
Replace
Reweight
Transform
```

---

## 4.6 Ch23 — Raw vs Fixed-mix Metric

状态：`PASS`

\[
S_{obs}=\sum_k p_{new}(k)S_k
\]

\[
S_{fixed}=\sum_k p_{ref}(k)S_k
\]

正文明确：前者反映真实新 task mix 下体验，后者近似隔离 population mix 后观察 slice-level system performance；二者不能互相替代。

---

## 4.7 Formula Audit Summary

```text
Ch3   Pairwise logistic             PASS
Ch4   Recoverability               FIXED
Ch18  ROI / MU / heuristic         PASS
Ch20  Mixture / temperature / Neff PASS with scope clear
Ch21  Data intervention            FIXED
Ch23  Fixed-mix metric             PASS
```

原则：

> **Heuristic 不伪装成定律；承担 canonical definition 的公式必须让 notation 与概念语义一致。**

---

# 5. Research Number / Denominator Audit

## 5.1 More Thinking fixed-depth accuracy

状态：`NEEDS SOURCE ANCHOR — CLAIM SCOPE SAFE`

当前 Ch4 保留：

```text
depth 1 → 69.04%
depth 2 → 74.09%
depth 3 → 70.97%
```

并明确置于具体 Research Example，而不是普遍规律。

数字仍需未来 Source Anchor；在此之前不标成“外部 bibliographic fact 已核验”。

---

## 5.2 早期 More Thinking 其他数字

状态：`NOT PRESENT IN CURRENT BOOK BODY`

当前正文未使用：

```text
5,001 samples
Gap-Audit 76.03% / 2,988 tokens
fixed2 74.09% / 4,678 tokens
```

因此不为已经退出正文的数字制造引用负担。

---

## 5.3 K17 888 / 750 / 138

状态：`NOT PRESENT IN GENERIC Ch16 BODY`

通用章节保留：

```text
Full Population
≠ Triggered Population
```

以及 routing method 的 denominator discipline。

具体 cohort count 留在对应 research artifact，不回填通用教材章节。

---

# 6. Visual Integration Audit

状态：`PASS — CLOSED`

详见 [`00_Figure_Integration_Audit.md`](./00_Figure_Integration_Audit.md)。

三处高置信竞争性全局图已经全部完成接管：

```text
Ch14 §14.0 → F6
✓ DONE

Ch15 §15.0 → F7
✓ DONE

Ch19 §19.5 → F11
✓ DONE
```

大多数章节图保留为：

```text
LOCAL LENS
```

因为它们提供比 Master Figure 更细的局部机制，而不是竞争 global definition。

---

# 7. Terminology / Style Audit

状态：`PASS — ACCEPTANCE LEVEL`

Canonical forms 已固定，例如：

```text
Pretraining
Post-training
LLM-as-a-Judge
Agent-visible State
World State
Environment State
Reasoning State
Working State
Same-prefix
Same-state
Best-of-N
Data Flywheel
Data Curation
Data Intervention
Evaluation Protocol
Claim Scope
```

必须保持的语义边界：

```text
Outcome ≠ Reward ≠ Credit
Error ≠ Failure ≠ Root Cause
Risk ≠ Correctness ≠ Recoverability
Recoverability ≠ Repairability ≠ Selectability
Tool ≠ Harness ≠ Environment
Evidence ≠ Judgment ≠ Label
Benchmark ≠ Protocol ≠ Run ≠ Report
```

未发现高置信 semantic terminology conflict。

不声称做过字符级全仓库 grep proof；验收目标是概念身份与 canonical labels 稳定，而不是机械把普通句子全部 Title Case。

详见 [`00_Terminology_Style_Audit.md`](./00_Terminology_Style_Audit.md)。

---

# 8. Final Continuous Read-through

状态：`PASS — CLOSED`

覆盖：

```text
Ch0–25
```

书级结论：

```text
Chapter Order
✓ PASS

Part Boundaries
✓ PASS

Canonical Ownership Under Continuous Reading
✓ PASS

Cross-chapter Problem Handoff
✓ PASS

Synthesis / Ending
✓ PASS
```

Ch18 → Ch19 的唯一 bridge issue 已修复。

详见 [`00_Final_Readthrough_Log.md`](./00_Final_Readthrough_Log.md)。

---

# 9. Acceptance Queue

## Core / P0

```text
[x] Chapter architecture
[x] Canonical concept ownership
[x] Ch0–25 continuous read-through
[x] Ch18 → Ch19 bridge
[x] Formula / metric audit
[x] Research number / denominator scope audit
[x] Terminology acceptance pass
[x] F6 / F7 / F11 visual canonicalization
[x] Canonical case / figure target existence
[x] Final high-risk case / figure link spot-check
```

**P0 = 0 open items.**

---

## Non-blocking / P1

```text
[ ] More Thinking fixed-depth source anchor
[ ] exhaustive rendered deep-heading-anchor proof if tooling becomes available
```

这两项影响：

```text
citation completeness
formal deep-link proof
```

但不影响：

```text
book architecture
canonical definitions
case / figure IDs
retrieval assets
methodology stability
```

---

# 10. Verification Discipline

1. **没核验就写 NEEDS VERIFY / DEFERRED，不靠记忆补 bibliographic detail。**
2. **Internal research result 可以保留，但必须限定 protocol / version / denominator / claim scope。**
3. **Research Example 不自动升级成 Universal Claim。**
4. **Corrected Label 不改写 Historical Decision。**
5. **Web fact 与 repository/internal fact 分开处理来源。**
6. **部分审计不写成全量保证。**
7. **Heuristic 不伪装成定律；canonical formula 的 notation 必须匹配语义。**
8. **具体 research cohort 数字优先留在 research artifact；通用章节保留可迁移原则。**
9. **Master Figure 是全局视觉真源；局部图只保留真正增加分析粒度的 Lens。**
10. **Stable file target 优先于不必要的 fragile auto-generated heading anchor。**

---

# 11. Current Status

```text
Architecture
✓

Concept Ownership
✓

Cases C1–C5
✓

Master Figures F1–F14
✓

Retrieval Indexes
✓

Header / Navigation
✓

Formula / Metric Audit
✓

Research Number / Denominator Audit
✓ scoped

Figure Integration
✓

Terminology / Style
✓

Continuous Read-through
✓

Final high-risk link spot-check
✓

Core Acceptance Blockers
0
```

一句话：

> **全书的核心架构、概念边界、案例、图示、公式、数字口径、术语、导航与连续阅读已经完成验收；当前只保留两个明确、非阻塞的 P1：More Thinking Source Anchor 与未来可选的 exhaustive rendered-anchor proof。**
