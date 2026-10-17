# 1. 从 Sample 到 Trajectory：先理解“数据对象”

## 1.1 Dataset、Sample、Task、Episode、Trajectory 分别是什么？

这些词经常混用，但在 Agent 场景中最好区分。

### Dataset

一组数据对象的集合。

```text
Dataset
├── Sample 1
├── Sample 2
├── Sample 3
└── ...
```

例如 MATH、GSM8K、HumanEval 都可以看作 dataset。

---

### Sample / Example

一个相对独立的数据实例。

普通 SFT 中可能是：

```json
{
  "instruction": "解释什么是梯度下降",
  "response": "梯度下降是一种……"
}
```

此时 sample 基本就是一个 input-output pair。

---

### Task

Task 更强调：**希望模型完成什么目标。**

例如：

```text
“找到订单 #1847，并判断它是否满足退款条件。”
```

这里标准答案可能并不是一段固定文本，而是一个目标状态。

Agent 场景下，Task 往往比 Question 更合适，因为模型需要“做事”，而不只是“回答”。

---

### Episode

一次从任务开始到终止的完整执行过程。

```text
Task
 ↓
Agent starts
 ↓
interaction...
 ↓
Success / Failure / Timeout
```

强化学习与 Agent 环境中经常使用这个词。

---

### Trajectory / Trace

Agent 在一次 episode 中实际走过的路径。

可以抽象成：

$$
\tau = (s_0, a_0, o_1, s_1, a_1, o_2, \ldots, s_T)
$$

其中：

- $s_t$：当前状态 State；
- $a_t$：Agent 的动作 Action；
- $o_{t+1}$：环境返回的 Observation；
- $\tau$：完整 trajectory。

最直观的例子：

```text
Task:
“查一下订单 1847 是否发货，如果没发货就取消。”

State 0
↓
Action: search_order(id=1847)
↓
Observation: status = pending
↓
State 1
↓
Action: cancel_order(id=1847)
↓
Observation: cancellation_success = true
↓
Final response: “订单已取消。”
```

这里真正的数据不只是最终一句“订单已取消”，而是整条执行轨迹。

---

## 1.2 为什么 Agent 时代必须从“答案”升级到“轨迹”？

看下面两个 Agent：

### Agent A

```text
User: 把明天下午三点的会议改到周五下午三点。

Agent:
calendar.search(...)
calendar.update(...)

Final:
已经帮你改好了。
```

### Agent B

```text
User: 把明天下午三点的会议改到周五下午三点。

Agent:
calendar.search(...)

Final:
已经帮你改好了。
```

如果只看最终回答，两者几乎完全一样。

但真实任务结果完全不同：

```text
Agent A → task success
Agent B → task failure
```

因此：

> **Agent 的正确性不能仅由最终自然语言回答决定，而必须结合工具调用、环境状态变化和最终任务完成状态。**

这也是 Agent Data 与传统 instruction-response data 最重要的区别之一。

---

## 1.3 一条 Agent 数据通常包含哪些字段？

一个较完整的 Agent sample 可能包含：

```text
Task
├── Initial Environment State
├── Available Tools
│   ├── tool name
│   ├── tool description
│   └── argument schema
│
├── Trajectory
│   ├── model message
│   ├── tool call
│   ├── tool arguments
│   ├── tool result / observation
│   └── repeated...
│
├── Final Response
│
├── Final Environment State
│
└── Labels / Rewards
    ├── task_success
    ├── tool_correctness
    ├── policy_violation
    ├── efficiency
    └── grader_feedback
```

因此 Agent 数据天然比普通问答数据更结构化。

---

## 1.4 数据的四个基本维度

理解任何一种大模型数据，都可以先问四个问题。

### 维度一：Source —— 数据从哪里来？

```text
Human-written
真实用户日志
专家编写
公开数据集
模型生成 Synthetic Data
模型 Rollout
多模型互评
环境自动生成
```

### 维度二：Supervision —— 给了什么监督信号？

```text
正确答案
示范轨迹
A > B 偏好
标量 Reward
步骤级标签
Verifier 结果
环境成功 / 失败
无标签数据
```

### 维度三：Granularity —— 监督到哪一级？

```text
Token-level
Step-level
Response-level
Trajectory-level
Task-level
```

例如“答案对了”是 outcome-level；而逐步判断哪一步开始出错，则属于 process / step-level supervision。

### 维度四：Purpose —— 这批数据拿来干什么？

```text
Pretraining
SFT
Preference Optimization
Reward Model
RL
Verifier / Grader
Evaluation
Failure Analysis
Regression Test
Data Synthesis Seed
```

同一条数据可能被转换后服务多个目的。

---

## 1.5 “标签”只是 Learning Signal 的一种

传统数据工作经常问：

> 标签是什么？

到了大模型阶段，更应该问：

> **模型从这条数据里到底能得到什么 learning signal？**

常见信号包括：

### 1. Demonstration / Imitation Signal

告诉模型：遇到这种输入，应该这样做。

典型形式：SFT。

```text
x → y*
```

### 2. Preference Signal

告诉模型：A 和 B 相比，B 更好。

```text
x
├── y_A
└── y_B

B > A
```

典型用途：DPO、preference optimization、reward modeling。

### 3. Scalar Reward

告诉模型：

```text
这一条轨迹得分 = 0.8
```

或者：

```text
success = 1
failure = 0
```

常用于 RL / policy optimization。

### 4. Process Supervision

不只看最终答案，而评价中间过程。

```text
Step 1: ✓
Step 2: ✓
Step 3: ✗
Step 4: 基于错误继续推导
```

它可以用于 reasoning verifier、process reward model、错误定位等。

### 5. Environment Feedback

这是 Agent 特别重要的一类信号。

例如：

```text
Tool Call:
transfer_money(amount=100)

Observation:
insufficient_balance
```

环境本身告诉模型动作没有成功。

再例如：

```text
database state before = meeting at Monday

database state after = meeting at Friday
```

这种 state transition 可以直接作为任务是否完成的证据。

---

## 1.6 Outcome Supervision 与 Process Supervision

### Outcome Supervision

只关心最终结果。

```text
Final Answer = Correct
```

优点：

- 标注便宜；
- 很多数学、代码任务可以自动判分；
- 易于大规模扩展。

问题：

- 不知道哪里做对了；
- 不知道哪里开始错；
- 可能出现“过程错误但碰巧答案正确”；
- 对长 Agent trajectory 的 credit assignment 很弱。

### Process Supervision

评价中间步骤。

```text
State 0 → Action 0 : correct
State 1 → Action 1 : unnecessary
State 2 → Action 2 : wrong tool
```

它能回答：Agent 是不会做，还是某一步选错了？

但成本更高，因为需要定义：

- 什么叫一个 step；
- 哪一步应该评分；
- 是否存在多条同样正确的路径；
- 标注者如何判断中间动作的合理性。

---

## 1.7 数据不只是“让模型学”，也可以“让人理解模型”

### Training-oriented Data

目标是改变模型。

```text
Data
 ↓
Training / Fine-tuning / Optimization
 ↓
New Model
```

### Evaluation-oriented Data

目标是测量模型。

```text
Data
 ↓
Run Model
 ↓
Measure Capability / Failure
```

但现实中二者经常形成循环：

```text
Eval 发现失败
   ↓
Failure Mining
   ↓
变成 Training Data
   ↓
新模型
   ↓
再次 Eval
```

因此成熟的数据体系通常不会把“训练数据团队”和“评测数据团队”完全割裂来看。

---

## 1.8 一句话理解现代大模型数据

```text
传统 ML：
数据 = 输入 + 标签

LLM Post-training：
数据 = 指令 + 响应 + 偏好 / Reward

Agent：
数据 = 任务 + 环境 + 轨迹 + 结果 + 反馈
```

再进一步：

> **数据工作的核心对象，从 Example 逐步扩大到了 Experience。**

---

## 1.9 本章关键词

| 术语 | 核心含义 |
|---|---|
| Dataset | 一组数据实例 |
| Sample / Example | 一个独立数据实例 |
| Task | 希望模型完成的目标 |
| Episode | 一次从开始到终止的完整执行 |
| State | 当前可用于决策的信息状态 |
| Action | Agent 采取的动作 |
| Observation | 环境对动作返回的结果 |
| Trajectory / Trace | 一次完整执行路径 |
| Outcome | 最终任务结果 |
| Learning Signal | 模型从数据中获得的学习反馈 |
| Outcome Supervision | 只监督最终结果 |
| Process Supervision | 对中间过程提供监督 |
| Verifier | 判断结果或过程是否满足条件的验证器 |
| Grader | 对模型输出 / trajectory 评分的评价器 |

---

## 1.10 常见误区

### 误区 1：大模型数据 = 文本语料

不对。Agent 数据还可能包括 JSON tool call、API 参数、网页状态、文件状态、数据库状态、GUI 操作、execution result、reward 和 grader output。

### 误区 2：有标准答案的数据才有用

不对。Preference、reward、环境反馈、pairwise comparison 都可以提供有效监督。

### 误区 3：最终答案正确，Agent 就执行正确

不对。Agent 可能根本没有执行工具、调错对象、调用失败、没有验证执行结果，却在最终自然语言中声称已经成功。因此必须检查真实 environment state。

### 误区 4：数据越多越好

不一定。真正需要研究的是：

```text
Quality
Diversity
Difficulty
Verifiability
Coverage
Novelty
Information Density
```

后续“数据筛选与 Data Curation”会专门展开。
