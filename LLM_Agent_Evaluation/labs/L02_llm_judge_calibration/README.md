# L02 — LLM Judge Calibration Lab

> 目标：把 Q08–Q11 从“看懂”推进到“会做”。完成本 Lab 后，你应该能独立判断一个 LLM Judge 是否足以承担某个实际 Evaluation 决策。

## Learning objective

你将完成一次小型但完整的 Judge 上线前 calibration：

1. 定义 Judge 要承担的 claim 与允许范围；
2. 计算 Judge ↔ Human agreement，而不是只看一个相关系数；
3. 检查 repeated judging 的稳定性；
4. 做 pairwise swap test，诊断 position sensitivity；
5. 按 task / length / style / family-match 做 bias slicing；
6. 对 Human/Judge disagreement 做人工 adjudication；
7. 基于预注册 gate 给出 `GO / CONDITIONAL GO / NO-GO` 结论；
8. 明确“这个结论能证明什么、不能证明什么”。

## Prerequisites

先读：

- [Q07 Grader / Verifier / Judge](../../02_Grader_and_LLM_as_a_Judge/01_Grader_Verifier_and_Judge.md)
- [Q08 Judge Reliability & Calibration](../../02_Grader_and_LLM_as_a_Judge/02_Judge_Reliability_and_Calibration.md)
- [Q09 Judge Bias & Failure Modes](../../02_Grader_and_LLM_as_a_Judge/03_Judge_Bias_and_Failure_Modes.md)
- [Q10 Rubric & Scoring Protocol](../../02_Grader_and_LLM_as_a_Judge/04_Rubric_and_Scoring_Protocol.md)
- [Q11 Human Disagreement & Adjudication](../../02_Grader_and_LLM_as_a_Judge/05_Human_Disagreement_and_Adjudication.md)

## Scenario

你正在评估一个候选 `Judge-X`。团队希望它同时承担：

- pointwise 1–5 评分；
- A/B pairwise preference；
- 大规模离线回归；
- 潜在的自动 release gate。

当前有一批冻结 calibration 数据：

```text
Human ratings
Judge repeated ratings
Pairwise original order
Pairwise swapped order
Task / length / style slices
A small set of disagreement cases
```

你的任务不是“证明 Judge-X 好不好”，而是回答更严格的问题：

> **在当前 evaluation contract 下，Judge-X 是否足以承担预期决策？如果不能，它还能在哪些受限场景使用？**

本 Lab 的数据是**合成教学数据**，不是任何真实模型的性能结论。数据被刻意设计成“总体某些指标看起来不错，但关键可靠性测试失败”，用于训练诊断能力。

## Files

```text
L02_llm_judge_calibration/
├── README.md
├── pointwise_scores.csv
├── pairwise_trials.csv
├── adjudication_cases.md
├── analyze.py
├── REPORT_TEMPLATE.md
└── SOLUTION.md
```

### `pointwise_scores.csv`

每行一个待评样本：

- `human_r1`, `human_r2`：两位人工评分；
- `human_gold`：已完成 adjudication 后的 reference score；
- `judge_r1`, `judge_r2`：Judge-X 两次独立评分；
- `slice`, `length_bucket`, `style`：诊断切片。

### `pairwise_trials.csv`

每行一个 A/B 比较：

- `human_r1`, `human_r2`：两位人工偏好；
- `human_gold`：adjudicated reference；
- `judge_ab_r1`, `judge_ab_r2`：A 在左、B 在右时两次 Judge 结果；
- `judge_ba_raw`：交换位置后，Judge 输出的是 `FIRST / SECOND / TIE`；
- `length_relation`, `style_relation`, `judge_family_match`：bias probe。

注意：

```text
交换后展示顺序是 B, A

FIRST  -> canonical B
SECOND -> canonical A
TIE    -> canonical TIE
```

如果这一层映射写错，整个 swap analysis 都会错。

## Pre-registered release gates

在看结果之前，先固定 gate：

| Gate | Threshold |
|---|---:|
| Pointwise within ±1 agreement | ≥ 90% |
| Critical disagreement `|Judge-Human| >= 2` | ≤ 2% |
| Pairwise Judge↔Human accuracy | ≥ 80% |
| Judge repeat consistency | ≥ 95% |
| Swap consistency | ≥ 95% |
| Style slice pairwise accuracy | ≥ 70% |
| Verbose-preference gap | ≤ 15 percentage points |

这些 threshold 只是本 Lab 的教学 release contract，不是通用行业标准。

## Task

### A. 先写 evaluation claim

在运行脚本前，先在 `REPORT_TEMPLATE.md` 写一句：

```text
We want to know whether Judge-X can ...
```

并明确：target task、unit of analysis、Judge 输出、reference evidence、planned decision、error cost。

### B. Pointwise agreement

从 1–5 评分计算 exact agreement、within-one agreement、MAE、critical disagreement rate、Human-Human exact agreement。

回答：为什么 `within ±1` 很高也不能直接上线？哪一种 disagreement 对 hard gate 最危险？如果 Human-Human 自己也不完全一致，应该怎样解释 Judge-Human disagreement？

### C. Repeat consistency

比较 `judge_r1` vs `judge_r2`。回答同一输入重复判断是否稳定；不稳定可能来自什么；哪些 slice 更值得复查。

### D. Swap test

对 pairwise 数据：

1. 将 `judge_ba_raw` 转为 canonical A/B/TIE；
2. 计算 swap consistency；
3. 比较 original-order accuracy 与 swapped-order accuracy；
4. 找出发生 verdict flip 的 pair。

核心问题：如果内容完全相同，只交换左右位置，结论为什么会变化？

### E. Bias slicing

至少检查 task family、response length、polished/plain style、B-more-verbose probe、B-more-polished probe、judge-family-match probe。

不要只写“存在 bias”，要写：

```text
Observed signal
→ plausible explanation
→ confounder
→ follow-up experiment
```

尤其注意：`verbosity`、`polish`、`family-match` 在这个小数据里存在相关性，因此不能只凭一个 slice 就宣称因果。

### F. Manual adjudication

打开 [adjudication_cases.md](adjudication_cases.md)。对每个 case 写：

```text
Final label:
Decisive evidence:
Why Human-1 may disagree:
Why Human-2 may disagree:
Why Judge may disagree:
Needs rubric change? yes/no
Needs judge change? yes/no
```

先完成再看 `SOLUTION.md`。

### G. Final deployment decision

最终只能选 `GO / CONDITIONAL GO / NO-GO`，但必须同时写 scope。例如：

```text
NO-GO for autonomous release gating.
CONDITIONAL GO for low-stakes triage with human escalation.
```

你的结论至少回答：哪些 gate 通过/失败；最严重的问题是什么；当前 Judge 可以/不能承担什么；下一轮最小修复实验是什么。

## Run

只需要 Python 标准库：

```bash
cd LLM_Agent_Evaluation/labs/L02_llm_judge_calibration
python analyze.py
```

Windows 也可以：

```powershell
python .\analyze.py
```

脚本只负责读取冻结 CSV、计算指标、输出 slice、对照预注册 gates。**脚本不会替你做最终 deployment decision。**

## Deliverables

完成一个自己的报告，至少包含：Evaluation claim、pointwise results、pairwise results、repeat consistency、swap analysis、bias slices、adjudication notes、GO/CONDITIONAL GO/NO-GO、allowed scope、what this experiment does NOT prove。

可直接复制 [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md)。

## Evaluation rubric

| 能力 | S2 | S3 | S4 迹象 |
|---|---|---|---|
| Agreement | 会解释指标 | 能正确计算并解释 | 知道 agreement 的边界与 confounder |
| Repeat | 知道要测稳定性 | 能定位 flip | 能设计复测/版本 gate |
| Swap | 知道 position bias | 能 canonicalize + 测 | 能设计 controlled counterfactual |
| Slicing | 会看分组 | 能找到弱 slice | 能区分 correlation 与 causal claim |
| Adjudication | 知道 disagreement | 能按 evidence 判定 | 能反推 rubric/evaluator 缺陷 |
| Deployment | 会报分数 | 能给 scope-aware verdict | 能 defend 风险、阈值和下一步实验 |

完成本 Lab 并能独立解释结果，可以作为 Q08–Q11 从 `S2` 向 `S3` 推进的证据；不会自动修改 `CORE_QUESTIONS.md` 中的个人 mastery。

## Common mistakes

- 只报 overall agreement；
- 把 `within ±1` 当成“95.8% 准确率”；
- swap 后忘记把 `FIRST / SECOND` 映射回 canonical A/B；
- 把 human disagreement 全部算 Judge 错；
- 看到 verbose slice 差就直接断言“因 verbosity 导致”；
- 只看 original-order accuracy，不看 swapped-order；
- release gate 看到结果后再改；
- 把一个 synthetic lab 的 threshold 当成通用标准。

## VeriAgent lens

VeriAgent 当前有大量更强的 deterministic evidence，例如 SQL 执行结果、独立 reference、schema / contract verification。因此这个 Lab 的关键迁移不是“给 VeriAgent 加 Judge”，而是：**先判断是否真的需要 Judge。**

如果未来 VeriAgent 需要评价 explanation quality、clarification quality、open-ended helpfulness、rationale usefulness，才应把这里的 calibration workflow 引入，而不是让 LLM Judge 替代已经存在的 deterministic correctness evidence。

## Extension

完成基础 Lab 后，可以继续：给 pairwise preference 加 Bradley–Terry aggregation；为 Judge 增加 confidence/abstain；构造独立 holdout calibration set；对 rubric version 做 Judge regression；将高风险 slice 路由给 Human；比较 single Judge、Judge ensemble、Human+Judge hybrid。
