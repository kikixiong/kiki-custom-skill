# Kiki Custom Skill

Read AGENTS.md, README.md and INSTALL_CLAUDE_CODE.md before installing or
maintaining this collection. Install into the current user's Claude Code skill
directory, respecting the configured client home. Use `python3 install.py
--target claude` or `--target both`; do not directly link unrendered templates. Pass
`--claude-allow-read` (after the user agrees to a settings.json change) so the
category routers can read leaf SKILL.md files; without it routing silently
degrades. Tell the user to open a new session afterwards.

Same-name skills are backed up, while system/plugin snapshots remain reference
only. Keep machine-specific settings in the local client configuration described
in README, not in shared skills. Do not run skill tests, model experiments or
unrelated login probes unless the task requests them.
