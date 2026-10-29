# Homework · AI / Agent Knowledge & Interview Practice

A long-term personal knowledge base for **LLM / Agent / Data systems** and **algorithm interview preparation**.

This repository is not a course-assignment archive. It is a maintained workspace for turning scattered reading, experiments, interview topics, and implementation patterns into reusable knowledge structures.

## What is here

### 1. Agent Knowledge System

[**Agent_Knowledge_System.md**](./Agent_Knowledge_System.md)

A structured knowledge system for understanding how practical LLM agents are built and controlled, including model–harness boundaries, tool use, context and memory, agent loops, verification, recovery, observability, and runtime policy.

The goal is not to collect isolated definitions, but to answer questions such as:

- Who drives an agent run?
- When should the model be called again?
- How does the action–observation loop progress?
- When should a runtime continue, wait, branch, verify, recover, or stop?
- How do we distinguish model capability from harness capability and tool policy?

### 2. LLM / Agent / Data Knowledge System

[**LLM_Agent_Data/**](./LLM_Agent_Data/)

A broader systems-oriented knowledge base connecting **LLM behavior, agent runtime design, data, evaluation, monitoring, failure analysis, and practical case studies**.

Useful entry points include:

- [Condensed Guide](./LLM_Agent_Data/00_Condensed_Guide.md)
- [Concept Index](./LLM_Agent_Data/00_Concept_Index.md)
- [Interview Index](./LLM_Agent_Data/00_Interview_Index.md)
- [Glossary & Notation](./LLM_Agent_Data/00_Glossary_and_Notation.md)
- [Canonical Casebook](./LLM_Agent_Data/00_Canonical_Casebook.md)
- [Canonical References](./LLM_Agent_Data/00_Canonical_References.md)

The system is maintained as a stable reference rather than an ever-growing collection of notes.

### 3. LLM / Agent Evaluation Knowledge System

[**LLM_Agent_Evaluation/**](./LLM_Agent_Evaluation/)

A long-term Evaluation knowledge system for learning, interview preparation, practical evaluation work, and VeriAgent experiments. It focuses on **how to define, measure, compare, diagnose, and maintain trustworthy LLM / Agent evaluations** rather than duplicating the existing data knowledge system.

Core entry points include:

- [Core Questions](./LLM_Agent_Evaluation/CORE_QUESTIONS.md) — evaluation mother questions and mastery tracking;
- [Evaluation Patterns](./LLM_Agent_Evaluation/EVAL_PATTERNS.md) — reusable evaluation design patterns;
- [Metrics](./LLM_Agent_Evaluation/METRICS.md), [Benchmarks](./LLM_Agent_Evaluation/BENCHMARKS.md), and [Failure Taxonomy](./LLM_Agent_Evaluation/FAILURE_TAXONOMY.md) — practical retrieval indexes;
- [Interview Index](./LLM_Agent_Evaluation/INTERVIEW_INDEX.md) — interview-oriented retrieval;
- [VeriAgent Cases](./LLM_Agent_Evaluation/cases/veriagent/) — current implementation cases and frozen experiments;
- [Source of Truth](./LLM_Agent_Evaluation/SOURCE_OF_TRUTH.md) — ownership rules that prevent duplication with `LLM_Agent_Data`.

The system separates stable theory, current VeriAgent implementation cases, and dated/versioned frozen experiments.

### 4. LeetCode Hot 100

[**LeetCode/Hot100/**](./LeetCode/Hot100/)

A pattern-oriented interview preparation system rather than a simple solved-problem list.

It currently includes:

- [49 core questions](./LeetCode/Hot100/CORE_QUESTIONS.md) prioritized as interview mother problems;
- [algorithm templates](./LeetCode/Hot100/TEMPLATES.md) with recognition signals, invariants, code skeletons, and common mistakes;
- topic-organized reference solutions;
- a Hot 100 master list for tracking coverage and review.

The intended workflow is:

```text
Recognize pattern
      ↓
State the invariant
      ↓
Write the template from memory
      ↓
Solve independently
      ↓
Review mistakes and variants
```

## Why I maintain this repository

My current research focuses on **LLM reasoning, evaluation, test-time compute, and selective intervention**. I also work on Agent systems and am preparing for applied LLM / research engineering roles.

Maintaining this repository serves three purposes:

1. turn research and engineering knowledge into explicit mental models;
2. connect model behavior with runtime, data, evaluation, and system design;
3. keep interview preparation systematic and reusable instead of fragmented across temporary notes.

## Related public work

- [**VeriAgent**](https://github.com/JiangHui0203/veriagent) — verifiable Agent runtimes for reasoning and constrained data analysis.
- [**NiceRice**](https://github.com/JiangHui0203/NiceRice) — a local-first WeChat Mini Program for multi-constraint meal planning.
- [**GitHub Profile**](https://github.com/JiangHui0203) — research, industry experience, and selected projects.

---

**Maintained by Hui Jiang · UCAS / CASIA · LLM Evaluation · Agent / Reasoning Systems · Research Engineering**