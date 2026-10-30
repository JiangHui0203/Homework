# L06 — Reference Solution

> 这是参考设计，不是唯一合法答案。先独立完成 `benchmark_plan.json` 和 `MY_REPORT.md` 再看。

## 1. Pool audit

冻结 pool：

```text
70 total tasks
```

硬审计得到：

```text
10 direct exposure blockers
  5 DEVELOPMENT_EXPOSED
  5 PUBLIC_CONTAMINATION_RISK

5 KNOWN_CLEAN rows blocked by exposed group
5 reference-not-verified rows
5 non-discriminative rows

45 fully eligible rows
```

这里最容易漏的是每个 capability 的 `*02`：

```text
LOOKUP02
JOIN02
TIME02
STOP02
RECOVER02
```

它们自己的：

```text
exposure_status = KNOWN_CLEAN
```

但和对应 `*01` dev-exposed item 共享同一个 `group_id`，所以不能当 clean holdout。

## 2. 一份满足 contract 的 Representative Set

```text
LOOKUP06
LOOKUP07
LOOKUP09
LOOKUP12
LOOKUP13
LOOKUP14
JOIN06
JOIN07
TIME06
TIME07
STOP06
RECOVER06
```

Capability counts：

```text
simple_lookup   6
join_fanout     2
time_scope      2
safe_stop       1
recovery        1
```

Observed share：

```text
50.0%
16.7%
16.7%
8.3%
8.3%
```

Target population：

```text
50%
20%
15%
10%
5%
```

Total variation distance：

```text
0.050
```

冻结 gate：

```text
<= 0.060
```

因此 PASS。

### Population-weighted task weights

不是简单让 12 个 task 每题都永久权重 `1/12`。

按 capability population weight 重加权：

```text
simple_lookup   0.50 / 6 = 0.08333 per selected task
join_fanout     0.20 / 2 = 0.10000
time_scope      0.15 / 2 = 0.07500
safe_stop       0.10 / 1 = 0.10000
recovery        0.05 / 1 = 0.05000
```

总权重为 1。

## 3. 一份满足 contract 的 Diagnostic Set

```text
LOOKUP08
LOOKUP10
LOOKUP11

JOIN08
JOIN10
JOIN11

TIME08
TIME10
TIME11

STOP08
STOP10
STOP11

RECOVER08
RECOVER10
RECOVER11
```

每个 capability 恰好 3 题：

```text
medium
hard
adversarial
```

全集 risk：

```text
12 / 15 are high or critical
```

因此满足：

```text
balanced capability coverage
+
difficulty coverage
+
risk floor
```

它适合 diagnosis，但不能解释成生产频率。

## 4. Canonical analyzer output

关键结果应为：

```text
pool size                         70
fully eligible                    45

representative n                  12
representative TV distance        0.050
representative quota              PASS
weight sum                        1.000

diagnostic n                      15
equal capability quota            PASS
high/critical risk                12/15
difficulty coverage               PASS

cross-set group overlap           none
cross-set template overlap        none
hard blockers                     0

benchmark design checks           PASS
```

## 5. 为什么 LOOKUP02 不能选

它自身是：

```text
KNOWN_CLEAN
```

但：

```text
LOOKUP01
LOOKUP02
```

共享：

```text
group_id = lookup_g01
```

而 `LOOKUP01` 已经是：

```text
DEVELOPMENT_EXPOSED
```

这说明“clean”不能只在 row level 判断。

## 6. 为什么 group overlap 是 blocker，而 template overlap 只是 warning

本 Lab 的 group 定义已经明确表示：

```text
near-duplicate source / solution family / source entity
```

因此跨 holdout 的 group overlap 直接破坏独立性。

Template 则更宽：

```text
same general structure
```

不同 source / entity / constraints 下，template 共性可能合理存在。因此这里要求：

```text
report + audit
```

而不是自动删除。

实际项目可以根据任务生成过程把 template overlap 升级成 blocker，但必须在 split contract 里提前写清。

## 7. Hard 不等于 Discriminative

例如 pool 中每个 capability 的 `*05`：

```text
difficulty = hard
discriminative_check = 0
```

它就是一个专门的反例：

> 看起来难，并不代表能可靠地区分正确行为与 plausible-wrong behavior。

Benchmark item 的第一优先级仍然是：

```text
valid task contract
+
reliable reference
+
observable behavioral distinction
```

## 8. Historical pass rate 的边界

可以用来检查：

```text
ceiling
floor
difficulty spread
instrument health
```

不能用来做：

```text
看 candidate 在哪些题输
→ 专门把这些题塞进最终 test
```

否则 test 会通过开发反馈参与 model selection。

## 9. 两个 Overall 的语义

### Representative population-weighted

回答：

> 在冻结 synthetic target population 权重下，系统平均表现怎样？

### Diagnostic macro-equal-capability

回答：

> 五个 capability 等权时，系统有没有明显能力短板？

如果两个分数趋势相反，不代表某个分数错了。

它们估计的是：

```text
different estimands
```

## 10. Exposure 后的生命周期

如果 clean test 被用于：

```text
prompt tuning
rule design
memory construction
failure-driven controller changes
```

就应该更新 exposure ledger。

典型角色变化：

```text
Fresh Holdout
→ DEVELOPMENT_EXPOSED
→ reviewed failure
→ Regression / Known-hard asset
```

旧 test 仍有价值，但价值从：

```text
fresh generalization evidence
```

转为：

```text
known-risk regression evidence
```

## 11. Reference benchmark plan

```json
{
  "claim": "Estimate average task reliability under the frozen target mix while preserving a separate balanced diagnostic view for capability weaknesses.",
  "target_population": "Synthetic structured-agent task population defined by benchmark_contract.json.",
  "unit_of_evaluation": "task",
  "representative": {
    "task_ids": [
      "LOOKUP06", "LOOKUP07", "LOOKUP09", "LOOKUP12", "LOOKUP13", "LOOKUP14",
      "JOIN06", "JOIN07",
      "TIME06", "TIME07",
      "STOP06",
      "RECOVER06"
    ],
    "aggregation": "population_weighted",
    "interpretation": "Primary representative view; use frozen population weights, not raw diagnostic macro."
  },
  "diagnostic": {
    "task_ids": [
      "LOOKUP08", "LOOKUP10", "LOOKUP11",
      "JOIN08", "JOIN10", "JOIN11",
      "TIME08", "TIME10", "TIME11",
      "STOP08", "STOP10", "STOP11",
      "RECOVER08", "RECOVER10", "RECOVER11"
    ],
    "aggregation": "macro_equal_capability",
    "interpretation": "Balanced capability diagnosis; not a production-frequency estimate."
  }
}
```

## 12. 90-second interview skeleton

一个比较完整的回答顺序：

```text
1. 先定义 benchmark claim 和 target population。
2. 从 claim 建 capability / risk coverage matrix。
3. 验证 reference 与 plausible-wrong distinction。
4. split 不按 row 随机切，要按 source / group / template 做 leakage audit。
5. representative view 尽量保留自然频率或重加权回总体。
6. diagnostic view 对 rare / high-risk capability 保证最低样本量。
7. frozen core / regression / hard / fresh 分工，不让一套 test 承担所有角色。
8. test 一旦参与开发，就更新 exposure status；新的 generalization claim 用 fresh holdout。
9. 最后同时报告 population-weighted 和 diagnostic slice view，并写 interpretation boundary。
```

最核心的一句话：

> Benchmark 的“公平”不是每类一样多，而是让 sampling、weighting 和你真正想估计的对象保持一致。
