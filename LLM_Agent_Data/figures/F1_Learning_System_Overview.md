# F1 — Learning System Overview

> 角色：全书总图。回答“LLM / Agent Data 工作到底在维护什么系统？”
>
> Canonical owner：Ch0 / Ch25
>
> 关联：Ch17 Data Flywheel、Ch18 Data Strategy、Ch21 Data Experiments、Ch24 Operating Model

```mermaid
flowchart LR
    A[真实世界<br/>Users / Product / Domain] --> B[Capability / Task Definition]
    B --> C[Experience Acquisition]
    C --> D[Experience Objects]
    D --> E[Evidence & Evaluation]
    E --> F[Learning Signal]
    F --> G[Training / Optimization]
    G --> H[New Model / Policy]
    H --> I[Deployment / Rollout]
    I --> J[Outcome / Failure / Feedback]
    J --> A

    C -.-> C1[Human]
    C -.-> C2[Synthetic]
    C -.-> C3[Production Mining]
    C -.-> C4[Rollout / Counterfactual]

    D -.-> D1[Sample]
    D -.-> D2[Episode]
    D -.-> D3[Trajectory]
    D -.-> D4[Candidate Pool]

    E -.-> E1[Environment Truth]
    E -.-> E2[Verifier]
    E -.-> E3[Grader / Judge]
    E -.-> E4[Human Gold]

    F -.-> F1[SFT Demonstration]
    F -.-> F2[Preference]
    F -.-> F3[Reward]
    F -.-> F4[Process / Recovery Signal]

    J -.-> J1[Success]
    J -.-> J2[Failure]
    J -.-> J3[Drift]
    J -.-> J4[User Feedback]
```

## 读图方式

这张图不是“训练 pipeline”，而是整个知识体系的最小闭环：

```text
真实目标
→ 定义能力
→ 获取经验
→ 记录经验
→ 判断发生了什么
→ 构造学习信号
→ 改变模型
→ 回到真实世界
```

其中最容易被忽略的三条边界是：

```text
Experience ≠ Learning Signal
Evidence ≠ Label
Training Data ≠ Raw Production Log
```

## Case Lens

- `C1`：真实 Agent failure 如何从 production 进入 verifier、data、training，再回到 monitoring。
- `C4`：reasoning state 如何产生 same-prefix counterfactual，再转成 selector / process / training signal。

## 对应章节

```text
Ch1–9   → Experience / Supervision / Acquisition
Ch10–16 → Task / Environment / Trajectory / Measurement
Ch17–21 → Flywheel / Strategy / Curation / Experiment
Ch22–24 → Production / Monitoring / Organization
Ch25    → 全系统调用
```
