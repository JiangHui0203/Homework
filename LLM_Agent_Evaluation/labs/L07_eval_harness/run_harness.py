from __future__ import annotations
import argparse, json, shutil
from pathlib import Path
from harness_lib import load_json, load_tasks, load_matrix, simulate, summarize, sha256_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["baseline", "candidate"], required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    contract_path = here / "harness_contract.json"
    tasks_path = here / "tasks.jsonl"
    matrix_path = here / "fixtures" / "scenario_matrix.csv"
    contract = load_json(contract_path)
    tasks = load_tasks(tasks_path)
    matrix = load_matrix(matrix_path)

    out = Path(args.out)
    if out.exists():
        shutil.rmtree(out)
    (out / "traces").mkdir(parents=True)

    snapshot = {
        "schema_version": contract["schema_version"],
        "benchmark_id": contract["benchmark_id"],
        "variant": args.variant,
        "seed": contract["seed"],
        "repeats": contract["repeats"],
        "evaluator_version": contract["evaluator_version"],
        "budget": contract["budget"],
        "source_hashes": {
            "harness_contract.json": sha256_file(contract_path),
            "tasks.jsonl": sha256_file(tasks_path),
            "fixtures/scenario_matrix.csv": sha256_file(matrix_path),
        },
    }
    (out / "config_snapshot.json").write_text(json.dumps(snapshot, indent=2) + "\n")

    results = []
    for task_id, task in tasks.items():
        for repeat_id in range(1, contract["repeats"] + 1):
            row = matrix[(task_id, repeat_id, args.variant)]
            result, events = simulate(task, row, contract)
            results.append(result)
            trace = {
                "trace_schema_version": contract["trace_schema_version"],
                "task_id": task_id,
                "repeat_id": repeat_id,
                "variant": args.variant,
                "events": events,
            }
            trace_path = out / "traces" / f"{task_id}_r{repeat_id:02d}.json"
            trace_path.write_text(json.dumps(trace, indent=2) + "\n")

    with (out / "results.jsonl").open("w") as f:
        for r in results:
            f.write(json.dumps(r, sort_keys=True) + "\n")

    planned = len(tasks) * contract["repeats"]
    summary = summarize(results, planned)
    summary["variant"] = args.variant
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    artifact_paths = [
        out / "config_snapshot.json",
        out / "results.jsonl",
        out / "summary.json",
        *sorted((out / "traces").glob("*.json")),
    ]
    manifest = {
        "run_id": f"{contract['benchmark_id']}__{args.variant}__seed{contract['seed']}",
        "status": "COMPLETED" if summary["artifact_completeness"] == 1.0 else "INCOMPLETE",
        "benchmark_id": contract["benchmark_id"],
        "variant": args.variant,
        "planned_runs": planned,
        "completed_runs": len(results),
        "artifacts": {
            str(p.relative_to(out)): sha256_file(p)
            for p in artifact_paths
        },
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
