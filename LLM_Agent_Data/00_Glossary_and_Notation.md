# LLM / Agent Data Knowledge System：Canonical Glossary & Notation

> 状态：Editorial Infrastructure / Canonical Terminology Draft
>
> 目的：为 1–25 章提供统一术语、对象边界和符号约定。后续章节精修时，以本文件作为默认语言标准；若某章需要特殊定义，应显式说明局部语义，而不是静默改变术语含义。

---

# 0. 使用原则

1. **同一个词尽量只表达一个核心概念。**
2. **不同层级对象不要因为日常口语相近就混用。**
3. **`Outcome / Reward / Credit`、`Error / Failure / Root Cause`、`Verifier / Grader / Judge` 等必须长期保持区分。**
4. **避免裸写 `State`，尽量写清楚是哪一种 state。**
5. **公式只做语义压缩，不制造伪精确。**
6. **如果行业没有统一标准，本体系会明确标注“practical convention / 实用约定”。**

---

# 1. Data Object：数据对象

## Dataset

一组按照某种目的、schema、selection policy 和版本规则组织起来的数据记录。

```text
Dataset
≠
一个文件名
```

一个 Dataset 应尽量具有：

```text
dataset_id
version
schema_version
selection / build policy
manifest
```

---

## Sample / Example

Dataset 中一个基本记录单元。

它可能是：

```text
prompt-response pair
preference pair
reasoning step
trajectory
failure record
benchmark case
```

因此 `sample` 是容器概念，不代表固定的数据粒度。

---

## Data Asset

可长期复用、具有明确身份与用途的数据资产。

例如：

```text
Human Gold Set
Agent Regression Set
Tool-use Preference Pool
Failure Taxonomy Dataset
```

---

## Data Batch

某次具体生产、采集、标注或合成得到的一批数据。

通常具有：

```text
source
production time
source model
selection policy
cost
quality report
```

---

## Dataset View

从 canonical data 根据特定 transform / selection / formatting rule 派生出来的数据视图。

例如：

```text
Canonical Trajectory
├── SFT View
├── Preference View
├── Regression View
└── Judge Calibration View
```

核心约定：

> View 是派生用途，不应该脱离 source lineage 变成另一份“真相”。

---

# 2. Task / Case / Episode / Trajectory

## Prompt

模型直接接收到的文本或结构化输入。

Prompt 只是 Task 的一个组成部分。

---

## Task

完整的任务定义。

Agent 场景中通常包含：

```text
Goal
Initial State
Available Actions / Tools
Constraints
Permissions
Hidden State
Success Condition
Termination Condition
```

因此：

```text
Prompt ⊂ Task
```

---

## Case

本体系中的实用约定：

> 一个具有稳定身份、可作为训练、分析或评测单位引用的具体任务实例。

在 benchmark 场景下，Case 往往进一步冻结：

```text
Task
Environment Snapshot
Verifier
Evaluation Protocol
```

---

## Episode

某个 Agent / Model 在一个 Task 上的一次实际运行。

```text
Task + Runtime / Policy
→ Episode
```

同一个 Task 可以产生多个 Episode。

---

## Trajectory / Trace

Episode 中实际发生的状态、决策、动作、环境反馈和终止过程。

经典表示：

\[
\tau=(s_0,a_0,o_1,s_1,a_1,o_2,\ldots,s_T)
\]

工程上更推荐理解成：

> typed event log + state lineage + execution evidence

本体系默认 `Trajectory` 与 `Trace` 大多数场景近义，但：

- `Trajectory` 更强调决策 / 状态路径；
- `Trace` 更强调记录 / 日志表现形式。

---

# 3. State：状态体系

## State

一个抽象的“当前决策条件”。

**后续正文尽量避免裸写 `State`。**

---

## World State

环境中真实存在的完整状态。

例如：

```text
数据库真实记录
文件系统真实内容
Calendar 当前事件
订单真实状态
```

Agent 通常无法直接看到完整 World State。

---

## Environment State

指由 Environment 定义和维护的外部状态。

多数情况下与 World State 高度重叠，但强调它属于可执行环境层。

---

## Agent-visible State

Agent 当前决策时可获得的信息。

包括：

```text
user request
system / policy constraints
tool descriptions
visible conversation
observations
retrieved memory
working state
```

核心：

```text
World State
≠
Agent-visible State
```

---

## Reasoning State

模型内部推理过程在某一时刻已经形成、并用于下一步 reasoning decision 的当前推理上下文 / 前缀状态。

用于：

```text
continue / stop
branch / repair
risk estimation
same-prefix comparison
```

---

## Working State

系统显式维护、可记录、可复现，并供后续决策使用的结构化工作状态。

例如：

```text
current plan
open subgoals
known facts
pending verification
resolved entities
```

不要把它与不可观测的神经 hidden state 混同。

---

## Memory

跨较长时间或跨 Episode 保存的信息。

应区分：

```text
Memory Write
Memory Store
Memory Retrieval
Memory Read / Injection
```

Memory 中的数据可能本身成为 failure source。

---

# 4. Decision / Action / Observation

## Decision

Agent / Model 对当前 state 做出的策略选择。

可能表现为：

```text
选择工具
选择 reasoning branch
选择继续 / 停止
选择澄清
选择验证
选择回退
```

---

## Action

真正进入 runtime / environment 的可执行行为。

例如：

```text
tool call
final response
ask user
write memory
wait
abort
verify
```

核心：

```text
Decision Intent
≠
Executed Action
```

---

## Observation

Agent 从环境、工具、用户或其他外部过程获得的新信息。

例如：

```text
Tool Result
User Reply
Timeout
Permission Error
File Change
Environment Event
```

---

## Observation Grounding

Observation 是否真正影响了后续 state update 与 decision。

例如：

```text
Observation: order = shipped
↓
Agent仍执行 refund
```

即 observation 存在，但 grounding 失败。

---

# 5. Tool / Harness / Environment

## Tool

Agent 可调用的动作接口。

定义：

```text
name
description
arguments
return schema
permissions
side-effect type
```

---

## Harness

组织模型、工具、环境和执行流程的 runtime orchestration layer。

负责例如：

```text
tool schema injection
tool call parsing
execution routing
observation injection
retry
stop condition
memory
context management
logging
```

---

## Environment

Tool / Action 实际作用的外部世界。

可抽象为：

\[
E=(S,A,T,O,R,G)
\]

其中：

```text
S = State
A = Actions
T = Transition
O = Observation
R = Reward / Feedback (optional)
G = Goal / Success Predicate
```

全书固定：

```text
Tool = Action Interface
Harness = Runtime Orchestration
Environment = World + Transition
```

---

# 6. Outcome / Reward / Credit

## Outcome

世界实际发生了什么。

属于事实层。

例如：

```text
任务成功
订单未取消
8/10 tests passed
Agent 正确拒绝不可执行任务
```

---

## Reward

人为设计、用于优化或排序的反馈信号。

例如：

```text
success = +1
unauthorized write = -2
extra tool call = -0.01
```

核心：

> Reward 是设计出来的，不是世界天然自带的。

---

## Credit

最终 outcome / reward 应该归因到哪些中间 decision / action，以及归因多少。

```text
Outcome
↓
Reward Design
↓
Credit Assignment
```

三者必须保持分离。

---

# 7. Correctness / Risk / Recoverability / Repairability / Selectability

## Correctness

当前 step / state / action 是否已经违反正确性条件。

回答：

> “这里已经错了吗？”

---

## Risk

当前状态是否具有更高未来失败风险或值得额外关注。

回答：

> “这里危险吗？”

可能使用：

```text
logprob
entropy
margin
constraint conflict
state inconsistency
```

但：

```text
Risk ≠ Error
```

---

## Recoverability

从当前 state 出发，是否存在某种未来策略可以让最终结果恢复到成功。

回答：

> “从这里理论上还有没有救？”

---

## Repairability

在当前允许的动作、时间和 budget 下，是否实际能够完成修复。

因此：

```text
Recoverable in principle
≠
Repairable under current budget
```

---

## Selectability

当更好的 alternative 存在时，当前可用 selector / scorer / observable evidence 是否足以可靠识别它。

回答：

> “有救是一回事，我们认不认得出那条更好的路？”

---

# 8. Error / Failure / Symptom / Root Cause

## Error

一个局部 decision / action / reasoning step 的错误。

---

## Failure

Task / Episode / Subgoal 未达到要求，或违反关键约束的结果。

```text
Error
不一定最终导致 Failure
```

反之，Failure 也可能来自 infrastructure，而不是 model error。

---

## Symptom

外部观察到的失败表现。

例如：

```text
最终任务没完成
重复发送邮件
错误退款
工具调用死循环
```

Symptom 不等于 Root Cause。

---

## Root Cause

导致失败的最根本机制或能力缺口。

例如：

```text
negative constraint 没被建模
entity resolution 出错
harness 丢失 observation
```

---

## First Error

最早出现的不正确行为。

---

## First Harmful Action

最早真正降低最终成功可能或破坏关键状态的 action。

```text
First Error
≠
First Harmful Action
```

---

## Last Recoverable State

失败轨迹中，仍存在可行 alternative 能够 rescue 的最后一个 state。

---

## Point of No Return

从 Last Recoverable State 之后进入不可恢复区域的关键 transition / action。

---

# 9. Counterfactual / Rescue / Harmful / Neutral

## Counterfactual

控制历史 state / prefix 等关键条件，只改变局部 action / continuation，观察未来 outcome 的比较。

典型：

```text
Same State s
├── baseline a0 → outcome O0
└── alternative a1 → outcome O1
```

---

## Rescue

```text
Baseline Fail
→ Alternative / Intervention Success
```

---

## Harmful

```text
Baseline Success
→ Alternative / Intervention Fail
```

---

## Neutral-positive

两者均成功。

---

## Neutral-negative

两者均失败。

---

## Net Gain

在简单二元任务中常使用：

\[
Net = Rescue - Harmful
\]

具体 denominator 必须随报告明确给出。

---

# 10. Candidate / Rollout / Selection

## Rollout

从某个 task / prompt / state 出发，让 policy 实际生成 response / reasoning / trajectory 并观察 outcome。

---

## Candidate

同一个选择问题下的一个可比较 alternative。

可能是：

```text
完整回答
reasoning continuation
next action
trajectory
```

---

## Same-prefix / Same-state Candidate

从完全相同历史 state 出发，只改变局部 continuation / action 得到的候选。

它比不同 prefix 的 candidate 更适合局部归因和 counterfactual analysis。

---

## Oracle

假设存在完美 selector 时，candidate pool 可以达到的理论上限。

Oracle 高、Selected 低：

```text
selection bottleneck
```

Oracle 本身低：

```text
generation bottleneck
```

---

## Selector

在 candidate pool 中执行选择 / 替换 / abstain / keep-baseline 等决策的机制。

---

# 11. Verifier / Grader / Judge

## Verifier

根据明确事实、形式规则或可执行条件判断结果。

例如：

```text
exact / symbolic checker
unit tests
final environment predicate
state diff
```

---

## Grader

更宽泛的评价器。

可以是：

```text
program
rule
model
human
hybrid
```

输出：

```text
pass/fail
score
rubric dimensions
failure type
```

本体系采用实用约定：

```text
Verifier ⊂ Grader
```

---

## Judge

强调对难以完全程序化的问题进行解释性判断的 evaluator。

通常指：

```text
LLM-as-a-Judge
Human Judge
```

---

## Evidence-first Principle

评价顺序优先：

```text
Direct Environment Evidence
>
Executable Verification
>
Deterministic Rule
>
Structured Grader
>
LLM Judge
>
Agent Self-report
```

不是说越靠后越差，而是：

> 如果直接证据存在，不应主动把问题升级成主观判断。

---

# 12. Gold / Anchor / Regression

## Gold Set

通过高可信流程得到的 reference labels / decisions，用于：

```text
annotation calibration
judge calibration
benchmark truth
quality audit
```

---

## Anchor Set

强调跨 evaluator / version 长期保持稳定、用于检测测量漂移的一组 case。

例如 Judge Anchor Set。

Gold Set 和 Anchor Set 可以重叠，但目的不同。

---

## Regression Set

历史已经发现、修复或被认为关键的问题集合，用于防止旧问题重新出现。

```text
Regression performance
≠
Population performance
```

---

# 13. Benchmark / Protocol / Population

## Benchmark

被定义好的测量对象与 case 集合。

---

## Evaluation Protocol

规定如何运行和评价 benchmark 的冻结实验规则。

包括：

```text
model
prompt
decoding
toolset
harness
environment
budget
verifier / judge
post-processing
metric
```

---

## Population

研究 / 产品结论所针对的总体。

必须区分：

```text
Total Population
Eligible Population
Triggered Population
Intervened Population
Resolved Population
```

---

## Coverage

某种 policy / evaluator / intervention 实际处理到的 population 比例。

任何 Coverage 指标必须明确 denominator。

---

# 14. Data Value / Quality / Mixture

## Data Quality

多维概念，不应默认压成一个总分。

可能包括：

```text
Correctness
Relevance
Completeness
Verifiability
Novelty
Diversity
Difficulty
Safety
Privacy
Provenance
```

---

## Data Value

一条 / 一批数据对目标能力、产品或风险控制的预期或测得贡献。

核心：

```text
High Quality
≠
High Learning Value
```

---

## Data ROI

概念上：

\[
DataROI(D)=\frac{\Delta Utility(D)}{TotalCost(D)}
\]

必须明确 Utility 与 Cost 的定义。

---

## Mixture

多个数据来源 / capability / task family 在训练中获得的相对 exposure policy。

核心：

```text
Dataset Size
≠
Training Exposure
```

要明确：

```text
sample ratio
token ratio
batch ratio
update ratio
```

---

## Effective Information Size

用于表达：大量高度重复 sample 并不等于大量独立学习信息。

不要求全书统一使用单一严格公式；重点是避免把 raw sample count 当作信息量。

---

# 15. Provenance / Lineage / Versioning

## Provenance

数据的来源证明。

回答：

> “它从哪里来？”

---

## Lineage

数据、标签、view、训练 run、模型和 evaluation artifact 之间的派生关系。

回答：

> “它经历了什么，又影响了什么？”

Lineage 通常是 DAG，而不是文件路径链。

---

## Versioning

系统中可变化对象必须区分版本，例如：

```text
dataset_version
schema_version
label_version
prompt_version
judge_version
environment_version
```

---

## Decision Freeze

历史 policy / selector 当时实际产生的 decision 保持不可篡改。

---

## Label Correction

后来发现 label / gold 有误后，创建新的 label version。

全书固定：

```text
Corrected Label
+
Frozen Historical Decision
→ Historical Re-score
```

不应静默 re-run policy 后覆盖历史结论。

---

# 16. Drift

## Data Drift

\[
P_{old}(X) \neq P_{new}(X)
\]

输入分布发生变化。

---

## Concept Drift

\[
P_{old}(Y\mid X) \neq P_{new}(Y\mid X)
\]

相同输入下“什么算正确”发生变化。

---

## Failure Drift

Failure composition / root-cause distribution 发生变化。

---

## Capability Drift

在相对稳定测量条件下，模型能力本身发生变化。

---

## Judge Drift

Evaluator 本身因为 model / prompt / rubric / evidence package 变化而改变测量结果。

---

## Infrastructure Drift

Tool / Harness / Environment 发生变化。

---

# 17. Research / Production

## Research Mode

目标：快速回答科学问题。

允许：

```text
manual steps
small cohort
narrow scripts
limited portability
```

只要关键 protocol 与 evidence 被记录。

---

## Production Mode

目标：稳定规模化。

通常要求：

```text
versioning
queue
retry
lineage
cost accounting
access control
monitoring
SLA
```

---

## Research-to-Production Gate

只有在 research prototype 已提供足够 evidence 后，才值得将稳定接口平台化。

原则：

> 平台化稳定接口，不平台化尚未稳定的研究假设。

---

# 18. 推荐符号

| 符号 | 含义 |
|---|---|
| \(x\) | task / input |
| \(y\) | response / candidate output |
| \(s_t\) | 当前 state（正文必须说明 state 类型） |
| \(a_t\) | action / decision action |
| \(o_{t+1}\) | observation |
| \(\tau\) | trajectory |
| \(R\) | reward / utility，必须在局部定义 |
| \(V(s)\) | state value / future value |
| \(Q(s,a)\) | action-conditioned future value |
| \(A(s,a)\) | action advantage（如使用） |
| \(D\) | dataset / data batch，局部说明 |
| \(M\) | model / mixture，避免同一公式中歧义 |

注意：

> 同一个字母不能在同一章节中同时表示两种对象。若已有章节符号冲突，精修时优先局部改名，而不是全书机械替换。

---

# 19. 全书固定原则句

以下可以作为高频核心原则，但后续章节应尽量采用“引用 + 应用”，而不是重新展开完整论证。

```text
Example → Experience

Risk ≠ Error
Low confidence ≠ Wrong ≠ Worth repairing

Tool success ≠ Task success
Final response correctness ≠ Environment success

Outcome ≠ Reward ≠ Credit
First Error ≠ First Harmful Action ≠ Root Cause

Recoverability ≠ Repairability
Candidate existence ≠ Selectability

Verifier / Judge output ≠ Ground Truth
Evidence first, Judge second

High Agreement ≠ High Validity
High Quality Data ≠ High Learning Value
Raw Sample Count ≠ Effective Information Size
Dataset Size ≠ Training Exposure

Production Log ≠ Training Data
Failure ≠ Data Problem
Monitoring Alert ≠ Model Regression

Corrected Label ≠ Historical Decision Rewrite

Stable Ruler + Moving Frontier
```

---

# 20. 后续维护规则

新增概念前先问：

```text
1. 它是否已经存在同义词？
2. 它和已有概念真正区别是什么？
3. 哪一章拥有它的 canonical definition？
4. 是否需要进入 Glossary？
5. 是新知识，还是旧知识的新应用？
```

如果只是旧概念的新应用：

> 优先链接，不新增术语。
