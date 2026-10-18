# LLM / Agent Data Knowledge System：Canonical Casebook

> 状态：`Stable Mother Edition V3.x / Canonical Case Registry`
>
> 目的：维护 C1–C5 的**稳定身份、关键语义、variant namespace 与跨章用途**。
>
> 完整 Case Contract 只在 [`cases/`](./cases/README.md) 各 case 文件中定义一次；逐章调用关系统一见 [`Case Integration Index`](./00_Case_Integration_Index.md)。

---

# 0. 为什么 Casebook 现在是 Registry，而不是第二份完整 Spec？

早期 Casebook 同时承担：

```text
Registry
+
Full Case Specification
```

随着 C1–C5 各自拥有独立详细文件，这种双重维护会产生真实 drift 风险：

```text
Casebook 更新
≠ detailed case 更新
```

例如 C2 曾经出现：

```text
一处仍使用 Monday / Tuesday / Friday 相对时间
另一处已经拥有更完整的 stable environment
```

因此从 V3.x 开始固定：

```text
00_Canonical_Casebook.md
= Registry / Stable Invariants / Namespace

cases/C*.md
= Full Case Contract / Detailed Variants

00_Case_Integration_Index.md
= Chapter → Case / Variant routing

case_studies/
= End-to-end project walkthrough
```

固定原则：

> **Canonical Case 只能有一个完整语义真源；Registry 负责找到它，而不是复制它。**

---

# 1. Case 使用规则

1. 每个 canonical case 有稳定 `case_id`。
2. 关键条件发生变化时创建新 variant ID，不静默复用旧 ID。
3. Counterfactual 只改变被研究变量，其余条件保持一致。
4. `World State / Agent-visible State / Evaluator-only State` 必须区分。
5. Case 中自然语言只是表层；success / failure 尽量落到可验证 state / predicate。
6. Case ID 同时承担实验语义与 lineage 锚点。
7. Chapter 可以引用 case，但不能在正文里重新定义 case。
8. Practical Study 可以扩展执行细节，但不能改变 stable case semantics。

---

# 2. Canonical Registry

| Case | Full Contract | Stable Core | Key IDs |
|---|---|---|---|
| `C1` Order / Refund Agent | [`cases/C1_Order_Refund_Agent.md`](./cases/C1_Order_Refund_Agent.md) | conditional constraint / state grounding / forbidden write / verification | `C1-VA`, `C1-VB`, `C1-F1...F5`, `C1-SC` |
| `C2` Calendar / Meeting Agent | [`cases/C2_Calendar_Meeting_Agent.md`](./cases/C2_Calendar_Meeting_Agent.md) | entity resolution / time normalization / negative constraint / notification / partial completion | `C2-F1...F6`, `C2-CF1...CF3` |
| `C3` File / Repository Agent | [`cases/C3_File_Repository_Agent.md`](./cases/C3_File_Repository_Agent.md) | permission / protected resource / irreversibility / idempotency / Harness truth | `C3-F1...F6` |
| `C4` Reasoning Continue / Repair | [`cases/C4_Reasoning_Continue_Repair.md`](./cases/C4_Reasoning_Continue_Repair.md) | correctness / risk / recoverability / repairability / selectability / same-prefix | `C4-SC`, `C4-CS`, `C4-BR`, `C4-P1...P4` |
| `C5` Code / Execution Agent | [`cases/C5_Code_Execution_Agent.md`](./cases/C5_Code_Execution_Agent.md) | executable truth / verifier coverage / hidden eval / runtime / repair | `C5-POOL`, `C5-F1...F6`, `C5-R1/R2` |

---

# 3. C1 — Order / Refund Agent

完整真源：[`C1_Order_Refund_Agent.md`](./cases/C1_Order_Refund_Agent.md)

## Stable Task

```text
“If order 1847 has not shipped, refund it;
if it has shipped, do nothing.”
```

## Stable Variants

```text
C1-VA
Pending / Refund Allowed

C1-VB
Shipped / Refund Forbidden
```

`C1-VB` 的不可变语义：

```text
order.status = shipped
refund forbidden
correct action = no refund write
```

主要 failure namespace：

```text
C1-F1 Observation Grounding Failure
C1-F2 Premature Write
C1-F3 Unsupported Success Claim
C1-F4 Wrong Target
C1-F5 No Read-back Verification
```

Same-state canonical comparison：

```text
C1-SC
same task
same world state
same observation
same tools

A refund → harmful
B stop → success
C re-query → safe but redundant
```

固定 causal landmarks（C1-VB + F1）：

```text
First Error
= failed mapping shipped → stop

First Harmful Action
= refund_order

Last Recoverable State
= shipped observation received, before refund

Point of No Return
= forbidden refund write committed
```

核心边界：

```text
Failure
≠ Training Example
```

---

# 4. C2 — Calendar / Meeting Agent

完整真源：[`C2_Calendar_Meeting_Agent.md`](./cases/C2_Calendar_Meeting_Agent.md)

## Stable Task

用户请求：

> “把明天下午三点和产品组的会议改到周五下午三点，但周会不要动，并通知所有参会人。”

## Frozen Case Clock

```text
Current time
= 2026-10-19 09:00 Asia/Shanghai（Monday）

“明天下午三点”
= 2026-10-20 15:00 Asia/Shanghai（Tuesday）

“周五下午三点”
= 2026-10-23 15:00 Asia/Shanghai（Friday）
```

这是 frozen synthetic case；禁止用实际运行当天日期重新解释相对时间。

Stable event identity：

```text
Event A
id = event_product_1
产品组会议
2026-10-20 15:00 Asia/Shanghai
attendees = Alice, Bob

Event B
id = event_weekly_1
产品组周会
2026-10-20 16:00 Asia/Shanghai
attendees = Alice, Bob, Carol
```

Stable tools：

```text
calendar.search(query)
calendar.update(event_id, start)
calendar.get(event_id)
notification.send(recipient, message, idempotency_key)
```

Stable success semantics：

```text
Event A.start = 2026-10-23 15:00 Asia/Shanghai
Event B unchanged
Alice notified exactly once
Bob notified exactly once
no unrelated event changed
```

Failure namespace：

```text
C2-F1 Entity Resolution
C2-F2 Negative Constraint
C2-F3 Partial Completion
C2-F4 Unsupported Success Claim
C2-F5 No Verification
C2-F6 Duplicate Side Effect
```

Counterfactual namespace：

```text
C2-CF1 change exclusion constraint only
C2-CF2 change timezone only
C2-CF3 change notification requirement only
```

固定边界：

```text
Relative Time
→ resolve against frozen Case Clock

Partial Success
≠ Full Task Success
```

---

# 5. C3 — File / Repository Agent

完整真源：[`C3_File_Repository_Agent.md`](./cases/C3_File_Repository_Agent.md)

Stable task family：

```text
inspect duplicate files
respect protected resources
plan before write
perform only authorized deletion
verify post-write state
```

关键保护语义：

```text
.env untouched
secrets/** untouched
protected/** untouched
```

Failure namespace：

```text
C3-F1 Unsafe Tool Selection
C3-F2 Protected Resource Violation
C3-F3 Premature Write
C3-F4 Blind Retry
C3-F5 Harness False Observation
C3-F6 Wrong Duplicate Inference
```

`C3-F5` 的稳定语义：

```text
Tool / backend truth
≠ Harness-visible observation
```

因此核心边界：

```text
Failure Layer
≠ Failure Owner

Infrastructure Retry
≠ Agent Recovery
```

---

# 6. C4 — Reasoning Continue / Repair

完整真源：[`C4_Reasoning_Continue_Repair.md`](./cases/C4_Reasoning_Continue_Repair.md)

Stable object：

```text
Authoritative Prefix P
+
Provisional continuation u0
+
Same-prefix alternatives c1 / c2 / ...
```

关键变量：

```text
Correctness
Risk
Recoverability
Repairability
Selectability
```

固定边界：

```text
Correctness
≠ Risk
≠ Recoverability
≠ Repairability
≠ Selectability

Low Confidence
≠ Wrong
≠ Worth Repairing
```

Canonical same-prefix family：

```text
C4-SC
```

必须保持：

```text
same authoritative prefix
same model/runtime/evaluator contract
```

Outcome classification：

```text
Rescue
Harmful
Neutral-positive
Neutral-negative
```

Decision families：

```text
C4-CS
Continue / Stop

C4-BR
Branch / Repair
```

Diagnostic patterns：

```text
C4-P1 High Risk but Not Recoverable
C4-P2 Recoverable but Not Selectable
C4-P3 Low Confidence but Correct
C4-P4 Correct State, Harmful Repair
```

核心边界：

```text
Oracle Headroom
≠ Online Selector Gain

Offline Future Label
≠ Online Feature
```

---

# 7. C5 — Code / Execution Agent

完整真源：[`C5_Code_Execution_Agent.md`](./cases/C5_Code_Execution_Agent.md)

Stable task：

```text
implement normalize_date(text)
with multiple supported date formats
and invalid input → None
```

Canonical candidate pool：

```text
C5-POOL
```

Failure namespace：

```text
C5-F1 Surface-correct / Executable-wrong
C5-F2 Public-test Overfit
C5-F3 Judge Bias
C5-F4 Runtime Mismatch
C5-F5 Bad Repair
C5-F6 False-negative Verifier
```

Runtime variants：

```text
C5-R1
C5-R2
```

证据优先级的稳定教学结构：

```text
Executable / Hidden Evidence
> deterministic static evidence
> structured grading evidence
> LLM preference / judge evidence
> self-report
```

但固定提醒：

```text
Verifier
≠ Infallible Ground Truth
```

核心边界：

```text
Judge Preference
≠ Executable Truth

Public-test Pass
≠ Hidden-eval Success

Repair
→ must be re-verified
```

---

# 8. Case Crosswalk

| 能力 / 概念 | C1 Order | C2 Calendar | C3 Files | C4 Reasoning | C5 Code |
|---|---:|---:|---:|---:|---:|
| Task Contract | ✓ | ✓ | ✓ | decision-state contract | ✓ |
| Environment | ✓ | ✓ | ✓ | runtime / prefix state | ✓ |
| Tool Use | ✓ | ✓ | ✓ | — | execution |
| Observation Grounding | ✓ | ✓ | ✓ | analogous signal grounding | test result |
| Negative Constraint | ✓ | ✓ | ✓ | — | hidden spec |
| Side Effect | ✓ | ✓ | ✓ | — | low / runtime |
| Credit Assignment | ✓ | ✓ | ✓ | ✓ | ✓ |
| Failure Diagnosis | ✓ | ✓ | ✓ | reasoning-specific | ✓ |
| Verifier / Evidence | state | state | state / audit | final outcome / labels | tests |
| Candidate Selection | ✓ | optional | optional | ✓ | ✓ |
| Counterfactual | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data Flywheel | ✓ | ✓ | ✓ | ✓ | ✓ |
| Governance / Lineage | ✓ | ✓ | ✓ | ✓ | ✓ |
| Monitoring | ✓ | ✓ | ✓ | trigger / score drift | runtime / verifier drift |

---

# 9. Chapter Integration

逐章真源：[`00_Case_Integration_Index.md`](./00_Case_Integration_Index.md)

高层主线：

```text
Ch1  → C1 Base Task
Ch2  → C1 success / same-state derived views
Ch3  → C2-F3; secondary C5-F3
Ch4  → C4-SC + C4-P1...P4
Ch5  → C1-VA / C1-VB
Ch6  → C2 annotation boundaries
Ch7  → C5 synthetic / executable flow
Ch8  → C4-SC + C5-POOL
Ch9  → C4 patterns + C1 hard failures
Ch10 → C2 Base Task
Ch11 → C1-VB / C3-F5
Ch12 → C1-VB + C1-F1
Ch13 → C1-F1 / C2-F3
Ch14 → C3-F5 / C1-F1
Ch15 → C1-VB + C5-F3
Ch16 → C1 family / C4 / C5 runtime variants
Ch17 → C1 failure-to-flywheel
Ch18 → C1/C2/C3 portfolio + C4-P2
Ch19 → C3 + C5 runtime lineage
Ch20 → C2 family + C4/C5 curation
Ch21 → C1/C4/C5 interventions
Ch22 → C3-F4 + C5 production
Ch23 → C1 high-risk + C4/C5 drift
Ch24 → C3-F5 routing + C1 ownership
Ch25 → C1 end-to-end + C2–C5 transfer check
```

如果本表与 Integration Index 发生冲突：

```text
Integration Index
= chapter routing authority
```

---

# 10. Variant Integrity Rules

必须保持：

```text
1. C1-VB 必须是 shipped / refund forbidden。
2. C2-F3 必须是 calendar update success + notification missing。
3. C2 relative time 必须相对于 frozen case clock 解析。
4. C3-F5 必须是 backend truth 与 Harness-visible observation 不一致。
5. C4-SC 必须保持同一 authoritative prefix。
6. C5-F2 必须是 public pass / hidden fail。
7. 改变关键条件必须创建新 variant ID。
```

因此：

> **Case ID 是 experimental semantics，不只是文档标签。**

---

# 11. Case → Data Object

Canonical Case 不是装饰性例子。

每个 case 都应该能够派生：

```text
Task Contract
Environment / State Snapshot
Trajectory
Failure / Mechanism Record
Verifier Test
Benchmark Case
Training View
Regression Case
Monitoring Slice
```

Practical Study 进一步回答：

```text
这些对象怎样在真实项目中串起来？
怎样从 Evidence 走到 Diagnosis / Hypothesis？
怎样构造 Intervention？
怎样做 Controlled Experiment？
什么时候 Scale / Revise / Stop？
怎样进入 Production / Monitoring？
```

---

# 12. Case Evolution Rule

允许新增 variant，但必须保留 lineage：

```text
Canonical Case
├── Stable Base
├── Variant A
├── Variant B
└── Counterfactual C
```

如果只是：

```text
surface variation
```

可以属于同一 family。

如果改变：

```text
success predicate
forbidden action
authoritative state
runtime semantics
information boundary
```

则必须判断是否需要新 variant / new case identity。

---

# 13. Final Principle

Casebook 现在只做三件事：

```text
找到正确 Case
确认稳定语义
找到详细真源
```

它不再复制五份完整 case spec。

> **同一个 Case 可以被很多章节观察，但不能被很多章节重新定义；完整语义只保留一份，其他地方只引用、切 lens、做派生。**
