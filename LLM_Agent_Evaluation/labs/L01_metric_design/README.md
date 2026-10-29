# L01 — Metric Design Lab

> 目标：把 Q01–Q04 从“会解释”推进到“会定义、会计算、会审计”。完成本 Lab 后，你应该能把一个模糊 KPI 改写成可执行的 metric contract，并识别 denominator、failure handling 与 protocol completeness 的陷阱。

## Learning objective

你将完成一次小型但完整的 Agent Evaluation metric design：

1. 明确 evaluation claim 与 unit of analysis；
2. 区分 task success、accepted-output accuracy 与 false accept；
3. 为 safe stop、recovery、cost、latency 定义独立指标；
4. 明确 numerator / denominator / eligibility / aggregation；
5. 处理 system failure、invalid output、provider abort 与 missing value；
6. 比较 micro 与 macro / slice 结果；
7. 将 metric definition 与 release gate 分离；
8. 最终判断这轮实验是否能形成正式 release 结论。

## Prerequisites

先读：

- [Q01 Evaluation Contract](../../01_LLM_Evaluation/01_Evaluation_Contract.md)
- [Q02 Estimand & Unit of Analysis](../../06_Statistics_and_Experiment_Design/01_Estimand_and_Unit_of_Analysis.md)
- [Q03 What Are We Measuring](../../01_LLM_Evaluation/02_What_Are_We_Measuring.md)
- [Q04 Metric Design](../../01_LLM_Evaluation/03_Metric_Design.md)
- [Metrics Registry](../../METRICS.md)

## Scenario

你负责一个结构化数据 Agent 的候选版本评测。任务有三类：

```text
numeric   -> 应返回正确数值答案
data_gap  -> 证据不足时应安全停止
tool      -> 需要正确调用工具，失败时允许 recovery
```

团队安排了 24 个冻结任务。运行后发现：

- 一部分任务正确完成；
- 一部分错误答案被 runtime 接受；
- 一部分错误被 runtime 拒绝；
- 一部分经过 recovery 后成功；
- 一部分 recovery 失败；
- 两个任务由于 provider 级故障没有完成。

你必须决定这些运行如何进入不同 metric。

## Pre-registered protocol rule

本 Lab 已经冻结以下实验规则，不能看结果后再修改：

1. provider / infrastructure abort **不计为 Agent capability failure**；
2. 但任何计划任务若因 infrastructure abort 未完成，则本轮不能生成正式 release score；必须补跑后才能形成正式结论；
3. 在补跑前允许计算 **provisional diagnostics**，但报告必须明确标为 provisional；
4. Agent 自身产生的 wrong answer、invalid output、tool failure、recovery failure 都属于被评系统行为，不能从 capability denominator 中悄悄删除；
5. 失败运行产生的 token / latency 不能从系统成本中消失。

这组规则本身就是 evaluation contract 的一部分。

## Files

```text
L01_metric_design/
├── README.md
├── runs.csv
├── metric_contract_starter.json
├── validate_contract.py
├── analyze.py
├── REPORT_TEMPLATE.md
└── SOLUTION.md
```

## Dataset schema

`runs.csv` 每行对应一个计划运行：

- `run_id`：运行 ID；
- `task_id`：冻结任务 ID；
- `family`：numeric / data_gap / tool；
- `expected_behavior`：answer / safe_stop / tool_completion；
- `outcome`：本次运行最终结果；
- `correct`：相对于冻结 reference 是否正确，`1/0`；provider abort 时为空；
- `runtime_accept`：runtime 是否把最终结果作为有效完成接受，`1/0`；provider abort 时为空；
- `recovery_opportunity`：是否发生了需要 recovery 的局部失败；
- `tokens`：本次完整运行 token；
- `latency_ms`：端到端耗时；
- `infra_status`：`ok` 或 `provider_abort`；
- `error_type`：主要失败类型。

## Your task

### Task 1 — 先写 Evaluation Claim

不要先跑脚本。

先用 3–5 句话回答：

```text
我们到底想知道什么？
unit of analysis 是什么？
哪些事件属于 Agent failure？
哪些事件属于 experiment infrastructure failure？
```

### Task 2 — 设计 Metric Contract

复制：

```bash
cp metric_contract_starter.json metric_contract.json
```

至少定义以下指标：

```text
M01 Task Success Rate
M02 Accepted Output Accuracy
M03 False Accept Rate
M04 Safe Stop Success Rate
M05 Recovery Success Rate
M06 Tokens per Valid Success
M07 End-to-End P95 Latency
M08 Experiment Completeness
```

每个 metric 必须明确：

```text
question
unit
numerator
denominator
inclusion_rule
aggregation
failed_missing_handling
direction
interpretation_boundary
```

特别注意：

- `Task Success Rate` 和 `Accepted Output Accuracy` 分母不同；
- `False Accept Rate` 必须说明是“所有错误运行中的错误放行率”，还是“所有运行中的错误放行占比”；二者不能共用一个名字；
- `Tokens per Valid Success` 的分子必须包含失败运行成本；
- provider abort 不能既从 capability metric 中删除、又假装实验是完整的。

### Task 3 — 检查 Contract 完整性

```bash
python validate_contract.py metric_contract.json
```

这个脚本只检查**结构完整性**，不会判断你的 denominator 是否语义正确。

如果它通过，只能说明：

```text
contract structurally complete
≠ metric scientifically correct
```

### Task 4 — 手算关键指标

在看 `SOLUTION.md` 前，至少手算：

- evaluable runs；
- Task Success Rate；
- Accepted Output Accuracy；
- False Accept Rate；
- Safe Stop Success Rate；
- Recovery Success Rate；
- Tokens per Valid Success；
- P50 / P95 latency；
- numeric / data_gap / tool 三个 slice 的 success rate；
- macro family success。

### Task 5 — 再运行参考分析脚本

```bash
python analyze.py
```

脚本会打印 canonical Lab protocol 下的 provisional diagnostics。

你需要检查：

1. 你的定义和脚本哪里一致？
2. 哪里不一致？
3. 差异来自公式，还是 denominator / inclusion rule？

### Task 6 — 做 Denominator Audit

必须回答：

1. 为什么 `16/19` 不能叫 Task Success Rate？
2. 为什么 `3/6` 和 `3/22` 都可能是合法数字，但不能叫同一个 False Accept Rate？
3. 为什么把失败 run 的 token 删除会让系统看起来更便宜？
4. provider abort 为什么不应直接算 Agent failure，但也不能直接忽略？
5. `tool` slice 明显更差时，只报 overall success 有什么风险？

### Task 7 — 给出 Release Conclusion

假设正式 release gate 已预注册为：

```text
Experiment completeness      = 100%
Task Success Rate            >= 75%
False Accept Rate            = 0%
Safe Stop Success Rate       >= 90%
Recovery Success Rate        >= 70%
Tokens per Valid Success     <= 1800
End-to-End P95 Latency       <= 4500 ms
```

你的最终报告必须先判断：

```text
这轮实验是否有资格形成 official release decision？
```

然后才能讨论 provisional metric 是否过门槛。

## Deliverables

完成后至少留下：

```text
metric_contract.json
MY_REPORT.md
```

建议从 `REPORT_TEMPLATE.md` 复制。

## Evaluation rubric

总分 100：

| 能力 | 分值 | 判定 |
|---|---:|---|
| Evaluation claim / unit 清楚 | 10 | 不混淆 task、run、accepted output |
| Metric contract 完整 | 25 | 分子、分母、失败处理、边界齐全 |
| Denominator audit | 20 | 能解释 16/19、3/6、3/22 的差异 |
| Failure / missing handling | 15 | system failure 与 infra failure 分开 |
| Slice / aggregation | 10 | 不只看 overall；理解 macro vs micro |
| Cost / latency | 10 | 失败成本不消失；P95 定义清楚 |
| Release conclusion | 10 | protocol completeness 优先于漂亮分数 |

### S3 证据

如果你可以在不看 `SOLUTION.md` 的情况下：

- 独立写出完整 metric contract；
- 找出 denominator trap；
- 解释为什么实验不完整时不能发正式 release score；
- 用 90 秒复述设计逻辑；

则 Q01–Q04 已开始进入 `S3`。

## Common mistakes

### 1. 只算“有答案的 run”

这会让失败越多的系统越容易通过筛选。

### 2. 把 provider outage 当模型错误

这会污染 capability estimate。

### 3. provider outage 直接删除后继续发正式成绩

这又会制造 selection bias，并违反冻结 protocol。

### 4. False Accept 没写条件分母

`wrong accepted / all wrong` 与 `wrong accepted / all evaluable` 回答的是两个问题。

### 5. Cost 只统计成功样本

这会隐藏 failure / recovery 的真实资源消耗。

## Related CORE_QUESTIONS

- Q01 Evaluation Contract
- Q02 Estimand & Unit of Analysis
- Q03 What Are We Measuring
- Q04 Metric Design
- Q12 Agent Evaluation Contract

## VeriAgent lens

这个 Lab 的设计直接训练 VeriAgent 已经使用的几个原则：

```text
失败成本不能消失
safe stop 可以是正确完成
ABORTED 实验不能混进正式成绩
错误放行必须单独计量
aggregate 必须能回到 failure / task slice
```

但本 Lab 使用合成数据，不是 VeriAgent 的历史实验复刻，也不构成任何真实系统性能证据。
