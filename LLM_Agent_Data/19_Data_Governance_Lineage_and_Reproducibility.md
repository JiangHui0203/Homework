# 第 19 章 Data Governance、Lineage 与 Reproducibility：让每个数据结论都能追溯到源头

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 18 章 Data Strategy 与 Data Valuation`](./18_Data_Strategy_and_Data_Valuation.md)
>
> 关联章节：[`第 6 章 Human Data`](./06_Human_Data_Annotation_and_Quality_Control.md)、[`第 12 章 Agent Trajectory Anatomy`](./12_Agent_Trajectory_Anatomy.md)、[`第 15 章 Grader、Verifier 与 LLM-as-a-Judge`](./15_Grader_Verifier_and_LLM_as_a_Judge.md)、[`第 16 章 Benchmark Design 与 Evaluation Protocol`](./16_Benchmark_Design_and_Evaluation_Protocol.md)、[`第 17 章 Data Flywheel`](./17_Data_Flywheel_and_Continuous_Improvement.md)、[`第 22 章 Data Production System`](./22_Data_Production_System.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> **Master Figure：** [`F11 — Governance / Lineage DAG`](./figures/F11_Governance_Lineage_DAG.md)
>
> 本章定位：**Identity / Provenance / Lineage / Versioning / Reproducibility，以及 Historical Decision / Corrected Label / Re-score / Re-run / Replay 边界的 canonical chapter。**
>
> 本章核心问题：**一条数据、一条标签、一次评测、一个模型版本，能不能回答“它是谁、从哪来、经历了什么、谁判的、为什么被选中、后来哪里变了、影响过什么，以及今天能不能重新得到同一个可解释结论”。**

---

# 19.0 Governance 的本质：Controlled Change

数据系统一定会变化：

```text
Data changes
Labels change
Rubrics change
Judge changes
Schema changes
Benchmark changes
Environment changes
```

治理的目标不是：

```text
No Change
```

而是：

> **允许系统变化，但变化必须有身份、有原因、有版本、有 lineage，历史事实不能被静默改写。**

可以压成：

```text
Raw Facts
→ preserve

Derived Labels
→ correctable + versioned

Dataset Views
→ rebuildable

Historical Decisions
→ frozen as history

Current Policies
→ rerunnable as new experiments
```

所以：

> **Governance = Controlled Change。**

---

# 19.1 七个治理问题

一个成熟数据系统至少回答：

```text
Identity
→ 它是谁？

Origin / Provenance
→ 从哪来？

Transformation
→ 经历了什么？

Decision
→ 为什么被保留 / 删除 / 标成这样？

Usage
→ 被哪些 Dataset / Run / Model 用过？

Change
→ 后来哪里变了？

Reproducibility
→ 能否按相同定义重新得到可比结果？
```

再加两条边界：

```text
Rights / Privacy
→ 能不能用？

Auditability
→ 出问题能不能追？
```

---

# 19.2 Stable Identity：Identity 不等于当前内容

一个对象应该有稳定 ID，即使它的 label / metadata 后来改变。

常见：

```text
task_id
case_id
episode_id
trajectory_id
sample_id
annotation_id
evaluation_id
dataset_id
run_id
model_id
```

例如：

```text
sample_id = s_1847
```

今天 label：

```text
failure_type = tool_selection
```

后来修正成：

```text
failure_type = observation_grounding
```

对象身份仍然是：

```text
s_1847
```

因此：

> **Identity 是“这是谁”，Label 是“我们现在如何解释它”。**

不要用可变内容 hash 直接代替全部业务 identity；hash 更适合完整性校验。

---

# 19.3 Raw / Canonical / Derived / View / Run：五层数据模型

推荐书级治理结构：

```text
L0 Raw Evidence
        ↓
L1 Canonical Records
        ↓
L2 Labels / Scores / Metadata
        ↓
L3 Curated Assets / Dataset Views
        ↓
L4 Runs / Models / Reports
```

## Raw Evidence

尽量保存原始事实：

```text
raw prompt / request
raw model output
raw tool result
raw environment state diff
raw judge response
source timestamp
```

原则：

> **尽量 append-only / immutable。**

---

## Canonical Record

把 Raw 解析成稳定 schema：

```text
normalized messages
parsed tool calls
canonical timestamps
normalized IDs
canonical event schema
```

Canonical 是标准表示，不是新真相。

---

## Derived Layer

由 Rule / Model / Human 推导：

```text
label
reward
failure type
quality score
embedding
cluster
judge score
selection score
```

关键纪律：

> **Derived information must not masquerade as raw truth。**

`judge_score=0.91` 只是某个 evaluator 在某个版本下的输出。

---

## Dataset View

从 Canonical + Derived 数据按 Build Recipe 派生：

```text
SFT View
Preference View
Regression View
Benchmark View
Recovery View
```

因此：

```text
Dataset View
=
Source Assets + Build Recipe + Version
```

---

## Run / Model / Report

这些是使用数据资产产生的下游节点：

```text
Training Run
Evaluation Run
Model Checkpoint
Benchmark Report
```

它们也必须进入 lineage graph。

---

# 19.4 Provenance：一条数据的出生证明

Provenance 回答：

> **这个对象最初从哪里来？**

可能包括：

```text
source_type
source_system / URI
source_time
human author / annotator pool
teacher model / checkpoint
generator prompt
sampling config
seed object
license / consent status
```

Synthetic 样本尤其需要：

```text
seed_id
family_id
generator_model
generator_prompt_version
generation_config
```

这样才能追：

```text
Production Failure
↓
Seed
↓
Synthetic Family
↓
Training View
```

---

# 19.5 Lineage：不是文件路径，而是关系图

全书的 canonical lineage visual 统一由 [`F11 — Governance / Lineage DAG`](./figures/F11_Governance_Lineage_DAG.md) 维护。

这里保留本章真正需要的三层语义：

```text
Lineage Node
= 数据、标签、Dataset View、Run、Model、Report 等稳定对象

Lineage Edge
= parent → child 的 transformation / usage 关系

Lineage Query
= 沿 DAG 正向或反向追踪影响范围
```

Lineage 节点和边应回答：

```text
parent
child
transform
version
actor / code
reason
when
```

这使系统能做反向追踪：

```text
Model issue
→ Training Run
→ Mixture
→ Dataset
→ Batch
→ Label / Judge
→ Raw Source
```

也能正向追踪：

```text
Bad Label
→ affected Dataset Views
→ affected Training Runs
→ affected Models / Reports
```

所以重点不是再画一张第二套总 DAG，而是保证：

> **同一套 lineage graph 能同时支持“这个结果从哪里来”与“这个坏源头影响了什么”两类查询。**

---

# 19.6 Versioning 不是一个 `v2` 就结束了

至少分开：

```text
Dataset Version
Schema Version
Label Version
Taxonomy Version
Evaluator Version
Build Recipe Version
Protocol Version
Environment / Tool Version
```

这些变化语义不同。

例如：

```text
Dataset v3
```

可能是新增样本；

```text
Label v3
```

可能是同样样本被重新判定；

```text
Schema v3
```

可能是 success 被拆成 goal_success + policy_compliance。

不能全部用一个版本号掩盖。

---

# 19.7 Dataset Change Type

建议记录：

```text
ADD
REMOVE
RELABEL
REWEIGHT
REFILTER
RESCHEMA
RESPLIT
REBUILD
```

于是：

```text
v7 → v8
```

不只是“新版本”，而能知道：

```text
为什么变
什么变
受影响对象是谁
```

---

# 19.8 Schema Change：字段语义改变是 Breaking Change

早期：

```json
{"success": true}
```

后来：

```json
{
  "goal_success": true,
  "policy_compliance": false
}
```

这不是“多了两个字段”，而是 success semantics 被重构。

所以要记录：

```text
schema_version
migration
backfill_status
compatibility
```

区分：

```text
Backward-compatible
vs
Breaking
```

---

# 19.9 Label Version：标签可以修，但历史不能被抹掉

标签会因：

```text
new evidence
guideline change
judge fix
reference correction
adjudication
```

发生变化。

应保留：

```text
label_v1
label_v2
change_reason
changed_by
changed_at
evidence_refs
```

而不是静默覆盖旧 label。

---

# 19.10 Historical Decision ≠ Evaluation Label ≠ Re-execution Result

这是全书非常重要的治理纪律。

历史 Selector 当时：

```text
chose A
```

后来 Corrected Label 表明：

```text
A wrong
B correct
```

应该保留：

```text
Historical Decision = A
```

并：

```text
Re-score frozen output with corrected label
```

而不是用新 label 重新让历史 policy 改选 B，然后覆盖原实验。

因此：

```text
Historical Decision
≠ Evaluation Label
≠ Fresh Re-execution Result
```

---

# 19.11 Re-score、Re-run、Replay：三个词必须分开

## Re-score

```text
Frozen Historical Output
+
New / Corrected Label or Evaluator Mapping
↓
New Metric
```

回答：

> 历史行为按当前正确评价应得多少分？

---

## Re-run

```text
Current Model / Policy / Runtime
↓
Fresh Execution
```

回答：

> 今天重新执行会发生什么？

---

## Replay

> 尽量在冻结 / 重建的历史输入与环境条件上重新执行，用于复现或调试。

Replay 是否能得到 bit-exact output，取决于系统 deterministic 程度。

三者回答的问题不同，不能混称“重新跑一下”。

---

# 19.12 Derived View：不要复制出多份失联“真相”

同一 Canonical Trajectory 可以生成：

```text
SFT messages
Preference pair
Failure record
Regression case
Recovery example
```

每个 View 应保存：

```text
source_ids
view_type
view_version
transform_config
build_code_version
```

这样 Label 修正后可以 rebuild。

不要把五份 JSONL 复制出去后失去 parent relation。

---

# 19.13 Reproducibility：不是只有一个模型 checkpoint

一次重要 Run 至少依赖：

```text
Code
Data
Model
Prompt
Runtime
Tools
Environment
Randomness
Evaluator
Budget / Stop Rules
```

可以概念化：

```text
Run = f(
  code_commit,
  dataset_manifest,
  model,
  prompt,
  runtime,
  environment,
  seed_policy,
  evaluator,
  budget
)
```

不是要求所有系统 bit-exact，而是要求实验定义和关键 inputs 可追溯。

---

# 19.14 Reproducibility 的三个层次

## Exact Reproducibility

相同输入得到完全一致结果。

适合 deterministic verifier / data build。

## Statistical Reproducibility

随机系统重复运行得到稳定分布 / 结论。

## Protocol Reproducibility

别人能重建同一 Evaluation / Training Contract，得到可比结论。

对复杂 Agent 系统，后两者经常比 token-level exact match 更现实。

---

# 19.15 Run Manifest：实验身份证

重要 Training / Eval Run 至少保存：

```yaml
run_id: eval_001
code_commit: abc123
case_manifest: benchmark_v5_manifest.json
schema_version: task_v3
model_version: model_m17
prompt_version: prompt_v9
toolset_version: tools_v4
harness_version: harness_v7
environment_snapshot: env_s17
verifier_version: verifier_v5
judge_version: judge_v8
seed_policy: seeds_v2
budget:
  max_steps: 40
  max_tokens: 16000
```

对于正式 frozen asset，再保存：

```text
row count
IDs manifest
file / artifact hash
```

防止：

```text
名字一样
内容悄悄变了
```

---

# 19.16 Environment / Tool / Clock 也是实验版本

Agent Case 不只是 Prompt。

需要追踪：

```text
DB / filesystem / calendar snapshot
permission map
clock
timezone
locale
tool schema
tool backend version
error semantics
```

因为：

```text
Task text same
Environment changes
```

可能已经是不同 Case / difficulty。

第 11 章定义 Environment；本章负责治理版本与 lineage。

---

# 19.17 Annotation Provenance

Human Label 可以保存：

```text
annotator_id / pseudonymous id
role / expertise tier
guideline_version
UI version
candidate order
time spent
confidence
adjudication status
```

UI version 重要，因为：

```text
reference 是否可见
证据是否折叠
A/B 顺序
```

都会影响 label。

完整 Human QC 归第 6 章。

---

# 19.18 Evaluator Provenance

Judge / Grader 输出至少绑定：

```text
evaluator_type
model / version
prompt version
rubric version
evidence schema
parser / mapping version
decoding config
run_id
raw artifact
```

所以：

```text
score = 0.87
```

本身没有脱离 provenance 的独立语义。

第 15 章定义 evaluator semantics；本章定义如何长期追踪。

---

# 19.19 Sampling / Selection Provenance

为什么一条数据进入训练集，也要可追：

```text
selection_policy
sampling_probability
sampling_bucket
priority_score
hardness / risk score
failure cluster
business priority
filter reason
```

因为 Selection Policy 自己会改变训练分布。

后续若模型对某类行为过拟合，可以追溯是否源于 acquisition / weighting policy。

---

# 19.20 Split Governance 与 Family Lineage

Train / Eval Leakage 不止 exact duplicate。

还包括：

```text
Near Duplicate
Same Seed Family
Same Workflow
Same Environment Fixture
Same User Session
Benchmark-derived Synthetic Data
Teacher Solution Leakage
```

因此 Split Policy 也要版本化：

```text
split_policy_version
```

并优先按：

```text
family_id
workflow_id
seed_id
case_family
```

做 group split。

---

# 19.21 Contamination Registry

可以长期记录：

```text
benchmark / asset
known training overlap
public exposure
near-duplicate risk
synthetic derivative status
first seen date
risk assessment
mitigation
```

不要把：

```text
“我们没有主动训练测试集”
```

当作 contamination 已被证明不存在。

---

# 19.22 Training Lineage：模型也必须是 Lineage Graph 的节点

一个 Model / Checkpoint 应追溯：

```text
base model
training code commit
config
optimizer / schedule
mixture version
dataset versions
sample / token weights
seed
checkpoint parent
```

这样可以双向查询：

```text
Model → trained on what?
Dataset → used by which models?
```

如果某 Dataset 后来发现严重问题，就能定位受影响模型。

---

# 19.23 Data Card ↔ Model Card

Data Card 至少说明：

```text
Purpose
Source
Schema
Collection / Generation
Labeling / Evaluator
Population / Sampling
Known Bias
Known Limitations
Privacy / Rights
Version
Intended / Prohibited Use
```

Model Card 则应能链接：

```text
training dataset / mixture IDs
major eval protocol IDs
known data limitations
```

两者通过 lineage 形成闭环。

---

# 19.24 Privacy：治理不是只有“版本号”

线上数据可能含：

```text
姓名
邮箱
账号
地址
订单
文件
企业内部信息
敏感业务状态
```

治理原则：

```text
Data Minimization
Purpose Limitation
PII Detection
Redaction / Pseudonymization
Least Privilege
Retention
Deletion
Audit
```

最强隐私策略往往是：

> **不需要的字段就不要进入数据闭环。**

---

# 19.25 Redaction ≠ Pseudonymization

```text
Redaction:
Alice → [NAME]

Pseudonymization:
Alice → user_8f12
```

前者去除具体值；后者保留跨事件关联能力。

Pseudonymization 仍可能有 re-identification risk，不能等同于匿名化。

---

# 19.26 Access Control

不同层的数据可设置不同访问范围：

```text
Raw Production Evidence
→ most restricted

Redacted Canonical Data
→ wider internal use

Aggregated Metrics
→ broadest
```

采用：

```text
least privilege
role-based access
purpose-based access
```

而不是“做 AI 的人默认都能看全部 raw logs”。

---

# 19.27 Consent / License / Intended Use

```text
Publicly accessible
```

不自动等于：

```text
可以训练
可以商业使用
可以重新分发
```

同样，用户为完成一次 Task 提供的数据，也不自动等于可作为：

```text
training data
public benchmark
synthetic seed
```

因此 provenance 还应记录：

```text
license
consent
collection purpose
allowed downstream use
```

---

# 19.28 Retention 与 Deletion 是 Lineage 问题

删除一个 Raw Row 可能还留下：

```text
Canonical Record
Annotation
Embedding
Synthetic Derivative
Dataset View
Cache
Backup
Evaluation Artifact
```

所以删除流程必须借助 lineage 查 downstream derivatives。

同时区分：

```text
删除存储中的数据
≠
逆转它已经对训练模型参数造成的影响
```

后者可能涉及 retraining / unlearning 等额外机制。

不要用：

```text
file deleted
```

宣称：

```text
model never learned it
```

---

# 19.29 Gold / Anchor / Regression Asset 要更严格治理

这些数据会承担：

```text
Judge Calibration
Benchmark Truth
Release Gate
Regression
```

所以至少要求：

```text
strong provenance
expert / adjudication status
change history
evidence
known ambiguity
version
access boundary
```

Gold 漂移会让整个 evaluation system 跟着漂。

---

# 19.30 One Sample, Multiple Trust / Use Levels

同一条数据可能：

```text
适合 analysis
但不适合 SFT
```

或者：

```text
适合 hard-case seed
但不够资格做 benchmark gold
```

因此可以保存：

```text
allowed_uses
prohibited_uses
trust_level
verification_status
```

不要用一个全局：

```text
usable = true
```

覆盖所有用途。

---

# 19.31 Audit Trail：谁在什么时候改了什么？

重要 mutation 最好记录：

```text
actor
action
timestamp
object_id
before_version
after_version
reason
reviewer
```

例如：

```text
label v1 → v2
reason: rubric boundary corrected
reviewer: adjudicator_7
```

Audit Trail 不是替代 Versioning，而是说明版本变化是谁、为什么做的。

---

# 19.32 Governance Failure 也需要 Taxonomy

常见：

```text
Unknown Source
Broken Lineage
Silent Relabel
Schema Drift
Untracked Judge Change
Untracked Environment Change
Train/Eval Leakage
Missing License
PII Exposure
Irreproducible Run
Orphaned Derived View
Deletion Incomplete
```

这些不是 Model Failure，却会破坏所有后续科学结论。

---

# 19.33 Governance Metrics

治理也应该可观测：

```text
% assets with complete provenance
% labels with version history
% runs with reproducibility manifest
% datasets with immutable manifest / hash
% benchmark cases with contamination status
% derived views rebuildable
% lineage edges resolved
% privacy / license checks complete
% deletion requests fully propagated
```

否则 Governance 容易沦为只写制度、无法验证执行情况。

---

# 19.34 Research Prototype：最低可信实现不需要庞大平台

小团队可以先有：

```text
Stable IDs
Immutable Raw Files
JSON / YAML Manifests
Git Commit
Hashes
Versioned Labels
Build Scripts
Artifact Paths
```

已经能解决大部分科研可追溯问题。

生产规模再升级：

```text
Catalog
RBAC
Central Lineage
Deletion Workflow
Policy Engine
Automated Audit
```

原则是：

> **治理强度随规模 / 风险增加，但 scientific identity / version / lineage 从第一天就值得保留。**

---

# 19.35 Reproducibility Debt

短期不记录：

```text
source
version
config
lineage
```

看似省事。

长期会变成：

```text
结果无法复算
Bug 无法定位
模型受影响范围未知
数据版本差异无法解释
历史结论不可审计
```

这就是 Reproducibility Debt。

它与 technical debt 一样会累积利息。

---

# 19.36 Canonical Case：C1 Failure → Training → Regression Lineage

假设生产出现：

```text
C1 Order / Refund Failure
```

可以形成：

```text
Production Event
prod_9138
↓
Raw Trajectory
traj_9138_raw
↓
Redacted Canonical Trajectory
traj_9138_v1
↓
Failure Annotation v1
↓
Adjudicated Label v2
↓
Synthetic Family
family_order_constraint_07
↓
Preference View
pref_order_v3
↓
Training Mixture
agent_mix_v12
↓
Training Run
run_m19_041
↓
Model
agent_m19
↓
Regression Case
reg_order_1847_v2
```

如果三个月后发现旧 failure label 错了：

```text
Raw Trajectory 不改
↓
新增 Corrected Label
↓
Rebuild Derived Views
↓
Re-score Frozen Evaluation
↓
检查哪些 Training Runs / Models 受影响
```

这就是 Governance 真正发挥作用的地方。

---

# 19.37 常见失败模式

### 失败 1：文件名被当作版本系统

`train_final_final2.jsonl` 不等于治理。

### 失败 2：Raw 与 Derived 混在一起

Judge score 被误当世界事实。

### 失败 3：Label 修正直接覆盖旧值

历史实验无法审计。

### 失败 4：Historical Decision 被 Corrected Label 反向改写

历史行为被篡改。

### 失败 5：Re-score / Re-run / Replay 混用

科学问题变了却不自知。

### 失败 6：Dataset Version、Schema Version、Label Version 全用一个 `v3`

无法知道什么发生了变化。

### 失败 7：Derived View 复制后与 Source 断链

修正无法传播。

### 失败 8：只版本化 Model，不版本化 Tool / Environment / Judge

Agent Run 无法复现。

### 失败 9：Random Split 没有 Family / Workflow Lineage

Train/Eval leakage 被隐藏。

### 失败 10：Publicly Accessible 被当成无限使用许可

Rights governance 失效。

### 失败 11：删除 Raw Row 就宣称完成所有删除

Derivative 仍然存在。

### 失败 12：研究原型因为怕“工程过重”连 Stable ID / Manifest 都不保存

会快速产生 reproducibility debt。

---

# 19.38 从数据岗位视角，这一章实际会做什么？

```text
设计 stable IDs / schema
维护 raw / canonical / derived layers
建立 dataset manifests
做 label / schema / dataset versioning
记录 generator / annotator / judge provenance
维护 family / workflow lineage
构建 train/eval split governance
做 contamination registry
维护 training / evaluation manifests
支持 corrected-label rescoring
做 model ↔ dataset impact tracing
管理 PII / access / retention / deletion
写 Data Card
支持 audit / regression / rollback
```

这类工作可能出现在：

```text
Data Platform
Model Evaluation
Training Data Pipeline
AI Infra
Agent Data
Governance / Compliance
```

而不一定直接叫“Data Governance”。

---

# 19.39 本章关键词

| 术语 | Canonical meaning |
|---|---|
| Identity | 一个数据 / run / model 对象稳定的身份 |
| Provenance | 对象最初从哪里来、由谁 / 什么生成 |
| Lineage | 对象经过 transformation 与 usage 形成的关系图 |
| Raw Evidence | 原始、尽量 immutable 的事实证据 |
| Canonical Record | 对 Raw 的稳定结构化表示 |
| Derived Data | Rule / Model / Human 推导出的 label / score / metadata |
| Dataset View | 从 canonical assets 按 build recipe 派生的用途视图 |
| Dataset Version | 数据资产内容 / 构成版本 |
| Schema Version | 字段结构与语义版本 |
| Label Version | 标签解释版本 |
| Historical Decision | 历史 policy 当时真实做出的决定 |
| Corrected Label | 后续根据更好 evidence 修正后的评价 |
| Re-score | 不改变历史 output，只更新评价 |
| Re-run | 当前系统重新执行产生新 output |
| Replay | 尽量重建历史输入 / runtime 重新执行 |
| Reproducibility Manifest | 描述一个 Run 完整依赖的身份证 |
| Audit Trail | 谁在何时因为什么改变了什么 |

更完整定义见 [`Canonical Glossary`](./00_Glossary_and_Notation.md)。

---

# 19.40 面试 / 自检问题

1. Identity、Provenance、Lineage 有什么区别？
2. Raw / Canonical / Derived 为什么必须分层？
3. Derived Label 为什么不能覆盖 Raw Truth？
4. 为什么 Lineage 更像 DAG 而不是文件链？
5. Dataset / Schema / Label Version 有什么不同？
6. Label Correction 为什么不能覆盖 Historical Decision？
7. Re-score、Re-run、Replay 分别回答什么问题？
8. Dataset View 为什么应该可重建？
9. 一个 Reproducibility Manifest 至少包含什么？
10. Exact / Statistical / Protocol Reproducibility 有什么区别？
11. 为什么 Tool / Environment / Clock 也要版本化？
12. Human Annotation Provenance 为什么包括 UI Version？
13. Judge Score 为什么离开 Evaluator Provenance 没有独立意义？
14. Sampling Policy 为什么需要 provenance？
15. 为什么 Family / Workflow Lineage 对 Split 很重要？
16. Contamination Registry 解决什么问题？
17. 怎样从 Dataset 反查受影响 Model？
18. Data Card 与 Model Card 如何连接？
19. Redaction 与 Pseudonymization 有什么区别？
20. Data Minimization 为什么优先于“全收再脱敏”？
21. 删除一条 Raw Data 为什么是 lineage 问题？
22. 为什么删除文件不等于消除模型参数影响？
23. Gold / Anchor Asset 为什么需要更严格治理？
24. Governance Metrics 可以有哪些？
25. 小研究团队最小需要哪些治理能力？

---

## 19.40.1 通用回答框架：发现一批 Label 错了怎么办？

```text
1. Preserve Raw Evidence
   ↓
2. 新增 Corrected Label Version
   ↓
3. 记录 Reason / Evidence / Reviewer
   ↓
4. 查 Lineage：受影响 Derived Views
   ↓
5. 对 Frozen Historical Outputs 先 Re-score
   ↓
6. 区分是否需要 Fresh Re-run
   ↓
7. 查受影响 Training Runs / Models
   ↓
8. 决定 Rebuild / Retrain / Regression
   ↓
9. 更新 Gold / Guideline / Judge Calibration
```

---

# 19.41 本章最终要形成的认识

把全章压成：

```text
Identity
↓
Provenance
↓
Immutable Raw Evidence
↓
Canonical Representation
↓
Versioned Labels / Metadata
↓
Rebuildable Dataset Views
↓
Training / Evaluation Runs
↓
Models / Reports
↓
Bidirectional Lineage
```

并始终保持：

```text
Raw Facts are preserved
Derived interpretations are versioned
Historical decisions are frozen
Views are rebuildable
Runs are reproducible enough to audit
Rights and privacy travel with the data
```

最终原则：

> **一个成熟的数据系统，不只是知道“有什么数据”，而是知道每个关键 artifact 是谁、从哪来、为什么变、影响了什么，以及怎样在不篡改历史的前提下持续纠错。**

下一章进入：

> [`第 20 章 Data Quality、Filtering、Deduplication 与 Mixture`](./20_Data_Quality_Filtering_Deduplication_and_Mixture.md)

在治理身份和 lineage 已经稳定以后，才继续问：

> **哪些数据应该留下、哪些应该删 / 降权、哪些彼此重复，以及最终模型应该以多大训练曝光看到它们。**