# Core Questions

> Evaluation 版“核心母题”。这里决定哪些问题必须真正掌握，而不是记录所有可能的知识点。

## 分级规则

### M1 — Core Evaluation Question

达到 `S4` 时应能：

- 60–90 秒给出核心回答；
- 5 分钟展开设计；
- 明确 evaluation contract、metric / protocol 与主要 confounder；
- 给出至少一个反例或失败模式；
- 用真实项目或 VeriAgent 举例；
- 面对追问能解释 trade-off。

### M2 — 高频扩展

应能独立解释、知道何时使用、主要假设是什么，并能关联至少一个 M1。

### M3 — 检索型知识

知道它解决什么问题、属于知识图谱哪个位置，需要时能快速查回即可。

## 掌握度

- `S0`：未系统学习。
- `S1`：见过，能识别术语或问题形态。
- `S2`：能脱离笔记独立解释。
- `S3`：能完成实际设计 / 实现 / 分析。
- `S4`：能诊断反例、比较方案、处理追问并 defend。

> M1/M2/M3 是相对稳定的重要性；S0–S4 是个人当前状态，两者不得混用。

---

# V0 Master List

## A. Evaluation Contract & LLM Eval

- [ ] `M1 · S0` **[Q01](./01_LLM_Evaluation/01_Evaluation_Contract.md)**：一个 LLM / Agent 评测在开始跑模型之前，必须先定义哪些 evaluation contract？
- [ ] `M1 · S0` **[Q02](./06_Statistics_and_Experiment_Design/01_Estimand_and_Unit_of_Analysis.md)**：你到底在估计什么——task、run、sample、user 还是 trajectory？为什么 unit of analysis 选错会让结论失真？
- [ ] `M1 · S0` **[Q03](./01_LLM_Evaluation/02_What_Are_We_Measuring.md)**：最终答案正确率提高，为什么不一定意味着系统能力真的提高？
- [ ] `M1 · S0` **[Q04](./01_LLM_Evaluation/03_Metric_Design.md)**：一个 metric 应该怎样定义分子、分母、aggregation、失败运行和缺失值？
- [ ] `M2 · S0` **Q05**：reference-based 与 reference-free evaluation 各适合什么任务？
- [ ] `M2 · S0` **Q06**：开放式生成为什么很难只靠一个 automatic metric 评价？

## B. Grader / Verifier / LLM-as-a-Judge

- [ ] `M1 · S0` **[Q07](./02_Grader_and_LLM_as_a_Judge/01_Grader_Verifier_and_Judge.md)**：Grader、Verifier、LLM-as-a-Judge 分别解决什么问题，什么时候应该优先 deterministic verifier？
- [ ] `M1 · S0` **[Q08](./02_Grader_and_LLM_as_a_Judge/02_Judge_Reliability_and_Calibration.md)**：如何证明一个 LLM judge 本身足够可靠，而不是把 judge score 当作 ground truth？
- [ ] `M1 · S0` **[Q09](./02_Grader_and_LLM_as_a_Judge/03_Judge_Bias_and_Failure_Modes.md)**：position bias、verbosity bias、self-preference、style bias 会怎样污染 judge 结果，如何诊断？
- [ ] `M1 · S0` **[Q10](./02_Grader_and_LLM_as_a_Judge/04_Rubric_and_Scoring_Protocol.md)**：如何设计 rubric、pairwise / pointwise protocol 和 adjudication 流程？
- [ ] `M2 · S0` **[Q11](./02_Grader_and_LLM_as_a_Judge/05_Human_Disagreement_and_Adjudication.md)**：judge 与 human disagreement 应如何分析，而不是只报一个相关系数？

## C. Agent Evaluation

- [ ] `M1 · S0` **[Q12](./03_Agent_Evaluation/01_Agent_Evaluation_Contract.md)**：为什么 Agent 不能只看 final task success？一个最小完备 Agent Eval 应包含哪些层次？
- [ ] `M1 · S0` **[Q13](./03_Agent_Evaluation/02_Tool_Use_and_Grounding_Evaluation.md)**：如何评价 tool selection、tool arguments、tool result grounding 与 final answer 之间的正确性？
- [ ] `M1 · S0` **[Q14](./03_Agent_Evaluation/03_Recovery_and_Graceful_Degradation.md)**：如何评价 recovery / graceful degradation，而不是把所有非成功运行都压成 failure？
- [ ] `M1 · S0` **[Q15](./03_Agent_Evaluation/04_State_Memory_and_Leakage_Evaluation.md)**：有 memory / state 的 Agent 应如何避免状态泄漏、历史污染和非独立测试？
- [ ] `M2 · S0` **[Q16](./03_Agent_Evaluation/05_Long_Horizon_Agent_Evaluation.md)**：long-horizon Agent 为什么需要过程指标、阶段性检查点和预算指标？

## D. Trajectory & Failure Analysis

- [ ] `M1 · S0` **[Q17](./04_Trajectory_and_Failure_Analysis/01_First_Meaningful_Failure_and_Root_Cause.md)**：如何从一条 trajectory 中区分 symptom、first meaningful failure 和 root cause？
- [ ] `M1 · S0` **[Q18](./04_Trajectory_and_Failure_Analysis/02_Step_Outcome_and_Credit_Assignment.md)**：step-level correctness 与最终 outcome 应如何联合分析，避免错误 credit assignment？
- [ ] `M1 · S0` **[Q19](./04_Trajectory_and_Failure_Analysis/03_Slice_Based_Regression_Diagnosis.md)**：平均分变差时，如何用 slice 找出真正退化的能力，而不是盲目看总体指标？
- [ ] `M2 · S0` **[Q20](./04_Trajectory_and_Failure_Analysis/04_Failure_Taxonomy_as_Engineering_Asset.md)**：failure taxonomy 如何转化为可检测、可统计、可回归测试的工程资产？

## E. Benchmark & Eval Data

- [ ] `M1 · S0` **[Q21](./05_Benchmark_and_Evaluation_Data/01_Discriminative_Benchmark_Design.md)**：如何构造一个真正有区分度的 eval set，而不是简单收集一批题？
- [ ] `M1 · S0` **[Q22](./05_Benchmark_and_Evaluation_Data/02_Leakage_and_Test_Set_Overfitting.md)**：如何避免 benchmark leakage、test-set overfitting 和开发集反复调参造成的伪提升？
- [ ] `M1 · S0` **[Q23](./05_Benchmark_and_Evaluation_Data/03_Frozen_Regression_Hard_and_Rotating_Sets.md)**：为什么 frozen core、regression set、hard set / rotating set 应该分工不同？
- [ ] `M2 · S0` **[Q24](./05_Benchmark_and_Evaluation_Data/04_Coverage_Difficulty_and_Distribution_Tradeoffs.md)**：difficulty、coverage、slice balance 和 natural frequency 应如何权衡？

## F. Statistics & Experiment Design

- [ ] `M1 · S0` **[Q25](./06_Statistics_and_Experiment_Design/02_Is_the_Improvement_Credible.md)**：准确率从 70% 到 73%，你如何判断这 3 个点是否可信？
- [ ] `M1 · S0` **[Q26](./06_Statistics_and_Experiment_Design/03_Paired_Evaluation.md)**：什么时候应该使用 paired evaluation，为什么同题配对通常比两组独立平均更有力？
- [ ] `M1 · S0` **[Q27](./06_Statistics_and_Experiment_Design/04_Bootstrap_Permutation_and_Confidence_Intervals.md)**：bootstrap、permutation test、confidence interval 分别在 Eval 中回答什么问题？
- [ ] `M1 · S0` **[Q28](./06_Statistics_and_Experiment_Design/05_Task_Count_and_Repeats.md)**：LLM / Agent 存在随机性时，题目数量和重复次数应该怎样设计？
- [ ] `M2 · S0` **[Q29](./06_Statistics_and_Experiment_Design/06_Multiple_Comparisons_and_Adaptive_Analysis.md)**：多指标、多切片、多轮试验为什么会产生 multiple-comparison 问题？
- [ ] `M2 · S0` **[Q30](./06_Statistics_and_Experiment_Design/07_Correlation_Does_Not_Replace_Human_Judgment.md)**：相关性高是否意味着 evaluator 可替代 human judgment？

## G. Eval Engineering

- [ ] `M1 · S0` **[Q31](./07_Eval_Engineering/02_Reproducible_Eval_Harness.md)**：一个可复现的 eval harness 至少需要记录哪些 artifact、version、trace 和 configuration？
- [ ] `M1 · S0` **[Q32](./07_Eval_Engineering/03_Replay_Fixture_Mock_and_Fault_Injection.md)**：如何设计 replay、fixture、mock、fault injection，使 Agent failure 可以稳定复现？
- [ ] `M1 · S0` **[Q33](./07_Eval_Engineering/04_CI_Regression_Gates_and_Flakiness.md)**：如何把 offline eval 变成 CI regression gate，同时避免 flaky eval 阻塞开发？
- [ ] `M1 · S0` **[Q34](./07_Eval_Engineering/05_Multidimensional_Eval_Reporting.md)**：如何同时报告 quality、cost、latency、stability，而不是只优化单一准确率？

## H. Eval → Data / Post-training

- [ ] `M1 · S0` **[Q35](./08_Data_Flywheel_and_Post_Training/01_Failure_Promotion_to_Data_Flywheel.md)**：什么样的 failure 才值得进入 hard-case mining / data flywheel，而不是直接拿所有失败去训练？
- [ ] `M1 · S0` **[Q36](./08_Data_Flywheel_and_Post_Training/02_Post_Training_Causal_Validation.md)**：post-training 后如何证明改善来自目标能力，而不是 benchmark 记忆或评测协议漂移？
- [ ] `M2 · S0` **[Q37](./08_Data_Flywheel_and_Post_Training/03_Evaluator_Signal_to_Supervision.md)**：如何把 evaluator signal 转成 preference / reward / supervision，同时控制 evaluator bias？

## 维护规则

- 新增 M1 必须能映射到至少一个 Pattern、一个真实案例或 Lab。
- 如果一个问题只是在问术语定义，默认不能成为 M1。
- 完成度更新只修改 `S0–S4`，不因为“已经学会”而降低 M1/M2 级别。
- M1 长期控制在“可反复复习”的规模，不无限增长。
