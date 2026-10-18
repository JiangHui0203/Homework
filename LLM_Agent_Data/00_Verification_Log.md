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

状态：`NEEDS REFINE — semantics correct, notation too narrow`

当前概念式：

\[
\exists a \in \mathcal{A}:\; V(s_t,a) > V(s_t,a_{base})
\]

语义目标是：

> 从当前 state 是否存在某个允许的未来 continuation / intervention，使最终 outcome 优于 baseline future。

问题：

- 单个 `a` 容易被理解成单步 action；
- Recoverability 在本章定义上允许 multi-step continuation / policy / branch。

最终公式统一 pass 建议改成：

\[
\exists \pi \in \Pi_{allowed}:\; V(s_t;\pi) > V(s_t;\pi_{base})
\]

或等价地：

\[
\max_{\pi\in\Pi_{allowed}} V(s_t;\pi) > V(s_t;\pi_{base})
\]

这样更贴合“存在更好的未来”，并自然与 Repairability / Selectability 区分。

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

状态：`NEEDS REFINE — current form is additive-specific`

当前：

\[
\Delta(D;M_0,T,E)
=
Metric(Train(M_0,B+D,T),E)
-
Metric(Train(M_0,B,T),E)
\]

对于 `Add Data` 实验是合理的。

但本章随后统一覆盖：

```text
Add
Remove
Replace
Reweight
Transform
```

所以作为“总 Data Experiment 因果对象”时，`B+D` 略窄。

最终公式统一 pass 建议写成 intervention operator：

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
= 对 baseline mixture B 施加的 Data Intervention
```

这样可以统一表示：

```text
Add / Remove / Replace / Reweight / Transform
```

并避免正文前面用 Additive notation、后面又声称它是所有 treatment 的总公式。

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
Ch4  Recoverability        NEEDS REFINE: action → future policy / continuation
Ch18 ROI / MU / heuristics PASS
Ch20 Mixture / temperature PASS
Ch21 Data intervention     NEEDS REFINE: B + D → general intervention operator
Ch23 Fixed-mix metric      PASS
```

原则：

> **能用普通语言清楚表达的 heuristic，不为了显得“理论化”强行伪精确；真正承担定义职责的公式，则要求 notation 与概念边界一致。**

---

# 5. Pending Verification Queue

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
[ ] More Thinking research example metrics / sample totals / token costs
[ ] RoTFuse / K17 benchmark counts / triggered denominators
[ ] 其他 research example percentages / cohort counts
```

## P1 — Formula / Metric

```text
[ ] Ch4 Recoverability notation final patch
[ ] Ch21 general Data Intervention notation final patch
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

# 6. Verification Discipline

1. **没核验就写 NEEDS VERIFY，不靠记忆补 bibliographic detail。**
2. **Internal research result 可以保留，但必须绑定 protocol / version / denominator。**
3. **Research Example 不自动升级成 Universal Claim。**
4. **Corrected label 不改写 historical decision history。**
5. **Web fact 和 repository/internal fact 分开记录来源。**
6. **部分审计不写成全量保证。**
7. **Heuristic 不伪装成定律；canonical formula 的 notation 必须匹配语义。**

---

# 7. Current Status

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
✓ with two planned refinements

Deep Link Audit
→ pending

Research Number / Bibliographic Audit
→ active next

Final Continuous Read-through
→ final stage
```

一句话：

> **现在的目标已经不是继续增加“看起来正确的内容”，而是逐项证明：链接是真的、题名是真的、数字有来源、公式语义一致、研究结论没有越过证据边界。**
