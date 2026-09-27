#!/usr/bin/env python3
"""Create a fresh, pinned ElegantPaper report project."""

from __future__ import annotations

import argparse
import re
import shutil
from datetime import date
from pathlib import Path


VALID_LANGUAGES = {"zh", "en"}
VALID_REPORT_TYPES = {"general", "progress", "experiment"}
CHINESE_REPORT_TYPES = {
    "general": "通用报告",
    "progress": "进度报告",
    "experiment": "实验报告",
}
TEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "#": r"\#",
    "$": r"\$",
    "%": r"\%",
    "&": r"\&",
    "~": r"\textasciitilde{}",
    "_": r"\_",
    "^": r"\textasciicircum{}",
    "{": r"\{",
    "}": r"\}",
}

RENDER_MARKER = re.compile(
    r"@@(?:TITLE|AUTHOR|REPORT_TYPE|DATE|SUMMARY|KEYWORDS|CONTEXT|METHOD|"
    r"RESULTS|INTERPRETATION|LIMITATIONS|NEXT_STEPS|APPENDIX)@@"
)
RESERVED_MARKER = re.compile(r"@@[^@\r\n]+@@")

SKILL_ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_SOURCE = SKILL_ROOT / "assets" / "upstream" / "ElegantPaper-v0.12"
PROJECT_ASSETS = SKILL_ROOT / "assets" / "report-project"


def _validate_options(language: str, report_type: str) -> None:
    if language not in VALID_LANGUAGES:
        raise ValueError(f"language must be one of {sorted(VALID_LANGUAGES)}")
    if report_type not in VALID_REPORT_TYPES:
        raise ValueError(f"report_type must be one of {sorted(VALID_REPORT_TYPES)}")


def _validate_metadata(title: str, author: str) -> None:
    for field, value in (("title", title), ("author", author)):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
        if any(ord(character) < 32 or ord(character) == 127 for character in value):
            raise ValueError(f"{field} must not contain control characters")
        if RESERVED_MARKER.search(value):
            raise ValueError(f"{field} must not contain reserved @@...@@ markers")


def _safe_output_path(output: Path) -> Path:
    resolved_output = output.expanduser().resolve()
    resolved_skill_root = SKILL_ROOT.resolve()
    if (
        resolved_output == resolved_skill_root
        or resolved_skill_root in resolved_output.parents
        or resolved_output in resolved_skill_root.parents
    ):
        raise ValueError(
            f"output must be outside the skill source directory: {resolved_output}"
        )
    return resolved_output


def _ensure_empty_target(output: Path) -> None:
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise FileExistsError(f"refusing to overwrite non-empty target: {output}")


def _escape_tex_plain_text(value: str) -> str:
    """Escape TeX-special characters in CLI metadata treated as plain text."""
    return "".join(TEX_ESCAPES.get(character, character) for character in value)


def _display_report_type(language: str, report_type: str) -> str:
    if language == "zh":
        return CHINESE_REPORT_TYPES[report_type]
    return report_type


def _render_metadata(
    template: str, *, language: str, title: str, author: str, report_type: str
) -> str:
    metadata = {
        "@@TITLE@@": _escape_tex_plain_text(title),
        "@@AUTHOR@@": _escape_tex_plain_text(author),
        "@@REPORT_TYPE@@": _display_report_type(language, report_type),
        "@@DATE@@": date.today().isoformat(),
    }
    unavailable = {
        "en": {
            "@@SUMMARY@@": "Unavailable: no summary was supplied.",
            "@@KEYWORDS@@": "report",
            "@@CONTEXT@@": "Unavailable: no context or objective was supplied.",
            "@@METHOD@@": "Unavailable: no work or method was supplied.",
            "@@RESULTS@@": "Unavailable: no measured results were supplied.",
            "@@INTERPRETATION@@": "Unavailable: no interpretation was supplied.",
            "@@LIMITATIONS@@": "Unavailable: no limitations or risks were supplied.",
            "@@NEXT_STEPS@@": "Planned: provide verified next steps before delivery.",
            "@@APPENDIX@@": "No appendix was supplied.",
        },
        "zh": {
            "@@SUMMARY@@": "未提供：未提供摘要。",
            "@@KEYWORDS@@": "报告",
            "@@CONTEXT@@": "未提供：未提供背景或目标。",
            "@@METHOD@@": "未提供：未提供工作或方法。",
            "@@RESULTS@@": "未提供：未提供测量结果。",
            "@@INTERPRETATION@@": "未提供：未提供解释。",
            "@@LIMITATIONS@@": "未提供：未提供局限或风险。",
            "@@NEXT_STEPS@@": "计划：交付前提供经核实的下一步。",
            "@@APPENDIX@@": "未提供附录。",
        },
    }
    metadata.update(unavailable[language])
    return RENDER_MARKER.sub(lambda match: metadata[match.group(0)], template)


def build_project(
    output: Path,
    language: str,
    title: str,
    author: str,
    report_type: str = "general",
) -> Path:
    """Create a fresh pinned ElegantPaper project and return its path."""
    _validate_options(language, report_type)
    _validate_metadata(title, author)
    output = _safe_output_path(Path(output))
    _ensure_empty_target(output)

    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(UPSTREAM_SOURCE, output / "upstream" / "ElegantPaper-v0.12", dirs_exist_ok=True)
    shutil.copy2(UPSTREAM_SOURCE / "elegantpaper.cls", output / "elegantpaper.cls")
    shutil.copy2(PROJECT_ASSETS / "references.bib", output / "references.bib")
    shutil.copy2(PROJECT_ASSETS / "latexmkrc", output / "latexmkrc")

    vscode_directory = output / ".vscode"
    vscode_directory.mkdir(exist_ok=True)
    shutil.copy2(PROJECT_ASSETS / "vscode-settings.json", vscode_directory / "settings.json")
    (output / "figures").mkdir(exist_ok=True)

    template = (PROJECT_ASSETS / f"main-{language}.tex").read_text(encoding="utf-8")
    (output / "main.tex").write_text(
        _render_metadata(
            template,
            language=language,
            title=title,
            author=author,
            report_type=report_type,
        ),
        encoding="utf-8",
    )
    return output


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a pinned ElegantPaper report project.")
    parser.add_argument("output", type=Path, metavar="OUTPUT")
    parser.add_argument("--language", required=True, choices=sorted(VALID_LANGUAGES))
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", required=True)
    parser.add_argument("--report-type", default="general", choices=sorted(VALID_REPORT_TYPES))
    return parser


def main() -> None:
    args = _parser().parse_args()
    try:
        project = build_project(
            args.output,
            args.language,
            args.title,
            args.author,
            args.report_type,
        )
    except (FileExistsError, ValueError) as error:
        _parser().error(str(error))
    print(project)


if __name__ == "__main__":
    main()
