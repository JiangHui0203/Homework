# Q10 如何设计 Rubric、Pointwise / Pairwise Protocol 和 Adjudication？

- Level: M1
- Mastery: S0
- Related Parts: Part 2 / Part 5 / Part 7
- Related Patterns: P01 Eval Contract First, P02 Deterministic First Judge Last, P08 Judge Calibration Before Scale
- Related Cases: VeriAgent verifier stack as a decomposition example

## 30-second answer

好的 Judge protocol 不是“写一个 prompt 让模型打分”，而是把评价任务拆成：

```text
criterion
→ observable evidence
→ scoring rule
→ protocol
→ aggregation
→ disagreement / adjudication
```

Rubric 应尽量原子化、可观察、减少重叠，并给出清晰的评分锚点。可确定性验证的 hard constraint 不要混进主观总分。

Pointwise 适合绝对评分和阈值判断；pairwise 适合比较两个候选的相对质量，但要处理 position bias 和排序聚合。争议、高风险或低置信 case 应有明确 adjudication / escalation 规则。

## 90-second answer

设计时先决定你需要的是：

- **absolute quality**：这个回答是否达到标准？→ pointwise；
- **relative preference**：A 和 B 哪个更好？→ pairwise；
- **hard validity**：是否满足明确约束？→ verifier；
- **多维质量画像**：correctness / completeness / clarity 等分别如何？→ rubric decomposition。

Rubric 最容易犯的错误是“几个看起来合理的维度 + 1–5 分”，但每个维度没有证据边界，最后 Judge 只是凭整体印象打分。

更可靠的结构是：每个 criterion 定义可观察证据、正反例、评分锚点和 critical error；最后再明确 hard gate 与 soft score 如何组合。

## Full reasoning

### 1. Rubric 的核心不是“维度多”，而是可判定

每个 criterion 至少回答：

```text
What exactly is being judged?
What evidence is allowed?
What counts as pass / fail / partial?
What should NOT influence this criterion?
What happens when evidence is insufficient?
```

例如：

#### 不好的 criterion

```text
Quality: 1-5
```

几乎没有操作性。

#### 更好的拆分

```text
Factual correctness
Instruction satisfaction
Coverage / completeness
Grounding to provided evidence
Clarity
```

但拆分不是越多越好。维度过多会增加 overlap、认知负担和 aggregation ambiguity。

### 2. Criterion 要尽量原子化、少重叠

如果“helpfulness”和“quality”同时存在，Judge 可能重复奖励同一属性。

检查两个 criterion 是否重叠，可以问：

> 是否可能只改变 A criterion，而 B 保持不变？

如果几乎不可能，说明二者可能没有必要分开。

### 3. 给评分等级提供 anchor，而不是只给数字

例如 0–2：

```text
0 = critical requirement missing / contradicted
1 = partially satisfied, material omission remains
2 = fully satisfied with no material error
```

比单纯：

```text
1 = poor
2 = fair
3 = good
4 = very good
5 = excellent
```

更容易稳定执行。

对于主观维度，可以使用行为描述 anchor；对于事实维度，尽量接 deterministic evidence。

### 4. Hard constraints 和 soft quality 分开

不要让严重错误被“语言流畅”抵消。

例如：

```text
hard gate:
- factual correctness
- policy violation
- executable validity

soft score:
- clarity
- concision
- style
```

Aggregation 可以定义为：

```text
if any critical_error:
    final = FAIL
else:
    final = weighted_soft_score
```

而不是简单平均所有维度。

### 5. Pointwise protocol

形式：

```text
candidate -> absolute score / label
```

优点：

- 适合 release threshold；
- 单个样本可独立评分；
- 易生成多维 score profile；
- 成本通常接近 O(n)。

缺点：

- Judge 的评分尺度可能漂移；
- leniency / severity bias；
- 1–5 分各档边界难稳定；
- 不同 Judge 的 scale 不可直接比较。

适合：

```text
是否达到最低质量线
是否满足 rubric
单模型长期 regression
```

### 6. Pairwise protocol

形式：

```text
(A, B) -> A / B / tie
```

优点：

- 对细微相对质量差更直观；
- 不要求 Judge 维持稳定绝对尺度；
- 很适合 model / prompt A-B comparison。

缺点：

- position bias；
- 大规模全 pair 成本高；
- 只有相对偏好，没有天然 absolute threshold；
- 排名还需要 Bradley-Terry / Elo / win-rate 等 aggregation。

最小协议至少考虑：

```text
blind candidate identity
randomized or dual order
tie policy
same rubric
same context
same judge version
pair-level audit trail
```

### 7. Pointwise vs Pairwise 不是谁“更高级”

选择取决于 estimand。

如果问题是：

> 新模型是否比旧模型更受偏好？

pairwise 很自然。

如果问题是：

> 一个回答是否超过生产准入线？

pointwise / checklist / hard gate 通常更合适。

实际系统常常 hybrid：

```text
Verifier -> hard validity
Pointwise rubric -> minimum quality
Pairwise -> compare two passing candidates
```

### 8. Checklist 何时优于 Likert scale？

当 criterion 可以拆成多个可观察的小问题时，binary / ternary checklist 往往更可审计：

```text
Does it answer the requested question? Y/N
Does it cite provided evidence correctly? Y/N
Does it introduce unsupported facts? Y/N
```

再根据 checklist 派生 score。

优势是每个 decision 更接近局部 evidence，而不是要求 Judge 直接形成一个模糊总分。

### 9. 输出 schema 要支持审计

建议 Judge 输出结构至少包括：

```json
{
  "criterion_results": [
    {
      "criterion": "...",
      "score": 0,
      "evidence": "...",
      "critical_error": false
    }
  ],
  "overall_verdict": "pass|fail|A|B|tie",
  "uncertain": false
}
```

注意：Judge 自报 confidence 不应直接当成已校准概率。

### 10. Adjudication 不是“再问一次模型”

明确什么情况升级：

- dual-order pairwise verdict 不一致；
- 多 Judge 不一致；
- Judge 与 deterministic evidence 冲突；
- critical / safety slice；
- near-threshold case；
- evidence insufficient；
- known bias probe 命中。

可能的 adjudicator：

```text
stronger deterministic verifier
expert human
second independent judge
panel + explicit tie-break rule
```

优先级由 evidence strength 和 error cost 决定。

### 11. Rubric 本身也要版本化和评测

rubric 一改，历史 score 就可能不可比。

必须记录：

```text
rubric version
judge prompt version
judge model version
aggregation rule
critical-error policy
```

如果 rubric 改变了 concept definition，应重新建立 calibration，而不是直接续用旧 threshold。

## Evaluation design

一个完整的 Judge protocol checklist：

```text
1. Define target claim
2. Separate deterministic vs judgmental criteria
3. Write atomic criteria
4. Define observable anchors
5. Choose pointwise / pairwise / checklist / hybrid
6. Define tie / abstain / insufficient-evidence behavior
7. Freeze presentation and output schema
8. Define aggregation and hard gates
9. Define adjudication triggers
10. Calibrate on anchor set
11. Test bias / repeatability
12. Confirm on holdout
```

## Common wrong answers

### 错误 1：Rubric 越详细越可靠

过多 criterion 会产生 overlap、冲突和 rubric artifacts。重点是可判定，不是字数。

### 错误 2：Pairwise 一定比 pointwise 可靠

pairwise 避免一部分绝对尺度问题，但引入 position bias、pair selection 和 ranking aggregation 问题。

### 错误 3：所有维度平均就是 overall score

critical factual error 可能不应被“清晰”“礼貌”等软指标抵消。

### 错误 4：Judge 给了 rationale，所以 judgment 可解释

rationale 只是 Judge 输出的一部分，不等于真实因果机制，也不能替代 counterfactual validation。

## Counterexample / boundary

一个数学题最终答案可以 exact verify，但“解答是否 pedagogically clear”无法完全程序化。

合理 evaluator stack：

```text
final answer correctness -> verifier
reasoning requirement coverage -> checklist
pedagogical clarity -> calibrated judge/human
```

而不是一个 1–10 总分同时承担三种概念。

## VeriAgent example

VeriAgent 本身展示了 evaluator decomposition 的思路：SQL 是否能执行、数值是否与冻结 reference 一致、数据不足时是否安全停止，这些可以分别由明确 contract 检查。

如果未来增加自然语言质量评估，应继续沿用分层：

```text
hard correctness contract
+
soft explanation rubric
```

而不是把已有 deterministic evidence 丢掉，让一个 Judge 重新综合裁决。

## Follow-up questions

- 什么时候 pairwise 比 pointwise 更合适？
- 什么时候 binary checklist 比 1–5 分更稳？
- rubric criterion 如何检测 overlap？
- pairwise tie 应不应该允许？
- Judge 与 verifier 冲突时如何 adjudicate？

## Evidence of mastery

达到 S4 时，应能对一个开放式任务写出完整 rubric 和 protocol，并解释为什么选择 pointwise / pairwise / checklist、哪些是 hard gate、哪些需要 adjudication。

## References

- Zheng et al., 2023, *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*: https://arxiv.org/abs/2306.05685
- Liu et al., 2023, *G-Eval*: https://arxiv.org/abs/2303.16634
- Lee et al., 2025, *CheckEval: A reliable LLM-as-a-Judge framework using checklists*: https://aclanthology.org/2025.emnlp-main.796/
- Bagaria et al., 2026, *Judging LLM-as-a-Judge: Concerning Rubric Artifacts*: https://aclanthology.org/2026.emnlp-main.2612/

## Related knowledge

- [Q07 Grader / Verifier / Judge](01_Grader_Verifier_and_Judge.md)
- [Q08 Judge Reliability](02_Judge_Reliability_and_Calibration.md)
- [Q09 Judge Bias](03_Judge_Bias_and_Failure_Modes.md)
- [Q11 Human Disagreement](05_Human_Disagreement_and_Adjudication.md)
