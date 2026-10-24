---
name: awesome-ai-research-writing
description: 提供翻译、缩写、扩写、润色、图注和论文检查的提示模板入口。
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

# Awesome AI Research Writing

Use this skill as a prompt-library router for fast, practical academic writing tasks. The upstream source is installed at:

`@@KIKI_SUPPORT_DIR@@/vendor/awesome-ai-research-writing/README.md`

## Route By Task

- Chinese to English LaTeX academic prose: use the repo's `中转英` style and keep LaTeX clean.
- English LaTeX to Chinese explanation: use `英转中`, removing citation/label noise when requested.
- Chinese academic rewriting for Word-style manuscripts: use `中转中`.
- Shorten or expand paper text: use `缩写` or `扩写` logic.
- Expression polish and anti-AI style: route to `nature-polishing`, `af-humanizer-zh`, or this skill's prompt style.
- Logic check and reviewer-facing diagnosis: route to `research-paper-writing`, `pre-submission-reviewer`, or `top-ai-paper-submission`.
- Figure/table caption generation: route to `figure-designer`, `figures4papers`, or `nature-figure` when visual quality matters.
- Experiment analysis: route to `analyze-results` and keep claims tied to real result artifacts.

## Output Rules

- Preserve the user's requested format exactly when they name one, such as `Part 1 [LaTeX]` plus `Part 2 [Translation]`.
- For LaTeX output, escape special characters, preserve math, and avoid decorative formatting.
- For polishing, remove mechanical AI transitions and overclaiming.
- For paper-review style prompts, lead with actionable risks and unsupported claims.

## Source Use

Open `references/prompt-map.md` for the local family map. Open the upstream README only for the specific prompt family needed. Do not load the entire prompt collection when a narrower local route is enough.
