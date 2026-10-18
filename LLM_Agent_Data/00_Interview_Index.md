# LLM / Agent Data Knowledge System：Interview Index

> 角色：把常见 LLM / Agent Data、Evaluation、Post-training、Agent Data 面试题映射到知识章节和答题结构。
>
> 原则：**不是背标准答案，而是学会用同一套 reasoning frame 组织回答。**
>
> 职责边界：[`Interview Pack`](./00_Interview_Pack.md) 负责 **Direct Answer / Stop Depth / Evidence Provenance**；本 Index 负责 27 类题目的检索与深层展开。不要用本文件的展开骨架替代第一句话的直接回答。

---

# 0. 深层展开骨架（Direct Answer 之后）

面对开放题，先按 Interview Pack：

```text
Direct Answer
→ Boundary
→ Mechanism / Evidence
→ Example
→ Broader System only if needed
```

只有当面试官继续追问、需要把问题展开成完整项目逻辑时，再使用：

```text
Define
→ Diagnose
→ Hypothesize
→ Construct
→ Verify
→ Experiment
→ Flywheel
```

也就是：

1. 先定义目标能力、对象和成功标准；
2. 再定位 failure / gap；
3. 明确为什么某类 data / intervention 可能有用；
4. 说明数据怎么构造；
5. 说明 label / verifier / judge 怎么来；
6. 说明如何做 controlled experiment；
7. 说明上线后怎样监控和回流。

这是一套 **deep-expansion map**，不是所有回答必须逐步走完的固定 chain。

---

# 1. “你理解的大模型数据工作是什么？”

## 推荐结构

```text
不是 collect + label
而是 Learning System Design
```

展开：

```text
Pretraining Data
Post-training Data
Preference / Reward
Reasoning / Process
Agent Trajectory
Synthetic / Human
Evaluation / Benchmark
Data Flywheel
```

## 章节

Ch0 / Ch1 / Ch17 / Ch25

## Figure

F1

---

# 2. “SFT、Preference、Reward Data 有什么区别？”

## 答题重点

```text
SFT
→ demonstration imitation

Preference
→ relative desirability

Reward
→ optimization scalar
```

补充：

```text
Outcome ≠ Reward ≠ Credit
```

## 章节

Ch1 / Ch2 / Ch3 / Ch13

## Figure

F2

---

# 3. “怎么设计一批高质量 SFT 数据？”

## 结构

```text
Target Capability
→ Task Distribution
→ Demonstration Source
→ Verification
→ Diversity / Difficulty
→ Curation
→ Matched-budget Experiment
```

## 章节

Ch2 / Ch6 / Ch7 / Ch20 / Ch21

## 加分点

不要只说：

```text
人工写高质量答案
```

要说明：

```text
target distribution realism
coverage
decision diversity
verifiability
learning value
```

---

# 4. “Synthetic Data 怎么做？风险是什么？”

## 结构

```text
Seed
→ Generator
→ Evolution / Variation
→ Verifier
→ Diversity Audit
→ Curation
→ Downstream Validation
```

## 风险

```text
Teacher Bias
Mode Collapse
Model Monoculture
Contamination
Surface-only Diversity
Weak Verifier
```

## 章节

Ch7 / Ch20 / Ch21

---

# 5. “什么样的 Preference Pair 更有价值？”

## 重点

```text
不是 perfect vs garbage 越多越好
```

看：

```text
near-boundary
hard negative
constraint difference
same-context decision contrast
label reliability
```

## 章节

Ch3 / Ch6 / Ch8

---

# 6. “如何验证 LLM Judge 靠谱？”

## 结构

```text
Gold / Anchor
→ Agreement
→ FP / FN
→ Position Swap
→ Verbosity / Style Bias
→ High-risk Slice
→ Abstention
→ Version / Drift Monitoring
```

## 章节

Ch15 / Ch23

## Figure

F7 / F13

---

# 7. “Verifier、Grader、Judge 有什么区别？”

## 最佳回答顺序

```text
Evidence first
```

然后：

```text
Verifier
→ objective / executable condition

Grader
→ structured broader scoring

Judge
→ interpretive evaluator, often LLM
```

## 章节

Ch15

## Figure

F7

---

# 8. “怎么设计一个 Agent Benchmark？”

## 结构

```text
Capability Taxonomy
→ Task Contract
→ Environment / Tools
→ Success / Forbidden Predicates
→ Frozen Protocol
→ Evaluator
→ Population / Budget
→ Repeated Runs
→ Statistics / Claim Scope
```

## 章节

Ch10 / Ch11 / Ch15 / Ch16

## Figure

F4 / F8

---

# 9. “Agent 任务为什么不能只看 Final Answer？”

## 举例

Agent 说：

```text
“会议已经改好了。”
```

但真实 Calendar state 没变。

## 核心

```text
Final Language
≠ Task Success
```

需要：

```text
Tool / State / Side Effect / Final Environment
```

## 章节

Ch5 / Ch11 / Ch12 / Ch15

## Cases

C1 / C2

---

# 10. “什么是 Agent Trajectory Data？”

## 答题结构

```text
Task / Case
+
State
+
Decision
+
Action
+
Tool / Environment Result
+
Observation
+
Final State / Outcome
+
Metadata / Versions
```

## 关键区别

```text
Trajectory ≠ Chat Log
```

## 章节

Ch5 / Ch12

## Figure

F5

---

# 11. “怎么做 Agent Failure Taxonomy？”

## 不要只列错误类型

回答：

```text
Outcome
→ Symptom
→ Localization
→ Mechanism
→ Root Cause
→ Owner
→ Severity / Detectability
→ Repairability
→ Routing
```

## 章节

Ch13 / Ch14

## Figure

F6

---

# 12. “怎么判断一个 bad case 值不值得做成训练数据？”

## 答题维度

```text
Frequency
Severity
Capability Gap
Learnability
Recoverability
Verifiability
Novelty
Transfer Potential
Cost
```

## 章节

Ch9 / Ch18

## Figure

F10

---

# 13. “Hard Case 越多越好吗？”

## 核心回答

```text
Hard ≠ Valuable
```

需要看：

```text
frontier
learnability
noise
verification
marginal utility
```

## 章节

Ch9 / Ch18 / Ch21

---

# 14. “给你 100 万条 Agent 数据，怎么筛？”

## 成熟 pipeline

```text
Integrity
→ Privacy / License
→ Exact / Near / Family Dedup
→ Executable / Rule Verification
→ Model Quality Labels
→ Human Disagreement / High-risk Review
→ Capability / Difficulty / Failure Tags
→ Distribution Audit
→ Mixture
→ Downstream Ablation
```

## 章节

Ch20 / Ch21

---

# 15. “怎么证明这批数据真的有用？”

## 核心

```text
把 Data 当 intervention
```

回答：

```text
Hypothesis
→ Baseline
→ Add / Replace / Remove
→ Matched Token / Compute Budget
→ Frozen Train Recipe
→ Frozen Eval
→ Target + Regression
→ Multi-seed if needed
→ Scaling Curve
→ Transfer
→ Cost / ROI
→ Scale / Stop
```

## 章节

Ch16 / Ch21

## Figure

F8 / F10

---

# 16. “数据量和数据质量哪个更重要？”

## 不做二选一

回答：

```text
看 target capability 下的 marginal downstream gain / cost
```

可以设计：

```text
10k expert
vs
50k medium
vs
100k synthetic
vs
hybrid
```

## 章节

Ch18 / Ch21

---

# 17. “如何决定 Data Mixture？”

## 结构

```text
Capability Targets
→ Source / Difficulty / Failure Buckets
→ Token Exposure
→ Positive / Negative / Recovery Balance
→ Weight Sweep
→ Regression / Pareto
→ Rebalance with Drift
```

## 章节

Ch20 / Ch21 / Ch23

---

# 18. “怎么避免训练 / 评测数据泄漏？”

## 不止 exact dedup

```text
Exact
Near
Semantic
Seed Family
Workflow
Synthetic Derivative
Solution Leakage
Teacher Leakage
```

## 章节

Ch16 / Ch19 / Ch20

---

# 19. “Data Lineage 为什么重要？”

## 回答

为了回答：

```text
这个结论来自哪套数据？
这些数据怎么加工？
哪个 label / judge / verifier？
哪个 training run？
哪个 model / report？
```

## 章节

Ch19

## Figure

F11

---

# 20. “怎么设计一个大模型数据生产平台？”

## 结构

```text
Production Contract
→ Job / Queue
→ Worker
→ Artifact / Metadata
→ Retry / Idempotency
→ Verification / Human
→ Routing
→ Dataset Builder
→ Cost / Yield Dashboard
→ Experiment Handoff
```

## 章节

Ch22

## Figure

F12

---

# 21. “系统 retry 和 Agent recovery 有什么区别？”

## 关键

```text
System Retry
= infrastructure behavior

Agent Recovery
= policy capability
```

不能让 production harness 替模型修错后，还把结果记成模型 recovery。

## 章节

Ch22

## Case

C3-F4

---

# 22. “线上指标掉了你会怎么排查？”

## 答题顺序

```text
Metric Definition
→ Judge / Verifier
→ Tool / Harness / Environment
→ Traffic Mix
→ Business Rule
→ Frozen Benchmark
→ Failure Composition
→ Fresh Cohort
→ Root Cause
→ Intervention
```

## 章节

Ch23

## Figure

F13

---

# 23. “什么是 Data Drift / Concept Drift？”

## 简洁区分

```text
Data Drift
P(X) changed

Concept Drift
P(Y|X) / correct behavior changed
```

Agent 还要加：

```text
Failure Drift
Judge Drift
Tool / Harness / Environment Drift
```

## 章节

Ch23

---

# 24. “怎么搭 Data Flywheel？”

## 不要回答

```text
收 bad case → 训模型
```

而要回答：

```text
Signal
→ Triage
→ Attribution
→ Capability Gap
→ Prioritize
→ Acquire
→ Supervise
→ Curate
→ Experiment
→ Train
→ Eval
→ Deploy
→ Monitor
```

## 章节

Ch17

## Figure

F9

---

# 25. “遇到线上 failure，什么时候该补数据，什么时候该修系统？”

## 推荐 gate

```text
Requirement
→ Tool
→ Harness
→ Environment
→ Evaluator
→ Model
→ Data Gap
```

只有确认是：

```text
Coverage / Supervision / Distribution Gap
```

才进入 Data Intervention。

## 章节

Ch14 / Ch24 / Ch25

## Figure

F14

---

# 26. “如果让我负责一个数据项目，我怎么推进？”

## 先判断项目入口

不要默认所有项目都从 bad case / A1 开始。先按 [`Project Starter Pack`](./00_Project_Starter_Pack.md) 判断：

```text
Failure-led
Monitoring-led
Hypothesis-led
Evaluation-led
Asset-led / Curation-led
```

然后汇合到：

```text
Relevant Contract + Evidence
→ Controlled Change
→ Evaluation
→ Decision
→ Monitoring / Re-entry
```

如果面试官继续追问完整推进逻辑，再用本 Index 的 deep-expansion map：

```text
Define
→ Diagnose
→ Hypothesize
→ Construct
→ Verify
→ Experiment
→ Flywheel
```

并补：

```text
Owner
Budget
Exit Criteria
Scale / Stop Rule
Monitoring
```

关键不是把所有项目强行走成同一条 chain，而是：**入口可以不同，Evidence / Comparison / Decision discipline 不能降级。**

## 章节

Ch21 / Ch24 / Ch25

---

# 27. 面试表达成熟度差异

## 初级

```text
我会收集更多 bad case，清洗以后训练。
```

## 中级

```text
我会按 failure type 分桶，构造 targeted data，再做离线评测。
```

## 高级

```text
我会先验证 root cause 和 Data Problem Gate，再定义 capability-level hypothesis；用最小数据 pilot 和 matched-budget experiment 验证 learning value，同时看 transfer、regression、cost 和 marginal utility，最后决定 scale / stop，并把线上 drift 接回下一轮 acquisition。
```

区别不在术语多少，而在：

> **有没有把问题、证据、干预和决策连成因果链。**
