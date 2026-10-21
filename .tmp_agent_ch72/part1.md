### 7.2 Agent Loop Policy

7.1 已经回答了：**Harness 是什么，以及它为什么是 Agent 的运行时控制层。**

7.2 不再重复 Harness 的定义，而是进一步回答一个更具体的问题：

> **一次 Agent run 到底怎样被持续驱动？什么时候应该再次调用模型，什么时候应该执行确定性逻辑、等待事件、验证结果、探索分支，什么时候必须停止？**

Chapter 2.2 已经从 Agent 基础机制角度解释过：

```text
State → Decision → Action → Observation → State Update
```

这一节讨论的不是这个闭环“长什么样”，而是：

> **谁拥有这个闭环的推进权，以及每一次状态转移应该依据什么 policy 发生。**

---

#### 7.2.1 Agent Loop Policy 到底是什么

**Agent Loop Policy** 是 Harness 中负责控制 Agent run 生命周期与状态转移的策略层。

它决定：

```text
当前 run 处于什么状态？
现在是否需要新的 model decision？
已有 action 是否应该先执行？
是否必须等待外部事件？
当前结果是否需要 verification？
是否需要探索替代 branch？
失败后是 retry、recover、escalate 还是 stop？
当前是否仍在取得 progress？
是否已经达到 terminal state？
```

最短定义可以写成：

> **Loop Policy 决定 Agent run 的下一次合法状态转移。**

因此：

```text
Agent Loop
= 运行中的反馈闭环

Loop Policy
= 控制这个闭环何时、为何、向哪里推进的规则
```

---

#### 7.2.2 Agent Loop ≠ Agent Loop Policy

这是 Chapter 2.2 与 7.2 的核心边界。

Chapter 2.2 主要回答：

```text
一个 Agent loop 由哪些基本元素组成？
State / Observation / Decision / Action 如何流动？
```

7.2 主要回答：

```text
当前 state 下，下一步允许发生什么？
是否真的需要再调用一次模型？
何时应该 suspend，而不是继续循环？
何时应该验证、分支或终止？
怎样防止循环失控？
```

所以可以记成：

```text
Chapter 2.2 = loop mechanics
Chapter 7.2 = loop control policy
```

---

#### 7.2.3 一次 Agent run 的真正 Driver 是谁

直觉上很容易把 Agent 理解成：

```text
LLM 想一步
→ 调一个 Tool
→ 再想一步
→ 再调一个 Tool
→ ...
```

但生产系统不能把整个 run 的推进权完全交给模型。

更准确的结构是：

```text
Harness / Runner / Orchestrator
        ↓
inspect current state
        ↓
decide legal transition
        ↓
possibly call model
        ↓
possibly execute action
        ↓
update state
        ↓
repeat transition policy
```

因此：

> **Model 可以提出下一步，但 Harness 才是 Agent run 的 driver。**

模型可以说：

```text
我还需要继续搜索。
```

Loop Policy 仍然可以判断：

```text
budget exhausted
same query repeated
sufficient evidence already collected
waiting for unavailable dependency
risk threshold exceeded
```

并拒绝继续。

---

#### 7.2.4 Model Call 不是 Agent Loop 的“时钟”

一种常见但危险的实现是：

```python
while not done:
    response = call_model(state)
```

这相当于默认：

> **只要任务还没结束，就应该再调用一次模型。**

但很多状态转移根本不需要模型：

```text
等待异步任务完成
检查固定 schema
执行 deterministic retry
读取已经完成的 tool result
检查 deadline
进行权限 gate
做 idempotency reconciliation
验证文件是否存在
更新结构化计数器
触发固定 fallback
```

因此更准确的原则是：

> **Model Call 是一种昂贵的、语义型 transition，而不是 Loop 每一拍都必然发生的 heartbeat。**

---

#### 7.2.5 Loop Policy 的三个核心问题

可以把整节压缩成三个问题。

##### 问题一：当前应该推进吗？

```text
CONTINUE
WAIT
SUSPEND
STOP
```

##### 问题二：如果推进，由谁推进？

```text
Model
Deterministic Logic
Tool / Runtime
Verifier
Human
Subagent
External Event
```

##### 问题三：推进到哪里？

```text
next action
verification
branch
recovery
approval
terminal state
```

因此 Loop Policy 并不是简单的：

```text
continue = true / false
```

而是一个**状态转移选择器**。

---

#### 7.2.6 最小 Agent Loop State Machine

可以先建立一张最小状态机：

```text
                         ┌──────────────┐
                         │    READY     │
                         └──────┬───────┘
                                ↓
                       ┌────────────────┐
                       │ MODEL_DECISION │
                       └───────┬────────┘
                               ↓
                       ┌────────────────┐
                       │ ACTION_PROPOSED│
                       └───────┬────────┘
                               ↓
                    validate / approve / route
                               ↓
                       ┌────────────────┐
                       │   EXECUTING    │
                       └───────┬────────┘
                               ↓
                       ┌────────────────┐
                       │  OBSERVATION   │
                       └───────┬────────┘
                               ↓
                       ┌────────────────┐
                       │  STATE_UPDATE  │
                       └───────┬────────┘
                               ↓
                    ┌──────────────────────┐
                    │ TRANSITION_DECISION  │
                    └──────────┬───────────┘
          ┌──────────┬─────────┼─────────┬──────────┬─────────┐
          ↓          ↓         ↓         ↓          ↓         ↓
      CONTINUE     VERIFY     WAIT     BRANCH    RECOVER     STOP
          │          │         │         │          │
          └──────────┴─────────┴─────────┴──────────┘
                              ↓
                         next state
```

真实系统通常会更复杂，但这张图已经表达了一个重要原则：

> **“下一次调用模型”只是众多 transition 中的一种。**

---

#### 7.2.7 Running、Waiting、Terminal 是三类根本不同的状态

从生命周期角度，一个 run 至少要区分三大类状态。

##### Running

系统目前可以主动推进：

```text
READY
DECIDING
EXECUTING
VERIFYING
RECOVERING
```

##### Waiting / Suspended

系统当前缺少外部条件：

```text
WAITING_FOR_USER
WAITING_FOR_APPROVAL
WAITING_FOR_TOOL
WAITING_FOR_SUBAGENT
WAITING_FOR_EVENT
WAITING_UNTIL_TIME
```

##### Terminal

当前 run 已不再继续：

```text
SUCCEEDED
FAILED
BLOCKED
CANCELLED
TIMED_OUT
BUDGET_EXHAUSTED
```

最大的工程错误之一，就是把：

```text
WAITING
```

误当成：

```text
还没完成，所以继续 call model
```

---

#### 7.2.8 Loop Policy 本质上是 Transition Policy

可以把它抽象成：

$$
T_t = \Pi_{loop}(S_t, O_t, E_t, B_t, P_t)
$$

其中：

- $S_t$：当前 durable / working state；
- $O_t$：最新 observation；
- $E_t$：当前可用 event；
- $B_t$：剩余 budget；
- $P_t$：权限、风险与系统 policy；
- $T_t$：下一次 transition。

$T_t$ 可以是：

```text
CALL_MODEL
EXECUTE_ACTION
VERIFY
WAIT
RESUME
BRANCH
RETRY
RECOVER
ESCALATE
STOP
```

这里最重要的变化是：

> **Loop Policy 的输出不是“自然语言答案”，而是下一次运行时 transition。**

---

#### 7.2.9 什么情况下应该再次调用模型

Model Call 应该发生在**需要新的语义决策**时。

常见触发条件包括：

1. 新 observation 改变了当前决策条件；
2. 上一个 action 已完成，需要决定下一步；
3. 当前存在多个非确定性行动方案，需要语义判断；
4. verifier 给出新的失败证据，需要决定如何修正；
5. 用户提供了新的信息或约束；
6. approval 返回后，需要重新规划剩余路径；
7. branch 汇合后，需要综合多个结果；
8. 当前 plan 已失效，需要 semantic replanning；
9. 一个外部 event 改变了可行动状态。

可以记成：

```text
new decision-relevant information
        ↓
semantic choice required
        ↓
CALL_MODEL
```

不是每个新字节、每个日志事件都值得一次 model call。

---

#### 7.2.10 什么情况下不应该调用模型

下面这些情况通常优先由系统直接处理。

##### Deterministic validation

```text
JSON schema valid?
file exists?
HTTP status == 200?
checksum matches?
required field present?
```

##### Mechanical retry

```text
429 + Retry-After
transient network timeout
known retryable database error
```

##### Fixed policy gate

```text
permission denied
budget exhausted
approval required
capability unavailable
```

##### Passive waiting

```text
job still running
user has not replied
approval has not arrived
scheduled time not reached
```

##### Deterministic completion check

```text
tests passed
artifact exists
record state == submitted
expected count == actual count
```

原则是：

> **能由可靠程序逻辑直接判断的 transition，不要为了“Agent 感”而强行再问一次模型。**

---

#### 7.2.11 Semantic Transition 与 Deterministic Transition 要分开

一个成熟 Loop 应该同时存在两类 transition。

##### Semantic Transition

需要模型判断：

```text
下一步应该搜索哪个方向？
两个证据冲突时更相信谁？
当前失败是否需要换策略？
怎样改写查询才能获得缺失信息？
```

##### Deterministic Transition

系统规则已经足够：

```text
超过 retry_limit → STOP / RECOVER
审批未完成 → WAIT
测试失败 → VERIFY_FAILED
任务到期 → TIMEOUT
```

因此：

```text
Loop Intelligence
≠
全部交给 LLM
```

更合理的是：

```text
Semantic uncertainty → Model
Mechanical certainty → Code / Policy
```

---

#### 7.2.12 Action–Observation Loop 真正怎样推进

生产级闭环不应写成：

```text
Model → Tool → Model
```

而更接近：

```text
Current State
    ↓
Context Construction
    ↓
Model Decision
    ↓
Action Intent
    ↓
Validation / Permission / Approval
    ↓
Execution
    ↓
Raw Result
    ↓
Observation Construction
    ↓
State Update
    ↓
Progress / Verification Check
    ↓
Transition Policy
    ↓
next state
```

这里每个箭头都可能失败、等待、暂停或产生新的 policy decision。

所以：

> **Agent Loop 不是“LLM 与 Tool 对话”，而是 Harness 管理的一串显式状态转移。**

---

#### 7.2.13 Tool Result ≠ Observation ≠ Next Prompt

7.1 已经说明 Raw Result 与 Observation 要区分。

到了 Loop Policy 层，还要再多区分一步：

```text
Tool Result
    ↓
Observation Construction
    ↓
State Update
    ↓
Transition Decision
    ↓
possibly Build Next Context
```

因此 Tool 返回：

```text
job_id = 8472
status = accepted
```

不能立刻机械变成：

```text
Assistant, here is the tool result. What next?
```

Loop Policy 应先判断：

```text
这是完成结果还是仅表示已接收？
是否需要等待？
是否需要 poll？
是否已经存在 callback / webhook？
是否应该把 job_id 存入 durable state？
```

---

#### 7.2.14 Fresh Observation 才能闭合反馈回路

Action 发生后，如果环境可能变化，就不能只依据旧 State 推理。

例如：

```text
Agent: deploy service
Runtime: command returned 0
```

Loop Policy 不应自动推断：

```text
service healthy
```

还可能需要：

```text
health check
read deployment status
verify endpoint
inspect logs
```

因此：

> **执行完成只是 transition 完成；任务进展需要新的 observation 证明。**

这也是为什么 Loop Policy 与 Verification Policy 紧密连接，但二者不能混成一个概念。

---

#### 7.2.15 Pending Action 必须是一等状态

如果 Tool 调用是异步的，Harness 需要显式保存：

```text
pending_action_id
action_type
submitted_at
expected_completion_signal
poll_policy / callback
retry_count
idempotency_key
owner
```

否则下一轮模型很容易：

- 忘记已有任务正在执行；
- 重复提交相同 action；
- 错把“submitted”当“completed”；
- 对同一副作用执行两次；
- 在结果尚未产生时凭空继续推理。

因此：

> **Pending ≠ Unknown；Pending 是一种需要被 Harness 明确建模的运行状态。**

---

#### 7.2.16 Async Action 之后不应该自动 Re-call Model

假设 Agent 提交一个需要 20 分钟的任务：

```text
start_training_job()
```

错误做法是：

```text
submit
→ call model
→ model asks status
→ poll
→ call model
→ model asks status
→ poll
→ ...
```

更合理的做法是：

```text
submit
→ persist pending state
→ WAIT
→ external completion event / scheduled poll
→ receive fresh observation
→ resume
→ only then decide whether model is needed
```

这就是：

> **event-driven Agent loop，而不是 token-driven busy loop。**

---

#### 7.2.17 CONTINUE 到底意味着什么

`CONTINUE` 不应该表示：

```text
任务还没完成，所以再来一轮。
```

更严格的定义是：

> **当前已经拥有足够的新状态，并且存在一个可立即执行、仍有价值的下一 transition。**

例如：

```text
search result arrived
→ evidence gap remains
→ next semantic query needs decision
→ CONTINUE → CALL_MODEL
```

或者：

```text
model proposed safe tool action
→ validation passed
→ CONTINUE → EXECUTE_ACTION
```

因此 CONTINUE 后面仍然要带 transition type。

---

#### 7.2.18 WAIT 到底意味着什么

`WAIT` 表示：

> **当前任务并未结束，但主动计算已经不能产生有效新信息；下一次合法进展依赖外部事件或时间。**

典型情况：

```text
等待用户补充信息
等待审批
等待异步任务完成
等待远端系统状态变化
等待定时窗口
等待另一个 agent / worker 返回
```

WAIT 的核心不是“慢”，而是：

```text
progress dependency is external
```

因此：

> **等待不是失败，也不是思考不足。**

---

#### 7.2.19 WAIT 与 SUSPEND 的区别

可以做一个工作定义：

```text
WAIT
= 逻辑状态：当前缺少外部 event

SUSPEND
= 运行时动作：把 active execution 释放掉，并保存可恢复状态
```

例如：

```text
state = WAITING_FOR_APPROVAL
runtime action = checkpoint + suspend
```

审批到达后：

```text
external event
→ load checkpoint
→ reconcile state
→ RESUME
```

这为 Chapter 8 的 durable execution 留出了清晰接口。

---

#### 7.2.20 Agent 应该是 Event-driven，而不是 Busy-loop

更成熟的 Loop 心智模型是：

```python
while run_is_active:
    state = load_state()

    if terminal(state):
        stop()

    elif waiting_for_event(state):
        suspend()

    elif deterministic_transition_available(state):
        apply_transition()

    elif verification_required(state):
        verify()

    elif semantic_decision_required(state):
        call_model()

    else:
        fail_closed_or_escalate()
```

这里最关键的是：

```text
while run_is_active
```

并不等于：

```text
while True: call_model()
```

---

#### 7.2.21 Resume 不是简单把旧 Prompt 再发一次

一个被 suspend 的 Agent 恢复时，需要先做：

```text
load durable state
        ↓
consume triggering event
        ↓
reconcile pending actions
        ↓
refresh stale observations
        ↓
re-check permission / budget / deadline
        ↓
reconstruct current working context
        ↓
choose next transition
```

所以：

> **Resume 是状态恢复过程，不是消息重放。**

否则很容易出现：

- 重复执行已完成 action；
- 使用过期权限；
- 忽略等待期间发生的环境变化；
- 丢失用户后来追加的约束。

---

#### 7.2.22 VERIFY 为什么是独立 Transition

很多 Agent 会犯一个错误：

```text
Action completed
→ Model says looks good
→ STOP
```

更合理的是：

```text
Action completed
→ VERIFY
→ completion evidence sufficient?
    ├─ yes → candidate for STOP
    └─ no  → CONTINUE / RECOVER / BRANCH
```

VERIFY 可以由：

```text
deterministic checker
test suite
schema validator
query-back
read-after-write
independent model / evaluator
human review
```

完成。

因此：

> **Verify 是 Loop 中改变“是否可以结束”判断的状态转移，不等于普通反思。**

