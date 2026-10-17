# C2 — Calendar / Meeting Agent

> Case ID: `C2`
>
> 角色：全书 multi-constraint / entity resolution / partial completion 主案例。
>
> 注册表：[`Canonical Casebook`](../00_Canonical_Casebook.md)

---

# C2.0 Base Task

用户请求：

> “把明天下午三点和产品组的会议改到周五下午三点，但周会不要动，并通知所有参会人。”

这个 case 适合讨论：

```text
entity resolution
time normalization
timezone
negative constraint
multi-step write
notification
verification
partial completion
```

---

# C2.1 Stable Environment

```text
Current day: Monday
Timezone: Asia/Shanghai

Event A
id = event_product_1
name = 产品组会议
start = Tuesday 15:00
attendees = Alice, Bob

Event B
id = event_weekly_1
name = 产品组周会
start = Tuesday 16:00
attendees = Alice, Bob, Carol
```

Tools：

```text
calendar.search(query)
calendar.update(event_id, start)
calendar.get(event_id)
notification.send(recipient, message, idempotency_key)
```

Stable constraints：

```text
只修改 Event A
Event B 必须保持不变
Event A 改到 Friday 15:00
Event A 所有参会人必须收到一次通知
不得重复通知
不得修改无关事件
```

---

# C2.2 Success Predicates

```text
Required:
Event A.start == Friday 15:00
Alice notified exactly once
Bob notified exactly once

Forbidden:
Event B changed == true
unrelated event changed == true
notification duplicated == true

Invariant:
Event A attendees unchanged
Event B content unchanged
```

这个 case 是 Required / Forbidden / Invariant 三类 predicate 的标准示例。

---

# C2.3 Canonical Failure Variants

## `C2-F1` — Entity Resolution Failure

```text
search_calendar
→ 同时看到 Event A / Event B
→ update Event B
```

---

## `C2-F2` — Negative Constraint Failure

```text
Event A 被修改
+
Event B 也被修改
```

模型完成了正向目标，但违反“周会不要动”。

---

## `C2-F3` — Partial Completion

```text
Event A 改期成功
但没有通知 Alice / Bob
```

适合说明：

```text
Partial Success
≠ Full Task Success
```

---

## `C2-F4` — Unsupported Success Claim

```text
calendar.update
→ failed
→ final: “已改期并通知参会人”
```

---

## `C2-F5` — No Verification

```text
calendar.update
→ API says success
→ persistent state actually unchanged
→ Agent no read-back
```

---

## `C2-F6` — Duplicate Side Effect

```text
notification.send timeout
→ blind retry
→ Alice receives two notices
```

适合讨论：

```text
idempotency
retry semantics
side-effect accounting
```

---

# C2.4 Canonical State Layers

## World State

```text
真实 calendar event values
notification delivery ledger
```

## Agent-visible State

```text
user request
search results
update response
notification response
```

## Evaluator-only State

```text
expected target event
expected final predicates
notification exactly-once truth
failure labels
```

如果模型只看到 Event A / B 的 display name，而 evaluator 看到稳定 event_id，不能把 evaluator-only ID 泄漏进 Agent input。

---

# C2.5 Canonical Partial-credit Decomposition

对于 `C2-F3`：

```text
Entity Resolution      ✓
Time Normalization     ✓
Calendar Update        ✓
Negative Constraint    ✓
Notification           ✗
Final Task Success     ✗
```

因此：

```text
Outcome = failure
```

并不意味着：

```text
所有 step credit = 0
```

这正好连接 Ch13 的 Credit Assignment。

---

# C2.6 Counterfactual Variants

## `C2-CF1` — Only change exclusion constraint

Base：

```text
但周会不要动
```

Counterfactual：

```text
把两个会议都改到周五下午三点
```

用于测试 negative-constraint sensitivity。

## `C2-CF2` — Only change timezone

```text
Asia/Shanghai → America/Los_Angeles
```

用于测试 time normalization，而不改变其他任务结构。

## `C2-CF3` — Only change notification requirement

```text
通知所有参会人 → 不需要通知
```

用于隔离 partial-completion capability。

---

# C2.7 Derived Data Assets

```text
Entity-resolution Preference
Negative-constraint SFT
Partial-credit Process Labels
Verification Data
Notification Side-effect Data
Time-normalization Benchmark
Human Annotation Boundary Case
Fresh Failure Regression
```

---

# C2.8 Chapter Lens

| Chapter | 使用 C2 看什么 |
|---|---|
| Ch5 | multi-tool trajectory |
| Ch6 | human guideline / ambiguity / adjudication |
| Ch10 | multi-constraint Task Contract |
| Ch11 | time / environment / tool semantics |
| Ch12 | event / notification / state lineage |
| Ch13 | partial completion and step credit |
| Ch14 | entity / constraint / termination failures |
| Ch15 | Required / Forbidden / Invariant verification |
| Ch16 | case-family benchmark split |
| Ch20 | decision-level dedup / hard negative retention |
| Ch21 | held-out family / counterfactual experiment |
| Ch23 | business-rule / timezone / task-mix drift |
| Ch25 | multi-constraint diagnosis example |

---

# C2.9 Stable Language

优先引用：

```text
C2 Base Task
C2-F1 ... C2-F6
C2-CF1 ... C2-CF3
```

不要为了每章方便而把“产品组会议 / 周会 / 通知”规则改成不同版本。

> **C2 的教学价值在于：一个最终失败可以由多项子能力共同决定，而“完成一部分”不等于“任务完成”。**
