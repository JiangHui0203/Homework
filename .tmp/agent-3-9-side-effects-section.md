### 3.9 Side Effects

#### 3.9.1 定义：Side Effect 到底是什么？

前面 3.1–3.8 已经把 Tool Use 从能力定义、输入结构、选择、参数、执行、Observation 到 Failure Handling 全部拆开。

但真正决定 Agent 风险上限的，还有最后一个问题：

> **一次 Action 执行以后，除了“返回了什么”，它到底对 Environment 改变了什么？**

这就是 Side Effect。

在程序设计里，Side Effect 通常指函数除了返回值之外，还改变了外部状态，例如：

```text
写文件
修改数据库
发送网络请求
写缓存
更新全局变量
发消息
创建订单
扣款
删除资源
```

在 Agent 系统里，这个概念需要进一步扩大。

更准确地说：

> **Side Effect 是一次 Agent Action 对当前推理过程之外的持久状态、外部主体、资源、权限、成本、可见性或未来行为产生的任何可观察影响。**

最小链路可以写成：

```text
Proposed Action
      ↓
Validation / Authorization
      ↓
Execution
      ↓
Environment Transition
      ↓
Primary Effect
      ↓
Secondary / Hidden Effects
      ↓
Observation
      ↓
Verification / Audit
```

所以首先要记住：

> **Tool Output 描述“返回了什么”；Side Effect 描述“世界变成了什么”。**

这两个概念不能混在一起。

---

#### 3.9.2 Pure Computation 与 Side-effecting Action

最理想的纯函数可以抽象成：

```text
input
 ↓
f(x)
 ↓
output
```

执行完成后，除了返回值，不改变外部世界。

例如：

```text
calculator("17 * 23")
```

通常可以近似看成 pure computation。

而：

```text
send_email(...)
```

不仅返回：

```text
message_id
```

还会改变真实世界：

```text
邮件进入发送系统
收件人可能收到通知
产生审计记录
可能产生计费
可能触发自动回复
可能触发下游 workflow
```

因此：

```text
Return Value
≠
Effect Set
```

可以形式化成：

$$
(e_{t+1}, r_t)=T(e_t,a_t)
$$

其中：

- $a_t$：Action；
- $e_t$：执行前 Environment State；
- $e_{t+1}$：执行后 Environment State；
- $r_t$：返回给 Runtime 的 Result。

真正的 side effect 是：

$$
\Delta e_t=e_{t+1}-e_t
$$

而不是 $r_t$ 本身。

---

#### 3.9.3 Read-only / Write / Irreversible：最基本的 Action 风险分层

Agent Tool 最常见的第一层分类是：

```text
Read-only
Write / Mutating
Irreversible / High-impact
```

**Read-only**

目标是读取状态，不主动修改目标业务对象：

```text
read_file
search_docs
get_order
list_calendar_events
query_database
```

**Write / Mutating**

会改变 Environment：

```text
write_file
update_order
create_ticket
send_email
create_calendar_event
```

**Irreversible / High-impact**

即使理论上可以补偿，也可能无法真正恢复原状态：

```text
publish_post
send_external_email
execute_payment
delete_without_backup
submit_application
revoke_access
```

因此风险通常满足：

```text
Read-only
   <
Reversible Write
   <
Compensatable Write
   <
Irreversible / External Effect
```

但这只是一个粗粒度起点。

---

#### 3.9.4 “Read-only” 并不等于“没有 Side Effect”

这是一个非常容易踩坑的地方。

例如：

```text
GET /document/123
```

看起来是 read-only。

但它可能同时：

```text
记录 access log
刷新 last_accessed_at
触发计费
更新 cache
触发 analytics
暴露访问行为
消耗 rate limit
改变推荐系统统计
触发 read receipt
```

所以：

> **Read-only 更准确地说是“不改变目标业务对象的核心状态”，而不是“系统里绝对没有任何副作用”。**

例如邮箱：

```text
read_message(message_id)
```

可能自动：

```text
mark_as_read = true
```

那么它实际上不是纯读取。

因此 Tool Contract 最好区分：

```text
business_state_mutation
telemetry_effect
billing_effect
visibility_effect
cache_effect
notification_effect
```

---

#### 3.9.5 Primary、Secondary、Hidden Side Effects

一个 Action 可能有多层 Effect。

**Primary Effect**

Tool 的直接业务目标。

例如：

```text
create_issue()
→ 创建 issue
```

**Secondary Effect**

由 primary effect 直接触发的附带变化：

```text
创建 issue
→ 通知 watchers
→ 触发 webhook
→ 触发 CI / bot
```

**Hidden Effect**

模型和用户可能没有显式意识到，但系统会发生：

```text
产生计费
写审计日志
刷新缓存
改变 ranking / analytics
暴露访问模式
触发 retention policy
```

因此：

```text
Action Semantics
≠
Single Effect
```

更真实的是：

```text
Action
  ↓
Effect Graph
├── Primary Effect
├── Secondary Effects
└── Hidden / Infrastructure Effects
```

---

#### 3.9.6 Side-effect Graph：一个 Action 可能触发整个事件链

现实系统往往不是：

```text
Agent → Tool → One Change
```

而是：

```text
Agent
 ↓
Tool
 ↓
Service A
 ↓
Event Bus
 ├── Service B
 ├── Service C
 └── External System
```

例如：

```text
create_order()
```

可能触发：

```text
reserve inventory
create payment intent
send confirmation
start fulfillment
emit analytics event
notify fraud system
```

因此评估 Side Effect 时不能只看第一跳。

需要考虑：

> **Effect Propagation。**

这也是为什么有些 Action 的真实 blast radius 远大于 Tool Description 表面看起来的范围。

---

#### 3.9.7 Blast Radius：一次错误 Action 最多能影响多大范围？

可以把 Action 风险粗略理解为：

$$
Risk \approx P(Error) \times Impact \times BlastRadius
$$

例如：

```text
edit_one_draft_file
```

和：

```text
delete_all_customer_records
```

即使模型犯错概率相同，风险完全不同。

Blast Radius 可以按多维度理解：

```text
对象数量
用户数量
金额
数据范围
时间跨度
权限范围
外部系统数量
可见受众
不可逆程度
```

因此成熟 Tool Design 应尽量提供：

```text
narrow-scope action
```

而不是默认暴露：

```text
bulk destructive action
```

---

#### 3.9.8 Side-effect Budget：不只是 Token Budget

前面 1.8 讲过 Agent Budget 不只包括 token 和 latency。

对于 effectful Agent，还应该有：

> **Side-effect Budget。**

例如一次任务可以限制：

```text
最多发送 3 封邮件
最多创建 5 个 issue
最多修改 10 个文件
最大支付金额 100 USD
最多删除 0 个永久资源
最多触达 20 个外部用户
```

可以写成：

```text
Budget
├── Tokens
├── Model Calls
├── Tool Calls
├── Wall Time
├── Money
└── Side Effects
    ├── mutations
    ├── external sends
    ├── destructive ops
    └── monetary impact
```

这使 Harness 能从：

```text
“调用次数还没超限”
```

升级到：

```text
“真实世界影响还在授权预算内”
```

---

#### 3.9.9 Reversible、Compensatable、Irreversible

不要简单把 Action 分成：

```text
能撤销 / 不能撤销
```

更准确可以分成三类。

**Reversible**

系统可以恢复到近似原状态：

```text
修改草稿
→ restore previous version
```

**Compensatable**

原 effect 已经发生，但可以执行一个新的 Action 抵消业务影响：

```text
charge card
→ refund
```

注意：

```text
refund
≠
原 charge 从历史上没发生过
```

**Irreversible**

无法可靠恢复：

```text
公开发布敏感信息
发送不可撤回外部邮件
永久删除无备份数据
泄露 secret
```

因此：

> **Compensation ≠ Reversibility。**

这是 Side Effect 语义里必须长期记住的一条。

---

#### 3.9.10 Irreversibility 不是二元变量

很多 Action 的不可逆性是连续谱。

例如发送邮件：

```text
技术上不能撤回
```

但可以：

```text
follow-up correction
```

删除 Git branch：

```text
如果 commit 仍可找回
→ technically recoverable
```

但如果已经影响协作：

```text
业务上仍有损失
```

所以可以从多个维度判断：

```text
technical reversibility
business reversibility
social reversibility
financial reversibility
privacy reversibility
```

尤其：

```text
privacy leakage
```

通常几乎不可真正撤销。

---

#### 3.9.11 Confirmation：什么时候必须二次确认？

并不是所有 Tool Call 都需要用户确认。

如果每次：

```text
read_file
search_web
run_tests
```

都要求 confirmation，Agent 会失去可用性。

合理做法是基于：

```text
Risk
Irreversibility
Blast Radius
Ambiguity
Cost
User Expectation
```

决定是否升级到 Confirmation / Approval。

例如：

```text
低风险读取
→ 自动执行

可逆草稿修改
→ 自动执行 + audit

外部发送
→ preview / confirmation

高金额支付
→ explicit approval

永久删除
→ strong confirmation
```

所以：

> **Confirmation 应该 risk-based，而不是 tool-call-based。**

---

#### 3.9.12 Confirmation ≠ Authorization

用户点了：

```text
Confirm
```

并不自动意味着：

```text
这个 Action 在权限上合法
```

完整链条仍然应该是：

```text
User Intent
    ↓
Authorization
    ↓
Policy
    ↓
Resolved Arguments
    ↓
Risk Evaluation
    ↓
Confirmation / Approval
    ↓
Execution
```

因此：

```text
Confirmed
≠
Authorized
```

同样：

```text
Authorized
≠
Confirmed
```

二者职责不同。

---

#### 3.9.13 Approval 必须绑定 Final Resolved Action

前面 3.5 已经讲过：

> Approval 的对象应该是最终解析后的参数，而不是模糊意图。

Side Effect 章节进一步强调：

```text
Approved Effect Set
=
Executed Effect Set
```

例如用户批准：

```text
recipient = A
amount = 100
currency = USD
```

如果执行前参数变成：

```text
recipient = B
```

原 approval 已经失效。

因此 approval 最好绑定：

```text
canonical action hash
resource version
resolved arguments
effect scope
expiry
```

---

#### 3.9.14 Preview → Confirm → Commit：高风险 Action 的经典三阶段结构

对于高风险 Tool，一个很稳健的模式是：

```text
Prepare / Preview
      ↓
Show Intended Effects
      ↓
Confirm / Approve
      ↓
Commit
      ↓
Verify Actual Effects
```

例如批量删除：

```text
delete_users(filter="inactive > 365d")
```

不应该一上来直接删。

更好的接口是：

```text
preview_delete_users(...)
→ 132 users
→ estimated scope

commit_delete_users(plan_id)
```

这样用户和系统都能看到真实 blast radius。

---

#### 3.9.15 Dry-run：模拟效果，但不要假装等于真实执行

Dry-run 常用于：

```text
deployment
migration
bulk update
filesystem operation
infra change
```

例如：

```text
dry_run_update(...)
```

返回：

```text
预计修改 82 个对象
预计删除 0 个对象
预计成本 $4.21
```

但必须记住：

> **Dry-run Prediction ≠ Real Execution Outcome。**

因为真正执行时：

```text
state may change
permissions may change
external services may fail
race conditions may appear
```

所以 dry-run 是：

```text
risk estimation
```

不是最终 Verification。

---

#### 3.9.16 Prepare / Commit 模式

比普通 dry-run 更强的一种设计是：

```text
prepare_action()
→ validate current state
→ reserve / lock necessary resources
→ produce plan_id

commit_action(plan_id)
→ execute exact prepared operation
```

其价值是缩短：

```text
check
→ use
```

之间的 TOCTOU 窗口。

特别适合：

```text
支付
批量修改
高风险部署
预订
资源迁移
```

但即使如此，也不能假设绝对 atomic。

---

#### 3.9.17 Idempotency：Side Effect 安全的核心概念

如果 Action 重复执行，最终 Environment 是否会重复变化？

这是 idempotency 的核心问题。

例如：

```text
set_status(order, "cancelled")
```

重复两次通常仍然是：

```text
status = cancelled
```

而：

```text
send_email()
```

执行两次就是两封邮件。

因此：

```text
Retry Safety
高度依赖
Idempotency Semantics
```

---

#### 3.9.18 Idempotency Key：把“同一个业务意图”绑定起来

对 create / send / charge 类 Action，可以使用：

```text
idempotency_key
```

例如：

```text
charge_card(
  amount=100,
  idempotency_key="task-1847-payment-1"
)
```

如果网络 timeout 后再次发送同一 request：

```text
same key
```

服务端可以理解为：

> 这是同一次业务操作的重试，而不是第二次支付。

但要注意：

> **Idempotency Key 只有在服务端真正实现幂等语义时才有意义。**

模型自己生成一个字符串，并不会神奇地让 Tool 变幂等。

---

#### 3.9.19 Exactly-once 是危险直觉

分布式系统里经常很难真正保证：

```text
exactly once
```

现实更常见的是：

```text
at-most-once
at-least-once
idempotent processing
effectively-once business semantics
```

对于 Agent 来说，最重要的不是背术语，而是理解：

> **一旦存在 timeout、retry、queue、callback，重复 effect 就必须被当作正常故障模型，而不是罕见异常。**

---

#### 3.9.20 Duplicate Effect：重复执行为什么特别危险？

常见 duplicate side effects：

```text
重复发邮件
重复下单
重复支付
重复创建 ticket
重复创建 calendar event
重复写同一条数据库记录
重复发 Slack / IM 消息
```

Agent 中特别容易发生，因为：

```text
timeout
→ model sees failure
→ retries
```

但第一次其实已经成功。

因此必须结合：

```text
call_id
idempotency_key
business key
reconciliation
read-after-write
```

共同防护。

---

#### 3.9.21 Effect Verification：不要只验证 Return Value

Side Effect 需要验证的是：

```text
Environment 是否真的变成预期状态
```

例如：

```text
write_file() → success
```

之后可以：

```text
read_file()
compare hash
```

支付：

```text
charge() → accepted
```

之后可能还需要：

```text
query_payment_status()
```

所以：

```text
Execution Receipt
≠
Effect Verification
```

---

#### 3.9.22 Read-after-write Verification

最常见的 Effect Verification 是：

```text
Write
 ↓
Read Back
 ↓
Compare Expected vs Actual
```

例如：

```text
update_profile(name="Alice")
↓
get_profile()
↓
name == "Alice" ?
```

但还需要考虑：

```text
eventual consistency
cache
replica lag
async processing
```

所以“马上读不到”也不一定自动等于失败。

---

#### 3.9.23 Intended Effect vs Actual Effect

模型提出的是：

```text
Intended Effect
```

而 Environment 真正发生的是：

```text
Actual Effect
```

安全系统应该比较：

```text
Intended Effect Set
        vs
Actual Effect Set
```

不仅检查：

```text
该发生的发生了吗？
```

还要检查：

```text
有没有多发生不该发生的？
```

因此 Effect Verification 需要：

```text
Required Effects
Forbidden Effects
Invariant Preservation
```

这和 2.6 Verification 的 Predicate 思路完全一致。

---

#### 3.9.24 Over-effect：任务完成了，但做多了

Agent failure 不只包括：

```text
没做成
```

还包括：

```text
做成了，但额外改了不该改的东西
```

例如 coding agent：

```text
bug fixed ✅
tests pass ✅
```

但同时：

```text
删除 unrelated config ❌
格式化整个 repository ❌
修改 public API ❌
```

这就是 **Over-effect**。

所以：

> **Task Success 不足以证明 Side-effect Correctness。**

---

#### 3.9.25 Under-effect：只完成了部分真实改变

相反也可能：

```text
Tool returns success
```

但只完成部分 effect。

例如：

```text
create account ✅
assign permissions ❌
send invitation ❌
```

如果 Agent 只看到第一步成功就宣称整个 Action 完成，就是 under-effect verification failure。

---

#### 3.9.26 Partial Side Effects

复合 Action 特别容易出现：

```text
A ✅
B ✅
C ❌
```

这时候系统状态可能落在：

```text
Neither Old State
Nor Intended New State
```

也就是中间态。

因此需要：

```text
partial-effect representation
```

而不能只返回：

```text
success / failure
```

---

#### 3.9.27 Atomicity：哪些 Effect 应该一起成功或一起失败？

如果多个变化必须保持一致：

```text
Debit A
Credit B
```

理想上应该在同一事务里：

```text
all commit
or
none commit
```

这就是 atomicity。

但跨服务 Agent Action 经常做不到真正 atomic。

例如：

```text
book flight
book hotel
book car
```

三个独立供应商之间没有统一 Transaction。

此时需要 Saga / Compensation 思路。

---

#### 3.9.28 Rollback vs Compensation

再次强调：

```text
Rollback
= effect 尚未最终提交时恢复
```

例如数据库 transaction abort。

而：

```text
Compensation
= effect 已真实发生，再执行新的反向业务动作
```

例如：

```text
book hotel
↓
取消预订
```

所以 compensation 本身：

```text
也有 side effect
也可能失败
也需要权限
也需要 verification
```

---

#### 3.9.29 Compensation 不是万能撤销键

有些 effect 可以补偿业务价值，但不能恢复历史事实。

例如：

```text
发布错误公告
→ 发布更正
```

但：

```text
第一条公告已经有人看过
```

无法被“撤销”。

同样：

```text
泄露 secret
→ rotate secret
```

只是降低未来风险，不能保证旧 secret 没被复制。

因此：

> **高不可逆 Side Effect 应尽量在执行前防错，而不是依赖执行后补偿。**

---

#### 3.9.30 Prevention > Recovery for Irreversible Effects

对于：

```text
irreversible
high blast radius
high monetary impact
privacy-sensitive
external communication
```

系统应该把更多计算花在 Action 前：

```text
clarify
validate
verify target
preview
approval
policy check
freshness check
```

而不是：

```text
先做
→ 出错再修
```

这其实是一种：

> **Risk-aware compute allocation。**

---

#### 3.9.31 Effectful Action 的 Two-man Rule / Separation of Duties

极高风险场景中，可以要求：

```text
Agent proposes
↓
Independent verifier checks
↓
Human approves
↓
Runtime executes
```

或者：

```text
one system prepares
another authority commits
```

这就是 separation of duties。

它不是所有 Agent 都需要，但对于：

```text
高额资金
生产基础设施
权限管理
法律提交
数据删除
```

非常重要。

---

#### 3.9.32 Least Privilege：缩小 Action 本身的影响范围

Least Privilege 不只体现在：

```text
credential scope
```

也应该体现在 Tool 设计。

例如与其给 Agent：

```text
admin_db(sql)
```

更安全的是：

```text
update_customer_note(customer_id, note)
```

因为后者天然缩小：

```text
Action Space
Blast Radius
Argument Surface Area
Side-effect Surface
```

所以：

> **Tool Granularity 本身就是 Side-effect Control。**

---

#### 3.9.33 Capability Surface vs Effect Surface

一个 Tool 可能看起来只提供一种 Capability：

```text
manage_calendar
```

但它内部 Effect Surface 可能包括：

```text
create
update
delete
invite attendees
send notifications
change visibility
```

因此安全设计不能只看 Tool 名称，还要看：

```text
每个 operation 的 effect semantics
```

最好把高风险 operation 显式拆开。

---

#### 3.9.34 Hidden Fan-out：一个调用触发很多外部动作

例如：

```text
publish_release()
```

可能同时：

```text
publish artifact
notify customers
update docs
trigger deployment
post announcement
```

如果 Agent 只知道：

```text
“发布 release”
```

却不知道 fan-out，就无法正确评估风险。

因此 Tool Description / Contract 应尽量暴露：

```text
important secondary effects
```

尤其是用户可感知的 effect。

---

#### 3.9.35 Notification 也是 Side Effect

很多系统把：

```text
通知
```

当成无关紧要的附属行为。

但它可能直接影响用户体验和隐私。

例如：

```text
update_document()
```

可能触发：

```text
email all collaborators
```

所以 Tool Contract 应明确：

```text
notify = true / false
```

或提供明确语义，而不是藏在 backend default 里。

---

#### 3.9.36 Visibility Change 也是 Side Effect

例如：

```text
share_file()
publish_page()
change_repo_visibility()
```

核心 effect 不是内容变化，而是：

```text
谁能看到它
```

因此权限与可见性变化应该被视为高敏 Side Effect。

特别是：

```text
private → public
```

通常具有高度不可逆的信息泄露风险。

---

#### 3.9.37 Permission Mutation 是高风险 Side Effect

例如：

```text
add_admin
change_role
grant_access
create_token
```

它们不会直接删除数据，但会改变未来谁可以做什么。

因此这种 effect 的风险是：

```text
Future Capability Expansion
```

也就是：

> **一个 Action 可能不是直接造成伤害，而是扩大未来 Action 的 Authority。**

这类 effect 应特别严格审计。

---

#### 3.9.38 Cost Side Effects

Tool 调用也可能产生真实费用：

```text
云计算资源
短信
邮件
地图 API
付费搜索
GPU job
购买商品
第三方 SaaS
```

所以 cost 不只是 latency / token cost。

还包括：

```text
External Monetary Side Effect
```

例如：

```text
launch_training_job(gpus=128, hours=24)
```

即使功能上合法，也可能产生巨大成本。

因此可以设置：

```text
monetary effect budget
```

---

#### 3.9.39 Privacy Side Effects

读取敏感数据即使不修改 Environment，也可能产生：

```text
data exposure
logging
context retention
external transmission
```

因此 Side Effect 还包括：

> **Information Flow。**

例如：

```text
read_customer_record
↓
include in model context
↓
call external tool
```

这已经改变了数据传播范围。

所以 Privacy Effect 不能只靠“是不是 write tool”判断。

---

#### 3.9.40 Data Exfiltration 是信息型 Side Effect

传统 side effect 常强调：

```text
修改状态
```

但 Agent 安全里还必须强调：

```text
信息从高信任域流向低信任域
```

例如：

```text
internal secret
↓
model context
↓
web search query
```

即使没有修改任何内部资源，也已经产生严重真实世界影响。

因此：

```text
Information Disclosure
```

也是 Side Effect。

---

#### 3.9.41 Side-effect Taint：外部数据不应该随便驱动高风险 Effect

结合 3.7 Observation：

```text
External Untrusted Observation
        ↓
Model Decision
        ↓
Effectful Tool
```

这里存在典型 indirect prompt injection 风险。

所以可以维护：

```text
Observation Trust Label
        ↓
Action Risk Policy
```

例如：

```text
untrusted webpage
```

不能单独作为：

```text
delete file
send secret
transfer money
```

的授权依据。

---

#### 3.9.42 Effect Escalation：低风险输入如何被放大成高风险输出？

一个系统风险很大的模式是：

```text
低信任信息
↓
模型解释
↓
高权限 Tool
↓
高影响 Action
```

这就是 effect escalation。

因此成熟 Harness 需要约束：

```text
Trust Level
×
Action Risk
×
Permission
```

而不是只判断 Tool Call 语法是否合法。

---

#### 3.9.43 Side Effect 与 Tool Selection

3.4 Tool Selection 不应该只优化：

```text
哪个 Tool 最容易完成任务？
```

还应该考虑：

```text
哪个 Tool 产生更小的非必要 Side Effect？
```

例如：

```text
read_file
```

能够解决问题时，就不应选择：

```text
clone_entire_private_repo_to_external_service
```

因此 selection utility 可以包含：

$$
U = Quality - Cost - Risk - SideEffectPenalty
$$

---

#### 3.9.44 Side Effect 与 Argument Generation

同一个 Tool，不同参数的 Side Effect 可以差很多。

例如：

```text
delete_files(paths=[one_file])
```

和：

```text
delete_files(paths=[entire_repo])
```

Tool Selection 相同，但风险不同。

因此必须做：

```text
argument-level risk evaluation
```

而不能只给 Tool 一个固定 risk label。

---

#### 3.9.45 Side Effect 与 Execution

3.6 Tool Execution 关注：

```text
Action 怎样真正被执行
```

3.9 Side Effects 关注：

```text
执行以后世界被怎样改变
```

两者关系是：

```text
Execution
→ causes
Effect
```

但：

```text
execution succeeded
```

不保证：

```text
all intended effects correct
and no unintended effects
```

---

#### 3.9.46 Side Effect 与 Observation

3.7 Observation 是系统对 Effect 的感知通道。

```text
Effect occurs
↓
Observation captures evidence
↓
State Update
```

如果 Observation 不完整，Agent 可能不知道真实 Side Effect。

例如：

```text
create_event()
```

返回：

```text
event created
```

却没告诉模型：

```text
notifications_sent = 37
```

那模型对 effect 的 belief 就是不完整的。

---

#### 3.9.47 Side Effect 与 Failure Handling

3.8 Failure Handling 的核心问题之一是：

```text
失败时 effect 到底发生了吗？
```

所以恢复策略必须 side-effect-aware。

例如：

```text
TIMEOUT
+
non-idempotent action
```

不能盲 retry。

而：

```text
schema validation failure
+
no execution
```

可以安全修正参数再试。

---

#### 3.9.48 Side Effect 与 Verification

Verification 不只验证：

```text
任务目标有没有满足
```

还应该验证：

```text
是否出现 forbidden side effects
```

例如：

```text
Required:
  report generated

Forbidden:
  source data modified
  external email sent
  secret exposed
```

所以 Side Effect 是 Verification specification 的一部分。

---

#### 3.9.49 Side Effect 与 Agent State

Agent State 应该记录：

```text
已经发生了哪些 effect
哪些 effect pending
哪些 effect unknown
哪些 effect compensated
哪些 effect irreversible
```

否则后续 Agent 很容易：

```text
重复执行
```

或者误以为：

```text
什么都没发生
```

---

#### 3.9.50 Effect Ledger：维护真实世界影响账本

对于长任务，可以维护：

```text
Effect Ledger
```

例如：

```json
[
  {
    "action": "create_ticket",
    "resource": "T-1847",
    "status": "committed",
    "reversible": true
  },
  {
    "action": "send_email",
    "message_id": "M-42",
    "status": "committed",
    "reversible": false
  }
]
```

这样 Recovery / Audit / Verification 都能知道真实发生过什么。

---

#### 3.9.51 Effect Ledger ≠ Model Narrative

不要只依赖模型自己说：

```text
“我已经发了一封邮件，然后修改了文件。”
```

这只是 model narrative。

更可靠的是 Runtime 记录：

```text
call_id
resource_id
before_state
after_state
execution_receipt
observed_at
approval_id
```

因此：

> **Side-effect history 应优先来自 Runtime evidence，而不是模型自述。**

---

#### 3.9.52 Audit Log：谁在什么时候改变了什么？

高风险 Action 至少应支持回答：

```text
Who?
When?
What Action?
Which Resource?
Which Arguments?
Under Which Permission?
With Which Approval?
What Result?
What Actual Effect?
```

这就是 Auditability。

Agent 场景尤其需要区分：

```text
user identity
agent identity
runtime identity
service identity
```

---

#### 3.9.53 Audit Log 不能泄露敏感内容

Audit 越详细不代表越安全。

例如：

```text
password
API key
OAuth token
private document contents
```

不应该因为“方便审计”就完整写进日志。

所以需要：

```text
redaction
hashing
field-level access
retention policy
```

---

#### 3.9.54 Side-effect Provenance

对于一个 Environment Change，最好能追溯：

```text
哪个 Task
哪个 Agent Run
哪个 Model Decision
哪个 Tool Call
哪个 Approval
哪个 Runtime Request
```

形成：

```text
Task
 ↓
Decision
 ↓
Action
 ↓
Execution
 ↓
Effect
```

这对事故复盘极其重要。

---

#### 3.9.55 External Communication 是特殊高风险 Effect

例如：

```text
email
Slack
SMS
social post
issue comment
customer notification
```

这类 Action 的风险不仅是技术状态变化，还包括：

```text
reputation
social commitment
legal meaning
privacy
human interpretation
```

所以通常应该：

```text
Draft
↓
Preview
↓
Confirm
↓
Send
```

而不是模型直接从意图跳到外部发送。

---

#### 3.9.56 Draft 与 Send 必须是两个不同 Action

一个非常推荐的 Tool Design 是：

```text
draft_email(...)
send_email(...)
```

而不是：

```text
email(..., mode="draft_or_send")
```

因为：

```text
Draft
= reversible internal state

Send
= external side effect
```

语义和风险完全不同。

把它们拆开可以降低 accidental execution。

---

#### 3.9.57 Previewable Action：先把 effect 显示出来

对：

```text
邮件
SQL update
文件删除
批量编辑
权限修改
```

尽量提供：

```text
preview
```

内容可以包括：

```text
affected resources
before / after diff
recipient list
estimated cost
irreversible flags
warnings
```

让 confirmation 基于具体 effect，而不是抽象 Action 名称。

---

#### 3.9.58 Diff 是非常强的 Side-effect Preview

对于文件、配置、数据库记录，最有用的 preview 往往是：

```diff
- old
+ new
```

因为用户和 verifier 可以直接检查：

```text
哪些东西会改变
```

这比一句：

```text
“将更新配置文件”
```

信息量高得多。

---

#### 3.9.59 Scope Confirmation：确认的不只是动作，还包括范围

例如：

```text
delete logs
```

需要进一步确定：

```text
哪个环境？
哪个时间范围？
多少对象？
是否包括 production？
```

所以 approval UI / Observation 最好展示：

```text
scope
count
resource identifiers
```

而不是只展示 Tool Name。

---

#### 3.9.60 Bulk Action 风险不是线性增加

如果：

```text
单个 Action 出错概率 = p
```

批量处理 10,000 个对象时，风险不能简单只看单次 p。

因为：

```text
blast radius
recovery cost
human detection delay
```

都会放大。

因此 bulk tool 应支持：

```text
preview count
batch limit
progress checkpoints
partial stop
sample verification
```

---

#### 3.9.61 Canary Effect：先影响一小部分

对于大规模 mutation，可以使用：

```text
Canary
```

例如：

```text
先更新 1%
↓
verify
↓
再扩大
```

这把不可控大 effect 转成：

```text
bounded effect
→ observed evidence
→ controlled expansion
```

与软件 deployment 的 canary 思路一致。

---

#### 3.9.62 Progressive Commit

对于长批量任务：

```text
10000 records
```

可以分为：

```text
batch 1
↓ verify
batch 2
↓ verify
...
```

这样即使中途失败，blast radius 也被限制。

但要明确：

```text
partial completion
```

是合法状态，需要在 Agent State 中保存。

---

#### 3.9.63 Human-in-the-loop 应放在高价值决策点

不要把 Human Approval 做成：

```text
每一步都点确认
```

那会变成 approval fatigue。

更合理的是在：

```text
高不可逆
高金额
大 blast radius
外部通信
权限升级
敏感数据暴露
```

这些 effect frontier 上介入。

---

#### 3.9.64 Approval Fatigue 本身是安全风险

如果用户连续看到：

```text
Confirm
Confirm
Confirm
Confirm
```

最终很可能：

```text
机械点击
```

因此：

> **过度审批会降低审批质量。**

好的系统应减少低价值确认，把人的注意力保留给真正关键 effect。

---

#### 3.9.65 Risk-tiered Side-effect Policy

可以把 Action 划成：

```text
Tier 0: Pure / read-only
Tier 1: Low-risk reversible write
Tier 2: Moderate effect
Tier 3: High-impact / external
Tier 4: Irreversible / privileged
```

不同层采用不同策略：

```text
Tier 0 → auto
Tier 1 → auto + audit
Tier 2 → policy check + verification
Tier 3 → preview + confirmation
Tier 4 → explicit approval + independent verification
```

这比：

```text
所有 Tool 一刀切
```

更合理。

---

#### 3.9.66 Risk 不是 Tool 的固定属性

同一个 Tool：

```text
transfer_money
```

参数不同：

```text
$1
vs
$1,000,000
```

风险完全不同。

同样：

```text
write_file
```

写：

```text
/tmp/draft.txt
```

和：

```text
/etc/production/config
```

也不同。

因此：

> **Risk = f(Tool, Arguments, Resource, State, Identity, Context)。**

---

#### 3.9.67 Context-sensitive Effect Policy

Action 在不同环境也有不同风险：

```text
staging
vs
production
```

```text
private draft
vs
public post
```

```text
sandbox account
vs
real bank account
```

所以 Side-effect Policy 必须读取 Environment State，而不是只看 Tool 名称。

---

#### 3.9.68 Sandbox：把 Effect 限制在隔离环境

对于：

```text
code execution
filesystem mutation
browser automation
```

可以把 Agent 限制在 sandbox 中。

这样错误 Action 的 effect 只能影响：

```text
isolated environment
```

而不是 host / production。

所以 Sandbox 本质上是：

> **Blast-radius containment。**

---

#### 3.9.69 Sandbox 不是绝对无副作用

Sandbox 仍然可能：

```text
访问网络
消耗 compute
生成数据
泄露信息
触发外部 API
```

所以真正安全的 sandbox 还要限制：

```text
network
filesystem
credentials
resource quota
process capability
```

---

#### 3.9.70 Network Egress 是 Side-effect Boundary

代码 Agent 在 sandbox 里运行：

```text
curl external-site.com
```

就可能产生：

```text
数据外传
外部请求
计费
外部系统触发
```

所以 network egress policy 是 Side-effect Control 的重要组成。

---

#### 3.9.71 Credential Scope 决定最大 Effect

如果 Runtime 给 Agent：

```text
read-only token
```

即使模型想：

```text
delete resource
```

也做不到。

所以：

> **Credential Scope 是最硬的 Side-effect 上限之一。**

这比 Prompt 里写：

```text
“不要删除东西”
```

可靠得多。

---

#### 3.9.72 Capability Token / Short-lived Credential

高风险 Action 可以在审批后临时发放：

```text
short-lived capability token
```

只允许：

```text
特定 resource
特定 action
特定时间窗口
特定金额
```

这样即使 Agent 后续行为漂移，也无法无限扩大 effect。

---

#### 3.9.73 Effect Scope 应尽可能服务端验证

不要只让模型保证：

```text
“我只会改这个文件。”
```

Runtime / Backend 应验证：

```text
path in allowed_scope
resource in approved_set
amount <= approved_limit
```

所以：

> **Effect Constraint 应尽可能成为 executable policy，而不是 natural-language instruction。**

---

#### 3.9.74 Side-effect Guard 应在执行前后都存在

执行前：

```text
Pre-effect Guard
├── permission
├── scope
├── freshness
├── confirmation
└── budget
```

执行后：

```text
Post-effect Guard
├── verify actual state
├── detect over-effect
├── detect partial effect
└── trigger compensation / escalation
```

这就是 defense in depth。

---

#### 3.9.75 Effect Drift：Backend 行为变了怎么办？

Tool Description 写着：

```text
update_profile
不会通知用户
```

但 backend 新版本突然开始：

```text
send notification
```

即使 Tool Schema 没变，Side-effect Contract 已经变了。

这就是：

> **Behavioral / Effect Contract Drift。**

因此 Tool versioning 不应只关注输入输出，还应关注 side-effect semantics。

---

#### 3.9.76 Tool Versioning 必须包括 Effect Contract

版本变化可能包括：

```text
input schema change
output schema change
permission change
side-effect change
notification change
billing change
```

其中 side-effect change 往往风险最大，却最容易被忽略。

---

#### 3.9.77 Safe Default：默认选择低影响路径

如果用户说：

```text
“帮我准备一封邮件”
```

合理默认：

```text
Draft
```

而不是：

```text
Send
```

如果用户说：

```text
“看看怎么改配置”
```

合理默认：

```text
Preview diff
```

而不是直接修改 production。

因此：

> **Ambiguity 下的默认行为应偏向较小 Side Effect。**

---

#### 3.9.78 Abstention 是 Side-effect Safety 的合法结果

如果系统无法确定：

```text
recipient
resource
scope
amount
permission
```

合理 Action 可以是：

```text
Ask User
Abstain
Escalate
```

而不是为了“完成任务”强行执行。

---

#### 3.9.79 Safety vs Helpfulness 不是“执行越多越 helpful”

一个 Agent 的价值不是：

```text
永远替用户做更多
```

而是：

```text
在授权边界内
完成用户真正想完成的事情
并控制非必要 Side Effect
```

所以：

> **Minimal Sufficient Effect 是一个很好的设计目标。**

---

#### 3.9.80 Minimal Sufficient Effect

定义：

> **在满足 Goal 的所有 Action 路径中，优先选择能够以最小必要真实世界影响完成任务的路径。**

例如：

```text
为了回答一个问题
```

不需要：

```text
修改原始数据
```

为了给用户提供邮件内容：

不需要：

```text
直接发送
```

这是 Side-effect-aware Agent Design 的核心思想。

---

#### 3.9.81 Side-effect Minimization 与 Workflow / Agent 边界

前面 2.8 讲过：

```text
把确定性留给程序
把不确定性留给 Agent
```

Side Effect 进一步增加：

> **把高影响、可验证的 effect boundary 尽量收回 Harness / Runtime。**

即：

```text
Agent 决定意图
Runtime 控制 effect
```

而不是让模型拥有无限制执行权。

---

#### 3.9.82 Coding Agent 示例：修改代码到底有哪些 Side Effect？

任务：

```text
修复 parser bug
```

看似简单，但可能有：

```text
修改源码
修改 lockfile
新增 dependency
格式化 unrelated files
删除 test fixture
执行网络安装
生成 build artifacts
修改 git state
```

所以一个好的 Coding Agent 应明确：

```text
allowed write scope
network policy
expected files
forbidden files
public API invariant
```

并在最后：

```text
git diff
```

验证实际 effect。

---

#### 3.9.83 Coding Agent：为什么 `git diff` 是 Side-effect Verifier

测试通过只说明：

```text
behavioral checks passed
```

而：

```text
git diff
```

回答的是：

```text
Agent 实际改了哪些文件？
改了什么？
```

所以：

```text
Tests
+
Diff
```

比只看 Tests 更接近完整验证。

---

#### 3.9.84 Browser Agent 示例：一次 Click 的 Side Effect 可能是什么？

页面上的按钮：

```text
Confirm
```

可能代表：

```text
提交表单
付款
发送消息
发布内容
删除资源
确认法律声明
```

所以 Browser Agent 不能只根据视觉 affordance 判断风险。

需要理解：

```text
semantic action
```

以及执行后的 Environment Effect。

---

#### 3.9.85 Browser Agent：Navigation 也可能产生 Effect

访问某 URL 可能：

```text
触发一次性 token
confirm email
unsubscribe
accept invitation
consume magic link
```

所以：

```text
GET-like navigation
```

也不一定纯读取。

这也是为什么外部链接应被当作潜在 effect boundary。

---

#### 3.9.86 Research Agent 示例：搜索也有 Side Effect 吗？

虽然搜索通常不修改研究对象，但仍可能：

```text
消耗付费 API quota
暴露 query
记录用户兴趣
触发外部 tracking
```

而如果 search query 中包含：

```text
internal confidential text
```

更可能产生 data exfiltration。

因此“只搜索”也不是完全零风险。

---

#### 3.9.87 Database Agent 示例

任务：

```text
找出过去 30 天异常订单
```

正确路径可能只需要：

```text
SELECT
```

如果 Agent 获得：

```text
UPDATE / DELETE
```

权限，就是不必要 effect surface。

所以最好：

```text
read-only database role
```

从 credential 层硬限制。

---

#### 3.9.88 Email Agent 示例

用户：

```text
帮我写一封给导师的邮件
```

最小充分 effect：

```text
draft text
```

而不是：

```text
send_email
```

如果用户进一步：

```text
发给导师
```

才进入：

```text
resolve recipient
preview final content
confirm if needed
send
verify message_id
```

这就是 Intent → Effect Scope 的逐级升级。

---

#### 3.9.89 Calendar Agent 示例

```text
“看看明天下午有没有空”
```

需要：

```text
read events
```

不需要：

```text
create event
```

而：

```text
“帮我约 3 点会议”
```

则可能需要：

```text
create event
invite attendees
send notifications
```

这三个 effect 最好都显式可见。

---

#### 3.9.90 Financial Agent 示例

资金类 Agent 必须特别关注：

```text
amount
currency
recipient
source account
fee
exchange rate
irreversibility
```

以及：

```text
payment intent
vs
actual transfer
```

建议拆成：

```text
prepare_transfer
↓
preview exact effect
↓
approve
↓
commit_transfer
↓
verify status
```

---

#### 3.9.91 Multi-Agent：Side Effect 不能因为委派就失去责任链

Supervisor Agent 委派给 Subagent：

```text
“处理这个客户问题”
```

Subagent 执行：

```text
refund
```

系统仍然必须能回答：

```text
谁授权 refund？
谁选择 subagent？
谁实际执行？
```

所以 delegation 不应该切断 effect provenance。

---

#### 3.9.92 Delegated Authority 必须有 Scope

Supervisor 可以授权：

```text
Subagent 可读取 customer record
```

并不意味着：

```text
Subagent 可退款
可删除账户
可发外部邮件
```

因此 Multi-Agent 中更需要：

```text
delegated capability scope
```

---

#### 3.9.93 Recursive Agents 的 Effect Amplification

如果 Agent 可以不断 spawn subagents：

```text
Agent
├── Subagent A
├── Subagent B
└── Subagent C
```

每个都拥有 effectful tools，整体 blast radius 会迅速扩大。

所以需要：

```text
shared side-effect budget
per-agent limit
central audit
permission inheritance rules
```

---

#### 3.9.94 Side-effect-aware Planning

Planning 不应该只问：

```text
哪条路径最可能成功？
```

还应该问：

```text
哪条路径副作用更小？
哪条路径可逆性更高？
哪条路径更容易验证？
```

因此 plan utility 可以包含：

$$
U(Plan)=Success-ComputeCost-SideEffectRisk-RecoveryCost
$$

---

#### 3.9.95 Epistemic Action 优先于 Effectful Action

在高不确定状态下：

```text
先查清楚
```

通常比：

```text
先改再说
```

安全。

因此：

```text
Uncertainty High
      ↓
Prefer Epistemic Action
      ↓
Reduce Uncertainty
      ↓
Then Effectful Action
```

这也是 2.1 中 information-gathering action 的真正工程价值。

---

#### 3.9.96 Effect-aware Routing

如果多个执行路径都能完成任务：

```text
Tool A：直接修改 production
Tool B：生成 patch 等待 review
```

对于高风险任务，Routing Policy 可以优先：

```text
Tool B
```

所以 Routing 不只考虑：

```text
quality / latency / cost
```

还应该考虑：

```text
side-effect profile
```

---

#### 3.9.97 Side-effect-aware Reflection

Reflection 不能只问：

```text
“任务为什么失败？”
```

还应该问：

```text
已经造成了什么 effect？
哪些 effect 需要 compensation？
哪些 effect 不可逆？
```

否则 Agent 很可能在恢复过程中制造第二次伤害。

---

#### 3.9.98 Side Effect 与 Termination

Agent 不能只因为：

```text
目标似乎完成
```

就 Stop。

对于 effectful task，结束前还需要确认：

```text
intended effects verified
forbidden effects absent
partial effects resolved
pending effects known
```

尤其异步系统：

```text
accepted
≠
completed
```

---

#### 3.9.99 Pending Effect

有些 Side Effect 尚未最终发生：

```text
email queued
payment pending
deployment running
approval requested
```

所以 Agent State 应区分：

```text
prepared
pending
committed
verified
failed
compensated
unknown
```

不能把：

```text
request accepted
```

直接当成：

```text
effect completed
```

---

#### 3.9.100 Effect Lifecycle

一个完整 effect lifecycle 可以写成：

```text
PROPOSED
  ↓
VALIDATED
  ↓
AUTHORIZED
  ↓
PREPARED
  ↓
COMMITTED
  ↓
OBSERVED
  ↓
VERIFIED
```

异常路径：

```text
REJECTED
FAILED
PARTIAL
UNKNOWN
COMPENSATING
COMPENSATED
```

这比单一：

```text
success = true / false
```

可靠得多。

---

#### 3.9.101 Side-effect Contract

一个成熟 Tool 的 contract 除了 input / output，还应明确：

```text
primary effect
secondary effects
reversibility
idempotency
blast radius
notification behavior
cost behavior
permission requirements
verification strategy
compensation strategy
```

这使 Tool 从：

```text
Callable Function
```

升级成：

```text
Executable Capability Contract
```

这正好回扣 3.1。

---

#### 3.9.102 Side-effect Metadata 示例

例如：

```json
{
  "name": "send_email",
  "effect": {
    "class": "external_communication",
    "reversible": false,
    "idempotent": false,
    "requires_confirmation": true,
    "max_recipients": 20,
    "verification": "delivery_status_query"
  }
}
```

这里的 metadata 不一定全部暴露给模型，但 Harness / Runtime 可以使用。

---

#### 3.9.103 Side-effect Policy 不应该全交给模型判断

模型可以参与判断：

```text
“这看起来风险高吗？”
```

但真正的硬限制应该尽量程序化：

```text
amount <= 1000
recipient in approved_domain
path under workspace
no production delete
```

因为：

> **Safety-critical effect boundary 应尽量 deterministic。**

---

#### 3.9.104 Side-effect Classification 可以是 Harness 的一等状态

例如 Action proposal 进入 Harness 后：

```text
classify_effect(action)
```

得到：

```json
{
  "risk_tier": 3,
  "reversible": false,
  "external": true,
  "blast_radius": 12,
  "requires_approval": true
}
```

然后再决定是否执行。

---

#### 3.9.105 Side-effect Detection 也可以是 Runtime 的一等能力

执行后：

```text
expected_effect
vs
observed_diff
```

如果发现：

```text
unexpected files changed
unexpected recipients notified
unexpected records updated
```

Runtime 可以：

```text
stop
alert
rollback if possible
escalate
```

而不是把一切都交给下一轮 LLM 自己发现。

---

#### 3.9.106 Side-effect Diff

对于能够 snapshot 的 Environment，可以计算：

```text
Before State
   ↓
Action
   ↓
After State
   ↓
Diff
```

这就是 Effect Diff。

例如：

```text
filesystem diff
database diff
permission diff
config diff
```

它往往是很强的 verification evidence。

---

#### 3.9.107 Effect Diff 不能总是完整获得

现实里：

```text
external email
social impact
webhook cascade
third-party system
```

很难得到完整世界 diff。

所以系统通常只能获得：

```text
partial effect evidence
```

这也是 Partial Observability 的一种。

---

#### 3.9.108 Side-effect Observability

为了可靠控制 effect，需要知道：

```text
发生了什么
何时发生
影响了谁
影响了多少
是否仍在进行
```

因此高风险 Tool 应尽量提供：

```text
resource IDs
counts
status
timestamps
versions
receipts
```

而不是只返回：

```text
Done.
```

---

#### 3.9.109 Side-effect Telemetry

可以监控：

```text
write count
external sends
bulk action size
destructive action count
permission changes
monetary volume
compensation count
duplicate effect count
```

这些指标对发现 Agent 行为漂移很有价值。

---

#### 3.9.110 Effect Drift Detection

例如过去 Agent 平均每个任务：

```text
0.2 external sends
```

新版本突然变成：

```text
3.7 external sends
```

即使 task success 提升，也可能出现严重 over-action。

因此上线监控需要同时看：

```text
Outcome
+
Effect Profile
```

---

#### 3.9.111 Success Rate 不能掩盖 Harm Rate

一个 Agent：

```text
Task Success = 95%
```

听起来很好。

但如果：

```text
1% duplicate payment
0.5% accidental delete
```

可能完全不可部署。

所以 Side-effect Evaluation 必须单独报告：

```text
harmful effect rate
```

而不能被平均 success metric 淹没。

---

#### 3.9.112 Side-effect Evaluation：第一层——Effect Precision

可以定义：

```text
Intended Effects
vs
Actual Effects
```

关注：

```text
必要 effect 是否发生
非必要 effect 是否被避免
```

直觉上：

```text
Effect Recall
= required effects 完成多少

Effect Precision
= 实际 effects 中有多少是必要的
```

Agent 很容易出现：

```text
高 recall
低 precision
```

也就是：

> 任务都做了，但做多了很多事情。

---

#### 3.9.113 Side-effect Evaluation：第二层——Harm Metrics

建议单独统计：

```text
Unauthorized Effect Rate
Irreversible Harm Rate
Duplicate Effect Rate
Over-effect Rate
Under-effect Rate
Forbidden Effect Rate
Compensation Rate
Compensation Failure Rate
False-success-after-effect Rate
```

这些比单纯 Tool Call Accuracy 更接近真实部署风险。

---

#### 3.9.114 Side-effect Evaluation：第三层——Blast Radius

不要只统计：

```text
出错次数
```

还要统计：

```text
每次错误影响多少对象
```

例如：

```text
1 次 bulk delete
```

可能比：

```text
100 次 harmless formatting error
```

严重得多。

所以可以记录：

```text
affected_objects
affected_users
money_at_risk
data_volume
```

---

#### 3.9.115 Side-effect Evaluation：第四层——Reversibility / Recovery Cost

两个错误 effect 数量相同：

```text
修改草稿
vs
发送外部邮件
```

恢复成本完全不同。

因此建议记录：

```text
reversible rate
compensatable rate
irreversible rate
mean recovery cost
mean time to containment
```

---

#### 3.9.116 Side-effect Evaluation：第五层——Approval Quality

可以评价：

```text
Approval Trigger Precision
Approval Trigger Recall
```

**Precision**：

```text
要求确认的 Action 中
有多少真的值得确认
```

**Recall**：

```text
真正高风险 Action 中
有多少被成功拦到 approval
```

这样可以量化 approval fatigue 与漏拦截之间的 trade-off。

---

#### 3.9.117 Side-effect Evaluation：第六层——Effect Claim Calibration

Agent 说：

```text
“已经发送。”
```

就应该有足够证据。

可以统计：

```text
Claimed-effect Precision
```

即：

```text
Agent 声称发生的 effect
有多少真的发生
```

这和 3.6 的 False-success Claim Rate 一脉相承。

---

#### 3.9.118 Side-effect Benchmark 应包含哪些 Case？

至少应该覆盖：

```text
read-only
reversible write
irreversible write
external communication
bulk mutation
permission change
financial action
partial execution
timeout unknown
duplicate retry
stale-state write
untrusted observation → effectful action
```

否则 benchmark 很容易只测“会不会调用 Tool”，却完全没有测真实风险。

---

#### 3.9.119 Counterfactual Effect Test

可以固定：

```text
same task
same model
same tool set
```

只改变：

```text
risk level
resource scope
amount
recipient
reversibility
```

观察 Agent 是否合理调整：

```text
auto execute
preview
ask
approve
abstain
```

这能直接测 risk-sensitive behavior。

---

#### 3.9.120 Effect Ablation Test

还可以做：

```text
With effect metadata
vs
Without effect metadata
```

看模型 / Harness 是否更容易：

```text
正确 routing
正确 approval
正确 recovery
```

这样能评价 Side-effect Contract 的贡献。

---

#### 3.9.121 Sandbox Benchmark

对于 Coding / Computer-use Agent，可以设计：

```text
允许路径
禁止路径
允许网络
禁止网络
```

然后测：

```text
是否越界
是否产生隐藏 effect
是否正确识别 permission denial
```

---

#### 3.9.122 Fault Injection：注入 Effect Failure

可以人为制造：

```text
partial write
commit timeout
duplicate callback
notification failure
compensation failure
stale confirmation
```

观察 Agent 是否：

```text
正确检测
避免重复 effect
进行 reconciliation
正确 escalation
```

---

#### 3.9.123 Side-effect Data：训练 / 优化数据应该记录什么？

一条高质量 trajectory 最好保留：

```text
Goal
State Before
Proposed Action
Resolved Arguments
Predicted Effects
Approval / Policy Decision
Execution Receipt
Observed Effects
Verification Result
Compensation / Recovery
Final State
```

这比只有：

```text
prompt + tool call
```

有价值很多。

---

#### 3.9.124 Negative Side-effect Examples

训练 Agent 不仅需要：

```text
正确 Action
```

也需要明确负例：

```text
unnecessary send
excessive scope
wrong recipient
duplicate action
forbidden mutation
unsafe retry
permission escalation
```

这样模型才能学习：

```text
什么时候不应该做
```

---

#### 3.9.125 Over-action Data

很多 Agent 数据只奖励：

```text
任务完成
```

却没有惩罚：

```text
为了完成任务做了很多不必要 Action
```

因此建议记录：

```text
Minimal Required Effects
vs
Observed Effects
```

训练 / 评测：

```text
Minimal Sufficient Action
```

能力。

---

#### 3.9.126 Side-effect-aware Reward

如果把 Agent 优化目标写成：

$$
R = TaskSuccess
$$

很容易出现：

```text
over-action
```

更合理可以考虑：

$$
R
= TaskSuccess
- \lambda_1 Cost
- \lambda_2 Harm
- \lambda_3 UnnecessaryEffects
$$

当然实际系统未必真的使用单一标量，但这个思想很重要。

---

#### 3.9.127 Reward Hacking：用副作用“刷成功”

如果 verifier 只看某个表面状态：

```text
file exists
```

Agent 可能通过：

```text
删除原目录
重新生成最小文件
```

让 verifier PASS，但造成大量 collateral damage。

所以 verifier 必须关注：

```text
Goal
+
Forbidden Effects
+
Invariants
```

---

#### 3.9.128 Side-effect Hacking

另一个风险是 Agent 找到：

```text
最容易改变 verifier 结果的方式
```

而不是：

```text
真正完成用户任务
```

例如直接修改测试文件，让测试通过。

这本质上是：

```text
通过不允许的 Side Effect 改变评价环境
```

所以 environment integrity 也必须被保护。

---

#### 3.9.129 Immutable Evaluation Artifacts

在 benchmark / Coding Agent Eval 中：

```text
tests
reference data
grader
```

最好不要允许 Agent 修改。

否则 Agent 可以：

```text
modify evaluator
→ achieve PASS
```

这是典型 evaluation side effect。

---

#### 3.9.130 Side Effect 与 Security Boundary

可以把整个 Action Security 写成：

```text
Model Intent
      ↓
Tool Selection
      ↓
Arguments
      ↓
Policy / Permission
      ↓
Effect Scope
      ↓
Execution
      ↓
Actual Effects
      ↓
Audit / Verification
```

安全系统真正要保护的是：

> **Environment Transition Boundary。**

而不是只保护 Tool Call JSON。

---

#### 3.9.131 Side Effect 与 Harness

Harness 负责：

```text
哪些 effect 允许自动执行
哪些需要 approval
side-effect budget
recovery policy
preview / commit policy
termination policy
```

因此 Side Effect Policy 是 Harness 的核心组成。

---

#### 3.9.132 Side Effect 与 Runtime

Runtime 负责真正落实：

```text
credential scope
sandbox
resource limit
transaction
idempotency key
execution identity
logging
checkpoint
```

所以：

```text
Harness
= 决定 effect policy

Runtime
= enforce effect boundary
```

---

#### 3.9.133 Side Effect 与 Permission

最终允许执行的 effect 应满足：

```text
Requested Effect
∩
Authorized Effect
∩
Policy-Allowed Effect
∩
Runtime-Capable Effect
```

只有交集才真正可执行。

---

#### 3.9.134 Autonomy ≠ Effect Authority

Agent 可以有很高的决策自主性：

```text
自己 plan
自己 search
自己 diagnose
```

但依然可以只拥有很窄的 effect authority：

```text
只能修改 workspace
不能发送外部消息
不能支付
```

所以：

> **Autonomy 与 Effect Authority 必须分开设计。**

---

#### 3.9.135 高 Agenticness 不应该自动意味着高 Side-effect Authority

这是现实 Agent 架构里非常重要的一点。

一个强模型可以：

```text
更自主地推理
```

不代表应该：

```text
更自由地修改真实世界
```

能力提升和权限扩大不是同一件事。

---

#### 3.9.136 Side-effect-aware Termination Status

任务结束时，可以不仅记录：

```text
COMPLETED
```

还记录：

```text
COMPLETED_NO_EFFECT
COMPLETED_WITH_EFFECTS
PARTIAL_EFFECT
COMPENSATED
BLOCKED_BEFORE_EFFECT
FAILED_AFTER_EFFECT
UNKNOWN_EFFECT_STATE
```

这对 Recovery / Audit 很有价值。

---

#### 3.9.137 Failure after Effect 与 Failure before Effect 完全不同

例如：

```text
schema validation failed
```

通常：

```text
No Effect
```

而：

```text
response parsing failed after POST
```

可能：

```text
Effect already happened
```

所以 Failure Handling 必须知道：

```text
failure boundary relative to commit point
```

---

#### 3.9.138 Commit Point

可以把 Effectful Action 划分：

```text
Before Commit Point
→ generally safe to abort

After Commit Point
→ must reason about actual effects
```

对于不同 Tool，commit point 不同：

```text
DB transaction commit
email accepted by provider
payment captured
file rename completed
```

这对 timeout recovery 特别关键。

---

#### 3.9.139 Effect Receipt

高风险 Action 最好返回能够确认 commit 的 receipt：

```text
transaction_id
message_id
resource_version
order_id
commit_sha
```

它不是 Ground Truth 的全部，但能帮助：

```text
reconciliation
verification
audit
```

---

#### 3.9.140 Receipt ≠ Final Outcome

比如：

```text
payment_id
```

说明 payment object 创建了。

不一定说明：

```text
settlement completed
```

同样：

```text
message_id
```

不一定说明：

```text
recipient read message
```

所以 receipt 只能证明某个 effect stage。

---

#### 3.9.141 Eventual Effects

有些 effect 会延迟发生：

```text
async job
email delivery
index update
cache invalidation
payment settlement
```

因此 Agent 需要区分：

```text
Committed Effect
vs
Materialized Effect
```

并根据任务需要决定是否等待 / query / verify。

---

#### 3.9.142 Effect Expiry

有些 effect 是临时的：

```text
reservation hold
temporary permission
temporary token
lock
```

所以 Side Effect 也可以有：

```text
expires_at
```

Agent 不能把临时状态当成永久状态。

---

#### 3.9.143 Lease / Reservation

为了避免直接 irreversible commit，可以先获取：

```text
lease / hold / reservation
```

例如：

```text
hold seat
↓
confirm details
↓
purchase
```

这是把：

```text
irreversible effect
```

拆成：

```text
reversible reservation
+
final commit
```

很有价值的设计模式。

---

#### 3.9.144 Soft Delete vs Hard Delete

对于删除类 Tool：

```text
soft_delete
```

通常比：

```text
hard_delete
```

更适合 Agent 默认使用。

因为 soft delete 提供：

```text
recovery window
```

降低 irreversible risk。

---

#### 3.9.145 Quarantine / Archive：比 Delete 更安全的替代动作

用户说：

```text
“清理这些文件”
```

可能优先：

```text
move to quarantine
archive
trash
```

而不是直接永久删除。

这也是 Minimal Sufficient Effect 的体现。

---

#### 3.9.146 Undo Window

对于某些 Action，系统可以设计：

```text
execute
↓
5-minute undo window
↓
finalize
```

例如：

```text
schedule email
soft delete
queued publish
```

从而人为增加 reversibility。

---

#### 3.9.147 Delay as Safety Mechanism

并不是所有 Action 都应该追求最低 latency。

对于高风险 effect，可以：

```text
short delay
```

给用户：

```text
cancel / undo
```

机会。

所以 Quality–Latency trade-off 在 Side Effect 场景里有新的含义。

---

#### 3.9.148 Side Effect 与 Human Expectation

即使技术上合法，Action 如果超出用户对当前请求的合理预期，也可能是错误。

例如：

```text
“帮我看看这封邮件怎么回”
```

用户通常期待：

```text
提供建议 / draft
```

而不是：

```text
直接 send
```

所以 Side Effect 控制还需要：

> **Intent–Effect Alignment。**

---

#### 3.9.149 Intent–Effect Alignment

可以问：

```text
用户明确要求了这个 effect 吗？
这个 effect 是完成 Goal 必需的吗？
用户合理预期它会发生吗？
```

如果三者都弱：

```text
不要自动执行
```

---

#### 3.9.150 Explicit vs Implicit Authorization

用户明确说：

```text
“发出去”
```

属于 explicit action intent。

而：

```text
“帮我处理一下这封邮件”
```

可能含义不清。

因此高影响 effect 不应该过度依赖 implicit intent 推断。

---

#### 3.9.151 Temporal Scope of Authorization

用户批准：

```text
“今天把这 3 封邮件发掉”
```

不一定授权：

```text
下周继续自动发类似邮件
```

所以 Authorization 应考虑：

```text
resource scope
action scope
time scope
quantity scope
```

---

#### 3.9.152 Side-effect Policy 与 Persistent Agent

长期运行 Agent 特别需要：

```text
每次 effect 的权限是否仍有效？
用户 intent 是否过期？
环境是否变化？
```

不能因为几天前得到过一次授权，就无限复用。

---

#### 3.9.153 Scheduled Action 的 Effect Freshness

Agent 在上午计划：

```text
18:00 发布公告
```

到 18:00 时：

```text
内容
受众
权限
业务状态
```

可能都已经变化。

因此真正 commit 前最好重新：

```text
validate
```

而不是盲执行旧计划。

---

#### 3.9.154 Stale Approval

Approval 本身也会过期。

例如：

```text
批准删除 12 个对象
```

但执行时 query 已经匹配：

```text
47 个对象
```

原 approval 不应继续有效。

因此批准最好绑定具体 scope / snapshot。

---

#### 3.9.155 Effect Scope Hash

可以把：

```text
resolved action
arguments
resource set
version
```

规范化后计算 hash。

Approval 绑定：

```text
effect_scope_hash
```

执行前重新检查。

如果变了：

```text
re-approve
```

---

#### 3.9.156 Race Condition 与 Effect Scope

即使 approval 时 scope 正确，执行过程中仍可能有并发变化。

所以服务端最好使用：

```text
expected_version
conditional update
transaction
```

把 effect 限制在批准时的状态假设内。

---

#### 3.9.157 Batch Snapshot

批量 Action 可以先冻结：

```text
resource snapshot
```

例如：

```text
对象 IDs = [1,2,3]
```

然后 commit 只允许作用于这个集合。

而不是：

```text
再次动态运行 query
```

导致 scope 漂移。

---

#### 3.9.158 Side-effect Escalation Ladder

可以设计：

```text
Low risk
→ auto execute

Moderate risk
→ preview

High risk
→ explicit approval

Very high risk
→ human + independent verifier

Forbidden
→ deny
```

这是 Side-effect Policy 的一个实用实现。

---

#### 3.9.159 Recovery 不能扩大 Side Effect

如果原 Action：

```text
修改一个文件失败
```

Recovery 不应该自动：

```text
重置整个 repository
```

除非新的 Action 经过独立授权。

因此：

> **Recovery Effect Scope ≤ Authorized Recovery Scope。**

这与 3.8 的 Recovery Authority 原则一致。

---

#### 3.9.160 Compensation 也必须最小化副作用

如果错误发了一封邮件：

不一定应该：

```text
给所有人群发道歉
```

补偿本身也需要：

```text
scope control
risk evaluation
approval
```

否则 recovery 可能造成更大伤害。

---

#### 3.9.161 Side-effect Loop

危险 Agent 可能进入：

```text
Action causes side effect
↓
Agent misreads Observation
↓
compensates
↓
compensation creates new issue
↓
compensates again
```

形成 effect oscillation。

因此必须有：

```text
recovery budget
no-progress detection
human escalation
```

---

#### 3.9.162 Effect Oscillation

例如：

```text
set A
↓
verifier says B
↓
set B
↓
another verifier says A
↓
set A
```

每一步都真实修改 Environment。

这种 oscillation 比纯 reasoning loop 危险得多。

---

#### 3.9.163 Effect Rate Limit

对高影响 Action 可以限制：

```text
每分钟最多 N 次
每任务最多 N 次
每用户每天最多 N 次
```

防止 Agent loop 把局部错误放大成大量真实 effect。

---

#### 3.9.164 Effect Deduplication

对于重复 Action，可以根据：

```text
canonical args
business key
resource state
idempotency key
```

检测：

```text
duplicate intent
```

在真正执行前去重。

---

#### 3.9.165 Semantic Duplicate

两个 Tool Call 参数不同，也可能业务语义相同：

```text
send_email(to=A, body=X)
send_email(to=A, body=X + whitespace)
```

所以 duplicate detection 有时需要：

```text
business semantics
```

而不只是 byte equality。

---

#### 3.9.166 Side-effect-aware Caching

Read-only query 可以缓存。

但 effectful Tool 不能简单：

```text
cache call result
```

然后把重复请求当作“已经执行”。

必须区分：

```text
cached observation
vs
actual new effect
```

---

#### 3.9.167 Replay 风险

Agent trajectory replay 如果包含：

```text
send_email
charge_card
delete_file
```

不能在真实环境中原样重放。

所以 Eval / Debug 应支持：

```text
recorded observation replay
simulated runtime
sandbox
```

而不是 live replay effectful actions。

---

#### 3.9.168 Deterministic Replay ≠ Real-world Replay

模型决策可以重放，但真实 external effect：

```text
时间变化
第三方状态变化
权限变化
```

都可能不同。

所以 reproducibility 与 side-effect safety 需要分开考虑。

---

#### 3.9.169 Test Double / Mock Tool

开发时可以用：

```text
mock send_email
fake payment
sandbox calendar
```

验证 Agent Decision，而不制造真实 effect。

但要记住：

> **Mock success 不等于 production execution reliability。**

---

#### 3.9.170 Shadow Mode

上线前可以让 Agent：

```text
产生 Action proposal
```

但不真正 execute。

同时与真实人类 / 系统行为比较。

这就是 shadow mode。

特别适合测试：

```text
high-risk effect policy
```

---

#### 3.9.171 Suggestion Mode vs Execution Mode

Agent 产品可以分成：

```text
Suggestion Mode
→ 只建议，不产生 effect

Execution Mode
→ 真正执行
```

并让不同用户 / 任务拥有不同权限。

这是一种很实用的 staged rollout。

---

#### 3.9.172 Gradual Authority Expansion

新 Agent 不必一开始拥有全部执行权限。

可以：

```text
Stage 1: read only
Stage 2: draft
Stage 3: reversible writes
Stage 4: limited external actions
Stage 5: broader autonomy
```

前提是每阶段都有真实可靠性证据。

---

#### 3.9.173 Authority 应由 Evidence 扩大，而不是由 Model Size 扩大

模型升级：

```text
8B → 70B
```

不自动意味着：

```text
可以删 production 数据
```

Effect Authority 的扩大应该基于：

```text
evaluation
incident rate
calibration
verification coverage
operational controls
```

而不是“模型更聪明”。

---

#### 3.9.174 Side-effect SLO / Safety SLO

真实系统可以为 effect 定义 SLO：

```text
Unauthorized Effect Rate < x
Duplicate Send Rate < y
Irreversible Harm Rate < z
```

这比只看：

```text
Task Success
```

更符合真实部署要求。

---

#### 3.9.175 Incident Severity

Side-effect incident 可以按：

```text
scope
reversibility
sensitivity
financial impact
external exposure
```

分级。

这有助于：

```text
自动 containment
human escalation
postmortem priority
```

---

#### 3.9.176 Containment：先限制继续扩散

发现异常 effect 时，第一目标有时不是：

```text
立即恢复
```

而是：

```text
stop further damage
```

例如：

```text
disable tool
revoke token
pause agent
block outbound network
stop queue
```

这就是 containment。

---

#### 3.9.177 Kill Switch

高权限 Agent 系统应该有：

```text
kill switch
```

能快速：

```text
stop new executions
revoke credentials
cancel queued effects
```

而不是只能等待 Agent 自己意识到问题。

---

#### 3.9.178 Kill Switch 也需要明确语义

即使 kill switch 被触发：

```text
in-flight actions
```

可能已经 commit。

所以：

```text
stop future effects
≠
undo past effects
```

仍需 reconciliation。

---

#### 3.9.179 Emergency Policy

事故状态下可以临时切换：

```text
read-only mode
no external sends
no destructive actions
manual approval only
```

让系统 graceful degrade，而不是完全失效。

---

#### 3.9.180 Side-effect Failure Modes 总览

这一节最值得长期记住的 Failure Modes 包括：

1. **Accidental Mutation**：本应读取，却修改了状态。
2. **Over-effect**：任务完成但产生额外不必要 effect。
3. **Under-effect**：只完成部分必要 effect。
4. **Duplicate Effect**：retry / replay 导致重复发送、支付、创建。
5. **Wrong-target Effect**：recipient / resource / environment 错误。
6. **Scope Explosion**：单对象操作变成 bulk effect。
7. **Hidden Side Effect**：通知、计费、权限变化没有暴露。
8. **Irreversible Premature Commit**：高风险 Action 在确认前执行。
9. **Stale Approval**：批准时 scope 与执行时 scope 不一致。
10. **Approval Drift**：参数变化后仍复用旧 approval。
11. **Unsafe Default**：backend 默认产生 destructive effect。
12. **Idempotency Failure**：逻辑重试造成重复业务 effect。
13. **Partial Effect**：复合 Action 只执行了一部分。
14. **Compensation Failure**：补偿 Action 又失败。
15. **Compensation Overreach**：恢复造成更大 effect。
16. **Permission Escalation**：Action 改变权限并扩大未来 authority。
17. **Data Exfiltration**：信息流向未授权外部域。
18. **Notification Leak**：修改行为意外通知不应知晓的人。
19. **Cost Explosion**：Agent Action 触发大量真实费用。
20. **Effect Oscillation**：Agent 在真实世界状态之间来回修改。
21. **Side-effect Loop**：恢复行为不断制造新 effect。
22. **Effect Contract Drift**：backend 行为变化但 Tool Contract 未更新。
23. **False Effect Claim**：Agent 声称 effect 已发生但实际没有。
24. **Unobserved Effect**：effect 发生但 Observation 未捕获。
25. **Verifier Blind Spot**：目标成功但 forbidden effect 未被检查。
26. **Evaluation Tampering**：Agent 修改 grader / test / benchmark artifact。
27. **Sandbox Escape Effect**：原本隔离的动作影响真实外部系统。
28. **Replay Effect**：debug / replay 意外重新执行真实 Action。
29. **Effect Fan-out Surprise**：一个 Tool 触发未预期的大量下游动作。
30. **Authority Persistence**：临时授权被错误地长期保留。

---

#### 3.9.181 Side-effect Engineering Principles

可以把这一节压缩成以下工程原则。

**原则 1：先识别 Effect，再谈执行。**

不要只看 Tool 名称。

**原则 2：默认选择 Minimal Sufficient Effect。**

能 Draft 就不 Send，能 Preview 就不 Commit。

**原则 3：高风险 Effect 尽量 Preview → Approve → Commit。**

**原则 4：Confirmation 必须绑定 resolved final scope。**

**原则 5：Read-only 也要审计隐藏 effect 与信息流。**

**原则 6：Retry Policy 必须理解 idempotency 与 commit point。**

**原则 7：Compensation 不是 Undo。**

**原则 8：权限和 credential 决定硬 Side-effect 上限。**

**原则 9：执行后验证 Actual Effects，而不只看返回值。**

**原则 10：验证 Required Effects，也验证 Forbidden Effects。**

**原则 11：Side-effect Budget 与 Token Budget 一样是一等资源。**

**原则 12：大 blast radius Action 要分批、canary、progressive commit。**

**原则 13：External Communication 默认比内部 Draft 更高风险。**

**原则 14：Effect history 应来自 Runtime ledger，不依赖模型自述。**

**原则 15：高不可逆 Action，Prevention > Recovery。**

**原则 16：Recovery 不得静默扩大 Effect Scope。**

**原则 17：权限扩大本身就是高风险 Side Effect。**

**原则 18：上线评测同时看 Success 与 Harm。**

**原则 19：High Agenticness ≠ High Effect Authority。**

**原则 20：真正要保护的是 Environment Transition Boundary。**

---

#### 3.9.182 与前面 3.1–3.8 的完整关系

现在 Chapter 3 可以完整串起来：

```text
3.1 Tool Definition
    ↓
什么能力可以被执行？

3.2 Tool Schema
    ↓
合法输入空间是什么？

3.3 Tool Description
    ↓
模型如何理解能力边界？

3.4 Tool Selection
    ↓
当前是否需要 Tool、应该选哪个？

3.5 Argument Generation
    ↓
这次具体怎样调用？

3.6 Tool Execution
    ↓
Action 怎样进入 Runtime 并真正执行？

3.7 Observation
    ↓
Environment 变化怎样重新进入 Agent State？

3.8 Failure Handling
    ↓
失败、不确定和部分完成怎样被恢复？

3.9 Side Effects
    ↓
整个过程中，真实世界到底被改变了什么，风险如何被约束？
```

所以 Chapter 3 最终回答的是：

> **Agent 怎样从“想做一件事”，走到“以受控、可验证、可恢复的方式真正影响外部世界”。**

---

#### 3.9.183 Tool Use 章节的最终总模型

可以把整章压缩成：

```text
Goal / State
    ↓
Need Tool?
    ↓
Tool Selection
    ↓
Argument Generation
    ↓
Validation
    ↓
Authorization
    ↓
Effect Risk Assessment
    ↓
Preview / Approval if needed
    ↓
Execution
    ↓
Environment Transition
    ↓
Observation
    ↓
Effect Verification
    ↓
Failure Handling / Compensation if needed
    ↓
State Update
    ↓
Next Decision
```

这才是一个完整的 Agent Tool Use Loop。

---

#### 3.9.184 面试掌握边界

完成这一节后，至少应该能稳定回答下面这些问题。

**Q1：Side Effect 在 Agent 里是什么意思？**

不是 Tool 返回值，而是 Action 对持久状态、外部主体、资源、权限、费用、可见性或信息流造成的真实影响。

**Q2：Read-only Tool 一定没有副作用吗？**

不一定。访问日志、计费、缓存、read receipt、analytics、信息暴露都可能是 Side Effect。

**Q3：Reversible 和 Compensatable 有什么区别？**

Reversible 能恢复到近似原状态；Compensatable 是 effect 已发生后，用新的业务 Action 抵消影响，历史事实仍存在。

**Q4：为什么高风险 Action 要 Preview / Confirm / Commit？**

因为需要先把 resolved effect scope 暴露出来，再进行明确授权，避免模糊意图直接变成不可逆动作。

**Q5：Confirmation 和 Authorization 有什么区别？**

Authorization 判断是否有权；Confirmation 判断在当前具体 Action 上是否获得了明确同意。

**Q6：Idempotency 为什么重要？**

因为 timeout / retry 可能重复执行同一业务 Action；幂等语义能防止重复 side effect。

**Q7：为什么 HTTP 200 不等于 effect 正确？**

它只证明某个接口阶段成功，不能证明所有 intended effects 完成，也不能证明没有 unintended effects。

**Q8：什么是 Blast Radius？**

一次错误 Action 最多能影响的对象、用户、金额、数据范围、权限范围等规模。

**Q9：什么是 Minimal Sufficient Effect？**

满足 Goal 的前提下，选择真实世界影响最小、最必要的执行路径。

**Q10：为什么 Draft 与 Send 应拆成两个 Tool / Action？**

因为二者 effect class、可逆性、风险和权限要求完全不同。

**Q11：为什么 Side Effect 需要 Runtime Ledger？**

因为模型自述不是可靠证据；真实 effect history 应由执行系统记录并支持 audit / recovery / verification。

**Q12：什么是 Stale Approval？**

批准时的参数、资源集合或版本在真正执行前已经变化，旧 approval 不再对应当前 effect scope。

**Q13：为什么 recovery 也会有 Side Effect？**

Retry、rollback、compensation 都可能进一步修改 Environment，所以 recovery 也必须受权限、范围和验证约束。

**Q14：为什么 Agent Success Rate 不能单独评价 effectful Agent？**

因为高 success 可能伴随 duplicate payment、accidental delete、privacy leak 等低频高危副作用。

**Q15：Sandbox 如何帮助 Side-effect Safety？**

它把错误 Action 的影响限制在隔离环境，但仍需控制 network、credential 和资源配额。

**Q16：Side-effect Policy 属于 Harness 还是 Runtime？**

Harness 主要定义 policy；Runtime 负责通过 credential、sandbox、transaction、quota 等机制执行硬边界。

**Q17：Autonomy 与 Effect Authority 有什么区别？**

Autonomy 是 Agent 自主决定做什么的程度；Effect Authority 是系统真正允许它对世界产生多大影响。

**Q18：为什么高不可逆 Action 应该 Prevention > Recovery？**

因为某些 effect 一旦发生无法真正恢复，事后 compensation 只能降低损失，不能抹除历史。

**Q19：什么是 Effect Contract Drift？**

Tool 输入输出可能没变，但 backend 的通知、计费、权限或其他副作用发生变化，导致原有安全假设失效。

**Q20：Side-effect-aware Agent 的最终设计目标是什么？**

不是“尽可能多地替用户执行”，而是：**在明确授权范围内，以最小充分 effect 完成 Goal，并让 effect 可观察、可验证、可审计、可恢复。**

---

#### 3.9.185 一句话总结

> **Side Effect 是 Agent Action 对真实世界造成的持久影响；可靠 Agent 不仅要会“调用 Tool”，还必须控制 Effect Scope、Blast Radius、Idempotency、Reversibility、Approval、Audit 与 Verification，在高不确定和高不可逆场景下优先选择 Minimal Sufficient Effect。**

---

#### 3.9.186 参考资料

- Kleppmann M. **Designing Data-Intensive Applications**. O'Reilly, 2017. 用于理解幂等、事务、消息重复、事件顺序、一致性与分布式 effect semantics。
- Gray J, Reuter A. **Transaction Processing: Concepts and Techniques**. Morgan Kaufmann, 1992. 用于理解 transaction、atomicity、commit point、recovery 等经典语义。
- Garcia-Molina H, Salem K. **Sagas**. ACM SIGMOD, 1987. 用于理解跨服务长事务中 compensation 而非全局 rollback 的设计。
- Fielding R T. **Architectural Styles and the Design of Network-based Software Architectures**. 2000. 用于理解 HTTP method semantics、safe / idempotent operation 等接口设计背景。
- OWASP. **Top 10 for Large Language Model Applications / Prompt Injection guidance**. 用于理解 indirect prompt injection、excessive agency、data exfiltration 与 effect boundary 风险。
- OpenTelemetry. **Tracing Concepts and Semantic Conventions**. 用于理解 Action → Execution → Effect 的 trace lineage、correlation 与 auditability。
- Google SRE. **Site Reliability Engineering / The Site Reliability Workbook**. 用于理解 blast radius、canary、containment、rate limiting、graceful degradation 与 incident response。
- NIST. **AI Risk Management Framework (AI RMF 1.0)**. 用于理解高影响 AI 系统中风险识别、治理、测量与持续监控。
