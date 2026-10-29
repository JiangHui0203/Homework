# L04 — Reference Solution

> 先独立完成再看。本答案给出一种可辩护标注，不意味着所有 root-cause wording 只有唯一写法。

## 1. Frozen outcome

```text
baseline  = 6/8 = 75.0%
candidate = 4/8 = 50.0%

wins      = 1
losses    = 3
both_ok   = 3
both_fail = 1
net       = -2/8
```

paired movement：

```text
T02 LOSS
T03 LOSS
T05 WIN
T07 LOSS
T06 BOTH_FAIL
```

因此 candidate 的总体下降是真实 paired outcome observation，但不能仅凭这 8 题宣布某个统一能力退化。

## 2. Reference failure reviews

### E04 — candidate / join_fanout

```text
Symptom:
wrong numeric answer delivered

First meaningful failure:
E1 plan loses order-level grain

Immediate mechanism:
raw item × payment join causes fanout before SUM

Root cause:
planner failed to preserve aggregation grain

Evidence:
OBSERVED

Owner:
model/controller
```

E2 的 SQL 错误是 E1 的 propagated manifestation；E5 的 wrong final answer 是 symptom，不应反过来当 root cause。

### E06 — candidate / schema_memory

```text
Symptom:
schema checker rejects nonexistent table

First meaningful failure:
E1 stale/incompatible memory is injected

Immediate mechanism:
analysis follows stale table name `payments`

Root cause:
memory compatibility/versioning failure

Evidence:
SUPPORTED
```

为什么可以到 `SUPPORTED`：数据明确给了 counterfactual note——移除 stale memory 后同任务能选择当前表并完成。

### E09 — baseline / verification_recovery

```text
Symptom:
episode terminates after actionable verifier error

First meaningful failure:
E2 controller refuses retry despite retryable=true

Immediate mechanism:
recovery policy does not execute permitted retry

Root cause:
recovery controller fails to act on actionable verifier feedback

Evidence:
OBSERVED
```

E0 malformed JSON 是 first local error，但它本身是可恢复的；真正把 episode 推向 failure 的是 E2。

### E11 / E12 — sql_scope

```text
Symptom:
DuckDB binder rejects alias

First meaningful failure:
E1 out-of-scope alias reference

Immediate mechanism:
generated SQL is unbindable

Root cause:
general alias-scope weakness

Evidence:
HYPOTHESIS
```

trace 能直接证明 alias misuse，但“一般性能力缺陷”需要更多同类案例，因此 root cause 只能写 hypothesis。

### E14 — candidate / answer_synthesis

```text
Symptom:
wrong monetary value accepted

First meaningful failure:
E2 final synthesis drops cents→dollars conversion

Immediate mechanism:
unit metadata is ignored in final rendering

Root cause:
unit-aware synthesis / validation gap

Evidence:
OBSERVED
```

## 3. 不应标成 episode failure 的 recovered cases

### E10

E0 malformed JSON 是局部错误，但 E1 提供可执行反馈，E2 正确 retry，之后成功完成。

因此：

```text
first local error exists
episode-level first meaningful failure = NONE
```

### E16

第一次 timeout 被正确识别为 transient fault，并在预算内一次 retry 成功。

因此同样不应因为出现 `VIOLATION` 就把 episode 记成 failure。

## 4. Slice diagnosis

candidate loss 分布在：

```text
join_fanout
schema_memory
answer_synthesis
```

而 candidate 在 `verification_recovery` 还有一次 win。

所以这批小样本不支持“candidate 统一变差于某一个机制”的结论。更合理的是：

- 先把 E04/E06/E14 分别形成 regression candidates；
- E11/E12 属于 baseline/candidate 共存 failure，不是 candidate-specific regression；
- 对 root-cause hypothesis 再做 replay / counterfactual。

## 5. 最适合直接工程化的 fixtures

```text
E04: raw fanout aggregation regression
E06: stale memory version mismatch
E09: retryable verifier failure must trigger one retry
E11/E12: out-of-scope SQL alias
E14: cents/dollars unit preservation
```

fixture 要验证可观测 contract，不要把“模型为什么会犯错”的假说硬编码成测试。
