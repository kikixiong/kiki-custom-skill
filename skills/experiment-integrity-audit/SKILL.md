---
name: experiment-integrity-audit
description: 检查数据泄漏、划分、基线公平性、指标、统计与可复现性。
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

# Experiment Integrity Audit

Use this skill when the question is whether results can be trusted.

## Audit Order

1. Dataset and split integrity:
   - train/val/test separation
   - subject-level or group-level split when needed
   - duplicate samples, near duplicates, cached features from wrong split
   - labels available only at allowed time

2. Baseline fairness:
   - same data, same budget, same preprocessing
   - no hidden extra supervision
   - majority/random/simple heuristic baselines where label skew exists

3. Metric correctness:
   - correct direction, averaging, sample weights, macro/micro choice
   - confidence intervals or seed variance for stochastic results
   - per-class/per-group metrics when aggregate scores can hide failure

4. Reproducibility:
   - exact command, config, commit, seed, environment
   - output paths and immutable summaries
   - regenerated figures/tables from source data

5. Claim discipline:
   - mark unsupported claims
   - separate pilot evidence from full benchmark evidence
   - list negative results if they matter for interpretation

## Useful Checks

Use project-local scripts first. If none exist, add narrow audit scripts that write JSON/CSV summaries and can be rerun.

Prefer checks like:

- split overlap by ID and hash
- missing-feature audit
- label distribution by split
- metric recomputation from raw predictions
- bootstrap confidence interval
- seed aggregation
- table-to-source consistency

## Output Standard

Lead with findings ordered by severity. Use file paths, line references, artifact paths, and exact numbers when available.

Do not merely say "looks good"; state what was checked and what remains unchecked.
