# Q21 如何构造一个真正有区分度的 Eval Set，而不是简单收集一批题？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 4 / Part 5 / Part 6
- Related Patterns: P01 Eval Contract First; P04 Slice Before Aggregate; P05 Frozen Core + Rotating Hard Set; P11 Holdout after Development
- Related Registry: `BENCHMARKS.md`
- Related Case: VeriAgent Olist Challenge Evaluation

## 30-second answer

一个有区分度的 eval set，不是“题多”或“题难”，而是能针对预先声明的 capability claim，在可靠 reference / evaluator 下，稳定地区分不同系统行为，并且知道这种区分来自哪些能力维度。

我通常先建 **capability × task-family coverage matrix**，再选有证据支持的题：既要避免全是天花板题或地板题，也要包含能暴露关键 failure mode 的 discriminative cases。最后冻结 task、reference、slice、evaluator、版本与 holdout 边界。

关键边界是：

> **Diagnostic / challenge set 可以故意偏难、偏脆弱点；它的分布不能直接当作真实产品分布。**

## 90-second answer

设计 benchmark 时我会先问四个问题：

1. **Claim**：这个 benchmark 要支持什么结论？
2. **Coverage**：结论涉及哪些 capability / task family / environment condition？
3. **Discrimination**：哪些 item 能真正区分合理的系统差异，而不是所有系统都对或都错？
4. **Evidence quality**：reference、evaluator、task contract 是否足够可靠？

然后建立 coverage matrix，例如：

```text
                easy   medium   hard   adversarial
payment_grain     ✓       ✓       ✓
join_fanout       ✓       ✓       ✓       ✓
time_scope        ✓       ✓       ✓
state_memory              ✓       ✓       ✓
```

Item 不只是看最终 pass/fail，还要检查：是否有唯一或可接受的正确行为、错误对照是否真的与 reference 不同、是否存在近重复泄漏、是否被某个模板表面特征轻易 shortcut。

因此 benchmark quality 更像：

```text
clear claim
+ coverage
+ discriminative items
+ reliable oracle
+ controlled protocol
+ known limitations
```

而不是简单的 `N=1000`。

## 1. Benchmark 是 Evaluation Instrument

Benchmark 不是“题库”的同义词。

它实际上是：

```text
Task distribution
+ Environment
+ Reference / evaluator
+ Protocol
+ Aggregation
+ Version
+ Interpretation boundary
```

只保存 prompt，而不保存 reference、环境或 protocol，很难形成稳定的 evaluation instrument。

## 2. 先从 Claim 反推能力覆盖

错误做法：

```text
先收集很多题
→ 再看看能测什么
```

更稳健的是：

```text
Claim
→ target capabilities
→ task families
→ observable behaviors
→ item construction
→ evaluator
```

例如要评价 Data Agent 的结构化分析可靠性，可以拆：

```text
grain / aggregation
identity resolution
join fanout
time scope
schema grounding
safe stop
recovery
```

每个能力都应该有可观察的正确 / 错误行为，而不是只写一个抽象标签。

## 3. Coverage Matrix

Benchmark 至少要知道“什么被覆盖、什么没被覆盖”。

一个实用表：

| Capability | Family | Difficulty | Risk | Count | Reference type | Known gap |
|---|---|---|---|---:|---|---|
| Join correctness | fanout | hard | high | 12 | executable | cross-db missing |
| Safe stop | missing data | medium | high | 8 | deterministic | permission missing |
| Tool choice | schema query | medium | medium | 10 | contract | multi-tool sparse |

没有 coverage map，就无法解释 aggregate score 的边界。

## 4. “有区分度”不等于“越难越好”

### Ceiling item

所有合理系统都能通过：

```text
P(success) ≈ 1
```

价值：回归、sanity check、基础能力。

但大量 ceiling item 对候选差异不敏感。

### Floor item

所有系统都失败：

```text
P(success) ≈ 0
```

可能说明任务超出当前能力，也可能是 task/reference 有问题。

同样不一定有比较价值。

### Discriminative item

不同系统 / 版本 /控制策略会表现出稳定差异，且差异能回到明确能力机制。

例如：

```text
正确聚合必须先到订单粒度
错误做法会产生可验证的 join fanout
```

这种 item 比“只是很难”更有诊断价值。

## 5. 错误对照 / Negative Controls

构造 benchmark 时，一个强方法是明确：

```text
correct reference
vs
plausible wrong behavior
```

例如：

- 错误时间字段；
- raw join 后直接 sum；
- customer_id 当用户身份；
- 缺证据却强行回答。

但要注意：

> “错误对照能产生不同结果”只证明题目有区分度，不证明模型实际会犯这种错误。

真实 failure frequency 仍必须从运行结果观察。

## 6. Item-level Contract

每个 item 最少应固定：

```text
item_id
task text / state
target capability
family
expected behavior
reference / oracle
tolerance
eligible outputs
failure conditions
slice metadata
source / provenance
version
```

Agent benchmark 还要固定：

```text
environment snapshot
tool versions
initial state
budget / retry policy
```

否则同名 benchmark 在不同运行中可能不是同一个测量工具。

## 7. Reference 必须独立于被测路径

一个危险做法：

```text
系统用 SQL 算答案
reference 也复用同一段 SQL
```

如果二者共享 bug，benchmark 会把错误当正确。

更好的证据结构：

```text
System path: generated SQL
Reference path: independent SQL / Python / deterministic contract / expert adjudication
```

越关键的 benchmark，越应该减少 evaluator 与 SUT 的 common-mode failure。

## 8. Representative Set vs Diagnostic Set

### Representative Evaluation

目标：估计某个真实任务总体下的表现。

更关心：

```text
natural frequency
sampling frame
population weighting
```

### Diagnostic / Challenge Evaluation

目标：放大关键 failure mode，提高版本间区分度。

更关心：

```text
capability coverage
hard-case density
known weakness
risk-critical cases
```

两者都合理，但结论不同。

```text
80% on challenge set
≠ 80% production success rate
```

## 9. 近重复与模板 Shortcut

表面不同并不代表独立能力覆盖。

例如：

```text
2025-01 的支付题
2025-02 的支付题
2025-03 的支付题
```

如果只是替换月份，它们可能是一个 template family 的近重复。

需要检查：

- semantic duplicate；
- same template / same solution skeleton；
- same source row / entity；
- train/dev/test 跨组近重复；
- metadata shortcut。

## 10. Difficulty 不是固定属性

题目 difficulty 往往相对于：

```text
model family
agent scaffold
tool access
budget
prompt
```

而变化。

因此不要只按“人工觉得难”分难度。可结合：

```text
historical pass rate
repeat stability
failure depth
number of constraints
tool / horizon complexity
```

但 difficulty 本身也不能替代 capability slice。

## 11. Benchmark 最小验收

建集前后至少检查：

```text
1. claim 清楚吗？
2. capability coverage map 有吗？
3. reference 独立且可靠吗？
4. item 能区分正确 / plausible wrong behavior 吗？
5. ceiling / floor 是否失衡？
6. 近重复是否跨 split？
7. slice metadata 是否冻结？
8. benchmark version / hash 是否保存？
9. score 的 interpretation boundary 写了吗？
10. holdout 是否真的未参与开发？
```

## Evaluation design

### Pilot → Audit → Freeze

一个实用流程：

```text
candidate item pool
→ deterministic/reference validation
→ duplicate / leakage audit
→ small pilot on baseline(s)
→ ceiling/floor/discrimination audit
→ rebalance coverage
→ freeze version
→ holdout evaluation
```

Pilot 的目的不是在 test 上调方法，而是验证 benchmark instrument 本身。

如果 item 已经被大量用于针对性调参，它就不再是干净 holdout。

## Common wrong answers

### 错误 1：题越难越有区分度

如果所有系统都失败，它只形成 floor effect。

### 错误 2：题越多越可靠

1000 个同模板近重复题，能力覆盖可能仍然只有一个点。

### 错误 3：challenge set 准确率就是产品准确率

challenge set 的 sampling distribution 本来就可能刻意偏离真实分布。

### 错误 4：reference 跟 system 用同一实现更一致

这会放大 common-mode failure 风险。

### 错误 5：错误对照存在，所以模型一定会犯这种错

错误对照只证明题目可区分该错误，不证明实际错误频率。

## Counterexample / boundary

纯 regression set 可以包含很多简单但关键的已知 bug cases。它的目标是阻止历史故障复发，不需要追求覆盖整个能力空间。因此“区分度”必须相对于 benchmark 的用途定义，而不是所有 set 都追求同一种 item difficulty。

## VeriAgent example

VeriAgent 的 Olist challenge set 是一个典型 diagnostic benchmark：24 题预先分成 dev/test，各覆盖 `payment_grain / customer_identity / join_fanout / time_scope` 四个 family；reference SQL 还会与独立 Python 计算交叉验证，并要求一个预设 plausible-wrong SQL 与正确结果确实不同。

这个设计支持：

- 题目有确定 reference；
- 已知错误机制在数据上可被区分；
- family coverage 可解释；
- dev/test 在模型运行前冻结。

但它仍是同一 Olist 数据库、相似表达模板下的领域内迁移 benchmark，不能据此宣称跨数据库或真实线上总体泛化。

## Follow-up questions

- 如何判断一个 item 是 ceiling / floor / discriminative？
- benchmark 是否应该按真实频率采样？
- hard case 应不应该进入正式总分？
- synthetic item 与 natural item 如何搭配？
- 如何定义 benchmark version？

## Evidence of mastery

达到 S4 时，应能从一个模糊的“做一套 Agent benchmark”需求出发，独立给出：

- target claim；
- capability coverage matrix；
- item contract；
- reference strategy；
- split / duplicate audit；
- pilot / freeze 方案；
- benchmark score interpretation boundary。

## Related knowledge

- [Benchmarks Registry](../BENCHMARKS.md)
- [Q01 Evaluation Contract](../01_LLM_Evaluation/01_Evaluation_Contract.md)
- [Q19 Slice-based Regression Diagnosis](../04_Trajectory_and_Failure_Analysis/03_Slice_Based_Regression_Diagnosis.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
