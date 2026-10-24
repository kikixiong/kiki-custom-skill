---
name: rebuttalstudio
description: 衔接 RebuttalStudio 的逐点回复、压缩、润色与多轮讨论流程。
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

# RebuttalStudio Adapter

Use this skill when the user wants RebuttalStudio-style rebuttal organization or names the project directly. The upstream project defines a five-stage rebuttal editor pipeline.

Load `references/pipeline.md` when a compact RebuttalStudio stage reminder is needed.

## Pipeline

1. `Breakdown`: split reviews into atomic weaknesses, questions, factual misunderstandings, and action items.
2. `Reply`: draft outline-first point-by-point responses grounded in evidence.
3. `First Round`: compile venue-ready rebuttal text within format and length constraints.
4. `Multi Rounds`: handle follow-up reviewer discussion and new questions.
5. `Final Remarks`: summarize remaining evidence and close with restrained confidence.

## Route

- Use `rebuttal` for final text-only OpenReview/CMT responses.
- Use `analyze-results` and `ablation-planner` when a reviewer concern needs new experiment evidence.
- Use `citation-audit` or `paper-claim-audit` if a response depends on citations or quantitative claims.
- Use `nature-polishing` only after the response coverage and evidence are correct.

## Operating Rules

- Preserve reviewer IDs and issue coverage.
- Do not merge distinct reviewer concerns until each has a traceable response.
- Separate real evidence, planned experiments, and unavailable evidence.
- Keep tone professional, concise, and non-defensive.
- When the user asks for OpenReview comments, draft copy-pastable comment-thread responses rather than LaTeX.

## Output Artifact

For non-trivial rebuttal work, create or return:

- issue table
- response plan
- final response text
- remaining evidence gaps
