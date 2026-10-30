# Q35 什么样的 Failure 才值得进入 Hard-case Mining / Data Flywheel，而不是直接拿所有失败去训练？

- Level: M1
- Mastery: S0
- Related Parts: Part 4 / Part 5 / Part 8
- Related Patterns: P04 Slice Before Aggregate; P05 Frozen Core + Rotating Hard Set; P06 Trajectory First-Failure Analysis; P11 Holdout after Development; P12 Mechanism ≠ Outcome
- Canonical Data Owners: `LLM_Agent_Data/09_Hard_Case_Mining_and_Curriculum.md`, `LLM_Agent_Data/17_Data_Flywheel_and_Continuous_Improvement.md`
- Related Case: VeriAgent reviewed dev failure → candidate memory

## 30-second answer

**Failure 只是 acquisition signal，不是自动的 training example。**

我只会把满足以下条件的 failure 推进到 data flywheel：任务本身有效、失败被可靠验证、first meaningful failure / mechanism 至少有可审计证据、与目标能力相关、不是纯 infra / evaluator / duplicate 问题，而且能够构造可信监督或可验证 intervention。

更重要的是，必须保护 evaluation independence：如果一个 holdout failure 被用于 prompt、memory、规则或训练，它就不再是 clean holdout，应转为 `DEVELOPMENT_EXPOSED / regression / known-hard`，下一轮效果必须用 fresh holdout 验证。

因此正确链路是：

```text
Observed failure
→ validate
→ diagnose
→ abstract capability gap
→ choose intervention owner
→ construct candidate supervision
→ freeze intervention
→ fresh re-evaluation
```

而不是：

```text
failed = 1
→ train on it
```

## 90-second answer

我会先做一个 **Failure Promotion Gate**。

至少检查七件事：

1. **Task validity**：任务、reference、environment 本身是否有效？
2. **Failure validity**：这是真 failure，还是 evaluator error / infra abort / ambiguous task？
3. **Mechanism evidence**：知道 first meaningful failure 在哪里吗？root cause 是 observed、supported 还是 hypothesis？
4. **Target relevance**：它对应产品 / benchmark 声明中的目标能力吗？
5. **Actionability / learnability**：这个 failure 更应该改模型、数据、tool、controller、memory、evaluator 还是环境？
6. **Redundancy / value**：是新的 failure family / capability frontier，还是已有 bug 的第 500 个近重复？
7. **Evaluation isolation**：这个 case 是否来自 clean holdout？一旦用于开发，是否已经更新 exposure status 并准备 fresh confirmation？

通过之后也不一定都变成训练数据。有些 failure 更适合：

```text
Regression fixture
Hard / challenge benchmark
Prompt / controller fix
Tool schema validation
Evaluator calibration set
Human adjudication queue
Memory / rule candidate
SFT / preference / recovery supervision
```

所以真正的问题不是“失败要不要训练”，而是：

> **这条失败证据最适合被提升成哪一种工程资产？**

---

# 1. Failure ≠ Training Example

一个系统失败，最多先说明：

```text
在这个 task / run / environment 下
出现了一个不符合 contract 的结果
```

它不自动说明：

```text
模型能力存在稳定缺口
原因已经知道
该样本标签正确
训练它会改善能力
训练收益大于副作用
```

尤其 Agent 系统里，失败可能来自：

```text
model reasoning
tool/API
environment
state contamination
controller policy
retry budget
evaluator
reference
benchmark ambiguity
infra outage
```

如果 owner 判断错，把所有失败都做成模型训练数据，只会把系统问题错误归给模型。

---

# 2. 先做 Failure Validity Audit

## 2.1 Task 是否有效？

检查：

```text
Task contract clear?
Reference valid?
Environment snapshot valid?
Required tool actually available?
Input complete?
```

如果题本身有歧义，最先需要的是：

```text
benchmark / task repair
```

不是：

```text
train model to imitate ambiguous gold
```

## 2.2 Failure 是否被可靠验证？

优先证据：

```text
Executable verifier
Deterministic contract
Independent reference
Environment outcome
Adjudicated human evidence
Calibrated Judge
```

弱 signal，例如：

```text
low confidence
long reasoning
Judge critique
matches a plausible-wrong template
```

可以触发 review，但不应直接升级成 training label。

---

# 3. Symptom 不能直接当 Supervision Target

例如：

```text
Final answer wrong
```

只是 symptom。

真正 first meaningful failure 可能是：

```text
wrong entity resolution
wrong tool choice
invalid SQL alias
stale memory
missed verifier feedback
unsafe retry
```

如果只从 final wrong answer 构造“正确答案 SFT”，可能完全没有覆盖真实机制。

建议保留：

```text
Outcome
Symptom
First meaningful failure
Immediate mechanism
Root-cause hypothesis
Evidence level
Owner
Recoverability
```

然后再决定 supervision type。

---

# 4. Failure Promotion Gate

一个可操作的 promotion record：

```text
failure_id
source_run_id
task_id
source_set
exposure_status
outcome
first_meaningful_failure
failure_family
mechanism
mechanism_evidence_level
owner
severity
frequency / recurrence
capability_gap
learnability
reference_quality
supervision_candidate
expected_intervention
expected_metric
regression_risk
fresh_confirmation_set
promotion_status
```

`promotion_status` 可以是：

```text
REJECT_INVALID
REVIEW_REQUIRED
REGRESSION_ONLY
BENCHMARK_HARD_CASE
EVALUATOR_CALIBRATION
DATA_CANDIDATE
CONTROLLER_CANDIDATE
TOOL_FIX
PROMOTED
```

这样避免所有失败最终都进入同一个“训练池”。

---

# 5. 哪些 Failure 通常不应直接进入训练？

## Infra / Provider Failure

例如：

```text
rate limit
provider outage
network timeout
```

如果目标不是训练 recovery policy，它们首先属于 infra / harness evidence。

## Invalid / Ambiguous Task

```text
missing reference
contradictory instruction
impossible task
```

训练这些数据可能制造错误监督。

## Evaluator Failure

如果 Judge 把正确答案判错：

```text
Evaluator bug
≠ model failure
```

这类 case 应进入 Judge calibration / adjudication。

## Exact / Near Duplicate

同一 mechanism 的 500 个模板近重复不等于 500 倍学习价值。

## Pure One-off Noise

一次 stochastic miss 可以有诊断价值，但不应因为“一次错”就自动变成能力缺口。

## Out-of-scope Failure

如果目标系统 contract 明确不支持某能力，它可以进入产品 scope review，但未必值得训练。

---

# 6. 哪些 Failure 更值得进入 Hard-case Mining？

更强候选通常具有：

```text
Target-relevant
Verified
Mechanistically interpretable
Recurring or risk-critical
Learnable / repairable
Non-duplicate
Has reliable supervision path
Can be re-evaluated independently
```

可以粗略理解成：

```text
Expected Learning Value
≈ relevance
× evidence quality
× severity / opportunity
× learnability
× novelty
```

这不是要求真的计算一个万能标量，而是提醒：

> 错得多，不等于值得学；错得少，也不等于不值得学。

低频但 critical 的 false accept / unsafe action 可能比高频轻微格式错误更值得优先处理。

---

# 7. Frequency 与 Severity 要分开

两个 failure family：

```text
A: 发生 20%，但只是轻微冗余
B: 发生 1%，但会执行错误外部动作
```

不能只按 frequency 排序。

至少保留：

```text
Opportunity count
Failure recurrence
Severity
Escape risk
Recoverability
Cost
```

Hard-case acquisition 的优先级来自多维权衡。

---

# 8. “能修”也不等于“该用训练修”

Owner routing 很重要。

| Failure | 更可能的 intervention |
|---|---|
| invalid tool schema | tool / validation |
| stale state leak | state isolation |
| alias scope reasoning error | prompt / memory / data / model |
| missing evidence yet answers | safe-stop policy / preference / controller |
| Judge verbosity bias | evaluator calibration |
| provider timeout | infra / retry policy |
| recurring domain knowledge gap | data / retrieval / model |

如果一个 deterministic guard 就能可靠阻止高风险错误，未必需要先花训练成本。

---

# 9. Holdout Failure 是最容易被误用的数据

这是 Q35 最重要的边界之一。

假设：

```text
clean test
→ 发现 failure X
→ 为 X 写 prompt / memory / training sample
```

此时：

```text
X 不再属于 clean confirmation evidence
```

它可以被提升为：

```text
regression fixture
known-hard case
training/development example
```

但必须同步更新：

```text
exposure_status = DEVELOPMENT_EXPOSED
```

下一轮如果要证明泛化，必须使用：

```text
fresh holdout
```

而不是继续在同一批 X 上反复跑到变好。

---

# 10. Regression Set 与 Training Set 的角色不同

一个 reviewed failure 可以同时产生两种资产：

```text
A. Minimal regression fixture
B. Candidate learning data
```

Regression fixture 回答：

> 已知 bug 回来了没有？

Training data 回答：

> 能不能让模型学习某类能力？

它们不应混成一个“hard set”。

训练后在 regression case 上通过，只证明：

```text
known failure no longer reproduces
```

不证明：

```text
unseen tasks generalize
```

---

# 11. 从 Single Case 到 Failure Family

高价值闭环不会只记：

```text
task_103 wrong
```

而会抽象成：

```text
Failure Family:
child-row eligibility evaluated at parent grain
```

然后问：

```text
还有哪些不同实体 / schema / wording 会触发同一机制？
```

这时才可能构造：

```text
natural examples
counterfactual examples
synthetic variants
hard negatives
recovery trajectories
```

但具体 data construction 归 `LLM_Agent_Data`。

---

# 12. Data Flywheel 的 Eval-side Contract

Evaluation 侧至少负责交付：

```text
1. Verified failure evidence
2. Failure / capability label with confidence
3. Exposure status
4. Intended intervention owner
5. Expected target metric
6. Regression / side-effect metrics
7. Fresh confirmation requirement
```

Data / training 侧再负责：

```text
acquisition
construction
mixture
sampling
training format
training protocol
```

这样不会把“发现失败”和“如何训练”混成同一个阶段。

---

# 13. Promotion 后必须提前定义 Success Criterion

在真正做 intervention 前，写清：

```text
Target capability:
Primary metric:
Expected direction:
Minimum meaningful improvement:
Critical regression metrics:
Cost / latency guardrails:
Fresh holdout:
```

否则训练后非常容易：

```text
看哪个指标涨了
→ 宣称这批 failure data 有用
```

这会重新落入 adaptive analysis。

---

# Evaluation Design

一个最小闭环：

```text
Frozen evaluation
↓
Verified failures
↓
Failure Promotion Gate
↓
DATA_CANDIDATE / REGRESSION / TOOL / EVALUATOR / CONTROLLER
↓
Intervention constructed outside clean holdout
↓
Freeze candidate
↓
Fresh holdout + frozen regression suite
↓
Target improvement + regression + cost analysis
```

建议保留两个 manifest：

```text
failure_promotion_manifest
intervention_manifest
```

并能追溯：

```text
哪一条训练 / memory / rule
来自哪一个 failure family
```

---

# Common Wrong Answers

## 错误 1：失败样本最有价值，所以全部回流训练

失败里混有 invalid task、infra、evaluator error、duplicate 和不可学习样本。

## 错误 2：test failure 最难，所以最适合立刻训练

一旦用于开发，它就不再是 clean test。可以训练，但必须降级 exposure，并准备 fresh confirmation。

## 错误 3：出现次数最多的 failure 优先级最高

还要看 severity、learnability、target relevance 和 redundancy。

## 错误 4：最终答案错，所以训练正确答案就能修

可能真正 failure 在 tool/state/recovery/controller 层。

## 错误 5：某个错误和预设 wrong pattern 相同，所以 root cause 已确认

Observable match 只是诊断 signal；root cause 仍需 trace / replay / counterfactual 证据。

---

# Counterexample / Boundary

如果是一个 deterministic compiler bug，10 个真实失败都来自同一明确实现错误，那么最佳 intervention 很可能是修代码并加 regression fixture，而不是构造 10 条 SFT 数据。

反过来，一个很少出现但高风险、可验证、跨多个任务模板复现的 unsafe action failure，可能值得高优先级进入 preference / policy supervision。

---

# VeriAgent Example

VeriAgent 的 Olist challenge 开发阶段提供了一个很清楚的 promotion flow：

```text
Dev failure
→ explicit failure review
→ verify actual mechanism
→ replay wrong/correct SQL
→ bind reviewed plan + trace hash
→ build candidate memory
→ freeze candidate
→ held-out paired test
```

其中：

- `CJ01_r01` 的问题是 child-row eligibility 被错误放到 parent grain；
- `CJ03_r01` 是 alias scope violation；
- 它们不是因为“答错了”就自动进入 memory；
- 真实根因由显式 review 建立，程序只做证据校验；
- held-out test failure 不作为本轮候选 memory 的学习材料。

这正对应 Q35 的原则：

```text
Failure
≠ Promotion-ready supervision
```

以及：

```text
Review + provenance + exposure control
→ candidate intervention
```

## Follow-up Questions

- 什么情况下一个 failure 只进入 regression，而不进入训练？
- rare critical failure 和 frequent low-severity failure 如何排序？
- 从 test 发现的 bug 修完后，旧 test 应如何重新分类？
- failure family 怎么避免被过度抽象？
- 一个 root-cause hypothesis 到什么证据级别才能进入 supervision？

## Evidence of Mastery

达到 S4 时，应能拿到一批失败日志，独立产出：

- invalid / infra / evaluator / system / model 分流；
- promotion criteria；
- exposure update；
- failure-family abstraction；
- intervention owner；
- regression fixture；
- fresh confirmation plan；
- 明确说明哪些 failure **不应该**进入 training data。

## Related Knowledge

- [Q17 First Meaningful Failure](../04_Trajectory_and_Failure_Analysis/01_First_Meaningful_Failure_and_Root_Cause.md)
- [Q20 Failure Taxonomy as Engineering Asset](../04_Trajectory_and_Failure_Analysis/04_Failure_Taxonomy_as_Engineering_Asset.md)
- [Q22 Leakage & Test-set Overfitting](../05_Benchmark_and_Evaluation_Data/02_Leakage_and_Test_Set_Overfitting.md)
- [Q23 Benchmark Set Roles](../05_Benchmark_and_Evaluation_Data/03_Frozen_Regression_Hard_and_Rotating_Sets.md)
- `LLM_Agent_Data/09_Hard_Case_Mining_and_Curriculum.md`
- `LLM_Agent_Data/17_Data_Flywheel_and_Continuous_Improvement.md`
