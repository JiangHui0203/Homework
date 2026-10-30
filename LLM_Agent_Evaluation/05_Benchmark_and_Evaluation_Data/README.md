# Part 5 — Benchmark & Evaluation Data

## 核心问题

如何把一批任务构造成一个**有明确 estimand、有区分度、可长期维护、且不会因开发过程失去解释力**的 Evaluation Instrument？

## 已建立

- [01 Discriminative Benchmark Design](01_Discriminative_Benchmark_Design.md) — Q21：claim、coverage matrix、discriminative item、reference independence
- [02 Leakage & Test-set Overfitting](02_Leakage_and_Test_Set_Overfitting.md) — Q22：split leakage、adaptive test overfit、exposure ledger、fresh confirmation
- [03 Frozen / Regression / Hard / Rotating Sets](03_Frozen_Regression_Hard_and_Rotating_Sets.md) — Q23：不同 benchmark asset 的职责、promotion 与 gate role
- [04 Coverage / Difficulty / Distribution Trade-offs](04_Coverage_Difficulty_and_Distribution_Tradeoffs.md) — Q24：coverage、difficulty、slice balance、natural frequency 与 weighting

## 学习顺序

```text
Q21 先设计：什么样的题集能真正测到目标能力？
 ↓
Q22 再隔离：如何保证 confirmation evidence 没被开发污染？
 ↓
Q23 再维护：不同 set 怎样分工，避免一个 test 包办所有任务？
 ↓
Q24 最后聚合：采样分布与总分到底代表什么？
```

## 四个必须形成条件反射的区分

```text
Hard
≠ Discriminative

Challenge distribution
≠ Production distribution

Exposed regression set
≠ Clean holdout

Balanced diagnostic score
≠ Population-weighted estimate
```

## 最小 Benchmark Contract

```text
Claim / target capability
Target population
Unit of evaluation
Task / environment contract
Sampling frame
Coverage matrix
Difficulty / risk policy
Reference / evaluator
Split / group policy
Exposure policy
Slices
Aggregation / weighting
Version / hashes
Known limitations
Recommended use
Not recommended use
```

## Canonical Boundary

数据获取、清洗、生产、治理、lineage 等完整 Data Lifecycle 由 `LLM_Agent_Data` 维护。

本 Part 只讨论数据作为 **Evaluation Instrument** 时的：

```text
benchmark claim
sampling semantics
coverage / discrimination
split / leakage
holdout independence
benchmark portfolio
score interpretation
versioning
```

## 与其它 Parts 的关系

- Part 1：benchmark 必须服从 Evaluation Contract 与 Metric Contract；
- Part 4：reviewed failures 可以 promote 到 regression / hard set；
- Part 6：sampling、paired comparison、uncertainty 决定 score 是否可信；
- Part 7：benchmark manifest、hash、snapshot、replay 属于 eval engineering；
- Part 8：benchmark failure 可进入 data flywheel，但 holdout 不应被无边界写回训练。

## 推荐后续 Lab

- `L06 Benchmark Slice Design`：给 task pool、natural frequency、risk 和 difficulty metadata，设计 representative + diagnostic 两套 view，并完成 split / leakage audit。

## VeriAgent Lens

Olist challenge evaluation 是 Part 5 的直接案例：

```text
24 tasks
12 dev + 12 held-out test
4 task families
group-aware construction
independent SQL + Python reference
plausible-wrong contrast
manifest / hash
no test writeback during evaluation
```

它是 diagnostic challenge set，不是线上自然频率估计；如果后续根据 test failures 继续开发，就应把旧 test 逐步转为 regression / known-hard evidence，并引入 fresh holdout 做新的 confirmation。
