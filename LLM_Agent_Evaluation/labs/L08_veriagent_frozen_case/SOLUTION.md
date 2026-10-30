# L08 — Reference Analysis

Do not use this file before completing `REPORT_TEMPLATE.md`.

## 1. Frozen identity

```text
Experiment:
veriagent-olist-challenge-candidate-memory-v1-2026-10-26

VeriAgent:
6f5f61c5a612b015c0462bba7f46fa4fd556092a

Experiment date:
2026-10-26
```

This is a historical experiment. Newer VeriAgent commits do not alter its interpretation.

## 2. Evaluation contract

### Claim

Does a two-rule memory candidate, derived from explicitly reviewed development failures and injected at SQL generation, improve held-out Olist challenge correctness over no memory?

### Scope

Same Olist database / task-template domain.

Not cross-database generalization.

### Primary unit

Distinct held-out task.

### Nested unit

Repeat/run.

### Conditions

```text
A: no memory
B: only reviewed candidate memory
```

### Intervention stage

SQL generation.

### Evaluator

Runtime safety checks + offline independent reference scoring.

### Primary metric

Paired correctness difference.

### Guardrails

- wrong-answer acceptance;
- stage exposure;
- target-error recurrence;
- tokens / correct;
- latency;
- repeat stability;
- test exposure.

## 3. Benchmark audit

```text
24 total tasks
12 dev
12 held-out
4 families
3 tasks/family/split
```

Reference construction requires:

```text
reference SQL
=
independent Python result
```

and the designated typical-wrong SQL must be distinguishable from the reference.

Because dev/test share database and expression templates, this is domain-internal scenario transfer.

## 4. Development

Baseline:

```text
22/24
```

### CJ01

Observed failure:

- child-row multiplicity was tested on unique parent-order rows;
- incorrect result was accepted.

Rule:

```text
reviewed:child_row_eligibility
```

### CJ03

Observed failure:

- alias `oi` referenced outside scope;
- execution rejected by DuckDB.

Rule:

```text
reviewed:alias_scope
```

The successful `_r02` runs are independent repeats. They do not prove a repair.

## 5. Candidate

```text
snapshot =
e2837d4e8852bfdc5fe7346889d6bf5e71948814d75086e862fed4d705b0ee7d
```

Candidate affects only SQL-generation-stage prompts for relevant row-count questions.

It does not alter the initial analysis prompt or model weights.

## 6. Held-out results

```text
no memory   29/36
candidate   30/36
delta       +1/36 = +2.78 pp
```

Pair movement:

```text
3 wrong→right
2 right→wrong
27 both-right
4 both-wrong
```

This proves only that the candidate arm had one more correct **run observation** under this frozen test.

It does not prove a causal candidate-memory benefit.

## 7. Why N is 12, not 36

There are:

```text
12 distinct tasks
3 repeated runs/task
```

The repeats provide stability information but do not create new task diversity.

## 8. Treatment-delivery audit

Potential candidate opportunities:

```text
8 eligible tasks × 3
= 24
```

Candidate-side outcome:

```text
6 failed before SQL
18 reached SQL and received rules
```

Thus:

```text
condition assignment
≠ treatment exposure before outcome
```

This is the core causal-engineering point.

## 9. Attribution conclusion

Frozen evidence:

```text
13 observed held-out failures
13/13 before SQL memory retrieval

36/36 first-analysis prompt hashes identical
```

Conditional on reaching SQL:

```text
no memory: 29/29 correct SQL
candidate: 30/30 correct SQL
```

So:

> The raw +1/36 outcome delta cannot be attributed to candidate memory because the observed failure events occurred upstream of the intervention and the target SQL failure mechanisms did not recur in either arm.

This does **not** prove the memory never helps. It means this experiment does not identify that effect.

## 10. Cost

```text
70,984 → 77,934 total tokens
= +9.79%

2,447.72 → 2,597.80 tokens/correct
= +6.13%
```

The candidate therefore has an observed cost regression.

P50/P95 happened to be slightly lower in the candidate arm, but hosted-service latency variability prevents treating that small difference as reliable efficiency evidence.

## 11. Exposure

Before test:

```text
held-out relative to candidate construction
```

After observing results:

```text
DEVELOPMENT_EXPOSED for future candidate iterations
```

Still valid:

- historical evidence;
- regression;
- known-hard diagnostics.

No longer valid:

- “first fresh independent test” for a modified candidate.

## 12. Decision

```text
DO NOT REPLACE DEFAULT MEMORY
```

Retain candidate and evidence.

Next target:

```text
earlier analysis-stage table/schema-name correctness
```

Next evidence requirement:

```text
fresh held-out set
```

## 13. Why this is a successful negative result

The experiment did its job:

```text
positive aggregate movement
→ attribution audit
→ causal mismatch found
→ promotion blocked
```

A weak evaluation system would have stopped at `30 > 29`.

A strong evaluation system preserved the distinction between observed association and mechanism credit.

## 14. Interview answer

The recommended 90-second answer is in `INTERVIEW_PACK.md`.

The one-line version is:

> I designed a real paired Agent evaluation where the candidate scored one run higher, but stage-level traces showed every failure happened before the memory intervention could act, so I rejected the apparent gain as non-attributable and did not promote the candidate.
