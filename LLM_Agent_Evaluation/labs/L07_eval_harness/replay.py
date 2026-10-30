from __future__ import annotations
import argparse, json
from pathlib import Path
from harness_lib import load_json, load_tasks, load_matrix, simulate, canonical_result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    run = Path(args.run_dir)
    config = load_json(run / "config_snapshot.json")
    contract = load_json(here / "harness_contract.json")
    tasks = load_tasks(here / "tasks.jsonl")
    matrix = load_matrix(here / "fixtures" / "scenario_matrix.csv")

    recorded = {}
    for line in (run / "results.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            recorded[(r["task_id"], r["repeat_id"])] = r

    mismatches = []
    checked = 0
    for key, old in sorted(recorded.items()):
        task_id, repeat_id = key
        row = matrix[(task_id, repeat_id, config["variant"])]
        new, _ = simulate(tasks[task_id], row, contract)
        checked += 1
        if canonical_result(old) != canonical_result(new):
            mismatches.append({"task_id": task_id, "repeat_id": repeat_id})

    report = {
        "run_id": load_json(run / "manifest.json")["run_id"],
        "match_mode": "exact_contract_fields",
        "checked": checked,
        "matched": checked - len(mismatches),
        "replay_match_rate": (checked - len(mismatches)) / checked if checked else 0.0,
        "mismatches": mismatches,
    }
    (run / "replay_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if not mismatches else 1)


if __name__ == "__main__":
    main()
