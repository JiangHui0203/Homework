# LLM / Agent Data Knowledge System：Checklist Index

> 状态：`Stable Mother Edition V3.x / Execution Checklist Index`
>
> 角色：把全书方法论压缩成可执行检查表。适合项目立项、实验设计、数据生产、评测、上线前 review 与复盘。
>
> 调用原则：**先判断项目从哪个 Entry 进入，再加载对应专项 Checklist；Checklist Index 不是要求所有项目按同一条线性流程逐项填写。**

---

# 0. Entry Router Checklist

```text
[ ] 当前项目属于哪种 origin / entry？

    Failure-led
    → 已有可复现 failure / bad case

    Monitoring-led Incident
    → 先看到 alert / online metric shift

    Hypothesis-led
    → 先有机制 / 方法假设

    Evaluation-led
    → 怀疑 evaluator / benchmark / rubric / protocol

    Asset-led / Curation-led
    → 已有 source assets / trajectories / labels，目标是形成可信 data view

[ ] 这个 Entry 的第一证据对象是什么？
[ ] 是否误把 Monitoring Alert 当成 Model Regression？
[ ] 是否误把 Hypothesis 当成已确认 Root Cause？
[ ] 是否误把 Existing Asset 当成 Training Dataset？
[ ] 是否误把 Evaluation Gap 当成 Data Gap？
[ ] 后续是否会汇合到 Controlled Change → Evaluation → Decision？
```

第一入口：[`Project Starter Pack`](./00_Project_Starter_Pack.md)

按需扩展：[`Scenario Pack Candidate Extensions`](./00_Scenario_Pack_Candidate_Extensions.md)

---

# 1. Problem Framing Checklist

```text
[ ] Problem Statement / Scientific Question 是否明确？
[ ] Project Origin / Entry 是否明确？
[ ] Target Capability 是否定义？
[ ] Target Population 是否定义？
[ ] User / Product / Scientific Value 是否明确？
[ ] Primary Metric 是否明确？
[ ] Guardrail Metrics 是否明确？
[ ] Failure / Gap / Hypothesis 的当前证据是什么？
[ ] 当前 Intervention Owner / Type 的候选是什么？
[ ] 是否存在更便宜的 Product / Prompt / Tool / Harness / Evaluator 修复？
[ ] 如果主张“这是 Data Problem”，证据是什么？
[ ] Decision Deadline / Owner 是否明确？
```

推荐章节：Ch10 / Ch18 / Ch24 / Ch25

---

# 2. Task / Case Checklist

```text
[ ] Goal
[ ] Initial World State
[ ] Hidden State / Evaluator-only State
[ ] Available Tools
[ ] Permissions
[ ] Required Constraints
[ ] Forbidden Side Effects
[ ] Success Predicate
[ ] Termination Condition
[ ] Verifier Contract
[ ] Case / Environment Version
[ ] Feasibility 已确认
```

推荐章节：Ch10

Figure：F4

---

# 3. Environment Checklist

```text
[ ] Tool schema version
[ ] Backend version
[ ] Permission set
[ ] Clock / Timezone
[ ] Random seed
[ ] Environment reset
[ ] Snapshot / fixture integrity
[ ] Observation semantics
[ ] Error semantics
[ ] Concurrency assumptions
[ ] Transaction / idempotency semantics
[ ] Final state observable / verifiable
```

推荐章节：Ch11

---

# 4. Trajectory Logging Checklist

```text
[ ] task_id / case_id / episode_id
[ ] model / prompt / runtime versions
[ ] initial world state reference
[ ] agent-visible state
[ ] decision intent
[ ] executed action
[ ] tool arguments
[ ] tool result
[ ] observation
[ ] world state transition / state diff
[ ] retry / backtrack events
[ ] termination type
[ ] final state
[ ] cost / latency / tokens
[ ] branch / parent / sibling lineage
```

推荐章节：Ch12

Figure：F5

---

# 5. Failure Diagnosis Checklist

> 仅在 `Failure-led` 或 incident triage 已确认存在具体 failure 时使用；Hypothesis-led / Evaluation-led 不强制伪造 Root Cause。

```text
[ ] Outcome 是否已客观验证？
[ ] Symptom 是什么？
[ ] First Error 在哪？
[ ] First Harmful Action 在哪？
[ ] Last Recoverable State 在哪？
[ ] Point of No Return 在哪？
[ ] Immediate Mechanism 是什么？
[ ] Root Cause 是什么？
[ ] Failure Layer 是什么？
[ ] Failure Owner 是谁？
[ ] Severity 多高？
[ ] Detectability 多高？
[ ] Repairability 如何？
[ ] 应路由到 Data / Model / Tool / Harness / Evaluator / Product 哪一层？
```

推荐章节：Ch13 / Ch14

Figure：F6

---

# 6. Human Annotation Checklist

```text
[ ] Annotation Unit 明确
[ ] Label Schema 明确
[ ] Guideline 有 positive / negative / boundary example
[ ] 允许 abstain / cannot judge
[ ] Annotator qualification
[ ] Expert routing
[ ] Gold set
[ ] Calibration round
[ ] Blind / randomized candidate order
[ ] IAA / disagreement analysis
[ ] Adjudication policy
[ ] Confidence / reason / evidence capture
[ ] Privacy / access control
[ ] Raw annotation 与 final adjudicated label 分开保存
[ ] Guideline / Gold 换版时，旧版与新版是否有 paired bridge / anchor continuity？
```

推荐章节：Ch6 / Ch19

---

# 7. Preference Data Checklist

```text
[ ] Context / Task 一致
[ ] Candidate lineage 可追踪
[ ] Chosen 不被当作绝对 ground truth
[ ] Tie / Both Bad / Cannot Judge 可表达
[ ] Candidate gap 不全是 perfect vs garbage
[ ] 有 hard negative / boundary pair
[ ] Rubric 多维且优先级明确
[ ] Position swap audit
[ ] Verbosity / style bias audit
[ ] Objective verifier 优先使用
[ ] Preference source / judge version 已记录
[ ] Downstream utility 最终验证
```

推荐章节：Ch3 / Ch6 / Ch15 / Ch21

---

# 8. Synthetic Data Checklist

```text
[ ] 目标 capability 明确
[ ] Seed provenance 完整
[ ] Generator version / prompt / seed 已保存
[ ] Task / response / trajectory / environment synthesis 类型明确
[ ] Surface diversity 和 decision diversity 分开评估
[ ] Teacher bias 风险已分析
[ ] Mode collapse / model monoculture 已检查
[ ] Executable / rule verifier 尽量优先
[ ] Synthetic family ID / lineage 已保存
[ ] Train / eval family 隔离
[ ] Human / production anchor 存在
[ ] Synthetic-to-real transfer 有验证
```

推荐章节：Ch7 / Ch19 / Ch20 / Ch21

---

# 9. Hard Case Mining Checklist

```text
[ ] Hard 的定义是什么？
[ ] Model-hard 还是 State-hard？
[ ] 是否位于 capability frontier？
[ ] Uncertainty 是否只是 proxy？
[ ] Disagreement 是否有 objective resolution？
[ ] Failure frequency / severity 如何？
[ ] Learnability 如何？
[ ] Verifiability 如何？
[ ] 是否与已有数据重复？
[ ] Mining policy 是否造成 selection bias？
[ ] 是否有 random / alternative mining baseline？
[ ] Training value 是否做过 downstream test？
```

推荐章节：Ch9 / Ch18 / Ch21

---

# 10. Candidate / Selector Checklist

```text
[ ] Authoritative state / prefix 是否冻结？
[ ] Candidate generation 是否同条件？
[ ] Candidate diversity 是否足够？
[ ] Oracle upper bound 多大？
[ ] Selector 使用的 feature 是否 online-available？
[ ] Online-observable / Offline-only / Forbidden-leakage 是否分开？
[ ] 是否存在 future-info leakage？
[ ] Abstention 是否允许？
[ ] Trigger / Selector / Generator 分开评估？
[ ] Rescue / Harmful / Net 是否统计？
[ ] Full / Screened / Eligible / Triggered / Intervened / Observed population ledger 是否完整？
[ ] 每个 metric 的 denominator 是否明确？
[ ] Candidate cost / Dynamic N 是否记录？
[ ] Per-trigger / incremental intervention / full-pop average / worst-case cost 是否分开？
```

推荐章节：Ch4 / Ch8 / Ch16

Figure：F3 / F8

---

# 11. Evaluator / Judge Checklist

```text
[ ] Raw evidence 是什么？
[ ] 是否有 direct environment / executable verifier？
[ ] 为什么需要 Grader / Judge？
[ ] Rubric version
[ ] Judge model / prompt version
[ ] Evidence package version
[ ] Gold / Anchor Set
[ ] FP / FN
[ ] Position bias
[ ] Verbosity / style bias
[ ] Swap consistency
[ ] Domain / difficulty slice
[ ] High-severity slice
[ ] UNRESOLVED / ABSTAIN 支持
[ ] Raw judgment 与 derived label 分开
[ ] Judge drift monitoring
[ ] Evaluator / rubric / guideline 换版时，是否建立 old↔new paired Measurement Bridge？
[ ] 没有 bridge 时，是否避免把新旧 score 直接拼成一条 longitudinal curve？
```

推荐章节：Ch15 / Ch23

Figure：F7

---

# 12. Benchmark / Evaluation Checklist

```text
[ ] Scientific / Product Question
[ ] Capability Definition
[ ] Benchmark Object
[ ] Full Population
[ ] Eligible Population
[ ] Triggered / Intervened Population if any
[ ] Model / Prompt / Tokenizer
[ ] Tool / Harness / Environment
[ ] Budget / Stop Conditions
[ ] Evaluator / Label Version
[ ] Seed / Repetition Policy
[ ] Paired / Matched Design
[ ] Primary Metric
[ ] Guardrails
[ ] Cost / Latency / Tokens
[ ] Failure Transition
[ ] Statistical Uncertainty
[ ] Cluster / repeated-case structure
[ ] Multiple-comparison risk
[ ] Claim Scope
[ ] Frozen Core + Fresh Frontier
```

推荐章节：Ch16

Figure：F8

---

# 13. Data Curation Checklist

```text
[ ] Source asset identity / lineage 完整
[ ] Structural validity
[ ] Privacy / license
[ ] Exact dedup
[ ] Near dedup
[ ] Semantic / decision-level dedup
[ ] Family-level grouping
[ ] Contamination
[ ] Verifier / rule checks
[ ] Model-based quality dimensions
[ ] Human review for high-risk / disagreement
[ ] Capability tags
[ ] Difficulty tags
[ ] Failure tags
[ ] Source tags
[ ] Drop / Keep / Quarantine / Downweight / Review routing
[ ] Sample ratio vs token ratio 明确
[ ] Length bias 检查
[ ] Source dominance 检查
[ ] Before / after distribution audit
[ ] Dataset View 是否可由 Source IDs + Build Recipe 重建？
[ ] Existing Asset 是否被误当作已验证 Training Dataset？
```

推荐章节：Ch20

---

# 14. Data Mixture Checklist

```text
[ ] Target capability weights
[ ] Source weights
[ ] Difficulty weights
[ ] Positive / negative / recovery balance
[ ] Sample exposure vs token exposure
[ ] Long trajectory token dominance
[ ] Small-but-important bucket 是否被淹没
[ ] Hard negative ratio
[ ] Safety / refusal overcorrection risk
[ ] Interaction between buckets
[ ] Curriculum 是否单独定义
[ ] Mixture version / rationale
[ ] Model version ↔ mixture version 绑定
[ ] Downstream ablation / weight sweep
```

推荐章节：Ch20 / Ch21

---

# 15. Data Experiment Checklist

> 本节专门检查 Data Intervention；非 Data Intervention 使用 Starter Pack 的通用 A7 / Method Contract，不需要硬改名成 Data Experiment。

```text
[ ] Research Question
[ ] Baseline
[ ] Treatment / Data Intervention
[ ] Add / Remove / Replace / Reweight / Transform 明确
[ ] Data manifest / version
[ ] Base model / checkpoint 固定
[ ] Training recipe 固定
[ ] Token / compute budget matching
[ ] Primary eval
[ ] General regression
[ ] Safety / risk regression
[ ] Cost metrics
[ ] Pilot first
[ ] Scaling curve
[ ] Transfer / held-out family
[ ] Seed / evaluation variance
[ ] Paired analysis
[ ] Failure transition
[ ] Mechanism check
[ ] Multiple comparison control
[ ] Experiment registry
[ ] SCALE / MAINTAIN / REVISE / STOP / RETIRE 决策
```

推荐章节：Ch21

---

# 16. Governance / Reproducibility Checklist

```text
[ ] Stable IDs
[ ] Raw evidence preserved
[ ] Canonical record defined
[ ] Provenance
[ ] Lineage DAG
[ ] Dataset version
[ ] Schema version
[ ] Label version
[ ] Prompt / model / tool / harness / environment version
[ ] Code commit
[ ] Config
[ ] Seed
[ ] Hash / counts
[ ] Re-score / Re-run / Replay semantics
[ ] Train lineage
[ ] Eval lineage
[ ] Contamination registry
[ ] Privacy / rights / purpose
[ ] Retention / deletion policy
```

推荐章节：Ch19

Figure：F11

---

# 17. Data Production Checklist

```text
[ ] Production Contract
[ ] Request ID
[ ] Job sharding
[ ] Job state machine
[ ] Queue priority
[ ] Worker type
[ ] Input manifest replayable
[ ] Transient / deterministic / semantic failure 区分
[ ] Retry budget
[ ] Idempotency
[ ] DLQ
[ ] Artifact Store
[ ] Metadata Store
[ ] Structural validation
[ ] Verifier / Judge / Human routing
[ ] Quality Gate
[ ] Dataset Router
[ ] Build Recipe
[ ] Split inheritance
[ ] Cost accounting
[ ] Yield funnel
[ ] Backpressure
[ ] Environment isolation / reset
[ ] Handoff to training / eval
[ ] Downstream result 回流
```

推荐章节：Ch22

Figure：F12

---

# 18. Monitoring / Drift Checklist

```text
[ ] Last-known-good version / time window
[ ] Change Ledger：Model / Prompt / Tool / Harness / Environment / Judge / Traffic / Business Rule
[ ] Stable raw facts
[ ] Metric definition version
[ ] Model / Prompt / Tool / Harness / Environment / Judge versions
[ ] Traffic metrics
[ ] Runtime metrics
[ ] Behavior metrics
[ ] Outcome metrics
[ ] Slice metrics
[ ] Raw overall + fixed-mix metric
[ ] Data Drift
[ ] Concept Drift
[ ] Failure Drift
[ ] Capability Drift
[ ] Judge Drift
[ ] Infrastructure Drift
[ ] Score calibration
[ ] Coverage / Success@Coverage
[ ] Eligible / Triggered / Intervened denominator
[ ] Fresh Failure Cohort
[ ] Frozen Core Benchmark
[ ] Shadow / Canary
[ ] Containment / Rollback Guardrails
[ ] Human escalation
[ ] Drift Response Playbook
[ ] Data freshness
[ ] Regression growth / retirement
[ ] Alert 只作为 sensing event，Root Cause claim 是否等待 triage evidence？
```

推荐章节：Ch23

Figure：F13

---

# 19. Operating Model Checklist

```text
[ ] Intake source
[ ] Problem owner
[ ] Entry / origin mode
[ ] Data Problem Gate
[ ] Failure routing
[ ] RACI
[ ] Decision rights
[ ] Research vs Production mode
[ ] Research-to-Production Gate
[ ] Handoff Contract
[ ] Stage Exit Criteria
[ ] Roadmap priority
[ ] Budget owner
[ ] Release gate
[ ] Monitoring owner
[ ] Rollback owner
[ ] Data incident process
[ ] Retirement rule
```

推荐章节：Ch24

Figure：F14

---

# 20. 30-minute Quick Diagnosis Checklist

## 0–5 min — Entry + Scope

```text
[ ] Entry：Failure / Monitoring / Hypothesis / Evaluation / Asset？
[ ] Goal / Scientific Question
[ ] Full Population
[ ] Primary Metric / Decision Object
[ ] Severity / Scientific Value
```

## 5–10 min — Contract + Evidence

```text
[ ] Task / Case / Decision State / Source Asset
[ ] Trace / Lineage
[ ] Tool / Harness / Environment / Evaluator versions
[ ] Available Evidence
```

## 10–15 min — 按 Entry 分支

```text
Failure-led
[ ] Symptom / Mechanism / Root Cause candidate / Owner candidate

Monitoring-led
[ ] Last-known-good / Change Ledger / Raw vs Fixed-mix / Containment

Hypothesis-led
[ ] Observable Signal / Mechanism / Counterfactual / Oracle Headroom

Evaluation-led
[ ] Claim / Evidence / Evaluator / Coverage / Measurement Bridge need

Asset-led
[ ] Source integrity / lineage / routing / dedup / rebuildability
```

## 15–20 min — Intervention Gate

```text
[ ] 最可能的 Intervention Owner / Type
[ ] Data / Model / Inference / Tool / Harness / Evaluator / Product？
[ ] 如果是 Data Problem：Coverage / Supervision / Distribution / Decision-boundary Gap？
```

## 20–25 min — Minimum Controlled Change

```text
[ ] Minimum credible intervention
[ ] Baseline / Treatment or old↔new bridge
[ ] Frozen Eval / Guardrail
[ ] Population / Information / Cost ledger if selective
```

## 25–30 min — Decision

```text
[ ] Scale / Maintain / Revise / Stop / Retire threshold
[ ] Regression guardrail
[ ] Cost bound
[ ] Claim scope
```

推荐章节：Ch25

---

# 最终总检查

一个成熟项目至少应该能回答：

```text
What kind of problem / entry is this?
What is the capability / decision object?
What actually happened or what hypothesis is being tested?
What is the evidence?
If failure-led: where did failure begin and who owns the root cause?
If evaluation-led: is the ruler valid and comparable across versions?
If asset-led: can the dataset view be rebuilt from source lineage?
Why is the chosen intervention layer the right owner?
If this is a data problem, what learning signal is appropriate?
How will we prove the controlled change works?
What does it cost?
When do we stop?
How will we know the world changed again?
```

如果其中某一问回答不了，说明项目还有一个关键闭环没有建立。