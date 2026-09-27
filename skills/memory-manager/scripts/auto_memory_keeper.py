#!/usr/bin/env python3
"""
Auto Memory Keeper - Automatically maintain memory hierarchy

This script should be called during heartbeat checks or session start.
It automatically:
1. Creates daily entry if missing
2. Compacts to weekly on Sundays
3. Compacts to monthly on month-end
4. Suggests MEMORY.md updates
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from memory_manager import MemoryManager

def should_compact_weekly(mm: MemoryManager) -> bool:
    """Check if weekly compaction is needed (Sunday)"""
    today = datetime.now()
    
    # Only on Sunday
    if today.weekday() != 6:
        return False
    
    # Check if this week already compacted
    week_num = today.isocalendar()[1]
    year_dir = mm.memory_root / "weekly" / str(today.year)
    weekly_file = year_dir / f"week-{week_num:02d}.md"
    
    # If already exists, check if it's recent (within last 2 days)
    if weekly_file.exists():
        mtime = datetime.fromtimestamp(weekly_file.stat().st_mtime)
        age_days = (today - mtime).days
        if age_days < 2:
            return False  # Already compacted recently
    
    return True

def should_compact_monthly(mm: MemoryManager) -> bool:
    """Check if monthly compaction is needed (last day of month)"""
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    
    # Last day of month: tomorrow is a different month
    if today.month != tomorrow.month:
        month_str = today.strftime("%Y-%m")
        month_dir = mm.memory_root / "monthly" / str(today.year)
        monthly_file = month_dir / f"{month_str}.md"
        
        # If already exists, check if it's recent (within last 7 days)
        if monthly_file.exists():
            mtime = datetime.fromtimestamp(monthly_file.stat().st_mtime)
            age_days = (today - mtime).days
            if age_days < 7:
                return False
        
        return True
    
    return False

def auto_maintain():
    """Automatically maintain memory hierarchy"""
    mm = MemoryManager()
    today = datetime.now()
    actions = []
    
    # 1. Ensure today's daily entry exists
    try:
        # Create returns path; capture but don't print in auto mode
        import io
        import contextlib
        
        # Suppress "already exists" message
        with contextlib.redirect_stdout(io.StringIO()):
            entry_path = mm.create_daily_entry("today")
        actions.append(f"Daily entry: {entry_path.name}")
    except Exception as e:
        print(f"[ERROR] Failed to create daily entry: {e}", file=sys.stderr)
    
    # 2. Weekly compaction (Sunday)
    if should_compact_weekly(mm):
        try:
            weekly_path = mm.compact_weekly(today.strftime("%Y-%m-%d"))
            if weekly_path:
                actions.append(f"Weekly compact: {weekly_path.name}")
                print(f"\n✅ Weekly summary created: {weekly_path.relative_to(mm.workspace)}")
                print("   Review and commit when ready.")
        except Exception as e:
            print(f"[ERROR] Weekly compaction failed: {e}", file=sys.stderr)
    
    # 3. Monthly compaction (last day of month)
    if should_compact_monthly(mm):
        try:
            monthly_path = mm.compact_monthly(today.strftime("%Y-%m"))
            if monthly_path:
                actions.append(f"Monthly compact: {monthly_path.name}")
                print(f"\n✅ Monthly summary created: {monthly_path.relative_to(mm.workspace)}")
                print("   Review and update MEMORY.md with key learnings.")
        except Exception as e:
            print(f"[ERROR] Monthly compaction failed: {e}", file=sys.stderr)
    
    # 4. Remind about MEMORY.md update (monthly)
    if should_compact_monthly(mm):
        print(f"\n💡 Reminder: Update MEMORY.md with learnings from {today.strftime('%B %Y')}")
    
    # Return status for silent mode
    if len(actions) == 1 and actions[0].startswith("Daily entry"):
        # Only created daily entry, normal routine
        return 0
    elif actions:
        # Did something notable
        return 1
    
    return 0

def main():
    """Entry point"""
    # Check if running in silent mode
    silent = "--silent" in sys.argv
    
    if not silent:
        print("🧠 Auto Memory Keeper")
        print("=" * 40)
    
    exit_code = auto_maintain()
    
    if not silent and exit_code == 0:
        print("\n✅ Memory maintenance complete")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())
