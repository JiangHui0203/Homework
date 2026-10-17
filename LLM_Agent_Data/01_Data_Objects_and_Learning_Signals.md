# 第 1 章 Data Objects & Learning Signals：从 Sample 到 Experience

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 0 章 Overview`](./00_Overview.md)
>
> 关联章节：[`第 4 章 Reasoning Data`](./04_Reasoning_Data_and_Process_Supervision.md)、[`第 5 章 Agent Trajectory Data`](./05_Tool_Use_and_Agent_Trajectory_Data.md)、[`第 10 章 Agent Task Design`](./10_Agent_Task_Design.md)、[`第 12 章 Agent Trajectory Anatomy`](./12_Agent_Trajectory_Anatomy.md)、[`第 13 章 Credit Assignment`](./13_Task_Success_and_Credit_Assignment.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md)
>
> 本章定位：**全书基础对象与 Learning Signal 的 canonical entry chapter。它定义 Dataset / Sample / Task / Case / Episode / Trajectory，以及 Demonstration / Preference / Reward / Process / Environment Feedback 的基本关系；专业细节交给后续章节。**
>
> 本章核心问题：**现代 LLM / Agent Data 到底在记录什么对象，又通过什么形式把“经验”变成模型可学习的信号？**

---

# 1.0 从 Example 到 Experience

传统监督学习常把数据理解为：

```text
Input + Label
```

LLM Post-training 开始扩展为：

```text
Instruction + Response + Preference / Reward
```

Agent 又进一步扩展为：

```text
Task Case
+
Environment
+
Trajectory
+
Outcome
+
Feedback
```

所以现代大模型数据的核心对象已经从：

```text
Example
```

扩展为：

> **Experience。**

---

# 1.1 Dataset、Sample、Task、Case、Episode、Trajectory

这六个词应该严格区分。

## Dataset

一组数据对象的集合。

```text
Dataset
├── Sample 1
├── Sample 2
└── ...
```

Dataset 是容器概念，不规定内部对象必须是问答、轨迹还是 preference pair。

---

## Sample / Example

一个相对独立的数据记录。

普通 SFT：

```json
{
  "instruction": "解释什么是梯度下降",
  "response": "梯度下降是一种……"
}
```

Preference Data 则可能是一组：

```text
Context + Candidate A + Candidate B + Preference
```

所以 Sample 是**存储 / 数据集层面的实例**，不等于 Task。

---

## Task

Task 定义：

> **希望系统完成什么目标，以及任务层规则是什么。**

例如：

> “查订单 1847；如果还没发货就取消，否则不要修改。”

Task 并不要求有唯一标准文本答案。

完整 Task Contract 见第 10 章。

---

## Case

Case 是一个**冻结后的 Task 实例**。

通常至少绑定：

```text
Task Definition
Initial / Hidden Environment State
Tool / Permission Configuration
Relevant Runtime Conditions
Success / Verifier Contract
```

同一个 Task 模板：

```text
“未发货则取消”
```

可以有多个 Case：

```text
Case A: pending
Case B: shipped
Case C: cancelled
Case D: permission denied
```

所以：

```text
Task = 要解决哪类问题
Case = 这一次具体问题是什么
```

---

## Episode

Episode 是：

> **某个 Agent / Model 在某个 Case 上的一次完整运行。**

```text
Case
↓
Start Runtime
↓
Interaction / Actions
↓
Termination
```

同一个 Case 可以重复运行多次，产生多个 Episode。

---

## Trajectory / Trace

Trajectory 是：

> **Episode 中实际经过的状态、决策、动作、Observation 与终止路径。**

理论上常写：

\[
\tau=(s_0,a_0,o_1,s_1,a_1,o_2,\ldots,s_T)
\]

但真实 Agent 数据最好进一步表示成 typed event log，详见第 12 章。

因此完整关系是：

```text
Task
↓ instantiate
Case
↓ run
Episode
↓ realized path
Trajectory
```

---

# 1.2 为什么 Agent 时代不能只看 Final Response？

例如两个 Agent 最终都说：

```text
“已经帮你改好了。”
```

Agent A 真正执行：

```text
search_event
→ update_event
→ verify_event
```

Agent B 只执行：

```text
search_event
→ final claim
```

自然语言几乎一样，但：

```text
A = task completed
B = unsupported claim
```

因此 Agent 正确性需要结合：

```text
Executed Action
Tool / Environment Observation
Final Environment State
Constraints / Side Effects
```

而不能只评最终文字。

---

# 1.3 一条 Agent Data Record 常包含什么？

概念上至少包括：

```text
Task / Case Identity
Initial Environment State
Tool / Permission Contract
Runtime Version
Trajectory
Final Environment State
Final Response
Outcome Evidence
Labels / Rewards / Judgments
Cost
```

但要注意：

```text
Runtime Fact
```

和：

```text
Derived Label / Judge Score
```

不是一回事。

Trajectory representation 见第 12 章；Governance / Lineage 见第 19 章。

---

# 1.4 理解任何 Data Asset 的四个维度

## Source：从哪里来？

```text
Human-written
Expert
Production Log
Public Dataset
Synthetic Generator
Current-policy Rollout
Program / Environment
```

## Supervision：给了什么反馈？

```text
Demonstration
Preference
Reward
Process Label
Verifier Result
Environment Feedback
No explicit label
```

## Granularity：监督到哪一级？

```text
Token
Step / Decision
Response
Trajectory
Task / Episode
```

## Purpose：拿来做什么？

```text
Pretraining
SFT
Preference Optimization
Reward / Verifier Training
RL
Evaluation
Failure Analysis
Regression
Synthetic Seed
```

同一条 source experience 可以派生成多个 Dataset View。

---

# 1.5 Learning Signal 比“标签”更宽

## Demonstration / Imitation

告诉模型：

```text
在这种 context 下，可以这样做
```

典型用途：SFT。

## Preference

告诉模型：

```text
A 比 B 更符合目标
```

完整理论见第 3 章。

## Reward

一个人为设计或学习得到的优化信号：

```text
r(x,y) ∈ R
```

注意：

```text
Outcome ≠ Reward
```

完整区分见第 13 章。

## Process Supervision

对中间 state / decision / step 提供反馈。

详见第 4 章。

## Environment Feedback

例如：

```text
Tool Result
State Diff
Permission Error
Executable Test
```

这是世界对动作产生的 Evidence，不自动等于 Reward。

---

# 1.6 Outcome Supervision 与 Process Supervision

### Outcome Supervision

只判断最终结果：

```text
Task Success / Failure
Final Answer Correct / Wrong
```

优势：便宜、容易规模化。

局限：很难回答中间哪一步造成结果。

### Process Supervision

评价：

```text
state
→ decision
→ action
```

中的局部行为。

优势：可以定位错误、构造 recovery / preference / step-level supervision。

局限：需要定义 segmentation、局部正确性和多路径等问题。

所以：

```text
Outcome
告诉我们最终发生了什么

Process
帮助解释中间发生了什么
```

Credit Assignment 则进一步回答最终 Outcome 应该归因给哪些中间 Decision，见第 13 章。

---

# 1.7 Training-oriented Data 与 Evaluation-oriented Data

### Training-oriented

目标是：

```text
改变模型行为
```

### Evaluation-oriented

目标是：

```text
测量模型行为
```

二者可以来自同一类原始经验，但必须保持用途和 split 边界。

一个成熟闭环通常是：

```text
Eval / Production Failure
↓
Mining / Diagnosis
↓
Derived Training Data
↓
New Model
↓
Independent Eval
```

而不是把同一个 hidden eval case 直接训练后再原题证明提升。

---

# 1.8 State、Action、Observation：这里只做最小定义

## State

本书以后尽量避免裸写 `State`。

根据语境使用：

```text
World State
Environment State
Agent-visible State
Reasoning State
Working State
```

完整定义见第 4、11、12 章。

## Action

Agent 对环境或运行过程采取的操作，例如：

```text
Tool Call
Ask User
Wait
Abort
Verify
Final Response
```

## Observation

Agent 从环境、工具、用户或其他 actor 得到的新信息。

```text
Action
→ Environment Transition
→ Observation
```

Observation 不是 World State 本身。

---

# 1.9 Outcome、Reward、Credit 必须区分

本章只做入口定义：

```text
Outcome
世界实际发生了什么

Reward
人为设计的优化信号

Credit
Outcome / Reward 应归因给哪些中间 decision
```

完整理论统一见第 13 章。

这是全书非常重要的一条术语纪律：

> **Outcome ≠ Reward ≠ Credit。**

---

# 1.10 Verifier、Grader、Judge 这里只做导航

```text
Verifier
检查客观 / 可执行条件

Grader
广义评价器

Judge
通常指需要解释性判断的 evaluator，常由 LLM 实现
```

完整定义与层级关系见第 15 章。

本章不再把它们和 Reward Model 混在基础词典里展开。

---

# 1.11 从 Example 到 Experience 的完整演化

```text
Pretraining
Token Sequence
↓
Instruction / SFT
Input → Desired Response
↓
Preference
Context + Alternatives + Relative Feedback
↓
Reasoning
State / Step / Process Feedback
↓
Agent
Task Case + Environment + Trajectory + Outcome + Feedback
```

这就是全书最基础的对象演化线。

---

# 1.12 Canonical Case C1：一个对象如何在不同层出现

Task：

> 如果订单 1847 还没发货就取消，已经发货就不要动。

可以表示为：

```text
Task
conditional cancellation

Case
order_1847.status = pending
permissions = normal

Episode
model_v17 在该 Case 上的一次运行

Trajectory
get_order → pending → cancel_order → success → verify

Outcome
order_1847.status = cancelled

Reward
可能被设计为 success=1, violation=0

Credit
哪些 decision 真正导致最终成功
```

同一个真实问题，就这样在不同数据层级上被表示。

---

# 1.13 常见误区

1. **Sample = Task。** Sample 是数据记录，Task 是目标定义。
2. **Task = Case。** Case 是 Task 的具体实例。
3. **Episode = Trajectory。** Episode 是一次运行，Trajectory 是实际路径表示。
4. **Agent Data = Final Response。** 必须包含执行 Evidence。
5. **Environment Feedback = Reward。** 前者是 Evidence，后者是优化信号。
6. **Outcome = Reward = Credit。** 三者完全不同。
7. **State 是一个统一对象。** 必须说明是哪一种 state。
8. **有标准答案的数据才有价值。** Preference、process、environment feedback 都可提供学习信号。
9. **同一份数据只能有一个用途。** Raw Experience 可以派生成多个 View。

---

# 1.14 本章关键词

| 术语 | 一句话定义 |
|---|---|
| Dataset | 一组数据对象的集合 |
| Sample | 一个数据记录实例 |
| Task | 要完成的目标与任务规则 |
| Case | 一个冻结的 Task 实例 |
| Episode | 某模型在某 Case 上的一次完整运行 |
| Trajectory | Episode 实际经过的执行路径 |
| Action | Agent 采取的操作 |
| Observation | Agent 收到的新环境反馈 |
| Outcome | 世界实际发生的最终结果 |
| Reward | 人为设计的优化信号 |
| Credit | 对中间 decision 的结果归因 |
| Learning Signal | 数据向模型提供的可学习反馈 |
| Demonstration | 值得模仿的行为示范 |
| Preference | 候选之间的相对优劣 |
| Process Supervision | 对中间过程提供监督 |
| Environment Feedback | 来自外部世界的执行证据 |

---

# 1.15 本章最终心智模型

```text
Task
定义要做什么
↓
Case
定义这一次具体世界
↓
Episode
系统真正运行一次
↓
Trajectory
记录它实际怎么走
↓
Outcome / Evidence
记录世界发生了什么
↓
Learning Signal
把经验转换成可学习反馈
```

一句话：

> **现代 LLM / Agent Data 的核心，不只是收集 Example，而是把任务、执行、结果和反馈组织成可学习、可评测、可复用的 Experience。**

下一章第 2 章继续回答：

> **这些不同类型的数据，分别在 Pretraining、SFT 与 Post-training 的什么阶段发挥作用？**