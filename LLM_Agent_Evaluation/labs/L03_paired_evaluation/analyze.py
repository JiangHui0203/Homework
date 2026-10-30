import csv
import itertools
import json
import math
import random
from collections import defaultdict

DATA_FILE = "paired_runs.csv"
CONTRACT_FILE = "experiment_contract.json"


def quantile(values, p):
    values = sorted(values)
    x = (len(values) - 1) * p
    lo = math.floor(x)
    hi = math.ceil(x)
    if lo == hi:
        return values[lo]
    return values[lo] * (hi - x) + values[hi] * (x - lo)


def pct(x):
    return f"{100*x:.1f}%"


def pp(x):
    return f"{100*x:+.2f} pp"


with open(CONTRACT_FILE, encoding="utf-8") as f:
    contract = json.load(f)

with open(DATA_FILE, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

required = {
    "task_id",
    "slice",
    "repeat_id",
    "baseline_success",
    "candidate_success",
    "seed",
}
missing = required - set(rows[0])
if missing:
    raise SystemExit(f"Missing columns: {sorted(missing)}")

by_task = defaultdict(list)
for row in rows:
    by_task[row["task_id"]].append(row)

n_tasks = len(by_task)
n_pairs = len(rows)
expected_tasks = contract["design"]["n_tasks"]
expected_repeats = contract["design"]["repeats_per_task"]

if n_tasks != expected_tasks:
    raise SystemExit(f"Expected {expected_tasks} tasks, got {n_tasks}")

for task_id, task_rows in by_task.items():
    if len(task_rows) != expected_repeats:
        raise SystemExit(
            f"{task_id}: expected {expected_repeats} repeats, got {len(task_rows)}"
        )

baseline_total = sum(int(row["baseline_success"]) for row in rows)
candidate_total = sum(int(row["candidate_success"]) for row in rows)
baseline_run_rate = baseline_total / n_pairs
candidate_run_rate = candidate_total / n_pairs

task_stats = {}
for task_id, task_rows in sorted(by_task.items()):
    baseline = sum(int(row["baseline_success"]) for row in task_rows) / len(task_rows)
    candidate = sum(int(row["candidate_success"]) for row in task_rows) / len(task_rows)
    task_stats[task_id] = {
        "slice": task_rows[0]["slice"],
        "baseline": baseline,
        "candidate": candidate,
        "diff": candidate - baseline,
    }

task_diffs = [value["diff"] for value in task_stats.values()]
effect = sum(task_diffs) / n_tasks
wins = [task_id for task_id, value in task_stats.items() if value["diff"] > 1e-12]
losses = [task_id for task_id, value in task_stats.items() if value["diff"] < -1e-12]
ties = [task_id for task_id, value in task_stats.items() if abs(value["diff"]) <= 1e-12]

# Task-level bootstrap: resample tasks, not run rows.
bootstrap_cfg = contract["bootstrap"]
rng = random.Random(bootstrap_cfg["seed"])
task_ids = list(task_stats)
bootstrap_effects = []
for _ in range(bootstrap_cfg["iterations"]):
    sampled = [rng.choice(task_ids) for _ in task_ids]
    bootstrap_effects.append(
        sum(task_stats[task_id]["diff"] for task_id in sampled) / n_tasks
    )

alpha = 1 - bootstrap_cfg["confidence_level"]
ci_low = quantile(bootstrap_effects, alpha / 2)
ci_high = quantile(bootstrap_effects, 1 - alpha / 2)

# Exact task-level sign-flip permutation on non-zero paired task differences.
nonzero_diffs = [diff for diff in task_diffs if abs(diff) > 1e-12]
permutation_stats = []
for signs in itertools.product((-1, 1), repeat=len(nonzero_diffs)):
    stat = sum(sign * diff for sign, diff in zip(signs, nonzero_diffs)) / n_tasks
    permutation_stats.append(stat)

p_two_sided = (
    sum(abs(stat) >= abs(effect) - 1e-12 for stat in permutation_stats)
    / len(permutation_stats)
)

slice_tasks = defaultdict(list)
for task_id, value in task_stats.items():
    slice_tasks[value["slice"]].append(value)

unstable_baseline = []
unstable_candidate = []
for task_id, task_rows in sorted(by_task.items()):
    baseline_values = [int(row["baseline_success"]) for row in task_rows]
    candidate_values = [int(row["candidate_success"]) for row in task_rows]
    if len(set(baseline_values)) > 1:
        unstable_baseline.append(task_id)
    if len(set(candidate_values)) > 1:
        unstable_candidate.append(task_id)

print("== DESIGN ==")
print(f"Distinct tasks: {n_tasks}")
print(f"Paired run rows: {n_pairs}")
print(f"Repeats per task: {expected_repeats}")
print(f"Primary unit: {contract['design']['primary_unit']}")
print(f"Nested unit: {contract['design']['nested_unit']}")
print()

print("== RAW / TASK-LEVEL EFFECT ==")
print(f"Baseline run accuracy:  {baseline_total}/{n_pairs} = {pct(baseline_run_rate)}")
print(f"Candidate run accuracy: {candidate_total}/{n_pairs} = {pct(candidate_run_rate)}")
print(f"Raw delta: {pp(candidate_run_rate - baseline_run_rate)}")
print(f"Task-averaged paired delta: {pp(effect)}")
print(f"Task wins / losses / ties: {len(wins)} / {len(losses)} / {len(ties)}")
print(f"Wins: {', '.join(wins) or '-'}")
print(f"Losses: {', '.join(losses) or '-'}")
print()

print("== UNCERTAINTY ==")
print(
    f"{int(100*bootstrap_cfg['confidence_level'])}% task-bootstrap CI: "
    f"[{pp(ci_low)}, {pp(ci_high)}]"
)
print(f"Exact two-sided task sign-flip permutation p: {p_two_sided:.3f}")
print(
    f"Minimum practical effect: "
    f"{contract['decision']['minimum_practical_effect_pp']:+.1f} pp"
)
print()

print("== SLICES (EXPLORATORY) ==")
for slice_name in contract["multiplicity"]["exploratory_slices"]:
    values = slice_tasks[slice_name]
    baseline = sum(value["baseline"] for value in values) / len(values)
    candidate = sum(value["candidate"] for value in values) / len(values)
    print(
        f"{slice_name:10s} n={len(values):2d}  "
        f"baseline={pct(baseline):>6s} candidate={pct(candidate):>6s} "
        f"delta={pp(candidate-baseline):>10s}"
    )
print(
    "These slice results are exploratory; selecting the best slice after inspection "
    "is not confirmatory evidence."
)
print()

print("== REPEAT / SAMPLE-SIZE AUDIT ==")
print(
    f"Baseline unstable tasks: {len(unstable_baseline)}/{n_tasks} -> "
    f"{', '.join(unstable_baseline)}"
)
print(
    f"Candidate unstable tasks: {len(unstable_candidate)}/{n_tasks} -> "
    f"{', '.join(unstable_candidate)}"
)
print(
    "36 run rows are execution observations, not 36 independent tasks for the "
    "primary future-task claim."
)
print()

credible = (
    ci_low > 0
    and 100 * effect >= contract["decision"]["minimum_practical_effect_pp"]
)

print("== EVIDENCE STATEMENT ==")
if credible:
    print("Supported improvement under the frozen teaching rule.")
else:
    print(
        "INCONCLUSIVE / insufficient evidence for a stable practically meaningful "
        "improvement."
    )
    print("Do not interpret CI crossing 0 as proof of equivalence.")
