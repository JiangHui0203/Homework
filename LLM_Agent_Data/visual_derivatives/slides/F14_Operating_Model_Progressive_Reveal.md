# F14 — Operating Model + Capability Map / Progressive Reveal

> Derivative Type: `D2 Presentation Storyboard`
>
> Canvas: `1920 × 1080 / 16:9`
>
> Semantic Source: [`F14_Operating_Model_and_Capability_Map.md`](../../figures/F14_Operating_Model_and_Capability_Map.md)
>
> Source Blob: `65a3c9acb498c06c74a870d5a3dd09b50e654ef2`
>
> Publication Derivative: [`F14_Operating_Model_and_Capability_Map.svg`](../publication/F14_Operating_Model_and_Capability_Map.svg)
>
> Thesis: **成熟团队先做 Diagnosis / Owner Routing，再做 Intervention；成熟个人则用同一套能力把 Problem 推进到可验证 Decision。**

---

# Presentation Rule

F14 不在第一帧同时展示 Organization OS 和 Practitioner OS。

顺序必须是：

```text
Organization OS
→ Decision Gate
→ Practitioner OS
→ Six Root Questions
```

否则一开始会形成两个 competing visual centers。

---

# Frame F14-1 — Start with Diagnosis, Not Data

## Visible Objects

```text
Problem / Requirement / Failure / Opportunity
↓
Diagnosis Gate
↓
Primary Root Cause?
```

## Speaker Line

> “成熟 operating model 的第一步不是把问题交给 Data Team，而是先确认问题真正属于哪一层。”

## Critical Boundary Introduced

```text
Problem
≠ Data Problem
```

---

# Frame F14-2 — Route to the Correct Owner

## Visible Objects

从 Root Cause Gate 展开五个 owner：

```text
Product / Domain
Agent / Infra
Evaluation
Research / Training
Data Research
```

## Speaker Line

> “Product spec、Tool / Harness / Environment、Evaluator、Model / Training、Data Gap 都可能是 owner。failure layer 和 failure owner 不能混。”

## Critical Boundary Introduced

```text
Failure Layer
≠ Failure Owner
```

---

# Frame F14-3 — Intervention Must Pass a Pilot

## Visible Objects

新增：

```text
Data Research / Research / Evaluation
→ Data Intervention Pilot
→ Confirmatory Evaluation
```

## Speaker Line

> “找到 owner 以后仍然不能直接 scale。先做最小 intervention，再用 confirmatory evaluation 决定它是不是真的值得推进。”

## Hidden Until Later

```text
Decision branches
Production
Deploy
Monitoring
Practitioner map
Six questions
```

---

# Frame F14-4 — Scale / Revise / Stop

## Visible Objects

新增 Decision Gate：

```text
Confirmatory Evaluation
→ Decision
```

三个分支必须同时出现：

```text
Scale  → Production / Platform
Revise → Diagnosis Gate
Stop   → Archive / Knowledge
```

## Speaker Line

> “Pilot result 不等于 scale decision。成熟系统必须允许 Revise 和 Stop，而不是所有研究成功都进入生产。”

## Critical Boundary Introduced

```text
Pilot Result
≠ Scale Decision
```

---

# Frame F14-5 — Deploy and Monitor

## Visible Objects

```text
Production / Platform
→ Deploy
→ Monitoring
→ Problem / Requirement / Failure / Opportunity
```

## Speaker Line

> “一旦进入生产，Monitoring 又把新现实带回入口。Organization OS 本质上是一个持续分诊、验证和决策的循环。”

---

# Frame F14-6 — Switch View: Practitioner OS

Organization OS 退为背景或缩到上方，新的主视觉出现：

```text
Real Problem
→ Problem Framing
→ Data Object & Supervision
→ Acquisition / Generation
→ State / Trajectory Understanding
→ Evaluation / Diagnosis
→ Curation / Optimization
→ Production / Governance
→ Monitoring / Continuous Improvement
↺
```

## Speaker Line

> “同一套系统落到个人能力，就是：先 framing，再理解 experience / state / trace，接着评估、实验、生产、监控，而不是一上来选 SFT 还是 DPO。”

## Critical Boundary Introduced

```text
Organization OS
≠ Practitioner OS
```

---

# Frame F14-7 — Six Root Questions

## Visible Objects

在 Practitioner OS 下方依次出现：

```text
1. What should the model learn?
2. From what experience?
3. With what feedback?
4. How do we know it learned?
5. Is it worth the cost?
6. When should the system learn again?
```

## Speaker Line

> “如果只记一件事，就记这六问。它们把 25 章重新压回一个 Learning System Design 的问题解决框架。”

## Final Takeaway

> **团队负责把问题路由到正确 owner；个人负责把问题推进到可验证 decision。两者共享同一套 evidence-first operating logic。**

---

# 30s Version

```text
F14-1
→ F14-2
→ F14-4
→ F14-7
```

# 90s Version

```text
F14-1 → F14-2 → F14-3 → F14-4 → F14-5 → F14-6 → F14-7
```

# Acceptance

```text
[x] Diagnosis precedes owner routing
[x] Scale / Revise / Stop all preserved
[x] Revise returns to Diagnosis Gate
[x] Stop ends in Archive / Knowledge
[x] Organization OS shown before Practitioner OS
[x] Six questions appear only after both systems are established
[x] Source SHA recorded
```