#### 6.7.21 Agent Interface：能力与传输方式之间的连接契约

在稳定的 A2A 语义中，Agent Card 不只是给一个 URL，而可以声明一个或多个 **Agent Interface**。

Interface 解决的是：

```text
同一个 Agent capability
可以通过什么 endpoint
使用什么 protocol binding
按照什么 protocol version
被访问？
```

因此应区分：

```text
Agent Identity
Agent Capability
Agent Interface
Transport / Binding
```

同一个 Agent 可以暴露多个 interface，而不是“一个 Agent = 一个 URL”。

---

#### 6.7.22 Protocol Binding ≠ Agent Semantics

A2A v1.x 将核心语义与具体 binding 更明确地分开。

当前标准体系支持多种 binding，例如：

```text
JSON-RPC
gRPC
HTTP+JSON / REST
```

重要的不是背这些名字，而是理解：

> **Transport / binding 可以变化，但 Task、Message、Artifact 等互操作语义应保持一致。**

因此不要把 A2A 理解成：

```text
A2A = JSON-RPC
```

更准确的是：

```text
A2A semantic model
      ↓
one or more protocol bindings
      ↓
network transport
```

---

#### 6.7.23 Interface Negotiation：不是“能连上就行”

调用方发现 Agent Card 后，需要判断：

```text
我支持它哪个 interface？
版本是否兼容？
认证方式是否可满足？
输入输出模式是否匹配？
required extension 是否支持？
```

因此连接前至少存在一层：

```text
Discovery
   ↓
Compatibility Negotiation
   ↓
Connection / Invocation
```

典型 failure 是：

```text
Agent 能做这个任务
但双方没有共同支持的 protocol binding
```

这属于 interoperability failure，不是 reasoning failure。

---

#### 6.7.24 Version Compatibility 为什么必须显式处理

跨 Agent 系统往往独立升级。

因此版本关系可能变成：

```text
Client: A2A 1.0
Server: A2A 1.1
```

或者：

```text
Client understands extension X v1
Server requires extension X v2
```

如果系统默认：

```text
"都是 A2A，所以一定兼容"
```

就会把 protocol family 与具体 compatibility 混在一起。

工程上应把：

- protocol version；
- binding；
- required extension；
- optional extension；
- input/output mode；

纳入连接决策。

---

#### 6.7.25 Extension：扩展协议，而不是偷偷建立私有协议

A2A 允许 Agent 声明 extension，用于表达 core protocol 之外的附加语义。

Extension 的价值在于：

```text
Core remains interoperable
        +
Domain-specific semantics can evolve
```

但 extension 也会带来风险：

```text
extension proliferation
→ compatibility fragmentation
→ nominally A2A-compatible but practically incompatible
```

所以应区分：

```text
core-required semantics
optional extension
required extension
vendor-private behavior
```

> **扩展越多，协议名义上的统一并不一定等于真实互操作性更强。**

---

#### 6.7.26 Message：一次交互内容，不等于一个 Task

**Message** 表示 client 与 remote agent 之间的一次通信 turn。

它可以承载：

- instruction；
- context；
- question；
- answer；
- additional input；
- status-related information。

但 Message 本身不等于 Task。

例如：

```text
Client → Remote Agent:
"请分析这个合同。"
```

Remote Agent 可能：

```text
立即返回 Message
```

也可能：

```text
创建一个 Task 并异步处理
```

因此：

> **Message 是 communication unit；Task 是 stateful work unit。**

---

#### 6.7.27 Part：A2A 的内容载体

Message 与 Artifact 都不是只装纯文本。

**Part** 是更细粒度的内容容器，可用于表达：

```text
text
structured data
file reference
inline binary content
```

因此 A2A 的内容模型是 modality-independent 的。

这意味着一个任务可以自然承载：

```text
instruction text
+
PDF file
+
JSON parameters
+
image
```

而不需要把所有内容强行塞进一个字符串 prompt。

---

#### 6.7.28 Structured Data 为什么比“全塞自然语言”更可靠

假设 Agent A 要把订单信息交给 Agent B。

弱设计：

```text
"客户张三买了两件 A，地址是……请帮我处理"
```

更稳定的设计：

```text
Message
 ├── TextPart: instruction
 └── DataPart:
       order_id
       customer_id
       items
       address
       constraints
```

Structured Part 可以降低：

- parsing ambiguity；
- schema drift；
- accidental omission；
- prompt-style dependency。

所以：

> **跨 Agent 协作中，能结构化表达的 contract data 不应依赖自然语言猜测。**

---

#### 6.7.29 Artifact：任务产物，不只是聊天回复

**Artifact** 是 remote agent 在 Task 中产生的正式输出或可消费结果。

例如：

```text
report.pdf
analysis.json
patch.diff
image.png
execution_plan.yaml
```

这与普通 Message 的区别在于：

```text
Message 主要用于交互
Artifact 主要用于交付
```

因此：

> **Message ≠ Artifact**

一个 Agent 可以发很多 progress message，但真正可供 downstream consumption 的可能只有一个最终 artifact。

---

#### 6.7.30 Artifact ≠ Verified Outcome

Artifact 被成功返回，只说明：

```text
remote agent produced something
```

不说明：

```text
内容正确
格式可用
版本最新
来源可信
满足用户目标
副作用已经正确发生
```

例如 Agent 返回：

```text
"payment_receipt.json"
```

不能只因为它是 artifact 就认定付款成功。

仍然需要：

- schema validation；
- provenance；
- freshness；
- external verification；
- business invariant check。

稳定原则仍然是：

> **Returned Artifact ≠ Ground Truth**

---

#### 6.7.31 Task：A2A 最关键的 stateful work abstraction

对于不能立即完成的工作，A2A 使用 **Task** 表达一个可跟踪的工作单元。

Task 通常具有：

```text
unique task ID
context association
current status
optional history
artifacts
metadata
```

因此 Task 不是一句 prompt，也不是一次 HTTP request。

它更接近：

> **跨 Agent 边界可被持续观察和管理的远程工作实例。**

---

#### 6.7.32 Task ID 为什么重要

如果没有稳定 task identity：

```text
request timeout
   ↓
client 不知道 server 是否已创建任务
   ↓
client retry
   ↓
server 创建第二个任务
   ↓
duplicate work / duplicate side effect
```

Task ID 让系统能够：

- 查询状态；
- 关联更新；
- resubscribe；
- cancel；
- deduplicate；
- trace；
- audit。

但要注意：

> **有 Task ID 不等于自动获得 exactly-once semantics。**

仍需要调用方与服务端共同设计幂等和重复提交策略。

---

#### 6.7.33 Task State Machine：为什么比一个 success 字段更重要

远程 Agent 的任务不是只有：

```text
success / failure
```

而可能处于：

```text
submitted
working
input-required
auth-required
completed
failed
canceled
rejected
unknown
```

这说明远程执行本质上具有：

- progress；
- pause；
- interruption；
- terminal state；
- uncertainty。

所以一个生产系统不应只有：

```text
if response.ok:
    done
```

而应显式建模 task lifecycle。

---

#### 6.7.34 submitted ≠ working

`submitted` 表示任务已被接收 / 建立，但不代表已经真正开始执行。

因此：

```text
Task accepted
   ≠
Execution started
```

这对：

- queue delay；
- capacity planning；
- timeout；
- SLA；

都很重要。

如果系统只统计“提交成功率”，会掩盖大量排队和执行启动失败。

---

#### 6.7.35 working ≠ making progress

Task 状态为 `working`，并不自动意味着它在有效推进。

可能出现：

```text
working
  ↓
waiting on hidden dependency
  ↓
working
  ↓
loop
  ↓
working
```

所以要区分：

```text
State = WORKING
          ≠
Progress > 0
```

这与 6.6 的 no-progress / liveness failure 是同一个系统问题在 A2A 边界上的表现。

---

#### 6.7.36 input-required：远程 Agent 需要额外信息

当 remote agent 无法继续时，可以进入需要额外输入的中断状态。

例如：

```text
Travel Agent:
"需要确认护照国家和出发日期。"
```

此时不应该把任务判成 failure。

正确语义是：

```text
RUNNING
  ↓
INPUT_REQUIRED
  ↓ user/client provides input
WORKING
```

因此：

> **Needs More Input ≠ Failed**

---

#### 6.7.37 auth-required：执行中也可能出现新的认证需求

Remote Agent 可能开始处理后发现：

```text
下一步访问受保护资源需要新的 credential / user consent
```

因此 `auth-required` 与普通业务输入不同。

它提醒系统：

```text
Authentication / Authorization
不是只发生在连接建立前的一次性检查。
```

Agentic workflows 中 credential scope、consent、step-up auth 都可能随任务推进而变化。

---

#### 6.7.38 completed ≠ End-to-End Success

A2A Task 进入 `completed`，表示 remote agent 认为该 Task 已成功结束。

但上游仍必须判断：

```text
artifact valid?
user goal satisfied?
side effect observed?
constraints preserved?
result fresh?
provenance acceptable?
```

因此：

> **Remote Completed ≠ Local Acceptance ≠ User Goal Success**

一个可靠 Harness 应有独立 acceptance / verification 阶段。

---

#### 6.7.39 failed、rejected、canceled 必须区分

这些状态都意味着当前任务没有完成，但原因不同：

```text
failed
= 执行中发生错误

rejected
= remote agent 决定不接受 / 不继续该任务

canceled
= 任务被取消
```

这会直接影响后续策略：

```text
failed   → maybe retry / fallback / diagnose
rejected → reroute / policy review
canceled → stop / compensate / confirm side effects
```

如果统一映射成：

```text
ERROR
```

就丢失了恢复决策所需的信息。

---

#### 6.7.40 unknown：不确定不是失败

在分布式系统里最危险的误判之一是：

```text
timeout → failed
```

实际上可能是：

```text
request sent
server processed
side effect committed
response lost
```

此时本地真实状态应更接近：

```text
UNKNOWN
```

因此仍然遵守前面反复强调的原则：

> **Unknown ≠ False**
>
> **Unknown ≠ Failed**

正确恢复通常是：

```text
reconcile first
then decide retry
```

而不是盲目重复提交。

---

#### 6.7.41 Terminal State ≠ Safe to Forget

Task 到 terminal state 后，系统仍可能需要保留：

- artifact provenance；
- status history；
- audit trail；
- verification result；
- side-effect evidence；
- retry lineage；
- cost；
- security decisions。

因此：

```text
Task terminal
   ≠
Operational state can be discarded immediately
```

这和 Chapter 4 的 persistence / durable state 直接相关。

---

#### 6.7.42 Context ID：关联交互，不等于完整共享上下文

A2A 中可以用 context identifier 将相关 Message / Task 逻辑分组。

但这不意味着两个 Agent 自动共享：

- full conversation history；
- private memory；
- internal state；
- hidden reasoning；
- tool outputs；
- organization-wide knowledge。

所以：

> **Context ID 是 correlation mechanism，不是 shared-memory magic。**

它解决：

```text
哪些交互属于同一个连续语境？
```

而不是：

```text
双方内部状态是否完全一致？
```

---
