# Failure Taxonomy — Evaluation View

> 完整 Agent Failure Taxonomy 的概念定义由 `LLM_Agent_Data` 维护。本文件不再复制 taxonomy，而是建立“失败 → 可观测证据 → evaluator → metric → slice → regression test”的 Evaluation 索引。

Canonical reference：[`../LLM_Agent_Data/14_Agent_Failure_Taxonomy.md`](../LLM_Agent_Data/14_Agent_Failure_Taxonomy.md)。

## Evaluation Failure Record

每类失败最终应能回答：

```text
Failure ID
Definition / canonical owner
Observable symptom
First meaningful failure
Evidence required
Detection method
Metric impact
Useful slices
Confounders
Debugging order
Regression test
Data / product action
VeriAgent example
```

## V0 诊断维度

- **Task understanding**：任务理解、约束遗漏、目标错位。
- **Planning / decomposition**：错误计划、缺步骤、不可执行分解。
- **Retrieval / context**：错误证据、缺证据、污染上下文。
- **Tool selection / arguments**：工具选错、参数错、作用域错。
- **Execution / environment**：工具失败、环境漂移、权限或资源问题。
- **Reasoning / transformation**：中间推理或数据变换错误。
- **Verification**：错误放行、误拒绝、coverage 不足。
- **State / memory**：旧状态污染、错误记忆、跨样本泄漏。
- **Recovery / control**：该重试时停止、该停止时继续、恢复失败。
- **Answer synthesis**：证据正确但最终表达或聚合错误。
- **Evaluation failure**：grader/judge/metric 本身错误，把系统问题与评测问题混淆。

## 核心规则

- `symptom != root cause`。
- 最后一个错误步骤不一定是 first meaningful failure。
- 失败分类必须可由证据支持；不能仅凭最终答案猜原因。
- taxonomy 最终要能落到 slice 与 regression test，否则只是标签表。