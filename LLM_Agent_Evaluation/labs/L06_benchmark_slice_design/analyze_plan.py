import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def load_pool(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows, {r["task_id"]: r for r in rows}


def pct(x):
    return f"{100 * x:.1f}%"


def print_counts(title, counter, order=None):
    print(title)
    keys = order or sorted(counter)
    for key in keys:
        print(f"  {key:20s} {counter.get(key, 0)}")


def tv_distance(observed, target):
    keys = set(observed) | set(target)
    return 0.5 * sum(
        abs(observed.get(k, 0.0) - target.get(k, 0.0)) for k in keys
    )


def main():
    plan_path = Path(sys.argv[1] if len(sys.argv) > 1 else "benchmark_plan.json")
    base = plan_path.parent
    pool_path = base / "task_pool.csv"
    contract_path = base / "benchmark_contract.json"

    rows, by_id = load_pool(pool_path)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    contract = json.loads(contract_path.read_text(encoding="utf-8"))

    blocked_status = set(contract["eligibility"]["blocked_exposure_statuses"])
    exposed_groups = {
        r["group_id"] for r in rows if r["exposure_status"] in blocked_status
    }

    directly_blocked = [r for r in rows if r["exposure_status"] in blocked_status]
    group_blocked_clean = [
        r for r in rows
        if r["exposure_status"] not in blocked_status
        and r["group_id"] in exposed_groups
    ]
    ref_bad = [r for r in rows if r["reference_verified"] != "1"]
    disc_bad = [r for r in rows if r["discriminative_check"] != "1"]

    def eligible(row):
        return (
            row["exposure_status"] not in blocked_status
            and row["group_id"] not in exposed_groups
            and row["reference_verified"] == "1"
            and row["discriminative_check"] == "1"
        )

    eligible_rows = [r for r in rows if eligible(r)]

    print("== Pool audit ==")
    print(f"pool size: {len(rows)}")
    print(f"direct exposure blockers: {len(directly_blocked)}")
    print(f"clean rows blocked by exposed group: {len(group_blocked_clean)}")
    print(f"reference-not-verified rows: {len(ref_bad)}")
    print(f"non-discriminative rows: {len(disc_bad)}")
    print(f"fully eligible rows: {len(eligible_rows)}")

    selected_by_section = {}
    blocker_total = 0

    for section in ["representative", "diagnostic"]:
        ids = plan[section]["task_ids"]
        selected = [by_id[i] for i in ids]
        selected_by_section[section] = selected

        print(f"\n== {section.title()} set ==")
        print(f"n={len(selected)}")

        capabilities = Counter(r["capability"] for r in selected)
        difficulties = Counter(r["difficulty"] for r in selected)
        risks = Counter(r["risk"] for r in selected)

        print_counts(
            "capability counts:",
            capabilities,
            list(contract["capabilities"]),
        )
        print_counts("difficulty counts:", difficulties)
        print_counts("risk counts:", risks)

        bad_direct = [
            r["task_id"] for r in selected
            if r["exposure_status"] in blocked_status
        ]
        bad_group = [
            r["task_id"] for r in selected
            if r["group_id"] in exposed_groups
        ]
        bad_ref = [
            r["task_id"] for r in selected
            if r["reference_verified"] != "1"
        ]
        bad_disc = [
            r["task_id"] for r in selected
            if r["discriminative_check"] != "1"
        ]

        group_counts = Counter(r["group_id"] for r in selected)
        duplicate_groups = sorted(
            group for group, count in group_counts.items() if count > 1
        )

        section_blockers = {
            "direct_exposure": bad_direct,
            "contaminated_group": bad_group,
            "reference": bad_ref,
            "discrimination": bad_disc,
            "duplicate_group": duplicate_groups,
        }

        for name, values in section_blockers.items():
            if values:
                print(f"BLOCKER {name}: {values}")
                blocker_total += len(values)

        historical = [float(r["historical_pass_rate"]) for r in selected]
        ceiling = contract["pilot_zone"]["ceiling_threshold"]
        floor = contract["pilot_zone"]["floor_threshold"]
        ceiling_n = sum(value >= ceiling for value in historical)
        floor_n = sum(value <= floor for value in historical)
        mid_n = len(historical) - ceiling_n - floor_n
        print(f"pilot zones: ceiling={ceiling_n}, mid={mid_n}, floor={floor_n}")

    representative = selected_by_section["representative"]
    capability_order = list(contract["capabilities"])
    rep_counts = Counter(r["capability"] for r in representative)
    rep_observed = {
        capability: rep_counts[capability] / len(representative)
        for capability in capability_order
    }
    target = {
        capability: contract["capabilities"][capability]["population_weight"]
        for capability in capability_order
    }
    tv = tv_distance(rep_observed, target)

    print("\n== Representative distribution ==")
    for capability in capability_order:
        print(
            f"  {capability:20s} "
            f"observed={pct(rep_observed[capability])} "
            f"target={pct(target[capability])}"
        )

    print(f"total variation distance: {tv:.3f}")
    max_tv = contract["representative_set"]["max_total_variation_distance"]
    print(
        f"distribution gate <= {max_tv:.3f}: "
        f"{'PASS' if tv <= max_tv else 'FAIL'}"
    )

    rep_target_counts = {
        capability: contract["capabilities"][capability]["representative_target"]
        for capability in capability_order
    }
    rep_quota_ok = all(
        rep_counts[capability] == rep_target_counts[capability]
        for capability in capability_order
    )
    print(f"representative quota match: {'PASS' if rep_quota_ok else 'FAIL'}")

    weight_sum = 0.0
    print("implied per-task weights:")
    for capability in capability_order:
        n = rep_counts[capability]
        weight = target[capability] / n if n else 0.0
        weight_sum += weight * n
        print(f"  {capability:20s} {weight:.5f} per selected task")
    print(f"weight sum: {weight_sum:.3f}")

    diagnostic = selected_by_section["diagnostic"]
    diag_counts = Counter(r["capability"] for r in diagnostic)
    diag_target = {
        capability: contract["capabilities"][capability]["diagnostic_target"]
        for capability in capability_order
    }
    diag_quota_ok = all(
        diag_counts[capability] == diag_target[capability]
        for capability in capability_order
    )

    high_risk_n = sum(
        r["risk"] in {"high", "critical"} for r in diagnostic
    )
    min_high = contract["diagnostic_set"]["min_high_or_critical_risk_items"]

    print("\n== Diagnostic coverage ==")
    print(f"equal capability quota: {'PASS' if diag_quota_ok else 'FAIL'}")
    print(
        f"high/critical risk items: {high_risk_n}/{len(diagnostic)} "
        f"({'PASS' if high_risk_n >= min_high else 'FAIL'}, min={min_high})"
    )

    difficulty_by_capability = defaultdict(set)
    for row in diagnostic:
        difficulty_by_capability[row["capability"]].add(row["difficulty"])

    difficulty_ok = True
    for capability in capability_order:
        values = difficulty_by_capability[capability]
        has_medium = "medium" in values
        has_hardish = bool(values & {"hard", "adversarial"})
        ok = has_medium and has_hardish
        difficulty_ok &= ok
        print(
            f"  {capability:20s} difficulties={sorted(values)} "
            f"{'PASS' if ok else 'FAIL'}"
        )

    print(
        f"diagnostic difficulty coverage: "
        f"{'PASS' if difficulty_ok else 'FAIL'}"
    )

    print("\n== Cross-set audit ==")
    rep_groups = {r["group_id"] for r in representative}
    diag_groups = {r["group_id"] for r in diagnostic}
    rep_templates = {r["template_id"] for r in representative}
    diag_templates = {r["template_id"] for r in diagnostic}

    group_overlap = sorted(rep_groups & diag_groups)
    template_overlap = sorted(rep_templates & diag_templates)

    if group_overlap:
        blocker_total += len(group_overlap)
        print(f"BLOCKER group overlap: {group_overlap}")
    else:
        print("group overlap: none")

    print(
        "template overlap (warning only): "
        f"{template_overlap if template_overlap else 'none'}"
    )

    size_ok = (
        len(representative) == contract["representative_set"]["size"]
        and len(diagnostic) == contract["diagnostic_set"]["size"]
    )

    print("\n== Plan verdict ==")
    print(f"size contract: {'PASS' if size_ok else 'FAIL'}")
    print(f"hard blockers: {blocker_total}")

    all_ok = (
        size_ok
        and blocker_total == 0
        and rep_quota_ok
        and tv <= max_tv
        and diag_quota_ok
        and difficulty_ok
        and high_risk_n >= min_high
    )

    print(f"benchmark design checks: {'PASS' if all_ok else 'FAIL'}")
    print(
        "NOTE: PASS means this synthetic lab contract is satisfied; "
        "it does not prove real-world representativeness or generalization."
    )


if __name__ == "__main__":
    main()
