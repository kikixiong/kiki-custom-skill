---
name: backtest-integrity-audit
description: 检查回测中的数据泄漏、未来信息、过拟合、成本与样本外验证。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Backtest Integrity Audit

Use this skill before trusting any strategy result.

## Critical Checks

1. Time alignment:
   - Features are known before the trade decision.
   - Labels/forward returns are never merged into features.
   - Financial statements use announcement dates, not report period dates.
   - Index membership and ST/suspension status are point-in-time.

2. Universe and tradability:
   - survivorship-free universe
   - delisted securities handled
   - suspensions and limit up/down constraints
   - volume/liquidity filters
   - T+1 and lot size rules when relevant

3. Costs and execution:
   - commission, stamp duty, slippage, bid-ask spread
   - turnover and rebalance frequency
   - capacity and market impact sensitivity
   - close-to-close versus next-open execution assumptions

4. Statistical robustness:
   - train/validation/test split by time
   - walk-forward or purged split for hyperparameters
   - multiple seed/config sensitivity
   - benchmark and simple baseline
   - regime and sector slices

5. Reporting:
   - CAGR/annual return, volatility, Sharpe, Calmar, max drawdown
   - turnover, average holding period, win/loss, exposure
   - drawdown duration and tail periods
   - cost sensitivity table

## Audit Output

Lead with issues by severity:

- `Blocker`: invalidates the backtest.
- `Major`: likely changes conclusions.
- `Medium`: needs quantification.
- `Minor`: presentation or reproducibility gap.

Include exact file paths, line references, and artifact names where possible.

## When Editing Code

- Add assertions around time alignment and split boundaries.
- Make cost/slippage assumptions explicit CLI/config parameters.
- Save raw trades and daily positions; performance summaries alone are insufficient.
- Recompute metrics from raw positions/trades when auditing.
