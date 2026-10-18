# LLM / Agent Data Knowledge System：Checklist Index

> 角色：把全书方法论压缩成可执行检查表。适合项目立项、实验设计、数据生产、评测、上线前 review 与复盘。

---

# 1. Problem Framing Checklist

```text
[ ] Problem Statement 是否明确？
[ ] Target Capability 是否定义？
[ ] Target Population 是否定义？
[ ] User / Product Value 是否明确？
[ ] Primary Metric 是否明确？
[ ] Guardrail Metrics 是否明确？
[ ] Failure / Gap 的当前证据是什么？
[ ] 是否存在更便宜的 Product / Prompt / Tool / Harness 修复？
[ ] 为什么这是 Data Problem？
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
[ ] 是否存在 future-info leakage？
[ ] Abstention 是否允许？
[ ] Trigger / Selector / Generator 分开评估？
[ ] Rescue / Harmful / Net 是否统计？
[ ] Coverage / Trigger / Intervention denominator 是否明确？
[ ] Candidate cost / Dynamic N 是否记录？
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

```text
[ ] Research Question
[ ] Baseline
[ ] Treatment / Data Intervention
[ ] Add / Remove / Replace / Reweight 明确
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
[ ] Rollback Guardrails
[ ] Human escalation
[ ] Drift Response Playbook
[ ] Data freshness
[ ] Regression growth / retirement
```

推荐章节：Ch23

Figure：F13

---

# 19. Operating Model Checklist

```text
[ ] Intake source
[ ] Problem owner
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

## 0–5 min

```text
[ ] Goal
[ ] Population
[ ] Primary Metric
[ ] Severity
```

## 5–10 min

```text
[ ] Task / Case
[ ] Trace
[ ] Tool / Harness / Environment
[ ] Evidence
```

## 10–15 min

```text
[ ] Symptom
[ ] Root Cause candidate
[ ] Owner candidate
```

## 15–20 min

```text
[ ] Data Problem?
[ ] Coverage / Supervision / Distribution Gap?
```

## 20–25 min

```text
[ ] Minimum credible intervention
[ ] Baseline / Treatment
[ ] Eval
```

## 25–30 min

```text
[ ] Scale / Revise / Stop threshold
[ ] Regression guardrail
[ ] Cost bound
```

推荐章节：Ch25

---

# 最终总检查

一个成熟项目至少应该能回答：

```text
What is the capability?
What actually happened?
What is the evidence?
Where did failure begin?
Who owns the root cause?
Why is this a data problem?
What learning signal is appropriate?
How will we prove it works?
What does it cost?
When do we stop?
How will we know the world changed again?
```

如果其中某一问回答不了，说明项目还有一个关键闭环没有建立。
