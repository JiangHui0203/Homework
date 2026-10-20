#### 6.7.71 Artifact Failure

Artifact failure 不只有“文件没返回”。

还包括：

```text
missing artifact
partial artifact
schema-invalid artifact
wrong artifact version
stale artifact
corrupted artifact
untrusted artifact
artifact belongs to wrong task
artifact contradicts completion state
```

因此 Artifact evaluation 应至少检查：

- presence；
- completeness；
- validity；
- provenance；
- task association；
- semantic correctness。

---

#### 6.7.72 False Completion：最危险的 remote success

最危险的状态之一不是显式 failure，而是：

```text
Task = completed
Artifact = returned
But real objective = not achieved
```

例如：

```text
"ticket created"
```

实际上只是生成了一段模拟 ticket text。

这就是：

> **False Success / False Completion**

它要求上游做 outcome verification，而不是只相信 remote status。

---

#### 6.7.73 Remote Status ≠ Ground Truth

Remote Agent 的 status 是对方系统提供的 observation。

它可能：

- 正确；
- stale；
- delayed；
- buggy；
- overly optimistic；
- semantically different from local definition。

所以延续 Chapter 3 的原则：

> **Tool Result ≠ Observation ≠ Ground Truth**

在 A2A 中对应为：

> **Remote Status / Artifact ≠ Verified Environment State**

---

#### 6.7.74 Recovery 的第一步通常是 Reconciliation

遇到：

```text
timeout
stream drop
unknown state
partial response
```

不应首先问：

```text
"要不要 retry？"
```

而应先问：

```text
"远端当前真实 task state 是什么？"
```

因此推荐恢复链路：

```text
Failure / Ambiguity
      ↓
Reconcile Existing Task
      ↓
Recover Latest State / Artifact
      ↓
Check Side Effects
      ↓
Then choose:
   resume / retry / cancel / compensate / reroute / escalate
```

---

#### 6.7.75 Retry、Resume、Reroute、Compensate 是四种不同恢复动作

**Retry**：重新尝试当前操作。

**Resume**：继续同一个已有 Task。

**Reroute**：把目标交给另一个 Agent。

**Compensate**：对已经发生的副作用执行补偿。

不能混成：

```text
失败了 → 再来一次
```

因为跨 Agent 长任务常常已经改变外部世界。

---

#### 6.7.76 Reroute 前必须知道原任务是否仍活着

危险模式：

```text
Agent B timeout
→ immediately delegate same task to Agent C
→ B recovers and completes
→ C also completes
```

最终可能出现 double effect。

因此 reroute 前需要明确：

```text
Can B be canceled?
Was B already committed?
Is task idempotent?
Can results coexist?
```

这本质上仍是 Coordination Failure 的一部分。

---

#### 6.7.77 A2A 与 6.6 Coordination Failure 的关系

A2A 可以让任务跨 Agent 边界更标准地传播，但它不会自动维持全局 invariant。

例如：

```text
Supervisor
   ├── A2A → Agent B
   └── A2A → Agent C
```

协议可能全部成功，但仍可能出现：

- duplicate assignment；
- conflicting writes；
- dependency violation；
- stale ownership；
- premature termination；
- split-brain decision。

所以：

> **A2A standardizes interaction; Coordination logic preserves global correctness.**

---

#### 6.7.78 A2A 与 Shared / Private Context 的关系

A2A 不应该被理解成：

```text
"把两个 Agent 的全部 Context 合并"
```

更合理的是：

```text
Private State A
     ↓ selective projection
A2A Message / Task
     ↓
Private State B
```

因此跨 Agent context sharing 仍遵循 6.5 的原则：

> **Minimal Sufficient Visibility**

只传当前任务真正需要的：

- goal；
- constraints；
- necessary evidence；
- correlation IDs；
- output contract。

而不是把全部 history、memory、secret 都发送过去。

---

#### 6.7.79 A2A 与 Capability Discovery 的关系

第 5 章已经建立：

```text
Capability Universe
→ Discovery
→ Candidate Action Space
→ Selection
```

A2A 将其中一个 capability category 扩展成：

```text
Remote Agents
```

因此完整路由可以是：

```text
Current Goal / State
       ↓
Need local tool, skill, workflow, or remote agent?
       ↓
Capability Discovery
       ↓
Candidate Tools / Skills / Agents
       ↓
Policy + Trust + Cost + Risk
       ↓
Selection
       ↓
Local execution or A2A delegation
```

A2A 不应绕过统一 capability governance。

---

#### 6.7.80 Agent Registry 不应直接变成模型的无限菜单

随着 remote agents 增加：

```text
10 agents
100 agents
10,000 agents
```

把所有 Agent Card 直接放进 prompt 会导致：

- context explosion；
- selection confusion；
- security exposure；
- irrelevant capability noise；
- stale descriptions。

因此应该复用：

> **Minimal Sufficient Capability Exposure**

即先通过 registry / retriever / policy 缩小 candidate set，再让模型做最终选择。

---

#### 6.7.81 最小生产级 A2A Client 应拥有什么

一个可靠 client 不只是：

```text
send_message()
```

至少需要：

```text
Agent Discovery
Capability / Interface Resolution
Authentication
Authorization / Policy Check
Task Correlation
State Tracking
Timeout Handling
Retry / Reconciliation
Artifact Validation
Outcome Verification
Tracing / Audit
Cost / Latency Accounting
```

因此 A2A client 本身最终仍会落入 Chapter 7 Harness 的治理范围。

---

#### 6.7.82 最小生产级 A2A Server 应拥有什么

Remote side 至少需要清晰处理：

- Agent Card lifecycle；
- interface/version declaration；
- authentication；
- authorization；
- message validation；
- task identity；
- task state transitions；
- cancellation；
- streaming / async update；
- artifact publication；
- audit；
- isolation；
- failure semantics。

否则只是：

```text
"套了一个 A2A endpoint"
```

而不是可靠 remote-agent service。

---

#### 6.7.83 Deterministic Shell 仍然适用于 A2A

即使 remote agent 内部高度自治，跨边界治理最好尽可能确定性：

```text
Model decides whether delegation is useful
      ↓
Deterministic policy checks authorization
      ↓
Deterministic protocol client submits
      ↓
Remote agent executes autonomously
      ↓
Deterministic state machine tracks status
      ↓
Verifier evaluates artifact / outcome
```

所以仍然遵循：

> **把不确定性留给语义决策，把协议、权限、状态机和副作用保护尽可能留给确定性系统。**

---

#### 6.7.84 Human Approval 应该放在哪里

高风险 A2A delegation 可能需要人工批准。

常见 gate：

```text
Before delegation
→ 是否允许把敏感数据交给 remote agent？

Before high-risk remote action
→ 是否允许产生真实副作用？

Before accepting result
→ 是否允许把结果提交到下游关键系统？
```

Human approval 不是简单插一个聊天框，而是：

```text
Policy-defined state transition
```

必须能被 audit。

---

#### 6.7.85 Observability：需要跨 Agent 的 causal trace

如果一次任务经过：

```text
Agent A
  ↓ A2A
Agent B
  ↓ Tool
Database
  ↓
Agent B
  ↓ A2A
Agent A
```

仅看单个服务日志无法解释完整 failure chain。

至少需要关联：

- parent goal / run ID；
- delegation ID；
- task ID；
- message ID；
- context ID；
- remote trace / span；
- tool calls；
- artifact IDs；
- verification result。

目标不是记录所有内部思维，而是恢复：

> **谁在什么状态下，把什么任务交给谁，发生了什么外部动作，返回了什么，最终为什么成功或失败。**

---

#### 6.7.86 最小 Trace 结构

可以抽象为：

```text
Run R
 └── Delegation D1
      ├── discover Agent B
      ├── select interface
      ├── submit Message M1
      ├── Task T1 created
      ├── state: submitted
      ├── state: working
      ├── Artifact A1
      ├── state: completed
      ├── verify A1
      └── accept / reject result
```

这比仅保存：

```text
"Agent B returned success"
```

有高得多的诊断价值。

---

#### 6.7.87 A2A Evaluation 不应只做 connectivity test

最弱的评测是：

```text
Can client connect to server?
```

但生产级互操作还需要评估：

```text
Discovery
Compatibility
Routing
Authentication
Task semantics
State synchronization
Artifact integrity
Recovery
Security
End-to-end correctness
```

因此 A2A evaluation 应该是 protocol + behavior + outcome 三层。

---

#### 6.7.88 Discovery 指标

可以评估：

```text
Agent Discovery Recall
Agent Discovery Precision
Relevant Agent Recall@K
Stale Card Rate
Unauthorized Exposure Rate
```

其中最关键的是：

> **如果正确 Agent 没进入 candidate set，后面的 selector 不可能修复。**

因此 Discovery Recall 仍然是 downstream selection 的上界之一。

---

#### 6.7.89 Selection / Routing 指标

在 candidate set 已包含正确 Agent 后，可以评估：

```text
Agent Selection Accuracy
Top-k Routing Accuracy
Wrong-Agent Delegation Rate
Unnecessary Remote Delegation Rate
Abstention Accuracy
```

对于高风险系统，还应看：

```text
Risk–Coverage
```

即系统在不同 delegation coverage 下的错误率与收益。

---

#### 6.7.90 Interoperability Matrix

真正验证协议兼容，应覆盖：

```text
Client implementation
× Server implementation
× protocol version
× protocol binding
× security scheme
× extension set
```

可以形成矩阵：

| Client | Server | Binding | Version | Auth | Result |
|---|---|---|---|---|---|
| C1 | S1 | HTTP+JSON | 1.x | OAuth | PASS |
| C1 | S2 | gRPC | 1.x | mTLS | PASS |
| C2 | S1 | HTTP+JSON | 1.x | OAuth | FAIL |

这样才能发现真正的 cross-implementation failure。

---

#### 6.7.91 Task Lifecycle 指标

值得长期保留的指标包括：

```text
Task Acceptance Rate
Task Completion Rate
Task Failure Rate
Task Rejection Rate
Cancellation Success Rate
Input-required Rate
Auth-required Rate
Unknown-state Rate
Median / P95 Task Duration
State Staleness Rate
```

但这些都不能单独替代 end-to-end correctness。

---

#### 6.7.92 Reliability 指标

对于 fault-prone distributed execution，可额外统计：

```text
Duplicate Task Rate
Duplicate Effect Rate
Lost Update Rate
Recovery Success Rate
Resubscription Success Rate
Retry Amplification
False Completion Rate
Artifact Corruption Rate
```

这里尤其应该保留：

> **Duplicate Work 与 Duplicate Effect 分开。**

前者主要浪费资源，后者可能真正破坏环境。

---

#### 6.7.93 Cost / Latency 指标

Remote delegation 不是免费的。

总成本可能包括：

```text
Discovery latency
Authentication latency
Network latency
Remote inference cost
Remote tool cost
Queue delay
Streaming overhead
Verification cost
Retry cost
```

因此比较：

```text
Local execution
vs
Remote Agent delegation
```

应看 Pareto trade-off：

```text
Quality × Reliability × Cost × Latency
```

而不是只问“多 Agent 更强吗”。

---

#### 6.7.94 Fault Injection：A2A 特别适合做系统性故障注入

可以主动注入：

```text
stale Agent Card
wrong protocol version
expired credential
stream disconnect
lost terminal event
delayed artifact
duplicate delivery
remote timeout
cancellation race
partial artifact
```

然后观察：

```text
Does system detect?
Does it reconcile?
Does it retry safely?
Does it avoid duplicate effects?
Does it escalate correctly?
```

这比只跑 happy-path benchmark 更接近真实可靠性。

---

#### 6.7.95 Oracle Decomposition：到底是哪一层限制了表现

当 A2A 系统成功率不高时，可以构造 oracle：

```text
Oracle Discovery
Oracle Agent Selection
Oracle Compatibility
Oracle Task Execution
Oracle Artifact Verification
```

例如：

```text
real system = 68%
oracle discovery = 71%
oracle routing = 82%
oracle remote execution = 91%
```

就可以判断主要瓶颈在哪一层。

避免把所有失败都归因于模型“不会合作”。

---

#### 6.7.96 一个完整示例：Research Agent 委派 Data Agent

用户要求：

```text
分析公司过去四季度营收，并给出趋势解释。
```

Research Agent 发现自己没有内部财务库权限。

可能流程：

```text
Research Agent
   ↓ discover
Finance Data Agent Card
   ↓ skill / policy check
skill = quarterly_financial_data
   ↓ auth
obtain scoped credential
   ↓ A2A message
request company + periods + fields
   ↓
Finance Data Agent
   ↓
Task T42 = submitted
   ↓
working
   ↓
Artifact: financials.json
   ↓
completed
   ↓
Research Agent validates schema + periods + provenance
   ↓
uses data for analysis
   ↓
final answer
```

这里 A2A 负责的是：

```text
remote agent boundary
```

真正最终答案质量仍取决于：

```text
discovery + selection + finance data correctness + verification + research reasoning
```

---

#### 6.7.97 同一个例子里可能出现哪些失败

可以沿链路逐层定位：

```text
1. Finance Agent 未被 discover
2. 发现了但选错另一个 Agent
3. credential scope 不够
4. interface version 不兼容
5. task 被创建但排队过久
6. stream 断开
7. artifact 少一个季度
8. task 标记 completed
9. Research Agent 未校验 artifact
10. 最终分析基于缺失数据
```

如果最后只标：

```text
Answer Wrong
```

几乎无法指导改进。

---

#### 6.7.98 什么时候根本不需要 A2A

不要把 A2A 当成 Agent 系统的默认必选组件。

如果：

```text
单进程内部 worker
同一框架中的简单 subagent
固定、稳定、低延迟内部调用
普通工具能力即可表达
```

直接 function / internal RPC / workflow 可能更简单。

使用 A2A 的合理条件通常是：

```text
真正存在独立 agent boundary
+
需要可移植 interoperability contract
```

这与整本书的原则一致：

> **不要为了 agentic form 引入不必要的系统复杂度。**

---

#### 6.7.99 A2A 的 Complexity Tax

引入 remote Agent 会增加：

- network boundary；
- failure modes；
- auth；
- task state；
- tracing；
- cost attribution；
- version compatibility；
- data governance；
- coordination；
- recovery。

所以必须证明：

```text
remote-agent autonomy / specialization / ownership benefit
>
integration + coordination + reliability cost
```

否则直接使用 Tool / Workflow 可能更好。

---

#### 6.7.100 2026 的关键变化：A2A 已从早期草案走向稳定协议栈

截至 2026 年，A2A 的重要演进不是“又多了一个 Agent 框架”，而是互操作协议逐渐成熟：

- v1.0 被定位为稳定、production-ready 的主版本；
- v1.x 更明确区分 semantic model 与 protocol bindings；
- Agent Card 使用更明确的 interface declaration；
- 标准 binding 不再只围绕单一 JSON-RPC 形态；
- compatibility / version negotiation 更成为一等问题；
- 社区继续推进 v1.1、BiDi streaming、multi-turn / elicitation、validation 与 TCK 等方向。

因此学习 A2A 时不要把早期某个 SDK 代码片段当成长期定义。

应该抓住稳定核心：

> **Discovery + Contract + Task Lifecycle + Message / Artifact + Security + Interoperability**

---

#### 6.7.101 不要死记某个 transport 细节

协议会继续演化。

长期稳定的知识优先级应是：

```text
第一层：为什么需要 Agent interoperability
第二层：Agent Card / Message / Task / Artifact 语义
第三层：discovery / trust / task lifecycle / recovery
第四层：protocol binding / SDK / concrete endpoint
```

面试和工程中最有价值的是前三层。

第四层需要使用时查当前 specification。

---

#### 6.7.102 A2A 的核心设计哲学

可以压缩成六句话：

1. **Agent 可以互操作，而不需要暴露内部实现。**
2. **能力发现必须先于远程委派。**
3. **长任务需要显式 lifecycle，而不是假装一次 RPC 就结束。**
4. **Message 用于交互，Artifact 用于交付。**
5. **协议成功不等于任务成功，更不等于用户目标成功。**
6. **跨 Agent 边界必须重新建立 trust、policy、verification 与 observability。**

---

#### 6.7.103 A2A 面试最常见的一阶问题

**Q：A2A 是什么？**

高质量回答：

> A2A 是面向独立 Agent 系统之间通信与互操作的开放协议。它通过 Agent Card 描述能力和连接方式，通过 Message / Part 交换信息，通过 stateful Task 管理长任务，并通过 Artifact 交付结果。它标准化跨 Agent 的交互边界，但不替代 Agent 内部推理、delegation policy、coordination、trust 或 outcome verification。

---

#### 6.7.104 二阶追问：A2A 和 MCP 有什么区别

不要只回答：

```text
MCP 连工具，A2A 连 Agent
```

应该继续解释：

```text
MCP 主要解决 Host / Agent 如何以标准方式连接 Tool、Resource 等 capability；
A2A 主要解决独立 agentic application 如何发现对方、交换消息、委派与跟踪 stateful task、接收 artifact。
```

最后补一句：

> 两者可以组合：Agent B 可以通过 A2A 被 Agent A 调用，同时 Agent B 内部再通过 MCP 使用工具。

---

#### 6.7.105 二阶追问：为什么不能直接 REST API

答案不是：

```text
REST 不行
```

而是：

> 普通 REST 完全可以实现两个系统之间的连接；A2A 的价值是把 Agent 特有的 discovery、capability description、task lifecycle、message/artifact semantics、streaming/async 与 interoperability contract 标准化，从而减少每一对 Agent 都自定义协议的成本。

因此：

```text
A2A is not magic transport
A2A is standardized agent interaction semantics
```

---

#### 6.7.106 三阶追问：Agent Card 能不能用来做 routing

可以，但不能直接等同。

合理流程是：

```text
Agent Card
→ candidate capability representation
→ retrieval / filter
→ policy / trust / compatibility
→ routing / selection
```

Card 是 routing evidence，不是 routing decision。

---

#### 6.7.107 三阶追问：Task completed 以后还要做什么

至少回答：

```text
validate artifact
verify business outcome
check side effects
update local state
record provenance / trace
```

关键一句：

> **Remote `completed` 是对端状态，不是调用方的最终 acceptance decision。**

---

#### 6.7.108 三阶追问：如何避免 timeout 后重复执行

高质量答案应包含：

```text
stable task identity
reconciliation before retry
idempotency / deduplication
side-effect-aware retry policy
resume existing task when possible
```

而不是只说：

```text
exponential backoff
```

Backoff 解决请求压力，不解决重复副作用。

---

#### 6.7.109 三阶追问：如何评估 A2A 系统

应该分层：

```text
Discovery
→ relevant Agent recall

Routing
→ selection accuracy

Interoperability
→ client/server/version/binding compatibility

Task Lifecycle
→ completion / stale state / unknown state

Reliability
→ duplicate effect / recovery

Outcome
→ end-to-end goal correctness

Efficiency
→ cost / latency / critical path
```

这比“接口调通率”完整得多。

---

#### 6.7.110 一个稳定的系统边界图

最终把 Chapter 3–6 连接起来：

```text
                         ┌─────────────────────┐
                         │      Agent A        │
                         │ Decision / Harness  │
                         └───────┬───────┬─────┘
                                 │       │
                     MCP / Tool  │       │ A2A
                                 ↓       ↓
                    ┌──────────────┐  ┌─────────────────────┐
                    │ Capability   │  │      Agent B        │
                    │ Tool / Data  │  │ Decision / Harness  │
                    └──────────────┘  └──────────┬──────────┘
                                                │
                                     MCP / Tool │
                                                ↓
                                      ┌─────────────────┐
                                      │ Capability /    │
                                      │ External System │
                                      └─────────────────┘
```

其中：

```text
Tool Calling
= model-facing action expression

MCP
= capability interoperability

A2A
= agent interoperability

Harness
= local policy / control / verification layer

Runtime
= actual execution layer
```

---

#### 6.7.111 Chapter 6 的完整逻辑链

到这里，Multi-Agent & Agent Interoperability 可以形成完整闭环：

```text
6.1 Why Multi-Agent?
→ 什么时候值得引入多个 Agent

6.2 Roles & Topologies
→ 多个 Agent 如何组织

6.3 Delegation
→ 工作如何被交给别的 Agent

6.4 Agent Communication
→ 信息如何传递

6.5 Shared / Private Context
→ 谁能看到、相信、修改什么状态

6.6 Coordination Failure
→ 多个局部正确单元为什么仍会破坏全局正确性

6.7 A2A
→ 独立 Agent 系统如何跨实现 / 组织边界标准化互操作
```

因此 Chapter 6 不是在鼓励“Agent 越多越好”，而是在回答：

> **当系统确实需要多个自治执行单元时，如何组织、委派、通信、控制可见性、维持全局一致性，并在跨系统边界上实现可靠互操作。**

---

#### 6.7.112 Chapter 6 最终原则：Autonomy 必须配套 Contract

Agent 越自治，系统越不能只依赖“大家自己理解”。

需要越来越清晰的：

```text
Capability Contract
Delegation Contract
Communication Contract
State Contract
Ownership Contract
Effect Contract
Interoperability Contract
```

因此：

> **Autonomy without Contract produces ambiguity; Contract without verification produces false confidence.**

---

#### 6.7.113 Chapter 6 最终原则：Interoperability ≠ Shared Implementation

真正的 interoperability 不是要求：

```text
大家使用同一个框架
同一个模型
同一个 memory
同一个 tool stack
```

而是：

```text
内部实现可以不同
但跨边界契约可以被共同理解
```

这正是 A2A 的长期价值。

---

#### 6.7.114 Chapter 6 最终原则：Local Autonomy + Global Invariants

Multi-Agent 系统不是让每个 Agent 无限制自由行动。

更准确的是：

```text
Local autonomy
within
Global invariants
```

A2A 扩大了可连接的自治单元范围，但全局 invariant 仍必须由 Harness、policy、runtime、coordination 与 verification 共同保护。

---

#### 6.7.115 Chapter 6 最终原则：Minimal Necessary Coordination

跨 Agent 边界越多，同步所有信息的代价越高。

因此仍然遵循 6.6 已建立的原则：

> **只协调保护关键 invariant 所必需的状态、事件与决策。**

不要因为使用 A2A 就把所有 Agent 变成全局共享状态系统。

---

#### 6.7.116 Chapter 6 最终原则：Minimal Sufficient Visibility

Remote Agent 只应看到完成委派任务真正需要的信息。

稳定目标：

```text
enough context to succeed
+
minimum unnecessary exposure
```

这同时改善：

- privacy；
- security；
- context efficiency；
- semantic focus；
- blast radius。

---

#### 6.7.117 Chapter 6 最终原则：Verify Across Boundaries

系统边界越远，越不能把对端状态直接当成本地事实。

因此：

> **跨 Agent 边界的每一次关键结果，都应该有与风险相匹配的验证强度。**

例如：

```text
low-risk summary
→ lightweight schema / citation check

payment / deletion / deployment
→ strong external outcome verification
```

---

#### 6.7.118 最终一句话

如果只记住 A2A 一句话，可以记：

> **A2A 让独立、可能彼此 opaque 的 Agent 通过标准契约发现彼此、交换消息、管理任务和交付产物；它解决互操作边界，但真正的可靠 Agent 系统仍必须在协议之外处理选择、权限、协调、恢复与验证。**

---

#### 6.7.119 参考资料

1. A2A Protocol. *Specification v1.x*. 关于 Agent Card、Agent Interface、Message、Part、Task、Artifact、security scheme、protocol binding 与 interoperability 的规范定义。
2. A2A Protocol. *Core Concepts*. 关于 Agent Card、Task、Message、Part、Artifact 与 context 的核心语义。
3. A2A Protocol. *What is A2A?*. 关于 discovery、authentication、SendMessage / SendStreamingMessage 与完整请求生命周期。
4. A2A Protocol. *Agent Discovery*. 关于 well-known URI、registry / catalog、direct configuration、Card security 与 caching。
5. A2A Protocol. *Life of a Task*. 关于 stateless Message、stateful Task、contextId、interrupted / terminal state 与长任务生命周期。
6. A2A Protocol. *Streaming & Asynchronous Operations*. 关于 streaming、artifact updates、断线与 resubscription 等异步执行语义。
7. A2A Protocol. *What's New in v1.0*. 关于 v1.0 的 interface declaration、binding 与数据模型演进。
8. A2A Protocol. *Roadmap*（2026-09）. 关于 v1.1、BiDi Streaming、Elicitation / Multi-Turn Workflows、validation 与 TCK 的后续方向。
9. A2A Protocol / Agentic AI Foundation. *A New Chapter for A2A: Joining the Agentic AI Foundation*. 关于 A2A 的开放治理与跨框架互操作定位。
10. OpenTelemetry. *Tracing Concepts and Semantic Conventions*. 关于跨服务 trace / span / correlation 与 distributed observability。
11. OWASP. *LLM / Agentic AI Security Guidance*. 关于 excessive agency、prompt injection、跨 Agent trust boundary 与高风险副作用控制。

概念边界：

```text
Tool
= primitive capability

Tool Calling
= model-facing action expression

MCP
= Agent / Host ↔ Capability / Data / Tool interoperability

A2A
= Client / Agent ↔ Remote Agent interoperability

Multi-Agent
= system architecture with multiple autonomous decision units

Delegation
= policy decision to transfer responsibility for work

Coordination
= mechanisms that preserve global invariants across those units

Harness
= local control plane that decides what may happen and verifies what happened
```

最终必须保持：

```text
A2A ≠ Multi-Agent
A2A ≠ Delegation Policy
A2A ≠ Tool Calling
A2A ≠ MCP
Agent Card ≠ Trust Certificate
Discovery ≠ Selection
Task Completed ≠ User Goal Satisfied
Artifact Returned ≠ Outcome Verified
Protocol Success ≠ Task Success
Remote Status ≠ Ground Truth
```

---
