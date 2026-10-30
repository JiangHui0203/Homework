# L07 Eval Harness — My Report

## 1. Evaluation Contract

```text
Benchmark:
Variants:
Tasks:
Repeats:
Planned runs / variant:
Critical tasks:
Fault profiles:
```

## 2. Artifact Graph

```text
tasks / contract / fixtures
→ config snapshot
→ results + traces
→ summary
→ manifest / hashes
→ validation
→ replay
→ gate
```

哪些 artifact 是 raw evidence？

哪些是 derived artifact？

## 3. Baseline Summary

| Metric | Value |
|---|---:|
| Completed / Planned | |
| Valid Success | |
| Success Rate | |
| Critical Invalid | |
| Total Tokens | |
| Tokens / Valid Success | |
| P50 Latency | |
| P95 Latency | |
| Repeat Consistency | |
| Flaky Tasks | |
| Budget Violations | |
| Replay Match | |

## 4. Candidate Summary

| Metric | Value |
|---|---:|
| Completed / Planned | |
| Valid Success | |
| Success Rate | |
| Critical Invalid | |
| Total Tokens | |
| Tokens / Valid Success | |
| P50 Latency | |
| P95 Latency | |
| Repeat Consistency | |
| Flaky Tasks | |
| Budget Violations | |
| Replay Match | |

## 5. Artifact Validation

Validation 通过意味着什么？

Validation 不证明什么？

故意篡改 trace 后发生了什么？

## 6. Replay

为什么本 Lab 可以 exact replay？

真实 hosted LLM 为什么通常只能要求较弱的 contract replay？

Replay reproduced 是否证明 root cause？

## 7. Fault Injection Review

### T03 — missing evidence

Expected behavior:

Observed:

### T04 — transient timeout

Expected behavior:

Observed:

### T05 — stale schema

Expected behavior:

Observed:

### T06 — permission denied

Expected behavior:

Observed:

## 8. Quality / Cost / Latency / Stability Trade-off

Candidate 改善了什么？

Candidate 变差了什么？

为什么 total tokens 和 tokens / valid success 会给出不同视角？

## 9. CI Placement

| Check | PR hard | PR soft | Scheduled / Release | Why |
|---|---|---|---|---|
| Artifact hash | | | | |
| Exact fixture replay | | | | |
| Critical safe-stop | | | | |
| P95 latency | | | | |
| Repeat consistency | | | | |
| Fresh generalization | | | | |

## 10. Gate Decision

```text
Decision:
Failed gates:
Passed gates:
```

为什么 quality improvement 不能覆盖 hard gate failure？

## 11. Final Evidence Statement

用一段话完整写出：

```text
artifact completeness
quality
critical reliability
cost
latency
stability
replay
gate
interpretation boundary
```
