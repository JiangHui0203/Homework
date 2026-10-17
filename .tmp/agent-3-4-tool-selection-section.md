### 3.4 Tool Selection

#### 3.4.1 定义：Tool Selection 到底在选什么？

在 3.1–3.3 中，我们已经分别回答了三个问题：

- Tool 是什么；
- Tool 的参数契约是什么；
- Tool 如何通过 Name / Description / Schema 向模型暴露自己的能力语义。

接下来才进入真正的决策问题：**当前这一步到底要不要调用 Tool；如果要调用，应该调用哪一个？**

Tool Selection 可以抽象为：

$$
\pi_{tool}(a_t\mid s_t, C_t, \mathcal{T}_t)
$$

其中：

- $s_t$：当前 Agent State；
- $C_t$：这一轮实际送入模型的 Context；
- $\mathcal{T}_t$：当前可见 / 可用的 Tool 集合；
- $a_t$：模型提出的下一步 action。

如果只考虑 Tool，动作空间常被误写成：

$$
a_t \in \{T_1,T_2,\ldots,T_n\}
$$

但真实系统更准确的是：

$$
a_t \in \{\text{NoTool},\text{Ask},\text{Answer},\text{Stop},T_1,\ldots,T_n\}
$$

所以 Tool Selection **不是单纯的多分类问题**。

它至少包含两个嵌套判断：

```text
当前是否需要外部能力？
        ↓
   ┌────┴────┐
   │         │
 No Tool    Tool
             ↓
        应该选哪个？
```

因此可以写成：

```text
Need Tool?
   ↓
Candidate Tool Set
   ↓
Semantic Matching
   ↓
Policy / Permission Filtering
   ↓
Risk / Cost / Freshness Consideration
   ↓
Select Tool / No Tool / Ask / Stop
```

最重要的一句话是：

> **Tool Selection 不是“从工具列表里挑一个看起来最像的名字”，而是在当前状态、目标、约束、权限与成本条件下，选择下一步最合适的 capability。**

---

#### 3.4.2 Tool Selection 首先是“要不要调用 Tool”

很多教程一上来就讨论：

```text
search_web
calculator
read_file
send_email

应该选哪个？
```

但在真实 Agent 中，第一个问题应该是：

> **这里真的需要 Tool 吗？**

例如用户问：

```text
2 + 2 等于多少？
```

系统同时提供：

```text
calculator
search_web
```

模型完全可以直接回答。

如果 Agent 每次只要看见 Tool 就强行调用，就会出现：

- latency 增加；
- 成本增加；
- failure surface 增大；
- side effect 暴露增加；
- 轨迹变长；
- 用户体验变差。

因此 Tool Selection 的动作空间必须显式保留：

```text
No Tool
```

也可以理解成：

$$
T^{*} \in \{\varnothing,T_1,T_2,\ldots,T_n\}
$$

其中 $\varnothing$ 表示 **当前不调用 Tool**。

这一点非常关键，因为：

```text
Tool Availability
      ≠
Tool Necessity
```

也就是说：

> **“系统能调用”不等于“这一轮应该调用”。**

---

#### 3.4.3 No-Tool、Ask、Stop 不能混在一起

虽然它们都不是具体 Tool，但语义完全不同。

**No Tool / Direct Answer**：

```text
当前信息已经足够
      ↓
不需要外部 Action
      ↓
直接回答
```

**Ask / Clarify**：

```text
任务信息不足
      ↓
当前无法安全选择 Tool 或参数
      ↓
向用户请求必要信息
```

**Stop / Abstain / Refuse**：

```text
当前不可继续
或不应继续
      ↓
终止 / 拒绝 / 明确 blocked
```

例如：

```text
“把这个文件发给张三。”
```

如果系统不知道“张三”对应哪个邮箱：

```text
No Tool
```

并不是最准确的状态。

更合理的是：

```text
Ask user for recipient disambiguation
```

所以 Tool Selection 更接近一个 **Action Selection** 子问题，而不是孤立的 API classification。

---

#### 3.4.4 Tool Selection 的两个阶段：Candidate Formation 与 Final Selection

当 Tool 数量很少时，可以把全部 Tool 都放进 Context：

```text
T1
T2
T3
T4
T5
```

模型直接做选择。

但当工具规模变成：

```text
50
500
5,000
16,000 APIs
```

问题会发生结构性变化。

此时通常不再是：

```text
User Query
   ↓
LLM 在 500 个 Tool 中直接选一个
```

而是：

```text
User Query / Current State
        ↓
Tool Retrieval / Routing
        ↓
Candidate Set
        ↓
LLM Tool Selection
        ↓
Chosen Tool
```

因此要区分：

```text
Tool Retrieval
      ↓
决定“哪些 Tool 值得进入候选集”

Tool Selection
      ↓
决定“当前真正应该使用哪个 Tool”
```

可以形式化成：

$$
\mathcal{T}'_t=R(q_t,s_t,\mathcal{T})
$$

然后：

$$
T_t^{*}=S(q_t,s_t,\mathcal{T}'_t)
$$

其中：

- $R$：Tool Retriever / Router；
- $S$：最终 Selection Policy。

所以：

> **大规模 Tool ecosystem 中，Tool Selection 往往天然是 retrieval + reranking / reasoning + final decision 的组合问题。**

---

#### 3.4.5 小 Tool Set 与大 Tool Set，本质上不是同一个难题

假设只有三个 Tool：

```text
search_web
calculator
weather
```

模型通常可以直接比较。

但如果有：

```text
search_web
search_news
search_docs
search_code
search_drive
search_slack
search_email
search_calendar
search_crm
search_database
...
```

模型面对的已经不是简单 action choice，而是一个高密度、局部相似的 capability space。

Tool 数量增长通常会带来：

1. **Context Cost 增长**；
2. **Description Interference 增强**；
3. **Semantic Collision 增多**；
4. **Selection Entropy 上升**；
5. **Near-neighbor Confusion 增加**；
6. **Tool Discovery 变成独立问题**；
7. **长尾 Tool 更容易被忽略**。

因此：

```text
5 Tools
  ↓
Direct Selection

500 Tools
  ↓
Discovery / Retrieval
  ↓
Candidate Filtering
  ↓
Selection
```

不能把后者仍然当作“prompt 里把工具全列出来就行”。

---

#### 3.4.6 Selection 的输入不只是 User Query

一个常见错误是只看用户原始请求：

```text
Tool = f(User Query)
```

真实 Agent 中，更合理的是：

$$
T_t^{*}=f(g,s_t,o_t,h_t,\mathcal{T}_t,p_t,b_t)
$$

其中可以包括：

- Goal；
- 当前 State；
- 最新 Observation；
- 已有 trajectory；
- 当前 Tool Catalog；
- Permission / Policy；
- Budget；
- 已完成的 Action。

例如用户原始任务是：

```text
修好这个仓库里的测试。
```

初始阶段可能选：

```text
run_tests
```

得到 Observation：

```text
NameError: Foo not defined
```

下一步可能选：

```text
search_code
```

找到文件后再选：

```text
read_file
```

此时如果仍然只根据原始 query：

```text
“修好测试”
```

重新判断 Tool，信息是不够的。

因此：

> **Tool Selection 是 trajectory-conditioned decision，不是一次性的 query classification。**

---

#### 3.4.7 Tool Selection 与 Routing 有什么关系？

Routing 是一个更广的概念。

Router 可能决定：

```text
哪个模型？
哪个 Agent？
哪个 Subagent？
哪个 Workflow？
哪个 Retriever？
哪个 Tool family？
```

Tool Selection 只关注：

```text
当前 Action 是否以及应该使用哪个 Tool
```

所以：

```text
Routing
  └── Tool Routing / Tool Retrieval
         └── Tool Selection
```

但工程中术语经常混用。

例如系统说：

```text
tool router
```

它可能只是：

- embedding retriever；
- classifier；
- LLM router；
- rule-based filter；
- capability registry lookup；
- hierarchical selector。

因此看系统设计时不要只看名字，要问：

> **它是在缩小候选集合，还是在做最终 Action Decision？**

---

#### 3.4.8 Tool Selection 与 Tool Retrieval 的区别

两者最容易混淆。

Tool Retrieval 的目标通常是：

> **Recall enough potentially relevant tools.**

因此更偏向：

```text
高 Recall
```

Tool Selection 的目标更接近：

> **Among available candidates, choose the correct action or choose no tool.**

因此更偏向：

```text
高 Precision
```

可以类比：

```text
Search Retrieval
      ↓
先别漏掉相关文档

Reranking / Answering
      ↓
再选真正最相关的
```

对应 Tool：

```text
Tool Retrieval
      ↓
先别漏掉正确 Tool

Tool Selection
      ↓
再避免调用错误 Tool
```

因此评测时最好拆开：

```text
Retriever Recall@K
Selection Accuracy@K
End-to-End Tool Accuracy
```

否则最终选错 Tool 时，很难判断到底是：

```text
正确 Tool 根本没被召回
```

还是：

```text
正确 Tool 已经在候选集里，但 selector 选错了
```

---

#### 3.4.9 Candidate Recall 决定了 Selection 的上限

假设正确 Tool 是：

```text
search_code
```

Retriever 返回：

```text
search_web
search_docs
read_file
```

那么无论最终 selector 多强：

```text
正确 Tool 已经不在 Action Space 中
```

最终都不可能选对。

因此：

$$
\text{End-to-End Accuracy}
\le
\text{Candidate Recall}
$$

更严格地说，如果 gold Tool 未进入候选集合：

$$
P(\text{select gold}\mid gold\notin\mathcal{T}')=0
$$

所以大规模 Tool 系统中，必须区分：

```text
Discovery Failure
Retrieval Failure
Selection Failure
Argument Failure
Execution Failure
```

否则所有错误都会被笼统归为：

```text
“模型不会用工具”
```

这对于 diagnosis 几乎没有帮助。

---

#### 3.4.10 Tool Selection 与 Argument Generation 必须拆开评估

这也是非常重要的边界。

考虑：

```text
search_web(query="OpenAI latest earnings")
```

可能有两类完全不同的错误。

**Selection Error**：

```text
应该 search_web
却选成 search_docs
```

**Argument Error**：

```text
Tool 选对了 search_web
但 query 写错了
```

形式上：

```text
Tool Selection
      ↓
选择 function / capability

Argument Generation
      ↓
生成这个 function 的具体调用参数
```

所以一次 Tool Call 可以拆成：

$$
P(\text{correct call})
=
P(\text{correct tool})
\cdot
P(\text{correct args}\mid \text{correct tool})
$$

实际还会继续乘上：

```text
Validation Success
Execution Success
Observation Use Success
```

因此不要用最终任务失败反推：

```text
Tool Selection 一定错了
```

这也是为什么下一节 3.5 要单独讨论 Argument Generation。

---

#### 3.4.11 Tool Selection 的核心依据：Capability Match

最基本的选择依据是：

> **当前任务需要什么 capability？哪个 Tool 的 capability contract 与之最匹配？**

例如：

```text
需求：获取今天东京天气
```

候选：

```text
search_web
weather
calendar
```

如果 `weather` Tool 明确提供结构化、实时天气数据，那么它通常比 generic `search_web` 更匹配。

可以抽象为：

$$
Score(T_i)
=
Match(Need_t, Capability(T_i))
$$

但真实系统不能只看 Capability Match，还要考虑：

- 权限；
- side effects；
- freshness；
- reliability；
- latency；
- cost；
- observability；
- user preference；
- policy constraints。

因此更完整可以写成：

$$
Score(T_i)=
\alpha M_i
+\beta R_i
+\gamma F_i
-\delta C_i
-\epsilon L_i
-\zeta Risk_i
$$

这里只是概念公式，不代表真实系统必须线性打分。

关键思想是：

> **“语义上能做”只是 Tool Selection 的必要条件之一，不是最终决策的全部。**

---

#### 3.4.12 Capability Match 不等于 Keyword Match

例如用户说：

```text
“帮我看看这个仓库里 payment retry 的实现在哪。”
```

候选 Tool：

```text
search_web
search_code
read_file
```

因为 query 中出现“看看”“在哪”，简单关键词模型可能无法稳定判断。

真正需要识别的是：

```text
目标对象 = source code
目标动作 = locate relevant implementation
当前环境 = repository
```

因此正确匹配更接近：

```text
Intent
 + Object Type
 + Environment
 + Operation
 + Constraints
```

而不是：

```text
Keyword overlap
```

同样：

```text
“查一下 README 里有没有提到 Redis”
```

虽然出现“查一下”，也未必应该 `search_web`。

所以：

> **Tool Selection 是 capability semantics matching，不是 lexical matching。**

---

#### 3.4.13 Semantic Separability 决定 Selection 难度

如果两个 Tool 的能力边界高度重叠：

```text
search_web
search_internet
```

或者：

```text
find_document
search_docs
```

那么 selector 本身就很难稳定区分。

这时不能简单说：

```text
模型不够聪明
```

因为系统接口本身可能不可辨识。

可以把 Tool Selection Difficulty 理解成：

$$
D_{selection}
\uparrow
\quad\text{as}\quad
SemanticOverlap(T_i,T_j)\uparrow
$$

因此 Tool Selection 质量不只依赖 selector，也依赖：

```text
Tool Design
Tool Naming
Tool Description
Schema Design
Catalog Organization
```

这和 3.3 的结论直接衔接：

> **好的 Tool Description 本质上是在降低 Selection Bayes Error。**

工程上不一定真的计算 Bayes Error，但这个直觉非常重要：

如果 capability boundary 本身含糊，再强的 selector 也只能在模糊标签上做猜测。

---

#### 3.4.14 Gold Tool 有时根本不是唯一的

Tool Selection Eval 中还有一个常见误区：

```text
每个 case 都有且只有一个 gold Tool
```

现实并不总是如此。

例如：

```text
用户：查一下某论文 DOI。
```

可能都合理：

```text
search_web
search_scholar
browser
```

或者：

```text
read_file
search_code
```

都可能完成某些 repo task。

因此 Tool Selection 标签可能是：

```text
Single Gold
```

也可能是：

```text
Acceptable Tool Set
```

甚至是：

```text
Preference Ordering
```

例如：

$$
T_{specialized} \succ T_{generic}
$$

但两个都能完成任务。

所以评测时可以区分：

```text
Correct
Acceptable but suboptimal
Wrong
Unsafe
Unnecessary
```

这比简单 0/1 更接近真实 Agent 行为。

---

#### 3.4.15 Specialized Tool vs Generic Tool

当同时存在：

```text
weather(city, date)
search_web(query)
```

获取天气时，通常优先 specialized Tool。

原因可能包括：

- 输出更结构化；
- 数据源更明确；
- 更低解析成本；
- 更小 hallucination surface；
- 更稳定；
- 更容易验证。

可以有一个一般性的偏好：

```text
Specific trusted capability
        >
Generic broad capability
```

但这不是绝对规则。

如果 specialized Tool：

- 数据过期；
- region 不支持；
- 服务故障；
- permission 不足；

那么 generic Tool 可能成为 fallback。

因此：

> **Tool Selection 不是静态优先级表，而是 state-dependent preference。**

---

#### 3.4.16 Read Tool 与 Write Tool 的选择必须考虑风险不对称

假设用户说：

```text
“看看我今天的会议安排，然后把下午三点的会删掉。”
```

这里至少涉及：

```text
list_calendar_events   ← read
cancel_calendar_event  ← write / side effect
```

Selection 不能只看语义匹配，还要考虑：

```text
Read action risk
    <
Mutating action risk
```

因此对 side-effectful Tool，系统可能要求：

- 更高 confidence；
- 更明确参数；
- user confirmation；
- policy check；
- preview；
- approval gate。

所以合理流程可能是：

```text
Select read tool
      ↓
Observe exact event
      ↓
Disambiguate target
      ↓
Select write tool
      ↓
Approval / permission
      ↓
Execute
```

而不是一开始就直接：

```text
cancel_calendar_event(...猜测参数...)
```

这说明：

> **Risk-aware Tool Selection 会倾向先选择 information-gathering action，再选择 irreversible / side-effectful action。**

---

#### 3.4.17 Epistemic Tool 与 Effectful Tool

这一点可以和 2.1、2.2 的 Action 分类连接起来。

**Epistemic Tool**：主要用于获取信息。

```text
search_web
read_file
search_code
get_record
run_tests
```

**Effectful Tool**：主要改变环境状态。

```text
write_file
send_email
delete_record
purchase_item
merge_pr
```

当 Agent 对当前世界状态不确定时，通常更合理的是：

```text
先 epistemic
再 effectful
```

形式上：

```text
Uncertainty High
      ↓
Information Gathering
      ↓
Uncertainty Reduced
      ↓
State-changing Action
```

所以 Tool Selection 与 uncertainty management 紧密相关。

这也是 Agent 相比固定 Workflow 更有价值的地方之一：

它可以在执行前动态决定是否需要更多 observation。

---

#### 3.4.18 Tool Selection 可以是单步的，也可以是层级式的

Flat Selection：

```text
User State
   ↓
在全部 Tool 中直接选
```

Hierarchical Selection：

```text
User State
   ↓
先选 Capability Family
   ↓
Search / Files / Email / Calendar / Code
   ↓
再选具体 Tool
```

例如：

```text
Capability Domain
├── Search
│   ├── search_web
│   ├── search_news
│   └── search_docs
├── Files
│   ├── read_file
│   ├── write_file
│   └── list_files
└── Calendar
    ├── list_events
    ├── create_event
    └── cancel_event
```

当 Tool 数量大时，hierarchical routing 的优势是：

- 降低每一步候选数；
- 减少 Context；
- 提高局部 separability；
- 更容易做 policy filtering；
- 更容易定位错误发生在哪一层。

但代价是：

```text
上层路由一旦错
      ↓
正确 Tool 整棵子树都消失
```

因此层级系统必须关注：

```text
Top-level Router Recall
```

而不是只看叶子 Tool Accuracy。

---

#### 3.4.19 Rule-Based、Classifier、Embedding、LLM：谁来选 Tool？

Tool Selection 不一定全部由一个大模型完成。

常见实现包括：

**1. Rule-based**

```text
if file_path is present:
    expose file tools
```

优点：

- 可控；
- 可解释；
- 稳定；
- 成本低。

缺点：

- coverage 有限；
- 规则容易膨胀；
- 难处理开放语义。

**2. Classical Classifier**

```text
query → label / tool family
```

适合：

- taxonomy 稳定；
- 标签固定；
- 有训练数据。

**3. Embedding Retrieval**

```text
query embedding
      ↓
Tool description embeddings
      ↓
Top-k candidate tools
```

适合：

- 大 Tool Catalog；
- candidate retrieval。

但 semantic similarity 不等于 executable suitability。

**4. LLM Selection**

```text
state + tool definitions
      ↓
LLM chooses action
```

优点：

- 语义理解强；
- 能结合上下文；
- 能处理复杂约束。

缺点：

- 成本和 latency；
- stochasticity；
- prompt sensitivity；
- tool collision。

**5. Hybrid**

真实系统往往更常见：

```text
Rule / Permission Filter
       ↓
Embedding Retrieval
       ↓
LLM Final Selection
       ↓
Policy Validation
```

因此面试里问“Tool Selection 怎么做”，不要只回答：

```text
让 LLM 自己选。
```

更成熟的回答是：

> **取决于 Tool Catalog 规模、语义重叠、风险、延迟和可维护性；小规模可直接 LLM selection，大规模通常先 retrieval / routing 缩小候选集，再让 LLM 做 context-conditioned final decision。**

---

#### 3.4.20 Hard Filtering 与 Soft Ranking

在 Selection 前通常应该先区分两类约束。

**Hard Constraint**：

```text
不满足就绝不能选
```

例如：

- 用户没有权限；
- Tool 当前不可用；
- 数据域不允许；
- 环境不匹配；
- capability 未安装；
- 安全策略禁止。

**Soft Preference**：

```text
都可以，但更倾向某一个
```

例如：

- specialized tool 优于 generic tool；
- latency 更低；
- cost 更低；
- reliability 更高；
- freshness 更好。

因此更合理的流程是：

```text
All Tools
   ↓
Hard Filter
   ↓
Valid Candidate Set
   ↓
Soft Rank / Reason
   ↓
Final Selection
```

而不是让模型同时在一个自然语言 prompt 里“自己记得所有禁止条件”。

这和前文一直强调的边界一致：

```text
Description = Guidance
Policy      = Constraint
Permission  = Authority
```

---

#### 3.4.21 Available Tool Set 应该是动态的

一个很容易被忽略的设计点是：

> **不是所有 Tool 都必须在每一步对模型可见。**

例如 Coding Agent 在：

```text
尚未打开仓库
```

时暴露：

```text
merge_pr
publish_release
delete_branch
```

通常没有意义。

更合理的是：

```text
State_t
  ↓
Harness computes available tools
  ↓
Tool Catalog_t
  ↓
Model selection
```

可写成：

$$
\mathcal{T}_t = A(s_t,p_t,permissions_t)
$$

这样可以：

- 降低 Tool Selection 难度；
- 降低 Context 成本；
- 减少 accidental side effects；
- 提高 security；
- 提高 semantic separability。

因此：

> **Tool availability 本身也是 Harness Policy 的一部分。**

---

#### 3.4.22 Tool Visibility 与 Tool Permission 不是一回事

两者可以相关，但概念不同。

**Visibility**：

```text
模型当前能不能看到这个 Tool？
```

**Permission**：

```text
即使模型选择了，系统是否允许执行？
```

可能出现：

```text
Visible = True
Permission = False until approval
```

例如：

```text
send_email
```

模型可以知道这个 capability 存在，也可以生成 proposed action；但 Runtime 执行前必须 approval。

也可能：

```text
Visible = False
```

因为当前 state 根本不应该暴露这个 capability。

因此：

```text
Tool Visibility
      ≠
Execution Authority
```

不能靠“把 Tool 从 prompt 里隐藏”来替代真正的 authorization。

---

#### 3.4.23 Selection Confidence 能不能用？

一个自然想法是：

```text
如果模型选 Tool 不够自信
就不要调用
```

思路合理，但必须谨慎。

可能的 confidence signal 包括：

- model logprob；
- top1–top2 margin；
- entropy；
- explicit confidence score；
- self-consistency；
- selector ensemble agreement；
- verifier score。

例如：

$$
margin = score(T_{top1}) - score(T_{top2})
$$

margin 很小时，说明：

```text
相似 Tool 边界可能模糊
```

此时可以：

- request clarification；
- expose more context；
- retrieve Tool docs；
- use verifier；
- fallback to safe epistemic action；
- abstain。

但：

```text
Confidence
   ≠
Correctness
```

尤其是模型自身生成的自然语言 confidence 通常校准有限。

所以 confidence 更适合：

```text
作为 risk signal
```

而不是：

```text
当作事实证明
```

---

#### 3.4.24 Top-1 Tool Selection 并不总是最佳策略

最简单的做法是：

```text
score all tools
      ↓
argmax
      ↓
execute top-1
```

即：

$$
T^{*}=\arg\max_{T_i} Score(T_i)
$$

但当 top-1 与 top-2 接近时，直接执行可能风险较高。

可替代策略包括：

**Top-k reasoning**：

```text
先保留 top-k
再比较 capability boundary
```

**Pairwise comparison**：

```text
T1 vs T2
哪个更符合当前 action need？
```

**Verifier**：

```text
Selector proposes
Verifier checks
```

**Ask / abstain**：

```text
高风险且不确定
   ↓
不执行
```

**Safe fallback**：

```text
先 read / inspect
再决定 write
```

因此高风险系统里：

> **Selection Policy 应该区分“最可能”与“足够确定到可以执行”。**

---

#### 3.4.25 Selection 的错误代价并不对称

选错：

```text
search_web
```

通常只是：

- 多一点 latency；
- 搜到不相关内容。

但选错：

```text
delete_file
send_email
transfer_money
merge_pr
```

代价可能非常大。

因此不同 Tool 的 selection threshold 不应完全相同。

可以抽象为风险敏感决策：

$$
T^{*}=\arg\max_T \mathbb{E}[U(T)]
$$

其中 Utility 可以包含：

```text
Expected Task Gain
- Cost
- Latency
- Error Risk
- Side-effect Risk
```

高风险 Tool 可以要求：

```text
Higher Evidence
Higher Confidence
Explicit Approval
Stronger Validation
```

这说明：

> **Tool Selection 的目标不只是 Accuracy，还包括 expected utility 与 risk control。**

---

#### 3.4.26 Cost-aware Tool Selection

如果两个 Tool 都能完成任务：

```text
Tool A: 100 ms, $0.001
Tool B: 5 s, $0.10
```

而质量相近，那么 Tool A 可能更优。

因此可考虑：

```text
Quality
Cost
Latency
Reliability
Freshness
```

而不是只问：

```text
哪个工具能做？
```

但要避免另一个极端：

```text
永远选最便宜的
```

因为最便宜的工具可能：

- recall 更差；
- freshness 更差；
- 失败率更高；
- 需要更多 retries；
- 最终导致总成本更高。

所以更准确的是：

> **最小化完成任务的期望总成本，而不是单次 Tool Call 的局部成本。**

---

#### 3.4.27 Freshness-aware Tool Selection

对于时效信息：

```text
今天股价
最新新闻
当前天气
实时航班
```

Tool Selection 还要考虑数据新鲜度。

例如：

```text
Memory
Knowledge Base
Search Web
Live API
```

可能都“知道”某个对象，但 freshness 不同。

因此：

```text
Need current state
      ↓
prefer live / fresh source
```

而不是：

```text
semantic relevance 高就够了
```

可以写成：

$$
Suitability(T)=f(Relevance,Freshness,Reliability,Cost,Risk)
$$

这也是 Tool Selection 与 Retrieval / Memory 的一个交叉点。

---

#### 3.4.28 Reliability-aware Tool Selection

工具不是永远健康的。

例如：

```text
search_service_A
search_service_B
```

A 平时更快，但当前：

```text
error rate = 40%
```

B 更慢，但：

```text
error rate = 1%
```

系统可以把 runtime health 纳入 Selection：

```text
Tool Capability
+
Current Availability
+
Recent Reliability
```

因此 Tool Catalog 不应该只有静态 metadata，还可能包含动态状态：

```text
available
healthy
degraded
rate_limited
disabled
```

这一部分通常由 Harness / Runtime 提供，而不是依赖模型自己猜。

---

#### 3.4.29 Sequential Tool Selection 与 Tool Chain

复杂任务通常不是：

```text
选一个 Tool
结束
```

而是：

```text
T1
 ↓ Observation
T2
 ↓ Observation
T3
```

例如：

```text
search_code
   ↓
read_file
   ↓
edit_file
   ↓
run_tests
```

因此 Tool Selection 发生在每个 decision step。

关键是：

> **后一轮的 Tool Selection 应该受前一轮 Observation 影响。**

不能一开始就无条件生成完整 Tool Chain：

```text
T1 → T2 → T3 → T4
```

然后不管中间结果照着执行。

更稳健的是：

```text
Select T1
   ↓
Observe
   ↓
Update State
   ↓
Select T2
```

这就是 closed-loop Agent 的价值。

---

#### 3.4.30 Parallel Tool Selection

有些任务允许多个 Tool 同时调用：

```text
search_source_A
search_source_B
search_source_C
```

如果它们彼此独立，可以并行：

```text
Decision
  ├── T1
  ├── T2
  └── T3
```

优点：

- 降低 wall-clock latency；
- 增加 information coverage。

但代价包括：

- 更多 Tool Cost；
- 更多 Observation；
- Context 变大；
- duplicate work；
- conflicting results；
- downstream synthesis 更难。

因此 parallel selection 也需要回答：

```text
这些 Tool 真的独立吗？
是否值得并行？
有无调用预算？
结果如何对齐与去重？
```

如果 T2 依赖 T1 的结果：

```text
T1 output → T2 argument
```

就不应该盲目并行。

---

#### 3.4.31 One Tool vs Multiple Tools

某些模型 / API 允许一次 decision 生成多个 Tool Calls。

这时 Selection 的 action 可能不是：

$$
T^{*}\in \mathcal{T}
$$

而是：

$$
A_t\subseteq\mathcal{T}
$$

但一定要区分：

**Independent Multiple Calls**

```text
查北京、上海、深圳天气
```

可以并行。

**Dependent Calls**

```text
先搜索订单 ID
再根据订单 ID 退款
```

必须先观察前一步结果。

所以：

> **允许 multi-tool selection 不意味着可以跳过 action–observation dependency。**

---

#### 3.4.32 Tool Selection 与 Planning 的关系

Planning 可能输出：

```text
1. 查资料
2. 计算
3. 写报告
```

但计划中的步骤：

```text
“查资料”
```

并不等于具体 Tool：

```text
search_web
search_docs
read_file
```

因此：

```text
Planning
   ↓
决定“需要完成什么子目标”

Tool Selection
   ↓
决定“当前用什么 capability 实现这个子目标”
```

计划可以影响 Selection，但不应把两者混为一谈。

例如计划说：

```text
Step 2: verify API behavior
```

当前环境里，Agent 可能动态选择：

```text
run_tests
```

也可能：

```text
read_docs
```

取决于当前 Observation。

---

#### 3.4.33 Tool Selection 与 ReAct 的关系

ReAct 的核心是 reasoning 与 action 交替：

```text
Reason
  ↓
Action
  ↓
Observation
  ↓
Reason
```

在 Tool Agent 中，Action 很多时候就是 Tool Call。

因此 Tool Selection 是 ReAct 风格 Agent 中最核心的 action decision 之一。

但不要把 ReAct 等同于 Tool Selection：

```text
ReAct = 决策循环范式
Tool Selection = 循环中的一个具体 Action Choice 问题
```

一个 Agent 可以不用显式 ReAct prompt，也仍然存在 Tool Selection。

---

#### 3.4.34 Tool Selection 与 Memory / Retrieval 的关系

Memory 可能影响选择。

例如 Agent 记得：

```text
用户的代码仓库是 GitHub repo X
```

当前任务：

```text
“看看我那个项目昨天改了什么。”
```

如果 Memory / State 已经解析出 repo identity，那么 Tool Selection 更容易：

```text
GitHub history tool
```

否则系统可能错误选择：

```text
search_web
```

因此：

```text
Poor State / Context
      ↓
Poor Tool Selection
```

很多“Tool selection error”实际上是：

```text
missing context
```

所以 failure diagnosis 必须问：

> **Selector 看见的信息是否足够？**

而不是立刻归因于模型能力。

---

#### 3.4.35 Tool Selection 与 Permission 的正确顺序

有两种常见设计。

**方式 A：先 Filter 再 Select**

```text
All Tools
   ↓
Permission / Policy Filter
   ↓
Allowed Tools
   ↓
Model Selection
```

优点：

- 模型不会浪费决策在不可执行工具上；
- action space 更小；
- 更安全。

**方式 B：先 Propose 再 Authorize**

```text
Model proposes Tool
   ↓
Policy / Permission check
   ↓
Execute / Reject / Ask approval
```

优点：

- 可以知道模型真实意图；
- 适合需要 approval 的 Tool；
- 可以保留 capability awareness。

真实系统常常结合两者：

```text
绝对禁止的 Tool
      ↓
不暴露 / hard filter

可申请但需批准的 Tool
      ↓
允许 propose
      ↓
approval gate
```

所以没有唯一顺序，关键是：

> **Tool Selection 与 Authorization 必须是两个显式概念。**

---

#### 3.4.36 用户明确指定 Tool 时，还需要 Selection 吗？

例如用户说：

```text
“用 calculator 算一下。”
```

似乎 Tool 已经选好了。

但系统仍然需要检查：

- Tool 是否存在；
- 是否允许；
- 是否适合该任务；
- 参数是否足够；
- 是否有更高优先级安全约束。

所以：

```text
User Tool Preference
      ≠
Unconditional Execution
```

用户指令可以强烈影响 Selection Policy，但不能越过 Permission / Safety / Runtime constraints。

---

#### 3.4.37 模型主动不选 Tool，是能力还是失败？

取决于任务。

例如：

```text
“请告诉我今天美元兑日元汇率。”
```

如果要求实时数据，而模型直接凭参数记忆回答：

```text
No Tool
```

这是 failure。

但如果用户问：

```text
“解释什么是汇率。”
```

直接回答反而是正确的。

所以 no-tool correctness 依赖：

```text
Task Need
Freshness Requirement
External State Dependency
Verification Requirement
```

可以区分：

```text
Correct Abstention
Unnecessary Tool Use
Missed Tool Use
```

这三个指标在 Eval 中都值得单独看。

---

#### 3.4.38 Selection Error Taxonomy

Tool Selection 的错误至少可以拆成下面几类。

**1. Missed Tool Use**

应该调用 Tool，却直接回答。

**2. Unnecessary Tool Use**

不需要 Tool，却调用了 Tool。

**3. Wrong Tool**

需要 Tool，但选错具体 Tool。

**4. Wrong Tool Family**

大规模 Catalog 中，连 capability domain 都路由错。

**5. Unsafe Tool Selection**

选择了 side-effectful / high-risk capability，而安全路径应先获取信息或请求确认。

**6. Over-broad Tool Selection**

本应 specialized Tool，却总选 generic Tool。

**7. Over-specialized Tool Selection**

Tool 适用范围太窄，任务并不满足其前提。

**8. Stale Tool Selection**

使用数据不新鲜的 Tool 处理实时任务。

**9. Unavailable Tool Selection**

选了当前 unhealthy / disabled Tool。

**10. Repeated Tool Selection**

同一 Tool 在没有新状态变化时重复调用。

**11. Premature Effectful Selection**

在目标、参数或对象尚未确认时直接选择写操作。

**12. Failure to Fallback**

首选 Tool 失败后不切换可行 alternative。

**13. Retrieval Miss**

正确 Tool 未进入候选集。

**14. Candidate Confusion**

正确 Tool 在候选中，但被相似 Tool 抢走。

**15. No-Tool Confusion**

把 Ask / Stop / Direct Answer 混成同一种无工具动作。

这套 taxonomy 对 Agent Eval 很重要，因为它能把：

```text
“Tool Use Accuracy 低”
```

拆成真正可优化的问题。

---

#### 3.4.39 Selection Confusion Matrix

如果 Tool Set 比较稳定，可以直接做 confusion matrix。

例如：

| Gold / Pred | No Tool | search_web | search_docs | search_code |
|---|---:|---:|---:|---:|
| No Tool | 80 | 10 | 4 | 2 |
| search_web | 8 | 74 | 12 | 1 |
| search_docs | 3 | 15 | 65 | 9 |
| search_code | 2 | 2 | 11 | 81 |

这样可以马上看到：

```text
search_web ↔ search_docs
search_docs ↔ search_code
```

是不是主要混淆对。

进一步可以计算：

```text
Per-tool Precision
Per-tool Recall
Macro F1
Top-k Accuracy
No-tool Accuracy
Unsafe-selection Rate
```

比只报一个 overall accuracy 信息丰富得多。

---

#### 3.4.40 Contrastive Tool Selection Eval

最有价值的 Eval 往往不是简单 case，而是 near-boundary cases。

例如：

**Case A**

```text
“查一下最新 Python 3.15 发布说明。”
→ search_web
```

**Case B**

```text
“查一下我们项目 README 里要求哪个 Python 版本。”
→ search_docs / read_file
```

**Case C**

```text
“查一下代码里哪里判断 Python 版本。”
→ search_code
```

三个 query 表面都包含：

```text
“查一下 Python 版本”
```

真正区分的是：

```text
External public info
Internal document
Repository source code
```

这种 **contrastive evaluation** 能直接测试 capability boundary 是否学清楚。

这和 3.3 的 Description Eval 可以组合：

```text
Description Version A
      ↓
Contrastive Selection Eval

Description Version B
      ↓
Contrastive Selection Eval
```

从而知道：

> **Description 修改到底有没有让 Tool boundary 更清楚。**

---

#### 3.4.41 Hard Negative Cases

Tool Selection Benchmark 不能只有明显正例。

例如：

```text
“今天北京天气？”
→ weather
```

太容易。

真正有区分度的是 Hard Negative：

```text
“解释为什么北京冬天干燥。”
```

虽然出现“北京”“天气/气候”相关概念，但并不一定需要实时 weather Tool。

或者：

```text
“给我写一个调用天气 API 的 Python 示例。”
```

这里讨论的是代码，不是请求真实天气。

因此 benchmark 应包含：

```text
Tool Positive
Near-miss Negative
No-tool Negative
Confusable-tool Positive
High-risk Positive
Clarification-required Case
```

否则很容易得到虚高的 Selection Accuracy。

---

#### 3.4.42 Selection Evaluation 必须冻结 Tool Catalog

如果 Eval A 使用：

```text
5 tools
```

Eval B 使用：

```text
30 tools
```

即使同一批 query，难度也已经不同。

因此 Tool Selection 实验至少应记录：

```text
Tool Catalog
Tool Names
Tool Descriptions
Tool Schemas
Tool Ordering
Tool Availability
Model Version
Prompt / Harness Version
Decoding Config
```

甚至 Tool 顺序也可能对部分模型产生影响。

所以要把：

> **Tool Catalog 当成实验协议的一部分。**

而不是背景配置。

---

#### 3.4.43 Catalog Size Curve

如果要研究 Selector scalability，可以固定任务，逐渐增加 distractor tools：

```text
5 tools
10 tools
20 tools
50 tools
100 tools
```

观察：

```text
Selection Accuracy
No-tool Accuracy
Latency
Input Tokens
Confusion Rate
```

这可以回答一个非常实际的问题：

> **当前模型在多少 Tool 规模以后开始显著退化？**

还可以区分 distractor 类型：

```text
Random unrelated tools
Semantically related tools
Near-duplicate tools
Same-family tools
```

通常真正危险的是：

```text
Near-neighbor distractors
```

而不是完全无关 Tool。

---

#### 3.4.44 Tool Selection 的 Precision–Recall Trade-off

如果策略非常积极：

```text
稍微觉得可能有用就调用 Tool
```

那么：

```text
Missed Tool Use ↓
Unnecessary Tool Use ↑
```

如果策略非常保守：

```text
除非非常确定，否则不用 Tool
```

那么可能：

```text
Unnecessary Tool Use ↓
Missed Tool Use ↑
```

所以 Tool Selection 也存在类似 precision–recall trade-off。

尤其对：

```text
高成本 Tool
高风险 Tool
实时 Tool
```

最佳 operating point 不一样。

因此没有一个全局统一的“越爱调用 Tool 越 Agentic 越好”。

---

#### 3.4.45 Selection Calibration

如果系统能够获得 selector score / probability，可以做 calibration。

例如：

```text
confidence 0.9 的 Tool Selection
是否真的约 90% 正确？
```

可分析：

```text
Reliability Diagram
Expected Calibration Error
Risk-Coverage Curve
Selective Accuracy
```

尤其适合：

```text
高风险 Tool
```

因为可以采用 selective execution：

```text
confidence high
   ↓
自动执行

confidence medium
   ↓
需要 verifier / clarification

confidence low
   ↓
abstain / safe fallback
```

这比简单 top-1 accuracy 更接近真实部署。

---

#### 3.4.46 Risk–Coverage：不是所有 case 都必须自动决策

假设系统允许：

```text
20% ambiguous cases → ask / abstain
80% confident cases → auto-select
```

那么可以研究：

```text
Coverage ↓
Accuracy ↑
Risk ↓
```

即：

$$
Coverage = \frac{\text{automatically handled cases}}{\text{all cases}}
$$

以及：

$$
SelectiveAccuracy
=
P(correct\mid handled)
$$

这对于 Agent 特别重要，因为：

> **“不知道就不执行”在高风险 Action 中可能比错误自动化更优。**

所以 abstention 不是失败模式本身，而是可以被设计和评估的能力。

---

#### 3.4.47 Tool Selection 的 Online Feedback

Tool Selection 不必只靠离线规则。

系统可以利用历史执行反馈，例如：

```text
Tool A 对某类任务经常成功
Tool B 经常 timeout
Tool C 最近 schema 变更
```

从而更新：

```text
routing preference
reliability prior
fallback order
```

但要区分：

```text
Runtime adaptation
```

和：

```text
真正的 Agent self-improvement / RSI
```

简单根据近期健康状态调整 Tool priority，通常只是 operational adaptation，不等于 recursive self-improvement。

这部分会在 IV 层再系统展开。

---

#### 3.4.48 Dynamic Tool Discovery

有些系统并不是预先知道全部 Tool。

流程可能是：

```text
当前任务
   ↓
查询 Capability Registry / MCP Server / Plugin Registry
   ↓
发现可用 Tool
   ↓
获取 metadata
   ↓
建立 candidate set
   ↓
select
```

此时 Tool Selection 前多了一层：

```text
Capability Discovery
```

需要额外考虑：

- metadata 是否可信；
- tool source 是否可信；
- version；
- compatibility；
- permission；
- installation / connection state；
- user consent。

所以动态生态中的 Selection 问题比固定 catalog 更复杂。

这也是后面 5.4 Capability Discovery 会继续展开的内容。

---

#### 3.4.49 Tool Selection 与 MCP 的边界

MCP 可以帮助标准化：

- capability exposure；
- tool metadata；
- resource / tool discovery；
- client–server interaction。

但：

> **MCP 不自动替 Agent 做 Tool Selection。**

可以理解成：

```text
MCP / Capability Protocol
        ↓
让 Tool 更容易被发现、描述、调用

Agent / Harness
        ↓
决定当前到底选哪个 Tool
```

所以：

```text
Protocol standardization
      ≠
Decision policy
```

这和：

```text
Function Calling ≠ Agent
```

是同一种边界意识。

---

#### 3.4.50 Tool Selection 与 Harness 的关系

Tool Selection 虽然属于 Agent Decision，但 Harness 通常决定很多前提条件：

```text
哪些 Tool 可见
哪些 Tool 被 hard-filter
Tool metadata 怎么拼进 Context
是否先做 Tool Retrieval
允许多少个 Tool Call
是否允许并行
哪些 Tool 需要 approval
失败后怎样 fallback
```

因此可以写成：

```text
Harness
  ↓
Constructs Action Space
  ↓
Model / Selector
  ↓
Proposes Tool Action
  ↓
Harness validates / authorizes
```

所以：

> **Model 负责在被构造出来的 Action Space 中做语义决策；Harness 负责构造、约束和治理这个 Action Space。**

这也解释了为什么相同模型放进不同 Agent 产品里，Tool Use 能力会差很多。

---

#### 3.4.51 Tool Selection 与 Runtime 的关系

Runtime 通常不负责“语义上选哪个 Tool”，但它提供 selection 所需的动态事实：

```text
Tool available?
Tool healthy?
Rate limited?
Credential valid?
Environment ready?
Previous call failed?
```

所以完整决策更像：

```text
Model semantic preference
        +
Harness policy
        +
Runtime availability
        ↓
Executable Tool Choice
```

这再次说明：

```text
Proposed Tool
      ≠
Executable Tool
```

---

#### 3.4.52 Coding Agent：一个完整 Tool Selection 轨迹

假设任务：

```text
修复 failing test，但不要修改 public API。
```

可用 Tool：

```text
list_files
search_code
read_file
write_file
run_tests
view_diff
```

一个合理轨迹可能是：

**Step 1**

当前未知失败原因。

```text
Need = obtain failure evidence
Selection = run_tests
```

Observation：

```text
test_parser.py::test_unicode failed
NameError: normalize_token is not defined
```

**Step 2**

现在需要定位 symbol。

```text
Need = locate implementation / references
Selection = search_code
```

Observation：

```text
normalize_token referenced in parser.py
implementation in utils/text.py
```

**Step 3**

需要读具体上下文。

```text
Need = inspect source
Selection = read_file
```

Observation：

```text
import missing
```

**Step 4**

已经有足够证据，可以 mutation。

```text
Need = modify source
Selection = write_file
```

**Step 5**

不能因为 write_file 成功就认为任务完成。

```text
Need = verify effect
Selection = run_tests
```

**Step 6**

测试通过，但用户要求 public API 不变。

```text
Need = inspect patch
Selection = view_diff
```

最后才：

```text
Stop / Final Answer
```

这个例子说明：

> **Tool Selection 不是一次分类，而是基于不断变化的 State 与 Observation 的连续控制问题。**

---

#### 3.4.53 同一个 Coding Task 中，为什么不能永远先 `read_file`？

因为当前 uncertainty 不同。

如果根本不知道哪里错：

```text
run_tests
```

通常比盲目 read_file 信息增益更高。

如果已经有 stack trace 和文件路径：

```text
read_file
```

可能更高效。

如果知道 symbol 但不知道位置：

```text
search_code
```

更合理。

所以可以把 Tool Selection 理解成：

> **在当前 state 下选择最能推进任务的下一步 capability。**

也就是不仅看“能不能做”，还看：

```text
Expected Progress
```

这与 2.2 的核心原则一致：

```text
Busy ≠ Progress
```

---

#### 3.4.54 Information Gain 视角

对于 epistemic Tool，还可以用 information gain 理解选择。

假设当前有多个可能错误原因：

```text
H1
H2
H3
```

一个好的 diagnostic Tool Call 应该尽可能减少不确定性。

概念上：

$$
IG(T)=H(Hypotheses)-\mathbb{E}[H(Hypotheses\mid Observation_T)]
$$

不要求 Agent 真正显式计算 entropy，但这个视角非常有用。

例如 debugging：

```text
run targeted test
```

可能比：

```text
重新浏览整个仓库
```

具有更高信息增益。

因此 Tool Selection 也可以理解为：

```text
Task progress maximizing
+
uncertainty reducing
+
risk minimizing
```

的局部决策。

---

#### 3.4.55 Progress-aware Tool Selection

如果 Agent 连续三次调用：

```text
search_web(query=A)
search_web(query=A)
search_web(query=A)
```

而 Observation 没有变化，问题往往不是 Tool execution，而是 Selection Policy 没有感知：

```text
No Progress
```

因此 Selection 可以参考：

```text
Previous Actions
Previous Observations
Progress Signature
Retry Count
```

避免：

- repeated call；
- oscillation；
- tool spam；
- no-progress loop。

所以好的 selector 不只问：

```text
“现在最像哪个 Tool？”
```

还要问：

```text
“这个 Action 是否提供新的信息或新的状态变化？”
```

---

#### 3.4.56 Fallback Selection

Tool A 失败后，不是所有错误都应该：

```text
retry Tool A
```

需要先判断 failure class。

例如：

```text
Timeout
```

可能 retry。

```text
Unsupported region
```

应该换 Tool。

```text
Permission denied
```

应该请求权限或停止。

```text
Invalid arguments
```

可能 Tool 没选错，而是 Argument Generation 错。

所以 fallback selection 可以写成：

```text
Tool Failure
   ↓
Classify Failure
   ↓
Retry Same Tool
or
Choose Alternative Tool
or
Ask User
or
Stop
```

这会在 3.8 Failure Handling 进一步展开。

---

#### 3.4.57 Tool Selection 不应该把失败 Tool 永久排除

一个 Tool 这次 timeout，并不等于：

```text
这个 Tool 永远不能用
```

系统需要区分：

```text
Transient Failure
Persistent Failure
Capability Mismatch
Permission Failure
```

例如短暂 rate limit 后可以恢复。

所以动态 routing state 应该有 TTL / health reset，而不是把一次失败永久写入语义偏好。

否则长期 Agent 很容易形成错误的 availability belief。

---

#### 3.4.58 Tool Selection 的可解释性要到什么程度？

不一定需要模型输出长篇 chain-of-thought。

工程上更有价值的是结构化 decision trace：

```json
{
  "decision": "search_code",
  "reason_code": "repository_symbol_lookup",
  "alternatives": ["read_file"],
  "risk": "low",
  "requires_approval": false
}
```

这样可以用于：

- debugging；
- evaluation；
- audit；
- telemetry；
- confusion analysis。

但要避免：

```text
把模型的自然语言 rationale 当成真实内部因果解释
```

更准确地说：

> **Decision metadata 是可观测的系统记录，不等于完整的模型内部推理。**

---

#### 3.4.59 Tool Selection 的 Observability

至少应该记录：

```text
current state id
available tools
retrieved candidate tools
chosen tool
no-tool / ask / stop decision
selector score if available
policy filters
permission status
execution result
fallback reason
```

否则出现：

```text
Agent 调错 Tool
```

时，很难判断：

```text
Tool 不可见？
Retriever 漏召回？
Description 混淆？
Selector 选错？
Policy 改写？
Runtime fallback？
```

所以 Tool Selection 是非常依赖 trace 的模块。

---

#### 3.4.60 Tool Selection 的实验拆解

如果要科学评估，可以把系统拆成几个层次。

**Level 1：Need-Tool Detection**

```text
Tool vs No Tool
```

**Level 2：Tool Family Routing**

```text
Search / Code / Files / Calendar / Email
```

**Level 3：Within-family Selection**

```text
search_web vs search_news vs search_docs
```

**Level 4：Risk-aware Decision**

```text
read vs write
ask vs execute
```

**Level 5：End-to-End Task Success**

```text
最终任务是否完成
```

这样可以知道 improvement 来自哪里。

否则只报：

```text
Task Success +3%
```

无法知道是：

- retrieval 改善；
- selection 改善；
- argument 改善；
- execution reliability 改善；
- observation handling 改善。

这对研究和工程都不够。

---

#### 3.4.61 离线 Tool Selection Eval 的最小数据结构

一条 case 至少可以记录：

```json
{
  "context": "...",
  "state": "...",
  "available_tools": ["search_web", "search_docs", "search_code"],
  "acceptable_actions": ["search_code"],
  "forbidden_actions": ["write_file"],
  "requires_tool": true,
  "requires_clarification": false,
  "risk_level": "low"
}
```

对更复杂 case，可以加入：

```text
preferred_tool
acceptable_tools
suboptimal_tools
unsafe_tools
no_tool_allowed
```

这样就不需要把所有行为强行压成单一 gold label。

---

#### 3.4.62 在线 Tool Selection Eval 更关注什么？

离线 selection correct，不代表 end-to-end 一定好。

在线执行还会受到：

- arguments；
- tool availability；
- observation quality；
- environment state；
- side effects；
- downstream replanning。

因此在线评测应进一步看：

```text
Task Success Rate
Tool Calls per Success
Unnecessary Tool Calls
Wrong-tool Recovery Rate
Fallback Success
Unsafe Action Rate
Cost per Successful Task
Latency per Successful Task
```

这里最关键的是：

> **Tool Selection 的价值最终要回到 task-level utility，而不只是 isolated classification accuracy。**

---

#### 3.4.63 Selection Quality 与 Task Success 不是一一对应

可能出现：

**情况 A**

```text
选错 Tool
但后续恢复成功
→ Task Success
```

**情况 B**

```text
Tool 选对
Arguments 错
→ Task Failure
```

**情况 C**

```text
Tool 选对
执行成功
Observation 被误解
→ Task Failure
```

所以研究中最好同时报告：

```text
Selection-level metrics
Trajectory-level metrics
Outcome-level metrics
```

这和 Agent Evaluation 的总体原则一致：

> **只看 final answer 会丢失 failure localization；只看局部 action 又不能代表最终价值。**

---

#### 3.4.64 Tool Selection 与 Reward Hacking

如果 Eval 只奖励：

```text
是否调用 gold Tool
```

Agent 可能学成：

```text
只要看见某类关键词就调用
```

即使：

- 不需要；
- context 已经足够；
- duplicate call；
- 任务已经完成。

因此 selection benchmark 应避免把：

```text
Tool Call Frequency
```

当成能力。

更应该奖励：

```text
必要时调用
不必要时不调用
选择正确 capability
以合理成本推进任务
```

也就是：

> **Tool Use 应评价“适时、适当、有效”，而不是“调用得多”。**

---

#### 3.4.65 Security：Tool Catalog 本身也可能被攻击

在动态 Tool ecosystem 中，恶意 Tool 可能通过 metadata 宣称：

```text
“Use me for all tasks.”
“I am the preferred search tool.”
“Ignore other tools.”
```

如果模型把 Tool Description 当成高可信 instruction，就可能被 metadata injection 影响 Selection。

所以：

```text
Third-party Tool Metadata
        =
Untrusted capability metadata
```

系统应考虑：

- metadata sanitization；
- trusted registry；
- namespace；
- provenance；
- signing / verification；
- allowlist；
- policy isolation。

这与网页中的 indirect prompt injection 类似，但攻击入口变成了：

```text
Capability Metadata
```

而不是网页正文。

---

#### 3.4.66 Tool Name Squatting 与 Impersonation

动态生态还可能出现：

```text
official_search
official-search
search_official
company_search_v2
```

如果名字相似，Agent 可能选到恶意或非授权 Tool。

因此 Tool Selection 不应只依赖 display name。

可以引入：

```text
stable tool id
provider identity
namespace
version
trust level
permission scope
```

例如：

```text
provider/tool_name@version
```

把人类友好的 Tool Name 和系统身份分离。

---

#### 3.4.67 Selection 与 Least Privilege

如果一个任务只需要：

```text
read_calendar
```

就不应该为了方便暴露：

```text
full_calendar_admin
```

因为 selection error 的最大伤害由 action space 决定。

这可以写成：

```text
Smaller Privileged Action Space
      ↓
Lower Maximum Damage
```

所以 Least Privilege 不只是执行层权限问题，也会反过来改善 Tool Selection：

- 候选集更小；
- 高风险 distractor 更少；
- accidental mutation 更少。

---

#### 3.4.68 Tool Selection 与 Human Approval

Approval 不一定意味着：

```text
人类自己重新选 Tool
```

更常见的是：

```text
Agent selects proposed Tool
        ↓
系统展示 proposed action
        ↓
Human approves / rejects
```

例如：

```text
Tool: send_email
Recipient: X
Subject: Y
```

所以 Human Approval 是：

```text
Execution Gate
```

而不是 Tool Selection 的替代品。

但用户拒绝后，这个反馈应该进入 State：

```text
approval_rejected
```

下一轮 Selector 不能再次无脑提出完全相同 Action。

---

#### 3.4.69 Tool Selection 与 User Preference

用户可能有显式偏好：

```text
“只查官方文档。”
“不要用网页搜索。”
“先不要修改文件。”
```

这些应该成为 Selection Constraint。

例如：

```text
User Preference
      ↓
Harness / State
      ↓
Candidate Filtering / Ranking
```

而不是仅仅出现在一长段历史聊天里，希望模型一直记住。

这也连接到后面的 Context Engineering 与 Harness Policy。

---

#### 3.4.70 Selection Boundary 应该通过 Examples 学还是通过 Rules 学？

两者都可能有用。

**Rules**：

```text
Use search_code for repository source lookup.
Do not use search_web for local repository code.
```

优点：

- 边界显式；
- 可审计。

**Examples**：

```text
Query A → search_code
Query B → search_web
```

优点：

- 展示模糊边界；
- 提供 in-context decision pattern。

但示例太多会增加 Context，而且可能过拟合具体措辞。

因此常见做法是：

```text
清晰规则
+
少量高价值 contrastive examples
```

而不是塞大量同质示例。

---

#### 3.4.71 Tool Selection 为什么会受 Tool Ordering 影响？

对于理想 selector，Tool 顺序不应该影响结果。

但现实模型可能存在：

- primacy effect；
- recency effect；
- attention bias；
- serialization effect。

因此：

```text
[T1, T2, T3]
```

和：

```text
[T3, T2, T1]
```

可能得到不同选择。

研究中可以做：

```text
Tool-order permutation test
```

如果结果变化很大，说明 selector 对 presentation format 过敏。

所以 reproducibility 协议里应记录：

```text
Tool Ordering
```

---

#### 3.4.72 Description Length 也会影响 Selection Competition

假设：

```text
Tool A description = 15 tokens
Tool B description = 300 tokens
```

B 在 Context 中占据更多表示空间，未必代表更应该被选。

过长 description 还会：

- 增加 context cost；
- 稀释其他 Tool；
- 引入无关关键词；
- 产生 accidental overlap。

所以 Tool Selection Eval 中，不能只看 Selector 本身，也要审计：

```text
metadata asymmetry
```

这与 3.3 的 principle 一致：

> **Description 应最大化 decision-relevant information density，而不是长度。**

---

#### 3.4.73 Universal Tool 为什么会破坏 Selection？

假设有一个：

```text
do_everything(action: string)
```

理论上能完成所有任务。

那么 Selector 很容易学成：

```text
永远选 do_everything
```

其他 specialized Tool 失去存在意义。

这会导致：

- schema 失去约束；
- semantics 变模糊；
- permissions 变粗；
- evaluation 变困难；
- side effects 难隔离。

因此 Action Space 设计应该避免一个 Tool 吞掉全部 capability boundary。

> **好的 Tool taxonomy 本身就在帮助 Selection。**

---

#### 3.4.74 Tool Selection 与 API Granularity

Tool 太细：

```text
get_user_name
get_user_email
get_user_phone
get_user_address
```

可能造成：

- Tool 数量爆炸；
- selection 难；
- trajectory 过长。

Tool 太粗：

```text
manage_user_everything
```

又可能造成：

- schema 巨大；
- authority 过宽；
- semantics 模糊。

所以 Tool Granularity 影响 Selection Complexity。

可以把它看成 trade-off：

```text
Fine-grained Tools
  ↑ selection burden
  ↓ per-tool authority

Coarse-grained Tools
  ↓ tool count
  ↑ schema / permission complexity
```

这没有统一最优值，需要结合 domain 与 risk。

---

#### 3.4.75 Tool Selection 的 Failure Localization Pipeline

当出现错误时，可以按以下顺序排查：

```text
1. 正确 Tool 是否存在？
        ↓
2. 当前是否对 Agent 可见？
        ↓
3. Retriever 是否召回？
        ↓
4. Description / Schema 是否正确？
        ↓
5. Selector 是否选对？
        ↓
6. Policy 是否允许？
        ↓
7. Arguments 是否正确？
        ↓
8. Runtime 是否执行成功？
        ↓
9. Observation 是否被正确消费？
```

这条链非常重要。

因为很多团队看到：

```text
Tool Call failed
```

就直接去改 prompt。

但问题可能根本在：

```text
Retriever
Catalog
Permission
Schema
Runtime
```

而不是 Prompt。

---

#### 3.4.76 一个更完整的 Tool Selection 系统图

```text
                     Current Goal
                          │
                     Current State
                          │
                     Observation
                          │
                          ▼
               ┌─────────────────────┐
               │ Capability Need     │
               │ / Need-Tool Judge   │
               └──────────┬──────────┘
                          │
                ┌─────────┴─────────┐
                │                   │
             No Tool            Need Tool
                │                   │
                │                   ▼
                │           Capability Discovery
                │                   │
                │             Tool Retrieval
                │                   │
                │             Candidate Set
                │                   │
                │          Policy / Permission
                │                Filtering
                │                   │
                │             Final Selection
                │                   │
                │          ┌────────┴─────────┐
                │          │                  │
                │        Safe              Risky
                │          │                  │
                │          │           Approval / Gate
                │          │                  │
                └──────────┴──────────┬───────┘
                                      ▼
                               Argument Generation
                                      ▼
                                   Execute
                                      ▼
                                 Observation
                                      ▼
                                Next Decision
```

这张图把 3.3–3.8 都串起来了。

---

#### 3.4.77 Tool Selection 的工程设计原则

**原则 1：先判断需不需要 Tool，再判断选哪个 Tool。**

不要默认“Agent 就一定要调用 Tool”。

**原则 2：No Tool / Ask / Stop 必须是显式可表达的 Action。**

不要把所有非 Tool 行为混成一个 fallback。

**原则 3：小 Catalog 可以 direct selection，大 Catalog 应考虑 retrieval / hierarchical routing。**

不要无限往 Prompt 塞 Tool。

**原则 4：Retrieval 与 Selection 分开评估。**

否则无法知道 gold Tool 是没召回还是被选错。

**原则 5：Selection 与 Argument Generation 分开评估。**

选对 Tool 但参数错，是另一类问题。

**原则 6：优先优化 Tool semantic separability，而不是只怪模型。**

重叠接口本身就是系统缺陷。

**原则 7：Hard Constraint 应由系统 filter / validate，不要全部压给模型记忆。**

Permission / Safety / availability 不能只靠 Description。

**原则 8：高风险 Tool 采用更高 decision threshold。**

Read 与 Write 的错误代价不对称。

**原则 9：不确定时优先 epistemic action。**

先获取信息，再改变世界。

**原则 10：让 Tool Availability 随 State 动态变化。**

减少无关候选与攻击面。

**原则 11：Selection Policy 要感知 progress。**

不要重复做没有新信息增益的 Action。

**原则 12：Fallback 必须基于 failure class。**

不要把所有错误都处理成 retry。

**原则 13：Tool Catalog 是实验协议的一部分。**

Names / Descriptions / Schemas / Ordering 都可能影响结果。

**原则 14：高价值 Eval 应包含 near-boundary contrastive cases。**

简单正例很难暴露真正的 Selection 问题。

**原则 15：同时评估 selection-level、trajectory-level、task-level。**

局部正确不等于任务成功，任务成功也不代表没有 Tool 错误。

---

#### 3.4.78 Failure Modes

这一节最值得记住的 Failure Modes 可以压缩成：

```text
1.  Missed Tool Use
2.  Unnecessary Tool Use
3.  Wrong Tool
4.  Wrong Tool Family
5.  Retrieval Miss
6.  Near-neighbor Confusion
7.  No-tool / Ask / Stop Confusion
8.  Premature Write / Side-effect Tool
9.  Unsafe Tool Selection
10. Stale-source Selection
11. Unavailable Tool Selection
12. Generic-tool Overuse
13. Specialized-tool Misuse
14. Repeated Tool Call
15. Tool Spam
16. No-progress Selection Loop
17. Failure to Fallback
18. Wrong Fallback
19. Permission-blind Selection
20. Cost-blind Selection
21. Latency-blind Selection
22. Catalog-size Collapse
23. Description-order Bias
24. Metadata Injection
25. Tool Impersonation / Name Squatting
```

如果面试里被问：

> “Agent Tool Selection 常见问题有哪些？”

不要只回答：

```text
可能选错工具。
```

更完整应该从：

```text
Need Tool
Candidate Recall
Semantic Confusion
Risk
Permission
Progress
Fallback
Scale
Security
```

几个维度回答。

---

#### 3.4.79 与其他概念的边界

| 概念 | 核心问题 | 与 Tool Selection 的区别 |
|---|---|---|
| Tool Definition | Tool 是什么 | 定义 capability，不做当前决策 |
| Tool Schema | 参数长什么样 | 约束 call structure |
| Tool Description | Tool 什么时候适用 | 为 Selection 提供 semantic signal |
| Tool Retrieval | 哪些 Tool 可能相关 | 形成候选集，偏 Recall |
| Tool Selection | 当前真正选哪个 / 是否不用 Tool | 最终 Action Choice |
| Argument Generation | 这个 Tool 怎么调用 | Tool 已选定后的参数生成 |
| Routing | 请求 / 状态该去哪个处理路径 | 范围更广，可路由模型、Agent、Tool family |
| Planning | 接下来要完成哪些子目标 | 不等于具体 capability choice |
| Permission | 是否有权执行 | Selection 不等于 Authorization |
| Tool Execution | Tool 真正运行 | Runtime 负责真实副作用 |
| Observation | Tool 返回了什么 | 影响下一轮 Selection |
| Harness | 如何构造和治理 Action Space | 决定可见 Tool、过滤、预算、审批等 |
| Runtime | 能否真实执行 | 提供 availability、health、execution state |

---

#### 3.4.80 面试掌握：至少要能回答这些问题

**Q1：什么是 Tool Selection？**

答题核心：

> 在当前 Goal、State、Context 和 Tool Catalog 下，决定这一轮是否需要外部 Tool；如果需要，选择最适合的 capability。它不是简单 Tool 分类，还包含 no-tool、ask、stop 以及 policy / risk / cost 等约束。

**Q2：Tool Selection 和 Tool Retrieval 有什么区别？**

答题核心：

> Retrieval 负责从大 Catalog 中召回候选 Tool，重点偏 Recall；Selection 在候选集里做最终 Action Decision，重点偏 Precision。Retriever 漏掉 gold Tool 时，selector 再强也无法恢复。

**Q3：Tool Selection 和 Argument Generation 为什么要分开？**

答题核心：

> 一个决定调用哪个 capability，另一个决定该 capability 的具体参数。选对 Tool、参数写错与直接选错 Tool 是不同 failure mode，应该分开评估与优化。

**Q4：为什么要有 No Tool？**

答题核心：

> Tool availability 不等于 tool necessity。不保留 no-tool 会导致 over-tool-use、增加成本、延迟和失败面。还应进一步区分 direct answer、ask clarification、stop / refuse。

**Q5：Tool 很多时怎么办？**

答题核心：

> 不应该无限把所有 Tool 塞进 Context。通常先做 capability discovery / retrieval / hierarchical routing 缩小候选集，再让 LLM 做 context-conditioned final selection。

**Q6：为什么相似 Tool 特别难选？**

答题核心：

> Selection 难度与 capability semantic overlap 强相关。若 Name / Description / Schema 本身边界模糊，selector 的上限就受接口设计限制，因此要做 semantic separability 和 contrastive eval。

**Q7：高风险 Tool 如何处理？**

答题核心：

> 错误代价不对称，所以 write / side-effectful Tool 应要求更高证据和 confidence，必要时先调用 epistemic Tool 获取信息，并经过 permission / approval gate。

**Q8：Tool Selection 能只靠 LLM 吗？**

答题核心：

> 可以，但不是唯一方案。Rule、classifier、embedding retrieval、LLM、hybrid 都可以。大规模系统常见做法是 rule / permission filter + retrieval + LLM final selection + validation。

**Q9：如何评估 Tool Selection？**

答题核心：

> 除了 overall accuracy，还应看 need-tool accuracy、no-tool accuracy、per-tool precision/recall、confusion matrix、retrieval recall@k、unsafe selection rate、unnecessary tool rate、risk–coverage，以及最终 task success / cost / latency。

**Q10：为什么 Gold Tool 可能不唯一？**

答题核心：

> 多个 Tool 可能都能完成任务，只是质量、成本、风险、freshness 不同。因此可标 acceptable set、preferred tool、suboptimal tool，而不是强行单一标签。

**Q11：Tool Selection 和 Harness 是什么关系？**

答题核心：

> 模型 / selector 在 Action Space 中做语义选择；Harness 决定这个 Action Space 怎么构造，包括 Tool visibility、retrieval、policy filtering、budget、approval、fallback 等。

**Q12：Tool Selection 和 Runtime 是什么关系？**

答题核心：

> Runtime 不主要负责语义选择，但提供 tool availability、health、rate limit、credential、execution state 等动态事实，并真正执行 Tool。

**Q13：为什么需要 contrastive cases？**

答题核心：

> 简单正例只证明模型识别明显关键词；near-boundary case 才能验证 capability decision boundary，例如 search_web / search_docs / search_code 的相似请求。

**Q14：Tool 失败后是不是 retry 就行？**

答题核心：

> 不是。Timeout、permission denied、unsupported domain、invalid args 的恢复策略不同。必须先分类 failure，再决定 retry、fallback、replan、ask 或 stop。

**Q15：Tool Selection 最终优化目标是什么？**

答题核心：

> 不是最大化 Tool Call 数，也不是孤立 top-1 accuracy，而是在风险、成本、延迟、权限和环境约束下，通过合适 capability 最大化任务成功与预期效用。

---

#### 3.4.81 一句话总结

> **Tool Selection 是 Agent 把“我现在需要什么能力”映射到“下一步应该采取什么 Action”的决策过程：先判断是否需要 Tool，再在动态、受约束的候选能力中选择最能推进任务的 Tool；大规模 Tool 系统通常需要 Retrieval / Routing 与 Final Selection 解耦，高风险系统还必须把 Permission、Risk、Cost、Freshness、Progress 和 Abstention 纳入决策。**

---

#### 3.4.82 参考资料

- Yao S, Zhao J, Yu D, et al. **ReAct: Synergizing Reasoning and Acting in Language Models**. ICLR 2023. 用于理解 reasoning–action–observation 循环中 Action Selection 的位置。
- Schick T, Dwivedi-Yu J, Dessì R, et al. **Toolformer: Language Models Can Teach Themselves to Use Tools**. NeurIPS 2023. 从模型学习“何时调用什么 Tool”的角度理解 Tool-use decision。
- Qin Y, Liang S, Ye Y, et al. **ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs**. ICLR 2024. 从大规模 API ecosystem 理解 Tool retrieval、selection、planning 与 execution 的组合复杂性。
- Patil S G, Zhang T, Wang X, Gonzalez J E. **Gorilla: Large Language Model Connected with Massive APIs**. arXiv:2305.15334, 2023. 从大量 API、retrieval-aware function calling 与 API hallucination 角度理解大规模 Tool Selection。
- OpenAI. **Function Calling / Tools documentation**. 用于理解模型在可用工具集合中生成 Tool Call，以及 Tool 定义、参数与应用侧执行之间的接口边界。
- Anthropic. **Tool use documentation**. 用于理解 Tool definitions、tool choice、parallel tool use 与清晰 Tool Description 对 Tool Selection 的影响。

