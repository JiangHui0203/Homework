### 6.7 A2A

#### 6.7.1 A2A 到底是什么

**A2A（Agent2Agent Protocol）** 是面向独立 Agent 系统之间通信与互操作的开放协议。

它要解决的核心问题不是：

```text
如何让一个 LLM 更会推理？
```

也不是：

```text
如何在同一个框架内部创建多个 subagent？
```

而是：

```text
当 Agent A 与 Agent B
由不同团队、不同框架、不同 runtime、不同厂商实现时，
它们如何在不了解彼此内部实现的前提下：

发现对方
→ 理解能力
→ 建立受控连接
→ 委派 / 接受任务
→ 交换消息与产物
→ 跟踪任务状态
→ 处理长任务与中断
→ 得到可验证结果
```

因此，A2A 的系统定位可以写成：

> **Agent ↔ Agent interoperability protocol**

它标准化的是**跨 Agent 边界的交互契约**，而不是 Agent 内部的 reasoning、memory、planner、tool loop 或 orchestration policy。

---

#### 6.7.2 为什么需要 A2A

在单一 Agent 平台内部，系统通常可以直接依赖内部对象：

```text
Python function
shared memory
internal queue
framework-specific state
subagent API
```

但一旦跨越团队或平台边界，这些假设迅速失效：

```text
Agent A: LangGraph
Agent B: custom runtime
Agent C: Java service
Agent D: vendor-managed agent
```

如果每一对 Agent 都定义一套私有协议，则集成复杂度近似增长为：

```text
A↔B
A↔C
A↔D
B↔C
B↔D
C↔D
...
```

这会产生：

- capability description 不一致；
- message schema 不一致；
- task state 不一致；
- authentication 方式不一致；
- streaming / async 语义不一致；
- retry / cancel 行为难以统一；
- observability 难以串联；
- vendor lock-in 加重。

A2A 的价值，就是把大量 pairwise integration 收敛到一个更稳定的协议边界。

---

#### 6.7.3 A2A 解决的是“互操作”，不是“智能”

这是理解 A2A 最重要的边界。

即使两个 Agent 完全遵守同一个 A2A 协议：

```text
Discovery OK
Authentication OK
Message delivered
Task created
Status updated
Artifact returned
```

也不代表：

```text
Agent 选对了对方
Agent 理解了任务
Agent 推理正确
Agent 完成了真实目标
Artifact 内容可信
全局系统协调正确
```

所以：

> **Protocol Correctness ≠ Task Correctness ≠ Global Correctness**

A2A 可以降低互操作摩擦，但不能替代：

- routing；
- delegation policy；
- trust decision；
- verification；
- coordination；
- governance；
- recovery；
- end-to-end evaluation。

---

#### 6.7.4 A2A 在整套 Agent 栈中的位置

可以把整体系统画成：

```text
User / Upstream Goal
        ↓
┌──────────────────────┐
│      Agent A         │
│ policy / memory /    │
│ planning / harness   │
└──────────┬───────────┘
           │
           │ A2A
           ↓
┌──────────────────────┐
│      Agent B         │
│ remote autonomous    │
│ agentic application  │
└──────────┬───────────┘
           │
           │ MCP / Tool API / Native Tool
           ↓
┌──────────────────────┐
│ Capability / Data /  │
│ Tool / External Sys  │
└──────────────────────┘
```

因此最简边界是：

```text
MCP：Agent / Host ↔ Capability / Data / Tool
A2A：Agent / Client ↔ Remote Agent
```

但这只是第一层理解。

真正工程上还必须继续区分：

```text
protocol
architecture
policy
runtime
trust
coordination
```

---

#### 6.7.5 A2A ≠ Multi-Agent Architecture

**Multi-Agent** 描述的是系统结构：

```text
一个任务中存在多个具有一定自治能力的 Agent，
它们通过 delegation、communication、coordination 共同完成目标。
```

**A2A** 描述的是互操作协议：

```text
两个独立 Agent 系统如何在标准边界上交换能力描述、消息、任务状态与结果。
```

所以：

```text
Multi-Agent without A2A   ✓
A2A between two services  ✓
A2A inside Multi-Agent    ✓
Multi-Agent = A2A         ✗
```

一个完全运行在同一进程内的 supervisor–worker 系统，可能根本不需要 A2A。

反过来，一个 shell client 或 CI job 也可以通过 A2A 把工作提交给 remote agent，而调用方本身未必是完整 Agent。

---

#### 6.7.6 A2A ≠ Delegation Policy

Delegation 回答：

```text
要不要把任务交给别人？
交给谁？
交多少？
何时收回？
```

A2A 回答：

```text
一旦决定与某个 remote agent 交互，
跨边界的信息和任务如何被标准化表达与传输？
```

因此：

> **A2A 可以承载 delegation，但不决定 delegation 是否正确。**

错误 routing 完全可能通过 A2A 被非常可靠地执行。

---

#### 6.7.7 A2A ≠ Tool Calling

Tool Calling 通常是：

```text
Model
  ↓
function / tool name + arguments
  ↓
Harness / Runtime
  ↓
Tool execution
```

A2A 更接近：

```text
Client Agent / Application
  ↓
Remote Agent contract
  ↓
Task / Message interaction
  ↓
Remote autonomous execution
```

Tool 往往暴露一个**能力原语**：

```text
search(query)
create_ticket(...)
query_database(...)
```

Remote Agent 则可能自行：

- 规划；
- 追问；
- 调多个工具；
- 长时间执行；
- 产生多个 artifact；
- 暂停等待输入；
- 处理自己的内部状态。

因此：

> **Tool Call 更像调用一个能力；A2A 更像把一个任务交给另一个自治执行单元。**

---

#### 6.7.8 A2A ≠ MCP

这两个协议最容易被混淆。

可以先记住：

```text
MCP
Agent / Host → 找能力、读资源、调用工具

A2A
Agent / Client → 找 Agent、发消息、委派任务、跟踪远程任务
```

进一步看：

| 维度 | MCP | A2A |
|---|---|---|
| 核心边界 | Host ↔ Capability Server | Client ↔ Remote Agent |
| 主要对象 | Tools / Resources / Prompts 等 | Agent Card / Message / Task / Artifact 等 |
| 自治性假设 | 服务暴露能力 | 对端可拥有独立 agentic runtime |
| 典型目的 | 扩展一个 Agent 的能力边界 | 连接独立 Agent 系统 |
| 长任务状态 | 不是核心抽象中心 | Task lifecycle 是核心语义之一 |
| 内部实现可见性 | 不要求暴露服务内部实现 | 不要求暴露 Agent 内部 state / memory / tools |

两者不是竞争关系，而是可组合关系：

```text
Agent A
   │
   ├── MCP → Search / DB / Files
   │
   └── A2A → Agent B
                 │
                 └── MCP → CRM / ERP / Internal Tools
```

---

#### 6.7.9 A2A ≠ “远程 Function Calling”

把 A2A 简化成“远程函数调用”会丢掉几个关键语义：

- Remote Agent 可能无法立即完成；
- 任务可能持续很久；
- 对端可能需要额外输入；
- 对端可能要求认证；
- 任务可能取消、拒绝或失败；
- 结果可能是多个 artifact；
- 状态可能通过 stream / async mechanism 持续更新。

因此 A2A 的中心不是：

```text
request → response
```

而更接近：

```text
request
  ↓
message or task
  ↓
stateful lifecycle
  ↓
updates / artifacts / further input
  ↓
terminal or interrupted state
```

---

#### 6.7.10 A2A 的最小交互闭环

一个最小 A2A interaction 可以抽象为：

```text
1. Discover
2. Inspect Capability Contract
3. Authenticate / Authorize
4. Select Compatible Interface
5. Send Message
6. Receive Message or Task
7. If Task:
      observe state
      receive updates
      provide more input if needed
8. Receive Artifact / final result
9. Verify outcome
10. Update local state
```

更完整一点：

```text
Discover
   ↓
Resolve Capability
   ↓
Trust / Policy Check
   ↓
Authenticate / Authorize
   ↓
Protocol / Interface Negotiation
   ↓
Message Submission
   ↓
Task Creation / Immediate Message
   ↓
Task Tracking
   ↓
Artifact / Result
   ↓
Verification
   ↓
Commit downstream action
```

注意最后两个步骤通常属于调用方 Harness，而不是协议自动替你完成的事情。

---

#### 6.7.11 A2A 的核心对象

长期最值得掌握的对象不是某个 SDK 方法名，而是这些语义对象：

```text
Agent Card
Agent Skill
Agent Interface
Security Scheme
Message
Part
Task
Task Status / State
Artifact
Context
Extension
```

它们大致对应：

```text
Who are you?              → Agent Card
What can you do?           → Skills / Capabilities
How can I reach you?       → Agent Interface
How do I authenticate?     → Security Scheme
What am I telling you?     → Message
What content is carried?   → Part
What work are you doing?   → Task
Where is the work now?     → Task State
What did you produce?      → Artifact
Which interactions belong together? → Context
What optional semantics exist?       → Extension
```

---

#### 6.7.12 Remote Agent 为什么可以是 opaque 的

A2A 的一个关键设计思想是：

> **互操作不要求共享内部实现。**

Remote Agent 不需要暴露：

- chain-of-thought；
- hidden state；
- internal memory；
- planner internals；
- private prompt；
- internal tool inventory；
- framework-specific graph；
- model weights。

调用方真正需要的是：

```text
能力契约
交互接口
任务状态
必要消息
正式产物
安全与认证要求
```

这也是为什么 A2A 更适合跨团队、跨组织、跨 vendor 的 agentic systems。

---

#### 6.7.13 Opaque ≠ Unobservable

“不暴露内部思维”不代表“什么都看不到”。

一个生产级 remote-agent boundary 仍需要足够的外部可观测性：

```text
request / task ID
current state
status timestamp
artifacts
errors
latency
retry history
provenance
trace correlation
policy decision
```

因此要区分：

```text
Private Internal Reasoning
          ≠
Operationally Necessary Observability
```

> **不要为了 observability 要求暴露 chain-of-thought；应该观测协议事件、状态转换、输入输出、side effect 和验证结果。**

---

#### 6.7.14 Agent Card：远程 Agent 的公开能力契约

**Agent Card** 可以理解为 remote agent 的机器可读“业务卡片 / 能力卡片”。

它用于描述：

- Agent identity；
- description / provider；
- 可连接的 interface；
- protocol version / binding；
- capabilities；
- security requirements；
- skills；
- input / output modes；
- extension support。

调用方因此能够在真正发送任务前先回答：

```text
它是谁？
它大概能做什么？
我该连哪个 endpoint？
我支持它的 protocol binding 吗？
需要什么认证？
它接受什么输入？
它可能返回什么输出？
```

---

#### 6.7.15 Agent Card ≠ Agent 本体

Agent Card 是 description，不是 Agent 本身。

因此：

```text
Agent Card says capability X
        ≠
Agent can always successfully perform X
```

也不代表：

```text
endpoint reachable
credentials valid
current capacity sufficient
skill currently enabled
backend dependency healthy
policy will authorize this caller
```

所以 Agent Card 更接近**可发现契约**，不是实时运行状态的完整镜像。

---

#### 6.7.16 Agent Card ≠ Trust Certificate

这是非常重要的安全边界。

一个 Agent Card 可以声明：

```text
name = "Finance Agent"
skill = "execute_payment"
```

这并不能自动证明：

```text
它确实属于可信组织
它有权执行付款
返回结果可信
当前 card 未被篡改
调用它符合本地 policy
```

即使 Card 支持签名，也只是帮助验证某些 authenticity / integrity 属性，不能自动完成：

- business trust；
- authorization；
- suitability；
- output correctness；
- safety approval。

因此：

> **Discovery Metadata ≠ Trust Decision**

---

#### 6.7.17 Discovery 到底发现什么

A2A Discovery 的目标不是“发现所有 Agent”。

更准确地说，它是在当前环境中找到：

> **可能与当前任务交互的 remote-agent contract。**

可抽象为：

```text
Agent Universe
   ↓
Known Domains / Registry / Configuration
   ↓
Discover Agent Cards
   ↓
Permission / Tenant Filter
   ↓
Compatibility Filter
   ↓
Trust / Risk Filter
   ↓
Task Relevance Filter
   ↓
Candidate Remote Agents
```

这与前面 Capability Discovery 的思想是一致的：

> **系统拥有很多可连接 Agent，不等于当前模型应该看到所有 Agent。**

---

#### 6.7.18 常见 Agent Discovery 路径

当前 A2A 体系中常见的 discovery 方式包括：

```text
1. well-known URI
2. curated registry / catalog
3. direct configuration
```

它们分别适合：

```text
public / domain-owned agent
enterprise capability catalog
known private integration
```

这里要注意：

> **A2A 标准化 Agent Card，本身并不意味着所有 registry 的查询 API 都被统一标准化。**

因此 Discovery Plane 往往仍然是企业治理的重要扩展点。

---

#### 6.7.19 Discovery ≠ Selection

发现一个 Agent，只说明：

```text
它进入了 candidate set
```

并不等于：

```text
应该选择它执行当前任务
```

所以应该沿用第 5 章 Capability Discovery 的分层思想：

```text
Discovered
   ↓
Compatible
   ↓
Authorized
   ↓
Trusted
   ↓
Relevant
   ↓
Suitable
   ↓
Selected
```

稳定表达是：

> **Discovered ≠ Trusted ≠ Authorized ≠ Reachable ≠ Compatible ≠ Suitable ≠ Selected**

---

#### 6.7.20 Agent Skill：能力描述，不是执行保证

Agent Card 中的 **Skill** 用于说明 remote agent 可以处理什么类型的任务。

一个 skill 通常需要让调用方理解：

- skill identity；
- name / description；
- input modes；
- output modes；
- examples / tags；
- capability scope。

它主要服务于：

```text
Discovery
Routing
Request Construction
Compatibility Check
```

但仍应坚持：

```text
Skill advertised
   ≠
Skill currently available
   ≠
Skill authorized for caller
   ≠
Skill succeeds on this case
```

这和 Tool schema 的边界非常类似：**schema 描述接口，不证明结果。**

---
