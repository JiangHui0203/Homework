# Probability & Statistics for Eval — 最小必需基础

> 目标不是学完整概率论，而是能读懂、设计和质疑 Evaluation。

## 1. Random Variable

把一次运行的结果抽象成随机变量。例如：

```text
Y = 1  正确完成
Y = 0  未正确完成
```

LLM/Agent 即使配置相同，也可能因为 sampling、服务端实现或环境交互产生不同结果，因此一次 run 不是“真实能力”的完整观察。

## 2. Bernoulli / Proportion

成功率类 metric 常可先理解为 Bernoulli observation：

```text
p_hat = successes / eligible observations
```

关键不是会背公式，而是知道 `eligible observations` 的定义决定了分母含义。

## 3. Mean, Variance, Distribution

- **Mean**：平均水平。
- **Variance / spread**：结果有多不稳定。
- **Distribution**：不要只看均值；latency、cost 常有长尾。

Agent latency 常报告 P50/P95，而不是只报 mean。

## 4. Population vs Sample

- Population：你想推广到的真实任务总体。
- Sample：实际评的有限任务。

一个 frozen benchmark 的分数首先描述这个 sample；要声称“未来任务也更好”，需要考虑 sample 是否代表目标 population。

## 5. Independence & Nested Data

常见结构：

```text
Task → Repeats → Trajectory → Steps
```

同一 task 的多个 repeat 通常相关；同一 trajectory 的多个 step 更不是独立样本。不要用“记录条数”替代真正样本量。

## 6. Sampling Uncertainty

有限样本得到的是 estimate，不是精确真值。两个系统相差 1–3 个点时，需要问：

- 任务数多少？
- 是否 paired？
- 差异集中在哪几题？
- CI 有多宽？
- repeated runs 是否稳定？

## 7. Confidence Interval

CI 用来表达估计的不确定范围，不是“有 95% 概率真值就在这一次算出的区间里”的简单概率陈述。

在本知识库中先掌握用途：

> **不要只报 point estimate；同时表达样本有限带来的 uncertainty。**

具体计算放 Part 6 后续章节。

## 8. Paired Difference

同一 task 上比较 A/B：

```text
D_i = score_i(B) - score_i(A)
```

paired design 利用了共享 task 难度，通常比完全独立两组更适合模型/Agent版本比较。

## 9. Bootstrap / Permutation 的直觉

- **Bootstrap**：通过重采样近似估计统计量的不确定性。
- **Permutation test**：在“条件标签可交换”的零假设下，观察当前差异有多极端。

先理解它们回答的问题，不急着背实现细节。

## 10. Evaluation 中必须形成的统计反射

看到任何数字先问：

1. `n` 是什么？
2. 分母是什么？
3. 独立单位是什么？
4. 是否 paired？
5. 有多少不同 task，而不是多少 run？
6. uncertainty 多大？
7. 是否看了很多指标/切片后只挑最好的一项？

## 练习

“12 道题每题跑 3 次，candidate 30/36，baseline 29/36。”

不要立刻说 candidate 提升 2.78 个百分点。先回答：

- 36 是 run 还是独立 task？
- 12 个 task 上 paired win/loss 如何？
- 同题重复是否稳定？
- claim 是 run-level reliability 还是 task-level generalization？

## Related

- [Q02 Estimand & Unit of Analysis](../06_Statistics_and_Experiment_Design/01_Estimand_and_Unit_of_Analysis.md)
- [Q04 Metric Design](../01_LLM_Evaluation/03_Metric_Design.md)
