#!/usr/bin/env python3
"""Scaffold a research wiki from Orgnization and Prompts.pdf."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


CLAUDE = """# Research Wiki Schema

## Identity

You are the maintainer of this research knowledge base.
Your goal is to turn raw papers and notes into structured wiki pages that help discover research gaps and testable ideas.
You write `wiki/`; the user provides raw material and direction judgments.

## Directory Contract

- `raw/papers/`: original paper markdown, read-only.
- `raw/notes/`: user notes and clips, read-only.
- `raw/assets/`: images and local assets.
- `wiki/papers/`: one page per paper.
- `wiki/concepts/`: methods, theories, and recurring concepts.
- `wiki/entities/`: authors, groups, datasets, systems, benchmarks.
- `wiki/comparisons/`: method comparisons and answer artifacts.
- `wiki/gaps/`: confirmed gaps, hypotheses, and open questions.
- `wiki/synthesis/`: field map, shared assumptions, and dated discussions.
- `wiki/index.md`: all pages plus one-line summaries.
- `wiki/log.md`: append-only operation log.

## Paper Page Template

---
paper_id:
title:
authors:
year:
venue:
status: queued
confidence: low
tags: []
---

## One-Sentence Contribution

## Problem Setting

## Core Method

## Experiments

## Limitations And Assumptions

## Relation To Existing Work

- Builds on:
- Contradicts:

## Gap Signals

## Operations

### Ingest

1. Read `raw/papers/[id].md`.
2. Extract 2-3 key takeaways.
3. Write `wiki/papers/[id].md`.
4. Update related concepts/entities.
5. Mark contradictions in both affected pages.
6. Update `wiki/gaps/questions.md` if new questions appear.
7. Update `wiki/index.md` and append `wiki/log.md`.

### Query

1. Read `wiki/index.md`.
2. Read relevant pages.
3. Answer with confidence and evidence.
4. Write valuable comparisons to `wiki/comparisons/` and synthesis to `wiki/synthesis/`.

### Lint

Check orphan pages, contradictions, stale claims, missing concept pages, and hypotheses that new papers support or refute.

### Idea Generation

1. Read `wiki/synthesis/shared-assumptions.md`.
2. Read `wiki/gaps/confirmed-gaps.md` and `wiki/gaps/questions.md`.
3. Propose hypotheses with evidence, counterarguments, and minimal experiments.
4. Write consensus into `wiki/gaps/hypotheses.md`.
"""


FILES = {
    "wiki/index.md": "# Research Wiki Index\n\n",
    "wiki/log.md": "# Research Wiki Log\n\n",
    "wiki/overview.md": "# Field Overview\n\n",
    "wiki/gaps/confirmed-gaps.md": "# Confirmed Research Gaps\n\n",
    "wiki/gaps/hypotheses.md": "# Research Hypotheses\n\n",
    "wiki/gaps/questions.md": "# Open Questions\n\n",
    "wiki/synthesis/field-map.md": "# Field Map\n\n",
    "wiki/synthesis/shared-assumptions.md": "# Shared Assumptions\n\n",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    root = args.path.expanduser().resolve()
    for rel in [
        "raw/papers",
        "raw/notes",
        "raw/assets",
        "wiki/papers",
        "wiki/concepts",
        "wiki/entities",
        "wiki/comparisons",
        "wiki/gaps",
        "wiki/synthesis",
    ]:
        (root / rel).mkdir(parents=True, exist_ok=True)

    targets = {"CLAUDE.md": CLAUDE, **FILES}
    for rel, text in targets.items():
        path = root / rel
        if path.exists() and not args.force:
            continue
        path.write_text(text, encoding="utf-8")

    log = root / "wiki/log.md"
    with log.open("a", encoding="utf-8") as handle:
        handle.write(f"- {date.today().isoformat()}: scaffolded research wiki.\\n")
    print(root)


if __name__ == "__main__":
    main()
