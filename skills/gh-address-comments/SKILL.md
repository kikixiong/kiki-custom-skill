---
name: gh-address-comments
description: 读取 PR 审查反馈并处理选定的修改意见。
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

# GitHub PR Comment Handler

Use this skill when the user wants to work through requested changes on a GitHub pull request. Discover available GitHub connector tools for PR metadata, patch context and review threads. Use `gh api graphql` or the bundled script when the available connector lacks complete thread state.

The user has confirmed GitHub authorization through the current machine's existing connection. Use the existing connection/session for the actual request without `gh auth status`, login tests or a new login prompt. Follow the active permission policy; do not require elevated network access.

## Workflow

1. Resolve the PR.
   - If the user provides a repository and PR number or URL, use that directly.
   - If the request is about the current branch PR, use local git context plus `gh pr view --json number,url` to resolve it.
2. Inspect review context with thread-aware reads.
   - Use the GitHub app from this plugin to fetch PR metadata and patch context when the repo and PR are known.
   - Use a thread-aware connector when available, or `@@KIKI_SKILLS_DIR@@/gh-address-comments/scripts/fetch_comments.py` for the current-branch PR. The script fetches `reviewThreads`, `isResolved`, `isOutdated`, and file/line anchors. For a supplied different PR, use the connector or explicit `gh api graphql` repository/number arguments instead of assuming the current branch.
   - Flat comment reads suffice for top-level summaries; actionable inline reviews require complete thread state regardless of transport.
3. Cluster actionable review threads.
   - Group comments by file or behavior area.
   - Separate actionable change requests from informational comments, approvals, already-resolved threads, and duplicates.
4. Confirm scope before editing.
   - Present numbered actionable threads with a one-line summary of the required change.
   - If the user did not ask to fix everything, ask which threads to address.
   - If the user asks to fix everything, interpret that as all unresolved actionable threads and call out anything ambiguous.
5. Implement the selected fixes locally.
   - Keep each code change traceable back to the thread or feedback cluster it addresses.
   - If a comment calls for explanation rather than code, draft the response rather than forcing a code change.
6. Summarize the result.
   - List which threads were addressed, which were intentionally left open, and what tests or checks support the change.

## Write Safety

- Do not reply on GitHub, resolve review threads, or submit a review unless the user explicitly asks for that write action.
- If review comments conflict with each other or would cause a behavioral regression, surface the tradeoff before making changes.
- If a comment is ambiguous, ask for clarification or draft a proposed response instead of guessing.
- Do not treat flat PR comments from the connector as a complete representation of review-thread state.
- If an actual request fails, distinguish authentication/permissions, rate limits and network errors. A rate limit is not a reason to log in again. Reuse another already available transport when appropriate; request account action only if the actual failure requires it.

## Fallback

If neither the connector nor `gh` can resolve the PR cleanly, tell the user whether the blocker is missing repository scope, missing PR context, or CLI authentication, then ask for the missing repo or PR identifier only when that context is missing; request refreshed authorization only if an actual operation established that need.
