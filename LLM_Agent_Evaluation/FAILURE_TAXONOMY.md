# Failure Taxonomy — Evaluation View

> 完整 Agent Failure Taxonomy 的概念定义由 `LLM_Agent_Data` 维护。本文件不复制 taxonomy，而建立“失败 → 可观测证据 → evaluator → metric → slice → regression test”的 Evaluation 索引。

Canonical reference：[`../LLM_Agent_Data/14_Agent_Failure_Taxonomy.md`](../LLM_Agent_Data/14_Agent_Failure_Taxonomy.md)。

## Evaluation Failure Record

每条正式 failure record 至少回答：

```text
Failure ID
Taxonomy version
Outcome
Observable symptom
First error (optional)
First harmful action (optional)
First meaningful failure
Immediate mechanism
Root cause / root-cause hypothesis
Evidence level
Evidence references
Primary failure layer
Secondary / propagated failures
Failure owner
Severity
Detectability
Recoverability
Detection method
Opportunity / denominator
Metric impact
Useful slices
Confounders
Debugging order
Regression fixture
Intervention route
```

## Evidence Level

建议统一使用：

```text
OBSERVED
trace / verifier / environment 直接可见

SUPPORTED
replay、counterfactual、paired 或重复证据支持

HYPOTHESIS
合理解释，但尚未获得足够因果证据
```

允许：

```text
UNRESOLVED
MULTI_CAUSE
INSUFFICIENT_EVIDENCE
```

不要为了填表强行制造唯一 root cause。

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

```text
Outcome
≠ Symptom
≠ First Error
≠ First Harmful Action
≠ First Meaningful Failure
≠ Immediate Mechanism
≠ Root Cause
```

同时：

- 最后一个错误步骤不一定是 first meaningful failure。
- 低 confidence / high entropy / repeated call 可以是 detection signal，不自动是 failure label。
- failure 分类必须由 evidence 支持；不能仅凭最终答案猜原因。
- primary failure 与 propagated symptom 分开，避免重复计数。
- taxonomy 最终要能落到 metric、slice 与 regression fixture，否则只是标签表。

## 从 Taxonomy 到工程资产

成熟度建议：

```text
Stage 0  free-form note
Stage 1  named label
Stage 2  operational definition + evidence + denominator
Stage 3  replayable regression fixture + expected behavior
```

只有 Stage 2/3 才适合长期统计。

## Failure Card

稳定 failure type 建议维护：

```text
Failure ID / Name
Canonical definition
Layer / Owner
Severity
Recoverability
Observable symptom
First meaningful failure pattern
Required evidence
Detection method
Opportunity / denominator
Known confounders
Metrics affected
Recommended slices
Representative cases
Regression fixture
Expected fix / intervention route
Version introduced
Status: provisional / stable / deprecated
```

## Promotion Rule

新发现 failure 默认先进入 `provisional`：

```text
incident
→ trace review
→ evidence / replay
→ operational definition
→ representative cases
→ stable taxonomy
→ regression fixture
```

不要因为一次实验出现新错误，就立刻永久增加 taxonomy 和 frozen benchmark。

## Primary vs Propagated

例：

```text
wrong time scope
→ wrong SQL predicate
→ wrong numeric result
→ false accept
```

可以记录：

```text
primary failure:
task_scope_error

propagated:
sql_predicate_error
wrong_numeric_result
false_accept
```

root-cause burden 与 surface symptom burden 可以分别统计。

## Failure → Intervention Routing

| Failure owner | 常见下一步 |
|---|---|
| Model / policy | prompt/controller、data、post-training、routing |
| Tool | schema/API/validation 修复 |
| Harness | evaluator、trace、replay、timeout 逻辑修复 |
| Environment | snapshot / fixture / permissions / availability |
| Task / benchmark | contract、reference、ambiguity 修复 |
| Evaluator | verifier/judge calibration、rubric 修复 |
| Memory / state | snapshot isolation、provenance、expiry、write policy |

先确认 owner，再决定是否进入 data flywheel。

## Regression Asset Rule

适合进入 frozen core 的 failure：

```text
high severity
real historical regression
stable reproducibility
important product contract
```

新颖、长尾、易过拟合模式更适合 rotating hard set。

## Related metrics

- First-Failure Distribution
- Failure Recurrence Rate
- Failure Escape / False Accept Rate
- Failure Detection Rate
- Recovery Success Rate
- Post-failure Waste
- Slice Regression Delta

## VeriAgent examples

Olist challenge 中已有可审计实例：

- child-row eligibility 被错误应用到 parent-table grain；
- SQL alias scope violation；
- wrong numeric result 被 runtime 接受；
- SQL execution rejection。

这些具体 failure 可以通过 SQL / trace / verifier evidence 支持；“模型不擅长多表推理”则更像高层 hypothesis，不能直接当作 operational root cause label。

## Related

- [Q17 First Meaningful Failure](04_Trajectory_and_Failure_Analysis/01_First_Meaningful_Failure_and_Root_Cause.md)
- [Q20 Failure Taxonomy as Engineering Asset](04_Trajectory_and_Failure_Analysis/04_Failure_Taxonomy_as_Engineering_Asset.md)
