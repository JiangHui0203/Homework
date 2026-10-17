### 2.3 ReAct

#### 2.3.1 定义：ReAct 到底是什么？

ReAct 的全称是：

> **Reasoning + Acting**

它最早由 Yao 等人在 *ReAct: Synergizing Reasoning and Acting in Language Models* 中系统提出，预印本发表于 2022 年，后发表于 ICLR 2023。

ReAct 试图解决一个非常直接的问题：

```text
只会 Reasoning
→ 模型可以思考，但无法主动获得新信息或改变环境

只会 Acting
→ 模型可以执行动作，但缺少显式的状态解释、计划更新和异常处理
```

于是 ReAct 将二者交错起来：

```text
Reason
  ↓
Act
  ↓
Observe
  ↓
Reason again
  ↓
Act again
  ↓
...
```

它的核心不是某个固定的 Prompt 模板，而是一种 **interleaved reasoning–action policy**：

> **Reasoning 用来解释当前状态、形成局部计划并决定下一步 Action；Action 用来获得新的外部信息或改变 Environment；Observation 再反过来修正后续 Reasoning。**

因此 ReAct 的真正价值来自闭环：

```text
Reasoning
   ↓ proposes
Action
   ↓ changes / queries
Environment
   ↓ returns
Observation
   ↓ updates
Reasoning
```

---

#### 2.3.2 ReAct 为什么不是“CoT 后面接一个 Tool”？

最容易出现的误解是：

```text
Chain-of-Thought
+
Tool Calling
=
ReAct
```

这个说法过于粗糙。

如果系统只是：

```text
先完整想一遍
↓
最后调用一次 Tool
↓
结束
```

它并没有体现 ReAct 最关键的特征：

> **Reasoning 与 Environment Interaction 是交错发生的。**

真正的 ReAct 更像：

```text
Thought_1:
我缺一个事实，需要先搜索。

Action_1:
search(...)

Observation_1:
...

Thought_2:
搜索结果改变了原来的判断，需要打开原始来源。

Action_2:
open(...)

Observation_2:
...

Thought_3:
现在证据足够，可以回答。

Final Answer:
...
```

所以区别在于：

```text
Reason once → Act once
```

与：

```text
Reason ↔ Act ↔ Observe ↔ Reason
```

后者才是 ReAct 的核心结构。

---

#### 2.3.3 ReAct 的三个逻辑角色：Reasoning、Action、Observation

经典 ReAct 轨迹通常表现为：

```text
Thought
Action
Observation
Thought
Action
Observation
...
```

但这三个词首先是**逻辑角色**，不一定要求真实系统必须把 `Thought:`、`Action:`、`Observation:` 这三个字符串打印出来。

##### Reasoning

回答：

```text
当前状态意味着什么？
缺什么信息？
下一步最值得做什么？
刚才的 Observation 是否改变了原计划？
```

##### Action

回答：

```text
系统接下来要真正执行什么？
```

例如：

```text
search
read_file
run_test
click
call_api
ask_user
```

##### Observation

回答：

```text
执行 Action 后，Environment 返回了什么新信息或状态变化？
```

例如：

```text
搜索结果
文件内容
命令 stdout
API response
网页截图
用户补充信息
permission denied
error / timeout
```

所以 ReAct 不是三个文本标签，而是：

> **认知状态 → 环境动作 → 外部反馈** 的交替。

---

#### 2.3.4 一个最小 ReAct Loop

最简形式可以写成：

```python
state = initialize(task)

while not done:
    context = build_context(state)

    decision = model(context)

    if decision.type == "final":
        return decision.answer

    action = validate(decision.action)
    observation = execute(action)

    state = update_state(
        state,
        reasoning=decision.reasoning,
        action=action,
        observation=observation,
    )
```

注意：

```text
model()
```

可以同时输出：

```text
reasoning state
+
structured action
```

也可以只输出结构化 Action，而把 reasoning 隐藏在模型内部。

ReAct 的关键不在于 reasoning 是否对用户可见，而在于：

```text
Observation_t
```

是否真正改变：

```text
Decision_{t+1}
```

---

#### 2.3.5 一个形式化视角

可以把 Agent Policy 写成：

$$
\pi(a_t \mid h_t)
$$

其中历史 $h_t$ 包含：

$$
h_t=(g,a_0,o_1,a_1,o_2,\ldots,o_t)
$$

ReAct 增加了显式或隐式的 reasoning variable $r_t$：

$$
r_t \sim P(r_t\mid h_t)
$$

再由 reasoning 影响 Action：

$$
a_t \sim P(a_t\mid h_t,r_t)
$$

环境产生 Observation：

$$
o_{t+1}\sim P(o\mid s_t,a_t)
$$

然后进入下一轮。

从这个角度看：

> **ReAct 不是独立于 Agent Loop 的另一套系统，而是在 Agent Loop 的 Decision 部分加入了“基于当前 Observation 进行显式/隐式 reasoning，再生成 Action”的策略结构。**

---

#### 2.3.6 为什么纯 CoT 在 Agent 场景中不够？

Chain-of-Thought 主要解决：

```text
已有信息
↓
内部多步推理
↓
答案
```

但现实 Agent 经常面对：

```text
信息根本不在 Context 里
环境会变化
工具执行可能失败
用户意图可能不完整
代码运行结果未知
网页当前状态未知
```

此时继续在模型内部“多想几步”并不能创造缺失的外部事实。

例如：

```text
问题：某公司今天股价是多少？
```

如果当前 Context 没有实时价格：

```text
CoT 再长
≠
获得实时价格
```

Agent 必须做：

```text
Reason:
这是时效信息，我缺当前数据。

Action:
search / market-data tool

Observation:
current price = ...

Reason:
现在可以回答。
```

所以 ReAct 引入了一个非常重要的能力：

> **当内部推理不足时，通过 Action 主动改变自己的信息条件。**

---

#### 2.3.7 为什么“只 Acting”也不够？

另一端是纯 Action policy：

```text
看到状态
↓
直接输出 Tool Call
```

这在简单确定性任务上可能足够。

但复杂长任务中，系统还需要：

```text
追踪当前目标
解释刚才结果
发现异常
更新计划
决定是否继续
判断何时停止
```

例如：

```text
search(query A)
↓
Observation: no result
```

如果没有 Reasoning 层，系统可能机械重复：

```text
search(query A)
search(query A)
search(query A)
```

而合理 reasoning 应该是：

```text
原 query 太具体，改用更宽泛关键词。
```

因此 Reasoning 的价值不仅是“把答案想得更深”，还包括：

> **解释 Observation、更新策略和协调长程行为。**

---

#### 2.3.8 ReAct 与 Agent Loop 的关系

这两个概念非常接近，但层级不同。

**Agent Loop** 是系统结构：

```text
State
→ Decision
→ Action
→ Observation
→ State Update
→ Termination
```

**ReAct** 是一种典型 Decision Policy：

```text
Reason about current state
→ choose Action
→ inspect Observation
→ reason again
```

所以：

```text
Agent Loop
= execution/control skeleton

ReAct
= reasoning–acting interleaving strategy inside the loop
```

Agent Loop 可以不使用 ReAct。

例如完全规则化系统：

```text
if error == timeout:
    retry()
```

就是 Agent Loop 中的 deterministic policy。

而 ReAct 通常依赖 LLM 对 Observation 进行语义解释，再动态决定下一步。

---

#### 2.3.9 ReAct 与 Tool Calling 的关系

Tool Calling 解决：

> **Action 怎样被结构化表达并交给系统执行？**

ReAct 解决：

> **Agent 怎样在 Reasoning 和 Environment Interaction 之间反复切换？**

例如：

```text
Reason:
需要查天气。

Action:
get_weather(city="Tokyo")
```

其中：

```text
“需要查天气”
→ ReAct 中的 reasoning / decision

get_weather(...)
→ Tool Calling 表达的 Action
```

然后 Tool Result 作为 Observation 回来：

```text
{"temperature": 18, "rain": true}
```

ReAct 再决定下一步。

所以：

```text
Tool Calling
= Action Interface

ReAct
= Action 何时发生、为什么发生、结果怎样改变后续决策的循环策略
```

---

#### 2.3.10 ReAct 与 Chain-of-Thought 的关系

可以把差异压缩成：

```text
CoT:
Question
↓
Reasoning
↓
Answer

ReAct:
Question / Goal
↓
Reasoning
↓
Action
↓
Observation
↓
Reasoning
↓
Action
↓
...
↓
Answer
```

CoT 的信息源主要来自已有 Context。

ReAct 则可以通过 Action 主动引入新的 Observation。

因此：

> **CoT 扩展的是内部推理轨迹；ReAct 扩展的是内部推理与外部环境交互组成的联合轨迹。**

这也是为什么 ReAct 更适合：

- Web / Search Agent；
- Coding Agent；
- Browser Agent；
- Database Agent；
- Tool-using Research Agent。

---

#### 2.3.11 ReAct 与 Plan-and-Execute 的关系

两者都在处理多步任务，但控制粒度不同。

ReAct 常见模式：

```text
Reason
→ one / few Actions
→ Observe
→ Reason again
```

它偏向 **local replanning**。

Plan-and-Execute 常见模式：

```text
Generate global plan
↓
Execute Step 1
↓
Execute Step 2
↓
...
```

必要时再 replan。

可以粗略理解：

```text
ReAct
= short-horizon feedback control

Plan-and-Execute
= explicit long-horizon decomposition + execution
```

但真实系统可以组合：

```text
High-level Plan
   ↓
Step 1
   ↓
ReAct locally
   ↓
Step 2
   ↓
ReAct locally
```

因此它们不是互斥方法。

---

#### 2.3.12 ReAct 最重要的价值：Observation Grounding

ReAct 真正是否成立，不看轨迹里有没有写：

```text
Thought:
```

而要看：

> **下一步决策是否被最新 Observation 约束。**

例如：

```text
Thought:
我要读取 config.json。

Action:
read_file(config.json)

Observation:
File not found.
```

下一步如果仍然：

```text
Thought:
很好，我已经读取了配置。
```

那么形式上有 Thought–Action–Observation，实际上 Observation 没有被 grounded。

真正的 ReAct 应该更新：

```text
Thought:
目标文件不存在，我需要搜索相似文件名或检查路径。

Action:
search_files("config")
```

所以：

```text
Observation present
≠
Observation used
```

这也是后面 Process Evaluation 的重要指标。

---

#### 2.3.13 Information-gathering Action：行动不一定是为了“完成任务”

ReAct 中一个非常重要的思想是：

> **Action 可以只是为了减少不确定性。**

例如：

```text
search
read
inspect
ask_user
run_test
zoom
open page
query status
```

它们未必直接完成目标，却改善 Agent 下一轮的决策条件。

可以把 Action 粗略分成：

```text
Epistemic / Information Action
→ 为了知道更多

World-changing Action
→ 为了改变环境
```

例如 Coding Agent：

```text
run_tests
read_file
search_symbol
```

属于信息获取；

```text
edit_file
commit
```

属于改变环境。

工程上通常应该允许 Agent 在不确定时优先执行低风险信息动作，而不是直接执行高风险世界修改。

---

#### 2.3.14 ReAct 的 Reasoning 不等于必须暴露完整 Chain-of-Thought

早期论文和教学示例经常把：

```text
Thought: ...
Action: ...
Observation: ...
```

全部显式打印。

但从系统设计角度：

> **ReAct 需要 reasoning function，不要求把全部内部推理文本公开给用户。**

现代系统完全可以采用：

```text
Internal reasoning / decision state
        ↓
Structured Action
        ↓
Observation
        ↓
Next internal decision
```

用户只看到：

```text
工具调用进度
必要解释
最终答案
```

甚至 reasoning 可以是更结构化的：

```json
{
  "need_external_information": true,
  "next_action": "search",
  "reason_code": "missing_current_fact"
}
```

而不是长篇自然语言 Thought。

因此不要把 ReAct 错误理解为：

> **“必须让模型输出一串可见 Thought。”**

---

#### 2.3.15 显式 Reasoning 什么时候仍然有价值？

虽然不要求暴露完整 CoT，但某种可审计决策状态仍然有价值。

例如：

```text
当前目标
当前假设
缺失信息
计划中的下一步
为什么选择这个 Tool
失败后为什么 retry
```

它们可以帮助：

- debugging；
- evaluation；
- human review；
- recovery；
- trajectory analysis。

所以更成熟的设计往往不是：

```text
full natural-language thought
```

而是：

```text
minimal structured rationale / decision metadata
```

例如：

```json
{
  "action": "search_web",
  "reason_code": "freshness_required",
  "evidence_gap": "current_price"
}
```

这样既保留可审计性，又避免把 Agent 内部控制完全建立在长篇自由文本 reasoning 上。

---

#### 2.3.16 ReAct 的粒度：是不是每一步都必须“想一下”？

不一定。

如果每一个微小动作都变成：

```text
LLM reason
↓
Tool call
↓
LLM reason
↓
Tool call
```

会带来巨大 latency 和 token cost。

例如需要读取三个彼此独立的文件：

```text
read A
read B
read C
```

如果模型已经确定三者都需要，可以一次发出多个并行 Action，而不是每读一个都重新 reasoning。

因此 ReAct 的真正设计问题是：

> **在哪些 Observation 边界上值得重新调用 Policy？**

常见策略：

```text
Action outcome highly uncertain
→ re-reason immediately

Actions independent and predictable
→ batch / parallelize

Environment high-risk
→ re-observe frequently

Deterministic subroutine
→ execute without LLM between every micro-step
```

这属于 Harness 的 Loop Policy。

---

#### 2.3.17 ReAct 与 Open-loop Planning 的根本区别

假设 Agent 一开始计划：

```text
1. 搜索论文
2. 打开论文
3. 摘要
4. 写答案
```

如果第 1 步实际得到：

```text
No results
```

Open-loop 仍可能机械进入：

```text
2. 打开论文
```

ReAct 则要求：

```text
Observation = no results
↓
Reason again
↓
change query / source / strategy
```

所以 ReAct 本质上更接近控制理论里的 feedback policy：

```text
plan
→ act
→ sense
→ correct
```

而不是：

```text
plan once
→ blindly execute
```

---

#### 2.3.18 ReAct 为什么能处理异常？

因为异常本身可以进入 Observation。

例如：

```text
Action:
open_url(...)

Observation:
403 Forbidden
```

下一轮 Reasoning 可以变成：

```text
这个来源不可访问，改找官方镜像或搜索同一标题。
```

再例如：

```text
Action:
run_test

Observation:
ModuleNotFoundError
```

Agent 可以判断：

```text
是代码 bug？
环境缺依赖？
还是测试配置错误？
```

所以异常不只是“失败”，而是：

> **改变后续策略的信息。**

这和上一节的 Agent Loop 错误语义完全一致。

---

#### 2.3.19 ReAct 与 Reflection 的区别

两者都可能出现“模型重新思考”，但关注点不同。

ReAct：

```text
Reason
→ Act
→ Observe
→ Reason again
```

主要由 Environment Feedback 驱动。

Reflection：

```text
Attempt
→ Critique own result / trajectory
→ identify error
→ revise
```

主要是对自己已有输出或过程进行再评价。

所以：

```text
ReAct
= environment-grounded iterative decision

Reflection
= self-evaluation / critique-driven revision
```

两者可以组合：

```text
Action fails
↓
Observation
↓
Reflection on why it failed
↓
new Action
```

但不能完全画等号。

---

#### 2.3.20 ReAct 与 Verification 的区别

ReAct 允许 Agent 根据 Observation 更新行为，但并不自动保证它会验证。

例如：

```text
edit_file
↓
Observation: write succeeded
↓
final answer
```

形式上是完整 ReAct。

但如果目标是修复 bug，真正可靠的流程还应该：

```text
run_tests
↓
Observation: tests pass
↓
check constraints
↓
finish
```

所以：

```text
ReAct
= iterative reasoning-action loop

Verification
= 判断结果是否满足 Goal / Constraint 的专门步骤
```

一个 ReAct Agent 完全可能“很会行动，但不验证结果”。

---

#### 2.3.21 一个 Research Agent 的完整 ReAct 例子

用户：

```text
某项政策目前是否已经正式生效？
```

Agent：

```text
Reason 1:
这是时效性事实，需要外部证据，优先找官方来源。

Action 1:
search_web(policy name + official)

Observation 1:
得到政府公告和若干媒体报道。

Reason 2:
媒体报道不是最强证据，先打开政府公告。

Action 2:
open(official_notice)

Observation 2:
公告说明法规发布日期，但写着未来某日生效。

Reason 3:
需要比较当前日期，并确认之后是否有修订或延期。

Action 3:
search_web(policy name + amendment + effective date)

Observation 3:
没有后续延期，官方实施页面显示已实施。

Reason 4:
证据闭环完成。

Final:
已正式生效，并给出生效日期和官方证据。
```

这里最关键的是：

```text
Observation_1
改变 Reason_2

Observation_2
改变 Reason_3
```

而不是预先写死三次搜索。

---

#### 2.3.22 一个 Coding Agent 的 ReAct 例子

用户：

```text
修复导致 unit test 失败的 bug，不要修改 public API。
```

可能轨迹：

```text
Reason 1:
先运行相关测试，观察真实失败。

Action 1:
run_tests(target)

Observation 1:
AssertionError in parser_test.py: expected 3, got 2

Reason 2:
需要检查 parser 以及失败 case。

Action 2:
read_file(parser.py)
read_file(parser_test.py)

Observation 2:
发现边界条件分支漏处理最后一个 token。

Reason 3:
做最小修复，避免改 public API。

Action 3:
edit_file(parser.py)

Observation 3:
patch applied

Reason 4:
必须验证局部测试和相关回归。

Action 4:
run_tests(parser tests)

Observation 4:
pass

Reason 5:
再运行较宽回归，确认没有副作用。

Action 5:
run_tests(relevant suite)

Observation 5:
pass

Final:
说明修改和验证结果。
```

这里 ReAct 的价值不在于“模型写了五段 Thought”，而在于：

```text
真实 test observation
→ 修改下一步决策
```

---

#### 2.3.23 常见 Failure Modes

**1. Reasoning Hallucination**

模型在 Reasoning 中假设了 Environment 中并不存在的事实。

例如：

```text
“既然测试已经通过……”
```

但实际上根本没有运行测试。

---

**2. Observation Ignored**

工具返回的信息与原计划冲突，但 Agent 仍沿原路径执行。

---

**3. Action–Observation Misalignment**

模型以为自己执行了 A，Runtime 实际执行的是 B，或 Tool Result 对应错 call_id。

---

**4. Tool Loop**

```text
search A
→ no useful result
→ search A
→ no useful result
→ search A
```

Reasoning 没有产生策略更新。

---

**5. Reasoning Loop**

模型不断重复：

```text
我需要进一步确认。
```

但没有选择新的有效 Action。

---

**6. Overthinking Before Acting**

明明可以通过一次低成本 Tool Call 获得事实，却在内部推理很久。

---

**7. Over-acting**

本来已有足够信息，却继续搜索、读取、调用工具。

---

**8. Premature Final Answer**

第一次 Observation 看起来合理，就提前结束，未满足真正 Success Criteria。

---

**9. Stale Observation**

Environment 已变化，Reasoning 仍基于旧 Tool Result / Screenshot / File Content。

---

**10. Context Accumulation**

每轮 Thought、Action、Observation 都完整保留，导致 Context 快速膨胀。

---

**11. Observation Injection**

网页、邮件、文件中的恶意文本被错误当成新的高优先级 Instruction。

---

**12. Incorrect Recovery**

Action 失败后模型机械 retry，而没有理解 error semantics 或 side effect。

---

**13. Hidden Progress Failure**

轨迹看起来很长，实际上没有产生新证据、没有减少不确定性、也没有接近 Goal。

---

**14. Action Without Verification**

世界修改成功不代表任务目标成功，例如“文件写入成功”不等于“bug 修复成功”。

---

#### 2.3.24 Harness 怎样控制 ReAct？

真正的 ReAct Agent 不是让模型无限自由：

```text
while true:
    think
    act
```

Harness 通常会控制：

```text
哪些 Tools 当前可见
哪些 Action 可以自动执行
哪些 Action 需要 approval
最多多少 Steps
哪些 error 可以 retry
什么时候 compact context
什么时候强制 verification
什么时候判断无进展
什么时候停止
```

因此：

```text
ReAct
= model-side decision pattern

Harness
= system-side control policy
```

一个可靠系统通常是：

```text
LLM proposes next Action
        ↓
Harness validates / constrains
        ↓
Runtime executes
        ↓
Observation
        ↓
Harness updates state/context
        ↓
LLM decides again
```

而不是模型独占整个循环控制权。

---

#### 2.3.25 ReAct 的 Stop Condition 为什么必须外置一部分？

如果完全让模型自己说：

```text
I am done.
```

就结束任务，会出现 premature termination。

成熟系统可以增加：

```text
model believes done
+
objective success checks
+
constraint checks
+
budget / policy state
```

例如 Coding Agent：

```text
Model: 修好了
```

Harness 仍可以要求：

```text
relevant tests passed?
no unauthorized files changed?
public API unchanged?
```

因此：

> **ReAct 决定“我下一步想做什么”；Termination Policy 决定“系统是否真的允许结束”。**

---

#### 2.3.26 ReAct 与 Cost / Latency 的 Trade-off

ReAct 的一个天然成本是：

```text
多轮模型调用
+
多轮 Tool round trip
+
不断增长的 Context
```

如果一次任务有 $N$ 个 reasoning-action cycles：

$$
L_{total}
\approx
\sum_{i=1}^{N} L_{model,i}
+
\sum_{i=1}^{N} L_{tool,i}
+
L_{orchestration}
$$

因此一个“更会反思、更会搜索”的 Agent 可能质量提高，但 latency 变得很差。

工程上常见优化：

```text
parallel independent tool calls
batch predictable actions
cache stable observations
compact old trajectory
use deterministic subroutines
skip unnecessary model turns
apply early exit
```

所以 ReAct 不意味着：

> **每一个最小动作前都必须重新调用一次 LLM。**

---

#### 2.3.27 如何判断 ReAct 是否真的在“进展”？

可以定义 Progress Signal。

例如：

```text
new evidence acquired?
uncertainty reduced?
subgoal completed?
verification coverage increased?
error state changed?
remaining plan shortened?
```

如果连续多个 step：

```text
same query
same result
same uncertainty
same subgoal
```

那么即使 token 和 tool calls 持续增加，也可能是：

```text
no progress
```

Harness 可以触发：

```text
replan
fallback
ask_user
stop
```

这和 2.2 中的 Progress Signal 直接衔接。

---

#### 2.3.28 ReAct Trajectory 应该怎样评测？

只看 final answer 不够。

至少可以拆成几个维度：

```text
1. Reasoning relevance
2. Tool / Action selection
3. Argument correctness
4. Observation grounding
5. Recovery quality
6. Verification behavior
7. Termination correctness
8. Efficiency
```

例如：

##### Action Selection

```text
当前状态是否真的需要这个 Tool？
是否有更直接、更低风险的 Action？
```

##### Observation Grounding

```text
下一步有没有利用刚刚获得的信息？
```

##### Recovery

```text
失败后是否改变策略，而不是盲目重复？
```

##### Efficiency

```text
是否存在无效 search / repeated read / redundant reasoning？
```

因此 ReAct Evaluation 天然适合 trajectory-level analysis。

---

#### 2.3.29 ReAct 的数据价值

一条高质量 ReAct trajectory 不只是最终答案数据。

它包含：

```text
State
Reasoning / Decision
Action
Observation
State Update
Termination
```

因此可以用于：

- Tool-use SFT；
- Action prediction；
- Process supervision；
- Failure analysis；
- Tool-selection evaluation；
- Recovery policy learning；
- Agent trajectory modeling。

但如果轨迹中 Thought 是后补的解释，而不是当时真实决策依据，就要注意：

> **post-hoc rationale 不一定等于 causal decision process。**

所以 Agent 数据设计需要记录真实 Action / Observation lineage，而不能只保存一段“看起来很合理”的自然语言解释。

---

#### 2.3.30 ReAct 设计原则

**原则一：Reasoning 必须服务于 Action。**

如果 reasoning 很长，却不改变下一步行为，只是在重复解释，价值有限。

**原则二：Action 必须产生可消费的 Observation。**

调用工具后要确保结果被正确关联到后续 Context。

**原则三：Observation 必须真正进入下一轮决策。**

存在日志里不等于被 Agent 使用。

**原则四：信息动作优先于高风险修改。**

不确定时先 search / inspect / verify，再 write / send / delete。

**原则五：低级确定性步骤不要全部交给 LLM。**

能由程序稳定处理的 parsing、retry guard、permission、state update，应由 Harness 完成。

**原则六：ReAct 必须有 Stop / Budget Guard。**

否则极容易形成 reasoning loop 和 tool loop。

**原则七：失败 Observation 要改变策略。**

如果 retry 后还是原样 action，就说明没有真正闭环。

**原则八：不要把可见 CoT 当成 ReAct 的必要条件。**

关键是 reasoning–action–observation 的因果循环。

**原则九：Final Answer 前要检查 Completion Criteria。**

行动完成不等于任务完成。

**原则十：评价 ReAct 要看 Quality–Cost–Latency。**

更长轨迹并不天然更好。

---

#### 2.3.31 与相邻概念的边界

| 概念 | 核心问题 | 与 ReAct 的关系 |
|---|---|---|
| Chain-of-Thought | 如何基于已有 Context 展开多步推理 | ReAct 在 reasoning 之间插入 Environment Action / Observation |
| Tool Calling | 如何结构化表达 Tool Action | ReAct 中 Action 的常见接口 |
| Agent Loop | State–Decision–Action–Observation 的系统闭环 | ReAct 是其中一种典型 Decision Policy |
| Planning | 怎样形成未来多步行动结构 | ReAct 常做短程动态 replanning |
| Plan-and-Execute | 先形成较长计划再执行 | 可与 ReAct 的局部反馈控制组合 |
| Reflection | 对自己已有结果或轨迹做 critique | 可嵌入 ReAct，但不是同义词 |
| Verification | 检查目标与约束是否真正满足 | ReAct 不自动保证 verification |
| Harness | 控制 Tools、Context、Budget、Permissions、Loop | 约束并执行 ReAct policy |
| Runtime | 真正执行 Action | 产生 Observation |
| Observation | 环境反馈 | ReAct 后续 Reasoning 的关键输入 |
| Workflow | 预定义控制流 | 可包围 ReAct，只把不确定节点交给 Agent |

---

#### 2.3.32 面试掌握边界

这一节至少需要稳定回答：

1. **ReAct 是什么？**  
   一种把 Reasoning 与 Environment Action 交错起来的 Agent 决策模式：reason → act → observe → reason again。

2. **ReAct 为什么比纯 CoT 更适合 Agent？**  
   CoT 只能基于已有 Context 推理；ReAct 可以通过 Tool / Environment Action 主动获得新 Observation，并据此更新后续决策。

3. **ReAct 和 Tool Calling 有什么区别？**  
   Tool Calling 是 Action 的结构化接口；ReAct 是 Reasoning、Action、Observation 如何反复组织起来的策略。

4. **ReAct 和 Agent Loop 有什么区别？**  
   Agent Loop 是系统级 State–Decision–Action–Observation skeleton；ReAct 是 Decision 层常见的 reasoning–acting policy。

5. **ReAct 是否必须输出 `Thought:`？**  
   不必须。Thought / Action / Observation 首先是逻辑角色；真实系统可以使用隐藏 reasoning 或结构化 decision state。

6. **ReAct 和 Plan-and-Execute 有什么区别？**  
   ReAct 更偏短程、每次观察后动态调整；Plan-and-Execute 更偏先做显式全局分解再逐步执行，两者可以组合。

7. **为什么 Observation Grounding 很重要？**  
   因为工具结果只有真正改变下一步 Policy 才有价值；“收到了 Observation”不等于“用到了 Observation”。

8. **ReAct 常见失败模式有哪些？**  
   Observation ignored、tool loop、reasoning loop、wrong tool、stale observation、premature final、over-acting、缺少 verification 等。

9. **为什么 ReAct 可能很慢？**  
   多轮 model–tool round trip 会累积 token、network、tool 和 inference latency；并非每个微动作都值得重新调用模型。

10. **怎么控制 ReAct 不无限循环？**  
    Harness 设置 max steps、budget、progress detection、retry policy、termination checks 和 fallback。

11. **ReAct 和 Reflection 是一回事吗？**  
    不是。ReAct 主要根据 Environment Observation 更新下一步；Reflection 主要对自身结果或轨迹做 critique 和 revision。

12. **怎样判断一条 ReAct trajectory 好不好？**  
    不只看 final answer，还要看 action selection、observation grounding、recovery、verification、termination、cost 和 latency。

13. **ReAct 最核心的一句话是什么？**  
    Reasoning 决定该怎样行动，而 Action 获得的 Observation 又必须真实改变下一步 Reasoning。

如果继续追问“什么时候应该先做全局计划、任务怎样拆成子任务、执行过程中什么时候 replan”，进入下一节 **2.4 Planning**；如果追问失败后如何自我批评，则进入 **2.5 Reflection / Critique**；如果追问怎样证明任务真的完成，则进入 **2.6 Verification**。

---

#### 2.3.33 本节一句话总结

> **ReAct 的本质不是一个带 `Thought / Action / Observation` 标签的 Prompt，而是一种基于反馈的决策结构：Agent 用 Reasoning 解释当前状态并选择 Action，用 Action 从 Environment 获得新的 Observation，再让 Observation 真正改变下一步 Reasoning；它因此把 LLM 的内部推理能力连接成了可与真实环境闭环交互的 Agent Policy。**

#### 2.3.34 参考资料

- Yao S, Zhao J, Yu D, et al. **ReAct: Synergizing Reasoning and Acting in Language Models**. arXiv:2210.03629, 2022；发表于 ICLR 2023。
- 原始工作重点实验覆盖知识型问答 / 事实核验任务（HotpotQA、FEVER）以及交互式决策任务（ALFWorld、WebShop），核心贡献是让 reasoning traces 与 task-specific actions 交错生成，并利用外部 Observation 持续更新决策。
