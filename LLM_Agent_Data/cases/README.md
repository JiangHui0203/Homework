# Canonical Cases

这组文件是 `LLM / Agent Data Knowledge System` 的稳定贯穿案例层。

总注册表：[`../00_Canonical_Casebook.md`](../00_Canonical_Casebook.md)

逐章接入表：[`../00_Case_Integration_Index.md`](../00_Case_Integration_Index.md)

Practical Walkthrough：[`../case_studies/README.md`](../case_studies/README.md)

两层职责必须分开：

```text
cases/
= Case Contract / Stable IDs / Variants

case_studies/
= End-to-end Walkthrough / Artifacts / Decisions
```

因此 Case Study 可以继续扩展项目执行细节，但不能静默改变这里定义的 stable case semantics。

---

## Case Registry

| Case | 核心问题 | 关键 ID | Practical Study |
|---|---|---|---|
| [C1 Order / Refund Agent](./C1_Order_Refund_Agent.md) | 条件约束、状态读取、write、verification、side effect | `C1-VA`, `C1-VB`, `C1-F1...F5`, `C1-SC` | [End-to-End Walkthrough](../case_studies/C1_End_to_End_Walkthrough.md) |
| [C2 Calendar / Meeting Agent](./C2_Calendar_Meeting_Agent.md) | entity resolution、negative constraint、partial completion、notification | `C2-F1...F6`, `C2-CF1...CF3` | planned |
| [C3 File / Repository Agent](./C3_File_Repository_Agent.md) | permission、protected resource、irreversibility、idempotency、Harness | `C3-F1...F6` | planned |
| [C4 Reasoning Continue / Repair](./C4_Reasoning_Continue_Repair.md) | correctness / risk / recoverability / selectability、same-prefix | `C4-SC`, `C4-CS`, `C4-BR`, `C4-P1...P4` | planned |
| [C5 Code / Execution Agent](./C5_Code_Execution_Agent.md) | executable verifier、hidden eval、runtime、repair | `C5-POOL`, `C5-F1...F6`, `C5-R1/R2` | planned |

---

## 引用原则

正文中优先引用稳定 ID，例如：

```text
沿用 `C1-VB`：订单已经 shipped，任务要求禁止退款。
```

或：

```text
使用 `C4-SC`：保持 authoritative prefix 不变，只替换当前 continuation。
```

而不是重新编一个相似但条件不同的例子。

如果需要改变 canonical case 的关键条件：

```text
创建新的 variant ID
```

不要偷偷复用旧 ID。

---

## Case 不是装饰性例子

每个 case 都应该能够被转换成真实的数据对象：

```text
Task Contract
Environment Snapshot
Trajectory
Failure Record
Verifier Test
Benchmark Case
Training View
Regression Case
Monitoring Slice
```

而 Practical Case Study 进一步回答：

```text
这些对象怎样在一个项目中串起来？
怎样从 Failure 走到 Capability Gap？
怎样设计 Data Intervention？
怎样做 Controlled Experiment？
什么时候 Scale / Stop？
怎样进入 Production / Governance / Monitoring？
```

因此：

> **Canonical Case ID 是实验语义和数据 lineage 的锚点；Practical Case Study 则是这套语义在真实项目工作流中的展开。**
