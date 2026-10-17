### 3.2 Tool Schema

#### 3.2.1 定义：Tool Schema 到底是什么？

在 3.1 中，我们把 Tool 定义为一个 **executable capability contract**。其中最重要的一部分，就是输入契约：Agent 到底可以用什么结构、什么字段、什么类型去表达一次合法的 Tool Call。

**Tool Schema** 就是这个输入契约的机器可读表示。

如果某个 Tool 的参数空间记为 $\mathcal{A}$，那么 Schema 可以近似理解为定义了一个结构上允许的子空间：

$$
\mathcal{A}_{schema}
=
\{a \in \mathcal{A} \mid a \text{ satisfies schema constraints}\}
$$

例如一个搜索 Tool：

```json
{
  "query": "Agent tool schema",
  "top_k": 10
}
```

对应的 Schema 可能要求：

```text
query:
  string
  required

top_k:
  integer
  optional
  1 <= top_k <= 20
```

因此，Tool Schema 解决的是：

> **一次 Tool Call 的 argument object，在结构上允许长什么样？**

它通常可以描述：

```text
字段名称
字段类型
required / optional
nullable
枚举值
数值范围
字符串长度
数组长度
嵌套对象
互斥分支
条件依赖
是否允许额外字段
```

但这里必须先把边界钉死：

> **Schema 定义的是结构合法性，不是事实正确性、业务正确性、权限合法性，也不是 Tool 的全部语义。**

例如：

```json
{
  "recipient": "wrong-person@example.com",
  "subject": "Meeting",
  "body": "..."
}
```

完全可能：

```text
Schema Valid = True
```

但业务上：

```text
Recipient Wrong = True
```

甚至权限上：

```text
Authorized = False
```

所以后面始终要记住：

```text
Schema Valid
≠
Semantically Correct
≠
Authorized
≠
Safe to Execute
```

---

#### 3.2.2 为什么 Agent 系统特别需要 Tool Schema？

如果没有 Schema，模型的 Action Interface 很容易退化成自由文本。

例如：

```text
Tool: send_email
Arguments: 给老板发一下明天开会的事
```

Runtime 还必须重新猜：

```text
老板是谁？
recipient 是什么？
subject 是什么？
body 是什么？
是草稿还是直接发送？
```

这会把一个原本应该确定性的接口问题重新交给自然语言解析。

而有了明确 Schema：

```json
{
  "recipient": "boss@example.com",
  "subject": "Tomorrow's meeting",
  "body": "...",
  "mode": "draft"
}
```

系统就可以在执行前做确定性检查。

因此 Tool Schema 的价值包括：

```text
1. 把开放自然语言映射成结构化 Action
2. 限定模型可表达的 argument space
3. 支持执行前 Validation
4. 减少字段歧义
5. 支持 constrained generation
6. 提升日志、回放与审计能力
7. 支持字段级 Evaluation
8. 支持版本管理与兼容性检查
9. 为权限和业务校验提供稳定输入
10. 让 Runtime 不必猜模型到底想表达什么
```

从 Agent 角度，可以把它看成：

```text
Natural-language Intent
        ↓
Model Decision
        ↓
Tool Schema
        ↓
Typed Action Object
        ↓
Validation / Authorization
        ↓
Execution
```

所以：

> **Schema Engineering 本质上也是 Action-Space Engineering。**

---

#### 3.2.3 Tool Schema、Tool Description 与 Tool Semantics 不是一回事

这三个概念很容易被写在同一份 Tool Definition 里，因此经常被混淆。

可以这样区分：

| 概念 | 回答的问题 |
|---|---|
| Tool Schema | 参数结构上可以怎么写？ |
| Tool Description | 这个 Tool / 字段是做什么的？什么时候用？ |
| Tool Semantics | Tool 实际执行后会发生什么？ |

例如：

```json
{
  "amount": {
    "type": "number"
  }
}
```

Schema 只告诉模型：

```text
amount 是 number
```

但没有告诉它：

```text
单位是什么？
美元还是日元？
税前还是税后？
允许负数吗？
这是查询金额还是支付金额？
```

这些需要 Description 与 Semantics 才能解释完整。

一句话记忆：

> **Schema 约束“长什么样”，Description 解释“是什么意思”，Semantics 定义“真正会发生什么”。**

---

#### 3.2.4 Required、Optional、Nullable 与 Missing 必须严格区分

这是 Tool Schema 最常见、也最隐蔽的工程坑之一。

假设：

```json
{
  "title": "Fix parser bug",
  "due_date": null
}
```

至少存在四种不同语义：

- **Required**：字段必须出现，missing 即 invalid。
- **Optional**：字段可以完全不出现。
- **Nullable**：字段出现时，可以显式为 `null`。
- **Empty Value**：如 `""`、`[]`、`{}`，又是另一种状态。

因此：

```text
missing
≠ null
≠ ""
≠ []
≠ {}
```

例如：

```text
missing due_date
→ 用户没有提供截止日期

null due_date
→ 显式取消截止日期
```

如果把两者混起来，Agent 可能在 PATCH / Update 操作中意外删除已有字段。

所以设计 Schema 时必须问：

> **字段不存在和字段显式为空，业务语义是否相同？**

如果答案是否定的，就必须在 contract 中区分。

---

#### 3.2.5 Required 字段也不能“越多越安全”

直觉上常会认为：

```text
更多 required
→ 输出更完整
→ 系统更稳定
```

但对 LLM Agent 并不总成立。

假设：

```json
{
  "customer_id": "required",
  "customer_name": "required",
  "customer_email": "required"
}
```

而当前 Context 里只有 `customer_name`。模型为了满足 Schema，可能直接编造 `customer_id` 和 `customer_email`。

也就是：

> **Schema 可以减少结构缺失，却可能放大 structured hallucination。**

因此 required 的原则是：

> **只有当模型在当前决策阶段应该能够可靠获得某个字段时，才把它设计为模型必须生成的 required 字段。**

否则更合理的是先做 entity resolution，再拿稳定 ID 调下一步 Tool。

---

#### 3.2.6 Primitive Type：类型不是小事

Tool Schema 最基础的约束包括：

```text
string
integer
number
boolean
object
array
null
```

但真实系统里很容易发生错误的数据类型设计。

例如：

```text
customer_id = 001234
```

如果定义成 integer：

```text
001234 → 1234
```

前导零会丢失。

同理：

```text
postal_code
phone_number
account_number
order_id
version_hash
```

虽然“看起来是数字”，本质上往往都是 identifier，更适合定义为 string。

一个很实用的判断是：

> **如果这个值主要用于标识，而不是参与数学运算，就优先把它当作 string。**

---

#### 3.2.7 不要依赖隐式 Type Coercion

某些 Runtime 会自动尝试：

```text
"123" → 123
"false" → false
"1" → true
```

这在普通表单里可能方便，但对 Agent Tool Call 很危险。

例如：

```json
{
  "dry_run": "false"
}
```

如果不同 Runtime 对字符串布尔值的解释不同，可能出现完全相反的行为。

所以更稳妥的原则是：

> **Tool Boundary 尽量采用严格类型验证，不做隐式 coercion；如果必须转换，应显式、确定、可观测。**

---

#### 3.2.8 Format Validity 仍然不是 Semantic Validity

Schema 可以进一步要求：

```text
email
URI
UUID
date-time
hostname
```

但：

```text
email 格式合法
≠ 邮箱真实存在
≠ 属于目标用户
≠ 当前用户有权发送
```

同理：

```text
UUID 格式合法
≠ 数据库里真的有这个对象
```

```text
URI 格式合法
≠ URL 安全、可访问或允许访问
```

因此：

> **Format Validation 只是比 Type Validation 更具体的一层结构检查，不是现实世界验证。**

---

#### 3.2.9 Enum：把开放语言压缩成有限决策空间

当字段只有有限且稳定的取值时，优先使用 enum。

例如：

```json
{
  "mode": {
    "type": "string",
    "enum": ["read", "append", "overwrite"]
  }
}
```

而不是完全开放的 string。

它可以：

```text
减少开放生成空间
降低拼写漂移
避免同义词歧义
方便 Routing / Policy
方便 Evaluation
方便日志统计
```

所以：

> **Enum 是把自然语言决策映射到稳定程序状态的一种重要方式。**

---

#### 3.2.10 Enum 也可能逼出错误答案

假设：

```json
{
  "category": {
    "enum": ["billing", "technical", "sales"]
  }
}
```

但真实请求是 `legal complaint`。

如果 Schema 没有：

```text
unknown
other
needs_review
```

模型就只能硬选现有类别。

于是 Schema 会把：

```text
“不知道”
```

强行压成：

```text
“错误但格式合法的答案”
```

因此 enum 设计必须问：

> **现实世界是否真的被这些类别穷尽？**

如果不能，就需要明确的 abstention / unknown path。

---

#### 3.2.11 Bounds：范围约束可以减少无意义 Action

Schema 可以限制数值和长度范围，例如：

```text
top_k:
  integer
  1..50

timeout_ms:
  integer
  100..30000

query:
  string
  minLength = 1
  maxLength = 500
```

这可以提前排除：

```text
top_k = -1
top_k = 1000000
timeout = 3 hours
empty query
```

因此 Bounds 也能承担一部分 resource guard。

但：

```text
amount <= 10000
```

只能证明金额没有超过 Schema 上限，不能证明用户授权这笔支付。

所以：

> **Schema Bound 是输入约束，不是 Authorization Policy。**

---

#### 3.2.12 Array：集合输入也是一种 Action Amplification

很多 Tool 接受数组：

```json
{
  "file_ids": ["a", "b", "c"]
}
```

Schema 应明确：

```text
item type
minItems
maxItems
uniqueItems
order semantics
```

例如 `maxItems = 20` 在 Agent 系统里尤其重要，因为：

```text
单个 delete_file
```

和：

```text
delete_files(files=[...10000 items...])
```

虽然只是多了一个数组，Action Blast Radius 完全不同。

因此：

> **Batch size 本身就是风险与成本维度。**

即使限制了数组长度，仍然需要 per-item validation、permission、side-effect handling 与 partial-success semantics。

---

#### 3.2.13 Nested Object：结构清晰与生成稳定之间要权衡

复杂对象天然有层级。例如：

```json
{
  "shipping_address": {
    "country": "JP",
    "city": "Tokyo",
    "postal_code": "100-0001",
    "street": "..."
  }
}
```

这种嵌套在语义上比一堆无组织字段完整。

但如果 Schema 变成：

```text
object
 └── object
      └── array
           └── object
                └── oneOf
                     └── object
```

模型生成难度、调试难度和 token overhead 都会明显增加。

所以要在：

```text
semantic coherence
vs
structural complexity
```

之间权衡。

经验上：

> **优先使用浅层、语义完整的嵌套；不要为了“数据结构漂亮”把模型逼进过深的对象树。**

---

#### 3.2.14 Union / oneOf：不要用一堆 Nullable 字段模拟互斥模式

假设一个 Tool 支持：

```text
file
url
raw_text
```

一种很差的 Schema 是：

```json
{
  "file_path": null,
  "url": null,
  "text": null
}
```

然后靠约定“三个字段只能填一个”。这会产生大量非法组合。

更合理的是显式 discriminator：

```json
{
  "source_type": "file",
  "file": {
    "path": "/tmp/a.txt"
  }
}
```

或概念上：

```text
oneOf:
  FileSource
  URLSource
  RawTextSource
```

核心原则：

> **如果几个字段代表互斥业务模式，就把“模式”本身建模出来，而不是靠大量 nullable field 猜。**

---

#### 3.2.15 oneOf / anyOf 也不是越复杂越好

理论上复杂 Schema 可以表达：

```text
oneOf
anyOf
allOf
not
if / then / else
```

但模型是否稳定理解这些组合、不同 Tool Runtime 是否完整支持，是另一个问题。

如果 Schema 逻辑过度复杂，即使规范本身合法，也可能让 argument generation 非常脆弱。

所以工程目标不是把所有业务规则塞进 Schema，而是：

> **用 Schema 表达适合结构化表达的约束，把复杂领域规则留给 Semantic / Business Validator。**

---

#### 3.2.16 Cross-field Dependency：单字段合法不代表组合合法

例如：

```json
{
  "start_date": "2026-10-20",
  "end_date": "2026-10-18"
}
```

两个字段分别都是合法日期，但组合上明显错误。

又例如：

```text
mode = "range"
```

则必须同时存在 `start` 和 `end`。

一部分依赖可以在 Schema 中表达：

```text
if mode=range
then require start,end
```

但像：

```text
end >= start
available_balance >= amount
user owns resource_id
```

通常已经进入 Semantic / State Validation。

所以：

> **Schema 擅长表达结构关系；真实世界关系通常需要额外 Validator。**

---

#### 3.2.17 `additionalProperties`：是否允许模型偷偷多塞字段？

假设 Tool 只定义 `query` 与 `limit`，模型却生成：

```json
{
  "query": "...",
  "limit": 10,
  "admin": true
}
```

如果 Runtime 默认接受未知字段，可能出现 schema drift、隐式参数注入和版本不一致。

因此 Agent Action Schema 通常更适合：

```text
closed by default
```

概念上即：

```json
{
  "additionalProperties": false
}
```

除非某个 Tool 明确需要开放扩展字段。

> **对于可执行 Action，Schema 应优先采用显式字段白名单，而不是开放字典。**

---

#### 3.2.18 Default Value：默认值其实是隐藏决策

假设：

```text
write_file(path, mode)
```

而 `mode` optional，Runtime 默认：

```text
mode = overwrite
```

模型没有明确生成 mode，却最终执行了 destructive write。

这说明：

> **Default 不是无害的工程便利，而是一个系统替模型做出的隐式 Action Decision。**

重要字段的默认值应该 safe、stable、documented、observable、versioned。高风险行为更应该要求 explicit value，而不是 silently default。

---

#### 3.2.19 Tool Call 的完整 Validation Pipeline

可靠系统不应该：

```text
Model Output
↓
Schema pass
↓
Execute
```

更完整的是：

```text
Model Tool Call
      ↓
Parse
      ↓
Schema Validation
      ↓
Semantic / Business Validation
      ↓
State / Precondition Validation
      ↓
Permission / Policy Check
      ↓
Approval if required
      ↓
Runtime Execution
      ↓
Postcondition Verification
```

其中：

```text
Parse
= 能不能构造成对象？

Schema Validation
= 字段、类型、结构是否合法？

Semantic Validation
= 值在业务语义上合理吗？

State Validation
= 当前世界状态允许这个 Action 吗？

Permission Check
= 当前主体是否有权执行？

Verification
= 执行后目标真的达成了吗？
```

所以：

> **Schema Validation 只是 Action Safety Pipeline 的一层，而不是终点。**

---

#### 3.2.20 Schema-valid 但仍然错误：三个典型例子

**实体不存在：**

```json
{"city": "Tokyoo"}
```

string 合法，但实体可能不存在。

**路径不允许：**

```json
{"path": "/etc/passwd"}
```

string 合法，但 Policy 应拒绝。

**目标实体错误：**

```json
{"recipient": "someone@example.com"}
```

email 格式合法，但可能发错人。

因此永远不要把：

```text
schema_valid == true
```

解释成：

```text
action_is_correct == true
```

---

#### 3.2.21 Tool Schema 与 Constrained Decoding

Schema 可以在两个阶段发挥作用。

第一种是 **Post-hoc Validation**：

```text
Model 自由生成
↓
Parse
↓
Schema Validator
↓
Pass / Reject
```

第二种是 **Constrained Generation / Decoding**：

```text
Model logits
↓
Schema / Grammar state
↓
Mask invalid continuations
↓
只允许结构合法输出
```

后者能提高 JSON validity、field structure validity 和 enum compliance，但仍无法保证 Tool 选对、argument 语义正确、目标实体正确或 Action 被授权。

所以：

```text
Constrained Decoding
≠ Semantic Validation
```

这与 1.5 Structured Output 完全衔接。

---

#### 3.2.22 Schema 本身会改变模型的 Decision Space

Schema A：

```json
{"operation": "string"}
```

模型理论上可以输出任意字符串。

Schema B：

```json
{
  "operation": {
    "enum": ["read", "append", "overwrite"]
  }
}
```

显式 Action Space 被压缩成三个选项。

再比如 `recipient_email` 与 `recipient_id` 会让模型采取完全不同的 entity-resolution 路径。

所以：

> **Schema 不只是 Validation Spec，它也在塑造模型看到的问题本身。**

Schema Design 会直接影响 argument generation difficulty、selection ambiguity、hallucination pressure、error attribution 与 safety surface。

---

#### 3.2.23 Mega-schema：一个 50 字段 Tool 往往不是“能力强”

一种常见反模式：

```text
manage_resource(
  create_...,
  update_...,
  delete_...,
  permission_...,
  query_...,
  export_...,
  ...50 fields
)
```

再配大量 optional / nullable / conditional 字段。

结果往往是：

```text
巨大 action space
字段组合爆炸
模型难以理解分支
权限难以拆分
副作用难以区分
评测难以 attribution
```

如果不同操作具有不同权限、副作用、审批或 retry semantics，更应该拆成语义清晰的 Tool。

但反过来，拆成几百个几乎同义的小 Tool 又会增加 Tool Selection 难度。

所以：

> **Schema Granularity 与 Tool Granularity 是同一个 Action-Space Design 问题的两个视角。**

---

#### 3.2.24 Model-visible Schema 不应该等于 Backend API Schema

假设后端真实请求：

```json
{
  "tenant_id": "t_123",
  "user_id": "u_456",
  "auth_token": "secret",
  "request_id": "...",
  "resource_id": "r_789",
  "operation": "update"
}
```

不代表这些字段都应暴露给模型。

model-visible Tool Schema 可能只需要：

```json
{
  "resource_id": "r_789",
  "operation": "update"
}
```

其余 `tenant_id`、`user_id`、`auth_token`、`request_id` 应由 Harness / Runtime 根据 authenticated session 注入。

否则模型可能尝试生成其他 tenant 或更高权限 user，从而制造 privilege-confusion surface。

所以：

> **Model-controlled Arguments 与 System-controlled Execution Context 必须分离。**

完整请求应该是：

```text
Model-generated Args
+
Runtime-bound Identity / Credentials / Policy Context
↓
Backend Request
```

而不是让 LLM 生成整个 backend request。

---

#### 3.2.25 Secret / Credential 不应该让模型生成

API key、access token、cookie、private credential 等字段通常不应出现在模型可写的 Tool Schema 中。

原因不只是泄露风险，还因为 credential 本身代表 authority。

前面已经固定：

```text
Autonomy ≠ Authority
```

所以更合理的是：

```text
Agent chooses action
↓
Harness authorizes
↓
Runtime injects credential
↓
Tool executes under least privilege
```

而不是：

```text
Agent chooses credential
```

> **Credential 是 Runtime Authority Context，不是普通 Model Argument。**

---

#### 3.2.26 Unit、Currency、Timezone：不要把隐含单位藏起来

很多线上错误并不是复杂 reasoning 错，而是单位歧义。

```json
{"distance": 10}
```

到底是 10 meters、kilometers 还是 miles？

```json
{"amount": 100}
```

是 USD、JPY 还是 CNY？

```text
2026-10-18 09:00
```

没有 timezone，真实执行时间可能完全不同。

更好的设计是显式单位，例如：

```json
{
  "distance": 10,
  "unit": "km"
}
```

```json
{
  "amount": 100,
  "currency": "JPY"
}
```

时间使用明确 timestamp + timezone。

> **如果单位会影响真实 Action，就不能只靠人类默认常识。**

---

#### 3.2.27 Identifier Schema：名字和稳定 ID 不应混为一谈

用户可能说：

```text
给 Alice 发邮件
```

但真实执行可能需要：

```text
contact_id = cnt_8f13...
```

不应该让模型直接猜 opaque ID。

更可靠的流程：

```text
Human-readable reference
↓
resolve_contact("Alice")
↓
Candidate entities
↓
Disambiguation / selection
↓
Stable ID
↓
send_email(contact_id=...)
```

所以：

> **模型擅长理解名字，但真实副作用最好绑定稳定实体身份。**

---

#### 3.2.28 Normalization 与 Validation 也不同

例如：

```text
" Tokyo "
"TOKYO"
"tokyo"
```

可能希望映射到同一 canonical value。

这一步是：

```text
Normalization / Canonicalization
```

而不是 Validation。

典型流程：

```text
Raw Model Argument
↓
Normalize
↓
Validate
↓
Execute
```

可以安全规范 whitespace、case、标准日期表示，但不能盲目规范 opaque ID、hash、password、case-sensitive filename。

> **Normalization 应只做确定、无歧义的表示变换。**

---

#### 3.2.29 Mutating Tool 的 Schema 通常应该更严格

对于只读 Tool，如 search、list、inspect，有时可以接受较宽松的查询参数。

但对于：

```text
send
delete
publish
pay
modify permission
```

Schema 通常应该更严格。

例如更新文件：

```json
{
  "path": "src/a.py",
  "expected_version": "abc123",
  "patch": "..."
}
```

`expected_version` 可用于防止 stale write：

```text
read version = abc123
↓
Agent decides edit
↓
write only if current version == abc123
```

如果环境已经变化，就拒绝写入并返回 stale-state observation。

这就是 optimistic concurrency control 的思想。

---

#### 3.2.30 哪些字段由模型生成，哪些由系统绑定？

可以做一个实用分类。

**Model-controlled fields**：

```text
query
requested action
content draft
search filters
user-intent-derived parameters
```

**System-controlled fields**：

```text
authenticated user ID
tenant ID
credentials
permission scope
audit ID
trusted timestamp
approval token
sandbox root
```

**Environment-derived fields**：

```text
current object version
resolved entity ID
server capability
resource availability
```

这些来源不应该混成一个大参数对象全部让 LLM 填。

更稳的模式是：

```text
Model Intent
+
Trusted System Context
+
Fresh Environment State
↓
Validated Runtime Request
```

这也是防止 confused deputy、privilege escalation 与 stale-state action 的基础。

---

#### 3.2.31 Schema Evolution：改字段就是改 Agent 的 Action Protocol

Tool Schema 一旦被使用，就会影响：

```text
Prompt / Tool Definition
Model Tool Calls
Saved Trajectories
Replay
Evaluation Dataset
Caches
Logs
Harness Parser
Runtime Client
```

因此 Schema 变化不能只看成普通后端重构。

通常较兼容的变化：

```text
新增 optional field
增加 backward-compatible metadata
```

可能 breaking 的变化：

```text
required field rename
string → integer
删除 enum value
改变 default semantics
新增 required field
改变单位
改变 nullable semantics
```

重要 Tool 应维护 schema version、migration policy 和 compatibility tests。若 contract 不兼容，显式 v1/v2 往往比静默修改更安全。

---

#### 3.2.32 Schema Version 会影响 Agent 实验可复现性

假设两次 Agent Eval 使用：

```text
same model
same prompt
same benchmark
```

但 Tool Schema 从：

```text
operation = free string
```

变成：

```text
operation = enum
```

Tool-call success rate 的提升未必来自模型能力，可能只是 Action Interface 变简单了。

所以实验协议除了记录 model version、prompt version、decoding config，也应记录：

```text
tool schema version
```

> **Tool Schema 是 Agent Evaluation 的实验变量，不只是实现细节。**

---

#### 3.2.33 Batch Tool 还需要明确 Partial Success Semantics

例如：

```json
{"file_ids": ["a", "b", "c"]}
```

执行时：

```text
a success
b fail
c success
```

系统必须知道：overall success、partial success、是否 rollback、是否只 retry b。

这些不是 input Schema 单独能解决的，而属于 Tool Contract 的执行语义。

Schema 可以表达 batch size、atomic flag、per-item identity，但 `atomic` 是否允许模型决定，又涉及 Policy。

所以：

> **Schema 能表达选项，不代表模型天然有权决定这些选项。**

---

#### 3.2.34 一个好的 Tool Schema 应该如何评价？

不能只看 JSON Parse Rate。

更完整的指标包括：

```text
Syntactic Validity Rate
Schema Validation Pass Rate
Required-field Missing Rate
Unexpected-field Rate
Enum Violation Rate
Type Error Rate
Field-level Argument Accuracy
Normalized Argument Accuracy
Semantic Argument Accuracy
Permission Rejection Rate
Tool Execution Success
Downstream Task Success
```

尤其要注意：

```text
Schema Pass Rate ↑
```

不一定意味着：

```text
Argument Quality ↑
```

constrained decoding 可能把结构通过率推得很高，但模型仍可能选错 recipient、date 或 resource ID。

所以 Tool Eval 应分层 attribution：

```text
Tool Selection Error
Argument Structure Error
Argument Semantic Error
Policy Rejection
Execution Error
Observation-use Error
```

---

#### 3.2.35 常见 Failure Modes

Tool Schema 设计里常见的坑包括：

1. **Everything is string**：所有字段都是自由字符串，Schema 形同虚设。
2. **Everything is optional**：模型生成无法执行的半成品 Action。
3. **Required but unknowable**：要求模型生成当前 Context 根本不知道的字段，逼出 hallucination。
4. **Missing / null / empty conflation**：更新语义发生错误。
5. **Implicit type coercion**：字符串、布尔、数字被 Runtime 隐式转换。
6. **Identifier modeled as number**：前导零或精度丢失。
7. **Ambiguous units**：金额、距离、时间语义错误。
8. **Enum without abstention path**：模型被迫选错误类别。
9. **Overly permissive additional properties**：未知字段进入 Runtime。
10. **Giant mega-schema**：字段组合爆炸。
11. **Deep nested schema**：生成和调试困难。
12. **Overlapping union branches**：oneOf 分支语义模糊。
13. **Unsafe default**：缺字段时自动选择 destructive behavior。
14. **Backend schema directly exposed**：tenant、auth、internal control 字段全暴露给模型。
15. **Model-generated credentials**：把 Authority 交给 LLM 生成。
16. **Breaking schema drift**：旧 trajectory / client / evaluator 失效。
17. **Unbounded batch**：一次 Tool Call 放大成大规模 side effect。
18. **Schema-valid semantic error**：结构正确但实体、金额、日期、目标错误。
19. **Stale-state mutation**：没有 version/state precondition，覆盖新状态。
20. **Backend-centric field names**：模型被迫理解实现细节而不是业务语义。

---

#### 3.2.36 工程设计原则

可以压缩成十二条：

1. **Schema 最小但充分**：只暴露完成 Action 真正需要的参数。
2. **类型表达真实语义**：Identifier 不因长得像数字就用 integer。
3. **Required 只要求模型能可靠知道的字段**：不要用 required 强迫 hallucination。
4. **显式区分 missing / null / empty**：尤其是更新类 Tool。
5. **稳定有限集合优先 enum**：现实不完备时保留 unknown / abstain。
6. **单位、币种、时区显式化**：不要依赖默认常识。
7. **Action Schema 默认 closed**：除非确实需要 extension，否则不接受任意额外字段。
8. **不要依赖隐式类型转换**：Tool Boundary 尽量 deterministic。
9. **Credential / Identity / Authority 不交给模型生成**：系统可信上下文与模型参数分离。
10. **Schema Validation 与 Semantic / Policy Validation 分层**：结构合法不是业务合法。
11. **高风险 Tool 的 Schema 更严格**：关注稳定目标、并发状态和 side-effect scope。
12. **Schema 版本化、可测试、可观测**：它本身就是 Agent Protocol 的一部分。

---

#### 3.2.37 一个较好的 Read Tool Schema 示例

假设有：

```text
search_documents
```

可以设计成：

```json
{
  "query": "agent verification",
  "top_k": 10,
  "filters": {
    "source": "paper",
    "year_from": 2024
  }
}
```

概念 Schema：

```text
query:
  string
  required
  minLength = 1

top_k:
  integer
  optional
  1..20
  default = 5

filters:
  object
  optional
  additionalProperties = false

  source:
    enum [paper, docs, code]
    optional

  year_from:
    integer
    optional
```

这比：

```json
{"search_options": "找论文，最好新的，多给一点"}
```

更容易验证、缓存、评测和重放。

---

#### 3.2.38 一个 Write Tool Schema 示例：不要把 Authority 暴露出去

假设 Tool：

```text
update_ticket_status
```

model-visible Schema：

```json
{
  "ticket_id": "ticket_123",
  "status": "resolved",
  "comment": "Issue fixed and verified."
}
```

其中 `status` 是稳定 enum。

Runtime 另外绑定：

```text
actor_id
organization_id
permission_scope
audit_id
```

而不是要求模型生成这些可信身份字段。

完整链路：

```text
Model Args
+
Authenticated Runtime Context
↓
Schema Validation
↓
Semantic Validation
↓
Authorization
↓
Execution
↓
Verification
```

这比“LLM 直接拼 backend request”可靠得多。

---

#### 3.2.39 Coding Agent 示例：为什么需要 expected version？

假设 Agent：

```text
read_file("parser.py")
```

Observation：

```text
content = ...
version = abc123
```

Agent 思考后准备修改：

```json
{
  "path": "parser.py",
  "expected_version": "abc123",
  "patch": "..."
}
```

Runtime 执行前检查：

```text
current_version == abc123 ?
```

如果不是，就返回：

```text
STALE_STATE
file changed since last read
```

Agent 再重新读取、重新规划。

这样可以避免：

```text
旧 Observation
↓
过期 Patch
↓
覆盖别人的新修改
```

所以 Schema 也可以携带一部分 concurrency precondition。

---

#### 3.2.40 Tool Schema 与系统其他概念的边界

| 概念 | 核心职责 | 与 Tool Schema 的关系 |
|---|---|---|
| Tool Definition | 定义完整能力契约 | Schema 是 Input Contract 的一部分 |
| Tool Schema | 定义参数结构空间 | 不负责完整 Tool 语义 |
| Tool Description | 告诉模型 Tool / 字段用途 | 补充 Schema 无法表达的语义 |
| Parser | 把输出转换为对象 | 不判断是否符合 Schema |
| Schema Validator | 检查类型、字段与结构 | 不判断业务正确性 |
| Semantic Validator | 检查值是否符合领域规则 | 在 Schema 之后 |
| State Validator | 检查当前世界状态是否允许 | 需要 Environment State |
| Permission Check | 判断是否有执行权 | 不应由 Schema 替代 |
| Backend API Schema | 后端真实接口结构 | 不一定应完整暴露给模型 |
| Constrained Decoding | 生成时限制结构空间 | 可利用 Schema，但不保证语义正确 |
| Runtime Context | 可信身份、凭证、环境信息 | 应与 model-controlled args 分离 |
| Observation Schema | 约束 Tool Result 如何反馈 | 属于输出 contract，不是输入 schema |

---

#### 3.2.41 面试需要掌握到什么程度？

至少要能稳定回答：

**Q1：什么是 Tool Schema？**

> Tool Schema 是 Tool 输入参数的机器可读结构契约，定义字段、类型、required/optional、enum、bounds、nested structure 等，使模型生成的 Tool Call 能被程序验证和稳定消费。

**Q2：Tool Schema 和 Tool Description 有什么区别？**

> Schema 约束结构；Description 解释语义和使用场景。仅靠类型不足以表达完整 Tool 语义。

**Q3：Schema-valid 是否意味着 Action 正确？**

> 不意味着。还要经过 semantic validation、state/precondition validation、permission/policy check，执行后还需要 verification。

**Q4：required、optional、nullable 有什么区别？**

> required 表示必须出现；optional 表示可以缺失；nullable 表示出现时可以显式为 null。missing、null、empty 语义可能不同。

**Q5：为什么不能把所有字段都设 required？**

> 如果模型当前拿不到信息，会为了满足结构而 hallucinate required field。

**Q6：为什么推荐 enum？**

> 能压缩开放语言空间、减少同义词漂移并提升验证和评测稳定性，但类别不完备时需要 unknown / abstention path。

**Q7：为什么通常要禁止未知字段？**

> 可执行 Action 使用字段白名单，可以减少 schema drift、未知参数和注入风险。

**Q8：为什么 Backend API Schema 不应该直接给 LLM？**

> 后端接口常包含 tenant、credential、actor、audit 等可信系统字段。模型只应控制与用户意图相关的参数，Authority Context 应由 Runtime 注入。

**Q9：为什么 ID 常用 string 而不是 integer？**

> Identifier 不用于数学运算，可能含前导零、超过数值精度或具有固定编码格式。

**Q10：Constrained Decoding 能解决 Tool Calling 正确性吗？**

> 只能提高结构合法性，不能保证 Tool 选择、实体、日期、金额、权限等语义正确。

**Q11：Schema 为什么也是 Agent 实验变量？**

> Schema 会改变 Action Space、生成难度和验证边界，不同 Schema 下 success rate 的变化不能简单归因于模型能力。

**Q12：Tool Schema 太严格和太宽松分别有什么问题？**

> 太宽松增加歧义和非法组合；太严格可能逼模型 hallucinate 或无法表达 unknown。目标是最小、充分、可验证且与业务语义对齐。

---

#### 3.2.42 一句话总结

> **Tool Schema 的核心不是“把参数写成 JSON”，而是把 Agent 可表达的 Action Argument Space 变成一个明确、可验证、可版本化的结构契约；它负责结构边界，却不能替代语义正确性、环境状态、权限控制和执行后的 Verification。**

进一步压缩：

```text
Tool Schema
=
Structured Action Space
+
Machine-checkable Input Contract
```

但可靠执行仍然需要：

```text
Schema Validation
+
Semantic Validation
+
State Validation
+
Authorization
+
Execution
+
Verification
```

---

#### 3.2.43 参考资料

- JSON Schema. **JSON Schema Specification**. 用于理解 JSON 数据结构、类型、组合约束与 validation vocabulary 等基础思想。
- OpenAPI Initiative. **OpenAPI Specification**. 用于理解 API operation、parameters、request/response schema 与机器可读接口契约。
- Yao S, Zhao J, Yu D, et al. **ReAct: Synergizing Reasoning and Acting in Language Models**. ICLR 2023. 从 Agent action–observation loop 角度理解结构化 Tool Action 的系统位置。
- Schick T, Dwivedi-Yu J, Dessì R, et al. **Toolformer: Language Models Can Teach Themselves to Use Tools**. NeurIPS 2023. 从模型学习 Tool 使用与 argument generation 的角度理解 Tool 接口设计的重要性。
- Qin Y, Liang S, Ye Y, et al. **ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs**. ICLR 2024. 从大规模 API / Tool ecosystem 角度理解 heterogeneous schemas、tool selection 与 execution 的现实复杂性。

