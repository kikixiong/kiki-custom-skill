# Search Query Matrix

Use these query families for paper scouting. Combine method terms with quant-transfer terms and venue filters.

## Method Terms

- `"time series foundation model"`
- `"time series representation learning"`
- `"self-supervised time series"`
- `"masked time series modeling"`
- `"contrastive learning" "time series"`
- `"long horizon time series forecasting"`
- `"state space model" "time series"`
- `"Mamba" "time series"`
- `"Transformer" "time series forecasting"`
- `"diffusion" "time series forecasting"`
- `"graph neural network" "time series forecasting"`
- `"learning to rank" "time series"`
- `"distribution shift" "time series"`
- `"domain adaptation" "time series"`
- `"online learning" "nonstationary time series"`
- `"calibration" "time series forecasting"`
- `"uncertainty estimation" "time series forecasting"`

## Quant Transfer Terms

- `"stock prediction"`
- `"stock return prediction"`
- `"financial time series"`
- `"futures prediction"`
- `"market microstructure"`
- `"limit order book"`
- `"alpha factor"`
- `"portfolio construction"`
- `"cross-sectional return"`
- `"learning to rank" "finance"`
- `"regime shift" "financial markets"`
- `"lead-lag" "financial"`

## Venue Filters

- `site:openreview.net ICLR time series`
- `site:openreview.net NeurIPS time series`
- `site:proceedings.mlr.press ICML time series`
- `site:kdd.org KDD financial time series`
- `site:arxiv.org "time series foundation model"`
- `site:arxiv.org q-fin "stock prediction"`

## Boolean Patterns

Use these as templates:

```text
("time series foundation model" OR "masked time series modeling") AND ("financial time series" OR "stock prediction" OR "futures")
```

```text
("distribution shift" OR "domain adaptation" OR "online learning") AND ("time series" OR "sequential data") AND ("forecasting" OR "prediction")
```

```text
("graph neural network" OR "cross-variable attention" OR "relational learning") AND ("financial time series" OR "stock return prediction" OR "lead-lag")
```

```text
("learning to rank" OR "ranking loss" OR "listwise") AND ("stock" OR "cross-sectional return" OR "portfolio")
```

## Query Rotation

For weekly scanning, use three passes:

1. `Broad novelty`: method terms only, filtered by recent date or venue.
2. `Finance transfer`: method terms plus quant transfer terms.
3. `Evaluation integrity`: leakage, distribution shift, OOD, backtest, benchmark, reproducibility.
