# Q23 为什么 Frozen Core、Regression Set、Hard Set / Rotating Set 应该分工不同？

- Level: M1
- Mastery: S0
- Related Parts: Part 4 / Part 5 / Part 7
- Related Patterns: P04 Slice Before Aggregate; P05 Frozen Core + Rotating Hard Set; P11 Holdout after Development
- Related Registry: `BENCHMARKS.md`

## 30-second answer

因为它们回答的是不同问题：

```text
Frozen Core      长期主指标是否可比？
Regression Set   已知关键 bug 是否复发？
Hard / Challenge 哪些脆弱能力仍能区分版本？
Rotating / Fresh 长期开发后，改进能否在新数据上继续成立？
```

把它们混成一个总分，会同时破坏纵向可比、诊断能力和独立泛化证据。最稳健的方案是分层报告，而不是追求“一个 benchmark 包办所有用途”。

## 90-second answer

我会把 benchmark portfolio 分成四种资产。

**Frozen Core** 很稳定，item 与 protocol 尽量不变，用来画长期趋势和做关键 release gate；代价是长期会有 exposure 风险。

**Regression Set** 收录历史真实 failure / critical bug，开发者可以反复看，目标是“别再犯”；它不是未见泛化集。

**Hard / Challenge Set** 提高关键脆弱能力密度，适合区分候选、做 failure analysis；但它常常不代表自然任务频率。

**Rotating / Fresh Set** 周期性更新，提供较干净的新鲜 evidence，用来对抗长期 test overfit；但因为内容会变化，不适合直接做长期绝对分数时间序列。

所以应该把“稳定性”和“新鲜度”拆成不同 set，而不是强迫一个 set 同时做到两者。

## 1. 四种 Set 的职责

### Frozen Core

目标：

```text
stable longitudinal comparison
release regression signal
shared baseline
```

特点：

- task/version 稳定；
- metric/protocol 稳定；
- 适合 paired / historical comparison；
- exposure 随时间增加。

### Regression Set

来源：

```text
historical incident
reviewed failure
critical edge case
fixed bug
```

目标：

> “这个已经理解并修过的 failure，不能再回来。”

它可以高度人工 curated，甚至刻意过采样罕见严重故障。

### Hard / Challenge Set

目标：

```text
find capability boundary
separate strong vs weak versions
stress critical mechanisms
```

可以：

- 过采样难例；
- 增加组合约束；
- 聚焦 known weak families；
- 做 synthetic perturbation / adversarial construction。

但不能把分数直接解释成线上成功率。

### Rotating / Fresh Set

目标：

```text
fresh confirmation
anti-overfit
drift / new scenario coverage
```

内容周期性变化，开发团队在运行前尽量不可见。

## 2. 为什么一个 Set 很难同时满足所有目标

存在天然冲突：

```text
长期稳定
vs
长期新鲜
```

Frozen set 越稳定，团队越熟悉；Fresh set 越新鲜，时间序列可比性越弱。

还有：

```text
自然分布
vs
高诊断密度
```

线上真实罕见但高风险的 failure，在自然采样 benchmark 中可能长期抽不到；challenge / regression 就需要人为提高它的权重。

因此 benchmark portfolio 比“万能 benchmark”更现实。

## 3. 推荐组合

一个实用 portfolio：

```text
A. Frozen Core
B. Known Regression
C. Hard / Challenge
D. Rotating Fresh
```

报告时分开：

| Set | Primary use | Score interpretation |
|---|---|---|
| Frozen Core | 长期可比 | 同版本 benchmark 下的稳定趋势 |
| Regression | bug recurrence | 已知 failure 是否复发 |
| Hard | capability stress | 脆弱能力区分，不代表自然频率 |
| Fresh | generalization check | 新样本上的当前证据 |

不要强行平均成一个“总 benchmark score”。

## 4. Promotion / Demotion 生命周期

Item 的角色可以变化。

典型流转：

```text
Fresh holdout failure
→ explicit review
→ root cause supported
→ bug fixed
→ promote to Regression Set
```

Hard item 如果已经变成长期稳定基础能力，也可能进入 Frozen Core。

Frozen Core 如果长期被过度针对、已经失去区分度，可以保留做 compatibility，同时补新版本或 fresh set，而不是悄悄替换后还沿用旧分数线。

## 5. Regression Set 不能无限增长

每次失败都塞进去，最终会造成：

- 高度重复；
- 运行成本爆炸；
- 同一 failure family 被重复加权；
- gate 极度保守。

应该做：

```text
deduplicate by mechanism
keep minimal reproducer
severity / criticality tagging
owner tagging
retirement / merge policy
```

一个 regression fixture 的价值是稳定复现一个机制，不是保留所有历史 incident 的完整副本。

## 6. Hard Set 不等于 “Bad Case Cemetery”

Hard set 仍然需要：

- 清楚 task contract；
- 可靠 reference；
- 可解释 family；
- 版本化；
- leakage boundary。

不能把所有难解、歧义、reference 不稳的题统称“hard”。

如果人类都无法确定正确行为，那可能是 benchmark quality 问题，不是模型 hard case。

## 7. Fresh Set 怎么保持可解释

Fresh 不意味着每次随机抓一堆未知分布样本。

应冻结 generation / sampling contract：

```text
source population
sampling frame
capability quotas
risk quotas
difficulty policy
reference validation
```

这样虽然 item 会换，但“它从什么总体、按什么规则来”仍可审计。

## 8. Release Gate 如何组合

示例：

```text
Frozen Core      no material regression
Critical Regression 100% pass
Hard Set         report / investigate, not always hard gate
Fresh Set        no statistically meaningful degradation
```

高风险业务也可能把某些 hard/safety slices 设为 hard gate。

关键是 gate 规则要预注册，不能看到分数后临时决定哪个 set 算数。

## 9. Score Dashboard 应按角色分区

推荐：

```text
Stable Quality
- Frozen Core

Known Risk
- Regression Set

Capability Frontier
- Hard / Challenge

Fresh Evidence
- Rotating Set
```

而不是：

```text
Overall Benchmark = 83.7
```

一个总分往往掩盖每个 set 完全不同的 sampling semantics。

## Evaluation design

### Benchmark Portfolio Contract

每个 set 写清：

```text
purpose
sampling source
exposure policy
update frequency
primary metric
gate role
promotion / retirement policy
interpretation boundary
```

### Periodic Audit

定期检查：

```text
ceiling / floor drift
repeat duplication
exposure level
runtime cost
failure-family coverage
reference validity
production drift
```

## Common wrong answers

### 错误 1：所有数据都混成一个更大的 test set，统计更稳

不同 sampling / exposure 语义混在一起，会让总分失去清晰含义。

### 错误 2：Regression Set 必须保持未见

它的目标恰恰是被反复使用，阻止已知 bug 复发。

### 错误 3：Frozen Core 永远不能变

可以版本升级，但必须显式 version bump 和桥接比较，不能静默换题。

### 错误 4：Hard Set 分数越高，线上表现就越好

只有在额外证明其与目标总体的关系后才能外推。

### 错误 5：Fresh Set 不需要结构，只要新就行

随机新鲜但分布漂移不可控，也难解释。

## Counterexample / boundary

非常小的研究原型可能暂时只需要 dev + frozen test 两层。但只要系统进入持续迭代、CI 或多版本对比，Regression 与 Fresh/Rotating 的职责很快就会出现；此时继续依赖单一 test set 会越来越难解释。

## VeriAgent example

VeriAgent 当前已经有这种分工雏形：challenge dev 用于 failure review 和候选 memory 构造；challenge held-out test 用于修改后的确认；已复核开发 failure 很适合进一步沉淀为 deterministic regression fixtures。

如果后续围绕 held-out test 的分析阶段错误继续开发，那么原 test 也会逐渐变成 known-hard / regression evidence。要继续证明新版本的泛化，就应构造新的 fresh holdout，而不是无限复用同一 12 题。

## Follow-up questions

- 什么时候把 hard case promote 到 regression？
- Frozen Core 多久更新一次？
- Fresh set 如何做统计比较？
- regression set 是否按线上频率加权？
- 哪些 set 应做 release hard gate？

## Evidence of mastery

达到 S4 时，应能给一个持续迭代项目设计完整 benchmark portfolio，并解释：

- 每个 set 的 sampling semantics；
- exposure policy；
- gate role；
- item promotion / retirement；
- score 为什么不能无脑合并。

## Related knowledge

- [Q22 Leakage & Test-set Overfitting](02_Leakage_and_Test_Set_Overfitting.md)
- [Q24 Coverage / Difficulty / Frequency Trade-offs](04_Coverage_Difficulty_and_Distribution_Tradeoffs.md)
- [Benchmarks Registry](../BENCHMARKS.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
