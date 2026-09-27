# AutoDL Experiment Skill English Mirror

Use this skill for AutoDL or SeetaCloud-style SSH GPU experiments. It should behave like an interactive experiment assistant, not a fixed script.

## Operating Principles

- Infer configuration from the project, existing scripts, logs, and runbooks first.
- Ask only for missing information that affects execution or safety.
- Ask no more than three high-priority questions at a time.
- Never persist SSH passwords, SMTP app passwords, API tokens, HF tokens, private keys, or private dataset URLs.

## Flexible Inputs

Collect or infer:

- SSH host, port, user, and authentication method.
- Existing remote shell script or launch command.
- Project name, run id, conda environment, remote root, output path.
- Progress source: log percentage, epoch/step, progress file, artifacts, or heartbeat-only fallback.
- Email provider, recipient, SMTP configuration, notification thresholds.

## Notification Behavior

Default alerts are 50%, 75%, 100%, and failure. The user may choose custom thresholds such as `25,50,75,100`, completion-only alerts, failure-only alerts, or heartbeat-style alerts when no reliable progress signal exists.

For already-running jobs, prefer sidecar log monitoring. Do not restart or kill the running process unless the user explicitly asks.

## Safety

Ask for explicit confirmation before destructive cleanup, overwriting run directories, killing broad process groups, deleting checkpoints/results, or publishing logs to a public repository.
