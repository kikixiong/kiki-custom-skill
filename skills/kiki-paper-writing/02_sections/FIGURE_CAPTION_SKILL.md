# Figure Caption Skill

## Function

A caption provides enough local context to interpret the rendered asset. It
should identify purpose, reading structure, setup, encodings, and licensed
observation. It complements the main text rather than copying it.

## Universal construction

1. **Purpose sentence:** what question, evidence, comparison, or pipeline the
   whole figure presents.
2. **Map:** panels/stages and reading order.
3. **Setup:** compared objects, conditions, metrics, and statistics needed to
   interpret the asset.
4. **Encoding:** colors, markers, arrows, shading, abbreviations, symbols.
5. **Observation:** the main visible pattern at evidence-appropriate strength.

Not every figure needs all five as separate sentences.

## Motivation/evidence figure

For each panel use:

```text
question → setup/comparison → observation → bounded inference
```

Include key numbers only when essential to interpreting scale. A closing
sentence may unify panels if the joint inference is directly supported. Leave
causal explanation to the main text unless the figure design establishes it.

## Framework figure

Use:

```text
method/pipeline identity → input/output → spatial stage map →
per-stage input/action/output → global state or constraints
```

Component names, symbols, shared state, arrows, and execution order must match
Method Overview and equations exactly.

## Results/ablation figure

Define axes, metrics, conditions, uncertainty, and aggregation. State a visually
clear trend; do not turn the caption into a full explanation of why it occurs.

## Panel-by-panel audit

For every panel:

- Is the panel mentioned?
- Does the caption state its role rather than repeat its title?
- Are comparison objects and metrics identifiable?
- Is the inference no stronger than the plotted evidence?
- Does panel order match the main text and visual reading order?

Group panels only when they answer the same sub-question.

## Rendered-asset consistency

Inspect the actual PDF/image:

- panel labels;
- legends, colors, markers, arrows, line styles;
- embedded words and mathematical symbols;
- direction of data flow;
- font size, clipping, whitespace, and resolution.

Text search cannot validate embedded visual labels.

## Self-contained test

A reader seeing only figure and caption should be able to answer:

- What is shown and why?
- How should it be read?
- What do panels and encodings mean?
- What observation is justified?

Self-contained does not mean reproducing the paper's full derivation.

## Common failures

- `Overview of our proposed method` with no data flow;
- panel list with no setup or observation;
- unexplained colors/arrows;
- inactive symbols left in the artwork;
- caption claiming causes from correlations;
- result analysis that belongs in the main text;
- absolute rules such as always including numbers or never stating a conclusion.

