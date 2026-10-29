# Q11 Judge 与 Human Disagreement 应如何分析？

- Level: M2
- Mastery: S0
- Related Parts: Part 2 / Part 6
- Related Patterns: P08 Judge Calibration Before Scale, P04 Slice Before Aggregate
- Related Cases: VeriAgent reviewed failure promotion

## 30-second answer

Judge 和 human 不一致时，不应该只报一个 correlation，也不应该默认 human 一定对、Judge 一定错。

Disagreement 可能来自：

- Judge error；
- human annotation error；
- rubric ambiguity；
- task ambiguity；
- evidence 缺失；
- 合理的主观偏好差异；
- 某个系统性 slice bias。

正确做法是保留 raw judgments，按 criterion / slice 看 confusion 和 disagreement pattern，需要时 adjudicate，并同时报告 human-human 与 judge-human reliability。

## 90-second answer

一个可靠分析至少分三层：

```text
Aggregate agreement
        ↓
Criterion / slice disagreement
        ↓
Case-level adjudication and root cause
```

不同输出类型用不同 metric：分类看 agreement / kappa / confusion matrix；有序分数看 weighted kappa；排序看 Spearman / Kendall；连续分数还可以看 MAE / systematic offset。

但 metric 只是入口。真正重要的是：不一致发生在哪里、是否会改变 release decision、是否属于 rubric 本身不可唯一化的主观区域。

如果人类之间本来就高度分歧，那么要求 Judge 与某一个 annotator 完全一致并不合理。

## Full reasoning

### 1. Disagreement 是诊断信号，不只是噪声

看到：

```text
Human = 4
Judge = 2
```

不能直接得出“Judge 错了”。

至少有几种可能：

1. Judge 漏掉了关键证据；
2. human 标错；
3. rubric 对 2/3/4 的边界不清楚；
4. 样本本身存在多种合理解释；
5. Judge 受 position / style / verbosity 影响；
6. human 和 Judge 实际使用了不同 criterion；
7. 参考上下文不一致。

因此 disagreement review 是 evaluator debugging 的核心入口。

### 2. 先把 Human label 分层

不要只存一个最终 `gold_score`。

更好的结构：

```text
annotator_1_raw
annotator_2_raw
annotator_3_raw
rationales / evidence
agreement status
adjudicated label
adjudication reason
```

这样以后 rubric 更新时，可以重新分析，而不是只剩一个被压平的标签。

### 3. Human-human agreement 是重要参照，但不是“天花板公式”

如果两个人类标注者之间都经常不一致，Judge-human 低 agreement 可能部分来自任务主观性或 rubric 问题。

因此至少对比：

```text
human-human
judge-human
judge-judge / judge-repeat
```

但不要机械地说：

> Judge-human 达到 human-human 就一定可以替代人工。

还需要看错误类型和业务代价。

### 4. Metric 要匹配 label 类型

#### Nominal label

例如：

```text
pass / fail
A / B / tie
failure type
```

看：

- percent agreement；
- confusion matrix；
- Cohen/Fleiss kappa（视 rater 数量而定）。

#### Ordinal score

例如 1–5：

- weighted kappa；
- MAE / absolute score difference；
- confusion matrix；
- systematic leniency / severity shift。

#### Ranking

例如模型排序：

- Spearman；
- Kendall；
- pairwise ordering agreement。

#### Continuous score

相关性之外还要看：

- calibration / scale offset；
- MAE / RMSE；
- residual by slice。

### 5. 为什么“只报相关系数”不够？

两个 evaluator 可能：

```text
Human: 1,2,3,4,5
Judge: 3,4,5,6,7
```

排序相关可以非常高，但 Judge 存在稳定的 scale shift。

反过来，两个 evaluator 也可能总体相关不错，但在 safety / hard slice 上严重不一致。

所以至少需要：

```text
agreement
error magnitude
systematic offset
slice behavior
case review
```

### 6. 不要用“平均人类分数”掩盖 disagreement

把多个 human score 先平均，再和 Judge 做 correlation，可能隐藏真实 rater variation。

更好的做法是保留 individual ratings，并明确 reference 构造方式：

- majority vote；
- median；
- adjudication；
- distribution；
- expert override。

每种方式都代表不同的 target。

### 7. Adjudication 的目标不是强行消灭分歧

需要 adjudicate 的典型情况：

- Judge-human 在 critical criterion 上冲突；
- human-human 大幅冲突；
- near-threshold decision；
- rubric 无法直接解释；
- bias probe 命中；
- evidence 有缺失/冲突。

Adjudication 记录应包含：

```text
original judgments
available evidence
final decision
reason
rubric clause used
whether rubric needs revision
```

### 8. 有些 disagreement 应保留成 distribution

例如：

```text
Which answer is more engaging?
Which tone feels more appropriate?
```

如果真实用户群体本来就存在偏好分布，强行 adjudicate 成一个“唯一真值”可能损失信息。

此时更合理的是报告：

```text
preference distribution
subpopulation slices
uncertainty
```

而不是制造虚假的 ground truth。

### 9. Disagreement analysis 最终要反馈 rubric 和 protocol

如果反复发现某类 disagreement，例如：

- 事实正确但不够详细；
- 引用完整但表达简短；
- 某类边界 case 人类也无法稳定判断；

就应该问：

> 是 Judge 需要修，还是 rubric 本身定义不清？

这也是为什么 evaluation system 需要 versioned rubric，而不是一次写完永远不变。

## 一个实用 disagreement review table

| 字段 | 用途 |
|---|---|
| sample_id | 定位样本 |
| criterion | 哪个维度冲突 |
| human_raw | 原始人工判断 |
| judge_raw | 原始 Judge 判断 |
| severity | 是否影响最终决策 |
| slice | 哪类 case |
| evidence | 可验证证据 |
| suspected cause | 初步原因 |
| adjudicated | 最终处理 |
| action | 改 rubric / judge / data / no change |

## Common wrong answers

### 错误 1：Human 是 ground truth，所以 disagreement 都算 Judge error

Human label 也可能错，尤其在复杂或主观任务里。

### 错误 2：Judge-human correlation 0.9，所以很可靠

可能仍有严重 scale bias、critical-slice error 或逐样本不一致。

### 错误 3：kappa 低说明数据完全不可用

低 agreement 可能提示任务主观、rubric 含糊或 annotator 培训不足；应先诊断来源。

### 错误 4：把争议样本删掉，agreement 就提高了

这会把最重要的 evaluator boundary case 从数据中清掉，得到虚假的可靠性。

## Counterexample / boundary

如果是“代码是否通过单元测试”，human disagreement 通常不是主要问题，因为存在 executable evidence。

如果是“解释是否清晰”，human disagreement 可能是目标分布本身的一部分。这两类任务不应使用同一种 gold 构造方式。

## VeriAgent example

VeriAgent challenge eval 中，某个模型输出恰好与预设错误 SQL 的结果相同，只能作为诊断线索，不能自动认定真实根因。失败记录先进入 `REQUIRES_REVIEW`，只有显式复核证据后才形成候选经验。

这个设计对应 disagreement/adjudication 的核心原则：

```text
observable match
≠ causal explanation
≠ promotion-ready label
```

复杂判断需要保留原始证据和人工复核，而不是让一个自动 signal 直接升级成 ground truth。

## Follow-up questions

- kappa 和 percent agreement 各自有什么局限？
- human-human agreement 很低时 Judge 应怎么评？
- 哪些 disagreement 应 adjudicate，哪些应保留分布？
- 为什么平均人类评分可能夸大 Judge alignment？
- 如何把 disagreement case 变成后续 regression set？

## Evidence of mastery

达到 S4 时，应能拿到一份 human + Judge 标注表，选择合适 agreement 指标，做 criterion/slice confusion analysis，并设计 adjudication 与 rubric revision 流程。

## References

- Thakur et al., 2025, *Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges*: https://aclanthology.org/2025.gem-1.33/
- Amidei et al., 2019, *Agreement is overrated: A plea for correlation to assess human evaluation reliability*: https://aclanthology.org/W19-8642/
- Mukherjee et al., 2026, *The Geometry of LLM-as-Judge: Why Inter-LLM Consensus Is Not Human Alignment*: https://aclanthology.org/2026.findings-emnlp.1696/

## Related knowledge

- [Q08 Judge Reliability](02_Judge_Reliability_and_Calibration.md)
- [Q09 Judge Bias](03_Judge_Bias_and_Failure_Modes.md)
- [Q10 Rubric / Protocol](04_Rubric_and_Scoring_Protocol.md)
- [Metrics Registry](../METRICS.md)
