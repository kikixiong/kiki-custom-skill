---
name: gh-fix-ci
description: 检查 GitHub Actions 失败日志、定位原因并修复。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# GitHub Actions CI Fix

Inspect failing GitHub Actions checks for the requested repository/PR, explain
the observed cause and apply fixes within the user's authorized scope.

Use the current machine's existing GitHub connection. Use the current connector or
existing `gh` session directly for the real request; do not run `gh auth status`,
login tests or demand fresh authentication as a prerequisite.

## Workflow

1. Resolve the supplied PR/repository or current branch PR. Use available GitHub
   connector tools for checks/logs when supported; discover their actual schema.
2. For CLI fallback, use the installed helper:
   `python3 @@KIKI_SKILLS_DIR@@/gh-fix-ci/scripts/inspect_pr_checks.py --repo <actual-repo> --pr <number-or-url> --json`.
   It reads failing checks and Actions logs; it does not rerun CI or run local tests.
3. Read the failing run/job logs and changed-file context. Distinguish actual
   failures, missing logs, ongoing jobs, unrelated failures and external providers.
4. State a focused diagnosis and fix. A request to fix CI authorizes relevant
   reversible code changes; do not add another blanket approval gate. A read-only
   diagnosis request does not authorize edits or a workflow rerun.
5. Use the user's lightweight verification policy. Honor a no-tests instruction,
   reuse applicable prior evidence and respect the user's execution-environment restrictions.
   Do not automatically install dependencies or change the environment.
6. Report changes, evidence, checks actually performed and remaining uncertainty.

If an actual operation fails, distinguish permissions/authentication from rate
limits or connectivity. Use an already available alternative transport when
appropriate. Ask for account action only when the actual failure requires it;
never ask the user to paste a token. Do not assume all connectors lack Actions logs.
