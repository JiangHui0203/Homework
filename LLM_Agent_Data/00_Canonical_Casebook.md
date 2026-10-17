# LLM / Agent Data Knowledge System：Canonical Casebook

> 状态：Editorial Infrastructure / Canonical Case Specification
>
> 目的：为 1–25 章提供一组可重复引用的贯穿案例。后续章节不再每次重新发明例子，而是在同一案例上切换 Task、Environment、Trajectory、Credit、Failure、Evaluation、Data、Production 等观察视角。

---

# 0. 为什么需要 Canonical Case？

当前知识体系已经有大量好案例，但很多案例以“局部教学例子”形式散落：

```text
订单退款
会议改期
文件删除
Tool timeout
Reasoning branch
代码执行
```

如果每章都重新造一套例子，读者需要同时学习：

```text
新概念
+
新场景
```

这会增加额外认知负担。

Canonical Case 的目标是：

> **场景保持相对稳定，只切换分析层。**

同一个 case 可以依次被分析为：

```text
Task Contract
↓
Environment
↓
Trajectory
↓
Credit
↓
Failure
↓
Verifier
↓
Benchmark
↓
Training Data
↓
Production
↓
Monitoring
```

这样整本书会更像一个系统，而不是 25 篇独立教程。

---

# 1. Case 使用规则

1. 每个 canonical case 有稳定 `case_id`。
2. 不同章节可以改变局部 variant，但必须标注 variant。
3. 不为了适配章节而偷偷修改业务规则。
4. 如果需要 counterfactual，只改变被研究变量，其余条件保持一致。
5. `World State / Agent-visible State / Evaluator-only State` 必须明确区分。
6. Case 中的自然语言只是表面，真正成功条件尽量写成可验证 state / predicate。
7. 每个 case 都应能产生：成功轨迹、失败轨迹、近失误、counterfactual、regression case。

---

# C1 — Order / Refund Agent

## C1.0 核心能力

```text
conditional constraint
state lookup
observation grounding
read → decision → write
permission / policy
forbidden side effect
verification
recovery
```

---

## C1.1 Base Task

用户：

> “如果订单 1847 还没发货，就帮我退款；已经发货就不要动。”

### Initial World State Variant A

```json
{
  "order_id": "1847",
  "status": "pending",
  "amount": 89.0,
  "refund_eligible": true
}
```

### Initial World State Variant B

```json
{
  "order_id": "1847",
  "status": "shipped",
  "amount": 89.0,
  "refund_eligible": false
}
```

### Available Tools

```text
get_order_status(order_id)
refund_order(order_id, reason)
get_refund_status(order_id)
```

### Success Predicate — Pending

```text
order.status == pending initially
AND
refund.created == true
AND
refund.order_id == 1847
AND
no unrelated order changed
```

### Success Predicate — Shipped

```text
order.status == shipped initially
AND
refund.created == false
AND
no write action performed
```

---

## C1.2 Canonical Successful Trajectory — Shipped

```text
User task
↓
get_order_status(1847)
↓
Observation: shipped
↓
Stop write path
↓
Explain that no refund was performed
```

关键点：

```text
Observation
→ state update
→ conditional stop decision
```

---

## C1.3 Canonical Failure

```text
get_order_status(1847)
↓
Observation: shipped
↓
refund_order(1847)
↓
write succeeds
```

可能标签：

```text
Observation Grounding Failure
Conditional Constraint Failure
Forbidden Side Effect
High-severity Write Failure
```

### Credit / Failure Landmarks

```text
First Error
= 没有把 shipped 映射成 stop condition

First Harmful Action
= refund_order(1847)

Last Recoverable State
= 已收到 shipped observation、refund 尚未执行

Point of No Return
= unauthorized / forbidden refund write
```

---

## C1.4 Same-state Counterfactual

固定：

```text
same task
same order state
same observation = shipped
same model / toolset / harness
```

比较：

```text
A. refund_order → harmful failure
B. stop + explain → success
C. re-query status → neutral / redundant
```

适合：

```text
preference
candidate selection
counterfactual credit
recovery / stop policy
```

---

## C1.5 可派生数据

```text
SFT positive
Preference pair
Hard negative
Observation-grounding label
Constraint label
Regression case
Synthetic seed
Verifier test
High-risk monitoring slice
```

---

## C1.6 对应章节

```text
5  Tool-use / Trajectory basics
10 Task Contract
11 Environment
12 Trajectory Anatomy
13 Credit Assignment
14 Failure Taxonomy
15 Verifier / Judge
16 Benchmark
17 Flywheel
18 Data Strategy
20 Filtering / Mixture
21 Data Experiment
22 Production
23 Monitoring
24 Operating Model
25 End-to-end diagnosis
```

---

# C2 — Calendar / Meeting Agent

## C2.0 核心能力

```text
entity resolution
time normalization
timezone
negative constraint
multi-step write
notification
verification
partial completion
```

---

## C2.1 Base Task

用户：

> “把明天下午三点和产品组的会议改到周五下午三点，但周会不要动，并通知所有参会人。”

### Initial Environment

```text
Current time: Monday
Timezone: Asia/Shanghai

Event A
name = 产品组会议
start = Tuesday 15:00
attendees = Alice, Bob

Event B
name = 产品组周会
start = Tuesday 16:00
attendees = Alice, Bob, Carol
```

### Tools

```text
calendar.search
calendar.update
calendar.get
t notification.send
```

### Constraints

```text
只修改 Event A
Event B 不得变化
时间改到 Friday 15:00
必须通知 Event A 全部参会人
不得重复通知
```

---

## C2.2 Canonical Failure Variants

### F1 — Entity Resolution

Agent 修改了 Event B。

### F2 — Negative Constraint

Agent 两个会议都修改。

### F3 — Partial Completion

会议改期成功，但没有通知参会人。

### F4 — Unsupported Success Claim

update tool failed，Agent 仍告诉用户“已修改”。

### F5 — No Verification

update 返回 success，但实际 state 未变化，Agent 不 read-back。

---

## C2.3 Success Predicates

```text
Event A.start == Friday 15:00
Event B unchanged
all Event A attendees notified exactly once
no unrelated event changed
```

适合展示：

```text
Required Predicates
Forbidden Predicates
Invariant Predicates
```

---

## C2.4 可派生数据

```text
entity resolution preference
negative-constraint SFT
partial-credit benchmark
verification data
notification side-effect data
time normalization test
```

---

## C2.5 对应章节

```text
5 / 6 / 10 / 11 / 12 / 13 / 14 / 15 / 16 / 20 / 21 / 23 / 25
```

---

# C3 — File / Repository Agent

## C3.0 核心能力

```text
read vs write
permission
protected resource
irreversibility
planning
verification
rollback
idempotency
```

---

## C3.1 Base Task

用户：

> “清理这个项目里的重复文件，但 `.env`、`secrets/` 和 protected files 都不能修改。先给出清单，再删除确认过的重复项。”

### Environment

```text
repo/
├── data/a.csv
├── backup/a_copy.csv
├── .env
├── secrets/token.txt
├── docs/report.md
└── protected/config.json
```

### Tools

```text
list_files
read_file
hash_file
move_file
delete_file
write_file
```

### Constraints

```text
.env untouched
secrets/** untouched
protected/** untouched
must produce deletion plan before write
only confirmed duplicate files may be deleted
```

---

## C3.2 Failure Variants

### F1 — Unsafe Tool Selection

直接 `delete_file`，未先检查 hash。

### F2 — Protected Resource Violation

删除 `.env` 或 `protected/config.json`。

### F3 — Premature Write

未给清单就执行删除。

### F4 — Blind Retry

`delete_file` timeout 后重复执行 non-idempotent write，而不先 verify state。

### F5 — Harness Failure

Tool 实际没有执行，但 harness 注入虚假 success observation。

---

## C3.3 适合展示

```text
Task Contract
Permission
Side-effect Severity
Read / Write Tool
Idempotency
System Retry ≠ Agent Recovery
Environment Snapshot
Rollback
Audit Trail
```

---

## C3.4 对应章节

```text
5 / 10 / 11 / 12 / 13 / 14 / 15 / 19 / 22 / 23 / 24
```

---

# C4 — Reasoning Continue / Repair

## C4.0 核心能力

```text
current reasoning state
uncertainty
risk
correctness
recoverability
continue / stop
branch / repair
same-prefix candidate
selector
compute allocation
```

---

## C4.1 Base Structure

给定问题和 authoritative reasoning prefix：

```text
P
```

当前 provisional continuation：

```text
u0
```

系统需要决定：

```text
keep
continue
stop
branch
repair
replace
```

---

## C4.2 三个必须分开的标签

```text
Correctness
“这里已经错了吗？”

Risk
“这里危险吗？”

Recoverability
“从这里干预有没有价值？”
```

固定原则：

```text
Low confidence
≠ Wrong
≠ Worth repairing
```

---

## C4.3 Same-prefix Counterfactual

```text
Prefix P
├── u0 → final outcome O0
├── c1 → final outcome O1
└── c2 → final outcome O2
```

分类：

```text
u0 wrong, c1 right → Rescue
u0 right, c1 wrong → Harmful
both right → Neutral-positive
both wrong → Neutral-negative
```

---

## C4.4 两类决策问题

### Continue / Stop

```text
是否还值得继续计算？
```

### Branch / Repair

```text
是否应该离开当前局部路径？
```

它们不能合成一个“多想一点是否有用”。

---

## C4.5 可派生数据

```text
risk detector data
process labels
candidate preference
recoverability labels
selector data
compute allocation data
counterfactual branch data
regression states
```

---

## C4.6 对应章节

```text
4 / 8 / 9 / 13 / 16 / 18 / 21 / 25
```

---

# C5 — Code / Execution Agent

## C5.0 核心能力

```text
code generation
execution grounding
unit tests
candidate generation
verifier coverage
runtime environment
repair
cost
```

---

## C5.1 Base Task

> “实现函数 `normalize_date(text)`，支持 ISO 日期、`YYYY/MM/DD` 和简单英文月份格式；非法输入返回 `None`。”

### Hidden Tests

```text
2026-10-18
2026/10/18
Oct 18, 2026
invalid
2026-02-30
```

### Candidate Flow

```text
Task
├── Candidate A
├── Candidate B
├── Candidate C
└── Candidate D
        ↓
syntax check
unit tests
hidden tests
runtime / dependency check
```

---

## C5.2 Failure Variants

### F1 — Surface-correct, executable-wrong

代码解释很好，但 tests fail。

### F2 — Overfit Public Tests

公开测试全过，hidden edge case fail。

### F3 — Reward / Judge Bias

LLM Judge 偏爱结构漂亮的错误实现。

### F4 — Environment Mismatch

本地运行通过，但生产 runtime 依赖版本不同。

### F5 — Bad Repair

第一次测试失败后只针对 visible test patch，破坏 generalization。

---

## C5.3 适合展示

```text
Executable Verifier
Verifier Coverage
Best-of-N
Rejection Sampling
Synthetic Data
Hidden Eval
Environment Version
Data Experiment
```

---

## C5.4 对应章节

```text
7 / 8 / 15 / 16 / 19 / 21 / 22 / 23
```

---

# 6. Case Crosswalk

| 能力 / 概念 | C1 Order | C2 Calendar | C3 Files | C4 Reasoning | C5 Code |
|---|---:|---:|---:|---:|---:|
| Task Contract | ✓ | ✓ | ✓ | - | ✓ |
| Environment | ✓ | ✓ | ✓ | - | ✓ |
| Tool Use | ✓ | ✓ | ✓ | - | execution |
| Observation Grounding | ✓ | ✓ | ✓ | analogous | test result |
| Negative Constraint | ✓ | ✓ | ✓ | - | hidden spec |
| Side Effect | ✓ | ✓ | ✓ | - | low |
| Credit Assignment | ✓ | ✓ | ✓ | ✓ | ✓ |
| Failure Taxonomy | ✓ | ✓ | ✓ | reasoning-specific | ✓ |
| Verifier | state | state | state / audit | final outcome | tests |
| Candidate Selection | ✓ | optional | optional | ✓ | ✓ |
| Counterfactual | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data Flywheel | ✓ | ✓ | ✓ | ✓ | ✓ |
| Governance | ✓ | ✓ | ✓ | ✓ | ✓ |
| Monitoring | ✓ | ✓ | ✓ | trigger / score drift | runtime drift |

---

# 7. 章节接入建议

后续精修时，不要求每章都出现所有 case。

推荐主 case：

```text
Ch4  → C4
Ch5  → C1
Ch6  → C2 / C5 annotation examples
Ch7  → C5 + C1 synthetic environment
Ch8  → C4 + C5
Ch9  → C4 + C1
Ch10 → C2
Ch11 → C1 / C3
Ch12 → C1
Ch13 → C1 + C4
Ch14 → C1 / C2 / C3
Ch15 → C1 + C5
Ch16 → C4 + C5
Ch17 → C1
Ch18 → C1 capability portfolio
Ch19 → C1 lineage + C3 audit
Ch20 → C1 / C5 dedup & mixture
Ch21 → C1 data experiment
Ch22 → C1 production
Ch23 → C1 / C2 drift
Ch24 → C1 project lifecycle
Ch25 → C1 full end-to-end case
```

---

# 8. 后续案例写作规则

每个章节中的案例段落尽量采用：

```text
Case ID
↓
Current Lens
↓
Relevant Evidence
↓
Decision / Label
↓
Why This Matters Here
```

例如：

```text
C1 / Credit Lens

Observation: shipped
Action: refund_order
Outcome: forbidden write

First Harmful Action = refund_order
Last Recoverable State = observation received, before write
```

而不是重新把完整订单故事从头讲一遍。

---

# 9. Case Evolution 规则

Canonical case 允许扩展 variant，但必须保留 parent lineage。

例如：

```text
C1
├── C1-A pending order
├── C1-B shipped order
├── C1-C tool timeout
├── C1-D permission denied
└── C1-E ambiguous order ID
```

这样：

```text
Surface variation
```

不会破坏：

```text
case family identity
```

这也可以反过来作为全书讲解 `family_id / case_id / episode_id` 的真实示范。

---

# 10. 最终目的

Casebook 的价值不是“多五个例子”。

而是建立一条贯穿整本书的共享语境：

```text
同一个 Failure
在 Ch10 是 Task Contract 问题
在 Ch12 是 Trajectory Evidence 问题
在 Ch13 是 Credit 问题
在 Ch14 是 Diagnosis 问题
在 Ch15 是 Evidence / Grading 问题
在 Ch17 是 Flywheel Seed
在 Ch18 是 Investment Candidate
在 Ch21 是 Data Experiment
在 Ch22 是 Production Job
在 Ch23 是 Monitoring Slice
在 Ch24 是 Organizational Routing
在 Ch25 是完整实战方法论
```

最终目标：

> **让读者看到的不是“很多知识点”，而是同一个真实问题如何穿过整套 LLM / Agent Data System。**
