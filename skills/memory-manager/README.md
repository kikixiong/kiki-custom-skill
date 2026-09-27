# Memory Manager

Hierarchical memory management system with daily entries, weekly/monthly summaries, and long-term knowledge base.

## Features

### Memory Hierarchy

```
workspace/
├── MEMORY.md                    # Long-term memory (curated knowledge)
└── memory/
    ├── daily/                   # Short-term daily logs
    │   └── YYYY/MM/YYYY-MM-DD.md
    ├── weekly/                  # Weekly summaries
    │   └── YYYY/week-NN.md
    └── monthly/                 # Monthly summaries
        └── YYYY/YYYY-MM.md
```

### Core Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| **Initialize** | `init` | Create directory structure |
| **Daily Entry** | `daily --date today` | Create today's entry |
| **Weekly Summary** | `compact --scope week --date YYYY-MM-DD` | Compress 7 days into 1 week |
| **Monthly Summary** | `compact --scope month --date YYYY-MM` | Compress 4-5 weeks into 1 month |
| **Search** | `search "query"` | Search all memory levels |
| **Statistics** | `stats` | Show memory statistics |

## Quick Start

### 1. Initialize Memory Structure

```bash
cd the current project root
python3 memory-manager/scripts/memory_manager.py init
```

**Creates:**
- `memory/daily/` - Daily entries directory
- `memory/weekly/` - Weekly summaries directory
- `memory/monthly/` - Monthly summaries directory
- `MEMORY.md` - Long-term memory template

### 2. Create Today's Entry

```bash
python3 memory-manager/scripts/memory_manager.py daily --date today
```

**Creates:**
- `memory/daily/2026/03/2026-03-18.md`
- With template: Events, Learnings, Decisions, TODOs, Notes

### 3. View Statistics

```bash
python3 memory-manager/scripts/memory_manager.py stats
```

**Shows:**
- Daily entries count
- Weekly/monthly summaries count
- MEMORY.md size
- Last update timestamps

## Daily Usage

### Morning (Session Start)

```bash
# Auto-create today's entry if missing
python3 memory-manager/scripts/memory_manager.py daily --date today

# Read yesterday's entry (for context)
cat memory/daily/2026/03/2026-03-17.md

# Main session: also read MEMORY.md
cat MEMORY.md
```

### During Day (Record Events)

**Edit today's entry manually:**
```bash
vim memory/daily/2026/03/2026-03-18.md
```

**What to record:**
- Events - Important events
- Learnings - Things learned
- Decisions - Important decisions made
- TODOs - Tasks to do
- Notes - Other observations

### Evening (Commit)

```bash
cd the current project root
git add memory/daily/2026/03/2026-03-18.md
git commit -m "Daily entry: 2026-03-18"
```

### Sunday (Weekly Compact)

```bash
# Compress past 7 days into weekly summary
python3 memory-manager/scripts/memory_manager.py compact --scope week --date 2026-03-17

# Review and edit if needed
vim memory/weekly/2026/week-11.md

# Commit
git add memory/weekly/
git commit -m "Weekly summary: Week 11, 2026"
```

### Month-End (Monthly Compact)

```bash
# Compress weekly summaries into monthly summary
python3 memory-manager/scripts/memory_manager.py compact --scope month --date 2026-03

# Review and add insights
vim memory/monthly/2026/2026-03.md

# Update long-term memory
vim MEMORY.md  # Extract important knowledge/habits

# Commit
git add memory/monthly/ MEMORY.md
git commit -m "Monthly summary + long-term update: March 2026"
```

## Search Memory

```bash
# Search specific topic
python3 memory-manager/scripts/memory_manager.py search "temporal conformal"

# Search project name
python3 memory-manager/scripts/memory_manager.py search "scbenchmark"

# Search user info
python3 memory-manager/scripts/memory_manager.py search "Jiaqi"
```

**Result format:**
```
File: memory/daily/2026/03/2026-03-15.md (daily)
  42: - Completed temporal conformal UQ experiments
  78: - User feedback: prefers Telegram over WhatsApp

File: MEMORY.md (longterm)
  156: ## Temporal Conformal UQ
```

## File Templates

### Daily Entry

```markdown
# 2026-03-18 (Wednesday)

## Morning Context
- Goals for today: Create memory-manager skill
- Carry-over from yesterday: Complete prompt-clarifier

## Events
- 14:30 - Created memory-manager skill
- 15:00 - Tested initialization and daily entry creation

## Learnings
- Hierarchical memory system is clearer than single MEMORY.md
- Weekly/monthly compact prevents information overload

## Decisions
- Use YYYY/MM directory structure (organized by year and month)
- Keep daily entries permanently (never delete - raw truth)

## TODOs
- [ ] Clean up workspace directory structure
- [ ] Test weekly compact functionality

## Notes
- User prefers short-term/long-term memory separation
- Need periodic MEMORY.md maintenance
```

### Weekly Summary

```markdown
# Week 11, 2026 (03-11 to 03-17)

## Key Events
- Created prompt-clarifier skill (v2 with typo handling)
- Created skill-advisor skill (indexes 56 skills)
- Created memory-manager skill

## Learnings
- Typo handling requires pinyin recognition + fuzzy matching
- Skill design should follow progressive disclosure principle

## Decisions
- Use hierarchical memory instead of single MEMORY.md

## Open TODOs
- [ ] Clean up workspace directory
- [ ] Test weekly compact
```

### Monthly Summary

```markdown
# 2026-03 (March)

## Key Achievements
- Created 3 important skills (skill-advisor, prompt-clarifier, memory-manager)
- Enhanced typo handling capability
- Built complete memory management system

## Project Updates
- Skills ecosystem: expanded from 56 to 59
- Memory system: upgraded from single file to hierarchical structure

## Growth & Learning
- Learned progressive disclosure design pattern
- Mastered fuzzy matching algorithms
- Understood challenges in agent memory management

## Habits & Patterns
- Create daily entry every day
- Weekly compact on Sunday
- Update MEMORY.md at month-end

## Next Month Focus
- Clean up workspace directory structure
- Test all skills in actual work
- Optimize memory search functionality
```

## Advanced Features

### Automatic Maintenance

```bash
# Run auto-keeper during heartbeat
python3 memory-manager/scripts/auto_memory_keeper.py

# Silent mode (for automated runs)
python3 memory-manager/scripts/auto_memory_keeper.py --silent
```

**What it does:**
- Creates today's daily entry if missing
- Auto-compacts to weekly on Sundays
- Auto-compacts to monthly on last day of month
- Reminds to update MEMORY.md

### Heartbeat Integration

Add to `HEARTBEAT.md`:

```markdown
# Daily check (run once per day)
- Ensure today's daily entry exists

# Sunday 23:00
- Run weekly compact

# Last day of month 23:00
- Run monthly compact
- Remind to update MEMORY.md
```

### Automation Scripts

**Auto-commit daily entries (cron):**
```bash
# Every day at 23:00
0 23 * * * cd the current project root && git add memory/daily && git commit -m "Daily: $(date +\%Y-\%m-\%d)" && git push
```

**Weekly compact (cron):**
```bash
# Every Sunday at 23:30
30 23 * * 0 cd the current project root && python3 memory-manager/scripts/memory_manager.py compact --scope week --date $(date +\%Y-\%m-\%d) && git add memory/weekly && git commit -m "Week: $(date +\%W, \%Y)" && git push
```

## Documentation

- **[SKILL.md](SKILL.md)** - Complete skill definition
- **[references/workflow-integration.md](references/workflow-integration.md)** - Workflow integration guide

## Best Practices

### File Size Control

| Type | Target Size | Max | Reason |
|------|-------------|-----|--------|
| Daily | 1-3 KB | 10 KB | Keep concise |
| Weekly | 2-5 KB | 15 KB | Lossy compression |
| Monthly | 5-10 KB | 30 KB | Keep only themes |
| MEMORY.md | 5-10 KB | 20 KB | Curated knowledge |

### What to Record

**DO record:**
- Important conversations
- Decisions and rationale
- Problems solved
- New knowledge learned
- Failed attempts (to avoid repetition)
- User feedback/preferences

**DON'T record:**
- Routine heartbeat checks
- Simple command executions
- Obvious operations
- Duplicate information

### Compact Timing

**Weekly:**
- Sunday night or Monday morning
- When daily entries accumulate (>10)

**Monthly:**
- Month-end or start of new month
- After quarterly reviews

**Long-term (MEMORY.md):**
- When learning important knowledge
- When user habits/preferences change
- When project status changes substantially
- At least monthly review

## Ready to Use

1. Initialized memory structure
2. Created today's daily entry
3. Stats showing normal operation

**Start recording your memories!**
