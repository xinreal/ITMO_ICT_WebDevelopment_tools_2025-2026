from __future__ import annotations

import asyncio
import time

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


async def _calculate_chunk(chunk: tuple[int, int], iterative: bool) -> int:
    await asyncio.sleep(0)
    return calculate_chunk_sum(chunk, iterative)


async def calculate_sum_async(
    limit: int = DEFAULT_LIMIT,
    workers: int = DEFAULT_WORKERS,
    iterative: bool = False,
) -> SumResult:
    validate_limit_for_iterative(limit, iterative)
    chunks = split_into_chunks(limit, workers)
    started_at = time.perf_counter()
    tasks = [_calculate_chunk(chunk, iterative) for chunk in chunks]
    partial_sums = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - started_at

    result = sum(partial_sums)
    expected = expected_sum(limit)
    return SumResult(
        approach="asyncio",
        limit=limit,
        workers=workers,
        mode="iterative" if iterative else "formula",
        result=result,
        expected=expected,
        is_correct=result == expected,
        elapsed_seconds=elapsed,
    )


def calculate_sum(
    limit: int = DEFAULT_LIMIT,
    workers: int = DEFAULT_WORKERS,
    iterative: bool = False,
) -> SumResult:
    return asyncio.run(calculate_sum_async(limit, workers, iterative))


def main() -> None:
    parser = build_sum_parser("Calculate a sum with asyncio.")
    args = parser.parse_args()
    result = calculate_sum(args.limit, args.workers, args.iterative)
    print_sum_result(result)


if __name__ == "__main__":
    main()
