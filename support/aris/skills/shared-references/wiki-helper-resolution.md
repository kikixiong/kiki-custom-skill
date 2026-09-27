# Wiki helper resolution for this Codex installation

Use the installed helper, not an assumed author checkout or project `tools/`.
Resolve wiki output against the active project and preserve its existing layout.

```bash
WIKI_SCRIPT="@@KIKI_SUPPORT_DIR@@/aris/tools/research_wiki.py"
[ -f "$WIKI_SCRIPT" ] || WIKI_SCRIPT="@@KIKI_SKILLS_DIR@@/research-wiki/research_wiki.py"
```

If the user explicitly selected a project-specific ARIS helper, use that recorded
path after confirming it exists. No `.aris/installed-skills.txt` manifest or
upstream clone is required for this global Codex installation. Do not search up
the directory tree, download another copy or run `install_aris.sh` by default.

For `$research-wiki`, a missing helper is a concrete blocker: report the missing
path. For caller skills, deliver the primary result and disclose a skipped wiki
update. Do not claim to have ingested records when no helper operation succeeded.

Invoke the located helper with the required subcommand and the actual project
wiki directory. Existing wiki data must not be overwritten or reinitialized as
part of path resolution. See [integration-contract.md](integration-contract.md).
