# Part 7 — Eval Engineering

## 核心问题

如何把一次性实验变成可复现、可审计、可回放、可持续运行的 Evaluation System？

## 计划主题

- Eval Harness Architecture
- Task / Result / Trace Schemas
- Fixtures / Mocks / Fault Injection
- Replay & Determinism
- Tracing & Observability
- Cost / Latency / Throughput
- CI Gates & Regression Testing
- Artifacts / Manifests / Reproducibility
- Human-Machine Review Workflow

## VeriAgent Lens

VeriAgent 的 structured traces、manifest/hash、challenge evaluation、fault injection 与 frozen runs 是主要案例来源，但本库不复制实现代码。