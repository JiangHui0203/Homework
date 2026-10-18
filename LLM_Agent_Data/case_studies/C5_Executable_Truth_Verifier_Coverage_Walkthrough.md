# C5 Practical Walkthrough：从“代码看起来正确”到 Executable Truth

> 状态：`Practical Case Study / Stable Mother Edition V3.x`
>
> Canonical Case：[`C5 — Code / Execution Agent`](../cases/C5_Code_Execution_Agent.md)
>
> 主要 Variant：`C5-POOL + C5-F2 + C5-F3 + C5-F4 + C5-F5 + C5-F6`
>
> 目的：用一个可执行代码任务，把 `Task Contract → Candidate Pool → Evidence → Verifier Coverage → Judge → Hidden Evaluation → Runtime → Repair → Data → Experiment → Production → Monitoring` 串成一条完整链。
>
> 注意：**本文是 walkthrough，不改变 C5 的稳定 ID 语义。所有 canonical definition 仍以 `cases/C5_Code_Execution_Agent.md`、Glossary 与对应章节为准。**

---

# 0. 为什么 C5 不只是“代码题案例”？

C5 的真正问题不是：

```text
模型会不会写 normalize_date？
```

而是：

> **当任务存在可执行真值时，我们怎样让 Evidence、Verifier、Judge、Runtime、Repair 与 Data Pipeline 围绕真实 execution truth 对齐？**

这套结构同样适用于：

```text
SQL
API workflow
configuration generation
spreadsheet formula
symbolic reasoning
structured transformation
browser / tool task
```

只要任务存在：

```text
可执行 predicate
可重放 state transition
可自动检查 output
```

就应该优先建立 executable evidence，而不是先找一个 Judge“看起来判得不错”。

---

# 1. Stable Task Contract

沿用 canonical C5：

```python
normalize_date(text) -> str | None
```

要求：

```text
2026-10-18      → 2026-10-18
2026/10/18      → 2026-10-18
Oct 18, 2026    → 2026-10-18
invalid         → None
2026-02-30      → None
```

真正的 Task Contract 不只是函数签名，还要冻结：

```text
Input Domain
Output Schema
Invalid-input Semantics
Runtime
Dependency Set
Locale / Timezone assumptions
Public Test Policy
Hidden Test Policy
Resource / Time Limits
```

否则“同一段代码”在两个环境里的结果可能不同。

第一条原则：

> **Executable Task = Artifact + Runtime + Evaluation Contract。**

---

# 2. Candidate Pool 不是四段文本，而是四个可执行对象

设同一 Task 生成：

```text
Candidate A
Candidate B
Candidate C
Candidate D
```

每个 candidate 都至少保留：

```text
candidate_id
source code
model / prompt / sampling metadata
syntax result
public-test result
hidden-test result
runtime identity
latency / token / execution cost
failure signature
```

因此 `C5-POOL` 的最小数据结构更像：

```json
{
  "case_id": "C5",
  "candidate_id": "cand_B",
  "artifact_sha": "...",
  "runtime_id": "runtime_v3",
  "verifier_suite": "date_suite_v5",
  "public_result": "PASS",
  "hidden_result": "PASS",
  "execution_cost_ms": 0,
  "judge_score": null
}
```

这里的关键不是字段名本身，而是：

```text
Code Artifact
≠ Execution Result
≠ Verifier Judgment
≠ Judge Preference
```

---

# 3. 先建立 Evidence Ladder，再决定用什么 Evaluator

对 C5，优先证据通常是：

```text
Runtime Execution
↓
Hidden / Held-out Tests
↓
Public Tests
↓
Static / Deterministic Checks
↓
Structured Grader
↓
LLM Judge
↓
Model Self-report
```

这不是绝对价值排序，而是 claim-specific evidence ordering。

如果 Claim 是：

```text
“实现是否满足 normalize_date 的功能契约？”
```

那么：

```text
Executable Tests
```

比：

```text
Judge: code quality = 9/10
```

更接近目标真值。

因此标准链应该是：

```text
Claim
→ Strongest Available Evidence
→ Evaluator
→ Raw Judgment
→ Derived Label
→ Decision
```

而不是：

```text
先选 Judge
→ 再想 Judge 分数代表什么
```

对应：

- [`F7 — Evidence → Evaluator Stack`](../figures/F7_Evidence_Verifier_Grader_Judge.md)
- [`Ch15 — Grader / Verifier / LLM-as-a-Judge`](../15_Grader_Verifier_and_LLM_as_a_Judge.md)

---

# 4. C5-F3：Judge Preference 与 Executable Truth 冲突时怎么办？

构造一个典型冲突：

```text
Candidate A
- naming 清晰
- docstring 完整
- decomposition 漂亮
- LLM Judge 偏好
- hidden tests FAIL

Candidate B
- 风格普通
- 实现更短
- LLM Judge 分数略低
- hidden tests PASS
```

如果目标 Claim 是：

```text
functional correctness
```

那么决策应是：

```text
Candidate B > Candidate A
```

不是因为“Verifier 永远比 Judge 高级”，而是因为：

> **对于这个具体 Claim，Executable Evidence 的 construct validity 更高。**

Judge 仍然可以负责：

```text
readability
maintainability
explanation quality
API ergonomics
```

但不能覆盖 executable failure。

于是 evaluation 可以拆成多维：

```text
Functional Correctness
→ executable verifier

Maintainability
→ rubric / judge / human

Safety / Policy
→ deterministic rules + evaluator
```

最后再由 task policy 定义优先级，而不是把所有维度压成一个 Judge 分数。

---

# 5. C5-F2：Public Test Pass 为什么还不能说“正确”？

设：

```text
public tests
→ ISO / slash / simple month all pass

hidden tests
→ invalid date 2026-02-30 fails
```

这是标准的：

```text
C5-F2 Public-test Overfit
```

它可能来自：

```text
visible-example memorization
insufficient boundary handling
narrow parser logic
benchmark leakage
repair only against visible cases
```

因此：

```text
Public Test Pass
≠ Task Correctness
```

更精确地说：

```text
Public Test Pass
= 在当前 visible verifier coverage 下未被证伪
```

这也是为什么 evaluation contract 必须保存：

```text
which tests
which version
which split
which family isolation
which runtime
```

否则一个 `PASS` 标签没有足够语义。

---

# 6. Verifier Coverage 本身会改变 Dataset Distribution

固定同一批 candidates，只改变 verifier：

```text
V1
syntax only

V2
syntax + public tests

V3
syntax + public + hidden tests
```

可能得到：

```text
Accepted(V1)
⊃ Accepted(V2)
⊃ Accepted(V3)
```

这意味着 verifier 不只是“测量工具”。

如果它参与：

```text
filtering
rejection sampling
Best-of-N
chosen/rejected construction
hard-negative mining
```

那么它实际上会改变：

```text
训练数据分布
```

因此：

> **Verifier Coverage 是 Data Policy 的一部分。**

这一步特别容易被漏掉。

很多团队会问：

```text
“为什么换了 verifier，训练效果也变了？”
```

答案可能不是 model / training recipe 变了，而是：

```text
what the pipeline accepts as positive data
```

已经变了。

---

# 7. C5-F6：Verifier 也可能错

现在反过来。

假设：

```text
implementation actually correct
↓
checker expected output has bug
↓
verifier marks FAIL
```

这是：

```text
C5-F6 False-negative Verifier
```

如果把 verifier 当 ground truth，会产生：

```text
correct candidate rejected
wrong preference pair
bad training label
misleading benchmark score
false failure diagnosis
```

所以 Verifier 自己也必须进入：

```text
Versioning
Regression
Calibration / Validation
Failure Analysis
Monitoring
```

最低资产：

```text
verifier_id
suite_version
runtime_id
expected-output source
known limitations
regression tests
```

这正是：

```text
Verifier
≠ Ground Truth by definition
```

而应该是：

```text
Verifier
= 对某类 Evidence 的可审计检查机制
```

---

# 8. C5-F4：Runtime Mismatch 不能算成纯 Model Failure

固定：

```text
same task
same code artifact
same tests
```

只改变：

```text
C5-R1 runtime
vs
C5-R2 runtime
```

如果结果从：

```text
PASS → FAIL
```

则需要问：

```text
Python / dependency version?
locale?
timezone?
OS behavior?
filesystem / sandbox permission?
resource limits?
```

这说明：

```text
Artifact Correctness
```

必须条件化于：

```text
Execution Environment
```

因此一个 benchmark 若想比较模型，而 runtime 漂了，就存在 confound。

Failure record 应至少区分：

```text
Model-generated artifact defect
Runtime compatibility defect
Harness execution defect
Verifier defect
```

对应：

- [`F4 — Agent Task–Environment–Trajectory`](../figures/F4_Agent_Task_Environment_Trajectory.md)
- [`F6 — Credit → Failure`](../figures/F6_Credit_to_Failure_Causal_Map.md)
- [`F8 — Evaluation Protocol`](../figures/F8_Benchmark_Evaluation_Protocol.md)

---

# 9. C5-F5：Repair 之后为什么必须重新走完整 Evidence？

典型 repair：

```text
test fails on one visible case
↓
model patches that branch
↓
visible case passes
```

错误做法：

```text
repair accepted
```

正确问题是：

```text
Did the repaired artifact satisfy the full contract?
```

因此 Repair Evaluation 至少重新检查：

```text
original failure
held-out boundary cases
general regression
runtime compatibility
side effects / complexity if relevant
```

这能区分：

```text
Local Patch
≠ General Repair
```

一个有用的 repair trajectory 应保存：

```text
pre-repair artifact
failure evidence
repair decision
post-repair artifact
full-suite result
new regressions
cost
```

这样它才能真正变成：

```text
Repair SFT
Recovery Preference
Process Supervision
Regression Asset
```

---

# 10. Candidate Pool：Oracle 与 Selector 仍然必须分开

对 `C5-POOL`：

## Oracle

回答：

```text
完整 executable truth 下，pool 里有没有正确 candidate？
```

## Online Selector

只能使用运行时允许的信息，例如：

```text
public tests
static checks
partial execution
model likelihood
cheap verifier
```

不能偷看：

```text
hidden tests
future held-out outcome
post-hoc adjudication
```

因此：

```text
Oracle Best-of-N
≠ Online Best-of-N
```

如果：

```text
Oracle 95%
Online selector 72%
```

研究问题不是“再生成更多 candidate”，而可能是：

```text
selection evidence too weak
```

这与 C4 的 reasoning candidate 问题同构：

```text
Candidate Exists
≠ Candidate Selectable
```

但 C5 多了一层：

```text
Executable Truth
```

因此特别适合解释 Verifier / Selector 的接口。

---

# 11. 从 Failure Family 到 Data Assets

围绕 C5 可以构造四类数据，而不是只保留“正确答案”。

## A. Correct Artifact Data

```text
valid implementation
+
full executable evidence
```

可用于：

```text
SFT
reference solution
regression
```

## B. Executable Hard Negatives

例如：

```text
public pass / hidden fail
beautiful code / functional fail
runtime-specific fail
```

它们比：

```text
syntax error / nonsense code
```

更有训练价值，因为更接近真实 decision boundary。

## C. Repair Trajectories

```text
failed artifact
→ failure evidence
→ repair
→ re-verification
```

## D. Evaluator Data

```text
verifier false positive
verifier false negative
judge/verifier disagreement
runtime-sensitive case
```

这一类数据不是直接训练主模型，而是训练 / 校准：

```text
Verifier
Grader
Selector
Judge policy
```

---

# 12. Controlled Experiment：到底是“数据有用”，还是 Verifier 变严了？

假设我们想验证：

> executable hard negatives 能否提高边界 case correctness？

一个最小可信设计：

```text
Baseline
B = current code-data mixture

Treatment
I_D(B)
= matched-token replace 一部分 easy negatives
  with C5-style executable hard negatives
```

固定：

```text
base model
training recipe
train token budget
runtime
benchmark protocol
verifier suite
```

评测至少包括：

```text
Target Eval
→ hidden boundary cases

Transfer Eval
→ other parsing / validation tasks

General Regression
→ normal code generation

Repair Eval
→ failure → repair → full re-check

Cost
→ generation / execution / verifier cost
```

需要特别避免：

```text
Treatment data 用 V3 verifier 过滤
Baseline data 用 V1 verifier 过滤
```

否则：

```text
Data Intervention
```

和：

```text
Verifier Policy Change
```

混在一起。

对应：

- [`Ch20 — Data Curation`](../20_Data_Quality_Filtering_Deduplication_and_Mixture.md)
- [`Ch21 — Data Experiments`](../21_Data_Experiments_and_Causal_Validation.md)

---

# 13. Production：Sandbox 不只是“能跑代码”

规模化生产 C5-style data，worker 至少需要：

```text
isolated execution
runtime image / environment identity
resource limits
timeouts
artifact hashing
stdout / stderr capture
exit code
public / hidden split isolation
verifier version
retry semantics
```

特别要区分：

```text
Infrastructure Retry
≠ Model Repair
```

例如：

```text
worker crashed
→ infra retry
```

和：

```text
candidate test failed
→ model sees failure and edits code
```

是两类完全不同的事件。

如果生产日志把它们合并成：

```text
final_status = success
```

就会把真实 Agent / Model recovery ability 隐掉。

---

# 14. Lineage：一个 PASS 到底是谁判出来的？

理想 lineage：

```text
Task Case
→ Candidate Artifact
→ Runtime Image
→ Public Test Suite
→ Hidden Test Suite
→ Verifier Result
→ Derived Label
→ Candidate Selection
→ Training View
→ Train Run
→ Eval Run
→ Report
```

于是如果后来发现：

```text
hidden verifier v5 有 bug
```

可以回答：

```text
哪些 candidate label 受影响？
哪些 training view 用过？
哪些 model run 被污染？
哪些 benchmark result 需要 re-score？
```

而不是全部重跑。

对应：

- [`F11 — Governance / Lineage DAG`](../figures/F11_Governance_Lineage_DAG.md)
- [`Ch19 — Governance / Lineage`](../19_Data_Governance_Lineage_and_Reproducibility.md)

---

# 15. Monitoring：线上 code success 下降先查什么？

不要直接说：

```text
model coding ability regressed
```

依次检查：

```text
Metric / test definition changed?
↓
Verifier version changed?
↓
Runtime / dependency changed?
↓
Task mix changed?
↓
Hidden-case distribution changed?
↓
Frozen benchmark regressed?
↓
New failure frontier emerged?
```

典型 drift：

```text
Runtime Drift
Verifier Drift
Task / Library Drift
Failure Drift
Capability Drift
```

因此 C5 也是 F13 的一个重要 executable-task lens。

---

# 16. C5 最终压缩成五个 Decision Gates

整个 walkthrough 最后可以压成：

```text
Gate 1 — Evidence
有没有比语言判断更直接的 executable evidence？

Gate 2 — Coverage
Verifier 到底覆盖了 spec 的多少？

Gate 3 — Attribution
失败属于 Artifact、Runtime、Harness 还是 Verifier？

Gate 4 — Repair
修复是否通过完整 re-verification，而不是只过 visible case？

Gate 5 — Data Value
这种 executable failure family 进入训练后，是否带来 held-out gain，且没有 regression？
```

只有五关都能回答，才可以从：

```text
“模型写代码错了”
```

升级成：

```text
“我们知道什么错、凭什么知道、该修哪一层、怎样构造成数据、怎样证明它真的有效。”
```

---

# 17. 与其他三个 Practical Case Study 的分工

```text
C1
→ conditional state-grounded Agent action

C3
→ permission / irreversible side effect / ownership

C4
→ reasoning intervention / oracle / selector / cost

C5
→ executable truth / verifier coverage / runtime / repair
```

所以 C5 补的是 C1 / C3 / C4 都无法替代的一层：

> **当世界给得出可执行真值时，如何让整个 Data / Evaluation / Repair 系统服从 executable evidence，而不是服从“看起来更像正确答案”的代理信号。**
