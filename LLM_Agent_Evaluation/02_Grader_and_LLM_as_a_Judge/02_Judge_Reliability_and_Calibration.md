# Q08 如何证明一个 LLM Judge 本身足够可靠？

- Level: M1
- Mastery: S0
- Related Parts: Part 2 / Part 6 / Part 7
- Related Patterns: P08 Judge Calibration Before Scale, P10 Replayable Evaluation
- Related Cases: VeriAgent deterministic verification as a boundary case

## 30-second answer

不能因为 Judge 很强、分数看起来合理，或者和人工有一个较高相关系数，就把它当作 ground truth。

Judge 的可靠性必须针对**具体任务、具体 rubric、具体协议和具体用途**验证。最小验证至少包括：

1. 与可靠 human / verifier anchor 的一致性；
2. 同一输入重复评分的稳定性；
3. 对位置、长度、风格等无关扰动的鲁棒性；
4. 关键 slice 上的错误率；
5. 版本、prompt、decoding 固定后的可复现性。

结论不是“这个 Judge 普遍可靠”，而是“在这个 evaluation contract 下，它是否足以承担这个决策”。

## 90-second answer

把 Judge 当成一个需要被评测的模型，而不是评测系统的终点。

一个实用的 meta-evaluation protocol 是：

```text
定义 Judge 要支持的 claim
        ↓
构造代表性的 calibration / anchor set
        ↓
获得 human / verifier reference
        ↓
冻结 judge model + prompt + rubric + decoding
        ↓
重复评分 + bias perturbation
        ↓
计算 agreement / consistency / slice errors
        ↓
设定 deployment threshold 与 escalation rule
        ↓
在独立 holdout 上确认
```

如果任务本身存在 deterministic evidence，例如 SQL 执行结果、单元测试或 proof checker，那么这些证据应优先作为 anchor，而不是让另一个 LLM 判断“看起来是否正确”。

## Full reasoning

### 1. 先问：Judge 到底要替你做什么决定？

“Judge 是否可靠”不是一个脱离用途的问题。

可能的用途包括：

- 给开放式回答打 1–5 分；
- 判断 A/B 哪个更好；
- 给训练数据生成 preference；
- 作为 benchmark 排名器；
- 作为 CI gate；
- 只用于低风险预筛，争议样本交人工。

这些用途的容错要求完全不同。

因此先定义：

```text
Target claim
Unit of analysis
Decision threshold
Error cost
Critical slices
Escalation path
```

### 2. Anchor 不一定等于“单个人工标签”

可靠 reference 可以来自：

- deterministic verifier；
- executable reference；
- expert adjudication；
- 多人独立标注后的 adjudicated label；
- 高质量 pairwise preference set。

人工也会有分歧，所以不能把任意一个 human label 自动视为绝对真值。

更合理的是区分：

```text
Raw human judgments
Adjudicated reference
Human-human agreement
Judge-human agreement
```

### 3. Judge reliability 至少是多维的

#### A. Validity / alignment

Judge 是否在测你真正关心的概念？

例如 rubric 说“正确性”，Judge 却主要奖励流畅和详细，就属于 construct mismatch。

#### B. Inter-rater agreement

Judge 与 human / gold anchor 的一致程度。

可根据输出类型使用：

- exact agreement；
- confusion matrix；
- weighted kappa；
- Spearman / Kendall；
- pairwise preference accuracy。

不要只报一个相关系数。

#### C. Intra-rater reliability

同一个 Judge 对完全相同输入重复运行，结果是否稳定？

如果 identical rerun 经常翻转，说明单次 judgment 不足以作为强证据。

#### D. Counterfactual robustness

改变与目标质量无关的因素后，Judge 是否仍保持结论？

例如：

- A/B 顺序交换；
- markdown ↔ plain text；
- 简洁 ↔ 冗长但语义等价；
- 隐去模型名称；
- 改变措辞但保持事实不变。

#### E. Slice reliability

整体 90% agreement 可能掩盖关键区域失败。

至少按以下类型看 slice：

- easy / hard；
- close-call / large-gap；
- 长/短回答；
- 不同任务族；
- 不同语言；
- safety / high-impact cases；
- judge 自己不确定的 case。

### 4. Calibration 不是“调 prompt 调到最好看”

这里的 calibration 指：

> 在冻结的目标任务上，用可靠 anchor 估计 Judge 的行为边界，并决定它在哪些条件下可以被信任。

需要冻结：

```text
judge model/version
system/user prompt
rubric
output schema
decoding parameters
candidate presentation order policy
reference context
```

否则今天校准的是 Judge A，明天线上实际使用的可能已经是 Judge B。

### 5. 一个可复用的最小 Judge calibration protocol

#### Step 1 — 选择 calibration set

必须覆盖真实部署分布和关键 slice，而不是只挑容易题。

#### Step 2 — 建立 anchor

优先级：

```text
Deterministic / executable evidence
> expert-adjudicated human evidence
> single human label
```

这不是绝对等级，而是提醒：证据来源本身也要审计。

#### Step 3 — 冻结 Judge contract

明确 prompt、rubric、输出格式、模型版本和 decoding。

#### Step 4 — 重复运行

对部分样本做 identical rerun，估计 self-consistency / flip rate。

#### Step 5 — 做 counterfactual bias tests

至少测试：

- swap order；
- verbosity；
- formatting/style；
- candidate identity masking。

#### Step 6 — 报告多维指标

不要只给一个“Judge accuracy”。

推荐至少包括：

```text
anchor agreement
critical-slice agreement
repeat consistency
swap consistency
major-error confusion matrix
abstain / escalation rate
cost / latency
```

#### Step 7 — 定义路由策略

例如：

```text
high-confidence + noncritical slice -> auto accept
close-call / disagreement -> second judge or human
hard factual constraint -> verifier overrides judge
```

#### Step 8 — 独立 holdout

不要在 calibration set 上不断修改 rubric 后，再拿同一套数据宣布 Judge 已经可靠。

## 一个常见误区：Human agreement 高，就等于 Judge 可以替代人工

不成立。

还要问：

- 错误是否集中在高风险 slice？
- Judge 是否有系统 bias？
- 这些错误是否会改变模型排名或 release decision？
- Judge-human agreement 是否接近 human-human reliability？
- disagreement 是否来自 rubric 本身含糊？

Judge 的目标通常不是“模仿某一个人”，而是提供足够可靠、可审计的 evaluation signal。

## Common wrong answers

### 错误 1：和人工 Spearman 相关系数高就够了

相关性主要回答排序关系，不等于逐样本一致，也不能发现系统性偏高/偏低或关键 slice 错误。

### 错误 2：temperature=0，所以 Judge 是确定的

即使设置确定性解码，服务端实现、模型版本、并行计算或 prompt sensitivity 仍可能带来变化；更重要的是，稳定地判错也不叫可靠。

### 错误 3：多个 Judge 都同意，所以结论可信

多个 Judge 可能共享同一类偏差。inter-judge consensus 不能自动证明 human alignment。

### 错误 4：Judge 比被评模型更大，所以天然可靠

模型能力强弱不是 evaluator validity 的充分条件。

## Counterexample / boundary

如果任务是“SQL 最终数值是否正确”，已有冻结 reference 与独立执行环境，那么再让 LLM Judge 判断答案正确性通常是在用更弱证据替代更强证据。

但如果任务还要评价“解释是否清楚、是否准确说明限制”，则可以把 correctness 留给 deterministic verifier，把 explanation quality 交给经过校准的 Judge / human。

## VeriAgent example

VeriAgent 的 Olist challenge eval 对数值正确性使用冻结 reference，并在建集时让 reference SQL 与独立 Python 计算交叉验证；这类 correctness 不需要 LLM Judge。

如果未来要评价自然语言解释质量，可以新增 Judge，但必须把它作为独立 evaluator layer：

```text
numeric correctness -> deterministic verifier
explanation quality -> calibrated human / LLM judge
final decision -> explicit aggregation rule
```

这比“让 Judge 综合看一下答案好不好”更可审计。

## Follow-up questions

- Judge-human agreement 到多少才算够？
- 为什么 human-human agreement 也要报告？
- identical rerun flip rate 高时怎么办？
- Judge ensemble 是否一定比单 Judge 更可靠？
- 如何选择 calibration set 和 holdout set？

## Evidence of mastery

达到 S4 时，应能针对一个新的开放式任务写出 Judge calibration plan，并明确：anchor、sample/slice、repeat、bias test、metric、threshold、escalation 和 holdout。

## References

- Zheng et al., 2023, *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*: https://arxiv.org/abs/2306.05685
- Liu et al., 2023, *G-Eval*: https://arxiv.org/abs/2303.16634
- Haldar & Hockenmaier, 2025, *Rating Roulette: Self-Inconsistency in LLM-As-A-Judge Frameworks*: https://aclanthology.org/2025.findings-emnlp.1361/
- Mukherjee et al., 2026, *The Geometry of LLM-as-Judge: Why Inter-LLM Consensus Is Not Human Alignment*: https://aclanthology.org/2026.findings-emnlp.1696/

## Related knowledge

- [Q07 Grader / Verifier / Judge](01_Grader_Verifier_and_Judge.md)
- [Q09 Judge Bias](03_Judge_Bias_and_Failure_Modes.md)
- [Q10 Rubric / Protocol](04_Rubric_and_Scoring_Protocol.md)
- [Q11 Human Disagreement](05_Human_Disagreement_and_Adjudication.md)
- [Metrics Registry](../METRICS.md)
- [Canonical data-system chapter](../../LLM_Agent_Data/15_Grader_Verifier_and_LLM_as_a_Judge.md)
