---
name: research-progress-tracker
description: 用进度文档和实验登记表维护项目状态及下一步任务。
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

# Research Progress Tracker

Use this to resume or audit an AI research project.

## Startup Flow

1. Inspect project files: `PROGRESS.md`, `PIPELINE.md`, `EXPERIMENTS.csv`, `ISSUES.md`, `AGENTS.md`, scripts, configs, and recent logs.
2. Run lightweight status commands: git status, recent commits, active env, and obvious result/log directories.
3. Identify current stage: setup, data, training, evaluation, ablation, analysis, writing, or blocked.
4. Report:
   - current state
   - latest reliable evidence
   - stale or missing records
   - next executable action
   - verification needed

## Maintained Artifacts

- `PROGRESS.md`: concise reverse-chronological work log.
- `PIPELINE.md`: recommended experiment execution order and dependencies.
- `EXPERIMENTS.csv`: structured experiment registry, including failed experiments.
- `ISSUES.md`: known bugs, risks, discarded ideas, and unresolved checks.

## Codex Rules

- Do not auto-commit or push unless the user explicitly asks.
- Do update local tracking artifacts when the user asks to resume, organize, or continue a project and a project root is clear.
- Keep failed experiments visible; do not overwrite history.
- If model/eval configs are involved, check training-inference consistency before trusting results.
