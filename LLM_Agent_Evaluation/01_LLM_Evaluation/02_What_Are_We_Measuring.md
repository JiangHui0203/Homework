# Q03 最终正确率提高，为什么不一定意味着系统能力真的提高？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 4 / Part 6 / Part 7
- Related Patterns: P04 Slice Before Aggregate, P11 Holdout after Development, P12 Mechanism ≠ Outcome
- Related Cases: VeriAgent candidate memory evaluation

## 30-second answer

因为一个最终分数同时受到**能力、评测协议、数据、随机性、外部机制和 evaluator** 的影响。Accuracy 上升只能说明“在这套条件下观测到更多正确结果”，不能自动推出“目标能力提高”，更不能自动推出“提升由新模块造成”。

要把 claim 升级为“能力提升”，至少要排除 denominator/protocol 漂移、数据泄漏、随机波动、judge 变化、非目标组件变化，并检查提升是否发生在机制能够影响的路径和目标 slice 上。

## 90-second answer

可以用五层 claim ladder 来理解：

```text
L1 Mechanism active
   新机制确实被调用
        ↓
L2 Behavior changed
   它确实改变了相关行为
        ↓
L3 Outcome improved
   目标指标在冻结协议下更好
        ↓
L4 Capability evidence
   在独立任务/重复实验上支持目标能力提高
        ↓
L5 Deployment value
   收益大于成本、风险与复杂度
```

任何一层都不能自动推出下一层。

例如 memory 被检索到了，只能证明 L1；如果失败都发生在 memory 注入之前，就没有证据证明 memory 改变了关键行为。即使最终正确数 +1，也可能只是生成随机性。

## Full reasoning

### 1. Observed score 是多个因素的函数

可以把观测分数粗略写成：

```text
Observed Score = f(
  system capability,
  task sample,
  evaluator,
  protocol,
  randomness,
  environment,
  aggregation
)
```

因此 `score ↑` 只是一个现象，不是原因解释。

### 2. 常见“伪提升”来源

#### A. 数据与划分变化

- test 题被用于调 prompt / memory / rule；
- benchmark contamination；
- 新旧系统评的不是同一批题；
- 删除了 candidate 更容易失败的样本。

#### B. 分母或失败处理变化

例如旧系统 timeout 算错，新系统 timeout 被排除，accuracy 会提高，但并非能力提高。

#### C. evaluator 变化

换了 judge prompt、rubric 或 reference，分数变化可能来自评分标准漂移。

#### D. 随机性

LLM/Agent 是随机系统。同一配置重复运行可能出现不同 SQL、tool call 或最终答案。小样本 + 单次运行尤其容易把随机变化误认成方法收益。

#### E. 非目标组件变化

candidate 同时改了模型版本、prompt、tool schema、retry policy、budget；即使结果提高，也无法归因于你声称的新模块。

#### F. 只看 aggregate

总体 +3%，可能只是一个简单 slice 大幅改善，而真正目标能力 slice 不变甚至退化。

### 3. Outcome improvement 与 capability evidence 的差别

“在这个 frozen test 上提高”是**实验结果**。

“目标能力提高”是更强的**泛化解释**，通常还需要：

- held-out 数据；
- 与 claim 对齐的 slice；
- 足够任务覆盖；
- 重复或不确定性分析；
- protocol/evaluator 不变；
- 机制路径与改进位置一致。

### 4. Causal attribution 再多一步

即使可以相信 candidate 更好，也不代表知道“为什么更好”。

如果要归因给某机制，需要至少检查：

```text
机制有机会被触发吗？
→ 实际触发了吗？
→ 触发后改变了中间行为吗？
→ 改变发生在 outcome 之前吗？
→ win 是否集中在被机制影响的样本？
```

这就是 trajectory / trace 在 Agent Eval 中的重要性。

## Evaluation design

看到“accuracy 提升”时按以下顺序审计：

1. 同一 task set 吗？
2. 同一 evaluator 吗？
3. 同一 denominator / failure handling 吗？
4. 唯一变化变量是什么？
5. 有 paired result 吗？
6. 提升集中在哪些 slices？
7. win/loss 的 trajectory 在机制作用点前后发生了什么？
8. 有独立 held-out 证据吗？
9. 置信区间/随机性有多大？
10. 成本和风险是否恶化？

## Common wrong answers

### 错误 1：只要 test set 是固定的，提升就是真提升

固定 test set 很重要，但如果反复根据 test 结果调方法，它会逐渐变成开发集。

### 错误 2：新模块命中了，所以提升来自新模块

命中只证明机制执行；必须验证 win 是否发生在它能影响的路径上。

### 错误 3：平均分提高就说明所有能力都提高

aggregate 会掩盖 slice-level regression。

## Counterexample / boundary

如果任务、协议、evaluator、配置全部冻结，样本规模充分，paired improvement 稳定且与目标 slice/机制路径一致，那么 final accuracy 的提高可以成为很强的 capability evidence。但措辞仍应与实验覆盖范围一致，不轻易外推到“通用能力”。

## VeriAgent example

VeriAgent challenge candidate memory 在 held-out test 上观测到：无记忆 29/36，候选记忆 30/36；paired 结果为 3 个 wrong→right、2 个 right→wrong，净 +1/36。

但 13 次失败都发生在 SQL 阶段 memory retrieval 之前，而 candidate 只在 SQL 生成阶段生效。因此这次 +1 **不能合理归因于候选经验**。这是非常典型的 `Mechanism ≠ Outcome` 案例：机制存在、部分运行也确实注入了经验，但 observed outcome difference 不能证明该机制带来能力收益。

## Follow-up questions

- 什么证据能把“outcome improved”升级成“capability improved”？
- 如果某机制只覆盖 20% 样本，应看总体指标还是 conditional metric？
- guardrail 提升 final success 属于模型能力提升吗？
- test set 被多轮使用后怎样修复评测可信度？

## Evidence of mastery

达到 S4 时，看到“我们提升了 3 个点”应能立即提出一组验证问题，并区分：**现象、机制、归因、泛化、部署价值**。

## Related knowledge

- [Q01 Evaluation Contract](01_Evaluation_Contract.md)
- [Q02 Estimand & Unit](../06_Statistics_and_Experiment_Design/01_Estimand_and_Unit_of_Analysis.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
