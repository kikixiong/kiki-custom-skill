#!/usr/bin/env python3
"""Rank paper candidates using the Quant AI Paper Scout triage rubric.

Input can be CSV or JSONL. Required score fields are 1-5:
quant_transfer, data_feasibility, novel_mechanism, robustness_value,
engineering_cost, leakage_risk.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

WEIGHTS = {
    "quant_transfer": 2.0,
    "data_feasibility": 1.5,
    "novel_mechanism": 1.5,
    "robustness_value": 1.5,
    "engineering_cost": 1.0,
    "leakage_risk": 2.0,
}

SCORE_FIELDS = tuple(WEIGHTS)


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
        title = record.get("title") or record.get("paper") or "<untitled>"
        raise ValueError(f"{title}: invalid {field}={value!r}") from exc
    if not 1 <= score <= 5:
        title = record.get("title") or record.get("paper") or "<untitled>"
        raise ValueError(f"{title}: {field} must be in [1, 5], got {score}")
    return score


def classify(record: dict[str, Any], total: float, min_score: float) -> str:
    if min_score < 3:
        return "Reject" if total < 32 else "Park"
    if total >= 38:
        return "Implement candidate"
    if total >= 32 or parse_score(record, "novel_mechanism") >= 5:
        return "Deep read"
    if total >= 24:
        return "Park"
    return "Reject"


def score_record(record: dict[str, Any]) -> dict[str, Any]:
    scores = {field: parse_score(record, field) for field in SCORE_FIELDS}
    total = sum(scores[field] * WEIGHTS[field] for field in SCORE_FIELDS)
    min_score = min(scores.values())
    return {
        **record,
        "score": round(total, 2),
        "min_dimension": min_score,
        "action": classify(record, total, min_score),
    }


def markdown_table(records: list[dict[str, Any]]) -> str:
    lines = [
        "| Rank | Paper | Score | Action | Venue | Note |",
        "|---:|---|---:|---|---|---|",
    ]
    for rank, record in enumerate(records, 1):
        title = str(record.get("title") or record.get("paper") or "<untitled>").replace("|", "\\|")
        venue = str(record.get("venue") or record.get("status") or "").replace("|", "\\|")
        note = str(record.get("note") or record.get("why") or "").replace("|", "\\|")
        lines.append(
            f"| {rank} | {title} | {record['score']} | {record['action']} | {venue} | {note} |"
        )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="CSV or JSONL paper candidate file")
    parser.add_argument("--top", type=int, default=20, help="Number of ranked rows to print")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of markdown")
    args = parser.parse_args()

    records = [score_record(record) for record in read_records(args.input)]
    records.sort(key=lambda item: (item["score"], item.get("novel_mechanism", 0)), reverse=True)
    records = records[: args.top]

    if args.json:
        print(json.dumps(records, ensure_ascii=False, indent=2))
    else:
        print(markdown_table(records))


if __name__ == "__main__":
    main()
