# Part 4 — Trajectory & Failure Analysis

## 核心问题

Agent 失败时，如何从 trace 中找到第一处有意义的失败并建立可复现的 root-cause evidence？

## 计划主题

- Trajectory as Evaluation Object
- Step-level Evaluation
- First Failure & Root Cause
- Credit Assignment for Evaluation
- Failure Slicing / Clustering
- Regression Triage

## Canonical Boundary

Trajectory anatomy 与完整 failure taxonomy 的基础定义引用 `LLM_Agent_Data`；本 Part 负责 measurement、diagnosis 与 regression use。

## VeriAgent Lens

把 structured trace、verification event、recovery decision 和最终 outcome 联合起来分析。