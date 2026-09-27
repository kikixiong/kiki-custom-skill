# Secondary Sections

**Maturity:** Provisional. These rules combine general top-conference practice,
the user's writing notes, and limited project evidence. Treat them as starting
points and update when stronger user-specific evidence appears.

## Related Work

Organize by capability, assumption, or solution family—not paper chronology.
For each group:

1. state the shared goal;
2. synthesize representative approaches;
3. identify what they handle;
4. state the exact criterion they leave unresolved;
5. connect that criterion to this paper without straw-manning.

Avoid citation inventory, praise, and Method detail. Verify literature before
priority or absence claims.

## Experiments

Organize by research question or claim:

- Does the method solve the main problem?
- Which components cause the gain?
- Do assumptions/proxies hold?
- Where does it fail?
- What are efficiency and robustness costs?

For each block:

```text
question → design → metric/statistic → result → interpretation → limitation
```

Setup must support reproducibility: datasets/splits, baselines, metrics,
implementation, seeds, compute, and statistical protocol as relevant.

Ablations should correspond to method roles, not merely remove named modules.
Analyze anomalies and negative results rather than hiding them. Do not assert
causality from an uncontrolled ablation.

## Conclusion

Restate problem, supported method idea, and evidence-backed takeaway at a
slightly higher level. Include limitations or scope when material. Add no new
method component, result, citation-dependent claim, or universal promise.

## Tables

The table and caption should identify task, data, metric, direction, statistic,
and visual conventions. Group rows/columns by meaningful comparison. Explain
abbreviations and missing values. Bold/underline only with a declared rule;
do not assume “best/second best” is always the right encoding.

The main text should interpret patterns, trade-offs, and exceptions, not read cells in
order. Ensure precision and significance claims match the reported statistics.

## Provisional update interface

When new project feedback appears, record:

```text
Section:
Explicit feedback:
Accepted/rejected alternatives:
Repeated pattern:
Proposed rule:
Evidence class:
Scope:
```

Promote a provisional rule only after explicit or repeated evidence.

