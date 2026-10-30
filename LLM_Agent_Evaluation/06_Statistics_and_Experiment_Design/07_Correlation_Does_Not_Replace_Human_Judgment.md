# Q30 相关性高是否意味着 Evaluator 可以替代 Human Judgment？

- Level: M2
- Mastery: S0
- Related Parts: Part 2 / Part 6
- Related Patterns: P08 Judge Calibration Before Scale; P04 Slice Before Aggregate
- Related Metrics: Judge-Human Agreement, Human-Human Agreement, Score Offset / MAE, Critical-slice Error Rate

## 30-second answer

不意味着。高 correlation 只能说明两个 evaluator 的分数或排序一起变化，不能证明它们逐样本一致、尺度校准一致、threshold decision 一致，也不能保证关键 slice 上没有系统性错误。

例如：

```text
Human: 1,2,3,4,5
Judge: 3,4,5,6,7
```

相关性可以接近 1，但 Judge 存在稳定 +2 的 scale shift。如果 release gate 是 `score >= 4`，两者会做出不同决策。

要论证“可替代人工”，至少还要看 agreement、MAE / offset、critical-slice errors、重复稳定性、bias robustness、human-human reference、adjudication 结果，以及在真实决策 threshold 上的 false accept / false reject。

## 90-second answer

我会先区分三种 claim：

```text
A. Judge 能否做粗粒度 ranking proxy？
B. Judge 能否辅助 triage？
C. Judge 能否 autonomous replace human decision？
```

C 的证据要求远高于 A。

Correlation 主要回答“变化趋势是否一致”，而 replacement 关心“最终决定是否一致且风险可接受”。因此至少要检查：

```text
agreement
calibration / scale shift
threshold confusion
critical slices
repeatability
bias probes
human-human agreement
adjudication
abstain / escalation policy
```

尤其在 safety、factual correctness、release gating 等高风险场景，即使总体 correlation 很高，只要少量 critical errors 不可接受，就不能把 Judge 当唯一 oracle。

## 1. Correlation 回答的是共同变化，不是逐样本一致

### Pearson-style correlation

更关注线性共同变化。

### Spearman correlation

更关注 rank order 是否一致。

两者都可能很高，但 evaluator 仍可能在绝对分数上系统偏移。

例如：

```text
Human: 1 2 3 4 5
Judge: 3 4 5 6 7
```

排序完全一致，但：

```text
Judge - Human = +2
```

如果要做绝对 threshold decision，这个 bias 很危险。

## 2. Agreement 与 Correlation 不一样

Agreement 关心：

> 同一个 sample 上是否给出相同 / 足够接近的判断？

Correlation 关心：

> 两个变量整体是否一起增减？

因此正式 evaluator validation 至少要同时看：

```text
correlation
agreement
error magnitude
systematic offset
```

不能互相替代。

## 3. Replacement 最关键的是 Decision Agreement

假设上线规则：

```text
score >= 4 → PASS
score < 4  → FAIL
```

即使 Judge 与 Human 的 Spearman ρ=0.95，也要看：

```text
Human PASS, Judge FAIL
Human FAIL, Judge PASS
```

尤其后者可能是 false accept。

因此 evaluator replacement 的真正问题是：

> Judge 在目标 decision policy 下会造成什么错误？

而不是：

> ρ 是否足够漂亮？

## 4. Critical Slice 可以击穿总体高相关

总体：

```text
ρ = 0.92
```

但可能：

```text
ordinary style   ρ = 0.95
factual hard     ρ = 0.70
safety critical ρ = 0.40
```

或者 correlation 仍然高，但 safety slice 有 10% catastrophic false accept。

高风险决策必须看：

```text
critical-slice error rate
```

而不是只看总体 correlation。

## 5. Human-Human Agreement 是参照，不是自动替代阈值

如果 human-human agreement 本身不高，Judge-human disagreement 可能部分来自：

```text
rubric ambiguity
subjective preference
annotation error
task ambiguity
```

所以应同时报告：

```text
human-human
judge-human
judge-repeat
```

但不要机械地说：

> Judge-human 达到 human-human，所以 Judge 可以替代 Human。

Human disagreement 的错误类型和业务代价，与 Judge 系统性 bias 不一定相同。

## 6. Reference Construction 很重要

“Human score”可能是：

```text
single annotator
majority vote
median
mean
expert adjudication
preference distribution
```

不同构造方式代表不同 target。

如果拿单一 annotator 当绝对 gold，再报告 correlation，可能低估 human noise；反过来，把多个 human 先平均也可能掩盖真实 disagreement。

## 7. Repeatability 是 Replacement 的必要条件之一

一个 Judge 即使平均上与 Human 很相关，但完全相同输入重复评分频繁 flip：

```text
PASS / FAIL / PASS / FAIL
```

也不适合做稳定 gate。

因此至少需要：

```text
Judge repeat consistency
swap consistency
```

以及冻结：

```text
model version
prompt
rubric
decoding
```

## 8. Bias Robustness 不能由 Correlation 代替

Judge 可能受：

```text
position
verbosity
style
self-preference
identity
```

影响。

如果 calibration set 中这些因素与真实 quality 恰好相关，总体 correlation 甚至会很好看，但一旦分布变化，bias 就暴露出来。

因此需要 controlled perturbation probes。

## 9. Replacement Claim 应分风险等级

### Low-risk ranking / triage

可以接受：

```text
较高相关
+ 可接受 agreement
+ 人工抽查
```

### Advisory scoring

需要：

```text
校准
repeat stability
slice reliability
```

### Autonomous release / safety gate

通常要求更严格：

```text
strong anchor validation
low critical error
abstention / escalation
replayability
continuous monitoring
```

不要把“可辅助排序”直接升级成“可替代人工”。

## 10. Distribution Shift 会让历史 Correlation 失效

Judge 在校准集表现很好，不代表未来：

```text
new domain
new language
new response style
new model family
new task difficulty
```

仍然可靠。

Replacement 需要持续监控：

```text
agreement drift
critical-slice drift
score distribution shift
adjudication rate
```

## 11. 一个最小 Replacement Validation Stack

```text
1. Define intended decision
2. Build reliable human / verifier anchor
3. Freeze Judge contract
4. Measure correlation
5. Measure agreement / MAE / offset
6. Measure threshold confusion
7. Measure repeatability
8. Run bias perturbations
9. Audit critical slices
10. Define abstain / escalation
11. Confirm on fresh holdout
12. Monitor drift after deployment
```

## 12. 什么情况下 Correlation 本身更有价值

如果目标就是：

```text
模型 ranking
relative ordering
trend tracking
```

那么 Spearman / Kendall 可以是重要指标。

但即使是 ranking，也要检查：

- top-k 是否稳定；
- close pairs 是否频繁反转；
- critical system 是否被错误排序；
- ranking 是否跨 slice 保持。

所以 correlation 仍然只是证据的一部分。

## Common wrong answers

### 错误 1：ρ=0.9，所以 Judge 可以替代人

不够。还缺 agreement、threshold error、slice behavior、stability 和 risk analysis。

### 错误 2：Judge-human 达到 human-human，就一定够了

错误类型与代价可能不同。

### 错误 3：相关性高就没有 scale bias

完全可能有固定 offset 或 nonlinear calibration error。

### 错误 4：总体结果好，critical slice 少量错误可以忽略

高风险场景中恰恰可能由 rare critical errors 决定是否可自动化。

### 错误 5：一次 calibration 通过，以后无需复测

任务、模型和分布会 drift。

## Counterexample / boundary

如果 evaluator 只用于低风险内部排序，例如从 1000 个候选样本中挑 100 个进入人工复核，那么高 rank correlation + acceptable recall 可能已经很有价值。

但如果 evaluator 直接决定：

```text
是否发布
是否安全
是否事实正确
```

replacement claim 需要更严格的逐样本 reliability 和 escalation 机制。

## VeriAgent example

VeriAgent 的结构化数值任务优先用 deterministic reference / executable checks，而不是用一个高 correlation 的 Judge 替代可验证证据。

对于失败 root-cause 或开放式质量判断，自动 signal 也只作为 evidence source；复杂 case 仍进入 review / adjudication。这体现了：

```text
可 deterministic verify
→ 不应降级成“相关性很高的主观 Judge”
```

## Follow-up questions

- Pearson / Spearman / Kendall 分别适合什么？
- replacement validation 如何定义 acceptable false accept？
- human-human disagreement 很高时怎么办？
- evaluator drift 应怎么监控？
- triage proxy 与 autonomous oracle 的证据门槛如何区分？

## Evidence of mastery

达到 S3/S4 时，应能看到一句：

```text
Judge-human correlation = 0.9
```

立刻追问：

```text
agreement 呢？
offset / MAE 呢？
threshold confusion 呢？
critical slices 呢？
repeatability 呢？
bias probes 呢？
human reference 怎么构造？
最终要替代哪一种人工决策？
```

## Related knowledge

- [Q08 Judge Reliability](../02_Grader_and_LLM_as_a_Judge/02_Judge_Reliability_and_Calibration.md)
- [Q11 Human Disagreement](../02_Grader_and_LLM_as_a_Judge/05_Human_Disagreement_and_Adjudication.md)
- [Q25 Credible Improvement](02_Is_the_Improvement_Credible.md)
