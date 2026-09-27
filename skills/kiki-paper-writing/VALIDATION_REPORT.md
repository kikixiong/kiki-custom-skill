# Validation Report

## Scope

Forward-test the consolidated Skill on three tasks unlike the source CAPD
project. The goal is routing and decision quality, not producing full papers.

## Test 1: Multimodal medical retrieval paper from an idea

**Input**

Sparse idea: retrieval errors arise when visually similar findings have
different clinical context; method uses region-text alignment and calibrated
hard negatives; one evidence figure and preliminary results.

**Expected routing**

`FROM_ZERO` → story/claim ledgers → Abstract → Introduction/Figure Caption →
Method.

**Result**

- Story model distinguishes visual similarity failure from contextual gap.
- Abstract slots cover both alignment and calibrated negatives without turning
  them into a module list.
- Figure Caption algorithm asks for cohort, comparison, metric, and panel
  inference.
- Method template adapts to training objectives; it does not require reference
  versus full-prompt branches.

**Status:** Pass.

## Test 2: General ML paper with two candidate Introductions

**Input**

An optimization paper compares a smooth but broad version claiming universal
convergence with a more precise version limited to weakly convex objectives.

**Expected routing**

`COMPARE_MULTIPLE_VERSIONS` plus Claim Calibration.

**Result**

- Lexicographic comparison selects scoped accuracy over fluency.
- It requests theorem assumptions before licensing `guarantees`.
- It audits paragraph role and downstream theorem/experiment consistency.
- No image-generation terminology or fixed six-paragraph structure is invoked.

**Status:** Pass.

## Test 3: Systems paper under iterative revision

**Input**

A distributed scheduler paper has confirmed paragraphs, an unsynchronized
canonical file, and feedback that a safe-baseline/optimized-plan comparison is
ambiguous.

**Expected routing**

`ITERATIVE_VERSIONING_AND_FEEDBACK` → Method multi-branch audit → global
assembly.

**Result**

- Confirmed, canonical, and synchronized states remain distinct.
- The branch audit transfers to shared workload state, branch-specific
  information, decision time, and one executed plan.
- Master-record protocol prevents stale assembly.
- Reviewer audit asks whether gains arise from extra compute.

**Status:** Pass.

## Anti-overfitting checks

- Fixed Abstract word/sentence counts: absent.
- Fixed Introduction paragraph count: absent.
- Universal ban on numbers or model names: absent.
- CAPD component/panel order as template: absent.
- Generative decoding assumed for all methods: absent.
- Formula-first Method mandated: absent.
- Provisional secondary guidance marked: present.

## Issues found and resolved during synthesis

1. Supplementary “no numbers in Introduction” was converted to a
   purpose-dependent density rule.
2. Exact word/paragraph limits were removed from quality gates.
3. Formula-driven Method language was balanced with a plain-language clarity
   test.
4. Caption rules were separated by evidence, framework, and result figures.
5. Version confirmation and manuscript synchronization were separated.
6. Unverified supplementary examples were not treated as user evidence.

## Validation summary

| Check | Result |
|---|---|
| Skill Creator structural validation | Pass |
| `SKILL.md` under 500 lines | Pass (297) |
| Local Markdown links | Pass (0 broken) |
| Links escaping Skill root | Pass (0) |
| External URI/local absolute-path dependency | Pass (0) |
| Bundled decision evidence | Pass (28 decisions) |
| Bundled rule evidence | Pass (48 rules) |
| YAML parsing | Pass |
| Placeholder-marker scan | Pass |
| Three cross-domain dry runs | Pass |
| Standalone validator | Pass (`scripts/validate_self_contained.py`) |
| Isolated distribution test with no sibling source folders | Pass |

The validation boundary is the `skill_paper_writing` directory itself. No
sibling Skill, original paper project, historical log, PDF, or network resource
is required at runtime.
