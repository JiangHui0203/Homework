# L08 — VeriAgent Frozen Case Capstone

> This is the capstone Lab for the Evaluation knowledge system. Unlike L01–L07, it uses a **real VeriAgent experiment**, not synthetic data.

Canonical frozen experiment:

[`../../cases/veriagent/frozen/2026-10-26_challenge_candidate_memory_v1.md`](../../cases/veriagent/frozen/2026-10-26_challenge_candidate_memory_v1.md)

Pinned VeriAgent source commit:

```text
6f5f61c5a612b015c0462bba7f46fa4fd556092a
```

## Learning objective

The goal is not to recompute one score. It is to demonstrate that you can reconstruct and defend the full evidence chain:

```text
evaluation contract
→ benchmark construction
→ dev / held-out separation
→ reviewed failure
→ candidate intervention
→ paired repeated test
→ stage-aware attribution
→ cost / stability
→ promotion decision
→ exposure update
```

After completing L08 you should be able to explain why:

```text
29/36 → 30/36
```

is a real observed result, while:

```text
candidate memory improved capability
```

is **not** supported by this experiment.

## Why this case is the capstone

L08 connects nearly the whole Q01–Q37 graph.

| Knowledge | Real case evidence |
|---|---|
| Q01–Q04 Contract / metrics | frozen claim, denominator, failure handling |
| Q07–Q11 Evaluator | runtime checks + offline independent reference |
| Q12–Q16 Agent eval | staged Data Agent execution and memory retrieval |
| Q17–Q20 Failure analysis | reviewed dev failure + failure-stage attribution |
| Q21–Q24 Benchmark | verified challenge set, dev/test split, exposure boundary |
| Q25–Q30 Statistics | paired movement, repeats vs distinct tasks, uncertainty boundary |
| Q31–Q34 Engineering | manifest, hashes, traces, frozen source commit |
| Q35–Q37 Eval → Data | reviewed failure promotion, candidate freeze, no promotion after attribution failure |

## Case in one diagram

```text
24 verified Olist challenge tasks
│
├── Dev: 12 tasks × 2 repeats
│   └── memory OFF
│       ├── 22/24 correct
│       ├── CJ01_r01 failure
│       └── CJ03_r01 failure
│
├── explicit review
│   ├── reviewed:child_row_eligibility
│   └── reviewed:alias_scope
│
├── freeze candidate memory
│   └── intervention stage = SQL generation
│
└── Held-out: 12 tasks × 3 repeats × 2 conditions
    ├── no memory       29/36
    ├── candidate       30/36
    ├── paired          3W / 2L / 27 both-right / 4 both-wrong
    └── attribution audit
        ├── all 13 failures before SQL-memory stage
        ├── 36/36 first-analysis prompt hashes identical
        └── target SQL errors did not recur
             ↓
        +1/36 NOT attributable to candidate memory
             ↓
        DO NOT PROMOTE
```

## Files

```text
L08_veriagent_frozen_case/
├── README.md
├── audit_case.py
├── REPORT_TEMPLATE.md
├── SOLUTION.md
└── INTERVIEW_PACK.md
```

Canonical evidence lives outside the Lab:

```text
cases/veriagent/frozen/
├── 2026-10-26_challenge_candidate_memory_v1.md
└── 2026-10-26_challenge_candidate_memory_v1.manifest.json
```

The Lab never copies VeriAgent source code.

## Evidence classes

This case deliberately distinguishes two audit levels.

### 1. Git-verifiable

These files exist at the pinned source commit and have frozen Git blob SHAs:

```text
docs/challenge_evaluation.md
docs/experience_memory.md
evaluation/reviews/olist_candidate_v1.json
```

They are sufficient to verify:

- frozen protocol;
- reported development/test summaries;
- candidate review mapping;
- recorded attribution conclusion;
- source commit identity.

### 2. Local-run evidence

The source docs reference local artifacts under:

```text
results/...
memory/...
```

Those are Git-ignored / local and are not present in a normal clone.

They include the raw:

- challenge catalog;
- development runs;
- failure analysis;
- candidate memory file;
- held-out score;
- candidate assessment.

Therefore:

```text
source summary is Git-verifiable
≠ every raw run artifact is public / clone-verifiable
```

This is a feature of the audit, not something to hide.

## Step 1 — Audit internal consistency

Run:

```bash
cd LLM_Agent_Evaluation/labs/L08_veriagent_frozen_case
python audit_case.py
```

This checks arithmetic and logical consistency in the frozen manifest, including:

```text
12 × 2 = 24 dev runs
12 × 3 = 36 held-out runs / condition
36 × 2 = 72 total task runs

3 wins + 2 losses + 27 both-right + 4 both-wrong = 36 pairs

candidate correct - baseline correct
= 30 - 29
= 1
= wins - losses

8 eligible tasks × 3 repeats = 24 potential retrieval hits
6 pre-SQL failures + 18 injected runs = 24
```

A PASS means the **case pack is internally consistent**.

It does not prove the underlying model claims by itself.

## Step 2 — Audit pinned Git provenance

If you have a local VeriAgent clone with the pinned commit object available:

```bash
python audit_case.py --veriagent-root /path/to/veriagent
```

The script reads the files directly from:

```text
git show 6f5f61c5a612b015c0462bba7f46fa4fd556092a:<path>
```

and verifies their Git blob SHA1.

It does not require checking out the old commit.

This protects against:

```text
current file changed
→ historical case silently follows current file
```

## Step 3 — Audit local-only raw artifacts

If the original local VeriAgent workspace still contains the 2026-10-26 run artifacts:

```bash
python audit_case.py \
  --veriagent-root /path/to/veriagent \
  --require-local-artifacts
```

This checks that all documented local-only artifact paths exist.

Important:

- existence is checked;
- their content hashes are **not invented** here because the source Git docs do not freeze those artifact hashes in a form available to this knowledge repository;
- the authoritative raw details remain the original local run artifacts.

## Step 4 — Reconstruct the Evaluation Contract

Without reading `SOLUTION.md`, fill:

```text
Claim:
Population / scope:
Primary unit:
Nested unit:
Conditions:
Intervention stage:
Evaluator:
Primary metric:
Guardrails:
Exposure rule:
Promotion decision:
```

The crucial part is:

> What could the intervention causally affect?

If you cannot answer that, you cannot interpret the result.

## Step 5 — Reconstruct development promotion

Explain why this sequence is valid:

```text
development failure
→ explicit review
→ candidate rule
```

but this shortcut is invalid:

```text
failure occurred
→ automatically write to memory
```

For each of `CJ01_r01` and `CJ03_r01`, distinguish:

```text
observed failure
evidence
rule abstraction
successful independent repeat
```

Do not describe the successful repeat as if it were a learned repair.

## Step 6 — Analyze held-out paired movement

Report:

```text
no-memory  = 29/36
candidate  = 30/36

wrong→right = 3
right→wrong = 2
both-right = 27
both-wrong = 4
```

Then answer:

1. What does `+1/36` prove?
2. What does it not prove?
3. Why are there only 12 distinct held-out tasks?
4. Why are 3 repeats still useful?

## Step 7 — Perform the treatment-delivery audit

Candidate memory is injected only at:

```text
SQL generation
```

Reconstruct:

```text
8 eligible tasks × 3 repeats
= 24 candidate retrieval opportunities

6 fail before SQL
18 receive candidate rules
```

Then answer:

> If a run fails before treatment delivery, can its failure be used as evidence that the treatment failed to repair that mechanism?

And:

> Can an early failure be counted as “the SQL error was avoided”?

Correct answer to both requires stage-aware reasoning.

## Step 8 — Make the attribution decision

The key evidence is:

```text
13 observed failures
13/13 before SQL-stage memory retrieval

36/36 paired first-analysis prompt hashes identical

executed SQL:
29/29 correct without memory
30/30 correct with candidate
```

Write the strongest claim supported by these facts.

Do **not** simply repeat:

```text
candidate +2.78 pp
```

## Step 9 — Add cost and deployment interpretation

Compare:

```text
total tokens:
70,984 → 77,934

tokens / correct:
2,447.72 → 2,597.80
```

Explain why the candidate's slightly lower observed P50/P95 latency does not cancel the cost regression or create reliable latency evidence.

## Step 10 — Update the exposure ledger

Before test:

```text
held-out test = clean for candidate construction
```

After results are observed:

```text
held-out test = exposed for future candidate development
```

State what the set may still be used for and what it may no longer honestly claim.

## Step 11 — Write your report

Copy:

```bash
cp REPORT_TEMPLATE.md MY_REPORT.md
```

Then complete it without using `SOLUTION.md`.

## Step 12 — Interview rehearsal

Use `INTERVIEW_PACK.md`.

You should be able to deliver:

```text
30-second
90-second
5-minute
follow-up defense
```

without reducing the project to “I added memory and accuracy improved.”

## S3 / S4 evidence

L08 is stronger than the synthetic Labs because it requires handling real negative / non-attributable evidence.

Completing it independently is evidence toward S3 across multiple M1 questions if you can:

- reconstruct the protocol from source evidence;
- identify the intervention stage;
- separate treatment assignment from treatment exposure;
- reject an unsupported causal claim despite a positive raw delta;
- preserve test exposure discipline;
- make a promotion decision with quality + cost + provenance;
- explain what would need to change in the next experiment.

S4 requires being able to defend the conclusion under adversarial follow-up.

## Common failure modes

### “30/36 is higher, so memory worked.”

Wrong. It is a raw observed difference. Attribution fails.

### “The target SQL error did not happen, so the memory prevented it.”

Wrong. It did not recur in either arm; early failures cannot be counted as prevented SQL errors.

### “There are 36 test samples.”

There are 36 run observations per condition but only 12 distinct held-out tasks.

### “The second development repeat fixed the first repeat.”

Wrong. It is an independent stochastic repeat.

### “110 tests passed, so the candidate is validated.”

Those tests validate implementation behavior. They do not prove real-model capability improvement.

### “We can change the candidate and test again on the same held-out set.”

You can run it as a regression/development set, but not call the result a fresh first independent test.

## Final capstone question

In one sentence:

> Why is “we did not promote the candidate” a successful Evaluation outcome?

Expected idea:

> Because the evaluation system prevented a small positive aggregate delta from being incorrectly promoted into a causal capability claim when stage-level evidence showed the intervention could not explain the observed failures.
