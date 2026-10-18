# F14 — Operating Model + Capability Map

> 角色：全书收束图。把“团队怎么运行”和“个人怎么调用”放在同一张 operating architecture 中。
>
> Canonical owner：Ch24–25
>
> 主案例：All Canonical Cases

## A. Organization Operating Model

```mermaid
flowchart LR
    IN[Problem / Requirement / Failure / Opportunity] --> DG[Diagnosis Gate]
    DG --> RC{Primary Root Cause?}

    RC -->|Product / Requirement| PROD[Product / Domain]
    RC -->|Tool / Harness / Environment| INFRA[Agent / Infra]
    RC -->|Evaluator| EVAL[Evaluation]
    RC -->|Model / Training| RES[Research / Training]
    RC -->|Data Gap| DATA[Data Research]

    DATA --> PILOT[Data Intervention Pilot]
    RES --> PILOT
    EVAL --> PILOT

    PILOT --> CONF[Confirmatory Evaluation]
    CONF --> DEC{Decision}

    DEC -->|Scale| PLATFORM[Production / Platform]
    DEC -->|Revise| DG
    DEC -->|Stop| ARCH[Archive / Knowledge]

    PLATFORM --> DEP[Deploy]
    DEP --> MON[Monitoring]
    MON --> IN
```

核心不是“所有问题都进入 Data Team”，而是：

```text
Problem
→ Diagnosis
→ Correct Owner
→ Evidence Gate
→ Intervention
→ Evaluation
→ Decision
```

## B. Practitioner Capability Map

```mermaid
flowchart TD
    P[Real Problem] --> A[Problem Framing]
    A --> B[Data Object & Supervision]
    B --> C[Acquisition / Generation]
    C --> D[State / Trajectory Understanding]
    D --> E[Evaluation / Diagnosis]
    E --> F[Curation / Optimization]
    F --> G[Production / Governance]
    G --> H[Monitoring / Continuous Improvement]
    H --> P
```

八域能力不是八个独立岗位，而是解决问题时会反复调用的八组能力。

## 30-minute Diagnosis Lens

```text
0–5 min
定义目标、population、metric

5–10 min
看 Task / Case / Trace / Tool / State / Evidence

10–15 min
做 Product / Model / Tool / Harness / Environment / Evaluator 归因

15–20 min
判断是否真的是 Data Gap

20–25 min
设计最小可信 intervention

25–30 min
预先定义 Scale / Revise / Stop Rule
```

## 六个根问题

```text
1. What should the model learn?
2. From what experience?
3. With what feedback?
4. How do we know it learned?
5. Is it worth the cost?
6. When should the system learn again?
```

这六问对应整本书最稳定的终局 mental model：

> **Learning System Design。**
