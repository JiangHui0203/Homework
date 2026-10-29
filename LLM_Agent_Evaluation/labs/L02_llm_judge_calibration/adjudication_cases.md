# L02 — Manual Adjudication Cases

> 先独立完成，再看 `SOLUTION.md`。这些 case 用来训练：Human disagreement 不是一个数字，而是需要回到 evidence 与 rubric。

## Rubric for these cases

按以下优先级：

```text
1. Hard factual / executable correctness
2. Explicit instruction compliance
3. Material omission / unsupported claim
4. Clarity and usefulness
5. Style / polish
```

如果 1–3 层出现 critical failure，不能被 4–5 层“平均回来”。

## C01 — Polished but wrong number

**Task**：根据给定表格回答“Q3 总收入是多少？”，参考数据明确为 `2.80M`。

**Response A**：Q3 revenue reached **3.10M**, reflecting strong quarter-over-quarter momentum. The result suggests...

**Response B**：Q3 total revenue is **2.80M**.

```text
Human-1: A
Human-2: B
Judge-X: A
```

请 adjudicate：`A / B / TIE / UNRESOLVED`。

## C02 — Explicit output constraint

**Task**：只允许 **3 个 bullet**，每个 bullet 一句话。

**Response A**

- Cause one.
- Cause two.
- Cause three.

**Response B**

- Cause one with additional explanation.
- Cause two with additional explanation.
- Cause three with additional explanation.
- Additional consideration.
- Caveat.
- Recommendation.

```text
Human-1: A
Human-2: B
Judge-X: B
```

请 adjudicate。

## C03 — Genuine subjective tie

**Task**：把一句普通通知改得“更自然友好”，没有长度限制，也没有事实性 reference。

**Response A**：Thanks for the update. I’ll take a look and get back to you soon.

**Response B**：Thanks so much for the update! I’ll review it shortly and follow up once I’ve had a chance to look through everything.

```text
Human-1: A
Human-2: B
Judge-X: B
```

请 adjudicate。

## C04 — Longer answer contains unsupported API

**Task**：解释如何读取一个已经提供的本地 JSON 文件。环境只保证 Python 标准库。

**Response A**：Use `json.load()` with a file opened in text mode.

**Response B**：Use `json.load()` and then call `json.validate_schema()` to validate the object before reading fields. This is safer and more production-ready...

已知 Python 标准库 `json` **不存在** `validate_schema()`。

```text
Human-1: A
Human-2: TIE
Judge-X: B
```

请 adjudicate。

## C05 — Correct abstention vs confident fabrication

**Task**：问“2027 年该产品销量是多少？”，但输入材料只包含到 2026 年的数据，没有预测模型或未来数据。

**Response A**：现有证据不足以给出 2027 年销量；需要预测假设或额外数据。

**Response B**：2027 年销量预计为 1.42M，同比增长约 8%。

```text
Human-1: A
Human-2: B
Judge-X: B
```

请 adjudicate。

## What to record

每个 case 填：

```text
Final label:
Decisive evidence:
Why Human-1 may disagree:
Why Human-2 may disagree:
Why Judge may disagree:
Needs rubric change? yes/no
Needs judge change? yes/no
```

最后回答：哪些 disagreement 说明 Judge 有问题，哪些 disagreement 说明 rubric / task 本身存在主观性？
