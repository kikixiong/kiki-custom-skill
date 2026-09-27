# Project-Specific vs General

## General rules

Transfer safely across AI/ML and technical papers:

- tell one causal story at different resolutions;
- put concrete failure before abstract diagnosis;
- make paragraphs perform unique roles;
- make examples and figures perform inference;
- distinguish correlation, trend correspondence, and causation;
- expand Abstract assertions in Introduction rather than copying them;
- keep Preliminaries minimal and Overview dependency-focused;
- make formula complexity follow necessary relationships;
- define the ideal objective before an approximation;
- audit terminology, notation, claims, and rendered assets globally;
- stop claim strength at the available evidence.

## Conditional patterns

Transfer only when the new method has the stated structure:

- **Reference and target branches:** state role, differing information, shared
  state, fusion/update order, and output multiplicity.
- **Lexicographic design:** formalize priorities separately only when
  feasibility, minimum intervention, and tie-breaking are real objectives.
- **Early proxy:** establish that the complete signal matters, that it can be
  observed early, and that the early proxy preserves the relevant relation.
- **Search approximation:** define the ideal target and disclose pruning,
  budget, stopping, and approximation limits.

## Historical project-specific examples

Do not reuse these as universal templates:

- CAPD, UMM, long-prompt image generation, or X-Omni;
- generation capacity as a field-independent construct;
- instruction-unit deletion and minimum deletion depth;
- exponentiated negative entropy and geometric prefix aggregation;
- historical Figure 1 percentages or prompt-length trends;
- symbols such as \(P,Q,P_S,P_s,g_\theta,\alpha\);
- a raw-logit residual or one visual-token trajectory;
- the exact paragraph/panel order of the source Introduction;
- benchmark-specific conclusions.

They remain useful only as examples of general reasoning patterns.

## Generalization test

Before promoting a local choice:

1. Identify at least two independent decisions supporting it.
2. State the underlying problem without source-project vocabulary.
3. Produce a transfer example in another domain.
4. Name a condition where the rule would be wrong.
5. Label it Explicit, Strongly Inferred, Project-Specific, or Provisional.

## Known uncertainty

- Final verbs such as `establishes` remain evidence-dependent.
- Terminology choices that were not globally resolved must be reconsidered in
  each new paper.
- Search fallback and threshold calibration require implementation evidence.
- Related Work, Experiments, Conclusion, and Table preferences remain less
  mature than the four core section Skills.

