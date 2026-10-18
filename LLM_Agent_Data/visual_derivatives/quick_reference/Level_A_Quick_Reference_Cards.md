# Level A Quick-reference Cards

> Status: `D3 Complete / Interview & Mobile Reference`
>
> Purpose: 把 Level A 六张 Master Figure 压成可在 30–90 秒内复习的单屏卡片。
>
> Rule: **只保留 Question / Spine / Boundary / Case / Takeaway；不重新定义 canonical concept。**

---

# Card F1 — Learning System

## Question

```text
LLM / Agent Data 到底在维护什么系统？
```

## Spine

```text
Real World
→ Capability / Task
→ Experience Acquisition
→ Experience Objects
→ Evidence
→ Learning Signal
→ Training / Optimization
→ Deployment
→ Outcome / Failure / Drift
↺
```

## Boundary

```text
Experience ≠ Learning Signal
Evidence ≠ Label
Training Data ≠ Raw Production Log
```

## Case

```text
C1:
production failure
→ evidence
→ diagnosis
→ intervention
→ experiment
→ deploy
→ monitor
```

## Takeaway

> **Data work is Learning System Design, not dataset assembly.**

Semantic source: [`F1`](../../figures/F1_Learning_System_Overview.md)

---

# Card F4 — Agent World

## Question

```text
Agent 系统里，Task / Tool / Harness / Environment / State 怎么连接？
```

## Spine

```text
Task / Case
→ Model / Policy
→ Harness
→ Action / Tool
→ Environment
→ World State
→ Observation
→ Harness
→ Agent-visible State
→ Model / Policy
```

Trajectory 记录：

```text
Action + Observation + State Transition + Runtime Evidence
```

## Boundary

```text
Tool ≠ Harness ≠ Environment
World State ≠ Observation ≠ Agent-visible State
Decision Intent ≠ Executed Action
```

## Case

```text
C3-F5:
Tool backend = failure
Harness-visible observation = success
```

## Takeaway

> **Agent failure cannot be diagnosed from dialogue text alone.**

Semantic source: [`F4`](../../figures/F4_Agent_Task_Environment_Trajectory.md)

---

# Card F6 — Credit → Failure

## Question

```text
bad outcome 到底怎么拆成可信 Root Cause / Owner？
```

## Spine

```text
Outcome
→ First Error
→ First Harmful Action
→ Last Recoverable State
→ Point of No Return
→ Symptom
→ Mechanism
→ Root Cause
→ Failure Owner
→ Intervention Routing
```

## Boundary

```text
First Error ≠ First Harmful ≠ Root Cause
Recoverability ≠ Repairability
Failure Layer ≠ Failure Owner
```

## Case

```text
C1-F1 → Model / Policy-owned
C3-F5 → Harness-owned
```

## Takeaway

> **The goal of failure analysis is correct routing, not merely a failure label.**

Semantic source: [`F6`](../../figures/F6_Credit_to_Failure_Causal_Map.md)

---

# Card F8 — Evaluation Protocol

## Question

```text
“方法更好”怎样才是可信 claim？
```

## Spine

```text
Question
→ Capability
→ Benchmark
→ Frozen Protocol
↙            ↘
Baseline    Treatment
↘            ↙
Paired / Matched Analysis
→ Metrics + Cost
→ Uncertainty
→ Claim Scope
```

## Boundary

```text
Benchmark ≠ Protocol ≠ Run ≠ Report
Triggered-only ≠ E2E
Higher Score ≠ Better Method if Budget Differs
```

## Case

```text
C1 family:
Rescue / Harmful / Neutral
+
Tokens / Calls / Latency / Coverage
```

## Takeaway

> **Evaluation produces an auditable claim, not just a score.**

Semantic source: [`F8`](../../figures/F8_Benchmark_Evaluation_Protocol.md)

---

# Card F9 — Data Flywheel

## Question

```text
真实 failure 怎么重新进入下一轮学习？
```

## Spine

```text
Real Use
→ Signal
→ Triage
→ Root Cause
→ Capability Gap
→ Prioritize
→ Acquire Experience
→ Construct Supervision
→ Curate
→ Controlled Experiment
→ Train
→ Evaluate
→ Deploy / Revise
↺
```

## Boundary

```text
Production Failure ≠ Training Example
Failure Signal ≠ Data Problem
Data Intervention ≠ Automatically Worth Scaling
```

## Case

```text
C1:
shipped refund failure
→ diagnose
→ capability abstraction
→ sibling / transfer family
→ matched-budget experiment
→ monitor
```

## Takeaway

> **A flywheel is a learning-opportunity routing system, not a bad-case collector.**

Semantic source: [`F9`](../../figures/F9_Data_Flywheel.md)

---

# Card F14 — Operating Model

## Question

```text
团队和个人怎么调用整套系统？
```

## Organization Spine

```text
Problem
→ Diagnosis
→ Correct Owner
→ Pilot
→ Confirmatory Evaluation
→ Scale / Revise / Stop
→ Deploy / Monitor
↺
```

## Practitioner Spine

```text
Problem Framing
→ Data / Supervision
→ Acquisition
→ State / Trajectory
→ Evaluation / Diagnosis
→ Curation / Optimization
→ Production / Governance
→ Monitoring
↺
```

## Boundary

```text
Problem ≠ Data Problem
Failure Layer ≠ Failure Owner
Pilot Result ≠ Scale Decision
Organization OS ≠ Practitioner OS
```

## Six Questions

```text
What should the model learn?
From what experience?
With what feedback?
How do we know it learned?
Is it worth the cost?
When should the system learn again?
```

## Takeaway

> **Teams route problems to the right owner; practitioners move problems to evidence-backed decisions.**

Semantic source: [`F14`](../../figures/F14_Operating_Model_and_Capability_Map.md)

---

# 2-minute Pre-interview Route

```text
F1
What system am I optimizing?

F6
How do I diagnose failure?

F8
How do I prove improvement?

F14
How do I operationalize it?
```

# 5-minute Agent Data Route

```text
F1
→ F4
→ F6
→ F9
→ F14
```

# 5-minute Research / Eval Route

```text
F1
→ F6
→ F8
→ F9
```

# D3 Acceptance

```text
[x] One screen worth of information per card
[x] No new canonical concepts
[x] One primary spine per card
[x] One boundary block per card
[x] Case used only as proof / lens
[x] Takeaway can stand alone
[x] Level A six-card coverage complete
```
