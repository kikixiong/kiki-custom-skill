# Experiment Design Template

Use this before implementing a paper-derived idea.

## Idea

- Source paper:
- Mechanism:
- Market analogue:
- Prediction target:
- Asset scope:
- Horizon:

## Data Contract

- Universe:
- Date range:
- Frequency:
- Required fields:
- Point-in-time timestamp for each field:
- Corporate action or futures roll policy:
- Missing data policy:
- Tradability filters:

## Baselines

Include at least:

- naive or historical baseline
- existing factor baseline
- simple linear/rank model
- current production or strongest local baseline if available

## Split Design

- Train/validation/test periods:
- Walk-forward schedule:
- Regime slices:
- Cross-sectional grouping:
- Purging or embargo if labels overlap:

## Metrics

Prediction:

- IC / RankIC
- hit rate
- calibration or uncertainty quality if applicable

Portfolio proxy:

- quantile spread
- turnover
- cost-adjusted return
- max drawdown
- exposure drift

## Acceptance Criteria

Define before running:

- minimum improvement over baseline:
- robustness requirement:
- maximum allowed turnover or cost drag:
- required consistency across regimes:

## Kill Criteria

Stop or pivot if:

- signal vanishes after point-in-time correction
- improvement exists only in one regime or one asset group
- performance is explained by sector, beta, liquidity, or size exposure
- turnover or cost overwhelms alpha
- result is not stable under walk-forward validation
