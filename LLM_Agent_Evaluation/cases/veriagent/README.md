# VeriAgent Casebook

VeriAgent 是本知识库的贯穿案例与实验环境，不是知识库本身。

Repository: `JiangHui0203/veriagent`

## 为什么适合作为 Evaluation 案例

VeriAgent 把 generation、verification、control、recovery 与 observability 显式分开，并保存结构化 trace；同时包含 ProofWriter reasoning runtime 与 Olist Data Agent 两种不同类型的系统。

## 三层映射

### Stable Theory

写在 Parts / Patterns / Metrics 中，不依赖项目版本。

### Current

见 [`current/`](./current/)：解释当前实现如何体现某个评测原则，只保存 pointer、行为、限制与 review date。

### Frozen

见 [`frozen/`](./frozen/)：保存带 commit / protocol / artifacts 的实验解释。

## 第一批建议案例

- Evaluation Architecture
- Trace & Observability
- Challenge Evaluation
- False Confidence / Wrong-answer Acceptance
- Recovery Evaluation
- Memory / Experience Paired Evaluation
- Reproducibility & Frozen Experiment

## 禁止事项

- 不复制大段 VeriAgent 源代码；
- 不把当前实现细节写成普遍理论；
- 不把“机制被调用”写成“能力提升”；
- 不用最新结果覆盖历史 frozen result。