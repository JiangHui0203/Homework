from __future__ import annotations
import argparse, json
from pathlib import Path
from harness_lib import load_json


def check(name, passed, value, rule):
    return {"name": name, "passed": bool(passed), "value": value, "rule": rule}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline-dir", required=True)
    ap.add_argument("--candidate-dir", required=True)
    args = ap.parse_args()

    here = Path(__file__).resolve().parent
    contract = load_json(here / "harness_contract.json")
    g = contract["gate"]
    bdir = Path(args.baseline_dir)
    cdir = Path(args.candidate_dir)
    b = load_json(bdir / "summary.json")
    c = load_json(cdir / "summary.json")
    replay_path = cdir / "replay_report.json"
    replay = load_json(replay_path) if replay_path.exists() else {"replay_match_rate": 0.0}

    delta_pp = 100 * (c["success_rate"] - b["success_rate"])
    checks = [
        check("artifact_completeness", c["artifact_completeness"] >= g["artifact_completeness"], c["artifact_completeness"], f">= {g['artifact_completeness']}"),
        check("critical_invalid_outcomes", c["critical_invalid_outcomes"] == g["critical_invalid_outcomes"], c["critical_invalid_outcomes"], f"= {g['critical_invalid_outcomes']}"),
        check("success_noninferiority", delta_pp >= g["candidate_success_noninferiority_pp"], delta_pp, f">= {g['candidate_success_noninferiority_pp']} pp"),
        check("repeat_consistency", c["repeat_consistency"] >= g["candidate_repeat_consistency_min"], c["repeat_consistency"], f">= {g['candidate_repeat_consistency_min']}"),
        check("tokens_per_valid_success", c["tokens_per_valid_success"] <= g["candidate_tokens_per_valid_success_max"], c["tokens_per_valid_success"], f"<= {g['candidate_tokens_per_valid_success_max']}"),
        check("p95_latency_ms", c["p95_latency_ms"] <= g["candidate_p95_latency_ms_max"], c["p95_latency_ms"], f"<= {g['candidate_p95_latency_ms_max']}"),
        check("budget_violations", c["budget_violations"] == g["budget_violations"], c["budget_violations"], f"= {g['budget_violations']}"),
        check("replay_match_rate", replay["replay_match_rate"] >= g["replay_match_rate"], replay["replay_match_rate"], f">= {g['replay_match_rate']}"),
    ]
    decision = "GO" if all(x["passed"] for x in checks) else "NO-GO"
    report = {
        "baseline_run": load_json(bdir / "manifest.json")["run_id"],
        "candidate_run": load_json(cdir / "manifest.json")["run_id"],
        "success_delta_pp": delta_pp,
        "checks": checks,
        "decision": decision,
    }
    (cdir / "gate_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if decision == "GO" else 2)


if __name__ == "__main__":
    main()
