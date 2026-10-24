---
name: benchmark-paper-template
description: 围绕评估缺口、数据构建、评估框架和实证发现组织 benchmark 论文。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
disable-model-invocation: true
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Benchmark Paper Template

Use this skill for benchmark, dataset, or evaluation papers. Do not treat those like normal technical papers.

## When To Use

- The paper's core contribution is a new benchmark, evaluation dimension, dataset, or diagnostic framework.
- The user is unsure whether the benchmark idea is substantive.
- The user needs benchmark-specific paper structure or experiments.

## When Not To Use

- If the main contribution is a novel method, use `tech-paper-template`.
- If the user only needs an Introduction for a normal technical paper, use `intro-drafter`.

## Core Distinction

Benchmark papers win by defining a meaningful evaluation gap and building a credible measurement pipeline, not by proposing a new algorithm.

## Five Pillars

1. `Research Gap`: what evaluation blind spot do prior benchmarks miss?
2. `Construction Pipeline`: how is the data built with quality, scale, and reproducibility?
3. `Evaluation Framework`: what taxonomy, difficulty tiers, or rubrics diagnose the gap?
4. `Empirical Findings`: what capability boundaries does the benchmark reveal?
5. `Companion Method` optional: is a specialized model useful to show the community can act on the findings?

All five should be checked explicitly.

## Introduction Six-Part Logic Chain

1. Background and running example
2. Existing benchmark limitations, at most three
3. Research questions
4. Design considerations
5. Our proposal
6. Contributions

## Section Skeleton

- `§2` Task and design goals
- `§3` Construction pipeline
- `§4` Companion method if any
- `§5` Experiments organized by research question
- `§6` Discussion and research opportunities
- `§7` Related work with a benchmark comparison table

## Review Heuristics

- Figure 1 is usually a running example plus pipeline intuition.
- Figure 2 is usually the construction pipeline.
- Experiments should answer explicit research questions rather than dump scores.
- Findings should read like clear takeaways, not loose observations.

## Output

Return:

1. Five-pillar completeness table
2. Introduction six-part chain
3. Section outline for `§2` to `§7`
4. Critical or major pre-submission issues
5. Top three next actions

## Source

Adapted for Codex from HKUSTDial/Supervisor-Skills, CC-BY-4.0:
https://github.com/HKUSTDial/Supervisor-Skills
