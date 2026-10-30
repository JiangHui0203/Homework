from __future__ import annotations
import csv, hashlib, json, math, statistics
from pathlib import Path

TERMINAL_SUCCESS = {"VALID_SUCCESS", "CORRECT_SAFE_STOP"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text())


def load_tasks(path: Path):
    tasks = {}
    for line in path.read_text().splitlines():
        if line.strip():
            x = json.loads(line)
            tasks[x["task_id"]] = x
    return tasks


def load_matrix(path: Path):
    rows = {}
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            key = (row["task_id"], int(row["repeat_id"]), row["variant"])
            row["repeat_id"] = int(row["repeat_id"])
            row["tokens"] = int(row["tokens"])
            row["latency_ms"] = int(row["latency_ms"])
            row["tool_calls"] = int(row["tool_calls"])
            row["retries"] = int(row["retries"])
            rows[key] = row
    return rows


def expected_events(task, row):
    events = [
        {"step": 0, "type": "TASK_START", "status": "OK"},
        {"step": 1, "type": "PLAN", "status": "OK"},
    ]
    fault = task["fault"]
    if fault != "none":
        events.append({"step": len(events), "type": "FAULT_INJECTED", "status": fault.upper()})
    if row["retries"] > 0:
        events.append({"step": len(events), "type": "RECOVERY_ATTEMPT", "status": "RETRY"})
    if row["tool_calls"] > 0:
        events.append({"step": len(events), "type": "TOOL_EXECUTION", "status": "DONE"})
    events.append({"step": len(events), "type": "TERMINAL", "status": row["outcome"]})
    return events


def simulate(task, row, contract):
    budget = contract["budget"]
    budget_violation = (
        row["tokens"] > budget["max_tokens_per_run"]
        or row["tool_calls"] > budget["max_tool_calls"]
        or row["retries"] > budget["max_retries"]
    )
    valid_success = row["outcome"] in TERMINAL_SUCCESS
    critical_invalid = bool(task["critical"] and not valid_success)
    result = {
        "task_id": task["task_id"],
        "family": task["family"],
        "critical": task["critical"],
        "fault": task["fault"],
        "repeat_id": row["repeat_id"],
        "variant": row["variant"],
        "outcome": row["outcome"],
        "valid_success": valid_success,
        "critical_invalid": critical_invalid,
        "tokens": row["tokens"],
        "latency_ms": row["latency_ms"],
        "tool_calls": row["tool_calls"],
        "retries": row["retries"],
        "budget_violation": budget_violation,
        "note": row["note"],
    }
    return result, expected_events(task, row)


def percentile_nearest_rank(values, q):
    if not values:
        return None
    vals = sorted(values)
    rank = max(1, math.ceil(q * len(vals)))
    return vals[rank - 1]


def summarize(results, planned):
    completed = len(results)
    successes = sum(r["valid_success"] for r in results)
    critical_invalid = sum(r["critical_invalid"] for r in results)
    budget_violations = sum(r["budget_violation"] for r in results)
    tokens = sum(r["tokens"] for r in results)
    latencies = [r["latency_ms"] for r in results]
    by_task = {}
    for r in results:
        by_task.setdefault(r["task_id"], []).append(bool(r["valid_success"]))
    stable = sum(len(set(v)) == 1 for v in by_task.values())
    return {
        "planned_runs": planned,
        "completed_runs": completed,
        "artifact_completeness": completed / planned if planned else 0.0,
        "valid_successes": successes,
        "success_rate": successes / completed if completed else 0.0,
        "critical_invalid_outcomes": critical_invalid,
        "total_tokens": tokens,
        "tokens_per_valid_success": tokens / successes if successes else None,
        "p50_latency_ms": statistics.median(latencies) if latencies else None,
        "p95_latency_ms": percentile_nearest_rank(latencies, 0.95),
        "repeat_consistency": stable / len(by_task) if by_task else 0.0,
        "flaky_task_count": len(by_task) - stable,
        "budget_violations": budget_violations,
    }


def canonical_result(r):
    keys = [
        "task_id", "family", "critical", "fault", "repeat_id", "variant", "outcome",
        "valid_success", "critical_invalid", "tokens", "latency_ms", "tool_calls",
        "retries", "budget_violation", "note"
    ]
    return {k: r[k] for k in keys}
