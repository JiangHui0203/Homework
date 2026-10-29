# Agent Fundamentals for Eval — 只学评测需要的抽象

> 本篇不讲如何构造所有 Agent 架构，只建立能读懂 Agent Evaluation 的最小模型。

## 1. Task

系统要完成的目标。Eval 必须区分 task specification 与模型自己生成的 plan。

## 2. Environment

Agent 交互的外部世界：数据库、浏览器、文件系统、API、代码执行器、游戏环境等。

Environment 会变化，因此 Agent Eval 常需要 snapshot / fixture / replay。

## 3. State

当前执行所依赖的信息状态，例如：

- 对话历史；
- tool results；
- structured scratch state；
- workflow status；
- memory retrieval result。

State 污染会造成跨任务泄漏。

## 4. Action

Agent 对环境采取的动作，例如 tool call、SQL query、API request、final answer。

Eval 不只看“有没有调用工具”，还要看：

- tool selection；
- arguments；
- constraints；
- timing；
- result usage。

## 5. Observation

环境返回给 Agent 的信息。Agent 可能正确得到 observation，也可能错误解释 observation；这两类 failure 要分开。

## 6. Tool

可执行能力接口。Tool correctness 与 Agent decision correctness 是两个层面：

```text
Agent 选错工具 ≠ 工具执行错误
```

## 7. Policy / Planner / Controller

决定下一步 action 的机制，可以是 LLM、规则、workflow 或混合系统。Evaluation 更关心**它在什么状态下做了什么决定**，而不是强制某一种架构术语。

## 8. Memory

跨 step 或跨 task 保存的信息。Eval 要问：

- memory 是否命中；
- 是否真正注入模型上下文；
- 是否被使用；
- 是否改善 outcome；
- 是否造成污染或成本增加。

## 9. Trajectory

一条完整交互序列：

```text
τ = (s0, a0, o1, s1, a1, o2, ...)
```

在工程上通常由 trace events 表示。Trajectory 是 Agent failure analysis 的核心对象。

## 10. Outcome

最终状态，不应只有 success/failure 两类。常见需要区分：

- correct success；
- partial completion；
- safe stop；
- recovered success；
- false accept；
- unrecovered failure；
- infrastructure abort。

## 11. Recovery

发生错误后，系统是否能检测、修正、重试、回滚或安全停止。Recovery 是 Agent 能力的一部分，也有额外成本。

## 12. Evaluation 映射

```text
Task        → task success / coverage
State       → contamination / memory correctness
Action      → tool selection / argument accuracy
Observation → grounding / interpretation
Trajectory  → first failure / credit assignment
Outcome     → correctness / safe stop / false accept
Recovery    → recovery success / recovery cost
Environment → reproducibility / replay
```

## Related

- [Q12 Agent Evaluation Contract](../03_Agent_Evaluation/01_Agent_Evaluation_Contract.md)
- [Evaluation Patterns](../EVAL_PATTERNS.md)
