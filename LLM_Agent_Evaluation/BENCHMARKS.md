# Benchmarks Registry

> 本文件维护 benchmark / eval set 的**测量语义与资产角色**，不维护某次运行分数。

## Benchmark Card 最小字段

```text
Benchmark ID / Name
Role: representative / frozen-core / regression / hard / fresh
Target claim / capability
Target population
Task / environment
Unit of evaluation
Sampling frame / construction method
Coverage matrix
Slice metadata
Difficulty policy
Risk policy
Reference / evaluator
Split / grouping policy
Leakage / contamination risk
Exposure status
Stochasticity / repeats
Budget / environment snapshot
Aggregation / weighting
Version / manifest / hash
Known limitations
Recommended use
Not recommended use
Promotion / retirement policy
Related frozen experiments
```

## Benchmark 不是只有“题目”

一个可审计 benchmark 至少是：

```text
Items
+ Environment
+ Reference / evaluator
+ Sampling semantics
+ Protocol
+ Aggregation
+ Version
```

只保存 prompts，而没有 reference、split、environment、aggregation 和 version，不能稳定支撑跨版本结论。

## Benchmark Portfolio Roles

| Role | 主要问题 | Exposure | 典型用途 | 不能直接证明 |
|---|---|---|---|---|
| Representative | 目标总体平均表现怎样？ | controlled | population estimate | 稀有 failure 都可靠覆盖 |
| Frozen Core | 长期趋势是否退化？ | grows over time | longitudinal / release | fresh generalization |
| Regression | 已知 bug 是否复发？ | intentionally exposed | CI / bug prevention | unseen generalization |
| Hard / Challenge | 能力边界和脆弱点在哪？ | mixed | diagnosis / stress | production success rate |
| Fresh / Rotating | 新数据上是否仍成立？ | low before run | confirmation / anti-overfit | stable long-term raw trend |

## 关键边界

```text
benchmark score
≠ 产品真实成功率
≠ 全能力覆盖
≠ 因果归因
```

以及：

```text
Hard ≠ Discriminative
Exposed Regression ≠ Clean Holdout
Balanced Macro ≠ Natural-frequency Estimate
Fresh ≠ Unstructured Random
```

## Benchmark Construction Checklist

### 1. Claim

- benchmark 要支持什么结论？
- target population 是什么？
- unit 是 task / episode / user / trajectory？

### 2. Coverage

- target capabilities 是否有 coverage matrix？
- critical / rare slices 是否有最小样本量？
- 有没有大量近重复造成“虚假覆盖”？

### 3. Discrimination

- 是否存在明显 ceiling / floor？
- plausible wrong behavior 是否能被 reference 区分？
- item difficulty 是否只是在“谁都做不出来”？

### 4. Reference

- reference 是否与被测路径独立？
- evaluator 是否足够可靠？
- tolerance / multiple valid outputs 是否定义？

### 5. Split / Leakage

- split unit 是 row 还是 template / source / group？
- exact / semantic / template duplicate 是否跨 split？
- reference / family metadata 是否可能进入 SUT？
- test 是否参与过调参 / failure review / memory construction？

### 6. Sampling / Weighting

- 是 natural、balanced、risk-weighted 还是 hard-case oversampling？
- overall 用 macro 还是 population weights？
- benchmark composition 改动是否 version bump？

### 7. Lifecycle

- Frozen / Regression / Hard / Fresh 各承担什么角色？
- failure 何时 promote 到 regression？
- stale / duplicate fixture 何时 retire / merge？

## Exposure Status

建议统一使用：

```text
KNOWN_CLEAN
CONTROLLED_EXPOSURE
DEVELOPMENT_EXPOSED
PUBLIC_CONTAMINATION_RISK
UNKNOWN
```

并附 exposure ledger，而不是只写 `clean=true/false`。

## Sampling Semantics

### Representative

目标是估计真实总体，应尽量从目标 sampling frame 抽样或使用可信 population weights。

### Diagnostic / Balanced

目标是保证 capability / risk slice 有足够观测，可以人为均衡或 oversample hard cases。

### Risk-weighted

低频但高损失的 failure 可以提高权重，但分数不能再解释为自然频率平均表现。

## Score Views

建议至少区分：

```text
Population-weighted view
Balanced / macro diagnostic view
Critical-slice view
```

不要为了一个“总榜单分数”把不同 estimand 混成一个数字。

## Benchmark Versioning

至少冻结：

```text
item IDs / hashes
split manifest
group keys
reference version
evaluator version
slice metadata
sampling weights
environment / tool snapshot
budget / retry policy
```

任何会改变 score semantics 的变化都应 version bump。

## Promotion Rules

典型生命周期：

```text
Fresh failure
→ explicit review
→ supported failure mechanism
→ minimal reproducible fixture
→ Regression Set
```

如果 hard item 长期稳定并代表基础能力，可以考虑进入 Frozen Core；如果 regression fixtures 重复表达同一机制，应 merge / retire，避免权重膨胀。

## Example Card — VeriAgent Olist Challenge

> 这里只登记 benchmark contract，不登记某次运行分数。

```text
Name:
  Olist Challenge Evaluation

Role:
  diagnostic challenge + frozen dev/test protocol

Target capability:
  structured data reasoning under aggregation, identity, join and time-scope traps

Unit:
  task run / paired repeat

Task families:
  payment_grain
  customer_identity
  join_fanout
  time_scope

Construction:
  24 tasks, pre-split 12 dev / 12 held-out test
  group-aware construction to reduce near-duplicate leakage

Reference:
  frozen reference SQL
  cross-checked with independent Python computation
  plausible-wrong SQL must differ from correct result beyond tolerance

Leakage controls:
  references / wrong SQL / family labels are scoring-only artifacts
  candidate memory built from reviewed dev failures only
  held-out test does not write back into memory during the run

Interpretation:
  supports domain-internal diagnostic comparison on one Olist database
  does not prove cross-database generalization
  does not estimate natural production task frequency
```

## Maintenance Rules

- 不在本文件维护模型分数；分数属于 frozen experiment / run report。
- 每个 benchmark 必须能回答“score 的分母和 sampling distribution 是什么”。
- test 被用于开发后，必须更新 exposure status；不要继续假装 clean holdout。
- benchmark composition 改变后，不得静默沿用旧版本号和旧 release threshold。
- Regression / Hard / Fresh 的分数默认分开报告，不强制合并为一个 overall。
