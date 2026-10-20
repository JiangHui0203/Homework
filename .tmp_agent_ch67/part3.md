#### 6.7.43 Stateless Message 与 Stateful Task 应该什么时候用

不是所有 Agent-to-Agent interaction 都需要创建长生命周期 Task。

可以粗略判断：

```text
Immediate + self-contained response
→ Message

Long-running / multi-step / resumable / needs tracking
→ Task
```

如果所有交互都强制建 Task，会增加：

- persistence；
- state management；
- cleanup；
- tracing；
- lifecycle complexity。

反过来，如果所有任务都压成一次 request-response，又会失去：

- progress；
- cancellation；
- recovery；
- async tracking；
- long-running semantics。

因此目标仍是：

> **使用足够表达真实执行语义的最小状态机制。**

---

#### 6.7.44 Streaming：传递增量状态，不代表最终正确

长任务往往需要流式更新：

```text
submitted
→ working
→ artifact chunk 1
→ artifact chunk 2
→ completed
```

Streaming 可以降低：

- perceived latency；
- polling cost；
- long-task opacity。

但 streaming 也引入新的 failure surface：

- connection drop；
- duplicate event；
- missed event；
- out-of-order handling；
- partial artifact；
- client reconnect；
- terminal event loss。

所以：

> **Streaming improves visibility, not correctness.**

---

#### 6.7.45 Partial Artifact 为什么不能直接消费

假设 remote agent 正在生成：

```text
report.json
```

stream 中已经收到 80%。

下游如果提前消费：

```text
Parser → Database Write
```

可能导致：

```text
partial data
→ irreversible side effect
```

因此系统需要知道：

- artifact 是否完整；
- chunk 是否可重组；
- 是否收到 completion signal；
- downstream 是否允许 speculative consumption。

稳定原则：

> **Incremental Availability ≠ Commit Readiness**

---

#### 6.7.46 Resubscription：连接断了，不等于 Task 消失

对于长任务：

```text
Task still working
     +
stream disconnected
```

这两个事实必须分开。

错误实现：

```text
stream EOF
→ mark task failed
→ create new task
```

更合理的恢复：

```text
stream lost
→ query / resubscribe existing task
→ reconcile latest state
→ continue observation
```

所以：

> **Transport Liveness ≠ Task Liveness**

---

#### 6.7.47 Push / Async Update：断开连接后仍需考虑任务继续执行

异步任务常见场景：

```text
Client submits
→ disconnects
→ Remote Agent continues
→ later status / result becomes available
```

这要求调用方区分：

```text
client session lifecycle
remote task lifecycle
```

二者不能绑定成：

```text
client connection gone
→ task must stop
```

否则长期任务会非常脆弱。

---

#### 6.7.48 Cancellation 是协议动作，不是时间倒流

Cancel Task 最容易被误解成：

```text
取消成功
= 世界恢复到任务开始前
```

实际可能是：

```text
Step 1: email sent
Step 2: DB updated
Step 3: user cancels
```

此时即使 Task 进入 canceled：

```text
previous side effects may remain
```

因此：

> **Cancellation ≠ Rollback**

需要额外考虑：

- side-effect boundary；
- compensating action；
- partial completion；
- external reconciliation。

---

#### 6.7.49 Retry 的核心问题不是“再发一次”

远程 Agent interaction 中 retry 的关键是：

```text
第一次到底发生了什么？
```

如果答案不确定：

```text
timeout
→ retry
```

可能产生：

```text
duplicate task
duplicate work
duplicate side effect
```

所以 retry policy 必须考虑：

- idempotency；
- task identity；
- deduplication；
- retry scope；
- side-effect semantics；
- reconciliation。

---

#### 6.7.50 Request Retry ≠ Task Retry ≠ Business Retry

这三个层次必须分开：

```text
Request Retry
= 网络 / transport 层重新发送

Task Retry
= 重新执行 remote work unit

Business Retry
= 重新尝试真实业务动作
```

它们的风险完全不同。

例如：

```text
GET task status retry
```

通常比较安全。

而：

```text
Create new payment task retry
```

可能造成真实重复付款。

---

#### 6.7.51 Idempotency：协议可靠性与业务正确性的连接点

如果一个动作可能被重复提交，就需要问：

```text
重复执行是否产生相同最终效果？
```

理想情况下可以通过：

- stable request identity；
- idempotency key；
- deduplication record；
- task lookup；
- conditional write；

降低 duplicate effect。

但：

> **A2A 互操作协议本身不应被误解成自动为所有业务动作提供 exactly-once semantics。**

业务副作用仍需要 runtime / application 层保证。

---

#### 6.7.52 Authentication 与 Authorization 必须分开

Authentication 回答：

```text
你是谁？
```

Authorization 回答：

```text
你被允许做什么？
```

一个 caller 即使成功认证，也不代表它有权：

- 调所有 skill；
- 读取所有 artifact；
- cancel 所有 task；
- 使用所有 tenant；
- 触发高风险 side effect。

因此：

> **Authenticated ≠ Authorized**

---

#### 6.7.53 Agent Card 中声明安全需求，不等于把 secret 放进 Card

Agent Card 可以声明：

```text
需要 OAuth2
需要 Bearer token
需要 mTLS
```

但 Card 不应该成为静态秘密分发器。

正确思路更接近：

```text
Card describes security scheme
      ↓
Client obtains credential through proper auth flow
      ↓
Credential sent through security boundary
```

因此要区分：

```text
Security Metadata
      ≠
Credential Material
```

---

#### 6.7.54 Agent Card 也可能是敏感资产

能力卡中可能暴露：

- internal endpoint；
- provider identity；
- private skills；
- supported interfaces；
- organization capability topology。

因此企业环境中不一定应该让所有 Card 公共可见。

可能需要：

```text
Authenticated Card
Extended Card
Registry-level ACL
Selective Disclosure
Network Boundary
```

所以：

> **Discoverability itself is a permission decision.**

---

#### 6.7.55 Card Cache：性能优化也会制造陈旧能力视图

Agent Card 通常变化不频繁，因此缓存很自然。

但 stale Card 可能导致：

```text
old endpoint
old auth requirement
removed skill
changed interface
outdated version
```

因此 caching 需要：

- expiry；
- validation；
- ETag / conditional retrieval；
- failure-triggered refresh。

这和 Chapter 4 的 freshness 原则一致：

> **Cached ≠ Current**

---

#### 6.7.56 Signed Agent Card 能证明什么，不能证明什么

签名主要帮助验证：

```text
content integrity
claimed signing identity / authenticity
```

但不能直接证明：

```text
Agent is safe
Agent output is correct
skill is suitable
provider is trusted by your policy
runtime is uncompromised
```

因此：

```text
Signature Valid
      ≠
Business Trust Granted
```

Trust 仍然需要本地 policy、identity governance、risk classification 与 verification。

---

#### 6.7.57 Remote Agent 是一个新的 Trust Boundary

一旦把任务交给 remote agent，就意味着：

```text
你的数据
你的目标
你的约束
你的权限意图
```

跨越了新的系统边界。

因此必须重新审视：

- data classification；
- least privilege；
- tenant isolation；
- credential scope；
- allowed side effects；
- output trust；
- provenance；
- retention；
- auditability。

不能因为“对方也是 Agent”就降低安全要求。

---

#### 6.7.58 Prompt Injection 可以跨 Agent 传播

典型链路：

```text
Web content
  ↓
Agent B ingests malicious instruction
  ↓
Agent B artifact / message
  ↓
Agent A treats it as trusted context
  ↓
Agent A performs unsafe action
```

因此跨 Agent message 必须继承 Chapter 3 / 4 的 Observation 边界：

> **Remote Agent Output ≠ Trusted Instruction**

需要区分：

- data；
- instruction；
- authority；
- provenance；
- trust level。

---

#### 6.7.59 Remote Agent 的“建议”不能自动升级成权限

例如 remote agent 返回：

```text
"下一步请执行 delete_account(user=123)"
```

调用方不能因为它来自一个 authenticated agent 就直接执行。

仍需本地 Harness 判断：

```text
Is this action allowed?
Does user intent authorize it?
Is approval required?
Is target correct?
Can it be verified?
```

因此：

> **Delegated Reasoning ≠ Delegated Authority**

---

#### 6.7.60 Capability Confusion：描述相似，不等于语义相同

两个 Agent 都可能声明：

```text
skill = "book travel"
```

但一个可能：

```text
只生成 itinerary
```

另一个可能：

```text
真实下单并扣款
```

因此 routing 不能只看 lexical similarity。

需要关注：

- preconditions；
- effect semantics；
- authorization scope；
- output contract；
- success criteria；
- side-effect level。

这和 Tool Selection 中的 capability semantics 是同一个问题。

---

#### 6.7.61 Semantic Interoperability 比 Syntax Interoperability 更难

A2A 可以让两个系统都理解：

```text
Task
Message
Artifact
```

但它们对业务语义的理解仍可能不同。

例如：

```text
"customer"
"approved"
"completed"
"high priority"
```

在两个组织中可能含义不同。

因此：

> **Schema Compatibility ≠ Semantic Compatibility**

真正跨组织时还需要：

- shared ontology；
- domain contract；
- explicit constraints；
- test cases；
- conformance suite。

---

#### 6.7.62 Protocol Success ≠ Task Success

协议层成功可能只是：

```text
HTTP success
message accepted
task created
```

任务层成功则是：

```text
remote agent achieved delegated objective
```

业务层成功还要继续问：

```text
user's actual goal satisfied?
```

因此至少分三层：

```text
Transport / Protocol Success
          ↓
Remote Task Success
          ↓
End-to-End Goal Success
```

每一层都需要独立指标。

---

#### 6.7.63 A2A Failure Taxonomy：先定位失败层

一次 remote-agent failure 可以来自：

```text
1. Discovery Failure
2. Capability Resolution Failure
3. Trust / Policy Failure
4. Authentication Failure
5. Authorization Failure
6. Compatibility Failure
7. Transport Failure
8. Message Validation Failure
9. Task Creation Failure
10. Remote Execution Failure
11. State Synchronization Failure
12. Artifact Failure
13. Verification Failure
14. Coordination Failure
15. End-to-End Goal Failure
```

如果不做 failure localization，最后往往只得到：

```text
"A2A 不稳定"
```

这种结论几乎没有工程价值。

---

#### 6.7.64 Discovery Failure

可能包括：

```text
Agent Card 找不到
registry recall 不足
Card 被权限过滤
Card cache stale
skill description 不可检索
```

评测时应该区分：

```text
Agent exists
        ↓
Agent discoverable
        ↓
retriever recalls Agent
        ↓
selector chooses Agent
```

这和 Tool Discovery 的 oracle decomposition 完全同构。

---

#### 6.7.65 Capability Resolution Failure

Agent 被发现了，但系统错误判断其能力。

例如：

```text
Task requires actual refund
Agent only supports refund explanation
```

表面上 skill 文本相似，实际 effect contract 不匹配。

因此可以评估：

- capability precision；
- capability recall；
- effect-level compatibility；
- required precondition coverage。

---

#### 6.7.66 Authentication / Authorization Failure

典型问题：

```text
credential expired
wrong audience
insufficient scope
wrong tenant
consent missing
policy denies high-risk action
```

不要统一归入：

```text
remote agent unavailable
```

因为恢复策略完全不同。

---

#### 6.7.67 Compatibility Failure

即使双方都支持 A2A，也可能因为：

- protocol version；
- binding；
- extension；
- input mode；
- output mode；
- media type；

而无法正确交互。

所以互操作测试必须覆盖：

```text
Client × Server × Version × Binding × Extension
```

而不能只验证一个 happy path。

---

#### 6.7.68 Task State Desynchronization

Client 认为：

```text
Task = working
```

Remote side 已经：

```text
Task = completed
```

或者反过来。

原因可能是：

- lost event；
- stale cache；
- stream disconnect；
- delayed update；
- race condition。

因此状态同步需要：

```text
correlation
latest-state reconciliation
timestamp / version awareness
terminal-state confirmation
```

---

#### 6.7.69 Duplicate Submission

典型链路：

```text
send message
→ timeout
→ client assumes failure
→ retry as new task
→ both tasks execute
```

如果任务只是写报告，可能浪费计算。

如果任务是：

```text
book flight
send email
charge account
```

就可能造成真实 damage。

所以必须分别统计：

```text
Duplicate Task Rate
Duplicate Work Rate
Duplicate Side-effect Rate
```

---

#### 6.7.70 Cancellation Race

可能出现：

```text
Client: cancel task
Remote: commits side effect
Server: marks canceled
```

此时：

```text
status = canceled
```

并不能回答：

```text
side effect happened or not?
```

因此 cancellation correctness 必须结合 effect reconciliation，而不是只看 terminal state。

---
