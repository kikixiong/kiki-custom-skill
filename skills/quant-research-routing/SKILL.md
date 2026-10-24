---
name: quant-research-routing
description: 把量化研究请求分派到因子、回测、数据或组合分析流程。
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

# Quant Research Routing

Use this as the first skill for quant tasks. Pick the more specific workflow after reading the request and local files.

## Route

- Factor or alpha idea, signal construction, IC, neutralization, decay, turnover: use `factor-alpha-lab`.
- Broad AI + Quant research, paper-to-alpha idea mining, or "帮我找 AI 量化 idea": use `quant-ai-research-autopilot` first.
- Narrow AI/ML paper search, top-conference time-series papers, literature triage, or one-paper deep reads: use `quant-ai-paper-scout`.
- Existing candidate idea worth, scope, feasibility, or reviewer value: use `idea-evaluator`, then `novelty-check` if collision risk matters.
- Backtest result, performance table, strategy claim, leakage suspicion, overfit concern: use `backtest-integrity-audit`.
- Position book, portfolio construction, risk exposure, drawdown, attribution, constraints: use `portfolio-risk-attribution`.
- Data pipeline, corporate actions, futures rolls, point-in-time data, vendor files, cleaning: use `quant-data-pipeline-audit`.
- JoinQuant-specific APIs, research notebooks, backtest scripts, jqdata style code: use `joinquant-research-workflow`.

## AI Quant Research Defaults

For broad "AI + Quant" requests, default to this sequence:

1. Start with `quant-ai-research-autopilot`, unless the request is clearly only a single paper lookup or a plain factor/backtest task.
2. Retrieve papers through `quant-ai-paper-scout` with live search when the user asks for recent, latest, this year, or venue-specific papers.
3. Translate papers into falsifiable market analogues: mechanism, predictive target, data contract, validation metric, and failure mode.
4. Rank ideas by point-in-time feasibility, novelty, expected implementation cost, leakage risk, and tradability.
5. Hand off only the strongest candidates to `factor-alpha-lab`, `experiment-plan`, or `research-code-autopilot`.

Prefer paper-derived `Idea Backlog` or `Experiment Card` artifacts over generic brainstorming.

## Operating Principles

- Treat live trading and allocation decisions as high-stakes. Provide research analysis, checks, and code; do not issue live trade instructions unless the user explicitly asks and the required data is available.
- Separate predictive validity from tradability: signal quality, costs, capacity, slippage, turnover, borrow/short constraints, liquidity, and operational risk are different checks.
- Always ask "what data timestamp did the strategy know at decision time?"
- For China A-share work, watch for ST status, suspension, limit up/down, survivorship, index membership timing, announcement timing, and T+1 constraints.
- Prefer robust evidence over single backtest curves: out-of-sample, walk-forward, grouped time splits, market-regime slices, and cost sensitivity.

## Default Report Shape

For a broad quant request, return:

- task classification
- data and universe assumptions
- highest-risk bias or failure mode
- concrete next analysis or code action
- validation metric and output artifact
