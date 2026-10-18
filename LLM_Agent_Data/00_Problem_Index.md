# LLM / Agent Data Knowledge System：Problem Index

> 角色：按真实问题 / 症状检索。回答“我现在遇到这个现象，先查什么、再读哪章、最后可能落到哪类 intervention？”
>
> 原则：**Symptom ≠ Root Cause。Problem Index 给的是排查路径，不是直接结论。**
>
> 路由边界：本 Index 是 **symptom-first retrieval**，因此天然更常服务于 `Failure-led / Monitoring-led`。如果项目起点本来就是 research hypothesis、evaluator / protocol 问题或 existing data asset，不要为了套 Problem Index 人造 symptom；直接进入 [`Project Starter Pack`](./00_Project_Starter_Pack.md) 的 `Hypothesis-led / Evaluation-led / Asset-led / Curation-led` Entry。

---

# 1. “Agent 说完成了，但其实没完成”

## 先查

```text
Final Response
vs
Tool Result
vs
Final World State
```

## 重点章节

```text
Ch11 Environment
Ch12 Trajectory
Ch14 Failure
Ch15 Verifier
```

## 典型原因

```text
Tool 没执行
Tool 执行失败
Harness 注入错误 observation
Agent 没有 read-back
Agent unsupported success claim
```

## Case / Figure

- C2-F4 / C3-F5
- F4 / F5 / F6 / F7

## 可能动作

```text
Tool / Harness fix
Verification data
Final-state verifier
Unsupported-success regression
```

---

# 2. “模型明明看到 Observation 了，还是做了错误动作”

## 先查

```text
Observation 是否真实进入 context？
Agent-visible State 是否正确？
Decision Intent 是什么？
Executed Action 是否和 intent 一致？
```

## 重点章节

Ch11 → Ch12 → Ch13 → Ch14

## Case

C1-F1 / C3-F5

## 典型分流

```text
Observation 根本没进入模型
→ Harness

进入了但被错误理解
→ Observation Grounding / Model

理解正确但执行错 tool
→ Action / Tool Selection
```

---

# 3. “低置信状态是不是应该重点修？”

## 不能直接回答 Yes

需要拆：

```text
Correctness
Risk
Recoverability
Repairability
Selectability
```

## 重点章节

Ch4 → Ch8 → Ch9 → Ch16 → Ch21

## Case / Figure

C4-SC / F3

## 关键提醒

```text
Low confidence
≠ Wrong
≠ Worth repairing
≠ Training value high
```

---

# 4. “有更好的 candidate，为什么系统还是没提升？”

## 排查链

```text
Generator 能不能产生好 candidate？
↓
Oracle gap 多大？
↓
Selector 能不能识别？
↓
Trigger 有没有覆盖正确 state？
↓
Harmful replacement 是否抵消 rescue？
↓
Cost 是否可接受？
```

## 重点章节

Ch4 / Ch8 / Ch16

## 关键区别

```text
Candidate existence
≠ Selectability
≠ End-to-end improvement
```

---

# 5. “Judge 分数涨了，但真实成功率没涨”

## 先查

```text
Judge 是否 drift？
Judge 是否只偏好 style / verbosity？
Evaluator evidence 是否不足？
Proxy 与 downstream 是否仍相关？
```

## 重点章节

Ch15 → Ch21 → Ch23

## Figure

F7 / F13

## Practical Route

```text
Evaluation-led
→ A5 Evaluator Contract
→ 如 evaluator / rubric / guideline 换版，按需加载 A5-M Measurement Bridge
→ same anchor set 做 old↔new paired bridge
```

## 可能原因

```text
Judge overfit
Proxy mismatch
Reward hacking
Evaluator calibration drift
Task success 没被纳入证据
```

---

# 6. “训练数据人工通过率很高，但训练没效果”

## 关键区别

```text
Intrinsic Data Quality
≠ Downstream Learning Value
```

## 重点章节

Ch20 → Ch21

## 排查

```text
Capability 是否对齐？
Exposure 是否足够？
监督形式是否合适？
数据是否太重复？
模型是否已饱和？
Evaluation 是否能感知目标变化？
```

---

# 7. “我们有 100 万条数据，为什么模型还是没提升？”

## 先问

```text
Unique information 有多少？
有效 token exposure 有多少？
Capability coverage 是什么？
Quality / difficulty / source distribution 怎样？
是否存在 massive duplication？
```

## 重点章节

Ch18 / Ch20 / Ch21

## Figure

F10

## 关键提醒

```text
Raw Sample Count
≠ Effective Information
≠ Training Exposure
≠ Learning Value
```

---

# 8. “Hard case 越难越值得做吗？”

## 答案

不一定。

## 重点章节

Ch9 → Ch18 → Ch21

## 判断维度

```text
Gap
Importance
Learnability
Verifiability
Novelty
Cost
```

## 关键提醒

```text
Hard ≠ Valuable
Extreme Hard 可能只是噪声或不可学
```

---

# 9. “Synthetic Data 很便宜，可以全用模型生成吗？”

## 重点章节

Ch7 → Ch20 → Ch21

## 主要风险

```text
Teacher Bias
Mode Collapse
Model Monoculture
Surface Diversity only
Contamination
Weak Verifier
Synthetic-to-real Gap
```

## 正确问题

> 对这个 capability，在当前阶段，synthetic 的 marginal ROI 是否优于 human / production-mined？

---

# 10. “Preference pair 越 hard 越好吗？”

## 不一定

过易：信息量低。

过难：标签噪声高。

## 重点章节

Ch3 / Ch6 / Ch8 / Ch21

## 应看

```text
Pair informativeness
Agreement
Tie / Both Bad
Downstream utility
```

---

# 11. “两个 annotator 老是意见不一致，是标注质量差吗？”

## 不一定

先区分：

```text
Guideline ambiguity
Task ambiguity
Expertise gap
Boundary case
True subjectivity
```

## 重点章节

Ch6

## 处理

```text
Gold
Calibration
Adjudication
Abstention
Boundary-case guideline
```

---

# 12. “LLM Judge 和人工一致率很高，能直接替代人工吗？”

## 不能直接推断

```text
Agreement ≠ Validity
```

## 重点章节

Ch15

## 还要看

```text
Gold accuracy
False Positive / Negative
Position Bias
Verbosity Bias
High-severity slices
Abstention
Swap consistency
```

---

# 13. “模型整体分数涨了，但某些用户感觉更差”

## 重点排查

```text
Task Mix
Slice Regression
Coverage
High-severity Failure
Failure Composition
```

## 重点章节

Ch16 → Ch23

## Figure

F8 / F13

## 关键提醒

```text
Overall Average
可能掩盖局部严重 regression
```

---

# 14. “线上 success rate 下降，是模型退化了吗？”

## 先按 F13 排查

```text
Metric Definition
Judge / Verifier
Tool / Harness / Environment
Traffic Mix
Business Rule
Frozen Benchmark
Failure Mix
```

## 重点章节

Ch23

## Figure

F13

## Practical Route

```text
Monitoring-led Incident
→ A10 Monitoring Incident / Drift Record
→ Last-known-good + Change Ledger + containment
→ 需要更完整 incident contract 时按需加载 A10-I
→ attribution 之后再决定是否进入 A1 / A3 / A4 / A5
```

固定边界：

```text
Monitoring Alert
≠ Model Regression
```

---

# 15. “固定 threshold 以前好用，现在 trigger 爆炸了”

## 可能是

```text
Score Distribution Drift
Calibration Drift
Model Version Shift
Task Mix Shift
```

## 重点章节

Ch4 / Ch16 / Ch23

## 关键区别

```text
Frozen Threshold
回答迁移性

Recalibrated Threshold
回答每个模型各自最优 operating point
```

---

# 16. “系统成功率很高，但只处理了很少任务”

## 必须看

```text
Coverage
Success@Coverage
Risk@Coverage
Escalation Rate
```

## 重点章节

Ch16 / Ch23

## 关键提醒

```text
95% success @ 20% coverage
不能直接胜过
90% success @ 90% coverage
```

---

# 17. “Tool API 挂了，为什么 benchmark 把它算模型错？”

## 这是 attribution 问题

## 重点章节

Ch11 → Ch14 → Ch16 → Ch22

## 关键区别

```text
Infrastructure Outcome
≠ Model Outcome
≠ Evaluation Outcome
```

---

# 18. “模型失败后系统自动 retry，最后成功，这算模型会 recovery 吗？”

## 不算

## 重点章节

Ch22

## 关键边界

```text
Infrastructure Retry
≠ Agent Policy Recovery
```

## Case

C3-F4

---

# 19. “Judge 更新后历史分数变了，要重新跑模型吗？”

## 通常先 Re-score

如果 raw output / trajectory 没变：

```text
reuse raw artifact
→ re-score
```

## 重点章节

Ch15 / Ch19 / Ch22 / Ch23

## Practical Route

```text
Evaluation-led
→ A5-M Measurement Bridge
→ same anchor set 比较 old↔new evaluator
→ 确认 measurement change 后再决定历史结果如何 re-score / bridge
```

## 关键区别

```text
Re-score ≠ Re-run ≠ Replay
Evaluator Upgrade ≠ Capability Improvement
```

---

# 20. “标签修正了，历史 selector 结果要重新决策吗？”

## 先区分

```text
Historical Decision
Corrected Label
Fresh Re-execution
```

如果研究问题是“旧决策按新标签重新计分”，应：

```text
freeze old decision
→ re-score
```

而不是重新决策。

## 重点章节

Ch16 / Ch19

---

# 21. “训练集和测试集没有 exact duplicate，就没有 contamination 吗？”

## 不是

还要看：

```text
Near Duplicate
Synthetic Derivative
Same Seed Family
Same Workflow
Solution Leakage
Teacher Leakage
```

## 重点章节

Ch16 / Ch19 / Ch20

---

# 22. “同一个 synthetic seed 的衍生样本可以随机拆 train/test 吗？”

## 不建议

应按：

```text
family_id / seed_id / workflow_id
```

group split。

## 重点章节

Ch19 / Ch22

---

# 23. “目标能力提升了，但普通任务变得过度 retry / 过度拒绝”

## 这是 regression / overbehavior

## 重点章节

Ch21 / Ch23

## 实验应同时看

```text
Target Gain
General Regression
Over-retry
Over-abstention
Cost
```

---

# 24. “某批数据 +1.2pt，值不值得继续做？”

## 不能只看 +1.2

还要看：

```text
Variance
Matched Budget
Transfer
Regression
Marginal Gain
Production Cost
Opportunity Cost
```

## 重点章节

Ch18 → Ch21

## Figure

F10

---

# 25. “做了很多配置，挑最好的那个，能算稳定结论吗？”

## 风险

```text
Multiple Comparisons
Winner's Curse
Dev-set Overfitting
```

## 重点章节

Ch16 / Ch21

## 应做

```text
Exploratory
→ select hypothesis

Confirmatory
→ frozen holdout / predefined metrics
```

---

# 26. “我们到底该修 Data、Model、Tool 还是 Harness？”

## 推荐顺序

```text
Requirement / Task
↓
Tool / API
↓
Harness
↓
Environment / Permission
↓
Verifier / Judge
↓
Model / Policy
↓
Data Gap
```

## 重点章节

Ch14 → Ch24 → Ch25

## Figure

F14

---

# 27. “一个 failure 怎么变成训练数据？”

## 不要直接转换

```text
Failure
↓
Verify
↓
Attribution
↓
Root Cause
↓
Capability Gap
↓
Choose Supervision
↓
Construct Data
↓
Controlled Experiment
```

## 重点章节

Ch13 → Ch14 → Ch17 → Ch21

## Figure

F6 / F9

---

# 28. “如何知道应该停止继续生产某类数据？”

## 看

```text
Scaling Curve
Marginal Utility
Regression
Cost
Capability Saturation
Fresh Failure Distribution
```

## 重点章节

Ch18 / Ch21 / Ch23

## 动作

```text
SCALE / MAINTAIN / REBALANCE / STOP / RETIRE
```

---

# 29. “生产 pipeline 每天产很多，但真正能用的数据很少”

## 重点看

```text
Raw Throughput
vs
High-value Yield
```

## 重点章节

Ch19 / Ch20 / Ch22

## Figure

F11 / F12

## Practical Route

如果输入本质上是“已有 source assets / trajectories 如何变成可用数据资产”，优先按：

```text
Asset-led / Curation-led
→ A11 source lineage
→ A6-C Curation Contract
→ Rebuildable Dataset View / Yield Funnel / Exposure
→ A7 downstream validation
```

不要把：

```text
Source Asset
```

直接当成：

```text
Dataset View / Training Data
```

## 分解 funnel

```text
Requested
→ Generated
→ Valid
→ Verified
→ Unique
→ Accepted
→ Dataset-ready
```

---

# 30. “人工审核队列堵爆了怎么办？”

## 不是先招更多人

先做：

```text
Risk / disagreement routing
Cheap rule / verifier first
Judge next
Human only for high-value unresolved
Backpressure
```

## 重点章节

Ch6 / Ch15 / Ch22

---

# 最短诊断原则

遇到陌生问题时优先问：

```text
1. 真实 Outcome 是什么？
2. Evidence 是什么？
3. Symptom 在哪一层？
4. Root Cause / Owner 是谁？
5. 这是 Data Problem 吗？
6. 什么最小 intervention 能验证假设？
7. 什么结果足以 Scale / Stop？
```

如果这 7 问能回答清楚，通常就已经从“看到 bad case”进入了真正的问题解决阶段。
