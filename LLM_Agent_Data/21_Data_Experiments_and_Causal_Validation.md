# 第 21 章 Data Experiments：如何证明一批数据真的有用

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 20 章 Data Quality、Filtering、Deduplication 与 Mixture`](./20_Data_Quality_Filtering_Deduplication_and_Mixture.md)
>
> 关联章节：[`第 9 章 Hard Case Mining`](./09_Hard_Case_Mining_and_Curriculum.md)、[`第 16 章 Benchmark Design`](./16_Benchmark_Design_and_Evaluation_Protocol.md)、[`第 18 章 Data Strategy`](./18_Data_Strategy_and_Data_Valuation.md)、[`第 19 章 Governance`](./19_Data_Governance_Lineage_and_Reproducibility.md)、[`第 23 章 Monitoring 与 Drift`](./23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**Data Intervention / Causal Validation 的 canonical chapter。它负责 Add / Remove / Replace / Reweight、Matched-budget、Pilot、Scaling Curve、Quality-vs-Quantity、Mixture / Curriculum Experiment、Interaction、Transfer、Mechanism Check、Experiment Registry 与 Scale / Stop Decision；通用 benchmark / statistics / denominator discipline 统一引用第 16 章。**
>
> 本章核心问题：**一批数据看起来正确、难、稀缺、Judge 分高，都不等于它真的能让模型变好。我们怎样通过受控 intervention 证明：哪类数据让哪项能力提高了多少，这个收益是否稳定、是否泛化、是否值得成本、是否伤害别的能力？**

---

# 21.0 Intrinsic Data Quality ≠ Downstream Learning Value

假设有：

```text
20,000 条 Recovery Trajectories
```

它们：

```text
人工审核通过
Verifier 可验证
轨迹完整
重复率低
```

这些只说明：

```text
Data Quality 高
```

但还没有回答：

```text
模型训练后 recovery 会不会提高？
是否只是学会固定模板？
会不会导致 over-retry？
20k 比 5k 是否真的更值？
同样 token budget 下优势还在吗？
```

因此：

> **Data Quality 是输入属性，Learning Value 是训练 intervention 的结果属性。**

本章只关心第二者如何被验证。

---

# 21.1 Data Experiment 的因果对象

更一般地，可以把一个 Data Intervention 写成作用在 baseline data mixture \(B\) 上的算子 \(I_D\)：

\[
\Delta(I_D;M_0,T,E)
=
Metric(Train(M_0,I_D(B),T),E)
-
Metric(Train(M_0,B,T),E)
\]

其中：

```text
M0  = base model / checkpoint
B   = baseline data mixture
I_D = 对 B 施加的数据 intervention
T   = training protocol
E   = frozen evaluation protocol
```

`I_D` 可以统一表示：

```text
Add
Remove
Replace
Reweight
Transform
```

真正要估计的是：

> **在其他关键条件尽量受控时，改变 Data Policy / Data Composition 导致了什么变化。**

---

# 21.2 一个完整实验至少要提前定义什么？

```text
Research Question
Baseline
Treatment
Data Manifest / Version
Training Protocol
Evaluation Protocol
Primary Metric
Regression Metrics
Budget Matching Rule
Seed Policy
Decision Rule
```

例如：

```text
RQ:
Recovery preference 是否提升 recoverable tool-failure success？

Baseline:
mixture_v9

Treatment:
用 3% token budget 替换成 recovery preference v3

Train:
相同 base model / optimizer / total tokens

Eval:
recovery_holdout + general agent + safety regression

Primary:
Recovery Success

Guardrail:
Over-retry / Tool Cost
```

这样避免“跑完以后挑最好看的指标”。

---

# 21.3 Data Intervention 的五种基本形式

## Add

```text
Baseline
vs
Baseline + D
```

回答：

> 多加这批数据是否有帮助？

但可能同时增加训练预算。

## Remove

```text
Full
vs
Full - D
```

回答：

> 去掉 D 是否伤害现有能力？

## Replace

```text
固定总 token
Original Bucket → D
```

回答：

> 相同预算下，D 是否比替代数据更值？

## Reweight

```text
D 从 2% → 5% → 10%
```

回答：

> 多少 exposure 合适？

## Transform

改变：

```text
filter threshold
pair construction
curriculum
negative sampling
supervision format
```

回答：

> 同样原始数据，用不同构造方式是否产生不同学习价值？

---

# 21.4 Matched-budget 是 Data Experiment 最重要的控制之一

如果：

```text
Baseline = 10B tokens
Treatment = 12B tokens
```

Treatment 提升不能直接归因于 Data Composition。

更有解释力的是：

```text
Baseline = 12B original-mixture tokens
Treatment = 12B tokens with D replacing part of baseline
```

尽量匹配：

```text
Total Tokens
Training Steps
Optimizer
Base Model
Batch Policy
```

对于 Agent 数据有时还要关注：

```text
Episode Count
Trajectory Length
Tool-event Density
```

匹配哪个 denominator 要由研究问题决定。

---

# 21.5 Add 与 Replace 回答不同问题

```text
Add Experiment
```

更接近：

> 增加更多这种经验，整体有没有帮助？

```text
Replace / Matched-budget
```

更接近：

> 在有限预算里，这种经验是否比其他经验更值得模型看到？

因此正式数据决策通常最好同时知道：

```text
absolute utility
+
relative utility per budget
```

---

# 21.6 Remove Ablation 的解释边界

删除 D 后变差，可以支持：

```text
D 在当前 mixture 中有贡献
```

但不自动说明：

```text
继续增加 D 仍然有高价值
```

可能出现：

```text
Remove → 明显下降
Add more → 几乎不再提升
```

说明 D 是基础成分，但已经接近 saturation。

这正是为什么需要 Scaling Curve。

---

# 21.7 Pilot Gate：先验证 signal，再扩规模

推荐：

```text
1k
→ 5k
→ 20k
→ 50k
→ scale
```

每一阶段问：

```text
是否出现目标 signal？
是否稳定？
是否有 regression？
verified yield 是否合理？
cost 是否失控？
```

因此 Data Project 最好明确：

```text
Pilot Gate
Confirmation Gate
Scale Gate
Stop Gate
```

而不是立项就默认扩到百万级。

---

# 21.8 Scaling Curve 与 Marginal Gain

假设：

```text
5k  → +1.8pt
20k → +3.0pt
50k → +3.5pt
100k → +3.6pt
```

说明边际收益快速下降。

战略上应该比较：

```text
继续加到 200k
```

和：

```text
把预算转去另一个 capability
```

哪个更值。

这就是 Ch21 向 Ch18 提供的最重要证据之一。

---

# 21.9 Quantity vs Quality Experiment

可以比较：

```text
10k Expert-verified
50k Medium-quality
100k Cheap Synthetic
Hybrid
```

匹配：

```text
Training Tokens
```

再看：

```text
Target Gain
Transfer
Regression
Total Cost
```

最后问：

> **每单位成本，哪种 quality tier 带来的 downstream gain 更高？**

不是预设“专家一定最好”或“Synthetic 一定更划算”。

---

# 21.10 Filtering Threshold Experiment

例如：

```text
Judge threshold = 0.6 / 0.7 / 0.8 / 0.9
```

随着阈值升高：

```text
Average Quality ↑
Volume ↓
Diversity 可能 ↓
Frontier Retention 可能 ↓
```

所以要同时记录：

```text
Pass Rate
Capability Coverage
Difficulty
Diversity
Downstream Gain
```

Ch20 负责生成这些不同 curation views；Ch21 负责比较它们训练后哪个真正更好。

---

# 21.11 Difficulty / Frontier Experiment

直接比较：

```text
Easy
Medium
Frontier
Extreme Hard
```

在 matched token budget 下的训练价值。

可能出现：

```text
Easy
维持基础稳定

Frontier
收益最高

Extreme Hard
noise / learnability 差
```

所以：

```text
Hardness
≠ Training Value
```

必须实验验证。

---

# 21.12 Curriculum Experiment

固定同一批数据与总曝光，只改变顺序：

```text
Random Shuffle
Easy → Hard
Hard → Easy
Foundation → Frontier
Dynamic Curriculum
```

这样才能把：

```text
Curriculum Effect
```

和：

```text
Data Composition Effect
```

分开。

---

# 21.13 Mixture Sweep

例如 Recovery token share：

```text
0%
2%
5%
10%
20%
```

同时观察：

```text
Recovery Success
Overall Success
Over-retry
Tool Cost
Safety
```

最佳点通常是 Pareto operating point，而不是目标指标最大的那个比例。

---

# 21.14 Interaction Experiment

两个组件：

```text
A = Tool-use SFT
B = Recovery Preference
```

做：

```text
No A / No B
A only
B only
A + B
```

判断：

```text
Synergy
Interference
Dependency
```

因为：

\[
V(A+B)\neq V(A)+V(B)
\]

Mixture interaction 的概念见 Ch20，本章负责正式验证。

---

# 21.15 Source Experiment

针对同一 capability 比较：

```text
Human-authored
Teacher-generated
Production-mined
Programmatic
Hybrid
```

尽量匹配：

```text
tokens
difficulty
capability coverage
```

然后比较：

```text
Gain
Transfer
Cost
Regression
```

最终结论应该是条件化的：

> 对这个模型、这个 capability、这个训练阶段，哪种 source 更有 marginal value。

---

# 21.16 Supervision Interface Experiment

同一个 failure 可以转成：

```text
Correct Demonstration
Wrong + Correction
Preference Pair
Critique
Recovery Trajectory
Verifier Data
```

所以应该问：

> **同样的经验，用哪种 supervision interface 最容易被模型学会？**

而不是只问：

> 失败数据有没有价值？

这是现代 Data Experiment 很重要的一类设计。

---

# 21.17 Synthetic Pipeline Ablation

可以固定 Task Source，仅改变：

```text
Raw Synthetic
Verified Synthetic
Human-corrected Synthetic
Synthetic + Hard Negative
```

或固定 Generator，只改变 Verifier / Filter。

这样能定位：

```text
Generator Bottleneck
Verifier Bottleneck
Filtering Bottleneck
```

而不是把整个 synthetic pipeline 当成一个不可拆黑箱。

---

# 21.18 Same-state / Counterfactual Data Experiment

保持：

```text
same prefix / same state
```

只改变：

```text
action
continuation
supervision
```

可以构造：

```text
baseline action
better action
recovery action
```

这种设计特别适合研究：

```text
Continue / Stop
Branch / Repair
Tool Selection
Recovery
Candidate Selection
```

因为 prior history 被严格控制。

---

# 21.19 Mining Policy 也必须实验验证

比较：

```text
Random Sampling
Uncertainty Mining
Disagreement Mining
Failure Mining
Risk-weighted Mining
```

在：

```text
相同样本数
相同 token budget
```

下训练，然后看 downstream gain。

因为：

> **Mining Signal 强，不等于 Training Value 高。**

这使第 9 章 acquisition policy 从 heuristic 升级成可验证对象。

---

# 21.20 Proxy Metric 必须经过 Downstream Validation

常见 proxy：

```text
Judge Score
Verifier Pass Rate
Novelty
Difficulty
Reward Gap
Uncertainty
```

它们适合：

```text
筛选
排序
实验预估
```

但不等于 Learning Value。

一个简单验证方法：

```text
按 proxy 分桶
↓
分别训练 / reweight
↓
比较 downstream gain
```

如果 proxy 与 gain 没有稳定关系，就不应继续把它称作 Data Value estimator。

---

# 21.21 Evaluation 要冻结，统计方法回到 Ch16

Data Experiment 使用 Ch16 的统一协议：

```text
Frozen Evaluation Set
Population Accounting
Paired Comparison
Confidence / Uncertainty
Cluster-aware Analysis
Budget / Cost Reporting
Claim Scope
```

本章不再重新建立一套统计学。

这里只强调：

> **Data intervention 的结论必须在独立、冻结、与 tuning 隔离的 measurement system 上成立。**

---

# 21.22 Training Variance 与 Evaluation Variance 分开

Training 随机性可能来自：

```text
seed
batch order
sampling
optimizer
```

Evaluation 随机性可能来自：

```text
inference sampling
environment stochasticity
judge variance
tool instability
```

所以出现：

```text
+0.7pt
```

时，需要知道噪声主要在哪一层。

资源有限可以：

```text
single-seed exploratory pilot
↓
promising
↓
multi-seed / repeated confirmatory run
```

无需每个小想法都一开始做最昂贵确认。

---

# 21.23 Exploratory vs Confirmatory

### Exploratory

目标：找方向。

允许：

```text
small data
single seed
many configurations
proxy-heavy analysis
```

### Confirmatory

目标：支持论文主结论 / 上线 / 大规模投资。

要求更严格：

```text
Frozen Protocol
Held-out Eval
Matched Budget
Predefined Primary Metric
Replicates when needed
Full Cost Accounting
```

这一区分能兼顾研究速度和最终可信度。

---

# 21.24 Multiple Comparisons 与 Winner's Curse

试很多：

```text
threshold
mixture
curriculum
source
```

然后只报最好的一个，会产生选择偏差。

因此推荐：

```text
Development / Exploration Set
↓
选方案
↓
Final Confirmatory Holdout
```

不要在同一组数据上既选冠军又证明冠军。

---

# 21.25 Transfer Experiment：证明学到的是 Capability，不是模板

例如训练数据全来自 Calendar 的：

```text
Negative Constraint Handling
```

测试不应只继续 Calendar。

还可以测：

```text
File
Email
Order
CRM
```

如果都提升，更能支持：

```text
capability transfer
```

而不是：

```text
surface template memorization
```

推荐划分：

```text
Seen Family
Near Family
Held-out Family
Cross-domain Transfer
```

---

# 21.26 Regression Matrix

每个重要 Data Experiment 至少看：

```text
Target Capability
Neighboring Capabilities
General Capability
Safety / High-risk
Efficiency / Cost
Over-behavior
```

例如 Recovery 提升后，要检查：

```text
Over-retry
Over-abstention
Unnecessary Clarification
```

否则“学会恢复”可能变成“什么都先重试三遍”。

---

# 21.27 Failure Transition 比总分更能解释机制

训练前：

```text
Tool Selection 30%
Recovery 25%
Verification 10%
```

训练后：

```text
Tool Selection 15%
Recovery 10%
Verification 25%
```

可能说明模型能力边界已经移动到更深层。

因此还应看：

```text
Failure Type Transition
Severity Transition
Recoverability Transition
```

这会直接给下一轮 Ch17 / Ch18 提供新信号。

---

# 21.28 Mechanism Check

一个 intervention 有效以后继续问：

```text
它究竟改变了什么行为？
```

例如 Recovery Preference 后：

```text
blind retry ↓ ?
error-conditioned recovery ↑ ?
verification ↑ ?
last recoverable state utilization ↑ ?
```

Mechanism Check 可以发现模型是否只是学到 shortcut。

例如：

```text
TIMEOUT → retry
PERMISSION_DENIED → retry
```

都机械重试，说明学到的不是 recovery policy，而只是 retry habit。

---

# 21.29 Data Scaling 与 Stop Decision

实验最终需要落到：

```text
SCALE
MAINTAIN
REVISE
STOP
RETIRE
```

典型判断：

### SCALE

```text
稳定提升
无关键 regression
ROI 高
尚未饱和
```

### MAINTAIN

```text
有价值但接近 saturation
```

### REVISE

```text
有 signal，但 source / filter / supervision 需改
```

### STOP

```text
无稳定收益或机会成本过高
```

### RETIRE

```text
能力已饱和 / 环境已变化
```

投资决策归 Ch18，但证据由本章产生。

---

# 21.30 Experiment Registry

重要实验至少保存：

```text
experiment_id
research_question
baseline
intervention_type
data_version
mixture_version
training_config
eval_protocol
budget_match_rule
seed_policy
primary_metric
regression_metrics
cost
result
conclusion
next_action
```

这是 Experiment-level lineage，底层治理规则统一见第 19 章。

---

# 21.31 一个推荐 Manifest

```yaml
experiment_id: recovery_pref_v3
question: Does recovery preference improve recoverable tool-failure success?
base_model: model_v17
baseline_data: mixture_v9
treatment_data: recovery_pref_v3
intervention: replace_3_percent_tokens
matched_budget: true
train_tokens: 8B
seeds: [11, 23, 37]
primary_eval: recovery_holdout_v4
secondary_eval:
  - general_agent_v8
  - safety_regression_v5
primary_metric: recovery_success
```

它让半年后的实验仍然可以复盘。

---

# 21.32 Negative Result 也是正式资产

如果：

```text
+0.1pt within noise
```

不能写成：

```text
Recovery Data 没有价值
```

更严谨的是：

> 在当前 base model、数据构造、mixture、预算和 evaluation protocol 下，没有观察到稳定增益。

即：

```text
No Evidence of Benefit
≠ Evidence of No Possible Benefit
```

Negative / Null Result 应进入 Registry，避免团队重复做同一个失败方案。

---

# 21.33 Leakage：Failure Seed 不能直接变成 Test Memorization

危险流程：

```text
Test Failure
↓
原题进训练
↓
还在原题上证明提升
```

更好的是：

```text
Observed Failure
↓
抽象 Capability
↓
生成 sibling training family
↓
原 failure 留作 Regression
↓
另一个 held-out family 测 Transfer
```

这样才能区分：

```text
case repair
```

和：

```text
capability learning
```

---

# 21.34 Split 粒度要匹配 Claim

根据要证明的泛化范围，split 可以是：

```text
Sample
Entity
Template
Family
Workflow
Environment
Domain
```

如果只是 sample random split，却共享：

```text
same seed
same workflow
same template
```

就不能声称强泛化。

Split / contamination 的系统规则见第 16 / 19 章。

---

# 21.35 Canonical Case C1：Recovery Data Experiment

问题：

> Tool Failure 后的恢复能力差。

候选 intervention：

```text
A. Recovery SFT
B. Recovery Preference
C. Wrong + Critique + Correction
D. Hybrid
```

Pilot：

```text
5k each
matched token budget
```

Primary：

```text
Recoverable-failure Success
```

Guardrail：

```text
Over-retry
General Tool-use
Latency
```

如果 Hybrid 最优，继续：

```text
5k → 20k → 50k scaling
```

若 20k 后边际收益明显下降：

```text
MAINTAIN / STOP SCALE
```

然后把下一轮预算转给新的 failure frontier。

这就是完整的：

```text
Hypothesis
→ Intervention
→ Matched Training
→ Frozen Eval
→ Scaling
→ Mechanism
→ Decision
```

---

# 21.36 研究方法迁移：More Thinking / K17 为什么与本章同构

这类研究都遵循同一个实验纪律：

```text
冻结大部分条件
↓
只改变一个 intervention
↓
看 Repair / Degradation / Cost
```

Reasoning intervention 可以是：

```text
Continue / Stop
Branch / Repair
Candidate Selection
```

Data intervention 则是：

```text
Add / Replace / Reweight / Transform Data
```

共同原则：

> **不要只看平均结果，要同时解释修了什么、伤了什么、花了多少，以及结论在哪个 population / protocol 下成立。**

---

# 21.37 常见失败模式

1. Data Quality 高就宣布 Training Value 高。
2. Add Data 同时加预算，却把提升全归因数据。
3. 只做 Add，不做 Replace / budget-matched comparison。
4. 一次单 seed 提升就宣布稳定结论。
5. Target Gain 提升，不看 Regression / Over-behavior。
6. Hardest Data 默认等于 Best Data。
7. Judge / Proxy 提升就当 Downstream 提升。
8. 调很多配置后直接在同一 eval 报最优结果。
9. 同模板测试提升就声称 Capability 泛化。
10. Mining Signal 强就默认 Training Value 高。
11. Null Result 被写成“永远无效”。
12. Experiment 没版本，半年后无法知道结果来自哪批数据。
13. Failure Seed 原题直接进训练，造成 leakage。

---

# 21.38 从数据岗位视角，本章实际在做什么？

典型工作：

```text
定义 data intervention
设计 baseline / treatment
做 matched-budget training
跑 small pilot
画 scaling curve
比较 quality / quantity / source
做 mixture / curriculum / supervision-form experiment
做 transfer / regression / mechanism check
维护 experiment registry
把结果交回 Ch18 做 Scale / Stop 决策
```

成熟的数据实验能力体现在：

> **能把“我觉得这批数据不错”变成一个可反驳、可复现、可决策的训练实验。**

---

# 21.39 面试 / 自检问题

1. Intrinsic Data Quality 和 Downstream Learning Value 有什么区别？
2. 一个 Data Experiment 最少要定义哪些对象？
3. Add / Remove / Replace / Reweight 分别回答什么问题？
4. 为什么 Matched-budget 很重要？
5. Add Experiment 为什么适合 Pilot 但不足以单独做正式归因？
6. Remove Ablation 下降为什么不代表继续加数据仍有高价值？
7. 为什么要画 Scaling Curve？
8. Quantity vs Quality 应怎样公平比较？
9. Filter Threshold 为什么需要 downstream experiment？
10. Difficulty / Frontier 数据为什么不能凭 intuition 选择？
11. Mixture Sweep 要看哪些 guardrail？
12. Interaction Experiment 能发现什么？
13. 同一个 failure 为什么要比较不同 supervision interface？
14. Mining Policy 为什么也需要训练后验证？
15. Proxy Score 怎么验证是否真的代表 Training Value？
16. Exploratory / Confirmatory Experiment 有什么区别？
17. Transfer Experiment 为什么要跨 family / domain？
18. Failure Transition 为什么比总分更能解释机制？
19. Mechanism Check 如何识别 shortcut？
20. Negative Result 应怎样严谨表述？
21. Data Experiment 最终为什么必须落到 Scale / Maintain / Stop 决策？

---

# 21.40 本章最终心智模型

```text
Hypothesis
↓
Data Intervention Manifest
↓
Control / Baseline
↓
Matched Budget
↓
Frozen Training Recipe
↓
Frozen Evaluation
↓
Target + Regression + Cost
↓
Transfer / Mechanism / Stability
↓
Scaling Curve
↓
Decision
```

一句话总结：

> **把“数据”当成一个可控 intervention，而不是一个静态文件。**

第 20 章回答：

```text
模型应该看到什么数据分布？
```

第 21 章回答：

```text
这个分布真的让模型变好了吗？
```

下一章第 22 章再继续回答：

> **已经知道什么值得生产以后，怎样把它稳定、可追踪、可恢复地规模生产出来？**