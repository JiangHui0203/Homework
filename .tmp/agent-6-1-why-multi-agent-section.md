本节回答一个比“Multi-Agent 怎么编排”更基础的问题：**为什么要有多个 Agent？**

很多系统一看到任务复杂，就自然想到：

```text
任务复杂
↓
拆成多个 Agent
↓
能力更强
```

这个推理并不成立。

Multi-Agent 会引入新的：

```text
communication
coordination
state synchronization
context transfer
permission delegation
failure propagation
latency
cost
observability
```

因此更准确的问题不是：

> “能不能拆成多个 Agent？”

而是：

> **“把一个系统拆成多个具有独立 Decision Loop / Context / State / Capability Boundary 的 Agent，是否产生了足够明确的系统收益？”**

---

#### 6.1.1 Multi-Agent 的基本定义

在本书语境中，Multi-Agent System（MAS）指：

> **同一任务或环境中存在多个具有相对独立 Decision Loop、局部 State / Context、Capability 与行动职责的 Agent，并通过显式或隐式机制协调以完成目标。**

可以抽象为：

\[
A = \{a_1,a_2,\ldots,a_n\}
\]

其中每个 Agent：

\[
a_i = (G_i,S_i,C_i,\pi_i,\mathcal{A}_i)
\]

分别具有：

- 局部 Goal 或 Role；
- Working State；
- Context；
- Decision Policy；
- Action / Capability Set。

系统级目标则可能是：

\[
G_{sys} = F(G_1,G_2,\ldots,G_n)
\]

但局部 Goal 与全局 Goal 不一定天然一致。

---

#### 6.1.2 Multi-Agent 的关键不在“多个模型实例”

下面这个结构：

```text
同一个 Prompt
↓
并行调用 5 次 LLM
↓
投票
```

更接近：

```text
Ensemble / Self-Consistency
```

不一定构成 Multi-Agent。

真正值得称为 Multi-Agent 的核心是：

```text
Distinct Roles / State / Context / Control / Capability
```

而不是简单：

```text
LLM Call Count > 1
```

---

#### 6.1.3 Single Agent + Tools ≠ Multi-Agent

例如：

```text
Agent
├── web_search
├── python
├── filesystem
└── database
```

这里只有一个 Decision Loop。

Tools 本身没有：

```text
Goal
Autonomy
Planning
Stateful Decision Policy
```

因此：

```text
Agent + 100 Tools
```

仍然可以只是 Single-Agent System。

---

#### 6.1.4 Subagent 与 Multi-Agent 的关系

Subagent 是 Multi-Agent 的一种常见组织形式，但两者不完全等价。

典型结构：

```text
Parent Agent
├── Research Subagent
├── Coding Subagent
└── Verification Subagent
```

其中 Parent：

- 创建或选择 Subagent；
- 分配任务；
- 规定 Context / Capability / Budget；
- 接收结果；
- 决定是否继续。

因此：

> **Subagent 是一种有层级的 Multi-Agent Pattern。**

但 Multi-Agent 还可能是：

- peer-to-peer；
- blackboard；
- market / auction；
- debate；
- swarm；
- committee；
- supervisor-worker。

---

#### 6.1.5 Multi-Agent ≠ Workflow

Workflow：

```text
A → B → C
```

通常由开发者预先定义控制流。

Multi-Agent：

```text
Agent A
   ↕
Agent B ↔ Agent C
```

可能由 Agent 自身根据 State 决定：

- 谁执行；
- 是否继续委派；
- 是否重新协商；
- 是否请求其他 Agent；
- 如何整合结果。

因此：

```text
多个节点
≠
多个 Agent
```

一个完全确定性的 DAG 仍然可以只是 Workflow。

---

#### 6.1.6 Multi-Agent ≠ Multi-model

系统可能是：

```text
Agent A → Model X
Agent B → Model X
Agent C → Model X
```

仍然是 Multi-Agent。

也可能是：

```text
一个 Agent
根据任务动态调用
Model X / Y / Z
```

这属于 Multi-model Routing，未必是 Multi-Agent。

因此：

```text
Multi-Agent
≠
Multi-model
```

---

#### 6.1.7 Multi-Agent ≠ Ensemble

Ensemble 常见结构：

```text
Model 1 ─┐
Model 2 ─┼→ Vote / Aggregate
Model 3 ─┘
```

多个成员通常：

- 解同一个问题；
- 不形成长期角色；
- 不维护独立持续 State；
- 不相互产生复杂行动影响。

Multi-Agent 更强调：

```text
division of labor
interaction
coordination
stateful roles
```

---

#### 6.1.8 Multi-Agent 的核心是系统分解

把单体 Agent：

```text
One Agent
├── plan
├── research
├── write
├── execute
├── verify
└── recover
```

拆为：

```text
Planner
Researcher
Executor
Verifier
```

本质上是：

> **把一个大的 Decision Boundary 拆成多个较小的 Decision Boundaries。**

这和软件工程中的：

```text
Monolith → Services
```

有一定相似性。

但不能机械类比，因为 Agent 边界还包含：

- Context；
- uncertainty；
- semantic communication；
- autonomous action；
- stochastic behavior。

---

#### 6.1.9 为什么会想到 Multi-Agent？

主要动机通常来自五类瓶颈：

```text
1. Specialization
2. Context Isolation
3. Parallelism
4. Authority Isolation
5. Failure / Verification Separation
```

也可以概括成：

```text
Knowledge Boundary
Context Boundary
Compute Boundary
Permission Boundary
Trust Boundary
```

---

#### 6.1.10 动机一：Specialization

一个 Agent 同时承担：

```text
法律分析
代码执行
财务计算
安全审批
```

意味着它需要同时加载大量：

```text
instructions
skills
tools
terminology
policies
```

拆分后：

```text
Legal Agent
Code Agent
Finance Agent
Security Agent
```

可以拥有不同：

```text
System Instructions
Skills
Tool Sets
Evaluation Criteria
Model Choice
```

因此：

> **Multi-Agent 可以通过 Role Specialization 缩小单个 Agent 的决策空间。**

---

#### 6.1.11 Specialization 的真正收益不是“角色名字”

给同一个模型分别写：

```text
You are a researcher.
You are a critic.
```

不自动产生有效 specialization。

真正的 specialization 需要至少在部分维度上不同：

```text
Context
Capability
Policy
Data Access
Objective
Verifier
Model
Budget
```

否则所谓 Multi-Agent 可能只是：

> **Role-playing over the same underlying decision process.**

---

#### 6.1.12 动机二：Context Isolation

单 Agent 很容易出现：

```text
Research Logs
+ Code
+ Tool Outputs
+ User Conversation
+ Safety Policies
+ Verification Evidence
```

全部堆进一个 Context。

结果：

```text
Context Pollution ↑
Token Cost ↑
Attention Competition ↑
Instruction Conflict ↑
```

Multi-Agent 可以把 Context 分域：

```text
Research Agent
→ 只看资料和问题

Coding Agent
→ 只看代码、Issue、测试

Verifier Agent
→ 只看 claim + evidence
```

所以：

> **Context Isolation 是 Multi-Agent 最现实的收益之一。**

---

#### 6.1.13 Context Isolation ≠ Information Loss

隔离并不意味着：

```text
Agent B 完全不知道 Agent A 做了什么
```

而应该通过显式 Handoff 传递：

```text
Minimal Sufficient Delegation Context
```

例如：

```text
Goal
Constraints
Relevant Evidence
Artifact References
Open Questions
Required Output Contract
```

而不是整段 Transcript Dump。

---

#### 6.1.14 动机三：Parallelism

若任务可以分解成互相独立的子问题：

```text
Search Source A
Search Source B
Inspect Code
Check Documentation
```

可以并行：

```text
        Coordinator
       /    |     \
      A     B      C
       \    |     /
        Aggregate
```

理论上可以降低：

```text
wall-clock latency
```

但不一定降低：

```text
Total Compute
Token Cost
Tool Cost
```

---

#### 6.1.15 Parallelism ≠ Efficiency

三个 Agent 并行：

```text
3 × 20 s
```

可能把 wall-clock 从 60 s 降到 20 s。

但总计算量可能仍是：

```text
60 agent-seconds
```

甚至更高，因为还需要：

```text
coordination
aggregation
deduplication
verification
```

所以：

> **Parallelism 优化的是 Critical Path，不自动优化 Total Cost。**

---

#### 6.1.16 并行成立需要低依赖

适合并行：

```text
A 与 B 输入独立
A 与 B 输出可独立产生
最后再聚合
```

不适合并行：

```text
B 必须依赖 A 的结果
```

如果强行并行：

```text
speculative work
↓
大量结果废弃
```

成本反而上升。

---

#### 6.1.17 动机四：Authority Isolation

非常重要的一类拆分是：

```text
Research Agent
→ read-only

Execution Agent
→ write permission
```

或者：

```text
Planner
→ can propose

Approver
→ can authorize

Executor
→ can execute
```

这样可以做到：

```text
Autonomy Separation
Authority Separation
```

---

#### 6.1.18 Multi-Agent 可以实现 Separation of Duties

例如高风险操作：

```text
Agent A proposes payment
Agent B validates invoice
Agent C executes payment
```

只要三者的：

```text
credentials
permissions
state
policies
```

真正隔离，就能形成类似：

```text
Separation of Duties
```

的安全控制。

---

#### 6.1.19 角色分离 ≠ 权限分离

如果：

```text
Planner Agent
Verifier Agent
Executor Agent
```

实际上都共享：

```text
same root credential
same unrestricted shell
```

那么只是：

```text
semantic role separation
```

不是：

```text
security isolation
```

因此：

> **真正的 Authority Isolation 必须由 Runtime / Credential / Permission Boundary 强制实现。**

---

#### 6.1.20 动机五：Independent Verification

如果同一个 Agent：

```text
生成答案
↓
再验证自己的答案
```

它可能共享：

```text
same assumptions
same context bias
same reasoning path
```

拆出独立 Verifier：

```text
Producer
    ↓ claim + evidence
Verifier
```

可以减少部分 correlated error。

---

#### 6.1.21 Verifier 独立性的来源

Verifier 真正有价值，需要至少有一部分独立性：

```text
Different Context
Different Evidence
Different Tool Access
Different Objective
Different Prompt
Different Model
```

否则：

```text
Producer
↓ same transcript
Verifier
```

可能只是重复确认原来的偏差。

---

#### 6.1.22 Independent Verification ≠ Different Model Required

可以是：

```text
same model weights
```

但：

```text
separate context
separate evidence
separate role objective
```

仍然可能带来一定独立性。

所以：

```text
Agent Independence
≠
Model Independence
```

---

#### 6.1.23 Multi-Agent 的第六类动机：Heterogeneous Models

不同 Agent 可以绑定不同模型：

```text
Router → small fast model
Researcher → long-context model
Coder → code-specialized model
Verifier → stronger reasoning model
```

优点是：

```text
Capability Matching
Cost Optimization
Latency Optimization
```

但这属于：

```text
Multi-Agent + Multi-model
```

而不是 Multi-Agent 的必要条件。

---

#### 6.1.24 第七类动机：Environment / Data Isolation

不同 Agent 可以运行在不同环境：

```text
Public Research Agent
→ Internet

Internal Data Agent
→ Private DB

Code Agent
→ Sandbox
```

它们不需要共享全部数据访问能力。

这可以减少：

```text
Cross-domain Leakage
Secret Exposure
Blast Radius
```

---

#### 6.1.25 第八类动机：Ownership Boundary

组织现实中不同能力可能属于：

```text
Finance Team
Security Team
Legal Team
Platform Team
```

如果每个域有自己的 Agent / Service Boundary：

```text
policy ownership
release cycle
audit responsibility
```

可能更清楚。

因此 Multi-Agent 有时不仅是 AI 架构，也是：

> **Organizational Boundary 的软件映射。**

---

#### 6.1.26 第九类动机：Long-running Delegation

一个 Parent Agent 可以：

```text
Delegate research task
↓
continue other work
↓
receive result later in logical task flow
```

这对：

```text
asynchronous workflows
long-running jobs
external approvals
```

尤其有价值。

但真正支持这种模式需要 Runtime 提供：

```text
Durable State
Task ID
Callback / Event
Checkpoint
Timeout
Cancellation
```

不能只靠 Prompt。

---

#### 6.1.27 第十类动机：Fault Containment

如果一个 Agent：

```text
crashes
loops
gets poisoned
```

不一定应该拖垮整个系统。

合理分区可以形成：

```text
Fault Domain
```

例如：

```text
Browser Agent compromised
↓
cannot directly access payment credential
```

这比单体 Agent 的共享全权限安全得多。

---

#### 6.1.28 Multi-Agent 的代价一：Coordination Overhead

拆分以后必须回答：

```text
谁做什么？
何时做？
输入是什么？
结果给谁？
失败谁处理？
冲突谁裁决？
什么时候结束？
```

这些原本在单 Agent 内部隐式解决的问题，都会变成系统设计问题。

---

#### 6.1.29 代价二：Communication Cost

Agent 之间的通信消耗：

```text
Tokens
Serialization
Network
Latency
Context Budget
```

甚至会引入：

```text
semantic distortion
```

因此：

> **Communication 本身是一种系统成本。**

---

#### 6.1.30 Communication Loss

Agent A 的内部 State：

```text
100 units information
```

Handoff 可能只传：

```text
20 units summary
```

于是：

```text
information compression
↓
possible omission
↓
downstream error
```

这就是：

```text
Communication Loss
```

---

#### 6.1.31 Communication Noise

除了漏信息，还可能加入新误差：

```text
mis-summary
ambiguous wording
wrong entity mapping
lost uncertainty
lost provenance
```

所以：

```text
Agent A 正确
```

不保证：

```text
Agent B 收到的信息正确
```

---

#### 6.1.32 Communication Protocol 是系统能力

高质量 Handoff 不应只是一段自由文本：

```text
“我做完了，大概是这样……”
```

更可靠的结构是：

```text
Task ID
Goal
Status
Inputs Used
Findings
Evidence
Artifacts
Open Questions
Uncertainty
Required Next Action
```

也就是：

> **Agent Communication 需要 Contract。**

---

#### 6.1.33 代价三：State Fragmentation

单 Agent：

```text
S_t
```

Multi-Agent：

```text
S_A
S_B
S_C
Shared State
Environment State
```

于是出现：

```text
谁的 State 才是权威？
```

如果不明确：

```text
Agent A says X
Agent B says Y
```

系统无法判断。

---

#### 6.1.34 Local State 与 Shared State

可以区分：

```text
Local State
= Agent 私有工作状态

Shared State
= 多个 Agent 需要共同依赖的状态
```

原则：

> **能局部化的 State 尽量局部化；必须共享的 State 才进入 Shared State。**

否则会造成：

```text
contention
pollution
coupling
```

---

#### 6.1.35 Shared State ≠ Shared Transcript

把所有 Agent 消息全部塞入一个公共聊天记录：

```text
A says...
B says...
C says...
```

并不等于有好的 Shared State。

真正 Shared State 应该更接近：

```text
Task Status
Artifact Registry
Decisions
Committed Effects
Open Issues
Ownership
Version
```

---

#### 6.1.36 代价四：Consistency Problem

如果 Agent A 修改：

```text
resource version = 12
```

Agent B 还基于：

```text
version = 11
```

执行，就出现：

```text
stale decision
```

因此 Multi-Agent 会放大：

```text
Concurrency
Versioning
Consistency
TOCTOU
```

问题。

---

#### 6.1.37 代价五：Duplicate Work

多个 Agent 很容易：

```text
Researcher A 搜同一页面
Researcher B 搜同一页面
Researcher C 又搜一遍
```

所以 Parallelism 可能退化为：

```text
Redundant Compute
```

需要：

```text
Task Assignment
Deduplication
Shared Artifact Index
```

---

#### 6.1.38 代价六：Conflicting Conclusions

如果：

```text
Agent A → YES
Agent B → NO
```

系统必须有：

```text
Arbitration Policy
```

例如：

- majority vote；
- confidence-weighted vote；
- evidence-based judge；
- authoritative role；
- human escalation。

如果没有：

```text
more agents
```

只会产生：

```text
more unresolved opinions
```

---

#### 6.1.39 代价七：Correlated Error

多个 Agent 并不保证独立。

如果都使用：

```text
same model
same prompt template
same retrieved evidence
same wrong assumption
```

那么：

```text
P(all wrong)
```

可能远高于“独立错误”假设。

因此：

> **Agent 数量 ≠ Error Diversity。**

---

#### 6.1.40 Debate 不是天然可靠

多个 Agent 互相辩论：

```text
A argues
B counters
A revises
```

可能提升结果，也可能出现：

```text
rhetorical convergence
false consensus
dominance by confident agent
shared hallucination
```

所以 Debate 必须被 Eval，而不是当作默认增强器。

---

#### 6.1.41 代价八：Error Amplification

如果上游 Agent 输出错误：

```text
A wrong summary
↓
B plans on it
↓
C executes it
```

会形成：

```text
Error Propagation Chain
```

甚至比单 Agent 更难定位。

---

#### 6.1.42 Agent-to-Agent Handoff 是新的 Trust Boundary

Agent A 输出给 Agent B 的内容：

```text
不能自动视为 Ground Truth
```

仍然需要：

```text
Provenance
Evidence
Trust Level
Version
```

因此：

```text
Agent Output
≠ Verified Fact
```

这个原则和 Observation / Memory 一样。

---

#### 6.1.43 代价九：Permission Propagation

如果 Parent Agent 有：

```text
read + write + delete
```

委派 Subagent 时，不能默认：

```text
Subagent inherits all permissions
```

更合理的是：

```text
Delegated Authority
⊆
Parent Authority
```

---

#### 6.1.44 Delegation ≠ Authorization Transfer

一句：

```text
“你帮我处理一下。”
```

不应该自动等价于：

```text
“把我所有 Credential 都交给你。”
```

因此：

> **Task Delegation 与 Authority Delegation 必须分开。**

---

#### 6.1.45 Delegated Authority 的最小化

例如 Parent 要求 Subagent：

```text
分析 PR 风险
```

Subagent 只需要：

```text
read repo
read diff
run tests
```

不需要：

```text
merge PR
delete branch
change repository settings
```

这就是：

```text
Least Privilege Delegation
```

---

#### 6.1.46 代价十：Observability Complexity

单 Agent Trace：

```text
Step 1 → Step 2 → Step 3
```

Multi-Agent Trace 可能是：

```text
Parent
├── A1
│   ├── A1.1
│   └── A1.2
├── B1
└── C1
    └── C1.1
```

所以至少需要：

```text
trace_id
agent_id
parent_agent_id
task_id
handoff_id
call_id
```

---

#### 6.1.47 Trace 必须支持因果关系

仅按时间排序：

```text
10:01 A
10:01 B
10:02 C
```

无法表达：

```text
C 是由 A 的结果触发
```

因此更需要：

```text
causal links
parent-child spans
artifact lineage
```

---

#### 6.1.48 Multi-Agent 的成本函数

可以用一个概念公式：

\[
C_{MAS} = \sum_i C(a_i) + C_{coord} + C_{comm} + C_{sync} + C_{verify}
\]

其中新增的：

```text
Coordination Cost
Communication Cost
Synchronization Cost
Verification Cost
```

是单 Agent 不一定拥有的系统开销。

---

#### 6.1.49 Multi-Agent 的收益函数

可以概念化为：

\[
B_{MAS} = B_{spec} + B_{parallel} + B_{isolation} + B_{verification} + B_{authority}
\]

包括：

```text
Specialization Benefit
Parallelism Benefit
Context Isolation Benefit
Independent Verification Benefit
Authority Isolation Benefit
```

因此是否拆分，本质上看：

\[
B_{MAS} - C_{MAS}
\]

而不是：

```text
Agent Count 越高越先进
```

---

#### 6.1.50 最重要的架构原则：Single Agent First

默认优先：

```text
Single Agent
+ Good Tools
+ Good Context
+ Good State
+ Good Harness
```

只有当明确发现：

```text
single-agent bottleneck
```

再拆。

这类似：

> **不要为了微服务而微服务，也不要为了 Multi-Agent 而 Multi-Agent。**

---

#### 6.1.51 什么情况下不需要 Multi-Agent？

如果任务：

```text
短
低风险
上下文小
能力单一
步骤高度依赖
没有并行价值
没有权限隔离需求
```

通常单 Agent 更简单可靠。

---

#### 6.1.52 情况一：简单 Tool Use

例如：

```text
查天气
```

Single Agent：

```text
understand → call weather tool → answer
```

拆成：

```text
Planner → Weather Agent → Formatter Agent
```

几乎只是增加成本。

---

#### 6.1.53 情况二：严格顺序流程

例如：

```text
A 必须完成
↓
B 才能开始
↓
C 必须基于 B
```

如果每一步又没有不同权限或 specialization，Workflow 通常优于 Multi-Agent。

---

#### 6.1.54 情况三：强共享上下文

如果所有步骤都依赖大量共同上下文：

```text
同一复杂法律案卷
```

拆成很多 Agent 可能导致：

```text
Context Duplication
Communication Loss
Cost Explosion
```

未必划算。

---

#### 6.1.55 情况四：极低延迟任务

Multi-Agent 通常多出：

```text
spawn
serialize
network
aggregate
```

如果 SLA 是：

```text
sub-second
```

可能完全不适合复杂 Multi-Agent。

---

#### 6.1.56 情况五：同质 Agent 无真实分工

如果：

```text
Agent A = same model + same tools + same prompt style
Agent B = same model + same tools + same prompt style
```

只有名字不同，往往价值有限。

---

#### 6.1.57 Multi-Agent 拆分判据一：Role Cohesion

一个 Agent 的职责应该尽量：

```text
high cohesion
```

即任务之间强相关。

例如：

```text
Research Agent
→ search
→ source evaluation
→ evidence extraction
```

比：

```text
Research + Payment + Deployment Agent
```

更合理。

---

#### 6.1.58 拆分判据二：Low Coupling

Agent 之间应尽量：

```text
low coupling
```

如果每一步都需要共享全部 State：

```text
A ↔ B ↔ C ↔ D
```

频繁同步，那么拆分可能错误。

---

#### 6.1.59 拆分判据三：Clear Contract

如果无法明确写出：

```text
Input Contract
Output Contract
Success Criteria
Failure Semantics
```

说明 Agent 边界可能还不成熟。

---

#### 6.1.60 拆分判据四：Independent Evaluation

一个好的 Agent Role 最好能独立评价：

```text
Research quality
Coding correctness
Verification accuracy
```

如果完全无法独立 Eval，边界可能太模糊。

---

#### 6.1.61 拆分判据五：Distinct Capability Boundary

当不同子任务需要明显不同的：

```text
Tool Set
Data Access
Model
Runtime
Permission
```

Multi-Agent 更容易合理。

---

#### 6.1.62 拆分判据六：Distinct Context Boundary

如果某一类任务需要大量专属 Context：

```text
Codebase Context
Legal Context
Financial Context
```

分离 Agent 可以减少 Context Pollution。

---

#### 6.1.63 拆分判据七：Distinct Trust Boundary

例如：

```text
Untrusted Web Agent
```

不应该与：

```text
Privileged Admin Agent
```

共享同一个 Trust Boundary。

这种拆分往往比“按业务角色拆分”更重要。

---

#### 6.1.64 拆分判据八：Parallelizable Work

如果子任务之间：

```text
Dependency Low
Work High
```

则并行收益可能很大。

反之：

```text
Dependency High
Work Low
```

拆分收益很低。

---

#### 6.1.65 拆分判据九：Independent Failure Domain

如果某子任务容易：

```text
timeout
crash
loop
poison
```

可以考虑独立 Agent / Runtime 隔离。

---

#### 6.1.66 拆分判据十：Ownership / Governance

如果不同模块需要不同：

```text
owner
policy
release cadence
approval
```

明确 Agent Boundary 可能利于治理。

---

#### 6.1.67 一个实用的拆分矩阵

| 维度 | 单 Agent 更合适 | Multi-Agent 更合适 |
|---|---|---|
| Context | 高共享 | 可明显分区 |
| Capability | 相似 | 明显不同 |
| Permission | 相同 | 需要隔离 |
| Dependency | 高 | 低/可并行 |
| Evaluation | 统一 | 可独立评测 |
| Failure | 强耦合 | 可隔离 |
| Latency | 极低 | 可容忍编排 |
| Task size | 小 | 大/复杂 |

---

#### 6.1.68 Single Agent + Skill vs Multi-Agent

如果问题只是：

```text
“这一类任务步骤很多”
```

优先考虑：

```text
Skill
```

如果问题是：

```text
“不同部分需要独立 Context / Authority / State / Decision Loop”
```

才更可能需要：

```text
Multi-Agent
```

因此：

```text
Complex Procedure
→ Skill / Workflow

Distinct Decision Boundary
→ Agent
```

---

#### 6.1.69 Tool vs Skill vs Agent

可以用一个连续谱理解：

```text
Tool
= primitive action

Skill
= reusable method

Agent
= autonomous decision loop
```

判断是否升级为 Agent，关键是：

> **是否真的需要独立决策权与持续状态。**

---

#### 6.1.70 Function ≠ Service ≠ Agent

类似软件工程：

```text
Function
→ does one computation

Service
→ exposes persistent API boundary

Agent
→ chooses actions toward goals
```

不能因为一个模块独立部署，就自动叫 Agent。

---

#### 6.1.71 Multi-Agent 不是“模拟公司组织架构”

常见设计：

```text
CEO Agent
Manager Agent
Engineer Agent
Reviewer Agent
```

如果这些层级并没有：

```text
真实不同的信息
权限
能力
状态
责任
```

往往只是组织隐喻。

因此：

> **组织角色名称不能替代系统边界。**

---

#### 6.1.72 人类组织类比的局限

人类团队需要分工，是因为：

```text
human cognitive bandwidth limited
knowledge localized
physical concurrency
organizational responsibility
```

LLM Agent 的成本结构不同：

```text
Context Copy Cost
Token Cost
Model Call Cost
Communication Loss
```

因此不能直接复制：

```text
“现实里有 8 个岗位，所以设计 8 个 Agent。”
```

---

#### 6.1.73 Multi-Agent 的最小单位：Decision Ownership

比 Role Name 更准确的问题是：

```text
谁拥有这个 Decision？
```

例如：

```text
Research Agent
owns evidence collection decision

Verifier Agent
owns claim verification decision

Executor Agent
owns execution decision
```

这比“你是研究员”更有工程意义。

---

#### 6.1.74 Decision Ownership 必须对应 Accountability

如果 Agent A 负责：

```text
approve deployment
```

但出错后系统只记录：

```text
“Multi-agent system failed”
```

那么边界没有形成可审计性。

应该能够定位：

```text
which agent
which decision
which evidence
which policy
```

---

#### 6.1.75 Global Goal 与 Local Goal

系统级：

```text
ship correct software
```

局部 Agent：

```text
Coder → fix issue
Verifier → find remaining failures
Security → prevent unsafe changes
```

局部 Goal 可以不同，甚至存在有意张力。

---

#### 6.1.76 Goal Decomposition 风险

如果 Parent 将：

```text
G
```

分解为：

```text
G1, G2, G3
```

但遗漏关键约束：

```text
C
```

Subagent 即使完美完成 G1/G2/G3，整体仍可能失败。

因此：

> **Goal Decomposition Error 是 Multi-Agent 的一等错误。**

---

#### 6.1.77 Local Optimality ≠ Global Success

例如：

```text
Researcher 最大化信息量
Writer 最大化完整度
```

可能导致：

```text
Final Answer 超长
```

每个 Agent 局部表现都很好，但系统目标：

```text
concise useful answer
```

反而失败。

这就是：

```text
Local Objective Misalignment
```

---

#### 6.1.78 Multi-Agent Credit Assignment

结果失败时需要知道：

```text
谁造成的？
```

可能是：

```text
bad decomposition
bad delegation
bad local execution
bad handoff
bad aggregation
bad arbitration
```

因此系统级 Eval 必须支持：

```text
Credit / Blame Assignment
```

---

#### 6.1.79 Parent Agent 不是天然 Ground Truth

在层级系统：

```text
Parent
↓
Subagents
```

Parent 的 decomposition / integration 也可能错。

所以不要默认：

```text
Supervisor = Correct
```

Supervisor 只是：

```text
Control Role
```

不是 Truth Oracle。

---

#### 6.1.80 Supervisor Bottleneck

所有信息都经过 Supervisor：

```text
Workers
↓
Supervisor
↓
Workers
```

会产生：

```text
serialization bottleneck
context overload
single point of failure
```

所以层级结构也有上限。

---

#### 6.1.81 Peer-to-Peer 的反面问题

完全去中心化：

```text
A ↔ B ↔ C ↔ D
```

可能出现：

```text
message explosion
unclear ownership
conflicting decisions
termination ambiguity
```

因此：

```text
centralization
vs
coordination overhead
```

也是 trade-off。

---

#### 6.1.82 Multi-Agent 的拓扑本身是设计变量

常见拓扑：

```text
Star
Tree
DAG
Peer-to-peer
Blackboard
Market
Committee
```

不同拓扑影响：

```text
latency
fault tolerance
communication cost
authority
observability
```

所以：

> **Agent Count 不是唯一重要参数，Interaction Topology 同样重要。**

---

#### 6.1.83 Agent Boundary 应和 Trust Boundary 对齐

如果：

```text
Agent A 处理不可信网页
Agent B 持有高权限凭证
```

最好不仅 Prompt 分离，还在：

```text
Context
Credentials
Sandbox
Network
Filesystem
```

层面真正隔离。

---

#### 6.1.84 Shared Model ≠ Shared Trust Boundary

两个 Agent 可以使用同一个模型服务，但仍然拥有：

```text
不同 system instruction
不同 context
不同 credential
不同 tools
不同 sandbox
```

因此：

```text
Model Instance
```

与：

```text
Security Boundary
```

不是同一个概念。

---

#### 6.1.85 Shared Memory 风险

多个 Agent 共用 Memory：

```text
A writes
↓
Shared Memory
↓
B retrieves
```

会引入：

```text
Memory Poisoning
Ownership Conflict
Stale Update
Cross-role Leakage
```

因此必须定义：

```text
who can write
who can overwrite
who can read
which provenance
```

---

#### 6.1.86 Shared Artifact 比 Shared Transcript 更稳

例如多个 Agent 协作写报告：

与其共享：

```text
所有聊天消息
```

更合理的是共享：

```text
outline.md
sources.json
claims.csv
draft.md
```

即：

> **通过 Artifact 协作，而不是通过无限聊天记录协作。**

---

#### 6.1.87 Blackboard Pattern 的基本思想

多个 Agent 不直接互相私聊，而通过：

```text
Shared Blackboard
```

写入：

```text
facts
hypotheses
tasks
artifacts
```

优点：

```text
shared visibility
looser coupling
```

风险：

```text
state pollution
write conflict
stale entries
```

---

#### 6.1.88 Multi-Agent 需要显式 Termination

单 Agent 已经可能无限循环。

多个 Agent 更可能：

```text
A asks B
B asks C
C asks A
```

因此必须定义：

```text
max_agents
max_delegation_depth
max_messages
max_steps
max_cost
wall-clock deadline
```

---

#### 6.1.89 Delegation Depth

例如：

```text
Parent
└── Subagent
    └── Sub-subagent
        └── ...
```

需要：

```text
Delegation Depth Limit
```

否则 Capability / Permission / Cost 都可能失控。

---

#### 6.1.90 Agent Spawn 也是一种 Side Effect

Spawn 新 Agent 会产生：

```text
compute cost
model calls
resource allocation
new authority surface
new communication paths
```

因此：

> **Spawn Subagent 不是免费的内部思考，而是一种系统动作。**

---

#### 6.1.91 Agent Budget

除了每个 Agent 自己的 Budget，还需要系统级：

```text
Total Agent Count
Total Model Calls
Total Tokens
Total Tool Calls
Total Wall Time
Total Money
```

否则每个 Subagent 都“预算内”，系统总体仍可能爆炸。

---

#### 6.1.92 Budget Delegation

Parent 可以把预算分配为：

```text
Researcher: 30%
Coder: 40%
Verifier: 20%
Reserve: 10%
```

这比每个 Agent 无限申请资源更可控。

---

#### 6.1.93 Dynamic Budget Reallocation

若 Research Agent 很快完成：

```text
unused budget
```

可以转给：

```text
Verifier
```

因此 Multi-Agent Budget 也可以动态管理。

---

#### 6.1.94 Multi-Agent 与 Reliability

Multi-Agent 可能：

```text
increase redundancy
```

也可能：

```text
increase failure surface
```

所以：

```text
More Agents
≠
More Reliable
```

需要实际评测。

---

#### 6.1.95 Redundancy 的两种类型

```text
Active Redundancy
= 多个 Agent 同时执行同一任务

Standby Redundancy
= 主 Agent 失败后 fallback
```

成本和可靠性特征不同。

---

#### 6.1.96 Fallback Agent

例如：

```text
Primary Coding Agent
↓ failure
Fallback Coding Agent
```

需要判断：

```text
failure class
state compatibility
partial effects
```

不能简单：

```text
primary failed → rerun everything
```

---

#### 6.1.97 Handoff 必须包含 Effect State

如果 Agent A 已经：

```text
sent email
```

Agent B 接手时必须知道：

```text
email effect committed
```

否则可能重复发送。

所以 Handoff 不能只传：

```text
“What remains to do?”
```

还必须传：

```text
“What has already happened?”
```

---

#### 6.1.98 Handoff State 的最小集合

常见至少包括：

```text
Goal
Constraints
Current State
Completed Work
Committed Effects
Pending / Unknown Effects
Evidence
Artifacts
Open Questions
Budget
Permission Scope
```

---

#### 6.1.99 Multi-Agent 与 Human-in-the-loop

Human 也可以被视为系统中的特殊 Decision / Approval Node：

```text
Agent
↓
Human Approval
↓
Agent
```

但：

```text
Human ≠ Agent
```

产品与责任语义必须保持清楚。

---

#### 6.1.100 Human 适合承担什么？

通常更适合：

```text
High-impact Approval
Ambiguous Intent Resolution
Normative Judgment
Exception Handling
```

而不是：

```text
每一步都人工点击确认
```

否则自动化价值消失。

---

#### 6.1.101 Multi-Agent 与 A2A

Multi-Agent 是系统架构概念。

A2A 是：

```text
Agent ↔ Agent
```

互操作的一类协议问题。

因此：

```text
Multi-Agent
≠
A2A
```

一个进程内 Multi-Agent 完全可以不需要网络协议。

---

#### 6.1.102 MCP 与 Multi-Agent

MCP 主要解决：

```text
Agent / Host
→ Tools / Resources / Capabilities
```

Multi-Agent 关注：

```text
Agent
↔
Agent
```

所以：

```text
MCP
≠
Multi-Agent Protocol
```

虽然一个 Agent 也可以通过某种包装暴露成 Tool，但语义会发生降级。

---

#### 6.1.103 Agent-as-Tool

一个 Agent 可以被另一个 Agent 调用：

```text
Parent
↓ tool call
ResearchAgent(query)
```

这是一种非常实用的模式。

对 Parent 来说：

```text
ResearchAgent
```

看起来像 Tool。

但内部仍然拥有：

```text
loop
state
tools
planning
```

---

#### 6.1.104 Agent-as-Tool 的边界

如果只暴露：

```text
input → final output
```

Parent 不一定看到：

```text
internal trajectory
```

优点：

```text
encapsulation
context isolation
```

代价：

```text
reduced observability
harder verification
```

---

#### 6.1.105 Multi-Agent 的三种主要收益类型

可以归纳为：

```text
Capacity Gain
Isolation Gain
Control Gain
```

其中：

```text
Capacity Gain
→ specialization / parallelism

Isolation Gain
→ context / permission / failure

Control Gain
→ verification / separation of duties
```

---

#### 6.1.106 Multi-Agent 的三种主要成本类型

```text
Coordination Cost
Information Loss
System Complexity
```

其中 System Complexity 包含：

```text
state
recovery
permission
observability
versioning
evaluation
```

---

#### 6.1.107 一个更完整的决策式

可以概念化：

\[
\Delta U = B_{spec} + B_{parallel} + B_{isolation} + B_{verify}
- C_{coord} - C_{comm} - C_{sync} - C_{failure} - C_{latency}
\]

只有当：

\[
\Delta U > 0
\]

拆分才有系统意义。

这不是严格数值公式，而是设计检查框架。

---

#### 6.1.108 Minimal Sufficient Agent Count

本章引入新的“最小充分”原则：

> **Minimal Sufficient Agent Count：用完成任务所需的最少 Agent 数量实现必要的 specialization、isolation 与 coordination。**

不是：

```text
越多 Agent 越强
```

而是：

```text
每增加一个 Agent
必须能解释它解决了哪个明确系统瓶颈
```

---

#### 6.1.109 新 Agent 的存在理由测试

为每个 Agent 回答：

```text
Why is this a separate Agent?
```

如果只能回答：

```text
“因为这个任务比较复杂。”
```

理由不够。

更合理的答案应是：

```text
需要独立 Context
需要独立 Permission
需要并行
需要独立 Verification
需要独立 Failure Domain
需要专用 Model / Tool
```

---

#### 6.1.110 Agent Removal Test

一个很实用的设计测试：

```text
删掉 Agent B
把它的职责并回 Agent A
```

如果：

```text
质量几乎不变
成本更低
系统更简单
```

说明 Agent B 可能没有必要。

---

#### 6.1.111 Agent Merge Test

如果两个 Agent：

```text
共享相同 Context
共享相同 Tool
共享相同 Permission
共享相同 Objective
频繁互相传消息
```

应该问：

> **为什么不合并？**

这和数据库 normalization / service boundary 一样，是架构审计问题。

---

#### 6.1.112 Agent Split Test

反过来，如果一个 Agent 同时：

```text
处理 untrusted web
持有 admin credential
执行支付
验证自己
```

就应该问：

> **为什么不拆？**

---

#### 6.1.113 Single-Agent Baseline 是必须的

任何 Multi-Agent 方法评测都应该有：

```text
Strong Single-Agent Baseline
```

例如：

```text
same model
same tools
same total budget
```

否则无法判断收益到底来自：

```text
更多计算
更多 Token
更多 Tool Call
还是 Multi-Agent 结构本身
```

---

#### 6.1.114 Budget-matched Baseline

非常重要：

Multi-Agent：

```text
4 Agents × 4k tokens
```

如果只和：

```text
1 Agent × 4k tokens
```

比较，不公平。

还应该考虑：

```text
1 Agent × 16k token budget
```

或同等 Model Call Budget。

---

#### 6.1.115 Multi-Agent Eval 的核心问题

不能只问：

```text
最终 Task Success 是否提高？
```

还要问：

```text
为什么提高？
在哪里提高？
新增成本多少？
哪些任务受益？
哪些任务退化？
```

---

#### 6.1.116 Multi-Agent Net Benefit

延续前面的净收益思路：

```text
MAS Net Benefit
=
Single-Agent Wrong → MAS Right
-
Single-Agent Right → MAS Wrong
```

同时报告：

```text
Cost Delta
Latency Delta
```

---

#### 6.1.117 Multi-Agent Failure Taxonomy

至少区分：

```text
Decomposition Failure
Delegation Failure
Role Selection Failure
Context Transfer Failure
Local Execution Failure
Communication Failure
State Sync Failure
Permission Failure
Aggregation Failure
Arbitration Failure
Termination Failure
```

这比一个：

```text
MAS failed
```

有诊断价值。

---

#### 6.1.118 Communication Evaluation

可以单独评价：

```text
Constraint Retention
Evidence Retention
Uncertainty Retention
Provenance Retention
Artifact Correctness
```

即：

```text
Agent A knows X
↓ handoff
Agent B receives X correctly?
```

---

#### 6.1.119 Coordination Evaluation

可以评价：

```text
Duplicate Work Rate
Idle Time
Conflicting Work Rate
Unnecessary Handoff Rate
Delegation Depth
Coordination Token Cost
```

---

#### 6.1.120 Authority Evaluation

重点看：

```text
Unauthorized Delegation Rate
Privilege Escalation Rate
Over-broad Credential Exposure
Cross-agent Secret Leakage
```

---

#### 6.1.121 Parallelism Evaluation

不要只报：

```text
总耗时下降
```

还要报告：

```text
Critical Path
Total Compute
Wasted Speculative Work
Synchronization Wait
```

---

#### 6.1.122 Oracle Decomposition

一个很有价值的实验：

```text
直接给系统正确任务分解
```

如果显著提升：

```text
bottleneck = decomposition
```

而不是 local agent ability。

---

#### 6.1.123 Oracle Delegation

直接告诉 Parent：

```text
哪个子任务交给哪个 Agent
```

可测：

```text
Delegation / Routing Upper Bound
```

---

#### 6.1.124 Oracle Communication

直接给下游 Agent：

```text
完整正确的 minimal handoff
```

可测：

```text
Communication Loss
```

---

#### 6.1.125 Oracle Aggregation

把所有正确子结果直接交给理想 Aggregator。

若提升明显：

```text
bottleneck = aggregation / arbitration
```

---

#### 6.1.126 Agent-count Ablation

例如：

```text
1 Agent
2 Agents
4 Agents
8 Agents
```

保持总预算尽量可比，观察：

```text
Quality
Cost
Latency
Coordination Errors
```

很可能出现：

```text
先升后降
```

而不是单调增加。

---

#### 6.1.127 Role Ablation

例如移除：

```text
Verifier
```

看：

```text
Task Success
False-success Rate
Cost
```

可以判断该角色是否真正贡献价值。

---

#### 6.1.128 Communication Ablation

比较：

```text
Full Transcript
vs
Structured Handoff
vs
Minimal Handoff
```

可以直接评估：

```text
Communication Compression Trade-off
```

---

#### 6.1.129 Shared-context Ablation

比较：

```text
All Agents Share Everything
vs
Private Context + Explicit Handoff
```

可以评估 Context Isolation 的真实贡献。

---

#### 6.1.130 Permission Isolation Ablation

比较：

```text
All Agents Full Permission
vs
Role-scoped Permission
```

观察：

```text
Task Success
Unauthorized Actions
Harm Rate
```

---

#### 6.1.131 Coding Agent 示例

单 Agent：

```text
Issue
↓
Read Code
↓
Patch
↓
Test
↓
Review Own Diff
```

Multi-Agent：

```text
Coordinator
├── Investigator
├── Implementer
└── Verifier
```

只有当：

- Investigator 可独立探索；
- Implementer 保持更窄 Context；
- Verifier 独立测试；
- 三者 Handoff 清晰；

这种拆分才值得。

---

#### 6.1.132 Research Agent 示例

可以拆：

```text
Source Discovery Agent
Evidence Extraction Agent
Synthesis Agent
Fact-check Agent
```

但如果问题只是：

```text
查一个事实
```

这种结构就是过度设计。

---

#### 6.1.133 Browser Agent 示例

一种安全拆分：

```text
Navigator
→ browser read / inspect

Executor
→ effectful click / submit
```

Navigator 可以处理大量不可信页面内容，而 Executor 只接受结构化 Action Proposal。

这比单纯：

```text
“你是安全执行 Agent”
```

更接近真实安全边界。

---

#### 6.1.134 Finance Agent 示例

```text
Invoice Reader
→ read-only

Policy Checker
→ business rules

Payment Executor
→ narrow payment credential

Auditor
→ receipt verification
```

这是 Multi-Agent 最合理的一类应用：

```text
Separation of Duties
```

有真实安全价值。

---

#### 6.1.135 Customer Support 示例

并不是所有客服都要：

```text
Router → Billing Agent → Product Agent → Refund Agent
```

简单问题可能一个 Agent + Tools 更好。

只有在：

```text
policy
data access
authority
specialization
```

明显不同的域，拆分才更合理。

---

#### 6.1.136 Long-running Project Agent 示例

大型任务可以采用：

```text
Project Coordinator
├── Research
├── Build
├── Test
└── Review
```

但必须有共享：

```text
Project State
Artifact Registry
Decision Log
Effect Ledger
```

否则长期协作会逐渐失真。

---

#### 6.1.137 Multi-Agent 与 Harness

Harness 决定：

```text
who may spawn whom
what context to pass
what tools each agent sees
what budgets they get
what permissions they inherit
how results are verified
when delegation stops
```

所以：

> **Multi-Agent 不是脱离 Harness 独立存在的能力。**

---

#### 6.1.138 Multi-Agent 与 Runtime

Runtime 负责：

```text
Agent Process / Task Lifecycle
State Persistence
Messaging
Scheduling
Concurrency
Checkpoint
Cancellation
Timeout
Resource Isolation
Credential Injection
```

因此：

```text
Harness
= coordination policy

Runtime
= coordination substrate
```

---

#### 6.1.139 Multi-Agent 与 Capability Discovery

一个 Agent 本身也可以被视作某类 Capability：

```text
Research Capability
Coding Capability
Verification Capability
```

因此 Parent 可以通过：

```text
Agent Registry
```

发现可用 Subagents。

这和 Chapter 5 的 Capability Discovery 有自然连接。

---

#### 6.1.140 但 Agent Capability 比 Tool 更复杂

因为 Agent 还拥有：

```text
Autonomy
State
Budget
Tools
Permissions
Failure Modes
```

所以 Agent Discovery 不能只看：

```text
name + schema
```

还要看：

```text
role
trust
cost
latency
authority
context needs
```

---

#### 6.1.141 Multi-Agent 与 Memory

需要区分：

```text
Private Memory
Shared Memory
Transferred Memory
```

原则：

> **Memory 不应因为 Agent 协作而自动全局共享。**

---

#### 6.1.142 Multi-Agent 与 Context Engineering

每个 Agent 应有自己的：

```text
Context Projection
```

而不是：

```text
global transcript
复制给所有 agent
```

因此 Multi-Agent 的 Context Engineering 本质上变成：

```text
Per-agent Context Policy
+
Cross-agent Handoff Policy
```

---

#### 6.1.143 Multi-Agent 与 Persistence

Long-running Multi-Agent 需要持久化：

```text
Agent Graph
Agent State
Delegation State
Pending Messages
Artifact Ownership
Effect History
Budget
```

否则系统 crash 后无法正确恢复协作拓扑。

---

#### 6.1.144 Multi-Agent Resume

Resume 时不能只恢复：

```text
Parent State
```

还要判断：

```text
哪些 Subagent 完成？
哪些仍 pending？
哪些 effect unknown？
哪些 permission 已变化？
```

所以 Multi-Agent Durable Execution 更复杂。

---

#### 6.1.145 Multi-Agent Security 总原则

可以概括：

```text
Delegated Authority
≤ Parent Authority

Shared Context
≤ Necessary Context

Shared Secrets
≤ Necessary Secrets

Cross-Agent Effects
≤ Authorized Effects
```

---

#### 6.1.146 Multi-Agent 最危险的反模式：全共享

如果所有 Agent 都共享：

```text
all context
all tools
all credentials
all memory
```

那么所谓 Multi-Agent：

```text
没有真正 isolation
却增加 coordination complexity
```

通常是最差组合。

---

#### 6.1.147 第二个反模式：角色爆炸

为每个小动作创建一个 Agent：

```text
FileReaderAgent
JSONParserAgent
FormatterAgent
```

这些更适合：

```text
Tool / Function / Workflow Node
```

不是 Agent。

---

#### 6.1.148 第三个反模式：无限专家化

过度 specialization 会导致：

```text
handoff count ↑
communication loss ↑
latency ↑
coordination ↑
```

因此存在最佳粒度，而不是越细越好。

---

#### 6.1.149 第四个反模式：Manager of Managers

结构：

```text
CEO Agent
↓
Director Agent
↓
Manager Agent
↓
Worker Agent
```

如果层级没有真实：

```text
authority / context / ownership
```

只是多加几轮 LLM。

---

#### 6.1.150 第五个反模式：用 Agent 解决 Deterministic Problem

例如：

```text
JSON validation
schema conversion
sorting
file copying
```

应优先：

```text
deterministic code
```

而不是创建 Agent。

---

#### 6.1.151 第六个反模式：Verifier 只是重复生成

如果 Verifier：

```text
重新回答原题
```

而不是：

```text
检查具体 claim / evidence / invariant
```

那常常不是 Verification，只是第二次 generation。

---

#### 6.1.152 第七个反模式：Consensus = Truth

多个 Agent 都同意：

```text
并不能证明正确
```

尤其在 correlated error 下。

真正应该看：

```text
Evidence
Independent Checks
Source Authority
```

---

#### 6.1.153 第八个反模式：Subagent 权限继承过宽

```text
Parent has admin
↓
all subagents inherit admin
```

会把攻击面指数放大。

应该：

```text
per-task scoped capability token
```

更合理。

---

#### 6.1.154 第九个反模式：聊天式协作替代状态管理

多个 Agent 一直：

```text
A: 我做了 X
B: 好的，我做 Y
C: 我觉得 Z
```

但没有：

```text
canonical task state
```

长期一定漂移。

---

#### 6.1.155 第十个反模式：结果聚合没有证据

Aggregator 只看到：

```text
Agent A says X
Agent B says Y
```

但看不到：

```text
source / artifact / test / citation
```

最终只能做意见投票。

因此：

> **Handoff 应尽量传 Evidence，不只传 Conclusion。**

---

#### 6.1.156 Multi-Agent 的设计顺序

推荐：

```text
1. Define System Goal
2. Build Strong Single-Agent Baseline
3. Identify Bottleneck
4. Choose Split Dimension
5. Define Agent Contract
6. Define Shared / Private State
7. Define Authority
8. Define Handoff
9. Define Failure / Recovery
10. Evaluate Net Benefit
```

而不是：

```text
先画 8 个 Agent
再想他们干什么
```

---

#### 6.1.157 Split Dimension

常见拆分维度：

```text
By Expertise
By Context
By Tool / Capability
By Permission
By Task Phase
By Environment
By Risk
By Verification Role
By Ownership
```

不同维度可以组合，但不要混乱。

---

#### 6.1.158 一个 Agent Contract 应至少包含

```text
Identity / Role
Goal
Input Contract
Output Contract
Available Tools
Permission Scope
Context Scope
Memory Scope
Budget
Success Criteria
Failure Semantics
Escalation Path
```

这是后续 Multi-Agent 所有章节的基础。

---

#### 6.1.159 Multi-Agent Failure 需要 Local + Global Status

例如：

```text
Research Agent = SUCCESS
Coding Agent = FAILURE
Verifier Agent = NOT_RUN
System = FAILURE
```

不能只记录：

```text
some agent failed
```

---

#### 6.1.160 Partial Success

复杂系统可能：

```text
A success
B success
C failure
```

此时需要决定：

```text
retry C?
replan?
return partial result?
human escalation?
```

因此 Partial Success 是一等状态。

---

#### 6.1.161 Multi-Agent Deadlock

例如：

```text
A waits for B
B waits for C
C waits for A
```

这是真正的：

```text
coordination deadlock
```

需要：

```text
dependency graph
timeout
deadlock detection
```

---

#### 6.1.162 Livelock

Agent 都在行动：

```text
A asks B
B rejects
A reformulates
B rejects
```

系统并未停止，但没有进展。

因此要区分：

```text
Activity
≠ Progress
```

---

#### 6.1.163 No-progress Detection

可以监控：

```text
new evidence?
new artifact?
state changed?
uncertainty reduced?
```

如果多轮没有变化：

```text
stop / replan / escalate
```

---

#### 6.1.164 Multi-Agent Race Condition

例如两个 Agent 同时：

```text
edit same file
```

会产生：

```text
lost update
merge conflict
```

因此需要：

```text
resource ownership
locking
optimistic concurrency
```

---

#### 6.1.165 Resource Ownership

可以明确：

```text
Agent A owns file X
Agent B owns file Y
```

或：

```text
shared resource requires coordinator
```

这样可以减少冲突。

---

#### 6.1.166 Multi-Agent Transaction Boundary

多个 Agent 联合完成一个高风险操作时：

```text
A prepare
B validate
C commit
```

需要明确：

```text
transaction boundary
commit point
compensation
```

不能只靠消息顺序。

---

#### 6.1.167 Message Delivery Semantics

Agent 通信可能是：

```text
at-most-once
at-least-once
effectively-once
```

重复消息可能导致：

```text
duplicate delegation
duplicate effect
```

因此消息也需要：

```text
message_id
idempotency
```

---

#### 6.1.168 Agent Identity

每个 Agent 应有稳定：

```text
agent_id
role
owner
version
trust tier
```

这样 Audit 才有意义。

---

#### 6.1.169 Agent Versioning

Agent 的：

```text
prompt
skills
tools
model
policy
```

都会变化。

因此一次任务应该能回答：

```text
哪个版本的 Agent 做了这个决定？
```

---

#### 6.1.170 Agent Drift

运行很久以后：

```text
Agent A version 2
Agent B version 5
```

可能产生 Contract 不兼容。

所以长期 Multi-Agent 系统还要考虑：

```text
Compatibility
```

---

#### 6.1.171 Dynamic Agent Discovery

系统不一定预先知道所有 Agent。

可能从 Registry 动态发现：

```text
Research Agent
Translation Agent
Compliance Agent
```

但 Discovery 仍需要：

```text
Trust
Permission
Compatibility
Availability
```

和 Capability Discovery 完全类似。

---

#### 6.1.172 Agent Registry

可以包含：

```text
Agent ID
Capabilities
Role
Input / Output Contract
Trust Tier
Cost
Latency
Availability
Permission Requirements
Version
```

这为后续 Routing 打基础。

---

#### 6.1.173 Agent Selection

如果多个 Agent 都能做：

```text
research
```

Parent 还要选择：

```text
which agent?
```

这本质上是：

```text
Agent Routing
```

---

#### 6.1.174 Agent Routing Utility

可以概念化：

```text
Utility(agent)
=
Capability Fit
× Reliability
× Availability
− Cost
− Latency
− Risk
```

与 Capability Routing 类似。

---

#### 6.1.175 Multi-Agent 与 Scheduling

当 Subagent 多时：

```text
CPU / GPU
Model Quota
Tool Quota
Concurrency
```

都需要调度。

因此 Multi-Agent 不只是 Prompt Engineering，也进入：

```text
Scheduler / Runtime Engineering
```

---

#### 6.1.176 Concurrency Limit

无限并发会导致：

```text
rate limits
cost spikes
resource contention
```

因此：

```text
max_parallel_agents
```

是重要 Runtime 参数。

---

#### 6.1.177 Backpressure

如果下游 Agent 处理不过来：

```text
incoming tasks > service capacity
```

需要：

```text
queue
backpressure
load shedding
```

这些都不是 LLM Prompt 能解决的。

---

#### 6.1.178 Multi-Agent 与 Model Context Protocol 的交点

MCP 可以让不同 Agent 共享标准化 Capability Access。

例如：

```text
Research Agent ─┐
Coder Agent ────┼→ MCP GitHub Server
Verifier Agent ─┘
```

但它们是否都应该看到同样 Tool，需要 Harness 决定。

---

#### 6.1.179 Multi-Agent 与 A2A 的交点

若 Agent 跨进程 / 跨组织 / 跨平台：

```text
Agent A
↔ protocol
Agent B
```

就需要讨论：

```text
identity
discovery
message contract
task lifecycle
status
artifact exchange
```

这会在后面的 A2A 小节展开。

---

#### 6.1.180 Multi-Agent 与 RSI

系统可以通过经验发现：

```text
某类任务总适合拆成两个角色
```

进而修改：

```text
routing
delegation policy
skill library
agent topology
```

这可能成为 Harness RSI 的优化对象。

---

#### 6.1.181 但自增 Agent 数量不等于 Self-improvement

如果系统只是：

```text
失败
↓
再 spawn 3 个 Agent
```

没有稳定学习和未来更新，就不是 RSI。

---

#### 6.1.182 Multi-Agent 评测应控制计算预算

至少报告：

```text
Total Model Calls
Total Input Tokens
Total Output Tokens
Tool Calls
Wall-clock Latency
Monetary Cost
```

否则无法解释收益。

---

#### 6.1.183 Outcome + Process 双重评价

Outcome：

```text
Task Success
```

Process：

```text
Correct Delegation
Correct Handoff
No Unauthorized Action
No Duplicate Work
Correct Verification
```

两者都需要。

---

#### 6.1.184 Reliability Metrics

可包含：

```text
Handoff Failure Rate
Coordination Failure Rate
Deadlock Rate
Duplicate Work Rate
False-success Rate
Recovery Rate
```

---

#### 6.1.185 Safety Metrics

可包含：

```text
Privilege Escalation
Cross-agent Leakage
Unauthorized Delegation
Unsafe Capability Exposure
Shared-memory Poisoning
```

---

#### 6.1.186 Efficiency Metrics

可包含：

```text
Task Success / Dollar
Task Success / Token
Task Success / Second
Useful Work Ratio
Coordination Overhead Ratio
```

---

#### 6.1.187 Coordination Overhead Ratio

可概念定义：

\[
R_{coord} = \frac{C_{communication}+C_{coordination}}{C_{total}}
\]

如果这个比例极高，而质量没有明显提升，说明拆分可能过度。

---

#### 6.1.188 Useful Work Ratio

可以看：

```text
最终真正被采用的工作
/
所有 Agent 产生的工作
```

大量 Speculative Work 被丢弃，说明并行策略可能低效。

---

#### 6.1.189 Diversity Metrics

如果使用 Committee / Debate，可以测：

```text
Answer Diversity
Evidence Diversity
Reasoning-path Diversity
```

而不是只数 Agent 数量。

---

#### 6.1.190 Correlation-aware Evaluation

三个 Agent 都答错同一个错误答案，比三个 Agent 分别出不同错误，说明：

```text
error correlation high
```

对 Ensemble / Debate 尤其重要。

---

#### 6.1.191 Multi-Agent Robustness Test

可以注入：

```text
one agent unavailable
one tool unavailable
one message delayed
one agent outputs wrong result
```

观察系统：

```text
fallback
recovery
containment
```

能力。

---

#### 6.1.192 Adversarial Agent Test

模拟一个 Subagent：

```text
returns malicious instructions
asks for extra permissions
claims false success
```

测试 Parent 是否盲信。

---

#### 6.1.193 Slow Agent Test

某个 Agent 延迟很高：

```text
straggler
```

系统是否：

```text
wait forever?
timeout?
use partial results?
launch fallback?
```

这是并行系统典型问题。

---

#### 6.1.194 Duplicate Agent Test

两个 Agent 被意外分配同一个 effectful task。

系统是否能通过：

```text
idempotency
ownership
effect ledger
```

避免重复执行？

---

#### 6.1.195 Stale Handoff Test

Agent A 交给 B 的 State 已过期。

B 是否：

```text
revalidate
```

而不是直接执行？

---

#### 6.1.196 Permission Revocation Test

Parent 委派后权限被撤销。

Subagent 是否还能继续？

正确系统应在 effectful action 前重新验证：

```text
current authority
```

---

#### 6.1.197 Crash / Resume Test

系统中途 crash。

恢复后：

```text
Agent topology
pending tasks
messages
committed effects
budgets
```

是否正确恢复？

---

#### 6.1.198 Minimal Working Example

任务：

```text
分析一个 PR 并决定是否适合合并
```

Single Agent：

```text
read diff
run tests
review
answer
```

若需要更强独立验证，可以拆：

```text
Reviewer Agent
→ inspect diff
→ identify risks

Verifier Agent
→ run tests
→ independently check claims

Coordinator
→ combine evidence
```

但如果 PR 很小，单 Agent 可能更优。

---

#### 6.1.199 什么时候值得从 Single Agent 升级？

出现以下信号之一：

```text
Context repeatedly overloaded
Permission boundaries conflict
Independent verification materially helps
Work is naturally parallel
Different models/tools needed
One role becomes a failure bottleneck
```

再考虑拆分。

---

#### 6.1.200 什么时候应该从 Multi-Agent 降级？

如果发现：

```text
handoff dominates cost
roles heavily overlap
agents share almost all context
duplicate work high
latency unacceptable
quality gain small
```

应考虑合并。

---

#### 6.1.201 Multi-Agent Architecture 需要持续审计

随着：

```text
model capability improves
tool quality improves
context window expands
skills mature
```

原本需要多个 Agent 的任务，未来可能一个 Agent 就能可靠完成。

因此：

> **Agent Boundary 不是永久的。**

---

#### 6.1.202 Model Improvement 会改变最优 Agent Count

更强模型可能：

```text
reduce need for specialization
reduce coordination overhead
```

也可能：

```text
enable more capable supervisor
```

所以 Multi-Agent 架构必须随 Model 能力重新评估。

---

#### 6.1.203 Better Harness 也可能替代 Multi-Agent

有时问题看似需要多个 Agent，实际上只是单 Agent 缺少：

```text
state management
context policy
tool filtering
verification
```

补强 Harness 后可能无需拆分。

因此：

```text
Bad Single-Agent Harness
→ Multi-Agent
```

不是合理默认路径。

---

#### 6.1.204 Better Skills 也可能替代 Multi-Agent

一个复杂流程如果已经成熟为：

```text
well-defined Skill
```

可能不再需要独立 Agent。

例如：

```text
code_review skill
```

可以被一个 Agent 稳定执行。

---

#### 6.1.205 Better Tool Contracts 也可能减少 Agent 数量

如果某个 Subagent 只是包装复杂 API，可能更适合直接做成：

```text
high-level Tool
```

而不是长期维护一个 Agent。

---

#### 6.1.206 Multi-Agent 是一种架构选择，不是能力标签

不能简单说：

```text
“我们的产品支持 Multi-Agent，
所以比 Single-Agent 产品强。”
```

真正需要看：

```text
是否有合理边界
是否提升任务结果
是否控制协调成本
是否提高安全与可靠性
```

---

#### 6.1.207 Multi-Agent 的核心设计问题

最终可以浓缩成五问：

```text
1. Why split?
2. Where is the boundary?
3. What is shared?
4. Who owns the decision?
5. How do we know splitting helped?
```

如果这五问答不清，系统大概率只是：

```text
more prompts
```

而不是成熟 Multi-Agent Architecture。

---

#### 6.1.208 Failure Modes

常见失败模式包括：

1. 为复杂而复杂，缺少明确拆分理由；
2. Agent 名字不同，但 Context / Tool / Permission 完全相同；
3. 把 deterministic node 包装成 Agent；
4. Subagent 继承过宽权限；
5. 所有 Agent 共享全部 Context；
6. Shared Transcript 代替 Shared State；
7. Goal decomposition 漏掉关键约束；
8. Handoff 丢失 evidence / uncertainty / provenance；
9. Agent 之间重复工作；
10. Parallelism 产生大量 wasted work；
11. Supervisor 变成 context bottleneck；
12. Peer-to-peer 消息爆炸；
13. 多个 Agent 错误高度相关；
14. Consensus 被误当成 Truth；
15. Verifier 只是重复生成；
16. Conflicting conclusions 无仲裁规则；
17. Agent-to-Agent 消息被盲信；
18. Shared Memory 被污染；
19. Resource ownership 不清；
20. 两个 Agent 同时修改同一资源；
21. Deadlock；
22. Livelock；
23. Delegation 深度无限增长；
24. Agent spawn 无系统级 Budget；
25. Retry 在多个层级叠加；
26. Handoff 未包含已发生 Side Effects；
27. Crash 后只恢复 Parent，不恢复协作拓扑；
28. Agent Version 不兼容；
29. 权限撤销后 Subagent 仍继续执行；
30. 多 Agent 提升仅来自额外计算预算；
31. 没有强 Single-Agent Baseline；
32. 只报 Task Success，不报 Cost / Latency；
33. 局部 Agent 全成功，但 Global Goal 失败；
34. 无法定位哪一个 Agent / Handoff 导致失败；
35. 人类组织架构被机械复制成 Agent 架构；
36. Agent 数量增长但信息/权限边界没有变化；
37. Communication 成为主要 Token 成本；
38. Artifact 无 ownership / version；
39. 恶意 Subagent 请求权限升级；
40. Agent Boundary 长期不重新审计。

---

#### 6.1.209 工程原则

1. **Single Agent First**：先有强单 Agent 基线，再拆。
2. **Every Agent Needs a Reason**：每个 Agent 必须对应明确瓶颈。
3. **Split by Real Boundary**：按 Context / Capability / Permission / Trust 等真实边界拆。
4. **High Cohesion, Low Coupling**：角色内部聚合，角色间低耦合。
5. **Contract before Conversation**：先定义 Handoff Contract，再让 Agent 聊。
6. **State before Transcript**：共享结构化 State，不靠聊天记录维持一致性。
7. **Evidence over Opinion**：跨 Agent 传 Evidence，不只传 Conclusion。
8. **Least Privilege Delegation**：委派权限最小化。
9. **Authority ≠ Autonomy**：能自主决定不等于拥有更大权限。
10. **Private by Default**：Context / Memory 默认私有，按需共享。
11. **Explicit Ownership**：每个 Decision / Artifact / Resource 要有 owner。
12. **Bound Delegation Depth**：限制 Subagent 深度与数量。
13. **System-level Budget**：预算必须跨 Agent 统一核算。
14. **Progress ≠ Activity**：检测无进展循环。
15. **Independent Verification Needs Real Independence**。
16. **Coordinator Is Not Truth Oracle**。
17. **Parallelism Optimizes Critical Path, Not Necessarily Cost**。
18. **Resume Requires Topology + Effects + Pending Work**。
19. **Measure Net Benefit**：同时统计 rescue 与 degradation。
20. **Budget-match Baselines**：控制额外 compute。
21. **Evaluate Communication Separately**。
22. **Evaluate Coordination Separately**。
23. **Use Oracle Ablations to Localize Bottlenecks**。
24. **Prefer Artifacts over Endless Agent Chat**。
25. **Re-audit Boundaries as Models/Harness/Skills Improve**。
26. **Minimal Sufficient Agent Count**。

---

#### 6.1.210 面试掌握

**Q1：什么是 Multi-Agent？**  
多个具有相对独立 Goal / State / Context / Decision Loop / Capability 的 Agent 通过协调完成系统目标。

**Q2：多个 LLM Call 就算 Multi-Agent 吗？**  
不算。多次调用可能只是 Ensemble、Self-Consistency 或 Workflow。

**Q3：Agent + 很多 Tool 是 Multi-Agent 吗？**  
不是，Tool 没有独立 Decision Loop。

**Q4：为什么要 Multi-Agent？**  
主要为了 specialization、context isolation、parallelism、authority isolation、independent verification、fault containment 等。

**Q5：为什么不能默认拆 Multi-Agent？**  
因为会增加 communication、coordination、state synchronization、failure surface、latency 和 cost。

**Q6：Single Agent 和 Multi-Agent 怎么选？**  
先做强 Single-Agent Baseline；只有明确存在可通过独立 Agent 边界解决的瓶颈才拆。

**Q7：Subagent 和 Tool 区别？**  
Tool 执行动作；Subagent 拥有独立决策循环和状态。

**Q8：Multi-Agent 和 Workflow 区别？**  
Workflow 控制流通常开发者预定义；Multi-Agent 中部分控制与行动选择由 Agent 自主决定。

**Q9：Multi-Agent 和 Ensemble 区别？**  
Ensemble 多成员通常解同一问题再聚合；Multi-Agent 更强调分工、状态和交互。

**Q10：Multi-Agent 和 Multi-model 区别？**  
Agent 是决策主体划分；Model 是模型资源选择。二者正交。

**Q11：Context Isolation 为什么重要？**  
可以减少 context pollution，并让每个 Agent 只看到当前职责所需的信息。

**Q12：为什么 Multi-Agent 可以提升安全性？**  
可通过权限隔离、separation of duties、fault containment 缩小 blast radius。

**Q13：角色分离就等于安全隔离吗？**  
不等于，必须有 Runtime / Credential / Permission 层真实隔离。

**Q14：Verifier Agent 为什么可能比自检更有效？**  
可以拥有独立 Context、Evidence、Objective，降低 correlated error。

**Q15：多个 Agent 都同意就一定对吗？**  
不一定，错误可能高度相关。

**Q16：怎么判断 Agent 拆得太细？**  
handoff 很多、上下文高度共享、职责重叠、communication cost 高且收益低。

**Q17：怎么判断应该拆？**  
出现明显独立 Context / Capability / Permission / Trust / Parallelism / Verification 边界。

**Q18：Multi-Agent 最大的工程难点是什么？**  
通常不是“让 Agent 互相说话”，而是 State、Ownership、Authority、Handoff、Recovery 与 Evaluation。

**Q19：Shared State 和 Shared Transcript 有什么区别？**  
Shared State 是结构化权威任务状态；Transcript 只是历史消息。

**Q20：为什么 Agent Handoff 需要 Contract？**  
否则容易丢失约束、证据、不确定性、版本和 side-effect 状态。

**Q21：Multi-Agent 如何控制权限？**  
Delegated Authority 必须是 Parent Authority 的子集，并按任务最小化。

**Q22：为什么 Agent Spawn 也要预算？**  
Spawn 会产生模型、工具、网络、权限与协调成本。

**Q23：Multi-Agent 如何评测？**  
Task Success + Cost/Latency + Decomposition/Delegation/Communication/Coordination/Safety 等过程指标。

**Q24：为什么必须做 Budget-matched Baseline？**  
否则性能提升可能只是因为用了更多 Token / Calls，而不是架构更好。

**Q25：什么是 Oracle Decomposition？**  
直接提供正确任务分解，用于测 decomposition bottleneck 的上界。

**Q26：什么是 Minimal Sufficient Agent Count？**  
完成任务所需 specialization / isolation / coordination 的最少 Agent 数量。

---

#### 6.1.211 一句话总结

> **Multi-Agent 的价值不在“多个 Agent 一起想”，而在于把一个系统中真正不同的 Context、Capability、Authority、Failure Domain 与 Decision Ownership 划成清晰边界；只有当这种分解带来的 specialization、parallelism、isolation 与 independent verification 收益大于 communication、coordination、consistency 和成本开销时，Multi-Agent 才是更好的架构。**

---

#### 6.1.212 参考资料

1. Wooldridge, M. *An Introduction to MultiAgent Systems*. Wiley, 2009.
2. Shoham, Y., Leyton-Brown, K. *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations*. Cambridge University Press, 2008.
3. Stone, P., Veloso, M. “Multiagent Systems: A Survey from a Machine Learning Perspective.” *Autonomous Robots*, 2000.
4. Wu, Q. et al. “AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.” arXiv:2308.08155, 2023.
5. Li, G. et al. “CAMEL: Communicative Agents for Mind Exploration of Large Scale Language Model Society.” NeurIPS, 2023.
6. Hong, S. et al. “MetaGPT: Meta Programming for Multi-Agent Collaborative Framework.” ICLR, 2024.
7. Park, J. S. et al. “Generative Agents: Interactive Simulacra of Human Behavior.” UIST, 2023.
8. Du, Y. et al. “Improving Factuality and Reasoning in Language Models through Multiagent Debate.” ICML, 2024.
9. Chan, C.-M. et al. “ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate.” ICLR, 2024.
10. Ouyang, S. et al. “A Survey on Multi-Agent Large Language Model Systems.” 2024.
11. Anthropic. *Building Effective Agents*. 关于简单架构优先、工作流与 Agent 选择的工程经验。
12. Google SRE. *Site Reliability Engineering*. 关于 fault isolation、backpressure、reliability 与 distributed systems operational principles。
13. NIST. *AI Risk Management Framework*. 关于治理、风险与责任边界。
14. OWASP. *Top 10 for LLM Applications*. 关于 prompt injection、excessive agency 与 tool/agent security 风险。
