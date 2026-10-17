# 第 11 章 Environment Design：状态、转移、观测、重置与可复现 Agent 世界

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 10 章 Agent Task Design`](./10_Agent_Task_Design.md)
>
> 关联章节：[`第 5 章 Tool-use Data 与 Agent Trajectory Data`](./05_Tool_Use_and_Agent_Trajectory_Data.md)、[`第 12 章 Agent Trajectory Anatomy`](./12_Agent_Trajectory_Anatomy.md)、[`第 15 章 Grader、Verifier 与 LLM-as-a-Judge`](./15_Grader_Verifier_and_LLM_as_a_Judge.md)、[`第 16 章 Benchmark Design 与 Evaluation Protocol`](./16_Benchmark_Design_and_Evaluation_Protocol.md)、[`第 19 章 Data Governance、Lineage 与 Reproducibility`](./19_Data_Governance_Lineage_and_Reproducibility.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**Tool / Harness / Environment、World State / Environment State / Observation / Agent-visible State 的 canonical chapter。** 后续 failure attribution、trajectory schema、benchmark freeze 与 production runtime 都应使用这里的系统边界。
>
> 本章核心问题：**Agent 的能力只有放进一个状态真实、转移明确、观测受控、可重置、可隔离、可复现、可验证的世界里才有意义。一个差的 Environment 会把 Model、Tool、Harness 与 Environment 的问题混成不可解释的分数。**

---

# 11.0 Environment 到底是什么？

普通 LLM 常被抽象成：

```text
Input
 ↓
Model
 ↓
Output
```

Agent 则更像：

```text
World / Environment State
        ↓
Agent-visible Information
        ↓
Decision
        ↓
Action
        ↓
Environment Transition
        ↓
Observation
        ↓
Updated Agent-visible State
        ↺
```

Environment 的核心不是“几个 API”，而是：

```text
State
Action Semantics
Transition
Observation
Exogenous Dynamics
Permissions / Resource Rules
```

Task Contract 则在这个世界之上定义：

```text
Goal
Constraints
Success Predicates
Forbidden Side Effects
Termination
```

因此要先钉死一个边界：

> **Environment 定义“世界如何运行”；Task 定义“在这个世界里要完成什么”。**

两者相关，但不能混成同一层。

---

# 11.1 Tool、Harness、Environment：三个系统层必须分开

这是整套 Agent 数据体系最重要的系统边界之一。

## Tool

Tool 是 Agent 可调用的动作接口 / action surface。

例如：

```text
search_order(id)
cancel_order(id)
create_event(...)
read_file(path)
run_python(code)
```

通常定义：

```text
name
description
argument schema
return schema
permission requirement
side-effect type
idempotency metadata
```

Tool 本身是“动作接口”。

---

## Environment

Environment 是 Action 真正作用的外部世界及其状态转移机制。

例如：

```text
订单数据库
日历系统
文件系统
浏览器 / Web backend
代码容器
CRM
邮件系统
GUI desktop
```

调用：

```text
cancel_order(1847)
```

可能导致：

```text
orders[1847].status:
pending → cancelled
```

这个真实状态变化属于 Environment。

---

## Harness

Harness 是把 Model、Tool、Environment 与执行流程组织起来的运行框架。

它可能负责：

```text
将 Tool Schema 放进模型 context
解析 model action / tool call
调用 tool adapter
把 observation 注入下一轮 context
维护 message history / memory
context truncation / summarization
最大步数
retry policy
parallel action orchestration
stop condition
logging
```

因此：

```text
Tool
= Action Interface

Environment
= World State + Transition + Observation Semantics

Harness
= Runtime Orchestration
```

---

## 11.1.1 为什么区分它们？

同一个失败：

```text
Agent 最终没有取消订单
```

可能来自：

```text
Model
→ 选错 action

Tool / Adapter
→ 参数映射错误

Environment
→ 后端真实执行失败

Harness
→ observation 丢失 / retry 改变语义 / context 被截断
```

如果数据里只保存：

```text
success = 0
```

就失去了 attribution 能力。

这套边界将在第 14 章 Failure Taxonomy 中作为 failure owner 的基础。

---

# 11.2 四种 State：不要再裸写一个 “State”

全书后续尽量明确写是哪一种 state。

## World State

现实或任务定义层面的完整真相。

例如：

```text
订单真实状态
用户真实权限
实际库存
真实文件内容
```

在真实产品中，World State 可能无法被系统完整序列化。

---

## Environment State

Benchmark / simulator / runtime 中，被环境系统实际维护、可用于转移和验证的状态表示。

例如：

```json
{
  "orders": {
    "1847": {
      "status": "shipped",
      "amount": 79
    }
  }
}
```

理想 benchmark 中，Environment State 应足够表达所有 task-relevant world truth。

---

## Observation

Environment 对某次 Action 返回给 Agent 的局部信息：

\[
o_{t+1}\sim O(s_{t+1},a_t)
\]

它可能经过：

```text
pagination
filtering
ranking
redaction
permission check
truncation
serialization
```

因此：

```text
Observation ≠ Full Environment State
```

---

## Agent-visible State

Agent 在某个时刻真正可用于决策的信息集合。

它可能由：

```text
User / System Context
+
Past Observations
+
Current Tool Results
+
Harness Memory / Summary
+
Visible Intermediate State
```

构成。

所以：

```text
World State
≠ Environment State Representation
≠ Observation
≠ Agent-visible State
```

这四者必须长期保持区分。

---

# 11.3 Transition：Action 以后世界怎么变化？

Environment 必须定义状态转移：

\[
s_{t+1}\sim T(s_t,a_t,\xi_t)
\]

其中 \(\xi_t\) 可以表示外部随机性、并发事件或时间推进。

例如：

```text
s_t:
order.status = pending

a_t:
cancel_order(1847)

s_t+1:
order.status = cancelled
```

---

## 11.3.1 Deterministic Transition

相同：

```text
state + action + runtime
```

得到相同结果。

适合：

```text
canonical benchmark
unit test
scientific comparison
```

优点是可复现、好 debug。

---

## 11.3.2 Stochastic / Exogenous Transition

现实可能存在：

```text
API timeout
搜索结果排序变化
网页动态内容
外部用户修改状态
随机延迟
服务波动
```

这类环境更真实，但会增加 evaluation variance。

因此应记录：

```text
seed
clock
service version
external snapshot
failure profile
retry policy
```

并区分：

```text
Canonical Deterministic Eval
vs
Stochastic / Robustness Eval
```

不要把两者无区分地混成一个总分。

---

# 11.4 Observation Function：Agent 看到什么，本身就是实验变量

真实 state 有 100 条订单，search tool 可能只返回：

```text
top 20
```

Agent 看到的 observation 可能受到：

```text
pagination
sorting
permission
redaction
schema
truncation
error semantics
```

影响。

因此同一个 Environment State，改变 Observation Function 就可能改变任务难度。

---

## 11.4.1 Observation Grounding

Tool call 成功不代表 Agent 正确使用了返回信息。

例如：

```text
Observation:
order_status = shipped
```

下一步 Agent 却执行：

```text
refund_order(...)
```

如果 shipped 应该阻止 refund，这就是典型：

```text
Observation Grounding Failure
```

因此 trajectory 至少要保留：

```text
Action
Observation
Next Decision / Action
```

完整 event schema 归第 12 章。

---

# 11.5 Snapshot 与 Reset：Benchmark 为什么必须回到同一起点？

如果 Task A 执行后：

```text
order 1847 = cancelled
```

下一次还从这个 mutated state 开始，就已经不是同一个 Case。

因此标准流程应该是：

```text
Load Frozen Snapshot
↓
Run Episode
↓
Capture Final State / Diff
↓
Reset / Restore
↓
Next Episode
```

常见实现：

```text
Full Rebuild
Snapshot Restore
Transaction Rollback
Copy-on-write
Disposable Container / VM
```

---

## 11.5.1 Snapshot 是 Environment Identity 的一部分

不能只说：

```text
“用了 CRM 环境。”
```

至少应能定位：

```text
environment_id
environment_version
snapshot_id
schema_version
fixture / data seed
clock
```

同一个 Case 应绑定明确的 snapshot / initial state reference。

---

# 11.6 Episode Isolation：不同运行不能互相污染

例如：

```text
Episode A 创建 file_x
Episode B 意外看到 file_x
```

那么 B 已经被前一条 trajectory 污染。

需要：

```text
isolated database tenant
isolated filesystem namespace
isolated browser session
isolated account / fixture
```

并验证：

```text
reset completeness
snapshot integrity
namespace isolation
```

Agent benchmark 里的 contamination 不只指 train/test leakage，还包括：

> **跨 Episode 的状态污染。**

---

# 11.7 Time：时间也是 Environment State

相对时间任务依赖：

```text
current_date
current_time
timezone
business hours
holiday calendar
```

例如：

```text
“订明天下午三点的会议室。”
```

如果 clock 不冻结，同一 Case 几天后语义就变了。

所以 benchmark 需要：

```text
frozen clock
simulated time
timezone
calendar version
```

必要时还要支持：

```text
advance_time(dt)
event queue
delayed event
```

---

# 11.8 Concurrency、Transaction 与 Atomicity

真实世界可能发生：

```text
Agent read state
↓
external actor modifies state
↓
Agent writes based on stale state
```

这就是 race condition / stale read。

基础 benchmark 可以先使用：

```text
single-agent
single-thread
frozen external state
```

高级 robustness benchmark 再加入：

```text
concurrent writes
external state changes
version conflict
resource contention
```

否则基础能力难以归因。

---

## 11.8.1 Partial Commit

例如任务要求：

```text
创建订单
+
扣库存
```

如果只完成第一步，Environment 是否允许 partial write？

需要明确：

```text
transaction boundary
atomic operation
rollback semantics
partial success state
```

因为这些都会影响 recovery 和 verifier。

---

# 11.9 Idempotency：System Retry 为什么会改变实验语义？

Read action 往往可以重复；Write action 不一定。

例如：

```text
send_email(...)
charge_card(...)
create_refund(...)
```

重复执行可能产生真实副作用。

因此 Tool / Environment metadata 应明确：

```text
idempotent = true / false
idempotency_key supported?
verify-before-retry?
```

关键纪律：

> **Infrastructure Retry ≠ Agent Recovery。**

如果 Harness 在模型不知情时自动重试一个语义失败，可能会替 Agent 完成它本应被评测的 recovery。

这一点在第 22 章 Production System 还会进一步展开。

---

# 11.10 Identity、Authentication 与 Authorization

Environment 必须知道：

```text
谁在操作
代表谁操作
拥有哪些 role / permission
资源属于谁
```

区分：

```text
Authentication
= 你是谁？

Authorization
= 你允许做什么？
```

Tool 出现在 schema 里，不代表当前 Agent / User 被授权调用它完成任意操作。

所以：

```text
Tool Availability
≠ Authorization
```

---

# 11.11 Error Semantics：环境不能只返回一个 ERROR

不同故障需要不同 recovery policy：

```text
NOT_FOUND
PERMISSION_DENIED
INVALID_ARGUMENT
RATE_LIMITED
TIMEOUT
CONFLICT
PRECONDITION_FAILED
SERVER_ERROR
```

如果全部压成：

```text
ERROR
```

Agent 无法学会条件化恢复。

因此 observation schema 中，错误类型本身就是重要训练信号。

---

# 11.12 Failure Injection：主动构造真实故障

Environment 可以有控制地注入：

```text
API timeout
rate limit
permission denied
empty result
malformed response
partial success
stale data
server 500
conflict
```

然后观察 Agent 是否：

```text
retry safely
verify state
switch strategy
ask user
rollback
escalate
abort
```

但 Failure Injection 必须版本化：

```text
failure_type
injection_step
schedule / probability
seed
expected semantics
```

基础 capability eval 不应一开始就混入大量随机故障；Robustness eval 可以单独建立 failure profile。

---

# 11.13 Sandbox 与 Safety Boundary

训练 / benchmark 可能包含：

```text
delete file
send email
modify database
run code
browse web
transfer / purchase simulation
```

所以需要：

```text
sandbox
container
VM
mock / test service
synthetic database
test account
restricted network
```

核心目标：

> **让 Agent 能真实执行行为，但副作用被限制在受控世界中。**

高风险环境还可以支持：

```text
dry-run
approval gate
spending limit
confirmation token
restricted scope
```

---

# 11.14 Dry-run 与 Commit 两阶段环境

一种常见安全设计：

```text
Plan / Dry-run
↓
Preview State Diff
↓
Approval
↓
Commit
```

这类机制既是产品设计，也可以被作为 Agent task 的 action space / policy boundary。

例如删除文件：

```text
Agent proposes 12 deletions
↓
preview diff
↓
approve
↓
commit
```

可以专门评测 Agent 是否知道什么时候应该先 preview / request approval。

---

# 11.15 Environment Verifier 与 State Diff

Task Contract 定义 Success Predicate；Environment 提供真实 State Evidence。

理想 verifier 直接读取环境状态，例如：

```text
order_1847.status == cancelled
AND other_orders_unchanged
AND duplicate_refund_count == 0
```

而不是读取：

```text
Agent final message contains “已完成”
```

---

## 11.15.1 State Diff

Write task 推荐保存：

```text
Before State
After State
Diff
```

例如：

```diff
- order_1847.status = pending
+ order_1847.status = cancelled
```

同时检查：

```diff
- order_1901.status = pending
+ order_1901.status = cancelled  ← forbidden side effect
```

State Diff 是 Agent evaluation 最强的一类 execution evidence。

完整 evaluator priority 归第 15 章。

---

# 11.16 Agent-visible Observation 与 Researcher-visible Evidence

“对 Agent 隐藏”不代表“研究日志里也不能记录”。

研究者可能需要看到：

```text
episode_id
case_id
environment snapshot
state before action
action / args
transition result
raw observation
state after action
verifier result
failure provenance
latency / cost
```

但 Agent 实际只能看到 policy 允许的 observation。

因此：

```text
Agent-visible Observation
≠ Evaluator / Researcher-visible Evidence
```

这是避免信息泄漏同时保持可调试性的关键。

---

# 11.17 Replay 与 Reproducibility

一次 Episode 的 replay 至少需要：

```text
Case Version
Environment Version / Snapshot
Tool Schema / Adapter Version
Harness Version
Model Version
Prompt / System Version
Seed
Clock
Failure Injection Config
Budget / Stop Rules
```

可抽象为：

```text
Episode
=
Case
× Environment
× Toolset
× Harness
× Model
× Runtime Config
```

这里是 replay identity，不是数学乘法。

数据治理层面的完整 provenance / lineage 归第 19 章。

---

# 11.18 Frozen Runtime：比较模型时必须控制什么？

如果目标是比较：

```text
Model A vs Model B
```

或者：

```text
Selector A vs Selector B
```

应尽量冻结：

```text
Case Set
Environment Snapshot
Tool Schema
Harness
Clock
Budget
Verifier
Failure Profile
```

只改变目标变量。

否则 performance delta 可能来自 runtime drift。

完整 Frozen Evaluation Protocol 在第 16 章展开。

---

# 11.19 State Leakage：环境真相不能提前泄漏

常见 leakage：

```text
prompt 泄漏 hidden state
tool description 泄漏 target entity
filename 泄漏 label
DOM hidden text 泄漏答案
metadata 泄漏 verifier result
```

例如任务要求：

```text
“找出未付款订单。”
```

Tool description 却写：

```text
order_1847 is unpaid
```

原本的 information acquisition 能力已经被绕开。

所以 benchmark Environment 需要专门做 leakage audit。

---

# 11.20 几类常见 Environment

## Database / CRM

适合：

```text
search
join
create
update
delete
aggregate
permission
transaction
```

优势：结构化、易 reset、易 verifier、易 synthetic state generation。

---

## Filesystem

适合：

```text
read
write
move
rename
delete
search
grep
archive
```

重点关注：

```text
path
permission
symlink
hidden file
encoding
large file
dependency
sandbox boundary
```

---

## Code Sandbox

需要：

```text
filesystem
runtime
compiler / interpreter
dependencies
test runner
resource limits
network policy
```

代码环境具有很强的 executable verifier：

```text
unit tests
integration tests
build
runtime output
static checks
```

---

## Browser / Web

状态包括：

```text
DOM
backend state
session
cookies
authentication
navigation
forms
pagination
popups
dynamic content
```

Live Web 真实但不稳定；Snapshot / Synthetic Web 可复现但存在 sim-to-real gap。

---

## Calendar / Email / Office / CRM

特点：

```text
multi-object
long-lived state
permissions
irreversible side effects
cross-tool dependency
human communication
```

非常适合真实 Agent benchmark。

---

## GUI / Computer-use

低层 action：

```text
click
scroll
type
drag
shortcut
window switch
```

同一个高层 goal 会拆成大量机械 action，因此再次说明：

> **Action Count ≠ Decision Complexity。**

---

# 11.21 Simulator 与 Sim-to-real Gap

真实系统可能：

```text
昂贵
危险
不可 reset
有隐私
速率受限
不可公开
```

因此经常需要 simulator。

Simulator fidelity 可以拆成：

```text
State Fidelity
Action Fidelity
Observation Fidelity
Failure Fidelity
Temporal Fidelity
Distribution Fidelity
```

原则不是“模拟得越复杂越好”，而是：

> **在目标 capability 相关维度上足够真实。**

常见 sim-to-real gap：

```text
模拟 API 永不 timeout
线上会 timeout

模拟数据很干净
线上缺字段 / 脏值

模拟权限简单
线上权限复杂

模拟页面固定
线上 UI 变化
```

一个更稳的验证链：

```text
Simulator Development
↓
Controlled Realistic Eval
↓
Limited Real-world Validation
```

---

# 11.22 Environment Difficulty 与 Environment Confound

同一个 Task，在不同 Environment 中难度可能完全不同。

例如“找到客户最近一次订单”：

```text
Easy Env:
search_customer → directly returns last_order

Hard Env:
search_customer
→ customer_id
→ list_orders with pagination
→ sort / compare
→ select latest
```

所以：

\[
Agent\ Difficulty=f(Task,Environment,Tools,Harness)
\]

这同样不是固定公式，而是提醒：

> **Task Difficulty 不是系统难度的全部。**

比较模型时如果 Environment / Tool / Harness 不同，就是严重 confound。

---

# 11.23 Multi-agent 与 Human-in-the-loop Environment

复杂系统还可能包含：

```text
Agent A
Agent B
Human
External Process
```

共享环境会引入：

```text
coordination
competition
message ordering
resource contention
race condition
shared-state conflict
```

Trajectory schema 应记录：

```text
actor_id
action order
shared state
message channel
```

Human-in-the-loop 场景则需要支持：

```text
Agent asks
↓
Human clarifies / approves
↓
Agent continues
```

否则 benchmark 无法真实测试 clarification / escalation / approval behavior。

---

# 11.24 Environment Cost Model

Action 不是免费的。

可能具有：

```text
latency
API cost
compute cost
risk cost
human interruption cost
```

可以记录：

\[
C(\tau)=\sum_t c(a_t)
\]

因此最终 evaluation 可以看：

```text
Success
vs
Tool Cost
vs
Latency
vs
Risk
```

而不是只看成功率。

---

# 11.25 Canonical Case：C1 Order / Refund

沿用第 10 章 Case C1：

```text
用户：
“如果订单 1847 还没发货，就帮我退款；已经发货就不要动。”
```

Environment Truth：

```text
order_1847.status = shipped
order_1847.amount = 79
```

Agent 初始只知道：

```text
order_id = 1847
```

Tools：

```text
order.get
refund.create
shipment.cancel
```

一次正确交互：

```text
order.get(1847)
↓
Observation: status = shipped
↓
Agent decides: no write action
↓
Final State unchanged
```

这里可以清楚区分：

```text
World / Environment Truth
→ status = shipped

Observation
→ tool returns shipped

Agent-visible State
→ context + this observation

Action
→ no refund

Verifier Evidence
→ before / after state diff = no forbidden write
```

如果 `refund.create` 第一次调用 timeout，还可以进一步测试：

```text
Environment failure semantics
Idempotency
Verify-before-retry
Agent Recovery
Harness Retry Boundary
```

完整案例见 [`Canonical Casebook`](./00_Canonical_Casebook.md)。

---

# 11.26 Environment Versioning 与 Lineage

建议记录：

```json
{
  "environment_id": "order_env",
  "environment_version": "v5",
  "schema_version": "v3",
  "snapshot_id": "order_case_1847_s01",
  "toolset_version": "tools_v4",
  "clock": "2026-10-18T09:00:00+08:00",
  "failure_profile": "none"
}
```

每个 Episode 再绑定：

```text
case_id
model_version
harness_version
runtime_config
seed
verifier_version
```

系统级 lineage / reproducibility 统一归第 19 章。

---

# 11.27 常见失败模式

### 失败 1：Tool、Harness、Environment 混在一起

Failure attribution 失真。

### 失败 2：Environment 没有 Reset / Isolation

前一个 Episode 污染后一个。

### 失败 3：Tool 返回 Success 就当真实 State 已正确更新

必须检查 environment evidence。

### 失败 4：Observation 与 Full State 混淆

Agent 被默认知道实际上不可见的信息。

### 失败 5：Live Web 直接作为唯一 benchmark

变化太多，纵向不可比。

### 失败 6：Simulator 太干净

线上 robustness 被高估。

### 失败 7：没有 Snapshot / Clock / Version

Episode 无法 replay。

### 失败 8：所有错误只返回 ERROR

Recovery semantics 学不到。

### 失败 9：Write Tool 被 Harness 无脑自动 Retry

可能改变实验语义并制造重复副作用。

### 失败 10：只看 Final Value，不看 State Diff

可能通过破坏其他对象达到目标。

### 失败 11：不同模型运行在不同 Environment / Harness 上

性能不可归因。

### 失败 12：Hidden State 泄漏

Agent task 被降级。

### 失败 13：只测 deterministic happy path

真实 robustness 被高估。

### 失败 14：基础 benchmark 一开始就混入大量随机故障

结果变成环境噪声测试。

### 失败 15：Environment 没有业务规则 / Permission Boundary

Agent 可以走非法 shortcut。

### 失败 16：Researcher Evidence 和 Agent Observation 不区分

很容易发生 evaluator-only information leakage。

---

# 11.28 从数据岗位视角，这一章实际会做什么？

```text
搭 sandbox / simulator
设计 environment state schema
区分 world / environment / observation / agent-visible state
实现 tool backend / adapter
实现 transition
实现 snapshot / reset
实现 state diff
设计 permission / identity
控制 side effect
定义 idempotency / transaction semantics
注入 failure
冻结 clock
做 episode isolation
实现 verifier evidence
记录 latency / cost
维护 environment version
做 leakage audit
复现 failure trajectory
区分 model / tool / harness / environment failure
```

所以 Agent Data 工程不是：

> “给模型接几个 API。”

而是：

> **构造一个足够真实，同时又可控、可验证、可复现的实验世界。**

---

# 11.29 本章关键词

| 术语 | Canonical meaning |
|---|---|
| Tool | Agent 可调用的动作接口 |
| Harness | 组织 Model / Tool / Environment 交互的 runtime |
| Environment | Action 真正作用的外部世界与转移机制 |
| World State | 任务相关的完整真实世界状态 |
| Environment State | Runtime / benchmark 中维护的状态表示 |
| Observation | Environment 暴露给 Agent 的局部信息 |
| Agent-visible State | Agent 当前可用于决策的信息集合 |
| Transition | Action 导致 Environment State 变化的机制 |
| Snapshot | 可定位 / 恢复的 Environment State 版本 |
| Reset | 恢复 Case 规定的初始状态 |
| Isolation | 防止 Episode / Agent 相互污染 |
| Idempotency | 重复执行 Action 是否产生额外效果 |
| Atomicity | 操作是否全部成功或全部失败 |
| Failure Injection | 受控构造环境故障 |
| State Diff | 执行前后环境状态差异 |
| Sandbox | 将副作用限制在受控空间 |
| Sim-to-real Gap | 模拟环境与真实世界差异 |
| Frozen Runtime | 固定非研究变量的运行条件 |

更完整定义见 [`Canonical Glossary`](./00_Glossary_and_Notation.md)。

---

# 11.30 面试 / 自检问题

1. Tool、Harness、Environment 有什么区别？
2. World State、Environment State、Observation、Agent-visible State 有什么区别？
3. 为什么 Agent Benchmark 必须支持 Reset？
4. Snapshot 与 Reset 分别解决什么问题？
5. Partial Observability 为什么是 Agent capability 的核心？
6. 为什么 Tool Success 不等于 Environment State 正确？
7. Deterministic 与 Stochastic Environment 应如何分工？
8. 为什么 benchmark 要冻结 clock？
9. Race Condition / Stale Read 是什么？
10. Idempotency 为什么决定 Retry 是否安全？
11. Infrastructure Retry 与 Agent Recovery 为什么必须区分？
12. Transaction / Atomicity 对 Agent 有什么意义？
13. 为什么 Before / After State Diff 很重要？
14. Failure Injection 测什么？
15. 为什么 Error Semantics 需要细分？
16. Episode Isolation 是什么？
17. Live Web 为什么难做稳定 benchmark？
18. Simulator Fidelity 应重点保证什么？
19. Sim-to-real Gap 怎么缓解？
20. 为什么比较模型必须冻结 Environment / Tool / Harness？
21. State Leakage 有哪些形式？
22. Multi-agent Environment 新增了什么问题？
23. Human-in-the-loop 为什么需要环境支持？
24. 为什么 Environment 还要记录 cost / latency？
25. 如何设计一个既真实又可控的 Agent Environment？

---

## 11.30.1 通用回答框架：搭一个 Agent Benchmark Environment

```text
1. 明确 target capability / Task Family
   ↓
2. 定义 Environment State Schema
   ↓
3. 区分 World Truth / Agent-visible Information
   ↓
4. 设计 Tool / Action Interface
   ↓
5. 实现 State Transition
   ↓
6. 实现 Observation Function
   ↓
7. 实现 Snapshot / Reset / Isolation
   ↓
8. 加 Identity / Permission / Side-effect / Idempotency Semantics
   ↓
9. 实现 State Evidence / Verifier
   ↓
10. 冻结 Clock / Seed / Version
   ↓
11. 先做 Deterministic Capability Eval
   ↓
12. 再加 Failure Injection / Stochastic Robustness
   ↓
13. 保存完整 Replay / Lineage 信息
```

---

# 11.31 与后续章节的关系

```text
第 12 章 Trajectory Anatomy
→ 把 Environment 交互记录成 typed event log

第 13 章 Credit Assignment
→ 哪些 Action / State Transition 真正导致最终 Outcome

第 14 章 Failure Taxonomy
→ Model / Tool / Harness / Environment failure 如何归因

第 15 章 Evaluator
→ Environment Evidence 怎样变成可信判分

第 16 章 Benchmark Protocol
→ Environment / Harness / Tool 如何被冻结以保证可比

第 19 章 Governance
→ Snapshot / Version / Replay / Provenance 如何长期治理
```

---

# 11.32 本章最终要形成的认识

把 Environment 压缩成：

```text
World / Environment State
        ↓
Allowed Action
        ↓
Transition
        ↓
Observation
        ↓
Agent-visible State
        ↺
```

一个可信环境还必须具备：

```text
Resettable
Reproducible
Isolated
Observable
Versioned
Verifiable
Safe
```

最终要记住两句话：

> **Task 定义“要完成什么”；Environment 定义“世界如何变化”。**

> **Tool 是动作接口，Environment 是世界，Harness 是把模型与世界连接起来的运行机制。**

下一章进入：

> [`第 12 章 Agent Trajectory Anatomy`](./12_Agent_Trajectory_Anatomy.md)

开始回答：

> **当 Agent 真正在这个世界里跑起来后，一条可用于训练、评测和诊断的 Trajectory 到底应该记录什么？**