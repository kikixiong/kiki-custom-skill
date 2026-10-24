---
name: quant-data-pipeline-audit
description: 检查行情、基本面、特征和时点一致性等量化数据管线。
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

# Quant Data Pipeline Audit

Use this skill when correctness of data construction is the main risk.

## Data Contract

For each dataset, establish:

- identifier schema: ticker, exchange, security ID, contract ID
- timestamp fields: event time, announcement time, effective time, ingestion time
- frequency: tick, minute, daily, monthly, quarterly
- adjustment policy: raw, forward-adjusted, backward-adjusted, total-return
- universe membership and delisting policy
- missing value policy

## Common Failure Modes

- using report period date instead of announcement date
- mixing adjusted and unadjusted prices
- silent ticker reuse or symbol changes
- survivorship bias from current constituent lists
- futures continuous contract roll leakage
- timezone/calendar mismatch
- vendor restatements changing historical values without versioning
- joining on calendar dates when market close times differ

## Audit Steps

1. Trace one sample row from raw source to feature output.
2. Verify keys are unique at the intended granularity.
3. Check date monotonicity and unexpected future timestamps.
4. Measure missingness by date, universe, sector, and source.
5. Compare random securities against raw files or vendor snapshots.
6. Confirm downstream factor/backtest code consumes the correct lagged version.

## Artifacts

Prefer deterministic audit outputs:

- schema summary
- row counts by date/source
- duplicate-key report
- missingness heatmap/table
- point-in-time join audit
- adjustment sanity checks

If a pipeline cannot prove timestamp availability, label downstream backtests as untrusted.
