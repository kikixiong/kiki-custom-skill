---
name: pre-submission-reviewer
description: 按严重程度列出论文逻辑、语言、LaTeX、图表和表达问题。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Pre-Submission Reviewer

Use this skill three to five days before submission, or after a major rewrite.

## Review Style

The output should be finding-first and severity-first. Do not default to a full rewrite.

Severity:

- `CRITICAL`: blocks submission
- `MAJOR`: likely reviewer complaint
- `MINOR`: polish

## When To Use

- The user wants a last-pass audit of a paper or major section.
- The user suspects logic gaps, weak English, or AI-tone contamination.
- The user wants proofreading plus structure checks.

## When Not To Use

- If the paper is still being designed, use `tech-paper-template`, `intro-drafter`, or `benchmark-paper-template`.

## Review Dimensions

### 1. Macro Logic

Check:

- Introduction flow is intact
- contributions map to sections and method modules
- experiments validate the main claims
- related work covers key prior art
- the running example stays consistent

Chain breaks are usually `CRITICAL`.

### 2. Writing Details

Check:

- every paragraph has a topic sentence
- transitions are smooth
- paragraphs are not bloated
- abstract covers problem, method, result
- repeated content is removed

### 3. English Grammar

Check common high-impact errors:

- articles
- subject-verb agreement
- tense consistency
- overlong sentences
- weak or Chinglish phrasing
- misuse of `which` and `that`

### 4. LaTeX Format

Check:

- equations are numbered and referenced correctly
- figures and tables have captions
- citations are formatted correctly
- labels are stable and readable
- vector figures are used
- page limits are respected

### 5. Figure Quality

Check each figure for:

- readability
- font size
- color safety
- self-contained caption
- honest axis ranges
- no chartjunk

### 6. AI-Tone And Em-Dash Scan

Flag hype or generic AI phrasing and sentence-connector em dashes. Examples of suspicious wording:

- innovative
- pioneering
- transformative
- superior
- remarkable
- unprecedented
- breakthrough
- general-purpose
- notably
- pave the way for

Escalate if these patterns appear repeatedly.

## Output

Return:

1. Summary counts for `CRITICAL`, `MAJOR`, `MINOR`
2. Findings grouped by dimension
3. Top three fixes first
4. Final submission recommendation

## Source

Adapted for Codex from HKUSTDial/Supervisor-Skills, CC-BY-4.0:
https://github.com/HKUSTDial/Supervisor-Skills
