---
name: research-task-executor
description: 执行一个明确的科研代码或实验实现任务，并更新任务记录。
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

# Research Task Executor

## Execution environment

Resolve the authorized host, project root, Python environment, datasets, weights
and device allocation from the task, project configuration or run manifest.
Use isolated code/output directories appropriate to that project. Before an
approved run, inspect devices, disk, processes, data/weights, destinations and
locks; respect queue priorities and preserve resumable checkpoints.

Follow the user's local execution restrictions. An unavailable host does not
authorize moving the experiment elsewhere. A plan does not authorize launching
an experiment, seizing a device, stopping another task, overwriting outputs or
changing hyperparameters.

Use this for concrete AI/ML research-code tasks.

## Execution Flow

1. Understand the target outcome and local project context.
2. Inspect existing code, scripts, configs, and result artifacts before editing.
3. Choose the smallest complete implementation that preserves existing project patterns.
4. Implement with focused changes.
5. Use scoped static inspection or existing logs/results first. Honor explicit no-tests instructions. Run tests only when warranted; any model/data experiment or smoke run must use the authorized execution environment.
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
