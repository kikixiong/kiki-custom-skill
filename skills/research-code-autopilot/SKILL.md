---
name: research-code-autopilot
description: 统筹科研代码、训练评估脚本、复现、日志和故障处理。
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

# Research Code Autopilot

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

Use this skill for code-heavy research work where the goal is a reproducible experimental result, not just a passing unit test.

## First Pass

1. Read the nearest README and dependency/config files.
2. Identify entrypoints: `train*.py`, `eval*.py`, `run*.sh`, `scripts/*`, `configs/*`, `exp/*`.
3. Inspect existing result conventions: `outputs/`, `runs/`, `results/`, `logs/`, `artifacts/`, `wandb/`.
4. Check git status before edits and preserve unrelated changes.

## Implementation Rules

- Reuse the project's existing CLI/config style.
- Prefer parameterizing one existing script over making `new.py`, `v2.py`, or one-off notebooks.
- Keep randomness explicit: seed, split, device, checkpoint, dataset version.
- For metrics, log sample count, split name, aggregation method, and baseline comparator.
- For generated artifacts, write a machine-readable file first (`json`, `csv`, `jsonl`) and derive markdown/figures from it.

## Verification scope

Use the user's lightweight policy and explicit task instructions. Inspect code
and existing evidence first; run only checks that address a concrete new risk.
Honor a no-tests request and reuse applicable prior results. Do not run blanket
`pytest` or assume a script's `--help`/`--dry-run` is free of model/data execution.

Any authorized smoke run, tiny-dataset check, CPU fallback experiment or metric
evaluation belongs in the agreed execution environment, with the agreed data,
configuration and allocated resources. Do not change the scientific setup just to shorten a
test. Label partial results as partial and never strengthen claims from a pilot.

## Final Report

Report:

- files changed
- command(s) run
- key metric or artifact path
- what remains blocked, if anything

Never upgrade a paper claim from a smoke run. Label pilots, single-seed results, and partial suites explicitly.
