# L04 — Trajectory Failure Analysis Lab

> 目标：把 Q17–Q20 从“知道概念”推进到“能从 structured trace 做可审计 failure diagnosis”。

## Learning objective

你将完成一次小型 paired regression triage：

1. 先看 final outcome，但不从 outcome 直接猜 root cause；
2. 沿 trace 找 symptom、first meaningful failure 与 immediate mechanism；
3. 区分 episode-level failure 与“已被完全 recovery 的局部错误”；
4. 为 root cause 标注 `OBSERVED / SUPPORTED / HYPOTHESIS`；
5. 做 baseline / candidate paired win-loss；
6. 按 slice 聚合 regression，但不把 slice association 当因果；
7. 把稳定 failure 提升为 regression candidate。

## Prerequisites

先读：

- [Q17 First Meaningful Failure & Root Cause](../../04_Trajectory_and_Failure_Analysis/01_First_Meaningful_Failure_and_Root_Cause.md)
- [Q18 Step / Outcome & Credit Assignment](../../04_Trajectory_and_Failure_Analysis/02_Step_Outcome_and_Credit_Assignment.md)
- [Q19 Slice-based Regression Diagnosis](../../04_Trajectory_and_Failure_Analysis/03_Slice_Based_Regression_Diagnosis.md)
- [Q20 Failure Taxonomy as Engineering Asset](../../04_Trajectory_and_Failure_Analysis/04_Failure_Taxonomy_as_Engineering_Asset.md)
- [Failure Taxonomy — Evaluation View](../../FAILURE_TAXONOMY.md)

## Scenario

你正在比较同一组 8 个任务的 `baseline` 与 `candidate`。每个 episode 都保存了结构化事件：

```text
task
→ plan / memory
→ tool arguments
→ execution
→ verification
→ recovery
→ final
```

数据故意包含：final success、correct safe stop、false accept、SQL execution failure、stale memory、missed recovery、answer synthesis error，以及 transient failure 后成功 recovery。

其中有些 trace 出现了局部错误，但最终完全恢复；这些不能自动升级成 episode-level failure。

## Files

```text
L04_trajectory_failure_analysis/
├── README.md
├── trajectory_cases.jsonl
├── annotations_starter.csv
├── validate_annotations.py
├── analyze.py
├── REPORT_TEMPLATE.md
└── SOLUTION.md
```

## Annotation contract

先复制：

```bash
cp annotations_starter.csv annotations.csv
```

每行对应一个 episode。`review_status` 只允许：

```text
FAILURE_REVIEWED
NO_EPISODE_FAILURE
```

对 `FAILURE_REVIEWED`，必须填写：

```text
symptom
first_meaningful_failure_event
primary_failure_label
immediate_mechanism
root_cause_hypothesis
evidence_level
owner
regression_candidate
```

`evidence_level` 只允许：`OBSERVED / SUPPORTED / HYPOTHESIS`。

注意：`first_meaningful_failure_event` 不是“最早 status=VIOLATION 的 event”的机械复制。如果某个局部错误被完全 recovery，且最终不再造成 episode-level harm，它可能不应该成为 episode failure。

## Your task

### Task 1 — 先看 outcome movement

在不读 `SOLUTION.md` 前，先回答：

```text
baseline success = ?
candidate success = ?
paired wins = ?
paired losses = ?
both fail = ?
net paired movement = ?
```

### Task 2 — 做逐条 trace review

对所有最终 `FAILURE / FALSE_ACCEPT` episode：写 symptom、找 first meaningful failure、写 immediate mechanism、root-cause hypothesis、evidence level、owner，并决定是否值得形成 regression fixture。

### Task 3 — 处理“局部错误但最终成功”

重点看包含 recovery 的成功 episode。必须回答：局部 first error 是否存在？它是否成为 first meaningful failure？为什么？

### Task 4 — 校验 annotation 结构

```bash
python validate_annotations.py annotations.csv
```

通过只代表：

```text
annotation contract structurally complete
≠ diagnosis scientifically correct
```

### Task 5 — 做 paired / slice analysis

```bash
python analyze.py annotations.csv
```

脚本会输出 baseline/candidate success、paired win/loss、per-slice success、episode-level failure list、你自己的 failure label/evidence/owner 分布，以及 regression candidates。

### Task 6 — 写 Regression Triage

至少回答：candidate 退化是否集中在单一 slice？哪些 loss 有直接 trace evidence？哪些 root cause 只是 hypothesis？哪些 failure 可以直接做 deterministic fixture？哪些需要 replay/counterfactual？为什么不能从 `candidate 50% < baseline 75%` 直接推出一个统一 root cause？

## Deliverables

```text
annotations.csv
MY_REPORT.md
```

建议：

```bash
cp REPORT_TEMPLATE.md MY_REPORT.md
```

## Evaluation rubric

| 能力 | 分值 |
|---|---:|
| outcome / paired movement 正确 | 15 |
| symptom 与 first meaningful failure 分开 | 20 |
| mechanism 与 root cause 分开 | 15 |
| evidence level 使用正确 | 15 |
| recovery episode 不误标 | 10 |
| slice regression 解释克制 | 10 |
| regression promotion 合理 | 15 |

## S3 evidence

不看 `SOLUTION.md` 能完成以下任务，可视为 Q17–Q20 开始进入 S3：从 trace 独立定位 failure；不把最后报错当 root cause；不把每个局部错误都算 episode failure；能做 paired loss + slice diagnosis；能写出 replay / regression next step。

## VeriAgent lens

这个 Lab 的结构直接对应 VeriAgent 当前的诊断方式：

```text
trace stage
→ failure localization
→ evidence strength
→ paired outcome
→ candidate mechanism attribution
```

但本 Lab 使用合成数据，不是 VeriAgent 历史运行产物。
