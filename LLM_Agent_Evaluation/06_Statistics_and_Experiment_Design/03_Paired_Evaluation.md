# Q26 什么时候应该使用 Paired Evaluation，为什么同题配对通常更有力？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 5 / Part 6
- Related Patterns: P03 Paired Same-Task Comparison; P11 Holdout after Development
- Related Metrics: Paired Net Win/Loss, Slice Regression Delta

## 30-second answer

当 baseline 和 candidate 能在**同一个 task / environment / evaluation contract** 下运行时，我优先做 paired evaluation。因为 task 难度、参考答案、环境条件等大量 nuisance variation 被共享，我们直接分析每个 task 上的差值，而不是比较两个彼此独立的总体均值。

对于二元 outcome，至少看 `wrong→right` 和 `right→wrong`；对于连续分数，分析每个 task 的 `D_i = candidate_i - baseline_i`。如果有 repeats，应先明确 pairing key 和 task-level aggregation，不能把相关重复当独立 pair。

## 90-second answer

独立两组比较问的是：

```text
mean(candidate sample) - mean(baseline sample)
```

paired comparison 则问：

```text
对同一个 task，candidate 相对 baseline 改变多少？
```

设第 i 个 task 的结果为：

```text
D_i = Y_i(candidate) - Y_i(baseline)
```

因为同一个 task 的难度会同时影响两个系统，paired design 可以消掉一部分 task-level variation。直觉上：如果 A/B 在同一题上的表现高度相关，那么差值 `D_i` 的方差通常比两个独立均值之差更小，因此估计更有力。

但 pairing 不是“同一张表里两列”就够了。必须冻结：相同 task、相同 environment snapshot、相同 evaluator、相同 budget，并写清 pairing key。若一个系统多跑了 retry 或看到了不同 memory，pair 仍可比较，但 treatment difference 必须是预先定义的系统差异，而不是意外 protocol drift。

## 1. 为什么版本比较天然适合 Paired Design

LLM / Agent 任务之间往往差异很大：

```text
Task A 很简单
Task B 很复杂
Task C 需要 tool recovery
Task D 有稀有边界条件
```

如果 baseline 在一批题上跑、candidate 在另一批题上跑，那么：

```text
system effect
```

和：

```text
task mix difference
```

会混在一起。

最直接的解决方式是让两个版本面对同一组 task。

## 2. Paired Difference

连续 / ordinal metric：

```text
D_i = score_i(candidate) - score_i(baseline)
```

主要估计量：

```text
mean(D_i)
```

二元 success：

```text
baseline  candidate
   1          1      both correct
   1          0      loss
   0          1      win
   0          0      both wrong
```

净变化：

```text
(wins - losses) / N_tasks
```

对于二元 paired outcome，真正决定版本差异的是 discordant pairs：

```text
wins + losses
```

`both correct` 和 `both wrong` 对净差没有直接贡献，但对绝对能力水平仍有信息。

## 3. 为什么 Paired 通常更有力

如果两个系统在同一 task 上的结果正相关，则：

```text
Var(B - A)
= Var(B) + Var(A) - 2 Cov(A, B)
```

当 `Cov(A,B) > 0`，差值方差会下降。

在 Eval 中这很常见，因为同一难题通常让两个版本都更难，同一简单题通常让两个版本都更容易。

因此 pairing 利用了共享 task 难度。

## 4. Pairing Key 必须明确

Agent Eval 常见层级：

```text
(task_id, repeat_id, condition)
```

一个安全的 paired key 可能是：

```text
(task_id, repeat_id)
```

然后 condition 分成 baseline / candidate。

必须检查：

- 每个 key 两个条件都存在；
- 没有重复 pair；
- 环境初始状态一致；
- task/reference version 一致；
- evaluator version 一致。

否则“paired”只是表面形式。

## 5. 有 Repeats 时怎么 Pair

假设：

```text
12 tasks × 3 repeats × 2 conditions
```

可以有两种主要 estimand。

### A. Task-level effect

先对每个 task 内的 repeats 聚合：

```text
p_i(A) = mean_r Y_ir(A)
p_i(B) = mean_r Y_ir(B)
D_i = p_i(B) - p_i(A)
```

再跨 task 分析 `D_i`。

适合：

> 对新任务平均而言，candidate 是否更好？

### B. Run-level paired effect

如果 repeat_id 本身有可比意义，也可以：

```text
D_ir = Y_ir(B) - Y_ir(A)
```

但 uncertainty 仍要考虑同一 task 内的相关性。

不能把 36 个 `D_ir` 默认当成 36 个独立 task effects。

## 6. Same Seed 是否必要？

不一定。

Same seed 有时能减少随机差异，但在不同 prompt / controller / tool path 下，“同 seed”不一定代表同一随机扰动，而且可能产生不自然耦合。

更重要的是：

```text
same task
same initial state
same environment
same budget contract
same evaluation path
```

如果系统本身有 stochasticity，通常通过 repeated paired runs 来估计，而不是迷信 seed 对齐。

## 7. 什么情况下 Paired 不成立

### A. 两组任务不同

例如 baseline 用旧 benchmark，candidate 用新 benchmark。

不能因为 task family 名称相同就强行配对。

### B. Environment 不可还原

例如真实 web 环境在两个条件运行时已经变化。

此时 pairing quality 会下降，需要 snapshot / replay / blocking。

### C. Treatment 会永久改变后续环境

例如一个 Agent 的动作修改了共享数据库，导致另一个条件面对不同 state。

需要独立 environment clone 或 counterbalanced order。

### D. User-level online experiment

如果同一用户不能同时接受两个条件，可以按 user randomization 做独立 A/B，而不是 task-level paired。

## 8. Paired Design 不会自动消除所有 Bias

它不能修复：

```text
benchmark leakage
judge bias
protocol drift
memory contamination
order effect
carryover effect
```

Paired 只是在相同单位上比较，提高可比性和统计效率。

## 9. Order 与 Carryover

对于 stateful Agent，运行顺序可能影响结果：

```text
baseline 先跑
→ cache / memory / environment 改变
→ candidate 后跑
```

这时需要：

- 独立 state clone；
- reset；
- randomized / counterbalanced order；
- 禁止 test writeback。

否则 paired design 反而会引入 carryover contamination。

## 10. Paired Reporting 最少保留什么

对于 binary outcome：

```text
N pairs
baseline success
candidate success
both correct
wins
losses
both wrong
net paired delta
uncertainty
```

对于 continuous metric：

```text
N pairs
mean(A)
mean(B)
mean paired difference
median paired difference
CI
slice distribution
```

## Common wrong answers

### 错误 1：同样 N，paired 和 unpaired 没区别

当 task-level variation 很大且 A/B 高度相关时，paired 通常显著减少 nuisance variance。

### 错误 2：两组平均分一样，所以没有 task-level difference

可能存在大量 win/loss 相互抵消；paired table 能看见这种 churn。

### 错误 3：同一 task 跑了 3 次，所以有 3 个独立 pair

它们共享 task，属于嵌套观测。

### 错误 4：用了同一个 seed 就等于严格 paired

Pairing 的核心是 experimental unit 和环境条件，而不是 seed 标签。

### 错误 5：paired test 显著，就证明机制有效

它只支持 outcome difference；机制归因仍要结合 trace / intervention evidence。

## VeriAgent example

VeriAgent candidate memory 的 held-out test 使用同一 12 个 task，在 no-memory / candidate 两种条件下各重复 3 次，并按 task + repeat 配对。

结果可写成：

```text
3 wrong→right
2 right→wrong
27 both right
4 both wrong
```

这比只看：

```text
29/36 vs 30/36
```

更清楚地说明 candidate 造成了双向变化，而不是稳定地修复所有失败。

## Follow-up questions

- paired bootstrap 应在哪一层 resample？
- binary paired outcome 为什么重点看 discordant pairs？
- order effect 如何处理？
- same seed 是否会制造不自然耦合？
- paired design 能否用于 latency / cost？

## Evidence of mastery

达到 S4 时，应能拿到两版系统结果，先判断是否真的可 pair，再定义 pairing key、paired estimand、nested repeat handling、order/reset policy 和 uncertainty method。

## Related knowledge

- [Q02 Estimand & Unit](01_Estimand_and_Unit_of_Analysis.md)
- [Q25 Credible Improvement](02_Is_the_Improvement_Credible.md)
- [Q27 Bootstrap / Permutation / CI](04_Bootstrap_Permutation_and_Confidence_Intervals.md)
