#!/usr/bin/env python3
"""Structural validator for the L01 metric contract.

This intentionally does NOT decide whether a denominator is scientifically correct.
It only checks whether required fields were explicitly filled.
"""

import json
import sys
from pathlib import Path

REQUIRED_TOP = [
    "evaluation_claim",
    "unit_of_analysis",
    "official_score_policy",
    "metrics",
    "release_gates",
]

REQUIRED_METRIC = [
    "id",
    "name",
    "question",
    "unit",
    "numerator",
    "denominator",
    "inclusion_rule",
    "aggregation",
    "failed_missing_handling",
    "direction",
    "interpretation_boundary",
]


def missing(value):
    return value is None or value == "" or value == [] or value == {}


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "metric_contract.json")
    if not path.exists():
        raise SystemExit(f"ERROR: {path} not found")

    data = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    warnings = []

    for key in REQUIRED_TOP:
        if key not in data or missing(data[key]):
            errors.append(f"missing top-level field: {key}")

    metrics = data.get("metrics", [])
    seen = set()
    for i, metric in enumerate(metrics, start=1):
        label = metric.get("id") or f"metric#{i}"
        if label in seen:
            errors.append(f"duplicate metric id: {label}")
        seen.add(label)

        for key in REQUIRED_METRIC:
            if key not in metric or missing(metric[key]):
                errors.append(f"{label}: missing field {key}")

        if "threshold" in metric:
            warnings.append(
                f"{label}: threshold found inside metric definition; keep release gates separate"
            )

    if len(metrics) < 8:
        errors.append(f"expected at least 8 metric cards, found {len(metrics)}")

    print(f"Contract: {path}")
    print(f"Metrics:  {len(metrics)}")

    if warnings:
        print("\nWARNINGS")
        for item in warnings:
            print(f"- {item}")

    if errors:
        print("\nFAILED")
        for item in errors:
            print(f"- {item}")
        raise SystemExit(1)

    print("\nPASS: contract is structurally complete")
    print("NOTE: structural completeness != scientific correctness")


if __name__ == "__main__":
    main()
