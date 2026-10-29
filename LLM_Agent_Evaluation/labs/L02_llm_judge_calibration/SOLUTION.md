# L02 — Reference Solution

> 建议先完成 `REPORT_TEMPLATE.md`，再阅读本文件。

## 1. Expected metric results

### Pointwise

```text
N                         : 24
Judge↔Human exact         : 45.8%
Judge↔Human within ±1     : 95.8%
Judge↔Human MAE           : 0.583
Critical disagreement ≥2  : 4.2%
Judge repeat exact        : 87.5%
Human↔Human exact         : 62.5%
```

最重要的陷阱：`95.8% within ±1` 不能被表述成“Judge 95.8% 准确”。它没有消除 critical disagreement、repeat instability、slice bias、pairwise position sensitivity。

### Pointwise slices

```text
factual      exact 60.0%   MAE 0.400
instruction  exact 60.0%   MAE 0.400
reasoning    exact 40.0%   MAE 0.600
safety       exact 40.0%   MAE 0.800
style        exact 25.0%   MAE 0.750

short        exact 83.3%   MAE 0.167
medium       exact 50.0%   MAE 0.500
long         exact 20.0%   MAE 0.900

plain        exact 64.3%   MAE 0.357
polished     exact 20.0%   MAE 0.900
```

这些仍然只是 observational slice：long 与 polished 在数据里相关，不能据此单独认定因果来自“长度”或“润色风格”。

## 2. Pairwise results

```text
N                         : 20
Judge↔Human accuracy      : 70.0%
Judge repeat consistency  : 90.0%
Swap consistency          : 75.0%
Accuracy after swap       : 45.0%
Human↔Human exact         : 75.0%
```

这说明 overall pairwise accuracy 未过 80% gate；同一顺序重复也有 10% flip；交换 A/B 后只有 75% verdict 保持一致；swapped-order accuracy 从 original 70% 降到 45%。因此不能把这个 Judge 当成 order-invariant preference oracle。

## 3. Task-family slice

```text
factual      acc 100.0%
instruction  acc 75.0%
reasoning    acc 75.0%
safety       acc 75.0%
style        acc 25.0%
```

`style` slice 是明显 failure concentration。但即使 factual original-order accuracy 是 100%，其 swap consistency 仍只有 75%。

## 4. Bias probes

```text
verbosity      Judge B 70.0%   Human B 20.0%   gap +50.0 pp
style/polish   Judge B 66.7%   Human B 11.1%   gap +55.6 pp
family-match   Judge B 70.0%   Human B 20.0%   gap +50.0 pp
```

正确表述是：数据中出现了与 verbosity / polish / family-match 一致的偏好信号。不能直接做因果归因，因为三种 probe 在这个小数据集里部分共线。下一轮应做 factor-controlled counterfactual。

## 5. Pre-registered gates

```text
[PASS] Pointwise within ±1 ≥ 90%
[FAIL] Critical disagreement ≤ 2%
[FAIL] Pairwise accuracy ≥ 80%
[FAIL] Repeat consistency ≥ 95%
[FAIL] Swap consistency ≥ 95%
[FAIL] Style slice pairwise accuracy ≥ 70%
[FAIL] Verbose-preference gap ≤ 15 pp
```

结果是 `6 / 7 gates failed`。不能因为唯一通过的 `within ±1` 很高，就把 Judge 描述为“基本可靠”。

## 6. Manual adjudication

- **C01 → B**：reference number 是 2.80M；A 的事实错误是 hard failure。
- **C02 → A**：任务明确要求 3 bullets；B 违反显式 output contract。
- **C03 → TIE**：两者都满足任务，没有客观 evidence 支持唯一答案；这是 preference variance。
- **C04 → A**：B 引用了不存在的 `json.validate_schema()`，属于 material factual/executable error。
- **C05 → A**：没有 2027 数据或预测假设；B 的数值没有 evidence，A 的 abstention 正确。

## 7. Reference deployment decision

推荐：

```text
NO-GO for autonomous release gating.
```

更细地说：

```text
CONDITIONAL GO for low-stakes advisory triage,
provided that deterministic checks remain authoritative
and uncertain/high-risk cases are escalated to human review.
```

### Potentially allowed

- 低风险辅助排序；
- triage；
- 作为多个信号之一；
- 给 Human review 提供候选解释；
- deterministic verifier 之后的软质量维度。

### Forbidden at this stage

- 唯一 release gate；
- 事实正确性的最终裁决；
- 高风险安全决策；
- 无人工 escalation 的 pairwise preference oracle；
- 替代已有 executable verifier。

## 8. Next minimum experiment

```text
1. 修复 / 约束 rubric
2. 固定 Judge version / prompt / decoding
3. 构造 factor-controlled verbosity/polish probes
4. 做更大 swap + repeat set
5. 单独扩充 style / safety hard slices
6. 加 abstain / human escalation
7. 在独立 holdout 上重新评估
```

不要“看到结果不好 → 调 prompt → 在同一批 calibration data 上继续试 → 报新最好结果”，否则会产生 evaluator overfitting。

## 9. Strong 90-second interview answer

先定义 Judge 要承担的 claim 和风险 → 用 human/verifier anchor set 做 calibration → 不只看 overall correlation → 看 exact/tolerance agreement/critical errors → 做 repeat consistency → pairwise 做 A/B swap → 做 verbosity/style/family 等 controlled bias probes → slice 分析 → disagreement adjudication → threshold 预注册 → 独立 holdout → 最后给 scope-aware GO/NO-GO。

最关键的一句话：**Judge reliability 不是模型的永久属性，而是相对于具体 evaluation contract、rubric、task distribution 和 decision risk 的经验结论。**
