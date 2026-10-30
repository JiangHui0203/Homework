# Part 1 — LLM Evaluation

## 核心问题

如何把“模型看起来不错”转化成明确、可执行、可比较的 evaluation contract？

## 已建立

- [01 Evaluation Contract](01_Evaluation_Contract.md) — Q01
- [02 What Are We Measuring](02_What_Are_We_Measuring.md) — Q03
- [03 Metric Design](03_Metric_Design.md) — Q04
- [04 Reference-based vs Reference-free Evaluation](04_Reference_Based_and_Reference_Free_Evaluation.md) — Q05
- [05 Open-ended Generation Evaluation](05_Open_Ended_Generation_Evaluation.md) — Q06

Q02 `Estimand / Unit of Analysis` 由 Part 6 维护，但属于这一组基础 measurement 问题。

## V1 学习链

```text
Q01 先定义 evaluation contract
 ↓
Q02 明确 estimand / unit
 ↓
Q03 区分 observed score 与 capability claim
 ↓
Q04 定义 metric contract
 ↓
Q05 选择 strongest available evidence / reference strategy
 ↓
Q06 为 open-ended output 拆 quality dimensions 与 evaluator portfolio
```

## Practice

- [L01 Metric Design Lab](../labs/L01_metric_design/README.md) — 用冻结 Agent run 数据亲手定义 denominator、failure handling、cost 与 release reporting contract。
- [L02 Judge Calibration](../labs/L02_llm_judge_calibration/README.md) — 当 Q05/Q06 需要 Judge / human-like evaluator 时，验证 agreement、repeat、swap 与 bias。

## 后续按需主题

- Human Evaluation protocol 的更细扩展；
- domain-specific generation metrics；
- production preference / user outcome measurement。

这些不作为 V1 主干 blocker；出现真实项目需求时再 reverse-fill。

## 依赖

Part 0 的统计、LLM 基础与实验设计；Q02 由 Part 6 维护。

## 不负责

Judge 的系统性可靠性问题归 Part 2；Agent 交互过程归 Part 3/4；Benchmark construction 与 sampling 归 Part 5。

## VeriAgent Lens

用 Olist challenge task 讨论“正确完成”“错误放行”“安全停止”“成本”如何同时定义，并进一步区分：

```text
numeric / SQL correctness
→ reference / executable evidence

open explanation quality
→ grounding + checklist + calibrated Judge / human
```

即：能 deterministic verify 的部分不要因为最终输出是自然语言就退化成主观评分。
