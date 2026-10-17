# 第 23 章 Data Monitoring、Online Feedback 与 Drift Detection：什么时候说明系统已经变了

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 22 章 Data Production System`](./22_Data_Production_System.md)
>
> 关联章节：[`第 14 章 Agent Failure Taxonomy`](./14_Agent_Failure_Taxonomy.md)、[`第 15 章 Grader / Verifier / Judge`](./15_Grader_Verifier_and_LLM_as_a_Judge.md)、[`第 16 章 Benchmark Design`](./16_Benchmark_Design_and_Evaluation_Protocol.md)、[`第 17 章 Data Flywheel`](./17_Data_Flywheel_and_Continuous_Improvement.md)、[`第 21 章 Data Experiments`](./21_Data_Experiments_and_Causal_Validation.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> 本章定位：**Monitoring / Online Feedback / Drift Detection 的 canonical chapter。它负责 Data / Concept / Failure / Capability / Judge / Tool-Harness-Environment Drift、Coverage、Calibration Drift、Trigger / Router / Selector Drift、Shadow / Canary / Rollback、Fresh Failure Cohort 与 Drift Response Playbook；Benchmark 定义归第 16 章，Flywheel 编排归第 17 章。**
>
> 本章核心问题：**线上指标变了以后，怎样判断到底是用户分布、任务规则、失败结构、测量工具、基础设施还是模型能力发生了变化，并把这个变化转成正确的下一步行动？**

---

# 23.0 Monitoring 是 Sensing，不是 Diagnosis

看到：

```text
Success
80% → 74%
```

只能说明：

```text
系统观测发生了变化
```

不能直接说明：

```text
模型退化了
```

因为可能同时来自：

```text
Traffic harder
Business rule changed
Judge changed
Tool changed
Harness changed
Environment changed
Model changed
```

所以 Monitoring 的第一职责是：

> **发现变化、定位变化发生在哪一层，并触发后续诊断。**

完整 Root Cause / Failure Diagnosis 仍由第 14 章负责。

---

# 23.1 六类 Drift 必须拆开

| Drift | 核心问题 | 常见例子 |
|---|---|---|
| Data Drift | 输入分布变了吗？ | multi-tool task 占比上升 |
| Concept Drift | 正确行为定义变了吗？ | 业务退款规则改变 |
| Failure Drift | 失败结构变了吗？ | Tool Selection ↓，Recovery ↑ |
| Capability Drift | 模型真实能力变了吗？ | frozen benchmark regression |
| Judge Drift | 测量工具变了吗？ | rubric / judge model 换版 |
| Infrastructure Drift | Tool / Harness / Environment 变了吗？ | API schema / context policy 改变 |

同一个总体指标变化，处理动作可能完全不同。

---

# 23.2 Monitoring Stack：五层一起看

```text
L1 Traffic
L2 Runtime
L3 Behavior
L4 Outcome
L5 Drift
```

## Traffic

```text
Task Family
Domain
Language
Prompt Length
Constraint Count
Tool-demand Rate
Risk Level
```

## Runtime

```text
Latency
Tokens
Tool Calls
Timeout
Rate Limit
Environment Error
```

## Behavior

```text
Tool Selection
Retry
Clarification
Verification
Abstention
Write-action Rate
Termination Type
```

## Outcome

```text
Task Success
Constraint Compliance
Side-effect Rate
Recovery Success
Human Override
```

## Drift

```text
Task Mix Shift
Failure Mix Shift
Unknown Failure Rate
Score Distribution Shift
Judge Disagreement Shift
Tool Error Mix Shift
```

这样才能区分“流量变了”和“模型做法变了”。

---

# 23.3 Raw Metric、Slice Metric、Fixed-mix Metric

只看：

```text
Overall Success
```

很危险。

建议同时保留：

```text
Raw Overall Metric
Slice Metrics
Fixed-mix Metric
```

若 slice 为 \(k\)：

\[
S_{obs}=\sum_k p_{new}(k)S_k
\]

反映真实线上体验。

固定参考分布：

\[
S_{fixed}=\sum_k p_{ref}(k)S_k
\]

更接近“任务组合不变时系统自身表现是否变化”。

二者回答不同问题，都应该保留。

---

# 23.4 Data Drift：输入分布变了

需要监控的不是只有文本长度，还包括：

```text
Task Family
Tool Count
Required Steps
Constraint Density
Read / Write Ratio
Permission Level
Environment Type
Difficulty
Risk
```

例如：

```text
Multi-tool Ratio
8% → 31%
```

即使 prompt length 几乎没变，也可能显著压低总体 success。

因此：

> **Online Metric Drop ≠ Model Regression。**

第一步永远先看 population mix。

---

# 23.5 Concept Drift：监督定义本身变了

例如旧业务规则：

```text
amount < 100
→ auto refund allowed
```

新规则：

```text
amount < 50
→ auto refund allowed
```

用户请求没有变化，但正确行为变了。

这意味着可能同时需要更新：

```text
Task Contract
Training Labels
Verifier
Benchmark
Regression
```

所以 Concept Drift 不是简单“补点新数据”，而是：

> **旧监督语义可能已经失效。**

---

# 23.6 Failure Drift：能力边界移动了

旧模型：

```text
Tool Selection 30%
Argument 25%
Verification 10%
Recovery 20%
```

新模型：

```text
Tool Selection 10%
Argument 10%
Verification 30%
Recovery 35%
```

总体 failure rate 可能变化不大，但系统真正瓶颈已经移动。

这说明：

```text
基础能力得到修复
→ 更深层 failure 暴露
```

因此 Failure Composition 本身就是下一轮 Data Strategy 的重要输入。

---

# 23.7 Failure Taxonomy 也会 Drift

新能力上线后可能出现过去不存在的 failure：

```text
Memory Contamination
Parallel Action Conflict
Delegation Failure
Stale Long-running State
```

所以 taxonomy 应保留：

```text
UNKNOWN
OTHER
NEEDS_NEW_TAXONOMY
```

并监控：

```text
Unknown Failure Rate
```

它持续上升，可能不是模型突然坏了，而是**诊断框架落后了**。

---

# 23.8 Capability Drift：要靠 Stable Ruler 证明

若怀疑模型能力本身退化，需要尽量冻结：

```text
Task Cases
Environment
Tool Version
Harness
Evaluator
Budget
```

再比较模型。

因此第 16 章的 Frozen Core Benchmark 是 capability monitoring 的“尺子”。

没有稳定 measurement object，就很难把线上变化归因给模型本身。

---

# 23.9 Stable Ruler + Moving Frontier

长期系统需要两种评测资产：

```text
Frozen Core Benchmark
→ longitudinal comparability
→ regression gate
```

和：

```text
Fresh Frontier Benchmark
→ new tasks
→ new failures
→ new tools / rules / distributions
```

一句话：

> **Regression 保护过去，Frontier 探索现在。**

Benchmark 的完整设计原则见第 16 章；本章只负责如何在持续监控中使用它们。

---

# 23.10 Judge Drift：尺子也会变

只要：

```text
judge model
judge prompt
rubric
evidence package
```

变化，历史分数就可能失去直接可比性。

因此应维护 Judge Anchor Set：

```text
Human Gold
Executable Truth
Boundary Cases
Bias Probes
High-severity Cases
```

每次 Judge 升级比较：

```text
Agreement
False Positive
False Negative
Bias Gap
Swap Consistency
Abstention
```

不要把 evaluator 变化误报成模型变化。

---

# 23.11 Tool / Harness / Environment Drift

### Tool Drift

```text
Schema
Parameter semantics
Return format
Error code
Permission
Pagination
Default behavior
```

### Harness Drift

```text
Context injection
Truncation
Memory summary
Retry policy
Stop rule
Parallelism
```

### Environment Drift

```text
DB schema
DOM
clock / timezone
permission state
fixtures
```

因此线上变化至少要能分解：

```text
Model
Prompt
Tool
Harness
Environment
Judge
Traffic
```

而不是只归因 Model。

---

# 23.12 Tool Contract Test

关键工具最好维护：

```text
known input
→ expected structural output
```

并监控：

```text
schema hash
latency
error rate
permission failure
null rate
pagination behavior
```

如果 contract test 先坏了，优先修 Tool / Adapter，而不是做训练数据。

---

# 23.13 Online Feedback 是 Signal，不是自动 Label

显式：

```text
rating
correction
report
```

隐式：

```text
retry
rephrase
undo
abandon
escalation
```

都很有价值，但只能先说明：

```text
这里值得看
```

不能直接说明：

```text
模型一定错了
```

正确链路是：

```text
Feedback
→ Mining
→ Audit
→ Attribution
→ Label
```

---

# 23.14 Delayed Feedback：未来事件要能关联回旧 Trajectory

一些错误数小时甚至数天后才暴露。

因此建议用：

```text
episode_id
transaction_id
entity_id
action_id
```

把未来事件关联回历史执行。

Future Feedback 是新增 Evidence；如何做 First Harmful / Credit Assignment 仍回到第 13 章。

---

# 23.15 Coverage 必须和 Quality 一起看

允许：

```text
abstain
clarify
escalate
```

的系统如果只报 success，会严重误导。

至少同时报告：

```text
Coverage
Success@Coverage
Risk@Coverage
Escalation Rate
```

一个只处理最容易 20% case 的 95% success，不能直接和处理 90% case 的 90% success 比较。

---

# 23.16 Policy-conditioned Population：Eligible / Triggered / Executed 分母必须保留

对于 selective system：

```text
Eligible
↓
Triggered
↓
Intervened
↓
Executed
↓
Observed Outcome
```

这些 population 不能混用。

否则 policy 改变后，观测到的 failure distribution 也会跟着变化，造成 Selection Bias。

这与第 16 章的 Denominator Discipline 是同一条统计纪律。

---

# 23.17 Trigger / Router / Selector 也会 Drift

固定 threshold 没改，并不代表 operating point 没变。

例如：

```text
Trigger Rate
20% → 70%
```

说明 score distribution 或 calibration 已经变化。

因此要同时监控：

```text
Score Distribution
Calibration
Trigger Rate
Coverage
Conditional Outcome
Cost
```

---

# 23.18 Calibration Drift：Ranking 还行，不代表 Threshold 还行

原来：

```text
score = 0.8
≈ 高成功概率
```

以后可能不再成立。

所以需要定期检查：

```text
bin-wise outcome
reliability curve
threshold coverage
calibration error
```

尤其对：

```text
abstain
trigger
route
```

这类 threshold policy 很重要。

---

# 23.19 Frozen Threshold 与 Recalibrated Threshold 回答不同问题

### Frozen Threshold

问：

> 同一规则能否直接迁移到新模型 / 新分布？

### Recalibrated Threshold

问：

> 每个模型重新校准后能达到什么最优 trade-off？

两者不能写成同一个结论。

---

# 23.20 Shadow Evaluation

新模型先看真实请求，但不执行真实 side effect：

```text
Production Model
→ 正式执行

Shadow Model
→ 同请求
→ 不改变真实世界
```

若环境可复制，更强的是：

```text
Clone Environment Snapshot
↓
Candidate Model in Sandbox
↓
Final State Verification
```

Shadow 更贴真实流量，但不能自动替代真正线上因果评估。

---

# 23.21 Canary 与 Rollback Guardrail

```text
1% → 5% → 20% → 50% → 100%
```

每一档同时看：

```text
Primary Metric
High-severity Failure
Side-effect
Latency
Cost
Escalation
Infrastructure Health
```

Release 条件应类似：

```text
Primary Gain acceptable
AND
No Critical Guardrail Violation
```

Overall gain 不能抵消 critical regression。

---

# 23.22 Alerting 与 Human Escalation

Alert 可以分：

```text
Info
Warning
Critical
```

并综合：

```text
Magnitude
Duration
Affected Volume
Severity
Confidence
```

真正的新业务意图、新 failure class、新安全边界通常需要 Human / Domain / Product 介入，而不是只依赖自动告警。

---

# 23.23 Fresh Failure Cohort：监控如何进入 Data Flywheel

周期性从线上抽取：

```text
New Failures
High Severity
Judge Disagreement
Unknown Taxonomy
High User Correction
Novel Tool Paths
```

形成 Fresh Failure Cohort。

再分：

```text
Training Candidate
Dev / Analysis
Held-out Fresh Eval
```

并按 family / workflow 隔离。

这就是本章与第 17、21 章的接口。

---

# 23.24 Incident → Long-term Data Asset

重要事故建议保留：

```text
incident_id
versions
affected slices
symptom
root cause
severity
impact
mitigation
rollback
followup action
regression case IDs
```

然后：

```text
Incident
→ Minimal Reproduction
→ Regression Case
→ Synthetic Variants
→ Training Candidate
→ Release Gate
```

让一次事故变成长期防回归资产。

---

# 23.25 Monitoring ≠ Root Cause Analysis

Monitoring 发现：

```text
“变化了”
```

Diagnosis 才判断：

```text
“为什么变”
```

常用后续手段：

```text
Frozen Benchmark
Version Comparison
Matched Slice
Controlled Replay
Shadow
A/B
Human Audit
```

不要让 dashboard 上的一条折线承担因果解释。

---

# 23.26 Fact Layer 与 Judgment Layer 分开

### Facts

```text
request count
latency
tool error
state diff
user correction
```

### Judgments

```text
judge score
failure type
risk label
capability label
```

后者会随着：

```text
Judge
Rubric
Taxonomy
```

改变。

因此 metric 也应该有：

```text
metric_definition_version
query_version
judge_version
taxonomy_version
```

否则一条趋势线里可能混着不同语义。

---

# 23.27 Drift Response Playbook

发现异常后按顺序：

```text
1. Metric definition changed?
2. Tool / Environment / Infra healthy?
3. Traffic mix changed?
4. Judge / Verifier changed?
5. Frozen benchmark regressed?
6. Failure composition changed?
7. Fresh cohort audit
8. Root cause
9. Choose intervention
```

可能动作：

```text
Rollback Model
Fix Tool
Fix Harness
Refresh Data
Refresh Benchmark
Update Judge
Update Taxonomy
Update Policy
Do Nothing / Continue Monitoring
```

核心原则：

> **不要把所有 drift 都翻译成“再训练一次”。**

---

# 23.28 Drift Response Matrix

| Drift | 典型证据 | 优先动作 |
|---|---|---|
| Data Drift | Task mix changed | Reweight eval / refresh data |
| Concept Drift | Rule changed | Update labels / verifier / benchmark |
| Failure Drift | Failure mix changed | Rebalance data portfolio |
| Capability Drift | Frozen benchmark regresses | Model / training investigation |
| Judge Drift | Anchor agreement changed | Recalibrate evaluator |
| Tool Drift | Contract test changed | Tool / adapter fix |
| Harness Drift | Context / retry changed | Runtime fix / rollback |
| Environment Drift | State / schema changed | Environment / benchmark refresh |

---

# 23.29 Control-loop Stability：飞轮不能过度敏感

如果：

```text
Failure ↑
→ 大量增产该类数据
→ Failure ↓
→ 立即停产
→ Failure 又 ↑
```

会产生 oscillation。

可用：

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

避免阈值附近反复开关。

这是 Monitoring 章非常独有的一层：**监控系统本身也是控制系统。**

---

# 23.30 Canonical Case C1：订单 Agent 的 Drift Diagnosis

观察：

```text
Success 88% → 82%
```

不能直接补训练数据。

依次查：

```text
1. Traffic
shipped-order request 占比是否上升？

2. Tool
get_order 返回 schema 是否变化？

3. Judge
success rubric 是否换版？

4. Frozen Core
同一批订单 case 上模型是否退化？

5. Failure Mix
是 precondition failure、grounding failure 还是 tool error 增长？
```

若结果是：

```text
Tool schema unchanged
Judge unchanged
Traffic mix similar
Frozen Core regressed
Observation Grounding Failure ↑
```

才更有证据把问题送进：

```text
Capability Drift
→ Fresh Cohort
→ Data Experiment
```

如果实际是：

```text
Tool pagination default changed
```

就应该修 Tool / Adapter，而不是训练模型。

---

# 23.31 常见失败模式

1. Overall metric 一降就归因模型。
2. 不看 Task Mix / Fixed-mix metric。
3. User Feedback 直接当 Ground Truth。
4. Judge 换版后仍画成连续趋势。
5. 只有 old regression，没有 fresh frontier。
6. 只有 frontier，没有 stable ruler。
7. Tool / Harness / Environment 变化不版本化。
8. 只看 Failure Rate，不看 Failure Composition。
9. Unknown Failure 长期塞进 Other。
10. Coverage 变化但只报 success。
11. Eligible / Triggered / Executed denominator 混用。
12. Ranking 还好就假设 threshold calibration 没变。
13. 发现 drift 直接大规模训练，没有 fresh cohort / pilot。
14. Alert 过多导致 Alert Fatigue。
15. 自动闭环反应过快，portfolio 震荡。

---

# 23.32 从数据岗位视角，本章实际在做什么？

典型工作：

```text
设计线上质量指标
做 task / failure / judge / tool drift dashboard
维护 Judge Anchor
构建 Fresh Failure Cohort
维护 Stable Core + Fresh Frontier
监控 coverage / trigger / calibration
建设 shadow / canary / rollback gate
分析 delayed feedback
把 incident 变成 regression asset
把确认后的 drift 路由到 Data / Model / Tool / Harness / Product
```

真正专业的 Monitoring 不是“有 dashboard”，而是：

> **系统能区分哪一层发生了变化，并选择正确 intervention。**

---

# 23.33 面试 / 自检问题

1. Monitoring 与 Diagnosis 有什么区别？
2. Data / Concept / Failure / Capability Drift 分别是什么？
3. 为什么线上 success 下降不自动等于模型退化？
4. Raw Metric 与 Fixed-mix Metric 分别回答什么？
5. Failure Drift 为什么能反映 capability frontier 移动？
6. Unknown Failure Rate 为什么值得监控？
7. Judge Drift 怎样检测？
8. Tool / Harness / Environment Drift 怎么区分？
9. Online Feedback 为什么只能先当 Signal？
10. Coverage 为什么必须和 Success 一起报？
11. Eligible / Triggered / Executed 为什么要分开？
12. Calibration Drift 会怎样让固定 threshold 失效？
13. Frozen Threshold 与 Recalibrated Threshold 回答什么不同问题？
14. Shadow / Canary / Rollback 各自解决什么？
15. Fresh Failure Cohort 如何进入 Data Flywheel？
16. Monitoring 为什么不能自己承担 Root Cause Analysis？
17. Fact Layer 与 Judgment Layer 为什么要分开？
18. Drift Response Playbook 的顺序是什么？
19. 为什么所有 drift 都不能直接转成训练？
20. Hysteresis 为什么能避免自动 flywheel 震荡？

---

# 23.34 本章最终心智模型

```text
Observe
↓
Detect Shift
↓
Separate
Traffic / Measurement / Capability / Infrastructure
↓
Diagnose
↓
Choose Intervention
↓
Verify Fix
↓
Feed Back into Flywheel
```

六个核心问题：

```text
Data Drift
输入变了吗？

Concept Drift
正确行为定义变了吗？

Failure Drift
失败结构变了吗？

Capability Drift
模型本身变了吗？

Judge Drift
尺子变了吗？

Infrastructure Drift
Tool / Harness / Environment 变了吗？
```

真正成熟的数据系统不仅会生产数据，还知道：

> **什么时候旧数据、旧 benchmark、旧 Judge 和旧 failure taxonomy 已经不再代表现实。**

下一章第 24 章会把前面所有能力放回组织层：

> **当一个真实问题进来以后，团队里的 Product、Research、Data、Eval、Training、Tool / Harness、Platform 各自应该负责什么，谁拥有最终决策权？**