---
name: quant-ai-paper-scout
description: 检索 AI/ML 论文，提炼适用于量化金融的研究思路。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Quant AI Paper Scout

Use this skill for high-intensity paper discovery, reading, and idea mining for a quant researcher working on stock and futures forecasting, multi-factor models, and AI time-series methods.

## User Profile Assumptions

- The research object is predictive modeling for stocks or futures, often through multi-factor or sequence models.
- Good ideas must survive point-in-time data, tradability, costs, liquidity, regime shift, and out-of-sample validation.
- AI conference papers are useful only if they can be translated into a falsifiable alpha, model module, data representation, training objective, or evaluation improvement.

## Search Scope

Prioritize recent and influential papers from:

- AI/ML venues: NeurIPS, ICML, ICLR, KDD, AAAI, IJCAI, WWW, SIGIR, CIKM, AISTATS, UAI, JMLR, TMLR.
- Time-series venues and tracks: forecasting, representation learning, anomaly detection, temporal distribution shift, irregular sampling, long-context sequence modeling.
- Finance-adjacent sources: SSRN, arXiv q-fin, Quantitative Finance, Journal of Financial Data Science, ACM ICAIF, market microstructure papers.

If the user asks for latest, recent, this year, new papers, conference papers, or a current venue list, browse or query paper databases before answering.

When doing live search, prefer primary or scholarly sources:

- OpenReview for reviews, submissions, acceptance status, and venue metadata.
- arXiv for preprints and newest versions.
- Proceedings pages for official accepted papers.
- Semantic Scholar or OpenAlex for citation graph, related papers, and author trail.
- Publisher or journal pages for final metadata when a paper has a DOI.

Do not rely on blog posts or social media as evidence unless the task is explicitly about community attention.

For repeat work, load only the needed reference:

- `references/radar-workflow.md` for recurring paper scouting.
- `references/search-query-matrix.md` for query design.
- `references/live-search-playbook.md` for current paper retrieval and source choice.
- `references/triage-rubric.md` for paper scoring.
- `references/deep-read-protocol.md` for one-paper close reading and adversarial review.
- `references/quant-transfer-patterns.md` for turning methods into alpha/model ideas.
- `references/paper-note-template.md` for one-paper deep reading.
- `references/idea-backlog-template.md` for ranked idea backlog output.
- `references/experiment-design-template.md` for converting an idea into a falsifiable test.
- `references/radar-report-template.md` for recurring radar reports.

## Research Tracks

Maintain separate buckets instead of mixing everything into one reading list:

1. Time-series foundation models and long-horizon forecasting.
2. Transformer, state-space, Mamba, diffusion, and hybrid sequence architectures.
3. Self-supervised, contrastive, masked, and representation learning for temporal data.
4. Cross-sectional ranking, tabular learning, multi-factor modeling, and learning-to-rank.
5. Graph, relational, cross-asset, sector, supply-chain, and lead-lag modeling.
6. Market microstructure, order book, intraday, execution-aware prediction.
7. Distribution shift, online learning, regime adaptation, OOD robustness, calibration.
8. Evaluation integrity: leakage, backtest bias, split design, and statistically reliable claims.

## Casual Request Routing

If the user says "帮我找 AI 量化 idea", "最近有什么 paper 能转成 alpha", "扫一下顶会时序论文", "做个 quant paper radar", or similar casual phrasing, produce the smallest useful artifact:

- `Radar` when the user needs papers.
- `Idea Backlog` when the user needs research directions.
- `Experiment Card` when one idea is already selected.
- `Deep Read` when the user names one paper or arXiv ID.

For broad idea discovery, do not stop at paper summaries. Always translate at least the strongest candidates into market analogues, minimal tests, and kill criteria.

## Paper Triage

Score each candidate paper before deep reading:

- `Quant Transfer`: can the idea map to alpha, ranking, portfolio, risk, or execution?
- `Data Feasibility`: can the required data exist point-in-time for stocks or futures?
- `Novel Mechanism`: does it contain a mechanism beyond "bigger model gets lower error"?
- `Robustness Value`: does it help with regime shift, noisy labels, nonstationarity, or tail events?
- `Engineering Cost`: can it be implemented and tested quickly in the user's environment?
- `Leakage Risk`: could the method accidentally use future information or unrealistic labels?

Use `Deep Read` only for papers with high transfer or high mechanism value. Otherwise summarize briefly and park them.

Default action thresholds:

- `Implement candidate`: high quant transfer, feasible point-in-time data, clear minimal experiment, and no severe leakage concern.
- `Deep read`: strong mechanism or strong relevance, but experiment path still needs design.
- `Park`: interesting AI method but weak quant transfer or unrealistic data requirement.
- `Reject`: dominated prior work, obvious leakage, benchmark-only contribution, or no credible market analogue.

## Paper Reading Template

For each deep-read paper, extract:

- citation, venue/status, code/data links, and date
- one-sentence contribution
- core technical mechanism
- assumptions the paper depends on
- exact evaluation setup and possible leakage or weak baselines
- what it would mean in stock/futures prediction
- one to three alpha/model ideas derived from it
- minimal experiment to falsify each idea
- kill criteria: what result would make the idea not worth pursuing

Use three reading passes:

1. `Triage pass`: decide whether the paper deserves attention.
2. `Mechanism pass`: understand the exact method, objective, data, and evaluation.
3. `Quant pass`: translate to a stock/futures experiment and attack leakage or tradability risk.

## Idea Mining Loop

Translate papers using this chain:

`paper mechanism -> market analogue -> predictive target -> factor/model design -> point-in-time data contract -> validation plan -> failure mode`

Examples of market analogues:

- masked temporal reconstruction -> robust latent factor representation
- cross-variable attention -> cross-asset or sector lead-lag signal
- domain adaptation -> regime-aware training across bull, bear, and shock periods
- calibration or uncertainty -> position sizing or risk filter
- learning-to-rank -> cross-sectional return ranking

## Default Outputs

Choose the output shape based on the request:

- `Radar`: table of papers with score, venue, link, why it matters, and action.
- `Deep Read`: full template for one paper.
- `Idea Backlog`: ranked ideas with experiment plans and risks.
- `Experiment Card`: one falsifiable experiment with data contract, baselines, metrics, and kill criteria.
- `Weekly Digest`: new papers, changed beliefs, and next reads.
- `Research Map`: taxonomy of a subfield and where alpha opportunities may exist.

## Guardrails

- Do not treat benchmark forecasting accuracy as sufficient evidence for tradable alpha.
- Always separate prediction quality from portfolio value, turnover, cost, capacity, and execution.
- Check whether labels, features, universe membership, and corporate/futures roll data were known at decision time.
- Avoid live trading instructions unless the user explicitly asks and supplies the required market context.
- Be skeptical of finance papers without realistic costs, survivorship handling, or out-of-sample tests.

## Handoff

- Use `af-paper-lookup` or browsing for paper search and metadata.
- Use `deep-research` for systematic literature review or a broad research map.
- Use `idea-evaluator` when the user wants to decide whether a derived idea is worth months of work.
- Use `factor-alpha-lab` for factor construction and signal validation.
- Use `backtest-integrity-audit` before trusting performance claims.
