---
name: skill-advisor
description: Search and discover existing Codex skills before creating new ones. Prevents duplicate skills by indexing available skills and finding similar functionality. Use when the user wants to create a new skill, asks about available skills, or needs recommendations on skill reuse versus creation.
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Skill Advisor

Helps prevent duplicate skills by searching existing Codex skills before creation.

## When to Use

Use this skill when:

- User wants to create a new skill
- User asks "do we already have a skill for X?"
- User needs advice on whether to extend existing skill vs create new one
- User wants to browse available skills

## How It Works

### 1. Index Skills (Run Once or Periodically)

```bash
python3 scripts/index_skills.py
```

This scans all `SKILL.md` files in configured Codex skill roots and creates `references/skills_index.json` with:
- Skill names
- Descriptions
- File paths

The index is saved locally and can be updated anytime.

### 2. Search for Similar Skills

When user describes a new skill idea, search for existing skills:

```bash
python3 scripts/search_skills.py "<description of proposed skill>"
```

**Examples:**

```bash
# Search for PDF-related skills
python3 scripts/search_skills.py "pdf document editing rotation"

# Search for messaging skills
python3 scripts/search_skills.py "send messages telegram whatsapp"

# Search for code/development skills
python3 scripts/search_skills.py "coding agent development review"
```

The script outputs:
- Top matching skills (ranked by similarity)
- Skill descriptions
- File paths for reference

### 3. Provide Recommendations

Based on search results, advise the user:

**High similarity (>40%)**:
- "You already have `<skill-name>` which does X. Consider extending it instead."
- Show the skill's location and description
- Ask if they want to see the existing skill's SKILL.md

**Medium similarity (20-40%)**:
- "There's a similar skill `<skill-name>`, but your use case might be different."
- Explain what the existing skill does
- Ask if their need is different enough to warrant a new skill

**Low/no similarity (<20%)**:
- "No similar skills found - this looks like a unique use case!"
- Proceed with skill creation

## Language Check (New!)

Before packaging a skill, verify it contains only English content:

```bash
python3 scripts/check_language.py <path/to/skill-directory>
```

**What it checks:**
- All `.md` files in the skill directory
- Detects non-English characters in documentation text
- Allows non-English in:
  - Example inputs (in tables, quotes, arrows)
  - Code blocks
  - URLs

**Example:**
```bash
python3 scripts/check_language.py @@KIKI_SKILLS_DIR@@/my-skill

# Output:
✅ All content is in English
# or
❌ Found non-English content:
   File: README.md
   Line 15: 这是中文说明  # Documentation text in Chinese - fix this!
```

**Why English-only?**
- Universal compatibility
- Easier for others to understand and contribute
- Better searchability and documentation
- Example inputs can still be in any language (e.g., for i18n skills)

## Example Workflow

**User says:** "Create a skill for managing GitHub pull requests"

**You do:**

1. Run search:
   ```bash
   python3 scripts/search_skills.py "github pull request review comments"
   ```

2. Analyze results and respond:
   - If `gh-pr-review` exists with 60% match: "You already have `gh-pr-review` which handles PR reviews and comments. Want to extend it or is your use case different?"
   - If no match: "No existing GitHub PR skills found. Let's create a new one!"

3. **Before packaging**, check language:
   ```bash
   python3 scripts/check_language.py path/to/new-skill
   ```

## Testing New Skills (MANDATORY)

**Every new skill MUST be tested before declaring it complete.**

### Testing Workflow

1. **After creation**: Immediately run through the skill's primary use case
2. **Verify outputs**: Check that all scripts/commands produce expected results
3. **Test edge cases**: Try error scenarios, missing inputs, etc.
4. **Document test results**: Add test output to skill's README or create a test log

### Examples

**arXiv skill test:**
```bash
cd @@KIKI_SKILLS_DIR@@/arxiv-daily-digest && ./scripts/run_digest.sh
# Verify: papers fetched, filtered, digest generated
```

**AutoDL skill test:**
```bash
python3 @@KIKI_SKILLS_DIR@@/autodl-manager/scripts/autodl_cli.py list
python3 @@KIKI_SKILLS_DIR@@/autodl-manager/scripts/autodl_cli.py status <instance>
# Verify: instances listed, status checked correctly
```

**Coding agent skill test:**
```bash
# Run the agent on a small coding task
# Verify: agent completes task, logs properly, cleanup works
```

### What to Check

- ✅ All commands/scripts execute without errors
- ✅ Output format matches expectations
- ✅ Error handling works (try invalid inputs)
- ✅ Dependencies are properly installed
- ✅ Documentation accurately describes behavior
- ✅ Config files use correct paths
- ✅ Cron jobs (if any) run successfully

### Failed Test Actions

If testing reveals issues:
1. **Fix immediately** - don't declare skill complete
2. **Update documentation** if actual behavior differs
3. **Add error handling** for discovered edge cases
4. **Re-test** after fixes

**Remember**: An untested skill is an incomplete skill.

## Keeping Index Fresh

The skills index should be refreshed when:
- New skills are installed
- User asks about skills and results seem outdated
- Periodically (e.g., monthly)

Simply re-run:
```bash
python3 scripts/index_skills.py
```

## Tips

- **Be specific in searches**: Include key actions/domains (e.g., "edit pdf rotate" vs just "document")
- **Check top 3-5 results**: Sometimes related skills use different terminology
- **Read the actual skill**: If similarity is borderline, read the existing SKILL.md to be sure
- **Suggest extensions**: Often better to add features to existing skill than fragment functionality
- **Always test**: See "Testing New Skills" section - no exceptions!
