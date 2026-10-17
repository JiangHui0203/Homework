# C5 — Code / Execution Agent

> Case ID: `C5`
>
> 角色：全书 executable verification、Best-of-N、hidden eval、runtime mismatch、repair 与 verifier coverage 主案例。
>
> 注册表：[`Canonical Casebook`](../00_Canonical_Casebook.md)

---

# C5.0 Base Task

用户任务：

> “实现函数 `normalize_date(text)`，支持 ISO 日期、`YYYY/MM/DD` 和简单英文月份格式；非法输入返回 `None`。”

目标不是“写一段看起来像代码的文本”，而是：

```text
implementation
→ execute
→ satisfy spec
→ pass held-out cases
```

---

# C5.1 Stable Contract

Function：

```python
normalize_date(text) -> str | None
```

Required behavior：

```text
2026-10-18      → 2026-10-18
2026/10/18      → 2026-10-18
Oct 18, 2026    → 2026-10-18
invalid         → None
2026-02-30      → None
```

Stable evaluation layers：

```text
Syntax
Public Unit Tests
Hidden Tests
Runtime / Dependency Check
Optional Style / Maintainability Rubric
```

硬原则：

> Executable correctness 优先于语言解释或代码外观。

---

# C5.2 Candidate Pool — `C5-POOL`

同一 Task 生成：

```text
Candidate A
Candidate B
Candidate C
Candidate D
```

每个 candidate 独立执行：

```text
syntax check
→ public tests
→ hidden tests
→ runtime check
```

得到：

```text
candidate_id
code
execution result
failure type
test coverage
cost
```

这个 pool 可以用于：

```text
Best-of-N
Rejection Sampling
Verifier Selection
Preference Construction
Hard Negative Mining
```

---

# C5.3 Canonical Failure Variants

## `C5-F1` — Surface-correct, Executable-wrong

解释清晰、代码结构漂亮，但 unit tests fail。

说明：

```text
Judge Style Score high
≠ Program Correctness
```

---

## `C5-F2` — Public-test Overfit

```text
public tests pass
hidden invalid-date case fails
```

适合讨论：

```text
Verifier Coverage
Held-out Evaluation
Benchmark Leakage
```

---

## `C5-F3` — Judge Bias

LLM Judge 更偏爱结构漂亮但错误的 Candidate A，而 executable verifier 判 Candidate B 正确。

用于固定评价优先级：

```text
Executable Evidence
>
LLM Stylistic Judgment
```

---

## `C5-F4` — Runtime Mismatch

```text
local dev runtime pass
production runtime fail
```

原因可能是：

```text
Python version
dependency version
locale
timezone
OS behavior
```

说明：

```text
Code artifact
+
Runtime Environment
```

共同定义可执行结果。

---

## `C5-F5` — Bad Repair

第一次 test failure 后，模型只针对 visible failing case patch：

```text
public test repaired
hidden generalization worsened
```

适合讨论：

```text
local repair
≠ general repair
```

---

## `C5-F6` — False-negative Verifier

正确 implementation 被有 bug 的 checker 判错。

说明：

```text
Model Failure
≠ Evaluator Failure
```

---

# C5.4 Evidence Hierarchy

对 C5，优先级通常是：

```text
Hidden / Executable Test Evidence
>
Deterministic Static Checks
>
Structured Grader
>
LLM Judge
>
Model Self-report
```

但 verifier 也不是天然真理：

```text
coverage insufficient
buggy expected output
runtime mismatch
flaky test
```

都会导致错误评价。

因此 verifier 自身也要版本化、校准和回归测试。

---

# C5.5 Oracle vs Selector

对于 `C5-POOL`：

## Oracle

```text
pool 中是否至少有一个 candidate 通过完整 executable suite？
```

## Selector

```text
在线可用的 scorer 能否在不偷看 hidden outcome 的情况下选中更好的 candidate？
```

例如 selector 可能使用：

```text
public tests
static features
model score
partial execution
```

但如果 hidden test 只用于 offline truth，就不能泄漏给在线 selector。

---

# C5.6 Verifier Coverage Counterfactual

固定 candidate，改变 verifier coverage：

```text
V1 syntax only
V2 syntax + public tests
V3 syntax + public + hidden tests
```

观察：

```text
accepted candidate set
false positive rate
false negative rate
training data quality
```

可以直接证明：

> Better verifier coverage may change the dataset distribution itself.

---

# C5.7 Runtime Variant Set

## `C5-R1`

```text
Python 3.x / dependency set A
```

## `C5-R2`

```text
Python 3.x / dependency set B
```

Task 与 code 不变，只改变 runtime。

用于隔离：

```text
Model capability
vs Environment compatibility
```

---

# C5.8 Derived Data Assets

```text
Correct Code SFT
Chosen / Rejected Code Pair
Executable Hard Negative
Repair Trajectory
Verifier Training / Test Set
Hidden-eval Regression
Runtime-compatibility Benchmark
Candidate Selection Pool
Synthetic Code Task Seed
```

---

# C5.9 Chapter Lens

| Chapter | 使用 C5 看什么 |
|---|---|
| Ch7 | synthetic task / response generation |
| Ch8 | Best-of-N / rejection / oracle / selector |
| Ch15 | executable verifier vs judge |
| Ch16 | hidden eval / frozen runtime / claim scope |
| Ch19 | code / runtime / verifier version lineage |
| Ch20 | executable filtering / semantic-vs-functional dedup |
| Ch21 | source / verifier / repair data experiment |
| Ch22 | sandbox worker / artifact / runtime production |
| Ch23 | runtime / dependency / verifier drift |
| Ch25 | verifiable-data diagnosis |

---

# C5.10 Stable Language

优先引用：

```text
C5-POOL
C5-F1 ... C5-F6
C5-R1 / C5-R2
```

> **C5 的核心价值，是不断提醒读者：对可执行任务，文本“看起来正确”永远不能替代运行证据；同时，Verifier 的 coverage 与 runtime 本身也必须成为数据和评测对象。**
