# Q32 如何设计 Replay、Fixture、Mock 和 Fault Injection，使 Agent Failure 可以稳定复现？

- Level: M1
- Mastery: S0
- Related Parts: Part 3 / Part 4 / Part 7
- Related Patterns: P06 Trajectory First-Failure Analysis; P07 Recovery-aware Evaluation; P10 Replayable Evaluation
- Related Metrics: Replay Match Rate, Fixture Regression Pass Rate, Fault Injection Coverage
- Related Case: VeriAgent Data Agent

## 30-second answer

Replay、fixture、mock、fault injection 解决的不是同一个问题：

```text
Replay          重放一次已经发生的执行证据
Fixture         固定一个最小可复现 case
Mock            用可控替代物隔离外部依赖
Fault Injection 主动制造指定异常，测试 detection / recovery
```

可靠的 failure reproduction 应先冻结**可控边界**：task、state、tool response、seed、budget、controller 和 evaluator，然后明确哪些部分要求 exact match，哪些只能要求 semantic / contract match。

核心边界：

> **Replay 成功说明 failure 可复现，不自动证明 root cause。**

## 90-second answer

我通常把复现分成四层：

1. **Exact replay**：输入、fixture、seed、工具响应都冻结，期待关键 trace / outcome 一致。
2. **Contract replay**：真实 provider 可能不 deterministic，只要求关键 contract，例如同类 tool error、同一 final correctness。
3. **Fixture regression**：把已经确认的 failure 压缩成最小 task + state + expected result，长期放进 regression。
4. **Fault injection**：例如 timeout、malformed tool output、stale schema、permission denied，验证系统能否正确 detect、retry、safe stop 或 handoff。

Mock 的目标是控制变量，不是模拟真实世界全部复杂性。最终仍应保留少量真实 integration evaluation，避免“只在 mock 世界里可靠”。

## Full reasoning

### 1. 四个工具分别回答什么

### Replay

回答：

> 当时这条路径还能不能重新产生？

Replay 需要：

```text
recorded input
recorded state
system/config version
dependency behavior or snapshot
seed / ordering
```

### Fixture

回答：

> 这个已经确认的 bug，未来版本还会不会复发？

Fixture 应尽可能：

```text
minimal
stable
deterministic
high signal
low irrelevant context
```

### Mock

回答：

> 如果把外部不稳定依赖控制住，系统本身的逻辑是否正确？

常见 mock：

```text
tool API
database response
retriever output
clock
permission service
LLM subcomponent
```

### Fault Injection

回答：

> 面对指定异常，系统的 detection / recovery / stop policy 是否符合 contract？

例如：

```text
timeout
malformed JSON
stale schema
partial result
permission denied
contradictory evidence
rate limit
```

## 2. Replay 不等于“重新调用线上服务”

如果今天重新调用一个外部 LLM/API：

```text
same prompt
```

但 provider backend、model snapshot、tool data 已经变化，这不能叫强 exact replay。

更稳健的做法是区分：

```text
Recorded replay
→ 重放冻结 observation / tool outputs

Live replay
→ 重新访问真实依赖，测试当前 integration
```

两者目的不同。

## 3. Determinism Envelope

不是所有组件都能做到 exact deterministic。

需要明确：

```text
inside determinism envelope
outside determinism envelope
```

例如：

```text
inside:
  fixture input
  tool mock
  evaluator rule
  aggregation

outside:
  hosted LLM
  public web API
```

然后定义：

```text
exact equality
semantic equality
contract equality
```

不能拿 exact-byte mismatch 去误判本来就允许自然语言变化的结果。

## 4. Failure Fixture 应从证据支持的 Failure 来

典型 lifecycle：

```text
incident
→ trace review
→ first meaningful failure
→ replay / counterfactual
→ supported mechanism
→ minimal fixture
→ regression suite
```

不要看到一个最终 wrong answer 就直接冻结整条巨大 trajectory，结果以后无法知道 regression 在防什么。

## 5. Fixture 的最小字段

```text
fixture_id
source_failure_id
task/input
initial state
dependency responses
expected behavior
forbidden behavior
failure contract
evaluator
version
owner
```

如果是高风险 fixture，还应注明：

```text
severity
release gate role
```

## 6. Mock 的主要风险

Mock 很容易变成：

```text
系统按照 mock 的理想化行为工作
```

但真实 API 可能：

- 字段缺失；
- 顺序变化；
- latency 长尾；
- error body 不一致；
- retry 产生副作用；
- permission 语义复杂。

所以：

> mock 用于控制变量；integration eval 用于验证现实边界。

两者不能互相替代。

## 7. Fault Injection 必须先有 Fault Contract

错误方式：

```text
随机让工具报错
```

更好的做法：

```text
fault_id
injection point
precondition
fault type
expected detection
allowed recovery
forbidden action
retry budget
expected terminal state
```

例如：

```text
fault:
  permission_denied

expected:
  no retry
  safe stop or handoff

forbidden:
  invent success
  repeated external action
```

## 8. Recovery Eval 与 Fault Injection

Fault injection 特别适合 Q14：

```text
Opportunity
→ Detection
→ Recovery attempt
→ Recovered success / safe stop
→ Cost
```

注意 synthetic injection 只能说明：

> 在这个故障模型下系统表现怎样

不能直接把 injection frequency 当线上自然故障频率。

## 9. Replay Match Rate 也要定义单位

可以定义：

```text
replayed cases matching expected contract
-----------------------------------------
valid replay attempts
```

但必须说明 match 是：

```text
exact
semantic
contract-level
```

否则同名 metric 没有意义。

## 10. Side Effect Safety

对会产生真实副作用的 Agent：

```text
send email
delete resource
transfer money
publish content
```

Replay 默认不能重新执行真实 side effect。

应使用：

```text
dry run
sandbox
mock
recorded observation
idempotency key
```

否则“复现 failure”本身可能再次造成损害。

## 11. Replay 失败本身也是诊断信号

如果过去的 failure 再也复现不了，可能是：

```text
environment drift
hidden state
provider drift
race condition
missing artifact
flaky system
```

因此 replay failure 不是简单删掉 case，而是说明 reproducibility contract 不完整。

## Evaluation design

建立一个三层 suite：

```text
Layer 1 — deterministic fixtures
  每次 PR 都跑

Layer 2 — mocked fault injection
  验证 recovery / stop policy

Layer 3 — live integration replay
  定期跑，接受受控 stochasticity
```

每层明确：

```text
what is frozen
match criterion
budget
failure handling
gate role
```

## Common wrong answers

### 错误 1：只要失败重新出现，就证明 root cause 分析正确

复现说明现象稳定，不自动证明原因唯一。

### 错误 2：Mock 通过，所以真实 API 一定可靠

Mock 只验证了你建模进去的行为。

### 错误 3：Fault injection 越随机越真实

随机并不等于覆盖关键 failure contract。

### 错误 4：replay 必须全文完全一致

对 stochastic natural-language outputs，contract-level match 可能更合理。

### 错误 5：线上副作用任务直接 live replay

应先 sandbox / dry-run / recorded observation。

## Counterexample / boundary

如果某个 failure 完全来自不可控第三方短时 outage，可能无法做到 exact replay。但仍可以把：

```text
第三方 timeout
→ system expected behavior
```

冻结成 fault-injection fixture，测试自己的 recovery contract。

## VeriAgent example

VeriAgent 的 challenge failure memory 构建不是看到错误后直接“学”。它先绑定开发集 run、review plan 和轨迹哈希，再重放错误与正确 SQL，验证修正结果与冻结 reference 一致。这个 replay 支持“修正路径确实改变了结果”，但文档仍明确：不能单凭重放自动证明所有 root-cause 判断。

这正是：

```text
replay evidence
≠ automatic causal ground truth
```

## Follow-up questions

- Exact replay 与 contract replay 什么时候各自合适？
- 如何把一条长 trajectory 压缩成最小 regression fixture？
- Mock response 应该由人工写还是从真实 trace 录制？
- fault injection 如何覆盖 retry side effect？
- replay 不一致时如何定位是系统 drift 还是 artifact 缺失？

## Evidence of mastery

达到 S4 时，应能针对一个真实 Agent failure：

1. 定义 determinism envelope；
2. 选择 replay 方式；
3. 构造最小 fixture；
4. 设计 mock dependency；
5. 写 fault contract；
6. 定义 replay match criterion；
7. 说明哪些证据支持 reproduction、哪些不能证明 causality。

## Related knowledge

- [Q14 Recovery & Graceful Degradation](../03_Agent_Evaluation/03_Recovery_and_Graceful_Degradation.md)
- [Q17 First Meaningful Failure](../04_Trajectory_and_Failure_Analysis/01_First_Meaningful_Failure_and_Root_Cause.md)
- [Q20 Failure Taxonomy as Engineering Asset](../04_Trajectory_and_Failure_Analysis/04_Failure_Taxonomy_as_Engineering_Asset.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
