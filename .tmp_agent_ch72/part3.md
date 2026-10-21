#### 7.2.45 一个系统里可能同时存在多层 Loop

真实 Agent 系统经常不是一个平面循环。

可能同时存在：

```text
Application Loop
    ↓
Workflow Loop
    ↓
Agent Run Loop
    ↓
Planning / Verification Sub-loop
    ↓
Tool Retry Loop
    ↓
Model Decoding Loop
```

这些 Loop 的 owner、state 和 stop condition 不同。

例如：

```text
Tool Retry Loop exhausted
```

不一定意味着：

```text
Agent Run failed
```

Agent 可能换 Tool。

同样：

```text
Agent Run completed
```

也不一定意味着：

```text
Application Workflow completed
```

外层可能还有审批或交付步骤。

---

#### 7.2.46 Nested Loop 必须有明确 Owner

如果多个层级都以为“自己应该继续”，很容易出现重复控制。

例如：

```text
SDK 自动 retry Tool
Harness 也 retry
Model 看到 error 后又 retry
Workflow Engine 再 retry 整个 node
```

一次失败最终可能被执行：

```text
3 × 3 × 3 = 27 次
```

因此每个循环都应该明确：

```text
loop_owner
retry_owner
budget_owner
state_owner
termination_owner
```

原则是：

> **同一种 failure semantics 最好只有一个主要控制层负责。**

---

#### 7.2.47 Subagent 不是“再开一个无限 Loop”

主 Agent 委托子 Agent 时，应该给子 run 明确 contract：

```text
subgoal
input state
allowed capabilities
budget
deadline
return schema
stop condition
```

主 Agent Loop 还要决定：

```text
spawn 后是 WAIT 还是继续做别的？
是否允许多个 subagent 并发？
何时 cancel？
结果回来后怎样 merge？
子 Agent 是否允许再次递归 delegation？
```

所以：

> **Delegation 会创建新的 run lifecycle，而不是把控制责任消失掉。**

---

#### 7.2.48 Parallel Action 需要 Join Policy

如果模型一次提出多个独立 Tool Call：

```text
search source A
search source B
search source C
```

Loop Policy 可以允许并行。

但并行之后必须定义：

```text
wait_all?
first_success?
quorum?
minimum_evidence?
timeout_partial_merge?
cancel_remaining?
```

例如：

```text
3 个搜索中 2 个已经返回充分证据
```

系统未必需要继续等第三个慢查询。

因此：

> **Concurrency Policy 不只是“能否并行”，还包括何时认为并行阶段已经足够完成。**

---

#### 7.2.49 Cancellation 是一等 Transition

用户可能说：

```text
停一下。
不用继续了。
不要发送。
```

或者上游系统撤销任务。

Loop Policy 必须能从：

```text
RUNNING / WAITING / EXECUTING
```

进入：

```text
CANCELLING
→ CANCELLED
```

如果存在正在执行的副作用，还需要判断：

```text
能否真正取消？
已经执行到什么程度？
是否需要 reconcile？
是否需要 compensation？
```

所以 cancellation 不是简单 `break`。

---

#### 7.2.50 User Interrupt 可能是新指令，也可能是控制事件

长任务中用户的新消息可能表示：

```text
补充信息
修改目标
暂停
取消
提高优先级
缩小范围
批准 action
拒绝 action
```

Loop Policy 应先分类这个 event 的控制语义，再决定是否把它直接放进下一次模型 context。

例如：

```text
“不要发送邮件”
```

首先是：

```text
cancel / revoke pending side effect
```

然后才是 conversational context。

因此：

> **User message 既可能是 content，也可能是 runtime control event。**

---

#### 7.2.51 Model 声称“完成”只是 Completion Proposal

模型输出：

```text
Done.
```

本质上只是：

```text
completion_proposal = true
```

Harness 仍应判断：

```text
required artifacts exist?
acceptance criteria satisfied?
pending actions cleared?
required verification passed?
mandatory approvals completed?
open blockers remain?
```

因此：

```text
Model says done
        ≠
Run is terminal-success
```

---

#### 7.2.52 Terminal State 不应只有 success / error

实际系统至少应该区分：

| Terminal State | 含义 |
|---|---|
| `SUCCEEDED` | 验收条件满足 |
| `FAILED` | 已发生无法恢复的失败 |
| `BLOCKED` | 当前缺少不可自行解决的条件 |
| `CANCELLED` | 被用户或上游主动取消 |
| `TIMED_OUT` | 超过时间限制 |
| `BUDGET_EXHAUSTED` | 达到计算 / 成本硬上限 |
| `PARTIAL` | 明确允许部分交付，且记录未完成项 |

这样 observability 才能回答：

```text
为什么停？
```

而不是所有情况都显示：

```text
Agent stopped
```

---

#### 7.2.53 一个 Research Agent 的 Loop 应该怎样走

用户要求：

```text
调研某技术路线，并给出证据支持的结论。
```

一个合理 Loop 可能是：

```text
READY
↓
CALL_MODEL：识别关键问题与证据缺口
↓
EXECUTE：并行搜索多个来源
↓
OBSERVE：收集结果
↓
VERIFY：来源是否足够独立 / 权威 / 新鲜
↓
CONTINUE：存在关键证据缺口
↓
CALL_MODEL：决定下一轮针对性检索
↓
EXECUTE
↓
OBSERVE
↓
NO-PROGRESS CHECK：边际新信息已经很低
↓
VERIFY：关键主张是否都有证据
↓
STOP → SUCCEEDED
```

这里不应该是：

```text
搜索 10 次，因为 max_searches = 10
```

而应该围绕：

```text
Evidence Gap
Information Gain
Verification Coverage
```

推进。

---

#### 7.2.54 一个 Coding Agent 的 Loop 应该怎样走

任务：

```text
修复一个测试失败的 bug。
```

合理轨迹可能是：

```text
read failure
↓
CALL_MODEL：形成局部假设
↓
inspect code
↓
CALL_MODEL：提出 patch
↓
apply patch
↓
run targeted test
↓
OBSERVE failure
↓
new evidence changes diagnosis
↓
CALL_MODEL：修正假设
↓
apply second patch
↓
run targeted test
↓
VERIFY pass
↓
run broader regression tests
↓
VERIFY pass
↓
STOP
```

这里：

```text
测试
```

既是 Tool Action，也是下一轮的重要 feedback source。

如果测试正在跑，则应该：

```text
WAIT_FOR_TEST
```

而不是继续让模型猜测试结果。

---

#### 7.2.55 一个 Approval-heavy Agent 的 Loop 应该怎样走

任务：

```text
根据发票创建并提交报销。
```

可能流程：

```text
extract invoice
↓
validate fields
↓
CALL_MODEL：处理语义歧义
↓
prepare expense draft
↓
VERIFY：金额 / 类别 / 收款方
↓
approval required
↓
WAITING_FOR_APPROVAL
↓
SUSPEND

[human approves]
↓
RESUME
↓
re-check current state
↓
submit expense
↓
read-after-write verification
↓
STOP
```

审批等待期间继续 call model 没有任何价值。

---

#### 7.2.56 一个 Long-running Agent 为什么必须把“等待”从“推理”里拆出来

假设任务跨度两天：

```text
Day 1：提交云端构建
Day 2：构建结果返回
```

如果系统把 Agent 理解成持续的模型会话，就会遇到：

- context 不断增长；
- worker 被无意义占用；
- 模型反复查询同一状态；
- restart 后难以恢复；
- 成本与 wall time 强耦合。

更好的结构是：

```text
Active Compute
→ checkpoint
→ suspend
→ external event
→ resume
→ Active Compute
```

所以：

> **长时间运行的是 Run State，不一定是模型进程。**

---

#### 7.2.57 Anti-pattern：while True + call_model

最典型反模式：

```python
while True:
    response = model(history)
    if response.tool_call:
        result = tool(response.tool_call)
        history.append(result)
    else:
        break
```

它适合最小 demo，但生产系统如果直接停在这里，会缺少：

```text
waiting state
pending action
approval gate
progress detection
reconciliation
budget dimensions
explicit verification
cancellation
recovery state
structured terminal reason
```

所以：

> **Demo Loop 可以 model-driven；生产 Loop 应 state-driven。**

---

#### 7.2.58 Anti-pattern：让模型自己决定所有继续 / 停止

如果系统 prompt 只写：

```text
继续工作直到完成。
```

会出现两类对称风险。

##### Premature Stop

模型过早认为：

```text
差不多完成了。
```

##### Overrun

模型不断：

```text
再查一点
再想一下
再优化一次
```

因此：

> **Semantic autonomy 可以交给模型；lifecycle authority 不能完全交给模型。**

---

#### 7.2.59 Anti-pattern：每个 Error 都重新问模型

例如：

```text
HTTP 429
→ LLM: “我该怎么办？”
```

这是典型浪费。

更合理的是：

```text
known transient error
→ retry policy

retry exhausted / non-retryable
→ expose structured observation
→ semantic decision if needed
```

这样不仅省 token，也减少模型在机械系统问题上的不稳定行为。

---

#### 7.2.60 Anti-pattern：只有 max_steps，没有 Progress Policy

`max_steps` 能防止无限消耗，但无法回答：

```text
为什么继续？
为什么现在停？
第几步开始已经没有价值？
```

所以：

```text
Hard Guard
+
Progress Signal
+
No-progress Detection
+
Transition Reason
```

应该同时存在。

---

#### 7.2.61 Anti-pattern：把 WAIT 当成“再思考一下”

如果当前真正缺少的是：

```text
用户账户 ID
审批结果
异步任务输出
外部系统恢复
```

继续思考不会创造这些事实。

所以：

> **当 uncertainty 来自缺失 observation，而不是推理不足时，正确动作通常是获取信息或 WAIT，而不是延长 reasoning。**

---

#### 7.2.62 Loop Trace 至少应该记录什么

为了能够 Debug / Eval / Replay，一个 transition trace 至少应包含：

```text
run_id
transition_id
state_before
transition_type
transition_reason
actor
model_call_id / action_id
observation_id
state_after
progress_delta
budget_before / after
pending_actions
verification_status
wait_reason
terminal_reason
parent / branch id
timestamp / latency
```

这样才能回答：

```text
为什么这时又调用了一次模型？
为什么这里没有停？
为什么等了 30 分钟？
为什么同一个 Tool 执行了两次？
为什么进入了 branch？
哪一步开始没有 progress？
```

---

#### 7.2.63 Loop Policy 应该怎样评估

不能只看最终任务成功率。

至少可以看：

##### Task Outcome

```text
success rate
verified success rate
partial / blocked / failed rate
```

##### Efficiency

```text
model calls per success
tokens per success
tool calls per success
wall time
cost
```

##### Loop Quality

```text
no-progress turns
repeated-action rate
repeated-state rate
oscillation rate
unnecessary model-call rate
premature-stop rate
overrun rate
```

##### Waiting / Resume Quality

```text
busy-wait rate
resume correctness
duplicate side-effect rate
stale-state rate
```

##### Verification Quality

```text
false completion rate
verification coverage
post-stop defect rate
```

最终目标是：

> **用尽可能少的无效 transition，取得可验证的任务进展。**

---

#### 7.2.64 Loop Eval 应该看 Trajectory，而不是只看 Final Answer

两个 Agent 最终都成功：

```text
Agent A：8 transitions，1 次 verify，无重复 action
Agent B：43 transitions，重复搜索 12 次，重试 9 次，最后碰巧成功
```

Final Accuracy 看起来一样。

但 Loop Quality 完全不同。

因此评测应保留：

```text
State Sequence
Transition Sequence
Action Sequence
Observation Sequence
Progress Sequence
Budget Consumption
Terminal Reason
```

这也是为什么 Chapter 9 的 Observability & Evaluation 必须与 Harness trace 接起来。

---

#### 7.2.65 面试时最容易被追问的 Loop Policy 问题

至少应该能回答：

1. **谁真正驱动一次 Agent run？**  
   Harness / Runner 驱动；模型只在需要语义决策时被调用。

2. **Tool 返回以后为什么不一定立刻再调模型？**  
   因为可能需要 deterministic validation、verification、等待异步完成或直接执行固定 transition。

3. **WAIT 和 STOP 有什么区别？**  
   WAIT 是非终止状态，等待外部 event；STOP 进入 terminal state。

4. **怎样避免 Agent 无限循环？**  
   不只靠 max turns，还要有 repeated action/state、no-progress、oscillation、retry ceiling、多维 budget 与 terminal checks。

5. **模型说 Done 为什么不一定结束？**  
   Done 只是 completion proposal，系统还需要验证验收条件与真实环境状态。

6. **什么时候应该 Branch？**  
   当多个候选路径有足够探索价值，且预期收益大于额外成本与 merge 风险。

7. **什么时候不应该再调用模型？**  
   当 transition 可以由可靠的 deterministic logic 完成，或系统正在等待外部信息。

8. **长任务为什么不应该一直保持 LLM 会话活跃？**  
   Run State 可以持久化并 suspend/resume，长时间存在不等于持续模型推理。

---

#### 7.2.66 一个 30 秒面试回答

如果面试官问：

> **Agent Loop Policy 是什么？**

可以回答：

> Agent Loop Policy 是 Harness 中控制一次 Agent run 如何推进的策略。它不只是“模型输出 Tool Call 就执行，再把结果喂回模型”，而是根据当前 state、最新 observation、pending action、verification 状态、budget、权限和外部 event，决定下一次 transition 是 call model、execute、verify、wait、branch、recover 还是 stop。可靠 Loop 还需要区分 waiting 与 terminal，检测 repeated action、repeated state、oscillation 和 no-progress，并用 max turns、cost、time、retry、branch 等多维 budget 做 hard guard。核心原则是：**Model proposes the next move; the Harness owns the lifecycle.**

---

#### 7.2.67 7.2 与 Chapter 7 后续 Policy 的接口

7.2 不应该把后面所有内容提前写完。

边界可以固定成：

```text
7.2 Agent Loop Policy
    → run 何时推进、暂停、验证、分支、恢复或停止

7.3 Instruction Policy
    → 当前决策受哪些指令约束

7.4 Context Policy
    → 每次 model call 看什么

7.5 Tool Policy
    → Tool 何时可见、可调、可执行

7.6 Memory Policy
    → 什么状态进入长期 / 短期记忆

7.7 Planning Policy
    → 何时规划、怎样规划、何时重规划

7.8 Model Routing Policy
    → 当前 transition 使用哪个模型 / 配置

7.9 Permission / Approval Policy
    → action 是否拥有执行 authority

7.10 Termination Policy
    → 什么条件构成真正 terminal state

7.11 Recovery Policy
    → failure / interruption 后如何恢复
```

7.2 是这些 Policy 的**运行时交通规则**：

> 它不定义所有局部规则，但决定在什么状态下调用哪一种规则。

---

#### 7.2.68 Loop Policy 设计检查表

设计一个 Agent run 时，可以检查：

##### Driver

- 谁拥有 run lifecycle？
- 谁决定下一次 model call？

##### State

- running / waiting / terminal 是否显式区分？
- pending action 是否是一等状态？

##### Transition

- 哪些 transition 是 deterministic？
- 哪些真的需要 semantic model decision？

##### Waiting

- 缺外部事件时能否 suspend？
- event 到来后如何 resume / reconcile？

##### Progress

- 什么算真实进展？
- 如何检测 no-progress / repetition / oscillation？

##### Budget

- model / tool / retry / branch / cost / time 是否分别计数？
- 是否存在 hard guard？

##### Verification

- action completion 与 goal completion 是否分开？
- Model 的 Done 是否需要外部验证？

##### Termination

- success / failed / blocked / cancelled / timeout 是否区分？

##### Observability

- 每个 transition 是否记录 reason？
- 能否解释为什么继续、等待或停止？

---

#### 7.2.69 Loop Policy 的长期稳定原则

这一节最值得长期记住的不是某个框架 API，而是下面这些原则。

1. **The Harness drives the run.**  
   模型提供语义决策能力，但不独占生命周期控制权。

2. **Model Call is a transition, not a heartbeat.**  
   只有需要新的语义判断时才调用模型。

3. **State-driven > model-call-driven.**  
   Loop 应根据 State 与 Event 推进，而不是根据“模型还愿不愿意继续”。

4. **Event-driven > busy-loop.**  
   等待外部信息时应 suspend，而不是空转推理。

5. **Pending is a real state.**  
   已提交未完成的 action 必须被显式建模。

6. **Iteration ≠ Progress.**  
   计算发生不代表任务状态改善。

7. **More thinking ≠ more progress.**  
   没有新证据、约束或 verifier feedback 时，反复 reflection 可能只是 semantic loop。

8. **Deterministic logic should stay deterministic.**  
   schema check、retry、权限、deadline 等能由程序处理的，不应无意义升级为 LLM 决策。

9. **Verification is a first-class transition.**  
   执行动作成功不等于目标已经完成。

10. **Model completion is a proposal, not authority.**  
    `Done` 必须与真实验收条件对齐。

11. **Every loop needs hard guards.**  
    max turns、time、cost、retry、branch 等上限用于控制最坏情况。

12. **Progress guards are stronger than step guards.**  
    no-progress、repetition、oscillation 能更早识别无效运行。

13. **Long-running state does not require continuously running inference.**  
    长任务应支持 checkpoint、suspend、resume。

14. **Nested loops need explicit ownership.**  
    SDK、Harness、Workflow、Tool retry 不能层层重复控制同一失败。

15. **Lifecycle authority must respect safety and system invariants.**  
    Goal pursuit 永远不能越过权限、风险与一致性边界。

---

#### 7.2.70 一句话总结

> **Agent Loop Policy 的本质，是让一次 Agent run 按 State、Observation、Event、Budget 与 Policy 受控推进：需要语义判断时才调用模型，需要真实反馈时执行并观察，需要外部条件时等待并挂起，需要证明时验证，需要探索时有限分支，检测到重复、振荡或无进展时改变策略，并在满足明确终止条件后停止；可靠 Agent 不是“能一直想下去”，而是知道什么时候该继续、该等、该查、该验、该换路，以及什么时候必须停。**

---

#### 7.2.71 参考资料

1. OpenAI. *Agents SDK — Running agents / Runner*. Runner 显式管理 agent loop：模型调用后根据 final output、handoff 或 tool call 决定后续 transition，并提供 `max_turns`、RunState 恢复、tool execution 与 lifecycle hooks 等机制。
2. OpenAI. *Agents SDK — Runner Reference*. 将一次 turn 定义为一次 AI invocation，并显式区分 final output、handoff、tool execution 与 `MaxTurnsExceeded`，说明 model invocation 只是 run lifecycle 中的一类步骤。
3. Anthropic. *Building effective agents*（2024）. 区分 workflow 与 agent，并把 Agent 描述为根据环境反馈动态控制自身 process / tool usage 的系统；强调从简单、可组合模式开始，而不是无条件增加 agentic complexity。
4. Anthropic. *Effective harnesses for long-running agents*（2025）. 讨论长时 Agent 如何跨多个 context window 持续取得增量进展，并通过结构化 artifacts 与 session handoff 维持任务连续性。
5. Anthropic. *Harness design for long-running application development*（2026）. 进一步讨论长任务中的 context reset、结构化 handoff、generator / evaluator 分离，以及 naive continuous iteration 在长时任务中的失稳问题。
6. Anthropic. *Long-running Claude for scientific computing*（2026）. 展示 Ralph-style repeated-agent loop，同时通过最大迭代次数和成功条件限制持续运行，说明“继续迭代”仍需要外部 guard。
7. LangChain / LangGraph. *Thinking in LangGraph*. 将 Agent 建模为显式 State、Node 与 Transition，并区分 LLM step、data step、action step、human-input step；同时展示 retry、interrupt、checkpointer、pause / resume 与不同 failure semantics 的处理方式。
8. Yao S, Zhao J, Yu D, et al. *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 提出 reasoning 与 action / observation 交错的经典 Agent loop 形式，为后续环境反馈驱动的 Agent 设计提供基础范式。

---

