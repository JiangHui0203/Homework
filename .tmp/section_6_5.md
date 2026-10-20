### 6.5 Shared / Private Context

如果说 6.4 Communication 解决的是：

> **一个 Agent 怎样把信息可靠地传给另一个 Agent？**

那么 6.5 Shared / Private Context 解决的是另一个更基础的问题：

> **在多个 Agent 同时参与同一个系统时，哪些信息应该被共同看见、共同依赖、共同更新，哪些信息应该只属于某个 Agent、某个角色、某个任务阶段或某个执行边界？**

因此，本节讨论的不是简单的：

```text
shared prompt
vs
private prompt
```

而是一套完整的 **Information Visibility、State Authority、Synchronization 与 Isolation Architecture**。

先记住本节最重要的定义：

> **Shared / Private Context 是多 Agent 系统的信息可见性与同步架构：它决定哪些信息对哪些 Agent 可见、谁可以读、谁可以写、谁拥有权威解释权、信息怎样同步、何时失效，以及局部 Context 如何在不破坏全局一致性的前提下保持自治。**

可以用一条总链表示：

```text
Environment / Tools / Users
        ↓
Observations
        ↓
Canonical / Shared State
        ↓ permission / role / task / freshness / trust
Per-agent Context Projection
        ↓
Agent_i Context
   ├── Shared View
   └── Private / Local Context
        ↓
Decision_i
        ↓
Proposed Update / Action / Artifact
        ↓
Validation / Ownership / Merge
        ↓
Canonical Shared State
```

因此：

> **Communication changes who receives information; Context Architecture determines who can see, trust, modify and depend on information.**

---

#### 6.5.1 Shared Context 到底是什么？

在本文中，**Shared Context** 指：

> **在某个 Task / Session / Collaboration Scope 内，被两个或多个 Agent 的当前决策过程共同可见、可引用或共同依赖的信息视图。**

例如一个软件修复任务中，三个 Agent 都可能需要看到：

```text
Task Goal
Public API Constraint
Current Branch / Commit
Issue Description
Verified Test Result
Canonical Decision Log
```

这些信息可以进入它们各自的 Shared Context Projection。

注意关键词是：

```text
共同可见 / 共同依赖
```

而不是：

```text
所有 Agent 看完全相同的 Prompt
```

---

#### 6.5.2 Private Context 到底是什么？

**Private Context** 指：

> **只对某个 Agent、角色、子任务或局部执行边界可见，并且不默认传播给其他 Agent 的模型可见信息。**

例如 Research Agent 的 Private Context 可以包括：

```text
当前搜索候选
局部检索 Query
临时 Hypothesis
尚未验证的 Source
局部工作计划
当前 Tool Observation
```

Verifier Agent 不一定需要看到这些内容。

它只需要：

```text
Claim
Evidence
Source
Verification Target
Relevant Constraints
```

这就是：

> **Private by default, share by decision need.**

---

#### 6.5.3 Private Context ≠ Secret

必须立即拆开一个容易混淆的概念：

```text
Private Context
≠
Secret
```

Private 表示：

```text
当前不应该被其他 Agent 默认看到
```

Secret 表示：

```text
高敏感 credential / protected data，不应该进入普通模型 Context
```

例如：

```text
Research Agent 的未验证假设
```

可以是 Private Context，但不是 Secret。

而：

```text
API key
OAuth token
private key
password
```

不应该简单归类为“某 Agent 的 Private Context”，而应由 Runtime / Credential Store 保管，只在可信执行边界使用。

所以：

> **Private ≠ Secret；Secret 通常应该在模型 Context 之外。**

---

#### 6.5.4 Shared Context ≠ Shared State

这是本节最重要的边界之一。

```text
Shared Context
= 多个 Agent 当前 inference 可以看到什么

Shared State
= 系统显式维护、多个 Agent 共同依赖的当前任务状态
```

例如：

```text
Shared State:
latest_test_status = passed
branch_head = abc123
```

Agent A 当前需要修改代码，因此 Context 中包含这些字段。

Agent B 正在做与 branch 无关的文档审查，可能不需要看到它们。

因此：

```text
Shared State
↓ per-agent projection
Shared Context_A
Shared Context_B
```

而不是：

```text
Shared State = broadcast everything to everyone
```

---

#### 6.5.5 Shared Context ≠ Shared Memory

Shared Memory 回答：

> **哪些过去的信息被长期或短期保存，并允许多个 Agent 在未来重新获取？**

Shared Context 回答：

> **当前这一轮，哪些信息真的进入多个 Agent 的模型可见输入？**

所以：

```text
Shared Memory
      ↓ retrieval / selection
Shared Context
```

Memory 中存在：

```text
不代表当前一定可见
```

Context 中可见：

```text
也不代表一定被长期保存
```

---

#### 6.5.6 Shared Context ≠ Communication

6.4 已经建立：

```text
Communication
= information exchange event
```

6.5 关注：

```text
Context Sharing
= information visibility / access model
```

例如：

```text
A sends X to B
```

是 Communication。

而：

```text
A 和 B 都可以从 Shared Workspace 读取 X
```

属于 Shared Context / Shared State 架构。

一句话：

> **Communication 是“信息怎样过去”；Shared Context 是“谁现在能看见什么”。**

---

#### 6.5.7 Shared Context ≠ Global Transcript

最危险的简化之一是：

```text
所有 Agent
→ 全部看到一个 Global Chat Transcript
```

这会把：

```text
共享必要信息
```

错误地实现为：

```text
共享所有历史文本
```

最终产生：

```text
Context Explosion
Stale Information
Role Leakage
Instruction Conflict
Privacy Leakage
Prompt Injection Propagation
Token Cost
```

所以：

> **Shared Context 应是经过策略构造的视图，不是全局 Transcript 的别名。**

---

#### 6.5.8 Shared Context 的真正系统位置

可以把信息分成五层：

```text
1. Environment / Source of Truth
2. Canonical Shared State / Artifact
3. Shared Memory / Event History
4. Per-agent Context Projection
5. Agent-local Private Context
```

它们的关系是：

```text
Environment
   ↓ observe / verify
Canonical Shared State
   ↓ persist / history
Shared Memory / Artifacts
   ↓ select / project
Agent-visible Shared Context
   +
Private Local Context
   ↓
Decision
```

这比“一个共享 Prompt + 几个角色 Prompt”更接近真实系统。

---

#### 6.5.9 Context Sharing 的第一原则：Context 是 Projection

延续 4.1：

> **Context 是模型当前决策所需的信息投影，不是系统全部已知信息。**

在 Multi-Agent 中应进一步写成：

\[
C_i^t = \phi(S_t, M_t, O_i^t, R_i, P_i, G_i^t)
\]

其中：

- \(S_t\)：当前共享 / 权威 State；
- \(M_t\)：可访问 Memory / Artifact；
- \(O_i^t\)：Agent i 当前 Observation；
- \(R_i\)：Role；
- \(P_i\)：Permission / Policy；
- \(G_i^t\)：当前局部 Goal；
- \(C_i^t\)：最终模型可见 Context。

因此不同 Agent 即使服务同一 Global Goal：

```text
C_A ≠ C_B ≠ C_C
```

完全正常。

---

#### 6.5.10 Shared 的正确含义不是“相同”

两个 Agent 可以共享同一个事实：

```text
branch_head = abc123
```

但它们看到的整体 Context 仍不同。

例如：

```text
Coder Context
= branch + failing test + source code

Reviewer Context
= branch + diff + review criteria
```

所以：

> **Shared means overlapping decision-relevant information, not identical context windows.**

---

#### 6.5.11 Visibility 是一个独立的系统维度

一个信息对象不只有：

```text
value
```

还可能有：

```text
owner
scope
visibility
write authority
source
version
freshness
sensitivity
trust
lifecycle
```

因此 Multi-Agent Context 管理不能只做：

```text
list[str]
```

而应该知道：

```text
who may see what under which conditions
```

---

#### 6.5.12 一个完整的 Visibility Pipeline

可以把 Agent 可见信息构造写成：

```text
Global Information Universe
        ↓
Identity / Tenant
        ↓
Role / Task / Session Scope
        ↓
Permission / Sensitivity
        ↓
Trust / Provenance
        ↓
Freshness / Version
        ↓
Decision Relevance
        ↓
Context Budget
        ↓
Minimal Sufficient Visibility
        ↓
Agent-visible Context
```

这与 5.4 Capability Discovery 的思想高度一致：

```text
系统拥有
≠
当前应该暴露
```

---

#### 6.5.13 Available Information ≠ Visible Information

系统可能拥有：

```text
全部用户记录
全部项目文件
全部 Agent 日志
全部 Memory
```

但当前 Agent 可能只需要：

```text
当前 Task
一个 Artifact
两个约束
一个 Verification Result
```

所以：

```text
Available
≠ Visible
```

就像：

```text
Capability Available
≠ Capability Visible
```

一样。

---

#### 6.5.14 Visible ≠ Writable

Agent 看得到某个共享状态：

```text
budget_remaining = 100
```

不代表它可以修改：

```text
budget_remaining = 999999
```

因此必须区分：

```text
Read Scope
Write Scope
```

一个 Agent 可以：

```text
read global budget
```

但只有 Budget Manager / Runtime：

```text
write authoritative budget
```

---

#### 6.5.15 Writable ≠ Canonical

即使 Agent 可以提交更新：

```text
claim_status = verified
```

也不代表它提交的值自动成为 Canonical Truth。

更稳健的结构是：

```text
Agent proposes update
        ↓
Schema / Permission / Evidence Validation
        ↓
Owner / Commit Policy
        ↓
Canonical Shared State
```

所以：

> **Write capability can mean proposal authority, not final truth authority.**

---

#### 6.5.16 Shared ≠ Trusted ≠ Authoritative

这三者必须长期保持严格边界：

```text
Shared
= 多个 Agent 可以看到

Trusted
= 来源具有较高可信度

Authoritative
= 系统在冲突时应以它为准
```

例如：

```text
Research Agent 的假设
```

可以被共享给 Reviewer，
但仍然只是：

```text
shared hypothesis
```

不是：

```text
authoritative fact
```

---

#### 6.5.17 Local ≠ False；Local ≠ True

Private / Local Context 中的内容可能完全正确，也可能错误。

“Local”只是作用域，不是 Truth Label。

因此：

```text
local hypothesis
local observation
local cached state
```

都需要独立的：

```text
source / trust / verification / freshness
```

属性。

---

#### 6.5.18 Canonical Shared State

复杂 Multi-Agent 系统最好存在明确的：

> **Canonical Shared State：多个 Agent 在关键协调决策上共同依赖、并由明确 Authority / Owner 管理的当前任务状态。**

例如：

```text
task_status
current_owner
approved_scope
committed_effects
artifact_versions
verified_claims
remaining_budget
```

这些字段不应该靠：

```text
“谁最后在群聊里说了一句”
```

来决定。

---

#### 6.5.19 Canonical State 与 Model Narrative

模型可能说：

```text
“测试已经全部通过。”
```

但 Shared State 记录：

```text
full_test_status = not_run
```

那么后者应优先。

继续沿用：

> **Fresh runtime evidence > stale model narrative.**

Multi-Agent 不改变这一原则，反而更需要它。

---

#### 6.5.20 Source of Truth 必须按字段定义

不一定所有 Shared State 都由一个组件拥有。

例如：

| 字段 | Source of Truth |
|---|---|
| `task_goal` | User / Task Contract |
| `branch_head` | Git |
| `test_status` | Test Runtime |
| `budget_remaining` | Budget Manager |
| `approval_status` | Approval Service |
| `verified_claim` | Verifier / Evidence Policy |
| `current_owner` | Orchestrator |

这样冲突发生时才能知道：

```text
应该相信谁？
```

---

#### 6.5.21 Shared Context 的常见层级

一个实用的 Context Taxonomy 可以是：

```text
System-global Context
Task-shared Context
Role-shared Context
Team / Subgraph Context
Agent-private Context
Step-local Transient Context
Runtime-only State
```

不是所有系统都需要全部层级，但这个模型能帮助审计：

```text
某条信息到底应该在哪一层？
```

---

#### 6.5.22 System-global Context

真正 System-global 的内容通常应该非常少，例如：

```text
hard safety policy
organization-wide constraints
protocol contract
critical incident stop signal
```

因为：

> **越 global 的信息，传播成本与 blast radius 越大。**

不要把“方便”当成全局共享的理由。

---

#### 6.5.23 Task-shared Context

Task-shared Context 是最常见的共享层：

```text
Goal
Success Criteria
Constraints
Current Task State
Canonical Artifacts
Committed Decisions
```

这些信息支持多个 Agent 围绕同一 Task 协作。

但也应按角色做投影，不一定全部复制。

---

#### 6.5.24 Role-shared Context

例如多个 Reviewer 共享：

```text
review policy
rubric
risk taxonomy
```

多个 Research Worker 共享：

```text
source criteria
research question
citation policy
```

而不同角色之间不必自动共享全部工作细节。

---

#### 6.5.25 Agent-private Context

Agent-private Context 常包括：

```text
local plan
local retrieval state
temporary candidate set
working notes
unverified hypothesis
recent local observations
```

它的价值包括：

```text
Isolation
Lower Noise
Lower Leakage
Independent Verification
Reduced Correlated Error
```

---

#### 6.5.26 Step-local Transient Context

某些信息只对一次 Decision 有用：

```text
当前 Tool 返回的大块日志
当前网页片段
当前候选打分
```

使用后可以：

```text
extract durable fact
store artifact reference
then discard raw transient context
```

不需要升级成长期 Shared Context。

---

#### 6.5.27 Runtime-only State

还有一些信息系统必须知道，但模型不需要看到：

```text
credential_ref
queue lease
worker pid
sandbox token
network routing metadata
secret handle
```

所以：

```text
System-visible State
≠ Model-visible Context
```

这条边界在 Multi-Agent 中尤其重要。

---

#### 6.5.28 最小充分可见性：Minimal Sufficient Visibility

本节加入一个新的最小充分原则：

> **Minimal Sufficient Visibility：只让一个 Agent 看见完成当前正确决策所需的最少信息集合。**

它连接已有原则：

```text
Minimal Sufficient Context
Minimal Sufficient Effect
Minimal Durable State
Minimal Sufficient Retrieval
Minimal Sufficient Communication
Minimal Sufficient Visibility
```

这些原则共同强调：

```text
more is not automatically better
```

---

#### 6.5.29 Minimal Sufficient Visibility 不等于信息越少越好

如果删得太狠：

```text
Goal missing
Constraint missing
Evidence missing
State missing
```

Agent 会做错。

因此目标不是：

```text
minimize tokens
```

而是：

```text
minimize unnecessary exposure
subject to correct decision
```

---

#### 6.5.30 Visibility 的 Utility Trade-off

可以概念化：

\[
U(V)=Q(V)-C_{token}(V)-C_{privacy}(V)-C_{attack}(V)-C_{conflict}(V)
\]

其中：

- \(Q(V)\)：信息带来的决策质量；
- \(C_{token}\)：Context 成本；
- \(C_{privacy}\)：隐私暴露；
- \(C_{attack}\)：攻击面；
- \(C_{conflict}\)：过多信息导致的冲突 / 稀释。

所以 Visibility 也是需要优化的 Policy。

---

#### 6.5.31 Global Consistency vs Local Autonomy

Shared / Private Context 最核心的系统张力之一是：

```text
Global Consistency
vs
Local Autonomy
```

全局一致太强：

```text
每个局部更新都同步所有 Agent
```

会造成：

```text
latency
coordination overhead
context churn
```

局部自治太强：

```text
每个 Agent 自己相信自己的世界
```

又会造成：

```text
state divergence
conflicting actions
stale decisions
```

---

#### 6.5.32 Strong Consistency 不应成为默认追求

很多 Multi-Agent 任务不需要每一秒所有 Agent 看到完全相同状态。

例如 Research Worker A 与 B 独立搜索时：

```text
local candidate sources
```

不必实时同步。

只有当：

```text
某条证据被验证并成为共享决策依据
```

才需要 Commit 到 Shared State。

所以：

> **Global consistency is a selective guarantee, not a universal default.**

---

#### 6.5.33 Local Autonomy ≠ Local Truth

允许 Agent 在局部 Context 中自由探索，不代表它的局部发现自动成为系统事实。

可以采用：

```text
Local Work
↓
Proposed Commit
↓
Validation / Review
↓
Shared Canonical State
```

这和 Git Branch → Review → Merge 的思想非常接近。

---

#### 6.5.34 Branch-and-Merge Context Pattern

多个 Agent 可以基于同一个 Shared Snapshot 工作：

```text
Shared State v10
├── Agent A Local Branch
├── Agent B Local Branch
└── Agent C Local Branch
```

完成后提交：

```text
Patch / Evidence / Artifact
```

再经过：

```text
merge policy
conflict check
verification
```

更新：

```text
Shared State v11
```

这比多个 Agent 直接随意改同一共享字典更稳健。

---

#### 6.5.35 Snapshot + Delta

跨 Agent 协作中，一个非常实用的结构是：

```text
Shared Snapshot
+
Local Delta
```

Agent 不必每步复制全局 State，只需要记录：

```text
基于哪个版本
我新增 / 修改了什么
```

例如：

```text
base_version = 42
patch = {verified_sources += S17}
```

---

#### 6.5.36 Version 是同步语义的基础

如果 Agent A 基于：

```text
state_version = 41
```

提交 patch，
但 Shared State 已经是：

```text
version = 44
```

系统应该检测：

```text
stale write
```

而不是静默覆盖。

---

#### 6.5.37 Optimistic Concurrency

典型流程：

```text
read v10
↓
local work
↓
commit if current_version == v10
```

如果不等：

```text
conflict
→ refresh / merge / re-evaluate
```

这种模式特别适合多个 Agent 并行写 Shared State。

---

#### 6.5.38 Lost Update

典型问题：

```text
State v10
├── A adds evidence X
└── B adds evidence Y
```

如果：

```text
A writes whole state
B writes whole state later
```

可能变成：

```text
Y exists
X lost
```

所以 Shared State Mutation 需要：

```text
version + patch + merge semantics
```

而不是 last-write-wins 默认。

---

#### 6.5.39 Last-write-wins 不适合所有字段

对于：

```text
latest_page
```

可能可以。

对于：

```text
executed_effects
verified_evidence
spent_budget
```

就非常危险。

字段需要知道自己的语义类型：

```text
scalar
set
append-only ledger
counter
exclusive choice
state-machine value
```

---

#### 6.5.40 Monotonic Shared State

有些 Shared State 最适合设计成单调增长：

```text
committed_effect_ledger
verified_evidence_set
spent_cost
completed_milestones
```

一旦真实发生，不应该因为某个 Agent 重写 Context 就消失。

这种设计能降低 Multi-Agent 覆盖式幻觉。

---

#### 6.5.41 Shared Blackboard Pattern

Blackboard 可以存：

```text
Tasks
Facts
Claims
Evidence
Artifacts
Hypotheses
Status
Locks
```

Agent 通过共享空间协作：

```text
A writes finding
B reads finding
C verifies finding
```

优点：

```text
loose coupling
shared visibility
asynchronous collaboration
```

风险：

```text
pollution
stale entries
write conflict
authority ambiguity
```

---

#### 6.5.42 Blackboard 不能只是一块“大家随便写”的文本区

成熟 Blackboard 至少需要：

```text
item_id
type
owner
source
version
status
created_at
updated_at
trust / verification
scope
```

否则很快退化为：

```text
Shared Transcript with extra steps
```

---

#### 6.5.43 Artifact-centered Collaboration

对于大型结果：

```text
report.md
analysis.csv
patch.diff
test_results.json
sources.json
```

更稳健的是：

```text
Artifact Store
+
Shared Metadata / References
```

而不是把全部 Artifact 复制进所有 Agent Context。

这延续：

> **Shared Artifact often beats Shared Transcript.**

---

#### 6.5.44 Artifact Ownership

每个共享 Artifact 最好知道：

```text
owner
version
writers
readers
canonical path / id
validation state
```

否则可能出现：

```text
A 修改 draft_v1
B 修改 draft_v1
C 不知道哪个是 canonical
```

---

#### 6.5.45 Decision Log

有些内容值得全局共享，但不适合塞进 Current State。

例如：

```text
为什么选择方案 A？
为什么拒绝方案 B？
哪个约束导致重新规划？
```

可以进入：

```text
Decision Log
```

当前 Context 按需检索，而不是永久重放全部历史。

---

#### 6.5.46 Event Log 与 Current Shared State

继续沿用 4.2：

```text
Event Log
= 发生过什么

Current State
= 现在什么成立
```

Multi-Agent 中尤其不应把：

```text
一堆事件
```

直接当：

```text
当前事实
```

---

#### 6.5.47 Shared Context 的 Freshness

一个 Context Item 必须考虑：

```text
observed_at
source_version
state_version
valid_until
```

例如：

```text
Agent A 10:00 看到库存 3 件
Agent B 10:20 执行购买
```

如果没有重新验证，Shared Context 只是旧快照。

---

#### 6.5.48 Synchronized ≠ Consistent

系统可以成功把一条消息同步到所有 Agent：

```text
sync success
```

但如果同步的是错误值：

```text
all agents consistently wrong
```

所以：

```text
Synchronization
≠ Truth
≠ Semantic Consistency
```

---

#### 6.5.49 Consistent ≠ Fresh

所有 Agent 都看到：

```text
branch_head = abc
```

可以完全一致。

但真实 Git 已经是：

```text
branch_head = def
```

所以仍然是 stale。

这说明 Context 正确性至少要分：

```text
Agreement
Freshness
Authority
Truth / Verification
```

---

#### 6.5.50 State Reconciliation

当 Local Context 与 Canonical State 不一致：

```text
Local v17
Shared v20
```

不能盲目继续。

可以：

```text
refresh
rebase local work
merge
invalidate stale assumption
replan
```

这就是 Multi-Agent 版 State–Environment Reconciliation。

---

#### 6.5.51 Shared Context 的 Conflict Resolution

冲突可以来自：

```text
A says X
B says not X
```

也可以来自：

```text
A and B edit same field
```

处理原则通常依据：

```text
source authority
version
freshness
verification
field ownership
business semantics
```

而不是：

```text
哪个 Agent 更自信
```

---

#### 6.5.52 Canonical Owner

关键共享对象最好有 canonical owner：

```text
Task ownership → Orchestrator
Test truth → Test Runtime
Payment truth → Payment Provider
Policy truth → Policy Store
Artifact truth → Repository / Artifact Store
```

Owner 不一定是唯一 reader，而是：

> **冲突时谁拥有最终写入 / 解释权。**

---

#### 6.5.53 Multi-writer Shared State 要非常谨慎

如果所有 Agent 都能：

```text
read all
write all
```

系统会很快遇到：

```text
race
semantic conflict
poisoning
untraceable mutation
```

更合理：

```text
scoped write
owner-specific fields
proposal + commit
append-only event
```

---

#### 6.5.54 Role-scoped Write Authority

例如：

```text
Researcher
→ may propose evidence

Verifier
→ may set verification_status

Executor
→ may append effect receipt

Budget Manager
→ may update budget
```

这比：

```text
everyone edits global_state.json
```

可靠得多。

---

#### 6.5.55 Private Context 与 Independent Verification

Verifier 如果完整看到 Producer 的：

```text
reasoning trace
confidence
self-justification
```

可能产生 anchoring / confirmation。

更合理的是提供：

```text
Claim
Artifact
Evidence
Evaluation Criteria
```

而不是完整上游过程。

所以 Private Context 还可以服务：

> **Independence by information separation.**

---

#### 6.5.56 不应要求共享隐藏 Chain-of-Thought

多 Agent 协作真正需要共享的是：

```text
Decision
Evidence
Constraint
Uncertainty
Artifact
Commitment
State Delta
```

而不是要求暴露模型内部完整推理过程。

工程上应优先设计：

```text
structured rationale / evidence / verification record
```

而不是依赖 hidden reasoning trace 作为系统接口。

---

#### 6.5.57 Share Commitments, Not Raw Process

一个非常实用的原则：

> **共享对下游决策有约束力的 Commitments 与 Evidence，而不是把整个局部工作过程广播出去。**

例如 Researcher 最终共享：

```text
Claim C17
Evidence S3, S8
Confidence = medium
Open conflict = S12
```

而不是：

```text
40 次搜索 Query + 全部思考草稿
```

---

#### 6.5.58 Handoff 中的 Private → Shared Promotion

Agent A 的某条 Local Observation：

```text
可能需要传给 B
```

这不是简单 copy。

更完整流程：

```text
Private Finding
↓ classify
Fact / Hypothesis / Evidence / Recommendation
↓ attach provenance / freshness
↓ validate sensitivity / authority
↓ promote to shared handoff item
```

即：

> **Private-to-Shared 是一种受控 Promotion。**

---

#### 6.5.59 Shared → Private Projection

反过来 Shared State 进入某个 Agent Context 时，也不是全量 dump：

```text
Canonical Shared State
↓ role / task / permission / relevance
Private Decision View
```

因此信息流是双向治理：

```text
local → shared: promotion
shared → local: projection
```

---

#### 6.5.60 Context Leakage

最典型风险是：

```text
Agent A 本不该看到的信息
因共享 Context 错误进入了 A 的 Prompt
```

可能包括：

```text
其他用户数据
其他 tenant 数据
内部审批信息
私有文档
敏感用户信息
系统内部策略细节
```

一旦进入模型 Context：

```text
“要求模型不要使用”
```

已经不是理想的第一道防线。

---

#### 6.5.61 Permission 应在 Context 构建前执行

更稳健：

```text
Information Universe
↓ Permission Filter
Allowed Candidate Information
↓ Context Selection
Model Context
```

而不是：

```text
全部放进去
↓
Prompt: 请不要看不该看的内容
```

所以：

> **Unauthorized information should ideally never enter model-visible context.**

---

#### 6.5.62 Cross-tenant Leakage

Multi-tenant Agent 最危险的错误之一：

```text
Tenant A 的 Memory / Artifact / Shared State
被 Tenant B 的 Agent 检索到
```

因此任何：

```text
cache
index
shared store
blackboard
artifact registry
```

都必须包含 scope / tenant boundary。

---

#### 6.5.63 Cache 也是 Shared Context 风险源

错误 Cache Key：

```text
key = query
```

正确至少可能需要：

```text
key = tenant + user + permission_scope + source_version + query
```

否则 Shared Cache 会偷偷变成跨 Context 泄漏通道。

---

#### 6.5.64 Prompt Injection 的跨 Agent 传播

典型链路：

```text
Malicious Web Content
↓
Research Agent Private Context
↓ bad promotion
Shared Blackboard
↓
Executor Agent Context
↓
High-privilege Action
```

攻击者只需要污染低权限 Agent 的输入，就可能沿 Shared Context 传播到高权限 Agent。

---

#### 6.5.65 Trust 标签必须随信息传播

如果一条信息来自：

```text
untrusted_web
```

经过 Research Agent Summary 后，不应该自动变成：

```text
trusted_internal_fact
```

应该保留：

```text
origin
transformation lineage
verification status
```

这叫：

> **Trust should propagate conservatively.**

---

#### 6.5.66 Derived Context 需要 Lineage

例如：

```text
Raw Source
↓ extraction
Claim
↓ summary
Shared Note
```

Shared Note 应能追到：

```text
source artifact
source range
transformer / agent
version
```

否则派生信息很容易与原始 Evidence 断开。

---

#### 6.5.67 Context Poisoning

一条错误信息进入 Shared State 后，比单 Agent Context Error 更危险：

```text
Wrong Fact
↓ Shared Store
A retrieves
B retrieves
C retrieves
↓
Correlated Failure
```

这是一种：

> **Error Amplification by Shared Context.**

---

#### 6.5.68 Authority Inversion

危险情况：

```text
Low-trust Agent 的自然语言总结
覆盖了 High-authority Runtime Fact
```

例如：

```text
Agent says: payment failed
Provider says: payment completed
```

如果 Shared State 最后采用 Agent Narrative，就是 Authority Inversion。

---

#### 6.5.69 Shared Hypothesis 必须标记为 Hypothesis

研究 / Debug 场景允许共享：

```text
hypothesis
```

但必须保持类型：

```text
HYPOTHESIS
not FACT
```

否则下游 Agent 很容易发生：

```text
repetition → perceived truth
```

---

#### 6.5.70 Consensus Amplification

多个 Agent 都读取同一错误 Shared Fact 后：

```text
A agrees
B agrees
C agrees
```

并不能形成三份独立证据。

实际上可能只有：

```text
one poisoned source
```

因此：

> **Shared Context 会降低信息独立性；Consensus Eval 必须看 provenance diversity。**

---

#### 6.5.71 Context Explosion

如果每个 Agent 都把自己的 Local Context 持续 Promotion 到 Shared：

```text
Shared Context_t
= all local histories
```

最终会：

```text
Token Cost ↑
Noise ↑
Conflict ↑
Freshness ↓
Security Surface ↑
```

所以 Shared Context 同样需要 Compaction / Selection。

---

#### 6.5.72 Shared Context Compaction

可以周期性把：

```text
many raw updates
```

压成：

```text
Canonical State
Verified Decisions
Open Questions
Artifact References
Recent Critical Events
```

但必须保留：

```text
provenance
versions
critical literals
```

---

#### 6.5.73 Context Garbage Collection

过期共享内容应：

```text
expire
supersede
archive
```

而不是永远留在 Active Shared Context。

典型对象：

```text
old plan
resolved hypothesis
obsolete candidate
stale availability
superseded branch
completed transient subtask
```

---

#### 6.5.74 Supersession

旧信息不一定需要物理删除。

可以记录：

```text
item v2
supersedes item v1
```

这样：

```text
current view 清晰
history / audit 仍保留
```

---

#### 6.5.75 Shared Context 与 Budget

共享也有 Budget：

```text
shared context tokens
synchronization messages
retrieval cost
serialization
storage
model attention
```

所以应该问：

```text
这条信息被 N 个 Agent 都看见，真的值得吗？
```

---

#### 6.5.76 Fan-out Cost

一条 5k-token 信息：

```text
复制给 10 个 Agent
```

可能产生：

```text
≈ 50k input tokens
```

还不算下游模型对它的处理成本。

因此 Shared Context 的成本会随 Agent Count 放大。

---

#### 6.5.77 Lazy Materialization

对于大共享对象，可以只共享：

```text
artifact_id
summary
metadata
version
```

需要时 Agent 再：

```text
read / retrieve selected range
```

这是一种：

> **Lazy Context Materialization。**

---

#### 6.5.78 Role-specific Projection

同一个 Artifact：

```text
production incident report
```

不同角色可以看到不同投影：

```text
Engineer → logs + stack trace
Manager → impact + status
Security → indicators + access trace
```

不是复制三个不同 Truth，而是：

```text
same authoritative source
→ different decision views
```

---

#### 6.5.79 Need-to-know Context

权限控制不仅问：

```text
“这个 Agent 能不能看？”
```

还应该问：

```text
“当前这一步需要看吗？”
```

这就是：

```text
Permission
+
Decision Need
```

共同决定 Visibility。

---

#### 6.5.80 Context Ownership

Context 本身可以是动态构造的，不一定需要“owner”。

但 Context 来源对象通常需要 Owner：

```text
State owner
Artifact owner
Memory owner
Policy owner
```

这样才能知道：

```text
谁负责更新？
谁负责修正？
谁负责失效？
```

---

#### 6.5.81 Context Builder 是 Harness Policy

Per-agent Context 通常由 Harness 执行：

```text
Global State
Shared Memory
Local State
Permissions
Role
Current Goal
↓
Context Policy
↓
Agent Context
```

所以：

```text
Shared / Private Context
= information architecture concept

Harness Context Policy
= operational implementation
```

---

#### 6.5.82 Runtime 的职责

Runtime 更负责：

```text
state store
artifact store
credential isolation
session
checkpoint
message queue
transaction / lock
```

它提供 Shared / Private Context 所依赖的真实隔离和同步基础设施。

因此：

```text
Prompt says private
≠
Runtime guarantees isolation
```

---

#### 6.5.83 Prompt-level Role Separation 不等于 Context Isolation

如果两个 Agent：

```text
system prompt 不同
```

但仍然共享：

```text
same full transcript
same credentials
same memory
same filesystem
```

那么真实隔离非常有限。

安全隔离需要至少考虑：

```text
Context
Memory
Tools
Credentials
Sandbox
Artifacts
Network
```

---

#### 6.5.84 Shared Context 与 Credential Boundary

不要通过 Shared Context 传播：

```text
API key
access token
session secret
private key
```

正确结构是：

```text
Context:
credential_ref = payment_exec_role

Runtime:
resolve credential under policy
```

即：

> **Agent can know a capability exists without seeing its credential.**

---

#### 6.5.85 Context Policy 与 Least Privilege

Least Privilege 不只是：

```text
少给 Tool 权限
```

还包括：

```text
少给不必要的信息权限
```

可以称为：

> **Least-context / Need-to-know Information Policy。**

---

#### 6.5.86 Shared Context Failure Localization

当 Multi-Agent 因“信息不同步”失败时，可以按顺序检查：

```text
1. 需要的信息是否真实存在？
2. Canonical Source / Owner 是谁？
3. 最新值是否进入 Shared State？
4. Update 是否通过 Validation / Commit？
5. Shared State Version 是否正确？
6. Context Projection 是否选中了它？
7. Receiver 是否有权限看到？
8. 信息是否 Fresh / Trusted？
9. 表达是否保持了语义 / provenance？
10. Receiver 是否正确消费？
11. Local State 是否成功更新？
12. 后续 Action 是否基于正确版本执行？
```

不要一看到失败就：

```text
调 Prompt
```

---

#### 6.5.87 Failure Mode：Stale Projection

Shared State 已经更新：

```text
v21
```

Agent Context 仍然是：

```text
v18
```

这就是：

```text
Shared-State → Context Projection lag
```

可能导致：

```text
重复工作
错误修改
错误执行
```

---

#### 6.5.88 Failure Mode：Under-sharing

Context 隔离过头：

```text
Agent 没拿到必要 Goal / Constraint / Evidence
```

结果：

```text
local task 看似完成
global task 失败
```

所以 Private-by-default 必须配合：

```text
explicit handoff / projection contract
```

---

#### 6.5.89 Failure Mode：Over-sharing

为了避免遗漏，直接：

```text
all agents see all data
```

会造成：

```text
noise
cost
privacy risk
attack propagation
correlated reasoning
```

这是最常见的反模式之一。

---

#### 6.5.90 Failure Mode：Wrong Truth Promotion

Agent 的：

```text
local inference
```

被错误写成：

```text
shared fact
```

这类错误比普通 Hallucination 更危险，因为它会污染多个下游 Agent。

---

#### 6.5.91 Failure Mode：Authority Ambiguity

两个 Agent 都认为自己有权修改：

```text
current_plan
current_owner
approval_status
```

最终出现：

```text
conflicting canonical state
```

根因不是语言能力，而是：

```text
write ownership undefined
```

---

#### 6.5.92 Failure Mode：Hidden Private Dependency

Agent A 的结果依赖一个只存在于 Private Context 的前提：

```text
“用户不接受方案 X”
```

但 Handoff 没传。

Agent B 接手后重新选择 X。

这说明：

> **真正影响下游决策的 private information 必须被显式 promotion。**

---

#### 6.5.93 Failure Mode：Semantic Drift

Shared 字段：

```text
status = done
```

不同 Agent 理解成：

```text
A: local work done
B: verified done
C: global task done
```

Schema 相同，语义不同。

所以 Shared State 需要：

```text
semantic contract
```

---

#### 6.5.94 Failure Mode：Context Broadcast Storm

某个 Agent 每产生小更新就广播：

```text
1 update × N agents × repeated responses
```

很容易形成消息与 Context 放大。

修复方式：

```text
batch
coalesce
event filter
subscription
importance threshold
```

---

#### 6.5.95 Failure Mode：Shared Memory Poisoning

错误 / 恶意信息进入 Shared Memory：

```text
future tasks
future agents
```

都可能再次检索。

所以 Shared Memory Write 比 Private Scratchpad Write 需要更严格的：

```text
provenance
validation
scope
retention
```

---

#### 6.5.96 Failure Mode：Global Consistency Theater

系统宣称：

```text
所有 Agent 状态一致
```

但实际上只是在每次 Prompt 开头复制一份 Summary。

这不等于：

```text
真实共享状态具有一致性保证
```

真正一致性需要：

```text
version
commit
reconciliation
conflict handling
```

---

#### 6.5.97 Failure Mode：Secret-in-Shared-Context

为了方便，系统把：

```text
credential
private token
sensitive identity
```

直接放入共享 Prompt。

这会把一个局部 credential 变成：

```text
N-agent exposure surface
```

应该使用 Runtime Indirection。

---

#### 6.5.98 Failure Mode：Stale Approval Sharing

Agent A 获得：

```text
approval for action X@v1
```

Agent B 看到“approved”后，对：

```text
X@v2
```

继续执行。

这说明 Approval Context 必须绑定：

```text
exact action
scope
version
expiry
```

---

#### 6.5.99 Failure Mode：Private Context Misread as Global Constraint

Agent 某个局部策略：

```text
“我先不看 Source B”
```

被共享后，其他 Agent 当成：

```text
“Source B 禁止使用”
```

这是 Scope / Authority 丢失。

---

#### 6.5.100 Observability：Context Trace

对每个 Agent Step，最好能回答：

```text
Which shared items were visible?
Which private items were visible?
Which items were excluded?
Why?
Which versions?
Which permissions?
Which source / provenance?
```

否则很难判断：

```text
模型没看到
vs
看到了但没用
vs
看到的是旧值
```

---

#### 6.5.101 Context Projection Trace

可以记录：

```text
agent_id
step_id
shared_state_version
included_item_ids
excluded_item_ids
exclusion_reason
private_item_ids
context_hash
token_count
permission_scope
```

这使 Shared / Private Context 成为可审计系统对象。

---

#### 6.5.102 Metric：Necessary Context Coverage

给定当前 Decision 所需的 Gold Information Set：

```text
G
```

实际 Context：

```text
C
```

可以评价：

```text
必要信息是否进入？
```

类似 Context Recall。

如果 Coverage 低，容易 Under-sharing。

---

#### 6.5.103 Metric：Context Exposure Precision

实际暴露的信息中：

```text
多少真的与当前 Decision 有关？
```

Precision 低意味着：

```text
over-sharing
noise
cost
privacy surface
```

因此需要同时看 Coverage 与 Precision。

---

#### 6.5.104 Metric：Unauthorized Exposure Rate

统计：

```text
本不应进入某 Agent Context 的 item
实际被暴露的比例
```

这是 Security / Governance 的核心指标。

---

#### 6.5.105 Metric：Stale Context Rate

统计 Agent Decision 使用：

```text
superseded / expired / version-lagged
```

Shared Item 的比例。

对于动态环境尤其重要。

---

#### 6.5.106 Metric：Cross-Agent Consistency

对必须一致的关键字段：

```text
task owner
committed effect
approved scope
artifact version
```

检查不同 Agent View 是否一致。

注意：

```text
一致率高 ≠ 事实一定对
```

必须同时看 Authority / Freshness。

---

#### 6.5.107 Metric：Private-to-Shared Leak Rate

衡量：

```text
本来只应局部保留的信息
被错误 Promotion 到 Shared Context / Memory 的频率
```

可用于评估：

```text
privacy
isolation
prompt injection containment
```

---

#### 6.5.108 Metric：Lost / Missed Update Rate

Agent 正确产生了应该进入 Shared State 的 Update：

```text
但没有成功 Commit / Propagate
```

这是 Shared-State Pipeline 的关键可靠性指标。

---

#### 6.5.109 Metric：Propagation Latency

对于必须同步的信息：

```text
Canonical State Update
→ Agent-visible Projection
```

之间的时间。

如果太长：

```text
stale decision risk ↑
```

---

#### 6.5.110 Metric：Canonical-source Violation Rate

统计关键字段被：

```text
non-authoritative source
```

覆盖 / 误解释的频率。

这能直接发现 Authority Inversion。

---

#### 6.5.111 Metric：Context-induced Wrong→Right / Right→Wrong

Context Policy 也应该看净收益。

比较：

```text
Private-only / Baseline
vs
Shared-context Policy
```

统计：

```text
Wrong → Right
Right → Wrong
```

最终：

```text
Net Context Benefit
= Rescue - Degradation
```

---

#### 6.5.112 Shared Context Ablation

一个很有价值的实验：

```text
All-shared Transcript
vs
Structured Shared State
vs
Private Context + Explicit Handoff
vs
Role-scoped Shared Projection
```

同时测：

```text
Task Success
Context Tokens
Leakage
Stale-state Error
Coordination Cost
```

---

#### 6.5.113 Oracle Context Projection

研究中可以直接给每个 Agent：

```text
Oracle Minimal Necessary Context
```

如果性能大幅提升：

```text
bottleneck = context selection / propagation
```

而不是 Agent Local Reasoning。

---

#### 6.5.114 Context Isolation Ablation

比较：

```text
Verifier sees producer full process
vs
Verifier sees claim + evidence only
```

可以测：

```text
independence
correlated error
verification accuracy
```

---

#### 6.5.115 Fault Injection

可以主动注入：

```text
stale shared state
lost update
conflicting writes
wrong version
unauthorized item
poisoned shared fact
late propagation
missing handoff field
```

测试系统是否：

```text
detect
contain
reconcile
recover
```

---

#### 6.5.116 Research Multi-Agent 示例

任务：

```text
分析一个新方法与已有工作的关系
```

Shared：

```text
research_question
scope
canonical paper list
verified citations
claim ledger
open conflicts
```

Researcher Private：

```text
raw search candidates
local query history
working hypotheses
rejected paths
```

Reviewer Context：

```text
claim
supporting evidence
source provenance
counter-evidence
verification rubric
```

Reviewer 不需要：

```text
Researcher 的全部搜索聊天历史
```

---

#### 6.5.117 Coding Multi-Agent 示例

结构：

```text
Investigator
Implementer
Verifier
```

Shared State：

```text
issue
base_commit
constraints
current_patch_ref
test_results
```

Investigator Private：

```text
search trail
candidate root causes
```

Implementer Private：

```text
local edit plan
working diff
```

Verifier Private：

```text
independent tests
risk hypotheses
```

只有通过验证的关键状态才 Promotion 到 Shared。

---

#### 6.5.118 Browser / Action Agent 示例

可以拆成：

```text
Navigator
→ sees untrusted page content

Executor
→ sees structured action proposal + validated target
```

不应让 Executor 自动继承：

```text
全部 untrusted web transcript
```

这样 Context Isolation 本身就是 Prompt Injection Containment。

---

#### 6.5.119 Finance Agent 示例

```text
Invoice Reader
Policy Checker
Payment Executor
Auditor
```

Shared：

```text
invoice_id
validated_amount
policy_result
approval_id
payment_state
receipt_ref
```

Private：

```text
OCR raw chunks
policy search trail
local audit notes
```

Secret：

```text
payment credential
```

只存在 Runtime，不进入普通 Context。

---

#### 6.5.120 Long-running Project 示例

长期项目最容易出现：

```text
Shared Context Drift
```

合理结构：

```text
Project State
Decision Log
Artifact Registry
Task Graph
Effect Ledger
```

每个 Agent 只构造当前 Step 的 Context View。

而不是：

```text
把三个月全部聊天记录给每个 Agent
```

---

#### 6.5.121 Resume 时的 Shared / Private Context

Crash 后恢复不能只恢复：

```text
global transcript
```

需要：

```text
Canonical Shared State
Agent-local checkpoints if needed
Artifact versions
Pending updates
Committed effects
Current ownership
```

恢复后还要：

```text
reconcile environment
```

再重新构造 Context。

---

#### 6.5.122 Agent Replacement

如果 Agent A crash，由 Agent A' 接手：

```text
A' 不需要继承 A 的全部 Private Context
```

而应拿到：

```text
Task Contract
Canonical State
Committed Local Results
Required Artifacts
Open Obligations
```

Private Scratchpad 如果没有形成 Commit，不应该被误当成全局事实。

---

#### 6.5.123 Dynamic Agent Discovery 下的 Context Scope

一个运行时新发现的 Agent：

```text
available
```

不代表：

```text
可以读取已有全部 Shared Context
```

接入还需要：

```text
identity
trust
permission
role
scope
```

这和 Capability Discovery 的边界完全一致。

---

#### 6.5.124 Remote Agent 的 Context 更应该最小化

跨组织 / 跨平台 Agent 通信时：

```text
full internal state
```

更不应该直接外发。

应构造：

```text
explicit task input
minimal evidence
artifact references
public / delegated authority
```

6.7 A2A 会进一步讨论 Remote Agent Interoperability。

---

#### 6.5.125 Shared Context 与 A2A

A2A 可以帮助标准化：

```text
Agent identity
Task
Message
Artifact
State
```

但 A2A 不会自动替你决定：

```text
哪些内部 Context 应暴露给 Remote Agent
```

这仍然是 Harness / Security / Data Governance Policy。

---

#### 6.5.126 Shared Context 与 MCP

MCP 更多解决：

```text
Agent / Host
→ Capability / Data / Tool
```

Shared Context 解决：

```text
多 Agent 如何拥有不同信息视图
```

MCP Resource 可以成为 Context 来源，但：

```text
MCP access
≠ all agents should see it
```

---

#### 6.5.127 Shared Context 与 Retrieval

共享信息很多时，不应全量加载。

可以：

```text
Shared Memory / Artifacts
↓ Retrieval
Relevant Candidates
↓ Role / Permission / Freshness Filter
Shared Context Projection
```

因此 Multi-Agent Context 同样依赖 Retrieval。

---

#### 6.5.128 Shared Context 与 Persistence

Shared State / Memory 如果需要跨进程、跨 crash 存活，就需要 Persistence。

但：

```text
persistent
≠ shared
```

一个 Agent 的 Private Checkpoint 也可以持久化。

同样：

```text
shared
≠ persistent
```

某个短期 Shared Context 也可能只存在当前 Session。

---

#### 6.5.129 Shared Context 与 Harness

Harness 主要负责：

```text
Context Policy
Visibility Policy
Permission Filter
Role Projection
Promotion Policy
Synchronization Trigger
Compaction Policy
```

所以 6.5 提供概念模型，7.4 Context Policy 会继续落到 Harness 控制层。

---

#### 6.5.130 Shared Context 与 Runtime

Runtime 负责更底层保证：

```text
state store
transaction
version
lock
checkpoint
sandbox
credential isolation
queue
```

因此：

```text
Shared / Private Context
= semantic information architecture

Runtime
= physical consistency / isolation substrate
```

---

#### 6.5.131 一个边界速查表

| 概念 | 核心问题 |
|---|---|
| Communication | 信息怎样从 A 传给 B？ |
| Shared Context | 当前哪些信息被多个 Agent 的决策共同看到？ |
| Private Context | 哪些信息只属于某 Agent / Role / Local Task View？ |
| Shared State | 多 Agent 共同依赖的当前权威任务状态是什么？ |
| Shared Memory | 哪些过去信息跨 Agent 可被未来检索？ |
| Artifact | 大型共享对象如何独立存储与版本化？ |
| Retrieval | 需要时怎样从共享信息空间取回候选？ |
| Context Policy | 当前 Agent 最终看到哪些候选？ |
| Persistence | State / Memory / Artifact 如何跨时间与故障存活？ |
| Runtime | 隔离、同步、执行、存储怎样真正实现？ |

---

#### 6.5.132 工程原则

设计 Shared / Private Context 时，建议长期坚持：

1. **Context is a projection, not a database dump.**
2. **Private by default, share by decision need.**
3. **Shared ≠ Trusted ≠ Authoritative.**
4. **Private ≠ Secret.**
5. **Visible ≠ Writable.**
6. **Writable ≠ Canonical.**
7. **Local Autonomy ≠ Local Truth.**
8. **Canonical Shared State 必须有明确 Source of Truth / Owner。**
9. **Shared State 通过版本化 Projection 进入 Context。**
10. **Local Result 进入 Shared State 前经过 Promotion / Validation。**
11. **共享 Evidence / Commitment，不广播全部过程。**
12. **关键 Shared Item 保留 Provenance / Version / Freshness。**
13. **权限过滤优先于模型可见 Context 构建。**
14. **Secret 留在 Runtime，不通过 Shared Prompt 传播。**
15. **多 Writer State 使用 Patch / Version / Merge，而非盲目覆盖。**
16. **Strong Global Consistency 只用于真正需要的字段。**
17. **Independent Verification 要维护必要的信息独立性。**
18. **Shared Context 也需要 Budget、Compaction 与 Garbage Collection。**
19. **大 Artifact 共享 Reference，不复制全量内容。**
20. **Prompt Injection 的 Trust Label 必须跨 Agent 保留。**
21. **Context Failure 与 Local Reasoning Failure 分开定位。**
22. **对 Context Policy 做 Coverage–Precision–Risk–Cost 联合评估。**
23. **用 Fault Injection 测 stale / conflict / leakage / poisoning。**
24. **Minimal Sufficient Visibility。**

---

#### 6.5.133 面试：Shared Context 和 Shared State 有什么区别？

回答要点：

```text
Shared State
= 系统维护的权威协作状态

Shared Context
= 从 Shared State / Memory / Artifact 中投影到多个 Agent 当前模型调用的信息视图
```

Shared State 可以存在，但某个 Agent 当前不一定需要看到全部。

---

#### 6.5.134 面试：Shared Context 和 Communication 有什么区别？

Communication 是信息交换事件；Shared Context 是信息可见性模型。

```text
A sends X to B
```

是 Communication。

```text
A / B 都能从共同 State View 看见 X
```

是 Shared Context。

---

#### 6.5.135 面试：为什么不能让所有 Agent 共享全部 Context？

因为会增加：

```text
Context Cost
Noise
Instruction Conflict
Privacy Exposure
Prompt Injection Propagation
Correlated Error
Authority Ambiguity
```

并削弱 Multi-Agent 原本的 Context Isolation 收益。

---

#### 6.5.136 面试：Private Context 的价值是什么？

主要是：

```text
local focus
isolation
privacy
independent verification
reduced context pollution
fault containment
```

但影响下游决策的关键内容必须通过显式 Handoff / Promotion 共享。

---

#### 6.5.137 面试：什么是 Canonical Shared State？

多个 Agent 在关键协调决策上共同依赖、由明确 Source of Truth / Owner 管理、具有版本与更新语义的当前任务状态。

---

#### 6.5.138 面试：为什么 Shared ≠ Trusted？

共享只描述可见性；一个恶意网页提取结果完全可以被多个 Agent 看到，但它仍然是不可信数据。

---

#### 6.5.139 面试：为什么 Visible ≠ Writable？

Agent 可能需要读取预算、审批、测试结果，但这些权威字段的修改权应属于 Runtime / 专门 Owner，而不是所有 Reader。

---

#### 6.5.140 面试：怎么处理多个 Agent 同时更新 Shared State？

使用：

```text
version
patch
ownership
optimistic concurrency
merge semantics
conflict resolution
```

而不是 last-write-wins 默认覆盖。

---

#### 6.5.141 面试：Global Consistency 越强越好吗？

不是。很多局部探索不需要实时全局同步。应只对真正影响共享决策 / Side Effect 的状态提供更强一致性，其他信息允许局部自治。

---

#### 6.5.142 面试：怎样避免 Shared Context 污染？

关键包括：

```text
provenance
trust label
fact / hypothesis typing
promotion validation
canonical ownership
freshness
compaction
permission filter
```

---

#### 6.5.143 面试：怎样利用 Context Isolation 提升 Verification？

让 Verifier 看到：

```text
claim + evidence + rubric
```

而不是 Producer 全部推理过程，减少 anchoring 与 correlated confirmation。

---

#### 6.5.144 面试：Shared Context 怎么评测？

至少看：

```text
Necessary Context Coverage
Context Exposure Precision
Unauthorized Exposure Rate
Stale Context Rate
Cross-Agent Consistency
Lost Update Rate
Propagation Latency
Canonical-source Violation
Task Success
Context Cost
```

并做 Wrong→Right / Right→Wrong 净收益分析。

---

#### 6.5.145 面试：什么是 Minimal Sufficient Visibility？

在保证当前 Agent 能正确完成决策的前提下，只暴露必要的信息，不额外扩散无关、敏感、过时或高风险内容。

---

#### 6.5.146 面试：Shared Memory 和 Shared Context 有什么区别？

Shared Memory 是可以跨时间保存并由多个 Agent 再次检索的信息；Shared Context 是当前这一次模型调用真正被选择出来并可见的信息。

---

#### 6.5.147 面试：为什么 Secret 不应该只是 Private Context？

因为 Private Context 仍然是模型可见输入；Credential 更安全的做法是留在 Runtime / Secret Manager，只通过引用或受控执行使用。

---

#### 6.5.148 面试：多 Agent 共享信息时最常见的错误是什么？

典型包括：

```text
all-shared transcript
stale projection
wrong truth promotion
authority ambiguity
lost update
hidden private dependency
cross-tenant leakage
prompt injection propagation
```

---

#### 6.5.149 一个最小实现伪代码

```python
def build_agent_context(agent, shared_state, local_state, memory, policy):
    shared_candidates = project_shared_state(
        shared_state,
        role=agent.role,
        task=agent.current_task,
    )

    shared_candidates = enforce_permissions(
        shared_candidates,
        identity=agent.identity,
    )
    shared_candidates = drop_stale_or_superseded(shared_candidates)
    shared_candidates = filter_by_trust_and_need(shared_candidates, policy)

    private_items = select_local_context(
        local_state=local_state,
        memory=memory,
        task=agent.current_task,
    )

    return assemble_under_budget(
        shared=shared_candidates,
        private=private_items,
        preserve_provenance=True,
    )
```

Local Update 进入 Shared State 则走另一条链：

```python
def propose_shared_update(agent, base_version, patch):
    assert authorized_to_propose(agent, patch)
    validate_patch_schema(patch)
    validate_provenance(patch)

    return commit_if_valid(
        base_version=base_version,
        patch=patch,
        owner_policy=resolve_owner_policy(patch),
    )
```

重点是：

```text
Shared → Local
= projection

Local → Shared
= validated promotion / commit
```

---

#### 6.5.150 一个完整 Context Lifecycle

可以把整套机制串起来：

```text
Environment / Authoritative Systems
        ↓
Observe / Verify
        ↓
Canonical Shared State / Artifact
        ↓
Persist / Version / Provenance
        ↓
Role + Task + Permission + Freshness + Need
        ↓
Shared Context Projection
        ↓
Agent Local Context
        +
Private Working Context
        ↓
Decision / Local Work
        ↓
Result / Evidence / Proposed Patch
        ↓
Promotion Validation
        ↓
Conflict / Ownership / Merge
        ↓
New Canonical Shared State
```

这是 Shared / Private Context 在 Multi-Agent Loop 中的完整位置。

---

#### 6.5.151 本节最核心的五条边界

如果只记五条：

```text
1. Shared Context ≠ Shared State
2. Shared ≠ Trusted ≠ Authoritative
3. Private ≠ Secret
4. Visible ≠ Writable ≠ Canonical
5. Local Autonomy ≠ Local Truth
```

再加一条工程原则：

```text
Context should be projected, not broadcast.
```

---

#### 6.5.152 一句话总结

> **Shared / Private Context 的本质不是决定“哪些聊天记录复制给哪些 Agent”，而是设计一套可验证的信息可见性与同步架构：把 Canonical Shared State、Role / Task-scoped Projection 与 Agent-local Working Context 分开，用明确的 Read / Write / Authority Boundary、Version / Freshness / Provenance 和 Conflict Semantics 在协作一致性与局部自治之间取得平衡；成熟系统共享的是完成当前决策所需的最小可信状态、证据与承诺，而不是把所有上下文广播给所有 Agent。**

---

#### 6.5.153 参考资料

1. Wooldridge, M. *An Introduction to MultiAgent Systems*. Wiley, 2009. 关于多 Agent 环境中的自治、交互、组织与协调边界。
2. Shoham, Y., Leyton-Brown, K. *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations*. Cambridge University Press, 2008. 关于多主体协调、信息与决策结构的基础理论。
3. Kleppmann, M. *Designing Data-Intensive Applications*. O’Reilly Media, 2017. 关于复制、一致性、版本、并发、事件日志、冲突与分布式状态管理；这些概念直接适用于 Shared State 的可靠实现。
4. Hohpe, G., Woolf, B. *Enterprise Integration Patterns*. Addison-Wesley, 2003. 关于 Message、Shared Data、Correlation、Idempotency 与松耦合系统的信息流模式。
5. OpenAI. *Agents SDK — Agent orchestration / Handoffs*. 关于 Agents-as-Tools、Handoff 与 Context / Control Ownership 转移的工程实现，可用于理解“调用另一个 Agent”与“共享 Context”并不是同一件事。
6. Anthropic. *Building Effective Agents*. 关于 orchestrator-workers、parallelization、routing，以及优先使用简单、可组合边界的工程原则。
7. Agent2Agent (A2A) Protocol. Official Specification. 关于 Agent、Task、Message、Artifact 与远程 Agent 交互对象的分离，为跨 Agent 信息边界提供协议级参照。
8. NIST. *AI Risk Management Framework*. 关于信息治理、责任、访问控制与风险管理的通用原则。
9. OWASP. *Top 10 for LLM Applications / Agentic AI security guidance*. 关于 Prompt Injection、Excessive Agency、敏感信息暴露与 Agent 间攻击传播风险。
