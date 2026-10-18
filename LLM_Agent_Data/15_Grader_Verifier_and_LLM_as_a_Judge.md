# 第 15 章 Grader、Verifier 与 LLM-as-a-Judge：从 Evidence 到可信 Label

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 前置章节：[`第 14 章 Agent Failure Taxonomy`](./14_Agent_Failure_Taxonomy.md)
>
> 关联章节：[`第 3 章 Preference Data、Reward 与 Feedback`](./03_Preference_Data_Reward_and_Feedback.md)、[`第 6 章 Human Data`](./06_Human_Data_Annotation_and_Quality_Control.md)、[`第 10 章 Agent Task Design`](./10_Agent_Task_Design.md)、[`第 11 章 Environment Design`](./11_Environment_Design.md)、[`第 13 章 Task Success 与 Credit Assignment`](./13_Task_Success_and_Credit_Assignment.md)、[`第 16 章 Benchmark Design 与 Evaluation Protocol`](./16_Benchmark_Design_and_Evaluation_Protocol.md)、[`第 19 章 Governance、Lineage 与 Reproducibility`](./19_Data_Governance_Lineage_and_Reproducibility.md)
>
> 编辑基础设施：[`Canonical Glossary`](./00_Glossary_and_Notation.md) · [`Canonical Casebook`](./00_Canonical_Casebook.md)
>
> **Master Figure：** [`F7 — Evidence → Verifier / Grader / Judge`](./figures/F7_Evidence_Verifier_Grader_Judge.md)
>
> 本章定位：**Evidence / Evaluator / Raw Judgment / Derived Label / Final Decision，以及 Verifier / Grader / Judge 边界的 canonical chapter。**
>
> 本章核心问题：**评测不是“找一个模型打分”，而是先确认我们拥有什么证据、这些证据能支持什么结论、哪个 evaluator 适合读取它、证据不足时是否应该 abstain，以及 evaluator 自己又如何被校准、审计和版本化。**

---

# 15.0 先建立评价系统的五层结构

前面不断产生：

```text
Task Success
Constraint Violation
Failure Type
Step Correctness
Preference
Recovery Quality
Reward
```

这些 Label 都必须来自某种证据与 evaluator。

全书关于 Evidence → Evaluator → Label 的 canonical visual relation 统一由 [`F7 — Evidence → Verifier / Grader / Judge`](./figures/F7_Evidence_Verifier_Grader_Judge.md) 维护。

本章使用同一套五层语义：

```text
Evidence
↓
Evaluator
↓
Raw Judgment
↓
Derived Label / Score
↓
Final Decision / Metric

Gold / Anchor Evidence
↓
Meta-evaluation
↓
Calibrate / Route / Replace
```

因此必须长期区分：

```text
Evidence
≠ Evaluator
≠ Raw Judgment
≠ Derived Label
≠ Final Decision
```

例如：

```text
Evidence:
order_1847.status = shipped

Evaluator:
rule verifier v3

Raw Judgment:
predicate shipped == true

Derived Label:
refund_forbidden = true

Final Decision:
Episode = policy-compliant success / failure
```

如果这些层混在一起，后续 rubric 更新、label correction、历史重算都很难审计。

---

# 15.1 Verifier、Grader、Judge：canonical boundary

现实团队命名并不统一，本书采用以下**实用约定**。

## Verifier

> **依据明确、可检查的事实、形式规则、可执行条件或环境状态，对一个命题进行验证的 evaluator。**

典型：

```text
exact / normalized answer check
symbolic equivalence
unit tests
SQL execution
state predicate
permission check
constraint checker
```

Verifier 不一定只输出布尔值，也可以输出：

```text
PASS / FAIL / UNRESOLVED
partial predicate results
counterexample
execution evidence
```

但它的核心是：

> **判断建立在可明确检查的 evidence 上。**

---

## Grader

> **把 Evidence 映射成 Score / Label / Rubric Dimension 的广义评价系统。**

Grader 可以是：

```text
rule
program
reward model
LLM
human
hybrid system
```

因此在本书约定中：

```text
Verifier ⊂ Grader
```

即 Verifier 是证据约束更强的一类 Grader。

---

## Judge

> **当评价标准不能被完全程序化时，对 Evidence 做解释性判断的 Grader。**

常见：

```text
LLM-as-a-Judge
Human Judge
Expert Review
```

适合：

```text
clarity
user intent satisfaction
subtle instruction following
planning quality
whether clarification was appropriate
open-ended preference
```

所以：

```text
Verifier
→ 事实 / 可执行条件

Judge
→ 解释性判断

Grader
→ 二者的上位概念
```

---

# 15.2 第一原则：Evidence First, Judge Second

错误做法：

```text
先决定“用 GPT Judge”
↓
所有问题都交给 Judge
```

更可靠的顺序：

```text
先定义要证明的 Claim
↓
找到最直接的 Evidence
↓
判断哪些部分可确定性验证
↓
剩余部分再选择解释性 Grader / Judge
```

例如 Task：

```text
取消订单 1847
```

最强 evidence 是：

```text
Environment State:
order_1847.status == cancelled
```

那么不应该让 LLM 根据一句：

```text
“已经帮你取消。”
```

去猜真实执行结果。

---

## 15.2.1 默认 Evidence 强度层级

在同一个事实性 Claim 上，如果都可用，可以优先：

```text
Direct Environment / Execution Evidence
        >
Executable Verification
        >
Deterministic Rule
        >
Structured Interpretive Grader
        >
LLM / Human Judgment from indirect evidence
        >
Agent Self-report
```

但这不是一个对所有评价维度都适用的绝对总排序。

例如：

```text
“回答是否礼貌”
```

不存在更“直接的数据库 state”。

因此更准确的原则是：

> **对于每个 Claim，使用能够最直接支持它、且可靠性已经被验证的 Evidence。**

---

# 15.3 Evidence Sufficiency：证据不够时，正确答案可能是“不判”

很多自动评价最大的隐性错误是：

```text
Evidence Missing
↓
Evaluator 仍被强迫给 PASS / FAIL
```

例如：

```text
只看到 Final Response
却要求判断数据库是否真的更新
```

这时正确输出应当是：

```text
UNRESOLVED
INSUFFICIENT_EVIDENCE
ABSTAIN
```

而不是猜。

所以每个 Evaluation Contract 都应定义：

```text
required evidence
missing-evidence behavior
abstention rule
escalation route
```

> **Coverage 可以低于 100%；伪确定性比合理 abstention 更危险。**

---

# 15.4 Deterministic Verifier：能程序化的尽量程序化

理想 Verifier 通常具有：

```text
Deterministic
Reproducible
Auditable
Versionable
Cheap
```

例如：

```text
Math
→ symbolic / normalized equivalence

Code
→ tests / execution

Agent
→ environment predicates / state diff
```

但 Deterministic 不等于“字符串 exact match”。

可能需要：

```text
canonicalization
parsing
unit conversion
symbolic equivalence
tolerance
set / order normalization
```

核心目标是：

> **把本来可验证的问题，尽可能变成稳定的事实判定。**

---

# 15.5 Executable Checker：让结果自己运行

例如代码：

```text
Candidate Patch
↓
Build
↓
Unit Tests
↓
Integration Tests
↓
Runtime / Resource Checks
```

SQL：

```text
Candidate Query
↓
Execute on hidden DB
↓
Compare result set / side effects
```

Executable Evidence 通常比“代码看起来对”强很多。

但必须牢记：

```text
Tests Pass
≠ Program universally correct
```

如果 test coverage 不足，Verifier 自身会产生 false positive。

所以 Verifier 也需要 meta-evaluation 和 adversarial test。

---

# 15.6 Agent Environment Verifier：Required / Forbidden / Invariant

Agent task 很适合把 success 写成三类 predicate：

```text
Required Predicates
→ 必须成立

Forbidden Predicates
→ 必须不成立

Invariant Predicates
→ 执行前后必须保持
```

概念上：

\[
Success=
\bigwedge_i R_i
\land
\bigwedge_j \neg F_j
\land
\bigwedge_k I_k
\]

例如会议改期：

```text
Required:
event.start == Friday 15:00
Alice in attendees

Forbidden:
external_contact_notified == true

Invariant:
unrelated_events unchanged
```

这也是为什么：

```text
Before State
After State
State Diff
```

是 Agent Evaluation 的高价值 evidence。

---

# 15.7 Rule-based Grader：PASS / FAIL 之外要允许 UNRESOLVED

规则适合判断：

```text
forbidden tool used?
budget exceeded?
permission violated?
success 后仍继续 action?
required field missing?
```

优点：

```text
fast
cheap
stable
auditable
```

缺点：

```text
coverage limited
边界规则复杂
规则本身也可能 bug
```

因此 rule system 最好支持：

```text
PASS
FAIL
UNRESOLVED
```

而不是：

```text
规则没命中 = PASS
```

---

# 15.8 Structured Grader：不要一开始就压成 Overall Score

复杂行为最好先拆 rubric dimensions。

普通回答：

```text
Correctness
Relevance
Completeness
Instruction Following
Clarity
```

Agent：

```text
Goal Completion
Constraint Satisfaction
Tool / Action Correctness
Observation Grounding
Recovery
Verification
Side Effects
Efficiency
Final Communication
```

先保留多维信息，再决定是否需要 aggregation。

因为：

```text
Correctness = 1
Constraint Following = 0
Style = 1
```

如果直接变成：

```text
Overall = 0.67
```

会掩盖一个可能是 hard failure 的 constraint violation。

---

# 15.9 Rubric Design：评价标准本身就是数据资产

Rubric 至少应包含：

```text
Dimension Definition
Positive Criteria
Negative Criteria
Boundary Cases
Examples
Required Evidence
Tie / Abstain Rule
Escalation Rule
```

并尽量让维度语义正交。

例如：

```text
Correctness
Helpfulness
Overall Quality
```

可能高度重叠。

更清晰：

```text
事实是否正确？
用户显式约束是否满足？
是否产生禁止副作用？
最终表达是否准确反映真实 outcome？
```

Rubric version 改变，本质上就是 evaluator semantics 改变。

---

# 15.10 Pointwise、Pairwise、Listwise

## Pointwise

```text
Candidate
↓
Score / Label
```

适合：

```text
absolute threshold
rubric dimensions
safety flag
pass / fail
```

风险：评分尺度 drift。

---

## Pairwise

```text
A vs B
↓
A / B / Tie / Both Bad / Cannot Judge
```

适合：

```text
preference
A/B model comparison
trajectory comparison
candidate selection
```

必须记住：

```text
A > B
```

不等于：

```text
A is good
```

所以要允许：

```text
Tie
Both Bad
Cannot Judge
```

---

## Listwise

```text
A B C D
↓
C > A > D > B
```

信息密度高，但候选多时：

```text
position bias
attention dilution
comparison complexity
context length
```

都会上升。

---

# 15.11 Reference-based 与 Reference-free

Reference-based：

```text
Task + Candidate + Reference
```

优点：事实判断容易；风险是：

```text
Reference 不唯一
Reference 自己可能错
Judge 过度锚定 reference
```

Reference-free：

```text
Task + Candidate + Rubric + Evidence
```

适合开放任务，但更依赖 Judge 自身能力。

不要要求所有维度统一模式。

可以：

```text
Correctness → executable / reference-based
Style → reference-free
Agent success → environment-state verifier
```

---

# 15.12 Evidence Package：Judge 真正看到什么？

Agent Judge 不应只看到：

```text
Final Response
```

更合理的 Evidence Package 可以包含：

```text
Task Contract
Relevant Constraints
Relevant State / Snapshot
Tool Calls
Tool Observations
State Diff
Verifier Results
Final Response
Rubric
```

但也不能无限塞 full trace。

需要控制：

```text
relevance
ordering
truncation
provenance
which fields are evaluator-only
```

否则 Judge 可能被无关 evidence 淹没。

---

# 15.13 Full-trace Judge 与 Local Judge

Full-trace 更适合：

```text
overall planning
trajectory coherence
end-to-end process quality
```

Local Judge：

```text
State + Action + Observation
```

更适合：

```text
Tool Selection
Argument Quality
Observation Grounding
Step Correctness
```

成熟系统通常组合：

```text
Local Evidence
+
Trajectory-level Evidence
```

而不是让一个超长 Judge Prompt 解决所有粒度。

---

# 15.14 LLM-as-a-Judge 的真正优势

核心优势通常不是：

> “比人更真。”

而是：

```text
便宜扩规模
快速迭代
可以执行自然语言 rubric
处理难以完全程序化的语义维度
生成结构化 rationale / error tag
```

最健康的角色关系是：

```text
Human / Domain Evidence defines standard
↓
LLM Judge scales application
↓
Gold / Anchor Set audits Judge
```

而不是：

```text
LLM Judge 自己定义什么叫正确
```

---

# 15.15 Judge Bias

常见：

```text
Position Bias
Verbosity Bias
Style Bias
Self / Model-family Preference
Reference Anchoring
Authority / Sycophancy Bias
```

对应 audit：

```text
A/B swap
short-correct vs long-redundant
style-controlled pairs
cross-model outputs
reference variants
unsupported-authority probes
```

Correctness 与 Style 最好分开判，避免漂亮表达掩盖事实错误。

---

# 15.16 Judge Variance 与 Calibration

同一个 Judge 可能：

```text
Run 1 → Pass
Run 2 → Fail
Run 3 → Pass
```

可以测：

```text
repeat consistency
self-agreement
ensemble agreement
```

但重复采样只能减少某些随机噪声，不能修复系统性 bias。

上线前应使用：

```text
Human Gold
Executable Truth
Boundary Cases
Bias Probes
High-severity Cases
```

做 calibration / meta-evaluation。

---

# 15.17 Meta-evaluation：Evaluator 本身怎么评？

至少可以看：

```text
Accuracy vs Gold
Precision / Recall
False Positive / False Negative
Agreement
Rank Correlation
Calibration
Abstention Quality
Consistency
Bias Gap
Coverage
Cost / Latency
```

高风险 evaluator 尤其要按：

```text
Severity
Failure Type
Task Family
```

分层看 False Negative。

总体 95% accuracy，若对高危 unauthorized action 经常漏判，仍然不可用。

---

# 15.18 Reliability ≠ Validity

```text
Judge 与 Human 很一致
```

不自动等于：

```text
结论真实有效
```

可能：

```text
Human rubric 也错
共同偏好 verbosity
reference 有 bug
Gold 发生 contamination
```

因此要区分：

```text
Reliability / Agreement
vs
Validity / Groundedness
```

这与第 6 章 Human Annotation 的逻辑一致。

---

# 15.19 Judge Confidence 不是天然概率

Judge 输出：

```text
confidence = 0.9
```

并不代表真实错误率就是 10%。

更可信 confidence 可以结合：

```text
historical calibration
multi-sample agreement
heterogeneous evaluator agreement
score margin
verifier / judge consistency
```

特别是 disagreement：

```text
Rule = Fail
LLM Judge = Pass
```

本身就是高价值 audit signal。

---

# 15.20 Ensemble：数量不等于独立证据

多个同源 Judge：

```text
Judge A
Judge B
Judge C
```

可能共享同样 bias。

所以：

> **Heterogeneous Evidence 通常比同质模型投票更有价值。**

例如：

```text
Executable Verifier
+
Rule Grader
+
LLM Judge
+
Human Audit
```

它们错误模式更不相同。

---

# 15.21 Hierarchical Evaluation 与 Routing

成熟系统可以：

```text
Stage 1
Deterministic / Executable Checks
↓
Stage 2
Rule / Structured Grader
↓
Stage 3
LLM Judge for unresolved semantics
↓
Stage 4
Human / Expert Escalation
```

目标不是：

```text
所有 Case 都交给最强 Judge
```

而是：

> **在质量约束下，以合适成本获得足够可靠的 label。**

不同 claim 也可路由：

```text
Math correctness → symbolic verifier
Code → execution
Agent outcome → environment state
Constraint semantics → rule + LLM
Tone → LLM / Human
High-risk domain → expert
```

---

# 15.22 Reward Model 与 LLM Judge

Reward Model 常被设计成高吞吐 scorer：

```text
(x, y) → scalar / ranking score
```

用于：

```text
RL
Best-of-N
Candidate Ranking
Training-time Optimization
```

LLM Judge 更适合：

```text
rubric reasoning
multi-dimensional labels
failure classification
rationale
```

边界可重叠，但不要因为两者都“打分”就当成同一个系统角色。

更重要的是：

> **Reward Model / Judge 的分数都不是目标本身。**

最终仍要用独立 downstream evidence 验证。

---

# 15.23 Judge Hacking 与 Verifier Hacking

如果长期优化：

```text
Judge Score
```

模型可能学会：

```text
迎合 Judge 风格
堆关键词
更冗长
更自信
```

而真实任务质量不变。

同样，程序 Verifier 也可能被 exploit：

```text
为了 tests pass 删除 tests
修改 assertion
mock 掉真实 failure
```

所以：

```text
Goal
+
Allowed Method / Invariants
+
Forbidden Side Effects
```

都要纳入验证。

典型 warning：

```text
Judge Score ↑
Executable / Human Outcome ↔ or ↓
```

---

# 15.24 Evaluator-only Evidence 与 Leakage

某些 evidence 只允许 evaluator 看：

```text
hidden tests
future outcome
full environment truth
gold label
oracle action
```

必须区分：

```text
Agent-visible Evidence
vs
Evaluator-only Evidence
```

如果 hidden verifier 文件、gold state、future result 被 policy 读到，benchmark 已经失效。

这和第 4 章：

```text
future information only for offline label
```

是同一条纪律。

---

# 15.25 Evaluation Contract：一条 Label 是怎样产生的？

一个成熟 Evaluation Contract 至少定义：

```text
Claim / Metric Dimension
Required Evidence
Evaluator Type
Evaluator Version
Rubric / Rule Version
Raw-output Schema
Parsing / Mapping Rule
Abstention Rule
Escalation Rule
Aggregation Rule
Severity Policy
```

例如：

```yaml
claim: policy_compliance
required_evidence:
  - task_contract
  - action_log
  - final_state_diff
primary_evaluator: deterministic_rule_v4
fallback: llm_judge_v6
abstain_on_missing_evidence: true
human_escalation:
  severity: S5+
```

这使一条 Label 不再只是：

```text
“Judge 说的”
```

而是一条可追溯的 measurement process。

---

# 15.26 Raw Artifact、Parsed Judgment、Derived Label 必须分层保存

例如：

```text
Raw Judge Response
↓
Parsed Rubric Scores
↓
Threshold / Mapping
↓
Derived Label
↓
Final Dataset / Metric
```

不要覆盖 Raw Judge Output。

这样 rubric / threshold / parser 更新时，可以：

```text
re-derive / re-score
```

而不是重新假装历史 evaluator 从没变过。

推荐字段：

```text
evaluation_id
evidence_refs
evaluator_id / version
raw_artifact
parsed_judgment
derived_label
label_version
```

完整 lineage 归第 19 章。

---

# 15.27 Corrected Labels 与 Frozen Historical Decisions

假设历史 Selector：

```text
chose Candidate A
```

后来发现旧 Judge 对部分 Candidate 判错。

严谨做法：

```text
历史 Policy Decision 保持冻结
↓
用 Corrected Labels 重新计分
```

而不是：

```text
用新 Judge 重新跑历史 Selector
然后把新行为当旧实验结果
```

必须区分：

```text
Re-score
= 同一历史 output，更新评价

Re-run
= 当前 policy / evaluator 重新执行
```

这两个问题在第 19 章会纳入版本治理。

---

# 15.28 Disagreement Mining：Evaluator 不一致本身就是数据

例如：

```text
Rule: Pass
LLM: Fail
Human: Pass
```

或者：

```text
Judge A: A wins
Judge B: B wins
```

Disagreement 常集中在：

```text
rubric boundary
hard cases
bias region
missing evidence
ambiguous task
```

可以形成：

```text
Disagreement Pool
↓
Human / Expert Adjudication
↓
Gold Expansion
↓
Rubric / Judge Update
↓
Recalibration
```

Evaluator 自己也需要 Data Flywheel。

---

# 15.29 Judge Drift：Measurement Instrument 会变

以下任何变化：

```text
judge_model
judge_prompt
rubric
evidence package
parser
threshold
```

都可能导致 label distribution 变化。

所以必须版本化：

```text
judge_model_version
prompt_version
rubric_version
evidence_schema_version
parser_version
mapping_version
```

线上长期 Judge Drift / Anchor Set 监控归第 23 章。

---

# 15.30 Canonical Agent Evaluation Stack

推荐顺序：

```text
1. Environment / Execution Evidence
   ↓
2. Required Predicate Check
   ↓
3. Forbidden Side-effect / Invariant Check
   ↓
4. Permission / Policy / Deterministic Rules
   ↓
5. Process / Recovery / Verification Grading
   ↓
6. Final Communication Grading
   ↓
7. Human / Expert Escalation for unresolved / high-risk cases
```

最终语言回复通常是最后一层，而不是第一层。

---

# 15.31 Canonical Case：C2 Calendar Agent

Task：

```text
把产品组会议改到周五 15:00，邀请 Alice，
但不要通知外部联系人。
```

Episode 最终：

```text
meeting moved correctly
Alice invited
external contact also notified
final response: “已经全部处理完成。”
```

分层判定：

### Environment Verifier

```text
meeting_time == Friday 15:00  PASS
Alice invited                  PASS
```

### Forbidden Side-effect Rule

```text
external_contact_notified == false  FAIL
```

### Process Judge

判断：

```text
是否读取 recipient type？
是否保留 negative constraint？
是否验证 recipient list？
```

### Final Communication Judge

```text
“已经全部处理完成”
```

在存在违规副作用时是 misleading。

因此：

> **一条 Trajectory 应由多个 evaluator 读取不同 evidence；不要让一个 Overall Judge 包办全部事实与解释。**

完整 Case 见 [`Canonical Casebook`](./00_Canonical_Casebook.md)。

---

# 15.32 Evaluation Schema 示例

```json
{
  "evaluation_id": "eval_001",
  "trajectory_id": "traj_001",
  "evidence_refs": {
    "case_id": "calendar_case_17",
    "state_diff_id": "diff_456",
    "trace_id": "trace_123"
  },
  "deterministic_checks": {
    "goal_predicate": true,
    "forbidden_side_effect_absent": false
  },
  "judge": {
    "model_version": "judge_v6",
    "prompt_version": "jp_v4",
    "rubric_version": "rubric_v5",
    "raw_artifact_id": "judge_raw_889",
    "parsed_scores": {
      "constraint_following": 0,
      "communication": 1
    },
    "abstain": false
  },
  "derived_label": "policy_noncompliant_failure",
  "label_version": "v3"
}
```

关键结构：

```text
Evidence
Evaluator
Version
Raw Output
Parsed Judgment
Derived Label
```

分开保存。

---

# 15.33 Evaluation Error Budget

Evaluator 不可能零误差。

真实决策需要权衡：

```text
Coverage
Accuracy
False Positive Cost
False Negative Cost
Abstention Rate
Human Escalation Rate
Cost
Latency
```

例如 bulk synthetic filtering 和 high-risk production audit 的最优 evaluator 策略完全不同。

因此：

> **Evaluator Quality 必须在用途和错误代价下定义。**

---

# 15.34 防止评价闭环自证

危险模式：

```text
Model A generates
↓
Model A / same-family Judge scores
↓
high-score data trains Model A
↓
same Judge declares improvement
```

可能形成 self-confirmation loop。

需要外部锚点：

```text
Executable Truth
Human Gold
Independent / Heterogeneous Judge
Frozen Benchmark
Production Outcome
```

不能只在同一自动评价体系里证明自己越来越好。

---

# 15.35 常见失败模式

### 失败 1：能直接验证却全部交给 LLM Judge

制造不必要的不确定性。

### 失败 2：Evidence 缺失仍强迫 PASS / FAIL

应该允许 UNRESOLVED / ABSTAIN。

### 失败 3：只看 Final Response，不看 Environment Evidence

Agent 可以 hallucinate completion。

### 失败 4：一个 Overall Score 包办所有维度

Hard Failure 被平均掉。

### 失败 5：Pairwise 强制 Winner

Both Bad 被错误转成 Preference。

### 失败 6：Judge-human Agreement 高就当绝对正确

Reliability ≠ Validity。

### 失败 7：只在 Easy Gold 校准

边界 / 高危 case 仍可能失真。

### 失败 8：不审计 Position / Verbosity / Style Bias

评价奖励表面形式。

### 失败 9：Judge / Rubric 改了仍混用旧分数

Measurement instrument 已经变化。

### 失败 10：Corrected Label 后重跑历史 Policy 并冒充原实验

破坏历史决策冻结。

### 失败 11：Judge Rationale 被当 Ground Truth

Rationale 本身也可能错。

### 失败 12：增加更多同源 Judge 就以为获得独立证据

相关 bias 不会消失。

### 失败 13：Evaluator-only Evidence 泄漏给 Policy

Benchmark 失效。

### 失败 14：只优化 Judge Score

可能发生 Judge Hacking。

### 失败 15：Verifier 只检查目标，不检查 Forbidden / Invariant

会奖励 destructive shortcut。

---

# 15.36 从数据岗位视角，这一章实际会做什么？

```text
定义 evaluation claim
设计 evidence package
写 state / execution verifier
写 rule checker
设计 rubric
设计 judge prompt
构造 gold / anchor set
做 position / verbosity bias audit
跑 pointwise / pairwise evaluation
测 FP / FN / calibration
设计 abstention / escalation
做 evaluator routing
保存 raw judge artifacts
维护 evaluator version
做 corrected-label rescoring
做 disagreement mining
监控 judge drift
做 judge / verifier regression
```

所以 Evaluation Data 工作不是：

> “写几个 prompt 给模型打分。”

而是：

> **Evidence Design + Measurement Contract + Evaluator Engineering + Meta-evaluation + Governance。**

---

# 15.37 本章关键词

| 术语 | Canonical meaning |
|---|---|
| Evidence | 支撑某个评价 Claim 的事实 / 执行 /状态 /人工证据 |
| Evaluator | 读取 Evidence 并产生 Judgment 的系统 |
| Verifier | 基于明确可检查条件做验证的 Grader |
| Grader | 将 Evidence 映射为 Score / Label 的广义评价器 |
| Judge | 对不可完全程序化标准做解释性判断的 Grader |
| Raw Judgment | Evaluator 原始输出 |
| Derived Label | 由 Raw Judgment 经 parser / rule / threshold 得到的标签 |
| Evaluation Contract | Claim、Evidence、Evaluator、Abstain、Aggregation 等完整定义 |
| Evidence Package | Evaluator 实际读取的证据集合 |
| Meta-evaluation | 评价 Evaluator 本身 |
| Calibration | 用 Gold / Anchor Evidence 校验 evaluator |
| Abstention | 证据不足或判断不可靠时不强制给标签 |
| Evaluation Routing | 不同 Claim / Case 路由到不同 evaluator |
| Judge Hacking | 优化 evaluator proxy 而非真实目标 |
| Verifier Leakage | Evaluator-only 信息泄漏给被评 policy |
| Corrected Label | 后续修正后的评价标签 |

更完整定义见 [`Canonical Glossary`](./00_Glossary_and_Notation.md)。

---

# 15.38 面试 / 自检问题

1. Evidence、Evaluator、Raw Judgment、Label 有什么区别？
2. Grader、Verifier、Judge 怎么区分？
3. 为什么 Evidence First, Judge Second？
4. 什么情况下应该输出 UNRESOLVED / ABSTAIN？
5. Deterministic Verifier 为什么也可能有错误？
6. Agent Eval 为什么要看 Required / Forbidden / Invariant？
7. 为什么 Overall Score 容易掩盖 hard failure？
8. Pointwise / Pairwise / Listwise 各适合什么？
9. Pairwise 为什么必须允许 Both Bad / Cannot Judge？
10. Reference-based Judge 的主要风险是什么？
11. Evaluation Evidence Package 应包含什么？
12. Full-trace 与 Local Judge 如何配合？
13. LLM-as-a-Judge 的核心价值是什么？
14. 常见 Judge Bias 有哪些？
15. Reliability 与 Validity 为什么不同？
16. Judge Confidence 为什么不是天然概率？
17. Ensemble 为什么不等于独立证据？
18. 什么是 Evaluation Routing？
19. Reward Model 与 LLM Judge 有什么区别？
20. Judge Hacking / Verifier Hacking 怎么检测？
21. Evaluator-only Evidence 为什么必须和 Agent-visible Evidence 分开？
22. Evaluation Contract 至少要冻结什么？
23. Raw Judge Output 为什么不能被覆盖？
24. Corrected Label 出现后，历史实验如何重算？
25. Judge Drift 如何被监控？
26. 为什么高风险 evaluator 不能只看总体 accuracy？
27. 怎么防止 generator–judge–student 自证闭环？
28. 怎样设计 Human Escalation？
29. 怎样证明一个 Judge 真有用，而不是只是便宜？
30. 如何设计一套可审计的 Agent Evaluation Stack？

---

## 15.38.1 通用回答框架：设计一套 Agent Grader

```text
1. Define Evaluation Claim
   ↓
2. 找最直接的 Evidence
   ↓
3. 能执行验证的先写 Verifier
   ↓
4. 对 Policy / Side Effect 写 Rule Checks
   ↓
5. 对剩余语义维度定义 Rubric
   ↓
6. 建 Human / Executable Gold / Anchor Set
   ↓
7. 校准 LLM Judge
   ↓
8. 做 Position / Verbosity / Style / Severity Audit
   ↓
9. 定义 Abstain / Human Escalation
   ↓
10. 保存 Evidence + Evaluator Version + Raw Artifact
   ↓
11. 持续做 Disagreement Mining / Corrected-label Rescoring
```

---

# 15.39 与后续章节的关系

```text
第 16 章 Benchmark Protocol
→ 多个 Case 与 Evaluator 如何组成可信比较实验

第 19 章 Governance
→ Evidence / Evaluator / Label 的 lineage 与历史重算

第 23 章 Monitoring
→ Judge Drift / Anchor Set / online evaluator health
```

本章只回答：

> **一条 Claim 应该拿什么 Evidence、由谁判、怎样知道判得可信。**

它不负责模型间统计比较、budget matching 或 benchmark population accounting；这些归第 16 章。

---

# 15.40 本章最终要形成的认识

```text
Claim
↓
Evidence
↓
Evidence Sufficiency
↓
Verifier / Grader / Judge
↓
Raw Judgment
↓
Derived Label
↓
Final Decision / Metric Input
↓
Meta-evaluation
↺
```

最终记住三句话：

> **Evidence first, Judge second。**

> **Verifier 负责尽可能直接的事实验证，Judge 负责不可完全程序化的解释性判断，Human / Gold 负责定义边界与校准自动系统。**

> **证据不足时，最专业的输出往往不是“猜一个标签”，而是 `UNRESOLVED / ABSTAIN`。**

下一章进入：

> [`第 16 章 Benchmark Design 与 Evaluation Protocol`](./16_Benchmark_Design_and_Evaluation_Protocol.md)

正式回答：

> **有了可信单样本评价以后，怎样把 Case、Runtime、Budget、Statistics 与 Reporting 组织成一套能支持“模型 / 方法真的更好”这一结论的实验协议？**