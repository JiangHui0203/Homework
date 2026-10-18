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

无需修改。

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

同时 Ch4 顶部的 C4 链接已从 heading anchor 改为稳定独立 case file：

```text
./cases/C4_Reasoning_Continue_Repair.md
```

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

作为资源配置 ratio 合理；Utility 的具体定义由项目决定。

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

结论：当前表达安全，不需要为了“数学化”进一步伪精确。

---

## 4.4 Ch20 — Mixture / Temperature Sampling

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

备注：早期草稿曾规划 weighted effective sample size，但当前精修版 Ch20 已不存在该公式，因此不需要再对不存在的表达做核验。

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

无需修改。

---

## 4.7 Formula Audit Summary

```text
Ch3  Pairwise logistic      PASS
Ch4  Recoverability        FIXED
Ch18 ROI / MU / heuristics PASS
Ch20 Mixture / temperature PASS
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

因此 final publication 前需要二选一：

```text
A. 链接正式 paper / arXiv / published artifact
```

或：

```text
B. 链接内部项目中的 frozen experiment summary / result table
```

在 Source Anchor 建立之前，不把这三个数标记成“外部 bibliographic fact 已核验”。

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

若未来重新加入，必须和 frozen protocol / dataset / model / token accounting 一起加入，而不是只加漂亮结果数字。

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

因此 888 / 750 / 138 不需要在 Ch16 里重新加回。

---

## 5.4 Number Audit Principle

```text
Illustrative Number
→ 明确是 example / hypothetical

Internal Research Number
→ 需要 source artifact + protocol + denominator

External Published Number
→ 需要 bibliographic citation

Canonical Definition
→ 尽量不要依赖某次实验数字
```

这能避免：

> 某次研究 cohort 的数字逐渐被写成整本书的固定常识。

---

# 6. Pending Verification Queue

## P0 — Navigation

```text
[ ] Deep body-link audit
[ ] Markdown anchor audit
[ ] Next-chapter link audit
[ ] Case / Figure links inside chapters after integration
```

## P1 — Bibliography

```text
[ ] More Thinking formal metadata / internal source anchor
[ ] 文中其他显式 paper / method citation
[ ] arXiv / venue / author spelling
```

## P1 — Numbers

```text
[ ] More Thinking fixed-depth source anchor
[ ] 其他仍保留在正文中的 research example percentages / cohort counts
```

已关闭：

```text
5,001 / Gap-Audit token numbers
→ 当前书稿未使用

K17 888 / 750 / 138
→ 当前通用 Ch16 未使用具体数字，只保留 denominator principle
```

## P1 — Formula / Metric

```text
[x] Ch4 Recoverability notation final patch
[x] Ch21 general Data Intervention notation final patch
[ ] paired / coverage metric notation spot-check
[ ] remaining chapter-local equations spot-check
```

## P2 — Terminology

```text
[ ] industry term capitalization
[ ] Pretraining / Post-training spelling
[ ] LLM-as-a-Judge hyphenation
[ ] Agent-visible State / World State consistency
```

---

# 7. Verification Discipline

1. **没核验就写 NEEDS VERIFY，不靠记忆补 bibliographic detail。**
2. **Internal research result 可以保留，但必须绑定 protocol / version / denominator。**
3. **Research Example 不自动升级成 Universal Claim。**
4. **Corrected label 不改写 historical decision history。**
5. **Web fact 和 repository/internal fact 分开记录来源。**
6. **部分审计不写成全量保证。**
7. **Heuristic 不伪装成定律；canonical formula 的 notation 必须匹配语义。**
8. **具体研究 cohort 数字优先留在 research artifact；通用章节保留可迁移的方法论。**

---

# 8. Current Status

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

Formula / Metric Audit Round 1
✓ all identified canonical-notation issues fixed

Research Number / Denominator Audit Round 1
✓ More Thinking / K17

Deep Link Audit
→ pending

Bibliographic Source Anchor Audit
→ active

Final Continuous Read-through
→ final stage
```

一句话：

> **现在的目标已经不是继续增加“看起来正确的内容”，而是逐项证明：链接是真的、题名是真的、数字有来源、公式语义一致、研究结论没有越过证据边界。**
