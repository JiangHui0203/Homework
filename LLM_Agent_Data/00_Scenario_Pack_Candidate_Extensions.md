# LLM / Agent Data Scenario Pack Extensions Registry

> 状态：`Mixed Status Registry / V3.x Compatible Extensions`
>
> 历史文件名保留：`00_Scenario_Pack_Candidate_Extensions.md`，避免已有链接失效；当前内容已经不再表示“所有 E1–E5 都是 Candidate”。
>
> 来源：[`Scenario Pack Stress Test — Round 2`](./00_Scenario_Pack_Stress_Test_Round_2.md) · [`Promotion Test`](./00_Scenario_Pack_Promotion_Test.md)
>
> 目的：维护 Scenario Stress Test 暴露出的 extension lineage、当前治理状态与可填写结构。它们不新增第二套 canonical Artifact ID，也不替代 `Project Starter Pack` 或 `Practical Artifact Kit`。

当前状态：

```text
E1 Entry Router
→ PROMOTED CORE PRINCIPLE
→ authoritative usage lives in Project Starter Pack

E2 A10-I Production Incident Extension
→ KEEP OPTIONAL / scenario-specific

E3 A5-M Evaluator Measurement Bridge
→ PROMOTED OPTIONAL

E4 A6-C Curation Contract
→ PROMOTED OPTIONAL

E5 A5-H Human Annotation / Gold Contract
→ KEEP CANDIDATE
```

固定边界：

```text
E-number
= extension lineage / promotion-test identifier
≠ new canonical Artifact ID

A10-I / A5-M / A6-C / A5-H
= extension naming
≠ A12 / A13 / new mandatory artifact sequence
```

模板语义：`<...>` 表示待填 placeholder / allowed shape；枚举项表示可选集合，不代表所有项都已发生。`null / [] / UNKNOWN / UNRESOLVED` 都是合法状态。只有挂接真实 artifact / trace / config / run / source asset 后，填写值才成为项目记录。

---

# 0. 从 Candidate 到 Mixed-status Registry

最初创建本文件时，第二轮压力测试刚暴露：

```text
Entry Router
Production Incident Contract
Evaluator Measurement Bridge
Curation Contract
```

当时合理策略是：

> **Use first, canonize later.**

随后 Promotion Test 又用：

```text
Human Gold / Annotation Refresh
Synthetic Data Production at Scale
```

继续验证，状态已经发生分化：

```text
E1
→ 跨场景稳定到足以进入 Core routing principle

E2
→ 对 production incident 有明确价值
→ 但仍是 scenario-specific optional extension

E3 / E4
→ 跨场景稳定
→ 但只对相关 project type 启用
→ Promoted Optional

E5
→ 有明确缺口与候选结构
→ 仍缺真实 annotation / expert-labeling workflow 验证
→ Keep Candidate
```

因此当前治理原则不是：

```text
所有 extension 都等待 canonize
```

而是：

```text
Core principle
Optional extension
Candidate extension
```

三种状态分开维护。

---

# E1 — Entry Router

**Current status：`PROMOTED CORE PRINCIPLE`**

E1 的当前 authoritative usage 已进入：

- [`Project Starter Pack`](./00_Project_Starter_Pack.md)
- [`Practical Use Map`](./00_Practical_Use_Map.md)
- [`Practical Artifact Kit`](./00_Practical_Artifact_Kit.md)

本节只保留 extension lineage 与最小语义，不作为第二份 routing 真源。

当前五入口固定为：

```text
Failure-led
Monitoring-led
Hypothesis-led
Evaluation-led
Asset-led / Curation-led
```

稳定汇合：

```text
Relevant Contract + Evidence
→ Controlled Change
→ Evaluation
→ Decision
→ Monitoring / Re-entry
```

固定边界：

```text
Project Origin
≠ Workflow Stage
≠ Decision Stage

Artifact Catalog
≠ A1 → A11 mandatory chain
```

如果需要当前完整 routing，回到 `Project Starter Pack`，不要从本节复制一份并行 Entry Router。

---

# E2 — A10-I Production Incident Extension

**Current status：`KEEP OPTIONAL / scenario-specific`**

仅用于：

```text
production metric shift
release regression
high-severity online incident
```

它扩展 A10，而不是取代 A10，也不是所有 Monitoring-led 项目的强制表单。

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
    previous: <value|null>
    current: <value|null>

  slices:
    - slice: <name>
      previous: <value|null>
      current: <value|null>

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
  blast_radius: <estimate|null>
  critical_guardrail_breached: <true|false|unknown>
  immediate_action: <hold|rollback|route|degrade|continue_observation|other>
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

如果普通 A10 已足以记录当前 incident，不为了“用了高级模板”而强制加载 A10-I。

---

# E3 — A5-M Evaluator Measurement Bridge

**Current status：`PROMOTED OPTIONAL`**

适用于 evaluator / measurement semantics 实际发生版本变化，例如：

```text
Judge model upgrade
Judge prompt change
Rubric change
Verifier suite change
Evidence package change
Human annotation guideline change
```

它是 A5 的条件式扩展；**没有 measurement change 时不加载**。

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
  - <one or more of: model|prompt|rubric|verifier_suite|evidence_schema|annotation_guideline>

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

上述 `historical_integrity` 三项是当前治理约束，不是某次项目已经执行完成的 measurement result。

## E3 Boundary

```text
New Evaluator Score
≠ Old Evaluator Score on the same scale by default

Re-score
≠ Historical Label / Decision Mutation

Evaluator Upgrade
≠ Capability Improvement
```

如果 evaluator 参与数据过滤，还按需记录：

```yaml
dataset_impact:
  affected_build_recipes: []
  affected_acceptance_policy: []
  requires_new_dataset_view: <true|false>
```

Promoted Optional 的含义是：

```text
when condition applies
→ should use the bridge discipline

condition does not apply
→ no A5-M required
```

而不是把 A5-M 变成所有项目的必填 Artifact。

---

# E4 — A6-C Curation Contract

**Current status：`PROMOTED OPTIONAL`**

它不替代 A6 Data Intervention，也不是新的 canonical artifact number；它服务于：

```text
已有大规模 source asset
→ routing / dedup / grouping / dataset view
```

的 Asset-led / Curation-led 项目。

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
  - <one or more relevant dimensions: correctness|relevance|completeness|verifiability|novelty|decision_diversity|safety|provenance_quality>

routing_policy:
  pass: <rule|null>
  drop: <rule|null>
  quarantine: <rule|null>
  review: <rule|null>
  downweight: <rule|null>
  regression_only: <rule|null>
  negative_view: <rule|null>
  recovery_view: <rule|null>

dedup_policy:
  exact: <rule|null>
  near_text: <rule|null>
  semantic: <rule|null>
  decision_level: <signature/rule|null>
  family_level: <grouping/rule|null>

split_policy:
  grouping_keys:
    - <one or more applicable keys: case_id|family_id|seed_id|workflow_id|environment_id>

mixture_and_exposure:
  sample_share: <policy|null>
  token_share: <policy|null>
  bucket_weights: <policy|null>
  loss_weight: <policy|null>

yield_funnel:
  raw: <n|null>
  structurally_valid: <n|null>
  evidence_complete: <n|null>
  verified_or_scored: <n|null>
  unique_enough: <n|null>
  accepted_or_routed: <n|null>
  high_value: <n|null>

dataset_view:
  view_id: <id>
  build_recipe_version: <version>
  source_refs: []
  filter_version: <version|null>
  evaluator_version: <version|null>
  schema_transform_version: <version|null>
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

因此 A6-C 最终仍应进入：

```text
A7 matched-budget downstream validation
```

而不是因为 curation KPI 变漂亮就直接宣称训练收益。

Promoted Optional 的含义仍然是：只有存在 source-asset → dataset-view curation contract 需求时加载；不要把它塞回 A6 主模板。

---

# E5 — A5-H Human Annotation / Gold Contract

**Current status：`KEEP CANDIDATE`**

来源：Promotion Test 的 Human Gold / Annotation Refresh 场景。

现有 A5 可以表达：

```text
凭什么判
```

但不完整表达：

```text
谁来判
如何 qualification / calibration
如何 hidden QC
如何 escalation / adjudication
```

因此 E5 只作为待继续验证的执行 contract 候选：

```yaml
annotation_contract_id: <id>
label_schema_version: <version>
guideline_version: <version>

evidence_required:
  - <evidence type>

annotator_roles:
  general: <allowed task|null>
  trained: <allowed task|null>
  expert: <allowed task|null>
  adjudicator: <allowed task|null>

qualification:
  training_set: <id|null>
  gold_set: <id|null>
  pass_rule: <rule|null>

production_qc:
  hidden_gold_rate: <value|null>
  random_audit_rate: <value|null>
  agreement_metric: <metric|null>
  abstain_allowed: <true|false>

escalation:
  disagreement: <route|null>
  low_confidence: <route|null>
  need_expert: <route|null>
  high_severity: <route|null>

adjudication:
  policy: <rule|null>
  final_label_version: <version|null>
  guideline_update_required: <condition|null>

outputs:
  raw_labels: <view|null>
  adjudicated_labels: <view|null>
  gold_updates: <view|null>
  boundary_examples: <view|null>
```

## E5 Boundary

```text
Human Label
≠ Ground Truth by identity

High Agreement
≠ High Validity

Majority Vote
≠ Adjudication

Corrected Label
≠ Historical Decision Rewrite
```

当前禁止：

```text
把 A5-H 写进所有 annotation project 的 mandatory core
把 E5 当作已经 promoted optional
给 E5 分配新的 canonical A-number
```

下一次只有在真实 annotation / expert-labeling workflow 中证明：

```text
缺少该 contract 会造成重复的 audit / decision failure
+
它不与 A5 / Ch6 ownership 冲突
```

才重新进入 Promotion Gate。

---

# 6. Extension Governance / Promotion Gate

当前不是 E1–E5 一起等待同一次 promotion。

状态机应理解为：

```text
Candidate
→ stress test / real use
→ KEEP_CANDIDATE | REVISE | REJECT | PROMOTE_OPTIONAL | PROMOTE_CORE
```

其中：

```text
PROMOTE_CORE
→ principle / routing 进入 Mother practical owner
→ registry 只保留 lineage，不维护第二份真源

PROMOTE_OPTIONAL
→ extension 语义稳定
→ 仅在触发条件成立时加载
→ 不变成 mandatory core / new A-number

KEEP OPTIONAL / scenario-specific
→ 保持可用但局部
→ 不因“有用”自动进入 Mother template

KEEP_CANDIDATE
→ 仍需更多真实使用证据
```

通用 promotion criteria：

```text
[ ] 跨足够不同的真实项目仍解决同一种 ambiguity
[ ] 不与现有 A1–A11 / chapter owner 发生 ownership 冲突
[ ] 字段能删除真实 ambiguity / audit / decision failure
[ ] 不要求不相关项目填写大量 N/A
[ ] 能用 optional extension 时，不强迫主模板膨胀
[ ] 能被外部读者独立填写和复核
```

如果某结构只适合单一场景：

```text
保持 scenario-specific
```

如果已有 contract 组合已经足够：

```text
优先组合
≠ 新增 A12 / P8 / parallel registry
```

---

# 7. Current Ownership Map

```text
Entry Router current truth
→ Project Starter Pack

A1–A11 core artifact definitions
→ Practical Artifact Kit

A10-I / A5-M / A6-C / A5-H extension status + fillable shape
→ this Extensions Registry

Promotion evidence / verdict history
→ Scenario Pack Promotion Test

Execution omission review
→ Checklist Index
```

因此：

```text
Promotion Test
= why status changed

Extensions Registry
= what the current status is

Mother practical asset
= where promoted core behavior is actually owned
```

不要让三者互相复制成 competing truth。

---

# 8. Final Principle

```text
Canonical Core
= 跨项目稳定、由 Mother practical owner 维护

Promoted Optional Extension
= 条件式稳定能力
= only load when relevant

Scenario-specific Optional
= 有用但局部
= do not promote by symmetry

Candidate Extension
= 尚需真实使用证明
```

最终原则：

> **模板成熟的标志不是字段越来越多，而是 Core 越来越稳定、Optional 越来越有条件、Candidate 永远不会因为编号已经存在就自动转正。**
