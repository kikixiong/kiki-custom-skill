# Quant AI Research Autopilot Playbook

Use this playbook for broad AI + Quant research tasks where the user wants a direction, paper radar, or executable research plan.

## Loop

1. Classify the request:
   - `scout`: find current papers and directions.
   - `deep-read`: understand one paper and attack its quant transfer.
   - `idea-evaluate`: judge one candidate idea.
   - `novelty`: find closest prior work.
   - `experiment`: turn an idea into a falsifiable test.
   - `validate`: inspect factor/backtest/research-code evidence.
2. Retrieve evidence:
   - Use live search for latest, recent, this year, venue, OpenReview, arXiv, or citation-sensitive requests.
   - Prefer arXiv/OpenReview/proceedings/Semantic Scholar/publisher pages.
   - Keep URLs or IDs for every paper that affects a decision.
3. Translate mechanisms:
   - AI mechanism -> market analogue -> target -> data contract -> test -> kill criterion.
   - Do not keep papers that only improve generic benchmarks without a credible market analogue.
4. Rank:
   - Prioritize high transfer, feasible point-in-time data, clear novelty delta, low implementation cost, and low leakage risk.
5. Hand off:
   - `quant-ai-paper-scout` for radar/deep reads.
   - `idea-evaluator` for whether to pursue.
   - `novelty-check` for collision risk.
   - `experiment-plan` for experiment cards.
   - `factor-alpha-lab` for signal-level validation.
   - `backtest-integrity-audit` before trusting performance.

## Stop Criteria

Stop scouting when one of these is true:

- Three implementable candidates exist with paper evidence and kill criteria.
- One candidate is clearly dominant and ready for an experiment card.
- The search shows the direction is crowded or weakly transferable, and a pivot is more valuable.

## Red Flags

- Uses future labels, revised fundamentals, or future universe membership.
- Reports benchmark forecast error but no realistic trading protocol.
- Requires unavailable alternative data or non-point-in-time metadata.
- Needs months of engineering before the first falsification.
- Only says "use a bigger model" without a mechanism that maps to a market failure mode.
