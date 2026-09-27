#!/usr/bin/env python3
"""Validate that the kiki-paper-writing Skill can be distributed alone."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".txt", ".tex", ".py"}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PLACEHOLDER_RE = re.compile(r"\bTODO\b|REPLACE_ME|\[TODO\]", re.IGNORECASE)
ABSOLUTE_PATH_RE = re.compile(
    r"(?:file://|[A-Za-z]:[\\/]|\\\\[^\\\s]+\\[^\\\s]+|"
    r"(?<![A-Za-z0-9_])/(?:home|Users|workspace|mnt|tmp)/)"
)


def inside_root(path: Path) -> bool:
    try:
        return os.path.commonpath([str(ROOT), str(path)]) == str(ROOT)
    except ValueError:
        return False


def parse_frontmatter(text: str) -> set[str]:
    if not text.startswith("---\n"):
        return set()
    end = text.find("\n---\n", 4)
    if end < 0:
        return set()
    keys: set[str] = set()
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):", line)
        if match:
            keys.add(match.group(1))
    return keys


def main() -> int:
    errors: list[str] = []
    if not SKILL.is_file():
        errors.append("Missing SKILL.md")
    else:
        skill_text = SKILL.read_text(encoding="utf-8")
        keys = parse_frontmatter(skill_text)
        if keys != {"name", "description"}:
            errors.append(
                f"SKILL.md frontmatter keys must be name and description; got {keys}"
            )
        if len(skill_text.splitlines()) >= 500:
            errors.append("SKILL.md must remain under 500 lines")

    for path in sorted(ROOT.rglob("*")):
        if path.is_symlink():
            target = path.resolve()
            if not inside_root(target):
                errors.append(f"Symlink escapes Skill root: {path.relative_to(ROOT)}")
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue

        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.name != "validate_self_contained.py" and PLACEHOLDER_RE.search(text):
            errors.append(f"Placeholder marker in {rel}")

        if path.name != "validate_self_contained.py":
            for match in ABSOLUTE_PATH_RE.finditer(text):
                errors.append(f"Absolute external path in {rel}: {match.group(0)}")

        if path.suffix.lower() != ".md":
            continue
        for raw_link in LINK_RE.findall(text):
            link = raw_link.strip().split("#", 1)[0]
            if not link:
                continue
            if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", link):
                errors.append(f"External URI in {rel}: {raw_link}")
                continue
            target = (path.parent / link).resolve()
            if not inside_root(target):
                errors.append(f"Link escapes Skill root in {rel}: {raw_link}")
            elif not target.exists():
                errors.append(f"Broken local link in {rel}: {raw_link}")

    if errors:
        print("SELF_CONTAINMENT_FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    file_count = sum(1 for path in ROOT.rglob("*") if path.is_file())
    print(
        "SELF_CONTAINMENT_PASS "
        f"root={ROOT} files={file_count} external_links=0 path_escapes=0"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
