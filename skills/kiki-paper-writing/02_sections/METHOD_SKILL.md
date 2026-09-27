# Method Skill

## Function

Method converts the Introduction's idea into an executable and auditable
specification: objects, objective, operations, dependencies, outputs, and
rationale. It is not an implementation log or a collection of equations.

## Recommended organization

1. **Preliminaries:** minimal task setting and objects needed globally.
2. **Overview:** component/dependency map aligned with the framework figure.
3. **Components:** in conceptual or execution order.
4. **Algorithm/decoding/optimization:** only when it clarifies actual control
   flow beyond equations.

Adapt organization to the method. Do not create Preliminaries or Overview when
the paper is simpler without them.

## Start from an execution trace

Before notation, write:

```text
Input:
Persistent state:
Step-by-step operations:
Shared versus branch-specific state:
Update/fusion order:
Stopping/tie-breaking/fallback:
Output:
Training/inference distinction:
```

Only then assign symbols.

## Preliminaries

Include objects, types, factorization/objective, and assumptions used across
multiple components. Exclude future thresholds, search details, and component
outputs that can be defined just in time.

Distinguish:

- model versus conditional distribution;
- function/map versus its evaluated value;
- textual condition versus prediction;
- set versus ordered sequence;
- history/state versus generated output.

## Overview

State method name, input/output, component roles, dependencies, and global
constraints. Match component names and flow in the framework figure.

Avoid repeating Preliminaries, writing formulas, or forecasting every local
detail.

## Component algorithm

Use:

1. **Connection/motivation:** what prior output or gap makes this needed?
2. **Definition/formula/algorithm:** one logical action at a time.
3. **Immediate explanation:** define unfamiliar symbols and actual behavior.
4. **Rationale/transition:** what property or next input results?

“Formula before all definitions” and “define everything before formula” are
both too rigid. Define prerequisites first; define local symbols in or
immediately after the formula.

## Notation design

- one symbol, one meaning;
- just-in-time introduction;
- visually coherent families without collisions;
- minimal symbols for repeated or relationship-critical objects;
- prefer a generic mapping evaluated under different inputs over separate
  superscripted variables when semantics are shared;
- after renaming, search equations, prose, captions, algorithms, and appendices.

## Formula audit

For each equation:

- What single logical action does it perform?
- Are all dependencies defined?
- Is the left-hand object typed?
- Does prose before it explain why?
- Does prose after it explain operational behavior?
- Is punctuation and equation reference correct?
- Would plain language be clearer?

Formula complexity must come from necessary relations, not presentation theater.

## Multi-branch methods

When a method has a reliable/reference branch and a full/target branch, state:

- responsibility of each branch;
- which condition or information differs;
- which state/history is shared;
- when predictions are computed;
- where information is compared or fused;
- whether fusion occurs before or after sampling/update;
- how many output trajectories exist.

Do not say branches or conditions are “aligned” if the precise fact is that
predictions share a history.

## Search and stopping

If search is method-defining, specify:

- state space and legal transitions;
- score or feasibility criterion;
- expansion/pruning policy;
- stopping condition;
- tie-breaking;
- budget and fallback when no feasible candidate exists.

Implementation-only beam widths, temperatures, and filters may belong in
Experiments unless they change method semantics.

## Cross-section audit

Check:

- Introduction components correspond to Method components;
- framework modules and arrows match dependencies;
- captions use active notation;
- ablations test claimed component roles;
- equations and algorithm share execution order;
- intended effects are not written as guarantees.

## Method anti-patterns

- textbook Preliminaries;
- Overview duplicating setup;
- prose repeating equations;
- formula without motivation;
- undefined or overloaded symbols;
- results or praise in Method;
- hyperparameter detail that hides the core rationale;
- branch ambiguity and unstated stopping.

