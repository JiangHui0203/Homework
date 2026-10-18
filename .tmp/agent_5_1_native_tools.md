### 5.1 Native Tools

#### 5.1.1 定义：什么是 Native Tool？

在本知识体系中，**Native Tool（原生工具）**指的是：

> **被某个模型平台、Agent SDK、Agent Runtime 或宿主环境以 first-class capability 的形式直接集成，并且在注册、调用、执行、状态、权限、Observation、Tracing 或生命周期管理上获得原生支持的 Tool。**

它强调的不是“这个能力在世界上是否原生存在”，而是：

```text
Capability
    ↓
被当前 Agent Platform / Runtime
作为 first-class integration 提供
    ↓
Native Tool
```

因此，`Native` 是一个**系统集成属性**，不是能力本体的自然属性。

例如同样的 Web Search：

```text
Platform A
→ Hosted Web Search
→ Native Tool

Platform B
→ 自己包装 search_api(query)
→ Function Tool

Platform C
→ MCP Server 暴露 web_search
→ MCP Tool
```

它们解决的用户需求可能相同，但：

```text
Execution Owner
Credential Handling
Permission Model
Latency
Result Schema
Observability
Failure Semantics
Cost Accounting
```

都可能不同。

---

#### 5.1.2 “Native” 不是行业统一协议名

必须先避免一个术语陷阱：

> **Native Tool 不是像 HTTP、MCP 那样有统一 wire protocol 的标准术语。**

不同平台可能使用：

```text
built-in tool
hosted tool
provider tool
native capability
managed tool
first-party tool
runtime tool
```

这些词的范围不完全一致。

所以工程讨论里最好明确：

```text
Native to what?
```

即：

```text
Native to Model Provider?
Native to SDK?
Native to Runtime?
Native to Sandbox?
Native to Product Host?
```

例如一个 `shell`：

```text
可能是 SDK 内置接口
但执行发生在本地 Runtime
```

它可以是：

```text
SDK-native
```

却不是：

```text
provider-hosted
```

这两个维度不能混。

---

#### 5.1.3 为什么需要区分 Native Tool？

因为 Agent 的能力不只是：

```text
有没有 Tool？
```

还包括：

```text
Tool 是谁提供的？
谁执行？
谁持有凭证？
谁维护状态？
谁定义权限？
结果怎么回到模型？
失败怎么表示？
谁负责审计？
```

同样的业务能力，如果集成方式不同，系统属性会完全不同。

因此 Capability Extension 不能只画成：

```text
Agent
↓
Tools
```

而应该进一步看到：

```text
Agent Capability Surface
├── Model-intrinsic Capability
├── Native / Built-in Tools
├── Function Tools
├── Skills
├── MCP-exposed Capabilities
├── Agents-as-Tools / Subagents
└── External Services / APIs
```

---

#### 5.1.4 Native Tool ≠ Model Intrinsic Capability

模型本身能够：

```text
写文本
做语言推理
根据已有 Context 做判断
生成结构化输出
```

这些通常属于：

```text
Model Capability
```

而：

```text
搜索互联网
执行 Python
读取文件系统
点击网页
调用企业数据库
```

需要真实外部系统参与。

所以：

```text
Model can reason about search
≠
Model can access the live web
```

同样：

```text
Model can write Python
≠
Python code has actually executed
```

Native Tool 本质上是在：

```text
Model Decision
```

和：

```text
External Capability
```

之间建立 first-class bridge。

---

#### 5.1.5 Native Tool ≠ Function Calling

`Function Calling` 解决的是：

> **模型怎样结构化表达“我要调用某个能力”。**

Native Tool 解决的是：

> **这个能力是否已经被平台/Runtime 以 first-class 方式集成。**

因此可以有：

```text
Native Tool
    ↓
通过统一 Tool Call Interface 被调用
```

也可以有：

```text
Developer Function
    ↓ wrap
Function Tool
    ↓
同样通过 Tool Call Interface 被调用
```

所以：

```text
Function Calling
= action interface

Native Tool
= capability integration category
```

两者不是同一层。

---

#### 5.1.6 Native Tool ≠ Function Tool

Function Tool 常见结构是：

```text
Developer Function / API Wrapper
        ↓
Name + Description + Schema
        ↓
Model Tool Call
        ↓
Application / Runtime Executes
```

而 Native Tool 可能直接由：

```text
Provider
SDK
Sandbox Runtime
Product Host
```

实现与维护。

最关键的区别不是：

```text
是不是函数
```

而是：

```text
Capability Integration Ownership
```

谁拥有：

```text
registration
execution adapter
credential path
runtime semantics
result normalization
tracing
versioning
```

---

#### 5.1.7 Hosted Tool 与 Native Tool 的关系

**Hosted Tool** 是 Native Tool 的一个常见子类型：

```text
Native Tool
├── Hosted / Provider-executed
├── SDK-native but Local-executed
├── Sandbox-native
└── Product-host-native
```

Hosted Tool 的典型特征是：

```text
Tool Call
↓
Provider Infrastructure
↓
Execution
↓
Result
```

应用侧不一定需要自己实现实际执行函数。

但：

> **Native 不必 Hosted。**

例如一个 SDK 自带的 `computer` 或 `apply_patch` abstraction，可能是 SDK-native，但真正操作的是本地环境。

---

#### 5.1.8 Native Tool ≠ External API

External API 是一个服务接口。

Native Tool 是 Agent 系统对能力的集成方式。

例如：

```text
Google Calendar API
```

本身不是 Agent Tool。

只有当它被包装成：

```text
create_calendar_event(...)
```

并注册给 Agent 后，才进入 Agent Action Space。

它可以：

```text
被开发者包装成 Function Tool
```

也可以：

```text
被平台作为 Connector / Native Integration 提供
```

所以：

```text
API
= system interface

Tool
= agent-facing capability contract
```

---

#### 5.1.9 Native Tool ≠ Skill

Skill 主要回答：

> **Agent 是否拥有一套可复用的“怎么做”的知识、流程、策略或操作方法。**

Native Tool 主要回答：

> **Agent 是否拥有一个 first-class executable capability。**

例如：

```text
Native Tool:
filesystem.write_file
```

而 Skill 可能是：

```text
“如何安全修改大型仓库配置文件”
├── 先读取
├── 检查版本
├── 修改最小范围
├── 运行验证
└── 查看 diff
```

Skill 可以调用多个 Tools。

所以：

```text
Tool
= capability primitive

Skill
= reusable capability composition / know-how
```

---

#### 5.1.10 Native Tool ≠ MCP Tool

MCP 解决的是：

> **外部 Capability 怎样通过标准化协议被发现、描述与调用。**

Native Tool 强调：

> **Capability 是否已被当前 Host / SDK 作为 first-class integration 纳入。**

因此一个 MCP Tool 可以同时是 Native Tool，也可以不是。

例如：

```text
Remote MCP Server
        ↓
Host Platform 直接托管 MCP integration
        ↓
对 Agent 来说是 first-class
```

这时可以说：

```text
Hosted MCP capability
```

但它的能力来源仍然是 MCP Server。

所以不要写成：

```text
Native Tool vs MCP
```

仿佛二者互斥。

更准确是：

```text
Integration Origin
×
Transport / Protocol
×
Execution Ownership
```

三个独立维度。

---

#### 5.1.11 Native Tool ≠ Plugin / Connector

Plugin / Connector 往往是更高一层的：

```text
Capability Package / Integration Package
```

它可能内部暴露：

```text
多个 Tools
多个 Resources
Authentication
Configuration
Permissions
UI
Actions
```

因此：

```text
Connector
    ↓ exposes
Tool A
Tool B
Tool C
```

一个 Connector 不是一个 Tool。

Native Connector 也不意味着其内部每个 Tool 都应该对模型无条件可见。

---

#### 5.1.12 判断 Native Tool 的五个维度

讨论一个 Tool 是否“原生”时，建议拆成五个维度：

```text
1. Provisioning
   谁提供？

2. Registration
   是否无需开发者自己定义完整 wrapper？

3. Execution
   谁真正执行？

4. Lifecycle Integration
   是否原生进入 Session / Sandbox / Trace / Billing / Permission？

5. Discovery
   是否能被系统自动发现 / 延迟加载 / 动态暴露？
```

因此 `native` 最好不是一个 Boolean：

```text
native = true / false
```

而应理解成一组集成属性。

---

#### 5.1.13 First-class Integration 到底意味着什么？

一个真正 first-class 的 Native Tool，通常会在若干方面得到平台级支持：

```text
Tool Registration
Schema / Capability Contract
Execution Adapter
Credential Binding
Session Binding
Sandbox Binding
Permission
Approval
Result Normalization
Tracing
Cost Accounting
Retry / Timeout
Observability
Lifecycle
```

不是每个平台都全部具备。

所以：

> **“平台有这个 Tool”不自动等于“平台替你处理了全部可靠性问题”。**

---

#### 5.1.14 Capability 注册：Pre-registered vs Runtime-added

Native Tool 可以：

```text
Pre-registered
```

例如系统启动时就存在：

```text
web_search
file_search
code_interpreter
```

也可以：

```text
Runtime-added
```

例如进入某个 Sandbox 后才有：

```text
workspace.shell
workspace.filesystem
```

因此 Tool Availability 是动态 State：

```text
AvailableTools_t
```

而不是静态常量。

---

#### 5.1.15 Visibility ≠ Availability ≠ Authority

继续沿用前面的严格边界：

```text
Available
= 系统当前具备

Visible
= 当前模型能看到

Selectable
= Policy 允许模型提出

Authorized
= 当前身份有权执行

Approved
= 必要的人类确认已完成

Executable
= Runtime 当前满足执行条件
```

因此：

```text
Native Tool
≠
Always Visible
≠
Always Authorized
```

Native 只描述集成程度，不描述权限大小。

---

#### 5.1.16 Native Tool 的 Model-facing Contract

即使 Native Tool 是平台内建能力，模型仍然需要理解：

```text
它叫什么？
它能做什么？
什么时候用？
输入是什么？
会返回什么？
```

所以 Native Tool 同样需要：

```text
Name
Description
Schema / Parameters
Output Semantics
Side-effect Semantics
```

平台原生并不会消除 3.2 / 3.3 里的 Tool Schema 与 Description 问题。

---

#### 5.1.17 Execution Ownership 是核心差异

Native Tool 设计最重要的问题之一：

> **谁真正执行？**

常见结构：

```text
Model Provider executes
SDK Runtime executes
Application executes
Sandbox executes
Browser / OS executes
Remote Service executes
```

这会直接决定：

```text
credentials
latency
observability
retry semantics
data boundary
failure mode
billing
```

因此同一个 Tool Name 并不足以说明系统行为。

---

#### 5.1.18 Credential Ownership

Native integration 的优势之一可能是：

```text
Model does not need raw credentials
```

更合理的结构：

```text
Model
→ proposes action

Harness
→ validates / authorizes

Runtime / Provider
→ injects credential inside trusted boundary

Service
→ executes
```

所以：

> **Agent 能使用能力，不等于模型可以读取凭证。**

这仍然遵循：

```text
Capability Access
≠
Credential Access
```

---

#### 5.1.19 Observation Contract 仍然存在

Native Tool 返回的结果也必须进入：

```text
Raw Result
↓
Observation
↓
State / Context
```

不能因为 Tool 是 Native，就默认：

```text
Result = Ground Truth
```

例如 Web Search 原生集成仍然可能返回：

```text
stale page
low-authority source
SEO spam
malicious content
contradictory evidence
```

所以：

> **Native execution 不等于 native truth。**

---

#### 5.1.20 Native Tool 与 Session State

某些 Native Tools 与 Session 强绑定。

例如：

```text
Sandbox filesystem
Browser session
Code interpreter container
Computer session
```

这些能力可能依赖：

```text
session_id
workspace_id
container_id
browser_state
```

所以它们不是纯函数：

```text
f(args) → result
```

而更像：

```text
f(session_state, args)
→ result + new_session_state
```

这意味着：

```text
Tool Identity
```

还不够，必须知道：

```text
Execution Context Identity
```

---

#### 5.1.21 Native Tool 与 Sandbox

Sandbox-native capability 的核心优势不是“能运行代码”这么简单。

而是：

```text
Capability
+
Isolated Environment
+
Scoped Filesystem
+
Resource Limits
+
Lifecycle
+
Audit
```

因此：

```text
shell in sandbox
```

和：

```text
shell on host machine
```

虽然 Tool Schema 可能一样，安全语义完全不同。

---

#### 5.1.22 Native Web Search

Native Search 常见优势：

```text
无需自己维护 search API wrapper
原生结果结构
原生 citations / provenance metadata
统一 tracing
统一 cost accounting
```

但仍然必须处理：

```text
query quality
source quality
freshness
search bias
retrieval poisoning
prompt injection
citation correctness
```

所以 Native Search 只是减少 Integration Burden，不消除 Retrieval Engineering。

---

#### 5.1.23 Native File Search / Retrieval

Native File Search 通常把：

```text
ingestion
indexing
vector retrieval
ranking options
```

部分托管给平台。

但系统仍然必须明确：

```text
canonical source 是什么？
index 是否 fresh？
权限是否正确？
metadata filter 是否完整？
删除是否传播？
```

即：

```text
Managed Retrieval
≠
Managed Truth
```

---

#### 5.1.24 Native Code Execution

Code Execution 的能力链应理解为：

```text
Model writes code
        ↓
Native Code Tool
        ↓
Sandbox / Interpreter
        ↓
stdout / files / artifacts
        ↓
Observation
```

这里至少有三种正确性：

```text
Code syntactically valid?
Execution succeeded?
Task outcome correct?
```

它们不能合并。

同样：

```text
exit code = 0
≠
user goal achieved
```

---

#### 5.1.25 Native Shell

Shell 是一个典型的**高通用、高风险** Tool。

优势：

```text
Capability breadth very high
```

代价：

```text
Action Surface Area high
Security risk high
Verification burden high
```

所以 Native Shell 最合理的搭配通常是：

```text
Sandbox
Working-directory scope
Resource limit
Network policy
Command logging
Approval for risky actions
```

而不是“原生提供了 Shell，所以模型可以随便执行”。

---

#### 5.1.26 Native Filesystem Tool

Filesystem Native Tool 可以提供：

```text
read
write
list
search
patch
move
```

但需要特别区分：

```text
Workspace Filesystem
vs
Host Filesystem
vs
User Filesystem
vs
Mounted External Storage
```

因为：

```text
/path/to/file
```

本身不能说明安全边界。

真正重要的是：

```text
Mount Scope
Permission
Ownership
Version / ETag
Effect Semantics
```

---

#### 5.1.27 Native Computer / Browser Use

Computer Use 把 Action Space 提升成：

```text
click
scroll
type
keypress
screenshot
```

它的风险在于：

```text
UI state is partially observable
coordinates can drift
pages change
side effects may be irreversible
```

所以 Native Computer Tool 仍然需要：

```text
Observe
Act
Re-observe
Verify
```

而不能：

```text
plan 20 clicks
→ blind execute
```

---

#### 5.1.28 Native Image / Media Generation

Image Generation、Speech、Transcription 等也可以是 Native Capability。

它们与普通文本工具的区别可能包括：

```text
binary / artifact output
large payload
streaming
moderation
storage lifecycle
content provenance
```

所以结果往往不应该直接全文进入 Context，而应进入：

```text
Artifact Store
+
Reference / Metadata
```

---

#### 5.1.29 Native Tool Search / Deferred Loading

当 Tool Catalog 很大时，可以把能力本身也变成可检索对象：

```text
Large Capability Space
        ↓
Tool Search
        ↓
Relevant Tool Subset
        ↓
Expose to Model
```

这和 3.4 的 Tool Retrieval 完全一致。

核心价值是：

```text
Context Pressure ↓
Selection Confusion ↓
Token Cost ↓
```

但同时增加：

```text
Tool Retrieval Failure
```

新的 failure layer。

---

#### 5.1.30 Native ≠ Always-loaded

原生能力可以：

```text
Built-in but Deferred
```

也就是说：

```text
平台原生支持
```

不等于：

```text
每轮都塞进 Tool Catalog
```

这再次说明：

```text
Provisioned Capability
≠
Current Context-visible Capability
```

---

#### 5.1.31 Capability Discovery 与 Native Tool

Native Tool 常常最容易被 Host 发现，因为 Host 已经知道它的：

```text
metadata
schema
runtime adapter
permission requirements
```

但 Capability Discovery 仍然是独立问题。

例如：

```text
100 个 Native Tools
```

模型未必应该每轮全部看到。

所以：

```text
Native Provisioning
↓
Capability Registry
↓
Discovery / Retrieval
↓
Visibility
↓
Selection
```

是更完整的链条。

---

#### 5.1.32 Permission Policy 不能由 Native Tool 自己决定

Tool 可以告诉系统：

```text
“执行这个动作需要 calendar.write”
```

但是否授予：

```text
calendar.write
```

应由：

```text
Identity
Policy
Scope
Approval
```

共同决定。

因此：

> **Native Tool 是 Capability，不是 Authority。**

---

#### 5.1.33 Approval Policy

高风险 Native Tool 仍然可能需要 Human Approval。

例如：

```text
send email
purchase
publish
production deploy
delete resource
```

即使 Tool 由平台原生提供：

```text
Native
≠
Safe to auto-execute
```

Approval 应绑定：

```text
Final Resolved Action
+
Arguments
+
Effect Scope
```

而不是只批准 Tool 名字。

---

#### 5.1.34 Native Tool 与 Side Effect

Native integration 不改变 Side-effect 语义。

仍然需要区分：

```text
Read-only
Mutating
Destructive
Irreversible
External Communication
Financial
Permission-changing
```

因此 Native Tool Catalog 最好带有：

```text
Effect Metadata
```

供 Harness 做：

```text
risk-aware selection
approval
budget
logging
```

---

#### 5.1.35 Native Tool 的 Blast Radius

一个看似简单的 Native Tool：

```text
publish_post
```

可能触发：

```text
public visibility
notification
indexing
webhook
analytics
third-party syndication
```

所以 Tool “原生”只意味着 Integration 更紧，不意味着 Blast Radius 更小。

---

#### 5.1.36 Native Tool 的 Determinism

Native 不等于 deterministic。

例如：

```text
calculator
```

可能高度确定。

但：

```text
web search
browser
computer use
remote service
```

高度依赖环境。

因此 Eval 时应区分：

```text
Model Nondeterminism
Tool Nondeterminism
Environment Nondeterminism
```

---

#### 5.1.37 Timeout 与 Retry

平台提供 Native Tool 以后，开发者仍然需要知道：

```text
Timeout means what?
Retry handled where?
Idempotency guaranteed?
Partial execution possible?
```

尤其 effectful Tool：

```text
timeout
≠
failure
```

所以不能因为 Tool 是 hosted，就假设 retry 永远安全。

---

#### 5.1.38 Provider-managed Retry ≠ Business-safe Retry

Provider 可能自动重试：

```text
network request
transport failure
```

但业务层是否可以重复：

```text
charge()
send()
create()
```

是另一回事。

因此必须问：

```text
哪一层 Retry？
重试的是什么？
重试发生在 commit 前还是 commit 后？
```

---

#### 5.1.39 Native Tool 的 Cost Model

原生 Tool 成本可能包括：

```text
per-call fee
compute
search quota
storage
bandwidth
sandbox runtime
third-party API cost
```

所以 Budget 不应只有：

```text
model tokens
```

还要：

```text
Tool Cost Budget
```

而且不同 Native Tools 的单位成本可能完全不同。

---

#### 5.1.40 Native Tool 的 Latency

Latency 可能来自：

```text
Model → Tool scheduling
Provider queue
Remote API
Sandbox startup
Browser load
Tool execution
Result serialization
```

因此：

```text
Native
≠
Low latency
```

Native 主要减少 Integration Complexity，不保证物理延迟。

---

#### 5.1.41 Observability 是 Native Integration 的关键价值

好的 Native Tool Integration 应让系统容易追踪：

```text
call_id
selected tool
arguments
start / end
execution owner
status
latency
cost
result summary
error class
side effect
```

如果平台只返回：

```text
“tool failed”
```

而没有 trace，Native 的工程价值会大幅下降。

---

#### 5.1.42 Provider Trace ≠ Application Trace

Provider 可能记录：

```text
tool call
```

但应用还需要：

```text
user task
agent state
approval
business transaction
final verification
```

所以完整 Trace 常常需要：

```text
Provider Trace
+
Harness Trace
+
Runtime / Business Trace
```

关联。

---

#### 5.1.43 Native Tool Versioning

平台可能升级：

```text
Tool Schema
Result Format
Ranking
Browser Runtime
Search Backend
Execution Environment
```

因此实验记录不能只写：

```text
model = X
```

还要尽可能记录：

```text
tool type
provider version / API version
configuration
environment image
schema / options
```

否则结果不可解释。

---

#### 5.1.44 Managed Capability 也会 Drift

即使你一行代码都没改：

```text
Hosted Search Backend updated
```

也可能改变：

```text
results
ranking
latency
coverage
```

所以：

> **Native Tool 会降低维护成本，但增加一部分 Provider Drift。**

这也是实验复现必须记录环境版本的原因。

---

#### 5.1.45 Portability 与 Vendor Lock-in

Native Tool 的优势：

```text
integration simple
managed lifecycle
less glue code
first-class tracing
```

代价可能是：

```text
provider-specific schema
provider-specific semantics
provider-specific artifacts
provider-specific billing
```

因此系统设计要判断：

```text
这个能力是否值得做 portability abstraction？
```

而不是所有 Tool 都强行抽象成最低公分母。

---

#### 5.1.46 Lowest-common-denominator Abstraction 的问题

为了同时支持多个平台，开发者可能定义：

```text
generic_search(query)
```

但这可能丢失原生能力：

```text
domain filters
location
image search
ranking options
citation metadata
```

所以 portability abstraction 有 trade-off：

```text
Portability ↑
Provider-specific Capability ↓
```

不应机械统一。

---

#### 5.1.47 Capability Equivalence ≠ Semantic Equivalence

两个 Tool 都叫：

```text
web_search
```

并不代表行为等价。

可能不同：

```text
index coverage
freshness
location
safe search
citation policy
ranking
result limits
```

因此 fallback 时不能只按 Name 做替换。

需要：

```text
Capability Contract Compatibility
```

---

#### 5.1.48 Native Tool Fallback

如果 Native Tool 不可用，可以 fallback 到：

```text
External API Function Tool
MCP Tool
Alternative Native Tool
Manual Workflow
```

但必须重新检查：

```text
permission
result schema
freshness
cost
side effect
verification
```

因为：

```text
Fallback same intent
≠
Fallback same semantics
```

---

#### 5.1.49 Native vs External Tool Selection

当系统同时有：

```text
native_web_search
external_search_api
browser_search
```

Router / Tool Selection 不应只问：

```text
谁更强？
```

而要结合：

```text
quality
freshness
latency
cost
permission
privacy
required output
availability
```

计算当前 utility。

---

#### 5.1.50 Native Tool 与 Context Pressure

Native Tools 也需要 model-facing metadata。

如果 Tool Catalog 很大：

```text
Description Tokens ↑
Selection Confusion ↑
Context Cost ↑
```

因此：

```text
Native Tool Search
Deferred Loading
Capability Retrieval
Namespace
```

依然很重要。

---

#### 5.1.51 Tool Result 不应机械塞回 Context

Native Tool 的结果同样可能巨大：

```text
search results
code output
file corpus
browser snapshot
```

因此仍然需要：

```text
Result
↓
Normalize
↓
Artifact / Store
↓
Observation Summary + Reference
↓
Context
```

而不是：

```text
native result
→ append all
```

---

#### 5.1.52 Native Tool 与 Prompt Injection

Native Search / Browser / File Tool 仍然可能把恶意内容带进 Context。

攻击链：

```text
Native Tool retrieves external content
        ↓
Observation
        ↓
Model mistakes data as instruction
        ↓
Unsafe action
```

所以：

```text
Native Source
≠
Trusted Source
```

这是必须长期保留的安全边界。

---

#### 5.1.53 Trusted Integration ≠ Trusted Content

平台可以值得信任地执行：

```text
web_search
```

但搜索回来的网页仍然是：

```text
external_untrusted
```

因此：

```text
Trust in Tool Execution
≠
Trust in Tool Content
```

这两个 trust domain 必须分开。

---

#### 5.1.54 Data Residency / Privacy

Native Hosted Tool 可能意味着数据会离开本地 Runtime。

系统必须知道：

```text
Query sent where?
Files uploaded where?
Artifacts stored where?
Retention how long?
Provider receives what metadata?
```

因此：

```text
Hosted Native Tool
```

不是纯工程便利选择，也可能是：

```text
Data Governance Decision
```

---

#### 5.1.55 Query Minimization

使用 Native Search / Retrieval 时仍应遵守：

```text
Minimum Necessary Data
```

不要把：

```text
full user profile
secret
internal incident detail
```

无必要地塞进 external query。

即：

> **Native Tool 也必须遵循 Data Minimization。**

---

#### 5.1.56 Sandbox Boundary

对于 Native Code / Shell / Computer Tool，真正的安全地基通常不是 Prompt：

```text
“请不要访问敏感文件。”
```

而是 Runtime Boundary：

```text
没有 mount
没有 permission
没有 network route
没有 credential
```

因此继续沿用：

```text
Prompt Policy
<
Runtime Enforcement
```

对于硬安全约束尤其如此。

---

#### 5.1.57 Native Tool 与 Least Privilege

即使平台提供一个能力，也不表示一定要给 Agent。

例如：

```text
Provider offers shell + computer + web + files
```

某个任务真正只需要：

```text
file_search
```

那么最小 Capability Surface 就应该只暴露：

```text
file_search
```

而不是：

```text
“反正是 Native，全开。”
```

---

#### 5.1.58 Capability Surface Area

可以把 Agent 的 Capability Risk 近似理解为：

```text
Capability Surface Area
≈
Visible Capabilities
×
Action Freedom
×
Effect Magnitude
×
Permission Scope
```

Native Integration 可能让能力更容易加入系统。

所以反而更需要：

```text
Capability Governance
```

避免 capability creep。

---

#### 5.1.59 Native Tool 的 Evaluation 不能只测“会不会调用”

至少要分成：

```text
Need-Tool Decision
Tool Selection
Argument Quality
Execution Success
Observation Quality
Task Success
Side-effect Correctness
Cost / Latency
Safety
```

Native Tool 只是减少某些 integration failure，不会消除整个 Tool Use Pipeline。

---

#### 5.1.60 Native Tool Availability Evaluation

Native Tool 可能：

```text
available
unavailable
degraded
rate-limited
permission-blocked
region-blocked
```

Agent 必须能够适应 Capability Availability 的变化。

因此 Eval 应包括：

```text
Tool normally available
Tool missing
Tool degraded
Tool timeout
Tool permission denied
```

而不是只在理想环境测试。

---

#### 5.1.61 Failure Localization

当 Native Tool 任务失败时，不要直接归因：

```text
“模型不会用 Native Tool。”
```

应依次定位：

```text
1. Capability provisioned?
2. Tool visible?
3. Description / schema correct?
4. Model selected correctly?
5. Arguments correct?
6. Permission allowed?
7. Runtime admitted?
8. Provider / local execution succeeded?
9. Result normalized correctly?
10. Observation consumed?
11. Verification correct?
12. Task finally succeeded?
```

这和 Chapter 3 的 Tool Pipeline 完全统一。

---

#### 5.1.62 Native Tool Ablation

一个非常有用的实验设计：

```text
Same Model
Same Task
Same Tool Semantics
```

对比：

```text
Native Tool
vs
Function Tool Wrapper
vs
MCP Tool
```

观察：

```text
Selection Accuracy
Argument Accuracy
Latency
Cost
Failure Rate
Observability
Task Success
```

这样可以真正测出：

> **“Native integration”本身到底贡献了什么。**

---

#### 5.1.63 Native Tool 不应该和模型能力提升混淆

如果：

```text
Model + Native Search
```

比：

```text
Model-only
```

更好，不能直接说：

```text
“模型知识能力提高了。”
```

更准确是：

```text
Agent System Capability ↑
```

因为提升来自：

```text
external capability access
```

而不是模型参数本身变化。

---

#### 5.1.64 Agent Capability 的系统公式

前面已经建立：

```text
Agent Capability
=
f(Model, Harness, Tools, Environment, Feedback)
```

Native Tools 正是在：

```text
Tools + Environment Integration
```

这一部分提高系统能力。

所以：

```text
Same Model
+
Different Native Capability Surface
=
Very Different Agent
```

---

#### 5.1.65 Native Tool 的工程价值到底是什么？

Native Tool 的主要价值通常不是：

```text
“这个能力只有平台能做到。”
```

而是减少：

```text
Glue Code
Integration Burden
Credential Plumbing
Result Adapter
Tracing Setup
Lifecycle Management
```

也就是：

> **把一部分 Harness / Runtime integration 责任标准化或托管。**

---

#### 5.1.66 但 Native Tool 不替代 Harness

即使所有 Tools 都是 Native：

Harness 仍然要决定：

```text
哪些 Tool 对当前 Agent 可见？
什么时候允许使用？
Risk Policy 是什么？
什么时候需要 Approval？
Tool Result 进多少 Context？
失败以后 fallback 什么？
什么时候停止？
```

所以：

```text
Native Tool
≠
Harness Policy
```

---

#### 5.1.67 Native Tool 不替代 Runtime

Native Hosted Tool 可能由 Provider 执行。

但整个 Agent Runtime 仍然需要维护：

```text
Task State
Session
Budget
Checkpoint
Approval
Effect Ledger
Recovery
```

所以：

```text
Tool Runtime
≠
Agent Runtime
```

不要混为一层。

---

#### 5.1.68 Native Tool 与 Workflow

Workflow 完全可以直接使用 Native Tools：

```text
Deterministic Workflow
↓
Native File Search
↓
Deterministic Validation
```

所以：

```text
Native Tool
≠
Agent-only
```

Tool 是 Capability；
Agent / Workflow 是 Control-flow Architecture。

---

#### 5.1.69 Native Tool 与 ReAct

ReAct 可以把 Native Tool 作为 Action：

```text
Reason
↓
Native Web Search
↓
Observation
↓
Reason
```

但：

```text
Native Tool
```

本身并不意味着系统采用 ReAct。

同一个 Tool 可以被：

```text
Workflow
ReAct Agent
Planner-Executor
Supervisor
```

使用。

---

#### 5.1.70 Native Tool 与 Planning

Planner 在计划时应该知道：

```text
Capability available?
Permission?
Latency?
Cost?
Side effect?
```

否则会生成：

```text
Impossible Plan
```

所以 Native Capability Metadata 可以进入 Planner 的 Capability Model。

---

#### 5.1.71 Dynamic Capability State

对于 Native Tools，Agent State 可以显式维护：

```json
{
  "web_search": "available",
  "code_interpreter": "available",
  "computer": "permission_blocked",
  "file_search": "degraded"
}
```

这样 Planner / Router 不必反复尝试已知不可用路径。

---

#### 5.1.72 Capability Health

Native Tool Registry 最好不仅记录：

```text
存在 / 不存在
```

还记录：

```text
health
latency
quota
region
permission
recent failures
```

于是 Tool Selection 可以变成：

```text
Capability-aware Routing
```

而不是静态选择。

---

#### 5.1.73 Native Tool 的 Capability Registry

一个结构化 Registry 可以包含：

```text
name
capability class
provider
execution owner
schema
risk level
side-effect class
permission requirement
session affinity
cost
latency estimate
availability
version
```

后面的 Capability Discovery 就可以基于 Registry 工作。

---

#### 5.1.74 Native Tool 与 Namespace

当 Tool 数量增大时：

```text
files.read
files.write
files.search

browser.open
browser.click
browser.screenshot

code.run
code.test
```

比：

```text
read
write
search
open
click
run
```

更容易建立清晰 Capability Taxonomy。

Namespace 本身也可以成为：

```text
Tool Retrieval / Permission
```

单位。

---

#### 5.1.75 Tool Granularity 仍然重要

Native Tool 可能过细：

```text
mouse_down
mouse_up
move_cursor
```

也可能过粗：

```text
solve_entire_task()
```

因此同样需要在：

```text
Feedback Granularity
Control
Latency
Risk
Model-call Overhead
```

之间平衡。

Native 并不会自动选对 abstraction level。

---

#### 5.1.76 Native Tool Anti-pattern：原生就全开

错误设计：

```text
Provider offers 20 tools
↓
Agent gets 20 tools
```

问题：

```text
context bloat
selection confusion
attack surface
permission surface
```

正确原则：

```text
Need-to-have Capability Exposure
```

---

#### 5.1.77 Anti-pattern：把 Native 当成可信内容源

错误：

```text
这是官方 Native Search 返回的
→ 一定是真的
```

正确：

```text
Execution channel trusted
Content still needs evidence evaluation
```

---

#### 5.1.78 Anti-pattern：隐藏 Execution Ownership

如果团队只知道：

```text
tool = shell
```

却不知道：

```text
local host?
container?
provider sandbox?
workspace sandbox?
```

几乎无法做正确安全评估。

因此 Tool Catalog 必须明确 execution owner。

---

#### 5.1.79 Anti-pattern：认为 Hosted 就无需验证

Hosted Tool 成功返回：

```text
success
```

仍然可能：

```text
结果不满足 Goal
返回证据不足
真实世界状态没达到预期
```

所以：

```text
Hosted Execution Success
≠
Task Success
```

---

#### 5.1.80 Anti-pattern：把 Native Tool 当成 Skill

例如：

```text
“有 shell，所以 Agent 会部署系统。”
```

这是错误的。

Shell 提供：

```text
Action Capability
```

但部署还需要：

```text
procedural knowledge
planning
verification
recovery
```

也就是 Skill / Workflow / Harness 层。

---

#### 5.1.81 Coding Agent 示例

一个 Coding Agent 可能拥有：

```text
Native / first-class workspace capabilities
├── filesystem
├── shell
├── apply_patch
└── code execution
```

合理轨迹：

```text
read failing test
↓
search relevant symbol
↓
read source
↓
apply patch
↓
run targeted test
↓
run broader test
↓
inspect diff
↓
verify invariants
```

关键不是：

```text
“它有 shell。”
```

而是：

```text
Capabilities
+
Harness Policy
+
State
+
Verification
```

共同决定可靠性。

---

#### 5.1.82 Research Agent 示例

Research Agent 可能拥有：

```text
web search
file search
code interpreter
```

一个合理链条：

```text
Form question
↓
Web Search
↓
Source filtering
↓
File / paper retrieval
↓
Evidence extraction
↓
Code Interpreter for analysis
↓
Cross-check
↓
Synthesis
```

Native Tool 解决：

```text
如何访问能力
```

但：

```text
source quality
methodological judgment
citation correctness
```

仍然需要上层 Decision / Verification。

---

#### 5.1.83 Native Tool Failure Modes

典型 Failure Modes：

```text
1. Tool provisioned but not visible
2. Tool visible but permission blocked
3. Wrong native/external route
4. Schema mismatch
5. Provider version drift
6. Session binding lost
7. Credential scope wrong
8. Hosted timeout
9. Duplicate effect
10. Partial execution
11. Observation truncation
12. Tool result mistaken as truth
13. Native search prompt injection
14. Sandbox escape / overbroad mount
15. Sensitive data sent to hosted tool
16. Capability catalog overload
17. Tool search misses capability
18. Fallback semantic mismatch
19. Provider outage
20. False task-success claim
```

---

#### 5.1.84 Engineering Principles

设计 Native Tool Integration 时，建议长期坚持：

1. **Native to what? 先说清集成层。**
2. **Capability ≠ Authority。**
3. **Visible ≠ Authorized ≠ Executable。**
4. **Hosted ≠ Truth。**
5. **Execution Trust ≠ Content Trust。**
6. **只暴露 Minimal Necessary Capability Surface。**
7. **Credential 留在 Trusted Runtime。**
8. **高风险 Native Tool 仍然要 Approval。**
9. **记录 Execution Owner 与 Session Scope。**
10. **Provider Drift 进入实验版本控制。**
11. **Fallback 必须检查 Semantic Compatibility。**
12. **大型 Catalog 用 Capability Retrieval，而不是全量暴露。**
13. **Native Result 仍然经过 Observation Policy。**
14. **Runtime Enforcement 优先于 Prompt-based Safety。**
15. **Native integration 降低 glue code，不降低 Verification 标准。**

---

#### 5.1.85 边界速查表

| 概念 | 核心问题 | 是否必然可执行 | 典型归属 |
| --- | --- | --- | --- |
| Model Capability | 模型本身会什么？ | 否 | Model |
| Tool | Agent 能调用什么能力？ | 取决于 Runtime | Capability |
| Native Tool | 哪些能力被当前 Host first-class 集成？ | 取决于权限/环境 | Platform / SDK / Runtime |
| Function Tool | 哪些函数被包装成 Agent Tool？ | 取决于应用 | Application |
| External API | 外部系统接口是什么？ | 否 | External System |
| Skill | 一类任务应该怎么做？ | 依赖 Tools | Reusable Know-how |
| MCP Tool | 通过 MCP 暴露了什么 Tool？ | 取决于 MCP Host / Server | Interoperability |
| Connector / Plugin | 一组外部能力如何打包接入？ | 不一定 | Integration Package |
| Harness Policy | 当前 Tool 应不应该被使用？ | 不直接执行 | Agent System |
| Runtime | Action 怎样真的发生？ | 是执行层 | Infrastructure |

---

#### 5.1.86 面试掌握：高频问题

**Q1：什么叫 Native Tool？**

不是“模型天生会的能力”，而是被某个 Agent Host / SDK / Runtime 以 first-class 方式集成的 Tool。

**Q2：Native Tool 和 Function Calling 有什么区别？**

Function Calling 是模型表达 Action 的接口；Native Tool 是 Capability 的集成类型。

**Q3：Native Tool 和 Function Tool 有什么区别？**

Function Tool 通常由开发者包装函数；Native Tool 的 registration / execution adapter / lifecycle 由平台或 Runtime first-class 支持。

**Q4：Hosted Tool 一定是 Native Tool 吗？**

通常是某个平台的 Native Tool 子类；但 Native 不一定 Hosted。

**Q5：Native Tool 和 MCP 冲突吗？**

不冲突。MCP 是 capability protocol / interoperability layer；平台可以原生托管 MCP Tool。

**Q6：Native Tool 和 Skill 的区别？**

Tool 是 Action capability；Skill 是“如何组合能力完成某类任务”的 reusable know-how。

**Q7：为什么 Native Tool 仍然需要 Harness？**

因为 Harness 决定 visibility、permission、routing、approval、context、retry、termination 等 policy。

**Q8：为什么 Native Tool 返回结果也不能直接信？**

Execution Channel 可信，不代表外部内容真实、新鲜、权威或无恶意。

**Q9：Native Tool 最大工程价值是什么？**

减少 glue code、credential plumbing、execution adapter、tracing 与 lifecycle integration 的开发负担。

**Q10：Native Tool 最大潜在代价是什么？**

Provider dependency、semantic drift、data boundary、vendor-specific behavior 和 capability lock-in。

**Q11：Native Tool 是不是越多越好？**

不是。Capability Surface 越大，selection confusion、attack surface 和 governance burden 越高。

**Q12：如何评价 Native Tool Integration？**

不能只看 Tool-call success，要联合看 selection、arguments、execution、observation、task success、cost、latency、safety 与 side effects。

**Q13：为什么 Provider-hosted retry 仍可能不安全？**

Transport retry 与 business idempotency 是不同层，effectful action 可能产生 duplicate effects。

**Q14：Native Tool 与 Agenticness 有关系吗？**

没有必然关系。Workflow 也能使用 Native Tool；Native 描述 capability integration，不描述 control-flow autonomy。

**Q15：怎样避免 Native Tool 造成 vendor lock-in？**

对真正需要跨平台的 capability 做 semantic abstraction，同时保留必要 provider-specific capability，不机械追求最低公分母。

---

#### 5.1.87 一句话总结

> **Native Tool 不是“模型自带魔法”，而是被某个 Agent 平台、SDK 或 Runtime 以 first-class 方式接入的 executable capability；它能降低 integration burden，却不会替代权限、Harness、Observation、Verification、Side-effect Control 与 Runtime Reliability。**

---

#### 5.1.88 参考资料

- OpenAI Agents SDK, **Tools**：区分 hosted tools、local/runtime execution tools、function tools、agents-as-tools 等能力类型，并展示 Web Search、File Search、Code Interpreter、Hosted MCP 等 first-class integrations。https://openai.github.io/openai-agents-python/tools/
- OpenAI Agents SDK JavaScript, **Tools**：进一步区分 hosted tools、built-in execution tools、function tools、MCP servers、sandbox capabilities 等类别。https://openai.github.io/openai-agents-js/guides/tools/
- OpenAI Agents SDK, **Model Context Protocol (MCP)**：展示 hosted MCP 与本地/远程 MCP capability integration。https://openai.github.io/openai-agents-python/mcp/
- Google Agent Development / Agents CLI documentation：展示 Agent、Tool、Runtime/Deployment 与 Skills 的不同角色，以及 Tool 通过函数/框架注册给 Agent 的典型方式。https://google.github.io/agents-cli/

