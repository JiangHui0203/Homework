# Part 2 — Grader / LLM-as-a-Judge

## 核心问题

评分器本身可靠吗？它的偏差、方差和失败模式会怎样影响最终结论？

## 已建立

- [01 Grader / Verifier / LLM-as-a-Judge](01_Grader_Verifier_and_Judge.md) — Q07：Evaluator 边界与 deterministic-first 原则
- [02 Judge Reliability & Calibration](02_Judge_Reliability_and_Calibration.md) — Q08：如何验证 Judge 本身是否足够可靠
- [03 Judge Bias & Failure Modes](03_Judge_Bias_and_Failure_Modes.md) — Q09：position / verbosity / self-preference / style bias
- [04 Rubric & Scoring Protocol](04_Rubric_and_Scoring_Protocol.md) — Q10：rubric、pointwise / pairwise、hard gate 与 adjudication
- [05 Human Disagreement & Adjudication](05_Human_Disagreement_and_Adjudication.md) — Q11：agreement、disagreement、human reference 与争议处理

## 这五篇的学习顺序

```text
Q07 先知道谁在评
 ↓
Q08 再验证 Judge 靠不靠谱
 ↓
Q09 找系统性 bias
 ↓
Q10 设计可执行 protocol
 ↓
Q11 处理 Judge 与 Human 不一致
```

## Practice

- [L02 — LLM Judge Calibration Lab](../labs/L02_llm_judge_calibration/README.md)

这个 Lab 使用冻结的 Human + Judge 数据，要求亲手完成：

```text
agreement
→ repeat consistency
→ swap test
→ bias slicing
→ human disagreement adjudication
→ release gates
→ scope-aware GO / NO-GO
```

完成 Lab 可以作为 Q08–Q11 从“理解”向“能独立设计与分析”推进的实践证据。

## 后续主题

- Pairwise ranking aggregation / Bradley-Terry / Elo
- Judge ensembles and routing
- Confidence / abstention calibration
- Judge regression suite

## Canonical Boundary

`LLM_Agent_Data/15_Grader_Verifier_and_LLM_as_a_Judge.md` 维护 Evidence → Evaluator → Label 的数据系统 canonical semantics；本 Part 不重写该章。

本 Part 的 owner 是：

```text
Judge reliability
Judge bias diagnosis
Rubric / scoring protocol
Human agreement / disagreement analysis
Operational calibration and adjudication
```

## VeriAgent Lens

VeriAgent 当前大量使用 deterministic proof / SQL / contract verification，因此主要作为 Judge 的边界案例：能直接验证的 correctness 不应降级成 LLM judgment。未来如增加解释质量、帮助性等开放式评价，再引入经过校准的 Judge layer。
