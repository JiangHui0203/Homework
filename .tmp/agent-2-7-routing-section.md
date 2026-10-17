### 2.7 Routing

#### 2.7.1 定义：Routing 到底是什么？

前面的 Agent Loop 已经回答：

```text
Agent 怎样循环运行？
```

Planning 回答：

```text
未来若干步怎样组织？
```

Routing 解决的是另一类问题：

> **当当前状态下存在多个合法执行路径、能力、模型、工具、Agent 或 Workflow 时，应该把这次任务交给哪一个？**

因此 Routing 可以定义为：

> **根据当前 Task、State、Context、Capability、Constraint、Cost、Risk 与 Availability，在一组候选执行路径中选择最合适的一条或一组。**

最小结构可以写成：

```text
Task / State
    ↓
Candidate Routes
    ↓
Router
    ↓
Selected Route
    ↓
Execution
    ↓
Outcome / Feedback
```

例如：

```text
用户问天气
```

系统有：

```text
Route A → 普通 LLM 直接回答
Route B → Weather Tool
Route C → Web Search
Route D → Ask User
```

真正 Routing 要决定的是：

```text
现在应该走哪条？
```

所以一句话：

> **Routing 是“从多个可执行路径中做条件选择”的决策机制。**

---

#### 2.7.2 为什么现代 Agent 特别需要 Routing？

单模型、单工具、单路径系统里，几乎没有 routing 问题。

例如：

```text
Input
↓
One Model
↓
Output
```

但现代 Agent 常常同时拥有：

```text
多个模型
多个 Tool
多个 Skill
多个 Subagent
多个 Workflow
多个执行环境
多种 Verification 路径
```

于是系统不再只是：

```text
“下一步做什么？”
```

还要回答：

```text
“谁来做？”
“用什么能力做？”
“走哪条控制路径？”
“失败以后切到哪里？”
```

因此 Routing 是复杂 Agent 从：

```text
single-capability system
```

走向：

```text
heterogeneous capability system
```

后自然出现的控制问题。

---

#### 2.7.3 Routing 的本质：Conditional Computation

Routing 可以从一个更一般的角度理解为：

```text
不是每个输入都使用同样的计算路径。
```

而是：

```text
Input / State 不同
→ 激活不同能力
→ 支付不同计算成本
```

形式上，设候选 route 集合为：

$$
\mathcal{R}=\{r_1,r_2,\ldots,r_n\}
$$

Router 根据当前状态 $s$ 和约束 $c$：

$$
r^*=\pi_{route}(s,c)
$$

或者更一般地：

$$
r^*=\arg\max_{r\in\mathcal{R}} U(r\mid s,c)
$$

其中 utility 可以综合：

```text
Expected Quality
Expected Cost
Latency
Risk
Capability Match
Availability
Reliability
```

所以 Routing 并不是简单分类：

```text
query → label
```

它更接近：

> **在多目标约束下做 capability selection。**

---

#### 2.7.4 Routing 与 Tool Selection 是什么关系？

Tool Selection 是 Routing 的一个特例。

例如当前 Action Space：

```text
search_web
calculator
read_file
send_email
```

模型选择：

```text
calculator
```

这本质上就是：

```text
Tool Routing
```

但 Routing 的范围更宽。

它还可以选择：

```text
Model
Agent
Workflow
Skill
Verifier
Execution Backend
Fallback Path
```

所以：

```text
Tool Selection
⊂
Routing
```

但本知识体系中，Tool Selection 的细节仍放在第 3 章 Tool Use 中；本节关注更一般的控制结构。

---

#### 2.7.5 Routing 可以发生在哪些层？

至少可以分成五类。

```text
1. Model Routing
2. Tool / Capability Routing
3. Agent / Subagent Routing
4. Workflow / Path Routing
5. Escalation / Fallback Routing
```

它们解决的问题不同。

---

#### 2.7.6 Model Routing：应该调用哪个模型？

假设系统有：

```text
Small Model
Medium Model
Strong Model
Specialized Code Model
Vision Model
```

Routing 问题可能是：

```text
简单分类
→ Small Model

复杂 reasoning
→ Strong Model

代码修复
→ Code-specialized Model

图片理解
→ Vision Model
```

这里通常存在 trade-off：

```text
Quality
↔
Cost / Latency
```

如果所有请求都走最强模型：

```text
quality 可能高
cost 很高
latency 较高
```

如果所有请求都走最便宜模型：

```text
cost 低
但 hard case 失败率高
```

因此 Model Router 的目标往往不是：

```text
永远选最强模型
```

而是：

> **在满足质量要求的前提下，把足够简单的任务交给更便宜的模型，把困难或高风险任务升级到更强模型。**

这也是 LLM cascade、cost-aware routing 等研究的核心思想之一。

---

#### 2.7.7 Model Routing 与 Model Cascade 的区别

Model Routing 通常是：

```text
先判断
↓
直接选 Model A / B / C
```

Model Cascade 更像：

```text
先跑便宜模型
↓
如果结果足够可信
    → accept
否则
    → escalate to stronger model
```

例如：

```text
Small Model
↓
confidence / verifier
↓
PASS → use result
FAIL / uncertain → Strong Model
```

所以：

```text
Routing
= selection before / during execution

Cascade
= staged routing with conditional escalation
```

Cascade 本质上是一种 Routing Pattern。

---

#### 2.7.8 Tool / Capability Routing：不是有 Tool 就都暴露给模型

一个 Agent 可能连接：

```text
100 个 Tools
```

如果每轮都把所有工具 schema 全塞进 Context，会产生：

```text
context cost ↑
tool confusion ↑
selection error ↑
latency ↑
```

所以实际系统可以先做 Capability Routing：

```text
Task
↓
Router
↓
选择相关 Tool Group
↓
只暴露必要 Tools
↓
LLM 进行具体 Tool Selection
```

例如：

```text
“帮我分析这个 CSV”
```

先 route 到：

```text
Data Analysis capability group
```

而不是让模型同时看到：

```text
calendar
email
weather
shopping
database
code
browser
...
```

所以：

> **Routing 也可以是 Context / Capability Surface 的压缩机制。**

---

#### 2.7.9 Agent / Subagent Routing：应该交给谁？

在 Multi-Agent 系统中，候选可能是：

```text
Research Agent
Coding Agent
Data Agent
Finance Agent
Reviewer Agent
```

Router 根据任务决定：

```text
当前 Subtask 最适合哪个 Agent？
```

例如：

```text
“查最新论文并修改实验代码”
```

可能拆成：

```text
Literature subtask
→ Research Agent

Code subtask
→ Coding Agent
```

这里 Router 做的不是完整 Planning，而是：

```text
Task / Subtask
→ Agent identity / capability
```

后面第 6 章 Multi-Agent 会详细讨论 Manager、Supervisor、Handoff、Agents-as-Tools 等模式。

---

#### 2.7.10 Workflow Routing：应该进入哪条控制流？

有些产品并不是所有请求都进入同一个 Agent Loop。

例如：

```text
Input
↓
Intent Router
├── FAQ Workflow
├── Refund Workflow
├── Research Agent
└── Human Support
```

这里 Routing 选择的是：

```text
control-flow graph
```

而不是一个具体 Tool。

因此 Workflow Routing 很常见于：

```text
客服
企业自动化
审批
文档处理
数据平台
```

系统可以把高频、稳定、结构化任务放进 deterministic workflow；只有真正需要开放判断的 case 才进入 Agent。

这实际上也是控制 Agenticness 的重要手段。

---

#### 2.7.11 Escalation / Fallback Routing：失败后去哪里？

Routing 不一定只发生在任务开始时。

例如：

```text
Primary Model fails
→ Backup Model

Tool timeout
→ Alternative Tool

Verifier UNKNOWN
→ Gather Evidence

Repeated failure
→ Human Escalation
```

所以 Routing 还负责：

```text
Recovery Path Selection
```

例如：

```text
search_web timeout
↓
retry once
↓
still fail
↓
route to alternative search provider
```

或者：

```text
LLM Judge uncertain
↓
human review
```

这类 Routing 与后面的 Harness Recovery Policy 紧密相关。

---

#### 2.7.12 Router 的输入不应该只有 User Query

一个弱 Router 可能只看：

```text
user text
```

但成熟 Routing 往往还需要：

```text
Task Type
Current State
History
Available Capabilities
Permissions
Budget
Latency Target
Risk Level
Tool Availability
Model Health
User Preference
Previous Failures
Verifier Feedback
```

因此 Router 更准确的输入是：

$$
r_t=R(s_t, g, C, A_t, B_t, H_t)
$$

其中：

- $s_t$：当前 State；
- $g$：Goal；
- $C$：Constraints；
- $A_t$：当前 available routes；
- $B_t$：Budget；
- $H_t$：History / feedback。

这说明：

> **Routing 是 state-dependent decision，不只是 intent classification。**

---

#### 2.7.13 Candidate Route 必须先满足 Feasibility

Router 不应该直接在所有 route 中比较 utility。

第一步应该先过滤：

```text
Capability available?
Permission allowed?
Dependency healthy?
Budget sufficient?
Input modality supported?
Region / policy allowed?
```

先得到：

```text
Feasible Routes
```

再优化：

```text
Quality / Cost / Latency / Risk
```

可以写成：

$$
\mathcal{R}_{feasible}(s)
=
\{r\in\mathcal{R}: constraints(r,s)=true\}
$$

然后：

$$
r^*=\arg\max_{r\in\mathcal{R}_{feasible}} U(r\mid s)
$$

这样可以避免：

```text
Router 选中了“理论上最好”但实际上没有权限执行的 route
```

---

#### 2.7.14 Routing 的四个常见目标

一个 Route 常常需要同时考虑：

```text
Quality
Cost
Latency
Risk
```

概念上：

$$
U(r)=
\alpha Q(r)
-\beta C(r)
-\gamma L(r)
-\delta Risk(r)
$$

这不是固定公式，而是帮助理解多目标 routing。

不同产品可能权重完全不同。

例如：

```text
离线批量分析
→ latency 权重低

实时语音 Agent
→ latency 权重很高

金融写操作
→ risk 权重极高
```

因此：

> **不存在脱离产品约束的“绝对最优 Router”。**

---

#### 2.7.15 Static Routing 与 Dynamic Routing

##### Static Routing

基于预定义规则：

```text
if task_type == "code":
    route = code_agent
```

优势：

```text
稳定
可解释
低成本
容易测试
```

缺点：

```text
边界 case 不灵活
规则可能爆炸
```

##### Dynamic Routing

根据运行时 State / Model / Classifier 决定：

```text
route = router_model(state)
```

优势：

```text
适应复杂语义
处理开放任务
```

缺点：

```text
不确定性
成本
可解释性
routing error
```

成熟系统通常采用：

```text
Deterministic guardrails
+
Learned / LLM routing inside safe region
```

而不是完全二选一。

---

#### 2.7.16 Rule-based Router

最简单 Router：

```python
if contains_image:
    return "vision_model"

if task == "calculation":
    return "calculator"

if risk == "high":
    return "human_review"
```

它非常适合：

```text
硬约束
安全路由
输入模态
明确业务类型
合规规则
```

不要因为 Agent 使用 LLM，就把所有 routing 都交给 LLM。

> **能可靠写成 deterministic rule 的边界，通常应该保留 deterministic。**

---

#### 2.7.17 Classifier / Learned Router

也可以训练或拟合轻量 Router：

```text
Input Features
↓
Classifier
↓
Route Probability
```

例如：

```text
P(simple_model)=0.82
P(strong_model)=0.18
```

优点：

```text
便宜
快
可批量训练
可校准
```

但要注意：

```text
router training distribution
≠
production distribution
```

可能出现 distribution shift。

所以 Router 需要像其他模型一样：

```text
validation
calibration
monitoring
regression
```

---

#### 2.7.18 LLM Router

可以直接让 LLM 输出：

```json
{
  "route": "research_agent",
  "reason_code": "fresh_external_information_required"
}
```

适合：

```text
任务语义复杂
候选路径描述自然语言化
规则难穷举
```

但风险包括：

```text
route hallucination
inconsistent choice
prompt sensitivity
cost
latency
```

所以 LLM Router 最好仍受：

```text
Candidate Set
Schema
Permission
Budget
Policy Guard
```

约束。

它负责：

```text
在允许的候选中选择
```

而不是：

```text
自己创造一个不存在的 route
```

---

#### 2.7.19 Router 输出最好是结构化 Decision

不要只让 Router 输出：

```text
“我觉得应该交给研究 Agent。”
```

更好的 schema：

```json
{
  "route": "research_agent",
  "reason_code": "freshness_required",
  "confidence": 0.84,
  "fallback": "general_agent"
}
```

如果涉及高风险：

```json
{
  "route": "human_review",
  "reason_code": "irreversible_action",
  "confidence": 1.0
}
```

这样 Harness 可以确定性执行。

---

#### 2.7.20 Confidence-based Routing：Confidence 到底是什么？

很多系统采用：

```text
confidence high
→ cheap path

confidence low
→ strong path
```

但这里必须非常谨慎。

因为模型输出的：

```text
"confidence": 0.95
```

不一定校准。

可用信号可能包括：

```text
classifier probability
logprob
entropy
margin
verifier score
ensemble disagreement
self-consistency
historical success rate
```

真正要问的是：

> **这个 routing signal 是否对“当前 route 会不会成功”具有可验证预测力？**

而不是：

```text
它看起来像 confidence
```

---

#### 2.7.21 Uncertainty Routing 与你的推理研究有什么联系？

Routing 可以理解成一种：

```text
conditional computation allocation
```

例如：

```text
low risk / high confidence state
→ cheap / default path

high uncertainty state
→ extra search / stronger model / verifier / exploration
```

这和 test-time reasoning budget allocation 的核心思想一致：

> **额外计算不应该平均分配，而应该路由到最值得使用额外资源的状态。**

可以把 routing 看成：

```text
State
↓
Need more compute?
├── No → fast path
└── Yes → expensive path
```

因此 Router 本身就是一个：

```text
compute allocation policy
```

---

#### 2.7.22 Router 与 Planner 的根本区别

Planner 问：

```text
未来需要做哪些步骤、依赖怎样组织？
```

Router 问：

```text
当前这个 Task / Step 应该走哪条路径？
```

例如 Planner 得到：

```text
1. 搜论文
2. 比较方法
3. 写代码
4. 跑实验
```

Router 再决定：

```text
Step 1 → Research Agent
Step 3 → Coding Agent
Step 4 → GPU Runtime
```

所以：

```text
Planning
= temporal / dependency structure

Routing
= capability / path selection
```

它们可以互相嵌套，但职责不同。

---

#### 2.7.23 Router 与 Orchestrator 的区别

Router 主要做：

```text
select route
```

Orchestrator 更宽：

```text
组织整个多组件执行过程
```

可能包括：

```text
route
sequence
parallelize
wait
merge
retry
cancel
```

所以：

```text
Router
⊂
Orchestration logic
```

一个 Orchestrator 可能内部调用多个 Router。

---

#### 2.7.24 Router 与 Supervisor 的区别

Supervisor 通常有更强的持续控制职责：

```text
观察多个 Agent 状态
分配任务
检查结果
决定是否继续
重新指派
终止
```

Router 可能只做一次：

```text
A or B?
```

所以：

```text
Router
= selection function

Supervisor
= ongoing control role
```

在具体框架里名称可能混用，因此面试时不要只背 API 名称，要解释控制职责。

---

#### 2.7.25 Router 与 Handoff 的区别

Routing 是：

```text
决定交给谁
```

Handoff 是：

```text
真正把控制权 / context / state 移交过去
```

例如：

```text
Router:
route = Billing Agent

Handoff:
transfer current task + relevant context + state
```

所以：

```text
Routing
→ decision

Handoff
→ transfer mechanism
```

后面 Multi-Agent 章节会再展开。

---

#### 2.7.26 Router 与 Load Balancer 的区别

这是工程上很重要的边界。

Load Balancer 解决：

```text
多个等价实例中把流量发给哪个实例？
```

例如：

```text
model-server-1
model-server-2
model-server-3
```

它通常关心：

```text
load
health
region
capacity
```

Router 解决：

```text
应该使用哪种能力 / 模型 / 路径？
```

例如：

```text
small-model
vs
strong-model
```

所以：

```text
Router
= semantic / capability selection

Load Balancer
= infrastructure instance selection
```

真实系统里两层会串联：

```text
Router selects strong_model
↓
Load Balancer selects replica-7
```

---

#### 2.7.27 Router 与 Dispatcher 的区别

Dispatcher 通常强调：

```text
把已确定的任务发送给目标执行单元
```

Routing 则强调：

```text
先决定目标是谁
```

所以可以记成：

```text
Router decides destination
Dispatcher delivers work
```

当然，不同系统命名并不严格统一。

---

#### 2.7.28 Router 与 Policy 的关系

从更高层看，Routing 本身就是 Policy 的一个子问题。

Agent Policy 可能决定：

```text
next_action
```

Router Policy 决定：

```text
which executor / capability / path
```

因此可以把 route 看成一种高层 Action：

```text
route_to(research_agent)
route_to(strong_model)
route_to(human)
```

但把 Routing 单独拿出来讨论很有价值，因为：

```text
跨模型
跨工具
跨 Agent
跨 Workflow
```

时，它会成为独立系统组件。

---

#### 2.7.29 Hierarchical Routing：一次 Routing 不一定够

复杂系统可以分层：

```text
Task
↓
Domain Router
↓
Research Domain
↓
Agent Router
↓
Research Agent
↓
Tool Router
↓
Web Search
```

这种结构叫：

```text
Hierarchical Routing
```

优点：

```text
每层候选更少
职责清晰
context 更小
```

缺点：

```text
上层 route 错误会向下传播
```

例如：

```text
Domain Router 错把 coding task 判成 writing
```

后面再强的 Tool Router 也救不回来。

所以 Hierarchical Router 需要：

```text
fallback
re-routing
uncertainty handling
```

---

#### 2.7.30 Multi-label / Composite Routing

Routing 不一定只能选一个。

有些 Task 需要：

```text
Research Agent
+
Coding Agent
```

或者：

```text
Web Search
+
Database
```

所以 Route 输出可以是：

```text
one-of-N
```

也可以是：

```text
subset-of-N
```

甚至：

```text
ordered route set
```

例如：

```text
primary = official_api
fallback = web_search
escalation = human
```

因此不要把 Routing 永远理解成单标签分类。

---

#### 2.7.31 Parallel Routing

如果两个路径彼此独立，而且结果都需要：

```text
route → A + B in parallel
```

可能比：

```text
A → wait → B
```

更低 latency。

例如：

```text
search official source
search academic source
```

可以并行。

但并行也意味着：

```text
cost ↑
result merge complexity ↑
conflict resolution ↑
```

所以：

> **Parallel Routing 是 latency–cost trade-off，不是默认最优。**

---

#### 2.7.32 Stateful Routing：Route 可能依赖历史

同一个 query 在不同 State 下，route 可以不同。

例如：

```text
第一次 search 失败
→ alternative search provider

两次失败
→ browser agent

仍失败
→ ask user / human
```

所以：

```text
route_t
≠
route(query only)
```

而更像：

```text
route_t
=
route(query, state_t, history, failures, budget)
```

这也是为什么 Routing 属于 Agent Decision Core，而不是单纯前置分类器。

---

#### 2.7.33 Routing Stickiness 与 Oscillation

如果 Router 每轮都重新决定：

```text
Agent A
→ Agent B
→ Agent A
→ Agent B
```

可能出现 route oscillation。

因此某些系统需要：

```text
stickiness
```

即在没有强新证据时：

```text
保持当前 route
```

只有满足：

```text
failure
capability mismatch
new evidence
budget change
```

才 re-route。

这和 Planning 中的原则类似：

> **不要因为每一步都能重新决定，就每一步都推翻已有有效决策。**

---

#### 2.7.34 Re-routing Trigger

常见 trigger：

```text
Route failed
Verifier FAIL
Repeated no-progress
Tool unavailable
Budget exhausted
Latency SLA threatened
Risk level increases
New modality appears
Capability requirement changes
User constraint changes
```

成熟 Router 不只是：

```text
initial selection
```

而是支持：

```text
route
→ observe
→ decide whether reroute
```

形成 feedback loop。

---

#### 2.7.35 Routing 与 Verification 的关系

Router 需要知道：

```text
哪条 route 成功了？
```

而这个信号往往来自 Verification。

例如：

```text
cheap_model
↓
verifier PASS
→ accept

verifier FAIL
→ route strong_model
```

因此：

```text
Router
→ allocates path

Verifier
→ evaluates route outcome
```

两者组合就形成：

```text
adaptive compute allocation
```

这也是 model cascade 和 escalation system 的核心。

---

#### 2.7.36 Routing 与 Budget 的关系

Routing 常常是在做预算分配。

例如：

```text
Budget Remaining = $0.02
```

可能不允许：

```text
strong_model + 3 verifiers + 2 subagents
```

所以 Router 应该看到：

```text
remaining tokens
remaining calls
remaining cost
remaining time
```

然后选择：

```text
best feasible route under budget
```

因此：

> **Routing 是 Budget Policy 进入具体执行路径的一个主要落点。**

---

#### 2.7.37 Routing 与 Risk 的关系

不同 route 的风险不同。

例如：

```text
read-only agent
vs
write-capable agent
```

如果 Task 只需要查询：

```text
应该 route 到最小权限能力
```

而不是：

```text
默认使用拥有删除 / 发送 / 修改权限的 Agent
```

所以 Router 也应遵循：

```text
Least Privilege
```

可以把风险约束写成：

```text
Capability Match
AND
Permission Minimality
```

这会在 Safety 与 Harness 章节展开。

---

#### 2.7.38 Route Description 为什么重要？

如果使用模型型 Router，它依赖候选 route 的描述。

例如：

```text
Agent A:
“用于各种任务”
```

非常模糊。

更好的描述：

```text
Research Agent:
- current external information
- source retrieval
- citation collection
- read-only
- no code execution
```

Router 才能正确判断：

```text
capability match
```

所以 Route Description 与 Tool Description 类似：

> **它是 Router 的 decision surface。**

描述错误会直接导致 routing error。

---

#### 2.7.39 Router 自己也可能成为瓶颈

如果每个请求都要：

```text
先调用一个昂贵 LLM 做 routing
再调用真正 executor
```

那么简单任务可能：

```text
routing cost > execution cost
```

因此需要考虑：

```text
Router Overhead
```

包括：

```text
tokens
latency
model call
failure probability
```

一个好的 Router 不只是提高 downstream quality，还应该：

```text
net utility > routing overhead
```

所以对简单、稳定路由：

```text
rule / lightweight classifier
```

可能比大模型更合理。

---

#### 2.7.40 Routing Failure Modes

**1. Capability Mismatch**

把任务交给不具备所需能力的路径。

**2. Over-routing**

简单任务被升级到昂贵 Agent / Model。

**3. Under-routing**

困难任务留在弱路径，导致失败。

**4. Route Hallucination**

模型选择不存在的 tool / agent / workflow。

**5. Permission-blind Routing**

选择当前没有权限的路径。

**6. Availability-blind Routing**

选择离线 / unhealthy capability。

**7. Cost-blind Routing**

忽视 budget，长期全部走最贵路径。

**8. Risk-blind Routing**

把低风险查询交给高权限执行路径。

**9. Routing Oscillation**

Agent 在多个 route 间来回切换。

**10. Sticky Wrong Route**

初始 route 错误后，系统又过度 stick，不愿 reroute。

**11. Upstream Router Error Propagation**

Hierarchical Router 上层分类错，下层无法恢复。

**12. Ambiguous Route Descriptions**

多个能力描述高度重叠，Router 无法稳定区分。

**13. Router–Executor Contract Mismatch**

Router 认为 executor 支持某种输入 / 输出，但真实接口不支持。

**14. State-blind Routing**

只看原始 query，忽视已经失败过什么、预算还剩多少。

**15. Confidence Miscalibration**

错误把高置信当成高成功概率。

**16. Router Distribution Shift**

训练时任务分布和生产时不同。

**17. Feedback Loop Bias**

因为只观察被选 route 的结果，长期无法知道未选 route 是否更好。

**18. Routing Leakage**

Router 使用了 deployment 时不可获得的信息。

**19. Route Collapse**

学到的 Router 几乎总选同一路径，失去 adaptive value。

**20. Excessive Fragmentation**

能力拆得过细，Routing 本身变成主要复杂度来源。

---

#### 2.7.41 Routing 应该怎样 Evaluation？

不能只看：

```text
Routing Accuracy
```

因为一个 route 标签本身未必有唯一 Ground Truth。

更应该看：

```text
Task Success Rate
Expected Utility
Cost per Successful Task
Latency
Risk Violation Rate
Escalation Rate
Fallback Rate
Wrong-route Recovery Rate
Router Overhead
Route Distribution
Calibration
Stability
```

如果有 oracle，可以看：

```text
Regret
```

概念上：

$$
Regret
=
U(r^*)-U(\hat r)
$$

其中：

```text
r* = hindsight best route
r_hat = router selected route
```

这比单纯问“route label 是否和人工一样”更贴近系统价值。

---

#### 2.7.42 Oracle Routing 与现实 Routing

离线分析时，可以把多个 route 全部跑一遍：

```text
A outcome
B outcome
C outcome
```

然后得到：

```text
oracle best route
```

但生产环境通常只能执行一个或少数几个 route。

因此有一个重要差异：

```text
Full-information offline evaluation
≠
Partial-feedback online routing
```

这意味着 Router 的训练和评估要注意：

```text
selection bias
counterfactual outcome unavailable
```

这也是为什么 routing 与 contextual bandit / online decision 问题存在天然联系。

---

#### 2.7.43 Routing Data 为什么有价值？

高质量 routing trajectory 可以记录：

```text
Task
State
Candidate Routes
Available Capabilities
Constraints
Budget
Selected Route
Reason Code
Route Outcome
Verifier Verdict
Fallback / Reroute
Final Outcome
Cost / Latency
```

这类数据可以研究：

```text
capability matching
hard-case escalation
cost-quality trade-off
router calibration
fallback policy
route collapse
routing drift
```

尤其有价值的是 counterfactual / paired 数据：

```text
同一个 task
Route A → fail
Route B → success
```

因为它直接提供：

```text
routing preference signal
```

但现实里这种 paired outcome 往往成本较高。

---

#### 2.7.44 Router 是否应该自己解释理由？

需要区分：

```text
Decision Explanation
```

和：

```text
真实决策机制
```

让 Router 输出：

```json
{
  "route": "strong_model",
  "reason_code": "high_reasoning_complexity"
}
```

对调试很有价值。

但不要自动认为自然语言 explanation 就是忠实 causal explanation。

工程上更可靠的是保存：

```text
input features
candidate routes
policy version
scores
constraints
selected route
outcome
```

这样才能真正审计 Routing。

---

#### 2.7.45 Routing 在 Agent 架构中的位置

可以把目前的决策层画成：

```text
Goal / State
    ↓
Planning
→ 需要完成哪些 Subgoals？
    ↓
Routing
→ 当前 Subgoal 交给哪种 Capability / Path？
    ↓
ReAct / Local Policy
→ 当前 Observation 下下一步具体做什么？
    ↓
Action
    ↓
Environment
    ↓
Observation
    ↓
Verification
    ↓
Reflection / Replan / Reroute
```

这里最重要的是：

> **Routing 不替代 Planning，也不替代 Agent Loop；它负责在这些控制结构中选择合适的执行路径。**

---

#### 2.7.46 一个 Research Agent Routing 示例

用户：

```text
比较三家公司的最新季度收入，并计算同比增长。
```

系统拥有：

```text
General LLM
Web Search Agent
Company Filing Tool
Calculator
Human Review
```

Routing 可以分层：

```text
Task requires current factual data
↓
route away from pure parametric answer
↓
Company Filing Tool / Web Research
```

获取收入后：

```text
numeric computation
↓
Calculator
```

如果某家公司没有公开 filing：

```text
primary source unavailable
↓
route to Web Research
```

如果来源冲突：

```text
verifier uncertain
↓
route to stronger research / human review
```

这里不是一次路由，而是：

```text
Capability Routing
→ Tool Routing
→ Fallback Routing
→ Verification-driven Rerouting
```

---

#### 2.7.47 一个 Coding Agent Routing 示例

任务：

```text
修复 repository 中一个 failing test。
```

系统可能有：

```text
Fast Code Model
Strong Reasoning Model
Search Tool
Shell Runtime
Human Approval
```

初始：

```text
simple localized failure
→ Fast Code Model
```

如果：

```text
两轮 patch 均失败
```

Router 可以：

```text
escalate → Strong Reasoning Model
```

如果需要外部最新 API 文档：

```text
route → Search Tool
```

如果 repair 需要：

```text
modify CI secrets / production deploy
```

则：

```text
route → Human Approval
```

所以一个成熟 Coding Agent 的 routing policy 不是：

```text
永远用最强模型
```

而是：

```text
local cheap path
→ verify
→ escalate only when needed
```

---

#### 2.7.48 Routing 与 Multi-Agent 的关系

Multi-Agent 系统一定会遇到 Routing，但：

```text
Routing
≠
Multi-Agent
```

因为单 Agent 系统也可以：

```text
route models
route tools
route workflows
```

而 Multi-Agent 只是增加了：

```text
Agent 作为可选 route
```

后面第 6 章会讨论：

```text
Manager
Supervisor
Handoff
Agents-as-Tools
Parallel Workers
```

Routing 是其中一个基础原语。

---

#### 2.7.49 Routing 与 Harness 的关系

Router 是选择组件。

Harness 决定 Routing Policy，例如：

```text
什么时候 route？
候选 route 是哪些？
哪些 route 对当前任务可见？
预算怎么约束？
高风险 route 是否需要 approval？
失败几次以后 reroute？
什么时候升级 human？
```

因此：

```text
Router
= selection component

Routing Policy
= Harness control logic
```

这和前面：

```text
Verifier
vs
Verification Policy
```

完全同构。

---

#### 2.7.50 Routing 与 Runtime 的关系

Runtime 提供：

```text
route availability
health
latency
queue
execution environment
```

Router / Harness 使用这些信号决定：

```text
当前 route 是否 feasible
```

例如：

```text
GPU queue overloaded
```

可能让 Router 选择：

```text
slower-quality-equivalent CPU path
```

或者延迟执行。

所以：

```text
Runtime
→ exposes operational state

Routing Policy
→ uses state to choose execution path
```

---

#### 2.7.51 Routing 的工程原则

1. **先做 Feasibility Filtering，再做 Utility Optimization。**
2. **能用 deterministic rule 的硬边界，不必强行 LLM routing。**
3. **Router 看到的不只是 Query，还应看到 State、Budget、Risk、Availability。**
4. **Route Description 必须明确 Capability 与限制。**
5. **Confidence 必须校准，不要把模型自报分数当事实。**
6. **默认保留 fallback / escalation path。**
7. **避免无意义 route oscillation，必要时使用 stickiness。**
8. **Routing overhead 必须计入 cost / latency。**
9. **高风险任务遵守 least privilege，优先最小权限 route。**
10. **Router 失败后要允许 reroute，而不是一次错误锁死整条轨迹。**
11. **Routing evaluation 应看 downstream utility，不只看 route label accuracy。**
12. **记录 candidate set、policy version、route score、outcome，保证可审计。**
13. **Hierarchical Routing 要特别评估上层错误传播。**
14. **在可行时收集 paired / counterfactual routing data。**
15. **Routing Policy 属于 Harness；Router 只是实现该策略的一个组件。**

---

#### 2.7.52 与相邻概念的边界

| 概念 | 核心问题 | 与 Routing 的关系 |
|---|---|---|
| Routing | 当前任务 / 状态应该走哪条路径？ | 选择 Model / Tool / Agent / Workflow / Escalation |
| Tool Selection | 当前 Action 用哪个 Tool？ | Routing 的一个特例 |
| Planning | 未来若干步怎样组织？ | 产生 Subgoal / dependency；Routing 可为每个 step 选 executor |
| ReAct | 当前 Observation 下下一步做什么？ | Routing 可作为 ReAct decision 的一部分 |
| Orchestrator | 整个多组件执行如何组织？ | Router 通常是 Orchestration 的一个组件 |
| Supervisor | 怎样持续监控并重新分配任务？ | 可反复调用 Router，但职责更宽 |
| Handoff | 怎样把控制权转交另一个 Agent？ | Routing 决定交给谁；Handoff 执行转交 |
| Dispatcher | 怎样把已决定的任务发送给执行者？ | Router 决定目的地，Dispatcher 发送 |
| Load Balancer | 等价实例之间如何分流？ | 偏基础设施负载；Routing 偏语义 / capability |
| Cascade | 是否逐级升级到更强路径？ | 一种 staged Routing Pattern |
| Verification | 当前 route 结果是否成功？ | 提供 reroute / escalation feedback |
| Harness | Routing Policy 如何制定？ | 决定 candidate、trigger、fallback、budget、risk |
| Runtime | 当前 route 是否可用？ | 提供 health / capacity / execution state |

---

#### 2.7.53 面试掌握边界

至少应该能够稳定回答：

1. **Routing 是什么？**  
   根据 Task、State、Capability、Constraint、Cost、Risk 和 Availability，在多个可执行路径中选择最合适路径的决策机制。

2. **Routing 只等于 Intent Classification 吗？**  
   不等于。成熟 Routing 是 state-dependent capability selection，可以考虑预算、风险、历史失败与运行状态。

3. **Routing 有哪些类型？**  
   Model、Tool / Capability、Agent / Subagent、Workflow、Escalation / Fallback Routing。

4. **Model Routing 为什么有价值？**  
   不同任务需要不同能力，可以在质量、成本与延迟之间做条件计算分配，而不是所有请求都用最强模型。

5. **Routing 和 Planning 区别？**  
   Planning 组织未来步骤与依赖；Routing 决定当前 Task / Step 由哪条能力路径执行。

6. **Router 和 Orchestrator 区别？**  
   Router 主要做 route selection；Orchestrator 负责更完整的 sequence、parallel、merge、retry、cancel 等执行组织。

7. **Router 和 Supervisor 区别？**  
   Router 可以是一次选择函数；Supervisor 是持续观察、分配、检查和重分配的控制角色。

8. **Routing 和 Handoff 区别？**  
   Routing 决定交给谁；Handoff 真正转移控制权、Context 与 State。

9. **Router 和 Load Balancer 区别？**  
   Router 选择语义能力 / 模型 / 路径；Load Balancer 在同类实例间根据 capacity / health 分流。

10. **什么是 Cascade？**  
    先走便宜 / 快速路径，结果不足时逐级升级，是 Routing 的一种 staged pattern。

11. **为什么 Router 需要看到 Budget？**  
    因为 route 本身就是 compute allocation；可选路径必须在剩余 cost / latency / call budget 下可执行。

12. **Confidence-based Routing 最大问题是什么？**  
    confidence 可能未校准；必须验证它是否真正预测 route success，而不是只相信模型自报。

13. **为什么 Routing 需要 fallback？**  
    初始 route 可能错误、不可用或失败，系统需要在新 Observation 下 reroute，而不是一次选择锁死任务。

14. **怎样评估 Router？**  
    看 task success、utility、cost、latency、risk、escalation、recovery、calibration、regret 和 routing overhead，而不只看 label accuracy。

15. **Routing 最核心的一句话是什么？**  
    Routing 不是给输入贴一个标签，而是在真实 State、Capability、Budget 与 Risk 约束下，把有限计算和执行权限分配给最合适的路径，并允许结果反馈触发 reroute。

如果继续追问“什么时候应该使用固定 Workflow，什么时候应该让 Agent 自主决定控制流，两者能否混合”，进入下一节 **2.8 Agent vs Workflow**。

---

#### 2.7.54 本节一句话总结

> **Routing 的本质，是在多模型、多工具、多 Agent、多 Workflow 的异构能力空间里做受约束的条件计算分配：先过滤不可执行的路径，再综合质量、成本、延迟、风险与可用性选择最合适 Route，并通过 Verification、失败反馈与 Budget 状态持续决定是否保持、升级、降级或重新路由；因此 Router 是选择组件，而 Routing Policy 属于更高层的 Harness 控制逻辑。**

#### 2.7.55 参考资料

- Chen L, Zaharia M, Zou J. **FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance**. arXiv:2305.05176, 2023. 从 LLM cascade 与成本—质量权衡角度理解模型路由。
- Ong I, Almahairi A, Wu V, et al. **RouteLLM: Learning to Route LLMs with Preference Data**. arXiv:2406.18665, 2024. 代表性研究之一：根据请求在强、弱模型之间学习动态路由，并显式考虑质量—成本权衡。
- Mohammadshahi A, Shaikh A R, Yazdani M. **Routoo: Learning to Route to Large Language Models Effectively**. arXiv:2401.13979, 2024. 通过 performance prediction 与 cost-aware selection 研究多模型路由。
- Fedus W, Zoph B, Shazeer N. **Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity**. Journal of Machine Learning Research, 23(120):1–39, 2022. 虽然讨论的是模型内部 Mixture-of-Experts routing，但对“conditional computation”这一更一般思想很有启发。
