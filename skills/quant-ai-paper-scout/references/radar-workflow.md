# Quant AI Paper Radar Workflow

Use this workflow when the user wants continuous, high-intensity paper discovery rather than a one-off list.

## Cadence

### Daily 15-Minute Scan

- Check arXiv categories: `cs.LG`, `stat.ML`, `cs.AI`, `cs.IR`, `q-fin.ST`, `q-fin.TR`, `q-fin.PM`.
- Search exact terms from `search-query-matrix.md`.
- Save only title, link, date, one-line mechanism, and first-pass action.

### Weekly Radar

Produce a ranked table:

| Rank | Paper | Venue/Date | Track | Quant Transfer | Data Feasibility | Leakage Risk | Action |
|---:|---|---|---|---:|---:|---:|---|

Add a short "changed beliefs" section:

- What looks more promising than last week?
- What looks overhyped?
- Which idea deserves one minimal experiment?

### Monthly Research Map

Build or update a taxonomy:

- core model families
- task setups and datasets
- dominant assumptions
- evaluation weaknesses
- quant-transfer opportunities
- implementation shortlist

## Source Priority

1. OpenReview for ICLR, NeurIPS, ICML when available.
2. arXiv for newest preprints and q-fin.
3. Semantic Scholar or OpenAlex for citation graph and related work.
4. Conference proceedings pages for accepted lists.
5. SSRN and finance journals for market-specific evidence.

## Output Discipline

- Do not list papers only because they are new.
- Every included paper needs a reason it may matter for stock/futures prediction.
- Keep "interesting AI" separate from "tradable research candidate".
- If there is no clear minimal experiment, mark the paper as `Park`, not `Implement`.
