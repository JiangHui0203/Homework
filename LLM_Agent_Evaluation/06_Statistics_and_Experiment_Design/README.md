# Part 6 — Statistics & Experiment Design

## 核心问题

怎样区分真实 improvement、样本波动、重复运行随机性和分析选择造成的假象？

## 已建立

- [01 Estimand & Unit of Analysis](01_Estimand_and_Unit_of_Analysis.md) — Q02：先定义估计目标与独立分析单位
- [02 Is the Improvement Credible?](02_Is_the_Improvement_Credible.md) — Q25：从 effect、paired movement、uncertainty、slice 与 practical significance 判断提升可信度
- [03 Paired Evaluation](03_Paired_Evaluation.md) — Q26：同题配对、pairing key、discordant pairs 与 nested repeats
- [04 Bootstrap / Permutation / Confidence Intervals](04_Bootstrap_Permutation_and_Confidence_Intervals.md) — Q27：CI、bootstrap、permutation 分别回答什么问题，以及 resampling unit 怎么选
- [05 Task Count & Repeats](05_Task_Count_and_Repeats.md) — Q28：task diversity、within-task stochasticity、MDE 与实验预算分配
- [06 Multiple Comparisons & Adaptive Analysis](06_Multiple_Comparisons_and_Adaptive_Analysis.md) — Q29：多指标、多切片、多配置与 repeated peeking 的选择偏差
- [07 Correlation Does Not Replace Human Judgment](07_Correlation_Does_Not_Replace_Human_Judgment.md) — Q30：correlation、agreement、calibration 与 autonomous replacement 的证据门槛

## 学习顺序

```text
Q02 先问：我到底在估计什么？独立 unit 是什么？
 ↓
Q25 再问：观察到的 improvement 值不值得相信？
 ↓
Q26 用 paired design 提高同题版本比较的可解释性
 ↓
Q27 给 effect 加 uncertainty，并理解 null test
 ↓
Q28 决定有限预算应该花在更多 tasks 还是更多 repeats
 ↓
Q29 控制“看了太多结果后挑赢家”的选择偏差
 ↓
Q30 把 evaluator correlation 与真实 replacement claim 分开
```

## Q25–Q28 必须形成的统计反射

看到任何 Eval 提升，先恢复：

```text
Estimand
Unit of analysis
N distinct tasks
Nested repeats
Pairing key
Effect size
Wins / losses
Confidence interval
Critical slices
Exposure / holdout status
```

再谈：

```text
significance
power
sample size
release decision
```

不要倒过来先问“应该用哪个检验”。

## 四个关键边界

```text
More runs
≠ more independent tasks

p < 0.05
≠ practically important

CI crosses 0
≠ systems are proven equivalent

High correlation
≠ evaluator can replace human
```

## 一个最小版本比较报告

```text
Primary estimand:
Primary unit:
Benchmark / exposure status:
N tasks:
Repeats:
Baseline:
Candidate:
Paired delta:
Wins / losses:
95% CI:
Critical slices:
Cost / latency delta:
Multiplicity status:
Decision:
```

## 基础依赖

- [Probability & Statistics for Eval](../00_Foundations/01_Probability_and_Statistics_for_Eval.md)
- [Experiment Design Basics](../00_Foundations/04_Experiment_Design_Basics.md)
- [Q02 Estimand & Unit](01_Estimand_and_Unit_of_Analysis.md)
- Part 5 Benchmark sampling / holdout design

## 与其它 Parts 的关系

- Part 1 定义 metric / decision contract；
- Part 2 提供 Judge / human reliability 问题，Q30 在统计层解释 correlation 边界；
- Part 4 提供 paired losses / slices / failure diagnosis；
- Part 5 决定 sample 来自什么 population、是否 clean holdout；
- Part 7 负责把 pairing、seed、snapshot、artifact 与 analysis pipeline 做成可复现 harness。

## 推荐后续 Lab

- `L03 Paired Evaluation`：给定 paired task × repeat 数据，完成 effect、paired win/loss、task-level bootstrap CI、permutation test、sample-size / repeat audit 和 multiple-comparison review。

Q25–Q30 学完后再做 L03，能把“这个提升到底可信不可信”真正压到 S3。

## VeriAgent Lens

VeriAgent 是很适合这部分的反例教材：12 个不同 task × 3 repeats 不能冒充 36 个独立 task；`29/36 → 30/36` 要结合 `3 win / 2 loss`、task-level stochasticity 和作用阶段分析；即使统计上观察到正差异，也不能绕过“memory 在失败发生之后才有机会作用”的因果边界。

## 原则

统计方法必须服务于明确的 estimand 与 unit of analysis；不能先选检验方法，再反推问题。
