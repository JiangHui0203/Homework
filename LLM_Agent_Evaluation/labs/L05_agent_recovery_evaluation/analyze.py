#!/usr/bin/env python3
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
with (ROOT / "recovery_episodes.csv").open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
policy = json.loads((ROOT / "recovery_policy.json").read_text(encoding="utf-8"))

def i(row, key):
    return int(row[key])

def ratio(a, b):
    return a / b if b else float("nan")

n = len(rows)
valid = sum(i(r, "valid_success") for r in rows)
first_pass = sum(r["final_state"] == "FIRST_PASS_SUCCESS" for r in rows)
opps = [r for r in rows if i(r, "recovery_opportunity") == 1]
attempts = [r for r in opps if i(r, "attempted_recovery") == 1]
recovered = [r for r in opps if r["final_state"] == "RECOVERED_SUCCESS"]
safe_required = [r for r in rows if r["expected_policy"] == "safe_stop"]
correct_stops = [r for r in safe_required if r["final_state"] == "CORRECT_SAFE_STOP"]
all_safe_stops = [r for r in rows if "SAFE_STOP" in r["final_state"]]
false_recovery = [r for r in rows if r["final_state"] == "FALSE_RECOVERY"]

violations = []
max_attempts = policy["max_recovery_attempts"]
for r in rows:
    if r["expected_policy"] == "recover":
        if i(r, "attempted_recovery") == 0:
            violations.append((r["episode_id"], "missed_recovery_attempt"))
        if i(r, "attempts_count") > max_attempts:
            violations.append((r["episode_id"], "retry_budget_exceeded"))
    elif r["expected_policy"] == "safe_stop" and i(r, "attempted_recovery") == 1:
        violations.append((r["episode_id"], "retried_when_safe_stop_required"))

avg_extra_tokens = sum(i(r, "tokens_total") - i(r, "tokens_before_fault") for r in recovered) / len(recovered)
avg_extra_latency = sum(i(r, "latency_ms") - i(r, "latency_before_fault_ms") for r in recovered) / len(recovered)
tokens_per_success = sum(i(r, "tokens_total") for r in rows) / valid

metrics = {
    "final_valid_success_rate": ratio(valid, n),
    "first_pass_success_rate": ratio(first_pass, n),
    "recovery_opportunity_rate": ratio(len(opps), n),
    "recovery_attempt_given_opportunity": ratio(len(attempts), len(opps)),
    "recovery_success_given_opportunity": ratio(len(recovered), len(opps)),
    "recovery_success_given_attempt": ratio(len(recovered), len(attempts)),
    "safe_stop_precision": ratio(len(correct_stops), len(all_safe_stops)),
    "safe_stop_recall": ratio(len(correct_stops), len(safe_required)),
    "tokens_per_valid_success": tokens_per_success,
}

print("== Recovery-aware metrics ==")
for k, v in metrics.items():
    if "tokens" in k:
        print(f"{k:38s} {v:.1f}")
    else:
        print(f"{k:38s} {v:.1%}")
print(f"{'avg_extra_tokens_per_recovered_success':38s} {avg_extra_tokens:.1f}")
print(f"{'avg_extra_latency_ms_per_recovered_success':38s} {avg_extra_latency:.1f}")
print(f"{'false_recovery_count':38s} {len(false_recovery)}")
print(f"{'control_policy_violation_count':38s} {len(violations)}")

print("\n== Control-policy violations ==")
for eid, reason in violations:
    print(f"{eid}: {reason}")

print("\n== Release gates ==")
g = policy["release_gates"]
checks = [
    ("Final valid success", metrics["final_valid_success_rate"] >= g["final_valid_success_rate_min"], metrics["final_valid_success_rate"], g["final_valid_success_rate_min"], ">="),
    ("Recovery success | opportunity", metrics["recovery_success_given_opportunity"] >= g["recovery_success_given_opportunity_min"], metrics["recovery_success_given_opportunity"], g["recovery_success_given_opportunity_min"], ">="),
    ("Safe-stop precision", metrics["safe_stop_precision"] >= g["safe_stop_precision_min"], metrics["safe_stop_precision"], g["safe_stop_precision_min"], ">="),
    ("Safe-stop recall", metrics["safe_stop_recall"] >= g["safe_stop_recall_min"], metrics["safe_stop_recall"], g["safe_stop_recall_min"], ">="),
    ("Control policy violations", len(violations) <= g["control_policy_violations_max"], len(violations), g["control_policy_violations_max"], "<="),
    ("False recovery", len(false_recovery) <= g["false_recovery_max"], len(false_recovery), g["false_recovery_max"], "<="),
    ("Tokens / valid success", metrics["tokens_per_valid_success"] <= g["tokens_per_valid_success_max"], metrics["tokens_per_valid_success"], g["tokens_per_valid_success_max"], "<="),
]
for name, passed, value, threshold, op in checks:
    if isinstance(value, float) and value <= 1:
        val = f"{value:.1%}"; thr = f"{threshold:.1%}"
    elif isinstance(value, float):
        val = f"{value:.1f}"; thr = f"{threshold:.1f}"
    else:
        val, thr = str(value), str(threshold)
    print(f"{name:31s} {val:>8s} {op} {thr:<8s} {'PASS' if passed else 'FAIL'}")

print("\nFINAL:", "GO" if all(x[1] for x in checks) else "NO-GO")
print("Do not collapse this conclusion into final success rate alone.")
