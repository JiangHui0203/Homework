# Q36 Post-training 后如何证明改善来自目标能力，而不是 Benchmark 记忆或评测协议漂移？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 5 / Part 6 / Part 7 / Part 8
- Related Patterns: P03 Paired Same-Task Comparison; P05 Frozen Core + Rotating Hard Set; P11 Holdout after Development; P12 Mechanism ≠ Outcome
- Canonical Data Owner: `LLM_Agent_Data/21_Data_Experiments_and_Causal_Validation.md`
- Related Case: VeriAgent candidate memory frozen paired evaluation

## 30-second answer

Post-training 之后看到 benchmark 分数提高，只能先说明：**在当前 evaluation protocol 下观察到更高分**。要证明提升来自目标能力，至少要控制三类混淆：

1. **训练干预本身**：baseline / treatment 的 base checkpoint、训练预算、数据 manifest、训练 protocol 是否可比；
2. **评测独立性**：primary holdout 是否没有进入训练、prompt、memory、规则或 model selection；
3. **测量稳定性**：task、reference、evaluator、environment、budget、aggregation 是否冻结，没有 protocol drift。

更强证据还应包括：target slice 改善、fresh holdout 泛化、邻近任务 transfer、mechanism check、general regression suite 与 cost / latency guardrails。

核心链路是：

```text
Frozen baseline
+ controlled intervention
+ frozen / fresh evaluation
+ target-specific effect
+ regression audit
+ mechanism-consistent evidence
```

而不是：

```text
train
→ old benchmark score ↑
→ capability improved
```

## 90-second answer

我会把 post-training 验证设计成一个 **Intervention Validation Contract**。

训练前就冻结：

```text
Research question
Base checkpoint
Baseline data / treatment data manifests
Training budget matching rule
Seed policy
Primary target capability
Primary clean holdout
Regression benchmarks
Evaluator / reference versions
Cost / latency guardrails
Decision rule
```

训练后至少分四层证据：

```text
L1 Exposed / training-adjacent set improved
L2 Clean frozen holdout improved
L3 Fresh / rotating holdout improved
L4 Mechanism + transfer + regression evidence agree
```

其中 L1 可以说明优化成功，但不能证明泛化；L2/L3 才开始支持 unseen-task improvement。

如果 test failure 已经被用来造训练数据，那么旧 test 必须标记为 exposed。它仍可作为 regression set，但不能继续当 fresh evidence。

同时还要避免 protocol drift：如果 candidate 用了更大 context、更高 token budget、更宽 retry、不同 Judge 或不同 reference，那么“分数变高”不再是单纯的 model/data effect。

---

# 1. 先定义因果对象：到底改了什么？

Post-training experiment 的 treatment 应尽量明确。

一般写成：

```text
Baseline:
  Train(M0, B, T)

Treatment:
  Train(M0, I_D(B), T)
```

其中：

```text
M0  = same base checkpoint
B   = baseline data mixture
I_D = data intervention
T   = matched training protocol
```

如果同时改变：

```text
data
optimizer
total tokens
context length
inference scaffold
prompt
budget
```

最终差异就很难归因给“这批数据”。

Evaluation 侧不负责训练细节，但必须知道 treatment contract 是否足够干净，才能解释 outcome。

---

# 2. Data Quality ≠ Learning Value

即使训练数据：

```text
人工审核通过
reference 可验证
重复率低
格式正确
```

也只能说明数据质量不错。

真正要验证的是：

```text
目标能力提高了吗？
在 unseen tasks 上提高了吗？
有没有伤害别的能力？
收益是否超过成本？
```

所以：

```text
high-quality data
≠ useful intervention
```

Learning value 是 intervention 后的结果属性。

---

# 3. Matched Budget 是最基本的归因控制

假设：

```text
Baseline training = 10B tokens
Treatment training = 12B tokens
```

Treatment 分数更高，可能只是因为：

```text
more compute / more exposure
```

而不是数据 composition 更好。

更有解释力的比较：

```text
same total tokens
same base checkpoint
same optimizer schedule
same number of steps
only mixture / data policy differs
```

如果不能完全 matched，也必须清楚报告差异并降低因果 claim。

---

# 4. Benchmark Memory 是 Post-training 验证的首要威胁

典型污染链：

```text
benchmark failure
→ human reviews answer
→ creates SFT / preference / synthetic variants
→ trains candidate
→ reruns same benchmark
→ score increases
```

这个提升可以是真实“已知题修复”，但不能直接叫：

```text
unseen capability improvement
```

因为 benchmark 已经进入 learning loop。

正确处理：

```text
old benchmark
→ DEVELOPMENT_EXPOSED / regression

fresh holdout
→ clean confirmation
```

---

# 5. Frozen Holdout 与 Fresh Holdout 各回答什么？

## Frozen Clean Holdout

如果从头到尾没有参与 development，它适合做：

```text
primary confirmation
```

优点：

```text
same items
stable comparison
```

风险：

随着多轮开发和人工观察，长期可能逐渐暴露。

## Fresh / Rotating Holdout

用于回答：

> 这次改善是否能迁移到新的、未被开发碰过的任务？

因此长期 flywheel 更稳健的 portfolio 是：

```text
Regression / Known-hard
+ Frozen core
+ Fresh rotating confirmation
```

而不是永远只跑一个 test。

---

# 6. Protocol Drift 会伪造“模型进步”

即使数据完全没泄漏，如果 evaluation protocol 变了，也可能出现假提升。

必须冻结或显式记录：

```text
prompt / system instruction
model decoding
context budget
tool versions
environment snapshot
retry policy
timeout
reference
evaluator / Judge version
rubric
aggregation
failed-run handling
```

例如：

```text
Baseline: max 1 retry
Candidate: max 5 retries
```

最终 task success 上升不能简单解释成模型本体更强。

可以说：

```text
system under candidate protocol improved
```

但不能偷换成：

```text
post-trained model capability improved
```

---

# 7. 目标能力改善要看 Target Slice

如果训练目的是：

```text
recovery preference data
```

primary evidence 应优先来自：

```text
recoverable failures
recovery success
false recovery
over-retry
safe-stop confusion
```

而不是只看一个总体 benchmark score。

更强的结果形态：

```text
Target capability ↑
General capability non-inferior
Safety / reliability non-inferior
Cost acceptable
```

如果 overall +2pp，但 target slice 没变，反而别的 easy slice 提升，需要重新检查机制 claim。

---

# 8. Mechanism Check：行为真的按预期改变了吗？

Outcome improvement 与 mechanism improvement 不完全相同。

假设 intervention 目的是：

```text
减少 stale schema 后直接执行错误 SQL
```

那么除了 final accuracy，还应观察：

```text
stale-schema detection
schema refresh behavior
argument correctness
recovery success
first-failure shift
```

如果 final score 涨了，但这些 mechanism 指标完全没变化：

```text
target mechanism attribution weak
```

反过来，如果 mechanism 明显改善但 final score 暂时没涨，也可能说明 downstream bottleneck 仍在。

---

# 9. Transfer Evidence：不要只看训练邻近模板

至少区分：

```text
Exact / near training patterns
Same mechanism, new template
Same capability, new domain condition
Adjacent capability
Out-of-scope capability
```

真正的 capability claim 越大，需要越远的 transfer evidence。

例如：

```text
训练 join_fanout Olist cases
```

在 Olist 新表达上改善，只能先支持领域内迁移；不能直接宣称：

```text
general SQL reasoning improved
```

除非有跨 schema / 数据库 / task family 的证据。

---

# 10. Regression Suite 是“收益没有买来副作用”的证据

Post-training 可能出现：

```text
target ↑
general ↓
latency ↑
over-retry ↑
verbosity ↑
refusal ↑
unsafe action ↑
```

所以验证至少包括：

```text
Primary target metric
Critical safety/reliability metrics
General capability regression
Cost / latency
Stability
```

不要用一个 target gain 抵消 critical regression。

这和 Q34 的 multidimensional release gate 一致。

---

# 11. Data Intervention 的常见对照形式

Evaluation 侧常见要识别的实验：

## Add

```text
B
vs
B + D
```

缺点：训练 token 也可能增加。

## Replace

```text
same total token budget
old bucket → D
```

更适合比较单位预算 learning value。

## Remove

```text
Full
vs
Full - D
```

看 D 是否真正必要。

## Reweight

```text
D: 2% / 5% / 10%
```

看 exposure-response curve。

## Transform

```text
same raw cases
but different supervision construction
```

例如：

```text
SFT vs preference
single answer vs recovery trajectory
```

具体训练实验属于 Data canonical chapter；Eval 负责保证比较可解释。

---

# 12. Seed 与 Training Stochasticity

一次训练 run 的提升可能受：

```text
initialization
batch order
optimizer stochasticity
sampling
```

影响。

如果成本允许，对关键 experiment 应考虑：

```text
multiple training seeds
```

但不能把多个 seed 当成多个 independent benchmark tasks。

需要区分：

```text
training-run variability
vs
evaluation-task sampling uncertainty
```

两层 uncertainty 不同。

---

# 13. 最小 Post-training Validation Report

建议固定：

```text
Research question
Target capability
Base checkpoint
Baseline data manifest
Treatment data manifest
Training protocol
Budget matching status
Training seeds
Evaluation benchmark versions
Exposure status
Primary metric
Primary effect + CI
Target slice effects
Fresh holdout result
Regression metrics
Cost / latency / stability
Mechanism checks
Known confounders
Decision
Interpretation boundary
```

没有 exposure status 与 fresh confirmation，报告非常容易把 benchmark repair 写成泛化提升。

---

# 14. Evidence Ladder

可以用一个简单的证据阶梯理解 claim 强度：

```text
E0 Training loss better
↓
E1 Exposed / train-adjacent eval better
↓
E2 Frozen clean holdout better
↓
E3 Fresh / rotating holdout better
↓
E4 Target mechanism + transfer evidence agree
↓
E5 Regression / cost / safety remain acceptable
```

不是每个项目都必须一次达到 E5，但 claim 不能超过证据层级。

例如只有 E1：

```text
可以说：intervention fits known cases better
不能说：general capability improved
```

---

# 15. 什么时候可以说“目标能力提高”？

一个相对稳健的最低组合：

```text
1. treatment contract clear
2. evaluation protocol frozen
3. primary holdout not used in development
4. target metric improves with uncertainty reported
5. target slice / mechanism evidence consistent
6. important regressions acceptable
7. claim scope matches benchmark scope
```

如果 holdout 已暴露，则需要 fresh confirmation 补回独立性。

---

# Evaluation Design

一个推荐 pipeline：

```text
Pre-register research question
↓
Freeze base + data manifests + training budget
↓
Freeze clean holdout + regression suite
↓
Train baseline / treatment
↓
Run same eval harness
↓
Target effect + uncertainty
↓
Mechanism / slice check
↓
Regression / cost / latency
↓
Fresh rotating confirmation
↓
Decision + exposure ledger update
```

---

# Common Wrong Answers

## 错误 1：训练后 benchmark 涨了，所以训练数据有效

如果 benchmark case 进入过训练或开发，只能先说明已知 set 改善。

## 错误 2：same benchmark、same accuracy metric，所以 protocol 一样

prompt、budget、retry、Judge、environment 变化都会改变测量语义。

## 错误 3：overall 提升，所以目标 capability 提升

可能提升来自非目标 slice。

## 错误 4：target slice 提升，所以训练数据因果有效

还需要控制 base model、training budget、其它数据和 protocol。

## 错误 5：fresh set 不需要 regression set

fresh set 测泛化；regression set 防已知 failure 回来，职责不同。

---

# Counterexample / Boundary

如果只做 prompt / memory / controller 更新，没有改变模型权重，它严格来说不是 post-training。但同一套 validation logic 仍适用：

```text
intervention exposure
frozen comparison
fresh holdout
mechanism attribution
regression / cost
```

因此 Q36 更一般地也是：

> 如何证明一个 learning / policy intervention 产生了目标能力改善？

---

# VeriAgent Example

VeriAgent candidate memory evaluation 是一个很好的“非训练 intervention”例子。

开发阶段：

```text
reviewed dev failures
→ candidate memory v1
→ freeze candidate
```

测试阶段：

```text
12 held-out tasks
× 3 repeats
baseline vs candidate
```

观察到：

```text
29/36 → 30/36
3 wrong→right
2 right→wrong
net +1/36
```

但不能归因于 candidate memory，因为：

```text
13 failures happened before SQL-stage memory retrieval
```

而 candidate 只影响 SQL generation stage。

这说明：

```text
Outcome delta
≠ intervention mechanism attribution
```

即使未来统计 evidence 更强，也必须检查 intervention 是否有机会作用于发生变化的路径。

## Follow-up Questions

- 一个旧 test 被用于 hard-case training 后应该怎样重新分类？
- matched-budget 为什么比简单 Add data 更有解释力？
- target slice 提升但 overall 不变时如何判断？
- training seeds 和 evaluation repeats 分别解决什么 uncertainty？
- fresh holdout 每轮都更换会不会失去长期可比性？

## Evidence of Mastery

达到 S4 时，应能为一次 post-training / policy update 独立设计：

- intervention contract；
- exposure ledger；
- matched comparison；
- primary / regression metrics；
- clean + fresh holdout strategy；
- mechanism check；
- uncertainty；
- release decision；
- 合理、不过度的 capability claim。

## Related Knowledge

- [Q03 What Are We Measuring](../01_LLM_Evaluation/02_What_Are_We_Measuring.md)
- [Q22 Leakage & Test-set Overfitting](../05_Benchmark_and_Evaluation_Data/02_Leakage_and_Test_Set_Overfitting.md)
- [Q25 Is the Improvement Credible](../06_Statistics_and_Experiment_Design/02_Is_the_Improvement_Credible.md)
- [Q34 Multidimensional Eval Reporting](../07_Eval_Engineering/05_Multidimensional_Eval_Reporting.md)
- `LLM_Agent_Data/21_Data_Experiments_and_Causal_Validation.md`
