# LLM / Agent Data Knowledge System：Verification Log

> 状态：Acceptance Cleanup / Verification Ledger
>
> 目的：记录全书在 Cross-reference、Fact、Citation、Number、Formula、Visual Integration 与 Research Claim Scope 上的核验结果。所有验证结论都写清“检查了什么、证据是什么、还有什么没检查”，避免把部分审计写成全量保证。

---

# 0. Verification Scope

当前分为六类：

```text
A. Navigation / Cross-reference
B. Bibliographic / External Fact
C. Internal Research Example
D. Number / Formula / Metric
E. Visual Integration
F. Final Continuous Read-through
```

状态：

```text
PASS
FIXED
NEEDS REFINE
NEEDS SOURCE ANCHOR
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

1. 旧版 Ch1–3 嵌在 root file 的结构已经退出；当前章节 header 链接均指向独立文件。
2. `Ch10 → Ch11 → Ch12 → Ch13 → Ch14 → Ch15 → Ch16` 主前置链完整。
3. `Ch17 → Ch18 → Ch19 → Ch20 → Ch21 → Ch22 → Ch23 → Ch24 → Ch25` 主前置链完整。
4. Header 中出现的关联章节文件均存在。
5. 搜索旧计划名称：
   - `第 17 章 LLM-as-a-Judge`
   - `第 20 章 Data Flywheel`
   未发现残留。

限制：

> 本轮是 header / navigation-level audit；正文深处的所有 Markdown link 尚未逐链接解析，因此不能声称“全仓库 0 broken link”。

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

## 1.5 Deep-link / Markdown Anchor Audit

状态：`PARTIAL / NEEDS VERIFY`

已知事实：

1. 默认分支 recursive Git tree 已确认 Ch0–25、C1–C5、F1–F14、Indexes 与编辑基础设施文件真实存在。
2. Header-level relative paths 已逐章检查。
3. GitHub Code Search 当前对该仓库返回过 `incomplete_results=true`，因此“搜索 0 条”不能当作“绝对不存在”。
4. 本地全仓库 Markdown parser 方案受运行环境外网 DNS 限制，未能建立可声称的全量 anchor proof。
5. 已将 Ch4 顶部 C4 链接从脆弱 heading anchor 改成稳定独立 case-file path。

因此当前只允许声称：

> **主导航和已检查 target paths 正常；尚不声称所有正文 heading anchor 已被形式化全量验证。**

详见：[`00_Link_Audit.md`](./00_Link_Audit.md)。

---

# 2. Bibliographic / External Fact Audit

## 2.1 More Thinking Is Not Always Better

状态：`SAFE IN CURRENT TEXT / NEEDS SOURCE ANCHOR`

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

2026-10-18 的公开检索没有建立“此前那个完整副标题”与该项目的一一对应公开记录；使用精确数字、四个 benchmark 名以及 Answerer–Auditor 组合反查，也没有找到可以安全充当正式公开来源的唯一记录。

因此当前处理原则：

> **不猜副标题，不拿相似公开论文冒充来源；只使用已经确定的项目主标题，并把它当 Internal Research Example。**

最终书稿若保留研究数字，需要二选一：

```text
A. 链接正式 paper / arXiv / published artifact
```

或：

```text
B. 链接内部 frozen experiment summary / result table
```

在 Source Anchor 建立之前，不伪造 bibliographic entry。

---

# 3. Internal Research Example Audit

## 3.1 More Thinking Research Example

状态：`CLAIM SCOPE CONTROLLED / NEEDS SOURCE ANCHOR FOR NUMBERS`

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

这些是方法论区分；具体效果数字则必须绑定对应实验协议与 denominator。

---

# 4. Formula / Metric Audit

## 4.1 Ch3 — Pairwise Reward Model Probability

状态：`PASS`

当前写法：

\[
P(y_w\succ y_l\mid x)
=\sigma\left(r_\theta(x,y_w)-r_\theta(x,y_l)\right)
\]

判断：

- 与经典 Bradley–Terry / logistic pairwise preference 建模形式一致；
- 章节明确把它作为“经典 pairwise 概率”而不是唯一 Reward Model 形式；
- 没有把 learned reward 写成客观真值。

---

## 4.2 Ch4 — Recoverability Notation

状态：`FIXED`

已从单步 action 形式：

\[
\exists a \in \mathcal{A}:\; V(s_t,a) > V(s_t,a_{base})
\]

修正为 future policy / continuation 形式：

\[
\exists \pi \in \Pi_{allowed}:\; V(s_t;\pi) > V(s_t;\pi_{base})
\]

并在正文中显式解释：

```text
π
= 从当前 state 开始的一段允许 future policy / continuation
```

这样与 Recoverability 的真实语义一致：

> **问“是否存在更好的未来”，而不是“是否存在一个更好的单步动作”。**

---

## 4.3 Ch18 — Data Value / ROI / Marginal Utility

状态：`PASS — explicitly heuristic / decision notation`

已检查：

\[
V(D\mid M,T,E)
\]

用于强调 Data Value 条件化于模型、训练与评测环境；语义合理。

\[
PotentialValue(D)
\approx
Quality\times Relevance\times Novelty\times Learnability\times Applicability
\]

正文已经明确标注为 heuristic，不是统计定律。

\[
DataROI(D)=\frac{\Delta Utility(D)}{TotalCost(D)}
\]

作为资源配置 ratio 合理。

\[
MU_k=\frac{\Delta Utility}{\Delta Cost}
\]

用于表达 marginal utility，合理。

\[
RiskPriority
\approx
Frequency\times Severity\times Exposure\times Irreversibility
\]

正文明确作为讨论框架，而非 calibrated risk equation。

\[
V(A+B)\neq V(A)+V(B)
\]

用于强调 mixture interaction，不声称具体交互形式。

结论：当前表达安全，不为了“数学化”进一步伪精确。

---

## 4.4 Ch20 — Mixture / Temperature Sampling / Effective Information

状态：`PASS`

当前：

\[
M=\{(D_i,w_i)\}_{i=1}^{K}
\]

作为 mixture 表示合理。

Temperature-style source sampling：

\[
p_i\propto n_i^\alpha
\]

并解释：

```text
α = 1  → 按原始规模
α < 1 → 提高小 bucket 相对曝光
α = 0 → 接近 source-level uniform
```

语义正确，并明确说明它只是 mixture implementation tool，不是通用最优策略。

当前正文还使用加权样本的直觉表达：

\[
N_{eff}\approx\frac{(\sum_i w_i)^2}{\sum_i w_i^2}
\]

正文明确将其定位为“直觉公式”，用于提醒 `Exposure ≠ Independent Information`，没有把它包装成对所有相关/簇结构都成立的精确有效样本量定律。

判断：`PASS WITH SCOPE CLEAR`。

---

## 4.5 Ch21 — General Data Intervention Formula

状态：`FIXED`

原先总公式使用 additive-specific 的：

\[
\Delta(D;M_0,T,E)
=
Metric(Train(M_0,B+D,T),E)
-
Metric(Train(M_0,B,T),E)
\]

现已改成通用 Data Intervention operator：

\[
\Delta(I_D;M_0,T,E)
=
Metric(Train(M_0,I_D(B),T),E)
-
Metric(Train(M_0,B,T),E)
\]

其中：

```text
I_D
= 对 baseline mixture B 施加的数据 intervention
```

可以统一覆盖：

```text
Add
Remove
Replace
Reweight
Transform
```

因此公式与整章实际 action space 已一致。

---

## 4.6 Ch23 — Raw vs Fixed-mix Metric

状态：`PASS`

当前：

\[
S_{obs}=\sum_k p_{new}(k)S_k
\]

用于反映当前线上真实 task mix 下的 aggregate performance。

固定参考分布：

\[
S_{fixed}=\sum_k p_{ref}(k)S_k
\]

用于近似回答：

> 如果任务组合保持参考分布，系统自身 slice-level performance 的变化如何？

两者回答不同问题，正文已经明确不能互相替代。

---

## 4.7 Formula Audit Summary

```text
Ch3  Pairwise logistic      PASS
Ch4  Recoverability        FIXED
Ch18 ROI / MU / heuristics PASS
Ch20 Mixture / temperature / N_eff
                            PASS with scope clear
Ch21 Data intervention     FIXED
Ch23 Fixed-mix metric      PASS
```

原则：

> **能用普通语言清楚表达的 heuristic，不为了显得“理论化”强行伪精确；真正承担定义职责的公式，则要求 notation 与概念边界一致。**

---

# 5. Research Number / Denominator Audit

## 5.1 More Thinking — fixed-depth accuracy

状态：`NEEDS SOURCE ANCHOR — claim scope currently safe`

当前 Ch4 保留：

```text
depth 1 → 69.04%
depth 2 → 74.09%
depth 3 → 70.97%
```

并明确将它们放在：

```text
ProofWriter
PrOntoQA
ProverQA
FOLIO
```

等逻辑推理任务的具体研究实例中。

当前文本的优点：

1. 没有把三组数写成“LLM 普遍规律”。
2. 紧接着用 `Wrong→Right / Right→Wrong` 解释为什么 average accuracy 不够，而不是只用三组数字做结论。
3. 已标记为 Research Example。

当前缺口：

> 书内尚未给这三个数字一个可点击的内部 experiment artifact / paper source anchor。

因此 final publication 前需要建立 source anchor；在此之前，不把这三个数标记成“外部 bibliographic fact 已核验”。

---

## 5.2 More Thinking — 5,001 / Gap-Audit / token numbers

状态：`NOT PRESENT IN CURRENT BOOK BODY`

早期研究材料中曾使用：

```text
5,001 samples
69.04 / 74.09 / 70.97
Gap-Audit 76.03% / 2,988 tokens
fixed2 74.09% / 4,678 tokens
```

但当前结构性精修后的 Ch4 正文只保留 fixed-depth 三个 accuracy 数字；`5,001`、`76.03`、`2,988`、`4,678` 目前没有写入本章。

因此当前书稿不需要为“已经被删掉的数字”制造新的引用负担。

---

## 5.3 RoTFuse / K17 — 888 / 750 / 138

状态：`NOT PRESENT IN CURRENT Ch16 BODY — denominator principle retained`

早期研究上下文里有：

```text
888 full population
750 triggered / intervention-path cases
138 screened but non-triggered cases
```

当前精修后的 Ch16 已不再把这些具体 cohort 数字写入通用 Evaluation Protocol 章节。

保留下来的是通用纪律：

```text
Full Population
↓
Screening
↓
Triggered / Non-triggered
↓
Candidate Generation
↓
Selection
↓
Final Outcome
```

并显式写明：

> `Non-triggered Cases 仍属于 Full Population。`

以及：

> routing 方法的 E2E 结论不能只统计 intervention subset。

判断：这是更好的书稿设计。

```text
Specific cohort count
→ 应留在具体 Research Artifact / Experiment Report

Denominator discipline
→ 留在通用方法论章节
```

---

# 6. Visual Integration Audit

状态：`PASS — ownership clear / 3 replacement tasks pending`

详见：[`00_Figure_Integration_Audit.md`](./00_Figure_Integration_Audit.md)。

结论：

- F1–F14 已有唯一 canonical visual ownership；
- 大多数章节图不是冗余，而是有额外教学价值的 `LOCAL LENS`；
- 只有三处属于高置信“同一全局关系被画两套”：

```text
R1  Ch14 §14.0 → F6 Credit → Failure Causal Map
R2  Ch15 §15.0 → F7 Evidence → Evaluator Stack
R3  Ch19 §19.5 → F11 Governance / Lineage DAG
```

这些整改属于视觉真源统一，不改变正文知识结构。

---

# 7. Final Continuous Read-through

状态：`PASS — one bridge fix identified`

详见：[`00_Final_Readthrough_Log.md`](./00_Final_Readthrough_Log.md)。

覆盖：

```text
Ch0–25
```

书级结论：

```text
Chapter Order
PASS

Part Boundaries
PASS

Canonical Ownership Under Continuous Reading
PASS

Cross-chapter Problem Handoff
PASS except Ch18 → Ch19 bridge

Synthesis / Ending
PASS
```

唯一明确的文字结构修复：

```text
Ch18 → Ch19
BRIDGE FIX
```

含义：Ch18 已经完整回答“数据预算应该投哪里”，但结尾还缺一句把读者自然送进：

```text
长期投资的数据资产
→ 必须拥有可追溯身份、版本、历史和 usage lineage
→ Ch19 Governance / Lineage
```

这不需要重写 Ch18 主体，只需要补短 bridge。

---

# 8. Remaining Acceptance Queue

## P0 — Book seams

```text
[ ] Ch18 → Ch19 bridge
```

## P0 — Visual canonicalization

```text
[ ] Ch14 §14.0 → F6
[ ] Ch15 §15.0 → F7
[ ] Ch19 §19.5 → F11
[ ] 给 canonical owner chapters 补轻量 Master Figure pointer
```

## P1 — Bibliography / Source Anchor

```text
[ ] More Thinking fixed-depth source anchor
[ ] formal metadata if / when a reliable source exists
```

## P1 — Terminology

```text
[ ] Pretraining / Post-training spelling consistency
[ ] LLM-as-a-Judge hyphenation consistency
[ ] Agent-visible State / World State capitalization consistency
[ ] canonical English term capitalization spot-check
```

## P1 — Navigation

```text
[ ] deep body-link audit as tooling permits
[ ] Markdown heading-anchor audit as tooling permits
[ ] case / figure links after final integration
```

---

# 9. Verification Discipline

1. **没核验就写 NEEDS VERIFY，不靠记忆补 bibliographic detail。**
2. **Internal research result 可以保留，但必须绑定 protocol / version / denominator。**
3. **Research Example 不自动升级成 Universal Claim。**
4. **Corrected label 不改写 historical decision history。**
5. **Web fact 和 repository/internal fact 分开记录来源。**
6. **部分审计不写成全量保证。**
7. **Heuristic 不伪装成定律；canonical formula 的 notation 必须匹配语义。**
8. **具体研究 cohort 数字优先留在 research artifact；通用章节保留可迁移的方法论。**
9. **Master Figure 是全局视觉真源；局部图只保留真正增加分析粒度的 Lens。**

---

# 10. Current Status

```text
Architecture
✓

Concept Ownership
✓

Cases
✓

Master Figures
✓

Retrieval Indexes
✓

Header / Navigation Audit Round 1
✓

Formula / Metric Audit Round 1
✓

Research Number / Denominator Audit Round 1
✓ More Thinking / K17 scope audited

Figure Integration Audit
✓ analysis complete
→ 3 visual replacements pending

Final Continuous Read-through
✓ complete
→ one Ch18→19 bridge pending

Deep Link Audit
→ partial / tooling-limited

Bibliographic Source Anchor
→ More Thinking pending

Terminology Consistency
→ next cleanup pass
```

一句话：

> **全书已经通过骨架、概念、公式、数字口径与连续阅读验收；剩余工作是少量接缝、视觉真源、术语一致性和引用锚点，不再属于知识体系重写。**
