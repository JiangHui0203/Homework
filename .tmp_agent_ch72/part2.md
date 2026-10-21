#### 7.2.23 BRANCH 到底什么时候出现

`BRANCH` 表示：

> **当前不应只沿一条 continuation 继续，而应该显式保留多个候选路径。**

常见触发条件包括：

- 高不确定性且错误代价高；
- 多个假设都合理，需要分别验证；
- 不同搜索方向可以并行探索；
- 一个 plan 出现风险，需要保留 fallback；
- 多个 subagent 可以独立处理互不依赖的子问题。

但 Branch 不是免费的。

它会增加：

```text
model calls
tool calls
state copies
merge complexity
verification cost
side-effect risk
```

所以 Loop Policy 需要决定的不是“能不能 branch”，而是：

```text
branch value > branch cost ?
```

---

#### 7.2.24 Branch 之后必须有 Merge / Selection Policy

只会分支，不会收束，会把 Agent 变成搜索树生成器。

一个完整 branch lifecycle 应该是：

```text
fork
  ├─ branch A
  ├─ branch B
  └─ branch C
        ↓
collect comparable evidence
        ↓
verify / score / reconcile
        ↓
select / merge / keep multiple
        ↓
commit accepted state
```

关键原则是：

> **Branch State 不应在未经 reconciliation 的情况下直接污染 authoritative state。**

例如三个候选都修改同一个文件时，不能把三个副作用直接执行一遍，再让模型决定哪个更好。

通常应该先：

```text
branch in isolated / speculative state
→ evaluate
→ commit selected effect
```

---

#### 7.2.25 Loop Policy 与 Planning Policy 的边界

Planning Policy 回答：

```text
怎样形成未来行动结构？
什么时候生成 plan？
什么时候 replan？
```

Loop Policy 回答：

```text
现在这个 run 应该进入哪个状态？
是否该执行 plan 的下一步？
是否该暂停、验证、重新决策或停止？
```

因此：

```text
Plan
= 对未来路径的表示

Loop Policy
= 对当前 transition 的控制
```

即使 Agent 已有完整 plan：

```text
Step 1 → Step 2 → Step 3 → Step 4
```

Loop Policy 仍需要在每一步检查：

```text
observation 是否符合预期？
plan 是否仍有效？
是否需要 WAIT？
是否需要 VERIFY？
是否应该 STOP？
```

---

#### 7.2.26 Loop Policy 与 Termination Policy 的边界

7.10 会专门讨论 Termination Policy，因此 7.2 只保留接口。

Loop Policy 需要知道：

```text
当前是否进入 terminal candidate？
是否需要 completion verification？
哪个 terminal state 应被设置？
```

但更细的：

```text
什么算 semantic completion？
成功条件怎样定义？
partial success 怎么表达？
blocked 与 failed 如何区分？
```

属于 7.10。

因此这里先记住：

> **Loop Policy 决定何时走向终止；Termination Policy 定义什么条件允许终止。**

---

#### 7.2.27 Loop Policy 与 Recovery Policy 的边界

7.11 会讨论：

```text
失败后从哪里恢复？
如何 checkpoint？
如何 fallback？
如何 compensation？
如何处理 partial side effect？
```

7.2 只回答：

```text
当前 failure 是否还能在正常 loop 内处理？
还是应该 transition 到 RECOVERING？
```

可以记成：

```text
Loop Policy
    ↓
RECOVER transition
    ↓
Recovery Policy
    ↓
recovered state / terminal failure
    ↓
Loop Policy resumes
```

---

#### 7.2.28 Transition 应该有优先级

如果同一时刻满足多个条件，不能随便选择。

一个常见的高层优先级可以是：

```text
1. cancellation / hard safety stop
2. terminal failure / hard budget limit
3. pending approval / permission gate
4. unresolved side-effect reconciliation
5. required verification
6. external wait dependency
7. deterministic transition
8. semantic model decision
9. optional optimization / branching
```

为什么安全停止要高于“继续完成任务”？

因为：

```text
Goal Pursuit
<
System Invariants
```

为什么 pending side effect 要高于重新规划？

因为如果不知道前一个 action 是否已经发生，再规划很可能产生重复副作用。

---

#### 7.2.29 Loop Invariant 是什么

**Loop Invariant** 是在整个 run 中始终必须成立的条件。

例如：

```text
每个 side-effecting action 都有唯一 action_id
未通过 approval 的 action 不得执行
pending action 未 reconcile 前不得重复提交
current state 必须可持久化
每个 transition 都记录 reason
terminal state 不能重新偷偷进入 running
```

它们与 Goal 不同。

Goal 是：

```text
我要完成什么？
```

Invariant 是：

```text
无论怎样完成，都不能破坏什么？
```

因此可靠的 Loop 不是只优化：

```text
finish the task
```

还要保证：

```text
preserve invariants while making progress
```

---

#### 7.2.30 Iteration ≠ Progress

Agent 运行了 50 轮，不代表取得了 50 轮进展。

可能只是：

```text
search A
→ reformulate A
→ search A again
→ summarize same evidence
→ reconsider same plan
→ search A again
```

因此：

> **Iteration 是计算发生；Progress 是任务状态发生了有意义的改善。**

Loop Policy 必须把两者分开。

否则最简单的防死循环方法只能是：

```text
max_steps = 20
```

但它只能限制损失，不能识别“第 6 步以后其实已经没有进展”。

---

#### 7.2.31 什么叫 Progress

Progress 应尽量绑定**任务状态变化**，而不是语言长度。

可能的 Progress Evidence 包括：

```text
一个未解决子目标被关闭
一个关键未知量被确定
一个 blocker 被解除
新的独立证据被获得
一个 artifact 从 invalid → valid
测试失败数减少
覆盖率增加
计划中的 milestone 被满足
风险降低
用户所需交付物更接近验收标准
```

因此可以抽象：

$$
\Delta P_t = P(S_{t+1}) - P(S_t)
$$

这里的 $P$ 不一定是单个数，但系统至少应该能回答：

> **这一轮具体改变了什么？**

---

#### 7.2.32 Progress Signal 可以是结构化的

与其让模型每轮自评：

```text
我觉得取得了进展。
```

更好的做法可能是维护：

```json
{
  "open_subgoals": 3,
  "resolved_subgoals": 5,
  "failed_tests": 2,
  "verified_claims": 8,
  "unresolved_blockers": 1,
  "last_novel_observation_at": 14
}
```

不同任务的 progress schema 不同，但原则一致：

> **能够从 Environment / State 推导的进展，优先结构化，不要全部交给模型自述。**

---

#### 7.2.33 No-progress Detection 比 Max Steps 更重要

一个基本 anti-loop policy 可以同时维护：

```text
max_turns
max_tool_calls
max_wall_time
max_cost
no_progress_window
same_state_window
same_action_window
```

例如：

```text
最近 5 个 transition：
- 没有关闭任何 subgoal
- 没有获得新的 observation
- 没有改变 accepted artifact
- 反复执行同类搜索
```

此时即使还没达到 `max_turns`，也应该触发：

```text
replan
branch
escalate
ask user
stop as blocked
```

---

#### 7.2.34 Repeated Action Detection

最直观的死循环是：

```text
search("X")
search("X")
search("X")
```

但实际判断不能只比较字符串。

下面这些也可能语义重复：

```text
search("OpenAI agent loop")
search("agent loop OpenAI")
search("OpenAI runner agent cycle")
```

因此 repeated action 可以分层：

```text
Exact Repeat
Parameter-equivalent Repeat
Semantic Repeat
Effect-equivalent Repeat
```

如果重复行为没有带来新的 observation，Loop Policy 应提高继续成本。

---

#### 7.2.35 Repeated State Detection

比重复 action 更一般的是：

```text
S_t ≈ S_{t-k}
```

也就是系统绕了一圈又回到同一任务状态。

例如：

```text
Plan A
→ Tool fail
→ Plan B
→ Tool fail
→ fallback
→ again Plan A
```

如果没有新证据，只是回到了同一个 unresolved state，这是一种 loop cycle。

因此可以维护：

```text
state fingerprint
open-goal signature
pending-action signature
artifact hash
known-facts digest
```

用来检测是否真正跨越了新的状态边界。

---

#### 7.2.36 Oscillation 是另一种 Loop Failure

有些 Agent 不会原地重复，而是在两个状态之间摇摆：

```text
A → B → A → B → A
```

例如：

```text
“应该重构”
→ 重构
→ “还是原方案更简单”
→ 回滚
→ “重构似乎更好”
→ 再重构
```

或者：

```text
Search web
→ Trust local docs
→ Search web
→ Trust local docs
```

这叫 **oscillation**。

Loop Policy 需要在检测到反复翻转时要求：

```text
新证据是什么？
切换的判据是什么？
是否应该冻结一个决策？
是否需要独立 verifier？
```

---

#### 7.2.37 Overthinking 也是 Loop Failure

无限循环不一定包含 Tool。

还可能是：

```text
Think
→ reconsider
→ critique
→ rethink
→ rewrite plan
→ critique again
```

状态没有获得新的外部证据，也没有提交任何可验证变化。

这可以叫：

```text
semantic loop
reasoning loop
reflection loop
```

因此：

> **更多思考不是天然的 progress。**

Loop Policy 应要求后续 deliberation 具备明确的信息价值：

```text
解决新的不确定性？
比较新的候选？
吸收新的 observation？
修复 verifier 指出的具体问题？
```

如果都没有，继续 reasoning 很可能只是无效计算。

---

#### 7.2.38 Productive Deliberation 与 Redundant Reflection

可以用下面的边界理解。

##### Productive Deliberation

```text
new evidence → reconsider
new constraint → replan
verifier failure → diagnose
multiple candidates → compare
high-risk decision → second check
```

##### Redundant Reflection

```text
same state → same question → another paraphrased answer
no new evidence → repeated self-critique
already verified → keep doubting without criterion
```

所以 Reflection Policy 不应该是：

```text
after every step, reflect once
```

而应该是：

```text
reflect when expected value of reconsideration is positive
```

---

#### 7.2.39 Retry ≠ Re-decide

Tool 超时后，系统可以：

```text
retry same request
```

这和：

```text
ask model what to do next
```

是两件事。

如果错误属于：

```text
known transient failure
```

则优先：

```text
system retry policy
```

如果错误属于：

```text
semantic failure
invalid assumption
wrong tool choice
non-retryable response
```

才更可能需要：

```text
model re-decision
```

因此：

> **不要把所有异常都升级成新的 LLM turn。**

---

#### 7.2.40 Retry 必须有 Ceiling

没有 ceiling 的 retry 只是另一种无限循环。

至少需要：

```text
attempt_count
retryable_error_class
backoff_policy
deadline
max_attempts
fallback
exhaustion_transition
```

例如：

```text
attempt 1 → retry
attempt 2 → retry with backoff
attempt 3 → fallback provider
fallback fail → RECOVER / BLOCKED
```

而不是：

```text
while error:
    retry()
```

---

#### 7.2.41 Loop Budget 不是只有 max_turns

`max_turns` 很重要，但只是最粗粒度的 guard。

一个 Agent run 可能同时拥有：

```text
model_call_budget
token_budget
tool_call_budget
search_budget
retry_budget
branch_budget
wall_clock_budget
monetary_budget
side_effect_budget
human_interrupt_budget
context_budget
```

不同资源不能简单等价。

一次：

```text
read_file
```

和一次：

```text
send_payment
```

即使都算一个 Tool Call，风险完全不同。

---

#### 7.2.42 Hard Budget 与 Soft Budget

##### Hard Budget

触发后必须阻断：

```text
absolute cost limit
security threshold
deadline
max recursive depth
regulatory restriction
```

##### Soft Budget

触发后提高继续门槛：

```text
搜索已很多次
上下文开始膨胀
边际信息增益下降
分支数量过多
```

Soft Budget 后可以要求：

```text
higher expected value to continue
```

所以：

> **预算不只是“还有多少”，还可以影响 Loop 的决策门槛。**

---

#### 7.2.43 Budget 应该与 Risk 联动

低风险 read-only task 可以允许更多自治探索。

高风险 side effect task 应更保守。

例如：

```text
Web Research
    → higher search / branch budget

Delete Production Data
    → minimal autonomous retries
    → stronger verification
    → approval before effect
```

因此更准确的是：

$$
ContinueThreshold = f(Cost, Risk, Uncertainty, ExpectedGain)
$$

即：

> **高风险场景下，“再试一次”的门槛应高于低风险场景。**

---

#### 7.2.44 Turn、Step、Transition 不应混用做预算

不同框架里 `turn` 的定义可能不同。

例如某些 Runner 把：

```text
一次 LLM invocation
```

算作一个 turn；而一次 turn 内可能包含多个 Tool Call。

所以生产系统最好分别记录：

```text
model_invocations
loop_transitions
actions_executed
tool_calls
retries
branches
```

否则：

```text
max_turns = 10
```

看起来简单，但你并不知道这 10 turn 实际对应多少外部行为。

