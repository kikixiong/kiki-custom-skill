# Paper Triage Rubric

Score before deep reading. Use 1 to 5 unless stated otherwise.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Quant Transfer | No market analogue | Plausible but indirect | Direct alpha/model/risk use |
| Data Feasibility | Unavailable or future-looking | Available with careful joins | Standard point-in-time data |
| Novel Mechanism | Benchmark tuning | Useful module or objective | New mechanism worth testing |
| Robustness Value | Ignores nonstationarity | Some robustness claim | Directly handles shift/noise/tails |
| Engineering Cost | Weeks or major infra | Several days | One small experiment |
| Leakage Risk | Severe risk | Manageable with checks | Low if implemented carefully |

For `Leakage Risk`, 5 means low risk and 1 means severe risk.

## Weighted Score

Use this rough score when ranking papers:

```text
score =
  2.0 * Quant Transfer
+ 1.5 * Data Feasibility
+ 1.5 * Novel Mechanism
+ 1.5 * Robustness Value
+ 1.0 * Engineering Cost
+ 2.0 * Leakage Risk
```

Maximum is 47.5.

## Decision Rules

- `Implement candidate`: score >= 38 and no dimension below 3.
- `Deep read`: score >= 32 or Novel Mechanism >= 5.
- `Park`: score 24-31, or high mechanism but weak data feasibility.
- `Reject`: score < 24, severe leakage, no falsifiable experiment, or benchmark-only contribution.

## Red Flags

- Uses random train/test split on temporal data.
- Predicts future labels using features computed from the full sequence.
- Uses current index constituents for historical universe.
- Reports only MSE/MAE without trading-aware evaluation.
- Ignores turnover, costs, liquidity, and capacity.
- Claims financial prediction but uses tiny, non-representative datasets.
- Compares against weak baselines while avoiding simple factor or rank baselines.
