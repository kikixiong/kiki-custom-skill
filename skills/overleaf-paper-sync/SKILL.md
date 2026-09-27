---
name: overleaf-paper-sync
description: Orchestrate evidence-grounded LaTeX paper planning and revision through a review-gated Overleaf Git workflow. Use when a user wants to write or revise an Overleaf paper one paragraph, caption, equation block, table, or other small reviewable slice at a time; push every revision candidate to Overleaf for web review; wait for explicit approval before continuing; or reconcile feedback and web edits without batching or overwriting accepted text.
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Overleaf Paper Sync

## Purpose

Use `$kiki-paper-writing` as the scientific writing and revision engine. Use this
Skill as the orchestration, Git synchronization, and approval layer.

Keep exactly one revision slice awaiting review. After the plan is approved,
edit one slice, validate it, commit it, push it to Overleaf, present a review
packet, and stop. Do not edit the next slice until the user explicitly approves
the latest pushed commit.

Treat these states as distinct:

- `planned`: scope and intent are agreed, but no edit exists;
- `drafted`: a local candidate exists, but is not yet published;
- `confirmed`: wording is accepted before publication, but is not yet verified
  in Overleaf;
- `pushed`: the exact candidate is visible in Overleaf and awaits review;
- `approved`: the user explicitly accepted the latest pushed commit;
- `synchronized`: local `HEAD` and Overleaf `master` agree.

Never infer `confirmed` or `approved` from `pushed`, and never infer
`synchronized` from a successful local commit.

## Use direct Overleaf Git

Prefer a direct Overleaf Git remote so that a successful push immediately
updates the project reviewed in the Overleaf web editor. Identify it by its
remote URL or by the user's explicit selection; do not assume its remote name.

Read [overleaf-git.md](references/overleaf-git.md) before configuring a remote,
handling authentication, resolving a synchronization problem, moving or
renaming files, or relying on Overleaf comments or Track Changes.

If only GitHub synchronization is available, explain that Overleaf does not
automatically pull each GitHub push into the web project. Ask the user to add or
select a direct Overleaf Git remote if immediate web review is required. Do not
claim that a GitHub push is already visible in Overleaf.

## Start the session safely

Before planning or editing:

1. Locate the repository root and inspect `git status --short`,
   `git branch --show-current`, recent commits, remotes, and upstream state.
2. Identify the direct Overleaf remote and its single target branch, `master`.
3. Never print, store in a command, or commit an Overleaf authentication token.
   Ask the user to configure authentication outside chat if credentials block a
   fetch or push.
4. Fetch `master` from the Overleaf remote. When the worktree is clean and the
   remote is strictly ahead, fast-forward the local branch. If histories have
   diverged or the synchronization base is uncertain, stop before editing and
   show the competing commits.
5. Inspect existing uncommitted changes. Preserve them and exclude unrelated
   files from staging. If they overlap the intended slice, ask the user how to
   treat them before modifying that slice.
6. Discover the main TeX file and the project's existing build command. Run a
   baseline build when practical so pre-existing failures can be distinguished
   from failures introduced by a slice.
7. Confirm that the Overleaf web project being reviewed corresponds to the
   selected remote. Never push to a guessed remote or project.

Use read-only inspection freely. Do not make a manuscript edit until the user
approves the revision plan.

## Build and approve the revision plan

Classify the paper task and load the relevant `$kiki-paper-writing` workflow,
foundation, section guidance, and checklist. Diagnose from paper story down to
sentence expression; do not begin with surface polish when a higher-level
problem exists.

Propose an ordered queue of reviewable slices. Give each slice a stable ID such
as `S01`, `S02`, and include:

- exact file and section or anchor;
- one role or problem to solve;
- intended semantic change;
- evidence, claim, terminology, or dependency risk;
- any mechanically necessary companion change.

Default to one paragraph. Use one caption, one table, one equation block, or one
coherent algorithm step when paragraph boundaries are not meaningful. Keep a
terminology rename or cross-reference repair with its smallest mechanically
necessary companions and disclose that expanded scope.

Ask the user to approve or revise the queue. Wait for approval before applying
`S01`. Put newly discovered work into the queue instead of silently expanding
the active slice.

## Execute one atomic slice

For the active slice only:

1. Fetch Overleaf `master` again immediately before editing. Integrate a clean
   fast-forward. If the user changed the active text on the web, treat that text
   as new input and preserve it.
2. Restate the slice's intent without strengthening the science.
3. Apply the smallest edit that resolves the agreed problem. Preserve accepted
   wording and unrelated formatting.
4. Inspect the diff at word and line level. Check the paragraph role, causal
   edges, claim strength, evidence support, terminology, symbols, citations,
   cross-references, and downstream consistency using `$kiki-paper-writing`.
5. Run `git diff --check`, scan the changed files for conflict markers, and use
   the project's available LaTeX build or lint command. Distinguish baseline
   failures from newly introduced failures.
6. Do not publish a candidate with a newly introduced compile error, unresolved
   conflict, unsupported claim, or accidental out-of-scope change.
7. Stage exact paths with `git add -- <paths>`. Never use `git add .`,
   `git add -A`, or commit unrelated dirty files.
8. Review `git diff --cached --stat` and the complete staged diff. Commit with a
   message such as `overleaf: S03 revise introduction gap paragraph`.
9. Fetch Overleaf `master` once more before pushing. If it advanced, integrate
   it only when the update is a clean, semantics-preserving fast-forward or a
   conflict-free rebase of the unpublished active-slice commit. Stop on any
   semantic overlap or conflict.
10. Push the current local commit to the Overleaf target:
    `git push <overleaf-remote> HEAD:master`.
11. Verify the remote `master` hash and record the pushed commit. Mark the slice
    `pushed`, not `approved`.

Never amend, squash, force-push, or rewrite a commit that has already been
pushed for review. Publish feedback revisions as new commits such as `S03-r2`.

## Hand off for web review

After each push, give a compact review packet in the user's language:

```text
Slice S03 — PUSHED / awaiting approval
Commit: <short hash>
Scope: <file + paragraph/caption/table anchor>
Changed: <semantic before → after summary>
Checks: <build/lint status and any baseline issue>
Review in Overleaf: <specific point to inspect>
Reply “approve S03” / “通过 S03” to continue, or send revision comments.
```

Provide the Overleaf project link when it is already known or can be derived
without exposing credentials. Do not report a push as successful unless the
push command and remote verification succeeded.

End the turn after the review packet. Do not draft, edit, commit, or push the
next slice while one slice is awaiting approval.

## Process approval and feedback

Accept `approve`, `approved`, `LGTM`, `通过`, or another unambiguous acceptance
only for the latest pushed slice. If multiple candidates or commits could be
meant, ask which commit is approved.

On approval:

1. Mark the latest pushed commit `approved`.
2. Fetch Overleaf `master` to capture any web edits made during review.
3. Inspect those web edits before proceeding; never overwrite them.
4. Move to the next planned slice and run the atomic loop.

On revision feedback:

1. Keep the active slice open and leave later slices untouched.
2. Fetch Overleaf first so comments implemented directly in the web editor
   become part of the baseline.
3. Map each comment to a concrete edit and revise only the smallest necessary
   scope.
4. Validate, create a new commit, push, and issue a new review packet.
5. Wait again; do not treat requested changes as approval.

If the user approves wording in chat before it is pushed, mark it `confirmed`
only. Still publish and verify the exact candidate before marking it
`synchronized`, and still obtain approval for the pushed commit unless the user
explicitly waives that gate.

## Handle failures conservatively

- On non-fast-forward rejection, fetch and compare local `HEAD`, the previous
  remote base, and current remote `master`. Rebase only an unpublished
  active-slice commit when the result is conflict-free and semantically
  unchanged; otherwise stop for user review.
- On authentication failure, do not request that a token be pasted into chat.
  Point the user to Overleaf token authentication and credential-helper setup.
- On an introduced LaTeX failure, repair it within the active slice and rerun
  validation before pushing.
- On a baseline LaTeX failure unrelated to the slice, report it explicitly and
  avoid widening scope unless the user adds a repair slice.
- On a partial or uncertain push, inspect local and remote hashes before
  retrying so duplicate or misleading commits are not created.
- Never use force push, hard reset, destructive checkout, or automatic conflict
  selection. Never stash user changes without permission.

## Preserve reviewability

Keep one coherent semantic change per commit. Avoid file moves, broad
reformatting, generated build files, and global wording churn in a content
slice. Do not depend on Overleaf Track Changes or comments as the durable review
record while Git pushes are active; preserve review history through atomic
commits, slice IDs, and the task conversation.

For long sessions, recover the slice ledger from the current task plan and
commit messages beginning with `overleaf:`. Never add a workflow ledger to the
paper repository unless the user requests it.
