# Merge Provenance

## Historical source snapshot

The following records document the synthesis origin only. They are not runtime
dependencies and are not required when this folder is distributed alone.

| Source | Role | Files | Bytes | Pre-merge tree SHA-256 |
|---|---|---:|---:|---|
| `skill_gpt` | authoritative evidence-grounded base | 67 | 888,433 | `a80aff341d63397cf8522cc2096a132322e20428aafc3144f0674b1231d05562` |
| `skill_qwen` | supplementary execution heuristics | 5 | 64,963 | `b26cb1193a7c2a24754eb2cfdff4a88bcf536454e35124a18865ffec0353aa4b` |
| `skill_qwen38_from_gpt` | supplementary templates/checklists | 49 | 229,582 | `411ac8624026655bf78119b32c4a8d71232ab285daa69d759ece6d41272bed53` |

Tree hash is computed over sorted relative path plus file bytes.

## Retained from `skill_gpt`

- evidence classification and user-preference hierarchy;
- one-story/multiple-resolution model;
- top-down revision levels;
- semantic candidate comparison;
- claim calibration;
- adaptive Abstract, Introduction, Method, and Figure Caption algorithms;
- notation and branch-state audits;
- provisional status for secondary sections;
- cross-domain rather than CAPD-specific transfer.

## Added from `skill_qwen`

- explicit incremental loop: componentize → revise one unit → assemble →
  compress → notation audit;
- user-feedback mapping and rule-distillation protocol;
- distinction among confirmed, canonical, and synchronized states;
- master-record maintenance for long projects;
- information deletion/replacement tests;
- explicit Abstract-to-Introduction functional expansion;
- panel evidence-boundary and framework-flow audits.

## Added from `skill_qwen38_from_gpt`

- compact experiment, caption, Method, and decision templates;
- stronger cross-section and anti-pattern check coverage;
- problem-driven experiment organization;
- reproducibility and reviewer-attack prompts.

## Rejected or softened

- fixed Abstract/Introduction word counts and paragraph counts;
- universal ban on numbers or model names in Abstract/Introduction;
- fixed CAPD panel/component order;
- exact lexical handoff rules;
- mechanical claim strength based only on dataset/model counts;
- blanket replacement of words such as `show`;
- invented or unverified candidate examples as user evidence;
- universal requirements to bold best and underline second-best results;
- exact sentence-length and paragraph-length lints.

These can be local venue or project constraints, but are not stable global
preferences.

## Architecture and distribution decision

The merged Skill is intentionally smaller than the sum of its sources. It uses
progressive disclosure and removes duplicated raw forensic artifacts. All
runtime knowledge and the decision/rule evidence needed to interpret it are
bundled in:

- `DECISION_LEDGER.md`;
- `RULE_EVIDENCE_MATRIX.md`;
- `PROJECT_SPECIFIC_VS_GENERAL.md`;
- `EVIDENCE_POLICY.md`.

No sibling directory, original manuscript, log, PDF, or network resource is
required to apply this Skill. Historical source names and hashes above serve
only as non-operational provenance.
