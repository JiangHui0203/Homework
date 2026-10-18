# LLM / Agent Data Scenario Extension Promotion Test

> 状态：`Scenario Validation / Promotion Gate`
>
> 前置：[`Round 2 Stress Test`](./00_Scenario_Pack_Stress_Test_Round_2.md) · [`Candidate Extensions`](./00_Scenario_Pack_Candidate_Extensions.md)
>
> 目的：用另外两类工作检查 E1–E4 是否真的跨场景稳定，并决定：**Promote / Keep Optional / Reject / Revise**。

测试对象：

```text
H — Human Gold / Annotation Refresh
S — Synthetic Data Production at Scale
```

---

# 1. Promotion Rule

不是“又有一个案例能套上”就 promote。

至少检查：

```text
1. 是否跨不同对象仍解决同一种 ambiguity？
2. 是否与已有 A1–A11 ownership 冲突？
3. 是否只在少数项目相关？
4. 能否以 optional extension 存在？
5. 不加它是否会造成真实 audit / decision failure？
```

决策含义：

```text
PROMOTE_CORE
→ 应进入 Starter Pack 的通用路由 /原则

PROMOTE_OPTIONAL
→ 稳定有用，但只对特定项目填写

KEEP_CANDIDATE
→ 有价值，但证据还不足

REJECT
→ 过拟合 / 与已有资产重复
```

---

# 2. Test H — Human Gold / Annotation Refresh

## 2.1 Scenario

已有一个长期评测 / 标注项目：

```text
Guideline v3
Gold Set G3
Annotator Pool A3
```

最近出现：

```text
Judge-Human disagreement ↑
Boundary-case adjudication ↑
New product rule
```

团队准备升级：

```text
Guideline v3 → v4
Gold G3 → G4
```

问题不是单纯：

```text
“再标一批数据”
```

而是：

> 新旧 label semantics 是否仍可比较？旧 benchmark / dataset / release decision 应怎样保留？

---

## 2.2 E1 Entry Router Test

它不是典型 model failure，也不是纯 production incident。

自然入口是：

```text
Evaluation-led
↓
A5 Evaluator / Label Contract
↓
Guideline / Gold evidence
↓
Measurement Bridge
↓
re-annotation / adjudication
↓
A7 impact comparison
↓
A8 decision
```

说明 E1 能处理：

```text
Human Annotation
```

而不只是：

```text
K17 / Agent Incident / Curation
```

### Verdict E1

```text
PROMOTE_CORE
```

理由：不同项目确实需要不同入口；强迫所有项目从 A1→A10 顺序走，会制造假 Root Cause 或无意义 N/A。

应该进入通用 Starter Pack 的，是：

> **Entry Router principle**

而不是把所有具体分支字段都塞进主模板。

---

## 2.3 E3 Measurement Bridge Test

Guideline v4 改变：

```text
label definition
priority rule
abstain rule
boundary examples
```

即使 annotator 没变，measurement object 也变了。

因此应该在同一 anchor subset 上：

```text
v3 guideline labeling
vs
v4 guideline labeling
```

比较：

```text
agreement shift
decision flip rate
abstention shift
Gold mismatch
slice-specific changes
adjudication rate
```

这和：

```text
Judge J4 → J5
```

本质同构。

### Verdict E3

```text
PROMOTE_OPTIONAL
```

E3 不应该让所有 A5 都变长；但只要 evaluator / guideline / rubric / verifier 发生 version change，就应该强制填写 Measurement Bridge。

它已经跨：

```text
LLM Judge
Verifier
Human Guideline
Gold Refresh
```

证明不是某个 case 的特例。

---

## 2.4 New Finding H1 — Human Annotation 仍缺一个执行 Contract

A5 能说明：

```text
凭什么判
```

但不能完整说明：

```text
谁来判
怎么训练 annotator
怎样 qualification
怎样 hidden QC
怎样 adjudication
```

现有 Ch6 已经有完整理论，但 Practical Artifact Kit 还缺一个按需执行挂件。

因此新增 candidate：

```text
E5 A5-H Human Annotation / Gold Contract
```

建议最小字段：

```yaml
annotation_contract_id: <id>
label_schema_version: <version>
guideline_version: <version>

evidence_required:
  - <evidence type>

annotator_roles:
  general: <allowed task|null>
  trained: <allowed task|null>
  expert: <allowed task|null>
  adjudicator: <allowed task|null>

qualification:
  training_set: <id>
  gold_set: <id>
  pass_rule: <rule>

production_qc:
  hidden_gold_rate: <value>
  random_audit_rate: <value>
  agreement_metric: <metric>
  abstain_allowed: true

escalation:
  disagreement: <route>
  low_confidence: <route>
  need_expert: <route>
  high_severity: <route>

adjudication:
  policy: <rule>
  final_label_version: <version>
  guideline_update_required: <condition>

outputs:
  raw_labels: <view>
  adjudicated_labels: <view>
  gold_updates: <view>
  boundary_examples: <view>
```

固定边界：

```text
Human Label
≠ Ground Truth by identity

High Agreement
≠ High Validity

Majority Vote
≠ Adjudication

Corrected Label
≠ Historical Decision Rewrite
```

### Verdict E5

```text
KEEP_CANDIDATE
```

需要再经过一个真实 annotation / expert-labeling workflow 后再决定是否 promote optional。

---

# 3. Test S — Synthetic Data Production at Scale

## 3.1 Scenario

目标：围绕某个 capability gap 生产：

```text
1,000,000 synthetic candidate experiences
```

流程：

```text
Seeds
→ Generator / Teacher / Simulator
→ Candidate Experience
→ Verifier / Judge / Human Audit
→ Routing / Curation
→ Dataset Views
```

风险包括：

```text
teacher bias
low task diversity
family leakage
verifier drift
duplicate decision patterns
low high-value yield
cost explosion
```

---

## 3.2 Does E1 Help?

这个项目可以是：

```text
Hypothesis-led
```

如果从 capability gap 出发；也可以是：

```text
Asset / Production-led
```

如果已经有 seeds / source pool，只需要规模生产。

E1 仍然成立：

```text
origin 不同
→ entry artifact 不同
→ 后面汇到 controlled change / evaluation / decision
```

再次支持：

```text
E1 = PROMOTE_CORE
```

---

## 3.3 Do We Need a New Synthetic Artifact?

现有资产组合已经可以表达：

```text
A6
→ capability gap / hypothesis
→ source experience
→ construction policy
→ verification policy
→ curation / mixture

A9
→ production objective
→ target volume
→ quality gate
→ job / retry / artifact / routing / cost contract

A11
→ source / derived lineage

A7
→ downstream matched-budget validation
```

也就是说，Synthetic Production 的核心问题能由：

```text
A6 + A9 + A11 + A7
```

覆盖。

### Finding S1

> **不是每一个重要领域都需要一个新 Artifact。已有 contract 的组合如果能保持 ownership 清楚，应优先组合，不要新建 `A12 Synthetic Card`。**

这是一条很重要的“反膨胀”证据。

---

## 3.4 E4 Curation Contract Test

1M candidates 生产后，E4 对以下问题依然有用：

```text
source lineage
family grouping
decision-level dedup
routing
yield funnel
mixture / exposure
dataset build recipe
```

但它只负责：

```text
Candidate Experience
→ Dataset View
```

不负责：

```text
Generator / Teacher / Simulator 的完整生产协议
```

后者已经由 A6 + A9 负责。

### Verdict E4

```text
PROMOTE_OPTIONAL
```

理由：E4 在 raw trajectory curation 和 synthetic candidate curation 中都反复出现，而且 ownership 清楚；但不是所有项目都需要，所以不进入 A6 主体字段。

应该把它定位成：

```text
A6-C optional curation extension
```

而不是新的 canonical artifact number。

---

## 3.5 E3 in Synthetic Production

如果生产跑到一半：

```text
Verifier V3 → V4
```

而没有 bridge，就会出现：

```text
前 400k candidate
按 V3 acceptance policy

后 600k candidate
按 V4 acceptance policy
```

最后混成一个 dataset view。

此时：

```text
source distribution
+
evaluator policy
```

同时变化。

所以至少应该：

```text
version-split build
or
paired bridge + explicit rebuild
```

这再次验证 E3 是跨 evaluator 类型和 data pipeline 的稳定 optional extension。

---

# 4. Promotion Matrix

| Extension | Production Incident | Judge Drift | Curation | Human Gold | Synthetic Production | Verdict |
|---|---:|---:|---:|---:|---:|---|
| E1 Entry Router | ✓ | ✓ | ✓ | ✓ | ✓ | **PROMOTE_CORE** |
| E2 A10-I Incident | ✓ | — | — | — | — | **KEEP OPTIONAL / scenario-specific** |
| E3 A5-M Measurement Bridge | △ | ✓ | △ | ✓ | ✓ when evaluator changes | **PROMOTE_OPTIONAL** |
| E4 A6-C Curation Contract | — | △ | ✓ | △ | ✓ | **PROMOTE_OPTIONAL** |
| E5 A5-H Human Annotation Contract | — | △ | △ | ✓ | △ human-audit stage | **KEEP_CANDIDATE** |

说明：

```text
✓ = directly exercised
△ = relevant interface, not primary focus
— = not materially relevant
```

---

# 5. What This Tells Us About the Mother Framework

经过三轮不同压力：

```text
Interview Follow-up
Selective Reasoning
Production Incident
Evaluator Drift
Trajectory Curation
Human Gold Refresh
Synthetic Production
```

真正稳定的不是一个固定流程图，而是五件事：

```text
1. Entry depends on problem origin.
2. Every important object has identity + version + evidence.
3. Controlled change must preserve comparison boundaries.
4. Result and decision are separate artifacts / reasoning steps.
5. Monitoring / new evidence can reopen the loop without rewriting history.
```

所以最终结构更准确地应该理解为：

```text
                 ┌─ Failure-led
                 ├─ Monitoring-led
Entry Router ────┼─ Hypothesis-led
                 ├─ Evaluation-led
                 └─ Asset-led
                        ↓
              Contracts + Evidence
                        ↓
                Controlled Change
                        ↓
                    Evaluation
                        ↓
                     Decision
                        ↓
               Monitoring / Re-entry
```

而不是：

```text
A1 → A2 → A3 → ... → A10
```

---

# 6. Promotion Decision

本轮建议真正回写 Mother Edition 的只有一条：

```text
E1 Entry Router
→ Promote to Starter Pack core principle
```

而：

```text
E2 Incident
E3 Measurement Bridge
E4 Curation
```

应保持：

```text
optional extension
```

因为它们很稳定，但只对特定 project type 有意义。

E5 继续观察。

这个决策体现一个重要原则：

> **成熟模板不是把所有已知最佳实践都塞进主表，而是让 core 足够小，让 extension 足够准。**
