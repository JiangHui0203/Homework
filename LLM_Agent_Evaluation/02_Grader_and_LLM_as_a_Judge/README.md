# Part 2 — Grader / LLM-as-a-Judge

## 核心问题

评分器本身可靠吗？它的偏差、方差和失败模式会怎样影响最终结论？

## 计划主题

- Grader / Verifier / Judge 边界
- Rubric & Scoring Design
- Judge Bias and Failure Modes
- Calibration & Human Agreement
- Pairwise / Ranking / Preference
- Adjudication / Judge Ensembles

## Canonical Boundary

`LLM_Agent_Data` 已有 Grader/Verifier/Judge 的数据系统视角；本 Part 重点维护 evaluator reliability 与 operational evaluation methodology。

## VeriAgent Lens

优先讨论 deterministic proof / SQL / contract verification 与模型 judgment 的边界。