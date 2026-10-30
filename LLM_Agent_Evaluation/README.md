# LLM / Agent Evaluation Knowledge System

> 面向长期学习、技术面试、真实评测工作与 VeriAgent 实验的个人 Evaluation Knowledge System。

## 目标

这不是资料收藏夹，也不是重新编写一套完整 CS / ML 教材。目标是建立一套能够长期维护、反复调用的评测知识系统：

1. 补齐 LLM / Agent Evaluation 所需的最小完备基础；
2. 系统掌握 LLM Eval、LLM-as-a-Judge、Agent Eval、Trajectory Evaluation、Failure Analysis、Benchmark、统计实验设计与 Eval Engineering；
3. 建立类似 Hot100 的“母题 → Pattern → 实战 → 复盘 → 面试”体系；
4. 与 `JiangHui0203/veriagent` 持续联动，但不复制其源代码；
5. 将稳定理论、当前实现案例和冻结实验严格分层。

## 四个主要入口

- [`CORE_QUESTIONS.md`](./CORE_QUESTIONS.md)：决定“必须真正掌握什么”。
- [`EVAL_PATTERNS.md`](./EVAL_PATTERNS.md)：决定“遇到这类评测问题应该想到什么方法”。
- [`METRICS.md`](./METRICS.md) / [`BENCHMARKS.md`](./BENCHMARKS.md) / [`FAILURE_TAXONOMY.md`](./FAILURE_TAXONOMY.md)：实际工作检索入口。
- [`INTERVIEW_INDEX.md`](./INTERVIEW_INDEX.md)：把知识转换成可口述、可追问、可举例的面试能力。

治理 / release 状态：[`V1_COMPLETION_AUDIT.md`](./V1_COMPLETION_AUDIT.md)。

建议学习循环：

```text
核心母题 → 最小理论 → Pattern → Lab / VeriAgent case → 失败复盘 → 面试表达 → 掌握度更新
```

## 三层知识结构

```text
Layer 1  Stable Theory
         长期稳定的评测概念、方法、统计与工程原则

Layer 2  VeriAgent Current Case
         当前实现如何体现这些原则；允许随项目演化

Layer 3  Frozen Experiment
         绑定日期 / commit / protocol / artifacts 的历史实验；冻结后不覆盖
```

## 知识地图

| Part | 主题 | 核心问题 |
|---|---|---|
| 0 | Foundations | 为了做 Eval，我最低限度必须懂什么？ |
| 1 | LLM Evaluation | 如何定义并测量模型输出质量？ |
| 2 | Grader / LLM-as-a-Judge | 谁来打分，评分本身是否可靠？ |
| 3 | Agent Evaluation | 如何评价有状态、有工具、有环境交互的 Agent？ |
| 4 | Trajectory & Failure Analysis | 错在哪里、为什么错、第一处关键失败在哪里？ |
| 5 | Benchmark & Evaluation Data | 用什么任务、数据和切片来测？ |
| 6 | Statistics & Experiment Design | 观察到的提升是否可信？ |
| 7 | Eval Engineering | 如何把评测变成可复现、可回放、可持续运行的工程系统？ |
| 8 | Data Flywheel / Post-training | 如何把 Eval 结果安全地反馈到数据与训练闭环？ |

## Part 目录

- [`00_Foundations/`](./00_Foundations/)
- [`01_LLM_Evaluation/`](./01_LLM_Evaluation/)
- [`02_Grader_and_LLM_as_a_Judge/`](./02_Grader_and_LLM_as_a_Judge/)
- [`03_Agent_Evaluation/`](./03_Agent_Evaluation/)
- [`04_Trajectory_and_Failure_Analysis/`](./04_Trajectory_and_Failure_Analysis/)
- [`05_Benchmark_and_Evaluation_Data/`](./05_Benchmark_and_Evaluation_Data/)
- [`06_Statistics_and_Experiment_Design/`](./06_Statistics_and_Experiment_Design/)
- [`07_Eval_Engineering/`](./07_Eval_Engineering/)
- [`08_Data_Flywheel_and_Post_Training/`](./08_Data_Flywheel_and_Post_Training/)

## 实战入口

- [`cases/veriagent/`](./cases/veriagent/)：VeriAgent 贯穿案例。
- [`labs/`](./labs/)：可独立完成的练习与小实验。
- [`templates/`](./templates/)：所有文档类型的统一模板。

## 与现有知识库的边界

本库不是 `LLM_Agent_Data` 的重写版。概念的 canonical owner 由 [`SOURCE_OF_TRUTH.md`](./SOURCE_OF_TRUTH.md) 决定。

简化原则：

```text
LLM_Agent_Data
= 经验 / 数据 / 学习信号如何进入 Learning System

LLM_Agent_Evaluation
= 如何定义、测量、比较、诊断并证明系统表现

veriagent
= 真实代码、运行时、trace 与实验产物
```

若已有概念在其他知识库完整定义，本库只保留必要摘要、Evaluation 视角和 canonical link。

## 状态约定

知识重要性与个人掌握度分开维护：

- `M1`：核心母题，必须能够独立设计并 defend。
- `M2`：高频扩展，必须理解并能应用。
- `M3`：检索型知识，知道何时需要以及去哪里查。

掌握度：`S0 未学习` → `S1 能识别` → `S2 能解释` → `S3 能设计/实现` → `S4 能诊断、比较并 defend`。

当前阶段：**V1 Release Candidate**。28/28 个 M1 已有正式正文，L01–L08 已建立；V1 Complete 仍需补齐 Q05/Q06，并至少建立一个 VeriAgent Current Case。完整结论与下一阶段顺序见 [`V1_COMPLETION_AUDIT.md`](./V1_COMPLETION_AUDIT.md)。
