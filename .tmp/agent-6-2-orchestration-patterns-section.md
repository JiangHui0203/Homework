#### 6.2.1 Orchestration 到底是什么

Multi-Agent 解决的是：

> **系统里为什么需要多个相对独立的 Decision Loop。**

而 Orchestration 解决的是另一件事：

> **当这些 Decision Loop 已经存在时，谁在什么时候获得控制权、接收什么任务与 Context、能够采取什么 Action、结果交给谁、失败后由谁恢复，以及整个系统何时停止。**

因此可以把 Orchestration 定义为：

> **对多个 Agent / Worker 的 Control Flow、Delegation、State Flow、Authority Flow、Result Flow 与 Termination / Recovery 进行组织的系统机制。**

它不是“让多个 Agent 聊起来”。

---

#### 6.2.2 Multi-Agent ≠ Orchestration

两个概念必须分开：

```text
Multi-Agent
= 系统中存在多个相对独立的 Agent / Decision Loop

Orchestration
= 这些 Decision Loop 怎样被组织与协调
```

因此：

```text
有 Multi-Agent
→ 必然存在某种 coordination / orchestration

有 Orchestration
↛ 一定意味着所有节点都是 Agent
```

一个确定性程序完全可以 orchestrate 多个 Agent。

---

#### 6.2.3 Orchestrator 不一定是 Agent

这是最容易被产品术语混淆的地方。

Orchestrator 可以是：

```text
Deterministic Code
Workflow Engine
Graph Runtime
Queue / Scheduler
Rule-based Router
LLM-based Supervisor
Agent
Human
Hybrid Controller
```

所以：

> **Orchestrator 是 control responsibility，不是固定的 capability category。**

不要看到“负责调度其他 Agent”就自动认为 orchestrator 自己也必须是 Agent。

---

#### 6.2.4 Orchestration 的核心不是 Agent 数量，而是 Control Ownership

真正要问的是：

```text
当前这一步由谁决定？
谁拥有下一步选择权？
谁能改变任务状态？
谁能把控制权交出去？
谁负责最终终止？
```

因此 Multi-Agent Orchestration 的第一原则仍然是前面反复强调的：

> **先找 Control Flow 的 Owner。**

---

#### 6.2.5 一个最小 Orchestration Loop

可以抽象成：

```text
Global Goal
→ Orchestration State
→ Select / Delegate / Schedule
→ Worker or Agent
→ Local Decision Loop
→ Result / Evidence / Status
→ Aggregate / Verify
→ Global State Update
→ Route / Continue / Recover / Terminate
```

这里有两个不同层级的闭环：

```text
Local Loop
= 单个 Agent 内部如何完成被委派任务

Global Loop
= 整个系统如何决定哪个 Agent 下一步工作
```

Multi-Agent 系统的复杂性，很多都来自这两个闭环同时存在。

---

#### 6.2.6 Control Plane 与 Execution Plane

一个很有用的工程抽象是：

```text
Control Plane
├── decomposition
├── routing
├── delegation
├── scheduling
├── permission / approval
├── aggregation
├── termination
└── recovery

Execution Plane
├── worker reasoning
├── tool calls
├── local actions
├── local state updates
└── artifact production
```

这个区分不是要求系统必须真的部署成两个服务。

它的价值是帮助定位责任：

> **谁在决定“做什么”，谁在真正“执行”。**

---

#### 6.2.7 Orchestration ≠ Routing

Routing 只是 Orchestration 的一个子问题。

Routing 回答：

> **这一步应该交给谁？**

Orchestration 还必须回答：

- 任务怎样拆；
- 是否串行或并行；
- Context 传多少；
- 权限传多少；
- 多个结果如何合并；
- 谁验证；
- 谁重试；
- 谁负责最终状态；
- 什么时候停止。

所以：

```text
Routing ⊂ Orchestration
```

---

#### 6.2.8 Orchestration ≠ Workflow

Workflow 描述的是：

> **控制流怎样被显式组织。**

Orchestration 描述的是更广义的：

> **多个执行主体之间怎样分配控制、任务、状态和责任。**

因此完全可以有：

```text
Deterministic Workflow
→ orchestrate
→ multiple Agents
```

也可以在一个 Workflow 节点内部：

```text
Agent
→ dynamic delegation
→ Subagents
```

两者不是互斥概念。

---

#### 6.2.9 最稳健的现实形态通常是 Hybrid Orchestration

现实系统很少需要把所有控制都交给 LLM。

更常见的是：

```text
Deterministic Skeleton
+
Agentic Decisions at Uncertainty Frontiers
```

例如：

```text
固定：
输入校验
→ 权限检查
→ 审批
→ 写审计日志

动态：
选择研究方向
选择专家 Agent
判断是否需要补证据
判断哪条假设更值得继续
```

这与前面建立的原则一致：

> **把确定性留给程序，把真正的不确定性留给 Agent。**

---

#### 6.2.10 Orchestration 的第一个设计对象：Delegation

Multi-Agent 系统不是简单的：

```text
Agent A
→ “你帮我做一下”
→ Agent B
```

真正可靠的 Delegation 至少要明确：

```text
Goal
Scope
Input
Context
Capabilities
Permissions
Budget
Success Criteria
Output Contract
Failure Semantics
Return Path
```

因此 Delegation 本身应该被当成系统协议，而不是一段自然语言。

---

#### 6.2.11 Delegation Contract

可以把一次成熟的委派抽象成：

```text
Delegation Contract
├── delegated_goal
├── scope / non_goals
├── required_inputs
├── supplied_context
├── allowed_capabilities
├── authority / permissions
├── side_effect_policy
├── budget / deadline
├── output_schema
├── evidence / provenance requirements
├── success_criteria
├── uncertainty semantics
├── failure semantics
└── return / escalation path
```

这与前面的 Tool Contract、Skill Contract 思路一致。

> **Delegation without Contract 很容易退化成 Context Dump + Responsibility Dump。**

---

#### 6.2.12 Delegated Goal 必须可局部判定

一个好的 delegated goal 应尽可能满足：

```text
Worker 知道自己要完成什么
Worker 知道什么不属于自己
Worker 能判断是否完成
Coordinator 能验证返回结果
```

坏例子：

```text
“把这个项目做好。”
```

更好的形式：

```text
“检查支付模块最近 20 个 commit 中可能引入幂等性缺陷的改动，返回候选 commit、证据和置信度；不要修改代码。”
```

---

#### 6.2.13 Scope 与 Non-goals 很重要

只定义“做什么”往往不够。

还应该定义：

```text
不要做什么
不要访问什么
不要修改什么
不要推断什么
```

否则 Worker 很容易发生 scope creep。

在有真实 Side Effect 的 Agent 系统中，这不是文风问题，而是安全边界。

---

#### 6.2.14 Input ≠ Context

委派时必须继续保持此前的边界：

```text
Input
= 当前任务明确需要处理的对象

Context
= 为了正确决策而额外提供的信息
```

把整个上游 Transcript 都塞给 Worker，不叫良好的 Context Engineering。

---

#### 6.2.15 Minimal Sufficient Delegation Context

Multi-Agent 中可以复用此前的 Minimal Sufficient 原则：

> **给 Worker 完成 delegated goal 所需的最少充分 Context。**

目标是同时避免：

```text
Too Little
→ 信息缺失
→ 错误假设
→ 重复检索

Too Much
→ Context Pollution
→ Instruction Conflict
→ Attention Dilution
→ Token / Latency Cost
→ Security Leakage
```

不是共享越多越协作。

---

#### 6.2.16 Context Isolation 的收益必须靠 Interface 补回来

6.1 已经讲过：Context Isolation 是 Multi-Agent 的重要收益。

但隔离意味着：

```text
Agent A 的局部事实
默认不会自动成为 Agent B 的事实
```

因此必须设计：

```text
Explicit Input
Structured Result
Artifact Reference
Evidence
State Version
Provenance
```

> **隔离减少污染，Interface 负责恢复必要的信息流。**

---

#### 6.2.17 Delegation 中的 Authority 不能隐式继承

主 Agent 有权限，不代表 Subagent 自动应该拥有同样权限。

错误做法：

```text
Manager can:
read + write + send + delete

↓ delegate

Worker automatically inherits all
```

更合理的是：

```text
Delegated Goal
→ derive Minimal Required Authority
→ grant scoped permissions
```

这本质上是 Least Privilege。

---

#### 6.2.18 Capability Delegation 与 Authority Delegation 必须分开

例如：

```text
Worker knows how to send email
```

并不意味着：

```text
Worker is allowed to send this email
```

所以：

```text
Capability
≠ Permission
≠ Approval
```

Multi-Agent 只是让边界更多，并没有改变这一原则。

---

#### 6.2.19 Output Contract 是 Orchestration 的关键接口

如果 Worker 只返回一段自由文本：

```text
“我调查过了，看起来没问题。”
```

Coordinator 很难：

- 稳定解析；
- 判断是否完整；
- 追踪证据；
- 比较多个 Worker；
- 自动恢复；
- 可靠更新 State。

因此高价值 Worker 输出通常应包含：

```text
status
result
artifacts
supporting_evidence
uncertainty
side_effects
remaining_risks
next_recommendation
```

---

#### 6.2.20 Worker Success ≠ System Success

必须继续复用：

```text
Action Success ≠ Task Success
```

在 Multi-Agent 中进一步变成：

```text
Worker Success
≠ Delegation Success
≠ Global Task Success
```

Worker 成功完成局部任务，只能证明局部合同满足。

最终任务是否完成仍由更高层 State / Evaluator 判定。

---

#### 6.2.21 Unknown ≠ Failed 在 Multi-Agent 中更重要

例如 Worker 超时：

```text
worker_status = UNKNOWN
```

不能自动解释成：

```text
worker_status = FAILED
```

因为 Worker 可能已经产生 Side Effect，只是结果没有成功返回。

盲目再次委派可能造成：

```text
duplicate payment
duplicate email
duplicate ticket
duplicate mutation
```

因此跨 Agent 的 Outcome Uncertainty 也必须状态化。

---

#### 6.2.22 Orchestration 的第二个设计对象：Control Topology

谁能把工作交给谁，决定了系统的 Control Topology。

常见形态包括：

```text
Centralized
Hierarchical
Router-based
Handoff chain
Peer-to-peer
Shared workspace / blackboard
Hybrid
```

不要先从框架 API 出发。

先看任务真正需要什么 Control Topology。

---

#### 6.2.23 Centralized Orchestration

最典型结构：

```text
            Manager
          /    |    \
      Agent A Agent B Agent C
```

Manager 通常负责：

```text
decomposition
routing
delegation
aggregation
verification
termination
```

Workers 主要负责局部执行。

---

#### 6.2.24 Centralized 的优势

优势通常是：

- Global State 更清晰；
- 权限和 Policy 更容易统一；
- 责任归属清楚；
- 更容易做 Trace；
- 更容易统一 Recovery；
- 最终输出 Owner 明确。

因此很多生产系统天然会先从中心化结构开始。

---

#### 6.2.25 Centralized 的代价

Manager 也可能成为：

```text
Context Bottleneck
Reasoning Bottleneck
Latency Bottleneck
Token Bottleneck
Single Point of Failure
Permission Concentration Point
```

如果所有细节都必须回流 Manager：

> **Multi-Agent 的 Context Isolation 收益可能又被中心节点重新吃掉。**

---

#### 6.2.26 Hierarchical Orchestration

任务很大时可以形成：

```text
Top-level Manager
├── Research Supervisor
│   ├── Search Worker A
│   └── Search Worker B
└── Implementation Supervisor
    ├── Coding Worker
    └── Test Worker
```

Hierarchical 的价值是：

> **把 Decision Scope 也分层。**

但层级越深，Delegation Loss 和 Failure Attribution 越难。

---

#### 6.2.27 层级不是越深越专业

每增加一层都会增加：

```text
communication hop
context transformation
latency
coordination state
failure surface
```

所以应遵循：

> **使用满足任务隔离与控制需求的最小层级深度。**

---

#### 6.2.28 Manager / Supervisor Pattern

Manager / Supervisor Pattern 可以抽象成：

```text
Goal
→ Manager observes global state
→ choose / call worker
→ worker executes local task
→ return structured result
→ Manager updates global state
→ choose next worker or terminate
```

关键不是名字叫 Manager 还是 Supervisor。

关键是：

> **中心节点持续拥有 Global Control Ownership。**

---

#### 6.2.29 Manager 与 Supervisor 不必硬造绝对边界

不同框架对这两个词使用并不统一。

有的把 Manager 理解为：

```text
owns user-facing task + aggregation
```

把 Supervisor 理解为：

```text
monitors / routes / controls workers
```

但行业并没有稳定到足以把它们写成永恒理论。

本体系更关注：

```text
Who owns control?
Who owns final answer?
Who owns global state?
Who can delegate?
```

---

#### 6.2.30 Router Pattern

Router 的最小机制是：

```text
Current Goal / State / Input
→ Routing Decision
→ Select Destination
→ Dispatch
```

Destination 可以是：

```text
Agent
Workflow
Skill
Tool
Human
Model
Queue
```

所以 Router 不是 Multi-Agent 专属概念。

---

#### 6.2.31 Static Routing vs Dynamic Routing

Static Routing：

```text
known rule
→ known destination
```

例如：

```text
language == Japanese
→ JP workflow
```

Dynamic Routing：

```text
semantic state
→ model / classifier / policy
→ destination
```

只有第二类真正需要运行时判断。

---

#### 6.2.32 能用确定性 Router，就不要强行用 Agent Router

如果规则清晰：

```text
refund request → refund flow
invoice request → billing flow
```

直接程序化通常拥有更好的：

```text
predictability
latency
cost
testability
auditability
```

Agentic Router 的价值主要出现在 Uncertainty Frontier。

---

#### 6.2.33 Routing 的关键不是“选谁”，而是 Candidate Space 是否正确

和 Tool Selection 一样：

```text
Agent Universe
→ Availability
→ Permission
→ Compatibility
→ Task Relevance
→ Candidate Agents
→ Route
```

如果正确 Agent 根本没有进入 Candidate Set：

> **后面的 Router 再聪明也救不回来。**

这仍然是 Recall Upper Bound。

---

#### 6.2.34 Routing Failure Localization

遇到错路由，不要直接调 prompt。

应沿链路排查：

1. 正确 Agent 是否存在？
2. 当前是否可用？
3. 是否被发现？
4. 是否有权限？
5. Role / Capability Description 是否准确？
6. Router 是否拿到了充分 State？
7. Routing Policy 是否合理？
8. Dispatch 是否真正成功？
9. 下游是否正确接管？

---

#### 6.2.35 Handoff Pattern

Handoff 的核心不是“调用另一个 Agent”。

而是：

> **Control Ownership 发生转移。**

最小结构：

```text
Agent A owns control
→ Handoff decision
→ transfer context / state / authority
→ Agent B owns control
```

这是 Handoff 与普通 Agent-as-Tool 最关键的区别。

---

#### 6.2.36 Handoff 必须回答“交出去什么”

至少包括：

```text
Goal
Conversation / Context Slice
Working State
Pending Commitments
Artifacts
Permissions
Open Questions
Failure / Uncertainty State
```

如果只传一句：

```text
“你接着处理。”
```

很容易发生信息断裂。

---

#### 6.2.37 Handoff 不是 Transcript Copy

简单复制整个会话可能造成：

```text
旧 Instructions 泄漏
Role 冲突
无关 Context 污染
敏感信息过度共享
Token Cost
```

更稳健的 Handoff Package 是：

```text
Task State
+ Minimal Sufficient Context
+ Explicit Pending Obligations
+ Evidence / Artifact References
+ Authority Boundary
```

---

#### 6.2.38 Handoff 要有 Acceptance

可靠的接力最好不是单向“发出去就算完”。

可以有：

```text
Handoff Proposed
→ Target validates capability / authority / context
→ Accepted / Rejected / Need More Context
```

这样可以避免：

```text
orphan task
silent drop
wrong owner
```

---

#### 6.2.39 Handoff Success ≠ Task Success

应分别记录：

```text
handoff_requested
handoff_accepted
control_transferred
work_started
work_completed
global_task_completed
```

否则系统很容易把：

```text
“成功把问题转给 Billing Agent”
```

误记为：

```text
“用户的账单问题已解决”
```

---

#### 6.2.40 Agents-as-Tools Pattern

Agents-as-Tools 的结构通常是：

```text
Manager Agent
→ call specialist Agent as bounded capability
→ specialist runs local loop
→ returns result
→ Manager retains control
```

核心是：

> **Specialist 有 Agent 级内部自治，但对 Manager 暴露为 bounded callable capability。**

---

#### 6.2.41 Agents-as-Tools 与 Handoff 的严格区别

可以用 Control Ownership 判断：

```text
Agents-as-Tools
Manager retains control

Handoff
Control transfers to target Agent
```

因此两者最重要的问题分别是：

```text
Agents-as-Tools:
“我调用谁来帮我完成一个子任务？”

Handoff:
“接下来谁成为当前任务的 Owner？”
```

---

#### 6.2.42 Agents-as-Tools 的优势

它适合：

- Specialist 只处理 bounded subtask；
- Manager 需要统一最终答案；
- 全局 Policy 应集中；
- 多个 Worker 结果需要统一比较；
- 用户不需要感知 Owner 切换。

它本质上保留了中心化控制。

---

#### 6.2.43 Agents-as-Tools 的风险

常见问题：

```text
Manager Context Explosion
Nested Agent Calls
Duplicate Retrieval
Opaque Cost
Recursive Delegation
Hidden Side Effects
```

尤其要防止：

```text
Agent A as tool
→ calls Agent B as tool
→ calls Agent A again
```

形成循环委派。

---

#### 6.2.44 Parallel Workers Pattern

Parallel Workers 适用于：

```text
Subtask A ─┐
Subtask B ─┼─ parallel → aggregate
Subtask C ─┘
```

收益通常来自两类：

```text
Sectioning
= 不同 Worker 处理不同子任务

Sampling / Perspectives
= 多个 Worker 独立处理同一问题
```

这两个目标不要混淆。

---

#### 6.2.45 Parallelism 成立的首要条件是低依赖

真正适合并行的是：

```text
A does not need B's output
B does not need A's output
```

如果：

```text
B requires A
C requires B
```

硬并行只会制造：

```text
stale assumption
speculative work
rework
merge conflict
```

---

#### 6.2.46 Parallelism 优化 Critical Path，不自动优化 Total Cost

如果三个 Worker 各耗时 20 秒：

```text
Sequential Latency ≈ 60s
Parallel Critical Path ≈ 20s + orchestration overhead
```

但总计算量仍可能接近：

```text
3 × worker cost
```

甚至因为聚合与重复检索而更高。

> **并行首先是 latency optimization，不是免费计算。**

---

#### 6.2.47 Parallel Fan-out 必须受控

如果一个 Agent 可以无限扩散：

```text
1 → 5 → 25 → 125 workers
```

很快会出现：

```text
cost explosion
rate-limit pressure
queue pressure
context merge explosion
observability overload
```

所以需要：

```text
max depth
max fan-out
budget
concurrency limit
timeout
backpressure
```

---

#### 6.2.48 Parallel Results 需要显式 Aggregation

Fan-out 之后必须回答：

> **多个结果怎样变成系统下一步可用的 State？**

Aggregation 可能是：

```text
Concatenate
Merge
Rank
Select
Vote
Synthesize
Verify
Resolve Conflicts
```

这些不是同一种操作。

---

#### 6.2.49 Merge ≠ Verify

把三个 Worker 的答案合在一起：

```text
A + B + C
→ Summary
```

并不能证明 Summary 是正确的。

因此：

```text
Aggregation
≠ Verification
```

需要事实正确性时，应有独立 Evidence / Verifier / Deterministic Check。

---

#### 6.2.50 Voting 只有在错误不高度相关时才有价值

如果多个 Worker：

```text
same model
same prompt
same context
same retrieval
```

它们的错误可能高度相关。

此时：

```text
3 votes
```

不等于三份独立证据。

> **Consensus 不是 Ground Truth。**

---

#### 6.2.51 Debate / Collaboration Pattern

Debate / Collaboration 常见结构：

```text
Agent A proposes
Agent B critiques
Agent C adds evidence
A/B revise
Judge / Manager selects
```

它适合：

- 问题存在真实多视角；
- critique 可以暴露不同错误；
- 评判标准相对明确；
- 增加计算确实可能换来质量。

---

#### 6.2.52 Debate 不等于“让模型互相说服”

如果没有：

```text
independent evidence
role-specific information
clear evaluation criteria
stop condition
```

Debate 很容易退化成：

```text
longer conversation
social convergence
repeated arguments
verbosity inflation
```

所以应问：

> **第二个 Agent 带来了新的 Evidence / Failure Detection，还是只是新的措辞？**

---

#### 6.2.53 Independent Verification Pattern

很多任务比 Debate 更适合：

```text
Producer
→ Artifact
→ Independent Verifier
→ Pass / Fail / Feedback
```

Verifier 应尽量拥有：

```text
independent criteria
independent evidence path
limited exposure to producer reasoning
```

否则容易产生 correlated confirmation。

---

#### 6.2.54 Evaluator–Optimizer Loop

另一种常见 Orchestration：

```text
Generator
→ Output
→ Evaluator
→ Feedback
→ Generator revises
→ ...
→ Stop
```

关键不是“多跑几轮”。

而是必须有：

```text
measurable evaluation criterion
improvement signal
budget
termination condition
```

否则容易形成 no-progress loop。

---

#### 6.2.55 Peer-to-Peer Orchestration

Peer-to-Peer 允许 Agent 间直接协作：

```text
A ↔ B
↕   ↕
C ↔ D
```

优势是：

- 不依赖单一中心；
- 局部协作可以更直接；
- 某些分布式任务扩展性更好。

但它把更多复杂性转移到：

```text
state consistency
authority
message routing
termination
failure attribution
```

---

#### 6.2.56 Shared Workspace / Blackboard Pattern

另一种思路不是 Agent 彼此直接传整段消息，而是共享一个显式 Workspace：

```text
Agent A ─┐
Agent B ─┼→ Shared Workspace / Blackboard
Agent C ─┘
```

Workspace 中可以保存：

```text
facts
artifacts
claims
tasks
status
open questions
locks
versions
```

Agent 通过读写共享状态间接协作。

---

#### 6.2.57 Shared State 不是免费的一致性

共享 Workspace 会引入：

```text
race condition
stale read
write conflict
schema drift
authority conflict
```

所以需要考虑：

```text
version
ownership
atomicity
locking / optimistic concurrency
source / provenance
```

“大家都能看到”并不等于“大家看到的是同一个正确状态”。

---

#### 6.2.58 Shared Context ≠ Shared State

继续保持此前的概念边界：

```text
Shared Context
= 多个 Agent 当前 inference 都能看到的信息

Shared State
= 系统持久维护、多个 Agent 共同依赖的任务状态
```

两者可能重叠，但不是一回事。

---

#### 6.2.59 Event-driven Orchestration

有些系统不适合中心节点不断轮询。

可以采用：

```text
Event
→ subscriber / router
→ Agent / Workflow
→ new event
```

例如：

```text
new incident
→ diagnosis agent

payment confirmed
→ fulfillment workflow

review rejected
→ revision agent
```

这时 Event 本身成为控制流的重要触发器。

---

#### 6.2.60 Event-driven 的关键是事件语义

必须明确：

```text
At-most-once?
At-least-once?
Exactly-once effect?
Order guaranteed?
Can duplicate?
Can arrive late?
```

否则 Agent 层再聪明，也挡不住底层消息语义导致的重复 Action。

---

#### 6.2.61 Sequential Orchestration

Sequential 最简单：

```text
Agent A
→ Agent B
→ Agent C
```

适合：

```text
B depends on A
C depends on B
```

优点是状态关系清楚。

缺点是 Critical Path 变长，而且上游错误会向下游传播。

---

#### 6.2.62 Sequential Chain 的 Error Propagation

如果：

```text
A produces wrong assumption
→ B trusts it
→ C summarizes it
```

最终错误会被层层包装。

因此关键接口应携带：

```text
provenance
confidence / uncertainty
evidence
validation status
```

而不只是自然语言结果。

---

#### 6.2.63 Dynamic Decomposition vs Predefined Decomposition

Predefined：

```text
Task
→ Research
→ Draft
→ Review
```

Dynamic：

```text
Task
→ Orchestrator inspects state
→ decides subtasks at runtime
```

前者更可预测。

后者更适合无法预先知道子任务数量与类型的问题。

---

#### 6.2.64 Dynamic 不等于更高级

动态分解带来：

```text
adaptivity
```

也带来：

```text
variance
harder testing
cost uncertainty
routing errors
unstable topology
```

所以仍然应该问：

> **这一步的不可预知性是否真的需要模型来决定？**

---

#### 6.2.65 Uncertainty Frontier 决定 Agentic Orchestration 放在哪里

可以把系统拆成：

```text
Known Control Region
→ deterministic workflow

Uncertainty Frontier
→ agentic routing / decomposition / escalation
```

例如：

```text
固定：并行抓取 5 个数据源
动态：根据证据决定下一步追哪条假设
```

这通常比“所有节点都 Agent 化”更稳健。

---

#### 6.2.66 Orchestration 的第三个设计对象：State Ownership

Multi-Agent 系统必须明确：

```text
Who owns global state?
Who may mutate it?
Which state is local?
Which state is shared?
Who resolves conflict?
```

如果这些问题没有答案，系统很容易出现：

```text
Agent A thinks step 3 completed
Agent B thinks step 3 pending
Manager thinks step 3 failed
```

---

#### 6.2.67 Global State 与 Local State

一个实用划分：

```text
Global State
├── overall goal
├── task graph
├── authoritative facts
├── commitments
├── permissions
├── completed effects
└── termination status

Local State
├── worker scratchpad
├── local hypothesis
├── local retrieval state
├── temporary artifacts
└── local retry counters
```

不要把所有 Local State 都升级成 Global State。

---

#### 6.2.68 Authoritative State 必须有明确 Owner

多个 Agent 同时写“真实任务状态”非常危险。

至少要定义：

```text
authoritative source
write owner
merge rule
version
conflict policy
```

否则只是把 Shared Memory 换了个名字。

---

#### 6.2.69 State Synchronization 不应依赖模型“记得告诉别人”

关键状态更新应由 Harness / Runtime 保证：

```text
Action executed
→ Runtime records effect
→ State updated
→ downstream sees authoritative state
```

而不是：

```text
Agent A mentally remembers
→ hopefully mentions it to Agent B
```

---

#### 6.2.70 Freshness 必须进入跨 Agent 信息协议

跨 Agent 传递的信息可能：

```text
correct when produced
stale when consumed
```

因此重要事实应尽量带：

```text
timestamp
version
source
validity window
```

特别是在长任务与并行 Worker 中。

---

#### 6.2.71 Orchestration 的第四个设计对象：Termination

单 Agent 已经需要 Termination Policy。

Multi-Agent 更复杂，因为：

```text
某个 Worker 完成
≠ 系统完成

所有 Worker 返回
≠ Goal 完成
```

必须定义 Global Termination Condition。

---

#### 6.2.72 Global Termination 可以基于什么？

例如：

```text
Goal condition satisfied
Required artifacts complete
Verifier passes
Budget exhausted
Deadline reached
No-progress detected
Human escalation required
Safety stop
```

不要只靠：

```text
“Manager 感觉差不多了。”
```

---

#### 6.2.73 Cyclic Delegation

典型故障：

```text
A → B
B → C
C → A
```

如果没有：

```text
visited path
delegation depth
budget
progress signal
```

系统可能持续循环而不产生新信息。

---

#### 6.2.74 Deadlock

例如：

```text
Agent A waits for B
Agent B waits for C
Agent C waits for A
```

这不是模型回答质量问题。

这是协调协议错误。

需要 Runtime / Orchestrator 层的依赖检测与 timeout。

---

#### 6.2.75 Livelock

Livelock 指系统一直在“做事”，但没有真正推进。

例如：

```text
A asks B to verify
B asks A to clarify
A asks B to verify again
...
```

所以需要：

```text
progress metric
state delta
retry cap
escalation
```

---

#### 6.2.76 Retry Storm

如果多个层级都自动 Retry：

```text
Worker retries 3x
Supervisor retries worker 3x
Manager retries supervisor 3x
```

一次失败可能变成：

```text
3 × 3 × 3 = 27 attempts
```

因此 Retry Budget 应跨层协调。

---

#### 6.2.77 Recovery Ownership 必须唯一或显式分层

遇到 Worker failure，应明确：

```text
Worker local retry?
Supervisor reroute?
Manager fallback?
Human escalation?
```

如果大家都认为“别人会恢复”，就是 orphan failure。

如果大家都恢复，就是 duplicate recovery。

---

#### 6.2.78 Side Effect Ownership

有真实 Action 时必须回答：

```text
Who may execute?
Who approves?
Who records effect?
Who verifies effect?
Who may retry?
```

尤其是：

```text
send
pay
delete
publish
modify
```

等不可逆或高风险操作。

---

#### 6.2.79 Parallel Side Effects 比 Parallel Reasoning 更危险

并行搜索通常只是多花钱。

并行写操作可能造成：

```text
duplicate order
conflicting edit
race condition
double notification
```

因此：

> **Reasoning 可以大胆并行，Side Effect 应更保守地串行化、加锁、幂等化或审批。**

---

#### 6.2.80 Idempotency 是 Multi-Agent Recovery 的基础设施

如果 Action 支持稳定 idempotency key：

```text
same logical action
→ repeated request
→ one effective mutation
```

那么系统才能更安全地处理：

```text
timeout
retry
worker crash
message duplication
```

这是 Runtime / Tool Contract 与 Orchestration 的连接点。

---

#### 6.2.81 Backpressure

当 Worker 产生任务的速度高于下游处理能力时：

```text
queue grows
latency grows
cost grows
stale work grows
```

所以并发不是只设一个 `max_workers`。

还要考虑：

```text
queue length
priority
rate limit
cancellation
backpressure
```

---

#### 6.2.82 Cancellation 也是 Orchestration 能力

如果 Global Goal 已经满足：

```text
remaining workers
```

可能已经没有继续运行价值。

可靠系统应该能够：

```text
cancel
ignore stale result
reclaim budget
```

否则 Parallelism 会制造大量无效尾部计算。

---

#### 6.2.83 Straggler Problem

并行系统的延迟常常被最慢 Worker 决定：

```text
Critical Path
≈ max(worker latency) + aggregation overhead
```

如果等待所有 Worker：

一个极慢 Worker 可能拖住全局。

可以考虑：

```text
timeout
partial aggregation
quorum
early stopping
backup worker
```

---

#### 6.2.84 Early Stopping

例如五个 Worker 找证据：

```text
已经获得足够独立证据
```

就可以停止剩余搜索。

这可以看作 Multi-Agent 版本的：

> **Minimal Sufficient Retrieval / Minimal Sufficient Evidence。**

---

#### 6.2.85 Orchestration 的第五个设计对象：Aggregation Ownership

必须明确：

```text
谁负责读取 Worker 输出？
谁解决冲突？
谁决定可信度？
谁生成最终 Artifact？
```

如果“所有 Agent 都可以自由改最终答案”，责任边界会迅速模糊。

---

#### 6.2.86 Aggregator 不是简单 Summarizer

成熟 Aggregator 应处理：

```text
coverage
conflict
provenance
uncertainty
duplicate evidence
staleness
priority
```

而不仅仅是“把几段话写成一段”。

---

#### 6.2.87 Evidence-first Aggregation

对于研究、分析、审计类任务，更稳健的模式是：

```text
Worker Result
→ Claims + Evidence + Provenance
→ Aggregator
→ reconcile claims
→ final synthesis
```

而不是：

```text
Worker Prose
→ More Prose
```

---

#### 6.2.88 Conflict Resolution 必须显式

两个 Worker 冲突：

```text
A says X
B says not X
```

系统可以：

```text
retrieve more evidence
invoke verifier
use authority ranking
mark unresolved
ask human
```

最差的做法是：

```text
LLM quietly blends both into a smooth sentence
```

---

#### 6.2.89 Orchestration 的第六个设计对象：Observability

Multi-Agent Trace 至少应该能回答：

```text
谁在什么时候拥有控制权？
谁委派给谁？
委派 Goal 是什么？
传了什么 Context？
用了哪些 Tool？
产生什么 Artifact？
发生什么 Side Effect？
为什么重试？
为什么终止？
```

否则系统出了问题只能看到最后一段答案。

---

#### 6.2.90 Trace 应保留因果链，而不只是消息列表

理想结构更像：

```text
Task
└── Delegation A
    ├── Tool Call A1
    ├── Worker Result A2
    └── Delegation B
        └── ...
```

而不是：

```text
Message 1
Message 2
Message 3
```

因为调试需要的是 causal structure。

---

#### 6.2.91 Multi-Agent 的关键 Trace ID

常见需要：

```text
task_id
run_id
agent_id
delegation_id
parent_delegation_id
span_id
artifact_id
action_id
```

这些 ID 能把：

```text
Global Task
↔ Local Runs
↔ Tool Calls
↔ Side Effects
```

重新串起来。

---

#### 6.2.92 Orchestration Failure 不能只看 Final Accuracy

如果最终答案正确，但系统发生：

```text
错误路由后碰巧被纠正
重复调用 8 个 Worker
产生一次重复 Side Effect
超出预算 5 倍
```

仍然是系统问题。

因此必须把 Process Metrics 纳入 Evaluation。

---

#### 6.2.93 Delegation Accuracy

可以评价：

> **需要委派时，是否把正确的 delegated goal 交给了合适的 Agent。**

它至少包含两部分：

```text
Should Delegate?
+
Delegate to Whom?
```

不要只统计“目标 Agent 选对率”。

---

#### 6.2.94 Unnecessary Delegation Rate

非常重要的成本指标：

```text
本可以由当前 Agent / Tool / Workflow 直接完成
却额外创建了 Agent delegation
```

这能直接检测：

> **Agent proliferation / over-orchestration。**

---

#### 6.2.95 Handoff Success Rate

不能只看 API 是否返回成功。

更完整的定义可以是：

```text
Handoff requested
→ target accepted
→ sufficient state transferred
→ target resumed correctly
```

缺一环都可能造成真实任务丢失。

---

#### 6.2.96 Handoff Information Loss

可以专门测：

```text
handoff 前必要约束集合
vs
handoff 后 target 实际获得并遵循的约束集合
```

这比只看最终结果更能定位 Context Transfer 问题。

---

#### 6.2.97 Duplicate Work Rate

衡量：

```text
多个 Worker 是否重复做了本不需要重复的搜索、分析、生成或工具调用
```

注意：

如果重复是为了 Independent Verification，不能简单算浪费。

所以需要区分：

```text
intentional redundancy
vs
accidental duplication
```

---

#### 6.2.98 Coordination Failure Rate

可以统计：

```text
misroute
lost handoff
state conflict
cyclic delegation
deadlock
livelock
duplicate action
merge failure
```

它比笼统的“Agent 失败率”更具有可诊断性。

---

#### 6.2.99 Cross-Agent Consistency

需要检查：

```text
shared facts
commitments
permissions
status
```

在多个 Agent 之间是否一致。

但不要追求所有局部观点都一致。

不同 Agent 保持不同 hypothesis 可能正是设计目标。

---

#### 6.2.100 Stale-State Rate

衡量：

> **Agent 做 Decision 时依赖的关键 State 中，有多少已经不是 authoritative latest state。**

这在并行与长任务中尤其重要。

---

#### 6.2.101 Orchestration Overhead

可以定义：

```text
Orchestration Cost
= routing
+ delegation
+ communication
+ aggregation
+ verification
+ coordination recovery
```

然后比较：

```text
Useful Worker Cost
vs
Orchestration Overhead
```

如果协调成本超过实际解决问题的成本，架构可能拆得过细。

---

#### 6.2.102 Critical-path Latency

Total latency 不应只把所有 Agent 时间相加。

对于并行 DAG，更应看：

```text
Critical Path
```

并拆成：

```text
routing latency
queue latency
worker latency
aggregation latency
verification latency
```

这样才能知道 Parallelism 是否真的带来收益。

---

#### 6.2.103 Parallel Efficiency

可以粗略看：

```text
Sequential-equivalent useful work
/
(actual critical-path time × allocated parallel capacity)
```

重点不是追求一个唯一公式。

而是避免看到“并行了”就假设“效率更高”。

---

#### 6.2.104 Recovery Metrics

可以继续复用前面已经建立的指标：

```text
Recovery Attempt Rate
Recovery Success Rate
Harmful Recovery Rate
Recovery Cost
Recovery Latency
No-progress Rate
Escalation Rate
False-success-after-recovery Rate
```

Multi-Agent 还应增加：

```text
Cross-agent Recovery Rate
Duplicate Recovery Rate
Orphan Failure Rate
```

---

#### 6.2.105 Oracle Decomposition

为了定位问题，可以做 controlled comparison：

```text
Learned / Agentic Decomposition
vs
Oracle Decomposition
```

如果 Oracle decomposition 下系统显著更好：

说明主要瓶颈可能在：

```text
planning / task decomposition
```

而不是 Worker capability。

---

#### 6.2.106 Oracle Routing

同理：

```text
Current Router
vs
Oracle Router
```

可以估计：

> **Routing error 对整体性能造成了多大的可恢复损失。**

这比直接更换整个 Multi-Agent 框架更科学。

---

#### 6.2.107 Oracle Aggregation

还可以把 Worker 输出固定，再比较：

```text
Current Aggregator
vs
Oracle / Human Aggregator
```

如果差距很大：

问题在结果整合，而不是 Worker。

这就是 failure localization。

---

#### 6.2.108 Multi-Agent Evaluation 必须有 Single-Agent Baseline

否则你无法回答：

> **这些额外 Agent 到底有没有创造净收益？**

至少比较：

```text
Task Success
Cost
Latency
Reliability
Side Effects
Recovery
```

最好还做相同预算下的 controlled comparison。

---

#### 6.2.109 同预算比较比“更多 Agent vs 一个 Agent”更公平

如果 Multi-Agent 使用：

```text
5 × tokens
4 × tool calls
3 × wall-clock resources
```

仅比较 Accuracy 很容易误导。

应同时看：

```text
quality–cost
quality–latency
quality–reliability
```

的 Pareto trade-off。

---

#### 6.2.110 安全边界：Prompt Injection 会跨 Agent 传播

例如：

```text
Research Worker reads malicious webpage
→ returns poisoned instruction-like text
→ Manager trusts summary
→ Action Agent executes
```

攻击可以沿 orchestration chain 传播。

所以 Agent 输出本身也可能是不可信输入。

---

#### 6.2.111 Agent Output ≠ Trusted Instruction

必须区分：

```text
Worker Output
= data / recommendation / artifact

Higher-level Instruction
= authorized control directive
```

不要因为输出来自“内部 Agent”就默认可信。

---

#### 6.2.112 Trust Boundary 必须穿过 Agent-to-Agent Interface

Agent 之间应考虑：

```text
source identity
authentication
authorization
schema validation
content filtering
provenance
```

尤其是跨进程、跨团队、跨组织或 A2A 场景。

---

#### 6.2.113 MCP 与 Orchestration 不在同一层

继续保持此前层级：

```text
MCP
= Host-facing Capability Interoperability Protocol

Orchestration
= multiple execution / decision entities 的 control organization
```

MCP 可以帮助 Agent 连接能力。

它并不自动决定多个 Agent 如何协作。

---

#### 6.2.114 A2A 与 Orchestration 也不应混淆

可以粗略理解：

```text
A2A / agent interoperability
→ Agent 怎样发现、描述、通信或协作

Orchestration
→ 系统怎样组织这些 Agent 的控制关系
```

协议可以支持 Orchestration。

协议本身不是 Orchestration Policy。

---

#### 6.2.115 Framework Graph ≠ Agent Architecture

很多框架提供：

```text
Node
Edge
Graph
```

但：

```text
Node
```

可能只是普通函数。

所以不能因为系统画成 Graph，就自动说它是 Multi-Agent。

判断仍然回到：

> **是否存在相对独立 Decision Loop 与 Control Ownership。**

---

#### 6.2.116 “多个 LLM Call”也不等于 Multi-Agent Orchestration

例如：

```text
Draft LLM Call
→ Critique LLM Call
→ Rewrite LLM Call
```

如果它们只是固定 Workflow 中的三个模型调用：

更准确的描述可能是：

```text
LLM Workflow
```

而不是多个独立 Agent。

---

#### 6.2.117 Anti-pattern：Role Theater

表现为：

```text
Research Agent
Writer Agent
Reviewer Agent
```

但三者：

```text
same context
same tools
same permissions
same policy
no local state
no real autonomy
```

只是换了三段 System Prompt。

这可能有 Prompt 分工价值，但不要夸大成强 Multi-Agent 架构收益。

---

#### 6.2.118 Anti-pattern：Context Ping-pong

A 把整段 Context 给 B。

B 再把更长的 Context 给 C。

C 再全部返回 A。

结果：

```text
Token Explosion
Information Duplication
Instruction Contamination
```

解决思路是 Interface + Artifact + Minimal Sufficient Context，而不是更多 summarization。

---

#### 6.2.119 Anti-pattern：Responsibility Diffusion

如果失败时每个 Agent 都可以说：

```text
“我只是把它交给了别人。”
```

说明系统缺少明确 Owner。

每个阶段至少应知道：

```text
Current Owner
Next Owner
Acceptance Condition
Escalation Owner
```

---

#### 6.2.120 Anti-pattern：Supervisor Bottleneck

所有 Worker 都必须向 Supervisor 汇报所有细节：

```text
Workers scale up
→ Supervisor context grows linearly or worse
→ latency / cost / error grow
```

解决方法可能是：

```text
hierarchical aggregation
artifact references
structured summaries
local verification
```

而不是简单换更大模型。

---

#### 6.2.121 Anti-pattern：Agent Proliferation

只要遇到一个新能力就新建 Agent：

```text
PDF Agent
CSV Agent
Search Agent
Email Agent
Calculator Agent
```

很多其实更适合作为：

```text
Tools
```

再次复用 6.1 的原则：

> **需要能力，优先 Tool；需要成熟方法，优先 Skill；需要固定流程，优先 Workflow；需要独立 delegated decision loop，才考虑另一个 Agent。**

---

#### 6.2.122 Anti-pattern：LLM Everywhere Orchestration

如果：

```text
是否重试
是否超时
是否有权限
是否达到预算
```

都让 LLM 决定：

系统会把本可确定的问题变成概率问题。

这些通常更适合 Harness / Runtime Policy。

---

#### 6.2.123 Anti-pattern：Hidden Side Effects

Worker 返回：

```text
“已处理。”
```

但 Manager 不知道它到底：

```text
read only?
modified file?
sent message?
created ticket?
charged money?
```

因此 Worker Result 应明确包含 Side Effects / Effect IDs。

---

#### 6.2.124 Anti-pattern：Silent Partial Failure

并行 5 个 Worker：

```text
4 success
1 timeout
```

Aggregator 仍然生成一个看似完整的答案。

这会形成：

```text
false success
```

应该把：

```text
coverage
missing branch
uncertainty
```

显式带到 Global State。

---

#### 6.2.125 Anti-pattern：Consensus Laundering

多个 Agent 重复了同一个未经验证的说法：

```text
A cites X
B copied X
C read B and repeats X
```

最终看起来像“多 Agent 共识”。

实际上只有一个 Evidence Source。

因此要追踪：

```text
Evidence Lineage
```

而不是只数同意票。

---

#### 6.2.126 设计 Orchestration 的第一问：能不能不拆？

先问：

```text
Single Agent + Tools
是否已经足够？
```

如果答案是“足够”：

不要因为框架支持 Multi-Agent 就拆。

---

#### 6.2.127 第二问：控制边界是否真的不同？

只有当任务存在真实不同的：

```text
Goal
State
Context
Capability
Authority
Failure Domain
Decision Ownership
```

才有更强理由形成独立 Agent 边界。

---

#### 6.2.128 第三问：Routing 是否可确定？

如果可以写成稳定规则：

```text
if X → A
if Y → B
```

优先 deterministic router。

只有难以经济编码的语义边界，才值得让 Agent / LLM 动态判断。

---

#### 6.2.129 第四问：应该 Call 还是 Handoff？

问：

> **原 Owner 是否还应该负责最终任务？**

如果是：

```text
Agents-as-Tools / worker call
```

如果不是，新的 Specialist 应成为 Owner：

```text
Handoff
```

---

#### 6.2.130 第五问：能不能并行？

检查：

```text
input dependency
shared state dependency
side-effect conflict
aggregation cost
```

只有独立性足够高时，Parallelism 才真正有价值。

---

#### 6.2.131 第六问：结果如何重新合成？

在启动 Worker 之前就应知道：

```text
谁聚合？
按什么标准？
冲突怎么办？
证据如何保留？
缺失结果怎么办？
```

否则 Fan-out 很容易，Fan-in 才成为真正瓶颈。

---

#### 6.2.132 第七问：失败由谁负责？

明确：

```text
local retry owner
reroute owner
fallback owner
escalation owner
global termination owner
```

Failure Ownership 不清晰，比 Worker 本身偶尔答错更危险。

---

#### 6.2.133 第八问：收益是否超过 Coordination Tax？

可以抽象成：

```text
Net Value
≈ specialization benefit
+ isolation benefit
+ parallelism benefit
+ verification benefit
- communication cost
- coordination cost
- aggregation cost
- reliability cost
- security cost
```

不需要真的得到一个精确数字。

它是架构思考框架。

---

#### 6.2.134 一个推荐的选择顺序

面对复杂任务，可以按：

```text
1. Single Agent + Tools
2. Single Agent + Skills / Retrieval
3. Deterministic Workflow
4. Workflow + bounded Agentic decisions
5. Manager + specialist workers
6. Handoffs / dynamic ownership
7. Hierarchical / distributed Multi-Agent
```

从简单到复杂逐层增加。

---

#### 6.2.135 Pattern 不是互斥选项

一个现实系统可以同时拥有：

```text
Deterministic Workflow
→ Router
→ Manager
→ Parallel Workers
→ Verifier
→ Handoff to Human
```

因此学习 Orchestration Patterns 的目标不是记“六种模式”。

而是理解每种模式解决哪一种 Control Problem。

---

#### 6.2.136 示例：Research System

一个较合理结构：

```text
User Goal
→ Manager
→ decompose research questions
→ parallel Search Workers
→ structured claims + sources
→ Evidence Aggregator
→ Verifier
→ Manager writes final answer
```

为什么不直接让 Worker 相互聊天？

因为真正需要的是：

```text
parallel evidence collection
+
centralized synthesis
+
independent verification
```

---

#### 6.2.137 Research System 的失败定位

如果最终答案漏掉关键证据，应依次看：

```text
Question decomposition wrong?
Correct worker absent?
Search recall low?
Worker discarded evidence?
Aggregation dropped claim?
Verifier missed coverage gap?
```

而不是一句：

> “Multi-Agent 没有效果。”

---

#### 6.2.138 示例：Customer Support

可以是：

```text
Front Door
→ Router
├── FAQ Agent
├── Billing Agent
├── Refund Agent
└── Technical Agent
```

如果 Specialist 需要直接接管对话：

```text
Handoff
```

如果 Front Door 仍统一负责用户回复：

```text
Agents-as-Tools
```

二者的核心差别仍是 Control Ownership。

---

#### 6.2.139 示例：Coding Agent

复杂代码修改可以是：

```text
Manager
→ inspect repository
→ dynamically split tasks
├── Worker A: backend
├── Worker B: tests
└── Worker C: docs
→ merge artifacts
→ run tests
→ verifier
```

但如果三个 Worker 会同时改同一个文件：

Parallelism 可能带来 merge conflict，反而不如串行。

---

#### 6.2.140 Coding Agent 的重要边界：Artifact Ownership

需要明确：

```text
Who owns which file / module / patch?
```

否则两个 Worker 都“成功”可能产生一个无法合并的全局结果。

所以 Artifact Boundary 也是 Orchestration Boundary。

---

#### 6.2.141 示例：高风险 Action System

可以拆成：

```text
Proposal Agent
→ Risk / Policy Verifier
→ Human Approval
→ Execution Agent
→ Effect Verifier
```

这里 Multi-Agent 的价值主要不是“更多智能”。

而是：

```text
Separation of Duties
Authority Isolation
Independent Verification
```

---

#### 6.2.142 Human 也可以是 Orchestration Node

现实 Agent 系统中：

```text
Human Approval
Human Escalation
Human Review
```

都是控制流的一部分。

所以 Orchestration 不应被写成纯 LLM-to-LLM 协作理论。

---

#### 6.2.143 Human-in-the-loop ≠ 所有步骤都人工确认

合理目标是：

```text
low-risk routine work
→ autonomous

high-risk / ambiguous / irreversible boundary
→ human gate
```

同样遵循 Minimal Sufficient Human Intervention。

---

#### 6.2.144 Orchestration 与 Harness 的连接

Chapter 6 讨论的是 Multi-Agent 结构。

真正落实这些规则通常依赖 Chapter 7 Harness：

```text
Agent Loop Policy
Tool Policy
Subagent Policy
Permission Policy
Approval Policy
Termination Policy
Recovery Policy
```

所以：

> **Orchestration Pattern 描述结构，Harness Policy 负责把结构变成可执行控制规则。**

---

#### 6.2.145 Orchestration 与 Runtime 的连接

Runtime 负责：

```text
process / task execution
queue
concurrency
checkpoint
persistence
sandbox
resume
fault tolerance
```

因此：

```text
Manager 想并行
```

并不等于系统真的具有可靠并行执行能力。

Runtime 必须提供 execution substrate。

---

#### 6.2.146 Orchestration 与 Evaluation 的连接

没有 Evaluation，就无法回答：

```text
为什么要增加 Agent？
哪种 Pattern 更好？
Routing 是否正确？
Parallelism 是否值？
Handoff 是否丢信息？
```

所以 Multi-Agent 架构决策最终必须回到 controlled evaluation。

---

#### 6.2.147 2026 年值得保留的现实观察：Code Orchestration 与 LLM Orchestration 并存

当前主流 Agent SDK 已经越来越明确地区分两类控制方式：

```text
Code Orchestration
→ flow primarily determined by application logic

LLM Orchestration
→ model dynamically decides next action / delegation
```

成熟系统通常组合两者，而不是二选一。

这与本体系一直强调的 deterministic workflow + agentic decision 完全一致。

---

#### 6.2.148 OpenAI Agents SDK 的 Manager 与 Handoff 是实现例，不是理论边界来源

当前 OpenAI Agents SDK 把常见多 Agent 组织方式明确区分为：

```text
Agents as tools
→ manager keeps control

Handoffs
→ selected specialist becomes active owner
```

这个实现非常适合帮助理解 Control Ownership。

但本体系关注的是背后的稳定抽象，而不是绑定某个 SDK API。

---

#### 6.2.149 Anthropic 的 Routing / Parallelization / Orchestrator–Workers / Evaluator–Optimizer 也是 Pattern 视角

Anthropic 的工程总结强调：

```text
Routing
Parallelization
Orchestrator–Workers
Evaluator–Optimizer
```

这些模式的价值在于说明：

> **不同任务结构需要不同控制拓扑，不存在“一个 Multi-Agent Pattern 适合所有问题”。**

---

#### 6.2.150 框架术语会变，控制问题不会变

未来可能出现更多名字：

```text
Swarm
Team
Crew
Graph
Society
Mesh
Fleet
```

学习时不要被名称牵着走。

永远先问：

```text
Control Owner?
State Owner?
Authority Owner?
Artifact Owner?
Failure Owner?
```

---

#### 6.2.151 一套完整的 Orchestration Failure Localization Pipeline

当 Multi-Agent 系统失败时，可以按：

```text
1. Goal 是否正确分解？
2. 是否真的应该委派？
3. 正确 Agent 是否存在 / 可见 / 可用？
4. Router 是否选对？
5. Delegation Contract 是否完整？
6. Context 是否充分且不过载？
7. 权限是否正确？
8. Worker 是否正确完成局部任务？
9. Result 是否结构化返回？
10. Provenance / Uncertainty 是否保留？
11. Aggregator 是否正确消费？
12. Global State 是否同步？
13. Verifier 是否有效？
14. Recovery 是否正确？
15. Termination 是否正确？
```

这比“再优化一下 Supervisor Prompt”更有诊断价值。

---

#### 6.2.152 Orchestration Design Checklist

设计前至少回答：

- 为什么不是 Single Agent？
- 为什么不是 Tool / Skill / Workflow？
- Agent 边界依据是什么？
- Global Control Owner 是谁？
- Global State Owner 是谁？
- Routing 是 deterministic 还是 agentic？
- Delegation Contract 是什么？
- Context 如何裁剪？
- Permission 如何缩减？
- 哪些任务并行？
- Fan-in 如何聚合？
- 谁验证？
- 谁处理 conflict？
- 谁负责 retry / recovery？
- Global Termination 是什么？
- 如何 Trace？
- 与 Single-Agent baseline 相比收益是什么？

---

#### 6.2.153 面试：什么是 Multi-Agent Orchestration？

推荐回答：

> **Multi-Agent Orchestration 是组织多个相对独立 Agent / Worker 的控制机制，决定任务如何拆分和委派、谁在什么时候拥有控制权、Context / State / Authority 如何流动、任务怎样串行或并行执行、多个结果如何聚合验证，以及失败恢复和全局终止由谁负责。它不等于让多个模型聊天，也不要求 Orchestrator 本身一定是 Agent。**

---

#### 6.2.154 面试：Manager 与 Handoff 的核心区别是什么？

回答：

```text
Manager / Agents-as-Tools
→ original manager retains control

Handoff
→ control ownership transfers to specialist
```

所以不要只说“一个是调用，一个是转发”。

真正稳定的区别是 Control Ownership。

---

#### 6.2.155 面试：什么时候适合 Parallel Workers？

回答要包含：

```text
subtasks sufficiently independent
shared-state conflict low
aggregation cost acceptable
parallel resource available
critical-path benefit meaningful
```

并补一句：

> **Parallelism 降低的主要是 critical-path latency，不自动降低 total token / compute cost。**

---

#### 6.2.156 面试：为什么 Orchestrator 不一定是 Agent？

因为 Orchestration 是 Control Responsibility。

固定规则、Workflow Engine、Scheduler、普通代码都可以协调多个 Agent。

只有当下一步控制决策本身处在 Uncertainty Frontier，才更有理由让 LLM / Agent 参与。

---

#### 6.2.157 面试：Multi-Agent 为什么更难调试？

因为失败不再只有：

```text
model reasoning error
```

还可能来自：

```text
decomposition
routing
delegation
context transfer
state synchronization
permission
aggregation
recovery
termination
```

因此必须有 causal trace 与 failure localization。

---

#### 6.2.158 面试：怎么判断 Multi-Agent 是否真的有收益？

至少做：

```text
Single-Agent baseline
vs
Multi-Agent
```

同时测：

```text
Task Success
Cost
Latency
Reliability
Coordination Failure
Side Effects
Recovery
```

必要时再做：

```text
Oracle Decomposition
Oracle Routing
Oracle Aggregation
```

定位理论上限。

---

#### 6.2.159 长期原则一：Orchestration 的本质是控制权流动

> **Multi-Agent 的难点不是让多个模型说话，而是让 Control、State、Authority 与 Responsibility 在多个 Decision Loop 之间可解释地移动。**

---

#### 6.2.160 长期原则二：Orchestrator 不必是 Agent

> **能由 deterministic code 稳定决定的控制流，不需要为了“agentic”而交给模型。**

---

#### 6.2.161 长期原则三：Delegation without Contract is Context Dump

> **一次可靠委派必须有 Goal、Scope、Context、Authority、Output、Success 与 Failure Semantics。**

---

#### 6.2.162 长期原则四：Parallelism is not Free

> **并行只有在 Independence Benefit 大于 Coordination / Merge Cost 时才有意义。**

---

#### 6.2.163 长期原则五：Consensus is not Ground Truth

> **多个 Agent 同意，只能说明输出一致；如果错误高度相关、证据同源，就不能把共识当成独立验证。**

---

#### 6.2.164 长期原则六：Shared Context is not Free

> **跨 Agent 共享的目标不是“信息最多”，而是让每个 Decision Loop 获得完成局部任务所需的最少充分信息。**

---

#### 6.2.165 长期原则七：Local Success is not Global Success

> **Worker 完成局部任务，不代表 Delegation 成功；Delegation 成功，也不代表 Global Goal 已完成。**

---

#### 6.2.166 长期原则八：Failure Ownership 必须显式

> **谁负责 Retry、Reroute、Fallback、Escalation 与 Global Termination，不能依赖 Agent 自己猜。**

---

#### 6.2.167 长期原则九：Use the Minimum Sufficient Orchestration

> **能用 Tool 不拆 Agent；能用 Workflow 不制造动态控制；能中心化就不无意义分布式；只有真实收益超过 Coordination Tax 时才增加 Orchestration Complexity。**

---

#### 6.2.168 一句话总结

> **Multi-Agent Orchestration 的核心不是安排“几个 Agent 按什么顺序说话”，而是建立一套明确的控制协议：谁拥有当前任务、怎样委派、传递多少 Context 与 Authority、哪些工作可以并行、结果怎样被聚合和验证、失败由谁恢复、全局状态由谁维护以及何时终止；最稳健的系统通常用 deterministic workflow 承担确定性控制，只在真正的 Uncertainty Frontier 引入 agentic routing、decomposition 与 delegation。**

---

#### 6.2.169 参考资料

1. OpenAI. *Agents SDK — Agent Orchestration*. https://openai.github.io/openai-agents-python/multi_agent/ 。关于 LLM orchestration、code orchestration、Agents-as-Tools、Handoffs 与 parallel execution 的当前工程实践。
2. OpenAI. *Agents SDK — Handoffs*. https://openai.github.io/openai-agents-python/handoffs/ 。关于控制转移与 specialist handoff 的实现语义。
3. Anthropic. *Building Effective Agents*. https://www.anthropic.com/engineering/building-effective-agents 。关于 routing、parallelization、orchestrator-workers、evaluator-optimizer，以及优先采用简单可组合模式的工程经验。
4. Wooldridge, M. *An Introduction to MultiAgent Systems*. Wiley, 2009. 关于 Multi-Agent coordination、interaction 与组织结构的经典基础。
5. Shoham, Y., Leyton-Brown, K. *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations*. Cambridge University Press, 2008. 关于多主体交互与协调问题的理论基础。
6. Google. *Agent Development Kit (ADK) API Reference*. https://google.github.io/adk-docs/ 。当前实现中包含 SequentialAgent、ParallelAgent、LoopAgent 等 workflow-oriented orchestration primitives，可作为“控制流不必由 LLM 决定”的实现例。
