# Part 8 — Eval → Data Flywheel / Post-training

## 核心问题

如何把可靠的 Evaluation 证据转化为数据 / policy / training intervention，并在更新后重新证明系统真的变好，而不是把 benchmark 暴露、evaluator bias 或 protocol drift 当成能力提升？

## 已建立

- [01 Failure Promotion to Data Flywheel](01_Failure_Promotion_to_Data_Flywheel.md) — Q35：什么 failure 值得进入 hard-case mining / data flywheel，哪些应分流到 regression / tool / evaluator / controller
- [02 Post-training Causal Validation](02_Post_Training_Causal_Validation.md) — Q36：如何用 matched intervention、clean/fresh holdout、mechanism check 和 regression suite 证明目标能力改善
- [03 Evaluator Signal to Supervision](03_Evaluator_Signal_to_Supervision.md) — Q37：如何把 verifier / human / Judge signal 转成 preference / reward / supervision，同时控制 bias、Goodhart 与 reward hacking

## 学习顺序

```text
Q35 先决定：什么 failure 有资格进入学习闭环？
 ↓
Q36 再证明： intervention 之后真的学到了目标能力吗？
 ↓
Q37 最后控制：用什么 evaluator signal 作为监督，怎样避免优化 evaluator 本身？
```

## 三个 Promotion / Validation Gate

### Failure Promotion Gate

```text
Observed failure
→ task valid?
→ failure verified?
→ mechanism evidence?
→ target relevant?
→ learnable/actionable?
→ correct owner?
→ exposure safe?
→ DATA / REGRESSION / TOOL / EVALUATOR / CONTROLLER
```

### Post-training Validation Gate

```text
Controlled intervention
→ matched budget?
→ frozen protocol?
→ clean holdout?
→ target effect?
→ mechanism-consistent?
→ regression acceptable?
→ fresh confirmation?
```

### Evaluator Signal Promotion Gate

```text
Raw judgment
→ strongest evidence source?
→ evaluator calibrated?
→ bias probes acceptable?
→ tie / both-bad / abstain supported?
→ provenance complete?
→ independent final eval available?
→ preference / reward / supervision candidate
```

## 必须形成的关键区分

```text
Failure
≠ Training Example

Exposed benchmark improvement
≠ Unseen capability improvement

High-quality data
≠ High learning value

Evaluator signal
≠ Ground truth

Chosen
≠ Absolutely correct

Judge score after optimization
≠ Independent evidence of improvement
```

## Strong Boundary with `LLM_Agent_Data`

本 Part **不重复** data construction / training 教材。

Canonical Data owners：

```text
LLM_Agent_Data/03_Preference_Data_Reward_and_Feedback.md
LLM_Agent_Data/09_Hard_Case_Mining_and_Curriculum.md
LLM_Agent_Data/17_Data_Flywheel_and_Continuous_Improvement.md
LLM_Agent_Data/21_Data_Experiments_and_Causal_Validation.md
```

`LLM_Agent_Data` 负责：

```text
acquisition
construction
sampling / mixture
preference / reward format
training data production
training intervention design
governance / lineage
```

本 Part 只负责 Evaluation 侧：

```text
failure evidence
promotion criteria
exposure status
evaluator reliability
intervention validation
fresh holdout
regression / cost / safety evidence
claim boundary
```

## Eval → Data 最小闭环

```text
Frozen evaluation
↓
Verified failure / disagreement / weakness
↓
Promotion Gate
↓
Capability gap + intervention owner
↓
Candidate data / memory / rule / controller / tool fix
↓
Freeze intervention
↓
Clean + fresh evaluation
↓
Target effect + mechanism + regression + cost
↓
Decision
↓
Exposure ledger update
↺
```

Flywheel 的核心不是“日志回流”，而是：

> 每一轮都知道什么值得学、为什么值得学、用什么证据学、学完以后如何独立证明。

## Holdout Discipline

这是 Part 8 的硬规则：

```text
clean holdout failure
→ used for prompt / memory / data / rule development
→ no longer clean holdout
```

旧 case 可以转成：

```text
regression
known-hard
training/development example
```

但新的泛化 claim 必须补：

```text
fresh holdout / rotating confirmation
```

不能在同一批 test 上反复优化，然后继续称它为 unseen evidence。

## Evaluator Discipline

当 evaluator 同时负责：

```text
produce training signal
+
score trained candidate
```

会产生循环自证风险。

因此优化后的模型至少需要某种独立证据：

```text
executable verifier
fresh human anchor
held-out evaluator
production-like environment outcome
```

并重新检查：

```text
position bias
verbosity bias
style bias
self-preference
critical-slice error
reward hacking
```

## 与前七个 Parts 的关系

```text
Part 1  定义 claim / metric contract
Part 2  校准 evaluator
Part 3  定义 Agent behavior / recovery
Part 4  定位 failure / root cause
Part 5  保护 benchmark / holdout
Part 6  判断 effect 是否可信
Part 7  冻结 artifact / replay / release gate
Part 8  决定哪些证据进入下一轮 learning，并重新验证
```

因此 Part 8 是前面知识的闭环，而不是独立的“训练章节”。

## 推荐后续 Lab

- `L08 VeriAgent Frozen Case`：把一次真实 VeriAgent intervention 整理成完整 frozen experiment，要求同时给出 evaluation contract、benchmark exposure、paired/statistical evidence、failure attribution、artifact provenance、intervention lineage 与最终 claim boundary。

这个 Lab 不需要训练模型；VeriAgent 当前的 reviewed failure → candidate memory → held-out paired evaluation 已足以训练完整的 Eval→Intervention→Re-eval 方法。

## VeriAgent Lens

VeriAgent 是本 Part 最直接的真实案例：

```text
Dev failures
→ explicit review
→ candidate memory construction
→ frozen memory snapshot
→ held-out paired evaluation
→ 29/36 vs 30/36
→ stage attribution check
```

两个关键结论同时成立：

1. dev failure 只有经过 review / replay / provenance 后才进入 candidate memory；
2. held-out 的 `+1/36` 不能归因于 memory，因为失败发生在 memory 有机会作用之前。

这正好说明完整闭环必须同时具备：

```text
promotion discipline
+
validation discipline
```
