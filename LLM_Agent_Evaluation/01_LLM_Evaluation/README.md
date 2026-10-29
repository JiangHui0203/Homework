# Part 1 — LLM Evaluation

## 核心问题

如何把“模型看起来不错”转化成明确、可执行、可比较的 evaluation contract？

## 已建立

- [01 Evaluation Contract](01_Evaluation_Contract.md) — Q01
- [02 What Are We Measuring](02_What_Are_We_Measuring.md) — Q03
- [03 Metric Design](03_Metric_Design.md) — Q04

## Practice

- [L01 Metric Design Lab](../labs/L01_metric_design/README.md) — 用冻结 Agent run 数据亲手定义 denominator、failure handling、cost 与 release reporting contract。

## 后续主题

- Reference-based vs Reference-free Eval
- Open-ended Generation Evaluation
- Human Evaluation
- Slicing / Regression / Error Analysis

## 依赖

Part 0 的统计、LLM 基础与实验设计；Q02 由 Part 6 维护。

## 不负责

Judge 的系统性可靠性问题归 Part 2；Agent 交互过程归 Part 3/4。

## VeriAgent Lens

用 Olist challenge task 讨论“正确完成”“错误放行”“安全停止”“成本”如何同时定义。
