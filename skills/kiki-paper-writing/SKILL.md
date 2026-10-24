---
name: kiki-paper-writing
description: Evidence-grounded planning, drafting, revision, comparison, and final audit for AI/ML and technical research papers. Use when writing from an idea or outline; revising an Abstract, Introduction, Method, Figure Caption, Related Work, Experiments, Conclusion, or Table; choosing among versions; calibrating claims; formalizing notation; processing iterative user feedback; or aligning story, evidence, figures, tables, citations, and LaTeX across a paper.
disable-model-invocation: true
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Kiki Paper Writing

## Purpose

Produce technically accurate, causally complete, compact conference-paper prose.
Treat surface fluency as the last layer, not the objective. Make the paper's
problem, gap, insight, method, evidence, terminology, symbols, figures, and
experiments mutually accountable.

This is a self-contained Skill. All operational rules, templates, user
preferences, decision evidence, and generalization boundaries required for use
are bundled in this folder. Fixed lengths and project-specific structures are
heuristics, never universal rules.

## Classify the task before writing

Classify the input:

- **Idea:** problem, intuition, scattered results, or one main figure.
- **Outline/template:** headings or paragraph slots without complete prose.
- **Draft:** prose whose story or structure may still change.
- **Near-final:** stable science requiring consistency and mechanical audit.
- **Candidates:** two or more alternatives requiring a decision.
- **Feedback turn:** a prior version plus user acceptance, rejection, or edits.

Route accordingly:

- Idea → [FROM_ZERO.md](01_workflows/FROM_ZERO.md)
- Outline → [FROM_OUTLINE_OR_TEMPLATE.md](01_workflows/FROM_OUTLINE_OR_TEMPLATE.md)
- Draft → [REVISE_EXISTING_DRAFT.md](01_workflows/REVISE_EXISTING_DRAFT.md)
- Candidates → [COMPARE_MULTIPLE_VERSIONS.md](01_workflows/COMPARE_MULTIPLE_VERSIONS.md)
- Feedback/version work → [ITERATIVE_VERSIONING_AND_FEEDBACK.md](01_workflows/ITERATIVE_VERSIONING_AND_FEEDBACK.md)
- Assembly or near-final → [GLOBAL_ASSEMBLY_AND_FINAL_AUDIT.md](01_workflows/GLOBAL_ASSEMBLY_AND_FINAL_AUDIT.md)

## Load references progressively

For story or structural work, read:

- [PAPER_STORY_MODEL.md](00_foundations/PAPER_STORY_MODEL.md)
- [USER_WRITING_PROFILE.md](00_foundations/USER_WRITING_PROFILE.md)

For claims, terminology, or style, read:

- [CLAIM_CALIBRATION.md](00_foundations/CLAIM_CALIBRATION.md)
- [STYLE_AND_CONSISTENCY.md](00_foundations/STYLE_AND_CONSISTENCY.md)
- [ANTI_PATTERNS.md](00_foundations/ANTI_PATTERNS.md)

Then load only the relevant section Skill:

- [ABSTRACT_SKILL.md](02_sections/ABSTRACT_SKILL.md)
- [INTRODUCTION_SKILL.md](02_sections/INTRODUCTION_SKILL.md)
- [METHOD_SKILL.md](02_sections/METHOD_SKILL.md)
- [FIGURE_CAPTION_SKILL.md](02_sections/FIGURE_CAPTION_SKILL.md)
- [SECONDARY_SECTIONS.md](02_sections/SECONDARY_SECTIONS.md)

Use the secondary-section guidance as **Provisional** where user-specific
evidence is limited.

## Preference hierarchy

When criteria conflict, decide in this order:

1. factual and evidential accuracy;
2. complete causal or inferential logic;
3. correct section and paragraph role;
4. coverage of the actual contributions and mechanisms;
5. terminology, notation, and cross-section consistency;
6. concision;
7. natural academic style;
8. rhythm and elegance.

Never select a prettier sentence that loses an earlier criterion.

## Build one paper story

Normalize the paper into:

> task/value → concrete failure → reasonable existing response → exact missing
> criterion → why unresolved → evidence-backed insight → method action(s) →
> claim-matched experiments → bounded takeaway.

For every arrow, write the missing causal or inferential sentence. If an edge
is unknown, mark it as an open scientific question; do not conceal it with
`therefore`, `importantly`, or novelty language.

Map the same story at different resolutions:

- Title: identity and searchable promise.
- Abstract: compressed conclusions.
- Introduction: motivation, mechanism, evidence, and logical expansion.
- Related Work: nearby capabilities and the exact remaining gap.
- Method: definitions, objective, algorithm, execution order, and rationale.
- Experiments: tests of claims, components, assumptions, and failure modes.
- Figures/Tables: independently interpretable evidence or data flow.
- Conclusion: supported closure, scope, and limitations.

Repeat core concepts and terms; do not repeat wording or section-specific
detail. See [PAPER_STORY_MODEL.md](00_foundations/PAPER_STORY_MODEL.md).

## Draft from zero

1. Extract task, failure, gap, insight, method, evidence, scope, and unknowns.
2. Build a claim–evidence ledger and controlled terminology table.
3. Define the paper story and test every edge.
4. Assign unique functions to sections and paragraphs.
5. Draft a provisional Abstract as a coherence test.
6. Expand the Introduction at a lower abstraction level without copying it.
7. Convert the method execution trace into minimal notation and formulas.
8. Organize experiments by research question or claim, not table order.
9. Draft figures, tables, and captions as information-bearing objects.
10. Revisit Abstract and Conclusion after evidence is concrete.
11. Run the global and rendered-PDF audits.

Do not force Abstract-first if the scientific story is unstable; use a
story-card or Method trace first.

## Revise an existing draft

Diagnose top-down:

1. paper story;
2. section structure;
3. paragraph function;
4. sentence-to-sentence logic;
5. sentence expression;
6. terminology, notation, grammar, references, and LaTeX.

Fix the lowest-numbered failing level first. Grammar polish is wasted when the
paragraph has the wrong job. Preserve the baseline and report semantic changes:
what changed, which problem it solves, and whether scientific meaning changed.

## Compare versions

For each candidate, identify:

- exact claim and main clause;
- information added, removed, or implied;
- causal edge and referents;
- evidence strength and scope;
- section/paragraph fit;
- repetition with neighboring text;
- terminology and downstream effects.

Select lexicographically by the preference hierarchy. Explain why rejected
versions fail. A hybrid is a new candidate and must be audited independently.

## Process user feedback

For each feedback turn:

1. restate the user's intent without upgrading it;
2. map each comment to a concrete edit;
3. preserve accepted text and decisions;
4. revise the smallest scope that resolves the issue;
5. explain semantic changes and remaining risks;
6. distill a reusable rule only after repeated or explicit evidence.

Maintain `draft`, `confirmed`, and `synchronized` as distinct states.
Confirmation means wording was accepted; synchronization means it was copied
into the canonical manuscript. Never infer one from the other.

For long projects, maintain a master record using
[ITERATIVE_VERSIONING_AND_FEEDBACK.md](01_workflows/ITERATIVE_VERSIONING_AND_FEEDBACK.md).

## Paragraph and sentence algorithms

For each paragraph assign:

- one main role;
- inherited premise;
- mechanism or evidence payload;
- strongest licensed conclusion;
- handoff to the next paragraph.

Ask: Why must it exist? What does it add? What prerequisite does it create?
What breaks if deleted? Split mixed roles; merge duplicated roles.

For each sentence:

1. identify subject, action, object, and claim;
2. put concrete mechanism or failure before its abstract label;
3. use examples only when they perform reasoning;
4. use a connector only when the relation is real;
5. split role assignment from multi-step operation when overloaded;
6. stop after a complete explanation;
7. calibrate the verb to evidence.

## Method algorithm

1. Keep Preliminaries minimal.
2. Make Overview a component/dependency map.
3. Introduce symbols just in time and maintain a global symbol table.
4. Use motivation/connection → formula → immediate explanation → behavior.
5. Make one formula perform one logical action.
6. Define the ideal objective before an approximation.
7. State branch roles, shared and different state, update/fusion order, output.
8. Specify stopping, tie-breaking, budget, and fallback when method-defining.
9. Move implementation-only hyperparameters and results elsewhere.
10. Audit Method, Introduction summary, algorithm, and framework figure jointly.

## Figure and table algorithm

Inspect the rendered asset, not only LaTeX:

- state the figure/table's purpose in the first sentence;
- map panels, rows, columns, stages, and reading order;
- explain setup, metric, statistic, uncertainty, and visual encodings;
- report only observations licensed by the asset;
- match active terminology and symbols exactly;
- check legibility and whitespace at final scale.

A caption should be self-contained enough for local interpretation, not a
miniature Results section or a list of labels.

## Output contract

Return only what the task needs. For substantive revision, provide:

1. diagnosis at the highest failing level;
2. revised text;
3. semantic changes and their reasons;
4. claim, terminology, or evidence risks;
5. unresolved decisions requiring the user.

For candidate comparison, include the selected version and rejected-version
failures. For file-based work, preserve version history and do not silently
overwrite confirmed sources.

## Quality gates

Before delivery:

- the paper's core problem is expressible in one sentence;
- the gap is real and the method directly addresses it;
- each paragraph has a unique role and advances the story;
- experiments test the headline claims and method components;
- claim verbs match evidence and scope;
- core terms, method/component names, metrics, and symbols are stable;
- figures and tables agree with the main text and remain readable when rendered;
- labels, citations, equations, and references resolve;
- prose contains no unsupported causality, generic praise, or redundant ending.

Use [CORE_SECTION_CHECKLISTS.md](06_checklists/CORE_SECTION_CHECKLISTS.md),
[CROSS_SECTION_CHECKLIST.md](06_checklists/CROSS_SECTION_CHECKLIST.md), and
[LATEX_AND_REVIEWER_CHECKLIST.md](06_checklists/LATEX_AND_REVIEWER_CHECKLIST.md).
Before standalone distribution, run
`python scripts/validate_self_contained.py` from this folder.

## Ask the user only when necessary

Ask when a choice would change:

- central problem, gap, or scientific interpretation;
- claim strength or scope;
- method semantics or formula;
- official name or terminology;
- acceptance of an unsupported assumption;
- selection between genuinely different paper stories.

Modify autonomously when fixing grammar, punctuation, clear referents,
meaning-preserving redundancy, formatting, nonbreaking citations, and obvious
symbol/caption inconsistencies. State assumptions that could affect science.

## Common failure modes

Avoid:

- sentence polish before story repair;
- Abstract as background essay or component list;
- Introduction as Abstract copy or Related Work inventory;
- evidence figures introduced after their conclusion;
- Method as implementation narration or notation theater;
- experiments narrated by table order;
- captions that merely repeat visible labels;
- rigid word/paragraph/number bans detached from venue and purpose;
- treating one project-specific choice as a universal preference.

Read [ANTI_PATTERNS.md](00_foundations/ANTI_PATTERNS.md) for diagnostics.

## Templates, examples, and provenance

- [TEMPLATE_LIBRARY.md](03_templates/TEMPLATE_LIBRARY.md)
- [DECISION_CASEBOOK.md](04_examples/DECISION_CASEBOOK.md)
- [MERGE_PROVENANCE.md](05_provenance/MERGE_PROVENANCE.md)
- [EVIDENCE_POLICY.md](05_provenance/EVIDENCE_POLICY.md)
- [DECISION_LEDGER.md](05_provenance/DECISION_LEDGER.md)
- [RULE_EVIDENCE_MATRIX.md](05_provenance/RULE_EVIDENCE_MATRIX.md)
- [PROJECT_SPECIFIC_VS_GENERAL.md](05_provenance/PROJECT_SPECIFIC_VS_GENERAL.md)

Do not seek a sibling source Skill or original project unless the user
explicitly supplies it for a new evidence audit. This folder is the complete
runtime boundary.
