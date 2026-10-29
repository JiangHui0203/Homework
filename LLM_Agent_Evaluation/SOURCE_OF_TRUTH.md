# Source of Truth & Ownership Rules

本文件定义 `LLM_Agent_Evaluation` 与 Homework 现有知识体系、VeriAgent 之间的内容所有权，优先级高于局部文档的临时写法。

## 1. Canonical Owner 原则

同一稳定概念只保留一个 canonical owner。其他文档可以做必要摘要、建立索引、增加新的分析视角，但不并行维护第二套完整定义。

| 主题 | Canonical owner | 本库职责 |
|---|---|---|
| Data objects / learning signals | `LLM_Agent_Data` | 引用；解释它们如何成为 eval object / signal |
| Agent trajectory anatomy | `LLM_Agent_Data` | 引用；重点写 trajectory measurement 与 diagnosis |
| Agent failure taxonomy 的完整概念定义 | `LLM_Agent_Data` | 建 detection / metric / slice / debugging 索引 |
| Grader / Verifier / Judge 的数据系统视角 | `LLM_Agent_Data` | 深入 reliability、calibration、agreement 与 operational use |
| Benchmark 基础概念 | `LLM_Agent_Data` | 深入 eval set construction、leakage、slice、regression set |
| Data flywheel / governance / data experiments | `LLM_Agent_Data` | 只维护 Eval → Data/Post-training 接口 |
| Evaluation contract / estimand / metric design | `LLM_Agent_Evaluation` | 本库 canonical owner |
| Judge calibration / evaluator reliability | `LLM_Agent_Evaluation` | 本库 canonical owner |
| Agent evaluation methodology | `LLM_Agent_Evaluation` | 本库 canonical owner |
| Applied statistics for Eval | `LLM_Agent_Evaluation` | 本库 canonical owner |
| Eval harness / replay / regression gates | `LLM_Agent_Evaluation` | 本库 canonical owner |
| VeriAgent 源代码与运行时行为 | `JiangHui0203/veriagent` | 只引用，不复制实现 |
| 某次 VeriAgent 冻结实验的解释 | 本库 frozen case | 绑定 commit / protocol / artifacts |

现有数据母库入口：[`../LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)。

## 2. 三层 VeriAgent 规则

### Layer 1 — Stable Theory

不得依赖某个临时代码路径、某个模型版本或某次实验结果。目标是几年后仍然成立。

### Layer 2 — Current Case

记录“当前 VeriAgent 如何实现/体现某个评测原则”。必须包含：

- `last_reviewed`；
- 当前实现 pointer；
- current behavior；
- known limitations；
- 哪些变化会使文档过期。

Current case 可以更新。

### Layer 3 — Frozen Experiment

必须绑定：

- 日期；
- VeriAgent commit SHA；
- task / data manifest；
- model / environment；
- protocol；
- metrics；
- artifacts；
- uncertainty / limitations。

冻结后不覆盖旧结果。新实验创建新条目，旧实验最多增加 `Superseded by`。

## 3. 避免重复建设的硬规则

1. **先查 owner，再写正文。**
2. 已在 canonical owner 中完整定义的概念，本库默认只保留 2–5 句最小摘要 + 链接 + Evaluation interpretation。
3. 禁止从 VeriAgent 复制大段源代码进入 Homework。
4. Benchmark 定义与某次 benchmark score 分离。
5. Metric 定义与某次 threshold / release gate 分离。
6. Current case 与 frozen experiment 分离。
7. 负结果、无显著提升、成本变差等结果必须保留，不只收录成功案例。

## 4. Promotion 规则

新内容默认进入最局部 owner。只有同时满足以下条件才提升为稳定知识：

- 跨至少两个案例仍成立；
- 不是某个当前实现细节；
- 能写出清晰适用条件与反例；
- 能映射到一个 CORE_QUESTION 或 EVAL_PATTERN。

否则留在 current case / frozen experiment / lab。

## 5. 变更审计

每季度或结构明显扩张后检查：

- 是否出现重复定义；
- 是否存在没有 owner 的概念；
- Current case 是否与 VeriAgent 漂移；
- frozen experiment 是否被新结果覆盖；
- M1 是否只有理论没有实战；
- 是否出现只为“完整”而加入、但 Evaluation 不需要的基础知识。