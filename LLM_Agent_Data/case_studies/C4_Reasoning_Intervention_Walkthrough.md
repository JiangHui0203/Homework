# C4 Practical Walkthrough：从可疑 Reasoning State 到 Trigger / Oracle / Selector / Cost

> 状态：`Practical Case Study / Stable Mother Edition V3.x`
>
> Canonical Case：[`C4 — Reasoning Continue / Repair`](../cases/C4_Reasoning_Continue_Repair.md)
>
> 主要 Variant：`C4-SC + C4-CS + C4-BR + C4-P1...P4`
>
> 目的：把一个局部 reasoning-state intervention 从 `Risk Detection → Same-prefix Candidate Generation → Oracle Headroom → Selector → End-to-end Evaluation → Cost / Coverage` 完整跑一遍。
>
> 注意：**本文讨论的是显式、可观察的 reasoning prefix / structured state，不依赖不可访问的隐藏 chain-of-thought。canonical definition 仍以 `cases/C4_Reasoning_Continue_Repair.md`、Glossary 与对应章节为准。**

---

# 0. 先看完整链

给定：

```text
Problem x
Authoritative Prefix P
Provisional Continuation u0
```

一个在线 reasoning intervention system 不能只问：

```text
u0 看起来可疑吗？
```

而要继续拆成：

```text
Risk
↓
Recoverability
↓
Repairability
↓
Selectability
↓
Net End-to-end Value
```

完整工作流：

```text
Current Reasoning State P
↓
Generate provisional u0
↓
Compute online risk signal
↓
Trigger?
├── No  → keep baseline path
└── Yes → generate same-prefix siblings
          ↓
          Candidate Pool
          ↓
          Online Selector / Abstention
          ↓
          Chosen Continuation
          ↓
          Final Outcome
          ↓
          Rescue / Harmful / Neutral
          ↓
          Cost / Coverage / Net Gain
```

这里任何一层都可能成为瓶颈。

---

# 1. Stable State Contract

固定：

```text
Problem x
Authoritative Prefix P
Model checkpoint
Tokenizer / decoding semantics
Candidate-generation contract
Downstream evaluator
Budget definition
```

`P` 必须是真正的当前 authoritative state，而不是：

```text
已经看到未来答案后的 reconstructed prefix
```

也不能在 sibling 间改变：

```text
system prompt
tool availability
evaluator
model version
```

否则比较不再是 clean same-prefix counterfactual。

---

# 2. Baseline Unit：`u0`

从 `P` 生成 provisional continuation：

```text
P
→ u0
```

然后计算只依赖在线可用信息的信号，例如：

```text
min token logprob
mean logprob
entropy
top1-top2 margin
local likelihood drop
structured audit state
```

这些都只是：

```text
Risk Features
```

而不是：

```text
Error Labels
```

固定原则：

```text
Low Confidence
≠ Wrong
≠ Recoverable
≠ Repairable
≠ Selectable
```

---

# 3. Trigger：只回答“要不要花额外计算”

Trigger 的职责不是选 candidate。

它只回答：

```text
当前 state 是否值得进入更昂贵的 exploration path？
```

输入必须 online-available：

```text
P
u0
local token / state signals
historical calibration parameters
```

不能使用：

```text
future rollout outcome
reference answer
candidate future success
```

否则产生 future-info leakage。

---

# 4. Same-prefix Candidate Generation — `C4-SC`

触发后，从完全相同的 `P` 生成 sibling candidates：

```text
P + u0
P + c1
P + c2
...
```

这里必须记录：

```text
candidate_id
parent_prefix_id
generation config
sampling seed / policy
candidate token count
candidate generation cost
```

并保持：

```text
same authoritative prefix
```

因为真正想测的是：

> **当前局部 continuation 如果换一条，未来 outcome 会不会改变？**

---

# 5. Offline Outcome Evidence

研究阶段可以让每个 sibling 继续 rollout 到 final outcome：

```text
P + u0 → O0
P + c1 → O1
P + c2 → O2
```

然后由 objective verifier / benchmark evaluator 判断 final correctness。

这一步定义离线标签：

```text
Rescue
Harmful
Neutral-positive
Neutral-negative
```

但注意：

> **这些 Future Outcomes 是监督证据，不是 online selector feature。**

---

# 6. Oracle Headroom：先问“好候选存在吗？”

对 triggered pool：

```text
Oracle Rescue Opportunity
= baseline u0 wrong
  AND 至少一个 sibling candidate right
```

它回答的是：

```text
Recoverability / Generator Headroom
```

而不是实际系统收益。

如果：

```text
Oracle headroom ≈ 0
```

那么无论 selector 多聪明，E2E 都很难提升。

可能原因：

```text
trigger 锁错 state
generation diversity 不够
candidate budget 太小
state 本身不可修
```

---

# 7. Selector：再问“在线认得出来吗？”

Selector 输入只能来自当前可用信息，例如：

```text
candidate mean log-likelihood
candidate length-normalized score
self-consistency feature
structured verifier-like local signal
candidate disagreement
```

输出：

```text
keep u0
choose c1
choose c2
abstain
```

Selector 的核心问题：

```text
Candidate Exists
≠ Candidate Selectable
```

这对应 `C4-P2`：

```text
pool 里有 rescue
selector 却选不到
```

---

# 8. Four Canonical Failure Patterns

## `C4-P1` — High Risk, Not Recoverable

```text
u0 likely wrong
siblings all wrong
```

解释：

```text
Risk high
Recoverability low
```

这类 state 适合：

```text
abstain / escalate / change action space
```

而不是盲目生成更多类似 candidate。

---

## `C4-P2` — Recoverable, Not Selectable

```text
pool contains rescue
selector picks wrong candidate
```

瓶颈：

```text
Selector
```

数据方向可以考虑：

```text
same-prefix preference
selector calibration
pairwise candidate ranking
```

---

## `C4-P3` — Low Confidence, Baseline Correct

```text
risk signal high
u0 final outcome correct
siblings no better
```

说明：

```text
Risk Proxy False Positive
```

如果 trigger 太激进，会产生：

```text
extra cost
+
potential harmful replacement
```

---

## `C4-P4` — Harmful Repair

```text
u0 would succeed
intervention replaces it with failing candidate
```

这是最重要的反例之一：

```text
“系统会修错题”
```

不等于：

```text
“系统端到端更好”
```

因为必须同时统计：

```text
Rescue
and
Harmful
```

---

# 9. Population Accounting

一个 routing / selective system 至少区分：

```text
Full Screened Population
↓
Eligible
↓
Triggered
↓
Candidate-generated
↓
Intervened
↓
Observed Final Outcome
```

任何 metric 必须写 denominator。

尤其不能把：

```text
Triggered subset accuracy
```

冒充：

```text
End-to-end system accuracy
```

Non-triggered case 仍属于 full population；它们只是走 baseline path。

---

# 10. Bottleneck Decomposition

建议把系统拆成五层分别测：

```text
A. Trigger Quality
B. Generator / Candidate Quality
C. Oracle Headroom
D. Selector Quality
E. End-to-end Gain / Cost
```

## A. Trigger

```text
Coverage
Risk enrichment
False-positive trigger rate
```

## B. Generator

```text
candidate diversity
generation cost
valid candidate rate
```

## C. Oracle

```text
oracle rescue opportunity
best-of-pool upper bound
```

## D. Selector

```text
rescue captured
harmful replacement
abstention
ranking calibration
```

## E. End-to-end

```text
final accuracy / success
Net = Rescue - Harmful
coverage
latency
tokens
candidate count
Success@Budget
```

这样才能知道：

```text
“不涨”到底卡在哪一层？
```

---

# 11. 一个纯教学的 Population Example

下面数字只用于说明 denominator，不代表任何真实实验结果。

```text
200 screened states
↓
50 triggered
↓
50 candidate pools generated
↓
20 pools have oracle rescue opportunity
↓
selector captures 11 rescue
↓
selector causes 6 harmful replacements
```

那么：

```text
Oracle Headroom
= 20 rescue opportunities among 50 triggered

Selector Capture
= 11 / 20 oracle opportunities

Net Transition
= +11 - 6 = +5
```

但最终 E2E 必须回到：

```text
200 full screened states
```

计算，而不是只报告：

```text
11 rescues in triggered subset
```

这也是 denominator discipline 的核心。

---

# 12. Cost Accounting

Reasoning intervention 的收益必须和 cost 一起看。

至少记录：

```text
baseline generation tokens
trigger computation
extra candidate tokens
selector computation
additional latency
number of candidate rollouts
```

如果：

```text
+0.5pt accuracy
```

来自：

```text
5× generation cost
```

它和：

```text
+0.4pt at 1.2× cost
```

不是同一个 operating point。

所以更合理的比较包括：

```text
Success@Budget
Accuracy–Cost Pareto
Net Gain per Extra Token
Coverage–Quality Curve
```

---

# 13. Continue / Stop 与 Branch / Repair 必须分开

## Continue / Stop — `C4-CS`

问：

```text
当前路径还值得继续计算吗？
```

典型 intervention：

```text
stop early
continue
allocate more tokens
```

## Branch / Repair — `C4-BR`

问：

```text
当前局部 continuation 应不应该被替换？
```

典型 intervention：

```text
keep u0
sample siblings
replace
repair
abstain
```

二者都属于 test-time control，但 action space 不同。

不要用一个模糊的：

```text
“more thinking”
```

把它们混成一件事。

---

# 14. Derived Data Assets

同一批 C4 state 可以派生：

```text
Risk Detector Data
Correctness Labels
Recoverability Labels
Repairability Labels
Same-prefix Preference
Selector Pairwise Data
Harmful-repair Negative Data
Continue / Stop Data
Branch / Repair Data
Trigger Calibration Set
Regression States
```

但要保持：

```text
source_state_id
prefix_id
candidate_id
future_outcome_id
label_version
```

否则不同 derived views 会失去 counterfactual lineage。

---

# 15. Controlled Experiment

假设我们想验证：

> same-prefix selector data 是否真的改善 branch / repair decision？

可以设计：

```text
Baseline
= current trigger + current selector

Treatment
= same trigger
+ selector trained / calibrated on C4 same-prefix preference data
```

严格保持：

```text
trigger frozen
candidate generator frozen
candidate count frozen
generation budget frozen
evaluator frozen
```

这样才更接近回答：

```text
selector data 本身是否有效？
```

主要指标：

```text
Rescue
Harmful
Net
Selector Capture of Oracle
E2E Accuracy
Extra Tokens
Latency
```

---

# 16. Trigger Experiment 和 Selector Experiment 不要混

如果同时改：

```text
trigger threshold
candidate count
selector score
```

最后涨了，很难知道为什么。

更稳的是：

```text
Experiment 1
freeze generator + selector
→ only test trigger

Experiment 2
freeze trigger + selector
→ only test generator / N

Experiment 3
freeze trigger + generator
→ only test selector
```

最后再做：

```text
E2E combined system
```

这就是 Ch16 / Ch21 的 controlled comparison 在 reasoning intervention 上的具体应用。

---

# 17. Monitoring / Drift

上线后要监控的不只是 final accuracy。

还包括：

```text
Risk Score Distribution
Trigger Rate
Candidate Count
Oracle-like offline audit sample
Selector Score Distribution
Abstention Rate
Rescue / Harmful sample estimate
Extra Token Cost
Latency
```

特别是：

```text
threshold frozen
```

不代表：

```text
operating point frozen
```

因为模型、任务分布或 score calibration 变化后：

```text
Trigger Rate
20% → 70%
```

也可能发生。

因此：

```text
Ranking quality
≠ Threshold calibration
```

---

# 18. 最小 Decision Memo

```yaml
problem:
  suspicious reasoning states sometimes admit better same-prefix continuations

baseline:
  greedy / current local path

trigger:
  online risk signal only

candidate_contract:
  same authoritative prefix
  fixed candidate budget

oracle_question:
  does a better continuation exist?

selector_question:
  can online features identify it?

primary_metrics:
  - end_to_end_success
  - rescue
  - harmful
  - net

cost_metrics:
  - extra_tokens
  - candidate_count
  - latency

claim_scope:
  fixed model / benchmark / protocol

scale_rule:
  positive net gain under acceptable cost

stop_rule:
  oracle headroom too low
  OR harmful offsets rescue
  OR cost dominates utility
```

---

# 19. C4 最终要建立的 mental model

```text
Risk Detector
只能回答“哪里值得看”

Generator
回答“能不能造出 alternative”

Oracle
回答“alternative 里有没有更好的”

Selector
回答“在线认不认得出来”

E2E Evaluation
回答“修的比伤的多不多”

Cost Accounting
回答“值不值得这么做”
```

因此：

```text
Risk Signal
≠ Error Detector

Oracle Gap
≠ Selector Gain

Selector Gain
≠ E2E Gain

E2E Gain
≠ Cost-effective Gain
```

---

# Cross-links

- [`C4 — Canonical Case`](../cases/C4_Reasoning_Continue_Repair.md)
- [`Ch4 — Reasoning Data / Process Supervision`](../04_Reasoning_Data_and_Process_Supervision.md)
- [`Ch8 — Candidate Selection`](../08_Rollout_Rejection_Sampling_and_Candidate_Selection.md)
- [`Ch16 — Evaluation Protocol`](../16_Benchmark_Design_and_Evaluation_Protocol.md)
- [`Ch21 — Data Experiments`](../21_Data_Experiments_and_Causal_Validation.md)
- [`Ch23 — Monitoring / Drift`](../23_Data_Monitoring_Online_Feedback_and_Drift_Detection.md)
- [`F3 — Reasoning State Decision Stack`](../figures/F3_Reasoning_State_Decision_Stack.md)
- [`F8 — Benchmark / Evaluation Protocol`](../figures/F8_Benchmark_Evaluation_Protocol.md)
- [`F13 — Monitoring / Drift`](../figures/F13_Monitoring_Drift_Diagnostic_Tree.md)

---

# 一句话收束

> **C4 的价值，是把“这个 reasoning state 看起来可疑”拆成一个真正可审计的在线决策系统：先判断值不值得触发，再判断有没有可救空间、能不能生成 alternative、在线能不能选出来，最后把 Rescue、Harmful、Coverage 与 Cost 一起还原成真实 E2E 价值。**
