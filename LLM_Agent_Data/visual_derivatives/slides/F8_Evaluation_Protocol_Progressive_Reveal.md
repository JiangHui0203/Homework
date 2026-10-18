# F8 — Benchmark / Evaluation Protocol / Progressive Reveal

> Derivative Type: `D2 Presentation Storyboard`
>
> Canvas: `1920 × 1080 / 16:9`
>
> Semantic Source: [`F8_Benchmark_Evaluation_Protocol.md`](../../figures/F8_Benchmark_Evaluation_Protocol.md)
>
> Source Blob: `07b82f944e80f5d1ed004251cdd2f0a3a7ea0886`
>
> Publication Derivative: [`F8_Benchmark_Evaluation_Protocol.svg`](../publication/F8_Benchmark_Evaluation_Protocol.svg)
>
> Thesis: **“方法更好”不是一个分数，而是一条从 Question → Frozen Protocol → Matched Comparison → Metrics / Cost → Uncertainty → Claim Scope 的证据链。**

---

# Frame F8-1 — Start from the Claim

## Visible Objects

```text
Scientific / Product Question
↓
Capability Definition
↓
Benchmark Object
```

## Speaker Line

> “评测不能从‘跑哪个 benchmark’开始。先要定义问题和 capability，benchmark 只是承载这个能力定义的对象。”

## Critical Boundary Introduced

```text
Question
≠ Benchmark
```

---

# Frame F8-2 — Freeze the Protocol

## Visible Objects

新增：

```text
Benchmark Object
↓
Evaluation Protocol
```

右侧逐项出现：

```text
Population / Eligibility
Model / Prompt / Tool / Harness / Environment
Budget / Stop Conditions
Evaluator / Label Version
Seeds / Repetitions
```

## Speaker Line

> “Protocol 才决定怎么跑、怎么判、花多少预算。只要这些条件漂了，方法差异就和实验条件差异混在一起。”

## Critical Boundary Introduced

```text
Benchmark Object
≠ Evaluation Protocol
```

---

# Frame F8-3 — Baseline vs Treatment

## Visible Objects

新增 paired branch：

```text
Evaluation Protocol
↙                ↘
Baseline Run    Treatment Run
↘                ↙
Paired / Matched Analysis
```

## Speaker Line

> “真正有说服力的比较不是两个独立平均分，而是尽可能 matched / paired，让差异更能归因于 treatment。”

## Hidden Until Later

```text
Metrics
Cost
Uncertainty
Claim Scope
Population Accounting
```

---

# Frame F8-4 — Metrics are Multidimensional

## Visible Objects

从 `Paired / Matched Analysis` 向下展开：

```text
Success / Accuracy
Rescue / Harmful / Net
Coverage / Trigger / Intervention
Cost / Latency / Tokens
Failure Transition
```

## Speaker Line

> “尤其 selective system，只看总体 accuracy 会把 repair 和 degradation 抵消掉；同时不报 cost，‘更好’可能只是‘花得更多’。”

## Critical Boundary Introduced

```text
Higher Score
≠ Better Method if Budget Differs
```

---

# Frame F8-5 — Population Accounting

## Side Panel

```text
Full Population
↓
Eligible
↓
Triggered
↓
Intervened
↓
Observed Outcome
```

## Speaker Line

> “每一个 selective metric 都必须写 denominator。Triggered subset 很漂亮，不代表 end-to-end 系统真的改善。”

## Critical Boundary Introduced

```text
Triggered-only
≠ E2E
```

---

# Frame F8-6 — Uncertainty and Claim Scope

## Visible Objects

新增：

```text
Metrics / Cost
↓
Uncertainty / Statistics
↓
Claim Scope
```

## Speaker Line

> “最后一步不是写‘显著提升’，而是限定 claim scope：这个结论只在冻结的 population、runtime、budget 和 evaluator 下成立到什么程度。”

## Critical Boundary Introduced

```text
Observed Improvement
≠ Universal Capability Improvement
```

---

# Frame F8-7 — Case Lens

## C1 Family

```text
Baseline wrong → Treatment right = Rescue
Baseline right → Treatment wrong = Harmful
Both same = Neutral
```

再补：

```text
Tokens
Tool Calls
Candidates
Latency
Coverage
```

## Speaker Line

> “C1 family 让我们看到为什么 pairwise transition 比只看两个总体均值更有解释力：到底修了谁、伤了谁、花了多少。”

## Final Takeaway

> **可信 Evaluation 的产物不是一个 score，而是一条可审计的 claim。**

---

# 30s Version

```text
F8-1
→ F8-2
→ F8-3
→ F8-6
```

# 90s Version

```text
F8-1 → F8-2 → F8-3 → F8-4 → F8-5 → F8-6 → F8-7
```

# Acceptance

```text
[x] Benchmark / Protocol / Run remain distinct
[x] Population accounting shown before E2E claim
[x] Cost is explicit, not footnote
[x] Uncertainty precedes Claim Scope
[x] Triggered-only ≠ E2E preserved
[x] Source SHA recorded
```