from __future__ import annotations

import argparse
import time
from pathlib import Path

from lab_2.task_2 import asyncio_parser, multiprocessing_parser, threading_parser
from lab_2.task_2.common import (
    DEFAULT_TIMEOUT,
    DEFAULT_WORKERS,
    ParserSummary,
    summarize_results,
    write_parser_summaries,
)
from lab_2.task_2.urls import URLS

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "task_2_results.csv"


def _run_approach(
    approach: str,
    workers: int,
    timeout: float,
) -> ParserSummary:
    started_at = time.perf_counter()
    if approach == "threading":
        results = threading_parser.parse_many(URLS, workers, timeout)
    elif approach == "multiprocessing":
        results = multiprocessing_parser.parse_many(URLS, workers, timeout)
    elif approach == "asyncio":
        results = asyncio_parser.parse_many(URLS, workers, timeout)
    else:
        raise ValueError(f"unknown approach: {approach}")
    elapsed = time.perf_counter() - started_at
    return summarize_results(approach, workers, results, elapsed)


def run_all(
    workers: int = DEFAULT_WORKERS,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[ParserSummary]:
    summaries = [
        _run_approach("threading", workers, timeout),
        _run_approach("multiprocessing", workers, timeout),
        _run_approach("asyncio", workers, timeout),
    ]
    write_parser_summaries(RESULTS_PATH, summaries)
    return summaries


def main() -> None:
    parser = argparse.ArgumentParser(description="Run all task 2 implementations.")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()

    summaries = run_all(args.workers, args.timeout)
    for summary in summaries:
        print(summary)
    print(f"Results saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
