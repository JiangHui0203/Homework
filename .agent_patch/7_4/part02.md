#### 7.4.13 Working Set 与 Archive 应分层

长运行 Agent 不应把全部历史一直保持为 active context。

更合理的是：

```text
Archive / Event Log
        ↓
Persistent State
        ↓
Working Set
        ↓
Current Context Snapshot
```

例如：

```text
Archive:
完整 300 次 tool call

Persistent State:
已完成 42 个步骤、5 个 artifact、当前 branch、错误历史

Working Set:
当前子任务相关的 3 个文件、最近 2 个失败、当前 test result

Context Snapshot:
本轮 decision 真正需要的部分
```

这类似操作系统中的工作集思想：大部分状态可以存在，但不必全部驻留在模型窗口里。

---

#### 7.4.14 Context Budget 不是只有 Token Limit

常见错误：

```text
context budget = model max context length
```

实际至少有：

```text
token budget
latency budget
retrieval budget
tool-output budget
attention budget
privacy budget
freshness budget
monetary budget
```

即使模型支持极长 context，也不意味着应该把窗口填满。

大 context window 解决的是**容量上限**，不是**信息选择问题**。

---

#### 7.4.15 Token Budget 应按信息角色分配

可以给不同 context zone 设置预算，例如：

```text
EffectivePolicy       reserved
Current Goal          reserved
Current State         reserved
Recent Observation    dynamic
Retrieved Evidence    dynamic
Relevant History      dynamic
Memory                capped
Raw Tool Output       strongly capped
```

一种简单分配思路：

\[
B =
B_{policy}
+
B_{goal}
+
B_{state}
+
B_{evidence}
+
B_{history}
+
B_{scratch}
\]

其中高优先级关键状态应有最低保留额度，而不是让一个 50k-token tool output 把其他内容全部挤出去。

---

#### 7.4.16 Context Window 不是数据库

把 context window 当数据库会导致：

```text
“只要之前说过，模型就应该记得”
```

这是错误假设。

Context window：

- 没有可靠索引语义；
- 不保证任意位置都同等可访问；
- 不负责版本控制；
- 不负责一致性；
- 不负责权限；
- 不负责持久化；
- 不负责事实刷新。

所以：

> **需要可靠保存的状态，应进入 state store / memory / artifact；需要当前决策使用的部分，再由 Context Policy 投影回来。**

---

#### 7.4.17 Append-Only Context 是最常见的反模式之一

最朴素 Agent loop：

```text
messages.append(model_output)
messages.append(tool_result)
call_model(messages)
```

短任务可以工作。

长任务中会逐渐变成：

```text
old assumptions
+ obsolete plan
+ failed attempts
+ huge logs
+ repeated tool results
+ superseded user corrections
+ current task
```

问题不是单纯“超过 token limit”。

即使没有超限，也会出现**语义腐化**：

- 旧计划与新计划同时存在；
- 失败结果反复干扰；
- 已纠正事实仍残留；
- 重要信息被重复噪声淹没。

所以成熟 Agent 通常需要**stateful reconstruction**，而不是无限 append。

---

#### 7.4.18 Rebuild 优于 Blind Append

推荐模型：

```text
Raw event log
    ↓
State reducer
    ↓
Current canonical state
    ↓
Context builder
    ↓
Fresh snapshot
```

而不是：

```text
old prompt
+ new event
+ new event
+ new event
...
```

这并不意味着每轮都从零计算全部内容。

工程上可以使用缓存和增量更新，但**语义上 Context Snapshot 应代表当前状态，而不是历史字符串的机械累积**。

---

#### 7.4.19 Tool Result 不应自动成为下一轮 Prompt

7.2 已经强调：

```text
Tool Result ≠ automatically next prompt
```

7.4 进一步说明中间应该有：

```text
Raw Tool Result
      ↓
Parse
      ↓
Validate
      ↓
Normalize
      ↓
Extract decision-relevant fields
      ↓
Store raw artifact if needed
      ↓
Context representation
```

例如一个测试工具返回 30,000 行日志。

下一轮模型真正需要的可能只是：

```text
status: failed
failed_tests: 3
first_root_error: ...
artifact: full_log.txt
```

而不是整个日志。

---

#### 7.4.20 Large Tool Output 应采用“索引 + 局部展开”

推荐模式：

```text
Full Tool Output
      ↓
Artifact Store
      ↓
Index / Metadata
      ↓
Relevant Slice
      ↓
Context
```

例如：

```text
full_build_log.txt
size: 18 MB
errors:
  - lines 1202–1238
  - lines 9140–9190
```

模型先看到错误索引；只有需要进一步诊断时，再展开对应片段。

这样可以同时保留：

- raw evidence；
- 可追溯性；
- 较低 token 成本；
- 按需深入能力。

---

#### 7.4.21 RAG 解决“找什么”，Context Policy 解决“怎么进入本轮决策”

RAG 通常负责：

```text
query
→ retrieve
→ rank
→ return evidence
```

但 retrieval result 还不是最终 context。

Context Policy 还要决定：

- 是否当前真的需要这些结果；
- 是否新鲜；
- 是否重复；
- 是否相互冲突；
- 是否需要全文；
- 是否需要摘要；
- provenance 如何呈现；
- 排序如何安排；
- 占多少预算。

所以：

```text
Retrieval Policy
      ↓
candidate evidence

Context Policy
      ↓
decision-ready evidence
```

---

#### 7.4.22 Retrieval Score 不等于 Decision Utility

向量相似度高，只说明：

```text
embedding similarity is high
```

并不保证：

- 信息正确；
- 时间有效；
- 来源可信；
- 足以回答问题；
- 对当前 action 有帮助；
- 不与更权威证据冲突。

因此不能直接做：

```text
top-k similarity
→ concatenate
→ model
```

更稳健的是：

```text
retrieve
→ filter
→ deduplicate
→ freshness check
→ source check
→ coverage check
→ context assembly
```

---

#### 7.4.23 多份证据冲突时，不要先摘要成一个“假共识”

例如检索到：

```text
Doc A: API v2 uses field "name"
Doc B: API v3 uses field "display_name"
```

错误做法：

```text
summary:
API uses a name field.
```

这种摘要消除了最关键的 version conflict。

正确做法是保留：

```text
A:
version = v2
claim = name

B:
version = v3
claim = display_name

current target:
v3
```

Context compression 不应该抹掉**影响决策的分歧结构**。

---

#### 7.4.24 Memory 是候选来源，不是自动注入层

7.6 会专门讨论 Memory Policy。

在 7.4 只需要固定一个边界：

```text
Memory Store
   ≠
Current Context
```

Memory 中即使保存了某个事实，也要经过：

```text
relevance
freshness
scope
privacy
conflict
```

检查后才能进入当前 Context Snapshot。

因此：

> **Remembered does not mean currently relevant.**

---

#### 7.4.25 Memory 还需要 Temporal Validity

例如长期 memory 保存：

```text
用户当前项目使用 Python 3.11
```

几个月后项目升级到 Python 3.13。

如果 Context Policy 每次无条件注入旧 memory，就会产生：

```text
memory poisoning by staleness
```

因此 context builder 最好能识别：

```text
stable preference
temporary state
versioned project fact
time-sensitive external fact
```

并对不同类型采用不同 refresh 规则。

---

#### 7.4.26 Conversation History 也不应全部等权保留

历史对话里通常同时存在：

```text
current requirement
superseded requirement
brainstorming
rejected idea
temporary assumption
confirmed fact
social chatter
```

如果全部平铺，模型可能重新拾起已经否决的方案。

建议将历史转换为更明确的 state：

```text
active goals
confirmed constraints
resolved decisions
rejected alternatives
open questions
```

必要时仍可回看原始 transcript，但当前模型不必每轮看到全部原文。

---

#### 7.4.27 Plan 在 Context 中应呈现“当前有效版本”

如果 planner 已经从：

```text
Plan v1
```

更新到：

```text
Plan v3
```

Context 中不应该让三个版本以同等权重并列。

推荐：

```text
Active Plan: v3
Supersedes: v1, v2
Reason: test result invalidated step 2
```

历史 plan 可以留在 event log 中，但默认不进入 working context。

这能够降低：

```text
plan resurrection
```

即模型突然回到已经废弃的旧执行路径。

---

#### 7.4.28 Verification State 是高价值 Context

很多 Agent 失败不是因为没有结果，而是忘了“这个结果尚未被验证”。

因此 context 应区分：

```text
proposed
executed
observed
verified
committed
```

例如：

```text
patch_created = true
tests_passed = false
deployment_verified = false
```

比一句：

```text
“代码差不多修好了”
```

更适合作为后续 decision context。

Context Policy 应尽量让模型看到**状态机语义**，而不是模糊叙述。

---

#### 7.4.29 Compression 的目标不是“尽量短”

好的 compression 要回答：

> **删掉哪些信息不会改变当前决策？**

因此应优先保留：

- active constraints；
- unresolved questions；
- current state；
- failures；
- causal dependencies；
- evidence provenance；
- conflicts；
- versions；
- exact identifiers；
- required next actions；
- verification status。

而可以更激进压缩：

- 重复解释；
- 已完成且无后续依赖的细节；
- 大量成功日志；
- 无关闲聊；
- 已被 canonical state 吸收的旧表述。

---

#### 7.4.30 Lossless、Extractive、Abstractive 三层压缩

可以按风险分层。

**Level 1：Lossless normalization**

```text
去重复
去格式噪声
结构化字段
保留原值
```

**Level 2：Extractive compression**

```text
从原文抽取真正相关片段
```

**Level 3：Abstractive summarization**

```text
用新文本概括多个事件
```

越往后压缩率越高，但信息失真风险也越高。

因此关键状态通常优先：

```text
structured / extractive
```

而不是自由摘要。

---

#### 7.4.31 哪些信息不应该被自由摘要

以下内容应谨慎做 abstractive compression：

- 精确 API 参数；
- 文件路径；
- commit SHA；
- error code；
- permission state；
- numerical threshold；
- legal / policy wording；
- user explicit constraint；
- unresolved contradiction；
- approval scope；
- version identifier。

例如：

```text
允许修改 /tmp/a.txt
```

不能摘要成：

```text
用户允许修改文件。
```

因为 scope 被丢失了。

---
