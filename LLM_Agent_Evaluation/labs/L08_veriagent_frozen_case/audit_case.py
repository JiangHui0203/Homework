#!/usr/bin/env python3
"""Audit the frozen L08 VeriAgent case pack.

Checks:
1) internal arithmetic / logic in the frozen manifest;
2) optional Git provenance against a local VeriAgent clone at the pinned commit;
3) optional existence of documented Git-ignored local run artifacts.

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = (
    HERE.parents[1]
    / "cases"
    / "veriagent"
    / "frozen"
    / "2026-10-26_challenge_candidate_memory_v1.manifest.json"
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def approx(actual: float, expected: float, tol: float = 1e-6) -> bool:
    return abs(actual - expected) <= tol


def audit_internal(m: dict) -> None:
    dev = m["development"]
    if dev["distinct_tasks"] * dev["repeats_per_task"] != dev["runs"]:
        fail("development run count does not equal tasks × repeats")

    test = m["heldout_test"]
    expected_per_condition = (
        test["distinct_tasks"] * test["repeats_per_task_per_condition"]
    )
    if expected_per_condition != test["runs_per_condition"]:
        fail("held-out run count per condition is inconsistent")

    if test["runs_per_condition"] * len(test["conditions"]) != test["total_task_runs"]:
        fail("held-out total task runs are inconsistent")

    paired = test["paired"]
    pair_total = (
        paired["wrong_to_right"]
        + paired["right_to_wrong"]
        + paired["both_right"]
        + paired["both_wrong"]
    )
    if pair_total != test["runs_per_condition"]:
        fail("paired outcome cells do not sum to runs per condition")

    observed_net = (
        test["candidate_memory_only"]["correct"] - test["no_memory"]["correct"]
    )
    paired_net = paired["wrong_to_right"] - paired["right_to_wrong"]
    if observed_net != paired_net or observed_net != paired["net_correct_runs"]:
        fail("aggregate correct delta and paired win/loss delta disagree")

    expected_pp = 100.0 * observed_net / test["runs_per_condition"]
    if not approx(expected_pp, paired["raw_delta_percentage_points"], 1e-8):
        fail("raw percentage-point delta is inconsistent")

    expected_token_delta = 100.0 * (
        test["candidate_memory_only"]["total_tokens"]
        / test["no_memory"]["total_tokens"]
        - 1.0
    )
    if not approx(expected_token_delta, test["cost_delta"]["total_tokens_percent"], 1e-8):
        fail("total-token delta is inconsistent")

    expected_tpc_delta = 100.0 * (
        test["candidate_memory_only"]["tokens_per_correct"]
        / test["no_memory"]["tokens_per_correct"]
        - 1.0
    )
    if not approx(
        expected_tpc_delta,
        test["cost_delta"]["tokens_per_correct_percent"],
        1e-8,
    ):
        fail("tokens-per-correct delta is inconsistent")

    retrieval = test["retrieval"]
    expected_hits = (
        retrieval["eligible_tasks"] * test["repeats_per_task_per_condition"]
    )
    if expected_hits != retrieval["potential_candidate_hits"]:
        fail("candidate retrieval opportunity count is inconsistent")

    if (
        retrieval["candidate_early_failures_before_sql"]
        + retrieval["candidate_runs_with_injection"]
        != retrieval["potential_candidate_hits"]
    ):
        fail("pre-SQL failures + injected runs do not cover eligible opportunities")

    attribution = m["attribution"]
    if attribution["observed_failures_total"] != attribution["failures_before_intervention_stage"]:
        fail("manifest no longer encodes the frozen attribution boundary: all failures pre-intervention")

    if m["decision"]["promotion"] != "DO_NOT_REPLACE_DEFAULT_MEMORY":
        fail("frozen promotion decision changed")

    print("CASE_CONSISTENCY PASS")


def git_show(repo: Path, commit: str, path: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), "show", f"{commit}:{path}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(
            f"cannot read {path} at {commit} from {repo}: "
            f"{proc.stderr.decode('utf-8', errors='replace').strip()}"
        )
    return proc.stdout


def audit_git_sources(m: dict, repo: Path) -> None:
    if not repo.exists():
        fail(f"VeriAgent root does not exist: {repo}")
    if not (repo / ".git").exists():
        fail(f"not a Git worktree/repository root: {repo}")

    commit = m["source_commit"]

    commit_check = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{commit}^{{commit}}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if commit_check.returncode != 0:
        fail(f"pinned commit {commit} is not available in the local repository")

    for item in m["git_verifiable_sources"]:
        data = git_show(repo, commit, item["path"])
        actual = git_blob_sha1(data)
        expected = item["git_blob_sha1"]
        if actual != expected:
            fail(
                f"Git blob mismatch for {item['path']}: "
                f"expected {expected}, got {actual}"
            )
        print(f"GIT_SOURCE PASS {item['path']} {actual}")

    print("GIT_SOURCE_PROVENANCE PASS")


def audit_local_artifacts(m: dict, repo: Path, require: bool) -> None:
    present = 0
    missing = []

    for item in m["documented_local_only_artifacts"]:
        path = repo / item["path"]
        if path.exists():
            present += 1
            print(f"LOCAL_ARTIFACT PRESENT {item['path']}")
        else:
            missing.append(item["path"])
            print(f"LOCAL_ARTIFACT MISSING {item['path']}")

    print(
        f"LOCAL_ARTIFACT_SUMMARY present={present} "
        f"missing={len(missing)} total={len(m['documented_local_only_artifacts'])}"
    )

    if require and missing:
        fail("required local-only run artifacts are missing")

    if missing and not require:
        print(
            "LOCAL_ARTIFACT_NOTE missing local/Git-ignored artifacts do not invalidate "
            "Git provenance; use --require-local-artifacts only in the original workspace."
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest",
        type=Path,
        default=DEFAULT_MANIFEST,
        help="Path to the frozen case manifest.",
    )
    parser.add_argument(
        "--veriagent-root",
        type=Path,
        default=None,
        help="Optional local VeriAgent repository root for pinned Git-source audit.",
    )
    parser.add_argument(
        "--require-local-artifacts",
        action="store_true",
        help="Fail if documented local/Git-ignored run artifacts are absent.",
    )
    args = parser.parse_args()

    if not args.manifest.exists():
        fail(f"manifest does not exist: {args.manifest}")

    with args.manifest.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    audit_internal(manifest)

    if args.require_local_artifacts and args.veriagent_root is None:
        fail("--require-local-artifacts requires --veriagent-root")

    if args.veriagent_root is not None:
        audit_git_sources(manifest, args.veriagent_root)
        audit_local_artifacts(
            manifest,
            args.veriagent_root,
            require=args.require_local_artifacts,
        )


if __name__ == "__main__":
    main()
