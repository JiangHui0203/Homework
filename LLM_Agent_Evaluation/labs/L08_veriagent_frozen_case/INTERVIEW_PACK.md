# L08 Interview Pack — VeriAgent Frozen Case

This file converts the frozen case into interview-ready language without erasing the negative result.

## 30-second version

> I built a frozen challenge evaluation around VeriAgent's Olist Data Agent. We first evaluated 12 development tasks twice with candidate memory disabled, got 22/24, and explicitly reviewed two failures into two narrow SQL-generation rules. Then we froze those rules and ran 12 held-out tasks three times under paired no-memory and candidate conditions. The raw result was 29/36 versus 30/36, but I did not call that a memory improvement: all 13 held-out failures occurred before the SQL-stage memory retrieval where the intervention could act, and the first-analysis prompts were identical in all 36 pairs. The candidate also increased tokens per correct completion by about 6.1%, so we kept the evidence but did not promote the candidate and required a fresh holdout for the next intervention.

## 90-second version

> The purpose was not just to test whether retrieval was active; it was to test whether reviewed failure-derived experience improved held-out task performance. We first constructed a 24-task Olist challenge set with independent reference validation and split it into 12 dev and 12 held-out tasks across four failure families. On dev, memory was off and we ran two repeats per task. The baseline was 22/24. Two concrete failures were reviewed: one incorrectly used parent-order rows to enforce child-row multiplicity, and one referenced an alias outside SQL scope. We authored two narrow rules from those reviews and froze them before testing.
>
> On held-out evaluation, we ran the same 12 tasks three times in each condition, paired by task and repeat. No-memory was 29/36 and candidate was 30/36, with 3 wins and 2 losses. That looks like +2.78 points, but the trace evidence changed the conclusion. The candidate only enters at SQL generation, while every one of the 13 failures happened before that stage; 36/36 first-analysis prompt pairs were identical. In the runs that reached SQL, both arms' executed SQL was correct against the independent reference. So the experiment did not observe the causal pathway needed to credit the +1 run to memory. On top of that, total tokens rose about 9.8% and tokens per correct rose about 6.1%. We therefore did not replace default memory. The next target was the earlier analysis-stage schema/table-name behavior, and the used test set was marked exposed so a revised candidate would need fresh held-out evidence.

## 5-minute structure

Use this order.

### 1. Problem

```text
Can reviewed development failures be converted into reusable memory
that improves future Olist Data Agent tasks?
```

Avoid saying:

```text
Can memory be retrieved?
```

That is only a mechanism question.

### 2. Benchmark contract

- 24 tasks;
- 12 dev / 12 held-out;
- four task families;
- reference SQL agrees with independent Python;
- designated typical wrong behavior must be distinguishable;
- dev/test share database/template family, so claim is domain-internal transfer.

### 3. Development

```text
12 dev × 2 repeats
memory off
22/24 correct
```

Review:

- `CJ01_r01` → child-row eligibility;
- `CJ03_r01` → alias scope.

Stress:

> The correct second repeat is not a learned repair. It only shows stochastic variation under the same configuration.

### 4. Candidate

Two narrow rules.

Intervention stage:

```text
SQL generation
```

That fact must be frozen **before** interpreting test outcomes.

### 5. Held-out paired result

```text
12 tasks × 3 repeats × 2 conditions
72 task runs
190 model requests
```

```text
29/36 → 30/36
3 wins
2 losses
27 both right
4 both wrong
```

### 6. Attribution audit

Ask:

```text
Did the intervention have an opportunity to cause the observed change?
```

Evidence:

```text
13/13 failures before SQL memory retrieval
36/36 first-analysis prompt hashes identical
target SQL errors absent in executed SQL in both arms
```

Conclusion:

```text
positive raw delta
but no valid attribution to candidate memory
```

### 7. Cost

```text
total tokens +9.79%
tokens / correct +6.13%
```

Candidate does not dominate baseline.

### 8. Decision

```text
do not promote
keep candidate + evidence
fix earlier analysis-stage failure
fresh holdout next
```

### 9. Why this is good evaluation

Because the system was designed to be able to say:

```text
the number moved in the desired direction,
but the claimed mechanism did not earn credit.
```

## Follow-up questions

### Q1. Why paired evaluation?

Because task difficulty is shared across conditions. Pairing the same task and repeat exposes:

```text
wrong→right
right→wrong
both-right
both-wrong
```

instead of hiding movement inside two aggregate accuracies.

### Q2. Why not use 36 as the independent sample size?

Because there are only 12 distinct held-out tasks. The three repeats are nested observations used to study stochasticity/stability.

### Q3. Could the memory still have helped some successful runs?

Possibly, but the frozen evidence does not identify a target-error rescue. The correct claim is not “impossible to help”; it is “this experiment did not provide attribution evidence for the observed net improvement.”

### Q4. Why does `29/29` and `30/30` SQL correctness not prove memory works?

Because both arms were perfect conditional on reaching SQL. The target SQL errors did not recur, so there is no differential event from which to identify prevention.

### Q5. Why can’t a pre-SQL failure count as avoiding a SQL error?

Because the system never reached the opportunity where that SQL error could occur. Removing an opportunity from the denominator would create survivorship/eligibility bias.

### Q6. Why review development failures manually?

The goal is to prevent:

```text
symptom
→ automatic long-term rule
```

A failure needs evidence, an operational mechanism, a correct owner and a bounded abstraction before becoming a candidate intervention.

### Q7. Why keep the candidate if it was not promoted?

Because “not proven” is not the same as “useless.” Provenance-preserving candidates can remain hypotheses or regression assets without being deployed as default behavior.

### Q8. Why is the used test set now exposed?

Once its outcomes affect the next design, it participates in development. Reusing it is valid for regression but not as fresh independent confirmation.

### Q9. Did the candidate increase cost?

Yes. Total tokens increased from 70,984 to 77,934, about 9.79%; tokens per correct completion increased from 2,447.72 to 2,597.80, about 6.13%.

### Q10. But candidate P95 latency was lower. Is that a win?

Not enough to claim one. Hosted-service latency varies, and the experiment did not freeze evidence strong enough for a reliable latency improvement claim. The candidate also used more tokens.

### Q11. What was the next engineering target?

The earlier analysis-stage behavior that produced inaccurate/nonexistent table naming, because held-out failures occurred before SQL-memory retrieval.

### Q12. What would a better next test look like?

```text
new intervention targeting the earlier failure stage
+
frozen candidate
+
fresh held-out tasks
+
same paired protocol
+
stage exposure logging
+
quality/cost/stability guardrails
```

### Q13. What did 110 regression tests prove?

Implementation behavior and protocol guards. They are not real-model capability evidence.

### Q14. What is the strongest one-line project lesson?

> I learned to treat an aggregate improvement as an observation to explain, not as automatic credit for the mechanism I hoped would work.

## Resume / interview phrasing boundary

Good:

> Designed a paired held-out evaluation for failure-derived Agent memory, traced treatment exposure by pipeline stage, and rejected an apparent +2.78pp gain as non-attributable when all observed failures occurred before the intervention stage.

Also good:

> Built development-review → candidate-freeze → held-out-test provenance and preserved negative evidence rather than promoting a higher aggregate score.

Avoid:

> Improved VeriAgent accuracy with memory by 2.78%.

That statement is unsupported by the frozen experiment.
