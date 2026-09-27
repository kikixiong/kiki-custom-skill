---
name: overleaf-sync
description: 复用本机已有 Overleaf 授权与项目配置，同步论文，并衔接 Kiki 写作流程。
metadata:
  upstream-argument-hint:
  - setup <project-id> | pull | push | status
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Overleaf Sync

Synchronize the user's existing local paper and Overleaf project. GitHub and
Overleaf are used through the current machine's existing connection. Reuse that configuration;
do not begin with login checks, a new token, a new clone or the setup helper.

## Choose the requested workflow

- Plain pull/push/status: use this skill with the existing project and transport.
- Scientific drafting/revision: use `$kiki-paper-writing` by default.
- Explicit paragraph-by-paragraph Overleaf review: use the user's
  `@@KIKI_SKILLS_DIR@@/overleaf-paper-sync/SKILL.md` and its existing
  slice approval workflow. Do not impose that workflow on an ordinary sync.
- Full Kiki Custom pipeline: use `$kiki-paper-workflow` only when that chain is requested.

## Resolve the actual project

1. Use the active task, known Overleaf project link, local checkout and project
   notes to identify the manuscript. Ask only if multiple plausible targets remain.
2. Inspect the local worktree and identify the existing Overleaf Git remote or
   connected Overleaf capability. Redact embedded credentials if inspecting URLs.
3. Derive local directory, remote name, target branch and main TeX file from that
   project. Do not assume `paper/`, `paper-overleaf/`, `origin` or a local `master`.
   The direct Overleaf workflow uses its existing remote branch (normally `master`);
   inspect the configured target before using it.
4. Preserve all unrelated local edits and collaborators' web changes. Do not create
   a second mirror or change credential helpers merely to match an upstream example.

## Pull

Fetch the actual requested remote, compare against the current checkout and
fast-forward when clean. If there is a separate paper copy already configured,
copy only the intended files into the actual destination. Preserve tracked
collaborator edits. Resolve routine unambiguous integration within the authorized
scope; ask about semantic conflicts or an unclear authoritative version.

Inspect changed claims, numbers and citations when that matters to the writing
task. Sync does not require an entire paper-review pipeline or test suite.

## Push

1. Review local changes and fetch current remote state to avoid overwriting web edits.
2. Prepare only the requested manuscript changes. Do not use blanket `rsync --delete`
   or stage unrelated files. Stage explicit paths in a Git workflow.
3. Give a concise description of the concrete changes. An explicit request to sync
   or push authorizes that action; do not ask for it again. If only local writing was
   requested, prepare the candidate before asking whether to publish it.
4. Commit and push to the identified Overleaf remote and branch, or use an available
   connector operation with equivalent scope. Never force-push or reset shared history.
5. Report actual operation results. A GitHub push alone does not establish that the
   corresponding Overleaf web project has updated.

## Status and recovery

Status reads project/worktree and remote state; it is not a separate auth test.
If an actual fetch, push or connector request fails, preserve local work, report
the specific failure, and distinguish connectivity, access and merge problems.
Do not infer that a 401 always means the user's Keychain entry expired, inspect
secrets, or rerun setup automatically.

Only when the user requests a new Git bridge that is not already configured,
consult the optional helper at
`@@KIKI_SUPPORT_DIR@@/aris/tools/overleaf_setup.sh`.
It is not part of routine synchronization. Never request a token in chat.

## Deliverable

Report the actual project, synchronized files, direction, commit/remote result
when applicable, and any unresolved conflict. Use the current project's paths.
