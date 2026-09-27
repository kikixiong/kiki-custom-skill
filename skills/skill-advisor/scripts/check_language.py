#!/usr/bin/env python3
"""
Check if skill contains only English content (no Chinese or other non-English text).
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple

def contains_non_english(text: str) -> List[Tuple[int, str]]:
    """
    Check if text contains non-English characters.
    Returns list of (line_number, line_content) with non-English text.
    
    ALLOWS non-English in:
    - Code blocks
    - Table cells (examples)
    - Lines with quotes (example inputs)
    - Lines with arrows (transformations)
    """
    issues = []
    in_code_block = False
    
    for i, line in enumerate(text.split('\n'), 1):
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        
        # Skip code blocks and URLs
        if in_code_block or line.strip().startswith('http'):
            continue
        
        # Allow non-English in specific contexts:
        # 1. Table cells (usually examples)
        if '|' in line:
            continue
        # 2. Lines with quotes (example inputs)
        if '"' in line or "'" in line:
            continue
        # 3. Lines with transformation arrows (A → B patterns)
        if '→' in line or '->' in line:
            continue
        
        # Check for Chinese characters (most common non-English in our context)
        if re.search(r'[\u4e00-\u9fff]', line):
            issues.append((i, line.strip()[:80]))  # First 80 chars
        
        # Check for other non-ASCII that's likely not English
        # Allow common symbols: ✓ ✅ ❌ → etc. (these are OK for documentation)
        cleaned = re.sub(r'[✓✅❌🎯📝💡🚀🔧📊🎉⚠️🆕→←↓↑⭐️]', '', line)
        
        # Check for non-ASCII letters (excluding allowed symbols)
        if re.search(r'[^\x00-\x7F]', cleaned):
            # But allow if it's just punctuation or already flagged
            if not re.search(r'[a-zA-Z]', cleaned):
                continue
            if (i, line.strip()[:80]) not in issues:
                # Check if it's actually problematic
                if re.search(r'[\u0080-\u024F\u0400-\u04FF\u0600-\u06FF\u3000-\u303F\uFF00-\uFFEF]', cleaned):
                    issues.append((i, line.strip()[:80]))
    
    return issues

def check_skill_language(skill_path: Path) -> Tuple[bool, List[str]]:
    """
    Check all files in skill directory for non-English content.
    Returns (is_english_only, list_of_issues)
    """
    issues = []
    
    if not skill_path.exists():
        return False, [f"Skill path not found: {skill_path}"]
    
    # Check all markdown files
    for md_file in skill_path.rglob("*.md"):
        # Skip certain files that might legitimately have examples
        if "example" in md_file.name.lower() or "test" in md_file.name.lower():
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
        except Exception as e:
            issues.append(f"❌ {md_file.name}: Failed to read - {e}")
            continue
        
        non_english = contains_non_english(content)
        
        if non_english:
            issues.append(f"\n📄 {md_file.relative_to(skill_path)}:")
            for line_num, line_text in non_english[:5]:  # Show max 5 examples
                issues.append(f"   Line {line_num}: {line_text}")
            if len(non_english) > 5:
                issues.append(f"   ... and {len(non_english) - 5} more")
    
    return len(issues) == 0, issues

def main():
    if len(sys.argv) < 2:
        print("Usage: check_language.py <skill-directory>")
        print("Example: check_language.py @@KIKI_SKILLS_DIR@@/memory-manager")
        return 1
    
    skill_path = Path(sys.argv[1]).expanduser()
    
    print(f"🔍 Checking language in: {skill_path.name}\n")
    
    is_english, issues = check_skill_language(skill_path)
    
    if is_english:
        print("✅ All content is in English")
        return 0
    else:
        print("❌ Found non-English content:\n")
        for issue in issues:
            print(issue)
        print("\n💡 Tip: Skills should use English only for compatibility and clarity.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
