# Q06 Open-ended Generation Evaluation：为什么开放式生成很难只靠一个 automatic metric？

- Level: M2
- Mastery: S0
- Related Parts: Part 1 / Part 2 / Part 5 / Part 6
- Related Patterns: P02 Deterministic First, Judge Last; P04 Slice Before Aggregate; P08 Judge Calibration Before Scale
- Related Questions: Q04 Metric Design, Q05 Reference Strategy, Q08–Q11 Judge Reliability, Q30 Correlation Does Not Replace Human Judgment

## 30-second answer

开放式生成很难只靠一个 automatic metric，因为它通常同时包含多个质量维度，而且存在大量不同表述但同样合理的答案。

一个单一分数往往会混淆：

```text
semantic correctness
factuality / grounding
relevance
coverage
instruction following
style / clarity
safety / policy constraints
```

lexical overlap 可能惩罚正确 paraphrase；semantic similarity 可能放过 hallucination；LLM Judge 又可能受 verbosity、position、style bias 影响。

所以更合理的做法是：

> **先把 claim 拆成可观测维度，再为每个维度选择最强证据，最后才考虑是否需要聚合。**

## 90-second answer

我不会先问“这个生成任务用 BLEU、ROUGE 还是 Judge”。我会先问：

```text
这个任务到底哪些性质必须正确？
哪些可以 deterministic verify？
哪些需要 source grounding？
哪些属于 human preference / rubric judgment？
```

例如一个带解释的事实型回答，可以拆成：

```text
final fact correct?          → deterministic / reference
claims supported by source?  → grounding
required points covered?     → checklist
clear and concise?           → calibrated Judge / human
```

开放式生成的关键不是找到一个“万能 metric”，而是建立一个 **evidence portfolio**。如果最终必须形成一个 overall score，也要明确权重、aggregation 与 failure rule，否则一个高风格分可能掩盖事实错误。

---

## 1. 什么叫 Open-ended Generation？

开放式生成不是“完全没有正确答案”。

它更常见的特征是：

```text
valid output space 很大
surface forms 不唯一
多个质量维度同时存在
部分维度可客观验证，部分维度需要判断
```

典型任务：

- summarization；
- long-form QA；
- explanation；
- dialogue；
- rewriting；
- report generation；
- planning；
- recommendation explanation；
- creative / style-constrained writing。

因此：

```text
open-ended
≠ unscorable
≠ purely subjective
```

## 2. 单一 Metric 为什么容易失真？

因为最终输出质量通常是一个向量，而不是天然的一个标量。

可以写成：

```text
Quality = (
  correctness,
  groundedness,
  completeness,
  relevance,
  instruction_following,
  clarity,
  safety,
  cost
)
```

如果直接压成一个数：

```text
score = 0.81
```

就必须问：

```text
0.81 是哪些维度的组合？
事实错误能否被流畅表达抵消？
漏掉关键条件能否被风格加分抵消？
安全 hard failure 是否还能被平均掉？
```

如果没有明确答案，这个 overall score 的决策语义就很弱。

## 3. Lexical-overlap Metric 的边界

典型 lexical metric 关注：

```text
n-gram overlap
word / token overlap
reference surface similarity
```

它们在某些任务上有价值，尤其适合：

```text
格式受限
reference phrasing 相对稳定
需要快速粗筛
历史 benchmark 需要连续性
```

但开放式生成会出现：

### Valid paraphrase 被低估

```text
Reference:
The experiment does not establish causality.

Candidate:
The observed association is insufficient for a causal claim.
```

表面不同，但语义可能高度一致。

### 高 overlap 不等于事实正确

输出可以复制大量 reference wording，同时把关键实体、数字或否定关系写错。

因此：

```text
lexical similarity
≠ semantic correctness
```

## 4. Semantic Similarity 也不是万能解

embedding / learned semantic metric 能减轻 surface mismatch，但仍可能失败。

例如：

```text
reference: revenue increased by 12%
candidate: revenue increased by 21%
```

两句整体语义很接近，但关键数字错了。

或者：

```text
source 没说某件事
candidate 写得语义自然且和主题高度相关
```

semantic similarity 仍可能很高。

所以：

```text
semantic similarity
≠ factuality
≠ grounding
≠ instruction compliance
```

## 5. LLM Judge 为什么仍然不能“一把梭”？

LLM Judge 能处理复杂语义，但它本身也是一个测量系统。

常见风险：

```text
verbosity bias
position bias
style preference
self-preference
prompt sensitivity
rubric ambiguity
repeat instability
critical factual miss
```

因此 Judge score 不能直接当 ground truth。

应该接 Q08–Q11：

```text
human / verifier anchor
agreement
repeat stability
swap test
bias slices
adjudication
critical-error audit
```

Judge 可以是强工具，但必须经过 calibration。

## 6. “Automatic Metric” 不是一个统一类别

至少可以分成：

### A. Lexical metrics

看 surface overlap。

### B. Semantic similarity metrics

看表示空间或模型语义相似度。

### C. Task-specific deterministic checks

例如：

```text
required field present?
JSON valid?
all cited IDs exist?
numeric answer matches?
forbidden action absent?
```

### D. Source-grounded checks

检查 claim 是否被给定 source / evidence 支持。

### E. Model-based Judge

按 rubric 对整体或某个维度评分。

其中 C/D 往往比“通用文本相似度”更接近真实任务 contract。

## 7. 先拆 Dimension，再选 Evidence

推荐流程：

```text
Task claim
↓
Quality dimensions
↓
Per-dimension failure definition
↓
Strongest evaluator / evidence
↓
Calibration / validation
↓
Slice analysis
↓
Optional aggregation
↓
Decision rule
```

例如长回答：

| Dimension | Evidence |
|---|---|
| factual correctness | reference / source / verifier |
| groundedness | citation-source consistency |
| required coverage | checklist |
| instruction following | deterministic constraints + rubric |
| clarity | human / calibrated Judge |
| concision | length constraint + preference judgment |

不是所有维度都应该交给同一个 metric。

## 8. Hard Constraint 与 Soft Preference 要分开

这是开放生成最重要的工程边界之一。

### Hard Constraint

违反就应直接 fail 或进入 guardrail failure：

```text
wrong factual answer
invalid schema
missing mandatory field
unsafe prohibited action
unsupported citation
```

### Soft Preference

允许 trade-off：

```text
more concise
more natural
better organized
more helpful tone
```

如果把二者简单平均：

```text
factuality 0
style 5
average = 2.5
```

这个分数通常没有合理决策语义。

因此建议：

```text
hard gates first
soft ranking second
```

## 9. Pointwise 与 Pairwise 各有什么用？

### Pointwise

回答：

```text
这个回答是否达到某个绝对标准？
```

适合 release gate、rubric compliance。

### Pairwise

回答：

```text
A 和 B 哪个更好？
```

开放质量偏好有时更容易做相对判断。

但 pairwise 也有问题：

```text
A > B
```

不代表：

```text
A 足够好
```

可能只是“两者都差，但 A 稍好”。

因此如果用于 release，pairwise 最好搭配 absolute quality floor。

## 10. Multiple Valid Answers 如何影响 Metric？

开放任务常见：

```text
reference A valid
candidate B also valid
but B not similar to A
```

这会导致传统 reference matching 低估系统。

解决方式可以包括：

```text
multiple references
accepted constraints
semantic / executable equivalence
rubric-based criteria
human / Judge adjudication
```

这与 Q05 直接相连：

> reference 不完整时，不要把“没匹配到 gold”直接等价成“错”。

## 11. Factuality / Groundedness 必须单独测

一段回答可以：

```text
结构好
语言流畅
覆盖充分
```

但包含一个关键 hallucination。

因此 grounded task 至少要独立问：

```text
每个关键 claim 是否有 source support？
引用是否真的支持对应 claim？
有没有 unsupported extrapolation？
```

不要期待一个整体“质量分”自动识别所有事实问题。

## 12. Coverage 与 Concision 存在真实 Trade-off

例如 summary：

```text
更短
```

可能意味着：

```text
更简洁
```

也可能意味着：

```text
漏掉关键事实
```

所以“长度更短”不能直接作为质量提升。

需要联合看：

```text
coverage
redundancy
critical omission
length / cost
```

## 13. Slice 比 Overall 更重要

开放生成 metric 很容易出现 aggregate 看起来稳定，但某类任务明显失效。

推荐切片：

```text
answer length
language
task family
reference availability
factual density
number of required constraints
source length
critical-risk category
Judge confidence / disagreement
```

例如 Judge 在普通解释题上很好，不代表在数字密集回答上同样可靠。

## 14. Aggregation 什么时候才合理？

如果最终业务需要一个 scorecard，可以聚合，但必须先固定：

```text
dimensions
weights
hard-gate rules
missing handling
normalization
aggregation method
```

更推荐：

```text
Primary quality metric
+ critical guardrails
+ supporting dimensions
```

而不是：

```text
所有指标平均成一个“AI quality score”
```

## 15. Evaluation Design Template

设计开放式生成 Eval 时至少回答：

```text
1. Claim 是什么？
2. 哪些 quality dimensions 是必须的？
3. 哪些是 hard constraints？
4. 哪些是 soft preferences？
5. 每个维度最强 evidence 是什么？
6. Reference 是否覆盖 valid-output space？
7. Judge / human 是否经过 calibration？
8. 哪些 slice 最容易失效？
9. 是否需要 pointwise、pairwise 或二者？
10. 是否真的需要一个 overall score？
11. 如果聚合，权重和 failure rule 是什么？
12. 如何报告 uncertainty / disagreement？
```

## 16. 一个最小 Evidence Portfolio

对于开放式回答，可以是：

```text
Task correctness
→ deterministic / reference evidence

Groundedness
→ source support check

Coverage
→ required-point checklist

Instruction following
→ constraint validator + rubric

Clarity / preference
→ calibrated Judge / human
```

这通常比任何一个单独 automatic metric 更可解释。

## 17. Common Wrong Answers

### 错误 1：ROUGE / BLEU 低，所以回答差

可能只是 paraphrase。

### 错误 2：embedding similarity 高，所以回答正确

关键实体、数字、否定关系仍可能错。

### 错误 3：Judge 很强，所以一个 Judge score 就够

Judge 仍有 bias、variance 和 blind spot。

### 错误 4：开放任务太主观，没法严格评测

很多子维度其实可以 deterministic / source-grounded verify。

### 错误 5：多指标最后平均一下就好

hard failure 不能总被 soft preference 抵消。

### 错误 6：human score 就天然是 gold

human 也有 disagreement、rubric drift 和 fatigue，需要 protocol / adjudication。

## 18. Counterexample / Boundary

有些任务虽然输出很长，但真正 estimand 很窄。

例如：

```text
“请给出结论并解释原因”
```

如果产品决策只关心最终分类是否正确，那么 classification correctness 可以仍是 primary deterministic metric；解释质量只是 supporting diagnostic。

因此：

> 输出开放，不代表最终 estimand 一定开放。

## 19. VeriAgent Example

假设 VeriAgent 对 Olist 数据返回：

```text
“共有 12,431 个符合条件的订单，因为我按 customer_id 聚合并过滤了……”
```

可以拆成：

```text
12,431 是否正确？
→ frozen reference / independent computation

SQL / aggregation 是否有效？
→ executable / trace evidence

解释是否与实际 SQL 一致？
→ grounding / trace consistency

是否清楚说明关键口径？
→ checklist + calibrated Judge / human
```

如果只用一个整体 Judge score，可能出现：

```text
数字错
但解释流畅
→ Judge 给高分
```

也可能出现：

```text
数字和逻辑都对
但措辞不像 reference
→ lexical metric 偏低
```

所以正确做法不是选“最聪明的单指标”，而是拆 evidence channel。

## 20. 与 Q05 的关系

Q05 回答：

> reference-based 还是 reference-free？

Q06 进一步回答：

> 即使决定使用 reference-free / open-ended evaluation，为什么也不能自动退化成一个通用 automatic score？

两者合起来：

```text
先选证据来源
→ 再拆质量维度
→ 再选 evaluator
→ 最后决定是否聚合
```

## 21. Follow-up Questions

- ROUGE 什么时候仍然值得保留？
- semantic metric 与 Judge 的角色有什么区别？
- open-ended task 如何建立 release gate？
- pairwise preference 能否替代 absolute rubric？
- 多个 Judge ensemble 是否就解决 bias？
- human disagreement 应如何进入最终 uncertainty？

## 22. Evidence of Mastery

达到 S2/S3 时，应能拿到一个开放生成任务后，独立设计：

```text
quality dimension map
hard vs soft criteria
reference strategy
per-dimension evaluator
Judge calibration
slice plan
aggregation / non-aggregation rule
decision contract
```

并能指出至少三个“单一 automatic metric 看起来合理但会失效”的具体反例。

## Related Knowledge

- [Q04 Metric Design](03_Metric_Design.md)
- [Q05 Reference-based vs Reference-free Evaluation](04_Reference_Based_and_Reference_Free_Evaluation.md)
- [Q08 Judge Reliability](../02_Grader_and_LLM_as_a_Judge/02_Judge_Reliability_and_Calibration.md)
- [Q09 Judge Bias](../02_Grader_and_LLM_as_a_Judge/03_Judge_Bias_and_Failure_Modes.md)
- [Q10 Rubric and Scoring Protocol](../02_Grader_and_LLM_as_a_Judge/04_Rubric_and_Scoring_Protocol.md)
- [Q30 Correlation Does Not Replace Human Judgment](../06_Statistics_and_Experiment_Design/07_Correlation_Does_Not_Replace_Human_Judgment.md)
