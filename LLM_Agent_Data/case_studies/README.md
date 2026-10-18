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

它用同一个 `C1-VB + C1-F1` 把整本书从 Ch10 一路串到 Ch23。

---

# Planned Studies

后续按“不可替代的教学任务”扩，而不是机械地给每个 case 都写一遍全链路：

```text
C2
→ Multi-constraint / Partial Completion / Notification

C3
→ Permission / Side Effect / Harness Ownership

C4
→ Reasoning State / Same-prefix / Selector

C5
→ Executable Truth / Hidden Tests / Verifier Coverage
```

优先原则：

> **每增加一个 Case Study，都必须带来新的诊断 / 数据 /评测结构；换皮案例不单独成篇。**
