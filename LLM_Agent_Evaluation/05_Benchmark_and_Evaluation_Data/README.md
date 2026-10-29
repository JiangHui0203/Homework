# Part 5 — Benchmark & Evaluation Data

## 核心问题

如何构造一个既有区分度、又能支持正确结论的 eval set？

## 计划主题

- Benchmark Design
- Evaluation Set Construction
- Contamination & Leakage
- Coverage / Difficulty / Slices
- Dynamic & Environment Benchmarks
- Golden / Regression Sets

## Canonical Boundary

数据获取、质量、治理等完整体系由 `LLM_Agent_Data` 维护。本 Part 只讨论它们作为 Evaluation Instrument 时的设计。

## VeriAgent Lens

challenge set、dev/test 隔离、independent reference、hard case 与 regression set。