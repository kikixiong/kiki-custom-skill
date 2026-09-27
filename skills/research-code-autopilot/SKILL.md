---
name: research-code-autopilot
description: 统筹科研代码、训练评估脚本、复现、日志和故障处理。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Research Code Autopilot

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
evaluation still belongs on the remote host, with the agreed data/configuration
and allocated resources. Do not change the scientific setup just to shorten a
test. Label partial results as partial and never strengthen claims from a pilot.

## Final Report

Report:

- files changed
- command(s) run
- key metric or artifact path
- what remains blocked, if anything

Never upgrade a paper claim from a smoke run. Label pilots, single-seed results, and partial suites explicitly.
