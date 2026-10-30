# Q31 一个可复现的 Eval Harness 至少需要记录哪些 Artifact、Version、Trace 和 Configuration？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 3 / Part 5 / Part 6 / Part 7
- Related Patterns: P01 Eval Contract First; P10 Replayable Evaluation
- Related Metrics: Artifact Completeness, Artifact Integrity, Replay Match Rate
- Related Case: VeriAgent Data Agent

## 30-second answer

一个可复现的 Eval Harness 不是“把模型跑一遍的脚本”，而是把一次评测变成一个**可重建的证据包**。至少要冻结：task set / split、system config、model / prompt / controller version、environment / tool snapshot、state / memory snapshot、seed / decoding、ordered trace、raw evaluator output、metric config、最终 result，以及一个把这些 artifact 用 version / hash 串起来的 run manifest。

核心原则是：

> **同一份代码，不代表同一次 Evaluation。**

如果 task、prompt、memory、tool、evaluator、budget 或 aggregation 任何一个变化，score semantics 都可能变化。正式 run 还必须区分 `COMPLETED / ABORTED / INVALID`；不完整运行不能悄悄进入正式成绩。

## 90-second answer

我会把 harness artifact 分成六层：

```text
1. Input
   task / split / reference / benchmark manifest

2. System
   model / prompt / agent / memory / controller / decoding

3. Environment
   tool schema / data snapshot / dependency version / permissions

4. Execution
   run_id / task_id / repeat / seed / ordered trace / tool I/O

5. Evaluation
   evaluator version / rubric / raw judgment / derived label / metric contract

6. Provenance
   hashes / versions / timestamps / code revision / completeness status
```

然后用 `run_manifest.json` 把它们连起来。一个结果至少应该能回答：

```text
这个分数是哪套题？
哪版系统？
哪版 evaluator？
什么环境？
什么 budget？
哪些 run 完成了？
原始 evidence 在哪里？
能不能 replay？
```

没有这些信息，即使今天得到 83.2%，过两周也很难知道 82.9% 到底是系统退化、题集变化、grader 变化还是环境漂移。

## Full reasoning

### 1. Eval Harness 的职责不是“调用模型”

最小 harness 的职责更接近：

```text
Load frozen contract
→ materialize task + environment
→ execute system under test
→ record trace
→ evaluate raw result
→ aggregate metrics
→ validate completeness
→ freeze artifacts
→ make replay possible
```

因此：

```text
runner
≠ complete eval harness
```

只有执行，没有 artifact / validation / replay，仍然是一段实验脚本。

### 2. Run Identity 必须可重建

建议一个正式 run 的 identity 至少由这些部分决定：

```text
benchmark_version
system_version
model_version
prompt_version
controller_version
memory_snapshot
environment_snapshot
evaluator_version
metric_contract_version
budget_policy
seed / repeat policy
```

可以把它们写进：

```text
config_snapshot.json
```

并在 manifest 中记录 hash。

### 3. Input Artifact

至少保存：

```text
task_id
task version
split
group / slice metadata
reference / oracle version
benchmark manifest hash
```

对于 Agent benchmark 还要保存：

```text
initial state
tool availability
environment snapshot
permissions
```

不能只保存自然语言 prompt，因为最终行为可能依赖很多隐式状态。

### 4. System Artifact

至少记录：

```text
model/provider
model version or immutable identifier
prompt / system prompt hash
tool descriptions
controller / router policy
memory / state snapshot
decoding config
retry / recovery policy
token / time / call budget
```

如果 provider 模型只能用一个可变 alias，也应明确记录这个 limitation。

### 5. Execution Trace

推荐用结构化事件而不是一整块自由文本日志：

```text
event_id
timestamp / logical_order
task_id
run_id
step_id
event_type
input_ref
output_ref
status
latency
token usage
error type
state_before / state_after refs
```

关键不是字段越多越好，而是能够支持：

```text
replay
failure localization
cost accounting
state isolation audit
```

### 6. Evaluator Artifact

不要只保存最终：

```text
score = 1
```

还应保留：

```text
evaluator version
rubric / reference version
raw evaluator output
derived label
failure / abstain status
adjudication status
```

这样 evaluator 更新后才能区分：

```text
system changed
vs
grading changed
```

### 7. Summary 不是 Evidence Source

`summary.json` / dashboard 是派生 artifact。

它应该可以从：

```text
frozen raw results
+ frozen metric contract
```

重新计算。

如果 summary 是唯一保存的产物，就无法审计 denominator、failed runs 或 slice aggregation。

### 8. Manifest 与 Hash

典型 manifest：

```json
{
  "run_id": "...",
  "status": "COMPLETED",
  "benchmark_version": "...",
  "system_version": "...",
  "evaluator_version": "...",
  "artifacts": {
    "results.jsonl": "sha256:...",
    "config_snapshot.json": "sha256:...",
    "summary.json": "sha256:..."
  }
}
```

hash 不能证明“内容科学上正确”，但能证明：

```text
你现在看的 artifact
就是当时被冻结的 artifact
```

### 9. Completeness 是正式 metric 前置条件

如果计划：

```text
100 tasks × 2 conditions × 3 repeats
```

只完成 544 / 600 runs，不能直接把已有结果当完整正式实验而不说明。

至少有：

```text
planned
started
completed
aborted
invalid
missing
```

正式 protocol 应决定：

```text
什么时候 run status = ABORTED？
能否 resume？
不完整 run 是否允许做 descriptive partial analysis？
能否进入 release decision？
```

### 10. Version Everything That Changes Score Semantics

需要 version 的不只是模型：

```text
task set
reference
prompt
rubric
tool schema
memory
metric definition
aggregation
budget
fault profile
```

如果一个修改会改变：

> “这个 score 到底测的是什么”

就应该进入 version / manifest。

### 11. 最小 Directory Contract

一个很实用的最小结构：

```text
run_<id>/
├── manifest.json
├── config_snapshot.json
├── results.jsonl
├── summary.json
└── traces/
    ├── task001_r01.json
    └── ...
```

进一步可以保存：

```text
raw_model/
raw_tools/
evaluator/
replay_report.json
validation_report.json
```

## Evaluation design

设计 harness 时先画 artifact graph：

```text
task manifest
     ↓
config snapshot
     ↓
execution trace
     ↓
raw result
     ↓
evaluator output
     ↓
derived metric
     ↓
release decision
```

对每条边问：

```text
输入保存了吗？
version 保存了吗？
hash 保存了吗？
失败状态保存了吗？
可以重新计算吗？
```

## Common wrong answers

### 错误 1：Git commit 已经记录了代码，所以可复现

代码版本只是条件之一。数据、模型 alias、tool、memory、evaluator 和环境都可能变化。

### 错误 2：保存最终 CSV 就够了

CSV 可能没有 trace、config、reference version 和失败运行。

### 错误 3：日志越详细越可复现

大量不可结构化日志未必可用于 replay。关键是稳定 schema 和 artifact references。

### 错误 4：失败 run 不进结果文件

这样 denominator 和成本都会被污染。失败也是正式 evidence。

### 错误 5：只给模型设 seed 就完全 deterministic

外部 API、工具、环境、并发、provider backend 都可能仍然变化。

## Counterexample / boundary

非常简单的纯 deterministic unit test 不需要像 Agent eval 一样保存复杂 trajectory。但只要结论依赖外部 model/tool/state/evaluator，artifact contract 就应该扩展到能解释这些依赖。

## VeriAgent example

VeriAgent challenge evaluation 已体现一套接近正式 harness 的做法：题集和 reference 先冻结，manifest 记录题目/参考文件、数据库、指标合同等哈希；每次实验落在独立结果目录，保存逐题逐次 trace、score report、token、耗时和稳定性。API 中断会把运行标成 `ABORTED`，而不是用已经完成的部分偷偷生成正式结论。

这里最值得学习的不是具体目录名，而是：

```text
frozen inputs
+ structured execution evidence
+ version/hash
+ explicit completeness state
```

一起构成可审计实验。

## Follow-up questions

- provider 只给可变模型 alias 时怎样记录 reproducibility limitation？
- resume 一个 aborted run 时，旧 run_id 还是新 run_id？
- evaluator 更新后应该重算旧 result 还是创建新 experiment view？
- 哪些 trace 字段值得长期稳定，哪些只属于 debug telemetry？
- artifact hash 能证明什么、不能证明什么？

## Evidence of mastery

达到 S4 时，应能独立设计一个 eval run directory / manifest，使另一个人可以：

1. 知道测了什么；
2. 知道系统和 evaluator 是什么版本；
3. 检查 run 是否完整；
4. 追到任意 task 的 trace；
5. 验证 artifact 未变化；
6. 重新计算 summary；
7. 对可控部分执行 replay。

## Related knowledge

- [Q01 Evaluation Contract](../01_LLM_Evaluation/01_Evaluation_Contract.md)
- [Q15 State / Memory Isolation](../03_Agent_Evaluation/04_State_Memory_and_Leakage_Evaluation.md)
- [Q23 Benchmark Set Roles](../05_Benchmark_and_Evaluation_Data/03_Frozen_Regression_Hard_and_Rotating_Sets.md)
- [Q27 Bootstrap / Permutation / CI](../06_Statistics_and_Experiment_Design/04_Bootstrap_Permutation_and_Confidence_Intervals.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
