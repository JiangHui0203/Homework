from pathlib import Path

path = Path("Agent_Knowledge_System.md")
text = path.read_text(encoding="utf-8")

old = "### 6.3 Subagents\n### 6.4 Communication"
assert text.count(old) == 1, f"expected one 6.3 placeholder, got {text.count(old)}"

section = r'''### 6.3 Subagents

#### 6.3.1 Subagent 到底是什么

在 Multi-Agent 系统里，**Subagent** 最容易被误解成“另一个 Agent”。

更准确地说：

> **Subagent 是在某个 Parent / Manager 的任务边界下，被委派一个局部目标，并拥有自己局部 Decision Loop 的 Agent 实例。**

它强调的不是“模型有几个”，而是一个明确的 **delegation relationship**：

```text
Parent Agent
    ↓ delegates bounded objective
Subagent
    ↓ executes local loop
Result / Evidence / Escalation
    ↑
Parent Agent
```

因此 Subagent 的核心关键词是：

```text
Delegated Goal
+ Local Autonomy
+ Bounded Context
+ Bounded Authority
+ Return Contract
```

---

#### 6.3.2 Subagent 不是一种模型类型

Subagent 可以：

- 与 Parent 使用同一个模型；
- 使用不同模型；
- 使用不同 System Prompt；
- 拥有不同 Tool Set；
- 拥有不同 Context Window；
- 运行在不同 Sandbox；
- 使用不同权限；
- 使用不同预算。

所以：

> **Subagent 是运行时角色与控制关系，不是模型架构分类。**

---

#### 6.3.3 Subagent 的本质是“局部闭环”

普通 Tool 往往是一次受控调用：

```text
Input → Function / API → Output
```

Subagent 则通常拥有局部闭环：

```text
Observe
  ↓
Reason / Plan
  ↓
Act / Tool Use
  ↓
Observe Again
  ↓
Stop / Escalate / Return
```

也就是说，它可以在 Parent 不逐步指定每一步的情况下，自己完成一个 bounded subtask。

---

#### 6.3.4 Subagent 与普通 Tool 的边界

如果一个组件：

```text
输入确定
→ 操作路径确定
→ 输出结构确定
```

更像 Tool / Workflow。

如果它需要：

```text
根据中间 Observation 动态决定下一步
```

才更像 Subagent。

因此：

> **不要因为“这个 Tool 背后也调用了 LLM”就把它自动归类为 Subagent。**

是否有独立的局部 Decision Loop，比是否调用 LLM 更关键。

---

#### 6.3.5 Subagent 与 Agents-as-Tools

在 Manager-style orchestration 中，一个 Specialist Agent 常被暴露成 Tool。

```text
Manager
  ├─ call Research Agent as Tool
  ├─ call Analysis Agent as Tool
  └─ combine results
```

从 Parent 的视角看：

```text
调用方式像 Tool
执行主体是 Agent
```

这正是 Agents-as-Tools。

这里最重要的是：

> **Parent 仍保留顶层 Control Ownership。**

---

#### 6.3.6 Subagent 与 Handoff 不一样

Handoff 的核心是：

```text
Control Ownership Transfer
```

而典型 Subagent delegation 更常见的是：

```text
Parent retains top-level control
Subagent owns local execution
```

因此：

```text
Subagent delegation ≠ Handoff
```

一个 Agent 可以既被当作 Subagent 调用，也可以成为 Handoff Target；区别不在 Agent 本体，而在 **这一次控制权如何分配**。

---

#### 6.3.7 Execution Ownership 与 Control Ownership 必须区分

这是理解 Subagent 最重要的边界之一。

例如：

```text
Parent:
  决定要不要委派
  决定预算
  决定是否接受结果
  决定下一步

Subagent:
  决定局部任务内部怎么做
```

因此可以说：

```text
Parent owns global control
Subagent owns local execution
```

---

#### 6.3.8 Parent 仍然承担顶层责任

“我把任务交给 Subagent 了”不能成为责任转移机制。

Parent 至少仍要负责：

- 是否应该委派；
- 委派给谁；
- 给了什么 Context；
- 给了什么 Authority；
- 是否需要 Verification；
- 是否接受返回结果；
- 是否继续产生 Side Effect。

> **Delegation 可以转移执行，不应隐式转移 Accountability。**

---

#### 6.3.9 为什么需要 Subagent：Specialization

最直接的价值是角色专门化。

例如：

```text
Parent: general task manager
Subagent A: code review
Subagent B: security analysis
Subagent C: documentation synthesis
```

不同 Subagent 可以拥有：

- 不同 Prompt；
- 不同 Domain Context；
- 不同 Tools；
- 不同 Output Schema；
- 不同 Verification Criteria。

---

#### 6.3.10 为什么需要 Subagent：Context Isolation

一个长任务常见的问题不是“模型不会”，而是：

```text
所有历史
+ 所有搜索结果
+ 所有工具输出
+ 所有中间草稿
```

全部堆进同一个 Context。

Subagent 可以把某个局部任务放进独立 Context：

```text
Parent Context
    ↓ minimal sufficient delegation context
Subagent Context
    ↓ compressed result / evidence
Parent Context
```

这是一种 **Context Boundary**。

---

#### 6.3.11 Context Isolation 不等于 Information Isolation

Subagent 不是“什么都不知道”。

正确目标是：

> **只隔离无关信息，不隔离完成任务所需的信息。**

如果 Parent 为了“保持 Context 干净”而漏掉关键约束，Subagent 只会更稳定地做错事。

---

#### 6.3.12 为什么需要 Subagent：Parallel Investigation

当多个子任务近似独立时，可以：

```text
             ┌→ Subagent A
Parent ──────┼→ Subagent B
             └→ Subagent C
                  ↓
                Join
```

典型场景：

- 多个代码模块并行检查；
- 多个信息源并行检索；
- 多个假设并行验证；
- 多个候选方案并行分析。

这里优化的是 **Critical-path Latency**，不一定降低 Total Compute。

---

#### 6.3.13 为什么需要 Subagent：Failure Isolation

局部 Agent 的失败可以被封装为：

```text
status = failed
error = ...
evidence = ...
retryable = true / false
```

而不是直接污染整个 Parent 的状态。

这让系统更容易：

- 重试；
- 替换 Worker；
- 降级；
- 跳过非关键分支；
- 做 Failure Localization。

---

#### 6.3.14 为什么需要 Subagent：Authority Isolation

不同子任务不需要相同权限。

例如：

```text
Research Subagent: read-only web / file access
Reviewer Subagent: read repository, no write
Execution Subagent: narrow write permission
Payment Subagent: no arbitrary network access
```

因此 Subagent 也是一种 **Least-Privilege Boundary**。

---

#### 6.3.15 为什么需要 Subagent：Ephemeral Autonomy

很多任务只需要一个临时 Specialist：

```text
spawn
→ execute bounded task
→ report
→ terminate
```

不需要把它升级成长期存在、长期有 Memory、长期占据系统角色的 Peer Agent。

> **Temporary problem usually deserves temporary autonomy.**

---

#### 6.3.16 什么时候不应该创建 Subagent

如果任务只是：

```text
格式转换
固定 API 调用
确定性规则检查
一次数据库查询
简单文件读取
```

优先使用 Tool / Function / Workflow。

如果 Parent 自己完成只需极少步骤，也没有明显的 specialization、isolation 或 parallelism 收益，那么拆 Subagent 往往只增加 coordination tax。

---

#### 6.3.17 Coordination Tax

每增加一个 Subagent，系统至少多出：

```text
任务描述成本
Context Transfer 成本
调度成本
模型调用成本
等待成本
结果聚合成本
验证成本
Trace 成本
失败恢复成本
```

因此决策不应该是：

```text
Can I use a subagent?
```

而应该是：

```text
Does the benefit exceed the coordination tax?
```

---

#### 6.3.18 Minimum Sufficient Subagent

延续上一节的 Minimum Sufficient Orchestration：

> **只在一个局部问题确实需要独立 Decision Loop 时，才创建 Subagent。**

能用 Tool 的，不拆 Agent；
能用确定性 Workflow 的，不制造自主决策；
能在 Parent Context 内稳定完成的，不为了“架构高级感”强行隔离。

---

#### 6.3.19 Subagent 的核心设计对象：Delegation Envelope

一次成熟的 Subagent 调用可以抽象成：

```text
Delegation Envelope =
    Objective
  + Scope / Non-goals
  + Input
  + Context
  + Capabilities
  + Authority
  + Budget
  + Output Contract
  + Acceptance Criteria
  + Escalation Policy
  + Termination Policy
```

它定义了 Subagent 的“局部世界边界”。

---

#### 6.3.20 Objective：到底要它完成什么

Objective 应尽量满足：

```text
局部可理解
局部可执行
局部可判断完成
```

坏例子：

```text
“看看这个项目有没有问题。”
```

更好的例子：

```text
“审查 auth/ 下最近一次改动是否引入权限绕过；返回具体文件、证据、风险等级，不修改代码。”
```

---

#### 6.3.21 Scope：允许处理到哪里

Scope 可以包括：

- 哪些文件；
- 哪些服务；
- 哪个时间区间；
- 哪些数据源；
- 哪些实体；
- 哪些操作类型。

Scope 越模糊，Subagent 越容易发生 Task Drift。

---

#### 6.3.22 Non-goals：明确什么不要做

很多安全问题来自“没有说不能做”。

例如：

```text
Do not modify files.
Do not send messages.
Do not purchase anything.
Do not contact external systems beyond X.
Do not create further subagents.
```

Non-goals 是 Delegation Contract 的一部分。

---

#### 6.3.23 Input 与 Context 仍然不是一回事

Input 是本次任务直接消费的对象。

Context 是帮助 Subagent 正确解释 Input 的背景。

例如：

```text
Input:
  pull request diff

Context:
  repository conventions
  security policy
  relevant architecture notes
```

不要把所有 Context 都伪装成 Input。

---

#### 6.3.24 Context Snapshot

Subagent 常收到的是某一时刻的状态快照：

```text
state@t0
```

但执行过程中真实世界可能已经变成：

```text
state@t1
```

因此需要知道：

- Snapshot 什么时候生成；
- 哪些字段可能变旧；
- 哪些操作前必须重新读取 authoritative state。

---

#### 6.3.25 Capability：会什么，不等于能做什么

Capability 描述：

```text
What can this Subagent technically do?
```

例如：

- web search；
- code execution；
- database query；
- repository inspection。

但它不自动意味着有 Authority。

---

#### 6.3.26 Authority：允许它真正做什么

Authority 描述：

```text
What is this Subagent authorized to do now?
```

例如：

```text
Capability: can call send_email
Authority: this task may not send any email
```

必须保持：

```text
Capability ≠ Authority
```

---

#### 6.3.27 Tool Set 应按任务裁剪

不要默认：

```text
Parent 有什么 Tool
→ Subagent 全继承
```

更好的方式是：

```text
Delegated Goal
→ derive required capabilities
→ expose minimum tool set
```

这同时降低：

- 误调用；
- 攻击面；
- Prompt 复杂度；
- Tool-selection confusion。

---

#### 6.3.28 Permission Set 应比 Tool Set 更细

即使暴露同一个 Tool，也可以限制：

- 只读 / 可写；
- 路径范围；
- Domain Allowlist；
- 数据行范围；
- 最大金额；
- 操作类型；
- 是否需要 Approval。

因此 Tool Exposure 只是第一层，Runtime Authorization 才是实际边界。

---

#### 6.3.29 Budget 是 Delegation Envelope 的硬边界

常见 Budget：

```text
max_steps
max_tokens
max_tool_calls
max_wall_time
max_cost
max_subagent_depth
max_parallelism
```

没有预算的递归 Agent 系统，很容易把“继续努力”变成无限扩张。

---

#### 6.3.30 Output Contract

Parent 不应该只说：

```text
“做完告诉我。”
```

更稳健的是定义：

```text
status
summary
findings[]
evidence[]
confidence
unresolved[]
actions_taken[]
side_effects[]
```

Structured Return 能显著降低 Integration Ambiguity。

---

#### 6.3.31 Evidence Contract

如果 Parent 之后要做 Verification，Subagent 应返回足够证据。

例如：

```text
finding
→ source
→ exact location
→ observation
→ inference
```

而不是只返回：

```text
“我认为这里有风险。”
```

---

#### 6.3.32 Acceptance Criteria

Subagent 的“完成”与 Parent 的“接受”不是一回事。

```text
Subagent Completion
    ≠
Parent Acceptance
```

Parent 应知道：

- 什么输出算完整；
- 哪些字段必须存在；
- 什么证据强度足够；
- 哪些结论需要二次验证。

---

#### 6.3.33 Escalation Policy

Subagent 遇到以下情况不应继续猜：

- Goal 冲突；
- 缺关键输入；
- 权限不足；
- 预算即将耗尽；
- 高风险 Side Effect；
- 关键状态发生变化；
- 无法满足验收条件。

这时应该：

```text
Escalate → Parent
```

而不是静默扩大自主权。

---

#### 6.3.34 Escalation 不是 Failure

合理的 Subagent 应该知道自己的边界。

因此：

> **在正确时间 Escalate，本身可能是成功行为。**

如果 Evaluation 把所有 Escalation 都算失败，系统会激励 Agent 越权猜测。

---

#### 6.3.35 Cancellation Policy

Parent 可能因为：

- 用户取消；
- 上游目标改变；
- 另一路已经得到答案；
- 预算耗尽；
- 风险升级；

需要取消正在执行的 Subagent。

因此需要明确：

```text
cancel request
→ stop new actions
→ handle in-flight actions
→ return partial state
→ release resources
```

---

#### 6.3.36 Termination Policy

Subagent 至少要知道什么时候停止：

```text
Goal satisfied
OR impossible
OR budget exhausted
OR cancelled
OR escalated
OR safety blocked
```

否则“继续搜索一点”很容易成为无界循环。

---

#### 6.3.37 Minimal Sufficient Delegation Context

给 Subagent 的 Context 应满足：

> **完成 delegated goal 所需的最少充分信息。**

目标不是最短 Prompt，而是：

```text
Sufficient for correctness
Minimal for isolation
```

---

#### 6.3.38 不要把完整 Transcript 当 Delegation Context

直接复制 Parent 全部历史，常见问题包括：

- 无关信息污染；
- 旧约束与新约束冲突；
- 隐私信息扩散；
- Token 成本上升；
- Subagent 更难识别真正目标。

> **Context Dump 不是 Context Engineering。**

---

#### 6.3.39 Context 应尽量结构化

例如：

```text
Goal:
Constraints:
Relevant facts:
Artifacts:
State snapshot:
Allowed actions:
Expected output:
```

这比一大段“以下是此前所有聊天记录”更容易验证信息是否完整。

---

#### 6.3.40 Provenance 必须跟着信息走

Parent 传给 Subagent 的关键事实，应尽可能带：

```text
value
source
observed_at
version
confidence
```

否则 Subagent 无法区分：

```text
authoritative fact
vs
parent inference
vs
stale memory
```

---

#### 6.3.41 Stale Context 是 Subagent 的高频风险

一个典型错误：

```text
Parent 在 t0 读取文件
→ 把内容传给 Subagent
→ 文件在 t1 被其他流程修改
→ Subagent 在 t2 基于旧内容做写入决策
```

因此涉及 Side Effect 时，应结合：

- version / ETag；
- compare-and-swap；
- precondition check；
- re-read before write。

---

#### 6.3.42 Write-back Contract

Subagent 返回 Parent 的，不应该默认是整个内部 Context。

应明确：

```text
What should be written back?
```

通常包括：

- final findings；
- supporting evidence；
- changed artifacts；
- unresolved issues；
- side effects；
- state version。

---

#### 6.3.43 不应该默认回传完整 Scratchpad

Parent 真正需要的是：

```text
decision-relevant result
+ evidence
+ trace metadata
```

而不是 Subagent 的全部内部生成过程。

这既减少 Context Pollution，也让接口更稳定。

---

#### 6.3.44 Interface First

Subagent 设计顺序最好是：

```text
先定义边界与接口
→ 再定义 Prompt
→ 再选择模型与工具
```

而不是：

```text
先造一个 Agent
→ 再想它能干什么
```

---

#### 6.3.45 Subagent Lifecycle

一个典型生命周期：

```text
Spawn
→ Initialize
→ Execute
→ Checkpoint / Report
→ Join / Return
→ Terminate
```

每个阶段都有不同的状态与失败语义。

---

#### 6.3.46 Spawn

Spawn 时至少要绑定：

- subagent_id；
- parent_id；
- task_id；
- delegated_goal；
- context_version；
- authority_scope；
- budget；
- trace linkage。

如果这些关系不可追踪，后面很难做审计。

---

#### 6.3.47 Initialize

Initialize 不只是加载 Prompt。

还可能包括：

- 创建独立 Context；
- 挂载 Workspace；
- 注入 Credentials；
- 配置 Tool Allowlist；
- 建立 State Snapshot；
- 注册 Cancellation Token。

---

#### 6.3.48 Execute

执行阶段应把局部 autonomy 限制在 Delegation Envelope 内。

Subagent 可以自主决定：

```text
局部搜索顺序
局部工具选择
局部推理路径
局部重试
```

但不应自动扩大：

```text
Goal
Authority
Budget
Scope
```

---

#### 6.3.49 Checkpoint / Progress Report

长任务不一定要等到最后才返回。

可以周期性报告：

```text
progress
current hypothesis
evidence collected
remaining work
budget remaining
blockers
```

但 Checkpoint 频率也不能高到让 Parent 重新变成逐步遥控器。

---

#### 6.3.50 Join / Return

Join 阶段的核心不是“字符串拼接”，而是：

```text
Validate
→ Normalize
→ Reconcile
→ Verify when needed
→ Integrate
```

尤其多个 Subagent 并行返回时，结果可能互相冲突。

---

#### 6.3.51 Terminate

任务结束后，应明确清理：

- 临时 Credentials；
- Sandbox；
- File Locks；
- Background Jobs；
- Temporary State；
- Cancellation Handles。

Ephemeral Subagent 的生命周期结束，不意味着它的资源一定自动消失。

---

#### 6.3.52 Ephemeral vs Persistent Subagent

**Ephemeral Subagent**：

```text
per-task / per-subtask
```

优点：隔离强、状态简单、易回收。

**Persistent Specialist**：

```text
long-lived identity / state / service
```

优点：可复用长期 Memory 或资源，但状态治理更复杂。

不要因为 Specialist 会被重复调用，就自动给它永久 Memory。

---

#### 6.3.53 Persistent Subagent 会引入 Hidden State

长期存在意味着它可能携带：

- 旧用户信息；
- 旧任务假设；
- 旧缓存；
- 旧权限；
- 旧计划。

因此 Persistent Agent 更需要：

```text
state ownership
state expiry
tenant isolation
reset semantics
```

---

#### 6.3.54 Parent–Child Tree

最常见拓扑：

```text
Parent
├── Child A
├── Child B
└── Child C
```

优点是：

- Ownership 清晰；
- Trace 简单；
- Result 回流路径明确。

---

#### 6.3.55 Recursive Subagents

Subagent 也可以继续 spawn：

```text
Parent
  └─ A
      ├─ A1
      └─ A2
```

但递归会快速放大：

```text
fan-out × depth × retries
```

因此必须有硬边界。

---

#### 6.3.56 Recursive Spawn 至少要限制四件事

```text
max_depth
max_children_per_agent
max_total_agents
max_total_budget
```

最好再加：

```text
allowed_child_types
```

避免任意角色无限复制自己。

---

#### 6.3.57 Subagent 不应该默认拥有 Spawn 权限

Spawn 本身也是 Authority。

如果 Worker 只需要完成一个局部分析，就没有必要让它继续创建更多 Agent。

> **Agent creation should be permissioned, not assumed.**

---

#### 6.3.58 DAG / Shared Specialist

现实系统有时不是树：

```text
A ─┐
   ├→ Shared Specialist
B ─┘
```

这会引入：

- 多 Parent 请求；
- Request correlation；
- Tenant / task isolation；
- Queueing；
- Shared state contamination 风险。

此时它更像一个独立 Agent Service，而不是简单 Child Process。

---

#### 6.3.59 Synchronous Request–Response

最简单通信方式：

```text
Parent call
→ wait
→ Subagent result
```

适合：

- 任务短；
- Parent 必须等结果再继续；
- 不需要中间流式事件。

缺点是 Parent 的 Critical Path 被阻塞。

---

#### 6.3.60 Streaming Result

长任务可返回：

```text
status events
partial findings
artifact updates
final result
```

但要区分：

```text
partial ≠ authoritative final
```

否则 Parent 可能过早消费未稳定结果。

---

#### 6.3.61 Event-driven Subagent

异步系统中可能是：

```text
Parent emits task event
→ Worker consumes
→ emits progress / completion event
```

此时必须额外处理：

- delivery semantics；
- duplicate event；
- ordering；
- correlation id；
- timeout；
- cancellation。

---

#### 6.3.62 Shared Memory 不是天然的协作方案

多个 Subagent 都读写同一 Memory，看起来方便，但会引入：

```text
race condition
stale read
semantic conflict
accidental leakage
```

协作需要定义 State Semantics，而不是只“接一个共享数据库”。

---

#### 6.3.63 Local State 与 Shared State

一个稳健原则：

```text
能留在 Local 的，不升级成 Shared。
```

Local State 适合：

- 中间 Hypothesis；
- 搜索缓存；
- 草稿；
- 临时计划。

Shared State 只放其他 Agent 真正需要依赖的事实或产物。

---

#### 6.3.64 Authoritative State 必须有 Owner

如果多个 Agent 都能修改同一个关键对象：

```text
order status
incident status
repository branch
customer record
```

就要明确：

```text
Who is authoritative writer?
```

否则“协作”很容易变成 Lost Update。

---

#### 6.3.65 Snapshot Isolation

一种简单方法是：

```text
每个 Subagent 在固定 Snapshot 上工作
→ 返回 Patch / Proposal
→ Parent 在最新 State 上验证并合并
```

这比让所有 Worker 直接并发写 Global State 更容易控制。

---

#### 6.3.66 Shared Mutable State 是高风险设计

如果必须共享写状态，至少考虑：

- versioning；
- optimistic concurrency control；
- locking；
- idempotency；
- conflict detection；
- merge semantics。

LLM 不应该承担数据库并发控制器的职责。

---

#### 6.3.67 Conflict Resolution 不能靠“谁后写谁赢”

两个 Subagent 可能分别产生：

```text
Patch A
Patch B
```

冲突处理应基于：

- authoritative state；
- dependency relation；
- semantic compatibility；
- explicit merge policy；
- verifier / human approval。

---

#### 6.3.68 什么任务适合并行 Subagents

并行最适合：

```text
low dependency
+ independently executable
+ independently evaluable
```

例如多个资料源检索。

不适合：

```text
B 强依赖 A 的完整结果
```

这时伪并行只会增加返工。

---

#### 6.3.69 Dependency Graph 应先于 Parallelism

不要先问：

```text
“能不能开 8 个 Subagent？”
```

先问：

```text
任务依赖图是什么？
```

真正可并行的是没有未满足依赖的节点。

---

#### 6.3.70 Duplicate Work

多个 Subagent 在信息不足时，常会自然地重复：

- 搜同一个网页；
- 读同一个文件；
- 验证同一个假设；
- 生成近似方案。

因此 Parallelism 应配合：

```text
partitioning
claim / lease
shared index
explicit search space assignment
```

---

#### 6.3.71 Deliberate Redundancy 与 Accidental Duplication 不一样

有时故意让多个 Subagent 独立做同一题，用于：

- robustness；
- diversity；
- cross-check。

这是 **Deliberate Redundancy**。

无意重复同样工作则是 **Accidental Duplication**。

Evaluation 必须区分两者。

---

#### 6.3.72 Aggregation 不是 Verification

多个 Subagent 返回结果之后：

```text
merge / vote / summarize
```

只是 Aggregation。

Verification 问的是：

```text
结果是否有证据支持？
是否满足约束？
是否与 authoritative state 一致？
```

因此：

> **Many answers do not automatically create a verified answer.**

---

#### 6.3.73 Consensus 也不是 Ground Truth

如果三个 Subagent：

```text
共享同一错误前提
共享同一错误数据源
共享同一 Prompt 偏差
```

它们可能高度一致地出错。

所以 Majority Vote 不能替代外部证据或 deterministic verifier。

---

#### 6.3.74 Subagent Failure 要分类型

至少区分：

```text
Transport Failure
Tool Failure
Budget Exhaustion
Policy Block
Task Misunderstanding
Insufficient Evidence
Semantic Error
State Conflict
Cancellation
Timeout
```

不同 Failure 的恢复策略不同。

---

#### 6.3.75 Retry 只适合可重试 Failure

网络抖动可以 Retry。

但如果失败原因是：

```text
任务定义错误
权限设计错误
缺关键输入
```

原样 Retry 十次只会重复错误。

> **Retry is not a universal recovery strategy.**

---

#### 6.3.76 Retry 必须结合 Idempotency

如果 Subagent 可能执行 Side Effect：

```text
create ticket
send email
charge card
write file
```

Retry 前必须知道：

```text
上一次是否已经成功但 ACK 丢失？
```

因此需要：

- idempotency key；
- operation id；
- state re-check；
- duplicate suppression。

---

#### 6.3.77 Timeout 不是简单“杀掉进程”

Timeout 发生时，可能已经存在：

- in-flight API；
- 已提交 Side Effect；
- 部分文件修改；
- 后台任务。

所以 Timeout Handling 要回答：

```text
What has already happened?
What can still happen?
What must be compensated?
```

---

#### 6.3.78 Cancellation Propagation

如果 Parent 任务被取消：

```text
Parent cancelled
```

通常要向 Child 传播。

否则可能出现：

```text
用户已经取消
但后台 Subagent 仍继续发消息 / 写数据 / 消耗预算
```

---

#### 6.3.79 Partial Result

Subagent 失败不代表所有产物都无价值。

可以返回：

```text
status = partial
completed = [...]
unresolved = [...]
evidence = [...]
side_effects = [...]
```

Parent 再决定是否续跑或换 Worker。

---

#### 6.3.80 安全问题一：Confused Deputy

Parent 有权限，Subagent 有能力，外部输入可能诱导它替攻击者使用 Parent 的权限。

典型风险：

```text
untrusted content
→ manipulates Subagent
→ Subagent uses delegated privilege
```

所以 Delegation 不能只传 Credentials，还必须传明确的 Authority Scope。

---

#### 6.3.81 安全问题二：Privilege Amplification

危险链路：

```text
Parent 权限 A
→ Child 自动继承 A
→ Child 又 spawn Child2
→ 权限继续扩散
```

应避免：

```text
inherit all permissions by default
```

更安全的是显式 capability / authority grants。

---

#### 6.3.82 安全问题三：Capability Laundering

某个 Subagent 自己无权执行某操作，却通过调用另一个高权限 Agent 间接完成。

因此权限检查不能只看：

```text
Who made the final tool call?
```

还要考虑：

```text
On whose behalf?
Under which delegated authority?
```

---

#### 6.3.83 安全问题四：Prompt Injection Propagation

如果 Research Subagent 读取了不可信网页，然后把其中恶意指令当“结论”回传 Parent，攻击可能跨 Agent 传播。

因此返回内容应区分：

```text
source content
vs
agent instruction
vs
agent conclusion
```

不要让下游 Agent 把上游采集到的文本自动升级成高优先级 Instruction。

---

#### 6.3.84 安全问题五：Secret Leakage

Parent 的 Context 可能包含：

- API Key；
- 用户隐私；
- 内部凭据；
- 机密文档；
- 与子任务无关的敏感数据。

如果完整 Context Dump 给 Subagent，就扩大了 Secret Exposure Surface。

因此 Context Isolation 也是 Data Minimization。

---

#### 6.3.85 安全问题六：Cross-tenant Contamination

Persistent Specialist 或 Shared Agent Service 尤其要注意：

```text
Task A / User A state
```

不能泄漏到：

```text
Task B / User B
```

必须有明确 tenant / session / task namespace。

---

#### 6.3.86 Observability：必须能看见 Parent–Child 因果链

至少需要：

```text
task_id
parent_run_id
subagent_run_id
delegation_id
trace_id
span_id
```

这样才能回答：

```text
为什么创建它？
它做了什么？
结果被谁消费？
最终决策受它什么影响？
```

---

#### 6.3.87 Trace 不应只有 Message Transcript

还要记录：

- Delegation Envelope；
- Context Version；
- Tool Calls；
- Authority Grants；
- Budget Consumption；
- State Reads / Writes；
- Escalation；
- Cancellation；
- Return Status。

这样才能做真正的 Failure Localization。

---

#### 6.3.88 Subagent Evaluation：先看 Delegation Quality

需要评价 Parent 是否：

- 在正确时机委派；
- 选择正确 Specialist；
- 给对 Objective；
- 给足 Context；
- 没有给过多权限；
- 给了可用的 Output Contract。

很多“Subagent 失败”其实是 Parent 的 Delegation Failure。

---

#### 6.3.89 Task Success 不能只看 Subagent 自报成功

至少要区分：

```text
reported_success
contract_satisfied
externally_verified_success
```

Agent 说“完成了”只是一个 Observation，不是 Ground Truth。

---

#### 6.3.90 Evidence Quality

可以评价：

- Evidence Coverage；
- Source Reliability；
- Citation Accuracy；
- Freshness；
- Claim–Evidence Alignment；
- Uncertainty Calibration。

对于 Research / Review Subagent，这些往往比语言流畅度更重要。

---

#### 6.3.91 Efficiency Metrics

常见指标：

```text
subagent_calls_per_task
total_model_tokens
total_tool_calls
wall_clock_latency
critical_path_latency
parallelism_factor
duplicate_work_rate
unused_result_rate
```

其中 `unused_result_rate` 很有价值：大量结果最终完全没被 Parent 使用，通常意味着过度 fan-out。

---

#### 6.3.92 Escalation Metrics

可以统计：

```text
escalation_rate
necessary_escalation_rate
missed_escalation_rate
false_escalation_rate
```

真正危险的是：

```text
should escalate but did not
```

而不是 Escalation 数量本身。

---

#### 6.3.93 State / Merge Metrics

并发 Subagent 可以额外统计：

```text
stale_read_rate
write_conflict_rate
merge_conflict_rate
lost_update_rate
rework_rate
```

这些是 Multi-Agent 系统特有的可靠性信号。

---

#### 6.3.94 Failure Localization

当最终任务失败时，要能判断失败发生在哪一层：

```text
wrong delegation?
wrong context?
wrong subagent decision?
tool failure?
stale state?
bad merge?
missing verification?
unsafe authority?
```

这比只给 Final Accuracy 一个 0 更有调试价值。

---

#### 6.3.95 常见反模式一：Agent Proliferation

“这个任务复杂，所以再加 5 个 Agent”通常不是系统设计。

如果每个 Agent 都没有明确：

```text
unique responsibility
unique context boundary
unique authority boundary
```

很可能只是角色数量膨胀。

---

#### 6.3.96 常见反模式二：Full Context Replication

如果每个 Subagent 都收到 Parent 的完整 Context：

```text
所谓 Context Isolation 实际不存在
```

只是在复制 Context 成本。

---

#### 6.3.97 常见反模式三：Implicit Authority Inheritance

```text
Parent can do X
→ Child can do X
```

不是安全的默认规则。

权限应来自本次 Delegation，而不是血缘关系。

---

#### 6.3.98 常见反模式四：Fire-and-Forget Side Effects

如果 Parent spawn 一个会产生真实副作用的 Subagent，然后既不追踪也不验证：

```text
spawn → forget
```

就会失去：

- completion status；
- cancellation；
- auditability；
- compensation ability。

---

#### 6.3.99 常见反模式五：No Return Contract

自由文本返回会导致 Parent 每次都重新猜：

```text
它做完了吗？
哪些是事实？
哪些是建议？
是否真的执行了动作？
还有什么没完成？
```

这会把 Integration 重新变成另一个模糊推理任务。

---

#### 6.3.100 常见反模式六：No Verification Boundary

Subagent 既提出方案，又执行方案，又宣布自己成功，且没有任何外部检查时：

```text
planner = actor = verifier
```

高风险任务尤其容易形成闭环盲区。

---

#### 6.3.101 一个稳健的 Parent–Subagent 参考结构

```text
User / Upstream Goal
        ↓
Parent Agent
  ├─ decide whether delegation is necessary
  ├─ construct Delegation Envelope
  ├─ grant minimum Context / Capability / Authority
  ↓
Subagent
  ├─ local Decision Loop
  ├─ bounded Tool Use
  ├─ evidence collection
  ├─ escalate when boundary reached
  ↓
Structured Return
  ↓
Parent
  ├─ validate contract
  ├─ verify critical claims / side effects
  ├─ reconcile with authoritative state
  └─ decide next action
```

---

#### 6.3.102 一个简单伪代码

```python
def run_parent(task):
    if can_solve_deterministically(task):
        return run_workflow(task)

    if not needs_independent_loop(task):
        return parent_agent.solve(task)

    envelope = build_delegation_envelope(task)
    child = spawn_subagent(
        context=envelope.minimal_context,
        tools=envelope.allowed_tools,
        authority=envelope.authority,
        budget=envelope.budget,
    )

    result = child.run(envelope.objective)

    validate_return_contract(result)
    verify_if_required(result)
    reconcile_with_authoritative_state(result)

    return integrate(result)
```

重点不在 API，而在三个 Gate：

```text
Does it need a Subagent?
What exact boundary does it get?
How is its result verified and integrated?
```

---

#### 6.3.103 Subagent 与 Workflow Worker 的面试区分

可以这样回答：

> **Workflow Worker 的执行路径主要由外部流程图决定；Subagent 在被委派的局部目标内，自己通过 Decision Loop 决定若干下一步动作。**

两者可以结合：

```text
Deterministic Workflow
→ node invokes Subagent
→ Subagent completes uncertain local task
→ Workflow resumes
```

---

#### 6.3.104 Subagent 与 Microservice 的面试区分

Microservice 主要描述：

```text
software deployment / service boundary
```

Subagent 主要描述：

```text
agentic decision / delegation boundary
```

一个 Subagent 可以运行在 Microservice 中；一个 Microservice 也可以只暴露确定性 API，没有任何 Agent。

---

#### 6.3.105 Subagent 与 Thread / Process 的面试区分

Thread / Process 是计算执行机制。

Subagent 是：

```text
goal + policy + context + capabilities + local decision loop
```

它可以由 Thread、Process、Container、Remote Service 等不同运行时承载。

不要把逻辑角色和基础设施机制混为一谈。

---

#### 6.3.106 Subagent 与 Persona 的面试区分

Persona 只是行为 / 表达 /角色设定时：

```text
“你现在作为安全专家回答”
```

不一定创建新的 Agent 实例。

只有当系统形成独立的：

```text
Context
Decision Loop
Capability / Authority boundary
Lifecycle
```

才更接近真正 Subagent。

---

#### 6.3.107 Subagent 与 Handoff 的一句话区别

面试可以直接说：

> **Subagent 解决的是“把一个 bounded subtask 交给另一个局部闭环执行”；Handoff 解决的是“把当前控制权交给另一个 Agent”。**

因此典型 Agents-as-Tools 场景中，Subagent 完成后控制返回 Parent；典型 Handoff 场景中，目标 Agent 成为新的 active owner。

---

#### 6.3.108 设计 Subagent 时最值得先问的 10 个问题

1. 为什么这不是一个 Tool / Workflow？
2. 它需要独立 Decision Loop 的原因是什么？
3. Parent 保留哪些 Control Ownership？
4. Delegated Goal 是否局部可判定？
5. 最少需要哪些 Context？
6. 最少需要哪些 Tool / Authority？
7. Budget 和终止条件是什么？
8. 返回什么结构、什么证据？
9. 什么时候必须 Escalate？
10. Parent 如何 Verify / Integrate？

---

#### 6.3.109 一个非常实用的判断公式

可以把是否值得拆 Subagent 粗略理解为：

```text
Subagent Value
≈
Specialization Gain
+ Context Isolation Gain
+ Parallelism Gain
+ Failure / Authority Isolation Gain
-
Coordination Tax
-
Verification Cost
-
State / Security Complexity
```

不是数学定律，但很适合作为设计检查框架。

---

#### 6.3.110 Subagents 最核心的一句话

> **Subagent 不是“多叫一个模型帮忙”，而是在 Parent 的顶层责任之下，为一个 bounded subtask 创建独立但受约束的局部 Decision Loop。**

真正成熟的 Subagent 设计，关注的不是 Agent 数量，而是：

```text
清楚的 Goal
+ 最少充分 Context
+ 最小必要 Authority
+ 明确 Budget
+ 可验证 Return Contract
+ 可追踪 Lifecycle
```

因此：

> **Subagents are an execution and isolation primitive, not a reason to fragment every task.**

---

#### 6.3.111 参考资料

1. OpenAI. *Agents SDK — Agent orchestration*. https://openai.github.io/openai-agents-python/multi_agent/ 。区分 manager-style Agents-as-Tools 与 Handoffs；前者由 Manager 保留对话控制并调用 specialist agents，后者让 specialist 接管当前控制。
2. OpenAI. *Agents SDK — Agents*. https://openai.github.io/openai-agents-python/agents/ 。关于 Agent 的 instructions、tools、handoffs、guardrails、structured outputs 等运行时组成，以及多 Agent 的 manager / handoff 两类常见关系。
3. Anthropic. *Building Effective Agents*. https://www.anthropic.com/engineering/building-effective-agents 。关于 routing、parallelization、orchestrator-workers，以及优先选择简单、可组合模式的工程原则。
4. Anthropic. *Enabling Claude Code to work more autonomously*. https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously 。将 Subagents 用于 specialized tasks 与 parallel development，并与 checkpoint、hooks、background tasks 等控制机制结合。
5. Anthropic. *Trustworthy agents in practice*. https://www.anthropic.com/research/trustworthy-agents 。讨论更长、更自主的 Agent 行为如何改变用户监督方式，并指出并行 Subagents 带来的可理解性与可控制性问题。
'''

text = text.replace(old, section + "\n### 6.4 Communication", 1)

old_progress = "| II | 6. Multi-Agent & Agent Interoperability | 进行中：6.1–6.2 已完成 |"
new_progress = "| II | 6. Multi-Agent & Agent Interoperability | 进行中：6.1–6.3 已完成 |"
assert text.count(old_progress) == 1, f"progress marker count: {text.count(old_progress)}"
text = text.replace(old_progress, new_progress, 1)

old_next = "下一步：继续 **II. Capabilities & Interoperability → 6. Multi-Agent & Agent Interoperability → 6.3 Subagents**。"
new_next = "下一步：继续 **II. Capabilities & Interoperability → 6. Multi-Agent & Agent Interoperability → 6.4 Communication**。"
assert text.count(old_next) == 1, f"next marker count: {text.count(old_next)}"
text = text.replace(old_next, new_next, 1)

assert text.count("### 6.3 Subagents") == 1
assert text.count("#### 6.3.111 参考资料") == 1
assert "进行中：6.1–6.3 已完成" in text
assert "→ 6.4 Communication**。" in text

path.write_text(text, encoding="utf-8")
print("6.3 patch applied successfully")
