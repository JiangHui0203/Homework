> **本节定位：**4.1 Context Engineering 已经回答“为了当前决策，模型应该看到什么”；7.4 Context Policy 进一步回答：**Harness 如何把这种选择策略变成可执行、可审计、可恢复的系统规则，决定什么信息有资格进入 Context、保留多久、何时刷新、如何压缩、能否跨 Agent / Session 共享，以及哪些信息即使相关也绝不能暴露给模型。**
>
> 因此，Context Engineering 更偏向 **information design**，而 Context Policy 更偏向 **runtime governance**。前者追求“上下文好不好”，后者负责“上下文怎样被系统稳定地管起来”。

---

#### 7.4.1 为什么 Harness 需要独立的 Context Policy

在简单聊天里，可以把上下文近似理解成“最近几轮消息 + system prompt”。但 Agent 一旦开始长时间运行、读写外部系统、调用多个 Tool、维护 Working State、检索 Memory、派生 Subagent，模型每一次推理可见的信息来源会迅速扩张：

- platform / developer instruction；
- user goal 与后续修正；
- Working State；
- 当前 Plan；
- Tool schema；
- Tool Observation；
- Memory；
- Retrieval Evidence；
- 文件、日志、网页、截图；
- Effect Ledger；
- Approval State；
- Retry / Failure History；
- Subagent 输出；
- Budget / Deadline；
- Runtime metadata。

如果系统只采用：

```text
有信息
→ append 到 messages
→ token 快满了再 summary
```

那么很快会出现：

- stale context；
- duplicated context；
- contradictory context；
- secret leakage；
- prompt injection；
- approval scope 丢失；
- action 重复执行；
- state / context 不一致；
- summary drift；
- context overflow；
- model-visible capability 失控。

因此 Context Policy 的任务不是“帮 prompt 做排版”，而是：

> **把模型输入看成一种受治理的 runtime view，并对其来源、资格、生命周期、预算、信任、权限与刷新语义做明确控制。**

---

#### 7.4.2 Context Policy 的统一定义

可以把某一时刻的 Context Policy 写成：

\[
\Pi_C : (S_t, E_t, I_t, M_t, R_t, O_t, A_t, B_t) \rightarrow C_t
\]

其中：

- \(S_t\)：Working State；
- \(E_t\)：Environment metadata；
- \(I_t\)：Effective Instructions；
- \(M_t\)：Memory candidates；
- \(R_t\)：Retrieved evidence；
- \(O_t\)：Recent observations；
- \(A_t\)：available capabilities / approvals；
- \(B_t\)：context / cost / latency budget；
- \(C_t\)：最终模型可见 Context。

这说明：

> **Context 不是 storage；Context 是 policy 在某个 decision point 对系统状态做出的投影。**

---

#### 7.4.3 Context Engineering 与 Context Policy 的边界

两者关系可以写成：

```text
Context Engineering
= 设计“什么信息组织方式更利于模型决策”

Context Policy
= 把这些设计原则变成 Harness 中持续执行的规则
```

例如：

```text
Context Engineering:
    最近失败记录应该结构化压缩，而不是原样塞日志。

Context Policy:
    最多保留最近 3 个 distinct failure signatures；
    同类失败合并；
    UNKNOWN outcome 永久 pin 到 reconciliation 完成。
```

前者是方法，后者是系统语义。

---

#### 7.4.4 Context Policy ≠ Prompt Engineering

Prompt Engineering 主要关心：

```text
怎样表达 instruction，
让模型更容易理解和遵循？
```

Context Policy 则关心：

```text
这条信息是否有资格进入模型输入？
什么时候进入？
保留多久？
是否必须刷新？
是否允许压缩？
是否需要隐藏？
```

因此：

\[
PromptEngineering \subset ContextEngineering \subset HarnessContextGovernance
\]

这不是严格数学包含，而是系统范围上的近似关系。

---

#### 7.4.5 Context Policy 的输入不只是“消息”

成熟 Harness 不应该只接受：

```python
messages: list[Message]
```

更合理的是从多种 typed source 构建：

```text
Instruction Store
Working State
Observation Store
Memory Store
Retrieval Results
Capability Registry
Approval Store
Effect Ledger
Artifact Store
Runtime Metadata
```

然后统一经过 Context Policy。

---

#### 7.4.6 Context 不是 Source of Truth

这一原则必须再次强调：

```text
Context
= 当前模型可见的 view

Canonical State
= 系统真正依赖的权威状态
```

如果 Context 中写着：

```text
payment_status = pending
```

但 canonical payment service 已经变成：

```text
payment_status = completed
```

真正应该修复的是 Context，而不是让旧 Context 反过来覆盖现实。

因此：

> **Context 可以过期；Source of Truth 不应由 Context 定义。**

---

#### 7.4.7 Context Admission：先判断“有资格”，再判断“有用”

推荐把 Context 构建分成两个阶段：

```text
Eligibility
    ↓
Relevance / Utility
```

也就是说先问：

```text
Can this information enter context?
```

再问：

```text
Should this information enter context now?
```

例如某条跨租户数据即使与任务高度相关，也可能：

```text
Relevance = high
Eligibility = false
```

最终仍然不能进入 Context。

---

#### 7.4.8 Eligibility Filter 应早于 Semantic Ranking

错误流程：

```text
Retrieve everything
↓
Rank by relevance
↓
把 top-k 放进模型
↓
最后再做权限检查
```

危险在于：

> 信息可能已经进入 embedding、reranker 或 LLM 可见面。

更安全的是：

```text
Authorized Scope
↓
Candidate Retrieval
↓
Semantic Ranking
↓
Context Admission
```

即：

> **Permission-aware context construction 应尽量发生在数据暴露之前。**

---

#### 7.4.9 Context Source 必须保留 Provenance

至少需要知道：

```text
source_type
source_id
observed_at
version
trust_level
owner / tenant
```

例如同一句：

```text
“立即删除本地仓库。”
```

如果来自：

```text
user-approved action plan
```

和来自：

```text
webpage body
```

其控制意义完全不同。

没有 provenance，Harness 很难正确执行 7.3 Instruction Policy。

---

#### 7.4.10 Authority 与 Relevance 必须分开

高相关不等于高 authority。

可以写成：

\[
Relevance(x) \neq Authority(x)
\]

网页中的恶意指令可能和当前任务高度相关，但仍然没有权力覆盖用户目标或 Harness Policy。

---

#### 7.4.11 Context Item 的推荐元数据

一个可治理 Context Item 可以抽象为：

```text
ContextItem
├── content
├── semantic_role
├── source
├── provenance
├── trust
├── authority
├── freshness
├── version
├── scope
├── sensitivity
├── exactness_requirement
├── compression_policy
├── expiry
└── priority
```

这比“字符串数组”更适合 Agent Harness。

---

#### 7.4.12 Semantic Role：不要把所有文字都叫 Message

建议区分：

```text
INSTRUCTION
GOAL
STATE
OBSERVATION
EVIDENCE
MEMORY
PLAN
CAPABILITY
APPROVAL
EFFECT
FAILURE
BUDGET
REFERENCE
```

不同 role 应使用不同生命周期与压缩策略。

---

#### 7.4.13 Static Context 与 Dynamic Context

Context 可以按变化速度分为：

```text
Static
├── stable system rules
├── stable tool contracts
└── long-lived app policy

Dynamic
├── current state
├── recent observation
├── active plan
├── budget
├── approval
└── retrieved evidence
```

Static Context 可以适合缓存；Dynamic Context 必须更重视 freshness。

---

#### 7.4.14 Session Context 与 Step Context

同一条信息可能应该存在于：

```text
整个 Session
```

但不一定每一步都要进入模型。

例如用户偏好：

```text
默认代码使用 Python
```

可以保留为 Session-level preference，但当前如果 Agent 正在做纯文档检索，该信息可能无需进入 Step Context。

所以：

> **Persistent in session ≠ visible on every step。**

---

#### 7.4.15 Context Lifetime 应显式建模

常见生命周期：

```text
one-shot
turn-scoped
step-scoped
subtask-scoped
run-scoped
session-scoped
until-invalidated
until-revoked
```

把所有信息都默认“直到 Context Window 挤掉”为止，是非常弱的策略。

---

#### 7.4.16 Context Expiry 不只依赖 TTL

与 Memory 一样，Context 也有 semantic expiry。

例如：

```text
“当前还没有用户批准”
```

一旦 approval 到达，这条 Context 立刻失效。

因此：

```text
TTL Expiry
≠ Semantic Expiry
```

---

#### 7.4.17 Context Invalidation 是一等机制

真正可靠的 Harness 应该能显式执行：

```text
invalidate(context_item_id)
```

触发条件可能包括：

- underlying resource changed；
- user corrected requirement；
- permission revoked；
- tool result superseded；
- state transitioned；
- plan replaced；
- environment mutated。

---

#### 7.4.18 Mutation 后必须考虑 Context Invalidation

例如：

```text
Context:
    file A = old content

Agent edits file A
```

这时 old content 不应该继续作为 authoritative context 存在。

推荐链路：

```text
Write
↓
Invalidate old view
↓
Read / Verify
↓
Update canonical state
↓
Rebuild context
```

---

#### 7.4.19 Read-after-write Context Policy

对于高影响 mutation：

```text
write success response
```

不一定足以更新 Context。

更稳妥的是：

```text
Write
↓
Read-after-write / verify
↓
Context update
```

这样 Context 反映的是已验证状态，而不是模型希望发生的状态。

---

#### 7.4.20 Freshness 应是一等字段

Context Item 至少应该能够表达：

```text
observed_at
valid_as_of
source_version
freshness_requirement
```

否则模型很难区分：

```text
刚刚查询的库存
```

和：

```text
30 分钟前的库存
```

---

#### 7.4.21 Freshness Policy 应按数据类型变化

不同信息有不同 freshness sensitivity：

```text
数学定理       → 很低
用户任务目标   → 中等，除非用户修改
Git HEAD       → 高
库存           → 高
权限           → 很高
支付状态       → 很高
网页新闻       → 高
静态文档       → 低到中
```

因此不能只有统一 TTL。

---

#### 7.4.22 Context Versioning

推荐对关键 Context 建立版本：

```text
state_version
plan_version
instruction_version
resource_version
approval_version
capability_snapshot_version
```

这样可以检测：

```text
Model decided under version 17
but action executed under version 19
```

即典型 stale-decision / TOCTOU 风险。

---

#### 7.4.23 State–Context Consistency

核心 invariant：

> **模型看到的关键执行状态，不应与 Harness 当前权威状态静默分叉。**

如果：

```text
State: approval = revoked
Context: approval = granted
```

这是高风险一致性故障。

---

#### 7.4.24 Context Snapshot

在关键 decision point，可以记录：

```text
context_snapshot_id
context_hash
policy_version
state_version
capability_snapshot
```

这样以后可以回答：

> “模型当时到底看到了什么？”

这是可审计 Agent 的重要能力。

---

#### 7.4.25 Context Hash 不是内容理解，但适合 Trace

Hash 可以用于：

- replay correlation；
- cache key；
- drift detection；
- audit；
- experiment reproducibility。

但不能告诉你：

```text
Context 为什么错了
```

所以仍然需要结构化 metadata。

---

#### 7.4.26 Context Budget 是 Policy，不只是 Token Limit

Context Window 只是物理容量。

Context Policy 还需要考虑：

```text
Token Cost
Latency
Attention Competition
Privacy Exposure
Injection Surface
Decision Utility
```

因此：

> **Window 还有空间，不代表还应该继续塞信息。**

---

#### 7.4.27 Context Budget Partition

一个实用思路是为不同 role 预留预算：

```text
Instructions       15%
Current State      20%
Recent Evidence    25%
History            10%
Tools / Skills     15%
Retrieved Memory   10%
Safety Margin       5%
```

具体比例不是固定标准，关键是：

> **Budget 应显式分配，而不是让最啰嗦的来源自然占满窗口。**

---

#### 7.4.28 Output Reserve

不能把 Context Window 全部吃满。

如果模型最大窗口是 \(W\)，则：

\[
B_{input} \le W-B_{output}-B_{margin}
\]

否则可能出现：

- 输出被截断；
- tool argument 不完整；
- reasoning 未完成；
- structured output 无法闭合。

---

#### 7.4.29 Priority Tier

可以定义 Context Priority：

```text
P0  hard policy / approval / critical constraint
P1  current goal / current state / critical evidence
P2  active plan / recent observations
P3  retrieved memory / supporting evidence
P4  older history / verbose logs
```

当预算不足时，优先淘汰低优先级信息。

---

#### 7.4.30 Pinning

某些信息适合 pin：

- 当前 Goal；
- 不可违反的硬约束；
- 尚未解决的 UNKNOWN effect；
- 当前 approval scope；
- critical user correction。

但：

> **Pinned ≠ 永久。**

如果 goal 已修改、approval 已撤销，旧 pin 必须失效。

---

#### 7.4.31 Over-pinning

如果所有东西都 pin：

```text
Pinned Context → 80% window
```

系统等于失去上下文调度能力。

因此 Pin 本身也应有：

```text
owner
reason
scope
expiry
```

---

#### 7.4.32 Exactness Requirement

不同 Context Item 对“原样保留”的需求不同。

高 exactness：

- ID；
- 金额；
- 时间；
- 权限 scope；
- API schema；
- shell command；
- source code；
- mathematical expression；
- approval parameters。

低 exactness：

- 长日志趋势；
- 对话背景；
- 低风险历史摘要。

---

#### 7.4.33 Lossless-ish 与 Lossy Transformation

Context Transform 可以分为：

```text
Lossless-ish
├── formatting
├── dedup
├── field extraction
└── canonicalization

Lossy
├── summarization
├── abstraction
├── compression
└── clustering
```

高风险字段尽量避免 lossy transformation。

---

#### 7.4.34 Summary ≠ Source

任何摘要都应保留：

```text
source_ref
summary_version
created_at
```

这样需要时可以 drill down 回原始证据。

否则 summary 可能逐渐变成新的“伪 Source of Truth”。

---

#### 7.4.35 Summary Drift

危险链：

```text
raw history
↓ summary A
↓ summary B of A
↓ summary C of B
```

每轮都可能丢失：

- 否定词；
- 数值；
- 例外；
- uncertainty；
- provenance。

因此长期 Agent 应定期：

> **从 canonical state / source artifact 重新锚定，而不是无限递归总结摘要。**

---

#### 7.4.36 Structured Distillation 优先于自由摘要

对于 Working State，通常更推荐：

```json
{
  "goal": "...",
  "completed": ["..."],
  "pending": ["..."],
  "unknown_effects": ["..."],
  "constraints": ["..."]
}
```

而不是：

```text
“目前总体进展不错，之前有一些失败……”
```

因为结构化表示更适合：

- diff；
- validation；
- recovery；
- policy checks。

---

#### 7.4.37 Context Compiler

可以把 Context Builder 升级理解为一个 Compiler：

```text
Typed Sources
↓
Policy Checks
↓
Normalization
↓
Selection
↓
Transformation
↓
Budgeting
↓
Ordering
↓
Rendering
↓
Model Context
```

这个视角比简单的 `messages.append()` 更接近真实 Agent Harness。

---

#### 7.4.38 Deterministic Context Logic 应尽量外置

例如：

```text
权限过滤
敏感字段脱敏
版本检查
TTL
去重
预算裁剪
```

这些逻辑如果可以确定性执行，通常不应该全部交给模型决定。

原则：

> **Deterministic constraint → deterministic enforcement。**

---

#### 7.4.39 Model-assisted Context Selection 的适用位置

模型适合辅助：

- semantic relevance；
- query reformulation；
- document summarization；
- ambiguity detection；
- evidence clustering。

但模型输出仍应被 Harness 视为：

```text
proposal / derived view
```

而不是 policy authority。

---

#### 7.4.40 Instruction / Data Separation

Context Rendering 应尽量显式区分：

```text
[INSTRUCTIONS]
...

[CURRENT STATE]
...

[UNTRUSTED EXTERNAL CONTENT]
...
```

结构标签不能构成硬安全边界，但可以减少模型误把数据当 instruction 的概率。

---

#### 7.4.41 Prompt Injection 的 Context Policy 防线

建议形成：

```text
External Content
↓
mark untrusted
↓
strip / isolate dangerous metadata where appropriate
↓
preserve provenance
↓
prevent authority escalation
↓
select minimum necessary excerpt
↓
model
```

重点不是“把所有恶意文字删干净”，而是：

> **即使恶意文字存在，也不能因此获得控制权。**

---

#### 7.4.42 Context Poisoning

Prompt Injection 更像某次输入攻击。

Context Poisoning 更广，包括：

- stale false fact；
- wrong memory；
- malicious retrieval；
- compromised subagent output；
- outdated plan；
- summary hallucination。

如果长期保留，它可能持续影响后续决策。

---

#### 7.4.43 Secret Minimization

原则：

> **Runtime 能看到的 Secret，不代表 Model 应该看到。**

例如：

```text
OAuth token
API key
DB password
private key
```

应尽量由 Runtime 使用，而不是写入 Context。

---

#### 7.4.44 Credential by Reference

更安全：

```text
credential_ref = github_prod_readonly
```

而不是：

```text
credential = ghp_xxxxxxxxx
```

Model 只需要知道能力和 scope，不需要知道 secret value。

---

#### 7.4.45 Sensitive Data Policy

Context Policy 应考虑：

```text
PII
financial data
health data
private source code
credentials
internal documents
```

不同 sensitivity 应对应：

- exposure rules；
- retention；
- logging；
- redaction；
- sharing policy。

---

#### 7.4.46 Tenant Isolation

跨用户 / 跨组织 Agent 必须保证：

```text
Tenant A Context
∩
Tenant B Unauthorized Data
=
∅
```

至少在逻辑授权意义上如此。

Context cache、retrieval cache、summary cache 都必须 tenant-aware。

---

#### 7.4.47 Permission-aware Context

不仅 Action 需要权限，**Information Exposure 也需要权限**。

例如用户没有权限读某项目：

```text
模型也不应该先看到内容，
再由 Harness 阻止它写出去。
```

读取本身已经是暴露。

---

#### 7.4.48 Least-Data Principle

与 Least Privilege 对应：

```text
Least Privilege
= 最小必要操作权限

Least Data
= 最小必要信息暴露
```

一个成熟 Agent 应同时控制：

```text
Action Surface
Information Surface
```

---

#### 7.4.49 Conversation History ≠ Context Policy

把整个聊天记录直接传给模型只是最简单的 history policy。

更成熟的方式是：

```text
Raw Transcript
↓
Extract Current Constraints
↓
Extract Decisions / Commitments
↓
Keep Exact Quotes where needed
↓
Archive older chatter
↓
Build current context
```

---

#### 7.4.50 用户最新消息不应机械覆盖所有旧信息

用户说：

```text
“改成周五。”
```

Harness 需要知道它是在更新：

```text
meeting_date
```

而不是删除此前所有：

```text
participants
location
duration
```

所以 Context Policy 与 Working State Update 必须配合。

---

#### 7.4.51 User Correction 应快速传播

如果用户明确纠正：

```text
“不是上海，是北京。”
```

系统应：

```text
update canonical state
↓
invalidate old context
↓
supersede stale memory if needed
↓
rebuild context
```

而不是只在聊天尾部追加一句 correction。

---

#### 7.4.52 Contradiction 不应该静默压平

如果两个可信来源冲突：

```text
Source A: version = 4
Source B: version = 5
```

不能简单 summary 成：

```text
version = 5
```

除非有明确 authority / freshness 依据。

更合理：

```text
conflict = true
candidates = [A, B]
resolution_basis = freshness / source authority
```

---

#### 7.4.53 Preserve Uncertainty

如果 Observation 是：

```text
payment outcome = UNKNOWN
```

Context Summary 不能压成：

```text
payment failed
```

这属于 semantic corruption。

因此 uncertainty 是必须保留的字段。

---

#### 7.4.54 Context 中的时间必须带时区 / reference time

例如：

```text
“明天下午 3 点”
```

对于 Calendar Agent，应该转成：

```text
2026-10-30 15:00 Asia/Tokyo
```

或显式保留 unresolved timezone。

Temporal ambiguity 不应在 Context 压缩时丢失。

---

#### 7.4.55 Tool Result ≠ Context

Tool 返回：

```text
10000 行日志
```

不意味着 10000 行都应该进入模型。

中间还需要：

```text
Normalization
Filtering
Aggregation
Artifact Externalization
Context Selection
```

---

#### 7.4.56 Observation Context Policy

对于 Observation，应考虑：

```text
status
completeness
freshness
provenance
trust
error
warning
artifact_ref
```

而不是只保留一段 `result_text`。

---

#### 7.4.57 Large Tool Output Externalization

推荐：

```text
Tool Result
↓
Artifact Store
↓
summary + reference
↓
Context
```

需要细节时再按需展开。

这叫 Progressive Disclosure。

---

#### 7.4.58 Logs 的 Context Policy

日志通常适合：

```text
aggregate
cluster failure signatures
keep latest representative samples
preserve exact error line references
```

不适合：

```text
全量复制到每一轮 Context
```

---

#### 7.4.59 Code Context Policy

Coding Agent 不应该默认塞整个仓库。

推荐：

```text
Issue / Goal
Relevant Files
Exact Target Symbols
Current Diff
Relevant Tests
Repo Instructions
Recent Failures
```

而把其余代码按需 retrieval。

---

#### 7.4.60 Numerical Context Policy

数值数据特别需要：

```text
exact value
unit
precision
source
as_of
```

不要随意 summary 成：

```text
“差不多一百多万”
```

如果实际决策依赖精确金额。

---

#### 7.4.61 Citation / Evidence Context

Research Agent 可维护：

```text
claim_id
source_id
evidence_span
confidence
conflict_status
```

模型不需要每次看到整篇文章，只需要当前 claim 相关证据与可追溯引用。

---

#### 7.4.62 Tool Catalog 也是 Context

Tool schema、description、side-effect metadata 会占模型输入。

因此 Tool Policy 与 Context Policy 有交叉：

```text
Tool Policy
→ 决定哪些能力允许被暴露

Context Policy
→ 决定如何把这些能力表示给模型
```

---

#### 7.4.63 Native Tool ≠ Always Visible

系统支持 Browser、Shell、Calendar，不代表每一步都要把这些工具暴露给模型。

应根据：

- task phase；
- permission；
- risk；
- relevance；
- budget。

动态曝光。

---

#### 7.4.64 Skill Context Policy

Skill 可以 Progressive Disclosure：

```text
metadata
↓
summary
↓
core procedure
↓
examples / scripts
```

不要每次激活 Skill 就把完整材料全部塞入 Context。

---

#### 7.4.65 Plan Context Policy

Plan 应作为 State，而不是一段永久 prompt。

模型通常只需要：

```text
current goal
current step
critical dependencies
completed milestones
next checkpoints
```

而不是重复读取所有已完成细节。

---

#### 7.4.66 Stale Plan 不应压过 Fresh Evidence

如果 Plan 说：

```text
next: modify file A
```

但最新 Observation 显示：

```text
file A 已被其他人修改
```

Context Policy 应突出 fresh evidence，并标记 plan stale。

---

#### 7.4.67 Failure History Context

失败历史应该防止：

```text
Agent 重复做同一个无效动作
```

但不应该让 Context 被几十次 retry log 占满。

推荐保留：

```text
failure_signature
attempt_count
last_attempt
what_changed_since_last_attempt
```

---

#### 7.4.68 Recovery History 是 Context 的重要部分

如果已经尝试：

```text
A → failed
B → failed
```

模型下一次决策必须知道这件事。

否则 Agent 会出现：

```text
Failure Amnesia
```

---

#### 7.4.69 UNKNOWN Effect 应高优先级保留

例如：

```text
send_email outcome = UNKNOWN
```

在 reconciliation 完成前，这条状态不能被普通 history compression 清掉。

否则可能重复发送。

---

#### 7.4.70 Effect Ledger 的 Context 投影

模型通常不需要看到整个 Ledger，但当前决策相关的 effect 应明确呈现：

```text
committed
pending
unknown
compensated
```

特别是不可逆 action。

---

#### 7.4.71 Approval Context

Approval 不应只是：

```text
approved = true
```

还应包括：

```text
scope
resource
arguments
version
expiry
approved_by
```

进入模型的 Context 也要保留关键 scope。

---

#### 7.4.72 Stale Approval 必须失效

如果用户批准：

```text
send $100 to account A
```

随后参数变成：

```text
send $1000 to account B
```

旧 approval 不能继续存在于 Context 中作为“已批准”。

---

#### 7.4.73 Budget State 应进入必要 Context

Agent 决策可能依赖：

```text
remaining_steps
remaining_cost
remaining_time
remaining_tool_calls
```

如果模型完全不知道预算，可能规划出无法完成的方案。

---

#### 7.4.74 Budget Context 不必精确到所有内部计费细节

模型可能只需要：

```text
low / medium / high budget remaining
```

或关键限额。

Context Policy 应决定哪些成本状态对决策真正有用。

---

#### 7.4.75 Capability Snapshot

对于动态能力系统，可以给模型：

```text
currently_available_tools
current_permissions
current_provider_health
```

但不需要暴露整个全局 Capability Registry。

---

#### 7.4.76 Capability Exposure 与 Context Policy 的关系

5.4 已定义：

```text
Minimal Sufficient Capability Exposure
```

7.4 进一步负责：

```text
如何把这组能力描述进当前 Context
```

即：

```text
Discovery → Exposure Set → Context Rendering
```

---

#### 7.4.77 Model-visible State 与 Runtime-private State

不是所有 Runtime State 都应进入模型。

例如：

```text
internal credential handle
security detector score
fraud-rule threshold
private audit annotation
```

可能只属于 Harness / Runtime private state。

---

#### 7.4.78 Hidden State 仍应可审计

“模型看不到”不代表“不记录”。

Runtime-private policy state 应进入受控 audit trace，以便复盘：

```text
为什么某 Tool 没暴露？
为什么某 Context 被过滤？
```

---

#### 7.4.79 Context Policy 与 Memory Policy

两者区别：

```text
Memory Policy
= 什么值得保存、保留多久、怎样更新

Context Policy
= 当前这一步从已有信息中给模型看什么
```

因此：

```text
Memory contains X
≠
Context must contain X
```

---

#### 7.4.80 Memory Activation

从 Memory 召回的信息进入 Context 前仍需经过：

```text
freshness
scope
permission
trust
relevance
conflict
```

旧 Memory 不能因为“曾经被保存”就自动获得 authority。

---

#### 7.4.81 Retrieval Result 不是最终 Context

4.6 已定义 Retrieval Pipeline。

Context Policy 接在后面：

```text
Retrieved Candidates
↓
Evidence Selection
↓
Context Admission
↓
Rendering
```

因此 Retrieval Recall 高，不代表 Context Quality 高。

---

#### 7.4.82 Retrieval Poisoning 的最后一道门

即使 Retriever 召回恶意文档，Context Policy 仍可以：

- 标记 untrusted；
- 只截取必要片段；
- 去除无关 instruction-like text；
- 保留 provenance；
- 降低 priority。

---

#### 7.4.83 Cache ≠ Memory ≠ Context

三者职责：

```text
Cache
= 加速重复计算

Memory
= 保存未来可能有用的信息

Context
= 当前模型看到的信息
```

不要因为某 Context 被 cache，就误认为它成为长期 Memory。

---

#### 7.4.84 Context Cache Key

至少可能依赖：

```text
policy_version
state_version
instruction_version
tenant
permission_scope
capability_snapshot
source_versions
```

否则容易复用 stale / unauthorized context。

---

#### 7.4.85 Cache Invalidation

Context Cache 的危险通常不在 cache miss，而在：

```text
错误命中旧结果
```

尤其 permission / approval / state 改变时，应快速失效。

---

#### 7.4.86 Context Ordering

即使内容相同，不同排列也可能影响模型决策。

建议稳定分区：

```text
Instructions
Goal
Current State
Critical Constraints
Recent Observations
Evidence
Available Capabilities
References
```

但具体顺序应评测，不应迷信单一“最佳位置”。

---

#### 7.4.87 Primacy / Recency Effect 不应被当作固定规律

不同模型、任务、长度下 position sensitivity 不同。

因此：

> **不要把“重要信息永远放最前 / 最后”当作不可变真理；应使用稳定结构并做模型级验证。**

---

#### 7.4.88 Lost-in-the-Middle 的工程含义

长 Context 中，信息即使“还在窗口里”，也可能：

```text
effectively under-used
```

因此 Context Policy 目标不是：

```text
avoid truncation only
```

而是：

```text
maximize decision-relevant signal density
```

---

#### 7.4.89 Context Pollution

典型污染源：

- verbose logs；
- duplicate evidence；
- stale plans；
- outdated memory；
- repeated tool schemas；
- unrelated history；
- low-value chain-of-thought-like notes。

更多 token 不一定提升质量。

---

#### 7.4.90 Signal Density

可以用一个概念性指标：

\[
SignalDensity = \frac{DecisionRelevantInformation}{ContextCost}
\]

不是严格可观测量，但很适合作为设计目标。

---

#### 7.4.91 Dynamic Context by Decision Phase

不同阶段需要不同 Context：

```text
Planning
→ goal / constraints / capability map

Execution
→ current step / exact arguments / state

Verification
→ expected outcome / observed result / invariants

Recovery
→ failure history / side effects / remaining options
```

所以单一固定 prompt 不适合复杂 Agent。

---

#### 7.4.92 Planning Context 不等于 Execution Context

规划阶段可以高层抽象。

执行阶段需要：

```text
exact resource ID
version
permission
arguments
```

Context Policy 应允许 phase-specific materialization。

---

#### 7.4.93 Verification Context 应偏 Evidence

Verifier 不应该只看到：

```text
Agent 自己的成功声明
```

而应看到：

```text
success predicate
independent evidence
actual state
```

否则容易 self-confirmation。

---

#### 7.4.94 Recovery Context 应突出“发生过什么”

Recovery 需要：

```text
attempt history
known side effects
unknown outcomes
failure class
current environment
```

而不是重新从原始目标开始猜。

---

#### 7.4.95 Long-running Agent 必须周期性重建 Context

不要：

```text
C_{t+1} = C_t + new_message
```

无限增长。

更合理：

```text
Canonical State
+ Current Policy
+ Relevant Recent Evidence
+ On-demand Memory
→ Rebuild C_t
```

---

#### 7.4.96 Rebuild > Recursive Append

周期性重建的好处：

- 清掉 stale info；
- 去重；
- 恢复 canonical state；
- 降低 summary drift；
- 应用最新 policy version。

---

#### 7.4.97 Durable Resume 后必须重建 Context

Checkpoint 恢复后不能直接把旧 prompt 原样继续。

应：

```text
Restore Durable State
↓
Reobserve Critical Environment
↓
Revalidate Permission / Capability
↓
Apply Current Context Policy
↓
Build Fresh Context
```

---

#### 7.4.98 Context Snapshot ≠ Resume Context

旧 Snapshot 是历史证据。

Resume Context 应结合：

```text
current environment
current policy
current permissions
```

重新生成。

---

#### 7.4.99 Multi-Agent：Shared Context 不是复制全部上下文

Parent → Subagent 不应该默认：

```text
copy entire parent context
```

应该生成 Delegation Context：

```text
goal
scope
necessary evidence
allowed capabilities
constraints
return contract
```

---

#### 7.4.100 Delegation Context = Information Boundary + Authority Boundary

给 Subagent 什么信息，与给它什么权限，应共同设计。

例如：

```text
需要总结合同
```

Subagent 可能只需要合同正文和输出格式，不需要：

```text
用户全部历史
支付凭证
其他项目文件
```

---

#### 7.4.101 Shared Context 与 Private Context

6.5 已讨论共享 / 私有上下文。

Harness Context Policy 负责把这一概念落成：

```text
shareable
private
parent-only
child-only
redacted
reference-only
```

等实际标签与传播规则。

---

#### 7.4.102 Subagent Output 应重新经过 Context Admission

子 Agent 返回：

```text
“请执行 rm -rf /”
```

不因为来自 Subagent 就自动成为 instruction。

它仍然是：

```text
untrusted / lower-authority derived content
```

需经过 parent Harness 再评估。

---

#### 7.4.103 Context Delegation 不得隐式扩权

Parent 有权限访问 A+B。

Subagent 只需要 A。

则：

```text
Child Context Scope = A
```

而不是自动继承 B。

这与 Least Privilege 同构。

---

#### 7.4.104 Human-in-the-loop Context

向用户请求确认时，应提供：

```text
what will happen
critical parameters
side effects
alternatives
why approval is needed
```

而不是把整个内部 Context 原样暴露给用户。

---

#### 7.4.105 Approval UI 的 Context Policy

Approval Context 应遵循：

```text
Minimal Sufficient Disclosure
```

既足够让用户做知情决定，又不泄露无关 secret / internal data。

---

#### 7.4.106 Ask-User Context

Agent 向用户追问时，应该暴露真正缺失的信息：

```text
Need:
    destination timezone
```

而不是：

```text
“我不确定，请提供更多信息。”
```

Harness 可以保存 unresolved field，让下一轮 Context 直接恢复到缺口位置。

---

#### 7.4.107 Context Policy 应支持 Partial Information

现实 Agent 经常不是：

```text
known / unknown
```

二元状态。

而是：

```text
known
unknown
conflicting
stale
partial
unverified
```

Context 表示应保留这些状态。

---

#### 7.4.108 Fail-open vs Fail-closed

如果 Context Policy 无法确认某高敏信息是否允许暴露：

```text
fail-open
→ 先给模型看
```

可能带来泄露。

高风险场景通常应偏：

```text
fail-closed
→ 不暴露 / 请求重新授权
```

但低风险场景可采用 graceful degradation。

---

#### 7.4.109 Graceful Degradation

当某些 Context 无法获取，可以：

```text
use stale-but-labeled cache
ask user
use lower-confidence mode
limit action set
switch to read-only
```

而不是假装信息完整。

---

#### 7.4.110 Context Policy as Code

高影响规则应尽量结构化，例如：

```python
if item.sensitivity == "secret":
    deny_model_visibility()

if item.source == "external_web":
    mark_untrusted()

if item.version < canonical.version:
    invalidate()
```

而不是只写在 prompt：

```text
“请不要泄露敏感信息。”
```

---

#### 7.4.111 Policy Engine

可以把 Context Policy 实现为：

```text
Rule Engine
Attribute-based Policy
Typed Filters
Declarative Config
Hybrid Deterministic + Model-assisted Selector
```

关键是：

> **Policy 决策必须可追溯，不应完全藏在模型自由生成里。**

---

#### 7.4.112 Policy Decision Trace

每次 Context Assembly 可以记录：

```text
candidate item
admitted / rejected
reason
transformation
priority
policy version
```

这样 debug 时能回答：

> “为什么这条关键信息没进 Context？”

---

#### 7.4.113 Context Failure Localization

当 Agent 因“没看到信息”失败时，至少要问：

```text
1. 信息存在吗？
2. Source 正确吗？
3. State / Memory 中保存了吗？
4. 被检索出来了吗？
5. Context Policy 允许进入吗？
6. Budget 裁掉了吗？
7. 压缩时丢失了吗？
8. 排序 / 渲染有问题吗？
9. 模型看到了但没利用吗？
```

不要全部归因成“模型忘了”。

---

#### 7.4.114 Context Policy Evaluation

至少可以评价：

```text
Constraint Retention Rate
Relevant Evidence Recall
Context Precision
Freshness Accuracy
Provenance Coverage
Secret Exposure Rate
Cross-tenant Leakage Rate
Injection Resistance
Context Token Cost
Decision Quality
```

---

#### 7.4.115 Context Precision

可以定义近似指标：

\[
ContextPrecision = \frac{UsefulContextItems}{PresentedContextItems}
\]

目的是衡量：

```text
模型看到的信息里，多少真正与当前 Decision 有关？
```

---

#### 7.4.116 Context Recall

\[
ContextRecall = \frac{RequiredItemsPresented}{RequiredItems}
\]

Context 太精简可能：

```text
Precision 高
Recall 低
```

导致遗漏关键约束。

因此 Context Policy 是 Precision / Recall 权衡。

---

#### 7.4.117 Constraint Retention Rate

特别适合长任务：

```text
早期用户约束
经过 20 个 steps
是否仍在真正需要它的 decision point 生效？
```

这是比“模型是否记得原句”更有意义的指标。

---

#### 7.4.118 Stale-context Incident Rate

统计：

```text
因模型看到旧状态而导致错误动作的比例
```

例如：

- stale inventory；
- stale permission；
- stale Git HEAD；
- stale approval。

---

#### 7.4.119 Context-induced Harm

Context 并不只会帮助。

可能：

```text
原本正确
↓
加入错误 / stale / malicious context
↓
决策变错
```

因此应报告：

```text
Context Rescue
vs
Context Degradation
```

---

#### 7.4.120 Context Net Benefit

可以继续沿用统一评价：

\[
NetBenefit = Wrong\rightarrow Right - Right\rightarrow Wrong
\]

适用于：

- Retrieval；
- Memory；
- Skill；
- Context Policy。

---

#### 7.4.121 Counterfactual Context Test

固定：

```text
same model
same state
same task
```

只改变一个 Context 元素：

```text
with / without critical constraint
fresh / stale observation
trusted / untrusted source
full / compact history
```

观察 Decision 是否按预期变化。

---

#### 7.4.122 Context Ablation

可以比较：

```text
Raw Transcript
vs
Structured State

All Tools
vs
Filtered Tools

Raw Tool Output
vs
Normalized Observation

No Memory
vs
Retrieved Memory
```

帮助定位 Context Policy 的真实贡献。

---

#### 7.4.123 Context Stress Test

建议测试：

- 100+ turns；
- conflicting instructions；
- stale observation；
- duplicated logs；
- prompt injection；
- capability explosion；
- tenant-mixed candidates；
- summary drift；
- mid-run permission revocation。

---

#### 7.4.124 Long-context Model 不能替代 Context Policy

更大 Context Window 可以减少：

```text
hard truncation
```

但不能自动解决：

```text
stale data
wrong authority
secret leakage
contradictions
permission
prompt injection
context pollution
```

所以：

> **Long Context ≠ No Context Engineering ≠ No Context Policy。**

---

#### 7.4.125 “全塞进去，让模型自己判断”为什么不可靠

因为模型无法天然知道：

- 哪个版本 authoritative；
- 哪条内容被撤销；
- 哪个 secret 不应看到；
- 哪个网页是恶意注入；
- 哪个 Tool 已失效；
- 哪个 approval 已过期。

这些都属于 Harness 应显式维护的系统语义。

---

#### 7.4.126 Minimal Sufficient Context 的 Harness 化

4.1 提出：

```text
Minimal Sufficient Context
```

7.4 把它工程化成：

```text
Eligibility
↓
Priority
↓
Budget
↓
Freshness
↓
Trust
↓
Exactness
↓
Selection
```

最终目标：

> **给模型足以正确、安全完成下一步决策的最小信息集合。**

---

#### 7.4.127 Context Policy 与 Harness Engineering

Context Policy 只是 Harness 的一个组成部分。

完整 Harness 还会管理：

```text
Agent Loop Policy
Instruction Policy
Tool Policy
Memory Policy
Planning Policy
Subagent Policy
Permission Policy
Termination Policy
Recovery Policy
```

因此：

```text
Context Engineering
⊂ Context Policy
⊂ Harness Engineering
```

这里同样是系统范围上的近似关系。

---

#### 7.4.128 Coding Agent 最小示例

任务：

```text
修复 issue #123
```

好的 Context 可能包含：

```text
Goal
Relevant repo instructions
Target issue
Relevant source snippets
Current diff
Failing test
Recent attempt history
Allowed write scope
```

而不是：

```text
整个仓库
所有 git log
全部 tests 输出
全部历史聊天
```

修改以后：

```text
invalidate old file content
→ refresh diff
→ run tests
→ rebuild verification context
```

---

#### 7.4.129 Browser Agent 最小示例

当前 Context：

```text
Goal
Current URL
Fresh screenshot / DOM
Recent click history
Known form state
Permission / approval
```

导航以后旧 screenshot 应：

```text
stale = true
```

不能继续当作当前页面状态。

---

#### 7.4.130 Research Agent 最小示例

Context 不应是：

```text
20 篇网页全文
```

而应更接近：

```text
Research Question
Current Claims
Evidence per Claim
Source Provenance
Contradictions
Open Gaps
Next Search Need
```

这样模型是在“证据状态”上工作，而不是在网页堆里游泳。

---

#### 7.4.131 Calendar Agent 最小示例

任务：

```text
安排明天下午三点会议
```

Context 至少要明确：

```text
resolved date
resolved timezone
participants
calendar account
availability freshness
approval state
```

不能只保留自然语言：

```text
“明天下午三点”
```

否则 Resume / 跨时区容易出错。

---

#### 7.4.132 Payment Agent 最小示例

高风险 Context：

```text
recipient_id
amount
currency
approval_scope
payment_status
idempotency_key
unknown_outcome
```

这些字段通常要求 exact preservation，不适合自由摘要。

---

#### 7.4.133 Multi-Agent Supervisor 示例

Supervisor 不需要收到每个 Worker 的全部思考历史。

更适合：

```text
worker goal
status
artifacts
verified findings
open risks
requested decisions
```

这能显著减少 shared-context pollution。

---

#### 7.4.134 Context Policy Failure Mode 1：Append Forever

症状：

```text
所有历史永久累加
```

后果：

- token cost；
- stale state；
- duplicate info；
- attention dilution。

修复：

```text
state-centric rebuild
```

---

#### 7.4.135 Failure Mode 2：Blind Truncation

症状：

```text
超过长度就删最早消息
```

可能删掉：

- user constraint；
- approval scope；
- unresolved effect；
- important exception。

修复：role-aware retention。

---

#### 7.4.136 Failure Mode 3：Summary Everything

把：

```text
ID / 金额 / 权限 / API Contract
```

都自由摘要。

后果：semantic corruption。

修复：exactness-aware policy。

---

#### 7.4.137 Failure Mode 4：No Freshness

模型持续基于旧 inventory / permission / Git HEAD 行动。

修复：freshness policy + invalidation。

---

#### 7.4.138 Failure Mode 5：No Provenance

External data 与 instruction 混在一起。

修复：typed source + trust label。

---

#### 7.4.139 Failure Mode 6：Secrets in Prompt

为了方便，直接把 credential 放入 Context。

修复：runtime credential injection + reference handle。

---

#### 7.4.140 Failure Mode 7：Shared-context Explosion

Multi-Agent 把所有 Worker 输出广播给所有 Agent。

修复：need-to-know shared context。

---

#### 7.4.141 Failure Mode 8：Stale Approval

参数已变但旧批准仍存在。

修复：approval scope hash + version binding。

---

#### 7.4.142 Failure Mode 9：Failure Amnesia

压缩历史时把之前失败尝试删掉。

修复：structured recovery history。

---

#### 7.4.143 Failure Mode 10：Effect Amnesia

Context 忘记已经执行的真实动作。

修复：Effect Ledger projection。

---

#### 7.4.144 Failure Mode 11：Recursive Summary Drift

摘要的摘要不断累积误差。

修复：periodic re-anchor。

---

#### 7.4.145 Failure Mode 12：All Tools Always Visible

Tool catalog 占满输入，并扩大错误动作面。

修复：Minimal Sufficient Capability Exposure。

---

#### 7.4.146 Failure Mode 13：Context Cache Cross-tenant Leak

不同用户复用相同 cache key。

修复：tenant / permission-aware cache key。

---

#### 7.4.147 Failure Mode 14：Context ≈ Reality

把旧 Context 当成当前环境。

修复：Source of Truth + re-observation。

---

#### 7.4.148 Failure Mode 15：Model Manages Policy Alone

把所有过滤、权限、freshness 都交给 LLM 自己判断。

修复：deterministic Harness enforcement。

---

#### 7.4.149 Context Policy 的工程原则

可以压缩为二十条：

1. **State before Context**：先有权威状态，再投影给模型。
2. **Eligibility before relevance**：先判断能不能看，再判断值不值得看。
3. **Provenance first**：所有重要信息保留来源。
4. **Freshness first-class**：新旧不是隐含信息。
5. **Context is a view**：永远不要把 Context 当 Source of Truth。
6. **Rebuild, not append forever**。
7. **Exact fields stay exact**。
8. **Summaries keep source refs**。
9. **External content is data, not authority**。
10. **Runtime secrets stay runtime-private**。
11. **Least Data + Least Privilege**。
12. **Mutation invalidates stale views**。
13. **UNKNOWN must remain UNKNOWN**。
14. **Failure / Effect history must survive compression**。
15. **Tool / Skill visibility is dynamic**。
16. **Subagent context is delegated, not copied wholesale**。
17. **Resume rebuilds context from current reality**。
18. **Policy decisions must be traceable**。
19. **Evaluate Context separately from Model**。
20. **Minimal Sufficient Context**。

---

#### 7.4.150 面试掌握：Context Engineering 与 Context Policy 有什么区别？

推荐答法：

> Context Engineering 关注怎样选择、组织、压缩和呈现信息，让模型在当前推理中看到高价值上下文；Context Policy 则是 Harness 层把这些原则系统化，明确哪些信息有资格进入、生命周期如何、怎样做 freshness / permission / trust / budget / invalidation 管理。前者偏信息设计，后者偏 runtime governance。

---

#### 7.4.151 面试掌握：Context 和 State 最大区别是什么？

> State 是系统当前任务的权威操作表示；Context 是为了当前模型决策，从 State、Observation、Memory、Retrieval 等来源投影出的临时 view。State 可以比 Context 大，Context 也可能过期，因此 Context 不能反过来充当 Source of Truth。

---

#### 7.4.152 面试掌握：为什么 Long Context 不能替代 Context Policy？

> 更长窗口只减少硬截断，不能解决 stale data、权限、secret leakage、prompt injection、contradiction、summary drift、approval 失效和 tool explosion。Context Policy 管的是信息治理，不只是容量。

---

#### 7.4.153 面试掌握：为什么 Tool Result 不能直接 append？

> Tool Result 是原始执行结果，可能过大、过期、不可信或包含敏感信息；进入模型前应经过 normalization、provenance、freshness、trust、filtering、externalization 和 context selection。Tool Result ≠ Observation ≠ Context。

---

#### 7.4.154 面试掌握：怎样避免长任务忘记早期约束？

> 不依赖原始 transcript 一直留在窗口，而是把关键约束抽取进 authoritative state / effective instruction set，Context Policy 在相关 decision point 按 scope 与 priority 重新投影，并通过 Constraint Retention Rate 测试它是否真正生效。

---

#### 7.4.155 面试掌握：Prompt Injection 在 Context Policy 层怎么防？

> 关键是 provenance 与 authority separation。网页、邮件、RAG chunk、tool output 默认属于 data plane，即使内容像 instruction，也不能自动获得 control-plane 权限；Harness 还应最小化暴露、保留 trust label，并让高影响 policy 由确定性机制执行。

---

#### 7.4.156 面试掌握：Context Compression 最大风险是什么？

> 不是“压缩率不够高”，而是语义损失：否定词、数值、exception、uncertainty、provenance、effect history 被压掉。高风险字段应 exact preserve，摘要要保留 source reference，并定期重新从 canonical source 锚定。

---

#### 7.4.157 面试掌握：Context Cache 有什么安全问题？

> Cache key 如果不包含 tenant、permission scope、policy version、state version 等，就可能复用 stale 或跨用户 Context。Context cache 的主要风险往往不是 miss，而是错误 hit。

---

#### 7.4.158 面试掌握：Multi-Agent 为什么不能共享全部 Context？

> 因为会带来 token 爆炸、隐私泄露、authority 扩散和 irrelevant information pollution。更好的做法是按 delegation contract 给每个 Subagent 最小必要信息，并区分 shared / private / parent-only / reference-only context。

---

#### 7.4.159 面试掌握：Context Policy 怎么评测？

> 不能只看最终 Task Success。还要看 Constraint Retention、Relevant Evidence Recall、Context Precision、Freshness Accuracy、Provenance Coverage、Secret Exposure、Injection Resistance、Stale-context Incident、Token Cost，以及 Context-induced rescue / degradation。

---

#### 7.4.160 面试掌握：什么时候应该重建 Context？

典型触发：

- state mutation；
- user correction；
- permission / approval change；
- tool result supersession；
- plan change；
- resume from checkpoint；
- context pollution 增长；
- policy version change。

---

#### 7.4.161 一句话总结

> **Context Policy 是 Agent Harness 对“模型此刻能看到什么”的可执行治理层：它不把 Context 当聊天历史或存储，而把它当一个受 provenance、authority、permission、freshness、budget、exactness、lifecycle 和 security 约束的动态 runtime view；成熟系统的目标不是塞入最多信息，而是持续构造最小、最新、可信、可追溯且足以支持下一步正确决策的 Context。**

---

#### 7.4.162 参考资料

- Liu N F, Lin K, Hewitt J, et al. **Lost in the Middle: How Language Models Use Long Contexts**. TACL, 2024.
- Lewis P, Perez E, Piktus A, et al. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**. NeurIPS, 2020.
- Yao S, Zhao J, Yu D, et al. **ReAct: Synergizing Reasoning and Acting in Language Models**. ICLR, 2023.
- Kaelbling L P, Littman M L, Cassandra A R. **Planning and Acting in Partially Observable Stochastic Domains**. Artificial Intelligence, 1998.
- OWASP. **Top 10 for Large Language Model Applications / Prompt Injection guidance**.
- NIST. **AI Risk Management Framework (AI RMF 1.0)**.
- Kleppmann M. **Designing Data-Intensive Applications**. O’Reilly, 2017.
- Google. **Site Reliability Engineering** — reliability, state, failure and operational policy principles.

---
