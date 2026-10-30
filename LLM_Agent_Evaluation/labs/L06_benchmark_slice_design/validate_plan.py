import csv
import json
import sys
from pathlib import Path

REQUIRED_TOP = [
    "claim", "target_population", "unit_of_evaluation",
    "representative", "diagnostic", "split_policy", "interpretation_boundary"
]


def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def load_ids(pool_path):
    with open(pool_path, newline="", encoding="utf-8") as f:
        return {r["task_id"] for r in csv.DictReader(f)}


def nonempty_text(obj, key):
    return isinstance(obj.get(key), str) and obj[key].strip() != ""


def main():
    plan_path = Path(sys.argv[1] if len(sys.argv) > 1 else "benchmark_plan.json")
    base = plan_path.parent
    pool_path = base / "task_pool.csv"

    if not plan_path.exists():
        fail(f"missing {plan_path}")
    if not pool_path.exists():
        fail(f"missing {pool_path}")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    for key in REQUIRED_TOP:
        if key not in plan:
            fail(f"missing top-level field: {key}")

    for key in ["claim", "target_population", "unit_of_evaluation"]:
        if not nonempty_text(plan, key):
            fail(f"{key} must be non-empty text")

    known_ids = load_ids(pool_path)

    for section in ["representative", "diagnostic"]:
        obj = plan.get(section)
        if not isinstance(obj, dict):
            fail(f"{section} must be an object")

        ids = obj.get("task_ids")
        if not isinstance(ids, list) or not ids:
            fail(f"{section}.task_ids must be a non-empty list")
        if len(ids) != len(set(ids)):
            fail(f"{section}.task_ids contains duplicates")

        unknown = sorted(set(ids) - known_ids)
        if unknown:
            fail(f"{section} contains unknown task ids: {unknown}")

        if not nonempty_text(obj, "aggregation"):
            fail(f"{section}.aggregation must be non-empty")
        if not nonempty_text(obj, "interpretation"):
            fail(f"{section}.interpretation must be non-empty")

    overlap = sorted(
        set(plan["representative"]["task_ids"])
        & set(plan["diagnostic"]["task_ids"])
    )
    if overlap:
        fail(f"same task ids used in both views: {overlap}")

    split_policy = plan.get("split_policy", {})
    for key in ["group_disjoint_within_set", "group_disjoint_across_sets"]:
        if not isinstance(split_policy.get(key), bool):
            fail(f"split_policy.{key} must be boolean")

    if not nonempty_text(split_policy, "template_overlap_policy"):
        fail("split_policy.template_overlap_policy must be non-empty")

    boundary = plan.get("interpretation_boundary", {})
    for key in ["representative_supports", "diagnostic_supports", "does_not_support"]:
        if not nonempty_text(boundary, key):
            fail(f"interpretation_boundary.{key} must be non-empty")

    print("PASS: benchmark plan is structurally complete")
    print(
        "NOTE: structural validity does not prove sampling, leakage, "
        "or benchmark semantics are correct."
    )


if __name__ == "__main__":
    main()
