# Q04 Metric Design：一个 metric 到底应该怎样定义？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 3 / Part 6
- Related Patterns: P04 Slice Before Aggregate, P07 Recovery-aware Evaluation, P09 Cost per Valid Success
- Related Index: `METRICS.md`

## 30-second answer

一个 metric 不是“名字 + 公式”。至少要固定：**它回答什么问题、unit、分子、分母、纳入/排除规则、aggregation、failed/missing handling、方向、不确定性、slice 和解释边界**。

尤其要先问：**分母是什么？失败运行去哪了？** 很多 Eval 误差不是公式算错，而是把 timeout、aborted、invalid output 或提前失败从分母里悄悄删掉。

## 90-second answer

我通常把一个正式 metric 写成 Metric Card：

```text
Question
Definition / Formula
Unit of analysis
Numerator
Denominator
Eligibility / inclusion rule
Aggregation / weighting
Direction
Failed / missing handling
Uncertainty
Slices
What it measures
What it does NOT measure
Decision threshold（另存，不写死在定义里）
```

例如 `Tokens per Valid Success`：

```text
所有有效评测运行消耗的总 token
--------------------------------
正确完成次数
```

失败运行消耗仍留在分子；若 0 次成功，返回 undefined/null，而不是写成 0。它衡量的是单位有效成功成本，不等于“模型更聪明”。

## Full reasoning

### 1. Metric 从问题开始

先问：

> 我想用这个数字回答什么决策问题？

如果问题是“系统是否会错误放行错误答案”，metric 应围绕 false accept；如果问题是“是否可靠完成任务”，只看 syntactic validity 就不够。

### 2. 最小 Metric Contract

#### A. Unit

一个观测是 task、run、user、trajectory 还是 tool call？

#### B. Numerator

什么事件被算作“命中”？

#### C. Denominator

哪些观测有资格进入比例？

#### D. Inclusion / Exclusion

网络失败、API 认证失败、业务失败、数据缺口是否计入？必须提前定义。

#### E. Aggregation

macro average、micro average、weighted average、per-task average 可能回答不同问题。

#### F. Missing / Failed handling

缺失不是自动等于 0，也不是自动删除。要区分：

- 系统失败导致没有结果；
- evaluator 无法评分；
- 数据本身缺失；
- 实验基础设施故障。

#### G. Uncertainty

点估计后面应考虑 CI、paired difference、repeat variability 等。

#### H. Interpretation boundary

明确“这个 metric 不测什么”。

### 3. 三个典型 metric

#### Task Success Rate

```text
正确完成的 eligible runs / 全部 eligible runs
```

关键不是公式，而是：safe stop 算成功还是失败？aborted experiment 是否进入正式分母？partial completion 怎么处理？

#### False Accept Rate

概念上：

```text
错误但被系统接受的结果 / evaluator 可判定的错误结果或相关机会
```

具体 denominator 取决于问题。若定义为“所有 runs 中错误放行比例”，与“所有错误 runs 中被放行比例”是两个不同指标，名称不能混用。

#### Cost per Valid Success

```text
所有运行总成本 / 正确完成数
```

这里失败消耗必须保留，否则一个频繁失败但失败很早的系统会被错误描述为“便宜”。

### 4. Metric definition 与 gate threshold 分离

Metric 是稳定定义：

```text
Task Success Rate = ...
```

Gate 是具体版本的决策条件：

```text
TSR ≥ 95%
False Accept = 0 on frozen safety set
P95 latency ≤ 8s
```

阈值会随业务风险、版本和阶段变化，不应污染 metric 的稳定语义。

### 5. Aggregate 必须能回到 slice

任何总体指标都应该能按关键维度切开，例如：

- task family；
- difficulty；
- tool type；
- failure stage；
- language；
- recovery path；
- memory hit / no-hit。

否则 aggregate 退化时几乎无法诊断。

## Evaluation design

新增 metric 前至少回答：

- 这个 metric 对应哪个 claim？
- denominator 是否会因系统失败而变化？
- missing 是否 informative？
- 是否存在 Simpson's paradox / slice mix 变化？
- 是否容易被 gaming？
- 哪个 paired / uncertainty statistic 与它配套？
- threshold 是否独立于定义？

## Common wrong answers

### 错误 1：失败请求没产出答案，所以不计入 accuracy

如果失败属于被评系统的行为，通常不能直接消失；否则 reliability 被高估。

### 错误 2：平均 latency 足够

长尾 Agent 常需要 P50/P95，并区分完整任务耗时与单次模型调用耗时。

### 错误 3：成本只统计成功 run

这会隐藏失败和 recovery 的真实资源消耗。

## Counterexample / boundary

基础设施级 outage 可能应该把整轮实验标成 `ABORTED`，而不是把它作为系统 failure 混进 capability metric。关键是**预定义分类**并保留证据，而不是事后挑选有利处理。

## VeriAgent example

VeriAgent memory evaluation 明确定义“每次正确完成成本”为**所有运行 token / 正确完成次数**，因此失败消耗不会消失；0 次正确完成返回 `null`。它还同时报告正确完成、错误放行、重复稳定性、P50/P95 latency 和 memory net benefit，避免单一 accuracy 掩盖代价。

这也解释了为什么 v3 中两组都是 36/36 正确，但启用 memory 的 token 仍可以被识别为更高：正确性持平不代表系统等价。

## Follow-up questions

- false accept 的 denominator 应该怎么选？
- macro 与 micro aggregation 什么时候会得出相反结论？
- safe stop 应该放在哪个 metric？
- 为什么“0 个错误放行”不等于 verifier 的拦截率 100%？

## Evidence of mastery

达到 S4 时，应能把一个模糊 KPI（如“Agent 准确率”“成本”“稳定性”）改写成完整 Metric Card，并指出至少两个 denominator trap。

## Related knowledge

- [Metrics Registry](../METRICS.md)
- [Q02 Estimand & Unit](../06_Statistics_and_Experiment_Design/01_Estimand_and_Unit_of_Analysis.md)
- [Q12 Agent Evaluation Contract](../03_Agent_Evaluation/01_Agent_Evaluation_Contract.md)
