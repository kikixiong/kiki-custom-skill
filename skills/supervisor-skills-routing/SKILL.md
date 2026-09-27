---
name: supervisor-skills-routing
description: 把宽泛的论文求助分派到 idea、提纲、Introduction、图形或审查技能。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Supervisor Skills Routing

Use this skill as the entry point when the user clearly wants research-paper help, but their current stage is broad or mixed.

## Routing Rules

- If the user is deciding whether an idea is worth doing, route to `idea-evaluator`.
- If the user needs a technical paper's story, logic chain, or methodology skeleton, route to `tech-paper-template`.
- If the user is blocked on the Introduction, route to `intro-drafter`.
- If the paper is a benchmark or evaluation paper, route to `benchmark-paper-template`.
- If the user needs figure planning, chart choice, or figure audit, route to `figure-designer`.
- If the user wants pre-submission review, proofreading, or a last-pass audit, route to `pre-submission-reviewer`.
- If the user is asking how to use Codex or other AI tools during a research workflow, route to `vibe-research-workflow`.

## Fast Classifier

Classify the request by the smallest artifact that will unblock the user:

- `idea`: scope, novelty, feasibility, worth doing
- `skeleton`: whole-paper logic before prose
- `intro`: Introduction story or six-paragraph flow
- `benchmark`: benchmark or evaluation paper design
- `figure`: Figure 1, method overview, experiment plot, chart type
- `review`: submission audit, proofread, checklist
- `workflow`: AI-assisted coding, writing, figure, tool choice

If the stage is still ambiguous, ask one short question about the current artifact or bottleneck, then route.

## Source

Adapted for Codex from HKUSTDial/Supervisor-Skills, CC-BY-4.0:
https://github.com/HKUSTDial/Supervisor-Skills
