### 2.5 Reflection / Critique

#### 2.5.1 定义：Reflection 到底是什么？

在前面的 Agent Loop、ReAct 和 Planning 中，Agent 已经能够：

```text
观察环境
→ 做决策
→ 执行动作
→ 接收反馈
→ 更新计划
```

但仅仅“收到反馈”还不等于知道自己哪里做错了。

Reflection / Critique 进一步解决的是：

> **基于已有结果、轨迹和证据，对自己的决策、推理、计划或执行进行诊断，并形成可用于下一轮修正的反馈。**

一个最小闭环可以写成：

```text
Attempt
  ↓
Evidence / Outcome
  ↓
Critique
  ↓
Diagnosis
  ↓
Revision Target
  ↓
Repair
  ↓
Re-verify
```

因此 Reflection 不是简单的“再想一遍”，而是：

> **用新的证据重新解释刚才的行为，并把错误定位成可修复对象。**

---

#### 2.5.2 Critique 和 Reflection 有什么区别？

这两个词经常混用，可以采用一个实用区分：

**Critique** 更偏：

```text
指出哪里有问题
```

例如：

```text
答案引用了过期来源。
第二步没有验证文件是否存在。
计划遗漏了依赖安装。
```

**Reflection** 更偏：

```text
理解为什么会错，并形成下一步修正策略
```

例如：

```text
我把搜索结果摘要当成了一手证据；
后续应该先打开官方来源，再决定是否结束检索。
```

所以可以理解为：

```text
Critique
= error description

Reflection
= critique + causal interpretation + repair implication
```

但在很多论文和系统中两者不会严格区分，因此更重要的是看它是否真正产生了：

```text
actionable feedback
```

---

#### 2.5.3 Reflection 为什么需要 Evidence？

没有 Evidence 的 Reflection 很容易变成：

```text
“也许我哪里做得不够好。”
```

但没有任何事实依据。

有效 Reflection 应尽量基于：

```text
Tool Observation
Environment State
Verifier Result
Test Failure
Constraint Violation
Human Feedback
Reference Answer
Execution Trace
```

例如 Coding Agent：

```text
Attempt:
修改函数 parse_config()

Evidence:
pytest: 3 failed, 12 passed

Failure:
test_empty_config expected {}, got None
```

好的 Reflection：

```text
修改引入了 empty-config 回归；
问题集中在默认返回值，不需要推翻整个 patch。
```

差的 Reflection：

```text
“代码可能还有问题，我应该更加仔细。”
```

因此：

> **Reflection 的质量上限首先受 Evidence 质量限制。**

---

#### 2.5.4 一个形式化视角

设当前 Agent trajectory 为：

$$
\tau=(s_0,a_0,o_1,s_1,a_1,o_2,\ldots,s_T)
$$

执行后得到 evaluator / environment feedback：

$$
f = E(\tau)
$$

Reflection 可以看作一个函数：

$$
r = R(\tau,f,g,C)
$$

其中：

- $g$：Goal；
- $C$：Constraints；
- $f$：外部或内部评价信号；
- $r$：reflection / critique。

然后修正策略根据 $r$ 产生新的候选：

$$
\tau' \sim P(\tau'\mid \tau,r,f)
$$

关键点是：

> **Reflection 本身不是成功；它只是产生了一个新的控制信号。**

真正是否改进，还要由下一轮执行和 Verification 判断。

---

#### 2.5.5 Reflection、ReAct、Planning 的位置关系

可以把三者放在同一条控制链里：

```text
Planning
→ 我准备怎样完成任务？

ReAct
→ 根据当前 Observation，下一步怎样走？

Reflection
→ 刚才的尝试哪里有问题，为什么，应该怎样修？
```

因此：

```text
Planning
= prospective structure

ReAct
= online feedback control

Reflection
= retrospective diagnosis
```

三者可以组合：

```text
Plan
↓
ReAct execution
↓
Failure / weak outcome
↓
Reflection
↓
Plan repair / local repair
↓
continue
```

---

#### 2.5.6 Reflection 与 Verification 的根本区别

这是最重要的边界之一。

**Verification** 问：

```text
对不对？
完成了吗？
约束满足了吗？
```

**Reflection** 问：

```text
为什么没对？
哪里出了问题？
应该改哪一部分？
```

例如：

```text
Verifier:
FAIL — test_user_login failed
```

Reflection：

```text
失败来自 session token 没有在 refresh 后更新；
修复应该集中在 token state，而不是重写登录逻辑。
```

因此：

```text
Verification
= detect / judge

Reflection
= diagnose / explain / guide repair
```

一个 verifier 完全可以不给原因，只返回：

```text
PASS / FAIL
```

但 Reflection 如果没有诊断信息，就难以指导下一步。

---

#### 2.5.7 Reflection 与 Retry 的区别

Retry 是：

```text
再执行一次
```

Reflection 是：

```text
先判断为什么失败，再决定是否以及怎样重试
```

例如 API timeout：

```text
Retry:
call API again
```

可能就够了。

但如果：

```text
400 invalid_argument
```

无脑 retry 没意义。

此时需要：

```text
Critique:
argument schema mismatch

Reflection:
字段 user_id 应为 integer，但生成成了 email string

Repair:
regenerate arguments
```

所以：

> **Retry 是动作；Reflection 是决定修复方式的诊断过程之一。**

---

#### 2.5.8 Reflection 与 Replanning 的区别

Replanning 发生在：

```text
原计划已经不适合当前状态
```

Reflection 则可以只发现一个局部问题。

例如：

```text
Plan:
A → B → C → D
```

如果 B 的参数错了：

```text
Reflection
→ 修 B
→ 继续 C、D
```

不需要整个 replan。

如果 Observation 表明 A 的核心假设错误：

```text
Reflection
→ 原计划建立在错误前提上
→ Full Replan
```

因此常见层级是：

```text
local retry
<
local repair
<
plan repair
<
full replan
```

Reflection 的任务之一就是判断错误位于哪个层级。

---

#### 2.5.9 Reflection 与 Self-Correction 的区别

Self-Correction 是结果层概念：

> Agent 最终把自己的错误修正了。

Reflection 是可能促成 Self-Correction 的机制之一。

```text
Reflection
→ Repair Proposal
→ New Attempt
→ Verification
→ Correct
```

才构成真正 Self-Correction。

如果只是：

```text
“我之前可能错了。”
```

但最终答案仍错，就不能称为有效 self-correction。

所以：

```text
Reflection
≠
Self-Correction
```

更准确地说：

```text
Reflection
→ candidate feedback

Self-Correction
→ verified behavior improvement
```

---

#### 2.5.10 “再想一遍”为什么不一定有用？

一个常见做法是：

```text
Initial Answer
↓
“Please reflect and improve your answer.”
↓
Second Answer
```

问题在于，如果第二轮没有新的 Evidence：

```text
同一个模型
同一份错误信息
同一套错误假设
```

模型可能只是：

```text
把原错误说得更完整
随机改掉正确部分
产生另一种错误
```

因此有效 Reflection 更接近：

```text
Attempt
+
New Evidence / Explicit Criteria
+
Targeted Critique
+
Repair
```

而不是无条件增加一次 model call。

这和第一章的原则一致：

> **More Thinking Is Not Always Better。**

---

#### 2.5.11 Reflection 的三个层级：Outcome、Process、Strategy

Reflection 可以发生在不同层级。

##### Outcome-level Reflection

检查最终结果：

```text
答案是否遗漏关键事实？
代码是否通过测试？
任务是否完成？
```

##### Process-level Reflection

检查 trajectory：

```text
为什么用了错误工具？
为什么忽略 Observation？
为什么重复搜索？
```

##### Strategy-level Reflection

检查更高层方法：

```text
这个问题是不是根本不该继续搜索？
是否应该换数据源？
是否应该先澄清用户约束？
```

可以理解为：

```text
Outcome
→ 结果错在哪

Process
→ 路径错在哪

Strategy
→ 方法为什么不合适
```

复杂 Agent 往往需要区分这三个层级。

---

#### 2.5.12 Credit Assignment：错到底应该归因给哪一步？

长轨迹最大的困难之一是：

```text
最终失败
≠
最后一步一定错
```

例如：

```text
Step 1: 搜错公司
Step 2: 正确读取该公司年报
Step 3: 正确计算增长率
Step 4: 正确写答案
```

最终答案错，但真正错误发生在 Step 1。

Reflection 需要进行某种 **Credit Assignment**：

```text
Failure
↓
Which decision caused it?
↓
Which state / assumption became wrong first?
```

否则修复可能针对最后一步，而真正 root cause 未改变。

所以一个高质量 Reflection 常常包含：

```text
Symptom
Root Cause
Affected Steps
Repair Target
```

---

#### 2.5.13 Root Cause 和 Symptom 必须分开

例如：

```text
Symptom:
最终数字错了
```

可能的 Root Cause：

```text
取错年份
单位换算错
读取了二手来源
calculator 参数顺序错
```

再例如 Coding Agent：

```text
Symptom:
test failed

Root Cause:
mock setup stale
```

如果 Reflection 只描述 symptom：

```text
测试没通过
```

对修复帮助很弱。

更成熟的反馈应该接近：

```json
{
  "symptom": "test failed",
  "root_cause": "state not refreshed after write",
  "affected_step": 6,
  "repair_target": "state synchronization"
}
```

---

#### 2.5.14 Reflection 应该输出什么？

最差的 Reflection 输出是长篇自由文本，但没有明确修复对象。

一个更工程化的 Reflection schema 可以包含：

```json
{
  "failure_type": "observation_ignored",
  "evidence": "tool returned file_not_found",
  "root_cause": "agent assumed read succeeded",
  "affected_step": 4,
  "repair_scope": "local",
  "recommended_action": "search_files",
  "confidence": "high"
}
```

它的好处是：

- 可追踪；
- 可评估；
- 可供 Harness 路由；
- 可作为 training / trajectory data；
- 不依赖一段长自然语言才能解释。

因此：

> **Reflection 最终应该产生可执行的 correction signal。**

---

#### 2.5.15 谁来做 Reflection？Self-Critic 并不是唯一答案

最简单形式：

```text
同一个模型生成
↓
同一个模型 critique
```

但也可以使用：

```text
separate critic model
rule-based checker
verifier + LLM diagnosis
human reviewer
environment feedback
dedicated subagent
```

例如：

```text
pytest
→ deterministic failure evidence

LLM critic
→ explain likely root cause
```

这通常比完全让模型“凭感觉批评自己”更有 grounding。

所以：

> **Reflection 是系统功能，不要求由原 Answerer 自己完成。**

---

#### 2.5.16 Independent Critic 为什么有时更好？

同一个生成器常常共享原来的错误假设。

独立 Critic 可以提供：

```text
fresh context
不同 instruction
不同 model
不同 evidence view
专门 rubric
```

这可能降低：

```text
self-confirmation
anchoring
```

但代价是：

```text
extra model call
latency ↑
cost ↑
context transfer complexity ↑
critic itself may be wrong
```

因此不能简单认为：

```text
多一个 Critic
→ 一定更可靠
```

还必须评估 Critic 的 precision / recall 和实际净收益。

---

#### 2.5.17 Critic 也会错：Meta-Verification

假设 Critic 说：

```text
你的答案错在公式使用错误。
```

但实际上原公式正确。

如果 Agent 无条件服从 Critic，可能出现：

```text
Right → Wrong
```

所以 Reflection 系统本身也需要验证。

一种结构：

```text
Attempt
↓
Critic
↓
Revision
↓
Verifier
↓
accept / reject revision
```

这非常重要：

> **Critique 是 hypothesis，不是 ground truth。**

最终是否采用修订，最好由更强的外部证据判断。

---

#### 2.5.18 Positive Reflection：不是只有失败才需要总结

Reflection 也可以用于成功轨迹：

```text
为什么这次成功？
哪些步骤真正关键？
哪些动作其实多余？
哪些策略值得以后复用？
```

这类信息可以形成：

```text
procedural memory
skill
successful pattern
```

例如：

```text
“处理实时政策问题时，先定位官方来源，再核对生效日期，避免从新闻摘要直接下结论。”
```

这会在后面的 Experience Learning 中变成跨任务资产。

不过当前 2.5 讨论的 Reflection 仍主要属于：

> 当前 episode 内的诊断与修正。

是否持久保存到未来任务，是 Chapter 12 的问题。

---

#### 2.5.19 Reflection 与 Memory 的边界

Reflection 是：

```text
生成经验 / 诊断
```

Memory 是：

```text
保存并在未来取回这些经验
```

因此：

```text
Reflection
→ “这次为什么失败”

Memory
→ “以后还能不能记得这次为什么失败”
```

如果 reflection 只存在当前 Context：

```text
本轮修复后消失
```

仍然只是 inference-time self-refinement。

如果被写入长期 memory 并影响未来任务：

```text
开始进入 Experience Learning
```

这就是为什么 Reflection 不等于 RSI。

---

#### 2.5.20 Reflection 的触发策略：不是每一步都要 Critique

每一步都跑一次 Critic 会极其昂贵：

```text
Action
↓
Critic
↓
Action
↓
Critic
```

通常更合理的是 condition-triggered reflection。

例如：

```text
Verifier FAIL
Tool error
Repeated action detected
Low confidence
Plan deviation
Constraint violation
No progress
High-risk action before commit
Final answer before submission
```

即：

> **只有当 Reflection 的期望价值足以覆盖额外成本时才触发。**

这本质上又回到 budget allocation。

---

#### 2.5.21 Before-Action Critique 与 After-Action Reflection

Critique 不一定只能发生在失败之后。

**Before Action**：

```text
Proposed high-risk action
↓
Critique / review
↓
approve / revise / reject
```

例如：

```text
send_email
payment
delete_file
production deploy
```

**After Action**：

```text
Outcome
↓
Reflection
↓
repair
```

所以 Critique 可以既是：

```text
preventive control
```

也可以是：

```text
corrective control
```

但涉及权限和不可逆操作时，真正的硬阻断仍应由 Harness / Permission Policy 完成，而不能只靠 Critic 文本建议。

---

#### 2.5.22 Reflection Loop 为什么必须有限？

如果没有硬限制：

```text
Answer
→ Critique
→ Revise
→ Critique
→ Revise
→ ...
```

可能永远不结束。

尤其模型可能不断发现：

```text
“还可以更清楚一些”
```

但任务质量不再实质提高。

因此需要：

```text
max_reflection_rounds
improvement threshold
budget limit
verifier pass
no-new-error criterion
```

例如：

```text
Revision accepted only if verifier score improves
```

或者：

```text
no measurable gain
→ stop
```

所以：

> **Reflection 也必须有 Termination Policy。**

---

#### 2.5.23 Reflection 如何影响 Harness？

Harness 可以把 Reflection 当成一种 control module：

```text
trajectory / outcome
      ↓
reflection trigger
      ↓
critic
      ↓
structured diagnosis
      ↓
Harness routes repair
```

例如：

```text
failure_type = invalid_arguments
→ regenerate tool args

failure_type = stale_plan
→ replan

failure_type = missing_permission
→ ask approval

failure_type = insufficient_evidence
→ retrieve more information
```

因此 Reflection 的价值不只是给模型看一段“自我总结”，而是：

> **为 Harness 提供错误分类和恢复路由信号。**

---

#### 2.5.24 一个 Reflection-aware Agent Loop

```python
state = initialize(task)

while not terminal(state):
    action = policy(build_context(state))
    result = runtime.execute(action)
    state = update_state(state, action, result)

    verdict = verifier(state)

    if verdict.failed:
        critique = critic(
            trajectory=state.trajectory,
            evidence=verdict.evidence,
            goal=state.goal,
        )

        repair = route_repair(critique)
        state = apply_repair_policy(state, repair)
        continue

    if verdict.success:
        return finalize(state)
```

真正核心是：

```text
Verifier
→ detect failure

Critic / Reflection
→ diagnose failure

Harness
→ choose repair mechanism
```

这三者职责不同。

---

#### 2.5.25 Research Agent 示例

任务：

```text
判断某政策是否已经正式生效。
```

Agent 初始轨迹：

```text
Search news
↓
Read media article
↓
Answer: 已生效
```

Verifier / review 发现：

```text
没有官方来源
```

差的 Reflection：

```text
“我应该更加谨慎。”
```

好的 Reflection：

```text
Symptom:
结论缺少一手证据。

Root cause:
把二手媒体摘要当成 authoritative source。

Repair target:
证据获取阶段。

Next action:
搜索政府官网 / 法规原文，并确认 effective date。
```

然后：

```text
Search official source
→ open regulation
→ confirm effective date
→ update answer
```

这才形成完整 self-correction。

---

#### 2.5.26 Coding Agent 示例

初始：

```text
Edit parser
↓
Run tests
↓
3 failures
```

Verifier evidence：

```text
test_empty_input failed
test_null_field failed
test_default_config failed
```

Reflection：

```text
三个失败共享同一模式：
默认值路径被这次 parser 重构破坏。

不是三个独立 bug，root cause 是 fallback branch 被删除。
```

Repair：

```text
恢复 fallback handling
```

再运行测试：

```text
0 failures
```

这说明 Reflection 真正做的是：

> **把多个 failure symptoms 压缩成更准确的 root-cause hypothesis。**

---

#### 2.5.27 常见 Failure Modes

**1. Generic Reflection**

```text
“我应该更仔细。”
```

没有 actionable repair。

**2. Evidence-free Critique**

没有新证据，只凭模型感觉找错。

**3. Wrong Root Cause**

发现 symptom，却归因到错误组件。

**4. Self-confirmation**

Critic 复述原模型假设，没有真正挑战。

**5. Overcorrection**

局部错误导致整套正确方案被推翻。

**6. Right-to-Wrong Revision**

原本正确，Critic 误判，revision 反而变差。

**7. Critic Hallucination**

Critic 引用了不存在的约束、错误日志或事实。

**8. Symptom Fixing**

只修最后表现，不修 root cause。

**9. Reflection Loop**

Critique / revise 无限循环。

**10. No Re-verification**

修改后没有再次验证，直接相信“已经修好”。

**11. Scope Mismatch**

应该 local repair，却 full replan；或者相反。

**12. Stale Evidence**

Reflection 使用旧 Observation，而 Environment 已变化。

**13. Critic–Executor Drift**

Critic 建议 A，但 Executor 实际修成 B。

**14. Constraint Blindness**

修正确性时破坏了成本、安全或用户约束。

**15. No Credit Assignment**

只知道最终失败，不知道最早错误步骤。

**16. Excessive Reflection**

简单可恢复错误也调用昂贵 Critic。

**17. Critique without Action**

诊断正确，但没有转成修复动作。

**18. Memory Pollution**

错误 Reflection 被长期保存，未来任务重复使用。

---

#### 2.5.28 Reflection 应该怎样评估？

不能只问：

```text
“这段 critique 写得像不像有道理？”
```

更应该看它是否真正帮助后续行为。

可以评估：

```text
Failure Detection Accuracy
Root-cause Accuracy
Repair Target Accuracy
Actionability
Revision Success Rate
Right→Wrong Rate
Wrong→Right Rate
Net Improvement
Extra Cost
Extra Latency
Reflection Rounds
```

一个非常重要的净收益指标是：

```text
Net Correction
= Wrong→Right - Right→Wrong
```

因为 Reflection 如果同时大量破坏原本正确案例，平均“看起来更会反思”没有意义。

---

#### 2.5.29 Outcome Eval 和 Reflection Eval 必须分开

假设 Agent 最终成功，但 Critique 本身很差，可能只是后续偶然修对。

也可能 Critique 正确，但 Executor 没有按建议执行。

所以至少要区分：

```text
Critique Quality
Repair Selection Quality
Execution Quality
Final Outcome
```

这对 credit assignment 很重要。

否则所有错误都被归给“reflection 不行”，无法知道真正应该优化哪里。

---

#### 2.5.30 Reflection Data 为什么有价值？

高质量 trajectory 不只包含：

```text
State
Action
Observation
```

还可以包含：

```text
Failure
Critique
Root Cause
Repair Decision
Revised Action
Verification Result
```

这种数据可以用于：

- error taxonomy；
- recovery policy；
- critic training；
- process evaluation；
- self-improvement research；
- skill / memory extraction。

尤其有价值的是：

```text
Attempt A failed
↓
Critique C
↓
Repair B
↓
Verifier passed
```

因为它明确记录了：

> 什么反馈真正把失败轨迹修成了成功轨迹。

---

#### 2.5.31 Reflection、Self-Refinement 与 RSI 的边界

这一节讨论的是当前 episode 内：

```text
Attempt
→ Reflection
→ Revision
```

即使 Agent 当前任务表现变好了，只要系统本身没有发生持久更新，就仍然属于：

```text
Inference-time Self-Refinement
```

如果 Reflection 被保存成 Memory / Skill：

```text
开始进入 Experience Learning
```

如果 Agent 根据这些反馈持续修改 Prompt、Tool Policy、Harness、Evaluator，形成：

```text
Agent_t
→ evaluate
→ modify agent
→ Agent_t+1
```

才进入 Agent Optimization / RSI。

因此：

> **Reflection 是 RSI 可以调用的机制，但普通 Reflection 本身不是 RSI。**

---

#### 2.5.32 工程设计原则

1. **Evidence before Reflection**：尽量先取得真实证据，再 critique。
2. **Detect 与 Diagnose 分离**：Verifier 判断是否错，Reflection 解释为什么错。
3. **Root Cause 优先**：不要只改 symptom。
4. **Structured Feedback**：输出 failure type、evidence、root cause、repair scope。
5. **Local Repair 优先**：能局部修复，不轻易 full replan。
6. **Revision 必须 Re-verify**：Critic 不是 ground truth。
7. **控制 Right→Wrong**：Reflection 不能只看 rescue，也要看 degradation。
8. **Condition-triggered Reflection**：不是每一步都反思。
9. **Bounded Loop**：限制 reflection rounds、cost、latency。
10. **Critic 也要 Eval**：评估 critic 的错误类型与净收益。
11. **高风险 Action 前可增加 preventive critique**，但权限仍由 Harness 强制。
12. **当前任务 Reflection 与长期 Memory 分开**，避免未经验证的经验污染长期状态。

---

#### 2.5.33 概念边界总表

| 概念 | 核心问题 | 主要输出 |
|---|---|---|
| ReAct | 现在根据 Observation 做什么？ | Next Action |
| Planning | 未来若干步怎样组织？ | Plan / Subgoals |
| Verification | 对不对、完成了吗？ | Verdict / Evidence |
| Critique | 哪里有问题？ | Error Description |
| Reflection | 为什么错、应该改哪里？ | Diagnosis / Repair Signal |
| Retry | 要不要再执行一次？ | Re-execution |
| Replanning | 原计划是否要改？ | New / Repaired Plan |
| Self-Correction | 错误最终是否被修正？ | Verified Improvement |
| Memory | 经验以后能否被取回？ | Persisted Experience |
| RSI | 系统自身是否递归更新？ | Agent_t → Agent_t+1 |

---

#### 2.5.34 面试掌握边界

至少应该能够回答：

1. **Reflection 是什么？**  
   基于结果、轨迹和证据，对失败进行诊断并形成可执行修复信号。

2. **Critique 和 Reflection 有什么区别？**  
   Critique 偏错误描述；Reflection 更强调 root cause 和 repair implication。

3. **Reflection 和 Verification 有什么区别？**  
   Verification 判断对错；Reflection 解释为什么错、改哪里。

4. **Reflection 和 Retry 是一回事吗？**  
   不是。Retry 是动作；Reflection 是决定如何修的诊断过程。

5. **Reflection 和 Replanning 的关系？**  
   Reflection 可以判断错误是否要求 local repair、plan repair 或 full replan。

6. **为什么“再想一遍”不一定有效？**  
   没有新 evidence 时，同一模型可能重复原错误或把正确答案改坏。

7. **Critic 能不能直接信？**  
   不能。Critique 是 hypothesis，revision 仍需 re-verification。

8. **如何防止 Reflection 无限循环？**  
   max rounds、budget、improvement threshold、verifier pass、no-progress termination。

9. **Reflection 应该怎样评估？**  
   看 root-cause accuracy、repair success、Wrong→Right、Right→Wrong、net gain、cost、latency。

10. **Reflection 等于 Self-Correction 吗？**  
    不等于。只有 reflection 导致 revision 且 verifier 证明确实变好，才是 self-correction。

11. **Reflection 等于 RSI 吗？**  
    不等于。当前 episode 内反思属于 inference-time self-refinement；只有系统被持久更新并递归参与下一轮改进，才进入 RSI。

12. **Reflection 最核心的一句话是什么？**  
    Reflection 不是“再想一遍”，而是基于 Evidence 做 root-cause diagnosis，并把诊断转成可验证的 repair signal。

如果继续追问“怎样证明修完以后真的正确、最终任务是否完成、哪些检查应该由 deterministic verifier / environment / model 完成”，进入下一节 **2.6 Verification**。

---

#### 2.5.35 本节一句话总结

> **Reflection / Critique 的本质不是让模型重复思考，而是把失败轨迹中的 Evidence 转化为可定位的错误诊断和可执行的修复信号；Verifier 负责发现问题，Reflection 负责解释问题，Harness 负责选择修复路径，而修复是否真的有效仍必须通过新的 Environment Feedback 与 Verification 证明。**

#### 2.5.36 参考资料

- Shinn N, Cassano F, Gopinath A, et al. **Reflexion: Language Agents with Verbal Reinforcement Learning**. NeurIPS 2023. 代表性思想是把环境反馈转化为语言形式的 reflection，并在后续尝试中使用。
- Madaan A, Tandon N, Gupta P, et al. **Self-Refine: Iterative Refinement with Self-Feedback**. NeurIPS 2023. 研究模型通过 feedback → refine 的迭代机制改进输出。
- Gou Z, Shao Z, Gong Y, et al. **CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing**. ICLR 2024. 强调借助外部工具反馈进行 critique，而不是完全依赖无证据的自我判断。
