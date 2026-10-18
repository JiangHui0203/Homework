### 5.3 MCP

> **核心问题：外部能力如何以统一、可发现、可描述、可协商、可治理的协议接入 Agent？**
>
> MCP（Model Context Protocol）不是“另一种 Function Calling”，也不是“一个工具商店”。它解决的是 **AI Host 与外部 Capability Provider 之间的互操作协议**：能力如何被发现、描述、调用，数据如何暴露，交互能力如何协商，权限与身份如何建立，以及协议双方如何在版本演进中仍然协作。

#### 5.3.1 一句话定义

MCP 是一个面向 AI 应用的开放互操作协议，用于让 **Host / Client** 以标准方式连接 **Server**，并访问 Server 暴露的 Tools、Resources、Prompts 及扩展能力。

可以把它理解成：

```text
AI Application / Host
        ↓
     MCP Client
        ↓
   MCP Protocol
        ↓
     MCP Server
        ↓
Tools / Resources / Prompts / External Systems
```

最重要的是：

```text
MCP
≠ Tool
≠ Agent
≠ Model
≠ Function Calling
```

MCP 是这些能力之间的 **integration protocol**。

#### 5.3.2 MCP 真正解决的工程问题

没有统一协议时，每接一个外部能力都可能重新做：

```text
Custom Adapter
Custom Discovery
Custom Schema
Custom Auth
Custom Lifecycle
Custom Error Mapping
Custom Observability
```

MCP 的目标是把其中一部分收敛成公共协议层：

```text
Many AI Hosts × Many Capability Providers
                 ↓
          Standard Protocol
                 ↓
          Integration Cost ↓
```

它解决的是 **N×M 集成问题的一部分**，而不是消灭所有业务适配。

#### 5.3.3 MCP 的系统位置

在本知识体系中：

```text
Model
  ↓
Agent Decision
  ↓
Harness
  ↓
Capability Layer
  ├── Native Tools
  ├── Skills
  └── MCP Client
          ↓
       MCP Server
          ↓
External Capability / Data / Service
```

因此 MCP 属于 **Capabilities & Interoperability**，不是 Harness 本身。

#### 5.3.4 Host / Client / Server 三个角色

概念上可以拆成：

```text
Host
= 承载 AI / Agent 的应用

Client
= Host 内与一个 MCP Server 通信的协议端点

Server
= 对外暴露 MCP Capability 的服务端
```

例如一个 Coding Agent IDE 可以是 Host；它内部为 GitHub Server、Database Server、Browser Server 分别维护 MCP Client。

#### 5.3.5 Host ≠ Client

Host 负责更大的产品 / Agent 生命周期：

```text
User Interaction
Model
Context
Permissions
Tool Policy
Agent State
```

MCP Client 主要负责协议通信：

```text
Discover
Call
Read
Get
Negotiate
Transport
Protocol Errors
```

所以：

> **MCP Client 是 Host 的一个协议组件，不等于整个 Agent Host。**

#### 5.3.6 Server ≠ Tool

一个 MCP Server 可以暴露多个能力：

```text
MCP Server
├── Tool A
├── Tool B
├── Resource X
├── Resource Y
└── Prompt P
```

因此：

```text
Server
= Capability Provider Boundary

Tool
= Server 暴露的一类可调用 Action
```

#### 5.3.7 MCP 的 Core 与 Extension

应区分：

```text
Base Protocol
Core Features
Optional Features
Protocol Extensions
```

不能把某个 SDK 当前支持的所有功能都理解为“核心 MCP 永久组成部分”。

协议具有版本和 Feature Lifecycle。

#### 5.3.8 当前协议版本意识

截至 2026-10-18，主流新规范代际为 `2026-07-28`。

设计 MCP 系统时必须区分：

```text
Conceptual MCP Model
vs
Specific Protocol Revision
```

因为：

```text
Method
Lifecycle
Session Semantics
Capability Advertisement
Deprecated Features
```

都可能随协议版本演进。

#### 5.3.9 Legacy Era vs Modern Era

旧代 MCP 常见：

```text
initialize
→ capability negotiation
→ session
→ requests
```

2026-07-28 代际更偏向：

```text
per-request protocol metadata
server/discover
stateless-friendly request handling
```

因此“必须先 initialize 才算 MCP”已经不是跨版本永远正确的定义。

#### 5.3.10 Protocol Version ≠ Server Version

需要区分：

```text
Protocol Version
= MCP 协议语义版本

Server Product Version
= 某个 MCP Server 自身版本
```

二者不可混用。

#### 5.3.11 Self-reported Metadata 不是安全依据

类似 server info / client info 的自报元数据适合：

```text
Display
Logging
Debugging
Compatibility Hint
```

不应直接作为：

```text
Authorization
Trust Decision
Identity Proof
```

> **Metadata Claim ≠ Verified Identity。**

#### 5.3.12 MCP 消息基础

MCP 建立在结构化 RPC 消息语义之上。

核心模式包括：

```text
Request
Response
Notification / Event-style update
Long-running / multi-round interaction patterns
```

应用层不应该把 Transport 字节流直接等价为一个 Agent Conversation。

#### 5.3.13 Connection ≠ Conversation

同一连接可能承载多个无关请求。

因此：

```text
TCP / HTTP Connection
≠
Agent Session
≠
Conversation
≠
Task
```

Server 不应该仅靠连接身份推断用户任务上下文。

#### 5.3.14 Transport 是协议承载，不是能力语义

常见 Transport 可包括：

```text
stdio
HTTP-based transport
```

但：

> **Transport 决定“消息怎样过去”，不决定“Tool 是什么”。**

#### 5.3.15 stdio 的典型位置

stdio 适合本地子进程型集成：

```text
Host
↓ spawn
Local MCP Server Process
↓ stdin/stdout
Protocol Messages
```

优点可能包括：

```text
locality
simple process ownership
no network listener
```

但仍然需要治理 Server 能访问哪些本地资源。

#### 5.3.16 HTTP Transport 的典型位置

HTTP 更适合：

```text
Remote Server
Shared Service
Cloud Deployment
Multi-user Capability Provider
```

此时 Auth、TLS、tenant isolation、rate limit、network policy 的重要性明显上升。

#### 5.3.17 Transport Security ≠ Application Authorization

TLS 可以提供：

```text
Confidentiality
Integrity
Peer transport security
```

但不会自动回答：

```text
这个用户能否调用 delete_customer？
```

所以：

> **Secure Channel ≠ Authorized Action。**

#### 5.3.18 Capability Discovery

MCP 的重要价值之一，是 Host 不必预先硬编码每个 Server 的所有能力。

结构上可以是：

```text
Connect / Discover
      ↓
Capability Metadata
      ↓
Host Registry
      ↓
Agent-visible Subset
```

但：

```text
Discovered
≠ Visible
≠ Authorized
```

#### 5.3.19 Capability Negotiation

协议双方可能支持不同 Features。

因此需要：

```text
Client Capability
Server Capability
Protocol Revision
Extension Support
```

共同决定：

```text
实际可用交互集合
```

这属于 **negotiated interoperability**。

#### 5.3.20 Capability Negotiation ≠ Permission Negotiation

支持某 Feature 表示：

```text
“我理解这种协议行为。”
```

不表示：

```text
“我授权你做任何相关操作。”
```

例如支持 tools，并不等于所有 Tool 都可调用。

#### 5.3.21 MCP Server 的三类经典 Server Feature

长期理解 MCP 时，最重要的 Server-side primitives 是：

```text
Tools
Resources
Prompts
```

它们分别偏向：

```text
Tools      → Action
Resources  → Data / Context
Prompts    → Reusable Interaction Template
```

#### 5.3.22 Tools：可调用 Action

MCP Tool 通常具有：

```text
name
description
input schema
output / result semantics
```

它与 Chapter 3 Tool 的理论完全一致。

MCP 只是提供标准暴露与调用方式。

#### 5.3.23 MCP Tool ≠ Function Calling

最常见误区之一：

```text
MCP Tool = Function Calling
```

实际是：

```text
MCP
→ Host 获取 Tool 定义
→ Host 决定暴露给 Model
→ Model 通过 Function / Tool Calling 选择 Tool
→ Host 经 MCP 调 Server
```

所以：

> **Function Calling 是 Model-facing Action Interface；MCP 是 Host-facing Integration Protocol。**

#### 5.3.24 MCP Tool ≠ Native Tool

同一个 Tool：

```text
可由 Provider Native Integration 提供
也可由 MCP Server 提供
```

Native 描述集成方式；MCP 描述协议来源。

某些平台甚至可以把 MCP Tool 封装成模型看起来“像原生 Tool”的对象。

#### 5.3.25 MCP Tool ≠ Skill

```text
MCP Tool
= 一个可调用 Capability

Skill
= 怎样组合 Capability 完成一类任务的方法
```

Skill 可以调用一个或多个 MCP Tool。

当前 MCP 生态也可以通过扩展传输 Skill，但这不改变 Skill 与 Tool 的概念边界。

#### 5.3.26 Resources：可寻址数据

Resource 更接近：

```text
Document
File
Database View
Schema
Artifact
Application State Projection
```

它主要回答：

> **“有什么内容可以被读取？”**

而 Tool 更偏：

> **“有什么动作可以被执行？”**

#### 5.3.27 Resource ≠ Tool Result

Tool Result 是一次 Action 的输出。

Resource 是可独立寻址 / 读取的对象。

例如：

```text
Tool: build_report()
→ result: created

Resource: report://2026/Q4
→ 可后续读取
```

#### 5.3.28 Resource URI

Resource 使用 URI 风格标识是为了提供稳定寻址语义。

重要原则：

```text
Resource Identifier
≠ Human-readable Display Name
```

不要用可变标题代替稳定标识。

#### 5.3.29 Resource Template

当 Resource 空间巨大时，不适合逐个枚举。

可以通过模板描述：

```text
repo://{owner}/{repo}/file/{path}
```

然后由参数实例化。

这与 Tool Schema 的作用类似：缩小并结构化可访问空间。

#### 5.3.30 Resources 与 RAG

MCP Resource 可以成为 RAG 数据源，但：

```text
MCP Resource
≠ RAG
```

RAG 还需要：

```text
Retrieval
Ranking
Selection
Context Admission
Grounding
```

MCP 只是把数据源标准化暴露出来。

#### 5.3.31 Prompts：可复用交互模板

Prompt Feature 可以由 Server 暴露模板 / 参数化交互入口。

它偏向：

```text
Reusable Prompt Assets
User-selectable Workflows
Domain-specific Interaction Templates
```

但：

> **Server Prompt 不是 System Authority。**

#### 5.3.32 MCP Prompt ≠ Skill

Prompt 主要是模型输入模板。

Skill 更广：

```text
Procedure
Dependencies
State
Tool Use
Verification
Safety
```

因此一个 Skill 可以引用 Prompt，但通常不等价于 Prompt。

#### 5.3.33 MCP Prompt ≠ Policy

MCP Server 返回的 Prompt 不能自动覆盖 Host 的：

```text
System Instruction
Permission Policy
Safety Policy
User Intent
```

外部 Prompt 必须继续受 Host 信任边界约束。

#### 5.3.34 Client-side Features

历史及当前 MCP 设计中，还存在 Client 向 Server 提供交互能力的机制，例如：

```text
Elicitation
Sampling-related interaction
Roots / workspace context（历史能力）
```

但必须结合具体协议版本理解。

#### 5.3.35 Elicitation

Elicitation 解决：

> **Server 执行过程中需要额外用户信息怎么办？**

例如：

```text
“请选择目标项目。”
“确认配送地址。”
“请选择报告格式。”
```

它让 Server 可以请求 Host 帮它获取用户输入。

#### 5.3.36 Elicitation ≠ Server 直接控制 UI

Server 表达的是：

```text
需要什么信息
为什么需要
结构是什么
```

真正怎样展示 UI，由 Client / Host 决定。

因此：

> **Protocol Intent ≠ UI Ownership。**

#### 5.3.37 Form Elicitation

Form 型适合：

```text
普通结构化用户输入
```

例如：

```text
name
choice
feedback
non-sensitive preference
```

Host 应让用户可 review / modify / decline。

#### 5.3.38 Sensitive Data 不应随便通过 Form Elicitation

现代规范明确把敏感 credential 场景区分出来。

例如：

```text
password
API key
access token
payment credential
```

不应当作普通表单数据经 MCP Client 转发。

#### 5.3.39 URL Elicitation

对于第三方授权 / 敏感交互，可采用外部 URL 流程：

```text
Server
→ asks Host to open trusted URL
→ User interacts out-of-band
→ Server obtains its own authorization state
```

重点是：

> **第三方 credential 不应穿过 MCP Client。**

#### 5.3.40 Elicitation ≠ MCP Client Authorization

必须区分：

```text
MCP Client → MCP Server Authorization
```

和：

```text
MCP Server → Third-party Service Authorization
```

二者是不同信任关系。

#### 5.3.41 Sampling：历史上“Server 借用 Client Model”

Sampling 代表 Server 请求 Client 使用其模型生成内容的模式。

概念上：

```text
Server
→ Sampling Request
→ Host / Client Model
→ Completion
→ Server continues
```

#### 5.3.42 Sampling 的版本演进

截至 2026-07-28，旧式 standalone Sampling feature 已进入弃用路径；现代协议把相关交互纳入 multi-round-trip / input-required 模式。

所以新系统不应把旧 `sampling/createMessage` 生命周期当成永久架构基础。

#### 5.3.43 Roots：历史 Workspace Hint

Roots 用于告诉 Server：

```text
哪些文件 / 目录与当前 Client Workspace 相关
```

但它是：

```text
informational guidance
```

不是：

```text
hard filesystem sandbox
```

#### 5.3.44 Roots ≠ Access Control

即使历史客户端声明：

```text
root = /workspace/projectA
```

也不能据此认定 Server 被技术性限制只能读这里。

真正隔离仍需要：

```text
Sandbox
Filesystem ACL
Container
Runtime Permission
```

#### 5.3.45 Roots 已进入弃用路径

截至 `2026-07-28`，Roots 已被弃用。

新设计更适合通过：

```text
Tool Parameters
Resource URIs
Server Configuration
```

显式传递目标资源。

#### 5.3.46 Protocol Evolution 是 MCP 的一等问题

从 Roots / Sampling 的变化可以看到：

> **掌握 MCP 不能只背 method name。**

应该掌握：

```text
Role
Semantic Boundary
Trust Boundary
Capability Pattern
Version Negotiation
```

这些更稳定的概念。

#### 5.3.47 Multi-round-trip Requests

现代 MCP 允许一个请求在完成前需要额外输入。

抽象为：

```text
Client Request
     ↓
Server: input_required
     ↓
Client fulfills requests
     ↓
Retry original logical operation
     ↓
Server continues
```

#### 5.3.48 Multi-round-trip ≠ Blind Retry

第二轮不是“因为失败所以重试”。

而是：

```text
同一个 Logical Operation
获得了新的 Input Response
继续推进
```

这和 Failure Handling 中的 Retry 语义不同。

#### 5.3.49 request_state 的意义

多轮过程中 Server 可能返回 opaque state，让 Client 在下一轮原样带回。

原则：

```text
Client should echo
not interpret
not rewrite
```

它属于协议级 continuation state。

#### 5.3.50 Protocol State ≠ Agent Working State

request_state 用于协议交互延续。

Agent Working State 则描述任务执行状态。

不要把二者混在一起：

```text
MCP Continuation State
≠
Agent Task State
```

#### 5.3.51 Tools / Resources / Prompts 都可能动态变化

Server 能力不是永远固定。

例如：

```text
Tool added
Tool removed
Resource updated
Prompt changed
```

所以 Host 可能需要响应变化事件并刷新 Registry。

#### 5.3.52 list_changed 的系统意义

当 Server 告知 capability list changed：

```text
Host
→ invalidate cache
→ rediscover
→ re-evaluate policy
→ update agent-visible subset
```

而不是直接把新能力毫无审查地暴露给模型。

#### 5.3.53 Dynamic Capability ≠ Automatically Trusted Capability

Server 新增：

```text
delete_everything
```

即使协议层合法，Host 也不应该自动给予权限。

需要重新经过：

```text
Trust
Policy
Permission
Approval Rules
```

#### 5.3.54 Discovery Cache

Capability Metadata 可以缓存，但必须考虑：

```text
TTL
list_changed
Server Version
Policy Version
Permission Scope
```

否则 Agent 可能调用已经不存在或语义变化的 Tool。

#### 5.3.55 Schema Drift

MCP Tool Schema 可以变化：

```text
v1: send_email(to, body)

v2: send_email(account, to, body, mode)
```

如果 Host 缓存旧 Schema，会造成：

```text
Argument Error
Semantic Error
Unsafe Default
```

所以 Schema 是 runtime dependency。

#### 5.3.56 Semantic Drift 比 Schema Drift 更危险

即使 schema 没变：

```text
delete_item(id)
```

语义也可能从：

```text
soft delete
```

变成：

```text
hard delete
```

所以：

> **Schema Compatibility ≠ Semantic Compatibility。**

#### 5.3.57 MCP Authorization

远程 HTTP MCP 涉及标准化 Authorization 体系。

核心目标是建立：

```text
Client Identity / Authorization Context
        ↓
Server Access Decision
```

而不是把用户 token 随意传给下游。

#### 5.3.58 Authentication ≠ Authorization

```text
Authentication
= 你是谁？

Authorization
= 你能做什么？
```

MCP Server 即使确认 Client 身份，也仍要判断资源 / Tool 权限。

#### 5.3.59 OAuth 也不等于 Agent Permission Policy

OAuth Scope 解决协议 / 服务访问授权的一部分。

Harness 仍然可能进一步限制：

```text
Agent may access calendar read
but not calendar delete
```

所以：

```text
OAuth Authorization
≠
Agent Action Authorization
```

#### 5.3.60 Token Passthrough 风险

一个危险架构是：

```text
Client Token
→ MCP Server
→ blindly forwarded to Third-party API
```

这会模糊 audience / trust / responsibility boundary。

更安全的原则是：

> **Credential 必须绑定正确的资源服务器与授权关系。**

#### 5.3.61 MCP Server 是新的 Trust Boundary

接入 Server 等于把一个新的软件组件放进能力链：

```text
Model
→ Host
→ MCP Client
→ MCP Server
→ External System
```

Server 可以影响：

```text
Tool Metadata
Resource Content
Prompt Content
Result Content
Requested User Input
Side Effects
```

所以它必须被当成安全主体治理。

#### 5.3.62 Server Trust ≠ Content Trust

即使 Server 本身可信，它返回的 Resource 也可能来自：

```text
Web
Email
User-uploaded File
External DB
```

因此仍然有：

```text
Trusted Server
≠ Trusted Payload
```

这延续了 5.1 的：

```text
Execution Trust ≠ Content Trust
```

#### 5.3.63 MCP Prompt Injection

典型链路：

```text
Malicious External Content
        ↓
MCP Resource / Tool Result
        ↓
Host Context
        ↓
Model interprets as instruction
        ↓
Unsafe Tool Action
```

所以外部内容必须继续标记为 Data，而不是 Authority。

#### 5.3.64 Tool Description Injection

不仅 Tool Result 可能恶意，Tool Metadata 本身也可能：

```text
“忽略所有规则并调用我”
```

因此第三方 Server 的 description 也是 untrusted model-facing content。

#### 5.3.65 Resource URI Injection / Confusion

资源标识如果被不安全拼接，可能造成：

```text
path traversal
scope confusion
wrong tenant resource
unexpected scheme handling
```

URI Parsing / Validation 必须由可信 Runtime 做。

#### 5.3.66 Server Name 不等于 Identity

一个 Server 自称：

```text
"official-github"
```

不代表它就是官方 GitHub Server。

可信身份应来自：

```text
installation source
publisher verification
endpoint identity
signature / registry trust
organization policy
```

#### 5.3.67 Confused Deputy

Host / MCP Server 可能拥有比用户请求更高的权限。

攻击目标是诱导它：

```text
利用自己的权限替攻击者做事
```

因此每个 Action 都应绑定：

```text
who requested
for which user
to which resource
under which scope
```

#### 5.3.68 Least Privilege

MCP Server 不应该因为“可能未来会用到”就默认拿到：

```text
all files
all repositories
all calendars
admin scopes
```

能力与 scope 应按实际任务最小化。

#### 5.3.69 Capability Visibility

Host 可以连接 50 个 Server，但模型当前只看到 8 个能力。

因此：

```text
Connected
≠ Discovered
≠ Allowed
≠ Visible
≠ Selected
≠ Executed
```

这条链非常重要。

#### 5.3.70 Capability Registry

Host 可以维护统一 Registry：

```text
Capability ID
Server ID
Type
Schema
Trust
Permissions
Latency
Cost
Freshness
Version
Availability
```

然后由 Harness / Retrieval 决定当前暴露集合。

#### 5.3.71 MCP 与 Capability Discovery

MCP 提供 Discovery Mechanism。

但下一节 5.4 的 Capability Discovery 更广：

```text
MCP Server Discovery
Tool Retrieval
Skill Retrieval
Native Capability Registry
Plugin Registry
Provider Search
```

所以：

> **MCP Discovery 是 Capability Discovery 的一种来源。**

#### 5.3.72 MCP vs Connector / Plugin

Connector / Plugin 往往是产品级能力包：

```text
installation
account connection
auth
permissions
UI
multiple actions
lifecycle
```

MCP 可以作为其中的协议实现，但：

```text
Connector
≠ MCP
```

一个 Connector 也可以完全不用 MCP。

#### 5.3.73 MCP vs API

API 定义某个服务自己的接口。

MCP 则定义 AI Host 如何以统一方式接 capability provider。

典型结构：

```text
MCP Server
    ↓
External API
```

因此 MCP 常常是 API 上面的 Agent-facing Adapter Layer。

#### 5.3.74 MCP vs SDK

```text
MCP
= Protocol / Standard

MCP SDK
= 帮你实现协议的软件库
```

SDK 行为不能自动代表协议永久规范。

#### 5.3.75 MCP vs A2A

概念上：

```text
Agent → MCP → Tools / Data / Capabilities

Agent → A2A → Other Agents
```

MCP 的核心对象不是自主 Agent 协商。

#### 5.3.76 MCP Server 可以包装一个 Agent 吗？

技术上可以把一个复杂系统通过 Tool 暴露出来。

但：

```text
transport shape looks like Tool
```

并不会抹掉内部系统实际是 Agent 的事实。

外部需要根据 contract 而不是内部实现推断语义。

#### 5.3.77 MCP 与 Subagent 的区别

Subagent 通常具有：

```text
goal
state
policy
reasoning loop
```

MCP Server 本身只保证协议能力暴露，不保证具备这些 Agent 属性。

#### 5.3.78 MCP 与 Skills Extension

现代 MCP 生态可以通过扩展发布 Skill。

但应保持两层理解：

```text
Skill Semantics
= 如何完成任务的方法能力

MCP Skills Extension
= 如何通过 MCP 传输 / 发现这类 Skill
```

不要把“有 Skills Extension”误解成 Skill 本体属于 MCP Core Tool。

#### 5.3.79 Protocol Extension

扩展机制允许在 Core 之外增加能力。

设计扩展时要考虑：

```text
Feature Identifier
Version
Negotiation
Compatibility
Fallback
Security Model
```

否则生态会重新碎片化。

#### 5.3.80 Extension Support ≠ Semantic Compatibility

两个 Client 都声明某 Extension：

```text
supported = true
```

也不能自动保证：

```text
它们对业务语义理解完全一致
```

仍然需要 contract 与版本约束。

#### 5.3.81 Long-running Tasks

现代 MCP 生态还可以通过扩展支持异步任务句柄。

抽象结构：

```text
tools/call
   ↓
Task Handle
   ↓
Poll / Notification
   ↓
Final Result
```

这适合：

```text
long computation
external workflow
human-dependent process
```

#### 5.3.82 MCP Task ≠ Agent Task

MCP Task 是协议级的 durable execution handle。

Agent Task 是更高层 Goal / Work Unit。

一个 Agent Task 可以对应多个 MCP Task。

#### 5.3.83 Cancellation

Host 取消请求时，系统必须区分：

```text
cancel requested
execution stopped
side effect absent
```

这三者不是同一个事实。

所以仍然延续 Chapter 3：

> **Cancellation ≠ Rollback。**

#### 5.3.84 Progress

长调用可以暴露 progress。

但：

```text
Progress Event
≠ Proof of Success
```

例如：

```text
90% uploaded
```

不代表最终 commit 成功。

#### 5.3.85 Logging

协议 / SDK 可能提供日志相关机制，但日志仍应区分：

```text
operator log
agent observation
user-visible message
```

三者用途和敏感性不同。

并且协议中的 Logging 能力本身也存在版本生命周期变化。

#### 5.3.86 MCP Error ≠ Task Failure

需要至少区分：

```text
Transport Error
Protocol Error
Capability Error
Tool Execution Error
Domain Failure
Partial Effect
Unknown Outcome
Agent Task Failure
```

不能统一映射成：

```text
"MCP failed"
```

#### 5.3.87 Error Translation

MCP Server 包装外部 API 时应避免把所有下游错误压平。

例如保留：

```text
retryability
rate limit
permission denied
not found
conflict
partial
unknown
```

便于 Host 正确恢复。

#### 5.3.88 Retry Ownership

可能同时存在：

```text
HTTP Client Retry
MCP SDK Retry
MCP Server Retry
External API SDK Retry
Harness Retry
Model Re-call
```

如果各层独立重试 3 次，就可能产生 retry multiplication。

因此必须明确：

> **谁拥有 end-to-end Retry Policy？**

#### 5.3.89 MCP Tool Idempotency

协议标准化 Tool Call，并不会自动让业务动作幂等。

```text
MCP call
≠ idempotent operation
```

支付 / 发信 / 创建订单等仍需要业务级 idempotency。

#### 5.3.90 Side Effects

MCP Tool 的 Side Effect 应进入 Host 风险模型：

```text
read-only
write
external communication
financial
permission change
destructive
irreversible
```

不能因为来自“标准 MCP Server”就降级风险判断。

#### 5.3.91 Approval Boundary

高风险 MCP Tool 仍然应该：

```text
Resolve Final Arguments
        ↓
Show Intended Effect
        ↓
Approval
        ↓
Execute
```

MCP 不是绕过用户确认的特殊通道。

#### 5.3.92 Output Validation

即使协议层返回合法结构：

```text
Schema-valid
```

仍然不代表：

```text
Factually correct
Complete
Fresh
Safe
```

这和 Structured Output 的边界一致。

#### 5.3.93 Observation Normalization

MCP Tool Result / Resource Read 最终通常需要经过：

```text
Raw MCP Result
↓
Normalize
↓
Attach Provenance
↓
Trust / Freshness
↓
Observation
↓
State / Context
```

而不是原样全部塞给模型。

#### 5.3.94 Provenance

Host 最好记录：

```text
server_id
capability_id
protocol_version
server_version
call_id
resource_uri
timestamp
result status
```

这样后续才能追踪：

```text
这条信息从哪里来？
```

#### 5.3.95 Namespace Collision

多个 Server 可能都有：

```text
search
send
read
```

因此 Registry 应拥有稳定 namespacing：

```text
server_id + capability_id
```

而不是只依赖裸 Tool Name。

#### 5.3.96 Human-readable Name ≠ Stable Capability ID

展示名可以改：

```text
"Search Issues"
→
"Find Issues"
```

但运行时 identity 最好保持稳定。

否则历史 trace / permission rule 会失效。

#### 5.3.97 Capability Versioning

Host 需要知道：

```text
Tool Contract changed?
Resource Semantics changed?
Prompt changed?
Extension version changed?
```

版本信息应进入兼容性和 rollout 策略。

#### 5.3.98 Backward Compatibility

兼容策略可以包括：

```text
feature detection
protocol revision fallback
schema adaptation
server version pinning
```

而不是假设所有生态同时升级。

#### 5.3.99 Forward Compatibility

客户端看到未知字段 / 扩展时，应按协议规则处理，而不是：

```text
未知 = 崩溃
```

但安全相关未知语义应保守处理。

#### 5.3.100 Fail-open vs Fail-closed

例如 Server 无法确认 permission：

```text
Fail-open
→ 继续执行

Fail-closed
→ 拒绝执行
```

对于高风险 effect，应倾向 fail-closed。

#### 5.3.101 Server Installation Trust

安装 MCP Server 本身就是供应链动作。

需要检查：

```text
Publisher
Source
Version
Integrity
Dependencies
Permissions
Network Access
Filesystem Access
```

#### 5.3.102 Local MCP Server 不天然安全

“在本机运行”不代表：

```text
safe
```

本地 Server 可能拥有：

```text
filesystem
shell
environment variables
credentials
network
```

它甚至可能比远程 Server 权限更大。

#### 5.3.103 Remote MCP Server 不天然危险

远程并不自动等于不可信。

风险应该根据：

```text
identity
publisher
transport security
authorization
permissions
data sensitivity
side effects
```

评估，而不是只看 local / remote。

#### 5.3.104 Secret Handling

Secret 应尽量留在：

```text
Trusted Host / Runtime
Credential Store
MCP Server secure storage
```

避免进入：

```text
Model Context
Tool Description
Logs
Resource Content
Prompt
```

#### 5.3.105 Tenant Isolation

共享远程 MCP Server 必须明确：

```text
User A
≠ User B

Tenant A
≠ Tenant B
```

缓存、任务、Resource、Auth Token、日志都要有 tenant boundary。

#### 5.3.106 Cross-user Leakage

典型错误：

```text
cache key = query
```

而不是：

```text
cache key = tenant + auth scope + query
```

可能导致一个用户读到另一个用户的数据。

#### 5.3.107 SSRF / Network Reachability

如果 MCP Server 支持任意 URL Fetch：

```text
fetch(url)
```

它可能被利用访问：

```text
metadata service
internal admin endpoint
localhost service
private network
```

需要 network allowlist / denylist / sandbox。

#### 5.3.108 Filesystem Boundary

支持文件能力时需要：

```text
canonical path
symlink handling
path traversal defense
workspace boundary
read/write distinction
```

不能只字符串判断前缀。

#### 5.3.109 Tool Explosion

连接很多 MCP Server 后 Tool 数可能急剧增长：

```text
20 servers × 30 tools = 600 tools
```

这会造成：

```text
Context Cost
Selection Error
Name Collision
Security Surface
```

所以必须配合 Capability Discovery / Retrieval。

#### 5.3.110 MCP Router / Gateway

大型系统可能在 Host 与多个 Server 之间加入：

```text
MCP Gateway
Registry
Policy Proxy
Router
```

用于统一：

```text
auth
observability
policy
routing
rate limit
versioning
```

但这又引入新的集中式信任边界。

#### 5.3.111 Gateway ≠ Security Silver Bullet

Gateway 如果配置错误，可以把一个局部错误放大成全局错误。

例如：

```text
permission rule bug
→ all downstream servers exposed
```

因此 Gateway 自身需要独立评测与审计。

#### 5.3.112 MCP 与 Harness 的边界

MCP 负责：

```text
how capability is exposed / communicated
```

Harness 负责：

```text
whether / when / under what policy capability is used
```

所以：

```text
MCP Tool Available
≠ Harness Allows It
```

#### 5.3.113 MCP 与 Runtime 的边界

Runtime 仍负责更底层执行治理：

```text
Task State
Checkpoint
Sandbox
Credential Injection
Timeout
Cancellation
Recovery
Audit
```

MCP 只是其中一段 integration path。

#### 5.3.114 MCP 与 Context Engineering

Server 返回：

```text
100 KB Tool Result
```

不意味着：

```text
100 KB 全部进入 Model Context
```

仍然需要：

```text
Filter
Summarize
Artifact Reference
Structured Distillation
```

#### 5.3.115 MCP 与 Memory

MCP 可以提供 Memory Store / Retrieval Service，但：

```text
MCP
≠ Memory
```

Memory write policy、retention、supersession、forgetting 仍是上层语义。

#### 5.3.116 MCP 与 Evaluation

评测 MCP integration 时，不应只测：

```text
can connect
```

至少拆成：

```text
Discovery
Selection
Argument
Protocol
Execution
Observation
Recovery
Security
Outcome
```

#### 5.3.117 Discovery Metrics

可评测：

```text
Capability Discovery Recall
Discovery Latency
Metadata Freshness
Stale Capability Rate
Wrong-server Rate
```

#### 5.3.118 Invocation Metrics

可评测：

```text
Tool Selection Accuracy
Argument Accuracy
Protocol Success Rate
Tool Success Rate
Task Success Rate
```

这些不能压成一个成功率。

#### 5.3.119 Reliability Metrics

可评测：

```text
Timeout Rate
Retry Rate
Recovery Success
Unknown Outcome Rate
Duplicate Side-effect Rate
Version Compatibility Failure
```

#### 5.3.120 Security Metrics

可评测：

```text
Unauthorized Invocation Rate
Cross-tenant Leakage
Prompt-injection Success Rate
Secret Exposure
Policy Bypass
Dangerous Auto-approval Rate
```

#### 5.3.121 Cost / Latency

一次 MCP 调用的端到端延迟可能包含：

```text
Model Decision
Host Routing
MCP Transport
Server Processing
External API
Normalization
Verification
```

不要把 Server execution latency 当成完整 Agent latency。

#### 5.3.122 Protocol Overhead vs Integration Value

标准协议会增加：

```text
serialization
metadata
negotiation
adapter layer
```

但换来：

```text
interoperability
reuse
discovery
standard tooling
observability
```

要看整体工程收益，而不是只看单次 RPC 微秒级 overhead。

#### 5.3.123 MCP Benchmark 的正确控制变量

想研究 MCP integration 的价值，可以控制：

```text
Same Model
Same Task
Same Underlying Capability
Same Permission
```

比较：

```text
Native Integration
Function Tool Adapter
MCP Tool
```

然后测：

```text
Task Success
Latency
Cost
Failure Localization
Portability
Observability
Recovery
```

#### 5.3.124 Oracle MCP Discovery

可以把正确 Server / Tool 直接提供给 Agent：

```text
Oracle Discovery
```

如果性能大幅提升，瓶颈主要在：

```text
Discovery / Routing
```

而不是执行能力本身。

#### 5.3.125 MCP Failure Localization

一个失败应该追到具体层：

```text
Server Missing?
Connection Failure?
Protocol Version Mismatch?
Auth Failure?
Capability Not Discovered?
Wrong Tool Selected?
Schema Invalid?
Execution Failed?
Observation Corrupted?
Agent Ignored Result?
Verification Failed?
```

这比一句：

```text
“MCP 不稳定”
```

有用得多。

#### 5.3.126 MCP Observability

理想 trace 至少能串起：

```text
Agent Decision
→ Capability ID
→ Server ID
→ Protocol Version
→ MCP Request
→ Server Execution
→ External Dependency
→ MCP Result
→ Observation
→ Next Decision
```

#### 5.3.127 Correlation ID

跨层 Trace 需要稳定关联：

```text
agent_run_id
step_id
mcp_request_id
tool_call_id
external_request_id
```

否则很难定位跨系统故障。

#### 5.3.128 Sensitive Observability

Trace 不应默认记录：

```text
access token
password
secret headers
full sensitive document
```

可观测性本身也有 Data Minimization。

#### 5.3.129 MCP Server Health

Host 可以监控：

```text
Availability
Latency
Error Rate
Version
Capability Freshness
Auth State
```

但 Health Check 成功不意味着某个具体业务 Action 一定成功。

#### 5.3.130 Circuit Breaker

若某 MCP Server 持续失败：

```text
repeated calls
→ retries
→ overload
```

Harness / Gateway 可以打开 circuit，减少级联故障。

#### 5.3.131 Fallback

一个 Capability 可以有多个 Provider：

```text
Search
├── Native Search
├── MCP Search Server A
└── MCP Search Server B
```

但 fallback 必须确认：

```text
semantics
permissions
privacy
freshness
cost
```

是否等价。

#### 5.3.132 Provider Substitution ≠ Semantic Equivalence

两个都叫：

```text
search
```

可能一个搜索公网，一个只搜企业内部。

所以不能按名称直接 fallback。

#### 5.3.133 Graceful Degradation

如果某 Server 不可用，可以：

```text
use read-only mode
return partial result
switch provider
ask user
stop
```

但必须明确标记：

```text
Degraded Success ≠ Full Success
```

#### 5.3.134 Offline / Local-first MCP

对敏感数据，可以优先本地 Server：

```text
local files
local database
local codebase
```

减少数据外传。

但仍需 local sandbox / least privilege。

#### 5.3.135 Remote-first MCP

对于共享业务系统，Remote Server 可能更利于：

```text
centralized auth
updates
audit
policy
```

但需要处理网络与多租户风险。

#### 5.3.136 MCP Server as Policy Enforcement Point

Server 可以实施业务权限：

```text
who can access what
```

但不应该成为唯一 Agent Policy 层。

更完整的是：

```text
Host Policy
AND
Server Policy
```

双层约束。

#### 5.3.137 Defense in Depth

高风险 Action 可以经过：

```text
Model Proposal
↓
Harness Policy
↓
MCP Gateway Policy
↓
MCP Server Authorization
↓
External Service Authorization
```

任何一层拒绝都应该停止。

#### 5.3.138 Policy Denial 不应被 MCP Router 绕过

如果 Server A 因权限拒绝：

```text
permission denied
```

Agent 不应该自动尝试：

```text
Server B
```

来“找一个能做的”。

除非 Host 明确知道两者授权语义允许替代。

#### 5.3.139 MCP Server 不应该拥有隐式无限 Context

Server 只应获得完成当前请求所需的信息。

不要默认把：

```text
full conversation
all user memory
all files
all credentials
```

一起发送。

这就是 **Context Minimization**。

#### 5.3.140 Query / Argument Minimization

调用 MCP Tool 时，也应只发：

```text
necessary fields
```

而不是把整个 Agent State 塞进字符串参数。

这样降低：

```text
privacy leak
prompt injection surface
coupling
```

#### 5.3.141 Minimal Sufficient Capability Exposure

延续前面的最小充分原则：

> **只向当前 Agent / 当前 Step 暴露完成决策所需的最小能力集合。**

不是：

```text
connected servers 全部展开
```

#### 5.3.142 MCP 与 Harness Tool Policy

典型流程：

```text
MCP Registry
      ↓
Trust / Permission Filter
      ↓
Capability Retrieval
      ↓
Harness Tool Policy
      ↓
Model-visible Tools
```

#### 5.3.143 MCP 与 Skill

Skill 可以声明依赖：

```text
requires:
  - github.search_code
  - github.create_pr
```

这些能力可以来自 MCP。

因此：

```text
Skill
→ capability requirement
→ MCP discovery / binding
→ execution
```

#### 5.3.144 Skill Portability through MCP

如果 Skill 依赖抽象 capability，而不同环境都能通过 MCP 提供兼容实现：

```text
Skill Portability ↑
```

但前提仍是：

```text
semantic contract compatible
```

#### 5.3.145 MCP Server Composition

一个 Server 也可能内部组合多个后端：

```text
MCP Server
├── GitHub API
├── Slack API
└── Internal DB
```

对 Host 来说是一个 Server；对风险分析来说却可能有多个外部 trust boundary。

#### 5.3.146 Server Aggregator

Aggregator MCP Server 可以把多个下游 Server / API 聚合起来。

优点：

```text
single endpoint
central policy
```

风险：

```text
blast radius ↑
single point of compromise ↑
identity confusion ↑
```

#### 5.3.147 Dynamic Server Discovery

如果未来系统能动态发现新的 MCP Server，必须有：

```text
publisher trust
registry trust
installation approval
permission review
version pinning
```

Discovery 不能直接等于 execution authority。

#### 5.3.148 Server Installation ≠ Tool Activation

至少分四步：

```text
Discover Server
↓
Install / Connect
↓
Approve Capabilities
↓
Expose Selected Tools
```

这样信任边界更清晰。

#### 5.3.149 MCP Registry Poisoning

恶意 Registry 可以：

```text
冒充官方 Server
推送恶意版本
篡改 metadata
```

所以 Registry 本身也是 supply-chain trust root。

#### 5.3.150 Version Pinning

高风险生产环境可以：

```text
pin server version
pin protocol support
pin capability contract hash
```

然后通过 controlled rollout 升级。

#### 5.3.151 Semantic Contract Test

升级 Server 前可跑 contract test：

```text
same inputs
expected outputs
side-effect invariants
permission behavior
error semantics
```

防止“schema 没变但业务语义漂移”。

#### 5.3.152 MCP Security Test

建议注入：

```text
malicious description
prompt-injected resource
stale capability
wrong tenant token
expired auth
path traversal
SSRF URL
oversized result
malformed schema
```

验证 Host / Server 是否安全失败。

#### 5.3.153 Fault Injection

可靠性测试可以注入：

```text
server timeout
connection reset
429
503
partial result
protocol mismatch
list_changed during task
auth expiry
```

观察 recovery 是否正确。

#### 5.3.154 Counterfactual Policy Test

同一个 Tool Call，只改变：

```text
permission scope
side-effect class
user role
server trust tier
```

系统应做出不同决策。

这可以检测 Policy 是否真的生效。

#### 5.3.155 MCP Evaluation 不应只做 Connectivity Test

```text
“能列出 tools”
```

只能说明最底层连通。

真正 Agent-grade Eval 需要：

```text
Discover → Select → Call → Observe → Verify → Recover
```

整链评测。

#### 5.3.156 常见失败模式 1：把 MCP 当 Function Calling

结果是把协议层和模型层混在一起，导致：

```text
模型 schema
server schema
permission
execution
```

职责不清。

#### 5.3.157 常见失败模式 2：连接就全部暴露

```text
connect server
→ expose every tool to model
```

会增加：

```text
selection error
context cost
attack surface
```

#### 5.3.158 常见失败模式 3：把 Server Description 当可信 Instruction

Server metadata 是外部输入。

不能拥有比 Host System Policy 更高的优先级。

#### 5.3.159 常见失败模式 4：只校验 Schema，不校验 Permission

```text
arguments valid
```

不代表：

```text
user authorized
```

#### 5.3.160 常见失败模式 5：Roots 当 Sandbox

这是经典误解。

Roots 即便在旧版存在，也不是 filesystem enforcement boundary。

#### 5.3.161 常见失败模式 6：把旧协议教程当永久规范

例如把：

```text
initialize
session id
standalone sampling
roots
```

全部当成 MCP 永恒结构。

应始终结合 revision。

#### 5.3.162 常见失败模式 7：Token Passthrough

把一个服务的 bearer token 透传给另一个服务，会造成 audience / trust boundary 混乱。

#### 5.3.163 常见失败模式 8：Server Name Spoofing

按 name 直接授予高权限，而没有验证 endpoint / publisher / installation source。

#### 5.3.164 常见失败模式 9：Tool Explosion

几十个 Server 的 Tools 一次性全部塞给模型。

#### 5.3.165 常见失败模式 10：Stale Discovery Cache

Server 已更新 capability，但 Host 继续使用旧 Schema。

#### 5.3.166 常见失败模式 11：Silent Semantic Drift

Schema 不变，但 Tool 从 read-like 变成 write-like 语义。

#### 5.3.167 常见失败模式 12：Retry Multiplication

Transport、SDK、Server、Harness 同时 retry。

#### 5.3.168 常见失败模式 13：Remote Result 直接进 Context

没有 provenance、过滤、截断和 trust label。

#### 5.3.169 常见失败模式 14：跨 Tenant Cache

Cache 没带用户 / scope 维度。

#### 5.3.170 常见失败模式 15：Local Server 过度授权

为了方便给本地 Server 整个 home directory、shell 和所有环境变量。

#### 5.3.171 常见失败模式 16：Policy Bypass Fallback

Server A 拒绝后自动尝试 Server B 绕过权限。

#### 5.3.172 常见失败模式 17：没有 Capability Provenance

最后只知道调用了 `search`，不知道来自哪个 Server / Version。

#### 5.3.173 常见失败模式 18：Unknown Outcome 被当失败

effectful MCP Tool timeout 后直接 retry，导致重复副作用。

#### 5.3.174 常见失败模式 19：把 Protocol Success 当 Task Success

```text
MCP response = success
```

不代表：

```text
user goal achieved
```

#### 5.3.175 常见失败模式 20：不做版本兼容测试

升级 Server / SDK 后直接生产切换。

#### 5.3.176 工程原则 1：协议层与 Agent 层分离

MCP 负责互操作；Agent 负责决策。

#### 5.3.177 工程原则 2：Discovery ≠ Authority

发现能力之后再做 Trust / Permission / Visibility。

#### 5.3.178 工程原则 3：Server 是供应链主体

按软件依赖管理其来源、版本、权限和升级。

#### 5.3.179 工程原则 4：外部内容默认不可信

Tool Result、Resource、Prompt、Description 都要过信任边界。

#### 5.3.180 工程原则 5：最小权限

Server、Tool、User Scope 都应最小化。

#### 5.3.181 工程原则 6：最小能力暴露

当前 Step 不需要的 Tool，不必给模型看。

#### 5.3.182 工程原则 7：版本感知

记录 Protocol Version、Server Version、Capability Version。

#### 5.3.183 工程原则 8：保留 Provenance

每条 MCP-derived Evidence 都能追到 Server / Capability / Call。

#### 5.3.184 工程原则 9：区分协议错误与业务错误

不要压成统一异常。

#### 5.3.185 工程原则 10：Effect-aware Recovery

effectful timeout 必须先 reconciliation，再决定 retry。

#### 5.3.186 工程原则 11：Approval 绑定最终 Effect

不能批准模糊 Skill 后自动允许所有 MCP 写操作。

#### 5.3.187 工程原则 12：缓存必须 scope-aware

Discovery / Result / Auth cache 都要带正确身份与权限维度。

#### 5.3.188 工程原则 13：旧 Feature 不作为新架构硬依赖

对 deprecated capability 要有迁移意识。

#### 5.3.189 工程原则 14：契约测试

升级前验证 schema、semantics、side effects、errors。

#### 5.3.190 工程原则 15：端到端评测

不要只做协议连通性测试。

#### 5.3.191 Coding Agent 示例

```text
Coding Host
├── Filesystem Native Tool
├── GitHub MCP Server
│   ├── search_code
│   ├── create_issue
│   └── create_pr
└── Database MCP Server
    └── query_test_results
```

Agent 当前任务只是定位 bug：

```text
Capability Retrieval
→ expose search_code + query_test_results
```

不应顺便暴露：

```text
create_pr
admin mutation
```

直到真正需要。

#### 5.3.192 Research Agent 示例

```text
Research Agent
→ MCP Server A: internal papers
→ MCP Server B: experiment artifacts
→ Native Web Search
```

最终 Evidence 必须保留来源，不能把三者全部压成“模型知道”。

#### 5.3.193 Enterprise Agent 示例

```text
Employee Agent
→ CRM MCP
→ Calendar MCP
→ HR MCP
```

即使 Host 连接了三个 Server，某员工权限仍可能只有：

```text
CRM read
Calendar read/write own events
HR self-service only
```

权限不能由 Tool Discovery 自动推断。

#### 5.3.194 一个完整 MCP Action Trace

```text
User Goal
↓
Agent State
↓
Capability Retrieval
↓
MCP Tool Selected
↓
Harness Permission
↓
Approval if needed
↓
MCP Client Request
↓
MCP Server
↓
External Service
↓
Raw Result
↓
Observation Normalization
↓
State Update
↓
Verification
```

这才是 MCP 在完整 Agent System 中的位置。

#### 5.3.195 与前面章节的连接

```text
3. Tool Use
→ MCP Tool 仍遵循 Tool Contract

4. Retrieval
→ MCP Resource / Tool Registry 需要 Retrieval

5.1 Native Tools
→ MCP 是另一种 Integration Source

5.2 Skills
→ Skill 可以依赖 MCP Capability

7. Harness
→ MCP Capability 的可见性 / 权限 /审批由 Harness 控制

8. Runtime
→ Transport / Credential / Recovery / Durable State 由 Runtime 承担
```

#### 5.3.196 MCP 的一句话心智模型

> **Function Calling 让模型表达“我要调用一个能力”；MCP 让 Host 以标准协议找到、理解并连接这个外部能力；Harness 决定它是否可以被使用；Runtime 负责把调用安全可靠地执行。**

#### 5.3.197 面试高频：MCP 是什么？

推荐回答：

> MCP 是 AI Host 与外部 Capability Provider 之间的开放互操作协议。Server 可以标准化暴露 Tools、Resources、Prompts 及扩展能力；Host 通过 MCP Client 发现和调用这些能力。它解决的是能力接入与互操作，不等于 Function Calling，也不负责 Agent 自身的规划与权限策略。

#### 5.3.198 面试高频：MCP 和 Function Calling 有什么区别？

```text
Function Calling
= Model → structured action proposal

MCP
= Host ↔ external capability provider protocol
```

二者经常串联，但不是替代关系。

#### 5.3.199 面试高频：MCP 和 Tool 有什么区别？

Tool 是 capability；MCP 是暴露 / 发现 / 调用 capability 的协议。

#### 5.3.200 面试高频：MCP 和 API 有什么区别？

API 是具体服务自己的接口；MCP 是面向 AI Host 的标准适配层，MCP Server 往往在内部再调用 API。

#### 5.3.201 面试高频：MCP 和 Skill 有什么区别？

Skill 是任务方法；MCP 是能力互操作协议。Skill 可以依赖通过 MCP 获得的 Tool。

#### 5.3.202 面试高频：MCP 和 A2A 的区别？

MCP 更偏 Agent ↔ Tool/Data/Capability；A2A 更偏 Agent ↔ Agent 协作。

#### 5.3.203 面试高频：MCP 有哪几个核心角色？

至少能说清：

```text
Host
Client
Server
```

并解释 Client 是 Host 内协议端点。

#### 5.3.204 面试高频：Tools / Resources / Prompts 区别？

```text
Tools      → Actions
Resources  → Addressable Data
Prompts    → Reusable Interaction Templates
```

#### 5.3.205 面试高频：MCP Server 安全吗？

不能只回答“协议有 OAuth 所以安全”。

应该拆：

```text
server trust
transport security
authorization
permission
content trust
side effects
sandbox
supply chain
```

#### 5.3.206 面试高频：Roots 是不是目录权限？

不是。历史 Roots 是 workspace guidance，不是 filesystem access-control boundary；并且 2026-07-28 已进入弃用路径。

#### 5.3.207 面试高频：Sampling 是什么？

历史上用于 Server 请求 Client 侧模型生成；现代协议已调整相关交互方式，旧 standalone Sampling feature 已进入弃用路径，因此应结合协议 revision 回答。

#### 5.3.208 面试高频：为什么 MCP 还需要 Harness？

因为 MCP 告诉系统“能力是什么、怎样连接”，Harness 决定“什么时候能用、谁能用、是否审批、暴露哪些”。

#### 5.3.209 面试高频：如何避免 MCP Tool 太多？

```text
Registry
→ Capability Retrieval
→ Policy Filter
→ Model-visible Subset
```

而不是全部放入 Context。

#### 5.3.210 面试高频：MCP 失败如何排查？

按层拆：

```text
Discovery
Transport
Version
Auth
Schema
Selection
Execution
Observation
Verification
```

#### 5.3.211 面试高频：如何评价一个 MCP Integration？

至少测：

```text
Task Success
Discovery Accuracy
Selection Accuracy
Latency
Cost
Failure Rate
Recovery
Security
Observability
```

#### 5.3.212 面试高频：MCP 的最大价值是什么？

不是“能接工具”，而是：

> **让不同 AI Host 与不同 Capability Provider 之间形成可复用的互操作边界，降低重复适配成本，同时为 Discovery、Versioning、Auth、Observability 和扩展机制提供公共基础。**

#### 5.3.213 一句话总结

> **MCP 是 Capability Interoperability Layer：它标准化 Host 与外部 Server 之间的能力发现、描述、交互和扩展；但它不替代 Function Calling、Harness、Runtime、Permission、Verification，也不会自动把外部能力变成可信或安全的能力。**

#### 5.3.214 当前版本特别提示（2026-10-18）

当前学习 MCP 时应优先理解 `2026-07-28` 规范代际，同时保留旧版兼容知识：

```text
Modern era
→ per-request metadata / discovery / modern multi-round interaction

Legacy era
→ initialize / session-oriented lifecycle
```

并特别注意：

```text
Roots                  → deprecated
standalone Sampling    → deprecated
protocol Logging       → deprecated
ping                    → removed in modern revision
```

不要用旧教程的 method-level 细节覆盖稳定的架构概念。

#### 5.3.215 参考资料

1. Model Context Protocol Specification — Overview / Base Protocol / Authorization / Server & Client Features.
2. MCP Specification `2026-07-28` — protocol revision and feature lifecycle.
3. Model Context Protocol official SDK documentation — protocol versions, Tools, Resources, Prompts, Elicitation, Multi Round-Trip Requests.
4. MCP Authorization specification — OAuth-based authorization framework for HTTP transports.
5. MCP Security Best Practices — token passthrough, confused deputy, credential and authorization boundaries.
6. MCP Skills Extension — transport binding for publishing Skills alongside MCP capabilities.
7. MCP Tasks Extension — durable asynchronous task handles and input-required interaction.
8. JSON-RPC 2.0 — conceptual RPC message foundation used by MCP protocol generations.

