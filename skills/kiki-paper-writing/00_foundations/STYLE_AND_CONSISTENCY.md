# Style and Consistency

## Academic style

- Lead with the concrete subject and action.
- Prefer one main clause when a sentence already contains a causal comparison.
- Use a colon, semicolon, or dash only when it reveals structure better than
  two sentences; punctuation is not a substitute for logic.
- Replace generic importance language with the actual consequence.
- Use transitions that name the relation: contrast, consequence, condition,
  refinement, or evidence.
- Vary sentence rhythm after logic is stable; do not optimize rhythm first.
- Stop at the strongest complete explanation.

## Information-density test

For each sentence ask:

1. What proposition disappears if deleted?
2. Does the next sentence depend on it?
3. Is it new, or a paraphrase of nearby text?
4. Does its section need this resolution of detail?

If deletion loses nothing, delete. If it contains one needed element, replace
it with the smallest sentence carrying that element.

## Controlled terminology

Maintain a table:

| Concept ID | Canonical term | Definition | Allowed local variants | Forbidden collisions |
|---|---|---|---|---|

Canonical terms and component names should remain exact. Contextual grammar
may vary; uncontrolled synonym drift may not.

## Symbol table

Track:

| Symbol | Meaning/type | First definition | Dependencies | Used in figure/algorithm |
|---|---|---|---|---|

Rules:

- one symbol, one stable semantic role;
- distinguish object, set, sequence, distribution, function, and scalar;
- introduce at first genuine need;
- prefer a reusable mapping evaluated on different inputs over multiple
  case-specific superscripts;
- avoid visual collisions even when formally distinguishable;
- audit all occurrences after renaming.

## Cross-section matrix

Compare Title, Abstract, Introduction, Method, Experiments, captions, and
Conclusion for:

- task/gap wording;
- method and component names;
- contribution count;
- claim proposition, strength, and scope;
- metrics and result direction;
- symbols and branch roles;
- data flow and update order;
- figure/table interpretation;
- labels, citations, and numbering.

## Mechanical conventions

- Expand abbreviations at first relevant appearance.
- Use consistent capitalization, hyphenation, decimal precision, and tense.
- Use nonbreaking spaces in LaTeX references where appropriate.
- Resolve every label/reference and inspect the rendered PDF.
- Do not rely on text search to validate labels embedded in PDF/SVG figures.

