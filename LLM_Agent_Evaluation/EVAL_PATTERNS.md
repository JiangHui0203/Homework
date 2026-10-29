# Evaluation Patterns

> 类似 Hot100 的 Pattern / Template：不是背术语，而是看到某类评测问题时知道应该采用什么设计。

## Pattern Card 统一字段

`Problem shape → Recognition signals → Preconditions → Evaluation recipe → Invariant → Metrics → Required artifacts → Failure modes → Anti-pattern → VeriAgent example → Interview hook`

## V0 Pattern Registry

| ID | Pattern | 识别信号 | 核心原则 |
|---|---|---|---|
| P01 | Eval Contract First | “先跑一版看看”但 success/denominator 未定义 | 先定义对象、协议、判定和失败处理，再运行 |
| P02 | Deterministic First, Judge Last | 存在可程序验证的结构化事实 | 能 deterministic verify 的部分不要交给 LLM judge |
| P03 | Paired Same-Task Comparison | 比较两个 prompt/model/controller | 尽量在同 task / repeat 上配对比较 |
| P04 | Slice Before Aggregate | 总体均值变化但原因不明 | 先看能力/难度/失败族切片，再解释 aggregate |
| P05 | Frozen Core + Rotating Hard Set | 既要回归稳定，又要防止 overfit | 稳定 regression set 与动态 hard set 分工 |
| P06 | Trajectory First-Failure Analysis | Agent 最终失败且链路长 | 找 first meaningful failure，不把末端 symptom 当 root cause |
| P07 | Recovery-aware Evaluation | 系统可能重试、回滚、停止 | success / safe stop / recovered / unrecovered 分开计量 |
| P08 | Judge Calibration Before Scale | 想用 LLM judge 批量替代人工 | 先和人工/可靠 verifier 校准再扩大 |
| P09 | Cost per Valid Success | 失败会消耗 token / latency | 成本分母用有效成功，失败消耗不能消失 |
| P10 | Replayable Evaluation | Agent 含工具/环境/随机性 | 保存 trace、fixture、snapshot、version，使结论可重放 |
| P11 | Holdout after Development | 根据 dev failure 改了方法 | 改动后必须在未参与开发的冻结集合评估 |
| P12 | Mechanism ≠ Outcome | 新模块确实被调用 | “链路生效”与“能力提升”分别验证 |

## 维护规则

- Pattern 必须是可复用设计，不是某个 benchmark 的专用技巧。
- 每个稳定 Pattern 至少关联：1 个 CORE_QUESTION + 1 个 failure mode + 1 个案例或 Lab。
- 某次项目经验只有跨案例成立后才从 case promote 到 Pattern。
- 具体阈值、模型名、临时代码路径不得进入稳定 Pattern 定义。