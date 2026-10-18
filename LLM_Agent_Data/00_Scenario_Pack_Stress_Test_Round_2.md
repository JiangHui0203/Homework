# LLM / Agent Data Scenario Pack Stress Test — Round 2

> 状态：`Stable Mother Edition V3.x / Scenario Validation / Heterogeneous Stress Test`
>
> 前一轮：[`Scenario Pack Stress Test`](./00_Scenario_Pack_Stress_Test.md)
>
> 目的：第一轮用连续面试追问和 K17 selective reasoning protocol 验证了表达、decision-state、population、information boundary 与 cost discipline。本轮刻意换三种结构明显不同的问题，检查同一套 Scenario Pack 是否仍然成立：
>
> 1. **Agent Production Incident**：线上指标突然下降；
> 2. **Judge / Evaluator Drift**：尺子升级后分数变化；
> 3. **Large-scale Trajectory Curation**：手上已有大批 trajectory，怎样变成可信数据资产。
>
> 本轮重点不是继续加字段，而是判断：**哪些是真正跨项目稳定的骨架，哪些只是 K17 特有结构。**

---

# 0. Round-2 Acceptance Criteria

如果框架真的有跨项目稳定性，应满足：

```text
[ ] 不要求所有项目都从 A1 bad-case intake 开始
[ ] Monitoring alert 不自动解释成 Model Regression
[ ] Evaluator 变更不破坏历史可比性
[ ] 历史 decision 与新版本 re-score 不互相覆盖
[ ] 大批数据不会因为 sample count 很大就被默认高价值
[ ] Source Asset 与 Dataset View 有 lineage
[ ] Curation policy 可被独立版本化和验证
[ ] Raw / Valid / Verified / Unique / Accepted / High-value 分母不混
[ ] Entry point 可以不同，但最终能汇合到 Evaluation → Decision
```

---

# 1. Stress Test P — Agent Production Incident

## 1.1 Scenario

假设线上 Agent 在一周内出现：

```text
Overall Task Success
82% → 74%
```

同时已知：

```text
model checkpoint unchanged
```

但这一周可能还发生过：

```text
traffic mix changed
tool schema changed
harness parser deployed
business rule changed
judge prompt upgraded
retry policy changed
```

如果机械走：

```text
A1 Problem Intake
→ A4 Failure Record
→ “模型退化？”
```

顺序仍然过早。

这里真正的第一对象应该是：

```text
A10 Monitoring Incident / Drift Record
```

因为当前事实只是：

```text
observable metric changed
```

还不是：

```text
model capability changed
```

---

## 1.2 First-pass Evidence

第一层至少冻结：

```text
Alert Time
Incident Window
Last-known-good Window
Model / Prompt / Tool / Harness / Environment / Evaluator versions
Traffic mix
Business-rule version
Release / deployment IDs
Raw overall metric
Slice metrics
Fixed-mix metric
Frozen-core benchmark
Fresh-failure composition
```

如果：

```text
Raw Overall ↓
Fixed-mix ≈ flat
Frozen Core ≈ flat
```

更像：

```text
traffic / case-mix shift
```

而不是直接叫：

```text
model regression
```

如果：

```text
Raw Overall ↓
Fixed-mix ↓
Frozen Core ↓
```

才更值得进入 capability regression branch。

---

## Finding P1 — Monitoring-led Entry

> **Production incident 的自然入口是 A10，不一定是 A1。A10 负责 sensing / change capture，只有确认需要新项目后再创建 A1。**

这修正了一种过于线性的理解：

```text
A1 → A2 → ... → A10
```

真实系统更像：

```text
A10
→ triage
→ A1 / A3 / A4 / A5 / system fix
→ ...
→ A10
```

A10 既可以是末端，也可以是下一轮的起点。

---

## Finding P2 — Last-known-good + Change Ledger

仅记录：

```text
current metric
```

不够。

Incident attribution 需要：

```text
Last Known Good
+
Changed Since Last Good
```

至少覆盖：

```text
model
prompt
tool
harness
environment
evaluator
traffic mix
business rule
release / config
```

因此：

> **Production diagnosis 的基本比较单位不是“现在 vs 以前大概怎样”，而是 frozen last-known-good state vs incident state。**

---

## Finding P3 — Metric View Contract

同一 incident 至少保留：

```text
Raw Overall
Slice Metrics
Fixed-mix Metric
Frozen Core
Fresh Frontier / Fresh Failure
```

它们回答的是不同问题：

```text
Raw Overall
→ 用户现在真实体验怎样？

Fixed-mix
→ population mix 不变时系统行为是否变化？

Frozen Core
→ stable ruler 下 capability 是否变化？

Fresh Frontier
→ 新任务 / 新 failure 是否出现？
```

不能互相替代。

---

## Finding P4 — Rollback is a Decision, not a Diagnosis

线上 incident 还多一个研究项目里经常没有的维度：

```text
是否需要立即 rollback？
```

Rollback 条件应依赖：

```text
severity
blast radius
confidence
reversibility
critical guardrail
```

而不是等 root cause 100% 确认后才行动。

因此 production incident 有两条并行链：

```text
Safety / Containment Decision
+
Root-cause Diagnosis
```

不要把它们写成一条线。

---

# 2. Stress Test J — Judge / Evaluator Drift

## 2.1 Scenario

假设 Judge 从：

```text
J4 → J5
```

上线后观察到：

```text
Judge Score
71 → 78
```

但：

```text
Executable Success / Human Outcome
≈ flat
```

错误解释是：

```text
“模型能力涨了，但线上没体现。”
```

因为这里甚至可能根本没有改模型。

首先要问：

```text
尺子是不是变了？
```

---

## 2.2 Measurement Bridge

Evaluator upgrade 前后至少需要同一组 anchor：

```text
Human Gold
Executable Truth
Boundary Cases
High-severity Cases
Known Bias Probes
```

然后在**同一个 anchor set** 上同时跑：

```text
Old Evaluator J4
New Evaluator J5
```

得到：

```text
paired score shift
disagreement matrix
false-positive delta
false-negative delta
abstention delta
slice-specific change
decision-flip rate
```

必要时再做：

```text
score mapping / calibration bridge
```

---

## Finding J1 — Evaluator Change is a Measurement Intervention

> **换 Judge / Verifier 不是“后台实现细节”，而是 measurement intervention。**

因此 evaluator version 必须像 model / runtime version 一样进入：

```text
Experiment Contract
Monitoring Contract
Decision Memo
Lineage
```

---

## Finding J2 — Old↔New Measurement Bridge

如果 J4 和 J5 没有 paired anchor bridge：

```text
J4 score = 71
J5 score = 78
```

不能直接画成：

```text
71 → 78 improvement
```

因为两端不是同一把尺子。

所以：

> **跨 evaluator version 的 longitudinal claim 必须先建立 Measurement Bridge，或者明确断开历史曲线。**

---

## Finding J3 — Re-score ≠ Historical Decision Rewrite

假设历史样本在 J4 下：

```text
PASS
→ 被纳入 dataset_v4
→ 触发了某次 release decision
```

J5 重评分后变成：

```text
FAIL
```

正确做法不是把旧记录静默改成 FAIL。

而是保留：

```text
Historical Judgment
Historical Decision
Historical Evaluator Version
```

再新增：

```text
Rescored View under J5
```

因此：

```text
Corrected / New Judgment
≠ Historical Decision Rewrite
```

这对 audit / reproducibility 极其重要。

---

## Finding J4 — Evaluator Drift Can Become Data Drift

如果 Judge / Verifier 同时参与：

```text
filtering
rejection sampling
Best-of-N
preference construction
hard-negative mining
```

那么 evaluator policy 变化还会改变：

```text
what enters the dataset
```

于是：

```text
Measurement Change
→ Data Distribution Change
```

因此必须把：

```text
Evaluator Policy Version
```

写进 dataset build lineage。

---

# 3. Stress Test C — 500k Agent Trajectory Curation

## 3.1 Scenario

手里已有：

```text
500,000 trajectories
```

来源混合：

```text
production logs
synthetic rollouts
human demonstrations
recovery runs
benchmark traces
```

环境和 runtime 也不完全一致。

问题是：

> “第一步怎么处理，最后能不能做成训练资产？”

如果机械从：

```text
Failure Record
→ Data Intervention
```

进入，就显得很别扭。

它本质上是：

```text
Asset-led / Curation-led Project
```

---

## 3.2 First-pass Contract

第一层不是先给每条样本打一个 `quality=0.86`。

应该先问：

```text
Source identity complete?
Episode / Case identity complete?
Runtime / environment version known?
Final-state evidence available?
Family / seed lineage known?
Rights / privacy valid?
Evaluator / label version known?
```

因为如果：

```text
source lineage broken
```

后面的：

```text
quality score
dedup
mixture
split
```

都可能没有可靠对象。

---

## Finding C1 — Asset-led Entry

> **不是所有 Data 项目都从 failure 或 capability gap 开始；已有大批 source asset 时，需要 Asset-led / Curation-led entry。**

自然入口更像：

```text
Source Asset + A11 Lineage
↓
Curation Contract
↓
Dataset View
↓
A7 Downstream Validation
↓
A8 Decision
```

这再次说明：

```text
Artifact Chain
```

不应该被理解成一条所有项目都必须逐张填写的直线。

---

## Finding C2 — Source Asset ≠ Dataset View

500k raw trajectories 不是一个“训练集”。

更合理的是：

```text
Immutable / traceable Source Assets
+
Build Recipe
=
Dataset View
```

Build Recipe 至少包括：

```text
validity checks
filter version
evaluator version
dedup policy
family grouping
routing policy
sampling / mixture
schema transform
split policy
```

因此：

> **Dataset View 应该可重建，而不是把 raw source 原地修改成“清洗后数据”。**

---

## Finding C3 — Quality Gate is a Router

一条 trajectory 可能：

```text
不适合 Positive SFT
```

但非常适合：

```text
Preference Negative
Recovery Seed
Regression Case
Failure Analysis
Verifier Calibration
```

所以 curation action 不应只有：

```text
KEEP / DROP
```

而应该允许：

```text
PASS
DROP
QUARANTINE
REVIEW
DOWNWEIGHT
REGRESSION_ONLY
ROUTE_TO_NEGATIVE
ROUTE_TO_RECOVERY
```

---

## Finding C4 — Dedup Unit Must Match Decision Semantics

文本相似度不足以判断 Agent trajectory 是否“重复”。

至少考虑：

```text
Exact
Near-text
Semantic
Decision-level
Family-level
```

两个文本很像的任务可能因为：

```text
one forbidden constraint
one permission bit
one world-state difference
```

而具有完全不同的 decision boundary。

所以：

```text
Semantic Similarity
≠ Decision Equivalence
```

反过来，十万条实体名不同但决策结构完全一样的轨迹，也不能按十万份独立信息计算。

---

## Finding C5 — Yield Funnel Needs Its Own Denominators

500k raw 最终可能变成：

```text
500k Raw
→ 470k Structurally Valid
→ 410k Evidence-complete
→ 320k Verified / Scored
→ 210k Unique-enough
→ 150k Accepted / Routed
→ 70k High-value for target capability
```

每一层都应该记录：

```text
count
pass rate
failure reason
cost
latency
```

所以：

```text
Raw Sample Count
≠ Usable Yield
≠ High-value Yield
≠ Effective Information Size
```

---

## Finding C6 — Exposure is the Final Denominator

即使最终留下：

```text
150k samples
```

模型实际看到多少还取决于：

```text
sample share
token share
batch share
update share
loss weight
trajectory length
```

所以：

```text
Dataset Size
≠ Training Exposure
```

如果项目目标是训练影响，最终不能只报告 dataset count。

---

## Finding C7 — Curation Quality ≠ Learning Value

某个新 filter 可能让：

```text
label agreement ↑
parseability ↑
acceptance precision ↑
```

但也可能：

```text
hard negatives ↓
boundary diversity ↓
rare capability coverage ↓
```

所以最终仍然需要 A7：

```text
matched-budget downstream comparison
```

来回答：

```text
这个 curation policy 是否真的让目标能力学得更好？
```

因此：

```text
Intrinsic Data Quality
≠ Downstream Learning Value
```

---

# 4. Cross-scenario Verdict

三种任务放在一起后，最重要的发现不是“还缺多少字段”，而是 Artifact Chain 应被重新理解为：

```text
Entry Router
↓
Relevant Contracts / Evidence
↓
Controlled Change
↓
Evaluation
↓
Decision
↓
Monitoring / Re-entry
```

不同项目可以从不同入口进来：

```text
Failure-led
→ A1 / A2 / A3 / A4

Monitoring-led Incident
→ A10
→ triage
→ A1 / A3 / A4 / A5 / system fix

Hypothesis-led Research
→ A1 / A2-S / A7

Evaluation-led
→ A5
→ Measurement Bridge
→ A7

Asset-led / Curation-led
→ A11 source lineage
→ Curation Contract
→ A7
```

但最终都应汇合到：

```text
What changed?
↓
How do we know?
↓
What is the decision?
```

---

# 5. What Survived Both Stress-test Rounds

经过：

```text
Interview pressure
K17 selective reasoning
Production incident
Evaluator drift
Large-scale curation
```

下面这些结构仍然稳定：

```text
Task / Claim / Asset identity must be explicit
Evidence before attribution
Layer ≠ Owner
Evaluator output ≠ Ground Truth by definition
Online information ≠ Offline label
Population denominator must be explicit
Cost denominator must be explicit
Intervention type must not be assumed
Controlled comparison before claim
Decision must be separate from result
Monitoring can reopen the loop
Lineage must preserve historical meaning
```

这部分可以认为是真正的“承重骨架”。

---

# 6. Candidate Extensions — Do Not Canonize Yet

本轮发现先进入 candidate extension，而不是立刻修改所有 canonical template。

原因：

```text
Round 1
→ selective reasoning 暴露的问题高度明确
→ 已回写 A2-S / A7

Round 2
→ 三种异质任务暴露 entry routing / measurement bridge / curation contract
→ 需要至少再经过一轮不同场景验证
```

候选扩展：

```text
E1 Entry Router
E2 A10-I Production Incident Extension
E3 A5-M Evaluator Measurement Bridge
E4 A6-C Curation Contract
```

详见：

- [`Scenario Pack Candidate Extensions`](./00_Scenario_Pack_Candidate_Extensions.md)

---

# 7. Final Principle

第二轮压力测试之后，最重要的变化是：

```text
不是“Artifact Chain 更长了”
```

而是：

```text
Artifact Chain 不再被误解成单一路径
```

最终原则：

> **成熟框架不是要求所有问题从同一个门进入，而是允许不同真实问题从正确的入口进入，并在证据、比较和决策处重新汇合。**
