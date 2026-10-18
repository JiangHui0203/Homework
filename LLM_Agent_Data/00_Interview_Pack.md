# LLM / Agent Data Interview Pack

> 状态：`Stable Mother Edition V3.x / Scenario Assembly`
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
有没有把 Failure 直接等于 Data Gap？
有没有把 Judge 当 Ground Truth？
有没有只报 Accuracy 不报 Budget？
有没有把 Agent failure 自动归 Model？
有没有给内部研究结果编外部出处？
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
Canonical Definition
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
→ Tool / Harness / Environment
→ Evaluator
→ Failure Chain
→ Owner
→ Intervention
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
→ Matched Budget
→ Frozen Protocol
→ Target / Transfer / Regression
→ Uncertainty
→ Cost
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
Evidence 从哪来？
↓
数据怎么构造？
↓
label / verifier 靠谱吗？
↓
实验怎么公平？
↓
有没有 regression？
↓
成本值不值？
↓
上线后怎么监控？
```

一个答案如果能一路走到：

```text
Decision + Monitoring
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

# 9. 面试表达的七条红线

```text
1. 不把 Agent Failure 自动归 Model。
2. 不把 Production Log 自动当 Training Data。
3. 不把 Judge Agreement 当 Ground Truth Validity。
4. 不把 Oracle Headroom 当 Online Selector Gain。
5. 不把 Triggered-only 结果当 E2E。
6. 不把更高 Score 与不同 Budget 混在一起。
7. 不把未公开的内部 Research Result 包装成外部事实。
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
一个 Case
+
一个 Experiment
+
一个 Decision
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
```

最终原则：

> **面试不是证明“我见过这些名词”，而是证明“我能把真实问题组织成可验证、可决策、可迭代的系统”。**
