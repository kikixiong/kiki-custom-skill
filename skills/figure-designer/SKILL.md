---
name: figure-designer
description: 规划 Figure 1、方法总览图和实验图的布局、标注与信息结构。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
disable-model-invocation: true
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Figure Designer

Use this skill for research-paper figures, not generic plotting alone.

## Figure Types

- `Motivated Example`: early paper figure that exposes the real failure case or task need.
- `Solution Overview`: method/system overview inside methodology.
- `Experimental Results`: plots or composite figures in the experiments section.

## Procedure

### 1. Identify The Figure Type

If the user's request does not fit one of the three core types, treat it as a supporting figure and use the experimental-results guidance as a fallback.

If the user provides an image or a local image path for audit, inspect it first with `view_image` or the attached image context before analyzing it.

### 2. Recommend The Best Paradigm

Choose the best figure pattern for the storytelling goal and briefly explain why the other likely patterns are worse fits.

### 3. Produce A Layout Sketch

Describe:

- canvas
- panel order
- arrows and connections
- element placement
- color roles

The sketch should be concrete enough that the first draft can be drawn from it directly.

### 4. Labeling And Annotation Rules

- use concrete names, not placeholders like "Module A"
- mark key failure or success regions
- specify target font sizes
- use color-blind-safe palettes

### 5. Suggest The Tool

Default recommendations:

- schematic figures: PowerPoint for first draft, Figma for polish
- experiment plots: Matplotlib or Seaborn
- LaTeX-native plots: PGFPlots or TikZ when needed

### 6. Run The Universal Audit

Check:

- vector export
- font size at least 8pt after scaling
- small enough canvas for readable text
- color-blind-safe encoding
- self-contained caption with the finding in sentence 1
- honest axis ranges
- no 3D effects or chartjunk

Flag issues as `CRITICAL`, `MAJOR`, or `MINOR`.

## Output

Return:

1. Figure type and reason
2. Paradigm recommendation
3. Layout sketch
4. Labeling and annotation plan
5. Tool suggestion
6. Universal audit checklist
7. Severity summary
8. Top three actions first

## Source

Adapted for Codex from HKUSTDial/Supervisor-Skills, CC-BY-4.0:
https://github.com/HKUSTDial/Supervisor-Skills
