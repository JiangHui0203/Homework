# 第 0 章 Overview：这套 LLM / Agent Data 知识体系到底研究什么？

> 所属体系：[`LLM_Agent_Data_Knowledge_System.md`](../LLM_Agent_Data_Knowledge_System.md)
>
> 本章定位：定义整套知识体系的研究对象、基本闭环与书级结构。

---

# 0.0 这套知识体系到底研究什么？

很多岗位会写：

- 大模型数据
- AI Data
- Agent 数据
- 数据策略
- 数据生产
- 数据合成
- 数据飞轮
- 模型评测 / Benchmark

如果只把它理解成“收集数据、清洗数据、人工标注”，会低估现在大模型数据工作的范围。

在传统监督学习里，一个数据样本经常可以抽象成：

```text
x → y
```

例如：

```text
图片 → 类别
文本 → 情感标签
问题 → 标准答案
```

而在今天的大模型系统里，一个“数据单元”可能是：

```text
Instruction
   ↓
Response
```

也可能是：

```text
Prompt
 ├── Response A
 └── Response B
        ↓
Preference: B > A
```

还可能是一条推理过程：

```text
Problem
  ↓
Reasoning State 1
  ↓
Reasoning State 2
  ↓
Reasoning State 3
  ↓
Final Answer
```

到了 Agent，更常见的是完整交互轨迹：

```text
Task
 ↓
State
 ↓
Action / Tool Call
 ↓
Observation
 ↓
New State
 ↓
Action
 ↓
...
 ↓
Final Outcome
```

因此，本体系采用一个更一般的定义：

> **大模型 / Agent 数据，本质上是在设计模型能够从中获得什么信息、什么反馈和什么学习信号。**

换句话说，“做数据”的核心已经逐渐从：

> 给样本打标签

转向：

> **定义任务 → 构造经验 → 提供反馈 → 判断成败 → 选择真正值得学习的数据。**

---

# 0.1 一张总图：从“数据样本”到“模型改进闭环”

```text
真实用户 / 目标能力 / 产品需求
            ↓
       Capability Definition
            ↓
         Task Design
            ↓
 ┌──────────┴──────────┐
 ↓                     ↓
Real Data         Synthetic Data
真实数据             合成数据
 └──────────┬──────────┘
            ↓
         Rollout
            ↓
   Response / Reasoning /
      Agent Trajectory
            ↓
 ┌──────────┴──────────┐
 ↓                     ↓
Grading              Analysis
评价/打分             错误分析
 ↓                     ↓
Training Data       Eval Set
 ↓                     ↓
SFT / DPO / RL      Regression
 └──────────┬──────────┘
            ↓
         New Model
            ↓
         New Rollout
            ↺
```

这张图里最重要的是：**数据不是流水线的起点，而是闭环中的中间产物。**

同一条模型轨迹，可能同时被用作：

- 失败分析材料；
- Benchmark case；
- SFT 样本；
- preference pair；
- reward / verifier 训练数据；
- hard case seed；
- 下一轮 synthetic data 的生成条件。

因此现代数据工作经常同时横跨：**模型、Agent、Eval、数据分析与工程系统。**

---

# 0.2 全书七个 Part

经过 1–25 章完整扩展后，整套体系已经自然形成七个 Part：

```text
Part I — Learning Signals
模型到底从什么经验和反馈中学习？

Part II — Data Acquisition & Selection
这些经验如何被人工、模型、Rollout 与 Mining 生产和选择？

Part III — Agent World & Diagnosis
Agent 在什么任务和环境里行动，轨迹与失败如何定义？

Part IV — Measurement
谁来判、怎么测、如何证明改进真实成立？

Part V — Data Optimization & Lifecycle
哪些数据值得留下、投资、治理、混合和验证？

Part VI — Data Operations
如何把有效的数据方法稳定生产、监控并组织运行？

Part VII — Synthesis
面对一个真实问题，如何把前面的知识转成可执行方案？
```

对应的总问题链是：

```text
What should the model learn?
        ↓
Where does experience come from?
        ↓
What world is the agent acting in?
        ↓
How do we know what happened?
        ↓
Which experience is worth learning?
        ↓
How do we operationalize it?
        ↓
How do we solve a real problem end-to-end?
```

---

# 0.3 一句话理解现代 LLM / Agent Data

```text
传统 ML：
数据 = 输入 + 标签

LLM Post-training：
数据 = 指令 + 响应 + 偏好 / Reward

Agent：
数据 = 任务 + 环境 + 轨迹 + 结果 + 反馈

完整 Learning System：
真实问题
→ 经验
→ 证据
→ 学习信号
→ 训练 / 策略更新
→ 评测
→ 上线
→ 新经验
```

最终要形成的能力不是“会做数据集”，而是：

> **懂模型为什么错 → 能把错误变成数据 → 能证明数据有用 → 能把这个过程规模化，并知道什么时候应该停止或重新学习。**
