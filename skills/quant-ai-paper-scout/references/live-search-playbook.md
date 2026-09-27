# Live Search Playbook

Use this when the user asks for recent, latest, this year, top-conference, or current paper discovery.

## Source Selection

| Need | Source |
|---|---|
| ICLR/NeurIPS/ICML submissions and reviews | OpenReview |
| New preprints | arXiv |
| Citation graph and related work | Semantic Scholar or OpenAlex |
| Official accepted lists | Conference proceedings pages |
| Final DOI metadata | Crossref or publisher page |
| Finance preprints | SSRN and arXiv q-fin |

## Search Order

1. Start broad with arXiv or OpenReview using method terms.
2. Narrow with quant-transfer terms.
3. Use Semantic Scholar/OpenAlex to find related and citing papers.
4. Verify venue/status from primary source.
5. Score candidates with `triage-rubric.md`.

## Minimum Metadata

For every paper in a radar table, collect:

- title
- authors
- venue/status
- date or year
- source link
- abstract-level mechanism
- code link if available
- first-pass quant-transfer note

## Avoid Shallow Retrieval

Do not stop at search results. For the top candidates:

- open the paper or abstract page
- identify the actual mechanism
- check datasets and split setup
- decide whether it maps to stocks/futures before recommending a deep read

## Recency Rule

If the user says "latest", "recent", "this year", or names a current conference cycle, verify dates online during that turn. Use absolute dates in the answer when clarifying freshness.
