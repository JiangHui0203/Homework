# LLM / Agent Data Scenario Pack Stress Test

> 状态：`Stable Mother Edition V3.x / Scenario Validation`
>
> 目的：不用“看起来完整”判断 Scenario Pack，而是让它们承受真实追问和真实研究协议。本文只记录压力测试、暴露的问题和回写原则；不新建另一套方法论。

---

# 0. Stress-test Protocol

本轮测试两条路径：

```text
Interview Pack
→ 连续追问下是否还能直接、准确、可证据化地回答？

Project Starter Pack
→ 套到真实 selective / test-time reasoning 项目时，population、state、information boundary、cost 是否还能保持可审计？
```

通过标准：

```text
不是“能套上框架”
而是：

[ ] 不答非所问
[ ] 不把理论 / 外部文献 / 自己项目混成一种证据
[ ] 数字有 denominator / protocol / comparison context
[ ] selective system 保留 full-population accounting
[ ] online feature 与 offline label 严格分开
[ ] intervention unit / authoritative state 可重建
[ ] cost 能从 triggered slice 回到 E2E
[ ] final claim scope 不越界
```

---

# 1. Interview Pack Stress Test

## Test I1 — Definition under time pressure

问题：

```text
“Verifier 和 Judge 有什么区别？”
```

如果机械套总框架：

```text
Learning System
→ Evidence
→ Evaluation
→ ...
```

虽然没错，但第一句话没有回答问题。

更稳的顺序应该是：

```text
Direct Answer
→ Boundary
→ Example
→ Broader System only if asked
```

例如：

```text
Verifier 更依赖可明确检查的 evidence / predicate；
Judge 处理更解释性的 quality criterion。
二者都不是因为名字不同而天然更接近 Ground Truth，关键看 claim 和 evidence 是否匹配。
```

### Finding I1

> **Framework 是地图，不是答案。第一句话必须先回答当前问题。**

---

## Test I2 — Diagnosis follow-up

问题：

```text
“Judge 分数涨了，但线上 success 没涨，怎么办？”
```

第一层可以回答：

```text
先检查 Judge / metric construct validity，
再排 traffic / runtime / tool / environment，
最后看是否真的存在 model capability gain。
```

追问：

```text
“所以你是说 Judge 不靠谱吗？”
```

如果回答变成：

```text
“是，Judge 有 bias。”
```

则越界。

正确边界：

```text
Judge score 与目标 outcome 解耦
≠ Judge 一定坏了

可能是：
- Judge construct mismatch
- online distribution shift
- runtime / tool failure
- treatment effect only on proxy metric
- real capability gain too small / noisy
```

### Finding I2

> **追问时要保持 alternative hypotheses，不要把一个 diagnostic branch 讲成唯一 root cause。**

---

## Test I3 — “你自己做了什么？”

问题：

```text
“这些都是框架。你自己真正做过什么？”
```

如果继续讲公开论文或 canonical case，会显得回避。

回答必须显式区分：

```text
Public Literature
My Project / Frozen Result
Canonical Teaching Case
Hypothetical Design
```

也就是说：

```text
“文献里通常……”
“我在自己的项目里实际冻结的是……”
“为了说明结构，我用 C1 举例……”
“如果让我做新项目，我会……”
```

四种话语不能混。

### Finding I3

> **面试表达需要 Evidence Provenance。知道什么、做过什么、举例什么、假设怎么做，必须听得出区别。**

---

## Test I4 — Quantitative challenge

问题：

```text
“你说方法有提升，提升多少？”
```

只报：

```text
+X pt
```

不够。

最少要带：

```text
Population
Baseline / Treatment
Protocol
Budget
Metric
Uncertainty if material
Claim Scope
```

Selective system 还要额外说明：

```text
Full
Eligible
Triggered
Intervened
Observed
```

### Finding I4

> **数字不是装饰；每个 quantitative claim 都应该携带 denominator 和 protocol。**

---

## Test I5 — Framework overload

问题：

```text
“100 万条 Agent trajectory，你第一步做什么？”
```

如果回答完整跑：

```text
Task → Environment → Trajectory → Failure → Data Strategy → Experiment → Production...
```

会显得没判断优先级。

第一层更应该是：

```text
先确认数据 contract / provenance / task-family / success evidence 是否完整，
因为如果连 episode identity、environment version、final-state evidence 都不可靠，
后面的 quality score 和 training value 都没有稳固对象。
```

然后再按追问展开。

### Finding I5

> **答案要有 Stop Depth：先给最小充分回答，面试官继续追再展开系统。**

---

# 2. Interview Stress-test Verdict

原 Interview Pack 的知识结构通过；需要补的是表达协议：

```text
Direct Answer First
Alternative Hypotheses
Evidence Provenance
Quantitative Claim Contract
Stop Depth
```

因此不是“框架不够”，恰好相反：

> **框架已经够强，下一步要防止框架压过问题本身。**

---

# 3. K17 Project Starter Stress Test

真实测试对象：RoTFuse / K17 selective test-time reasoning intervention。

冻结配置可见：

- `JiangHui0203/RoTFuse/configs/routed_memory/k17_suspicion_e2e_v1.json`
- `cohort_total = 750`
- `tau = -1.1107723712921143`
- gate = `strict_less_than`
- local reasoning unit cap = `256` tokens
- sibling sampling `temperature = 0.7`, `top_p = 0.95`
- soft / hard intervention caps = `5 / 20`
- mainline token budget = `32768`
- frozen model path points to Qwen3-8B

项目完整 E2E accounting 同时保留：

```text
888 full decision population
=
750 triggered / intervention-path questions
+
138 screened but non-triggered questions
```

其中后 138 仍经过 threshold screening，只是未触发，因此 K17 与 Greedy 确定性相同。

这组真实语义马上暴露出 Starter Pack 中“Population”一词过于粗的问题。

---

# 4. K17 through Day 0 → A8

## A1 — Problem Intake

不是：

```text
“我们要做低置信度 sampling。”
```

而应写成科学问题：

> 在单模型、无 LLM fine-tuning 的条件下，当前 reasoning state 出现低置信信号时，从同一 authoritative prefix 做局部候选探索与选择，能否在可接受额外计算成本下提高 full-population end-to-end correctness？

这一步通过。

---

## A2 — Contract

普通 Task / Case Contract 还不够。

K17 必须额外冻结：

```text
Authoritative Prefix P
Provisional Unit u0
Unit Boundary / Delimiter
Trigger Statistic
Threshold τ
Comparison operator
Candidate generation policy
Same-prefix requirement
Selector observable features
Acceptance / continuation semantics
Intervention budget / cap
Final mainline budget
```

否则：

```text
“同一方法”
```

可能只是名字相同，decision state 已经不同。

### Finding K1 — Decision-state Contract

> **Selective / local intervention system 必须冻结 Intervention Point 和 Authoritative State，不只是 Task / Case。**

---

## A3 — Evidence Bundle

每题至少应能追回：

```text
full benchmark identity
screening result
trigger statistic
trigger decision
P identity / hash
u0 text / tokens / logprobs
candidate lineage
selected action / continuation
final answer
correctness label
cost / tokens / generations
```

如果只保存最终 answer 和是否 trigger，就不足以做 mechanism audit。

这一步总体通过，但要求 lineage 明确。

---

## A4 — Failure Record?

K17 说明 Starter Pack 不能假设所有项目都从 production failure 开始。

这个项目更接近：

```text
Hypothesis-led Research
```

研究对象是：

```text
Risk signal
Recoverability
Candidate existence
Selectability
Cost-aware intervention value
```

因此 A4 可以没有单一 `Root Cause`。

正确处理是：

```text
Failure-led project
→ A4 Failure Record

Hypothesis-led research
→ Mechanism / Opportunity decomposition

Evaluation-led project
→ Evaluator / Protocol gap record
```

### Finding K2 — Project Origin Mode

> **Starter Pack 需要区分 Failure-led / Hypothesis-led / Evaluation-led，不应把所有项目强制写成 bad-case root cause analysis。**

---

## A5 — Evaluator Contract

K17 需要明确：

```text
answer correctness evaluator
label version
benchmark-specific grading
censoring / incomplete handling
```

以及最重要的：

```text
Offline Label
≠ Online Feature
```

future rollout、最终 correctness、post-hoc adjudication 可以用于：

```text
analysis / supervision / oracle
```

但不能偷偷进入：

```text
online trigger / selector feature
```

### Finding K3 — Information Boundary

> **Experiment Contract 必须显式列出 Online-observable / Offline-only / Forbidden-leakage 三类信息。**

---

## A6 — Intervention

K17 不是 Data Intervention，也不应该被强行塞进：

```text
A6 Data Intervention Card
```

它是：

```text
Inference-time / policy intervention
```

因此 Starter Pack 的通用研究路径应允许：

```text
Data Intervention
Model / Training Intervention
Inference-time Intervention
Tool / Harness Intervention
Evaluator Intervention
Product / Contract Intervention
```

数据知识体系仍然可以分析这些 intervention，但不能为了让 Artifact Chain 整齐，把非数据方案改名成 Data Intervention。

### Finding K4 — Intervention Type

> **Project Starter 是问题启动器，不应预设最终 intervention 一定是 Data。**

---

## A7 — Experiment Card

这是本轮压力最大的一层。

原本：

```text
full / eligible / triggered
```

仍不足以覆盖真实 selective system。

至少需要：

```text
Full Decision Population
Screened
Eligible
Triggered
Intervened
Observed / Scorable
```

K17 的关键例子：

```text
Full = 888
Triggered = 750
Non-triggered = 138
```

750 的 triggered cohort 不能被写成 E2E denominator。

同时 Cost 也要分：

```text
Cost per Triggered Case
Incremental Cost on Intervention Path
Average E2E Cost over Full Population
Worst-case / Cap Cost
```

否则一个 selective method 很容易同时出现：

```text
“触发样本很贵”
```

和：

```text
“全体平均成本还可以”
```

却因为 denominator 不同产生表面矛盾。

### Finding K5 — Population + Cost Ledger

> **Selective experiment 必须同时拥有 Population Ledger 和 Cost Ledger。**

---

## A8 — Decision Memo

K17 的 Decision 不能只写：

```text
accuracy ↑ / ↓
```

而要拆：

```text
Full-pop E2E effect
Triggered-slice effect
Rescue
Harmful
Net
Coverage
Added tokens / generations
Budget cap behavior
Task heterogeneity
Uncertainty
```

Claim Scope 最后才决定能说：

```text
“在冻结 benchmark / model / protocol 下有 E2E gain”
```

还是只能说：

```text
“triggered cohort 存在 oracle headroom”
```

二者不是同一结论。

---

# 5. K17 Stress-test Verdict

Project Starter Pack 主顺序通过：

```text
Problem
→ Contract
→ Evidence
→ Evaluation First
→ Decision
```

但真实 selective research 暴露五个必须补强的字段：

```text
K1 Decision-state Contract
K2 Project Origin Mode
K3 Information Boundary
K4 Intervention Type
K5 Population + Cost Ledger
```

这些都是“真实项目一套就会遇到”的问题，不是为了模板更漂亮而增加字段。

---

# 6. Back-propagation Rules

本轮 finding 应回写原资产，而不是长期只留在 stress-test 文档：

```text
Interview Pack
→ Direct Answer First
→ Evidence Provenance
→ Quantitative Claim Contract
→ Stop Depth

Project Starter Pack
→ Project Origin Mode
→ Selective-system Contract
→ Information Boundary
→ Population / Cost Ledger
→ non-data intervention path

Practical Artifact Kit
→ A2 增 Intervention Point / Decision State（按需）
→ A7 墧 Population Ledger / Information Boundary / Cost Scope
```

---

# 7. Final Principle

压力测试的价值不是证明 Pack “很好用”。

而是找到：

```text
在真实追问里会不会答偏？
在真实 protocol 里会不会 denominator 漏掉？
在真实 selective system 里会不会 online/offline 泄漏？
在真实研究项目里会不会把非数据问题硬塞成数据问题？
```

最终原则：

> **一个 Framework 只有在被真实问题顶过以后，才知道哪些是骨架，哪些只是纸面整齐。**
