#!/usr/bin/env python3
"""
Migrate old flat memory files to new hierarchical structure.

Old: memory/YYYY-MM-DD.md
New: memory/daily/YYYY/MM/YYYY-MM-DD.md
"""

import shutil
from pathlib import Path
import re
from datetime import datetime

def migrate_memories(workspace_root: str):
    """Migrate old memory files to new structure"""
    workspace = Path(workspace_root).expanduser()
    memory_dir = workspace / "memory"
    
    if not memory_dir.exists():
        print("❌ Memory directory not found")
        return
    
    # Find old format files: YYYY-MM-DD.md at root of memory/
    old_files = []
    for file_path in memory_dir.glob("*.md"):
        # Match YYYY-MM-DD.md pattern
        if re.match(r'^\d{4}-\d{2}-\d{2}\.md$', file_path.name):
            old_files.append(file_path)
    
    if not old_files:
        print("✅ No old memory files to migrate")
        return
    
    print(f"Found {len(old_files)} old memory files to migrate:\n")
    
    migrated = 0
    for old_file in sorted(old_files):
        # Parse date from filename
        date_str = old_file.stem  # YYYY-MM-DD
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            print(f"⚠️  Skipping invalid date: {old_file.name}")
            continue
        
        # New path: memory/daily/YYYY/MM/YYYY-MM-DD.md
        year_dir = memory_dir / "daily" / str(date.year)
        month_dir = year_dir / f"{date.month:02d}"
        month_dir.mkdir(parents=True, exist_ok=True)
        
        new_file = month_dir / old_file.name
        
        # Move file
        if new_file.exists():
            print(f"⚠️  Target exists, skipping: {old_file.name}")
            continue
        
        shutil.move(str(old_file), str(new_file))
        print(f"✓ Migrated: {old_file.name} → {new_file.relative_to(workspace)}")
        migrated += 1
    
    print(f"\n✅ Migrated {migrated} files")

if __name__ == "__main__":
    import sys
    workspace = sys.argv[1] if len(sys.argv) > 1 else "."
    migrate_memories(workspace)
