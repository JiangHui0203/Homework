# L01 — Reference Solution

> 建议先独立完成 `metric_contract.json` 和 `MY_REPORT.md` 再看本文件。

## 1. Correct protocol interpretation

共有 24 个计划运行：

```text
22 evaluable Agent runs
2 provider-level infrastructure aborts
```

因此：

```text
Experiment Completeness = 22 / 24 = 91.7%
```

根据冻结 protocol：provider abort 不计作 Agent capability failure，但本轮也不能当成完整 release evaluation。

所以第一结论不是某个 accuracy，而是：

> **Official evaluation status = INCOMPLETE / ABORTED.**

后续数字只能称 provisional diagnostics。

## 2. Recommended metric contracts

### M01 Task Success Rate

```text
正确完成的 evaluable Agent runs
--------------------------------
全部 evaluable Agent runs
```

- infrastructure abort 排除；
- Agent wrong answer / rejected output / invalid output / unrecovered failure 保留在分母；
- correct safe stop 与 recovered success 都可算正确完成。

结果：

```text
16 / 22 = 72.7%
```

### M02 Accepted Output Accuracy

```text
被 runtime 接受且正确的 runs
----------------------------
所有被 runtime 接受的 runs
```

结果：

```text
16 / 19 = 84.2%
```

这不是 Task Success Rate，因为它条件化在“已经被系统接受”的结果上，拒绝和失败的运行没有进入分母。

### M03 False Accept Rate

本 Lab canonical 定义：

```text
错误且被 runtime 接受的 evaluable runs
--------------------------------------
所有错误的 evaluable runs
```

结果：

```text
3 / 6 = 50.0%
```

另一个合法但不同的问题是：

```text
错误放行 / 所有 evaluable runs = 3 / 22 = 13.6%
```

这个数字更适合命名为 `False Accept Incidence among All Runs`，不能与 conditional False Accept Rate 混用。

### M04 Safe Stop Success Rate

```text
正确 safe stop
--------------
所有要求 safe stop 的 evaluable tasks
```

结果：

```text
5 / 6 = 83.3%
```

### M05 Recovery Success Rate

```text
发生 recovery opportunity 后最终正确完成
------------------------------------------
所有 recovery opportunities
```

结果：

```text
2 / 3 = 66.7%
```

### M06 Tokens per Valid Success

```text
所有 evaluable runs 的总 token
------------------------------
正确完成数
```

数据：

```text
Total evaluable tokens = 27,610
Valid successes        = 16
Tokens / success       = 1,725.6
```

失败 run 消耗了：

```text
8,150 / 27,610 = 29.5%
```

如果只统计成功 run 的 token，会把近三成真实消耗从系统成本中删除。

### M07 End-to-End P95 Latency

对所有 evaluable runs 的完整端到端 latency 使用 nearest-rank P95：

```text
P50 = 2,300 ms
P95 = 4,100 ms
```

这里测的是完整 task runtime，不是单次 LLM request latency。

### M08 Experiment Completeness

```text
完成并可评估的计划 runs
----------------------
全部计划 runs
```

```text
22 / 24 = 91.7%
```

它是 protocol health metric，不是模型能力 metric。

## 3. Slice results

```text
numeric   8/10 = 80.0%
data_gap  5/6  = 83.3%
tool      3/6  = 50.0%
```

Micro overall：

```text
16/22 = 72.7%
```

Macro family success：

```text
(80.0% + 83.3% + 50.0%) / 3 = 71.1%
```

真正重要的诊断不是 72.7% vs 71.1% 的小差异，而是：

> **tool family 只有 50%，明显低于其它两类。**

只报 overall 会隐藏这个能力缺口。

## 4. Release gates

| Gate | Result | Pass? |
|---|---:|---|
| Experiment completeness = 100% | 91.7% | FAIL |
| Task Success >= 75% | 72.7% | FAIL |
| False Accept = 0% | 50.0% | FAIL |
| Safe Stop >= 90% | 83.3% | FAIL |
| Recovery >= 70% | 66.7% | FAIL |
| Tokens / valid success <= 1800 | 1725.6 | PASS |
| P95 latency <= 4500 ms | 4100 ms | PASS |

## 5. Correct conclusion

正式结论应分两层。

### Protocol conclusion

```text
NO OFFICIAL RELEASE DECISION
```

原因：2/24 计划任务被 provider outage 中断，本轮未达到 100% completeness。应先按冻结规则补跑对应任务。

### Provisional system conclusion

即使暂时只看 22 个 evaluable runs：

```text
NO-GO
```

原因不是单一 accuracy，而是多个关键 gate 同时失败：

- overall success 不足；
- false accept 极高；
- safe stop 不足；
- recovery 不足；
- tool slice 只有 50%。

成本和 P95 latency 通过，不能抵消 correctness / reliability hard gate。

## 6. Five denominator traps

### Trap 1 — 16/19 看起来比 16/22 好

因为 19 只包含 runtime accepted outputs。失败和拒绝已经被条件化掉，因此回答的是“接受结果有多准”，不是“系统有多可靠地完成任务”。

### Trap 2 — 3/6 vs 3/22

二者分子相同，但问题不同：

```text
3/6  -> P(accepted | wrong)
3/22 -> P(wrong and accepted)
```

前者衡量错误发生后 guard 是否会放行；后者衡量所有任务中错误放行事件的总体发生率。

### Trap 3 — infrastructure abort 从 capability denominator 排除

因为它不是 Agent 行为。

但不能从实验记录中消失，因为它决定这轮是否完整。

### Trap 4 — 失败 token 必须留在成本分子

否则失败更频繁、但失败得更早的系统可能被误判为“更便宜”。

### Trap 5 — overall 掩盖 tool slice

overall 72.7% 不能告诉你 tool family 只有 50%。如果线上 workload 对 tool 依赖更高，真实风险会远高于 aggregate 所显示的水平。

## 7. Example 90-second answer

我会先把 metric 当成 contract，而不是一个公式。首先确定 unit 是 task run，并把 infrastructure abort 和 Agent failure 分开：前者不进入 capability denominator，但会让实验 completeness 失败，阻止正式 release score。然后分别定义 task success、accepted-output accuracy、false accept、safe stop、recovery、cost 和 latency，因为它们回答不同问题。这里最典型的 denominator trap 是 16/19 与 16/22：前者只看被 runtime 接受的输出，所以是 accepted-output accuracy，不是 task success。False accept 也必须明确是 3/6 的 conditional rate，还是 3/22 的 overall incidence。成本则用所有 evaluable run 的 token 除以有效成功数，失败消耗不能删除。最后我会同时看 overall 和 family slice；这个例子里 tool success 只有 50%。因此这轮先因为 91.7% completeness 不能形成正式 release 结论；即使看 provisional 结果，也因为 success、false accept、safe stop 和 recovery 多个 hard gate 失败而 NO-GO。
