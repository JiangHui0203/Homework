### 3.6 Tool Execution

#### 3.6.1 定义：Tool Execution 到底是什么？

前面 3.1–3.5 已经完成了：

```text
Tool 是什么
↓
Tool 接受什么结构
↓
模型如何理解 Tool
↓
当前应该选哪个 Tool
↓
具体参数是什么
```

但到这里，Agent 仍然只是**提出了一个 Action Proposal**。

真正的 Tool Execution 发生在：

> **Harness / Runtime 把已经验证、授权的 Tool Call 转交给实际执行环境，并产生可追踪的执行结果、环境变化和后续 Observation。**

因此必须把：

```text
Model Proposal
Validated Action
Executed Action
Environment Effect
Observed Result
Task Success
```

严格区分。

最小执行链：

```text
Model proposes Tool Call
        ↓
Parse / Canonicalize
        ↓
Schema + Semantic Validation
        ↓
Permission / Policy / Approval
        ↓
Execution Admission
        ↓
Runtime Dispatch
        ↓
Tool / API / Process / Sandbox
        ↓
Execution Receipt
        ↓
Environment State Change
        ↓
Observation Construction
        ↓
Verification
```

最重要的一句话是：

> **Tool Call 不是事实，Tool Result 也不自动等于事实；只有 Runtime 真正执行，并且结果与环境状态被验证后，系统才有资格更新“发生了什么”。**

---

#### 3.6.2 Proposed Action ≠ Executed Action

模型生成：

```json
{
  "tool": "send_email",
  "arguments": {
    "recipient": "alice@example.com",
    "subject": "Meeting update"
  }
}
```

只能说明：

```text
Model proposed:
send_email(...)
```

它并不说明：

```text
邮件已经发送
```

中间仍然可能发生：

```text
schema reject
permission denied
human approval pending
rate limit
queue failure
network failure
runtime crash
timeout
cancellation
service unavailable
```

因此日志里至少应区分：

```text
proposed
validated
authorized
accepted
started
succeeded / failed / unknown
verified
```

而不是只有：

```text
tool_called = true
```

---

#### 3.6.3 Execution Admission：真正执行前还有一道门

即使参数已经合法，也不意味着应该立刻执行。

Execution Admission 可以检查：

- permission；
- approval；
- budget；
- rate limit；
- resource availability；
- current state freshness；
- concurrency lock；
- risk policy；
- preconditions；
- idempotency key；
- deadline。

可以写成：

```text
Valid Action
   ↓
Can this action execute now?
   ↓
Yes / No / Wait / Re-resolve / Re-approve
```

所以：

> **Validation 回答“这个 Action 是否合法”，Admission 回答“它现在是否允许进入执行系统”。**

---

#### 3.6.4 Runtime 才是执行主体

模型本身并不会真的：

```text
发送邮件
删除文件
提交订单
执行 shell
修改数据库
点击网页
```

更准确的系统结构是：

```text
LLM
 ↓
Action Proposal
 ↓
Harness
 ↓
Validation / Policy
 ↓
Runtime
 ↓
Actual Tool Implementation
 ↓
Environment
```

因此：

```text
Model = proposes
Harness = controls
Runtime = executes
Environment = changes
```

这条边界后面到 Harness、Runtime、安全章节都会反复使用。

---

#### 3.6.5 Execution Lifecycle：不要只记录 success / failure

一次 Tool Execution 通常有完整生命周期：

```text
CREATED
  ↓
VALIDATED
  ↓
AUTHORIZED
  ↓
QUEUED
  ↓
RUNNING
  ↓
SUCCEEDED
FAILED
TIMED_OUT
CANCELLED
PARTIAL
UNKNOWN
```

有些系统还需要：

```text
WAITING_APPROVAL
RETRYING
ROLLING_BACK
COMPENSATING
```

为什么重要？

因为：

```text
queued ≠ started
started ≠ completed
completed ≠ domain success
```

例如支付 API 已经接受请求：

```text
HTTP 202 Accepted
```

只说明：

```text
request accepted for processing
```

并不说明：

```text
payment succeeded
```

---

#### 3.6.6 Execution Receipt：每次执行都应该有“收据”

建议每次执行返回一个结构化 Execution Receipt：

```json
{
  "call_id": "call_123",
  "tool": "send_email",
  "status": "SUCCEEDED",
  "started_at": "...",
  "finished_at": "...",
  "attempt": 1,
  "idempotency_key": "...",
  "result_ref": "...",
  "side_effects": ["message_created"],
  "error": null
}
```

Execution Receipt 的作用是：

- trace correlation；
- retry deduplication；
- audit；
- recovery；
- billing / cost accounting；
- latency analysis；
- side-effect verification。

注意：

> **Receipt 是“Runtime 说它做了什么”的结构化证据，不等于最终业务真相。**

最终仍可能需要 read-back / environment verification。

---

#### 3.6.7 Call ID：把 Proposal、Execution、Observation 串起来

如果一个 Agent 同时发起多个 Tool Call：

```text
search_web(...)
read_file(...)
calendar.get(...)
```

必须能把返回结果精确对应回原调用。

因此需要：

```text
call_id
request_id
trace_id
span_id
```

最小对应关系：

```text
Decision
 ↓
Tool Call [call_id=42]
 ↓
Execution [call_id=42]
 ↓
Result [call_id=42]
 ↓
Observation [source_call_id=42]
```

否则并发执行时很容易出现：

```text
结果 A 被模型当成 Tool B 的结果
```

这属于严重的 state corruption。

---

#### 3.6.8 Synchronous vs Asynchronous Execution

同步执行：

```text
Agent
 ↓ call
Tool
 ↓ wait
Result
 ↓
Agent continues
```

适合：

- 低延迟读取；
- calculator；
- local file read；
- 快速 API。

异步执行：

```text
Agent
 ↓ submit
Job ID
 ↓
Runtime keeps job running
 ↓
Poll / Event / Callback
 ↓
Completion Observation
```

适合：

- 长时间代码执行；
- 数据处理；
- 大文件任务；
- 外部长流程；
- human approval；
- browser / workflow jobs。

关键区别是：

```text
submit success
≠
job success
```

所以异步 Tool 必须显式区分：

```text
accepted
running
terminal outcome
```

---

#### 3.6.9 Timeout 是最危险的“未知状态”之一

假设：

```text
send_email(...)
```

Runtime 等待 30 秒后 timeout。

有三种真实情况：

```text
A. 请求根本没到服务端
B. 服务端已收到，但还没处理
C. 邮件已经发送，只是响应丢了
```

所以：

```text
TIMEOUT
≠ FAILURE
```

更准确的是：

```text
TIMEOUT
→ execution outcome unknown
```

如果 Agent 此时直接 retry：

```text
send_email again
```

可能造成：

```text
duplicate email
```

因此超时后应该先问：

> **这个 Action 是否可能已经产生副作用？有没有办法查询真实状态？**

---

#### 3.6.10 Retry 不是默认安全操作

很多系统看到：

```text
network error
503
timeout
```

就直接：

```text
retry
```

但 Retry Safety 取决于：

```text
Action semantics
+
Idempotency
+
Observed failure point
+
Environment state
```

读取类 Tool：

```text
get_weather()
```

通常 retry 风险较小。

写入类 Tool：

```text
charge_card()
send_email()
create_order()
```

盲目 retry 可能制造重复副作用。

所以：

> **Retry Policy 必须 side-effect-aware，而不是 transport-error-aware。**

---

#### 3.6.11 Idempotency：同一个操作执行多次是否等价于一次？

如果操作满足：

$$
f(f(s,a),a)=f(s,a)
$$

可以把它理解为对同一状态重复执行相同 Action 不再产生新的业务效果。

例如：

```text
set_status(order, "cancelled")
```

可能具有较强 idempotency。

而：

```text
increment_balance(+100)
send_email()
create_ticket()
```

通常不天然幂等。

工程上常用：

```text
idempotency_key
```

例如：

```text
create_payment(
  amount=100,
  idempotency_key="task123-payment1"
)
```

服务端保证相同 key 重放不会创建第二笔支付。

---

#### 3.6.12 Idempotent Tool ≠ Idempotent Agent Trajectory

即使单个 Tool 幂等，整个轨迹也未必幂等。

例如：

```text
lookup customer
↓
create ticket
↓
send notification
```

其中：

```text
lookup customer   幂等
create ticket     key-based 幂等
send notification 可能不幂等
```

所以重复整个 Agent step 或 episode 仍可能产生额外影响。

因此幂等性需要明确粒度：

```text
Tool-call level
Workflow-step level
Transaction level
Episode level
```

---

#### 3.6.13 At-most-once、At-least-once、Exactly-once：不要轻易说“Exactly Once”

分布式执行常见语义：

**At-most-once**

```text
最多执行一次
可能丢
```

**At-least-once**

```text
至少执行一次
可能重复
```

**Exactly-once effect**

```text
业务上只产生一次效果
```

现实中所谓 exactly-once 往往依赖：

```text
unique key
idempotency key
transaction
state machine
consumer dedup
```

而不是“网络真的只发送了一次”。

所以 Agent 系统里更实用的问题是：

> **怎样做到 externally visible effect effectively once？**

而不是轻易承诺真正物理意义上的 exactly-once execution。

---

#### 3.6.14 Partial Execution：Tool 可能“做了一半”

假设 Tool：

```text
book_trip()
```

内部执行：

```text
book flight   ✅
book hotel    ✅
book car      ❌
```

此时不能简单返回：

```text
FAILED
```

因为世界已经改变了一部分。

更准确的结果：

```json
{
  "status": "PARTIAL",
  "completed": ["flight", "hotel"],
  "failed": ["car"]
}
```

否则 Agent 可能误以为“什么都没发生”，重新执行整个 Tool，造成：

```text
duplicate flight
duplicate hotel
```

所以：

> **Partial execution 必须进入 Agent State。**

---

#### 3.6.15 Atomicity：要么全部发生，要么全部不发生

对于可以由数据库事务包裹的操作，理想语义是：

```text
BEGIN
  write A
  write B
  write C
COMMIT
```

如果中间失败：

```text
ROLLBACK
```

于是：

```text
all-or-nothing
```

但很多真实 Agent Action 跨多个外部系统：

```text
calendar
email
CRM
payment service
```

无法共享一个数据库 transaction。

此时需要：

```text
Saga
Compensating Action
Workflow State Machine
```

---

#### 3.6.16 Rollback 与 Compensation 不一样

Rollback：

```text
操作从未真正提交
→ 回到原状态
```

Compensation：

```text
原操作已经真实发生
→ 再执行另一个动作进行业务补偿
```

例如：

```text
已创建机票订单
```

无法“让历史不存在”。

只能：

```text
cancel ticket
refund payment
```

所以：

```text
Compensation
≠ perfect undo
```

它本身也是新的 Effectful Action，也可能失败。

---

#### 3.6.17 Cancellation：取消请求 ≠ Action 已停止

用户点击“取消”时，真实状态可能是：

```text
queued
running
external side effect already committed
```

因此 cancellation 至少有：

```text
Cancel requested
Cancel acknowledged
Execution stopped
Too late to cancel
Compensation required
```

不能把：

```text
cancel_requested = true
```

直接解释成：

```text
Action 没发生
```

---

#### 3.6.18 Concurrency：两个合法 Action 也可能互相冲突

假设两个 Agent / 两个并发 step 同时读取：

```text
balance = 100
```

然后分别写：

```text
A: withdraw 80
B: withdraw 50
```

单独看每个参数都可能合法。

但合并执行后：

```text
overspend
```

这就是并发状态问题。

常见控制方法：

- optimistic concurrency；
- expected_version；
- compare-and-swap；
- lock；
- transaction；
- serializable queue；
- resource-level mutex。

所以：

> **Argument Validity 是基于某个 State 判断的；Execution 必须确认那个 State 仍然成立。**

---

#### 3.6.19 Race Condition：检查通过到执行之间，世界可能已经变了

经典 TOCTOU：

```text
Time Of Check
   ↓
condition = true
   ↓
... delay ...
   ↓
Time Of Use
   ↓
condition may no longer be true
```

例如：

```text
check order = pending
↓
其他进程发货
↓
refund_order()
```

因此高风险 Tool 应尽量把：

```text
check + mutation
```

放到同一原子操作 / server-side precondition 中。

而不是让 Agent：

```text
先查
过一会儿再写
```

然后假设状态没变。

---

#### 3.6.20 Preconditions 最好由执行端再校验一次

即使 Agent 已经在 reasoning 阶段确认：

```text
order.status == pending
```

执行 Tool 仍应允许：

```text
refund_order(
  order_id="1847",
  expected_status="pending"
)
```

Runtime / backend 再检查：

```text
current status == pending ?
```

不成立则：

```text
PRECONDITION_FAILED
```

这比把所有安全性都寄托在模型最新记忆上可靠得多。

---

#### 3.6.21 Sandbox：代码执行不是普通 Function Call

对于：

```text
run_python(code)
run_shell(command)
execute_notebook(...)
```

风险远高于普通 read API。

Runtime 应考虑：

- filesystem scope；
- network access；
- process limits；
- CPU / GPU limits；
- memory limit；
- wall-clock timeout；
- secret exposure；
- package installation；
- syscall restrictions；
- working directory；
- output size；
- cleanup。

所以：

> **Code Tool 的 Schema 约束不了代码执行的真实能力边界，Sandbox 才是 Runtime 侧的硬边界。**

---

#### 3.6.22 Execution Environment 是实验条件的一部分

同一段代码在：

```text
Python 3.10
Python 3.12
CUDA 12.1
CUDA 12.6
Linux
Windows
```

结果可能不同。

因此 Agent Eval / Coding Agent 应记录：

```text
runtime image
OS
language version
dependency lock
hardware
network policy
filesystem snapshot
```

否则：

```text
同一个 Tool Call
```

不一定意味着：

```text
同一个 execution semantics
```

---

#### 3.6.23 Environment Isolation：不要让实验互相污染

如果多个 benchmark case 共用同一个 Environment：

```text
case A 修改文件
case B 读取文件
```

那么 B 的结果可能依赖 A。

这会破坏：

```text
independence
reproducibility
causal attribution
```

所以常见策略是：

```text
per-case sandbox
snapshot restore
container reset
transaction rollback
database fixture reset
```

这对 Agent benchmark 尤其重要。

---

#### 3.6.24 Tool Execution 与 Side Effects

一次 Action 可能产生：

```text
Primary Effect
Secondary Effect
External Effect
Hidden Effect
```

例如：

```text
calendar.update(event)
```

Primary：

```text
事件时间变化
```

Secondary：

```text
系统自动发送通知
```

External：

```text
第三方 webhook 被触发
```

Hidden：

```text
审计日志 / billing counter 改变
```

所以 Tool Contract 中必须尽量明确：

```text
what changes
what may additionally change
what cannot be rolled back
```

3.9 会进一步系统展开 Side Effects。

---

#### 3.6.25 Read-only 也不是绝对“无副作用”

例如：

```text
GET /messages
```

可能会：

```text
mark_as_read
update last_accessed
consume rate limit
write audit log
trigger billing
```

因此 read-only 最准确的含义应该是：

> **不会改变任务关注的业务资源状态，或其 side effects 已知且可接受。**

不能只根据 HTTP GET / Tool 名称推断安全性。

---

#### 3.6.26 Execution Success ≠ Domain Success

假设：

```text
calendar.update(...)
```

Runtime 返回：

```text
200 OK
```

只能说明：

```text
backend accepted / processed this request
```

但最终还可能：

```text
改错 event
时间错误
参会人通知失败
周会也被误改
状态后来又被覆盖
```

所以：

```text
Transport Success
≠ Execution Success
≠ Domain Success
≠ Task Success
```

这四层要分开。

---

#### 3.6.27 Exit Code 0 也不等于任务成功

Coding Agent 常见：

```text
pytest
→ exit code 0
```

这说明：

```text
这些 tests passed
```

不说明：

```text
public API unchanged
hidden tests pass
performance okay
security okay
requested behavior fully implemented
```

所以 Tool Execution 的 success flag 永远只描述这个 Tool 的执行语义，不应该被提升成整个 Task Completion。

---

#### 3.6.28 Tool Result ≠ Observation

Runtime 可能返回：

```text
20 MB stdout
```

但 Agent Context 不应该机械注入全部内容。

中间还需要：

```text
Raw Tool Result
      ↓
Normalize
      ↓
Filter / Summarize / Structure
      ↓
Attach provenance
      ↓
Observation
```

因此：

```text
Execution produces Result
Harness constructs Observation
Model consumes Observation
```

这正是下一节 3.7 的主题。

---

#### 3.6.29 Error 应该结构化，而不是只返回一段字符串

坏的 Tool Error：

```text
"Something went wrong"
```

更好的：

```json
{
  "status": "FAILED",
  "error_code": "PERMISSION_DENIED",
  "retryable": false,
  "side_effect_possible": false,
  "details": {...}
}
```

或者：

```json
{
  "status": "UNKNOWN",
  "error_code": "TIMEOUT_AFTER_SUBMIT",
  "retryable": "CHECK_STATE_FIRST",
  "side_effect_possible": true
}
```

这样 Agent / Harness 才能区分：

```text
retry
re-authenticate
replan
ask user
check status
compensate
stop
```

---

#### 3.6.30 Retryability 不应该只是 boolean

简单字段：

```json
{"retryable": true}
```

往往不够。

更实用的是：

```text
SAFE_RETRY
RETRY_WITH_BACKOFF
RETRY_AFTER_REFRESH
CHECK_STATE_BEFORE_RETRY
REQUIRES_NEW_APPROVAL
DO_NOT_RETRY
```

原因是：

```text
Transient Failure
```

和：

```text
Unknown Side Effect
```

虽然都可能表现成 timeout，但恢复策略完全不同。

---

#### 3.6.31 Backoff、Jitter 与 Retry Storm

当服务端故障时，如果 1000 个 Agent 同时：

```text
retry immediately
```

可能进一步压垮服务。

因此 Runtime 常需要：

```text
exponential backoff
jitter
retry budget
circuit breaker
```

例如：

```text
1s
2s
4s
8s
```

并加随机 jitter，避免所有客户端同步重试。

---

#### 3.6.32 Circuit Breaker：故障服务不应被无限调用

如果某 Tool 连续失败：

```text
fail
fail
fail
fail
```

Harness / Runtime 可以进入：

```text
OPEN circuit
```

短时间拒绝新的执行请求。

之后：

```text
HALF_OPEN
```

允许少量探测。

恢复后：

```text
CLOSED
```

这避免 Agent 在已知不可用能力上持续浪费预算。

---

#### 3.6.33 Rate Limit 本身也是 Environment Constraint

Tool 可能返回：

```text
429 Too Many Requests
```

这不是：

```text
模型参数错了
```

而是：

```text
当前执行资源受限
```

应进入 State：

```text
available_after
remaining_quota
retry_after
```

然后 Routing / Planning 再决定：

```text
wait
fallback
use alternate Tool
stop
```

---

#### 3.6.34 Deadline 与 Timeout 不一样

Timeout：

```text
单次执行最多等多久
```

Deadline：

```text
整个任务必须在什么时候之前完成
```

例如：

```text
Task deadline = 30s
Tool timeout = 60s
```

显然不合理。

执行前应检查：

```text
remaining_budget
remaining_time
expected_tool_latency
```

如果已经来不及，就不应该启动一个注定超过 deadline 的 Tool。

---

#### 3.6.35 Queue 与 Scheduling 也会改变 Agent 行为

Action 被接受后可能：

```text
立即执行
```

也可能：

```text
进入 queue 30 秒后执行
```

这段时间：

```text
world state may change
permission may expire
approval may become stale
user may cancel
```

所以异步 Tool 需要考虑：

```text
admission-time validation
execution-time revalidation
```

而不是只在入队前检查一次。

---

#### 3.6.36 Approval 也可能过期

假设用户批准：

```text
删除 file A version=123
```

十分钟后文件已变成：

```text
version=456
```

此时执行旧 approval 可能不再安全。

所以 approval 应绑定：

```text
resolved arguments
resource identity
resource version / state
expiry
```

而不是只有：

```text
approved = true
```

---

#### 3.6.37 Secret / Credential 应由 Runtime 管理

模型不应该获得：

```text
API key
OAuth refresh token
database password
cloud secret
```

更合理：

```text
Model chooses capability
      ↓
Harness validates
      ↓
Runtime injects credential
      ↓
Tool executes
```

这样：

```text
Agent can use capability
≠
Agent can read credential
```

这是非常重要的 Least Privilege 设计。

---

#### 3.6.38 Runtime Identity 与 User Identity 要区分

一次请求可能涉及：

```text
user identity
agent identity
service identity
execution identity
```

例如：

```text
User asks Agent
Agent proposes action
Service account executes API
```

系统必须知道：

```text
on whose behalf?
under which permission?
who is accountable?
```

否则审计会非常混乱。

---

#### 3.6.39 Delegation 不能扩大权限

如果 Parent Agent 只有：

```text
read-only permission
```

它创建 Subagent 后，Subagent 不应该突然获得：

```text
write permission
```

同理 Tool Execution 权限应满足：

```text
Delegated Authority
⊆
Parent Authority
```

除非系统有明确的独立授权过程。

---

#### 3.6.40 Parallel Tool Execution：什么时候可以并行？

如果两个 Action 相互独立：

```text
search_web(query A)
search_web(query B)
```

可以并行降低 latency。

但如果：

```text
create_file()
read_file(created_file)
```

第二个依赖第一个结果，不能简单并行。

判断并行至少要考虑：

```text
data dependency
resource conflict
side effects
shared quota
ordering constraint
```

所以：

> **Parallel Tool Calling 是 dependency analysis 问题，不只是模型一次输出多个 call。**

---

#### 3.6.41 Parallel Writes 更危险

两个写操作：

```text
update profile
send notification
```

表面互不依赖。

但如果 notification 内容依赖最终 profile state：

```text
它们实际上有语义依赖
```

因此工程上应区分：

```text
syntactic independence
semantic independence
```

只有后者才真正适合并行。

---

#### 3.6.42 Ordering Constraint

有些 Action 必须严格顺序：

```text
reserve resource
↓
charge payment
↓
confirm booking
```

如果乱序：

```text
charge before reservation
```

可能产生严重业务问题。

因此 Tool Execution 可以显式维护：

```text
predecessor_call_ids
execution DAG
barriers
```

这和 Planning 中的 dependency graph 对接。

---

#### 3.6.43 Side-effect Verification：写成功后最好再确认世界状态

对于高价值 mutation：

```text
update_calendar
write_file
refund_order
```

最可靠流程常是：

```text
Write
 ↓
Execution Receipt
 ↓
Read-back / Query State
 ↓
Verify Expected Effect
```

也就是：

```text
Act
↓
Observe
↓
Verify
```

不要把：

```text
Tool returned success
```

当成终点。

---

#### 3.6.44 Read-after-write Consistency

即使写操作成功，立即读取也可能因为：

```text
replication lag
cache
async propagation
```

暂时看到旧状态。

因此 read-back verification 也要理解系统 consistency model。

例如：

```text
strong consistency
read-your-writes
eventual consistency
```

否则 Agent 可能：

```text
write succeeded
↓
immediate read sees old value
↓
误判失败
↓
重复执行写操作
```

---

#### 3.6.45 Execution Error 与 Domain Rejection 要分开

例如：

```text
refund_order(order_id=1847)
```

返回：

```text
ORDER_ALREADY_SHIPPED
```

这可能表示：

```text
Tool implementation 工作正常
```

只是业务前提不满足。

所以：

```text
Infrastructure Failure
≠ Domain Rejection
```

两者的恢复路径不同：

```text
Infrastructure Failure
→ retry / fallback / backoff

Domain Rejection
→ update state / replan / stop
```

---

#### 3.6.46 Execution Error Taxonomy

可以按层拆分：

```text
Admission Error
├── permission denied
├── approval missing
├── budget exceeded
└── precondition failed

Dispatch Error
├── queue unavailable
├── route failure
└── executor unavailable

Transport Error
├── DNS
├── network timeout
├── connection reset
└── HTTP 5xx

Runtime Error
├── process crash
├── OOM
├── sandbox kill
└── dependency failure

Domain Error
├── resource not found
├── conflict
├── invalid state transition
└── business rule rejection

Outcome Uncertainty
├── timeout after submit
├── lost acknowledgement
└── partial execution
```

这比统一成：

```text
Tool failed
```

有用得多。

---

#### 3.6.47 Failure Localization：Tool 失败不一定是 Tool Implementation 的错

一次失败可能来自：

```text
Model selected wrong Tool
Arguments wrong
Permission policy wrong
Runtime routing wrong
Tool implementation bug
External service down
Environment stale
Observation normalization wrong
```

因此诊断顺序可以是：

```text
1. proposal correct?
2. args correct?
3. authorization correct?
4. executor correct?
5. actual request sent?
6. remote response received?
7. side effect occurred?
8. result mapped correctly?
```

不要看到最终 failure 就直接改 Tool prompt。

---

#### 3.6.48 Execution Observability

建议每次执行至少记录：

```text
call_id
trace_id
tool_name
tool_version
resolved_args_hash
actor / principal
permission_scope
approval_ref
executor
runtime_version
environment_id
start_time
end_time
queue_time
latency
attempt
idempotency_key
status
error_code
side_effect_possible
result_ref
verification_status
```

这样才能支持：

- replay；
- debugging；
- audit；
- latency attribution；
- failure attribution；
- cost accounting；
- incident analysis。

---

#### 3.6.49 Logging 不等于把所有敏感参数明文记录

Execution trace 很重要，但也有数据安全问题。

例如：

```text
password
token
PII
credit card
medical data
```

不应该因为“可观测性”就完整写入日志。

应采用：

```text
redaction
hash / fingerprint
secret reference
field-level access control
retention policy
```

所以：

> **Observability 要足够诊断，但不能成为新的 data exfiltration surface。**

---

#### 3.6.50 Deterministic Tool ≠ Deterministic Execution

一个 Tool implementation 本身可能是确定性的：

```text
calculate(expression)
```

但整体 Execution 仍可能受到：

```text
runtime version
floating point
concurrency
time
environment
external state
random seed
hardware
```

影响。

所以实验复现要冻结的不只是：

```text
Tool code
```

还包括：

```text
Execution Environment
```

---

#### 3.6.51 Nondeterministic Tool 要怎样评价？

例如：

```text
web_search
recommendation API
LLM-based Tool
```

输出本身可能变化。

评测时不能只存：

```text
Tool Name + Args
```

最好同时保存：

```text
actual response
response timestamp
provider version
request metadata
```

否则后续无法区分：

```text
Agent decision changed
```

还是：

```text
Tool world changed
```

---

#### 3.6.52 Replay：重放 Tool Call 有多种语义

**Live Replay**

```text
重新真正调用 Tool
```

可能得到不同结果，也可能再次产生副作用。

**Recorded Replay**

```text
直接返回历史 Tool Result
```

更可复现，但不反映当前环境。

**Simulated Replay**

```text
在 sandbox / simulator 中重建结果
```

因此实验必须说明：

```text
live / recorded / simulated
```

不能都叫 replay。

---

#### 3.6.53 Tool Execution 与 Benchmark 污染

真实 Tool Eval 如果访问：

```text
live web
shared database
mutable repo
```

会出现：

```text
environment drift
state leakage
cross-case contamination
```

因此 benchmark 设计往往需要：

```text
frozen snapshot
sandbox
mock service
replay fixture
controlled environment
```

否则 Agent 版本差异和 Environment 差异混在一起。

---

#### 3.6.54 Execution Cost

Tool Execution 也有真实成本：

```text
API fee
compute
browser time
GPU
storage
network
human approval
external transaction fee
```

所以 Agent cost 不能只看 model tokens。

可以写成：

$$
C_{task}=C_{model}+C_{tool}+C_{runtime}+C_{human}+C_{external}
$$

这和 1.8 的 Budget 直接连接。

---

#### 3.6.55 Execution Latency

Tool latency 应拆成：

```text
queue latency
setup latency
network latency
service latency
execution latency
verification latency
```

否则只看 end-to-end latency，很难优化。

例如 Coding Agent 慢，可能不是模型慢，而是：

```text
container startup = 18s
pytest = 22s
model = 2s
```

优化方向完全不同。

---

#### 3.6.56 Tail Latency 比平均值更容易毁掉 Agent 体验

如果 Tool：

```text
p50 = 500ms
p95 = 6s
p99 = 30s
```

平均值可能还不错，但多步 Agent 连续调用多个 Tool 时：

```text
一次长尾
```

就会显著拖慢整个 trajectory。

因此应跟踪：

```text
p50 / p90 / p95 / p99
```

并结合：

```text
critical path
```

分析。

---

#### 3.6.57 Parallelism：降低 latency 可能增加 cost 和 failure surface

并行两个搜索：

```text
wall-clock latency ↓
```

但同时：

```text
API cost ↑
context volume ↑
conflicting evidence ↑
rate-limit risk ↑
```

所以：

> **Parallelism 是 latency–cost–complexity trade-off，不是免费加速。**

---

#### 3.6.58 Execution Budget Guard

Runtime 层可以硬限制：

```text
max_tool_calls
max_parallel_calls
max_runtime_seconds
max_compute
max_external_cost
max_write_actions
max_retries
```

这些限制不应该只依赖模型“记得节省”。

这正是：

```text
Prompt soft guidance
vs
Runtime hard enforcement
```

的又一个例子。

---

#### 3.6.59 Tool Execution 与 Human Approval

Human Approval 最合理的位置通常是：

```text
Resolved Final Action
       ↓
Approval
       ↓
Execution
```

而不是：

```text
模糊计划
↓
提前批准所有未来 Action
```

高风险 Action 应展示：

```text
what
which resource
which exact arguments
expected effect
risk / irreversibility
```

让批准真正对应将执行的内容。

---

#### 3.6.60 Approval 不是替代验证

用户批准：

```text
删除 file A
```

不代表：

```text
Tool 一定删对了 file A
```

所以仍然需要：

```text
execute
↓
observe
↓
verify
```

Human Approval 解决的是：

```text
authority
```

Verification 解决的是：

```text
correct outcome
```

不能互相替代。

---

#### 3.6.61 Tool Execution 与 Planning

Planning 决定：

```text
应该有哪些 Action，以及依赖顺序
```

Execution 决定：

```text
某一个已经批准的 Action 怎样真实发生
```

所以：

```text
Plan Step
≠
Execution Record
```

一个 Plan Step 可以：

```text
尚未执行
执行中
失败
部分成功
完成
取消
```

必须由 Runtime State 维护，而不是让模型文字描述代替真实执行状态。

---

#### 3.6.62 Tool Execution 与 ReAct

ReAct 的结构是：

```text
Reasoning
↓
Action
↓
Observation
```

Tool Execution 位于：

```text
Action
↓
[Execution]
↓
Observation
```

因此 ReAct 中的 `Action → Observation` 不是一个瞬时箭头，中间实际包含：

```text
validation
authorization
runtime execution
error handling
result normalization
```

工程系统就是把这个箭头展开。

---

#### 3.6.63 Harness 与 Runtime 的职责边界

一个实用划分：

**Harness**：

```text
是否允许执行？
何时执行？
失败后如何决策？
是否 retry / fallback / ask / stop？
怎样把结果变成 Observation？
```

**Runtime**：

```text
在哪执行？
用什么 credential？
如何调度？
怎样 timeout / cancel？
如何隔离？
如何持久化执行状态？
真实 Tool 结果是什么？
```

可以总结为：

```text
Harness = execution policy
Runtime = execution mechanism
```

---

#### 3.6.64 Tool Implementation 与 Runtime 也不是同一个东西

例如：

```text
send_email()
```

Tool Implementation 定义：

```text
如何构造并发送邮件请求
```

Runtime 负责：

```text
credential
network
retry policy enforcement
process isolation
timeout
logging
call tracking
```

所以：

```text
Tool Implementation
⊂
Execution Stack
```

---

#### 3.6.65 一个 Coding Agent 的完整 Execution 例子

任务：

```text
修复 parser.py，使 tests 通过，但不能改变 public API。
```

Tool Call：

```text
write_file(
  path="parser.py",
  expected_version="abc123",
  patch=...
)
```

执行链：

```text
1. Schema Validation
2. path allowed?
3. write permission?
4. expected_version == current_version?
5. acquire file lock / optimistic guard
6. apply patch in sandbox
7. persist file
8. return new_version=def456
9. read-back / diff
10. run targeted tests
11. run API compatibility check
12. update Agent State
```

如果第 4 步失败：

```text
STALE_STATE
```

此时正确动作通常不是：

```text
blind retry same patch
```

而是：

```text
re-read file
↓
rebase reasoning
↓
regenerate patch
```

---

#### 3.6.66 一个 Calendar Agent 的 Execution 例子

用户：

```text
把明天下午三点的产品组会议改到周五下午三点，但周会不要动。
```

最终 Action：

```text
calendar.update(
  event_id="evt_product_123",
  expected_version="v17",
  new_start="2026-10-23T15:00:00+09:00"
)
```

Runtime 执行前检查：

```text
permission
approval if required
event_id still exists
version == v17
new time valid
```

执行后：

```text
receipt: SUCCEEDED
```

仍要验证：

```text
Event A = Friday 15:00
Event B = unchanged
```

如果系统自动发通知，还要把它当成 Side Effect 纳入结果。

---

#### 3.6.67 一个 timeout 后正确恢复的例子

```text
refund_order(1847)
↓
TIMEOUT_AFTER_SUBMIT
```

错误恢复：

```text
retry refund_order(1847)
```

正确思路：

```text
TIMEOUT_AFTER_SUBMIT
↓
side_effect_possible = true
↓
get_refund_status(1847)
↓
if refund exists:
    treat as already executed
else:
    retry with same idempotency key
```

这就是：

> **Recovery 要基于真实 execution semantics，而不是基于错误字符串。**

---

#### 3.6.68 Tool Execution Failure Modes

**1. Proposal-as-fact**

模型生成 Tool Call 后就告诉用户“已完成”。

**2. Validation bypass**

参数未完整校验直接进入 executor。

**3. Authorization bypass**

模型能看到 Tool 就能执行。

**4. Stale precondition**

检查时合法，执行时状态已变化。

**5. Blind retry**

timeout 后直接重复 effectful action。

**6. Missing idempotency**

重试造成 duplicate side effect。

**7. Partial-success collapse**

部分执行被压成单一 FAILED。

**8. False success**

HTTP 200 被解释为任务成功。

**9. Lost correlation**

并行 Tool Result 对错 call_id。

**10. Cancellation illusion**

cancel requested 被当成 action 未发生。

**11. Race condition**

并发写覆盖或违反 invariant。

**12. No execution-time revalidation**

长队列后仍使用旧 permission / version / approval。

**13. Unsafe parallel writes**

存在隐藏语义依赖却并发执行。

**14. Secret leakage**

把 runtime credential 暴露给模型或日志。

**15. Environment contamination**

不同 benchmark case 共用 mutable state。

**16. Retry storm**

故障时无限或同步重试。

**17. Missing resource guard**

代码执行无限 CPU / memory / output。

**18. Receipt without verification**

只信 Runtime receipt，不核对 Environment。

**19. Observation mismatch**

Tool 已执行，但返回给模型的 observation 错了。

**20. Duplicate completion claim**

同一 Action 多 attempt 后，Agent 无法识别哪一个真正生效。

---

#### 3.6.69 Tool Execution 的评价指标

至少可以分成六层。

**Admission**

```text
Unauthorized Execution Rate
Rejected-valid Action Rate
Stale-precondition Catch Rate
Approval Compliance
```

**Runtime Reliability**

```text
Execution Success Rate
Timeout Rate
Crash Rate
Queue Failure Rate
```

**Semantics**

```text
Idempotency Violation Rate
Duplicate Effect Rate
Partial-state Detection Rate
Cancellation Correctness
```

**Efficiency**

```text
Tool Latency p50/p95/p99
Queue Time
Retry Count
Tool Cost
Runtime Cost
```

**Safety**

```text
Unauthorized Side-effect Rate
Sandbox Escape Rate
Secret Exposure Rate
Cross-case Contamination Rate
```

**End-to-End**

```text
Verified Effect Rate
Task Success Rate
False-success Claim Rate
Recovery Success Rate
```

---

#### 3.6.70 一个非常重要的指标：False-success Claim Rate

Agent 系统最危险的一类错误不是：

```text
“我执行失败了。”
```

而是：

```text
实际没完成
但告诉用户“已经完成”
```

所以应该单独统计：

$$
\text{False Success Rate}
=
\frac{\text{Claimed Success but Environment Not Successful}}
{\text{Claimed Success}}
$$

对于写操作、高风险业务，这个指标非常重要。

---

#### 3.6.71 Execution Evaluation 要冻结 Runtime 条件

比较两个 Agent 时，如果：

```text
Agent A 用 fast service
Agent B 用 degraded service
```

最终 success / latency 不能直接归因给模型。

因此实验协议应记录：

```text
tool version
runtime image
external provider
service snapshot
retry policy
rate-limit state
sandbox config
network policy
```

尽量把 Runtime variance 与 Model variance 分开。

---

#### 3.6.72 Fault Injection：可靠性不能只在“系统正常时”测

可以主动注入：

```text
timeout
429
500
partial response
stale version
permission revoked
process kill
network partition
slow service
malformed result
```

观察 Agent 是否：

```text
blind retry
misclaim success
replan
fallback
verify
stop safely
```

这比只测 happy path 更能看出 Agent 工程质量。

---

#### 3.6.73 Side-effect Simulation / Dry Run

高风险 Tool 可以支持：

```text
dry_run=true
preview=true
```

让系统先返回：

```text
would change X
would notify Y
estimated cost Z
```

再：

```text
approve
↓
execute
```

注意：

```text
Dry Run
≠ guaranteed future execution result
```

因为世界状态可能随后变化。

---

#### 3.6.74 Two-phase Action Pattern

对于危险 Action，可以使用：

```text
Prepare
  ↓
Return resolved effect
  ↓
Approve / Validate
  ↓
Commit
```

例如：

```text
prepare_delete(path)
↓
resolved file + hash + impact
↓
approval
↓
commit_delete(token)
```

这能把：

```text
intent resolution
```

和：

```text
irreversible commit
```

分开。

---

#### 3.6.75 Execution Token / Capability Token

Prepare 阶段可以产生：

```text
short-lived execution token
```

绑定：

```text
exact action
exact resource
exact arguments
expiry
approval
```

Commit 阶段只能执行这个已解析 Action。

这样可以减少：

```text
approval 后参数漂移
```

以及模型再次生成危险参数的机会。

---

#### 3.6.76 Tool Execution 与 Security Boundary

最终真正能够改变世界的，不是模型输出文本，而是：

```text
Runtime accepting an Action
```

所以安全边界应放在：

```text
Model Proposal
      ↓
Untrusted
      ↓
Validation / Policy / Authorization
      ↓
Trusted Execution Boundary
      ↓
Runtime
```

可以记成：

> **Model-generated Action is an untrusted proposal until Runtime admits it.**

---

#### 3.6.77 Capability Security 的核心不是“模型会不会听话”

真正的系统安全不应依赖：

```text
“请不要调用危险工具”
```

而应依赖：

```text
Tool exposure
Permission scope
Argument validation
Approval
Sandbox
Runtime policy
Audit
```

即：

```text
Soft Instruction
      ↓
不能替代
      ↓
Hard Enforcement
```

---

#### 3.6.78 Execution Policy 也是 Harness Policy

例如：

```text
read Tool → auto execute
write Tool → validation
high-risk Tool → approval
destructive Tool → preview + approval
unknown outcome → status check before retry
```

这些不是模型本身的 capability，而是 Harness 对执行路径的政策。

---

#### 3.6.79 Tool Execution 数据可以反过来改进 Agent

日志中可以提取：

```text
selection correct but execution failed
argument correct but stale state
blind retry
unnecessary retry
partial success handled correctly
safe fallback
correct compensation
false success claim
```

这些数据可以用于：

- failure analysis；
- regression set；
- retry-policy optimization；
- Tool redesign；
- Harness improvement；
- SFT / preference data；
- evaluator calibration。

所以 execution trace 本身也是非常高价值的数据资产。

---

#### 3.6.80 工程设计原则

**原则 1：Model Proposal 永远不等于 Executed Action。**

执行必须经过显式 runtime boundary。

**原则 2：写操作的 retry 必须先理解 side-effect semantics。**

不要把 timeout 当成天然失败。

**原则 3：为 effectful Tool 设计 idempotency。**

尤其是 create / send / pay / submit 类操作。

**原则 4：Partial Success 必须成为一等状态。**

不要压扁成 boolean。

**原则 5：高风险 precondition 在执行端再验证。**

避免 TOCTOU。

**原则 6：Execution Receipt 必须可关联、可审计。**

至少保留 call_id、attempt、status、error、side-effect metadata。

**原则 7：Runtime 管 Credential，模型只拿 Capability。**

不要让 Agent 直接持有 secrets。

**原则 8：并行执行必须基于真实依赖关系。**

不是“能一起发”就等于“应该一起发”。

**原则 9：Mutation 后优先做 Environment Verification。**

Tool success flag 不是最终证据。

**原则 10：实验必须冻结或记录 Runtime。**

否则结果无法正确归因。

**原则 11：错误必须结构化。**

让 Harness 能区分 retry、refresh、replan、compensate、stop。

**原则 12：硬 Budget Guard 放在 Runtime。**

不要依赖 Prompt 提醒模型节省。

**原则 13：把 unknown outcome 明确表示为 UNKNOWN。**

不要强行二值化为失败。

**原则 14：高风险 Tool 优先支持 preview / prepare / commit。**

缩小 irreversible action 的不确定性。

**原则 15：最终安全边界是 Execution Admission。**

模型输出永远只是未信任的动作提议。

---

#### 3.6.81 面试掌握边界

**Q1：Tool Call 和 Tool Execution 有什么区别？**

Tool Call 是模型提出的结构化 Action；Tool Execution 是 Runtime 真正让这个 Action 对 Environment 生效。

**Q2：为什么 timeout 不能直接当 failure？**

因为请求可能已经产生副作用，只是 acknowledgement 丢失；此时 outcome 是 UNKNOWN。

**Q3：为什么 effectful Tool 不能 blind retry？**

因为重复执行可能产生 duplicate side effects，应先考虑 idempotency 和真实环境状态。

**Q4：什么是 idempotency key？**

一个稳定请求标识，使重复提交同一逻辑操作时，服务端复用原结果或阻止重复 effect。

**Q5：Partial Success 为什么重要？**

因为 Tool 可能已经改变一部分世界状态；若误判成完全失败，重试可能造成重复操作。

**Q6：Rollback 和 Compensation 有什么区别？**

Rollback 撤销未提交事务；Compensation 是对已经发生的业务效果执行新的反向 / 补偿 Action。

**Q7：为什么 Argument Validation 通过后执行端还要检查 precondition？**

因为 Check 与 Use 之间环境可能变化，存在 TOCTOU / stale state。

**Q8：HTTP 200 为什么不等于任务成功？**

它只说明请求在某个协议层成功处理，不证明业务目标、约束和最终 Environment State 全部正确。

**Q9：什么时候可以 parallel tool execution？**

只有在不存在数据依赖、资源冲突、顺序约束和隐藏语义依赖时才安全。

**Q10：为什么 Tool Result 不等于 Observation？**

Result 是 Runtime 原始输出；Observation 是 Harness 选择、规范化、带 provenance 后真正送给模型的表示。

**Q11：Harness 和 Runtime 在执行上分别负责什么？**

Harness 负责执行政策与恢复决策；Runtime 负责真实调度、隔离、credential、timeout、持久化与执行机制。

**Q12：Exactly once 是否容易实现？**

真正的 exactly-once 很难，工程上通常通过 idempotency、unique key、事务和 dedup 实现 effectively-once effect。

**Q13：如何防止 Agent 的 credential 泄露？**

模型只获得 Capability，credential 由 Runtime 在 trusted boundary 内注入。

**Q14：怎样验证一个 write Tool 真正成功？**

Execution Receipt 后再 read-back / query Environment，并检查 expected postcondition 和 forbidden side effects。

**Q15：Tool Execution 最危险的错误是什么？**

通常不是显式失败，而是实际未成功或状态未知，却向用户声称已经成功，或者 blind retry 导致重复副作用。

---

#### 3.6.82 一句话总结

> **Tool Execution 是 Agent 从“决定要做什么”跨入“真实世界发生变化”的可信执行边界：模型输出只是未信任的 Action Proposal，Harness 负责验证与执行政策，Runtime 负责真实调度和隔离；可靠系统必须显式处理 lifecycle、timeout、unknown outcome、idempotency、partial execution、concurrency、cancellation、transaction / compensation、credential、sandbox 与 execution receipt，并在写操作后用 Environment Verification 证明效果，而不能把 HTTP 200、exit code 0 或 Tool 的 `success=true` 直接当成任务完成。**

---

#### 3.6.83 参考资料

- Kleppmann M. **Designing Data-Intensive Applications**. O'Reilly, 2017. 用于理解 retry、replication、consistency、transactions、idempotency 与分布式执行语义。
- Fowler M. **Patterns of Enterprise Application Architecture**. Addison-Wesley, 2002. 用于理解事务、并发控制与企业系统中的执行边界。
- Richardson C. **Microservices Patterns**. Manning, 2018. 用于理解 Saga、Compensating Transaction、消息投递与跨服务业务一致性。
- OpenTelemetry. **Trace / Span Semantic Concepts**. 用于理解 call correlation、trace_id / span_id、执行可观测性与端到端 tracing。
- OpenAI. **Function Calling / Tools documentation**. 用于理解模型产生 Tool Call 与应用侧负责实际执行之间的接口边界。
- Anthropic. **Tool use documentation**. 用于理解 Tool-use block 与 client / application 执行 Tool 后返回结果的职责分离。
