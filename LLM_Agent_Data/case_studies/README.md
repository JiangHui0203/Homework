# Practical Case Studies

本目录负责把 `Canonical Cases` 从“稳定案例定义”推进成“完整工作流演练”。

两层必须分开：

```text
../cases/
= Case Contract / Stable IDs / Variants

./case_studies/
= End-to-end Walkthrough / Artifacts / Decisions
```

因此 Case Study 可以增加：

```text
Trajectory Example
Failure Record
Evaluation Contract
Derived Data Assets
Data Intervention Plan
Controlled Experiment
Production Contract
Monitoring Plan
Decision Memo
```

但不能静默改变：

```text
C1–C5 stable ID semantics
Task Contract
canonical failure variant meaning
```

原则：

> **每增加一个 Case Study，都必须带来新的诊断 / 数据 / 评测结构；换皮案例不单独成篇。**

---

# Current Studies

## C1 — Order / Refund Agent

- [`C1_End_to_End_Walkthrough.md`](./C1_End_to_End_Walkthrough.md)

主链：

```text
Task / Case
→ Environment / Runtime
→ Trajectory
→ Evidence
→ Credit / Failure
→ Capability Gap
→ Derived Data
→ Controlled Experiment
→ Production / Governance
→ Monitoring / Flywheel
```

它用同一个 `C1-VB + C1-F1 + C1-SC` 把整本书从 Ch10 一路串到 Ch23。

核心教学任务：

> **一条真实 Agent failure 怎样变成一个完整 Data Learning Loop。**

---

## C3 — File / Repository Agent

- [`C3_Permission_Harness_Ownership_Walkthrough.md`](./C3_Permission_Harness_Ownership_Walkthrough.md)

主链：

```text
Permission / Protected Resource
→ Side-effecting Write
→ Tool Truth
→ Harness Observation
→ Agent-visible State
→ Failure Layer / Owner
→ Idempotency / Retry
→ System vs Model Intervention
→ Regression / Monitoring
```

主要使用：

```text
C3-F2  Protected Resource Violation
C3-F4  Blind Retry
C3-F5  Harness False Observation
```

核心教学任务：

> **表面 Agent failure 为什么可能真正属于 Tool / Harness / Permission System，以及真实 write side effect 下为什么必须把 authorization、idempotency 与 world-state verification 放进同一个协议。**

---

## C4 — Reasoning Continue / Repair

- [`C4_Reasoning_Intervention_Walkthrough.md`](./C4_Reasoning_Intervention_Walkthrough.md)

主链：

```text
Reasoning State
→ Online Risk Signal
→ Trigger
→ Same-prefix Candidate Pool
→ Oracle Headroom
→ Selector
→ Rescue / Harmful / Net
→ Population Accounting
→ Cost-aware E2E Evaluation
→ Monitoring / Calibration
```

主要使用：

```text
C4-SC
C4-CS
C4-BR
C4-P1...P4
```

核心教学任务：

> **把“reasoning state 看起来可疑”拆成一个可审计的 Trigger / Generator / Oracle / Selector / E2E / Cost 系统。**

固定边界：

```text
Risk Signal
≠ Error Detector

Oracle Gap
≠ Selector Gain

Selector Gain
≠ E2E Gain

E2E Gain
≠ Cost-effective Gain
```

---

# Three-study Coverage

当前三篇 walkthrough 已经覆盖三类彼此不可替代的问题空间：

| Study | 主要世界 | 核心问题 |
|---|---|---|
| C1 | External Agent Decision | failure 怎样进入完整 data learning loop |
| C3 | Runtime / Permission / Side Effect | failure layer 和 failure owner 为什么不同 |
| C4 | Explicit Reasoning Intervention | trigger / candidate / selector / cost 怎样拆解 |

可以压成：

```text
C1
→ Should this behavior become learning data?

C3
→ Is the model even the right owner to fix?

C4
→ Does intervention headroom actually convert into online value?
```

这三问已经覆盖大多数 Agent Data / Reasoning Data 项目最容易误判的三个层级。

---

# Planned Studies

后续不机械追求 C1–C5 全部各写一篇。

只有在提供新的不可替代结构时才继续：

```text
C2
→ Multi-constraint / Partial Completion / Notification

C5
→ Executable Truth / Hidden Tests / Verifier Coverage
```

当前优先级低于：

```text
C1 / C3 / C4
```

因为 C2 的部分结构已被 C1 覆盖，C5 的价值主要在 executable verification，适合后续与代码 / verifier 专题一起扩。
