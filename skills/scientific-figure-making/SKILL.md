---
name: scientific-figure-making
description: 按 figures4papers 的风格制作柱状图、趋势图、热图等发表用图。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Scientific figure making

Open `references/` only as needed; do not preload every file. Start from the table below, then follow links inside the document you opened (and into `figure_*` code via [references/demos.md](references/demos.md)) instead of loading the full reference set up front.

## When to load this skill

- Matplotlib figures for **papers, slides, or reports** that must match **this repo’s publication look** (fonts, palette, spines, legends, export).
- Requests involving **grouped bars, trend lines, heatmaps, multi-panel grids**, or **PDF/SVG/high-DPI** output in a scientific-figure context.
- References to **figures4papers** `figure_*` projects or “same style as the repo figures.”

## When not to load

- **Plotly, Altair, Bokeh**, or other interactive / web-first plotting.
- **EDA-only** plots where seaborn or pandas is enough until there is a publication target.
- Primary workflow is **3D, GIS**, or **non-matplotlib** tooling.
- **Illustrator / Figma–first** layout or infographic (not matplotlib data plots).

## Related files

| File | Open when |
|------|-----------|
| [references/tutorials.md](references/tutorials.md) | End-to-end walkthroughs (bar, trends, heatmap) |
| [references/api.md](references/api.md) | Function signatures, `PALETTE`, validation rules |
| [references/common-patterns.md](references/common-patterns.md) | Layout patterns, legend panel, print-safe bars |
| [references/design-theory.md](references/design-theory.md) | Typography, export policy, palette rationale |
| [references/demos.md](references/demos.md) | Canonical `figure_*` demo links in figures4papers |
