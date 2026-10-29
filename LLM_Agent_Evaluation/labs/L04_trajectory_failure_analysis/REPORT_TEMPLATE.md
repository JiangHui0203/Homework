# L04 — My Trajectory Failure Analysis Report

## 1. Outcome summary

- Baseline:
- Candidate:
- Paired wins:
- Paired losses:
- Both fail:
- Net:

## 2. Failure reviews

为每个 `FAILURE / FALSE_ACCEPT` episode 写：

```text
Episode:
Symptom:
First meaningful failure:
Immediate mechanism:
Root cause / hypothesis:
Evidence level:
Owner:
Propagated symptoms:
Regression candidate:
```

## 3. Recovered local errors

列出 final success 但中间出现 violation 的 episode：

```text
Episode:
Local error:
Recovery:
Why this is / is not an episode-level first meaningful failure:
```

## 4. Slice diagnosis

| Slice | Baseline | Candidate | Observation | Causal claim allowed? |
|---|---:|---:|---|---|

## 5. Regression triage

### Highest-confidence regression
- Episode:
- Evidence:
- Fixture idea:

### Needs replay / counterfactual
- Episode:
- Hypothesis:
- Minimal replay:

### Shared pre-existing failure
- Episode:
- Why not candidate-specific:

## 6. What the evidence does NOT prove

至少写 3 条。

## 7. 90-second interview answer

用 90 秒回答：

> Agent 最终失败后，你如何从 trajectory 定位 first meaningful failure，并避免错误 root-cause attribution？
