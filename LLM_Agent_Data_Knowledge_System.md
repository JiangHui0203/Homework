# 大模型与 Agent 数据知识体系

> 用途：系统学习“大模型 / Agent 中的数据工作到底在做什么”，覆盖训练数据、偏好数据、Reasoning 数据、Agent trajectory、合成数据、数据筛选、Eval / Benchmark 与数据飞轮。
>
> 维护方式：按“层 → 章 → 节”逐步补全。先建立统一概念和完整地图，再逐章深入到数据结构、生产方法、评价指标、工程流程、常见失败模式与面试问题。
>
> 当前版本：V1（2026-10-16）
>
> 关联文档：[`Agent_Knowledge_System.md`](./Agent_Knowledge_System.md)

---

# 0. 这套知识体系到底研究什么？

很多岗位会写：

- 大模型数据
- AI Data
- Agent 数据
- 数据策略
- 数据生产
- 数据合成
- 数据飞轮
- 模型评测 / Benchmark

如果只把它理解成“收集数据、清洗数据、人工标注”，会低估现在大模型数据工作的范围。

在传统监督学习里，一个数据样本经常可以抽象成：

```text
x → y
```

例如：

```text
图片 → 类别
文本 → 情感标签
问题 → 标准答案
```

而在今天的大模型系统里，一个“数据单元”可能是：

```text
Instruction
   ↓
Response
```

也可能是：

```text
Prompt
 ├── Response A
 └── Response B
        ↓
Preference: B > A
```

还可能是一条推理过程：

```text
Problem
  ↓
Reasoning State 1
  ↓
Reasoning State 2
  ↓
Reasoning State 3
  ↓
Final Answer
```

到了 Agent，更常见的是完整交互轨迹：

```text
Task
 ↓
State
 ↓
Action / Tool Call
 ↓
Observation
 ↓
New State
 ↓
Action
 ↓
...
 ↓
Final Outcome
```

因此，本体系采用一个更一般的定义：

> **大模型 / Agent 数据，本质上是在设计模型能够从中获得什么信息、什么反馈和什么学习信号。**

换句话说，“做数据”的核心已经逐渐从：

> 给样本打标签

转向：

> **定义任务 → 构造经验 → 提供反馈 → 判断成败 → 选择真正值得学习的数据。**

---

## 0.1 一张总图：从“数据样本”到“模型改进闭环”

```text
真实用户 / 目标能力 / 产品需求
            ↓
       Capability Definition
            ↓
         Task Design
            ↓
 ┌──────────┴──────────┐
 ↓                     ↓
Real Data         Synthetic Data
真实数据             合成数据
 └──────────┬──────────┘
            ↓
         Rollout
            ↓
   Response / Reasoning /
      Agent Trajectory
            ↓
 ┌──────────┴──────────┐
 ↓                     ↓
Grading              Analysis
评价/打分             错误分析
 ↓                     ↓
Training Data       Eval Set
 ↓                     ↓
SFT / DPO / RL      Regression
 └──────────┬──────────┘
            ↓
         New Model
            ↓
         New Rollout
            ↺
```

这张图里最重要的是：**数据不是流水线的起点，而是闭环中的中间产物。**

同一条模型轨迹，可能同时被用作：

- 失败分析材料；
- Benchmark case；
- SFT 样本；
- preference pair；
- reward / verifier 训练数据；
- hard case seed；
- 下一轮 synthetic data 的生成条件。

因此现代数据工作经常同时横跨：**模型、Agent、Eval、数据分析与工程系统。**

---

# 0.2 全体系分层

整套知识体系暂分为五层。

```text
I. Data Objects & Learning Signals
   数据对象与学习信号
                ↓
II. Data Production & Synthesis
    数据生产与合成
                ↓
III. Agent Tasks, Environments & Trajectories
     Agent 任务、环境与轨迹
                ↓
IV. Data Quality, Evaluation & Grading
    数据质量、评测与判分
                ↓
V. Data Flywheel & Data Strategy
   数据飞轮与数据策略
```

它们分别回答五个问题：

1. **模型到底在从什么样的数据中学习？**
2. **这些数据是怎么被生产出来的？**
3. **Agent 数据为什么和普通问答数据不一样？**
4. **我们怎么知道一条数据是对的、有价值的、没有污染的？**
5. **怎样把一次实验变成可持续的数据改进闭环？**

---

# I. Data Objects & Learning Signals

> 本层解决最基础的问题：**“大模型数据”究竟有哪些类型，它们分别向模型提供什么学习信号？**

---

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

---

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

---

### 维度三：Granularity —— 监督到哪一级？

```text
Token-level
Step-level
Response-level
Trajectory-level
Task-level
```

例如：

```text
“答案对了”
```

是 outcome-level。

而：

```text
第 1 步正确
第 2 步正确
第 3 步发生逻辑错误
```

则属于 process / step-level supervision。

---

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

告诉模型：

> 遇到这种输入，应该这样做。

典型形式：SFT。

```text
x → y*
```

---

### 2. Preference Signal

告诉模型：

> A 和 B 相比，B 更好。

```text
x
├── y_A
└── y_B

B > A
```

典型用途：DPO、preference optimization、reward modeling。

---

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

---

### 4. Process Supervision

不只看最终答案，而评价中间过程。

```text
Step 1: ✓
Step 2: ✓
Step 3: ✗
Step 4: 基于错误继续推导
```

它可以用于 reasoning verifier、process reward model、错误定位等。

---

### 5. Environment Feedback

这是 Agent 特别重要的一类信号。

例如：

```text
Tool Call:
transfer_money(amount=100)

Observation:
insufficient_balance
```

环境本身告诉模型：动作没有成功。

再例如：

```text
database state before = meeting at Monday

database state after = meeting at Friday
```

这种 state transition 可以直接作为任务是否完成的证据。

---

## 1.6 Outcome Supervision 与 Process Supervision

这是 Reasoning / Agent 数据里非常重要的一组概念。

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

---

### Process Supervision

评价中间步骤。

```text
State 0 → Action 0 : correct
State 1 → Action 1 : unnecessary
State 2 → Action 2 : wrong tool
```

它能回答：

> Agent 是不会做，还是某一步选错了？

但成本也更高，因为需要定义：

- 什么叫一个 step；
- 哪一步应该评分；
- 是否存在多条同样正确的路径；
- 标注者如何判断中间动作的合理性。

---

## 1.7 数据不只是“让模型学”，也可以“让人理解模型”

需要区分两类用途。

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

可以用下面三个层次记忆：

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

不对。

Agent 数据中还可能包括：

- JSON tool call；
- API 参数；
- 网页状态；
- 文件状态；
- 数据库状态；
- GUI 操作；
- execution result；
- reward；
- grader output。

---

### 误区 2：有标准答案的数据才有用

不对。

Preference、reward、环境反馈、pairwise comparison 都可以提供有效监督。

---

### 误区 3：最终答案正确，Agent 就执行正确

不对。

Agent 可能：

- 根本没有执行工具；
- 调错对象；
- 调用了工具但失败；
- 没有验证执行结果；
- 最终自然语言却声称已经成功。

因此要检查真实 environment state。

---

### 误区 4：数据越多越好

不一定。

如果新增数据只是大量重复已有能力，边际价值可能很低。

真正需要研究的是：

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

---

# 2. Pretraining、SFT 与 Post-training Data

> 状态：待逐节展开。
>
> 核心问题：模型从“海量语料”到“会按照人的要求做事”，分别需要哪些数据？

计划内容：

## 2.1 Pretraining Data

- Web / Books / Code / Academic / Multilingual Data
- token-level next-token prediction
- 数据去重、质量过滤与 contamination
- 为什么 pretraining data 与 instruction data 不是一回事

## 2.2 Instruction Data

```text
Instruction → Response
```

- single-turn instruction
- multi-turn dialogue
- system / developer / user hierarchy
- formatting constraints
- capability-specific instruction data

## 2.3 SFT Data

- demonstration learning
- expert data vs synthetic data
- positive-only imitation 的能力与局限
- SFT 对行为格式、工具调用、回答风格的影响

## 2.4 Post-training Data

- SFT
- Preference
- Reward
- RL rollouts
- Verifiable tasks

## 2.5 数据 mixture

- 不同能力如何配比
- 数据量与能力覆盖
- domain balancing
- oversampling / undersampling
- curriculum

---

# 3. Preference Data、Reward 与 Feedback

> 核心问题：当“唯一标准答案”不存在时，如何告诉模型什么更好？

计划内容：

## 3.1 Pairwise Preference

```text
Prompt
├── Response A
└── Response B

A > B
```

## 3.2 Preference Label 从哪里来？

- human preference
- expert preference
- AI feedback / RLAIF
- rule-based grading
- environment-based outcome

## 3.3 Reward Model Data

- scalar reward
- ranking signal
- reward model 与 grader 的关系

## 3.4 Preference 的噪声

- annotator disagreement
- positional bias
- verbosity bias
- style vs correctness conflation
- sycophancy preference

## 3.5 Rubric-based Preference

将“哪个好”拆成：

```text
Correctness
Instruction Following
Completeness
Relevance
Style
Safety
Tool Use
```

---

# 4. Reasoning Data 与 Process Supervision

> 核心问题：不仅知道“答案错了”，还要知道“从哪一步开始错”。

计划内容：

## 4.1 Chain-of-Thought / Reasoning Trace

## 4.2 Outcome Label vs Step Label

## 4.3 Process Reward Model

## 4.4 Verifier

## 4.5 Reasoning Error Taxonomy

- calculation error
- logical jump
- wrong assumption
- hallucinated fact
- premature commitment
- failed backtracking

## 4.6 Recoverability

```text
当前 reasoning state
↓
还能不能通过继续推理修复？
```

## 4.7 Reasoning Data 的特殊问题

- 多条正确推理路径
- hidden reasoning 与可观测 trace
- 长推理的 credit assignment
- final answer correct but process flawed

---

# 5. Tool-use Data 与 Agent Trajectory Data

> 核心问题：Agent 如何学会“什么时候调用什么工具、参数怎么填、看到结果后下一步做什么”？

计划内容：

## 5.1 Function Calling Data

```text
User Request
 ↓
Tool Selection
 ↓
Argument Generation
```

## 5.2 Tool-use Trajectory

```text
Task
↓
Tool Call
↓
Observation
↓
Next Decision
```

## 5.3 Tool Selection Error

## 5.4 Argument Error

## 5.5 Missing Tool Call

## 5.6 Redundant Tool Call

## 5.7 Observation Grounding

## 5.8 Execution Verification

## 5.9 Long-horizon Agent Data

---

# II. Data Production & Synthesis

> 本层回答：**这些数据到底怎么来？**

---

# 6. Human Data：人工数据生产

计划内容：

- crowd annotation
- expert annotation
- annotation guideline
- gold set
- inter-annotator agreement
- adjudication
- 标注成本与质量控制
- 为什么 Agent 标注比普通 NLP 标注更难

---

# 7. Synthetic Data：模型生成数据

计划内容：

## 7.1 Self-Instruct

## 7.2 Teacher Model Generation

## 7.3 Distillation

## 7.4 Prompt Evolution

## 7.5 Task Synthesis

## 7.6 Response Synthesis

## 7.7 Synthetic Trajectory

## 7.8 Synthetic Environment

## 7.9 Synthetic Data 的典型风险

- mode collapse
- teacher bias
- error amplification
- fake diversity
- benchmark contamination

---

# 8. Rollout、Rejection Sampling 与 Candidate Selection

计划内容：

```text
Prompt
 ↓
Generate N candidates
 ↓
Score / Verify
 ↓
Select
 ↓
Training Data
```

重点：

- best-of-N
- rejection sampling
- self-consistency
- verifier-guided selection
- reward-guided selection
- positive filtering
- negative data 如何保留价值

---

# 9. Hard Case Mining 与 Curriculum

计划内容：

- easy / medium / hard
- model-specific hard case
- error-driven sampling
- uncertainty sampling
- disagreement mining
- adversarial generation
- curriculum learning
- capability frontier

核心问题：

> **下一条最值得生产的数据是什么？**

---

# III. Agent Tasks, Environments & Trajectories

> 这是 Agent 数据区别于普通 LLM 数据的核心层。

---

# 10. Agent Task Design

计划内容：

- task goal
- initial state
- constraints
- available tools
- hidden state
- success condition
- termination condition
- difficulty
- task decomposition
- realistic task vs toy task

---

# 11. Environment Design

计划内容：

- database environment
- browser environment
- coding environment
- filesystem
- calendar / email / CRM
- GUI / computer-use environment
- simulator
- sandbox
- deterministic vs stochastic environment

---

# 12. Agent Trajectory Anatomy

计划内容：

```text
State
 ↓
Decision
 ↓
Action
 ↓
Observation
 ↓
State Update
```

深入讨论：

- trace schema
- message / action / observation boundary
- multi-step dependency
- trajectory length
- branching
- backtracking
- memory
- context truncation

---

# 13. Task Success 与 Credit Assignment

计划内容：

- binary success
- partial credit
- trajectory reward
- step reward
- terminal state check
- side effect verification
- efficiency penalty
- unnecessary actions
- correct result via wrong path

---

# 14. Agent Failure Taxonomy

计划内容：

```text
理解失败
规划失败
工具选择失败
参数失败
执行失败
Observation 理解失败
状态跟踪失败
验证失败
停止失败
最终表达失败
```

这部分最终会形成一套可直接用于：

- 标注 guideline；
- failure analysis；
- eval taxonomy；
- 数据生产策略

的统一错误分类。

---

# IV. Data Quality, Evaluation & Grading

> 本层解决：**数据很多并不代表数据好，分数很多也不代表评价可信。**

---

# 15. 什么叫高质量数据？

计划从以下维度建立质量模型：

```text
Correctness
Relevance
Diversity
Difficulty
Coverage
Novelty
Verifiability
Consistency
Naturalness
Information Density
```

---

# 16. Verifiable Data

重点讨论：

- exact match
- unit test
- code execution
- mathematical verifier
- state-based verification
- database check
- constraint checker
- executable reward

核心思想：

> **能自动可靠验证的任务，更容易扩大 rollout 与 RL 数据规模。**

---

# 17. LLM-as-a-Judge 与 Grader

计划内容：

- pointwise grading
- pairwise grading
- rubric grading
- reference-based grading
- reference-free grading
- judge calibration
- judge bias
- position bias
- verbosity bias
- self-preference
- model-family bias

---

# 18. Eval / Benchmark Data

计划内容：

- capability taxonomy
- benchmark construction
- static benchmark
- dynamic benchmark
- regression set
- hidden test set
- contamination
- saturation
- task validity
- metric validity

---

# 19. Data Curation：为什么“筛数据”越来越重要？

计划内容：

## 19.1 Deduplication

## 19.2 Quality Filtering

## 19.3 Difficulty Filtering

## 19.4 Diversity Selection

## 19.5 Coverage Analysis

## 19.6 Near-duplicate 与 Semantic Duplicate

## 19.7 Data Value

尝试回答：

```text
这一条数据加入训练集，边际价值是多少？
```

而不是只问：

```text
这条数据有没有错误？
```

---

# V. Data Flywheel & Data Strategy

> 最后一层研究：如何让“数据生产”从一次性项目变成持续改进系统。

---

# 20. Data Flywheel

典型闭环：

```text
Deploy / Evaluate
      ↓
Collect Traces
      ↓
Failure Mining
      ↓
Root Cause Analysis
      ↓
Generate / Label New Data
      ↓
Train / Prompt / Harness Update
      ↓
Regression Eval
      ↓
Deploy Again
      ↺
```

后续重点讨论：

- 什么信号值得回流；
- 如何避免线上分布被噪声淹没；
- 用户纠正数据；
- failure-driven data synthesis；
- model-data co-evolution。

---

# 21. Data Lineage、Versioning 与 Experiment

计划内容：

- dataset version
- provenance
- lineage
- generation config
- model version
- prompt version
- grader version
- label version
- train/eval split
- leakage prevention
- reproducibility

目标：任何一条数据都能回答：

```text
它从哪里来？
谁生成的？
谁判的？
为什么留下？
进入过哪些训练？
出现在哪些评测？
```

---

# 22. Data Strategy：什么数据最值得做？

数据策略最终不是“多造数据”，而是资源分配问题。

需要同时考虑：

```text
Capability Gap
× Failure Frequency
× Business Importance
× Data Cost
× Verifiability
× Expected Learning Value
```

后续会展开：

- capability gap analysis
- marginal data value
- data ROI
- bottleneck identification
- train-eval alignment
- distribution shift
- long-tail coverage

---

# 23. 一个“大模型 / Agent 数据岗”实际可能在做什么？

把前面的体系映射回工作，会得到以下典型任务。

## 23.1 数据生产

```text
设计任务
写 prompt
模型批量 rollout
清洗结果
打标签
筛数据
生成训练集
```

## 23.2 Agent 数据

```text
搭环境
定义工具
生成任务
跑 trajectory
检查 task success
分析 tool-use failure
构造新数据
```

## 23.3 Eval 数据

```text
设计 capability taxonomy
构造 benchmark
写 rubric
校准 grader
分析 failure
维护 regression set
```

## 23.4 数据策略

```text
找到模型弱点
判断值得补什么数据
设计实验
比较不同数据方案
证明哪批数据真正有效
```

## 23.5 数据工程

```text
pipeline
versioning
lineage
dedup
sampling
batch inference
quality control
statistics dashboard
```

因此，一个成熟的大模型数据岗位，往往不是单纯的数据标注岗位，而是下面几种能力的交叉：

```text
LLM / Agent Understanding
        +
Data Analysis
        +
Evaluation
        +
Experiment Design
        +
Python / Data Pipeline
```

---

# 24. 最终应该形成的能力树

学完整套体系后，希望能够回答下面这些问题。

## Level 1：看懂数据

- 这是什么类型的数据？
- 它的监督信号是什么？
- 它服务训练还是评测？
- 它的粒度是什么？

## Level 2：生产数据

- 怎么构造这批数据？
- 人工还是 synthetic？
- 怎么生成 candidate？
- 怎么筛选？
- 怎么判分？

## Level 3：分析数据

- 模型在哪些 case 上失败？
- 失败属于什么类型？
- 数据分布是否失衡？
- 是否存在 contamination？
- 哪些数据重复、低价值？

## Level 4：设计数据实验

- 补哪批数据最可能提升目标能力？
- 如何设置 train / eval / control？
- 如何证明提升来自数据而不是别的变量？

## Level 5：建立数据飞轮

- 如何从模型失败自动产生下一批数据？
- 如何持续监控能力退化？
- 如何维护 regression set？
- 如何把线上经验转化为可靠学习信号？

最终最重要的一句话是：

> **懂模型为什么错 → 能把错误变成数据 → 能证明数据有用 → 能把这个过程规模化。**

---

# 25. 后续逐章补全顺序

建议不按“热门词汇”乱学，而按下面顺序推进：

```text
第 1 章  数据对象与 Learning Signal       ← 已完成第一版
   ↓
第 2 章  Pretraining / SFT / Post-training
   ↓
第 3 章  Preference / Reward
   ↓
第 4 章  Reasoning / Process Supervision
   ↓
第 5 章  Tool-use / Agent Trajectory
   ↓
第 7-9 章  Synthetic Data 与数据生产
   ↓
第 10-14 章 Agent Task / Environment / Failure
   ↓
第 15-19 章 Quality / Grader / Eval / Curation
   ↓
第 20-22 章 Data Flywheel / Data Strategy
```

其中，每一章后续统一按以下模板展开：

```text
1. 定义
2. 为什么需要
3. 数据结构
4. 生产流程
5. 常见方法
6. 评价指标
7. 常见失败模式
8. 与相邻概念的区别
9. 一个具体案例
10. 工程实践
11. 面试常问问题
12. 延伸论文 / 系统
```

这样最终得到的不是“数据八股合集”，而是一套可以继续长大的知识体系。
