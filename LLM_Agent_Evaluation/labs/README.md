# Labs

Lab 用来把“看懂”推进到“会做”。每个 M1 最终应至少关联一个 Lab 或真实项目证据。

## 第一批 Labs

- [**L01 Metric Design**](L01_metric_design/README.md)：用冻结 Agent run 数据定义 outcome / reliability / recovery / cost / latency metrics，审计 denominator、failed/missing handling 与 protocol completeness。
- [**L02 Judge Calibration**](L02_llm_judge_calibration/README.md)：用冻结 Human + Judge 数据完成 agreement、repeat、swap、bias slicing、adjudication 和上线判定。
- `L03 Paired Evaluation`：设计 paired experiment + uncertainty。
- [**L04 Trajectory Failure Analysis**](L04_trajectory_failure_analysis/README.md)：用 paired structured traces 做 first meaningful failure、evidence strength、slice regression 与 regression promotion。
- [**L05 Agent Recovery Evaluation**](L05_agent_recovery_evaluation/README.md)：用冻结 recovery episodes 计算 opportunity / attempt / success、safe stop、retry policy、false recovery 与 recovery cost。
- [**L06 Benchmark Slice Design**](L06_benchmark_slice_design/README.md)：从带 capability / difficulty / risk / natural-frequency / group / exposure 元数据的 task pool 构造 representative + diagnostic 两套 benchmark view，并做 split / leakage / weighting audit。
- `L07 Eval Harness`：实现最小 task-result-artifact-replay 链路。
- `L08 VeriAgent Frozen Case`：把一次真实实验整理成 frozen experiment。

Lab 使用 [`../templates/LAB.md`](../templates/LAB.md)。

## 推荐学习路径

```text
Q01–Q04 -> L01 Metric Design
Q07–Q11 -> L02 Judge Calibration
Q12–Q20 -> L04 Trajectory Failure Analysis + L05 Agent Recovery Evaluation
Q21–Q24 -> L06 Benchmark Slice Design
```

L04 与 L05 有意分工：

```text
L04: failure 发生在哪里？证据支持到哪一层？如何聚合成 regression？
L05: failure 发生以后，系统应该 retry、recover、safe stop 还是 handoff？
```

L06 则训练：

```text
benchmark claim
→ pool eligibility
→ representative sampling
→ diagnostic coverage
→ split / leakage audit
→ weighting / interpretation
```

## 完成度原则

- 阅读知识正文只能说明“见过/理解”；
- 跑完 Lab、独立写出分析与结论，才是向 `S3` 推进的证据；
- Lab 的参考答案不能替代自己的报告；
- synthetic Lab 只验证方法掌握，不构成任何真实模型/系统的性能证据。
