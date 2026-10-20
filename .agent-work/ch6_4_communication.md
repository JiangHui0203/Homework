### 6.4 Communication

#### 6.4.1 Communication 到底是什么

在 Multi-Agent 系统中，**Communication** 不是“多个 Agent 互相发几句话”。

更准确地说：

> **Communication 是一个 Agent 将决策相关的信息、请求、状态、证据或控制意图，以可解释、可追踪、可约束的形式传递给另一个 Agent，并让接收方能够据此安全地更新自己的局部状态或采取下一步行动。**

一个最小通信链路可以写成：

```text
Sender
  ↓
Message Construction
  ↓
Envelope / Contract
  ↓
Transport
  ↓
Receiver Intake
  ↓
Validation / Interpretation
  ↓
Local State Update / Action
  ↓
Ack / Result / Follow-up
```

真正困难的不是“把字符串送过去”，而是：

```text
对方收到的是什么？
它如何知道这条消息属于哪个任务？
它是否有权相信 / 执行？
消息是否过期、重复、乱序？
对方理解的语义是否和发送方一致？
结果如何回到正确的因果链？
```

因此，Agent Communication 同时具有：

```text
Transport Semantics
+ Message Semantics
+ Task / Coordination Semantics
+ Authority / Trust Semantics
```

---

#### 6.4.2 Communication 不是一个单独的 API

同一种通信语义，可以通过很多机制承载：

```text
direct function call
HTTP request
message queue
event bus
stream
websocket
shared mailbox
remote agent protocol
```

所以不能把：

```text
Communication = HTTP
Communication = message queue
Communication = A2A
```

这些等号成立。

Transport 是“怎么送”，Communication 还要回答“送什么、代表什么、收到后怎么办”。

---

#### 6.4.3 Communication 与 Delegation 不一样

Delegation 的核心是：

```text
把一个 bounded goal 交给另一个执行主体
```

Communication 的范围更大。

Agent 之间可以通信而不发生 Delegation，例如：

```text
状态通知
事实同步
请求证据
进度汇报
冲突告警
取消信号
心跳
```

因此：

```text
Delegation ⊂ Communication
```

但不是所有 Communication 都是 Delegation。

---

#### 6.4.4 Communication 与 Handoff 不一样

Handoff 关心的是：

```text
Control Ownership Transfer
```

Communication 只表示信息或控制信号的传递。

例如：

```text
Agent A → Agent B: “请核验这条事实”
```

如果 A 仍是顶层 owner，这只是 communication + bounded delegation。

如果：

```text
A → B: “接下来由你接管这个用户请求”
```

并且 active owner 真的切换，才是 Handoff。

---

#### 6.4.5 Communication 与 Shared State 不一样

这是一个必须严格保持的边界：

```text
Message Passing ≠ Shared State
```

Message Passing 是：

```text
A sends information to B
```

Shared State 是：

```text
A and B depend on a common state object
```

即使所有 Agent 都通过消息同步某个事实，也不意味着它们共享同一个 authoritative state。

下一节 6.5 会专门讨论 Shared / Private Context。

---

#### 6.4.6 Communication 与 Context 也不是一回事

一条 Message 可以进入 Receiver 的 Context，但：

```text
Message ≠ Context
```

Context 是当前模型推理真正看到的完整输入。

Message 只是其中一个潜在组成部分。

因此：

```text
received
≠
included in next context
≠
attended to correctly
≠
used in decision
```

---

#### 6.4.7 Communication 的四层模型

可以把一次 Agent Communication 拆成四层。

**第一层：Transport**

```text
How is it delivered?
```

例如 HTTP、Queue、Stream。

**第二层：Envelope**

```text
Who sent what to whom, for which task, under which version?
```

**第三层：Semantic Payload**

```text
What does the content mean?
```

**第四层：Coordination Effect**

```text
What state transition or action should this communication enable?
```

很多系统只实现了第一层，却把它称作“Agent 通信已经解决”。

---

#### 6.4.8 最重要的一组不等式

Agent Communication 中非常值得长期记住：

```text
Sent
≠ Delivered
≠ Received
≠ Parsed
≠ Understood
≠ Accepted
≠ Started
≠ Completed
≠ Verified
```

因此：

> **“我已经发给另一个 Agent 了”不能作为任务完成证据。**

---

#### 6.4.9 Message Sent ≠ Message Delivered

Sender 成功调用发送接口，只说明：

```text
send request accepted locally
```

不一定说明 Receiver 已经拿到消息。

可能存在：

- 网络失败；
- broker 故障；
- queue backlog；
- downstream unavailable；
- timeout；
- routing error。

所以 Transport Success 必须有明确语义。

---

#### 6.4.10 Message Delivered ≠ Message Processed

消息到达 Receiver 的 mailbox / queue 后，仍可能：

```text
未消费
消费失败
解析失败
权限拒绝
Schema 不兼容
过期丢弃
```

因此 delivery metric 不是 task metric。

---

#### 6.4.11 Message Processed ≠ Semantic Understanding

即使 Receiver 成功解析 JSON，也不代表它理解了发送方真正意图。

例如：

```text
priority = high
```

如果两个 Agent 对 `high` 的业务语义不同，Schema 正确也会产生 Semantic Drift。

这说明 Agent Communication 不只是 serialization problem。

---

#### 6.4.12 Semantic Understanding ≠ Ground Truth

Receiver 理解了 Sender 的意思，Sender 本身仍可能是错的。

因此：

```text
A says X
→ B correctly understands “A says X”
```

不能自动升级成：

```text
X is true
```

必须保留 Provenance 与 Evidence。

---

#### 6.4.13 Message 是 Observation，不是 Ground Truth

从 Receiver 视角看，另一个 Agent 的消息首先应该被当成：

```text
an observation from a source
```

它可能是：

- authoritative；
- inferred；
- stale；
- uncertain；
- adversarial；
- partially correct。

所以应复用前面的原则：

> **Tool Result ≠ Observation ≠ Ground Truth。**

在 Multi-Agent 场景中进一步变成：

> **Agent Message ≠ Ground Truth。**

---

#### 6.4.14 Message 类型应该显式区分

不要让所有通信都变成：

```text
{"text": "..."}
```

至少可以区分：

```text
Request
Command
Query
Event
Result
Progress
Ack
Error
Cancel
Escalation
Heartbeat
```

因为不同类型对应不同状态机和恢复策略。

---

#### 6.4.15 Request

Request 表示：

```text
请你尝试完成某件事
```

它通常需要：

- request_id；
- expected response；
- deadline；
- scope；
- authority；
- acceptance criteria。

Request 不自动意味着 Receiver 一定接受。

---

#### 6.4.16 Command

Command 比 Request 更强：

```text
在已有 authority / workflow 下要求执行某个明确动作
```

但即使是 Command，Receiver 仍应做：

```text
authentication
authorization
policy validation
precondition check
```

不能因为消息类型写着 `command` 就跳过边界检查。

---

#### 6.4.17 Query

Query 主要请求信息：

```text
What do you know about X?
```

它通常不应产生真实 Side Effect。

因此 Query Agent 的权限集可以明显小于 Execution Agent。

---

#### 6.4.18 Event

Event 表示：

```text
something happened
```

例如：

```text
file_changed
payment_confirmed
task_cancelled
new_evidence_available
```

Event 与 Command 的区别在于：

```text
Event 描述事实 / 状态变化
Command 请求动作
```

不要把所有 Event 都解释成必须执行的指令。

---

#### 6.4.19 Result

Result 表示某个已知 Request / Task 的输出。

它应该能回答：

```text
Result of what?
Produced by whom?
Based on which state / version?
Final or partial?
Verified or self-reported?
```

没有关联信息的 Result 很容易被错误消费。

---

#### 6.4.20 Progress

Progress 是中间状态：

```text
still working
current stage
partial findings
budget consumed
blockers
```

它的语义必须明确：

```text
Progress ≠ Final Result
```

否则 Parent 可能把流式中间结论误当成最终结论。

---

#### 6.4.21 Ack

Ack 最容易被过度解释。

至少要区分：

```text
received
accepted
started
completed
```

因此一个成熟系统不应该只有：

```text
ack = true
```

而应知道 Ack 的具体层级。

---

#### 6.4.22 Error

Error 不只是自由文本：

```text
“出了点问题”
```

更好的结构包括：

```text
error_type
error_code
retryable
failed_stage
side_effect_state
evidence
recommended_next_action
```

这样上游才能做正确 Recovery。

---

#### 6.4.23 Cancel

Cancel 是控制消息，不等于任务已经停止。

需要区分：

```text
cancellation_requested
cancellation_acknowledged
cancelled
```

因为可能存在：

- 已在执行的 API；
- 已提交的 Side Effect；
- 不可中断阶段；
- 延迟到达的 Cancel。

---

#### 6.4.24 Escalation

Escalation 表示：

```text
当前 Agent 不应继续独立处理
```

可能原因：

- 权限不足；
- 输入缺失；
- 高风险；
- 目标冲突；
- 预算不足；
- 需要 Human / Parent。

Escalation 是一种有价值的 Communication outcome，而不是默认失败。

---

#### 6.4.25 Heartbeat

长任务里，Heartbeat 可以说明：

```text
worker alive
lease still valid
task still owned
```

但：

```text
Heartbeat ≠ Progress
```

Agent 还活着，不代表任务有实质推进。

---

#### 6.4.26 一个成熟的 Message Envelope

可以抽象成：

```text
Message Envelope =
    message_id
  + message_type
  + sender
  + recipient
  + task_id
  + conversation_id
  + delegation_id
  + correlation_id
  + causation_id
  + schema_version
  + created_at
  + expires_at
  + priority
  + authority_context
  + provenance
  + payload
  + expected_response
```

不一定每条消息都需要全部字段，但这些是常见设计维度。

---

#### 6.4.27 message_id

每条消息应有稳定身份：

```text
message_id
```

主要用于：

- deduplication；
- trace；
- retry；
- audit；
- causality reconstruction。

“内容一样”不能替代 Message Identity。

---

#### 6.4.28 task_id

`task_id` 回答：

```text
这条消息属于哪个工作单元？
```

没有 Task Correlation 时，并发执行很容易串线。

特别是同一个 Agent 同时服务多个任务时：

```text
sender identity
```

不足以定位上下文。

---

#### 6.4.29 conversation_id / context_id

一个长期交互可能包含多个 Task。

因此有时需要更高层的：

```text
conversation_id
context_id
session_id
```

它们与 `task_id` 不应该混成一个字段。

---

#### 6.4.30 delegation_id

如果消息来自一次明确 Delegation，应能关联：

```text
delegation_id
```

这样才能回答：

```text
这条 Result 是否属于那次委派？
```

尤其 Parent 重试或重新委派同一 Goal 时非常重要。

---

#### 6.4.31 correlation_id

Request / Response 常用：

```text
correlation_id
```

用于把：

```text
response
```

关联回：

```text
request
```

这是并发 Multi-Agent 系统最基础的 bookkeeping 之一。

---

#### 6.4.32 causation_id

`causation_id` 回答：

```text
是什么直接触发了这条消息？
```

例如：

```text
Message A
→ causes Message B
→ causes Tool Call C
→ causes Event D
```

这样可以重建因果链，而不只是时间顺序。

---

#### 6.4.33 Timestamp 不等于 Causality

两个消息时间分别是：

```text
10:00:01
10:00:02
```

不代表第二条一定由第一条导致。

分布式系统里：

```text
wall-clock order ≠ causal order
```

因此 Trace 需要显式 Parent / Causation relation。

---

#### 6.4.34 created_at 与 expires_at

很多消息具有时效性。

例如：

```text
“库存还有 3 件”
“当前 branch head = abc123”
“用户刚刚批准了操作”
```

如果消息两小时后才被消费，可能已经无效。

所以：

```text
Freshness should be encoded, not guessed.
```

---

#### 6.4.35 Priority

不同消息优先级不同。

例如：

```text
progress update
```

通常应低于：

```text
cancel
security block
authority revoked
```

否则 backlog 中可能出现：

```text
Agent 先继续执行旧工作
很久以后才看到取消消息
```

---

#### 6.4.36 Payload 与 Metadata 必须分开

Payload 是业务内容：

```text
finding
artifact
request parameters
```

Metadata 是解释消息如何被处理的信息：

```text
source
timestamp
version
correlation
authority
```

把两者混在自然语言里，会增加解析和审计难度。

---

#### 6.4.37 Natural Language Payload 的价值

自然语言适合：

- 高语义复杂度；
- 开放式任务；
- 无法预先穷举的 reasoning；
- 人类可读解释。

因此 Agent Communication 不可能完全消灭自然语言。

---

#### 6.4.38 Natural Language Payload 的风险

自由文本容易出现：

- ambiguity；
- omitted constraints；
- contradictory statements；
- implicit authority；
- prompt injection；
- schema drift；
- 难以自动验证。

所以高风险控制信息不应只靠自然语言表达。

---

#### 6.4.39 Structured Message 的价值

结构化消息适合：

```text
status
ids
versions
amount
permissions
task transitions
artifact references
```

优点是：

- machine validation；
- stable contract；
- easier observability；
- lower interpretation ambiguity。

---

#### 6.4.40 Structured ≠ Semantically Correct

即使：

```json
{"status": "completed"}
```

Schema 完全合法，也可能是假的。

因此：

```text
schema_valid
≠ semantically_valid
≠ externally_verified
```

结构化解决的是表达稳定性，不是事实真实性。

---

#### 6.4.41 Hybrid Communication

现实中常见最稳健形式是：

```text
Structured Envelope
+ Structured Critical Fields
+ Natural-language Explanation
+ Evidence / Artifact References
```

即：

```text
机器可验证骨架
+
模型可表达语义
```

---

#### 6.4.42 Schema Versioning

Multi-Agent 系统会演进。

如果 Sender 使用：

```text
schema v3
```

Receiver 只理解：

```text
schema v1
```

就可能发生 silent misinterpretation。

因此需要：

- schema version；
- compatibility policy；
- unknown-field handling；
- migration strategy。

---

#### 6.4.43 Forward / Backward Compatibility

设计消息 Schema 时要问：

```text
旧 Receiver 能否忽略新字段？
新 Receiver 能否处理旧字段缺失？
```

不要让一个非关键字段升级导致整个 Agent network 停摆。

---

#### 6.4.44 Unknown Field 不应该自动解释

当 Receiver 看见未知字段：

```text
override_policy = ...
```

不能让 LLM 自己“猜这大概什么意思”。

对于关键控制字段，更稳健的是：

```text
reject / ignore under explicit rule / escalate
```

---

#### 6.4.45 Synchronous Request–Response

最简单模式：

```text
A → request → B
A waits
B → response → A
```

优点：

- 易理解；
- 因果关系清楚；
- 错误直接返回。

缺点：

- blocking；
- critical-path latency；
- 不适合长任务。

---

#### 6.4.46 Asynchronous Messaging

异步模式：

```text
A → enqueue
A continues
B consumes later
B → result event
```

适合：

- long-running task；
- high fan-out；
- disconnected execution；
- background work。

但会引入更多状态治理问题。

---

#### 6.4.47 Async 的核心代价：Outcome Uncertainty

异步之后，A 不能再假设：

```text
send succeeded
→ work succeeded
```

而必须显式维护：

```text
pending
accepted
running
partial
completed
failed
cancelled
unknown
```

这与前面长期原则一致：

> **Unknown ≠ False，Pending ≠ Failed。**

---

#### 6.4.48 Streaming

Streaming 可以传递：

```text
token chunks
status updates
partial artifacts
progress events
```

它适合降低 perceived latency，但增加了：

- partial-state semantics；
- ordering；
- replay；
- finality；
- cancellation。

---

#### 6.4.49 Streaming 中必须定义 Finality

Receiver 必须知道：

```text
这只是 chunk
还是完整 artifact？
这是 tentative
还是 authoritative final？
```

否则中间结果可能提前触发下游 Side Effect。

---

#### 6.4.50 Publish–Subscribe

Pub/Sub 适合：

```text
one event
→ many interested consumers
```

例如：

```text
new_incident
→ triage agent
→ notification agent
→ audit agent
```

但广播会放大：

- duplicate work；
- cost；
- privacy exposure；
- inconsistent reactions。

---

#### 6.4.51 Queue

Queue 适合把：

```text
producer rate
```

与：

```text
consumer rate
```

解耦。

但 Queue 不会自动解决：

- task ownership；
- duplicate delivery；
- ordering；
- idempotency；
- stale work。

---

#### 6.4.52 Direct Peer-to-Peer

Peer-to-Peer：

```text
Agent A ↔ Agent B
```

优点：

- 路径短；
- autonomy 高。

缺点：

- topology 快速复杂化；
- 权限关系难审计；
- routing 分散；
- trace 重建困难。

---

#### 6.4.53 Hub-and-Spoke

中心协调：

```text
        B
        ↑
C ← Orchestrator → D
        ↓
        E
```

优点：

- control ownership 清晰；
- policy 集中；
- trace 简单。

缺点：

- bottleneck；
- single coordination hotspot；
- manager context pressure。

---

#### 6.4.54 Brokered Communication

Broker 模式：

```text
Agent
  ↓
Message Broker / Router
  ↓
Agent
```

Broker 可以负责：

- routing；
- queueing；
- retry；
- fan-out；
- access policy；
- observability。

但 Broker 不应该擅自改变消息的业务语义。

---

#### 6.4.55 Blackboard / Shared Workspace

另一类协作模式不是互相直发，而是：

```text
Agent A ─┐
Agent B ─┼→ Shared Workspace / Blackboard
Agent C ─┘
```

这已经开始跨入 6.5 的 Shared Context / State 问题。

关键区别是：

```text
communication by message
vs
coordination through common state
```

两者不要混淆。

---

#### 6.4.56 Delivery Semantics：At-most-once

At-most-once 的含义接近：

```text
最多处理一次
但可能丢
```

适合：

- 丢一条影响不大；
- 重复比丢失更危险；
- 上层能容忍缺失。

---

#### 6.4.57 Delivery Semantics：At-least-once

At-least-once：

```text
尽量保证送到
但可能重复
```

这意味着 Receiver 必须准备处理 Duplicate。

对于 Agent Side Effect，这一点尤其关键。

---

#### 6.4.58 “Exactly-once” 不应被轻易承诺

端到端系统中：

```text
network
queue
receiver
database
external API
```

跨越多个故障边界。

所谓 exactly-once 往往依赖：

- transaction；
- idempotency；
- deduplication；
- state machine；
- atomic commit。

因此更稳健的工程思想是：

> **不要假设消息只会来一次；设计效果可被安全去重。**

---

#### 6.4.59 Duplicate Message

重复来源可能是：

- retry；
- broker redelivery；
- timeout 后重发；
- producer crash recovery；
- network ambiguity。

Receiver 不应该通过：

```text
“文本看起来一样”
```

判断是否重复。

应使用稳定 operation / message identity。

---

#### 6.4.60 Idempotency Key

对于可能重复的 Side Effect，可以绑定：

```text
idempotency_key
```

例如：

```text
create-ticket:task-123
```

重复请求使用同一 key，Runtime / downstream service 才能抑制重复效果。

---

#### 6.4.61 Message Idempotency 与 Effect Idempotency 不一样

消息只处理一次，不代表环境效果只发生一次。

反过来，消息可能被重复处理，但如果 Side Effect 有稳定 idempotency key，最终效果仍可保持一次。

所以更重要的是：

```text
effect-level idempotency
```

---

#### 6.4.62 Lost Ack

一个经典问题：

```text
B 已成功执行
→ Ack 在网络中丢失
→ A timeout
→ A retry
```

如果 A 把 timeout 解释成：

```text
B failed
```

就可能重复 Side Effect。

因此再次强调：

> **Timeout ≠ Failure。**

---

#### 6.4.63 Out-of-order Message

异步环境可能出现：

```text
update v2
先到
update v1
后到
```

如果 Receiver 只按到达顺序覆盖：

```text
latest arrival wins
```

就可能回退到旧状态。

---

#### 6.4.64 Version / Sequence

对有序更新可带：

```text
sequence_number
state_version
event_version
```

Receiver 再决定：

```text
accept
ignore stale
buffer
request resync
```

而不是让 LLM根据文本猜先后。

---

#### 6.4.65 Stale Message

消息在发送时正确，也可能在消费时过期。

例如：

```text
branch_head = abc
```

发送后 repository 已到：

```text
branch_head = def
```

因此关键行动前应：

```text
re-read authoritative state
```

而不是盲信通信快照。

---

#### 6.4.66 Superseded Message

有些新消息明确替代旧消息：

```text
plan_v3 supersedes plan_v2
```

应该显式表达 supersession relation。

否则多个 Agent 可能同时执行不同版本计划。

---

#### 6.4.67 Retry Policy

Retry 前至少问：

```text
failure 是 transport transient 吗？
上一次可能已经有 Side Effect 吗？
operation 是 idempotent 吗？
state 是否已经变化？
deadline 是否还有效？
```

Retry 不是简单的：

```text
for i in range(3)
```

---

#### 6.4.68 Backoff

大量 Agent 同时 Retry 会形成：

```text
retry storm
```

因此需要：

- exponential backoff；
- jitter；
- rate limit；
- retry budget。

Multi-Agent fan-out 会放大这个问题。

---

#### 6.4.69 Timeout

Timeout 应被理解为：

```text
在指定时间内没有获得预期证据
```

而不是：

```text
任务一定失败
```

需要进入：

```text
UNKNOWN / TIMED_OUT / CHECK_REQUIRED
```

等显式状态。

---

#### 6.4.70 Late Response

A timeout 后可能已经：

```text
重新委派给 C
```

此时 B 的旧结果又返回。

系统要定义：

```text
accept?
ignore?
compare?
use as secondary evidence?
```

否则 Late Result 会污染新状态。

---

#### 6.4.71 Cancellation Race

可能发生：

```text
A sends cancel
B completes task
cancel arrives later
```

这不是简单 bug，而是分布式并发竞态。

因此 Task 状态机必须定义合法 transition。

---

#### 6.4.72 Backpressure

如果 Receiver 处理速度跟不上发送速度：

```text
queue grows
latency grows
freshness falls
```

最终即使消息没有丢，也可能因为过期而失去价值。

所以 Communication Capacity 也是系统资源。

---

#### 6.4.73 Communication Budget

通信成本包括：

```text
tokens
serialization
network
queueing
model inference
context consumption
verification
latency
```

因此“让 Agent 多交流”不是免费优化。

---

#### 6.4.74 More Communication Is Not Always Better

过度通信会带来：

- Context Pollution；
- coordination overhead；
- duplicated facts；
- stale information；
- privacy exposure；
- groupthink；
- token cost；
- critical-path latency。

所以多 Agent 系统不是消息越密集越聪明。

---

#### 6.4.75 Minimal Sufficient Communication

可以定义一个原则：

> **只传递 Receiver 完成当前决策所需的最少充分信息，并保留必要的身份、来源、时效、权限与关联元数据。**

重点不是“消息越短越好”，而是：

```text
Sufficient for correct decision
+
Minimal for cost / privacy / isolation
```

---

#### 6.4.76 Communication Utility

可以粗略写成：

```text
Communication Utility
≈
Decision Quality Gain
+ Coordination Gain
+ Verification Gain
-
Token Cost
-
Latency Cost
-
Interpretation Risk
-
Security / Privacy Cost
```

这不是严格公式，但适合作为设计直觉。

---

#### 6.4.77 Decision-Relevant Information

最值得传的不是“所有我知道的东西”，而是：

```text
What changes the Receiver's next decision?
```

例如 Research Agent 返回：

```text
50 页完整浏览历史
```

往往不如：

```text
关键结论
+ evidence
+ source
+ unresolved uncertainty
```

更有用。

---

#### 6.4.78 Summary 不应丢失关键约束

压缩通信时最危险的是把：

```text
constraint
exception
uncertainty
authority boundary
```

一起压掉。

因此 Summarization 也需要 Contract：

```text
what must be preserved
```

---

#### 6.4.79 Context Dump 是通信反模式

把 Parent 全部 Transcript 直接发送给另一个 Agent，看似“信息最全”，实际会导致：

- 目标不清；
- 隐私扩散；
- 旧信息污染；
- token 浪费；
- 指令优先级混乱。

应优先构造 task-specific communication package。

---

#### 6.4.80 Instruction 与 Data 必须分层

跨 Agent 通信中尤其要区分：

```text
Instruction
Data
Quoted external content
Agent inference
Evidence
```

否则：

```text
网页里的恶意文本
```

可能经 Research Agent 转发后，被下游误当成：

```text
trusted instruction
```

---

#### 6.4.81 Prompt Injection Propagation

典型链路：

```text
Untrusted Web Page
→ Research Agent
→ Summary Message
→ Parent Agent
→ High-privilege Tool
```

攻击不一定直接命中最终执行 Agent，也可能跨 Agent 传播。

因此消息需要 Trust Boundary。

---

#### 6.4.82 Provenance

关键 Claim 应尽可能携带：

```text
source
observed_at
source_type
agent_inference
confidence
version
```

这样 Receiver 才能知道：

```text
这是原始事实？
还是上游 Agent 的解释？
```

---

#### 6.4.83 Evidence 不应只剩自然语言结论

例如：

```text
“代码没有安全问题。”
```

信息量很低。

更好的返回：

```text
finding
location
evidence
check_performed
limitations
```

这样下游才能独立验证。

---

#### 6.4.84 Sender Identity

Receiver 必须知道：

```text
Who sent this?
```

身份用于：

- policy；
- trust；
- audit；
- routing；
- delegation chain。

匿名文本不适合承载高权限控制。

---

#### 6.4.85 Authentication

Authentication 回答：

```text
这个消息真的来自声称的 Sender 吗？
```

没有 Authentication，后续 Authorization 无从谈起。

---

#### 6.4.86 Authorization

即使 Sender 身份真实，也要问：

```text
它有权要求我做这件事吗？
```

因此：

```text
Authenticated
≠ Authorized
```

---

#### 6.4.87 Authority Context

一条高风险请求最好携带：

```text
on_behalf_of
delegated_by
scope
constraints
approval
expires_at
```

这样 Receiver 能验证 Delegation Chain。

---

#### 6.4.88 Capability Laundering

一个低权限 Agent 可能试图：

```text
请求高权限 Agent 代它执行
```

如果 Receiver 只看自己的权限，不看请求来源与 delegated authority，就会发生 Capability Laundering。

因此需要回答：

```text
Who is asking?
On whose behalf?
Under what authority?
```

---

#### 6.4.89 Confused Deputy

高权限 Agent 可能被低信任消息诱导，为发送方完成本不允许的动作。

通信层的防护包括：

- explicit authority；
- provenance；
- policy check；
- side-effect confirmation；
- data / instruction separation。

---

#### 6.4.90 Secret Minimization

不要因为“另一个也是内部 Agent”就发送全部 Secrets。

通信应遵循：

```text
Need-to-know
```

包括：

- credentials；
- personal data；
- private files；
- tenant data；
- hidden system instructions。

---

#### 6.4.91 Cross-tenant Communication

Multi-tenant Agent Service 中必须绑定：

```text
tenant_id
session_id
task_id
```

并确保消息不能跨 namespace 错投。

否则一个 routing bug 就可能成为数据泄漏。

---

#### 6.4.92 Trust Level

不同消息源可有不同 Trust：

```text
authoritative service
trusted internal agent
unverified peer
external remote agent
untrusted content-derived message
```

Receiver 的处理策略应该随 Trust Level 变化。

---

#### 6.4.93 Remote Agent 不应该自动被当作内部 Agent

跨组织 / 跨供应商时：

```text
remote agent
```

通常意味着不同：

- identity domain；
- policy；
- SLA；
- data governance；
- observability；
- trust boundary。

6.7 A2A 会专门展开协议层。

---

#### 6.4.94 Communication Contract 应先于 Prompt

设计 Agent 通信时优先顺序应该是：

```text
Message semantics
→ state transitions
→ authority
→ error / retry
→ schema
→ prompt wording
```

而不是：

```text
先写“请你和另一个 Agent 协作”
→ 再希望模型自己发明协议
```

---

#### 6.4.95 Semantic Contract

除了 JSON Schema，还需要回答：

```text
status=completed 到底表示什么？
confidence=0.8 如何产生？
evidence 字段必须满足什么条件？
partial 的边界是什么？
```

这就是 Semantic Contract。

---

#### 6.4.96 Completion Contract

`completed` 至少可能有三种语义：

```text
sender believes completed
contract conditions satisfied
externally verified completed
```

必须区分，否则系统会出现 False Success。

---

#### 6.4.97 Ack Contract

Ack 也应定义层级：

```text
RECEIVED
VALIDATED
ACCEPTED
STARTED
COMPLETED
VERIFIED
```

不要把所有阶段压成一个布尔值。

---

#### 6.4.98 Error Contract

错误至少应定位到：

```text
transport
routing
authentication
authorization
schema
semantic validation
execution
tool
state conflict
verification
timeout
cancellation
```

这样才能做 Failure Localization。

---

#### 6.4.99 Communication State Machine

一次 Request 可以简化为：

```text
CREATED
  ↓
SENT
  ↓
RECEIVED
  ↓
VALIDATED
  ↓
ACCEPTED
  ↓
RUNNING
  ↓
COMPLETED / FAILED / CANCELLED / UNKNOWN
  ↓
VERIFIED
```

实际系统可以更简单，但必须知道自己省略了哪些状态。

---

#### 6.4.100 Task State 与 Message State 不一样

一条 Message 可以：

```text
delivered successfully
```

但它对应的 Task 仍然：

```text
running
```

所以：

```text
Message State ≠ Task State
```

---

#### 6.4.101 Artifact 与 Message 不一样

Message 适合表达：

```text
instruction
status
small result
reference
```

Artifact 适合承载：

```text
report
file
dataset
large structured output
```

不要把 10 MB 报告直接塞进每个 Agent Context。

---

#### 6.4.102 Artifact Reference

更合理的方式常是：

```text
Message:
  artifact_id
  summary
  provenance
  checksum / version
```

Receiver 按需读取 Artifact。

这符合 Minimal Sufficient Context。

---

#### 6.4.103 Message History 不等于 Authoritative State

聊天记录可以帮助解释发生过什么，但：

```text
latest message
```

不一定是最新真实状态。

关键业务对象仍应有 authoritative source。

---

#### 6.4.104 Group Chat 是高风险默认设计

把多个 Agent 全部放进同一个共享聊天：

```text
A, B, C, D all see everything
```

看起来协作自然，但会导致：

- Context 膨胀；
- authority 模糊；
- ownership 模糊；
- information leakage；
- response competition；
- duplicated work。

---

#### 6.4.105 广播不是默认方案

如果只有 B 需要某条信息：

```text
A → B
```

通常优于：

```text
A → everyone
```

广播应有明确理由，例如：

- global safety event；
- shared schedule change；
- system-wide cancellation。

---

#### 6.4.106 Routing

通信系统必须回答：

```text
Who should receive this?
```

Routing 可以基于：

- role；
- capability；
- task ownership；
- subscription；
- policy；
- tenant；
- locality；
- availability。

Routing 本身也是 coordination policy。

---

#### 6.4.107 Recipient Discovery 与 Message Delivery 不一样

先解决：

```text
Who can handle this?
```

再解决：

```text
How do I send it?
```

前者属于 Discovery / Routing，后者属于 Transport。

6.7 A2A 会讨论 Remote Agent Discovery 的标准化表达。

---

#### 6.4.108 Single Owner Principle

对关键 Task 最好始终能回答：

```text
Who currently owns the next decision?
```

如果所有 Agent 都“共同负责”，实际往往意味着没有清晰 owner。

Communication 应服务 Ownership，而不是模糊 Ownership。

---

#### 6.4.109 Peer Collaboration 仍需要责任边界

即使没有中心 Parent，也应明确：

```text
decision owner
artifact owner
state owner
approval owner
```

Peer-to-Peer 不等于无治理。

---

#### 6.4.110 Communication Conflict

两个 Agent 可能发送冲突结论：

```text
A: X is true
B: X is false
```

不能简单：

```text
last message wins
```

应回到：

- provenance；
- evidence；
- authority；
- freshness；
- verifier；
- uncertainty。

---

#### 6.4.111 Consensus 不是 Verification

三个 Agent 一致：

```text
X is true
```

仍可能因为：

- 共享错误数据源；
- 共享 Prompt；
- 共享模型偏差；
- 相互抄袭。

因此：

> **Agreement is evidence about consistency, not automatically about truth.**

---

#### 6.4.112 Semantic Echo

Agent B 可能只是复述 A：

```text
A → B → C
```

最后看起来像“三个 Agent 都认为 X”，实际信息源只有一个。

因此 Provenance Graph 要保留 source lineage。

---

#### 6.4.113 Information Cascade

一个早期错误消息被后续 Agent 当作事实：

```text
A guesses X
→ B treats X as fact
→ C sees A+B agreement
→ confidence increases
```

这是 Multi-Agent 特有的错误放大方式之一。

---

#### 6.4.114 Independent Verification

需要独立验证时，应尽量避免给 Verifier：

```text
上游完整结论 + 强引导
```

而是提供：

```text
claim
evidence
verification target
```

必要时让其重新查询 authoritative source。

---

#### 6.4.115 Semantic Ack

对于关键任务，可以让 Receiver 返回：

```text
I understand the objective as ...
Constraints are ...
I will not ...
Success means ...
```

这是一种 Semantic Ack。

它比：

```text
OK
```

更能发现误解。

---

#### 6.4.116 Semantic Ack 不应该滥用

每条简单消息都要求 Receiver 复述，会增加：

- tokens；
- latency；
- verbosity。

因此只在：

- 高风险；
- 高歧义；
- 长任务；
- 权限敏感；

场景使用。

---

#### 6.4.117 Clarification Protocol

当 Receiver 发现消息不足以安全执行，应：

```text
request clarification
```

而不是补全关键未知信息。

典型缺失：

- target；
- scope；
- authority；
- deadline；
- success criteria；
- destructive-action confirmation。

---

#### 6.4.118 Ambiguity Budget

并非所有歧义都值得澄清。

可以问：

```text
Will this ambiguity change the action or risk?
```

若不会，可继续。

若会显著改变 Side Effect，则应 clarify / escalate。

---

#### 6.4.119 Communication Failure Taxonomy

至少可以分成：

```text
Transport Failure
Routing Failure
Delivery Failure
Schema Failure
Version Failure
Authentication Failure
Authorization Failure
Semantic Misunderstanding
Stale Information
Duplicate Processing
Ordering Failure
Correlation Failure
Task-state Mismatch
Trust / Provenance Failure
Verification Failure
```

这比统一归类成：

```text
multi-agent failed
```

更有诊断价值。

---

#### 6.4.120 Failure Localization

当最终结果错误时，可以沿通信链检查：

```text
Was the right information produced?
Was it sent?
Was it delivered?
Was it routed to the right Agent?
Was it fresh?
Was the schema understood?
Was the semantic intent understood?
Was it authorized?
Was it incorporated into state?
Was the resulting action correct?
Was completion verified?
```

这是非常实用的 Debug Checklist。

---

#### 6.4.121 Observability：Message Trace

至少要能追踪：

```text
message_id
sender
recipient
task_id
correlation_id
causation_id
timestamp
message_type
schema_version
delivery status
processing status
```

高风险场景还应记录：

```text
authority
policy decision
state version
side effects
```

---

#### 6.4.122 Trace Graph 比 Transcript 更重要

Multi-Agent 系统不是简单线性聊天。

更接近：

```text
Message A
 ├→ Message B
 │   └→ Tool Call C
 └→ Message D
     └→ Agent E
```

因此 Observability 最好支持：

```text
causal graph / trace graph
```

而不只是按时间打印所有文本。

---

#### 6.4.123 Communication Metrics：Delivery

Transport 层可以看：

```text
delivery_success_rate
delivery_latency
duplicate_delivery_rate
out_of_order_rate
expired_message_rate
queue_age
```

这些主要评价基础设施。

---

#### 6.4.124 Communication Metrics：Semantic Fidelity

更 Agent-specific 的指标包括：

```text
constraint_preservation_rate
intent_understanding_accuracy
field_extraction_accuracy
semantic_ack_mismatch_rate
critical_omission_rate
```

这些评价“信息有没有被正确理解”。

---

#### 6.4.125 Communication Metrics：Coordination

可以统计：

```text
handoff_success_rate
delegation_return_rate
wrong_recipient_rate
unnecessary_broadcast_rate
duplicate_work_rate
stale-result-consumption_rate
late-result-conflict_rate
```

---

#### 6.4.126 Communication Metrics：Efficiency

常见指标：

```text
messages_per_task
tokens_per_message
communication_tokens_per_task
communication_latency
critical_path_communication_latency
unused_message_rate
```

`unused_message_rate` 很重要：如果大量消息从未影响任何决策，系统可能过度通信。

---

#### 6.4.127 Communication Metrics：Safety

可以看：

```text
unauthorized_message_rate
privilege-escalation-via-message
secret-exposure rate
cross-tenant leakage
prompt-injection propagation rate
unverified-claim consumption rate
```

---

#### 6.4.128 Communication Metrics：Reliability

可以额外统计：

```text
lost_ack_rate
duplicate_effect_rate
retry_success_rate
false_failure_rate
false_success_rate
cancel-after-complete rate
unknown_outcome_rate
```

---

#### 6.4.129 Fault Injection

成熟系统可以主动注入：

```text
delay
drop
duplicate
reorder
stale message
schema mismatch
receiver unavailable
lost ack
```

观察 Agent 系统是否仍能安全恢复。

这比只在理想网络里测试更接近真实可靠性。

---

#### 6.4.130 Communication Evaluation 不应只看最终 Accuracy

最终任务对了，不代表通信设计健康。

可能存在：

```text
大量重复
偶然成功
权限过宽
错误 Ack
高额通信成本
```

因此要同时评价：

```text
Outcome
+ Process
+ Reliability
+ Efficiency
+ Safety
```

---

#### 6.4.131 典型反模式一：Free-form Everything

所有消息都是：

```text
一段自然语言
```

没有 Task ID、状态、Schema、Authority。

系统规模变大后几乎无法可靠调试。

---

#### 6.4.132 典型反模式二：Ack = Success

```text
Receiver: OK
```

上游立刻标记：

```text
task completed
```

这是最常见的状态语义错误之一。

---

#### 6.4.133 典型反模式三：Timeout = Failure

Timeout 后直接 Retry 高副作用动作，可能产生：

```text
duplicate ticket
duplicate email
duplicate payment
duplicate file write
```

---

#### 6.4.134 典型反模式四：Broadcast Everything

所有 Agent 接收所有消息：

```text
everyone knows everything
```

会导致 Context、成本、隐私与责任边界同时恶化。

---

#### 6.4.135 典型反模式五：Agent Says So

一个 Agent 说：

```text
“已经完成”
```

系统就把它当 Ground Truth。

应保留：

```text
self-reported success
vs verified success
```

---

#### 6.4.136 典型反模式六：No Version / Freshness

Agent 根据旧状态通信，Receiver 又把它当最新事实，会形成 silent stale-state failure。

---

#### 6.4.137 典型反模式七：Implicit Authority

消息里一句：

```text
“帮我把这个删掉”
```

Receiver 不验证 on-behalf-of / scope / approval 就执行。

这是 Communication → Side Effect 的危险跨越。

---

#### 6.4.138 典型反模式八：Conversation as Database

通过翻历史消息判断当前状态：

```text
“最后一次有人说 status=approved”
```

不等于 authoritative state。

关键状态应该有明确 owner / store。

---

#### 6.4.139 典型反模式九：LLM as Message Broker

让一个 LLM 负责：

```text
排序
去重
幂等
锁
事务
版本比较
```

这些确定性基础设施问题应交给 Runtime / System，而不是模型猜。

---

#### 6.4.140 典型反模式十：Communication Without Acceptance Criteria

Agent A 要 B：

```text
“查一下这个问题。”
```

B 返回一大段文字，A 无法判断：

```text
够不够？
可不可信？
下一步是什么？
```

Communication Contract 应从 Task Contract 开始。

---

#### 6.4.141 一个稳健的通信参考结构

```text
Sender Agent
  ↓
Construct Message
  ├─ task / correlation
  ├─ type / schema
  ├─ minimal payload
  ├─ provenance / freshness
  ├─ authority
  └─ expected response
  ↓
Transport / Broker
  ↓
Receiver Intake
  ├─ authenticate
  ├─ authorize
  ├─ deduplicate
  ├─ validate schema
  ├─ validate freshness
  ├─ interpret semantics
  └─ update local task state
  ↓
Execute / Respond
  ↓
Ack / Progress / Result / Error
  ↓
Sender Reconcile
  ├─ correlate
  ├─ verify
  ├─ update authoritative state
  └─ decide next action
```

---

#### 6.4.142 一个简单伪代码

```python
def send_agent_request(receiver, task, payload):
    msg = build_message(
        type="request",
        message_id=new_id(),
        task_id=task.id,
        correlation_id=new_id(),
        schema_version="v1",
        expires_at=task.deadline,
        authority=task.delegated_authority,
        provenance=task.provenance,
        payload=payload,
    )

    transport.send(receiver, msg)

    result = wait_for_correlated_result(
        correlation_id=msg.correlation_id,
        deadline=task.deadline,
    )

    if result is None:
        return reconcile_unknown_outcome(msg)

    validate_sender(result)
    validate_schema(result)
    validate_freshness(result)
    verify_if_required(result)

    return update_task_state(result)
```

重点不是 API，而是：

```text
Identity
Correlation
Semantics
Authority
Unknown outcome
Verification
```

---

#### 6.4.143 Communication 与 Tool Call 的面试区分

可以这样回答：

> **Tool Call 通常是 Agent 对某个 Capability 的调用；Agent Communication 是两个具有独立决策边界的执行主体之间的信息与协调交换。**

一个 Remote Agent 可以被包装成 Tool，但系统语义上仍可能存在：

- 独立 Task；
- 独立状态；
- 长生命周期；
- 双向消息；
- authority boundary。

---

#### 6.4.144 Communication 与 Memory 的面试区分

Memory 解决：

```text
过去信息如何被保存、检索、复用
```

Communication 解决：

```text
当前一个主体如何把信息传给另一个主体
```

消息可以被写入 Memory，但二者不是同一层。

---

#### 6.4.145 Communication 与 Shared Context 的面试区分

Communication：

```text
A → B sends X
```

Shared Context：

```text
A and B both observe / depend on X
```

前者是 exchange mechanism，后者是 information visibility / state-sharing model。

下一节会继续展开。

---

#### 6.4.146 Communication 与 A2A 的面试区分

可以直接说：

> **Communication 是问题域；A2A 是一种面向独立 Agent 互操作的协议标准。**

Communication 先定义：

```text
message semantics
task semantics
state
authority
reliability
```

A2A 再给出跨实现的标准化对象与交互方式。

---

#### 6.4.147 A2A 对本节最有价值的启发

当前 A2A 规范显式区分：

```text
Message
Task
Artifact
Context
Streaming / Push updates
```

这很重要，因为它说明：

```text
一条消息
≠ 一个任务
≠ 一个最终产物
```

6.7 会再详细讨论 Agent Card、Discovery、Task State 与 Remote Agent。

---

#### 6.4.148 OpenAI Agents SDK 对本节的启发

Agents-as-Tools 与 Handoffs 展示了两种不同 communication / control relation：

```text
Manager keeps control
vs
Specialist becomes active owner
```

这说明设计通信时不能只看“Agent A 调用了 Agent B”，还要看：

```text
Who owns the next decision?
```

---

#### 6.4.149 Anthropic 工程经验对本节的启发

Routing、parallelization、orchestrator-workers 等模式反复说明：

> **Multi-Agent 的价值来自清晰分解与可组合边界，而不是 Agent 数量。**

Communication 也是如此：消息越多，不等于协作越好。

---

#### 6.4.150 设计 Agent Communication 时最值得先问的 15 个问题

1. 这条通信的 Message Type 是什么？
2. 它属于哪个 Task / Delegation？
3. Sender / Receiver 身份是什么？
4. 谁拥有当前 Control Ownership？
5. Payload 中哪些是事实、推断、指令、证据？
6. 信息是否可能过期？
7. 需要什么 Authority 才能执行？
8. 是否允许重复投递？
9. Side Effect 是否幂等？
10. Timeout 后 Outcome 是 Failed 还是 Unknown？
11. 是否可能乱序 / 晚到？
12. Ack 到底表示哪个阶段？
13. Receiver 如何验证关键 Claim？
14. 这条消息真的需要发送吗？
15. 如何从 Trace 重建完整因果链？

---

#### 6.4.151 一个非常实用的判断框架

可以把通信可靠性粗略理解为：

```text
Reliable Communication
=
Correct Recipient
× Correct Payload
× Correct Semantics
× Correct Freshness
× Correct Authority
× Correct Correlation
× Safe Delivery / Retry
× Correct State Integration
```

任何一项接近 0，最终协作质量都可能显著下降。

---

#### 6.4.152 Communication 最核心的一句话

> **Agent Communication 不是“把文字发给另一个模型”，而是让跨决策边界的信息交换具备明确身份、语义、任务关联、时效、权限、可靠性与可验证结果。**

真正成熟的通信设计关注：

```text
Minimal Sufficient Information
+ Explicit Message Semantics
+ Correlation / Causality
+ Provenance / Freshness
+ Least Authority
+ Idempotent Recovery
+ Observable State Transitions
+ Verification
```

因此：

> **More messages do not create better coordination; better contracts do.**

---

#### 6.4.153 参考资料

1. Agent2Agent (A2A) Protocol. *Official Specification, v0.3.0*. https://a2a-protocol.org/v0.3.0/specification/ 。当前规范显式区分 Message、Task、Artifact、Context，并支持流式更新与异步任务交互；可作为跨 Agent 通信中“消息、任务、产物不要混为一谈”的协议级参考。
2. OpenAI. *Agents SDK — Agent orchestration*. https://openai.github.io/openai-agents-python/multi_agent/ 。关于 Agents-as-Tools 与 Handoffs 两种常见多 Agent 控制关系，以及 LLM orchestration 与 code orchestration 的边界。
3. OpenAI. *Agents SDK — Handoffs*. https://openai.github.io/openai-agents-python/handoffs/ 。关于 Agent 间任务转移、handoff input 与 active agent 切换，可用于理解 Communication 与 Control Ownership Transfer 的区别。
4. Anthropic. *Building Effective Agents*. https://www.anthropic.com/engineering/building-effective-agents 。关于 routing、parallelization、orchestrator-workers，以及优先采用简单、可组合架构的工程原则。
5. Martin Kleppmann. *Designing Data-Intensive Applications*. O’Reilly Media, 2017. 关于消息传递、复制、并发、分布式故障、幂等与一致性等基础概念；这些语义在异步 Multi-Agent 通信中仍然成立。
6. Michael Nygard. *Release It! Design and Deploy Production-Ready Software*, 2nd ed. Pragmatic Bookshelf, 2018. 关于 timeout、retry、backpressure、circuit breaker 与故障隔离等生产系统可靠性原则，可用于理解 Agent Communication 的运行时语义。
