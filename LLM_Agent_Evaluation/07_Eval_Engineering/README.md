# Part 7 — Eval Engineering

## 核心问题

如何把一次性实验变成**可复现、可审计、可回放、可持续运行**的 Evaluation System？

## 已建立

- [02 Reproducible Eval Harness](02_Reproducible_Eval_Harness.md) — Q31：artifact / version / trace / manifest / completeness
- [03 Replay / Fixture / Mock / Fault Injection](03_Replay_Fixture_Mock_and_Fault_Injection.md) — Q32：failure reproduction 与 determinism envelope
- [04 CI Regression Gates & Flakiness](04_CI_Regression_Gates_and_Flakiness.md) — Q33：hard gate、stochastic gate、rerun policy、quarantine
- [05 Multidimensional Eval Reporting](05_Multidimensional_Eval_Reporting.md) — Q34：quality / reliability / cost / latency / stability / budget scorecard

## 学习顺序

```text
Q31 先定义：一次 Eval 要留下哪些可审计证据？
 ↓
Q32 再解决：失败如何被稳定 replay / fixture / fault injection？
 ↓
Q33 再工程化：哪些证据能进入 CI gate，flaky 怎么治理？
 ↓
Q34 最后决策：多维指标怎样联合成 release decision？
```

## 四个必须形成条件反射的边界

```text
Runner
≠ Eval Harness

Replay reproduced
≠ Root cause proven

Rerun until pass
≠ Flakiness management

Higher accuracy
≠ Better deployed system
```

## 最小 Eval Harness Contract

```text
Task / Benchmark manifest
System config snapshot
Environment / tool snapshot
Execution trace
Raw result
Evaluator artifact
Metric summary
Artifact hashes
Run completeness state
Replay / validation report
Gate decision
```

## 推荐工程分层

```text
Layer 1 — deterministic contracts
Layer 2 — stable regression fixtures
Layer 3 — small paired smoke eval
Layer 4 — scheduled larger benchmark
Layer 5 — fresh / rotating confirmation
```

越靠前越适合 PR hard gate；越靠后越适合 release / scheduled evidence。

## 与其它 Parts 的关系

- Part 1 定义 Evaluation / Metric Contract；
- Part 3 定义 tool / state / recovery / long-horizon observability；
- Part 4 把 failure 提炼成 regression asset；
- Part 5 提供 frozen / regression / hard / fresh benchmark portfolio；
- Part 6 决定 paired comparison、uncertainty 与 stochastic gate 的解释；
- Part 7 把这些 contract 落成 artifact、replay 和 CI workflow。

## 实践

- [L07 Eval Harness](../labs/L07_eval_harness/README.md)：纯离线最小 harness，真正生成 manifest、config snapshot、results、structured traces、hashes，支持 artifact validation、exact replay 与 release gate。

## VeriAgent Lens

VeriAgent 的 structured traces、manifest/hash、challenge evaluation、failure replay 与 frozen runs 是本 Part 的主要真实案例来源，但本库不复制实现代码。

当前最值得抽象的工程原则是：

```text
frozen inputs
+ explicit run status
+ structured traces
+ immutable-ish artifacts
+ replayable evidence
+ scorecard / gate
```

而不是某个具体目录结构。
