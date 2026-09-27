---
name: quant-ai-research-autopilot
description: 组织 AI 量化方向的文献、idea、查新和实验设计。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Quant AI Research Autopilot

Use this as the broad default workflow for AI + quantitative finance research. The user may speak casually; do not require exact skill names. Infer the stage, inspect local context when present, retrieve current literature when needed, then route to the smallest set of installed skills that can produce a usable artifact.

## Stage Router

| User intent | Primary route | Output artifact |
| --- | --- | --- |
| Find directions from recent papers | `quant-ai-paper-scout` with live retrieval | `Radar` plus ranked `Idea Backlog` |
| Search arXiv or venue papers | `arxiv`, `semantic-scholar`, `research-lit` | paper table with links and relevance |
| Deep read one paper | `quant-ai-paper-scout` deep-read protocol, `alphaxiv` for arXiv quick pass | `Deep Read` note |
| Turn papers into alpha/model ideas | `quant-ai-paper-scout`, then `idea-evaluator` | ranked idea backlog |
| Check whether an idea is novel | `novelty-check`, with current literature search | closest-prior-work report |
| Decide if an idea is worth doing | `idea-evaluator` | verdict and top actions |
| Convert idea into experiments | `experiment-plan`, then `factor-alpha-lab` if signal-level | `Experiment Card` |
| Validate a factor or signal | `factor-alpha-lab` | IC/RankIC and robustness diagnostics |
| Audit backtest or performance claims | `backtest-integrity-audit` | leakage and integrity report |
| Build research code or run ML experiments | `research-code-autopilot`, `training-check`, `monitor-experiment` | runnable code and verified logs |
| Draft or push a paper | `top-ai-paper-submission` if it is now a manuscript/submission task | paper-stage artifact |

## Default Workflow

For broad requests such as "帮我找 AI 量化 idea" or "最近有什么 paper 能做":

1. Retrieve current papers first when recency matters. Prefer arXiv, OpenReview, official proceedings, Semantic Scholar, DOI/publisher pages, and finance-adjacent sources.
2. Score candidates for quant transfer, data feasibility, novelty mechanism, robustness value, engineering cost, and leakage risk.
3. Translate the strongest mechanisms into market analogues: predictive target, universe, point-in-time data contract, validation metric, tradability risk, and kill criteria.
4. Produce a ranked `Idea Backlog`; for the top one to three ideas, add `Experiment Card` sketches.
5. If the user gives a concrete idea, skip generic scouting and run `idea-evaluator` plus `novelty-check` directly.

## Workbench Files

Load these only when needed:

- `references/autopilot-playbook.md` for a strict stage-by-stage operating loop.
- `references/query-and-scoring-matrix.md` for search query families, paper scoring, and idea scoring.
- `references/research-brief-template.md` when producing a durable research note.

When a project directory is active and a durable output is useful, create a brief skeleton with:

```bash
quant-ai brief "TOPIC" --outdir research/quant-ai
```

Then fill the generated Markdown with live paper evidence, idea scoring, and experiment cards.

Use the workbench for repeatable operations:

```bash
quant-ai queries --family foundation --venue --max 20
quant-ai paper-template --output paper_candidates.csv
quant-ai score-papers paper_candidates.csv
quant-ai idea-template --output idea_candidates.csv
quant-ai score-ideas idea_candidates.csv
```

## Research Posture

- Do not stop at generic paper summaries. Every paper worth keeping should imply a falsifiable alpha, model module, representation, training objective, risk filter, or evaluation improvement.
- Separate paper benchmark quality from market usefulness. Forecasting MSE, benchmark rank, and trading value are different claims.
- Treat point-in-time availability as a first-class constraint. Always identify what the strategy knew at decision time.
- Be strict about leakage, survivorship, corporate action timing, futures roll timing, universe membership timing, limit-up/down, suspension, and transaction costs.
- Prefer ideas that can be killed quickly by a small experiment over ideas that need months before the first falsification.

## Artifact Contract

When the user asks for idea discovery, return:

- `Top thesis`: one sentence saying what research bet looks strongest.
- `Paper radar`: papers, venue/date, link, mechanism, quant-transfer score, and action.
- `Idea backlog`: ranked ideas with market analogue, data contract, minimal test, likely failure, and next route.
- `Immediate next step`: the one artifact to build next, usually an `Experiment Card` or novelty check.

When working in a local project, save durable outputs next to the project when there is an obvious research folder. Otherwise, keep the first pass in chat and ask only if a write location is genuinely ambiguous.
