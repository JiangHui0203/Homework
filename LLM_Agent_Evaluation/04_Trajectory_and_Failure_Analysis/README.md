# Part 4 — Trajectory & Failure Analysis

## 核心问题

Agent 失败时，如何从 trace 中定位第一处有意义的失败、正确分配 credit，并把单次 failure 变成可复现的 regression evidence？

## 已建立

- [01 First Meaningful Failure & Root Cause](01_First_Meaningful_Failure_and_Root_Cause.md) — Q17：symptom、first error / harmful action、first meaningful failure、mechanism 与 root cause
- [02 Step / Outcome & Credit Assignment](02_Step_Outcome_and_Credit_Assignment.md) — Q18：step correctness 与 final outcome 联合分析，避免把 final score 错归因给中间机制
- [03 Slice-based Regression Diagnosis](03_Slice_Based_Regression_Diagnosis.md) — Q19：paired loss、capability slice、failure slice 与 regression triage
- [04 Failure Taxonomy as Engineering Asset](04_Failure_Taxonomy_as_Engineering_Asset.md) — Q20：从标签表到 detection、metric、fixture、regression 与 intervention routing

## 这四篇的学习顺序

```text
Q17 先定位：失败最早从哪里变得有意义？
 ↓
Q18 再归因：哪些 step 应获得 credit / blame？
 ↓
Q19 再聚合：退化集中在哪些 slice？
 ↓
Q20 最后工程化：如何把 failure 变成长期 regression asset？
```

## 核心区分

```text
Outcome
≠ Symptom
≠ First Error
≠ First Harmful Action
≠ First Meaningful Failure
≠ Immediate Mechanism
≠ Root Cause
```

以及：

```text
Correlation / slice association
≠ causal attribution

Mechanism activated
≠ behavior changed
≠ outcome improved
```

## Canonical Boundary

完整 failure taxonomy 概念定义由：

`LLM_Agent_Data/14_Agent_Failure_Taxonomy.md`

维护。

Part 4 不复制 Data taxonomy，而负责 Evaluation 侧的：

```text
measurement
trace localization
credit assignment
slice diagnosis
failure aggregation
regression promotion
```

## 与 Part 3 的边界

Part 3 定义 Agent 运行中应观测什么：

```text
tool
recovery
state / memory
checkpoint
budget
```

Part 4 使用这些 trace evidence 做：

```text
first-failure localization
causal-strength labeling
regression triage
failure taxonomy engineering
```

## 最小 diagnosis pipeline

```text
Frozen task + environment + trace
↓
Outcome / symptom
↓
Event timeline
↓
First meaningful failure
↓
Immediate mechanism
↓
Root-cause hypothesis + evidence level
↓
Paired / counterfactual check
↓
Slice aggregation
↓
Regression fixture
```

## Labs

- [L04 Trajectory Failure Analysis](../labs/L04_trajectory_failure_analysis/README.md)：16 条 paired synthetic trajectories，完成 first meaningful failure、root-cause evidence、paired loss、slice diagnosis 与 regression promotion。
- [L05 Agent Recovery Evaluation](../labs/L05_agent_recovery_evaluation/README.md)：24 条 recovery episodes，完成 retry / safe stop / false recovery / budget / cost 的条件评测。

L04 是 Part 4 的主实践；L05 把 Part 4 的 failure localization 接回 Part 3 的 recovery control。

## VeriAgent Lens

VeriAgent 是这一 Part 很合适的真实案例：

- Olist challenge 保存 task、trace、SQL、verification、最终 outcome；
- `CJ03_r01` 能区分 execution symptom 与 alias-scope first meaningful failure；
- candidate memory 测试用 failure stage 证明 `+1/36` 不能直接归因于 memory；
- 预定义 task families 支持 slice regression，但 family association 不能替代具体 root-cause diagnosis；
- 开发失败经显式 review 后才进入候选经验，体现了 failure evidence 与 intervention routing 的边界。
