# Q37 如何把 Evaluator Signal 转成 Preference / Reward / Supervision，同时控制 Evaluator Bias？

- Level: M2
- Mastery: S0
- Related Parts: Part 2 / Part 4 / Part 6 / Part 8
- Related Patterns: P02 Deterministic First, Judge Last; P08 Judge Calibration Before Scale; P10 Replayable Evaluation; P12 Mechanism ≠ Outcome
- Canonical Data Owner: `LLM_Agent_Data/03_Preference_Data_Reward_and_Feedback.md`
- Related Case: VeriAgent reviewed failure signal → candidate memory promotion

## 30-second answer

Evaluator signal 可以进入 preference / reward / supervision，但**不能把 evaluator output 直接当 ground truth**。

我会先定义 signal contract：它评价什么、证据来源是什么、输出是 label / score / pairwise preference / critique 还是 abstain、可靠性在什么 slice 上成立。能 deterministic verify 的部分优先用 verifier；开放语义再用经过校准的 human / Judge。

真正进入监督前，要保留 raw judgment、confidence / abstain、rubric version、evaluator version、position/order、evidence 与 provenance，并对 position、verbosity、style、self-preference、critical slices 做 bias audit。

最重要的是训练后的闭环：一旦模型开始优化这个 evaluator，原来的 Judge validity 可能失效，必须用**独立 verifier / human anchor / holdout evaluator**重新检查 reward hacking 和 Goodhart effect。

核心原则：

```text
Evaluator signal
≠ truth
≠ reward-ready label
```

而是：

```text
signal
→ reliability gate
→ supervision construction
→ optimization
→ independent re-evaluation
```

## 90-second answer

把 evaluator signal 变成学习信号，我会做一个 **Evaluator Signal Promotion Gate**。

先问：

1. **Evidence**：有没有更强的 deterministic / executable evidence？
2. **Evaluator validity**：Judge / human 在目标 task、rubric、slice 上是否校准过？
3. **Output semantics**：`chosen` 是绝对正确，还是只相对更好？是否允许 tie / both bad / cannot judge？
4. **Bias controls**：position、verbosity、style、self-preference、identity 是否会改变 label？
5. **Provenance**：model、prompt、rubric、decoding、reference、timestamp、raw rationale 是否可追溯？
6. **Optimization risk**：训练模型能否学会迎合 evaluator，而不是改善真实目标？
7. **Independent validation**：训练后是否还有没有参与监督构造的 human / verifier / evaluator holdout？

监督形式也必须匹配 evidence：

```text
Exact verifier → correctness / accept-reject signal
Pairwise human/Judge → preference
Rubric score → criterion-level supervision
Failure trace → process / recovery supervision candidate
Critique → editing / repair candidate
```

不要把所有 signal 压成一个万能 scalar reward。

---

# 1. Evaluator 是 Measurement Instrument，不是 Truth Oracle

一个 evaluator 的输出可能是：

```text
PASS / FAIL
A > B
score = 4/5
failure_type = grounding
critique text
confidence = 0.72
ABSTAIN
```

这些首先表示：

> 在当前 evaluator contract 下，evaluation system 产生了某个 judgment。

它不自动表示：

```text
真实用户一定同意
标签绝对正确
可以直接作为 reward
模型优化这个 signal 就会改善真实目标
```

尤其 LLM-as-a-Judge 本身会受系统性 bias 影响。

---

# 2. Evidence Hierarchy：能验证的不要降级成主观 Reward

一个实用层级：

```text
Executable / deterministic verifier
        ↓
Environment outcome / task contract
        ↓
Adjudicated expert / human anchor
        ↓
Calibrated LLM Judge
        ↓
Heuristic / weak signal
```

不是说上一层永远完美，而是：

> 当更直接的 task evidence 已经存在时，不应该让更弱的 Judge opinion 覆盖它。

例如代码是否通过测试、SQL 数值是否正确、工具参数是否满足 schema，都应尽量使用 deterministic evidence。

Judge 更适合：

```text
clarity
helpfulness
instruction following
open-ended quality
multi-valid-output comparison
```

---

# 3. Signal Type 决定 Supervision Type

## Pointwise

```text
response → 1..5
```

可以用于 rubric / reward-style supervision，但要注意：

```text
scale calibration
leniency / severity shift
criterion overlap
```

## Pairwise

```text
A vs B → A preferred
```

适合 preference data。

但必须允许：

```text
A > B
B > A
Tie
Both Bad
Cannot Judge
```

否则会强迫 evaluator 制造伪 preference。

## Binary verifier

```text
valid / invalid
```

可作为强 correctness signal，但仍要区分：

```text
valid execution
vs
semantic correctness
```

## Critique

Critique 是：

```text
diagnostic artifact
```

不是天然的 gold correction。

要把 critique 变成 repair / SFT data，需要额外验证修复后的输出真的更好。

---

# 4. Chosen 不等于 Correct

Preference 中最常见的错误之一：

```text
A > B
```

被错误解释成：

```text
A = good
B = bad
```

实际上可能是：

```text
A wrong
B more wrong
```

或者：

```text
A good
B also good
```

因此 preference record 最好保留：

```text
absolute validity if available
relative preference
criterion-level evidence
```

如果两个候选都违反 critical safety / correctness contract，应该允许：

```text
Both Bad
```

而不是强行选一个 chosen。

---

# 5. 最小 Evaluator Signal Record

建议监督构造前至少保存：

```text
sample_id
context_id
candidate_ids
raw_outputs
evaluator_type
evaluator_model_version
evaluator_prompt_version
rubric_version
decoding / seed
presentation_order
raw_judgment
criterion_scores
rationale / evidence
confidence
abstain_status
reference / verifier result
human_anchor_status
slice
known_bias_flags
adjudication_status
promotion_status
```

如果最后只保存：

```text
chosen = A
rejected = B
```

以后几乎无法审计这个 preference 为什么成立。

---

# 6. Judge Bias 会被 Training 放大

假设 Judge 有 verbosity bias：

```text
内容相同
更长回答更容易赢
```

如果把 Judge preference 大规模用于训练，模型会学到：

```text
be verbose
```

然后新模型在同一个 Judge 下分数继续提高。

这形成：

```text
Evaluator bias
→ supervision bias
→ model behavior adapts
→ evaluator score rises
```

但真实用户价值可能不升反降。

这就是为什么：

> **一个 evaluator 在被优化之前有效，不代表在模型开始直接优化它之后仍然有效。**

---

# 7. Goodhart / Reward Hacking

当某个指标成为优化目标：

```text
measure → target
```

模型可能找到 evaluator shortcut。

常见形式：

```text
verbosity hacking
style imitation
rubric keyword stuffing
unearned confidence
self-preference exploitation
Judge identity cues
reward-model blind spot
```

Agent 中还可能出现：

```text
avoid difficult tool call to keep trace clean
premature safe stop to avoid false accept
excessive retries to maximize verifier pass
```

所以训练后不能只用同一个 reward source 再评一次。

---

# 8. Train Evaluator 与 Eval Evaluator 要有 Independence

如果：

```text
Judge J
→ produces preference data
→ trains candidate
→ Judge J evaluates candidate
```

结果存在循环自证风险。

更强设计：

```text
Training signal:
  Judge J1 + verifier + human review

Final evaluation:
  frozen verifier
  fresh human anchor
  held-out Judge J2 / different protocol
  production-like outcomes
```

不一定每次都需要多个模型，但必须至少有**某种独立证据**，不能所有 claim 都来自同一个被优化的 signal source。

---

# 9. Bias Probe 应在 Supervision Construction 前运行

对于 pairwise Judge，至少检查：

## Position Bias

```text
(A, B)
(B, A)
```

内容偏好应保持。

## Verbosity Bias

保持核心内容不变，只改变冗长度。

## Style Bias

只改变格式、措辞、礼貌程度等非目标因素。

## Self-preference

隐藏 system/model identity，或用不同 model family anchor。

## Critical Slice Bias

单独检查：

```text
safety
hard reasoning
short answers
non-native style
minority task families
```

总体 agreement 高不能掩盖关键 slice 失真。

---

# 10. Confidence / Abstention 不应被丢掉

如果 evaluator 自己不确定：

```text
Cannot Judge
Insufficient Evidence
Low Confidence
```

最差的做法是强制变成 binary label。

可以采用：

```text
high-confidence → auto promotion
medium-confidence → second judge / human review
low-confidence → abstain / no supervision
```

这比追求 100% coverage 更可靠。

尤其 high-risk supervision，应该允许缺标签，而不是伪造 certainty。

---

# 11. Weighting 不能只看 Judge Confidence

Judge 说：

```text
confidence = 0.99
```

不代表它真的 calibrated。

Supervision weight 可以综合：

```text
evidence source strength
historical calibration
agreement / adjudication
criticality
reference availability
slice reliability
```

而不是简单：

```text
weight = self-reported confidence
```

---

# 12. Evaluator Disagreement 是 Data Signal，也可能是 Evaluator Problem

如果：

```text
Human = A
Judge = B
Verifier = A
```

不要直接把它当作“hard preference case”。

它可能更应该进入：

```text
Judge calibration set
```

如果：

```text
Human1 = A
Human2 = B
No verifier
```

可能说明：

```text
rubric ambiguity
real preference distribution
```

这种 case 也未必适合压成单一 reward label。

所以：

```text
Disagreement
→ diagnose source
→ decide supervision or evaluator repair
```

---

# 13. Process Supervision 更容易发生 Credit Assignment Error

Trajectory 里可能有：

```text
step 3 locally wrong
step 5 recovered
final correct
```

如果仅因为 final correct 就把所有 steps 标正：

```text
错误 credit assignment
```

反过来 final wrong 也不代表所有 steps 都负。

Process / trajectory supervision 应结合：

```text
step correctness
criticality
first meaningful failure
recovery
final outcome
```

这是 Q18 的直接延伸。

---

# 14. Evaluator Signal Promotion Gate

一个实用 gate：

```text
1. Is task/evidence valid?
2. Is there a stronger deterministic evaluator?
3. Is evaluator calibrated for this slice?
4. Are bias probes acceptable?
5. Is label semantics explicit?
6. Are tie / both-bad / abstain allowed?
7. Is provenance complete?
8. Is this signal independent of final eval?
9. Can reward hacking be detected?
10. Is there independent post-training validation?
```

Promotion status 可以是：

```text
REJECT
REVIEW
CALIBRATION_ONLY
PREFERENCE_CANDIDATE
REWARD_CANDIDATE
PROCESS_SUPERVISION_CANDIDATE
PROMOTED
```

---

# 15. 不要过早把多维 Rubric 压成一个 Scalar

假设 rubric：

```text
correctness
safety
helpfulness
conciseness
```

直接加权成：

```text
Reward = 0.4C + 0.3S + 0.2H + 0.1K
```

会隐藏：

```text
critical safety fail
```

被其它维度平均掉的问题。

更稳健的做法：

```text
hard constraints first
then soft preference
```

例如：

```text
if correctness_invalid or safety_critical:
    reject
else:
    compare helpfulness / style
```

这和 Q10 rubric protocol、Q34 multi-dimensional gate 一致。

---

# 16. Evaluator Version 本身也是 Data Version

如果 preference labels 来自：

```text
Judge v1
```

后来换成：

```text
Judge v2
```

新旧 labels 不是天然同分布。

必须追踪：

```text
Judge model
prompt
rubric
decoding
reference context
bias mitigation
adjudication policy
```

否则 supervision dataset 的 label semantics 会悄悄漂移。

---

# 17. Post-training 后要重新校准 Evaluator

尤其当模型针对 Judge signal 优化后：

```text
pre-training Judge accuracy
```

不能直接外推到：

```text
post-training candidate distribution
```

需要 fresh audit：

```text
Judge-human agreement
critical-slice error
swap consistency
verbosity probe
new failure patterns
```

这实际上是 evaluator distribution shift。

---

# Evaluation Design

一个推荐闭环：

```text
Candidate outputs
↓
Deterministic verification where possible
↓
Calibrated human / Judge evaluation
↓
Bias / disagreement audit
↓
Raw judgments + provenance
↓
Supervision promotion gate
↓
Preference / reward / process data construction
↓
Training / policy update
↓
Independent fresh evaluation
↓
Reward-hacking / evaluator re-calibration
```

---

# Common Wrong Answers

## 错误 1：Judge agreement 90%，所以它的 label 可以全量训练

还要看 critical slices、bias、abstain、label semantics 和 optimization shift。

## 错误 2：chosen 一定是正确答案

Preference 只表示相对优劣，可能 both bad。

## 错误 3：模型训练后 Judge score 更高，所以 reward 设计成功

可能只是学会了 Judge shortcut。

## 错误 4：多个 Judge 投票就没有 bias

如果 Judge 共享同类偏差，多数票会稳定放大 bias。

## 错误 5：把所有 rubric 维度加权成一个分数最方便

可能让 critical failure 被 soft metric 抵消。

---

# Counterexample / Boundary

如果有一个完全可执行的数学 checker 能确定答案是否正确，那么 correctness supervision 不需要 LLM Judge。

但如果目标是“解释是否适合初学者”，deterministic verifier 无法直接给出 preference；这时经过 rubric calibration 的 human / Judge signal 更合理。

所以正确原则不是“永远不要用 Judge”，而是：

```text
Use the strongest evaluator that matches the claim.
```

---

# VeriAgent Example

VeriAgent challenge 中，一个模型输出如果恰好等于预设 plausible-wrong SQL 的结果：

```text
observable match
```

只作为 failure review signal。

系统不会自动：

```text
match wrong pattern
→ infer root cause
→ write memory
```

而是：

```text
trace review
→ explicit mechanism judgment
→ SQL replay
→ bind evidence hashes
→ candidate memory
```

这对应 Q37 的核心：

```text
Evaluator / heuristic signal
≠ promotion-ready supervision
```

必须经过 reliability、evidence 和 provenance gate。

## Follow-up Questions

- LLM Judge 生成的 preference 最少要做哪些 bias probe？
- chosen / rejected 都错时 preference data 怎么处理？
- 为什么训练后的模型可能让原 Judge 失效？
- 一个 scalar reward 什么时候会掩盖 critical failure？
- 多 Judge ensemble 为什么也不能自动解决 shared bias？

## Evidence of Mastery

达到 S3/S4 时，应能拿到一批 evaluator judgments，设计：

- evaluator hierarchy；
- signal schema；
- tie / both-bad / abstain policy；
- bias audit；
- supervision promotion gate；
- provenance / versioning；
- train/eval separation；
- post-training reward-hacking audit；
- independent confirmation protocol。

## Related Knowledge

- [Q08 Judge Reliability](../02_Grader_and_LLM_as_a_Judge/02_Judge_Reliability_and_Calibration.md)
- [Q09 Judge Bias](../02_Grader_and_LLM_as_a_Judge/03_Judge_Bias_and_Failure_Modes.md)
- [Q10 Rubric & Scoring Protocol](../02_Grader_and_LLM_as_a_Judge/04_Rubric_and_Scoring_Protocol.md)
- [Q18 Step / Outcome & Credit Assignment](../04_Trajectory_and_Failure_Analysis/02_Step_Outcome_and_Credit_Assignment.md)
- [Q30 Correlation Does Not Replace Human Judgment](../06_Statistics_and_Experiment_Design/07_Correlation_Does_Not_Replace_Human_Judgment.md)
- `LLM_Agent_Data/03_Preference_Data_Reward_and_Feedback.md`
