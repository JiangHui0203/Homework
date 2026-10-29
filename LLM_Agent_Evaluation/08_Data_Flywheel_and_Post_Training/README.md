# Part 8 — Eval → Data Flywheel / Post-training

## 核心问题

如何把可靠的 Evaluation 证据转化为数据与训练动作，并在更新后重新证明系统真的变好？

## 计划主题

- From Evaluation to Data
- Hard Example Mining
- Feedback / Reward / Preference Signals
- Post-training Change Validation
- Online Feedback / Drift
- Closing the Evaluation Loop

## 强边界

本 Part 不重新编写 data flywheel、data quality、governance 或 post-training data 教材；这些主题的 canonical owner 是 `LLM_Agent_Data`。

这里只维护：

```text
Eval failure → evidence → candidate intervention → update → frozen re-evaluation
```

## VeriAgent Lens

reviewed failure → candidate experience/memory → frozen paired evaluation，是当前最直接的案例。