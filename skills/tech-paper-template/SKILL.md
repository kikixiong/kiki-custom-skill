---
name: tech-paper-template
description: 梳理方法论文的背景、局限、核心想法、挑战、模块和贡献链条。
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

# Tech Paper Template

Use this skill for technical or position papers before writing prose.

## When To Use

- The user wants a whole-paper logic skeleton.
- The paper story feels incoherent.
- The user is preparing for an advisor meeting.
- `idea-evaluator` passed, and the next step is structuring the paper.

## When Not To Use

- If the paper is a benchmark or evaluation paper, use `benchmark-paper-template`.
- If the user needs paragraph-level Introduction help, use `intro-drafter`.
- If the user wants a review of an existing draft, use `pre-submission-reviewer`.

## Procedure

### 1. Position The Paper Type

Decide whether the paper is:

- `Technique Paper`: the main contribution is a method or mechanism.
- `New Problem/Setting Paper`: the main contribution is the goal or problem definition itself.

If the paper is actually a benchmark paper, stop and route to `benchmark-paper-template`.

### 2. Fill The Thinking Template

Complete these cells:

1. Research background
2. Limitation 1
3. Limitation 2
4. Limitation 3 if needed
5. Key idea or goal in one sentence
6. Challenge 1
7. Challenge 2
8. Challenge 3 if needed
9. Methodology topic sentence
10. Module A for Challenge 1
11. Module B for Challenge 2
12. Module C for Challenge 3 if needed
13. Contribution 1 with section mapping
14. Contribution 2 with section mapping
15. Contribution 3 with section mapping

If the user has not provided enough information for a cell, mark it as a gap with severity.

### 3. Run Four Self-Consistency Checks

Every break here is `CRITICAL`:

1. `Limitations -> Key Idea`: does the key idea actually solve the stated limitations?
2. `Key Idea -> Challenges`: do the challenges naturally arise from implementing that idea?
3. `Challenges -> Methodology`: does each module answer a real challenge?
4. `Methodology -> Contributions`: do the claimed contributions match the modules and evidence?

### 4. Generate The Methodology Outline

Derive:

- the section topic sentence
- subsection names
- one-sentence purpose per module

## Output

Return:

1. Paper type and rationale
2. Filled thinking template
3. Four self-consistency checks
4. Severity summary
5. Top three fixes first
6. Next suggested skill

Usually:

- if the skeleton is solid, recommend `intro-drafter`
- if not, fix chain breaks first

## Source

Adapted for Codex from HKUSTDial/Supervisor-Skills, CC-BY-4.0:
https://github.com/HKUSTDial/Supervisor-Skills
