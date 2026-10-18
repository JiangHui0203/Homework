# 第 18 章 Data Strategy 与 Data Valuation：把有限预算投到最值得学的地方

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 17 章 Data Flywheel`](./17_Data_Flywheel_and_Continuous_Improvement.md)
>
> 关联章节：[`第 9 章 Hard Case Mining`](./09_Hard_Case_Mining_and_Curriculum.md)、[`第 16 章 Benchmark Design`](./16_Benchmark_Design_and_Evaluation_Protocol.md)、[`第 20 章 Data Quality / Mixture`](./20_Data_Quality_Filtering_Deduplication_and_Mixture.md)、[`第 21 章 Data Experiments`](./21_Data_Experiments_and_Causal_Validation.md)、[`第 23 章 Monitoring 与 Drift`](./23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**Data Strategy / Data Valuation / Portfolio / ROI / Marginal Utility / Stop Rule 的 canonical chapter。它负责回答“为什么做这批数据、做多少、与其他方向相比是否更值、什么时候停”；Mixture 的技术实现归第 20 章，因果验证归第 21 章。**
>
> 本章核心问题：**当采集、标注、验证、训练、评测和工程预算都有限时，团队怎样把资源投入到边际能力收益最高、业务价值最高、风险最值得控制的数据上？**

---

# 18.0 Data Strategy = Resource Allocation under Uncertainty

当团队已经会：

```text
Human Annotation
Synthetic Generation
Rollout Mining
Verifier / Judge
Hard Case Mining
Data Flywheel
```

真正稀缺的东西就不再只是“数据生产能力”，而是：

```text
预算
时间
专家
训练算力
验证能力
工程注意力
```

因此 Data Strategy 回答的是：

```text
为什么做这个？
做多少？
现在做还是以后做？
和另一个方向相比哪个更值？
什么证据会让我们停止？
```

而不是“怎么生成”。

---

# 18.1 Data Asset、Data Batch、Data Investment

## Data Asset

可长期复用的数据资产：

```text
Human Gold Set
Agent Regression Set
Recovery Preference Pool
Verifiable Code Corpus
```

## Data Batch

某次具体生产：

```text
2026Q4_recovery_failures_v2
```

它有明确来源、版本、成本和用途。

## Data Investment

从战略视角看：

> **为了某个 Capability，我们投入了多少资源去生产、验证和训练某类数据，它最终带来了多少可测收益。**

所以一个 Data Investment 至少包括：

```text
Target Capability
Why Now
Source
Supervision Type
Quantity / Tokens
Quality Level
Total Cost
Training Exposure
Measured Delta
Risk / Business Impact
Decision
```

---

# 18.2 先从 Capability Portfolio 看预算，而不是从 Dataset 名字看预算

一个 Agent 可能包含：

```text
Task Understanding
Tool Selection
Argument Construction
Observation Grounding
Recovery
Verification
Termination
```

因此不应该只说：

```text
“今年做 100 万条 Agent Data”
```

而应维护类似：

| Capability | Current Level | Importance | Risk | Data Gap | Marginal Spend |
|---|---:|---:|---:|---:|---:|
| Tool Selection | High | High | Medium | Low | Medium |
| Recovery | Low | High | High | High | Low |
| Verification | Medium | High | High | High | Low |
| Tone | High | Medium | Low | Low | High |

它会直接暴露：

```text
Recovery / Verification 欠投
Tone 可能过度投入
```

这就是 Data Portfolio。

---

# 18.3 Capability Gap ≠ Benchmark Gap

一个 benchmark 分数低，不自动意味着值得投数据。

还要问：

```text
是否代表真实目标分布？
业务重要吗？
失败严重吗？
能被训练改善吗？
有没有更便宜的 Tool / Product / Harness 修复？
```

所以 Capability Opportunity 可以概念上写成：

\[
Opportunity(c)=f(
PerformanceGap,
Importance,
Risk,
Frequency,
Learnability,
AlternativeFixCost
)
\]

这里不是固定公式，而是强迫团队把“为什么值得做”讲清楚。

---

# 18.4 Is This a Data Problem?

Data Strategy 的第一道 Gate 应该是：

```text
Requirement unclear?
Tool broken?
Harness missing observation?
Environment infeasible?
Evaluator wrong?
```

如果答案是这些，就不应该优先做训练数据。

真正适合 Data Intervention 的通常是：

```text
Coverage Gap
Supervision Gap
Distribution Gap
Decision-boundary Gap
Recovery / Process Gap
```

因此：

> **Data Strategy 不是“怎样多做数据”，而是“什么时候数据才是正确 intervention”。**

---

# 18.5 Data Value 是条件化的，不存在脱离目标的“高价值数据”

一批数据可能：

```text
提升 Accuracy
但增加 Latency
```

也可能：

```text
总体 Success 几乎不变
但 High-severity Failure 大幅下降
```

所以 Data Value 必须相对于：

```text
Target Model
Target Capability
Target Metric
Target Distribution
Target Risk Profile
Training Recipe
```

来定义。

即：

\[
V(D \mid M,T,E)
\]

而不是说：

```text
“这批数据天然价值高。”
```

---

# 18.6 一个实用的潜在价值分解

可以用下面的心智模型：

\[
PotentialValue(D)
\approx
Quality
\times Relevance
\times Novelty
\times Learnability
\times Applicability
\]

如果其中某项接近 0：

```text
错误
完全重复
和目标无关
模型几乎学不会
已高度饱和
```

边际价值都会很低。

这是筛方向的 heuristic，不替代第 21 章的下游训练验证。

---

# 18.7 Data ROI：分子和分母都要完整

\[
DataROI(D)=\frac{\Delta Utility(D)}{TotalCost(D)}
\]

Utility 可以是：

```text
Target Capability Gain
Production Success Gain
Risk Reduction
Escalation Reduction
Latency Reduction
Cost Reduction
```

Total Cost 则至少包含：

```text
Acquisition
Generation
Human Annotation
Expert Review
Verification
Judge
Tool / Environment Execution
Cleaning / Dedup
Training
Evaluation
Engineering
```

所以：

> **Synthetic raw generation 很便宜，不代表 verified synthetic 很便宜。**

---

# 18.8 Raw Count、Usable Yield、High-value Yield 必须分开

例如：

```text
Generate        1,000,000
Schema Valid      800,000
Verifier Pass     300,000
Unique            220,000
Accepted          180,000
High-value         80,000
```

真正战略上关心的不是：

```text
1M generated
```

而是：

```text
Cost / Verified Sample
Cost / Unique Sample
Cost / High-value Sample
```

否则 throughput 会被错当成价值。

---

# 18.9 Marginal Utility：同一种数据不能无限扩

常见曲线：

```text
0 → 10k
提升明显

10k → 50k
仍有收益

50k → 200k
收益下降

200k → 1M
接近饱和
```

于是需要关心：

\[
MU_k = \frac{\Delta Utility}{\Delta Cost}
\]

而不是平均历史收益。

同一类数据的第 100 万条和第 1 万条通常不是同一个投资决策。

---

# 18.10 Stop Rule 必须在扩规模前就定义

常见 Stop 条件：

```text
Capability Saturation
Marginal Gain too low
Duplicate Rate too high
Verified Yield collapse
Frontier moved
Alternative investment has higher ROI
Business priority changed
Regression cost too high
```

成熟项目应该在开始前写明：

> **什么证据出现时，我们会停止继续生产这一类数据。**

否则很容易被 sunk cost 推着继续扩。

---

# 18.11 Risk-adjusted Investment

低频并不等于低优先级。

可以用：

\[
RiskPriority
\approx
Frequency \times Severity \times Exposure \times Irreversibility
\]

作为讨论框架。

比如：

```text
未经授权删除文件
错误转账
隐私泄漏
错误外发邮件
```

即使出现频率低，也可能值得专门数据预算。

所以除了普通 ROI，还可以看：

\[
ROI_{risk}=\frac{ExpectedRiskReduction}{TotalCost}
\]

---

# 18.12 Build / Buy / Generate / Mine

四条 acquisition channel：

## Build

内部 Human / Expert 设计。

适合：

```text
高风险
复杂 rubric
专业 domain
```

## Buy

外部数据 / 标注服务。

适合快速扩规模，但要处理：

```text
quality
rights
provenance
distribution fit
```

## Generate

Teacher / LLM / Simulator。

适合：

```text
定向扩展
结构化 variation
稀有 edge case
```

但有 teacher bias 和 verification burden。

## Mine

Production / Rollout / Failure Logs。

最贴当前模型真实边界，但常伴随：

```text
privacy
selection bias
weak labels
```

因此战略问题不是：

> “Human 还是 Synthetic？”

而是：

> **哪个 capability gap 用哪个 acquisition channel 的单位成本回报更高？**

---

# 18.13 Source Portfolio：不同数据源承担不同职能

一个健康组合可能是：

```text
Production Failures
→ 现实性

Human Gold
→ 标准锚点

Synthetic Expansion
→ 规模

Adversarial / Frontier Cases
→ 推边界

Regression Cases
→ 防遗忘
```

所以 Data Portfolio 不是只在“能力维度”分，也要在“来源职能”上保持结构。

---

# 18.14 Core / Repair / Frontier / Safety / Exploration 五类预算

可以把投资分成：

```text
Core
维持主分布能力

Repair
修当前已知 failure

Frontier
扩下一层能力边界

Safety / High-risk
保护低频高后果场景

Exploration
试尚未证明的新 acquisition / supervision 方法
```

这比把所有项目都塞进一个“训练数据”预算池更可控。

---

# 18.15 Targeted Data 与 Broad Data 要同时存在

Targeted Data：

```text
修特定 capability gap
```

Broad Data：

```text
维持整体覆盖与正常 prior
```

只做 Targeted：

```text
容易过拟合当前 failure distribution
```

只做 Broad：

```text
修关键弱点效率低
```

所以战略目标不是最大化 hard-case ratio，而是：

> **Fix the frontier without forgetting the center。**

---

# 18.16 Mixture 是 Strategy 的执行接口，但技术 owner 在 Ch20

战略层只回答：

```text
哪些能力应该得到更多训练曝光？
哪些 source 应该被上调 / 下调？
Hard-case 是否过采样？
Safety bucket 是否需要最低保障？
```

真正的：

```text
sample ratio
token exposure
temperature sampling
effective sample size
mixture interaction
```

统一见第 20 章。

这样避免 Strategy 章重新变成 Training Mixture 教程。

---

# 18.17 Sample Count 不是训练曝光

即使在战略层，也必须记住：

```text
100k short samples
```

与：

```text
20k long trajectories
```

可能产生完全不同的 token exposure。

所以任何投资 memo 至少要同时写：

```text
Samples
Tokens
Unique Families / Clusters
Expected Training Exposure
```

而不能只报 sample 数。

---

# 18.18 数据价值不是可加的：Interaction 很重要

\[
V(A+B) \neq V(A)+V(B)
\]

例如：

```text
Recovery Data
```

可能只有在：

```text
基础 Tool-use SFT 足够
```

以后才有价值。

又比如：

```text
大量 Hard Negative
```

在某个比例前有益，继续增加可能导致过度拒绝。

因此 Data Strategy 是 portfolio optimization，而不是 dataset 排行榜。

---

# 18.19 Data Value 随 Model Version 变化

\[
V(D\mid M_1) \neq V(D\mid M_2)
\]

对弱模型有用的数据，强模型可能已经饱和。

所以任何 valuation 都应该绑定：

```text
base model
model version
current capability level
training recipe
```

“历史上有效”不是继续无限生产的理由。

---

# 18.20 Freshness 也是价值维度

Agent / Product 环境会变：

```text
Tool API
UI
Business Rules
User Behavior
Permissions
```

因此数据应有：

```text
collection_time
environment_version
tool_version
policy_version
```

过时数据可以进入：

```text
Deprecated
Archived
Regression-only
```

而不应该永久保持 Active Training 状态。

---

# 18.21 Retirement：Data Asset 也应该退出生产组合

应该考虑 retire：

```text
过时产品流程
旧 API
重复 case
失效 rubric
错误历史标签
高度饱和 task family
```

Retire 不等于删除历史。

更好的状态机：

```text
Exploratory
→ Active
→ Maintenance
→ Deprecated
→ Archived / Regression-only
```

这样既保留 lineage，又避免旧数据长期占训练预算。

---

# 18.22 Exploration Budget 是必要的

如果所有项目都要求：

```text
事先证明 ROI
```

团队不会发现新的高价值 supervision interface。

因此可以保留小比例 Exploration Budget，用于：

```text
new task family
new verifier
new annotation schema
new synthetic method
new trajectory supervision
```

但探索必须带：

```text
Hypothesis
Pilot Budget
Success Criterion
Stop Rule
```

而不是无边界试验。

---

# 18.23 Valuation 的证据层级

可以把证据从弱到强排成：

```text
Data-level Proxy
↓
Intrinsic Quality
↓
Small Pilot
↓
Matched-budget Training Experiment
↓
Held-out Capability Gain
↓
Production / Risk Utility
```

例如：

```text
Judge Score 高
```

只能说明 proxy 好看。

真正的 Data Value 需要第 21 章的 downstream intervention experiment。

---

# 18.24 Controlled Ablation 是最低可信的 Data Valuation 手段之一

战略层关心的基本问题是：

```text
Baseline
vs
Baseline + D
```

或更严格：

```text
Matched-budget Baseline
vs
Matched-budget Replacement with D
```

然后看：

```text
Target Gain
General Regression
Safety
Cost
```

实验具体怎么设计，统一见第 21 章。

本章只负责把实验结果转成投资决策。

---

# 18.25 数据实验结果最终要转成 Decision

实验结束后不是只写：

```text
+1.2 pt
```

而要变成：

```text
SCALE
信号稳定、ROI 高、尚未饱和

MAINTAIN
有价值但接近饱和

REVISE
有 signal，但 acquisition / supervision 方案需改

STOP
无稳定收益或机会成本太高

RETIRE
能力已饱和或环境已变化
```

这是 Ch21 与 Ch18 的接口。

---

# 18.26 Portfolio Rebalancing

每个模型版本 / 业务周期都重新看：

```text
Capability Level
Failure Distribution
Risk Profile
Data Saturation
Freshness
Measured Marginal Utility
```

然后决定：

```text
Increase
Maintain
Reduce
Retire
Explore
```

这使 Data Strategy 成为动态资产配置，而不是年度一次性规划。

---

# 18.27 Canonical Case C1：订单 Agent 的数据预算

线上 failure：

```text
Tool Selection          1%
Argument Error          2%
Negative Constraint     4%
Recovery Failure        2%
Verification Failure    2%
Infrastructure          1%
```

不能直接：

```text
Negative Constraint 最大
→ 全投这里
```

继续看：

```text
Negative Constraint
频率高 / 严重度中 / 可学性高

Verification Failure
频率较低 / 严重度高 / 不可逆风险高 / 可学性高

Infrastructure Failure
不是 Data Problem
```

于是更成熟的投资组合可能是：

```text
Negative Constraint
→ targeted synthetic + human boundary audit

Verification
→ high-risk family + preference / recovery data

Infrastructure
→ engineering fix
```

并且为 Tool Selection 维持 regression，而不是继续大规模新增数据。

---

# 18.28 Data Investment Memo

重要项目建议在启动前写：

```text
Target Capability
Current Evidence
Why Data
Why Now
Candidate Acquisition Channel
Proposed Quantity / Tokens
Quality Standard
Verification Plan
Estimated Total Cost
Training Exposure
Evaluation Plan
Risk / Regression Concern
Scale Rule
Stop Rule
```

完成后补：

```text
Actual Yield
Actual Cost
Downstream Delta
Regression
ROI
Decision
```

这样 Data Project 就从“做一批数据”升级成可审计投资。

---

# 18.29 Data Strategy Dashboard

建议至少分四组。

### Capability

```text
Score
Failure Rate
Frontier Status
Regression
```

### Data

```text
Samples
Tokens
Unique Families
Verified Yield
Freshness
```

### Cost

```text
Generation
Human
Verification
Training
Evaluation
Engineering
```

### Return

```text
Target Gain
Generalization
Risk Reduction
Marginal Gain
ROI
```

如果 dashboard 只有：

```text
本周产出 50 万条
```

那仍然只是生产 dashboard，不是 strategy dashboard。

---

# 18.30 常见失败模式

1. **用数据量代表价值。** 100 万条不自动优于 10 万条。
2. **Benchmark Gap = 投资优先级。** 忽略业务与风险。
3. **所有 failure 都做数据。** 没先经过 Data Problem Gate。
4. **忽略 Total Cost。** 只看 annotation / generation price。
5. **忽略 Marginal Utility。** 历史上有用就无限扩。
6. **只看平均指标。** 低频高风险能力长期欠投。
7. **只做 hard case。** 中心分布 prior 被破坏。
8. **只追短期 ROI。** Exploration 和长尾能力饿死。
9. **把 Mixture 技术细节和 Strategy 混在一起。** 决策边界不清。
10. **Proxy 好看就宣布数据有价值。** 没做 downstream validation。
11. **不做 Retirement。** 旧数据永远挤占预算。
12. **忽略 Model Version。** 把过去的价值外推到现在。

---

# 18.31 从数据岗位视角，本章实际在做什么？

成熟 Data Strategy 工作包括：

```text
构建 Capability Portfolio
做 Data Problem Gate
估计 acquisition channel 成本
比较 Human / Synthetic / Mine / Programmatic
定义 High-risk / Frontier / Core allocation
做 small pilot
读取 Ch21 experiment result
计算 marginal return
做 Scale / Maintain / Stop decision
定期 rebalance portfolio
管理 Data Asset lifecycle
```

真正专业的表达不是：

> “我做了 20 万条数据。”

而是：

> **“我们为什么选这类数据、为什么是这个规模、和其他方向相比为什么更值、实验结果是否支持继续投入。”**

---

# 18.32 面试 / 自检问题

1. Data Production 和 Data Strategy 的区别是什么？
2. 什么是 Data Asset / Batch / Investment？
3. 为什么预算应该映射到 Capability，而不只是 Dataset？
4. Capability Gap 为什么不等于 Benchmark Gap？
5. 怎么判断 failure 是否真的是 Data Problem？
6. Data Value 为什么必须条件化于 Model / Metric / Distribution？
7. Data ROI 的分母应该包含哪些成本？
8. Raw Count、Verified Yield、High-value Yield 有什么区别？
9. 什么是 Marginal Utility？
10. Stop Rule 应该什么时候定义？
11. 低频高风险 failure 为什么仍可能值得高投入？
12. Build / Buy / Generate / Mine 分别适合什么？
13. 为什么 Portfolio 需要 Core / Repair / Frontier / Safety / Exploration？
14. Targeted Data 和 Broad Data 为什么要共存？
15. Sample Count 为什么不等于 training exposure？
16. 为什么 Data Value 不是可加的？
17. 同一批数据为什么对不同模型版本价值不同？
18. 什么叫 Data Retirement？
19. 为什么 Exploration Budget 也必须有 Stop Rule？
20. 怎样把 Data Experiment 的结果转成投资决策？
21. 一个 Data Investment Memo 应该写什么？
22. Strategy Dashboard 为什么不能只有数据产量？

---

# 18.33 本章最终心智模型

```text
Capability Map
↓
Gap / Risk / Opportunity
↓
Is This a Data Problem?
↓
Candidate Data Investments
↓
Expected Value + Total Cost
↓
Portfolio Decision
↓
Pilot / Data Experiment
↓
Measured Marginal Utility
↓
Scale / Maintain / Revise / Stop / Retire
↓
Portfolio Rebalance
```

这就是 Data Strategy。

其中：

```text
Ch9
发现候选 case / frontier

Ch17
把它们送进闭环

Ch20
执行 filtering / dedup / mixture

Ch21
证明数据真的产生因果收益

Ch23
观察环境和能力何时变化
```

本章负责的是最上层的一件事：

> **决定有限的数据预算下一步应该压在哪里。**

但一旦某类数据被决定继续 `SCALE / MAINTAIN`，它就不再只是一次性项目产物，而开始成为需要长期维护的 Data Asset。此时下一个问题自然变成：

```text
它是谁？
从哪里来？
经历过哪些 transformation？
为什么被保留 / 重标 / 重建？
被哪些 Dataset / Run / Model 使用过？
以后发生修正时，能否沿历史准确追溯影响范围？
```

因此下一章进入：

> [`第 19 章 Data Governance、Lineage 与 Reproducibility`](./19_Data_Governance_Lineage_and_Reproducibility.md)

正式回答：

> **当“值得投资”已经成立以后，怎样让这些数据资产在持续变化中仍然有稳定身份、版本、lineage 与可复现历史。**