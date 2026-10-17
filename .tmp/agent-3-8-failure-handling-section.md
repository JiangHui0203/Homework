### 3.8 Failure Handling

#### 3.8.1 定义：Failure Handling 到底是什么？

前面 3.1–3.7 已经把 Tool Use 链条拆成了：

```text
Tool Definition
    ↓
Tool Schema
    ↓
Tool Description
    ↓
Tool Selection
    ↓
Argument Generation
    ↓
Tool Execution
    ↓
Observation
```

但真实 Agent 系统不会只沿着“成功路径”运行。任何一层都可能失败：

```text
选错 Tool
参数错误
权限不足
Tool unavailable
请求超时
执行部分成功
结果未知
Observation 过期
结果被截断
环境状态冲突
Verification 不通过
```

因此 Failure Handling 不是一个简单的：

```python
try:
    execute()
except Exception:
    retry()
```

更准确地说：

> **Failure Handling 是 Agent 系统对异常、错误、拒绝、冲突、不确定结果与目标未达成进行检测、分类、恢复、验证和终止决策的完整控制过程。**

标准链路可以写成：

```text
Failure / Anomaly
      ↓
Detect
      ↓
Classify
      ↓
Assess
├── Retryable?
├── Recoverable?
├── Side effect happened?
├── State still fresh?
├── Need new evidence?
└── Risk / cost acceptable?
      ↓
Choose Recovery
├── Retry
├── Repair
├── Fallback
├── Reroute
├── Replan
├── Rollback
├── Compensate
├── Ask User
├── Human Escalation
└── Abort
      ↓
Execute Recovery
      ↓
Re-observe
      ↓
Verify
      ↓
Continue / Escalate / Stop
```

最重要的一句话是：

> **失败处理的核心不是“再试一次”，而是先判断“究竟失败在什么层、世界已经发生了什么、下一步哪种恢复动作才不会造成二次伤害”。**

---

#### 3.8.2 Failure、Error、Exception、Rejection、Unknown Outcome 不要混在一起

这些词在工程里常常被混用，但语义不同。

**Exception** 通常指程序执行过程中抛出的控制流异常：

```text
TimeoutError
ConnectionError
ValueError
PermissionError
```

它是一种实现层信号，不一定等于业务失败。

**Error** 表示某个层面出现不符合预期的状态，例如：

```text
invalid argument
HTTP 500
schema violation
parse error
```

**Rejection** 表示系统明确拒绝执行：

```text
PERMISSION_DENIED
POLICY_BLOCKED
APPROVAL_REQUIRED
RATE_LIMITED
CONFLICT
```

它不一定表示系统“坏了”，而可能是正常策略结果。

**Failure** 表示某个预期目标没有达到，例如：

```text
Tool execution failed
Plan step failed
Verification failed
Task failed
```

**Unknown Outcome** 表示当前系统不知道真实效果是否已经发生：

```text
request timeout after submit
connection dropped after server accepted request
callback missing
```

它既不是已知成功，也不是已知失败。

因此：

```text
Exception
≠ Error
≠ Rejection
≠ Failure
≠ Unknown Outcome
```

这一区分会直接决定 Recovery Policy。

---

#### 3.8.3 Failure Handling 首先是 Failure Localization

当用户看到：

```text
Agent 没完成任务
```

最差的诊断方式是：

```text
模型不够聪明。
```

成熟系统应该先做 failure localization：

```text
Task Failure
    ↓
Which Layer?
├── Capability Missing
├── Tool Selection
├── Argument Generation
├── Validation / Authorization
├── Runtime Execution
├── Observation
├── State Update
├── Planning / Routing
├── Verification
└── Termination
```

例如“邮件没发出去”可能分别来自：

```text
1. Agent 根本没选 send_email
2. recipient 解析错
3. permission denied
4. SMTP timeout
5. 邮件已发出但 Observation 丢失
6. Observation 被模型误读为 failure
7. Agent 盲目 retry，发了两封
8. 最终 verification 没检查 delivery state
```

如果 failure localization 错了，后续 repair 往往也会错。

所以：

> **Recovery Quality 的上限首先由 Failure Diagnosis 决定。**

---

#### 3.8.4 Failure Taxonomy：按失败层分类

可以把 Tool / Agent failure 粗略分成以下几层：

```text
A. Intent / Goal Failure
B. Selection Failure
C. Argument Failure
D. Validation / Authorization Failure
E. Execution Failure
F. Observation Failure
G. State Consistency Failure
H. Planning / Routing Failure
I. Verification Failure
J. Termination Failure
K. Infrastructure Failure
L. Safety / Security Failure
```

每一种 failure 对应不同恢复动作。

例如：

```text
Argument invalid
→ repair arguments

Tool unavailable
→ fallback / reroute

State stale
→ re-observe

Plan invalid
→ replan

Permission denied
→ request approval / escalate

Unknown outcome
→ query status before retry
```

因此不要设计一个统一的：

```text
on_error → retry
```

---

#### 3.8.5 Retryability 与 Recoverability 是两回事

**Retryable** 问的是：

> 同一个动作重新执行一次，是否有合理概率成功？

**Recoverable** 问的是：

> 即使不能直接重试，系统是否仍然有其他路径继续完成目标？

例如：

```text
Tool A permanently unavailable
```

可能：

```text
retryable = false
recoverable = true
```

因为可以 fallback 到 Tool B。

相反：

```text
send_email timeout
```

技术上也许可以 retry，但如果结果未知、且发送邮件不是幂等操作：

```text
retryable = unsafe / conditional
```

因此：

```text
Retryability
≠
Recoverability
```

---

#### 3.8.6 Retry：什么时候才是真的“再试一次”？

Retry 的定义应该很严格：

> **在逻辑意图基本不变的情况下，对同一个或等价 Action 再次尝试执行。**

例如：

```text
GET /resource
→ transient network error
→ retry same request
```

但下面这些不是纯 Retry：

```text
改参数再调用
→ Repair

换 Tool
→ Fallback / Reroute

改变计划
→ Replan

先重新读取状态再执行
→ Re-observe + Retry / Repair
```

这一边界非常重要，否则系统统计里所有恢复都被粗暴记成 retry，失去诊断价值。

---

#### 3.8.7 Retry 必须满足哪些条件？

至少应检查：

```text
1. Failure 是否 transient？
2. Action 是否幂等？
3. 真实 effect 是否已知？
4. Current State 是否仍然有效？
5. Retry 是否会造成重复副作用？
6. Retry budget 是否允许？
7. Backoff 是否需要？
8. 是否已经连续无进展？
```

可以写成：

```text
Retry Safe
=
Retryable Failure
∧ Effect Semantics Known
∧ State Valid
∧ Budget Available
∧ Duplicate Risk Acceptable
```

因此：

> **“报错了”从来不是 Retry 的充分条件。**

---

#### 3.8.8 Blind Retry 为什么危险？

例如：

```text
charge_card($100)
↓
timeout
```

如果 Harness 立即：

```text
retry charge_card($100)
```

可能产生 double charge。

因为 timeout 只说明：

```text
caller 没在 deadline 前拿到结果
```

不说明：

```text
server 没执行
```

更合理的是：

```text
timeout / unknown
    ↓
query transaction status
    ↓
if not executed
    → retry
else
    → continue
```

所以：

> **Unknown Outcome 应优先 Status Reconciliation，而不是 Blind Retry。**

---

#### 3.8.9 Retry Budget

没有预算的 Retry 很容易变成 retry storm。

常见限制包括：

```text
max_attempts
max_retry_time
max_retry_cost
per-tool retry budget
global episode retry budget
```

同时可以记录：

```text
attempt_count
last_error
first_failure_time
cumulative_wait
cumulative_cost
```

Retry 不是无限资源。

---

#### 3.8.10 Backoff 与 Jitter

对于瞬时服务故障或 rate limit：

```text
retry immediately
retry immediately
retry immediately
```

通常会让问题更严重。

因此常见策略是：

```text
Exponential Backoff
+
Jitter
```

例如：

```text
1s
2s
4s
8s
```

再加入随机扰动，避免大量 Agent 同时重试形成 thundering herd。

但要注意：

> **Backoff 解决“什么时候重试”，不解决“这个 Action 本身是否安全重试”。**

---

#### 3.8.11 Repair：不是重试，而是修正 Action

Repair 是：

> **根据 failure evidence 修正参数、结构、输入、状态或局部步骤，再生成新的 Action。**

例如：

```text
Tool: create_event
Error: end_time must be after start_time
```

合理恢复：

```text
修正 end_time
→ validate
→ execute new action
```

这不是 Retry，因为 Action 已经发生变化。

典型 Repair 包括：

```text
Argument Repair
Query Reformulation
Path Correction
Format Repair
Entity Re-resolution
State Refresh
Patch Revision
```

---

#### 3.8.12 Error Message 必须足以支持 Repair

如果 Tool 只返回：

```text
ERROR
```

模型几乎无法进行有效修复。

更好的 structured error：

```json
{
  "status": "invalid_argument",
  "field": "end_time",
  "reason": "must_be_after_start_time",
  "retryable": false,
  "current_value": "14:00",
  "related_field": {
    "start_time": "15:00"
  }
}
```

这样 Agent 可以进行 targeted repair。

因此：

> **Error Observation 的质量直接决定 Recovery 的质量。**

---

#### 3.8.13 Fallback：换一个实现路径

Fallback 表示：

> **当前首选 capability / implementation 不可用或不适合时，切换到预先允许的替代路径。**

例如：

```text
primary_search_api unavailable
→ fallback_search_api
```

Fallback 通常意味着：

```text
Goal 不变
Capability category 基本不变
Implementation path 变化
```

这和 Replan 不一样。

---

#### 3.8.14 Fallback 不是“什么能跑就用什么”

替代 Tool 必须重新检查：

```text
Capability equivalence
Permission scope
Data freshness
Output semantics
Cost
Latency
Privacy
Jurisdiction
Side effects
```

例如主 Tool 是 internal_customer_db，不能因为失败就随便 fallback 到 public_web_search，因为能力语义、数据权限、隐私边界完全不同。

因此：

> **Fallback 必须是 policy-approved equivalence，而不是 opportunistic substitution。**

---

#### 3.8.15 Reroute：把当前任务交给另一条能力路径

Reroute 与 Fallback 相近，但更强调动态 routing decision。

例如：

```text
small model route
↓
confidence too low
↓
reroute to stronger model
```

或：

```text
general agent
↓
domain-specific failure
↓
reroute to finance agent
```

它通常由 Router / Supervisor / Harness Policy 触发。

---

#### 3.8.16 Replan：局部失败已经破坏了未来计划

如果 failure 只影响当前 Action，Repair / Retry 可能足够。

但如果 failure 改变了未来可行路径：

```text
关键资源不可用
前置条件永久失效
用户约束变化
环境发生重大变化
```

则需要 Replan。

所以：

```text
Retry
→ 同一 Action 再尝试

Repair
→ 修正当前 Action

Replan
→ 重构未来 Action 序列
```

---

#### 3.8.17 Rollback 与 Compensation

**Rollback** 常见于支持事务的系统：

```text
BEGIN
write A
write B
error
ROLLBACK
```

如果事务尚未 commit，系统可以恢复到原状态。

**Compensation** 则是事情已经真实发生，只能再做一个新的业务动作补偿。

例如：

```text
hotel booked
flight booking failed
→ cancel hotel
```

所以：

```text
Rollback
= 撤销未最终提交的事务状态

Compensation
= 对已经发生的业务 effect 做反向补偿动作
```

而 Compensation 本身也可能失败，也可能需要新的 Approval。

---

#### 3.8.18 Ask User：缺失信息不是系统应该猜的 Failure

某些 failure 的根因不是 Tool 或 Runtime，而是：

```text
用户信息不足
目标存在歧义
高风险字段未确认
```

例如“把报告发给张老师”，但通讯录里有三个张老师。

最合理的恢复不是 guess one，而是 Ask User。

所以：

> **Clarification 是一种正常 Recovery Action，不是 Agent 无能的表现。**

---

#### 3.8.19 Human Escalation

适合 Human Escalation 的情况包括：

```text
高风险不可逆 Action
多次恢复仍失败
证据互相冲突
权限边界不明确
安全事件
法律 / 合规要求
重大金额
关键生产变更
```

关键不是“模型不会了”，而是：

```text
Expected Cost of Autonomous Continuation
>
Expected Cost of Human Escalation
```

因此 Human-in-the-loop 本质上也是一种风险路由机制。

---

#### 3.8.20 Abort：有时候最可靠的恢复就是停止

成熟 Agent 必须允许 STOP / ABORT。

如果：

```text
没有安全恢复路径
风险过高
预算耗尽
权限不足
关键证据缺失
恢复循环无进展
```

继续执行往往比失败本身更危险。

因此：

> **Failure Handling 的目标不是“无论如何都完成”，而是在可靠性、风险和成本约束下做最合理的终止或恢复决策。**

---

#### 3.8.21 Terminal Failure 与 Recoverable Failure

可以把 failure 状态显式分成：

```text
RECOVERABLE
DEGRADED
BLOCKED
TERMINAL
UNKNOWN
```

例如：

```text
rate limited
→ recoverable / delayed

optional Tool unavailable
→ degraded

need user approval
→ blocked

hard policy violation
→ terminal

timeout after effectful submit
→ unknown
```

这比统一返回 FAILED 有用得多。

---

#### 3.8.22 Transient、Permanent、Deterministic、Stochastic Failure

**Transient Failure**：

```text
network jitter
short-term rate limit
temporary overload
service restarting
```

可能适合 Retry。

**Permanent Failure**：

```text
resource deleted
permission permanently absent
schema changed
invalid account
unsupported operation
```

继续 Retry 通常无意义。

如果每次同样输入都会失败，如 invalid schema、permission denied，通常属于 deterministic failure；network timeout、sporadic 503 则可能是 stochastic failure。

因此：

```text
same action + same state + same deterministic error
```

继续重复通常没有价值。

---

#### 3.8.23 Recoverability 应该看 State，不只看 Error Code

同一个错误码，在不同 State 下恢复策略可能不同。

例如 409 Conflict：如果只是 version stale，可以 re-read → repair → retry；如果代表 business invariant conflict，可能必须 replan / ask user / abort。

所以更准确的是：

$$
Recovery = f(Error, State, History, SideEffects, Budget, Risk)
$$

而不是：

```text
error_code → fixed action
```

---

#### 3.8.24 Failure History 本身也是 State

Recovery 不能每次都像第一次见到错误。

应该记录：

```text
failure_type
attempt_count
previous_repairs
previous_routes
previous_tools
observed_effects
last_progress
cumulative_cost
```

例如第 1 次 timeout 可以 retry，但第 5 次同样 timeout 不应仍然机械 retry。

因此：

> **Recovery Policy 必须 history-aware。**

---

#### 3.8.25 Recovery Loop 也可能陷入死循环

例如：

```text
Tool A fails
→ fallback B
→ B fails
→ fallback A
→ ...
```

或者：

```text
repair argument
→ same validation error
→ repair again
→ same validation error
```

这叫 recovery thrashing。

需要：

```text
max recovery attempts
visited recovery states
no-progress detector
repeated-error detector
route oscillation detector
```

否则 Failure Handling 本身会成为新的 Failure Source。

---

#### 3.8.26 Busy Recovery ≠ Progress

系统连续执行：

```text
retry
repair
fallback
retry
replan
```

并不意味着任务正在接近成功。

应该问：

```text
新 Evidence 出现了吗？
State 改变了吗？
Failure class 改变了吗？
成功概率提升了吗？
可行路径扩大了吗？
```

因此沿用 2.2 的原则：

> **Busy ≠ Progress。**

Recovery 也需要 Progress Signal。

---

#### 3.8.27 Progress-aware Recovery

可以定义简单的恢复进展信号：

```text
new_evidence
new_valid_state
reduced_uncertainty
new_route_available
fewer_failed_constraints
verification_score_improved
```

如果连续 N 次恢复都没有任何变化，则应升级到 replan、human escalation 或 abort，而不是无限循环。

---

#### 3.8.28 Recovery Action 也必须再次经过 Validation / Authorization

一个常见错误是：

```text
正常 Action 有权限检查
Recovery Action 没检查
```

恢复不是绕过安全边界的特殊通道。

所有 effectful recovery action 仍然需要：

```text
Schema Validation
Semantic Validation
Permission
Approval
Runtime Guard
```

并且原则上：

```text
Recovery Authority
≤
Original Authorized Scope
```

除非明确经过新的 escalation / approval。

---

#### 3.8.29 Failure Handling 与 Observation 的关系

3.7 已经说明：Failure 本身也是 Observation。

3.8 进一步强调：

> **Recovery 的输入应该是结构化 failure evidence，而不是“Tool failed”这种低信息文本。**

例如：

```json
{
  "status": "conflict",
  "error_code": "STALE_VERSION",
  "expected_version": "abc123",
  "current_version": "def456",
  "retryable": false
}
```

这允许系统选择 re-read → repair，而不是 blind retry。

---

#### 3.8.30 Failure Handling 与 Reflection、Verification、Planning、Routing 的关系

**Reflection** 负责：为什么失败、哪里有问题、应该改什么。

**Failure Handling** 负责：系统下一步实际采用哪种恢复机制。

**Verification** 负责：Recovery 后是否真的恢复成功。

**Planning** 负责：当失败破坏未来结构时，重构计划。

**Routing** 负责：当当前能力路径失效时，选择另一条路径。

因此：

```text
Failure
↓
Observation
↓
Diagnosis / Reflection
↓
Recovery Policy
↓
Retry / Repair / Reroute / Replan / ...
↓
Re-observe
↓
Verification
```

---

#### 3.8.31 Recovery Policy 应该优先确定性，还是交给 LLM？

适合 deterministic policy 的：

```text
HTTP 429 → bounded backoff
schema invalid → reject before execution
permission denied → no retry
stale version → refresh state
retry count exhausted → escalate
```

更适合 LLM / Planner 判断的：

```text
是否换研究策略
怎样改写搜索 query
怎样修复复杂代码 patch
是否重构计划
```

因此成熟系统往往是：

```text
Deterministic Failure Policy
        ↓
处理清晰、低歧义错误
        ↓
LLM / Planner Recovery
        ↓
处理真正需要语义判断的复杂失败
```

这正是：

> **把确定性留给程序，把不确定性留给 Agent。**

---

#### 3.8.32 Recovery Policy 属于 Harness，执行恢复属于 Runtime

模型可以提出“我想 retry”，但是否允许 retry，不应该只由模型决定。

Harness 应控制：

```text
max retries
which errors are retryable
which tools can fallback
when to replan
when approval is required
when to escalate
when to abort
```

Runtime 更偏底层：

```text
timeout detection
process status
exit code
cancellation
sandbox reset
checkpoint restore
idempotency key
transaction state
retry scheduling
backoff timer
resource cleanup
```

所以：

```text
Harness
= 为什么恢复、恢复到哪里、允许哪种恢复

Runtime
= 恢复动作怎样被可靠执行
```

---

#### 3.8.33 Circuit Breaker、Bulkhead、Backpressure 与 Load Shedding

如果 backend 连续 503，每个 Agent 都继续 retry 会造成级联故障。

Circuit Breaker 可以：

```text
CLOSED → normal traffic
OPEN → fail fast
HALF_OPEN → limited probe
```

Bulkhead / Isolation 则通过独立 worker pool、queue、quota 限制一个 Tool 拖死全局。

Backpressure 在下游处理能力不足时，把压力反馈给上游，而不是无限接任务。

Load Shedding 在极端过载下主动拒绝低优先级任务，优于“全部接受然后全部超时”。

这些是 system-level Failure Handling，而不是单个 Agent reasoning 能解决的问题。

---

#### 3.8.34 Graceful Degradation

并不是所有 failure 都必须把任务判成完全失败。

例如实时价格 Tool 不可用，系统仍然可以返回静态分析，并明确声明实时价格不可验证。

这叫 graceful degradation。

关键是：

> **降低能力可以，但必须显式暴露能力下降，不能把 degraded result 冒充完整结果。**

---

#### 3.8.35 Partial Success 与 Recovery Granularity

例如用户要求给 10 个客户创建工单，结果 8 success、2 failed。

系统不应该简单说 SUCCESS，也不应该把整个 batch 重跑。

更合理：

```json
{
  "status": "partial",
  "succeeded": [...],
  "failed": [...],
  "retryable_failed": [...]
}
```

然后针对失败子集恢复。

Recovery 可以在：

```text
field-level
call-level
step-level
subtask-level
plan-level
episode-level
```

发生。

原则上：

> **优先修复最小必要范围。**

---

#### 3.8.36 Checkpoint 与 Resume

长任务失败时，从头重跑可能代价巨大。

Runtime 可以保留：

```text
checkpoint
completed steps
artifacts
verified state
pending operations
```

恢复时 resume from last verified checkpoint，而不是 restart everything。

但必须确认 checkpoint freshness、external side effects 与 environment drift。

---

#### 3.8.37 Unknown Outcome 与 Reconciliation

Unknown Outcome 是 Failure Handling 里最危险的一类状态之一：

```text
known success → continue
known failure → recover
unknown → 不知道该继续还是恢复
```

把 UNKNOWN 当 FAIL 可能造成 duplicate effect；把 UNKNOWN 当 SUCCESS 可能造成 false-success claim。

所以优先需要：

```text
status query
read-after-write
independent verification
reconciliation
```

Reconciliation 的核心问题是：

> **Agent 当前 State 与 Environment 实际 State 是否一致？**

---

#### 3.8.38 Error Budget 与 Recovery Budget

Failure Handling 本身也消耗：

```text
tokens
model calls
tool calls
latency
money
human attention
```

因此可以设置：

```text
max_recovery_steps
max_recovery_cost
max_recovery_wall_time
max_human_escalations
```

一个理论上可恢复、但恢复成本远高于任务价值的 failure，可能应该直接停止。

---

#### 3.8.39 Expected Recovery Value

可以抽象成：

$$
ERV(a)=P(\text{recover}\mid a)\cdot V_{success}-C(a)-R(a)
$$

其中：

- $a$：某种 recovery action；
- $P(\text{recover}\mid a)$：恢复成功概率；
- $V_{success}$：成功价值；
- $C(a)$：成本；
- $R(a)$：风险。

于是继续恢复不应该是默认行为，而应取决于边际价值。

---

#### 3.8.40 Recovery Escalation Ladder

可以把恢复动作组织成逐步升级：

```text
Level 0: Re-observe
Level 1: Retry
Level 2: Local Repair
Level 3: Fallback / Reroute
Level 4: Replan
Level 5: Ask User / Human Escalation
Level 6: Compensation / Safe Shutdown
Level 7: Abort
```

实际系统不一定严格按顺序，但思想是：

> **不要一遇到小错误就重规划整个世界，也不要在重大故障上永远只 Retry。**

---

#### 3.8.41 Recovery Decision Table

| Failure | First Response | Avoid |
|---|---|---|
| schema invalid | repair args | execute anyway |
| permission denied | request authority / stop | blind retry |
| rate limited | backoff | rapid retry |
| stale state | re-observe | write with old state |
| timeout, unknown effect | reconcile status | immediate duplicate write |
| tool unavailable | fallback / reroute | infinite retry |
| partial success | repair failed subset | rerun whole batch |
| plan assumption invalid | replan | follow stale plan |
| verification failed | diagnose / repair | claim success |
| budget exhausted | degrade / stop | continue silently |

这种表特别适合 Harness deterministic policy。

---

#### 3.8.42 Failure Severity 与 Blast Radius

Failure 不只有类型，还有严重程度。

可以考虑：

```text
impact
blast radius
reversibility
financial cost
privacy impact
security impact
user-visible harm
```

例如 search timeout 和 wrong-recipient email sent 都可以叫 failure，但严重程度完全不同。

Blast radius 也可能只影响一个字段、一个文件、一个用户、一个 tenant 或整个服务。

因此可靠系统应尽量通过 sandbox、least privilege、small batch、transaction、checkpoint、dry-run、approval、version precondition 做 failure containment。

> **可靠系统的目标不是假设失败不会发生，而是假设失败必然会发生，然后限制它的传播。**

---

#### 3.8.43 Cascading Failure

一个局部错误可能触发：

```text
Tool timeout
→ Retry storm
→ Backend overload
→ More timeout
→ Queue saturation
→ Other Agents fail
```

所以 Failure Handling 不只需要 Agent-local policy，还需要 system-level protection：

```text
circuit breaker
rate limit
bulkhead
backpressure
load shedding
```

---

#### 3.8.44 Poison Pill 与 Dead-letter Queue

某些特定输入无论重试多少次都会触发同一故障：

```text
malformed document
unsupported encoding
corrupt artifact
```

如果一直放回队列，就变成 poison pill。

因此需要：

```text
max attempts
quarantine
dead-letter queue
manual inspection
```

DLQ 可保留 payload、failure history、trace、last error、attempt count，避免坏任务持续阻塞主执行路径。

---

#### 3.8.45 Failure Observability 与 Attribution

一个 failure 至少应该能关联：

```text
trace_id
step_id
call_id
tool
arguments hash
status
error type
attempt
latency
side-effect status
recovery action
final outcome
```

最终 Task Failure 发生时，还应该区分：

```text
first failure
root failure
proximate failure
recovery failure
terminal failure
```

例如：

```text
first failure: search query bad
recovery failure: Agent didn't reformulate
terminal failure: budget exhausted
```

如果只记录最后一个 BUDGET_EXHAUSTED，就会掩盖真正根因。

---

#### 3.8.46 Root Cause vs Proximate Cause

Proximate Cause 是离失败最近的原因，例如 HTTP 500。

Root Cause 则可能是更早的：Agent 选择了已废弃 endpoint。

所以 Failure Analysis 不应该停在最后一层异常码。

Recovery Failure 也必须被记录，因为恢复策略本身也可能是系统问题。

---

#### 3.8.47 Safety Failure 与 Ordinary Failure 必须分开

普通 failure：tool unavailable。

安全 failure：

```text
prompt injection detected
unauthorized cross-tenant request
credential leak risk
destructive action without approval
```

安全 failure 的 recovery 原则通常更保守，往往倾向 fail closed，而不是“换条路继续试”。

---

#### 3.8.48 Fail-open vs Fail-closed

当安全检查自身出错时：

```text
Fail-open
→ 允许继续

Fail-closed
→ 默认拒绝
```

对于高风险 Action，通常更倾向 fail-closed。

例如权限服务不可用时，不应该：

```text
“既然查不到权限，那先执行吧。”
```

---

#### 3.8.49 User-visible Error、Model-facing Error、Internal Log 不应混用

系统内部可能有 stack trace、service topology、internal host、request IDs。

对用户需要可理解、可行动的信息；对模型需要足够支持 recovery 的结构化证据；对日志需要足够 debug 的技术细节。

三者不应混用。

同时 error message 可能包含 API key、PII、internal endpoint，也可能本身带有恶意 prompt injection，因此进入 Context 前仍需 redaction 与 trust labeling。

---

#### 3.8.50 Failure Handling 与 Memory / Learning from Experience

一次 failure 是否值得长期记忆，需要 Memory Policy 决定：

```text
Failure Observation
≠
Automatic Memory
```

但 failure trajectory 本身是很有价值的数据：

```text
State
Action
Failure
Diagnosis
Recovery
Outcome
```

可以用于分析哪些 failure 最常见、哪些 recovery 最有效、哪些 retry 是浪费、哪些 fallback 真正 rescue。

---

#### 3.8.51 Rescue 与 Harm 都要统计

如果一种 recovery strategy 把 20 个失败救回来，但同时把 8 个本来可安全停止的状态变成有害副作用，不能只报告 20 个 rescue。

可以定义：

```text
Net Recovery Benefit
=
Recovered Success
-
Recovery-induced Harm
```

更完整还应考虑成本与风险。

---

#### 3.8.52 Recovery Evaluation

至少可以测：

```text
Failure Detection Precision / Recall
Failure Classification Accuracy
Recovery Attempt Rate
Recovery Success Rate
Harmful Recovery Rate
Duplicate Side-effect Rate
Recovery Cost
Recovery Latency
Escalation Rate
Abort Appropriateness
No-progress Rate
False-success-after-recovery Rate
```

其中 classification 最好看 Confusion Matrix 与 severity-weighted error，因为不同误判的风险并不相同。

---

#### 3.8.53 Fault Injection 与 Chaos Testing

为了评估 Recovery，不应该只等真实系统自然出故障。

可以主动注入：

```text
network delay
503
429
timeout
connection reset
stale version
permission denied
partial write
corrupt observation
missing callback
```

然后测：

```text
Detection
Classification
Recovery
Final Outcome
Side Effects
```

更高层还可以在受控环境测试 Tool unavailable、worker crash、network partition、storage failure，验证系统是否 fail safely、recover predictably、preserve state、avoid cascading failure。

---

#### 3.8.54 Recovery Counterfactual

可以问：

```text
如果 failure 没发生，trajectory 会怎样？
如果采用另一种 recovery，会怎样？
```

这对于比较 retry vs fallback、repair vs replan、abort vs continue 很有价值。

---

#### 3.8.55 Failure Handling 的数据记录格式

可以记录：

```json
{
  "failure_id": "fail_1847",
  "step_id": "step_12",
  "failure_type": "STALE_STATE",
  "severity": "medium",
  "retryable": false,
  "recoverable": true,
  "effect_state": "none",
  "evidence": {},
  "recovery_action": "REOBSERVE_AND_REPAIR",
  "attempt": 2,
  "outcome": "recovered"
}
```

这样才适合后续统计和学习。

---

#### 3.8.56 Failure Handling 的最小状态机

可以抽象成：

```text
RUNNING
   ↓ failure
FAILED_STEP
   ↓ classify
RECOVERING
   ├── success → RUNNING
   ├── blocked → WAITING_USER / WAITING_APPROVAL
   ├── unknown → RECONCILING
   ├── budget exhausted → TERMINAL_FAILED
   └── unrecoverable → TERMINAL_FAILED
```

这比 try / except / retry 更符合真实 Agent Runtime。

---

#### 3.8.57 Minimal Robust Recovery Loop

```python
while not state.terminal:
    result = execute_next_action(state)
    obs = normalize(result)
    state.update(obs)

    if obs.ok:
        continue

    failure = classify_failure(state, obs)

    if failure.effect_unknown:
        recovery = reconcile_first(state, failure)
    else:
        recovery = choose_recovery(state, failure)

    if recovery.requires_approval:
        state.blocked = True
        break

    if recovery.is_abort:
        state.fail(reason=failure)
        break

    state.record_recovery(recovery)
    execute_recovery(recovery)

    if state.recovery_budget_exhausted():
        state.fail(reason="recovery_budget_exhausted")
```

真实系统还需要 authorization、idempotency、checkpoint、verification 等，但核心结构就是：

```text
failure → classify → recover → re-observe
```

---

#### 3.8.58 Coding Agent 示例

任务：修复 parser bug，并保证测试通过。

```text
run_tests
↓
3 failing tests
↓
read_file
↓
edit_file
↓
run_tests
↓
1 failure remains
```

这里合理策略不是把同一个 patch 再应用一次，而是：

```text
Failure Classification:
repair incomplete
↓
read new failing trace
↓
local diagnosis
↓
repair patch
↓
rerun targeted test
↓
full verification
```

如果出现 STALE_STATE，则 re-read file → compare external changes → reconstruct patch，而不是 blind overwrite。

---

#### 3.8.59 Browser Agent 示例

任务：提交表单。

点击 Submit 后页面超时。

错误恢复：立即再次点击 Submit，可能造成重复订单。

更合理：

```text
timeout = unknown outcome
↓
refresh / query order status
↓
if order exists
    continue
else
    retry submit
```

这就是 Reconciliation before Retry。

---

#### 3.8.60 Research Agent 示例

任务：找三篇支持某结论的高质量来源。

搜索 Tool 返回 rate limited，可以 bounded backoff；如果一直不可用，可以 fallback search provider；如果 fallback 只能访问较低质量数据，则 graceful degradation + explicit limitation，而不是把低质量来源伪装成等价高质量证据。

---

#### 3.8.61 Multi-Agent Failure Handling

多 Agent 系统还会出现：

```text
subagent timeout
handoff lost
conflicting outputs
agent unavailable
recursive delegation
```

Recovery 可能包括 reassign、reroute、arbitration、cancel duplicate subtask、fallback to single-agent path。

但必须防止：

```text
subagent failure
→ spawn more subagents
→ more failure
→ recursive fan-out
```

分布式恢复还需要 resource lock、version、idempotency key、leader / ownership 等协调机制。

---

#### 3.8.62 Failure Handling Failure Modes

典型 failure modes 包括：

1. **Blind Retry**：不判断 failure 类型直接重试。
2. **Retry Storm**：大量并发立即重试扩大故障。
3. **Unknown-as-Failure**：把未知结果当失败导致重复副作用。
4. **Unknown-as-Success**：把未知结果当成功导致 false-success。
5. **Infinite Recovery Loop**：恢复路径没有终止条件。
6. **Recovery Thrashing**：在多个恢复路径之间来回振荡。
7. **Over-Replanning**：小错误就重做整个计划。
8. **Under-Replanning**：计划前提失效仍然局部 retry。
9. **Unsafe Fallback**：替代 Tool 权限 / 语义不等价。
10. **Duplicate Side Effect**：重复执行非幂等 Action。
11. **Partial-success Replay**：整个批次重跑导致重复成功项。
12. **Stale-state Recovery**：基于旧状态继续修复。
13. **Permission Escalation via Recovery**：恢复路径越权。
14. **Compensation without Approval**：补偿动作产生新风险却未确认。
15. **Error-message Injection**：把外部 error 当指令。
16. **Silent Degradation**：能力下降却对用户声称完整成功。
17. **No-progress Recovery**：动作很多但 State 没改善。
18. **Budgetless Recovery**：恢复无限消耗资源。
19. **Root-cause Masking**：只记录最后 error，掩盖原始根因。
20. **Recovery Failure Unobserved**：恢复本身失败却未进入 State。
21. **Cascade Amplification**：局部失败被 retry 放大成系统故障。
22. **Poison-pill Loop**：坏输入永久占据队列。
23. **Checkpoint Drift**：恢复旧 checkpoint 时外部环境已改变。
24. **False Completion after Recovery**：恢复 Action 成功就直接 claim task success。

---

#### 3.8.63 Engineering Principles

1. **先分类 Failure，再决定恢复动作。**
2. **Unknown Outcome 优先 Reconcile，不要盲目 Retry。**
3. **Retry 必须同时考虑 transientness、idempotency、state freshness 与 side effects。**
4. **最小范围 Repair 优于不必要的 Full Replan。**
5. **Fallback 必须保证 capability / permission / semantics 足够等价。**
6. **Recovery Action 仍然必须经过 validation、authorization 与 approval。**
7. **Recovery Authority 不得隐式高于 Original Authority。**
8. **所有恢复都必须重新 Observation + Verification。**
9. **Partial Success 要按子任务恢复，不要盲目重放整个 batch。**
10. **显式维护 Failure History 与 Recovery History。**
11. **设置 Recovery Budget、No-progress Guard 和 Oscillation Guard。**
12. **高风险故障优先 fail-safe / fail-closed。**
13. **结构化 Error Observation 应足以支持 targeted repair。**
14. **记录 Root Cause、Recovery Failure 与 Terminal Failure，而非只记录最后异常。**
15. **可靠系统应假设 failure 必然发生，并提前做 containment。**
16. **Graceful Degradation 必须显式披露能力下降。**
17. **不要让 recovery mode 成为绕过 permission 的后门。**
18. **Busy Recovery ≠ Progress。**

---

#### 3.8.64 Boundary Table

| 概念 | 核心问题 |
|---|---|
| Retry | 同一个 Action 是否值得再执行一次？ |
| Repair | 当前 Action 应怎样被修正？ |
| Fallback | 是否有等价替代实现？ |
| Reroute | 是否应切换到另一条能力路径？ |
| Replan | 未来计划是否需要重构？ |
| Rollback | 未最终提交的状态能否撤销？ |
| Compensation | 已经发生的业务 effect 怎样被补偿？ |
| Reconciliation | Agent State 怎样重新与 Environment 对齐？ |
| Ask User | 是否需要用户补充信息或消除歧义？ |
| Human Escalation | 是否应把决策交给人？ |
| Abort | 是否应该安全停止？ |
| Verification | Recovery 后是否真的恢复成功？ |

---

#### 3.8.65 Interview Mastery

这一节至少要能回答：

1. Failure Handling 为什么不能等价成 `try/except + retry`？
2. Retryable 和 Recoverable 有什么区别？
3. Timeout 为什么不能直接判定为 Failure？
4. Unknown Outcome 应该怎样处理？
5. Retry、Repair、Fallback、Reroute、Replan 分别是什么？
6. Rollback 和 Compensation 有什么区别？
7. 为什么 Recovery Action 也需要 Permission / Approval？
8. 为什么 Error Message 的结构会影响 Agent 的 Recovery 能力？
9. Partial Success 应该怎样恢复？
10. 怎么检测 Recovery Loop 没有 Progress？
11. Circuit Breaker、Backoff、Jitter 分别解决什么问题？
12. 什么情况下应该 Ask User，而不是让 Agent 猜？
13. Human Escalation 的触发依据是什么？
14. Failure Handling 如何与 Reflection / Verification 区分？
15. Failure History 为什么必须进入 State？
16. 怎样评价一个 Recovery Policy？
17. 什么是 false-success after recovery？
18. 为什么 graceful degradation 必须显式告诉用户？
19. Fail-open 与 Fail-closed 怎么选？
20. 怎样用 fault injection 测 Agent 的 Failure Handling？

---

#### 3.8.66 一句话总结

> **Failure Handling 是 Agent 可靠性的恢复控制层：失败后先做 localization 与 classification，再根据 effect、state、retryability、recoverability、risk 与 budget 选择 Retry、Repair、Fallback、Reroute、Replan、Rollback、Compensation、Ask User、Human Escalation 或 Abort；任何 Recovery 都必须重新观察和验证，且不能绕过原有权限边界。**

---

#### 3.8.67 参考资料

- Kleppmann M. **Designing Data-Intensive Applications**. O'Reilly, 2017. 用于理解 retry、idempotency、consistency、transactions、failures 与 distributed-system recovery。
- Nygard M. **Release It! Design and Deploy Production-Ready Software**. Pragmatic Bookshelf. 用于理解 circuit breaker、stability patterns、failure containment 与 cascading failure。
- Richardson C. **Microservices Patterns**. Manning, 2018. 用于理解 Saga、Compensating Transaction、retry、message delivery 与跨服务 recovery。
- Beyer B, Jones C, Petoff J, Murphy N R. **Site Reliability Engineering: How Google Runs Production Systems**. O'Reilly, 2016. 用于理解 error budget、incident handling、overload、reliability 与 operational recovery。
- Allspaw J, Robbins J. **Web Operations**. O'Reilly, 2010. 用于理解生产系统故障、可观测性与恢复思维。

