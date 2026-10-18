# LLM / Agent Data Scenario Pack Candidate Extensions

> 状态：`Candidate / Not Canonical / Pending Further Stress Test`
>
> 来源：[`Scenario Pack Stress Test — Round 2`](./00_Scenario_Pack_Stress_Test_Round_2.md)
>
> 目的：把第二轮异质压力测试暴露出的结构先做成**可填写、可试用、但尚未 canonize** 的扩展。它们不新增 canonical concept，不替代 `Project Starter Pack` 或 `Practical Artifact Kit`。

---

# 0. 为什么先做 Candidate，而不是直接改母本？

第一轮 K17 压力测试暴露的是：

```text
Decision State
Population Ledger
Information Boundary
Cost Ledger
```

这些在 selective system 中属于明显的 correctness requirement，因此已经回写母本。

第二轮新增的是：

```text
Entry Router
Production Incident Contract
Evaluator Measurement Bridge
Curation Contract
```

它们跨域价值很高，但还应该再经过至少一轮真实项目验证，避免把：

```text
“几个案例里很好用”
```

过早升级成：

```text
“所有项目都必须这么写”
```

所以本文件遵循：

> **Use first, canonize later.**

---

# E1 — Entry Router

Artifact Chain 不再默认：

```text
A1 → A2 → A3 → ... → A10
```

而先按项目 origin 选择入口。

## E1.1 Failure-led

```text
Observed failure / regression
↓
A1 Problem Intake
↓
A2 Contract
↓
A3 Evidence
↓
A4 Failure Record
↓
owner / intervention routing
```

## E1.2 Monitoring-led Incident

```text
Alert / metric shift
↓
A10 Incident
↓
last-known-good + change ledger
↓
triage
├─ infrastructure / evaluator / traffic / product fix
└─ confirmed new problem → A1 / A3 / A4 / A5
```

## E1.3 Hypothesis-led Research

```text
Scientific hypothesis
↓
A1 Question / Scope
↓
A2 or A2-S
↓
Controlled Comparison
↓
A7
↓
A8
```

不要求伪造一个：

```text
Root Cause
```

作为项目起点。

## E1.4 Evaluation-led

```text
Measurement / benchmark concern
↓
A5 Evaluator Contract
↓
E3 Measurement Bridge if version change
↓
A7 comparison
↓
A8 decision
```

## E1.5 Asset-led / Curation-led

```text
Existing source assets
↓
A11 Lineage / Source Identity
↓
E4 Curation Contract
↓
Dataset View
↓
A7 downstream validation
↓
A8
```

## E1.6 Stable convergence point

入口不同，但最终都应该回答：

```text
What changed / what is proposed?
What evidence supports it?
What comparison isolates the effect?
What decision follows?
```

---

# E2 — A10-I Production Incident Extension

仅用于：

```text
production metric shift
release regression
high-severity online incident
```

建议在现有 A10 上按需增加：

```yaml
incident_context:
  alert_id: <id>
  detected_at: <timestamp>
  incident_window: <start/end>
  last_known_good_window: <start/end>
  last_known_good_snapshot_ref: <artifact/release id>

release_context:
  current_release: <id>
  previous_release: <id|null>
  rollout_stage: <shadow|canary|partial|full|null>
  rollback_available: <true|false>
  rollback_status: <not_started|prepared|executed|not_applicable>

change_ledger:
  model: <from/to|null>
  prompt: <from/to|null>
  tool: <from/to|null>
  harness: <from/to|null>
  environment: <from/to|null>
  evaluator: <from/to|null>
  retry_policy: <from/to|null>
  traffic_mix: <summary|null>
  business_rule: <from/to|null>
  other_release_config: []

metric_views:
  raw_overall:
    previous: <value>
    current: <value>

  slices:
    - slice: <name>
      previous: <value>
      current: <value>

  fixed_mix:
    reference_distribution: <id|null>
    previous: <value|null>
    current: <value|null>

  frozen_core:
    protocol: <id|null>
    previous: <value|null>
    current: <value|null>

  fresh_frontier:
    cohort: <id|null>
    result: <value|null>

containment_decision:
  severity: <level>
  blast_radius: <estimate>
  critical_guardrail_breached: <true|false>
  immediate_action: <hold|rollback|route|degrade|continue_observation>
  rationale: >

root_cause_status:
  state: <unresolved|suspected|confirmed>
  leading_hypotheses: []
  ruled_out: []
```

## E2 Boundary

```text
Alert
≠ Diagnosis

Rollback
≠ Root-cause Proof

Raw Overall Change
≠ Capability Drift
```

核心：

> **先保住 change evidence 和 containment decision，再做 attribution。**

---

# E3 — A5-M Evaluator Measurement Bridge

适用于：

```text
Judge model upgrade
Judge prompt change
Rubric change
Verifier suite change
Evidence package change
Human annotation guideline change
```

建议结构：

```yaml
measurement_bridge_id: <id>

old_evaluator:
  id: <id>
  version: <version>

new_evaluator:
  id: <id>
  version: <version>

change_type:
  - model
  - prompt
  - rubric
  - verifier_suite
  - evidence_schema
  - annotation_guideline

anchor_set:
  id: <id>
  composition:
    human_gold: <n|null>
    executable_truth: <n|null>
    boundary_cases: <n|null>
    high_severity: <n|null>
    bias_probes: <n|null>

paired_results:
  old_score_distribution: <ref>
  new_score_distribution: <ref>
  correlation: <value|null>
  agreement: <value|null>
  decision_flip_rate: <value|null>

error_analysis:
  old_false_positive: <value|null>
  new_false_positive: <value|null>
  old_false_negative: <value|null>
  new_false_negative: <value|null>
  abstention_delta: <value|null>
  slice_deltas: []

bridge_policy:
  historical_curve_comparable: <true|false|conditional>
  score_mapping: <method|null>
  recalibration_required: <true|false>
  rebaseline_required: <true|false>

historical_integrity:
  preserve_original_judgment: true
  preserve_original_decision: true
  rescore_as_new_view: true
```

## E3 Boundary

```text
New Evaluator Score
≠ Old Evaluator Score on the same scale by default

Re-score
≠ Historical Label Mutation

Evaluator Upgrade
≠ Capability Improvement
```

如果 evaluator 参与数据过滤，还额外记录：

```yaml
dataset_impact:
  affected_build_recipes: []
  affected_acceptance_policy: []
  requires_new_dataset_view: <true|false>
```

---

# E4 — A6-C Curation Contract

这不是替代 A6 Data Intervention，而是给：

```text
已有大规模 source asset
→ 构建 dataset view
```

的项目一个候选 contract。

```yaml
curation_contract_id: <id>

source_assets:
  - artifact_id: <id>
    source_type: <production|synthetic|human|rollout|benchmark|other>
    count: <n>
    lineage_manifest: <A11/id>

source_integrity_requirements:
  episode_identity: <required|optional>
  case_identity: <required|optional>
  runtime_version: <required|optional>
  environment_version: <required|optional>
  final_state_evidence: <required|optional>
  evaluator_version: <required|optional>
  family_or_seed_lineage: <required|optional>
  privacy_rights: <required|optional>

validity_checks:
  - <schema / tool / lineage / privacy / contamination checks>

quality_dimensions:
  - correctness
  - relevance
  - completeness
  - verifiability
  - novelty
  - decision_diversity
  - safety
  - provenance_quality

routing_policy:
  pass: <rule>
  drop: <rule>
  quarantine: <rule>
  review: <rule>
  downweight: <rule>
  regression_only: <rule>
  negative_view: <rule>
  recovery_view: <rule>

dedup_policy:
  exact: <rule>
  near_text: <rule>
  semantic: <rule>
  decision_level: <signature/rule>
  family_level: <grouping/rule>

split_policy:
  grouping_keys:
    - case_id
    - family_id
    - seed_id
    - workflow_id
    - environment_id

mixture_and_exposure:
  sample_share: <policy>
  token_share: <policy>
  bucket_weights: <policy>
  loss_weight: <policy|null>

yield_funnel:
  raw: <n>
  structurally_valid: <n>
  evidence_complete: <n>
  verified_or_scored: <n>
  unique_enough: <n>
  accepted_or_routed: <n>
  high_value: <n>

dataset_view:
  view_id: <id>
  build_recipe_version: <version>
  source_refs: []
  filter_version: <version>
  evaluator_version: <version|null>
  schema_transform_version: <version>
```

## E4 Boundary

```text
Raw Asset
≠ Dataset View

PASS / DROP
≠ Complete Routing Policy

Semantic Similarity
≠ Decision Equivalence

Raw Count
≠ High-value Yield

Dataset Size
≠ Training Exposure

Intrinsic Quality
≠ Downstream Learning Value
```

因此 E4 最终仍应进入：

```text
A7 matched-budget downstream validation
```

而不是因为 curation KPI 变漂亮就直接宣称训练收益。

---

# 5. Candidate Promotion Gate

E1–E4 只有在继续压力测试后才考虑并入 Mother Artifacts。

建议 promotion criteria：

```text
[ ] 至少跨 2 个额外真实项目仍有用
[ ] 没有与现有 A1–A11 发生 ownership 冲突
[ ] 字段能删除至少一种常见 ambiguity / audit failure
[ ] 不要求不相关项目填写大量 N/A
[ ] 能用 optional extension，而不是强迫主模板膨胀
[ ] 能被一个外部读者独立填写
```

如果某扩展只适合单一场景：

```text
保持 scenario-specific
```

不要 canonize。

---

# 6. Final Principle

```text
Canonical Core
= 所有成熟项目都需要的约束

Candidate Extension
= 某类项目反复需要，但尚未证明跨域稳定
```

最终原则：

> **模板成熟的标志不是字段越来越多，而是核心越来越稳定、扩展越来越有条件。**
