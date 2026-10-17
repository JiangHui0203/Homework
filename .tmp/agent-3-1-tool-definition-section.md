### 3.1 Tool Definition

#### 3.1.1 定义：Tool 到底是什么？

在 Agent 系统里，Tool 不是“模型之外所有能调用的东西”的模糊统称，也不只是一个函数名。

更准确地说：

> **Tool 是由 Agent 可以选择调用、由系统可以真实执行、并且有明确输入、执行语义与输出契约的一种外部能力接口。**

一个最小 Tool 可以抽象成：

```text
Tool
├── Identity
├── Input Contract
├── Execution Semantics
├── Side-effect Semantics
├── Permission Boundary
└── Observation Contract
```

例如：

```text
read_file(path)
```

表面上只有：

```text
name = read_file
argument = path
```

但真正让它成为一个可靠 Tool，还需要知道：

```text
它读取什么范围？
path 是相对路径还是绝对路径？
允许读哪些目录？
文件不存在会怎样？
返回全文还是截断内容？
编码错误怎么表示？
它是否会修改文件？
调用结果以什么结构返回？
```

所以 Tool 的本质不是：

```text
一个 callable
```

而是：

> **一个可被 Agent 决策系统安全理解、调用、执行、观察和验证的 capability contract。**

---

#### 3.1.2 为什么 Agent 需要 Tool？

LLM 本身最擅长的是：

```text
根据 Context 生成下一段 token
```

但真实任务经常需要：

```text
读取最新信息
精确计算
访问文件
执行代码
查询数据库
调用业务 API
修改环境
发送消息
创建资源
与其他系统交互
```

这些能力并不天然包含在一次语言模型 forward pass 里。

因此 Tool 解决的是：

```text
Model's internal generation capability
        ↓
External executable capability
```

之间的接口问题。

可以画成：

```text
LLM Policy
   ↓
Tool Call
   ↓
Harness / Runtime
   ↓
External Capability
   ↓
Observation
   ↓
LLM Policy
```

这也是为什么 Tool Use 是 Agent 从：

```text
“会说”
```

走向：

```text
“能作用于环境”
```

的重要一步。

---

#### 3.1.3 Tool、Function、API、Capability、Action 必须分开

这五个词经常被混用，但最好保持边界。

##### Capability

Capability 是最宽的概念：

> **系统具备完成某类操作的能力。**

例如：

```text
Web Search Capability
File Read Capability
Code Execution Capability
Email Sending Capability
```

它不一定直接暴露给模型。

---

##### Function

Function 是一种程序实现形式：

```python
def read_file(path):
    ...
```

Function 关注：

```text
程序怎样执行
```

它可以被 Tool 包装，也可以只是内部 helper。

所以：

```text
Function
≠
天然就是 Tool
```

例如：

```python
def _delete_internal_cache():
    ...
```

虽然是 function，但可能根本不应该暴露给 Agent。

---

##### API

API 是系统与系统之间的接口。

例如：

```text
GET /weather
POST /email/send
```

Tool 可以封装 API：

```text
get_weather(city)
        ↓
Weather API
```

但 Tool 不一定依赖远程 API。

例如：

```text
calculator
read_file
run_python
```

都可以完全本地执行。

所以：

```text
Tool
≠
API
```

---

##### Action

Action 是 Agent 在某一步选择执行的具体动作实例。

Tool 是：

```text
可选动作类型 / capability interface
```

Action 是：

```text
某一次实际调用
```

例如 Tool：

```text
search_web(query)
```

Action：

```json
{
  "tool": "search_web",
  "query": "ReAct paper"
}
```

可以记成：

```text
Tool
= action type

Tool Call / Action
= action instance
```

---

##### 最终关系

```text
Capability
   ↓ exposed as
Tool
   ↓ may wrap
Function / API / Runtime Primitive
   ↓ selected at runtime as
Action / Tool Call
```

这是后面整章 Tool Use 最重要的术语地基之一。

---

#### 3.1.4 Tool Definition 和 Tool Implementation 不是一回事

Tool Definition 是：

```text
Agent / Model 看见的接口契约
```

Tool Implementation 是：

```text
系统内部真正执行这个能力的代码
```

例如 Agent 看到：

```json
{
  "name": "search_web",
  "description": "Search the web for current information.",
  "parameters": {
    "query": {"type": "string"}
  }
}
```

实际内部可能是：

```text
search_web
    ↓
provider router
    ↓
Search API A / B
    ↓
normalize results
    ↓
filter
    ↓
return Observation
```

模型并不需要知道全部实现细节。

因此：

> **Tool Definition 是 model-facing contract；Tool Implementation 是 runtime-facing execution logic。**

两者可以独立演化。

---

#### 3.1.5 一个完整 Tool Definition 应该包含什么？

最小情况下常见的是：

```text
name
+ description
+ input schema
```

但从系统设计角度，一个完整 Tool Contract 应该至少考虑七个部分：

```text
1. Identity
2. Purpose / Description
3. Input Contract
4. Execution Semantics
5. Side-effect Semantics
6. Permission / Safety Boundary
7. Observation / Output Contract
```

可以写成：

```text
Tool Contract
├── What is this tool?
├── When should it be used?
├── What input does it accept?
├── What exactly happens when executed?
├── What can it change?
├── Under what authority can it run?
└── What observation does it return?
```

这比单纯：

```text
name + JSON schema
```

更接近真实 Agent 系统。

---

#### 3.1.6 Tool Identity：名字不只是标识符

Tool Name 一方面是程序标识符，另一方面也是模型的语义信号。

例如：

```text
search
```

比：

```text
s1
```

更容易让模型理解用途。

但：

```text
search
```

又可能过于宽泛。

如果系统同时存在：

```text
search_web
search_files
search_email
search_database
```

语义边界会更清楚。

因此 Tool Name 设计需要兼顾：

```text
机器稳定性
模型可理解性
命名一致性
版本兼容性
能力区分度
```

一个常见原则：

> **名字负责“这是什么”，Description 负责“什么时候该用、什么时候不该用”。**

---

#### 3.1.7 Tool Description 也是 Agent Policy 的输入

Tool Description 不是普通 API 文档里的装饰文字。

对 LLM Agent 来说，它会直接影响：

```text
Tool Selection
Argument Generation
Failure Avoidance
```

例如两个 Tool：

```text
search_web
search_internal_docs
```

如果 Description 都只写：

```text
Search for information.
```

模型很难知道什么时候该选哪个。

更好的定义：

```text
search_web:
Search public web sources for current or externally published information.

search_internal_docs:
Search private organization documents available to the current user.
```

所以 Tool Description 实际上承担：

```text
Capability Semantics
+
Selection Guidance
```

这也是为什么下一节 3.3 会单独讨论 Tool Description。

---

#### 3.1.8 Input Contract：Tool 能接受什么？

Tool 必须有明确输入边界。

例如：

```text
get_weather(city, date)
```

不能只停留在自然语言：

```text
“帮我查天气”
```

而应该明确：

```text
city: string
date: date | null
```

Input Contract 通常需要表达：

```text
字段
类型
required / optional
enum
范围
格式
默认值
nullable
互斥关系
依赖关系
```

这些会在 3.2 Tool Schema 中细讲。

这里先固定一件事：

> **Input Schema 描述“结构上允许什么输入”，但不等于“这个输入语义上正确、被授权或安全”。**

---

#### 3.1.9 Execution Semantics：同一个名字必须有稳定含义

Tool Definition 必须让系统知道：

```text
调用以后到底发生什么？
```

例如：

```text
save_file(path, content)
```

可能有多种语义：

```text
覆盖原文件
追加写入
不存在则创建
存在则报错
自动创建目录
不自动创建目录
```

如果这些没有定义清楚，Agent 即使参数完全合法，也可能产生错误效果。

所以 Tool Contract 应该尽量说明：

```text
Preconditions
Effects
Failure Semantics
Atomicity
Idempotency
```

这和 Planning 里的 Preconditions / Effects 直接相连。

---

#### 3.1.10 Tool 可以理解成带 Preconditions / Effects 的 Action Operator

从 Planning 视角，可以把一个 Tool 抽象为：

```text
Tool T
├── Preconditions(T)
├── Input(T)
├── Effect(T)
└── Observation(T)
```

例如：

```text
Tool: delete_file(path)
```

Precondition：

```text
path exists
user has delete permission
```

Effect：

```text
file removed
```

Observation：

```text
success / not_found / denied / error
```

因此 Tool 不是只有：

```text
signature
```

而是一个能改变 Agent–Environment transition 的操作符。

---

#### 3.1.11 Side Effect 是 Tool Definition 的一等属性

Tool 最重要的区分之一是：

```text
Read-only Tool
vs
State-changing Tool
```

例如：

```text
read_file
search_web
query_database
```

通常是 read-like。

而：

```text
write_file
send_email
delete_record
create_payment
```

会改变环境。

Side Effect 直接决定：

```text
是否需要审批
retry 是否安全
是否要做 idempotency
是否需要 checkpoint
失败如何恢复
verification 强度
```

所以：

> **Side-effect semantics 不是 Runtime 才需要知道的细节，而应该是 Tool contract 的核心属性。**

---

#### 3.1.12 Read Tool、Write Tool、Irreversible Tool

可以按环境影响粗略分层：

```text
Level 0: Pure / Local Compute
calculator
format_text

Level 1: Read-only External
search
read_file
query_db

Level 2: Reversible Write
edit_draft
create_temp_file

Level 3: Persistent / External Write
send_email
create_issue
commit_code

Level 4: Destructive / Financial / High-risk
remove_resource
transfer_money
revoke_access
```

这不是通用固定标准，但这种风险分层非常有价值。

因为：

```text
Tool exposed
≠
Tool always executable
```

Harness 可以根据风险层级施加不同 policy。

---

#### 3.1.13 Permission Boundary：Tool Available ≠ Tool Authorized

这是 Agent Tool Use 最重要的安全边界之一。

模型在 context 中看见：

```text
send_email
```

只说明：

```text
这个 capability 存在
```

不说明：

```text
当前用户有权对任意地址发送
```

更不说明：

```text
模型自己拥有授权
```

所以必须区分：

```text
Capability Availability
        ↓
Tool Visibility
        ↓
Authorization
        ↓
Approval
        ↓
Execution
```

核心原则：

> **Tool Definition 描述能力；Permission System 决定当前调用有没有权执行。**

---

#### 3.1.14 Authentication、Authorization、Approval 不是一回事

Tool 调用里经常混淆三层：

```text
Authentication
= 你是谁？

Authorization
= 你是否有权做这件事？

Approval
= 这一次具体操作是否得到确认？
```

例如：

```text
用户已经登录邮箱
```

说明 Authentication 成立。

但：

```text
Agent 是否允许删除全部邮件？
```

是 Authorization。

而：

```text
真的要发送这封外部邮件吗？
```

可能还需要一次 Human Approval。

Tool Definition 应该能够被 Harness 映射到这些控制。

---

#### 3.1.15 Observation Contract：Tool 执行以后应该返回什么？

Tool 不只是：

```text
input → side effect
```

还需要：

```text
input → execution → observation
```

一个成熟 Tool Result 最好能区分：

```text
Status
Payload
Error
Metadata
Provenance
Freshness
Warnings
```

例如：

```json
{
  "status": "success",
  "data": {
    "temperature_c": 18
  },
  "source": "weather_provider_x",
  "observed_at": "..."
}
```

而不是只返回：

```text
18
```

因为 Agent 后面还需要判断：

```text
结果可靠吗？
新鲜吗？
有没有 partial failure？
来自哪里？
是否需要再次验证？
```

---

#### 3.1.16 Tool Output 和 Observation 不完全等价

严格说：

```text
Raw Tool Output
```

可能还需要经过：

```text
normalization
filtering
redaction
truncation
provenance attachment
error mapping
```

才形成 Agent 真正看到的：

```text
Observation
```

因此可以写成：

```text
Tool Execution
    ↓
Raw Result
    ↓
Runtime / Harness Processing
    ↓
Observation
    ↓
Context
```

所以：

> **Tool Result 是执行产物；Observation 是被 Agent 消费的状态反馈。**

这一区分后面 3.7 Observation 会展开。

---

#### 3.1.17 Tool Error 也属于 Observation Contract

Tool Contract 不能只定义成功返回。

还需要定义：

```text
invalid_argument
not_found
permission_denied
timeout
rate_limited
unavailable
partial_success
conflict
unknown
```

如果所有异常都变成：

```text
"Something went wrong"
```

Agent 就无法做正确 recovery。

例如：

```text
not_found
→ 可能应该换 path

permission_denied
→ 可能应该请求授权

timeout
→ 可能 retry

conflict
→ 可能重新读取 state
```

所以：

> **错误类型本身也是 Agent 决策信号。**

---

#### 3.1.18 Tool Definition 必须定义 Success，而不是只定义“调用完成”

例如：

```text
send_email(...)
```

Runtime 返回：

```text
request accepted
```

这和：

```text
message delivered
```

不是同一个状态。

再如：

```text
run_tests()
```

Tool execution 成功：

```text
process exited normally
```

并不等于：

```text
all tests passed
```

所以 Tool Result 至少要区分：

```text
Execution Status
vs
Domain Outcome
```

这和 2.6 Verification 完全对应。

---

#### 3.1.19 Synchronous Tool 和 Asynchronous Tool

有些 Tool 可以立即返回最终结果：

```text
calculator
read_file
```

有些 Tool 只是创建任务：

```text
start_training_job
submit_render
launch_batch_job
```

调用后可能返回：

```json
{
  "job_id": "123",
  "status": "queued"
}
```

真正结果需要之后：

```text
poll_status
wait
callback
event
```

因此 Tool Definition 应该说明：

```text
调用完成
≠
业务动作完成
```

尤其对 long-running task 非常重要。

---

#### 3.1.20 Stateful Tool 和 Stateless Tool

Stateless Tool：

```text
calculator(expression)
```

同样输入通常独立执行。

Stateful Tool：

```text
browser_click
terminal_session
transaction_update
```

它的语义依赖当前环境状态。

例如：

```text
click(x=200,y=300)
```

如果页面状态变了，同一个 Action 可能完全不同。

因此 Stateful Tool 更需要：

```text
fresh observation
session identity
state version
precondition check
```

这会和 Runtime 的 Session / State 紧密相关。

---

#### 3.1.21 Deterministic Tool 和 Nondeterministic Tool

Tool 本身也可能有随机性或外部变化。

例如：

```text
calculator
```

通常接近 deterministic。

而：

```text
web_search
recommendation_api
external_market_query
```

结果可能随时间或 backend 状态变化。

因此 Tool Contract 最好让系统知道：

```text
结果是否稳定？
是否时间敏感？
是否值得缓存？
verification 是否需要 freshness？
```

这会直接影响重放、测试和评估。

---

#### 3.1.22 Idempotency 为什么应该进入 Tool 语义？

如果一个 Tool 重复调用：

```text
T(x)
T(x)
```

结果是否等价于调用一次？

这就是 idempotency 的核心直觉。

例如：

```text
read_file(path)
```

通常重复调用不会产生额外副作用。

但：

```text
send_email(...)
```

重复调用可能发送两封邮件。

所以 Tool Definition 至少应允许 Harness 知道：

```text
safe_to_retry?
idempotency_key_supported?
side_effect_scope?
```

否则 Runtime 的普通 retry policy 可能制造严重错误。

---

#### 3.1.23 Atomicity：Tool Call 是不是“一次完成”？

Tool 可能执行多个内部步骤：

```text
create_order
↓
write DB
↓
reserve inventory
↓
charge payment
```

如果中途失败：

```text
前半成功，后半失败
```

就可能出现 partial success。

因此 Tool Contract 应该说明：

```text
atomic
or
partial effects possible
```

以及失败后：

```text
能否 rollback？
如何查询真实 state？
是否需要 compensating action？
```

这对高风险 Agent Tool Use 非常关键。

---

#### 3.1.24 Tool Granularity：Tool 应该多大？

Tool 设计有一个非常重要的问题：

```text
暴露低层原子动作
还是
暴露高层业务能力？
```

例如邮件系统。

低层 Tool：

```text
open_mailbox
find_contact
create_draft
set_recipient
set_subject
set_body
send
```

高层 Tool：

```text
send_email(recipient, subject, body)
```

两种都可能合理。

低层工具：

```text
更灵活
更可组合
```

但：

```text
step 更多
错误面更大
成本更高
```

高层工具：

```text
更稳定
更容易验证
减少 agent loop 次数
```

但：

```text
灵活性较低
业务语义更重
```

所以 Tool Granularity 本质上是在做：

```text
Autonomy
vs
Determinism
```

的分配。

这和上一节 Agent vs Workflow 完全衔接。

---

#### 3.1.25 高层 Tool 本质上可以封装一个 Workflow

例如 Agent 看见：

```text
book_trip(destination, dates, preferences)
```

内部可能执行：

```text
search flights
↓
filter
↓
search hotel
↓
validate dates
↓
create itinerary
```

对 Agent 来说它只是一个 Tool。

因此：

```text
Tool
```

描述的是：

```text
对 Agent 暴露的 capability boundary
```

而不是内部复杂度。

一个 Tool 内部完全可以是：

```text
function
API
workflow
subsystem
another agent
```

这也是后面 “Agents-as-Tools” 能成立的原因。

---

#### 3.1.26 Tool 不一定必须直接暴露给 LLM

系统可能有很多内部能力：

```text
200 tools
```

但当前模型只看到：

```text
8 tools
```

因为 Harness 可以做：

```text
capability filtering
dynamic loading
routing
permission filtering
context budgeting
```

因此：

```text
System Capability Set
        ↓
Currently Exposed Tool Set
        ↓
Model Action Space
```

三者不一定相同。

这也是为什么：

> **Tool Registry 和 Model-visible Tool List 不是一回事。**

---

#### 3.1.27 Tool Registry：系统怎么管理大量 Tool？

Tool Registry 可以理解成：

```text
系统侧的 capability catalog
```

通常保存：

```text
Tool ID
Name
Version
Description
Schema
Runtime Binding
Permission Metadata
Risk Metadata
Ownership
Availability
```

Harness 根据任务和用户状态，从 Registry 中筛出：

```text
Eligible Tools
```

再决定哪些进入当前 Context。

因此：

```text
Registry
= system inventory

Tool Definition in Context
= model-visible projection
```

---

#### 3.1.28 Tool Versioning：接口变化会直接改变 Agent 行为

Tool 不是定义一次就永远不变。

例如：

```text
search_web_v1(query)
```

后来增加：

```text
search_web_v2(query, recency, domains)
```

这会改变：

```text
模型可表达的 action
历史 trajectory 是否可重放
测试样本是否仍兼容
argument generation 是否稳定
```

所以 Tool 版本变化应该纳入：

```text
schema version
behavior version
runtime version
```

管理。

尤其在 Agent Eval 里：

> **Tool Interface 本身就是实验条件的一部分。**

---

#### 3.1.29 Backward Compatibility：Tool 变了，旧 Agent 会怎样？

假设旧模型一直生成：

```json
{
  "query": "..."
}
```

新 Tool 改成必须：

```json
{
  "query": "...",
  "language": "en"
}
```

旧 trajectory replay 可能直接失败。

所以 Tool 演进时需要考虑：

```text
optional fields
default values
schema migration
version pinning
compatibility adapter
```

不能把 Tool 当成无状态 prompt 文本。

---

#### 3.1.30 Tool Definition 与 Prompt 的关系

Tool Definition 最终往往会进入模型 Context。

因此它既是：

```text
machine interface metadata
```

也是：

```text
model-facing prompt context
```

这带来两个后果。

第一：

```text
描述方式会影响模型行为
```

第二：

```text
Tool metadata 也会消耗 context budget
```

如果给模型暴露几百个长 Description：

```text
context 成本上升
selection ambiguity 上升
attention 被稀释
```

因此 Tool Definition 设计也是 Context Engineering 的一部分。

---

#### 3.1.31 Tool Definition 与 Structured Output 的关系

Structured Output 定义：

```text
模型如何表达一个结构化对象
```

Tool Definition 则定义：

```text
有哪些动作可以被表达，以及每个动作的参数契约是什么
```

例如：

```json
{
  "tool": "search_web",
  "arguments": {
    "query": "..."
  }
}
```

Structured Output 保证：

```text
这个对象结构可解析
```

Tool Definition 保证：

```text
search_web 代表什么能力
arguments 应该是什么
```

但两者都不保证：

```text
这次调用是正确的
```

还需要 Tool Selection、Validation 和 Verification。

---

#### 3.1.32 Tool Definition 与 Function Calling 的关系

1.6 已经讲过：Function Calling 是模型表达 Action Request 的机制。

现在可以更精确地说：

```text
Tool Definition
→ 定义 action space

Function Calling
→ 从 action space 中生成一个具体 action instance
```

例如：

```text
Tool Definition:
search_web(query)

Function Call:
search_web(query="Agent evaluation")
```

所以：

> **Tool Definition 是“能调用什么”的契约；Function Calling 是“这一步具体调用什么”的生成机制。**

---

#### 3.1.33 Tool Definition 与 Harness Tool Policy 的关系

Tool 本身定义 capability。

Harness Tool Policy 决定：

```text
什么时候暴露
什么时候允许调用
一次允许几个
是否需要 approval
失败后能否 retry
何时 fallback
是否允许 parallel
何时隐藏
```

因此：

```text
Tool
= Capability

Tool Policy
= Control over Capability
```

这是整套知识体系必须一直保持的边界。

---

#### 3.1.34 Tool Definition 与 Runtime 的关系

Runtime 负责：

```text
真正执行 Tool
```

例如：

```text
subprocess
browser
HTTP
filesystem
database
sandbox
```

Tool Definition 则是：

```text
Agent 可理解的接口层
```

所以：

```text
Tool Definition
≠
Execution Environment
```

同一个 Tool Definition：

```text
run_code(code)
```

可以绑定到：

```text
local sandbox
remote container
cloud worker
```

不同 Runtime。

---

#### 3.1.35 Tool Definition 与 MCP 的关系

MCP 以后会专门讨论。

这里先固定边界：

```text
Tool Definition
= 描述一个可调用能力的接口契约

MCP
= 让外部 capability 可以通过标准协议被 Host / Client 发现和调用
```

MCP Server 可以暴露多个 Tools。

但：

```text
Tool
≠
MCP
```

Tool 可以来自：

```text
native runtime
local function
REST API
MCP server
subagent
```

MCP 只是 capability exposure / interoperability 的一种标准化方式。

---

#### 3.1.36 Tool Definition 与 Skill 的关系

Tool 通常强调：

```text
可执行能力接口
```

Skill 更可能表示：

```text
一套任务知识 / procedure / instruction / reusable workflow
```

Skill 可能调用多个 Tool。

例如：

```text
Skill: review_pull_request
```

内部可能使用：

```text
read_diff
search_repo
run_tests
post_comment
```

所以通常：

```text
Tool
= primitive / executable capability interface

Skill
= reusable higher-level procedure
```

但不同产品命名可能不同，最终要看实际 contract。

---

#### 3.1.37 Tool Definition 与 Resource 的关系

有些系统会区分：

```text
Tool
= 执行动作

Resource
= 可读取的数据 / 对象
```

例如：

```text
Tool: search_documents(query)
Resource: document://policy.pdf
```

这种区分有助于把：

```text
Action
```

和：

```text
Addressable Information
```

分开。

尤其在 MCP 等协议里会很重要。

---

#### 3.1.38 一个标准 Tool Contract 示例

例如定义一个读取文件 Tool：

```yaml
name: read_file
purpose: Read UTF-8 text from an allowed workspace file.
inputs:
  path:
    type: string
    required: true
  start_line:
    type: integer
    optional: true
  end_line:
    type: integer
    optional: true
semantics:
  read_only: true
  deterministic: mostly
  idempotent: true
permissions:
  allowed_roots:
    - workspace
side_effects:
  none
output:
  status:
    enum: [success, not_found, permission_denied, invalid_range, error]
  content:
    type: string
  metadata:
    path: string
    truncated: boolean
```

真正的 Tool Definition 不一定必须用这个格式。

重点是：

```text
接口含义完整
```

而不是只拥有一个 callable signature。

---

#### 3.1.39 一个坏 Tool Definition 长什么样？

例如：

```json
{
  "name": "manage_data",
  "description": "Manage data.",
  "parameters": {
    "input": {"type": "string"}
  }
}
```

问题很多：

```text
manage 是读还是写？
能删吗？
input 到底表示什么？
作用域在哪里？
执行成功怎么判断？
失败怎么返回？
权限是什么？
```

这种 Tool 把大量隐式语义重新丢给模型猜。

结果就是：

```text
Tool Selection ambiguity ↑
Argument ambiguity ↑
Safety surface ↑
Verification difficulty ↑
```

---

#### 3.1.40 Tool Boundary 应该对齐业务语义，而不是后端实现细节

一个常见反模式是：

```text
后端有什么 endpoint
→ 就原样全部暴露给模型
```

但后端 API 的设计目标和 Agent Tool 的设计目标不同。

后端可能有：

```text
/internal/v2/object/update
/internal/v2/object/patch
/internal/v2/object/reindex
```

这些对模型未必是合理 action space。

更好的 Agent Tool 可能是：

```text
update_customer_address(customer_id, address)
```

内部再编排多个 backend calls。

核心原则：

> **Tool boundary 应优先反映 Agent 需要理解的业务动作，而不是暴露底层系统偶然形成的接口形状。**

---

#### 3.1.41 Tool 的参数应该表达 Intent，而不是实现步骤

例如一个搜索 Tool。

差的接口：

```text
open_connection
set_header
send_request
parse_response
```

更适合 Agent 的接口：

```text
search_web(query, recency, domains)
```

因为 Agent 真正需要表达的是：

```text
“我要搜索什么”
```

而不是：

```text
“HTTP 每一步怎么实现”
```

所以 Tool 设计本质上是在做 abstraction。

---

#### 3.1.42 Tool 应该尽量缩小危险的 Action Space

如果模型拥有：

```text
execute_arbitrary_shell(command)
```

它理论上可以完成很多事。

但安全面也极大。

如果实际任务只需要：

```text
run_tests(test_target)
```

那么暴露更窄的 Tool 往往：

```text
更易验证
更易授权
更易审计
更少 prompt injection surface
```

所以：

> **Capability 越通用，不一定越适合作为直接暴露给 Agent 的 Tool。**

这是 Least Privilege 在 Tool Design 上的体现。

---

#### 3.1.43 General Tool vs Domain Tool

通用 Tool：

```text
shell
browser
HTTP request
SQL
```

Domain Tool：

```text
create_invoice
lookup_patient_appointment
approve_expense
run_repo_tests
```

通用 Tool：

```text
灵活
覆盖面广
```

但需要 Agent 自己承担更多：

```text
planning
argument construction
safety reasoning
error recovery
```

Domain Tool：

```text
限制更强
业务语义更明确
更容易验证
```

因此实际系统经常使用：

```text
Domain Tools by default
+
General Tools in sandbox / expert path
```

---

#### 3.1.44 Tool Composition：复杂能力来自 Tool 的组合

Agent 的能力不等于单个 Tool 能力的简单相加。

例如：

```text
search_web
+
read_page
+
calculator
+
write_report
```

组合以后可以完成：

```text
研究 → 取证 → 计算 → 报告
```

所以 Tool Set 实际定义了 Agent 的：

```text
Action Vocabulary
```

而 Agent Loop / Planning 决定：

```text
如何组合这些动作形成 trajectory
```

可以写成：

```text
Tool Set
= Action Alphabet

Trajectory
= Sequence / Graph over Actions
```

---

#### 3.1.45 Tool Completeness：Action Space 是否足以完成任务？

如果 Agent 被要求：

```text
修改代码并提交 PR
```

但 Tool Set 只有：

```text
read_file
search_repo
```

那么任务从一开始就不可完成。

这不是模型能力问题，而是：

```text
Capability Gap
```

因此 Agent failure analysis 首先应该问：

```text
模型选错了吗？
还是根本没有可完成任务的 Tool？
```

这叫：

```text
Action-space feasibility
```

后面 Tool Evaluation 必须考虑这一点。

---

#### 3.1.46 Tool Redundancy：多个 Tool 做相似事情会怎样？

如果系统同时暴露：

```text
web_search
search_web
internet_search
browse_search
```

而语义高度重叠，会导致：

```text
selection entropy ↑
wrong-route rate ↑
prompt tokens ↑
```

所以 Tool Set 设计不只是：

```text
工具越多越好
```

还要考虑：

```text
semantic separation
coverage
redundancy
```

这和 Routing 的 candidate design 类似。

---

#### 3.1.47 Tool Discoverability：模型怎么知道这个 Tool 存在？

Tool 即使系统里存在，如果模型根本看不到：

```text
就等于当前 step 不可用
```

常见方式：

```text
static tool list
filtered tool list
dynamic discovery
search capability catalog
MCP discovery
```

因此 Tool Definition 还必须能支持：

```text
discovery
selection
loading
```

后面 5.4 Capability Discovery 会详细展开。

---

#### 3.1.48 Tool Availability 是动态状态

一个 Tool 的 definition 存在，不代表此刻 backend 正常。

例如：

```text
search tool exists
```

但当前：

```text
provider outage
quota exhausted
auth expired
region blocked
```

所以应该区分：

```text
Defined
Visible
Authorized
Available
Executable
```

这几个状态。

Routing 和 Harness 必须基于真实 availability，而不是只看静态 catalog。

---

#### 3.1.49 Tool Capability 与 Tool Quality 也要分开

一个 Tool 可能“能做”某件事，但做得不一定好。

例如两个搜索 Tool：

```text
A: fast but shallow
B: slower but high-recall
```

它们 capability 相似，但：

```text
quality
latency
cost
freshness
coverage
```

不同。

因此 Tool Metadata 可以进一步包含：

```text
expected latency
cost
quality tier
freshness
rate limit
risk
```

供 Routing / Harness 使用。

---

#### 3.1.50 Tool Definition 也决定 Evaluation Unit

如果 Tool 定义边界清楚，就可以分别评估：

```text
Tool selection correct?
Arguments correct?
Execution successful?
Observation correct?
Result utilized?
Side effect appropriate?
```

如果 Tool Definition 本身模糊，这些指标都会混在一起。

因此：

> **好的 Tool Contract 不只是方便调用，也让 failure attribution 和 evaluation 成为可能。**

---

#### 3.1.51 Tool Call Trace 应该记录什么？

一个可靠系统至少应能追踪：

```text
Tool Name
Tool Version
Call ID
Arguments
Caller / Agent
Permission Context
Start Time
End Time
Status
Raw Result Reference
Observation
Error Type
Retry Count
Side-effect ID
```

这不是 Tool Definition 本体的一部分，但很多字段都由 Tool Contract 决定。

它为：

```text
debugging
audit
evaluation
replay
recovery
```

提供基础。

---

#### 3.1.52 Tool Call ID 为什么重要？

当系统存在：

```text
parallel calls
retry
async jobs
streaming results
```

必须知道：

```text
哪个 result 对应哪个 call
```

因此常见结构：

```text
call_id = abc123
```

结果返回：

```text
in_reply_to = abc123
```

否则多个并发 Tool Result 很容易错位进入 Context。

---

#### 3.1.53 Tool Result 需要 Provenance

例如搜索结果：

```text
某公司营收 100 亿
```

Agent 后面需要知道：

```text
来自哪个 source？
什么时候获取？
是否直接抓取？
是否是缓存？
```

因此 Observation Contract 最好保留：

```text
source
retrieved_at
resource_id
version
```

这对：

```text
Verification
Citation
Audit
Freshness
```

非常重要。

---

#### 3.1.54 Tool Output 可能是不可信输入

Tool 来自外部环境。

例如：

```text
网页内容
邮件正文
第三方 API 返回
用户文件
```

这些数据可能包含：

```text
恶意指令
prompt injection
错误信息
伪造结果
```

所以：

> **Tool 是受控 Action Boundary，不代表 Tool Observation 是可信指令来源。**

系统必须继续保持：

```text
Instruction
vs
Data
```

的边界。

---

#### 3.1.55 Tool Design 和 Prompt Injection Surface

Tool 越能读取外部内容：

```text
browser
email
web
files
```

越容易把 untrusted content 带回 Context。

Tool 越能执行高权限动作：

```text
shell
email
cloud admin
```

prompt injection 的后果越严重。

所以真正风险不是：

```text
模型看到了恶意文本
```

而是：

```text
恶意文本
→ 影响 Policy
→ 高权限 Tool
→ 真实 side effect
```

这就是 Tool Capability 与 Permission 设计必须联动的原因。

---

#### 3.1.56 Tool Definition 的 Failure Modes

Tool Definition 层最常见的失败包括：

**1. Ambiguous Name**

```text
process
handle
manage
```

无法表达具体能力。

**2. Vague Description**

多个 Tool 都写：

```text
Get information.
```

导致模型难以选择。

**3. Overloaded Tool**

一个 Tool 同时做太多语义完全不同的操作。

**4. Missing Side-effect Semantics**

模型 / Harness 不知道调用会不会改环境。

**5. Missing Error Contract**

所有失败都变成 generic error。

**6. Missing Observation Structure**

返回无法可靠解析的大段自由文本。

**7. Overly General Tool**

暴露远超任务需要的权限和 action space。

**8. Backend-shaped Interface**

直接把内部 API endpoint 机械暴露给模型。

**9. Tool Redundancy**

多个语义高度重叠的 Tool 造成选择混乱。

**10. Capability Gap**

任务所需操作根本没有对应 Tool。

**11. Schema / Behavior Drift**

接口字段没变，但实际行为改变。

**12. Version Drift**

模型、trajectory 和 runtime 使用不同版本 Tool。

**13. Permission Metadata Missing**

Capability 与 Authority 被混在一起。

**14. Retry Semantics Missing**

对非幂等 Tool 自动重试。

**15. Partial-success Hidden**

Tool 内部只完成一部分却返回 success。

**16. Stale Availability**

Catalog 说可用，但 backend 已失效。

**17. Untrusted Observation Treated as Instruction**

Tool Result 中的外部文本直接改变高层规则。

**18. No Provenance**

后续无法判断结果来源和 freshness。

---

#### 3.1.57 Tool Definition 的工程原则

可以压缩成以下原则。

**原则 1：Tool 是 contract，不只是 callable。**

必须考虑输入、语义、side effect、permission、observation。

**原则 2：对 Agent 暴露业务意义，不要机械暴露后端结构。**

Tool boundary 应该服务于决策。

**原则 3：Action Space 越小越容易控制。**

不需要任意 shell，就不要给任意 shell。

**原则 4：Read 和 Write 要显式区分。**

高风险 write 应加强 approval / verification。

**原则 5：Error 是 Observation。**

错误类型必须足够结构化，支持 recovery。

**原则 6：Tool Result 要支持 Verification。**

状态、provenance、freshness 和 outcome 需要可追踪。

**原则 7：Tool Definition 需要版本化。**

它是 Agent 行为和实验条件的一部分。

**原则 8：Available ≠ Authorized ≠ Executable。**

能力存在不等于当前有权调用。

**原则 9：暴露 Tool Set 也是 Context Engineering。**

不要无脑把所有 Tool 塞给模型。

**原则 10：Tool 内部可以 deterministic，外部由 Agent 决定何时调用。**

这通常比让模型控制每个低层步骤更可靠。

---

#### 3.1.58 一个 Coding Agent 的 Tool Set 例子

假设任务：

```text
修复 repository bug 并验证
```

可能暴露：

```text
search_repo(query)
read_file(path, range)
edit_file(path, patch)
run_tests(target)
git_diff()
```

而不直接暴露：

```text
arbitrary_root_shell
```

每个 Tool 有清晰语义：

```text
search_repo
→ read-only

read_file
→ read-only

edit_file
→ workspace write

run_tests
→ sandbox compute

git_diff
→ read-only verification support
```

这时 Agent 的 action space 已经能够覆盖：

```text
Inspect
→ Diagnose
→ Edit
→ Verify
```

同时避免把系统权限无限打开。

---

#### 3.1.59 一个 Research Agent 的 Tool Set 例子

任务：

```text
研究最新论文并写综述
```

Tool Set 可能是：

```text
search_web
search_papers
open_document
extract_metadata
save_note
```

不同 Tool 的 contract 应该区分：

```text
public web
vs
academic corpus
vs
local document
```

否则 Agent 很难建立 source strategy。

另外 Search Tool 的 Observation 最好保留：

```text
URL
Title
Published Date
Source
Snippet
```

这样后续 Verification 和 citation 才有依据。

---

#### 3.1.60 Tool Design 和 Agent Reliability 的关系

很多“模型犯错”其实来自：

```text
Tool interface 设计差
```

例如：

```text
模型选错 Tool
```

可能是因为：

```text
两个 Tool description 语义重叠
```

模型参数填错，可能是因为：

```text
schema 字段命名反直觉
```

Agent 重复产生 side effect，可能是因为：

```text
Tool 没有 idempotency contract
```

所以：

> **Agent Reliability 不只由模型能力决定，Tool Contract 本身也是系统能力的一部分。**

这与前面：

```text
Agent Capability = f(Model, Harness, Tools, Environment, Feedback)
```

完全一致。

---

#### 3.1.61 Tool Design 和 Agent Eval 的关系

评价 Tool Use 时至少应拆成：

```text
Was the needed capability available?
Was the right tool exposed?
Was the right tool selected?
Were arguments correct?
Did execution match contract?
Was the observation correct?
Did the Agent use the result correctly?
Was the side effect appropriate?
```

否则一句：

```text
Tool use failed
```

无法定位故障层。

因此 Tool Definition 是后续：

```text
Tool Eval
Process Eval
Failure Attribution
```

的基础。

---

#### 3.1.62 Tool Definition 的最小面试回答

如果面试官问：

> 什么是 Agent Tool？

一个合格回答可以是：

> **Tool 是 Agent 可以选择调用、由 Runtime 实际执行的外部能力接口。它不只是函数名和 JSON 参数，还应该有清晰的能力语义、输入契约、side-effect 语义、权限边界以及输出 / error observation contract。模型通过 Tool Calling 产生具体 action request，Harness 做策略与权限控制，Runtime 执行，结果再作为 Observation 返回 Agent。**

如果继续追问，可以补：

```text
Tool ≠ Function
Tool ≠ API
Tool ≠ Capability
Tool ≠ Action instance
```

以及：

```text
Tool = Capability Contract
Tool Call = Action Instance
```

---

#### 3.1.63 高频追问与回答边界

1. **Tool 和 Function 有什么区别？**  
   Function 是程序实现形式；Tool 是暴露给 Agent 的 capability contract。一个 Tool 可以封装 function、API、workflow，甚至 subagent。

2. **Tool 和 API 有什么区别？**  
   API 是系统接口；Tool 是 Agent-facing action abstraction。Tool 可以调用 API，也可以本地执行。

3. **Tool 和 Action 有什么区别？**  
   Tool 是动作类型；Action / Tool Call 是某一次具体调用实例。

4. **Tool Definition 最少包含什么？**  
   常见最小形式是 name + description + input schema；可靠系统还应明确 execution semantics、side effects、permissions 和 observation / error contract。

5. **为什么 Tool Description 很重要？**  
   因为它直接进入模型决策上下文，影响 Tool Selection 和参数生成。

6. **为什么 schema-valid 不代表 tool call 正确？**  
   Schema 只保证结构合法，不保证选择正确、语义正确、被授权或安全。

7. **为什么 Side Effect 要放进 Tool Contract？**  
   因为它决定 approval、retry、idempotency、recovery 和 verification policy。

8. **Tool 可用就能执行吗？**  
   不能。Defined / Visible / Authorized / Available / Executable 是不同状态。

9. **为什么 error 要结构化？**  
   不同 error 应触发不同 recovery；generic error 会丢失决策信息。

10. **Tool Output 和 Observation 区别？**  
    Tool Output 是原始执行结果；Observation 是经过 normalization / filtering 后真正进入 Agent State / Context 的反馈。

11. **Tool 越多越好吗？**  
    不一定。过多或冗余 Tool 会增加 context cost 和 selection ambiguity，应通过 filtering / discovery 动态暴露。

12. **为什么不直接给 Agent shell？**  
    通用 Tool 灵活但权限面和验证难度大。能用更窄的 domain tool 表达任务时，通常更可靠、更安全。

13. **高层 Tool 会不会太不 Agentic？**  
    不会。Agenticness 取决于哪些决策在 runtime 动态完成；高层 deterministic Tool 可以减少不必要的低层自由度。

14. **Tool 和 Workflow 什么关系？**  
    一个 Tool 内部完全可以封装 deterministic workflow；Agent 只看到外层 capability contract。

15. **Tool 和 MCP 什么关系？**  
    Tool 是能力接口；MCP 是标准化暴露、发现和调用这些能力的一种协议机制。

16. **Tool Definition 最核心的一句话？**  
    Tool 不是“一个模型能调用的函数名”，而是 Agent action space 中一个有明确输入、语义、副作用、权限和 observation 契约的可执行 capability boundary。

---

#### 3.1.64 本节一句话总结

> **Tool 的本质，是把外部 Capability 压缩成 Agent 可以理解和选择的 Action Contract：它不仅定义 name 与 arguments，还必须明确执行语义、side effects、权限边界、错误语义和 Observation contract；Function Calling 只是产生具体 Tool Call 的机制，Harness 决定何时与是否允许使用，Runtime 真正执行，而 Tool Contract 的质量直接决定 Agent 的可控性、可验证性与可靠性。**

#### 3.1.65 参考资料

- Yao S, Zhao J, Yu D, et al. **ReAct: Synergizing Reasoning and Acting in Language Models**. ICLR 2023. 通过 reasoning 与 environment actions / observations 的交错，为现代 LLM Agent 的 Tool-use loop 奠定了重要范式。
- Schick T, Dwivedi-Yu J, Dessì R, et al. **Toolformer: Language Models Can Teach Themselves to Use Tools**. NeurIPS 2023. 代表性展示语言模型如何学习何时调用外部工具、传递参数并利用工具结果。
- Qin Y, Liang S, Ye Y, et al. **ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs**. ICLR 2024. 从大规模 API / Tool use 数据与评测角度展示 Tool ecosystem、selection 与 execution 的复杂性。
- Patil S G, Zhang T, Wang X, Gonzalez J E. **Gorilla: Large Language Model Connected with Massive APIs**. arXiv:2305.15334, 2023. 讨论 LLM 与大规模 API / tool interfaces 的连接与调用问题。

