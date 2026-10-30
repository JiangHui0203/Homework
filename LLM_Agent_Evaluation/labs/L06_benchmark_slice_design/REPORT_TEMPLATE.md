# L06 — My Benchmark Slice Design Report

## 1. Evaluation claim

```text
Claim:
Target population:
Unit:
```

## 2. Pool eligibility audit

```text
Pool size:
Direct exposure blockers:
Clean rows blocked by exposed group:
Reference-not-verified:
Non-discriminative:
Fully eligible:
```

解释至少一个 row-level clean / group-level contaminated 的例子。

## 3. Representative view

### Selected tasks

```text
...
```

### Capability mix

| Capability | Selected n | Selected share | Population weight |
|---|---:|---:|---:|
| simple_lookup | | | 50% |
| join_fanout | | | 20% |
| time_scope | | | 15% |
| safe_stop | | | 10% |
| recovery | | | 5% |

### Interpretation

- 为什么这组适合 representative view？
- sampling distribution 与 reporting weight 是否相同？
- 哪些 slice 仍然样本太少？

## 4. Diagnostic view

### Selected tasks

```text
...
```

### Coverage

| Capability | n | Difficulty coverage | High/Critical risk |
|---|---:|---|---:|
| simple_lookup | | | |
| join_fanout | | | |
| time_scope | | | |
| safe_stop | | | |
| recovery | | | |

### Interpretation

说明为什么它是 diagnostic view，而不是 production-frequency estimate。

## 5. Split / leakage audit

```text
Direct exposure:
Contaminated groups:
Within-set duplicate groups:
Cross-set group overlap:
Template overlap:
Reference blockers:
Discrimination blockers:
```

回答：

- 哪些是 hard blocker？
- 哪些只是 warning？
- test exposure 发生后如何更新 asset role？

## 6. Difficulty / discrimination audit

```text
Ceiling items:
Mid-range items:
Floor items:
```

回答：

- 为什么 hard 不等于 discriminative？
- historical pass rate 可以用于什么，不能用于什么？

## 7. Aggregation / weighting

### Representative

```text
Aggregation:
Estimand:
```

### Diagnostic

```text
Aggregation:
Estimand:
```

解释为什么两个 overall 可能不同但都正确。

## 8. Interpretation boundary

### This benchmark supports

```text
...
```

### This benchmark does NOT support

```text
...
```

## 9. Final benchmark design decision

```text
PASS / REVISE
```

列出任何必须修改的 blocker。

## 10. 90-second interview answer

用 90 秒回答：

> 如果让你从一批 Agent tasks 中构造 benchmark，你怎样同时处理 coverage、leakage、natural frequency 和 hard cases？
