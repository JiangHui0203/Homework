# Q02 Estimand & Unit of Analysis：你到底在估计什么？

- Level: M1
- Mastery: S0
- Related Parts: Part 0 / Part 1 / Part 6
- Related Patterns: P03 Paired Same-Task Comparison, P04 Slice Before Aggregate
- Related Cases: VeriAgent repeated paired evaluation

## 30-second answer

**Estimand** 是你真正想估计的目标量；**unit of analysis** 是统计分析中承载独立比较或泛化的基本单位。两者必须匹配。

例如 12 道题每题跑 3 次得到 36 个 run。如果问题是“对新题目的平均成功率是否提高”，主要泛化单位通常仍是 **task**，36 个 run 不能简单当成 36 道独立题；重复运行主要帮助估计同一 task 下的随机性。把相关重复当独立样本会造成 pseudo-replication，置信区间过窄、显著性被夸大。

## 90-second answer

先分清四个概念：

- **Population**：想泛化到的总体，例如同一业务域中的未来分析问题。
- **Sample**：实际抽到的任务集合。
- **Estimand**：总体上希望估计的量，例如 candidate 相对 baseline 的平均 task-level success difference。
- **Unit of analysis**：用于估计与不确定性计算的基本单位，例如 task。

LLM/Agent Eval 经常有嵌套结构：

```text
Task
└── Repeat / Run
    └── Trajectory
        └── Step / Tool call
```

step 很多不等于样本很多；同一 task 的 3 次 repeat 也不等于 3 个独立 task。选择单位时要问：**结论最终想推广到什么层面？**

## Full reasoning

### 1. Estimand 先于统计方法

不要先问“该用 t-test 还是 bootstrap”，先问：

> 我想估计的到底是哪一个量？

常见 estimand：

1. **Task-level success rate**：随机抽一项目标任务，系统成功的概率。
2. **Paired treatment effect**：同一 task 上 candidate 相对 baseline 的平均变化。
3. **Run-level reliability**：固定任务条件下，随机重复运行成功的概率。
4. **User-level utility**：一个用户会话/工作流上的平均收益。
5. **Trajectory-level failure probability**：一条完整执行链出现某类 failure 的概率。

这些不是一回事。

### 2. 为什么 unit 选错会出问题

假设有 12 道题，每题运行 3 次：

```text
12 tasks × 3 repeats = 36 runs
```

如果 3 次运行共享同一道题、相同 schema、相似上下文，它们显然相关。直接把 `n=36` 当作 36 个独立任务，会让你误以为覆盖了更多任务多样性。

这种错误叫 **pseudo-replication（伪重复）**：观测数增加了，但真正独立的实验单位没有等比例增加。

### 3. Task 与 Run 回答不同问题

设第 `i` 个 task 的第 `r` 次运行结果为：

```text
Y_ir ∈ {0, 1}
```

对每个 task 可以先得到重复成功率：

```text
p_i = (1/R_i) * Σ_r Y_ir
```

再跨 task 聚合：

```text
Task-averaged success = (1/N) * Σ_i p_i
```

这样每个 task 的权重清楚可见。

如果你的目标就是评估“随机一次 run 的总体成功概率”，run-level estimand 也可以成立，但必须明确这意味着高重复 task 会获得更高权重，且不确定性计算要考虑 task 内相关性。

### 4. 常见单位及其适用问题

| Unit | 适合回答 | 常见风险 |
|---|---|---|
| Task | 对新任务是否更好 | task 数太少 |
| Run | 同一配置单次执行的可靠性 | 把重复当独立新任务 |
| User / Session | 用户体验是否提高 | session 长度差异、用户异质性 |
| Trajectory | 完整链路失败模式 | 一个 task 可有多个相关 trajectory |
| Step / Tool call | 局部行为质量 | 不能直接代表最终能力 |

### 5. Paired comparison 的单位

比较 baseline 与 candidate 时，如果它们运行在相同 task 上，可定义 task-level paired difference：

```text
D_i = score_i(candidate) - score_i(baseline)
```

然后分析 `D_i`。这样 task 难度被共享，通常比两组独立均值更有解释力。

如果每个 task 有多次重复，可以先在 task 内汇总，再比较 task-level difference；或者采用显式考虑层级结构的方法。关键不是某一种公式，而是**不要假装相关观测彼此独立**。

## Evaluation design

每次实验先填写：

```text
Population:
Sample:
Primary estimand:
Primary unit of analysis:
Repeated / nested units:
Pairing key:
Aggregation rule:
Uncertainty method:
```

## Common wrong answers

### 错误 1：样本量就是总 run 数

不一定。总 run 数描述执行量，不自动等于独立信息量。

### 错误 2：轨迹有 100 个 step，所以 n=100

step 是同一 trajectory 内的相关事件，不能用来证明对 100 个独立任务的泛化。

### 错误 3：只要 accuracy 一样，按 task 还是 run 聚合都无所谓

当不同 task 重复次数不一致、失败提前终止或某些 task 更不稳定时，两种 aggregation 会产生不同权重和不同结论。

## Counterexample / boundary

如果目标明确就是线上“每一次请求”的平均成功概率，run/request 可以是合理分析单位。但仍需考虑同一用户、同一任务模板、同一环境造成的聚类相关性。

## VeriAgent example

VeriAgent memory v3 有 12 道不同题，每题两种条件各重复 3 次，共 72 次任务执行。72 是 execution count，但若 claim 是“对不同问题的泛化”，不能把它当成 72 道独立题。重复运行的主要价值是观察同题稳定性与随机生成波动；task coverage 仍只有 12 道不同题。

这也是为什么报告同时保留“36/36 runs”与“三次均通过的不同题目 12/12”等不同层级统计。

## Follow-up questions

- 为什么 paired evaluation 通常更有力？
- task 之间难度差异很大时怎样加权？
- 用户级 A/B test 中为什么不能把每条消息都当独立样本？
- 有多层随机性时 bootstrap 应该在哪一层 resample？

## Evidence of mastery

达到 S4 时，看到任意 eval 表格都应先问：**这个 n 到底是什么？独立单位是什么？结论想泛化到哪里？**

## Related knowledge

- [Probability & Statistics for Eval](../00_Foundations/01_Probability_and_Statistics_for_Eval.md)
- [Experiment Design Basics](../00_Foundations/04_Experiment_Design_Basics.md)
- [Q01 Evaluation Contract](../01_LLM_Evaluation/01_Evaluation_Contract.md)
