---
name: top-survey-workflow
description: 规划面向高水平期刊的综述，构建分类体系与批判性综合。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
disable-model-invocation: true
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Top Survey Workflow

Use this skill when the user wants a survey, review article, tutorial review, or state-of-the-art synthesis that must clear a high editorial bar.

This workflow is designed for venues such as ACM Computing Surveys and comparable top journals. It does not promise acceptance. It does enforce the work needed to make acceptance plausible.

Use [acm-csur-heuristics.md](references/acm-csur-heuristics.md) when pressure-testing whether the draft feels like a top-journal survey instead of a long reading note.

## What Good Looks Like

A strong top-journal survey usually has all of these:

- A sharp scope, not a vague mega-topic
- A defensible taxonomy or organizing framework that feels better than a chronological summary
- Broad coverage with explicit inclusion logic
- Critical synthesis, not just paper-by-paper description
- Clear articulation of tensions, blind spots, and open problems
- High-quality figures and comparison tables that make the paper useful as an entry point for the field
- A polished abstract, introduction, and conclusion that state why this survey had to be written now

## Default Stack

Prefer these installed skills in this order:

- Discovery and corpus building: `af-paper-lookup`, `af-citation-management`, `af-literature-review`
- Drafting and synthesis: `kiki-paper-writing`, `af-scientific-writing`; use `kiki-paper-workflow` for an explicitly selected full Kiki Custom chain
- Critical pressure-testing: `af-peer-review`, `af-scientific-critical-thinking`, `paper-review`
- Venue fit and packaging: `af-venue-templates`, `pdf`
- Figure and table work: `af-academic-plotting`, `af-markdown-mermaid-writing`
- Chinese-source polishing when needed: `af-humanizer-zh`, `af-paper-polish-workflow`

## Workflow

### Phase 1: Viability

Before drafting, answer:

1. Why this topic now?
2. Why a survey instead of a regular paper?
3. What will readers learn from this paper that existing surveys do not already provide?
4. Is the contribution a taxonomy, a benchmark-style comparison frame, a historical synthesis, or a forward-looking agenda?

If these answers are weak, the survey is not yet top-journal ready.

### Phase 2: Corpus

Build a paper pool with explicit rules:

- search queries
- time span
- core venues and archives
- inclusion/exclusion rules
- canonical seed papers
- recent surveys that overlap and must be differentiated

Deliverables:

- search log
- screened paper list
- grouped bibliography
- gap list describing what prior surveys missed

### Phase 3: Taxonomy

Do not start body writing before the organizing frame is stable.

Choose one primary structure:

- task/problem taxonomy
- method taxonomy
- pipeline/lifecycle taxonomy
- evidence-level taxonomy
- systems-stack taxonomy
- debate/tension map

The taxonomy must survive contact with edge cases. If too many major papers do not fit cleanly, redesign it.

### Phase 4: Core Synthesis

Write sections that do more than summarize.

Each major section should answer:

- what this sub-area is trying to solve
- what the dominant approaches are
- where the evidence is strong
- where comparisons are unfair or incomplete
- what assumptions keep recurring
- what remains unresolved

Prefer cross-paper comparisons and explicit contrasts over isolated mini-summaries.

### Phase 5: Figures And Tables

At minimum, plan:

- one overview figure for the taxonomy
- one comparison table across representative methods or systems
- one future-directions or open-problems figure/table

For strong submissions, figures should carry part of the argument, not just decorate it.

### Phase 6: Internal Review

Run at least three distinct checks:

- reviewer-style critique: `af-peer-review`
- rigor and evidence critique: `af-scientific-critical-thinking`
- claim-evidence and structure critique: `paper-review`

Do not treat favorable first-pass feedback as enough.

### Phase 7: Submission Readiness

Before venue targeting, verify:

- title is precise and credible
- abstract states scope, framework, and contribution clearly
- introduction explains why prior surveys are insufficient
- conclusion does more than repeat sections
- references are consistent and complete
- figures are publication-ready
- venue-specific formatting is already aligned

## Operating Rules

- Prefer one stable outline and iterate it, rather than repeatedly reinventing the structure.
- Maintain a living table of papers, tags, key claims, evidence type, limitations, and where each paper appears in the survey.
- Every time a new paper enters the corpus, test whether it breaks the taxonomy.
- If you cannot state the survey's novel contribution in 2-3 sentences, the scope is still weak.

## First Move

Start by producing a survey viability brief with:

1. target venue
2. candidate title
3. scope boundaries
4. novelty against existing surveys
5. proposed taxonomy
6. first-pass corpus plan

Then proceed to corpus construction before drafting long prose.
