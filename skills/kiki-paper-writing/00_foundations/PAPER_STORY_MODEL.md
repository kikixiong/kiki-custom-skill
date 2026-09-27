# Paper Story Model

## Story graph

Represent the paper as a graph before writing prose:

| Node | Required question |
|---|---|
| Task/value | What capability matters, and to whom? |
| Failure | What concrete behavior is inadequate? |
| Default response | What would a reasonable existing method try? |
| Gap | Which necessary criterion remains unmet? |
| Difficulty | Why is the gap nontrivial? |
| Insight | What evidence-backed observation changes the solution? |
| Method | What action follows from the insight? |
| Evidence | Which test supports each claim? |
| Scope | Where does the conclusion apply or fail? |

Every edge needs a causal, logical, or empirical warrant. A missing edge is a
scientific/story problem, not a transition-word problem.

## Cross-section resolution map

| Section | Resolution | Must answer |
|---|---|---|
| Title | identity | What is the paper about? |
| Abstract | compressed assertion | What, why, how, evidence, takeaway? |
| Introduction | expanded reasoning | Why does the gap exist and why may this work? |
| Related Work | contrast | What is close, and what exact criterion remains? |
| Method | executable specification | What are inputs, states, operations, outputs, and rationale? |
| Experiments | claim tests | Which evidence licenses each promise? |
| Figures/Tables | local evidence/data flow | Can the object be understood independently? |
| Conclusion | bounded closure | What was established, within what scope? |

## Repetition policy

Repeat across sections:

- task and core gap;
- method identity and major actions;
- headline claim and scope;
- canonical terminology and component names.

Change across sections:

- abstraction level;
- amount of mechanism;
- type of evidence;
- rhetorical purpose.

Do not repeat:

- identical opening sentences in Abstract and Introduction;
- derivations in Overview or captions;
- benchmark tables in Abstract;
- full motivation in every Method component.

## Claim–evidence ledger

Before drafting, create:

| Claim ID | Claim | Scope | Required evidence | Actual evidence | Sections |
|---|---|---|---|---|---|

Every headline claim must have a row. Experiments should be organized around
these rows, not around whichever tables already exist.

## Paragraph map

For each paragraph record:

| Paragraph | Main role | Inherited premise | New information | Licensed conclusion | Handoff |
|---|---|---|---|---|---|

Adjacent paragraphs must show real progression. Lexical handoff can help, but
matching the previous last word to the next first word is not required.

## Story stress test

- Can the problem and gap be stated in one sentence each?
- Does the method directly address that gap?
- Does the insight license the method action rather than merely correlate with
  the task?
- Would deleting any paragraph break a needed edge?
- Do experiments test the Abstract and Introduction promises?
- Does Figure 1 establish a premise used later?
- Does the Conclusion stay within the evidence?

