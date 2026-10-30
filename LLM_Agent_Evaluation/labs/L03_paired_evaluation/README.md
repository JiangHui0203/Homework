# L03 — Paired Evaluation Lab

> 目标：把 Q25–Q29 从“知道统计概念”推进到“能判断一次小幅版本提升到底有没有足够证据”。

## Learning objective

完成本 Lab 后，你应该能：

1. 区分 `run count` 与真正的独立 `task count`；
2. 在同题版本比较中构造 paired task-level effect；
3. 报告 wins / losses / ties，而不是只看两个 accuracy；
4. 用 **task-level bootstrap** 给 effect 加 confidence interval；
5. 用 **task-level sign-flip permutation** 回答 null 下当前差异是否异常；
6. 解释为什么 CI 跨 0 不等于“证明等价”；
7. 区分 task diversity 与 repeat stability；
8. 识别多个 exploratory slice 中挑最好结果的 multiple-comparison / selection bias；
9. 写出一个克制的 evidence statement，而不是把 `+2.78pp` 自动写成“提升”。

## Prerequisites

先读：

- [Q02 Estimand & Unit of Analysis](../../06_Statistics_and_Experiment_Design/01_Estimand_and_Unit_of_Analysis.md)
- [Q25 Is the Improvement Credible?](../../06_Statistics_and_Experiment_Design/02_Is_the_Improvement_Credible.md)
- [Q26 Paired Evaluation](../../06_Statistics_and_Experiment_Design/03_Paired_Evaluation.md)
- [Q27 Bootstrap / Permutation / Confidence Intervals](../../06_Statistics_and_Experiment_Design/04_Bootstrap_Permutation_and_Confidence_Intervals.md)
- [Q28 Task Count & Repeats](../../06_Statistics_and_Experiment_Design/05_Task_Count_and_Repeats.md)
- [Q29 Multiple Comparisons & Adaptive Analysis](../../06_Statistics_and_Experiment_Design/06_Multiple_Comparisons_and_Adaptive_Analysis.md)

## Scenario

你正在比较 `baseline` 与 `candidate`。

冻结实验设计：

```text
12 distinct tasks
× 3 paired repeats per task
= 36 paired run rows
```

原始 run-level 结果看起来是：

```text
baseline   29/36
candidate  30/36
```

表面上：

```text
+1 correct run
= +2.78 percentage points
```

但你的 primary claim 不是：

> 在这 36 行日志上 candidate 更高。

而是：

> 对从同一目标任务总体抽到的未来 task，candidate 的平均成功概率是否比 baseline 更高？

因此 primary analysis unit 被冻结为：

```text
task_id
```

`repeat_id` 是 nested unit，用来观察同题随机性，不是新的独立 task。

## Files

```text
L03_paired_evaluation/
├── README.md
├── paired_runs.csv
├── experiment_contract.json
├── analyze.py
├── REPORT_TEMPLATE.md
└── SOLUTION.md
```

## Frozen experiment contract

`experiment_contract.json` 固定：

```text
Primary estimand:
  mean task-level success difference
  candidate - baseline

Primary unit:
  task_id

Nested unit:
  repeat_id

Pairing key:
  task_id + repeat_id

Bootstrap:
  resample task_id
  20,000 iterations
  seed = 20261030

Permutation:
  exact task-level sign flip
  two-sided

Confirmatory view:
  overall

Exploratory slices:
  lookup
  join
  time
  safe_stop

Minimum practical effect:
  +5.0 pp
```

不能看完数据后再把 `join` 改成 primary slice，也不能因为 p-value 不好看而换 analysis unit。

## Dataset schema

`paired_runs.csv` 每行是一对在相同 task / repeat 条件下的运行：

```text
task_id
slice
repeat_id
baseline_success
candidate_success
seed
```

其中：

```text
success ∈ {0,1}
```

## Your task

### Task 1 — 不跑脚本，先手算 raw movement

先回答：

```text
baseline run accuracy = ?
candidate run accuracy = ?
raw delta = ?
```

然后立刻写一句：

> 为什么这 36 个 paired rows 不能直接解释成 36 个独立 tasks？

### Task 2 — 聚合到 task level

对每个 task 先计算：

```text
baseline task success rate
candidate task success rate
D_i = candidate - baseline
```

然后数：

```text
task wins
task losses
task ties
```

重点回答：

> 同样的 `+2.78pp`，为什么 `3 wins / 2 losses / 7 ties` 比单独两个 accuracy 更有信息？

### Task 3 — Bootstrap CI

运行：

```bash
python analyze.py
```

脚本执行：

```text
task-level bootstrap
```

也就是每次重采样：

```text
task_id
```

并把这个 task 的 repeats 作为一个整体隐含保留下来。

你必须解释：

```text
20,000 bootstrap samples
≠ 20,000 new tasks
```

以及：

> 如果把 36 个 run rows 当成 36 个独立 task 来 bootstrap，错在哪里？

### Task 4 — Permutation test

脚本还会做：

```text
exact task-level sign-flip permutation
```

它回答的是：

> 在 paired difference 的零效应假设下，像当前这样或更极端的差异有多容易出现？

必须明确：

```text
permutation p-value
≠ probability that H0 is true
```

### Task 5 — CI 与 practical significance

冻结 minimum practical effect：

```text
+5.0 pp
```

回答：

1. point estimate 是否超过 +5pp？
2. CI 是否排除 0？
3. CI 是否足够窄到支持“至少 +5pp”的结论？
4. 如果 CI 跨 0，能不能写“两个系统等价”？

### Task 6 — Tasks vs Repeats

脚本会告诉你哪些 task 在 3 次 repeat 间不稳定。

你需要判断：

> 下一批额外预算更应该增加新 tasks，还是继续给现有 12 个 task 加 repeats？

没有唯一机械答案，但必须基于 primary estimand：

```text
future-task generalization
```

和当前 observed stochasticity 来解释。

### Task 7 — Multiple-comparison trap

数据有 4 个 slice：

```text
lookup
join
time
safe_stop
```

其中某个 slice 看起来提升很大。

但 contract 已经冻结：

```text
overall = confirmatory
4 slices = exploratory
```

你必须回答：

> 为什么跑完后挑出最高的 slice，再写“candidate 在该能力上显著提升”，属于 post-hoc selection？

正确处理应该是：

```text
exploratory finding
→ new hypothesis
→ fresh confirmatory evaluation
```

### Task 8 — 写最终 Evidence Statement

禁止只写：

```text
candidate +2.78pp, better
```

至少包含：

```text
primary unit
N distinct tasks
repeats
point estimate
wins / losses / ties
95% CI
permutation result
practical threshold
multiplicity status
interpretation boundary
```

## Deliverable

```bash
cp REPORT_TEMPLATE.md MY_REPORT.md
```

完成：

```text
MY_REPORT.md
```

## Evaluation rubric

| 能力 | 分值 |
|---|---:|
| estimand / unit 正确 | 15 |
| task-level paired aggregation | 15 |
| wins / losses / ties 解释 | 10 |
| bootstrap unit 正确 | 15 |
| permutation 含义正确 | 10 |
| task vs repeat 预算判断 | 10 |
| multiple-comparison 处理 | 10 |
| final evidence statement | 15 |

## S3 evidence

不看 `SOLUTION.md` 独立完成后，可视为 Q25–Q29 开始进入 S3：

- 不把 runs 当 independent tasks；
- 能从 paired data 得到 task-level effect；
- 会正确选 bootstrap / permutation unit；
- 能解释 CI、p-value 与 practical significance 的边界；
- 能判断新增 tasks 与 repeats 的信息价值；
- 不把 exploratory best slice 冒充 confirmatory result。

## Common mistakes

### 1. 直接写 `30/36 > 29/36，所以有提升`

这是 point estimate，不是完整 evidence。

### 2. `n=36`

对于本 Lab 的 primary future-task claim，独立 task 只有：

```text
n = 12
```

### 3. CI 跨 0，所以“证明没有差异”

错。只能说当前数据没有把 effect 精确到排除 0；不等于证明等价。

### 4. p 很大，所以 H0 有很高概率是真的

频率学派 permutation p-value 不是 `P(H0 | data)`。

### 5. join slice +22pp，所以 candidate 改善了 join 能力

这个 slice 是看结果后从 4 个 exploratory slices 中观察到的。它是下一轮 hypothesis，不是本轮 confirmatory claim。

### 6. 多跑 repeats 就等于样本量增加

它增加 run observations 与 within-task reliability information，但没有等比例增加 task diversity。

## VeriAgent lens

这个 Lab 故意采用和 VeriAgent 很相似的证据形状：

```text
12 tasks × 3 repeats
29/36 → 30/36
```

但它是**合成教学数据**，不是 VeriAgent 历史产物。

真正应形成的条件反射是：

```text
raw run delta
→ task-level paired movement
→ uncertainty
→ repeat stability
→ slice / multiplicity
→ causal boundary
```

即使统计 evidence 看起来更强，也不能绕过机制作用阶段等因果证据。
