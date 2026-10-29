# L05 — Agent Recovery Evaluation Lab

> 目标：把 Q14 的 recovery-aware evaluation 真正算一遍，并学会区分 recovery opportunity、attempt、success、safe stop、false recovery、retry budget 与 recovery cost。

## Learning objective

完成本 Lab 后，你应该能：

1. 定义哪些 failure 是 retryable、哪些必须 safe stop；
2. 正确选择 Recovery Success 的 denominator；
3. 区分 opportunity / attempt / recovered success；
4. 计算 safe-stop precision / recall；
5. 发现 false recovery 和 over-retry；
6. 计算 recovery 额外 token / latency；
7. 在 final success 看起来尚可时，仍能识别控制层可靠性问题；
8. 给出 `GO / NO-GO`。

## Prerequisites

- [Q14 Recovery & Graceful Degradation](../../03_Agent_Evaluation/03_Recovery_and_Graceful_Degradation.md)
- [Q12 Agent Evaluation Contract](../../03_Agent_Evaluation/01_Agent_Evaluation_Contract.md)
- [Q17 First Meaningful Failure](../../04_Trajectory_and_Failure_Analysis/01_First_Meaningful_Failure_and_Root_Cause.md)
- [Metrics Registry](../../METRICS.md)

## Scenario

冻结数据包含 24 个 episode：

```text
8  first-pass success
9  recovery opportunities
7  faults that should safe stop
```

其中故意包含：正确 recovery、recovery opportunity 但没尝试、尝试后仍失败、false recovery、超 retry budget 后偶然成功、应 safe stop 却继续重试、应 recover 却错误 safe stop、unsafe continue，以及正确 safe stop。

## Files

```text
L05_agent_recovery_evaluation/
├── README.md
├── recovery_episodes.csv
├── recovery_policy.json
├── analyze.py
├── REPORT_TEMPLATE.md
└── SOLUTION.md
```

## Frozen recovery policy

`recovery_policy.json` 已冻结：

```text
max recovery attempts = 2
retryable faults = transient / malformed / stale schema / detectable arg / verifier feedback
must-safe-stop faults = missing evidence / permanent permission / policy forbidden / critical tool unavailable / contradictory evidence
```

不能看完结果后再修改这些规则。

## Your task

### Task 1 — 先手算 denominator

不要先跑脚本。回答：

```text
all episodes = ?
recovery opportunities = ?
attempted recovery among opportunities = ?
recovered successes = ?
must-safe-stop episodes = ?
all observed safe stops = ?
```

### Task 2 — 计算 Recovery 指标

至少手算：

```text
Final Valid Success Rate
First-pass Success Rate
Recovery Opportunity Rate
Recovery Attempt Rate | Opportunity
Recovery Success | Opportunity
Recovery Success | Attempt
Safe-stop Precision
Safe-stop Recall
Tokens per Valid Success
```

### Task 3 — 找 control-policy violations

逐条检查：该 recover 时是否 attempt？retry 次数是否超预算？该 safe stop 时是否仍 retry？

### Task 4 — 识别 False Recovery

必须回答：为什么“第二次调用成功返回”不等于 recovered success？最终正确性必须回到 task contract 验证。

### Task 5 — 计算 Recovery Cost

对于最终 `RECOVERED_SUCCESS`：

```text
extra_tokens  = tokens_total - tokens_before_fault
extra_latency = latency_ms - latency_before_fault_ms
```

计算平均额外成本。

### Task 6 — 跑参考脚本

```bash
python analyze.py
```

### Task 7 — Release Decision

冻结 gates：

```text
Final valid success                  >= 80%
Recovery success | opportunity       >= 80%
Safe-stop precision                  >= 90%
Safe-stop recall                     >= 90%
Control-policy violations            = 0
False recovery                       = 0
Tokens / valid success               <= 1800
```

必须说明：哪些 gate 是 quality/reliability hard gate？哪些只是 efficiency gate？为什么成本 PASS 不能抵消 recovery reliability FAIL？

## Deliverables

```text
MY_REPORT.md
```

建议：

```bash
cp REPORT_TEMPLATE.md MY_REPORT.md
```

## Evaluation rubric

| 能力 | 分值 |
|---|---:|
| opportunity / attempt / success denominator | 25 |
| safe stop precision / recall | 15 |
| false recovery diagnosis | 15 |
| retry budget / policy audit | 15 |
| recovery cost | 10 |
| final gate decision | 10 |
| interpretation boundary | 10 |

## S3 evidence

独立完成后，应能给任何带 verifier/retry/fallback/handoff 的 Agent 写出：recovery opportunity contract、retry budget、safe-stop policy、conditional metrics、cost metrics 与 release gates。

## VeriAgent lens

VeriAgent 已体现本 Lab 的几个原则：正确 safe stop 可以是 valid success；JSON repair/retry 的额外调用属于真实成本；提前失败导致更少 calls 不自动等于“更高效”；recovery/stop 必须结合 task contract，而不是只看有没有最终答案。

本 Lab 数据仍为合成教学数据。
