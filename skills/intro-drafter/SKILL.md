---
name: intro-drafter
description: 把研究动机组织成六段式 Introduction 提纲。
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

# Introduction Drafter

Use this skill when the paper idea is already fairly stable, but the Introduction story is not.

## When To Use

- The user wants a six-paragraph Introduction outline.
- The story between motivation, limitations, challenges, and contributions is broken.
- The user has a partial Introduction and wants to restructure it.

## When Not To Use

- If the idea itself is not stable, use `idea-evaluator`.
- If the user needs the whole paper skeleton first, use `tech-paper-template`.
- If the paper is a benchmark paper, use `benchmark-paper-template`.
- If the user wants final review instead of outlining, use `pre-submission-reviewer`.

## Procedure

### 1. Paper-Type Positioning

Choose:

- `Technique Paper`
- `New Problem/Setting Paper`

This affects how heavy Paragraph 3 should be.

### 2. Draft The Six Paragraphs

For each paragraph, provide:

- purpose
- writing points
- gaps with severity

Paragraphs:

1. Background and motivation, with a running example
2. Limitations of prior work, at most three
3. Problem essence and goal
4. Key challenges, at most three
5. Solution overview with challenge-to-module mapping
6. Contributions, three or four, each mapped to a section

### 3. Running Example Design

If the user does not yet have a running example, propose two or three candidates and choose the one that:

- is real
- is specific
- is simple enough to explain early
- can reappear later in the paper

### 4. Contribution Alignment Check

Verify that every contribution bullet maps to at least one of:

- a challenge
- a methodology module
- a concrete experiment result

Reject vague items such as "comprehensive evaluation" unless they are tied to actual evidence and a section.

### 5. Flowchart Consistency Check

Check the chain:

- running example -> solution overview
- limitations -> challenges
- goal -> contribution 1
- challenges -> modules
- contributions -> sections

Any broken link is `CRITICAL`.

## Output

Return:

1. Type positioning
2. Paragraph 1 to 6 outline
3. Flowchart consistency report
4. Integrity or gap summary
5. Top three actions first

## Source

Adapted for Codex from HKUSTDial/Supervisor-Skills, CC-BY-4.0:
https://github.com/HKUSTDial/Supervisor-Skills
