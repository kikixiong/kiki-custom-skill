# Workflow: Revise Existing Draft

## Preserve a baseline

Keep the original version and identify canonical versus experimental files.
Do not overwrite confirmed text without an explicit need.

## Six-level diagnosis

### Level 1: Paper story

- Can problem, gap, insight, method, and evidence each be stated?
- Does every arrow have a warrant?

### Level 2: Section structure

- Is each idea in the section that should carry it?
- Is any prerequisite introduced after its use?

### Level 3: Paragraph function

- Does each paragraph have one primary job?
- Does it add information and create the next prerequisite?

### Level 4: Sentence logic

- Are referents, comparison axes, and causal relations explicit?
- Does each connector describe a real relation?

### Level 5: Expression

- Are subject and action concrete?
- Can wording be shorter without losing logic?
- Does the prose sound formulaic or promotional?

### Level 6: Mechanics

- terminology, notation, grammar, punctuation;
- LaTeX, citations, labels, references, figures, and tables.

Fix the earliest failing level first.

## Revision passes

1. Diagnose without rewriting.
2. Propose the smallest structural repair.
3. Rewrite the affected scope.
4. Produce a semantic Diff: added, removed, narrowed, reordered, renamed.
5. Recheck neighboring paragraphs and downstream sections.
6. Run mechanics only after semantics stabilize.

## Output

```text
Highest failing level:
Why:
Revised text:
Semantic changes:
Claim/consistency risks:
User decisions:
```

