---
name: memory-manager
description: Manage hierarchical memory system with daily entries, weekly/monthly compaction, and long-term knowledge base. Use when creating daily logs, reviewing/summarizing past memories, maintaining MEMORY.md, searching memory, or organizing the memory directory structure.
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Memory Manager

Hierarchical memory management system for agent continuity across sessions.

## Memory Hierarchy

```
workspace/
├── MEMORY.md                            # Long-term memory (curated knowledge)
└── memory/
    ├── daily/                           # Short-term daily logs
    │   └── YYYY/
    │       └── MM/
    │           └── YYYY-MM-DD.md
    ├── weekly/                          # Weekly summaries
    │   └── YYYY/
    │       └── week-NN.md
    └── monthly/                         # Monthly summaries
        └── YYYY/
            └── YYYY-MM.md
```

### Memory Types

| Type | Location | Retention | Purpose |
|------|----------|-----------|---------|
| **Daily** | `memory/daily/YYYY/MM/` | Raw logs, never delete | Journal-style entries |
| **Weekly** | `memory/weekly/YYYY/` | Keep all | Compact 7 days → key events |
| **Monthly** | `memory/monthly/YYYY/` | Keep all | Compact 4-5 weeks → themes |
| **Long-term** | `MEMORY.md` | Permanent, curated | Distilled knowledge/habits |

## Core Operations

### 1. Create Daily Entry

```bash
python3 scripts/memory_manager.py daily --date today
```

**Creates:**
- File: `memory/daily/2026/03/2026-03-18.md`
- Template with sections: Events, Decisions, Learnings, TODOs

**Auto-trigger:**
- First interaction each day
- After significant events
- Before session ends

### 2. Compact to Weekly

```bash
python3 scripts/memory_manager.py compact --scope week --date 2026-03-17
```

**Process:**
1. Read 7 daily entries (Mon-Sun)
2. Extract key events, decisions, learnings
3. Remove repetitive details
4. Save to `memory/weekly/2026/week-11.md`

**Keep:**
- Important events
- Major decisions
- Significant learnings
- Open TODOs

**Discard:**
- Routine tasks
- Duplicate info
- Low-impact details

### 3. Compact to Monthly

```bash
python3 scripts/memory_manager.py compact --scope month --date 2026-03
```

**Process:**
1. Read 4-5 weekly summaries
2. Identify themes and patterns
3. Track progress on goals/projects
4. Save to `memory/monthly/2026/2026-03.md`

**Focus on:**
- Project milestones
- Recurring patterns
- Habit changes
- Knowledge growth

### 4. Update Long-term Memory

```bash
python3 scripts/memory_manager.py update-longterm --source recent
```

**Process:**
1. Review recent daily/weekly entries
2. Identify:
   - New knowledge worth keeping
   - User habits/preferences
   - Lessons learned
   - Project context
3. Update `MEMORY.md` sections

**MEMORY.md Structure:**
```markdown
# MEMORY.md - Long-Term Memory

## User Profile
- Name, preferences, timezone
- Communication style
- Work habits

## Knowledge Base
- Technical learnings
- Domain expertise
- Tools and workflows

## Projects
- Active projects
- Key decisions
- Status updates

## Habits & Patterns
- Daily routines
- Recurring tasks
- Preferred approaches

## Lessons Learned
- Mistakes to avoid
- What works well
- Best practices
```

### 5. Search Memory

```bash
python3 scripts/memory_manager.py search "topic or keyword"
```

**Searches:**
- Daily entries (last 90 days)
- All weekly/monthly summaries
- MEMORY.md

**Returns:**
- Matching snippets with dates
- File paths for context

### 6. Memory Stats

```bash
python3 scripts/memory_manager.py stats
```

**Shows:**
- Daily entries count (total, this week, this month)
- Weekly summaries count
- Monthly summaries count
- MEMORY.md size
- Last update timestamps

## Workflow Integration

### Daily Routine

**Morning (first session):**
```
1. Check if today's daily entry exists
2. If not, create with template
3. Review yesterday's entry briefly
```

**Evening (heartbeat or explicit):**
```
1. Update today's daily entry with:
   - What happened
   - What was learned
   - Open TODOs
2. Save and commit
```

### Weekly Compact (Sunday night or Monday morning)

```
1. Run: compact --scope week
2. Review generated summary
3. Optionally edit for clarity
4. Commit weekly summary
```

### Monthly Compact (End of month)

```
1. Run: compact --scope month
2. Review month themes
3. Update project status
4. Commit monthly summary
```

### Long-term Update (Monthly or as-needed)

```
1. Run: update-longterm --source recent
2. Script suggests updates to MEMORY.md
3. Review and approve changes
4. Commit updated MEMORY.md
```

## File Templates

### Daily Entry Template

```markdown
# YYYY-MM-DD (Weekday)

## 🌅 Morning Context
- Goals for today:
- Carry-over from yesterday:

## 📝 Events
- [Time] Event description

## 💡 Learnings
- What I learned today

## 🎯 Decisions
- Important decisions made

## 📋 TODOs
- [ ] Task description

## 🤔 Notes
- Miscellaneous observations
```

### Weekly Summary Template

```markdown
# Week NN, YYYY (MM-DD to MM-DD)

## 🎯 Key Events
- Major events this week

## 🚀 Progress
- Project updates
- Milestones reached

## 💡 Learnings
- Key takeaways

## 🔄 Recurring Patterns
- Habits observed

## 📋 Open Items
- TODOs carried forward
```

### Monthly Summary Template

```markdown
# YYYY-MM (Month Name)

## 🏆 Achievements
- Major milestones

## 📊 Project Status
- Project A: status
- Project B: status

## 🌱 Growth
- Skills learned
- Knowledge gained

## 🔁 Habits
- New habits formed
- Changes in routines

## 🎯 Next Month
- Goals and focus areas
```

## Best Practices

### What to Log in Daily Entries

**DO log:**
- Significant conversations
- Decisions made and rationale
- Problems solved and how
- New learnings
- Failed attempts (to avoid repetition)
- User feedback/preferences

**DON'T log:**
- Routine heartbeat checks (unless something found)
- Simple command executions
- Obvious/trivial actions
- Redundant information

### When to Compact

**Weekly:**
- Sunday night or Monday morning
- After completing major project phases
- When daily entries accumulate (>10)

**Monthly:**
- Last day or first day of month
- After quarterly reviews
- When starting new initiatives

### MEMORY.md Maintenance

**Update when:**
- Learning significant new knowledge
- User habits/preferences change
- Project status changes substantially
- Major milestones reached

**Keep it:**
- Concise (aim for <10k words)
- Organized by sections
- Actionable (facts, not fluff)
- Up-to-date (remove outdated info)

## Command Reference

```bash
# Daily operations
python3 scripts/memory_manager.py daily --date today
python3 scripts/memory_manager.py daily --date 2026-03-15

# Compaction
python3 scripts/memory_manager.py compact --scope week --date 2026-03-17
python3 scripts/memory_manager.py compact --scope month --date 2026-03

# Long-term memory
python3 scripts/memory_manager.py update-longterm --source recent
python3 scripts/memory_manager.py update-longterm --source all --since 2026-02-01

# Search
python3 scripts/memory_manager.py search "query"
python3 scripts/memory_manager.py search "project name" --since 2026-03-01

# Utilities
python3 scripts/memory_manager.py stats
python3 scripts/memory_manager.py verify  # Check directory structure
python3 scripts/memory_manager.py init    # Initialize memory structure
```

## Integration with AGENTS.md

The memory system supports the AGENTS.md workflow:

**From AGENTS.md:**
> Every Session:
> 1. Read `SOUL.md` — this is who you are
> 2. Read `USER.md` — this is who you're helping
> 3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
> 4. **If in MAIN SESSION**: Also read `MEMORY.md`

**Memory Manager ensures:**
- Today's daily entry exists
- Yesterday's entry is available
- MEMORY.md is kept up-to-date
- Old daily entries are summarized (not deleted)

## Tips

- **Daily entries are permanent** - They're the raw truth, never delete
- **Weekly/monthly are summaries** - Lossy compression, keep high-signal
- **MEMORY.md is curated** - Quality over quantity, update deliberately
- **Use git commits** - Each compact or long-term update should be a commit
- **Review before compacting** - Scripts suggest, you decide what to keep
