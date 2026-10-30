# Q29 多指标、多切片、多轮试验为什么会产生 Multiple-Comparison 问题？

- Level: M2
- Mastery: S0
- Related Parts: Part 4 / Part 5 / Part 6
- Related Patterns: P04 Slice Before Aggregate; P11 Holdout after Development

## 30-second answer

如果你同时看很多 metric、slice、prompt、threshold、seed 或多轮实验，即使系统其实没有真实提升，也更容易“碰巧”找到一个看起来很好的结果。问题不只来自一次正式的 20 个 hypothesis tests，还来自整个开发过程中不断看结果、换配置、再看结果的 **adaptive analysis**。

解决思路不是简单“都 Bonferroni”，而是先区分 **confirmatory** 与 **exploratory**：预先冻结 primary metric / critical slices / hypothesis family；必要时对同一 family 做 Holm / FDR 等调整；探索中发现的亮点应进入下一轮 fresh holdout，而不是直接当成最终证据。

## 90-second answer

假设每个独立 test 都用 `α=0.05`。如果一次看 20 个完全无效的 hypothesis，至少出现一个 false positive 的概率在独立近似下是：

```text
1 - 0.95^20 ≈ 64%
```

现实 Eval 更复杂，因为我们不仅看 20 个 p-values，还可能：

```text
换 prompt
换 threshold
换 task subset
换 aggregation
看很多 slices
多次 rerun
最后只报告最好的一版
```

这种 winner selection 会产生 selection bias / winner's curse。

因此统计纪律应从实验设计开始：一个 primary estimand、一组预定义 critical slices、明确 exploratory space、固定 holdout。必要时用 family-wise error control 或 FDR；但更重要的是不要把开发期反复试出来的最好结果当成 fresh confirmation。

## 1. Multiple Comparisons 不只是“同时做很多检验”

最显式的情况：

```text
20 metrics
× 10 slices
= 200 comparisons
```

但 Eval 中更常见的是隐式 multiplicity：

```text
试 8 个 prompt
试 5 个 threshold
看 6 个 model variants
跑 3 次不同 seed
挑最好的一版
```

即使你最后只展示一个数字，选择过程已经使用了大量比较。

## 2. Family-wise Error 的直觉

单个 test 的 false positive rate 是 5%，不表示：

```text
整个分析中发现一个“显著结果”的 false positive 风险也是 5%
```

如果有 m 个独立 null tests：

```text
P(at least one false positive)
= 1 - (1 - α)^m
```

例如 `m=20, α=0.05`：

```text
≈ 64.2%
```

这只是直觉公式；现实 tests 往往相关，所以精确概率不同，但问题仍存在。

## 3. Metrics、Slices、Configs 属于不同的 Comparison Family

不要机械地把全世界所有数字一次 Bonferroni。

先定义 analysis family，例如：

```text
Primary release metrics
Critical safety slices
Exploratory capability slices
Prompt-selection candidates
```

哪些结果共同服务于同一个决策，就需要考虑它们的联合选择风险。

## 4. Confirmatory vs Exploratory

### Confirmatory

运行前冻结：

```text
primary estimand
primary metric
critical slices
candidate version
analysis method
release threshold
```

这类结果可以承担强结论。

### Exploratory

结果出来后发现：

```text
某个 task family +12pp
某类 failure 几乎消失
某 threshold 特别好
```

这些很有价值，但更合适的身份是：

```text
new hypothesis
```

下一步应 fresh confirm，而不是立即升级成“已证明”。

## 5. Winner's Curse

假设 20 个 prompt 的真实能力完全一样，但每个都带 sampling noise。

你选：

```text
最高分 prompt
```

那么它的 observed score 往往同时包含：

```text
true performance
+ positive noise
```

因此在新数据上常会回落。

这就是为什么：

```text
best on dev
```

和：

```text
best generalizing system
```

不是同一个概念。

## 6. 常见控制方法

### Bonferroni

将显著性阈值变成：

```text
α / m
```

简单、保守，适合少量关键 family。

### Holm

step-down family-wise error control，通常比简单 Bonferroni 更有力。

### Benjamini-Hochberg / FDR

控制发现集合中的预期 false discovery proportion，适合大量探索性 hypothesis，但不等价于严格控制“一个错误都不能有”。

选择方法必须看决策风险，不是默认一个算法覆盖所有场景。

## 7. 预注册 Primary Metric 是最有效的控制之一

如果上线决策事先写：

```text
Primary: Task Success
Guardrail: False Accept
Critical slice: Safe Stop
Secondary: Tokens / Valid Success
```

然后其它 20 个 slice 只做诊断，那么 evidence hierarchy 很清楚。

相反，如果：

```text
总分没涨
→ 看 slice
→ slice 没涨
→ 看 cost
→ cost 没涨
→ 看某个 threshold
```

直到找到一个正结果，就会严重 over-interpret。

## 8. Holdout 是对 Adaptive Analysis 的核心防线

开发过程允许探索：

```text
Dev
→ analyze failures
→ change system
→ rerun Dev
```

但 confirmation 应在：

```text
Fresh / held-out set
```

完成。

一旦看过 holdout failure 并据此修改系统，这个 holdout 的 exposure status 就应更新，不能继续假装 clean。

## 9. 多轮实验也是 Multiple Looks

即使每轮只有一个 metric：

```text
Round 1 p=.12
Round 2 p=.08
Round 3 p=.04 → stop and report
```

如果没有预先定义 sequential rule，这种“看到显著就停”的策略也会提高 false positive 风险。

因此应冻结：

```text
sample size
or
valid sequential testing procedure
```

## 10. Slice Mining 的正确姿势

错误：

```text
切 100 个 slice
→ 挑下降最多的那个
→ 宣称根因
```

更合理：

```text
predefined capability slices
→ confirmatory comparison

post-hoc failure clusters
→ exploratory diagnosis
→ regression / hard set
→ next-round confirmation
```

这与 Q19 的 slice diagnosis 完全一致。

## 11. Multiple Comparisons 不只影响 p-value

即使你根本不算 p-value，仍会有 selection bias。

例如从 50 个结果中挑最高 accuracy：

```text
max observed score
```

本身就会被 upward noise 偏置。

因此问题本质是：

> **结果是否参与了选择这个结果本身？**

## 12. 一个实用 Analysis Contract

正式实验前写：

```text
Primary hypothesis:
Primary metric:
Primary unit:
Critical guardrails:
Confirmatory slices:
Exploratory slices:
Number / family of planned tests:
Multiplicity strategy:
Stopping rule:
Holdout policy:
```

## Common wrong answers

### 错误 1：我只报告最终一个数字，所以没有 multiple comparisons

如果这个数字是从很多配置中挑出来的，选择过程本身就是 multiplicity。

### 错误 2：所有测试都 Bonferroni 就最科学

过度保守会损失 power，而且不同 hypothesis family / decision risk 应分开设计。

### 错误 3：探索性 slice 显著，所以可以直接上线

探索结果应 fresh confirm。

### 错误 4：不算 p-value 就不存在问题

winner selection / adaptive analysis 仍会产生 bias。

### 错误 5：holdout 可以无限重复使用，只要不训练模型

反复查看并据此改 prompt / rule / memory 也会 test-set overfit。

## VeriAgent example

如果针对 Olist challenge dev failures 不断调整 memory、prompt、schema guard，再反复在同一个 test 上看哪个版本最好，那么即使没有微调模型权重，也会逐渐把 test 变成开发数据。

正确做法是：开发可在 dev / regression 上迭代；最终 improvement 需要 fresh held-out confirmation，并记录 exposure ledger。

## Follow-up questions

- Holm 和 BH 的目标有什么不同？
- exploratory result 什么时候可以 promote 成 confirmatory hypothesis？
- dashboard 上几十个指标如何定义 family？
- sequential testing 如何合法化？
- winner's curse 如何通过 nested holdout 缓解？

## Evidence of mastery

达到 S3/S4 时，应能看到一个“试了很多方案后提升显著”的实验，主动追问：

```text
看了多少配置？
看了多少 metric / slice？
哪个是 primary？
holdout 看过几次？
是否 fresh confirm？
```

## Related knowledge

- [Q22 Leakage & Test-set Overfitting](../05_Benchmark_and_Evaluation_Data/02_Leakage_and_Test_Set_Overfitting.md)
- [Q25 Credible Improvement](02_Is_the_Improvement_Credible.md)
- [Q27 Bootstrap / Permutation / CI](04_Bootstrap_Permutation_and_Confidence_Intervals.md)
