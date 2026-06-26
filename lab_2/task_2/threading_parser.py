from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor

import requests

from lab_2.task_2.common import (
    DEFAULT_TIMEOUT,
    DEFAULT_WORKERS,
    PageResult,
    build_parser,
    extract_title,
    print_page_result,
)
from lab_2.task_2.database import save_hackathon_from_page
from lab_2.task_2.urls import URLS


def parse_and_save(url: str, timeout: float = DEFAULT_TIMEOUT) -> PageResult:
    started_at = time.perf_counter()
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        title = extract_title(response.text)
        record_id = save_hackathon_from_page(url, title)
        status = "created"
        error = None
    except requests.RequestException as exc:
        title = None
        record_id = None
        status = "failed"
        error = f"network or HTTP error: {exc}"
    except (RuntimeError, ValueError) as exc:
        title = None
        record_id = None
        status = "failed"
        error = str(exc)

    elapsed = time.perf_counter() - started_at
    result = PageResult("threading", url, title, status, elapsed, record_id, error)
    print_page_result(result)
    return result


def parse_many(
    urls: list[str] | None = None,
    workers: int = DEFAULT_WORKERS,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[PageResult]:
    selected_urls = urls or URLS
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(lambda url: parse_and_save(url, timeout), selected_urls))


def main() -> None:
    parser = build_parser("Parse pages with threading.")
    args = parser.parse_args()
    parse_many(URLS, args.workers, args.timeout)


if __name__ == "__main__":
    main()
