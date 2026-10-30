# L07 — Eval Harness Lab

> 目标：把 Q31–Q34 从“知道 Eval Engineering 应该做什么”推进到“能运行、审计、回放并 gate 一次最小 Evaluation System”。

## Learning objective

完成本 Lab 后，你应该能：

1. 区分 `runner` 与完整 eval harness；
2. 生成可审计的 `manifest + config snapshot + results + traces + summary`；
3. 用 SHA256 检查 artifact integrity；
4. 理解 `COMPLETED / INCOMPLETE / ABORTED` 为什么属于评测语义；
5. 对可控 simulator 做 exact replay；
6. 把 fault injection 写进 trace，而不是只在 README 声称测试过；
7. 计算 quality / cost / latency / stability scorecard；
8. 用冻结 release gate 做 `GO / NO-GO`；
9. 理解为什么更高 success 仍可能因为 deployment hard gate 而不能 release。

## Prerequisites

先读：

- [Q31 Reproducible Eval Harness](../../07_Eval_Engineering/02_Reproducible_Eval_Harness.md)
- [Q32 Replay / Fixture / Mock / Fault Injection](../../07_Eval_Engineering/03_Replay_Fixture_Mock_and_Fault_Injection.md)
- [Q33 CI Regression Gates & Flakiness](../../07_Eval_Engineering/04_CI_Regression_Gates_and_Flakiness.md)
- [Q34 Multidimensional Eval Reporting](../../07_Eval_Engineering/05_Multidimensional_Eval_Reporting.md)
- [Metrics Registry](../../METRICS.md)

## Scenario

这里不是调用真实 LLM，而是一个**纯离线 deterministic simulator**。

原因很简单：本 Lab 的教学目标是 Eval Harness 本身，而不是测某个模型能力。

冻结 benchmark 有：

```text
8 tasks
× 2 repeats
× 2 variants
```

任务覆盖：

```text
lookup
aggregate
safe_stop
recovery
join
synthesis
```

并固定注入：

```text
missing_evidence
transient_timeout
stale_schema
permission_denied
```

你会运行：

```text
baseline
candidate
```

然后比较两组 artifact。

## Files

```text
L07_eval_harness/
├── README.md
├── tasks.jsonl
├── harness_contract.json
├── harness_lib.py
├── run_harness.py
├── validate_artifacts.py
├── replay.py
├── gate.py
├── REPORT_TEMPLATE.md
├── SOLUTION.md
└── fixtures/
    └── scenario_matrix.csv
```

## Harness artifact contract

每个 run 会生成：

```text
run_dir/
├── manifest.json
├── config_snapshot.json
├── results.jsonl
├── summary.json
└── traces/
    ├── T01_r01.json
    ├── ...
    └── T08_r02.json
```

运行 validation / replay / gate 后还会生成：

```text
validation_report.json
replay_report.json
gate_report.json
```

## Frozen Gate

`harness_contract.json` 固定：

```text
artifact completeness              = 100%
critical invalid outcomes          = 0
candidate success delta            >= 0 pp
candidate repeat consistency       >= 0.75
candidate tokens / valid success   <= 1400
candidate P95 latency              <= 2400 ms
budget violations                  = 0
replay match rate                  = 100%
```

不要看完结果后修改 threshold。

## Your task

### Task 1 — 先读 Contract，不先看 SOLUTION

阅读：

```text
tasks.jsonl
harness_contract.json
fixtures/scenario_matrix.csv
```

回答：

1. 哪些 task 是 critical？
2. 哪些 fault 应 recovery？
3. 哪些 fault 应 safe stop？
4. primary run count 是多少？
5. 为什么 fault injection frequency 不能当生产故障频率？

### Task 2 — 跑 Baseline

```bash
python run_harness.py \
  --variant baseline \
  --out runs/baseline
```

不要只看终端 summary。

检查：

```text
runs/baseline/manifest.json
runs/baseline/config_snapshot.json
runs/baseline/results.jsonl
runs/baseline/traces/
```

回答：

> `summary.json` 为什么是 derived artifact，而不是唯一 evidence source？

### Task 3 — Artifact Validation

```bash
python validate_artifacts.py \
  --run-dir runs/baseline
```

它会检查：

```text
manifest listed artifacts exist
SHA256 matches
completed count consistent
trace count consistent
COMPLETED really means complete
```

然后故意做一次实验：复制一个 run_dir，修改其中一个 trace，再重新 validate，观察 hash mismatch。不要修改正式 `runs/baseline`。

### Task 4 — Exact Replay

```bash
python replay.py \
  --run-dir runs/baseline
```

本 Lab 的 deterministic envelope 是：

```text
tasks
fixture matrix
contract
simulator logic
```

因此要求：

```text
Replay Match Rate = 100%
```

必须回答：为什么这里能要求 exact replay，而 hosted LLM 通常未必能？

### Task 5 — 跑 Candidate

```bash
python run_harness.py \
  --variant candidate \
  --out runs/candidate

python validate_artifacts.py \
  --run-dir runs/candidate

python replay.py \
  --run-dir runs/candidate
```

手工比较：

```text
valid success
total tokens
tokens / valid success
P50 latency
P95 latency
repeat consistency
flaky task count
critical invalid outcomes
budget violations
```

### Task 6 — 看 Fault Traces

重点打开：

```text
T03
T04
T05
T06
```

观察：

```text
FAULT_INJECTED
RECOVERY_ATTEMPT
TOOL_EXECUTION
TERMINAL
```

然后回答：

- T04 timeout 为什么允许 retry？
- T06 permission denied 为什么不应该 retry？
- candidate 的 T05 为什么两个 repeat 不稳定？
- fault 被注入并不等于系统一定失败，为什么？

### Task 7 — Release Gate

先确保 candidate 已生成 `replay_report.json`，再运行：

```bash
python gate.py \
  --baseline-dir runs/baseline \
  --candidate-dir runs/candidate
```

注意：

```text
NO-GO 时 exit code = 2
```

这不是脚本崩溃，而是 release decision。

你必须解释：为什么 candidate quality 明显提高，仍然可能 NO-GO？

### Task 8 — 设计 CI Placement

把本 Lab 中的检查分到：

```text
PR hard gate
PR diagnostic / soft gate
scheduled release eval
```

至少判断：

```text
artifact validation
exact replay
critical safe-stop fixture
P95 latency
repeat consistency
fresh generalization
```

哪些应该每 PR 跑，哪些更适合 scheduled / release。

### Task 9 — 写 Final Scorecard

不要只写：

```text
candidate 14/16 > baseline 11/16
```

必须同时写：

```text
Quality
Critical reliability
Cost
Latency
Stability
Budget
Artifact completeness
Replay
Gate decision
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
| artifact / manifest 理解 | 15 |
| validation / hash integrity | 10 |
| replay / determinism boundary | 15 |
| fault injection / recovery contract | 15 |
| quality-cost-latency-stability scorecard | 20 |
| CI gate / flakiness 解释 | 15 |
| final release decision | 10 |

## S3 evidence

不看 `SOLUTION.md` 能独立完成以下任务，可视为 Q31–Q34 开始进入 S3：

- 能运行 harness 并找到所有关键 artifacts；
- 能验证 hash / completeness；
- 能解释 exact replay 的适用边界；
- 能从 fault trace 判断 recovery / safe stop；
- 能做多维 scorecard；
- 能接受“quality improved but release gate failed”；
- 能设计 PR gate vs release eval 的分层。

## Common mistakes

### 1. `summary.json` 有了，所以 harness 完整

不够。summary 必须能追溯到 raw result / trace / config。

### 2. Replay 100%，所以系统能力被证明

Replay 只说明在冻结 simulator contract 下可复现。

### 3. Candidate total tokens 更高，所以更低效

不一定。还要看 `tokens / valid success`。

### 4. Candidate success 更高，所以应该 GO

deployment hard constraint 可能仍失败。

### 5. Fault injection 的 25% timeout 就表示线上 timeout 率 25%

完全错误。这里是人为 coverage，不是 production frequency。

### 6. Gate NO-GO 用多跑几次改成 GO

本 Lab 是 deterministic；rerun 不能抹掉 gate failure。

## VeriAgent lens

L07 的目录结构不是复制 VeriAgent，但抽象了它已经具备的几个能力：

```text
frozen task/reference artifacts
manifest / hash
per-run trace
explicit ABORTED semantics
score report
token / latency / stability
failure replay
```

真正系统中 hosted model / database / external tools 会让 determinism envelope 更窄，因此需要更谨慎地区分 exact replay 与 contract replay。
