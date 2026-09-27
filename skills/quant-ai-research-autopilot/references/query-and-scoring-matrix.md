# Query And Scoring Matrix

Use this when designing live paper searches and ranking candidates.

## Query Families

Recent AI time-series:

- `"time series foundation model" finance`
- `"self-supervised time series" "stock return prediction"`
- `"masked time series modeling" "financial time series"`
- `"Mamba" "time series forecasting" finance`
- `"state space model" "financial time series"`
- `"long context" "time series forecasting" "stock"`

Cross-sectional and ranking:

- `"learning to rank" "stock return prediction"`
- `"cross-sectional return prediction" "deep learning"`
- `"multi-factor" "transformer" "stock"`
- `"tabular deep learning" "alpha factor"`

Graph and relational:

- `"graph neural network" "stock prediction"`
- `"lead-lag" "financial time series" "deep learning"`
- `"supply chain" "stock prediction" graph`
- `"sector relation" "stock return prediction"`

Robustness and shift:

- `"distribution shift" "financial time series"`
- `"regime adaptation" "stock prediction"`
- `"online learning" "financial time series" "deep learning"`
- `"uncertainty calibration" "stock prediction"`

Microstructure and execution:

- `"limit order book" "self-supervised learning"`
- `"market microstructure" "transformer"`
- `"execution cost" "deep learning" "forecasting"`

Venue filters:

- `site:openreview.net`
- `site:arxiv.org`
- `site:proceedings.mlr.press`
- `site:dl.acm.org ICAIF`
- `site:ssrn.com "machine learning" "asset pricing"`

## Paper Score

Score each dimension 1-5:

- `quant_transfer`: maps to alpha, risk, portfolio, or execution.
- `data_feasibility`: required data is point-in-time and accessible.
- `novel_mechanism`: more than a generic bigger-model benchmark.
- `robustness_value`: helps nonstationarity, noisy labels, regimes, tails, or calibration.
- `engineering_cost`: can be tested quickly.
- `leakage_risk`: low score means likely leakage; high score means clean protocol is plausible.

Suggested weighted score:

`2*quant_transfer + 1.5*data_feasibility + 1.5*novel_mechanism + 1.5*robustness_value + engineering_cost + 2*leakage_risk`

Actions:

- `Implement candidate`: score >= 38 and all dimensions >= 3.
- `Deep read`: score >= 32 or novel mechanism is 5.
- `Park`: score >= 24, but weak transfer or high cost.
- `Reject`: severe leakage, weak market analogue, or no feasible data contract.

## Idea Score

Rank ideas using:

- `first_test_speed`: can produce a falsifying result in days.
- `evidence_delta`: likely to beat a simple baseline after costs.
- `paper_novelty`: defensible delta from closest papers.
- `market_realism`: handles tradability, costs, liquidity, and capacity.
- `paper_story`: can become a clean paper contribution if it works.

Prefer ideas with one strong core claim over wide systems with many moving parts.
