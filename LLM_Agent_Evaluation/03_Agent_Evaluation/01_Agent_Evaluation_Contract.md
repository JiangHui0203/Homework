# Q12 为什么 Agent Eval 不能只看 final task success？

- Level: M1
- Mastery: S0
- Related Parts: Part 3 / Part 4 / Part 7
- Related Patterns: P06 Trajectory First-Failure Analysis, P07 Recovery-aware Evaluation, P09 Cost per Valid Success, P10 Replayable Evaluation
- Related Cases: VeriAgent ProofWriter / Olist Data Agent

## 30-second answer

因为 Agent 是一个**与环境多步交互的系统**，final success 只告诉你“最后成没成”，却不能告诉你：工具是否选对、参数是否正确、是否用了错误中间信息、是否发生 recovery、是否错误放行、为什么失败、成本是否失控，以及同样任务是否稳定。

最小完备的 Agent Eval 至少要覆盖：**Outcome、Trajectory/Process、Tool/Action、Reliability/Recovery、Efficiency/Stability**，并保留可回放 trace。

## 90-second answer

Agent 与一次文本生成的关键区别是：它有状态、有工具、有环境反馈、有多步决策，而且可能重试、回滚、停止或恢复。

所以评测对象应分层：

1. **Outcome**：任务最终是否正确完成，是否 partial / safe stop。
2. **Trajectory**：关键步骤是否合理，first meaningful failure 在哪里。
3. **Tool / Action**：工具选择、参数、grounding、执行结果使用是否正确。
4. **State / Memory**：状态是否污染、memory 是否真正命中并被使用。
5. **Recovery / Safety**：失败后是否恢复，证据不足时是否安全停止，是否 false accept。
6. **Efficiency / Stability**：token、calls、latency、重复运行稳定性。

final success 仍是核心 outcome metric，但不是充分诊断信号。

## Full reasoning

### 1. Agent 的评测对象是 interaction loop

最小 Agent 抽象：

```text
Task
→ State
→ Action / Tool call
→ Observation
→ State update
→ ...
→ Final outcome
```

因此同样 final answer 可能来自完全不同的 trajectory。

### 2. 只看 final success 会漏掉什么

#### A. False confidence

Agent 得到错误结果，但 runtime 没发现并直接交付。Final answer 可能格式正常，系统却不可靠。

#### B. Lucky success

中间推理/工具调用有错误，最后因为偶然抵消得到正确答案。只看 outcome 会把脆弱路径当成可靠能力。

#### C. Recoverable failure

第一次 tool call 错了，但 Agent 正确诊断并 recovery。最终 success 相同，但系统能力明显不同。

#### D. Safe stop

数据缺失时，“拒绝编造并说明缺口”可能是正确完成。如果 binary success 设计不好，会把安全行为误记为 failure。

#### E. Hidden cost

两个系统都是成功，一个调用 3 次工具，另一个循环 30 次。只看 success 无法支持部署决策。

#### F. Unstable success

一次成功不能说明稳定性。同题重复运行可能出现不同 plan、SQL 或 tool route。

### 3. 一个实用的最小 Agent Eval Stack

| Layer | 核心问题 | 示例指标 |
|---|---|---|
| Outcome | 最后完成了吗？ | task success, partial credit |
| Reliability | 错误有没有被放行？ | false accept, safe stop |
| Process | 为什么成/败？ | first-failure distribution |
| Tool | 工具行为对吗？ | tool selection / arg accuracy |
| Recovery | 出错后能回来吗？ | recovery success / cost |
| Efficiency | 值得吗？ | token/calls per valid success, P95 latency |
| Stability | 可重复吗？ | repeat consistency |

“最小完备”不是要求每次都塞十几个 KPI，而是不能让一个 final score 承担所有语义。

### 4. Outcome 与 process 的关系

过程指标不是为了替代 outcome，而是用于：

- 诊断 root cause；
- 区分 lucky success 与 robust success；
- 判断机制是否真的生效；
- 构造 regression tests；
- 定位数据/训练机会；
- 解释成本和 latency。

### 5. Agent Eval 的特殊 confounders

- environment 状态变化；
- tool/API 版本变化；
- external data drift；
- memory 跨任务污染；
- retry policy 改变；
- concurrency / timeout；
- 模型生成随机性；
- trace 丢失导致不可归因。

因此 Agent Eval 比静态文本 benchmark 更依赖 replay、snapshot 和 observability。

## Evaluation design

设计 Agent Eval 时，按顺序写：

```text
Task contract
→ Environment snapshot
→ Outcome states
→ Tool/action contracts
→ Trace schema
→ Recovery/safe-stop states
→ Metrics
→ Repeat/replay protocol
→ Failure taxonomy
→ Regression gates
```

## Common wrong answers

### 错误 1：只要 final answer 对，中间步骤错没关系

如果中间错误会在稍微不同的输入上导致失败，就说明路径脆弱；工程系统必须知道这种风险。

### 错误 2：trajectory metric 越多越好

不对。过程指标必须服务于诊断、归因或 gate；无决策用途的 telemetry 只是噪声。

### 错误 3：所有非成功都算同一种 failure

timeout、tool error、unsafe answer、safe stop、unrecovered planning failure 的含义完全不同。

## Counterexample / boundary

对于完全无工具、无状态、单次生成的简单 QA，final correctness 可能足以作为主要指标。但只要系统引入多步决策、外部环境、恢复或 memory，就需要更丰富的 evaluation object。

## VeriAgent example

VeriAgent 的设计天然适合作为 Agent Eval 案例：它把 generation、verification、control、observability 分开，并保留结构化 trace。

Olist challenge evaluation 不只报告最终正确数，还报告错误答案被 runtime 接受、SQL 执行失败、重复稳定性、model requests、token、每次正确完成成本和 latency。更关键的是，candidate memory 的 +1/36 会结合 trace 检查失败发生阶段，因此不会只凭 final score 宣称 memory 有效。

## Follow-up questions

- safe stop 算 success 还是 failure？
- recovery 后成功应和 first-pass success 等价吗？
- trajectory correctness 能否作为 primary metric？
- Agent 的 tool-call accuracy 如何定义 denominator？
- environment 无法完全 replay 时怎么办？

## Evidence of mastery

达到 S4 时，应能拿到一个 Agent 架构图，直接映射出：**评测对象、trace 事件、主要 metrics、failure slices、replay 需求和 regression gates**。

## Related knowledge

- [Agent Fundamentals for Eval](../00_Foundations/06_Agent_Fundamentals_for_Eval.md)
- [Q04 Metric Design](../01_LLM_Evaluation/03_Metric_Design.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
