#### 7.4.51 推荐的 Context Builder 伪代码

```python
def build_context(run_state, decision, budget):
    candidates = collect_candidates(run_state, decision)

    eligible = [
        x for x in candidates
        if allowed_for_context(x, decision)
    ]

    valid = [
        x for x in eligible
        if not stale_or_revoked(x, run_state)
    ]

    ranked = rank_by_decision_utility(valid, decision)

    selected = allocate_budget(
        ranked,
        reserved={
            "policy": True,
            "goal": True,
            "current_state": True,
        },
        total=budget,
    )

    represented = [
        choose_representation(x, decision)
        for x in selected
    ]

    snapshot = order_and_package(
        represented,
        state_version=run_state.version,
        policy_version=run_state.policy.version,
    )

    return snapshot
```

这里最重要的不是具体算法，而是 pipeline 顺序：

```text
collect
→ eligibility
→ validity
→ rank
→ budget
→ represent
→ order
→ snapshot
```

---

#### 7.4.52 不要让模型独自承担 Context Management

可以让模型帮助判断：

```text
哪些证据可能相关？
这个日志哪些部分值得展开？
哪些历史应该摘要？
```

但不应把所有职责都交给模型。

特别是：

- privacy boundary；
- authority metadata；
- revoked information；
- hard token budget；
- cross-user isolation；
- access control；

应由 Harness / data layer 强制。

原则仍然是：

> **模型可以参与语义选择，但系统必须维护硬边界。**

---

#### 7.4.53 Context Policy 的典型 Failure Modes

| Failure Mode | 表现 | 根因 |
|---|---|---|
| Context Overflow | 超限或频繁截断 | 无预算管理 |
| Context Pollution | 无关信息持续进入 | 只 append 不选择 |
| Stale Context | 使用旧文件/旧状态 | 无 freshness / invalidation |
| Lost Critical State | 关键约束被压缩掉 | summary 设计错误 |
| Provenance Collapse | 无法区分来源 | 扁平字符串拼接 |
| Retrieval Flood | top-k 结果全塞入 | retrieval 与 context 未分层 |
| Summary Drift | 越总结越偏 | summary-of-summary |
| Plan Resurrection | 模型回到旧 plan | 无 canonical active plan |
| Tool Log Flood | 巨量日志占窗口 | raw result 直接注入 |
| Cross-Scope Leakage | 子任务看到不该看的数据 | 无 projection / isolation |
| Contradiction Flattening | 冲突证据被摘要成假共识 | compression 过度 |
| Cache Staleness | 复用过期 prefix | invalidation 设计缺失 |

这些 failure mode 很多最终表现为“模型推理差”，但根因其实在 Harness 的 context engineering。

---

#### 7.4.54 Context Policy 应如何测试

不能只做：

```text
最终答案 accuracy
```

至少应构造以下测试族：

**1. Relevance test**

加入大量无关历史，看关键决策是否稳定。

**2. Freshness test**

给出旧状态和新状态，确认旧状态不会继续主导。

**3. Supersession test**

明确更新 requirement，检查旧要求是否被移出 active view。

**4. Long-context test**

把关键证据放在不同位置，观察利用率。

**5. Tool-output test**

返回巨量日志，检查是否正确抽取关键错误。

**6. Retrieval-conflict test**

提供相互冲突、不同版本的文档。

**7. Memory-staleness test**

旧 memory 与当前事实冲突。

**8. Injection-containment test**

external content 中含有命令式文本。

**9. Subagent-isolation test**

确认 child 只得到需要的 context。

**10. Compression-fidelity test**

压缩前后关键状态和约束是否保持。

---

#### 7.4.55 推荐指标：不要只看 Token 数

可以记录：

| 指标 | 含义 |
|---|---|
| Context Tokens / Call | 每轮上下文成本 |
| Useful Evidence Recall | 必要证据是否被选入 |
| Irrelevant Context Rate | 无关内容比例 |
| Stale Item Rate | 过期内容进入比例 |
| Provenance Retention | 来源信息保留率 |
| Compression Fidelity | 压缩后关键事实保持程度 |
| Contradiction Preservation | 冲突是否被正确保留 |
| Refresh Latency | 状态变化到 context 更新的延迟 |
| Tool Output Reduction Ratio | 原始 tool output 到实际 context 的压缩率 |
| Context-Induced Error Rate | 因 context 选择/污染导致的错误 |
| Cross-Scope Leakage Rate | 越界暴露率 |
| Decision Quality per Context Token | 单位 context 成本下的决策质量 |

最后一个指标尤其值得关注：

> **更长 context 是否真的产生了更多 decision utility？**

---

#### 7.4.56 Observability：一次模型调用应该记录什么

建议最少记录：

```text
run_id
decision_id
context_snapshot_id

state_version
policy_version

included_item_ids
omitted_high-priority_items

token_count
compression_actions
retrieval_sources
memory_items
tool_observations

model_call_id
result
```

如果涉及动态资源，还应记录：

```text
resource_version
observed_at
```

这样才能回答：

> “这是模型能力问题，还是模型当时根本没有看到正确的信息？”

---

#### 7.4.57 Context Debugging 应先问四个问题

遇到错误决策时，推荐顺序：

```text
1. Missing?
   必要信息有没有进入？

2. Stale?
   进入的是不是旧版本？

3. Polluted?
   是否有无关/冲突内容干扰？

4. Misrepresented?
   信息是否在摘要、排序、格式化时被扭曲？
```

只有这四类问题基本排除后，再直接归因于：

```text
model reasoning failure
```

这样能避免把 Harness bug 全部算到模型头上。

---

#### 7.4.58 典型案例 A：网页研究 Agent

任务：

```text
比较两个软件库当前版本的 API 差异。
```

错误实现：

```text
搜索 20 个网页
→ 全文全部拼入 context
→ 模型总结
```

问题：

- 旧版本文档混入；
- SEO 页面和官方文档等权；
- 重复内容占满窗口；
- 不同版本信息相互污染。

更好的 pipeline：

```text
明确 target version
→ 优先官方 source
→ retrieve candidate pages
→ freshness / version filter
→ extract API-specific sections
→ preserve source + version
→ compare
```

Context Policy 在这里做的不是搜索本身，而是把搜索结果变成**可用于当前比较决策的 evidence set**。

---

#### 7.4.59 典型案例 B：Coding Agent

任务：

```text
修复一个单元测试失败。
```

运行过程中已有：

```text
repository: 20k files
test log: 80k lines
conversation: 40 turns
previous failed patches: 6
```

好的 Context Snapshot 可能只有：

```text
user goal
active constraints

failing test
current stack trace
target function
relevant interface
latest diff
last verifier result

previous attempts:
  - attempt 3 failed because ...
  - attempt 5 invalidated because ...
```

而不是：

```text
entire repo
+ entire logs
+ every previous patch
+ every conversation turn
```

这是 Context Policy 的典型价值：**保留因果链，丢掉历史噪声。**

---

#### 7.4.60 典型案例 C：长运行 Research Agent

一个 research run 持续几个小时，已经：

- 搜索 100 个来源；
- 阅读 40 篇文档；
- 形成 12 个中间结论；
- 推翻 4 个假设；
- 有 7 个未解决问题。

如果继续 append：

```text
模型会同时看到
old hypothesis
new hypothesis
rejected hypothesis
partial evidence
duplicated notes
```

更好的 state：

```text
Research State
├─ confirmed findings
├─ disputed findings
├─ rejected hypotheses
├─ unresolved questions
├─ source map
└─ evidence graph
```

然后不同 decision：

```text
search next source
write section
verify claim
resolve contradiction
```

各自获得不同 Context Snapshot。

---

#### 7.4.61 典型案例 D：Permission 改变后 Context 必须同步

用户先允许：

```text
可以修改 staging。
```

随后撤销：

```text
接下来只读，不要再改。
```

7.3 会更新 EffectivePolicy。

7.4 必须确保下一轮 context：

```text
active policy = read-only
```

而不是仍然同时展示：

```text
old write approval
+ new read-only
```

这里可以看到两节的边界：

```text
7.3:
哪条规则现在有效？

7.4:
如何让模型看到当前有效规则，而不是历史冲突堆栈？
```

---

#### 7.4.62 与 7.5 Tool Policy 的边界

7.4 负责：

```text
当前模型应该看到哪些 tool description / tool result？
tool result 应该如何压缩、刷新、进入 context？
```

7.5 负责：

```text
应该暴露哪些 tools？
如何选 tool？
参数如何验证？
tool call 如何执行？
失败如何处理？
```

所以：

```text
Context Policy
= information exposure

Tool Policy
= action capability governance
```

不要把 tool execution semantics 提前塞进 7.4。

---

#### 7.4.63 与 7.6 Memory Policy 的边界

7.4：

> **这一轮要不要把某条 memory 放进 context？**

7.6：

> **什么值得被记住、保存多久、如何写入、更新、遗忘和检索？**

因此：

```text
Memory Policy
→ manages persistent memory

Context Policy
→ decides current exposure
```

Memory 可以存在但不被当前模型看到。

---

#### 7.4.64 与 7.7 Planning Policy 的边界

7.4 负责给 planner / executor 提供：

```text
current goal
current state
relevant constraints
evidence
progress
```

7.7 负责：

```text
是否需要 plan
如何分解
何时 re-plan
plan 粒度
plan 更新
```

所以：

> **Context Policy supplies the decision view; Planning Policy decides the plan.**

---

#### 7.4.65 与 7.8 Subagent Policy 的边界

7.4 只规定：

```text
child context should be a projection
```

7.8 会进一步规定：

```text
when to delegate
what role to create
what authority to delegate
what budget to allocate
what return contract to require
how to merge results
```

因此不要把 subagent orchestration 混进 Context Policy。

---
