---
name: arxiv-daily-digest
description: Automatically fetch, filter, rank, and summarize arXiv papers based on the user's configured research interests. Use when the user wants daily arXiv paper updates, personalized paper recommendations, research interest configuration, or scheduled research digests.
disable-model-invocation: true
---

## Runtime configuration

Read [the installed runtime configuration](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's actual tools, account access and execution restrictions.

# arXiv Daily Digest

Fetch, filter and summarize papers according to the current user's research
interests. Save a local Markdown digest. Scheduling, a delivery channel and a
summarization model are not selected by installation.

## Configure before the first run

Ask for the user's research areas and keywords, arXiv categories, and any output
limits that matter. Reuse already supplied preferences. Ask about a schedule,
time zone or notification destination only when recurring delivery is requested.

Copy the three templates from `config/` to the local directory below, keeping
existing settings if they are already present:

- Configuration: `@@KIKI_AGENT_HOME@@/skill-config/arxiv-daily-digest/`.
- Runtime cache and output: `@@KIKI_AGENT_HOME@@/skill-data/arxiv-daily-digest/`.

Override these locations with `ARXIV_DIGEST_CONFIG_DIR` and
`ARXIV_DIGEST_DATA_DIR` when the user already has a configuration or storage
location. Configuration and generated results remain outside this repository
and outside the installed skill directory so a skill update does not replace them.

`research_interests.json` starts with an empty `interests` list. Each item needs
an `id`, a display `name`, a list of `keywords`, and `priority` (`high` or `medium`).
For example, use `your-topic` as the ID and fill the other fields from the request.
Do not adopt the maintainer's research areas as the user's preferences.

`arxiv_categories.json` starts with an empty `categories` list. Each item has an
arXiv `id` and a `check_daily` boolean. Select valid categories for the requested
subject; the empty template makes no subscriptions on the user's behalf.

`digest_settings.json` controls display limits and local storage. External
notification settings are not part of the default. If an assistant adds a
qualitative summary, use its actual configured model and distinguish summaries
from claims verified against full papers.

## Run a requested digest

From the installed skill directory:

```bash
./scripts/run_digest.sh
```

The script checks local configuration before network requests. It then:

1. Fetches recent papers from the selected arXiv categories, reusing today's cache
   when present. Raw records are saved under the runtime data directory.
2. Matches interest keywords and ranks relevant papers. High-priority interests
   receive twice the keyword weight; unmatched papers are omitted.
3. Groups results into top picks, worth reading and quick glance, then produces
   Markdown with source links, matched interests and an interest breakdown.
4. Saves the digest under the configured storage path and prints its location.

The fetching, ranking and formatting scripts do not run an embedding model or
LLM. Do not imply that reading an abstract verifies a paper's experimental claims.

## Scheduling and delivery

Create a recurring job only when requested, using the current client's supported
scheduler and the user's chosen time and time zone. Report a missing scheduler
instead of inventing a cron installation. No particular chat application, account
or recipient is assumed. Send externally only when the user explicitly asks.

For a one-off request, generate one digest and return the artifact or saved path.
See [workflow.md](references/workflow.md) for configuration and troubleshooting.
