---
name: figures4papers
description: 把科研绘图请求转到 figures4papers 示例与对应绘图技能。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Figures4Papers Router

Use this skill when a paper figure should follow the `figures4papers` style or when the user names the repo directly. The installed source is at:

`@@KIKI_SUPPORT_DIR@@/vendor/figures4papers`

## Route

- For matplotlib implementation details, load `scientific-figure-making`.
- For Nature-style or journal-level figure design, use `nature-figure` together with `scientific-figure-making`.
- For figure planning before code, use `figure-designer`.
- For deterministic architecture/workflow diagrams, use `figure-spec` or `mermaid-diagram`.

## Operating Rules

- Prefer reusable plotting scripts that export `.pdf` or `.svg` plus a high-DPI `.png`.
- Follow the figures4papers conventions for palette, typography, clean axes, legend placement, multi-panel layout, and export.
- Inspect the closest demo under the vendor source before writing a new plot.
- Do not invent data. If data is missing, create a script with clear input paths and a tiny synthetic smoke-test block only when useful.

## Default Output

Return or create:

- plot script path
- expected input data schema
- output figure paths
- style choices
- verification command
