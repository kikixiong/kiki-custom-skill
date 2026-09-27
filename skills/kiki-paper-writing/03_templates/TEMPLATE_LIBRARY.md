# Template Library

Templates are function maps, not mandatory wording. Delete unavailable slots;
do not invent content to fill them.

## Story card

```text
Task/value:
Failure:
Existing/default response:
Missing criterion:
Why unresolved:
Insight and evidence source:
Method actions:
Headline evidence:
Scope/limitations:
```

## Abstract slots

```text
[Task/value.]
[Concrete failure and consequence.]
[Exact gap or missing criterion.]
[Evidence-backed insight.]
[Method identity, actions, and rationale.]
[Headline evidence and evaluated scope.]
[Bounded takeaway.]
```

## Introduction paragraph map

```text
P?: Role:
Inherited premise:
New mechanism/evidence:
Strongest licensed conclusion:
Handoff:
Figure/table support:
```

Possible roles include task/tension, gap/difficulty, evidence/observation,
inference/insight, method/rationale, evidence preview, and contributions.

## Contribution item

```text
We [establish/identify/introduce/evaluate] [specific contribution object],
which [action or new capability] under [scope], supported by [evidence class].
```

Vary grammar across items if clarity improves; keep abstraction levels parallel.

## Method section

```text
Preliminaries (only if needed)
  objects, types, objective, assumptions

Overview
  input/output, component roles, dependencies, figure alignment

Component
  connection/motivation
  definition/formula/algorithm
  local symbol explanation
  operational behavior and handoff

Execution/algorithm (if equations do not expose control flow)
  state, order, stopping, tie-breaking, fallback, output
```

## Formula wrapper

```text
[Why this relation/action is needed.]
[Equation.]
where [only unfamiliar local symbols].
[What the equation does operationally and what it provides next.]
```

## Figure captions

### Motivation/evidence

```text
[Whole-figure question or evidence role.]
(a) [setup/comparison and observation].
(b) [setup/comparison and observation].
[(c,d) grouped role when appropriate].
[Joint bounded inference, if directly supported.]
```

### Framework

```text
[Method/pipeline identity and overall input/output.]
[Left/Top:] [stage input → action → output].
[Center:] [dependency and action].
[Right/Bottom:] [final action and output].
[Shared state, global constraint, or encoding legend.]
```

### Results

```text
[Metric/outcome versus factor or methods.]
[Axes, conditions, aggregation, uncertainty.]
[Panel map and encodings.]
[Main visible pattern without unsupported explanation.]
```

## Experiment block

```text
Research question:
Claim tested:
Comparison/control:
Data and metric:
Statistic/uncertainty:
Result:
Interpretation:
Alternative explanation or limitation:
```

## Version decision

```text
Function being compared:
Candidate A proposition/scope:
Candidate B proposition/scope:
Decisive criterion:
Selected:
Rejected-version failure:
Downstream effects:
```

## Feedback record

```text
User intent:
Must preserve:
Requested change:
Mapped edits:
Semantic effect:
Remaining risk:
Version state:
Reusable rule and evidence class:
```

