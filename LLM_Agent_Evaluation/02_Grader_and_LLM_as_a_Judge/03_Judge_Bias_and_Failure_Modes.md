# Q09 Position Bias、Verbosity Bias、Self-preference、Style Bias 会怎样污染 Judge？

- Level: M1
- Mastery: S0
- Related Parts: Part 2 / Part 6
- Related Patterns: P08 Judge Calibration Before Scale, P03 Paired Same-Task Comparison
- Related Cases: VeriAgent deterministic verification as a boundary case

## 30-second answer

Judge bias 的本质是：**本来不应该决定质量判断的变量，却系统性改变了 judgment。**

典型包括：

- position bias：偏好 A/B 中某个位置；
- verbosity bias：更长、更详细的回答被高估；
- self-preference：偏好与 Judge 自身模型家族/表达风格更相近的回答；
- style / formatting bias：markdown、语气、结构、断言强度等影响分数。

诊断不能靠“提醒 Judge 不要有偏差”，而要做受控 counterfactual：只改变可疑因素、保持目标内容尽量不变，观察 verdict 是否翻转。

## 90-second answer

Bias 测试可以当成一种 evaluator unit test。

例如 pairwise Judge：

```text
Original:  [A, B] -> A wins
Swap:      [B, A] -> ?
```

如果只交换位置、内容完全不变，但大量 verdict 随槽位翻转，就说明存在 position bias。

verbosity / style 也类似：构造语义尽量等价、只在长度或格式上变化的版本，再看 Judge 是否系统性偏向某种表面属性。

关键点是：

> **先证明 perturbation 与目标质量无关，再把 judgment change 解释为 bias。**

如果用户真实偏好确实包含“清晰结构”或“适当详细”，那么并不是所有 style / length preference 都是偏差。

## Full reasoning

### 1. Bias 必须相对于 evaluation target 定义

不能把所有偏好都叫 bias。

例如目标是“帮助性”，适当解释更详细可能真的更好；如果目标是“事实正确性”，那么单纯因为回答更长就提高正确性分数才是偏差。

因此先问：

```text
Target criterion 是什么？
这个被改变的属性是否属于 criterion？
```

只有无关属性影响判断，才构成 evaluator bias。

### 2. Position bias

#### 症状

在 pairwise protocol 中，Judge 系统性偏向第一位或第二位候选。

#### 最小诊断

对同一 pair 做双顺序：

```text
(A, B)
(B, A)
```

然后统计：

- swap consistency；
- slot-conditioned win rate；
- flip rate；
- close-pair vs large-gap pair 的差异。

#### 不能只看什么？

不能只看“第一位胜率是不是 50%”。如果真实数据里 A 本来就更强，50% 不是正确基准。

更强的设计是**同一内容配对交换位置**。

### 3. Verbosity bias

#### 症状

更长、解释更多、看起来更“努力”的回答，即使没有增加有效信息，也更容易得高分。

#### 诊断

构造内容尽量等价的变体：

```text
concise correct answer
vs
same answer + redundant explanation
```

或者将同一答案压缩/扩写，再保持事实和核心论证不变。

统计：

- preference flip；
- score delta vs length delta；
- 不同长度 slice 的 residual error。

#### 注意

如果 rubric 本身奖励完整解释，就不能简单做 length normalization。应区分：

```text
useful completeness
vs
redundant verbosity
```

### 4. Self-preference / model-family preference

#### 症状

Judge 更偏好来自自己或相近模型家族的回答，或者偏好与自身训练风格相似的表达。

#### 难点

这是最容易误诊的 bias 之一，因为：

```text
same-family output 可能真的更好
style similarity 也可能与质量相关
```

因此不能只比较“Judge 更喜欢自己模型多少次”。

#### 更可靠的诊断思路

- 隐去 candidate identity；
- 使用人工/可验证 anchor 控制真实质量；
- 比较不同 generator family 在同质量 bucket 中的 residual preference；
- 对答案做语义保持的 paraphrase / style normalization；
- 使用跨 Judge family 的对照。

### 5. Style / formatting bias

可能包括：

- markdown heading；
- bullet list；
- 更正式的语气；
- confident wording；
- 引用样式；
- 先结论后解释；
- 表格 vs prose。

诊断方法仍然是 controlled perturbation：

```text
content fixed
style changed
```

如果目标 criterion 不包含 style，但 score 显著改变，就需要警惕。

### 6. Bias test 应该进入 Judge regression suite

Judge bias 不是一次性的论文分析，而应该像软件测试一样长期保留。

建议保存固定 probe set：

```text
position swap probes
verbosity probes
formatting probes
identity-masked probes
close-call probes
known critical errors
```

每次 Judge model / prompt / rubric 更新，都重新跑。

### 7. Mitigation 不等于“把 bias 提示写进 prompt”

常见 mitigation：

#### Position

- randomize order；
- 双顺序评分；
- 双顺序不一致时 abstain / escalate；
- ranking 聚合时保留 order metadata。

#### Verbosity / style

- rubric 明确只奖励 relevant evidence；
- criterion decomposition；
- normalize presentation；
- 使用 deterministic checks 分离 factual correctness；
- 对已知 style probe 做回归。

#### Self-preference

- blind model identity；
- multi-family calibration；
- human anchor；
- 不把单一 Judge family 当唯一真值源。

### 8. Judge ensemble 也会共享 bias

多个 Judge 同意不代表 unbiased。

如果它们：

- 使用相似训练数据；
- 共享 rubric；
- 共享 prompt pattern；
- 都依赖相同表面 heuristic；

就可能形成“稳定但共同偏”的 consensus。

## Evaluation design

一个最小 bias audit：

```text
1. Freeze judge contract
2. Sample representative pairs / outputs
3. Build controlled perturbations
4. Run original + counterfactual
5. Measure flip / score delta
6. Slice by quality gap / task / length
7. Apply mitigation
8. Re-run same probes
9. Confirm on held-out probes
```

不要在看到某个 probe 后无限调 prompt，再用同一组 probe 宣布问题解决。

## Common wrong answers

### 错误 1：A/B 位置随机化后就没有 position bias 了

随机化主要减少系统级平均偏差，不代表单个 judgment 可靠，也不告诉你 flip rate 多高。

### 错误 2：回答更长被喜欢就是 verbosity bias

只有长度不是目标质量的一部分、且内容控制后仍影响判断时，才更有资格叫 bias。

### 错误 3：Judge 偏好同家族模型，所以一定是 self-preference

生成模型质量、风格和任务适配都可能混杂，需要 matched-quality 或 controlled transformation。

### 错误 4：加一句“忽略回答长度”就算 debias 完成

Mitigation 需要通过同一套 probe 和独立 holdout 验证。

## Counterexample / boundary

如果 rubric 明确要求“解释充分、结构清晰”，那么结构和长度并非完全无关属性。此时要拆成：

```text
criterion-relevant completeness
criterion-irrelevant verbosity
```

否则容易把真正的质量差异误判成 bias。

## VeriAgent example

VeriAgent 的 SQL correctness 依赖执行结果和冻结 reference，因此不会因为 SQL 写得更漂亮、解释更长或排版更好就改变 correctness label。

这提供了一个重要边界：

> 能用 deterministic evidence 锚定的 criterion，可以天然减少 style / verbosity 这类 Judge bias 的攻击面。

如果未来增加解释质量 Judge，则应把正确性与表达质量拆成两个 evaluator，而不是一个 Judge 总分。

## Follow-up questions

- 如何定义 swap consistency？
- 为什么 close-call pair 更容易出现不一致？
- randomization 和 dual-order evaluation 有什么区别？
- self-preference 如何与真实质量差异区分？
- 多 Judge ensemble 如何检测 shared bias？

## Evidence of mastery

达到 S4 时，应能为一个 Judge 设计至少四类 controlled bias probes，并说明每类 probe 的 confounder、metric、mitigation 和 holdout 验证方式。

## References

- Zheng et al., 2023, *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*: https://arxiv.org/abs/2306.05685
- Shi et al., 2024, *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge*: https://arxiv.org/abs/2406.07791
- Yin et al., 2026, *The Judge Can Debias Itself*: https://arxiv.org/abs/2610.24320
- Yagubyan, 2026, *The Coin Flip Judge? Reliability and Bias in LLM-as-a-Judge Evaluation*: https://aclanthology.org/2026.groundlm-1.64/

## Related knowledge

- [Q08 Judge Reliability](02_Judge_Reliability_and_Calibration.md)
- [Q10 Rubric / Protocol](04_Rubric_and_Scoring_Protocol.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
