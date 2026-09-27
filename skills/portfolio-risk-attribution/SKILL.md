---
name: portfolio-risk-attribution
description: 分析投资组合风险、暴露、收益归因和约束。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Portfolio Risk Attribution

Use this skill when the object is a portfolio or book, not just a single signal.

## Analysis Flow

1. Identify inputs:
   - positions or target weights
   - prices/returns
   - benchmark
   - sector/industry classification
   - style/factor exposures
   - constraints and rebalance schedule

2. Exposure checks:
   - gross/net exposure
   - beta and benchmark active exposure
   - industry/sector active weights
   - size, value, momentum, volatility, liquidity, quality exposure
   - single-name and group concentration

3. Performance attribution:
   - allocation versus selection if classification data exists
   - factor contribution versus idiosyncratic contribution
   - top contributors and detractors
   - turnover and cost drag
   - long/short or active/passive decomposition

4. Risk:
   - volatility, drawdown, drawdown duration
   - downside volatility, VaR/CVaR if appropriate
   - stress periods and scenario shocks
   - liquidity and capacity

5. Optimization sanity:
   - objective and constraints are explicit
   - covariance estimate is stable
   - weights are not dominated by estimation noise
   - constraints match trading reality
   - turnover penalty is tested

## Output Standard

Return tables or scripts that make the book explainable:

- exposures by date
- active weights by sector/style
- daily attribution
- drawdown-period attribution
- risk summary and constraint violations

Do not reduce portfolio health to Sharpe alone.
