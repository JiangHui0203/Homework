### 7.1 What is an Agent Harness?

#### 7.1.1 Agent Harness 到底是什么

**Agent Harness** 是围绕模型建立的一层**运行时控制系统（runtime control system / control plane）**：它把一次次模型调用、上下文构造、能力暴露、工具执行、状态更新、权限判断、人工审批、终止与恢复组织成一个可持续运行、可观察、可约束的 Agent loop。

最短定义可以写成：

> **Model 负责提出下一步；Harness 负责决定模型在什么状态下被调用、能看到什么、能做什么、什么时候执行、什么时候停止，以及失败后如何继续。**

因此，一个 Agent 不应被理解为：

```text
Agent = LLM + Prompt
```

而更接近：

```text
Agent System
=
Model
+ Harness
+ Capabilities
+ Runtime / Environment
+ State / Persistence
+ Policy / Governance
+ Observability
```

其中 Harness 是把这些部分连接成**闭环控制系统**的那一层。

---

#### 7.1.2 为什么“有一个强模型”仍然不等于“有一个 Agent”

一个模型即使能够：

- reasoning；
- function calling；
- 生成代码；
- 识别下一步行动；
- 使用长上下文；

也仍然只是在给定输入条件下产生输出。

真正的 Agent 还需要系统回答：

```text
下一次什么时候调用模型？
当前 state 是什么？
哪些 observation 应该进入 context？
哪些 tool 当前可见？
某个 action 是否允许执行？
高风险操作是否需要审批？
工具 timeout 后应该 retry 还是 reconcile？
什么时候认为任务已经完成？
失败后从哪里恢复？
长任务如何 pause / resume？
```

这些都不是“模型本身会不会推理”能够自动解决的。

因此：

> **Agent capability 不只来自 Model capability，也来自 Harness quality。**

---

#### 7.1.3 Harness 的核心问题不是“模型能不能”，而是“系统允许模型怎样持续行动”

可以把模型能力问题写成：

```text
Can the model decide X?
```

而 Harness 问题更接近：

```text
When should the model decide X?
What state should it see?
What actions may it choose?
Which action requires approval?
How is the action executed?
How is the result converted into observation?
How does execution change system state?
When should the loop continue or stop?
```

所以 Harness 研究的是：

> **Model intelligence 如何被变成受控、持续、可恢复的 system behavior。**

---

#### 7.1.4 Harness 在整套 Agent 架构中的位置

可以先用一张最小图理解：

```text
                 User / Upstream System
                          │
                          ↓
                ┌──────────────────┐
                │     Harness      │
                │                  │
                │ state / context  │
                │ policy / loop    │
                │ approval / stop  │
                │ recovery / trace │
                └───────┬──────────┘
                        │
                  Model Call
                        ↓
                ┌──────────────────┐
                │      Model       │
                └───────┬──────────┘
                        │
                 Proposed Action
                        ↓
                ┌──────────────────┐
                │     Harness      │
                │ validate / gate  │
                │ route / record   │
                └───────┬──────────┘
                        ↓
                ┌──────────────────┐
                │ Runtime / Env    │
                │ tools / compute  │
                │ files / services │
                └───────┬──────────┘
                        ↓
                   Raw Result
                        │
                        └────→ Harness → Observation → State → next Model Call
```

因此 Harness 处在：

```text
Application / User
        ↕
     Harness
   ↙    ↓    ↘
Model  State  Runtime
        ↕
   Tools / Memory / Subagents / External Systems
```

它不是所有组件本身，而是这些组件之间的**控制与协调层**。

---

#### 7.1.5 Model ≠ Harness

这是第一条必须严格区分的边界。

**Model** 主要提供：

- next-token generation；
- reasoning；
- semantic understanding；
- action proposal；
- structured output generation。

**Harness** 主要负责：

- model invocation；
- state lifecycle；
- context assembly；
- capability exposure；
- action validation；
- execution routing；
- approval gates；
- observation construction；
- retry / recovery；
- stop conditions；
- tracing / accounting。

可以记成：

```text
Model   = decision intelligence
Harness = decision control system
```

模型变强，并不会自动消除 Harness 问题。

---

#### 7.1.6 Harness ≠ Runtime

这是 Chapter 7 与 Chapter 8 最重要的边界之一。

Harness 主要回答：

```text
Should we do it?
What should happen next?
Under what policy?
With what state?
```

Runtime 主要回答：

```text
How is it actually executed?
Where does it run?
How are processes, files, network and resources managed?
```

例如模型提出：

```text
run_tests()
```

Harness 可能负责：

```text
检查该工具是否可见
验证参数
检查预算
检查权限
决定是否执行
记录 action_id
```

Runtime 则负责：

```text
启动进程
分配 CPU / memory
执行命令
捕获 stdout / stderr
处理 timeout
返回 execution result
```

因此：

> **Harness = control logic；Runtime = execution substrate。**

---

#### 7.1.7 Harness ≠ Sandbox / Environment

Sandbox 是一个**执行边界**。

它可以提供：

- filesystem；
- shell；
- packages；
- process isolation；
- network policy；
- resource limits；
- snapshots。

Harness 则决定：

- 是否需要进入 sandbox；
- 允许模型调用什么；
- 哪些文件被暴露；
- 哪些命令需要 approval；
- 结果如何进入 observation；
- 任务是否继续。

所以：

```text
Harness ≠ Sandbox
Control Plane ≠ Execution Plane
```

把 Harness 全部塞进模型可写、可执行的 sandbox 中，也意味着把一部分可信控制逻辑与模型驱动的执行面放进同一个 trust boundary，生产系统需要明确评估这种耦合。

---

#### 7.1.8 Harness ≠ Tool

Tool 是一种能力：

```text
search_web
send_email
read_file
execute_sql
run_shell
```

Harness 负责决定工具**如何被使用**：

```text
哪些 Tool 当前可见？
谁有权调用？
参数是否合法？
哪些 Tool 需要审批？
是否允许并行？
失败后是否重试？
结果如何裁剪？
副作用如何确认？
```

因此沿用前面的核心边界：

```text
Tool        = Capability
Tool Policy = Harness
```

---

#### 7.1.9 Harness ≠ Memory

Memory 是可被写入、保存、检索、更新和遗忘的信息能力。

Harness 决定的是：

```text
什么时候写？
写什么？
保存多久？
什么时候检索？
检索结果如何进入 context？
冲突信息如何处理？
哪些 memory 不能向当前任务暴露？
```

因此：

```text
Memory        = Capability / State Resource
Memory Policy = Harness
```

Memory 存在，并不意味着 Agent 已经拥有可靠的 memory behavior。

---

#### 7.1.10 Harness ≠ Subagent

Subagent 是另一个可承担任务的 agentic capability。

Harness 决定：

- 是否 delegation；
- delegation 给谁；
- 给多少 context；
- 权限是否继承；
- 如何等待与汇总；
- 是否允许递归 delegation；
- 如何处理冲突结果；
- 何时取消子任务。

所以：

```text
Subagent        = Capability
Subagent Policy = Harness
```

多 Agent 系统中，Harness 还是**协调规则真正落地的位置之一**。

---

#### 7.1.11 Harness ≠ Prompt / System Instruction

Prompt 可以表达行为要求，例如：

```text
不要删除文件。
```

但如果 `delete_file` 仍然被暴露且执行层无阻断，那么这仍然只是模型可见的语言约束。

Harness 可以实施：

```text
if action == delete_file:
    require_approval()
```

甚至：

```text
deny capability entirely
```

因此：

> **Instruction 约束模型行为倾向；Harness policy 约束系统可执行行为。**

二者可以配合，但不能互相替代。

---

#### 7.1.12 Harness ≠ Agent Framework / SDK

Framework 或 SDK 是开发者用来构建 Agent 的软件工具。

它可能提供：

- Agent class；
- tool decorator；
- runner；
- tracing；
- state store；
- handoff primitives；
- guardrails；
- sandbox adapter。

Harness 则是**实际运行中的控制逻辑及其策略**。

因此：

```text
Framework / SDK = implementation vehicle
Harness         = runtime control semantics
```

同一个 Harness 设计可以用不同框架实现；同一个框架也可以被配置成完全不同的 Harness behavior。

---

#### 7.1.13 Harness ≠ Workflow Engine

Workflow Engine 更擅长表达：

```text
A → B → C
if X → D
retry 3 times
wait for event
```

Harness 则需要围绕**模型驱动的动态决策**管理：

```text
State → Model Decision → Action → Observation → State Update
```

两者可以组合：

```text
Deterministic Workflow
        ↓
Agentic Decision Node
        ↓
Harness-managed Agent Loop
        ↓
Return structured result
        ↓
Deterministic Workflow
```

所以成熟系统通常不是“workflow 或 agent 二选一”，而是：

> **用 workflow 固定确定性骨架，用 Harness 管理真正需要自治决策的部分。**

---

#### 7.1.14 Harness ≠ Orchestrator，但二者有重叠

Orchestrator 通常强调：

- 任务调度；
- 依赖关系；
- worker / agent routing；
- 并发；
- 生命周期协调。

Harness 更强调围绕 Agent decision loop 的：

- model invocation；
- context；
- capabilities；
- policy；
- approvals；
- recovery；
- termination。

在具体产品中，一个组件可能同时承担两者，因此名称可以重叠；但分析系统时应按**职责**而不是按类名判断。

---

#### 7.1.15 Capability ≠ Policy：Chapter 7 的总边界

前面的章节主要回答：

```text
Agent 有什么能力？
```

Chapter 7 开始回答：

```text
这些能力在什么时候、以什么规则、对谁、在什么状态下被使用？
```

因此可以建立总表：

| Capability / Resource | Harness Policy |
|---|---|
| Tool | Tool Policy |
| Memory | Memory Policy |
| Context Sources | Context Policy |
| Planning | Planning Policy |
| Subagent | Subagent Policy |
| Human Approval | Permission / Approval Policy |
| Model Invocation | Agent Loop Policy |
| Stop / Completion Signal | Termination Policy |
| Retry / Checkpoint / Resume | Recovery Policy |

最值得记住的是：

> **拥有 Capability，不等于系统拥有正确使用 Capability 的策略。**

---

#### 7.1.16 Autonomy ≠ Authority

模型可以有很强的 autonomy：

```text
自主判断下一步做什么
自主选择工具
自主拆任务
自主请求子 Agent
```

但它不应该因此自动拥有同等强度的 execution authority。

例如：

```text
Model may propose:
    transfer $10000

Harness may require:
    explicit human approval
```

所以：

```text
Model Autonomy
      ≠
Execution Authority
```

Harness 的核心职责之一，就是把这两者分开。

---

#### 7.1.17 Harness 可以理解为 Agent 的 Control Plane

在系统工程中，可以把 Agent 系统粗略拆成：

```text
Control Plane
    ↓
决定策略、权限、状态、路由、生命周期

Execution Plane
    ↓
真正运行命令、访问文件、调用服务、改变环境
```

Agent Harness 通常主要处于 Control Plane。

它并不一定执行所有 action，但它应该知道：

- 为什么执行；
- 谁请求执行；
- 是否允许执行；
- 当前执行到了哪里；
- 返回了什么；
- 是否完成；
- 是否需要恢复。

---

#### 7.1.18 最小 Agent Harness 闭环

一个最小 Harness 可以抽象为：

```text
Initialize State
      ↓
Build Context
      ↓
Call Model
      ↓
Parse Decision
      ↓
Validate / Gate Action
      ↓
Execute or Delegate
      ↓
Receive Raw Result
      ↓
Construct Observation
      ↓
Update State
      ↓
Verify / Continue / Stop
      └───────────────↺
```

这个闭环比：

```python
while True:
    response = model(messages)
```

多出的，正是生产 Agent 最重要的系统语义。

---

#### 7.1.19 Harness 的输入不是只有 User Prompt

Harness 的真实输入可能包括：

```text
User Goal
System / Developer Instructions
Current Working State
Conversation State
Retrieved Evidence
Tool Registry
Permissions
Identity / Tenant
Budget
Deadline
Environment State
Pending Actions
Human Feedback
Previous Failures
Checkpoint
```

因此一次 model call 的 context 是 Harness 根据当前状态**构造出来的决策视图**，不是 Agent 系统全部真实状态的简单拼接。

---

#### 7.1.20 Harness 的输出也不是只有 Final Answer

Harness 运行过程中会产生：

- model calls；
- tool calls；
- approval requests；
- state transitions；
- checkpoints；
- events；
- artifacts；
- traces；
- final result；
- failure / cancellation state。

所以一个生产 Agent run 更像**有状态执行实例**，而不是一次聊天 completion。

---

#### 7.1.21 Harness 拥有 Model Invocation 的生命周期

Harness 必须知道：

```text
为什么现在需要调用模型？
使用哪个模型 / 配置？
给什么 context？
允许什么 tools？
输出必须满足什么 schema？
调用失败如何处理？
结果是否可以直接执行？
```

这意味着 Model Call 本身也是一种受策略管理的系统操作。

后续 7.2 Agent Loop Policy 会进一步展开这一点。

---

#### 7.1.22 Context Engineering 是 Harness 行为，而不是简单 Prompt 拼接

Context Policy 要决定：

```text
什么必须进入当前 context？
什么只保存在 durable state？
什么应该 retrieval-on-demand？
什么应该 summary？
什么应该保留原文？
哪些 observation 已过期？
哪些内容来自低信任源？
```

因此：

> **Context 是 Harness 为当前决策构造的 working view。**

这也解释了为什么前面的：

```text
Context ≠ Memory
Working State ≠ Conversation History
Retrieved ≠ Trusted
```

到 Harness 层会真正成为工程策略。

---

#### 7.1.23 Harness 管理的是 Model-visible Action Space

系统拥有 1000 个 Tool，并不意味着模型每次 inference 都应该看到 1000 个 Tool。

Harness 可以先经过：

```text
Capability Universe
      ↓
Identity / Tenant Filter
      ↓
Permission Filter
      ↓
Availability Filter
      ↓
Task Relevance / Retrieval
      ↓
Risk Filter
      ↓
Minimal Sufficient Capability Exposure
      ↓
Model-visible Action Space
```

因此 Capability Discovery 到最终 action execution 之间，需要 Harness 管理多个门。

---

#### 7.1.24 Harness 不应该把“模型提出 Action”等同于“系统批准 Action”

模型输出：

```json
{"tool": "delete_file", "path": "important.csv"}
```

只表示：

```text
Proposed Action
```

而不是：

```text
Authorized Action
```

中间至少可能存在：

```text
schema validation
permission check
risk classification
policy check
human approval
idempotency check
precondition verification
```

因此：

> **Action Intent ≠ Execution Authority。**

---

#### 7.1.25 Harness 负责把 Raw Result 变成 Observation

Tool 返回：

```text
200 OK
```

并不必然意味着：

```text
业务目标已完成
```

Harness 可能需要做：

```text
Raw Result
   ↓
Normalize
   ↓
Parse
   ↓
Validate
   ↓
Attach provenance / freshness
   ↓
Truncate / summarize when needed
   ↓
Construct Observation
   ↓
Update State
```

这延续前面的关键边界：

```text
Tool Result ≠ Observation ≠ Ground Truth
```

---

#### 7.1.26 Harness 负责保护 State Transition

一个 Agent run 不只是 messages 增长。

Harness 还要维护：

```text
current task state
accepted facts
pending actions
completed actions
artifacts
permissions
budget
checkpoint
retry count
subtask status
human approval state
```

因此：

> **Working State 应该是显式系统对象，而不是被隐式埋在聊天历史里。**

---

#### 7.1.27 Harness 决定何时继续 Loop

模型完成一次输出之后，系统可能：

```text
continue reasoning
execute tool
wait for event
ask user
request approval
spawn subagent
retry
recover
finish
fail
cancel
```

真正决定 run 是否继续的，是 Harness 的 control logic 与 policy，而不是“模型还愿不愿意继续说”。

---

#### 7.1.28 Harness 决定什么叫“完成”

模型说：

```text
Done.
```

不应该自动等价于：

```text
Task Success
```

系统可能还需要验证：

- required artifact 是否存在；
- side effect 是否真的发生；
- output schema 是否满足；
- tests 是否通过；
- 用户约束是否全部满足；
- 子任务是否全部收敛；
- 环境状态是否符合 postcondition。

因此：

```text
Model says done
      ≠
Harness accepts completion
      ≠
Task success in the environment
```

后续 7.10 Termination Policy 会专门展开。

---

#### 7.1.29 Harness 负责把失败变成“可恢复状态”

工具失败之后，最差的系统行为之一是：

```text
error → blindly retry
```

Harness 应该判断：

```text
失败发生在哪一层？
是否可重试？
是否已经产生副作用？
状态是否确定？
是否需要 reconcile？
是否需要换路径？
是否应该回滚？
是否需要人工介入？
```

所以 Recovery 不是一个 `try/except`，而是 Agent lifecycle 的一部分。

---

#### 7.1.30 Unknown 是 Harness 必须显式表示的状态

假设支付请求 timeout：

```text
request sent
   ↓
timeout
```

系统不能直接推断：

```text
payment failed
```

真实状态可能是：

```text
SUCCEEDED but response lost
FAILED before execution
PENDING
UNKNOWN
```

因此：

```text
Unknown ≠ False
Pending ≠ Failed
Action Success ≠ Task Success
```

Harness 必须让这些不确定状态进入显式 state machine，而不是让模型“猜一个最像的答案”。

---

#### 7.1.31 Harness 是 Side-effect Safety 的关键层

对纯读取 Tool：

```text
retry(search)
```

通常风险较低。

对不可逆 action：

```text
send_email
transfer_money
delete_resource
submit_order
publish_post
```

Harness 必须考虑：

- approval；
- idempotency；
- deduplication；
- precondition；
- postcondition；
- reconciliation；
- audit log。

因为：

> **Tool Output ≠ Side Effect。**

真正重要的是环境有没有被改变，以及改变是否符合意图。

---

#### 7.1.32 Harness 让 Human-in-the-loop 成为系统机制

人类介入不应只是：

```text
Agent 不会了 → 问用户
```

更成熟的 Harness 会明确区分：

```text
clarification
approval
exception handling
policy escalation
high-risk confirmation
quality review
ownership transfer
```

每一种都对应不同的 state transition。

因此 HITL 本质上也是 Harness policy 的一部分。

---

#### 7.1.33 Harness 是“最小权限”真正落地的位置之一

模型 prompt 中写：

```text
只访问必要数据
```

并不能建立真正的 least privilege。

Harness 可以在运行时控制：

```text
which tool
which account
which tenant
which file path
which database scope
which credential
which operation
for how long
```

所以权限设计不能只停留在自然语言 instruction。

---

#### 7.1.34 Harness 需要理解 Identity / Tenant / Principal

当 Agent 代表用户行动时，Harness 需要知道：

```text
Who is the user?
Who is the agent acting as?
Which organization / tenant?
Which credential is being used?
Which permission is delegated?
Which action must be attributed to whom?
```

否则系统很容易把：

```text
Model can access X
```

错误地变成：

```text
Every user can access X
```

这已经不是模型能力问题，而是控制平面的 identity failure。

---

#### 7.1.35 Harness 需要管理 Budget，而不是无限 Loop

自治系统如果没有预算，很容易出现：

```text
endless search
repeated tool calls
recursive delegation
retry storm
context explosion
cost explosion
```

Harness 可以管理：

- token budget；
- tool-call budget；
- wall-clock budget；
- monetary budget；
- recursion depth；
- parallelism；
- retry count。

所以：

> **Autonomy 必须有 resource envelope。**

---

#### 7.1.36 Harness 是 Long-running Agent 的连续性机制

长任务可能跨越：

- 多次 model call；
- 多个 context window；
- 多个进程；
- 多个 worker；
- 人工等待；
- 服务重启；
- 几小时甚至更长的外部任务。

因此 Harness 不能假设：

```text
one process = one task lifetime
```

它需要把任务状态从单次推理中解耦出来。

---

#### 7.1.37 Pause / Resume 是 Harness 生命周期语义

长任务常见：

```text
Running
  ↓
Waiting for Approval
  ↓
Paused
  ↓
Resume
  ↓
Running
```

如果系统只能：

```text
start → run → final answer
```

那么它很难支持真正的异步 agentic work。

Pause / Resume 需要：

- durable state；
- checkpoint；
- pending action identity；
- environment continuity or reconstruction；
- freshness revalidation。

---

#### 7.1.38 Checkpoint 不是“保存聊天记录”

Checkpoint 应该保存恢复所需的**最小充分状态**。

可能包括：

```text
task state
accepted outputs
artifact references
pending action IDs
subtask states
approval state
budget usage
environment snapshot reference
```

而不是简单地把全部 conversation dump 一份。

这延续：

> **Minimal Durable State。**

---

#### 7.1.39 Harness 必须区分 State Persistence 与 Context Reconstruction

恢复任务时：

```text
Persisted State
      ↓
Harness reconstructs current decision state
      ↓
Builds fresh context
      ↓
Model continues
```

不应该默认：

```text
把过去所有 token 原样塞回去
```

所以：

```text
Persistence ≠ Context
Resume ≠ Replay Entire Conversation
```

---

#### 7.1.40 Harness 还是并发控制的边界之一

当多个工具或 subagent 并行工作时，可能出现：

```text
A reads state v1
B updates to v2
A writes result based on v1
```

这就是 stale-state / write-conflict 问题。

Harness 需要与 Runtime / State Store 配合管理：

- task identity；
- version；
- dependency；
- cancellation；
- join；
- conflict detection；
- merge / reject policy。

“并行更多”并不自动意味着“更快更好”。

---

#### 7.1.41 Subagent Delegation 需要由 Harness 管理 Context Boundary

Delegation 时最容易犯的错误是：

```text
把主 Agent 的全部 context 原样复制给 Subagent
```

这会带来：

- context bloat；
- privacy leakage；
- stale assumptions；
- instruction conflict；
- unnecessary capability exposure。

更合理的是：

```text
Goal
+ relevant constraints
+ minimal evidence
+ required output contract
+ scoped permissions
```

即：

> **Minimal Sufficient Delegation Context。**

---

#### 7.1.42 Harness 管理的是“控制权转移”，不只是消息传递

Handoff / Delegation 不只是：

```text
send message to another agent
```

还涉及：

```text
Who owns the task now?
Who may act?
Who can terminate?
Who receives the result?
Who verifies it?
What happens on timeout?
```

因此 Multi-Agent 的 coordination invariants 最终必须在 Harness / Runtime 层有可执行语义。

---

#### 7.1.43 Harness 与 MCP / A2A 的关系

前面已经建立：

```text
MCP → Host-facing Capability Interoperability
A2A → Agent-to-Agent Interoperability
```

Harness 则决定这些协议暴露的能力**是否、何时、怎样进入当前 Agent loop**。

例如：

```text
MCP Server exposes tool
      ↓
Harness discovers + filters
      ↓
Model may see tool
      ↓
Model proposes call
      ↓
Harness checks policy
      ↓
Runtime executes
```

A2A 同理：

```text
Remote Agent discovered
      ↓
Harness decides whether delegation is appropriate
      ↓
Creates / tracks remote task
      ↓
Consumes events / artifacts
      ↓
Updates local state
```

所以：

> **Protocol 提供 interoperable interface；Harness 把 interface 变成受控行为。**

---
