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

#### 1.1.1 定义：什么是自回归生成？

大多数通用 LLM 的生成过程可以抽象成一个非常简单的目标：**在已经看到的上下文和已经生成的 token 条件下，预测下一个 token 的概率分布，然后选出一个 token，再把它加入上下文，重复这个过程。**

设初始上下文为 $c$，输出 token 序列为 $x_1,x_2,\ldots,x_T$，则整个输出序列的概率可以分解为：

$$
P(x_1,\ldots,x_T\mid c)
=
\prod_{t=1}^{T} P(x_t\mid c,x_1,\ldots,x_{t-1})
$$

也就是说，模型并不是一次性生成完整答案，而是在每一个时间步计算：

$$
P(x_t\mid c,x_{<t})
$$

然后根据这个分布，通过 greedy、temperature sampling、top-p 等 decoding 策略选择下一个 token。

最小流程可以写成：

```text
Context
   ↓
Model forward
   ↓
Logits for next token
   ↓
Probability distribution
   ↓
Decoding / Sampling
   ↓
Choose one token
   ↓
Append token to context
   ↓
Repeat
```

直到模型生成 EOS、命中 stop condition，或者达到长度上限。

这里最重要的一句话是：

> **LLM 的一次长回答，本质上是大量“预测下一个 token”步骤连续执行后的结果。**

这也是理解 Agent 行为的第一个地基。

---

#### 1.1.2 为什么 Agent 必须理解这一点？

对于普通聊天，知道“模型是逐 token 生成”可能只是基础知识；对于 Agent，它会直接决定系统行为。

原因在于 Agent 的决策、工具调用、计划和最终回答，最终都必须通过自回归生成过程被表达出来。

例如一个 Agent 面对：

```text
帮我查一下北京明天的天气，并告诉我是否适合跑步。
```

模型并不是先在内部完整决定：

```text
1. 调天气工具
2. 参数 city=Beijing
3. 获取结果
4. 判断是否适合跑步
5. 输出答案
```

然后一次性把整个计划执行出来。

实际系统更接近：

```text
已有 Context
   ↓
LLM 自回归生成下一步决策
   ↓
产生 tool call
   ↓
Harness / Runtime 执行工具
   ↓
得到 Observation
   ↓
Observation 加回 Context
   ↓
LLM 在“新的 Context”上继续自回归生成
```

因此，Agent loop 可以理解成：

> **把 LLM 内部连续的 token-level 自回归生成，扩展成了跨越模型与环境的 action–observation 自回归循环。**

可以写成：

```text
Token generation
      ↓
Action decision
      ↓
Environment changes
      ↓
Observation
      ↓
New context
      ↓
Next generation
```

Observation 不是附加信息而已，它会改变下一步条件概率：

$$
P(a_{t+1}\mid c,a_{\le t},o_{\le t})
$$

其中 $a_t$ 可以理解为 Agent 的 action，$o_t$ 是环境返回的 observation。

这就是为什么 Tool Result、网页内容、文件内容、代码执行结果等，一旦被送回模型上下文，就可能显著改变 Agent 后续行为。

---

#### 1.1.3 最小生成机制

一次典型的 inference 可以简化为以下六步。

**第一步：Tokenization**

输入文本先被 tokenizer 转换成 token：

```text
"Agent can use tools"
        ↓
[token_1, token_2, token_3, ...]
```

模型实际处理的是 token ID，而不是人类意义上的“词”。

**第二步：Forward Pass**

当前上下文进入模型，模型计算最后一个位置对应的 logits：

```text
logits = [z1, z2, ..., zV]
```

其中 $V$ 是词表大小。

**第三步：Softmax**

logits 被转换为下一个 token 的概率分布：

$$
P(x_i)=\frac{e^{z_i}}{\sum_j e^{z_j}}
$$

**第四步：Decoding**

系统根据 decoding 策略选出一个 token。

例如 greedy decoding：

$$
x_t=\arg\max_x P(x\mid c,x_{<t})
$$

而 temperature、top-p 等策略会允许从多个候选 token 中采样。具体放在 1.4 节展开。

**第五步：Append**

选出的 token 被加入当前序列：

```text
context_t
   +
new token
   ↓
context_{t+1}
```

**第六步：Repeat**

模型基于新的上下文重新预测下一个 token，直到终止。

所以生成过程天然具有一个重要性质：

> **前面的输出会成为后面的输入。**

这正是很多 Agent failure mode 的来源。

---

#### 1.1.4 误差为什么会累积？

假设模型在某一步生成了一个错误事实：

```text
A = 17
```

后面的所有 token 都会在包含 `A = 17` 的上下文条件下继续生成。

即使模型原本有能力得出正确答案，后续条件分布也已经发生变化：

```text
正确前缀
   ↓
正确 continuation 概率较高

错误前缀
   ↓
模型开始尝试“把错误前缀解释通”
```

在 Agent 中问题更加明显，因为错误的不只是文字，还可能是：

```text
错误 Tool
错误参数
错误文件
错误搜索 query
错误计划
错误状态判断
错误 termination decision
```

例如：

```text
User Task
   ↓
模型错误选择 delete_file
   ↓
Environment 被真实修改
   ↓
新的 Observation
   ↓
后续推理已经建立在改变后的世界状态上
```

因此 Agent 的错误传播不仅是 **token-level error propagation**，还可能变成 **environment-level error propagation**。

这也是为什么后面必须学习：

- Tool validation
- Human approval
- Retry policy
- Checkpoint
- Recovery
- Verification
- Guardrails

它们本质上都在试图阻止自回归决策中的局部错误不断向后扩散。

---

#### 1.1.5 自回归生成不是“模型已经想好整段答案再打印出来”

这是一个非常常见的直觉误区。

错误理解：

```text
LLM
 ↓
内部先得到完整答案
 ↓
逐字打印
```

更准确的理解是：

```text
已有 prefix
 ↓
预测 next token
 ↓
prefix 发生变化
 ↓
再次预测 next token
 ↓
...
```

因此，后面的内容受到前面真实生成结果的条件约束。

这也意味着：

> **生成轨迹本身会影响之后的生成。**

例如同一个问题前几步如果走了两条不同 reasoning path：

```text
Prefix A              Prefix B
   ↓                      ↓
P(next token | A)     P(next token | B)
```

后面的概率分布通常已经不同。

这也是为什么 reasoning trajectory、candidate generation、branching、beam-like exploration、self-consistency、test-time search 等方法有意义：它们并不是简单地“让同一个答案多说几遍”，而是在探索不同的生成前缀和后续条件分布。

---

#### 1.1.6 Training 与 Inference：不要混淆 Teacher Forcing

训练时和推理时有一个重要区别。

训练阶段常见的是 **teacher forcing**：预测第 $t$ 个 token 时，前缀通常来自训练数据中的真实 token：

$$
P(x_t^{*}\mid x_{<t}^{*})
$$

而 inference 时，模型下一步看到的是**自己刚刚生成的 token**：

$$
P(\hat{x}_t\mid \hat{x}_{<t})
$$

因此推理阶段一旦前面生成偏离，后续模型面对的输入分布也会随之改变。

对 Agent 来说，这个差异被进一步放大，因为系统还会把真实环境返回的 observation 插入上下文：

```text
Model output
     ↓
Tool execution
     ↓
External observation
     ↓
Next model inference
```

因此 Agent inference 是一个不断由**模型输出 + 外部环境反馈**共同改变上下文的动态过程。

---

#### 1.1.7 自回归生成在 Agent 架构中的系统位置

可以把一个最小 Agent 写成：

```text
                  ┌────────────────────┐
                  │      Context       │
                  └─────────┬──────────┘
                            ↓
                  ┌────────────────────┐
                  │        LLM         │
                  │ autoregressive     │
                  │ generation         │
                  └─────────┬──────────┘
                            ↓
                    Decision / Action
                            ↓
                  ┌────────────────────┐
                  │ Harness / Runtime  │
                  └─────────┬──────────┘
                            ↓
                     Environment
                            ↓
                      Observation
                            │
                            └──────────→ Context
```

因此：

- **Autoregressive Generation** 是模型层的生成机制；
- **Agent Loop** 是模型与环境之间的决策循环；
- **Harness** 决定何时调用模型、给模型什么上下文、允许什么 action、何时停止；
- **Runtime** 真正执行 tool / code / filesystem 等操作。

这些概念不能混在一起。

---

#### 1.1.8 一个最小 Agent 例子

假设 Agent 有两个工具：

```text
search_web(query)
calculator(expression)
```

用户问：

```text
查一下某公司 2025 年营收，再计算同比增长率。
```

一次可能的执行轨迹：

```text
[Context 0]
User request
      ↓
LLM generation
      ↓
Action: search_web(...)
      ↓
Observation: 2025 revenue = ...
      ↓
[Context 1]
User request + search action + observation
      ↓
LLM generation
      ↓
Action: search_web(...2024...)
      ↓
Observation: 2024 revenue = ...
      ↓
[Context 2]
      ↓
LLM generation
      ↓
Action: calculator(...)
      ↓
Observation: growth = ...
      ↓
[Context 3]
      ↓
LLM generation
      ↓
Final answer
```

注意这里每一次模型调用都不是从零开始。

后一次决策取决于前面已经发生的：

- user request；
- model action；
- tool result；
- intermediate state。

这就是 Agent trajectory。

---

#### 1.1.9 Failure Modes

从自回归生成机制出发，最值得记住的 failure modes 有以下几类。

**1. Early-error propagation**

早期 reasoning / action 出错，后续不断建立在错误前缀上。

**2. Local plausibility ≠ global correctness**

模型每一步都只需要生成“当前条件下很合理”的下一个 token，但大量局部合理步骤拼起来，不保证整体任务一定正确完成。

这对于长链 Agent 特别重要：

```text
每一步看起来都合理
≠
最终任务完成
```

**3. Context contamination**

错误 observation、恶意网页文本、无关检索结果等进入上下文后，会影响之后的生成概率。

**4. Long-horizon drift**

随着轨迹变长，Agent 可能逐渐偏离原始目标或遗漏早期约束。

**5. Premature termination**

模型可能生成“任务已完成”的语言模式，但实际上必要步骤还没有执行。

**6. Repetition / Looping**

某些上下文状态可能反复诱导模型生成类似 action，形成工具调用循环或 reasoning loop。

这些问题后面分别会在 Context、Tool Use、Harness、Evaluation、Safety 等章节继续展开。

---

#### 1.1.10 工程上意味着什么？

理解自回归生成之后，可以得到几个非常重要的 Agent 工程原则。

**原则一：不能只验证最终答案。**

因为错误可能在 trajectory 中很早就发生，所以 Agent evaluation 往往需要同时看：

```text
Outcome
+
Trajectory
+
Tool Calls
+
Intermediate State
```

**原则二：高风险 Action 不能完全依赖下一 token 决策。**

例如删除文件、付款、发送邮件等，应在模型生成 action 后增加确定性校验或 human approval。

**原则三：Observation 的质量与可信度非常重要。**

外部 observation 会成为后续生成条件，因此 Tool Result、网页内容、Memory、RAG 文档都可能改变 Agent 行为。

**原则四：长任务需要 Harness 做显式控制。**

单纯让模型不断自由生成，容易出现 context growth、goal drift、loop、premature termination 等问题，因此需要：

- step limit；
- stop condition；
- context management；
- checkpoint；
- verification；
- retry / recovery。

**原则五：模型能力与 Agent 可靠性不是一回事。**

即使单次 next-token prediction 很强，也不能直接推出长轨迹 Agent 一定可靠。Agent 的最终表现还取决于 Harness、Tools、Environment、Context 和 Evaluation。

---

#### 1.1.11 与相邻概念的边界

| 概念 | 关注点 | 与 Autoregressive Generation 的关系 |
|---|---|---|
| Tokenization | 文本如何映射成 token | 自回归生成操作的基本单位 |
| Decoding | 如何从 next-token 分布中选择 token | 决定每一步实际走哪条生成路径 |
| Context Window | 当前预测最多能条件化多少信息 | 定义自回归生成能够直接看到的信息范围 |
| Structured Output | 输出需要满足什么结构 | 约束自回归序列的形式 |
| Function Calling | 用结构化序列表达工具调用意图 | 仍然由自回归模型生成 |
| Agent Loop | 模型如何反复决策并接收环境反馈 | 将自回归生成扩展到 action–observation 循环 |
| Harness | 如何控制模型、工具、上下文和循环 | 管理自回归模型在 Agent 中的使用方式 |

---

#### 1.1.12 面试掌握边界

这一节不需要把 Transformer 数学细节讲到训练课的程度，但至少应该能稳定回答下面几件事：

1. **什么叫 autoregressive generation？**  
   给定已有上下文，模型逐 token 预测下一个 token，并把已生成 token 作为后续预测条件。

2. **为什么整个序列概率能写成条件概率乘积？**  
   来自概率链式法则，自回归模型按照前缀对序列概率进行因子分解。

3. **模型是一开始就想好整段答案再打印吗？**  
   不是。真实生成结果会成为后续条件，因此不同前缀会改变之后的概率分布。

4. **为什么 Agent 容易出现误差累积？**  
   前面的 reasoning / action / observation 会进入之后的 context；错误前缀甚至会真实改变环境状态，从而影响整个后续 trajectory。

5. **自回归生成和 Agent loop 有什么关系？**  
   自回归生成发生在模型内部；Agent loop 则在更高层将模型生成的 action、环境 observation 和下一轮模型调用连接起来。

6. **这对 Agent 工程意味着什么？**  
   需要 verification、tool validation、context management、stop policy、checkpoint、recovery 等外部机制，而不能假设强模型自然会产生可靠的长轨迹。

如果面试官继续追问 logits、softmax、temperature、top-p、greedy decoding，则进入 **1.4 Sampling & Decoding**；如果追问模型到底能看到哪些历史内容，则进入 **1.3 Context Window**；如果追问 tool call 如何被表达和执行，则进入 **1.5–1.6 Structured Output / Function Calling**。

---

#### 1.1.13 本节一句话总结

> **LLM 每一步只是在当前上下文上预测下一个 token；Agent 则把这种逐步条件生成扩展为“生成决策 → 执行动作 → 接收环境反馈 → 更新上下文 → 再生成”的长程闭环，因此局部生成误差、上下文污染和环境副作用都可能沿 trajectory 累积。**

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
| I | 1. LLM Foundation for Agents | 进行中：1.1 已完成 |
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

下一步：继续 **I. Model & Decision Core → 1.2 Prompt / System Instruction**。