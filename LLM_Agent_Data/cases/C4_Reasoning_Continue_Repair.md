# C4 — Reasoning Continue / Repair

> Case ID: `C4`
>
> 角色：全书 reasoning-state、risk、recoverability、same-prefix counterfactual、continue/stop 与 branch/repair 主案例。
>
> 注册表：[`Canonical Casebook`](../00_Canonical_Casebook.md)

---

# C4.0 Base Structure

给定：

```text
Problem x
Authoritative reasoning prefix P
Current provisional continuation u0
```

系统可能需要决定：

```text
keep
continue
stop
branch
repair
replace
```

C4 的关键不是某一道具体数学题，而是一个稳定的局部决策对象：

```text
same current reasoning state
→ different local decisions
→ different future outcomes
```

---

# C4.1 Canonical State Variables

建议至少区分：

```text
Reasoning State
当前可观察的推理前缀 / structured state

Correctness
当前状态 / continuation 是否已经包含实质错误

Risk
从当前状态继续沿 baseline path，未来失败的风险

Recoverability
是否存在 alternative future 能改善最终 outcome

Repairability
在当前系统可用 action / candidate / budget 下，是否真的能实现修复

Selectability
好 candidate 存在时，在线 scorer / selector 能否识别出来
```

固定原则：

```text
Correctness
≠ Risk
≠ Recoverability
≠ Repairability
≠ Selectability
```

以及：

```text
Low confidence
≠ Wrong
≠ Worth repairing
```

---

# C4.2 Canonical Same-prefix Set — `C4-SC`

固定同一个 authoritative prefix：

```text
P
```

生成：

```text
u0  baseline / provisional continuation
c1  sibling candidate
c2  sibling candidate
```

然后各自 rollout 到最终 outcome：

```text
P + u0 → O0
P + c1 → O1
P + c2 → O2
```

必须保持：

```text
same prefix
same model family / checkpoint
same tool / runtime semantics
same downstream evaluator
```

这样 outcome 差异才更能归因到当前 local decision。

---

# C4.3 Outcome Transition Labels

相对 baseline `u0`：

```text
u0 wrong, candidate right
→ Rescue

u0 right, candidate wrong
→ Harmful

both right
→ Neutral-positive

both wrong
→ Neutral-negative
```

注意：

> Rescue / Harmful 是相对 baseline intervention 的 transition label，不是 candidate 的固有属性。

---

# C4.4 Two Decision Families

## `C4-CS` — Continue / Stop

核心问题：

```text
当前状态还值得继续计算吗？
```

Action space：

```text
continue
stop
allocate more compute
```

它主要涉及：

```text
future gain
cost
stopping policy
compute allocation
```

---

## `C4-BR` — Branch / Repair

核心问题：

```text
是否应该离开当前局部路径，探索 alternative continuation？
```

Action space：

```text
keep u0
sample siblings
replace u0
repair current unit
abstain
```

这主要涉及：

```text
risk trigger
candidate generation
oracle headroom
selector quality
```

Continue/Stop 和 Branch/Repair 不应被压成同一个“多想一点”。

---

# C4.5 Oracle vs Selector

对 `C4-SC`：

## Oracle Question

```text
候选池里是否存在比 u0 更好的 continuation？
```

它定义：

```text
recoverability / headroom
```

## Selector Question

```text
在线可用信息能不能把那个更好的 candidate 选出来？
```

它定义：

```text
selectability
```

因此：

```text
Candidate Exists
≠ Candidate Selectable
```

---

# C4.6 Offline Labels vs Online Features

允许 offline label 使用：

```text
future rollout outcome
final correctness
sibling comparison
human / verifier adjudication
```

但在线 trigger / selector 不能偷看：

```text
future outcome
hidden reference
future sibling success
```

固定原则：

> Future information may supervise a decision without being available to the decision policy itself.

---

# C4.7 Canonical Example Patterns

## `C4-P1` — High Risk but Not Recoverable

```text
baseline continuation likely wrong
all sibling candidates also wrong
```

说明：

```text
Risk high
Recoverability low
```

触发 exploration 也不一定有价值。

---

## `C4-P2` — Recoverable but Not Selectable

```text
candidate pool contains rescue
selector picks harmful / neutral candidate
```

说明：

```text
Oracle headroom exists
Selector bottleneck remains
```

---

## `C4-P3` — Low Confidence but Correct

```text
u0 has low confidence signal
final outcome correct
siblings do not improve
```

说明：

```text
uncertainty signal
≠ error label
```

---

## `C4-P4` — Correct State, Harmful Repair

```text
baseline would succeed
intervention replaces it with failing candidate
```

这是 harmful transition，应单独计入净收益。

---

# C4.8 Metrics Lens

C4 适合同时报告：

```text
Trigger Coverage
Oracle Rescue Rate
Selector Rescue
Harmful Replacement
Net Gain
Candidate Count
Token / Generation Cost
Success@Budget
```

必须区分 population：

```text
all screened states
eligible states
triggered states
candidate-generated states
selected-intervention states
```

---

# C4.9 Derived Data Assets

```text
Risk Detector Data
Process Labels
Same-prefix Preference
Recoverability Labels
Repairability Labels
Selector Training Data
Continue / Stop Data
Compute Allocation Data
Counterfactual Branch Data
Regression States
```

---

# C4.10 Chapter Lens

| Chapter | 使用 C4 看什么 |
|---|---|
| Ch4 | correctness / risk / recoverability / repairability / selectability |
| Ch8 | candidate pool / oracle / selector / abstention |
| Ch9 | state-hard mining / uncertainty / frontier |
| Ch13 | counterfactual credit / local harmful action |
| Ch16 | paired evaluation / denominator / cost |
| Ch18 | state-data investment value |
| Ch21 | controlled data intervention on reasoning states |
| Ch23 | trigger / score / calibration drift |
| Ch25 | reasoning-data problem routing |

---

# C4.11 Stable Language

优先引用：

```text
C4-SC  same-prefix set
C4-CS  continue / stop
C4-BR  branch / repair
C4-P1 ... C4-P4 pattern
```

> **C4 的核心贡献，是把“当前 reasoning state 看起来可疑”继续拆成：会不会错、能不能救、系统救不救得了，以及在线到底选不选得出来。**
