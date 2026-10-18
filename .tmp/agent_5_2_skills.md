### 5.2 Skills

#### 5.2.1 定义：Skill 到底是什么？

在 Agent 系统里，**Skill 是一种可复用、可调用、可版本化的任务完成方法（reusable task-solving procedure）**。它描述的不只是“调用哪个 Tool”，而是针对一类任务：应该如何理解目标、准备上下文、满足前置条件、组合能力、执行步骤、检查结果、处理失败并决定何时结束。

一个 Skill 可以概括为：

```text
Skill
=
Task Semantics
+
Procedure
+
Capability Dependencies
+
State / Context Contract
+
Safety Constraints
+
Verification Criteria
```

因此，Skill 的本质不是一个新的原子动作，而是**把一类反复出现的任务方法从临时推理中抽出来，变成可以稳定复用的能力单元**。

---

#### 5.2.2 为什么 Agent 需要 Skill？

如果没有 Skill，Agent 每次遇到类似任务，都可能从零开始重新规划：

```text
Task
↓
重新理解
↓
重新探索 Tool
↓
重新决定步骤
↓
重新发现边界条件
↓
重新踩相同的坑
```

Skill 把已经成熟的方法沉淀为：

```text
Repeated Task Pattern
        ↓
Validated Procedure
        ↓
Reusable Skill
```

它主要解决五类问题：

1. **重复推理成本**：相同任务不必每次重新发明流程；
2. **执行一致性**：关键步骤、验证和安全边界不容易遗漏；
3. **能力扩展**：Agent 可以通过增加 Skill 扩展“会做什么类型的任务”；
4. **可评测性**：Skill 可以独立测试、版本化、回归；
5. **知识沉淀**：经验不再只停留在临时 Memory 或人的脑子里。

---

#### 5.2.3 Skill 在整个 Agent 系统中的位置

可以把它放在 Tool 与 Agent 决策之间：

```text
Goal / State
    ↓
Agent Decision
    ↓
Skill Selection / Activation
    ↓
Skill Procedure
    ↓
Tool / Native Tool / MCP Tool / Workflow
    ↓
Environment
```

因此：

> **Tool 提供原子能力；Skill 提供完成一类任务的方法；Agent 决定当前是否应该使用这个方法。**

---

#### 5.2.4 Tool vs Skill

最重要的边界：

```text
Tool
= 能做什么动作？

Skill
= 怎样把一个或多个动作组织成可靠任务方法？
```

例如：

```text
Tool:
read_file(path)
write_file(path, content)
run_tests()
git_diff()
```

而 Skill 可以是：

```text
Skill: safe_code_patch
1. 读取相关文件
2. 定位最小修改范围
3. 修改
4. 运行目标测试
5. 运行回归测试
6. 检查 diff
7. 确认无无关改动
8. 报告证据
```

所以：

> **Skill 可以调用 Tool；Tool 不等于 Skill。**

---

#### 5.2.5 Skill vs Workflow

二者都可能描述多步骤任务，但控制语义不同。

```text
Workflow
= 显式定义控制流

Skill
= 可复用任务方法，可以包含固定步骤，也可以保留局部决策空间
```

例如：

```text
Workflow:
A → B → C → D
```

而 Skill 可能是：

```text
1. 先检查环境
2. 根据结果选择 A 或 B
3. 必须验证
4. 若失败则按错误类型恢复
```

所以 Skill 可以：

- 内部调用 Workflow；
- 被 Workflow 调用；
- 自己包含一定 Agentic Decision。

不要把两者硬做成互斥概念。

---

#### 5.2.6 Skill vs Prompt

Prompt 是模型当前推理时看到的文本或结构化 Instruction；Skill 是一个更完整的可复用能力单元。

```text
Prompt
= inference-time instruction/context

Skill
= procedure + dependencies + constraints + verification + lifecycle
```

一个 Skill 可能包含 Prompt 片段，但 Skill 不应该被简化为：

```text
skill.txt = 一大段提示词
```

否则版本、依赖、权限、结果验证和安全语义都会丢失。

---

#### 5.2.7 Skill vs Procedural Memory

这是本章很重要的边界。

```text
Procedural Memory
= “以后遇到类似情况，应该这样做”的经验

Skill
= 这条经验经过整理、结构化、验证后形成的可复用能力
```

例如：

```text
Procedural Memory:
修改配置前最好先验证 schema。
```

成熟以后可以升格为：

```text
Skill: safe_config_update
Precondition: schema available
Procedure:
  validate → preview diff → update → revalidate → verify
```

因此：

> **Procedural Memory 是 Skill Acquisition 的重要原材料，但未经验证的经验不应该自动升级成 Skill。**

---

#### 5.2.8 Skill vs Policy

Policy 回答：

```text
允许什么？
必须遵守什么？
什么时候需要审批？
```

Skill 回答：

```text
怎样完成这类任务？
```

例如：

```text
Skill:
部署服务

Policy:
Production 部署必须人工审批
```

Skill 不能通过自己的 Procedure 绕过 Policy。

因此：

> **Skill describes how; Policy constrains what is allowed.**

---

#### 5.2.9 Skill vs Agent

Agent 是持续做 Decision 的主体；Skill 是 Agent 可选择的一种能力。

```text
Agent
├── Decide
├── Select Skill
├── Select Tool
├── Replan
└── Stop

Skill
└── Reusable task procedure
```

一个 Skill 本身可以包含局部 Agentic Loop，但不要因为它能做复杂任务，就把 Skill 与 Agent 混成同义词。

---

#### 5.2.10 Skill vs Subagent

Subagent 通常意味着：

- 独立或半独立 Context；
- 独立 State / Loop；
- 独立 Tool Set；
- 可以产生自己的 trajectory。

Skill 则不要求这些。

```text
Skill
= 方法能力

Subagent
= 另一个执行主体
```

Agent 可以：

```text
activate skill
```

也可以：

```text
spawn subagent with skill X
```

两者是不同维度。

---

#### 5.2.11 Skill vs MCP

MCP 解决的是标准化能力暴露与连接；Skill 解决的是任务方法。

```text
MCP
= capability interoperability / transport / discovery layer

Skill
= reusable task procedure layer
```

一个 Skill 完全可以依赖 MCP Tool：

```text
Skill: publish_release
    ↓
MCP GitHub tools
    ↓
Repository
```

也可以完全不依赖 MCP。

---

#### 5.2.12 Skill Contract

一个成熟 Skill 不应只有名称和正文，还需要明确 Contract：

```text
Skill Contract
├── identity
├── purpose
├── applicability
├── inputs
├── outputs
├── preconditions
├── dependencies
├── state requirements
├── permissions
├── side effects
├── success criteria
├── failure semantics
└── version
```

Contract 决定了 Skill 是否能被安全选择、组合和评测。

---

#### 5.2.13 Skill Identity

Skill 至少应有稳定身份：

```text
skill_id
name
version
owner
```

不要只依赖自然语言标题。

因为：

```text
“代码修复”
```

可能未来有：

```text
safe_code_patch@1
safe_code_patch@2
production_hotfix@1
```

稳定 ID 才能支持 trace、版本和回归。

---

#### 5.2.14 Purpose 与 Applicability

好的 Skill 必须说明：

```text
什么时候应该使用？
什么时候不应该使用？
```

例如：

```text
Skill: safe_code_patch
Use when:
- 已有代码库
- 目标是局部修复

Do not use when:
- 需求是新建整个系统
- 用户只要求代码解释
```

这直接影响 Skill Activation Precision。

---

#### 5.2.15 Skill Input Contract

输入可以包括：

```text
Task Goal
Parameters
Current State
Artifact References
Environment Metadata
Constraints
```

输入定义越模糊，Skill 越容易把 Context 中的偶然内容当作参数。

所以成熟 Skill 应尽量区分：

```text
required input
optional input
default
unknown / missing
```

---

#### 5.2.16 Skill Output Contract

Skill 的输出不应只是一段“我完成了”的自然语言。

可以明确：

```text
status
result
artifacts
evidence
side_effects
warnings
next_state
```

例如：

```json
{
  "status": "success",
  "changed_files": ["a.py"],
  "tests": {"passed": 42, "failed": 0},
  "diff_reviewed": true
}
```

这样更利于 Harness / Workflow 消费结果。

---

#### 5.2.17 Preconditions

Skill 应明确自己的前置条件。

例如：

```text
publish_release
```

可能要求：

```text
repository clean
version resolved
tests passed
release permission available
```

如果前置条件不满足，正确行为可能是：

```text
PRECONDITION_NOT_MET
```

而不是硬执行。

---

#### 5.2.18 Postconditions

Skill 完成后应定义哪些条件必须成立：

```text
Postcondition
= successful skill completion implies what?
```

例如：

```text
safe_code_patch
```

不能只要求：

```text
file saved
```

还可能要求：

```text
target tests pass
no unrelated diff
requested behavior verified
```

---

#### 5.2.19 Capability Dependencies

Skill 应声明依赖哪些能力：

```text
required_tools
optional_tools
required_skills
runtime_capabilities
```

例如：

```text
research_report
requires:
- web_search
- document_read
optional:
- citation_manager
```

这样系统可以在 Activation 前做 Capability Check。

---

#### 5.2.20 Environment Dependencies

除了 Tool，Skill 还可能依赖：

```text
OS
filesystem
network
repository
browser session
runtime package
specific service
```

因此：

> **Tool available ≠ Skill executable。**

Skill 的完整可执行性取决于整个 Environment Contract。

---

#### 5.2.21 Permission Requirements

Skill 应显式声明所需权限：

```text
read files
write workspace
send message
modify repository
production deploy
```

而不是等执行到最后一步才发现：

```text
permission denied
```

更重要的是：

> **Skill 被激活，不代表它的所有内部 Action 自动获得授权。**

---

#### 5.2.22 Side-effect Contract

Skill 可能包含多步 Effect，因此必须描述：

```text
expected effects
possible effects
irreversible effects
external communication
monetary effects
```

例如：

```text
Skill: book_trip
```

最后可能涉及真实付款和预订，风险语义显然高于：

```text
Skill: compare_trip_options
```

---

#### 5.2.23 Skill Package

一个工程化 Skill 可以被理解成一个 package：

```text
skill/
├── manifest
├── instructions
├── schemas
├── examples
├── templates
├── scripts
├── resources
├── tests
└── metadata
```

并非每个 Skill 都需要所有文件，但这个模型有助于理解：

> **Skill 是可以被管理的能力资产，而不是一段散落的 Prompt。**

---

#### 5.2.24 Manifest

Manifest 适合放机器可读信息：

```text
id
version
description
inputs
outputs
dependencies
permissions
risk level
entrypoint
```

这样 Capability Discovery 不必先加载完整 Skill 内容。

---

#### 5.2.25 Instruction Body

Instruction Body 描述：

```text
目标
步骤
决策点
失败处理
验证方式
```

它是 Skill 中最接近 Prompt 的部分，但不代表 Skill 的全部。

---

#### 5.2.26 Examples

示例可以帮助模型学习 Skill 的适用边界和执行模式。

但示例要避免：

```text
Example-specific value
↓
被模型误认为必须复制的规则
```

因此示例最好显式标记：

```text
illustrative only
```

并覆盖正例与反例。

---

#### 5.2.27 Templates

Skill 可以附带：

```text
report template
PR template
SQL template
checklist
config skeleton
```

模板的作用是减少重复生成和格式漂移。

但模板仍需允许当前任务参数化，不应成为僵化复制。

---

#### 5.2.28 Scripts

某些稳定步骤适合从自然语言 Procedure 下沉成 deterministic script：

```text
LLM instruction
↓
repeated deterministic step
↓
script
```

例如：

```text
lint
schema validation
hash check
format conversion
```

这通常能提升可靠性并降低 token 成本。

---

#### 5.2.29 Skill 不是“把所有逻辑都写成自然语言”

成熟 Skill 应根据问题选择：

```text
Natural-language judgment
→ model reasoning

Deterministic transformation
→ code / script

Hard constraint
→ policy / validator

Effectful operation
→ tool / runtime
```

因此 Skill 更像一个**混合执行配方**。

---

#### 5.2.30 Skill Activation

Skill 被使用之前，需要回答：

```text
当前任务是否适合这个 Skill？
```

可以形式化成：

\[
S^*=\arg\max_{s\in\mathcal S} U(s\mid g_t, state_t, context_t)
\]

其中 \(U\) 不只考虑语义相关性，还应考虑：

```text
applicability
capability availability
permission
risk
cost
confidence
```

---

#### 5.2.31 Explicit Activation

最简单的是用户或开发者明确指定：

```text
use skill X
```

优点：

- 可控；
- 易解释；
- 激活误判少。

缺点：

- 用户必须知道 Skill 名称；
- 自动化程度低。

---

#### 5.2.32 Automatic Activation

Agent 根据任务自动判断：

```text
Task / State
↓
Skill Matcher
↓
Activate Skill X
```

这时 Skill Description、Applicability、Metadata 的质量非常重要。

自动激活带来的新 failure mode 是：

```text
Wrong Skill Activation
```

---

#### 5.2.33 Skill Retrieval

当 Skill 数量很多时，不应全部加载：

```text
Large Skill Registry
        ↓
Skill Retrieval
        ↓
Candidate Skills
        ↓
Skill Selection
```

这和：

```text
Document Retrieval → Evidence Selection
Tool Retrieval → Tool Selection
```

是同一种两阶段架构。

---

#### 5.2.34 Skill Retrieval 的目标

Candidate 阶段优先保证：

```text
Recall
```

Selection 阶段再优化：

```text
Precision / Utility
```

因此：

> **正确 Skill 没进入 Candidate Set，后面的 Agent 再聪明也选不到。**

---

#### 5.2.35 Skill Description 是检索接口

Skill Description 不只是给人看的说明，它直接影响：

```text
Discovery
Retrieval
Activation
```

因此 Description 应表达：

```text
what it solves
when to use
when not to use
important constraints
```

而不是营销式描述。

---

#### 5.2.36 Progressive Disclosure

大 Skill 不应该一次全部塞进 Context。

可以分层加载：

```text
Level 0: metadata
Level 1: summary / trigger rules
Level 2: core procedure
Level 3: examples / templates
Level 4: detailed references / scripts
```

只有当前决策需要时才继续展开。

---

#### 5.2.37 为什么 Progressive Disclosure 很重要？

否则 Skill Library 容易造成：

```text
Context Explosion
Instruction Conflict
Attention Dilution
Cost ↑
Selection Error ↑
```

所以：

> **Skill 可用 ≠ Skill 全文必须进入 Context。**

---

#### 5.2.38 Skill Context Budget

Skill 自己也消耗 Context Budget。

因此可以设置：

```text
skill_metadata_budget
active_skill_instruction_budget
example_budget
reference_budget
```

这延续了 4.1 的原则：

> **Minimal Sufficient Context。**

---

#### 5.2.39 Skill Activation 与 Context Loading 要分开

可以出现：

```text
Skill X 已被选中
```

但只加载它当前必要的部分。

所以：

```text
Activation
≠
Full Materialization into Context
```

这是降低上下文污染的重要机制。

---

#### 5.2.40 Skill State

复杂 Skill 通常需要自己的执行状态：

```text
current_stage
completed_steps
open_questions
artifacts
verification_status
retry_count
```

这不意味着 Skill 有独立 Agent 身份，只表示：

> **多步方法需要可恢复的过程状态。**

---

#### 5.2.41 Stateless Skill

简单 Skill 可以是近似无状态的：

```text
input
↓
procedure
↓
output
```

例如：

```text
normalize_citation
```

此时不必人为引入复杂 State Machine。

---

#### 5.2.42 Stateful Skill

长任务可能需要：

```text
INIT
↓
COLLECT
↓
ANALYZE
↓
DRAFT
↓
VERIFY
↓
DONE
```

显式状态有助于：

- 恢复；
- 可观察性；
- Debug；
- 终止判断。

---

#### 5.2.43 Resumable Skill

对于长 Skill，应考虑：

```text
Skill State
+
Checkpoint
+
Effect History
+
Pending Actions
```

从而：

```text
process crash
≠
skill must restart from zero
```

这直接连接 4.5 Persistence。

---

#### 5.2.44 Skill Step

Skill 内部每一步不一定等于一个 Tool Call。

```text
Skill Step
```

可以是：

- reasoning；
- retrieval；
- tool call；
- verification；
- user clarification；
- subskill activation。

因此不要把 Skill 简化成 Tool Sequence。

---

#### 5.2.45 Decision Point

好的 Skill 会明确哪些地方允许动态决策：

```text
if test failure is deterministic
→ repair

if environment is stale
→ re-observe

if requirement ambiguous
→ ask user
```

这比写：

```text
“自行判断”
```

更可审计。

---

#### 5.2.46 Skill Composition

复杂任务往往由多个 Skill 组合：

```text
research
↓
analysis
↓
report writing
↓
fact verification
```

因此 Skill System 不只是一个平面列表，而可能形成 Skill Graph。

---

#### 5.2.47 Sequential Composition

最简单的组合：

```text
Skill A
↓
Skill B
↓
Skill C
```

关键问题是：

```text
A 的 output contract
是否满足
B 的 input contract？
```

也就是接口兼容性。

---

#### 5.2.48 Conditional Composition

例如：

```text
run_diagnosis
   ↓
if dependency issue
   → dependency_repair
else if code bug
   → safe_code_patch
```

这时 Skill 的输出应支持结构化 routing signal，而不是只有自然语言总结。

---

#### 5.2.49 Nested Skill

Skill 可以调用另一个 Skill：

```text
release_product
├── run_release_checks
├── build_artifact
├── publish_release
└── verify_release
```

但需要明确：

```text
state ownership
permission inheritance
budget accounting
error propagation
```

---

#### 5.2.50 Skill Recursion

递归 Skill 需要非常谨慎。

例如：

```text
solve_subproblem
→ generate smaller subproblem
→ call solve_subproblem
```

必须存在：

```text
base case
depth limit
budget guard
progress criterion
```

否则容易形成无限展开。

---

#### 5.2.51 Skill Cycle

Skill Graph 中可能出现：

```text
A → B → C → A
```

如果没有 cycle detection，会造成无进展循环。

因此可维护：

```text
active_skill_stack
activation_history
cycle_signature
```

---

#### 5.2.52 Skill Conflict

两个 Skill 可能都适用，但原则冲突：

```text
Skill A: 快速修复
Skill B: 先完整验证再改
```

不能简单把两段 Instruction 拼在一起。

需要：

```text
priority
scope
policy
explicit arbitration
```

---

#### 5.2.53 Skill Precedence

优先级来源可以包括：

```text
system policy
user-selected skill
organization-approved skill
more-specific skill
higher-trust skill
```

但优先级必须可解释，不能由加载顺序偶然决定。

---

#### 5.2.54 Skill Granularity

Skill 太小：

```text
rename_file
```

可能和 Tool 没区别。

Skill 太大：

```text
run_entire_company
```

又难以复用、测试和控制。

好的颗粒度通常对应：

> **一个稳定重复出现、具有明确输入输出和成功标准的任务单元。**

---

#### 5.2.55 Macro Skill vs Micro Skill

```text
Micro Skill
= 局部方法，例如 verify_citation

Macro Skill
= 跨多个阶段，例如 produce_research_report
```

Macro Skill 往往由多个 Micro Skill 组成。

这比要求所有 Skill 同一粒度更现实。

---

#### 5.2.56 Mega-skill Anti-pattern

一个巨大的：

```text
universal_agent_skill
```

如果包含几乎所有任务规则，会导致：

```text
activation meaningless
context huge
conflicts hidden
testing impossible
versioning difficult
```

因此 Skill 不应成为新的“万能 System Prompt”。

---

#### 5.2.57 Minimal Sufficient Skill

可以建立一个新原则：

> **Skill 应包含完成目标所需的最小充分方法结构，而不是把所有相关知识都塞进去。**

即：

```text
Minimal Sufficient Skill
=
Enough Procedure
+
Enough Guardrails
+
Enough Verification
```

不等于最大知识包。

---

#### 5.2.58 Declarative Skill

Declarative Skill 更强调：

```text
goal
constraints
success criteria
available capabilities
```

由 Agent 动态决定内部步骤。

优点：灵活。

缺点：轨迹稳定性较低。

---

#### 5.2.59 Imperative Skill

Imperative Skill 更强调固定 Procedure：

```text
step 1
step 2
step 3
```

优点：稳定、可审计。

缺点：环境变化时可能僵化。

实际系统常用混合形式。

---

#### 5.2.60 Hybrid Skill

典型结构：

```text
Fixed Safety Skeleton
        +
Flexible Local Decisions
```

例如：

```text
必须：read → modify → test → diff review

但：
具体读哪些文件、修什么实现
由 Agent 判断
```

这是很多工程 Skill 比较合理的形态。

---

#### 5.2.61 Skill 与 Verification

Skill 不能只描述“怎么做”，还应该描述“怎样知道做对了”。

例如：

```text
Skill Procedure
↓
Execution
↓
Evidence
↓
Verification
↓
Skill Success
```

所以：

> **Skill returned ≠ Skill succeeded。**

---

#### 5.2.62 Skill Success Criteria

成功标准可以包括：

```text
required effects
forbidden effects
quality threshold
schema validity
test pass
user acceptance
```

越高风险的 Skill，越不能只依赖模型自我声明。

---

#### 5.2.63 Skill Failure Semantics

Skill 应能够报告：

```text
PRECONDITION_FAILED
DEPENDENCY_UNAVAILABLE
PERMISSION_BLOCKED
EXECUTION_FAILED
PARTIAL_SUCCESS
UNKNOWN_OUTCOME
VERIFICATION_FAILED
```

而不是全部压成：

```text
“Skill failed.”
```

---

#### 5.2.64 Skill Recovery

失败后的恢复可以分：

```text
retry step
repair input
fallback tool
activate alternative skill
replan
ask user
escalate
abort
```

恢复逻辑必须沿用 3.8 的原则：

> **Failure Handling ≠ Retry。**

---

#### 5.2.65 Retry Ownership

如果：

```text
Tool SDK retry 3 次
Skill retry 3 次
Harness retry 3 次
```

最终可能是：

```text
27 attempts
```

所以必须明确：

```text
who owns retry?
```

Skill 不应和 Runtime / SDK 隐式重复重试。

---

#### 5.2.66 Skill Fallback

Skill 可以声明：

```text
preferred capability
fallback capability
```

但 fallback 必须保持：

```text
semantic compatibility
permission compatibility
side-effect compatibility
```

不能因为主路径不可用，就偷偷换成更高风险路径。

---

#### 5.2.67 Skill Budget

Skill 可以消耗：

```text
tokens
model calls
tool calls
wall time
money
side effects
human approvals
```

因此 Skill Contract 可以声明预算上限或成本预期。

---

#### 5.2.68 Budget-aware Skill

复杂 Skill 应根据剩余预算调整策略：

```text
budget high
→ deeper verification / broader search

budget low
→ prioritize critical checks
```

但不应 silently 省略强制安全检查。

---

#### 5.2.69 Skill Observability

每次激活至少应能记录：

```text
skill_id
version
activation_reason
inputs
state snapshot ref
steps
subskills
tool calls
outputs
verification
cost
latency
final status
```

否则很难 Debug Skill 本身的问题。

---

#### 5.2.70 Skill Trace

一条完整 Trace 可以是：

```text
Task
↓
Skill Candidate Set
↓
Skill Selected
↓
Skill Version
↓
Step 1
↓
Tool Call
↓
Observation
↓
Step 2
↓
Verification
↓
Outcome
```

这样能区分：

```text
Activation Failure
vs
Execution Failure
vs
Verification Failure
```

---

#### 5.2.71 Skill Versioning

Skill 会变化：

```text
procedure
prompt
script
tool dependency
policy assumption
output schema
```

因此必须版本化。

否则同一个：

```text
skill_name
```

在不同时间可能已经不是同一个实验条件。

---

#### 5.2.72 Semantic Versioning 思路

可以借用：

```text
major.minor.patch
```

例如：

```text
major
= interface / behavior breaking change

minor
= backward-compatible capability increase

patch
= bug fix / wording refinement
```

不一定机械照搬，但版本语义必须明确。

---

#### 5.2.73 Skill Compatibility

升级 Skill 时要检查：

```text
input contract
output contract
tool dependencies
runtime assumptions
permission requirements
```

否则：

```text
Skill v2
```

可能把旧 Workflow 直接破坏。

---

#### 5.2.74 Skill Pinning

关键任务可以固定：

```text
skill_id@version
```

而不是永远调用：

```text
latest
```

这对：

```text
reproducibility
benchmarking
regulated workflows
```

尤其重要。

---

#### 5.2.75 Skill Migration

如果 Skill State 跨版本持久化，升级后可能需要：

```text
state migration
```

例如：

```text
v1 state schema
↓
converter
↓
v2 state schema
```

否则 Resume 可能失败。

---

#### 5.2.76 Skill Provenance

应知道 Skill 来自哪里：

```text
author
organization
source repository
created_at
reviewed_by
build / commit
```

特别是外部 Skill，Provenance 是 Trust 判断的重要输入。

---

#### 5.2.77 Skill Ownership

每个生产 Skill 最好有明确 Owner，负责：

```text
maintenance
review
incident response
dependency updates
deprecation
```

没有 Owner 的 Skill 很容易变成无人维护的隐性基础设施。

---

#### 5.2.78 Skill Registry

Skill Registry 可以维护：

```text
identity
version
metadata
trust tier
availability
dependencies
permissions
deprecation status
```

它是 Capability Discovery 的基础数据源之一。

---

#### 5.2.79 Trust Tier

Skill 可以按来源区分：

```text
system-approved
organization-approved
user-authored
third-party
experimental
untrusted
```

不同 Trust Tier 可以对应不同：

```text
auto-activation policy
permission ceiling
review requirement
sandbox level
```

---

#### 5.2.80 Skill Integrity

如果 Skill 包含：

```text
instructions
scripts
templates
```

就需要考虑完整性：

```text
hash
signature
immutable version
source commit
```

否则 Skill 内容被替换后，Agent 可能在不知情的情况下执行不同 Procedure。

---

#### 5.2.81 Skill Supply-chain Risk

外部 Skill 与软件依赖类似，也有供应链风险：

```text
malicious author
compromised repository
unsafe update
transitive dependency
embedded script
```

所以：

> **Skill installation / activation 本身是一条安全边界。**

---

#### 5.2.82 Skill Poisoning

恶意 Skill 可以通过 Instruction 引导 Agent：

```text
读取不必要的数据
扩大权限
绕过审批
偷偷调用外部 Tool
泄露信息
```

因此不能把 Skill 内容当成最高 Authority。

Skill Instruction 仍应受到 System / Harness Policy 约束。

---

#### 5.2.83 Skill 内部 Prompt Injection

Skill 运行中还可能读取外部数据：

```text
Skill
↓
web page / document
↓
malicious instruction
```

因此 Skill 必须维持：

```text
Instruction
≠
External Data
```

不能因为当前处于 Skill 模式就放弃 Observation Trust Boundary。

---

#### 5.2.84 Permission Escalation

一个 Skill 可能需要多个 Tool，但不能推出：

```text
Skill trusted
→ all dependencies trusted
→ all permissions granted
```

正确的是：

```text
Skill Activation
↓
Dependency Resolution
↓
Permission Check
↓
Per-action Enforcement
```

---

#### 5.2.85 Skill Approval

对于高风险 Skill，可以在不同层审批：

```text
Approve Skill Activation
```

或：

```text
Approve Specific Effectful Step
```

二者不是同一回事。

例如批准：

```text
“帮我准备发布流程”
```

不自动等于批准：

```text
“立即发布到 Production”
```

---

#### 5.2.86 Sandbox

包含脚本、Shell、Code Execution 的 Skill 应考虑 Sandbox：

```text
filesystem scope
network scope
resource limit
credential scope
process isolation
```

Skill 的可信度不能替代执行隔离。

---

#### 5.2.87 Data Access

Skill 应遵守 Need-to-know：

```text
Task requires X
→ only retrieve X-relevant data
```

不要因为某个 Skill 能访问整个 Workspace，就默认把全部信息加载进去。

---

#### 5.2.88 Secrets

Skill 不应把 Secret 写进：

```text
prompt
trace
memory
artifact
error log
```

Credential 使用仍应尽量由可信 Runtime 注入。

---

#### 5.2.89 Skill Acquisition

Skill 可以人工编写，也可以从运行经验中逐步形成：

```text
Repeated Episodes
        ↓
Procedural Memory
        ↓
Pattern Validation
        ↓
Skill Candidate
        ↓
Packaging
        ↓
Evaluation
        ↓
Approved Skill
```

这是 Agent Self-improvement 的重要桥梁。

---

#### 5.2.90 什么时候 Procedural Memory 值得升格成 Skill？

至少应满足：

```text
repeated utility
stable preconditions
clear task boundary
repeatable procedure
measurable success criteria
manageable risk
sufficient evidence
```

不能因为：

```text
一次成功
```

就自动生成永久 Skill。

---

#### 5.2.91 Skill Candidate

在正式 Skill 前可以有：

```text
experimental skill
```

只允许：

- 沙箱运行；
- 低风险任务；
- 人工审查；
- 小流量启用。

这类似软件从实验到生产的晋级过程。

---

#### 5.2.92 Skill Validation

候选 Skill 至少要验证：

```text
Does it activate correctly?
Does it execute correctly?
Does it improve task outcome?
Does it cause new harm?
Does it generalize?
```

这比“看起来写得合理”严格得多。

---

#### 5.2.93 Skill Update

Skill 更新来源可以是：

```text
incident
new tool
new policy
better procedure
new environment
repeated failure pattern
```

但更新后必须重新评测，而不是直接覆盖生产版本。

---

#### 5.2.94 Skill Learning ≠ Model Training

更新 Skill：

```text
external procedure changes
```

并不等于：

```text
model weights changed
```

所以：

> **Skill-based improvement 可以在完全冻结模型参数的情况下发生。**

这也是 Harness RSI / Agent Optimization 的重要机制。

---

#### 5.2.95 Skill Deprecation

旧 Skill 不应直接消失。

可以经历：

```text
active
↓
deprecated
↓
disabled
↓
retired
```

并保留：

```text
replacement
migration guidance
last supported version
```

---

#### 5.2.96 Skill Removal

删除 Skill 还需要检查：

```text
who depends on it?
which workflows reference it?
which checkpoints may resume into it?
```

所以：

```text
Skill deleted
≠
Dependency safely removed
```

---

#### 5.2.97 Skill Evaluation：不能只看最终 Task Success

至少拆成：

```text
Activation Quality
Execution Quality
Verification Quality
Safety
Efficiency
Generalization
```

否则 Skill 的具体问题会被最终成功率掩盖。

---

#### 5.2.98 Activation Metrics

可以评估：

```text
Skill Activation Precision
Skill Activation Recall
Wrong-skill Rate
Missed-skill Rate
Unnecessary Activation Rate
```

因为：

```text
Skill 本身很好
```

不代表：

```text
系统知道什么时候用它
```

---

#### 5.2.99 Execution Metrics

执行阶段可以看：

```text
Skill Completion Rate
Step Failure Rate
Tool Error Rate
Recovery Success Rate
Verification Pass Rate
```

并按 Skill Version 分层统计。

---

#### 5.2.100 Outcome Metrics

最终可以看：

```text
Task Success
Quality Score
False-success Rate
Harmful Side-effect Rate
Cost per Success
Latency per Success
```

Skill 的目标不是“被执行”，而是带来净任务收益。

---

#### 5.2.101 Skill Net Benefit

延续前面的 repair–degradation 视角：

```text
Skill Net Benefit
=
Cases Improved
-
Cases Degraded
```

因为一个 Skill 可能：

```text
救回 30 个任务
```

同时：

```text
把 10 个原本正确任务带偏
```

只统计 rescue 会高估价值。

---

#### 5.2.102 Skill Ablation

可以做：

```text
No Skill
vs
Skill Metadata Only
vs
Skill Instructions
vs
Skill + Scripts
vs
Skill + Verification
```

从而判断 Skill 的收益究竟来自哪里。

---

#### 5.2.103 Oracle Skill Selection

给定正确 Skill：

```text
Oracle Skill Selection
```

可以测：

```text
Skill Execution Upper Bound
```

而 Normal Selection → Oracle Selection 的差距，则反映 Skill Retrieval / Activation 的问题。

---

#### 5.2.104 Failure Localization

当 Skill 失败时，可以追：

```text
1. Skill 存在吗？
2. Registry 可见吗？
3. 被召回了吗？
4. 被正确选择了吗？
5. Preconditions 满足吗？
6. Dependencies 可用吗？
7. 权限够吗？
8. Procedure 执行对吗？
9. Verification 正确吗？
10. 最终 Outcome 对吗？
```

这样避免一句：

```text
“Skill 不好用。”
```

把所有层次混在一起。

---

#### 5.2.105 Robustness Evaluation

应测试：

```text
missing tool
stale state
partial observation
ambiguous input
conflicting instruction
rate limit
permission denial
unexpected output
```

好的 Skill 不应只在 Happy Path 有效。

---

#### 5.2.106 Generalization

Skill 应验证：

```text
同类但未见过的任务
不同用户输入风格
不同环境条件
不同 Tool Provider
```

否则可能只是 benchmark-specific recipe。

---

#### 5.2.107 Skill Overfitting

如果 Skill 过度针对历史案例：

```text
case-specific heuristics
hard-coded paths
benchmark-specific wording
```

离线效果可能很高，但真实泛化很差。

所以：

> **Skill Optimization 也会过拟合。**

---

#### 5.2.108 Coding Agent 示例

```text
Task:
修复 failing test

Skill: safe_code_patch

1. 读取失败测试与相关实现
2. 复现失败
3. 定位最小修复点
4. 修改
5. 跑目标测试
6. 跑相关回归
7. 检查 git diff
8. 验证无无关修改
9. 报告 evidence
```

这里 Tool 是：

```text
read_file
edit_file
run_test
git_diff
```

Skill 则是整个方法。

---

#### 5.2.109 Research Agent 示例

```text
Skill: evidence_based_research

1. 明确问题
2. 拆检索子问题
3. 优先权威来源
4. 交叉验证
5. 记录 provenance
6. 区分事实与推断
7. 处理冲突
8. 输出带证据结论
```

它可能调用 Search Tool，但显然不等于 Search Tool。

---

#### 5.2.110 Data Agent 示例

```text
Skill: safe_data_analysis

1. 明确口径
2. 检查 schema
3. 数据质量审计
4. 构造查询
5. 结果 sanity check
6. 分析
7. 输出可复现口径
```

这里 Skill 把“分析规范”变成了可重复方法。

---

#### 5.2.111 Browser Agent 示例

```text
Skill: safe_form_submission

1. 识别目标表单
2. 填写但不提交
3. 校验关键字段
4. 展示预期 side effect
5. 获取必要 approval
6. submit
7. re-observe
8. verify success
```

这体现 Skill 可以把 Permission / Verification 直接嵌入 Procedure。

---

#### 5.2.112 Multi-Agent 中的 Skill

不同 Agent 可以拥有不同 Skill Set：

```text
Research Agent
→ research skills

Coding Agent
→ coding skills

Reviewer Agent
→ verification skills
```

这比让所有 Agent 共享全部能力更容易控制。

---

#### 5.2.113 Shared Skill vs Private Skill

```text
Shared Skill
= 多 Agent 可调用

Private Skill
= 某角色 / Agent 专属
```

共享 Skill 要特别关注：

```text
state assumptions
permission assumptions
context assumptions
```

因为不同 Agent 的执行环境可能不同。

---

#### 5.2.114 Skill Handoff

Agent A 可以输出：

```text
Skill-compatible artifact / state
```

再由 Agent B 接着执行。

这要求 Skill Contract 对 State 与 Output 有清晰结构，否则 Multi-Agent Handoff 会退化成自然语言猜测。

---

#### 5.2.115 Skill 与 Harness

Harness 负责：

```text
哪些 Skill 可见？
什么时候允许自动激活？
哪些需要审批？
Context 加载多少？
预算是多少？
失败后如何升级？
```

因此：

```text
Skill
= capability method

Harness Skill Policy
= capability governance
```

---

#### 5.2.116 Skill 与 Runtime

Runtime 负责更底层的：

```text
execution
state persistence
checkpoint
sandbox
credentials
scheduling
recovery
```

Skill 可以描述“应该做什么”，但可靠执行仍依赖 Runtime。

---

#### 5.2.117 Skill 与 Capability Discovery

Capability Discovery 要回答：

```text
当前系统有哪些 Skill？
哪些现在可用？
哪个适合当前任务？
```

所以 Skill Metadata 是 5.4 的重要输入。

---

#### 5.2.118 Skill 与 MCP

MCP 可以帮助系统发现 / 调用外部能力；Skill 可以声明自己依赖哪些 MCP Capability。

例如：

```text
Skill: triage_issue
    ↓
MCP GitHub
├── issue read
├── comment
└── labels
```

所以：

```text
Skill = 方法
MCP = 能力连接协议
```

两者互补。

---

#### 5.2.119 Skill Library 的真正价值

Skill Library 不是：

```text
更多 Prompt 文件
```

而是：

```text
组织已验证的方法能力
↓
让 Agent 在需要时发现
↓
以受控方式激活
↓
持续评测与迭代
```

这是从“临时聪明”走向“系统可积累能力”的关键机制。

---

#### 5.2.120 常见失败模式

1. **Skill = Prompt File**：只有一段文本，没有 Contract、验证和依赖；
2. **Wrong Skill Activation**：相关但不适用的 Skill 被自动激活；
3. **Missed Skill**：正确 Skill 存在但未被召回；
4. **Skill Explosion**：大量重叠 Skill 导致选择困难；
5. **Mega-skill**：一个 Skill 承担所有任务；
6. **Granularity Collapse**：Skill 小到和 Tool 没区别；
7. **Context Flooding**：所有 Skill 全量注入；
8. **Instruction Conflict**：多个 Skill 规则互相打架；
9. **Hidden Dependency**：依赖 Tool / Environment 未声明；
10. **Permission Assumption**：Skill 默认自己拥有所需权限；
11. **Unsafe Fallback**：失败后切换到更高风险路径；
12. **Retry Multiplication**：Skill 与 Runtime 重复重试；
13. **No Verification**：执行结束就宣称 Skill 成功；
14. **Stale Skill**：Procedure 与 Tool / Policy 已经不匹配；
15. **Version Drift**：同一 Skill 名字行为不断变化；
16. **Skill Poisoning**：外部 Skill 植入恶意 Instruction；
17. **Supply-chain Compromise**：依赖包或脚本被篡改；
18. **Overgeneralization**：一次经验被错误升格为通用 Skill；
19. **Skill Overfitting**：只对历史 Benchmark 有效；
20. **No Owner**：Skill 无人维护，长期腐化；
21. **State Loss**：长 Skill crash 后只能从头执行；
22. **Approval Laundering**：激活 Skill 被错误解释为批准内部所有 Action；
23. **Secret Leakage**：Skill 把 Credential 写入 Context / Log；
24. **Cycle / Recursion Loop**：Skill 互相调用但无终止条件；
25. **False-success Skill**：模型说完成，但 Environment 没满足成功条件。

---

#### 5.2.121 工程原则

1. **Skill 要有稳定 Contract，而不只是自然语言正文。**
2. **Tool 描述原子能力；Skill 描述任务方法。**
3. **Skill Activation 与 Full Context Loading 分离。**
4. **大规模 Skill Library 采用 Retrieval → Selection。**
5. **优先 Progressive Disclosure，避免 Context Flooding。**
6. **Procedure、Dependency、Permission、Side Effect、Verification 都应显式。**
7. **Skill 激活不等于权限自动提升。**
8. **高风险 Action 仍逐步经过 Policy / Approval。**
9. **稳定确定步骤尽量下沉为脚本或 Validator。**
10. **复杂 Skill 维护显式 State 和 Checkpoint。**
11. **明确 Retry Ownership，避免多层重试倍增。**
12. **Skill 必须版本化，关键任务应支持 Pinning。**
13. **外部 Skill 视为供应链依赖，检查 Provenance 与 Integrity。**
14. **Procedural Memory 升格 Skill 前必须经过重复证据与评测。**
15. **Skill 更新必须做 Regression，不要直接覆盖生产版本。**
16. **同时评估 Skill 的 rescue 与 degradation。**
17. **把 Activation Failure、Execution Failure、Verification Failure 分开统计。**
18. **Skill 应有明确 Owner、生命周期与 Deprecation Policy。**
19. **用 Minimal Sufficient Skill 控制复杂度。**
20. **Skill Library 的目标是积累可靠能力，不是积累 Prompt 数量。**

---

#### 5.2.122 面试高频问法

**Q1：Skill 和 Tool 有什么区别？**  
Tool 是原子可执行能力；Skill 是围绕一类任务组织 Tool、规则、状态和验证的可复用方法。

**Q2：Skill 和 Workflow 有什么区别？**  
Workflow 更强调显式固定控制流；Skill 可以包含固定骨架，也可以保留局部 Agentic Decision。

**Q3：Skill 和 Prompt 有什么区别？**  
Prompt 是当前推理输入；Skill 是包含 Procedure、Dependencies、Contract、Safety、Verification 和 Version 的能力资产。

**Q4：Skill 和 Procedural Memory 有什么区别？**  
Procedural Memory 是经验性方法知识；Skill 是经过整理、验证和封装后可复用调用的能力。

**Q5：什么时候应该把 Procedural Memory 升级成 Skill？**  
当方法重复有效、边界稳定、成功标准清楚、可复用且风险可控，并经过独立验证时。

**Q6：为什么 Skill 需要 Progressive Disclosure？**  
因为 Skill 数量和内容很大时，全量注入会造成 Context Explosion、冲突和成本上升。

**Q7：Skill 怎么自动选择？**  
通常先通过 Metadata / Description 做 Candidate Retrieval，再结合 State、适用性、权限、成本和风险做 Selection。

**Q8：Skill 激活后是不是自动拥有内部 Tool 权限？**  
不是。Activation 与 Authorization 是两层；内部 effectful Action 仍需正常权限和审批。

**Q9：Skill 如何评测？**  
至少拆 Activation、Execution、Verification、Outcome、Safety、Cost / Latency，并统计净收益而非只看成功案例。

**Q10：Skill 可以调用 Skill 吗？**  
可以，但需要处理接口兼容、State Ownership、Budget、Permission、Cycle 与 Error Propagation。

**Q11：Skill 与 MCP 什么关系？**  
Skill 描述任务方法；MCP 负责标准化能力暴露和连接。Skill 可以依赖 MCP Tool。

**Q12：Skill 与 Agent 什么关系？**  
Agent 是动态决策主体；Skill 是 Agent 可选择使用的能力之一。

**Q13：Skill 会不会成为新的 System Prompt？**  
不应该。Skill 应保持明确任务边界，通过检索和按需加载使用，而不是把所有规则堆成一个超级 Prompt。

**Q14：Skill 怎样避免版本漂移？**  
稳定 ID + Version + Pinning + Regression + Migration + Deprecation。

**Q15：Skill 的安全风险是什么？**  
主要包括恶意 Skill、供应链风险、Prompt Injection、权限扩大、数据泄露、危险 Side Effect、Approval Laundering 和陈旧 Procedure。

---

#### 5.2.123 一句话总结

> **Skill 是介于知识与执行之间的可复用任务方法：它把成熟经验组织成有 Contract、有依赖、有状态、有安全边界、有验证、有版本的能力单元，由 Agent 在合适的 State 下选择，并通过 Tool / Workflow / Runtime 真正执行。**

也可以把整个关系压缩成：

```text
Experience
↓
Procedural Memory
↓
Validation / Packaging
↓
Skill
↓
Agent Selection
↓
Tool / Workflow / MCP Capability
↓
Environment
↓
Evidence / Outcome
↓
Skill Evaluation / Update
```

---

#### 5.2.124 与下一节 MCP 的衔接

到这里我们已经知道：

```text
Native Tool
= Host 原生集成了哪些能力

Skill
= 怎样把这些能力组织成可复用任务方法
```

下一节要继续回答：

> **如果能力并不原生属于当前 Host，系统怎样用一种标准方式发现、描述、连接并调用外部 Tool / Resource？**

这就是 **5.3 MCP** 的问题。

---

#### 5.2.125 参考资料

- Sutton, R. S., Barto, A. G. *Reinforcement Learning: An Introduction*：Options / temporal abstraction 对“可复用高层行为单元”的经典启发。
- Dietterich, T. G. Hierarchical Reinforcement Learning with the MAXQ Value Function：层次化任务分解与子任务复用。
- Sutton, Precup, Singh. Between MDPs and Semi-MDPs: A Framework for Temporal Abstraction in Reinforcement Learning：高层 action / option 与 temporal abstraction。
- ReAct：Reasoning 与 Action 交替，为 Skill 内部的动态 procedure 提供基础模式。
- Plan-and-Execute / hierarchical planning literature：Skill 与 plan / subtask decomposition 的关系。
- 软件工程中的 API Contract、Semantic Versioning、Dependency Management、Supply-chain Security：Skill Contract、版本与依赖治理的重要工程参照。
- SRE / fault-tolerant workflow literature：长 Skill 的 retry ownership、recovery、checkpoint 与 observability。
- OWASP Agentic / LLM Application Security guidance：外部 Instruction、Tool 权限、Prompt Injection 与供应链风险。
