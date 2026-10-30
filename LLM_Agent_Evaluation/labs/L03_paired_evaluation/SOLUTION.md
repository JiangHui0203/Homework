# L03 — Solution / Reference Analysis

> 先独立完成 Lab。这里给的是参考口径，不替代自己的报告。

## 1. Frozen design

```text
12 distinct tasks
3 paired repeats / task
36 paired run rows

Primary estimand:
mean task-level success difference
candidate - baseline

Primary unit:
task_id

Nested unit:
repeat_id
```

因此：

```text
36 = execution / paired-run count
12 = primary independent task count for the future-task claim
```

## 2. Raw accuracy

```text
Baseline  = 29/36 = 80.6%
Candidate = 30/36 = 83.3%

Raw delta = +1/36
          = +2.78 pp
```

因为每个 task 恰好都有 3 个 repeats，task-average point estimate 在这个数据集上也恰好是：

```text
+2.78 pp
```

但这不意味着可以把 36 rows 当成 36 个独立 tasks；point estimate 相同，不代表 uncertainty structure 相同。

## 3. Task-level paired movement

| Task | Slice | Baseline | Candidate | Δ |
|---|---|---:|---:|---:|
| T01 | lookup | 1.000 | 1.000 | 0 |
| T02 | lookup | 1.000 | 1.000 | 0 |
| T03 | lookup | 0.667 | 0.667 | 0 |
| T04 | join | 0.667 | 1.000 | +0.333 |
| T05 | join | 0.667 | 1.000 | +0.333 |
| T06 | join | 0.667 | 0.667 | 0 |
| T07 | time | 1.000 | 1.000 | 0 |
| T08 | time | 1.000 | 0.667 | -0.333 |
| T09 | time | 0.667 | 0.667 | 0 |
| T10 | safe_stop | 1.000 | 1.000 | 0 |
| T11 | safe_stop | 0.667 | 1.000 | +0.333 |
| T12 | safe_stop | 0.667 | 0.333 | -0.333 |

所以：

```text
Wins   = 3  (T04, T05, T11)
Losses = 2  (T08, T12)
Ties   = 7
```

这说明 `+2.78pp` 实际来自一个很小的 discordant task 集合，而不是广泛一致的改善。

## 4. Task-level bootstrap CI

脚本固定：

```text
20,000 bootstrap samples
resampling unit = task_id
seed = 20261030
```

参考结果：

```text
95% bootstrap CI
= [-8.33 pp, +13.89 pp]
```

解释：

- 区间很宽；
- 包含负效应；
- 也包含比当前 point estimate 更大的正效应；
- 当前 12 个 tasks 无法把 effect 精确估到足以排除 0。

正确结论不是：

```text
systems are equal
```

而是：

```text
current evidence is too imprecise to establish a stable positive effect
```

## 5. Exact task-level sign-flip permutation

非零 task differences 只有 5 个：

```text
3 positive
2 negative
```

exact two-sided sign-flip permutation：

```text
p = 1.000
```

这里 p 很大并不表示：

```text
P(H0 | data) = 1
```

而表示在冻结 null / exchangeability 结构下，当前这样大小的绝对 paired effect 并不罕见。

因为 non-zero discordant task 很少，检验本身的信息也非常有限。

## 6. Practical significance

冻结 minimum practical effect：

```text
+5.0 pp
```

当前：

```text
point estimate = +2.78 pp
```

连 point estimate 本身都没有达到 +5pp。

而且 CI：

```text
[-8.33, +13.89] pp
```

也远不足以证明 effect 至少达到 +5pp。

所以：

```text
statistical evidence insufficient
+
practical threshold not met by point estimate
```

## 7. Slice results

```text
lookup
baseline 88.9%
candidate 88.9%
delta 0.00 pp

join
baseline 66.7%
candidate 88.9%
delta +22.22 pp

time
baseline 88.9%
candidate 77.8%
delta -11.11 pp

safe_stop
baseline 77.8%
candidate 77.8%
delta 0.00 pp
```

`join +22.22pp` 很诱人。

但 contract 已冻结：

```text
overall = confirmatory
all 4 slices = exploratory
```

因此正确表述：

> join slice shows an exploratory positive signal.

错误表述：

> candidate has proven a +22pp improvement on join capability.

如果这个 slice 很重要，应在 fresh tasks 上把 `join` 预注册成 confirmatory target 再验证。

## 8. Repeat instability

脚本定义：

```text
同一 task 的 3 次结果不全相同
→ unstable
```

Baseline：

```text
7/12 unstable
T03, T04, T05, T06, T09, T11, T12
```

Candidate：

```text
5/12 unstable
T03, T06, T08, T09, T12
```

说明 stochasticity 不是零，因此 repeats 有价值。

但 primary claim 是 future-task generalization，而 distinct tasks 只有 12。

所以如果新增一批预算，合理方向通常是：

```text
保留最小 repeats 用于稳定性估计
+
优先增加更多独立 tasks
```

而不是无限增加同 12 题 repeats。

## 9. Final evidence statement

一个合格表述：

> On 12 distinct paired tasks with 3 repeats per task, candidate increased raw success from 29/36 to 30/36, corresponding to a task-averaged paired effect of +2.78 pp. The movement consisted of 3 task wins, 2 losses, and 7 ties. A task-level bootstrap gave a 95% CI of approximately [-8.33, +13.89] pp, and the exact two-sided task sign-flip permutation p-value was 1.000. The point estimate is below the frozen +5 pp practical-effect target, and the interval is too wide to establish a stable positive effect. Slice results are exploratory; the +22.22 pp join signal requires fresh confirmatory evaluation. Therefore the current evidence is inconclusive and does not support claiming a reliable practically meaningful improvement.

## 10. 90-second answer

> 我不会因为 29/36 到 30/36 就直接说提升。先看 estimand 和 unit：这里是 12 个不同 task，每题 3 次 repeat，所以 primary independent unit 是 task，不是 36 个 run。按 task 配对后是 3 个 win、2 个 loss、7 个 tie，平均差只有 +2.78pp。task-level bootstrap 的 95% CI 大约是 -8.33 到 +13.89pp，区间很宽且跨 0；exact sign-flip permutation 也没有提供反对零效应的证据。并且冻结的 practical threshold 是 +5pp，point estimate 本身都没达到。虽然 join slice 看起来 +22pp，但它是四个 exploratory slices 里事后看到的，不能直接升级成 confirmatory claim。因此我会把当前结论写成 evidence insufficient / inconclusive，并优先在更多独立 tasks 上做 fresh confirmation，同时保留适量 repeats 估计随机性。
