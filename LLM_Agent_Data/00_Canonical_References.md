# LLM / Agent Data Knowledge System：Canonical References

> 状态：`Stable Mother Edition V3.x / Verified External Anchors`
>
> Source Policy：[`00_Reference_Source_Policy.md`](./00_Reference_Source_Policy.md)
>
> 目的：维护一组**少而稳定、真正承担方法论支撑的外部文献锚点**。本文件不是完整 related work，也不是按“论文重要性”排序。
>
> 核心边界：**External Literature 负责支撑公开方法与公开证据；C1–C5、Practical Walkthrough 与内部 Research Example 仍由本书 / 内部 artifact 自己负责。**
>
> Freshness check：`2026-10-20`。本轮只刷新已有 anchor 的 venue / version metadata 与内部研究证据边界，**不新增 Rxx**。

---

# 0. Reference Map

| ID | Anchor | Role | 主要章节 |
|---|---|---|---|
| R01 | Deep RL from Human Preferences | FOUNDATIONAL / PREFERENCE | Ch3 / Ch6 |
| R02 | InstructGPT | RLHF / SFT / PREFERENCE | Ch2 / Ch3 / Ch6 |
| R03 | DPO | PREFERENCE METHOD | Ch3 |
| R04 | Let's Verify Step by Step | PROCESS SUPERVISION | Ch4 / Ch15 |
| R05 | Self-Instruct | SYNTHETIC DATA | Ch7 |
| R06 | Toolformer | TOOL USE / DATA | Ch5 / Ch7 |
| R07 | ReAct | AGENT / TRAJECTORY | Ch5 / Ch11 / Ch12 |
| R08 | MT-Bench / LLM-as-a-Judge | EVALUATION / JUDGE | Ch15 / Ch16 |
| R09 | HELM | BENCHMARK / PROTOCOL | Ch16 |
| R10 | AgentBench | AGENT EVALUATION | Ch10–16 |
| R11 | WebArena | ENVIRONMENT / AGENT EVAL | Ch11 / Ch16 |
| R12 | SWE-bench | EXECUTABLE EVAL | Ch15 / Ch16 / C5 |
| R13 | Datasheets for Datasets | GOVERNANCE / DOCUMENTATION | Ch19 / Ch22 |
| R14 | Benchmark Data Contamination | CONTAMINATION | Ch16 / Ch19 / Ch20 |
| R15 | LiveBench | FRESH / OBJECTIVE EVAL | Ch16 / Ch23 |

---

# R01 — Human Preference Learning

**Christiano P F, Leike J, Brown T B, et al. Deep reinforcement learning from human preferences[C]//Advances in Neural Information Processing Systems. 2017. arXiv:1706.03741.**

- Venue Source: https://papers.nips.cc/paper/7017-deep-reinforcement-learning
- arXiv: https://arxiv.org/abs/1706.03741
- Status: `VERIFIED + VENUE`
- Role: `FOUNDATIONAL / PREFERENCE`

它提供的外部锚点：

```text
pairwise human preference over behavior / trajectory
→ learned reward / objective signal
```

适合支撑：

```text
Preference Data 的历史基础
trajectory preference
human feedback as learned objective signal
```

不能拿它直接证明：

```text
现代 LLM preference pipeline 的所有工程细节
DPO objective
本书 Outcome / Reward / Credit taxonomy
```

---

# R02 — InstructGPT / RLHF Pipeline

**Ouyang L, Wu J, Jiang X, et al. Training language models to follow instructions with human feedback[C]//Advances in Neural Information Processing Systems. 2022. arXiv:2203.02155.**

- Source: https://arxiv.org/abs/2203.02155
- Status: `VERIFIED + VENUE`
- Role: `RLHF / SFT / PREFERENCE`

核心锚点：

```text
human demonstrations
→ supervised fine-tuning
→ human rankings
→ reward modeling / RLHF
```

适合：

```text
Ch2 training-stage map
Ch3 preference / reward
Ch6 human data
```

注意：

> 本书把数据对象、Learning Signal、Evaluator 与 Credit 做了更细的工程拆分；这些 canonical distinctions 仍由本书定义。

---

# R03 — Direct Preference Optimization

**Rafailov R, Sharma A, Mitchell E, et al. Direct Preference Optimization: Your Language Model is Secretly a Reward Model[C]//Advances in Neural Information Processing Systems. 2023. arXiv:2305.18290.**

- Source: https://arxiv.org/abs/2305.18290
- Status: `VERIFIED + VENUE`
- Role: `PREFERENCE METHOD`

核心锚点：

```text
preference pair
→ direct policy optimization objective
```

适合说明：

```text
Preference Data 不必只服务于显式 Reward Model + RL pipeline
```

不要把：

```text
DPO
=
所有 pairwise preference learning
```

二者不是同义词。

---

# R04 — Process Supervision

**Lightman H, Kosaraju V, Burda Y, et al. Let's Verify Step by Step[C]//International Conference on Learning Representations. 2024. arXiv:2305.20050.**

- Venue Source: https://proceedings.iclr.cc/paper_files/paper/2024/hash/aca97732e30bcf1303bc22ac3924fd16-Abstract-Conference.html
- arXiv: https://arxiv.org/abs/2305.20050
- Status: `VERIFIED + VENUE`
- Role: `PROCESS SUPERVISION`

核心锚点：

```text
Outcome Supervision
vs
Process Supervision
```

以及 step-level human feedback / process reward modeling。

适合：

```text
Ch4 Reasoning Data / Process Supervision
Ch15 process evaluator context
```

不能直接证明：

```text
Risk = Recoverability
low confidence = error
本书 C4 selector / same-prefix taxonomy
```

这些属于不同问题。

---

# R05 — Synthetic Instruction Data

**Wang Y, Kordi Y, Mishra S, et al. Self-Instruct: Aligning Language Models with Self-Generated Instructions[C]//Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers). 2023: 13484–13508. arXiv:2212.10560.**

- Venue Source: https://aclanthology.org/2023.acl-long.754/
- arXiv: https://arxiv.org/abs/2212.10560
- Status: `VERIFIED + VENUE`
- Role: `SYNTHETIC DATA`

核心锚点：

```text
seed tasks
→ model-generated instructions / inputs / outputs
→ filtering
→ instruction tuning data
```

适合：

```text
Ch7 synthetic generation
synthetic filtering / similarity control
```

本书进一步扩展到：

```text
trajectory synthesis
environment synthesis
failure-driven synthesis
counterfactual family
```

这些不应反向归因给 Self-Instruct。

---

# R06 — Tool-use Learning

**Schick T, Dwivedi-Yu J, Dessì R, et al. Toolformer: Language Models Can Teach Themselves to Use Tools[C]//Advances in Neural Information Processing Systems. 2023. arXiv:2302.04761.**

- Source: https://arxiv.org/abs/2302.04761
- Status: `VERIFIED + VENUE`
- Role: `TOOL USE / DATA`

核心锚点：

```text
when to call tool
which tool
arguments
how to incorporate result
```

适合：

```text
Ch5 tool-use decision
Ch7 synthetic / self-generated tool-use data
```

不能用来定义：

```text
Tool ≠ Harness ≠ Environment
```

这个 boundary 是本书为了 Agent data / failure ownership 建立的 canonical operating distinction。

---

# R07 — Reasoning + Acting / Trajectory

**Yao S, Zhao J, Yu D, et al. ReAct: Synergizing Reasoning and Acting in Language Models[C]//International Conference on Learning Representations. 2023. arXiv:2210.03629.**

- Source: https://arxiv.org/abs/2210.03629
- Status: `VERIFIED + VENUE`
- Role: `AGENT / TRAJECTORY`

核心锚点：

```text
reasoning trace
↔ action
↔ external observation
```

适合：

```text
Ch5 Agent trajectory intuition
Ch11 environment interaction
Ch12 reasoning/action/observation sequence
```

本书的 typed event log、World State / Agent-visible State、Harness boundary 是进一步的工程化表达。

---

# R08 — LLM-as-a-Judge

**Zheng L, Chiang W L, Sheng Y, et al. Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena[C]//Advances in Neural Information Processing Systems 36, Datasets and Benchmarks Track. 2023. arXiv:2306.05685.**

- Venue Source: https://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html
- arXiv: https://arxiv.org/abs/2306.05685
- Status: `VERIFIED + VENUE`
- Role: `EVALUATION / JUDGE`

重要外部锚点：

```text
LLM-as-a-Judge
position bias
verbosity bias
self-enhancement bias
human agreement analysis
```

适合：

```text
Ch15 Judge bias / meta-evaluation
Ch16 evaluator version discipline
```

固定边界：

```text
Human Agreement
≠ Ground-truth Validity
```

本书进一步强调：

```text
Evidence First, Judge Second
```

---

# R09 — Holistic Evaluation / Standardized Protocol

**Liang P, Bommasani R, Lee T, et al. Holistic Evaluation of Language Models[J]. arXiv preprint arXiv:2211.09110, 2022.**

- Full Technical Report: https://arxiv.org/abs/2211.09110
- Related Formal Concise Report: https://doi.org/10.1111/nyas.15007
- Status: `VERIFIED / VERSION-AWARE`
- Role: `BENCHMARK / PROTOCOL`

版本说明：

```text
2022 full technical report
≠
2023 formal concise report
```

后者由 Bommasani / Liang / Lee 以 concise report 形式正式发表；它可以核对 HELM 的 publication identity 与总体思想，但不是对 full technical report 的机械替换。本 registry 继续使用 full technical report 承担完整 benchmark / protocol anchor。

核心锚点：

```text
scenario coverage
multiple metrics
standardized evaluation conditions
transparency
```

适合：

```text
Ch16 benchmark design
multi-metric / claim-scope thinking
```

本书的：

```text
Benchmark Object
≠ Evaluation Protocol
≠ Evaluation Run
≠ Evaluation Report
```

属于更面向实验治理的 canonical decomposition。

---

# R10 — Agent Evaluation Across Environments

**Liu X, Yu H, Zhang H, et al. AgentBench: Evaluating LLMs as Agents[C]//International Conference on Learning Representations. 2024. arXiv:2308.03688.**

- Venue Source: https://openreview.net/pdf?id=zAdUB0aCTQ
- arXiv: https://arxiv.org/abs/2308.03688
- Status: `VERIFIED + VENUE`
- Role: `AGENT EVALUATION`

核心锚点：

```text
interactive environments
multi-turn agent behavior
agent benchmark across heterogeneous tasks
```

适合：

```text
Ch10–14 Agent task / environment / failure context
Ch16 Agent benchmark context
```

不能把 benchmark 中观测到的失败原因直接升级成本书 universal failure taxonomy。

---

# R11 — Realistic Agent Environment

**Zhou S, Xu F F, Zhu H, et al. WebArena: A Realistic Web Environment for Building Autonomous Agents[C]//International Conference on Learning Representations. 2024. arXiv:2307.13854.**

- Source: https://arxiv.org/abs/2307.13854
- Status: `VERIFIED + VENUE`
- Role: `ENVIRONMENT / AGENT EVALUATION`

核心锚点：

```text
reproducible interactive environment
functional task success
long-horizon web tasks
```

适合：

```text
Ch11 Environment Design
Ch16 task success / interactive benchmark
```

与本书 C1 / C3 类 case 的共同点是：

```text
final world state matters
```

而不是只看 final response text。

---

# R12 — Executable Software Evaluation

**Jimenez C E, Yang J, Wettig A, et al. SWE-bench: Can Language Models Resolve Real-World GitHub Issues?[C]//International Conference on Learning Representations. 2024. arXiv:2310.06770.**

- Venue Source: https://openreview.net/forum?id=VTF8yNQM66
- arXiv: https://arxiv.org/abs/2310.06770
- Status: `VERIFIED + VENUE`
- Role: `EXECUTABLE EVALUATION`

核心锚点：

```text
real repository state
code modification
execution / tests
functional correctness
```

适合：

```text
Ch15 executable evidence
Ch16 environment-frozen evaluation
C5 Executable Truth walkthrough
```

固定边界：

```text
textual plausibility
≠ executable correctness
```

---

# R13 — Dataset Documentation / Governance

**Gebru T, Morgenstern J, Vecchione B, et al. Datasheets for Datasets[J]. Communications of the ACM, 2021, 64(12): 86–92. arXiv:1803.09010.**

- Source: https://arxiv.org/abs/1803.09010
- Status: `VERIFIED + VENUE`
- Role: `GOVERNANCE / DOCUMENTATION`

核心锚点：

```text
dataset motivation
composition
collection process
recommended uses
transparency / accountability
```

适合：

```text
Ch19 Data Governance
Ch22 Production Handoff / documentation
```

本书的 Lineage DAG、Re-score / Re-run / Replay、Decision Freeze 等是更偏实验与运行历史的扩展。

---

# R14 — Benchmark Contamination

**Deng C, Zhao Y, Tang X, Gerstein M, Cohan A. Investigating Data Contamination in Modern Benchmarks for Large Language Models[C]//NAACL 2024. 2024: 8706–8719.**

- Source: https://aclanthology.org/2024.naacl-long.482/
- arXiv: https://arxiv.org/abs/2311.09783
- Status: `VERIFIED + VENUE`
- Role: `CONTAMINATION / EVALUATION`

核心锚点：

```text
benchmark contamination risk
retrieval-based overlap investigation
test-set memorization / guessing signals
```

适合：

```text
Ch16 contamination threat
Ch19 provenance / split lineage
Ch20 dedup / family isolation
```

注意：

```text
No exact duplicate
≠ No contamination
```

---

# R15 — Fresh / Objective Benchmark Design

**White C, Dooley S, Roberts M, et al. LiveBench: A Challenging, Contamination-Free LLM Benchmark[C]//International Conference on Learning Representations. 2025. arXiv:2406.19314.**

- Source: https://arxiv.org/abs/2406.19314
- Project: https://livebench.github.io/
- Status: `VERIFIED + VENUE`
- Role: `FRESH / OBJECTIVE EVALUATION`

核心锚点：

```text
frequently refreshed questions
objective / verifiable ground truth
contamination-aware benchmark maintenance
```

适合：

```text
Ch16 fresh evaluation / contamination-aware design
Ch23 Stable Ruler + Moving Frontier
```

它可以支撑“fresh benchmark / objective scoring 是有价值的设计方向”，但不等于任何动态 benchmark 都天然无污染或天然有效。

---

# 1. Chapter → Reference Quick Map

```text
Ch2
→ R02 / R05

Ch3
→ R01 / R02 / R03

Ch4
→ R04

Ch5
→ R06 / R07

Ch7
→ R05 / R06

Ch10–12
→ R07 / R10 / R11

Ch15
→ R08 / R12

Ch16
→ R08 / R09 / R10 / R11 / R12 / R14 / R15

Ch19
→ R13 / R14

Ch20
→ R05 / R14

Ch23
→ R15
```

---

# 2. Internal Research Is Not in This Registry

以下对象**故意不编号为 Rxx external reference**：

```text
More Thinking fixed-depth results
RoTFuse / K17 results
C1–C5
C1 / C3 / C4 / C5 walkthroughs
A1–A11 Artifact Kit
F1–F14
```

原因：

```text
Internal Research
→ 应指向 internal artifact / formal publication

Teaching / Editorial Asset
→ 由本书自己定义
```

不能把一篇外部“相似论文”挂上去以后，就把内部 claim 伪装成 external evidence。

## More Thinking — current source boundary

公开作者主页现已列出：

```text
NLPCC
More Thinking Is Not Always Better:
Structural and Semantic Factors of Complex Reasoning Tasks in LLMs

Hui Jiang / Shizhu He / Kang Liu / Jun Zhao
```

- Public identity listing: https://heshizhu.github.io/
- Identity status: title / authors / NLPCC venue identity publicly checkable
- Quantitative evidence status: `SOURCE ANCHOR PENDING`

因此：

```text
public publication listing
≠ evidence for 69.04 / 74.09 / 70.97
≠ evidence for fixed-depth protocol details
```

在 formal paper / proceedings 或 internal frozen result summary 可定位以前，固定深度数值仍保持 Internal Research Example 口径。

---

# 3. Maintenance Rule

新增 Rxx 前至少回答：

```text
它提供了什么当前 registry 没有的不可替代 claim anchor？
```

如果答案只是：

```text
“也是做 synthetic data”
“也是 Agent benchmark”
“也是 Judge”
```

则通常放 related reading，而不进入 canonical registry。

Reference metadata 更新时还要额外检查：

```text
formal venue version
≈ current claim-bearing version ?
```

如果不等价，则保留 version relationship，不做 silent replacement。

目标不是拥有最长 bibliography，而是：

> **读者看到一个关键方法论结论时，能迅速找到最接近的一手公开来源；同时始终知道哪些边界是文献结论，哪些是本书为了 LLM / Agent Data 实践建立的 operating model。**
