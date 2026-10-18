# LLM / Agent Data Figure Presentation Kit

> 状态：`Stable Mother Edition V3.x / Presentation Layer`
>
> 目标：把 Level A Master Figures 从“能看懂”推进成“能在面试、组会、答辩、分享里稳定讲清楚”。
>
> Semantic Source：[`Master Figure System`](./00_Master_Figure_System.md)
>
> Visual Contract：[`Figure Design Contract`](./00_Figure_Design_Contract.md)
>
> 原则：**Talk Track 可以因场景压缩，但不能改变 Master Figure 的 canonical relation。**

---

# 0. 使用规则

Level A 六张图：

```text
F1  Learning System
F4  Agent Task–Environment–Trajectory
F6  Credit → Failure
F8  Evaluation Protocol
F9  Data Flywheel
F14 Operating Model + Capability Map
```

每张图提供：

```text
One-sentence Thesis
30-second Track
90-second Track
Progressive Reveal
Common Misread
Best Use Cases
```

不要在一次汇报里机械展示六张。

推荐按问题选图：

```text
“你怎么看 LLM / Agent Data？”
→ F1

“Agent 系统为什么不能只看对话？”
→ F4

“bad case 怎么诊断？”
→ F6

“怎么证明一个方案真的更好？”
→ F8

“数据闭环怎么运转？”
→ F9

“团队 / 个人怎么落地？”
→ F14
```

---

# 1. F1 — Learning System Overview

[打开 F1](./figures/F1_Learning_System_Overview.md)

## One-sentence Thesis

> **LLM / Agent Data 工作不是“做训练集”，而是在真实目标、经验、证据、学习信号、训练、部署和反馈之间维护一个可验证的 Learning System。**

## 30-second Track

```text
我会把 LLM / Agent Data 看成一个闭环，而不是数据流水线。
真实问题先被定义成 capability / task；系统从 human、synthetic、rollout、production 获取 experience；
然后必须先用 environment truth / verifier / judge / human 判断发生了什么，才能构造 SFT、preference、reward 或 process signal。
这些 signal 改变 model / policy，再部署回真实世界。
最重要的三个边界是：Experience ≠ Learning Signal，Evidence ≠ Label，Production Log ≠ Training Data。
```

## 90-second Track

先指出传统误区：

```text
Collect Data
→ Clean
→ Train
```

然后解释完整链：

```text
Real Problem
→ Capability Definition
→ Experience Acquisition
→ Experience Object
→ Evidence / Evaluation
→ Learning Signal
→ Training / Optimization
→ Deployment
→ Outcome / Failure / Drift
↺
```

最后强调：

```text
不是所有 failure 都是 Data Problem；
不是所有 log 都值得训练；
不是所有 evaluator output 都是 truth。
```

## Progressive Reveal

```text
1. Real Problem → Capability
2. + Experience Acquisition
3. + Evidence / Evaluation
4. + Learning Signal / Training
5. + Deployment / Feedback loop
6. 最后再展开 Human / Synthetic / Verifier / Preference 等旁支
```

不要一开始把全部旁支都放出来，否则读者只会看到“复杂”。

## Common Misread

错误讲法：

```text
“F1 就是一个训练 pipeline。”
```

正确讲法：

```text
F1 是 Learning System；
Training 只是其中一环。
```

## Best Use Cases

```text
岗位面试开场
项目 framing
团队 shared mental model
整本书导读
```

---

# 2. F4 — Agent Task–Environment–Trajectory

[打开 F4](./figures/F4_Agent_Task_Environment_Trajectory.md)

## One-sentence Thesis

> **Agent 不是“模型 + Tool Call”；Task、Case、Harness、Tool、Environment、Observation、Agent-visible State 和 Trajectory 必须分层。**

## 30-second Track

```text
Task 规定应该完成什么；Case 冻结这一次具体世界；Model 不直接操作世界，而是经过 Harness 调 Tool，Tool 改变 Environment / World State，再把 Observation 返回。
Trajectory 不是聊天文本，而是这次 Episode 的执行证据。
因此 World State ≠ Observation，Observation ≠ Agent-visible State，Tool ≠ Harness ≠ Environment。
```

## 90-second Track

用 `C1-VB`：

```text
Task:
shipped → 不退款

World State:
status = shipped

Tool:
get_order_status

Observation:
shipped

Agent-visible State:
包含这个 observation 的当前 context

Decision:
应该 stop write path
```

如果最终仍退款，不能只说：

```text
“模型错了。”
```

还要看：

```text
Observation 是否真实进入 context？
Harness 是否翻译正确？
Tool 是否执行了预期动作？
World State 最后发生什么？
```

## Progressive Reveal

```text
1. Task / Case
2. Model / Harness
3. Action / Tool / Environment
4. World State → Observation → Agent-visible State
5. 最后加入 Trajectory / Outcome / Verifier
```

## Common Misread

```text
Tool result = Observation
```

不一定。

Harness 可能：

```text
parse
truncate
transform
inject
mis-map
```

所以 Tool Truth 和 Agent-visible Observation 必须分开记录。

## Best Use Cases

```text
Agent 系统设计
Trajectory Data 面试
Tool-use 失败归因
Harness / Environment 讨论
```

---

# 3. F6 — Credit → Failure Causal Map

[打开 F6](./figures/F6_Credit_to_Failure_Causal_Map.md)

## One-sentence Thesis

> **“最后失败了”不是 Diagnosis；必须继续拆到 First Error、First Harmful Action、Last Recoverable State、Root Cause 和 Failure Owner。**

## 30-second Track

```text
Outcome 只能告诉我们结果不好。
Credit Assignment 先问哪个 decision 真正改变了结果；Failure Diagnosis 再问为什么会做出这个 decision、根因属于谁。
所以 First Error ≠ First Harmful Action ≠ Root Cause，Failure Layer 也不一定等于 Failure Owner。
```

## 90-second Track

先用 C1：

```text
看到 shipped
→ 没有应用 stop condition
→ refund_order
```

可得到：

```text
First Error
= 没把 shipped 映射成 stop

First Harmful
= refund_order

Last Recoverable
= write 前
```

再用 C3-F5：

```text
Tool backend = failure
Harness observation = success
Agent reports success
```

表面 symptom 在 Agent 输出层，真正 owner 却是 Harness。

由此得到：

> **Failure Layer ≠ Failure Owner。**

## Progressive Reveal

```text
1. Outcome → First Error → First Harmful
2. + Last Recoverable / Point of No Return
3. + Symptom / Mechanism / Root Cause
4. + Failure Owner
5. 最后再接 Intervention Routing / Learning Signal
```

## Common Misread

错误：

```text
看到 bad final answer
→ 直接生成 correction SFT
```

正确：

```text
先判断是不是 Model-owned failure。
```

## Best Use Cases

```text
Bad-case analysis
Agent Evaluation
Failure Taxonomy
Data Problem Gate
```

---

# 4. F8 — Benchmark / Evaluation Protocol

[打开 F8](./figures/F8_Benchmark_Evaluation_Protocol.md)

## One-sentence Thesis

> **“方法更好”不是一个分数，而是 Benchmark Object、Frozen Protocol、Paired / Matched Run、Cost 和 Claim Scope 共同成立。**

## 30-second Track

```text
我会把 Benchmark、Protocol、Run、Report 分开。
Benchmark 决定测什么；Protocol 决定怎么跑、怎么判；Run 是一次具体执行；Report 才是统计结论。
如果是 selective / routing 系统，还必须保留 Full / Eligible / Triggered / Intervened population；否则 triggered subset 的高分不能冒充 E2E improvement。
```

## 90-second Track

先定义：

```text
Scientific Question
→ Capability
→ Benchmark
→ Protocol
```

Protocol 冻结：

```text
Model / Prompt / Tool / Harness / Environment
Budget / Stop Rule
Evaluator / Label Version
Seed / Repetition
```

再做：

```text
Baseline vs Treatment
→ Paired / Matched Analysis
```

不只看平均 accuracy，还看：

```text
Rescue
Harmful
Coverage
Cost
Latency
Failure Transition
```

最后才写 Claim Scope：

```text
Observed under this benchmark / protocol
≠ Universal improvement
```

## Progressive Reveal

```text
1. Question → Benchmark → Protocol
2. + Baseline / Treatment
3. + Paired / Matched
4. + Metrics / Cost
5. + Uncertainty / Claim Scope
```

## Common Misread

```text
“Treatment +1.2pt，所以方法有效。”
```

缺少：

```text
same budget?
paired cases?
variance?
regression?
multiple configurations tried?
```

## Best Use Cases

```text
研究方案设计
Benchmark 面试
实验 review
方法论文答辩
```

---

# 5. F9 — Data Flywheel

[打开 F9](./figures/F9_Data_Flywheel.md)

## One-sentence Thesis

> **真正的 Data Flywheel 不是“收 bad case → 加训练”，而是 Reality → Diagnosis → Capability Gap → Data / Other Intervention → Controlled Validation → Deploy → Learn Again。**

## 30-second Track

```text
线上 failure 只是 signal，不是 training example。
先 Triage 和 Root Cause，确认是不是 Data Problem，再抽象 capability gap，选择 acquisition / supervision / curation，做 controlled experiment；有效才规模化、部署和监控。
Flywheel 的关键不是数据越来越多，而是现实问题越来越快被路由到正确 intervention。
```

## 90-second Track

用 C1：

```text
shipped 订单仍退款
```

不能直接：

```text
加入 SFT
```

而是：

```text
verify failure
→ rule out Tool / Harness / Judge
→ capability = conditional constraint + observation grounding
→ build C1 family + transfer family
→ matched-budget experiment
→ regression
→ production
→ monitoring
```

如果 Root Cause 是 Tool / Harness：

```text
Flywheel 输出 = system fix
```

而不是 Data。

## Progressive Reveal

```text
1. Production → Signal → Triage
2. + Attribution → Capability Gap
3. + Acquire / Supervision / Curation
4. + Experiment / Train / Evaluate
5. + Deploy / Monitor / Loop Back
```

## Common Misread

```text
Data Flywheel = 自动不断采集新数据
```

错误。

正确的是：

```text
持续把现实变化转成可验证 intervention。
```

## Best Use Cases

```text
Data Strategy
Agent Data 平台设计
持续改进体系
团队 roadmap
```

---

# 6. F14 — Operating Model + Capability Map

[打开 F14](./figures/F14_Operating_Model_and_Capability_Map.md)

## One-sentence Thesis

> **成熟的 LLM / Agent Data 能力最终表现为：团队知道问题归谁、什么时候推进；个人知道拿到问题以后先问哪六件事。**

## 30-second Track

```text
F14 有两层：Organization OS 和 Practitioner OS。
组织层先做 Diagnosis Gate，把问题路由到 Product / Infra / Eval / Model / Data；任何 intervention 都必须经过 pilot 和 confirmatory evaluation，再决定 scale / revise / stop。
个人层则用八域能力和六个根问题快速定位当前缺口。
```

## 90-second Track

组织层：

```text
Problem
→ Diagnosis
→ Correct Owner
→ Pilot
→ Confirmatory Eval
→ Scale / Revise / Stop
→ Deploy / Monitor
```

个人层：

```text
Problem Framing
Data Object & Supervision
Acquisition
State / Trajectory
Evaluation / Diagnosis
Curation / Optimization
Production / Governance
Monitoring
```

最后用六问收束：

```text
1. What should the model learn?
2. From what experience?
3. With what feedback?
4. How do we know it learned?
5. Is it worth the cost?
6. When should the system learn again?
```

## Progressive Reveal

建议不要同时展示两张子图。

先：

```text
Organization OS
```

再切：

```text
Practitioner Capability Map
```

最后才出现六问。

## Common Misread

```text
“所有 AI 问题最后都应该落到 Data Team。”
```

恰好相反。

F14 第一层就是：

> **先确认谁才是正确 Owner。**

## Best Use Cases

```text
面试总结
团队协作
项目立项
答辩结尾
整本书收束
```

---

# 7. 推荐组合

## 5 分钟岗位面试

```text
F1
→ F6
→ F8
→ F14
```

讲法：

```text
我怎么看这个领域
→ 我怎么诊断问题
→ 我怎么证明方案
→ 我怎么落地
```

---

## 10 分钟 Agent Data 分享

```text
F1
→ F4
→ F6
→ F9
→ F14
```

讲法：

```text
Learning System
→ Agent World
→ Failure Causality
→ Data Loop
→ Operating Model
```

---

## 10 分钟研究 / Benchmark 分享

```text
F1
→ F3
→ F8
→ F9
```

讲法：

```text
总体系统
→ reasoning-state decision
→ scientific evaluation
→ feedback into learning
```

F3 是 Level B，但对 reasoning research 是必需图。

---

## 15 分钟完整框架

```text
F1
→ F2 / F3
→ F4
→ F6
→ F7 / F8
→ F9
→ F10 / F11
→ F12 / F13
→ F14
```

注意：

> 不要逐图“念图”。每张只承担一个转场问题。

---

# 8. Slide / Talk Discipline

## 一页只回答一个问题

```text
Good:
“为什么 Agent failure 不能直接变训练数据？”

Bad:
“Agent Data 全景图”里塞 30 个节点再逐个念。
```

## 先讲结论，再揭图

顺序：

```text
一句 Thesis
→ 显示主链
→ 给一个 Case
→ 点一个 Boundary
→ 进入下一问
```

## Case 不要换

同一段分享优先持续使用：

```text
C1
```

需要讲 ownership 时切到：

```text
C3-F5
```

需要讲 reasoning intervention 时切到：

```text
C4-SC
```

不要每页重新创造故事。

## 不用图证明数字

Master Figures 是概念关系图，不是 empirical chart。

实验数字应单独使用：

```text
result table
curve
error bars
paired transition table
```

不要混进 canonical concept figure。

---

# 9. 最终讲述链

整套 Presentation Kit 最终压成：

```text
F1
What system are we improving?
↓
F4
What actually happened in the agent world?
↓
F6
Why did it fail and who owns it?
↓
F8
How do we prove an intervention works?
↓
F9
How does evidence become the next learning opportunity?
↓
F14
How do teams and practitioners operate this continuously?
```

这六问就是 Level A Master Figures 最稳定的口头叙事顺序。
