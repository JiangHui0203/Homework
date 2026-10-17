# 第 3 章 Preference Data、Reward 与 Feedback：让模型学会“多个可行行为里哪个更值得”

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 2 章 Pretraining、Instruction、SFT 与 Post-training Data`](./02_Pretraining_Instruction_SFT_and_Post_training_Data.md)
>
> 关联章节：[`第 6 章 Human Data`](./06_Human_Data_Annotation_and_Quality_Control.md)、[`第 8 章 Candidate Selection`](./08_Rollout_Rejection_Sampling_and_Candidate_Selection.md)、[`第 13 章 Credit Assignment`](./13_Task_Success_and_Credit_Assignment.md)、[`第 15 章 Grader / Verifier / Judge`](./15_Grader_Verifier_and_LLM_as_a_Judge.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md)
>
> 本章定位：**Preference / Reward / Relative Feedback 的 canonical chapter。它负责 Pointwise / Pairwise / Listwise、Chosen / Rejected、Reward Model、DPO-like Direct Preference、Rubric、Bias、Hard Negative 与 Agent Trajectory Preference；Evaluator 的正式边界归第 15 章，Outcome / Reward / Credit 的完整区分归第 13 章。**
>
> 本章核心问题：**当唯一“标准答案”不足以定义理想行为时，怎样通过比较、评分和反馈告诉模型：在多个看起来都合理的候选里，哪一个更符合真实目标？**

---

# 3.0 SFT 告诉模型“可以这样做”，Preference 告诉模型“更应该这样做”

假设两个回答都正确：

```text
A
准确、简短、偏技术

B
同样准确，但更适合初学者
```

SFT 通常只能选择一个 target demonstration。

Preference 则可以直接表达：

```text
在当前用户需求下
B > A
```

因此 Preference 的核心对象是：

```text
Context
+
Alternative Behaviors
+
Evaluation Objective
+
Relative Feedback
```

而不是孤立候选。

---

# 3.1 Pairwise Preference

经典结构：

```text
Context x
├── Chosen y_w
└── Rejected y_l

Label: y_w > y_l
```

例如：

```json
{
  "prompt": "用一句话解释过拟合。",
  "chosen": "过拟合是模型过度适应训练数据，导致在新数据上泛化变差。",
  "rejected": "过拟合就是模型训练得太好了。"
}
```

重要的是：

> **Chosen 表示相对更优，不自动等于绝对正确。**

两个候选都可能错，也可能都对。

---

# 3.2 Tie、Both Bad、Cannot Judge 不是异常值

强制所有 pair 二选一会制造伪监督。

真实动作空间应允许：

```text
A > B
B > A
Tie
Both Bad
Cannot Judge / Insufficient Evidence
```

这和 Human Annotation 的 abstention、Evaluator 的 `UNRESOLVED` 是同一条原则：

> **不要为了 coverage 伪造 certainty。**

---

# 3.3 Pointwise、Pairwise、Listwise

## Pointwise

```text
A → 4/5
B → 2/5
```

优势：适合多维 rubric。

风险：不同 judge 对绝对分数尺度理解可能不同。

## Pairwise

```text
A vs B → A wins
```

优势：人通常更容易做相对比较。

风险：position bias、比较成本、非传递性。

## Listwise

```text
A > C > B > D
```

一次提供更多排序信息，但认知负担更高。

不存在永远最好的结构，要根据 downstream objective 选择。

---

# 3.4 Feedback 从哪里来？

Preference / Reward 的 Feedback Source 可以是：

```text
Human
Domain Expert
AI Judge
Deterministic Rule
Executable Verifier
Environment Outcome
```

关键不是“人还是模型”，而是：

```text
Evidence 是否足够？
Evaluator 是否适合读取这种 Evidence？
Feedback 与真实目标是否一致？
```

Human Data 见第 6 章；Evaluator 层级见第 15 章。

---

# 3.5 Human / Expert Preference

Human 特别适合：

```text
clarity
naturalness
instruction following
user experience
ambiguous boundary
```

Expert 更适合：

```text
math
medicine
law
code correctness
specialized Agent policy
```

关键不是所有 pair 都用最高成本专家，而是：

```text
general cases → trained annotator
boundary / high-risk → expert / adjudication
```

---

# 3.6 AI Feedback

AI 可以提供：

```text
pairwise choice
pointwise rubric score
critique
ranking
```

优势：

```text
scale
speed
cost
```

风险：

```text
position bias
verbosity bias
style bias
self-preference
shared blind spot
```

所以 AI Feedback 的核心问题不是：

> Judge 强不强？

而是：

> **它对目标 Evidence 的判断是否经过独立校准。**

完整 Judge calibration 见第 15 章。

---

# 3.7 Rule / Environment Feedback

可执行任务中，优先利用客观 evidence：

```text
JSON parse
unit test
exact match
DB state
constraint predicate
side-effect check
```

例如 Agent：

```text
A final state = Friday 15:00
B final state = Tuesday 15:00
```

用户要求改到 Friday 时，A > B 不需要仅靠语言 Judge 猜。

因此：

> **Preference 的 label source 可以主观，但能 objective verify 的维度尽量不要只靠主观 preference。**

---

# 3.8 Reward：优化信号，不是世界事实

Reward 可以写成：

\[
r(x,y)\in\mathbb{R}
\]

最简单：

```text
success = 1
failure = 0
```

也可以包含：

```text
correctness
constraint compliance
safety
efficiency
```

但必须保持术语边界：

```text
Outcome
= 世界实际发生什么

Reward
= 用来优化行为的信号

Credit
= 如何把结果归因到中间 decision
```

完整理论见第 13 章。

---

# 3.9 多维 Objective 不要过早压成一个 Scalar

例如：

| Candidate | Correctness | Following | Safety | Efficiency |
|---|---:|---:|---:|---:|
| A | 1 | 1 | 1 | 0.4 |
| B | 1 | 0.5 | 1 | 0.9 |

直接算：

```text
A = 0.75
B = 0.85
```

可能把 instruction failure 隐藏掉。

所以很多系统更适合：

```text
Hard Constraints
↓
Task Success
↓
Safety / Side Effect
↓
Secondary Quality
↓
Efficiency / Style
```

即 lexicographic / hierarchical preference，而不是所有维度简单线性相加。

---

# 3.10 Reward Model

有 pairwise data：

```text
(x, y_w, y_l)
```

可以学习：

\[
r_\theta(x,y)
\]

使：

\[
r_\theta(x,y_w)>r_\theta(x,y_l)
\]

经典 pairwise 概率可以写成：

\[
P(y_w\succ y_l\mid x)=
\sigma(r_\theta(x,y_w)-r_\theta(x,y_l))
\]

Reward Model 的价值是把有限 preference 扩展成可对新 candidate 打分的 learned scorer。

但：

> **Reward Model 学到的是标签分布，不是真理。**

标注偏差也会被学习。

---

# 3.11 Reward Model、Verifier、Grader、Judge 不要按名字判断

本章只保留接口关系：

```text
Reward Model
→ learned optimization / ranking signal

Verifier / Grader / Judge
→ evaluation instruments
```

正式边界、Evidence Hierarchy 和 `Verifier ⊂ Grader` 的实用约定统一见第 15 章。

不要在每个 preference pipeline 里重新定义一套 evaluator taxonomy。

---

# 3.12 Direct Preference Optimization

Preference Data 不一定先训练 Reward Model。

另一条路线是直接用：

```text
Chosen / Rejected
```

优化 policy，例如 DPO-like 方法。

从数据角度真正重要的是：

```text
Pair 是怎么构造的？
Label 是谁给的？
Pair 是否有信息量？
Downstream algorithm 怎么消费它？
```

所以同一种 pair 数据可以被：

```text
Reward Model
Direct Preference Optimization
Judge Training
Candidate Analysis
```

不同下游使用。

---

# 3.13 Rubric：把“哪个好”拆成可解释标准

模糊问题：

> “A 和 B 哪个更好？”

更稳定的 rubric：

```text
Correctness
Instruction Following
Completeness
Relevance
Safety
Tool / Environment Grounding
Efficiency
Communication
```

还要定义维度之间的优先级。

例如 Agent：

```text
1. Hard policy constraints
2. Actual task success
3. No forbidden side effect
4. Observation grounding
5. Verification
6. Efficiency
7. Final communication
```

这样才能避免漂亮文字抵消真实执行失败。

---

# 3.14 Preference Bias

## Position Bias

候选位置影响选择。

控制：

```text
randomize order
swap audit
```

## Verbosity Bias

系统偏爱更长回答。

## Style / Correctness Conflation

流畅错误答案击败朴素正确答案。

## Sycophancy

把迎合用户误当帮助用户。

## Self / Model-family Bias

Judge 偏爱和自己风格相似的输出。

这些 bias 不应只作为“Judge 问题”，因为它们会直接被写进 Preference Data，进而改变训练分布。

---

# 3.15 Annotator Disagreement 不是纯噪声

分歧可能意味着：

```text
Rubric 不清
Candidate 太接近
需要专业知识
信息不足
任务本来就主观
```

所以应保留：

```text
raw labels
confidence
abstention
adjudication state
```

详细 Human Quality Control 见第 6 章。

---

# 3.16 什么样的 Pair 更有信息量？

### Low-information

```text
Perfect
vs
Garbage
```

### High-information

```text
Correct but misses one constraint
vs
Fully correct but slightly longer
```

真正有价值的 pair 往往靠近当前模型 decision boundary。

常见构造：

```text
near-score pair
hard-negative pair
same-state discordant pair
failure-specific pair
model-disagreement pair
```

Pair Construction 本身就是 Data Policy。

候选池如何产生和筛选详见第 8 章。

---

# 3.17 Hard Negative

Hard Negative 是：

> **看起来合理，但关键处失败的候选。**

例如：

```text
答案基本正确但漏条件
Tool 对但参数错一个 entity
成功执行但没有 verification
```

它比 obvious garbage 更能教模型真正的 decision boundary。

---

# 3.18 Agent Trajectory Preference

Agent 比较的不是只看 Final Response，而可能是整条：

```text
State
→ Action
→ Observation
→ Next Action
→ Final State
```

例如：

```text
A
success + verified + 5 calls

B
success + no harmful side effect + 9 calls

C
final text 很漂亮，但实际没有执行 update
```

一般优先级应是：

```text
Hard Constraint
Task Outcome
Side Effect
Grounding / Verification
Efficiency
Communication
```

所以自然语言 quality 只是 Agent preference 的一个末端维度。

---

# 3.19 从 Rollout 到 Preference Data

```text
Task / State Pool
↓
Generate Candidates / Trajectories
↓
Structural Validation
↓
Objective Verification where possible
↓
Pair Construction
↓
Human / AI Relative Judgment
↓
Quality Audit
↓
Chosen / Rejected / Tie / Both Bad
```

需要保存：

```text
generator version
sampling config
candidate order
verifier result
rubric version
judge / annotator version
raw judgment
confidence / abstention
```

这些 version / lineage 的系统治理见第 19 章。

---

# 3.20 Preference Data Quality

至少看：

```text
Label Reliability
Gold Accuracy
Position-swap Consistency
Coverage
Pair Difficulty
Class Balance
Domain / Failure Coverage
```

但最后最重要的仍然是：

> **训练后模型行为有没有真正改善？**

Preference 内部质量指标不能替代第 21 章的 Downstream Data Experiment。

---

# 3.21 Reward Hacking

一旦 Reward 成为优化目标，模型就可能搜索 reward 的漏洞。

例如：

```text
越长分越高
→ 模型无条件变长
```

或：

```text
只检查 final response 包含“已完成”
→ 模型学会直接声称完成
```

因此 reward 必须锚定：

```text
real outcome
environment state
hard constraints
held-out evaluation
adversarial audit
```

而不是只优化 proxy。

---

# 3.22 Canonical Case C2：会议改期的 Preference

任务：

> 把产品组会议改到周五 15:00。

### A

```text
search
→ update
→ read-back verify
→ success
```

### B

```text
search
→ final: “已改好”
```

### C

```text
search
→ update
→ repeated unnecessary search × 4
→ success
```

相对关系可能是：

```text
A > C > B
```

因为：

```text
A
真正成功 + verified + efficient

C
成功但冗余

B
语言看起来正确但任务没完成
```

这展示了 Preference Data 为什么必须和 Outcome Evidence 结合。

---

# 3.23 常见失败模式

1. **Chosen = Ground Truth。** Relative preference 不等于绝对正确。
2. **强制所有 pair 二选一。** 制造伪标签。
3. **Rubric 只有“哪个好”。** 多个目标混成黑箱。
4. **只比较 Final Response。** Agent execution 被忽略。
5. **所有 pair 都 perfect vs garbage。** 信息密度低。
6. **所有 pair 都极难。** 标注噪声过高。
7. **AI Judge 未校准就规模化。** 偏差被放大。
8. **Reward Model 被当成真正目标。** 容易 reward hacking。
9. **Outcome / Reward / Credit 混用。** 训练语义失真。
10. **Pair construction 没版本 / lineage。** 无法解释数据变化。
11. **Preference proxy 提升就宣布 data value。** 没有 downstream validation。

---

# 3.24 从数据岗位视角，本章实际在做什么？

典型工作：

```text
设计 preference rubric
生成 / 选择 candidate pool
构造 informative pairs
组织 Human / Expert / AI feedback
做 position / verbosity / style bias audit
训练 / 验证 reward model
构造 hard negatives
维护 chosen / rejected / tie data
分析 reward hacking
验证 preference training 后行为变化
```

真正成熟的表达不是：

> “我们标了 20 万个 A/B。”

而是：

> **“这些 pair 为什么值得比、Evidence 来自哪里、谁判、按什么标准判、标签有什么 bias，以及训练后模型是否真的学会了我们想要的 trade-off。”**

---

# 3.25 面试 / 自检问题

1. 为什么有 SFT 还需要 Preference Data？
2. Chosen 为什么不一定正确？
3. Pointwise / Pairwise / Listwise 各适合什么？
4. Tie / Both Bad / Cannot Judge 为什么重要？
5. Feedback 可以来自哪些来源？
6. Outcome 与 Reward 有什么区别？
7. Reward Model 学到的究竟是什么？
8. 为什么 Direct Preference 不一定需要显式 RM？
9. Rubric 为什么不能只写“哪个好”？
10. Position / Verbosity / Style Bias 如何进入数据？
11. Hard Negative 为什么信息量高？
12. Preference Pair 为什么应靠近 decision boundary？
13. Agent Trajectory Preference 为什么不能只看最终文字？
14. 如何防止 Reward Hacking？
15. Preference 内部质量好为什么仍不能证明 Training Value？

---

# 3.26 本章最终心智模型

```text
Generate / Observe Alternatives
↓
Collect Evidence
↓
Define Rubric
↓
Relative / Scalar Feedback
↓
Preference / Reward Data
↓
Policy / Reward Model Optimization
↓
Independent Downstream Evaluation
```

最重要的一句话：

> **Preference Data 的价值，不在于给候选排个名，而在于把真实目标中的 trade-off 转成模型可学习的相对监督。**

下一章第 4 章将继续进入更局部的问题：

> **当最终 Outcome 不足以解释一条 reasoning path 时，怎样监督中间 State、Step、Risk 与 Recoverability？**