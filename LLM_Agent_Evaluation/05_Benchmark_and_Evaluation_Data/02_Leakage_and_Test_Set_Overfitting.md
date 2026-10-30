# Q22 如何避免 Benchmark Leakage、Test-set Overfitting 和反复开发造成的伪提升？

- Level: M1
- Mastery: S0
- Related Parts: Part 5 / Part 6 / Part 7 / Part 8
- Related Patterns: P03 Paired Same-Task Comparison; P05 Frozen Core + Rotating Hard Set; P10 Replayable Evaluation; P11 Holdout after Development
- Related Registry: `BENCHMARKS.md`

## 30-second answer

Leakage 不只是“训练集里见过测试题”。任何本应只用于最终验证的信息，如果通过 prompt、memory、人工调试、error review、阈值选择、benchmark 多轮反复查看或 evaluator 设计进入了开发决策，都可能让 test 不再独立。

我会把开发资产和确认资产分开：**dev 可以反复看；holdout 不参与修方法；根据 dev failure 改过系统后，用冻结未见 test 验证；长期高频评测再配 rotating / fresh set。** 同时记录 benchmark exposure ledger，知道每个 set 被谁、在什么阶段、以什么形式看过。

## 90-second answer

我把 contamination 分成几层：

```text
pretraining / public contamination
train ↔ eval item overlap
dev → test near-duplicate leakage
test feedback → system tuning
human / agent memory writeback
reference / answer leakage into prompts
evaluator leakage
environment state contamination
```

其中最容易被忽略的是 adaptive test overfitting：每次都“只看测试分数”，但根据它改 prompt、controller、threshold、memory、case rule，经过很多轮后测试集已经事实上变成开发集。

因此要冻结：split、reference、evaluator、metric、budget、threshold 和 test access policy。测试结果用于一次确认；如果决定根据 test failure 修改系统，那么旧 test 应降级为 regression evidence，下一轮主要确认需要新的 holdout / fresh set。

## 1. Leakage 不只发生在模型训练

### A. Pretraining / Public Contamination

模型可能在预训练中见过公开 benchmark 题目或答案。

### B. Data Split Leakage

train/dev/test 之间存在：

- exact duplicate；
- semantic near-duplicate；
- shared template；
- same source entity；
- same trajectory continuation；
- derived answer / paraphrase。

### C. Development Leakage

你根据 test failure 修改：

```text
prompt
controller
rules
threshold
memory
retrieval
retry policy
```

那么 test 已经影响系统开发。

### D. Runtime Leakage

评测运行中把：

```text
reference answer
family label
wrong-answer pattern
test metadata
```

发送给被测系统。

### E. Memory / State Leakage

测试结果写入 memory，再用于同一 test set 后续 episode，会破坏独立性。

### F. Evaluator Leakage

如果 Judge / grader 提示中包含 system identity、candidate/baseline 标记、期望结论或 gold explanation，也可能污染评判。

## 2. Test-set Overfitting 是 Adaptive Data Analysis

典型循环：

```text
run test
→ 看失败
→ 改 prompt
→ run same test
→ 看失败
→ 加规则
→ run same test
→ ...
```

即使没有梯度训练，开发者也在通过 test feedback 优化系统。

因此：

> “没有训练模型权重”并不意味着“没有对 test overfit”。

规则系统、Agent controller、prompt、memory 同样能 overfit。

## 3. Dev / Test / Regression 的角色要分开

### Dev

允许：

```text
看逐题结果
看 trace
做 failure analysis
改方法
调阈值
```

### Frozen Holdout

目标：回答“改完后是否在未参与开发的数据上仍成立”。

限制：

```text
运行前冻结
不用于调参
reference 不进 prompt
运行中不写回学习状态
```

### Regression Set

一旦某个 test failure 被你深入研究并修复，它很适合进入 regression set。

但它不再是“完全未见”的 confirmation evidence。

## 4. Exposure Ledger

建议给 benchmark / item 记录：

```text
benchmark_id
version
item_id
first_seen_by_model?
first_seen_by_developer?
used_for_debugging?
used_for_threshold_selection?
used_for_memory/data construction?
used_for final confirmation?
last_exposure_date
```

不是为了形式主义，而是避免几年后没人知道“这个 test 到底还干不干净”。

## 5. Near-duplicate 比 Exact Duplicate 更危险

完全重复容易查。

更隐蔽的是：

```text
同一 SQL skeleton，只换月份
同一逻辑证明，只换实体名
同一工具路径，只换参数值
同一 source paragraph 的不同问法
```

如果按行随机 split，很可能把同一个 latent template 分到 dev/test 两边。

更好的 split unit 可能是：

```text
group_key
template family
source document
user / account
scenario
entity cluster
```

必须与真正的泛化 claim 对齐。

## 6. Reference Leakage

下面这些都可能让 benchmark 失效：

```text
prompt 中出现 gold answer
reference SQL 暴露给 Agent
error family label 暴露
典型错误答案值暴露
Judge rationale 被用于下一次生成
```

评测 harness 应做到：

```text
SUT inputs
⊥
scoring-only artifacts
```

也就是被测系统与评分资产分层保存。

## 7. Test Failure 被看过之后怎么办？

不要假装没看过。

合理处理：

```text
old holdout failure
→ explicit review
→ fix
→ promote case to regression / known-hard set
→ confirm on untouched holdout / fresh set
```

旧测试仍然有价值，只是它的证据角色发生变化。

## 8. 多轮开发时用 Fresh / Rotating Set

当系统长期迭代、每周/每天评测时，单一 frozen test 很容易逐渐被开发过程“记住”。

可以组合：

```text
Frozen Core
+ Regression Set
+ Rotating / Fresh Set
```

Frozen Core 保证纵向可比；Regression 阻止已知 bug 复发；Rotating/Fresh 提供新鲜 confirmation evidence。

## 9. Benchmark Versioning

至少保存：

```text
benchmark version
item manifest / hashes
split manifest
reference version
evaluator version
metric / threshold version
environment / tool snapshot
```

如果 benchmark 内容变了，不能继续把新旧分数当同一条时间序列比较。

## 10. 如何报告污染风险

不是只有 `clean / contaminated` 两种。

建议分：

```text
KNOWN_CLEAN
CONTROLLED_EXPOSURE
DEVELOPMENT_EXPOSED
PUBLIC_CONTAMINATION_RISK
UNKNOWN
```

并说明具体 exposure。

## Evaluation design

### Holdout Protocol

在正式 confirmation 前冻结：

```text
system version
benchmark version
reference
metric
threshold
budget
repeats
randomization
memory snapshot
writeback policy
```

运行完成前不要针对测试结果改系统。

### Leakage Audit

至少检查：

```text
exact duplicate
semantic / template duplicate
source overlap
group overlap
reference-in-prompt
state writeback
human review exposure
public contamination risk
```

## Common wrong answers

### 错误 1：我们没有 fine-tune，所以不存在 test overfit

prompt / rule / memory / controller 都可以通过 test feedback 过拟合。

### 错误 2：只要文本不一样，就不是 leakage

共享 solution template / source entity / scenario 仍可能造成近重复泄漏。

### 错误 3：测试失败修复后继续跑同一 test 就能证明泛化

它可以证明 bug 没复发，但不再是独立 holdout evidence。

### 错误 4：公开 benchmark 没法确定预训练污染，所以没必要做

不能完全消除风险，但可以记录风险、加入 fresh/private set、避免过度解读。

### 错误 5：candidate 和 baseline 都看过 test，所以公平

对比可能仍公平，但 test 已失去独立 confirmation 语义。

## Counterexample / boundary

CI regression suite 本来就会被开发者反复查看。它不需要假装是“未见测试集”；它的价值是稳定复现历史关键行为。问题不是 exposure 本身，而是把 exposed regression score 错解释成独立泛化证据。

## VeriAgent example

VeriAgent challenge evaluation 的开发流程把 12 道 dev 与 12 道 held-out test 在模型运行前冻结。开发集失败经过显式 review 后构造候选 memory；测试集运行时不修改候选，也不把测试失败写回 memory。

测试后发现 candidate 的失败主要发生在 memory 能作用之前，因此这个 test 结果仍能支持“当前 memory 不能解释这些失败”。但如果下一轮根据这些 test failures 修改分析阶段，再用同一 12 题宣称独立泛化，就不再成立；这些题更适合转为 regression / known-hard evidence，再用新 holdout 确认。

## Follow-up questions

- exact duplicate 与 template leakage 怎么区分？
- test 运行多少次之后算“被开发污染”？
- public benchmark 还能不能用于研究？
- rotating set 如何保持纵向可比？
- human review 是否也算 exposure？

## Evidence of mastery

达到 S4 时，应能给一个长期迭代的 Agent eval 设计：

- split unit；
- exposure ledger；
- dev / holdout / regression boundary；
- memory / state writeback policy；
- benchmark versioning；
- fresh-set confirmation plan；
- leakage-risk reporting。

## Related knowledge

- [Q21 Discriminative Benchmark Design](01_Discriminative_Benchmark_Design.md)
- [Q23 Benchmark Set Roles](03_Frozen_Regression_Hard_and_Rotating_Sets.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
- [Benchmarks Registry](../BENCHMARKS.md)
