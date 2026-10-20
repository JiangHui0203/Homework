# LLM / Agent Data Interview Pack

> 状态：`Stable Mother Edition V3.x / Scenario Assembly / Stress-tested`
>
> 目标：把已经稳定的知识、图、Case、Interview Index 与 Quick-reference **装配成一套可以直接用于面试 / 答辩 / 自我介绍的使用路径**。
>
> 本文件不新增 canonical concept，也不重复 27 类题库答案。
>
> 题库真源：[`Interview Index`](./00_Interview_Index.md)
>
> 快速框架：[`Condensed Guide`](./00_Condensed_Guide.md)
>
> 视觉表达：[`Figure Presentation Kit`](./00_Figure_Presentation_Kit.md)
>
> 快速卡片：[`Level A Quick-reference Cards`](./visual_derivatives/quick_reference/Level_A_Quick_Reference_Cards.md)
>
> 压力测试：[`Scenario Pack Stress Test`](./00_Scenario_Pack_Stress_Test.md)

---

# 0. 面试真正要展示的不是“知道多少词”

成熟表达应该让面试官听到一条稳定因果链：

```text
Problem
→ Object / State
→ Evidence
→ Diagnosis
→ Intervention
→ Evaluation
→ Decision
→ Flywheel
```

因此面试准备不是：

```text
背 SFT
背 DPO
背 Judge
背 Synthetic Data
背 Agent
```

而是训练：

> **遇到一个开放问题时，能否快速把它压回同一套问题解决系统。**

但压力测试后再加一条：

> **Framework 是地图，不是答案。第一句话必须先回答当前问题。**

---

# 0.1 Answer Contract：先回答，再展开

面试时统一使用：

```text
Direct Answer
→ Boundary
→ Mechanism / Evidence
→ Example
→ Broader System only if needed
```

例如被问：

```text
“Verifier 和 Judge 有什么区别？”
```

不要从 F1 开始讲 Learning System。

第一层应该直接说：

```text
Verifier 更依赖可明确检查的 evidence / predicate；
Judge 更适合解释性 quality criterion。
但二者都不是天然 Ground Truth，关键仍是 claim 与 evidence 是否匹配。
```

然后看面试官是否继续追。

## Stop Depth

回答默认只展开到“最小充分深度”：

```text
30 秒
→ thesis / direct answer

2 分钟
→ boundary + mechanism + evidence

5 分钟
→ case + experiment + decision
```

不要为了证明自己系统，主动把每个问题都讲成一堂课。

## Evidence Provenance

口头上必须能听出四种信息来源：

```text
Public Literature
→ “公开工作里……”

My Project / Frozen Result
→ “我自己的项目里实际冻结的是……”

Canonical Teaching Case
→ “为了说明结构，我用 C1 举例……”

Hypothetical Design
→ “如果让我新做这个项目，我会……”
```

固定边界：

```text
我知道
≠ 我做过
≠ 我用来教学的例子
≠ 我假设会怎么做
```

## Quantitative Claim Contract

任何实验数字，至少带：

```text
Population / denominator
Baseline vs Treatment
Protocol
Budget
Metric
Claim Scope
```

如果是 selective / routing system，再补：

```text
Full
Eligible / Screened
Triggered
Intervened
Observed
```

数字本身不是加分点；**数字的实验语义说清楚才是。**

---

# 1. 一套面试只准备四种资产

## A. 1 个总框架

使用：

```text
F1 Learning System
```

一句话：

> LLM / Agent Data 不是维护训练集，而是在真实目标、Experience、Evidence、Learning Signal、Training、Evaluation 与 Monitoring 之间维护一个可验证的 Learning System。

---

## B. 2–3 个深度 Case

按岗位选择：

```text
Agent Data
→ C1 + C3

Reasoning / Test-time
→ C4

Eval / Verifier / Code Agent
→ C5
```

这里的 C1 / C3 / C4 / C5 是 **Canonical Teaching Case / Practical Study**，适合练习“怎么把问题讲完整”，不等于个人项目经历。面试官如果追问“你实际做过什么”，必须切换到自己的 My Project / Frozen Result；尤其 C4 只能帮助组织 reasoning-intervention 结构，不能直接当作 RoTFuse / K17 的实验证据。

不要准备十个浅案例。

目标是任何案例都能讲到：

```text
Task Contract
Evidence
Failure / Gap
Intervention
Experiment
Decision
```

---

## C. 4 张核心图

默认：

```text
F1
→ F6
→ F8
→ F14
```

它们分别回答：

```text
我怎么看这个领域？
我怎么诊断问题？
我怎么证明方案？
我怎么落地？
```

Agent-heavy 岗位增加：

```text
F4
```

Data-flywheel 岗位增加：

```text
F9
```

---

## D. 1 套回答骨架

固定：

```text
Define
→ Diagnose
→ Hypothesize
→ Construct
→ Verify
→ Experiment
→ Flywheel
```

来自 [`Interview Index`](./00_Interview_Index.md)。

这套骨架只在需要展开时使用；**不能替代 Direct Answer。**

---

# 2. 30 分钟面试前复习路径

## 0–5 min：只看六问

```text
1. What should the model learn?
2. From what experience?
3. With what feedback?
4. How do we know it learned?
5. Is it worth the cost?
6. When should the system learn again?
```

## 5–10 min：看四张 Quick-reference

```text
F1
F6
F8
F14
```

## 10–20 min：复述一个 Case

推荐 C1：

```text
shipped observation
→ wrong refund
→ evidence
→ first harmful action
→ capability gap
→ data intervention
→ matched-budget experiment
→ scale / stop
```

## 20–25 min：过五类高频题

```text
什么是 Agent Data？
怎么做 Synthetic Data？
怎么验证 Judge？
怎么证明一批数据有用？
线上指标掉了怎么排？
```

对应 [`Interview Index`](./00_Interview_Index.md)。

## 25–30 min：检查表达红线

```text
有没有第一句话没回答问题，先开始背框架？
有没有把 Failure 直接等于 Data Gap？
有没有把 Judge 当 Ground Truth？
有没有只报 Accuracy 不报 Budget？
有没有把 Agent failure 自动归 Model？
有没有混淆“公开工作 / 我做过 / 教学例子 / hypothetical”？
有没有给内部研究结果编外部出处？
有没有报数字但没说 denominator / protocol？
```

---

# 3. 90 分钟系统准备路径

```text
20 min
Condensed Guide

20 min
F1 / F4 / F6 / F8 / F14 Presentation Track

25 min
C1 + 目标岗位 Case

15 min
Interview Index 按题型抽查

10 min
模拟追问
```

模拟追问不只测“能不能答”，还测：

```text
能不能先直接答？
会不会把一个 hypothesis 讲成唯一 root cause？
会不会在数字追问里丢 denominator？
会不会把公开文献和自己的实验混在一起？
```

目标不是“读完”，而是能脱稿完成：

```text
30 秒定义
2 分钟展开
5 分钟案例
```

三个尺度。

---

# 4. 60 秒自我定位模板

不要按技能名堆砌：

```text
SFT / DPO / Agent / Judge / Synthetic / Benchmark...
```

推荐按问题链表达：

```text
我关注的是如何把真实 LLM / Agent failure
转成可验证的数据与评测问题。

我通常先定义 Task / Case / Environment 和 Evidence，
再做 Failure / Credit Analysis 判断是不是 Data Gap；
如果是，再设计 Human / Synthetic / Rollout 等 Experience，
构造合适的 SFT / Preference / Process / Recovery Signal，
并用 matched-budget、frozen protocol 的实验验证收益、回归和成本。

有效以后才进入 production / monitoring，
把 fresh failure 接回下一轮 learning loop。
```

然后接自己的一个真实研究 / 项目案例。

一旦进入自己的项目，显式切换话语：

```text
“在我自己的项目里……”
```

不要让面试官猜哪些是 literature、哪些是 personal evidence。

---

# 5. 五类面试问题，五种入口

## Type A — Definition

例如：

```text
Preference Data 是什么？
Agent Trajectory 是什么？
Verifier 和 Judge 有什么区别？
```

回答方式：

```text
Direct Definition
→ Neighbor Boundary
→ Example
```

优先资产：

```text
Glossary
Concept Index
F2 / F5 / F7
```

---

## Type B — Design

例如：

```text
怎么设计 Agent Benchmark？
怎么设计 Synthetic Data pipeline？
怎么做 Data Flywheel？
```

回答方式：

```text
Goal
→ Contract
→ Evidence
→ Pipeline
→ Quality Gate
→ Experiment
→ Decision
```

优先资产：

```text
F8 / F9
Playbooks
Artifact Kit
```

---

## Type C — Diagnosis

例如：

```text
线上 success 掉了怎么办？
Agent 明明说成功但任务没完成怎么办？
Judge score 涨但真实 success 不涨怎么办？
```

回答方式：

```text
Metric / Evidence
→ Alternative Hypotheses
→ Tool / Harness / Environment
→ Evaluator
→ Failure Chain
→ Owner
→ Intervention
```

压力测试后的固定纪律：

```text
提出一个可能 root cause
≠ 已经证明它是 root cause
```

优先资产：

```text
F4 / F6 / F13
C1 / C3 / C5
Problem Index
```

---

## Type D — Experiment

例如：

```text
怎么证明这批数据有用？
怎么比较两个 selector？
怎么证明 hard negatives 有价值？
```

回答方式：

```text
Hypothesis
→ Baseline
→ Intervention
→ Population Ledger
→ Matched Budget
→ Frozen Protocol
→ Target / Transfer / Regression
→ Uncertainty
→ Cost
→ Claim Scope
→ Scale / Stop
```

优先资产：

```text
F8 / F10
Ch21
C4 / C5
```

---

## Type E — Strategy / Ownership

例如：

```text
100 万条数据先做什么？
这个 failure 要不要补数据？
资源有限怎么投？
```

回答方式：

先给“第一步”：

```text
先确认对象是否可信：
identity / provenance / task-family / success evidence / environment version
```

再展开：

```text
Problem Gate
→ Root Cause / Owner
→ Capability Gap
→ Value / Learnability / Verifiability / Cost
→ Minimal Pilot
→ Decision
```

优先资产：

```text
F10 / F14
Ch18 / Ch24 / Ch25
```

---

# 6. 追问树：回答到哪一层算“站得住”

面试官往下追时，常见顺序是：

```text
你为什么这么定义？
↓
怎么知道问题真的在这里？
↓
还有哪些 alternative hypotheses？
↓
Evidence 从哪来？
↓
数据怎么构造？
↓
label / verifier 靠谱吗？
↓
实验怎么公平？
↓
denominator / budget 是什么？
↓
有没有 regression？
↓
成本值不值？
↓
这个结论能说多大？
↓
上线后怎么监控？
```

一个答案如果能一路走到：

```text
Decision + Claim Scope + Monitoring
```

通常比只讲 pipeline 更完整。

---

# 7. 四个 Case 的面试用途

| Case | 最适合回答 | 关键边界 |
|---|---|---|
| C1 | Agent failure → data loop | Failure ≠ Training Example |
| C3 | Tool / Harness / Permission | Failure Layer ≠ Failure Owner |
| C4 | Test-time reasoning / selector | Oracle Gap ≠ E2E Gain |
| C5 | Eval / verifier / code | Judge Preference ≠ Executable Truth |

不要把四个都讲一遍。

面试里只选最能回答当前问题的一个。

---

# 8. 三个成熟度层级

## Level 1 — Knowledge

```text
我知道 SFT / DPO / Judge / Agent Data。
```

## Level 2 — Pipeline

```text
我知道这些组件怎样串起来。
```

## Level 3 — Decision System

```text
我知道在什么 Evidence 下该用哪个 intervention，
怎么验证它，什么时候停止，以及失败时该归谁。
```

目标始终是 Level 3。

---

# 9. 面试表达的十条红线

```text
1. 不让 Framework 盖过问题本身；第一句话先回答问题。
2. 不把 Agent Failure 自动归 Model。
3. 不把 Production Log 自动当 Training Data。
4. 不把 Judge Agreement 当 Ground Truth Validity。
5. 不把 Oracle Headroom 当 Online Selector Gain。
6. 不把 Triggered-only 结果当 E2E。
7. 不把更高 Score 与不同 Budget 混在一起。
8. 不把一个 diagnostic hypothesis 讲成已确认 Root Cause。
9. 不混淆 Public Literature / My Project / Teaching Case / Hypothetical Design。
10. 不报脱离 denominator / protocol / claim scope 的数字，也不把未公开内部结果包装成外部事实。
```

---

# 10. 一页最终复习顺序

```text
F1
我怎么看整个系统？
↓
F4
Agent 世界里真实发生什么？
↓
F6
为什么失败、该修谁？
↓
F8
怎么证明方案有效？
↓
F9
怎么进入下一轮学习？
↓
F14
团队 / 个人怎么持续运行？
```

然后记住：

```text
一个 Direct Answer
+
一个 Case
+
一个 Experiment
+
一个 Decision
+
一个 Claim Scope
```

比背二十个术语更有说服力。

---

# 11. 配套入口

```text
快速知识
→ Condensed Guide

题型
→ Interview Index

图怎么讲
→ Figure Presentation Kit / D2 Storyboards

面试前速记
→ Level A Quick-reference Cards

案例
→ C1 / C3 / C4 / C5 Practical Studies

方法出处
→ Canonical References

压力测试
→ Scenario Pack Stress Test
```

最终原则：

> **面试不是证明“我见过这些名词”，而是证明“我能先准确回答眼前问题，再把它组织进一个有证据、有边界、有决策的系统”。**
