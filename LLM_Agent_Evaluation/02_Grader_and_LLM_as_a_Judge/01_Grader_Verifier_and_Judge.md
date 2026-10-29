# Q07 Grader、Verifier、LLM-as-a-Judge 到底有什么区别？

- Level: M1
- Mastery: S0
- Related Parts: Part 1 / Part 2 / Part 7
- Related Patterns: P02 Deterministic First, Judge Last, P08 Judge Calibration Before Scale
- Related Cases: VeriAgent deterministic verification

## 30-second answer

可以把 **Grader** 看成上位概念：任何把模型/Agent 输出映射为 score、label 或 preference 的评估器。

**Verifier** 重点是检查可被明确验证的约束或事实，例如 exact answer、schema、SQL 执行结果、proof validity、tool argument contract；能 deterministic verify 的部分优先用 verifier。

**LLM-as-a-Judge** 是用另一个 LLM 根据 rubric 评价正确性、质量或偏好，适合开放式、语义性强、难以程序化验证的任务，但它本身也会有 bias 和 variance，不能天然当 ground truth。

## 90-second answer

三者不是三个完全互斥的盒子，而是不同层级：

```text
Evaluator
└── Grader
    ├── Deterministic / rule-based verifier
    ├── Reference-based grader
    ├── Human grader
    └── LLM-as-a-Judge
```

工程上最重要的原则是：

> **能由更强证据直接验证的部分，不要降级成主观模型判断。**

例如 SQL 是否只读、结果数值是否匹配独立 reference、JSON 是否符合 schema，都应优先 deterministic check。只有“解释是否清晰”“开放回答是否覆盖关键点”这类难以形式化的部分，再考虑 human/LLM judge。

## Full reasoning

### 1. Grader：把输出变成可比较信号

抽象地说：

```text
G(input, output, context) -> score / label / preference
```

Grader 可以是：

- exact match；
- regex / schema checker；
- unit test；
- executable reference；
- deterministic verifier；
- human rubric；
- LLM judge；
- 多阶段组合 grader。

因此“grader”描述的是**功能角色**，不是某一种实现技术。

### 2. Verifier：有可检查 contract 的 evaluator

Verifier 适合存在明确可执行正确性条件的场景：

- 数学最终答案；
- 编译/单元测试；
- SQL 执行结果；
- structured output schema；
- proof checker；
- tool arguments；
- 安全约束与权限边界。

Verifier 的优势：

- 可复现；
- 通常低成本；
- 容易回归测试；
- 不受措辞和风格影响；
- 更适合作为 hard gate。

但 verifier 也不是万能的：**验证 contract 不完整时，程序可以稳定地验证错东西。** 所以 verifier 的可靠性依赖 reference、spec 和 coverage。

### 3. LLM-as-a-Judge：处理难形式化质量

适合：

- 开放式问答；
- 摘要质量；
- 风格/帮助性；
- 多维 rubric；
- pairwise preference；
- 复杂语义一致性。

主要风险：

- position bias；
- verbosity bias；
- self-preference / model-family bias；
- prompt sensitivity；
- stochasticity；
- 对事实错误的漏判；
- rubric 理解漂移。

所以 judge 本身也必须被 evaluation：与人工或更可靠 verifier 对齐、分析 disagreement、做稳定性与 bias 测试。

### 4. 推荐的 evaluator hierarchy

对一个复杂 Agent 输出，可以分层：

```text
Layer 1: deterministic validity
  schema / syntax / permission / tool contract

Layer 2: executable correctness
  unit tests / SQL reference / proof checker

Layer 3: semantic correctness
  reference-aware semantic grader / human / judge

Layer 4: quality / preference
  rubric-based human or LLM judge
```

不是所有任务都需要四层，但原则是**最强可验证证据优先**。

### 5. Judge 不能替代 measurement design

即使 judge 很强，也仍然需要：

- 明确 rubric；
- 明确 unit；
- 盲化 candidate identity；
- position randomization（pairwise 时）；
- human calibration set；
- disagreement review；
- version freeze；
- confidence / uncertainty reporting。

## Evaluation design

选择 evaluator 时依次问：

1. 是否存在 executable ground truth？
2. 是否存在结构化 contract？
3. reference 是否可靠且覆盖目标？
4. 哪些维度只能人工/LLM 判断？
5. judge 错误的业务代价有多大？
6. 是否需要 hybrid evaluator？
7. evaluator 自身如何被校准和版本化？

## Common wrong answers

### 错误 1：LLM judge 更智能，所以比 rule-based grader 更高级

不成立。对于可精确验证的问题，deterministic verifier 通常证据更强。

### 错误 2：deterministic verifier 没有 bias

它没有模型式随机 bias，不代表 spec 没有偏差。错误 reference 或不完整 contract 会产生系统性错误。

### 错误 3：judge 与 human correlation 高，就可以完全替代 human

高相关不代表在关键 slice、极端 case 或 pairwise 顺序变化下足够可靠。

## Counterexample / boundary

开放式创意写作没有唯一 executable ground truth，此时强行设计 deterministic verifier 会丢失目标概念。应把可客观验证的约束与主观质量拆开，后者使用 rubric + human/judge。

## VeriAgent example

VeriAgent 的 Olist challenge 不是让 LLM judge 判断 SQL“看起来对不对”，而是用冻结 reference 与实际执行结果做离线 correctness；建集时 reference SQL 还要与独立 Python 计算一致。SQL 只读性、schema、运行时结果等也由确定性检查处理。

这正是 `Deterministic First, Judge Last`：能直接验证的事实不交给另一个模型猜。

## Follow-up questions

- deterministic verifier 的 reference 自己错了怎么办？
- LLM judge 怎样做 calibration？
- pairwise judge 为什么需要交换左右顺序？
- verifier 与 judge 冲突时谁优先？

## Evidence of mastery

达到 S4 时，应能为一个新任务画出 evaluator stack，并解释哪些层必须 deterministic、哪些层可以 judge、以及 judge 自身如何验证。

## Related knowledge

- [Evaluation Patterns](../EVAL_PATTERNS.md)
- [Q01 Evaluation Contract](../01_LLM_Evaluation/01_Evaluation_Contract.md)
- [LLM_Agent_Data · Grader / Verifier / LLM-as-a-Judge](../../LLM_Agent_Data/15_Grader_Verifier_and_LLM_as_a_Judge.md) — 数据系统视角的 canonical owner；本篇只负责 Evaluation 方法论边界。
