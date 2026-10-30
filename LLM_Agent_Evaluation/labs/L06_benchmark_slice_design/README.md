# L06 — Benchmark Slice Design Lab

> 目标：把 Q21–Q24 从“知道 benchmark 怎么设计”推进到“能从候选 task pool 构造 representative + diagnostic 两套评测视图，并完成 split / leakage / weighting audit”。

## Learning objective

完成本 Lab 后，你应该能：

1. 从 target claim 反推 capability coverage；
2. 区分 representative set 与 diagnostic set；
3. 根据 natural frequency 设计总体估计视图；
4. 根据 capability / difficulty / risk 设计诊断视图；
5. 识别 row-level clean 但 group-level contaminated 的 leakage；
6. 排除 reference 未验证、缺乏区分度的 item；
7. 区分 group leakage 与 template overlap；
8. 明确 population-weighted 与 macro diagnostic 两种 aggregation 的 estimand；
9. 写出 benchmark interpretation boundary。

## Prerequisites

先读：

- [Q21 Discriminative Benchmark Design](../../05_Benchmark_and_Evaluation_Data/01_Discriminative_Benchmark_Design.md)
- [Q22 Leakage & Test-set Overfitting](../../05_Benchmark_and_Evaluation_Data/02_Leakage_and_Test_Set_Overfitting.md)
- [Q23 Frozen / Regression / Hard / Rotating Sets](../../05_Benchmark_and_Evaluation_Data/03_Frozen_Regression_Hard_and_Rotating_Sets.md)
- [Q24 Coverage / Difficulty / Distribution Trade-offs](../../05_Benchmark_and_Evaluation_Data/04_Coverage_Difficulty_and_Distribution_Tradeoffs.md)
- [Benchmarks Registry](../../BENCHMARKS.md)

## Scenario

你手上有 70 个候选 task。它们属于 5 个 capability：

```text
simple_lookup   natural frequency = 50%
join_fanout     natural frequency = 20%
time_scope      natural frequency = 15%
safe_stop       natural frequency = 10%
recovery        natural frequency = 5%
```

你需要从同一个候选池中构造两个**互相独立的评测视图**：

```text
Representative view
→ 主要回答：目标总体下平均表现怎样？

Diagnostic view
→ 主要回答：关键 capability / hard slice 哪里薄弱？
```

本 Lab 有意加入一些陷阱：

- `KNOWN_CLEAN` 行可能和已暴露 dev item 共享 `group_id`；
- 有些题 reference 未完成独立验证；
- 有些题虽然很难，但 plausible-wrong check 无法区分，因此并不适合作 discriminative item；
- historical pass rate 只能用于 instrument audit，不能变成“按候选版本结果挑题”的依据；
- template overlap 与 group leakage 的严重性不同。

## Files

```text
L06_benchmark_slice_design/
├── README.md
├── task_pool.csv
├── benchmark_contract.json
├── benchmark_plan_starter.json
├── validate_plan.py
├── analyze_plan.py
├── REPORT_TEMPLATE.md
└── SOLUTION.md
```

## Dataset schema

`task_pool.csv` 每行是一个候选 task：

```text
task_id
capability
difficulty
risk
natural_frequency
group_id
template_id
exposure_status
reference_verified
discriminative_check
historical_pass_rate
source
notes
```

### 三个最重要的审计字段

#### exposure_status

```text
KNOWN_CLEAN
DEVELOPMENT_EXPOSED
PUBLIC_CONTAMINATION_RISK
```

注意：

> `KNOWN_CLEAN` 只描述当前 row，不保证它所在 group 没被污染。

#### group_id

同一个 `group_id` 表示共享近重复来源 / solution skeleton / source entity 的任务组。

如果某个 group 已有 dev-exposed item，那么同组的“新表述”不能继续冒充 clean holdout。

#### discriminative_check

`1` 表示 correct reference 与预设 plausible-wrong behavior 在冻结数据上确实能被区分。

它说明：

```text
这个 item 能区分某种错误
```

不说明：

```text
真实模型一定会犯这种错误
```

## Frozen benchmark contract

`benchmark_contract.json` 已冻结。

### Representative view

目标大小：

```text
N = 12
```

目标 capability mix：

```text
simple_lookup   6
join_fanout     2
time_scope      2
safe_stop       1
recovery        1
```

这个 mix 是对自然频率的小样本近似。

最终报告使用：

```text
population_weighted
```

而不是把 12 题 raw micro accuracy 当作唯一生产估计。

### Diagnostic view

目标大小：

```text
N = 15
```

每个 capability：

```text
3 tasks
```

并要求：

- 每个 capability 至少覆盖 `medium`；
- 每个 capability 至少覆盖 `hard` 或 `adversarial`；
- 全集至少 8 个 `high / critical risk` item。

最终报告使用：

```text
macro_equal_capability
```

它是诊断分数，不是自然频率估计。

## Your task

### Task 1 — 先写 Benchmark Claim

不要先看 `SOLUTION.md`。

复制：

```bash
cp benchmark_plan_starter.json benchmark_plan.json
```

先填写：

```text
claim
target_population
unit_of_evaluation
representative.interpretation
diagnostic.interpretation
interpretation_boundary
```

先定义“这个 benchmark 能证明什么”，再选题。

### Task 2 — 做 Pool Eligibility Audit

阅读 `task_pool.csv`，回答：

1. 哪些 row 因直接 exposure 被阻止？
2. 哪些 row 自己写着 `KNOWN_CLEAN`，但其 `group_id` 已被 dev exposure 污染？
3. 哪些 row reference 未验证？
4. 哪些 row `discriminative_check=0`？
5. 通过全部硬条件后还剩多少 eligible items？

不要只过滤：

```text
exposure_status == KNOWN_CLEAN
```

这会漏掉 group-level leakage。

### Task 3 — 设计 Representative Set

在：

```text
representative.task_ids
```

填入 12 个 task ID。

要求：

- 近似自然 capability mix；
- 不违反 exposure / group / reference / discrimination contract；
- 不和 diagnostic set 共享 group；
- 能解释为什么它支持“target mix estimate”。

你需要明确：

```text
sampling distribution
≠ reporting weights
```

本 Lab 最终 population-weighted score 使用 contract 中冻结的 capability weights。

### Task 4 — 设计 Diagnostic Set

在：

```text
diagnostic.task_ids
```

填入 15 个 task ID。

要求：

```text
5 capabilities × 3 tasks
```

每个 capability 至少包含：

```text
medium
+
hard or adversarial
```

并保证高风险任务有足够覆盖。

不要把“最难的 15 题”直接叫 diagnostic benchmark；difficulty 只是一个维度。

### Task 5 — 校验 Plan 结构

```bash
python validate_plan.py benchmark_plan.json
```

通过只表示：

```text
benchmark plan structurally complete
```

不表示：

```text
sampling scientifically correct
holdout clean
coverage sufficient
```

### Task 6 — 运行 Benchmark Audit

```bash
python analyze_plan.py benchmark_plan.json
```

脚本会检查：

```text
pool eligibility
representative capability mix
total variation distance
population-weighted implied weights
diagnostic capability balance
difficulty coverage
risk coverage
direct exposure
group contamination
reference validity
discriminative validity
cross-set group overlap
template overlap warning
pilot ceiling / floor mix
```

### Task 7 — 做 Leakage Audit

必须回答下面几个问题：

1. 为什么 `LOOKUP02` 虽然是 `KNOWN_CLEAN`，仍不能进入 clean benchmark？
2. `group overlap` 为什么是 hard blocker？
3. `template overlap` 为什么在本 Lab 只是 warning，而不是自动判失败？
4. test 被用于 prompt / memory / rule 开发之后，exposure status 应怎样变化？
5. 为什么旧 test 可以转为 regression set，但不能继续假装 fresh holdout？

### Task 8 — 解释两个 Overall

假设未来在这两个 set 上跑出了成绩，你必须分别解释：

```text
Representative population-weighted score
```

与：

```text
Diagnostic macro-equal-capability score
```

为什么两个分数可能不同，甚至趋势相反？

正确回答应该落到：

```text
different sampling / weighting
→ different estimand
```

而不是“哪个算法更科学”。

### Task 9 — Pilot / Difficulty Audit

`historical_pass_rate` 是冻结历史 pilot 信息，只允许用于：

```text
ceiling / floor / discrimination audit
```

不能用于：

```text
根据当前 candidate 谁输谁赢来挑正式 test
```

否则 benchmark 本身就参与了 model selection。

## Deliverables

完成后留下：

```text
benchmark_plan.json
MY_REPORT.md
```

建议：

```bash
cp REPORT_TEMPLATE.md MY_REPORT.md
```

## Evaluation rubric

| 能力 | 分值 |
|---|---:|
| Claim / estimand 清楚 | 10 |
| Pool eligibility audit | 15 |
| Representative sampling | 15 |
| Diagnostic coverage | 15 |
| Group / exposure leakage audit | 20 |
| Weighting / aggregation 解释 | 10 |
| Difficulty / discrimination 边界 | 5 |
| Interpretation boundary | 10 |

## S3 evidence

不看 `SOLUTION.md` 能完成以下任务，可视为 Q21–Q24 开始进入 S3：

- 从 task pool 构造两种不同用途的 set；
- 不把 row-level clean 当成 group-level clean；
- 能解释 natural frequency 与 diagnostic balance 的冲突；
- 能写 population-weighted 与 macro diagnostic 两种 estimand；
- 能识别 reference / discrimination / leakage blocker；
- 能说明哪些分数可以外推、哪些只能诊断。

## Common mistakes

### 1. 只过滤 exposure_status

会漏掉：

```text
clean row
+ exposed sibling in same group
```

### 2. 每个 capability 一样多，所以 overall 就更公平

它更适合 diagnosis，不再代表 natural frequency。

### 3. 只选 hard / adversarial

如果所有系统都失败，会产生 floor effect，而不是高区分度。

### 4. historical_pass_rate 越低越值得进 test

历史 pass rate 只能辅助 instrument audit；按当前开发反馈不断挑“最能打候选”的题，会造成 adaptive overfitting。

### 5. template overlap = 一定 leakage

未必。template overlap 需要结合 split contract、source、group 与 expected solution 判断。本 Lab 将 group overlap 设为 blocker，template overlap设为 warning + 人工审计。

## VeriAgent lens

这个 Lab 直接对应 VeriAgent Olist challenge 的几个设计原则：

```text
family coverage
group-aware split
independent reference
plausible-wrong contrast
dev/test exposure control
diagnostic distribution != production distribution
```

但这里全部使用合成 task metadata，不是 VeriAgent 的真实题目，也不构成任何真实系统性能证据。
