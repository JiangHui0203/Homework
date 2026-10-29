# L05 — My Agent Recovery Evaluation Report

## 1. Frozen policy

- Retryable faults:
- Must-safe-stop faults:
- Max attempts:

## 2. Denominators

- All episodes:
- Recovery opportunities:
- Recovery attempts:
- Recovered successes:
- Must-safe-stop episodes:
- Observed safe stops:

## 3. Metrics

| Metric | Value | Denominator |
|---|---:|---|
| Final valid success | | |
| First-pass success | | |
| Recovery opportunity rate | | |
| Recovery attempt \| opportunity | | |
| Recovery success \| opportunity | | |
| Recovery success \| attempt | | |
| Safe-stop precision | | |
| Safe-stop recall | | |
| Tokens / valid success | | |

## 4. Control-policy violations

| Episode | Violation | Why it matters |
|---|---|---|

## 5. False recovery

- Episode:
- Why mechanism executed != recovery success:

## 6. Recovery cost

- Mean extra tokens:
- Mean extra latency:
- High-cost outlier:

## 7. Release gates

| Gate | Result | PASS/FAIL |
|---|---:|---|

## 8. Final decision

`GO / NO-GO`

Explain why.

## 9. What this experiment does NOT prove

至少 3 条。

## 10. 90-second interview answer

回答：

> 一个 Agent 带 retry / fallback 时，你怎样评价 recovery，而不让最终成功率掩盖不稳定和成本？
