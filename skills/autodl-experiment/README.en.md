# AutoDL Experiment Runner

![Codex Skill](https://img.shields.io/badge/Codex-Skill-111827?style=flat-square)
![AutoDL Workflow](https://img.shields.io/badge/AutoDL-Workflow-2563EB?style=flat-square)
![Email Alerts](https://img.shields.io/badge/Email-Alerts-16A34A?style=flat-square)
![Bilingual](https://img.shields.io/badge/Docs-ZH%20%2F%20EN-F59E0B?style=flat-square)
![Security Aware](https://img.shields.io/badge/Security-Secret%20Aware-DC2626?style=flat-square)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)

A Codex Skill for running AutoDL / SeetaCloud-style SSH GPU experiments with safer launch scripts, concise monitoring, email progress alerts, artifact pullback, and append-only runbooks.

## Install

Clone directly into the Codex skills directory:

```powershell
git clone https://github.com/handsomeZR-netizen/autodl-experiment-skill "$env:USERPROFILE\.codex\skills\autodl-experiment"
```

Or use it as a project-local skill:

```powershell
git clone https://github.com/handsomeZR-netizen/autodl-experiment-skill .codex\skills\autodl-experiment
```

## Example Prompt

```text
Use $autodl-experiment to launch my training job on AutoDL.
Ask me for any missing SSH, conda, run.sh, and email alert settings.
Notify me at 50%, 75%, 100%, and when the job fails.
```

## What It Handles

- remote SSH GPU experiment launch;
- AutoDL data disk and HuggingFace cache layout;
- tmux/screen background execution;
- progress parsing from percentages, epoch/step logs, progress files, or artifacts;
- SMTP email alerts for progress, success, and failure;
- sidecar monitoring for already-running jobs;
- result pullback and reusable runbook notes.

## Security

The skill is designed to avoid storing secrets. SSH passwords, SMTP app passwords, API keys, HF tokens, and private keys should only be provided through secure runtime prompts, remote environment variables, or uncommitted `.env` files.

## License

MIT
