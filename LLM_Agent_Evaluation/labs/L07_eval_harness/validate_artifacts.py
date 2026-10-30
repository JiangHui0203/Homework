from __future__ import annotations
import argparse, json
from pathlib import Path
from harness_lib import load_json, sha256_file


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    args = ap.parse_args()
    run = Path(args.run_dir)
    manifest = load_json(run / "manifest.json")
    errors = []

    for rel, expected in manifest["artifacts"].items():
        path = run / rel
        if not path.exists():
            errors.append(f"missing artifact: {rel}")
        elif sha256_file(path) != expected:
            errors.append(f"hash mismatch: {rel}")

    summary = load_json(run / "summary.json")
    if manifest["completed_runs"] != summary["completed_runs"]:
        errors.append("manifest/summary completed_runs mismatch")
    if manifest["status"] == "COMPLETED" and summary["artifact_completeness"] != 1.0:
        errors.append("COMPLETED run is not complete")

    trace_count = len(list((run / "traces").glob("*.json")))
    if trace_count != summary["completed_runs"]:
        errors.append(f"trace count {trace_count} != completed {summary['completed_runs']}")

    report = {
        "run_id": manifest["run_id"],
        "passed": not errors,
        "checked_artifacts": len(manifest["artifacts"]),
        "errors": errors,
    }
    (run / "validation_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
