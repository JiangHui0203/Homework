# Q18 step-level correctness 与最终 outcome 应如何联合分析，避免错误 credit assignment？

- Level: M1
- Mastery: S0
- Related Parts: Part 3 / Part 4 / Part 6
- Related Patterns: P03 Paired Same-Task Comparison, P06 Trajectory First-Failure Analysis, P12 Mechanism ≠ Outcome

## 30-second answer

Agent 的 step correctness 与 final outcome 是两个不同层次的变量。**正确 outcome 不证明每一步正确，错误 outcome 也不证明每一步都错。**

做 credit assignment 时，应把 trajectory 分成关键 decision point / checkpoint，记录每一步是否正确、是否必要、是否被采用、是否影响下游，再与最终 outcome 联合分析。最重要的是区分：`robust success`、`lucky success`、`recovered success`、`downstream failure after correct prefix` 和 `irrelevant mechanism activation`。

## 90-second answer

我不会给每一步平均打分后直接当 Agent 总分。先定义哪些 step 对 claim 有语义：tool selection、arguments、verification、recovery decision、memory injection 等。然后建立：

```text
step state
→ downstream behavior change
→ final outcome
```

至少做四格分析：

```text
step correct + outcome correct
step correct + outcome wrong
step wrong   + outcome correct
step wrong   + outcome wrong
```

其中 `step wrong + outcome correct` 是 lucky / compensated success 的重要信号；`step correct + outcome wrong` 说明失败在更后游，不能把 outcome loss 归给当前 step。

对机制改动，最好做 paired / counterfactual evidence，避免把“机制被触发”误写成“机制贡献了成功”。

## 1. 为什么 outcome 不能直接反推 step

例子：

```text
wrong tool argument
→ tool returns overly broad data
→ later filter accidentally removes extra rows
→ final answer correct
```

Final success=1，但这不是可靠路径。

反过来：

```text
correct plan
→ correct SQL
→ provider timeout
→ final failure
```

Final failure=1，也不能说 planner / SQL 能力失败。

## 2. 四类基础联合状态

设关键 step correctness 为 S，final outcome correctness 为 Y：

| S | Y | 解释 |
|---|---|---|
| 1 | 1 | 可能是 robust success；仍需看其他关键步骤 |
| 1 | 0 | 当前 step 不是失败点，继续向后找 |
| 0 | 1 | lucky / compensated / recovered success |
| 0 | 0 | step 可能贡献失败，但仍需因果证据 |

这张表是 trajectory credit assignment 的最低配。

## 3. 不要把所有 step 等权平均

平均 step score 的问题：

```text
9 个无关紧要步骤正确
+ 1 个关键 irreversible action 错误
```

平均 90% 仍可能是灾难性 failure。

所以需要：

```text
criticality
exposure
recoverability
downstream dependency
```

而不是只数“对了几步”。

## 4. Step 是否“正确”也需要 contract

不同 step 的 correctness evidence 不同：

```text
Task interpretation -> constraint checklist / human reference
Tool selection      -> eligible tool set / task contract
Arguments           -> schema / state predicate / reference
Execution           -> environment result
Grounding           -> observation-support relation
Verification        -> verifier reference
Recovery decision   -> recoverability policy
Memory retrieval    -> eligibility / snapshot / provenance
```

开放语义 step 若必须 Judge，Judge 本身也需要 Q08–Q11 的 calibration。

## 5. Credit assignment 的三层问题

### A. Did the mechanism activate?

例如 memory 是否 retrieved / injected。

### B. Did behavior change?

同一 prefix / comparable condition 下，输出是否因该机制改变。

### C. Did outcome improve because of it?

行为改变是否真正改善 final outcome。

所以：

```text
Activated
≠ Used
≠ Behavior changed
≠ Outcome improved
```

## 6. Paired evidence 比 aggregate correlation 更有力

若比较 baseline / candidate：

```text
same task
same repeat slot
same environment snapshot
same evaluator
```

记录：

```text
both correct
baseline only
candidate only
both wrong
```

然后再检查 winner / loser 的 first meaningful failure 是否落在候选机制可作用的阶段。

这比“candidate 组平均分更高，所以机制有效”更可信。

## 7. Credit window

对于某个 step，不要把整个 episode 的所有后果都归给它。

可以定义局部 credit window：

```text
step event
→ immediate observation
→ next decision / checkpoint
```

先判断局部影响，再决定是否向最终 outcome 延伸。

这对 long-horizon Agent 尤其重要。

## 8. Recovery 会改变 credit 解释

```text
wrong first tool call
→ verifier detects
→ corrected retry
→ success
```

应该同时记：

```text
initial step incorrect
recovery correct
final outcome correct
```

不能把 episode 简化成“成功，所以所有模块表现好”。

也不能简化成“发生错误，所以整个任务失败”。

## 9. Step metrics 的 denominator 需要 exposure-aware

例如 SQL-stage memory retrieval：

```text
retrieved / all episodes
```

如果很多 episode 根本没到 SQL stage，会混淆 eligibility。

更合理：

```text
retrieved / episodes that reached eligible SQL stage
```

同理，verification accuracy 应基于真正产生 verification opportunity 的事件。

## 10. VeriAgent example

challenge candidate memory 测试中：

```text
baseline 29/36
candidate 30/36
paired net +1/36
```

如果只看 final outcome，很容易给 memory 记正 credit。

但 trace 显示 13 次失败都发生在 SQL-stage memory retrieval 之前，而且两组首次 analysis prompt hash 相同。candidate memory 只在 SQL generation 阶段生效。

因此正确的 credit assignment 是：

```text
mechanism implementation: active on eligible later-stage runs
observed final difference: +1/36
causal credit to memory: unsupported
```

这就是 `Mechanism ≠ Outcome` 的真实案例。

## 11. Recommended record

关键 step 记录至少包含：

```text
step_id
stage
opportunity / eligibility
expected behavior
observed behavior
correctness label
evidence source
criticality
recovered?
downstream checkpoint effect
final outcome
causal status: observed / supported / hypothesis
```

## Common wrong answers

### 错误 1：Final answer 对，所以 trajectory 对

会隐藏 lucky success 和脆弱路径。

### 错误 2：Final answer 错，所以所有步骤都给 0

无法定位真正 failure，也无法识别正确但被后游破坏的模块。

### 错误 3：模块触发次数多，所以贡献大

coverage 不是 benefit。

### 错误 4：每步 reward 加起来就是可靠 credit

若 reward/evaluator 有偏差、步骤依赖强或 action 不等价，加和会制造伪精度。

## Evaluation design

对一个候选机制至少回答：

1. 它在哪些 opportunity eligible？
2. 实际是否 activate？
3. 是否改变了局部行为？
4. 改变发生在 first meaningful failure 之前还是之后？
5. paired outcome 是否改善？
6. 是否存在 regressions？
7. 是否能 replay / counterfactually isolate？

## Follow-up questions

- Process reward model 能否替代 trajectory analysis？
- lucky success 要不要算 task success？
- step correctness 不可 deterministic verify 时怎么办？
- 如何给 irreversible action 更高权重？

## Evidence of mastery

达到 S4 时，应能对一条多步 trajectory 同时给出：

```text
step correctness map
first meaningful failure
recovery map
final outcome
credit / no-credit conclusion
```

并解释为什么某个中间模块不能仅凭 final score 获得 causal credit。

## Related knowledge

- [Q17 First Meaningful Failure & Root Cause](01_First_Meaningful_Failure_and_Root_Cause.md)
- [Q14 Recovery & Graceful Degradation](../03_Agent_Evaluation/03_Recovery_and_Graceful_Degradation.md)
- [Q15 State / Memory Evaluation](../03_Agent_Evaluation/04_State_Memory_and_Leakage_Evaluation.md)
