# Q16 Long-horizon Agent 为什么需要过程指标、阶段性检查点和预算指标？

- Level: M2
- Mastery: S0
- Related Parts: Part 3 / Part 4 / Part 7
- Related Patterns: P04 Slice Before Aggregate; P06 Trajectory First-Failure Analysis; P07 Recovery-aware Evaluation; P09 Cost per Valid Success; P10 Replayable Evaluation
- Related Metrics: Checkpoint Completion Rate, Conditional Stage Success, Loop / Stall Rate, Budget Violation Rate, Post-failure Waste
- Related Case: VeriAgent as a short-horizon boundary case

## 30-second answer

Long-horizon Agent 的难点不是“步骤多”，而是**错误会累积、状态会漂移、失败可能很晚才暴露、成本可能在已经无望的轨迹上继续增长**。所以 final task success 仍然要保留，但必须配合阶段性 checkpoint、first-failure、budget、loop/stall、recovery 和 partial-progress 指标。

关键是不要给每一步都打一个主观“推理分”。更实用的是围绕任务语义定义少量 milestone / invariant：关键状态是否达到、必要证据是否已获得、不可逆操作前前置条件是否满足。这样才能回答“系统在哪一段开始失控”和“成功率提升是否靠更高预算硬堆出来”。

## 90-second answer

我会把 long-horizon episode 看成一个有阶段结构的过程：

```text
Start
→ Milestone 1
→ Milestone 2
→ ...
→ Irreversible / high-risk action
→ Final outcome
```

每个 milestone 只检查真正影响后续可行性的任务状态，而不是逐 token 或逐 thought 打分。评测至少同时看：end-to-end success、各 checkpoint completion、条件阶段成功率、first meaningful failure、recovery、loop/stall、预算利用和超预算率。

长链的 denominator 也要特别小心：到达 Stage 4 的样本只是一部分，`Stage-4 success / all tasks` 和 `Stage-4 success / reached Stage 4` 回答不同问题。另一个常见错误是把平均步骤数下降当成效率提升；如果是因为系统更早失败，调用更少反而是坏事。

## Full reasoning

### 1. 什么叫 Long Horizon

Long horizon 不一定按固定“10 步以上”定义。更实用的是看系统是否具有：

- 多阶段依赖；
- 状态持续演化；
- 工具 / 环境交互；
- 中间决策影响后续可达状态；
- 延迟暴露的错误；
- recovery / rollback；
- 不可逆或高风险操作；
- 显著 token / call / time budget。

所以 horizon 可以用不同单位表达：

```text
model decisions
tool calls
state transitions
wall-clock time
milestones
external side effects
```

评测前应固定所用口径。

### 2. 为什么 Final Success 越来越不够

随着 horizon 增长，final failure 可能来自完全不同的链路：

```text
规划一开始就错
→ 中间执行错
→ 正确执行但观察误读
→ 状态在后半段漂移
→ 预算耗尽
→ 恢复策略进入循环
→ 最后一步才暴露之前的错误
```

如果只保存 final score，就无法判断是能力问题、控制问题还是预算问题。

### 3. Checkpoint 应该检查“任务状态”，不是“每一步想法”

好的 checkpoint 通常是：

- 必要事实已经验证；
- 所需资源已定位；
- 关键约束满足；
- environment 已进入目标中间状态；
- 不可逆操作的前置条件满足；
- 当前 plan 仍具可执行性。

不推荐把每条自然语言 thought 都做成主要 correctness label，因为：

- 很多不同推理路径都可能正确；
- 标注成本高；
- Judge noise 会累积；
- 容易把“像标准答案”误当“能完成任务”。

因此优先：

```text
state / evidence checkpoint
> free-form thought grading
```

### 4. Milestone Completion 与 Conditional Stage Success

假设任务有四阶段：

```text
S1 discover
S2 verify
S3 execute
S4 finalize
```

可以报告：

```text
Checkpoint Completion Rate at S_k
= reached valid S_k / all eligible episodes
```

还可以报告：

```text
Conditional Stage Success
= valid transition S_k -> S_{k+1}
  / episodes that validly reached S_k
```

二者不能混用。

前者告诉你“整体有多少任务活到这里”；后者告诉你“已经走到这里之后，这一段有多可靠”。

### 5. Exposure / Denominator Problem

Long-horizon eval 特别容易出现 survivorship bias。

例如：

```text
Stage 4 成功 9/10
```

看起来很好，但如果总共 100 个任务只有 10 个到达 Stage 4，那么这个数字并不能说明系统整体可靠。

因此阶段指标至少配对展示：

```text
reached stage / all tasks
success at stage / reached stage
```

### 6. First Meaningful Failure

长链里 final error 常常只是 symptom。

建议保留：

```text
first meaningful failure stage
first failure type
whether detected
whether recovered
final outcome
```

这样才能判断：

```text
早期 planning failure
vs
后期 execution failure
vs
recovery failure
```

深入 root cause 与 credit assignment 归 Part 4，但 Part 3 必须先把这些事件 trace 出来。

### 7. Loop / Stall

长链 Agent 常见一种特殊失败：系统没有明确报错，但不再产生有效进展。

典型表现：

- 重复相同 search；
- 反复调用同一 tool；
- plan 改写但 state 不变；
- 在两个状态之间震荡；
- 不断验证已经验证过的事实；
- token 增长但 milestone 不前进。

因此可以定义：

```text
Loop / Stall Rate
```

但必须先有 operational definition，例如：

```text
连续 N 个关键 action 没有新增 evidence、state transition 或 milestone progress
```

具体 N 是 protocol 参数，不应写进稳定 metric 定义。

### 8. Budget 是能力的一部分，不只是成本报表

Long-horizon system 通常需要多维预算：

```text
tokens
model calls
tool calls
wall-clock latency
retries
external actions
money
```

推荐报告：

- total cost；
- cost per valid success；
- P50 / P95；
- Budget Violation Rate；
- success under fixed budget；
- cost by stage；
- recovery cost。

如果候选方法成功率从 60% 到 65%，但平均预算翻倍，不能只报成功率提升。

### 9. Post-failure Waste

这是长链很有价值的诊断指标。

如果 first meaningful failure 已经发生并且事实上不可恢复，系统却继续消耗大量资源，可以定义：

```text
Post-failure Waste
= first unrecoverable failure 之后的 token / calls / time
```

它需要可靠的 failure annotation，因此更适合作为诊断 metric，而不是所有系统都直接拿来做 release gate。

### 10. Partial Progress

长任务可能有真实的 partial value，但 partial credit 必须来自任务合同，而不是“走了很多步所以给点分”。

好的 partial credit 对应：

- 已完成独立可验证子目标；
- 已产生用户可用 artifact；
- 完成了不可丢失的环境状态；
- 明确减少后续剩余工作。

坏的 partial credit：

```text
写了很多 reasoning
调用了很多工具
花了很多 token
```

过程长度本身不是进展。

### 11. 不要把 Step Accuracy 相乘当 End-to-End Success

一个常见直觉：

```text
每步 95% 正确
10 步 ≈ 0.95^10
```

这个近似只有在非常强的独立、同质假设下才成立。真实 Agent：

- 步骤难度不同；
- 错误相关；
- 有 recovery；
- 有可跳过步骤；
- 某些错误不影响最终结果；
- 某些关键步骤单点失效。

所以更应直接测 episode outcome + stage transitions，而不是用简单乘法代替真实评测。

## Recommended metrics

### End-to-End Task Success

仍然是核心 outcome，不应被过程指标替代。

### Checkpoint Completion Rate

衡量从起点到达某个有效 milestone 的比例。

### Conditional Stage Success

定位具体阶段的条件可靠性。

### First-Failure Distribution

按 stage / failure type 统计第一次有意义的失败。

### Loop / Stall Rate

衡量“没有报错但失去进展”的运行。

### Budget Violation Rate

```text
超过冻结预算的 episodes / eligible episodes
```

### Success under Fixed Budget

比较不同系统时非常重要，避免“多花无限计算换一点成功”。

### Post-failure Waste

用于发现失败后仍持续消耗的控制问题。

## Evaluation design

一个实用的 long-horizon protocol：

```text
1. 定义最终 task contract
2. 定义 3–7 个 task-semantic milestones
3. 为每个 milestone 定义 deterministic / rubric evidence
4. 冻结预算
5. 记录完整 action/state trace
6. 标记 first meaningful failure
7. 标记 recovery / rollback
8. 计算 end-to-end + stage + budget metrics
9. 按 horizon / task family / failure stage 切片
10. 对高风险不可逆 action 单独设 gate
```

Milestone 数量不应机械追求越多越好；只保留能支持诊断或决策的节点。

## Common wrong answers

### 错误 1：过程越长说明任务越难、Agent 越努力

可能只是 loop 或低效。

### 错误 2：步骤越少越高效

也可能是更早失败，导致后续调用根本没发生。

### 错误 3：每一步都让 LLM Judge 打分就能完整评价 long horizon

这会累积 evaluator noise，而且未必对应真实 state progress。

### 错误 4：最终失败都归到最后一步

最后一步往往只是暴露早期错误。

### 错误 5：预算只作为附加成本指标

对于 autonomy / long horizon，预算本身约束可部署能力。

## Counterexample / boundary

如果一个 Agent 只有固定两步、没有可持续状态、无 recovery、无外部副作用，复杂 checkpoint 体系可能是过度设计。这时 Q12/Q13 的 outcome + tool contract 往往足够。

## VeriAgent example

VeriAgent 当前 Olist challenge 并不是典型 long-horizon autonomous benchmark，因此不应把它包装成长链案例。但它已经展示了 long-horizon Eval 所需的基础习惯：

- 按 analysis、memory retrieval、SQL generation / execution、final scoring 等阶段保留 trace；
- 区分失败发生在 memory 可介入之前还是之后；
- 失败提前发生时，不把更少 requests 误判成效率提升；
- 报告完整任务 P50/P95、总 token、每次正确完成成本和重复稳定性；
- 不完整实验标为 `ABORTED`，不生成正式比较结论。

因此 VeriAgent 更适合作为“从短 horizon 走向长 horizon 前，observability 应该先具备什么”的边界案例。

## Follow-up questions

- checkpoint 太多会不会改变 Agent 行为？
- milestone 应该由 human、verifier 还是 Judge 标注？
- 如何评估不可逆 action 的风险？
- 不同 task 的 horizon 不同，能否直接平均 step count？
- success under fixed budget 与 cost per success 各回答什么问题？

## Evidence of mastery

达到 S3/M2 熟练度时，应能拿一个多阶段 Agent 任务设计：

- task-semantic milestones；
- exposure-aware denominators；
- first-failure event；
- loop/stall definition；
- recovery markers；
- fixed budget；
- end-to-end / checkpoint / cost 联合报告。

## Related knowledge

- [Q12 Agent Evaluation Contract](01_Agent_Evaluation_Contract.md)
- [Q13 Tool Use & Grounding](02_Tool_Use_and_Grounding_Evaluation.md)
- [Q14 Recovery & Graceful Degradation](03_Recovery_and_Graceful_Degradation.md)
- [Q15 State / Memory & Leakage](04_State_Memory_and_Leakage_Evaluation.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
- [Metrics Registry](../METRICS.md)
