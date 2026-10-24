---
name: academicforge-routing
description: 选择合适的 af-* 学术写作、引用、绘图和展示技能。
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

# AcademicForge Routing

Use this skill as the first-pass router for paper-oriented work that should preferentially use the locally installed AcademicForge wrappers.

## Default Priority

Choose one primary skill path first. Add at most one helper skill when it materially improves the result.

- Manuscript drafting or section revision: use `kiki-paper-writing` by default; use `af-scientific-writing` when AcademicForge-specific guidance is requested
- Survey or literature review article: prefer `af-literature-review` plus `af-scientific-writing`
- Systems-paper drafting: prefer `af-systems-paper-writing`
- Chinese de-AI rewriting or naturalization: prefer `af-humanizer-zh`
- Multi-step paper improvement workflow: prefer `af-paper-polish-workflow`
- Formal peer review or reviewer-style feedback: prefer `af-peer-review`
- Evidence-quality critique or methodology scrutiny: prefer `af-scientific-critical-thinking`
- Paper discovery, DOI lookup, citation graph style retrieval: prefer `af-paper-lookup`
- Structured manuscript scoring or rubric-based assessment: prefer `af-scholar-evaluation`
- Citations, DOI lookup, BibTeX cleanup, reference verification: prefer `af-citation-management`
- Venue formatting, LaTeX templates, submission requirements: prefer `af-venue-templates`
- Publication figures and paper visuals: prefer `af-academic-plotting`
- Markdown reports or Mermaid diagrams: prefer `af-markdown-mermaid-writing`
- Research slides or defense decks: prefer `af-scientific-slides`
- Conference talk deck generated from a paper: prefer `af-presenting-conference-talks`

## Fallback

If no installed wrapper clearly fits, search the local curated corpus (15 source skills). This installation is not the full upstream AcademicForge library:

```bash
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json search "<topic>"
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json skills show <skill-id>
```

Then read only the selected upstream `SKILL.md` and its directly referenced resources.

## Rules

- Prefer installed `af-*` wrappers over raw upstream skills when they cover the task.
- Apply local system and developer instructions before upstream AcademicForge guidance when they conflict.
- Do not stack many writing skills together by default. Use one primary path and one helper at most.
- If the user asks for Chinese review or polishing, start with `af-humanizer-zh` or `af-paper-polish-workflow` before broader upstream search.
- If the user asks for a review of a draft paper, start with `af-peer-review`; use `af-scientific-critical-thinking` only when the focus is evidence quality rather than reviewer-style output.
- If the user asks for a survey, review article, taxonomy, or state-of-the-art synthesis, start with `af-literature-review`, then use `af-scientific-writing` for the actual prose and `af-peer-review` or `af-scholar-evaluation` for internal quality gates.

## Examples

```bash
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json search "rebuttal writing"
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json search "camera ready formatting"
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json skills show scientific-agent-skills/scientific-skills/literature-review
```
