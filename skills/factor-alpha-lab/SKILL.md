---
name: factor-alpha-lab
description: 研究因子与信号，分析 IC、衰减、换手和中性化。
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

# Factor Alpha Lab

Use this skill for factor research from idea to evidence.

## Research Flow

1. Define the factor:
   - economic intuition or behavioral rationale
   - exact data fields and timestamp availability
   - universe, rebalance frequency, holding horizon
   - transformation: winsorization, normalization, industry/size neutralization

2. Validate raw signal:
   - coverage by date and universe
   - missingness and outliers
   - autocorrelation and decay
   - cross-sectional distribution by sector/market-cap bucket

3. Predictive tests:
   - IC and RankIC by date
   - mean, std, t-stat, hit rate, IR
   - quantile spread returns
   - monotonicity across quantiles
   - horizon curve and decay curve

4. Robustness:
   - time-period slices
   - bull/bear/sideways market regimes
   - sector-neutral and size-neutral variants
   - alternative winsorization and z-score methods
   - liquidity and tradability filters
   - transaction-cost sensitivity

5. Combination readiness:
   - correlation to existing factor library
   - incremental IC after orthogonalization
   - turnover contribution
   - capacity impact

## Coding Rules

- Use point-in-time data and lag accounting.
- Keep factor values, forward returns, and membership masks separately auditable.
- Save factor diagnostics as CSV/Parquet plus a compact Markdown summary.
- Never infer annualized performance from a tiny sample without labeling it.

## Minimum Evidence

For a factor claim, include:

- universe and dates
- rebalance/holding horizon
- IC mean, t-stat, hit rate
- long-short or quantile spread with cost assumption
- turnover
- worst regime or failure slice
