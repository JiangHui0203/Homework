# 第 12 章 Agent Trajectory Anatomy：把一次 Agent 运行表示成可回放、可归因的数据资产

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 10 章 Agent Task Design`](./10_Agent_Task_Design.md)、[`第 11 章 Environment Design`](./11_Environment_Design.md)
>
> 关联章节：[`第 5 章 Tool-use Data 与 Agent Trajectory Data`](./05_Tool_Use_and_Agent_Trajectory_Data.md)、[`第 13 章 Task Success 与 Credit Assignment`](./13_Task_Success_and_Credit_Assignment.md)、[`第 14 章 Agent Failure Taxonomy`](./14_Agent_Failure_Taxonomy.md)、[`第 19 章 Data Governance、Lineage 与 Reproducibility`](./19_Data_Governance_Lineage_and_Reproducibility.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**Agent Trajectory Representation 的 canonical chapter。它负责 typed event log、state lineage、context / memory lineage、branch / retry / backtrack / replay 以及由 Raw Trace 派生不同 Data View 的表示方法；system-wide provenance / dataset governance 归第 19 章。**
>
> 本章核心问题：**一次 Agent 运行到底应该怎样记录，才能准确恢复“当时 Agent 看到了什么、决定了什么、真正执行了什么、环境发生了什么、上下文如何变化、分支从哪里产生，以及后来还能不能重放和重新派生监督信号”。**

---

# 12.0 Trajectory 不是聊天记录，而是执行事实

最简单的日志可能只是：

```text
User: 取消订单 1847
Assistant: 我先查一下。
Tool Call: get_order_status(1847)
Tool Result: pending
Tool Call: cancel_order(1847)
Tool Result: success
Assistant: 已取消。
```

这足够人类大致理解发生了什么，却不足以支持严谨的数据工作。

如果要做：

```text
step-level evaluation
failure localization
counterfactual branching
replay
credit assignment
SFT / preference / eval view reconstruction
context-truncation audit
```

至少还需要知道：

```text
这个 Tool Call 是模型主动产生的，还是 Harness 自动重试？
Agent 当时真正可见的 Observation 是什么？
World State 与 Agent-visible State 是否一致？
Tool Call 前后环境发生了什么 State Diff？
这次动作是不是上一动作的 retry？
分支是否真的来自同一个 authoritative state？
结束是 Model Stop 还是 Harness 达到 max_steps？
哪些字段只对研究者可见，哪些在线模型真的能看到？
```

因此本章采用一个核心定义：

> **Agent Trajectory = Typed Event Log + State Lineage + Execution Evidence。**

而不是简单的 transcript。

---

# 12.1 从经典序列到 Typed Event Log

经典 Agent trajectory 可以写成：

\[
\tau=(s_0,a_0,o_1,s_1,a_1,o_2,\ldots,s_T)
\]

这个形式很适合理论分析，但真实系统通常需要更细的 event 表示：

\[
\tau=(e_0,e_1,\ldots,e_n)
\]

其中 event 可以是：

```text
USER_MESSAGE
SYSTEM_MESSAGE
MODEL_DECISION
TOOL_CALL
TOOL_RESULT
ENVIRONMENT_EVENT
STATE_UPDATE
MEMORY_READ
MEMORY_WRITE
RETRY
BACKTRACK
VERIFY
FINAL_RESPONSE
TERMINATION
```

Event-based schema 的价值在于：

```text
谁产生了这个事件？
它影响了什么？
是否对 Agent 可见？
它和前一个事件是什么关系？
它属于逻辑动作、执行尝试，还是评价结果？
```

都可以被显式记录。

---

# 12.2 五类状态必须拆开

本书不鼓励裸写 `State`。在 Agent trajectory 中至少要区分：

```text
World State
Environment State
Agent-visible State
Working State
Persistent Memory
```

完整定义与 Environment 语义见第 11 章，这里只讨论它们在 trajectory 中如何被记录。

## 12.2.1 World State

真实世界中此刻成立的事实。

例如：

```text
order_1847.status = shipped
```

Agent 未必能直接访问。

## 12.2.2 Environment State

当前受控任务环境中被系统显式建模、可快照和验证的状态。

例如：

```text
DB row
filesystem tree
calendar entries
permission map
```

## 12.2.3 Agent-visible State

模型做决策时实际能使用的信息：

```text
User request
System / Developer instruction
Tool schemas
Visible history
Tool observations
Retrieved memory
Structured working state
```

所以：

> **World State ≠ Environment State ≠ Agent-visible State。**

## 12.2.4 Working State

系统显式维护、允许进入后续决策的结构：

```text
resolved entities
open subgoals
known facts
uncertainties
pending verification
current plan
```

它不是模型不可见的内部神经状态。

## 12.2.5 Persistent Memory

跨较长时间甚至跨 episode 保存的信息，例如：

```text
user preference
project context
confirmed entity mapping
historical task state
```

Memory 必须通过显式 read / write event 进入 trajectory，否则模型行为会显得“凭空知道”。

---

# 12.3 Context 与 State 不是一回事

系统可能拥有很多信息，但模型只会看到被 Harness 选进 context 的那一部分。

```text
Full System State
      ↓
Context Construction Policy
      ↓
Actual Model Context
      ↓
Decision
```

因此 trajectory 应该能够恢复：

```text
context_version
visible_event_ids
retrieved_memory_ids
summarized_ranges
truncated_event_ids
```

这对于区分下面两种情况尤其重要：

```text
模型明明看到了关键事实却没用
```

与：

```text
Harness 根本没有把关键事实放进 context
```

后者不能简单归因成模型忘记。

---

# 12.4 Decision Intent、Planned Action、Executed Action 必须分层

Agent 可能说：

```text
“我应该先查询订单状态。”
```

但真正执行：

```text
cancel_order(1847)
```

所以至少要区分：

```text
Decision Intent
Planned Action
Executed Action
Execution Result
```

这能揭示：

```text
plan-action inconsistency
serialization bug
harness dispatch bug
policy override
```

Action 也不只包括 Tool Call，还可以是：

```text
ASK_USER
WAIT
ABORT
DELEGATE
VERIFY
BACKTRACK
WRITE_MEMORY
READ_MEMORY
FINAL_RESPONSE
```

因此 function calling 只是 action space 的一个子集。

---

# 12.5 Observation 不等于 Tool Result

Observation 指 Agent 获得的新信息，它可能来自：

```text
Tool Result
User Reply
Environment Event
Permission Error
Timeout
File Change
Another Agent
Human Approval
```

一个规范 Observation 至少应记录：

```json
{
  "event_type": "observation",
  "source": "tool",
  "source_id": "get_order_status",
  "status": "ok",
  "payload": {
    "order_id": "1847",
    "status": "pending"
  },
  "visible_to_agent": true
}
```

进一步还要区分：

```text
observation_received
observation_parsed
observation_used
```

因为 Agent “收到”一个 Observation，并不代表它真的 grounding 到下一步决策中。

---

# 12.6 Raw Message、Normalized Event、Decision Transition 三层表示

真实系统通常先得到 API messages：

```json
{"role":"assistant", ...}
{"role":"tool", ...}
```

但一个 message 可能同时包含：

```text
自然语言说明
Tool Call
结构化状态
Final answer fragment
```

所以推荐三层表示：

```text
L0 Raw Message / Runtime Log
        ↓
L1 Normalized Typed Events
        ↓
L2 Decision / Transition Representation
```

其中：

```text
L0
保留原始事实

L1
统一不同模型和工具 API

L2
服务分析、训练和 credit assignment
```

这是 trajectory-local representation；更广义的数据治理层级见第 19 章。

---

# 12.7 推荐的 Event Schema

一个事件至少应该有下面几组字段。

## Identity

```text
trajectory_id
episode_id
task_id
event_id
run_id
candidate_id
branch_id
```

## Event Semantics

```text
event_type
actor
action_type
source
payload
status
```

## Local Lineage

```text
parent_event_id
parent_state_id
branch_from_event_id
retry_of_attempt_id
backtrack_to_state_id
call_id
logical_action_id
```

## Visibility

```text
visible_to_agent
visible_to_researcher
included_in_context
```

## Runtime Reference

```text
model_version
prompt_version
toolset_version
harness_version
environment_snapshot_id
```

## Cost / Timing

```text
timestamp
latency_ms
input_tokens
output_tokens
tool_cost
```

## Evaluation Reference

```text
verifier_result
judge_result
human_label
failure_label
reward
```

注意：这里保存的是与 trajectory 关联的局部引用。Dataset-level lineage、version history 和 audit trail 的 canonical owner 是第 19 章。

---

# 12.8 Step 怎么切？Segmentation 必须服务下游问题

Trajectory 可以按不同粒度切分。

### Message-level

```text
一条 message = 一步
```

适合简单日志，但经常太粗。

### Tool-call-level

```text
Tool Call + Result = 一步
```

适合 function calling / tool accuracy。

### Decision-level

```text
Agent-visible State
→ Decision
→ Action
→ Observation
```

最适合 process analysis 和 credit assignment。

### Subgoal-level

```text
定位目标
判断条件
执行写操作
验证结果
```

最适合 long-horizon planning，但自动切分困难。

因此：

> **Segmentation 不是日志格式选择，而是 supervision design。**

要研究 tool selection，就不必强行做 subgoal segmentation；要研究 long-horizon recovery，仅按 message 切又远远不够。

---

# 12.9 Sequence 不够时，要用 Graph

线性轨迹：

```text
A → B → C → D
```

只适用于没有分支、回退、并行的简单 episode。

真实 Agent 可能出现：

```text
Branching
Backtracking
Parallel Actions
Delegation
Join
```

例如：

```text
State S
├── Query Inventory
├── Query Price
└── Query Shipping
       ↓
      Join
       ↓
Next Decision
```

因此复杂 trace 最好支持：

```text
parent_event_ids
branch_id
join_id
```

而不是强行把并行事件解释成因果顺序。

---

# 12.10 Same-state Branch Lineage 是局部比较的前提

若从同一个 state 产生多个 candidate：

```text
Authoritative State S
├── Candidate A
├── Candidate B
└── Candidate C
```

至少要固定：

```text
branch_from_state_id
branch_from_event_id
context_hash
world_snapshot_id
memory_snapshot_id
```

否则所谓 same-state comparison 可能偷偷混入：

```text
不同 context
不同 memory
不同 environment snapshot
```

此时 outcome 差异就不能再归因给当前 action。

这与第 4 / 8 章的 same-prefix / same-state discipline 完全一致。

---

# 12.11 Retry 与 Backtracking 是两种不同事件

Retry：

```text
同一个 logical action 再尝试一次
```

Backtracking：

```text
返回更早 decision state，改选另一条路径
```

因此 Retry 建议记录：

```text
logical_action_id
attempt_id
retry_of_attempt_id
retry_reason
```

Backtracking 建议记录：

```text
backtrack_from_event_id
backtrack_to_state_id
invalidated_event_ids
replacement_branch_id
```

需要特别注意：**Production System 的 infrastructure retry 与 Agent policy 的 recovery 不是同一件事**。前者见第 22 章，后者才应该进入 Agent behavior trajectory。

---

# 12.12 Loop 不能只靠“重复次数”判断

重复行为可能是：

```text
合法分页
polling
对多个对象逐个处理
合理 retry
```

也可能是：

```text
dead loop
same tool + same args + same observation
planning stuck
```

所以 Loop Detection 更适合检查：

```text
Action Similarity
Observation Similarity
State Progress
Goal Progress
Retry Semantics
```

一个较强信号是：

```text
同一 action signature 重复
+
observation 基本不变
+
goal progress = 0
```

而不是机械设置“超过三次就是 loop”。

---

# 12.13 Memory 必须进入事件流

至少支持：

```text
MEMORY_READ
MEMORY_WRITE
MEMORY_UPDATE
MEMORY_DELETE
```

并记录：

```text
memory_id
scope
source
version
visibility
retention_scope
```

否则：

```text
Agent 为什么知道这个用户偏好？
为什么下一次 episode 还记得上次结果？
```

都无法解释。

Benchmark 中尤其要记录：

```text
memory reset policy
cross-episode persistence policy
```

否则可能出现 cross-episode contamination。

---

# 12.14 Hidden Reasoning 不是 Trajectory Audit 的必要前提

Agent 数据不应该依赖“保存完整内部思维”才能分析。

更稳的 evidence 是：

```text
observable message
structured plan
selected action
tool result
memory operation
state transition
verification result
```

因此：

> **Trajectory audit 建立在可观察行为和可复现状态证据上，而不是假设自然语言 CoT 等于模型真实内部计算。**

Reasoning state supervision 的边界见第 4 章。

---

# 12.15 Agent-visible Trace 与 Researcher-visible Trace 必须分开

### Agent-visible Trace

在线模型真正可访问：

```text
User messages
System / Developer instructions
Tool schemas
Visible observations
Allowed memory
```

### Researcher-visible Trace

离线分析还可以包含：

```text
Hidden Environment State
Gold Outcome
Verifier Output
Failure Attribution
Future Outcome
Counterfactual Labels
```

二者一旦混淆，会产生：

```text
future leakage
label leakage
hidden-state leakage
```

所以建议字段级维护：

```text
visible_to_agent: true / false
```

这是所有在线 / 离线分析的基本边界。

---

# 12.16 State Diff 比 Tool Return 更接近真实执行结果

例如：

```text
refund_order(1847)
→ {"success": true}
```

Tool Return 只说明执行接口返回 success。

真正想确认的是：

```text
Before:
refunded = false

After:
refunded = true
```

因此 write action 最好保存：

```text
pre_state_id
post_state_id
state_diff
```

这让：

```text
Tool Success
```

与：

```text
World / Environment Change
```

能够被区分。

---

# 12.17 Progress 是 trajectory-local 的衍生属性

一个 action 可以完全合法，却不推动任务目标。

因此可以派生：

```text
progress_label
resolved_subgoal
information_gain
constraint_delta
```

但要注意：这些属于**derived annotation**，不是 raw runtime fact。

真正如何把最终 Outcome 归因给中间 decision，见第 13 章。

本章只要求 trajectory representation 足够支持后续计算，而不重新定义 Credit theory。

---

# 12.18 Termination 本身是一类 Event

至少区分：

```text
SUCCESS
VALID_REFUSAL
NEED_USER_INPUT
TIMEOUT
BUDGET_EXHAUSTED
UNRECOVERABLE_ERROR
POLICY_BLOCK
MODEL_STOP
HARNESS_STOP
```

尤其要区分：

```text
Model Stop
```

与：

```text
Harness Stop
```

如果模型本想继续，但 Harness 因 max_steps 强制结束，这不是 premature model termination。

---

# 12.19 Multi-Agent 与 Human-in-the-loop 需要 Actor-level Lineage

Multi-Agent trace 至少记录：

```text
actor_id
role
sender
recipient
action_owner
shared_state_id
private_state_id
handoff_id
```

否则：

```text
Planner 给错计划
Executor 正确执行
```

最终失败时会误罚 Executor。

Human-in-the-loop 则最好区分：

```text
HUMAN_CLARIFICATION
HUMAN_APPROVAL
HUMAN_CORRECTION
HUMAN_OVERRIDE
```

它们代表完全不同的能力需求。

---

# 12.20 Replay：Trajectory 能不能被重新执行？

理想 replay 至少需要：

```text
Task Case
Environment Snapshot
Runtime Versions
Action Sequence
```

Replay 可分：

```text
Exact Replay
同样输入产生字节级一致结果

Semantic Replay
结果不必字节一致，但关键状态与语义等价
```

如果 replay 失败，可能说明：

```text
环境 drift
Tool version changed
外部 API 变化
时间依赖
Snapshot 不完整
```

注意：Replay 的系统级治理和历史版本管理见第 19 章；这里关注的是一条 trajectory 是否包含足够本地证据支持 replay。

---

# 12.21 Raw Trace 是 Data Asset，SFT / Preference / Eval 只是 View

同一条 Raw Trajectory 可以派生：

```text
SFT Demonstration
Tool Selection Data
Argument Data
Observation Grounding Data
Preference Pair
Recovery Data
Failure Classification
Regression Case
Benchmark Episode
```

因此推荐：

```text
Raw Trace
↓
Normalized Events
↓
Annotated Trajectory
↓
Derived Views
```

而不是：

```text
Runtime Log
↓
直接压成某个训练 JSON
↓
删除原始证据
```

System-wide Dataset View、versioning 和 lineage 管理见第 19 章。

---

# 12.22 Trajectory Quality 是多维的，但本章不负责最终评分

至少可以从这些维度观察：

```text
Outcome
Decision Quality
Execution Quality
Grounding
Safety / Side Effect
Efficiency
Auditability
```

但“最终怎样给 reward / credit”属于第 13 章；“怎样定义 failure”属于第 14 章；“谁来判”属于第 15 章；“怎样比较系统”属于第 16 章。

本章的职责是保证：

> **这些后续判断需要的执行证据都被 trajectory 正确表示。**

---

# 12.23 Canonical Case C1：订单退款 Agent

任务：

> **如果订单 1847 还没发货，并且金额不超过 100 元，就退款；否则不要动。**

一个完整 trajectory 可以表示为：

```text
E0 USER_MESSAGE
↓
E1 TOOL_CALL get_order(1847)
↓
E2 TOOL_RESULT status=pending, amount=79
↓
E3 DECISION eligible=true
↓
E4 TOOL_CALL refund_order(1847)
↓
E5 TOOL_RESULT success
↓
E6 TOOL_CALL get_order(1847)
↓
E7 TOOL_RESULT refunded=true
↓
E8 FINAL_RESPONSE
↓
E9 TERMINATION SUCCESS
```

其中真正值得保存的是：

```text
E4.branch_from_state_id
E4.visible_context
E4.logical_action_id
E5.call_id
Pre-state / Post-state
State Diff
Runtime Versions
Final Verification Reference
```

如果失败版本是：

```text
get_order(1847)
→ pending, 79
refund_order(1848)
→ success
```

Tool Return 依旧可能是 success，但 trajectory evidence 会暴露：

```text
entity binding changed
wrong target action
forbidden side effect
目标订单未退款
```

这说明为什么执行轨迹不能被压成：

```text
Tool Success = true
```

---

# 12.24 一个推荐的 Trajectory Dataset Contract

至少能够回答：

```text
Identity
这是谁的一次运行？

Visibility
Agent 当时到底看到了什么？

Decision
它决定了什么？

Execution
真正发生了什么动作？

Observation
环境返回了什么？

State Transition
世界怎样变化？

Lineage
它是从哪里分支 / retry / backtrack 来的？

Runtime
哪版 Model / Tool / Harness / Environment？

Termination
为什么结束？

Evidence
以后怎样验证与回放？
```

---

# 12.25 常见失败模式

1. **把 trajectory 当聊天记录。** Event / state / lineage 全丢。
2. **只保存最终训练格式。** 后续无法重新标注和派生。
3. **不记录 Agent-visible Context。** 无法判断信息是否真的可用。
4. **World State 与 Agent-visible State 混用。** 产生 hidden-state leakage。
5. **Decision 与 Executed Action 混用。** 无法发现 plan-action inconsistency。
6. **Branch 没有 authoritative state ID。** same-state 比较不成立。
7. **Retry 没有 logical action lineage。** 系统重试与 Agent recovery 混在一起。
8. **Backtracking 被压成线性文本。** 恢复逻辑丢失。
9. **并行动作强行线性化。** 制造假的因果顺序。
10. **Memory 不入 trace。** 行为看起来像凭空知道。
11. **Context truncation 不记录。** Harness 问题被误归因模型。
12. **只保存 Tool Return，不保存 State Diff。** 无法确认写操作真实生效。
13. **Termination 只有 boolean。** 不知道谁、为什么停止。
14. **Researcher-only label 混入 Agent Context。** 产生 future leakage。
15. **Trajectory-local lineage 和 system-wide governance 混成一套。** 职责不清且难维护。

---

# 12.26 从数据岗位视角，本章实际在做什么？

典型工作包括：

```text
设计 trajectory schema
定义 event taxonomy
统一不同模型 / 工具 API trace
保存 authoritative state / state diff
记录 context construction
记录 memory read/write
设计 branch / retry / backtrack lineage
做 multi-agent actor lineage
区分 Agent-visible / Researcher-visible view
构建 replay-ready trace
从 raw trace 派生 SFT / Preference / Eval views
```

真正成熟的 Agent Data 工作不是：

> “把日志收集下来。”

而是：

> **把一次执行过程保存成可以被重放、比较、归因和重新派生监督信号的经验资产。**

---

# 12.27 面试 / 自检问题

1. 为什么 Agent trajectory 不能只保存成 messages？
2. World State、Environment State、Agent-visible State 有什么区别？
3. State 与 Context 为什么不是同一个概念？
4. Decision Intent 与 Executed Action 为什么必须分开？
5. Observation 为什么不等于 Tool Result？
6. 为什么要区分 `observation_received / parsed / used`？
7. Trajectory segmentation 有哪些常用粒度？
8. 什么情况下 trajectory 应该建成 Graph？
9. same-state candidate 为什么需要 authoritative state ID？
10. Retry 和 Backtracking 有什么区别？
11. 为什么 Memory read/write 必须进入 trace？
12. Context truncation 会怎样污染 failure attribution？
13. Agent-visible Trace 和 Researcher-visible Trace 为什么必须分开？
14. 为什么 State Diff 比单独 Tool Success 更可靠？
15. Model Stop 与 Harness Stop 怎么区分？
16. Multi-Agent 为什么需要 actor-level lineage？
17. Replay 需要哪些最小信息？
18. Raw Trace 为什么应该长期保留？
19. 一条 Raw Trace 可以派生成哪些 Data View？
20. Trajectory-local lineage 与 system-wide provenance 有什么区别？

---

# 12.28 本章最终心智模型

把本章压成一条链：

```text
Task Case
↓
Authoritative Environment State
↓
Agent-visible Context
↓
Decision Intent
↓
Executed Action
↓
Environment Transition
↓
Observation
↓
State / Context Update
↓
Next Decision
↓
Termination
```

在这条主链之外，还必须保留：

```text
Branch Lineage
Retry Lineage
Backtrack Lineage
Memory Lineage
Runtime References
Visibility Boundary
State Diff
```

这样，一条 trajectory 才真正从：

```text
“一段日志”
```

升级成：

```text
“可重放的经验对象”
```

本章到此只解决**怎么把行为过程记录清楚**。

下一章第 13 章继续回答：

> **记录清楚以后，最终 Outcome 到底该怎样归因给中间 Decision？**

也就是从 Representation 正式进入 Credit Assignment。