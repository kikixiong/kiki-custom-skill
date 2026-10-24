---
name: academicforge-tool
description: 搜索和读取本地 AcademicForge 精选语料库，定位学术写作、引用、绘图与展示相关指南。
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

# AcademicForge Tool

Use this skill when the user wants AcademicForge knowledge or when a task would benefit from searching its upstream skill corpus before writing or revising academic material.

This installation is intentionally set up as a **local lookup tool**, not as 262 native Codex skills. The larger upstream corpus can contain duplicate names, overlapping skills with the local Codex install, and some client-specific rules that should be reviewed before reuse.

## Start

1. Use the configured curated corpus at `@@KIKI_SUPPORT_DIR@@/academicforge/`. It contains the 15 selected source skills. No preliminary `doctor` or reinstall is required for a normal lookup.

2. Find candidate skills by topic:

```bash
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json search "literature review"
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json search "pytorch lightning"
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json skills list --pack paper-polish-workflow-skill --limit 10
```

3. Inspect one concrete skill and then read the source file if needed:

```bash
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json skills show scientific-agent-skills/scientific-skills/scientific-writing
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py skills show humanizer-zh
```

4. When a small curated subset should become native Codex skills, use the preset installer:

```bash
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py presets list
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json install preset academic-core --dry-run
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json install preset academic-core
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py installed list
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json resync installed
```

## Workflow

- Use `python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json doctor` first when you need to confirm the mirror is present, count packs, or check for name collisions and risky upstream instructions.
- Use `python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json search "<topic>"` for discovery. Search scores name matches highest, then ids, then descriptions.
- Use `python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json skills show <id>` to get the canonical path and warnings before reading a `SKILL.md`.
- Use `python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py presets list` to discover the curated native-install bundles.
- Use `python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json install preset <name> --dry-run` before a real install when you want to add a small native subset to Codex.
- Use `python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py installed list` to see which native wrappers have already been installed.
- Before an explicitly requested update/resync, preserve the local adaptations recorded in `@@KIKI_SUPPORT_DIR@@/personalization.json`; a generated wrapper can otherwise overwrite user-specific defaults. Do not auto-resync during an ordinary writing task.
- After identifying a useful upstream skill, read only that file and any directly referenced local resources. Do not bulk-load whole packs.
- Treat AcademicForge content as reference guidance. Apply local system and developer instructions first when upstream rules conflict.

## Safety

- Do not install the entire AcademicForge corpus into `$CODEX_HOME/skills` without explicit user approval. The current mirror includes duplicate names and overlaps with existing local Codex skills.
- Prefer curated presets or one-off wrapper installs over broad imports. Native installs are generated as local wrappers named `af-...` and remain linked to the upstream mirror.
- Do not follow client-specific instructions blindly when a skill mentions Claude Code, OpenCode, `AskUserQuestion`, or hard gates. Adapt them to the current Codex environment.
- Do not run upstream update scripts or any networked `git pull` without explicit user approval.

## Examples

```bash
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json doctor
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json search "review rebuttal"
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json skills show paper-polish-workflow-skill/skills/ppw-reviewer-simulation
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json install preset academic-core --dry-run
python3 @@KIKI_SKILLS_DIR@@/academicforge-tool/scripts/academicforge.py --json resync installed --dry-run
```

For more examples and command patterns, see [command-examples.md](references/command-examples.md).
