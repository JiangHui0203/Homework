# Q05 Reference-based vs Reference-free Evaluation：什么时候该依赖参考答案，什么时候不该？

- Level: M2
- Mastery: S0
- Related Parts: Part 1 / Part 2 / Part 5
- Related Patterns: P02 Deterministic First, Judge Last; P08 Judge Calibration Before Scale
- Related Questions: Q04 Metric Design, Q07 Grader / Verifier / Judge, Q21 Benchmark Design

## 30-second answer

选择 reference-based 还是 reference-free，不是看任务“主观不主观”，而是看：**是否存在可靠、独立、覆盖有效答案空间的 reference，以及它能否支持当前 claim。**

如果正确行为可以被明确 reference、可执行结果、结构化约束或环境状态验证，优先使用 reference-based / deterministic evidence；如果任务存在大量同样合理的输出、没有唯一 gold，或者目标是风格、帮助性、解释质量等开放维度，就需要 reference-free evaluation。

但：

> **reference-free ≠ evidence-free。**

没有单一 gold answer 时，仍然需要 task contract、source evidence、rubric、human / calibrated Judge、环境反馈或其他独立证据来约束判断。

## 90-second answer

我通常按“最强可用证据”而不是按“最流行 metric”选择 evaluator：

```text
Executable / environment truth
→ deterministic structured reference
→ accepted-reference set / tolerance
→ source-grounded rubric
→ calibrated human / LLM Judge
```

例如数学、SQL、代码执行、分类标签，如果有可靠 oracle，就没必要先让 LLM Judge 猜对错；而 summarization、解释质量、对话帮助性往往没有唯一 reference，此时应把质量拆成多个 criteria，再用 source grounding、rubric、pairwise comparison、human/Judge 等证据组合评估。

真正需要避免的是两个极端：

```text
有 reference → 直接字符串匹配
```

以及：

```text
没有唯一 reference → 只能主观打分
```

前者可能误伤等价答案，后者忽略了大量仍可 deterministic verify 的局部性质。

---

## 1. Reference 到底是什么？

Reference 不只是“一条标准答案文本”。

可以包括：

```text
canonical answer
accepted answer set
structured label / schema
executable program / SQL
expected environment state
unit-test outcomes
constraint set
gold evidence spans
human-authored rubric anchor
```

因此首先要问的不是：

> 有没有一段 gold text？

而是：

> 有没有独立、可靠的 expected behavior / outcome 可以作为比较基准？

## 2. Reference-based Evaluation

Reference-based evaluation 的核心是：

```text
observed output / behavior
vs
predefined expected output / behavior
```

常见任务：

- classification；
- extraction；
- numerical QA；
- math；
- code；
- SQL / structured query；
- deterministic tool-use contract；
- regression fixture；
- known environment state transition。

### 它的优势

```text
reproducible
cheap to scale
low evaluator variance
clear error analysis
suitable for regression / CI
```

但前提是 reference 本身可靠。

## 3. 有 Reference 不等于只能 Exact Match

这是最常见误区之一。

存在 reference 时，scoring 可以是：

```text
exact match
normalized match
set / unordered match
numeric tolerance
schema validation
semantic equivalence
unit tests
execution result
state comparison
```

例如：

```text
reference = 0.333333
prediction = 1/3
```

字符串不同，不代表答案不同。

因此要区分：

```text
Reference availability
≠ Matching rule
```

## 4. Reference-based Evaluation 的主要风险

### 4.1 Reference 不完整

开放任务可能有很多 valid outputs，但 benchmark 只存一个 reference。

于是：

```text
valid answer
→ does not match narrow gold
→ false negative
```

### 4.2 Annotation / Reference Error

Gold 本身也可能错。

所以：

```text
reference label
≠ metaphysical ground truth
```

关键 benchmark 应有 reference audit、adjudication 或独立交叉验证。

### 4.3 Common-mode Failure

如果：

```text
SUT 用实现 A 计算
reference 也复用实现 A
```

两边共享 bug，就可能把错误当正确。

因此高价值 benchmark 尽量使用独立 reference path。

### 4.4 Stale Reference

工具、知识、环境会变化。

旧 reference 可能从“正确答案”变成“历史答案”。

时间敏感任务必须保存：

```text
reference version
time / snapshot
environment version
```

### 4.5 Surface-form Bias

只看 lexical overlap 会惩罚正确 paraphrase，也可能奖励复制 reference 但事实错误的输出。

## 5. 什么是 Reference-free Evaluation？

Reference-free 并不是“完全没有比较基准”。

它更准确地表示：

> **不依赖一个预先给定的唯一 gold output 来评分。**

常见目标：

- helpfulness；
- relevance；
- coherence；
- explanation quality；
- instruction following；
- conversational quality；
- style；
- summarization quality；
- multi-valid solution preference。

此时 evaluator 仍然可以依赖：

```text
user instruction
source document
system policy
tool observation
environment state
rubric
human preference
calibrated Judge
```

所以：

```text
reference-free
≠ contract-free
≠ evidence-free
≠ evaluator-free
```

## 6. Reference-free 什么时候更合理？

### A. Valid-output space 很大

例如：

```text
“解释为什么这个实验不能支持因果结论”
```

可能有很多不同但正确的表达。

单一 gold answer 不应成为唯一真值。

### B. 目标本身是偏好或质量维度

例如：

```text
哪一个回答更清楚？
哪个总结更覆盖核心信息？
哪个回复更符合用户约束？
```

这些问题更适合 rubric / pairwise / human-Judge evaluation。

### C. Gold 制作成本过高

某些复杂输出难以为每题创建完整 gold，但可以构建：

```text
source evidence
constraint checklist
critical error rubric
human anchor sample
```

以较低成本评估。

## 7. Reference-free 的核心风险

最大风险不是“没有 gold”，而是 evaluator validity 不明确。

例如使用 LLM Judge：

```text
Judge score high
```

只说明这个 Judge 按当前 prompt / rubric 给了高分。

它不自动说明：

```text
human agrees
factuality correct
product outcome improved
critical errors absent
```

因此要连接 Q08–Q11：

```text
calibration
agreement
repeat stability
bias probes
critical slices
adjudication
```

## 8. Multi-valid Outputs 应怎样处理？

不要在“reference-based”和“reference-free”之间做假二选一。

可以使用：

### Accepted Reference Set

```text
{valid_A, valid_B, valid_C}
```

### Canonicalization

把等价输出规范化，例如：

```text
JSON key order
units
whitespace
case
set ordering
```

### Tolerance / Equivalence Rule

例如：

```text
numeric tolerance
semantic equivalence
program execution equivalence
```

### Constraint-based Verification

不要求答案长得像 reference，只检查必须满足的约束。

这类设计常常比“彻底 reference-free”更可靠。

## 9. Hybrid Evaluation 通常最好

现实 LLM / Agent 输出往往同时包含：

```text
可验证部分
+
开放部分
```

例如一个 Data Agent：

```text
最终数字      → deterministic / reference-based
SQL 是否有效  → executable verifier
证据是否支持  → grounding checks
解释是否清楚  → rubric / Judge / human
```

因此推荐：

```text
Deterministic where possible
+ Reference-based where reliable
+ Reference-free only where necessary
```

而不是强迫整条输出只使用一种 evaluator。

## 10. Evidence Ladder

在同等可行条件下，可优先考虑：

```text
1. Environment / executable outcome
2. Deterministic contract / structured reference
3. Independent gold / accepted reference set
4. Source-grounded scoring
5. Human adjudication / calibrated Judge
6. Weak proxy metric
```

这不是绝对排名；关键仍是它是否真正对应当前 claim。

例如用户偏好本身就是 estimand 时，human preference 不是“弱于 executable outcome”，而是直接证据。

## 11. Claim 决定 Reference Strategy

同一输出可以有不同 claim。

例：一段摘要。

### Claim A

```text
是否覆盖了指定 5 个关键事实？
```

可以 reference / checklist-based。

### Claim B

```text
事实是否都能由 source 支持？
```

可以 source-grounded verification。

### Claim C

```text
是否读起来更清楚？
```

更适合 human / calibrated Judge。

所以：

```text
same output
≠ one universal evaluator
```

## 12. Evaluation Design

为一个任务选择 reference strategy 时，至少回答：

```text
1. Claim 是什么？
2. Valid behavior space 有多大？
3. 是否存在独立可靠的 reference / oracle？
4. Reference 是否覆盖 multiple valid outputs？
5. 哪些维度可以 deterministic verify？
6. 哪些维度必须依赖 human / Judge？
7. Evaluator 本身如何校准？
8. Reference / evaluator 是否与 SUT 共享 failure mode？
9. 时间 / 环境变化是否会让 reference 过期？
10. 最终 decision 需要多高的证据强度？
```

## 13. Common Wrong Answers

### 错误 1：有 gold 就用 exact match

Gold 存在不代表 surface form 必须一致。

### 错误 2：开放任务没有标准答案，所以只能 LLM Judge

仍可能存在 deterministic constraint、source grounding、environment outcome 等更强证据。

### 错误 3：reference-free 就是不需要 ground truth

它只是没有唯一预写 gold output；evaluator validity 仍需证据。

### 错误 4：Judge 比 reference 更智能，所以应该统一用 Judge

能 deterministic verify 的事实交给 Judge，通常只会引入额外 variance 与 bias。

### 错误 5：reference-based 一定客观

错误、狭窄、过期或共享 bug 的 reference 同样会系统性误导。

## 14. Counterexample / Boundary

一个 creative-writing benchmark 可能根本不存在唯一 gold story。

但其中仍可以有明确 hard constraints：

```text
必须使用第一人称
不得超过 500 字
必须包含给定角色
不得泄漏指定信息
```

这些部分可以 deterministic check；“是否有感染力”再交给 human / calibrated Judge。

因此：

> 开放任务也可以拆出 reference-based 子问题。

## 15. VeriAgent Example

VeriAgent 的 Olist challenge 是典型 reference-based 场景：

```text
generated SQL / numeric answer
→ frozen reference SQL
→ independent Python cross-check
→ tolerance / execution evidence
```

这里数值正确性有强 reference，就不应让 LLM Judge 成为主要 oracle。

但如果以后评价：

```text
“最终解释是否清楚地告诉用户为什么这个数字可信”
```

这部分就没有必要要求唯一 gold paragraph，可以拆为：

```text
数字正确性            → deterministic
是否引用真实计算证据  → grounding
解释完整性 / 清晰度   → rubric + calibrated Judge / human
```

这就是 hybrid evaluation。

## 16. Follow-up Questions

- 多个 reference 仍覆盖不了所有 valid outputs 怎么办？
- reference 与 Judge 冲突时谁优先？
- reference 本身怎样做质量审计？
- 什么情况下 human preference 才是直接 estimand？
- source-grounded evaluation 算 reference-based 还是 reference-free？

最后一个问题不必执着命名。更重要的是明确：

```text
评分依赖了什么证据
以及它能支持什么 claim
```

## 17. Evidence of Mastery

达到 S2/S3 时，应能拿到一个新任务后独立画出：

```text
Claim
→ Valid output space
→ Strongest available evidence
→ Reference / reference-free split
→ Evaluator
→ Calibration / reference audit
→ Failure modes
→ Decision boundary
```

并能解释为什么不是“所有任务都 exact match”或“所有开放任务都交给 Judge”。

## Related Knowledge

- [Q04 Metric Design](03_Metric_Design.md)
- [Q06 Open-ended Generation Evaluation](05_Open_Ended_Generation_Evaluation.md)
- [Q07 Grader / Verifier / Judge](../02_Grader_and_LLM_as_a_Judge/01_Grader_Verifier_and_Judge.md)
- [Q08 Judge Reliability](../02_Grader_and_LLM_as_a_Judge/02_Judge_Reliability_and_Calibration.md)
- [Q21 Discriminative Benchmark Design](../05_Benchmark_and_Evaluation_Data/01_Discriminative_Benchmark_Design.md)
