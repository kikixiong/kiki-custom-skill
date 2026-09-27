# ElegantPaper Project Contract

## Deliverable

Create a fresh, self-contained project containing:

```text
OUTPUT/
├── main.tex
├── references.bib
├── elegantpaper.cls
├── figures/
├── latexmkrc
├── .vscode/settings.json
└── upstream/ElegantPaper-v0.12/
```

Use `scripts/create_report.py` with a language (`zh` or `en`), title, author, report type, and explicit empty output directory. It refuses a non-empty target. The generated source contains explicit `Unavailable` or `Planned` evidence states rather than unresolved markers; replace those statements with finished, supported content before delivery.

The title and author CLI options are plain-text metadata and escape TeX-special characters. Reserved `@@...@@` template-marker syntax and control characters are rejected before any output write so every generated project can pass the structural gate. Edit the generated `main.tex` for an advanced TeX author structure rather than passing raw TeX to `--author`.

`upstream/ElegantPaper-v0.12/` is the bundled ElegantLaTeX/ElegantPaper v0.12 snapshot (commit `366d1e095a595b812b9a76bef1b6e245fbe417b3`). Preserve its files, provenance, and `License` byte-for-byte. The root `elegantpaper.cls` is copied from that snapshot so the project can be uploaded intact. Keep report edits outside the snapshot.

## Content and citations

Use only supplied or verified facts. Label evidence as **Measured**, **Supplied**, **Verified source**, **Planned**, or **Unavailable**. Separate observations, interpretations, limitations, and next steps. Omit sections with no purpose rather than adding filler. Do not invent results, citations, authors, affiliations, figures, tables, or completion.

Add a BibLaTeX entry and `\cite{key}` only when a supplied or verified source supports the nearby claim. The scaffold leaves both `\addbibresource` and `\printbibliography` commented so a source-free draft compiles without an empty-bibliography or no-citations Biber warning; enable both lines only after adding a real citation and bibliography entry. Label and reference every included figure or table; provide its values, units, and source.

## Mechanical validation and compilation

Run `scripts/validate_report.py OUTPUT` before compilation. It rejects `OUTPUT` itself or any descendant that is a symlink; its non-following inventory runs before marker, class, or hash reads. It then deterministically checks required file/directory types, an uncommented `\documentclass{elegantpaper}` line (including options), the exact eight-path/SHA-256 upstream v0.12 snapshot, equality of the root/upstream class copies, and every unresolved `@@...@@` marker in `.tex` files. Use `--require-pdf` only when `main.pdf` must exist.

Compile with the already-installed local XeLaTeX and Biber toolchain. The
stable launcher is absolute so VS Code and Codex do not depend on a shell
profile or GUI-process `PATH`:

```sh
cd OUTPUT
@@KIKI_LATEXMK@@ -xelatex -interaction=nonstopmode -file-line-error -halt-on-error main.tex
```

Treat a nonzero exit, fatal log error, unresolved citation/reference, Biber error, or missing `main.pdf` as unverified. If the stable launcher or one of its XeLaTeX/Biber dependencies is unavailable, do not install anything implicitly: report the unavailable executable and the exact command above, then deliver the structurally validated source. After a successful build, run `validate_report.py OUTPUT --require-pdf` and inspect `main.log` plus the rendered PDF.

## Delivery boundary

Deliver the complete source tree and, only after the successful compile and visual inspection above, `main.pdf`. The project is Overleaf-ready, but local preparation does not authorize upload, Git operations, credentials, or synchronization. Use `overleaf-paper-sync` only for an explicit Git-sync or review-gate request.

Keep deliberate writes within the explicit user-approved `OUTPUT`. Do not create installers, wrappers, symlinks, profile/PATH edits, configuration, helper files, or dependency caches elsewhere. Audit the named high-risk paths in `SKILL.md` before and after the run and disclose their observed status. This is an agent-write boundary, not a claim that an existing compiler cannot update its own user-level caches; disclose known compiler-managed writes or use source-only fallback when strict containment cannot be assured.
