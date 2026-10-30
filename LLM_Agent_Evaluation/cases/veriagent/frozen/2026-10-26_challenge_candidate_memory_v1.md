# VeriAgent Frozen Experiment — Olist Challenge Candidate Memory v1

- Experiment ID: `veriagent-olist-challenge-candidate-memory-v1-2026-10-26`
- Experiment date: 2026-10-26
- Frozen source repository: `JiangHui0203/veriagent`
- Frozen source commit: `6f5f61c5a612b015c0462bba7f46fa4fd556092a`
- Case pack date: 2026-10-30
- Objective: test whether two rules distilled from reviewed development failures improve held-out Olist challenge correctness when injected only at SQL generation.
- Status: **completed; candidate not promoted to default memory**
- Primary lesson: **observed outcome improvement is not automatically attributable to the intervention.**

> This is a historical frozen experiment. It records what was observed under the protocol at the pinned VeriAgent commit. It must not be overwritten by newer project results.

## 1. Executive summary

The experiment followed a disciplined development-to-test sequence:

```text
24-task verified challenge set
├── 12 dev tasks
└── 12 held-out test tasks

Dev baseline, memory off
12 tasks × 2 repeats
→ 22/24 correct
→ review two concrete failures
→ author two candidate rules
→ freeze candidate memory

Held-out paired test
12 tasks × 3 repeats × 2 conditions
→ no-memory: 29/36
→ candidate: 30/36
→ paired: 3 win / 2 loss / 27 both-right / 4 both-wrong
```

The raw paired outcome difference was `+1/36` (`+2.78 pp`). However, this **cannot be credited to the candidate memory**:

```text
candidate intervention stage = SQL generation

all 13 observed held-out failures
occurred before SQL-stage memory retrieval

36/36 paired first-analysis prompts
had identical hashes
```

The target SQL error mechanisms that motivated the two rules did not recur in executed SQL in either arm. Therefore the test did not produce direct counterfactual evidence that the candidate prevented those errors.

Cost also moved in the wrong direction:

```text
total tokens:
70,984 → 77,934  (+9.79%)

tokens / correct completion:
2,447.72 → 2,597.80  (+6.13%)
```

Decision:

```text
retain candidate + evidence
do not replace default memory
fix the earlier analysis-stage table-name failure
validate the next intervention on a fresh held-out set
```

This is a stronger evaluation result than simply reporting “30/36 > 29/36,” because it separates:

```text
mechanism exists
≠ mechanism was exposed
≠ outcome changed because of mechanism
≠ intervention deserves promotion
```

## 2. Task / Data Manifest

The challenge set contains 24 Olist tasks:

```text
12 development
12 held-out test
```

Each split contains 3 tasks from each family:

| Family | Target weakness |
|---|---|
| `payment_grain` | payment-record vs order-level aggregation |
| `customer_identity` | customer identity / repeat-customer semantics |
| `join_fanout` | multi-table fanout and aggregation |
| `time_scope` | purchase/delivery/status time boundaries |

The set was validated before model evaluation:

1. target data subset must be non-empty;
2. reference SQL must agree with an independent Python computation;
3. a designated typical-wrong SQL must differ from the reference beyond tolerance.

The source protocol also records `group_key` handling to reduce near-duplicate leakage across dev/test. The experiment still shares the same database and task-expression templates across splits, so the valid claim is **domain-internal scenario transfer**, not cross-database generalization.

Frozen catalog ID:

```text
fde2a8141cc95b6a2fd5836bd1c11ee3d80efb92a6f9cb7d06bd3124964f4e06
```

## 3. Conditions

### Development condition

```text
candidate memory = OFF
12 dev tasks × 2 repeats
```

Purpose:

- establish baseline behavior;
- locate actual failures;
- explicitly review evidence;
- create a candidate intervention only from development evidence.

### Held-out test conditions

```text
A = no memory
B = only the two reviewed candidate rules

12 held-out tasks
× 3 repeats
× 2 conditions
= 72 task runs
```

The source protocol alternated conditions by task/repeat and did not modify the candidate during the held-out run.

## 4. Model

Requested model:

```text
deepseek-v4-flash
```

The intervention is external experience memory. It does **not** update model weights.

## 5. Environment

The experiment uses:

- local Olist data;
- the VeriAgent Data Agent runtime;
- deterministic schema / SQL safety checks;
- DuckDB execution;
- offline reference scoring;
- hosted-model requests for generation.

The frozen source documents do not make a claim about hardware-specific model execution because generation is provided by the external model service.

## 6. Seeds / Repeats

Development:

```text
12 distinct tasks × 2 repeats = 24 runs
```

Held-out test:

```text
12 distinct tasks × 3 repeats / condition
= 36 runs per condition
```

Important statistical boundary:

```text
36 runs
≠ 36 independent tasks
```

The independent task coverage remains 12 held-out tasks. Repeats measure within-task stochasticity and stability.

No special claim is made that a sampling seed guarantees hosted-model determinism.

## 7. Evaluator

Evaluation deliberately separates runtime checks from offline correctness.

### Runtime layer

The Agent performs normal schema / SQL / safety validation.

### Offline correctness layer

Reference SQL and independent reference values are read for scoring after the paired run. They are not supplied to the model.

The challenge construction requires reference SQL to agree with an independent Python computation.

### Causal attribution layer

The candidate assessment inspects:

- stage at which a failure occurred;
- whether candidate retrieval was reached;
- whether candidate experience was injected;
- first-analysis prompt hashes;
- whether target SQL failure mechanisms recurred.

This prevents the final outcome metric from carrying a causal claim it cannot support.

## 8. Development Results

Development baseline:

| Metric | Result |
|---|---:|
| Correct completions | 22/24 |
| Repeat 1 | 10/12 |
| Repeat 2 | 12/12 |
| Wrong answer accepted | 1 |
| SQL execution failure | 1 |
| Model requests | 71 |
| Total tokens | 46,717 |
| Tokens / correct completion | 2,123.5 |

Two failures were explicitly reviewed.

### CJ01_r01 — child-row eligibility

Observed problem:

- the query grouped the parent order table by unique `order_id`;
- it then used `COUNT(*) >= 2` as if this measured item-row multiplicity;
- the resulting filter was wrong and the runtime accepted the wrong numeric answer.

The successful `CJ01_r02` is an **independent repeat**, not a learned repair.

Candidate rule:

```text
reviewed:child_row_eligibility
```

### CJ03_r01 — alias scope

Observed problem:

- SQL referenced `oi.order_item_id`;
- alias `oi` was not visible in that scope;
- DuckDB rejected the query.

The successful `CJ03_r02` is again an independent repeat.

Candidate rule:

```text
reviewed:alias_scope
```

The frozen review plan is explicitly marked:

```text
APPROVED_FOR_CANDIDATE
```

This means “approved as a candidate intervention for testing,” not “proven useful.”

## 9. Candidate Intervention

Two fixed reviewed rules were authored:

```text
reviewed:child_row_eligibility
reviewed:alias_scope
```

They are retrieved only at the **SQL generation stage**, for questions containing relevant item/payment row-count language.

The candidate does not change:

- model weights;
- the first analysis prompt;
- the default memory file;
- historical answers or dates.

Frozen candidate snapshot ID:

```text
e2837d4e8852bfdc5fe7346889d6bf5e71948814d75086e862fed4d705b0ee7d
```

This stage boundary later becomes decisive for attribution.

## 10. Held-out Results

Held-out execution completed:

```text
72 task runs
190 model requests
```

### Aggregate comparison

| Metric | No memory | Candidate only |
|---|---:|---:|
| Correct | 29/36 | 30/36 |
| Wrong answer accepted | 0 | 0 |
| Analysis-stage nonexistent `payments` table | 7 | 6 |
| Correct after entering SQL | 29/29 | 30/30 |
| Tasks passing all 3 repeats | 7/12 | 9/12 |
| Tasks failing all 3 repeats | 0/12 | 1/12 |
| Total tokens | 70,984 | 77,934 |
| Tokens / correct | 2,447.72 | 2,597.80 |
| Latency P50 | 4.72 s | 4.63 s |
| Latency P95 | 5.61 s | 5.41 s |

Raw accuracy:

```text
no memory  = 80.56%
candidate  = 83.33%
raw delta  = +2.78 pp
```

### Paired movement

| Pair state | Count |
|---|---:|
| Wrong → Right | 3 |
| Right → Wrong | 2 |
| Both Right | 27 |
| Both Wrong | 4 |

Therefore:

```text
paired net = 3 - 2 = +1 run
```

This is an **observed paired outcome difference**, not yet an attribution result.

## 11. Exposure / Treatment Delivery Audit

The candidate can act only after the run reaches SQL-stage experience retrieval.

Candidate retrieval eligibility:

```text
8 held-out tasks
× 3 repeats
= 24 potential candidate hits
```

Within those opportunities:

```text
6 candidate runs failed before SQL
18 candidate runs reached retrieval and received the rules
```

Across all candidate runs:

```text
18/36 actually received candidate injection
```

This distinction matters:

```text
assigned to candidate condition
≠ intervention actually delivered before failure
```

## 12. Attribution Failure

The central finding is not the `+1/36`. It is the mismatch between the intervention stage and the observed failure stage.

Frozen evidence:

```text
observed held-out failures = 13
failures before SQL-stage memory retrieval = 13
```

Also:

```text
36/36 paired first-analysis prompts had identical hashes
```

The candidate memory therefore cannot explain analysis-stage behavior that occurred before memory retrieval.

Further, among runs that actually executed SQL:

```text
no-memory SQL correct = 29/29
candidate SQL correct = 30/30
```

The two target SQL failure types did not recur in either arm.

Therefore:

> The held-out experiment observed a small net outcome difference, but it did not observe the causal pathway required to credit that difference to the candidate memory.

Another crucial boundary:

> “The target error did not occur” is not equivalent to “the memory prevented the target error.”

An early failure never reaching SQL is not an avoided SQL failure.

## 13. Cost / Efficiency

Candidate memory increased model context and cost:

```text
total token delta:
+9.79%

tokens per correct completion:
+6.13%
```

The slight observed P50/P95 latency reduction in the candidate arm is not interpreted as a reliable speed improvement because service latency is externally variable and the candidate consumed more tokens overall.

## 14. Uncertainty

The source experiment deliberately avoids overstating statistical certainty.

Relevant boundaries:

- only 12 distinct held-out tasks;
- 3 repeats per task are nested observations, not new task coverage;
- the frozen source report does not provide a confirmatory task-level CI;
- the test shares the same database / task-template family as development;
- latency is affected by hosted-service variability.

Therefore the correct language is:

```text
small positive observed paired delta
with insufficient causal attribution evidence
```

not:

```text
candidate memory improves capability
```

## 15. Failure Slices

### Intended target mechanisms

- child-row eligibility;
- SQL alias scope.

Observed on development and used to construct the candidate.

### Held-out dominant failure stage

The observed held-out failures occurred before the candidate intervention stage, notably during earlier analysis/table-name behavior.

This means the experiment discovered a more important next intervention target:

```text
earlier analysis-stage schema/table-name correctness
```

rather than validating the SQL-memory intervention.

## 16. Interpretation

### What was demonstrated

1. A challenge set can be built and independently validated before model use.
2. Development failures can be reviewed rather than automatically converted into memory.
3. A candidate intervention can be frozen before held-out testing.
4. Paired repeated evaluation can measure both improvements and regressions.
5. Trace-stage evidence can block an invalid causal attribution.
6. Negative / inconclusive evidence can correctly stop promotion.

### Final decision

```text
DO NOT REPLACE DEFAULT MEMORY
```

Keep:

- the candidate;
- its provenance;
- the development failure evidence;
- the held-out result;
- the attribution failure.

Next:

```text
fix earlier analysis-stage table-name behavior
→ construct / reserve fresh held-out evidence
→ rerun frozen comparison
```

## 17. What this does NOT prove

This experiment does **not** prove:

- candidate memory improves Olist accuracy;
- the two rules prevent their target SQL errors in general;
- the candidate is harmful in general;
- a `+1/36` raw delta is statistically meaningful;
- 36 repeats represent 36 independent tasks;
- the challenge set supports cross-database generalization;
- 0 wrong-answer accepts means all wrong answers are detectable;
- scripted regression tests prove real-model capability;
- slightly lower candidate P95 proves latency improvement.

## 18. Exposure Ledger

At the moment of the held-out run:

```text
12 test tasks = held out from candidate construction
```

After their results were observed:

```text
those tasks are no longer fresh for the next candidate iteration
```

They can remain:

- regression tests;
- known-hard evidence;
- historical frozen evidence.

They cannot be described as a **first independent test** after the candidate is changed.

## 19. Artifacts and Auditability

### A. Git-verifiable evidence

Pinned to VeriAgent commit `6f5f61c5a612b015c0462bba7f46fa4fd556092a`:

- `docs/challenge_evaluation.md`
  - Git blob SHA1: `1ea4f06d34a687b2ccb2c386d5e369a3c72f2626`
- `docs/experience_memory.md`
  - Git blob SHA1: `49f4ede65998cfbdfc99da36df97242d4c632725`
- `evaluation/reviews/olist_candidate_v1.json`
  - Git blob SHA1: `404ef68b64bb09a5841d06a9580db1e57ce0fe7b`

The review plan additionally records:

```text
review_sha256 =
4c0bd9932af8b9f37da4e04c9af050ec38f1ee85b4bdd0d8b08ca09eb75cc0c8
```

### B. Local-run evidence referenced by the frozen source

The source documentation points to local / Git-ignored artifacts including:

- challenge catalog;
- development score and failure analysis;
- candidate memory and promotion report;
- held-out paired score;
- candidate assessment Markdown / JSON.

A normal Git clone does not contain those run directories.

Therefore audit status must distinguish:

```text
Git-verifiable source summary
vs
local raw-run availability
```

The accompanying manifest and `audit_case.py` make that distinction explicit.

## 20. Known Limitations

- Raw run artifacts are local/Git-ignored rather than committed to the source repository.
- Exact hosted-model nondeterminism cannot be replayed byte-for-byte from Git alone.
- The held-out set has only 12 distinct tasks.
- The benchmark remains within one database/domain.
- The candidate was tested only for a narrow SQL-stage retrieval scope.
- No task-level confidence interval was frozen in the source result.
- The target SQL errors did not recur on held-out SQL executions, limiting direct effect identification.

## 21. Source Pointers

Pinned source:

- <https://github.com/JiangHui0203/veriagent/blob/6f5f61c5a612b015c0462bba7f46fa4fd556092a/docs/challenge_evaluation.md>
- <https://github.com/JiangHui0203/veriagent/blob/6f5f61c5a612b015c0462bba7f46fa4fd556092a/docs/experience_memory.md>
- <https://github.com/JiangHui0203/veriagent/blob/6f5f61c5a612b015c0462bba7f46fa4fd556092a/evaluation/reviews/olist_candidate_v1.json>

## 22. Superseded by

None.

Future experiments may update the current project state, but must not mutate this historical record.
