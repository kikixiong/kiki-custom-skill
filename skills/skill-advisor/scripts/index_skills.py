#!/usr/bin/env python3
"""
Index all available skills by reading their SKILL.md frontmatter.
Outputs a JSON file with skill metadata for quick searching.
"""

import os
import json
import yaml
import re
from pathlib import Path
from typing import List, Dict, Optional

def find_skill_files(base_path: str) -> List[Path]:
    """Find all SKILL.md files in the given directory tree."""
    skill_files = []
    base = Path(base_path).expanduser()
    
    for skill_md in base.rglob("SKILL.md"):
        skill_files.append(skill_md)
    
    return skill_files

def extract_frontmatter(skill_path: Path) -> Optional[Dict]:
    """Extract YAML frontmatter from SKILL.md."""
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match YAML frontmatter between --- markers
        match = re.match(r'^---\s*\n(.*?\n)---\s*\n', content, re.DOTALL)
        if not match:
            return None
        
        frontmatter = yaml.safe_load(match.group(1))
        
        # Add file path for reference
        frontmatter['_path'] = str(skill_path)
        frontmatter['_dir'] = str(skill_path.parent)
        
        return frontmatter
    except Exception as e:
        print(f"Error reading {skill_path}: {e}")
        return None

def default_skill_roots() -> List[Path]:
    """Return Codex skill roots that commonly exist on this machine."""
    return [Path("@@KIKI_SKILLS_DIR@@")]



def index_skills(skill_roots: List[Path]) -> Dict:
    """Index all skills in the provided Codex skill roots."""
    skill_files = []
    for root in skill_roots:
        skill_files.extend(find_skill_files(str(root)))
    
    skills = []
    for skill_file in skill_files:
        metadata = extract_frontmatter(skill_file)
        if metadata and 'name' in metadata:
            skills.append(metadata)
    
    # Sort by name
    skills.sort(key=lambda x: x.get('name', ''))
    
    return {
        'total': len(skills),
        'roots': [str(root) for root in skill_roots],
        'skills': skills
    }

def main():
    if len(os.sys.argv) > 1:
        roots = [Path(arg).expanduser() for arg in os.sys.argv[1:]]
        roots = [root for root in roots if root.exists()]
    else:
        roots = default_skill_roots()

    if not roots:
        print("Error: no Codex skill roots found")
        return 1

    print("Indexing skills from:")
    for root in roots:
        print(f"  - {root}")
    index = index_skills(roots)
    
    # Save to references directory
    output_dir = Path(__file__).parent.parent / "references"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "skills_index.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Indexed {index['total']} skills")
    print(f"📄 Saved to: {output_file}")
    
    return 0

if __name__ == "__main__":
    exit(main())
