from __future__ import annotations

import argparse
from pathlib import Path

from lab_2.task_1 import asyncio_sum, multiprocessing_sum, threading_sum
from lab_2.task_1.common import (
    DEFAULT_LIMIT,
    DEFAULT_WORKERS,
    SumResult,
    print_sum_result,
    write_sum_results,
)

RESULTS_PATH = Path(__file__).resolve().parent / "results" / "task_1_results.csv"


def run_all(
    limit: int = DEFAULT_LIMIT,
    workers: int = DEFAULT_WORKERS,
    iterative: bool = False,
) -> list[SumResult]:
    results = [
        threading_sum.calculate_sum(limit, workers, iterative),
        multiprocessing_sum.calculate_sum(limit, workers, iterative),
        asyncio_sum.calculate_sum(limit, workers, iterative),
    ]
    first_result = results[0].result
    if any(result.result != first_result for result in results):
        raise RuntimeError("sum implementations returned different results")
    if any(not result.is_correct for result in results):
        raise RuntimeError("at least one sum implementation returned a wrong result")
    write_sum_results(RESULTS_PATH, results)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Run all task 1 implementations.")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--iterative", action="store_true")
    args = parser.parse_args()

    results = run_all(args.limit, args.workers, args.iterative)
    for result in results:
        print_sum_result(result)
        print()
    print(f"Results saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
