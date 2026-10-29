# Q01 Evaluation Contract：开始跑模型之前，必须先定义什么？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 5 / Part 6 / Part 7
- Related Patterns: P01 Eval Contract First, P10 Replayable Evaluation, P11 Holdout after Development
- Related Cases: VeriAgent Olist challenge evaluation

## 30-second answer

Evaluation Contract 是一份**在看到结果之前就尽量固定的评测约定**。至少要回答：评谁、在什么任务分布上评、一次观测单位是什么、什么算成功/失败、由谁判、指标怎样聚合、失败和缺失怎么处理、随机性怎么重复、版本与环境怎样冻结，以及最后用什么规则做决策。

核心原则是：**先定义“什么证据可以支持什么结论”，再运行系统。** 否则很容易在看到结果后改分母、改规则、挑样本，把评测变成事后解释。

## 90-second answer

一个可执行的 Evaluation Contract 至少包含九项：

1. **Claim / Question**：想判断什么，例如“新 controller 是否提高 held-out task success”。
2. **Scope / Population**：结论适用于哪些任务、用户、环境、模型版本。
3. **Estimand & Unit**：最终要估计的量是什么；task、run、user 还是 trajectory 是分析单位。
4. **System Conditions**：baseline/candidate 的模型、prompt、tool、memory、budget 等哪些相同、哪些不同。
5. **Evaluator / Oracle**：正确性由 deterministic verifier、reference、human 还是 LLM judge 判定。
6. **Metric Contract**：分子、分母、aggregation、失败/缺失处理、方向和主要 slices。
7. **Protocol**：数据切分、重复次数、随机性、配对方式、执行顺序、停止规则。
8. **Artifacts & Versions**：数据快照、代码/配置、模型、trace、manifest、hash。
9. **Decision Rule**：什么结果才算通过，例如主指标不退化、false accept 不增加、成本在预算内。

Contract 的价值不是让实验“复杂”，而是让**结果不可被随意重新解释**。

## Full reasoning

### 1. Evaluation 不是“跑一套题”

真正的评测对象不是一个裸模型分数，而是一个更完整的条件集合：

```text
System under test
+ Task distribution
+ Environment
+ Evaluator
+ Protocol
+ Metric
+ Decision rule
```

只要其中任一项变化，数字的含义就可能变化。

### 2. 先写 claim，再选 metric

错误顺序：

```text
先跑 benchmark → 得到 accuracy → 再想这个数字说明什么
```

更稳妥的顺序：

```text
Claim
→ Estimand
→ Unit of analysis
→ Evaluator
→ Metric
→ Protocol
→ Artifacts
→ Run
→ Analysis
```

例如 claim 是“memory 能提高同类问题的可靠完成率”，就不能只验证 `memory_retrieved=true`；还要比较同任务条件下的 outcome，并确认失败发生在 memory 有机会发挥作用的阶段。

### 3. 最小 Contract 表

| 字段 | 必答问题 |
|---|---|
| Objective | 我到底想知道什么？ |
| Scope | 结论能泛化到哪里？ |
| Task set | 任务如何采样、是否 frozen / held-out？ |
| Unit | task / run / user / trajectory 谁是主要分析单位？ |
| Conditions | baseline 与 candidate 唯一预期差异是什么？ |
| Success | 什么算正确完成、partial、safe stop、failure？ |
| Evaluator | 谁判定？其可靠性如何验证？ |
| Metrics | 分子、分母、聚合、失败处理是什么？ |
| Repeats | 如何处理模型随机性？ |
| Slices | 哪些能力/失败族必须单独看？ |
| Artifacts | 哪些输入、配置、trace、hash 必须保存？ |
| Decision | 什么证据支持 ship / reject / continue investigating？ |

### 4. Contract 与 Protocol 的区别

- **Contract**：规定“什么算有效证据和有效结论”。
- **Protocol**：规定“具体怎样收集这些证据”。

Protocol 是 Contract 的执行方案。例如“同题两种条件各跑 3 次并交替执行”是 protocol；“比较同任务条件下的 paired outcome，且测试集不可回流开发”是更高层 contract。

## Evaluation design checklist

开始运行之前检查：

- [ ] 主 claim 能否用一句话写清楚？
- [ ] primary metric 是否唯一或明确分层？
- [ ] 分母是否提前固定？
- [ ] aborted / timeout / invalid output 是否有预定义处理？
- [ ] baseline 与 candidate 除目标变量外是否尽量一致？
- [ ] dev 与 held-out test 是否隔离？
- [ ] judge/verifier 是否在正式实验前冻结？
- [ ] 重复次数与配对关系是否定义？
- [ ] trace / manifest / config / snapshot 是否可重放？
- [ ] 什么结果“不足以证明 claim”是否提前写下？

## Common wrong answers

### 错误 1：Evaluation Contract 就是 metric 列表

不够。Metric 只回答“怎么算数字”，没有定义 scope、unit、evaluator、protocol 和因果边界。

### 错误 2：benchmark 固定，所以 contract 已经固定

不一定。模型版本、prompt、工具、judge、失败处理、重复次数、aggregation 都可能改变结果含义。

### 错误 3：先看结果，再决定哪些失败不计入

这是典型的事后修改分母，会系统性高估性能。

## Counterexample / boundary

探索阶段可以允许更灵活的分析，不要求所有假设都预注册。但一旦要声称“方法优于 baseline”“可以上线”“能力提高”，就应把关键 contract 冻结，并在独立数据上验证。

## VeriAgent example

以当前 `JiangHui0203/veriagent` 的 Olist challenge evaluation 为例：挑战集先固定 24 题，并在真实模型测试前划分 dev/test；标准答案由 SQL 与独立 Python 计算交叉验证；candidate memory 在 dev failure 复核后冻结，再在 held-out test 上做 paired comparison；测试失败不回流本轮 memory。这里真正有价值的不是“跑了 72 次”，而是**开发、冻结、测试和归因边界事先被分开**。

当前实现入口：`veriagent/docs/challenge_evaluation.md`（reviewed against `veriagent@6f5f61c`）。

## Follow-up questions

- 为什么 decision rule 不能只看 primary accuracy？
- evaluator 改版后历史结果还能直接比较吗？
- exploratory analysis 与 confirmatory evaluation 如何分开？
- 为什么 test failure 不能立刻加入 memory 再继续同一轮测试？

## Evidence of mastery

达到 S4 时，应能拿到一个新 LLM/Agent 系统，在 10–15 分钟内写出一页可执行 Evaluation Contract，并主动指出至少三个会导致伪提升的 confounder。

## Related knowledge

- [Q02 Estimand & Unit of Analysis](../06_Statistics_and_Experiment_Design/01_Estimand_and_Unit_of_Analysis.md)
- [Q04 Metric Design](03_Metric_Design.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
- [Metrics Registry](../METRICS.md)
