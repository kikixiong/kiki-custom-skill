---
name: joinquant-research-workflow
description: 面向聚宽 API 和回测脚本的研究工作流。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# JoinQuant Research Workflow

Use this skill for JoinQuant-style research code and strategy scripts.

## Orientation

Identify whether the code is:

- research notebook/script using `jqdata`
- JoinQuant platform strategy with `initialize`, `before_trading_start`, `handle_data`, `run_daily`
- local backtest trying to mimic JoinQuant behavior
- factor pipeline using JoinQuant data exports

## JoinQuant-Specific Checks

- Query functions can be slow or rate-limited; cache raw pulls with explicit date ranges.
- Always distinguish query date, trade date, and announcement date.
- For A-shares, account for:
  - ST and delisting filters
  - suspensions
  - limit up/down
  - T+1 selling
  - stamp duty and commission
  - index membership timing
  - financial statement announcement timing
- Avoid using today's full-day data before the simulated decision time.

## Code Patterns

- Put universe construction in one function with a date argument.
- Put data retrieval in cacheable functions.
- Put signal computation in pure functions where possible.
- Put portfolio construction and order generation separately.
- Make rebalance frequency explicit.

## Audit Questions

Before trusting a JoinQuant result:

- What exact timestamp did each field become available?
- Are suspended or limit-up stocks removed before selection or only after order failure?
- Are costs identical to the platform backtest settings?
- Is the benchmark aligned with the strategy universe?
- Is there a local artifact containing daily positions and trades?

## Final Output

When editing code, return:

- changed files
- how to run in JoinQuant or locally
- assumptions that must match platform settings
- remaining data/API limitations
