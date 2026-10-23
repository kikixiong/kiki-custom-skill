---
name: paper-illustration
description: 使用 Codex 原生图像工具制作和修改论文插图，按需衔接可编辑结构图与科研绘图。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Paper Illustration: Multi-Stage Codex-Supervised Figure Generation

Create scientific illustrations using the native Codex image-generation tool
and the installed `imagegen` skill. Use the actual tool available in the current
session. Gemini/OpenRouter keys and a local model installation are not required.

## Select the output method

- Measured data plots: use deterministic plotting with saved aggregate results
  and `$af-academic-plotting` or `$nature-figure`; never generate numerical evidence
  with an image model.
- Precise architecture/flow diagrams with editable text: use `$figure-spec` or
  `$mermaid-diagram` when suitable.
- AI illustrations or edits: use native image generation. Inspect supplied images
  with the available image-viewing tool before edits and follow imagegen's current
  reference-image interface.

## Workflow

1. Read the user's figure brief, relevant methods, labels and any reference images.
   Derive the actual components, arrow directions, evidence and output dimensions.
2. Plan a clear reading order, grouping, sparse labels and colorblind-friendly
   palette. Use legible type, consistent symbols and sufficient white space;
   size strokes and fonts for the final printed figure rather than fixed pixels.
3. Generate through the native image tool. Use its documented image-output method
   and return the generated result. Do not invent a local output path.
4. Inspect scientific accuracy and legibility. Fix a concrete error when needed;
   do not force five iterations or an arbitrary score threshold.
5. If a local artifact was actually produced, retain it under the active project's
   `figures/ai_generated/` or requested output directory. Preserve sources and
   captions, and disclose raster limitations if editable vector output was requested.

Use the current model/tool configuration and the user's permitted execution
environment. Do not install or launch another backend implicitly. Use author
names and affiliations from the manuscript or user input.

## Optional backend

Read [the historical Gemini workflow](references/optional-gemini-workflow.md)
only when the user explicitly requests that backend. Reuse existing access;
do not load it as a prerequisite for native generation. Its names and examples
must be checked against the requested backend before use. Create task-scoped
`work/` files if needed, and never write API keys into them or print credentials.
