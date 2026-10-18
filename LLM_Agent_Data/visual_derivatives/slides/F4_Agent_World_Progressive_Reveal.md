# F4 — Agent Task–Environment–Trajectory / Progressive Reveal

> Derivative Type: `D2 Presentation Storyboard`
>
> Canvas: `1920 × 1080 / 16:9`
>
> Semantic Source: [`F4_Agent_Task_Environment_Trajectory.md`](../../figures/F4_Agent_Task_Environment_Trajectory.md)
>
> Source Blob: `5084a6e0704e3f876e7dd2129ce3089a18301fd0`
>
> Publication Derivative: [`F4_Agent_Task_Environment_Trajectory.svg`](../publication/F4_Agent_Task_Environment_Trajectory.svg)
>
> Thesis: **Agent 不是“模型 + Tool Call”，而是 Task / Case / Model / Harness / Tool / Environment / World State / Observation / Agent-visible State 共同组成的交互系统。**

---

# Frame F4-1 — Task and Case First

## Visible Objects

```text
Task Contract
↓
Case
```

Task Contract 内只保留：

```text
Goal
Constraints
Success
Forbidden
```

Case 内只保留：

```text
Initial World
Permissions
Versions
```

## Speaker Line

> “Agent 运行之前，先要区分 Task 和 Case。Task 定义应该完成什么；Case 冻结这一次具体世界、权限和版本。”

## Hidden Until Later

```text
Model
Harness
Tool
Environment
World State
Observation
Agent-visible State
Trajectory
Outcome
Verifier
```

---

# Frame F4-2 — Runtime Mediation

## Visible Objects

新增：

```text
Model / Policy
→ Harness
→ Action
→ Tool Interface
```

Case 连接 Harness；Model 也连接 Harness。

## Speaker Line

> “Model 不直接操作世界。Harness 是 runtime orchestration：它组 prompt、调用 tool、处理 observation、维护 execution state。”

## Critical Boundary Introduced

```text
Model
≠ Harness
```

---

# Frame F4-3 — Tool Changes the World

## Visible Objects

新增：

```text
Tool Interface
→ Environment / World
→ World State Transition
```

## Speaker Line

> “Tool 只是 action interface；真正定义状态怎样变化的是 Environment。真实 side effect 发生在 World State。”

## Critical Boundary Introduced

```text
Tool
≠ Environment
```

---

# Frame F4-4 — Observation is not World State

## Visible Objects

新增完整回路：

```text
World State
→ Observation
→ Harness
→ Agent-visible State
→ Model / Policy
```

## Speaker Line

> “世界状态不会原样进入模型。Environment 产生 observation，经 Harness 解析、截断、转换或注入后，才形成 Agent-visible State。”

## Critical Boundary Introduced

```text
World State
≠ Observation
≠ Agent-visible State
```

## Hidden Until Later

```text
Trajectory
Outcome
Verifier
C1 / C3 case lens
```

---

# Frame F4-5 — Trajectory Records What Happened

## Visible Objects

在执行主链下方新增：

```text
Action -----------┐
Observation ------┼→ Trajectory / Typed Event Log
World State ------┤
Harness Runtime --┘
```

Trajectory 再指向：

```text
Outcome / Final State
```

## Speaker Line

> “Trajectory 不是另一个执行组件，而是对实际发生过的 Action、Observation、State Transition 和 Runtime Evidence 的记录。”

## Critical Boundary Introduced

```text
Episode
≠ Trajectory
```

---

# Frame F4-6 — Verify Against the Task

## Visible Objects

新增：

```text
Task Contract -.-> Success / Forbidden Predicates
Outcome -------> Success / Forbidden Predicates
```

## Speaker Line

> “最终不是让 Agent 自己说‘我完成了’，而是把 final state 与 Task Contract 中冻结的 success / forbidden predicates 对齐。”

---

# Frame F4-7 — Case Lens

## C1-VB

```text
Task:
shipped → no refund

World State:
status = shipped

Observation:
shipped

Agent-visible State:
status=shipped is in context

Correct next decision:
stop write path
```

## C3-F5 Boundary Callout

```text
Tool backend = failure
Harness-visible observation = success
```

## Speaker Line

> “C1 证明 observation grounding 的问题；C3-F5 则提醒我们 Tool truth 和 Agent-visible observation 之间还隔着 Harness。”

## Final Takeaway

> **Agent Data 的基本对象不是聊天文本，而是一个有 Task、Runtime、World State 与可审计 Trajectory 的交互 Episode。**

---

# 30s Version

```text
F4-1
→ F4-2
→ F4-4
→ F4-5
```

# 90s Version

```text
F4-1 → F4-2 → F4-3 → F4-4 → F4-5 → F4-6 → F4-7
```

# Acceptance

```text
[x] Observation → Harness → Agent-visible State direction preserved
[x] Tool / Harness / Environment remain distinct
[x] Trajectory is evidence record, not runtime component
[x] Task predicates verify final outcome
[x] C1 / C3 case lenses do not alter canonical chain
[x] Source SHA recorded
```