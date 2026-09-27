#!/usr/bin/env python3
"""Validate the portable structure of an ElegantPaper report project."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
from pathlib import Path


MARKER_PATTERN = re.compile(r"@@[^@\r\n]+@@")
DOCUMENTCLASS_PATTERN = re.compile(
    r"^\s*\\documentclass(?:\[[^]]*\])?\{elegantpaper\}\s*(?:%.*)?$",
    re.MULTILINE,
)
REQUIRED_FILES = (
    "main.tex",
    "references.bib",
    "elegantpaper.cls",
    "latexmkrc",
    ".vscode/settings.json",
    "upstream/ElegantPaper-v0.12/License",
    "upstream/ElegantPaper-v0.12/elegantpaper.cls",
)
REQUIRED_DIRECTORIES = (
    "figures",
    "upstream/ElegantPaper-v0.12",
)
UPSTREAM_SHA256 = {
    ".gitignore": "9418471bdd439c3052ec9596753b43a1f4f6d4562c171069f10ceda3d5b68286",
    "License": "5f05fcf6ef25a6c31bccd2df7c0c46b23107bbeb2ce5cdba74efb5cc357f4dbb",
    "README.md": "58aa89440e6fc19e0a8e77c75a8c7c9caeea95f25573a06cd777a74e00dde6d5",
    "elegantpaper-cn.tex": "d794b5e1754a3215eb02d41b9324d70a6280a23b82b04fd02c49a4f759241337",
    "elegantpaper-en.tex": "a969f9991f5888b0c17775750c28c338a1d5ceefcea0aaaa727391e9229cf6ea",
    "elegantpaper.cls": "29370455a0cdf0af94039a6483ba1433f5b067666771b0f96c4cca0159830173",
    "image/founder.png": "57d2f4fc3176f0cfd85e7da2b6ab93943c23c6ee7c523d3d06250d1dbbdcc52a",
    "reference.bib": "0581994f7803ddd05eb73178d0a1a04b4a4205e4902978c4cad0fde4069d5e63",
}


class ValidationResult:
    def __init__(self, errors: list[str]) -> None:
        self.errors = errors

    @property
    def ok(self) -> bool:
        return not self.errors


def _find_markers(project: Path) -> list[str]:
    errors: list[str] = []
    for path in sorted(project.rglob("*.tex")):
        if not path.is_file():
            continue
        for marker in sorted(set(MARKER_PATTERN.findall(path.read_text(encoding="utf-8")))):
            errors.append(f"unresolved marker {marker} in {path.relative_to(project)}")
    return errors


def _find_symlinks(project: Path) -> list[str]:
    """Inventory symlinks without following them into external content."""
    errors: list[str] = []
    for root, directories, files in os.walk(project, topdown=True, followlinks=False):
        directories.sort()
        files.sort()
        root_path = Path(root)
        for name in directories + files:
            path = root_path / name
            if path.is_symlink():
                errors.append(f"symlink not allowed: {path.relative_to(project)}")
        directories[:] = [
            name for name in directories if not (root_path / name).is_symlink()
        ]
    return errors


def _validate_upstream_snapshot(project: Path) -> list[str]:
    """Require the exact eight-file ElegantPaper v0.12 snapshot."""
    errors: list[str] = []
    root = project / "upstream" / "ElegantPaper-v0.12"
    if not root.is_dir():
        return errors

    actual_paths = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }
    expected_paths = set(UPSTREAM_SHA256)
    for relative_path in sorted(expected_paths - actual_paths):
        errors.append(f"upstream file missing: {relative_path}")
    for relative_path in sorted(actual_paths - expected_paths):
        errors.append(f"unexpected upstream file: {relative_path}")
    for relative_path in sorted(actual_paths & expected_paths):
        digest = hashlib.sha256((root / relative_path).read_bytes()).hexdigest()
        if digest != UPSTREAM_SHA256[relative_path]:
            errors.append(f"upstream hash mismatch: {relative_path}")
    return errors


def validate_project(project: Path, require_pdf: bool = False) -> ValidationResult:
    """Return structural validation errors for ``project`` without compiling it."""
    project = Path(project)
    if project.is_symlink():
        return ValidationResult([f"project directory must not be a symlink: {project}"])
    if not project.is_dir():
        return ValidationResult([f"project directory not found: {project}"])

    errors = _find_symlinks(project)
    if errors:
        return ValidationResult(errors)

    errors = _find_markers(project)
    errors.extend(_validate_upstream_snapshot(project))

    for required in REQUIRED_FILES:
        if not (project / required).is_file():
            errors.append(f"required file missing: {required}")

    for required in REQUIRED_DIRECTORIES:
        if not (project / required).is_dir():
            errors.append(f"required directory missing: {required}")

    main_tex = project / "main.tex"
    if main_tex.is_file() and not DOCUMENTCLASS_PATTERN.search(
        main_tex.read_text(encoding="utf-8")
    ):
        errors.append("main.tex does not use the elegantpaper document class")

    root_class = project / "elegantpaper.cls"
    upstream_class = project / "upstream" / "ElegantPaper-v0.12" / "elegantpaper.cls"
    if (
        root_class.is_file()
        and upstream_class.is_file()
        and root_class.read_bytes() != upstream_class.read_bytes()
    ):
        errors.append(
            "elegantpaper.cls differs from "
            "upstream/ElegantPaper-v0.12/elegantpaper.cls"
        )

    if require_pdf and not (project / "main.pdf").is_file():
        errors.append("required PDF missing: main.pdf")
    return ValidationResult(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an ElegantPaper report project.")
    parser.add_argument("project", type=Path, metavar="PROJECT")
    parser.add_argument("--require-pdf", action="store_true")
    args = parser.parse_args()
    result = validate_project(args.project, require_pdf=args.require_pdf)
    if result.ok:
        print("[OK] ElegantPaper project is structurally valid")
        return 0
    for error in result.errors:
        print(f"[ERROR] {error}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
