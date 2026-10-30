# Q27 Bootstrap、Permutation Test、Confidence Interval 分别在 Eval 中回答什么问题？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 5 / Part 6
- Related Patterns: P03 Paired Same-Task Comparison; P04 Slice Before Aggregate
- Related Metrics: Confidence Interval, Paired Net Win/Loss, Slice Regression Delta

## 30-second answer

三者解决的问题不同：

- **Confidence Interval**：表达 effect estimate 的不确定范围；
- **Bootstrap**：通过对正确的分析单位重采样，近似统计量的 sampling distribution，常用于构造 CI；
- **Permutation Test**：在零假设下利用“标签可交换”构造 null distribution，回答观察到的差异在零效应下有多极端。

最重要的不是背方法名，而是**resample / permute 哪个 unit**。如果 12 个 task 每题 3 repeats，而 claim 是 task-level generalization，应以 task 为主要 resampling unit；不能把 36 runs 当成 36 个独立 task。

## 90-second answer

我会先写：

```text
estimand
unit of analysis
pairing structure
```

然后选工具。

如果想回答“candidate 相对 baseline 的平均 task-level effect 有多不确定”，可以对 task-level paired differences 做 bootstrap CI。

如果想检验零假设：

```text
H0: 两个条件在 paired unit 上没有系统差异
```

可以在可交换性成立时做 paired permutation，例如对每个 task 随机交换 A/B 标签，或等价地随机翻转 paired difference 的符号，再看观察到的 statistic 有多极端。

CI 与 p-value 不同：CI 更直接表达 effect size 的 plausible range；permutation p-value 更直接回答“在零假设下，这么极端的差异有多罕见”。正式 Eval 更推荐把 effect size + CI 放在主位，test 作为补充。

## 1. Confidence Interval 是报告层，不是一种唯一算法

CI 的目标是表达：

> 基于有限 sample，我们对目标 estimand 有多大 sampling uncertainty？

例如：

```text
paired delta = +3.0pp
95% CI = [-1.5pp, +7.2pp]
```

这说明当前数据仍与轻微退化、无变化和较大提升都相容。

不要写成：

> “真值有 95% 概率落在这一次计算出的区间里。”

在经典频率学派解释中，95% 指的是重复抽样下构造程序的覆盖率。

实践上你只需形成一个反射：

> **point estimate 没有 uncertainty，证据是不完整的。**

## 2. Bootstrap 是“用样本近似重复抽样”

最基本 bootstrap：

```text
原始独立 units
→ 有放回重采样相同数量 units
→ 每次重算 statistic
→ 得到 bootstrap distribution
```

例如有 100 个 task-level paired differences：

```text
D_1, D_2, ..., D_100
```

每次有放回抽 100 个 `D_i`，计算 mean delta，重复很多次，就能近似 estimate 的 sampling distribution。

## 3. Bootstrap 最关键的问题：抽谁？

### 错误

```text
12 tasks × 3 repeats = 36 rows
→ 直接 bootstrap 36 rows
```

如果 repeats 共享 task，这会破坏层级结构，并夸大独立信息量。

### 更合理

如果 primary unit 是 task：

```text
resample tasks
```

每次被抽中的 task 连同它的全部 repeats / paired conditions 一起进入样本。

这通常叫：

```text
cluster bootstrap / task-level bootstrap
```

如果你的 estimand 是 user-level，就应该 resample users；如果是 session-level，就应该 resample sessions。

## 4. Paired Bootstrap

对于 paired A/B：

错误做法：

```text
独立 bootstrap A
独立 bootstrap B
```

这会破坏 pairing。

更合理：

```text
(task_i, A_i, B_i)
```

作为一个整体重采样，或直接 resample：

```text
D_i = B_i - A_i
```

这样保留相同 task 上的共享难度。

## 5. Permutation Test 的核心是 Null Exchangeability

Permutation test 不只是“把数据打乱”。

它依赖一个问题：

> 在零假设成立时，哪些标签交换不会改变数据的联合分布？

### Paired A/B 例子

对每个 task：

```text
(A_i, B_i)
```

在 H0 下，如果两条件标签可交换，可以随机决定：

```text
保留 A/B
或交换 A/B
```

等价地，对：

```text
D_i = B_i - A_i
```

随机翻转符号。

每次重新计算 mean / net win 等 statistic，就得到零假设下的 null distribution。

## 6. Permutation p-value 回答什么

它回答的不是：

> candidate 为真的概率是多少？

而是：

> 如果 H0 和交换性假设成立，观察到当前或更极端 statistic 的概率有多大？

因此：

```text
small p-value
≠ large practical effect
≠ mechanism causality
≠ deployment value
```

## 7. Bootstrap 与 Permutation 的区别

| 方法 | 主要问题 | 主要输出 |
|---|---|---|
| Bootstrap | estimate 有多不稳定？ | sampling distribution / CI |
| Permutation | 零假设下当前差异有多极端？ | null distribution / p-value |
| CI | effect 的 uncertainty 范围多大？ | interval |

实际中 bootstrap 可以用于构造 CI，但 CI 也可以来自解析公式、Bayesian posterior 等其它方法。

## 8. Binary Paired Outcome

对于 success/failure paired tasks：

```text
wins   = baseline wrong, candidate right
losses = baseline right, candidate wrong
```

版本差异主要来自 discordant pairs。

可以：

- 报 paired net delta；
- 对 task pairs bootstrap；
- 使用适合 paired binary data 的 exact / McNemar-style inference；
- 或使用 paired randomization / sign-flip 思路。

知识库这里更强调设计原则，而不是要求你只背某一个检验名。

## 9. Small N 时 Bootstrap 也不是魔法

如果只有：

```text
N = 8 tasks
```

bootstrap 只是不断重组这 8 个 task。

它不能创造：

```text
新 capability coverage
新 failure mode
新 task diversity
```

所以很宽的 CI 是诚实结果；不要靠多跑 bootstrap 次数让小样本“变可靠”。

## 10. Rare Event 的困难

例如 false accept 只有 1 次：

```text
1 / 200
```

简单 bootstrap sample 中可能大量出现 0 次，也可能多次抽中唯一事件，分布会很离散。

这不是算法坏，而是数据告诉你：

> 对 rare event 的频率估计证据很少。

解决方法通常是增加 eligible opportunities / targeted critical set，而不是仅换一个 fancy estimator。

## 11. Non-representative Sample 的 CI 不能修复 Bias

CI 描述的是 sampling uncertainty，不会自动修复：

```text
benchmark leakage
selection bias
wrong sampling frame
judge bias
protocol drift
```

一个非常窄的 CI 也可能围绕错误 estimand 或有偏 sample。

因此：

```text
low variance
≠ low bias
```

## 12. Slice CI 与 Multiple Comparisons

如果对 30 个 slice 都算 CI，然后只展示一个不跨 0 的 slice，就会产生 selection bias。

应区分：

```text
pre-registered critical slices
vs
post-hoc exploratory slices
```

后者更适合生成 hypothesis，而不是立即作为 confirmation。

## 13. 一个实用选择表

### 我想表达 effect uncertainty

优先：

```text
effect estimate + CI
```

### statistic 很复杂、解析 SE 不好算

考虑：

```text
bootstrap
```

### 想在较弱分布假设下检验 paired H0

考虑：

```text
paired permutation / randomization test
```

### 数据有 task → repeats 层级

必须：

```text
resampling respects clusters
```

## Evaluation design

每次正式 uncertainty analysis 先填写：

```text
Estimand:
Analysis unit:
Clusters / nesting:
Pairing key:
Statistic:
CI method:
Resampling unit:
Null hypothesis:
Permutation exchangeability assumption:
Number of pre-registered tests:
```

## Common wrong answers

### 错误 1：Bootstrap 次数越多，原始样本就越大

错。更多 resamples 只减少 Monte Carlo error，不增加真实独立信息。

### 错误 2：Permutation 就是随便 shuffle rows

必须基于零假设下合法的 exchangeability structure。

### 错误 3：CI 跨 0，证明两个系统等价

只能说当前证据不足以排除 0 附近 effect；equivalence 需要专门定义可接受区间和设计。

### 错误 4：p < 0.05 就说明 effect 很大

p-value 受 N 和 variance 影响，不等于 effect size。

### 错误 5：36 runs 就 bootstrap 36 rows

如果它们来自 12 个 task × 3 repeats，必须处理 task clustering。

## VeriAgent example

VeriAgent 的 12 个 test task 每个条件重复 3 次。如果要估计“对新 task 的平均 paired effect”，应让 task 成为主要 resampling unit，而不是把 36 runs 当 36 个独立任务。

而 candidate memory 的 `+1/36` 本身就非常小；即使计算一个 p-value，也不能绕过更重要的问题：失败发生阶段与 memory 作用阶段不匹配，所以 outcome difference 不支持 memory causal attribution。

## Follow-up questions

- percentile bootstrap 有什么局限？
- paired binary data 为什么只靠两个独立 proportion CI 不够？
- cluster bootstrap 如何实现？
- permutation 的 exchangeability 什么时候被破坏？
- equivalence / non-inferiority 应如何另行设计？

## Evidence of mastery

达到 S4 时，应能面对一个 Eval dataset，明确说出：

```text
我要估计什么
哪个 unit 独立
bootstrap 抽谁
permutation 换什么标签
CI 表达什么
p-value 不表达什么
```

## Related knowledge

- [Q02 Estimand & Unit](01_Estimand_and_Unit_of_Analysis.md)
- [Q25 Credible Improvement](02_Is_the_Improvement_Credible.md)
- [Q26 Paired Evaluation](03_Paired_Evaluation.md)
- [Q28 Tasks vs Repeats](05_Task_Count_and_Repeats.md)
