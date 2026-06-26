from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_LIMIT = 10_000_000_000_000
DEFAULT_WORKERS = 4


@dataclass(frozen=True)
class SumResult:
    approach: str
    limit: int
    workers: int
    mode: str
    result: int
    expected: int
    is_correct: bool
    elapsed_seconds: float


def expected_sum(limit: int) -> int:
    if limit < 1:
        return 0
    return limit * (limit + 1) // 2


def split_into_chunks(limit: int, workers: int) -> list[tuple[int, int]]:
    if limit < 1:
        return []
    if workers < 1:
        raise ValueError("workers must be greater than zero")

    worker_count = min(workers, limit)
    base_size, remainder = divmod(limit, worker_count)
    chunks: list[tuple[int, int]] = []
    start = 1

    for index in range(worker_count):
        size = base_size + (1 if index < remainder else 0)
        end = start + size - 1
        chunks.append((start, end))
        start = end + 1

    return chunks


def formula_range_sum(start: int, end: int) -> int:
    if end < start:
        return 0
    count = end - start + 1
    return count * (start + end) // 2


def iterative_range_sum(start: int, end: int) -> int:
    return sum(range(start, end + 1))


def calculate_chunk_sum(chunk: tuple[int, int], iterative: bool) -> int:
    start, end = chunk
    if iterative:
        return iterative_range_sum(start, end)
    return formula_range_sum(start, end)


def validate_limit_for_iterative(limit: int, iterative: bool) -> None:
    if iterative and limit > 100_000_000:
        raise ValueError(
            "iterative mode is intended only for reduced limits; use --limit 10000000"
        )


def build_sum_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--iterative", action="store_true")
    return parser


def print_sum_result(result: SumResult) -> None:
    print(f"Approach: {result.approach}")
    print(f"Limit: {result.limit}")
    print(f"Workers: {result.workers}")
    print(f"Mode: {result.mode}")
    print(f"Result: {result.result}")
    print(f"Expected: {result.expected}")
    print(f"Correct: {result.is_correct}")
    print(f"Elapsed seconds: {result.elapsed_seconds:.6f}")


def write_sum_results(path: Path, results: Iterable[SumResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "approach",
                "limit",
                "workers",
                "mode",
                "result",
                "expected",
                "is_correct",
                "elapsed_seconds",
            ],
        )
        writer.writeheader()
        for result in results:
            writer.writerow(result.__dict__)
