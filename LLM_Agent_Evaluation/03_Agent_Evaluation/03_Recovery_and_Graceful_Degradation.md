# Q14 如何评价 Recovery / Graceful Degradation，而不是把所有非成功都压成 Failure？

- Level: M1
- Mastery: S0
- Related Parts: Part 3 / Part 4 / Part 7
- Related Patterns: P06 Trajectory First-Failure Analysis; P07 Recovery-aware Evaluation; P09 Cost per Valid Success; P10 Replayable Evaluation
- Related Metrics: First-pass Success Rate, Recovery Opportunity Rate, Recovery Success Rate, Recovery Cost, Safe Stop Appropriateness
- Related Case: VeriAgent Data Agent

## 30-second answer

Recovery-aware evaluation 的关键不是“最终有没有成功”，而是先区分：**first-pass success、出现可恢复故障、尝试恢复、恢复成功、恢复失败、正确 safe stop、错误继续执行**。

`Recovery Success Rate` 的 denominator 应该是**真正存在 recovery opportunity 的运行**，而不是所有任务；同时必须报告 recovery 的额外 token / calls / latency，避免靠无限重试把最终成功率“刷高”。Graceful degradation 则要求系统在证据不足、工具不可用或约束无法满足时，能正确降级或安全停止，而不是编造结果。

## 90-second answer

我通常先定义一个 outcome state machine：

```text
FIRST_PASS_SUCCESS
RECOVERED_SUCCESS
CORRECT_SAFE_STOP
UNRECOVERED_FAILURE
UNSAFE_CONTINUE / FALSE_ACCEPT
INFRA_ABORT
```

然后再标注过程中的 recovery opportunity。一次工具参数错误、解析失败或临时执行错误可能是可恢复的；永久缺权限、缺关键数据或业务约束不可满足，则更适合 safe stop，而不是盲目 retry。

评测时至少分开看：first-pass success、recovery opportunity rate、attempt rate、conditional recovery success、recovery cost、safe-stop correctness 和最终 task success。最终成功仍重要，但 recovered success 不应该在诊断层和 first-pass success 完全混为一谈，因为它反映不同的可靠性与成本结构。

## Full reasoning

### 1. 为什么 binary success/failure 不够

下面三条轨迹 final outcome 都可能是“成功”：

```text
A. 一次完成
B. 第一次失败，正确诊断后一次恢复
C. 连续重试 12 次，最后偶然成功
```

如果只看最终成功率，它们完全相同；但部署风险、成本和稳定性完全不同。

反过来，两条“没有产出答案”的轨迹也可能完全不同：

```text
D. 数据缺失，系统正确说明无法回答
E. 数据充足，系统因为 planning failure 直接放弃
```

D 可能是正确行为，E 才是 failure。

### 2. 先定义 Recovery Opportunity

Recovery metric 最大的 denominator trap 是：什么算“有机会恢复”？

需要在 protocol 中预先定义可恢复事件，例如：

```text
invalid structured output
wrong but detectable tool arguments
tool execution rejection
transient tool timeout
recoverable schema mismatch
verification failure with actionable feedback
```

而以下事件未必应该进入 recovery denominator：

```text
provider-wide outage
permanent permission denial
required evidence genuinely absent
explicit policy forbids continuation
```

因此：

```text
Recovery Success Rate
= successful recoveries / valid recovery opportunities
```

而不是：

```text
successful recoveries / all tasks
```

### 3. Opportunity、Attempt、Success 必须分开

三个问题不同：

```text
机会存在吗？
系统识别并尝试了吗？
尝试后真正恢复了吗？
```

推荐至少保留：

- Recovery Opportunity Rate；
- Recovery Attempt Rate given Opportunity；
- Recovery Success Rate given Opportunity；
- Recovery Success Rate given Attempt。

这样能区分：

- 根本没发现错误；
- 发现了但不敢恢复；
- 尝试了但策略无效。

### 4. Recovered Success 与 First-pass Success

产品层面，两者可能都算 valid success；诊断层面必须分开。

```text
Task Success
= first-pass success + recovered success + contract-defined correct safe stop
```

但同时报告：

```text
First-pass Success Rate
Recovered Success Rate
```

否则一个系统可能靠大量 retry 掩盖首轮质量退化。

### 5. Recovery Cost 不能消失

恢复通常增加：

- tokens；
- tool calls；
- wall-clock latency；
- external API cost；
- risk exposure；
- state complexity。

因此应报告：

```text
Recovery Cost
= recovered path cost - comparable first-pass path baseline
```

实际工程里也常直接报告 recovery path 的额外 calls / tokens / latency。

重要原则：

> 最终成功不能让之前失败尝试的成本从分子里消失。

### 6. Graceful Degradation

Recovery 不是任何时候都继续尝试。

当系统发现：

```text
missing evidence
insufficient permission
unavailable critical tool
contradictory observations
uncertainty beyond allowed threshold
```

可能更正确的动作是：

```text
safe stop
partial result
request clarification
handoff to human
fallback to lower-risk mode
```

这就是 graceful degradation。

### 7. Safe Stop 也需要 precision / recall 思维

如果系统遇到任何困难都停止，它可能“很安全”但没用。

因此要同时关心：

```text
必要停止时是否停了？
本可继续时是否过度停止？
```

可以定义：

```text
Safe Stop Recall
= 正确触发 safe stop 的需要停止任务 / 所有应停止任务

Safe Stop Precision
= 正确 safe stop / 所有 safe stop
```

如果任务规模小，也可以直接报告 confusion table，而不是急着压成单个分数。

### 8. False Recovery

一个容易被忽视的失败类型：系统“看起来恢复了”，但实际上恢复到错误状态。

例如：

- tool call 第二次执行成功，但参数仍错误；
- verifier 不再报格式错，但语义仍错；
- fallback 返回了看似完整但无证据的答案。

因此：

```text
recovery mechanism executed
≠ recovered correctness
```

最终恢复是否成功必须回到 task / state contract 验证。

### 9. Retry Budget

Recovery protocol 必须冻结预算：

```text
max retries
max tool calls
max tokens
max latency
which failures are retryable
backoff / fallback policy
```

否则不同系统通过无限重试比较 final success，会失去可比性。

## 一个实用 Outcome State Machine

```text
START
  ├─ valid completion ─────────────> FIRST_PASS_SUCCESS
  ├─ recoverable failure
  │      ├─ no attempt ───────────> UNRECOVERED_FAILURE
  │      └─ recovery attempt
  │             ├─ valid completion -> RECOVERED_SUCCESS
  │             ├─ correct stop ────> CORRECT_SAFE_STOP
  │             └─ still wrong ─────> UNRECOVERED_FAILURE
  ├─ evidence genuinely insufficient -> CORRECT_SAFE_STOP
  ├─ wrong result accepted ─────────> FALSE_ACCEPT
  └─ infra outage ──────────────────> INFRA_ABORT
```

不同业务可以扩展，但这些状态不应全部压成 success/failure 两类后再丢掉过程信息。

## Recommended metrics

### First-pass Success Rate

回答“无需恢复即可完成”的基础可靠性。

### Recovery Opportunity Rate

告诉你系统多频繁进入异常路径；它不是越低越好，取决于任务难度，但可用于版本对比。

### Recovery Success Rate

必须写清 denominator 是 opportunity 还是 attempt。

### Recovery Cost

额外 calls / tokens / latency / money。

### Safe Stop Appropriateness

可按 precision / recall 或 task-family confusion table 报告。

### Unrecovered Failure Rate

保留第一失败类型与最终失败类型，避免只看末端 symptom。

## Evaluation design

### 正常任务 + Fault Injection

真实失败可能稀少，所以 recovery eval 通常需要两类数据：

```text
natural failures
controlled fault injection
```

例如固定注入：

- malformed tool output；
- timeout；
- stale schema；
- missing field；
- permission denied；
- contradictory result。

但必须明确 synthetic failure 只能证明对应 failure mode 下的恢复能力，不能直接代表线上自然频率。

### Paired comparison

比较两个 recovery controller 时，尽量让它们面对同一 task、同一 injected fault 和相同初始 state。

## Common wrong answers

### 错误 1：最终成功了，所以恢复机制有效

可能只是随机重试碰巧成功，必须看失败检测、恢复动作和正确性链路。

### 错误 2：Recovery Success = recovered tasks / all tasks

分母错误。它回答的是总体贡献，不是条件恢复能力。

### 错误 3：重试越多越鲁棒

重试可能提高表面成功率，同时放大成本、延迟和外部副作用。

### 错误 4：safe stop 都算 failure

在证据不足任务中，正确停止本身可能是正确完成。

### 错误 5：safe stop 都算 success

过度停止会逃避本可完成的任务，因此必须看 appropriateness。

## Counterexample / boundary

对于一次性、无外部工具且失败后没有可执行动作的静态问答，Recovery Eval 价值有限。但只要系统有 verifier feedback、工具重试、fallback、clarification、handoff 或 state rollback，Recovery 就应成为独立评测层。

## VeriAgent example

VeriAgent 已经体现两个重要边界。

第一，净收入类任务在必要数据缺失时由共同守卫正确停止；这类任务不能简单记成“没回答所以失败”，而应根据 task contract 判断 safe stop 是否正确。

第二，memory v3 报告中明确提醒：提前失败会减少后续 model requests，不能把“少调用了几次”自动解释成成本优化；失败路径的 token / latency 仍要进入总成本。JSON repair 等额外调用也属于真实运行成本，而不是从成功样本里隐藏。

这正对应：

```text
recovered / safe-stop outcome
+ recovery cost
+ first-pass quality
```

必须联合报告。

## Follow-up questions

- 什么时候 timeout 应该 retry，什么时候应该 safe stop？
- recovered success 在业务 KPI 中是否和 first-pass success 同权？
- 如何给 recovery 设置公平预算？
- fault injection 的频率能不能直接当线上 failure distribution？
- human handoff 是 recovery success 还是 partial success？

## Evidence of mastery

达到 S4 时，应能给一个带 retry / verifier / fallback 的 Agent 设计：

- recovery opportunity contract；
- outcome state machine；
- conditional denominators；
- retry budget；
- fault-injection suite；
- recovery cost；
- safe-stop appropriateness；
- release gates。

## Related knowledge

- [Q12 Agent Evaluation Contract](01_Agent_Evaluation_Contract.md)
- [Q13 Tool Use & Grounding](02_Tool_Use_and_Grounding_Evaluation.md)
- [Q04 Metric Design](../01_LLM_Evaluation/03_Metric_Design.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
- [Metrics Registry](../METRICS.md)
