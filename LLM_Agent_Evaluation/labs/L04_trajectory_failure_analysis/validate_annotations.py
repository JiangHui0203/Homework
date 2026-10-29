#!/usr/bin/env python3
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
trace_path = ROOT / "trajectory_cases.jsonl"
ann_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "annotations.csv"

episodes = {}
with trace_path.open(encoding="utf-8") as f:
    for line in f:
        if line.strip():
            e = json.loads(line)
            episodes[e["episode_id"]] = e

if not ann_path.exists():
    print(f"ERROR: {ann_path} not found")
    print("Copy annotations_starter.csv to annotations.csv and complete it first.")
    raise SystemExit(2)

with ann_path.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

by_id = {r["episode_id"]: r for r in rows}
errors = []
allowed_status = {"FAILURE_REVIEWED", "NO_EPISODE_FAILURE"}
allowed_evidence = {"OBSERVED", "SUPPORTED", "HYPOTHESIS"}

for eid, ep in episodes.items():
    row = by_id.get(eid)
    if row is None:
        errors.append(f"{eid}: missing annotation row")
        continue
    status = row.get("review_status", "").strip()
    if status not in allowed_status:
        errors.append(f"{eid}: review_status must be FAILURE_REVIEWED or NO_EPISODE_FAILURE")
        continue
    episode_failed = ep["final_outcome"] in {"FAILURE", "FALSE_ACCEPT"}
    if episode_failed and status != "FAILURE_REVIEWED":
        errors.append(f"{eid}: failed episode must be FAILURE_REVIEWED")
    if status == "FAILURE_REVIEWED":
        required = [
            "symptom", "first_meaningful_failure_event", "primary_failure_label",
            "immediate_mechanism", "root_cause_hypothesis", "evidence_level",
            "owner", "regression_candidate"
        ]
        for key in required:
            if not row.get(key, "").strip():
                errors.append(f"{eid}: missing {key}")
        ev = row.get("evidence_level", "").strip()
        if ev and ev not in allowed_evidence:
            errors.append(f"{eid}: evidence_level must be OBSERVED/SUPPORTED/HYPOTHESIS")

extra = sorted(set(by_id) - set(episodes))
for eid in extra:
    errors.append(f"{eid}: annotation row has no matching episode")

if errors:
    print("ANNOTATION CONTRACT: FAIL")
    for err in errors:
        print("-", err)
    raise SystemExit(1)

print("ANNOTATION CONTRACT: PASS")
print(f"episodes={len(episodes)} reviewed_rows={len(rows)}")
print("Structural validation only; causal correctness still requires trace evidence.")
