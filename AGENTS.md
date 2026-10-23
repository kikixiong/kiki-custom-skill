# Kiki Custom Skill — repository instructions

This is a portable collection for Codex and Claude Code. Read README.md and the
relevant INSTALL_CODEX.md or INSTALL_CLAUDE_CODE.md before installation.

- Keep `skills/kiki-paper-writing` and the separate `skills/kiki-paper-workflow`
  entrypoints and their supporting resources.
- Maintain portable `@@KIKI_*@@` templates and install.py together. Do not embed
  personal usernames, host aliases, IPs, project roots, credentials, account
  state or machine-specific execution policies in shared files.
- Install to the current client's user skill directory, respecting its home
  override. Keep optional environment settings in that client's local
  `skill-config/kiki-custom-skill/environment.md`, outside this repository.
- Preserve same-name skills through backups, unrelated skills, system skills
  and plugin management. Never wipe an entire skill root.
- Reuse existing service access. Do not run unrelated authorization preflights.
  Do not execute functional tests or model/data experiments unless requested.
- Preserve licenses, authorship and source provenance. Collection branding does
  not change ownership. Record portability adaptations to imported material.
- `reference/` is an archive, not an automatically installed capability. Explain
  actual platform limitations rather than claiming tools work everywhere.
- Review intended changes and scan for personal environment data before commit.
  Never commit local configuration, credentials or private library documents.
