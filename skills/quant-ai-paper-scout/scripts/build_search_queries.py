#!/usr/bin/env python3
"""Generate reusable paper search queries for quant AI scouting."""

import argparse

METHOD_TERMS = [
    '"time series foundation model"',
    '"masked time series modeling"',
    '"self-supervised time series"',
    '"state space model" "time series"',
    '"Mamba" "time series"',
    '"Transformer" "time series forecasting"',
    '"distribution shift" "time series"',
    '"learning to rank" "time series"',
    '"graph neural network" "time series forecasting"',
]

QUANT_TERMS = [
    '"financial time series"',
    '"stock return prediction"',
    '"futures prediction"',
    '"alpha factor"',
    '"cross-sectional return"',
    '"market microstructure"',
]

VENUE_FILTERS = [
    "site:openreview.net",
    "site:arxiv.org",
    "site:proceedings.mlr.press",
]


def build_queries(max_queries: int, with_venue: bool) -> list[str]:
    queries: list[str] = []
    for method in METHOD_TERMS:
        for quant in QUANT_TERMS:
            base = f"{method} {quant}"
            if with_venue:
                for venue in VENUE_FILTERS:
                    queries.append(f"{venue} {base}")
                    if len(queries) >= max_queries:
                        return queries
            else:
                queries.append(base)
                if len(queries) >= max_queries:
                    return queries
    return queries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=30, help="Maximum queries to print")
    parser.add_argument("--with-venue", action="store_true", help="Include venue/site filters")
    args = parser.parse_args()

    for query in build_queries(args.max, args.with_venue):
        print(query)


if __name__ == "__main__":
    main()
