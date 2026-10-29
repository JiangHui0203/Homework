# Q15 有 Memory / State 的 Agent 应如何避免状态泄漏、历史污染和非独立测试？

- Level: M1
- Mastery: S0
- Related Parts: Part 3 / Part 6 / Part 7
- Related Patterns: P03 Paired Same-Task Comparison; P10 Replayable Evaluation; P11 Holdout after Development; P12 Mechanism ≠ Outcome
- Related Metrics: State Isolation Violation Rate, Memory Retrieval Coverage, Memory Net Benefit, Stale Memory Hit Rate
- Related Case: VeriAgent Experience Memory / Challenge Evaluation

## 30-second answer

有 memory / state 的 Agent，评测的第一前提不是“多跑几次”，而是**保证每个实验条件从可比、可追溯的初始状态开始**。必须冻结并记录：模型与 prompt、environment snapshot、memory snapshot、cache / tool state、读写策略、运行顺序和 test-set writeback policy。

最危险的污染包括：**跨任务状态泄漏、dev→test 之外的 test→memory 回写、paired 条件初始状态不同、重复运行之间共享历史、旧 memory 与新 contract 不兼容**。同时，memory 被检索到只证明机制被调用，不证明它导致了结果提升；要用 trace 确认 retrieval → injection → affected stage → outcome 的因果路径。

## 90-second answer

我会把 stateful Agent 的实验对象拆成四层状态：

```text
Model / prompt state
Environment state
Agent memory / working state
External cache / tool state
```

每次正式评测前，都要决定哪些状态应该 reset、哪些应该 snapshot/fork、哪些允许在 episode 内演化、哪些严禁跨 test episode 写回。比较 memory-on / memory-off 时，两组必须共享相同 task、environment 和初始 state，只在目标 memory 条件上不同。

评测还要保存 memory snapshot ID、source provenance、retrieval event、实际注入内容或 hash、作用阶段和 write events。否则一旦分数变化，你无法判断是 memory 真有帮助，还是 run order、旧状态、测试污染或随机性造成的。尤其要记住：`memory retrieved ≠ memory used ≠ behavior changed ≠ outcome improved`。

## Full reasoning

### 1. Stateful Agent 为什么破坏“独立样本”的直觉

普通静态 benchmark 常近似认为：

```text
task_i run
不改变
task_j run
```

但有 memory / state 后，运行 i 可能改变运行 j 的输入分布：

```text
Run i
→ write memory / cache / environment
→ Run j reads changed state
```

因此同一批 task 的顺序、重复次数和写回政策都会影响结果。

如果不冻结这些条件，所谓“重复评测”可能其实是在测一个持续学习 / 持续污染的系统。

### 2. 至少区分四类 State

#### A. Model / Prompt State

- system prompt；
- controller config；
- tool definitions；
- context window；
- model version / decoding config。

#### B. Environment State

- database snapshot；
- files；
- user/account state；
- permissions；
- external service state；
- simulated world state。

#### C. Agent Memory / Internal State

- long-term memory；
- experience rules；
- scratchpad / working memory；
- episodic summaries；
- planner state；
- state-machine checkpoint。

#### D. External Cache / Tool State

- search cache；
- browser session；
- tool result cache；
- vector-store index；
- temporary files；
- database transaction state。

只 reset 对话历史，不代表实验已经 state-isolated。

### 3. 六类常见 Leakage / Contamination

#### 3.1 Cross-task contamination

上一题的信息进入下一题，导致后续任务“提前知道”答案、schema、错误修正或路径。

#### 3.2 Dev-to-test overreach

根据开发集错误构造规则本身可以是合法开发；问题在于测试集必须是未参与这轮规则设计的 holdout。

#### 3.3 Test-to-memory writeback

正式测试期间把 test failure / answer / feedback 写回 memory，然后继续评同一测试集，会让后面的样本不再是同一冻结系统。

#### 3.4 Repeat contamination

同一 task 跑三次，如果第 1 次结果写进 memory，第 2、3 次就不再是独立重复，而是在测 adaptation。

#### 3.5 Condition contamination

memory-on 条件先跑并改变共享 environment，memory-off 条件随后使用了已经变化的 state。

#### 3.6 Stale / incompatible memory

旧 memory 对应旧 schema、旧 contract、旧 tool API，却继续被检索。即使没有“答案泄漏”，也会产生隐蔽 confounder。

### 4. Snapshot / Fork / Reset

正式 protocol 应对每类状态明确策略：

```text
RESET      每个 episode 从空状态开始
SNAPSHOT   记录精确版本，并在运行前恢复
FORK       两个条件从同一 snapshot 分叉
PERSIST    明确允许跨 episode 保留
READ_ONLY  可读但不允许写
WRITE      允许写，但必须说明写入范围与后续影响
```

对于 baseline vs candidate 的 paired eval，一个强设计是：

```text
Frozen task
+ same environment snapshot
+ same model config
+ same initial memory base
→ fork
   ├─ baseline condition
   └─ candidate condition
```

### 5. Memory Provenance 必须可追溯

每条可检索 memory 最少应知道：

```text
memory_id
version / snapshot_id
source type
source task hash
source split
created_at / build version
contract / schema version
validation status
```

否则无法回答：

- 这条规则是不是来自 test？
- 是否包含原题答案？
- 是否仍兼容当前 schema？
- 是人工复核规则还是自动生成？

### 6. Retrieval Event 只是机制第一步

一个完整因果链应拆成：

```text
eligible opportunity
→ memory retrieved
→ memory actually injected
→ model request saw it
→ behavior changed at affected stage
→ downstream outcome changed
```

因此：

```text
Retrieval coverage high
```

只能说明链路触发得多，不能直接说明 memory 有效。

### 7. Mechanism ≠ Outcome

典型错误归因：

```text
memory-on score 更高
+ memory retrieval 出现过
→ memory caused improvement
```

不够。

至少继续问：

1. 改善样本是否真的命中该 memory？
2. 失败 / 改善发生阶段是否在 memory 可影响的阶段之后？
3. baseline / candidate 在 memory 介入前的 prefix 是否一致？
4. memory 注入后具体 action 是否变化？
5. 变化是否和正确结果存在可解释路径？

### 8. Memory Eval 的几个独立问题

不要把它们压成一个“memory accuracy”：

#### Availability

应该检索时是否有可用 memory？

#### Retrieval

是否检索到相关且兼容的 memory？

#### Utilization

模型是否真正利用，而不是 prompt 里出现但行为不变？

#### Effect

行为 / outcome 是否改善？

#### Harm

是否引入错误、过时规则、过拟合或额外成本？

#### Cost

memory 增加多少 prompt token、latency、retrieval calls？

### 9. 推荐 Metrics

#### State Isolation Violation Rate

```text
检测到非预期跨 episode / 条件状态泄漏的运行
---------------------------------------
正式评测运行
```

理想情况下关键冻结评测应为 0。

#### Memory Retrieval Coverage

```text
发生 retrieval / injection 的 eligible opportunities
-----------------------------------------------
eligible opportunities
```

这是机制 coverage，不是收益指标。

#### Stale / Invalid Memory Hit Rate

衡量检索到过期、contract 不兼容或来源不允许的 memory。

#### Memory Net Benefit

对于 paired runs：

```text
(candidate 对而 baseline 错)
-
(candidate 错而 baseline 对)
--------------------------------
paired runs
```

它描述观察到的净 outcome 差，不自动提供因果证明。

#### Memory Cost per Valid Success

所有 memory-on 运行成本都进入分子，包含失败和无收益命中。

### 10. Run Order

即使所有状态都“理论可重置”，运行顺序仍可能关联：

- provider drift；
- rate limit；
- warm cache；
- environment time；
- shared resource contention。

因此 paired condition 常采用：

```text
same task / repeat
alternate or randomized order
```

并保存 order，便于诊断。

## 一个实用 Stateful Eval Contract

```text
Task set + split
Model/config version
Environment snapshot ID
Memory snapshot ID
Memory source policy
Read/write policy
Per-episode reset policy
Cache/tool-state policy
Condition fork strategy
Run order
Repeat policy
Retrieval trace schema
Write-event trace schema
Test writeback prohibition
Scoring / metrics
Abort / resume policy
```

## Common wrong answers

### 错误 1：只要 test question 没直接写进 memory，就不存在 leakage

还可能泄漏 schema、答案模式、错误修正、环境状态或同一题的等价信息。

### 错误 2：同一题重复 3 次就是 3 个独立样本

如果共享可写状态，就不是独立重复；即使只读，也仍然只是 1 个不同 task 的 3 次 stochastic observations。

### 错误 3：Memory hit 多说明 memory 有价值

命中率只说明机制活跃。高命中但无收益甚至增加成本完全可能发生。

### 错误 4：测试失败很有价值，所以直接加入 memory 再继续测

这会把同一 test set 变成开发集，破坏 holdout。

### 错误 5：两组最终分数不同，所以一定是 memory 导致

需要检查 memory 作用路径和介入前状态是否可比。

## Counterexample / boundary

如果 memory 的产品目标本来就是“在线持续学习”，那么跨 episode 写入不是 bug。但评测问题必须随之改变：你需要测的是 adaptation curve、catastrophic contamination、regret、forgetting 和安全性，而不能再把每个 episode 当作冻结系统的 IID benchmark。

## VeriAgent example

VeriAgent 的 memory evaluation 很适合作为 stateful Eval 的 canonical case。

现有设计会：

- 在运行前冻结 memory snapshot；
- memory-on / memory-off 使用相同题目与模型配置；
- 运行期间不追加经验；
- 禁止 source question 与评测问题完全相同；
- 测试目录不会被默认经验构建脚本扫描；
- 记录 `memory_retrieved`、snapshot ID、命中规则与阶段；
- `llm_request_started` 保存 messages 与 prompt hash，可验证规则是否真的进入模型输入；
- API 错误导致整轮 `ABORTED`，不对不完整 paired experiment 出比较结论。

更关键的是 challenge candidate 的保留测试：candidate 最终比 baseline 多对 1/36，但 13 次失败都发生在 SQL-stage memory retrieval 之前，而 candidate memory 只作用于 SQL 阶段。因此这个 +1/36 不能合理归因于 memory。

这正是：

```text
memory mechanism exists
≠ memory affected this failure
≠ memory caused observed score difference
```

## Follow-up questions

- memory-on/off 是否必须完全同顺序？
- retrieval hit 的 denominator 应该是所有任务还是 eligible opportunity？
- 如何检测语义近重复造成的 test contamination？
- online-learning Agent 应该如何重新定义 evaluation unit？
- cache 算 memory 吗？什么时候必须 reset？

## Evidence of mastery

达到 S4 时，应能为一个带长期记忆的 Agent 写出：

- state inventory；
- reset/snapshot/fork policy；
- provenance schema；
- dev/test write policy；
- paired protocol；
- retrieval → behavior → outcome attribution；
- contamination tests；
- memory benefit / harm / cost metrics。

## Related knowledge

- [Q12 Agent Evaluation Contract](01_Agent_Evaluation_Contract.md)
- [Q13 Tool Use & Grounding](02_Tool_Use_and_Grounding_Evaluation.md)
- [Q14 Recovery & Graceful Degradation](03_Recovery_and_Graceful_Degradation.md)
- [Q03 What Are We Measuring](../01_LLM_Evaluation/02_What_Are_We_Measuring.md)
- [Q02 Estimand & Unit of Analysis](../06_Statistics_and_Experiment_Design/01_Estimand_and_Unit_of_Analysis.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
