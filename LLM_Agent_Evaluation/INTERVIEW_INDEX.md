# Interview Index

本文件不是另一套正文，而是把知识映射成面试入口。

## 回答层级

每个高频问题准备四层：

1. **30 秒**：定义 + 核心结论。
2. **90 秒**：方法 + 一个关键 trade-off。
3. **5 分钟**：完整 protocol / metric / failure analysis。
4. **追问层**：反例、统计严谨性、工程实现、真实案例。

## V0 高频入口

| 面试主题 | 首要母题 | 推荐案例 |
|---|---|---|
| 怎么设计一个 LLM Eval | Q01/Q02/Q04 | VeriAgent challenge eval |
| LLM-as-a-Judge 靠谱吗 | Q07–Q11 | deterministic verifier vs judge |
| Agent 怎么评 | Q12–Q16 | ProofWriter / Olist Data Agent |
| 怎么分析 Agent 失败 | Q17–Q20 | trace + first failure |
| Benchmark 怎么做 | Q21–Q24 | challenge set / held-out test |
| 3% 提升可信吗 | Q25–Q30 | paired repeated evaluation |
| Eval 工程怎么落地 | Q31–Q34 | manifest / replay / trace / CI |
| Eval 如何服务数据和训练 | Q35–Q37 | reviewed failure → candidate experience |
| 一个完整真实 Eval 项目怎么讲 | Q01–Q37 | [L08 VeriAgent Frozen Case](labs/L08_veriagent_frozen_case/INTERVIEW_PACK.md) |

## VeriAgent capstone

推荐把 [L08 Interview Pack](labs/L08_veriagent_frozen_case/INTERVIEW_PACK.md) 作为项目主案例。

核心不是：

```text
加了 memory
→ 29/36 变成 30/36
```

而是：

```text
reviewed development failure
→ freeze candidate
→ paired held-out evaluation
→ stage-level treatment exposure audit
→ raw delta exists
→ attribution fails
→ candidate not promoted
→ used test becomes exposed
→ next iteration requires fresh evidence
```

这能同时回答：

- 怎么做 benchmark；
- 怎么处理 repeated / paired eval；
- 怎么从 trace 做 failure attribution；
- 怎么控制 data flywheel；
- 怎么避免 test overfit；
- 怎么做 negative-result decision；
- 为什么 mechanism active 不等于 capability improved。

## 项目表达约束

讲 VeriAgent 时应清楚区分：

```text
实现了某个机制
≠ 机制产生了可测行为
≠ 指标提升
≠ 统计上可归因
≠ 值得线上部署
```

优先保留负结果和边界条件，因为它们能体现真实 Evaluation 能力。
