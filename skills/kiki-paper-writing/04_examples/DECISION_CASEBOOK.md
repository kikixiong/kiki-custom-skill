# Decision Casebook

These compact cases preserve the decision logic of the source Skills. Project
terms are illustrative; transfer the rule, not the exact structure.

## Case 1: Complete explanation versus redundant ending

**Before**

> The model must satisfy several instructions simultaneously, but its reliable
> capacity is unknown, leaving the feasibility criterion ill-posed.

**Issue**

The first clause already explains why feasibility cannot be known. The final
abstract label repeats the diagnosis without advancing the story.

**After**

> The model must satisfy several instructions simultaneously, but its reliable
> capacity is unknown.

**Rule**

Stop once mechanism and consequence are complete. Keep an abstract label only
when later reasoning consumes that label.

## Case 2: Correlation does not become causality

**Too strong**

> Early confidence determines final generation quality.

**Calibrated**

> Early confidence tracks final generation quality across the evaluated
> conditions, motivating its use as an early indicator.

**Rule**

Separate the observed association from the design decision it motivates.

## Case 3: Introduction detail belongs in Method

**Overloaded preview**

> We compute token entropy, search all deletion subsets with beam width \(B\),
> and fuse logits with coefficient \(\alpha\).

**Role-correct preview**

> We use an early reliability signal to identify a feasible reference
> condition, then guide the full prediction against that reference.

**Rule**

Introduction states actions, dependencies, and rationale. Method carries local
formulas and implementation-defining execution details.

## Case 4: Generic mapping reduces notation

**Before**

Separate symbols are introduced for the same logit function under a full and a
reduced condition.

**After**

Define one logit mapping and evaluate it under the two conditions.

**Rule**

When semantics are shared and only inputs differ, prefer one typed mapping over
case-specific superscripts. This reduces definitions and exposes comparison.

## Case 5: Branch alignment requires exact state language

**Ambiguous**

> The two conditions are aligned during decoding.

**Precise**

> Both predictions are evaluated on the same generated-token history before
> their logits are fused, producing one sampled trajectory.

**Rule**

For multi-branch methods, state shared state, differing information, fusion
time, and output multiplicity.

## Case 6: Caption label list versus local narrative

**Before**

> Confidence analysis. (a) Quality comparison. (b) Prefix influence.

**After**

> Relationship between early confidence and generation quality. (a) Compares
> quality across confidence groups under matched prompt lengths. (b) Measures
> how much early-token perturbations alter the later trajectory.

**Rule**

Caption panels need question/setup and interpretable observation, not only
names. Add numbers only when needed for scale.

## Case 7: Rigid supplementary rule rejected

**Candidate rule**

> Introduction must contain no numbers and exactly six paragraphs.

**Merged rule**

> Use the paragraph count required by the story. Usually reserve dense
> quantitative detail for Experiments; retain a decisive Introduction number
> when it establishes magnitude or credibility.

**Rule**

Convert project-specific successful patterns into conditional heuristics.

## Transfer example: systems paper

A scheduler paper may use two branches (safe baseline and optimized plan).
Apply the multi-branch rule by specifying shared workload state, branch-specific
information, decision fusion time, and whether the system executes one plan.
Do not copy generation-specific terminology.

