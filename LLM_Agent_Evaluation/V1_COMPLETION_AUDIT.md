# LLM / Agent Evaluation Knowledge System — V1 Completion Audit

- Audit date: 2026-10-30
- Audited repository: `JiangHui0203/Homework`
- Audited pre-audit head: `a4d5cf9da7e10f2f62ca821d6fd6b180ad48ebc6`
- Scope: `LLM_Agent_Evaluation/`
- Verdict: **V1 Release Candidate — conditional pass, not yet V1 Complete**

> 这次审计的目标不是继续扩内容，而是回答：当前知识系统是否已经形成可冻结的 V1；如果没有，真正的 blocker 是什么；V1 之后应该停止“建库”并进入怎样的 mastery 阶段。

## 1. Executive verdict

当前仓库已经不是 `V0 Architecture / Skeleton`。

主干已经形成完整的 Evaluation learning system：

```text
Evaluation Contract
→ Evaluator / Judge
→ Agent Evaluation
→ Trajectory / Failure
→ Benchmark
→ Statistics
→ Eval Engineering
→ Eval → Data / Post-training
→ Frozen real case
```

截至本次审计：

```text
CORE questions             37
formal question docs       35 / 37 = 94.6%
M1 questions               28
M1 with formal docs        28 / 28 = 100%
Labs                       L01–L08 = 8 / 8
real frozen capstone       1
stable Patterns            P01–P12
VeriAgent architecture     Stable + Frozen populated; Current empty
mastery state              unchanged; all questions remain S0
```

因此当前最准确的状态是：

> **V1 Release Candidate：核心方法已闭合，剩余问题是 release closeout，而不是继续扩展主干。**

## 2. V1 release blockers

V1 不应现在直接标记 `Complete`。剩余 blocker 只有三项，而且都很明确。

### B1 — Q05 缺正式正文

`CORE_QUESTIONS.md` 已定义：

```text
Q05 reference-based 与 reference-free evaluation 各适合什么任务？
```

但 Part 1 目前只有 Q01 / Q03 / Q04，Q05 仍只是未链接条目。

建议正式 owner：

```text
01_LLM_Evaluation/04_Reference_Based_and_Reference_Free_Evaluation.md
```

完成标准不是写 automatic-metric 百科，而是能回答：

```text
什么情况下可靠 reference 存在？
什么情况下 reference-free 更合理？
reference-free evaluator 的 validity 从哪里来？
多 valid outputs 如何处理？
什么时候 deterministic/executable evidence 仍应优先？
```

Priority: **P0 / V1 blocker**.

### B2 — Q06 缺正式正文

`CORE_QUESTIONS.md` 已定义：

```text
Q06 开放式生成为什么很难只靠一个 automatic metric 评价？
```

但没有正式 Part 1 文档。

建议 owner：

```text
01_LLM_Evaluation/05_Open_Ended_Generation_Evaluation.md
```

建议聚焦：

```text
multi-dimensional quality
multiple valid answers
surface similarity vs semantic quality
automatic metric blind spots
human / Judge / deterministic evidence combination
slice + rubric + uncertainty
```

Priority: **P0 / V1 blocker**.

### B3 — VeriAgent Current Case 层为空

本库明确声明三层结构：

```text
Stable Theory
Current Case
Frozen Experiment
```

现在：

```text
Stable Theory   已大量建立
Frozen          已有 L08 对应真实实验
Current         只有 cases/veriagent/current/README.md 规则，没有 actual case
```

这不是理论缺口，但它意味着三层架构还没有真正全部运行起来。

建议 V1 至少建立一个 current case：

```text
cases/veriagent/current/01_olist_evaluation_architecture.md
```

内容只维护：

```text
last_reviewed
current VeriAgent commit
stable principle
repo/file pointers
current behavior
trace / artifact fields
current metrics / evidence entry
known limitations
drift conditions
```

写之前必须重新读取当时 VeriAgent `main`，不能从 L08 frozen commit 反推“当前实现”。

Priority: **P0 / V1 architecture blocker**.

## 3. Core Questions completeness

### 3.1 M1 coverage

结论：**28 / 28 M1 已正式落地。**

M1 已覆盖：

```text
Q01–Q04 中的 M1
Q07–Q10
Q12–Q15
Q17–Q19
Q21–Q23
Q25–Q28
Q31–Q36 中的 M1
```

这意味着当前仓库已经具备完整的核心 Eval spine，不存在“最关键的问题还没有正文”的情况。

### 3.2 M2 coverage

M2 共 9 个：

```text
Q05 Q06 Q11 Q16 Q20 Q24 Q29 Q30 Q37
```

其中：

```text
formalized: Q11 Q16 Q20 Q24 Q29 Q30 Q37 = 7
missing:    Q05 Q06 = 2
```

因此整体 formal coverage：

```text
35 / 37 = 94.6%
```

### 3.3 Mastery is not content completeness

当前 `CORE_QUESTIONS.md` 中所有题仍是：

```text
S0
```

这是正确状态。

```text
document authored
≠ user independently learned it
≠ S2

Lab exists
≠ user independently completed it
≠ S3

reference answer exists
≠ user can defend it
≠ S4
```

本审计不修改任何 mastery level。

## 4. Lab / practice completeness

已建立：

```text
L01 Metric Design
L02 Judge Calibration
L03 Paired Evaluation
L04 Trajectory Failure Analysis
L05 Agent Recovery Evaluation
L06 Benchmark Slice Design
L07 Eval Harness
L08 VeriAgent Frozen Case
```

### M1 → Practice coverage

当前学习路径已经提供：

```text
Q01–Q04  → L01
Q07–Q11  → L02
Q12–Q20  → L04 + L05
Q21–Q24  → L06
Q25–Q29  → L03
Q31–Q34  → L07
Q35–Q37  → L08 real case
Q01–Q37  → L08 capstone integration
```

结论：**所有 M1 都有 Lab 或真实项目证据入口。**

因此 V1 之后不建议继续创建 `L09` 只是为了扩数量。

## 5. Source of Truth / ownership audit

`SOURCE_OF_TRUTH.md` 当前边界总体健康。

### `LLM_Agent_Data` owns

```text
Data objects / learning signals
Agent trajectory anatomy canonical concepts
complete Agent failure taxonomy
Grader / Judge data-system perspective
Benchmark basics
Data flywheel / governance / data experiments
preference / reward / post-training data construction
```

### `LLM_Agent_Evaluation` owns

```text
Evaluation contract / estimand / metric design
Judge reliability / calibration
Agent evaluation methodology
Trajectory measurement / diagnosis
Applied Eval statistics
Benchmark measurement semantics / leakage / portfolio
Eval harness / replay / CI gates
Eval-side promotion / validation interface to Data
```

### `veriagent` owns

```text
source code
current runtime behavior
raw traces / experiment outputs
```

### Evaluation frozen case owns

```text
historical experiment interpretation
bound to commit / protocol / evidence / limitation
```

No hard canonical-owner conflict was found.

## 6. Duplication audit

当前重复主要是**有意的“Teaching Doc + Working Registry”双层结构**，不是互相争定义权。

### Healthy overlap

```text
Q04 + METRICS.md
Q20 + FAILURE_TAXONOMY.md
Q21–Q24 + BENCHMARKS.md
Q25–Q34 + METRICS.md statistical/engineering rules
```

其职责分别是：

```text
Question doc
= teach / explain / interview / counterexample

Registry
= operational lookup / contract / maintenance rules
```

不建议为了去重而合并。

### Duplication watchlist — Part 8

Q35–Q37 目前仍然守住了边界：

```text
Eval evidence
→ promotion / validation / supervision gate
```

而不是重新讲一套完整 data/post-training pipeline。

但 Part 8 是未来最容易发生重复建设的位置。

固定维护原则：

> 具体 acquisition、data construction、mixture、preference format、training protocol、governance 继续交给 `LLM_Agent_Data`；Evaluation 只保留 evidence qualification、independent re-evaluation 和 claim boundary。

### P1 consistency debt

对与 Data 高重叠的正文，可以逐步统一增加：

```text
Canonical owner
Evaluation-specific angle
```

尤其 Q18、Q21–Q24、Q35–Q37。

这不是 V1 blocker。

## 7. Link / navigation audit

本轮检查了 V1 主要导航图：

```text
root README
→ CORE / PATTERNS / METRICS / BENCHMARKS / FAILURE / INTERVIEW / SOT
→ Part 0–8
→ labs
→ cases/veriagent
→ current / frozen
→ L08 canonical frozen case
```

结果：**未发现已检查导航中的 broken file target。**

`CORE_QUESTIONS.md` 中 35 个已有链接的问题均有对应 formal file；Q05/Q06 没有链接的原因是正文尚不存在，属于 content gap，不是失效链接。

### Audit limitation

本轮没有在本地 clone 上完成“遍历所有 Markdown 的所有相对路径 + heading anchor”的自动化 crawler，因为当前执行环境不能直接通过网络 clone GitHub 仓库。

因此正确声明是：

```text
V1 navigation / file-target audit: PASS for inspected graph
exhaustive deep-anchor crawler: not yet implemented
```

建议未来作为 P1 Eval Engineering dogfooding：

```text
scripts / CI link audit
```

但不作为内容 V1 blocker。

## 8. Foundations audit

Part 0 计划了 7 个最小基础：

```text
1 Probability & Statistics        已建立
2 Machine Learning Basics         未建立
3 LLM Fundamentals                未建立
4 Experiment Design               已建立
5 Data Handling                   未建立
6 Agent Fundamentals              已建立
7 Software Engineering            未建立
```

表面完成度是：

```text
3 / 7
```

但这**不应被当作 V1 blocker**。

Part 0 自己的纳入标准就是：只有基础缺口会真实阻塞 Eval 时才 reverse-fill，避免重新写完整 CS/ML 教材。

因此 V1 之后采用 mastery-triggered reverse fill：

```text
Q25/Q27 卡住
→ Probability / Statistics

Q03/Q07/Q30 卡住
→ ML / LLM Fundamentals

Q31/Q32 卡住
→ Data Handling / Software Engineering

Q12–Q16 卡住
→ Agent Fundamentals
```

不要为了目录数字从 3/7 变成 7/7 而提前扩写。

## 9. Patterns audit

当前稳定 Patterns：

```text
P01 Eval Contract First
P02 Deterministic First, Judge Last
P03 Paired Same-Task Comparison
P04 Slice Before Aggregate
P05 Frozen Core + Rotating Hard Set
P06 Trajectory First-Failure Analysis
P07 Recovery-aware Evaluation
P08 Judge Calibration Before Scale
P09 Cost per Valid Success
P10 Replayable Evaluation
P11 Holdout after Development
P12 Mechanism ≠ Outcome
```

这些 Pattern 已经广泛被 Question / Lab 使用。

当前 `EVAL_PATTERNS.md` 更像 registry，而不是 12 篇完整 Pattern Card。这是合理的 V1 形态。

建议下一阶段优先补一个：

```text
Pattern → Core Questions → Labs / Cases
```

crosswalk，而不是马上把 12 个 Pattern 各扩成长文。

Priority: **P1, non-blocking**.

## 10. Version / status debt

根 `README.md` 在审计前仍写：

```text
V0 Architecture / Skeleton
```

这已经与仓库事实不符。

本审计将根状态更新为：

```text
V1 Release Candidate
```

但现在还不应改成 `V1 Complete`。

此外这些局部标签仍存在：

```text
CORE_QUESTIONS.md   V0 Master List
EVAL_PATTERNS.md    V0 Pattern Registry
INTERVIEW_INDEX.md  V0 高频入口
FAILURE_TAXONOMY.md V0 诊断维度
```

它们可能表示局部 registry version，不一定是错误；V1 closeout 时应统一决定：

```text
bump to V1
or
remove version label and keep registry versionless
```

Priority: **P0 closeout housekeeping after B1–B3**.

## 11. Structural items that should NOT be “fixed” now

### Part 7 starts at `02_...`

这是 cosmetic naming debt，不影响语义和导航。

不要为了编号美观重命名，避免制造大量 link churn。

### Foundation numbering has gaps

这是计划中的 deferred topic，不需要为了连续编号补空文档。

### More frozen cases

L08 已经足够证明 frozen architecture 可用；更多 frozen case 属于真实项目自然增长，不属于 V1 blocker。

## 12. V1 closeout order

在进入大规模 mastery audit 前，先完成一个很短的 closeout sprint：

```text
Step 1  Q05 formal doc
Step 2  Q06 formal doc
Step 3  first VeriAgent Current Case
Step 4  normalize V0/V1 registry labels
Step 5  final navigation acceptance
Step 6  mark V1 Complete and freeze a release snapshot
```

完成后停止继续增加 broad theory chapters，除非真实 mastery / project work 暴露新缺口。

## 13. Post-V1 learning sequence

下一阶段的目标不是“继续写”，而是：

> **把已有知识转成闭卷解释、独立设计、实际分析和追问 defend 能力。**

### Wave 1 — Measurement spine

```text
Q01 Q02 Q03 Q04 Q25 Q26 Q27 Q28
```

训练链：

```text
claim
→ estimand / unit
→ metric / denominator
→ paired design
→ uncertainty
→ task vs repeat
→ credible evidence statement
```

优先级最高，因为后面所有“提升可信吗”都依赖它。

### Wave 2 — Evaluator reliability

```text
Q07 Q08 Q09 Q10 Q11 Q30
```

使用 L02。

目标：能清楚处理 deterministic verifier、Judge reliability、bias、rubric、human disagreement 与 replacement boundary。

### Wave 3 — Agent process & failure

```text
Q12–Q20
```

使用 L04 / L05 / L08。

目标：

```text
final success insufficient
→ tool / state / recovery
→ first meaningful failure
→ evidence level
→ operational taxonomy
→ intervention owner
```

### Wave 4 — Benchmark & experimental discipline

```text
Q21 Q22 Q23 Q24 Q29
```

使用 L06 / L03。

重点：

```text
discriminative set
leakage / test overfit
frozen / regression / hard / fresh
sampling semantics
multiple comparisons
```

### Wave 5 — Eval Engineering

```text
Q31 Q32 Q33 Q34
```

使用 L07。

目标：artifact provenance、replay、fault injection、CI gate、flakiness、多维 release decision。

### Wave 6 — Eval → Data

```text
Q35 Q36 Q37
```

使用 L08。

目标：failure promotion、fresh confirmation、evaluator signal promotion、Goodhart / reward hacking control。

## 14. Mastery audit protocol

每个题不要靠“看过文档”升级。

建议闭卷考核：

```text
1. 60–90 秒核心回答
2. 5 分钟 evaluation design expansion
3. 至少一个 counterexample / failure mode
4. 一个真实或 VeriAgent example
5. 一轮 adversarial follow-up / trade-off defense
```

升级建议：

```text
S1: 能识别问题和术语
S2: 脱离笔记解释核心逻辑
S3: 独立设计 / 实现 / 分析
S4: 能诊断反例、比较方案并 defend
```

### First target

先让所有 M1 到：

```text
S3
```

再把下面的 interview spine 推到 S4：

```text
Q01 Q02 Q04
Q07 Q08
Q12
Q17
Q21 Q22
Q25 Q26
Q31 Q34
Q35 Q36
```

M2 第一阶段达到 S2 / S3 即可，不必平均追求 S4。

## 15. Release acceptance checklist

V1 Complete 前必须全部满足：

```text
[ ] Q05 formalized and linked
[ ] Q06 formalized and linked
[ ] at least one VeriAgent Current Case exists
[ ] root status no longer says V0 Skeleton
[ ] registry version labels normalized
[ ] main navigation/file-target check rerun
[ ] no mastery level raised only because docs/labs exist
[ ] V1 release snapshot / audit commit recorded
```

## 16. Final recommendation

现在最不应该做的是：

```text
继续增加 Q38/Q39/...
继续增加 L09/L10 只为数量
一次性补全四篇 generic foundations
把 Data 库已有内容复制进 Part 8
```

现在最应该做的是：

```text
close Q05/Q06
populate Current Case
freeze V1
switch to mastery-driven maintenance
```

V1 之后，新增 stable theory 必须满足至少一个条件：

- mastery audit 暴露真实知识缺口；
- 新项目反复遇到同一问题；
- 至少两个案例支持新的 reusable pattern；
- current / frozen case 需要新的稳定 abstraction。

否则默认不扩 core。
