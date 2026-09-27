#!/usr/bin/env python3
"""Create a durable Quant AI research brief skeleton."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text.strip()).strip("-").lower()
    return slug[:80] or "quant-ai-brief"


def brief_text(topic: str, today: str) -> str:
    return f"""# Quant AI Research Brief: {topic}

Date: {today}
Status: scouting

## Top Thesis

TBD.

## Search Scope

- Universe:
- Horizon:
- Data sources:
- Model family:
- Exclusions:

## Paper Radar

| Paper | Date/Venue | Link | Mechanism | Quant Transfer | Action |
|---|---|---|---|---:|---|

## Idea Backlog

| Rank | Idea | Market Analogue | Data Contract | Minimal Test | Kill Criterion | Next Route |
|---:|---|---|---|---|---|---|

## Experiment Cards

### Idea 1

- Claim:
- Universe and dates:
- Features known at decision time:
- Target:
- Baselines:
- Metrics:
- Cost/slippage assumption:
- Robustness slices:
- Kill criterion:

## Novelty And Prior Work Risks

TBD.

## Integrity Risks

- Leakage:
- Survivorship:
- Timestamp:
- Universe:
- Cost:
- Capacity:

## Next Action

TBD.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", help="Research topic or direction")
    parser.add_argument("--outdir", type=Path, default=Path("research/quant-ai"))
    parser.add_argument("--slug", help="Optional filename slug")
    parser.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    slug = args.slug or slugify(args.topic)
    path = args.outdir / f"{args.date}-{slug}.md"
    if path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.write_text(brief_text(args.topic, args.date), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
