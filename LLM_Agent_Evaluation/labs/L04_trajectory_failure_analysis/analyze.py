#!/usr/bin/env python3
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
trace_path = ROOT / "trajectory_cases.jsonl"
ann_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "annotations.csv"

episodes = []
with trace_path.open(encoding="utf-8") as f:
    for line in f:
        if line.strip():
            episodes.append(json.loads(line))

VALID = {"VALID_SUCCESS", "CORRECT_SAFE_STOP"}

def ok(ep):
    return ep["final_outcome"] in VALID

print("== Frozen trajectory summary ==")
versions = sorted({e["version"] for e in episodes})
for version in versions:
    xs = [e for e in episodes if e["version"] == version]
    passed = sum(ok(e) for e in xs)
    print(f"{version:10s}: {passed}/{len(xs)} = {passed/len(xs):.1%}")

print("\n== Paired outcome movement ==")
by_task = defaultdict(dict)
for e in episodes:
    by_task[e["task_id"]][e["version"]] = e
wins = losses = ties_good = ties_bad = 0
for task_id in sorted(by_task):
    pair = by_task[task_id]
    b = ok(pair["baseline"])
    c = ok(pair["candidate"])
    if (not b) and c:
        tag = "WIN"; wins += 1
    elif b and (not c):
        tag = "LOSS"; losses += 1
    elif b and c:
        tag = "BOTH_OK"; ties_good += 1
    else:
        tag = "BOTH_FAIL"; ties_bad += 1
    print(f"{task_id}: baseline={pair['baseline']['final_outcome']:<18s} candidate={pair['candidate']['final_outcome']:<18s} {tag}")
print(f"wins={wins} losses={losses} both_ok={ties_good} both_fail={ties_bad} net={wins-losses:+d}/{len(by_task)}")

print("\n== Success by slice ==")
slices = sorted({e["slice"] for e in episodes})
for s in slices:
    parts = []
    for version in versions:
        xs = [e for e in episodes if e["slice"] == s and e["version"] == version]
        if xs:
            parts.append(f"{version}={sum(ok(e) for e in xs)}/{len(xs)}")
    print(f"{s:24s} " + " ".join(parts))

failed = [e for e in episodes if not ok(e)]
print("\n== Episode-level failures requiring review ==")
print(", ".join(e["episode_id"] for e in failed))

if not ann_path.exists():
    print(f"\nNo {ann_path.name} found. Complete annotations first to get failure-label aggregation.")
    raise SystemExit(0)

with ann_path.open(encoding="utf-8", newline="") as f:
    anns = list(csv.DictReader(f))
reviewed = [r for r in anns if r.get("review_status", "").strip() == "FAILURE_REVIEWED"]
print("\n== Your reviewed failure labels ==")
labels = Counter(r["primary_failure_label"].strip() for r in reviewed if r["primary_failure_label"].strip())
evidence = Counter(r["evidence_level"].strip() for r in reviewed if r["evidence_level"].strip())
owners = Counter(r["owner"].strip() for r in reviewed if r["owner"].strip())
print("labels:", dict(labels))
print("evidence:", dict(evidence))
print("owners:", dict(owners))

print("\n== Regression candidates from your annotations ==")
for r in reviewed:
    if r.get("regression_candidate", "").strip().lower() in {"yes", "y", "true", "1"}:
        print(f"{r['episode_id']}: {r['primary_failure_label']} @ {r['first_meaningful_failure_event']}")

print("\nReminder: slice association and label counts are diagnostic evidence, not causal proof.")
