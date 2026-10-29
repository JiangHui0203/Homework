#### 7.4.32 Summary Drift：摘要本身也会累积错误

危险模式：

```text
raw history
→ summary v1
→ summary of summary v2
→ summary of summary v3
```

每次都可能：

- 丢掉限定词；
- 改变因果关系；
- 混淆时间；
- 把假设写成事实；
- 把 proposed 写成 completed。

最终得到一个非常流畅但不再忠实的 context。

因此推荐：

```text
canonical state derived from source events
```

而不是无限：

```text
summary(summary(summary(...)))
```

对于高价值事实，应保留 source pointer，使摘要可回溯。

---

#### 7.4.33 Ordering：上下文顺序本身就是策略

即使包含相同信息，不同顺序也可能产生不同模型行为。

常见 zone：

```text
1. Active policy / contract
2. Current goal
3. Current state
4. Current decision request
5. Relevant evidence
6. Recent observations
7. Optional background
```

具体顺序依模型与任务而异，但原则是：

> **不要假设“只要放进窗口，模型就会同等利用”。**

Context Policy 应把 ordering 当成显式设计变量。

---

#### 7.4.34 Lost in the Middle：长窗口不是均匀记忆

长上下文模型可能对不同位置的信息利用能力不同。

典型风险：

```text
关键证据
  buried in middle
        ↓
模型看到了
≠
模型有效使用了
```

因此重要内容可以：

- 放在明确结构中；
- 在当前 decision 附近重新呈现；
- 使用 heading / schema；
- 通过 concise state 重述；
- 避免被大量无关内容夹住。

但注意：

> **重复重要信息是 salience technique，不应制造多个彼此不一致的副本。**

---

#### 7.4.35 Salience 与 Duplication 要区分

适度重述：

```text
Active constraint:
read-only
```

可以提高可见性。

但如果 context 同时出现：

```text
read-only
write allowed
read-only unless needed
probably can write
```

模型面对的是 conflict amplification。

所以推荐：

```text
one canonical active representation
+
source references if needed
```

而不是不断复制自然语言规则。

---

#### 7.4.36 Context Pollution：无关内容也会改变模型

Context pollution 不只意味着 token 浪费。

它可能产生真实行为偏差：

```text
irrelevant code
→ 模型误判 dependency

old error
→ 模型重复修已经解决的问题

unrelated user preference
→ 错误套用到当前任务

retrieved marketing page
→ 干扰技术事实判断
```

因此 Context Policy 应有：

```text
negative selection
```

即明确知道哪些内容**不应该进入**当前 snapshot。

---

#### 7.4.37 Prompt Injection 也是 Context Contamination 问题

7.3 已经处理 authority。

7.4 负责另一层：

> 即使 external content 只是 data，它应该如何安全进入 context？

推荐保留显式边界：

```text
<external_data source="web">
...
</external_data>
```

或者等价的结构化 block。

同时避免：

```text
user/system instruction
+ raw web text
```

被无边界拼接成一个扁平字符串。

Context Policy 不能单独消灭 prompt injection，但可以减少**来源混淆和污染传播**。

---

#### 7.4.38 不可信内容应遵循 Least Propagation

如果某个网页片段只在一个局部分析步骤需要：

```text
read
→ extract fact
→ record provenance
→ discard raw malicious payload from future snapshots
```

通常比：

```text
append raw page forever
```

安全。

可以称为：

> **least propagation principle**

即不可信 external content 在 Agent trajectory 中只传播到真正需要它的范围。

---

#### 7.4.39 Stale Context 与 Stale State 是两种不同问题

可能出现：

```text
runtime state 已更新
context 仍然旧
```

例如：

```text
State:
branch = new-fix

Context:
branch = old-fix
```

这说明 state reducer 正确，但 context snapshot 未刷新。

也可能相反：

```text
context 中写了新状态
canonical runtime state 没更新
```

这说明模型只是“说”了状态变化，系统并没有真正记录。

因此：

```text
State Update
≠
Context Update
```

两者要有明确的数据流。

---

#### 7.4.40 哪些事件应该触发 Context Refresh

典型 invalidation event：

- 用户修改目标；
- instruction policy 更新；
- permission / approval 状态变化；
- tool 返回新 observation；
- 文件或资源版本变化；
- plan 被重新规划；
- verifier 否定已有假设；
- subagent 返回；
- 外部事件到达；
- memory 被更新或撤销；
- 当前 decision type 改变。

推荐：

```text
event
→ update state
→ invalidate affected context components
→ rebuild / refresh
```

而不是等模型“自己发现上下文旧了”。

---

#### 7.4.41 Context Snapshot 应有 Version

对于可审计 Agent，可以记录：

```text
context_snapshot_id
state_version
policy_version
plan_version
memory_version
retrieval_version
created_at
decision_type
```

这样发生错误时可以回答：

```text
模型当时到底看到了什么？
基于哪个 state version？
是不是用了过期 evidence？
```

没有 snapshot version，很多 Agent bug 只能靠猜。

---

#### 7.4.42 Context Snapshot 不是永久事实

一次 snapshot 是：

```text
a view at time t
```

不是：

```text
the truth forever
```

因此 debug 日志里既要保留 snapshot，也要保留其：

```text
validity interval
source pointers
transformation metadata
```

这对于动态系统尤其重要。

---

#### 7.4.43 Subagent 应获得 Context Projection，而不是 Parent Transcript Copy

7.8 会详细讨论 Subagent Policy。

在 7.4 先固定原则：

\[
Context(subagent)
=
Projection(Context(parent), task, authority, need)
\]

而不是：

```text
parent full transcript
→ child
```

子 Agent 通常只需要：

- delegated goal；
- 必要 constraints；
- relevant artifacts；
- allowed tools / authority summary；
- required return contract。

这同时降低：

- token 成本；
- information leakage；
- confusion；
- inherited stale context。

---

#### 7.4.44 Context Minimization 也是隐私控制

如果 Agent 只需要：

```text
订单是否已支付？
```

就不应自动把：

```text
完整用户档案
家庭地址
历史订单
支付卡信息
全部客服记录
```

一起提供给模型。

因此 Context Policy 与 privacy 有一个非常直接的原则：

> **Need-to-know applies to model context too.**

这并不取代正式 permission / privacy policy，但它减少了不必要的数据暴露面。

---

#### 7.4.45 Capability Description 也需要按需进入 Context

Agent 有 100 个 tools，不代表每轮都应该把 100 个完整 schema 放入模型上下文。

可以采用：

```text
current decision
→ relevant capability subset
→ expose selected tools
```

这有助于：

- 降低 token 成本；
- 降低错误 tool selection；
- 缩小攻击面；
- 提高 tool routing clarity。

但具体 Tool Policy 放在 7.5。

7.4 只负责强调：

> **Tool availability is also part of context exposure design.**

---

#### 7.4.46 Context Cache 可以优化成本，但不能破坏语义

很多 context 片段可能跨轮稳定：

```text
system contract
tool schemas
stable project description
large static document prefix
```

可以利用 provider / runtime 的 prompt caching。

但 cache 只是执行优化。

不能因为“已经缓存”就继续使用已经失效的内容。

语义顺序必须是：

```text
still valid?
    ↓ yes
can reuse cache?
```

而不是：

```text
cached?
    ↓ yes
therefore valid
```

---

#### 7.4.47 Cache Invalidation 是 Context Policy 的一部分

缓存最危险的问题不是 miss，而是错误 hit。

典型 invalidation key：

```text
policy_version
resource_version
tool_schema_version
memory_version
task_scope
model_version
```

例如 tool schema 已经升级，旧 schema 的 prompt cache 必须失效。

所以：

> **Fast stale context is still stale context.**

---

#### 7.4.48 Context Policy 还应适配模型特性

不同模型可能存在：

- context capacity 差异；
- long-context utilization 差异；
- tool schema 理解差异；
- structured input 支持差异；
- multimodal context 差异；
- caching 能力差异。

因此 Context Policy 可以有 model-specific rendering：

```text
Canonical Context State
       ↓
Model Adapter
       ↓
Provider-specific input
```

但 canonical state 不应被 provider-specific prompt format 绑死。

---

#### 7.4.49 一个实用的数据结构：ContextItem

可以把候选 context 单元建模为：

```python
@dataclass
class ContextItem:
    id: str
    kind: str
    content_ref: str

    source: str
    provenance: str

    created_at: datetime
    observed_at: datetime | None
    valid_until: datetime | None
    version: str | None

    relevance: float | None
    priority: int

    sensitivity: str
    authority_class: str

    compressibility: str
    token_estimate: int

    dependencies: list[str]
    supersedes: list[str]
```

重点不是字段必须完全一样，而是让 Context Policy 操作**有类型的信息对象**，而不是任意字符串。

---

#### 7.4.50 一个实用的数据结构：ContextSnapshot

```python
@dataclass
class ContextSnapshot:
    snapshot_id: str
    run_id: str
    decision_id: str

    state_version: str
    policy_version: str
    created_at: datetime

    items: list[ContextItem]

    token_estimate: int
    omitted_items: list[str]
    compression_records: list[str]
```

这样可以回答：

```text
included what?
omitted what?
compressed how?
based on which state?
```

这对 observability 和 evaluation 都很重要。

---
