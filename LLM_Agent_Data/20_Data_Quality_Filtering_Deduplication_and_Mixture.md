# 第 20 章 Data Quality、Filtering、Deduplication 与 Mixture：决定模型真正会看到什么

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 19 章 Data Governance、Lineage 与 Reproducibility`](./19_Data_Governance_Lineage_and_Reproducibility.md)
>
> 关联章节：[`第 7 章 Synthetic Data`](./07_Synthetic_Data_Generation_and_Synthesis.md)、[`第 9 章 Hard Case Mining`](./09_Hard_Case_Mining_and_Curriculum.md)、[`第 15 章 Grader / Verifier / Judge`](./15_Grader_Verifier_and_LLM_as_a_Judge.md)、[`第 18 章 Data Strategy`](./18_Data_Strategy_and_Data_Valuation.md)、[`第 21 章 Data Experiments`](./21_Data_Experiments_and_Causal_Validation.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**Data Curation 的 canonical chapter。它负责 Quality Dimension、Rule / Model / Human Filtering、Exact / Near / Semantic / Decision / Family Dedup、Contamination Filtering、Reweighting、Capability / Difficulty Balance、Sampling Weight、Token Exposure 与 Mixture Policy。正式 Data ROI 归第 18 章，Filtering / Mixture 是否真的有效的因果验证归第 21 章。**
>
> 本章核心问题：**进入训练资产池的数据，哪些该留、哪些该删、哪些该降权、哪些其实只是重复曝光，以及在有限训练预算里，模型最终应该多看到哪些经验、少看到哪些经验？**

---

# 20.0 Data Curation 不是“把脏数据删掉”

真实数据可能：

```text
事实正确但高度重复
标签可靠但不再新颖
任务很难但不可验证
答案很好但 benchmark-contaminated
真实线上产生但包含隐私
synthetic 很干净但 decision pattern 单一
```

因此不是只问：

> 这条数据好不好？

而是问：

```text
它在哪些维度可信？
它提供了多少新信息？
它属于哪个 capability / failure family？
它该被保留、删除、隔离还是降权？
它最终应该获得多少训练曝光？
```

完整链路：

```text
Raw / Human / Synthetic / Rollout Data
↓
Validity / Rights Checks
↓
Quality Assessment
↓
Dedup / Contamination
↓
Capability / Difficulty Tagging
↓
Filter / Reweight
↓
Mixture Policy
↓
Training View
```

---

# 20.1 Data Quality 是向量，不是单一分数

至少可以拆成：

```text
Correctness
Relevance
Completeness
Instruction Fidelity
Consistency
Verifiability
Novelty
Diversity
Difficulty
Safety
Privacy / Rights
Provenance Quality
Parseability
```

Agent 数据还常见：

```text
Tool Validity
Argument Correctness
Observation Grounding
State Consistency
Recovery Quality
Side-effect Safety
Termination Quality
```

因此：

```json
{
  "correctness": 1.0,
  "verifiability": 1.0,
  "novelty": 0.4,
  "decision_diversity": 0.3,
  "privacy_ok": true
}
```

通常比：

```json
{"quality": 0.86}
```

更有解释力。

---

# 20.2 不同 Data View 对“质量”的要求不同

### SFT

更重：

```text
Correctness
Instruction Fidelity
Low Noise
```

### Preference

更重：

```text
Pair Informativeness
Reliable Relative Label
Decision-relevant Difference
```

### Verifier / Judge Data

更重：

```text
Boundary Case
Hard Negative
Gold Reliability
```

### Recovery Data

更重：

```text
Authentic Failure State
Recoverability
State Fidelity
Counterfactual Value
```

所以：

> **Quality 是 downstream-objective dependent 的。**

---

# 20.3 第一层：Validity / Integrity / Rights Hard Checks

在语义质量以前，先检查：

```text
schema valid?
JSON parseable?
tool exists?
arguments valid?
parent IDs resolved?
environment snapshot exists?
label version known?
privacy / rights allowed?
```

这些应尽量 deterministic。

适合 Hard Reject 的常见情况：

```text
Corrupt Record
Invalid Tool
Broken Lineage
PII / Rights Violation
Known Eval Leakage
Unsafe Forbidden Positive Demo
```

这里不需要 LLM Judge 来猜。

---

# 20.4 Filtering 不只 PASS / DROP

推荐动作空间：

```text
PASS
DROP
QUARANTINE
REVIEW
DOWNWEIGHT
REGRESSION_ONLY
```

例如一个失败 trajectory：

```text
不适合 Positive SFT
```

但可能非常适合：

```text
Preference Negative
Recovery Seed
Regression
Failure Analysis
```

所以：

> **Quality Gate 也是 Data Routing Gate。**

---

# 20.5 Rule-based Filtering

适合：

```text
empty output
length anomaly
schema violation
illegal tool
obvious PII
exact benchmark match
invalid encoding
```

优势：

```text
Cheap
Deterministic
Auditable
```

但规则只能覆盖明确问题，不能替代语义判断。

---

# 20.6 Model-based Filtering

适合判断：

```text
instruction following
completeness
reasoning plausibility
failure category
semantic redundancy
```

但必须把它视为：

> **有误差、有 bias 的 selector。**

需要保存：

```text
filter_model
prompt_version
raw score
reason
threshold
filter_version
```

并用第 6 / 15 章的 Human Gold / Evaluator calibration 定期审计。

---

# 20.7 Human Filtering 只用于高信息区域

人更适合：

```text
High-risk Case
Boundary Case
Disagreement
New Failure Type
Expert Domain
Gold Expansion
```

常见 cascade：

```text
Rule
↓
Executable Verifier
↓
Model Grader
↓
High-risk / Disagreement
↓
Human
```

目标是把昂贵判断留给最需要的样本。

---

# 20.8 Filter Precision / Recall 也要被评估

过滤“坏数据”同样有：

```text
False Positive
删掉好数据

False Negative
留下坏数据
```

PII / Safety 往往更偏 high recall；Frontier / Hard Case filtering 则必须警惕误杀。

因此应在 gold subset 上测：

```text
Precision
Recall
Slice-specific error
```

而不是只看 acceptance rate。

---

# 20.9 Filtering 最大的隐性风险：Distribution Narrowing

如果 filter 偏爱：

```text
流畅
标准
高置信
容易判断
```

它可能系统性删掉：

```text
Hard Negatives
Boundary Cases
Rare Domains
Uncertain-but-important Cases
```

所以过滤后必须比较：

```text
Capability
Difficulty
Failure Type
Domain
Length
Style
Source
```

分布变化。

> **Filter 是 Distribution Transformer，不只是 Cleaner。**

---

# 20.10 Dedup：Raw Sample Count ≠ Effective Information

如果：

```text
100k samples
```

里面 80k 只是同模板换实体 ID，信息量远小于 100k。

Dedup 的目标不是追求“文本都不一样”，而是控制：

```text
哪些经验被重复曝光了多少次
```

---

# 20.11 Exact Dedup

通常使用：

```text
normalize
→ hash
```

适合完全相同或非常近的记录。

这是最便宜、最稳定的一层。

---

# 20.12 Near Dedup

可用：

```text
n-gram
MinHash
SimHash
Jaccard
edit distance
```

处理表面相似但非完全一致的文本。

---

# 20.13 Semantic Dedup

Embedding + nearest-neighbor 可以发现语义近似。

但：

```text
“取消会议”
```

与：

```text
“取消会议，但周会不要动”
```

语义很近，decision boundary 却可能完全不同。

所以：

> **Semantic Similarity ≠ Decision Equivalence。**

这也是为什么 Agent / Reasoning 数据不能只做 embedding dedup。

---

# 20.14 Decision-level Dedup

对 Agent / Reasoning 更有价值的 signature 可能是：

```text
State Type
Constraint Pattern
Action Type
Tool Sequence
Failure Type
Recovery Pattern
```

例如：

```text
lookup → permission_check → write → verify
```

如果 10 万条都属于同一决策结构，即使文本完全不同，Decision Diversity 仍然很低。

---

# 20.15 Family-level Dedup / Split

Synthetic / Counterfactual 数据必须保留：

```text
seed_id
family_id
workflow_id
```

避免：

```text
同 seed 的兄弟样本
train / test 各放一部分
```

造成 family leakage。

Split governance 详见第 16 / 19 章。

---

# 20.16 Dedup 不是“越狠越好”

有些模式在线上本来就高频。

如果全部只留一条，会丢掉真实 frequency signal。

所以区分：

```text
Redundant Duplicate
vs
Legitimate Frequency
```

可采用：

```text
cap per cluster
frequency-aware subsampling
reweight instead of delete
```

目标是防止采集机制造成不合理放大，而不是让每种 pattern 只出现一次。

---

# 20.17 Contamination Filtering

至少区分：

```text
Exact Match
Near Duplicate
Paraphrase
Solution Leakage
Synthetic Derivative
Same Seed / Workflow
Reference Leakage
```

Contamination 的评测含义与 split protocol 见第 16 章；provenance / registry 见第 19 章。

本章只负责在 Curation pipeline 中执行相应过滤与隔离。

---

# 20.18 Hard Delete 与 Reweight

不是所有边界数据都应该删。

可以用：

```text
keep
+
lower weight
```

表达：

```text
label uncertainty
source uncertainty
lower trust tier
```

因此 Curation 的动作空间是：

```text
删除
隔离
复核
保留
降权
```

而不是单一二元过滤。

---

# 20.19 什么是 Data Mixture？

设数据 bucket 为：

\[
M=\{(D_i,w_i)\}_{i=1}^{K}
\]

其中：

```text
D_i
某个 source / capability / domain bucket

w_i
训练时获得的采样权重
```

Mixture 的本质是：

> **在有限训练预算里，决定模型多看到哪些经验、少看到哪些经验。**

所以 Mixture 本身就是一种 Training Data Policy。

---

# 20.20 Dataset Size ≠ Training Exposure

例如：

```text
General = 10M short examples
Recovery = 100k long trajectories
```

原始 sample 比例不能说明实际曝光。

至少要明确：

```text
Sample Share
Token Share
Batch Share
Update Share
Loss Weight
```

因此“20% Agent Data”如果没说 denominator，信息是不完整的。

---

# 20.21 Sample-based 与 Token-based Mixture

长 trajectory 会拿走更多 token budget。

所以对 Agent / Reasoning 数据尤其要同时监控：

```text
Sample Share
Token Share
Trajectory Length Distribution
```

否则少量超长轨迹可能悄悄主导训练。

---

# 20.22 Temperature Sampling

当 bucket 大小差异巨大时，可用：

\[
p_i \propto n_i^\alpha
\]

其中：

```text
α = 1
按原始规模

α < 1
提高小 bucket 相对曝光

α = 0
接近 source-level uniform
```

它是 mixture 的一个实现工具，不是通用最优策略。

---

# 20.23 Capability-balanced Mixture

Domain balance 不足以描述 Agent 数据。

例如：

```text
Calendar
Email
CRM
```

三个 domain 都很多，但可能 90% 都只是 lookup。

所以至少同时标：

```text
Domain
Capability
Difficulty
Failure Type
Risk
Source
```

典型 capability bucket：

```text
Tool Selection
Argument Construction
Observation Grounding
Recovery
Verification
Termination
```

---

# 20.24 Difficulty Balance：Mixture ≠ Curriculum

Mixture 关注：

```text
同一阶段有哪些数据、各占多少
```

Curriculum 关注：

```text
不同阶段先后看到什么
```

典型 mixture 可能同时保留：

```text
Easy
Medium
Frontier
High-risk Hard
```

避免全是 easy，也避免全是极端 hard。

Curriculum 的详细 acquisition / ordering 思路见第 9 章，是否有效则由第 21 章验证。

---

# 20.25 Positive / Negative / Recovery Balance

如果数据只有：

```text
成功回答
正确 Tool Call
成功 Trajectory
```

模型很难学会：

```text
什么时候不要做
什么时候停止
什么时候澄清
什么时候回退
什么时候恢复
```

因此 mixture 还要关注：

```text
Positive
Hard Negative
Near-miss
Recovery
Abstention
Clarification
```

行为类型的覆盖。

---

# 20.26 成功 Trajectory 不等于所有 Step 都该模仿

成功轨迹可能包含：

```text
lucky recovery
unsafe shortcut
redundant action
unnecessary retry
```

失败轨迹中也可能有多个正确步骤。

因此 routing / mixture 最好结合：

```text
Trajectory Outcome
+
Step Labels
+
Failure Attribution
```

而不是：

```text
success → 全部 positive
failure → 全部 negative
```

---

# 20.27 Effective Information Size

当大量数据属于同 cluster，或者权重极度集中时，真实信息量远低于 raw count。

加权样本的一个直觉公式：

\[
N_{eff}\approx\frac{(\sum_i w_i)^2}{\sum_i w_i^2}
\]

不必机械使用，但它提醒：

> **Exposure ≠ Independent Information。**

---

# 20.28 Mixture Interaction

\[
Value(A+B)\neq Value(A)+Value(B)
\]

例如：

```text
Recovery Preference
```

可能只有在基础 Tool-use 能力足够以后才有效。

又例如 Hard Negative 比例过高，可能导致 over-refusal。

因此 Mixture 不是简单把各 bucket 的“单独价值”相加。

正式 interaction experiment 见第 21 章。

---

# 20.29 Training Distribution 不必等于 Production Distribution

线上高频代表：

```text
Frequency
```

训练曝光还要考虑：

```text
Learning Value
Risk
Coverage
Business Priority
```

所以：

```text
Training Distribution
≠
Raw Production Frequency
```

例如线上 0.01% 的严重安全 case，训练中完全可能获得更高权重。

---

# 20.30 Source Balance：避免一个 Generator 定义整个世界

如果绝大多数 synthetic 来自同一 teacher，模型会继承：

```text
Teacher Style
Teacher Bias
Teacher Failure Modes
```

所以可组合：

```text
Human
Production
Multiple Teachers
Programmatic
Environment-grounded Rollout
```

目的不是形式上的多源，而是减少单一生成机制支配。

---

# 20.31 Filter-induced Bias 与 Dedup-induced Bias

Filter 可能偏爱：

```text
long
fluent
standard
high-confidence
```

Dedup 也可能更容易删掉某些天然结构相似的 capability。

因此 Curation 前后都应该审计：

```text
Length
Style
Domain
Capability
Difficulty
Failure Type
Source
```

否则 Cleaner / Deduper 会悄悄变成新的分布设计器。

---

# 20.32 推荐的 Curation Order

一个常见顺序：

```text
Integrity
↓
Privacy / Rights
↓
Exact Dedup
↓
Near / Family Dedup
↓
Executable / Rule Verification
↓
Model Quality Assessment
↓
Human Disagreement / High-risk Review
↓
Capability / Difficulty Tagging
↓
Reweight / Mixture Assignment
```

原则是：

> **越便宜、越确定的判断越早做；越昂贵、越主观的判断越后做。**

---

# 20.33 Filter Reason 必须可追溯

不要只存：

```json
{"kept": false}
```

而应记录：

```text
filter_stage
reason
score
threshold
cluster_id
matched_sample_id
filter_version
```

这样 threshold / policy 改变后，可以重新构建 Dataset View，而不必修改 raw truth。

完整 version / lineage 见第 19 章。

---

# 20.34 Hard Constraints 与 Soft Scores 分开

### Hard Constraints

例如：

```text
PII violation
invalid rights
known eval leakage
wrong gold-positive SFT answer
forbidden unsafe behavior
```

通常直接 reject / quarantine。

### Soft Scores

例如：

```text
novelty
style
difficulty
verbosity
```

更适合：

```text
ranking
sampling
reweighting
```

不要用一个平均 Quality Score 让高 novelty 抵消 correctness failure。

---

# 20.35 Mixture Versioning

Mixture 应被当成可版本化 Policy：

```yaml
mixture_id: agent_posttrain_v7
sampling_unit: token
buckets:
  general_sft: 0.30
  tool_use: 0.20
  recovery: 0.15
  verification: 0.10
  safety: 0.10
  reasoning: 0.15
```

并绑定：

```text
model_version ↔ mixture_version
```

否则模型变化后很难追溯训练曝光发生了什么。

---

# 20.36 Mixture Health Dashboard

至少监控：

```text
Samples
Tokens
Unique Clusters / Families
Duplicate Rate
Verified Share
Synthetic / Human / Production Share
Capability Distribution
Difficulty Distribution
Failure Distribution
High-risk Coverage
Length Distribution
Filter Acceptance Rate
```

它回答的是：

> **模型现在到底被喂了什么分布？**

不是模型是否因此变好；后者交给第 21 章。

---

# 20.37 Curation 与 Data Experiment 的接口

Ch20 产出的是：

```text
Filter Policy
Dedup Policy
Weight Policy
Mixture Version
```

Ch21 要验证：

```text
这些 policy 改动
是否导致真实 downstream gain
```

因此本章不再完整展开：

```text
matched-budget ablation
scaling curve
statistical power
seed variance
```

只要求所有 Curation 决策都能够被版本化、被实验化。

---

# 20.38 Canonical Case C1：Recovery Data 如何 Curate

来源：

```text
Production Failures
Synthetic Failure Injection
Historical Regression
```

第一步排除：

```text
Harness Bug
Environment Corruption
Invalid Task
```

第二步按：

```text
failure_type
recovery_action
workflow
```

做 family / decision-level dedup。

第三步路由为：

```text
Recovery SFT
Preference
Regression
```

第四步给 mixture 分配：

```text
capability = recovery
risk tier
source trust tier
training weight
```

至于：

```text
Recovery 2% / 5% / 10% 哪个最好？
```

这是第 21 章的 Data Experiment。

---

# 20.39 常见失败模式

1. 一个 Quality Score 控制所有决策。
2. Judge 分数直接当 Ground Truth。
3. 只做 Exact Dedup。
4. Semantic Dedup 太激进，删掉关键约束变体。
5. Surface Diversity 高，却没有 Decision Diversity。
6. Dedup 越多越好，真实频率 signal 被删光。
7. Dataset Size 直接当 Training Exposure。
8. 只报 sample ratio，不报 token ratio。
9. Hard Case 全部高权重，导致 over-retry / over-refusal。
10. 成功 trajectory 全部作为 positive demo。
11. Filter / Dedup 后不做分布审计。
12. Mixture 没版本，模型效果无法追溯。
13. 把 Curation proxy 的改善当成 downstream 成功。

---

# 20.40 从数据岗位视角，本章实际在做什么？

典型工作：

```text
定义 quality dimensions
搭 deterministic validity gates
设计 model / human filtering cascade
做 exact / near / semantic / decision / family dedup
维护 contamination filter
做 capability / difficulty / failure tagging
设计 reweighting
核算 sample / token exposure
维护 mixture version
监控 curation-induced distribution shift
把 curation policy 交给 Ch21 做 downstream validation
```

真正的目标不是：

> “把数据清洗得很干净。”

而是：

> **把原始数据资产转成一个信息密度高、覆盖合理、风险受控、训练曝光可解释的学习分布。**

---

# 20.41 面试 / 自检问题

1. Data Quality 为什么不能压成一个分数？
2. SFT / Preference / Recovery 对质量要求有什么不同？
3. Hard Constraint 与 Soft Score 有什么区别？
4. 为什么 Filtering 需要 `QUARANTINE / REVIEW / DOWNWEIGHT`？
5. Filter Precision / Recall 分别意味着什么？
6. 为什么 Filter 是 Distribution Transformer？
7. Exact / Near / Semantic / Decision Dedup 分别解决什么？
8. 为什么 Semantic Similarity 不等于 Decision Equivalence？
9. Family-level split 为什么重要？
10. Dedup 为什么不是越多越好？
11. Hard Delete 和 Reweight 什么时候分别更适合？
12. Dataset Size 为什么不等于 Training Exposure？
13. Sample Ratio 和 Token Ratio 为什么要分开？
14. Capability-balanced Mixture 为什么比只看 Domain 更有信息？
15. Mixture 与 Curriculum 的区别是什么？
16. 为什么 Positive / Negative / Recovery 要同时考虑？
17. 什么是 Effective Information Size？
18. 为什么 Mixture 有 interaction？
19. Training Distribution 为什么不应该简单复制线上频率？
20. Filter / Mixture 怎样和第 21 章的 Data Experiment 对接？

---

# 20.42 本章最终心智模型

```text
Quality
这条数据在哪些维度值得信？

Dedup
它提供新信息，还是重复曝光？

Filtering / Routing
它应该删、留、隔离、复核还是降权？

Mixture
在有限训练预算里，它应该被看到多少次？
```

因此：

> **Data Curation 最终不是在“挑好数据”，而是在定义模型真正会看到的学习分布。**

下一章第 21 章进一步回答：

> **这套 Filtering / Weighting / Mixture Policy，究竟有没有真的让模型变得更好？**