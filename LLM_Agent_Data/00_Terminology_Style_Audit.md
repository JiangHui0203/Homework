# LLM / Agent Data Knowledge System：Terminology & Style Audit

> 状态：`PASS — Acceptance Baseline / Maintenance Reference`
>
> 目的：统一全书 canonical terminology 的拼写、大小写、连字符与语义边界，同时避免把自然语言正文机械改造成“每个英文词都首字母大写”的不自然文本。
>
> 原则：**统一的是概念身份，不是表面排版癖好。Canonical definition / title / table 使用稳定写法；普通叙述句可以自然小写，但不能悄悄改变概念含义。**

---

# 0. 两种一致性必须分开

## Semantic Consistency

必须严格：

```text
Outcome ≠ Reward ≠ Credit
Error ≠ Failure ≠ Root Cause
Risk ≠ Correctness ≠ Recoverability
Recoverability ≠ Repairability ≠ Selectability
Tool ≠ Harness ≠ Environment
Evidence ≠ Judgment ≠ Label
Benchmark ≠ Protocol ≠ Run ≠ Report
```

这类差异不是 style，而是方法论本身。

## Surface Consistency

需要统一 canonical form，但不需要把每个普通句子都强制 Title Case：

```text
Post-training
LLM-as-a-Judge
Agent-visible State
World State
Reasoning State
Working State
Same-prefix / Same-state
Best-of-N
Data Flywheel
Data Curation
```

---

# 1. Canonical Spelling Table

| Concept | Canonical form | Avoid as canonical label |
|---|---|---|
| post-training | `Post-training` | `Posttraining`, `Post Training` |
| pretraining | `Pretraining` | `Pre-training` 作为全书主写法 |
| supervised fine-tuning | `SFT` / `Supervised Fine-tuning` | 同一表格中混用多个缩写写法 |
| LLM judge | `LLM-as-a-Judge` | `LLM as a Judge`, `LLM-as-Judge` |
| agent-visible state | `Agent-visible State` | `Agent Visible State` 作为 canonical label |
| world state | `World State` | `WorldState` |
| environment state | `Environment State` | `Env State` 作为正式定义 |
| reasoning state | `Reasoning State` | `ReasoningState` |
| working state | `Working State` | `Work State` |
| tool use | `Tool Use` / `Tool-use Data` | 标题内随机切换 `Tooluse` |
| same-prefix | `Same-prefix` | `Same Prefix` 作为定义标签 |
| same-state | `Same-state` | `Same State` 作为定义标签 |
| best-of-N | `Best-of-N` | `Best of N` 作为正式术语 |
| hard negative | `Hard Negative` | 无必要时缩写成 `HN` |
| data flywheel | `Data Flywheel` | `DataFlywheel` |
| data curation | `Data Curation` | 与 `Cleaning` 等价使用 |
| data intervention | `Data Intervention` | 把所有 intervention 都写成 `Add Data` |
| evaluation protocol | `Evaluation Protocol` | 与 `Benchmark` 混用 |
| claim scope | `Claim Scope` | 只写结论不写 scope |

说明：表中“canonical form”主要用于：

```text
标题
术语表
定义段
表格 key
图节点
索引
```

普通中文句子里可以写：

```text
“当前 agent-visible state 中缺少该 observation”
```

只要语义明确；不要求机械改成整句 Title Case。

---

# 2. State Family

Glossary 已固定：

```text
World State
Environment State
Agent-visible State
Reasoning State
Working State
```

当前验收结果：`PASS`。

全书最重要的 style rule 不是 capitalization，而是：

> **尽量避免裸写 `State`。**

如果正文确实使用小写 `state`，必须能从局部上下文唯一判断是哪一种；在 canonical definition、schema key 或跨章对比中应写全名。

禁止把：

```text
World State
```

和：

```text
Agent-visible State
```

因为语言简化而重新合并成一个模糊 `State`。

---

# 3. Evaluator Family

Canonical：

```text
Verifier
Grader
Judge
LLM-as-a-Judge
```

当前验收结果：`PASS`。

规则：

```text
Verifier ⊂ Grader
```

是本书的 practical convention；`Judge` 强调解释性判断。

允许章节标题写：

```text
Grader / Verifier / Judge
```

也允许正式标题写：

```text
Grader、Verifier 与 LLM-as-a-Judge
```

这不是术语冲突。

真正禁止的是：

```text
Reward Model = Judge
Judge = Ground Truth
Verifier = LLM Judge 的同义词
```

---

# 4. Training-stage Terms

Canonical：

```text
Pretraining
Continued Pretraining
Instruction Data
SFT
Post-training
Preference
Reward / RL
Process Supervision
Agent Training
```

当前 Ch2 已采用：

```text
Pretraining、Instruction、SFT 与 Post-training Data
```

验收结果：`PASS`。

风格规则：

- 正式标题 / 表格使用 `Post-training`；
- 不新增 `Posttraining` 这一第二拼写；
- `pretraining` 在普通英文句中可小写，但 canonical label 使用 `Pretraining`；
- `Post-training` 是宽义阶段集合，不与 `DPO / RLHF` 等价。

---

# 5. Agent System Terms

Canonical：

```text
Task
Case
Episode
Trajectory
Decision
Action
Observation
Tool
Harness
Environment
```

当前验收结果：`PASS`。

尤其保持：

```text
Decision Intent
≠ Executed Action

Tool Result
≠ Observation
≠ World State

Task
≠ Case
≠ Episode
≠ Trajectory
```

不要为了语言简洁把：

```text
“一次任务”
```

同时拿来指 Task / Case / Episode。

中文正文若必须使用“一次任务”，最好在首次出现处补英文对象。

---

# 6. Failure / Causality Terms

Canonical：

```text
Outcome
Error
Failure
Symptom
Immediate Mechanism
Root Cause
Failure Layer
Failure Owner
First Error
First Harmful Action
Last Recoverable State
Point of No Return
```

当前验收结果：`PASS`。

规则：

- `Failure Layer` 表示 failure 在哪层呈现；
- `Failure Owner` 表示主要修复责任属于谁；
- `Root Cause` 不应被 `First Error` 替代；
- `First Harmful Action` 不等于最早不完美行为。

这组词的意义一致性比大小写更重要。

---

# 7. Counterfactual / Candidate Terms

Canonical：

```text
Same-prefix Candidate
Same-state Candidate
Baseline
Alternative / Intervention
Rescue
Harmful
Neutral-positive
Neutral-negative
Oracle@N
Selector
Selectability
Best-of-N
```

当前验收结果：`PASS`。

规则：

```text
Rescue / Harmful
```

只描述相对 baseline 的 outcome transition，不是 candidate 固有属性。

`Oracle` 是 offline upper bound，不等于 online selector capability。

---

# 8. Data Lifecycle Terms

Canonical：

```text
Data Asset
Data Batch
Dataset View
Data Flywheel
Data Strategy
Data Governance
Data Curation
Data Mixture
Data Intervention
Data Experiment
Data Production System
Monitoring / Drift
```

当前验收结果：`PASS`。

需要长期避免的语义滑移：

```text
Data Quality ≠ Data Value
Data Curation ≠ Data Experiment
Data Strategy ≠ Data Mixture
Monitoring ≠ Diagnosis
Production Log ≠ Training Data
```

---

# 9. Hyphenation / Symbol Style

推荐：

```text
state-dependent
same-prefix
same-state
budget-matched
cost-aware
failure-driven
model-relative
high-risk
end-to-end
LLM-as-a-Judge
Best-of-N
```

但不要求把所有中文句中的英文修饰短语都机械加连字符；只在它作为稳定英文 compound / canonical label 时保持一致。

数学符号：

```text
τ = trajectory
s_t = state
π = future policy / continuation when discussing Recoverability
I_D = data intervention operator
D_i / w_i = mixture bucket / weight
```

同一章内不要同一符号承担两个完全不同的 canonical semantics。

---

# 10. 当前发现的冲突

在本轮人工对照的：

```text
Glossary
Landing Page
Ch1
Ch2
Ch3
Ch4
Ch5
Ch11
Ch15
Ch20
Ch23
Ch25
```

以及此前连续通读的 Ch0–25 中，**没有发现需要立刻修复的高置信 semantic terminology conflict**。

需要注意：GitHub Code Search 对本仓库出现过 incomplete indexing，因此：

> **本结论是 canonical anchors + continuous read-through 的人工一致性判断，不是字符级全仓库 grep 证明。**

---

# 11. 最终 Style Rule

全书使用下面三层规则：

```text
Level 1 — Canonical Definition
必须严格使用 Glossary 的术语和语义。

Level 2 — Figure / Table / Index
使用统一 canonical spelling / capitalization。

Level 3 — Natural Prose
允许自然语言小写和中文混排，但不能引入第二套定义。
```

这样既避免：

```text
术语漂移
```

也避免：

```text
为了“统一”把整本书写成僵硬的 API 文档。
```

---

# 12. Acceptance Result

```text
Semantic terminology consistency
PASS

Canonical spelling table
DEFINED

High-confidence conflict requiring body patch
0 found in current acceptance pass

Character-level full-repo grep proof
NOT CLAIMED
```

最终原则：

> **语言统一的目标不是让每个词看起来一样，而是让读者永远知道“这个词此刻指的是哪一个对象”。**
