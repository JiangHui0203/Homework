# F6 — Credit → Failure Causal Map / Progressive Reveal

> Derivative Type: `D2 Presentation Storyboard`
>
> Canvas: `1920 × 1080 / 16:9`
>
> Semantic Source: [`F6_Credit_to_Failure_Causal_Map.md`](../../figures/F6_Credit_to_Failure_Causal_Map.md)
>
> Source Blob: `a343e95aaf74cd98fda331d4ef4987a240cc7c02`
>
> Publication Derivative: [`F6_Credit_to_Failure_Causal_Map.svg`](../publication/F6_Credit_to_Failure_Causal_Map.svg)
>
> Thesis: **Failure Analysis 不能从最终 Outcome 直接跳到 Root Cause；First Error、First Harmful Action、Recoverability、Mechanism 和 Failure Owner 必须逐层拆开。**

---

# Frame F6-1 — Outcome is Only the Start

## Visible Objects

```text
Observed Outcome
↓
First Error
↓
First Harmful Action
```

## Speaker Line

> “看到 final failure 只能说明结果不好。第一步是找最早的局部错误，再区分什么时候这个错误真正变成 harmful action。”

## Critical Boundary Introduced

```text
First Error
≠ First Harmful Action
```

---

# Frame F6-2 — Where Could We Still Recover?

## Visible Objects

新增：

```text
First Harmful Action
↓
Last Recoverable State
↓
Point of No Return
```

旁边出现辅助链：

```text
Last Recoverable State
-.-> Recoverability
-.-> Repairability
```

## Speaker Line

> “接下来不是马上找 root cause，而是问：在什么状态之前还有更好的未来？更好的未来存在，不等于当前 action space 和预算下真的修得了。”

## Critical Boundary Introduced

```text
Recoverability
≠ Repairability
```

---

# Frame F6-3 — From Symptom to Mechanism

## Visible Objects

新增：

```text
Point of No Return
↓
Failure Symptom
↓
Immediate Mechanism
```

## Speaker Line

> “Symptom 是我们看到的失败表现；Mechanism 是直接导致它发生的机制。二者仍然不是 Root Cause。”

## Hidden Until Later

```text
Root Cause
Failure Owner
Intervention Routing
Counterfactual Credit
Case comparison
```

---

# Frame F6-4 — Root Cause and Owner

## Visible Objects

新增：

```text
Immediate Mechanism
↓
Root Cause
↓
Failure Owner
↓
Intervention Routing
```

## Speaker Line

> “Root Cause 负责解释为什么这类 failure 会发生；Failure Owner 决定谁应该先修。表面错误发生在哪一层，不等于真正 owner 在哪一层。”

## Critical Boundary Introduced

```text
Failure Layer
≠ Failure Owner
```

---

# Frame F6-5 — Credit is a Parallel Question

## Visible Objects

新增第二条辅助链：

```text
First Harmful Action
-.-> Counterfactual Credit
-.-> Learning Signal
```

## Speaker Line

> “Credit Assignment 和 Failure Diagnosis 有交集，但不是同一件事。Credit 问哪个 decision 改变了 outcome；Diagnosis 问为什么会做出这个 decision、应该修谁。”

---

# Frame F6-6 — C1-F1

## Case Callout

```text
Observation: shipped
↓
First Error:
shipped 没被映射成 stop
↓
First Harmful:
refund_order(1847)
↓
Last Recoverable:
write 前
↓
Root Cause:
conditional policy / observation grounding
↓
Owner:
Model / Policy
```

## Speaker Line

> “C1 是典型 model-owned failure。这个 case 说明错误、伤害、恢复边界和 root cause 分别落在不同位置。”

---

# Frame F6-7 — C3-F5 Contrast

## Second Case Callout

```text
Tool backend = failure
↓
Harness-visible observation = success
↓
Agent receives false success
↓
Agent reports completed
```

## Speaker Line

> “C3-F5 表面 symptom 在 Agent 输出层，但真正 root cause 和 owner 是 Harness。这就是为什么不能把所有 bad case 都直接路由给 Model / Data。”

## Final Takeaway

> **Failure Analysis 的终点不是一个标签，而是可信的 Owner + Intervention Routing。**

---

# 30s Version

```text
F6-1
→ F6-2
→ F6-4
→ F6-7
```

# 90s Version

```text
F6-1 → F6-2 → F6-3 → F6-4 → F6-5 → F6-6 → F6-7
```

# Acceptance

```text
[x] First Error / First Harmful / Root Cause remain distinct
[x] Recoverability / Repairability branch retained
[x] Counterfactual Credit remains auxiliary, not causal-spine replacement
[x] Failure Layer / Owner distinction preserved
[x] C1 / C3 contrast used only after canonical chain is established
[x] Source SHA recorded
```