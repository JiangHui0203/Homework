# 第 9 章 Hard Case Mining 与 Curriculum：下一批数据到底该从哪里来

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 8 章 Rollout、Rejection Sampling 与 Candidate Selection`](./08_Rollout_Rejection_Sampling_and_Candidate_Selection.md)
>
> 关联章节：[`第 4 章 Reasoning Data`](./04_Reasoning_Data_and_Process_Supervision.md)、[`第 7 章 Synthetic Data`](./07_Synthetic_Data_Generation_and_Synthesis.md)、[`第 14 章 Failure Taxonomy`](./14_Agent_Failure_Taxonomy.md)、[`第 16 章 Benchmark Design`](./16_Benchmark_Design_and_Evaluation_Protocol.md)、[`第 18 章 Data Strategy / Valuation`](./18_Data_Strategy_and_Data_Valuation.md)、[`第 21 章 Data Experiments`](./21_Data_Experiments_and_Causal_Validation.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**Hard Case Acquisition / Capability Frontier / Uncertainty / Disagreement / Near-miss / Adversarial Mining / Active Learning / Curriculum 的 canonical chapter。正式 Data Value、ROI、Portfolio 与 Stop Rule 归第 18 章。**
>
> 本章核心问题：**数据生产真正稀缺的不是“还能不能再造更多”，而是如何把有限生成、标注和训练预算放在当前模型最值得学习的 state / case 上。**

---

# 9.0 从“更多数据”到“更值得采的数据”

当系统已经具备：

```text
Task Synthesis
↓
Rollout
↓
Verifier / Judge
↓
Candidate Selection
↓
Training Data
```

下一个真正困难的问题就是：

> **下一批 Task / State 应该选什么？**

如果继续随机扩量，随着模型变强会出现大量：

```text
已经稳定会做
决策模式重复
错误率接近 0
训练信息高度冗余
```

所以 Acquisition 越来越关心：

```text
Where does the model still fail?
Where is it unstable?
Where do models disagree?
Where is failure still recoverable?
Which failure is important enough to fix?
```

Hard Case Mining 本质上是：

> **从大规模候选数据里定位“下一单位监督最可能有价值”的区域。**

至于这个价值如何正式进入资源配置、ROI 和 Portfolio，统一交给第 18 章。

---

# 9.1 Hard Case 不是一个概念，而是五种“难”

## 9.1.1 Human-hard

对人类认知上很难：

```text
高等数学证明
复杂法律推理
冷门医学知识
```

但不一定对模型难。

---

## 9.1.2 Model-hard

对当前模型难：

```text
Current-model success low
```

例如：

```text
人觉得复杂但模型 95% 正确
人觉得简单但模型 40% 正确
```

从当前训练角度，后者可能更值得研究。

所以：

> **Human Difficulty ≠ Model Difficulty。**

---

## 9.1.3 State-hard

同一个 Task 内，真正困难的可能只是某个局部 state：

```text
关键分支
实体消歧
工具选择
约束冲突
修复节点
```

所以：

```text
Hard Task
≠
Hard State
```

这对 Reasoning / Agent 特别重要。

---

## 9.1.4 Evaluation-hard

有些 case 的困难主要在：

```text
Judge disagreement
Gold ambiguity
Multi-path validity
Verification cost
```

它更适合作：

```text
Gold Expansion
Judge Calibration
Rubric Refinement
Adjudication
```

而不是直接当训练难例。

---

## 9.1.5 Learning-hard / Learning-valuable

当前模型答错，不代表值得训练。

例如：

```text
坏题
标签不可验证
极端低价值冷知识
与产品目标无关
几乎不可学
```

所以真正值得采的 case 通常还需要满足：

```text
Capability Gap Exists
Relevant
Verifiable
Learnable
Not Pure Duplicate
```

正式的 Data Value 函数、边际价值和资源分配归第 18 章；本章只负责**发现候选 acquisition region**。

---

# 9.2 Capability Frontier：最值得盯的是能力边界

可以把模型能力空间想成：

```text
Stable-success Region
↓
Frontier Region
↓
Stable-failure Region
```

Frontier 的典型特征：

```text
Sometimes Correct
Sometimes Wrong
Decision Unstable
Small intervention may matter
```

它通常比纯 easy region 信息量高，也比“几乎完全不会”的区域更容易形成有效学习信号。

但不能机械规定：

```text
30%–70% success 一定最好
```

真正的 frontier 必须结合：

```text
Model
Task Family
Capability
Training Objective
```

实验估计。

---

# 9.3 Frontier 是 Model-relative，也是动态的

Hard 必须写清：

```text
hard for which model?
```

例如：

```text
Model v1 hard
↓ training
Model v2 easy
```

所以 hard-case asset 最好记录：

```text
mined_by_model
model_version
prompt / runtime version
measured success
mining signal
```

Hard Pool 不应永久冻结为“永远困难”。

更合理：

```text
Model v1
↓ Mine Frontier
↓ Train
Model v2
↓ Re-evaluate Old Pool
↓ Mine New Frontier
```

这就是 Model–Data Co-evolution。

---

# 9.4 Error-driven Sampling：从真实失败开始

最直接流程：

```text
Current Model
↓
Eval / Production / Rollout
↓
Verified Failures
↓
Failure Taxonomy
↓
Targeted Sampling
```

例如 failure profile：

```text
Observation Grounding 17%
Tool Selection          8%
Recovery                6%
Verification            3%
```

不能简单因为 17% 最大就全部做 Observation Grounding。

还要看：

```text
Severity
Target Importance
Learnability
Verifiability
Existing Coverage
```

Failure 的 canonical taxonomy 与 owner 见第 14 章。

---

# 9.5 Error Count ≠ Acquisition Priority

两个 failure：

```text
A：30%，多一次冗余 tool call
B：2%，会错误删除文件
```

显然 B 可能优先级更高。

所以 mining signal 可以来自：

```text
Frequency
Severity
Risk
Business Criticality
Novelty
Recoverability
```

但正式 Data Investment priority 和 ROI 不在本章定最终结论，交给第 18 章。

---

# 9.6 Uncertainty Sampling：在决策边界附近找样本

常见 LLM uncertainty signal：

```text
Token Entropy
Min / Mean Logprob
Top1–Top2 Margin
Sequence Likelihood
Self-consistency Disagreement
Candidate Score Margin
```

经典直觉：

```text
高 uncertainty
→ 可能接近当前模型 decision boundary
→ 人工 / verifier supervision 可能更有信息量
```

但必须牢记第 4 章定义：

```text
High Risk / Uncertainty
≠ Wrong
≠ Recoverable
≠ High Data Value
```

Uncertainty 在这里的角色只是：

> **Acquisition Signal。**

---

# 9.7 Calibration：Uncertainty Threshold 需要有经验语义

如果一个 logprob threshold 被用来 mining，最好知道：

```text
不同 score bucket 的 empirical outcome
```

例如：

```text
High-confidence bucket → 97% correct
Mid bucket             → 80%
Low-confidence bucket  → 58%
```

否则：

```text
score = -1.2
```

本身没有可解释 acquisition meaning。

这里不是要求所有 score 都完美 calibrated，而是：

> **至少知道你的 mining signal 与真实 outcome 大概是什么关系。**

---

# 9.8 Disagreement Mining：不一致是边界信号

Disagreement 可以来自三类。

## Model vs Model

```text
Old vs New
Small vs Large
Family A vs Family B
```

尤其：

```text
Old Correct → New Wrong
```

非常适合 regression mining。

## Same Model, Multiple Rollouts

```text
A, A, B, C
```

说明 policy 对这个 state 不稳定。

## Model vs Evaluator

```text
Agent says success
Environment says fail
```

可能暴露 self-evaluation / verification 问题。

Disagreement 本身不是 ground truth，而是：

> **值得进一步验证的 acquisition cue。**

---

# 9.9 Hard Negative Mining

Hard Negative：

> **表面高度合理，但存在决定性错误的负例。**

例如：

```text
数学：只错一个符号
代码：只漏一个边界条件
Agent：动作基本正确但漏关键 constraint
Reasoning：前缀正确，关键 branch 选错
```

相比乱码或明显答非所问：

```text
Hard Negative
```

更能教会模型真正的 decision boundary。

生成 Hard Negative 的方法已在第 7 章展开，本章更关注：

> **怎样从真实模型行为里把高信息量 negative 挖出来。**

---

# 9.10 Near-miss：差一点做对的失败通常很珍贵

典型 Near-miss：

```text
最后一步算错
只漏一个 constraint
完成写操作但没 verify
正确 prefix 后只选错一个 branch
```

它们通常具有：

```text
Existing Partial Capability
Localized Failure
Clear Counterfactual
Lower Repair Distance
```

因此特别适合：

```text
Correction
Preference
Recovery
First-error / Last-recoverable Analysis
```

---

# 9.11 Adversarial Generation：主动寻找有效弱点

基本流程：

```text
Observed Weakness
↓
Adversarial Generator
↓
Valid Challenging Cases
↓
Current Model Rollout
↓
Keep Verified Failures
```

但：

```text
Adversarial
≠ Weird
```

好的 adversarial case 仍然应该：

```text
Valid
Relevant
Plausible
Capability-targeted
```

而不是靠语言绕口或现实中不存在的条件制造“假难”。

---

# 9.12 Active Learning：人工 / 验证预算投给谁？

假设：

```text
1,000,000 unlabeled rollouts
```

只能人工处理：

```text
10,000
```

可以定义 acquisition score：

$$
a(x)=f(U,D,R,N,C)
$$

其中例如：

```text
U = uncertainty
D = disagreement
R = risk / severity
N = novelty
C = capability importance
```

这里的函数不必复杂。

真正重要的是：

> **明确为什么这个 case 比另一个 case 更值得消耗人工 / verifier budget。**

---

# 9.13 不能只追最难：Hardness 需要和 Coverage / Diversity 共存

如果 acquisition 永远选最难：

```text
大量不可学 case
标注成本飙升
数据分布严重偏移
基础覆盖丢失
```

所以 acquisition 往往需要平衡：

```text
Hardness
Coverage
Diversity
Risk
Novelty
```

正式 Portfolio allocation 见第 18 章。

---

# 9.14 Diversity-aware Mining：别让 Hard Pool 被一个 failure 淹没

假设 10 万 failure 中：

```text
80k = 同一种 order-id formatting error
```

全收会让数据严重偏斜。

更合理：

```text
Cluster
↓
Estimate Frequency
↓
Keep Representative Cases
↓
Preserve Rare High-severity Cases
```

目标不是简单复制线上频率，而是同时保留：

```text
Population Evidence
+
Failure-space Coverage
```

---

# 9.15 Root-cause Mining：不要只按表面现象补数据

现象：

```text
Wrong Tool
```

根因可能是：

```text
Tool descriptions 太相似
Entity resolution 错
Negative constraint 没理解
Harness context 丢失关键 evidence
```

如果不先诊断，就会出现：

```text
Wrong Tool
→ 再生成更多 tool-selection SFT
```

但真实 bottleneck 根本没被修。

因此推荐链条：

```text
Observed Failure
↓
Failure Owner / Root Cause
↓
Capability Gap
↓
Acquisition Strategy
```

Failure Owner / Root Cause 归第 14 章。

---

# 9.16 Failure Seed → Synthetic Family

最实用的闭环之一：

```text
Real Failure
↓
Abstract Capability Gap
↓
Generate Same-capability Variants
↓
Verify
↓
Train
↓
Original Failure stays in Regression
```

例如：

```text
“不要改周会”被忽略
```

抽象为：

```text
Negative Constraint Handling
```

扩展到：

```text
Files：不要删 .env
Orders：VIP 不要动
Email：不要发 external contact
Code：protected branch 不要 push
```

这才是从一个 failure 学到一个能力，而不是记住一个 case。

---

# 9.17 Regression Holdout：原 failure 不应该既训练又证明自己被修好

危险做法：

```text
Failure Case F
→ 直接放进训练
→ 再在 F 上测试
→ 宣称问题解决
```

更合理：

```text
Failure F
↓
Keep F hidden as regression
↓
Generate related-but-distinct training family
↓
Train
↓
Evaluate on F + fresh same-capability cases
```

这让结果更接近真正 transfer，而不是 memory。

正式 split / leakage protocol 见第 16、19 章。

---

# 9.18 Curriculum：数据顺序也是一种训练策略

典型 curriculum：

```text
Easy
↓
Medium
↓
Hard
↓
Frontier
```

Agent 可以按 decision complexity：

```text
L1 Single Tool
L2 Tool Selection
L3 Multi-step Dependency
L4 Constraint Handling
L5 Failure Recovery
L6 Long Horizon
L7 Adversarial / Ambiguous
```

重要的是：

> **顺序应该对应能力结构，而不是只按 prompt 长度。**

---

# 9.19 Curriculum、Static Mixture、Hard-first 都只是 Hypothesis

“Easy → Hard”很直觉，但不自动正确。

可能失败：

```text
difficulty definition wrong
stage distribution shift too large
forgetting
model already knows easy part
```

所以应该比较：

```text
Curriculum
vs
Static Mixture
vs
Random Shuffle
vs
Hard-first / Frontier-heavy
```

最终是否有用由第 21 章 Data Experiment 证明，而不是靠教育学直觉。

---

# 9.20 Self-paced / Competence-aware Curriculum

更动态的策略：

```text
Current Model Performance
↓
Estimate Frontier
↓
Choose Next Difficulty Band
```

例如：

```text
Stable Success
→ reduce exposure

Frontier
→ increase exposure

Near-zero Success
→ simplify / decompose / prerequisite training
```

重点不是固定阈值，而是：

> **训练数据随着模型能力变化而重新分配。**

---

# 9.21 Mining Signal ≠ Training Label

这是本章最重要的一条纪律之一。

```text
Low Logprob
High Entropy
Disagreement
Long Trace
Judge Conflict
```

都可以负责：

```text
“把 case 找出来”
```

但最终训练 label 仍然需要：

```text
Verifier
Human / Expert
Environment Outcome
Counterfactual Evidence
```

所以：

> **Acquisition Signal 负责“去哪看”，Ground Truth / Supervision 负责“看完以后怎么教”。**

---

# 9.22 Triggered Pool 不等于 Error Pool

如果使用某个 trigger：

```text
low confidence
specific failure heuristic
high disagreement
```

得到：

```text
Triggered Cohort
```

这个 cohort 里面仍然可能有：

```text
Correct Cases
Wrong Cases
Recoverable Cases
Unrecoverable Cases
Potentially Harmful Interventions
```

所以必须明确：

```text
Triggered
≠
Wrong
```

这点对 uncertainty-based reasoning / Agent mining 尤其重要。

---

# 9.23 Trigger-based Mining 会引入 Selection Bias

如果所有研究数据都来自：

```text
P(data | triggered)
```

结论不能直接外推到：

```text
P(all data)
```

所以最好保留：

```text
Sampling Frame
Trigger Rate
Untriggered Reference Sample
Population Accounting
```

总体 denominator discipline 归第 16 章。

---

# 9.24 研究实例：More Thinking 的 State Frontier

`More Thinking Is Not Always Better` 类问题展示了：

```text
Hard Task
≠
Continue-worthy State
```

同一 Task 在不同 reasoning state 上：

```text
继续计算可能 Rescue
也可能 Degrade
```

所以比“题目难度”更有价值的 acquisition unit 是：

```text
Current Reasoning State
+
Potential Continuation Value
```

这可以理解为 state-conditioned frontier：

> **不是寻找最难题，而是寻找下一单位 compute / supervision 最可能改变 outcome 的 state。**

---

# 9.25 研究实例：K17 的 Low-confidence Trigger 是 Acquisition，不是 Error Label

典型结构：

```text
All Reasoning States
↓
Low-confidence / Risk Signal
↓
Triggered Pool
↓
Same-prefix Candidates
↓
Offline Outcomes
```

Low-confidence signal 做的是：

```text
Acquisition / Exploration Gating
```

不是：

```text
Ground-truth Error Detection
```

所以：

```text
Low Confidence
≠ Wrong
≠ Recoverable
```

只有后续同前缀 outcome evidence 才能进一步判断局部 intervention 是否有潜在价值。

---

# 9.26 Hard Case Pool 数据结构

建议至少保留：

```json
{
  "case_id": "hc_001",
  "source": "production",
  "mined_by_model": "agent_v7",
  "mining_signal": {
    "type": "disagreement",
    "value": 0.84
  },
  "verified_failure_type": "observation_grounding",
  "severity": "high",
  "model_success_rate": 0.41,
  "frontier_band": "frontier",
  "root_cause_ref": "failure_031",
  "regression_holdout": true,
  "recommended_action": "generate_same_capability_variants"
}
```

注意区分：

```text
mining_signal
```

和：

```text
verified_failure / supervision
```

它们不应该共用同一字段。

---

# 9.27 如何评价 Mining Pipeline？

可以看：

```text
Mining Precision
目标 failure 的命中率

Coverage
不同 capability / failure 是否被覆盖

Novelty
是否只是重复旧 cluster

Frontier Density
是否集中在当前模型边界

Verifiability Rate
多少样本能可靠判定

Training Yield
多少样本最终可转成训练 data

Downstream Gain
训练以后是否真的改善目标能力
```

最后一项仍然需要第 21 章 controlled experiment 才能回答。

---

# 9.28 本章与第 18 章的边界：Mining ≠ Data Strategy 全部

本章可以说：

```text
这个 case 很 hard
这个 state 很 uncertain
这个 failure 很 rare
这个 cluster 很 novel
```

但最终“值不值得投预算”还需要第 18 章进一步考虑：

```text
Business Importance
Data Cost
Expected Learning Value
Risk
Portfolio Balance
Marginal ROI
Stop Rule
```

所以：

> **Ch9 负责发现值得考虑的数据候选；Ch18 负责决定资源最终投向哪里。**

---

# 9.29 常见失败模式

1. 把所有错误样本都叫 Hard Case。
2. 只选最低置信样本。
3. 把 Uncertainty 当 Correctness Label。
4. Hard Pool 被单一 failure cluster 淹没。
5. 用 Human Difficulty 代替 Model Difficulty。
6. 训练数据直接泄漏 hidden regression case。
7. Adversarial 变成现实中不存在的怪题。
8. 只追最难，不看 learnability / verifiability。
9. Curriculum 没有 static / random baseline。
10. Hard Case 不记录 model version。
11. 只看 task-level hard，不看 state-level hard。
12. Frontier 已移动，但 data allocation 没更新。
13. Triggered cohort 被错误描述成 error cohort。
14. 对 triggered-only 数据得出 full-population 结论。
15. 在本章就直接把“hardness”升级成完整 Data ROI 结论。

---

# 9.30 从数据岗位视角，这一章实际会做什么？

```text
跑 current-model rollout / eval
建立 failure pool
按 confidence / entropy / disagreement 筛 case
做 failure clustering
识别 near-miss
建立 capability frontier
设计 acquisition function
做 adversarial generation
从真实 failure 生成 synthetic family
维护 hidden regression
设计 curriculum / self-paced bands
监控 triggered cohort bias
把候选 hard pool 交给 Data Strategy 做最终 budget allocation
```

所以 Hard Case Mining 不是简单“挑难题”，而是：

> **用模型行为和失败证据主动决定下一批数据从哪里来。**

---

# 9.31 本章关键词

| 术语 | 一句话理解 |
|---|---|
| Hard Case | 对当前模型存在重要能力缺口的候选样本 |
| Model-hard | 对特定模型表现困难 |
| State-hard | 轨迹局部状态上的决策困难 |
| Evaluation-hard | evaluator 难以可靠判定的 case |
| Capability Frontier | Stable Success 与 Stable Failure 之间的能力边界 |
| Error-driven Sampling | 从 verified failure 反向选择数据 |
| Uncertainty Sampling | 从模型不确定区域采样 |
| Disagreement Mining | 从模型 / rollout / evaluator 不一致中找边界样本 |
| Hard Negative | 高相似、关键处错误的负例 |
| Near-miss | 大部分已正确、局部失败的 case |
| Adversarial Generation | 主动构造目标能力上的有效挑战 |
| Active Learning | 在有限监督预算下选择最值得标的数据 |
| Acquisition Signal | 用于决定“去哪看”的信号 |
| Curriculum | 按能力 / 难度组织训练顺序或 exposure |
| Self-paced Learning | 根据当前模型能力动态选择下一阶段数据 |
| Failure Seed | 可扩展成同能力 synthetic family 的真实失败 |
| Regression Holdout | 原始重要 failure 保留作隐藏回归，不直接训练 |
| Trigger Bias | 条件采样导致研究分布偏离总体分布 |

---

# 9.32 面试 / 自检问题

1. 什么叫 Hard Case？为什么不等于所有错误样本？
2. Human-hard、Model-hard、State-hard、Evaluation-hard 有什么区别？
3. 为什么 Capability Frontier 很重要？
4. Frontier 为什么是 model-relative、动态的？
5. Error-driven Sampling 的正确起点是什么？
6. Error Count 为什么不等于 Priority？
7. Uncertainty 在本章是什么角色？
8. 为什么 Uncertainty 不是 Error Label？
9. Disagreement Mining 有哪些来源？
10. Near-miss 为什么通常很有价值？
11. Adversarial Case 怎么避免变成无意义怪题？
12. Active Learning 的 acquisition function 可以包含什么？
13. 为什么不能只追最难？
14. 如何避免 Hard Pool 被一个 failure cluster 淹没？
15. Root Cause 为什么应该先于 targeted data generation？
16. 如何从一个真实 failure 生成 synthetic family？
17. 为什么原 failure 应该保留 hidden regression？
18. Curriculum 为什么必须和 static / random baseline 比较？
19. 什么是 Self-paced Curriculum？
20. Mining Signal 与 Training Label 有什么区别？
21. Triggered Pool 为什么不是 Error Pool？
22. Trigger-based mining 为什么需要 Population Accounting？
23. Ch9 和 Ch18 的职责边界是什么？
24. 如何证明一个 hard-case mining pipeline 真正有用？

---

## 9.32.1 一个通用回答框架：下一批数据应该做什么？

```text
1. 从 Eval / Production / Rollout 获取 verified outcomes
   ↓
2. 先用 Ch14 taxonomy 做 Failure Attribution
   ↓
3. 再用 uncertainty / disagreement / near-miss 做 acquisition
   ↓
4. 建 cluster，防止单一 failure 重复淹没
   ↓
5. 找当前 model-specific frontier
   ↓
6. 保留重要 failure 做 hidden regression
   ↓
7. 从 root cause 生成 same-capability variants
   ↓
8. 用 Ch18 做最终 Data Investment priority
   ↓
9. 用 Ch21 验证 targeted data / curriculum 是否有 causal gain
```

最关键的一句话是：

> **Hardness 只告诉你“这里值得看”，真正的数据决策还要经过验证、归因、资源配置和下游实验。**

---

# 9.33 本章最终要形成的认识

第 7–9 章现在可以清楚连成：

```text
Ch7 Synthetic Data
→ 怎样造出新经验

Ch8 Candidate Selection
→ 已经有多个候选后怎样利用它们

Ch9 Hard Case Mining
→ 下一批经验应该去哪里找
```

因此整个 Acquisition Loop 是：

```text
Current Model
↓
Rollout / Production
↓
Failure / Uncertainty / Disagreement
↓
Hard State / Frontier
↓
Targeted Synthesis
↓
Candidate Pool
↓
Selection / Routing
↓
Training
↓
New Model
↓
Re-mine Frontier
```

下一部分将进入 Agent 的 Task / Environment / Trajectory 世界：

> **不再只问“数据从哪里来”，而是正式定义“Agent 到底在什么问题、什么世界、什么状态空间里行动”。**
