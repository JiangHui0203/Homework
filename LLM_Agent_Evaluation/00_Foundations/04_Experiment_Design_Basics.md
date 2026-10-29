# Experiment Design Basics for Eval — 最小必需基础

> 目标：能把“我想看看新方法有没有用”改写成可验证实验。

## 1. 从 Question 到 Evidence

最小链条：

```text
Question
→ Claim / Hypothesis
→ Estimand
→ Unit of analysis
→ Conditions
→ Dataset / Split
→ Evaluator
→ Metrics
→ Protocol
→ Analysis
→ Decision
```

任何一环模糊，最后都容易出现“数字有了，但不知道说明什么”。

## 2. Baseline 与 Candidate

比较两个系统时尽量做到：

```text
除目标改动外，其余条件相同
```

包括模型版本、prompt 基础结构、task set、tool、budget、evaluator、运行环境。否则 improvement 无法清晰归因。

## 3. Dev / Validation / Test 的核心思想

名字不重要，职责重要：

- **Development data**：允许看错误、调方法。
- **Held-out evaluation data**：用于验证冻结方案。

一旦根据 test failure 修改系统，再继续把同一 test 当独立证据，它已经开始承担 dev 的角色。

## 4. Paired Evaluation

当 A/B 可以在同一 task 上运行时，优先保存配对关系：

```text
(task_id, repeat_id, baseline_result, candidate_result)
```

这样可以直接分析：

- wrong → right；
- right → wrong；
- both right；
- both wrong。

比只看两个独立平均值更容易解释。

## 5. Repeats 与 Randomness

重复运行解决的是**同一条件下的随机性**，不是自动扩展 task coverage。

要同时考虑：

- 不同 task 的覆盖；
- 同一 task 的重复稳定性。

## 6. Freeze Before Confirmation

确认性评测前尽量冻结：

- candidate implementation；
- model/config；
- dataset snapshot；
- evaluator；
- primary metric；
- failure handling；
- protocol。

冻结不是为了形式主义，而是防止看到结果后调整规则。

## 7. Negative Result 也是结果

如果机制被触发但 outcome 无改善，或者准确率持平但成本增加，应保留这个结果。真实 Eval 的目标不是“证明新模块有效”，而是判断它是否有效。

## 8. 最小实验卡

```text
Objective:
Hypothesis:
Population / Scope:
Primary estimand:
Unit:
Baseline:
Candidate:
Only intended difference:
Dataset split:
Evaluator:
Primary metric:
Secondary metrics:
Repeats / pairing:
Artifacts:
Decision rule:
What this experiment cannot prove:
```

## Related

- [Q01 Evaluation Contract](../01_LLM_Evaluation/01_Evaluation_Contract.md)
- [Q03 What Are We Measuring](../01_LLM_Evaluation/02_What_Are_We_Measuring.md)
- [Q02 Estimand & Unit](../06_Statistics_and_Experiment_Design/01_Estimand_and_Unit_of_Analysis.md)
