# LLM / Agent Data Practical Artifact Kit

> 状态：`Stable Mother Edition V3.x / Execution Artifacts / Multi-scenario-tested`
>
> 目标：把全书方法论进一步压成一组**可以直接复制、填写、评审和版本化**的项目工件。
>
> 场景压力测试：[`Round 1`](./00_Scenario_Pack_Stress_Test.md) · [`Round 2`](./00_Scenario_Pack_Stress_Test_Round_2.md) · [`Promotion Test`](./00_Scenario_Pack_Promotion_Test.md)
>
> 按需扩展：[`Scenario Pack Candidate Extensions`](./00_Scenario_Pack_Candidate_Extensions.md)
>
> 原则：**没有 Artifact 的流程很难复盘；没有 Version / Evidence / Decision 的 Artifact 很难审计。Artifact Kit 是工件目录，不是要求所有项目 A1→A11 线性填满的流水线。**

---

# 0. 这套 Artifact Kit 负责什么？

与现有资产的区别：

```text
Problem Index
= 去哪里查

Checklist Index
= 别漏什么

Practical Playbook
= 按什么顺序做

Project Starter Pack
= 先从哪个 Entry 进入，Day 0 / Day 1 / First Week 什么时候做什么

Practical Artifact Kit
= 每一步最终应该产出什么可审计对象
```

A1–A11 是**可组合的工件集合**：

```text
A1  Problem Intake
A2  Task / Case / Decision-state Contract
A3  Trajectory / Evidence Bundle
A4  Failure / Mechanism Record
A5  Evaluator Contract
A6  Data Intervention Card          （仅 Data Intervention）
A7  Experiment Card
A8  Decision Memo
A9  Production Handoff
A10 Monitoring Incident / Drift Record
A11 Minimal Lineage Manifest         （贯穿全程）
```

不同项目从不同入口进入：

```text
Failure-led
→ 常见起点 A1 / A2 / A3 / A4

Monitoring-led Incident
→ 常见起点 A10
→ triage 后再进入 A1 / A3 / A4 / A5

Hypothesis-led
→ 常见起点 A1 + A2 / A2-S + A7

Evaluation-led
→ 常见起点 A5

Asset-led / Curation-led
→ 常见起点 A11 source lineage + curation contract
```

它们最终汇合到：

```text
Relevant Contract + Evidence
→ Controlled Change
→ A7 Evaluation
→ A8 Decision
→ Production / Monitoring / Re-entry if needed
```

注意：

```text
A6 不是所有项目必经。
A1 也不是所有项目的强制第一张表。
```

如果项目最终是：

```text
Inference-time / Policy
Tool
Harness / Environment
Evaluator
Product / Task Contract
```

等 intervention，应使用对应的 method / system contract，并直接进入 A7，而不是为了模板整齐把它改名成 Data Intervention。

---

# A1 — Problem Intake Card

适用：需要正式定义问题 / scientific question 的 failure-led、hypothesis-led、evaluation-led、strategy-led 项目；Monitoring-led 可以先从 A10 进入，Asset-led 可以先从 A11 / source asset contract 进入。

```yaml
problem_id: PI-YYYYMMDD-001
owner: <person/team>
created_at: <timestamp>

project_origin: <failure_led|monitoring_led|hypothesis_led|evaluation_led|asset_led|strategy_led>

problem_statement: >
  用一句话描述真实问题 / scientific question，而不是预设解决方案。

user_or_product_impact: >
  这个问题为什么值得解决？研究项目可写 scientific value。

observed_signal:
  metric: <name|null>
  value: <value|null>
  population: <who/what>
  time_window_or_dataset_version: <when/version>

full_population_definition: >
  所有最终 claim 要覆盖的 decision population。

selective_population_layers:
  screened_or_eligible: <definition|null>
  triggered: <definition|null>
  intervened: <definition|null>
  observed_or_scorable: <definition|null>

initial_evidence:
  - <artifact / trace / report / frozen config>

severity_or_priority: <low|medium|high|critical>

suspected_layers:
  - task
  - model
  - tool
  - harness
  - environment
  - evaluator
  - data
  - inference_policy
  - unknown

candidate_intervention_owner_or_type: >
  当前最可能属于哪一层？未确认时写 UNKNOWN。

why_this_might_be_a_data_problem: >
  当前证据是什么？如果没有证据，写 UNKNOWN / NOT YET ESTABLISHED。

cheaper_or_non_data_fixes_checked:
  - <prompt / product / tool / harness / evaluator / policy fix>

decision_deadline_or_milestone: <date>
```

固定边界：

```text
Problem Statement
≠ Proposed Solution

Monitoring Alert
≠ Model Regression

Triggered Population
≠ Full Population

Existing Asset
≠ Validated Training Dataset
```

不要把：

```text
“我们需要再做 20 万条 synthetic data。”
```

或：

```text
“我们要加一个低置信触发器。”
```

写成 problem statement。

---

# A2 — Task / Case / Decision-state Contract

对应：Ch10 / Ch11 / F4；selective reasoning / routing system 同时对应 Ch4 / Ch8 / F8。

普通任务至少：

```yaml
task_id: <stable task id>
case_id: <stable case id>

objective: >
  目标行为。

initial_world_state:
  <structured fields>

agent_visible_state:
  <what the agent may observe initially>

evaluator_only_state:
  <hidden truth / gold predicates>

available_tools:
  - name: <tool>
    schema_version: <version>

permissions:
  - <allowed actions>

constraints:
  - <must satisfy>

forbidden_side_effects:
  - <must never happen>

success_predicates:
  - <machine-checkable if possible>

termination_conditions:
  - <success / safe-stop / timeout / escalation>

runtime:
  model: <version|null>
  prompt: <version|null>
  harness_version: <version|null>
  environment_version: <version|null>
  tool_versions: {}
  seed_protocol: <version|null>
```

## A2-S — Selective / Local Intervention Extension

只在存在：

```text
trigger
router
selector
same-prefix / same-state branch
local repair
adaptive budget
```

时填写：

```yaml
decision_state:
  authoritative_state_ref: <artifact/hash/id>
  authoritative_prefix_ref: <token/text/hash|null>
  intervention_point: <event/state/token span/unit>
  unit_definition: >
    当前 intervention unit 怎样结束？
  lineage_parent: <event/state id|null>

selective_policy:
  trigger_statistic: <name|null>
  trigger_rule: <e.g. statistic < tau>
  trigger_threshold: <value|null>
  comparison_operator: <strict_less_than|less_equal|other|null>

  candidate_generation_policy: >
    如何从 authoritative state / prefix 生成候选。

  same_state_or_prefix_constraint: >
    什么必须保持不变？

  selection_policy: >
    online 怎样选择？

  acceptance_or_continuation_semantics: >
    选择后如何回到 mainline / final answer？

  intervention_budget:
    per_state_cap: <value|null>
    soft_cap: <value|null>
    hard_cap: <value|null>
    global_or_mainline_cap: <value|null>

information_contract:
  online_observable:
    - <feature available at decision time>

  offline_only:
    - <future outcome / oracle / adjudicated label used only offline>

  forbidden_online_information:
    - <hidden/future information that would constitute leakage>
```

固定边界：

```text
Task
≠ Case
≠ Episode
≠ Decision State

Same Task
≠ Same Authoritative State

Offline Label
≠ Online Feature
```

A2-S 的目标不是把所有 research method 写成通用框架，而是保证：

> **别人可以重建“方法到底在什么 state、看到了什么、允许做什么”。**

---

# A3 — Trajectory / Evidence Bundle

对应：Ch12 / F5。

```yaml
episode_id: <id>
task_id: <id>
case_id: <id>

model:
  checkpoint: <version>
  prompt_version: <version>

runtime:
  harness_version: <version|null>
  environment_version: <version|null>
  tool_versions: {}
  seed_or_seed_protocol: <value/version|null>

initial_state_ref: <snapshot / artifact id>

events:
  - event_id: e001
    type: <observation|decision|action|tool_result|state_transition|trigger|candidate|selection>
    parent_event_id: null
    parent_state_id: null
    branch_from_event_id: null
    retry_of_attempt_id: null
    logical_action_id: null
    agent_visible: true
    payload: {}
    timestamp: <optional>

selective_state_evidence:
  authoritative_state_ref: <id|null>
  trigger_value: <value|null>
  trigger_decision: <true|false|null>
  provisional_output_ref: <id|null>
  candidate_refs: []
  selected_candidate_ref: <id|null>

final_state_ref: <artifact id>
final_answer_ref: <artifact id|null>
termination_type: <success|failure|safe_stop|timeout|escalation|eos>

cost:
  tokens_total: <n|null>
  tokens_incremental: <n|null>
  model_generations: <n|null>
  tool_calls: <n|null>
  latency_ms: <n|null>

artifacts:
  - <stdout/stderr/state diff/screenshot/log/token trace/etc>
```

关键：

```text
Decision Intent
≠ Executed Action

Tool Result
≠ Observation

Observation
≠ World State

Final Answer
≠ Full Trajectory Evidence
```

selective system 还要保证：

```text
Trigger Decision
Candidate Lineage
Selected Continuation
```

都能追回 authoritative state。

---

# A4 — Failure / Mechanism Record

对应：Ch13 / Ch14 / F6。

## Failure-led 项目

```yaml
record_id: <id>
episode_id: <id>
record_type: failure

verified_outcome: <success|failure|partial|unresolved>

symptom: >
  最终看到的失败表现。

first_error:
  event_id: <id|null>
  description: >

first_harmful_action:
  event_id: <id|null>
  description: >

last_recoverable_state:
  event_id: <id|null>
  description: >

point_of_no_return:
  event_id: <id|null>
  description: >

immediate_mechanism: >

root_cause: >

failure_layer: <task|reasoning|action|tool|harness|environment|evaluator|other>
failure_owner: <product|model|data|tool|harness|environment|evaluator|external>

severity: <low|medium|high|critical>
detectability: <easy|medium|hard>
recoverability: <yes|no|unknown>
repairability: <yes|no|budget-dependent|unknown>

evidence_refs:
  - <artifact id>

alternative_hypotheses:
  - <candidate explanation not yet ruled out>

recommended_routing:
  - <product|model|data|tool|harness|environment|evaluator>
```

固定边界：

```text
Symptom
≠ Mechanism
≠ Root Cause

Failure Layer
≠ Failure Owner
```

## Hypothesis-led 项目

不需要伪造一个 Root Cause。

可以使用：

```yaml
record_id: <id>
record_type: opportunity_or_mechanism

observable_signal: >

target_property: <risk|recoverability|selectability|other>

mechanism_hypothesis: >

counterfactual_definition: >

oracle_question: >

online_decision_question: >

alternative_hypotheses:
  - <...>

evidence_refs:
  - <artifact>
```

---

# A5 — Evaluator Contract

对应：Ch15 / Ch16 / F7 / F8。

```yaml
evaluator_id: <id>
version: <version>

claim: >
  这个 evaluator 实际要判断什么？

evidence_inputs:
  - <world state / execution / text / trace / test result>

evaluator_type: <verifier|grader|judge|human|hybrid>

output_schema:
  label_space: []
  score_range: <optional>
  abstain_supported: true

priority_rules:
  - <e.g. executable failure overrides style preference>

known_limitations:
  - <coverage / bias / unsupported slice>

gold_or_anchor_set: <id|null>
measurement_bridge_ref: <old-new paired bridge id|null>

validation:
  false_positive_rate: <value|unknown>
  false_negative_rate: <value|unknown>
  high_severity_slice_result: <value|unknown>

version_dependencies:
  prompt: <version|null>
  model: <version|null>
  test_suite: <version|null>
  runtime: <version|null>

information_boundary:
  may_use_online: []
  may_use_offline_only: []
  must_never_feed_online_policy: []
```

必须回答：

```text
What is the claim?
What is the evidence?
Why is this evaluator valid for that claim?
```

Evaluator / rubric / guideline 换版时，还要回答：

```text
旧尺子与新尺子之间有没有 paired bridge？
没有 bridge 时，新旧 score 是否被错误拼成一条 longitudinal curve？
```

固定边界：

```text
Evaluator Output
≠ Ground Truth by definition

Offline Evaluation Evidence
≠ Online Policy Feature

New Evaluator Score
≠ Historically Comparable Score by default
```

---

# A6 — Data Intervention Card

对应：Ch17–21 / F9 / F10。

只在 intervention 真的是 Data 时使用。

```yaml
intervention_id: <id>
intervention_type: data

source_problem_ids:
  - <PI...>

capability_gap: >
  从 failure / mechanism abstraction 得到的能力缺口。

hypothesis: >
  为什么这类 data intervention 可能改善目标能力？

data_operation: <add|remove|replace|reweight|transform>

source_experience:
  - human
  - synthetic
  - rollout
  - production_mined

learning_signal:
  - sft
  - preference
  - reward
  - process
  - recovery
  - verifier

construction_policy: >
  数据如何产生？

verification_policy: >
  如何判断数据本身是否满足 contract？

curation_policy:
  dedup: <rule>
  family_grouping: <rule>
  contamination: <rule>
  routing: <rule>

mixture_policy:
  token_budget: <n>
  exposure_rule: <description>

expected_benefit: >

expected_risks:
  - <regression / overbehavior / bias / cost>
```

关键：

```text
Failure
≠ Training Example

Capability Gap
→ Data Hypothesis
→ Data Intervention
```

如果 intervention 不是 Data：

```text
不要填写假的 A6。
```

改为保存对应：

```text
Method / Policy Contract
Tool / Harness Change Contract
Evaluator Change Contract
Product / Task Contract Change
```

并在 A7 的 `intervention.ref` 指向它。

Asset-led / Curation-led 项目如果只是在把既有 source assets 构造成可信 Dataset View，可以按需使用 `A6-C Curation Contract`，不必伪装成“新增训练数据 intervention”。

---

# A7 — Experiment Card

对应：Ch16 / Ch21 / F8。

这是任何 comparison / intervention 项目的核心工件。

```yaml
experiment_id: <id>
question: >
  这个实验只回答一个主要问题。

baseline:
  model: <version|null>
  policy_or_method: <version/id|null>
  data_policy: <version|null>
  training_recipe: <version|null>
  runtime: <version/id>
  source_artifact: <frozen baseline artifact/id>

intervention:
  type: <data|model|training|inference_policy|tool|harness|environment|evaluator|product>
  ref: <artifact/method/change id>
  data_intervention_id: <id|null>

matched_dimensions:
  - <model checkpoint>
  - <prompt/runtime>
  - <train tokens or inference token budget>
  - <candidate / intervention cap>
  - <training steps / compute if relevant>

population:
  full: <definition + count if known>
  screened: <definition/count|null>
  eligible: <definition/count|null>
  triggered: <definition/count|null>
  intervened: <definition/count|null>
  observed_or_scorable: <definition/count|null>

information_boundary:
  online_observable:
    - <available at decision time>
  offline_only:
    - <oracle/future/adjudicated info for analysis only>
  forbidden_online:
    - <information that would leak future/hidden truth>

primary_eval: <benchmark/protocol id>
transfer_eval: <id|null>
regression_eval: <id|null>

metrics:
  primary: <metric + denominator>
  guardrails:
    - <metric + denominator>
  failure_transition:
    - rescue
    - harmful
    - net
  cost:
    per_triggered_case: <metric|null>
    incremental_intervention: <metric|null>
    average_e2e_full_population: <metric|null>
    worst_case_or_cap: <metric|null>

statistics:
  paired: <true|false>
  seeds_or_repetitions: <n>
  uncertainty_method: <method>
  multiple_comparison_policy: <method|null>

predefined_decision_rule:
  scale_if: >
  revise_if: >
  stop_if: >

claim_scope_template: >
  结果最多支持到哪个 model / population / protocol / budget / evaluator version？
```

A7 的固定边界：

```text
Exploratory
≠ Confirmatory

Full Population
≠ Triggered Population
≠ Intervened Population

Triggered-slice Gain
≠ E2E Gain

Offline Label
≠ Online Feature

Same Task
≠ Same Decision State

Per-trigger Cost
≠ Average E2E Cost
```

每一个数值指标至少能回答：

```text
Numerator 是什么？
Denominator 是什么？
属于哪个 population？
在什么 budget / protocol 下？
```

---

# A8 — Decision Memo

一个实验结束后，不应只有结果表。

```yaml
decision_id: <id>
experiment_id: <id>

result_summary: >
  一句话说明 observed effect。

claim_scope: >
  结论只支持到哪里？

population_results:
  full_population: <value|null>
  triggered_or_key_slice: <value|null>
  intervention_coverage: <value|null>

primary_gain: <value>
transfer_result: <value|null>
regressions:
  - <slice / metric>

cost:
  per_triggered_case: <value|null>
  incremental_intervention: <value|null>
  average_e2e_full_population: <value|null>
  worst_case_or_cap: <value|null>

uncertainty: >

failure_transition:
  rescue: <value|null>
  harmful: <value|null>
  net: <value|null>

information_boundary_audit: <pass|fail|not_applicable>

decision: <scale|maintain|revise|stop|retire>

rationale: >

follow_up:
  - <next action>
```

目标：

> **把“结果是什么”“在哪个 denominator 上成立”和“因此决定什么”分开。**

---

# A9 — Production Handoff Contract

对应：Ch22 / Ch24 / F12。

```yaml
handoff_id: <id>
source_decision_id: <id>

production_objective: >

target_volume: <n>
quality_gate: <policy id>

job_contract:
  sharding: <rule>
  retry_budget: <n>
  idempotency: <rule>
  timeout: <value>

artifact_contract:
  raw_store: <path/system>
  metadata_store: <path/system>
  required_hashes: true

routing:
  pass: <destination>
  review: <destination>
  quarantine: <destination>
  negative: <destination>

cost_budget:
  per_sample_or_intervention: <value>
  total: <value>

release_gate:
  - <condition>

owner:
  production: <team>
  quality: <team>
  downstream: <team>
```

关键：

```text
Research Success
≠ Production Readiness
```

---

# A10 — Monitoring Incident / Drift Record

对应：Ch23 / F13。

Monitoring-led project 可以直接从 A10 开始，不需要先人为制造一张 A1。

```yaml
incident_id: <id>
detected_at: <timestamp>

last_known_good:
  timestamp_or_window: <time/window>
  release_or_model_version: <id|null>
  metric_definition_version: <id|null>

signal:
  metric: <name>
  previous: <value>
  current: <value>
  population_or_slice: <population>

comparison_view:
  raw_overall: <value/change|null>
  fixed_mix: <value/change|null>
  slice_results: []

changed_since_last_good:
  model: <version change|null>
  prompt: <change|null>
  tool: <change|null>
  harness: <change|null>
  environment: <change|null>
  evaluator: <change|null>
  traffic_mix: <change|null>
  business_rule: <change|null>
  trigger_router_selector: <change|null>

frozen_core_result: <value|null>
fresh_failure_result: <value|null>

population_shift:
  full: <change|null>
  triggered_or_routed: <change|null>

suspected_drift:
  - data
  - concept
  - failure
  - capability
  - judge
  - infrastructure
  - routing_or_calibration

root_cause_status: <confirmed|suspected|unresolved>
owner: <team|null>

containment:
  action: <none|rollback|disable_route|freeze_write|other>
  status: <planned|active|complete|not_needed>

immediate_action: >
rollback_condition: >

follow_up_artifacts:
  - <new A1 / case / regression / evaluator bridge / data intervention / tool fix / recalibration>
```

固定原则：

```text
Monitoring Alert
≠ Model Regression

Raw Overall Drift
≠ Fixed-mix Capability Drift

Trigger-rate Drift
≠ Capability Drift by definition
```

---

# A11 — Minimal Lineage Manifest

任何项目即使是研究原型，也建议至少保存：

```yaml
artifact_id: <stable id>
artifact_type: <source_asset|trajectory|dataset|dataset_view|label|model|report|verifier|case|method_contract|experiment>
version: <version>
created_at: <timestamp>

parents:
  - <artifact id>

code_commit: <sha|null>
config_ref: <path/id|null>

content_hash: <hash>
count: <n|null>

producer:
  model: <version|null>
  prompt: <version|null>
  tool: <version|null>
  harness: <version|null>
  environment: <version|null>
  evaluator: <version|null>
  policy_or_selector: <version|null>

population_ref: <ledger/artifact id|null>
information_boundary_ref: <contract id|null>
build_recipe_ref: <id|null>

notes: >
```

它不需要一开始就做成复杂 lineage platform。

最低目标是：

> **能从结论追回输入，也能从输入追到受影响结论。**

Asset-led / Curation-led 项目可以直接从 A11 建立 source truth，再进入 routing / curation / validation。

---

# 1. Artifact 与章节的映射

| Artifact | Canonical Owner |
|---|---|
| A1 Problem Intake | Ch24 / Ch25 |
| A2 Task / Case / Decision-state Contract | Ch10 / Ch11；selective state 关联 Ch4 / Ch8 |
| A3 Trajectory / Evidence | Ch12 |
| A4 Failure / Mechanism Record | Ch13 / Ch14 |
| A5 Evaluator Contract | Ch15 / Ch16 |
| A6 Data Intervention | Ch17–20 |
| A7 Experiment Card | Ch16 / Ch21 |
| A8 Decision Memo | Ch18 / Ch21 / Ch24 |
| A9 Production Handoff | Ch22 / Ch24 |
| A10 Monitoring Incident | Ch23 |
| A11 Lineage Manifest | Ch19 |

---

# 2. Artifact 与 Playbook / Scenario 的映射

## P1 — 一条线上 Agent Failure

```text
A1
→ A2
→ A3
→ A4
→ A5
→ A6 or non-data fix
→ A7
→ A8
```

## P2 — 几十万条 Agent Trajectory / Existing Data Asset

```text
A11 source asset / lineage gate
→ A3 batch evidence view
→ A6-C curation contract if needed
→ A5 verifier / judge contract if scoring is used
→ A7 downstream validation
→ A8
```

如果 batch 里先发现明确 failure mechanism，再按需进入 A4；不要为了流程整齐给所有 trajectory 强制生成 Root Cause。

## P3 — Synthetic Data

```text
A2
→ A5
→ A6
→ A7
→ A8
```

## P4 — Judge Score ↑ / Success 不涨

```text
A5
→ A5-M Measurement Bridge if evaluator version changed
→ A7
→ A8
→ A10 if production
```

## P5 — Oracle Gap 有但 E2E 不涨

```text
A2-S
→ A3
→ A5
→ A7 Population / Information / Cost Ledger
→ A8
```

## P6 — +1.2pt 值不值得继续投

```text
A7
→ A8
→ A9 if SCALE
```

## P7 — 线上 Success Rate 掉了

```text
A10
→ last-known-good / change ledger / raw-vs-fixed-mix triage
→ A3 / A4 only when failure evidence is available
→ correct owner
→ A6 only if true Data Gap
```

## Hypothesis-led Selective Research（如 K17 类）

```text
A1 scientific question
→ A2-S authoritative state / intervention contract
→ A3 branch lineage / evidence
→ A4 opportunity / mechanism record
→ A5 evaluator + information boundary
→ method-specific intervention contract
→ A7 population / information / cost ledger
→ A8 claim-scope decision memo
```

---

# 3. 一个成熟项目的最短“证据包”

最短证据包也应按 Entry 选择，不是机械复制固定八件套。

共同最小核：

```text
Problem / Scientific Question / Incident / Asset Identity
Relevant Contract
Raw Evidence / Lineage
Frozen Evaluator / Protocol when measurement is involved
Controlled Change or Comparison Contract
Decision Memo
```

按需增加：

```text
Failure-led
→ Failure / Mechanism Record

Selective / Adaptive
→ Population Ledger + Information Boundary + Cost Ledger

Evaluator Change
→ Measurement Bridge

Monitoring Incident
→ Last-known-good + Change Ledger + Containment

Asset-led / Curation-led
→ Source Lineage + Build Recipe / Dataset View
```

如果这些都没有，就很容易出现：

```text
只记得最后分数
不知道样本是谁
不知道 triggered 到底占谁
不知道 intervention 看到了什么信息
不知道为什么改
不知道谁判的
不知道到底花了多少成本
不知道新旧 evaluator 是否可比
不知道 dataset view 从哪些 source build 出来
不知道为什么决定继续做
```

---

# 4. 最终原则

```text
Entry Router
决定从哪个工件开始

Playbook
告诉你怎么走

Artifact
证明你真的走过

Population Ledger
证明数字到底在说谁

Information Boundary
证明 online decision 没偷看未来

Measurement Bridge
证明换尺子后哪些历史比较仍成立

Lineage
证明你走的是哪一条路

Decision Memo
证明为什么最终往这个方向走
```

因此一套成熟的 LLM / Agent Data / Reasoning Research 工作方式，不只是：

```text
Analysis
→ Experiment
```

而应该是：

```text
Correct Entry
→ Evidence
→ Contract
→ Artifact
→ Controlled Comparison
→ Decision
→ Lineage
→ Reuse / Re-entry
```

> **知识体系真正进入执行阶段的标志，不是知道更多术语，而是每个重要判断都有一个可以被别人重新检查的项目工件；每个数字都知道自己的 denominator，每个 online decision 都知道自己当时允许看见什么，每次换尺子也知道历史比较还能不能成立。**