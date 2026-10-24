---
name: vibe-research-workflow
description: 规划 AI 在科研编程、绘图与写作各阶段的协作方式。
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

# Vibe Research Workflow

Use this as a meta-skill for AI-assisted research sessions.

## Non-Negotiable Rules

State these clearly:

1. AI may help with search organization, code implementation support, debugging, figure drafting, and language polish.
2. Research ideas, novelty claims, technical design, experiment design, and conclusions remain the user's responsibility.
3. The user must verify every AI-assisted statement against real code, results, and facts.
4. No fabricated citations, data, experiments, or claims.
5. No hidden academic misconduct or plagiarism laundering.
6. Venue or school AI-disclosure rules must be followed.

## Phase Classification

Classify the session as:

- `coding`
- `figure`
- `writing`
- `mixed`

## Phase Guidance

### Coding

- plan in small steps
- make requirements explicit
- use Codex for repo-local implementation, debugging, and iteration in this environment
- verify every experiment and metric with actual runs

### Figure

- decide the story first
- sketch fast
- polish in the right tool
- export vector
- audit before submission

### Writing

- structure before prose
- prose before polish
- polish before proofreading
- never invent citations or results

## Tool Selection

Prefer tools by task:

- coding: `Codex` first in this environment; Cursor or Claude Code only if the user explicitly wants them
- figures: PowerPoint or Figma for schematics, Matplotlib or Seaborn for result plots
- writing: Codex or chat assistants for outline and polish, but factual content must come from the user's real work

## Output

Return:

1. Primary and secondary phases
2. A time-block workflow plan
3. Tool recommendations
4. Verification checkpoints
5. Red-line reminders

If the user asks AI to write the whole paper or decide the scientific claims for them, refuse that part and redirect to a narrower, valid workflow.

## Source

Adapted for Codex from HKUSTDial/Supervisor-Skills, CC-BY-4.0:
https://github.com/HKUSTDial/Supervisor-Skills
