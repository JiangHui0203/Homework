# LLM / Agent Data Knowledge System：Figure Design Contract

> 状态：`Stable Mother Edition V3.x / Visual Production Contract`
>
> 目的：把 F1–F14 从“逻辑正确的 Mermaid 图”进一步稳定成一套可长期维护、可出版重绘、可单独截图传播的视觉系统。
>
> 核心原则：**Mermaid 是 semantic source of truth；SVG / PPT / PDF / image redraw 是 presentation derivative。视觉可以升级，但 canonical relation 不允许在重绘过程中静默改变。**

---

# 0. 一张 Master Figure 必须回答一个问题

每张图必须能用一句问题定义自己的认知任务：

```text
F1  这本书到底描述什么 Learning System？
F2  Data Object 怎样从 Example 扩展为 Experience？
F3  一个 Reasoning State 上到底要区分哪五种判断？
F4  Agent 的 Task / Tool / Harness / Environment / Trajectory 怎么连接？
F5  一条 Trajectory 到底应该记录什么？
F6  从 Outcome 到 Credit / Failure / Root Cause 应怎样拆？
F7  一条 Label 到底建立在什么 Evidence 和 Evaluator 上？
F8  “方法更好”这个结论怎样才成立？
F9  一个真实 Failure 怎样重新进入 Learning Loop？
F10 有限 Data Budget 应该投到哪里？
F11 一个模型 / 结论怎样追溯回原始 Evidence？
F12 高价值 Experience 怎样被稳定规模生产？
F13 指标变化以后首先应该排查什么？
F14 团队和个人怎样调用整套系统？
```

如果一张图同时想回答两个同等重要的问题，应拆图，而不是继续堆节点。

---

# 1. Figure Header Contract

F1–F14 文件顶部统一包含：

```text
Figure Question
Level
Canonical Owner
Primary Case
Scope
```

推荐格式：

```markdown
# F6 — Credit → Failure Causal Map

> **Figure Question：** 从一个 Outcome 到 Root Cause / Owner，因果链应该怎样拆？
>
> **Level：** Book-level
>
> **Canonical Owner：** Ch13–14
>
> **Primary Case：** `C1-F1` + `C3-F5`
>
> **Scope：** 固定全书 Credit / Failure 的全局关系；章节局部 pipeline 只作为 analytical lens。
```

目的不是增加格式感，而是让任何一张图被单独打开时也知道：

```text
它回答什么
它属于哪个尺度
谁拥有定义权
用什么 case 解释
它不负责什么
```

---

# 2. Arrow Grammar

统一使用两种主关系，不增加过多视觉编码。

## Solid Arrow `-->`

表示：

```text
Execution
State Transition
Causal / Operational Progression
Primary Pipeline
```

例如：

```text
Action --> Tool --> Environment --> World State
```

或：

```text
Evidence --> Evaluator --> Judgment --> Label
```

## Dashed Arrow `-.->`

表示：

```text
Evidence supports
Feedback
Derived relation
Measurement / Annotation
Auxiliary reference
```

例如：

```text
Future Outcome -.-> Recoverability Label
```

或：

```text
Gold Set -.-> Meta-evaluation
```

如果同一图中的虚线承担不同语义，必须给 edge 加短 label，而不是让读者猜。

---

# 3. Node Grammar

不依赖颜色表达核心意义，优先保证 GitHub Light / Dark Mode、打印和导出稳定。

推荐语义：

```text
[Rectangle]
→ Object / Process / Artifact

{Diamond}
→ Decision / Gate / Question

Subgraph
→ Layer / Phase / Owner boundary
```

图中节点文字规则：

1. 一般不超过两行。
2. 第一行写 canonical term，第二行才写解释。
3. 不在节点中塞完整定义。
4. 同一概念始终使用 Glossary canonical spelling。
5. Case variant 使用稳定 ID，如 `C1-VB`、`C4-SC`。

---

# 4. Visual Hierarchy

每张 Master Figure 优先呈现：

```text
Primary Spine
+
最多 1–2 层辅助 branch
```

Primary Spine 应该让读者在 5–10 秒内看懂。

避免：

```text
每个知识点都放进图
```

因为 Master Figure 的任务是压缩关系，不是代替正文。

推荐节点数量：

```text
Book-level F1/F4/F6/F8/F9/F14
主干约 6–12 个核心节点

Part-level F2/F3/F5/F7/F10/F11/F12/F13
主干约 5–10 个核心节点
```

不是硬限制；如果超出，应重新检查是否混入 chapter-local 细节。

---

# 5. Figure Body Contract

每个 figure 文件在 Mermaid 之后统一优先使用以下四类说明。

## A. Read the Spine

用 1 个短块说明主链：

```text
A → B → C → D
```

回答“第一眼应该怎么看”。

## B. Critical Boundaries

只保留本图最容易混淆的 2–5 条：

```text
Outcome ≠ Reward ≠ Credit
Tool ≠ Harness ≠ Environment
Evidence ≠ Label
```

## C. Case Lens

使用稳定 Canonical Case ID 说明图怎样落到真实任务。

## D. Cross-links

只链接真正相关的：

```text
Owner chapters
Adjacent Master Figures
Canonical Case file
```

不把 figure file 变成第二套目录页。

---

# 6. Caption Contract

未来导出 SVG / PPT / PDF 时，每张图至少有一个可独立使用的 caption：

```text
F6 — Credit → Failure Causal Map.
A failed episode should not jump directly from outcome to root cause:
credit localization, harmful action, recoverability, mechanism and owner are distinct questions.
```

中文版可以更自然，但必须满足：

```text
1 句话说明图在解决什么问题
+
1 句话说明最重要的边界
```

不要写：

```text
“图 6 展示了相关流程。”
```

---

# 7. Case Marking Rule

Case 在图里只承担两种角色：

```text
Primary Case
→ 帮助解释整张图

Boundary Case
→ 专门证明一个容易混淆的边界
```

例如 F6：

```text
C1-F1
→ Model / Policy-owned failure

C3-F5
→ Harness-owned failure
```

这样一组 case 是为了证明：

```text
Failure Layer ≠ Failure Owner
```

不是为了“图里多放案例”。

---

# 8. Publication Redraw Rule

未来如果用 Figma / Illustrator / PowerPoint / image generation 重画：

```text
Mermaid source
= semantic authority

Redrawn SVG / PNG / PPT
= presentation artifact
```

必须保留：

```text
Figure ID
semantic_version
source Mermaid path
redraw_version
```

如果 redraw 需要改变：

```text
node semantics
edge semantics
canonical concept relation
```

不能只改图片；必须先回写 Mermaid / Master Figure source，再更新 derivative。

---

# 9. Suggested Export Families

未来可以从同一个 semantic source 派生三套输出。

## Book / PDF

```text
完整 Figure
+ caption
+ Case Lens
```

## Slides / Talk

```text
Primary Spine only
→ progressive reveal
```

## Social / Interview Quick Reference

```text
一个 Figure
+ 3 个关键边界
+ 1 个 case
```

这样同一套图可以服务：

```text
学习
面试
汇报
论文 / 报告
公众号 / 分享
```

但语义源只有一套。

---

# 10. Acceptance Checklist

一张 Master Figure 进入“成品化”状态前检查：

```text
[ ] Figure Question 是否唯一？
[ ] Canonical Owner 是否明确？
[ ] Primary Case 是否稳定？
[ ] Primary Spine 是否 5–10 秒可读？
[ ] Solid / dashed arrow 是否语义一致？
[ ] 是否依赖颜色才能理解？
[ ] 节点是否使用 canonical terms？
[ ] 是否重新定义了其他 Master Figure 的关系？
[ ] Critical Boundaries 是否清楚？
[ ] Case Lens 是否真正解释边界？
[ ] SVG / PPT 重画时是否能保持 Mermaid 为 semantic source？
```

最终目标：

> **每张图单独拿出来都能讲清一个问题，14 张放在一起又能拼回同一套 Learning System。**
