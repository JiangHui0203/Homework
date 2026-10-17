# 第 2 章 Pretraining、Instruction、SFT 与 Post-training Data：不同阶段到底在教模型什么

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 1 章 Data Objects & Learning Signals`](./01_Data_Objects_and_Learning_Signals.md)
>
> 关联章节：[`第 3 章 Preference Data`](./03_Preference_Data_Reward_and_Feedback.md)、[`第 4 章 Reasoning Data`](./04_Reasoning_Data_and_Process_Supervision.md)、[`第 5 章 Agent Trajectory Data`](./05_Tool_Use_and_Agent_Trajectory_Data.md)、[`第 16 章 Benchmark Design`](./16_Benchmark_Design_and_Evaluation_Protocol.md)、[`第 20 章 Data Curation`](./20_Data_Quality_Filtering_Deduplication_and_Mixture.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md)
>
> 本章定位：**训练阶段与 Data Purpose 的 canonical overview。它负责说明 Pretraining / Continued Pretraining / Instruction / SFT / Preference / Reward / RL / Agent Training 分别消费什么经验、提供什么 learning signal；Filtering / Dedup / Mixture 的完整技术细节归第 20 章。**
>
> 本章核心问题：**模型从“会续写文本”到“会按用户要求行动并在环境中完成任务”，不同训练阶段到底希望它学会什么，因此需要什么类型的数据？**

---

# 2.0 先记住一条主线

```text
Pretraining
→ 学语言、知识、模式与世界分布

Instruction / SFT
→ 学“收到任务以后应该怎样响应 / 行动”

Preference / Reward / RL
→ 学“多个可行行为中哪一种更值得选择”

Reasoning / Process Data
→ 学中间 state / decision 怎样更可靠

Agent Data
→ 学在外部环境中连续决策直到任务完成
```

这不是互斥分箱。

同一条 experience 可以被转换后用于多个阶段；真正应该问的是：

> **当前训练目标准备从这条数据里提取什么 learning signal？**

---

# 2.1 Pretraining Data：让模型学习“世界和语言长什么样”

经典 decoder-only LLM 的目标是 next-token prediction：

\[
\max \sum_{t=1}^{T}\log P(x_t\mid x_{<t})
\]

数据通常是大规模自然 token sequence：

```text
Web
Books
Code
Papers
Technical Docs
Forums
Multilingual Text
Math / Structured Content
```

Pretraining 不依赖人工逐条给 label；文本本身提供 self-supervised signal。

因此它通常具有：

```text
规模最大
单条目的性较弱
覆盖最广
数据分布本身极其重要
```

---

# 2.2 Pretraining Data 的工作不是“下载语料”

一个典型 pipeline：

```text
Source Acquisition
↓
Parsing / Extraction
↓
Normalization
↓
Language / Domain Identification
↓
Validity / Rights / Privacy
↓
Quality Filtering
↓
Dedup / Contamination Handling
↓
Mixture / Sampling
↓
Tokenization / Sharding
```

这里每一步都会重塑模型看到的世界。

但本章只建立概览：

```text
Dedup / Mixture / Filtering
→ Ch20

Contamination 对 Eval 的影响
→ Ch16

Provenance / Rights / Version
→ Ch19
```

避免在训练阶段总览章里重复完整 Data Curation 理论。

---

# 2.3 Pretraining Data 的几个典型来源

## Web

优势：

```text
规模
覆盖
长尾知识
```

风险：

```text
noise
SEO / spam
duplicate
synthetic pollution
privacy / rights
```

## Books / Long-form

更容易提供：

```text
long coherence
narrative structure
cross-paragraph dependency
```

## Code

除了编程知识，还提供：

```text
formal syntax
API patterns
dependency structure
test / error-handling patterns
```

## Academic / Technical

提供：

```text
专业术语
符号系统
技术结构
领域知识
```

## Multilingual

需要处理：

```text
language imbalance
translationese
cross-language duplication
low-resource coverage
```

---

# 2.4 Pretraining、Continued Pretraining 与 Domain Adaptation

有时基础模型已有通用 pretraining，再针对：

```text
Finance
Medical
Code
Long Context
Multilingual
Company Knowledge
```

继续做语言模型训练。

这类通常可理解为：

```text
Continued Pretraining / Domain-adaptive Pretraining
```

它和 SFT 的区别仍然是主要 learning signal：

```text
Continued Pretraining
→ token prediction on domain corpus

SFT
→ imitate desired response / behavior
```

所以“用了专业数据”本身不能判断它属于哪个阶段。

---

# 2.5 Instruction Data：从文本分布走向任务响应

Instruction Data 显式建立：

```text
User Intent / Instruction
↓
Desired Behavior
```

例如：

```text
Summarize
Translate
Rewrite
Extract
Classify
Solve
Write Code
Follow Format
Use Tool
Refuse / Clarify
```

它的重点不是只教知识，而是教：

> **当前这段输入是一个需要遵循的任务。**

---

# 2.6 Single-turn、Multi-turn 与 Role Structure

### Single-turn

```text
User → Assistant
```

适合局部能力。

### Multi-turn

可以训练：

```text
constraint retention
reference resolution
user correction handling
state maintenance
clarification
```

### Role Structure

现代模型还需要区分：

```text
System
Developer
User
Assistant
Tool
```

所以 message role 和优先级本身也是输入分布的一部分。

---

# 2.7 Formatting Constraint 也是 Behavior

例如：

> “只返回 JSON，不要解释。”

对 API / Agent pipeline 来说：

```text
内容正确但格式不合法
```

仍可能是 task failure。

因此 Instruction / SFT 数据需要覆盖：

```text
format constraints
positive constraints
negative constraints
conditional constraints
cross-turn constraints
```

---

# 2.8 SFT：用 Demonstration 教模型“应该怎么做”

SFT 的核心可以写成：

```text
Context x
→ Desired Behavior y*
```

模型最大化：

\[
\log P(y^*\mid x)
\]

从数据角度：

> **SFT 是 demonstration imitation。**

因此 SFT 的关键不是“有答案”，而是 target behavior 是否值得被模仿。

---

# 2.9 SFT Data 可以从哪里来？

常见来源：

```text
Human / Expert Demonstration
Curated Existing Data
Teacher Model + Verification
Successful Agent Rollout
Human-corrected Model Output
Programmatic Construction
```

不同 source 的核心风险不同：

```text
Human
→ cost / consistency

Teacher
→ teacher bias / shared blind spot

Rollout
→ success does not guarantee ideal policy

Programmatic
→ coverage / realism
```

因此 Source 不能替代 Quality / Downstream Validation。

---

# 2.10 成功轨迹不自动等于好 SFT

两个 Agent trajectory 都成功：

```text
A
3 个必要 tool calls

B
17 个 calls
多次错误后偶然恢复
```

如果直接：

```text
success = positive SFT
```

模型可能学到无效甚至危险习惯。

所以 SFT demonstration 还要考虑：

```text
policy validity
side effects
observation grounding
efficiency
verification behavior
```

详细 Agent Data 见第 5 / 12 章。

---

# 2.11 SFT 的天然局限：主要展示“好行为”，不擅长表达相对边界

SFT 很擅长：

```text
这里应该怎么做
```

但较弱于：

```text
为什么 A 比 B 好
什么时候不该这样做
两个都对时哪个更优
near-miss 错在哪里
```

这些问题自然引出：

```text
Preference
Reward
Process Supervision
Hard Negative
```

也就是后续 Post-training Data。

---

# 2.12 Post-training 是一个大集合

本书采用宽义：

```text
Post-training Data
├── SFT Demonstration
├── Preference / Ranking
├── Reward Model Data
├── Critique / Correction
├── Process Supervision
├── RL Rollout
├── Verifier / Judge Data
├── Safety / Alignment Data
└── Agent Trajectory / Tool Feedback
```

所以：

> **SFT Data ⊂ Post-training Data。**

不要把 Post-training 简化成“DPO / RLHF”。

---

# 2.13 Preference Data：从“示范”转向“相对选择”

基本形式：

```text
Context
├── A
└── B

A > B
```

它适合学习：

```text
style trade-off
constraint fidelity
hard negative boundary
efficiency
trajectory preference
```

完整定义与 bias 见第 3 章。

---

# 2.14 Reward / RL Data：让 Outcome 与 Policy Update 连起来

RL 场景常出现：

```text
State / Task
↓
Policy Rollout
↓
Outcome / Verifier / Reward
↓
Policy Update
```

重要术语边界：

```text
Outcome
= 世界实际发生什么

Reward
= 用来优化 policy 的信号
```

详细区分见第 13 章。

---

# 2.15 On-policy 与 Off-policy Data

### On-policy

来自当前 policy：

```text
Current Model
→ Current Rollouts
```

优点：贴当前真实错误分布。

### Off-policy

来自：

```text
Teacher
Old Model
Human
Historical Logs
Other Policy
```

优点：便于复用、覆盖更广。

但可能与当前 policy 分布不一致。

所以：

> **Data Source 与 Current Model 的距离本身就是数据属性。**

---

# 2.16 Verifiable Data 为什么特别重要？

有些任务可以得到高可信外部 outcome：

```text
Math exact / symbolic result
Code unit tests
SQL execution
Final Environment State
Schema / Constraint Check
```

这类数据适合大规模：

```text
Rollout
→ Verify
→ Rank / Reward / Filter
```

因为监督不完全依赖主观 Judge。

Evaluator 层级见第 15 章。

---

# 2.17 Reasoning / Process Data

Reasoning Data 的对象可能是：

```text
Reasoning State
Step
Transition
Alternative Continuation
Critique
Correction
```

它解决：

```text
最终 answer 对了，但过程是否可靠？
错误从哪里开始？
当前 state 是否值得继续 / repair？
```

完整理论见第 4 章。

---

# 2.18 Agent Training Data

Agent 数据进一步引入：

```text
Task Case
Tool Contract
Environment
Trajectory
Observation
Final State
Side Effects
```

可能被转换为：

```text
Trajectory SFT
Tool Preference
Recovery Data
State-action Supervision
RL Rollout
Regression Case
```

因此 Agent Training 的基本对象经常不是“回答”，而是 Experience。

---

# 2.19 不同训练阶段的简化对照

| 阶段 / 目的 | 主要数据对象 | 核心 Learning Signal | 典型问题 |
|---|---|---|---|
| Pretraining | token sequence | next-token prediction | 世界与语言长什么样 |
| Continued PT | domain sequence | domain token prediction | 专业分布怎么补 |
| SFT | context + demo | imitation | 应该怎么响应 / 行动 |
| Preference | candidates + relative label | comparison | 哪个行为更好 |
| RM / Grader Training | candidates + score/ranking | learned evaluation | 怎样预测质量 |
| RL | rollout + reward | outcome-conditioned policy update | 怎样提高长期行为 |
| Process Supervision | state / step / transition | local feedback | 中间决策哪里错 |
| Agent Training | task + environment + trajectory | action/outcome feedback | 怎样完成真实任务 |

这张表是本章核心导航，不等于所有训练系统都必须按完全相同阶段实现。

---

# 2.20 Data Mixture：这里只建立“曝光”概念

一个训练 run 往往同时消费：

```text
General SFT
Tool-use
Recovery
Reasoning
Safety
Domain Data
```

真正需要关注的是：

```text
Sample Share
Token Share
Training Exposure
Loss Weight
```

而不是只报：

```text
“用了 100k Agent Data”
```

Mixture、Dedup、Weighting 的完整理论统一见第 20 章。

---

# 2.21 Curriculum：顺序也是 Training Policy

即使使用同一批数据：

```text
Random Mix
Easy → Hard
Foundation → Frontier
Dynamic Curriculum
```

也可能产生不同学习结果。

Curriculum 的 acquisition / frontier 逻辑见第 9 章；是否真的有效必须由第 21 章 Data Experiment 验证。

---

# 2.22 Training Data 与 Evaluation Data 必须有目的边界

训练资产用于：

```text
改变模型
```

Evaluation Asset 用于：

```text
测量模型
```

如果：

```text
Hidden Eval Failure
→ 原题直接进入训练
→ 还用同一题证明 capability gain
```

就混淆了：

```text
case repair
```

和：

```text
generalization
```

Benchmark / contamination discipline 见第 16 / 19 章。

---

# 2.23 一个 Inventory Agent 的阶段映射例子

目标：让 Agent 正确处理“查实时库存”。

### Pretraining

学到：

```text
商品、库存、API 等一般语言与知识模式
```

### SFT

示范：

```text
需要实时信息时调用 inventory tool
```

### Preference

比较：

```text
真实查询 > 凭记忆猜库存
```

### Agent Rollout / RL

在环境中：

```text
query inventory
→ observation
→ answer / fallback
```

根据真实 outcome 提供 feedback。

所以同一个 capability 会横跨多个阶段；每个阶段教的是不同层次。

---

# 2.24 常见失败模式

1. **Pretraining Data = 原始网页。** 忽略解析、过滤、分布设计。
2. **有大量 QA 文本就不需要 Instruction Tuning。** 统计模式不等于稳定任务遵循。
3. **SFT 成功样本全部值得模仿。** Outcome success 不等于 policy ideal。
4. **Post-training = DPO。** 它远比 preference optimization 更宽。
5. **Teacher 更强 = Synthetic 自动更好。** Teacher bias 仍会被复制。
6. **On-policy / Off-policy 不区分。** 当前模型真实错误分布可能被错估。
7. **数据量直接跨阶段比较。** 1B pretraining tokens 与 10k expert trajectories 不是同一量纲。
8. **Sample count = exposure。** 长轨迹可能获得更多 token weight。
9. **Mixture / curriculum 凭直觉。** 必须实验验证。
10. **Training / Eval 边界模糊。** 容易产生 contamination 与过强 claim。

---

# 2.25 从数据岗位视角，本章实际在做什么？

典型工作包括：

```text
判断数据属于什么 training purpose
设计 instruction / SFT schema
构建 teacher / human demo
维护 role / formatting constraints
区分 on-policy / off-policy rollout
准备 preference / reward / process data
规划 data mixture 的目标曝光
维护 train / eval 边界
```

真正成熟的判断不是：

> “这是一批高质量数据。”

而是：

> **“它要在哪个训练阶段，以什么 learning signal，被当前模型怎样消费？”**

---

# 2.26 面试 / 自检问题

1. Pretraining 与 SFT 的核心 learning signal 有什么区别？
2. Continued Pretraining 与 SFT 怎样区分？
3. Instruction Data 为什么不只是知识数据？
4. Role / Format 为什么也属于模型输入分布？
5. 什么样的成功 trajectory 不适合直接做 SFT？
6. 为什么 `SFT Data ⊂ Post-training Data`？
7. Preference / Reward / Process Data 分别解决什么？
8. On-policy 与 Off-policy Data 有什么区别？
9. 为什么 Verifiable Data 对规模化 Post-training 特别重要？
10. Agent Training Data 为什么比 response data 更复杂？
11. Sample Count 为什么不等于 Training Exposure？
12. Mixture 与 Curriculum 有什么区别？
13. 为什么 Training Data 与 Eval Data 必须隔离？
14. 同一个 capability 为什么可能同时需要 SFT、Preference 和 RL？
15. 如果模型会输出正确 Tool JSON 但实际任务仍经常失败，你会往哪个数据层继续查？

---

# 2.27 本章最终心智模型

```text
Pretraining
学分布
↓
SFT
学示范行为
↓
Preference / Reward
学相对选择
↓
Process / Agent Data
学 state-conditioned decision
↓
RL / Continued Improvement
把 outcome 反馈到 policy
```

一句话：

> **训练阶段的名字不是重点；重点是这批数据正在向模型提供什么 learning signal，以及它试图改变哪一层行为。**

下一章第 3 章将专门进入：

> **当一个“正确示范”不足以定义理想行为时，怎样用 Preference、Reward 与 Feedback 表达行为之间的相对优劣？**