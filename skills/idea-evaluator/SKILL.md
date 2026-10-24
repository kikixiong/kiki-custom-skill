---
name: idea-evaluator
description: 评估研究 idea 的致命缺陷、创新性、可行性与投入成本。
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

# Idea Evaluator

Use this skill before implementation or paper drafting.

## When To Use

- The user has a draft idea and wants to know whether it is worth pursuing.
- The user wants a novelty, feasibility, or scope check.
- The user is comparing two or three candidate ideas.
- The user worries the idea is too big for their timeline, compute, or background.

## When Not To Use

- If the user already has a stable paper skeleton, use `tech-paper-template`.
- If the user is blocked on the Introduction, use `intro-drafter`.
- If the user wants a finished-paper audit, use `pre-submission-reviewer`.
- If the paper is clearly a benchmark paper, use `benchmark-paper-template`.

## Procedure

### 1. First Impression

Classify the idea as one of:

- Novel Problem
- Novel Method
- New Setting

Write the one-sentence story. If that sentence is weak or impossible to write, ask the user to restate the idea more clearly before scoring it.

### 2. Fatal-Flaw Audit

Run this before any scoring. Identify at most two serious flaws. Typical fatal flaws:

- The contribution is already dominated by known prior work.
- The task does not matter enough to justify a paper.
- The evaluation target is vague or not falsifiable.
- The required data or compute is unrealistic for the user.
- The user's skill, time, and the idea's lifecycle are badly mismatched.

Severity:

- `CRITICAL`: one flaw is enough to reject this version now.
- `MAJOR`: serious but fixable with scope control.
- `MINOR`: polish or framing issue.

If any flaw is `CRITICAL`, stop after the flaw analysis and give `Reject and Pivot`.

### 3. Lifecycle And Capability Match

Estimate the idea's likely execution style and ask for missing inputs if needed:

- weekly effective hours
- theory vs engineering strength
- compute and data access
- team size
- target timeline

Return `Green`, `Yellow`, or `Red` fit.

### 4. Five-Dimension Scoring

Score each from 1 to 10 with explicit evidence:

- `Higher`: accuracy or effectiveness gain
- `Faster`: efficiency or cost reduction
- `Stronger`: robustness or generalization
- `Cheaper`: lower data, annotation, or deployment cost
- `Broader`: transfer across tasks, domains, or settings

Call out the top two or three dimensions worth emphasizing in the paper.

### 5. Paradigm-Shift Probe

Ask four questions:

1. Does it break a hidden field assumption?
2. Does it tackle an elephant-in-the-room problem others avoid?
3. Does it benefit from a new technology cycle that changes feasibility?
4. If solved, would the field actually change?

Two or more yes answers means the idea has disruptive potential.

### 6. Feasibility Check

Assess:

- compute risk
- data risk
- engineering risk
- timeline risk

Every high risk needs a concrete mitigation.

### 7. Verdict

Use one of:

- `Strong Accept`: start now
- `Accept with Revisions`: narrow or reshape first
- `Reject and Pivot`: do not pursue this version

## Output

Return:

1. First impression and one-sentence story
2. Fatal flaws with severity
3. Lifecycle and capability fit
4. Five-dimension score table
5. Paradigm-shift probe
6. Feasibility risks
7. Verdict
8. Top three actions

## Source

Adapted for Codex from HKUSTDial/Supervisor-Skills, CC-BY-4.0:
https://github.com/HKUSTDial/Supervisor-Skills
