---
name: top-ai-paper-submission
description: 按当前阶段选择查新、实验、写作、审查和投稿相关技能。
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

# Top AI Paper Submission

Treat this as the default high-level workflow for serious AI-paper writing and submission work. The user may speak casually; do not require exact skill names. Phrases like "帮我看看这篇 paper", "继续推进 submission", "这质量够吗", "不像终稿", or "审稿人会怎么喷" should trigger this workflow when the surrounding context is an AI/ML/NLP/CV/research paper. Infer the stage from local files, user wording, and available evidence, then route to the smallest set of existing paper skills that can move the paper forward.

## Default Behavior

Start by identifying the active artifact:
- If a directory, `.tex`, PDF, review file, result table, W&B/log path, or OpenReview/CMT form is mentioned, inspect it directly.
- If the user gives only a broad request, search the current project for likely paper roots: `main.tex`, `paper/`, `submission/`, `reviews`, `rebuttal`, `results`, `figures`, `references.bib`.
- Keep outputs directly usable: edited source, compiled PDF, submission checklist, OpenReview/CMT field text, reviewer-risk map, rebuttal comments, or experiment/action tables in the project folder.

## Route By Stage

Use these installed skills as sub-workflows. Invoke only the relevant subset; do not run the full chain when a narrower stage is obvious.

| User intent / stage | Primary route |
| --- | --- |
| Idea novelty, "有没有人做过", related work gap | `novelty-check`, `research-lit`, `semantic-scholar`, `arxiv` |
| Experiment design, ablations, reviewer-facing validation | `experiment-plan`, `ablation-planner` |
| Results are available, claims are unclear | `result-to-claim`, `analyze-results`, then `paper-claim-audit` when drafting claims |
| Full draft generation from notes/report | `kiki-paper-workflow`, with `academicforge-routing` or `af-scientific-writing` for section prose |
| Existing manuscript needs top-venue hardening | `pre-submission-reviewer`, `auto-paper-improvement-loop`, `nature-polishing` when prose polishing is explicitly requested |
| Citation, bibliography, reference weakness | `citation-audit`, `research-lit`, `af-citation-management` |
| Figures/tables are weak | `figure-designer`, `paper-figure`, `nature-figure`, `af-academic-plotting` |
| LaTeX/PDF/submission packaging | `paper-compile`, then venue-specific checklist and upload/source boundary checks |
| OpenReview/CMT form filling | Inspect the live/form text if provided, then produce copy-pastable fields keyed to that form |
| Reviews/rebuttal/author response/meta-review | `rebuttal`, `analyze-results`, `ablation-planner`, with strict existing-evidence boundaries |

## Quality Gates

For a paper to be called `submission-ready`, verify at least:
- The PDF compiles from the active source tree.
- Page limits and venue-specific exclusions are checked from the actual compiled PDF.
- No undefined citations/references remain.
- Main quantitative claims match available result artifacts, or unresolved placeholders are clearly marked.
- Bibliography entries are real and used in contexts they support.
- Reviewer-risk notes exist for major weak points.

If any gate is not run, say exactly what remains unverified. Do not label a paper final or submission-ready when the evidence is missing.

## Writing Posture

- Improve argument structure before surface prose when the paper feels thin.
- Strengthen claim-to-evidence alignment rather than adding generic polish.
- Preserve strict boundaries between real results, placeholders, and debugging-only reference values.
- Prefer concrete artifacts in the project directory over chat-only advice.
- When the user asks "能中吗", answer with reviewer-risk diagnosis and the next work items, not vague encouragement.
