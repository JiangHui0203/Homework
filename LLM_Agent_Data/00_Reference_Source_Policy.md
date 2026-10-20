# LLM / Agent Data Knowledge System：Reference & Source Policy

> 状态：`Stable Mother Edition V3.x / Reference Layer`
>
> 目的：规定外部文献、内部研究、教学案例与工程约定应该怎样进入知识体系，避免“有引用就等于有证据”或“外部论文替内部结果补身份”。
>
> 核心原则：**Source 必须和 Claim 类型匹配。**

---

# 0. 四类 Source 必须分开

## S1 — External Literature Anchor

用于支撑：

```text
方法来源
经典技术机制
已公开 benchmark / evaluator / data practice
社区中可复查的研究结论
```

例如：

```text
RLHF / Preference Learning
DPO
Process Supervision
Self-Instruct
ReAct / Toolformer
LLM-as-a-Judge
HELM / AgentBench / SWE-bench
Datasheets / Contamination
```

External Literature 只能支撑它实际研究过的 claim，不能因为“主题相近”就替本书定义背书。

---

## S2 — Internal Research Example

用于：

```text
本项目 / 本人已有实验
冻结协议下的数值结果
未公开但有内部 artifact 的研究结论
```

必须至少能指向：

```text
frozen config / protocol
result summary
artifact path
commit / version
population / denominator
```

如果没有 Source Anchor：

```text
标记 INTERNAL / SOURCE ANCHOR PENDING
```

而不是借一篇外部相似论文来“补来源”。

典型例子：

```text
More Thinking fixed-depth 69.04 / 74.09 / 70.97
```

截至 2026-10-20，公开作者主页已经可以核对该工作的 title / authors / NLPCC venue identity；但这种公开身份信息只解决 bibliographic identity，不足以支撑固定深度结果、denominator、protocol 或其他定量 claim。

因此在正式 paper / proceedings 或 internal frozen result summary 挂上以前，相关定量结果仍只能作为：

```text
Internal Research Example
+ SOURCE ANCHOR PENDING for quantitative evidence
```

固定边界：

```text
Public identity listing
≠ Claim-bearing evidence anchor
```

---

## S3 — Canonical Teaching Case

例如：

```text
C1 Order / Refund
C2 Calendar / Meeting
C3 File / Repository
C4 Reasoning Continue / Repair
C5 Code / Execution
```

它们的目的不是证明一个经验事实，而是稳定：

```text
object relation
failure boundary
evaluation structure
artifact workflow
```

因此 Teaching Case 不需要伪装成真实 production incident。

如果使用教学数字：

```text
必须明确写 illustrative / teaching-only
```

不能让读者误以为是实测结果。

---

## S4 — Engineering / Editorial Convention

例如：

```text
A1–A11 Artifact Catalog / stable Artifact IDs
C1–C5 Case IDs
F1–F14 Figure IDs
stable owner / canonical term
Research-to-Production Gate
Entry Router / optional extension rule
```

这些属于本书的工作方法与信息架构，不需要伪装成“论文提出”。

其中：

```text
A1–A11
= composable artifact catalog
≠ 所有项目必须顺序执行的 canonical chain
```

不同项目可以从不同 Artifact Entry 进入；这种 orchestration 规则由 Starter Pack / Playbook 负责，而不是由外部论文承担定义权。

可以参考外部实践，但：

> **本书自己的 taxonomy / operating model 仍由本书定义并负责保持内部一致。**

---

# 1. Citation Role

External reference 进入正文时，优先说明它承担什么角色。

```text
FOUNDATIONAL
→ 历史 / 基础范式

METHOD
→ 具体技术机制

EVALUATION
→ benchmark / judge / protocol / environment

DATA
→ synthesis / curation / contamination / documentation

AGENT
→ tool use / reasoning-action / interactive environment

GOVERNANCE
→ provenance / documentation / transparency
```

一篇论文可以有多个 role，但不要把 role 写得无限宽。

---

# 2. Source Status

统一使用：

```text
VERIFIED
→ title / authors / identifier / target source 已核对

VERIFIED + VENUE
→ 公开论文与正式 venue 均已核对

INTERNAL
→ 内部研究，有可定位 artifact

SOURCE ANCHOR PENDING
→ 当前只有内部 claim，尚缺正式 anchor

TEACHING
→ 教学 / illustrative object，不是实测 claim

DO NOT CITE AS EVIDENCE
→ 仅用于启发或背景，不能支撑目标 claim
```

状态升级只针对它实际解决的证据问题。例如作者主页、会议 program 或 publication list 可以核对 title / authors / venue identity，但如果页面没有目标实验、protocol 与结果，就不能据此把内部 quantitative claim 从 `SOURCE ANCHOR PENDING` 升级成 public evidence。

---

# 3. Source Priority

Source priority 先受两个条件约束：

```text
Claim Coverage
+
Version Equivalence
```

只有在多个来源确实对应同一 bibliographic object、且对目标 claim 的覆盖基本等价时，才按下面顺序优先：

```text
正式 venue / publisher page
>
官方 project page / official repository
>
arXiv original paper
>
author-maintained page
>
可靠二手来源
```

如果不同版本在 authorship、篇幅、实验细节或 claim coverage 上存在实质差异，则不能机械执行“venue 替换 arXiv”。应选择**真正包含目标证据的版本**，并保留 version note。

典型情况：

```text
full technical report
≠ later concise venue report
```

此时正式 venue 可以证明 publication identity，但未必能替代完整 technical report 承担所有方法与实验 claim。

正文 bibliography 默认至少保留：

```text
Title
Authors
Year
Venue or arXiv ID
Stable URL
```

不要只保存搜索结果页面。

---

# 4. Claim Matching Rules

## 可以

```text
“DPO directly optimizes a preference objective without explicitly fitting a separate reward model in the standard RLHF pipeline.”
→ DPO paper
```

```text
“LLM judges may exhibit position / verbosity / self-enhancement bias.”
→ MT-Bench / Chatbot Arena judge paper
```

```text
“Executable benchmarks can expose failures hidden by surface-level textual judgment.”
→ SWE-bench / executable benchmark literature
```

## 不可以

```text
“我们的 selector 在某 benchmark 上 +2.1pt。”
→ 引一篇 selector 相关论文
```

外部论文不能证明内部数字。

也不可以：

```text
“本书定义 Tool ≠ Harness ≠ Environment，所以 ReAct 证明这个 taxonomy 正确。”
```

ReAct 可以作为 reasoning-action / environment interaction 的外部 anchor，但不能替本书自己的 canonical boundary 承担定义权。

---

# 5. Research Example Rule

本书出现 Research Example 时，建议采用：

```text
Research Example
Source Type: Internal / External
Protocol Scope: ...
Population: ...
Evidence Anchor: ...
Claim Scope: ...
```

如果 Evidence Anchor 缺失：

```text
Source Anchor Pending
```

必须保留。

尤其不要把：

```text
“这项工作公开列在作者主页 / program 上”
```

误写成：

```text
“这些内部结果已经有公开证据支持”
```

bibliographic identity 与 result evidence 是两个不同问题。

---

# 6. Numbers / Tables / Claims

任何具体数值优先附带：

```text
population
denominator
protocol
model / runtime
metric definition
source
```

尤其：

```text
Triggered-only
≠ Full-population E2E

Judge Score
≠ Environment Success

Public Test Pass
≠ Hidden / Full Correctness
```

Reference Layer 不能替 denominator discipline 补洞。

---

# 7. Chapter Citation Density

这本书不是 literature survey。

推荐：

```text
每个 canonical concept cluster
→ 1–3 个高质量 anchor
```

而不是：

```text
每段话
→ 3–8 篇 paper
```

优先保留：

```text
第一性来源
代表性方法
代表性 benchmark
真正影响本章方法论边界的工作
```

弱相关、重复、只因为关键词相同的论文不进入 canonical registry。

---

# 8. Canonical Reference Registry

统一入口：

- [`00_Canonical_References.md`](./00_Canonical_References.md)

Reference ID 固定为：

```text
R01
R02
...
```

正文如果需要轻量 cross-reference，可写：

```text
External Anchor: R08
```

Reference ID 是检索 ID，不是论文重要性排名。

---

# 9. Reference Update Rule

可以直接增量更新：

```text
补正式 venue
补 DOI
补 official repo / project page
新增一个真正不可替代的 anchor
修作者 / title / year
```

其中“补正式 venue”仍要先检查：

```text
venue version
≈ current claim-bearing version ?
```

如果只是 publication identity 得到确认，而正文依赖的完整方法 / 实验仍只存在于 technical report，则应保留两者关系，不做 silent replacement。

需要 review 的变化：

```text
用新论文替换 canonical foundational anchor
改变某 reference 的 claim role
把 internal claim 升级成 public evidence
```

原则：

> **Bibliography 可以增长，但 Claim ↔ Source 的对应关系不能静默漂移；Version ↔ Claim 也不能静默漂移。**
