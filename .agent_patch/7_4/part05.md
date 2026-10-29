#### 7.4.66 与 7.9 Permission / Approval Policy 的边界

某条敏感信息进入 context：

```text
does not grant permission
```

模型知道一个 credential 存在：

```text
does not mean it may disclose or use it
```

模型看到一个 write tool：

```text
does not mean write is approved
```

因此必须保持：

\[
Visibility \neq Permission \neq Approval
\]

7.4 负责 visibility；7.9 负责 concrete side-effect authorization。

---

#### 7.4.67 与 7.10 Termination Policy 的边界

Context Policy 可以提供：

```text
remaining tasks
verification status
open questions
```

但：

```text
是否满足 terminal condition
```

由 7.10 负责。

否则 context builder 会逐渐变成另一个隐藏 orchestrator。

---

#### 7.4.68 与 7.11 Recovery Policy 的边界

7.4 可以发现：

```text
context stale
context incomplete
summary corrupted
required evidence missing
```

并触发：

```text
refresh / rehydrate / retrieve
```

但复杂 failure 后：

```text
rollback
checkpoint restore
alternative route
human escalation
```

属于 7.11 Recovery Policy。

---

#### 7.4.69 面试高频问题：Context 越长越好吗

**问：模型已经支持 1M context，为什么还要做 Context Policy？**

答：

> 大 context window 解决的是容量上限，不等于信息利用质量。Agent 的完整 runtime state 里包含大量无关、过期、重复甚至相互冲突的信息；直接全部塞进去会增加成本、延迟、attention dilution 和 stale-context 风险。成熟做法是把 state 与 context 分离，在每个 decision point 构建 minimum sufficient context，并保留 provenance、freshness 和 version。

---

#### 7.4.70 面试高频问题：为什么不直接把所有 Tool Result 放回模型

**问：Tool Result 越完整，不是越不容易漏信息吗？**

答：

> 原始结果应该保留，但不代表每轮都要原样进入 context。大日志、网页和 API payload 更适合保存为 artifact，再抽取当前决策需要的字段或片段，并保留指向原始证据的引用。这样既不丢 raw evidence，又避免 tool output flood。真正需要进一步检查时，再按需展开。

---

#### 7.4.71 面试高频问题：RAG 和 Context Policy 有什么区别

**问：已经有 RAG 了，Context Policy 还有什么用？**

答：

> RAG 主要解决从外部知识中“检索哪些候选证据”；Context Policy 解决这些候选证据以及当前状态、历史、memory、tool observation 最终“哪些进入本轮模型调用、以什么形式进入、放在哪里、是否需要刷新或压缩”。Retrieval 是候选生成，Context Policy 是 decision-time information assembly。

---

#### 7.4.72 面试高频问题：Context 和 Memory 有什么区别

**问：Agent 记住的信息不就是 context 吗？**

答：

> 不是。Memory 是持久化信息层，可以跨 step 或跨 run 存在；Context 是一次模型调用的临时决策视图。Memory 中的信息必须经过 relevance、freshness、scope、privacy 等检查后才能进入当前 context。一个长期 Agent 可以拥有远大于 context window 的 memory 和 runtime state。

---

#### 7.4.73 30 秒回答版本

如果面试官问：

> **Context Policy 是什么？**

可以回答：

> Context Policy 是 Agent Harness 用来决定“某一次模型调用到底应该看到什么”的运行时信息编排层。完整 Agent state 往往远大于模型上下文，因此不能把聊天历史、tool result、RAG、memory 全部 append。Context Policy 会先做 eligibility 和 scope 隔离，再按当前 decision 的 relevance、freshness、provenance 和成本选择信息，对大结果做结构化或按需压缩，最后形成带版本的 Context Snapshot。关键原则是 state 不等于 context、retrieval 不等于 context、memory 不等于 context，而且 more context is not always better；目标是 minimum sufficient context。

---

#### 7.4.74 设计检查表

设计一个 Agent Context Policy 时，至少检查：

- [ ] Runtime State 与 Model Context 是否明确分离？
- [ ] Context 是否围绕当前 decision point 构建？
- [ ] 是否先做 eligibility / isolation，再做 relevance？
- [ ] 是否保留 provenance、version 和 observed time？
- [ ] 动态信息是否有 freshness / invalidation 机制？
- [ ] Tool Result 是否经过 parse / normalize / extract，而非无脑 append？
- [ ] 大型结果是否保留 raw artifact 并按需展开？
- [ ] RAG evidence 是否经过去重、版本和来源检查？
- [ ] Memory 是否经过当前 relevance 与 temporal validity 检查？
- [ ] 当前 active plan 是否有 canonical representation？
- [ ] proposed / executed / verified 是否被区分？
- [ ] compression 是否保留精确标识、约束、冲突和 unresolved state？
- [ ] 是否避免 summary-of-summary drift？
- [ ] 关键内容是否避免 lost-in-the-middle？
- [ ] external data 是否保持来源边界？
- [ ] 是否有 context refresh / cache invalidation？
- [ ] subagent 是否只获得 need-to-know projection？
- [ ] 是否记录 Context Snapshot 与 state / policy version？
- [ ] evaluation 是否测 stale、pollution、leakage 和 compression fidelity？
- [ ] debug 时能否重建“模型当时到底看到了什么”？

---

#### 7.4.75 长期稳定原则

这一节可以压缩成十条长期原则：

1. **Context is a runtime view, not the entire state.**
2. **State can be much larger than the model context.**
3. **More context is not always better; optimize minimum sufficient context.**
4. **Eligibility and isolation come before relevance ranking.**
5. **Visibility does not create authority, permission, or approval.**
6. **Raw observations should be preserved, but only decision-relevant representations need to enter context.**
7. **Freshness, provenance, version and contradiction are first-class context properties.**
8. **Compression must preserve decision-critical invariants, not merely shorten text.**
9. **Long-running agents should rebuild context from canonical state instead of blindly appending history forever.**
10. **Every important model decision should be traceable to a versioned Context Snapshot.**

如果只记住一句话：

> **Context Policy 的目标不是让模型“看到尽可能多”，而是让模型在当前决策点“看到足够正确、足够新鲜、来源清楚且真正有用的信息”。**

---

#### 7.4.76 参考资料

1. Liu N. F., Lin K., Hewitt J., Paranjape A., Bevilacqua M., Petroni F., Liang P. **Lost in the Middle: How Language Models Use Long Contexts**. *Transactions of the Association for Computational Linguistics*, 2024.  
   说明长上下文中的信息位置会影响模型利用效果，是理解“放进 context 不等于被有效使用”的经典依据。

2. Lewis P., Perez E., Piktus A., et al. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks**. *NeurIPS*, 2020.  
   奠定 retrieval-augmented generation 的经典范式；在 Agent 架构中应进一步把 retrieval 与 decision-time context assembly 区分开。

3. Yao S., Zhao J., Yu D., et al. **ReAct: Synergizing Reasoning and Acting in Language Models**. *ICLR*, 2023.  
   展示 reasoning、action 与 observation 交错的 Agent loop，帮助理解 observation 如何成为后续决策上下文的一部分。

4. Park J. S., O'Brien J., Cai C. J., Morris M. R., Liang P., Bernstein M. S. **Generative Agents: Interactive Simulacra of Human Behavior**. *UIST*, 2023.  
   展示长期 memory、retrieval 与 reflection 在 Agent 中的组合，可用于理解“持久 memory”与“当前 context”之间的选择关系。

5. Packer C., Fang V., Patil S. G., Lin K., Wooders S., Gonzalez J. E. **MemGPT: Towards LLMs as Operating Systems**. arXiv:2310.08560, 2023.  
   以分层 memory / context management 的方式讨论有限 context 下的长期运行，为“working context 与外部状态分离”提供直观工程视角。

---
