# LLM / Agent Data Knowledge System：Master Figure System

> 状态：**Canonical Visual System / Production Refinement**
>
> 目的：为 0–25 章维护一套稳定、可复用、可版本化的 Master Figures。图的任务不是装饰，而是压缩跨章节关系、固定对象边界、帮助读者建立全书级 mental model。
>
> 原则：**一张图只承担一个主要认知任务；canonical concept 只在对应 Master Figure 中完整展开，其他章节优先引用而不是重复重画。**
>
> 视觉成品规范：[`Figure Design Contract`](./00_Figure_Design_Contract.md)

---

# 0. Semantic Source 与 Presentation Derivative

当前视觉系统采用：

```text
Mermaid Master Figure
= semantic source of truth

SVG / PNG / PPT / PDF redraw
= presentation derivative
```

因此未来可以升级：

```text
字体
配色
布局
线型
留白
动画 / progressive reveal
```

但不能只在图片里静默修改：

```text
node semantics
edge semantics
canonical concept relation
Case ID meaning
```

如果语义关系改变，必须先回写 Mermaid source。

---

# 1. Visual Grammar

统一语义：

```text
实线箭头  → Execution / State Transition / Causal or Operational Progression
虚线箭头  → Evidence / Feedback / Derived / Auxiliary Relation
菱形       → Decision / Gate / Question
方框       → Object / State / Artifact / Process
子图       → Layer / Owner / Phase
```

Mermaid 默认不依赖颜色表达核心含义，保证 GitHub Light / Dark Mode、打印和后续导出都可读。

图内文字规则：

1. 节点优先放 canonical term，不放完整段落。
2. 第一行写 canonical term，必要时第二行补解释。
3. 同一概念全书统一写法，例如 `World State`、`Agent-visible State`、`Outcome`、`Reward`、`Credit`。
4. Case variant 直接使用 `C1-VB / C4-SC` 等稳定 ID。
5. 图下正文解释“为什么”，图本身展示“关系是什么”。

完整规则见 [`00_Figure_Design_Contract.md`](./00_Figure_Design_Contract.md)。

---

# 2. Master Figure Registry

| ID | Figure | Figure Question | Canonical Owner | Primary Case |
|---|---|---|---|---|
| [F1](./figures/F1_Learning_System_Overview.md) | Learning System Overview | 整本书到底在描述什么 Learning System？ | Ch0 / Ch25 | C1 + C4 |
| [F2](./figures/F2_Data_Object_and_Learning_Signal_Evolution.md) | Data Object & Learning Signal Evolution | Example 怎样扩展成 Experience？ | Ch1–3 | C1 |
| [F3](./figures/F3_Reasoning_State_Decision_Stack.md) | Reasoning State Decision Stack | Reasoning State 上哪五种判断必须分开？ | Ch4 | C4-SC |
| [F4](./figures/F4_Agent_Task_Environment_Trajectory.md) | Agent Task–Environment–Trajectory | Task、Tool、Harness、Environment、Trajectory 怎么连接？ | Ch10–12 | C1-VB |
| [F5](./figures/F5_Trajectory_Anatomy.md) | Trajectory Anatomy | 一条 trajectory 到底应该记录什么？ | Ch12 | C1-F1 |
| [F6](./figures/F6_Credit_to_Failure_Causal_Map.md) | Credit → Failure Causal Map | 从 Outcome 到 Root Cause / Owner 应怎样拆？ | Ch13–14 | C1-F1 + C3-F5 |
| [F7](./figures/F7_Evidence_Verifier_Grader_Judge.md) | Evidence → Evaluator Stack | 一条 Label 到底建立在什么 Evidence 和 Evaluator 上？ | Ch15 | C1-VB + C5-F3 |
| [F8](./figures/F8_Benchmark_Evaluation_Protocol.md) | Benchmark / Evaluation Protocol | “方法更好”这个结论怎样才成立？ | Ch16 | C1 family |
| [F9](./figures/F9_Data_Flywheel.md) | Data Flywheel | 一个真实 Failure 怎样重新进入 Learning Loop？ | Ch17 | C1 |
| [F10](./figures/F10_Data_Strategy_Portfolio_ROI.md) | Data Strategy / Portfolio / ROI | 有限 Data Budget 应该投到哪里？ | Ch18 | C1–C5 portfolio |
| [F11](./figures/F11_Governance_Lineage_DAG.md) | Governance / Lineage DAG | 一个结论怎样追溯回原始 Evidence？ | Ch19 | C1 assets |
| [F12](./figures/F12_Data_Production_System.md) | Data Production System | 高价值 Experience 怎样被稳定规模生产？ | Ch22 | C1 recovery family |
| [F13](./figures/F13_Monitoring_Drift_Diagnostic_Tree.md) | Monitoring / Drift Diagnostic Tree | 指标变化以后首先应该排查什么？ | Ch23 | C1 / C3 |
| [F14](./figures/F14_Operating_Model_and_Capability_Map.md) | Operating Model + Capability Map | 团队和个人怎样调用整套系统？ | Ch24–25 | all cases |

---

# 3. Figure Levels

## Level A — Book-level

用于形成整本书的 mental model：

```text
F1  Learning System
F4  Agent Task–Environment–Trajectory
F6  Credit → Failure
F8  Evaluation Protocol
F9  Data Flywheel
F14 Operating Model + Capability Map
```

这六张应满足：

> **即使脱离章节单独展示，也能在 30–90 秒内讲清自己的主问题。**

## Level B — Part-level

负责压缩某一个 Part 的核心关系：

```text
F2  Learning Signals
F3  Reasoning State
F5  Trajectory Anatomy
F7  Evaluator Stack
F10 Data Strategy
F11 Governance / Lineage
F12 Data Production
F13 Monitoring / Drift
```

## Level C — Chapter-local

局部 pipeline / formula / example 图仍可保留，但不能重新定义 Level A/B 已固定的关系。

原则：

```text
Master Figure
= stable system model

Chapter-local Figure
= analytical lens
```

---

# 4. Figure File Contract

F1–F14 顶部统一包含：

```text
Figure Question
Level
Canonical Owner
Primary Case
Scope
```

Mermaid 之后优先包含：

```text
Read the Spine
Critical Boundaries
Case Lens
Cross-links
```

不是所有图都必须机械使用四个标题；但任何图单独打开时，必须能够回答：

```text
它在讲什么？
怎么看主链？
最容易混淆什么？
哪个 case 能证明？
应该去哪里继续读？
```

---

# 5. Case Integration Rule

图中使用 case 时：

```text
C1-VB = shipped / no refund allowed
C1-F1 = shipped observed but refund executed
C3-F5 = tool truth failure / harness observation success
C4-SC = same authoritative prefix sibling set
C5-F2 = public tests pass / hidden test fail
```

Case ID 不得为了图示简洁改变语义。

Case 只承担两种角色：

```text
Primary Case
→ 帮助理解整张图

Boundary Case
→ 专门证明一个容易混淆的边界
```

---

# 6. 14 张图形成的完整视觉链

```text
F1  Learning System
↓
F2  Data Object / Learning Signal
↓
F3  Reasoning Decision Stack

F4  Agent World
↓
F5  Trajectory Anatomy
↓
F6  Credit → Failure

F7  Evidence / Evaluator
↓
F8  Evaluation Protocol

F9  Data Flywheel
↓
F10 Data Strategy
↓
F11 Governance / Lineage

F12 Data Production
↓
F13 Monitoring / Drift
↓
F14 Operating Model / Capability Map
```

它们对应整本书最重要的六个问题：

```text
What is the learning system?
What experience exists?
What happened in the agent world?
How do we know it is good or bad?
Which experience is worth learning?
How do we keep the system operating and learning?
```

---

# 7. Production Refinement Order

成品化按两层进行：

```text
Batch A — Level A
F1 / F4 / F6 / F8 / F9 / F14

Batch B — Level B
F2 / F3 / F5 / F7 / F10 / F11 / F12 / F13
```

每张图只做：

```text
header contract
reading spine
critical boundaries
case lens
caption readiness
cross-links
```

不在本阶段改变 canonical relation。

之后才考虑：

```text
publication SVG redraw
slide progressive reveal
social / interview quick-reference derivative
```

---

# 8. Visual Acceptance

当前基础状态：

```text
F1–F14 semantic registry
✓ stable

Canonical visual ownership
✓ stable

Duplicate global visual definitions
✓ cleaned

Figure Design Contract
✓ established

Production refinement
→ active
```

最终目标：

> **读者即使暂时不读 25 章全文，也能通过 14 张 Master Figures 建立正确的整体结构；再进入章节时，只是在放大某个局部，而不是重新学习一套世界。**
