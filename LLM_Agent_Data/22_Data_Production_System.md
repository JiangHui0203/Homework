# 第 22 章 Data Production System：把高价值数据稳定地生产出来

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 21 章 Data Experiments`](./21_Data_Experiments_and_Causal_Validation.md)
>
> 关联章节：[`第 11 章 Environment Design`](./11_Environment_Design.md)、[`第 12 章 Agent Trajectory Anatomy`](./12_Agent_Trajectory_Anatomy.md)、[`第 15 章 Grader / Verifier / Judge`](./15_Grader_Verifier_and_LLM_as_a_Judge.md)、[`第 19 章 Governance`](./19_Data_Governance_Lineage_and_Reproducibility.md)、[`第 20 章 Data Curation`](./20_Data_Quality_Filtering_Deduplication_and_Mixture.md)、[`第 23 章 Monitoring 与 Drift`](./23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**Experience Manufacturing Infrastructure 的 canonical chapter。它负责 Production Contract、Data Job、Queue、Worker、Retry / Idempotency、Artifact / Metadata、Quality Gate、Data Router、Dataset Build、Cost Accounting、Backpressure、Environment Pool 与 Experiment Handoff；system-wide Governance 归第 19 章，Curation 归第 20 章，Monitoring / Drift 归第 23 章。**
>
> 本章核心问题：**已经知道什么数据值得做以后，怎样保证它能在规模扩大、任务失败、版本变化、环境异常和人工介入时，仍然被稳定、可恢复、可追踪、可计量地生产出来？**

---

# 22.0 从脚本到 Production System

研究原型可能只是：

```text
for task in tasks:
    output = model.generate(task)
    save(output)
```

进入规模化以后会出现：

```text
任务漏跑 / 重跑
Judge 中途换版本
Environment 没 reset
Write Tool 被重复执行
Human Queue 堵塞
成本无法归因
Raw / Normalized / Scored 文件互相失联
```

因此生产系统要保证：

```text
每个工作单元有 Identity
每个阶段有 State
失败可以局部恢复
原始证据可持久化
成本可归因
结果可重建
```

核心链路：

```text
Production Contract
↓
Job Planning / Sharding
↓
Task Queue
↓
Generator / Environment Workers
↓
Raw Artifact
↓
Normalize / Validate
↓
Verifier / Judge / Human
↓
Quality Gate / Router
↓
Dataset Builder
↓
Training / Eval Handoff
```

---

# 22.1 Production Contract：先定义“这批数据要生产成什么”

一个请求至少应包含：

```text
Target Capability
Source Pool / Seed
Requested Size
Generation Policy
Environment Version
Verifier / Judge Policy
Human Review Policy
Acceptance Criteria
Budget
Output Schema
```

例如：

```yaml
production_request_id: recovery_pref_v3
capability: agent_recovery
source_pool: timeout_failure_v2
requested_pairs: 20000
candidate_n: 4
environment_snapshot: order_env_v5
verifier: final_state_v3
judge: recovery_rubric_v4
max_budget_usd: 12000
output_schema: preference_pair_v3
```

它就是 Data Production Contract。

---

# 22.2 Production Request ≠ Data Job ≠ Artifact ≠ Dataset Record

```text
Production Request
我要生产什么

Data Job
一次可独立调度 / 执行 / 重试 / 计量的工作

Artifact
运行产生的原始证据

Dataset Record
最终进入某种数据视图的记录
```

所以完全可能：

```text
1 Job
→ 4 Candidate Trajectories
→ 2 Preference Pairs
→ 1 SFT Example
→ 1 Regression Case
```

不要假设“一次任务 = 一条训练样本”。

---

# 22.3 Job State Machine

推荐显式状态：

```text
PENDING
→ CLAIMED
→ RUNNING
→ SUCCEEDED
```

异常：

```text
RETRYABLE_FAILED
NON_RETRYABLE_FAILED
PARTIAL
QUARANTINED
WAITING_REVIEW
WAITING_ADJUDICATION
CANCELLED
```

这样“没有 output”不再是一个模糊状态。

---

# 22.4 Sharding：大生产任务必须可局部恢复

不要只有：

```text
generate_100k
```

而应拆成：

```text
Request
├── shard A0
├── shard A1
├── shard B0
└── ...
```

每个 shard 有独立：

```text
job_id
input_manifest
runtime_config
budget
retry_policy
output_manifest
```

局部失败时只重跑局部。

---

# 22.5 Queue：排的是工作，不是训练样本

Queue 需要支持：

```text
Priority
Capability Bucket
Worker Requirement
Deadline
Dependency
Cost Class
```

例如：

```text
P0 blocking regression
P1 experiment / release eval
P2 normal production
P3 background synthetic expansion
```

优先级应该来自业务 / 实验价值，而不是提交顺序。

---

# 22.6 Worker 按职责拆分

### Generator Worker

```text
Prompt Assembly
Inference
Candidate Sampling
Raw Output Capture
```

### Environment Worker

```text
Reset
Snapshot
Tool Execution
State Transition
Final State Capture
```

### Verifier Worker

```text
Executable Check
Final-state Predicate
Constraint / Side-effect Check
```

### Judge Worker

```text
Rubric Scoring
Pairwise Comparison
Failure Grading
```

### Transformation Worker

```text
Normalization
Redaction
Schema Conversion
Pair Construction
```

### Human Review Stage

```text
Review
Expert Check
Adjudication
Gold Annotation
```

这样不同资源可以分别扩缩容和计量。

---

# 22.7 Worker 输入必须可重放

不要依赖进程内隐式状态。

一个 input manifest 应明确：

```text
task_id / case_id
environment_snapshot
model_version
prompt_version
toolset_version
harness_version
seed
```

这样才能在某条 episode 出问题时重建当时条件。

Trajectory-local replay 见第 12 章；完整版本治理见第 19 章。

---

# 22.8 System Retry ≠ Agent Recovery

这是本章最重要的边界。

### Infrastructure Retry

例如：

```text
HTTP 503
GPU preemption
network timeout
```

是生产系统行为。

### Agent Recovery

例如模型看到：

```text
TIMEOUT
```

然后主动：

```text
backoff / switch tool / verify
```

是被评测对象的能力。

如果 Harness 偷偷替模型恢复，再只保存最终 success，就会污染 trajectory 语义。

---

# 22.9 Retry 先分三类失败

```text
Transient Failure
→ may retry

Deterministic Failure
→ fix input / config

Semantic Failure
→ model / task outcome，不应 production retry 掉
```

例如：

```text
503
→ transient

invalid schema
→ deterministic

model chose wrong tool
→ semantic
```

---

# 22.10 Idempotency：Write Action 的生命线

对于：

```text
send_email
charge
cancel_order
delete_file
```

盲目 retry 可能造成重复 side effect。

需要记录：

```text
idempotent: true / false
idempotency_key
transaction_id
```

非幂等动作 retry 前应优先验证第一次是否已生效。

---

# 22.11 Retry Budget 与 DLQ

每个 job 应有限制：

```text
max_attempts
max_runtime
max_cost
```

超过后进入 Dead Letter Queue。

DLQ 不是垃圾桶，而是：

```text
Failure Clustering
→ Root Cause
→ Fix / Requeue / Drop
```

的重要数据源。

---

# 22.12 Partial Success 必须由 Contract 预先定义

例如要 N=8 candidates：

```text
6 succeeded
2 failed
```

是否可接受取决于：

```text
min_candidates
```

而不是事后为了保住产量随意解释。

---

# 22.13 Artifact Store 与 Metadata Store 分工

### Artifact Store

存：

```text
Raw Responses
Trajectory
Candidate Pool
Tool Logs
Environment Snapshot
Judge Evidence Package
```

即大的、尽量 immutable 的原始证据。

### Metadata Store

存：

```text
job status
identity
version reference
lineage reference
cost
quality state
dataset membership
failure code
```

即用于查询、调度和审计的结构化元信息。

---

# 22.14 Normalization ≠ Evaluation

Normalization 只改变表示：

```text
Parse
Canonicalize
Type Cast
Timestamp Normalize
Tool Schema Normalize
```

不能偷偷把：

```text
TIMEOUT
```

压成：

```text
success=false
```

并丢掉错误语义。

---

# 22.15 Structural Validity ≠ Behavioral Correctness

一条错误 trajectory 完全可以：

```text
schema valid
lineage complete
environment valid
```

并且可能是非常高价值的 hard negative。

所以先问：

```text
能否可靠解释？
```

再问：

```text
行为好不好？
```

---

# 22.16 Verifier / Judge Service 的生产接口

Verifier 输出至少应带：

```text
verdict
partial scores
evidence
version
```

Judge 请求至少应指定：

```text
judge_task_type
rubric_version
judge_model_version
evidence_schema_version
```

不要做一个没有语义边界的万能 `score(text)`。

Evaluator 的完整理论见第 15 章。

---

# 22.17 Human Review Queue：把人当稀缺资源调度

优先来源可以是：

```text
High Severity
Judge Disagreement
Low Confidence
New Failure Type
Gold Calibration
Random Audit
```

Generation Queue 与 Human Queue 应分开管理，因为它们的瓶颈完全不同。

---

# 22.18 Quality Gate 不是 Pass / Fail

输出建议：

```text
PASS
DROP
QUARANTINE
REVIEW
DOWNWEIGHT
REGRESSION_ONLY
```

失败 trajectory 可能不适合 SFT，却适合 Preference / Recovery / Regression。

所以：

> **Quality Gate 同时是 Data Routing Gate。**

具体 filtering / dedup / weighting 规则见第 20 章。

---

# 22.19 One Source Artifact → Multiple Derived Views

一条 Raw Failure Trajectory 可以派生：

```text
Preference Pair
Recovery SFT
Regression Case
Synthetic Seed
Failure Benchmark
```

应保持：

```text
one source identity
→ many views
```

而不是复制成五份互相失联的数据。

---

# 22.20 Dataset View = Source Assets + Build Recipe

正式数据集不应该靠：

```text
cat a.jsonl b.jsonl > train.jsonl
```

人工拼接。

它应该由：

```text
Source IDs
Filter Version
Sampling Policy
Mixture Version
Schema Transform
Build Code
```

构建。

这样才能：

```text
rebuild
remove contaminated source
apply corrected label
change mixture
```

而不破坏 raw truth。

---

# 22.21 Split 应沿 Lineage 继承

至少考虑：

```text
family_id
workflow_id
seed_id
environment_id
case_id
```

Same-state sibling candidates 应作为同一个 group。

如果某 seed family 已被分到 hidden eval，它后续 synthetic children 不应偷偷进入 train。

---

# 22.22 Environment Pool：Agent Production 的特殊资源

Episode 通常需要隔离的：

```text
DB
Filesystem
Browser
Calendar
CRM
Code Sandbox
```

基本生命周期：

```text
Acquire
→ Reset / Verify
→ Run Episode
→ Capture State
→ Verify
→ Release
```

Worker crash 后环境应标记 dirty，不能直接复用。

---

# 22.23 Cost Accounting：成本要落到 Job / Sample / Bucket

\[
C_{sample}=C_{gen}+C_{env}+C_{verify}+C_{judge}+C_{human}+C_{infra}
\]

真正有意义的指标：

```text
Cost / Raw Sample
Cost / Verified Sample
Cost / Accepted Sample
Cost / Preference Pair
Cost / Capability Bucket
```

而不是只看一次 API 调用多少钱。

---

# 22.24 Raw Throughput ≠ High-value Yield

例如：

```text
1M raw/day
→ 900k valid
→ 400k verified
→ 250k unique
→ 180k accepted
→ 80k high-value
```

真正的数据产能接近：

```text
80k high-value/day
```

不是 1M。

因此 funnel 每层都应记录：

```text
Count
Pass Rate
Latency
Cost
Failure Reason
```

---

# 22.25 Backpressure：下游堵塞，上游必须减速

如果：

```text
Generation = 1M/day
Human Review = 50k/day
```

继续全速只会造成：

```text
queue explosion
storage explosion
stale data
```

可以：

```text
减慢低优先级 generation
改变 routing
提高自动处理比例
```

Production System 的成熟不是“永远满速”，而是能控制流量。

---

# 22.26 Staleness：排队数据也会过时

Queue item 最好保存：

```text
source_model_version
created_at
freshness_deadline
```

一个月前的 Model v12 hard case，到 Model v16 可能已经不再值得专家标注。

是否继续生产应由新 capability state 决定。

---

# 22.27 Exactly-once 不必神化

现实里更常见：

```text
At-least-once Execution
+
Idempotent Commit
```

Worker 可以重复执行，但相同：

```text
job_id
```

不能重复写入正式 Dataset View。

这是比昂贵追求绝对 exactly-once 更实用的策略。

---

# 22.28 Commit Protocol

推荐：

```text
1. Produce Artifact
2. Persist Artifact
3. Persist Metadata
4. Validate Manifest / Hash
5. Commit Job Success
```

避免：

```text
Job 显示 Success
但 Artifact 根本没落盘
```

这种半提交状态。

---

# 22.29 Budget Guardrail

每个 request / job 可设：

```text
max_tokens
max_gpu_hours
max_api_cost
max_tool_calls
max_human_hours
```

避免 retry / long trajectory / judge cascade 导致成本静默爆炸。

---

# 22.30 Canary / Shadow Production

新：

```text
Generator
Judge
Filter
Schema
```

可以先：

```text
1% → 5% → 20% → 100%
```

或 Shadow 运行，不进入正式 Dataset。

比较：

```text
Yield
Quality
Cost
Failure Modes
```

后再切换。

这不是第 23 章的 Model Drift Monitoring；这里关注的是**生产流水线升级本身的安全发布**。

---

# 22.31 Re-score ≠ Re-generate

如果只是：

```text
judge_v3 → judge_v4
```

Raw Trajectory 没变，通常应该：

```text
reuse raw artifact
→ re-score
```

而不是重新生成行为。

否则会同时改变：

```text
Evaluator
+
Model stochastic output
```

失去可比性。

历史治理规则见第 19 章。

---

# 22.32 Experiment Handoff 不是扔一个 JSONL

Data → Training 至少交付：

```text
Dataset Version
Manifest
Schema
Data Card
Build Recipe
Mixture Recommendation
Quality Report
Known Risks
Expected Capability
Regression Targets
Cost Report
```

训练完成后回流：

```text
training_run_id
model_version
downstream delta
regression
cost
```

使 Production 与 Ch17–21 的闭环连接起来。

---

# 22.33 Research Prototype 与 Production Platform

研究原型可以从：

```text
Stable IDs
JSONL Manifests
Directory Artifacts
SQLite / DuckDB
Simple Queue
Retry Script
Cost CSV
Git Versioning
```

开始。

只要满足：

```text
可追踪
可恢复
可重建
可审计
```

就足够支持大量可信研究。

当出现：

```text
多人并行覆盖
故障恢复困难
成本无法归因
规模人工不可管理
```

再升级基础设施。

> **不要为了产品级工程完整度拖慢仍在探索的科学问题。**

---

# 22.34 Canonical Case C1：生产 Recovery Preference Data

目标：

```text
Tool TIMEOUT 后的 Recovery
```

流程：

```text
Production Contract
↓
从 failure pool 选 recoverable states
↓
冻结 environment snapshot
↓
same-state 生成 alternatives
↓
rollout-to-end
↓
Verifier 检查 success / side effect
↓
构造 informative preference pair
↓
high-risk / disagreement 送 Human
↓
Dataset Build
↓
Ch21 matched-budget experiment
↓
结果回流下一轮 quota
```

整个过程中：

```text
System Retry
```

不能替代：

```text
Agent Recovery
```

这是最关键的实验语义边界。

---

# 22.35 Production System 的核心 KPI

### Reliability

```text
Job Success
Retry
DLQ
Environment Corruption
```

### Throughput / Yield

```text
Raw Generated
Verified
Unique
Accepted
Dataset-ready
```

### Efficiency

```text
Cost / Accepted Sample
GPU Hours
Human Hours
Latency
```

### Quality

```text
Verifier Pass
Audit Pass
Lineage Completeness
```

### Downstream Interface

```text
哪些 Dataset Version 进入哪些 Experiment / Model
```

注意：**Downstream Gain 本身由 Ch21 评估，不由 Production KPI 代替。**

---

# 22.36 常见失败模式

1. 脚本 exit code=0 就算数据成功。
2. 没有 Job Identity，漏跑和重跑无法区分。
3. 所有 Error 都 Retry。
4. System Retry 污染 Agent Recovery。
5. 非幂等 Write Tool 被盲目重试。
6. 只存 Final Dataset，不存 Raw Artifact。
7. Artifact 与 Metadata 失联。
8. Generation 完成就算 Data Ready。
9. Quality Gate 只有 Pass / Fail。
10. Dataset Build 靠人工拼文件。
11. Environment 不 reset，episode 互相污染。
12. 没有 Backpressure，下游积压上游仍全速。
13. Judge 更新后重新生成 trajectory，混淆变量。
14. 没有 Sample-level Cost，无法判断真实 Yield Economics。
15. 过早建设巨大平台，反而拖慢研究。

---

# 22.37 面试 / 自检问题

1. Production Request、Data Job、Artifact、Dataset Record 有什么区别？
2. 为什么 Job 要有显式状态机？
3. 为什么 Queue Item 不等于 Training Sample？
4. Worker 为什么最好按职责拆分？
5. System Retry 与 Agent Recovery 有什么区别？
6. 什么错误可以 Retry，什么不能？
7. 为什么 Idempotency 对 Write Action 特别重要？
8. DLQ 应该如何被使用？
9. Artifact Store 与 Metadata Store 各存什么？
10. Structural Validity 为什么不等于 Behavioral Correctness？
11. Quality Gate 为什么也是 Data Router？
12. Dataset View 为什么应该由 Build Recipe 构造？
13. sibling candidates 为什么应该 group split？
14. Raw Throughput 和 High-value Yield 的区别是什么？
15. Backpressure 解决什么问题？
16. 为什么 Stale Data 也需要重新判断价值？
17. At-least-once + Idempotent Commit 为什么实用？
18. Re-score 与 Re-generate 为什么要区分？
19. Experiment Handoff 为什么不能只给一个 JSONL？
20. 什么时候值得把研究脚本升级成正式平台？

---

# 22.38 本章最终心智模型

```text
Plan
→ Queue
→ Execute
→ Persist
→ Verify
→ Route
→ Build
→ Handoff
```

每一步都必须有：

```text
Identity
State
Version Reference
Evidence
Cost
Lineage Reference
```

一句话：

> **Data Production System 不是批量调用模型，而是一套 Experience Manufacturing System。**

它负责把“已经被证明值得做的数据方案”稳定制造出来；下一章第 23 章再回答：

> **系统上线和持续运行以后，什么时候说明模型、用户、环境或测量系统已经变了？**