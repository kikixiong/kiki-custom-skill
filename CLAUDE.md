# Kiki Custom Skill

Read `AGENTS.md`, `README.md` and `INSTALL_CLAUDE_CODE.md` before installing or
maintaining this personal skill library. Install Claude Code skills into the
current user's `~/.claude/skills`, with configured home overrides respected.
Use `python3 install.py --target claude` or `--target both`; do not directly
link unrendered templates into the skills directory. Existing skills are backed
up, and plugins/system snapshots remain reference-only. Do not run skill tests,
model experiments or login probes unless the user specifically requests them.
