# Part 0 — Foundations

目标：只补 LLM / Agent Evaluation 真正需要的地基，不扩展成完整 CS / ML 教材。

## 最小范围

1. [Probability & Statistics for Eval](01_Probability_and_Statistics_for_Eval.md) — **已建立第一版**
2. Machine Learning Basics for Eval
3. LLM Fundamentals for Eval
4. [Experiment Design Basics](04_Experiment_Design_Basics.md) — **已建立第一版**
5. Data Handling for Eval
6. [Agent Fundamentals for Eval](06_Agent_Fundamentals_for_Eval.md) — **已建立第一版**
7. Software Engineering for Eval

## 纳入标准

只有当缺少某个基础会直接导致以下至少一项受阻时才纳入：

- 看不懂评测论文/报告；
- 设计不了 metric / experiment；
- 分析不了 uncertainty / failure；
- 实现不了 eval harness；
- 无法解释 Agent trace。

否则默认不展开。

## 第一批基础的学习顺序

```text
Probability & Statistics
        ↓
Estimand / Unit of Analysis
        ↓
Experiment Design
        ↓
Evaluation Contract / Metric Design

Agent Fundamentals
        ↓
Agent Evaluation Contract
```

## 学习完成标准

不是“看过公式”，而是能在后续 Part 中实际使用。
