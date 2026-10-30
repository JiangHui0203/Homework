# Q25 准确率从 70% 到 73%，你如何判断这 3 个点是否可信？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 5 / Part 6
- Related Patterns: P03 Paired Same-Task Comparison; P04 Slice Before Aggregate; P11 Holdout after Development
- Related Metrics: Paired Net Win/Loss, Confidence Interval, Repeat Consistency

## 30-second answer

不能只看 `70% → 73%`。我会先确认两组是否在**同一个冻结评测合同**下比较，再看：独立单位是什么、是否 paired、具体是哪些 task 从错变对 / 从对变错、置信区间有多宽、重复运行是否稳定、差异是否集中在少数 slice，以及这 3 个点是否经过多轮试验后才挑出来。

如果是同一批 task，优先分析 task-level paired difference；如果有 repeats，要保留 task 内相关性，不能把所有 run 当独立样本。最终结论应该是：**effect size + uncertainty + paired movement + practical relevance**，而不是只报一个 point estimate 或 p-value。

## 90-second answer

判断 3 个点是否可信，我通常按这个顺序：

```text
1. Comparable protocol?
2. Correct estimand / unit?
3. Paired movement?
4. Uncertainty?
5. Repeat stability?
6. Slice consistency?
7. Multiple testing / adaptive development?
8. Practical significance?
```

例如 100 个 paired tasks 上 baseline 70/100、candidate 73/100。这个 +3pp 可能来自：

```text
10 wrong→right
7 right→wrong
```

也可能来自：

```text
3 wrong→right
0 right→wrong
```

两者 point estimate 都是 +3pp，但证据结构完全不同。因此 paired win/loss 比单独看两个 accuracy 更有信息。

我会对 task-level paired effect 做 CI，必要时做 paired bootstrap / permutation；若任务存在 repeats，则以 task 为主要 resampling unit。最后再问：即使统计上与 0 有区分，这个提升是否大到足以抵消额外成本、延迟或风险。

## 1. 第一步不是算显著性，而是检查可比性

任何统计结论之前先确认：

```text
same task set / sampling frame
same evaluator / reference
same failure handling
same budget
same tool / environment snapshot
same aggregation rule
same exposure policy
```

如果 candidate 比 baseline 多拿了 retry budget，或者 grader 版本不同，那么 `+3pp` 可能首先是 protocol change，而不是 system improvement。

## 2. 先写清楚 estimand

常见目标有：

```text
Task-level average success difference
Run-level reliability difference
User-level utility difference
Critical-slice error-rate difference
```

它们需要不同的 unit 和 uncertainty 处理。

如果 claim 是“对新任务平均更好”，主要 unit 通常是 task。

## 3. Paired movement 比两个总体 accuracy 更有信息

同题比较时至少保留四格：

```text
baseline correct, candidate correct
baseline correct, candidate wrong   = loss
baseline wrong,   candidate correct = win
baseline wrong,   candidate wrong
```

对于二元任务：

```text
paired net change
= (wins - losses) / N_tasks
```

这个量直接对应同题条件下的版本变化。

### 同样 +3pp，稳定性可以完全不同

Case A：

```text
wins   = 10
losses = 7
net    = +3
```

Case B：

```text
wins   = 3
losses = 0
net    = +3
```

Case A 表明版本有大量双向变化，只是净值为正；Case B 表明变化少但方向单一。

所以不能只报：

```text
70% → 73%
```

应同时报：

```text
wins / losses / ties
```

## 4. Effect Size 与 Uncertainty 分开

### Effect size

回答：

> 观察到的差异有多大？

例如：

```text
Δ = +3 percentage points
```

### Uncertainty

回答：

> 如果我们从同一目标总体重新抽任务，这个 estimate 可能波动多大？

因此正式报告应至少有：

```text
point estimate
confidence interval
N independent units
```

而不是只有：

```text
p < 0.05
```

## 5. Confidence Interval 应围绕正确 unit 计算

如果有：

```text
12 tasks × 3 repeats = 36 runs
```

而目标是 task-level generalization，不能简单把 36 个 run 当独立样本做 CI。

更合理的基础方案：

```text
先在 task 内聚合 repeats
再以 task 为 resampling / analysis unit
```

或者显式使用 clustered / hierarchical 方法。

关键原则：

> **resampling unit 应匹配主要泛化单位。**

## 6. 重复运行回答的是稳定性，不自动增加 task coverage

Repeats 可以告诉你：

```text
candidate 是否只是偶然赢
同一 task 上是否经常 flip
某些 task 是否高度随机
```

但：

```text
12 tasks × 10 repeats
```

仍然只有 12 个不同 task。

如果你要证明“对更多新任务泛化”，通常增加 task diversity 比继续堆同题 repeats 更直接。

## 7. Slice 可以解释“平均提升”来自哪里

+3pp 可能来自：

```text
simple tasks +8pp
hard tasks   -2pp
```

也可能来自：

```text
safe-stop +20pp
其他全部 0
```

因此至少检查预定义关键 slice：

- capability；
- difficulty；
- risk；
- task family；
- first-failure type。

但不要事后切 50 个 slice，只挑一个最漂亮的出来。

## 8. Multiple Testing 会放大“偶然赢”

如果你试了：

```text
20 prompts
10 thresholds
8 subsets
5 metrics
```

最后挑一个 +3pp 的配置，这个提升的可信度远低于“事先冻结单一配置后，在 clean holdout 上得到 +3pp”。

因此要区分：

```text
exploratory improvement
vs
confirmatory improvement
```

开发期发现的最好结果，需要 fresh / held-out confirmation。

## 9. Statistical Significance ≠ Practical Significance

即使 CI 很窄，+3pp 也可能不值得上线，例如：

```text
accuracy +3pp
cost     +80%
latency  +2x
false accept ↑
```

反过来，在高风险 rare slice 上 +1pp 也可能很有价值。

所以最后还要回到 deployment decision：

```text
quality
cost
latency
risk
stability
```

## 10. 一个实用判断模板

看到：

```text
Baseline 70%
Candidate 73%
```

依次问：

```text
N 是多少？
unit 是 task 还是 run？
是否同题 paired？
wins / losses 是多少？
CI 多宽？
repeat 是否稳定？
关键 slice 怎么变？
是否用同一个 frozen protocol？
这个结果是 exploratory 还是 holdout confirmation？
是否看过很多配置后才选到它？
实际收益是否值得成本？
```

## Evaluation design

推荐最小报告：

```text
Primary estimand
Unit of analysis
N distinct tasks
Repeats per task
Baseline estimate
Candidate estimate
Paired delta
Wins / losses / both-correct / both-wrong
95% CI of paired delta
Critical slices
Cost / latency delta
Exposure / holdout status
Decision
```

## Common wrong answers

### 错误 1：73% 比 70% 高，所以 candidate 更好

有限样本可能出现随机波动；还要看 protocol、paired movement 与 uncertainty。

### 错误 2：p < 0.05，所以一定值得上线

统计证据不等于业务价值，也不覆盖成本和风险。

### 错误 3：36 runs，所以 n=36

如果只是 12 个 task 各跑 3 次，独立 task coverage 仍是 12。

### 错误 4：CI 跨 0，所以“两个系统一样”

更准确地说：当前数据不足以排除 0 附近的 effect；不能证明严格等价。

### 错误 5：总体 +3pp 就够了

关键 slice 可能退化；总体平均会隐藏风险。

## VeriAgent example

VeriAgent candidate memory 测试中：

```text
no-memory 29/36
candidate 30/36
```

表面净差约 +2.8pp，但 paired movement 是：

```text
3 wrong→right
2 right→wrong
27 both right
4 both wrong
```

净值只有 +1/36，而且 36 runs 来自 12 个不同 task × 3 repeats。更关键的是，13 次失败发生在 candidate memory 能作用的阶段之前，所以这个差异既不能被强统计解读，也不能做因果归因。

这说明“数字变高”只是证据链的一部分。

## Follow-up questions

- CI 与 hypothesis test 分别回答什么？
- paired 设计为什么通常更有力？
- 什么时候 +3pp 虽小但值得上线？
- repeated runs 应如何进入 CI？
- clean holdout 与 repeated test peeking 有什么关系？

## Evidence of mastery

达到 S4 时，应能看到任何 `A=70%, B=73%` 的表格，不急着下结论，而是先恢复完整的：

```text
estimand
unit
pairing
wins/losses
uncertainty
multiplicity
practical significance
```

## Related knowledge

- [Q02 Estimand & Unit of Analysis](01_Estimand_and_Unit_of_Analysis.md)
- [Q26 Paired Evaluation](03_Paired_Evaluation.md)
- [Q27 Bootstrap / Permutation / CI](04_Bootstrap_Permutation_and_Confidence_Intervals.md)
- [Q28 Tasks vs Repeats](05_Task_Count_and_Repeats.md)
