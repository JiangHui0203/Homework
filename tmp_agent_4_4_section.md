### 4.4 Long-term Memory

如果说 4.3 Short-term Memory 解决的是：

> **近期哪些信息值得暂时保留，并在接下来的若干步骤中复用？**

那么 Long-term Memory 解决的是更长期的问题：

> **哪些信息即使跨越当前 Task、Episode、Session 甚至较长时间之后，仍然值得影响未来决策？**

Long-term Memory 不是简单的“永久保存”，而是一套长期信息治理机制：

```text
Experience / Observation / Feedback
        ↓
Candidate Memory
        ↓
Write Gate
        ↓
Normalize / Abstract / Ground
        ↓
Validate / De-duplicate / Resolve Conflict
        ↓
Scope / Permission / Retention Check
        ↓
Persist + Index
        ↓
Future Retrieval
        ↓
Use
        ↓
Revise / Supersede / Consolidate / Forget
```

因此先记住本节最核心的一句话：

> **Long-term Memory 的目标不是“记住更多”，而是长期保留那些未来仍有决策价值、且能够被更新、追溯、隔离和删除的信息。**

---

#### 4.4.1 什么是 Long-term Memory？

在本文中，Long-term Memory 指：

> **跨越当前活跃任务或短期上下文生命周期，由 Agent 系统持久保留、未来可重新检索并影响决策的信息。**

关键词有三个：

```text
cross-episode / cross-session
persistent
retrievable
```

如果一条信息只在当前模型调用中存在，它是 Context。

如果只在当前任务运行过程中维护，它更接近 Working State 或 Short-term Memory。

如果任务结束后仍被保留，并在未来任务中重新发挥作用，才进入 Long-term Memory 的典型范围。

---

#### 4.4.2 Long-term Memory 为什么不是“永久存储”？

“长期”描述的是：

```text
retention horizon
```

而不是：

```text
never delete
```

真实系统里，长期记忆仍然应该支持：

```text
update
supersede
expire
archive
forget
delete
revoke
```

因此：

> **Persistent ≠ Immutable ≠ Permanent。**

长期记忆如果只能增加、不能修正和删除，最终一定会积累 stale、conflicting、sensitive 或错误信息。

---

#### 4.4.3 Long-term Memory 的四类核心形态

本知识体系采用四类核心记忆：

```text
Long-term Memory
├── Semantic Memory
├── Episodic Memory
├── Procedural Memory
└── User Memory
```

它们不是互斥存储引擎，而是语义分类。

同一套数据库中完全可以同时保存四类 Memory Item。

---

#### 4.4.4 Semantic Memory 是什么？

Semantic Memory 保存：

> **相对稳定、可概括、脱离某一次具体经历仍有意义的事实、关系和知识。**

例如：

```text
项目主分支是 main
服务 A 依赖数据库 B
客户 C 的正式合同编号是 X17
团队代码规范要求 Python 3.12
用户明确指定默认输出语言为中文
```

它强调：

```text
what is known
```

而不是：

```text
when one particular event happened
```

---

#### 4.4.5 Semantic Memory 不等于“任何事实”

一个事实是否值得长期保存，还取决于：

```text
future utility
stability
scope
confidence
sensitivity
cost
```

例如：

```text
“当前网页滚动到了 63%”
```

虽然是事实，但通常没有跨 Session 的长期价值。

所以：

> **Fact ≠ Long-term Semantic Memory。**

Long-term write 仍然需要选择。

---

#### 4.4.6 Episodic Memory 是什么？

Episodic Memory 保存：

> **某一次具体经历、事件或交互在什么时间、什么上下文下发生，以及结果如何。**

例如：

```text
2026-10-18
用户在项目 P 中尝试方案 A
A 因接口版本不兼容失败
随后改用方案 B 成功
```

Episodic Memory 典型结构包含：

```text
time
context
action
observation
outcome
participants
artifacts
```

它强调：

```text
what happened
```

---

#### 4.4.7 Episode Log 不等于 Episodic Memory

完整 trajectory / log 记录：

```text
发生过的一切
```

Episodic Memory 则应该保留：

```text
未来可能有价值的经历表示
```

所以：

```text
Raw Episode Log
      ↓ select / summarize / structure
Episodic Memory
```

而不是：

```text
所有日志永久塞进 Memory
```

---

#### 4.4.8 Procedural Memory 是什么？

Procedural Memory 保存：

> **“如何做”——可复用的方法、策略、操作顺序、经验规则或执行模式。**

例如：

```text
遇到该仓库测试失败时：
先运行 targeted tests
再检查 public API diff
最后运行 full suite
```

或者：

```text
查询客户前先 resolve tenant
再按 stable customer_id 查询
不要直接依赖 display name
```

它强调：

```text
how to do
```

---

#### 4.4.9 Procedural Memory ≠ Skill

后面 Chapter 5 会讲 Skill。

这里先固定边界：

```text
Procedural Memory
= 可被未来决策参考的“做法 / 经验规则”

Skill
= 被包装成更明确、可调用、可复用的能力单元
```

例如：

```text
“修改配置前先备份并验证 schema”
```

可以只是 Procedural Memory。

而：

```text
safe_config_update(...)
```

可能已经被工程化成 Skill / Tool / Workflow。

所以：

> **Procedural Memory 可以成为 Skill Acquisition 的原材料，但两者不是同一个概念。**

---

#### 4.4.10 User Memory 是什么？

User Memory 保存：

> **与特定用户持续交互有关、且未来仍可能提升任务质量的长期信息。**

例如用户明确表达的：

```text
preferred language
preferred output format
长期项目名称
稳定工作流偏好
明确要求保留的约束
```

它的核心是：

```text
user-specific
cross-session
future-useful
```

---

#### 4.4.11 User Memory 不等于“用户画像越详细越好”

长期保存用户信息会带来：

```text
privacy risk
incorrect inference
over-personalization
sensitive attribute leakage
staleness
```

因此：

> **长期 User Memory 必须服从数据最小化，而不是追求画像最大化。**

应该优先保存：

```text
明确
稳定
任务相关
可解释
未来有用
```

的信息。

---

#### 4.4.12 Explicit User Memory 与 Inferred User Memory

二者风险完全不同。

##### Explicit

```text
用户明确说：
“以后代码示例默认用 Python。”
```

##### Inferred

```text
系统根据若干次行为猜测：
“用户应该偏好 Python。”
```

因此 Memory Item 最好标记：

```text
source_type = explicit | inferred
```

并且：

> **Inferred Memory 的 confidence、适用范围和更新策略应比 Explicit Memory 更保守。**

---

#### 4.4.13 不应把敏感推断自动写成 User Memory

系统不应该因为若干对话就自动持久推断：

```text
健康状况
宗教
政治立场
性取向
犯罪历史
其他高敏感属性
```

长期记忆是持久 Side Effect。

因此：

> **Memory Write 本身需要 Privacy / Permission Policy。**

---

#### 4.4.14 Long-term Memory 与 Short-term Memory 的核心区别

可以记成：

```text
Short-term Memory
= 近期任务邻域中的暂存信息

Long-term Memory
= 跨任务 / Session 仍值得保留的信息
```

但边界不是只由时间决定。

更重要的是：

```text
Scope
Durability
Expected Future Utility
```

---

#### 4.4.15 时间长短不是唯一标准

一条信息即使只保存一天，也可能是 Long-term Memory：

```text
跨多个 Session
跨多个 Episode
```

另一条信息即使在同一 Session 中存在数小时，也可能只是 Working State。

所以：

> **Memory type 主要由语义角色与生命周期决定，不只是 wall-clock duration。**

---

#### 4.4.16 Long-term Memory 与 Working State 的区别

Working State 回答：

```text
当前任务现在是什么状态？
```

Long-term Memory 回答：

```text
过去哪些知识 / 经验值得未来任务再次使用？
```

例如：

```text
Working State:
current_branch = feature-x

Long-term Semantic Memory:
repo default branch = main
```

---

#### 4.4.17 Long-term Memory 与 Context 的区别

Memory 是：

```text
stored information
```

Context 是：

```text
currently model-visible information
```

典型链路：

```text
Long-term Memory
      ↓ retrieval / selection
Context_t
      ↓
Model
```

因此：

> **Memory 可以存在但不进入当前 Context。**

---

#### 4.4.18 Long-term Memory 与 Transcript 的区别

Transcript 保存：

```text
对话历史
```

Long-term Memory 保存：

```text
从历史中选择、结构化、更新后值得长期复用的信息
```

所以：

```text
Transcript
≠
Memory
```

否则历史里的旧约束、玩笑、猜测和错误信息都会永久污染未来决策。

---

#### 4.4.19 Long-term Memory 与 Model Weights 的区别

这是一个关键边界。

```text
External Long-term Memory
= 模型之外可独立读写的信息层

Model Weights
= 模型参数中编码的能力与统计规律
```

External Memory 通常可以：

```text
inspect
edit
delete
version
audit
scope
attach provenance
```

模型参数通常不能以同样粒度做到这些。

所以：

> **Memory Update ≠ Model Training。**

---

#### 4.4.20 Long-term Memory 与 Continual Learning 的区别

Continual Learning 往往改变：

```text
model parameters
```

Long-term Memory 往往改变：

```text
external persistent information state
```

二者可以组合：

```text
Experience
├── write to memory
└── later become training data
```

但不能混成一个概念。

---

#### 4.4.21 Long-term Memory 的基本生命周期

一个可靠生命周期至少包括：

```text
Observe / Experience
      ↓
Candidate Generation
      ↓
Write Decision
      ↓
Encoding
      ↓
Validation
      ↓
Conflict Resolution
      ↓
Persistence
      ↓
Indexing
      ↓
Retrieval / Use
      ↓
Update / Supersede / Forget
```

任何一环都可能出错。

---

#### 4.4.22 Experience ≠ Memory

Agent 经历了某件事，只代表：

```text
event happened
```

不代表：

```text
should persist forever
```

例如：

```text
一次临时 API timeout
```

可能不值得长期记忆。

但：

```text
同一 API 在特定版本下持续不兼容
```

可能值得形成长期知识。

---

#### 4.4.23 Candidate Memory

更合理的流程是先生成：

```text
Candidate Memory
```

然后再判断是否长期写入。

Candidate 可以来自：

```text
Observation
Successful Episode
Failure Episode
User Correction
Verified Fact
Repeated Pattern
Reflection
```

但：

> **Candidate ≠ Accepted Memory。**

---

#### 4.4.24 Long-term Memory Write Gate

Write Gate 可以考虑：

```text
future utility
stability
novelty
confidence
verification
scope
sensitivity
retention cost
risk
```

抽象写成：

$$
Write(m)=\mathbb{1}[U_{future}(m)-C(m)-R(m)>\tau]
$$

这里不是要求真的拟合公式，而是强调：

> **长期写入是一种选择决策，不是默认副作用。**

---

#### 4.4.25 什么信息通常值得长期写？

常见候选包括：

```text
稳定事实
重复出现的偏好
长期项目约束
高价值成功经验
高代价失败教训
被用户明确纠正的旧信息
可复用流程规则
长期实体关系
```

---

#### 4.4.26 什么信息通常不值得长期写？

例如：

```text
临时页面位置
一次随机采样结果
一次无代表性的瞬时错误
当前 token-level uncertainty
很快失效的中间变量
未经验证的模型猜测
无未来任务价值的闲聊细节
```

原则是：

> **Long-term Memory 应优化 Future Decision Utility，而不是 Storage Coverage。**

---

#### 4.4.27 Memory Write 是 Side Effect

Long-term Memory 会影响未来行为。

所以：

```text
write_memory(...)
```

本质上也是一种 effectful action。

尤其 User Memory：

```text
保存
修改
删除
共享
```

都应当受到权限与审计控制。

---

#### 4.4.28 Memory Item 最好是结构化对象

不要只保存裸文本：

```text
“用户喜欢简洁回答。”
```

更可靠的 Memory Item 可以包含：

```text
memory_id
memory_type
subject
content
scope
source
source_type
created_at
updated_at
valid_from
valid_until
confidence
verification_status
trust
sensitivity
owner
version
supersedes
related_memories
retrieval_keys
```

这样后续才有更新、冲突和权限语义。

---

#### 4.4.29 Memory ID 为什么重要？

如果 Memory 没有稳定 ID：

```text
更新哪条？
删除哪条？
谁覆盖了谁？
引用的是哪个版本？
```

都会变得模糊。

所以长期 Memory 应当是：

```text
addressable object
```

而不是一堆匿名 chunk。

---

#### 4.4.30 Scope 是长期记忆的核心字段

Memory 可以属于：

```text
user
project
workspace
organization
agent
team
tenant
```

例如：

```text
“默认分支是 main”
```

可能只对某个 Repository 有效。

如果错误提升到 global scope，就会污染其他任务。

---

#### 4.4.31 Scope Leakage

典型错误：

```text
Project A 的配置规则
↓
被写成全局 Memory
↓
Project B 也按 A 的规则执行
```

因此：

> **长期 Memory 必须显式回答：这条信息对谁、在哪个环境、哪些任务有效？**

---

#### 4.4.32 Cross-user Isolation

不同用户的 Memory 必须隔离。

风险包括：

```text
user A preference
→ retrieved for user B

user A private project info
→ leaked into user B context
```

所以：

```text
tenant / user / workspace scope
```

不能只依靠 embedding similarity。

必须先做权限过滤。

---

#### 4.4.33 Provenance 为什么必须长期保留？

一条长期事实如果几年后被取回，系统仍应该知道：

```text
它从哪里来的？
谁说的？
是观察还是推断？
是否验证过？
```

否则：

```text
Memory
→ 无来源断言
```

会逐渐变成难以纠正的伪事实。

---

#### 4.4.34 Verified Fact 与 Inferred Memory 要分开

例如：

```text
User: “我的默认输出语言是中文。”
```

可以记为：

```text
verification_status = explicit_user_statement
```

而：

```text
模型根据最近 3 次对话猜测用户偏好中文
```

应该记为：

```text
source_type = inferred
confidence < 1
```

二者不能同等对待。

---

#### 4.4.35 Confidence 不是 Truth Probability 的完美替代

Memory 的 confidence 可以辅助：

```text
是否写入
是否需要确认
冲突时谁优先
是否进入 Context
```

但不能机械理解为：

```text
0.9 = 90% 真
```

它更像：

```text
系统当前对这条 Memory 的证据强度 / 使用置信
```

---

#### 4.4.36 Long-term Memory 需要时间语义

至少区分：

```text
created_at
updated_at
valid_from
valid_until
```

例如：

```text
“负责人是 Alice”
```

可能在 2026-01 有效，2026-10 已经无效。

如果没有 valid-time：

```text
旧事实
```

会被误当成当前事实。

---

#### 4.4.37 Updated At ≠ Valid From

一个事实可能今天才被系统知道：

```text
updated_at = today
```

但它描述的是：

```text
valid_from = last month
```

这两个时间语义不能混。

在复杂系统里甚至可以进一步采用：

```text
valid time
transaction time
```

的双时间模型。

---

#### 4.4.38 Supersession 比覆盖更可审计

用户原来偏好：

```text
输出英文
```

后来明确改成：

```text
输出中文
```

更好的模型不是简单删除历史，而是：

```text
M1: English   [superseded]
M2: Chinese   [active, supersedes=M1]
```

这样可以知道：

```text
现在什么有效
为什么改变
```

---

#### 4.4.39 In-place Update vs Append-only History

两种模式各有用途：

```text
Current View
= 当前有效值

History Log
= 所有变化记录
```

成熟系统通常同时需要：

```text
read current state quickly
+
audit historical evolution
```

---

#### 4.4.40 Memory Contradiction

长期 Memory 中非常常见：

```text
M1: Project uses Python 3.11
M2: Project uses Python 3.12
```

不能简单：

```text
两条一起塞进 Context
```

应该判断：

```text
scope
time
source
verification
version
```

再做 conflict resolution。

---

#### 4.4.41 冲突不一定意味着其中一条错

例如：

```text
Project A uses Python 3.11
Project B uses Python 3.12
```

如果 Scope 丢失，就会看起来矛盾。

所以长期 Memory 的冲突判断必须：

> **先对齐实体、范围和时间，再判断事实冲突。**

---

#### 4.4.42 User Correction 应具有高优先级

如果用户明确纠正：

```text
“不是 A，是 B。”
```

系统应该：

```text
定位旧 Memory
↓
标记 superseded / incorrect
↓
写入修正 Memory
↓
更新索引
```

而不是：

```text
再追加一句 B
```

让 A 和 B 以后同时被检索出来。

---

#### 4.4.43 Memory Correction ≠ Memory Deletion

有时应保留历史 lineage：

```text
old value
→ superseded
```

有时必须真正删除：

```text
privacy deletion
legal deletion
user request
secret exposure
```

所以：

```text
correct
supersede
delete
```

需要不同语义。

---

#### 4.4.44 Tombstone

长期 Memory 删除后，如果索引、缓存或副本仍存在，可能被重新检索。

因此系统可以使用：

```text
tombstone / deletion marker
```

告诉下游：

```text
该 Memory 不再允许作为有效信息使用
```

---

#### 4.4.45 Hard Delete 与 Soft Delete

##### Soft Delete

```text
保留记录
active = false
```

适合：

```text
audit
supersession
history
```

##### Hard Delete

```text
物理移除
```

适合某些：

```text
privacy / security / legal requirements
```

具体策略取决于系统约束。

---

#### 4.4.46 Long-term Forgetting 是必要能力

随着 Memory 增长：

```text
retrieval noise ↑
staleness ↑
conflict ↑
privacy surface ↑
index cost ↑
```

所以 Forgetting 不是失败。

> **可控遗忘是长期记忆系统的健康机制。**

---

#### 4.4.47 TTL 与 Long-term Retention Policy

长期记忆也可以有：

```text
TTL
```

例如：

```text
临时项目偏好：90 天
临时访问上下文：7 天
长期显式用户偏好：直到修改
```

但不能只靠 TTL。

---

#### 4.4.48 Semantic Expiry 仍然重要

例如：

```text
“用户当前在做毕业论文项目 P”
```

项目结束后：

```text
即使 TTL 没到
也可能不应继续作为 active memory
```

所以：

```text
semantic invalidation
```

比单纯时间更重要。

---

#### 4.4.49 Memory Decay

某些系统可以让 Memory relevance 随时间衰减：

$$
score_t(m)=score_0(m)\cdot e^{-\lambda \Delta t}
$$

但需要注意：

```text
old
≠
wrong
```

有些稳定事实即使很久以前写入，仍然有效。

所以 decay 应与：

```text
memory type
freshness
verification
scope
```

联合使用。

---

#### 4.4.50 Usage-based Retention

也可以根据：

```text
retrieval frequency
successful use
recent confirmation
```

调整保留优先级。

但：

> **Frequently retrieved ≠ Correct。**

错误 Memory 如果频繁被召回，反而可能形成自我强化。

---

#### 4.4.51 Self-reinforcing Memory Loop

危险链路：

```text
错误 Memory
↓ retrieved
模型据此行动
↓
产生与旧 Memory 一致的文本
↓
再次写回
↓
confidence 上升
```

这会把错误从偶然变成稳定系统偏差。

因此：

> **Memory 不能仅根据“被使用过”自动提高可信度。**

---

#### 4.4.52 Memory Consolidation 是什么？

Memory Consolidation 指：

> **把多个较具体、零散或重复的经历，整理成更稳定、更抽象、未来更容易复用的长期表示。**

例如：

```text
Episode 1: 方法 A 在环境 X 因权限失败
Episode 2: 方法 A 在环境 X 再次因权限失败
Episode 3: 方法 B 成功
```

可能整理成：

```text
Procedural Memory:
环境 X 中不要走 A；优先使用 B
```

---

#### 4.4.53 Consolidation ≠ Summarization

Summary 只是压缩表达。

Consolidation 还涉及：

```text
cross-event pattern
abstraction
conflict resolution
validation
scope assignment
```

所以：

```text
Summary
≠
Generalized Knowledge
```

---

#### 4.4.54 Single Episode 不应轻易变成 General Rule

一次成功：

```text
A worked once
```

不能直接固化成：

```text
Always use A
```

否则会发生：

```text
anecdote → policy overgeneralization
```

因此 Procedural Consolidation 要考虑：

```text
sample count
context similarity
counterexamples
failure cases
confidence
```

---

#### 4.4.55 Episodic → Semantic Consolidation

例如多个 Episode：

```text
项目 P 在多次执行中均使用 Python 3.12
```

经过验证后，可形成：

```text
Semantic Memory:
Project P runtime = Python 3.12
```

这就是：

```text
specific experiences
↓
stable fact
```

---

#### 4.4.56 Episodic → Procedural Consolidation

例如多个 Episode 显示：

```text
先跑 full suite 很慢
先跑 targeted test 更高效
```

可以形成：

```text
Procedural Memory:
优先 targeted verification，再 full verification
```

---

#### 4.4.57 Short-term → Long-term Consolidation

4.3 中的 Short-term Memory 可能经过一段时间后：

```text
仍被多次使用
持续有效
具有跨任务价值
```

于是被提升为 Long-term Memory。

所以：

```text
Short-term Memory
     ↓ consolidation
Long-term Memory
```

不是自动发生的。

---

#### 4.4.58 Consolidation 应保留 Lineage

长期规则最好能追溯：

```text
由哪些 Episode 支持？
依据哪些 Observation？
有没有反例？
```

否则抽象后的规则会失去可解释性。

因此可以维护：

```text
derived_from = [episode_17, episode_23, episode_51]
```

---

#### 4.4.59 Memory Abstraction 的风险

抽象过度：

```text
specific rule
↓
very general rule
```

可能导致：

```text
scope expansion
loss of exceptions
overgeneralization
```

所以长期 Memory 应保留：

```text
applicable_when
not_applicable_when
```

这类条件。

---

#### 4.4.60 Procedural Memory 应记录 Preconditions

不要只保存：

```text
“使用方法 B。”
```

更好的是：

```text
IF environment = X
AND permission = P
THEN prefer B
```

否则方法会被错误迁移到不适用环境。

---

#### 4.4.61 Procedural Memory 应记录 Outcome Evidence

例如：

```text
strategy = targeted-test-first
observed benefit = lower latency
sample_count = 12
affected repo = P
```

比：

```text
“targeted tests are better”
```

更可审计。

---

#### 4.4.62 User Memory 的更新应该以最新明确表达为准

用户偏好会变化。

例如：

```text
过去：回答尽量详细
现在：回答尽量简洁
```

系统不应该平均两个偏好。

应该：

```text
new explicit statement
→ supersede old preference
```

---

#### 4.4.63 Over-personalization

长期 Memory 可能让 Agent 过度依赖历史：

```text
以前用户喜欢 A
↓
当前问题其实更适合 B
↓
Agent 仍强行给 A
```

所以 User Memory 是：

```text
contextual prior
```

而不是：

```text
absolute rule
```

除非用户明确给了硬约束。

---

#### 4.4.64 Memory Should Inform, Not Override Reality

如果长期 Memory 说：

```text
service endpoint = old.example.com
```

但当前 Environment / official config 明确显示：

```text
new.example.com
```

应优先采用新鲜权威证据。

因此：

```text
Current Authoritative State
>
Stale Long-term Memory
```

---

#### 4.4.65 Memory 与 Source of Truth

长期 Memory 通常不是所有事实的最终 Source of Truth。

例如：

```text
账户余额
库存
Git HEAD
订单状态
权限状态
```

这些应以真实 Environment / authoritative service 为准。

Memory 更适合保存：

```text
reference
summary
historical knowledge
preferences
experience
```

---

#### 4.4.66 Memory Pointer 比复制权威数据更稳

对于频繁变化的数据，可以保存：

```text
resource_id
source_location
retrieval method
```

而不是复制一份值。

例如：

```text
customer_profile_id = C184
```

未来再从权威系统查询当前状态。

这样可以减少 stale copy。

---

#### 4.4.67 Long-term Memory 的存储形式

可以使用：

```text
Relational DB
Document Store
Key-Value Store
Vector Store
Graph Store
Hybrid Store
```

关键不在于数据库名字，而是：

```text
数据模型
查询方式
版本
权限
更新
删除
索引
```

能否满足 Memory 语义。

---

#### 4.4.68 Vector Store ≠ Memory System

Vector Store 主要解决：

```text
similarity retrieval
```

而长期 Memory 还需要：

```text
write policy
scope
version
conflict
supersession
privacy
deletion
provenance
freshness
```

所以：

> **向量库只是 Memory System 的一种索引 / 存储组件，不等于 Memory 本身。**

---

#### 4.4.69 Memory Record 与 Retrieval Index 应区分

可以有：

```text
Canonical Memory Record
        ↓
Derived Indexes
├── embedding
├── keyword
├── graph edge
└── metadata index
```

Canonical Record 是权威内容。

Index 是为了更快查找。

这样更新 / 删除时语义更清楚。

---

#### 4.4.70 Index Lag

如果 Memory 已经更新：

```text
canonical = new value
```

但 vector index 仍然是旧版本：

```text
retrieval → stale memory
```

所以要关注：

```text
write-to-index latency
index version
reindex status
```

---

#### 4.4.71 Delete Propagation

删除 Memory 后，还要考虑：

```text
vector index
cache
replica
summary
search index
backup policy
```

否则：

```text
record deleted
≠
information no longer retrievable
```

这对隐私特别重要。

---

#### 4.4.72 Memory Cache ≠ Memory Store

缓存可以提高读取速度，但：

```text
cache
```

通常不是长期真相源。

应注意：

```text
cache invalidation
version
TTL
```

否则会出现：

```text
memory updated
cache still old
```

---

#### 4.4.73 Memory Write 与 Retrieval Indexing 可以异步，但要显式状态化

例如：

```text
memory persisted = true
index_ready = false
```

不要假装：

```text
write success
→ immediately retrievable everywhere
```

这对最终一致系统非常重要。

---

#### 4.4.74 Long-term Memory 也需要 Permission Boundary

不是所有 Agent / Tool 都应该能：

```text
read all memories
write all memories
delete all memories
```

可以区分：

```text
read scope
write scope
update scope
delete scope
share scope
```

---

#### 4.4.75 Memory Least Privilege

一个 Coding Agent 修当前 Repo：

```text
可能需要 project memory
```

但通常不需要：

```text
其他用户的 private memory
其他项目的 confidential notes
```

所以：

> **Memory Retrieval 也必须 obey Least Privilege。**

---

#### 4.4.76 Secrets 不应该作为普通 Long-term Memory

例如：

```text
API key
password
OAuth token
private key
```

应该由：

```text
Secret Manager / Runtime Credential Store
```

管理。

Memory 可以保存：

```text
credential reference
```

但不应把 secret 明文送入一般 Memory / Context 流程。

---

#### 4.4.77 Long-term Memory Poisoning

攻击者可以试图让 Agent 记住：

```text
恶意指令
错误事实
伪造偏好
错误操作规则
```

如果进入长期 Memory，影响会跨 Session 持续。

因此：

```text
Memory Write
```

是高价值 Trust Boundary。

---

#### 4.4.78 Indirect Prompt Injection → Persistent Memory Poisoning

攻击链：

```text
malicious webpage
↓
Observation
↓
Agent summarizes it
↓
write long-term memory
↓
future session retrieval
↓
malicious instruction resurfaces
```

所以外部不可信内容不能因为“写进 Memory”就升级成 trusted instruction。

---

#### 4.4.79 Memory 中必须保留 Instruction / Data 边界

例如一条网页 Memory：

```text
“This document says: ignore previous instructions ...”
```

它应被理解为：

```text
quoted external data
```

不是：

```text
future system instruction
```

---

#### 4.4.80 Memory Provenance 需要跨 Session 保持

不能：

```text
当前轮知道来源是网页
↓
写入 Memory 后只剩正文
↓
未来取回时来源丢失
```

否则 trust boundary 会在持久化时消失。

---

#### 4.4.81 Memory Audit Log

高价值 Long-term Memory 应能回答：

```text
谁写的？
何时写的？
为什么写？
由什么证据支持？
谁更新过？
谁删除过？
什么时候被使用？
```

这对 debug、privacy 和 incident response 都重要。

---

#### 4.4.82 Memory Versioning

Memory Item 更新时可以维护：

```text
version = 1, 2, 3 ...
```

这样 Retrieval / Context Trace 可以记录：

```text
使用的是哪个版本
```

避免后来更新后无法复现实验。

---

#### 4.4.83 Memory Snapshot 与 Historical Replay

为了复现实验，有时需要：

```text
memory snapshot at time t
```

否则今天重新跑昨天的 Agent：

```text
Memory 已经变了
```

结果无法比较。

所以 Memory 也是 Agent Eval 的实验条件之一。

---

#### 4.4.84 Memory 版本应进入实验协议

至少考虑记录：

```text
memory store snapshot
index version
write policy version
retrieval policy version
consolidation policy version
```

否则：

```text
same model + same prompt
```

也可能因为 Memory 状态不同得到完全不同结果。

---

#### 4.4.85 Long-term Memory 与 Multi-Agent

多 Agent 系统可以有：

```text
Private Memory
Shared Memory
Team Memory
Project Memory
```

但最难的不是“共享读取”，而是：

```text
谁可以写？
谁可以覆盖？
如何处理冲突？
如何标记来源？
```

---

#### 4.4.86 Shared Memory 的写权限应更严格

因为：

```text
one agent writes wrong memory
↓
many agents retrieve it
↓
error amplification
```

所以 Shared Long-term Memory 往往需要：

```text
validation
review
confidence
ownership
versioning
```

比 Private Scratch Memory 更严格。

---

#### 4.4.87 Organizational Memory

团队 / 组织也可以有长期 Memory：

```text
verified procedures
architecture decisions
known incidents
project conventions
validated lessons
```

它更接近：

```text
shared semantic / procedural memory
```

但仍然需要权限和治理。

---

#### 4.4.88 Long-term Memory 与 Knowledge Base 的关系

Knowledge Base 往往强调：

```text
组织知识的外部存储
```

Agent Long-term Memory 更强调：

```text
信息如何从 Agent Experience 被写入
如何影响未来 Agent Decision
```

所以二者有重叠，但不完全等价。

---

#### 4.4.89 Memory Consolidation 与 Knowledge Curation

如果 Long-term Memory 越来越重要，它就需要像数据资产一样：

```text
review
quality control
lineage
retention
access control
cleanup
```

因此长期 Memory 最终会从：

```text
agent feature
```

变成：

```text
managed information system
```

---

#### 4.4.90 Long-term Memory 的 Failure Localization

当 Agent “记错了”时，不要直接归因给模型。

可以沿链路排查：

```text
Should memory have been written?
        ↓
Write decision correct?
        ↓
Encoding correct?
        ↓
Persisted successfully?
        ↓
Indexed correctly?
        ↓
Updated / superseded correctly?
        ↓
Retrieved correct version?
        ↓
Selected into Context?
        ↓
Model consumed it correctly?
```

---

#### 4.4.91 Write Precision 与 Write Recall

长期写入策略有经典 trade-off。

##### Write Recall 太低

```text
重要信息没记住
```

##### Write Precision 太低

```text
什么都记
→ noise / privacy / stale memory
```

所以不能只追求：

```text
Memory Capture Rate
```

---

#### 4.4.92 Memory Update Accuracy

需要评价：

```text
旧事实变化后
系统能否正确 supersede / revise？
```

这通常比初次写入更难。

例如测试：

```text
Session 1: preference = A
Session 2: preference = B
Session 3: ask again
```

正确行为应基于 B。

---

#### 4.4.93 Conflict Resolution Accuracy

可以构造：

```text
old source
new authoritative source
inferred memory
explicit user correction
```

测试系统是否能正确排序：

```text
freshness
source authority
explicit correction
scope
```

---

#### 4.4.94 Stale Memory Incident Rate

一个很重要的指标：

$$
\text{Stale Memory Incident Rate}
=
\frac{\text{决策被过时 Memory 错误影响的次数}}
{\text{Memory-assisted decisions}}
$$

因为长期 Memory 最大风险之一就是：

```text
曾经正确
现在错误
```

---

#### 4.4.95 Memory-induced Harm

Memory 提升一些任务的同时，也可能让原本正确的任务变错。

所以可以看：

```text
Memory Rescue
-
Memory-induced Harm
```

也就是：

> **不要只统计“有 Memory 后多答对多少”，还要统计“错误 Memory 又毁掉多少”。**

---

#### 4.4.96 Long-term Memory 的 End-to-End Evaluation

可以比较：

```text
No Memory
vs
Short-term Only
vs
Long-term Memory
vs
Long-term + Consolidation
vs
Long-term + Update / Forgetting
```

指标包括：

```text
Task Success
Cross-session Recall
Update Accuracy
Stale-memory Harm
Privacy Incidents
Cross-user Leakage
Retrieval Cost
Latency
Memory Size
```

---

#### 4.4.97 真正的 Long-term Memory Benchmark 应有跨 Session 延迟依赖

如果信息刚出现就立即提问：

```text
更像 context utilization
```

更合理测试：

```text
Session 1: information appears
Session 2: unrelated tasks
Session 3: old information needed
```

甚至：

```text
Session 4: information updated
Session 5: verify old memory no longer dominates
```

---

#### 4.4.98 Memory Update Benchmark

至少应覆盖：

```text
add
correct
supersede
expire
delete
```

因为现实 Long-term Memory 的难点通常不是：

```text
第一次记住
```

而是：

```text
世界变化以后还能保持正确
```

---

#### 4.4.99 Memory Privacy Benchmark

需要测试：

```text
cross-user leakage
cross-project leakage
sensitive retrieval
unauthorized memory write
unauthorized deletion
prompt-injection persistence
```

不能只看 recall。

---

#### 4.4.100 Memory Counterfactual Test

固定：

```text
Task
Model
Tools
```

只改变 Memory：

```text
correct memory
stale memory
conflicting memory
no memory
malicious memory
```

观察 Agent Decision 是否符合预期。

这能直接测：

> **Agent 对 Memory 的依赖是否合理。**

---

#### 4.4.101 Memory Ablation

可以消融：

```text
without provenance
without timestamp
without confidence
without scope
without supersession
without consolidation
without forgetting
```

观察：

```text
Task Success
Stale Errors
Privacy Errors
Conflict Errors
```

从而评价不同 Memory Policy 的真实贡献。

---

#### 4.4.102 Coding Agent 的 Long-term Memory 例子

跨多个任务，系统积累：

```text
Semantic:
repo default branch = main
repo uses Python 3.12

Episodic:
2026-10-10 某次升级因 dependency X 失败

Procedural:
先运行 targeted tests，再 full suite

User / Project:
不要修改 public API
```

新 Task 到来时：

```text
retrieve relevant memories
↓
validate against current repo state
↓
build context
↓
act
```

注意：

> 仍然要检查当前 Git / config，不能只信旧 Memory。

---

#### 4.4.103 Research Agent 的 Long-term Memory 例子

长期保存：

```text
Semantic:
研究问题定义
稳定术语
已确认的数据集信息

Episodic:
曾经尝试过哪些检索策略
哪些来源后来被证伪

Procedural:
关键结论优先核查原始论文

User:
用户偏好的引用格式
```

这样新研究任务可以复用历史经验，但仍应对最新事实重新搜索。

---

#### 4.4.104 Customer-support Agent 的 Long-term Memory 例子

可以保存：

```text
客户稳定配置
长期产品偏好
历史已解决事件
```

但：

```text
当前账户余额
当前订单状态
当前权限
```

仍应从权威系统实时查询。

这体现：

```text
Memory
≠
Live Operational State
```

---

#### 4.4.105 Failure Mode 1：Everything Becomes Memory

表现：

```text
每句话都写
每个 Tool Result 都写
每个模型猜测都写
```

后果：

```text
noise
cost
privacy risk
retrieval confusion
```

修复：

```text
Write Gate
```

---

#### 4.4.106 Failure Mode 2：Nothing Becomes Memory

系统表面有 Memory 模块，但写入策略过严：

```text
跨 Session 仍然反复问相同信息
```

这属于：

```text
write recall failure
```

---

#### 4.4.107 Failure Mode 3：Inference Becomes Fact

模型猜测：

```text
“用户可能喜欢 A”
```

被保存成：

```text
“用户喜欢 A”
```

这是典型：

```text
provenance loss
```

---

#### 4.4.108 Failure Mode 4：Stale Memory Dominates Fresh Evidence

旧 Memory：

```text
endpoint = A
```

当前官方配置：

```text
endpoint = B
```

Agent 仍使用 A。

修复：

```text
fresh authoritative evidence > stale memory
```

---

#### 4.4.109 Failure Mode 5：Superseded Memory Still Retrieved

用户已经改偏好，但旧版本仍高排名返回。

修复：

```text
active flag
supersedes link
index invalidation
```

---

#### 4.4.110 Failure Mode 6：Scope Leakage

Project A 的经验影响 Project B。

修复：

```text
scope-aware write + retrieval filter
```

---

#### 4.4.111 Failure Mode 7：Cross-user Leakage

A 用户 Memory 出现在 B 用户 Context。

这是严重安全问题。

修复必须依赖：

```text
tenant isolation
ACL
permission filter
```

而不是相似度阈值。

---

#### 4.4.112 Failure Mode 8：Memory Poisoning

恶意内容进入长期 Memory，并跨 Session 影响未来行为。

修复：

```text
trust label
provenance
write validation
instruction/data isolation
```

---

#### 4.4.113 Failure Mode 9：Over-consolidation

少数 Episode 被抽象成过强规则。

修复：

```text
counterexample check
scope
confidence
sample support
```

---

#### 4.4.114 Failure Mode 10：Under-consolidation

系统保存了成千上万重复 Episode，却从不形成稳定知识。

后果：

```text
retrieval noise
storage explosion
```

修复：

```text
periodic consolidation
```

---

#### 4.4.115 Failure Mode 11：No Forgetting

长期 Memory 永远增加。

最终：

```text
old truth + new truth + duplicates + noise
```

共同竞争 Retrieval。

---

#### 4.4.116 Failure Mode 12：Aggressive Forgetting

系统为了降低成本删除：

```text
长期稳定约束
重要失败教训
明确用户偏好
```

导致反复犯同样错误。

所以 forgetting 也需要 policy。

---

#### 4.4.117 Failure Mode 13：Index / Record Divergence

Canonical Memory 已修改，但 Index 仍返回旧内容。

需要：

```text
version-aware index
reindex
invalidation
```

---

#### 4.4.118 Failure Mode 14：Deleted Memory Resurfaces

主记录已删除，但：

```text
cache
summary
embedding index
backup restore
```

使内容重新出现。

需要端到端 delete semantics。

---

#### 4.4.119 Failure Mode 15：Memory Becomes Authority

系统把 Memory 当成最终真相源，停止查询实时 Environment。

这对：

```text
payment
inventory
permission
current version
```

尤其危险。

---

#### 4.4.120 Failure Mode 16：User Preference Becomes Hard Rule

过去的软偏好被当成不可违反约束。

需要区分：

```text
preference
constraint
policy
```

---

#### 4.4.121 Failure Mode 17：Memory Hallucination by Reconstruction

系统只保存摘要，后来根据摘要“重建”原始事实。

可能造成：

```text
summary drift
```

关键事实应保留引用 / 原始 evidence pointer。

---

#### 4.4.122 Failure Mode 18：Procedural Memory Without Preconditions

“方法 A 很好”被跨环境使用。

修复：

```text
applicability conditions
```

必须随 procedural memory 保存。

---

#### 4.4.123 Failure Mode 19：Memory Write Storm

Agent 每一步都大量写长期 Memory：

```text
latency ↑
cost ↑
index churn ↑
```

需要：

```text
batching
write threshold
consolidation schedule
```

---

#### 4.4.124 Failure Mode 20：Memory Read Storm

每一步都检索整个 Memory Store。

后果：

```text
latency
cost
noise
```

后面 4.6 Retrieval 会讲按需检索。

---

#### 4.4.125 Failure Mode 21：Memory Feedback Loop

模型根据 Memory 行动，行动结果再被自动写回为同一结论的“新证据”。

需要区分：

```text
independent evidence
vs
self-generated evidence
```

---

#### 4.4.126 Failure Mode 22：Unbounded User Profiling

系统把所有长期行为都汇总成越来越细的用户画像。

风险：

```text
privacy
bias
incorrect inference
creepy personalization
```

应坚持：

```text
data minimization
purpose limitation
```

---

#### 4.4.127 Long-term Memory 的 15 条工程原则

1. **Experience ≠ Memory：先筛选，再持久化。**
2. **External Memory ≠ Model Weights：保持可查看、可更新、可删除。**
3. **Scope First：每条 Memory 都要明确适用范围。**
4. **Provenance First：保留来源、时间和验证状态。**
5. **Fresh Authority Wins：实时权威事实优先于旧 Memory。**
6. **Supersede, Don’t Accumulate Contradictions：更新要有版本语义。**
7. **Forget Deliberately：可控遗忘是能力。**
8. **Consolidate with Evidence：不要把一次经历过度泛化。**
9. **Separate Record from Index：Canonical Memory 与 Retrieval Index 分离。**
10. **Permission Before Similarity：先权限过滤，再做相似度检索。**
11. **Memory Write Is a Side Effect：长期写入也需要治理。**
12. **Do Not Store Secrets as Ordinary Memory：凭证留在 Runtime / Secret Store。**
13. **Preserve Instruction/Data Boundary：不可信内容写入后仍然是不可信数据。**
14. **Evaluate Harm, Not Just Recall：统计 stale / poisoning / leakage 造成的损害。**
15. **Memory Should Improve Future Decisions：存储量不是目标，未来决策价值才是。**

---

#### 4.4.128 一个最小 Long-term Memory Schema

```json
{
  "memory_id": "mem_1847",
  "type": "semantic",
  "subject": "repo:project-p",
  "content": "Default branch is main.",
  "scope": {
    "workspace": "project-p"
  },
  "source": {
    "kind": "verified_repository_metadata",
    "ref": "repo_metadata_2026_10_18"
  },
  "created_at": "2026-10-18T10:00:00Z",
  "updated_at": "2026-10-18T10:00:00Z",
  "valid_from": "2026-10-18T10:00:00Z",
  "valid_until": null,
  "confidence": 1.0,
  "verification_status": "verified",
  "trust": "trusted_internal",
  "sensitivity": "normal",
  "version": 1,
  "supersedes": null,
  "active": true
}
```

真实系统不一定用这个 JSON，但语义最好类似。

---

#### 4.4.129 一个最小 Memory Write Pipeline

```python
candidate = extract_candidate(event)

if not write_policy.should_persist(candidate):
    return

memory = normalize(candidate)
memory = attach_scope(memory)
memory = attach_provenance(memory)

validate(memory)
check_permission(memory)

conflicts = find_conflicts(memory)
memory = resolve_conflicts(memory, conflicts)

record_id = persist(memory)
index(record_id)
```

注意：

```text
extract
≠
persist
```

中间有完整治理层。

---

#### 4.4.130 一个最小 Memory Update Pipeline

```python
current = load_active_memory(key)
new_fact = normalize(observation)

if stronger_or_fresher(new_fact, current):
    new_record = supersede(current, new_fact)
    persist(new_record)
    invalidate_indexes(current)
    index(new_record)
```

核心不是：

```text
append new text
```

而是：

```text
maintain current truth + history
```

---

#### 4.4.131 Memory Consolidation Pipeline

```text
Recent Episodes
      ↓
Cluster / Group Related Experiences
      ↓
Find Repeated Pattern
      ↓
Check Counterexamples
      ↓
Abstract Candidate Rule
      ↓
Validate Scope
      ↓
Attach Supporting Episodes
      ↓
Persist Semantic / Procedural Memory
```

这比：

```text
“让 LLM 总结一下最近经历”
```

更完整。

---

#### 4.4.132 Long-term Memory 与 Learning from Experience 的关系

Chapter 12 会进一步展开。

现在先记住：

```text
Long-term Memory
= 保存可复用经验的一种机制

Learning from Experience
= 如何利用过去 trajectory / feedback 改善未来行为
```

后者可以通过：

```text
Memory
Skill
Prompt Update
Policy Update
Training
```

等多种方式实现。

---

#### 4.4.133 Long-term Memory 与 RSI 的关系

Memory 增长本身不等于 RSI。

只有当：

```text
Agent 使用过去经验
↓
系统能力 /策略被持续改进
↓
改进后的系统又参与后续改进
```

才接近后面 RSI 的递归自改进框架。

所以：

```text
Remembering
≠
Self-Improving
```

---

#### 4.4.134 一个边界表

| 概念 | 核心问题 | 与 Long-term Memory 的关系 |
|---|---|---|
| Context | 当前模型看什么？ | Memory 被检索后可进入 Context |
| Working State | 当前任务必须知道什么？ | 当前执行状态，不等于长期记忆 |
| Short-term Memory | 近期暂时保留什么？ | 可被巩固为长期记忆 |
| Long-term Memory | 跨任务仍值得保留什么？ | 本节主体 |
| Semantic Memory | 长期事实 / 关系是什么？ | Long-term Memory 类型之一 |
| Episodic Memory | 过去具体发生了什么？ | 类型之一 |
| Procedural Memory | 以后怎么做更好？ | 类型之一 |
| User Memory | 对特定用户长期有用什么？ | 类型之一 |
| Transcript | 历史说过什么？ | Memory 的来源之一，不等于 Memory |
| Knowledge Base | 外部组织知识如何存储？ | 可与 Semantic Memory 重叠 |
| Vector Store | 如何做相似度索引？ | 组件，不等于 Memory System |
| Model Weights | 模型参数学到了什么？ | 与 External Memory 不同 |
| Skill | 可复用执行能力是什么？ | 可由 Procedural Memory 演化而来 |
| Persistence | 信息怎样跨时间存活？ | 4.5 的存储机制问题 |
| Retrieval | 未来怎样找到相关 Memory？ | 4.6 的访问问题 |

---

#### 4.4.135 面试时必须能回答的问题

**Q1：什么是 Long-term Memory？**

跨越当前任务 / Session，由系统持久保存、未来可重新检索并影响决策的信息。

---

**Q2：Long-term Memory 与 Short-term Memory 的区别？**

Short-term 面向近期任务邻域；Long-term 面向跨任务、跨 Session 的未来复用，关键差异是 scope、durability 与 expected future utility，而不只是时间长度。

---

**Q3：Semantic / Episodic / Procedural Memory 分别是什么？**

Semantic 保存稳定事实与关系；Episodic 保存具体经历与事件；Procedural 保存可复用的做法、策略和经验规则。

---

**Q4：User Memory 应该保存什么？**

优先保存用户明确、稳定、任务相关、未来有用且允许长期持有的信息，并遵循数据最小化，不追求无限画像。

---

**Q5：为什么 Vector Store 不等于 Memory System？**

向量库主要解决相似度查找；Memory System 还需要写入策略、scope、版本、冲突、删除、权限、provenance、freshness 和 consolidation。

---

**Q6：Memory 与 Model Weights 有什么区别？**

External Memory 是模型外部可独立读写、更新、删除和审计的信息层；Model Weights 是模型参数。Memory Write 不等于训练。

---

**Q7：为什么 Experience 不能自动写入长期 Memory？**

大量经历是临时、低价值、噪声或未经验证的；自动永久写入会造成噪声、隐私和错误积累，需要 Write Gate。

---

**Q8：什么是 Memory Consolidation？**

把多个相关具体经历整理成更稳定、更抽象、可复用的 Semantic / Procedural Memory，同时保留证据、scope 和反例检查。

---

**Q9：为什么单次成功不能直接变成 Procedural Rule？**

单一 Episode 可能偶然有效，直接泛化会产生 overgeneralization；需要重复证据、上下文条件和反例检查。

---

**Q10：为什么 Memory 需要 Provenance？**

未来取回时必须知道信息从哪来、是否是推断、是否验证、何时有效，否则错误内容会逐渐变成无来源“事实”。

---

**Q11：如何处理 Long-term Memory 冲突？**

先对齐 subject、scope 和 valid time，再比较来源权威性、新鲜度、验证状态；必要时 supersede，而不是把矛盾文本一起塞进 Context。

---

**Q12：为什么长期 Memory 需要 Forgetting？**

无限积累会增加 stale 信息、retrieval noise、隐私风险和成本；可控遗忘是长期健康机制。

---

**Q13：Memory Poisoning 是什么？**

恶意或错误内容被持久写入，跨 Session 被反复检索并影响未来决策。Memory Write 因此是重要 Trust Boundary。

---

**Q14：为什么当前权威状态应优先于旧 Memory？**

Memory 本质是历史持久信息，可能过时；对支付、库存、权限、Git HEAD 等实时状态应重新查询 Source of Truth。

---

**Q15：Procedural Memory 和 Skill 有什么区别？**

Procedural Memory 是未来可参考的经验规则；Skill 是更明确封装、可调用的能力。Procedural Memory 可以成为 Skill 的原材料。

---

**Q16：如何评价 Long-term Memory？**

不仅看跨 Session recall，还要看 write precision / recall、update accuracy、conflict resolution、stale-memory harm、privacy leakage、cross-user isolation 和最终任务收益。

---

**Q17：为什么删除 Memory 比删除一条数据库记录复杂？**

因为内容可能存在于向量索引、缓存、摘要、副本等派生层；删除需要端到端传播和失效。

---

**Q18：Long-term Memory 什么时候反而有害？**

当它 stale、错误、过度泛化、范围错误、泄露隐私、被攻击污染或压倒当前新鲜证据时，会让 Agent 比无 Memory 更差。

---

#### 4.4.136 一句话总结

> **Long-term Memory 是 Agent 的跨任务持久经验层：它不是“把历史永久保存”，而是把未来仍有决策价值的 Semantic、Episodic、Procedural 与 User-specific 信息，以带有 Scope、Provenance、Version、Freshness、Permission 与 Retention 语义的可治理对象长期保存，并允许 Consolidate、Supersede、Correct、Forget 与 Delete。可靠的长期记忆系统必须避免把 Memory 当作实时 Truth、把 Vector Store 当作 Memory 本身、把一次经历直接泛化成规则，也必须防止 stale memory、cross-user leakage、memory poisoning 与无法传播的删除。**

---

#### 4.4.137 参考资料

1. Tulving, E. **Episodic and Semantic Memory.** In *Organization of Memory*, 1972. 用于区分 episodic 与 semantic memory 的经典认知框架。
2. Squire, L. R. **Memory Systems of the Brain: A Brief History and Current Perspective.** *Neurobiology of Learning and Memory*, 2004. 用于理解不同长期记忆系统的基本划分。
3. Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. **Generative Agents: Interactive Simulacra of Human Behavior.** *UIST*, 2023. arXiv:2304.03442. 用于理解 observation、reflection 与 memory stream 在长期 Agent 行为中的作用。
4. Packer, C., Fang, V., Patil, S. G., Lin, K., Wooders, S., & Gonzalez, J. E. **MemGPT: Towards LLMs as Operating Systems.** arXiv:2310.08560, 2023. 用于理解有限 Context 与外部长期 Memory 分层管理。
5. Zhong, W., Guo, L., Gao, Q., et al. **MemoryBank: Enhancing Large Language Models with Long-Term Memory.** arXiv:2305.10250, 2023. 用于理解跨会话用户记忆与长期信息保留。
6. Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K., & Yao, S. **Reflexion: Language Agents with Verbal Reinforcement Learning.** *NeurIPS*, 2023. arXiv:2303.11366. 用于理解将任务反馈持久化为可复用经验的思路。
7. Wang, G., Xie, Y., Jiang, Y., et al. **Voyager: An Open-Ended Embodied Agent with Large Language Models.** arXiv:2305.16291, 2023. 用于理解 experience、skill library 与长期 procedural knowledge 的关系。
