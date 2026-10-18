from pathlib import Path
import re
import subprocess

DOC = Path("Agent_Knowledge_System.md")
text = DOC.read_text(encoding="utf-8")

# Import the already-written 4.1 section from the previous staging branch,
# while applying it onto the latest main-derived document so concurrent main
# changes are preserved.
old_doc = subprocess.check_output(
    [
        "git",
        "show",
        "origin/agent-doc-4-1-context-engineering:Agent_Knowledge_System.md",
    ],
    text=True,
)
old_41_match = re.search(
    r"### 4\.1 Context Engineering\n.*?(?=\n### 4\.2 Working State)",
    old_doc,
    re.DOTALL,
)
assert old_41_match, "could not extract completed 4.1 section from staging branch"
section_41 = old_41_match.group(0).rstrip("\n")
assert "#### 4.1.67 参考资料" in section_41, "4.1 section appears incomplete"

current_41_pattern = re.compile(
    r"### 4\.1 Context Engineering\n.*?(?=\n### 4\.2 Working State)",
    re.DOTALL,
)
assert len(current_41_pattern.findall(text)) == 1, "expected exactly one current 4.1 section"
text = current_41_pattern.sub(lambda _m: section_41, text, count=1)

new_section = r'''### 4.2 Working State

如果说 4.1 Context Engineering 解决的是：

> **这一轮模型应该看到什么？**

那么 Working State 解决的是更底层的问题：

> **为了让当前任务能够连续、正确、可恢复地执行，系统此刻必须知道什么？**

一个 Agent 即使每一轮都重新调用模型，也不能每次都从零开始。它必须持续维护：

```text
目标是什么
已经做了什么
现在真实处于什么状态
哪些约束仍然有效
哪些 Action 正在进行
哪些结果已经验证
还剩多少预算
哪些权限已经批准
哪些错误尚未恢复
```

这些信息共同构成当前任务的 **Working State**。

先记住本节最核心的一条链：

```text
Environment
    ↓ Observation / Reconciliation
Working State_t
    ↓ Context Projection
Context_t
    ↓ Policy / Decision
Action_t
    ↓ Runtime Execution
Environment_{t+1}
    ↓ Observation / Reconciliation
Working State_{t+1}
```

因此：

> **Working State 是 Agent Loop 的状态骨架；Context 是 Working State 面向当前模型调用的一次投影。**

---

#### 4.2.1 什么是 Working State？

在本文中，**Working State** 指：

> **当前一个活跃任务 / Episode 为了继续正确执行，而由 Agent 系统显式维护的、当前有效的操作状态。**

它不是“所有历史信息”的集合，而是：

```text
此刻继续执行任务真正需要的状态
```

例如一个 Coding Agent 的 Working State 可以包含：

```text
goal
repo_root
current_branch
base_commit
changed_files
current_failure
latest_test_result
public_api_constraint
pending_actions
approval_state
remaining_budget
verification_status
terminal_status
```

一个 Research Agent 可以包含：

```text
research_question
required_date_scope
claims_under_review
candidate_sources
verified_sources
unresolved_conflicts
freshness_requirements
remaining_queries
citation_coverage
completion_status
```

一个 Booking Agent 可以包含：

```text
origin
destination
date_range
traveler_count
price_limit
selected_option
reservation_hold_id
payment_status
approval_state
booking_status
```

共同点是：

> 这些字段不是为了“让系统显得记得很多”，而是为了下一步 Action、Verification 和 Termination 能有可靠依据。

---

#### 4.2.2 Working State 为什么必须显式化？

最脆弱的 Agent 往往把状态隐藏在自然语言 transcript 里：

```text
User said X
Assistant said Y
Tool returned Z
Assistant summarized ...
```

然后每一步让模型自己从长文本里重新推断：

```text
现在到底做到哪了？
```

这会带来：

```text
遗漏
歧义
旧状态残留
模型自述污染
状态冲突
恢复困难
```

显式 Working State 则把关键执行变量提升为系统对象：

```json
{
  "task_status": "running",
  "remaining_budget": 6,
  "latest_tests": "failed",
  "changed_files": ["src/a.py"],
  "approval": "not_required"
}
```

模型可以读取其中一部分，但系统不需要依赖模型“记住”这些事实。

所以：

> **重要执行事实应成为 State，而不是只存在于 Narrative。**

---

#### 4.2.3 Working State 不等于 Context

这条边界必须和 4.1 完全对齐。

**Working State**：

```text
系统为了继续当前任务而维护什么？
```

**Context**：

```text
这一轮模型实际看到什么？
```

关系是：

\[
C_t = \phi(S_t, O_t, M_t, R_t, \ldots)
\]

其中：

- \(S_t\)：Working State；
- \(C_t\)：当前 Context；
- \(\phi\)：Context Projection / Builder。

因此可能出现：

```text
Working State 中有 50 个字段
当前 Context 只暴露其中 12 个
```

这是正常的。

真正危险的是反过来：

```text
系统真正需要的状态
只存在于某次 Context 中
但没有进入 Working State
```

因为下一轮一旦压缩、截断或重新组装 Context，这些信息就可能永久丢失。

---

#### 4.2.4 Working State 不等于 Conversation Transcript

Transcript 是：

```text
发生过什么的文本记录
```

Working State 是：

```text
现在什么仍然有效
```

例如历史里出现：

```text
Step 2: tests failed
Step 5: tests passed
```

Transcript 两条都保留。

但 Working State 应该是：

```text
latest_test_status = passed
```

所以：

> **Transcript 更像历史日志；Working State 更像当前快照。**

两者用途不同：

```text
Transcript / Event History
→ audit / replay / debugging

Working State Snapshot
→ next decision / verification / execution
```

---

#### 4.2.5 Working State 不等于 Memory

Memory 解决的是：

> **哪些过去信息值得保留下来，并在未来再次使用？**

Working State 解决的是：

> **当前这个正在运行的任务，此刻必须知道什么？**

例如：

```text
用户长期偏好：喜欢靠窗座位
```

属于 Long-term Memory。

当用户本次订票时，这个偏好被取出并进入当前任务：

```text
seat_preference = window
```

此时它可以成为 Working State 的一个字段。

因此可以写成：

```text
Memory
  ↓ retrieve / activate
Working State or Context
```

而不是：

```text
Memory = Working State
```

---

#### 4.2.6 Working State 不等于 Environment State

**Environment State** 是真实世界此刻的状态。

例如：

```text
文件真实内容
数据库真实记录
网页真实页面
订单真实状态
远端 Job 真实执行状态
```

Working State 是 Agent 系统对当前任务相关事实的内部维护。

因此：

```text
Environment
≠
Working State
```

更准确是：

```text
Environment
   ↓ observe / query
Observation
   ↓ normalize / reconcile
Working State
```

如果外部世界已经变化，而 Working State 还没刷新，就会出现：

> **State–Environment Mismatch**。

这会是 Agent 长任务中非常常见的错误来源。

---

#### 4.2.7 Working State 不等于 Observation

Observation 是：

> **某一时刻从 Environment 获得的反馈。**

Working State 是：

> **结合已有状态与新 Observation 后，对当前任务维护的有效状态。**

例如 Tool 返回：

```json
{
  "status": "completed",
  "job_id": "J17",
  "result": "..."
}
```

这是 Observation。

系统随后更新：

```text
pending_job = none
last_completed_job = J17
result_ref = ...
workflow_status = ready_for_verification
```

这些才是 Working State。

所以：

\[
S_{t+1} = U(S_t, O_{t+1})
\]

而不是：

```text
State = latest Observation
```

---

#### 4.2.8 Working State 不等于 Plan

Plan 是：

```text
准备如何完成任务
```

Working State 更广：

```text
当前目标
当前事实
当前进度
当前约束
当前预算
当前权限
当前计划
当前错误
当前验证证据
当前终止状态
```

因此：

```text
Plan ⊂ Working State
```

通常更合理。

Plan 可以被修改、废弃或重新生成，但 Goal、已发生 Action、真实 Effect、预算消耗等状态不能随着“换计划”一起被遗忘。

---

#### 4.2.9 Working State 不等于 Runtime State

本文把 4.2 的 Working State 放在 Capability / Context & Memory 层，主要讨论：

> **任务语义上需要维持的活跃状态。**

后面 8.2 Runtime State 更关注：

```text
process id
container id
queue lease
worker assignment
callback token
scheduler metadata
checkpoint location
execution handle
```

这些是执行基础设施状态。

二者可以关联：

```text
Working State:
pending_job = J17

Runtime State:
J17 worker = gpu-03
J17 process = 8124
J17 lease_expiry = ...
```

但不要混成一个概念。

---

#### 4.2.10 一个 Working State 最少应该有哪些类别？

一个通用任务状态可以粗略拆成：

```text
Working State
├── Goal / Task Contract
├── Constraints / Invariants
├── Progress / Subgoals
├── Environment References
├── Latest Facts / Observations
├── Action / Effect State
├── Verification State
├── Permission / Approval State
├── Budget / Deadline State
├── Error / Recovery State
└── Terminal State
```

不同 Agent 不需要完全照搬，但这组分类可以帮助检查：

> 系统有没有把真正关键的执行状态漏掉？

---

#### 4.2.11 Goal / Task Contract 应成为 Working State 的根

很多系统只在最开始 Prompt 里放一次用户目标：

```text
“帮我修 bug，但不能改变 public API。”
```

然后几十步之后只保留最近的日志。

这很容易 Goal Drift。

更稳健的是把任务契约结构化：

```json
{
  "objective": "fix failing test",
  "must_preserve": ["public API"],
  "forbidden": ["modify vendor/"],
  "success_criteria": ["tests pass", "public API unchanged"]
}
```

这样每一轮都可以从 State 投影关键约束。

所以：

> **Goal 不应该只是历史消息；对长轨迹而言，它应成为持续有效的 State。**

---

#### 4.2.12 Immutable State 与 Mutable State

Working State 中有些字段一旦任务开始就不应被 Agent 随意修改。

例如：

```text
user_goal
protected_resources
approved_budget
safety_constraints
base_commit
```

可以视为：

> **Immutable / Protected State**。

另一些会不断变化：

```text
latest_observation
current_plan
changed_files
remaining_budget
retry_count
verification_status
```

属于 Mutable State。

因此 schema 可以显式区分：

```text
Task Contract
= protected

Execution State
= mutable under rules
```

否则模型可能在遇到困难时“修改目标来让自己成功”。

---

#### 4.2.13 Authoritative State 与 Derived State

另一个重要划分是：

```text
Authoritative State
vs
Derived State
```

例如：

```text
changed_files = ["a.py", "b.py"]
```

如果它来自真实 Git diff，可以是较权威状态。

而：

```text
risk_level = "high"
```

可能是系统根据多个字段推导出的 Derived State。

又例如：

```text
remaining_budget
```

应该由计费 / runtime 真实记录计算，不应该让模型自由填写。

因此：

> **关键事实应尽量绑定权威来源；模型推断值应明确标记为推断，而不是伪装成事实。**

---

#### 4.2.14 Source of Truth：每个关键字段最好知道谁说了算

一个成熟 State Schema 不只定义：

```text
field name
field type
```

还应该隐含或显式定义：

```text
owner / source of truth
```

例如：

| 字段 | Source of Truth |
|---|---|
| `remaining_budget` | Budget Manager |
| `file_version` | Filesystem / Git |
| `payment_status` | Payment Provider |
| `approval_status` | Approval Service |
| `current_plan` | Agent / Harness |
| `task_goal` | User / Task Contract |
| `test_status` | Test Runtime |

这样遇到冲突时才能知道：

```text
应该相信谁？
```

---

#### 4.2.15 State Schema 为什么重要？

如果 State 只是任意字典：

```python
state["stuff"] = ...
```

长期运行后很容易出现：

```text
字段命名漂移
类型漂移
空值歧义
旧字段遗留
不同模块语义不一致
```

显式 Schema 可以约束：

```text
field
meaning
type
required / optional
allowed transitions
owner
version
sensitivity
```

例如：

```json
{
  "task_status": "running | blocked | completed | failed",
  "remaining_steps": 8,
  "approval_status": "not_required | pending | approved | rejected"
}
```

这让 State 更像可靠系统接口，而不是模型笔记本。

---

#### 4.2.16 Optional、Unknown、Missing、False 必须区分

Agent State 中非常常见的错误是把：

```text
不知道
```

写成：

```text
false
```

例如：

```text
payment_succeeded = false
```

到底是：

```text
明确失败
```

还是：

```text
尚未查询
```

完全不同。

因此可以使用：

```text
UNKNOWN
PENDING
TRUE
FALSE
NOT_APPLICABLE
```

而不是滥用二值。

一句话：

> **Unknown 是一种状态，不是 False。**

---

#### 4.2.17 State Transition：Working State 怎样变化？

Working State 不是随意覆盖，而应该通过明确状态转移更新。

抽象地：

\[
S_{t+1}=U(S_t,E_t)
\]

其中 \(E_t\) 可以是：

```text
new Observation
Action Result
Approval Event
Timer Event
User Update
Verifier Result
Budget Event
Runtime Failure
```

更具体：

```text
Current State
    ↓
Event / Observation
    ↓
Validation
    ↓
Transition Rule
    ↓
New State
```

这就是 Agent Loop 能保持一致性的关键。

---

#### 4.2.18 State Update 不是“让模型重写整份 JSON”

一个简单但危险的实现是：

```text
把旧 State 给模型
让模型输出一份新 State
完全替换旧 State
```

这样模型可能：

```text
误删字段
篡改 protected field
更改 budget
丢失 provenance
错误改写已验证事实
```

更稳健的做法是：

```text
Model proposes patch / event
      ↓
Schema Validation
      ↓
Transition Policy
      ↓
System applies allowed fields
```

也就是：

> **Model may propose state changes; the system should own authoritative state mutation.**

---

#### 4.2.19 Patch Update 比 Full Rewrite 更可靠

假设 State 有 80 个字段，而本轮只变化：

```text
latest_test_status
retry_count
```

更合理的更新是：

```json
{
  "latest_test_status": "passed",
  "retry_count": 2
}
```

而不是重新输出全部 80 个字段。

Patch 的优势：

```text
减少无关字段误改
更容易 audit
更容易验证
更容易 conflict detection
```

因此复杂 Agent 常更适合：

> **event / patch-oriented state transitions**。

---

#### 4.2.20 Event 与 State Snapshot 的关系

可以同时保留两类信息：

```text
Event Log
= 发生了什么

State Snapshot
= 现在是什么
```

例如：

```text
Event 1: test_failed
Event 2: file_modified
Event 3: test_passed
```

当前 Snapshot：

```text
test_status = passed
changed_files = [a.py]
```

因此：

```text
Events
→ fold / reduce
→ Current State
```

这种思想与 event sourcing 类似，但 Agent 系统不一定需要完整采用 event-sourced architecture。

---

#### 4.2.21 为什么既要 Snapshot，又要 History？

只有 Snapshot：

```text
现在知道发生了什么
但不知道为什么变成这样
```

只有 History：

```text
知道所有过程
但每次都要重算当前状态
```

所以常见组合是：

```text
Current Snapshot
+
Append-only Event / Trace History
```

Snapshot 支持快速决策。

History 支持：

```text
audit
replay
debugging
failure attribution
recovery
```

---

#### 4.2.22 State Versioning

只要 Environment 和 State 都可能变化，就需要版本概念。

例如：

```text
state_version = 41
file_version = commit abc123
record_version = 17
```

版本的作用包括：

```text
检测 stale write
检测旧 Observation
支持 resume
支持 optimistic concurrency
支持 conflict resolution
```

因此：

> **Working State 不只是“值”，还需要知道这些值对应哪个版本。**

---

#### 4.2.23 Timestamp 与 Version 不完全等价

时间戳可以回答：

```text
什么时候观察到的？
```

版本可以回答：

```text
观察的是哪一个状态实例？
```

例如两个更新发生在同一秒：

```text
timestamp 相同
version 不同
```

所以高一致性系统不能只靠时间排序。

可以同时记录：

```text
observed_at
source_version
state_version
```

---

#### 4.2.24 Freshness 是 State 的一等属性

某个字段历史上正确，不代表现在仍然正确。

例如：

```text
inventory_count
flight_price
page_content
branch_head
permission_scope
job_status
```

都可能快速变化。

所以 State 不仅要存：

```text
value
```

还可以存：

```text
value
source
timestamp
version
expiry / freshness policy
```

当数据过期时，下一步 Action 应优先：

```text
re-observe / refresh
```

而不是继续基于旧值推理。

---

#### 4.2.25 State–Environment Reconciliation

Agent 不能永远假设内部 State 与世界一致。

特别是在：

```text
长任务
异步任务
多人协作
外部 API
并发编辑
```

中，Environment 可能绕过 Agent 自己变化。

因此需要周期性或事件驱动的 reconciliation：

```text
Internal State
      ↓ compare
Fresh Environment Observation
      ↓
Mismatch?
  ├─ no → continue
  └─ yes → reconcile / replan / block
```

这与分布式系统里的 control loop 思想非常接近。

---

#### 4.2.26 State–Environment Mismatch 示例

Coding Agent：

```text
State:
branch_head = A
```

但用户在外部又提交了一次：

```text
Environment:
branch_head = B
```

如果 Agent 仍然按 A 修改：

```text
可能覆盖新改动
```

所以真正执行写操作前，可以检查：

```text
expected_head == actual_head ?
```

不一致则：

```text
refresh
rebase / reconcile
ask user
```

而不是盲写。

---

#### 4.2.27 State–Context Projection

当 Working State 维护正确后，还要决定：

```text
本轮模型需要看到哪些 State 字段？
```

例如：

```text
State:
80 fields
```

当前 Action 是搜索资料，只需要：

```text
research question
date scope
missing evidence
source constraints
remaining search budget
```

所以：

\[
C_t^{state}=\phi(S_t, decision\_need_t)
\]

这就是 4.1 Context Engineering 与 4.2 Working State 的接口。

---

#### 4.2.28 State–Context Mismatch

即使 State 是对的，如果 Context 投影错误，模型仍会做错。

例如：

```text
State:
latest_test_status = passed

Context:
仍然展示旧日志：tests failed
```

模型可能继续修已经修好的问题。

所以 Agent 需要同时控制：

```text
State correctness
+
Context projection correctness
```

这两个 Failure Mode 必须分开定位。

---

#### 4.2.29 State Invariant

Working State 中有些条件必须始终成立。

例如 Coding Agent：

```text
base_commit never changes silently
protected_files ∩ changed_files = ∅
remaining_budget >= 0
```

Booking Agent：

```text
selected_option must belong to current search result version
payment cannot be committed before approval
```

这些就是 **State Invariants**。

可以形式化：

\[
I(S_t)=\text{true}
\]

每次 Transition 后都应满足：

\[
I(S_{t+1})=\text{true}
\]

---

#### 4.2.30 Precondition、Transition、Postcondition

一次可靠 State Update 可以分成三部分：

```text
Precondition
↓
Transition
↓
Postcondition / Invariant Check
```

例如：

```text
Precondition:
approval_status == approved

Transition:
payment_status: pending → submitted

Postcondition:
transaction_id exists
```

这比自由文本：

```text
“支付应该成功了”
```

可靠得多。

---

#### 4.2.31 Pending State 为什么很重要？

现实 Action 并不总是瞬间完成。

可能存在：

```text
queued
running
pending approval
submitted
waiting callback
```

如果 Working State 只有：

```text
success / failure
```

就无法正确表达中间态。

因此 effectful / async 任务应显式维护：

```text
PROPOSED
AUTHORIZED
SUBMITTED
PENDING
COMPLETED
FAILED
UNKNOWN
```

这和 3.9 Effect Lifecycle 直接对接。

---

#### 4.2.32 Unknown Outcome 必须进入 State

最危险的一类情况：

```text
支付请求发出
↓
timeout
```

此时不是：

```text
payment = failed
```

而应该是：

```text
payment = unknown
transaction_request_id = ...
```

下一步应：

```text
query status
```

而不是直接 retry。

因此：

> **Outcome Uncertainty 本身必须被状态化。**

否则 Agent 会把“不知道”误当“没发生”，造成重复副作用。

---

#### 4.2.33 Action State 与 Task State 必须分开

某个 Tool Call 成功：

```text
Action Status = success
```

并不意味着：

```text
Task Status = success
```

例如：

```text
search_web success
```

只说明搜索动作成功，不说明研究问题已经回答。

所以 Working State 可以分开维护：

```text
last_action_status
subgoal_status
task_status
```

避免把局部执行结果升级成全局完成。

---

#### 4.2.34 Verification State

如果任务要求可靠完成，State 中最好显式记录：

```text
什么已经验证
什么尚未验证
使用什么证据验证
哪个 verifier 给出结果
```

例如：

```json
{
  "tests_passed": true,
  "public_api_verified": false,
  "verification_evidence": {
    "tests": "run_184",
    "api_diff": null
  }
}
```

这比一个简单：

```text
done = false
```

信息丰富得多。

---

#### 4.2.35 Evidence State

对于 Research / Verification Agent，Working State 可以维护：

```text
claim
candidate evidence
verified evidence
source provenance
source freshness
conflict status
coverage status
```

例如：

```text
Claim A
├── evidence_1: primary / supports
├── evidence_2: secondary / conflicts
└── status: unresolved
```

这样模型不会因为“看过一篇文章”就误以为 Claim 已经定论。

---

#### 4.2.36 Permission / Approval State

权限也是任务状态的一部分。

例如：

```text
Action proposed
approval pending
approval granted for exact scope
approval expired
```

State 应保存：

```text
approval_id
approved_action
approved_scope
approved_version
expires_at
```

而不是只有：

```text
user said yes earlier
```

这能防止 Stale Approval 和 Scope Drift。

---

#### 4.2.37 Budget State

Budget 不能只写在 Prompt：

```text
“尽量少调用工具。”
```

应该显式维护：

```text
remaining_steps
remaining_model_calls
remaining_tool_calls
remaining_cost
remaining_wall_time
```

例如：

```json
{
  "model_calls_left": 4,
  "tool_calls_left": 7,
  "deadline": "...",
  "cost_spent": 0.84
}
```

这样 Policy 才能做真正的 budget-aware 决策。

---

#### 4.2.38 Error State

错误不能只出现在日志里然后消失。

Working State 可以维护：

```text
last_error
error_class
retryable
attempt_count
side_effect_possible
recovery_status
```

例如：

```json
{
  "error_type": "timeout_after_submit",
  "retryable": false,
  "side_effect_possible": true,
  "next_required_action": "status_query"
}
```

这样 Recovery 才能基于错误语义，而不是机械 retry。

---

#### 4.2.39 Recovery State

一旦进入恢复流程，还需要知道：

```text
正在从哪个失败恢复
已经尝试过什么
哪些补偿已经执行
恢复预算还剩多少
是否需要升级人工
```

否则 Recovery 自己也会变成无穷循环。

可以维护：

```text
recovery_attempts
recovery_strategy
recovery_effects
recovery_deadline
escalation_status
```

---

#### 4.2.40 Terminal State

Agent 停止不只有：

```text
done = true
```

更合理的终态包括：

```text
SUCCESS
FAILED
BLOCKED
NEEDS_USER
NEEDS_APPROVAL
BUDGET_EXHAUSTED
TIMEOUT
CANCELLED
```

并带：

```text
terminal_reason
completion_evidence
unresolved_items
```

这样系统才能区分：

```text
任务真的完成
vs
只是不能继续
```

---

#### 4.2.41 State Machine View

Working State 很适合用状态机理解。

例如：

```text
INITIALIZED
    ↓
RUNNING
    ├──→ WAITING_APPROVAL
    ├──→ WAITING_EXTERNAL
    ├──→ RECOVERING
    ├──→ BLOCKED
    └──→ VERIFYING
             ↓
        COMPLETED / FAILED
```

状态机的价值是：

```text
合法 transition 可枚举
非法 transition 可拒绝
终止条件可验证
恢复路径更清晰
```

---

#### 4.2.42 State Machine 不等于 Agent Policy

状态机规定：

```text
哪些状态和 transition 是允许的
```

Policy 决定：

```text
在当前允许范围内，下一步选什么 Action
```

因此：

```text
State Machine
= legal transition structure

Agent Policy
= decision rule within structure
```

不要因为有状态机就认为系统“不再 agentic”。

Agent 仍然可以在合法 Action Space 内动态选择路径。

---

#### 4.2.43 State Validation

每次 State Update 后，可以做：

```text
schema validation
cross-field validation
invariant validation
reference validation
freshness validation
```

例如：

```text
status == completed
```

但：

```text
completion_evidence == null
```

可能违反业务约束。

所以有效 State 不只是字段类型合法，还必须语义一致。

---

#### 4.2.44 Cross-field Constraint

很多状态规则跨多个字段。

例如：

```text
if payment_status == completed:
    transaction_id must exist

if approval_status == approved:
    approval_scope_hash must exist

if task_status == success:
    success_verification must be passed
```

这类约束应该程序化，而不是依赖模型自己注意。

---

#### 4.2.45 State Reference：大对象不要直接复制进 State

Working State 不等于所有数据本体。

大对象例如：

```text
完整 PDF
整个 repository
数 GB 日志
视频
数据库结果集
```

更适合 State 保存：

```text
artifact_id
path
version
hash
relevant ranges
metadata
```

需要时再读取。

因此：

```text
State
= operational metadata + references
```

不等于：

```text
all bytes in memory
```

---

#### 4.2.46 Content Addressing / Hash 可以帮助 State 绑定对象版本

如果任务依赖某个文件：

```text
report.csv
```

仅保存文件名不够。

文件可能变化。

可以保存：

```text
path
hash
version
last_modified
```

这样后续能判断：

```text
还是同一个对象吗？
```

对于实验、评测和可复现工作尤其重要。

---

#### 4.2.47 State Provenance

关键字段最好知道：

```text
从哪里来？
什么时候得到？
由谁更新？
是否经过验证？
```

例如：

```json
{
  "value": "passed",
  "source": "pytest_run_184",
  "observed_at": "...",
  "verified": true
}
```

Provenance 可以帮助：

```text
conflict resolution
audit
recovery
trust assessment
```

---

#### 4.2.48 State Conflict

不同来源可能给出不同状态：

```text
Cache: order = pending
API: order = completed
Model summary: order = failed
```

系统不能简单取最后一句。

需要根据：

```text
source authority
version
freshness
verification
```

决定最终 State。

例如：

```text
Provider API > model summary
new version > old cache
```

---

#### 4.2.49 Conflict Resolution Policy

可以显式定义：

```text
authoritative source wins
higher version wins
fresh query wins
verified evidence wins
otherwise mark unresolved
```

最后一种非常重要：

> **冲突无法可靠解决时，应保留 unresolved，而不是强行猜一个值。**

---

#### 4.2.50 Concurrency：两个执行分支同时更新 State 怎么办？

多工具并行、Subagent、多人协作都可能出现：

```text
State_v10
├── Worker A → update X
└── Worker B → update Y
```

如果都直接覆盖：

```text
last write wins
```

可能丢失更新。

所以需要考虑：

```text
optimistic concurrency
version check
compare-and-swap
merge policy
transaction
lock
```

这些机制的基础是：

> **State Update 必须知道自己基于哪个版本。**

---

#### 4.2.51 Optimistic Concurrency Control

典型模式：

```text
read state_version = 10
↓
compute patch
↓
write if version == 10
```

如果此时已经变成：

```text
version = 11
```

则拒绝旧 patch：

```text
conflict
```

然后重新读取、合并、决策。

这比静默覆盖安全得多。

---

#### 4.2.52 Merge 并不总是字段级拼接

例如两个分支：

```text
A: selected_flight = F1
B: selected_flight = F2
```

不能简单同时保留。

这属于语义冲突。

而：

```text
A: source_1 verified
B: source_2 verified
```

可能可以集合合并。

所以 State Merge 需要知道字段语义：

```text
scalar
set
append-only list
counter
exclusive choice
state machine value
```

---

#### 4.2.53 Monotonic State

有些状态可以设计成单调增长：

```text
verified_evidence set
completed_subgoals set
spent_cost
executed_effect ledger
```

一旦发生，不应该被后续模型“改没”。

这种 **Monotonic State** 特别适合：

```text
audit
side effects
budget
completed events
```

因为它降低了回滚式幻觉。

---

#### 4.2.54 Non-monotonic State

另一些状态会合理改变：

```text
current_plan
current_hypothesis
selected_candidate
latest_page
```

这些可以被新证据推翻。

所以 State Schema 应知道：

```text
哪些字段可以覆盖？
哪些字段只能追加？
哪些字段需要显式 invalidation？
```

---

#### 4.2.55 Invalidation 比静默覆盖更可审计

旧事实失效时，与其直接删除：

```text
source A disappears
```

不如记录：

```text
source A
status = superseded
superseded_by = source B
```

这样：

```text
当前 State 清晰
历史 provenance 仍保留
```

对于高风险任务尤其有价值。

---

#### 4.2.56 State Compaction

Working State 也会增长。

例如：

```text
1000 个候选 source
数百次 tool result
大量 completed subgoals
```

因此也需要 Compaction。

但 Working State Compaction 与 Context Compression 不同：

```text
Context Compression
→ 减少模型输入

State Compaction
→ 减少系统活跃状态规模
```

State Compaction 不能破坏未来正确执行所需的信息。

---

#### 4.2.57 什么可以从 Active State 移出？

典型候选：

```text
已经完成且不再依赖的细节
旧 observation payload
历史 debug logs
已归档候选
过期 intermediate artifacts
```

可以移动到：

```text
history store
artifact store
memory
trace
```

Active State 只保留：

```text
current operational summary + references
```

---

#### 4.2.58 State Promotion to Memory

任务结束后，Working State 不应全部永久保留。

可以选择有长期价值的信息：

```text
稳定用户偏好
已确认项目约束
成功解决方案
失败经验
新技能
```

经过筛选后进入 Memory。

所以：

```text
Working State
  ↓ task completion
Selective Consolidation
  ↓
Memory
```

这会连接 4.3、4.4 和第 12 章 Learning from Experience。

---

#### 4.2.59 Memory Retrieval to Working State

反过来，任务开始时：

```text
Memory
↓ retrieve relevant items
Working State initialization
```

例如从用户长期偏好中加载：

```text
preferred_language = Chinese
```

但要注意：

```text
retrieved memory
```

不一定直接成为权威 State。

有些需要：

```text
validate freshness
confirm user intent
resolve conflict
```

之后才能激活。

---

#### 4.2.60 Checkpoint 与 Working State

Checkpoint 是：

> **Working State 在某个时刻的可恢复持久化快照。**

因此：

```text
Working State
= live operational state

Checkpoint
= persisted recoverable representation of state
```

二者不是同义词。

没有 Persistence，Working State 可以只存在内存里。

有了 Checkpoint，系统崩溃后可以恢复。

详细 Persistence 留到 4.5 和 Runtime 章节。

---

#### 4.2.61 Resume 为什么依赖完整 State？

如果系统中断后只保存：

```text
最后一条模型消息
```

通常不足以恢复。

真正 Resume 还需要：

```text
Goal
State Version
Pending Actions
External Handles
Budget
Approval
Executed Effects
Verification Status
Environment References
```

否则系统会：

```text
重复执行
忘记约束
误判完成
丢失 pending job
```

---

#### 4.2.62 Resume 前必须 Reconcile

Checkpoint 保存的是过去状态。

恢复时 Environment 可能已经变化。

因此稳健流程是：

```text
Load Checkpoint
     ↓
Re-observe Environment
     ↓
Reconcile
     ↓
Resume Decision
```

而不是：

```text
Load old State
→ continue blindly
```

---

#### 4.2.63 State 与 Idempotency

如果 Agent crash 后恢复，它可能不知道：

```text
上一个 Action 到底执行没有
```

所以 State 应保存：

```text
call_id
idempotency_key
submission_status
execution_receipt
```

这样恢复时可以先查询，而不是重复 effect。

这说明 Idempotency 不只是 Tool Execution 问题，也依赖 State Continuity。

---

#### 4.2.64 State 与 Side-effect Ledger

真实副作用最好有独立 ledger：

```text
what action
which resource
when
status
effect receipt
verification
```

Working State 可以引用 ledger 中当前任务相关记录。

但不应该让模型一句：

```text
“我已经发了邮件”
```

直接成为权威 effect state。

---

#### 4.2.65 State Security：不是所有 State 都应该进入模型

Working State 可能包含：

```text
user identifiers
internal IDs
private document refs
permission metadata
payment status
security flags
```

其中有些是系统运行需要，但模型不需要知道。

所以：

```text
Working State
  ↓ permission-aware projection
Context
```

而不是：

```text
Working State
= dump everything into prompt
```

---

#### 4.2.66 Secret 不应该成为普通 Working State 字段

例如：

```text
API key
OAuth token
password
private key
```

更合理的是：

```text
credential_ref = cred_17
```

真正 Secret 由 Runtime / Secret Manager 持有。

这样：

```text
Agent knows capability exists
≠
Agent sees credential
```

---

#### 4.2.67 State Access Control

多 Agent / Subagent 系统中，不能默认所有 Worker 都看到全部 State。

可以区分：

```text
shared state
private state
role-scoped state
parent-only state
runtime-only state
```

例如 Research Subagent 只需看到：

```text
research subquestion
source constraints
budget
```

不必看到：

```text
用户全部账户信息
其他无关 private context
```

---

#### 4.2.68 Parent–Subagent State

Subagent 可以拥有自己的局部 State：

```text
Parent State
  ↓ delegated task contract
Child State
  ↓ result / evidence
Parent State Update
```

关键是：

```text
Child State ≠ Parent State clone
```

更好的做法是最小授权、最小上下文、明确回传 Contract。

---

#### 4.2.69 Shared State 的风险

多个 Agent 直接写同一份共享字典容易出现：

```text
race condition
semantic conflict
accidental overwrite
untraceable mutation
```

更稳健的是：

```text
scoped patches
version checks
ownership rules
merge policy
append-only events
```

多 Agent 并不自动意味着“共享全部状态”。

---

#### 4.2.70 State Ownership

复杂系统可以为字段分配 owner：

```text
Planner owns plan
Budget Manager owns cost
Runtime owns execution handle
Verifier owns verification result
User / Task Contract owns goal
```

Owner 不一定表示只有一个模块能读，而是：

> **谁有权威写入权限。**

这样能减少“所有模块都能随意改所有字段”的混乱。

---

#### 4.2.71 State Schema Evolution

Agent 系统升级后 State Schema 也会变化：

```text
v1: status
v2: task_status + verification_status
```

如果旧 Checkpoint 仍存在，需要：

```text
schema_version
migration
backward compatibility
validation
```

否则升级后 resume 可能失败。

---

#### 4.2.72 State Migration

典型流程：

```text
load v1 state
↓
validate old schema
↓
migrate v1 → v2
↓
validate v2
↓
resume
```

Migration 不应该静默猜测重要字段。

缺失关键事实时，可以：

```text
mark unknown
re-observe
ask user
block
```

---

#### 4.2.73 State Corruption

Working State 本身也可能损坏：

```text
partial write
invalid JSON
missing field
impossible transition
wrong version
conflicting duplicate state
```

所以 State Store 也需要：

```text
validation
atomic write
checksum
versioning
backup / checkpoint
```

Agent Reliability 不只是模型 Reliability。

---

#### 4.2.74 Atomic State Update

如果一次 transition 同时更新：

```text
budget -= 1
last_action = X
pending_action = Y
```

中途 crash 可能出现半更新。

高一致性场景下可以使用：

```text
transaction
atomic commit
write-ahead event
```

保证 State 要么更新完整，要么不更新。

---

#### 4.2.75 Write-ahead Intent / Event

对于高风险 Action，一种稳健思路是：

```text
record intent
↓
execute action
↓
record result
↓
reconcile
```

例如：

```text
INTENT: charge order 1847
EXECUTION: submitted tx_91
RESULT: provider says completed
VERIFICATION: ledger confirmed
```

这样 crash 后能知道系统停在哪一步。

---

#### 4.2.76 State 与 No-progress Detection

Agent 是否在“忙”不等于是否在“前进”。

Working State 可以支持进度检测：

```text
completed_subgoals
unresolved_items
new_evidence_count
state_signature
last_progress_step
```

如果连续多步：

```text
Action changed
but meaningful State unchanged
```

可能是：

```text
no-progress loop
```

因此：

> **Progress 应定义为有意义的 State 改变，而不是 Action 数量。**

---

#### 4.2.77 State Signature

可以对关键状态做规范化摘要或 hash：

```text
progress_signature = hash(
    unresolved_items,
    verified_items,
    selected_candidate,
    terminal_status,
)
```

如果：

```text
signature_t == signature_{t-k}
```

且中间消耗了大量 Action，可能触发：

```text
reflection
replan
fallback
human escalation
stop
```

但必须注意：某些合法探索也可能暂时不改变关键 State。

---

#### 4.2.78 State Observability

每次重要 Transition 最好记录：

```text
state_version_before
state_version_after
event / action
fields_changed
source
actor
timestamp
validation_result
```

这样失败时可以问：

```text
哪一步把状态改错了？
```

而不是只看到最终结果。

---

#### 4.2.79 State Diff

完整 State 很大时，日志可以记录 Diff：

```text
+ verified_source: S17
- pending_query: Q3
~ task_status: researching → verifying
```

State Diff 很适合：

```text
audit
debugging
trajectory visualization
regression analysis
```

也比每一步复制全部 State 更节省。

---

#### 4.2.80 State Trace 与 Agent Trajectory

Agent Trajectory 通常记录：

```text
State_t
Action_t
Observation_{t+1}
State_{t+1}
```

因此 Working State 是 Process Evaluation 的关键对象。

如果只记录：

```text
Prompt
Final Answer
```

就很难知道：

```text
失败来自错误 Observation？
错误 State Update？
错误 Context Projection？
错误 Decision？
错误 Execution？
```

---

#### 4.2.81 Working State Evaluation

可以单独评价 State 质量。

例如：

```text
State Accuracy
State Completeness
State Freshness
State Consistency
State Update Accuracy
Invariant Violation Rate
Stale-state Rate
State–Environment Mismatch Rate
State–Context Mismatch Rate
Resume Success Rate
Conflict Resolution Accuracy
```

这比只评价最终任务成功更有诊断价值。

---

#### 4.2.82 State Accuracy

State Accuracy 问：

> 当前 State 中的事实是否和权威 Environment / Source 一致？

例如：

```text
State says tests passed
Reality says tests failed
```

就是直接 State Error。

对于可验证字段，应尽量用 deterministic comparison，而不是 LLM Judge。

---

#### 4.2.83 State Completeness

即使已有字段都正确，也可能缺少关键字段。

例如任务要求：

```text
修复 bug 且 public API 不变
```

State 只记录：

```text
tests_passed
```

却没有：

```text
api_verification_status
```

那么 State 不完整，会诱发错误 termination。

---

#### 4.2.84 State Freshness Metric

对于有时效性的字段，可以评价：

```text
age of observation
version lag
stale decision count
```

例如：

```text
Agent 基于 >10 min old inventory 作出购买决策
```

可以被单独统计。

---

#### 4.2.85 State Transition Accuracy

给定：

```text
S_t + Event_t
```

系统是否正确得到：

```text
S_{t+1}
```

这可以构造专门的 Unit Test / Benchmark。

尤其适合：

```text
approval
budget
pending action
error recovery
state machine
```

这些结构化 transition。

---

#### 4.2.86 State Invariant Violation Rate

可以统计：

```text
每 1000 transitions
出现多少 invariant violation
```

例如：

```text
budget < 0
success without verification
write without approval
completed task with pending effect
```

对于部署可靠性非常关键。

---

#### 4.2.87 Resume Success Rate

长任务系统尤其应测试：

```text
随机中断
↓
从 checkpoint 恢复
↓
能否继续并保持语义一致？
```

评价：

```text
resume correctness
no duplicate effect
no lost constraint
state reconciliation success
final outcome parity
```

---

#### 4.2.88 Working State 的最小实现

一个非常简单的实现可以是：

```python
from dataclasses import dataclass, field
from typing import Literal

@dataclass
class TaskState:
    goal: str
    constraints: list[str]
    status: Literal[
        "running",
        "blocked",
        "completed",
        "failed",
    ] = "running"
    current_subgoal: str | None = None
    pending_action_id: str | None = None
    latest_observation_ref: str | None = None
    remaining_steps: int = 10
    verified_conditions: set[str] = field(default_factory=set)
    state_version: int = 0
```

重点不是 dataclass，而是：

```text
State 有明确字段
有明确语义
有明确生命周期
```

---

#### 4.2.89 一个更可靠的 State Update

```python
def apply_event(state, event):
    assert event.base_version == state.state_version

    new_state = copy_state(state)

    if event.type == "tool_completed":
        new_state.pending_action_id = None
        new_state.latest_observation_ref = event.observation_ref

    elif event.type == "verification_passed":
        new_state.verified_conditions.add(event.condition)

    elif event.type == "budget_spent":
        new_state.remaining_steps -= event.steps

    validate_invariants(new_state)
    new_state.state_version += 1
    return new_state
```

这里的关键顺序是：

```text
Version Check
→ Apply Allowed Transition
→ Validate Invariants
→ Commit New Version
```

---

#### 4.2.90 Context Builder 如何消费 Working State？

```python
def build_context(state, decision_type):
    view = {
        "goal": state.goal,
        "constraints": state.constraints,
        "status": state.status,
        "current_subgoal": state.current_subgoal,
    }

    if decision_type == "recovery":
        view["last_error"] = state.last_error
        view["recovery_attempts"] = state.recovery_attempts

    if decision_type == "tool_selection":
        view["remaining_budget"] = state.remaining_budget

    return view
```

说明：

> **模型不必看到完整 State；它只需要看到当前 Decision 所需的 State View。**

---

#### 4.2.91 Coding Agent 示例：State 如何贯穿全过程？

任务：

```text
修复失败测试，但不能改变 public API。
```

初始化：

```text
Goal:
fix failure

Constraints:
public API unchanged

State:
status = running
tests = unknown
changed_files = ∅
api_verified = false
```

第一次运行测试：

```text
Observation:
test_x failed
```

更新 State：

```text
tests = failed
failing_test = test_x
```

读取源码并修改：

```text
changed_files = {src/a.py}
```

再次测试：

```text
tests = passed
```

但此时不能终止，因为：

```text
api_verified = false
```

继续检查 API：

```text
api_verified = true
```

只有：

```text
tests == passed
AND
api_verified == true
```

才能：

```text
status = completed
```

这里可以清楚看到：

> **Termination 是 State 条件成立的结果，而不是模型说“应该好了”。**

---

#### 4.2.92 Research Agent 示例：State 如何管理证据？

任务：

```text
判断某政策是否已经正式生效。
```

Working State：

```text
claim = policy_effective?
required_source = official
required_date = today
primary_source_found = false
effective_date = unknown
conflict = unresolved
```

找到新闻：

```text
candidate_source += news_A
```

但：

```text
primary_source_found = false
```

所以不能终止。

找到官方法规：

```text
primary_source_found = true
effective_date = 2026-10-01
```

再和今天比较：

```text
effective_date <= today
```

Verification 完成后：

```text
claim_status = verified_true
```

这就是 Evidence-driven Working State。

---

#### 4.2.93 Booking Agent 示例：为什么 Pending / Approval 必须状态化？

任务：

```text
找一张机票，确认后再购买。
```

State：

```text
selected_flight = F17
approval = pending
payment = not_started
```

用户批准后：

```text
approval = approved
approval_scope = F17 + current_price
```

如果价格随后变化：

```text
selected_flight_price_version changed
```

旧 approval 可能失效：

```text
approval = stale
```

系统需要重新确认，而不是因为 transcript 里有一句“可以”就继续付款。

---

#### 4.2.94 Working State Failure Modes

最常见的失败包括：

1. **State Hidden in Transcript**：关键状态只存在聊天历史。
2. **Model-owned Truth**：模型自然语言被当作权威事实。
3. **State–Environment Mismatch**：内部状态落后于真实世界。
4. **State–Context Mismatch**：State 已更新，Context 仍展示旧值。
5. **Stale Observation**：旧 Observation 覆盖新 Environment。
6. **Unknown-as-False**：未知结果被误写成失败。
7. **Action Success = Task Success**：局部成功被误当全局完成。
8. **Goal Drift**：任务约束未作为持续状态维护。
9. **Protected State Mutation**：模型修改 Goal、Budget、权限等保护字段。
10. **Full-state Rewrite Loss**：每轮重写整份 State 导致字段丢失。
11. **Schema Drift**：同一字段在不同模块语义不同。
12. **State Conflict Ignored**：来源冲突时直接取最后一个值。
13. **No Provenance**：不知道字段从哪里来。
14. **No Versioning**：无法检测 stale update。
15. **Lost Update**：并发写覆盖彼此修改。
16. **Partial State Commit**：crash 导致半更新。
17. **Pending State Collapsed**：把 queued / submitted / unknown 都压成 success/failure。
18. **Duplicate Effect after Resume**：恢复后不知道 Action 是否执行过。
19. **Approval State Drift**：批准范围与当前 Action 不一致。
20. **Budget State Drift**：模型认为还有预算，系统实际已耗尽。
21. **Verification State Missing**：无法知道哪些 Success Criteria 已验证。
22. **Terminal Status Ambiguity**：blocked / failed / success 都写成 done。
23. **Shared-state Race**：多个 Agent 无控制写同一状态。
24. **Oversharing State**：不必要敏感信息全部进入 Context。
25. **Secret-in-State**：Credential 被普通 State 暴露。
26. **Unbounded Active State**：State 永远只增不归档。
27. **Broken Resume**：Checkpoint 缺少 pending action / effect / version。
28. **Schema Migration Failure**：新版代码无法正确解释旧状态。
29. **No-progress Blindness**：执行很多 Action，但关键 State 不变化。
30. **State Corruption Undetected**：非法状态进入下一轮决策。

---

#### 4.2.95 Working State Engineering Principles

可以把这一节压缩成下面这些工程原则。

**原则 1：关键执行事实进入 State，不只进入自然语言。**

**原则 2：State 是当前有效真相的系统表示，不是完整历史。**

**原则 3：Context 是 State 的投影，不是 State 本身。**

**原则 4：每个关键字段尽量有明确 Source of Truth。**

**原则 5：区分 Immutable / Protected 与 Mutable State。**

**原则 6：区分 Authoritative 与 Derived State。**

**原则 7：Unknown、Pending、Failed 不要混成一个 False。**

**原则 8：使用显式 Transition，而不是让模型自由重写整份 State。**

**原则 9：Patch / Event 更新通常优于 Full-state Rewrite。**

**原则 10：每次 Transition 检查 Schema、Cross-field Constraint 与 Invariant。**

**原则 11：保存 Version、Freshness 与 Provenance。**

**原则 12：写操作前检查 State 是否仍与 Environment 一致。**

**原则 13：Action Status、Subgoal Status、Task Status 分开。**

**原则 14：Pending / Unknown Outcome 必须成为一等状态。**

**原则 15：Effect、Budget、Approval、Verification 不依赖模型自述。**

**原则 16：大对象保存 Reference + Version，而不是复制全部内容。**

**原则 17：并发 State Update 必须有 Version / Merge / Ownership 语义。**

**原则 18：Checkpoint 是 State 的持久化表示，Resume 前要 Reconcile。**

**原则 19：State 访问遵循 Least Privilege。**

**原则 20：Progress 看有意义的 State Change，而不是 Action Count。**

---

#### 4.2.96 一个完整的 State Lifecycle

把前面的内容串起来：

```text
Task / Goal
    ↓
Initialize Working State
    ↓
Observe Environment
    ↓
Reconcile
    ↓
Project State → Context
    ↓
Decision
    ↓
Validate / Authorize
    ↓
Record Intent
    ↓
Execute Action
    ↓
Receive Observation
    ↓
Apply State Transition
    ↓
Validate Invariants
    ↓
Verify Progress / Completion
    ↓
Checkpoint if needed
    ↓
Continue / Terminate
    ↓
Archive / Consolidate to Memory
```

这就是 Working State 在 Agent 生命周期中的完整位置。

---

#### 4.2.97 与 2.2 Agent Loop 的关系

2.2 已经定义：

```text
Observe
→ State Update
→ Context
→ Decide
→ Validate
→ Act
→ Observe
→ Terminate
```

4.2 则回答：

> **这里的 State Update 到底在更新什么？怎样才能可靠？**

所以：

```text
2.2 Agent Loop
= control-flow view

4.2 Working State
= operational-state view
```

二者是同一系统的两个视角。

---

#### 4.2.98 与 4.1 Context Engineering 的关系

4.1：

```text
What should the model see now?
```

4.2：

```text
What must the system know now?
```

可以记成：

```text
Working State
= system-visible operational truth

Context
= model-visible decision view
```

因此：

> **State 追求完整到足以正确执行；Context 追求最小到足以正确决策。**

---

#### 4.2.99 与 4.3 Short-term Memory 的关系

Working State 保存：

```text
当前任务必须持续有效的操作状态
```

Short-term Memory 更关注：

```text
近期发生过、可能再次相关、但不一定属于当前权威状态的信息
```

例如：

```text
Working State:
current_selected_option = F17

Short-term Memory:
用户刚才否定过 F12，因为转机太久
```

后者可能影响后续选择，但不是当前系统状态的核心字段。

下一节会专门拆这个边界。

---

#### 4.2.100 与 4.5 Persistence 的关系

Working State 是：

```text
what state exists
```

Persistence 是：

```text
how state survives time / crash / process boundary
```

因此：

```text
State
≠
Persistence
```

State 可以存在但不持久。

Persistence 可以保存：

```text
Working State
Memory
Artifacts
Checkpoints
Logs
```

---

#### 4.2.101 与 Harness 的关系

Harness 通常负责：

```text
State transition policy
Context projection policy
permission-aware mutation
budget update
approval routing
termination rules
recovery rules
```

所以 Working State 是 Harness 控制循环的重要输入输出。

但：

```text
Working State
```

本身仍是系统状态概念，不等于 Harness。

---

#### 4.2.102 与 Runtime 的关系

Runtime 负责让 State 真正可执行：

```text
storage
transaction
checkpoint
session
queue
worker
sandbox
process
filesystem
```

可以记成：

```text
Working State
= semantic task state

Runtime
= state persistence + execution substrate
```

后面第 8 章会进一步细化。

---

#### 4.2.103 一个边界表

| 概念 | 核心问题 | 与 Working State 的关系 |
|---|---|---|
| Environment State | 世界真实是什么？ | Working State 的外部依据 |
| Observation | 刚刚观察到了什么？ | State Update 的输入 |
| Working State | 当前任务继续执行必须知道什么？ | 本节主体 |
| Context | 本轮模型实际看到什么？ | Working State 的投影之一 |
| Transcript | 历史上说过 / 做过什么？ | 历史记录，不等于当前 State |
| Plan | 准备怎么做？ | Working State 的组成部分之一 |
| Short-term Memory | 近期哪些信息可能再次有用？ | 可被激活进入 State / Context |
| Long-term Memory | 哪些信息跨任务长期保留？ | 不等于当前 State |
| Checkpoint | 如何保存某时刻 State 以恢复？ | State 的持久化快照 |
| Persistence | 状态如何跨时间 / crash 存活？ | 存储机制 |
| Runtime State | 执行基础设施此刻是什么状态？ | 与语义 Working State 相邻但不同 |
| Event Log | 发生过哪些 transition？ | 可重建 / 审计 State |
| Verifier | 当前条件是否成立？ | 产生 Verification State |

---

#### 4.2.104 面试时必须能回答的问题

**Q1：什么是 Working State？**

当前一个活跃任务为了继续正确执行，由 Agent 系统显式维护的、当前有效的操作状态。

---

**Q2：Working State 和 Context 有什么区别？**

Working State 是系统必须知道的当前任务状态；Context 是当前模型调用实际看到的 State 投影和其他信息。

---

**Q3：Working State 和 Memory 有什么区别？**

Working State 面向当前活跃任务；Memory 面向过去信息的保存与未来复用。Memory 可以被检索并激活进 Working State。

---

**Q4：为什么不能直接用完整对话历史当 State？**

历史同时保留新旧事实、模型自述和已失效信息，无法直接表达“当前什么仍然有效”，也难以验证、并发更新和恢复。

---

**Q5：什么是 Authoritative State？**

由明确 Source of Truth 支持、系统应当据此执行的权威字段，例如真实预算、Git commit、支付状态、批准记录。

---

**Q6：为什么 State Update 最好用 Patch / Event，而不是让模型重写整个 JSON？**

因为局部更新更容易验证、审计和控制权限，也能减少字段丢失、保护字段被篡改与并发冲突。

---

**Q7：Unknown 和 False 为什么必须区分？**

Unknown 表示尚无可靠结论；False 表示已有证据确认条件不成立。把 Unknown 当 False 会诱发错误 retry 或错误决策。

---

**Q8：什么是 State–Environment Mismatch？**

Agent 内部维护的状态与真实外部环境已经不一致，例如 State 仍指向旧 Git head。

---

**Q9：什么是 State–Context Mismatch？**

系统 State 已更新，但本轮模型看到的 Context 仍是旧状态或错误投影。

---

**Q10：State Version 有什么用？**

用于检测 stale update、并发冲突、resume 版本和对象变化，是可靠状态转移的重要基础。

---

**Q11：为什么 Pending / Unknown Outcome 是一等状态？**

外部 Action 可能已经提交但结果未知；如果直接当失败 retry，可能造成重复支付、重复发送等副作用。

---

**Q12：Checkpoint 和 Working State 有什么区别？**

Working State 是 live state；Checkpoint 是某一时刻用于持久化和恢复的 State 表示。

---

**Q13：Resume 为什么不能直接加载旧 State 后继续？**

因为中断期间 Environment 可能变化，必须重新观察并 reconcile，否则会基于 stale state 执行。

---

**Q14：多 Agent 共享 State 最大的问题是什么？**

并发覆盖、语义冲突和权限过宽，因此需要字段 ownership、版本控制、局部 patch 和 merge policy。

---

**Q15：如何评价 Working State 质量？**

看 State Accuracy、Completeness、Freshness、Consistency、Transition Accuracy、Invariant Violation、State–Environment / State–Context Mismatch 与 Resume Success。

---

**Q16：为什么 Working State 不应该存 Secret 明文？**

任务可能需要能力引用，但不需要模型或一般状态读取 credential；Secret 应由 Runtime / Secret Manager 持有，只在执行边界注入。

---

**Q17：Working State 与 Agent Loop 的关系是什么？**

Agent Loop 定义状态如何在 Observe–Decide–Act 之间流动；Working State 是这条 Loop 中被持续维护的语义状态载体。

---

**Q18：为什么 Progress 应看 State Change，而不是 Action Count？**

Agent 可以连续搜索、重试、反思却没有减少未解决问题；只有关键状态朝 Success Criteria 推进才是真正进展。

---

#### 4.2.105 一句话总结

> **Working State 是 Agent 当前任务的可执行状态骨架：它显式维护 Goal、约束、进度、环境引用、Action / Effect、Verification、Approval、Budget、Error 与 Terminal Status，并通过受验证的 State Transition 随 Observation 和 Event 更新。Context 是 Working State 面向当前模型决策的投影，Memory 是跨时间可复用的信息存储，Environment 则是真实外部世界。可靠 Agent 必须让 State 有明确 Schema、Source of Truth、Version、Freshness、Provenance、Invariant 与 Recovery 语义，而不是把“现在做到哪了”寄托在模型从长 Transcript 中自行猜测。**

---

#### 4.2.106 参考资料

1. Sutton, R. S., & Barto, A. G. **Reinforcement Learning: An Introduction.** 2nd ed., MIT Press, 2018. 用于理解 state、observation、policy、transition 与 partial observability 的基础概念。
2. Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. **Planning and Acting in Partially Observable Stochastic Domains.** *Artificial Intelligence*, 1998. 用于理解 Agent 在不完整 Observation 下维护内部状态 / belief 的理论背景。
3. Kleppmann, M. **Designing Data-Intensive Applications.** O'Reilly, 2017. 用于理解 event log、snapshot、versioning、concurrency、consistency、idempotency 与 recovery。
4. Fowler, M. **Patterns of Enterprise Application Architecture.** Addison-Wesley, 2002. 用于理解 Unit of Work、Identity Map、transactional state 与持久化边界等工程模式。
5. Hohpe, G., & Woolf, B. **Enterprise Integration Patterns.** Addison-Wesley, 2003. 用于理解 message、event、correlation、idempotent receiver 与 long-running workflow state。
6. OpenTelemetry. **Trace and Context Concepts.** 用于理解 execution trace、correlation、provenance 与跨组件状态观测。
7. Yao, S., Zhao, J., Yu, D., et al. **ReAct: Synergizing Reasoning and Acting in Language Models.** *ICLR*, 2023. arXiv:2210.03629. 用于理解 Action–Observation 交互如何形成持续 Agent trajectory。
'''

section_42_pattern = re.compile(
    r"### 4\.2 Working State\n.*?(?=\n### 4\.3 Short-term Memory)",
    re.DOTALL,
)
section_42_matches = section_42_pattern.findall(text)
assert len(section_42_matches) == 1, f"expected one 4.2 section, got {len(section_42_matches)}"
text = section_42_pattern.sub(lambda _m: new_section.rstrip("\n"), text, count=1)

progress_pattern = re.compile(
    r"^\|\s*II\s*\|\s*4\. Context, Memory & Retrieval\s*\|.*\|$",
    re.MULTILINE,
)
progress_matches = progress_pattern.findall(text)
assert len(progress_matches) == 1, f"expected one chapter-4 progress row, got {progress_matches}"
text = progress_pattern.sub(
    "| II | 4. Context, Memory & Retrieval | 进行中：4.1–4.2 已完成 |",
    text,
    count=1,
)

footer_pattern = re.compile(
    r"^下一步：继续 .*4\. Context, Memory & Retrieval.*4\.1 Context Engineering.*$",
    re.MULTILINE,
)
footer_matches = footer_pattern.findall(text)
assert len(footer_matches) == 1, f"expected one chapter-4 footer, got {footer_matches}"
text = footer_pattern.sub(
    "下一步：继续 **II. Capabilities & Interoperability → 4. Context, Memory & Retrieval → 4.3 Short-term Memory**。",
    text,
    count=1,
)

DOC.write_text(text, encoding="utf-8")
print("PATCH_OK")
