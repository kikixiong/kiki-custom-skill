#!/usr/bin/env python3
"""Local CLI for browsing the AcademicForge skill corpus."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_ROOTS = [
    Path('@@KIKI_SUPPORT_DIR@@/academicforge'),
    Path.home() / "tools" / "AcademicForge",
]

GENERIC_UPSTREAM_TOOLS = {"Read", "Write", "Edit", "Bash", "Grep", "Glob"}

DEFAULT_INSTALL_ROOT = Path("@@KIKI_SKILLS_DIR@@")
DEFAULT_ACTIVE_ROOT = Path("@@KIKI_SKILLS_DIR@@")

PRESETS: dict[str, dict[str, Any]] = {
    "academic-core": {
        "description": "Safe general academic-writing helpers with no detected upstream tool conflicts.",
        "skills": [
            "scientific-agent-skills/scientific-skills/citation-management",
            "scientific-agent-skills/scientific-skills/venue-templates",
            "scientific-agent-skills/scientific-skills/scientific-critical-thinking",
            "scientific-agent-skills/scientific-skills/markdown-mermaid-writing",
        ],
    },
    "paper-workbench": {
        "description": "Paper drafting and presentation helpers that remain locally inspectable and easy to override.",
        "skills": [
            "scientific-agent-skills/scientific-skills/scientific-writing",
            "scientific-agent-skills/scientific-skills/scientific-slides",
            "scientific-agent-skills/scientific-skills/venue-templates",
            "scientific-agent-skills/scientific-skills/scientific-critical-thinking",
        ],
    },
    "ml-paper-stack": {
        "description": "ML/systems paper helpers sourced from AcademicForge without overlapping existing local Codex skill names.",
        "skills": [
            "AI-research-SKILLs/20-ml-paper-writing/academic-plotting",
            "AI-research-SKILLs/20-ml-paper-writing/presenting-conference-talks",
            "AI-research-SKILLs/20-ml-paper-writing/systems-paper-writing",
            "scientific-agent-skills/scientific-skills/venue-templates",
        ],
    },
    "zh-review-stack": {
        "description": "Chinese writing and review helpers. Includes one wrapper with an upstream AskUserQuestion hint, but the core rewrite and review guidance remains usable in Codex.",
        "skills": [
            "paper-polish-workflow-skill/skills/paper-polish-workflow",
            "scientific-agent-skills/scientific-skills/peer-review",
            "humanizer-zh",
            "scientific-agent-skills/scientific-skills/citation-management",
        ],
    },
    "survey-journal-stack": {
        "description": "Survey-paper stack for ACM Computing Surveys and comparable top journals: literature discovery, survey synthesis, structured evaluation, citations, and venue fit.",
        "skills": [
            "scientific-agent-skills/scientific-skills/literature-review",
            "scientific-agent-skills/scientific-skills/paper-lookup",
            "scientific-agent-skills/scientific-skills/scholar-evaluation",
            "scientific-agent-skills/scientific-skills/citation-management",
            "scientific-agent-skills/scientific-skills/peer-review",
            "scientific-agent-skills/scientific-skills/scientific-writing",
            "scientific-agent-skills/scientific-skills/venue-templates",
        ],
    },
}


MULTILINE_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*([|>][-+]?)\s*$")
SCALAR_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)\s*$")
LIST_RE = re.compile(r"^\s*-\s*(.+?)\s*$")
QUOTE_RE = re.compile(r'^"(.*)"$|^\'(.*)\'$')


@dataclass
class SkillRecord:
    skill_id: str
    name: str
    description: str
    pack: str
    path: Path
    relative_path: str
    allowed_tools: list[str]
    warnings: list[str]
    score: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "pack": self.pack,
            "path": str(self.path),
            "relative_path": self.relative_path,
            "allowed_tools": self.allowed_tools,
            "warnings": self.warnings,
            "score": self.score,
        }


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def print_json(data: Any) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def unquote(value: str) -> str:
    value = value.strip()
    match = QUOTE_RE.match(value)
    if match:
        return next(group for group in match.groups() if group is not None)
    return value


def resolve_root(explicit: str | None) -> Path:
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if not root.exists():
            raise SystemExit(f"AcademicForge root does not exist: {root}")
        return root

    env_root = os.environ.get("ACADEMICFORGE_ROOT")
    if env_root:
        root = Path(env_root).expanduser().resolve()
        if root.exists():
            return root

    for candidate in DEFAULT_ROOTS:
        if candidate.exists():
            return candidate.resolve()

    raise SystemExit(
        "AcademicForge root not found. Set ACADEMICFORGE_ROOT or clone the repo "
        "to @@KIKI_SUPPORT_DIR@@/academicforge."
    )


def frontmatter_block(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    if end == -1:
        return ""
    return text[4:end]


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    if end == -1:
        return text
    remainder = text[end + 4 :]
    return remainder.lstrip("\n")


def parse_frontmatter(text: str) -> dict[str, Any]:
    block = frontmatter_block(text)
    data: dict[str, Any] = {}
    lines = block.splitlines()
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue

        multiline = MULTILINE_RE.match(line)
        if multiline:
            key = multiline.group(1)
            index += 1
            collected: list[str] = []
            while index < len(lines):
                candidate = lines[index]
                if candidate.startswith("  ") or candidate.startswith("\t"):
                    collected.append(candidate[2:] if candidate.startswith("  ") else candidate.lstrip("\t"))
                    index += 1
                    continue
                if not candidate.strip():
                    collected.append("")
                    index += 1
                    continue
                break
            data[key] = "\n".join(collected).strip()
            continue

        scalar = SCALAR_RE.match(line)
        if not scalar:
            index += 1
            continue

        key = scalar.group(1)
        raw_value = scalar.group(2).strip()
        if raw_value:
            data[key] = unquote(raw_value)
            index += 1
            continue

        index += 1
        items: list[str] = []
        while index < len(lines):
            candidate = lines[index]
            list_match = LIST_RE.match(candidate)
            if list_match:
                items.append(unquote(list_match.group(1)))
                index += 1
                continue
            if not candidate.strip():
                index += 1
                continue
            break
        if items:
            data[key] = items

    return data


def detect_warnings(text: str, allowed_tools: list[str]) -> list[str]:
    warnings: set[str] = set()
    if "<HARD-GATE>" in text:
        warnings.add("hard-gate")
    for tool in allowed_tools:
        if tool not in GENERIC_UPSTREAM_TOOLS:
            warnings.add(f"unsupported-tool:{tool}")
    if "Claude Code" in text or "OpenCode" in text:
        warnings.add("other-client-instructions")
    if text.count("MUST") >= 3:
        warnings.add("heavy-global-rules")
    return sorted(warnings)


def normalize_tools(raw_value: Any) -> list[str]:
    if not raw_value:
        return []
    if isinstance(raw_value, list):
        return [str(item).strip() for item in raw_value if str(item).strip()]

    text = str(raw_value).strip()
    if not text:
        return []
    if text.startswith("[") and text.endswith("]"):
        return [item.strip(" '\"") for item in text[1:-1].split(",") if item.strip()]
    if "," in text:
        return [item.strip() for item in text.split(",") if item.strip()]
    if " " in text:
        return [item.strip() for item in text.split() if item.strip()]
    return [text]


def sanitize_name(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9-]+", "-", value.lower())
    cleaned = re.sub(r"-{2,}", "-", cleaned).strip("-")
    return cleaned or "skill"


def wrapper_name_for(record: SkillRecord, requested_name: str | None = None) -> str:
    if requested_name:
        return sanitize_name(requested_name)

    base = sanitize_name(record.name)
    return f"af-{base}"


def resolve_install_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    return DEFAULT_INSTALL_ROOT.resolve()


def resolve_active_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()

    return DEFAULT_ACTIVE_ROOT.resolve()


def remove_path(path: Path) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)


def installed_metadata_path(wrapper_dir: Path) -> Path:
    return wrapper_dir / ".academicforge-install.json"


def load_installed_records(target_root: Path) -> list[dict[str, Any]]:
    if not target_root.exists():
        return []

    rows: list[dict[str, Any]] = []
    for meta_file in sorted(target_root.glob("*/.academicforge-install.json")):
        try:
            payload = json.loads(meta_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        rows.append(payload)
    return rows


def find_installed_by_name(rows: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    for row in rows:
        if row.get("name") == name:
            return row
    return None


def find_installed_by_source(rows: list[dict[str, Any]], source_id: str) -> dict[str, Any] | None:
    for row in rows:
        if row.get("source_id") == source_id:
            return row
    return None


def make_wrapper_skill_text(record: SkillRecord, wrapper_name: str) -> str:
    upstream_body = strip_frontmatter(record.path.read_text(encoding="utf-8", errors="ignore"))
    description = f"AcademicForge native wrapper for upstream skill {record.name}. {record.description}".strip()
    header_lines = [
        "---",
        f"name: {wrapper_name}",
        f"description: {yaml_quote(description)}",
        "---",
        "",
        f"# AcademicForge Wrapper: {record.name}",
        "",
        f"Upstream source: `{record.skill_id}`.",
        "",
        "This wrapper mirrors an AcademicForge skill into the local Codex install.",
        "Apply local system and developer instructions first when upstream guidance conflicts.",
    ]
    if record.warnings:
        header_lines.extend(
            [
                "",
                f"Upstream compatibility notes: {', '.join(record.warnings)}.",
            ]
        )
    header_lines.append("")
    header = "\n".join(
        header_lines
    )
    return header + upstream_body


def install_wrapper(
    record: SkillRecord,
    wrapper_name: str,
    target_root: Path,
    active_root: Path,
    dry_run: bool,
    force: bool,
    installed_rows: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    wrapper_dir = target_root / wrapper_name
    active_link = active_root / wrapper_name
    source_dir = record.path.parent
    installed_rows = installed_rows if installed_rows is not None else load_installed_records(target_root)

    installed_same_name = find_installed_by_name(installed_rows, wrapper_name)
    installed_same_source = find_installed_by_source(installed_rows, record.skill_id)

    if installed_same_name and installed_same_name.get("source_id") == record.skill_id and not force:
        return {
            "name": wrapper_name,
            "source_id": record.skill_id,
            "wrapper_dir": str(wrapper_dir),
            "active_link": str(active_link),
            "dry_run": dry_run,
            "status": "already-installed",
        }

    if installed_same_source and installed_same_source.get("name") != wrapper_name and not force:
        return {
            "name": installed_same_source["name"],
            "source_id": record.skill_id,
            "wrapper_dir": installed_same_source["wrapper_dir"],
            "active_link": installed_same_source["active_link"],
            "dry_run": dry_run,
            "status": "already-installed",
        }

    if dry_run:
        return {
            "name": wrapper_name,
            "source_id": record.skill_id,
            "wrapper_dir": str(wrapper_dir),
            "active_link": str(active_link),
            "dry_run": True,
            "status": "dry-run",
        }

    if wrapper_dir.exists() or wrapper_dir.is_symlink():
        if not force:
            raise SystemExit(f"Install target already exists: {wrapper_dir}")
        remove_path(wrapper_dir)

    if active_link.exists() or active_link.is_symlink():
        if not force:
            raise SystemExit(f"Active skill link already exists: {active_link}")
        remove_path(active_link)

    wrapper_dir.mkdir(parents=True, exist_ok=True)
    active_root.mkdir(parents=True, exist_ok=True)

    for child in source_dir.iterdir():
        if child.name == "SKILL.md":
            continue
        (wrapper_dir / child.name).symlink_to(child)

    (wrapper_dir / "SKILL.md").write_text(
        make_wrapper_skill_text(record, wrapper_name),
        encoding="utf-8",
    )
    installed_metadata_path(wrapper_dir).write_text(
        json.dumps(
            {
                "name": wrapper_name,
                "source_id": record.skill_id,
                "source_name": record.name,
                "source_relative_path": record.relative_path,
                "wrapper_dir": str(wrapper_dir),
                "active_link": str(active_link),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    active_link.symlink_to(wrapper_dir)

    return {
        "name": wrapper_name,
        "source_id": record.skill_id,
        "wrapper_dir": str(wrapper_dir),
        "active_link": str(active_link),
        "dry_run": False,
        "status": "installed",
    }


def uninstall_wrapper(
    name: str,
    target_root: Path,
    active_root: Path,
    dry_run: bool,
) -> dict[str, Any]:
    wrapper_name = sanitize_name(name)
    wrapper_dir = target_root / wrapper_name
    active_link = active_root / wrapper_name

    if not wrapper_dir.exists() and not wrapper_dir.is_symlink():
        raise SystemExit(f"Installed wrapper not found: {wrapper_dir}")

    payload = {
        "name": wrapper_name,
        "wrapper_dir": str(wrapper_dir),
        "active_link": str(active_link),
        "dry_run": dry_run,
    }
    if dry_run:
        return payload

    remove_path(active_link)
    remove_path(wrapper_dir)
    return payload


def resync_wrappers(
    records: list[SkillRecord],
    target_root: Path,
    active_root: Path,
    name: str | None,
    dry_run: bool,
) -> list[dict[str, Any]]:
    installed_rows = load_installed_records(target_root)
    if name:
        requested = sanitize_name(name)
        installed_rows = [row for row in installed_rows if row.get("name") == requested]
        if not installed_rows:
            raise SystemExit(f"Installed wrapper not found: {requested}")

    record_map = {record.skill_id: record for record in records}
    results: list[dict[str, Any]] = []
    for row in installed_rows:
        source_id = row.get("source_id")
        wrapper_name = row.get("name")
        record = record_map.get(source_id)
        if record is None:
            results.append(
                {
                    "name": wrapper_name,
                    "source_id": source_id,
                    "wrapper_dir": row.get("wrapper_dir"),
                    "active_link": row.get("active_link"),
                    "dry_run": dry_run,
                    "status": "missing-source",
                }
            )
            continue
        results.append(
            install_wrapper(
                record=record,
                wrapper_name=wrapper_name,
                target_root=target_root,
                active_root=active_root,
                dry_run=dry_run,
                force=True,
                installed_rows=installed_rows,
            )
        )
    return results


def load_records(root: Path) -> list[SkillRecord]:
    skills_root = root / "skills"
    if not skills_root.exists():
        raise SystemExit(f"AcademicForge skills directory not found: {skills_root}")

    records: list[SkillRecord] = []
    for skill_file in sorted(skills_root.rglob("SKILL.md")):
        text = skill_file.read_text(encoding="utf-8", errors="ignore")
        frontmatter = parse_frontmatter(text)
        rel_dir = skill_file.parent.relative_to(skills_root).as_posix()
        pack = rel_dir.split("/", 1)[0]
        name = str(frontmatter.get("name") or skill_file.parent.name)
        description = str(frontmatter.get("description") or "").replace("\n", " ").strip()
        allowed_tools = normalize_tools(frontmatter.get("allowed-tools") or frontmatter.get("tools"))
        warnings = detect_warnings(text, allowed_tools)
        records.append(
            SkillRecord(
                skill_id=rel_dir,
                name=name,
                description=description,
                pack=pack,
                path=skill_file,
                relative_path=skill_file.relative_to(root).as_posix(),
                allowed_tools=list(allowed_tools),
                warnings=warnings,
            )
        )
    return records


def local_codex_skill_names() -> set[str]:
    code_home = "@@KIKI_AGENT_HOME@@"

    names: set[str] = set()
    skills_root = Path(code_home) / "skills"
    for skill_file in skills_root.glob("*/SKILL.md"):
        text = skill_file.read_text(encoding="utf-8", errors="ignore")
        frontmatter = parse_frontmatter(text)
        names.add(str(frontmatter.get("name") or skill_file.parent.name))
    return names


def git_output(root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""
    return result.stdout.strip()


def build_doctor(root: Path, records: list[SkillRecord]) -> dict[str, Any]:
    duplicate_names: dict[str, int] = {}
    name_counts: dict[str, int] = {}
    for record in records:
        name_counts[record.name] = name_counts.get(record.name, 0) + 1
    for name, count in name_counts.items():
        if count > 1:
            duplicate_names[name] = count

    local_names = local_codex_skill_names()
    overlaps = sorted(local_names.intersection(name_counts))
    warnings: list[str] = []
    if overlaps:
        warnings.append("AcademicForge contains skill names that overlap existing Codex skills.")
    if duplicate_names:
        warnings.append("AcademicForge contains duplicate upstream skill names.")

    packs: dict[str, int] = {}
    for record in records:
        packs[record.pack] = packs.get(record.pack, 0) + 1

    installed = load_installed_records(resolve_install_root(None))

    return {
        "ok": True,
        "root": str(root),
        "packs": packs,
        "skill_count": len(records),
        "installed_wrapper_count": len(installed),
        "warnings": warnings,
        "duplicate_names": duplicate_names,
        "codex_name_overlaps": overlaps,
        "flag_counts": {
            "hard_gate": sum("hard-gate" in record.warnings for record in records),
            "unsupported_tool": sum(
                any(item.startswith("unsupported-tool:") for item in record.warnings)
                for record in records
            ),
            "other_client_instructions": sum(
                "other-client-instructions" in record.warnings for record in records
            ),
            "heavy_global_rules": sum(
                "heavy-global-rules" in record.warnings for record in records
            ),
        },
        "git": {
            "branch": git_output(root, "branch", "--show-current"),
            "head": git_output(root, "rev-parse", "HEAD"),
            "status_short": git_output(root, "status", "--short"),
        },
    }


def score_record(record: SkillRecord, query: str) -> int:
    terms = [term.lower() for term in query.split() if term.strip()]
    if not terms:
        return 0

    haystacks = {
        "id": record.skill_id.lower(),
        "name": record.name.lower(),
        "description": record.description.lower(),
        "pack": record.pack.lower(),
    }
    score = 0
    for term in terms:
        if term in haystacks["name"]:
            score += 8
        if term in haystacks["id"]:
            score += 5
        if term in haystacks["description"]:
            score += 3
        if term in haystacks["pack"]:
            score += 1
    return score


def filter_records(
    records: list[SkillRecord],
    pack: str | None,
    query: str | None,
    warnings_only: bool,
    duplicates_only: bool,
) -> list[SkillRecord]:
    filtered = records
    if pack:
        filtered = [record for record in filtered if record.pack == pack]
    if warnings_only:
        filtered = [record for record in filtered if record.warnings]
    if duplicates_only:
        counts: dict[str, int] = {}
        for record in filtered:
            counts[record.name] = counts.get(record.name, 0) + 1
        filtered = [record for record in filtered if counts[record.name] > 1]
    if query:
        for record in filtered:
            record.score = score_record(record, query)
        filtered = [record for record in filtered if record.score > 0]
        filtered.sort(key=lambda item: (-item.score, item.skill_id))
    return filtered


def record_by_id(records: list[SkillRecord], skill_id: str) -> SkillRecord:
    normalized = skill_id.strip().strip("/")
    for record in records:
        if record.skill_id == normalized:
            return record
    raise SystemExit(f"Skill not found: {skill_id}")


def emit_text_table(records: list[SkillRecord], limit: int) -> None:
    shown = records[:limit]
    for record in shown:
        warning_text = ""
        if record.warnings:
            warning_text = f"  warnings={','.join(record.warnings)}"
        print(f"{record.skill_id}  name={record.name}{warning_text}")
        if record.description:
            print(f"  {record.description}")
        print(f"  path={record.path}")

    if len(records) > limit:
        print(f"... {len(records) - limit} more")


def emit_show_text(record: SkillRecord, preview_lines: int) -> None:
    text = record.path.read_text(encoding="utf-8", errors="ignore").splitlines()
    print(f"id={record.skill_id}")
    print(f"name={record.name}")
    print(f"pack={record.pack}")
    print(f"path={record.path}")
    if record.allowed_tools:
        print(f"allowed_tools={','.join(record.allowed_tools)}")
    if record.warnings:
        print(f"warnings={','.join(record.warnings)}")
    if record.description:
        print(f"description={record.description}")
    print("")
    for line in text[:preview_lines]:
        print(line)


def emit_installed_text(rows: list[dict[str, Any]]) -> None:
    for row in rows:
        print(f"{row['name']}\tsource={row['source_id']}")
        print(f"  wrapper_dir={row['wrapper_dir']}")
        print(f"  active_link={row['active_link']}")
        if "status" in row:
            print(f"  status={row['status']}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="academicforge",
        description="Browse the local AcademicForge skill corpus from Codex.",
    )
    parser.add_argument("--root", help="Override AcademicForge repo root.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Inspect local AcademicForge install health.")
    doctor.set_defaults(action="doctor")

    packs = subparsers.add_parser("packs", help="List available skill packs.")
    packs_sub = packs.add_subparsers(dest="packs_command", required=True)
    packs_list = packs_sub.add_parser("list", help="List skill packs.")
    packs_list.set_defaults(action="packs-list")

    presets = subparsers.add_parser("presets", help="List curated native-install presets.")
    presets_sub = presets.add_subparsers(dest="presets_command", required=True)
    presets_list = presets_sub.add_parser("list", help="List preset names and source skills.")
    presets_list.set_defaults(action="presets-list")

    skills = subparsers.add_parser("skills", help="List or inspect individual skills.")
    skills_sub = skills.add_subparsers(dest="skills_command", required=True)

    skills_list = skills_sub.add_parser("list", help="List skills.")
    skills_list.add_argument("--pack", help="Filter by pack name.")
    skills_list.add_argument("--query", help="Filter by query string.")
    skills_list.add_argument("--limit", type=int, default=20, help="Maximum rows to show.")
    skills_list.add_argument("--warnings-only", action="store_true", help="Only show warned skills.")
    skills_list.add_argument("--duplicates-only", action="store_true", help="Only show duplicate names.")
    skills_list.set_defaults(action="skills-list")

    skills_show = skills_sub.add_parser("show", help="Show metadata and a preview for one skill.")
    skills_show.add_argument("skill_id", help="Skill id from `skills list`.")
    skills_show.add_argument("--preview-lines", type=int, default=40, help="Lines of file preview.")
    skills_show.set_defaults(action="skills-show")

    search = subparsers.add_parser("search", help="Search skills by query.")
    search.add_argument("query", help="Search query.")
    search.add_argument("--pack", help="Filter by pack name.")
    search.add_argument("--limit", type=int, default=20, help="Maximum rows to show.")
    search.set_defaults(action="search")

    install = subparsers.add_parser("install", help="Install native Codex wrappers for selected skills.")
    install_sub = install.add_subparsers(dest="install_command", required=True)

    install_skill = install_sub.add_parser("skill", help="Install one upstream skill as a native wrapper.")
    install_skill.add_argument("skill_id", help="Skill id from `skills list`.")
    install_skill.add_argument("--name", help="Optional wrapper skill name; defaults to af-<upstream-name>.")
    install_skill.add_argument("--target-root", help="Wrapper install root. Defaults to @@KIKI_SKILLS_DIR@@.")
    install_skill.add_argument("--active-root", help="Active Codex skills root. Defaults to $CODEX_HOME/skills.")
    install_skill.add_argument("--force", action="store_true", help="Replace existing wrappers or links.")
    install_skill.add_argument("--dry-run", action="store_true", help="Show actions without writing files.")
    install_skill.set_defaults(action="install-skill")

    install_preset = install_sub.add_parser("preset", help="Install a curated preset of wrappers.")
    install_preset.add_argument("preset", choices=sorted(PRESETS), help="Preset name.")
    install_preset.add_argument("--target-root", help="Wrapper install root. Defaults to @@KIKI_SKILLS_DIR@@.")
    install_preset.add_argument("--active-root", help="Active Codex skills root. Defaults to $CODEX_HOME/skills.")
    install_preset.add_argument("--force", action="store_true", help="Replace existing wrappers or links.")
    install_preset.add_argument("--dry-run", action="store_true", help="Show actions without writing files.")
    install_preset.set_defaults(action="install-preset")

    installed = subparsers.add_parser("installed", help="Inspect installed native wrappers.")
    installed.add_argument("--target-root", help="Wrapper install root. Defaults to @@KIKI_SKILLS_DIR@@.")
    installed_sub = installed.add_subparsers(dest="installed_command", required=True)
    installed_list = installed_sub.add_parser("list", help="List installed wrappers.")
    installed_list.set_defaults(action="installed-list")

    uninstall = subparsers.add_parser("uninstall", help="Remove one installed native wrapper.")
    uninstall.add_argument("name", help="Wrapper skill name, for example af-citation-management.")
    uninstall.add_argument("--target-root", help="Wrapper install root. Defaults to @@KIKI_SKILLS_DIR@@.")
    uninstall.add_argument("--active-root", help="Active Codex skills root. Defaults to $CODEX_HOME/skills.")
    uninstall.add_argument("--dry-run", action="store_true", help="Show actions without deleting files.")
    uninstall.set_defaults(action="uninstall")

    resync = subparsers.add_parser("resync", help="Refresh installed wrappers from the current upstream mirror.")
    resync_sub = resync.add_subparsers(dest="resync_command", required=True)
    resync_installed = resync_sub.add_parser("installed", help="Rebuild installed wrappers in place.")
    resync_installed.add_argument("--name", help="Only resync one installed wrapper name.")
    resync_installed.add_argument("--target-root", help="Wrapper install root. Defaults to @@KIKI_SKILLS_DIR@@.")
    resync_installed.add_argument("--active-root", help="Active Codex skills root. Defaults to $CODEX_HOME/skills.")
    resync_installed.add_argument("--dry-run", action="store_true", help="Show actions without writing files.")
    resync_installed.set_defaults(action="resync-installed")

    upgrade = subparsers.add_parser("upgrade", help="Alias for refreshing installed wrappers after upstream changes.")
    upgrade_sub = upgrade.add_subparsers(dest="upgrade_command", required=True)
    upgrade_installed = upgrade_sub.add_parser("installed", help="Rebuild installed wrappers in place.")
    upgrade_installed.add_argument("--name", help="Only upgrade one installed wrapper name.")
    upgrade_installed.add_argument("--target-root", help="Wrapper install root. Defaults to @@KIKI_SKILLS_DIR@@.")
    upgrade_installed.add_argument("--active-root", help="Active Codex skills root. Defaults to $CODEX_HOME/skills.")
    upgrade_installed.add_argument("--dry-run", action="store_true", help="Show actions without writing files.")
    upgrade_installed.set_defaults(action="upgrade-installed")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    root = resolve_root(args.root)
    records = load_records(root)

    if args.action == "doctor":
        payload = build_doctor(root, records)
        if args.json:
            print_json(payload)
        else:
            print(f"root={payload['root']}")
            print(f"skills={payload['skill_count']}")
            print(f"installed_wrappers={payload['installed_wrapper_count']}")
            print("packs:")
            for pack, count in sorted(payload["packs"].items()):
                print(f"  {pack}: {count}")
            if payload["codex_name_overlaps"]:
                print("codex_name_overlaps:")
                for name in payload["codex_name_overlaps"]:
                    print(f"  {name}")
            if payload["duplicate_names"]:
                print("duplicate_names:")
                for name, count in sorted(payload["duplicate_names"].items()):
                    print(f"  {name}: {count}")
            print("flag_counts:")
            for key, value in payload["flag_counts"].items():
                print(f"  {key}: {value}")
            print("git:")
            print(f"  branch: {payload['git']['branch'] or '(detached)'}")
            print(f"  head: {payload['git']['head']}")
            if payload["warnings"]:
                print("warnings:")
                for warning in payload["warnings"]:
                    print(f"  {warning}")
        return 0

    if args.action == "packs-list":
        packs: dict[str, int] = {}
        for record in records:
            packs[record.pack] = packs.get(record.pack, 0) + 1
        rows = [{"pack": pack, "skill_count": count} for pack, count in sorted(packs.items())]
        if args.json:
            print_json(rows)
        else:
            for row in rows:
                print(f"{row['pack']}\t{row['skill_count']}")
        return 0

    if args.action == "presets-list":
        rows = []
        for preset_name, payload in sorted(PRESETS.items()):
            rows.append(
                {
                    "preset": preset_name,
                    "description": payload["description"],
                    "skills": payload["skills"],
                }
            )
        if args.json:
            print_json(rows)
        else:
            for row in rows:
                print(f"{row['preset']}")
                print(f"  {row['description']}")
                for skill_id in row["skills"]:
                    print(f"  - {skill_id}")
        return 0

    if args.action in {"skills-list", "search"}:
        query = args.query if args.action == "search" else args.query
        filtered = filter_records(
            records,
            pack=getattr(args, "pack", None),
            query=query,
            warnings_only=getattr(args, "warnings_only", False),
            duplicates_only=getattr(args, "duplicates_only", False),
        )
        limit = getattr(args, "limit", 20)
        if args.json:
            print_json([record.to_dict() for record in filtered[:limit]])
        else:
            emit_text_table(filtered, limit)
        return 0

    if args.action == "skills-show":
        record = record_by_id(records, args.skill_id)
        payload = record.to_dict()
        payload["preview"] = record.path.read_text(encoding="utf-8", errors="ignore").splitlines()[
            : args.preview_lines
        ]
        if args.json:
            print_json(payload)
        else:
            emit_show_text(record, args.preview_lines)
        return 0

    if args.action == "install-skill":
        target_root = resolve_install_root(args.target_root)
        active_root = resolve_active_root(args.active_root)
        record = record_by_id(records, args.skill_id)
        installed_rows = load_installed_records(target_root)
        payload = install_wrapper(
            record=record,
            wrapper_name=wrapper_name_for(record, args.name),
            target_root=target_root,
            active_root=active_root,
            dry_run=args.dry_run,
            force=args.force,
            installed_rows=installed_rows,
        )
        if args.json:
            print_json(payload)
        else:
            print(f"{payload['name']}\tsource={payload['source_id']}")
            print(f"  wrapper_dir={payload['wrapper_dir']}")
            print(f"  active_link={payload['active_link']}")
            print(f"  status={payload['status']}")
            if payload["dry_run"]:
                print("  dry_run=true")
        return 0

    if args.action == "install-preset":
        target_root = resolve_install_root(args.target_root)
        active_root = resolve_active_root(args.active_root)
        installed_rows = load_installed_records(target_root)
        results = []
        for skill_id in PRESETS[args.preset]["skills"]:
            record = record_by_id(records, skill_id)
            payload = install_wrapper(
                record=record,
                wrapper_name=wrapper_name_for(record),
                target_root=target_root,
                active_root=active_root,
                dry_run=args.dry_run,
                force=args.force,
                installed_rows=installed_rows,
            )
            results.append(payload)
            if payload["status"] == "installed":
                installed_rows = load_installed_records(target_root)
        payload = {
            "preset": args.preset,
            "description": PRESETS[args.preset]["description"],
            "results": results,
        }
        if args.json:
            print_json(payload)
        else:
            print(args.preset)
            print(f"  {PRESETS[args.preset]['description']}")
            emit_installed_text(results)
        return 0

    if args.action == "installed-list":
        target_root = resolve_install_root(args.target_root)
        rows = load_installed_records(target_root)
        if args.json:
            print_json(rows)
        else:
            emit_installed_text(rows)
        return 0

    if args.action == "uninstall":
        target_root = resolve_install_root(args.target_root)
        active_root = resolve_active_root(args.active_root)
        payload = uninstall_wrapper(args.name, target_root, active_root, args.dry_run)
        if args.json:
            print_json(payload)
        else:
            print(f"{payload['name']}")
            print(f"  wrapper_dir={payload['wrapper_dir']}")
            print(f"  active_link={payload['active_link']}")
            if payload["dry_run"]:
                print("  dry_run=true")
        return 0

    if args.action in {"resync-installed", "upgrade-installed"}:
        target_root = resolve_install_root(args.target_root)
        active_root = resolve_active_root(args.active_root)
        results = resync_wrappers(
            records=records,
            target_root=target_root,
            active_root=active_root,
            name=args.name,
            dry_run=args.dry_run,
        )
        payload = {
            "results": results,
            "dry_run": args.dry_run,
        }
        if args.json:
            print_json(payload)
        else:
            emit_installed_text(results)
            if args.dry_run:
                print("dry_run=true")
        return 0

    parser.error("Unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
