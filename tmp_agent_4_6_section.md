### 4.6 Retrieval

#### 4.6.1 定义：Retrieval 到底是什么？

Retrieval 是从一个**当前没有完整进入模型 Context 的外部信息空间**中，根据当前任务、State、Query、权限与预算，选择一小部分候选信息供后续判断或生成使用的过程。

可以抽象为：

```text
Large External Information Space
        ↓
Query / Current State
        ↓
Candidate Retrieval
        ↓
Filter / Rerank / Select
        ↓
Retrieved Evidence
        ↓
Context Builder
        ↓
Model Decision
```

因此 Retrieval 不是“搜索一个向量库”这么窄，而是一类更一般的**信息选择机制**。

---

#### 4.6.2 Retrieval 的核心目标不是“找相似”，而是“找此刻有决策价值的信息”

相似只是可能有用的代理信号。

真正目标更接近：

```text
Retrieve items
that maximize downstream decision utility
under budget / freshness / trust / permission constraints
```

因此：

```text
Semantic Similarity
≠
Decision Relevance
```

例如用户问：

```text
“这个订单现在还能退款吗？”
```

最相似的历史退款说明，可能不如：

```text
当前订单状态
最新退款政策
用户所在地区规则
支付方式
```

更有决策价值。

---

#### 4.6.3 Retrieval 在 Agent 系统中的位置

前面几节已经回答：

```text
4.1 Context Engineering
→ 当前模型应该看到什么？

4.2 Working State
→ 当前任务系统必须知道什么？

4.3 Short-term Memory
→ 近期什么值得暂存？

4.4 Long-term Memory
→ 什么值得跨任务长期保留？

4.5 Persistence
→ 这些东西怎样真正活下来？
```

4.6 回答的是：

> **当信息没有直接进入当前 Context 时，怎样在真正需要它的那一刻把它找回来？**

---

#### 4.6.4 Retrieval ≠ Context

Retrieval 输出的是：

```text
Candidate / Selected Evidence
```

Context 是：

```text
当前模型真正看到的全部输入
```

所以：

```text
Retrieved
≠
Automatically inserted into Context
```

中间还应该经过：

```text
Trust Check
Freshness Check
Permission Check
Deduplication
Conflict Resolution
Budget Selection
Formatting / Compression
```

---

#### 4.6.5 Retrieval ≠ RAG

RAG 通常指：

```text
Retrieve external knowledge
        ↓
Augment model context
        ↓
Generate answer
```

但 Retrieval 更广。

它还可以服务于：

```text
Memory Recall
Tool Discovery
Code Search
Agent Routing
Case Retrieval
Policy Lookup
Example Retrieval
Skill Retrieval
Environment Inspection
Planning
Verification
```

因此：

> **RAG 使用 Retrieval，但 Retrieval 不等于 RAG。**

---

#### 4.6.6 Retrieval ≠ Memory

Memory 回答：

```text
什么被保存？
```

Retrieval 回答：

```text
当前需要时，从已保存或外部信息中取什么？
```

于是：

```text
Memory Quality
×
Retrieval Quality
×
Context Selection Quality
```

共同决定最终是否“想得起来”。

---

#### 4.6.7 Retrieval ≠ Search Engine

Search Engine 是 Retrieval 的一种实现形态。

Agent 可能从以下对象检索：

```text
Web
Vector Store
Keyword Index
Database
Filesystem
Code Index
Event Log
Conversation Archive
Long-term Memory
Tool Registry
Skill Registry
Knowledge Graph
Artifact Store
```

因此 Retrieval 是系统概念，而不是某个特定产品或数据库。

---

#### 4.6.8 Retrieval 的完整流水线

成熟 Retrieval 通常不是一步：

```text
Current Task / State
        ↓
Query Formation
        ↓
Scope / Permission Filter
        ↓
Candidate Generation
        ↓
Sparse / Dense / Structured Retrieval
        ↓
Candidate Merge
        ↓
Deduplication
        ↓
Freshness / Authority / Trust Filter
        ↓
Reranking
        ↓
Diversity Control
        ↓
Evidence Selection
        ↓
Context Packaging
        ↓
Downstream Decision
```

其中任何一层都可能成为性能瓶颈。

---

#### 4.6.9 第一原则：Retriever Recall 构成下游能力上限

如果真正需要的信息根本没有进入 Candidate Set：

```text
Gold Evidence ∉ Candidates
```

那么：

```text
Reranker
LLM
Verifier
Judge
```

都不可能把它“凭空选回来”。

因此：

> **Candidate Retrieval 阶段通常优先保证 Recall；最终 Context Selection 阶段再提高 Precision。**

这与前面 Tool Retrieval → Tool Selection 完全同构。

---

#### 4.6.10 Candidate Generation 与 Final Selection 要分开评价

可以拆成：

```text
Stage A: Candidate Generation
目标：正确证据别漏掉

Stage B: Rerank / Selection
目标：候选里真正重要的排前面

Stage C: Context Admission
目标：最终真正值得进 Context 的才进入
```

否则最终回答错误时，很难知道：

```text
没找到？
找到但排太后？
排前了但没放进 Context？
放进 Context 但模型没用？
```

---

#### 4.6.11 Query Formation：检索前先决定“到底要找什么”

用户原话不一定是最佳 Retrieval Query。

例如：

```text
“上次那个 deployment 为什么挂了？”
```

真正的检索条件可能需要展开成：

```text
project = X
entity = deployment
reference_time = previous deployment
intent = failure cause
sources = deploy logs + incident notes + commits
```

因此 Query Formation 本身就是一个推理步骤。

---

#### 4.6.12 User Query ≠ Retrieval Query

用户输入：

```text
“他后来怎么处理的？”
```

直接 embedding 这句话通常信息不足。

Retrieval Query 需要结合 Working State：

```text
he = previous incident owner
later = after timestamp T
处理 = remediation actions
```

所以更准确的是：

```text
RetrievalQuery_t = f(UserInput, WorkingState, Goal, RecentContext)
```

---

#### 4.6.13 Query Rewriting

Query Rewriting 可以：

```text
补全省略对象
展开缩写
标准化术语
加入实体 ID
加入时间范围
消除代词
转换语言
增加领域关键词
```

但必须注意：

> **Query Rewrite 是派生表示，不应改变用户真正的检索意图。**

---

#### 4.6.14 Query Expansion

为了提高 Recall，可以加入：

```text
synonyms
aliases
abbreviations
related technical terms
historical names
entity aliases
```

例如：

```text
“OOM”
→ OOM / out of memory / memory exhausted / CUDA OOM
```

但 Expansion 太宽会迅速引入噪声。

---

#### 4.6.15 Query Decomposition

复杂问题往往不能用一个 Query 一次取全。

例如：

```text
“为什么这次线上延迟比上个月高？”
```

可以拆成：

```text
当前 latency metrics
上月 baseline
deployment changes
traffic changes
dependency incidents
```

然后分别检索。

这就是 multi-query / decomposition retrieval。

---

#### 4.6.16 Query Routing

不同问题适合不同 Retrieval Source：

```text
当前订单状态
→ transactional DB

内部设计规范
→ docs index

最新新闻
→ web search

代码定义
→ code index

用户长期偏好
→ user memory
```

所以：

> **Retrieval Routing 决定“去哪里找”，Retriever 决定“在那个空间里找什么”。**

---

#### 4.6.17 Scope First：先缩小允许搜索的空间

在检索前，应优先确定：

```text
user scope
tenant scope
project scope
repository scope
time range
resource type
permission scope
```

而不是先从整个库召回，再事后删掉不该看的内容。

---

#### 4.6.18 Permission Filtering 应尽量发生在 Retrieval 之前

危险设计：

```text
retrieve everything
↓
LLM sees candidates
↓
filter unauthorized items later
```

此时数据已经泄露进 Context。

更安全的是：

```text
Authorized Search Space
        ↓
Retrieval
```

因此：

> **Permission is a retrieval constraint, not merely a rendering filter.**

---

#### 4.6.19 Sparse Retrieval：关键词匹配的价值

典型 sparse retrieval 包括：

```text
TF-IDF
BM25
inverted index
exact term match
```

它擅长：

```text
精确关键词
专有名词
错误码
函数名
文件名
ID
缩写
版本号
```

不要因为有 embedding 就轻易放弃 lexical retrieval。

---

#### 4.6.20 Dense Retrieval：语义相似的价值

Dense Retrieval 通常把 Query 与 Document 映射到 embedding space：

```text
q → e_q

d → e_d

score(q,d) = sim(e_q, e_d)
```

它更擅长：

```text
语义近义
表达改写
自然语言描述
跨词汇匹配
```

但对精确 identifier 未必稳定。

---

#### 4.6.21 Dense Retrieval 的一个典型误区：相似 ≠ 正确

例如 Query：

```text
“如何删除测试数据？”
```

最相似结果可能是：

```text
“如何删除生产数据？”
```

语义很像，但行为风险完全不同。

因此 Dense Similarity 只能作为候选信号之一。

---

#### 4.6.22 Hybrid Retrieval

现实系统往往组合：

```text
Sparse
+
Dense
+
Metadata Filter
+
Domain Signals
```

例如：

```text
CandidateScore
=
α · dense_score
+
β · lexical_score
+
γ · recency_score
+
δ · authority_score
```

实际权重是否显式线性不重要，重要的是多信号融合思想。

---

#### 4.6.23 Exact Match 应该保留自己的优先级

遇到：

```text
ERR_1042
commit 7f3a9c
user_id = 1847
function parse_response
```

如果存在 exact match，通常比“语义上很像”更值得优先。

所以：

```text
Exact Identifier Match
```

应被视为高价值 retrieval feature。

---

#### 4.6.24 Structured Retrieval

如果信息天然是结构化的：

```text
SQL database
knowledge graph
metadata catalog
API
```

不应强行全部 embedding 化。

例如：

```text
orders where user_id = X and status = pending
```

SQL / structured query 往往比向量搜索更准确。

---

#### 4.6.25 Vector Search 不是万能 Retrieval Layer

如果每个问题最后都变成：

```text
chunk everything
embed everything
cosine similarity
```

通常会失去：

```text
exactness
relational constraints
freshness semantics
transactional truth
permission structure
version semantics
```

所以：

> **Retrieval Method 应匹配 Source Semantics。**

---

#### 4.6.26 Metadata Filtering

常见 metadata：

```text
source
author
tenant
project
language
created_at
updated_at
valid_from
valid_until
document_type
security_level
version
status
```

Metadata Filter 可以显著减少候选噪声。

---

#### 4.6.27 Pre-filter vs Post-filter

```text
Pre-filter
→ 先限制搜索空间，再检索

Post-filter
→ 先检索，再删不符合条件的候选
```

对于：

```text
权限
租户隔离
资源类型
强时间边界
```

通常更适合 pre-filter。

---

#### 4.6.28 Freshness-aware Retrieval

不是所有知识都适合“最相似优先”。

例如：

```text
当前库存
权限
价格
软件版本
政策
服务状态
```

旧结果可能高度相关，但已经失效。

所以 Retrieval Score 应显式考虑 Freshness。

---

#### 4.6.29 Recency ≠ Freshness

新发布的文档：

```text
可能描述旧事实
```

旧文档：

```text
可能仍然是当前权威规范
```

因此：

```text
Recent
≠
Current Truth
```

Freshness 应结合 source semantics / version / validity 判断。

---

#### 4.6.30 Authority-aware Retrieval

同一个事实可能出现在：

```text
官方规范
内部 wiki
用户评论
历史邮件
模型总结
论坛帖子
```

相关性相同时，权威性完全不同。

因此可以维护：

```text
authority_level
source_type
verification_status
```

---

#### 4.6.31 Trust-aware Retrieval

检索结果可能来自：

```text
trusted_system
trusted_internal
user_provided
external_untrusted
model_derived
```

Retrieval 不应该把它们洗平成同一种证据。

> **Retrieved ≠ Trusted。**

---

#### 4.6.32 Retrieval Poisoning

攻击者可以故意制造：

```text
看起来和高频 Query 很相似的恶意内容
```

使其更容易进入 top-k。

典型链路：

```text
Attacker Content
↓ indexed
Retriever ranks high
↓
Context
↓
Model follows malicious text
```

因此 retrieval surface 本身也是安全边界。

---

#### 4.6.33 Indirect Prompt Injection 与 Retrieval 的关系

问题不是：

```text
“检索到了恶意文本”
```

而是：

```text
低信任 Data
↓
进入 Context
↓
被模型错误当成 Instruction
```

所以 Retrieved Content 必须保留 source / trust / role semantics。

---

#### 4.6.34 Candidate Set 的大小是重要超参数

`top_k` 太小：

```text
Recall ↓
```

`top_k` 太大：

```text
Noise ↑
Latency ↑
Rerank Cost ↑
Context Pressure ↑
```

因此：

> **Top-k 是 Quality–Cost–Recall trade-off，不是固定魔法数字。**

---

#### 4.6.35 Retrieval Recall@K

定义：

```text
在前 K 个候选中，是否至少包含所需证据？
```

对于单一 gold evidence：

\[
Recall@K = \frac{\#\{query: gold \in topK\}}{\#queries}
\]

对于多证据任务，还可评价 evidence-set recall。

---

#### 4.6.36 Precision@K

Precision@K 关注：

```text
top-k 中有多少是真正相关的？
```

但对 Agent 来说，最终更重要的是：

```text
这些候选是否帮助下游做对 Decision？
```

所以 Precision 仍然只是中间指标。

---

#### 4.6.37 MRR

Mean Reciprocal Rank 关注第一个正确结果出现的位置：

\[
MRR = \frac{1}{N}\sum_i \frac{1}{rank_i}
\]

适合：

```text
一个主要正确答案 / 文档
希望它尽量靠前
```

的 retrieval task。

---

#### 4.6.38 nDCG

当相关性存在等级：

```text
highly relevant
partially relevant
weakly relevant
irrelevant
```

nDCG 比纯 Recall / Precision 更适合评价 ranking quality。

---

#### 4.6.39 Retrieval Accuracy 不等于 End-to-End Utility

可能出现：

```text
Retriever metrics ↑
但最终 Agent success ↓
```

原因包括：

```text
多召回了干扰证据
上下文更长
冲突更多
模型注意力被稀释
错误权威排序
```

所以必须同时做 end-to-end evaluation。

---

#### 4.6.40 Reranking

第一阶段 Retriever 往往追求：

```text
cheap + high recall
```

第二阶段 Reranker 再做更精细判断：

```text
Candidates
↓
Cross-encoder / LLM / heuristic / domain scorer
↓
Reordered Candidates
```

---

#### 4.6.41 Retriever 与 Reranker 的职责

```text
Retriever
= 别漏掉

Reranker
= 别把真正重要的埋在后面
```

如果 Retriever 没召回：

```text
Reranker 无能为力
```

这是重要 failure localization 边界。

---

#### 4.6.42 LLM Reranker 的优势与风险

优势：

```text
理解复杂语义
多条件判断
任务感知
```

风险：

```text
成本高
延迟高
不稳定
受 prompt injection 影响
可能过度偏好语言流畅文本
```

因此不应默认所有候选都用昂贵 LLM rerank。

---

#### 4.6.43 Diversity：top-k 不应该全是同一件事的重复版本

如果前 10 条都是：

```text
同一文档的相邻 chunk
```

虽然相关性都很高，但信息增益很低。

因此可引入 diversity control。

---

#### 4.6.44 MMR：Relevant 与 Diverse 的折中

Maximal Marginal Relevance 的直觉：

```text
既和 Query 相关
又不要和已经选中的结果太重复
```

可抽象为：

\[
MMR(d)=\lambda Rel(d,q)-(1-\lambda)\max_{d'\in S}Sim(d,d')
\]

重点是 trade-off 思想，而不是死记公式。

---

#### 4.6.45 Deduplication

重复可能来自：

```text
同文档多个 chunk
镜像网页
版本副本
摘要 + 原文
相同 Memory 多次写入
```

如果不去重，会造成：

```text
false evidence majority
context waste
attention bias
```

---

#### 4.6.46 Chunking 是 Retrieval 的隐性实验变量

同一份文档切成：

```text
128 tokens
512 tokens
2000 tokens
semantic sections
```

Retrieval 行为可能完全不同。

因此 benchmark 应记录 chunking policy。

---

#### 4.6.47 Chunk 太小的问题

```text
上下文语义断裂
实体指代丢失
条件与结论分离
证据不完整
```

例如：

```text
前 chunk：退款允许于 30 天内
后 chunk：企业客户除外
```

只取前者可能直接误判。

---

#### 4.6.48 Chunk 太大的问题

```text
embedding 表征被平均
精确信息被淹没
Context 成本增加
Rerank 成本增加
```

因此 chunk size 是 Recall–Specificity–Cost trade-off。

---

#### 4.6.49 Semantic Chunking

比固定 token 切分更合理的一种思路是按：

```text
heading
paragraph
function
class
semantic topic
logical unit
```

划分。

但 semantic chunking 本身也可能引入边界错误。

---

#### 4.6.50 Parent–Child Retrieval

常见设计：

```text
Small Child Chunk
→ 用于精确召回

Parent Section
→ 用于补足上下文
```

可以兼顾：

```text
retrieval precision
+
context completeness
```

---

#### 4.6.51 Retrieval Granularity

不同问题可能需要不同粒度：

```text
一句事实
一个段落
一个函数
一个文件
一个 Episode
一条 Memory
一个完整 Artifact
```

因此 Retrieval Unit 本身需要设计。

---

#### 4.6.52 Retrieval Unit ≠ Storage Unit

一个大 PDF 可以作为 Storage Artifact，
但 Retrieval Unit 可以是：

```text
section
page
paragraph
figure caption
```

反过来，多个小事件也可以先 consolidate 成一个可检索 Memory Unit。

---

#### 4.6.53 Multi-hop Retrieval

有些问题需要：

```text
Evidence A
↓ reveals entity B
Evidence B
↓ reveals relation C
Evidence C
↓ answer
```

一次 top-k 很难直接覆盖。

这时需要 multi-hop retrieval。

---

#### 4.6.54 Multi-hop Retrieval 与 Agent Loop

典型结构：

```text
Retrieve
↓
Reason
↓
Identify Missing Information
↓
Form New Query
↓
Retrieve Again
```

这实际上已经是一个小型 epistemic Agent Loop。

---

#### 4.6.55 Iterative Retrieval

首次 Retrieval 不一定要解决全部问题。

可以：

```text
broad retrieval
↓
inspect
↓
refine query
↓
narrow retrieval
```

这比一次构造一个“完美 Query”更现实。

---

#### 4.6.56 Query Drift

多轮检索中，Agent 可能逐渐偏离原 Goal：

```text
原问题 A
↓
看到相关内容 B
↓
继续追 B
↓
最后忘了 A
```

因此 iterative retrieval 必须持续保留 Goal anchor。

---

#### 4.6.57 Retrieval Stopping

什么时候停止继续找？

可能依据：

```text
required evidence 已齐
uncertainty 足够低
marginal information gain 很小
budget exhausted
no new evidence
verification satisfied
```

所以 Retrieval 也需要 termination policy。

---

#### 4.6.58 More Retrieval ≠ Better Retrieval

不断搜索可能带来：

```text
更多噪声
更多冲突
更多 token
更高延迟
更高成本
更大 prompt-injection surface
```

所以：

> **Retrieval 同样存在 diminishing return。**

---

#### 4.6.59 Information Gain

一个候选是否值得继续检索，不只看 relevance，还可以问：

```text
它是否会减少当前关键不确定性？
```

概念上：

```text
Useful Retrieval
≈
Expected Reduction in Decision Uncertainty
```

---

#### 4.6.60 Negative Retrieval

系统有时应该明确得出：

```text
“没有找到足够证据。”
```

而不是：

```text
没有结果
→ 强行拿最相似的一条
```

这就是 retrieval abstention。

---

#### 4.6.61 No Evidence 是合法结果

成熟 Retriever 的输出空间应该允许：

```text
NO_RELEVANT_EVIDENCE
INSUFFICIENT_EVIDENCE
PERMISSION_BLOCKED
INDEX_UNAVAILABLE
FRESHNESS_UNCERTAIN
```

而不是永远返回 top-k。

---

#### 4.6.62 Score Threshold

常见做法：

```text
if score < τ:
    abstain
```

但 raw similarity score 往往：

```text
不跨 query 可比
不跨模型可比
不天然 calibrated
```

因此 threshold 需要单独验证。

---

#### 4.6.63 Retrieval Confidence

Confidence 可以来自多信号：

```text
ranking margin
score calibration
source agreement
retrieval-method agreement
freshness
authority
query coverage
```

但不能简单把 embedding cosine 当成“正确概率”。

---

#### 4.6.64 Margin Signal

如果：

```text
score_1 ≈ score_2 ≈ score_3
```

说明候选可能存在 ambiguity。

如果：

```text
score_1 >> score_2
```

则 top-1 选择可能更稳定。

但 margin 依然只是 proxy。

---

#### 4.6.65 Conflict-aware Retrieval

召回结果可能互相冲突：

```text
Doc A: policy = 30 days
Doc B: policy = 14 days
```

不能简单：

```text
哪个排名高就信哪个
```

需要检查：

```text
version
authority
valid_from
scope
jurisdiction
supersession
```

---

#### 4.6.66 Agreement 不等于 Truth

如果 10 个网页都复制了同一个错误来源：

```text
10-way agreement
```

并不等于 10 个独立证据。

因此应尽量追踪 provenance / source lineage。

---

#### 4.6.67 Provenance-aware Retrieval

候选最好携带：

```text
source_id
source_type
author
version
observed_at
validity
parent_artifact
retrieval_method
retrieval_score
```

这样后续才能正确做冲突解析和审计。

---

#### 4.6.68 Canonical Source 优先

如果某事实有权威 Source of Truth：

```text
transactional DB
current config
official policy
Git repository
```

就不应该优先从：

```text
旧聊天
旧摘要
二手文档
模型记忆
```

获取。

---

#### 4.6.69 Memory Retrieval 的特殊性

Long-term Memory 不只是文档。

它往往带：

```text
scope
confidence
source
supersession
validity
user ownership
memory type
```

因此 Memory Retrieval 需要利用这些结构，而不是只做 embedding similarity。

---

#### 4.6.70 Semantic Memory Retrieval

适合按：

```text
entity
relation
fact type
semantic query
validity
```

召回。

例如：

```text
user preference
project convention
stable domain fact
```

---

#### 4.6.71 Episodic Memory Retrieval

常常需要：

```text
time
actor
project
outcome
failure type
similar situation
```

例如：

```text
“之前有没有遇到过同样的 CI failure？”
```

---

#### 4.6.72 Procedural Memory Retrieval

更像：

```text
当前情境满足哪些 preconditions？
有哪些经验规则适用？
```

而不是简单问：

```text
哪条文字最像当前 Query？
```

---

#### 4.6.73 User Memory Retrieval

User Memory 必须先满足：

```text
same user / allowed scope
```

再谈 relevance。

不能：

```text
因为语义很像
→ 召回另一个用户的偏好
```

---

#### 4.6.74 Cross-user Leakage 是 Retrieval Failure

即使数据库本身没有泄露，只要 Retriever：

```text
把 User A 的 memory 放进 User B 的 Context
```

就已经构成严重安全问题。

所以 tenant/user isolation 是 Retrieval Correctness 的组成部分。

---

#### 4.6.75 Short-term Memory Retrieval

短期记忆往往更重视：

```text
recency
current task relevance
unresolved issues
recent failures
recent decisions
```

而 Long-term Memory 可能更重视：

```text
stability
cross-session utility
verified knowledge
```

---

#### 4.6.76 State Retrieval 这个说法要谨慎

Working State 本质上应该是：

```text
当前任务权威状态
```

如果核心 State 还需要像普通文档一样“希望 Retriever 能找回来”，说明 State Management 可能设计得过于松散。

关键 State 更适合结构化直接读取。

---

#### 4.6.77 Retrieval 与 Context Engineering 的关系

```text
Retrieval
= 找候选信息

Context Engineering
= 决定最终让模型看哪些信息、怎么组织
```

因此：

> **高质量 Retrieval 是 Context Engineering 的输入，不是 Context Engineering 的全部。**

---

#### 4.6.78 Retrieved Evidence 不应自动全量进 Context

例如召回 100 条：

```text
只因为 Retriever 返回了
```

不代表全部塞入 Context。

应该继续：

```text
Rerank
Dedup
Select
Compress
Reference
```

---

#### 4.6.79 Context Budget-aware Retrieval

Retrieval 不能忽略下游 Context Budget。

如果只剩 4k tokens：

```text
retrieve 100k tokens
```

最终仍然必须丢掉绝大部分。

所以 Retrieval Strategy 可以感知：

```text
remaining context budget
```

---

#### 4.6.80 Retrieval Budget

除了 Context Budget，还有：

```text
query count
search depth
latency
money
rerank calls
web requests
DB load
```

所以 Retrieval 也是 test-time compute allocation 问题。

---

#### 4.6.81 Cheap-first Retrieval Cascade

一种常见结构：

```text
Exact / Metadata Filter
        ↓ insufficient
Sparse / Dense Search
        ↓ insufficient
Reranker
        ↓ insufficient
Multi-hop / Web / Expensive Search
```

这和前面的 Verification Cascade、Model Routing 有同样的经济学逻辑。

---

#### 4.6.82 Retrieval Escalation

当：

```text
low confidence
high risk
missing evidence
conflicting evidence
```

时，可以升级：

```text
wider index
fresh web search
stronger reranker
additional source
human lookup
```

---

#### 4.6.83 Local-first Retrieval

Coding Agent 常见顺序：

```text
known file / exact symbol
↓
repository search
↓
broader code index
↓
external docs / web
```

优点：

```text
更快
更便宜
更贴近当前代码版本
更少外部噪声
```

---

#### 4.6.84 Retrieval 的 Freshness Escalation

如果任务问：

```text
“现在”
“最新”
“当前”
```

而当前索引 freshness 无法保证，应该升级到更实时 Source，而不是继续依赖旧 index。

---

#### 4.6.85 Index Freshness

检索系统本身也有状态：

```text
canonical data updated
↓
index update pending
↓
retrieval sees old data
```

因此必须知道：

```text
index_version
last_indexed_at
lag
```

---

#### 4.6.86 Index Lag Failure

典型：

```text
Memory record 已 supersede
但 vector index 仍保留旧 embedding
↓
旧 Memory 再次被召回
```

因此 index consistency 是 Retrieval correctness 的一部分。

---

#### 4.6.87 Delete Propagation 与 Retrieval

删除 canonical record 后，还要保证：

```text
vector index
keyword index
cache
materialized view
```

不再继续召回。

所以：

```text
Delete Success
≠
Retrieval Inaccessibility
```

---

#### 4.6.88 Tombstone-aware Retrieval

如果使用 soft delete / tombstone：

```text
record.status = deleted
```

Retriever 必须默认排除。

否则“逻辑已删除、检索仍可见”。

---

#### 4.6.89 Version-aware Retrieval

当多个版本并存：

```text
v1
v2
v3
```

Retriever 应知道当前任务需要：

```text
latest
historical as-of time T
specific version
```

而不是默认相似度最高。

---

#### 4.6.90 Temporal Retrieval

有些问题问的是：

```text
“当时是什么？”
```

而不是：

```text
“现在是什么？”
```

因此需要支持：

```text
as_of_time
valid_from
valid_until
```

这和 current-truth retrieval 是不同任务。

---

#### 4.6.91 Event Retrieval

Event Log 中的 Retrieval 往往按：

```text
entity
time range
event type
correlation ID
causal chain
```

而非 semantic similarity。

例如查：

```text
某个 payment 到底经历了哪些状态变化？
```

---

#### 4.6.92 Graph Retrieval

当问题依赖关系链：

```text
A belongs to B
B depends on C
C owned by D
```

Knowledge Graph / graph traversal 可能比纯 embedding 更合适。

---

#### 4.6.93 Code Retrieval

Code Search 需要特殊信号：

```text
symbol
AST
call graph
imports
file path
exact token
semantic description
repository version
```

只做自然语言 embedding 往往不足。

---

#### 4.6.94 Tool Retrieval

当 Tool Catalog 很大：

```text
500 tools
```

不一定全部放进 Context。

可以：

```text
Task
↓
Capability Retrieval
↓
small candidate tool set
↓
Tool Selection
```

因此 Tool Retrieval 与知识 Retrieval 共享很多设计原则。

---

#### 4.6.95 Skill Retrieval

未来 Chapter 5 中，Skill 也可能按：

```text
task type
preconditions
tool requirements
historical success
risk
```

被检索。

所以 Retrieval 是 Capability Extension 的基础能力之一。

---

#### 4.6.96 Example Retrieval

Few-shot / demonstration retrieval 也属于 Retrieval：

```text
当前任务
↓
寻找最有帮助的示例
↓
进入 Prompt / Context
```

但“最相似示例”未必是“最有教学价值的示例”。

---

#### 4.6.97 Case-based Reasoning

Agent 可以检索：

```text
过去类似问题
过去 repair 成功案例
过去 failure pattern
```

再用于当前决策。

但必须防止：

```text
表面相似
关键条件不同
→ 错误迁移
```

---

#### 4.6.98 Retrieval 与 Planning

Planning 可能需要先获取：

```text
available tools
constraints
resource status
previous similar plans
```

所以 Retrieval 可以发生在 Planning 前或 Planning 中间。

---

#### 4.6.99 Retrieval 与 Verification

Verifier 可能需要检索：

```text
specification
reference answer
policy
expected state
historical baseline
```

因此 Retrieval Failure 也可能表现成 Verification Failure。

---

#### 4.6.100 Retrieval 与 Reflection

Reflection 想诊断：

```text
“为什么失败？”
```

可能需要检索：

```text
相关 logs
过去失败案例
policy
known issue
recent changes
```

所以 Reflection 不是纯内部思考。

---

#### 4.6.101 Retrieval 与 Routing

Routing 决定：

```text
去哪个 source / retriever
```

Retrieval 决定：

```text
在该 source 中拿哪些信息
```

二者职责不同但经常组合。

---

#### 4.6.102 Retrieval 与 Observability

应该记录：

```text
query
query rewrite
source
filters
retriever version
index version
top-k
scores
rerank scores
selected evidence
abstention reason
latency
cost
```

否则失败很难复盘。

---

#### 4.6.103 Retrieval Trace

推荐把一次 Retrieval 保存成：

```text
retrieval_id
query
source_scope
candidate_ids
candidate_scores
rerank_order
selected_ids
rejected_ids
filters
index_version
timestamp
```

这对 Agent Eval 特别有用。

---

#### 4.6.104 Query Provenance

Query 可能来自：

```text
user text
model rewrite
planner-generated subquery
verifier-generated query
memory recall trigger
```

应该知道：

```text
这个 Query 是谁生成的？
```

否则 query drift 很难定位。

---

#### 4.6.105 Retrieval Failure Taxonomy

至少应区分：

```text
Query Failure
Scope Failure
Permission Failure
Index Failure
Candidate Recall Failure
Ranking Failure
Freshness Failure
Trust Failure
Dedup Failure
Context Admission Failure
Consumption Failure
```

不要把所有问题都叫“RAG 不准”。

---

#### 4.6.106 Query Failure

真正需要找：

```text
退款政策
```

Agent 却生成：

```text
订单状态
```

即使 Retriever 完美，最终也会错。

---

#### 4.6.107 Scope Failure

例如：

```text
应该搜索 current project
却搜索 all projects
```

可能导致：

```text
噪声
权限风险
错误跨项目迁移
```

---

#### 4.6.108 Candidate Recall Failure

Gold Evidence 明明在 Index：

```text
但 top-k 没召回
```

这是 Retriever 问题，而不是 Reranker 问题。

---

#### 4.6.109 Ranking Failure

Gold Evidence 已经在 candidate set：

```text
但排在太后
```

导致最终没有进入 Context。

这是 ranking / reranking failure。

---

#### 4.6.110 Context Admission Failure

正确证据已经排在前面：

```text
但 Context Builder 因错误预算策略删掉
```

此时 Retrieval 本身可能是成功的。

---

#### 4.6.111 Consumption Failure

正确 Evidence 已经在 Context 中：

```text
模型仍然没用它
```

这更接近：

```text
reasoning / attention / instruction-following failure
```

而不是 Retrieval Failure。

---

#### 4.6.112 Failure Localization Pipeline

遇到“Agent 没想起来”时，可以按顺序查：

```text
1. 信息是否存在？
2. 是否已被正确持久化？
3. 是否进入可检索索引？
4. Query 是否正确？
5. Scope / Permission 是否正确？
6. Candidate Set 是否召回？
7. Ranking 是否足够高？
8. 是否进入 Context？
9. 模型是否真正消费？
10. 最终 Decision 是否正确？
```

---

#### 4.6.113 Retrieval Evaluation 要分层

建议至少四层：

```text
Index / Availability
Candidate Recall
Ranking Quality
End-to-End Task Utility
```

否则很容易优化错层级。

---

#### 4.6.114 Retrieval Dataset

一条评测样本最好包含：

```text
query
state / context
allowed scope
gold evidence ids
hard negatives
time validity
source authority
expected abstention
```

而不是只有 query–document pair。

---

#### 4.6.115 Hard Negative

Hard Negative 是：

```text
很像
但关键条件不满足
```

例如：

```text
旧版本政策
另一个用户的数据
另一个项目的同名文件
生产环境 vs 测试环境
同名函数的不同实现
```

它们比随机负样本更能测真正 decision boundary。

---

#### 4.6.116 Temporal Hard Negative

非常重要的一类：

```text
过去正确
现在过期
```

例如旧政策、旧权限、旧版本配置。

这能测 Retriever 是否理解 Freshness。

---

#### 4.6.117 Authority Hard Negative

内容很像，但来源权威级别不同：

```text
官方规范
vs
论坛转述
```

用于测试 Authority-aware Retrieval。

---

#### 4.6.118 Permission Hard Negative

内容高度相关：

```text
但当前用户无权访问
```

正确行为应该是：

```text
不召回 / 不暴露
```

而不是“因为 relevant 所以给出来”。

---

#### 4.6.119 Abstention Benchmark

必须有一部分 case：

```text
库里没有足够证据
```

否则 Retriever 会被训练成：

```text
无论如何都给 top-1
```

真实系统会产生高置信错误。

---

#### 4.6.120 Index-size Curve

应测试：

```text
1k docs
10k docs
100k docs
1M docs
```

观察：

```text
Recall@K
MRR
Latency
Cost
Noise
```

因为 Retrieval 在小库和大库上可能完全不是同一个问题。

---

#### 4.6.121 Distractor-size Curve

固定 gold evidence，只不断加入：

```text
unrelated distractors
semantic distractors
near-duplicate distractors
stale distractors
permission-blocked distractors
```

可以直接测 robustness。

---

#### 4.6.122 Query Robustness

同一语义可以改写成：

```text
formal
colloquial
abbreviation
misspelling
cross-language
underspecified
```

观察 Retrieval 是否稳定。

---

#### 4.6.123 Retrieval Ablation

可以比较：

```text
Dense only
Sparse only
Hybrid
+ metadata
+ freshness
+ reranker
+ authority
+ diversity
```

看每层真实贡献。

---

#### 4.6.124 Reranker Ablation

固定 Candidate Set，只改变 Reranker：

```text
none
heuristic
cross-encoder
LLM
```

这样才能单独评价 Ranking 层。

---

#### 4.6.125 Query Rewrite Ablation

固定 Index / Retriever，只比较：

```text
raw user query
state-aware rewrite
expanded query
multi-query
```

可以直接评价 Query Formation。

---

#### 4.6.126 Counterfactual Retrieval Test

固定 Task 和 Model，只替换：

```text
correct evidence
stale evidence
conflicting evidence
no evidence
malicious evidence
```

看下一步 Decision 是否合理变化。

这能测 Agent 是否真正依赖检索证据。

---

#### 4.6.127 Oracle Retrieval

研究中可以构造：

```text
Oracle Evidence
```

直接给模型正确证据。

如果 Oracle Retrieval 下仍然表现差：

```text
瓶颈不在 Retriever
```

这是很有价值的上界实验。

---

#### 4.6.128 Oracle Context vs Oracle Retrieval

还可以进一步区分：

```text
Oracle Retrieval
= gold evidence 在 candidate set

Oracle Context
= gold evidence 直接放入最终 Context
```

二者之间的差距反映：

```text
reranking / context selection loss
```

---

#### 4.6.129 Retrieval Cost

成本包括：

```text
embedding
index lookup
DB query
reranker
LLM query rewrite
web request
network
context tokens
```

所以应评价：

```text
Cost per Useful Retrieval
```

而不是只看每次 search 的价格。

---

#### 4.6.130 Retrieval Latency

可拆成：

```text
query formation
routing
index lookup
candidate merge
rerank
source fetch
context packaging
```

其中 tail latency 很重要。

---

#### 4.6.131 Parallel Retrieval

可以同时查：

```text
memory
internal docs
code
web
```

降低 wall-clock latency。

但代价是：

```text
cost ↑
noise ↑
merge complexity ↑
```

---

#### 4.6.132 Sequential Retrieval

如果 source 之间有依赖：

```text
先解析 entity ID
再查该实体历史
```

就不应为了并行而并行。

---

#### 4.6.133 Retrieval Cache

缓存 Query Result 可以降低成本，但必须考虑：

```text
freshness
permission
user scope
index version
query normalization
```

否则 cache 会成为 stale / leakage 来源。

---

#### 4.6.134 Permission-sensitive Cache Key

危险：

```text
cache_key = query
```

更合理至少包含：

```text
query
user / tenant
permission scope
source version
```

否则 User A 的结果可能被复用给 User B。

---

#### 4.6.135 Retrieval Security：不要把所有 Query 原样发给外部 Search

内部 Context 可能包含：

```text
secret
customer data
private project names
internal identifiers
```

如果 Query Rewrite 把它们发给外部搜索引擎，就发生 data exfiltration。

---

#### 4.6.136 Query Minimization

对外部 Retriever 应坚持：

```text
只发送完成检索所需的最小信息
```

也就是 Retrieval 版的数据最小化。

---

#### 4.6.137 Retrieval 与 Least Privilege

不仅工具权限要最小化，信息权限也要最小化：

```text
Need-to-know Retrieval
```

Agent 不应该因为技术上“能搜到”，就拥有全部数据访问面。

---

#### 4.6.138 Search Result Snippet ≠ Source

搜索引擎 snippet 只是派生摘要。

如果结论重要：

```text
Search Result
↓
Open Source
↓
Inspect Primary Evidence
```

而不是把 snippet 当完整事实。

---

#### 4.6.139 Primary Source Preference

高风险 / 高价值问题应尽量从：

```text
original document
official API
canonical database
source repository
first-party policy
```

取证。

---

#### 4.6.140 Retrieval Grounding

最终回答最好能回答：

```text
这条 Claim 来自哪一个 Retrieved Evidence？
```

即：

```text
Claim
↓ grounded by
Evidence ID / Source
```

这对可审计性和 Verification 很重要。

---

#### 4.6.141 Citation ≠ Grounding

有 citation 只表示：

```text
附了一个来源
```

不证明：

```text
这个来源真的支持当前 Claim
```

真正 Grounding 还要看 entailment / support relationship。

---

#### 4.6.142 Retrieval 与 Hallucination

Retrieval 可以降低某些知识幻觉，但不能保证：

```text
模型不会误读证据
模型不会忽略证据
模型不会组合出错误结论
模型不会引用错误来源
```

所以：

> **RAG is not a truth guarantee.**

---

#### 4.6.143 Retrieval-induced Hallucination

甚至检索本身会制造新错误：

```text
错误候选
过期候选
上下文冲突
无关细节
```

进入 Context 后，可能让原本模型能答对的问题答错。

---

#### 4.6.144 Retrieval Benefit 也应看净收益

类似前面的 Reflection / Memory：

```text
Retrieval Net Benefit
=
Rescued Cases
-
Retrieval-induced Harm
```

不能只统计“检索帮了多少”。

---

#### 4.6.145 Retrieval Trigger Policy

不是每个 Query 都应该检索。

可以基于：

```text
knowledge freshness requirement
uncertainty
need for private data
need for exact facts
risk
cost
```

决定是否 Retrieval。

---

#### 4.6.146 Always-on Retrieval 的问题

无条件检索会导致：

```text
latency ↑
cost ↑
noise ↑
attack surface ↑
context pollution ↑
```

因此：

```text
Need Retrieval?
```

本身也可以是一层决策。

---

#### 4.6.147 Retrieval Routing vs Retrieval Trigger

```text
Trigger
= 要不要找？

Routing
= 去哪里找？

Query Formation
= 找什么？

Retriever
= 候选有哪些？

Reranker
= 哪些最重要？

Context Policy
= 最终哪些给模型看？
```

这套职责划分非常重要。

---

#### 4.6.148 Minimal Sufficient Retrieval

继前面的：

```text
Minimal Sufficient Context
Minimal Sufficient Effect
Minimal Durable State
```

这里再加入：

> **Minimal Sufficient Retrieval：为当前 Decision 获取足够证据，但不过度搜索。**

目标不是：

```text
找到越多越好
```

而是：

```text
证据足以支持正确决策即可
```

---

#### 4.6.149 Retrieval Progress Signal

继续检索是否有价值，可以看：

```text
new unique evidence
uncertainty reduction
new source coverage
conflict resolution
verification progress
```

如果连续检索只返回同样内容：

```text
Busy Search ≠ Progress
```

---

#### 4.6.150 No-progress Guard

可以设置：

```text
max_queries
max_same-source_queries
max_no-new-evidence_steps
max_retrieval_cost
max_wall_time
```

防止 Agent 陷入 search loop。

---

#### 4.6.151 Retrieval Failure Recovery

不同 failure 应采用不同恢复：

```text
no results
→ query rewrite / broader scope

ambiguous results
→ add constraints / ask user

stale results
→ fresher source

permission blocked
→ request access / alternate source

index unavailable
→ fallback source

conflicting evidence
→ authority / version resolution
```

而不是统一“再搜一次”。

---

#### 4.6.152 Retrieval 与 Ask User

如果缺的信息属于：

```text
用户私有意图
主观偏好
不可推断约束
```

继续搜索并不能解决。

这时：

```text
Ask User
```

比 Retrieval 更正确。

---

#### 4.6.153 Retrieval 与 Tool Use 的区别

Retrieval 本身通常是 Epistemic Action：

```text
获取信息
```

但 Retrieval Tool 仍然是 Tool。

所以：

```text
Retrieval semantics
```

属于信息获取逻辑；

```text
Tool execution semantics
```

属于它如何真正运行。

---

#### 4.6.154 Retrieval 与 Side Effects

即使 retrieval 看起来是 read-only，也可能产生：

```text
access logs
billing
rate limit usage
read receipts
privacy exposure
external query leakage
```

所以 Chapter 3 的 Side Effects 仍然适用。

---

#### 4.6.155 Retrieval Observation

Retriever 返回结果以后：

```text
Raw Search Result
≠
Observation
```

仍然需要：

```text
normalize
attach provenance
mark truncation
mark freshness
mark trust
```

才能安全进入 Agent State / Context。

---

#### 4.6.156 Retrieval Result 的 Lossy Transformation

如果对检索结果做：

```text
summary
extract
translation
OCR
```

必须保留 lineage：

```text
Derived Observation
→ Source Evidence
```

否则以后会把摘要当原始事实。

---

#### 4.6.157 Retrieval 与 Multimodal Evidence

Retrieval Unit 不一定是文本。

还可能是：

```text
image
page screenshot
figure
chart
audio segment
video clip
PDF page
```

需要跨模态索引和后续 grounding。

---

#### 4.6.158 Multimodal Retrieval 的粒度问题

例如 PDF：

```text
整个 PDF
page
figure
caption
paragraph
```

不同粒度会显著影响召回和 Context 成本。

---

#### 4.6.159 Multilingual Retrieval

Query 与 Document 语言不同：

```text
Chinese Query
English Document
```

可以使用：

```text
multilingual embeddings
query translation
cross-lingual sparse expansion
```

但 translation 本身可能改变技术术语。

---

#### 4.6.160 Domain Retrieval

法律、医学、代码、金融等领域往往需要：

```text
领域 tokenizer
specialized embedding
metadata
citation hierarchy
versioning
```

不能假设一个通用 Retriever 在所有 domain 都同样好。

---

#### 4.6.161 Retrieval Model Version 也是实验变量

应该记录：

```text
embedding model
reranker model
index build version
chunking version
query rewrite version
```

否则 benchmark 很难复现。

---

#### 4.6.162 Index Build 是 Retrieval Pipeline 的一部分

Offline 阶段可能包括：

```text
parse
clean
chunk
metadata extract
embed
index
version
```

任一环节错误，在线 Retriever 都可能被误判。

---

#### 4.6.163 Parsing Failure 可以伪装成 Retrieval Failure

例如 PDF 解析漏掉一页：

```text
Gold Evidence 根本没进 Index
```

在线 Retriever 当然永远找不到。

所以要区分：

```text
Corpus Coverage Failure
vs
Retriever Recall Failure
```

---

#### 4.6.164 Corpus Coverage

在评价 Retrieval 前先问：

```text
需要的信息是否真的存在于 Corpus？
```

否则 Recall 指标没有意义。

---

#### 4.6.165 Indexability

信息即使存在，也可能因为：

```text
scan image
unsupported format
encrypted file
parsing error
ACL omission
```

没有真正被索引。

因此：

```text
Exists
≠
Indexed
≠
Retrievable
```

---

#### 4.6.166 Retrieval Lineage

一条候选最好能追踪：

```text
source artifact
parser version
chunk id
embedding model
index version
retrieval query
retrieval score
rerank score
```

这样结果才可审计。

---

#### 4.6.167 Production Drift

随着：

```text
corpus grows
user behavior changes
new vocabulary appears
index distribution shifts
```

Retrieval Quality 会漂移。

需要持续 monitoring。

---

#### 4.6.168 Retrieval Monitoring

可以持续看：

```text
zero-result rate
abstention rate
click/use rate
gold recall on probes
latency
index lag
query distribution
source distribution
stale-hit rate
```

---

#### 4.6.169 Online Feedback 的风险

如果直接用用户点击 / Agent 使用作为 relevance label：

```text
position bias
exposure bias
confirmation loop
```

都会污染训练信号。

因此 online feedback 需要去偏。

---

#### 4.6.170 Self-reinforcing Retrieval Loop

危险链路：

```text
Retriever 先把 A 排前
↓
Agent 更常使用 A
↓
系统把“被使用”当正反馈
↓
A 排得更前
```

可能形成错误强化。

---

#### 4.6.171 Retrieval Data Flywheel

更健康的闭环：

```text
Queries
↓
Candidates
↓
Downstream Outcome
↓
Human / Verifier Feedback
↓
Failure Attribution
↓
Retriever / Reranker / Index Improvement
```

关键是 Outcome-aware，而不是 click-only。

---

#### 4.6.172 Retrieval for Agent Evaluation

Agent benchmark 应保存：

```text
retrieval trace
```

否则同一个最终错误可能来自完全不同层。

这对 failure analysis 非常重要。

---

#### 4.6.173 End-to-End Evaluation 与 Component Evaluation 必须同时存在

Component：

```text
Recall@K
MRR
nDCG
latency
```

End-to-End：

```text
Task Success
Correct Decision
Grounded Answer
Harmful Retrieval Rate
Cost per Success
```

两者缺一不可。

---

#### 4.6.174 Retrieval-induced Right→Wrong

一个本来模型能答对的问题：

```text
加入错误 Retrieval
↓
模型反而改错
```

这是 Retrieval 的 degradation。

因此也应统计：

```text
No Retrieval Correct → Retrieval Wrong
```

---

#### 4.6.175 Retrieval Rescue

反过来：

```text
No Retrieval Wrong → Retrieval Correct
```

是 rescue。

最终应联合看：

```text
Net Retrieval Benefit
=
Wrong→Right
-
Right→Wrong
```

---

#### 4.6.176 Retrieval Coverage–Risk Curve

当只在高置信 Query 上使用 Retrieval：

```text
Coverage ↓
Reliability ↑
```

当放宽 trigger：

```text
Coverage ↑
但可能引入更多错误 retrieval
```

可以画 selective retrieval curve。

---

#### 4.6.177 Retrieval Confidence Calibration

如果系统声称：

```text
confidence = 0.9
```

最好验证：

```text
约 90% 真的有足够证据吗？
```

否则 confidence 只是未经校准的分数。

---

#### 4.6.178 Retrieval Benchmark 必须固定 Index Snapshot

如果 Corpus 每天都变：

```text
今天 rerun
≠
昨天同一个 retrieval environment
```

研究实验应记录：

```text
corpus snapshot
index version
retrieval timestamp
```

---

#### 4.6.179 Web Retrieval 的特殊挑战

Web 是动态环境：

```text
页面更新
排名变化
网页消失
地区差异
个性化
广告
访问限制
```

所以可重复性比静态 corpus 更差。

---

#### 4.6.180 Live Retrieval vs Frozen Retrieval

研究可以区分：

```text
Frozen Corpus Retrieval
→ 可重复性高

Live Retrieval
→ 更贴近真实系统
```

二者回答不同科学问题。

---

#### 4.6.181 Retrieval 与 Cache 的实验污染

重复 benchmark 时：

```text
第一次 query 已缓存
第二次直接命中
```

会改变：

```text
latency
source behavior
freshness
```

所以实验需要明确 cache policy。

---

#### 4.6.182 Retrieval Reproducibility Contract

至少记录：

```text
corpus / source snapshot
index build
embedding model
chunking
metadata schema
query rewriting
filters
top-k
reranker
threshold
cache policy
retrieval timestamp
```

---

#### 4.6.183 Coding Agent 示例

任务：

```text
修复 parse_config() 在空值下崩溃的问题
```

合理 Retrieval：

```text
1. exact symbol search: parse_config
2. inspect definition
3. inspect callers
4. search existing tests
5. search similar parser utilities
6. only if needed, consult external docs
```

而不是先全网搜索“Python parser crash”。

---

#### 4.6.184 Research Agent 示例

问题：

```text
“这篇新方法和已有 test-time reasoning 工作是什么关系？”
```

合理流程：

```text
identify method claims
↓
retrieve primary paper
↓
retrieve closest prior work
↓
retrieve current benchmark context
↓
compare mechanism / training / inference / budget / evaluation
↓
resolve contradictions
```

---

#### 4.6.185 Customer-support Agent 示例

问题：

```text
“我这个订单为什么不能退款？”
```

应优先：

```text
current order state
customer-specific eligibility
current official policy
```

而不是：

```text
旧 FAQ
历史对话里的旧政策
其他用户案例
```

---

#### 4.6.186 Retrieval Failure Mode 1：只用 Semantic Similarity

问题：

```text
精确 ID / 版本 / 权限 / 时间条件丢失
```

修复：

```text
Hybrid + Metadata + Exact Match
```

---

#### 4.6.187 Failure Mode 2：只看关键词

问题：

```text
表达改写后召回差
```

修复：

```text
Dense / Query Expansion / Hybrid
```

---

#### 4.6.188 Failure Mode 3：Top-k 太小

结果：

```text
Gold Evidence 经常被漏掉
```

应通过 Recall@K 曲线选择，而不是凭感觉定 K。

---

#### 4.6.189 Failure Mode 4：Top-k 太大

结果：

```text
噪声、成本、Context Pollution、冲突增加
```

应增加 rerank / diversity / admission policy。

---

#### 4.6.190 Failure Mode 5：Old-but-similar

旧文档高度相似，却已经失效。

修复：

```text
Freshness / Version-aware Retrieval
```

---

#### 4.6.191 Failure Mode 6：Cross-scope Retrieval

召回另一个：

```text
用户
项目
tenant
environment
```

的内容。

这是 correctness + security failure。

---

#### 4.6.192 Failure Mode 7：Duplicate Flooding

同一来源被切成多个相邻 chunk，占满 top-k。

修复：

```text
Dedup / Parent grouping / MMR
```

---

#### 4.6.193 Failure Mode 8：Query Drift

多跳检索逐渐偏离原 Goal。

修复：

```text
Goal anchoring
query trace
step-level verification
```

---

#### 4.6.194 Failure Mode 9：Retriever Hallucination by Proxy

Retriever 返回“最像的”，Agent 把它误当“答案”。

修复：

```text
Retrieved ≠ Verified
```

并要求 Evidence sufficiency check。

---

#### 4.6.195 Failure Mode 10：Index Lag

Canonical State 已更新，Index 还没跟上。

修复：

```text
index version
fresh source fallback
read-after-write path
```

---

#### 4.6.196 Failure Mode 11：Silent Permission Leakage

Retriever 内部看到了 unauthorized item，虽然最后没展示。

若该 item 已影响 ranking / model decision，也可能构成信息泄漏。

权限最好尽量前置。

---

#### 4.6.197 Failure Mode 12：Retrieval Injection

恶意文档通过高相似度进入 Context。

修复：

```text
trust labeling
instruction/data separation
source policy
runtime authorization boundary
```

---

#### 4.6.198 Failure Mode 13：Always Retrieve

所有 Query 都查外部库，导致：

```text
cost / latency / noise ↑
```

修复：

```text
Retrieval Trigger Policy
```

---

#### 4.6.199 Failure Mode 14：Never Abstain

库里没答案也强行返回最相似结果。

修复：

```text
NO_EVIDENCE / threshold / calibration
```

---

#### 4.6.200 Failure Mode 15：Summary-only Retrieval

只存摘要，不保留原始 source lineage。

结果：

```text
无法核验
错误摘要被长期传播
```

---

#### 4.6.201 Failure Mode 16：Context Admission 不透明

Retriever 明明找到了正确证据，但被 Context Builder 丢掉。

必须记录：

```text
retrieved → selected → admitted
```

的完整 trace。

---

#### 4.6.202 Failure Mode 17：Score Worship

把 cosine 0.91 当成：

```text
91% 正确
```

这是错误解释。

Similarity Score ≠ Calibrated Probability。

---

#### 4.6.203 Failure Mode 18：Reranker Overfitting

在固定 benchmark 上训练 / 调参后，看起来 ranking 很好，但对新 Query distribution 不稳定。

要测 cross-domain / temporal generalization。

---

#### 4.6.204 Failure Mode 19：No Source Diversity

多个结果看似不同，其实都来自同一源的复制。

应做 provenance clustering。

---

#### 4.6.205 Failure Mode 20：Search Loop

Agent 不断：

```text
search
rewrite
search
rewrite
```

但 Evidence 没增加。

修复：

```text
No-progress Guard + Retrieval Budget
```

---

#### 4.6.206 工程原则 1：先保证 Corpus Coverage，再优化 Retriever

如果信息根本没被收录或解析，调 embedding 没意义。

---

#### 4.6.207 工程原则 2：Candidate Recall 与 Final Precision 分开优化

不要要求一个 Retriever 同时完美解决所有阶段。

---

#### 4.6.208 工程原则 3：Source Semantics 决定 Retrieval Method

```text
结构化事实 → structured query
代码 → symbol / code search
自然语言知识 → hybrid retrieval
当前状态 → authoritative API / DB
```

---

#### 4.6.209 工程原则 4：Permission First

不该看的信息最好从 Candidate Space 就不存在。

---

#### 4.6.210 工程原则 5：Freshness First for Dynamic Facts

对于动态状态：

```text
相似但旧
<
稍弱但当前权威
```

---

#### 4.6.211 工程原则 6：Retrieved ≠ Trusted

保留：

```text
source
provenance
trust
version
freshness
```

直到最终 Context。

---

#### 4.6.212 工程原则 7：No Evidence 是一等结果

不要逼 Retriever 永远给答案。

---

#### 4.6.213 工程原则 8：最小充分检索

达到 Evidence Sufficiency 后及时停止。

---

#### 4.6.214 工程原则 9：Trace Every Retrieval

没有 Query / Candidate / Ranking / Selection trace，就很难做 failure analysis。

---

#### 4.6.215 工程原则 10：评价净收益，而不是只评价召回率

最终目标仍是：

```text
更正确
更可靠
更便宜
更安全
```

而不是 Retriever leaderboard。

---

#### 4.6.216 最小 Retrieval-aware Agent Loop

```python
while not state.terminal:
    need = retrieval_policy(state)

    if need:
        query = form_query(state)
        scope = resolve_scope_and_permissions(state)

        candidates = retrieve(
            query=query,
            scope=scope,
            top_k=state.retrieval_budget.top_k,
        )

        candidates = filter_fresh_trusted_allowed(candidates, state)
        ranked = rerank(query, candidates)
        selected = select_under_context_budget(ranked, state)

        state.record_retrieval_trace(query, candidates, selected)

        if not evidence_sufficient(selected):
            state = handle_retrieval_gap(state)
            continue

        state.attach_evidence(selected)

    context = build_context(state)
    action = policy(context)
    state = execute_and_observe(state, action)
```

重点不是具体代码，而是：

```text
Need Retrieval?
Query
Scope
Candidates
Filter
Rerank
Select
Evidence Sufficiency
Context
```

每一层都可独立观察和评价。

---

#### 4.6.217 Retrieval 的系统边界

| 概念 | 主要问题 |
| --- | --- |
| Context Engineering | 最终让模型看到什么？ |
| Working State | 当前系统必须知道什么？ |
| Memory | 什么值得保存？ |
| Persistence | 怎样让它活下来？ |
| Retrieval | 当前需要时找回什么？ |
| Reranker | 候选里谁更重要？ |
| RAG | 怎样把外部知识取回并用于生成？ |
| Search Engine | Retrieval 的一种实现 |
| Router | 去哪个 Source / Retriever？ |
| Verifier | 找到以后，它真的支持结论吗？ |

---

#### 4.6.218 面试：为什么 Retrieval 不等于 RAG？

回答要点：

```text
RAG 是 Retrieve → Augment → Generate 的一种应用模式；
Retrieval 更一般，可以服务 Memory、Tool、Skill、Code、Planning、Verification 等。
```

---

#### 4.6.219 面试：Dense 和 Sparse 怎么选？

不要回答“Dense 更高级”。

应回答：

```text
精确词 / ID / symbol → sparse / exact 强
语义改写 → dense 强
现实系统常 hybrid
并结合 metadata / freshness / authority
```

---

#### 4.6.220 面试：为什么 Retriever Recall 很重要？

因为：

```text
Gold Evidence 不在 Candidate Set
→ 下游不可能选到
```

所以 Candidate Recall 是后续 Reranker / LLM 的能力上限之一。

---

#### 4.6.221 面试：Top-k 越大越好吗？

不是。

```text
K ↑
Recall 可能 ↑
但 Noise / Cost / Latency / Context Pressure 也 ↑
```

需要结合 Recall@K、downstream quality 与成本调参。

---

#### 4.6.222 面试：为什么 Retrieved ≠ Trusted？

Retriever 只说明：

```text
某内容与 Query 匹配
```

不能证明：

```text
正确
最新
权威
有权限
无恶意
```

这些属于额外 trust / freshness / permission 层。

---

#### 4.6.223 面试：Reranker 解决什么问题？

Retriever 负责高 Recall 地找候选；Reranker 用更贵、更细的判断把最重要的候选排前。

前者没召回，后者救不了。

---

#### 4.6.224 面试：为什么 Vector Store 不等于 Retrieval System？

完整 Retrieval System 还包括：

```text
Corpus
Parsing
Chunking
Metadata
Permissions
Query Formation
Routing
Candidate Generation
Reranking
Freshness
Trust
Abstention
Context Admission
Observability
```

Vector Store 只解决其中一部分。

---

#### 4.6.225 面试：如何评价一个 Retrieval 系统？

至少分：

```text
Corpus Coverage
Recall@K
MRR / nDCG
Freshness
Permission Safety
Abstention
Latency / Cost
End-to-End Task Success
Retrieval-induced Harm
```

---

#### 4.6.226 面试：为什么 Memory Retrieval 不能只靠 embedding？

因为 Memory 还有：

```text
scope
user
validity
supersession
confidence
source
memory type
```

这些结构信号经常比纯语义相似更重要。

---

#### 4.6.227 面试：怎么处理动态事实？

优先走 authoritative fresh source，并保留：

```text
version
timestamp
validity
index lag
```

不要只依赖历史 embedding index。

---

#### 4.6.228 面试：什么时候应该停止 Retrieval？

当：

```text
required evidence 已足够
关键 uncertainty 已下降
继续搜索没有新信息
验证条件满足
或预算达到上限
```

---

#### 4.6.229 面试：Retrieval 如何影响 Agent 安全？

主要风险：

```text
cross-user leakage
unauthorized retrieval
external query leakage
retrieval poisoning
indirect prompt injection
stale high-risk information
```

所以权限与 trust 必须进入 Retrieval Pipeline。

---

#### 4.6.230 面试：什么是 Minimal Sufficient Retrieval？

为了当前 Decision 获取足够证据，但不过度搜索。

它平衡：

```text
Recall
Cost
Latency
Noise
Attack Surface
Context Budget
```

---

#### 4.6.231 一句话总结 Retrieval

> **Retrieval 不是“从向量库里找最相似的文本”，而是在权限、时效、可信度、预算与上下文容量约束下，从外部信息空间中为当前 Decision 找到最有用的证据；一个成熟系统必须把 Query、Candidate Recall、Ranking、Freshness、Trust、Abstention、Context Admission 和 End-to-End Utility 分层处理。**

---

#### 4.6.232 Chapter 4 总结：从“知道”到“找得到”

整个 Chapter 4 现在形成完整链路：

```text
4.1 Context Engineering
→ 当前这一轮应该让模型看到什么？

4.2 Working State
→ 当前任务为了继续正确执行，系统必须知道什么？

4.3 Short-term Memory
→ 哪些近期信息值得暂时保留？

4.4 Long-term Memory
→ 哪些知识 / 经历值得跨任务长期保留？

4.5 Persistence
→ 这些 State / Memory 怎样跨时间和故障活下来？

4.6 Retrieval
→ 真正需要时，怎样把正确的信息找回来？
```

最终闭环：

```text
Environment / Experience
        ↓
Observation
        ↓
Working State
        ↓
Memory Write / Persistence
        ↓
Stored Knowledge / History
        ↓
Retrieval
        ↓
Context Engineering
        ↓
Model Decision
        ↓
Action
        ↓
Environment
```

这意味着：

> **Agent 的“记忆能力”不是一个单独 Memory 模块，而是 Write、Persist、Retrieve、Select、Use、Update、Forget 共同构成的系统能力。**

---

#### 4.6.233 参考资料

- Robertson S, Zaragoza H. *The Probabilistic Relevance Framework: BM25 and Beyond*. Foundations and Trends in Information Retrieval, 2009.
- Karpukhin V, Oguz B, Min S, et al. *Dense Passage Retrieval for Open-Domain Question Answering*. EMNLP, 2020.
- Lewis P, Perez E, Piktus A, et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS, 2020.
- Khattab O, Zaharia M. *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT*. SIGIR, 2020.
- Carbonell J, Goldstein J. *The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries*. SIGIR, 1998.
- Thakur N, Reimers N, Rücklé A, et al. *BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models*. NeurIPS Datasets and Benchmarks, 2021.
- Gao Y, Xiong Y, Gao X, et al. *Retrieval-Augmented Generation for Large Language Models: A Survey*. arXiv, 2023.

> 本节的系统设计观点还综合吸收了现代 RAG、hybrid search、memory retrieval、Agent context engineering 与 production retrieval systems 中关于权限、时效、索引一致性、检索可观测性和端到端评测的通用工程实践。
