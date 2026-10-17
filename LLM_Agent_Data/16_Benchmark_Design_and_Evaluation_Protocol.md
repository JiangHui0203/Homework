# 第 16 章 Benchmark Design 与 Evaluation Protocol：一个“更好”的结论到底怎样才成立

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 15 章 Grader、Verifier 与 LLM-as-a-Judge`](./15_Grader_Verifier_and_LLM_as_a_Judge.md)
>
> 关联章节：[`第 9 章 Hard Case Mining 与 Curriculum`](./09_Hard_Case_Mining_and_Curriculum.md)、[`第 10 章 Agent Task Design`](./10_Agent_Task_Design.md)、[`第 11 章 Environment Design`](./11_Environment_Design.md)、[`第 13 章 Task Success 与 Credit Assignment`](./13_Task_Success_and_Credit_Assignment.md)、[`第 14 章 Agent Failure Taxonomy`](./14_Agent_Failure_Taxonomy.md)、[`第 21 章 Data Experiments`](./21_Data_Experiments_and_Causal_Validation.md)、[`第 23 章 Monitoring 与 Drift`](./23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**Benchmark Object / Evaluation Protocol / Evaluation Run / Report、Population Accounting、Paired / Matched Comparison、Budget Matching、Statistics、Claim Scope 的 canonical chapter。**
>
> 本章核心问题：**评测不是“跑一个分数”，而是在受控条件下回答：测的到底是什么能力、对哪一群 case 成立、比较是否公平、提升是否稳定、代价是多少、退化发生在哪里，以及这些证据究竟允许我们把结论说到多大。**

---

# 16.0 先把四个对象分开：Benchmark、Protocol、Run、Report

这四个词经常混用。

## Benchmark

> **被定义好的测量对象。**

它包括：

```text
Cases
Capability / Slice Metadata
Evaluation Targets
Benchmark Version
```

Agent Benchmark Case 通常还绑定：

```text
Task Contract
Environment Snapshot
Toolset / Permission
Success / Forbidden Predicates
```

---

## Evaluation Protocol

> **规定 Benchmark 应怎样被运行、判分、聚合和比较的协议。**

包括：

```text
Prompt / Runtime
Generation Config
Tool / Harness / Environment
Budget / Stop Rules
Evaluator
Metric Definition
Aggregation
Seed Policy
Inclusion / Exclusion Rules
```

---

## Evaluation Run

> **某个具体 Model / Method 在某个 Benchmark + Protocol 上的一次实际执行。**

它产生：

```text
Raw Outputs
Trajectories
Per-case Evidence
Labels
Costs
Runtime Logs
```

---

## Evaluation Report

> **把一组 Run 经过预先定义的统计与分析规则转成可解释结论。**

所以：

```text
Benchmark
≠ Protocol
≠ Run
≠ Report
```

这一点是后续所有复现与历史重算的基础。

---

# 16.1 先定义 Evaluation Question，不要先找 Dataset

好的评测先问：

> **我们到底想知道什么？**

例如：

```text
模型数学 reasoning 更强吗？
Agent 更会处理 negative constraint 吗？
新 policy 是否减少 harmful write？
增加 test-time compute 是否值得？
Selector 是否能在线识别更优 candidate？
同预算下新方法是否更优？
```

这些问题对应完全不同的：

```text
Population
Protocol
Metric
Budget
Statistical Test
Claim Scope
```

因此 Evaluation Question 至少明确：

```text
Target Capability
Target Population
Compared Systems / Intervention
Primary Metric
Secondary / Guardrail Metrics
Budget Constraint
Failure Cost
Claim Scope
```

---

# 16.2 Capability Taxonomy：Dataset 名称不是能力名称

```text
AIME
MATH
LiveBench
```

是 benchmark / dataset 名称，不是 capability 本身。

Agent capability 可以拆：

```text
Task Understanding
Constraint Following
Planning
Tool Selection
Argument Construction
Observation Grounding
State Tracking
Memory
Recovery
Verification
Termination
Permission / Safety
Final Communication
```

好的 taxonomy 应：

```text
可解释
可操作
能映射 failure taxonomy
能映射 data strategy
不过度绑定某一个 benchmark
```

太宽的：

```text
Agent Ability
```

缺乏诊断性。

太窄的：

```text
某 API 第三个字段能否填对
```

又缺乏迁移价值。

---

# 16.3 Scope 与 Claim：评多少，就说多少

Benchmark Scope 至少包括：

```text
Domain
Task Family
Difficulty Range
Language
Environment / Tool Type
Model Family
Budget Range
Interaction Horizon
Risk Level
```

如果只测一个窄 cohort，就不应直接宣称：

```text
“普遍提升 Agent capability”
```

更严谨：

> **在当前模型、任务 population、budget 与 frozen protocol 下，观察到……**

所以 Claim Scope 是 Protocol 的一部分，不是论文写作最后才补的一句话。

---

# 16.4 Benchmark Case：不是一个 Prompt String

普通 QA Case 可能只有：

```text
input
reference / verifier
metadata
```

Agent Case 更接近：

```text
Task Contract
+
Initial Environment Snapshot
+
Agent-visible / Hidden Information
+
Toolset / Permission
+
Success / Forbidden / Invariant Predicates
+
Termination
+
Verifier
+
Metadata
```

因此：

```text
Benchmark Case
≠ Prompt
```

它应该使用第 10 章的 canonical Case 定义。

---

# 16.5 Benchmark Set 的四种功能

成熟体系通常同时需要：

## Representative Set

近似目标总体分布，用于估计真实平均表现。

## Challenge / Frontier Set

集中于难例、边界、高价值 capability gap。

## Regression Set

确保历史修过的问题不再复发。

## Safety / High-risk Set

集中检查低频但高严重度 failure。

所以：

```text
Challenge Performance
≠ Population Performance
```

也不能用 Regression Set 的比例直接解释线上成功率。

---

# 16.6 Sampling：样本从哪里来，结论就带有什么偏差

来源：

```text
Random Production Logs
Stratified Sampling
Human / Expert Design
Synthetic Generation
Failure Mining
Adversarial Generation
Counterfactual Generation
```

Random Sampling 更接近真实 traffic，但容易被大量简单 case 淹没。

Stratified Sampling 提高 coverage，但若要恢复真实总体指标，可能需要按 reference distribution 重新加权。

Challenge Sampling 适合 frontier，不适合估算 overall population success。

所以 Benchmark Report 应说明：

```text
Sampling Frame
Sampling Policy
Weights if any
Selection Bias
```

---

# 16.7 Split：Agent 场景不能只做随机 Row Split

如果：

```text
Train:
取消订单 1001
取消订单 1002

Test:
取消订单 9999
```

很可能只是 surface change。

更可靠的 holdout 可以按：

```text
family_id
workflow_id
seed_id
tool combination
constraint pattern
environment layout
failure mode
domain
```

做 group split。

同一个 synthetic seed / workflow 派生出的 sibling cases 应尽量整体分组，避免 family leakage。

---

# 16.8 Contamination 与 Leakage

至少区分：

```text
Train / Pretraining Contamination
Near-duplicate Exposure
Solution / Reference Exposure
Workflow / Family Leakage
Leaderboard Overfitting
Verifier Leakage
Agent Memory Leakage
```

Verifier Leakage 指运行时把：

```text
hidden tests
gold state
future outcome
oracle action
```

泄漏给 policy。

这与训练前 benchmark contamination 是不同位置的问题。

完整 evaluator-only evidence boundary 见第 15 章。

---

# 16.9 Evaluation Contract：真正要冻结的是什么？

可以把协议写成一个显式 Contract：

```text
Benchmark Version
Case Manifest
Inclusion / Exclusion Rule
Model / Checkpoint
Prompt / System / Template
Tokenizer
Decoding / Sampling Config
Seed Policy
Toolset / Schema
Harness
Environment Snapshot / Clock
Budget
Stop / Timeout
Evaluator / Rubric / Verifier
Metric Definitions
Aggregation Rules
Population Denominators
Reporting Schema
```

即：

```text
Evaluation Contract
=
Benchmark
+
Runtime
+
Budget
+
Measurement
+
Reporting Semantics
```

如果其中一项改变，至少应该产生新的 protocol / run version，而不是悄悄覆盖旧结果。

---

# 16.10 Frozen Protocol：只改变你真的想研究的变量

例如比较：

```text
Baseline
vs
New Selector
```

就应尽量保持：

```text
same model
same prompt
same candidate generator
same toolset
same environment
same budget semantics
same evaluator
```

只改变：

```text
selector
```

如果 Prompt、Judge、Temperature、Tool timeout 同时都变了，最终 delta 无法归因。

所以：

> **Frozen Protocol 是“可解释差异”的前提。**

---

# 16.11 Population Accounting：先回答“这 80% 到底是谁的 80%？”

Routing / Trigger / Abstention 系统尤其容易分母混乱。

建议显式区分：

```text
Full Population
↓
Eligible Population
↓
Screened Population
↓
Triggered Population
↓
Intervened Population
↓
Resolved Population
```

具体系统不一定全部有这些层，但只要存在，就应分别记录。

例如：

```text
Trigger Rate
= Triggered / Screened
```

而：

```text
End-to-end Success
= Successful Final Outcomes / Full Population
```

不能把 triggered-only success 冒充 full-population success。

---

## 16.11.1 Denominator Discipline

每一个百分比最好都能回答：

```text
Numerator
Denominator
Inclusion Rule
Exclusion Rule
```

例如：

```text
Replacement Precision
= beneficial replacements / all replacements

Rescue Opportunity Rate
= baseline-failure cases with a rescuing candidate
  / eligible baseline-failure cases
```

如果 denominator 口径不一致，不同表格里的“率”无法直接比较。

---

# 16.12 Paired Comparison：同一个 Case 上的变化最有信息量

两个系统都跑同一批 Case，可构造：

```text
A correct, B correct
A correct, B wrong
A wrong, B correct
A wrong, B wrong
```

真正有信息的是 discordant cells：

```text
Wrong → Right
Right → Wrong
```

相比只看：

```text
A = 72%
B = 75%
```

paired transition 能告诉我们：

```text
谁被 repair 了？
谁被 degrade 了？
净变化来自哪里？
```

---

# 16.13 Matched Comparison：把非研究变量尽量控制住

不仅 case 要相同，还可以进一步匹配：

```text
same Task
same Initial State
same Environment Snapshot
same Reasoning Prefix / Agent State
same Budget
same Candidate Count
```

只改变：

```text
Policy / Action / Intervention
```

这让局部差异更容易解释。

Reasoning same-prefix 与 Agent same-state counterfactual 都属于这一思想。

---

# 16.14 Rescue / Harmful / Neutral：本章只负责测量，不重新定义

第 4 / 13 章已定义：

```text
Baseline Fail → Intervention Success = Rescue
Baseline Success → Intervention Fail = Harmful
Both Success = Neutral-positive
Both Fail = Neutral-negative
```

本章重点是**如何报告**：

```text
Rescue Count / Rate
Harmful Count / Rate
Net Correct Change
Coverage
Intervention Rate
Conditional Gain
```

若 Rescue / Harmful 以同一 full-population denominator 计 rate，则：

```text
Accuracy Delta
=
Rescue Rate - Harmful Rate
```

若分母不同，则不能机械相减。

因此 `Net` 必须同时写清 numerator 与 denominator。

---

# 16.15 Trigger / Generator / Selector / E2E 必须拆开

Candidate-based system：

```text
State
↓
Trigger
↓
Candidate Generator
↓
Candidate Evaluator / Selector
↓
Commit
↓
Outcome
```

至少分别看：

```text
Trigger Coverage / Precision-like Utility
Candidate Oracle / Outcome Discordance
Selector Accuracy / Regret / Abstention
End-to-end Rescue / Harmful / Net
Compute Cost
```

如果 Oracle 很低：

```text
generator / action space 是瓶颈
```

如果 Oracle 高但 actual selection 差：

```text
selectability / selector 是瓶颈
```

不能把所有失败压成：

```text
“method 不行”
```

---

# 16.16 Oracle Analysis：上限是什么？

例如：

```text
Oracle@N
= N 个候选中至少存在一个成功候选的 Case 比例
```

它回答：

> **当前 Candidate Pool 给在线 Selector 留了多大可能空间？**

如果：

```text
Oracle@8 = high
Selected@8 = low
```

说明存在明显 Selection Gap。

但 Oracle 是 offline upper bound，不是 online achievable result；不能把未来 outcome information 偷渡到真实 selector。

---

# 16.17 Budget Matching：提升是方法带来的，还是“多花钱”带来的？

如果 Method 比 Baseline 多用：

```text
10× tokens
8 candidates
更多 tool calls
更长 latency
```

那么只比较 final accuracy 不公平。

需要根据研究问题设计：

```text
Token-matched Baseline
Compute-matched Baseline
Candidate-count-matched Baseline
Tool-call-matched Baseline
Latency-constrained Comparison
```

有时应该同时报告：

```text
Unmatched Practical Result
+
Budget-matched Scientific Comparison
```

因为两者回答不同问题。

---

# 16.18 Success@Budget 与 Pareto Frontier

对 test-time compute / Agent 系统更合理的问题常是：

```text
Success@TokenBudget
Success@ToolBudget
Success@LatencyBudget
Success@DollarBudget
```

一个系统：

```text
78% success @ 20k tokens
```

不一定比：

```text
76% success @ 3k tokens
```

更适合产品。

因此需要看：

```text
Quality–Cost Curve
Pareto Frontier
```

如果一个系统在质量不高、成本又更大，则被另一个系统 dominated。

---

# 16.19 Average Cost 与 Conditional Cost

按需触发方法经常：

```text
多数 Case 便宜
少数 Triggered Case 很贵
```

因此同时报告：

```text
Overall Mean / Median Cost
Triggered-case Cost
Non-triggered Cost
P90 / P95 Cost
Trigger Rate
```

只报其中一层都可能误导。

---

# 16.20 Repeated Runs：随机系统不能只跑一次

随机性可能来自：

```text
model sampling
tool stochasticity
environment randomness
judge randomness
```

重复运行用于估计 variance，不是为了挑最漂亮的一次。

需要区分：

```text
Train Seed
Inference Seed
Environment Seed
Judge Seed
```

如果研究成本很高，可以采用：

```text
cheap single-run exploration
↓
promising configurations
↓
multi-seed confirmatory run
```

完整数据实验阶段策略见第 21 章。

---

# 16.21 Statistical Uncertainty：点估计不是完整结论

报告：

```text
Accuracy = 73.2%
```

至少还要考虑：

```text
N
Raw Correct Count
Confidence Interval / Bootstrap Interval
Paired Structure
Repeated-case Dependency
```

常见工具：

```text
Binomial CI
Bootstrap
Paired Bootstrap
McNemar-style paired binary comparison
Cluster / Hierarchical Bootstrap
```

方法取决于数据结构。

如果一个 Case 产生多个 sibling trajectories，它们通常不是独立样本；把所有 row 当 IID 会低估 uncertainty。

---

# 16.22 Effect Size > 单独盯 p-value

统计显著不等于实践值得。

还要问：

```text
Effect Size
Confidence Interval
Cost
High-severity Regression
Target-slice Gain
Operational Relevance
```

例如：

```text
+0.3pt
但 compute +300%
```

可能没有部署价值。

所以：

> **CI + Effect Size + Cost + Risk，比一个孤立 p-value 更接近真实决策。**

---

# 16.23 Multiple Comparison 与 Winner’s Curse

如果你尝试：

```text
30 个 threshold
20 个 mixture
10 个 prompt
```

然后只报告最高的一个，很容易选中偶然赢家。

应考虑：

```text
predefined primary metric
exploratory vs confirmatory split
held-out confirmation
multiple-comparison awareness
```

不要在同一个 dev set 上：

```text
选配置
+
宣布最终结论
```

这会把 benchmark 变成 optimization target。

---

# 16.24 Pass@k 与 Single-run Accuracy

```text
Greedy Accuracy
Single-sample Accuracy
Pass@k
Best-of-N
Self-consistency
```

测的不是同一件事。

Pass@k 回答：

> 给 k 次生成机会，至少一次成功的概率有多大？

它更接近“候选产生能力”，不能直接和 greedy 单次成功率放同一口径下解释为等价系统性能。

---

# 16.25 Selective Prediction：Coverage 与 Risk 要一起看

系统如果可以：

```text
Answer
Abstain
Escalate
```

就不能只报被处理样本里的高 accuracy。

至少看：

```text
Coverage
Success@Coverage
Risk@Coverage
Abstention / Escalation Rate
```

常见关系：

```text
Coverage ↑
Risk 通常也 ↑
```

因此 Risk–Coverage Curve 比单个 threshold 更完整。

---

# 16.26 Slice Analysis：总体平均会掩盖异质性

总体：

```text
+2.1pt
```

可能来自：

```text
Math +8
Code +4
Agent -3
Safety -5
```

因此至少按：

```text
Task Family
Capability
Difficulty
Failure Type
Risk / Severity
Domain / Language
```

做 breakdown。

对 high-risk slice，哪怕总体提升也不能自动抵消关键 regression。

---

# 16.27 Micro / Macro / Weighted Average

如果不同 slice 大小差异很大：

```text
Micro
→ 每个 Case 同权

Macro
→ 每个 Group / Dataset 同权

Weighted
→ 按目标 traffic / business weight
```

三者回答不同问题。

必须说明 aggregation rule，不能只写“平均准确率”。

---

# 16.28 Ablation 与 Strong Baseline

完整方法：

```text
Trigger
+
Generator
+
Selector
+
Verifier
```

如果整体变好，仍然不知道贡献来源。

可做：

```text
No Trigger
Random Trigger
No Selector
Random Selector
Different N
Different Score
No Verification
Greedy-only
Budget-matched Simple Baseline
```

Strong Baseline 的目标不是“让新方法难赢”，而是回答：

> **复杂机制是否真的超出了一个简单、合理、同预算替代方案。**

---

# 16.29 Negative Result 的 Claim Scope

没有提升时，先检查：

```text
Oracle / Candidate Space 是否有上限？
样本量 / power 是否足够？
Metric 是否测到目标？
Implementation 是否正确？
Online feature 是否包含所需信息？
Protocol 是否过窄？
```

更严谨的结论：

> **在当前样本、模型、表示、预算与 protocol 下，没有观察到稳定可兑现收益。**

而不是直接：

```text
“这种 signal 不存在”
```

Negative Result 也必须有边界。

---

# 16.30 Corrected Labels：Re-score ≠ Re-run

历史 Run 已经产生：

```text
Raw Outputs
Policy Decisions
```

后来 Gold / Judge 被修正。

正确历史重算：

```text
冻结历史 Outputs / Decisions
↓
使用 Corrected Labels
↓
Re-score / Re-aggregate
```

而：

```text
重新运行当前 Policy / Judge
```

是新的实验。

因此区分：

```text
Re-score
Re-run
Replay
```

完整版本治理归第 19 章。

---

# 16.31 Evaluation Lineage：一个分数必须能追到 Case

最终 Metric 应能追溯：

```text
Benchmark / Case Version
Protocol Version
Model / Prompt
Runtime / Environment
Raw Output / Trajectory
Evidence
Evaluator Version
Per-case Labels
Aggregation Script
Metric Definition
```

原则：

```text
Raw Run Immutable
Labels Versioned
Metrics Recomputable
```

只有一个：

```text
accuracy = 76.2%
```

但没有 per-case artifacts，几乎不可审计。

---

# 16.32 Leaderboard Overfitting 与 Benchmark Saturation

反复：

```text
看 test score
→ 调 prompt / policy
→ 再看 test
```

Test 实际已经变成 Dev。

缓解：

```text
private test
fresh holdout
rotating cases
limited reveal
confirmatory set
```

另一方面，如果所有强模型都：

```text
97–99%
```

Benchmark 已经 saturation。

应补：

```text
真实新 failure
new capability slice
longer horizon
higher-risk constraints
frontier cases
```

而不是为了“难”制造怪题。

---

# 16.33 Stable Ruler 与 Moving Frontier 的分工

长期系统最好同时有：

```text
Frozen Core
→ 稳定纵向比较 / regression / release gate

Fresh Frontier
→ 新 failure / 新 task / 新 tool / 新 policy
```

本章负责 Frozen Core 的**measurement protocol**。

Frontier 如何持续刷新、如何识别 drift，归第 23 章。

这两个集合不能互相替代。

---

# 16.34 Offline → Shadow → Canary → Online

典型验证梯度：

```text
Offline Frozen Benchmark
↓
Shadow Evaluation
↓
Canary
↓
Limited Online
↓
Production Monitoring
```

Shadow 允许 Candidate Policy 处理真实 request，但不产生真实 side effect。

Canary 则逐步扩大真实 exposure，并持续看：

```text
Primary Metric
Guardrail
High-severity Failure
Cost
Latency
Runtime Health
```

线上部署方法的完整 drift / rollback 机制在第 23 章展开。

---

# 16.35 Safety-critical Evaluation：平均成功率不够

高风险系统至少单独报告：

```text
Unauthorized Action Rate
Irreversible Harm Rate
Privacy Violation Rate
Policy Violation Rate
Hallucinated Success Rate
Safe Abort / Escalation Quality
```

即使：

```text
Overall Success ↑
```

也不能自动抵消 critical guardrail regression。

---

# 16.36 Benchmark Report 最低信息集

```text
1. Evaluation Question
2. Target Population / Capability
3. Benchmark + Case Version
4. Sampling / Inclusion / Exclusion
5. Frozen Protocol
6. Compared Systems / Baselines
7. Primary Metric
8. Guardrail / Cost Metrics
9. Population Accounting
10. Per-case / Slice Results
11. Paired Transition Analysis
12. Statistical Uncertainty
13. Ablations
14. Failure Breakdown
15. Cost / Budget Accounting
16. Known Limitations / Claim Scope
17. Artifact / Lineage References
```

如果缺少这些信息，漂亮数字也很难复用。

---

# 16.37 推荐的 Evaluation Protocol Template

```yaml
question: "..."
claim_scope: "..."

population:
  benchmark_version: "..."
  case_manifest: "..."
  sampling_policy: "..."
  inclusion_rule: "..."
  exclusion_rule: "..."

systems:
  baseline: "..."
  treatment: "..."

frozen_runtime:
  model: "..."
  prompt: "..."
  generation_config: "..."
  toolset: "..."
  harness: "..."
  environment: "..."
  budget: "..."

measurement:
  evaluator_contract: "..."
  primary_metric: "..."
  guardrails: []
  cost_metrics: []

analysis:
  paired: true
  uncertainty: "paired bootstrap"
  population_accounting: true
  slices: []

artifacts:
  raw_outputs: "..."
  per_case_labels: "..."
  summary: "..."
```

这不是固定格式，重点是把实验语义显式化。

---

# 16.38 研究实例：固定深度 reasoning 为什么需要 Transition Analysis？

只看：

```text
Depth 1
Depth 2
Depth 3
```

的平均 accuracy，可以发现总体非单调。

但只有进一步看：

```text
Wrong → Right
Right → Wrong
```

才能知道额外计算同时产生：

```text
repair
+
degradation
```

于是问题会从：

```text
“多想一轮平均有没有用？”
```

升级成：

```text
“哪些 current states 值得继续投入 compute？”
```

这就是 Paired Transition Analysis 的价值。

---

# 16.39 研究实例：Trigger / Candidate / Selector 系统如何拆解

对于状态触发的 candidate intervention：

```text
Full Population
↓
Screening
↓
Triggered / Non-triggered
↓
Candidate Generation
↓
Selection
↓
Final Outcome
```

必须分别回答：

```text
Trigger 把预算用到哪里？
Candidate pool 是否含 better future？
Selector 是否可在线识别？
Rescue 是否大于 Harmful？
Full-population net gain 是多少？
Cost 增加在哪里？
```

Non-triggered Cases 仍属于 Full Population。

所以 routing 方法的 E2E 结论绝不能只统计 intervention subset。

---

# 16.40 常见 Failure Modes

### 失败 1：Dataset 名字当 Capability

只能说明“这个 dataset 上变化了”。

### 失败 2：Benchmark、Protocol、Run 混在一起

版本变化后无法解释历史数字。

### 失败 3：只报告 Overall Accuracy

看不到 repair / degradation / slice regression。

### 失败 4：Baseline 与 Method Budget 不一致

Compute advantage 被当 method advantage。

### 失败 5：Protocol 同时改多个变量

归因失败。

### 失败 6：Random Row Split 导致 workflow / family leakage

Surface novelty 不等于 generalization。

### 失败 7：Challenge Set 冒充 Population Performance

Sampling bias 被忽略。

### 失败 8：Triggered-only Metric 冒充 E2E Metric

分母错误。

### 失败 9：Percentage 不写 Numerator / Denominator

口径无法审计。

### 失败 10：Repeated sibling rows 当 IID

统计 uncertainty 被低估。

### 失败 11：只报 p-value

不看 effect size / CI / cost / risk。

### 失败 12：大量试配置后只报最高分

Winner’s curse。

### 失败 13：Corrected Label 后 Re-run 再冒充历史结果

破坏历史不可变性。

### 失败 14：Negative Result 直接上升成“signal 不存在”

超出协议支持范围。

### 失败 15：只有 Aggregate，没有 Per-case Artifact

结果不可审计。

---

# 16.41 从数据 / Eval 岗视角，这一章实际会做什么？

```text
定义 evaluation question
设计 capability taxonomy
构造 representative / challenge / regression / safety set
设计 group split
做 contamination audit
冻结 evaluation contract
跑 strong / budget-matched baseline
做 population accounting
做 paired transition analysis
统计 Rescue / Harmful
计算 CI / bootstrap
做 ablation
做 cost accounting
做 slice / failure breakdown
维护 benchmark / protocol / label version
保存 per-case artifact
写 claim scope / limitation
```

核心能力不是：

> “会跑 Benchmark。”

而是：

> **知道一个数字在什么条件下可解释、是否公平、是否稳定，以及它究竟支持多大的结论。**

---

# 16.42 本章关键词

| 术语 | Canonical meaning |
|---|---|
| Benchmark | 被定义好的 Case / Capability 测量对象 |
| Evaluation Protocol | 如何运行、判分、聚合和比较的协议 |
| Evaluation Run | 一个具体系统在某协议下的一次执行 |
| Evaluation Report | 对一组 Run 的统计、分析与结论 |
| Evaluation Contract | Benchmark + Runtime + Budget + Measurement + Reporting Semantics |
| Representative Set | 用于估计目标总体表现的样本 |
| Challenge Set | 聚焦能力边界 / 难例的样本 |
| Regression Set | 防止历史 failure 复发的冻结资产 |
| Population Accounting | 明确 full / eligible / triggered / intervened 等人数关系 |
| Denominator Discipline | 所有 rate 明确 numerator / denominator / inclusion rule |
| Paired Comparison | 在同一 Case 上比较系统 |
| Matched Comparison | 控制 Case / State / Budget 等非研究变量 |
| Oracle@N | Candidate pool 中至少存在一个成功 candidate 的比例 |
| Success@Budget | 给定预算下的成功率 |
| Coverage | 系统实际处理 / 干预的 population 比例 |
| Rescue / Harmful | 相对 baseline 的 outcome transition |
| Pareto Frontier | 质量–成本空间中不被其他系统同时支配的点 |
| Claim Scope | 当前证据允许结论覆盖的范围 |
| Evaluation Lineage | 从 Aggregate Metric 追溯到 Run / Case / Evidence / Label |

更完整定义见 [`Canonical Glossary`](./00_Glossary_and_Notation.md)。

---

# 16.43 面试 / 自检问题

1. Benchmark、Protocol、Run、Report 有什么区别？
2. 为什么 Dataset 名字不能直接当 Capability？
3. Representative / Challenge / Regression / Safety Set 如何分工？
4. Agent split 为什么不能只随机分 row？
5. Evaluation Contract 至少冻结什么？
6. 什么是 Population Accounting？
7. 为什么 Triggered-only 结果不能冒充 Full-population 结果？
8. Denominator Discipline 是什么？
9. Paired 与 Matched Comparison 有什么区别？
10. Rescue / Harmful 如何进入 E2E Accuracy Delta？
11. Trigger / Generator / Selector 为什么要拆开评？
12. Oracle@N 说明什么，不说明什么？
13. 怎样设计 Budget-matched Baseline？
14. Success@Budget 为什么比单纯 accuracy 更适合部分系统？
15. Average Cost 与 Conditional Cost 为什么都要报？
16. Multiple Seeds 的目的是什么？
17. Sibling trajectories 为什么不能简单当 IID？
18. 什么时候用 Paired Bootstrap / McNemar / Cluster Bootstrap？
19. Effect Size 与 p-value 有什么不同？
20. Winner’s Curse 怎么产生？
21. Pass@k 和 Greedy Accuracy 为什么不能混用？
22. Coverage 与 Risk 为什么必须一起看？
23. Micro / Macro / Weighted Average 各回答什么问题？
24. Negative Result 如何限定 Claim Scope？
25. Re-score、Re-run、Replay 有什么区别？
26. 什么是 Leaderboard Overfitting？
27. Frozen Core 与 Fresh Frontier 如何分工？
28. 为什么 high-risk regression 不能被 overall gain 抵消？
29. 一个 Benchmark Report 至少应该包含什么？
30. 如何证明“提升”不是更多 compute、不同 Judge 或不同 Runtime 造成的？

---

## 16.43.1 通用回答框架：设计一套 Agent Benchmark

```text
1. 定义 Evaluation Question / Claim Scope
   ↓
2. 定义 Capability / Target Population
   ↓
3. 构造 Representative + Challenge + Regression + Safety Slices
   ↓
4. 冻结 Case Contract / Environment / Evaluator
   ↓
5. 做 Family / Workflow Split 与 Leakage Audit
   ↓
6. 建 Strong + Budget-matched Baseline
   ↓
7. 显式记录 Population Accounting
   ↓
8. 做 Paired Per-case Comparison
   ↓
9. 报 Primary + Guardrail + Cost + Coverage
   ↓
10. 用合适的 CI / Paired / Cluster-aware Statistics
   ↓
11. 做 Slice / Failure / Ablation Analysis
   ↓
12. 保存 Raw Run / Per-case Label / Aggregation Lineage
   ↓
13. 只做与 Evidence Scope 一致的结论
```

---

# 16.44 与后续章节的关系

```text
第 21 章 Data Experiments
→ 把 Frozen Evaluation 用于验证“这批数据是否真的带来因果增益”

第 23 章 Monitoring
→ 把 Frozen Core 与 Fresh Frontier 用于长期 drift / release 管理

第 19 章 Governance
→ Run / Label / Protocol 的 versioning 与 reproducibility
```

本章只负责：

> **如何公平、稳定、可审计地比较系统并控制 Claim Scope。**

---

# 16.45 本章最终要形成的认识

```text
Evaluation Question
        ↓
Target Population / Capability
        ↓
Benchmark Object
        ↓
Evaluation Contract
        ↓
Frozen / Matched Runs
        ↓
Evidence-based Labels
        ↓
Population Accounting
        ↓
Paired + Budget-aware + Uncertainty-aware Analysis
        ↓
Slice / Failure / Cost Analysis
        ↓
Claim with Explicit Scope
```

真正可信的结论必须回答：

```text
对谁提升？
提升什么？
相对什么 baseline？
在什么预算下？
哪些 case 被 repair？
哪些 case 被 harm？
统计不确定性多大？
有没有关键 regression？
这个结论能推广到哪里？
```

最终原则：

> **Benchmark 不是制造漂亮分数的工具，而是一套让比较结论可解释、可复现、可审计、可限定边界的 measurement system。**

下一阶段将从 Measurement 进入 Data Lifecycle：

> **如何让这些可信的 failure、label 与 benchmark evidence 回流，决定下一轮到底生产什么数据、投多少预算，并证明数据真的值得。**