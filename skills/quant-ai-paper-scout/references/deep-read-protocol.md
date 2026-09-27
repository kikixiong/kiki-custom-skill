# Deep Read Protocol

Use this when a paper passes first triage or the user explicitly asks to read one paper deeply.

## Pass 1: Triage

Answer quickly:

- What problem does the paper actually solve?
- Is the contribution a new mechanism, new training recipe, new dataset, or benchmark result?
- Does the paper have any plausible market analogue?
- Is there code or enough detail to reproduce the core idea?
- Should this be `Deep read`, `Implement candidate`, `Park`, or `Reject`?

## Pass 2: Mechanism

Extract the irreducible technical idea:

- input representation
- model architecture or factor construction
- training objective
- sampling strategy
- target label
- loss function
- evaluation split
- baseline set
- claimed reason it works

Do not accept the authors' framing until the mechanism is restated in simpler terms.

## Pass 3: Quant Translation

Translate with this chain:

```text
paper task -> market analogue -> point-in-time data -> prediction horizon -> tradable decision -> validation design
```

Required checks:

- Could the feature be known before the trade decision?
- Does the paper's target correspond to returns, ranking, volatility, liquidity, risk, or execution?
- Would the method improve IC, RankIC, turnover, drawdown, cost-adjusted return, or robustness?
- Is the effect likely cross-sectional, time-series, or portfolio-level?
- What simple baseline would embarrass the method if it fails?

## Adversarial Questions

- Is the paper using future context that a trading system would not have?
- Does it rely on random splits for temporal data?
- Are benchmarks weak or mismatched?
- Does lower forecasting error necessarily imply better portfolio value?
- Would transaction costs erase the expected benefit?
- Is the method robust to regime change or only benchmark-specific?

## Output

Return:

1. one-sentence verdict
2. mechanism summary
3. quant translation
4. leakage/tradability audit
5. derived ideas
6. minimal experiment
7. kill criteria
