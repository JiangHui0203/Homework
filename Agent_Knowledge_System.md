# Agent 基础知识体系

> 用途：作为 Agent 学习、面试准备与后续专题扩展的长期主文档。
>
> 维护方式：按“层 → 章 → 节”逐步补全。先建立概念体系，再整理面试问题；新概念优先归入现有结构，除非确实无法归类，否则不随意增加一级章节。
>
> 当前版本：V1（2026-10-16）

---

## 0. 总体框架

整套知识体系分为四层，分别回答四个问题：

1. **Model & Decision Core**：Agent 下一步为什么这样决策？
2. **Capabilities & Interoperability**：Agent 能感知什么、调用什么、与谁交互？
3. **Harness & Agent System**：这些能力如何被组织成一个可靠运行的 Agent 系统？
4. **Adaptation & Self-Improvement**：Agent 如何从执行经验中改进自身？

```text
I. Model & Decision Core
        ↓
II. Capabilities & Interoperability
        ↓
III. Harness & Agent System
        ↓
IV. Adaptation & Self-Improvement
```

学习顺序原则：**I → II → III → IV**。

---

# I. Model & Decision Core

## 1. LLM Foundation for Agents

> 目标：只学习真正影响 Agent 行为的 LLM 基础，不重新展开完整的大模型原理课程。

### 1.1 Autoregressive Generation

待补充。

### 1.2 Prompt / System Instruction

待补充。

### 1.3 Context Window

待补充。

### 1.4 Sampling & Decoding

- Temperature
- Top-p
- Deterministic decoding / greedy decoding

待补充。

### 1.5 Structured Output

待补充。

### 1.6 Function Calling / Tool Calling

待补充。

### 1.7 Multimodal Input

待补充。

### 1.8 Token / Cost / Latency Budget

待补充。

---

## 2. Agent Decision Loop

### 2.1 What is an Agent?

待补充。

### 2.2 Agent Loop

- State
- Decision
- Action
- Observation
- Termination

待补充。

### 2.3 ReAct

待补充。

### 2.4 Planning

- Task decomposition
- Plan-and-Execute
- Replanning

待补充。

### 2.5 Reflection / Critique

待补充。

### 2.6 Verification

待补充。

### 2.7 Routing

待补充。

### 2.8 Agent vs Workflow

待补充。

---

# II. Capabilities & Interoperability

## 3. Tool Use & Action

### 3.1 Tool Definition
### 3.2 Tool Schema
### 3.3 Tool Description
### 3.4 Tool Selection
### 3.5 Argument Generation
### 3.6 Tool Execution
### 3.7 Observation
### 3.8 Failure Handling

- Invalid arguments
- Timeout
- Empty result
- Execution failure
- Retry

### 3.9 Side Effects

- Idempotency
- Confirmation
- Irreversible actions

以上各节待补充。

---

## 4. Context, Memory & Retrieval

### 4.1 Context Engineering

- Context selection
- Context compression
- Context ordering
- Context budgeting

### 4.2 Working State
### 4.3 Short-term Memory
### 4.4 Long-term Memory

- Semantic Memory
- Episodic Memory
- Procedural Memory
- User Memory

### 4.5 Persistence
### 4.6 Retrieval

- Search
- RAG
- Query Rewrite
- Iterative Retrieval
- Agentic RAG

以上各节待补充。

需要始终保持以下边界：

```text
Context = 当前一次 inference 中模型实际看到的内容
Memory  = 信息如何被保存、组织并在之后重新取回
RAG     = 从外部知识源检索信息并送入 Context 的机制之一
```

---

## 5. Capability Extension & Protocols

### 5.1 Native Tools
### 5.2 Skills
### 5.3 MCP

- Host
- Client
- Server
- Tools
- Resources
- Prompts
- Transport

### 5.4 Capability Discovery

以上各节待补充。

---

## 6. Multi-Agent & Agent Interoperability

### 6.1 Why Multi-Agent?
### 6.2 Orchestration Patterns

- Manager / Supervisor
- Router
- Handoff
- Agents-as-Tools
- Parallel Workers
- Debate / Collaboration

### 6.3 Subagents
### 6.4 Communication
### 6.5 Shared / Private Context
### 6.6 Coordination Failure
### 6.7 A2A

- Agent Card
- Discovery
- Task
- State
- Remote Agent

以上各节待补充。

概念边界：

```text
MCP：Agent ↔ Capability / Data / Tool
A2A：Agent ↔ Agent
```

---

# III. Harness & Agent System

## 7. Agent Harness

> Harness 是本体系的核心章节之一。重点不是罗列 Tool、Memory、Subagent，而是理解 Harness 如何制定并执行这些能力的使用策略。

### 7.1 What is an Agent Harness?
### 7.2 Agent Loop Policy
### 7.3 Instruction Policy
### 7.4 Context Policy
### 7.5 Tool Policy
### 7.6 Memory Policy
### 7.7 Planning Policy
### 7.8 Subagent Policy
### 7.9 Permission / Approval Policy
### 7.10 Termination Policy
### 7.11 Recovery Policy

以上各节待补充。

核心边界：

```text
Tool / Memory / Subagent = Capability
Tool Policy / Memory Policy / Subagent Policy = Harness
```

---

## 8. Runtime & Infrastructure

### 8.1 Execution Environment
### 8.2 State
### 8.3 Session
### 8.4 Persistence
### 8.5 Checkpoint
### 8.6 Sandbox
### 8.7 Filesystem
### 8.8 Code Execution
### 8.9 Long-running Tasks
### 8.10 Scheduling / Queue
### 8.11 Concurrency
### 8.12 Fault Tolerance

- Timeout
- Retry
- Resume
- Recovery

以上各节待补充。

核心边界：

```text
Harness = control logic
Runtime = execution substrate
```

---

## 9. Observability & Evaluation

### 9.1 Observability

- Logs
- Trace
- Span
- Trajectory

### 9.2 Outcome Evaluation

- Correctness
- Task completion
- User goal satisfaction

### 9.3 Process Evaluation

- Reasoning trajectory
- Planning
- Intermediate state

### 9.4 Tool Evaluation

- Tool selection
- Argument correctness
- Result utilization

### 9.5 Agent Evaluation
### 9.6 Evaluators

- Rule-based
- Ground Truth
- LLM-as-Judge
- Human
- Environment / Verifier

### 9.7 Efficiency

- Tokens
- Latency
- Tool calls
- Cost

### 9.8 Reliability

待补充。

---

## 10. Safety, Permissions & Governance

### 10.1 Prompt Injection
### 10.2 Indirect Prompt Injection
### 10.3 Tool Injection
### 10.4 Data Exfiltration
### 10.5 Authentication
### 10.6 Authorization
### 10.7 Least Privilege
### 10.8 Sandbox
### 10.9 Human Approval
### 10.10 Guardrails
### 10.11 Audit

以上各节待补充。

基本安全链路：

```text
Model Capability
       ↓
Agent Capability
       ↓
Permission
       ↓
Allowed Action
```

---

# IV. Adaptation & Self-Improvement

## 11. Inference-time Self-Refinement

### 11.1 Critique
### 11.2 Reflection
### 11.3 Retry
### 11.4 Verification
### 11.5 Self-Correction
### 11.6 Iterative Refinement

以上各节待补充。

核心边界：当前任务中的自我修正不等于 Agent 自身发生持久变化，因此不能简单等同于 RSI。

---

## 12. Learning from Experience

### 12.1 Trajectory Storage
### 12.2 Success / Failure Memory
### 12.3 Experience Retrieval
### 12.4 Skill Acquisition
### 12.5 Procedural Memory
### 12.6 Continual Adaptation

以上各节待补充。

---

## 13. Agent Optimization

### 13.1 Prompt Optimization
### 13.2 Context Policy Optimization
### 13.3 Memory Optimization
### 13.4 Tool Optimization
### 13.5 Skill Optimization
### 13.6 Planning Optimization
### 13.7 Workflow Optimization
### 13.8 Harness Optimization
### 13.9 Evaluator Optimization

以上各节待补充。

---

## 14. Recursive Self-Improvement (RSI)

### 14.1 What is being improved?
### 14.2 Improvement Proposer
### 14.3 Evaluator / Verifier
### 14.4 Candidate Generation
### 14.5 Selection
### 14.6 Update
### 14.7 Recursive Iteration
### 14.8 Credit Assignment
### 14.9 Generalization
### 14.10 Overfitting
### 14.11 Regression
### 14.12 Reward Hacking
### 14.13 Stability

典型闭环：

```text
Agent_t
  ↓
Tasks
  ↓
Trajectories
  ↓
Evaluation
  ↓
Improvement Proposal
  ↓
Candidate Agent
  ↓
Selection / Update
  ↓
Agent_t+1
  └──────────────→ 下一轮自我改进
```

---

## 15. Harness RSI & Model–Harness Co-evolution

### 15.1 Frozen Model + Evolving Harness
### 15.2 Harness as Optimization Target
### 15.3 Context / Tool / Memory Policy Evolution
### 15.4 Inter-agent Information Flow
### 15.5 Generalization vs Evolution-set Overfitting
### 15.6 Regression Control
### 15.7 Model–Harness Co-evolution

以上各节待补充。

---

# 16. Cross-cutting Concepts

以下概念会跨层出现，但必须保持主归属清晰：

| 概念 | 主归属 | 在其他层出现时的含义 |
|---|---|---|
| Reflection | I. Decision Core | IV 中作为 self-refinement 手段 |
| Tool | II. Capability | III 中讨论 Tool Policy |
| Memory | II. Capability | III 中讨论 Memory Policy；IV 中用于 experience learning |
| RAG | II. Context / Retrieval | 不单独作为一级层 |
| Skills | II. Capability Extension | III 中讨论何时加载与调用 |
| MCP | II. Interoperability | III 中讨论 MCP capability 的使用策略 |
| Subagent | II. Multi-Agent | III 中讨论 delegation / spawning policy |
| A2A | II. Agent Interoperability | 与 MCP 区分 |
| Harness | III. Agent System | IV 中可成为 optimization target |
| Runtime | III. Agent System | 提供执行基础设施 |
| Evaluation | III. Agent System | IV 中提供 self-improvement feedback |
| RSI | IV. Self-Improvement | 不等同于普通 reflection |

---

# 17. 不作为一级知识层的内容

## 17.1 Frameworks

例如：

- LangGraph
- OpenAI Agents SDK
- Google ADK
- AutoGen
- CrewAI

这些是实现多个知识层的工程载体，而不是独立的知识层。后续采用“概念 → 框架映射”的方式学习，而不是围绕框架 API 组织整套知识体系。

## 17.2 Domain Case Studies

例如 Coding Agent。它是多个能力与系统组件的综合应用：

```text
Model
+ Planning
+ Search
+ File Tools
+ Shell
+ Code Editing
+ Harness
+ Sandbox
+ Git
+ Tests
+ Evaluation
```

后续可用 Codex、Claude Code、Cursor、OpenCode 等作为综合案例，但不把 Coding Agent 单独提升为基础知识层。

---

# 18. 每章统一写作模板

后续每一章尽量按照同一模板补全：

1. **定义：它是什么？**
2. **动机：为什么需要它？**
3. **机制：最小工作原理是什么？**
4. **系统位置：它位于 Agent 架构的哪一层？**
5. **边界：它与相邻概念有什么区别？**
6. **最小例子：用一个简单场景说明。**
7. **典型实现：主流框架/系统如何落地？**
8. **Failure Modes：常见失败方式是什么？**
9. **工程问题：可靠性、成本、延迟、安全如何处理？**
10. **面试掌握边界：需要回答到什么深度？**
11. **高频追问：在完整知识体系建立后再补充。**
12. **参考资料：优先官方文档、原始论文与高质量工程资料。**

---

# 19. 当前进度

| 层 | 章节 | 状态 |
|---|---|---|
| I | 1. LLM Foundation for Agents | 待写 |
| I | 2. Agent Decision Loop | 待写 |
| II | 3. Tool Use & Action | 待写 |
| II | 4. Context, Memory & Retrieval | 待写 |
| II | 5. Capability Extension & Protocols | 待写 |
| II | 6. Multi-Agent & Agent Interoperability | 待写 |
| III | 7. Agent Harness | 待写 |
| III | 8. Runtime & Infrastructure | 待写 |
| III | 9. Observability & Evaluation | 待写 |
| III | 10. Safety, Permissions & Governance | 待写 |
| IV | 11. Inference-time Self-Refinement | 待写 |
| IV | 12. Learning from Experience | 待写 |
| IV | 13. Agent Optimization | 待写 |
| IV | 14. Recursive Self-Improvement | 待写 |
| IV | 15. Harness RSI & Model–Harness Co-evolution | 待写 |

下一步：从 **I. Model & Decision Core → 1. LLM Foundation for Agents** 开始逐节补全。
