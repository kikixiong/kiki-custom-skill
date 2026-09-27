---
name: research-start-routing
description: 把科研启动与继续推进请求分派到进度、算法审查和任务执行技能。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Research Start Routing

Use this as the broad router for research-code workflow management adapted to Codex.

## Routes

- Research ideas and method/claim refinement: `brainstorming-research-ideas`, `idea-evaluator`, then `experiment-plan` as needed.

- Project state, progress logs, pipeline, experiments registry: `research-progress-tracker`.
- Algorithm correctness, boundary cases, numerical issues, implementation vs paper: `research-algorithm-checker`.
- Concrete research coding task execution: `research-task-executor` or `research-code-autopilot`.
- GPU/CUDA/training health: `server-gpu-diagnosis`, `training-check`, or `monitor-experiment`.

## Codex Safety Adaptation

The upstream Claude skills suggest automatic commits and exact trigger words. In this Codex setup:

- Trigger broadly from natural language.
- Do not auto-commit or push unless the user explicitly asks.
- When committing is requested, follow the actual project AGENTS.md and user instructions; no upstream-specific Lore protocol is assumed.
- Preserve artifacts such as `PROGRESS.md`, `PIPELINE.md`, `EXPERIMENTS.csv`, and `ISSUES.md` when useful.
- Use the user's lightweight verification policy, respect no-tests requests, and keep all model/data experiments on the authorized remote host.
