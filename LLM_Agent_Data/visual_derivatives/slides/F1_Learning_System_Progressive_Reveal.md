# F1 — Learning System Overview / Progressive Reveal

> Derivative Type: `D2 Presentation Storyboard`
>
> Canvas: `1920 × 1080 / 16:9`
>
> Semantic Source: [`F1_Learning_System_Overview.md`](../../figures/F1_Learning_System_Overview.md)
>
> Source Blob: `32a88e3fa6efa31acc8ed1d396008bcf1210fc70`
>
> Publication Derivative: [`F1_Learning_System_Overview.svg`](../publication/F1_Learning_System_Overview.svg)
>
> Thesis: **LLM / Agent Data 不是“做训练集”，而是在维护 Reality → Experience → Evidence → Learning Signal → Optimization → Deployment → Reality 的 Learning System。**

---

# Slide Contract

```text
Safe area: 120 px from each edge
Title zone: top 150 px
Main visual zone: y=170...850
Footer / source zone: bottom 90 px
```

Progressive reveal 只允许：

```text
增加节点
增加合法边
增加 callout
强调已有对象
```

不允许后续 frame 改变早先出现节点的语义。

---

# Frame F1-1 — Start from Reality

## Visible Objects

```text
Real World
→ Capability / Task Definition
```

## New Objects

```text
Real World
Capability / Task Definition
```

## Hidden Until Later

```text
Experience Acquisition
Experience Objects
Evidence
Learning Signal
Training
Deployment
Feedback loop
Boundary box
Case lens
```

## Speaker Line

> “我不会从‘有什么数据’开始，而是从现实里到底要改变什么行为开始。Data 工作的第一步是把真实问题定义成 capability / task。”

## Transition

从 `Capability / Task Definition` 向右生长下一段。

---

# Frame F1-2 — Experience is the Raw Material

## Visible Objects

```text
Real World
→ Capability / Task Definition
→ Experience Acquisition
→ Experience Objects
```

## New Objects

```text
Experience Acquisition
Experience Objects
```

## Secondary Annotation

只出现一条轻量 band：

```text
Human · Synthetic · Rollout · Production Mining
```

## Hidden Until Later

```text
Evidence readers
Learning Signal types
Training / Deployment
Feedback
Boundary box
C1
```

## Speaker Line

> “接下来才是经验从哪里来。但 Experience Acquisition 和 Experience Object 不能合并：前者是怎么获得，后者是最终记录下来的 Task / Episode / Trajectory / Candidate 等对象。”

## Critical Boundary Introduced

```text
Experience Source
≠ Experience Object
```

---

# Frame F1-3 — Evidence Before Signal

## Visible Objects

在上一帧基础上新增：

```text
Experience Objects
→ Evidence & Evaluation
→ Learning Signal
```

## New Objects

```text
Evidence & Evaluation
Learning Signal
```

## Secondary Annotation

```text
Evidence readers:
Environment Truth · Verifier · Grader / Judge · Human Gold

Signal forms:
SFT · Preference · Reward · Process / Recovery
```

## Speaker Line

> “经验不会自动变成训练信号。先要回答真实发生了什么，再决定怎样把它变成 SFT、preference、reward 或 process signal。”

## Critical Boundary Introduced

```text
Experience ≠ Learning Signal
Evidence ≠ Label
```

---

# Frame F1-4 — Learning Changes the Policy

## Visible Objects

新增：

```text
Learning Signal
→ Training / Optimization
→ New Model / Policy
→ Deployment
```

## Speaker Line

> “训练只是整个系统的一环。Learning Signal 改变 policy，policy 被部署回真实世界，然后才有机会产生新的行为分布。”

## Hidden Until Later

```text
Outcome / Failure / Drift
feedback loop
C1 case lens
```

---

# Frame F1-5 — Close the Loop

## Visible Objects

完整主链：

```text
Real World
→ Capability / Task
→ Experience Acquisition
→ Experience Objects
→ Evidence
→ Learning Signal
→ Training / Optimization
→ New Model / Policy
→ Deployment
→ Outcome / Failure / Drift
↺ Real World
```

## New Objects

```text
Outcome / Failure / Drift
Feedback return arrow
```

## Speaker Line

> “到这里才是 Learning System。现实中的新 failure / drift 回来以后，我们重新判断到底该改 task、tool、harness、evaluator、data，还是 model。”

## Critical Boundary Box

```text
Experience ≠ Learning Signal
Evidence ≠ Label
Training Data ≠ Raw Production Log
Failure ≠ automatically a Data Problem
```

---

# Frame F1-6 — Case Lens / C1

## Visible Objects

保持完整主链，右下角出现 C1 callout：

```text
production failure
→ environment evidence
→ failure diagnosis
→ data / non-data intervention
→ controlled experiment
→ deploy
→ monitor
```

## Speaker Line

> “C1 的意义不是订单退款本身，而是证明一条真实 failure 怎样穿过整套 learning system，而不是直接被塞进训练集。”

## Final Takeaway

> **Learning System 的最小单位不是 dataset，而是可验证的现实问题 → 经验 → 证据 → 学习 → 再验证闭环。**

---

# 30s Version

只播放：

```text
F1-1
→ F1-3
→ F1-5
```

# 90s Version

完整播放：

```text
F1-1 → F1-2 → F1-3 → F1-4 → F1-5 → F1-6
```

# Acceptance

```text
[x] Experience Acquisition 与 Experience Objects 未合并
[x] Evidence 在 Learning Signal 之前
[x] Training 不是起点
[x] Feedback loop 最后出现
[x] C1 只做 case lens，不改变主链
[x] Source SHA recorded
```