# Q24 Difficulty、Coverage、Slice Balance 和 Natural Frequency 应如何权衡？

- Level: M2
- Mastery: S0
- Related Parts: Part 5 / Part 6
- Related Patterns: P04 Slice Before Aggregate; P05 Frozen Core + Rotating Hard Set
- Related Registry: `BENCHMARKS.md`

## 30-second answer

没有一种 sampling distribution 能同时最优地完成“估计真实产品表现”和“诊断稀有脆弱能力”。Natural-frequency sampling 适合估计目标总体；balanced / hard sampling 适合保证 slice 覆盖和提高诊断功效。

所以我会把 **sampling distribution 与 reporting distribution 分开说明**：benchmark 为什么这样采样、每个 slice 占多少、总分是否加权回目标总体。必要时同时报告 natural-weighted estimate 与 balanced diagnostic score，而不是把人为均衡后的分数冒充线上成功率。

## 90-second answer

Benchmark 设计里常有四个冲突目标：

```text
Coverage      关键能力都要看到
Difficulty    避免大量 ceiling item
Slice balance 稀有关键 slice 要有足够样本
Natural frequency 希望接近真实任务分布
```

如果完全按线上自然频率采样，罕见但高风险的 tool / safe-stop / join-fanout failure 可能几乎没有样本；如果强行每类 25%，又会让 benchmark 总分失去自然分布意义。

因此推荐双轨：

```text
Representative estimate
= 按目标总体抽样 / 重加权

Diagnostic view
= 按 capability / risk slice 保证最低样本量
```

两者都报告，并明确哪一个用于什么决策。

## 1. 四个目标分别在优化什么

### Coverage

回答：

> 我声明的能力空间，有哪些部分真正被测到了？

Coverage 不是样本数，而是对 target claim 的覆盖。

### Difficulty

回答：

> 题目是否处在能观察系统差异的难度区域？

太容易产生 ceiling，太难产生 floor。

### Slice Balance

回答：

> 每个重要 capability / risk slice 是否有足够观测支持诊断？

### Natural Frequency

回答：

> benchmark 中各类任务的权重是否接近我们想估计的真实总体？

四者不能简单统一。

## 2. Natural Sampling 的优点与限制

优点：

- 更接近部署总体；
- 总体 metric 更容易解释；
- 可估计真实 exposure 下的平均表现。

限制：

- rare slice 样本少；
- critical failure 可能长期抽不到；
- 大量 easy/common tasks 会淹没小但重要的 regression。

例如线上：

```text
simple lookup 80%
join-heavy    10%
safe-stop      2%
others         8%
```

如果只抽 100 题，safe-stop 期望只有约 2 题，很难评价可靠性。

## 3. Balanced Sampling 的优点与限制

假设四个 family 各取 25%。

优点：

- 每类都有统计/诊断信号；
- 版本差异更容易定位；
- 对 rare failure 更敏感。

限制：

- benchmark distribution 偏离线上；
- 简单平均不能叫 production success estimate；
- 人为 slice 定义会影响总分。

## 4. Risk-weighted Sampling

有些低频任务的错误代价极高。

例如：

```text
ordinary lookup error   low impact
wrong external action   high impact
false accept            high impact
privacy leakage         critical
```

这时可以建立 risk-weighted set 或 critical regression set。

但必须明确：

```text
risk-weighted score
≠ natural-frequency score
```

## 5. Coverage Floor

一个实用做法：给关键 slice 设最低样本量，而不是强行完全均衡。

例如：

```text
natural sample
+ ensure each critical slice n >= 30
```

分析时可以：

- slice 内正常报告；
- overall 若要估计真实总体，则按 population weights 重加权。

## 6. 两种 Overall Score

### Diagnostic Macro

```text
Macro score
= mean(slice score)
```

每个 slice 等权，适合看能力是否均衡。

### Population-weighted

```text
Weighted score
= Σ population_weight_s × score_s
```

适合估计目标总体表现。

两者可能方向相反，这不是谁“算错了”，而是 estimand 不同。

## 7. Difficulty Balance

不要只按 easy/medium/hard 各 1/3。

先问：

```text
为什么需要 difficulty 分层？
```

可能是：

- 避免 ceiling；
- 测能力边界；
- 检查预算随难度的变化；
- 检查 long-horizon degradation。

Difficulty 可以由多种信号定义：

```text
historical pass rate
constraint count
horizon / tool depth
reference complexity
human effort
```

但最好固定定义，不能每个版本按结果重新分档。

## 8. Hard-case Oversampling

如果 hard case 被过采样：

```text
benchmark score ↓
```

并不一定说明产品能力下降，只说明 benchmark sampling changed。

因此 benchmark version 更新时必须记录 slice mix。

## 9. Slice Definition Drift

如果今天 `hard` 是 top 20% baseline failures，明天又按新模型重新定义 top 20%，那么不同版本 hard score 不再直接可比。

建议：

- 固定 slice definition；或
- 明确写成 dynamic slice，并避免长期直接比较。

## 10. Simpson's Paradox

版本 A 在每个 slice 都不差，但因为测试样本 mix 改变，overall 反而下降；或反之。

因此版本比较应同时保存：

```text
same item paired comparison
per-slice score
slice counts / weights
overall aggregation rule
```

这也是为什么 benchmark composition 是 artifact，而不只是背景信息。

## 11. Benchmark Sampling Contract

每个 benchmark 至少记录：

```text
target population
sampling frame
sampling method
slice quotas
minimum slice counts
difficulty policy
risk oversampling
population weights
aggregation rule
```

没有这些信息，一个总分很难解释。

## Evaluation design

### 双视图报告

推荐同一评测报告同时给：

```text
1. Representative / population-weighted view
2. Diagnostic / balanced slice view
```

并在每个 score 旁标注其 estimand。

### 小样本时

不要制造虚假的精确小数。

优先报告：

```text
counts
slice pass / total
paired changes
uncertainty
```

## Common wrong answers

### 错误 1：benchmark 应完全复现线上自然频率

那会让罕见但关键的 failure 几乎不可评价。

### 错误 2：每个类别一样多最公平

均衡提高诊断性，但总分不再代表自然频率。

### 错误 3：Hard 占比提高后准确率下降，说明模型退化

如果 benchmark composition 变了，不能直接归因给模型。

### 错误 4：Macro 比 Micro 更科学

它们估计不同问题。必须先定义 estimand。

### 错误 5：按当前模型表现重新分 difficulty 更准确

这会让跨版本比较发生 target drift。

## Counterexample / boundary

如果 benchmark 只用于一个极窄、固定、均匀的合成任务空间，natural frequency 与 balanced coverage 可能近似一致。但真实 Agent / 产品任务通常有长尾、风险差异和能力 slice，不应默认二者相同。

## VeriAgent example

VeriAgent challenge set 的四个 family 在 dev/test 中各自均衡，是典型 diagnostic design：它确保 `payment_grain / customer_identity / join_fanout / time_scope` 都有足够观察，不意味着 Olist 用户真实请求中四类各占 25%。

因此它适合回答“候选 memory / controller 在这些已定义能力族上表现怎样”，不适合直接回答“生产环境总体成功率是多少”。如果未来要估计后者，需要从真实目标任务总体抽样或用可信 population weights 重加权。

## Follow-up questions

- macro 与 weighted overall 哪个应该做 release gate？
- rare critical slice 最少需要多少样本？
- dynamic difficulty 能否用于每轮 hard mining？
- risk weighting 如何避免业务主观性？
- natural frequency 漂移后 benchmark 怎么更新？

## Evidence of mastery

达到 S3/S4 时，应能拿到一份 benchmark composition，明确指出：

- target population；
- sampling distribution；
- diagnostic quotas；
- natural weights；
- difficulty policy；
- aggregation estimand；
- 哪些 score 可外推、哪些只能诊断。

## Related knowledge

- [Q21 Discriminative Benchmark Design](01_Discriminative_Benchmark_Design.md)
- [Q23 Benchmark Set Roles](03_Frozen_Regression_Hard_and_Rotating_Sets.md)
- [Q02 Estimand & Unit of Analysis](../06_Statistics_and_Experiment_Design/01_Estimand_and_Unit_of_Analysis.md)
- [Benchmarks Registry](../BENCHMARKS.md)
