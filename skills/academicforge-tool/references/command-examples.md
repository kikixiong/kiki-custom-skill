# AcademicForge CLI Examples

## Health

```bash
academicforge --json doctor
academicforge packs list
```

## Discovery

```bash
academicforge --json search "abstract polishing"
academicforge --json search "single-cell analysis" --pack scientific-agent-skills --limit 5
academicforge --json skills list --pack AI-research-SKILLs --query "axolotl" --limit 5
```

## Inspection

```bash
academicforge --json skills show humanizer-zh
academicforge skills show scientific-agent-skills/scientific-skills/scientific-writing --preview-lines 25
academicforge --json skills list --warnings-only --limit 20
academicforge --json skills list --duplicates-only --limit 20
```

## Native Install

```bash
academicforge presets list
academicforge --json install preset academic-core --dry-run
academicforge --json install preset academic-core
academicforge installed list
academicforge --json install preset zh-review-stack --dry-run
academicforge uninstall af-citation-management --dry-run
academicforge --json resync installed
```
