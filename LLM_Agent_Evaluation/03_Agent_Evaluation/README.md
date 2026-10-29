# Part 3 — Agent Evaluation

## 核心问题

Agent 不只是一次文本生成；如何评价 task、tool、state、environment、recovery 和长期行为？

## 已建立

- [01 Agent Evaluation Contract](01_Agent_Evaluation_Contract.md) — Q12：为什么 final task success 不足以评价 Agent
- [02 Tool Use & Grounding Evaluation](02_Tool_Use_and_Grounding_Evaluation.md) — Q13：tool opportunity、selection、arguments、execution、observation / final grounding
- [03 Recovery & Graceful Degradation](03_Recovery_and_Graceful_Degradation.md) — Q14：first-pass、recovered、safe stop、unrecovered 与 recovery cost
- [04 State / Memory & Leakage Evaluation](04_State_Memory_and_Leakage_Evaluation.md) — Q15：snapshot、state isolation、test contamination 与 memory causal attribution
- [05 Long-Horizon Agent Evaluation](05_Long_Horizon_Agent_Evaluation.md) — Q16：checkpoint、stage denominator、loop/stall 与 fixed-budget evaluation

## 这五篇的学习顺序

```text
Q12 先建立 Agent Eval 的分层对象
 ↓
Q13 检查每次 tool/action 是否真正正确
 ↓
Q14 检查失败后如何恢复、降级或停止
 ↓
Q15 保证跨任务 / 跨条件 state 不污染实验
 ↓
Q16 扩展到长链任务的 checkpoint 与 budget
```

## 核心区分

```text
Final success
≠ Tool correctness
≠ Recovery quality
≠ State isolation
≠ Long-horizon reliability
```

Part 3 的目标不是制造尽可能多的过程 KPI，而是让每个过程指标都服务于至少一个目的：

```text
diagnosis
causal attribution
reliability gate
cost / deployment decision
replay / regression
```

## 与 Part 4 的边界

Part 3 负责定义 Agent 运行中**应该观测和测量什么**：tool、state、recovery、checkpoint、budget。

Part 4 `Trajectory & Failure Analysis` 进一步负责：

```text
symptom vs first meaningful failure vs root cause
step correctness vs final outcome
credit assignment
failure slicing / taxonomy
```

因此 Q16 会记录 first-failure event，但不会在这里展开完整 root-cause methodology。

## 依赖

- Part 1：Evaluation Contract / Metric Design；
- [Agent Fundamentals for Eval](../00_Foundations/06_Agent_Fundamentals_for_Eval.md)；
- Part 2：开放语义过程判断需要经过校准的 Judge；
- Part 6：paired / repeated / uncertainty；
- Part 7：trace、replay、fixture、snapshot。

## Labs

- [L04 Trajectory Failure Analysis](../labs/L04_trajectory_failure_analysis/README.md)：从 paired structured trace 找 first meaningful failure、evidence strength 与 regression candidates。
- [L05 Agent Recovery Evaluation](../labs/L05_agent_recovery_evaluation/README.md)：计算 recovery opportunity / attempt / success、safe-stop appropriateness、retry policy violation 与 recovery cost。
- `L07 Eval Harness`：后续实现可重放的 task-state-action-observation artifact 链。

推荐先做 L04，再做 L05：先学会定位 failure，再判断 failure 之后应该采取什么控制动作。

## VeriAgent Lens

ProofWriter 与 Olist Data Agent 提供两类可验证环境。当前最成熟的实例是 Olist：

- SQL / numeric correctness 可以 deterministic verify；
- trace 能区分 analysis、memory retrieval、SQL execution 与 final outcome；
- memory snapshot 与 test writeback policy 可用于 Q15；
- challenge evaluation 中“错误答案被接受”和“SQL 被执行器拒绝”可用于 Q13；
- 数据缺失时的正确停止与失败成本可用于 Q14；
- 它目前不是典型 long-horizon benchmark，因此 Q16 只把它当 observability 的边界案例，不夸大成长期自治能力证据。
