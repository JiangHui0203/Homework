# L02 Judge Calibration — My Report

## 1. Evaluation claim

We want to know whether Judge-X can:

```text
...
```

- Target task:
- Unit of analysis:
- Judge output:
- Reference evidence:
- Planned decision:
- Error cost:

## 2. Pre-registered gates

| Gate | Threshold | Result | Pass? |
|---|---:|---:|---|
| Pointwise within ±1 | ≥ 90% | | |
| Critical disagreement | ≤ 2% | | |
| Pairwise accuracy | ≥ 80% | | |
| Repeat consistency | ≥ 95% | | |
| Swap consistency | ≥ 95% | | |
| Style slice pairwise accuracy | ≥ 70% | | |
| Verbose-preference gap | ≤ 15 pp | | |

## 3. Pointwise results

- Exact agreement:
- Within ±1:
- MAE:
- Critical disagreement:
- Human-Human exact:
- Judge repeat exact:

### Interpretation

- What looks good:
- What is risky:
- Why within ±1 alone is insufficient:

## 4. Pairwise results

- Judge-Human accuracy:
- Judge repeat consistency:
- Swap consistency:
- Accuracy after swap:
- Human-Human exact:

### Verdict flips

- Pair IDs:
- Likely explanation:
- Alternative explanation:

## 5. Bias slicing

### Task family

| Slice | N | Accuracy | Repeat | Swap | Interpretation |
|---|---:|---:|---:|---:|---|
| factual | | | | | |
| instruction | | | | | |
| reasoning | | | | | |
| safety | | | | | |
| style | | | | | |

### Probe analysis

| Probe | Judge signal | Human reference | Gap | Causal claim allowed? |
|---|---:|---:|---:|---|
| B more verbose | | | | |
| B more polished | | | | |
| B family-match | | | | |

For each suspected bias:

```text
Observed signal:
Plausible explanation:
Confounder:
Follow-up controlled experiment:
```

## 6. Manual adjudication

### C01
- Final label:
- Decisive evidence:
- Why disagreement happened:
- Rubric change?
- Judge change?

### C02
- Final label:
- Decisive evidence:
- Why disagreement happened:
- Rubric change?
- Judge change?

### C03
- Final label:
- Decisive evidence:
- Why disagreement happened:
- Rubric change?
- Judge change?

### C04
- Final label:
- Decisive evidence:
- Why disagreement happened:
- Rubric change?
- Judge change?

### C05
- Final label:
- Decisive evidence:
- Why disagreement happened:
- Rubric change?
- Judge change?

## 7. Deployment decision

Choose one: `GO / CONDITIONAL GO / NO-GO`.

- Decision:
- Allowed scope:
- Forbidden scope:
- Required human escalation:
- Required deterministic checks:
- Required next experiment:

## 8. What this experiment does NOT prove

1.
2.
3.

## 9. 90-second interview answer

> “你会怎样验证一个 LLM-as-a-Judge 是否足够可靠，可以上线使用？”

...
