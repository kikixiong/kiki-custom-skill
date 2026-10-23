---
name: monitor-experiment
description: 查看运行中实验的进度、日志和输出结果。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Monitor Experiment Results

Read progress, logs and saved outputs for the requested run. One snapshot is the
default. Do not create recurring monitoring merely because this skill is loaded.

## Locate the run

Use launch notes or the run manifest for execution host, run ID, job/session,
code, log and result paths. Confirm the actual target before operations; do not
assume a host alias or directory layout. Resolve placeholders before commands.

Monitor another existing backend only when the user/run context identifies it.
Do not assume `screen`, create a cloud instance or launch a replacement job.

## Read available evidence

1. Read a bounded tail of the identified remote log and the relevant job/process
   state. If the run uses tmux/screen/scheduler, use that run's recorded session.
   Prefer existing logs over creating shared `/tmp` screen dumps.
2. Read small saved JSON/CSV summaries from the run directory. Follow the run's data-handling
   and execution policy; do not transfer datasets or rerun evaluation implicitly.
3. If a W&B run is already configured, use its exact URL/entity/project/run ID.
   Reuse access; missing W&B is not a failed experiment and does not require setup.
4. Compare baseline and treatment only when their evaluation settings match.
   Include metric values, step/time, baseline delta and whether results are partial.
5. Report crashes, stale logs or uncertainty with evidence. Do not relaunch, change
   hyperparameters, seize GPUs or stop jobs as a side effect of monitoring.

## Report and follow-up

Return a compact run/metric/status table in this Codex task with evidence paths
and available W&B links. For training quality use `$training-check`.

If the user explicitly asks to keep watching or notify later, use the Codex
automation tool, reuse an existing matching monitor, and notify only on a
meaningful change, completion, failure or required action. Quiet unchanged runs
do not need repeated status messages. No Feishu/email/Slack message is authorized
by a configuration file; send externally only when explicitly requested.
