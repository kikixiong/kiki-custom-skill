#!/usr/bin/env python3
"""
Memory Manager - Hierarchical memory system for agent continuity
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import argparse
from typing import List, Dict, Optional
import re

class MemoryManager:
    def __init__(self, workspace_root: Optional[str] = None):
        if workspace_root:
            self.workspace = Path(workspace_root).expanduser()
        else:
            self.workspace = Path.cwd()
        
        self.memory_root = self.workspace / "memory"
        self.memory_md = self.workspace / "MEMORY.md"
    
    def init_structure(self):
        """Initialize memory directory structure"""
        dirs = [
            self.memory_root / "daily",
            self.memory_root / "weekly",
            self.memory_root / "monthly"
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✓ Created: {dir_path.relative_to(self.workspace)}")
        
        if not self.memory_md.exists():
            self._create_longterm_template()
            print(f"✓ Created: MEMORY.md template")
        
        print("\n✅ Memory structure initialized")
    
    def _create_longterm_template(self):
        """Create MEMORY.md template"""
        template = """# MEMORY.md — Long-Term Memory

## User Profile
- Name: 
- Timezone: 
- Communication preferences: 

## Knowledge Base
### Technical
- 

### Domain Expertise
- 

### Tools & Workflows
- 

## Active Projects
### Project Name
- Status: 
- Key decisions: 
- Next steps: 

## Habits & Patterns
### Daily Routines
- 

### Work Style
- 

### Preferences
- 

## Lessons Learned
### What Works
- 

### Mistakes to Avoid
- 

### Best Practices
- 

---
*Last updated: {date}*
""".format(date=datetime.now().strftime("%Y-%m-%d"))
        
        self.memory_md.write_text(template)
    
    def create_daily_entry(self, date_str: str = "today") -> Path:
        """Create daily entry for specified date"""
        if date_str == "today":
            target_date = datetime.now()
        else:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Path: memory/daily/YYYY/MM/YYYY-MM-DD.md
        year_dir = self.memory_root / "daily" / str(target_date.year)
        month_dir = year_dir / f"{target_date.month:02d}"
        month_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = month_dir / f"{target_date.strftime('%Y-%m-%d')}.md"
        
        if file_path.exists():
            print(f"ℹ️  Daily entry already exists: {file_path.relative_to(self.workspace)}")
            return file_path
        
        # Create from template
        weekday = target_date.strftime("%A")
        template = f"""# {target_date.strftime('%Y-%m-%d')} ({weekday})

## 🌅 Morning Context
- Goals for today:
- Carry-over from yesterday:

## 📝 Events

## 💡 Learnings

## 🎯 Decisions

## 📋 TODOs
- [ ] 

## 🤔 Notes

---
*Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        
        file_path.write_text(template)
        print(f"✅ Created daily entry: {file_path.relative_to(self.workspace)}")
        return file_path
    
    def compact_weekly(self, end_date_str: str) -> Path:
        """Compact 7 days into weekly summary"""
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        start_date = end_date - timedelta(days=6)
        
        # ISO week number
        week_num = end_date.isocalendar()[1]
        
        # Collect daily entries
        daily_entries = []
        current = start_date
        while current <= end_date:
            entry_path = self._get_daily_path(current)
            if entry_path.exists():
                daily_entries.append({
                    'date': current,
                    'path': entry_path,
                    'content': entry_path.read_text()
                })
            current += timedelta(days=1)
        
        if not daily_entries:
            print(f"⚠️  No daily entries found for week {week_num}")
            return None
        
        # Create weekly summary
        year_dir = self.memory_root / "weekly" / str(end_date.year)
        year_dir.mkdir(parents=True, exist_ok=True)
        
        weekly_path = year_dir / f"week-{week_num:02d}.md"
        
        summary = self._generate_weekly_summary(daily_entries, week_num, start_date, end_date)
        weekly_path.write_text(summary)
        
        print(f"✅ Created weekly summary: {weekly_path.relative_to(self.workspace)}")
        print(f"   Compacted {len(daily_entries)} daily entries")
        return weekly_path
    
    def compact_monthly(self, month_str: str) -> Path:
        """Compact 4-5 weeks into monthly summary"""
        month_date = datetime.strptime(month_str, "%Y-%m")
        
        # Find weekly summaries for this month
        year_dir = self.memory_root / "weekly" / str(month_date.year)
        if not year_dir.exists():
            print(f"⚠️  No weekly summaries found for {month_str}")
            return None
        
        # Collect weekly summaries
        weekly_entries = []
        for week_file in sorted(year_dir.glob("week-*.md")):
            content = week_file.read_text()
            # Extract date range from content
            weekly_entries.append({
                'file': week_file.name,
                'content': content
            })
        
        if not weekly_entries:
            print(f"⚠️  No weekly summaries to compact for {month_str}")
            return None
        
        # Create monthly summary
        month_dir = self.memory_root / "monthly" / str(month_date.year)
        month_dir.mkdir(parents=True, exist_ok=True)
        
        monthly_path = month_dir / f"{month_str}.md"
        
        summary = self._generate_monthly_summary(weekly_entries, month_date)
        monthly_path.write_text(summary)
        
        print(f"✅ Created monthly summary: {monthly_path.relative_to(self.workspace)}")
        print(f"   Compacted {len(weekly_entries)} weekly summaries")
        return monthly_path
    
    def _get_daily_path(self, date: datetime) -> Path:
        """Get path for daily entry"""
        return (self.memory_root / "daily" / str(date.year) / 
                f"{date.month:02d}" / f"{date.strftime('%Y-%m-%d')}.md")
    
    def _generate_weekly_summary(self, entries: List[Dict], week_num: int, 
                                 start_date: datetime, end_date: datetime) -> str:
        """Generate weekly summary from daily entries"""
        # Extract sections from daily entries
        events = []
        learnings = []
        decisions = []
        todos = []
        
        for entry in entries:
            content = entry['content']
            date_str = entry['date'].strftime('%Y-%m-%d')
            
            # Extract each section
            events.extend(self._extract_section(content, "Events", date_str))
            learnings.extend(self._extract_section(content, "Learnings", date_str))
            decisions.extend(self._extract_section(content, "Decisions", date_str))
            todos.extend(self._extract_section(content, "TODOs", date_str))
        
        # Build summary
        summary = f"""# Week {week_num:02d}, {start_date.year} ({start_date.strftime('%m-%d')} to {end_date.strftime('%m-%d')})

## 🎯 Key Events
{self._format_items(events) if events else "- No significant events recorded"}

## 💡 Learnings
{self._format_items(learnings) if learnings else "- No learnings recorded"}

## 🎯 Decisions
{self._format_items(decisions) if decisions else "- No decisions recorded"}

## 📋 Open TODOs
{self._format_items(todos) if todos else "- No open TODOs"}

---
*Compacted from {len(entries)} daily entries on {datetime.now().strftime('%Y-%m-%d')}*
"""
        return summary
    
    def _generate_monthly_summary(self, weekly_entries: List[Dict], 
                                  month_date: datetime) -> str:
        """Generate monthly summary from weekly entries"""
        month_name = month_date.strftime("%B")
        
        # Combine all weekly content
        all_content = "\n\n".join([e['content'] for e in weekly_entries])
        
        summary = f"""# {month_date.strftime('%Y-%m')} ({month_name})

## 🏆 Key Achievements
- *Review weekly summaries and extract major milestones*

## 📊 Project Updates
- *Summarize project progress*

## 🌱 Growth & Learning
- *What was learned this month*

## 🔁 Patterns & Habits
- *Recurring themes or habit changes*

## 🎯 Next Month Focus
- *Goals and priorities*

---
## Weekly Summaries

{all_content}

---
*Compacted from {len(weekly_entries)} weekly summaries on {datetime.now().strftime('%Y-%m-%d')}*
"""
        return summary
    
    def _extract_section(self, content: str, section_name: str, date_str: str) -> List[str]:
        """Extract items from a section"""
        pattern = rf"## [^\n]*{section_name}[^\n]*\n(.*?)(?=\n## |\n---|\Z)"
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            return []
        
        section_content = match.group(1).strip()
        if not section_content or section_content == "-":
            return []
        
        # Extract bullet points or paragraphs
        items = []
        for line in section_content.split('\n'):
            line = line.strip()
            if line and not line.startswith('*'):
                # Add date prefix
                if not line.startswith('-'):
                    line = f"- {line}"
                items.append(f"{line} ({date_str})")
        
        return items
    
    def _format_items(self, items: List[str]) -> str:
        """Format list of items"""
        return '\n'.join(items) if items else "- None"
    
    def search_memory(self, query: str, since: Optional[str] = None) -> List[Dict]:
        """Search all memory files"""
        results = []
        
        # Search daily entries
        daily_dir = self.memory_root / "daily"
        if daily_dir.exists():
            for file_path in daily_dir.rglob("*.md"):
                content = file_path.read_text()
                if query.lower() in content.lower():
                    # Find matching lines
                    lines = content.split('\n')
                    matches = [f"  {i+1}: {line}" for i, line in enumerate(lines) 
                              if query.lower() in line.lower()]
                    results.append({
                        'file': str(file_path.relative_to(self.workspace)),
                        'type': 'daily',
                        'matches': matches[:3]  # Top 3 matches
                    })
        
        # Search weekly/monthly summaries
        for summary_type in ['weekly', 'monthly']:
            summary_dir = self.memory_root / summary_type
            if summary_dir.exists():
                for file_path in summary_dir.rglob("*.md"):
                    content = file_path.read_text()
                    if query.lower() in content.lower():
                        lines = content.split('\n')
                        matches = [f"  {i+1}: {line}" for i, line in enumerate(lines) 
                                  if query.lower() in line.lower()]
                        results.append({
                            'file': str(file_path.relative_to(self.workspace)),
                            'type': summary_type,
                            'matches': matches[:3]
                        })
        
        # Search MEMORY.md
        if self.memory_md.exists():
            content = self.memory_md.read_text()
            if query.lower() in content.lower():
                lines = content.split('\n')
                matches = [f"  {i+1}: {line}" for i, line in enumerate(lines) 
                          if query.lower() in line.lower()]
                results.append({
                    'file': 'MEMORY.md',
                    'type': 'longterm',
                    'matches': matches[:5]  # Top 5 for long-term
                })
        
        return results
    
    def stats(self) -> Dict:
        """Get memory statistics"""
        stats = {
            'daily_entries': 0,
            'weekly_summaries': 0,
            'monthly_summaries': 0,
            'memory_md_size': 0,
            'last_daily_entry': None,
            'last_weekly_summary': None,
            'last_monthly_summary': None
        }
        
        # Count daily entries
        daily_dir = self.memory_root / "daily"
        if daily_dir.exists():
            daily_files = list(daily_dir.rglob("*.md"))
            stats['daily_entries'] = len(daily_files)
            if daily_files:
                latest = max(daily_files, key=lambda p: p.stat().st_mtime)
                stats['last_daily_entry'] = latest.stem
        
        # Count weekly summaries
        weekly_dir = self.memory_root / "weekly"
        if weekly_dir.exists():
            weekly_files = list(weekly_dir.rglob("*.md"))
            stats['weekly_summaries'] = len(weekly_files)
            if weekly_files:
                latest = max(weekly_files, key=lambda p: p.stat().st_mtime)
                stats['last_weekly_summary'] = latest.stem
        
        # Count monthly summaries
        monthly_dir = self.memory_root / "monthly"
        if monthly_dir.exists():
            monthly_files = list(monthly_dir.rglob("*.md"))
            stats['monthly_summaries'] = len(monthly_files)
            if monthly_files:
                latest = max(monthly_files, key=lambda p: p.stat().st_mtime)
                stats['last_monthly_summary'] = latest.stem
        
        # MEMORY.md size
        if self.memory_md.exists():
            stats['memory_md_size'] = self.memory_md.stat().st_size
        
        return stats

def main():
    parser = argparse.ArgumentParser(description="Memory Manager CLI")
    parser.add_argument(
        "--workspace",
        default=None,
        help="Workspace root for MEMORY.md and memory/ (defaults to current directory)",
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Init
    subparsers.add_parser('init', help='Initialize memory structure')
    
    # Daily
    daily_parser = subparsers.add_parser('daily', help='Create daily entry')
    daily_parser.add_argument('--date', default='today', help='Date (YYYY-MM-DD or "today")')
    
    # Compact
    compact_parser = subparsers.add_parser('compact', help='Compact memories')
    compact_parser.add_argument('--scope', choices=['week', 'month'], required=True)
    compact_parser.add_argument('--date', required=True, help='End date for week (YYYY-MM-DD) or month (YYYY-MM)')
    
    # Search
    search_parser = subparsers.add_parser('search', help='Search memories')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--since', help='Only search from this date (YYYY-MM-DD)')
    
    # Stats
    subparsers.add_parser('stats', help='Show memory statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    mm = MemoryManager(args.workspace)
    
    if args.command == 'init':
        mm.init_structure()
    
    elif args.command == 'daily':
        mm.create_daily_entry(args.date)
    
    elif args.command == 'compact':
        if args.scope == 'week':
            mm.compact_weekly(args.date)
        else:
            mm.compact_monthly(args.date)
    
    elif args.command == 'search':
        results = mm.search_memory(args.query, args.since)
        if results:
            print(f"\n🔍 Found {len(results)} files matching '{args.query}':\n")
            for r in results:
                print(f"📄 {r['file']} ({r['type']})")
                for match in r['matches']:
                    print(match)
                print()
        else:
            print(f"❌ No results found for '{args.query}'")
    
    elif args.command == 'stats':
        stats = mm.stats()
        print("\n📊 Memory Statistics\n")
        print(f"Daily entries:      {stats['daily_entries']}")
        print(f"Weekly summaries:   {stats['weekly_summaries']}")
        print(f"Monthly summaries:  {stats['monthly_summaries']}")
        print(f"MEMORY.md size:     {stats['memory_md_size']} bytes")
        print()
        if stats['last_daily_entry']:
            print(f"Last daily entry:   {stats['last_daily_entry']}")
        if stats['last_weekly_summary']:
            print(f"Last weekly:        {stats['last_weekly_summary']}")
        if stats['last_monthly_summary']:
            print(f"Last monthly:       {stats['last_monthly_summary']}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
