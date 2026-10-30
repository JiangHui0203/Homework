# Q28 LLM / Agent 存在随机性时，题目数量和重复次数应该怎样设计？

- Level: M1
- Mastery: S0
- Related Parts: Part 5 / Part 6
- Related Patterns: P03 Paired Same-Task Comparison; P04 Slice Before Aggregate; P11 Holdout after Development
- Related Metrics: Repeat Consistency, Confidence Interval, Paired Net Win/Loss

## 30-second answer

题目数量和重复次数解决的是两个不同问题：

- **更多 tasks**：增加任务覆盖，帮助估计对新任务的泛化；
- **更多 repeats**：估计同一 task / condition 下的随机性与稳定性。

如果主要 claim 是“对新任务平均更好”，通常在保证最小 repeat 能看见随机性后，应优先增加独立 task 数，而不是无限堆同题重复。设计时要用 pilot 估计 between-task variation、within-task variation 和 paired effect，再结合最小可接受提升、关键 slice 最低样本量与总预算做分配。

## 90-second answer

把结果写成：

```text
Y_ir
```

其中 i 是 task，r 是 repeat。

观测波动至少来自：

```text
between-task variation
+ within-task stochasticity
```

增加 task 数 N 主要减少“我抽到哪些题”的不确定性；增加 repeat 数 R 主要减少“同一道题偶然采样”的不确定性。

如果 task generalization 是主要 estimand，12 道题跑 20 次通常不等于 240 道题跑 1 次，因为它只覆盖 12 个任务结构。反过来，如果系统极度 stochastic，完全不做 repeat 可能让 paired win/loss 充满偶然 flip。

所以我通常：先 pilot → 估计 task 间与 task 内波动 → 冻结最小 repeats → 优先扩 task diversity → 对高风险 / 高波动 slice 做额外 repeats 或最低样本量保障。

## 1. Tasks 与 Repeats 回答不同问题

### 增加 Tasks

主要改善：

```text
capability coverage
population coverage
between-task uncertainty
rare slice coverage
```

### 增加 Repeats

主要改善：

```text
within-task reliability estimate
stochastic flip detection
per-task success probability estimate
recovery / trajectory variability
```

两者不是可完全替代的预算。

## 2. 一个最小层级模型

可以把某个连续型 task score 粗略写成：

```text
Y_ir = μ + α_i + ε_ir
```

其中：

```text
α_i  = task-level variation
ε_ir = run-level stochasticity
```

如果对每个 task 做 R 次平均，task mean 的 run-noise 方差会近似随：

```text
1 / R
```

下降。

但 task-level variation `α_i` 不会因为同题多跑几次而消失。

因此对“新 task 泛化”而言，增加 N 往往非常关键。

## 3. 为什么 12 × 20 不能替代 240 × 1

假设：

```text
12 tasks × 20 repeats = 240 runs
240 tasks × 1 repeat  = 240 runs
```

两者执行成本可能相近，但信息完全不同。

前者更适合：

```text
同一小批任务的 stochastic reliability
```

后者更适合：

```text
更广泛 task population coverage
```

如果你的 claim 是“未来不同任务上更好”，前者不能冒充后者。

## 4. 什么时候 Repeat 很重要

### A. Model sampling 高随机

同题结果频繁：

```text
pass / fail / pass / fail
```

单次 run 很难代表 task-level behavior。

### B. Agent trajectory 有随机分支

例如：

- planner 选择不同 tool；
- retry path 不同；
- memory retrieval 排名波动；
- external environment 返回有随机性。

### C. 你关心 reliability 本身

如果 estimand 是：

> 固定任务下，随机一次运行成功的概率是多少？

那么 repeats 本身就是核心数据，而不仅是 nuisance control。

## 5. 什么时候应优先增加 Tasks

### A. Task coverage 很少

比如只有 10–20 道独立任务，却已经每题 10 次。

### B. 版本差异主要集中在 task family

这说明 between-task heterogeneity 很重要。

### C. CI 主要受 task sampling 影响

尤其在 task-level bootstrap 中，N 很小会让 interval 很宽、离散。

### D. 你要支持更广的 generalization claim

跨 task、跨 template、跨 source 的覆盖不能靠 repeat 补出来。

## 6. 先用 Pilot 估计，不要凭感觉定 N 和 R

Pilot 阶段至少估计：

```text
baseline task success distribution
candidate-baseline paired differences
within-task flip rate
between-task heterogeneity
critical-slice event rate
cost per run
```

然后问：

```text
目标 minimum detectable effect 是多少？
希望 CI 宽到什么程度？
critical slice 至少要多少 eligible cases？
总计算预算是多少？
```

再决定 N / R。

## 7. Minimum Detectable Effect（MDE）

不要只问：

> 多少样本才能显著？

更好的问题是：

> 我们真正关心的最小改进是多少？

例如：

```text
+0.5pp 对业务没意义
+3pp 才值得讨论
```

那实验就应围绕能否可靠区分 ±3pp 量级来设计。

否则可能出现：

```text
N 很大
→ +0.2pp 显著
→ 实际不值得上线
```

## 8. Critical Slice 需要自己的样本量思维

总体 N=1000 不代表：

```text
safe-stop slice N 也够
```

如果 critical slice 只占 1%，自然采样里可能只有约 10 个案例。

因此常需要：

```text
representative sample
+
critical-slice oversampling / dedicated set
```

并分开解释总体 estimate 和诊断 estimate。

## 9. Repeats 也应按 Slice 分配吗？

可以，但要预先定义理由。

例如：

- 高随机 task：更多 repeats；
- deterministic verifier task：较少 repeats；
- expensive long-horizon task：较少 repeats，但更多不同 tasks。

这种 unequal repeats 可以合理，但 aggregation 必须避免让高-repeat task 获得意外更高权重。

推荐：

```text
先得到 per-task estimate
再按 task-level rule 聚合
```

## 10. Paired Experiment 下的 N / R

若 baseline / candidate 在同题运行：

```text
N tasks × R repeats × 2 conditions
```

主要 power 取决于：

```text
paired difference distribution
```

而不是两个独立 accuracy 的方差简单相加。

Pilot 应重点记录：

```text
wins
losses
discordant pair rate
per-task repeat flip rate
```

这比只看 baseline accuracy 更能指导版本比较样本设计。

## 11. Early Stopping / Sequential Peeking 的风险

如果每跑 20 题就看一次：

```text
显著了就停
不显著就继续
```

而没有预先定义 sequential protocol，会增加 false positive 风险。

同样：

```text
先跑 1 repeat
不满意再加 5 repeats
```

如果扩样规则由当前结果驱动，也会影响推断解释。

应预先冻结：

```text
N / R
或合法的 sequential stopping rule
```

## 12. Infrastructure Failure 不应偷偷减少 N

如果计划：

```text
N=200 tasks
```

结果 15 个 provider timeout 后只分析 185 个，并且这些 timeout 不是随机发生的，就可能产生 selection bias。

应报告：

```text
planned N
completed N
infra-aborted N
rerun policy
```

必要时按冻结协议补跑，而不是静默缩分母。

## 13. 一个实用预算分配流程

```text
1. Define estimand
2. Define independent unit
3. Identify critical slices
4. Pilot small N × small R
5. Estimate between-task / within-task variation
6. Set MDE / desired precision
7. Set minimum slice counts
8. Choose N and R under budget
9. Freeze stopping / rerun rule
10. Run paired if possible
```

## Common wrong answers

### 错误 1：总 runs 越多，样本量越大

不是。独立 unit 和 cluster structure 才决定信息量。

### 错误 2：每题多跑几次就能证明泛化

重复只增加同题稳定性信息，不增加新的 task diversity。

### 错误 3：永远优先更多 tasks，不需要 repeats

如果系统 stochasticity 很高，单次 run 可能噪声过大，也无法估计 reliability。

### 错误 4：每个 task 必须同样 repeat 数

不是绝对必要；但 unequal repeats 需要预先定义，并避免 aggregation weight drift。

### 错误 5：N 越大越好

预算有限时，过度追求微小 effect 的显著性可能挤压 critical slice、replay 和诊断成本。

## VeriAgent example

VeriAgent memory v3：

```text
12 distinct tasks
× 3 repeats
× 2 conditions
= 72 executions
```

3 repeats 帮助看同题稳定性，但 task coverage 仍只有 12。若下一阶段要支持更强的“对新 Olist-style tasks 泛化”结论，与其继续把每题从 3 次堆到 20 次，通常更应该增加不同 group / template / capability 的独立 tasks，同时保留足够 repeats 监控 stochasticity。

## Follow-up questions

- 如何从 pilot 估计 ICC / cluster effect？
- 二元 paired outcome 的 power 如何估？
- rare failure 的样本量怎样设计？
- unequal repeats 如何聚合？
- sequential testing 什么时候是合法的？

## Evidence of mastery

达到 S4 时，应能拿到一个固定 compute budget，解释为什么把预算分成某个 `N tasks × R repeats`，并明确：

```text
哪个在提高 coverage
哪个在估计 stochasticity
哪个 critical slice 有最低样本要求
MDE 是什么
停止规则是什么
```

## Related knowledge

- [Q02 Estimand & Unit](01_Estimand_and_Unit_of_Analysis.md)
- [Q25 Credible Improvement](02_Is_the_Improvement_Credible.md)
- [Q26 Paired Evaluation](03_Paired_Evaluation.md)
- [Q27 Bootstrap / Permutation / CI](04_Bootstrap_Permutation_and_Confidence_Intervals.md)
