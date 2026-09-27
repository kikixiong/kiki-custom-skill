# Claim Calibration

## Audit a claim

Record:

| Field | Question |
|---|---|
| Proposition | What exactly is asserted? |
| Subject | Which model, method, data, or setting? |
| Scope | Datasets, tasks, assumptions, conditions? |
| Relation | Causal, correlational, comparative, descriptive? |
| Strength | Possible, indicative, consistent, demonstrated, guaranteed? |
| Evidence | Figure, controlled experiment, theorem, analysis? |
| Alternative | What competing explanation remains? |

## Evidence-to-language map

- Mathematical proof under explicit assumptions may license `proves` or
  `guarantees` within those assumptions.
- Controlled intervention may license causal language for the manipulated
  relation.
- Repeated experiments may license `shows` or `demonstrates` within evaluated
  scope.
- Observational association licenses `correlates with`, `tracks`, `indicates`,
  or `is consistent with`.
- Exploratory evidence licenses `suggests`, `may`, or `could`.

These are semantic guides, not automatic word replacements.

## Common repairs

- `eliminates` → `reduces` when failures remain.
- `always` → `consistently across evaluated settings` when coverage is finite.
- `causes` → `is associated with` without intervention.
- `generalizes` → name the evaluated transfer setting.
- `the first` → verify literature coverage or remove priority.
- `significantly` → provide statistical evidence or use a quantitative margin.

## Cross-section monotonicity

Claim strength must not silently increase as the paper progresses:

`Abstract ≤ Introduction ≤ actual evidence` and
`Method effect language ≤ demonstrated behavior`.

Different sections may emphasize different aspects, but proposition and scope
must remain compatible.

## Claim gate

Reject or revise a claim when:

- its subject is ambiguous;
- the verb implies causality unsupported by design;
- scope exceeds evaluated conditions;
- it conflates a proxy with the target property;
- it treats trend correspondence as pointwise equality;
- it turns intended behavior into guaranteed behavior;
- no experiment, theorem, or analysis can be named as support.

