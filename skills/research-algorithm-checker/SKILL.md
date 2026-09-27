---
name: research-algorithm-checker
description: 对照算法或论文检查实现、张量形状、数值逻辑、边界和性能。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Research Algorithm Checker

Use this for rigorous research-code correctness review.

## Review Lanes

Check the implementation from five angles:

- algorithm flow and data path
- boundary cases, dtype, shape, indexing, and missing values
- numerical correctness, objectives, gradients, probabilities, and thresholds
- performance, memory, caching, and avoidable recomputation
- consistency against paper, pseudo-code, configs, or design notes

## Procedure

1. Locate the entry point and target files.
2. Read in small logical blocks and restate what each block does.
3. Compare each block with expected algorithm behavior.
4. Record concrete issues with file and line references.
5. Classify issues into bug, correctness risk, performance risk, missing test, or unclear assumption.
6. If editing is requested or clearly needed, implement minimal fixes and verify.

## Issue Tracking

When a project root is clear, maintain `ISSUES.md` with:

- Todo
- Doing
- Done
- Discarded

Respect discarded ideas so the same weak optimization is not re-proposed repeatedly.

## Codex Rules

- Do not require exact trigger phrases.
- Do not auto-commit or push unless explicitly requested.
- Prefer tests or smoke checks that prove the reviewed behavior.
- Report unresolved assumptions instead of presenting guesses as confirmed.
