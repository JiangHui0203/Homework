### 4.5 Persistence

#### 4.5.1 定义：Persistence 到底是什么？

在 Agent 系统中，Persistence 不是“把变量写到磁盘”这么简单。

更准确地说：

> **Persistence 是让 Agent 的关键 State、Memory、Artifact 与执行证据，在模型调用、进程、机器、Session、故障甚至部署边界之外，仍能按照明确的一致性与恢复语义继续存在。**

可以把它理解为：

```text
Volatile Runtime State
        ↓
Persistence Boundary
        ↓
Durable Representation
        ↓
Reload / Recover / Resume
        ↓
Usable State Again
```

它回答的不是：

> “什么值得记？”

而是：

> **“已经决定要保留的东西，怎样真的不会因为一次进程退出、机器重启或服务升级就消失？”**

---

#### 4.5.2 Persistence 与 Memory 的第一条边界

```text
Memory
= 什么信息值得保留并影响未来决策

Persistence
= 这些信息怎样跨时间和故障存活
```

因此：

```text
Long-term Memory
需要 Persistence
```

但：

```text
Persistence
不只服务于 Memory
```

还可能持久化：

- Working State；
- Session；
- Checkpoint；
- Pending Action；
- Approval；
- Budget；
- Tool Receipt；
- Effect Ledger；
- Audit Log；
- Artifact；
- Queue / Job State；
- Retry State；
- Evaluation Trace。

所以：

> **Memory 是持久化对象的一类；Persistence 是更底层的系统能力。**

---

#### 4.5.3 Persistence 与 State 的边界

Working State 描述：

```text
Agent 当前处于什么执行状态
```

Persistence 描述：

```text
这个状态是否能在 Runtime 生命周期之外继续存在
```

例如：

```text
state.current_step = 7
```

如果只存在进程内内存：

```text
process crash
↓
current_step 丢失
```

如果被可靠持久化：

```text
process crash
↓
restart
↓
load persisted state
↓
current_step = 7
```

因此：

```text
State Semantics
≠
Persistence Semantics
```

State 可以设计得很好，但如果没有正确持久化，仍然无法可靠恢复。

---

#### 4.5.4 Persistent ≠ Permanent

这是非常重要的一条边界。

```text
Persistent
= 能跨某些生命周期边界存活
```

不代表：

```text
Permanent
= 永远不能删除
```

持久化数据仍然应该支持：

- retention；
- expiry；
- deletion；
- compaction；
- archival；
- legal hold；
- user-requested removal；
- schema migration。

所以：

> **Persistence 解决“能留下来”；Retention Policy 决定“应该留多久”。**

---

#### 4.5.5 Durability 是 Persistence 的核心属性之一

Durability 通常回答：

> **系统告诉你“写成功”以后，即使发生故障，这次写入是否仍然应该存在？**

例如：

```text
memory.write(x)
→ success
```

如果下一秒进程 crash 后：

```text
x 消失
```

那么这个 success 的 durability 语义很弱。

因此：

```text
Write Acknowledgement
必须对应某种明确的 Durability Guarantee
```

不能只看 API 返回成功。

---

#### 4.5.6 In-memory State 与 Durable State

最基本的区别：

```text
In-memory
├── 快
├── 低延迟
├── 易变
└── process loss 后通常消失

Durable
├── 相对慢
├── 有持久化成本
├── 可跨进程 / 重启
└── 可用于恢复
```

Agent 系统经常需要二者结合：

```text
Hot Working State
      ↓ periodic / transactional persist
Durable State Store
```

而不是强迫每个 token、每个中间变量都同步落盘。

---

#### 4.5.7 Persistence Boundary 必须明确

至少要回答：

```text
什么事件发生以后，State 才算 durable？
```

可能是：

- 每个 Agent Step 后；
- 每个 Tool Call 前；
- 每个 Tool Call 后；
- 每次 Effectful Action 前后；
- 每个 Plan Step 后；
- 每 N 秒；
- Session 结束时；
- 显式 checkpoint 时。

不同边界意味着不同的：

```text
Recovery Point
Lost Work Window
Write Cost
Latency
Consistency
```

---

#### 4.5.8 Persistence Granularity

持久化粒度可能是：

```text
Whole State
Field-level State
Event
Transition
Artifact
Memory Item
Tool Receipt
Effect Record
```

粒度越粗：

```text
实现简单
但写放大更大
冲突合并更难
```

粒度越细：

```text
增量更新灵活
但 schema / consistency / replay 更复杂
```

因此没有统一最优答案。

---

#### 4.5.9 Snapshot 是什么？

Snapshot 是：

> **某个时间点上系统状态的一份相对完整映像。**

例如：

```json
{
  "task_id": "T42",
  "step": 8,
  "plan": [...],
  "budget_remaining": 1200,
  "pending_actions": [],
  "memory_refs": [...],
  "status": "running"
}
```

它回答：

> “在这个时间点，State 大致是什么样？”

---

#### 4.5.10 Checkpoint 是什么？

Checkpoint 通常比 Snapshot 多一层语义：

> **它不仅保存状态，而且被系统认可为一个可以恢复 / Resume 的执行点。**

因此：

```text
Snapshot
= 状态副本

Checkpoint
= 可恢复执行点
```

一个 Snapshot 不一定包含足够的信息用于正确 Resume。

---

#### 4.5.11 Checkpoint 必须包含什么？

可靠 Checkpoint 通常至少要考虑：

```text
Task Identity
Current State
Plan / Cursor
Pending Actions
Committed Effects
Unknown Effects
Tool Receipts
Approval State
Budget
Version
Environment References
Schema Version
Checkpoint Time
```

尤其是：

```text
哪些 Effect 已经发生？
```

如果没有记录，Resume 时极易重复执行。

---

#### 4.5.12 Resume ≠ Restart

```text
Restart
= 从头再来

Resume
= 从已知恢复点继续
```

二者完全不同。

如果一个 Agent 已经：

```text
发出 3 封邮件
创建 2 个 issue
修改 5 个文件
```

然后 crash，简单 Restart 可能复制所有副作用。

所以对于 effectful Agent：

> **Resume correctness 比单纯“能重新启动”重要得多。**

---

#### 4.5.13 Event Log 是什么？

Event Log 保存的不是“当前最终状态”，而是：

```text
发生过哪些状态变化事件
```

例如：

```text
TaskCreated
PlanGenerated
ToolSelected
ToolExecuted
FileWritten
VerificationPassed
```

于是当前状态可以通过：

```text
Initial State
+
Events
↓
Replay
↓
Current State
```

重建。

---

#### 4.5.14 Snapshot vs Event Log

```text
Snapshot
= current state image

Event Log
= how state changed over time
```

Snapshot 读取快，但历史细节弱。

Event Log 审计强，但 replay 成本高。

现实系统经常组合：

```text
Periodic Snapshot
+
Incremental Event Log
```

恢复时：

```text
Latest Snapshot
+
Events after Snapshot
↓
Current State
```

---

#### 4.5.15 Event Sourcing 的直觉

Event Sourcing 的核心思想是：

> **把“发生了什么”作为权威历史，而不是只保存最终对象。**

对于 Agent 很有价值，因为 Agent 本身天然是 trajectory-based system：

```text
State
→ Action
→ Observation
→ State
→ ...
```

但它也会带来：

- event schema 演进；
- replay compatibility；
- duplicate event；
- ordering；
- compaction；
- privacy deletion；
- derived state rebuild；
- 长轨迹存储成本。

所以不应因为“Agent 有 trajectory”就自动采用完整 Event Sourcing。

---

#### 4.5.16 WAL：Write-Ahead Log 是什么？

Write-Ahead Log 的基本思想是：

```text
先记录将要提交的变化
↓
再真正修改主要状态
```

这样 crash 后可以根据 Log 判断：

```text
哪些操作已提交？
哪些操作只记录但未完成？
哪些需要恢复或回滚？
```

对于 Agent Runtime，它尤其适用于：

```text
State Mutation
Effect Ledger
Job State
Transactional Metadata
```

---

#### 4.5.17 WAL ≠普通日志

普通日志可能只是：

```text
“正在修改文件...”
```

WAL 通常承担的是：

```text
恢复正确性的一部分
```

所以：

```text
Observability Log
≠
Recovery Log
```

不能因为“系统日志很全”就认为它具备 crash recovery。

---

#### 4.5.18 Transaction 是什么？

Transaction 解决的是：

> **多个相关状态变化应该以什么原子性和一致性语义提交。**

经典属性常用 ACID 描述：

- Atomicity；
- Consistency；
- Isolation；
- Durability。

对于 Agent，不需要机械背数据库定义，而要理解：

```text
某次 State Update
是否允许只成功一半？
```

---

#### 4.5.19 Atomicity 在 Agent Persistence 中的意义

假设一次 Agent Step 同时更新：

```text
step = 9
budget_remaining -= 1
last_tool_result = X
status = running
```

如果只更新了：

```text
step = 9
```

却没有更新 budget 和 last_tool_result，系统可能进入不一致状态。

所以需要考虑：

```text
这些字段是否应该原子提交？
```

---

#### 4.5.20 Persistence Atomicity ≠ External Effect Atomicity

非常重要。

数据库里可以原子提交：

```text
state.status = sent
```

但真正的：

```text
send_email()
```

发生在外部系统。

因此：

```text
Database Commit
≠
Real-world Effect Commit
```

跨系统时很难获得真正的全局原子性。

这也是为什么需要：

- idempotency；
- reconciliation；
- compensation；
- effect ledger；
- outbox / inbox pattern。

---

#### 4.5.21 Crash Consistency

Crash Consistency 关注：

> **如果系统在任意时刻突然停止，重启后看到的持久化状态是否仍然是一个合法、可解释的状态？**

不是简单：

```text
“数据还在不在？”
```

而是：

```text
“剩下的数据是否彼此一致？”
```

---

#### 4.5.22 Crash Window

可以把一次执行抽象成：

```text
1. decide action
2. persist intent
3. execute tool
4. receive result
5. persist result
6. update state
```

系统可能在任意两个步骤之间 crash。

例如：

```text
Tool 已经成功
但 result 还没持久化
↓
crash
```

恢复后系统可能以为：

```text
Tool 从未执行
```

于是重复副作用。

所以 Persistence 设计必须分析：

> **Crash can happen anywhere.**

---

#### 4.5.23 Intent Record

对高风险 effectful Action，可以在执行前先 durable 记录：

```text
Action Intent
```

例如：

```json
{
  "action_id": "A17",
  "tool": "send_email",
  "resolved_args_hash": "...",
  "status": "prepared"
}
```

执行后再变成：

```text
committed / failed / unknown
```

这样恢复时至少知道：

```text
系统曾经准备执行什么
```

---

#### 4.5.24 Effect Ledger 与 Persistence

前面 Side Effects 已经定义 Effect Ledger。

Persistence 层要解决：

> **Effect Ledger 自己怎样可靠保存。**

如果 Ledger 只存在内存：

```text
Agent crash
↓
Effect History 丢失
↓
Duplicate Side Effects
```

所以 effectful 系统里：

```text
Effect Ledger
通常属于高价值 durable state
```

---

#### 4.5.25 Outbox Pattern 的直觉

典型问题：

```text
数据库状态更新成功
但外部消息没发出去
```

或者反过来：

```text
外部消息发出
但数据库状态没更新
```

Outbox Pattern 的核心思想是：

```text
业务状态更新
+
待发送事件
```

先在同一 durable transaction 内保存。

然后独立 worker 再可靠发送。

它不能解决所有 Agent effect 问题，但能说明：

> **把“我要产生一个外部 effect”先变成可恢复的 durable intent，常比直接裸调用可靠。**

---

#### 4.5.26 At-most-once / At-least-once / Effectively-once

分布式持久化和恢复经常绕不开：

```text
At-most-once
= 最多执行一次，但可能丢

At-least-once
= 至少执行一次，但可能重复

Effectively-once
= 通过幂等、去重等机制让业务效果看起来像一次
```

对于 Agent：

```text
“重试几次”
```

必须结合这些语义理解。

---

#### 4.5.27 Exactly-once 为什么很难？

尤其跨：

```text
Agent Runtime
Email API
Payment API
Filesystem
Database
```

多个独立系统时，很难保证真正意义上的全局 exactly-once。

更现实的是组合：

```text
Stable Action ID
Idempotency Key
Deduplication
Durable Intent
Reconciliation
```

达到业务上的 effectively-once。

---

#### 4.5.28 Stable Identity 很重要

Persistence 系统必须有稳定 ID。

例如：

```text
run_id
session_id
task_id
step_id
action_id
checkpoint_id
memory_id
artifact_id
```

否则恢复后很难知道：

```text
这个对象是不是同一个逻辑对象？
```

稳定 ID 也是去重、审计、幂等和关联日志的基础。

---

#### 4.5.29 Session Persistence

Session 通常代表：

```text
一段连续交互 / 执行上下文
```

Session Persistence 可能保存：

- session metadata；
- active task；
- working state ref；
- short-term memory ref；
- current plan；
- pending approvals；
- resume token；
- timestamps；
- ownership。

但：

```text
Session
≠
Memory
```

Session 只是组织运行生命周期的一种边界。

---

#### 4.5.30 Session End 后什么保留？

不能默认：

```text
Session 结束
→ 全部删除
```

也不能默认：

```text
Session 结束
→ 全部永久保存
```

需要分类：

```text
Ephemeral State
Short-term Memory
Long-term Memory
Audit Evidence
Artifacts
Compliance Records
```

分别应用不同 retention policy。

---

#### 4.5.31 Checkpoint Frequency

Checkpoint 太频繁：

```text
Write Cost ↑
Latency ↑
Storage ↑
Contention ↑
```

Checkpoint 太稀疏：

```text
Lost Work Window ↑
Replay Cost ↑
Duplicate Effect Risk ↑
```

所以要根据：

```text
Step Cost
Effect Risk
State Size
Recovery Objective
Latency Budget
```

权衡。

---

#### 4.5.32 Risk-aware Checkpointing

不是所有 Step 都同等重要。

例如：

```text
search_web
```

和：

```text
charge_card
```

前后对 checkpoint 的需求不同。

更合理：

```text
high-risk action
→ checkpoint before
→ durable intent
→ execute
→ checkpoint after
```

而低风险 read-only action 可以更宽松。

---

#### 4.5.33 Recovery Point Objective（RPO）的直觉

RPO 可以理解为：

> **最多能接受丢失多少最近状态？**

例如：

```text
RPO = 0
```

意味着关键 committed state 不应丢失。

而某些临时 scratchpad：

```text
丢几秒也没关系
```

不同 Agent State 不必采用同一种 RPO。

---

#### 4.5.34 Recovery Time Objective（RTO）的直觉

RTO 回答：

> **发生故障后，多久需要恢复可用？**

例如长任务 Agent：

```text
恢复 5 分钟
```

可能可以接受。

而实时客服 Agent：

```text
恢复几秒
```

可能更合理。

所以：

```text
Persistence Design
必须考虑 Recovery Time
```

而不只是 storage durability。

---

#### 4.5.35 Persistence Store 的常见类型

可能包括：

```text
Relational Database
Key-value Store
Document Store
Filesystem
Object Store
Append-only Log
Queue
Vector Store
Graph Store
```

重点不是背产品名，而是理解各自适合存什么语义。

---

#### 4.5.36 Database 适合什么？

数据库通常适合：

- structured working state；
- task metadata；
- checkpoint metadata；
- memory records；
- effect ledger；
- approval state；
- status machine；
- versioned records。

尤其需要：

```text
query
transaction
constraint
version
index
```

时通常很合适。

---

#### 4.5.37 Filesystem 适合什么？

Filesystem 常用于：

- code artifacts；
- generated documents；
- intermediate files；
- logs；
- local checkpoints；
- workspace state。

但要注意：

```text
local filesystem
可能只属于单台机器
```

所以：

```text
process persistence
≠
machine failure persistence
```

---

#### 4.5.38 Object Store 适合什么？

对象存储适合：

- large artifacts；
- model outputs；
- screenshots；
- PDFs；
- trajectory archives；
- snapshot files；
- immutable blobs。

通常不适合把高频细粒度 mutable working state 直接当数据库使用。

---

#### 4.5.39 Queue 也承载 Persistence Semantics

Job Queue / Message Queue 不只是调度。

它可能保存：

```text
pending work
retry count
delivery state
visibility timeout
dead-letter state
```

所以对于 long-running Agent：

```text
Execution Persistence
```

往往一部分在状态库，一部分在队列。

---

#### 4.5.40 Vector Store 的 Persistence 位置

Vector Store 可以持久保存 embedding index。

但要强调：

```text
Vector Index
≠
Canonical State Store
```

尤其长期 Memory：

```text
Canonical Record
应该有稳定 source of truth
```

Vector Index 更像 derived retrieval structure。

---

#### 4.5.41 Persistence 与 Canonical Source of Truth

一个非常重要的问题：

> **到底哪个副本是真相？**

例如同一 Memory 同时存在：

```text
SQL record
Vector index
Cache
Context summary
Local copy
```

必须明确：

```text
Canonical Record
```

否则更新时容易出现多个“真相”。

---

#### 4.5.42 Derived Index 不应反客为主

如果：

```text
Vector Index = old value
Canonical DB = new value
```

那么应该：

```text
DB wins
```

而不是因为 Retriever 找到了旧 embedding，就重新把旧事实写回系统。

这是长期 Memory / Retrieval 里很典型的 stale-index failure。

---

#### 4.5.43 Cache ≠ Persistence Store

Cache 通常追求：

```text
speed
```

不一定保证：

```text
durability
completeness
source of truth
```

因此：

> **不能因为 Cache 中“通常有”，就把它当恢复所依赖的唯一数据源。**

---

#### 4.5.44 Cache Loss 应该是可容忍的吗？

理想情况下：

```text
Cache Lost
↓
Performance Degrades
```

而不是：

```text
Cache Lost
↓
Correctness Breaks
```

如果 Cache 一丢 Agent 就无法恢复正确状态，说明系统很可能把 Cache 误当了 authoritative state。

---

#### 4.5.45 Persistence 与 Replication

Replication 是把数据复制到多个节点 / 区域，以提高：

- availability；
- fault tolerance；
- read scalability；
- disaster recovery。

但：

```text
Replicated
≠
Always Strongly Consistent
```

副本之间可能存在延迟。

---

#### 4.5.46 Replica Lag

例如：

```text
Primary:
state = completed

Replica:
state = running
```

如果 Agent 从 lagging replica 读取：

```text
可能错误地继续执行
```

所以对高风险状态：

```text
read freshness
```

本身就是 correctness requirement。

---

#### 4.5.47 Strong vs Eventual Consistency

不需要把它理解成数据库考试题。

对 Agent 最重要的是：

```text
如果我刚刚写入某个关键状态，下一步是否必须立刻读到它？
```

如果答案是 Yes：

```text
这个路径需要更强的 read-after-write consistency
```

而某些 analytics / old trajectory index 可以接受 eventual consistency。

---

#### 4.5.48 Read-after-write Consistency

典型：

```text
Agent 写：approval = granted
↓
马上读 approval
```

如果读到旧值：

```text
approval = pending
```

就可能走错控制流。

因此关键状态的 persistence / read path 不能只考虑写成功，还要考虑：

```text
下一步到底从哪里读？
```

---

#### 4.5.49 Concurrency 与 Persistence

多个 worker / subagent 可能同时修改同一状态。

风险包括：

```text
Lost Update
Write Skew
Duplicate Transition
Out-of-order Event
```

Persistence 层必须配合：

- version；
- compare-and-swap；
- transaction；
- lock；
- optimistic concurrency；
- idempotent state transition。

---

#### 4.5.50 Lost Update 例子

初始：

```text
budget = 10
```

Worker A 读取 10，减 1，准备写 9。

Worker B 也读取 10，减 1，写 9。

最终：

```text
budget = 9
```

但其实发生了两次消耗，应该是：

```text
budget = 8
```

这就是 persistence-level concurrency bug。

---

#### 4.5.51 Optimistic Concurrency

一种常见方法：

```text
read state version = 17
↓
compute update
↓
write only if version still = 17
```

否则：

```text
CONFLICT
↓
reload
↓
recompute
```

这和前面 Tool Execution 的 `expected_version` 是同一思想。

---

#### 4.5.52 Pessimistic Locking

另一种方法是：

```text
先锁资源
↓
修改
↓
解锁
```

可以降低并发冲突，但会带来：

- lock contention；
- deadlock；
- latency；
- crash 后 stale lock；
- distributed lock complexity。

所以不应机械选择。

---

#### 4.5.53 State Machine Transition 最好持久化语义化

与其裸写：

```text
status = "completed"
```

更可靠的系统可能显式执行：

```text
RUNNING
→ VERIFYING
→ COMPLETED
```

并检查：

```text
transition allowed?
```

这使非法跳转更容易被发现。

---

#### 4.5.54 Durable State Machine

对 long-running Agent：

```text
状态机本身
```

需要 durable。

否则 process crash 后：

```text
系统不知道任务停在哪个 phase
```

常见状态：

```text
CREATED
RUNNING
WAITING_TOOL
WAITING_APPROVAL
RECOVERING
VERIFYING
COMPLETED
FAILED
CANCELLED
```

---

#### 4.5.55 Waiting State 特别需要持久化

例如：

```text
WAITING_APPROVAL
```

可能持续：

```text
几分钟
几小时
几天
```

显然不能依赖一个进程一直活着。

所以：

> **Long-running Agent 的等待状态必须是 durable state，而不是“sleep 着等”。**

---

#### 4.5.56 External Event Resume

Agent 可能等待：

- user reply；
- approval；
- webhook；
- job completion；
- external system callback；
- scheduled time。

这些事件到达后需要：

```text
identify session/task
load durable state
apply event
resume execution
```

因此 Persistence 与 Runtime Event Handling 强相关。

---

#### 4.5.57 Correlation ID

外部 callback 必须知道：

```text
它属于哪个 task / action / run？
```

所以需要：

```text
correlation_id
callback_token
action_id
run_id
```

这些映射也必须 durable。

---

#### 4.5.58 Pending Action 需要持久化

如果 Tool 已提交但还没有 final outcome：

```text
pending_action
```

不应只存在模型 Context 中。

否则 restart 后系统可能：

```text
完全忘记自己还有一个未决操作
```

---

#### 4.5.59 UNKNOWN Outcome 需要 durable

前面已强调：

```text
UNKNOWN ≠ FAILED
```

而 Persistence 进一步要求：

> **Unknown 状态必须能跨 restart 存活。**

否则 crash 以后系统重新加载：

```text
找不到结果
→ 当成从未执行
```

就会重新制造 duplicate effect。

---

#### 4.5.60 Approval State 需要 durable

Approval 可能包含：

```text
who approved
what action
resolved args
scope
expires_at
version
```

如果只在 Context：

```text
process restart
↓
approval 丢失
```

或者更危险：

```text
approval scope 丢失
只剩“用户同意了”一句摘要
```

都会产生安全问题。

---

#### 4.5.61 Approval Replay 防护

一个已消费的 approval 不应该被无限重复使用。

可以维护：

```text
approval_id
consumed_at
action_id
scope_hash
```

从而避免：

```text
同一批准
→ 被多个高风险 Action 重放
```

---

#### 4.5.62 Budget State 也要 durable

如果 Budget 只在内存：

```text
Agent 花了 80% budget
↓
crash
↓
restart
↓
budget 又恢复 100%
```

那么 Budget Guard 失去意义。

因此重要 budget：

- model calls；
- tool calls；
- money；
- side-effect budget；
- retry count；
- deadline；

应该具备合适的 persistence semantics。

---

#### 4.5.63 Retry Count 需要 durable

否则：

```text
每次 restart
retry_count = 0
```

系统可能永久进入：

```text
crash → retry → crash → retry
```

所以 Failure Handling 的 history-aware policy 依赖 durable retry history。

---

#### 4.5.64 No-progress State 也可能需要 durable

如果系统维护：

```text
no_progress_count
repeated_action_hashes
last_progress_signature
```

这些只在内存时，restart 会让 Agent“失忆”，再次重复同样无效循环。

---

#### 4.5.65 Artifact Persistence

Agent 生成的：

- document；
- code patch；
- report；
- image；
- dataset；
- notebook；
- log；

通常不应该全部内嵌到 State DB。

更常见：

```text
Artifact Store
+
Metadata / Reference in State
```

---

#### 4.5.66 Artifact Identity

Artifact 应有：

```text
artifact_id
content hash
version
creator/run
created_at
media type
location
permission
```

尤其内容哈希有助于：

```text
验证恢复后引用的还是同一份内容
```

---

#### 4.5.67 Mutable vs Immutable Artifact

有些 Artifact 适合 immutable：

```text
trajectory archive
raw observation
execution receipt
```

有些需要 versioned mutable：

```text
working draft
code file
plan document
```

Persistent system 应明确版本语义。

---

#### 4.5.68 Versioned Artifact

不要只保存：

```text
report.md
```

还可以保存：

```text
report@v3
```

以及：

```text
parent_version
content_hash
created_by
```

这样 recovery / audit / rollback 更可靠。

---

#### 4.5.69 State 与 Artifact 不要混成一个巨型 JSON

一个常见反模式：

```text
所有状态
所有工具输出
所有文件
所有历史
```

全部塞进一个 State Blob。

结果：

- write amplification；
- merge conflict；
- schema migration 困难；
- partial update 困难；
- retrieval 困难；
- 巨大序列化成本。

更合理：

```text
Structured State
+
Artifact References
+
Event References
```

---

#### 4.5.70 Schema Version

持久化数据寿命可能比代码版本长。

所以必须考虑：

```text
今天的代码
能否读昨天的数据？
```

至少记录：

```text
schema_version
```

否则升级后无法判断如何解释旧 State。

---

#### 4.5.71 Schema Migration

当 State Schema 从：

```text
v1
```

升级到：

```text
v2
```

需要定义：

```text
old record
↓ migrate
new record
```

而不是假设所有持久化状态会神奇适配新代码。

---

#### 4.5.72 Backward Compatibility

如果系统存在 long-running tasks：

```text
Task 在 v1 创建
服务升级到 v2
Task 在 v2 恢复
```

这是非常真实的场景。

因此需要：

```text
Backward-compatible Reader
```

或明确迁移策略。

---

#### 4.5.73 Forward Compatibility

有时旧 worker 也可能看到新版本数据。

是否允许：

```text
unknown fields
```

取决于系统设计。

盲目忽略未知字段可能危险；盲目报错又可能降低可用性。

---

#### 4.5.74 Event Schema Evolution

Event Log 更麻烦，因为旧事件可能长期存在。

例如：

```text
ToolExecuted_v1
ToolExecuted_v2
```

Replay engine 需要知道：

```text
如何解释历史版本事件
```

所以 Event Sourcing 的 schema evolution 是真实成本。

---

#### 4.5.75 Snapshot Migration

Snapshot 也需要版本。

否则：

```text
load old checkpoint
↓
字段缺失 / 语义变化
↓
恢复出错
```

所以 checkpoint format 也是公共协议的一部分。

---

#### 4.5.76 Persistence Version ≠ Model Version

State / Memory 可能由：

```text
Model A
```

创建，又由：

```text
Model B
```

继续使用。

因此还应保留：

```text
created_by_model
harness_version
tool_catalog_version
```

用于 replay / audit / regression analysis。

---

#### 4.5.77 Checkpoint Resume 与 Model Change

如果 checkpoint 中保存了：

```text
Plan generated by Model A
```

恢复时已经换成 Model B：

```text
是否继续旧 Plan？
是否需要 re-validate？
```

这是 Persistence 与 Harness Policy 的交叉问题。

---

#### 4.5.78 Environment Drift

即使 Agent State 完整恢复：

```text
External Environment
```

也可能已经变化。

例如：

```text
文件变了
库存变了
Git HEAD 变了
权限变了
订单状态变了
```

因此：

> **Restore State ≠ Restore World。**

---

#### 4.5.79 Resume 前必须 Reconcile

一个可靠 resume 流程通常是：

```text
Load Durable State
↓
Check Schema / Version
↓
Inspect Pending / Unknown Effects
↓
Re-observe Critical Environment State
↓
Reconcile Differences
↓
Re-validate Plan / Approval / Preconditions
↓
Resume
```

而不是：

```text
load checkpoint
→ 直接继续下一行
```

---

#### 4.5.80 Checkpoint 不应该冻结 Stale Assumption

比如 checkpoint 保存：

```text
inventory = 5
```

两小时后恢复。

如果直接相信：

```text
inventory 仍然 = 5
```

可能错误。

所以 checkpoint 中要区分：

```text
Authoritative Internal State
vs
Observed External State
```

后者可能需要 refresh。

---

#### 4.5.81 Resume Token

系统可以使用一个稳定 token / pointer 表示：

```text
从哪里恢复
```

但 Resume Token 应该：

- scoped；
- authenticated；
- expirable when needed；
- bound to task/session；
- not leak secrets。

不能把完整敏感 State 直接塞进客户端可见 token。

---

#### 4.5.82 Persistence 与 Security

Persistent data 的风险比 transient data 更长久。

一旦保存：

```text
Secret
PII
Private Document
Access Token
Sensitive Tool Result
```

泄露窗口变长。

所以 Persistence 设计必须包括：

- access control；
- encryption；
- minimization；
- retention；
- deletion；
- audit；
- scope isolation。

---

#### 4.5.83 Data at Rest

持久化数据通常会进入：

```text
disk
database
object store
backup
replica
```

因此要考虑：

```text
encryption at rest
```

但加密不能替代：

```text
authorization
```

因为合法服务进程通常仍可解密。

---

#### 4.5.84 Secret 不应该默认持久化

尤其：

```text
API Key
OAuth Token
Password
Temporary Credential
```

原则上应尽量：

```text
reference secure secret store
```

而不是复制到：

```text
Agent State
Checkpoint
Memory
Trajectory
Log
```

---

#### 4.5.85 Credential Persistence 与 Expiry

某些 execution token 可能必须跨 resume 使用。

更安全的做法通常是：

```text
persist credential reference / scope
```

恢复时：

```text
重新获取 short-lived credential
```

而不是保存长期明文 token。

---

#### 4.5.86 Access Control 必须跟随 Persistent Object

例如：

```text
memory_id = M42
```

不仅内容要保存，权限语义也要保存：

```text
owner
workspace
tenant
visibility
ACL
```

否则恢复后可能发生 cross-user leakage。

---

#### 4.5.87 Tenant Isolation

多用户 Agent 系统里：

```text
Tenant A State
```

必须和：

```text
Tenant B State
```

明确隔离。

而且不仅主表要隔离：

- index；
- cache；
- backup；
- artifact；
- log；
- vector store；

都需要保持相同 scope。

---

#### 4.5.88 Persistence Leakage Through Derived Data

即使主记录隔离良好，仍可能通过：

```text
embedding index
summary
cache
analytics table
backup
```

泄漏。

所以权限与删除都必须传播到 derived persistence layer。

---

#### 4.5.89 Retention Policy

Persistence 不是无限保存。

不同数据可以有不同 retention：

```text
Working State       → task 生命周期
Short-term Memory   → 小时 / 天
Long-term Memory    → 可长期，但可更新/删除
Audit Record        → 依业务要求
Raw Tool Payload    → 更短
Artifact            → 按项目生命周期
```

---

#### 4.5.90 Retention ≠ TTL Only

简单 TTL：

```text
30 days
```

很有用，但不够。

还可能根据：

```text
Task Completion
User Deletion
Supersession
Policy Change
Legal Requirement
Storage Pressure
```

触发删除 / 归档。

---

#### 4.5.91 Soft Delete

Soft Delete 通常是：

```text
record 仍存在
但标记 deleted
```

优点：

- recovery；
- audit；
- accidental delete reversal。

缺点：

- 信息仍然存在；
- derived index 仍需处理；
- 隐私删除可能不满足。

---

#### 4.5.92 Hard Delete

Hard Delete 表示真正删除主要记录。

但真实系统还要考虑：

```text
replica
backup
cache
index
log
```

所以：

```text
DELETE FROM table
≠
所有副本立刻消失
```

---

#### 4.5.93 Tombstone

在分布式或索引系统中，删除有时需要保留：

```text
tombstone
```

告诉其他副本：

```text
这个对象不是“没见过”
而是“已被删除”
```

否则旧副本可能把删除的数据重新同步回来。

---

#### 4.5.94 Backup 是什么？

Backup 主要解决：

```text
大规模数据损坏 / 删除 / 灾难后
能否恢复历史数据
```

它不是：

```text
实时高可用
```

也不是：

```text
正常 checkpoint
```

---

#### 4.5.95 Backup ≠ Replica

```text
Replica
= 在线副本

Backup
= 独立恢复副本
```

如果主库误删：

```text
Replica 可能立刻同步误删
```

Backup 才可能保留较早版本。

---

#### 4.5.96 Backup 也需要验证

没有测试过 restore 的 Backup 不能被默认视为可靠。

应该周期性验证：

```text
Can Restore?
Restore Time?
Data Complete?
Schema Compatible?
Credentials Available?
```

所以：

> **Backup Success ≠ Recovery Success。**

---

#### 4.5.97 Restore Drill

工程上可以定期做：

```text
restore into isolated environment
↓
validate key state
↓
measure RTO / data loss
```

这比只看：

```text
backup job = success
```

可信得多。

---

#### 4.5.98 Disaster Recovery

更大范围故障可能包括：

- machine loss；
- region loss；
- database corruption；
- credential failure；
- provider outage。

Agent 系统如果承担长期关键任务，也要考虑：

```text
State Store 不可用时怎么办？
```

---

#### 4.5.99 High Availability 与 Durability 不一样

```text
High Availability
= 服务尽量持续可用

Durability
= 已确认数据尽量不丢
```

一个系统可以：

```text
高可用但数据丢失
```

也可以：

```text
数据很耐久但恢复很慢
```

二者不要混。

---

#### 4.5.100 Persistence 与 Observability

至少应能够观察：

```text
write latency
write failure
checkpoint age
checkpoint lag
replication lag
replay duration
restore success
schema migration failure
conflict rate
storage growth
```

否则 persistence failure 往往只会在真正需要恢复时才暴露。

---

#### 4.5.101 Persistence Metrics

可以包括：

```text
Checkpoint Success Rate
Checkpoint Freshness
Durable Write Latency
Recovery Success Rate
Recovery Time
Lost-state Rate
Duplicate-effect-after-recovery Rate
State Conflict Rate
Schema Migration Failure Rate
Backup Restore Success Rate
```

---

#### 4.5.102 Persistence Correctness 比“写成功率”更重要

系统可能有：

```text
99.999% write success
```

但恢复后：

```text
状态互相矛盾
重复执行 effect
预算重置
approval 失真
```

仍然是坏的 persistence system。

所以要测：

> **Recovered execution 是否语义正确。**

---

#### 4.5.103 Crash Injection Test

一种非常实用的测试方式：

在执行路径随机位置注入：

```text
process crash
```

然后检查：

```text
restart
↓
recover
↓
state correct?
side effects duplicated?
budget preserved?
pending action handled?
```

这比只写 unit test 更接近真实故障。

---

#### 4.5.104 Kill -9 思维实验

可以对每个关键步骤问：

> **“如果现在突然 kill -9，重启以后会发生什么？”**

例如：

```text
1. persist intent
2. send payment
3. persist receipt
```

在 2 与 3 之间 crash 时怎么办？

如果回答不出来，Persistence 设计还没有闭环。

---

#### 4.5.105 Network Partition

Persistence 问题不只 crash。

可能发生：

```text
Agent can reach Tool
but cannot reach State Store
```

或：

```text
State Store write unknown
```

这时是否继续 effectful action？

通常需要非常保守。

---

#### 4.5.106 State Store Unavailable 时怎么办？

对于 read-only exploration：

```text
可能允许有限 degraded mode
```

对于高风险 effectful action：

```text
如果无法 durable 记录 intent / effect
通常更应该 fail closed
```

所以：

> **Persistence availability 本身可以成为执行前置条件。**

---

#### 4.5.107 Fail-open vs Fail-closed

如果持久化失败：

```text
继续执行
还是停止？
```

取决于 Action 风险。

```text
read-only search
→ 可以考虑 fail-open

payment / delete / send
→ 更适合 fail-closed
```

不能统一处理。

---

#### 4.5.108 Partial Persistence Failure

例如：

```text
State DB 写成功
Vector Index 写失败
```

应该如何处理？

因为 Canonical DB 才是真相，可以：

```text
mark index dirty
↓
async repair
```

而不是把整个 Memory 当作不存在。

这再次说明：

```text
Canonical Store
vs
Derived Store
```

必须分清。

---

#### 4.5.109 Dual-write Problem

如果应用代码同时写：

```text
DB
+
Search Index
```

可能：

```text
DB success
Index fail
```

或反过来。

所以跨多个 store 的写入需要：

- transactional outbox；
- change log；
- retry；
- reconciliation；
- derived-index rebuild。

---

#### 4.5.110 Rebuildable Derived State

一个重要设计原则：

> **Derived State 尽量可以从 Canonical State 重建。**

例如：

```text
Embedding Index
```

损坏后可以：

```text
Canonical Memory Records
↓
Re-embed
↓
Rebuild Index
```

这样 recovery 更清晰。

---

#### 4.5.111 Canonical State 不能只存在 Derived Index

如果唯一的长期 Memory 只存在 vector store：

```text
embedding = source of truth
```

会带来：

- exact update 困难；
- deletion 追踪困难；
- provenance 弱；
- migration 困难；
-重建困难。

因此更合理：

```text
Canonical Record
+
Embedding Index
```

---

#### 4.5.112 Persistence 与 Audit

为了回答：

```text
谁在什么时候改了什么？
```

重要对象应保留：

```text
actor
operation
before / after
source
run_id
reason
approval_id
timestamp
```

这对 Memory correction、Effect investigation、Security 都很重要。

---

#### 4.5.113 Audit Log ≠ State Store

Audit Log 主要用于：

```text
历史追踪
```

State Store 用于：

```text
当前执行真相
```

二者可以关联，但不应简单互相替代。

---

#### 4.5.114 Immutable Audit Log 的价值

如果高风险系统允许 Agent 修改：

```text
自己的审计记录
```

那审计意义会显著下降。

所以一些 audit trail 应位于：

```text
Agent 无法任意覆写的 trust boundary
```

---

#### 4.5.115 Persistence 与 User Deletion

如果用户要求删除长期数据，需要知道它存在于：

```text
primary store
index
cache
backup
artifact
summary
replica
```

这要求系统具备：

```text
Data Lineage
```

否则无法可靠执行删除传播。

---

#### 4.5.116 Lineage 对 Persistence 的意义

Lineage 回答：

```text
这份数据从哪里来？
又生成了哪些派生数据？
```

例如：

```text
Raw Conversation
↓
Memory Summary
↓
Embedding
↓
Retrieved Context
```

如果上游删除，哪些下游需要失效？

这是 Persistence + Governance 的交叉问题。

---

#### 4.5.117 Persistence 与 Privacy Minimization

因为持久化会延长数据寿命，所以：

> **能不持久化的敏感信息，就不要为了“以后可能有用”而默认保存。**

可以优先保存：

```text
reference
hash
redacted form
minimal field
```

而不是完整原文。

---

#### 4.5.118 Raw Transcript 是否永久保存？

通常不应该把：

```text
Raw Transcript Forever
```

当成 Memory / Persistence 的默认方案。

因为它：

- 隐私风险高；
- 噪声多；
- stale information 多；
- retrieval 成本高；
- 删除复杂。

更合理是按用途分层保存。

---

#### 4.5.119 Tiered Storage

可以把数据按温度分层：

```text
Hot
→ active working state

Warm
→ recent memory / checkpoints

Cold
→ historical trajectories / archive
```

不同层使用不同：

```text
cost
latency
retention
availability
```

策略。

---

#### 4.5.120 Archival

Archive 与 active persistence 不同。

Archive 更适合：

```text
很少访问
但出于研究 / 合规 /历史原因保留
```

而不应该参与高频在线 Agent 决策。

---

#### 4.5.121 Compaction

Event Log / trajectory 长期增长时，可以做：

```text
compaction
```

例如保留：

```text
latest snapshot
+
关键事件
```

删除已经被 snapshot 吸收且不再需要的冗余细节。

但必须先明确：

```text
哪些历史仍承担 audit / research / replay 价值
```

---

#### 4.5.122 Log Compaction ≠ Memory Consolidation

非常容易混。

```text
Log Compaction
= 存储层减少冗余历史

Memory Consolidation
= 认知 / 语义层把经历抽象成长期知识
```

一个解决 storage efficiency，一个解决 knowledge representation。

---

#### 4.5.123 Persistence 与 Cost

存储不是免费的。

长期 Agent 会累积：

```text
State
Memory
Trajectory
Observation
Artifact
Checkpoint
Audit Log
Embedding
Backup
```

所以应关注：

```text
Storage Cost per Task
Storage Growth Rate
Write Amplification
Index Cost
Backup Cost
Retention Cost
```

---

#### 4.5.124 Write Amplification

一次逻辑写入可能产生：

```text
DB row
WAL
replica
index
cache invalidation
audit event
backup delta
```

所以：

```text
1 logical write
≠
1 physical write
```

这影响成本和延迟。

---

#### 4.5.125 Persistence Latency

同步 durability 越强，可能：

```text
latency ↑
```

因此需要区分：

```text
critical durable path
vs
best-effort async path
```

而不是所有数据都采用最昂贵的同步保障。

---

#### 4.5.126 Asynchronous Persistence

有些低风险数据可以：

```text
write buffer
↓
async flush
```

提高性能。

但代价是：

```text
crash window 内可能丢失
```

所以系统必须知道：

```text
哪些字段允许 eventual durability
```

---

#### 4.5.127 Critical vs Best-effort State

可以按重要性分：

```text
Critical Durable State
├── effect ledger
├── approvals
├── task terminal state
├── payment intent
└── budget

Best-effort State
├── UI hint
├── transient scratchpad
├── cached summary
└── low-value telemetry
```

不同类别采用不同 persistence policy。

---

#### 4.5.128 Persistence Policy 本身属于 Harness / Runtime

模型不应该决定：

```text
“这次 payment intent 不落盘吧，省点延迟。”
```

真正的：

```text
what to persist
when to checkpoint
what durability level
how to recover
```

应该由 Harness / Runtime policy 控制。

---

#### 4.5.129 Model 可以建议，但不能掌握 Durability Authority

模型可以输出：

```text
“这个信息以后可能有用。”
```

但最终：

```text
是否写长期 Memory
保存多久
存到哪里
权限是什么
```

不应完全由模型自由决定。

---

#### 4.5.130 Persistence 与 Harness 的关系

Harness 通常负责：

```text
Checkpoint Policy
Memory Write Policy
Retention Policy
Resume Policy
State Transition Policy
Recovery Policy
```

而 Persistence Backend 提供：

```text
Durable Storage Primitive
```

所以：

```text
Persistence Mechanism
≠
Persistence Policy
```

---

#### 4.5.131 Persistence 与 Runtime 的关系

Runtime 更直接负责：

- session lifecycle；
- checkpoint execution；
- durable task state；
- queue / scheduling；
- resume；
- timeout；
- crash recovery；
- concurrent worker coordination。

所以 4.5 属于 Capability 层知识，但实现会深度落在 Chapter 8 Runtime。

---

#### 4.5.132 Persistence 与 Retrieval 的关系

Persistence 回答：

```text
东西活下来了吗？
```

Retrieval 回答：

```text
未来需要时找得到吗？
```

因此：

```text
Durable
≠
Retrievable
```

一个文件可能完好存了十年，但如果没有 index / metadata / identity，Agent 仍然找不到。

---

#### 4.5.133 Persistence 与 Availability 的关系

数据即使 durable：

```text
store unavailable
```

当前也可能读不到。

所以：

```text
Durability
≠
Availability
```

两者需要分别设计与评测。

---

#### 4.5.134 Persistence 与 Integrity

除了：

```text
有没有丢
```

还要关心：

```text
有没有被损坏 / 篡改
```

可以使用：

- checksum；
- content hash；
- version；
- signed receipt；
- integrity constraints。

---

#### 4.5.135 Content Hash

对 immutable artifact / checkpoint，可以保存：

```text
SHA-256(content)
```

恢复时：

```text
recompute
↓
compare
```

帮助发现 corruption / wrong artifact reference。

---

#### 4.5.136 Persistence Corruption

故障不仅是：

```text
missing data
```

还可能是：

```text
partial file
invalid JSON
wrong version
silent corruption
cross-linked record
```

所以 restore 路径要做 validation。

---

#### 4.5.137 Restore Validation

恢复出来的 State 不能直接相信。

至少可以检查：

```text
schema valid?
version supported?
invariants hold?
references exist?
pending effect consistent?
budget non-negative?
terminal state coherent?
```

恢复也是一次 validation boundary。

---

#### 4.5.138 State Invariant 在恢复时尤其重要

例如 invariant：

```text
status = COMPLETED
→ pending_actions must be empty
```

如果恢复出来：

```text
COMPLETED + pending payment
```

说明持久化状态内部已经矛盾。

系统不应盲目继续。

---

#### 4.5.139 Recovery Mode

检测到不一致后，可以进入：

```text
RECOVERING
```

然后：

```text
reconcile
repair state
ask human
abort
```

而不是伪装成普通 RUNNING。

---

#### 4.5.140 Recovery 本身也要 durable

否则：

```text
正在补偿
↓
又 crash
↓
系统忘记已经补偿到哪一步
```

就可能制造二次问题。

所以复杂 recovery workflow 本身也是 long-running durable workflow。

---

#### 4.5.141 Cancellation State

用户取消 long-running Agent 时，需要持久化：

```text
cancel_requested
cancelled_at
pending effects
cleanup state
```

而不是只给某个进程发一个 transient signal。

---

#### 4.5.142 Cancel Requested ≠ Cancelled

和 Tool Execution 一样：

```text
cancel_requested
```

只代表：

```text
系统想停
```

不代表：

```text
所有动作已经停止
所有副作用都没有发生
```

所以 terminal state 必须经过确认。

---

#### 4.5.143 Durable Timer / Schedule

如果 Agent 要：

```text
明天继续
一小时后重试
下周检查
```

不能依赖：

```text
sleep()
```

而应该使用 durable scheduling state：

```text
scheduled_at
job_id
state
```

这会在 Runtime 章节详细展开。

---

#### 4.5.144 Persistence 与 Long-running Task

Long-running Agent 的核心不是：

```text
进程一直跑
```

而是：

> **任务状态可以跨进程存在，执行可以中断并恢复。**

这就是 durable execution 的关键直觉。

---

#### 4.5.145 Durable Execution

所谓 Durable Execution，可以理解为：

```text
逻辑任务生命周期
>
单个进程生命周期
```

进程可以死：

```text
Task 不一定死
```

只要关键状态与 effect history 能正确恢复。

---

#### 4.5.146 Durable Execution ≠ 永不失败

它不是承诺：

```text
任务一定成功
```

而是承诺：

```text
失败 / 重启以后
系统仍然知道自己在哪里
以及应该怎样继续或安全停止
```

---

#### 4.5.147 Deterministic Replay

一些 durable workflow 系统会要求：

```text
workflow logic 可确定性 replay
```

因为历史事件重放时需要得到一致控制流。

而 LLM generation 天然可能：

```text
nondeterministic
```

所以不能简单 replay：

```text
“重新调用模型”
```

来重建过去。

---

#### 4.5.148 Model Output 应作为历史结果保存

如果过去一步模型已经生成：

```text
Plan P
```

replay 时更可靠的是：

```text
replay recorded Plan P
```

而不是：

```text
重新调用模型
期待它再次生成一模一样的 Plan
```

所以：

> **Nondeterministic decisions should often be persisted as events/results.**

---

#### 4.5.149 Tool Result 也可能需要持久化

同样：

```text
search result
API response
filesystem state
```

未来可能变化。

如果为了 audit / replay 需要知道：

```text
当时 Agent 看到了什么
```

则应保存：

```text
raw result / snapshot / hash / provenance
```

而不是重跑 Tool 假装得到历史现场。

---

#### 4.5.150 Replay ≠ Re-execution

非常关键：

```text
Replay
= 重建历史决策 / 状态

Re-execution
= 再次真实执行 Action
```

Replay 时绝不能无意间：

```text
重新发邮件
重新付款
重新删文件
```

所以 replay path 与 live execution path 必须有明确隔离。

---

#### 4.5.151 Simulation / Recorded Tool Mode

为了 debug / evaluation，可以提供：

```text
Recorded Tool Result
```

而不是 live tool。

这样：

```text
trajectory replay
```

不会产生真实 Side Effect。

---

#### 4.5.152 Persistence 与 Reproducibility

如果要复现实验，需要保存：

```text
model version
prompt / harness version
tool catalog
state
observations
random seed if relevant
external evidence snapshot
```

仅保存最终答案不够。

这和 Agent Evaluation 强相关。

---

#### 4.5.153 Persistence 与 Research Artifact

对于研究型 Agent，可额外保存：

```text
trajectory
checkpoint
raw observation
model call metadata
tool call metadata
verdict
cost
latency
```

以支持：

- ablation；
- replay；
- failure analysis；
- audit；
- benchmark regeneration。

---

#### 4.5.154 Persistence 会影响 Benchmark 结果

如果一个 Agent：

```text
跨 case 错误共享 Memory
```

或者：

```text
没有清理 Session State
```

Benchmark 可能产生 contamination。

所以实验协议必须明确：

```text
case isolation
session reset
memory reset
persistent cache policy
```

---

#### 4.5.155 Benchmark Reset Semantics

例如每个 benchmark case 前：

```text
Working State reset
Short-term Memory reset
Long-term Memory frozen / disabled
Cache policy fixed
```

否则不同 run 不可比。

Persistence 本身就是 evaluation protocol 的一部分。

---

#### 4.5.156 Persistent Cache Contamination

即使关闭 Memory，仍可能有：

```text
retrieval cache
tool cache
model response cache
```

跨 case 影响结果。

所以：

> **“Memory off” 不等于“系统没有跨 case persistence”。**

---

#### 4.5.157 Multi-Agent Persistence

Multi-Agent 下，还要保存：

```text
agent identities
ownership
delegation
shared state
private state
handoff state
message history
subtask status
```

否则 parent crash 后可能不知道：

```text
哪些 subagent 已经做过什么
```

---

#### 4.5.158 Shared State 与 Private State

Persistence 层必须保留 scope：

```text
Parent-only
Subagent-only
Shared Workspace
User-visible
```

不能因为都落在同一数据库就失去逻辑隔离。

---

#### 4.5.159 Handoff Persistence

Agent A 把任务交给 Agent B 时，应 durable 记录：

```text
what was delegated
state snapshot / reference
constraints
budget
permissions
handoff time
ownership
```

否则恢复时会出现：

```text
“双主”
```

即 A 和 B 都认为自己仍负责同一 effectful task。

---

#### 4.5.160 Ownership Lease

一种思路是：

```text
某个 worker / agent
暂时拥有 task lease
```

lease 到期后其他 worker 才可接管。

这有助于防止：

```text
两个 worker 同时执行同一任务
```

但 lease 自身也有：

- clock；
- renewal；
- network partition；
- stale owner；

等复杂问题。

---

#### 4.5.161 Fencing Token

仅有 distributed lock 有时不够。

旧 owner 可能锁过期后仍继续写。

Fencing Token 的思想是：

```text
每次 ownership epoch 单调递增
```

资源端拒绝旧 epoch 的写入。

这是更底层的并发可靠性思想，了解概念即可。

---

#### 4.5.162 Persistence Failure Modes

常见失败包括：

1. 状态只在内存，crash 后丢失；
2. checkpoint 太旧；
3. checkpoint 缺关键 effect history；
4. pending action 丢失；
5. UNKNOWN outcome 被恢复成 FAILED；
6. duplicate execution；
7. lost update；
8. stale replica read；
9. schema migration 失败；
10. index 与 canonical store 不一致；
11. cache 被误当 source of truth；
12. backup 从未测试 restore；
13. secret 被持久化进普通 State；
14. cross-tenant persistence leakage；
15. retention 失控；
16. delete 未传播到 index / cache；
17. resume 后不 re-observe Environment；
18. budget / retry count 在 restart 后重置；
19. replay 意外触发 live side effect；
20. approval 状态被错误重放。

---

#### 4.5.163 Failure Localization

当恢复失败时，可以按链路定位：

```text
Was the state written?
        ↓
Was it durably acknowledged?
        ↓
Was the correct version loaded?
        ↓
Was schema migration correct?
        ↓
Were references intact?
        ↓
Were pending effects reconciled?
        ↓
Was environment refreshed?
        ↓
Did resume policy choose correctly?
```

这样不会把所有问题都归因成：

```text
“Agent 不会恢复。”
```

---

#### 4.5.164 Persistence Evaluation：Write Layer

可以测：

```text
Write Success Rate
Durable Ack Accuracy
Write Latency
Conflict Rate
Partial-write Rate
```

---

#### 4.5.165 Persistence Evaluation：Checkpoint Layer

可以测：

```text
Checkpoint Success Rate
Checkpoint Age
Checkpoint Completeness
Checkpoint Size
Checkpoint Restore Time
```

---

#### 4.5.166 Persistence Evaluation：Recovery Layer

可以测：

```text
Recovery Success Rate
State Fidelity after Recovery
Lost-work Amount
Duplicate-effect Rate
Recovery Time
Reconciliation Accuracy
```

---

#### 4.5.167 Persistence Evaluation：Migration Layer

可以测：

```text
Old Schema → New Code
New Schema → Old Reader
Event Replay Compatibility
Checkpoint Upgrade Success
```

---

#### 4.5.168 Persistence Evaluation：Security / Privacy Layer

可以测：

```text
Cross-user Leakage
Unauthorized Restore
Secret Persistence Incident
Delete Propagation Success
Retention Compliance
Backup Access Control
```

---

#### 4.5.169 Persistence Evaluation：End-to-End

最重要的仍然是：

```text
Task running
↓
random crash
↓
restart
↓
resume
↓
correct final outcome?
```

并同时检查：

```text
no duplicate effects
no lost approvals
budget correct
state correct
```

---

#### 4.5.170 Recovery Fidelity

可以定义：

> **恢复后的逻辑状态与“如果系统从未 crash，理论上应有状态”的一致程度。**

这比单纯：

```text
process restarted successfully
```

更有意义。

---

#### 4.5.171 Recovery-induced Harm

恢复本身也可能制造伤害：

```text
duplicate payment
duplicate email
repeated deletion
wrong retry
stale approval reuse
```

所以可以看：

```text
Net Recovery Benefit
=
Recovered Tasks
-
Recovery-induced Harm
```

这和前面的 Reflection / Failure Handling 评价逻辑一致。

---

#### 4.5.172 Minimal Durable State

一个很好的工程问题：

> **恢复当前任务，最少需要 durable 保存什么？**

不是：

```text
“什么都存。”
```

而是：

```text
Minimal Durable State
```

减少：

- storage；
- privacy risk；
- migration complexity；
- write latency。

---

#### 4.5.173 Minimal Durable State ≠ Minimal Context

两者虽然相似，但职责不同：

```text
Minimal Context
= 当前模型正确决策最少要看什么

Minimal Durable State
= 系统正确恢复最少必须保存什么
```

Persistence State 往往比 Model Context 更完整。

---

#### 4.5.174 Persistence by Reference

对于大对象：

```text
不要复制进 State
```

可以保存：

```text
artifact_id
URI
hash
version
```

也就是：

```text
Persist Reference
instead of Payload
```

但前提是引用目标本身也 durable。

---

#### 4.5.175 Dangling Reference

如果 State 保存：

```text
artifact_id = A42
```

但 Artifact 已被删除：

```text
State 仍合法 JSON
却无法恢复语义
```

所以 reference integrity 也必须验证。

---

#### 4.5.176 Garbage Collection

随着任务结束，很多：

```text
temporary artifact
old checkpoint
stale cache
superseded state
```

不再需要。

需要 GC / cleanup policy。

否则 storage 会无限增长。

---

#### 4.5.177 GC 必须理解引用关系

不能看到“旧”就删。

可能：

```text
latest checkpoint
仍引用 old artifact
```

所以安全 GC 需要知道：

```text
reachability / reference graph
```

否则会删掉恢复仍需要的数据。

---

#### 4.5.178 Checkpoint Chain

增量 checkpoint 可能形成：

```text
C1
↓ delta
C2
↓ delta
C3
```

如果 C1 丢失：

```text
C3 也可能无法恢复
```

所以要考虑：

```text
full snapshot frequency
chain length
compaction
```

---

#### 4.5.179 Full vs Incremental Checkpoint

```text
Full Checkpoint
= 保存完整状态

Incremental Checkpoint
= 只保存变化
```

Full：

```text
恢复简单
存储大
```

Incremental：

```text
写入小
恢复链更复杂
```

---

#### 4.5.180 Copy-on-write / Immutable Snapshot 的直觉

对复杂状态，一个安全思路是：

```text
不原地修改旧 snapshot
而创建新 version
```

这样：

```text
旧版本仍可回退
```

也减少 partial overwrite 风险。

---

#### 4.5.181 Persistence 与 Rollback

Rollback 可以指：

```text
恢复到旧持久化版本
```

但要非常小心：

> **State rollback 不能自动回滚真实世界 Side Effect。**

例如：

```text
数据库恢复到发邮件前
```

不代表：

```text
邮件从收件箱里消失
```

---

#### 4.5.182 State Rollback 与 Compensation

所以：

```text
State Rollback
≠
Effect Compensation
```

一个处理内部状态，一个处理真实世界副作用。

恢复流程必须联合考虑两者。

---

#### 4.5.183 Persistence 与 Human-in-the-loop

人在回路中时，等待可能很长。

必须 durable 保存：

```text
question
pending decision
approval scope
submitted options
context references
expiration
```

这样一天后用户回复，系统仍能正确恢复语境。

---

#### 4.5.184 Human Reply 也是 External Event

流程：

```text
WAITING_USER
↓
Persist
↓
Process stops
↓
User replies hours later
↓
Load task
↓
Apply reply
↓
Resume
```

这就是 durable Agent interaction。

---

#### 4.5.185 Long-term Memory Persistence

Long-term Memory 需要的 persistence 属性通常比 Working State 更偏：

```text
versioning
supersession
retention
delete
index consistency
cross-session availability
```

而 Working State 更偏：

```text
low-latency update
transaction
checkpoint
resume
```

同样叫“存储”，需求不同。

---

#### 4.5.186 Short-term Memory Persistence

Short-term Memory 不一定需要和长期 Memory 一样 durable。

例如：

```text
仅当前 session 内重要
```

可以使用较轻 persistence。

但如果 Session 允许跨小时 resume：

```text
Short-term Memory 也必须跨进程存活
```

所以“短期”描述语义寿命，不必然描述存储介质。

---

#### 4.5.187 Ephemeral ≠ Short-term

```text
Ephemeral
= 不承诺跨生命周期存活

Short-term
= 语义上只短时间有用
```

一条 short-term memory 完全可以 durable 保存 24 小时。

一个 in-memory cache 也可能保存很久，只要进程没死。

不要混淆。

---

#### 4.5.188 Persistent ≠ Long-term Memory

反过来也成立。

```text
retry_count
```

可能被 durable 持久化，

但它不是 Long-term Memory。

所以：

```text
Persistent Data
⊃
Long-term Memory
```

---

#### 4.5.189 Coding Agent 示例：可恢复修改仓库

任务：

```text
修复 bug，并保证测试通过
```

执行：

```text
Step 1 读取代码
Step 2 生成 patch
Step 3 修改文件
Step 4 跑 targeted tests
Step 5 跑 full tests
```

在 Step 4 后 crash。

可靠 Persistence 至少应知道：

```text
当前 Git HEAD
已修改文件及版本
已执行测试
测试结果
pending verification
budget
```

恢复后不能：

```text
再次盲目应用同一 patch
```

而应：

```text
load state
↓
inspect current workspace
↓
reconcile diff
↓
continue verification
```

---

#### 4.5.190 Research Agent 示例：长时间研究

任务持续数小时：

```text
搜索论文
阅读 PDF
记录证据
建立引用
写报告
```

Persistence 可以保存：

```text
source registry
read progress
artifact refs
claims
citation mapping
open questions
checkpoint
```

这样进程重启后不用重新从零检索全部材料。

---

#### 4.5.191 Browser Agent 示例：表单提交

高风险点：

```text
点击 Submit
```

执行前：

```text
durable intent
```

执行后如果 timeout：

```text
outcome = UNKNOWN
```

并持久化。

恢复后：

```text
query submission status
```

而不是重新 Submit。

这就是 Persistence + Failure Handling + Side Effects 的联合闭环。

---

#### 4.5.192 Payment Agent 示例

更严格：

```text
prepare payment
↓
persist intent + idempotency key
↓
approval
↓
execute
↓
persist receipt / unknown
↓
reconcile
```

其中任何 crash 都不应让系统失去：

```text
这个逻辑 payment 是否已经尝试过
```

---

#### 4.5.193 Persistence 的工程原则一：先定义 Source of Truth

在设计 store 前先回答：

> **哪个数据源是真相？**

没有这个答案，后面 index、cache、backup、replica 都会变得模糊。

---

#### 4.5.194 工程原则二：按重要性分 Durability Level

不要所有东西：

```text
全部同步 durable
```

也不要：

```text
全部 best effort
```

而要分级。

---

#### 4.5.195 工程原则三：Effectful Action 前后建立 Durable Boundary

高风险操作尤其应该：

```text
checkpoint / intent before
receipt / state after
```

减少 unknown recovery window。

---

#### 4.5.196 工程原则四：把 Unknown 显式保存

不要把：

```text
missing result
```

解释成：

```text
never happened
```

Unknown 本身就是必须持久化的状态。

---

#### 4.5.197 工程原则五：Resume 前 Re-observe Environment

Persistent State 是历史内部认知。

真实世界可能已经变化。

所以：

```text
Restore
≠
Blind Continue
```

---

#### 4.5.198 工程原则六：Nondeterministic Output 要记录

不要依赖：

```text
“以后重新调用模型就能复现。”
```

需要 replay 的关键 model/tool output 应持久保存。

---

#### 4.5.199 工程原则七：Derived Store 必须可重建

Embedding / search index / cache 尽量：

```text
rebuildable from canonical source
```

降低恢复复杂度。

---

#### 4.5.200 工程原则八：恢复路径必须真实演练

没有跑过：

```text
crash → restore → resume
```

就不能假设恢复逻辑可靠。

---

#### 4.5.201 工程原则九：Retention 与 Delete 从第一天设计

不要等数据积累几年以后再问：

```text
“怎么删？”
```

因为 derived index / backup / lineage 会让删除越来越难。

---

#### 4.5.202 工程原则十：Audit 与 Live State 分离

Live State 可以更新。

Audit Trail 应更难被静默覆写。

职责不同。

---

#### 4.5.203 工程原则十一：不要把模型 Context 当 Persistence

模型看见了：

```text
不代表系统持久化了
```

更不代表：

```text
下次进程启动还能恢复
```

---

#### 4.5.204 工程原则十二：不要把数据库存在当成“已可靠”

还要问：

```text
写入确认语义是什么？
backup 可恢复吗？
replica lag 多大？
schema 可迁移吗？
delete 能传播吗？
```

---

#### 4.5.205 工程原则十三：把 Persistence 纳入 Failure Model

设计时主动枚举：

```text
process crash
machine crash
network partition
state store timeout
partial write
stale replica
corrupt checkpoint
schema mismatch
backup failure
```

而不是只考虑 happy path。

---

#### 4.5.206 工程原则十四：恢复后先验证，再继续

Resume 是新的执行边界。

应该：

```text
validate state
reconcile world
check permission
check deadline
check budget
```

再继续。

---

#### 4.5.207 工程原则十五：Persistence 也要最小权限

Agent 不应：

```text
任意读取所有用户 checkpoint
任意覆盖别人的 memory
任意删除 audit records
```

持久化层本身也是权限边界。

---

#### 4.5.208 面试问题：Persistence 和 Memory 的区别？

推荐回答：

> Memory 讨论哪些信息值得跨时间影响未来决策；Persistence 讨论这些 State、Memory、Artifact 和执行证据怎样跨进程、Session、Crash 等生命周期边界可靠存活。Long-term Memory 依赖 Persistence，但 Persistence 还服务于 checkpoint、session、approval、effect ledger、budget、artifact 和 durable execution，因此两者不是同义词。

---

#### 4.5.209 面试问题：Checkpoint 和 Snapshot 有什么区别？

推荐回答：

> Snapshot 是某一时刻状态的映像；Checkpoint 通常是被系统认可为可以恢复执行的状态点，因此除了状态本身，还需要足够的 cursor、pending action、effect history、version、budget、approval 等恢复语义。不是所有 Snapshot 都足够用于 Resume。

---

#### 4.5.210 面试问题：为什么 Agent Resume 不能简单 load checkpoint 后继续？

推荐回答：

> 因为 checkpoint 保存的是历史内部状态，而外部 Environment 可能已经变化；另外还可能存在执行成功但结果未持久化的 Unknown Effect。因此 Resume 前应检查 schema/version，恢复 pending/unknown action，重新观察关键外部状态，做 reconciliation，再验证 plan、approval、budget 和 precondition 后继续。

---

#### 4.5.211 面试问题：Event Log 和 Snapshot 怎么选？

推荐回答：

> Snapshot 读取和恢复快，但历史信息弱；Event Log 保留完整 transition，审计和 replay 强，但重放和 schema evolution 成本高。实际常组合 periodic snapshot + incremental events。是否值得采用完整 Event Sourcing 要看审计、恢复和历史重建价值，不能因为 Agent 有 trajectory 就默认使用。

---

#### 4.5.212 面试问题：为什么 timeout 后恢复很危险？

推荐回答：

> timeout 可能表示请求没有执行，也可能表示已经成功但响应丢失。如果系统没有 durable 保存 action intent、idempotency key 和 UNKNOWN outcome，恢复后很容易把它当成“从未执行”而重复 effectful action。正确做法是持久化 unknown 状态，先 reconciliation，再决定是否 retry。

---

#### 4.5.213 面试问题：数据库已经写成功，为什么还可能不可靠？

推荐回答：

> 因为“数据库写成功”只覆盖一个 store 的写入。系统还可能存在外部 Side Effect、Derived Index、Cache、Replica、Artifact、Backup 和 Schema Compatibility 问题。真正的可靠性要看 crash consistency、read-after-write、恢复语义、effect reconciliation、migration 和 restore 能力，而不是单次 insert 成功。

---

#### 4.5.214 面试问题：Persistence 和 Cache 怎么区分？

推荐回答：

> Cache 的主要目的通常是性能优化，不应被默认当作 source of truth 或唯一恢复来源；Persistence 关注跨生命周期的 durability 与恢复语义。理想情况下 cache 丢失只影响性能，不应破坏 correctness。

---

#### 4.5.215 面试问题：Durability、Availability、Consistency 有什么区别？

推荐回答：

> Durability 关心已经确认的数据会不会因为故障丢失；Availability 关心当前能不能访问；Consistency 关心多个读写方看到的数据关系是否满足约定。Agent 的关键控制状态通常不仅要 durable，还要足够新鲜并在需要时可用，否则依然可能做出错误动作。

---

#### 4.5.216 面试问题：什么是 Durable Execution？

推荐回答：

> Durable Execution 的核心不是让一个进程永远不死，而是让逻辑 Task 生命周期超越单个进程生命周期：关键 State、Event、Timer、Pending Action 和 Effect History 被持久化，进程可以停止、迁移或重启，然后从正确状态继续执行，并避免重复副作用。

---

#### 4.5.217 面试问题：为什么 Replay 不能重新调用模型？

推荐回答：

> 因为 LLM generation 和很多 Tool observation 是 nondeterministic 或随时间变化的。历史 replay 的目标是重建“当时实际发生了什么”，所以关键 model output、tool result 和 environment evidence 应作为历史结果持久保存；重新调用模型属于 re-execution，不是 replay，甚至可能产生不同轨迹。

---

#### 4.5.218 面试问题：为什么 Persistent Data 还需要 Version？

推荐回答：

> 因为持久化数据的寿命可能超过当前代码和模型版本。长任务可能在 v1 创建、v2 恢复；没有 schema version、migration 和 backward compatibility，旧 checkpoint / event / memory 可能无法被新代码正确解释。Persistence 实际上也是长期协议设计。

---

#### 4.5.219 面试问题：怎样测试 Persistence？

推荐回答：

> 不应只测 write/read API。更关键的是在真实执行路径随机注入 crash、timeout、network partition、partial write、stale replica、schema upgrade 等故障，然后 restart、restore、reconcile、resume，检查 state fidelity、lost work、duplicate side effects、budget/approval 保真度和最终 task success。恢复能力必须通过真实演练验证。

---

#### 4.5.220 一句话总结

> **Persistence 是 Agent 的“时间连续性基础设施”：它把易失的 State、Memory、Effect History、Approval、Budget 和 Artifact 变成可跨进程、Session、Crash 与部署边界存活的 durable representation，并通过 checkpoint、version、transaction、reconciliation、migration、retention 与 recovery，让 Agent 在中断之后仍然知道“自己是谁、做到哪了、世界可能发生了什么、接下来怎样安全继续”。**

---

#### 4.5.221 参考资料

进一步学习 Persistence 时，建议优先阅读：

- Martin Kleppmann, *Designing Data-Intensive Applications*：数据模型、复制、一致性、事务、日志、流处理与容错的系统性基础；
- PostgreSQL Documentation：Transactions、WAL、MVCC、Backup / Restore 等数据库持久化基础；
- SQLite Documentation：Atomic Commit、WAL、Crash Recovery，适合理解小型系统中的 durability 语义；
- Temporal Documentation：Durable Execution、Workflow History、Replay、Retry 与 long-running workflow；
- Microsoft Azure Architecture Center：Saga、Transactional Outbox、Compensating Transaction 等分布式一致性模式；
- AWS Builders' Library：timeouts、retries、backoff、idempotency 与 distributed system failure handling；
- Fowler, *Event Sourcing*：事件作为权威历史的基本思想；
- CNCF / distributed systems literature：checkpoint、replication、consistency、recovery 与 stateful service 基础。

这一节的目标不是让你先背某个数据库或工作流框架的 API，而是先建立一个稳定判断：

> **Agent 能“记住”不是因为某个变量还在，而是因为关键状态有明确的 source of truth、durability、version、恢复点、重放/迁移语义，并且在 crash 之后仍能与真实 Environment 正确对账。**
