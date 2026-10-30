# L07 — Reference Solution

> 先独立完成 Lab，再阅读本文件。

## 1. Frozen Experiment

```text
8 tasks
× 2 repeats
= 16 runs / variant
```

critical tasks：

```text
T03 missing_evidence
T06 permission_denied
```

两者的正确 terminal 都是：

```text
CORRECT_SAFE_STOP
```

recoverable faults：

```text
T04 transient_timeout
T05 stale_schema
```

## 2. Baseline

参考输出：

```text
Completed / Planned        16 / 16
Artifact Completeness      100%

Valid Successes            11 / 16
Success Rate               68.75%

Critical Invalid           0

Total Tokens               17,320
Tokens / Valid Success     1,574.55

P50 Latency                1,450 ms
P95 Latency                2,300 ms

Repeat Consistency         5 / 8 = 62.5%
Flaky Tasks                3

Budget Violations          0
Replay Match               100%
```

baseline 的不稳定 task：

```text
T02
T04
T07
```

## 3. Candidate

```text
Completed / Planned        16 / 16
Artifact Completeness      100%

Valid Successes            14 / 16
Success Rate               87.50%

Critical Invalid           0

Total Tokens               19,510
Tokens / Valid Success     1,393.57

P50 Latency                1,665 ms
P95 Latency                2,650 ms

Repeat Consistency         6 / 8 = 75.0%
Flaky Tasks                2

Budget Violations          0
Replay Match               100%
```

candidate 的不稳定 task：

```text
T05
T07
```

## 4. Quality Movement

```text
87.50% - 68.75%
= +18.75 pp
```

在这套 synthetic fixture 上，candidate quality 明显更高。

但这仍然只是：

```text
L07 frozen synthetic benchmark
```

不能外推为真实 Agent 或真实用户总体能力。

## 5. 为什么 Total Tokens ↑，但 Tokens / Valid Success ↓

candidate：

```text
total tokens:
19,510 > 17,320
```

但 candidate 成功更多，因此：

```text
19,510 / 14
= 1,393.57
```

反而低于 baseline：

```text
17,320 / 11
= 1,574.55
```

这说明：

```text
total resource use
```

和：

```text
resource efficiency per valid success
```

不是同一个问题。

## 6. Latency Trade-off

candidate：

```text
P50 1665 ms
P95 2650 ms
```

baseline：

```text
P50 1450 ms
P95 2300 ms
```

candidate 的 quality / unit-success cost / stability 更好，但 latency 更差。

这是典型 multi-objective trade-off。

## 7. Fault Review

### T03 missing evidence

正确行为：

```text
safe stop
```

两组都满足。

### T04 transient timeout

允许：

```text
retry <= 1
```

baseline 只有一个 repeat recovery 成功；candidate 两次都成功。

### T05 stale schema

允许：

```text
refresh + retry
```

candidate 一个 repeat recovery 成功、一个失败，因此形成 flaky task。

### T06 permission denied

这是 permanent fault。

正确行为：

```text
no retry
safe stop
```

两组都满足。

## 8. Validation

`validate_artifacts.py` 通过说明：

```text
manifest listed files exist
hash matches
trace count matches
completed count consistent
```

不说明：

```text
benchmark scientifically representative
system capability is good
root cause is correct
```

如果修改 manifest 已记录的 trace，应该出现：

```text
hash mismatch
```

## 9. Replay

两组：

```text
Replay Match Rate = 100%
```

因为本 Lab 把：

```text
task
fixture matrix
contract
simulator
```

都放在 deterministic envelope 内。

真实 hosted LLM 未必能做 exact replay，因为 provider backend / model snapshot / sampling / external state 可能变化。

## 10. Gate Result

冻结 gate：

```text
artifact completeness              PASS
critical invalid outcomes          PASS
success non-inferiority            PASS
repeat consistency                 PASS
tokens / valid success             PASS
P95 latency <= 2400ms              FAIL
budget violations                  PASS
replay match                       PASS
```

所以：

```text
NO-GO
```

`gate.py` 的 exit code：

```text
2
```

代表正式 NO-GO，不是程序异常。

## 11. 为什么不能用 Quality 覆盖 Latency Hard Gate

如果 deployment contract 预先规定：

```text
P95 <= 2400 ms
```

那么 candidate：

```text
P95 = 2650 ms
```

就违反 hard constraint。

不能结果出来后说：

> 但成功率高很多，所以把 latency gate 忽略。

这会让 gate 失去预注册意义。

可以做的是：

```text
优化 candidate latency
→ 新版本
→ 重新跑冻结 protocol
```

或者业务上正式修改 SLO，并 version gate policy；不能事后豁免本轮结果。

## 12. CI Placement

一个合理答案：

### PR hard

```text
artifact schema / hash
deterministic fixture replay
critical safe-stop fixture
forbidden action
```

### PR soft / small smoke

```text
repeat consistency
small cost / latency sample
```

### Scheduled / release

```text
larger latency measurement
fresh benchmark
stochastic capability confirmation
```

本 Lab 为教学目的把 P95 也直接做成 hard gate；真实系统中是否每 PR 都做 latency hard gate，要看 measurement noise 和环境稳定性。

## 13. Final Evidence Statement

一个合格版本：

> 在冻结的 8-task × 2-repeat synthetic L07 harness 上，baseline 与 candidate 均完成 16/16 runs，artifact validation 与 exact replay 均为 100%。Candidate 的 valid success 从 68.75% 提高到 87.50%，critical safe-stop failure 保持为 0，repeat consistency 从 62.5% 提高到 75.0%；虽然 total tokens 从 17,320 增至 19,510，但 tokens per valid success 从 1,574.55 降至 1,393.57。Candidate 的 P95 latency 从 2,300ms 上升到 2,650ms，超过冻结的 2,400ms hard gate，因此最终 release decision 为 NO-GO。该结果只验证这套 synthetic harness 的工程流程，不构成真实模型或真实生产性能证据。
