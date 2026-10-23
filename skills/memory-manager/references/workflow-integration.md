# Workflow Integration Guide

How to integrate Memory Manager into daily agent operations.

## Daily Workflow

### Morning (Session Start)

**Check for today's entry:**
```python
mm = MemoryManager()
today_entry = mm.create_daily_entry("today")
```

**Read recent context:**
```python
# Read today's entry (if exists)
# Read yesterday's entry
# In main session: also read MEMORY.md
```

### During Session

**Log significant events:**
- After completing tasks
- After making decisions
- After learning something new
- After user feedback

**Update daily entry:**
```bash
# Manually append to today's entry
echo "## 15:30 - Completed X project" >> memory/daily/2026/03/2026-03-18.md
```

### Evening (Before Session End)

**Review and finalize today's entry:**
1. Check all sections are filled
2. Capture open TODOs
3. Note anything to remember

**Commit to git:**
```bash
cd the current project root
git add memory/daily/2026/03/2026-03-18.md
git commit -m "Daily entry: 2026-03-18"
```

## Weekly Workflow

### Sunday Night or Monday Morning

**Compact last week:**
```bash
# If today is Monday 2026-03-17
python3 scripts/memory_manager.py compact --scope week --date 2026-03-17
```

**Review generated summary:**
1. Read `memory/weekly/2026/week-11.md`
2. Edit if needed (add missing context, remove noise)
3. Commit:
   ```bash
   git add memory/weekly/
   git commit -m "Weekly summary: Week 11, 2026"
   ```

## Monthly Workflow

### End of Month

**Compact last month:**
```bash
python3 scripts/memory_manager.py compact --scope month --date 2026-03
```

**Review monthly summary:**
1. Read `memory/monthly/2026/2026-03.md`
2. Add high-level insights
3. Identify patterns/themes
4. Commit:
   ```bash
   git add memory/monthly/
   git commit -m "Monthly summary: March 2026"
   ```

**Update long-term memory:**
1. Read monthly summary
2. Identify knowledge/habits worth keeping
3. Update `MEMORY.md` sections:
   - User preferences
   - Project status
   - Lessons learned
   - Habits formed
4. Commit:
   ```bash
   git add MEMORY.md
   git commit -m "Update long-term memory: March 2026"
   ```

## Heartbeat Integration

### In HEARTBEAT.md

```markdown
# Heartbeat Tasks

## Daily (Run once per day)
- Create today's daily entry if not exists
- Review yesterday's entry

## Weekly (Sunday 23:00)
- Compact last week's daily entries
- Review and commit weekly summary

## Monthly (Last day of month, 23:00)
- Compact last month's weekly summaries
- Update MEMORY.md with key learnings
- Commit monthly summary
```

### Heartbeat Implementation

```python
# In heartbeat handler
from datetime import datetime

today = datetime.now()

# Daily check
if not daily_entry_exists(today):
    create_daily_entry(today)

# Weekly check (Sunday)
if today.weekday() == 6:  # Sunday
    compact_weekly(today)

# Monthly check (last day of month)
if is_last_day_of_month(today):
    compact_monthly(today)
    suggest_memory_md_updates()
```

## Search Usage

### When to Search

**Before answering questions about:**
- Past decisions
- Previous work on similar topics
- User preferences
- Historical context

**How to search:**
```bash
# Search for specific topic
python3 scripts/memory_manager.py search "temporal conformal"

# Search for project
python3 scripts/memory_manager.py search "example-project"

# Search for person/tool
python3 scripts/memory_manager.py search "example-user"
```

### Search Results Interpretation

```
📄 memory/daily/2026/03/2026-03-15.md (daily)
  42: - Completed temporal conformal UQ experiments
  78: - User feedback: prefers Telegram over WhatsApp

📄 MEMORY.md (longterm)
  156: ## Temporal Conformal UQ (2026-02)
  157: - Fixed split validation completed
```

**What to do:**
- Read the relevant sections
- Cite sources in your response ("According to memory/daily/2026-03-15...")
- Update if needed

## Maintenance Tasks

### Weekly

- **Review daily entries** for completeness
- **Compact to weekly** summary
- **Check for gaps** in logging

### Monthly

- **Review weekly summaries**
- **Compact to monthly** summary
- **Update MEMORY.md**
- **Archive old logs** (optional, if disk space is concern)

### Quarterly (Every 3 months)

- **Review MEMORY.md** for outdated info
- **Reorganize sections** if needed
- **Prune old/irrelevant** long-term memories
- **Back up memory directory**

## File Size Guidelines

### Daily Entries
- **Target**: 1-3 KB per day
- **Max**: 10 KB (if very eventful day)
- **Tip**: Be concise, focus on high-signal events

### Weekly Summaries
- **Target**: 2-5 KB per week
- **Max**: 15 KB
- **Tip**: Lossy compression, keep only key events

### Monthly Summaries
- **Target**: 5-10 KB per month
- **Max**: 30 KB
- **Tip**: High-level themes, major milestones only

### MEMORY.md
- **Target**: 5-10 KB
- **Max**: 20 KB
- **Tip**: Curated knowledge, remove outdated info

**Why these limits?**
- Keep context window efficient
- Force prioritization of important info
- Make searches faster

## Automation Scripts

### Auto-commit daily entries

```bash
#!/bin/bash
# project scripts/auto-commit-daily.sh

cd the current project root
git add memory/daily/$(date +%Y/%m)/$(date +%Y-%m-%d).md
git commit -m "Daily entry: $(date +%Y-%m-%d)" || true
git push origin main || true
```

**Run via cron:**
```bash
# Every day at 23:00
0 23 * * * project scripts/auto-commit-daily.sh
```

### Weekly compact script

```bash
#!/bin/bash
# project scripts/weekly-compact.sh

cd the current project root
python3 memory-manager/scripts/memory_manager.py compact --scope week --date $(date +%Y-%m-%d)
git add memory/weekly/
git commit -m "Weekly summary: Week $(date +%W), $(date +%Y)"
git push origin main || true
```

**Run via cron:**
```bash
# Every Sunday at 23:30
30 23 * * 0 project scripts/weekly-compact.sh
```

## Tips

### What Makes a Good Daily Entry

**Good:**
```markdown
## 📝 Events
- 14:30 - Deployed example-project to AutoDL server
  - Used port <SSH_PORT>, <GPU_DESCRIPTION>
  - Training started successfully

## 💡 Learnings
- AutoDL network acceleration: source /etc/network_turbo before downloads
- Significantly improves git clone / pip install speed

## 🎯 Decisions
- Decided to use Sonnet 4.5 for routine tasks, Opus for complex debugging
- Rationale: Cost efficiency while maintaining quality
```

**Bad (too vague):**
```markdown
## 📝 Events
- Worked on project

## 💡 Learnings
- Learned something

## 🎯 Decisions
- Made some decisions
```

### What Makes a Good Weekly Summary

**Good:**
- Identifies 3-5 key events
- Connects related events
- Highlights progress on goals
- Notes recurring patterns

**Bad:**
- Just lists all events (no compression)
- No context or connections
- Misses important themes

### What to Keep in MEMORY.md

**Keep:**
- User preferences that affect decisions
- Project context needed across sessions
- Hard-won lessons (mistakes to avoid)
- Established workflows/best practices
- Infrastructure details (servers, keys, etc.)

**Don't keep:**
- Obvious/common knowledge
- Temporary project status (use daily/weekly instead)
- Redundant information
- Outdated context
