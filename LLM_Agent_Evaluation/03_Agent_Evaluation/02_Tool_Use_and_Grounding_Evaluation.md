# Q13 如何评价 Tool Selection、Arguments、Grounding 与 Final Answer？

- Level: M1
- Mastery: S0
- Related Parts: Part 3 / Part 4 / Part 7
- Related Patterns: P02 Deterministic First, Judge Last; P06 Trajectory First-Failure Analysis; P10 Replayable Evaluation; P12 Mechanism ≠ Outcome
- Related Metrics: Tool Selection Accuracy, Argument / Constraint Accuracy, Tool Result Grounding Rate, Unnecessary Tool Call Rate
- Related Case: VeriAgent Olist Data Agent

## 30-second answer

Tool-use evaluation 不能只看“工具有没有调用成功”。一条完整链路至少要拆成：

```text
Should call a tool?
→ Which tool?
→ With what arguments / constraints?
→ Did execution succeed?
→ Was the returned observation interpreted correctly?
→ Did the final answer stay grounded in that observation?
```

其中每一层都可能独立失败，而且 denominator 不一样。最重要的两个原则是：**不要只在实际发生的 tool calls 上算 accuracy**，否则“根本没调用该调用的工具”会从分母消失；以及**execution success 不等于 semantic correctness**，一个 SQL、API 或搜索调用完全可以执行成功但回答错问题。

## 90-second answer

我会把 Tool Eval 设计成一个可审计的 action contract，而不是单一 tool-call accuracy。

第一层是 **tool opportunity / selection**：这个状态下是否应该调用工具，允许哪些工具，是否允许 no-tool。第二层是 **arguments / constraints**：参数、过滤条件、时间范围、ID、权限、schema 等是否满足任务合同。第三层是 **execution**：调用是否真正完成，区分系统参数错误、工具业务错误与基础设施错误。第四层是 **observation grounding**：Agent 后续推理是否忠实使用工具返回，而不是忽略、误读或编造。最后是 **final grounding**：最终结论是否能追溯到有效 observation，是否出现 unsupported claim。

因此常见指标会分开报告：tool selection accuracy、critical-argument accuracy、execution success、grounding rate、unnecessary call rate、unsupported final claim rate。对于数据库、计算器、代码执行、schema validation 等有强证据的部分优先 deterministic verifier；开放语义部分才交给 rubric / Judge。

## Full reasoning

### 1. Tool-use 不是一个动作，而是一条证据链

最小链路：

```text
State S_t
→ Decide tool / no-tool
→ Construct action A_t
→ Tool executes
→ Observation O_t
→ State update
→ Later reasoning / action
→ Final answer
```

因此“tool call 成功”最多证明执行层没有报错，不能证明：

- 工具选对了；
- 参数语义正确；
- observation 是所需证据；
- Agent 读懂了结果；
- final answer 没有越过 evidence。

### 2. 第一层：Tool Opportunity 与 Selection

先定义状态下的允许动作：

```text
required tool set
allowed equivalent tools
no-tool allowed?
forbidden tools
```

然后再定义 selection correctness。

#### Denominator trap

错误：

```text
正确 tool calls / 实际 tool calls
```

如果 Agent 在 10 个必须查数据库的任务里有 4 次直接编答案，只在剩下 6 次调用工具，那么这 4 次会从分母消失。

更合理的是根据 **tool opportunities / decision states** 计量：

```text
correct tool decision / eligible tool-decision opportunities
```

同时把：

```text
missed required call
unnecessary call
forbidden call
```

分开记录。

### 3. 第二层：Arguments / Constraints

同一个工具被选中后，参数仍可能错。

常见关键字段：

- entity / resource ID；
- time range；
- filter / status；
- aggregation grain；
- permissions；
- query / schema；
- output format；
- safety constraints。

不要把所有字段机械平均。更实用的方式是区分：

```text
critical arguments
optional arguments
format-only fields
```

一个关键 ID 错误不应该被 8 个无关格式字段的正确率稀释。

可以同时报告：

```text
Exact Action Contract Pass
Critical-Argument Accuracy
Field-level Diagnostic Accuracy
```

其中 release gate 通常更适合前两者，field-level 更适合诊断。

### 4. 第三层：Execution Success

需要至少区分：

```text
SUCCESS
TOOL_REJECTED_INVALID_ARGUMENT
TOOL_BUSINESS_ERROR
PERMISSION_DENIED
TIMEOUT
PROVIDER / INFRA ERROR
```

这一步的重要边界是：

> execution failure 不一定说明 tool selection 错；execution success 也不说明任务语义正确。

例如错误 SQL 可以合法执行并返回一个错误数字；错误日期过滤也可能正常返回结果。

### 5. 第四层：Observation Grounding

工具返回结果后，Agent 是否真的基于它继续？

典型失败：

- observation 明确是 42，Agent 最后写成 24；
- tool 返回 `NOT_FOUND`，Agent 却补出一个实体属性；
- tool 返回多个候选，Agent 无依据选其中一个；
- 新 observation 已推翻旧信息，但 Agent 继续沿用 stale state；
- 调用了工具，但最终答案实际上来自模型先验。

可定义：

```text
Grounded Observation Use Rate
= 后续关键结论被有效 observation 支持的机会数
  / 需要使用 observation 的机会数
```

更严格的系统可以把 final claims 映射到 evidence IDs。

### 6. 第五层：Final Answer Grounding

最终答案至少检查：

1. final claim 是否来自有效 tool evidence；
2. 是否漏掉必要约束；
3. 是否在证据范围之外扩张；
4. tool evidence 冲突时如何处理；
5. tool failure 时是否安全停止或降级。

因此应长期区分：

```text
Tool execution success
≠ Tool semantic correctness
≠ Observation grounding
≠ Final task success
```

### 7. Deterministic First

优先 deterministic verify 的对象包括：

- JSON / schema；
- API required fields；
- SQL execution；
- exact IDs；
- numeric result；
- permission predicates；
- environment state change。

Judge 更适合：

- observation 是否充分支持开放式解释；
- 多证据综合是否合理；
- final answer 是否清楚表达不确定性。

不要让 LLM Judge 去猜一个本来可以直接执行验证的参数或结果。

## 一个实用的 Tool Eval Contract

每个关键 action 至少保留：

```text
task_id
run_id
step_id
pre_state_id
opportunity_type
expected_action_set
chosen_tool / NO_TOOL
arguments
critical_argument_checks
execution_status
observation_id / hash
observation_validity
later_steps_using_observation
final_claim_evidence_links
```

这样才能稳定回答“第一次真正失败在哪一层”。

## Recommended metrics

### Tool Selection Accuracy

```text
正确 tool / no-tool 决策数
------------------------
eligible tool-decision opportunities
```

如果多个工具等价，应在 contract 里声明 allowed set，而不是只接受一个名字。

### Critical-Argument Accuracy

```text
通过全部 critical argument checks 的 actions
------------------------------------------
需要这些关键参数的 actions
```

### Tool Execution Success Rate

回答的是工具执行层可靠性，不等价于任务成功。

### Tool Result Grounding Rate

衡量后续关键结论是否被有效 observation 支持。

### Unnecessary Tool Call Rate

```text
无必要 / 无信息增益的调用
-----------------------
eligible tool-decision opportunities
```

需要预先定义“unnecessary”的判据，不能结果不好后再主观判定。

## Evaluation design

拿到一个新 Agent，建议按以下顺序：

```text
1. 定义 task-level outcome
2. 标注关键 tool opportunities
3. 为每个 opportunity 定义 allowed action set
4. 冻结 critical argument contract
5. 区分 execution status
6. 保存 observation / state transition
7. 定义 grounding checks
8. 最后再汇总 final outcome
```

### 最少切片

- tool type；
- task family；
- first-pass / recovery path；
- critical vs non-critical action；
- success vs failure trajectory；
- long vs short trajectory。

## Common wrong answers

### 错误 1：API 返回 200，所以工具调用正确

HTTP / execution success 只证明调用完成，不证明语义正确。

### 错误 2：只统计实际 tool calls

会把 missed calls 从 denominator 删除，selection accuracy 被高估。

### 错误 3：所有 argument 字段同权平均

关键 ID 或权限错误可能被大量格式字段稀释。

### 错误 4：最终答案正确，所以工具路径正确

可能是 lucky success、错误抵消，甚至完全没使用工具结果。

### 错误 5：Tool Eval 就是 Tool Benchmark

Benchmark 是任务集合；Tool Eval 还需要 action contract、state、execution、grounding 和 final attribution。

## Counterexample / boundary

如果任务只要求调用一个确定函数，参数完全由输入直接映射，且 final output 就是工具原样返回，那么 selection / argument / grounding 可以高度合并。但一旦存在多个工具、多阶段状态、重试或证据综合，就应拆层。

## VeriAgent example

VeriAgent 的 Olist Data Agent 提供了一个很好的“execution 与 semantic correctness 必须分开”的案例。

挑战题中曾出现：

- SQL 因引用当前作用域不存在的 alias 而被 DuckDB 拒绝；
- 另一条 SQL 可以执行，但筛选逻辑错误并返回 0，错误答案被 runtime 接受；
- 保留测试中多次失败发生在 SQL 阶段经验检索之前，因此不能把后续 memory 模块是否命中当作这些失败的原因。

这些 trace 说明：

```text
调用了 SQL
≠ SQL 可执行
≠ SQL 语义正确
≠ runtime 正确识别结果
≠ final answer 可靠
```

而 schema / SQL / numeric reference 本身又有较强 deterministic evidence，所以这些层不需要先交给 LLM Judge。

## Follow-up questions

- 多个工具都能完成任务时 selection accuracy 怎么定义？
- tool opportunity 本身需要人工标注吗？
- 一次错误调用后成功 recovery，tool accuracy 和 task success 怎么联合报告？
- retrieval / search 返回相关但不充分的信息，grounding 怎么打分？
- tool result 本身错误时责任归 Agent 还是环境？

## Evidence of mastery

达到 S4 时，应能拿到一条真实 Agent trace，逐步标出：

```text
opportunity
selection
arguments
execution
observation
state update
grounding
final claim
```

并为每层定义 denominator、deterministic checks、failure type 与至少一个不应被 aggregate 掩盖的 slice。

## Related knowledge

- [Q12 Agent Evaluation Contract](01_Agent_Evaluation_Contract.md)
- [Q04 Metric Design](../01_LLM_Evaluation/03_Metric_Design.md)
- [Q07 Grader / Verifier / Judge](../02_Grader_and_LLM_as_a_Judge/01_Grader_Verifier_and_Judge.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
- [Metrics Registry](../METRICS.md)
