from __future__ import annotations

import asyncio
import time

import aiohttp

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


async def parse_and_save(url: str, timeout: float = DEFAULT_TIMEOUT) -> PageResult:
    started_at = time.perf_counter()
    try:
        client_timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=client_timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                html = await response.text()
        title = extract_title(html)
        record_id = await asyncio.to_thread(save_hackathon_from_page, url, title)
        status = "created"
        error = None
    except aiohttp.ClientError as exc:
        title = None
        record_id = None
        status = "failed"
        error = f"network or HTTP error: {exc}"
    except (RuntimeError, ValueError, asyncio.TimeoutError) as exc:
        title = None
        record_id = None
        status = "failed"
        error = str(exc)

    elapsed = time.perf_counter() - started_at
    result = PageResult("asyncio", url, title, status, elapsed, record_id, error)
    print_page_result(result)
    return result


async def _parse_with_semaphore(
    url: str,
    semaphore: asyncio.Semaphore,
    timeout: float,
) -> PageResult:
    async with semaphore:
        return await parse_and_save(url, timeout)


async def parse_many_async(
    urls: list[str] | None = None,
    workers: int = DEFAULT_WORKERS,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[PageResult]:
    selected_urls = urls or URLS
    semaphore = asyncio.Semaphore(workers)
    tasks = [
        _parse_with_semaphore(url, semaphore, timeout)
        for url in selected_urls
    ]
    return list(await asyncio.gather(*tasks))


def parse_many(
    urls: list[str] | None = None,
    workers: int = DEFAULT_WORKERS,
    timeout: float = DEFAULT_TIMEOUT,
) -> list[PageResult]:
    return asyncio.run(parse_many_async(urls, workers, timeout))


def main() -> None:
    parser = build_parser("Parse pages with asyncio.")
    args = parser.parse_args()
    parse_many(URLS, args.workers, args.timeout)


if __name__ == "__main__":
    main()
