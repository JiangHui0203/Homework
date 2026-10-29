# L01 Metric Design — My Report

## 1. Evaluation claim

### What decision are we supporting?


### Unit of analysis


### Agent failure vs infrastructure failure


## 2. Protocol health

| Item | Result | Interpretation |
|---|---:|---|
| Scheduled runs | | |
| Evaluable runs | | |
| Infrastructure aborts | | |
| Experiment completeness | | |
| Official score status | | |

## 3. Metric contracts

### M01 Task Success Rate

- Question:
- Unit:
- Numerator:
- Denominator:
- Inclusion rule:
- Aggregation:
- Failed / missing handling:
- Direction:
- What it measures:
- What it does NOT measure:

### M02 Accepted Output Accuracy

- Question:
- Unit:
- Numerator:
- Denominator:
- Inclusion rule:
- Aggregation:
- Failed / missing handling:
- Direction:
- Interpretation boundary:

### M03 False Accept Rate

- Question:
- Unit:
- Numerator:
- Denominator:
- Inclusion rule:
- Aggregation:
- Failed / missing handling:
- Direction:
- Interpretation boundary:

### M04 Safe Stop Success Rate

- Question:
- Unit:
- Numerator:
- Denominator:
- Inclusion rule:
- Failed / missing handling:
- Interpretation boundary:

### M05 Recovery Success Rate

- Question:
- Unit:
- Numerator:
- Denominator:
- Inclusion rule:
- Failed / missing handling:
- Interpretation boundary:

### M06 Tokens per Valid Success

- Question:
- Numerator:
- Denominator:
- Failed-run cost handling:
- Zero-success handling:
- Interpretation boundary:

### M07 End-to-End P95 Latency

- Population:
- Quantile definition:
- Missing handling:
- Interpretation boundary:

### M08 Experiment Completeness

- Numerator:
- Denominator:
- Why it is not a capability metric:
- How it gates official reporting:

## 4. Results

| Metric | Result | Gate | Pass? |
|---|---:|---:|---|
| Experiment completeness | | 100% | |
| Task Success Rate | | >= 75% | |
| Accepted Output Accuracy | | diagnostic | |
| False Accept Rate | | 0% | |
| Safe Stop Success Rate | | >= 90% | |
| Recovery Success Rate | | >= 70% | |
| Tokens per Valid Success | | <= 1800 | |
| P95 latency | | <= 4500 ms | |

## 5. Denominator audit

### Why is 16/19 not Task Success Rate?


### Why can 3/6 and 3/22 both be mathematically valid?


### Which one should be named False Accept Rate in this contract?


## 6. Failure / missing audit

### System failures included in capability denominator


### Infrastructure failures excluded from capability but retained in protocol completeness


### Why failed-run cost stays in total cost


## 7. Slice analysis

| Family | Success | Interpretation |
|---|---:|---|
| numeric | | |
| data_gap | | |
| tool | | |
| macro family | | |
| micro overall | | |

What would be hidden if only overall success were reported?


## 8. Release conclusion

Choose one:

```text
GO
CONDITIONAL GO
NO-GO
NO OFFICIAL DECISION — INCOMPLETE EXPERIMENT
```

### Formal conclusion


### Provisional system conclusion


### Required next action


## 9. What this evaluation does NOT prove

- 
- 
- 

## 10. 90-second interview answer

Explain how you designed the metric system, what denominator traps you found, and why protocol completeness matters.
