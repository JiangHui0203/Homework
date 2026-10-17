### 2.4 Planning

#### 2.4.1 定义：Planning 到底是什么？

上一节 ReAct 解决的是：

> **基于当前 Observation，下一步应该做什么？**

Planning 则进一步问：

> **为了达到一个较远的 Goal，未来若干个相互依赖的步骤应该怎样组织？**

因此 Planning 不是简单生成一句：

```text
“我先做 A，再做 B，最后做 C。”
```

更完整地说，Planning 是：

> **根据 Goal、当前 State、可用 Action、约束和资源，构造一组可执行的中间目标与动作关系，使 Agent 能从当前状态逐步到达目标状态。**

经典抽象可以写成：

```text
Current State s0
      ↓
Goal g
      ↓
Available Actions A
      ↓
Constraints C
      ↓
Planner
      ↓
Plan π
      ↓
Execution
      ↓
Goal State
```

如果计划是动作序列：

$$
\pi=(a_1,a_2,\ldots,a_n)
$$

理想情况下执行这些 Action 后：

$$
s_0 \xrightarrow{a_1} s_1
\xrightarrow{a_2} \cdots
\xrightarrow{a_n} s_n
$$

并满足：

$$
g(s_n)=\text{true}
$$

但是现实 Agent 环境通常：

```text
部分可观测
工具可能失败
环境会变化
执行结果不确定
用户可能补充新约束
```

所以现代 Agent Planning 往往不是一次性生成一条永远不变的计划，而是：

```text
Plan
→ Execute
→ Observe
→ Validate
→ Repair / Replan
→ Continue
```

因此一句话：

> **Planning 负责为未来组织结构，Agent Loop 负责在真实反馈下不断修正这个结构。**

---

#### 2.4.2 为什么 Agent 需要 Planning？

如果任务只需要一步：

```text
查询今天东京天气
```

可能只需：

```text
get_weather("Tokyo")
```

Planning 价值有限。

但如果任务是：

```text
阅读一个代码仓库，定位 bug，修复代码，运行测试，并给出修改说明。
```

则至少隐含：

```text
理解任务
↓
定位相关文件
↓
建立故障假设
↓
复现问题
↓
修改代码
↓
运行验证
↓
必要时修复
↓
检查 diff
↓
完成
```

这些步骤存在：

```text
dependency
ordering
precondition
resource requirement
verification point
```

如果 Agent 只在每一步问：

> “现在最像应该做什么？”

而没有任何更长程结构，就容易出现：

```text
局部合理
但全局遗漏
```

例如：

```text
修复了代码
→ 直接回答用户
→ 忘了运行测试
```

或者：

```text
重复搜索
→ 没有形成明确子目标
→ trajectory 漂移
```

所以 Planning 的核心价值是：

> **把一个长程 Goal 转换为可管理的中间结构。**

---

#### 2.4.3 Planning 的本质不是“列 Todo List”

最弱的计划可能是：

```text
1. 分析问题
2. 查找信息
3. 得出结论
```

看起来像计划，但几乎没有控制价值。

因为它没有说明：

```text
每一步什么时候算完成？
步骤之间有什么依赖？
缺什么输入？
失败怎么办？
哪些步骤可以并行？
哪些步骤必须先验证？
完成后 State 应该发生什么变化？
```

真正有执行价值的计划更像：

```text
Step A: locate target module
Precondition: repository available
Success condition: relevant file set identified

Step B: reproduce failure
Depends on: A
Success condition: failing test or minimal reproduction obtained

Step C: patch root cause
Depends on: B
Success condition: code diff created

Step D: verify
Depends on: C
Success condition: relevant tests pass
```

因此：

> **Planning 的质量不在于计划文本有多详细，而在于它是否形成了可执行、可检查、可更新的控制结构。**

---

#### 2.4.4 Goal Decomposition：先把 Goal 拆成 Subgoals

Planning 最核心的操作之一是 Task / Goal Decomposition。

例如 Goal：

```text
判断某项政策是否已经正式生效，并给出可靠证据。
```

可以拆成：

```text
G0: determine current policy status
│
├── G1: identify authoritative policy document
├── G2: determine stated effective date
├── G3: check whether implementation conditions are satisfied
└── G4: collect evidence sufficient for final answer
```

这里最重要的是：

```text
Subgoal
≠
随便拆出来的一段任务描述
```

一个好的 Subgoal 应该尽量满足：

```text
有明确输出
有完成条件
与其他 Subgoal 边界清晰
能够映射到 Action / Tool
```

例如：

```text
“继续研究一下”
```

不是好 Subgoal。

而：

```text
“找到政策发布机构的原始公告，并提取生效日期”
```

更容易执行和验证。

---

#### 2.4.5 Plan Step 最好有 Preconditions 和 Effects

经典 AI Planning 中，一个 Action 常被描述为：

```text
Preconditions
Action
Effects
```

例如：

```text
Action:
run_test_suite

Preconditions:
repository_checked_out
runtime_ready

Effects:
test_result_available
```

对于 Agent，同样有用。

假设计划写：

```text
Step 3: deploy service
```

但实际 State：

```text
tests_pass = false
```

如果没有显式 precondition，Agent 可能仍然继续执行。

更合理的是：

```text
deploy_service
requires:
    tests_pass == true
    approval == granted
```

因此 Planning 不只是“排顺序”，也是：

> **描述在什么状态下什么动作才合法。**

---

#### 2.4.6 Dependency：计划不是只有顺序，还有依赖关系

很多计划看起来像：

```text
A → B → C → D
```

但真实任务往往不是纯线性。

例如研究任务：

```text
                ┌→ Search source A ─┐
Identify topic ─┼→ Search source B ─┼→ Compare evidence → Write conclusion
                └→ Search source C ─┘
```

此时：

```text
A、B、C
```

可以并行；而：

```text
Compare evidence
```

必须等待多个输入完成。

因此 Plan 更适合表示成：

```text
DAG / dependency graph
```

而不是永远是一串列表。

这直接影响：

```text
parallel execution
critical path
latency
resource scheduling
failure propagation
```

---

#### 2.4.7 Linear Plan、Hierarchical Plan 与 DAG Plan

常见计划结构可以分为三类。

##### 1. Linear Plan

```text
A → B → C → D
```

适合：

```text
步骤依赖明确
任务短
并行空间小
```

##### 2. Hierarchical Plan

```text
Goal
├── Subgoal A
│   ├── A1
│   └── A2
├── Subgoal B
│   ├── B1
│   └── B2
└── Subgoal C
```

适合复杂长任务。

这与经典 HTN（Hierarchical Task Network）Planning 的直觉接近：

```text
高层任务
↓
不断分解
↓
最终得到可执行动作
```

##### 3. Dependency Graph / DAG Plan

```text
A ─┐
   ├→ D → F
B ─┤
   └→ E ─┘
C ─────→ E
```

适合：

```text
并行研究
多文件分析
多子 Agent 协作
数据 pipeline
```

所以：

> **Plan 的表示形式应该匹配任务结构，而不是所有任务都强制写成 numbered list。**

---

#### 2.4.8 Planning Granularity：计划应该拆多细？

过粗：

```text
1. 解决问题
2. 验证结果
```

没有控制价值。

过细：

```text
1. 打开终端
2. 输入 c
3. 输入 d
4. 输入空格
5. 输入 .
```

会让计划本身变成负担。

好的粒度通常满足：

> **每个 Plan Step 对应一个有语义的状态变化或可验证子目标。**

例如 Coding Agent：

```text
locate failing module
reproduce bug
patch root cause
run targeted tests
run broader regression
inspect diff
```

比：

```text
click terminal
open file
scroll down
```

更适合作为高层 Plan。

微操作由 Runtime / Tool execution 负责。

因此：

```text
Planning
→ semantic steps

Runtime
→ execution details
```

---

#### 2.4.9 Planning Horizon：应该提前计划多远？

Planning 的另一个关键变量是 Horizon。

Short-horizon：

```text
只计划接下来 1–2 步
```

Long-horizon：

```text
提前规划完整任务
```

环境越稳定，长计划越有价值。

环境越不确定：

```text
网页会变
工具返回未知
用户可能补充信息
执行可能失败
```

越应该采用：

```text
shorter horizon
+
frequent replanning
```

所以：

> **计划越远，对环境模型准确性的要求越高。**

这和控制系统中的 receding-horizon 思想很接近：

```text
计划未来若干步
↓
只执行近期动作
↓
拿到新 Observation
↓
重新规划
```

---

#### 2.4.10 ReAct 与 Planning 到底是什么关系？

上一节已经看到：

```text
ReAct
= Reason → Action → Observation → Reason
```

它强调的是局部反馈。

Planning 强调的是：

```text
Goal
↓
future structure
↓
subgoals / dependencies / order
```

可以粗略理解：

```text
ReAct
= local feedback control

Planning
= longer-horizon structure
```

它们不是竞争关系。

成熟 Agent 常常是：

```text
Goal
↓
High-level Plan
↓
Execute current Plan Step
↓
ReAct locally
↓
Observation
↓
Update / Replan if needed
↓
Next Plan Step
```

所以：

> **Planning 决定“我们大体往哪里走”，ReAct 决定“面对当前真实反馈下一步具体怎么走”。**

---

#### 2.4.11 Plan-and-Execute 是什么？

一种典型结构是：

```text
Planner
   ↓
Plan
   ↓
Executor
   ↓
Step 1
   ↓
Step 2
   ↓
...
   ↓
Final Result
```

Planner 负责：

```text
任务分解
步骤排序
依赖设计
```

Executor 负责：

```text
具体工具选择
Action 执行
Observation 处理
```

如果执行结果偏离计划，则：

```text
Executor
   ↓
Observation / Failure
   ↓
Planner
   ↓
Replan
```

这样可以把：

```text
long-horizon planning
```

和：

```text
short-horizon execution
```

分开。

---

#### 2.4.12 Planner 和 Executor 一定要是两个 Agent 吗？

不一定。

逻辑角色：

```text
Planner
Executor
```

不等于必须：

```text
两个独立 LLM Agent
```

可以是同一个模型在不同调用中承担不同角色：

```text
LLM call 1 → generate plan
LLM call 2 → execute next step
```

也可以：

```text
Planner = deterministic code
Executor = LLM Agent
```

甚至：

```text
Planner = LLM
Executor = workflow engine
```

因此：

> **Planner / Executor 首先是系统职责边界，不是进程或 Agent 数量。**

---

#### 2.4.13 Static Plan vs Dynamic Plan

Static Plan：

```text
生成一次
↓
执行到底
```

适合：

```text
环境稳定
任务步骤可预测
失败概率低
```

Dynamic Plan：

```text
Plan_t
↓
Execute
↓
Observation
↓
Plan_{t+1}
```

适合 Agent 环境。

因为 Agent 面临：

```text
unknown tool result
external changes
partial failure
new user constraints
new evidence
```

因此大多数复杂 Agent 更接近：

> **Plan–Execute–Observe–Replan。**

---

#### 2.4.14 什么情况下应该 Replan？

不是每一步都重新规划。

否则 Planning 会退化成：

```text
每一步都重新从头想一遍
```

成本很高。

常见 Replanning Trigger 包括：

```text
1. 当前 Plan Step 失败
2. Preconditions 不再成立
3. Observation 与预测严重不一致
4. 新约束出现
5. Goal 发生变化
6. 关键资源不可用
7. 原计划出现死路
8. 发现更便宜 / 更安全路径
9. 已完成步骤改变了后续依赖
10. Progress 长时间停滞
```

因此可以抽象为：

```text
if plan_still_valid(state):
    continue
else:
    replan()
```

---

#### 2.4.15 Replanning 不是“每次失败都推翻整个计划”

失败之后至少有三种处理层级：

```text
Retry
Plan Repair
Full Replan
```

##### Retry

当前 Step 本身仍合理，只是瞬时失败：

```text
timeout
rate limit
transient network error
```

##### Plan Repair

整体方向仍正确，只需替换局部步骤：

```text
source A unavailable
→ replace with source B
```

##### Full Replan

核心假设或 Goal 路径已经失效：

```text
原以为 bug 在 parser
但新证据证明问题来自 upstream schema
```

此时继续原计划代价很高。

所以：

> **Replanning 应该有层级，而不是“一有异常就全部重做”。**

---

#### 2.4.16 Plan Validation：计划本身也需要被检查

模型生成的计划并不天然可执行。

应该检查：

```text
步骤是否覆盖 Goal？
是否存在循环依赖？
Preconditions 是否可能满足？
是否引用不存在的 Tool？
是否违反权限？
是否遗漏必要验证步骤？
是否超预算？
是否包含不可逆高风险 Action？
```

例如：

```text
Plan:
1. 删除旧数据库
2. 备份数据库
```

顺序显然错误。

所以：

> **Plan 是模型提出的候选控制结构，不是自动可信的执行命令。**

Harness 可以在执行前做：

```text
schema validation
constraint check
dependency check
permission check
budget check
```

---

#### 2.4.17 Plan 应该进入 Agent State

如果 Plan 只存在于某一次模型输出文本中：

```text
“I will first A, then B, then C...”
```

后续很难可靠跟踪。

更好的做法是将 Plan 结构化存入 State：

```json
{
  "plan_id": "plan_17",
  "goal": "fix failing parser test",
  "steps": [
    {
      "id": "P1",
      "description": "reproduce failure",
      "status": "done"
    },
    {
      "id": "P2",
      "description": "locate root cause",
      "status": "in_progress"
    },
    {
      "id": "P3",
      "description": "patch implementation",
      "status": "pending"
    }
  ]
}
```

这样 Harness 可以知道：

```text
current_step
completed_steps
blocked_steps
pending dependencies
```

因此：

> **Plan 应该是 State，而不仅是 Prompt 中的一段自然语言。**

---

#### 2.4.18 Plan Step 的状态机

Plan Step 不应该只有：

```text
finished / unfinished
```

更完整的状态可能是：

```text
PENDING
READY
IN_PROGRESS
DONE
FAILED
BLOCKED
SKIPPED
CANCELLED
```

例如：

```text
P1 DONE
P2 DONE
P3 BLOCKED: permission_required
P4 PENDING: depends_on=P3
```

这对：

```text
resume
checkpoint
parallel scheduling
failure recovery
human approval
```

非常重要。

---

#### 2.4.19 Planning 与 Workflow 的区别

Workflow：

```text
开发者预定义控制流
```

例如：

```text
A → B → C
```

Planning：

```text
运行时根据 Goal / State 构造控制结构
```

因此：

```text
Workflow
= control structure known beforehand

Planning
= control structure at least partially decided at runtime
```

但它们可以组合：

```text
Fixed Workflow
↓
Planning Node
↓
Dynamic Subplan
↓
Back to Workflow
```

因此并不是：

```text
Workflow OR Agent
```

而更常见：

```text
Workflow + bounded planning
```

---

#### 2.4.20 Planning 与 Search 的区别

Planning 经常需要 Search，但二者不相同。

Planning 问：

> **应该走哪条未来动作路径？**

Search 问：

> **在多个可能候选之间怎样探索、评价和选择？**

例如 Planner 生成三个候选计划：

```text
Plan A
Plan B
Plan C
```

然后：

```text
simulate / score / verify
↓
choose B
```

此时：

```text
Planning
→ generated candidate futures

Search
→ explored and selected among them
```

所以：

> **Planning 可以是 Search 的对象；Search 也可以是 Planning 的内部机制。**

---

#### 2.4.21 Planning 与 Scheduling 的区别

两者也经常混淆。

Planning 主要关心：

```text
做什么
为什么做
依赖是什么
```

Scheduling 更关心：

```text
什么时候做
在哪个 worker 上做
资源怎样分配
哪些可以并行
```

例如：

```text
Plan:
A、B 独立完成后执行 C

Schedule:
worker1 executes A at t0
worker2 executes B at t0
worker1 executes C after both finish
```

所以：

```text
Planning
= logical action structure

Scheduling
= temporal / resource assignment
```

Runtime 会在后面专门处理 Scheduling / Queue。

---

#### 2.4.22 Planning 与 Reflection 的区别

Planning：

```text
面对未来
→ 决定接下来怎样组织行动
```

Reflection：

```text
面对已经发生的结果 / 轨迹
→ 分析哪里错、为什么错、怎样改
```

当然 Reflection 的结果可以触发 Replanning：

```text
Execution failed
↓
Reflection finds wrong assumption
↓
Replan
```

但二者职责不同。

---

#### 2.4.23 Planning 与 Verification 的区别

Planning 负责：

```text
怎样到达目标
```

Verification 负责：

```text
是否真的到达目标
```

例如计划：

```text
1. modify code
2. run tests
```

真正的 Verification 是：

```text
tests_pass == true
```

而不是：

```text
计划里写了“run tests”
```

因此：

> **计划中包含验证步骤，不代表验证已经发生。**

---

#### 2.4.24 Constraint-aware Planning

真实 Agent 的 Goal 通常不是唯一约束。

例如：

```text
完成任务
AND
不能修改 protected files
AND
不能超过 $1 预算
AND
必须使用官方来源
AND
高风险写操作需要 approval
```

所以 Planner 面对的是：

```text
Goal
+
Constraints
```

而不是只有 Goal。

计划生成时应该同时考虑：

```text
permission
budget
time
safety
user preference
resource availability
policy
```

否则可能出现：

```text
能完成
但不允许
```

或者：

```text
理论可行
但超预算
```

---

#### 2.4.25 Resource-aware Planning

Plan 还应理解资源。

例如：

```text
Tool A:
fast, cheap, lower accuracy

Tool B:
slow, expensive, high accuracy
```

不同状态下可能选择不同计划：

```text
routine case
→ A

high uncertainty
→ B
```

又例如：

```text
三个 independent searches
```

可以并行，但会增加：

```text
concurrency
cost
rate-limit pressure
```

所以规划也可以是：

> **资源分配问题。**

---

#### 2.4.26 Tool-aware Planning

Planner 不能假设 Agent 拥有任意能力。

计划必须建立在真实 Action Space 上：

```text
available_tools
permissions
runtime
skills
subagents
```

错误计划：

```text
Step 2: query private database
```

但 Agent 根本没有数据库 Tool。

因此 Planner 的输入通常应该包含某种：

```text
capability model
```

即：

> **我实际能做什么？**

这就是为什么 Planning 与 Tool Discovery、Skills、MCP、Subagents 后面会连接起来。

---

#### 2.4.27 Planning under Uncertainty

经典确定性计划假设：

```text
执行 Action A
→ 一定得到 State B
```

但 Agent 世界更像：

```text
Action A
→ success
→ empty result
→ timeout
→ partial success
→ permission denied
```

因此不能把计划理解成唯一确定未来。

更合理的是：

```text
Action
↓
possible outcomes
├── O1 → branch A
├── O2 → branch B
└── O3 → recovery
```

这叫 contingent / conditional planning 的直觉。

例如：

```text
search official website
├── found → inspect source
└── not found → search archive / alternate authority
```

因此：

> **现实 Agent 的 Plan 常常应该包含条件分支，而不是只有单一路径。**

---

#### 2.4.28 Partial Observability 对 Planning 有什么影响？

如果 Agent 看不到完整 World State，就不能一次性规划得完全准确。

此时计划中必须包含：

```text
information-gathering actions
```

例如：

```text
不知道依赖版本
→ inspect environment

不知道用户预算
→ ask user

不知道测试失败原因
→ run diagnostic test
```

所以在部分可观测环境下：

> **“先获取什么信息”本身就是 Planning 的一部分。**

这与 ReAct 中的 epistemic action 直接连接。

---

#### 2.4.29 Plan 里应该显式表示 Assumption 吗？

复杂计划往往建立在假设上：

```text
Assumption A:
当前失败由 parser 导致

Assumption B:
官方公告页面仍是最新版本
```

如果假设不显式保存，后续 Observation 推翻它时，Agent 可能仍继续旧计划。

因此高价值计划状态可以包含：

```text
assumptions
unknowns
risks
expected observations
```

例如：

```json
{
  "assumption": "failure originates in parser",
  "evidence": "stack trace points to parse_config",
  "confidence": "medium",
  "invalidate_if": "minimal parser test passes"
}
```

这样 Replanning 更容易被触发。

---

#### 2.4.30 Plan 与 World Model

要规划未来，Planner 隐含需要某种预测：

```text
如果执行 A，会发生什么？
```

即：

$$
\hat{s}_{t+1}=f(s_t,a_t)
$$

这个 $f$ 可以来自：

```text
模型知识
规则
工具说明
环境模拟器
历史轨迹
```

如果 World Model 错误：

```text
错误预测 Action 后果
↓
错误 Plan
```

例如模型以为：

```text
删除缓存后服务会自动恢复
```

但真实系统并不会。

所以：

> **Planning quality 受到 Environment / World Model quality 的上限约束。**

这也是为什么长 horizon 计划更脆弱。

---

#### 2.4.31 Plan Repair：只修坏掉的部分

假设计划：

```text
A → B → C → D
```

执行到 B 时发现：

```text
B unavailable
```

如果 C、D 的逻辑仍然有效，可以：

```text
A → B' → C → D
```

而不是重新生成整个计划。

这种局部修复叫 Plan Repair 的思想。

优势：

```text
保留已经验证的结构
减少 token / latency
降低无意义漂移
```

但如果 B 的失败意味着上层假设都错了，则需要 Full Replan。

关键是判断：

> **失败是局部执行问题，还是全局计划假设被推翻？**

---

#### 2.4.32 Multi-Agent Planning

多 Agent 系统会多一层：

```text
Task decomposition
↓
Agent assignment
↓
Dependency
↓
Coordination
↓
Aggregation
```

例如：

```text
Research Goal
├── Agent A: regulatory sources
├── Agent B: technical sources
└── Agent C: market evidence
        ↓
     Aggregator
```

Planner 还必须考虑：

```text
哪些 Subtask 真正独立？
Context 如何共享？
谁拥有最终决策权？
结果冲突怎样处理？
是否值得并行成本？
```

因此 Multi-Agent 并不是把计划中的每一步都交给一个 Agent。

更合理的是：

> **只有当任务分解产生真实并行性、专业能力差异或上下文隔离收益时，才值得 delegation。**

---

#### 2.4.33 Cost-aware Planning

计划 A：

```text
20 次网页搜索
5 个 verifier
3 个 subagents
```

计划 B：

```text
先查 1 个权威源
只有不确定时再扩展
```

两者都可能完成任务，但成本完全不同。

所以计划评分可以考虑：

$$
U(\pi)
=
Q(\pi)
-\lambda C(\pi)
-\mu L(\pi)
-\gamma R(\pi)
$$

其中：

```text
Q = expected quality
C = cost
L = latency
R = risk
```

这与前面 Budget 章节完全一致。

真正好的 Planner 不只问：

> “哪条路径能做完？”

还问：

> **哪条路径在质量、成本、延迟、风险之间更合适？**

---

#### 2.4.34 Minimal Plan Schema

一个实用计划结构可以是：

```json
{
  "plan_id": "plan_42",
  "goal": "fix parser regression",
  "assumptions": [
    "failure is reproducible"
  ],
  "steps": [
    {
      "id": "P1",
      "goal": "reproduce failure",
      "status": "ready",
      "depends_on": [],
      "preconditions": ["repo_available"],
      "success_criteria": ["failing_test_identified"],
      "allowed_actions": ["run_test", "read_file"]
    },
    {
      "id": "P2",
      "goal": "locate root cause",
      "status": "pending",
      "depends_on": ["P1"],
      "success_criteria": ["root_cause_hypothesis_supported"]
    }
  ],
  "constraints": {
    "max_cost": 1.0,
    "protected_paths": ["prod/secrets"]
  }
}
```

重点不是字段名，而是 Plan 能表达：

```text
Goal
Dependency
State
Precondition
Success Criteria
Constraint
```

---

#### 2.4.35 一个 Planning-aware Agent Loop

```python
state = initialize(task)
plan = planner.create(state)

while True:
    state = observe_and_update(state)

    if success_check(state):
        return finish(state)

    if not plan.is_valid(state):
        plan = planner.repair_or_replan(
            state=state,
            previous_plan=plan,
        )

    step = plan.next_ready_step(state)

    if step is None:
        return blocked("no executable plan step")

    action = executor.decide(
        state=state,
        plan_step=step,
    )

    action = validate(action, state)
    result = runtime.execute(action)

    state = update_state(state, action, result)
    plan = update_plan_status(plan, state, result)
```

这里有两个循环：

```text
Planning Loop
→ plan validity / repair / replan

Execution Loop
→ action / observation / state update
```

二者嵌套，而不是混为一层。

---

#### 2.4.36 Coding Agent：Planning 到底解决什么？

用户：

```text
修复支付模块里偶发的重复扣款问题。
```

弱 Agent 可能：

```text
search "payment"
↓
看到一个函数
↓
直接改代码
```

Planning-aware Agent 首先可能形成：

```text
Goal:
stop duplicate charge without breaking legitimate retries

Plan:
P1. locate payment initiation and retry logic
P2. reproduce / identify duplicate path
P3. inspect idempotency mechanism
P4. design minimal fix
P5. run duplicate-charge regression test
P6. run normal retry tests
P7. inspect diff and side effects
```

注意这里：

```text
P5 + P6
```

不是装饰，而是 Goal 的不同约束：

```text
prevent duplicate
AND
preserve retry behavior
```

执行过程中如果发现：

```text
实际重复扣款来自 webhook replay
```

则应该：

```text
invalidate original assumption
↓
repair / replan
```

而不是继续在 client retry 上改代码。

---

#### 2.4.37 Research Agent：为什么 Planning 比“多搜几次”更重要？

任务：

```text
判断某技术方案是否适合生产部署。
```

没有计划时：

```text
搜很多网页
↓
信息不断堆积
↓
最后凭印象总结
```

Planning 可以先建立证据维度：

```text
G1: capability evidence
G2: reliability evidence
G3: cost / latency evidence
G4: security constraints
G5: operational maturity
```

然后每个 Subgoal 定义 evidence requirement：

```text
primary docs
benchmarks
incident / limitation evidence
```

于是搜索行为由 Plan 驱动：

```text
缺 G3
→ search cost evidence

G2 evidence sufficient
→ stop searching reliability
```

这会显著减少：

```text
漫无目的 retrieval
```

所以：

> **Research Planning 的核心不是“列几个搜索词”，而是先定义证据结构。**

---

#### 2.4.38 Planning 的典型 Failure Modes

**1. Fake Planning**

输出一个看起来像计划的 numbered list，但没有可执行语义。

**2. Over-decomposition**

把任务拆成大量微步骤，计划维护成本超过收益。

**3. Under-decomposition**

计划过粗，不能指导执行。

**4. Missing Dependency**

后续步骤在前置条件未满足时启动。

**5. Wrong Ordering**

例如先 destructive action，再 backup。

**6. Hallucinated Capability**

计划依赖不存在的 Tool / Permission / Data。

**7. Stale Plan**

Environment 已变化，Agent 仍执行旧计划。

**8. No Replanning Trigger**

Observation 已经推翻原假设，但计划不更新。

**9. Replan Too Often**

每一步都推翻重来，产生高成本和 trajectory drift。

**10. Replan Too Late**

明显死路仍持续执行。

**11. Plan–Execution Drift**

计划写 A，实际一直执行 B、C，却不更新 Plan State。

**12. Missing Completion Criteria**

Step 标记 done 只是因为“做过了”，而不是 success criteria 满足。

**13. Planning without Verification**

计划最后写“验证”，但系统从未真正执行 verifier。

**14. Constraint Blindness**

计划能完成 Goal，却违反权限、预算或用户约束。

**15. Optimistic World Model**

假设 Tool 一定成功、环境一定稳定。

**16. Unbounded Branching**

计划生成太多候选、Subagents 或搜索分支。

**17. Premature Commitment**

信息不足时过早确定一个长计划。

**18. No Information-gathering Step**

缺关键事实，却直接开始改变 Environment。

**19. Planning as Narrative**

计划只用于向用户展示，没有进入 State，也不控制 Execution。

**20. Completed-plan Illusion**

所有 plan steps 标记 done，但真正 Goal 尚未验证。

---

#### 2.4.39 怎样评价 Planning？

不能只问：

```text
“这个计划看起来合理吗？”
```

至少可以分为四层。

##### Plan-level

```text
Goal coverage
Dependency correctness
Constraint compliance
Executability
Risk awareness
```

##### Step-level

```text
step relevance
precondition satisfaction
success criteria
```

##### Execution-level

```text
plan adherence
observation-driven update
replanning quality
```

##### Outcome-level

```text
task success
cost
latency
reliability
```

一个漂亮计划最后失败，仍然是失败的 Agent。

一个计划文本普通，但执行过程中不断正确修正并完成任务，可能反而是好系统。

因此：

> **Plan Quality ≠ Agent Quality。**

真正要评价的是：

> **计划是否帮助 Agent 更可靠、更高效地完成 Goal。**

---

#### 2.4.40 Plan Adherence 也不能越高越好

如果定义：

```text
plan_adherence
= 实际执行与原计划一致程度
```

直觉上越高越好。

但如果 Environment 改变：

```text
旧计划已失效
```

仍然高度 adherence 反而是坏事。

所以真正希望的是：

```text
有效计划时稳定执行
失效计划时及时偏离并 Replan
```

因此要联合看：

```text
plan validity
+
plan adherence
+
replanning quality
```

---

#### 2.4.41 Planning 数据为什么很有价值？

高质量 Agent trajectory 中，可以抽取：

```text
Goal
Subgoals
Plan
Step status
Action
Observation
Plan revision
Outcome
```

这类数据可以研究：

```text
任务分解质量
dependency error
错误 assumption
replanning trigger
plan repair
long-horizon drift
```

相比只保存最终答案：

```text
input → final output
```

Planning data 提供了更强的过程监督信号。

但要注意：

> **模型写出来的“Plan 文本”不一定是真正驱动执行的 Plan State。**

做数据时必须区分：

```text
declared plan
executed plan
actual trajectory
```

---

#### 2.4.42 Planning 的工程原则

**原则一：只在任务复杂度值得时 Planning。**

简单任务不需要人为增加 Planner。

**原则二：Plan Step 必须有可观察的完成条件。**

否则无法知道进度。

**原则三：Plan 是 State，不只是文本。**

需要结构化跟踪版本和状态。

**原则四：规划必须建立在真实 Capability 上。**

不能依赖不存在的 Tool / Permission。

**原则五：计划必须允许 Observation 推翻它。**

否则只是 Open-loop script。

**原则六：优先局部 Repair，再决定是否 Full Replan。**

降低无谓漂移和成本。

**原则七：Planning 与 Verification 分离。**

Planner 不能自己宣告 Goal 已满足。

**原则八：高风险计划先验证约束再执行。**

尤其是不可逆 Action。

**原则九：规划粒度保持在语义状态变化层。**

不要把微操作全塞进 Plan。

**原则十：计划质量必须放进 task-level trade-off 看。**

更长、更复杂的计划不自动更好。

---

#### 2.4.43 与相邻概念的边界

| 概念 | 核心问题 | 与 Planning 的关系 |
|---|---|---|
| Agent Loop | 系统怎样循环运行？ | Planning 是 Loop 中产生未来结构的一种决策机制 |
| ReAct | 当前 Observation 下下一步怎么做？ | 偏局部反馈；可用于执行 Plan Step |
| Task Decomposition | Goal 如何拆成 Subgoals？ | Planning 的核心操作之一 |
| Plan-and-Execute | 如何分离长程规划和局部执行？ | Planning 的经典系统模式 |
| Search | 如何探索多个候选？ | 可用于搜索计划空间 |
| Workflow | 控制流是否预先固定？ | Planning 通常在运行时动态构造部分控制流 |
| Scheduling | 何时、在哪些资源上执行？ | 在 Plan 上进一步做时间与资源安排 |
| Reflection | 已发生的轨迹哪里有问题？ | 反思结果可触发 Replanning |
| Verification | 是否真的满足 Goal？ | 检查计划 / 执行是否达成目标 |
| Harness | 谁管理 Plan Policy？ | 决定何时规划、重规划、验证和终止 |
| Runtime | 谁真正执行 Plan 中的 Action？ | 提供 execution substrate |

---

#### 2.4.44 面试掌握边界

这一节至少要能稳定回答：

1. **Agent Planning 是什么？**  
   根据 Goal、State、Action Space、约束和资源，构造可执行的中间目标与动作结构，使系统逐步到达 Goal。

2. **Planning 和普通 Todo List 有什么区别？**  
   真正 Plan 有 dependency、precondition、success criteria、state 和 replanning semantics，而不仅是自然语言列表。

3. **为什么需要 Task Decomposition？**  
   把长程 Goal 转换成边界清晰、可执行、可验证的 Subgoals。

4. **ReAct 和 Planning 有什么区别？**  
   ReAct 更偏局部 feedback control；Planning 更偏较长 horizon 的 future structure。两者通常组合。

5. **Plan-and-Execute 是什么？**  
   Planner 负责分解和组织任务，Executor 根据 Plan Step 执行具体 Action，并在反馈异常时触发 Replan。

6. **Planner 和 Executor 必须是两个 Agent 吗？**  
   不需要，它们首先是职责边界，可以由同一模型不同调用、代码、Workflow 或多个 Agent 实现。

7. **什么时候应该 Replan？**  
   当 Step 失败、前置条件失效、Observation 推翻假设、新约束出现、Goal 改变或 progress 停滞时。

8. **Retry、Plan Repair、Full Replan 有什么区别？**  
   Retry 重做当前 Action；Repair 局部修改计划；Full Replan 在核心路径 / 假设失效时重建计划。

9. **Planning 和 Workflow 区别？**  
   Workflow 控制流通常开发时预定义；Planning 至少部分控制结构在运行时根据 State 动态产生。

10. **Planning 和 Search 区别？**  
    Planning 构造未来行动结构；Search 探索和选择多个候选，二者可以嵌套。

11. **Planning 和 Scheduling 区别？**  
    Planning 关心做什么和依赖；Scheduling 关心何时做、在哪个资源上做。

12. **为什么 Plan 应该进入 State？**  
    为了跟踪 step status、依赖、版本、失败和 replanning，而不是只留在一次模型输出文本里。

13. **怎样评价 Plan？**  
    看 goal coverage、dependency、constraint、executability，也要看执行中的 adherence、replanning、最终 success、cost 和 latency。

14. **为什么 plan adherence 不是越高越好？**  
    环境变化时应及时偏离失效计划；真正目标是对有效计划稳定执行，对失效计划快速 Replan。

15. **Planning 最核心的一句话是什么？**  
    Planning 不是预测一条不会变的未来，而是给长程 Goal 建立可执行、可检查、可修正的中间结构。

如果继续追问 Agent 在执行失败后怎样 critique 自己、怎样利用失败信息修改当前尝试，就进入 **2.5 Reflection / Critique**；如果追问怎样证明计划或任务真的完成，则进入 **2.6 Verification**。

---

#### 2.4.45 本节一句话总结

> **Agent Planning 的本质不是提前写一份漂亮的步骤清单，而是把长程 Goal 转换为带有 Subgoal、Dependency、Precondition、Success Criteria、Constraint 和 State 的可执行控制结构，并允许真实 Observation 持续验证、修复甚至推翻它；因此成熟 Agent 的规划闭环不是 Plan once，而是 Plan → Execute → Observe → Validate → Repair / Replan。**

#### 2.4.46 参考资料

- Fikes R E, Nilsson N J. **STRIPS: A New Approach to the Application of Theorem Proving to Problem Solving**. Artificial Intelligence, 1971.
- Ghallab M, Nau D, Traverso P. **Automated Planning: Theory and Practice**. Morgan Kaufmann, 2004.
- Yao S, Zhao J, Yu D, et al. **ReAct: Synergizing Reasoning and Acting in Language Models**. ICLR, 2023. 用于理解局部 feedback control 与长程 planning 的组合关系。
- Yao S, Yu D, Zhao J, et al. **Tree of Thoughts: Deliberate Problem Solving with Large Language Models**. NeurIPS, 2023. 可用于理解 candidate future、search 与 planning space 的关系。
