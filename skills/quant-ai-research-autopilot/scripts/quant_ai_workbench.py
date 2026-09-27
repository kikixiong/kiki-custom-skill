#!/usr/bin/env python3
"""CLI workbench for AI + Quant research scouting artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path
from typing import Any, Iterable

PAPER_WEIGHTS = {
    "quant_transfer": 2.0,
    "data_feasibility": 1.5,
    "novel_mechanism": 1.5,
    "robustness_value": 1.5,
    "engineering_cost": 1.0,
    "leakage_risk": 2.0,
}

IDEA_WEIGHTS = {
    "first_test_speed": 1.5,
    "evidence_delta": 2.0,
    "paper_novelty": 1.5,
    "market_realism": 2.0,
    "paper_story": 1.0,
    "leakage_risk": 2.0,
}

QUERY_FAMILIES = {
    "foundation": [
        '"time series foundation model" finance',
        '"time series foundation model" "stock"',
        '"time series foundation model" "futures"',
        '"foundation model" "financial time series"',
        '"long context" "time series forecasting" "stock"',
    ],
    "ssl": [
        '"self-supervised time series" "stock return prediction"',
        '"masked time series modeling" "financial time series"',
        '"contrastive learning" "financial time series"',
        '"representation learning" "stock prediction"',
    ],
    "sequence": [
        '"Mamba" "time series forecasting" finance',
        '"state space model" "financial time series"',
        '"Transformer" "stock return prediction"',
        '"diffusion" "time series forecasting" finance',
    ],
    "cross_sectional": [
        '"learning to rank" "stock return prediction"',
        '"cross-sectional return prediction" "deep learning"',
        '"multi-factor" "transformer" "stock"',
        '"tabular deep learning" "alpha factor"',
    ],
    "graph": [
        '"graph neural network" "stock prediction"',
        '"lead-lag" "financial time series" "deep learning"',
        '"sector relation" "stock return prediction"',
        '"supply chain" "stock prediction" graph',
    ],
    "robustness": [
        '"distribution shift" "financial time series"',
        '"regime adaptation" "stock prediction"',
        '"online learning" "financial time series" "deep learning"',
        '"uncertainty calibration" "stock prediction"',
    ],
    "microstructure": [
        '"limit order book" "self-supervised learning"',
        '"limit order book" "deep learning" prediction',
        '"market microstructure" "transformer"',
        '"execution cost" "deep learning" forecasting',
    ],
}

VENUE_FILTERS = [
    "site:openreview.net",
    "site:arxiv.org",
    "site:proceedings.mlr.press",
    "site:dl.acm.org ICAIF",
    'site:ssrn.com "machine learning" "asset pricing"',
]


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


def write_brief(args: argparse.Namespace) -> None:
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    slug = args.slug or slugify(args.topic)
    path = outdir / f"{args.date}-{slug}.md"
    if path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.write_text(brief_text(args.topic, args.date), encoding="utf-8")
    print(path)


def emit_queries(args: argparse.Namespace) -> None:
    families = args.family or list(QUERY_FAMILIES)
    queries: list[str] = []
    for family in families:
        if family not in QUERY_FAMILIES:
            valid = ", ".join(sorted(QUERY_FAMILIES))
            raise SystemExit(f"Unknown family {family!r}. Valid: {valid}")
        for query in QUERY_FAMILIES[family]:
            if args.venue:
                queries.extend(f"{venue} {query}" for venue in VENUE_FILTERS)
            else:
                queries.append(query)
    for query in queries[: args.max]:
        print(query)


def write_csv_template(path: Path, fields: Iterable[str], force: bool) -> None:
    if path.exists() and not force:
        raise SystemExit(f"Refusing to overwrite existing file: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
    print(path)


def paper_template(args: argparse.Namespace) -> None:
    fields = [
        "title",
        "venue",
        "year",
        "link",
        "mechanism",
        *PAPER_WEIGHTS,
        "note",
    ]
    write_csv_template(Path(args.output), fields, args.force)


def idea_template(args: argparse.Namespace) -> None:
    fields = [
        "idea",
        "market_analogue",
        "data_contract",
        "minimal_test",
        "kill_criterion",
        *IDEA_WEIGHTS,
        "note",
    ]
    write_csv_template(Path(args.output), fields, args.force)


def read_records(path: Path) -> list[dict[str, Any]]:
    if path.suffix.lower() == ".jsonl":
        records = []
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_score(record: dict[str, Any], field: str) -> float:
    value = record.get(field, "")
    try:
        score = float(value)
    except (TypeError, ValueError) as exc:
        title = record.get("title") or record.get("idea") or "<untitled>"
        raise ValueError(f"{title}: invalid {field}={value!r}") from exc
    if not 1 <= score <= 5:
        title = record.get("title") or record.get("idea") or "<untitled>"
        raise ValueError(f"{title}: {field} must be in [1, 5], got {score}")
    return score


def score_record(record: dict[str, Any], weights: dict[str, float]) -> dict[str, Any]:
    scores = {field: parse_score(record, field) for field in weights}
    total = sum(scores[field] * weights[field] for field in weights)
    min_score = min(scores.values())
    return {**record, "score": round(total, 2), "min_dimension": min_score}


def classify_paper(record: dict[str, Any]) -> str:
    score = float(record["score"])
    min_score = float(record["min_dimension"])
    novel = parse_score(record, "novel_mechanism")
    if min_score < 3:
        return "Reject" if score < 32 else "Park"
    if score >= 38:
        return "Implement candidate"
    if score >= 32 or novel >= 5:
        return "Deep read"
    if score >= 24:
        return "Park"
    return "Reject"


def classify_idea(record: dict[str, Any]) -> str:
    score = float(record["score"])
    min_score = float(record["min_dimension"])
    if min_score < 3:
        return "Reject or narrow"
    if score >= 39:
        return "Experiment now"
    if score >= 33:
        return "Novelty check then experiment"
    if score >= 26:
        return "Park"
    return "Reject or pivot"


def markdown_table(records: list[dict[str, Any]], kind: str) -> str:
    if kind == "paper":
        lines = [
            "| Rank | Paper | Score | Action | Venue | Note |",
            "|---:|---|---:|---|---|---|",
        ]
        for rank, record in enumerate(records, 1):
            title = safe_cell(record.get("title") or "<untitled>")
            venue = safe_cell(record.get("venue") or record.get("year") or "")
            note = safe_cell(record.get("note") or record.get("mechanism") or "")
            lines.append(f"| {rank} | {title} | {record['score']} | {record['action']} | {venue} | {note} |")
        return "\n".join(lines)

    lines = [
        "| Rank | Idea | Score | Action | Market Analogue | Kill Criterion |",
        "|---:|---|---:|---|---|---|",
    ]
    for rank, record in enumerate(records, 1):
        idea = safe_cell(record.get("idea") or "<untitled>")
        analogue = safe_cell(record.get("market_analogue") or "")
        kill = safe_cell(record.get("kill_criterion") or "")
        lines.append(f"| {rank} | {idea} | {record['score']} | {record['action']} | {analogue} | {kill} |")
    return "\n".join(lines)


def safe_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def score_items(args: argparse.Namespace, kind: str) -> None:
    weights = PAPER_WEIGHTS if kind == "paper" else IDEA_WEIGHTS
    classify = classify_paper if kind == "paper" else classify_idea
    records = [score_record(record, weights) for record in read_records(Path(args.input))]
    for record in records:
        record["action"] = classify(record)
    records.sort(key=lambda item: (item["score"], item["min_dimension"]), reverse=True)
    records = records[: args.top]
    if args.json:
        print(json.dumps(records, ensure_ascii=False, indent=2))
    else:
        print(markdown_table(records, kind))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    brief = sub.add_parser("brief", help="Create a research brief skeleton")
    brief.add_argument("topic")
    brief.add_argument("--outdir", default="research/quant-ai")
    brief.add_argument("--slug")
    brief.add_argument("--date", default=date.today().isoformat())
    brief.add_argument("--force", action="store_true")
    brief.set_defaults(func=write_brief)

    queries = sub.add_parser("queries", help="Print live-search query candidates")
    queries.add_argument("--family", action="append", choices=sorted(QUERY_FAMILIES))
    queries.add_argument("--venue", action="store_true", help="Add site/venue filters")
    queries.add_argument("--max", type=int, default=30)
    queries.set_defaults(func=emit_queries)

    paper_t = sub.add_parser("paper-template", help="Create paper scoring CSV")
    paper_t.add_argument("--output", default="paper_candidates.csv")
    paper_t.add_argument("--force", action="store_true")
    paper_t.set_defaults(func=paper_template)

    idea_t = sub.add_parser("idea-template", help="Create idea scoring CSV")
    idea_t.add_argument("--output", default="idea_candidates.csv")
    idea_t.add_argument("--force", action="store_true")
    idea_t.set_defaults(func=idea_template)

    score_p = sub.add_parser("score-papers", help="Score paper candidate CSV/JSONL")
    score_p.add_argument("input")
    score_p.add_argument("--top", type=int, default=20)
    score_p.add_argument("--json", action="store_true")
    score_p.set_defaults(func=lambda args: score_items(args, "paper"))

    score_i = sub.add_parser("score-ideas", help="Score idea candidate CSV/JSONL")
    score_i.add_argument("input")
    score_i.add_argument("--top", type=int, default=20)
    score_i.add_argument("--json", action="store_true")
    score_i.set_defaults(func=lambda args: score_items(args, "idea"))

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
