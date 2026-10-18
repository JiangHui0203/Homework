# LLM / Agent Data Practical Artifact Kit

> 状态：`Stable Mother Edition V3.x / Execution Artifacts`
>
> 目标：把全书方法论进一步压成一组**可以直接复制、填写、评审和版本化**的项目工件。
>
> 与现有资产的区别：
>
> ```text
> Problem Index
> = 去哪里查
>
> Checklist Index
> = 别漏什么
>
> Practical Playbook
> = 按什么顺序做
>
> Practical Artifact Kit
> = 每一步最终应该产出什么可审计对象
> ```
>
> 原则：**没有 Artifact 的流程很难复盘；没有 Version / Evidence / Decision 的 Artifact 很难审计。**

---

# 0. 最小 Artifact Chain

一个完整项目至少应该形成：

```text
A1 Problem Intake
↓
A2 Task / Case Contract
↓
A3 Trajectory / Evidence Bundle
↓
A4 Failure Record
↓
A5 Evaluator Contract
↓
A6 Data Intervention Card
↓
A7 Experiment Card
↓
A8 Decision Memo
↓
A9 Production Handoff
↓
A10 Monitoring Incident / Drift Record
↺
```

它们分别回答：

```text
为什么做？
到底在测什么？
真实发生了什么？
为什么失败？
凭什么判？
准备改什么数据？
怎么证明有效？
最后决定什么？
怎样规模执行？
现实后来又发生了什么？
```

---

# A1 — Problem Intake Card

适用：项目立项、线上 bad case、benchmark regression、数据策略需求。

```yaml
problem_id: PI-YYYYMMDD-001
owner: <person/team>
created_at: <timestamp>

problem_statement: >
  用一句话描述真实问题，而不是预设解决方案。

user_or_product_impact: >
  这个问题为什么值得解决？

observed_signal:
  metric: <name>
  value: <value>
  population: <who/what>
  time_window: <when>

initial_evidence:
  - <artifact / trace / report>

severity: <low|medium|high|critical>

suspected_layers:
  - task
  - model
  - tool
  - harness
  - environment
  - evaluator
  - data

why_this_might_be_a_data_problem: >
  当前证据是什么？如果没有证据，写 UNKNOWN。

cheaper_non_data_fixes_checked:
  - <prompt / product / tool / harness / policy fix>

decision_deadline: <date>
```

最低要求：

```text
Problem Statement
≠ Proposed Solution
```

不要把：

```text
“我们需要再做 20 万条 synthetic data”
```

写成 problem statement。

---

# A2 — Task / Case Contract

对应：Ch10 / Ch11 / F4。

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
  harness_version: <version>
  environment_version: <version>
  tool_versions: {}
  seed: <optional>
```

固定边界：

```text
Task
≠ Case
≠ Episode
```

---

# A3 — Trajectory / Evidence Bundle

对应：Ch12 / F5。

建议保留：

```yaml
episode_id: <id>
task_id: <id>
case_id: <id>

model:
  checkpoint: <version>
  prompt_version: <version>

runtime:
  harness_version: <version>
  environment_version: <version>

initial_state_ref: <snapshot / artifact id>

events:
  - event_id: e001
    type: <observation|decision|action|tool_result|state_transition>
    parent_event_id: null
    agent_visible: true
    payload: {}
    timestamp: <optional>

final_state_ref: <artifact id>
termination_type: <success|failure|safe_stop|timeout|escalation>

cost:
  tokens: <n>
  tool_calls: <n>
  latency_ms: <n>

artifacts:
  - <stdout/stderr/state diff/screenshot/log/etc>
```

关键：

```text
Decision Intent
≠ Executed Action

Tool Result
≠ Observation

Observation
≠ World State
```

---

# A4 — Failure Record

对应：Ch13 / Ch14 / F6。

```yaml
failure_id: <id>
episode_id: <id>

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
  直接导致 failure 的机制。

root_cause: >
  最值得修复、能解释一类 failure 的上游原因。

failure_layer: <task|reasoning|action|tool|harness|environment|evaluator|other>
failure_owner: <product|model|data|tool|harness|environment|evaluator|external>

severity: <low|medium|high|critical>
detectability: <easy|medium|hard>
recoverability: <yes|no|unknown>
repairability: <yes|no|budget-dependent|unknown>

evidence_refs:
  - <artifact id>

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

validation:
  false_positive_rate: <value|unknown>
  false_negative_rate: <value|unknown>
  high_severity_slice_result: <value|unknown>

version_dependencies:
  prompt: <version|null>
  model: <version|null>
  test_suite: <version|null>
  runtime: <version|null>
```

必须回答：

```text
What is the claim?
What is the evidence?
Why is this evaluator valid for that claim?
```

---

# A6 — Data Intervention Card

对应：Ch17–21 / F9 / F10。

```yaml
intervention_id: <id>
source_problem_ids:
  - <PI...>

capability_gap: >
  从 failure abstraction 得到的能力缺口。

hypothesis: >
  为什么这类 data intervention 可能改善目标能力？

intervention_type: <add|remove|replace|reweight|transform>

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

---

# A7 — Experiment Card

对应：Ch16 / Ch21 / F8。

```yaml
experiment_id: <id>
question: >
  这个实验只回答一个主要问题。

baseline:
  model: <version>
  data_policy: <version>
  training_recipe: <version>

intervention:
  data_intervention_id: <id>

matched_dimensions:
  - train_tokens
  - compute
  - training_steps

population:
  full: <definition>
  eligible: <definition|null>
  triggered: <definition|null>

primary_eval: <benchmark/protocol id>
transfer_eval: <id|null>
regression_eval: <id|null>

metrics:
  primary: <metric>
  guardrails: []
  cost: []

statistics:
  paired: <true|false>
  seeds: <n>
  uncertainty_method: <method>
  multiple_comparison_policy: <method|null>

predefined_decision_rule:
  scale_if: >
  revise_if: >
  stop_if: >
```

必须保证：

```text
Exploratory
≠ Confirmatory
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

target_gain: <value>
transfer_result: <value|null>
regressions:
  - <slice / metric>

cost:
  training: <value>
  inference: <value>
  production: <value>

uncertainty: >

failure_transition:
  rescue: <value|null>
  harmful: <value|null>
  net: <value|null>

decision: <scale|maintain|revise|stop|retire>

rationale: >

follow_up:
  - <next action>
```

目标：

> **把“结果是什么”和“因此我们决定什么”分开。**

---

# A9 — Production Handoff Contract

对应：Ch22 / F12。

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
  per_sample: <value>
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

```yaml
incident_id: <id>
detected_at: <timestamp>

signal:
  metric: <name>
  previous: <value>
  current: <value>
  slice: <population>

changed_since_last_good:
  model: <version change|null>
  prompt: <change|null>
  tool: <change|null>
  harness: <change|null>
  environment: <change|null>
  evaluator: <change|null>
  traffic_mix: <change|null>
  business_rule: <change|null>

frozen_core_result: <value|null>
fresh_failure_result: <value|null>

suspected_drift:
  - data
  - concept
  - failure
  - capability
  - judge
  - infrastructure

root_cause_status: <confirmed|suspected|unresolved>
owner: <team|null>

immediate_action: >
rollback_condition: >
follow_up_artifacts:
  - <new case / regression / data intervention / tool fix>
```

固定原则：

```text
Monitoring Alert
≠ Model Regression
```

---

# A11 — Minimal Lineage Manifest

任何项目即使是研究原型，也建议至少保存：

```yaml
artifact_id: <stable id>
artifact_type: <trajectory|dataset|label|model|report|verifier|case>
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

notes: >
```

它不需要一开始就做成复杂 lineage platform。

最低目标是：

> **能从结论追回输入，也能从输入追到受影响结论。**

---

# 1. Artifact 与章节的映射

| Artifact | Canonical Owner |
|---|---|
| A1 Problem Intake | Ch24 / Ch25 |
| A2 Task / Case Contract | Ch10 / Ch11 |
| A3 Trajectory / Evidence | Ch12 |
| A4 Failure Record | Ch13 / Ch14 |
| A5 Evaluator Contract | Ch15 / Ch16 |
| A6 Data Intervention | Ch17–20 |
| A7 Experiment Card | Ch21 |
| A8 Decision Memo | Ch18 / Ch21 / Ch24 |
| A9 Production Handoff | Ch22 / Ch24 |
| A10 Monitoring Incident | Ch23 |
| A11 Lineage Manifest | Ch19 |

---

# 2. Artifact 与 Playbook 的映射

## P1 — 一条线上 Agent Failure

```text
A1
→ A2
→ A3
→ A4
→ A6 or non-data fix
→ A7
→ A8
```

## P2 — 几十万条 Agent Trajectory

```text
A3
→ A4 batch view
→ A6
→ A7
→ A8
```

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
→ A7
→ A8
→ A10 if production
```

## P5 — Oracle Gap 有但 E2E 不涨

```text
A2 / A3
→ A5
→ A7
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
→ A3 / A4
→ correct owner
→ A6 only if true Data Gap
```

---

# 3. 一个成熟项目的最短“证据包”

如果项目时间非常紧，至少保留：

```text
Problem Intake
Task / Case Contract
Raw Trajectory / Evidence
Failure Record
Frozen Eval Protocol
Data / System Intervention
Experiment Result
Decision Memo
```

如果这八样都没有，就很容易出现：

```text
只记得最后分数
不知道样本是谁
不知道为什么改
不知道谁判的
不知道到底花了多少成本
不知道为什么决定继续做
```

---

# 4. 最终原则

```text
Playbook
告诉你怎么走

Artifact
证明你真的走过

Lineage
证明你走的是哪一条路

Decision Memo
证明为什么最终往这个方向走
```

因此一套成熟的 LLM / Agent Data 工作方式，不只是：

```text
Analysis
→ Experiment
```

而应该是：

```text
Evidence
→ Artifact
→ Decision
→ Lineage
→ Reuse
```

> **知识体系真正进入执行阶段的标志，不是知道更多术语，而是每个重要判断都有一个可以被别人重新检查的项目工件。**
