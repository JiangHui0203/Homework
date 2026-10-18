# F8 — Benchmark / Evaluation Protocol

> 角色：固定“一个模型 / 方法提升结论到底怎样成立”。
>
> Canonical owner：Ch16
>
> 主案例：C1 family / paired model comparison

```mermaid
flowchart TD
    Q[Scientific / Product Question] --> CAP[Capability Definition]
    CAP --> B[Benchmark Object]
    B --> P[Evaluation Protocol]

    P --> P1[Population / Eligibility]
    P --> P2[Model / Prompt / Tool / Harness / Environment]
    P --> P3[Budget / Stop Conditions]
    P --> P4[Evaluator / Label Version]
    P --> P5[Seeds / Repetitions]

    P --> R1[Baseline Run]
    P --> R2[Treatment Run]

    R1 --> PAIR[Paired / Matched Analysis]
    R2 --> PAIR

    PAIR --> M[Metrics]
    M --> M1[Success / Accuracy]
    M --> M2[Rescue / Harmful / Net]
    M --> M3[Coverage / Trigger / Intervention]
    M --> M4[Cost / Latency / Tokens]
    M --> M5[Failure Transition]

    M --> U[Uncertainty / Statistics]
    U --> C[Claim Scope]
```

## 四个不同对象

```text
Benchmark Object
= 测什么 case

Evaluation Protocol
= 怎么运行和怎么判

Evaluation Run
= 某一次具体执行

Evaluation Report
= 对 runs 的统计与结论
```

## Population Accounting

Selective / triggered system 必须保留：

```text
Full Population
↓
Eligible
↓
Triggered
↓
Intervened
↓
Resolved / Observed Outcome
```

任何分数必须说明 denominator。

## Paired Comparison

同一 Case 上比较 Baseline 与 Treatment：

```text
Baseline wrong → Treatment right
= Rescue / Repair

Baseline right → Treatment wrong
= Harmful / Degradation
```

仅比较两个总体平均分，会隐藏 intervention 到底修了什么、伤了什么。

## Budget Discipline

```text
Better Score
```

必须同时问：

```text
Same token budget?
Same tool budget?
Same number of candidates?
Same latency class?
```

否则结论可能只是：

> 花了更多计算，所以更高。

## Claim Scope

最后的结论应与证据匹配：

```text
Observed on this benchmark / protocol
≠
Universal capability improvement
```

尤其小样本、many-config exploration、single-seed 结果需要限制表述范围。
