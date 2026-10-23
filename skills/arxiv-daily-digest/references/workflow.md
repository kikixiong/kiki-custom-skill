# arXiv digest workflow

## Local setup

Read SKILL.md for the local configuration and storage locations. Copy the bundled
JSON templates to the configuration directory without overwriting existing
settings. Fill interests and arXiv categories from the user's request. Never
commit the resulting personal settings or generated digests back into this repo.

`ARXIV_DIGEST_CONFIG_DIR` and `ARXIV_DIGEST_DATA_DIR` override the defaults.
Configuration is required before fetching; empty templates intentionally fail
with an actionable message instead of silently using someone else's topics.

## Processing

1. Check configuration with `scripts/local_config.py`.
2. Fetch from configured arXiv categories into the runtime cache.
3. Filter and rank by the user's keywords and priorities.
4. Generate Markdown, honoring the selected display limits and storage path.
5. Return the saved artifact. Schedule or send notifications only when requested.

The shell orchestrator combines those steps. Individual scripts accept their
existing file/stdin inputs and share the same configuration and data directories.

## Troubleshooting

- Missing configuration: initialize the local templates and fill required fields.
- No matching papers: check selected categories, keywords, dates and source errors.
- Source unavailable: report it; do not replace the user's topics or invent papers.
- Delivery unavailable: return the local artifact; do not switch channels silently.
- Duplicate caches: check the configured data directory before fetching again.

Scheduling is managed by the actual client, not by the JSON templates. Use the
user's specified time zone and interval; installation creates no recurring job.
