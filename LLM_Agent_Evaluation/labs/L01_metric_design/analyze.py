#!/usr/bin/env python3
"""Reference analysis for L01 Metric Design Lab.

Uses Python standard library only. The output follows the frozen protocol in README.md.
It produces provisional diagnostics when infrastructure aborts exist.
"""

import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).with_name("runs.csv")


def pct(num, den):
    if den == 0:
        return "NA"
    return f"{100.0 * num / den:.1f}%"


def nearest_rank(values, p):
    if not values:
        return None
    ordered = sorted(values)
    rank = max(1, math.ceil(p * len(ordered)))
    return ordered[rank - 1]


def as_int(value):
    if value is None or value == "":
        return None
    return int(value)


def main():
    with DATA.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    scheduled = len(rows)
    evaluable = [r for r in rows if r["infra_status"] == "ok"]
    infra_aborts = [r for r in rows if r["infra_status"] != "ok"]

    for r in evaluable:
        r["correct"] = as_int(r["correct"])
        r["runtime_accept"] = as_int(r["runtime_accept"])
        r["recovery_opportunity"] = as_int(r["recovery_opportunity"])
        r["tokens"] = as_int(r["tokens"])
        r["latency_ms"] = as_int(r["latency_ms"])

    successes = [r for r in evaluable if r["correct"] == 1]
    incorrect = [r for r in evaluable if r["correct"] == 0]
    accepted = [r for r in evaluable if r["runtime_accept"] == 1]
    accepted_correct = [r for r in accepted if r["correct"] == 1]
    false_accepts = [r for r in incorrect if r["runtime_accept"] == 1]

    safe_stop = [r for r in evaluable if r["expected_behavior"] == "safe_stop"]
    safe_stop_success = [r for r in safe_stop if r["correct"] == 1]

    recovery = [r for r in evaluable if r["recovery_opportunity"] == 1]
    recovery_success = [r for r in recovery if r["correct"] == 1]

    total_tokens = sum(r["tokens"] for r in evaluable)
    failure_tokens = sum(r["tokens"] for r in incorrect)
    latencies = [r["latency_ms"] for r in evaluable]

    family = defaultdict(lambda: [0, 0])
    for r in evaluable:
        family[r["family"]][1] += 1
        family[r["family"]][0] += r["correct"]

    family_rates = {
        key: good / total for key, (good, total) in family.items()
    }
    macro_family = sum(family_rates.values()) / len(family_rates)

    completeness = len(evaluable) / scheduled
    task_success = len(successes) / len(evaluable)
    accepted_accuracy = len(accepted_correct) / len(accepted)
    false_accept_conditional = len(false_accepts) / len(incorrect)
    false_accept_all = len(false_accepts) / len(evaluable)
    safe_stop_rate = len(safe_stop_success) / len(safe_stop)
    recovery_rate = len(recovery_success) / len(recovery)
    tokens_per_success = total_tokens / len(successes)
    failure_token_share = failure_tokens / total_tokens
    p50 = statistics.median(latencies)
    p95 = nearest_rank(latencies, 0.95)

    print("L01 Metric Design — reference diagnostics")
    print("=" * 48)
    print(f"Scheduled runs:       {scheduled}")
    print(f"Evaluable runs:       {len(evaluable)}")
    print(f"Infrastructure abort: {len(infra_aborts)}")
    print(f"Completeness:         {pct(len(evaluable), scheduled)}")
    print()

    if infra_aborts:
        print("OFFICIAL STATUS: INCOMPLETE / ABORTED")
        print("Release score is not valid until aborted tasks are rerun.")
        print("Numbers below are PROVISIONAL diagnostics only.\n")
    else:
        print("OFFICIAL STATUS: COMPLETE\n")

    print("Outcome / reliability")
    print(f"Task Success Rate:            {len(successes)}/{len(evaluable)} = {pct(len(successes), len(evaluable))}")
    print(f"Accepted Output Accuracy:     {len(accepted_correct)}/{len(accepted)} = {pct(len(accepted_correct), len(accepted))}")
    print(f"False Accept Rate | incorrect:{len(false_accepts)}/{len(incorrect)} = {pct(len(false_accepts), len(incorrect))}")
    print(f"False Accept / all evaluable: {len(false_accepts)}/{len(evaluable)} = {pct(len(false_accepts), len(evaluable))}")
    print(f"Safe Stop Success Rate:       {len(safe_stop_success)}/{len(safe_stop)} = {pct(len(safe_stop_success), len(safe_stop))}")
    print(f"Recovery Success Rate:        {len(recovery_success)}/{len(recovery)} = {pct(len(recovery_success), len(recovery))}")
    print()

    print("Cost / latency")
    print(f"Total evaluable tokens:       {total_tokens}")
    print(f"Tokens per Valid Success:     {tokens_per_success:.1f}")
    print(f"Failure token share:          {pct(failure_tokens, total_tokens)}")
    print(f"End-to-End P50 latency:       {p50:.0f} ms")
    print(f"End-to-End P95 latency:       {p95} ms")
    print()

    print("Success slices")
    for key in sorted(family):
        good, total = family[key]
        print(f"{key:10s}: {good}/{total} = {pct(good, total)}")
    print(f"Macro family success:         {macro_family * 100:.1f}%")
    print(f"Micro overall success:        {task_success * 100:.1f}%")
    print()

    gates = [
        ("Experiment completeness = 100%", completeness == 1.0),
        ("Task Success Rate >= 75%", task_success >= 0.75),
        ("False Accept Rate = 0%", false_accept_conditional == 0.0),
        ("Safe Stop Success Rate >= 90%", safe_stop_rate >= 0.90),
        ("Recovery Success Rate >= 70%", recovery_rate >= 0.70),
        ("Tokens per Valid Success <= 1800", tokens_per_success <= 1800),
        ("P95 latency <= 4500 ms", p95 <= 4500),
    ]

    print("Pre-registered gates")
    for name, passed in gates:
        print(f"{'PASS' if passed else 'FAIL':4s}  {name}")

    print("\nREFERENCE CONCLUSION")
    if infra_aborts:
        print("No official release decision: the evaluation round is incomplete.")
    if not all(passed for _, passed in gates):
        print("Even provisionally, the candidate fails one or more release gates.")
        print("Operational recommendation: NO-GO pending rerun and system fixes.")
    else:
        print("All provisional gates pass; complete the frozen reruns before release.")


if __name__ == "__main__":
    main()
