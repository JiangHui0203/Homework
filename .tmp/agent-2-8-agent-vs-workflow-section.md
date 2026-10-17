### 2.8 Agent vs Workflow

#### 2.8.1 为什么这一节要放在 Decision Core 的最后？

前面的内容已经回答了：

```text
Agent 是什么？
怎样形成 Agent Loop？
怎样 Reason → Act → Observe？
怎样 Planning？
怎样 Reflection？
怎样 Verification？
怎样 Routing？
```

但真正做系统设计时，还剩下一个比“怎么做 Agent”更重要的问题：

> **这个问题到底需不需要 Agent？**

很多失败的 Agent 项目并不是模型能力不够，而是：

```text
原本可以确定性解决的部分
↓
被不必要地交给模型动态决策
↓
引入随机性、成本、延迟和新的 failure surface
```

反过来，也有任务本身高度开放、不确定，却被硬塞进固定 Workflow，结果变成：

```text
规则越来越多
分支越来越复杂
边界 case 越来越脆
```

所以本节真正回答的是：

> **哪些控制决策应该在开发阶段固定，哪些应该在运行时交给 Agent Policy？**

这也是第一层 Model & Decision Core 的自然收束。

---

#### 2.8.2 Workflow 到底是什么？

Workflow 可以定义为：

> **由开发者预先定义主要控制结构、状态转移和执行边界，并由系统按照这些规则推进任务的过程。**

最简单的 Workflow：

```text
Input
  ↓
Step A
  ↓
Step B
  ↓
Step C
  ↓
Output
```

也可以有条件分支：

```text
Input
  ↓
Validate
  ↓
if valid ─────→ Execute
if invalid ───→ Ask User
```

还可以有：

```text
parallel branches
retry
queue
approval gate
fallback
compensation
state machine
DAG
```

因此：

> **Workflow 不等于“只能线性执行的脚本”。**

它可以非常复杂。

真正关键的是：

> **主要可选路径及其切换规则，通常在开发时已经被显式定义。**

---

#### 2.8.3 Agent 与 Workflow 的核心差异：Control-flow Ownership

最重要的分界不是：

```text
有没有 LLM？
有没有 Tool？
有没有多个 Step？
```

而是：

> **运行时下一步控制流由谁决定？**

Workflow：

```text
Developer-defined control graph
        ↓
Runtime follows graph / rules
```

Agent：

```text
Goal + State + Observation
        ↓
Policy decides next Action at runtime
        ↓
Control path emerges dynamically
```

因此可以记成：

```text
Workflow
= control structure mainly specified before runtime

Agent
= part of control structure selected dynamically by Policy at runtime
```

这条边界比“LLM vs 非 LLM”准确得多。

---

#### 2.8.4 用形式化方式看：Fixed Transition vs Policy-selected Transition

Workflow 可以近似写成：

$$
s_{t+1}=F(s_t,e_t)
$$

其中：

- $F$：开发者预定义的 transition logic；
- $e_t$：当前事件 / 条件。

Agent 更接近：

$$
a_t \sim \pi(a\mid s_t,g,o_t)
$$

然后：

$$
s_{t+1}=T(s_t,a_t,o_{t+1})
$$

也就是说：

```text
Workflow
→ transition rule owns control

Agent
→ policy chooses action, action induces transition
```

当然真实系统通常是两者组合，而不是纯粹二选一。

---

#### 2.8.5 “用了 LLM”不等于 Agent

假设一个系统：

```text
用户输入
↓
LLM 做分类
↓
固定模板生成摘要
↓
存数据库
```

即使中间调用了 LLM：

```text
control flow 仍完全固定
```

它仍然更像：

```text
LLM-powered Workflow
```

而不是自主 Agent。

所以：

> **LLM 可以只是 Workflow 中的一个 probabilistic function。**

例如：

```text
extract_fields()
classify_intent()
summarize_document()
generate_draft()
```

只要这些节点的位置、调用顺序和后续逻辑由系统预先定义，就没有必要因为用了 LLM 就把整个系统称为 Agent。

---

#### 2.8.6 “有 Tool Calling”也不等于 Agent

例如：

```text
Step 1:
模型必须调用 extract_invoice()

Step 2:
系统固定调用 validate_invoice()

Step 3:
系统固定写入 ERP
```

这里模型虽然产生 Tool Arguments，但：

```text
可调用什么 Tool
什么时候调用
调用后去哪一步
```

都已经固定。

所以它仍然可能主要是：

```text
Workflow + LLM Tool Interface
```

真正 Agentic 的地方在于：

```text
模型 / Policy 能根据新 Observation
动态决定下一步 Action / Route / Termination
```

---

#### 2.8.7 Workflow 也可以有动态条件分支

另一个误区是：

```text
有 if / branch
→ 就是 Agent
```

不是。

例如：

```python
if amount < 1000:
    auto_approve()
else:
    request_manager_approval()
```

虽然运行时走哪条分支取决于数据，但：

```text
branch set
branch condition
branch destination
```

都由开发者预定义。

所以这是典型 Workflow。

因此：

> **Dynamic execution 不等于 dynamic control-policy generation。**

---

#### 2.8.8 Agent 也不是“完全自由”

反过来，Agent 也不应该被理解成：

```text
模型想做什么就做什么
```

成熟 Agent 往往有严格 Envelope：

```text
Allowed Tools
Permissions
Budget
Max Steps
Sandbox
Approval Gates
Success Criteria
Termination Rules
```

所以真实结构更像：

```text
Workflow / Harness defines safe envelope
            ↓
Agent chooses inside the envelope
```

因此：

> **Agentic autonomy 应该是 bounded autonomy，而不是 unrestricted autonomy。**

---

#### 2.8.9 Agenticness 是连续谱，不是二元标签

很多系统很难简单归成：

```text
Workflow
or
Agent
```

更准确的是一个连续谱：

```text
完全固定脚本
  ↓
条件 Workflow
  ↓
Workflow + LLM nodes
  ↓
Workflow + Router
  ↓
Workflow + Agentic node
  ↓
Agent with bounded tools
  ↓
Long-horizon autonomous Agent
```

Agenticness 增加意味着：

```text
更多运行时路径由 Policy 决定
```

同时通常也意味着：

```text
更高 flexibility
+
更高 uncertainty
+
更高 evaluation complexity
+
更大 failure surface
```

所以 Agenticness 本身不是优化目标。

---

#### 2.8.10 Autonomy Budget：自主性也是一种预算

前面已经讲了：

```text
Token Budget
Tool-call Budget
Latency Budget
Cost Budget
```

还可以再引入一个系统设计直觉：

```text
Autonomy Budget
```

意思是：

> **只有真正需要动态判断的地方，才把控制权交给模型。**

例如：

```text
确定性数据校验
→ 不需要 Agent

开放信息检索策略
→ 适合 Agent

高风险转账执行
→ 不应该完全交给 Agent
```

因此一个成熟系统不是最大化：

```text
autonomy
```

而是：

```text
allocate autonomy where it creates value
```

---

#### 2.8.11 什么时候 Workflow 更合适？

Workflow 通常更适合以下情况。

##### 1. Control Flow 稳定

任务步骤长期不变：

```text
上传
→ 校验
→ 转换
→ 存储
```

##### 2. Success Criteria 明确

可以程序化判断：

```text
schema valid
payment settled
file uploaded
```

##### 3. 高风险 / 强合规

例如：

```text
资金
权限
生产部署
外部通信
隐私数据
```

##### 4. 高频大规模

每次多一个模型调用都会显著增加成本。

##### 5. 需要高可复现性

相同输入希望得到高度一致的执行路径。

##### 6. 边界可以写成 deterministic rule

如果规则已经清晰，就没有必要付出 Agent 决策成本。

---

#### 2.8.12 什么时候 Agent 更合适？

Agent 更适合：

##### 1. Path 不能预先穷举

例如：

```text
研究一个开放问题
调试未知 bug
在陌生网站完成任务
```

##### 2. Observation 会显著改变下一步

```text
search result
error log
web state
user reply
```

不断改变策略。

##### 3. 需要信息获取决策

Agent 要自己决定：

```text
缺什么信息？
去哪找？
什么时候够了？
```

##### 4. 输入分布开放

无法用少量规则覆盖全部 case。

##### 5. 需要运行时 Planning / Replanning

任务路径依赖真实 Environment。

所以：

> **Agent 的核心价值来自 runtime uncertainty，而不是来自“看起来更智能”。**

---

#### 2.8.13 一个实用判断：Uncertainty × Consequence

可以用两个维度帮助选择架构：

```text
                Consequence
              Low          High
Uncertainty
Low        Workflow     Workflow + strict guards

High       Agent        Bounded Agent + approval + verification
```

解释：

- **低不确定 + 低风险**：直接 Workflow。
- **低不确定 + 高风险**：更应该确定性，不是更 Agentic。
- **高不确定 + 低风险**：Agent 很适合探索。
- **高不确定 + 高风险**：可以让 Agent 做判断，但真正 Action 必须有更强的 guard / approval / verifier。

这比一句“复杂任务用 Agent”更准确。

---

#### 2.8.14 Hybrid Architecture：现实系统最常见的形态

真实高可靠系统通常是：

```text
Workflow Backbone
      ↓
Agentic Decision Node
      ↓
Deterministic Execution
      ↓
Verifier
      ↓
Workflow continues
```

例如：

```text
Receive Ticket
↓
Deterministic validation
↓
Agent decides category + needed investigation
↓
Fixed permission check
↓
Agent gathers evidence
↓
Deterministic policy engine
↓
Human approval if needed
↓
Fixed execution workflow
↓
Postcondition verification
```

这通常比：

```text
“给 Agent 所有工具，让它自己想办法”
```

更可靠。

所以一个极其重要的工程原则是：

> **Workflow 控制高确定性、高风险边界；Agent 处理高不确定性、语义判断和开放探索。**

---

#### 2.8.15 Workflow Backbone + Agentic Nodes

可以把 Hybrid System 理解为：

```text
┌────────────────────────────┐
│      Deterministic Flow    │
│                            │
│ Validate                   │
│   ↓                        │
│ [Agentic Decision Node]    │
│   ↓                        │
│ Permission Check           │
│   ↓                        │
│ Execute                    │
│   ↓                        │
│ Verify                     │
└────────────────────────────┘
```

Agentic Node 可以负责：

```text
classification
routing
planning
research
exception handling
semantic interpretation
```

但：

```text
权限
不可逆执行
关键 invariant
最终 completion check
```

仍可以留给确定性系统。

---

#### 2.8.16 Agent 也可以把 Workflow 当作 Tool

组合关系也可以反过来：

```text
Agent
  ↓
choose workflow
  ↓
run_invoice_processing_workflow(...)
```

这里 Workflow 变成一个高层 Tool。

优点是：

```text
Agent 不需要逐步控制每一个低层动作
```

例如：

```text
book_travel_workflow()
run_release_pipeline()
process_refund_workflow()
```

都可以封装成 deterministic capability。

这体现一个重要思想：

> **把稳定子过程压缩成可靠 Tool，把不确定决策留给 Agent。**

---

#### 2.8.17 Workflow 也可以调用 Agent

另一种方向：

```text
Workflow Step 4
↓
Call Research Agent
↓
Agent returns structured result
↓
Workflow Step 5
```

此时 Agent 只是整个业务流程中的一个动态节点。

所以：

```text
Agent contains Workflow
```

和：

```text
Workflow contains Agent
```

都很常见。

不要把两者理解成互斥架构。

---

#### 2.8.18 Agent vs Workflow 与 Planning 的区别

Planning 解决：

```text
未来步骤怎样组织？
```

Workflow 解决：

```text
哪些步骤和控制结构已经由系统预先规定？
```

Agent 可以动态 Planning：

```text
Goal
↓
Plan generated at runtime
```

Workflow 则通常：

```text
Control graph defined at development time
```

但 Workflow 中也可以有：

```text
predefined planner node
```

所以：

> **Planning 是生成 /维护未来行动结构的能力；Workflow 是承载执行控制结构的一种系统形态。**

---

#### 2.8.19 Agent vs Workflow 与 Routing 的关系

Workflow 可以包含 Router：

```text
Input
↓
Router
├── Flow A
├── Flow B
└── Agent
```

Agent 也可以在运行时 Routing：

```text
State
↓
route to tool / model / subagent
```

所以 Routing 不决定系统是不是 Agent。

关键仍然是：

> **Route Policy 的自由度和后续路径是否主要在运行时动态决定。**

---

#### 2.8.20 Agent vs Workflow 与 Harness 的关系

Harness 可以同时控制：

```text
Workflow execution
Agent loop
Routing
Tool policy
Memory policy
Permissions
Verification
Recovery
```

因此 Harness 不是 Agent 的同义词。

更准确：

```text
Harness
= system control layer

Agent
= dynamic decision component / loop

Workflow
= explicit control-flow structure
```

一个 Harness 完全可以运行：

```text
80% deterministic workflow
+
20% agentic decision
```

---

#### 2.8.21 Workflow 的确定性不是绝对的

即使 control flow 固定，节点本身仍可能是随机的。

例如：

```text
Step 1: LLM summarize
Step 2: LLM classify
Step 3: Save
```

Graph 固定，但节点 output 仍可能 stochastic。

因此要区分：

```text
Control-flow Determinism
vs
Node-level Determinism
```

系统可能：

```text
control flow deterministic
node output probabilistic
```

也可能：

```text
control flow dynamic
but some actions deterministic
```

这是理解 Hybrid 系统时非常重要的两个轴。

---

#### 2.8.22 Agent 的动态性也不是无限的

Agent 一般仍然处在一个有限 Action Space：

```text
search
read
edit
run_test
ask_user
finish
```

Harness 还会进一步限制：

```text
which tools visible
which parameters allowed
which files writable
which domains reachable
```

所以更准确地说：

> **Agent 是在预定义 Action Envelope 内进行 runtime control selection。**

这和“完全任意控制流”不同。

---

#### 2.8.23 从 Control Theory 看：Workflow 更像 Open-loop / State Machine，Agent 更像 Feedback Policy

这只是帮助理解的类比，不是严格等价。

Workflow 常见形态：

```text
Known transition rules
↓
Follow state machine
```

Agent 更强调：

```text
Observe current Environment
↓
Policy chooses next Action
↓
Observe again
↓
adapt
```

所以 Agent 特别适合：

```text
环境不确定
反馈丰富
路径难提前确定
```

但如果环境稳定、规则明确：

```text
复杂 feedback policy
```

可能只是增加不必要的复杂度。

---

#### 2.8.24 Workflow 的优势：可预测性与可证明边界

Workflow 的核心优势包括：

```text
可解释 control flow
可枚举 path
容易做 permission review
容易做 audit
容易做 regression test
容易估算 cost / latency
容易证明 invariant
```

特别是在：

```text
金融
审批
生产系统
企业流程
安全敏感操作
```

这些优势非常重要。

因此：

> **“更确定”在很多产品里是一种能力，不是缺点。**

---

#### 2.8.25 Agent 的优势：处理未建模的变化

Workflow 的最大问题是：

```text
你必须提前想到可能发生什么
```

而 Agent 的优势在于：

```text
遇到新 Observation
↓
重新解释
↓
选择新 Action
```

所以 Agent 擅长：

```text
未知错误
开放检索
语义模糊
复杂用户目标
非结构化环境
```

可以理解为：

> **Workflow 把知识编码进 control graph；Agent 把一部分决策推迟到 runtime。**

---

#### 2.8.26 复杂度应该放在哪里？

系统设计的本质之一是决定：

```text
Complexity at design time
vs
Complexity at runtime
```

Workflow：

```text
开发者提前处理更多复杂度
→ runtime 更稳定
```

Agent：

```text
开发者把更多 decision freedom 留到 runtime
→ runtime 更灵活
```

没有免费的灵活性。

把复杂度从规则移给 Agent 后，通常会增加：

```text
evaluation
observability
recovery
verification
permission design
```

的要求。

---

#### 2.8.27 Agenticness 的成本曲线

随着 Agenticness 增加，通常：

```text
Flexibility ↑
Coverage of open-ended cases ↑
```

但同时：

```text
Variance ↑
Token Cost ↑
Latency ↑
Trajectory Length ↑
Debugging Difficulty ↑
Security Surface ↑
Evaluation Cost ↑
```

所以：

> **Agenticness 必须用增量 utility 来证明，而不能靠架构时髦程度证明。**

---

#### 2.8.28 High-risk Action 为什么应该更 Workflow-like？

假设 Agent 可以：

```text
删除文件
发送邮件
转账
上线部署
```

即使前面的 reasoning 很 Agentic，真正执行阶段也应该逐渐变得确定：

```text
Agent proposes
↓
Schema validation
↓
Policy check
↓
Permission check
↓
Human approval if required
↓
Deterministic execution
↓
Postcondition verification
```

所以：

> **越接近不可逆副作用，控制流通常越应该从开放 Agent 决策收紧到明确 Workflow / Policy。**

---

#### 2.8.29 Information Action 与 World-changing Action 可以采用不同 Agenticness

前面 ReAct 中区分了：

```text
Epistemic Action
vs
World-changing Action
```

这在架构选择里非常有用。

例如：

```text
search / read / inspect
→ 可以高度 Agentic
```

因为失败通常可恢复。

而：

```text
send / delete / purchase / deploy
→ 更 Workflow-like
```

因为错误代价更高。

因此可以设计：

```text
Agent explores freely
↓
Agent proposes final action
↓
Workflow validates and executes
```

这是一种非常实用的 Hybrid Pattern。

---

#### 2.8.30 Exception Handling：Agent 最适合成为 Workflow 的“异常处理器”之一

稳定流程可能覆盖 90% case：

```text
happy path
```

剩下 10%：

```text
missing field
unexpected document
ambiguous intent
external error
```

如果为每个 exception 增加规则：

```text
if / else 爆炸
```

可以考虑：

```text
Workflow
↓
Exception detected
↓
Agent investigates / proposes repair
↓
Verifier
↓
Return to Workflow
```

因此 Agent 的一个高价值位置是：

> **处理 deterministic system 无法经济枚举的 exception frontier。**

---

#### 2.8.31 Escalation Pattern：先 Workflow，必要时 Agent

一种常见设计：

```text
cheap deterministic path
↓
if sufficient → finish
↓
otherwise
↓
Agent path
```

例如：

```text
FAQ exact match
→ deterministic answer

No match
→ retrieval

Still ambiguous
→ Research Agent
```

这和上一节 Routing / Cascade 自然衔接。

它的核心价值是：

```text
只为难例支付 Agent 成本
```

而不是所有 case 都走最复杂路径。

---

#### 2.8.32 De-escalation Pattern：Agent 也应该能回到 Workflow

Agent 并不需要一直 Agentic 到任务结束。

例如：

```text
Agent investigates
↓
identifies known case type
↓
route to deterministic workflow
```

比如 Coding Agent：

```text
Agent 发现问题只是 formatter failure
↓
run fixed formatting workflow
↓
re-test
```

所以系统可以：

```text
Workflow → Agent → Workflow
```

而不是一旦进入 Agent 就永远由模型控制。

---

#### 2.8.33 Workflow State 与 Agent State 的差异

Workflow State 通常比较结构化：

```text
current_node
completed_steps
business_fields
approval_status
retry_count
```

Agent State 还可能包含：

```text
working hypotheses
plan
retrieved evidence
uncertainty
open questions
trajectory summary
```

Hybrid 系统需要明确：

> **哪些 State 属于业务事实，哪些只是 Agent 的内部工作状态。**

不能把：

```text
Agent hypothesis
```

误当成：

```text
Workflow business truth
```

---

#### 2.8.34 Workflow Invariant 应该高于 Agent Proposal

例如系统 invariant：

```text
不得修改 public API
不得未经审批转账
不得访问 restricted dataset
```

Agent 即使提出：

```text
为了完成任务，我建议暂时绕过限制
```

Workflow / Harness 也必须拒绝。

所以：

```text
Agent proposal
<
System invariant
```

这是安全系统必须保持的优先级。

---

#### 2.8.35 可恢复性：Workflow 和 Agent 的 Recovery 机制不同

Workflow 通常可以明确设计：

```text
retry
rollback
compensating action
resume from checkpoint
```

因为执行路径相对已知。

Agent Recovery 更难，因为：

```text
错误可能来自 decision policy
state interpretation
planning
observation grounding
```

所以 Agent 更依赖：

```text
trajectory
checkpoint
reflection
verification
rerouting
```

这也是 Agent System 比普通 Workflow 需要更多 observability 的原因。

---

#### 2.8.36 可测试性：Workflow Test 与 Agent Eval 不一样

Workflow 可以大量使用：

```text
unit test
path coverage
branch coverage
state transition test
invariant test
```

因为路径集合相对明确。

Agent 则还需要：

```text
trajectory evaluation
multi-run success rate
failure taxonomy
cost distribution
right-action rate
recovery rate
termination quality
```

所以：

```text
Workflow testing
≈ known-path correctness

Agent evaluation
≈ policy quality under state distribution
```

两者都需要，但方法不同。

---

#### 2.8.37 可复现性：不要把随机性引入没有价值的地方

如果某一步：

```text
parse ISO date
```

用 deterministic parser 就能稳定完成，没必要让 LLM 每次重新解释。

如果某一步：

```text
分析陌生错误日志并决定调查方向
```

Agent reasoning 可能更有价值。

因此：

> **把 stochasticity 留给语义不确定的决策，把 deterministic computation 留给确定性问题。**

这是 Hybrid Agent 设计非常重要的原则。

---

#### 2.8.38 Cost / Latency：Agentic Node 应该证明自己的边际收益

假设纯 Workflow：

```text
success = 91%
cost = 1
latency = 1s
```

加入 Agentic Node：

```text
success = 92%
cost = 8
latency = 6s
```

是否值得不能只看：

```text
+1% accuracy
```

还要看：

```text
case value
failure severity
volume
human savings
risk reduction
```

所以每个 Agentic Node 都应该回答：

> **它解决的 uncertainty 是否值得它引入的 cost / latency / variance？**

---

#### 2.8.39 Security：Agentic Control Flow 扩大攻击面

Workflow 的路径预定义，攻击者可操控空间较小。

Agent 会读取：

```text
web
email
files
tool output
```

这些 Observation 可能含有 prompt injection。

如果 Observation 可以改变：

```text
next action
next tool
next target
```

攻击面明显增大。

因此高安全系统常采用：

```text
Agent interprets data
↓
hard policy constrains actions
↓
workflow executes approved effects
```

也就是：

> **语义理解可以 Agentic，Authority 不应因此自动 Agentic。**

---

#### 2.8.40 Human-in-the-loop 在 Hybrid 系统中的位置

Human 不只是最后兜底。

可以作为：

```text
approval gate
ambiguity resolver
high-risk verifier
policy exception reviewer
```

典型：

```text
Agent proposes high-risk action
↓
Workflow detects approval required
↓
Human approves / rejects
↓
Deterministic execution
```

这样：

```text
Agent autonomy
```

和：

```text
real-world authority
```

仍然被分离。

---

#### 2.8.41 常见反模式 1：Everything is an Agent

典型系统：

```text
Agent 负责解析日期
Agent 负责拼 URL
Agent 负责判断状态码
Agent 负责决定是否存文件
Agent 负责校验 JSON
```

大量本来 deterministic 的工作都交给模型。

结果：

```text
成本高
延迟高
难测试
难复现
错误面变大
```

原则：

> **不要让 Agent 做普通程序已经能可靠做好的事。**

---

#### 2.8.42 常见反模式 2：Fake Agent

有些系统叫 Agent，但实际：

```text
固定 Step A
固定 Step B
固定 Step C
```

模型只填几个字段。

这不是坏事。

问题只是：

> **不要用“Agent”命名掩盖真实 control flow。**

正确理解架构比营销标签重要。

---

#### 2.8.43 常见反模式 3：Prompt 里藏 Workflow

例如 System Prompt 写：

```text
第一步必须搜索
第二步必须读取
第三步必须验证
第四步必须回答
```

实际上这是：

```text
用自然语言 Prompt 模拟 Workflow Engine
```

问题是：

```text
规则无法硬保证
状态难跟踪
异常处理脆弱
测试困难
```

如果控制逻辑非常确定，更好的做法通常是：

```text
把它写进 Harness / Workflow
```

而不是只写进 Prompt。

---

#### 2.8.44 常见反模式 4：固定 Workflow 硬扛开放世界

另一边也会过度 Workflow 化。

例如开放研究任务被写成：

```text
if source A missing → source B
if B missing → source C
if C says X → ...
```

随着 case 增加：

```text
rules explode
```

此时 Agent 可能更适合处理：

```text
search strategy
source selection
query reformulation
```

因此：

> **规则开始大量描述语义例外时，往往说明有一部分 control decision 应该升级为 Agentic。**

---

#### 2.8.45 常见反模式 5：Agent 负责 Safety，系统不做 Enforcement

例如 Prompt：

```text
不要删除重要文件。
```

然后仍然把：

```text
delete_file(path="/")
```

完整暴露给 Agent，没有权限限制。

这是把：

```text
policy preference
```

误当成：

```text
security boundary
```

正确结构应该是：

```text
Agent proposal
↓
Permission / Policy Engine
↓
Allowed / Denied
```

而不是要求 Agent 自己永远记得拒绝危险动作。

---

#### 2.8.46 一个实用的架构设计流程

面对一个新任务，不要第一步问：

```text
用哪个 Agent Framework？
```

更推荐：

##### Step 1：画出 Goal 和 Success Criteria

```text
什么状态才算完成？
```

##### Step 2：找出确定性子过程

```text
哪些可以 Rule / Code / Workflow 可靠完成？
```

##### Step 3：找出 Uncertainty Frontier

```text
哪些地方路径无法提前确定？
哪些地方需要语义判断？
哪些地方需要根据 Observation 自适应？
```

##### Step 4：只在这些位置增加 Agentic Decision

##### Step 5：把高风险 Action 放回硬 Policy / Workflow

##### Step 6：增加 Verification 和 Recovery

最终结构往往是：

```text
Deterministic Core
+
Targeted Agentic Decisions
+
Hard Safety Boundaries
+
Verification
```

而不是：

```text
One giant autonomous agent
```

---

#### 2.8.47 Uncertainty Frontier：最值得记住的设计概念

可以把系统里的步骤分成：

```text
Known / Deterministic Region
        ↓
Uncertainty Frontier
        ↓
Open-ended Region
```

例如 Coding：

```text
run tests
→ deterministic

interpret unfamiliar failure
→ uncertainty frontier

choose investigation / edit strategy
→ agentic

apply patch
→ deterministic tool execution

run tests again
→ deterministic verifier
```

所以 Agent 并不需要占满整个系统。

最有价值的位置常常只是：

> **传统程序最难经济编码、但模型可以根据上下文判断的边界。**

---

#### 2.8.48 Determinism Allocation：可靠 Agent 系统的核心能力之一

最终可以把架构设计理解成：

```text
Where should we spend determinism?
Where should we spend autonomy?
```

确定性应该优先用在：

```text
Safety
Permissions
Accounting
Schema
Business invariants
Irreversible execution
Verification
```

Agentic flexibility 优先用在：

```text
Interpretation
Planning
Research
Exploration
Exception handling
Recovery diagnosis
```

于是：

> **优秀的 Agent 系统不是 Agent 最多，而是 determinism 和 autonomy 分配得最合理。**

---

#### 2.8.49 Workflow 与 Agent 的 Failure Modes 对比

Workflow 常见失败：

```text
missing branch
wrong business rule
state-machine bug
retry storm
integration failure
stale configuration
```

Agent 常见失败：

```text
goal drift
wrong action
observation ignored
planning failure
hallucinated state
premature termination
looping
```

Hybrid 系统还可能出现：

```text
Agent/Workflow state mismatch
wrong handoff
lost context
policy disagreement
agent output incompatible with workflow schema
```

因此 Hybrid 并不自动更简单。

它的价值是：

```text
把不同类型的问题交给更适合的控制机制
```

---

#### 2.8.50 Workflow 与 Agent 的 Observability 不同

Workflow Trace 常见：

```text
Node A started
Node A success
Branch B selected
Node C failed
```

Agent Trace 还需要：

```text
State
Selected Action
Observation
Plan revision
Tool arguments
Verifier result
Termination reason
```

Hybrid 系统最好能统一到一条 trace：

```text
Workflow Node
→ Agent Episode
→ Tool Calls
→ Verification
→ Workflow Resume
```

否则生产事故很难归因。

---

#### 2.8.51 Workflow 与 Agent 的 Evaluation 应联合看什么？

不能只问：

```text
Agent 回答得好不好？
```

应该看整个系统：

```text
Task Success
Constraint Compliance
Path / Route Quality
Unnecessary Agent Invocation Rate
Escalation Rate
Recovery Rate
Cost
Latency
Variance
Human Intervention
Safety Violations
```

特别值得看一个指标：

```text
Unnecessary Agent Rate
```

也就是：

> 本来 deterministic path 足够解决，却调用了昂贵 Agent 的比例。

另一个方向：

```text
Missed Agent Opportunity Rate
```

即：

> 固定 Workflow 已经明显无法解决，却没有及时升级 Agent 的比例。

这两者共同衡量 autonomy allocation 是否合理。

---

#### 2.8.52 如何比较 Workflow-only、Agent-only 和 Hybrid？

一个严谨实验可以设计三组：

```text
A. Workflow-only
B. Agent-only
C. Hybrid
```

统一比较：

```text
Success
Cost
Latency
Variance
Safety
Recovery
Human Escalation
```

常见结果并不是：

```text
Agent-only 全面最好
```

更可能是：

```text
Workflow-only
→ 稳定但 coverage 不够

Agent-only
→ coverage 高但 cost / variance 大

Hybrid
→ 在某个 Pareto frontier 上更优
```

所以架构选择本质上仍然是多目标 trade-off。

---

#### 2.8.53 一个 Research Agent 示例

任务：

```text
研究某公司是否已经发布最新财报，并总结核心变化。
```

可以设计：

```text
Workflow:
validate company identity
↓
check official investor-relations endpoint
↓
if latest report found
    deterministic parse metadata
else
    Agent searches broader web
↓
Agent reads / compares relevant evidence
↓
Verifier checks date + official source
↓
Workflow formats final output
```

这里：

```text
确定性的 identity / date / official-source checks
```

不需要交给 Agent 自由发挥。

而：

```text
开放检索与跨来源分析
```

适合 Agent。

---

#### 2.8.54 一个 Coding Agent 示例

任务：

```text
修复 bug，不改 public API。
```

可以设计：

```text
Workflow:
checkout clean branch
↓
run baseline tests
↓
Agent:
inspect failure
search code
plan repair
edit
↓
Workflow:
run tests
run API diff
run static checks
↓
if fail
    return evidence to Agent
else
    finish
```

这里最关键的不是：

```text
“使用 Coding Agent”
```

而是：

```text
开放诊断 / 修复
→ Agentic

测试 / invariant / completion
→ Deterministic
```

这正是 Hybrid 的典型形态。

---

#### 2.8.55 一个 Customer Support 示例

```text
User request
↓
Deterministic identity check
↓
Router
├── known FAQ → Workflow
├── simple refund → Refund Workflow
├── ambiguous case → Support Agent
└── high-risk dispute → Human
```

Support Agent 可以：

```text
理解复杂语义
收集缺失信息
解释政策
```

但实际退款动作仍通过：

```text
Refund Workflow
```

完成。

所以：

> **Agent 可以决定“应该做什么”，Workflow 可以负责“安全可靠地把它做掉”。**

---

#### 2.8.56 Agent vs Workflow 的工程设计原则

1. **先 Workflow，后 Agenticness。** 先写出能确定性解决的部分。
2. **把 Agent 放在 Uncertainty Frontier。** 不要把模型撒满整条链。
3. **控制流归属比“有没有 LLM”更重要。**
4. **高风险越靠近 Execution，越应该确定性。**
5. **Agent Proposal 与 System Authority 分离。**
6. **稳定子过程封装成 Tool / Workflow。**
7. **Agent 允许进入，也必须允许退出。** 支持 escalation / de-escalation。
8. **Workflow Invariant 高于 Agent Suggestion。**
9. **Agentic Node 必须证明增量 utility。**
10. **Hybrid Trace 必须统一可观测。**
11. **测试方法分层。** Workflow 做 path/state tests；Agent 做 trajectory/distribution eval。
12. **不要把 Workflow 规则藏在 Prompt 里。** 硬规则写进 Harness / Policy。
13. **不要为了 Agent 而 Agent。** 架构目标是完成任务，不是最大化 autonomy。
14. **成功标准仍由 Verification 驱动。**
15. **最终优化目标是 Quality–Cost–Latency–Reliability–Risk 的 Pareto trade-off。**

---

#### 2.8.57 与相邻概念的边界

| 概念 | 核心问题 | 与 Agent / Workflow 的关系 |
|---|---|---|
| Workflow | 已知控制流怎样可靠执行？ | 主要路径与规则在开发时定义 |
| Agent | 当前 State 下下一步动态做什么？ | Policy 在运行时选择 Action |
| LLM Node | 某一步用模型做语义计算 | 可以存在于 Workflow，不自动变成 Agent |
| Tool Calling | 怎样表达 / 执行 Action？ | Agent 和 Workflow 都可使用 |
| Planning | 未来步骤怎样组织？ | Agent 可运行时规划；Workflow 通常预先定义较多结构 |
| Routing | 当前走哪个 Route？ | 可作为 Workflow Node，也可由 Agent 动态执行 |
| Orchestrator | 多组件怎样组织执行？ | 可编排 Workflow 与 Agent |
| Harness | 哪些 policy / context / tools / loop 被允许？ | 可同时控制 Workflow 与 Agentic Loop |
| Runtime | 真正在哪里执行？ | 两者共同依赖执行基础设施 |
| Verification | 是否真的成功？ | 无论 Workflow 还是 Agent 都需要 |
| Human Approval | 是否授予高风险 Authority？ | 常作为 Hybrid Workflow 的硬 Gate |

---

#### 2.8.58 面试掌握边界

至少应该能够稳定回答：

1. **Agent 和 Workflow 的核心区别是什么？**  
   核心不是有没有 LLM，而是谁拥有运行时 control-flow decision；Workflow 主要预定义控制结构，Agent 根据 State / Observation 动态选择 Action。

2. **用了 LLM 就是 Agent 吗？**  
   不是。LLM 可以只是固定 Workflow 中的分类、抽取、生成节点。

3. **Tool Calling 就是 Agent 吗？**  
   不是。固定流程中的 Tool Calling 仍可能只是 Workflow。

4. **Workflow 可以有条件分支吗？**  
   可以。运行时分支不等于 Agent；只要 branch set 和 transition rules 主要由开发者预定义，仍然是 Workflow。

5. **Agent 是不是完全自主？**  
   不应该。成熟 Agent 通常在 Tool、Permission、Budget、Sandbox、Approval 等边界内运行。

6. **什么时候优先 Workflow？**  
   路径稳定、规则明确、高风险、高频、需要强可复现性时。

7. **什么时候优先 Agent？**  
   路径难预先穷举、Observation 会持续改变策略、需要开放检索 / 规划 / 异常处理时。

8. **什么是 Hybrid Agent System？**  
   Workflow 提供确定性骨架和硬边界，Agentic Node 处理运行时不确定决策，两者通过 structured state / tool / verifier 连接。

9. **为什么 Workflow 不比 Agent“低级”？**  
   Workflow 的确定性、可审计、可测试和可证明边界在高风险系统中本身就是优势。

10. **什么是 Workflow Backbone + Agentic Nodes？**  
    整体 control graph 稳定，只在语义不确定或开放探索节点调用 Agent。

11. **Agent 可以调用 Workflow 吗？**  
    可以。稳定子过程可以封装成高层 Tool，由 Agent 选择调用。

12. **Workflow 可以调用 Agent 吗？**  
    可以。Agent 可以作为 Workflow 中一个动态节点。

13. **为什么高风险 Action 应更 Workflow-like？**  
    越接近不可逆副作用，越需要 deterministic validation、permission、approval 和 postcondition verification。

14. **如何判断要不要引入 Agent？**  
    找 Uncertainty Frontier：只有需要运行时语义判断、自适应或开放探索的位置才引入 Agentic control。

15. **Agenticness 越高越好吗？**  
    不。更高 Agenticness 通常同时增加 variance、cost、latency、security surface 与 eval complexity。

16. **最推荐的系统设计原则是什么？**  
    把确定性留给程序，把不确定性留给 Agent；把 Authority 留给 Policy / Permission，把 Proposal 交给模型。

17. **怎样评价 Hybrid 系统？**  
    联合看 task success、constraint、cost、latency、variance、safety、recovery、unnecessary-agent rate 与 missed-agent-opportunity rate。

18. **Agent vs Workflow 最核心的一句话是什么？**  
    不是“Agent 还是 Workflow”二选一，而是决定哪些控制权必须在开发时固定、哪些值得推迟到运行时由 Policy 根据真实 Observation 决定。

---

#### 2.8.59 第一层 Model & Decision Core 如何在这里闭环？

现在可以把整个第一层连成一条完整逻辑：

```text
LLM autoregressive generation
        ↓
模型怎样产生局部决策
        ↓
Agent definition / Agent Loop
        ↓
Reasoning + Action + Observation
        ↓
Planning
        ↓
Reflection
        ↓
Verification
        ↓
Routing
        ↓
Agent vs Workflow
        ↓
决定哪些 runtime decisions 值得交给 Agent
```

所以第一层最终不是教：

```text
“怎么把所有东西做成 Agent”
```

而是教：

> **怎样判断一个 Agent 决策应该存在，以及它应该拥有多大的自由度。**

这才是 Model & Decision Core 真正完整的闭环。

---

#### 2.8.60 本节一句话总结

> **Agent 与 Workflow 的根本区别不在于是否使用 LLM、Tool 或多步流程，而在于运行时控制流的自由度由谁拥有：Workflow 把更多决策提前固化为显式规则和状态转移，Agent 把部分控制权推迟到运行时由 Policy 根据 Goal、State 与 Observation 动态选择；成熟系统通常不是二选一，而是用 Workflow 固定确定性、高风险与可验证边界，用 Agent 处理真正的语义不确定性、开放探索与异常 frontier，从而把 determinism 与 autonomy 分配到最有价值的位置。**

#### 2.8.61 参考资料

- van der Aalst W M P, ter Hofstede A H M, Kiepuszewski B, Barros A P. **Workflow Patterns**. Distributed and Parallel Databases, 14:5–51, 2003. 经典工作，用于理解 Workflow 中 sequence、choice、parallelism、synchronization 等控制流模式。
- Russell S, Norvig P. **Artificial Intelligence: A Modern Approach**. Pearson. 可用于理解 agent、environment、state、action、policy 与 rational action 的基础框架。
- Yao S, Zhao J, Yu D, et al. **ReAct: Synergizing Reasoning and Acting in Language Models**. ICLR, 2023. 用于理解运行时 Observation 如何改变 Agent Action，而不是固定执行一条预先生成的路径。
- Shinn N, Cassano F, Gopinath A, et al. **Reflexion: Language Agents with Verbal Reinforcement Learning**. NeurIPS, 2023. 可用于理解 Agent 在动态执行失败后如何基于反馈改变后续尝试。
