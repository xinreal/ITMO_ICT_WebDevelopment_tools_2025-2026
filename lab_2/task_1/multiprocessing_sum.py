from __future__ import annotations

import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor

from lab_2.task_1.common import (
    DEFAULT_LIMIT,
    DEFAULT_WORKERS,
    SumResult,
    build_sum_parser,
    calculate_chunk_sum,
    expected_sum,
    print_sum_result,
    split_into_chunks,
    validate_limit_for_iterative,
)


def _calculate_chunk_from_args(args: tuple[tuple[int, int], bool]) -> int:
    chunk, iterative = args
    return calculate_chunk_sum(chunk, iterative)


def calculate_sum(
    limit: int = DEFAULT_LIMIT,
    workers: int = DEFAULT_WORKERS,
    iterative: bool = False,
) -> SumResult:
    validate_limit_for_iterative(limit, iterative)
    chunks = split_into_chunks(limit, workers)
    started_at = time.perf_counter()

    with ProcessPoolExecutor(max_workers=workers) as executor:
        partial_sums = list(
            executor.map(
                _calculate_chunk_from_args,
                [(chunk, iterative) for chunk in chunks],
            )
        )

    elapsed = time.perf_counter() - started_at
    result = sum(partial_sums)
    expected = expected_sum(limit)
    return SumResult(
        approach="multiprocessing",
        limit=limit,
        workers=workers,
        mode="iterative" if iterative else "formula",
        result=result,
        expected=expected,
        is_correct=result == expected,
        elapsed_seconds=elapsed,
    )


def main() -> None:
    parser = build_sum_parser("Calculate a sum with multiprocessing.")
    args = parser.parse_args()
    result = calculate_sum(args.limit, args.workers, args.iterative)
    print_sum_result(result)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
