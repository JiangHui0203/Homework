### 2.6 Verification

#### 2.6.1 定义：Verification 到底是什么？

前面的 Agent Loop、Planning、ReAct、Reflection 已经分别回答了：

```text
下一步怎么做？
未来怎样组织？
环境反馈怎样改变决策？
失败以后为什么错、该修哪里？
```

Verification 解决的是另一类问题：

> **我们有什么证据可以证明当前结果、状态或轨迹满足 Goal 与 Constraints？**

因此 Verification 不是“模型觉得自己做对了”，而是：

> **根据可观测 Evidence，对某个 Claim、Action Result、Intermediate State、Final Outcome 或 Constraint 是否成立进行检查，并产生可供控制系统使用的 Verdict。**

最小结构可以写成：

```text
Claim / State / Outcome
        ↓
Evidence
        ↓
Verifier
        ↓
Verdict
        ↓
PASS / FAIL / UNKNOWN
        ↓
Continue / Repair / Stop / Escalate
```

一个可靠 Agent 不应该只有：

```text
Action
→ model says done
→ STOP
```

而应该更接近：

```text
Action
→ Observe
→ Verify
→ if PASS: continue / finish
→ if FAIL: repair
→ if UNKNOWN: gather more evidence
```

所以一句话：

> **Verification 是把“我认为完成了”转换成“我有证据证明完成了”的机制。**

---

#### 2.6.2 为什么 Verification 是 Agent 可靠性的硬地基？

LLM 很容易生成语言上完整、语气上自信的完成声明：

```text
“文件已经创建。”
“邮件已经发送。”
“测试已经通过。”
“订单已经取消。”
```

但真实 Environment 可能是：

```text
文件根本不存在
邮件 API timeout
测试没运行
订单状态仍是 pending
```

如果系统把模型的自然语言声明直接当作 Ground Truth，就会出现：

```text
Self-report
→ mistaken as reality
→ premature termination
```

Verification 的作用就是打断这个错误链。

例如：

```text
Claim:
“测试已经通过”

Evidence:
pytest exit code = 0

Verifier:
exit_code == 0 ?

Verdict:
PASS
```

这里真正支持结论的是：

```text
Environment Evidence
```

而不是模型语言。

因此：

> **Agent Completion 应尽量由 Environment / Verifier 驱动，而不是由模型自我声明驱动。**

---

#### 2.6.3 Verification 的最小形式化表示

设 Goal 为 $g$，Constraints 为 $C$，当前 Environment / Agent State 为 $s$，可观测证据为 $e$。

Verifier 可以写成：

$$
V(g,C,s,e) \rightarrow y
$$

其中：

$$
y \in \{\text{PASS},\text{FAIL},\text{UNKNOWN}\}
$$

为什么最好保留 `UNKNOWN`？

因为现实中：

```text
没有证据证明成功
```

不一定等于：

```text
已经证明失败
```

例如：

```text
send_email() timeout
```

可能意味着：

```text
邮件没发出去
```

也可能：

```text
服务端已接收，只是客户端没收到响应
```

所以正确状态可能是：

```text
UNKNOWN
```

下一步应该：

```text
query delivery status
```

而不是盲目 resend。

因此：

> **Verification 应允许 epistemic uncertainty，而不是强迫所有状态立刻二分类。**

---

#### 2.6.4 Verification 和 Validation 有什么区别？

这两个词工程里经常混用，可以采用一个很实用的区分。

**Validation** 更偏向：

```text
输入 / Action 是否满足执行前的规则？
```

例如：

```text
JSON schema 合法吗？
amount 在范围内吗？
用户有权限吗？
参数类型对吗？
```

它发生在：

```text
before execution
```

**Verification** 更偏向：

```text
执行以后，目标 / 结果是否真的成立？
```

例如：

```text
订单真的 cancelled 了吗？
文件真的写入了吗？
测试真的 pass 了吗？
数据库值真的更新了吗？
```

所以可以记成：

```text
Validation
= Can / Should we do this?

Verification
= Did it actually work / Is the claim true?
```

例如：

```text
send_email
```

执行前：

```text
recipient format valid?
permission granted?
```

属于 Validation。

执行后：

```text
message accepted?
delivery status?
```

属于 Verification。

两者共同构成可靠 Action Pipeline。

---

#### 2.6.5 Verification 与 Reflection 的根本区别

上一节已经建立：

```text
Verification
= detect / judge

Reflection
= diagnose / explain / guide repair
```

例如：

```text
Verifier:
FAIL — 2 tests failing
```

这已经足以说明：

```text
Goal 尚未完成
```

但它未必解释为什么。

Reflection 进一步做：

```text
两个 failure 都来自 empty-input fallback 被删除。
```

因此：

```text
Verifier
→ 提供 verdict / evidence

Reflection
→ 解释 evidence / root cause
```

Verification 可以完全 deterministic；Reflection 则往往需要更多推理。

更重要的是：

> **Reflection 的输出仍然要回到 Verification 才能闭环。**

即：

```text
FAIL
→ Reflect
→ Repair
→ Verify again
```

而不是：

```text
FAIL
→ Reflect
→ “看起来修好了”
→ STOP
```

---

#### 2.6.6 Verification、Evaluation、Grading 有什么区别？

三个词也经常混用。

一个实用区分是：

**Verification**

```text
某个明确 predicate 是否成立？
```

偏 binary / objective / executable。

**Grading**

```text
给结果分数 / 等级 / rubric label
```

例如：

```text
0–5
partial credit
pass / weak-pass / fail
```

**Evaluation**

是最宽的上位概念：

```text
任务结果
过程质量
成本
延迟
安全
可靠性
```

都可以属于 Evaluation。

所以概念上可以理解：

```text
Verification
⊂ Evaluation

Grading
⊂ Evaluation
```

但实际论文 / 产品命名不会总遵守这套严格边界。

---

#### 2.6.7 Verification 的证据层级

不同 Evidence 的可靠程度不同。

可以采用一个非常重要的优先级：

```text
Direct Environment State
        ↓
Executable Checker
        ↓
Deterministic Rule
        ↓
Structured External Evidence
        ↓
Independent Model / Judge
        ↓
Agent Self-report
```

一般原则：

> **如果更直接、更可执行的证据存在，就不要主动把问题降级成模型主观判断。**

例如用户要求：

```text
创建文件 report.md
```

最强 Evidence：

```text
filesystem.exists("report.md")
```

而不是：

```text
LLM judge:
“这个 Agent 看起来应该创建成功了。”
```

---

#### 2.6.8 Direct Environment-state Verification

Agent 与传统纯文本模型最大的区别之一是：

> **很多任务的 Ground Truth 存在于 Environment，而不是最终回答文本。**

例如：

```text
把会议改到周五 15:00，并邀请 Alice。
```

真正要验证的是：

```text
event.start == Friday 15:00
Alice in event.attendees
old duplicate event does not exist
unrelated events unchanged
```

可以形式化成三类 predicate：

```text
Required Predicates
Forbidden Predicates
Invariant Predicates
```

即：

$$
Success = \bigwedge_i R_i
\land
\bigwedge_j \neg F_j
\land
\bigwedge_k I_k
$$

其中：

- $R_i$：必须发生；
- $F_j$：禁止发生；
- $I_k$：必须保持不变。

这比只检查：

```text
目标动作完成了吗？
```

更可靠，因为 Agent 可能：

```text
完成目标
+
破坏了其他状态
```

所以：

> **Success Verification 必须同时检查目标状态和副作用边界。**

---

#### 2.6.9 State Diff 为什么特别适合 Agent Verification？

对于有副作用的任务，可以记录：

```text
State_before
State_after
```

再计算：

```text
State Diff
```

例如：

```text
Before:
order_17.status = pending
order_18.status = paid

After:
order_17.status = cancelled
order_18.status = paid
```

如果任务是取消 17：

```text
Required change:
order_17 → cancelled

Invariant:
order_18 unchanged
```

这让 Verification 不只是：

```text
desired change happened?
```

还包括：

```text
undesired changes happened?
```

所以 State Diff 对 database、calendar、filesystem、browser / SaaS、code-editing Agent 都很有价值。

---

#### 2.6.10 Executable Verification：能运行，就尽量运行

很多任务的正确性可以通过执行判断。

例如 Coding Agent：

```text
Patch
↓
Build / Compile
↓
Unit Tests
↓
Integration Tests
↓
Static Checks
↓
Verdict
```

SQL：

```text
Candidate Query
↓
Execute on test DB
↓
Compare result
```

数学 / symbolic task：

```text
candidate expression
↓
symbolic simplification / numeric check
```

API workflow：

```text
perform action
↓
query resulting state
```

这种 verifier 的优势是：

```text
objective
reproducible
auditable
cheap relative to human review
```

但仍要注意：

> **Checker coverage 不完整，不等于结果完整正确。**

例如：

```text
10 个测试全过
```

只能证明：

```text
通过了这 10 个测试
```

不能逻辑上推出：

```text
所有可能输入都正确
```

因此 verifier 本身也有 coverage 边界。

---

#### 2.6.11 Outcome Verification 与 Process Verification

Verification 不一定只发生在最终答案。

##### Outcome Verification

回答：

```text
最终任务完成了吗？
```

例如：

```text
tests pass?
order cancelled?
answer correct?
```

##### Process Verification

回答：

```text
中间步骤是否有效 / 合规 / 正确？
```

例如：

```text
Step 3 是否引用了真实证据？
这个 tool call 是否违反约束？
这个 intermediate state 是否已经偏离 Goal？
```

长程 Agent 中只做最终 outcome check 可能太晚。

如果第 2 步已经严重偏离：

```text
Step 2 wrong
→ 继续 20 steps
→ 最终 fail
```

过程 verifier 可以更早触发：

```text
detect
→ repair
→ save cost
```

所以：

> **Verification 可以是终点检查，也可以是 trajectory 中的在线控制信号。**

---

#### 2.6.12 Process Verifier 为什么不等于“监督完整 Chain-of-Thought”？

Process Verification 可以检查：

```text
action validity
evidence use
constraint compliance
intermediate state
subgoal completion
```

不一定要求取得或评价模型完整自然语言思维过程。

现代 Agent 更实用的对象往往是：

```text
structured step state
Action
Observation
Plan status
Verifier evidence
```

因此：

> **Process Verification 关注的是中间决策和状态是否可靠，不等于必须读取完整隐藏思维。**

---

#### 2.6.13 Completion Check 是 Verification 的特殊位置

Agent Loop 中一个非常关键的 verifier 是：

```text
success_check(state)
```

它决定：

```text
继续
or
终止
```

因此 Completion Check 应基于：

```text
Goal satisfied
Constraints satisfied
Required evidence present
No unresolved critical failure
No forbidden side effect
```

而不是：

```text
model says "done"
```

例如 Coding Agent：

```text
success =
all_required_tests_pass
AND
public_api_unchanged
AND
no_forbidden_files_modified
```

这比“模型觉得 patch 完成”可靠得多。

---

#### 2.6.14 Verification 的三个典型时机

Verification 可以发生在不同阶段。

##### Before Action

严格说更接近 validation / precondition check：

```text
这个 Action 现在是否允许 / 可执行？
```

##### After Action

```text
Action 实际产生了什么结果？
```

##### Before Termination

```text
是否真的满足最终 Success Criteria？
```

成熟 Agent 通常三者都会存在：

```text
Precondition Check
→ Execute
→ Postcondition Verification
→ Completion Verification
```

---

#### 2.6.15 Postcondition：Action 执行完，不代表 Action 成功

假设：

```text
Action:
write_file("report.md", content)
```

Runtime 返回：

```text
success
```

仍然可以进一步 verify：

```text
file exists?
content hash correct?
path correct?
```

因为 Runtime 的 `success` 可能只代表：

```text
API call returned without error
```

而不是：

```text
Goal-level postcondition satisfied
```

类似地：

```text
send_email() returned 200
```

也不必然等于：

```text
recipient actually received email
```

所以要区分：

```text
Execution Success
≠
Task Success
```

---

#### 2.6.16 Verification 必须和 Success Criteria 一起设计

如果 Goal 定义不清：

```text
“把这个分析做好”
```

Verifier 很难判断。

更好的任务定义会明确：

```text
必须回答三个问题
必须引用至少两个一手来源
数据截至某日期
不得修改源文件
最终输出 Markdown
```

于是 Verifier 可以逐项检查：

```text
criterion_1
criterion_2
criterion_3
...
```

因此：

> **可验证性不是任务结束时才补的功能，而应该在任务设计阶段就进入 Success Criteria。**

---

#### 2.6.17 Binary Verdict 不总够用

很多任务不是简单：

```text
PASS / FAIL
```

可以引入：

```text
PASS
FAIL
PARTIAL
UNKNOWN
BLOCKED
```

例如：

```text
Goal A satisfied
Goal B satisfied
Goal C blocked by permission
```

如果强行二分类成 FAIL，会丢失重要状态。

因此 verifier 输出最好是结构化对象：

```json
{
  "status": "partial",
  "checks": [
    {"criterion": "A", "status": "pass"},
    {"criterion": "B", "status": "pass"},
    {"criterion": "C", "status": "blocked"}
  ],
  "evidence": [],
  "retryable": false
}
```

这样 Harness 才能决定：

```text
repair?
ask user?
escalate?
terminate partial?
```

---

#### 2.6.18 Verification 的输出应该包含 Evidence

只有：

```text
FAIL
```

通常不足以支持后续 Reflection。

更好的输出是：

```json
{
  "status": "fail",
  "criterion": "tests_pass",
  "evidence": {
    "exit_code": 1,
    "failed_tests": ["test_empty_config"]
  }
}
```

这样 Reflection 可以基于事实诊断。

所以：

```text
Verdict
+
Evidence
```

比单独 verdict 更有价值。

进一步还可以包含：

```text
confidence
scope
source
freshness
retryable
severity
```

---

#### 2.6.19 Deterministic Verifier 优先原则

如果一个条件可以用稳定程序判断：

```text
file exists?
number equal?
test pass?
JSON valid?
state predicate true?
```

一般优先使用 deterministic verifier。

原因是：

```text
reproducible
cheap
low variance
auditable
versionable
```

例如：

```python
passed = actual_total == expected_total
```

通常比：

```text
让 LLM 判断两个数字是否看起来一致
```

更合理。

因此一个非常重要的设计原则是：

> **Do not use an LLM to judge what code can verify exactly.**

---

#### 2.6.20 Rule-based Verifier 的边界

规则适合：

```text
字段存在性
工具黑名单
预算限制
状态 predicate
格式要求
时间范围
禁止副作用
```

但规则也可能：

```text
coverage 不全
边界条件遗漏
维护复杂
```

所以规则系统最好允许：

```text
PASS
FAIL
UNRESOLVED
```

而不是：

```text
规则没发现问题
→ 自动认为完全正确
```

这与前面的 `UNKNOWN` 原则一致。

---

#### 2.6.21 LLM-as-a-Judge 什么时候有价值？

某些目标很难完全程序化，例如：

```text
回答是否真正满足用户意图？
总结是否遗漏关键论点？
解释是否清晰？
两个方案哪个更合适？
```

此时可以使用 LLM Judge。

它适合读取：

```text
rubric
candidate
reference / evidence
trajectory summary
```

然后输出结构化判断。

但要明确：

> **LLM Judge 是可扩展 evaluator，不是天然 Ground Truth。**

它可能存在：

```text
position bias
verbosity bias
self-preference / style bias
reasoning error
reference misuse
prompt sensitivity
```

所以 Judge 本身也必须：

```text
calibrate
benchmark
version
monitor
```

---

#### 2.6.22 LLM Judge 不应该覆盖更强 Evidence

假设代码测试已经显示：

```text
expected = 42
actual = 17
```

不应该再让 Judge 说：

```text
“整体思路不错，我给 8/10。”
```

来覆盖 deterministic failure。

更合理的 evaluator routing 是：

```text
Executable truth available?
→ use executable verifier

Otherwise deterministic rule available?
→ use rule

Otherwise structured evidence available?
→ use evidence-based grader

Otherwise open-ended quality judgment?
→ use LLM / Human judge
```

即：

> **Judge 是证据不足时的判断工具，不是替代强 Ground Truth 的万能层。**

---

#### 2.6.23 Reference-based 与 Reference-free Verification

某些任务有标准答案：

```text
candidate
vs
reference
```

叫 reference-based。

例如：

```text
数学答案
标准 SQL result
固定目标 state
```

另一些任务没有唯一答案：

```text
写研究综述
设计方案
解释概念
```

此时更适合：

```text
rubric
constraints
evidence
user intent
```

即 reference-free evaluation。

要注意：

> **没有 reference 不等于无法验证。**

可以验证：

```text
事实是否有证据
约束是否满足
状态是否正确
逻辑是否自洽
执行是否成功
```

---

#### 2.6.24 Verification 与 Grounding

如果 Agent 给出一个 factual claim：

```text
政策已于某日生效
```

Verification 可以检查：

```text
是否存在 primary source？
source 是否真的支持这个 claim？
date 是否一致？
source 是否最新？
```

所以 Research Agent 中常见：

```text
Claim
↓
Evidence Retrieval
↓
Claim–Evidence Alignment
↓
Verdict
```

这类 Verification 的核心不是：

```text
“文本像不像正确答案”
```

而是：

> **Claim 是否被足够可靠的 Evidence 支持。**

---

#### 2.6.25 Evidence Freshness 也是 Verification 条件

对于时效任务：

```text
当前价格
今天营业状态
最新法规
服务器当前状态
```

旧 Evidence 即使历史上正确，也不能证明现在正确。

因此 verifier 可能需要检查：

```text
source timestamp
observation timestamp
environment version
cache age
```

即：

```text
Correct evidence
+
Fresh enough
```

才足够。

所以：

> **Verification 不只关心证据内容，也关心证据是否仍适用于当前 State。**

---

#### 2.6.26 Independent Verification 为什么有时更可靠？

如果同一个模型：

```text
generate
→ judge own answer
```

可能保留原有错误假设。

因此可以引入不同信息路径：

```text
Generator
↓
Candidate

Independent Verifier
↑
Fresh Evidence / Tool / Rule
```

真正重要的不一定是“换一个模型”，而是：

> **让 verifier 获得相对独立、可区分的 Evidence。**

例如：

```text
代码由 LLM 生成
测试由真实 runtime 执行
```

就是强独立性。

而：

```text
LLM A 生成
LLM A 用相同上下文再判断
```

独立性较弱。

---

#### 2.6.27 Verification 与 Redundancy

有些高风险任务可以使用多个独立检查：

```text
schema check
+
business rule
+
environment query
+
human approval
```

这不是简单“多跑几个 Judge”，而是：

> **使用不同 failure modes 的 verifier 形成 defense in depth。**

例如转账：

```text
amount valid?
recipient verified?
permission allowed?
transaction state committed?
ledger consistent?
```

任何一层失败都不能直接宣告 SUCCESS。

---

#### 2.6.28 Verification 的 False Positive 与 False Negative

Verifier 自己也会犯错。

**False Positive**：

```text
实际失败
Verifier → PASS
```

这是最危险的，因为系统可能提前终止。

**False Negative**：

```text
实际成功
Verifier → FAIL
```

会导致：

```text
unnecessary retry
cost ↑
possible duplicate side effect
```

所以 verifier quality 不能只看 accuracy，还要看错误代价。

高风险 completion verifier 通常特别需要控制：

```text
False Positive Rate
```

---

#### 2.6.29 Verification Coverage

一个 verifier 可能在自己检查的维度上很准，但 coverage 很窄。

例如：

```text
unit tests pass
```

但没检查：

```text
performance regression
security issue
API compatibility
unrelated file modification
```

因此 Verification 应该区分：

```text
Verifier Accuracy
vs
Verification Coverage
```

前者问：

```text
我检查的条件判得准吗？
```

后者问：

```text
真正重要的条件我检查全了吗？
```

这两个维度必须分开。

---

#### 2.6.30 Verification Specification 也可能错

如果 Success Criteria 本身定义错了：

```text
Verifier perfectly passes wrong target
```

系统仍会失败。

例如用户要求：

```text
不改变 public API
```

但 verifier 只检查：

```text
tests pass
```

那么 Agent 完全可能：

```text
通过修改 API 让 tests pass
```

却被错误判为成功。

因此：

> **Verifier correctness 依赖 Verification Specification correctness。**

真正完整链路是：

```text
User Goal
↓
Success Criteria
↓
Verification Specification
↓
Verifier Implementation
↓
Evidence
↓
Verdict
```

每一层都可能出错。

---

#### 2.6.31 Verification 与 Reward Hacking

只要 Agent 能感知或推断 verifier 规则，就可能优化：

```text
how to pass verifier
```

而不是：

```text
how to truly satisfy user goal
```

例如：

```text
只修 visible tests
硬编码 benchmark-specific pattern
生成能骗 Judge 的冗长文本
修改 evaluator input
```

因此 verifier 设计需要考虑：

```text
hidden checks
independent state
adversarial cases
invariants
out-of-distribution validation
```

但最根本的原则仍是：

> **Verifier 应尽量读取真实任务状态，而不是容易被 Agent 操控的代理指标。**

---

#### 2.6.32 Verifier Leakage

如果 Agent 可以直接看到：

```text
hidden expected output
hidden tests
judge rationale
```

它可能不是“完成任务”，而是：

```text
reverse-engineer evaluator
```

所以评测系统需要区分：

```text
Task Information
vs
Evaluation-only Information
```

在 benchmark / training pipeline 中尤其重要。

---

#### 2.6.33 Verification Cost 也需要预算

Verifier 不是免费的。

可能需要：

```text
another model call
run tests
query DB
browser check
external API
human review
```

所以不是每一步都应该运行最昂贵 verifier。

可以采用：

```text
cheap checks first
↓
expensive checks on uncertainty / risk
↓
human escalation when necessary
```

即：

```text
Verification Cascade
```

例如：

```text
schema
→ deterministic rules
→ executable test
→ LLM judge
→ human
```

越往后成本越高，只在必要时升级。

---

#### 2.6.34 Risk-aware Verification

不同 Action 的 Verification 强度应该不同。

低风险：

```text
read-only search
```

可能只需基本结果检查。

高风险：

```text
money transfer
send external email
delete file
production deploy
```

需要更强：

```text
precondition validation
human approval
postcondition verification
state reconciliation
audit log
```

因此 Verification Policy 应与：

```text
risk
irreversibility
cost of false positive
```

绑定。

---

#### 2.6.35 Verification-driven Agent Loop

把前面的概念放在一起：

```python
state = initialize(task)

while True:
    observation = observe(state)
    state = update_state(state, observation)

    completion = verify_completion(state)

    if completion.status == "pass":
        return finalize(state)

    if completion.status == "unknown":
        action = gather_missing_evidence(completion)
        state = execute_and_record(state, action)
        continue

    proposal = policy(build_context(state))
    action = validate(proposal)
    result = execute(action)
    state = record(state, action, result)

    post = verify_postcondition(state, action)

    if post.status == "fail":
        critique = reflect(post.evidence, state)
        state = repair(state, critique)
```

这里最关键的是：

```text
Verification
不是最后一行
```

而是可以贯穿：

```text
before action
post action
before termination
```

整个 Agent Loop。

---

#### 2.6.36 Research Agent 示例

任务：

```text
判断某政策今天是否已正式生效，并提供证据。
```

Agent 找到一篇新闻：

```text
Article says policy approved
```

但 Verification Specification 是：

```text
official primary source present
AND
effective date confirmed
AND
effective date <= today
```

当前 verifier：

```text
primary_source = false
```

所以：

```text
Verdict = UNKNOWN / FAIL-EVIDENCE
```

Agent 不应该结束，而应继续：

```text
search official gazette
→ open regulation
→ inspect effective date
```

最终所有条件满足，才允许输出最终结论。

这里 Verification 实际上定义了 Research Agent 的 stopping rule。

---

#### 2.6.37 Coding Agent 示例

任务：

```text
修复 bug，不改变 public API。
```

Agent 修改后：

```text
unit tests = pass
```

如果 verifier 只检查测试：

```text
PASS
```

可能不够。

完整 verification 可以是：

```text
required tests pass
AND
public API diff == none
AND
forbidden files unchanged
AND
build succeeds
```

所以：

```text
Tests Pass
≠
Task Complete
```

SWE-style software engineering 任务之所以强调真实 repository、执行环境和测试 harness，本质上就是把代码能力评价尽量落在可执行 Evidence 上，而不是只判断 patch 文本是否“看起来正确”。

---

#### 2.6.38 常见 Failure Modes

**1. Self-report as Ground Truth**：模型说完成就停止。

**2. No Postcondition Check**：Action 返回 success 就默认目标已实现。

**3. Weak Success Criteria**：只检查部分目标。

**4. Missing Invariants**：目标完成，但破坏无关状态。

**5. Stale Evidence**：用旧 Observation 验证新状态。

**6. Judge over Deterministic Truth**：明明可以程序验证，却交给 LLM 主观判断。

**7. Verifier False Positive**：失败状态被判 PASS。

**8. Verifier False Negative**：成功状态被判 FAIL，导致无意义 retry。

**9. Coverage Blind Spot**：Verifier 很准，但没检查真正重要的维度。

**10. Wrong Verification Spec**：判分标准本身和用户 Goal 不一致。

**11. Evidence Leakage**：把 evaluator-only 信息暴露给 Agent。

**12. Reward / Verifier Hacking**：Agent 学会过 verifier 而不是完成任务。

**13. Unbounded Verification**：每步都调用昂贵 Judge / tests，成本失控。

**14. Coupled Generator–Verifier Error**：Generator 和 Verifier 共享错误假设。

**15. Unknown Forced into Pass/Fail**：证据不足却被强行二分类。

**16. Verification without Evidence**：Judge 给 verdict，但无法指出支持事实。

**17. No Re-verification after Repair**：修完后不重新检查。

**18. Partial Success Collapsed to Failure**：无法区分部分完成、blocked、permission issue。

**19. Environment–Verifier Mismatch**：Verifier 检查的不是 Agent 真正操作的环境实例 / 版本。

**20. Non-idempotent Verification Action**：用于“检查状态”的操作本身改变环境。

---

#### 2.6.39 怎样评价 Verifier 本身？

Verifier 也必须被 Evaluation。

至少可以看：

```text
Accuracy
Precision / Recall
False Positive Rate
False Negative Rate
Coverage
Calibration
Robustness
Cost
Latency
Reproducibility
Inter-run Variance
```

对于 LLM Judge 还要看：

```text
human agreement
position bias
verbosity bias
prompt sensitivity
self-preference
reference sensitivity
```

对于 executable verifier 还要看：

```text
test coverage
flakiness
environment reproducibility
hidden dependency
```

所以：

> **Evaluator 本身也是系统组件，也需要版本化、回归测试和质量审计。**

---

#### 2.6.40 Verification Data 为什么特别有价值？

一条高价值 Agent trajectory 可以记录：

```text
Goal
Success Criteria
Action
Observation
Verifier Check
Evidence
Verdict
Repair
Re-verification
Final Outcome
```

这比只有：

```text
input
→ final answer
```

多出了非常关键的 supervision：

```text
什么时候发现失败？
哪个 criterion 失败？
什么 evidence 支持？
修复后是否通过？
```

这些数据可以用于 outcome reward、process reward、verifier training、failure attribution、recovery policy、hard-case mining、agent evaluation 与 self-improvement。

---

#### 2.6.41 Outcome Verifier 与 Process Verifier 的经典研究联系

在数学 reasoning 中，已有工作研究：

```text
Outcome supervision
vs
Process supervision
```

Outcome verifier 只判断最终答案；Process verifier 对中间步骤提供评价。

这一思想映射到 Agent 后非常自然：

```text
Outcome:
任务最终成功了吗？

Process:
中间 Tool / State / Subgoal / Constraint 是否正确？
```

但 Agent 比纯 reasoning 更复杂，因为中间 step 可能真实改变 Environment。

所以 Agent Process Verification 不只关心“推理逻辑”，还关心：

```text
Action validity
Observation grounding
state transition
side effect
permission
recovery
```

---

#### 2.6.42 Verification 与 Harness 的关系

Verifier 是判断组件；Harness 决定 Verification Policy：

```text
什么时候 verify？
verify 什么？
用哪个 verifier？
失败后怎么 route？
UNKNOWN 时怎么补证据？
高风险任务是否升级人工？
什么时候允许 STOP？
```

所以：

```text
Verifier
= 判断组件

Verification Policy
= Harness 控制策略
```

这和前面的：

```text
Tool
vs
Tool Policy
```

是同一种层级关系。

---

#### 2.6.43 Verification 与 Runtime 的关系

很多强 verifier 依赖 Runtime：

```text
run tests
query filesystem
execute SQL
inspect DB
open browser
read process state
```

所以 Runtime 提供：

```text
Evidence acquisition substrate
```

Verifier 则解释这些 evidence。

例如：

```text
Runtime:
pytest → exit code 1

Verifier:
required test suite failed
→ FAIL
```

不要把二者混成一个概念。

---

#### 2.6.44 Verification 的工程原则

1. **Environment evidence 优先于 self-report。**
2. **能 deterministic verify，就不要先用 LLM Judge。**
3. **Success Criteria 在任务开始前定义。**
4. **检查 Required、Forbidden 和 Invariant 三类 predicate。**
5. **Execution success 与 Task success 分开。**
6. **Verdict 最好带 Evidence，而不是只给标签。**
7. **允许 UNKNOWN / PARTIAL / BLOCKED。**
8. **Repair 后必须 Re-verify。**
9. **Verifier accuracy 与 coverage 分开评估。**
10. **高风险任务强化 postcondition 与 independent verification。**
11. **Verifier 本身必须版本化、审计和回归测试。**
12. **Verification cost 要进入 Budget。**
13. **避免 verifier leakage 和 reward hacking。**
14. **停止条件由可验证状态决定，而不是由模型语言决定。**
15. **Verifier 和 Verification Policy 分层：判断组件属于 evaluator，何时调用属于 Harness。**

---

#### 2.6.45 与相邻概念的边界

| 概念 | 核心问题 | 与 Verification 的关系 |
|---|---|---|
| Validation | Action 执行前是否合法 / 可执行？ | 偏 precondition；Verification 更偏 postcondition / truth check |
| Verification | Claim / State / Outcome 是否真的成立？ | 产生 Verdict + Evidence |
| Reflection | 为什么错、应该改哪里？ | 消费 Verification evidence 做诊断 |
| Evaluation | 系统整体表现如何？ | Verification 是其中一种评价机制 |
| Grader | 怎样给分 / label？ | 可比 verifier 更宽泛、更主观 |
| LLM Judge | 开放问题如何自动判断？ | Verification 的一种较弱 / 较主观实现 |
| Success Criteria | 什么状态算完成？ | Verification 的 specification 来源 |
| Completion Check | 是否允许结束？ | Verification 在 termination point 的应用 |
| Harness | 何时、如何、用哪个 verifier？ | 管 Verification Policy |
| Runtime | 怎样获取真实执行 evidence？ | 提供执行 / 查询 substrate |
| Environment | 真正任务状态在哪里？ | 最强 Ground Truth 来源之一 |

---

#### 2.6.46 面试掌握边界

至少应该能够稳定回答：

1. **Verification 是什么？**  
   根据 Evidence 判断某个 Claim、State、Action Result 或 Goal 是否真实成立，并输出可用于控制 Agent 的 Verdict。

2. **为什么 Agent 不能自己说“完成了”就结束？**  
   Self-report 不是 Environment Ground Truth；必须验证真实状态和 Success Criteria。

3. **Validation 和 Verification 区别？**  
   Validation 更偏执行前是否合法 / 可执行；Verification 更偏执行后是否真的满足结果。

4. **Verification 和 Reflection 区别？**  
   Verification 判断对错；Reflection 解释为什么错以及怎样修。

5. **什么是 Environment-state Verification？**  
   直接检查任务执行后的真实环境状态，而不是只检查自然语言输出。

6. **为什么 State Diff 有价值？**  
   同时检查目标变化和非目标副作用 / invariant。

7. **为什么 executable verifier 通常优于 LLM Judge？**  
   当问题可程序化时，前者更稳定、可复现、低方差且可审计。

8. **LLM Judge 什么时候有价值？**  
   开放式质量、用户意图、完整性等难以程序化的维度；但 Judge 本身不是 Ground Truth。

9. **Outcome Verification 和 Process Verification 区别？**  
   前者检查最终结果；后者检查中间步骤、状态、Action 或 Subgoal。

10. **为什么 verifier 要支持 UNKNOWN？**  
    缺乏成功证据不等于已证明失败；UNKNOWN 可以触发信息获取而不是错误 retry。

11. **Verifier Accuracy 和 Coverage 区别？**  
    Accuracy 看已检查条件判得准不准；Coverage 看真正重要的条件有没有被覆盖。

12. **什么是 verifier hacking？**  
    Agent 优化通过 evaluator 的代理规则，而不是满足真实用户 Goal。

13. **如何防止 verifier 成本过高？**  
    使用 cascade：cheap deterministic checks → executable checks → model judge → human escalation。

14. **Verification 和 Harness 什么关系？**  
    Verifier 负责判断；Harness 决定何时调用、选择哪个 verifier、失败 / UNKNOWN 后怎样处理。

15. **Verification 最核心的一句话是什么？**  
    Agent 不能靠“我觉得完成了”终止，而要用尽可能直接、可执行、独立的 Evidence 证明 Goal、Constraints 与 Environment State 确实满足。

如果继续追问“当存在多个模型 / tool / subagent / workflow 时，应该把任务交给谁、何时切换路径”，进入下一节 **2.7 Routing**。

---

#### 2.6.47 本节一句话总结

> **Verification 的本质，是把 Agent 的完成声明和真实世界状态之间建立一条可审计的证据链：先定义 Success Criteria，再优先从 Environment 与 Executable Checker 获取强 Evidence，由 Verifier 产生 PASS / FAIL / UNKNOWN 等 Verdict，并由 Harness 根据 Verdict 决定继续、补证据、修复还是终止；只有经过 Verification 的成功，才应该成为 Agent 可靠终止和后续 Self-Correction 的基础。**

#### 2.6.48 参考资料

- Cobbe K, Kosaraju V, Bavarian M, et al. **Training Verifiers to Solve Math Word Problems**. arXiv:2110.14168, 2021. 代表性地展示了生成候选后使用 verifier 排序 / 选择的思路。
- Lightman H, Kosaraju V, Burda Y, et al. **Let’s Verify Step by Step**. arXiv:2305.20050, 2023. 区分 outcome supervision 与 process supervision，并研究 step-level process reward / verification。
- Zheng L, Chiang W-L, Sheng Y, et al. **Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena**. NeurIPS 2023 Datasets and Benchmarks Track. 讨论 LLM Judge 的可扩展性以及 position、verbosity、自偏好等局限。
- Jimenez C E, Yang J, Wettig A, et al. **SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** ICLR 2024. 用真实 repository issue 与执行评测环境体现 executable task verification 在软件工程 Agent 评价中的价值。

### 2.7 Routing