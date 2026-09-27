# Kiki Custom Skill — repository instructions

This is Kiki's private personal-use collection. Read README.md and the relevant
INSTALL_CODEX.md or INSTALL_CLAUDE_CODE.md when asked to install it.

- Keep Kiki Paper Writing as `skills/kiki-paper-writing`; the separate full
  workflow is `skills/kiki-paper-workflow`. Preserve all supporting resources.
- Maintain portable `@@KIKI_*@@` templates and install.py together. Never put a
  fixed Mac username, machine IP, login token, SSH key or account state in the repo.
- Personal skills install to the current machine's `~/.codex/skills` or
  `~/.claude/skills`. Respect configured client-home overrides. Do not mistake
  cloning the repo for installation, or a profile name for remote deployment.
- Preserve existing same-name skills via the installer's backups, unrelated
  skills, system skills and plugin management. Never wipe an entire skill root.
- Reuse existing service access. Do not run authorization preflights. Do not
  execute functional tests/model/data experiments unless the user asks for them.
- Keep licenses and provenance, especially pinned upstream asset directories.
  Branding this collection does not change upstream ownership or license terms.
- `reference/` is an archive, not an automatically installed capability. Explain
  actual platform limitations rather than claiming every tool works everywhere.
- Commit only intended changes. Never push secrets or private library PDFs.
