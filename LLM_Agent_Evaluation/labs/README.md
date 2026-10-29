# Labs

Lab 用来把“看懂”推进到“会做”。每个 M1 最终应至少关联一个 Lab 或真实项目证据。

## 第一批 Labs

- `L01 Metric Design`：给一个 Agent 任务定义 outcome / reliability / cost metrics。
- [**L02 Judge Calibration**](L02_llm_judge_calibration/README.md)：用冻结 Human + Judge 数据完成 agreement、repeat、swap、bias slicing、adjudication 和上线判定。
- `L03 Paired Evaluation`：设计 paired experiment + uncertainty。
- `L04 Trajectory Failure Analysis`：从 trace 找 first meaningful failure。
- `L05 Agent Recovery Evaluation`：区分 recovered / safe stop / unrecovered failure。
- `L06 Benchmark Slice Design`：从 task set 构造 capability / difficulty slices。
- `L07 Eval Harness`：实现最小 task-result-artifact-replay 链路。
- `L08 VeriAgent Frozen Case`：把一次真实实验整理成 frozen experiment。

Lab 使用 [`../templates/LAB.md`](../templates/LAB.md)。

## 完成度原则

- 阅读知识正文只能说明“见过/理解”；
- 跑完 Lab、独立写出分析与结论，才是向 `S3` 推进的证据；
- Lab 的参考答案不能替代自己的报告；
- synthetic Lab 只验证方法掌握，不构成任何真实模型/系统的性能证据。
