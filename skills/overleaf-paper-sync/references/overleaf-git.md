# Overleaf Git operating notes

Read this reference when setting up or troubleshooting synchronization, when
changing repository structure, or when deciding how the user should review in
the Overleaf web editor.

Last checked against official Overleaf documentation: 2026-07-26.

## Direct Git integration

- Overleaf Cloud Git integration is a premium feature. It is also available on
  Overleaf Server Pro when enabled by the administrator.
- Obtain the exact Git URL from the project's **Integrations → Git** interface.
  A Cloud project URL of `https://www.overleaf.com/project/<PROJECT_ID>` uses
  `https://git.overleaf.com/<PROJECT_ID>` as its Git URL.
- Use token-based authentication. When prompted, use username `git` and the
  user's Overleaf Git authentication token as the password.
- Never place a token in a repository URL, command, commit, log, or chat
  message. Let the user configure an OS or Git credential helper privately.
- Overleaf Git exposes one linear branch named `master`. Push a differently
  named local branch with:

  ```bash
  git push <overleaf-remote> HEAD:master
  ```

- A fetch or pull may cause Overleaf to create a just-in-time Git commit for
  recent web-editor history. Fetch before each slice and again before push.

Official documentation:

- [Git integration](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/git)
- [Authentication tokens](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/git/git-integration-authentication-tokens)
- [Advanced Git operations](https://docs.overleaf.com/integrations-and-add-ons/git-integration-and-github-synchronization/git/advanced-git-operations)

## GitHub synchronization differs

Overleaf's GitHub synchronization is not automatic. A GitHub push alone does
not prove that the new revision is visible in Overleaf; the user must perform
the appropriate pull/synchronization action in Overleaf. Prefer the direct Git
integration for a push-then-review loop.

Do not claim that an Overleaf web project is synchronized merely because a
GitHub remote accepted a push.

## Important limitations

- Do not use branches or tags on the Overleaf remote.
- Do not add Git LFS objects or nested Git submodules.
- Avoid symlinks; Overleaf can convert them to regular files.
- Set `core.fileMode=false` locally if permission churn creates irrelevant
  diffs; Overleaf does not preserve executable permissions.
- Avoid moving or renaming files that carry Overleaf comments or Track Changes.
  Git-side renames become delete-and-create operations and can lose associated
  metadata.
- Avoid mixing active Git pushes with reliance on Track Changes or comments.
  Pushes can displace or lose them. Prefer reviewing the rendered or source text
  visually and recording decisions by slice ID and commit.
- Split large or structural changes into smaller commits. Large changes can
  time out, and folder renames can leave empty folders on the Overleaf side.
- Disable aggressive automatic remote polling if it triggers Git Bridge rate
  limits.

## Conflict policy

Treat the Overleaf web state as collaborator work:

1. Fetch `master`.
2. Compare the previous remote base, local `HEAD`, and current remote `master`.
3. Preserve all remote edits.
4. Fast-forward when possible.
5. Rebase only unpublished, active-slice local work when no semantic conflict
   exists.
6. Stop for user direction when both sides changed the same scientific text,
   formula, caption, citation, or terminology.

Never force-push to make a conflict disappear.
