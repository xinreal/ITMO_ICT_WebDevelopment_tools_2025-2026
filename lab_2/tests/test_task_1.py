from __future__ import annotations

from lab_2.task_1 import asyncio_sum, multiprocessing_sum, threading_sum
from lab_2.task_1.common import expected_sum, split_into_chunks
from lab_2.task_2.common import extract_title


def test_split_into_chunks_covers_full_range_without_gaps() -> None:
    chunks = split_into_chunks(limit=20, workers=6)
    flattened = [value for start, end in chunks for value in range(start, end + 1)]

    assert flattened == list(range(1, 21))


def test_split_into_chunks_has_no_overlaps() -> None:
    chunks = split_into_chunks(limit=101, workers=8)
    seen: set[int] = set()

    for start, end in chunks:
        values = set(range(start, end + 1))
        assert seen.isdisjoint(values)
        seen.update(values)

    assert seen == set(range(1, 102))


def test_expected_sum_formula() -> None:
    assert expected_sum(10) == 55
    assert expected_sum(10_000_000_000_000) == 50_000_000_000_005_000_000_000_000


def test_three_sum_implementations_return_same_result() -> None:
    limit = 10_000
    workers = 4

    threading_result = threading_sum.calculate_sum(limit, workers)
    multiprocessing_result = multiprocessing_sum.calculate_sum(limit, workers)
    asyncio_result = asyncio_sum.calculate_sum(limit, workers)

    assert threading_result.result == expected_sum(limit)
    assert multiprocessing_result.result == expected_sum(limit)
    assert asyncio_result.result == expected_sum(limit)
    assert {
        threading_result.result,
        multiprocessing_result.result,
        asyncio_result.result,
    } == {expected_sum(limit)}


def test_extract_title_normalizes_whitespace() -> None:
    html = "<html><head><title>  Hello\n   Lab 2  </title></head><body></body></html>"

    assert extract_title(html) == "Hello Lab 2"
