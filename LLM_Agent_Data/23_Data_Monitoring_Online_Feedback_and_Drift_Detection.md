# 第 23 章 Data Monitoring、Online Feedback 与 Drift Detection：什么时候说明系统已经变了

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 22 章 Data Production System`](./22_Data_Production_System.md)
>
> 关联章节：[`第 14 章 Agent Failure Taxonomy`](./14_Agent_Failure_Taxonomy.md)、[`第 15 章 Grader、Verifier 与 LLM-as-a-Judge`](./15_Grader_Verifier_and_LLM_as_a_Judge.md)、[`第 16 章 Benchmark Design 与 Evaluation Protocol`](./16_Benchmark_Design_and_Evaluation_Protocol.md)、[`第 17 章 Data Flywheel`](./17_Data_Flywheel_and_Continuous_Improvement.md)、[`第 19 章 Data Governance、Lineage 与 Reproducibility`](./19_Data_Governance_Lineage_and_Reproducibility.md)
>
> 本章目标：建立一套面向 LLM / Agent 数据与线上系统的持续监控框架，理解 Data Drift、Concept Drift、Failure Drift、Capability Drift、Judge Drift、Tool / Environment Drift、Fresh Benchmark、Shadow Evaluation、Online Feedback、Alerting、Rollback Signal 与 Human Escalation 的关系。
>
> 本章核心问题：**模型上线以后，真正困难的不是“有没有监控指标”，而是如何判断：到底是用户分布变了、任务规则变了、工具或环境变了、Judge 变了，还是模型能力真的退化了；以及一旦发现变化，应该刷新数据、更新 benchmark、重校 Judge、回滚模型，还是修 Tool / Harness。**

---

# 23.0 为什么 Drift Detection 是 Data Flywheel 的感知系统？

前面第 17 章建立了：

```text
Production
↓
Logs
↓
Failure Mining
↓
Data
↓
Training
↓
Eval
↓
Deployment
↓
New Production
```

但这个闭环有一个前提：系统必须及时知道“现实已经和旧数据不一样了”。

否则可能出现：

```text
旧 benchmark 仍然很高
旧 regression 全部通过
旧 Judge 仍然给高分

但线上真实用户已经开始失败
```

原因可能来自：

```text
用户任务分布变化
业务规则变化
Tool API 变化
权限变化
环境变化
Judge 标准变化
模型行为变化
新 failure 出现
```

所以 Drift Detection 不是简单的：

```text
metric 下降 → alert
```

而是：

> **持续判断当前系统和原先定义的问题，还是不是同一个问题。**

---

# 23.1 先区分六种 Drift

至少要区分：

```text
1. Data Drift
2. Concept Drift
3. Failure Drift
4. Capability Drift
5. Judge / Evaluator Drift
6. Tool / Harness / Environment Drift
```

这些 drift 的证据、风险和处理动作不同。

---

# 23.2 Data Drift：输入分布变了

训练或历史分布记作：

\[
P_{old}(X)
\]

当前线上分布记作：

\[
P_{new}(X)
\]

如果：

\[
P_{old}(X) \neq P_{new}(X)
\]

就出现 input drift。

例如：

```text
过去：
查询类任务 80%
写操作 20%

现在：
查询类任务 40%
写操作 60%
```

或者：

```text
过去单工具任务为主
现在跨 Calendar + Email + CRM 的多工具任务显著增加
```

因此：

```text
Online Metric Drop
≠
Model Regression
```

第一步要先问：

> Task Mix 变了吗？

---

# 23.3 Agent 系统应该监控哪些输入分布？

不仅是文本长度，还包括：

```text
Task Family
Domain
Language
Conversation Length
Tool Count
Required Steps
Constraint Count
Read / Write Ratio
Permission Level
Environment Type
Risk Level
Difficulty
```

例如平均 prompt length 没变，但：

```text
Multi-tool Ratio
8% → 31%
```

或者：

```text
Constraint Density
1.2 → 3.7
```

就可能显著改变 task success。

---

# 23.4 Concept Drift：同样输入，正确行为的定义变了

Concept Drift 更接近：

\[
P_{old}(Y\mid X)
\neq
P_{new}(Y\mid X)
\]

例如旧规则是：

```text
金额 < 100
可以自动退款
```

后来规则变成：

```text
金额 < 50
才允许自动退款
```

用户仍然说：

```text
“帮我退款。”
```

但正确行为已经变了。

这时旧的：

```text
Training Data
Benchmark
Verifier
Rubric
```

可能一起过时。

所以 Concept Drift 不是单纯“补新数据”，而往往意味着：

> **监督定义本身必须更新。**

---

# 23.5 Policy / Business Rule Drift

Agent 场景中的 Concept Drift 常表现为：

```text
业务规则变化
权限策略变化
安全规则变化
产品交互变化
合规要求变化
```

因此 Task Contract 和关键数据资产最好记录：

```text
policy_version
business_rule_version
permission_version
```

规则升级时应触发：

```text
affected dataset audit
benchmark refresh
verifier refresh
regression refresh
```

---

# 23.6 Failure Drift：失败结构变了

即使总 success rate 接近不变，failure composition 也可能发生很大变化。

例如旧模型：

```text
Tool Selection Failure   30%
Argument Failure         25%
Verification Failure     10%
Recovery Failure         20%
Other                    15%
```

新模型：

```text
Tool Selection Failure   10%
Argument Failure         10%
Verification Failure     30%
Recovery Failure         35%
Other                    15%
```

这说明：

```text
基础 Tool Use 问题减少
↓
更深层 Recovery / Verification 问题暴露
```

所以监控不能只看：

```text
Failure Rate
```

还要看：

```text
Failure Composition
```

Failure Drift 还是 Data Strategy 的直接输入：

```text
Failure Drift
↓
Capability Gap Update
↓
Data Portfolio Rebalance
```

---

# 23.7 Taxonomy 本身也会过时

新模型支持新的能力后，会出现新的 failure：

```text
Parallel Action Conflict
Memory Contamination
Delegation Failure
Stale Long-running State
```

如果旧 taxonomy 没覆盖，不应该硬塞进“Other”后就结束。

建议保留：

```text
UNKNOWN
OTHER
NEEDS_NEW_TAXONOMY
```

并长期监控：

```text
Unknown Failure Rate
```

它升高时，可能说明观测框架本身落后了。

---

# 23.8 Capability Drift：模型本身真的变了

Capability Drift 指在相对稳定的任务和评测条件下，模型能力发生变化。

要证明它，必须尽量冻结：

```text
Task
Environment
Tool Version
Harness
Verifier
Judge
Budget
```

因此第 16 章的 Frozen Core Benchmark 很重要。

没有 stable ruler，线上 metric 的变化很难归因。

---

# 23.9 Stable Ruler + Moving Frontier

线上长期评估最好同时维护：

```text
Frozen Core Benchmark
```

负责：

```text
纵向可比
Regression Detection
Release Gate
```

和：

```text
Fresh Frontier Benchmark
```

负责：

```text
新任务
新 failure
新工具
新业务规则
新用户分布
```

只有 Frozen Core，会出现 benchmark saturation；只有 Fresh Frontier，则无法知道旧能力有没有退化。

所以成熟体系需要：

> **Stable Ruler + Moving Frontier。**

---

# 23.10 Judge Drift：测量工具也会变

如果：

```text
judge_model v3 → v4
judge_prompt v7 → v8
rubric v2 → v3
```

之后：

```text
Pass Rate
82% → 74%
```

并不能直接说模型变差。

可能只是：

```text
Judge 变严格了
```

因此必须版本化：

```text
judge_model_version
judge_prompt_version
rubric_version
evidence_schema_version
```

评价系统自己也必须被监控。

---

# 23.11 Judge Anchor Set

建议长期保留一套：

```text
Judge Anchor Set
```

包括：

```text
Human Gold
Executable Truth
Boundary Cases
Bias Probes
High-severity Cases
```

每次 Judge 升级都做：

```text
Old Judge
vs
New Judge
```

比较：

```text
Agreement
False Positive
False Negative
Bias Gap
Swap Consistency
Abstention
```

这样才能知道变化来自 production quality 还是 measurement instrument。

---

# 23.12 Tool Drift

工具可能在不“下线”的情况下发生语义变化：

```text
API Schema
Parameter Semantics
Return Format
Error Code
Latency
Rate Limit
Permission
Pagination
Default Value
```

因此关键 Tool 最好监控：

```text
Schema Hash
Version
Latency
Error Rate
Permission Failure Rate
Response Shape
Null Rate
Pagination Behavior
```

并用 contract test 验证：

```text
known input
↓
expected structural output
```

如果 contract test 失败，应优先检查 Tool / Adapter，而不是直接归因给模型。

---

# 23.13 Environment Drift 与 Harness Drift

Environment Drift 包括：

```text
网页 DOM 变化
数据库 schema 变化
时区变化
文件权限变化
业务 fixture 更新
```

Harness Drift 包括：

```text
Tool Result 注入格式变化
Context Truncation Policy 变化
Memory Summary 变化
Retry Policy 变化
Stop Condition 变化
Parallelism 变化
```

所以线上性能变化时，至少要分解：

```text
Model
Prompt
Tool
Harness
Environment
Judge
Traffic
```

而不是只问：

> 是不是模型退化了？

---

# 23.14 一个成熟 Monitoring Stack

可以分五层：

```text
L1 Traffic
L2 Runtime
L3 Behavior
L4 Outcome
L5 Drift
```

### Traffic

```text
Request Count
Task Family Mix
Language Mix
Prompt Length
Risk Level
Tool-demand Rate
```

### Runtime

```text
Latency
Token Usage
Tool Calls
API Errors
Timeout
Rate Limit
Environment Failure
```

### Behavior

```text
Tool Selection
Retry Rate
Clarification Rate
Verification Rate
Abstention Rate
Write-action Rate
Termination Type
```

### Outcome

```text
Task Success
Constraint Compliance
Side-effect Rate
Recovery Success
User Correction
Human Override
```

### Drift

```text
Task Mix Shift
Failure Mix Shift
Score Distribution Shift
Unknown Failure Rate
Tool Error Mix Shift
Judge Disagreement Shift
```

---

# 23.15 Outcome Metric 不能脱离 Task Mix

假设：

```text
Week 1 Success = 80%
Week 2 Success = 74%
```

如果 Week 2 的任务显著更难，不能直接解释为系统退化。

所以线上最好同时报告：

```text
Raw Overall Metric
Slice Metrics
Fixed-mix Reweighted Metric
```

假设 slice 为 \(k\)：

\[
S_{obs}=\sum_k p_{new}(k)S_k
\]

而固定参考分布下：

\[
S_{fixed}=\sum_k p_{ref}(k)S_k
\]

Raw Metric 反映真实线上体验；Fixed-mix Metric 更接近模型能力变化。

两者都要保留。

---

# 23.16 Drift Metric 不能只靠单一统计量

可以使用：

```text
Mean / Quantile Shift
PSI
KS-style comparison
Wasserstein Distance
JS Divergence
Category Frequency Shift
Embedding Cluster Shift
Novel Cluster Rate
```

但：

> **统计显著 ≠ 产品重要。**

真正应该结合：

```text
Effect Size
Persistence
Affected Volume
Severity
Downstream Impact
```

而不是看到某个阈值过线就机械告警。

---

# 23.17 Online Feedback：用户行为也是信号

很多任务没有直接 verifier。

这时可以利用：

```text
Explicit Feedback
- rating
- correction
- report

Implicit Feedback
- rephrase
- retry
- undo
- abandon
- escalation
- repeated action
```

但：

```text
User Feedback
≠
Ground Truth
```

用户也可能改变主意或表达不清。

所以它更适合做：

```text
Mining Signal
Audit Priority
Active Learning Signal
```

而不是未经验证直接变成 label。

---

# 23.18 Delayed Feedback

一些真实错误会延迟出现：

```text
执行动作
↓
数小时 / 数天后发现结果不对
```

因此要通过：

```text
episode_id
transaction_id
entity_id
action_id
```

把未来事件关联回原 trajectory。

Online Feedback 是新的 evidence，不是自动生成的 step label；仍需要：

```text
Failure Attribution
First Harmful Action
Last Recoverable State
Credit Assignment
```

---

# 23.19 Shadow Evaluation

新模型可以先对真实线上请求做 shadow run：

```text
Production Model
→ 正式服务

Shadow Model
→ 同样请求
→ 不执行真实 side effects
```

比较：

```text
Tool Choice
Proposed Action
Verifier / Judge
Cost
Latency
Failure Type
```

优点是使用真实流量分布，用户风险较低。

但如果 shadow 不真正执行操作，后续 observation 可能不同，所以它不是完整线上 A/B 的替代。

对于可复制环境，更好的方式是：

```text
Production Request
↓
Clone Environment Snapshot
↓
Candidate Model in Sandbox
↓
Compare Final State
```

---

# 23.20 Canary Release

新模型 / 新 policy 可以：

```text
1%
↓
5%
↓
20%
↓
50%
↓
100%
```

逐档检查：

```text
Task Success
High-severity Failure
Side-effect Rate
Latency
Cost
Escalation
Tool Error
```

高风险指标应该作为 hard guardrail，而不是被 overall improvement 抵消。

---

# 23.21 Rollback Signal

Rollback 不应该只绑定总体 success。

例如：

```text
Overall Success ↑
```

但某类严重 policy violation 也显著上升，仍然可能必须回滚。

所以 release gate 应该包含：

```text
Primary Metric
Guardrail Metrics
High-severity Metrics
Cost / Latency Limits
Infrastructure Health
```

原则是：

```text
Release
if
Primary Gain is acceptable
AND
No Critical Guardrail Violation
```

---

# 23.22 Alerting 与 Human Escalation

Alert 过多会造成 Alert Fatigue。

可以分：

```text
Info
Warning
Critical
```

并结合：

```text
Magnitude
Duration
Affected Volume
Severity
Confidence
```

部分变化可自动识别；新业务意图、新 failure class、新安全边界则往往需要：

```text
Domain Expert
Data Analyst
Researcher
Product Owner
Safety Reviewer
```

介入。

---

# 23.23 Monitoring 也是 Data Acquisition Engine

监控发现某类 failure 上升后，不应该只发告警。

应该进入：

```text
Sampling Queue
↓
Audit
↓
Failure Taxonomy
↓
Data Acquisition
↓
Regression Set
↓
Data Experiment
```

所以 Monitoring 是 Data Flywheel 的入口之一。

---

# 23.24 Fresh Failure Cohort 与 Fresh Benchmark

可以周期性抽取：

```text
New Failures
High Severity
Judge Disagreement
Unknown Taxonomy
High User Correction
High Uncertainty
Novel Tool Paths
```

形成：

```text
Fresh Failure Cohort
```

再分成：

```text
Training Candidates
Dev / Analysis
Held-out Fresh Eval
```

并按 family / workflow 隔离，避免 fresh benchmark 很快又污染训练。

---

# 23.25 Regression Set Growth 与 Retirement

线上确认的关键 failure 应进入 regression。

但 regression 也不能无限增长。

可以分层：

```text
Tier 0 Critical
每次 release 必跑

Tier 1 Core
周期性跑

Tier 2 Historical
低频回归
```

对已经被稳定 system rule 解决、长期不再出现的问题，可以从 hot regression 中退休，但保留 historical archive。

---

# 23.26 Data Freshness Monitoring

训练数据本身也会 stale。

建议记录：

```text
created_at
last_validated_at
source_model_version
source_tool_version
policy_version
freshness_status
```

状态可以是：

```text
Fresh
Aging
Stale
Invalid
```

旧数据不一定要删除，可以：

```text
Keep
Downweight
Archive
Regression-only
Drop
```

关键是重新评估它对当前模型是否仍有学习价值。

---

# 23.27 Training–Serving Skew

训练环境和线上环境经常不同：

```text
Training:
Tool 几乎总成功

Serving:
存在 timeout / rate limit / permission change
```

那么模型可能 offline 很强，online recovery 很弱。

需要持续比较：

```text
Task Complexity
Tool Error Distribution
Observation Noise
Environment Stochasticity
```

训练和 serving 是否一致。

---

# 23.28 Policy-induced Selection Bias

线上日志不是自然独立样本，而是：

> **Policy-conditioned Data。**

例如系统对高风险任务大量 abstain，那么日志中自然很少出现真正执行后的高风险失败。

因此应记录：

```text
Eligible
Triggered
Intervened
Executed
Observed Outcome
```

不能只看最终 executed population。

这和 triggered system 的 denominator discipline 是同一类问题。

---

# 23.29 Coverage Monitoring

允许 abstain / clarify / escalate 的系统必须同时报告：

```text
Coverage
Success@Coverage
Risk@Coverage
Escalation Rate
```

一个只处理最容易 20% 任务、success 95% 的系统，不能直接和处理 90% 流量的系统比较。

所以：

> **Quality 必须和 Coverage 一起看。**

---

# 23.30 Slice Monitoring

总体指标容易藏住局部问题。

应按重要维度切片：

```text
Capability
Domain
Risk
Language
Task Family
Tool
Environment
Failure Type
```

但不能无限组合造成 slice explosion。

优先保留：

```text
Business-critical Slices
Known-risk Slices
Failure-driven Slices
Automatically Discovered Slices
```

---

# 23.31 Monitoring ≠ Root Cause Analysis

Monitoring 只能先告诉我们：

```text
发生变化了
```

但：

```text
Success ↓
```

可能来自：

```text
Traffic harder
Model worse
Tool failing
Judge stricter
Policy changed
Environment changed
```

所以还需要：

```text
Frozen Benchmark
Version Comparison
Matched Slice
Controlled Replay
Shadow
A/B
```

做因果诊断。

---

# 23.32 Dashboard 要分事实层和判断层

事实层：

```text
request count
latency
tool errors
final state
user correction
```

判断层：

```text
judge score
failure type
risk label
capability label
```

判断层可能随着 Judge / Taxonomy / Rubric 改变，所以不能和 raw fact 混为一谈。

监控指标本身也要记录：

```text
metric_definition_version
query_version
judge_version
taxonomy_version
```

否则同一条趋势线中可能混着不同定义。

---

# 23.33 Incident → Data Asset

一次重要线上异常建议保留：

```text
incident_id
start_time
end_time
affected_versions
affected_slices
symptom
root_cause
severity
user_impact
data_impact
mitigation
rollback
followup_data_action
regression_case_ids
```

然后转化成：

```text
Incident
↓
Minimal Reproduction
↓
Regression Case
↓
Synthetic Variants
↓
Training Candidate
↓
Release Gate
```

这样事故不会只留下一篇 postmortem，而会变成长期数据资产。

---

# 23.34 Trigger / Router / Selector 也会 Drift

如果线上系统有：

```text
trigger
router
fallback
selector
```

必须分别监控：

```text
Eligible Rate
Trigger Rate
Intervention Rate
Rescue Rate
Harmful Rate
Net Gain
Cost
```

例如固定 threshold 原来触发 20%，模型升级后变成 70%，说明 score distribution 已经变了。

即使阈值数值不变，也可能不再对应同一种风险语义。

---

# 23.35 Score Calibration Drift

一个 score 原本：

```text
0.8 ≈ 高成功概率
```

之后可能不再成立。

所以用于：

```text
abstain
trigger
route
```

的 score 需要定期检查：

```text
bin-wise outcome
reliability curve
calibration error
threshold coverage
```

Ranking 仍然好，不代表 fixed threshold 仍然有效。

---

# 23.36 Frozen Threshold vs Recalibrated Threshold

在研究里，两种比较回答不同问题。

如果问：

> 同一个固定规则迁移到新模型是否仍工作？

则：

```text
freeze threshold
```

如果问：

> 每个模型在自己重新校准后能达到什么最优 trade-off？

则：

```text
recalibrate threshold
```

两者不能混在同一个结论里。

---

# 23.37 一个通用 Drift Response Playbook

发现异常后，可以按顺序：

```text
Step 1
确认 metric definition 是否变化

Step 2
检查 infrastructure / tool / environment health

Step 3
检查 traffic / task mix drift

Step 4
检查 Judge / verifier version

Step 5
在 frozen benchmark 上复测 capability

Step 6
做 failure composition / slice analysis

Step 7
抽 fresh cohort 做 objective / human audit

Step 8
确定 root cause

Step 9
选择 action
```

Action 可能是：

```text
Rollback Model
Fix Tool
Fix Harness
Refresh Data
Refresh Benchmark
Update Judge
Update Taxonomy
Update Policy
Do Nothing / Monitor
```

重要原则：

> **不要把所有 drift 都翻译成“再训练一次模型”。**

---

# 23.38 Drift Response Matrix

| Drift | 典型证据 | 优先动作 |
|---|---|---|
| Data Drift | Task mix changed | Reweight eval / refresh data |
| Concept Drift | Business rule changed | Update label / verifier / benchmark |
| Failure Drift | Failure composition changed | Rebalance data portfolio |
| Capability Drift | Frozen benchmark regresses | Model / training investigation |
| Judge Drift | Anchor agreement changes | Recalibrate evaluator |
| Tool Drift | Contract test changes | Tool / adapter fix |
| Harness Drift | Context / retry behavior changes | Runtime fix / rollback |
| Environment Drift | State / UI / schema changes | Environment refresh / benchmark update |

---

# 23.39 Monitoring 与 Data Experiment 的接口

发现某个 drift 后，不应该直接大规模造数据。

更合理的是：

```text
Drift Signal
↓
Fresh Cohort
↓
Root Cause
↓
Candidate Data Intervention
↓
Small Pilot
↓
Matched Data Experiment
↓
Scale / Stop
```

这样把第 23 章接回第 21 章。

---

# 23.40 Control Loop Stability

如果自动飞轮过度敏感：

```text
某 failure ↑
→ 大量增产该类数据
→ failure ↓
→ 立即停产
→ failure 又 ↑
```

就会出现 oscillation。

可以使用：

```text
smoothing
minimum allocation
cooldown
hysteresis
slow-changing portfolio weights
```

例如：

```text
> 5.5% 才增加 allocation
< 4.5% 才取消 allocation
```

避免在阈值附近反复开关。

---

# 23.41 常见失败模式

1. 只看总体 Success，局部高风险问题被平均掉。
2. 指标下降就归因给模型，忽略 Traffic / Tool / Judge / Environment。
3. 把 User Feedback 直接当 Ground Truth。
4. Judge 换版后仍画成一条连续趋势线。
5. 只有老 regression，没有 fresh benchmark。
6. 只有 fresh benchmark，没有 stable ruler。
7. Tool / Harness 变化不做版本记录。
8. Alert 太多导致 Alert Fatigue。
9. 发现 drift 后直接大规模训练，没有 root cause 和 pilot。
10. 所有 failure 都进入训练，Infrastructure 问题被误标为模型负例。
11. 忽略 Coverage，只报高 success。
12. 混用 eligible / triggered / completed denominator。
13. 不监控 unknown failure，taxonomy 逐渐失效。
14. 不监控 score calibration，threshold policy 静默失效。
15. 自动 flywheel 反应过快，数据 portfolio 反复震荡。

---

# 23.42 在大模型 / Agent 数据岗位里，这一章对应什么工作？

包括：

```text
设计线上质量指标
建设 failure dashboard
定义 data / concept / judge drift
做 fresh failure sampling
维护 regression set
构造 fresh benchmark
做 judge anchor calibration
分析 tool / environment drift
建设 shadow evaluation
设计 canary release gate
追踪 user correction / escalation
做 offline-online gap analysis
把 drift 转成下一轮 data quota
```

当岗位描述写：

```text
“搭建数据闭环”
“持续发现模型 bad case”
“做在线质量监控”
“推动数据迭代”
```

背后通常就是这一整套能力。

---

# 23.43 关键词速查

| 关键词 | 核心含义 |
|---|---|
| Data Drift | 输入分布变化 |
| Concept Drift | 正确映射 / 规则变化 |
| Failure Drift | 失败组成变化 |
| Capability Drift | 模型真实能力变化 |
| Judge Drift | evaluator 行为变化 |
| Tool Drift | 工具契约变化 |
| Environment Drift | 世界状态 / UI / schema 变化 |
| Harness Drift | 运行编排变化 |
| Shadow Eval | 真实流量上的影子评估 |
| Canary | 小流量逐步发布 |
| Rollback Gate | 触发回滚的规则 |
| Fresh Benchmark | 新近分布上的评测 |
| Regression Set | 历史关键失败回归集 |
| Coverage | 系统实际处理任务的比例 |
| Calibration Drift | score 与 outcome 的映射变化 |
| Train–Serve Skew | 训练与线上分布不一致 |

---

# 23.44 自测 / 面试题

1. Data Drift 和 Concept Drift 有什么区别？
2. 为什么线上 success rate 下降不一定说明模型退化？
3. Failure Drift 为什么比总体 failure rate 更有信息？
4. 什么是 Judge Drift？如何检测？
5. Tool Drift 和 Harness Drift 分别是什么？
6. 为什么需要 Stable Ruler + Moving Frontier？
7. User Feedback 为什么不能直接当 ground truth？
8. 什么是 delayed feedback？
9. Shadow Eval 和线上 A/B 有什么区别？
10. Canary release 应该看哪些 guardrail？
11. 为什么 coverage 必须和 success 一起报告？
12. 什么是 policy-induced selection bias？
13. 为什么 triggered system 要保留 eligible / triggered / intervened denominator？
14. Score calibration 为什么会 drift？
15. Frozen threshold 和 recalibrated threshold 回答的科学问题有什么不同？
16. 什么是 Train–Serve Skew？
17. Fresh Failure Cohort 应该怎么进入数据飞轮？
18. Regression Set 为什么也需要 retirement？
19. 为什么 Monitoring 不等于 Root Cause Analysis？
20. 如何把一次线上 incident 变成长期数据资产？
21. 为什么 automated flywheel 可能 oscillate？
22. Hysteresis 在数据策略中有什么作用？
23. Monitoring Dashboard 为什么要区分 facts 和 derived labels？
24. Offline–Online Gap 可以反映哪些系统问题？
25. 如何设计一套完整的 Drift Response Playbook？

---

# 23.45 一个通用 Monitoring / Drift 框架

如果从零搭一套 LLM / Agent 线上监控，可以按：

```text
Step 1
定义稳定事实日志

Step 2
版本化 Model / Prompt / Tool / Harness / Environment / Judge

Step 3
定义 Traffic / Runtime / Behavior / Outcome 指标

Step 4
建立 capability / risk / failure slices

Step 5
保留 Frozen Core Benchmark

Step 6
构造 Fresh Failure Cohort

Step 7
建立 Judge Anchor Set

Step 8
监控 task mix / failure mix / tool error / score calibration

Step 9
建设 Shadow + Canary

Step 10
定义 Release / Rollback Guardrails

Step 11
建立 Drift Response Playbook

Step 12
把确认后的 drift 转成 data / benchmark / system action
```

最终目标不是：

```text
“有一个漂亮 dashboard”
```

而是：

> **系统能够持续判断：现在真实世界最重要的问题是什么，以及下一步该改数据、模型、评测还是基础设施。**

---

# 23.46 本章最终心智模型

整章可以压缩成：

```text
Observe
↓
Detect Shift
↓
Separate Traffic / Measurement / Capability / Infrastructure
↓
Diagnose Root Cause
↓
Prioritize by Risk and Value
↓
Refresh Data / Benchmark / Judge / System
↓
Verify Fix
↓
Feed Back into Flywheel
```

对应七个关键问题：

```text
Data Drift
→ 输入变了吗？

Concept Drift
→ 正确行为的定义变了吗？

Failure Drift
→ 失败结构变了吗？

Capability Drift
→ 模型本身变了吗？

Judge Drift
→ 测量工具变了吗？

Infrastructure Drift
→ Tool / Harness / Environment 变了吗？

Data Value Drift
→ 过去值得学的东西现在还值得学吗？
```

真正成熟的数据系统，不只是会生产数据，还必须知道：

> **什么时候旧数据已经不再够用。**

---

# 下一章：第 24 章 End-to-End LLM / Agent Data Operating Model

前面已经分别建立了：

```text
Data Object
Learning Signal
Human Data
Synthetic Data
Reasoning Data
Agent Task / Environment / Trajectory
Credit Assignment
Failure Taxonomy
Verifier / Judge
Benchmark
Flywheel
Strategy
Governance
Quality / Mixture
Experiment
Production
Monitoring
```

第 24 章会把这些部分重新合并成一套完整的：

> **LLM / Agent Data Operating Model。**

也就是回答：一个团队到底如何组织这些能力，数据、研究、训练、评测、产品和工程之间如何交接；一条 failure 从线上回来以后经过哪些角色；哪些能力应该平台化，哪些应该留在研究侧快速迭代；一个季度的数据 roadmap 又该怎么制定。