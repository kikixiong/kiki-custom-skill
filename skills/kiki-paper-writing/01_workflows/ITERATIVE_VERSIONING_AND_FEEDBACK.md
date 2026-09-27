# Workflow: Iterative Versioning and Feedback

This protocol handles iterative revision and version management.

## Feedback loop

For each user turn:

1. **Intent:** restate what must change and what must remain.
2. **Mapping:** map each comment to sentence, paragraph, symbol, or global rule.
3. **Scope:** revise the smallest unit that resolves all mapped issues.
4. **Preservation:** keep accepted wording and scientific decisions stable.
5. **Explanation:** report semantic changes, not a generic “polished” claim.
6. **Learning:** add a preference rule only if explicit or repeatedly observed.

## Version states

- **Draft:** candidate under active revision.
- **Confirmed:** user accepted content/wording at that point.
- **Canonical:** selected source for the manuscript.
- **Synchronized:** canonical text was copied to the active manuscript.
- **Superseded:** replaced but retained as evidence.

Do not equate confirmed with synchronized. Do not delete superseded versions.

## File/version convention

Use stable component names and monotonic versions, for example:

```text
abstract_v003.tex
intro_p2_v005_confirmed.tex
method_overview_v004.tex
```

Add semantic suffixes only when useful (`_notation`, `_compressed`,
`_confirmed`). Do not use multiple ambiguous `final_final` names.

## Master record

For long projects maintain `WRITING_MASTER_RECORD.md` with:

```text
Current canonical files
Confirmed but unsynchronized files
Open scientific decisions
Terminology and symbol decisions
Section/paragraph status
Important rejected alternatives and reasons
Latest compilation/render status
Session/log index
```

Update the record after a meaningful decision, not after every punctuation edit.
Verify it against actual files before treating it as fact.

## Semantic Diff record

For important changes record:

```text
Source → target:
User feedback:
Surface change:
Problem solved:
Claim/meaning effect:
Reusable rule:
Evidence class:
```

Label rules as Explicit, Strongly Inferred, or Project-Specific.

## Confirmation boundary

Ask the user before changing a confirmed scientific interpretation, equation,
claim scope, official term, or story branch. Fix grammar and clear consistency
errors autonomously when meaning is unchanged.

