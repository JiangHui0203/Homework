# 2. Pretraining、Instruction、SFT 与 Post-training Data

> 本章目标：把“大模型训练数据”这个经常被混在一起的概念拆开。
>
> 核心问题：**模型从“会续写文本”到“会听懂指令、遵循约束、调用工具并完成任务”，各阶段的数据究竟在教它什么？**

如果只记一句话，可以先记：

```text
Pretraining：学“世界和语言长什么样”
Instruction / SFT：学“用户让我做事时应该怎么回应”
Preference / RL：学“多个可行行为里哪一种更值得选择”
Agent Data：学“在环境里如何连续决策并真正把事情做完”
```

但现实中这些边界并不是绝对的。现代模型会使用 continued pretraining、instruction tuning、SFT、preference optimization、RL、verifiable reward 等多种阶段，数据也会交叉复用。理解它们时，不要只按“训练算法名字”分类，更要看**这批数据提供了什么监督信号**。

---

## 2.1 Pretraining Data：先学会预测“接下来会出现什么”

### 2.1.1 Pretraining Data 是什么？

最经典的 decoder-only LLM 预训练目标是 next-token prediction。

给定 token 序列：

$$
x_1, x_2, \ldots, x_T
$$

模型学习最大化：

$$
\sum_{t=1}^{T} \log P(x_t \mid x_{<t})
$$

或者等价地最小化 token-level cross entropy。

此时数据通常不是：

```text
Question → Answer
```

而只是大量自然产生的 token sequence，例如：

```text
网页文章
书籍
百科
论坛
新闻
代码仓库
论文
文档
问答网站
多语言文本
数学内容
```

模型不需要显式知道“这条数据是在教历史知识还是教语法”。它只是在巨量语料中学习统计规律、语言结构、事实关联、代码模式、推理模式和世界知识。

因此：

> **Pretraining Data 的基本监督信号不是人工标签，而是文本本身的下一个 token。**

---

### 2.1.2 为什么预训练数据规模可以特别大？

因为它天然属于 self-supervised learning。

原始文本：

```text
深度学习模型通常通过梯度下降优化参数。
```

可以自动变成许多训练位置：

```text
深度 → 学习
深度 学习 → 模型
深度 学习 模型 → 通常
...
```

不需要人工逐条标注。

这解释了一个重要现象：

```text
Pretraining
数据量巨大
人工标注比例低
监督信号自动产生

Post-training
数据量通常小得多
但单条数据更贵、更有目的性
```

所以“数据量”不能脱离训练阶段比较。

---

### 2.1.3 预训练数据常见来源

可以粗略分成：

#### Web Data

```text
网页
论坛
博客
新闻
知识站点
公开文档
```

优势是规模大、覆盖广；问题是噪声、广告、重复、SEO 文本、低质生成内容和隐私/版权风险都更明显。

#### Books / Long-form Text

更容易提供：

- 长篇连贯结构；
- 复杂叙事；
- 跨段依赖；
- 高质量自然语言。

#### Code

代码数据不只教“写代码”，还提供非常强的结构信号：

```text
syntax
function dependency
API usage
tests
error handling
program structure
```

这也是为什么代码能力与 Agent 的工具调用、结构化输出、程序化推理有一定关联。

#### Academic / Technical Data

包括论文、教材、技术文档、规范、专业资料等。它们对专业领域知识、符号系统、推理表达和术语覆盖很重要。

#### Multilingual Data

决定模型对不同语言的覆盖程度。这里不是“只要混进去就行”，还要处理语言识别、语种比例、翻译腔、跨语言重复和资源极不平衡的问题。

---

### 2.1.4 预训练数据真正的工作，不是“下载完就训练”

一个简化 pipeline 往往更像：

```text
Raw Sources
    ↓
Ingestion / Parsing
    ↓
Normalization
    ↓
Language / Domain Identification
    ↓
Quality Filtering
    ↓
Safety / Privacy Filtering
    ↓
Deduplication
    ↓
Contamination Check
    ↓
Sampling / Mixture
    ↓
Tokenization
    ↓
Training Shards
```

每一步都可能改变最终模型能力。

例如：

- 网页解析错了，会留下导航栏、乱码和广告；
- 去重过弱，会让高频网站被重复记忆；
- 去重过强，也可能误删真正不同但主题相近的文本；
- 质量过滤器偏英语风格，可能误伤其他语言；
- 代码过滤过重，会让模型丢失长尾 API；
- benchmark contamination 没查好，会让评测分数失真。

因此预训练数据工程的核心不是简单 ETL，而是：

> **通过数据分布设计，塑造基础模型能看到怎样的世界。**

---

### 2.1.5 Deduplication 为什么重要？

重复数据会带来至少三个问题。

#### 1. 浪费训练预算

如果同一篇文章出现 100 次，模型相当于反复花 token 预算学习同一个东西。

#### 2. 扭曲真实分布

某个网站因为爬虫结构被重复抓取，并不意味着这个知识在真实世界里应该占 100 倍权重。

#### 3. 放大记忆与 contamination

如果 benchmark 题目或其近似版本反复出现，模型评测时可能是在“见过题”而不是泛化。

去重可以发生在多个层级：

```text
exact duplicate
near duplicate
paragraph-level duplicate
document-level duplicate
semantic duplicate
```

后面 Data Curation 会详细展开。

---

### 2.1.6 Pretraining contamination 是什么？

假设某 benchmark 的测试题出现在预训练语料里：

```text
Benchmark test item
        ↓
进入 pretraining corpus
        ↓
模型训练时见过
        ↓
Benchmark evaluation
```

那么测试分数可能混入记忆效应。

这里需要区分：

- exact contamination：测试题原文直接出现；
- near contamination：轻微改写版本出现；
- solution contamination：题目或答案解析出现；
- benchmark-family exposure：没见过该测试题，但见过大量高度模板化同源题。

因此 contamination 不是简单 grep 一次就能完全解决的问题。

---

### 2.1.7 Pretraining Data 与 Instruction Data 的根本区别

看两个例子。

#### Pretraining-like text

```text
牛顿第二定律描述了物体受到的合外力与加速度之间的关系……
```

#### Instruction Data

```text
User:
请用高中生能理解的方式解释牛顿第二定律。

Assistant:
你可以把它理解成……
```

两者都可能教模型“牛顿第二定律”，但学习信号不同。

前者主要让模型学习：

> **什么文本通常接在什么文本后面。**

后者额外让模型学习：

> **当用户以这种方式提出需求时，应该采取怎样的响应行为。**

因此不能简单认为：

> “预训练里有大量问答网页，所以就不需要 instruction tuning。”

模型在预训练阶段可能学会了问答文本的统计模式，但未必稳定学会**把当前用户指令当作需要遵循的任务**。

---

## 2.2 Instruction Data：把“文本续写”变成“任务响应”

### 2.2.1 什么是 Instruction Data？

最基本结构是：

```text
Instruction
    ↓
Desired Response
```

例如：

```json
{
  "instruction": "把下面这段话改得更正式",
  "input": "这个方案还行，就是有点贵。",
  "output": "该方案整体可行，但成本相对较高。"
}
```

Instruction Data 的重点不是只提供知识，而是显式建立：

```text
用户意图
   ↓
期望行为
```

这种映射。

---

### 2.2.2 Instruction Data 可以教什么？

它可以教的不只是“回答知识问题”。

常见能力包括：

```text
问答
摘要
翻译
改写
分类
信息抽取
数学求解
代码生成
结构化输出
格式遵循
角色约束
拒绝不安全请求
多轮对话
工具调用
Agent 任务分解
```

因此 instruction data 往往需要按 capability taxonomy 来设计，而不是随机收集问题。

---

### 2.2.3 Single-turn 与 Multi-turn Instruction

#### Single-turn

```text
User → Assistant
```

适合教局部能力。

#### Multi-turn

```text
User
↓
Assistant
↓
User clarification / correction
↓
Assistant update
↓
...
```

多轮数据能教模型：

- 继承前文约束；
- 解析指代；
- 根据用户纠正更新答案；
- 不重复已经问过的问题；
- 维持任务状态；
- 处理上下文冲突。

Agent 场景里多轮数据尤其重要，因为一次任务往往不会在一轮内完成。

---

### 2.2.4 Message Role 也是数据的一部分

现代 chat 模型的数据常具有角色结构：

```text
System
Developer
User
Assistant
Tool
```

从数据视角看，模型必须学到的不只是文本内容，还包括**不同消息来源之间的控制关系和语义边界**。

例如：

```text
System: 只能使用提供的工具查询库存。
User: 你直接猜一个库存数字给我。
```

一个好的 instruction / SFT sample 不应该只训练语言流畅度，还需要训练：

```text
遵循高优先级约束
识别用户意图
知道何时需要工具
不虚构环境状态
```

因此 instruction data 的 schema 本身会影响模型行为。

---

### 2.2.5 Formatting Constraint 也是能力

例如：

```text
“只返回 JSON，不要解释。”
```

模型要学会：

```json
{"label":"positive"}
```

而不是：

```text
当然可以！结果如下：
{"label":"positive"}
```

在人类看来后者也“回答对了”，但对 API / Agent pipeline 来说可能已经失败。

因此 instruction following 数据里必须覆盖：

- 长约束；
- 多约束；
- 格式约束；
- 正负约束；
- 条件约束；
- 跨轮约束。

---

## 2.3 SFT Data：用示范告诉模型“应该怎么做”

### 2.3.1 SFT 是什么？

SFT = Supervised Fine-Tuning。

最直观地说，就是给模型大量高质量 demonstration：

```text
Prompt x
   ↓
Desired Response y*
```

然后最大化目标回答 token 的条件概率：

$$
\log P(y^* \mid x)
$$

从 learning signal 的角度：

> **SFT 是 imitation learning：让模型模仿被认为是正确、优质的示范。**

---

### 2.3.2 一条 SFT 数据长什么样？

最简单：

```json
{
  "messages": [
    {"role": "user", "content": "法国首都是哪里？"},
    {"role": "assistant", "content": "巴黎。"}
  ]
}
```

复杂一点可以包含多轮：

```text
System
↓
User
↓
Assistant
↓
User
↓
Assistant
```

Agent SFT 还可能包含：

```text
User task
↓
Assistant tool call
↓
Tool observation
↓
Assistant next tool call
↓
Tool observation
↓
Assistant final response
```

所以 SFT 并不等于“问答数据”。**任何希望模型直接模仿的行为序列，都可以成为 SFT demonstration。**

---

### 2.3.3 SFT 数据从哪里来？

#### Human-written / Expert-written

优点：

- 可控；
- 能表达真正专家行为；
- 适合复杂领域与高标准任务。

缺点：

- 贵；
- 慢；
- 难扩展；
- 标注者风格可能高度集中。

#### Existing High-quality Data

例如公开 instruction 数据、领域数据、历史产品数据。

问题是需要特别关注：

- license；
- 数据质量；
- 训练/评测泄漏；
- schema 是否一致；
- 是否真的适配当前模型和产品目标。

#### Synthetic Data

常见流程：

```text
Task / Seed
   ↓
Teacher Model
   ↓
Candidate Response
   ↓
Filter / Verify
   ↓
SFT Data
```

现代 SFT 中 synthetic data 很常见，但核心不是“模型生成了就能训”，而是**生成 + 验证 + 筛选**。

#### Successful Rollout

对于 Agent：

```text
任务
↓
模型跑出若干 trajectory
↓
环境验证 success
↓
筛掉异常路径
↓
成功轨迹作为 demonstration
```

这会自然连接到后面的 rejection sampling 和 agent trajectory data。

---

### 2.3.4 SFT 最擅长教什么？

SFT 非常适合教：

#### 1. 输出格式

```text
JSON
XML
tool call schema
固定模板
```

#### 2. 交互习惯

例如：

```text
什么时候先澄清
什么时候直接回答
什么时候调用工具
怎样引用工具结果
```

#### 3. 行为模式

```text
遇到代码题 → 写代码 + 测试
遇到搜索任务 → 先查证再回答
遇到工具错误 → 根据 observation 修正
```

#### 4. 风格

例如简洁、专业、结构化、避免废话。

#### 5. 基础任务能力的激活与对齐

预训练模型可能“知道”某些知识或模式，但 SFT 帮助它把这些能力稳定地映射到用户指令上。

---

### 2.3.5 Positive-only Imitation 的局限

SFT 常常只告诉模型：

> “这是一个好答案，请模仿。”

但没有直接告诉模型：

> “这个看起来也合理的答案为什么更差？”

例如：

```text
Prompt

Good response A
Bad-but-plausible response B
```

如果训练集只有 A，模型能学到 A 的模式，但并没有显式获得：

```text
A > B
```

这种相对偏好信号。

因此 SFT 的典型局限包括：

- 难表达“两个都能做，但哪个更好”；
- 难利用大量失败 candidate 的信息；
- 对细微风格和行为偏好的区分能力有限；
- 对 long-horizon credit assignment 支持有限。

这就是为什么 SFT 后面经常还会接 Preference Optimization / RL。

---

### 2.3.6 SFT 数据不是越“完美”越好

一个常见误区是：

> 只要所有回答都非常完美，SFT 就一定最好。

实际要考虑目标分布。

如果线上用户经常给出：

```text
错别字
模糊需求
半句话
多约束
互相冲突的要求
工具失败
```

而训练数据全部是：

```text
清晰、完整、标准、单轮 instruction
```

模型会面临 distribution shift。

因此高质量不等于“干净得不真实”。高质量数据应该是：

> **真实覆盖目标行为分布，同时拥有可靠监督信号。**

---

## 2.4 Post-training Data：从“会生成”到“会按目标行为”

### 2.4.1 Post-training 是什么？

广义上，pretraining 之后为了塑造模型行为进行的训练，都可以归到 post-training 讨论范围。

一个非常简化的框架是：

```text
Base Model
   ↓
SFT
   ↓
Preference / Reward Modeling
   ↓
RL / Preference Optimization
   ↓
Capability / Safety / Tool-use refinement
   ↓
Deployed Model
```

现实中的训练 recipe 可能并不会严格按这个顺序，也可能循环多轮。

---

### 2.4.2 Post-training Data 不等于 SFT Data

这是非常容易混淆的一点。

```text
SFT Data ⊂ Post-training Data
```

Post-training 还可能包括：

```text
Preference pairs
Ranked candidates
Reward labels
Critiques
Step-level process labels
RL rollout
Verifier outcome
Tool execution feedback
Safety adversarial data
Agent success / failure trajectory
```

因此，当岗位说“负责 post-training data”时，实际工作可能远远超过 instruction-response 标注。

---

### 2.4.3 Post-training 的核心：从“模仿答案”升级到“优化行为”

可以这样理解：

#### SFT 问：

> 一个好示范长什么样？

#### Preference 问：

> 两个答案里哪个更好？

#### Reward 问：

> 这条行为到底有多好？

#### RL / rollout 问：

> 当前模型自己会走出哪些路径，哪些路径值得强化？

#### Agent environment 问：

> 这条轨迹有没有真实完成任务？

所以 post-training data 越往后，越接近**模型当前策略产生的实际行为分布**。

---

### 2.4.4 On-policy 与 Off-policy 数据直觉

不用先陷入严格 RL 定义，可以先建立一个数据直觉。

#### Off-policy-like

数据主要来自别的分布：

```text
人工专家答案
teacher model 输出
历史模型 trajectory
公开数据集
```

当前模型只是去学习它们。

#### On-policy-like

让**当前模型本身**去 rollout：

```text
Current Model
    ↓
Generate candidates / trajectories
    ↓
Reward / Verify
    ↓
Use feedback to improve Current Model
```

优点是数据直接暴露当前模型真正会犯的错误。

这也是为什么后续 Agent data flywheel 会特别关注线上 trace 和 current-policy rollout。

---

### 2.4.5 Verifiable Tasks 为什么越来越重要？

如果任务结果可以自动验证：

```text
数学答案 → symbolic / exact verifier
代码 → unit tests / execution
Agent → final environment state
数据库任务 → SQL / state check
网页任务 → target state
```

那么可以低成本跑大量 rollout：

```text
1 task
↓
N trajectories
↓
automatic verification
↓
success / failure
↓
training signal
```

这比“每一条都请人工专家判断”更容易扩展。

因此现在很多 reasoning / agent data pipeline 都在追求：

> **生成成本可控 + 结果可验证 + 能大规模 rollout。**

---

## 2.5 Data Mixture：为什么“配数据”本身就是研究问题？

假设你有：

```text
数学数据 100 万
代码数据 80 万
通用问答 500 万
多轮对话 20 万
工具调用 5 万
安全数据 10 万
```

训练时直接全部拼起来，并不意味着模型会得到理想能力。

真正的问题是：

> **每一种数据应该以多大权重进入训练？**

这就是 mixture design。

---

### 2.5.1 为什么不能简单按原始数据量采样？

假设：

```text
General chat = 90%
Tool-use = 1%
```

如果严格按原始比例训练，模型几乎很少见到 tool-use。

结果可能是：

> 明明收集了 10 万条工具数据，但它在总 token 中被淹没，能力提升很小。

因此常用方法包括：

```text
oversampling
undersampling
source weighting
domain weighting
capability weighting
```

---

### 2.5.2 Token 比 Sample Count 更接近真实训练权重

1000 条短分类数据与 1000 条长 Agent trajectory，不是同一个量级。

例如：

```text
Dataset A
1000 samples × 100 tokens = 100k tokens

Dataset B
1000 samples × 5000 tokens = 5M tokens
```

如果只看 sample count，会严重误判 mixture。

所以需要同时跟踪：

```text
sample count
token count
source share
capability share
language share
length distribution
```

---

### 2.5.3 Domain Balancing

例如医学模型不应该简单变成：

```text
99% 医学
1% 通用能力
```

因为可能造成 general capability regression。

所以数据配比常常是在优化：

```text
目标领域提升
        vs
通用能力保持
```

这就是典型 trade-off。

---

### 2.5.4 Curriculum：数据顺序也可能重要

Curriculum learning 的直觉是：

```text
基础 → 复杂
简单 → 困难
短任务 → 长任务
单工具 → 多工具
```

例如 Agent 训练可以设计成：

```text
Stage 1: 单步 function calling
Stage 2: 两步工具链
Stage 3: 多工具依赖
Stage 4: 长时程任务 + failure recovery
```

但 curriculum 不是天然优于随机混合；是否有效必须通过实验验证。

---

### 2.5.5 Mixture 的核心不是“平均”，而是目标函数

更正确的思考是：

```text
我们希望优化哪些能力？
↓
每种能力目前差多少？
↓
什么数据最可能提供有效学习信号？
↓
训练预算有多少？
↓
如何配比？
```

也就是：

> **Mixture 是一种资源分配问题。**

---

## 2.6 Continued Pretraining、SFT、Preference：不要只看数据格式

一条文本长得像问答，不意味着它一定是 SFT；一条自然语言文档也可能用于 continued pretraining。

判断数据类型时应问：

```text
训练目标是什么？
loss 作用在哪些 token？
模型是在模仿 demonstration，还是比较 candidate？
有没有 reward / verifier？
数据是当前模型 rollout 的吗？
```

一个简化对照表：

| 阶段 | 典型数据 | 主要学习信号 | 最主要作用 |
|---|---|---|---|
| Pretraining | 海量 token sequence | next-token prediction | 语言、知识、通用模式 |
| Continued Pretraining | 领域原始语料 | next-token prediction | 增强领域分布覆盖 |
| Instruction Tuning | instruction-response | demonstration | 建立指令到行为映射 |
| SFT | 高质量目标行为 | imitation | 稳定行为、格式和能力 |
| Preference Optimization | chosen / rejected | relative preference | 学“哪个更好” |
| Reward Modeling | candidate + score/rank | reward signal | 学评价函数 |
| RL / Verifiable RL | rollout + reward | outcome / reward | 优化当前策略 |
| Agent Training | task + environment + trajectory | action/outcome/process signal | 学连续决策与任务完成 |

---

## 2.7 一个完整案例：教模型学会“查库存再回答”

假设目标能力是：

> 用户问商品库存时，模型不能凭记忆猜，要调用库存工具并根据真实返回回答。

### 只靠 Pretraining 会怎样？

模型可能见过：

```text
“某商品通常有库存……”
```

于是它学会生成看起来合理的库存回答，但它并不知道当前真实库存。

### 加 SFT

训练示范：

```text
User:
A100 显卡还有货吗？

Assistant tool call:
check_inventory(product="A100")

Tool:
{"stock": 3}

Assistant:
目前还有 3 件库存。
```

模型开始学会：

```text
库存问题 → 调库存工具 → 基于 observation 回答
```

### 再加入失败数据 / Preference

候选 A：

```text
我猜应该还有货。
```

候选 B：

```text
先调用 check_inventory，再根据返回回答。
```

标签：

```text
B > A
```

模型进一步学到：

> “直接猜”比“真实查询”差。

### 再做 Agent rollout

让当前模型自己处理 1 万个库存任务：

```text
成功
漏调用工具
参数错误
调用后忽略 observation
工具失败后仍声称成功
```

环境自动判定最终 answer 是否与 inventory state 一致。

此时数据工作已经从：

> 写标准答案

升级成：

> **构造任务 → 运行模型 → 收集轨迹 → 验证状态 → 分析失败 → 回流训练。**

这就是后面 Agent Data Flywheel 的雏形。

---

## 2.8 一条训练数据到底“好不好”，看什么？

不能只问“有没有语法错误”。

对于 SFT / Post-training Data，可以从以下维度检查：

### Correctness

答案、工具调用、状态变化是否真实正确？

### Instruction Following

是否真正满足用户所有显式约束？

### Behavioral Validity

这个行为是不是我们希望模型以后模仿的？

例如一个答案事实正确，但先胡乱调用了 8 次无关工具，也不应作为理想 Agent demonstration。

### Difficulty

是不是模型已经 99.9% 都会了？如果是，新增 10 万条可能边际价值很低。

### Diversity

是否只是模板替换？

```text
查询订单 1
查询订单 2
查询订单 3
...
```

表面上有 1 万条，实际 decision pattern 只有一种。

### Coverage

是否覆盖真正重要的 failure mode？

### Verifiability

标签能否可靠验证？

### Naturalness

是否符合真实用户分布，而不是全是模型生成的“教科书式问题”？

### Learning Value

最终要问：

> **这条数据加入训练后，是否有机会改变模型在目标能力上的行为？**

这比“这条数据看起来不错”更重要。

---

## 2.9 常见失败模式

### 失败 1：把所有“训练数据”都叫 SFT Data

会混淆 demonstration、preference、reward、rollout 等完全不同的学习信号。

### 失败 2：Teacher 越强，Synthetic Data 就一定越好

Teacher 也会带来系统性偏差、风格单一和错误模式。强 teacher 不等于自动得到高价值 student data。

### 失败 3：只看数据条数，不看 token 和 decision diversity

Agent trajectory 往往很长，只看 sample count 容易误判实际训练权重；模板化 synthetic data 又可能造成“条数很多、决策模式很少”。

### 失败 4：只做正例，不分析失败

如果当前模型最常犯的是：

```text
漏工具调用
```

但新增数据都只是普通高质量问答，那么数据并没有瞄准真正瓶颈。

### 失败 5：训练集质量很好，但和线上分布不一致

例如线上大量是模糊、多轮、短句、错别字、工具错误，而训练集全是标准单轮问题。

### 失败 6：训练数据和 Eval 混在一起

一旦 benchmark case 被有针对性地加入训练，再使用同一 benchmark 宣称能力提升，就可能把“泛化提升”和“记住测试集”混淆。

### 失败 7：Data Mixture 没有版本记录

如果最终只知道：

```text
“我们加了一批代码数据，效果涨了。”
```

却不知道：

```text
加了多少？
哪些 source？
多少 token？
采样权重多少？
过滤了什么？
模型版本是什么？
```

这个实验几乎无法复现，也无法沉淀为数据策略。

---

## 2.10 从数据岗位视角，这一章对应哪些实际工作？

可能是：

```text
抓取 / 接入原始语料
清洗 HTML / 文档
语言识别
质量打分
去重
PII / safety filtering
benchmark contamination 检查
instruction taxonomy 设计
SFT 样本生产
teacher model 批量生成
candidate filtering
数据配比
token 统计
训练集版本管理
训练前质量 audit
训练后 capability regression analysis
```

所以“做大模型数据”并不等于一个单独岗位动作，而是一整条从**数据来源 → 数据结构 → 学习信号 → 训练目标 → 效果验证**的链路。

---

## 2.11 本章关键词

| 术语 | 一句话理解 |
|---|---|
| Pretraining Data | 用于 next-token learning 的大规模原始语料 |
| Self-supervised Learning | 监督信号从数据本身自动构造 |
| Instruction Data | 显式描述“用户要求 → 期望响应”的数据 |
| SFT | 用高质量 demonstration 让模型模仿目标行为 |
| Continued Pretraining | 在目标领域语料上继续做语言模型训练 |
| Post-training | 预训练之后用于塑造能力和行为的一系列训练阶段 |
| Data Mixture | 多种数据源 / 能力数据的训练配比 |
| Oversampling | 提高某类数据在训练中的采样权重 |
| Curriculum | 按难度或能力阶段组织训练数据 |
| Contamination | 测试信息泄漏进入训练数据 |
| On-policy Rollout | 由当前策略自身生成训练经验 |
| Verifiable Task | 结果可通过规则、执行或环境状态可靠验证的任务 |

---

## 2.12 面试 / 自检问题

学完这一章至少应该能够回答：

1. **Pretraining Data 和 SFT Data 的根本区别是什么？**
2. **Instruction tuning 和 SFT 是完全同义的吗？**
3. **为什么 SFT 通常不够，还需要 preference / reward？**
4. **为什么 synthetic SFT data 不能 teacher 生成完直接用？**
5. **为什么 Agent 数据不能只统计 sample 数？**
6. **Data mixture 为什么会显著影响模型能力？**
7. **什么是 contamination，它为什么会让 benchmark 失真？**
8. **continued pretraining 和 SFT 分别适合解决什么问题？**
9. **为什么 current-model rollout 对后训练数据特别重要？**
10. **如果新增 10 万条数据模型没涨，你会从哪些角度排查？**

第 10 题可以使用一个通用分析框架：

```text
数据真的正确吗？
↓
数据覆盖目标 failure 吗？
↓
数据对当前模型有难度吗？
↓
数据在 mixture 中权重够吗？
↓
监督信号和目标行为一致吗？
↓
训练是否真的消费了这些数据？
↓
Eval 是否能测到预期能力？
↓
是否发生其他能力 regression？
```

这条链路以后会反复出现。
