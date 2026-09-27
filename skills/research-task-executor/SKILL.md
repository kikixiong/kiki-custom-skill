---
name: research-task-executor
description: 执行一个明确的科研代码或实验实现任务，并更新任务记录。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Research Task Executor

## User's experiment environment

Default authorized experiments run through `cnic-ps`; confirm actual hostname
`ps`. For scbenchmark/scGRAIN use `/data1/jiaqi/scREBOUND`, with isolated
`formal_worktrees/<run_id>` and `runs/<run_id>`. Derive other project roots,
environment, datasets and weights from that project's existing configuration.
Before launching an authorized run, inspect GPUs, disk, processes, environment,
data/weight identity, destination and locks; respect current queue priorities.
Keep jobs detached, assigned GPUs exclusive and checkpoints resumable.

The local Mac is for code editing and small report artifacts. Never run training,
forward/inference, probes, profiling or model/data experiments here, even on
CPU/MPS or tiny inputs. A failed remote connection is not permission for a local
fallback. A plan is not authorization to launch an experiment, seize a GPU, stop
another task, overwrite outputs or change hyperparameters.

Use this for concrete AI/ML research-code tasks.

## Execution Flow

1. Understand the target outcome and local project context.
2. Inspect existing code, scripts, configs, and result artifacts before editing.
3. Choose the smallest complete implementation that preserves existing project patterns.
4. Implement with focused changes.
5. Use scoped static inspection or existing logs/results first. Honor explicit no-tests instructions. Run tests only when warranted; any model/data experiment or smoke run must be authorized and remote.
6. Update progress, pipeline, experiment registry, or issue tracker when useful.

## Chain Check

Before finalizing, verify:

- input format and availability
- processing steps and state changes
- output format and downstream expectations
- affected scripts/configs
- experiments or metrics needed to validate the claim

## Codex Rules

- Do not auto-commit or push unless explicitly requested.
- Do not add dependencies unless necessary or requested.
- Record failed runs if they affect research decisions.
- Keep implementation claims tied to actual verification output.
