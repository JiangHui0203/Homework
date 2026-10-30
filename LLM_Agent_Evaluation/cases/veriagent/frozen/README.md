# VeriAgent — Frozen Experiments

每个冻结实验独立保存，不覆盖历史结果。

推荐命名：

```text
YYYY-MM-DD_<short-experiment-name>.md
```

必须使用 `templates/FROZEN_EXPERIMENT.md` 的字段语义，绑定 commit、protocol、data/task manifest、metrics、artifacts 与 limitations。

冻结实验回答的是：

> “当时按该协议观察到了什么？”

而不是永久的项目当前状态。

## Registered frozen experiments

- [**2026-10-26 — Olist Challenge Candidate Memory v1**](2026-10-26_challenge_candidate_memory_v1.md)
  - real VeriAgent experiment, not synthetic;
  - reviewed dev failures → two-rule SQL-stage candidate memory;
  - held-out paired test `29/36 → 30/36`;
  - stage-level attribution failed because all observed held-out failures occurred before the intervention stage;
  - candidate retained as evidence but not promoted to default memory.
- [Machine-readable evidence manifest](2026-10-26_challenge_candidate_memory_v1.manifest.json)

## Audit rule

Frozen cases must distinguish:

```text
Git-verifiable provenance
vs
local / external raw artifacts
```

Do not claim raw-artifact reproducibility when the source repository only freezes a summary or pointer.

For the 2026-10-26 case, use:

```text
../../labs/L08_veriagent_frozen_case/audit_case.py
```

to check internal consistency and optional pinned Git provenance.
