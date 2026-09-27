---
name: creating-elegantpaper-reports
description: Use when a user requests a human-readable Chinese or English report, midterm or progress report, experiment report, mentor or lab update, Overleaf-ready LaTeX source, printable PDF, or a decision between transient Markdown notes and a formal ElegantPaper deliverable.
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Creating ElegantPaper Reports

Create a complete, self-contained ElegantPaper v0.12 project from finished, evidence-calibrated report content. A successful deliverable has no template markers; it has a verified PDF only when the local TeX tools actually produced and checked one.

Route by audience and lifecycle:

| Observable request | Deliverable |
| --- | --- |
| Transient agent/self working record, run log, handoff, scratch analysis, or internal draft with no human review | Markdown |
| Human review, a formal report, mentor/adviser/lab/committee audience, or explicit ElegantPaper, LaTeX, Overleaf, or PDF request; including a human-facing draft | ElegantPaper v0.12 project |
| Mixed lifecycle: working notes plus a formal deliverable | Keep Markdown notes; create a separate ElegantPaper v0.12 project from verified content |

The word “draft” is not decisive: an internal draft is Markdown; a human-facing or formal draft is ElegantPaper.

Read `references/report-contract.md` before creating a project. Use `kiki-paper-writing` for scientific-paper claim review; this skill owns TeX packaging, not research-content synthesis. Do not upload, push, synchronize, or overwrite an existing project without explicit authorization.

## Workflow

**Write boundary:** Use the explicit user-approved `OUTPUT` as the artifact write sandbox. Do not deliberately create or modify installers, executable wrappers, symlinks, `PATH`, shell profiles, editor/tool configuration, helper files, or dependency caches outside `OUTPUT`. Dependency discovery is read-only and uses the current `PATH`; if a required command is absent, stop compilation and report it. Do not claim whole-filesystem immutability: an already-installed compiler may manage font or package caches outside `OUTPUT`. If such writes are known or observed, disclose them; if strict containment is required and the compiler cannot honor it, deliver source only.

Before and after work, record the status of these high-risk paths: `@@KIKI_TEXBIN@@/{latexmk,xelatex,biber}`, `~/.local/bin/latexmk`, `~/.local/bin/biber`, `~/.zshrc`, `~/.bashrc`, `~/.profile`, and any additional installer, wrapper, symlink, profile, configuration, helper, or cache path actually considered or touched. Report `absent`, `present and unchanged`, or the exact authorized/observed change. This audit does not authorize writes to those paths.

1. Choose an explicit empty output directory and generate the pinned project. Set `SKILL_DIR` to this skill's directory.

   ```sh
   python3 "$SKILL_DIR/scripts/create_report.py" OUTPUT \
     --language en --title "Weekly research update" --author "A. Researcher" \
     --report-type progress
   ```

   The CLI treats `--title` and `--author` as plain text and escapes TeX-special characters. For an advanced TeX author structure, edit `main.tex` after generation instead of passing raw TeX in `--author`.

2. Replace the generated evidence-state text in `main.tex` with the finished content. Keep unsupported fields explicit as `Unavailable` or `Planned`, or remove an irrelevant section. Add `references.bib` entries, `\cite{key}`, and the matching commented `\addbibresource` and `\printbibliography` lines only for supplied or verified sources.
3. Run the structural gate. It first rejects a symlinked `OUTPUT` or any symlink anywhere beneath it, without following linked files or directories. It then checks required file/directory types, a real uncommented `elegantpaper` document-class line, the exact eight-path/SHA-256 v0.12 upstream snapshot, equality of root/upstream class copies, and unresolved `@@...@@` markers. Add `--require-pdf` only after a successful compilation.

   ```sh
   python3 "$SKILL_DIR/scripts/validate_report.py" OUTPUT
   ```

4. Compile only when the already-installed stable `latexmk`, `xelatex`, and `biber` launchers are executable. ElegantPaper uses XeLaTeX; bibliography processing uses Biber. The absolute launcher avoids relying on a GUI process or shell-profile `PATH`.

   ```sh
   LATEXMK="$(command -v latexmk)"
   if [ -n "$LATEXMK" ] && command -v xelatex >/dev/null && command -v biber >/dev/null; then
     (cd OUTPUT && "$LATEXMK" -xelatex -interaction=nonstopmode -file-line-error -halt-on-error main.tex)
     python3 "$SKILL_DIR/scripts/validate_report.py" OUTPUT --require-pdf
   else
     printf '%s\n' 'Required existing XeLaTeX/Biber/latexmk toolchain unavailable; deliver source.'
   fi
   ```

5. On success, inspect `main.log` and the rendered PDF for title/author, language, evidence labels, citations, tables or figures, missing glyphs, clipping, and page flow. A verified PDF keeps each section heading with its first paragraph or table and avoids a mostly empty continuation page caused by a displaced float. If this check fails, move the short section together or add a justified page break before its heading, then recompile and re-render. If a tool is missing or compilation fails, deliver the validated source and report the exact missing command or compiler error; do not call the PDF verified.

## Minimal complete `main.tex`

```tex
\documentclass[lang=en,a4paper,11pt]{elegantpaper}
\title{Weekly research update}
\author{A. Researcher}
\date{2026-08-11}
\begin{document}
\maketitle
\section{Status}
Measured: the planned experiment has not yet produced results.
\section{Next steps}
Planned: run the approved protocol and report measured outcomes.
\end{document}
```

## Quick reference

| Need | Use |
| --- | --- |
| Fresh source project | `create_report.py OUTPUT` |
| Marker and structure check | `validate_report.py OUTPUT` |
| Require a compiled PDF | `validate_report.py OUTPUT --require-pdf` |
| TeX unavailable | Deliver source; state the unavailable stable launcher and compile command |

## Common mistakes

- “A missing launcher can be recreated while writing a report”: dependency setup is a separate, explicitly authorized task; report the stable launcher as unavailable.
- “No outside paths changed”: report only the enumerated high-risk audit and any known compiler-managed cache activity; do not claim an impossible whole-filesystem guarantee.
- “A linked asset is still inside the project tree”: symlinks can redirect reads outside `OUTPUT`; copy authorized content into the project as a regular file instead.
- Leaving generated text or `@@...@@` markers: replace it with supplied content, an evidence state, or remove the section, then validate.
- Claiming a PDF was checked because `main.pdf` exists: require successful compilation and inspect the rendered document.
- Switching to pdfLaTeX or BibTeX: use XeLaTeX and Biber for this project.
- Editing `assets/upstream/ElegantPaper-v0.12/`: retain that pinned upstream snapshot unchanged; edit only the generated project root.
