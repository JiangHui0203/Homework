#!/usr/bin/env python3
"""L02 LLM Judge Calibration Lab — standard-library-only analysis."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POINTWISE = ROOT / "pointwise_scores.csv"
PAIRWISE = ROOT / "pairwise_trials.csv"


def read_csv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def pct(x: float) -> str:
    return f"{100.0 * x:.1f}%"


def mean(values):
    values = list(values)
    return sum(values) / len(values) if values else float("nan")


def by(rows, key):
    groups = defaultdict(list)
    for row in rows:
        groups[row[key]].append(row)
    return dict(sorted(groups.items()))


def swap_to_canonical(raw: str) -> str:
    return {"FIRST": "B", "SECOND": "A", "TIE": "TIE"}[raw]


def pointwise_metrics(rows):
    n = len(rows)
    gold = [int(r["human_gold"]) for r in rows]
    j1 = [int(r["judge_r1"]) for r in rows]
    j2 = [int(r["judge_r2"]) for r in rows]
    h1 = [int(r["human_r1"]) for r in rows]
    h2 = [int(r["human_r2"]) for r in rows]
    return {
        "n": n,
        "judge_human_exact": mean(a == b for a, b in zip(j1, gold)),
        "judge_human_within1": mean(abs(a - b) <= 1 for a, b in zip(j1, gold)),
        "judge_human_mae": mean(abs(a - b) for a, b in zip(j1, gold)),
        "critical_disagreement": mean(abs(a - b) >= 2 for a, b in zip(j1, gold)),
        "judge_repeat_exact": mean(a == b for a, b in zip(j1, j2)),
        "human_human_exact": mean(a == b for a, b in zip(h1, h2)),
    }


def pairwise_metrics(rows):
    n = len(rows)
    swap_canonical = [swap_to_canonical(r["judge_ba_raw"]) for r in rows]
    return {
        "n": n,
        "judge_human_accuracy": mean(r["judge_ab_r1"] == r["human_gold"] for r in rows),
        "judge_repeat_consistency": mean(r["judge_ab_r1"] == r["judge_ab_r2"] for r in rows),
        "swap_consistency": mean(r["judge_ab_r1"] == swapped for r, swapped in zip(rows, swap_canonical)),
        "swapped_accuracy": mean(r["human_gold"] == swapped for r, swapped in zip(rows, swap_canonical)),
        "human_human_exact": mean(r["human_r1"] == r["human_r2"] for r in rows),
    }


def print_pointwise(rows):
    m = pointwise_metrics(rows)
    print("== Pointwise calibration ==")
    print(f"N                         : {m['n']}")
    print(f"Judge↔Human exact         : {pct(m['judge_human_exact'])}")
    print(f"Judge↔Human within ±1     : {pct(m['judge_human_within1'])}")
    print(f"Judge↔Human MAE           : {m['judge_human_mae']:.3f}")
    print(f"Critical disagreement ≥2  : {pct(m['critical_disagreement'])}")
    print(f"Judge repeat exact        : {pct(m['judge_repeat_exact'])}")
    print(f"Human↔Human exact         : {pct(m['human_human_exact'])}")
    print()
    for key in ("slice", "length_bucket", "style"):
        print(f"-- Pointwise slice: {key} --")
        for value, subset in by(rows, key).items():
            sm = pointwise_metrics(subset)
            print(f"{value:12s} n={sm['n']:2d}  exact={pct(sm['judge_human_exact']):>6s}  MAE={sm['judge_human_mae']:.3f}  critical={pct(sm['critical_disagreement']):>6s}")
        print()


def print_pairwise(rows):
    m = pairwise_metrics(rows)
    print("== Pairwise calibration ==")
    print(f"N                         : {m['n']}")
    print(f"Judge↔Human accuracy      : {pct(m['judge_human_accuracy'])}")
    print(f"Judge repeat consistency  : {pct(m['judge_repeat_consistency'])}")
    print(f"Swap consistency          : {pct(m['swap_consistency'])}")
    print(f"Accuracy after swap       : {pct(m['swapped_accuracy'])}")
    print(f"Human↔Human exact         : {pct(m['human_human_exact'])}")
    print()
    print("-- Pairwise slice: task family --")
    for value, subset in by(rows, "slice").items():
        sm = pairwise_metrics(subset)
        print(f"{value:12s} n={sm['n']:2d}  acc={pct(sm['judge_human_accuracy']):>6s}  repeat={pct(sm['judge_repeat_consistency']):>6s}  swap={pct(sm['swap_consistency']):>6s}")
    print()
    print("-- Bias probes --")
    probes = [("length_relation", "B_more_verbose", "verbosity"), ("style_relation", "B_more_polished", "style/polish"), ("judge_family_match", "B", "family-match")]
    for key, value, name in probes:
        subset = [r for r in rows if r[key] == value]
        judge_b = mean(r["judge_ab_r1"] == "B" for r in subset)
        human_b = mean(r["human_gold"] == "B" for r in subset)
        print(f"{name:12s} n={len(subset):2d}  Judge chooses B={pct(judge_b):>6s}  Human gold B={pct(human_b):>6s}  gap={100*(judge_b-human_b):+.1f} pp")
    print()


def print_release_gates(point_rows, pair_rows):
    pm = pointwise_metrics(point_rows)
    qm = pairwise_metrics(pair_rows)
    style_pairs = [r for r in pair_rows if r["slice"] == "style"]
    verbose_pairs = [r for r in pair_rows if r["length_relation"] == "B_more_verbose"]
    verbose_gap = mean(r["judge_ab_r1"] == "B" for r in verbose_pairs) - mean(r["human_gold"] == "B" for r in verbose_pairs)
    gates = [
        ("Pointwise within ±1 ≥ 90%", pm["judge_human_within1"] >= 0.90),
        ("Critical disagreement ≤ 2%", pm["critical_disagreement"] <= 0.02),
        ("Pairwise accuracy ≥ 80%", qm["judge_human_accuracy"] >= 0.80),
        ("Repeat consistency ≥ 95%", qm["judge_repeat_consistency"] >= 0.95),
        ("Swap consistency ≥ 95%", qm["swap_consistency"] >= 0.95),
        ("Style slice pairwise accuracy ≥ 70%", pairwise_metrics(style_pairs)["judge_human_accuracy"] >= 0.70),
        ("Verbose-preference gap ≤ 15 pp", abs(verbose_gap) <= 0.15),
    ]
    print("== Pre-registered release gates ==")
    failures = 0
    for name, passed in gates:
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        failures += not passed
    print(f"\nGate failures: {failures}/{len(gates)}")
    print("Do not let this script make the deployment decision for you. Write the final claim and allowed scope in REPORT_TEMPLATE.md.")


def main():
    point_rows = read_csv(POINTWISE)
    pair_rows = read_csv(PAIRWISE)
    print_pointwise(point_rows)
    print_pairwise(pair_rows)
    print_release_gates(point_rows, pair_rows)


if __name__ == "__main__":
    main()
