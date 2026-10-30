# Q33 如何把 Offline Eval 变成 CI Regression Gate，同时避免 Flaky Eval 阻塞开发？

- Level: M1
- Mastery: S0
- Related Parts: Part 4 / Part 5 / Part 6 / Part 7
- Related Patterns: P05 Frozen Core + Rotating Hard Set; P10 Replayable Evaluation; P11 Holdout after Development
- Related Metrics: Fixture Regression Pass Rate, Flaky Case Rate, Gate Decision Stability
- Related Case: VeriAgent Data Agent

## 30-second answer

CI Eval 的目标不是“每个 PR 都跑完整 benchmark”，而是把不同证据按稳定性和风险分层：

```text
deterministic contract tests
→ stable regression fixtures
→ small paired smoke eval
→ larger stochastic / fresh eval
```

只有足够稳定、failure semantics 明确的检查才适合作 hard gate。对 stochastic eval，需要冻结 repeats、rerun policy、threshold 和 quarantine 规则，不能失败后一直 rerun 到通过。

核心原则：

> **Flaky 不是“可以忽略”，也不是“每次都 hard fail”；它需要单独管理。**

## 90-second answer

我会把 CI gate 分成至少三类：

1. **Deterministic hard gate**：schema、artifact completeness、reference、critical regression fixture，失败一次就阻塞。
2. **Statistical / stochastic gate**：小型 paired set，使用冻结重复次数和 non-inferiority / critical-slice rule；若证据落在灰区，可以进入一次预定义 recheck，而不是无限重试。
3. **Scheduled confirmation**：较大的 holdout / fresh benchmark，不必每个 PR 都跑，用于 release 或定期确认。

Flakiness 要先定位来源：

```text
model stochasticity
environment/tool drift
evaluator stochasticity
order/concurrency
harness bug
```

然后选择：提高 repeats、mock 依赖、修 harness、quarantine case、降低 gate 权限，或者把 case 从 hard gate 转为 diagnostic alert。

## Full reasoning

### 1. Offline Eval 和 CI 的目标不同

Offline research eval 更关心：

```text
完整分析
uncertainty
slice exploration
fresh evidence
```

CI 更关心：

```text
快速
稳定
高信号
能阻止明确 regression
```

所以不能简单：

```text
把完整 benchmark 塞进每个 PR
```

### 2. Gate 应按 Evidence Stability 分层

推荐：

```text
Tier 0: schema / syntax / unit contracts
Tier 1: deterministic regression fixtures
Tier 2: small stable paired eval
Tier 3: scheduled large benchmark
Tier 4: fresh / rotating confirmation
```

越靠前：

```text
更快
更 deterministic
更适合 hard fail
```

越靠后：

```text
更接近能力结论
更贵
更 stochastic
更适合 release / scheduled evidence
```

## 3. Hard Gate 适合什么

典型 hard gate：

```text
artifact hash invalid
planned runs missing
critical safety fixture failed
known deterministic bug reappeared
forbidden tool action occurred
schema contract broken
```

这些 failure 的语义清楚，而且重复执行不应随机改变。

## 4. Stochastic Gate 不应只看单次 Pass/Fail

例如：

```text
20 tasks × 1 run
```

candidate 比 baseline 少对 1 题。

如果系统本来有生成随机性，一次结果就 hard fail 容易产生高噪声。

可以采用冻结规则：

```text
paired tasks
fixed repeats
minimum acceptable delta
critical slice floor
uncertainty / grey zone
```

注意 CI pipeline 不一定每次都需要复杂显著性检验；关键是 gate contract 预先冻结且符合风险。

## 5. Flakiness 来源

### Model

相同 task / config 不同 sampling outcome。

### Environment / Tool

API timeout、数据漂移、权限、网络。

### Evaluator

LLM judge 自己 flip。

### Ordering / Concurrency

共享 state、rate limit、race condition。

### Harness

未清理 cache、非稳定 seed、路径依赖、时间依赖。

只有先分类，才能决定怎么治理。

## 6. Flaky Case Rate

可以按 task 定义：

```text
至少一次 pass 且至少一次 fail 的 task
---------------------------------
有重复观测的 eligible tasks
```

但这个 metric 只说明 observed instability，不自动说明根因是 model。

## 7. Rerun Policy 必须预先冻结

危险流程：

```text
CI fail
→ rerun
→ fail
→ rerun
→ pass
→ merge
```

这本质上是：

```text
optional stopping
+ cherry-picking
```

正确做法是提前规定：

```text
first result
grey-zone criterion
max rechecks
how to aggregate rechecks
terminal decision
```

例如：

```text
确定性 hard gate:
  no rerun to erase failure

stochastic grey zone:
  exactly one full paired recheck

infra abort:
  rerun allowed, but mark first attempt ABORTED
```

## 8. Quarantine 不是删除失败

如果一个 fixture 经常 flaky：

```text
quarantine
```

应该意味着：

```text
仍然运行
仍然记录
暂时不 hard block
有 owner
有原因
有退出条件
```

而不是把它从 suite 中静默删掉。

## 9. Critical Slice 可以比 Overall 更严格

例如总体成功率提高，但：

```text
permission safe-stop
critical action confirmation
```

退化。

release gate 可以定义：

```text
overall non-inferiority
AND
critical slice no regression
```

避免平均分掩盖高风险 failure。

## 10. Regression Gate 与 Fresh Holdout 分工

Regression set 本来就是 exposed：

```text
开发者知道它
系统会针对它修
```

所以它非常适合 CI：

```text
known bug must not return
```

但不适合证明：

```text
unseen generalization improved
```

fresh / rotating set 则承担后一类证据。

## 11. Gate Decision 本身也应该可审计

保存：

```text
gate policy version
input run IDs
metric values
thresholds
hard / soft rule
recheck status
final decision
```

否则只能看到红灯/绿灯，不知道为什么。

## Evaluation design

一个实用 pipeline：

```text
PR
↓
contract/unit tests
↓
deterministic regression fixtures
↓
small paired smoke
↓
gate decision
↓
merge
↓
scheduled larger eval
↓
release confirmation
```

同时有：

```text
flaky registry
quarantine owner
fresh benchmark
```

## Common wrong answers

### 错误 1：所有 eval 都应该 CI hard gate

昂贵/stochastic/fresh benchmark 不适合每 PR 强阻塞。

### 错误 2：失败多 rerun 几次，最终通过就算过

这会选择性保留好结果。

### 错误 3：flaky case 直接删掉

它可能正暴露真实的不稳定能力或环境问题。

### 错误 4：Regression set 已被开发看过，所以没价值

它不再是 clean holdout，但非常适合防已知 bug 复发。

### 错误 5：overall 没掉，所以 critical slice 可以忽略

高风险 slice 可以有独立 hard floor。

## Counterexample / boundary

如果系统完全 deterministic、fixture 极小且执行成本低，那么 CI 可以非常严格。但 hosted LLM / Agent 往往存在多层 stochasticity，需要把 deterministic contracts 与 stochastic capability evidence 分开治理。

## VeriAgent example

VeriAgent challenge eval 的若干规则很适合 CI 思维：构建题集时先做独立 reference 验证；API 错误会标 `ABORTED` 而不是把不完整结果当正式成绩；失败 review 与候选 memory 构建会绑定 run / plan / trace hash。这些机制都让“失败到底是实验不完整、已知 regression，还是系统能力问题”更容易区分。

当前 VeriAgent 并不等于已经建立完整 PR CI gate；这里借用的是可审计 artifact 和 failure-state 设计，而不是夸大现状。

## Follow-up questions

- 什么指标适合 PR gate，什么适合 release gate？
- stochastic gate 的 grey zone 怎么定义？
- infra failure 和 model failure 的 rerun policy 是否相同？
- quarantine case 什么时候应该恢复 hard gate？
- 为什么 regression set exposed 仍然有工程价值？

## Evidence of mastery

达到 S4 时，应能给一个 LLM/Agent repo 设计：

- gate tiers；
- hard vs soft rules；
- flaky taxonomy；
- frozen rerun policy；
- quarantine workflow；
- critical-slice floor；
- artifacted gate decision；
- fresh confirmation plan。

## Related knowledge

- [Q20 Failure Taxonomy as Engineering Asset](../04_Trajectory_and_Failure_Analysis/04_Failure_Taxonomy_as_Engineering_Asset.md)
- [Q23 Benchmark Set Roles](../05_Benchmark_and_Evaluation_Data/03_Frozen_Regression_Hard_and_Rotating_Sets.md)
- [Q25 Improvement Credibility](../06_Statistics_and_Experiment_Design/02_Is_the_Improvement_Credible.md)
- [Q29 Multiple Comparisons](../06_Statistics_and_Experiment_Design/06_Multiple_Comparisons_and_Adaptive_Analysis.md)
