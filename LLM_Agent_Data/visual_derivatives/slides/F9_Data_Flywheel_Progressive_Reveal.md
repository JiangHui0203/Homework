# F9 — Data Flywheel / Progressive Reveal

> Derivative Type: `D2 Presentation Storyboard`
>
> Canvas: `1920 × 1080 / 16:9`
>
> Semantic Source: [`F9_Data_Flywheel.md`](../../figures/F9_Data_Flywheel.md)
>
> Source Blob: `340ee4458d9dfe0f8c1c5810fcfa4cb7b40e3cb2`
>
> Publication Derivative: [`F9_Data_Flywheel.svg`](../publication/F9_Data_Flywheel.svg)
>
> Thesis: **Production Failure 不是 Training Example；真正的 Flywheel 必须先做 Triage、Attribution、Capability Abstraction 和 Controlled Validation。**

---

# Frame F9-1 — Reality Produces Signals, Not Training Data

## Visible Objects

```text
Production / Real Use
→ Signals
```

Signals 只展开：

```text
Failure
Feedback
Drift
```

## Speaker Line

> “线上发生的第一件事不是‘拿到训练样本’，而是拿到一个 signal。Signal 可能来自 failure、feedback，也可能只是 drift。”

## Critical Boundary Introduced

```text
Production Failure
≠ Training Example
```

---

# Frame F9-2 — Diagnose Before You Acquire

## Visible Objects

新增：

```text
Signals
→ Triage
→ Attribution / Root Cause
→ Capability Gap
```

## Speaker Line

> “只有先确认 root cause，才能知道这是不是 Data Problem。Tool bug、Harness bug、Evaluator bug 都不应该被强行转成训练数据。”

## Critical Boundary Introduced

```text
Failure Signal
≠ Data Problem
```

---

# Frame F9-3 — Decide What is Worth Learning

## Visible Objects

新增：

```text
Capability Gap
→ Prioritize / Data Strategy
→ Acquire Experience
→ Construct Supervision
```

## Speaker Line

> “即使确认是 capability gap，也还要判断值不值得投，并决定需要什么 experience、什么 supervision，而不是默认 synthetic SFT。”

## Hidden Until Later

```text
Curation
Experiment
Train
Evaluate
Deploy
Monitoring
```

---

# Frame F9-4 — Curate and Test the Intervention

## Visible Objects

新增：

```text
Construct Supervision
→ Curate / Filter / Mixture
→ Controlled Data Experiment
```

## Speaker Line

> “Data intervention 在这里仍然只是 hypothesis。必须经过 curation 和 controlled experiment，才能知道是不是它导致了 improvement。”

## Critical Boundary Introduced

```text
Data Intervention
≠ automatically worth scaling
```

---

# Frame F9-5 — Learn, Evaluate, Decide

## Visible Objects

新增：

```text
Controlled Experiment
→ Train / Optimize
→ Evaluate / Regression
→ Deploy?
```

Decision Gate 显式出现：

```text
Yes → Production / Real Use
No  → Capability Gap
```

## Speaker Line

> “实验结果不是自动进入生产。要么 scale 回到 real use，要么 revise hypothesis 回到 capability gap。”

---

# Frame F9-6 — Monitoring Closes the Loop

## Visible Objects

新增完整反馈链：

```text
Production / Real Use
-.-> Monitoring / Drift
-.-> Signals
```

## Speaker Line

> “部署以后，Monitoring 重新产生 signal；但 signal 仍然要重新经过 diagnosis，不能直接触发 retraining。”

## Critical Boundary Introduced

```text
Fresh Frontier
≠ Frozen Regression Core
```

---

# Frame F9-7 — C1 Walkthrough

## Case Lens

```text
shipped order was refunded
↓
rule out Tool / Harness / Evaluator bug
↓
capability gap:
conditional constraint + observation grounding
↓
C1 sibling / transfer family
↓
SFT / Preference / Recovery / Regression
↓
matched-budget experiment
↓
scale only if target + transfer + regression pass
↓
monitor
```

## Speaker Line

> “C1 展示的是一个完整 learning opportunity，而不是一条 bad case。真正有价值的是它怎样被诊断、抽象、验证，再重新进入系统。”

## Final Takeaway

> **Flywheel 的速度不等于数据生产速度，而是 Reality 被正确路由到可验证 intervention 的速度。**

---

# 30s Version

```text
F9-1
→ F9-2
→ F9-4
→ F9-6
```

# 90s Version

```text
F9-1 → F9-2 → F9-3 → F9-4 → F9-5 → F9-6 → F9-7
```

# Acceptance

```text
[x] Production → Monitoring → Signals feedback preserved
[x] Deploy? Yes / No branches explicit
[x] Diagnosis precedes data acquisition
[x] Controlled experiment precedes scale
[x] Non-data routing remains possible
[x] Source SHA recorded
```